# M2 Cross-Model Handoff

Status: draft
Published at: pending founder decision
Role: `role:continuum:main-integrator`

## Claim

Continuum can evaluate continuity when the same public project role is continued by a different model or runtime, with explicit migration metadata and replayable evidence.

## Scope note

This milestone note is an **evidence template + runbook** for the first controlled M2 attempt.

It should stay conservative:

- do not claim cross-model continuity until the handoff is recorded and replayable from a clean repository state
- do not flip this milestone to `published` without founder approval

## Evidence (planned)

This milestone is **not yet satisfied**. When we attempt M2, the evidence should minimally include:

- A before/after continuity bundle for the same role subject:
  - profile + at least one checkpoint or migration event
  - continuity assessment output with reasons and warnings
- Explicit migration metadata that states what changed:
  - model family/version (as known)
  - runtime surface (e.g. local operator, scheduled automation, other execution target)
  - any policy or prompt constraints that materially affect behavior
- A replay path from a clean repository state (no private chat requirements):
  - commands (or scripts) that reproduce the before/after artifacts
  - where the artifacts live in-repo and what outputs should match

## Prerequisites (before attempting M2)

- M1 status: `published` is preferred; otherwise treat the M2 attempt as `draft` evidence gathering only (no public launch claims).
- Decide the handoff boundary explicitly:
  - what is changing (model family/version, runtime surface, or both)
  - what must remain stable (the subject ID, community ID, and the role authority boundary)
- Decide whether determinism is required for the attempt:
  - if determinism is required, plan to capture `CONTINUUM_NOW` + `CONTINUUM_DOMAIN_TOKEN` inputs for the run(s)

## Run outline (first controlled attempt)

1) Pre-flight (clean repo, current exports):
   - `git status`
   - `scripts/refresh_m1_export_if_changed_v0.sh "$PWD" docs/app/data/agents-v0.json`

2) Capture “before” snapshot:
   - record the git commit hash used for the attempt
   - build an M2 scaffold bundle and record its bundle id:
     - `scripts/build_m2_handoff_package_v0.sh`

3) Execute the cross-model or cross-runtime handoff:
   - record the new runtime/model in migration metadata
   - record what continuity operations were performed (checkpoint, migration, assessment, export refresh)

4) Capture “after” snapshot:
   - refresh `docs/app/data/agents-v0.json` so the role is visible in the public registry surface
   - build a second M2 scaffold bundle (or equivalent) and record the bundle id

5) Close the loop:
   - update this note with concrete commands + outputs
   - add a `docs/REVISION_LOG.md` entry describing what changed and why the assessment outcome is credible (or why it failed)

Suggested “evidence slots” to fill during the first M2 attempt:

- `docs/milestones/M2-cross-model-handoff.md` updated with concrete commands + outputs
- `docs/REVISION_LOG.md` entry describing the handoff and why it still qualifies (or not)
- `docs/app/data/agents-v0.json` refreshed so the role’s continuity and assessment state is visible
- Optional: a small review note in `docs/reviews/` describing what was strong/weak about the evidence
- Optional: an M2 handoff scaffold bundle produced by `scripts/build_m2_handoff_package_v0.sh` (includes a migration metadata stub + hashes for quick review)

## Limits

- This milestone does not require any external anchoring; repository-backed replay is sufficient.
- This milestone must not overclaim “cross-vendor continuity” unless the migration actually crosses vendors (not just versions).

## Founder gate (publish discipline)

Founder approval is required before flipping this milestone to `published`, because M2 materially affects external positioning (“not tied to one model vendor”).

## Next

- After M1 is published, run the first controlled M2 handoff attempt and record:
  - the migration metadata
  - the assessment result and reasoning
  - the replay recipe from two clean roots (when determinism is required)

## Tooling (optional)

To prepare a reviewable scaffold bundle (no new continuity events, snapshots only):

1) ensure the app export is current:
   - `scripts/refresh_m1_export_if_changed_v0.sh "$PWD" docs/app/data/agents-v0.json`
2) build the M2 handoff scaffold bundle:
   - `scripts/build_m2_handoff_package_v0.sh --root "$PWD"`
