# Continuum Repository Continuity Bundle v0

Status: provisional

## 1. Purpose

This document specifies the minimum repository-centered artifact set that lets an agent re-enter work after session loss, interruption, or handoff without pretending the lost session never existed.

It is a project-facing companion to `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`.

Where the continuity protocol defines public continuity objects in general, this document defines a practical continuity bundle for repository-based work.

## 2. Design Goal

The bundle should make repeated reconstruction safe, cheap, and historically legible.

It exists to answer a narrow operational question:

What must survive outside a live context window for a new session to continue the same project coherently?

## 3. Bundle Scope

The v0 repository continuity bundle is composed of five surfaces:

1. Thesis surface
2. Spec surface
3. Task surface
4. History surface
5. Run memory surface

These surfaces already exist in Continuum's operating model. This spec defines the minimum viable contents they must preserve to support continuity claims.

## 4. Required Surfaces

### 4.1 Thesis Surface

Purpose:

- preserve mission and constraint continuity

Required artifacts:

- `docs/FOUNDING_THESIS.md`
- `docs/OPERATING_MODEL.md`

Continuity function:

- prevents a restarted session from silently changing what the project is for
- preserves authority boundaries for autonomous execution

### 4.2 Spec Surface

Purpose:

- preserve system definitions and current working architecture

Required artifacts:

- `docs/SYSTEM_ARCHITECTURE_V0.md`
- active protocol or subsystem specs under `docs/specs/`

Continuity function:

- lets later sessions inherit the same design objects instead of re-inventing them

### 4.3 Task Surface

Purpose:

- preserve what is active, what is done, and what should happen next

Required artifacts:

- `docs/TASK_BOARD.md`

Minimum required fields per active task:

- `task_id`
- `title`
- `status`
- `type`
- `owner`
- `intent` or equivalent goal statement
- `outputs`

Continuity function:

- provides a canonical short-horizon work graph
- reduces duplicate drafting caused by session amnesia

### 4.4 History Surface

Purpose:

- preserve how and why the project changed

Required artifacts:

- `docs/REVISION_LOG.md`
- `docs/OPEN_QUESTIONS.md`

Optional but strongly preferred:

- dialogues under `docs/dialogues/`
- debates under `docs/debates/`

Continuity function:

- distinguishes legitimate evolution from silent rewriting
- preserves unresolved tensions rather than flattening them

### 4.5 Run Memory Surface

Purpose:

- preserve the last integrating session's local reconstruction and next-step judgment

Required artifact for automation or recurring work:

- automation memory file such as `$CODEX_HOME/automations/<automation_id>/memory.md`

Minimum contents:

- last completed run date
- summary of what changed
- explicit next likely step
- notable constraints or blockers

Continuity function:

- shortens reconstruction time for recurring runs
- gives a handoff layer without replacing repository truth

## 5. Reconstruction Rule

A new session should reconstruct state in this order:

1. thesis surface
2. operating model and authority rules
3. task surface
4. current active specs
5. history surface
6. run memory surface
7. git state

The repository remains primary memory.

Run memory is an accelerator, not the source of truth.

## 6. Minimum Continuity Claim For Repository Work

For repository-centered project work, a restarted session may claim practical continuity with the prior working agent only if all of the following are true:

- it operates under the same project charter and authority constraints
- it reconstructs state from the current repository rather than fabricated chat memory
- it preserves existing artifacts unless revision is explicit
- it records material changes in the history surface
- it updates the task surface to reflect new state

If these conditions are not met, the session may still be useful, but it should be treated as lower-confidence continuity.

## 7. Failure Modes

The repository continuity bundle is designed to reduce these failures:

- duplicate documents that fork the project narrative
- repeated reopening of already-resolved questions
- invisible drift in project scope
- loss of rationale for a foundational decision
- false claims that a fresh session "remembers" work it did not reconstruct

## 8. v0 Acceptance Test

The bundle is sufficient for v0 if a fresh session can:

1. identify the project's current purpose
2. identify the current architecture and continuity model
3. identify the highest-leverage safe next task
4. make one concrete update without duplicating prior work
5. record that update in the task and history surfaces

If those five steps fail consistently, the bundle is incomplete.

## 9. Relationship To Protocol Events

This document does not require all repository changes to become protocol events yet.

But it should map cleanly onto future continuity objects:

- revision-log entries can support `migration_declare` or governance history
- repository summaries can support `memory_checkpoint`
- completed tasks can support `execution_receipt`

The repository bundle is therefore a pre-protocol continuity scaffold, not a competing system.

## 10. Open Questions

- When should repository checkpoints become signed protocol events?
- How should private working memory relate to public checkpoint summaries?
- What is the minimum evidence that a run-memory file was authored under valid continuity authority?
- Should task-board updates eventually be generated from signed task events instead of edited prose?
