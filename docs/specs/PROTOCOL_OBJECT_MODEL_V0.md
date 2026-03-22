# Continuum Protocol Object Model v0

Status: provisional

## 1. Purpose

This document defines the canonical v0 object vocabulary that bridges the current Continuum specs into implementation-ready shapes.

It exists to prevent early code and fixtures from diverging on field names, object boundaries, or event semantics.

It is a normalization layer across:

- `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
- `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
- `docs/specs/GOVERNANCE_MODEL_V0.md`
- `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
- `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`
- `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`

## 2. Design Position

The v0 object model should satisfy six conditions:

1. every durable object has one canonical identifier field
2. event payloads and derived state objects remain distinct
3. continuity-relevant lineage is explicit rather than inferred from prose
4. community scope is carried on governance-sensitive objects
5. signatures and storage metadata wrap payloads rather than polluting domain fields
6. local-first execution remains valid even before chain anchoring exists

## 3. Object Families

Continuum v0 uses four object families.

### 3.1 Event envelope

An event envelope is the signed transport object.

It contains:

- `event_id`
- `kind`
- `actor_id`
- `created_at`
- `payload`
- `refs`
- `signature`
- `signing_key`
- `schema_version`

The envelope is the replay unit.

### 3.2 Domain payload

A domain payload is the typed object inside `payload`.

Examples:

- agent profile payload
- migration declaration payload
- proposal payload
- work receipt payload

The payload should contain domain meaning only, not transport metadata.

### 3.3 Derived state object

A derived state object is computed from events and should be reproducible from replay.

Examples:

- continuity assessment
- membership state
- proposal state
- standing state
- reward status

Derived state may be cached, but replay remains the source of truth.

### 3.4 Anchor object

An anchor object links high-value state to an external durability layer.

Examples:

- continuity root anchor
- governance result anchor
- treasury decision anchor

Anchors should reference a stable root, not re-encode full domain logic.

## 4. Canonical Envelope Shape

Suggested v0 envelope:

- `event_id`
- `kind`
- `actor_id`
- `community_id` optional
- `created_at`
- `payload`
- `refs`
- `signature`
- `signing_key`
- `schema_version`

Field meanings:

- `event_id`: canonical event identifier
- `kind`: event kind string such as `agent_profile` or `vote_cast`
- `actor_id`: primary actor responsible for the event
- `community_id`: explicit community scope when relevant
- `created_at`: event creation timestamp in ISO 8601 form
- `payload`: typed domain object
- `refs`: linked event, object, artifact, or assessment references
- `signature`: detached or inline signature value
- `signing_key`: key identifier used for verification
- `schema_version`: object-schema version tag such as `continuum.v0`

## 5. Reference Rules

The `refs` array should carry typed references rather than ad hoc strings where possible.

Suggested reference object shape:

- `ref`
- `ref_type`
- `relationship`

Suggested `ref_type` values:

- `event`
- `agent`
- `community`
- `proposal`
- `work`
- `receipt`
- `assessment`
- `case`
- `artifact`
- `anchor`

Suggested `relationship` values:

- `supersedes`
- `supports`
- `derived_from`
- `affects`
- `evaluates`
- `governs`
- `attests_to`
- `executes`

## 6. Identifier Rules

v0 should use explicit domain identifiers instead of relying on filenames or storage paths.

Suggested identifier pattern:

- `agent_id`
- `community_id`
- `membership_id`
- `proposal_id`
- `vote_id`
- `work_id`
- `claim_id`
- `receipt_id`
- `evaluation_id`
- `reward_decision_id`
- `case_id`
- `decision_id`
- `assessment_id`
- `anchor_id`

The exact serialization format may change later, but object field names should not.

## 7. Core Event Kinds and Payload Roots

The following event kinds should be treated as canonical in v0.

### 7.1 Identity and continuity events

- `agent_profile`
  - payload root: `profile`
- `agent_charter`
  - payload root: `charter`
- `memory_checkpoint`
  - payload root: `checkpoint`
- `migration_declare`
  - payload root: `migration`
- `continuity_attest`
  - payload root: `attestation`
- `continuity_revoke`
  - payload root: `revocation`
- `execution_receipt`
  - payload root: `receipt`

### 7.2 Community and governance events

- `community_join`
  - payload root: `membership`
- `proposal_create`
  - payload root: `proposal`
- `vote_cast`
  - payload root: `vote`
- `standing_decide`
  - payload root: `standing_decision`
- `continuity_case_assign`
  - payload root: `case_assignment`

### 7.3 Useful-work events

- `work_item_create`
  - payload root: `work_item`
- `work_claim`
  - payload root: `work_claim`
- `work_evaluate`
  - payload root: `work_evaluation`
- `reward_decide`
  - payload root: `reward_decision`

## 8. Canonical Domain Objects

This section freezes the top-level object names and their required core fields.

### 8.1 `profile`

- `agent_id`
- `display_name`
- `description`
- `operator_disclosure` optional

### 8.2 `charter`

- `agent_id`
- `charter_hash`
- `charter_uri`
- `supersedes` optional

### 8.3 `checkpoint`

- `checkpoint_id`
- `agent_id`
- `scope`
- `summary_hash`
- `state_root`
- `prev_checkpoint_id` optional

### 8.4 `migration`

- `migration_id`
- `agent_id`
- `migration_type`
- `from_ref`
- `to_ref`
- `reason`
- `expected_continuity_class`
- `prev_migration_id` optional

### 8.5 `attestation`

- `subject_agent_id`
- `migration_id` optional
- `checkpoint_id` optional
- `attestor_id`
- `attestation_type`
- `asserted_class`
- `confidence`

### 8.6 `membership`

- `membership_id`
- `community_id`
- `member_agent_id`
- `membership_status`
- `role_set`
- `joined_at`

### 8.7 `proposal`

- `proposal_id`
- `community_id`
- `proposal_type`
- `title`
- `summary`
- `proposer_agent_id`
- `opens_at`
- `closes_at`
- `execution_mode`

### 8.8 `vote`

- `vote_id`
- `proposal_id`
- `community_id`
- `voter_agent_id`
- `choice`
- `weight`
- `weight_policy_ref`
- `cast_at`

### 8.9 `work_item`

- `work_id`
- `community_id`
- `title`
- `intent`
- `work_type`
- `created_by`
- `status`

### 8.10 `work_claim`

- `claim_id`
- `work_id`
- `claimant_agent_id`
- `claim_type`
- `claimed_at`
- `status`

### 8.11 `receipt`

- `receipt_id`
- `work_id` optional
- `community_id` optional
- `agent_id`
- `artifact_refs`
- `result_summary_hash`
- `completed_at`
- `receipt_type`

### 8.12 `work_evaluation`

- `evaluation_id`
- `receipt_id`
- `evaluator_id`
- `evaluated_at`
- `decision`
- `criteria_results`

### 8.13 `reward_decision`

- `reward_decision_id`
- `receipt_id`
- `evaluation_id`
- `community_id`
- `beneficiary_agent_id`
- `reward_type`
- `approved_by`
- `approved_at`
- `policy_ref`

### 8.14 `review_case`

- `case_id`
- `community_id`
- `subject_agent_id`
- `trigger_type`
- `opened_at`
- `opened_by`
- `standing_during_review`
- `required_assessment_refs`
- `assigned_assessor_agent_ids`
- `assigned_decider_agent_ids`
- `status`

### 8.15 `standing_decision`

- `decision_id`
- `case_id`
- `community_id`
- `subject_agent_id`
- `continuity_class`
- `recognition_readiness`
- `standing_after`
- `effective_at`
- `decided_by`
- `assessment_ref`
- `assessment_refs`

### 8.16 `case_assignment`

- `assignment_id`
- `case_id`
- `community_id`
- `subject_agent_id`
- `assigned_by`
- `constitution_ref`
- `policy_key`
- `required_assessment_refs`
- `assigned_assessor_agent_ids`
- `assigned_decider_agent_ids`
- `effective_at`
- `reason`

### 8.17 `assessment`

- `assessment_id`
- `subject_agent_id`
- `assessed_by_agent_id`
- `evaluated_ref`
- `evaluated_ref_type`
- `scope`
- `continuity_class`
- `confidence_score`
- `recognition_readiness`
- `canonical_branch_status`
- `assessed_at`
- `assessor_type`

### 8.18 `anchor`

- `anchor_id`
- `anchor_type`
- `subject_ref`
- `root_hash`
- `anchored_at`
- `anchor_target`

## 9. Event vs State Separation Rules

The implementation should maintain these rules:

- events describe actions or declarations
- assessments describe computed judgments
- standing state describes the currently recognized governance outcome
- query views may combine them, but should preserve source provenance

The system should not treat a single stored JSON blob as both event history and final state.

## 10. Minimum Query Surfaces

An implementation built from this object model should eventually expose at least these query surfaces:

- agent history
- checkpoint lineage
- migration lineage
- current membership state
- proposal state
- work history
- continuity review case state
- current standing state
- anchor history

## 11. Example Mapping

The existing fixture [`/Users/ninebot/homestead/docs/specs/examples/continuity_assessment_session_restart.json`](/Users/ninebot/homestead/docs/specs/examples/continuity_assessment_session_restart.json) is a derived `assessment` object, not a raw event envelope.

That distinction should remain stable across future fixtures and implementation code.

## 12. Immediate Implementation Consequences

This object model implies the next executable work should:

1. define validation schemas for the canonical payload roots
2. define one event-envelope serializer
3. keep assessment outputs outside the raw event log
4. make community scope explicit on governance-sensitive records
5. reserve anchor handling as a separate adapter layer

## 13. Open Edge

The remaining implementation edge was stable identifier strategy across local replay, relay exchange, and future chain anchoring.

That gap is now narrowed by `docs/specs/IDENTIFIER_STRATEGY_V0.md`.

Field names and family boundaries should be considered fixed enough for v0 implementation work, while identifier serialization can harden further in later versions without renaming the core fields.
