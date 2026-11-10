# Phase 0: Foundations: Python, LLM APIs & Internals (Days 1-8)

Back to basics, done properly. By Day 8 you should be able to whiteboard the forward
pass, explain how a reasoning model was trained, and know why your API bill looks the way it does.

> **v1 reference:** your v1 work is in [../archive/v1/phase_00_llm_foundations/](../archive/v1/phase_00_llm_foundations/)
> (`bpe.py`, `dot.py`, `pre_arch.py`). **Rewrite from scratch first, then diff against v1.**
> Note that v1 `bpe.py` has a broken import line (`import time from date.time`) worth fixing in your head.

## Days

- **Day 1: Toolchain + first API calls + secrets hygiene.**
  `uv` project setup, type hints, Pydantic v2 models, `async`/`httpx`. Call the Claude Messages API and the
  OpenAI API: system prompt, multi-turn, streaming, token usage in the response.
  🔐 *Security lens:* keys in `.env` only, `.env` in `.gitignore`, add a **gitleaks** pre-commit hook today, and
  never print keys in logs.
- **Day 2: Tokenization & embeddings.** Train a byte-level BPE on a toy corpus (`bpe.py`). Why token counts ≠
  word counts, why some languages and code cost more, and what an embedding space captures.
  🔐 *Lens:* tokenization quirks are an attack surface (glitch tokens, Unicode/homoglyph smuggling, invisible tag characters).
- **Day 3: Attention from scratch.** Scaled dot-product, the √d_k scaling, causal mask, multi-head, sinusoidal
  positional encodings → **RoPE**. NumPy first, then PyTorch (`attention.py`).
- **Day 4: Pretraining, scaling laws & architecture variants.** Next-token prediction, Chinchilla scaling,
  dense vs **Mixture-of-Experts**, MHA vs GQA/MQA, sliding-window/long-context tricks, multimodal encoders.
- **Day 5: Post-training.** SFT → LoRA/QLoRA (run a tiny LoRA on a small model) → RLHF (reward model + PPO) →
  DPO → Constitutional AI / RLAIF → **RL with verifiable rewards (RLVR) & GRPO** (how reasoning models are trained).
- **Day 6: Reasoning models & test-time compute.** Extended thinking, thinking budgets, latency/cost tradeoffs,
  prompting reasoning vs non-reasoning models, and when a small fast model wins.
- **Day 7: The API surface that actually matters in production.** Structured outputs / JSON schema, tool-calling
  basics, **prompt caching**, batch APIs, context windows and context rot. Intro to *context engineering*
  as the successor to "prompt engineering".
- **Day 8: 🎯 Inference optimization + SD #1.** KV cache, PagedAttention (vLLM), quantization (INT8/INT4, GPTQ/AWQ,
  FP8), speculative decoding, continuous batching, prefill vs decode. Then **SD #1:** *Design a low-latency LLM
  inference service* (see [../system_design/](../system_design/README.md)).

## Resources

- ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762)
- Karpathy: [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) · [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)
- [DeepSeek-R1 paper](https://arxiv.org/abs/2501.12948) (RLVR/GRPO in practice)
- [Hugging Face PEFT docs](https://huggingface.co/docs/peft)
- [vLLM docs](https://docs.vllm.ai/)
- [Anthropic docs](https://docs.claude.com/) (Messages API, prompt caching, extended thinking, structured outputs)
- [OpenAI API docs](https://platform.openai.com/docs)

## Deliverables

- `attention.py`, `bpe.py`, a LoRA notebook, and `api_basics.py` (streaming + structured output + caching demo)
- A one-page "transformer + reasoning model" cheat sheet you could talk through with no slides
- SD #1 write-up
