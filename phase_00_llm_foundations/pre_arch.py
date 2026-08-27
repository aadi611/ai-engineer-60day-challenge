"""Day 3 — pretraining objectives, scaling laws, and the architecture deltas that matter."""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------- 1. Pretraining objectives ----------
def causal_lm_loss(logits, targets, pad_id=-100):
    """GPT/Llama/Claude-style: predict token t+1 from tokens <=t. Loss on every position."""
    logits = logits[:, :-1].reshape(-1, logits.size(-1))   # drop last (no target)
    targets = targets[:, 1:].reshape(-1)                   # drop first (no context)
    return F.cross_entropy(logits, targets, ignore_index=pad_id)


def mlm_loss(logits, targets, mask):
    """BERT-style: bidirectional, loss only on the ~15% masked positions."""
    return F.cross_entropy(logits[mask], targets[mask])


def mtp_loss(heads_logits, targets, pad_id=-100):
    """Multi-token prediction: k extra heads predict t+1..t+k. Denser signal per step,
    and the heads double as speculative-decoding drafters at inference."""
    total = 0.0
    for k, logits in enumerate(heads_logits, start=1):
        total = total + F.cross_entropy(
            logits[:, :-k].reshape(-1, logits.size(-1)),
            targets[:, k:].reshape(-1),
            ignore_index=pad_id,
        )
    return total / len(heads_logits)


# ---------- 2. RoPE: position injected into Q/K, not added to the embedding ----------
def rope_cache(seq_len, head_dim, base=10000.0, device=None):
    inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2, device=device).float() / head_dim))
    freqs = torch.outer(torch.arange(seq_len, device=device).float(), inv_freq)  # (L, d/2)
    return freqs.cos(), freqs.sin()


def apply_rope(x, cos, sin):
    """x: (B, h, L, d). Rotates each (even, odd) dim pair by an angle proportional to position."""
    x1, x2 = x[..., 0::2], x[..., 1::2]
    cos, sin = cos[None, None, :, :], sin[None, None, :, :]
    return torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1).flatten(-2)


def rope_cache_scaled(seq_len, head_dim, base=10000.0, scale=8.0):
    """Cheapest long-context trick: raise the base (or divide positions) so trained
    rotation frequencies cover a longer range. Used to stretch 8K -> 128K with light tuning."""
    return rope_cache(seq_len, head_dim, base=base * scale)


# ---------- 3. GQA: MHA -> GQA -> MQA is a KV-cache size dial ----------
class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, n_heads, n_kv_heads):
        super().__init__()
        assert n_heads % n_kv_heads == 0
        self.h, self.kv_h = n_heads, n_kv_heads
        self.d_k = d_model // n_heads
        self.rep = n_heads // n_kv_heads          # queries per KV head
        self.Wq = nn.Linear(d_model, n_heads * self.d_k, bias=False)
        self.Wk = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)
        self.Wv = nn.Linear(d_model, n_kv_heads * self.d_k, bias=False)
        self.Wo = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, cos, sin):
        B, L, _ = x.shape
        q = self.Wq(x).view(B, L, self.h, self.d_k).transpose(1, 2)
        k = self.Wk(x).view(B, L, self.kv_h, self.d_k).transpose(1, 2)
        v = self.Wv(x).view(B, L, self.kv_h, self.d_k).transpose(1, 2)
        q, k = apply_rope(q, cos, sin), apply_rope(k, cos, sin)
        k = k.repeat_interleave(self.rep, dim=1)   # share each KV head across a query group
        v = v.repeat_interleave(self.rep, dim=1)
        out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.Wo(out.transpose(1, 2).reshape(B, L, -1))


# ---------- 4. Sparse MoE: swap the dense FFN for top-k routed experts ----------
class SparseMoE(nn.Module):
    def __init__(self, d_model, d_ff, n_experts=8, top_k=2):
        super().__init__()
        self.n_experts, self.top_k = n_experts, top_k
        self.gate = nn.Linear(d_model, n_experts, bias=False)
        self.experts = nn.ModuleList(
            nn.Sequential(nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model))
            for _ in range(n_experts)
        )

    def forward(self, x):
        B, L, D = x.shape
        flat = x.view(-1, D)
        probs = self.gate(flat).softmax(-1)                       # (N, E)
        weights, idx = probs.topk(self.top_k, dim=-1)
        weights = weights / weights.sum(-1, keepdim=True)         # renormalize the top-k

        out = torch.zeros_like(flat)
        for e, expert in enumerate(self.experts):
            hit = (idx == e)
            if not hit.any():
                continue
            tok, slot = hit.nonzero(as_tuple=True)                # which tokens picked expert e
            out.index_add_(0, tok, expert(flat[tok]) * weights[tok, slot, None])

        # load-balancing aux loss: without it the router collapses onto a few experts
        frac = torch.zeros(self.n_experts, device=x.device)
        frac.index_add_(0, idx.reshape(-1), torch.ones(idx.numel(), device=x.device))
        frac = frac / idx.numel()
        aux = self.n_experts * (frac * probs.mean(0)).sum()
        return out.view(B, L, D), aux


# ---------- 5. The back-of-envelope math you get asked to do live ----------
def training_flops(n_params, n_tokens):
    return 6 * n_params * n_tokens                     # ~2 fwd + ~4 bwd per param per token


def chinchilla_optimal(flops):
    """Compute-optimal split: D ~= 20N  =>  C = 6N(20N) = 120N^2."""
    n = math.sqrt(flops / 120)
    return n, 20 * n


def kv_cache_bytes(batch, seq_len, n_layers, n_kv_heads, d_head, dtype_bytes=2):
    return 2 * batch * seq_len * n_layers * n_kv_heads * d_head * dtype_bytes


if __name__ == "__main__":
    n, d = chinchilla_optimal(1e24)
    print(f"1e24 FLOPs -> ~{n/1e9:.1f}B params on ~{d/1e12:.1f}T tokens")

    mha = kv_cache_bytes(1, 128_000, 80, 64, 128) / 1e9
    gqa = kv_cache_bytes(1, 128_000, 80, 8, 128) / 1e9
    print(f"128K-token KV cache: MHA {mha:.1f} GB vs GQA(8) {gqa:.1f} GB")

    x = torch.randn(2, 16, 256)
    cos, sin = rope_cache(16, 32)
    print("GQA out:", GroupedQueryAttention(256, 8, 2)(x, cos, sin).shape)
    y, aux = SparseMoE(256, 512)(x)
    print("MoE out:", y.shape, "aux loss:", round(aux.item(), 4))
