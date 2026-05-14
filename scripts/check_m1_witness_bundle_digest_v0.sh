#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
MILESTONE_PATH="${2:-$ROOT/docs/milestones/M1-self-continuity-role.md}"
WITNESS_ROOT="${3:-$ROOT/.continuum/witness/m1}"

cd "$ROOT"

if [[ ! -f "$MILESTONE_PATH" ]]; then
  echo "Missing milestone note: $MILESTONE_PATH" >&2
  exit 2
fi

if [[ ! -d "$WITNESS_ROOT" ]]; then
  echo "Missing witness directory: $WITNESS_ROOT" >&2
  echo "Hint: run scripts/build_m1_witness_package_v0.sh --root \"$ROOT\" to generate a bundle." >&2
  exit 2
fi

python3 - "$MILESTONE_PATH" "$WITNESS_ROOT" <<'PY'
import hashlib
import re
import sys
from pathlib import Path

milestone_path = Path(sys.argv[1])
witness_root = Path(sys.argv[2])

text = milestone_path.read_text(encoding="utf-8")

expected_pat = re.compile(r"bundle_id_sha256\(manifest\)=([0-9a-f]{64})")
expected_matches = expected_pat.findall(text)
expected_sha256 = expected_matches[-1] if expected_matches else None

bundle_dirs = sorted([p for p in witness_root.glob("bundle_*") if p.is_dir()])
manifest_path = None
latest_bundle_dir = None
for candidate in reversed(bundle_dirs):
  candidate_manifest = candidate / "WITNESS_MANIFEST.json"
  if candidate_manifest.is_file():
    latest_bundle_dir = candidate
    manifest_path = candidate_manifest
    break

if manifest_path is None:
  print(f"No bundle manifests found under: {witness_root}", file=sys.stderr)
  print('Hint: run scripts/build_m1_witness_package_v0.sh --root "$ROOT" to generate a bundle.', file=sys.stderr)
  sys.exit(3)

data = manifest_path.read_bytes()
actual_sha256 = hashlib.sha256(data).hexdigest()
actual_bytes = len(data)

print(f"Milestone: {milestone_path}")
print(f"Witness root: {witness_root}")
print(f"Latest bundle: {latest_bundle_dir.name if latest_bundle_dir else '(unknown)'}")
print(f"Manifest: {manifest_path}")
print(f"Actual: sha256={actual_sha256} bytes={actual_bytes}")

if expected_sha256 is None:
  print("Milestone missing expected bundle manifest digest.", file=sys.stderr)
  sys.exit(3)

print(f"Expected: sha256={expected_sha256}")

ok = actual_sha256 == expected_sha256
print("OK" if ok else "MISMATCH")
sys.exit(0 if ok else 4)
PY
