#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(pwd)}"
WORKDIR="${2:-$(mktemp -d "${TMPDIR:-/tmp}/continuum-constitutional-demo.XXXXXX")}"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

COMMUNITY_ID="community:continuum:lab"

json_get() {
  python3 -c "import json,sys; data=json.load(sys.stdin); print($1)"
}

echo "== Demo workdir =="
echo "$WORKDIR"

echo "== Initialize agent =="
python3 -m src.cli.main agent init \
  --scope continuum \
  --name main \
  --display-name "Continuum Main" \
  --description "Constitutional conflict demo operator"

echo "== Grant community membership =="
python3 -m src.cli.main governance membership grant \
  --community-id "$COMMUNITY_ID" \
  --member-agent-id agent:continuum:main \
  --membership-status active \
  --role maintainer \
  --role member \
  --sponsor-ref docs/FOUNDING_THESIS.md

echo "== Publish root constitution =="
ROOT_JSON=$(python3 -m src.cli.main governance constitution set \
  --community-id "$COMMUNITY_ID" \
  --title "Continuum Constitution v1" \
  --constitution-version "v1" \
  --amended-at "2026-03-22T00:00:00Z" \
  --artifact-ref docs/specs/CONSTITUTION_LINEAGE_V0.md)
echo "$ROOT_JSON"
ROOT_ID=$(printf '%s\n' "$ROOT_JSON" | json_get 'data["payload"]["constitution"]["constitution_id"]')

echo "== Publish first conflicting branch =="
BRANCH_A_JSON=$(python3 -m src.cli.main governance constitution set \
  --community-id "$COMMUNITY_ID" \
  --title "Continuum Constitution v2-a" \
  --constitution-version "v2-a" \
  --supersedes "$ROOT_ID" \
  --amended-at "2026-03-22T01:00:00Z" \
  --artifact-ref docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
echo "$BRANCH_A_JSON"
BRANCH_A_ID=$(printf '%s\n' "$BRANCH_A_JSON" | json_get 'data["payload"]["constitution"]["constitution_id"]')

echo "== Publish second conflicting branch with execution-proof requirement =="
CONTINUITY_POLICIES='{"case_assign":{"allow_subject_self_assign":false,"allowed_standings":["clear"],"required_roles":["maintainer"]},"case_decide":{"allow_opener_as_decider":false,"allow_subject_self_decide":false,"allowed_standings":["clear"],"min_assessment_count":1,"require_distinct_assessors":false,"required_roles":["maintainer","reviewer"]},"case_open":{"allow_subject_self_open":false,"allowed_standings":["clear"],"required_roles":["maintainer","reviewer"]},"constitution_resolution":{"allowed_standings":["clear"],"required_roles":["maintainer"],"require_proposal_ref":false,"require_execution_receipt":true}}'
BRANCH_B_JSON=$(python3 -m src.cli.main governance constitution set \
  --community-id "$COMMUNITY_ID" \
  --title "Continuum Constitution v2-b" \
  --constitution-version "v2-b" \
  --supersedes "$ROOT_ID" \
  --amended-at "2026-03-22T01:05:00Z" \
  --continuity-policies-json "$CONTINUITY_POLICIES" \
  --artifact-ref docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
echo "$BRANCH_B_JSON"
BRANCH_B_ID=$(printf '%s\n' "$BRANCH_B_JSON" | json_get 'data["payload"]["constitution"]["constitution_id"]')

echo "== Submit constitutional proposal =="
PROPOSAL_JSON=$(python3 -m src.cli.main governance proposal submit \
  --community-id "$COMMUNITY_ID" \
  --proposal-type constitutional \
  --title "Recognize canonical constitutional branch" \
  --summary "Select the branch that should count as canonical for replay." \
  --affected-ref "$BRANCH_A_ID" \
  --affected-ref "$BRANCH_B_ID" \
  --artifact-ref docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
echo "$PROPOSAL_JSON"
PROPOSAL_ID=$(printf '%s\n' "$PROPOSAL_JSON" | json_get 'data["payload"]["proposal"]["proposal_id"]')

echo "== Record branch resolution =="
RESOLUTION_JSON=$(python3 -m src.cli.main governance constitution resolve \
  --community-id "$COMMUNITY_ID" \
  --parent-constitution-id "$ROOT_ID" \
  --recognized-constitution-id "$BRANCH_B_ID" \
  --rejected-constitution-id "$BRANCH_A_ID" \
  --proposal-ref "$PROPOSAL_ID" \
  --reason "Select the canonical branch, but require execution proof before replay accepts it." \
  --artifact-ref docs/specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
echo "$RESOLUTION_JSON"
RESOLUTION_ID=$(printf '%s\n' "$RESOLUTION_JSON" | json_get 'data["payload"]["constitution_resolution"]["resolution_id"]')

echo "== Governance state before execution proof =="
python3 -m src.cli.main query governance-state \
  --community-id "$COMMUNITY_ID" \
  --refresh

echo "== Record constitution execution receipt =="
python3 -m src.cli.main governance execute record \
  --community-id "$COMMUNITY_ID" \
  --execution-type constitution_execution \
  --governed-ref "$RESOLUTION_ID" \
  --governed-ref "$PROPOSAL_ID" \
  --output-ref "doc://constitution-resolution/branch-b-finalized" \
  --result-summary "Execution proof recorded for the canonical constitutional branch." \
  --artifact-ref docs/DEMO_CONSTITUTIONAL_CONFLICT_V0.md

echo "== Governance state after execution proof =="
python3 -m src.cli.main query governance-state \
  --community-id "$COMMUNITY_ID" \
  --refresh

echo "Constitutional conflict demo complete."
