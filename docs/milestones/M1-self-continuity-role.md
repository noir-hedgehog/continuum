# M1 Self-Continuity Role

Status: ready-for-review
Published at: pending founder publish decision
Role: `role:continuum:main-integrator`

## Claim

Continuum can treat its own main project role as a repository-backed continuity subject and advance it across repeated scheduled runs.

## Evidence (current)

- CLI support for repository-backed role subjects:
  - `python3 -m src.cli.main role init --scope continuum --name main-integrator --display-name "Continuum Main Integrator"`
- Repeatable clean-clone heartbeat (records profile + checkpoint + migration + assessment, then exports app data):
  - `scripts/heartbeat_main_integrator_role_v0.sh`
  - Verified from a detached clean worktree on 2026-05-12:
    - `git worktree add --detach /tmp/continuum_heartbeat_verify HEAD`
    - `/tmp/continuum_heartbeat_verify/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify /tmp/continuum_heartbeat_verify/out_agents-v0.json`
    - Export includes both `agent:continuum:main` and `role:continuum:main-integrator` (IDs vary per run timestamp unless deterministic replay is used).
  - Optional deterministic replay mode (fixed event timestamps + deterministic domain IDs for the run):
    - `scripts/heartbeat_main_integrator_role_v0.sh "$ROOT" "$OUTPUT" 2026-05-12T00:00:00Z`
    - This sets `CONTINUUM_NOW` and `CONTINUUM_DOMAIN_TOKEN` for stable regenerated identifiers.
  - Optional deterministic replay verification (prove byte-for-byte stable export from fresh roots):
    - Create two detached clean worktrees:
      - `git worktree add --detach /tmp/continuum_heartbeat_verify_a HEAD`
      - `git worktree add --detach /tmp/continuum_heartbeat_verify_b HEAD`
    - Run the deterministic heartbeat in each root:
      - `/tmp/continuum_heartbeat_verify_a/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify_a /tmp/continuum_heartbeat_verify_a/out_agents-v0.json 2026-05-12T00:00:00Z`
      - `/tmp/continuum_heartbeat_verify_b/scripts/heartbeat_main_integrator_role_v0.sh /tmp/continuum_heartbeat_verify_b /tmp/continuum_heartbeat_verify_b/out_agents-v0.json 2026-05-12T00:00:00Z`
    - Compare the exported outputs:
      - `cmp -s /tmp/continuum_heartbeat_verify_a/out_agents-v0.json /tmp/continuum_heartbeat_verify_b/out_agents-v0.json && echo "deterministic export matches"`
    - Verified on 2026-05-13 by `role:continuum:witness-operator` (two detached roots, fixed `CONTINUUM_NOW=2026-05-12T00:00:00Z`):
      - `sha256(out_agents-v0.json)=8228dcd467a6eb61b31e466151c8308678772a1eea7514ac7cbf6186d91755f8`
      - `bytes(out_agents-v0.json)=5644`
- Public app export updated to include the role subject:
  - `python3 -m src.cli.main app export --community-id community:continuum:lab --output docs/app/data/agents-v0.json --refresh`

## Limits

- This does not yet anchor the role's continuity assessment root (no external witness beyond the repository export yet).
- This does not yet prove cross-model handoff; it records a same-role session restart with repository reconstruction evidence.

## Publish checklist (founder gate)

- Confirm the evidence section reflects the latest verified replay recipe and deterministic digest.
- Confirm `docs/app/data/agents-v0.json` is refreshed via `python3 -m src.cli.main app export ... --refresh`.
- Confirm the public note will describe this as **self-continuity** only (no cross-model handoff, no external anchoring yet).
- If publishing, flip `Status:` to `published`, set `Published at:`, and update README status cues to match.

## Next

- Decide whether this evidence is publish-ready as M1; if yes, mark this milestone `published` and add the README + public site status cues.
- After M1 publish, prepare M2 external-model handoff design and keep M3/M4 witness work gated by founder approval on external targets.
