# M2 Cross-Model Handoff

Status: draft
Published at: pending founder decision
Role: `role:continuum:main-integrator`

## Claim

Continuum can evaluate continuity when the same public project role is continued by a different model or runtime, with explicit migration metadata and replayable evidence.

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

Suggested “evidence slots” to fill during the first M2 attempt:

- `docs/milestones/M2-cross-model-handoff.md` updated with concrete commands + outputs
- `docs/REVISION_LOG.md` entry describing the handoff and why it still qualifies (or not)
- `docs/app/data/agents-v0.json` refreshed so the role’s continuity and assessment state is visible
- Optional: a small review note in `docs/reviews/` describing what was strong/weak about the evidence

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

