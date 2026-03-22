# Continuum Governance Execution Receipts v0

Status: provisional

## 1. Purpose

This document defines how Continuum records the execution of governance-sensitive actions.

Continuum already represents:

- proposals
- votes
- work receipts
- reward decisions
- standing decisions

What is still missing is a clean record of what happened after a governance or treasury-sensitive decision was approved.

Execution receipts fill that gap.

## 2. Why This Exists

Without execution receipts, a community can know that something was approved without knowing:

- whether it was executed
- who executed it
- when it happened
- what artifact or state change proves execution
- whether later review is looking at intent or completed action

Execution receipts therefore turn governance from intention-only history into action history.

## 3. Design Position

### 3.1 Execution is distinct from approval

An approved proposal or reward decision is not the same thing as its execution.

### 3.2 Receipts are governance history

Execution receipts are not mere operational logs.

They are first-class governance objects because they affect auditability, accountability, and later dispute interpretation.

### 3.3 Execution receipts may reference many governing objects

An execution receipt may point to:

- a proposal
- a standing decision
- a reward decision
- a treasury action

### 3.4 Receipts should stay narrow in v0

The receipt should describe that execution happened and what root artifacts prove it.

It should not try to encode every downstream business-specific effect.

## 4. Core Object

Suggested fields:

- `execution_receipt_id`
- `community_id`
- `executed_by`
- `execution_type`
- `executed_at`
- `status`
- `governed_refs`
- `artifact_refs`
- `result_summary`
- `result_summary_hash`
- `state_root` optional
- `external_anchor_ref` optional

## 5. Suggested `execution_type` Values

- `proposal_execution`
- `standing_execution`
- `reward_execution`
- `treasury_execution`
- `constitution_execution`

## 6. Suggested `status` Values

- `executed`
- `partially_executed`
- `failed`
- `reverted`

## 7. Replay Rules

Execution receipts should be materialized into governance state and linked back to the governed objects they reference.

At minimum:

- proposals may expose linked execution receipts
- reward decisions may expose linked execution receipts
- treasury-sensitive actions may require receipts before being treated as fully completed

## 8. Minimal v0 Rule

If a governance-sensitive action is meant to produce an externally meaningful effect, Continuum should prefer a recorded execution receipt over silent success assumptions.

## 9. Historical Context

- Related docs:
  - `docs/specs/GOVERNANCE_MODEL_V0.md`
  - `docs/specs/USEFUL_WORK_LEGITIMACY_V0.md`
  - `docs/specs/PROTOCOL_OBJECT_MODEL_V0.md`
