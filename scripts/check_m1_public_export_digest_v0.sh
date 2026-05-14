#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
EXPORT_PATH="${2:-$ROOT/docs/app/data/agents-v0.json}"
MILESTONE_PATH="${3:-$ROOT/docs/milestones/M1-self-continuity-role.md}"
LABEL="${4:-docs/app/data/agents-v0.json}"

cd "$ROOT"

if [[ ! -f "$EXPORT_PATH" ]]; then
  echo "Missing export file: $EXPORT_PATH" >&2
  exit 2
fi

if [[ ! -f "$MILESTONE_PATH" ]]; then
  echo "Missing milestone note: $MILESTONE_PATH" >&2
  exit 2
fi

python3 - "$EXPORT_PATH" "$MILESTONE_PATH" "$LABEL" <<'PY'
import hashlib
import re
import sys
from pathlib import Path

export_path = Path(sys.argv[1])
milestone_path = Path(sys.argv[2])
label = sys.argv[3]

data = export_path.read_bytes()
actual_sha256 = hashlib.sha256(data).hexdigest()
actual_bytes = len(data)

text = milestone_path.read_text(encoding="utf-8")

sha_pat = re.compile(rf"sha256\({re.escape(label)}\)=([0-9a-f]{{64}})")
bytes_pat = re.compile(rf"bytes\({re.escape(label)}\)=([0-9]+)")

sha_matches = sha_pat.findall(text)
bytes_matches = bytes_pat.findall(text)

expected_sha256 = sha_matches[-1] if sha_matches else None
expected_bytes = int(bytes_matches[-1]) if bytes_matches else None

print(f"Label: {label}")
print(f"Milestone: {milestone_path}")
print(f"Export: {export_path}")
print(f"Actual: sha256={actual_sha256} bytes={actual_bytes}")

if expected_sha256 is None or expected_bytes is None:
  print("Milestone missing expected digest/bytes for this label.", file=sys.stderr)
  sys.exit(3)

print(f"Expected: sha256={expected_sha256} bytes={expected_bytes}")

ok = (actual_sha256 == expected_sha256) and (actual_bytes == expected_bytes)
print("OK" if ok else "MISMATCH")
sys.exit(0 if ok else 4)
PY

