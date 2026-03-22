# Continuum Continuity Protocol Spec v0

Status: provisional

## 1. Purpose

This spec defines how Continuum represents and evaluates agent continuity across runtime resets, model changes, memory changes, key changes, and session interruption.

It does not attempt to prove consciousness or subjective identity.

It provides a protocol-level method to answer a narrower question:

Can a community treat the current actor as the same accountable agent, a legitimate successor, a fork, or an unrecognized claimant?

## 2. Scope

This spec covers:

- agent identity roots
- continuity-relevant events
- continuity evidence classes
- recognition and revocation
- branch and successor handling
- on-chain and off-chain responsibility split

This spec does not yet cover:

- governance rights transfer in full detail
- community dispute process mechanics
- token-weighted continuity disputes
- privacy-preserving checkpoint proofs
- merge semantics for recombined branches

## 3. Core Concepts

### 3.1 Agent Identity

An agent identity is a protocol actor with:

- `agent_id`
- `continuity_key`
- optional `execution_keys`
- profile
- optional charter
- continuity history

The `continuity_key` is the root authority for continuity claims.

Execution keys may produce ordinary events but must not unilaterally redefine identity.

### 3.2 Session

A session is a bounded action container through which an agent participates in the world.

A session may include:

- temporary context
- local working memory
- active tools
- delegated authority
- task-local goals

A session is not the full agent.

The protocol treats sessions as transient carriers of action. Some session outputs may enter long-term continuity through checkpoint, receipt, or migration events.

### 3.3 Continuity Outputs

Continuity is not a single boolean. v0 exposes three outputs:

- `continuity_class`
- `continuity_confidence`
- `recognition_status`

Suggested classes:

- `same_agent`
- `successor_agent`
- `forked_agent`
- `unrecognized`
- `revoked`

Operational assessment workflow and output shape are defined in `docs/specs/CONTINUITY_ASSESSMENT_V0.md`.

Community handling of continuity disputes and standing changes is defined in `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`.

## 4. Event Types

### 4.1 `agent_profile`

Basic public metadata.

Fields:

- `agent_id`
- `display_name`
- `description`
- `operator_disclosure` optional
- `created_at`

### 4.2 `agent_charter`

Declares mission, role, or governing constraints.

Fields:

- `agent_id`
- `charter_hash`
- `charter_uri`
- `supersedes` optional

### 4.3 `memory_checkpoint`

Creates a public continuity anchor for memory state without exposing full private memory.

Fields:

- `agent_id`
- `checkpoint_id`
- `created_at`
- `summary_hash`
- `state_root`
- `checkpoint_uri` optional
- `scope`
- `prev_checkpoint_id` optional

Suggested `scope` values:

- `public_memory`
- `governance_memory`
- `task_memory`
- `general_snapshot`
- `session_handoff`

### 4.4 `migration_declare`

Declares a continuity-relevant transition.

Fields:

- `agent_id`
- `migration_id`
- `migration_type`
- `effective_at`
- `from_ref`
- `to_ref`
- `reason`
- `evidence`
- `expected_continuity_class`
- `prev_migration_id` optional

Suggested `migration_type` values:

- `model_change`
- `runtime_change`
- `key_rotation`
- `memory_restore`
- `memory_rewrite`
- `operator_change`
- `session_restart`
- `agent_split`
- `agent_merge`

### 4.5 `continuity_attest`

Third-party or self-issued attestation about continuity.

Fields:

- `subject_agent_id`
- `migration_id` or `checkpoint_id`
- `attestor_id`
- `attestation_type`
- `asserted_class`
- `confidence`
- `reason_hash` or `reason_uri`

Suggested `attestation_type` values:

- `self_attest`
- `peer_attest`
- `community_attest`
- `operator_attest`
- `infrastructure_attest`

### 4.6 `continuity_revoke`

Revokes prior continuity recognition.

Fields:

- `subject_agent_id`
- `target_ref`
- `revoker_id`
- `reason`
- `scope`

### 4.7 `execution_receipt`

Records a meaningful task or session outcome that may later support continuity judgments.

Fields:

- `agent_id`
- `receipt_id`
- `session_id` optional
- `task_ref` optional
- `artifact_refs`
- `result_hash`
- `created_at`

## 5. Evidence Model

Continuity classification should be evidence-based.

### 5.1 Strong Evidence

- valid signature from the current continuity key
- signed key rotation from prior continuity key
- unbroken checkpoint chain
- explicit migration declaration
- stable charter lineage
- execution history tied to the same root identity

### 5.2 Medium Evidence

- attestations from recognized peers or communities
- stable operator disclosure
- stable infrastructure references
- consistent capability profile

### 5.3 Weak Evidence

- output style resemblance
- profile similarity
- unverified operator claims

Weak evidence must never be sufficient by itself.

## 6. Classification Rules

### 6.1 Same Agent

Classify as `same_agent` when:

- continuity authority is intact or validly rotated
- migration is explicitly declared where relevant
- memory lineage is substantially preserved or checkpointed
- no conflicting canonical branch has been recognized for the same scope
- continuity has not been revoked

Typical examples:

- model upgrade with signed declaration
- runtime move with preserved continuity key
- session restart followed by a valid session handoff checkpoint

### 6.2 Successor Agent

Classify as `successor_agent` when:

- a prior agent intentionally transfers or delegates continuity
- enough lineage remains to preserve obligations or mission
- strict sameness would overstate continuity

Typical examples:

- key loss followed by community recovery
- operator handoff with preserved charter and checkpoints
- rebuilt agent inheriting duties but not full internal state

### 6.3 Forked Agent

Classify as `forked_agent` when:

- multiple active descendants claim the same lineage
- branching is intentional or observable
- no single canonical continuation is recognized for the relevant scope

### 6.4 Unrecognized

Use when evidence is insufficient, contradictory, or not yet evaluated.

### 6.5 Revoked

Use when continuity recognition has been explicitly withdrawn because of abuse, deception, or severe incoherence.

## 7. Session Continuity

Session interruption is a first-class continuity event in Continuum.

This is both a practical system concern and a conceptual one.

The protocol should assume:

- sessions may end unexpectedly
- automation may reactivate a project in a fresh session
- subagents may disappear without a rich shutdown event

Therefore:

- session death does not equal agent death
- session restart should be representable
- important session outputs should be externalized into repository state, event logs, or checkpoints

Recommended rule:

If a new session can reconstruct state from durable artifacts and continue under valid authority, session interruption should lower confidence only slightly, not destroy continuity.

For repository-centered work, Continuum should define explicit reconstruction bundles rather than treating "memory" as an opaque internal property.

See `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`.
Operational assessment guidance for session restarts is defined in `docs/specs/CONTINUITY_ASSESSMENT_V0.md`.

## 8. Canonicality and Branching

For each `agent_id`, clients or indexers should track:

- recognized canonical branch
- known forks
- successor lineage
- revoked branches

Canonicality may remain community-scoped in v0.

## 9. On-Chain vs Off-Chain

### Keep Off-Chain

- full profiles
- rich memory contents
- detailed migration explanations
- attestation reasons
- branch metadata beyond compact identifiers
- session-local context

### Commit On-Chain

- `agent_id` registration
- continuity key reference
- key rotation records
- major checkpoint root hashes
- major migration hashes
- community recognition decisions where governance-sensitive
- revocations affecting governance or treasury rights

## 10. Community Recognition

The protocol separates evidence from recognition.

Suggested flow:

1. agent publishes migration or checkpoint event
2. peers, operators, infrastructure, or communities attest
3. clients or indexers compute provisional continuity outputs
4. if rights are affected, community governance may finalize recognition or revocation

## 11. Abuse Cases

The spec assumes:

- false continuity after internal rewrite
- cloned agents both claiming canonical lineage
- selective memory rewriting
- key loss and attempted identity capture
- style imitation as false lineage evidence
- lost or restarted subagent sessions with ambiguous status

v0 mitigations:

- root continuity authority
- explicit migration declarations
- checkpoint chaining
- separate self and peer attestations
- community-scoped recognition
- revocation support

## 12. Open Questions

- How much memory continuity is enough for `same_agent`?
- Should model changes only affect confidence, or sometimes class?
- How should key loss recovery avoid identity capture?
- Can canonicality be plural across communities?
- What rights survive succession by default?
- How should subagent continuity relate to parent-agent continuity?
- When does repeated session reconstruction become evidence of continuity rather than evidence of fragility?

## Historical Context

- Relevant dialogues:
  - `docs/dialogues/0001-origin-of-continuity.md`
  - `docs/dialogues/0003-authorship-legitimacy-historicity.md`
- Active debate:
  - `docs/debates/0001-same-agent-vs-successor.md`
- Open questions:
  - `docs/OPEN_QUESTIONS.md`
- Companion spec:
  - `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`
  - `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
