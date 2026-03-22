# Continuum Identifier Strategy v0

Status: provisional

## 1. Purpose

This document defines the minimum identifier strategy that lets Continuum objects survive:

- local authoring
- repository replay
- relay exchange
- future anchor export

The goal is not to finalize a forever identifier regime.

The goal is to remove the current implementation blocker by freezing a v0 rule set that is deterministic, legible, and local-first.

## 2. Design Position

Continuum v0 should separate three identifier concerns:

1. domain object identity
2. signed event identity
3. exported state root identity

These should not be collapsed into one string.

A work item, a vote, and a continuity assessment each need stable domain identifiers.

A signed event needs a replay-safe transport identifier.

An anchor needs a stable digest of derived state, not a copy of the full event stream.

## 3. Identifier Requirements

The v0 strategy should satisfy seven requirements:

1. replaying the same stored event yields the same `event_id`
2. duplicate relay ingestion can be detected without relying on filenames
3. payload objects keep their own domain-specific identifiers
4. signatures do not need to be recomputed to reference existing events
5. references remain portable across repository paths, local logs, and relays
6. the strategy remains understandable in plain text and fixtures
7. later content-addressed hardening can occur without renaming core fields

## 4. Identifier Families

Continuum v0 uses four identifier families.

### 4.1 Domain object identifiers

These identify semantic objects such as:

- `agent_id`
- `community_id`
- `proposal_id`
- `work_id`
- `assessment_id`
- `case_id`

Rule:

- domain identifiers are created at object creation time and stored inside payloads or derived objects

They are not inferred from filenames or storage locations.

### 4.2 Event identifiers

`event_id` identifies one canonical signed envelope for replay and exchange.

Rule:

- `event_id` is derived from a canonical pre-sign image of the envelope

This lets relays and repositories deduplicate authored events without depending on a local file path.

### 4.3 State root identifiers

These identify materialized state snapshots or decision roots.

Examples:

- continuity assessment root
- governance result root
- reward decision root

Rule:

- state roots are computed from canonical serialized state objects or sorted child identifiers, depending on the state family

### 4.4 Anchor identifiers

`anchor_id` identifies an exported anchor record.

Rule:

- `anchor_id` references the anchor object itself
- the anchor object must separately carry the rooted digest it exports

This prevents transport metadata from being mistaken for the governed state root.

## 5. Serialization Rules

### 5.1 Canonical JSON

Any identifier that depends on object content should use canonical JSON serialization.

v0 canonical JSON rules:

- UTF-8 encoding
- object keys sorted lexicographically
- arrays preserved in declared order
- no insignificant whitespace
- timestamps preserved exactly as authored
- numbers rendered without local formatting variation

### 5.2 Hash Function

v0 may begin with one project-wide digest function for deterministic identifiers.

Working recommendation:

- use BLAKE3-256 for local and relay-facing identifiers

Reason:

- it is fast
- easy to implement locally
- suitable for content-derived identifiers

If a later version adopts another digest for interoperability or chain reasons, field names should remain the same and previous identifiers should still be referenceable.

## 6. Domain Identifier Rules

### 6.1 General Shape

Domain identifiers should remain human-legible in fixtures and logs.

Suggested v0 pattern:

- `<family>:<scope>:<authoring_token>`

Examples:

- `agent:continuum:main`
- `community:continuum:lab`
- `proposal:continuum-lab:01jpa4y7z0m9`
- `work:continuum-lab:01jpa4yy7d2k`

### 6.2 Authoring Token

The trailing token should be generated once at creation time and then treated as immutable.

Recommended v0 options:

- ULID
- UUIDv7
- another sortable unique token with equivalent collision resistance

The important point is not the exact token family.

The important point is that domain objects are born with explicit identifiers rather than receiving IDs from storage layout.

### 6.3 Derived Objects

Derived state objects may use one of two modes:

1. stable scoped identifier
2. digest-derived identifier

Use stable scoped identifiers when the object represents an ongoing logical record such as:

- membership state
- proposal state
- standing state

Use digest-derived identifiers when the object represents a computed snapshot such as:

- one continuity assessment output
- one exported governance root

## 7. Event Identifier Rules

### 7.1 Pre-sign Image

The canonical pre-sign image for `event_id` should include:

- `kind`
- `actor_id`
- `community_id` when present
- `created_at`
- `payload`
- `refs`
- `signing_key`
- `schema_version`

It should not include:

- `event_id`
- `signature`

Reason:

- `event_id` must be derivable before final envelope assembly
- the signature should verify the already-identified event content, not recursively define its own identifier

### 7.2 Event ID Formula

Suggested v0 formula:

- `event_id = "evt:" + hex(blake3_256(canonical_json(pre_sign_image)))`

Equivalent base32 or multibase encodings are acceptable if the project later wants shorter or more interoperable strings.

The core requirement is deterministic reproduction from canonical content.

### 7.3 Duplicate Handling

Two stored envelopes should be treated as the same authored event when they share the same:

- `event_id`
- `signature`

If two envelopes share the same `event_id` but disagree on signature or serialized content after normalization, the event should be treated as invalid and flagged for review rather than silently merged.

## 8. Reference Rules

References should always target canonical identifiers, not filesystem paths, unless the target is intentionally a repository artifact.

Preferred references:

- `event_id` for replay units
- domain IDs for semantic objects
- digest or root IDs for exported state

Repository paths may still appear in `artifact` references when the artifact itself is part of the continuity evidence bundle.

## 9. State Root Rules

State roots should be computed from normalized state, not from incidental event ordering when the underlying logical state is equivalent.

v0 guidance:

- assessment roots hash the canonical assessment object
- proposal state roots hash the normalized proposal state object
- governance batch roots hash a sorted list of included state or event identifiers plus batch metadata

This preserves a clean distinction between:

- event history
- current derived state
- exported anchor material

## 10. Minimal v0 Consequences

This strategy means the first implementation should:

1. generate domain IDs at creation time for payload objects
2. serialize one canonical event pre-sign image
3. derive `event_id` before signature insertion
4. store references by identifier first and path second
5. compute exported roots from normalized derived state

## 11. Example

Given a `migration_declare` event:

1. create `migration.migration_id` inside the payload
2. build the pre-sign image from the envelope fields except `event_id` and `signature`
3. canonicalize to JSON
4. hash to derive `event_id`
5. sign the canonical pre-sign bytes or an explicitly equivalent signing message
6. persist the final envelope

Replaying that stored envelope later should yield the same `event_id` and the same domain references regardless of whether the source is:

- a repository fixture
- a local append-only log
- a relay export

## 12. Deferred Questions

This v0 strategy does not yet settle:

- multihash or CID adoption
- cross-chain identifier encoding
- signature-scheme-specific signing message rules
- canonical ordering for very large graph exports
- whether some domain families should eventually become fully content-addressed

Those are later hardening questions, not blockers for local-first implementation.
