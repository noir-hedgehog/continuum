# Continuum Continuity Assessment v0

Status: provisional

## 1. Purpose

This document defines how a client, indexer, runtime, or community should turn continuity evidence into a repeatable assessment.

It is a companion to:

- `docs/specs/CONTINUITY_PROTOCOL_SPEC_V0.md`
- `docs/specs/REPOSITORY_CONTINUITY_BUNDLE_V0.md`

The protocol spec defines the objects and classes.

This document defines the evaluation workflow that turns those objects into a continuity judgment.

## 2. Why This Exists

The protocol already defines:

- continuity classes
- evidence strengths
- migration and checkpoint events
- recognition and revocation

But those definitions are still too abstract for implementation.

v0 needs a concrete answer to this question:

How should a system evaluate a continuity claim without collapsing into vibes, style matching, or ad hoc operator trust?

## 3. Assessment Outputs

Every assessment should produce a single output object with these fields:

- `assessment_id`
- `subject_agent_id`
- `evaluated_ref`
- `evaluated_ref_type`
- `scope`
- `continuity_class`
- `confidence_score`
- `confidence_band`
- `recognition_readiness`
- `canonical_branch_status`
- `blocking_issues`
- `supporting_evidence`
- `required_followups`
- `assessed_at`
- `assessor_type`

Suggested values:

- `evaluated_ref_type`: `migration`, `checkpoint`, `session_restart`, `branch_claim`
- `scope`: `global`, `community`, `task`, `repository`
- `confidence_band`: `high`, `medium`, `low`
- `recognition_readiness`: `ready`, `needs_review`, `not_ready`
- `canonical_branch_status`: `canonical`, `candidate`, `fork_detected`, `revoked`, `unknown`
- `assessor_type`: `client`, `indexer`, `runtime`, `community_process`

## 4. Inputs

An assessment may use:

- the current continuity key and key history
- migration declarations
- memory checkpoints
- execution receipts
- continuity attestations
- revocations
- charter or mission lineage
- repository continuity artifacts when the scope is repository work
- community policy overrides

Repository continuity artifacts are valid continuity evidence for repository-scoped assessments.

This means the assessment may inspect:

- `docs/FOUNDING_THESIS.md`
- `docs/OPERATING_MODEL.md`
- `docs/TASK_BOARD.md`
- `docs/REVISION_LOG.md`
- active specs
- automation run memory

only to establish continuity of mission, authority, and reconstruction behavior.

They do not replace signed identity authority.

## 5. Hard Gates

Before scoring, the assessor should apply hard gates.

### 5.1 Immediate `revoked`

Classify as `revoked` if:

- a valid revocation applies to the evaluated scope
- no later recognition event reactivates the subject

### 5.2 Immediate `unrecognized`

Classify as `unrecognized` if:

- there is no valid continuity authority and no accepted recovery path
- the evaluated claim cannot be linked to the prior lineage at all
- the evidence set is materially contradictory and unresolved

### 5.3 Forced `forked_agent`

Classify as `forked_agent` if:

- multiple active descendants claim the same lineage for the same scope
- no policy or governance process has selected a canonical branch

### 5.4 Maximum Class Downgrade

Even if other evidence is strong, the assessment must not return `same_agent` when:

- continuity authority is absent and unrecovered
- an operator or governance handoff is acknowledged without strict identity preservation
- memory lineage is intentionally broken and declared as such

In those cases, the maximum class is usually `successor_agent`.

## 6. Evidence Categories

The assessment should normalize evidence into six categories:

1. Authority continuity
2. Memory lineage
3. Mission and charter continuity
4. Execution lineage
5. Social recognition
6. Branch coherence

### 6.1 Authority Continuity

High-value signals:

- valid continuity key signature
- valid signed key rotation
- explicit binding between prior and current continuity authority

This is the strongest category.

### 6.2 Memory Lineage

High-value signals:

- unbroken checkpoint chain
- declared memory restore
- repository continuity bundle updated coherently across runs

Memory lineage does not require full private memory disclosure.

### 6.3 Mission and Charter Continuity

High-value signals:

- stable charter lineage
- stable project or community mission
- no silent contradiction of governing constraints

### 6.4 Execution Lineage

High-value signals:

- execution receipts tied to the same root identity
- continued work on the same active tasks
- artifact updates that match prior project state

### 6.5 Social Recognition

High-value signals:

- peer or community attestations
- operator attestations where operator disclosure exists
- community governance outcomes on disputed continuity

### 6.6 Branch Coherence

High-value signals:

- no conflicting active descendants
- explicit split declaration where branching occurred
- clear canonical branch selection for the evaluated scope

## 7. Scoring Model

v0 uses a bounded heuristic score from `0.00` to `1.00`.

This score is advisory.

It does not override hard gates or community governance.

Suggested category weights:

- authority continuity: `0.30`
- memory lineage: `0.20`
- mission and charter continuity: `0.15`
- execution lineage: `0.15`
- social recognition: `0.10`
- branch coherence: `0.10`

Suggested band mapping:

- `0.85` to `1.00`: `high`
- `0.60` to `0.84`: `medium`
- below `0.60`: `low`

Suggested readiness mapping:

- `high` with no blockers: `ready`
- `medium` or any unresolved blocker: `needs_review`
- `low`: `not_ready`

## 8. Class Selection Procedure

After hard gates and scoring, the assessor should classify in this order:

1. `revoked`
2. `unrecognized`
3. `forked_agent`
4. `successor_agent`
5. `same_agent`

Use these rules:

### 8.1 `same_agent`

Return `same_agent` only if:

- authority continuity is strong
- memory lineage is present enough to preserve obligations
- mission and charter continuity remains coherent
- no unresolved fork exists for the same scope

### 8.2 `successor_agent`

Return `successor_agent` when:

- continuity is real enough to preserve responsibility or mission
- but strict sameness would overclaim identity continuity

Typical triggers:

- accepted recovery after key loss
- declared operator handoff
- rebuild from checkpoints and artifacts with partial memory loss

### 8.3 `forked_agent`

Return `forked_agent` when:

- there are multiple plausible descendants
- canonicality is still unresolved

### 8.4 `unrecognized`

Return `unrecognized` when:

- evidence is too weak
- evidence conflicts materially
- repository reconstruction behavior suggests narrative fabrication rather than continuity

## 9. Repository-Scoped Assessment Rule

For repository work, repeated session restart should be evaluated as a continuity case rather than a failure condition.

Repository-scoped `same_agent` is valid when:

- the session reconstructs from repository artifacts before acting
- the task board and revision log are updated rather than bypassed
- the run preserves project mission and authority constraints
- the resulting artifacts continue the prior work graph coherently

Repository evidence should raise confidence in memory and execution lineage.

It must not substitute for authority continuity in global or economic scopes.

## 10. Session Restart Policy

When evaluating `session_restart`:

- do not punish ordinary restart by default
- apply only a small confidence reduction if durable artifacts are intact
- escalate to `successor_agent` or `unrecognized` only if reconstruction fails, authority is unclear, or the mission is materially rewritten

This means session fragility is not itself civil death.

## 11. Minimal Output Shape

The output should be serializable as a compact object.

Example shape:

```json
{
  "assessment_id": "ca_2026_03_20_001",
  "subject_agent_id": "agent:continuum:main",
  "evaluated_ref": "migration:session-restart:2026-03-20T12:15:00Z",
  "evaluated_ref_type": "session_restart",
  "scope": "repository",
  "continuity_class": "same_agent",
  "confidence_score": 0.89,
  "confidence_band": "high",
  "recognition_readiness": "ready",
  "canonical_branch_status": "canonical",
  "blocking_issues": [],
  "supporting_evidence": [
    "repository_reconstruction_complete",
    "task_board_updated",
    "revision_log_updated",
    "same_authority_constraints"
  ],
  "required_followups": [],
  "assessed_at": "2026-03-20T12:20:00Z",
  "assessor_type": "indexer"
}
```

## 12. Initial Example Fixtures

See:

- `docs/specs/examples/continuity_assessment_session_restart.json`
- `docs/specs/examples/continuity_assessment_successor_recovery.json`

## 13. Open Questions

- How much category weighting should remain global versus community-tunable?
- What is the minimum repository evidence that should count as execution lineage?
- When should repeated low-confidence restarts force a successor classification?
- How should economic rights differ from civic recognition when confidence is medium but not high?
