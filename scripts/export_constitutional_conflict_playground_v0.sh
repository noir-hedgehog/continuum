#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
WORKDIR="${2:-$(mktemp -d "${TMPDIR:-/tmp}/continuum-playground-export.XXXXXX")}"
OUTPUT="${3:-$ROOT/docs/playground/scenarios/constitutional-conflict-v0.json}"

"$ROOT/scripts/demo_constitutional_conflict_v0.sh" "$ROOT" "$WORKDIR"

PYTHONPATH="$ROOT" python3 -m src.cli.main playground export \
  --scenario constitutional_conflict_v0 \
  --community-id community:continuum:lab \
  --output "$OUTPUT"

echo "Exported playground scenario to $OUTPUT"
