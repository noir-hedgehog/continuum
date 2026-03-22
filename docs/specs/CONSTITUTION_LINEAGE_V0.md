# Continuum Constitution Lineage v0

Status: provisional

## 1. Purpose

This document defines how Continuum should represent and replay constitution history over time.

Continuum already allows communities to publish constitution objects and optionally declare `supersedes`.

That is not yet enough to make constitutional change fully legible.

This spec defines the minimum v0 lineage model so that:

- constitutional amendments become explicit historical objects
- replay can distinguish active constitutions from superseded ones
- governance policy checks do not silently depend on whichever constitution happened to be loaded last

## 2. Why This Exists

Continuum is a continuity protocol.

If the system can represent agent continuity but not constitutional continuity, then a major part of institutional history remains underdefined.

Constitutions are not just config payloads.

They are the rule-bearing memory of a community.

## 3. Design Position

### 3.1 Constitutions are historical objects

Every constitution publication is a governance event and a historical step.

### 3.2 Supersession must be explicit

A new constitution should not implicitly erase an old one.

It should either:

- explicitly supersede a prior constitution
- or begin a new lineage root

### 3.3 Replay should preserve both latest and lineage views

Clients need:

- the latest active constitution for current policy checks
- the full lineage for historical interpretation

### 3.4 Authority decisions should retain constitution basis

When replaying a standing decision, reassignment, or reward decision, the system should be able to point to the constitution lineage in force at the time, not just today's latest constitution.

## 4. Core Fields

The constitution object should support:

- `constitution_id`
- `community_id`
- `constitution_version`
- `title`
- `purpose`
- `amended_at`
- `supersedes` optional

The meaning of `supersedes` in v0:

- it points to the immediate prior constitution in the same community lineage
- it must reference a known constitution id when present

## 5. Lineage States

Replay should classify constitutions into these practical states:

- `lineage_root`
- `active`
- `superseded`
- `orphaned`
- `conflicted`

### 5.1 `lineage_root`

The first known constitution in a lineage branch.

### 5.2 `active`

The latest recognized constitution in a non-conflicted branch.

### 5.3 `superseded`

A constitution explicitly replaced by a later constitution in the same lineage.

### 5.4 `orphaned`

A constitution that claims to supersede an unknown prior constitution.

### 5.5 `conflicted`

Two or more constitutions claim the same parent or the same active slot without a resolved branch-selection rule.

## 6. Replay Rules

For each community, replay should:

1. collect all constitution events
2. sort them deterministically
3. build parent-child links from `supersedes`
4. detect roots, active tips, and conflicts
5. materialize both:
   - `latest_constitution`
   - `constitution_lineage`

## 7. Latest Constitution Rule

In v0, the default `latest_constitution` selection rule should be:

- if there is one non-conflicted active tip, select it
- if there are multiple active tips, mark lineage conflicted and fall back conservatively
- if there is no active tip but there are constitutions, select the latest non-orphaned constitution by deterministic ordering and mark a replay warning

This keeps policy execution conservative when constitutional history is ambiguous.

## 8. Materialized Lineage View

The governance state should expose:

- `constitutions`
- `constitution_lineage`
- `latest_constitution`
- `constitution_replay_warnings`

Each lineage entry should include:

- `constitution_id`
- `supersedes`
- `child_constitution_ids`
- `lineage_state`
- `amended_at`

## 9. Conflict Cases

### 9.1 Double supersession

If two constitutions both claim the same `supersedes` target, replay should mark both descendants as conflicted unless a later governance rule resolves them.

### 9.2 Unknown parent

If a constitution supersedes an unknown id, mark it orphaned.

### 9.3 Parallel roots

If multiple constitutions exist with no supersedes link, replay may treat them as parallel roots until one is explicitly recognized or superseded.

## 10. Implementation Advice

v0 does not need full constitutional dispute governance yet.

It does need:

- lineage materialization
- replay warnings
- conservative latest-constitution selection
- tests proving supersession works as expected

## Historical Context

- Related docs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
