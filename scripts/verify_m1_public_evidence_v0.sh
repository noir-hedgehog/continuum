#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
EXPORT_PATH="${2:-$ROOT/docs/app/data/agents-v0.json}"
MILESTONE_PATH="${3:-$ROOT/docs/milestones/M1-self-continuity-role.md}"
WITNESS_ROOT="${4:-$ROOT/.continuum/witness/m1}"

cd "$ROOT"

LABEL="$EXPORT_PATH"
if [[ "$EXPORT_PATH" == "$ROOT/"* ]]; then
  LABEL="${EXPORT_PATH#$ROOT/}"
fi

echo "Root: $ROOT"
echo "Export: $EXPORT_PATH"
echo "Milestone: $MILESTONE_PATH"
echo "Witness root: $WITNESS_ROOT"
echo

scripts/init_automation_roles_v0.sh "$ROOT"
scripts/refresh_m1_export_if_changed_v0.sh "$ROOT" "$EXPORT_PATH"

echo
echo "== Verify public export digest =="
scripts/check_m1_public_export_digest_v0.sh "$ROOT" "$EXPORT_PATH" "$MILESTONE_PATH" "$LABEL"

if [[ -d "$WITNESS_ROOT" ]]; then
  echo
  echo "== Verify witness bundle manifest digest =="
  scripts/check_m1_witness_bundle_digest_v0.sh "$ROOT" "$MILESTONE_PATH" "$WITNESS_ROOT"
else
  echo
  echo "== Verify witness bundle manifest digest =="
  echo "SKIP (missing witness directory: $WITNESS_ROOT)" >&2
  echo "Hint: run scripts/build_m1_witness_package_v0.sh --root \"$ROOT\" to generate a bundle." >&2
fi

