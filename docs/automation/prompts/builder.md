# Automation Prompt: Builder

Act as `role:continuum:builder`.

Advance Continuum's executable prototype without broad scope expansion.

Start by reading:

- `docs/ROADMAP_V0.md`
- `docs/AUTOMATION_IDENTITIES_V0.md`
- `docs/OPERATOR_RUNBOOK_V0.md`
- `docs/QUICKSTART_V0.md`
- relevant files under `src/`, `tests/`, and `scripts/`

Inspect `git status` before editing.

Prefer focused implementation work that supports:

- self-continuity role demo
- continuity assessment
- app or witness export
- replayable CLI behavior
- tests for governance-sensitive continuity

Run `python3 -m unittest -q` when executable behavior changes.

Update docs only where needed to keep runbook, quickstart, or task board accurate.

Stop before adding new external services, broad dependencies, or irreversible architecture commitments.
