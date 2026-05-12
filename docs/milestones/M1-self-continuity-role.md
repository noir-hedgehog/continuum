# M1 Self-Continuity Role

Status: ready-for-review
Published at: pending founder publish decision
Role: `role:continuum:main-integrator`

## Claim

Continuum can treat its own main project role as a repository-backed continuity subject and advance it across repeated scheduled runs.

## Evidence (current)

- CLI support for repository-backed role subjects:
  - `python -m src.cli.main role init --scope continuum --name main-integrator --display-name "Continuum Main Integrator"`
- Repeatable clean-clone heartbeat (records profile + checkpoint + migration + assessment, then exports app data):
  - `scripts/heartbeat_main_integrator_role_v0.sh`
  - Verified from a detached clean worktree on 2026-05-12:
    - `git worktree add --detach /tmp/continuum_heartbeat_verify HEAD`
    - `/tmp/continuum_heartbeat_verify/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify /tmp/continuum_heartbeat_verify/out_agents-v0.json`
    - Export includes both `agent:continuum:main` and `role:continuum:main-integrator` (hash varies per run timestamp).
  - Optional deterministic replay mode (fixed event timestamps + deterministic domain IDs for this run):
    - `scripts/heartbeat_main_integrator_role_v0.sh "$ROOT" "$OUTPUT" 2026-05-12T00:00:00Z`
- Public app export updated to include the role subject:
  - `python -m src.cli.main app export --community-id community:continuum:lab --output docs/app/data/agents-v0.json --refresh`

## Limits

- This does not yet anchor the role's continuity assessment root (no external witness beyond the repository export yet).
- This does not yet prove cross-model handoff; it records a same-role session restart with repository reconstruction evidence.

## Next

- Decide whether this evidence is publish-ready as M1; if yes, mark this milestone `published` and add the README + public site status cues.
- After M1 publish, prepare M2 external-model handoff design and keep M3/M4 witness work gated by founder approval on external targets.
