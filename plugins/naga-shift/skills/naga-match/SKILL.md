---
name: naga-match
description: >
  Generates a target artifact whose N4 cosine fidelity to the source fingerprint
  clears the per-(pattern-class, target-domain) p10 threshold from the N5
  posterior. Loop: emit chunk, score, rewrite below threshold (cap 2 attempts),
  drop on third. Use when the user runs /naga:match or asks to generate a new
  artifact in the same shape as an existing one. Do not use for fingerprint-only
  reports (see /naga:fingerprint) or for cross-repo work (see /naga:match-across).
model: sonnet
tools: [Read, Write, Edit, Grep, Glob]
---

# naga-match

## Preconditions

- The source has been fingerprinted (`plugins/naga-observe/state/patterns/<hash>.json` exists). If not, the skill auto-runs `/naga:observe <source>` first.
- The N5 posterior at `plugins/naga-learning/state/posterior.json` is readable. Cold-start default: p10 = 0.6.

## Inputs

- **Slash command:** `/naga:match <source> <target>`
- **Arguments:**
  - `source` — path to the source artifact (must already be fingerprinted, or auto-fingerprinted here).
  - `target` — path where the new artifact will be written.

## Steps

1. Resolve the source fingerprint. If missing, invoke `/naga:observe <source>` and continue.
2. Read the N5 posterior; pick the (pattern_class, target_domain) p10 threshold. Mark `cold_start: true` when N=0.
3. Spawn the **naga-shaper** Sonnet agent with `{source_fingerprint, threshold, target_path}` and a structured-return clause.
4. The shaper emits chunk-by-chunk; each chunk is scored against the source vector via N4 cosine; chunks below threshold get one rewrite, then are dropped.
5. Aggregate chunk-level cosines into `(score, ci_low, ci_high, N)` via `bootstrap_ci`.
6. If source/target domains diverge (e.g., `.py` source -> `.md` target), the shaper escalates to **naga-orchestrator** Opus for the relaxation set; the shaper re-runs with the relaxed feature subset.
7. Write the target artifact via `Write`.
8. Publish `naga.artifact.generated` with `{source_path, target_path, fidelity_score, ci_low, ci_high, N}`.

## Outputs

- The generated artifact at `<target>`.
- One `naga.artifact.generated` event on the bus.
- Console: `(score, ci_low, ci_high, N, chunks_dropped)`.

## Handoff

If the developer wants an independent fidelity check, they run `/naga:validate <target> <source>` — the validator re-scores cold against the same fingerprint.

## Failure modes

- **F11 reward hacking** — never weaken the N5 threshold to pass a chunk. The threshold is read-only here; only naga-learning writes it.
- **F12 degeneration loop** — same chunk rewrite loops below threshold. Hard cap: 2 attempts per chunk; drop on the third.
- **F04 task drift** — extending into prompt-engineering. Naga replicates; that's Wixie's surface.
