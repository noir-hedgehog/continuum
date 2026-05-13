#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT="${2:-$ROOT/docs/app/data/agents-v0.json}"

cd "$ROOT"

tmp_out="$(mktemp -t continuum_agents_v0.XXXXXX.json)"
cleanup() {
  set +e
  rm -f "$tmp_out" 2>/dev/null || true
}
trap cleanup EXIT

PYTHONPATH="$ROOT" python3 -m src.cli.main app export \
  --community-id community:continuum:lab \
  --refresh \
  --output "$tmp_out" >/dev/null

python3 - "$tmp_out" <<'PY'
import hashlib
from pathlib import Path
import sys

path = Path(sys.argv[1])
data = path.read_bytes()
print(f"tmp sha256={hashlib.sha256(data).hexdigest()} bytes={len(data)}")
PY

if [[ -f "$OUTPUT" ]]; then
  if cmp -s "$tmp_out" "$OUTPUT"; then
    echo "No change: $OUTPUT already matches the current app export."
    exit 0
  fi
fi

mkdir -p "$(dirname "$OUTPUT")"
mv "$tmp_out" "$OUTPUT"
trap - EXIT
echo "Updated: wrote refreshed app export to $OUTPUT."
