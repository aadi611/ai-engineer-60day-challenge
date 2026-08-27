"""Day 2 — BPE tokenizer from scratch, embeddings, context windows."""
from collections import Counter
import torch
import torch.nn as nn

EOW = "</w>"  # end-of-word marker: keeps "in" (prefix) distinct from "in" (whole word)


def _merge(symbols, pair):
    """Replace every adjacent occurrence of `pair` with the joined symbol."""
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


class BPETokenizer:
    def __init__(self):
        self.merges = {}   # (a, b) -> rank (lower = learned earlier = applied first)
        self.stoi = {}
        self.itos = {}

    # ---------- training ----------
    def train(self, corpus, num_merges=50):
        freqs = Counter(w for line in corpus for w in line.lower().split())
        splits = {w: tuple(w) + (EOW,) for w in freqs}

        for rank in range(num_merges):
            pairs = Counter()
            for w, f in freqs.items():
                s = splits[w]
                for i in range(len(s) - 1):
                    pairs[(s[i], s[i + 1])] += f
            if not pairs:
                break
            best, count = pairs.most_common(1)[0]
            if count < 2:                      # stop merging one-off pairs
                break
            self.merges[best] = rank
            splits = {w: _merge(s, best) for w, s in splits.items()}

        base = {c for w in freqs for c in w} | {EOW}
        learned = {t for s in splits.values() for t in s}
        tokens = ["<pad>", "<unk>"] + sorted(base | learned)
        self.stoi = {t: i for i, t in enumerate(tokens)}
        self.itos = {i: t for t, i in self.stoi.items()}
        return self

    # ---------- inference ----------
    def _encode_word(self, word):
        symbols = tuple(word) + (EOW,)
        while len(symbols) > 1:
            candidates = [(self.merges[p], p) for p in zip(symbols, symbols[1:]) if p in self.merges]
            if not candidates:
                break
            symbols = _merge(symbols, min(candidates)[1])   # apply lowest-rank merge first
        return list(symbols)

    def tokenize(self, text):
        return [t for w in text.lower().split() for t in self._encode_word(w)]

    def encode(self, text):
        unk = self.stoi["<unk>"]
        return [self.stoi.get(t, unk) for t in self.tokenize(text)]

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids).replace(EOW, " ").strip()


# ---------- context windows: chunk a long id stream for training ----------
def sliding_windows(ids, block_size, stride=None):
    """Returns (x, y) next-token-prediction pairs. stride < block_size = overlap."""
    stride = stride or block_size
    xs, ys = [], []
    for i in range(0, len(ids) - block_size, stride):
        xs.append(ids[i:i + block_size])
        ys.append(ids[i + 1:i + block_size + 1])
    return torch.tensor(xs), torch.tensor(ys)


if __name__ == "__main__":
    corpus = [
        "low lower lowest",
        "new newer newest",
        "wide wider widest",
        "the lowest newer widest one",
    ]
    tok = BPETokenizer().train(corpus, num_merges=30)

    print("vocab size:", len(tok.stoi))
    print("first merges:", list(tok.merges)[:8])
    print("tokens:", tok.tokenize("lowest newer unseenword"))   # subwords handle OOV
    ids = tok.encode("the lowest newer one")
    print("ids:", ids, "->", tok.decode(ids))

    # embeddings: a lookup table, not a matmul with a one-hot
    emb = nn.Embedding(len(tok.stoi), 32, padding_idx=tok.stoi["<pad>"])
    print("embedded:", emb(torch.tensor(ids)).shape)            # (L, 32)

    stream = tok.encode(" ".join(corpus) * 5)
    x, y = sliding_windows(stream, block_size=8, stride=4)
    print("windows:", x.shape, y.shape)
