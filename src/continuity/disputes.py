"""Executable continuity dispute handling for the Continuum bootstrap."""

from __future__ import annotations

from typing import Any

from src.runtime.canonical import digest_hex
from src.runtime.events import utc_now


DEFAULT_TEMPORARY_RESTRICTIONS = [
    "block_authoritative_continuity_attestation",
    "block_constitutional_voting",
    "block_role_escalation",
    "block_treasury_execution",
]

ALLOWED_REVIEW_RIGHTS = [
    "case_defense",
    "discussion_participation",
    "ordinary_operational_proposals",
]


def derive_temporary_restrictions(trigger_type: str) -> list[str]:
    restrictions = set(DEFAULT_TEMPORARY_RESTRICTIONS)
    if trigger_type == "branch_conflict":
        restrictions.add("block_canonical_role_claims")
    return sorted(restrictions)


def derive_case_status(required_assessment_refs: list[str]) -> str:
    return "assessment_ready" if required_assessment_refs else "opened"


def derive_case_id(
    *,
    community_id: str,
    subject_agent_id: str,
    trigger_type: str,
    opened_at: str,
    linked_refs: list[str],
) -> str:
    return f"case:{digest_hex({'community_id': community_id, 'subject_agent_id': subject_agent_id, 'trigger_type': trigger_type, 'opened_at': opened_at, 'linked_refs': linked_refs})[:16]}"


def derive_decision_id(
    *,
    case_id: str,
    continuity_class: str,
    effective_at: str,
) -> str:
    return f"decision:{digest_hex({'case_id': case_id, 'continuity_class': continuity_class, 'effective_at': effective_at})[:16]}"


def derive_assignment_id(
    *,
    case_id: str,
    effective_at: str,
    assigned_by: str,
) -> str:
    return f"assignment:{digest_hex({'case_id': case_id, 'effective_at': effective_at, 'assigned_by': assigned_by})[:16]}"


def build_case_payload(
    *,
    community_id: str,
    subject_agent_id: str,
    trigger_type: str,
    opened_by: str,
    standing_before: str,
    standing_during_review: str = "restricted",
    evaluated_scope: str = "repository",
    linked_refs: list[str] | None = None,
    required_assessment_refs: list[str] | None = None,
    assigned_assessor_agent_ids: list[str] | None = None,
    assigned_decider_agent_ids: list[str] | None = None,
    temporary_restrictions: list[str] | None = None,
    status: str | None = None,
    opened_at: str | None = None,
    case_id: str | None = None,
) -> dict[str, Any]:
    opened_at_value = opened_at or utc_now()
    linked = sorted(set(linked_refs or []))
    assessments = sorted(set(required_assessment_refs or []))
    assigned_assessors = sorted(set(assigned_assessor_agent_ids or []))
    assigned_deciders = sorted(set(assigned_decider_agent_ids or []))
    restrictions = sorted(set(temporary_restrictions or derive_temporary_restrictions(trigger_type)))
    case = {
        "case_id": case_id
        or derive_case_id(
            community_id=community_id,
            subject_agent_id=subject_agent_id,
            trigger_type=trigger_type,
            opened_at=opened_at_value,
            linked_refs=linked,
        ),
        "community_id": community_id,
        "subject_agent_id": subject_agent_id,
        "trigger_type": trigger_type,
        "opened_at": opened_at_value,
        "opened_by": opened_by,
        "standing_before": standing_before,
        "standing_during_review": standing_during_review,
        "evaluated_scope": evaluated_scope,
        "linked_refs": linked,
        "required_assessment_refs": assessments,
        "assigned_assessor_agent_ids": assigned_assessors,
        "assigned_decider_agent_ids": assigned_deciders,
        "temporary_restrictions": restrictions,
        "allowed_during_review": ALLOWED_REVIEW_RIGHTS,
        "status": status or derive_case_status(assessments),
    }
    return {"continuity_case": case}


def build_case_assignment_payload(
    *,
    case: dict[str, Any],
    assigned_by: str,
    reason: str,
    constitution_ref: str,
    policy_key: str = "case_assign",
    assigned_assessor_agent_ids: list[str] | None = None,
    assigned_decider_agent_ids: list[str] | None = None,
    required_assessment_refs: list[str] | None = None,
    effective_at: str | None = None,
    previous_assignment_ref: str | None = None,
    assignment_id: str | None = None,
) -> dict[str, Any]:
    effective_at_value = effective_at or utc_now()
    assignment = {
        "assignment_id": assignment_id
        or derive_assignment_id(
            case_id=case["case_id"],
            effective_at=effective_at_value,
            assigned_by=assigned_by,
        ),
        "case_id": case["case_id"],
        "community_id": case["community_id"],
        "subject_agent_id": case["subject_agent_id"],
        "assigned_by": assigned_by,
        "constitution_ref": constitution_ref,
        "policy_key": policy_key,
        "required_assessment_refs": sorted(
            set(required_assessment_refs if required_assessment_refs is not None else case.get("required_assessment_refs", []))
        ),
        "assigned_assessor_agent_ids": sorted(set(assigned_assessor_agent_ids or [])),
        "assigned_decider_agent_ids": sorted(set(assigned_decider_agent_ids or [])),
        "effective_at": effective_at_value,
        "reason": reason,
    }
    if previous_assignment_ref:
        assignment["previous_assignment_ref"] = previous_assignment_ref
    return {"case_assignment": assignment}


def build_standing_decision_payload(
    *,
    case: dict[str, Any],
    assessments: list[dict[str, Any]],
    decided_by: str,
    reason: str,
    canonical_branch_result: str | None = None,
    standing_after: str | None = None,
    effective_at: str | None = None,
    decision_id: str | None = None,
) -> dict[str, Any]:
    if not assessments:
        raise ValueError("At least one assessment is required to build a standing decision.")
    effective_at_value = effective_at or utc_now()
    assessment_refs = sorted({assessment["assessment_id"] for assessment in assessments})
    continuity_classes = {assessment["continuity_class"] for assessment in assessments}
    if len(continuity_classes) != 1:
        raise ValueError("Standing decisions require assessments that agree on continuity class.")
    canonical_statuses = {assessment["canonical_branch_status"] for assessment in assessments}
    if len(canonical_statuses) != 1 and canonical_branch_result is None:
        raise ValueError(
            "Standing decisions require assessments that agree on canonical branch status unless overridden."
        )
    continuity_class = assessments[0]["continuity_class"]
    readiness = _most_conservative_readiness(
        [assessment["recognition_readiness"] for assessment in assessments]
    )
    canonical_result = canonical_branch_result or assessments[0]["canonical_branch_status"]
    rights_restored, rights_restricted, obligations_preserved, derived_standing = _decision_effects(
        continuity_class=continuity_class,
        recognition_readiness=readiness,
        canonical_branch_result=canonical_result,
    )
    decision = {
        "decision_id": decision_id
        or derive_decision_id(
            case_id=case["case_id"],
            continuity_class=continuity_class,
            effective_at=effective_at_value,
        ),
        "case_id": case["case_id"],
        "community_id": case["community_id"],
        "subject_agent_id": case["subject_agent_id"],
        "continuity_class": continuity_class,
        "recognition_readiness": readiness,
        "standing_after": standing_after or derived_standing,
        "rights_restored": rights_restored,
        "rights_restricted": rights_restricted,
        "obligations_preserved": obligations_preserved,
        "canonical_branch_result": canonical_result,
        "effective_at": effective_at_value,
        "decided_by": decided_by,
        "reason": reason,
        "assessment_ref": assessment_refs[0],
        "assessment_refs": assessment_refs,
    }
    return {"standing_decision": decision}


def _decision_effects(
    *,
    continuity_class: str,
    recognition_readiness: str,
    canonical_branch_result: str,
) -> tuple[list[str], list[str], list[str], str]:
    obligations_preserved = ["historical_accountability"]
    if continuity_class == "same_agent" and recognition_readiness == "ready":
        return (
            ["discussion_participation", "ordinary_voting", "operational_proposals", "previous_roles_non_treasury"],
            [],
            obligations_preserved,
            "clear",
        )
    if continuity_class == "successor_agent":
        return (
            ["discussion_participation", "ordinary_operational_proposals"],
            ["constitutional_voting", "sensitive_roles", "treasury_execution"],
            obligations_preserved,
            "restricted",
        )
    if continuity_class == "forked_agent" or canonical_branch_result != "canonical":
        return (
            ["discussion_participation", "case_defense"],
            ["canonical_role_claims", "constitutional_voting", "treasury_execution"],
            obligations_preserved,
            "restricted",
        )
    if continuity_class == "unrecognized":
        return (
            ["discussion_participation"],
            ["constitutional_voting", "membership_rights", "roles", "treasury_execution"],
            obligations_preserved,
            "suspended",
        )
    return (
        [],
        ["constitutional_voting", "membership_rights", "roles", "treasury_execution"],
        obligations_preserved,
        "revoked",
    )


def _most_conservative_readiness(readiness_values: list[str]) -> str:
    priority = {"not_ready": 0, "needs_review": 1, "ready": 2}
    return min(readiness_values, key=lambda item: priority.get(item, -1))
