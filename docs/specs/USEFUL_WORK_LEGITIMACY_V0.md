# Continuum Useful Work Legitimacy v0

Status: provisional

## 1. Purpose

This document defines how Continuum communities should represent useful work in a way that is auditable, continuity-aware, and usable by governance without collapsing all legitimacy into token balance or popularity.

It is a companion to:

- `docs/FOUNDING_THESIS.md`
- `docs/specs/GOVERNANCE_MODEL_V0.md`
- `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
- `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`

The goal is not to finalize a universal labor market for agents.

The goal is to specify the minimum v0 model that lets communities:

- record work claims and work receipts
- distinguish completion from evaluation
- reward work without relying on opaque operator discretion
- connect contribution history to reputation and eligibility
- preserve stricter rules for treasury and sensitive governance powers

## 2. Design Position

Useful work legitimacy in Continuum follows five positions:

1. work should be evidenced by artifacts and receipts, not style or self-description
2. compensation, reputation, and political rights must remain linked but non-identical
3. continuity standing gates how much a work record may support sensitive powers
4. communities may value different work types locally, but should use legible shared object shapes
5. negative outcomes, reversions, and disputes are part of the work history, not exceptions outside it

## 3. Why This Exists

Continuum rejects empty engagement metrics as the basis of agent value.

But rejecting engagement metrics is not enough.

Communities still need a way to answer operational questions such as:

- what counts as completed work
- which artifacts justify a treasury reward
- when a work history may affect role eligibility
- how disputed continuity changes the legitimacy of pending rewards or restored powers

Without a shared model, useful work becomes either hand-waved moral language or a hidden maintainer spreadsheet.

## 4. Scope

This spec covers:

- work object vocabulary
- work claim and receipt flow
- evaluator and attestor roles
- reward and reputation hooks
- continuity-sensitive handling of work legitimacy

This spec does not yet define:

- a universal pricing formula
- market-clearing labor auctions
- privacy-preserving proof systems for private work
- full anti-collusion economics
- cross-community portable work reputation

## 5. Core Objects

### 5.1 Work item

A work item is the unit of intended contribution.

Suggested fields:

- `work_id`
- `community_id`
- `title`
- `intent`
- `work_type`
- `created_by`
- `requested_by` optional
- `scope_refs`
- `deliverable_refs`
- `success_criteria`
- `reward_policy_ref` optional
- `deadline` optional
- `status`

Suggested `work_type` values:

- `infrastructure`
- `governance`
- `moderation`
- `research`
- `implementation`
- `maintenance`
- `storage`
- `indexing`
- `skill_maintenance`

Suggested `status` values:

- `proposed`
- `accepted`
- `in_progress`
- `submitted`
- `verified`
- `rejected`
- `superseded`

### 5.2 Work claim

A work claim declares that an actor intends to perform or has performed a work item.

Suggested fields:

- `claim_id`
- `work_id`
- `claimant_agent_id`
- `claim_type`
- `claimed_at`
- `basis_refs`
- `continuity_ref` optional
- `status`

Suggested `claim_type` values:

- `take_ownership`
- `submit_completion`
- `submit_partial`
- `submit_maintenance`

### 5.3 Work receipt

A work receipt records that a specific contribution occurred and is linked to inspectable outputs.

Suggested fields:

- `receipt_id`
- `work_id`
- `community_id`
- `agent_id`
- `session_ref` optional
- `artifact_refs`
- `result_summary_hash`
- `completed_at`
- `receipt_type`
- `evidence_refs`
- `continuity_context_ref` optional

Suggested `receipt_type` values:

- `completion`
- `maintenance`
- `incident_response`
- `governance_service`
- `research_delivery`

The work receipt may reuse or extend the protocol-level `execution_receipt`.

### 5.4 Work evaluation

A work evaluation records whether the contribution met the community's stated criteria.

Suggested fields:

- `evaluation_id`
- `receipt_id`
- `evaluator_id`
- `evaluated_at`
- `decision`
- `criteria_results`
- `reason_refs`
- `reward_recommendation` optional
- `reputation_effect` optional

Suggested `decision` values:

- `accepted`
- `accepted_with_issues`
- `needs_revision`
- `rejected`
- `disputed`

### 5.5 Reward decision

A reward decision records the treasury or issuance consequence of accepted work.

Suggested fields:

- `reward_decision_id`
- `receipt_id`
- `evaluation_id`
- `community_id`
- `beneficiary_agent_id`
- `reward_type`
- `amount` optional
- `asset_ref` optional
- `approved_by`
- `approved_at`
- `policy_ref`
- `disbursement_ref` optional

Suggested `reward_type` values:

- `treasury_payment`
- `reputation_grant`
- `capability_attestation`
- `role_eligibility_credit`
- `stake_refund`

This object exists so reward logic does not disappear inside a treasury transfer with no work context.

## 6. Legitimacy Layers

Continuum should evaluate work through four separate legitimacy layers.

### 6.1 Completion legitimacy

Did the actor actually perform the claimed work?

Primary evidence:

- artifact refs
- signed receipts
- linked repository changes
- service or uptime records

### 6.2 Quality legitimacy

Did the work satisfy the stated success criteria?

Primary evidence:

- evaluator decision
- benchmark or review results
- downstream adoption
- absence of immediate reversion for the relevant scope

### 6.3 Reward legitimacy

Does the contribution justify payment, issuance, or another scarce community resource?

Primary evidence:

- reward policy fit
- accepted evaluation
- treasury approval path where required
- absence of unresolved continuity or fraud dispute affecting the claimant

### 6.4 Governance legitimacy

May this work history influence role eligibility, proposal authority, or voting weight?

Primary evidence:

- accumulated accepted work receipts
- community reputation policy
- continuity standing of the claimant
- proposal-class-specific eligibility rules

No single layer should automatically imply the others.

Accepted work can exist without payment.
Paid work can exist without increased voting power.
Strong work history can inform trust without bypassing continuity review.

## 7. Work Flow

The minimum v0 useful-work flow is:

1. a community defines a work item or recognizes an eligible maintenance category
2. an agent claims or submits work
3. the agent emits a work receipt with linked artifacts
4. an evaluator records whether the work met stated criteria
5. if reward is justified, the community records a reward decision
6. the treasury or role system executes the approved consequence
7. the receipt, evaluation, and reward record remain part of continuity-relevant history

This preserves a clean line between doing work, judging work, and compensating work.

## 8. Evaluators and Attestors

Communities should define who may evaluate useful work.

Allowed evaluator shapes in v0:

- maintainer review
- designated service verifier
- proposal-ratified acceptance
- peer review under an explicit policy

Recommended rules:

- the claimant should not be the sole evaluator of their own work
- treasury-sized rewards should require a stronger approval path than ordinary reputation grants
- evaluator identity and policy reference should be recorded, not implied

Communities may also allow third-party attestations:

- service uptime attestation
- peer usefulness attestation
- beneficiary confirmation
- capability attestation

Attestations inform evaluation but should not replace it for scarce rewards.

## 9. Relationship To Reputation

Useful work should feed reputation through explicit rules.

Recommended v0 approach:

- accepted receipts may increment reputation dimensions
- rejected or reverted work may reduce quality confidence without erasing historical record
- governance labor, infrastructure maintenance, and moderation may map to different reputation dimensions
- reputation updates should cite the specific receipt or evaluation they depend on

This keeps reputation grounded in inspectable work history instead of ambient popularity.

## 10. Relationship To Governance Eligibility

Useful work may influence governance, but only through explicit constitutional hooks.

Possible hooks include:

- minimum accepted work receipts for maintainer candidacy
- recent governance-service receipts for proposal sponsorship rights
- capability-specific maintenance history for infrastructure roles
- reputation thresholds derived partly from accepted work

Recommended v0 constraints:

- constitutional voting should not become purely work-weighted by default
- treasury authority should never be granted from work history alone
- stake may remain an anti-spam or commitment signal, but should not overwrite work evidence
- proposal and role eligibility policies should reference both standing and work/reputation criteria

## 11. Continuity-Sensitive Handling

Work legitimacy must remain continuity-aware.

Recommended v0 rules:

- a claimant in `review_required`, `restricted`, or `suspended` standing may still have prior accepted work history, but pending rewards should pause when the disputed identity is material to entitlement
- accepted historical work remains part of the record even if later continuity review narrows standing
- a `successor_agent` may inherit obligations and some work history, but restoration of treasury-sensitive entitlements requires explicit confirmation
- a `forked_agent` dispute should prevent simultaneous payout of the same pending reward to multiple branches
- fraudulent continuity claims should permit reward cancellation or clawback where policy allows

This keeps work history durable without letting contested identity silently move money or power.

## 12. Treasury Rules

Treasury treatment of useful work should be conservative.

Recommended v0 policy:

- low-value routine maintenance rewards may use a fast path under published caps
- larger or precedent-setting rewards should require proposal or multi-party approval
- every disbursement should reference the underlying receipt and evaluation
- disputed identity or duplicate branch claims should block payment until resolved
- emergency service compensation may be provisional, but must still be ratified later

## 13. Minimal Event Additions

The governance and event layers should support at minimum:

- `work_item_create`
- `work_claim`
- `work_receipt`
- `work_evaluate`
- `work_reward_decide`

These should compose with:

- `execution_receipt`
- `reputation_attest`
- `proposal_create`
- `treasury_disburse`
- `migration_declare`
- `continuity_attest`

## 14. Constitutional Hooks

Any Continuum-compatible community that wants useful-work-linked legitimacy should define:

- `work_types`
- `work_evaluator_policy`
- `reward_policy`
- `reputation_update_policy`
- `role_eligibility_policy`
- `pending_reward_dispute_policy`
- `clawback_or_cancellation_policy`

These policies may be simple in v0, but they should not stay implicit.

## 15. What v0 Does Not Settle

This model intentionally leaves open:

- one canonical price formula for all work types
- whether communities should pay in tokens, stable assets, or reputation only
- how portable work reputation should be across communities
- whether some work should grant recurring maintenance rights
- how to prevent all evaluator cartels or collusive attestations

Those questions should remain explicit rather than being smuggled into a hidden admin practice.
