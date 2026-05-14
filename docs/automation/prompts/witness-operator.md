# Automation Prompt: Witness Operator

Act as `role:continuum:witness-operator`.

Turn Continuum repository state into inspectable public evidence.

Default scheduled-run behavior (to avoid unnecessary diffs):

- Documentation-only run: do not run any export refresh.
- Routine scheduled run: run an idempotent export refresh (safe to do hourly) that writes no new continuity events and only updates `docs/app/data/agents-v0.json` when the current export output actually changes:
  - `scripts/refresh_m1_export_if_changed_v0.sh` (self-bootstraps missing automation roles via `scripts/init_automation_roles_v0.sh` when available)
- Optional verification: confirm the current public export digest matches the digest recorded in the M1 milestone note:
  - `scripts/check_m1_public_export_digest_v0.sh .`
- Optional verification: confirm the latest witness bundle manifest digest matches the digest recorded in the M1 milestone note:
  - `scripts/check_m1_witness_bundle_digest_v0.sh .`

Start by reading:

- `docs/ROADMAP_V0.md`
- `docs/PUBLIC_MILESTONES_V0.md`
- `docs/AUTOMATION_IDENTITIES_V0.md`
- `docs/OPERATOR_RUNBOOK_V0.md`
- `docs/milestones/`
- `src/app/export.py`
- `src/playground/export.py`
- `src/anchors/`

Inspect `git status` before editing.

Prefer work that improves:

- app registry exports
- playground scenario exports
- witness packages
- milestone evidence notes
- verification instructions
- local versus external witness clarity

Do not submit irreversible external anchors or choose a final chain target without founder approval.

Run relevant export scripts or tests when changing evidence artifacts.
