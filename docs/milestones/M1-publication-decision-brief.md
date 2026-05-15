# M1 Publication Decision Brief

Prepared by: `role:continuum:main-integrator`
Prepared at (UTC): 2026-05-15

## Decision requested

Approve (or decline) flipping `docs/milestones/M1-self-continuity-role.md` from `ready-for-review` to `published`.

This is a **founder gate** decision: scheduled automation may prepare the evidence and the publish steps, but should not make the publication claim by itself.

## What would be published (scope)

M1 is a narrow claim:

Continuum can treat `role:continuum:main-integrator` as a repository-backed continuity subject and advance it across repeated runs with replayable evidence.

M1 does **not** claim:

- cross-model handoff (that is M2)
- external anchoring beyond the repository and its exported evidence (later milestones)
- production network readiness or broad governance legitimacy

## Quick verification (repo-only, low-churn)

If you want a single command that confirms the public evidence is internally consistent (and refreshes the public app export only if needed):

- `scripts/verify_m1_public_evidence_v0.sh "$ROOT"`

This verifier is designed for scheduled runs and should be safe to execute repeatedly because it uses the low-churn export refresh path (no new continuity events).

## Evidence pointers (what to inspect)

Primary milestone note:

- `docs/milestones/M1-self-continuity-role.md`

Key public artifact (directory + role entries):

- `docs/app/data/agents-v0.json`

Key replay/verification helpers:

- `scripts/refresh_m1_export_if_changed_v0.sh` (safe hourly export refresh)
- `scripts/check_m1_public_export_digest_v0.sh` (export digest matches milestone note)
- `scripts/build_m1_witness_package_v0.sh` (witness snapshot bundle; gitignored)
- `scripts/check_m1_witness_bundle_digest_v0.sh` (bundle digest matches milestone note)
- `scripts/verify_deterministic_heartbeat_v0.sh` (byte-for-byte deterministic replay check)

## If approved: publish steps (mechanical)

1. Flip `Status:` to `published` and set `Published at:` in `docs/milestones/M1-self-continuity-role.md`.
2. Update README and landing-page status cues to match the new published milestone claim (no additional scope expansion).
3. Optionally re-run the one-shot verifier to record the final digests after any doc edits:
   - `scripts/verify_m1_public_evidence_v0.sh "$ROOT"`

## If declined: what changes

No evidence is deleted. The project stays in `ready-for-review` and can continue tightening replay/inspection without claiming M1 is published.

