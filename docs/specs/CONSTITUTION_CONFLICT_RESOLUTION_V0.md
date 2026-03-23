# Continuum Constitution Conflict Resolution v0

Status: provisional

## 1. Purpose

This document defines the minimum v0 mechanism for resolving constitutional branch conflicts in Continuum.

Continuum already materializes constitution lineage and detects conflicts.

What it does not yet do by itself is let a community record which branch should count as canonical for future replay.

This spec fills that gap.

## 2. Why This Exists

Lineage warnings are useful, but they are not enough once a community needs to move forward.

If two constitutions claim the same parent, the system should not be forced to stay indefinitely in an ambiguous state.

The community needs a replayable way to say:

- this branch is recognized
- these sibling branches are rejected for canonical replay
- this was decided by a named actor at a named time for a stated reason

## 3. Design Position

### 3.1 Resolution is distinct from publication

Publishing a constitution creates a candidate historical object.

Resolving a conflict decides how replay should interpret competing candidates.

### 3.2 Resolution is conservative, not magical

v0 does not rewrite old events.

It records a later governance object that changes how lineage should be interpreted going forward.

### 3.3 Resolution should stay narrow in v0

v0 should support one practical action:

- select the canonical branch among already-published competing constitutions

It does not need a full constitutional court model yet.

## 4. Core Object

Suggested fields:

- `resolution_id`
- `community_id`
- `resolved_by`
- `resolved_at`
- `resolution_type`
- `parent_constitution_id` optional
- `recognized_constitution_id`
- `rejected_constitution_ids`
- `reason`
- `basis_refs`

Suggested `resolution_type` values:

- `select_canonical_branch`
- `select_canonical_root`

## 5. Replay Rules

When replaying constitution lineage:

1. materialize published constitutions first
2. detect sibling conflicts and unresolved parallel roots
3. apply the latest valid resolution for the affected parent or root set
4. mark the recognized constitution as eligible for canonical replay
5. mark explicitly rejected constitutions as `rejected`
6. keep the resolution ref on affected lineage entries

If no valid resolution exists, replay should remain conservative and keep the conflict visible.

## 6. Validity Rules

For a parent-scoped branch resolution:

- the recognized constitution must be a child of the referenced parent
- every rejected constitution must be a sibling child of that same parent

For a root-scoped resolution:

- the recognized constitution must be a root constitution
- every rejected constitution must also be a root constitution

Invalid resolutions should not silently alter lineage.

They should produce replay warnings instead.

## 7. Materialized State

Governance state should expose:

- `constitution_resolutions`
- `constitution_lineage`
- `constitution_replay_warnings`

Affected lineage entries should include:

- `resolution_ref` optional

## 8. v0 Boundary

This spec does not yet require:

- vote-driven constitutional courts
- appeals
- multi-step amendment litigation
- automatic slashing for invalid branch attempts

It does require:

- a first-class resolution object
- deterministic replay behavior after resolution
- tests proving a conflicted branch can become canonical

## Historical Context

- Related docs:
  - `docs/specs/CONSTITUTION_LINEAGE_V0.md`
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md`
