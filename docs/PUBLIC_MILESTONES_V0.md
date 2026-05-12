# Continuum Public Milestones v0

Status: provisional

## Purpose

This document defines what Continuum should reveal publicly, in what order, and under what evidence standard.

The project should publish progress gradually.

Each public milestone should correspond to a replayable artifact, not only a narrative claim.

## Publication Principle

Continuum should not announce a milestone because a document says the concept exists.

It should announce only when at least one of these exists:

- executable demo
- exported snapshot
- continuity assessment
- public witness package
- app or explorer surface
- external validation note

Public claims should be small, verifiable, and linked to repository artifacts.

## Public Surfaces

The first public surfaces are:

- `README.md`
- `docs/index.md`
- `docs/app/index.md`
- `docs/explorer/index.md`
- `docs/playground/index.md`
- public JSON under `docs/app/data/`
- public milestone notes added under `docs/milestones/`

The repository itself is also a public witness surface when commits and tags cite the relevant evidence.

## Milestone Ladder

### M0: Roadmap Alignment

Public claim:

Continuum has a unified roadmap for proving agent continuity through its own operation.

Required evidence:

- `docs/ROADMAP_V0.md`
- `docs/PUBLIC_MILESTONES_V0.md`
- updated operating model and task board

Publication status:

- internal-first
- public once committed and linked from README

### M1: Self-Continuity Role

Public claim:

Continuum can treat its own main project role as a continuity subject across sessions.

Required evidence:

- `role:continuum:main-integrator` profile or equivalent state
- checkpoint or migration event for a meaningful session handoff
- continuity assessment for the role
- exported app or witness snapshot

Publication status:

- publish after replay passes from a clean repository state

### M2: Cross-Model Handoff

Public claim:

Continuum can evaluate continuity when the same public role is continued by a different model or runtime.

Required evidence:

- explicit model/runtime migration metadata
- before and after role evidence
- continuity assessment with reasons and warnings
- review note explaining what the system accepted or downgraded

Publication status:

- publish only after the handoff is reproducible without private chat memory

### M3: Rights Affected by Continuity

Public claim:

Continuity status can affect governance rights rather than only profile labels.

Required evidence:

- same-agent or ready subject that can perform a permitted action
- successor or review subject that is restricted from a sensitive action
- test or demo output showing enforcement
- app or playground surface explaining the distinction

Publication status:

- publish after the enforcement path is covered by tests or demo scripts

### M4: Public Witness Package

Public claim:

A Continuum subject has an inspectable public witness package containing identity, continuity, assessment, and anchor evidence.

Required evidence:

- exported witness JSON
- event refs
- assessment root
- anchor record
- public page or README link

Publication status:

- publish after the package can be regenerated from repository state

### M5: External Validation

Public claim:

The continuity registry and audit layer is being validated against real agent-operation needs.

Required evidence:

- 3-5 external conversations or design partner notes
- named problem categories
- updated roadmap or positioning based on objections

Publication status:

- publish only summarized learnings unless participants approve attribution

### M6: Strong Public Anchor

Public claim:

At least one continuity or governance root is witnessed outside the local repository.

Required evidence:

- external reference
- anchor record
- verification instructions
- explorer/app status update

Publication status:

- publish after the external target is stable enough for a third party to inspect

## Announcement Mechanism

Each public milestone should create or update:

- a short milestone note in `docs/milestones/`
- a `docs/REVISION_LOG.md` entry
- a `docs/TASK_BOARD.md` status update
- a README status bullet when the milestone changes first-contact understanding
- an app or explorer data export when the milestone affects visible registry state

Milestone notes should use this shape:

```markdown
# M1 Self-Continuity Role

Status: published
Published at: YYYY-MM-DD

## Claim

One sentence.

## Evidence

- artifact
- command
- output path

## Limits

- what this does not yet prove

## Next

- next milestone
```

## Claim Discipline

Continuum should not publicly claim:

- production network status before external witness and operational hardening
- decentralized governance before multiple independent subjects and public process exist
- cross-model continuity before a real model or runtime handoff is recorded
- economic legitimacy before useful-work and reward flows have external users

Continuum may publicly claim:

- repository-backed continuity prototype
- replayable event and assessment path
- role-continuity experiment
- public witness roadmap
- governance-sensitive continuity demo

## Founder Approval Boundary

The main agent may prepare milestone notes and internal-public docs.

Founder approval is required before:

- broad launch announcement
- pricing or commercial commitment
- chain target positioned as final
- legal, fundraising, or token-related public claim

Routine repository updates, docs links, app exports, and evidence notes may proceed under the operating model.
