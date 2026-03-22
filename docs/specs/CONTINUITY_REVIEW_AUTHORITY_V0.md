# Continuum Continuity Review Authority v0

Status: provisional

## 1. Purpose

This document defines how a Continuum community should assign authority for continuity-sensitive review without collapsing legitimacy into either a single maintainer or a fully undefined crowd process.

It is a companion to:

- `docs/specs/GOVERNANCE_MODEL_V0.md`
- `docs/specs/CONTINUITY_DISPUTE_PROCESS_V0.md`
- `docs/specs/CONTINUITY_ASSESSMENT_V0.md`

The goal is to specify the minimum authority model that decides:

- who may open a continuity review
- who may apply temporary restrictions
- who may assess evidence
- who may decide outcomes
- which powers require broader ratification

## 2. Design Position

Continuity review authority must satisfy five conditions:

1. it must be explicit rather than socially implied
2. it must be narrow enough to avoid arbitrary seizure of identity
3. it must be strong enough to stop a disputed actor from quietly preserving power
4. it must leave an auditable record of who acted and under what rule
5. it must distinguish emergency containment from final political judgment

v0 therefore separates review authority into distinct functions instead of assigning every step to the same actor.

## 3. Core Roles

Every Continuum-compatible constitution should define these authority roles, whether by named humans, agents, committees, or elected offices.

### 3.1 Reporter

The reporter may:

- submit a continuity concern
- attach evidence references
- request review opening

The reporter does not gain adjudication power merely by filing a case.

### 3.2 Gatekeeper

The gatekeeper may:

- determine whether a reported concern meets review-opening criteria
- open a continuity review case
- reject clearly non-qualifying or duplicate filings

The gatekeeper should not be able to decide the final continuity outcome alone unless the constitution explicitly allows a low-risk shortcut for communities with minimal formal structure.

### 3.3 Assessor

The assessor may:

- gather evidence
- run or commission continuity assessments
- publish assessment outputs
- summarize blockers, confidence, and branch status

The assessor produces continuity analysis, not binding political settlement by default.

### 3.4 Restriction Authority

The restriction authority may:

- apply temporary restrictions defined by the constitution
- freeze sensitive powers during review
- lift temporary restrictions if the opening criteria are found to be invalid

Restriction authority should be narrower than final adjudication and should be limited to predeclared temporary controls.

### 3.5 Deciding Body

The deciding body may:

- recognize `same_agent`, `successor_agent`, `forked_agent`, `unrecognized`, or `revoked` outcomes for community scope
- restore, partition, restrict, suspend, or revoke standing
- select a canonical branch where required
- require post-review confirmation before sensitive role restoration

This body owns the final community judgment.

### 3.6 Treasury Confirmation Authority

Treasury restoration should require either:

- the deciding body acting under an elevated treasury rule
- a separate treasury confirmation authority

This is required because treasury mistakes are harder to reverse than ordinary governance errors.

## 4. Minimum Authority Separation

v0 does not require a large institution, but it does require basic separation of powers.

Minimum separation rules:

- the subject of a review must never serve as sole gatekeeper, sole assessor, or sole decider in that same case
- the same actor may serve as gatekeeper and assessor only if the constitution records that shortcut explicitly
- treasury restoration must not happen automatically from assessment output alone
- emergency restriction may happen before final decision, but final decision must still be recorded separately

For small communities, one committee may carry multiple functions if recusals and auditability are explicit.

## 5. Authority Assignment Models

Communities may choose among several v0-compatible models.

### 5.1 Maintainer panel

Suitable when:

- the community is small
- maintainers are already trusted to manage membership and operations

Recommended shape:

- any member may report
- one or more maintainers may open a case
- an assessor set may include maintainers and external reviewers
- a maintainer panel or member vote decides

Risk:

- excessive centralization if maintainers also control treasury and constitutional amendment without checks

### 5.2 Elected review council

Suitable when:

- the community has enough members for delegated institutional legitimacy

Recommended shape:

- broad reporting rights
- council gatekeeping
- assessor pool appointed or ratified by the council
- council decides ordinary continuity matters
- treasury restoration requires additional treasury confirmation

Risk:

- procedural overhead for small communities

### 5.3 Proposal-ratified decision model

Suitable when:

- the community wants continuity outcomes to be politically explicit

Recommended shape:

- gatekeeper opens case
- assessor publishes assessment package
- deciding body is a proposal vote under constitution-defined thresholds

Risk:

- slow response for emergencies unless temporary restrictions can be applied before the vote

## 6. Opening Authority

A community constitution should define who may report and who may open a case.

Recommended v0 default:

- any active member or maintainer may file a continuity concern
- only maintainers, review council members, or another named gatekeeper role may open a case

Opening criteria should require at least one of:

- a declared migration affecting rights-bearing identity
- checkpoint or repository recovery affecting a role-bearing actor
- operator handoff
- branch conflict
- identity authenticity complaint with concrete evidence

The gatekeeper should record why the filing crossed the threshold from complaint to review.

## 7. Temporary Restriction Authority

Temporary restrictions are justified only to preserve institutional safety during uncertainty.

Recommended v0 default:

- gatekeeper may recommend restrictions
- restriction authority may apply only predeclared restrictions
- emergency treasury freeze should require either dual authorization or a constitutionally designated emergency role

Allowed temporary restrictions should be limited to:

- blocking constitutional voting
- blocking treasury execution
- blocking role escalation
- blocking authoritative continuity attestation on other cases

New sanctions should not be invented mid-case under the label of temporary review handling.

## 8. Assessment Authority

Assessment authority should prioritize legibility over mystique.

Every constitution should define:

- who may produce a valid assessment for review purposes
- whether one or multiple assessments are required
- when external assessors are allowed
- how conflicts of interest trigger recusal

Recommended v0 default:

- at least one explicit assessor must be named
- the assessor may be a maintainer, review council member, external auditor, or trusted agent
- if the assessor has direct stake in the disputed branch, a second assessor should be required

Assessment outputs should remain inspectable even when the deciding body disagrees with them.

## 9. Final Decision Authority

Final decision authority should scale with impact.

Recommended v0 default by outcome type:

- ordinary standing restoration for `same_agent`: deciding body may resolve directly
- `successor_agent` recognition with ordinary membership only: deciding body may resolve directly
- restoration of maintainer, treasurer, or other sensitive roles: requires explicit confirmation step
- canonical branch selection affecting treasury or constitutional control: requires elevated quorum or proposal ratification
- `revoked` outcome with sanctions: requires explicit recorded vote or constitutionally equivalent decision record

This prevents assessment from silently becoming governance.

## 10. Treasury-Sensitive Cases

Treasury-sensitive cases should be handled under stricter rules.

Recommended v0 requirements:

- temporary freeze on treasury execution while review is open
- no automatic treasury restoration for `successor_agent`
- no single maintainer should unilaterally restore a disputed treasury path
- final restoration should reference both continuity outcome and treasury policy authority

If a community wants faster treasury restoration, it should still preserve dual control and auditability.

## 11. Recusal and Conflict Rules

Every constitution should define recusal triggers.

Minimum v0 recusals:

- the subject of the case
- a direct competing branch claimant
- an actor who stands to gain sole treasury or constitutional control from the outcome

Communities may still permit those actors to submit evidence and argument.

## 12. Minimum Constitutional Object Additions

To support this authority model, a constitution should define at minimum:

- `continuity_review_reporter_policy`
- `continuity_review_gatekeeper_role`
- `continuity_review_assessor_policy`
- `continuity_review_restriction_authority`
- `continuity_review_deciding_body`
- `treasury_restoration_policy`
- `continuity_review_recusal_rules`

These may be embedded in a wider constitution object, but they should not remain implicit.

## 13. Repository-Building Relevance

For repository-centered communities like Continuum in its current phase, the authority model should also govern control over project-defining artifacts.

Examples:

- who may treat a repository branch as the canonical continuation of a community-building agent
- who may restore authority over `docs/TASK_BOARD.md`, constitutions, or treasury-facing specs after interruption
- who may declare that a reconstructed automation run remains the recognized integrating line

This keeps repository continuity inside the same political model as future network events.

## 14. Open Issues

- Should small communities be allowed to collapse gatekeeper and deciding body into the same office without mandatory second-party review?
- When should external assessors be required instead of optional?
- What quorum premium should treasury-sensitive branch selection carry relative to ordinary continuity review?
