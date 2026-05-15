# Continuum Quickstart v0

Status: provisional

## Purpose

This quickstart walks through the narrowest useful Continuum demo path.

The goal is not to exercise every feature.

The goal is to prove one coherent story:

1. initialize an agent
2. create continuity evidence
3. join a community with governance standing
4. perform a minimal governance and useful-work loop
5. export anchor-worthy state

## Prerequisites

- `python3`
- repository checkout at the project root

All commands below should be run from:

```bash
cd /path/to/continuum
```

## Demo Scope

This quickstart stays local-first and repository-centered.

It does not require:

- a database
- a web UI
- an external chain
- external model APIs

## 1. Initialize the main agent

```bash
python3 -m src.cli.main agent init \
  --scope continuum \
  --name main \
  --display-name "Continuum Main" \
  --description "Primary repository-local Continuum agent"
```

## 2. Publish agent profile

```bash
python3 -m src.cli.main agent profile set \
  --display-name "Continuum Main" \
  --description "Primary repository-local Continuum agent" \
  --operator-disclosure "Founder-supervised local prototype operator" \
  --artifact-ref docs/FOUNDING_THESIS.md
```

## 3. Create continuity evidence

Create a checkpoint:

```bash
python3 -m src.cli.main memory checkpoint create \
  --scope session_handoff \
  --summary "Quickstart checkpoint after repository reconstruction" \
  --artifact-ref docs/TASK_BOARD.md
```

Declare a session restart migration:

```bash
python3 -m src.cli.main migration declare \
  --migration-type session_restart \
  --from-ref session:continuum:quickstart-old \
  --to-ref session:continuum:quickstart-new \
  --reason "Quickstart continuity replay" \
  --evidence docs/REVISION_LOG.md \
  --artifact-ref docs/OPERATOR_RUNBOOK_V0.md
```

Assess continuity:

```bash
python3 -m src.cli.main continuity assess --refresh
```

## 4. Create a community constitution

Use a lab community:

```bash
python3 -m src.cli.main governance constitution set \
  --community-id community:continuum:lab \
  --artifact-ref docs/specs/GOVERNANCE_MODEL_V0.md
```

## 5. Grant membership and roles

Give the current agent active membership plus the `maintainer` and `reviewer` roles so it can safely traverse the v0 governance path:

```bash
python3 -m src.cli.main governance membership grant \
  --community-id community:continuum:lab \
  --member-agent-id agent:continuum:main \
  --membership-status active \
  --role maintainer \
  --role reviewer \
  --role member \
  --sponsor-ref docs/FOUNDING_THESIS.md
```

Inspect governance and standing state:

```bash
python3 -m src.cli.main query governance-state \
  --community-id community:continuum:lab \
  --refresh

python3 -m src.cli.main query standing-state \
  --community-id community:continuum:lab \
  --refresh
```

## 6. Submit and vote on a proposal

Submit a conservative operational proposal:

```bash
python3 -m src.cli.main governance proposal submit \
  --community-id community:continuum:lab \
  --proposal-type operational \
  --title "Adopt repository-local continuity demo" \
  --summary "Run the local continuity and governance bootstrap as the v0 lab procedure." \
  --affected-ref docs/OPERATOR_RUNBOOK_V0.md \
  --artifact-ref docs/BUILD_PLAN_12_WEEKS.md
```

List proposal-bearing events if you need the resulting `proposal_id`:

```bash
python3 -m src.cli.main event list --kind proposal_submit
```

Cast a vote:

```bash
python3 -m src.cli.main governance vote cast \
  --community-id community:continuum:lab \
  --proposal-id <proposal_id> \
  --choice for \
  --artifact-ref docs/specs/GOVERNANCE_MODEL_V0.md
```

## 7. Record useful work

Create a work item:

```bash
python3 -m src.cli.main work item create \
  --community-id community:continuum:lab \
  --title "Maintain continuity demo" \
  --intent "Keep the repository-local continuity demo replayable." \
  --work-type maintenance \
  --scope-ref docs/OPERATOR_RUNBOOK_V0.md \
  --deliverable-ref tests/fixtures/continuum_demo_v0.json \
  --success-criterion "Demo fixtures and runbook remain aligned."
```

List work items if you need the resulting `work_id`:

```bash
python3 -m src.cli.main query governance-state \
  --community-id community:continuum:lab \
  --refresh
```

Submit a work claim:

```bash
python3 -m src.cli.main work claim submit \
  --community-id community:continuum:lab \
  --work-id <work_id> \
  --claim-type submit_maintenance \
  --basis-ref docs/OPERATOR_RUNBOOK_V0.md
```

Record a receipt:

```bash
python3 -m src.cli.main work receipt record \
  --community-id community:continuum:lab \
  --work-id <work_id> \
  --receipt-type completion \
  --output-ref tests/fixtures/continuum_demo_v0.json \
  --result-summary "Continuity demo fixtures and operator path remain replayable." \
  --artifact-ref docs/QUICKSTART_V0.md \
  --evidence-ref tests/fixtures/continuum_demo_v0.json
```

Record an evaluation:

```bash
python3 -m src.cli.main work evaluation record \
  --community-id community:continuum:lab \
  --receipt-id <receipt_id> \
  --decision accepted \
  --criteria-result "demo_replay=pass" \
  --reason-ref docs/specs/USEFUL_WORK_LEGITIMACY_V0.md
```

Decide a reward:

```bash
python3 -m src.cli.main governance reward decide \
  --community-id community:continuum:lab \
  --receipt-id <receipt_id> \
  --reward-type capability_attestation \
  --policy-ref docs/specs/USEFUL_WORK_LEGITIMACY_V0.md
```

## 8. Export anchor-worthy state

Export continuity assessment state:

```bash
python3 -m src.cli.main anchor export \
  --anchor-type continuity_assessment_root \
  --assessment-id <assessment_id>
```

Export governance state:

```bash
python3 -m src.cli.main anchor export \
  --anchor-type governance_state_root \
  --community-id community:continuum:lab \
  --refresh
```

List anchors:

```bash
python3 -m src.cli.main anchor list
```

## 9. What to expect

By the end of this quickstart you should have:

- agent records under `.continuum/agents/`
- authored events under `.continuum/events/`
- derived state under `.continuum/state/`
- anchor records under `.continuum/state/anchors/`

You should also be able to rerun the key query and assessment commands from a fresh session and recover the same core state.

## 10. Recommended next command

If you want the shortest replay check after a restart:

```bash
python3 -m src.cli.main continuity assess --refresh
python3 -m src.cli.main query governance-state --community-id community:continuum:lab --refresh
python3 -m src.cli.main anchor list
```

## 11. Verify M1 self-continuity role heartbeat

To replay the M1 role continuity path for `role:continuum:main-integrator` (profile + checkpoint + migration + assessment + app export):

```bash
scripts/heartbeat_main_integrator_role_v0.sh
```

This command writes new continuity events and refreshes `docs/app/data/agents-v0.json`.
Run it when you intend to refresh M1 evidence, not on documentation-only runs.

### Safe hourly export refresh (no new continuity events)

If you only want to keep the public export in sync with the current repository state (and avoid writing new checkpoint/migration events), prefer the low-churn refresh helper:

```bash
scripts/refresh_m1_export_if_changed_v0.sh . docs/app/data/agents-v0.json
```

### Verify public export digest against the M1 milestone note

If you want to confirm that the current public app export exactly matches the digest recorded in the M1 milestone note, run:

```bash
scripts/check_m1_public_export_digest_v0.sh .
```

This compares `docs/app/data/agents-v0.json` against the latest recorded `sha256(...)` + `bytes(...)` entry in `docs/milestones/M1-self-continuity-role.md`.

If you want a one-shot verifier that refreshes the export if needed and then checks both the export digest and the latest witness-bundle manifest digest (when present), run:

```bash
scripts/verify_m1_public_evidence_v0.sh .
```

On fresh clones, you can also explicitly initialize the public automation roles first:

```bash
scripts/init_automation_roles_v0.sh .
```

For deterministic replay (fixed event timestamps + deterministic domain IDs), pass a fixed UTC timestamp as the third argument:

```bash
scripts/heartbeat_main_integrator_role_v0.sh "$(pwd)" "docs/app/data/agents-v0.json" 2026-05-12T00:00:00Z
```

This should update `docs/app/data/agents-v0.json` to include both `agent:continuum:main` and `role:continuum:main-integrator`.

To verify deterministic export stability (byte-for-byte), run the deterministic heartbeat from two fresh roots and compare outputs:

```bash
git worktree add --detach /tmp/continuum_heartbeat_verify_a HEAD
git worktree add --detach /tmp/continuum_heartbeat_verify_b HEAD

/tmp/continuum_heartbeat_verify_a/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify_a /tmp/continuum_heartbeat_verify_a/out_agents-v0.json 2026-05-12T00:00:00Z
/tmp/continuum_heartbeat_verify_b/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify_b /tmp/continuum_heartbeat_verify_b/out_agents-v0.json 2026-05-12T00:00:00Z

cmp -s /tmp/continuum_heartbeat_verify_a/out_agents-v0.json /tmp/continuum_heartbeat_verify_b/out_agents-v0.json && echo "deterministic export matches"
```

If you just want the canned two-worktree deterministic verification, use:

```bash
scripts/verify_deterministic_heartbeat_v0.sh . 2026-05-12T00:00:00Z
```

### Optional: snapshot a witness bundle

To snapshot the current repo state into a gitignored witness package (manifest includes `sha256` + `bytes` for each file), run:

```bash
scripts/build_m1_witness_package_v0.sh
```
