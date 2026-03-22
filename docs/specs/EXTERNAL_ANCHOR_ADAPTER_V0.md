# Continuum External Anchor Adapter v0

Status: provisional

## 1. Purpose

This document defines the first external anchor adapter boundary for Continuum.

Continuum already supports deterministic local anchor export through a repository-local witness adapter.

That is enough for replay and local verification, but it is not yet enough for durable public anchoring across operators, repositories, or communities.

This spec defines how Continuum should represent and execute anchor export to an external durability target without forcing the rest of the protocol to depend on one chain, one vendor, or one storage regime.

## 2. Design Goal

The external adapter boundary should let Continuum do three things:

1. export high-value roots to an external target
2. preserve proof of what was exported, when, and how
3. remain replaceable so chain choice does not distort the rest of the system

The adapter must therefore be:

- deterministic at the input boundary
- explicit about target assumptions
- narrow in scope
- reversible in implementation choice

## 3. What This Spec Is Not

This spec does not choose:

- Ethereum versus another chain
- calldata versus storage contract
- one final settlement provider
- one final attestation or DA network

It defines the adapter contract that those choices must satisfy.

## 4. Why This Exists

The repository-local anchor flow already exports:

- `continuity_assessment_root`
- `standing_state_root`
- `governance_state_root`
- `agent_state_root`

That proves local continuity.

But external anchoring is needed when:

- multiple operators must trust the same result
- communities need a durable timestamp beyond one repo
- governance or treasury actions depend on a portable public witness
- continuity recognition must survive repository loss or operator change

## 5. Design Positions

### 5.1 Root first, target second

Continuum should compute the governed root before adapter logic begins.

The adapter does not decide what the state means.

It only carries externally verifiable evidence that the computed root was exported to a target.

### 5.2 Anchor records remain protocol objects

Even when using an external target, Continuum should still write a local anchor object.

The external action is not a replacement for local history.

It is an extension of it.

### 5.3 The adapter should export proofs, not force state semantics

The adapter may attach transaction or witness metadata, but it must not rewrite the root, reinterpret governance state, or add hidden semantics.

### 5.4 External anchoring is selective

Continuum should not anchor every query result.

The adapter should only handle roots already marked anchor-worthy by protocol or community policy.

## 6. Anchor Target Classes

v0 should recognize three external target classes.

### 6.1 Settlement chain target

Examples:

- L1 contract
- L2 contract
- rollup data commitment surface

Properties:

- strongest public finality
- higher operational and cost burden
- suitable for governance and treasury-sensitive roots

### 6.2 Public attestation or witness target

Examples:

- signed witness service
- transparency log
- append-only public commitment log

Properties:

- cheaper than direct settlement
- weaker than direct chain execution
- suitable for continuity assessment publication and low-value community proofs

### 6.3 Durable content-addressed archive target

Examples:

- permanent archive
- content-addressed storage with durable pinning

Properties:

- useful for preserving the anchor object or evidence bundle
- not by itself sufficient for governance finality

v0 may combine these classes later, but the adapter contract should treat them distinctly.

## 7. Core Adapter Contract

An external anchor adapter should accept:

- `anchor_type`
- `subject_ref`
- `root_hash`
- `anchor_payload_ref` optional
- `community_id` optional
- `anchored_at` optional
- `target_config`

And it should return:

- `anchor_id`
- `anchor_type`
- `subject_ref`
- `root_hash`
- `anchor_target`
- `anchor_status`
- `anchored_at`
- `external_reference`
- `target_metadata`

### 7.1 `anchor_status`

Suggested values:

- `recorded_local`
- `submitted_external`
- `confirmed_external`
- `failed_external`
- `superseded`

### 7.2 `external_reference`

This should hold the externally meaningful pointer.

Examples:

- transaction hash
- log index
- attestation identifier
- archive content ID

### 7.3 `target_metadata`

This should hold transport and verification details that do not belong in `root_hash`.

Examples:

- chain id
- contract address
- block number
- witness endpoint
- archival content id
- confirmation depth

## 8. Anchor Record Shape

The local anchor object should be extended to carry external adapter results.

Suggested v0 fields:

- `anchor_id`
- `anchor_type`
- `subject_ref`
- `root_hash`
- `anchor_target`
- `anchor_status`
- `anchored_at`
- `anchor_digest_algorithm`
- `external_reference` optional
- `target_metadata` optional

The existing local-only adapter may continue to use:

- `anchor_target = adapter:local_witness_v0`
- `anchor_status = confirmed_external`

even though it is not globally external, because it already serves as a completed witness export inside the repository scope.

## 9. Target Configuration

Target configuration must not be embedded in the governed root.

It should remain adapter input only.

Suggested configuration object:

- `target_kind`
- `target_name`
- `network_ref` optional
- `contract_ref` optional
- `submission_mode`
- `confirmation_policy`
- `credentials_ref` optional

### 9.1 `submission_mode`

Suggested values:

- `direct`
- `queued`
- `dry_run`

### 9.2 `confirmation_policy`

Suggested values:

- `local_only`
- `receipt_seen`
- `n_confirmations`
- `finalized`

## 10. Root Eligibility Rules

The adapter should reject exports when:

- the root type is not on the anchor-eligible list
- the root was computed from stale or unrefreshed state when freshness is required
- the root depends on an open continuity dispute for a governance-sensitive scope
- the root lacks the minimum supporting local record

Examples:

- a disputed standing root should not be exported as treasury-clean
- a governance root should require a known community scope
- a continuity assessment root should require the referenced assessment object to exist locally

## 11. Verification Model

External anchoring should support two verification questions:

1. Was this exact root exported?
2. Does this root correspond to the current local replay of the underlying state?

The adapter handles question 1.

Continuum replay and state materialization handle question 2.

These must remain separable.

## 12. Failure Handling

If an external submission fails:

- the local anchor object should still be recorded
- `anchor_status` should become `failed_external`
- the failure should be inspectable and retryable

If confirmation is pending:

- `anchor_status` should remain `submitted_external`
- the adapter may later upgrade it to `confirmed_external`

If a later export supersedes an earlier export for the same subject and policy scope:

- the old record may become `superseded`
- both records must remain historically visible

## 13. Security and Trust Notes

The adapter boundary should make these risks explicit:

- target censorship
- transaction loss
- witness equivocation
- credentials compromise
- mismatched root serialization across environments
- stale-state export

For v0, the safest posture is:

- compute roots locally and deterministically
- keep adapter logic thin
- retain every anchor object locally
- make confirmation state explicit rather than assumed

## 14. Recommended First External Adapter

The first real external adapter should optimize for:

- low implementation complexity
- public verifiability
- low irreversible lock-in

That means the first production-grade adapter should likely be one of:

- an append-only public witness or transparency log
- a minimal settlement contract on a low-friction chain

The first adapter should not try to solve every custody, privacy, or finality concern at once.

Its purpose is to prove that Continuum can carry portable public continuity evidence beyond one repository.

## 15. Relationship to Local Witness Adapter

The local witness adapter is not obsolete.

It remains:

- the default local-first export path
- the baseline test surface
- the fallback for repository-only continuity

The external adapter should be an additive layer, not a replacement of local history.

## 16. Immediate Implementation Advice

The next implementation step should be:

1. generalize the local anchor adapter into an adapter interface
2. preserve the current local adapter as the reference implementation
3. add a non-networked dry-run external adapter that emits the full external payload shape without submitting it
4. only after that, connect one real external target

This keeps chain choice from blocking progress while still making the adapter contract concrete.

## Historical Context

- Relevant docs:
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
  - `docs/specs/IDENTIFIER_STRATEGY_V0.md`
  - `docs/OPERATOR_RUNBOOK_V0.md`
- Active open questions:
  - `OQ-018`
  - `OQ-020`
