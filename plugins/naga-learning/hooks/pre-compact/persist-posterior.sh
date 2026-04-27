#!/usr/bin/env bash
# naga-learning: PreCompact hook.
# Fold any queued fidelity observations into the N5 per-(pattern-class x
# target-domain) posterior. Persists posterior.json + learnings.jsonl
# atomically. Advisory-only, fail-open. MUST exit 0.

if [[ -n "${CLAUDE_SUBAGENT:-}" ]]; then
  exit 0
fi

trap 'exit 0' ERR INT TERM
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
SHARED_SCRIPTS="$(cd "${PLUGIN_ROOT}/../.." && pwd)/shared/scripts"

python3 "${SHARED_SCRIPTS}/engines/n5_gauss.py" "$PLUGIN_ROOT" 2>/dev/null || true
exit 0
