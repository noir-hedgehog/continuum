#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
FIXED_NOW_UTC="${2:-2026-05-12T00:00:00Z}"

cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "error: git not found" >&2
  exit 1
fi

if ! command -v shasum >/dev/null 2>&1; then
  echo "error: shasum not found (macOS: should be available)" >&2
  exit 1
fi

if [[ ! -f "$ROOT/scripts/heartbeat_main_integrator_role_v0.sh" ]]; then
  echo "error: missing scripts/heartbeat_main_integrator_role_v0.sh under $ROOT" >&2
  exit 1
fi

WT_A="$(mktemp -d /tmp/continuum_heartbeat_verify_a.XXXXXX)"
WT_B="$(mktemp -d /tmp/continuum_heartbeat_verify_b.XXXXXX)"

cleanup() {
  set +e
  git -C "$ROOT" worktree remove -f "$WT_A" >/dev/null 2>&1
  git -C "$ROOT" worktree remove -f "$WT_B" >/dev/null 2>&1
  rm -rf "$WT_A" "$WT_B"
}
trap cleanup EXIT INT TERM

git -C "$ROOT" worktree add --detach "$WT_A" HEAD >/dev/null
git -C "$ROOT" worktree add --detach "$WT_B" HEAD >/dev/null

OUT_A="$WT_A/out_agents-v0.json"
OUT_B="$WT_B/out_agents-v0.json"

"$WT_A/scripts/heartbeat_main_integrator_role_v0.sh" "$WT_A" "$OUT_A" "$FIXED_NOW_UTC" >/dev/null
"$WT_B/scripts/heartbeat_main_integrator_role_v0.sh" "$WT_B" "$OUT_B" "$FIXED_NOW_UTC" >/dev/null

if ! cmp -s "$OUT_A" "$OUT_B"; then
  echo "deterministic export mismatch" >&2
  echo "a: $OUT_A" >&2
  echo "b: $OUT_B" >&2
  exit 2
fi

SHA="$(shasum -a 256 "$OUT_A" | awk '{print $1}')"
BYTES="$(wc -c <"$OUT_A" | tr -d ' ')"

echo "deterministic export matches"
echo "fixed_now_utc=$FIXED_NOW_UTC"
echo "sha256=$SHA"
echo "bytes=$BYTES"
