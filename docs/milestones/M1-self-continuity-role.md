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
    - Preferred helper script (creates two detached worktrees, runs the deterministic heartbeat in each, and prints the digest):
      - `scripts/verify_deterministic_heartbeat_v0.sh "$ROOT" 2026-05-12T00:00:00Z`
      - Expected output includes:
        - `deterministic export matches`
        - `sha256=...`
        - `bytes=...`
  - Low-churn app export refresh (only update `docs/app/data/agents-v0.json` when the export output changes; does not write new continuity events):
    - `scripts/refresh_m1_export_if_changed_v0.sh "$ROOT" docs/app/data/agents-v0.json`
    - Current public app export digest (re-verified 2026-05-15 by `role:continuum:witness-operator`):
      - `sha256(docs/app/data/agents-v0.json)=10bbdd55de0104e87fed58ebf26fa4abaeab4d63e148cc5a068f820eeda4d43b`
      - `bytes(docs/app/data/agents-v0.json)=24119`
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
- Public witness bundle packaging (snapshot existing repo state + hashes for third-party inspection):
  - `scripts/build_m1_witness_package_v0.sh`
  - Output is written under `.continuum/witness/m1/` (gitignored) and includes `WITNESS_MANIFEST.json` with per-file `sha256` + `bytes`.
  - Latest witness bundle snapshot (verified 2026-05-14 by `role:continuum:witness-operator`):
    - `built_at_utc=20260514T104624Z`
    - `bundle_id_sha256(manifest)=1d886f2a1bd439c39a7d32674e72170f1b21eaf7139c6e301523c9f2eec79d26`

## Limits

- This does not yet anchor the role's continuity assessment root (no external witness beyond the repository export yet).
- This does not yet prove cross-model handoff; it records a same-role session restart with repository reconstruction evidence.

## Publish checklist (founder gate)

This milestone flips to `published` only with explicit founder approval.

Minimum checks:

- Confirm the Evidence section reflects the latest verified replay recipe and digests.
- Confirm the public app export is up to date:
  - `scripts/refresh_m1_export_if_changed_v0.sh "$ROOT" docs/app/data/agents-v0.json`
  - (or) `python3 -m src.cli.main app export --community-id community:continuum:lab --output docs/app/data/agents-v0.json --refresh`
- Confirm the milestone copy stays scoped to **self-continuity** only (no cross-model handoff, no external anchoring).

Recommended checks (stronger publication evidence, still repo-only):

- Deterministic replay verification (byte-for-byte):
  - `scripts/verify_deterministic_heartbeat_v0.sh "$ROOT" 2026-05-12T00:00:00Z`
- Fresh witness snapshot bundle (manifested hashes for third parties):
  - `scripts/build_m1_witness_package_v0.sh --root "$ROOT"`

Publish steps (once approved):

- Flip `Status:` to `published`.
- Set `Published at:` to an ISO date.
- Update README + public landing-page status cues to match.

## Next

- Decide whether this evidence is publish-ready as M1; if yes, mark this milestone `published` and add the README + public site status cues.
- After M1 publish, prepare M2 external-model handoff design and keep M3/M4 witness work gated by founder approval on external targets.
