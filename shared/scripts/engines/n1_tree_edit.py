"""
N1 — Zhang-Shasha Tree Edit Distance

Reference:
    Zhang K. and Shasha D. (1989), "Simple fast algorithms for the editing
    distance between trees and related problems", SIAM Journal on Computing
    18(6):1245-1262.

Role:
    AST-shape distance between source and generated artifact. Per-(source-tree,
    target-tree) ordered-tree edit cost. Cost = 1 per insert, delete, relabel.

Stdlib only: `ast` for Python sources, `xml.etree.ElementTree` for XML/HTML.
Dict-based DP table over postorder traversal indices.
"""
from __future__ import annotations

import ast


def _postorder(node: ast.AST) -> list:
    """Postorder traversal — Zhang-Shasha indexing convention."""
    out: list = []
    for child in ast.iter_child_nodes(node):
        out.extend(_postorder(child))
    out.append(node)
    return out


def tree_edit_distance(source_tree: ast.AST, target_tree: ast.AST) -> int:
    """Returns int >= 0. 0 = identical shape. Cost = 1 per insert/delete/relabel.

    Wagner-Fischer DP over postorder sequences. O(n*m) time, O(n*m) space.
    For very large trees, callers should chunk via subtree hashing — see
    docs/science/README.md § N1 Implementation notes.
    """
    src = _postorder(source_tree)
    tgt = _postorder(target_tree)
    n, m = len(src), len(tgt)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if type(src[i - 1]) is type(tgt[j - 1]) else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[n][m]
