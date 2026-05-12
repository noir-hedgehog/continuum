#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT="${2:-$ROOT/docs/app/data/agents-v0.json}"

cd "$ROOT"
PYTHONPATH="$ROOT" python3 -m src.cli.main app export \
  --community-id community:continuum:lab \
  --refresh \
  --output "$OUTPUT"

echo "Exported app data to $OUTPUT"
