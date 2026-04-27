---
name: naga-fingerprint
description: >
  Read-only pattern report via N2 Spaerck Jones TF-IDF and N3 Levenshtein
  naming-convention scan. Returns the top-N stylistic terms and the naming
  convention distribution; performs no generation and writes no state outside
  the report. Use when the user runs /naga:fingerprint or asks "what pattern
  does this file follow?" without intending to replicate it. Do not use for
  fingerprint persistence (see /naga:observe) or for generation (see
  /naga:match).
model: haiku
tools: [Read, Grep, Glob]
---

# naga-fingerprint

## Preconditions

- The `<source>` path exists and is readable.
- The skill makes no state writes; it returns a console report only.

## Inputs

- **Slash command:** `/naga:fingerprint <source>`
- **Arguments:** `source` — absolute or repo-relative path.

## Steps

1. Read the source file with the Read tool.
2. Spawn the **naga-fingerprinter** Haiku agent with the content and a structured-return clause demanding `{n2_terms, n3_naming}`.
3. Format the report as a console table:
   - top-15 N2 terms with weights.
   - N3 naming distribution: `{snake, camel, pascal, screaming, mixed}` counts.
4. Do NOT persist anything. Do NOT publish to the bus. Read-only.

## Outputs

- Console table only. Zero state writes, zero events.

## Handoff

If the developer wants to capture the fingerprint for later replication, they run `/naga:observe <source>`.

## Failure modes

- **F02 fabrication** — never invent a term not present in the source.
- **F08 tool mis-invocation** — never use Write or Edit; this skill is read-only.
