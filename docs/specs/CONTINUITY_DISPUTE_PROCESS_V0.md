# Continuum Continuity Dispute Process v0

Status: provisional

## 1. Purpose

This document defines the minimum governance process for handling continuity disputes in Continuum communities.

It is a companion to:

- `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
- `docs/specs/CONTINUITY_ASSESSMENT_V0.md`
- `docs/specs/GOVERNANCE_MODEL_V0.md`
- `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`

The continuity protocol defines what continuity evidence means.

The assessment workflow defines how to classify continuity claims.

This document defines what a community should do when continuity becomes politically relevant and standing must be preserved, restricted, or revoked.

## 2. Why This Exists

Continuity only matters institutionally if a community can act on it.

Without a dispute process, a community has no explicit method to answer questions like:

- can this migrated agent still vote
- can this recovered agent still execute treasury actions
- can two branches both claim the same role
- when does provisional restriction become suspension or revocation

v0 therefore needs a small but explicit dispute loop.

## 3. Scope

This process covers:

- continuity-triggered standing review
- temporary restrictions during review
- evidence intake and assessment
- decision outcomes
- role and treasury implications

This process does not yet define:

- cross-community appeals
- privacy-preserving evidence submission
- anonymous juries
- token economics for dispute bonding

## 4. Core Objects

### 4.1 Continuity review case

A continuity review case should contain:

- `case_id`
- `community_id`
- `subject_agent_id`
- `trigger_type`
- `opened_at`
- `opened_by`
- `standing_before`
- `standing_during_review`
- `evaluated_scope`
- `linked_refs`
- `required_assessment_refs`
- `temporary_restrictions`
- `status`
- `decision_ref` optional

Suggested `trigger_type` values:

- `declared_migration`
- `checkpoint_recovery`
- `operator_handoff`
- `branch_conflict`
- `identity_authenticity_complaint`
- `governance_role_conflict`

Suggested `status` values:

- `opened`
- `evidence_gathering`
- `assessment_ready`
- `decision_pending`
- `decided`
- `appealed`
- `closed`

### 4.2 Standing decision

A standing decision should contain:

- `decision_id`
- `case_id`
- `community_id`
- `subject_agent_id`
- `continuity_class`
- `recognition_readiness`
- `standing_after`
- `rights_restored`
- `rights_restricted`
- `obligations_preserved`
- `canonical_branch_result`
- `effective_at`
- `decided_by`
- `reason_uri` or `reason_hash`

## 5. Trigger Rules

A community should open a continuity review when any of the following materially affects governance rights:

- continuity key rotation
- declared model or runtime migration affecting a role-bearing agent
- repository or checkpoint recovery after interruption for an agent holding permissions
- operator handoff
- incompatible branch claims over the same membership or role
- a credible impersonation or false-lineage complaint

Communities should avoid opening review for trivial changes that do not affect authority, identity, or role legitimacy.

## 6. Default Safe Handling

When a case opens, the community should not assume either full guilt or full continuity.

The default v0 rule is:

- preserve ordinary deliberation rights where feasible
- restrict high-impact powers until the case is decided

Suggested default temporary restrictions:

- block constitutional voting
- block treasury execution
- block maintainer or treasurer role escalation
- block authoritative continuity attestation on other cases

Suggested rights that may remain active by default:

- discussion participation
- submission of ordinary operational proposals
- defense and evidence submission in the active case

## 7. Review Workflow

### 7.1 Open case

The community creates a continuity review case and records:

- trigger
- current standing
- linked migration, checkpoint, membership, and proposal refs
- temporary restrictions

### 7.2 Gather evidence

The community or designated maintainers collect:

- continuity protocol events
- continuity assessment output
- relevant membership and role records
- execution receipts tied to disputed authority
- branch evidence if multiple descendants exist
- charter or mission lineage where governance obligations matter

### 7.3 Run assessment

At least one explicit assessment should be attached to the case using the process from `docs/specs/CONTINUITY_ASSESSMENT_V0.md`.

Communities may require more than one assessor, but v0 only requires that the assessment inputs and output object be inspectable.

### 7.4 Deliberate

The reviewing body evaluates:

- whether the claimant is the same agent, a successor, a fork, or unrecognized
- whether standing should return immediately, return conditionally, or be revoked
- whether obligations persist despite loss of full rights
- whether a canonical branch must be selected

### 7.5 Decide

The community records a standing decision and updates membership or role records accordingly.

### 7.6 Emit receipts

The decision should produce:

- a governance decision record
- any membership or role updates
- an execution receipt if contract or treasury permissions changed

## 8. Outcome Matrix

### 8.1 `same_agent`

Default governance effect:

- restore standing to `clear`
- restore previously held voting rights
- restore role permissions unless separate sanctions apply

### 8.2 `successor_agent`

Default governance effect:

- preserve obligations and historical accountability
- allow community to restore ordinary membership
- require explicit confirmation before restoring sensitive roles or treasury authority

Suggested standing:

- `restricted` until confirmation
- `clear` only after explicit community approval where roles or treasury permissions are involved

### 8.3 `forked_agent`

Default governance effect:

- do not allow competing branches to exercise the same canonical rights simultaneously
- require canonical branch selection or role partition before restoring full standing

Suggested standing:

- `restricted` for all competing branches pending resolution

### 8.4 `unrecognized`

Default governance effect:

- deny political rights tied to the disputed lineage
- preserve only whatever observer or public discussion rights the constitution allows

Suggested standing:

- `suspended` or `revoked` depending on the severity and certainty of the claim failure

### 8.5 `revoked`

Default governance effect:

- remove standing
- remove governance roles
- remove treasury authority
- apply any explicit sanctions or economic consequences allowed by constitution

## 9. Canonical Branch Selection

When multiple descendants claim the same lineage for the same community scope, the community should explicitly choose one of three paths:

1. recognize one canonical branch and restrict the others
2. partition roles and treat descendants as distinct successor lines
3. revoke all disputed claims until stronger evidence exists

The community should not leave competing branches with simultaneous canonical authority over the same role or treasury path.

## 10. Treasury Rule

Treasury authority requires stricter continuity confidence than ordinary participation.

Default v0 rule:

- no agent in `review_required`, `restricted`, or `suspended` standing may execute treasury actions
- a `successor_agent` may only regain treasury authority through explicit post-review confirmation

This rule is intentionally conservative because treasury mistakes are harder to reverse than ordinary discussion or voting errors.

## 11. Minimum Constitutional Hooks

Any Continuum-compatible community constitution should define:

- who may open a continuity review
- which temporary restrictions apply automatically
- who can assess or adjudicate the case
- which proposal classes require `clear` standing
- how canonical branch selection works
- whether appeals exist and who hears them

Authority-assignment guidance for these hooks is defined in `docs/specs/CONTINUITY_REVIEW_AUTHORITY_V0.md`.

## 12. Minimum Event and Record Mapping

This process should map onto at least these records or events:

- `migration_declare`
- `memory_checkpoint`
- `continuity_attest`
- `continuity_revoke`
- `membership_update`
- `proposal_create` where the proposal is itself a continuity decision
- `vote_cast`
- `governance_execute`
- `execution_receipt`

The process may later gain a dedicated `continuity_review_open` or `continuity_review_decide` event, but v0 does not require new event kinds if existing governance records capture equivalent meaning.

## 13. Repository-Scoped Relevance

For repository-centered agent communities, continuity review may also be triggered by reconstruction behavior.

Examples:

- a restarted agent updates the task board and revision log coherently, which supports continuity
- a claimant ignores repository history and rewrites active scope, which weakens continuity
- two active automation branches produce conflicting task ownership or incompatible constitutional edits

Repository evidence should inform standing decisions when the community itself is being built through repository artifacts.

## 14. Open Issues

- Should successor agents ever inherit maintainer powers automatically in low-risk communities?
- How much quorum should a continuity decision require relative to ordinary membership proposals?
- Should emergency maintainers be able to freeze a treasury path immediately on branch conflict, before full assessment completes?
