"""Day 1 — scaled dot-product attention, multi-head attention, positional encoding."""
import math
import numpy as np
import torch
import torch.nn as nn

# ---------- 1. NumPy version (pure math, no autograd) ----------
def softmax_np(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)          # numerical stability
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def sdpa_np(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.swapaxes(-2, -1) / np.sqrt(d_k)   # (..., Lq, Lk)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    attn = softmax_np(scores)
    return attn @ V, attn                            # (..., Lq, d_v)


# ---------- 2. PyTorch version ----------
def sdpa(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    attn = scores.softmax(dim=-1)
    return attn @ V, attn


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.h, self.d_k = n_heads, d_model // n_heads
        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)
        self.Wo = nn.Linear(d_model, d_model)

    def _split(self, x):                             # (B,L,D) -> (B,h,L,d_k)
        B, L, _ = x.shape
        return x.view(B, L, self.h, self.d_k).transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        B, L, _ = q.shape
        Q, K, V = self._split(self.Wq(q)), self._split(self.Wk(k)), self._split(self.Wv(v))
        if mask is not None and mask.dim() == 2:
            mask = mask[None, None]                  # broadcast over B and heads
        out, attn = sdpa(Q, K, V, mask)              # (B,h,L,d_k)
        out = out.transpose(1, 2).contiguous().view(B, L, self.h * self.d_k)
        return self.Wo(out), attn


# ---------- 3. Sinusoidal positional encoding ----------
def positional_encoding(max_len, d_model):
    pos = torch.arange(max_len).unsqueeze(1).float()             # (L,1)
    i = torch.arange(0, d_model, 2).float()                      # (D/2,)
    div = torch.exp(-math.log(10000.0) * i / d_model)            # 1/10000^(2i/d)
    pe = torch.zeros(max_len, d_model)
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe                                                    # (L,D)


def causal_mask(L):
    return torch.tril(torch.ones(L, L))                          # 1 = keep, 0 = block


if __name__ == "__main__":
    B, L, D, H = 2, 5, 16, 4
    x = torch.randn(B, L, D) + positional_encoding(L, D)
    mha = MultiHeadAttention(D, H)
    out, attn = mha(x, x, x, mask=causal_mask(L))
    print(out.shape, attn.shape)                                 # (2,5,16) (2,4,5,5)
    print(attn[0, 0].sum(-1))                                    # each row sums to 1
