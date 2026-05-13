#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/build_m2_handoff_package_v0.sh [--root <repo_root>] [--out-dir <dir>]

Builds a lightweight M2 handoff bundle under a gitignored directory (default:
.continuum/witness/m2/...) containing:
- selected public docs + exports
- a SHA256/bytes manifest
- a small README describing how to reproduce the bundle from a clean checkout
- a migration metadata stub to fill during the first M2 attempt

This script is meant for public evidence packaging. It does not write new
continuity events; it only snapshots existing repo state.
EOF
}

ROOT=""
OUT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="${2:-}"; shift 2;;
    --out-dir)
      OUT_DIR="${2:-}"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 2;;
  esac
done

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${ROOT}" ]]; then
  ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
fi

if [[ -z "${OUT_DIR}" ]]; then
  OUT_DIR="${ROOT}/.continuum/witness/m2"
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
stage="${OUT_DIR}/stage_${ts}"
bundle_dir="${OUT_DIR}/bundle_${ts}"

mkdir -p "${stage}"

files=(
  "README.md"
  "docs/ROADMAP_V0.md"
  "docs/PUBLIC_MILESTONES_V0.md"
  "docs/AUTOMATION_IDENTITIES_V0.md"
  "docs/OPERATING_MODEL.md"
  "docs/TASK_BOARD.md"
  "docs/REVISION_LOG.md"
  "docs/OPEN_QUESTIONS.md"
  "docs/milestones/M1-self-continuity-role.md"
  "docs/milestones/M2-cross-model-handoff.md"
  "docs/app/data/agents-v0.json"
)

missing=0
for rel in "${files[@]}"; do
  if [[ ! -f "${ROOT}/${rel}" ]]; then
    echo "Missing required file: ${rel}" >&2
    missing=1
  fi
done
if [[ "${missing}" -ne 0 ]]; then
  exit 1
fi

for rel in "${files[@]}"; do
  mkdir -p "${stage}/$(dirname -- "${rel}")"
  cp -p "${ROOT}/${rel}" "${stage}/${rel}"
done

cat > "${stage}/MIGRATION_METADATA_STUB.json" <<'EOF'
{
  "schema": "continuum:m2-migration-metadata-v0",
  "subject": "role:continuum:main-integrator",
  "handoff": {
    "from": {
      "model_family": "pending",
      "model_version": "pending",
      "runtime_surface": "pending"
    },
    "to": {
      "model_family": "pending",
      "model_version": "pending",
      "runtime_surface": "pending"
    }
  },
  "constraints": {
    "policy_or_prompt_notes": "pending"
  },
  "evidence": {
    "before_bundle_id": "pending",
    "after_bundle_id": "pending",
    "assessment_paths": []
  }
}
EOF

cat > "${stage}/WITNESS_README.txt" <<EOF
Continuum M2 handoff bundle (snapshot scaffold)

Built at (UTC): ${ts}

This bundle is a convenience packaging of the repository's *current* M1/M2
handoff-related surfaces. For M2, the evidence only becomes meaningful once a
real cross-model handoff is executed and recorded.

How to reproduce from a clean checkout:
  1) git clone the repo, cd into it
  2) ensure docs/app/data/agents-v0.json is current (safe no-op refresh):
       scripts/refresh_m1_export_if_changed_v0.sh "\$PWD" docs/app/data/agents-v0.json
  3) rebuild this scaffold snapshot:
       scripts/build_m2_handoff_package_v0.sh

During the first real M2 attempt:
  - fill MIGRATION_METADATA_STUB.json (or replace with MIGRATION_METADATA.json)
  - update docs/milestones/M2-cross-model-handoff.md with concrete commands + outputs
EOF

python3 - <<'PY' "${stage}" "${files[@]}"
import hashlib
import json
import os
import sys

stage = sys.argv[1]
files = sys.argv[2:]

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

extra = ["WITNESS_README.txt", "MIGRATION_METADATA_STUB.json"]
entries = []
for rel in files + extra:
    path = os.path.join(stage, rel)
    st = os.stat(path)
    entries.append(
        {
            "path": rel,
            "sha256": sha256_file(path),
            "bytes": st.st_size,
        }
    )

entries.sort(key=lambda e: e["path"])
manifest = {
    "schema": "continuum:witness-manifest-v0",
    "bundle": "M2-cross-model-handoff-scaffold",
    "entries": entries,
}

manifest_path = os.path.join(stage, "WITNESS_MANIFEST.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, sort_keys=True)
    f.write("\n")

bundle_id = sha256_file(manifest_path)
with open(os.path.join(stage, "WITNESS_BUNDLE_ID.txt"), "w", encoding="utf-8") as f:
    f.write(f"bundle_id_sha256(manifest)={bundle_id}\n")

print(bundle_id)
PY

mkdir -p "${bundle_dir}"
cp -pR "${stage}/." "${bundle_dir}/"

echo "Built handoff bundle scaffold:"
echo "  dir=${bundle_dir}"
echo "  manifest=${bundle_dir}/WITNESS_MANIFEST.json"
echo "  bundle_id_file=${bundle_dir}/WITNESS_BUNDLE_ID.txt"

