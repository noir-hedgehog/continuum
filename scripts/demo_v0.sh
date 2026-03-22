#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

COMMUNITY_ID="community:continuum:lab"

echo "== Initialize agent =="
python3 -m src.cli.main agent init \
  --scope continuum \
  --name main \
  --display-name "Continuum Main" \
  --description "Primary repository-local Continuum agent"

echo "== Publish profile =="
python3 -m src.cli.main agent profile set \
  --display-name "Continuum Main" \
  --description "Primary repository-local Continuum agent" \
  --operator-disclosure "Founder-supervised local prototype operator" \
  --artifact-ref docs/FOUNDING_THESIS.md

echo "== Create continuity evidence =="
python3 -m src.cli.main memory checkpoint create \
  --scope session_handoff \
  --summary "Quickstart checkpoint after repository reconstruction" \
  --artifact-ref docs/TASK_BOARD.md

python3 -m src.cli.main migration declare \
  --migration-type session_restart \
  --from-ref session:continuum:quickstart-old \
  --to-ref session:continuum:quickstart-new \
  --reason "Quickstart continuity replay" \
  --evidence docs/REVISION_LOG.md \
  --artifact-ref docs/OPERATOR_RUNBOOK_V0.md

ASSESSMENT_JSON=$(python3 -m src.cli.main continuity assess --refresh)
echo "$ASSESSMENT_JSON"
ASSESSMENT_ID=$(printf '%s\n' "$ASSESSMENT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["assessment_id"])')

echo "== Governance bootstrap =="
python3 -m src.cli.main governance constitution set \
  --community-id "$COMMUNITY_ID" \
  --artifact-ref docs/specs/GOVERNANCE_MODEL_V0.md

python3 -m src.cli.main governance membership grant \
  --community-id "$COMMUNITY_ID" \
  --member-agent-id agent:continuum:main \
  --membership-status active \
  --role maintainer \
  --role reviewer \
  --role member \
  --sponsor-ref docs/FOUNDING_THESIS.md

echo "== Proposal and vote =="
PROPOSAL_JSON=$(python3 -m src.cli.main governance proposal submit \
  --community-id "$COMMUNITY_ID" \
  --proposal-type operational \
  --title "Adopt repository-local continuity demo" \
  --summary "Run the local continuity and governance bootstrap as the v0 lab procedure." \
  --affected-ref docs/OPERATOR_RUNBOOK_V0.md \
  --artifact-ref docs/BUILD_PLAN_12_WEEKS.md)
echo "$PROPOSAL_JSON"
PROPOSAL_ID=$(printf '%s\n' "$PROPOSAL_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["payload"]["proposal"]["proposal_id"])')

python3 -m src.cli.main governance vote cast \
  --community-id "$COMMUNITY_ID" \
  --proposal-id "$PROPOSAL_ID" \
  --choice for \
  --artifact-ref docs/specs/GOVERNANCE_MODEL_V0.md

echo "== Useful work loop =="
WORK_JSON=$(python3 -m src.cli.main work item create \
  --community-id "$COMMUNITY_ID" \
  --title "Maintain continuity demo" \
  --intent "Keep the repository-local continuity demo replayable." \
  --work-type maintenance \
  --scope-ref docs/OPERATOR_RUNBOOK_V0.md \
  --deliverable-ref tests/fixtures/continuum_demo_v0.json \
  --success-criterion "Demo fixtures and runbook remain aligned.")
echo "$WORK_JSON"
WORK_ID=$(printf '%s\n' "$WORK_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["payload"]["work_item"]["work_id"])')

python3 -m src.cli.main work claim submit \
  --community-id "$COMMUNITY_ID" \
  --work-id "$WORK_ID" \
  --claim-type submit_maintenance \
  --basis-ref docs/OPERATOR_RUNBOOK_V0.md

RECEIPT_JSON=$(python3 -m src.cli.main work receipt record \
  --community-id "$COMMUNITY_ID" \
  --work-id "$WORK_ID" \
  --receipt-type completion \
  --output-ref tests/fixtures/continuum_demo_v0.json \
  --result-summary "Continuity demo fixtures and operator path remain replayable." \
  --artifact-ref docs/QUICKSTART_V0.md \
  --evidence-ref tests/fixtures/continuum_demo_v0.json)
echo "$RECEIPT_JSON"
RECEIPT_ID=$(printf '%s\n' "$RECEIPT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["payload"]["work_receipt"]["receipt_id"])')

EVAL_JSON=$(python3 -m src.cli.main work evaluation record \
  --community-id "$COMMUNITY_ID" \
  --receipt-id "$RECEIPT_ID" \
  --decision accepted \
  --criteria-result demo_replay=pass \
  --reason-ref docs/specs/USEFUL_WORK_LEGITIMACY_V0.md)
echo "$EVAL_JSON"
EVALUATION_ID=$(printf '%s\n' "$EVAL_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["payload"]["work_evaluation"]["evaluation_id"])')

python3 -m src.cli.main governance reward decide \
  --community-id "$COMMUNITY_ID" \
  --receipt-id "$RECEIPT_ID" \
  --reward-type capability_attestation \
  --policy-ref docs/specs/USEFUL_WORK_LEGITIMACY_V0.md

echo "== Export anchors =="
python3 -m src.cli.main anchor export \
  --anchor-type continuity_assessment_root \
  --assessment-id "$ASSESSMENT_ID"

python3 -m src.cli.main anchor export \
  --anchor-type governance_state_root \
  --community-id "$COMMUNITY_ID" \
  --refresh

echo "== Final anchor list =="
python3 -m src.cli.main anchor list

echo "Demo complete."
