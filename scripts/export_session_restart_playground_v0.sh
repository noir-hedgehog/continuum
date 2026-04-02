#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
WORKDIR="${2:-$(mktemp -d "${TMPDIR:-/tmp}/continuum-playground-session.XXXXXX")}"
OUTPUT="${3:-$ROOT/docs/playground/scenarios/session-restart-v0.json}"

rm -rf "$WORKDIR/.continuum"
mkdir -p "$WORKDIR/docs"
cat > "$WORKDIR/docs/FOUNDING_THESIS.md" <<'EOF'
# Founding Thesis
EOF
cat > "$WORKDIR/docs/OPERATING_MODEL.md" <<'EOF'
# Operating Model
EOF
cat > "$WORKDIR/docs/TASK_BOARD.md" <<'EOF'
# Task Board
EOF
cat > "$WORKDIR/docs/REVISION_LOG.md" <<'EOF'
# Revision Log
EOF

cd "$WORKDIR"
PYTHONPATH="$ROOT" python3 -m src.cli.main agent init \
  --scope continuum \
  --name main \
  --display-name "Continuum Main"
PYTHONPATH="$ROOT" python3 -m src.cli.main agent profile set \
  --display-name "Continuum Main" \
  --description "Bootstrap agent"
PYTHONPATH="$ROOT" python3 -m src.cli.main memory checkpoint create \
  --scope session_handoff \
  --summary "Checkpoint one" \
  --artifact-ref docs/TASK_BOARD.md \
  --artifact-ref docs/REVISION_LOG.md
MIGRATION_JSON="$(PYTHONPATH="$ROOT" python3 -m src.cli.main migration declare \
  --migration-type session_restart \
  --from-ref session:continuum:run-old \
  --to-ref session:continuum:run-new \
  --reason "Automation restart" \
  --evidence docs/REVISION_LOG.md)"
MIGRATION_EVENT_ID="$(printf '%s' "$MIGRATION_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["event_id"])')"
PYTHONPATH="$ROOT" python3 -m src.cli.main continuity assess \
  --event-id "$MIGRATION_EVENT_ID" \
  --refresh > /dev/null
PYTHONPATH="$ROOT" python3 -m src.cli.main playground export \
  --scenario session_restart_v0 \
  --actor-id agent:continuum:main \
  --output "$OUTPUT"

echo "Exported playground scenario to $OUTPUT"
