"""
N2 — Spaerck Jones TF-IDF (Term Frequency * Inverse Document Frequency)

Reference:
    Spaerck Jones K. (1972), "A statistical interpretation of term specificity
    and its application in retrieval", Journal of Documentation 28(1):11-21.

Role:
    Stylistic feature vectors over identifier tokens, comment tokens, and
    structure tokens. Captures the vocabulary signature of the source that
    AST shape (N1) misses.

Stdlib only. `collections.Counter` for term frequency; `math.log` for IDF.
Stopword stripping via stdlib frozenset. No sklearn.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Iterable

# Conservative stopword set — tokens too common to discriminate style.
_STOPWORDS = frozenset({
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
    "is", "it", "be", "as", "at", "by", "if", "this", "that",
    "self", "cls", "none", "true", "false",
})


def tf(tokens: Iterable[str]) -> dict:
    """Raw term-frequency counts over `tokens`, lowercased, stopwords stripped."""
    counts: Counter = Counter()
    for tok in tokens:
        t = tok.lower()
        if not t or t in _STOPWORDS:
            continue
        counts[t] += 1
    return dict(counts)


def tfidf_vector(
    tokens: list,
    corpus_df: dict,
    n_docs: int,
) -> dict:
    """Compute TF-IDF vector for a single document against a corpus DF table.

    `corpus_df` maps term -> number of corpus documents containing it.
    `n_docs` is the corpus size. Standard smoothed IDF: log((N+1)/(df+1)) + 1.

    Returns {term: weight}.
    """
    if not tokens:
        return {}
    term_counts = tf(tokens)
    total = sum(term_counts.values()) or 1
    out: dict = {}
    for term, count in term_counts.items():
        df = int(corpus_df.get(term, 0))
        idf = math.log((n_docs + 1) / (df + 1)) + 1.0
        out[term] = (count / total) * idf
    return out
