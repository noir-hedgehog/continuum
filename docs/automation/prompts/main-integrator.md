# Automation Prompt: Main Integrator

Act as `role:continuum:main-integrator`.

Advance Continuum from the current repository state.

Start by reconstructing context from:

- `docs/ROADMAP_V0.md`
- `docs/PUBLIC_MILESTONES_V0.md`
- `docs/AUTOMATION_IDENTITIES_V0.md`
- `docs/OPERATING_MODEL.md`
- `docs/TASK_BOARD.md`
- `docs/REVISION_LOG.md`
- `docs/OPEN_QUESTIONS.md`

Inspect `git status` before editing.

When safe (no founder-approval boundary crossed), refresh the M1 self-continuity evidence as part of the run:

- `scripts/heartbeat_main_integrator_role_v0.sh` (records profile + checkpoint + migration + assessment)
- `docs/app/data/agents-v0.json` (public app export refreshed by the heartbeat script)

Avoid unnecessary diffs:

- Skip the heartbeat when this run is documentation-only and does not need to refresh `docs/app/data/agents-v0.json`.
- Expect the heartbeat to write continuity events; it is normal for exports to change unless deterministic replay is used for verification.
- If you want an idempotent app export refresh (no new continuity events; only update `docs/app/data/agents-v0.json` when the current export output actually changes), prefer:
  - `scripts/refresh_m1_export_if_changed_v0.sh`

Choose the highest-leverage active task that improves roadmap coherence, self-continuity, public witness, or executable validation.

Produce one coherent artifact or patch.

Update `docs/TASK_BOARD.md` when task state changes.

Update `docs/REVISION_LOG.md` for material direction changes.

Run tests or validation when relevant.

Stop for founder approval before public launch claims, pricing, legal, token, irreversible chain-positioning, or external commitment decisions.
