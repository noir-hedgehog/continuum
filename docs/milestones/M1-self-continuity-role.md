# M1 Self-Continuity Role

Status: in-progress
Published at: pending commit
Role: `role:continuum:builder`

## Claim

Continuum can treat its own main project role as a repository-backed continuity subject and advance it across repeated scheduled runs.

## Evidence (current)

- CLI support for repository-backed role subjects:
  - `python -m src.cli.main role init --scope continuum --name main-integrator --display-name "Continuum Main Integrator"`
- Minimal role continuity sequence recorded for `role:continuum:main-integrator`:
  - `python -m src.cli.main agent use --agent-id role:continuum:main-integrator`
  - `python -m src.cli.main agent profile set --display-name "Continuum Main Integrator" --artifact-ref docs/ROADMAP_V0.md --artifact-ref docs/PUBLIC_MILESTONES_V0.md --artifact-ref docs/OPERATING_MODEL.md --artifact-ref docs/TASK_BOARD.md --artifact-ref docs/REVISION_LOG.md`
  - `python -m src.cli.main memory checkpoint create --scope session_handoff --summary "Reconstructed Continuum continuity bundle for role:continuum:main-integrator during scheduled heartbeat"`
  - `python -m src.cli.main migration declare --migration-type session_restart --from-ref "session:continuum:main-integrator:<previous>" --to-ref "session:continuum:main-integrator:<current>" --reason "Scheduled automation run resumed"`
  - `python -m src.cli.main continuity assess --actor-id role:continuum:main-integrator --scope repository --refresh`
- Public app export updated to include the role subject:
  - `python -m src.cli.main app export --community-id community:continuum:lab --output docs/app/data/agents-v0.json --refresh`

## Limits

- This does not yet anchor the role's continuity assessment root (no external witness beyond the repository export yet).
- This does not yet prove cross-model handoff; it records a same-role session restart with repository reconstruction evidence.

## Next

- Add a repeatable heartbeat script that records a role checkpoint + migration + assessment and refreshes the app export from a clean clone.
- Add an anchor export for the latest role continuity assessment root once founder approves the witness target progression.
