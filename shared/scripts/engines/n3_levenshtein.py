"""
N3 — Levenshtein Edit Distance

Reference:
    Levenshtein V.I. (1966), "Binary codes capable of correcting deletions,
    insertions, and reversals", Soviet Physics Doklady 10(8):707-710.

Role:
    Naming-convention distance: snake_case vs camelCase vs PascalCase, prefix
    conventions (_internal, kPrefix), suffix conventions (_test, Spec).
    Distance per identifier pair.

Stdlib only. Explicit Wagner-Fischer DP via 2D list. `difflib.SequenceMatcher`
ratio is exposed for callers that prefer a normalized [0,1] similarity.
"""
from __future__ import annotations

import difflib


def name_distance(source_name: str, candidate_name: str) -> int:
    """Wagner-Fischer Levenshtein distance over two identifier strings.

    Returns int >= 0. 0 means identical; max(len(a), len(b)) is the upper bound.
    """
    a = source_name or ""
    b = candidate_name or ""
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,        # deletion
                curr[j - 1] + 1,    # insertion
                prev[j - 1] + cost, # substitution
            )
        prev, curr = curr, prev
    return prev[m]


def name_similarity(source_name: str, candidate_name: str) -> float:
    """Normalized similarity in [0, 1] via difflib.SequenceMatcher.

    1.0 = identical. Useful when the caller wants a similarity instead of an
    edit cost (e.g., for direct entry into N4 cosine vectors).
    """
    return difflib.SequenceMatcher(None, source_name or "", candidate_name or "").ratio()
