# Phase 0: LLM & Transformer Foundations (Days 1-6)

Interview-grade depth on the internals — this is where "I use LangChain" gets
replaced with "here's what's actually happening in the forward pass."

## Days

- **Day 1** — Attention & multi-head attention, positional encoding. Implement scaled dot-product attention from scratch in NumPy/PyTorch (no library shortcuts) — this is the single most common "explain from first principles" ask.
- **Day 2** — Tokenization (BPE, SentencePiece), embeddings, context windows. Train a small BPE tokenizer on a toy corpus.
- **Day 3** — Pretraining objectives, scaling laws, and how GPT/Llama/Claude/Gemini architectures actually differ (dense vs MoE, context length tricks, attention variants).
- **Day 4** — Fine-tuning: full fine-tune vs LoRA/QLoRA vs other PEFT methods, instruction tuning. Run a small LoRA fine-tune end to end.
- **Day 5** — Alignment: RLHF, DPO, RLAIF, and practical guardrail techniques.
- **Day 6** — 🎯 Inference optimization: KV cache, quantization (GPTQ/AWQ), speculative decoding, continuous batching. Then System Design #1: "Design a low-latency LLM inference service" (see [../system_design/README.md](../system_design/README.md)).

## Resourc



- ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762) — the paper, worth re-reading start to finish
- [Hugging Face Transformers docs](https://huggingface.co/docs/transformers)
- [Hugging Face PEFT docs](https://huggingface.co/docs/peft) (LoRA/QLoRA)

## Deliverable

A from-scratch attention implementation + notes doc you could talk through on a whiteboard, no slides.
