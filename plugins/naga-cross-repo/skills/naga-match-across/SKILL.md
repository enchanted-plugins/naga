---
name: naga-match-across
description: >
  Cross-repo pattern replication. Reads a source artifact in one repository
  tree and generates a matched-form artifact in another, resolving paths via
  the sibling-repo convention (<repo-root>/<sibling>/...). Runs N1+N2+N3+N4
  with N5 threshold gating; escalates to naga-orchestrator when source and
  target domains diverge. Use when the user runs /naga:match-across or asks to
  propagate a pattern from repo A to repo B. Do not use for same-repo
  replication (see /naga:match).
model: sonnet
tools: [Read, Write, Edit, Grep, Glob]
---

# naga-match-across

## Preconditions

- Both `<source-repo>` and `<target-repo>` resolve to existing directories on disk.
- The source artifact within `<source-repo>` exists and is readable.
- If either repo path is missing, fail-fast with a precise error — do NOT create intermediate directories outside the Naga tree.

## Inputs

- **Slash command:** `/naga:match-across <source-repo>/<source-path> <target-repo>/<target-path>`
- **Arguments:**
  - First positional: source path including repo root (sibling-repo convention).
  - Second positional: target path including repo root.

## Steps

1. Resolve both paths. If either is absent, return `{error: "path_not_found", path: ...}`.
2. Auto-invoke `/naga:observe <source>` to capture the fingerprint.
3. Spawn the **naga-shaper** Sonnet agent with the cross-repo flag set; the shaper widens the N4 threshold by 15% per the cross-domain rule.
4. If source and target file extensions differ (e.g., `.py` -> `.md`), spawn **naga-orchestrator** Opus to compute the relaxation set; pass it to the shaper.
5. Write the target artifact via `Write`.
6. Publish `naga.artifact.generated` with the cross-repo paths.

## Outputs

- The generated artifact at `<target-repo>/<target-path>`.
- One `naga.artifact.generated` event.
- Console: `(score, ci_low, ci_high, N, relaxation_set, chunks_dropped)`.

## Handoff

If the developer maintains both repos, they typically run `/naga:validate` from each side to confirm the pattern transferred cleanly.

## Failure modes

- **F02 fabrication** — never invent a path under a repo root that does not exist. Fail-fast.
- **F09 parallel race** — never write the target file from two parallel shaper invocations. Serialize.
- **F04 task drift** — never edit the source repo. Read-only on source; Write only on target.
