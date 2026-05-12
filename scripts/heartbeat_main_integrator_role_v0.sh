#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT="${2:-$ROOT/docs/app/data/agents-v0.json}"
FIXED_NOW_UTC="${3:-}"

cd "$ROOT"
export PYTHONPATH="$ROOT"

ROLE_ID="role:continuum:main-integrator"
ROLE_RECORD="$ROOT/.continuum/agents/role__continuum__main-integrator.json"
MAIN_AGENT_ID="agent:continuum:main"
MAIN_AGENT_RECORD="$ROOT/.continuum/agents/agent__continuum__main.json"

if [[ -n "$FIXED_NOW_UTC" ]]; then
  export CONTINUUM_NOW="$FIXED_NOW_UTC"
  export CONTINUUM_DOMAIN_TOKEN="$FIXED_NOW_UTC"
fi

if [[ ! -f "$ROLE_RECORD" ]]; then
  python3 -m src.cli.main role init \
    --scope continuum \
    --name main-integrator \
    --display-name "Continuum Main Integrator" \
    --description "Public project role responsible for keeping the Continuum repository coherent across roadmap, milestones, runtime, demos, and witness exports." \
    --operator-disclosure "Occupied by scheduled model sessions; continuity evidence lives in repository exports."
fi

python3 -m src.cli.main agent use --agent-id "$ROLE_ID"

python3 -m src.cli.main agent profile set \
  --display-name "Continuum Main Integrator" \
  --description "Repository-backed public role. Occupied by different sessions that reconstruct the repo and leave auditable continuity evidence." \
  --operator-disclosure "Occupied by scheduled model sessions; see docs/ROADMAP_V0.md and docs/OPERATING_MODEL.md." \
  --artifact-ref docs/ROADMAP_V0.md \
  --artifact-ref docs/PUBLIC_MILESTONES_V0.md \
  --artifact-ref docs/OPERATING_MODEL.md \
  --artifact-ref docs/TASK_BOARD.md \
  --artifact-ref docs/REVISION_LOG.md

python3 -m src.cli.main memory checkpoint create \
  --scope session_handoff \
  --summary "Reconstructed Continuum continuity bundle for role:continuum:main-integrator during scheduled heartbeat; refreshed public export." \
  --artifact-ref docs/ROADMAP_V0.md \
  --artifact-ref docs/PUBLIC_MILESTONES_V0.md \
  --artifact-ref docs/OPERATING_MODEL.md \
  --artifact-ref docs/TASK_BOARD.md \
  --artifact-ref docs/REVISION_LOG.md

NOW_UTC="${CONTINUUM_NOW:-$(date -u +"%Y-%m-%dT%H:%M:%SZ")}"
TO_REF="session:continuum:main-integrator:${NOW_UTC}"
FROM_REF="$(
  python3 - <<'PY'
import json
from pathlib import Path

path = Path(".continuum/state/agents/role__continuum__main-integrator.json")
if not path.exists():
    print("session:continuum:main-integrator:bootstrap")
    raise SystemExit(0)
state = json.loads(path.read_text(encoding="utf-8"))
lineage = state.get("migration_lineage") or []
if not lineage:
    print("session:continuum:main-integrator:bootstrap")
    raise SystemExit(0)
latest = lineage[-1]
payload = latest.get("payload", {}).get("migration", {})
print(payload.get("to_ref") or "session:continuum:main-integrator:bootstrap")
PY
)"

python3 -m src.cli.main migration declare \
  --migration-type session_restart \
  --from-ref "$FROM_REF" \
  --to-ref "$TO_REF" \
  --reason "Scheduled heartbeat resumed; repository reconstructed and public export refreshed." \
  --evidence docs/ROADMAP_V0.md \
  --evidence docs/PUBLIC_MILESTONES_V0.md \
  --evidence docs/TASK_BOARD.md \
  --evidence docs/REVISION_LOG.md \
  --expected-continuity-class same_agent

if [[ ! -f "$MAIN_AGENT_RECORD" ]]; then
  python3 -m src.cli.main agent init \
    --scope continuum \
    --name main \
    --display-name "Continuum Main"
fi

python3 -m src.cli.main agent use --agent-id "$MAIN_AGENT_ID"

python3 -m src.cli.main continuity assess \
  --actor-id "$ROLE_ID" \
  --scope repository \
  --refresh

python3 -m src.cli.main app export \
  --community-id community:continuum:lab \
  --refresh \
  --output "$OUTPUT"

echo "Heartbeat complete; exported app data to $OUTPUT"
