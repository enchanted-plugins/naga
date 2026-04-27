"""
N4 — Salton-Wong-Yang Cosine Similarity

Reference:
    Salton G., Wong A., Yang C.S. (1975), "A vector space model for automatic
    indexing", Communications of the ACM 18(11):613-620.

Role:
    Pattern-fidelity score over feature vectors. Combines N1-derived shape
    features, N2-derived vocabulary features, N3-derived naming features into
    a single similarity in [0, 1].

Stdlib only. Pure-Python dot-product and norm via list comprehensions plus
`math.sqrt`. No numpy.
"""
from __future__ import annotations

import math


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """Cosine similarity between two sparse feature dicts.

    Returns 0.0 when either vector is empty or has zero norm; otherwise
    returns dot(a, b) / (||a|| * ||b||) clamped to [0, 1].
    """
    if not vec_a or not vec_b:
        return 0.0
    keys = set(vec_a) & set(vec_b)
    if not keys:
        return 0.0
    dot = sum(float(vec_a[k]) * float(vec_b[k]) for k in keys)
    norm_a = math.sqrt(sum(float(v) ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(float(v) ** 2 for v in vec_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    sim = dot / (norm_a * norm_b)
    if sim < 0.0:
        return 0.0
    if sim > 1.0:
        return 1.0
    return float(sim)
