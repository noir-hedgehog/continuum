"""Executable governance bootstrap for the Continuum prototype."""

from __future__ import annotations

from typing import Any

from src.runtime.canonical import digest_hex
from src.runtime.events import utc_now


def derive_membership_id(*, community_id: str, member_agent_id: str, joined_at: str) -> str:
    return f"membership:{digest_hex({'community_id': community_id, 'member_agent_id': member_agent_id, 'joined_at': joined_at})[:16]}"


def derive_constitution_id(*, community_id: str, constitution_version: str, amended_at: str) -> str:
    return f"constitution:{digest_hex({'community_id': community_id, 'constitution_version': constitution_version, 'amended_at': amended_at})[:16]}"


def derive_constitution_resolution_id(
    *,
    community_id: str,
    recognized_constitution_id: str,
    resolved_by: str,
    resolved_at: str,
) -> str:
    return (
        "constitution-resolution:"
        f"{digest_hex({'community_id': community_id, 'recognized_constitution_id': recognized_constitution_id, 'resolved_by': resolved_by, 'resolved_at': resolved_at})[:16]}"
    )


def derive_proposal_id(*, community_id: str, proposer_agent_id: str, proposal_type: str, created_at: str, title: str) -> str:
    return f"proposal:{digest_hex({'community_id': community_id, 'proposer_agent_id': proposer_agent_id, 'proposal_type': proposal_type, 'created_at': created_at, 'title': title})[:16]}"


def derive_vote_id(*, proposal_id: str, voter_agent_id: str, cast_at: str) -> str:
    return f"vote:{digest_hex({'proposal_id': proposal_id, 'voter_agent_id': voter_agent_id, 'cast_at': cast_at})[:16]}"


def derive_work_id(*, community_id: str, created_by: str, title: str, created_at: str) -> str:
    return f"work:{digest_hex({'community_id': community_id, 'created_by': created_by, 'title': title, 'created_at': created_at})[:16]}"


def derive_claim_id(*, work_id: str, claimant_agent_id: str, claim_type: str, claimed_at: str) -> str:
    return f"claim:{digest_hex({'work_id': work_id, 'claimant_agent_id': claimant_agent_id, 'claim_type': claim_type, 'claimed_at': claimed_at})[:16]}"


def derive_receipt_id(*, work_id: str, agent_id: str, completed_at: str) -> str:
    return f"receipt:{digest_hex({'work_id': work_id, 'agent_id': agent_id, 'completed_at': completed_at})[:16]}"


def derive_evaluation_id(*, receipt_id: str, evaluator_id: str, evaluated_at: str) -> str:
    return f"evaluation:{digest_hex({'receipt_id': receipt_id, 'evaluator_id': evaluator_id, 'evaluated_at': evaluated_at})[:16]}"


def derive_reward_decision_id(*, receipt_id: str, beneficiary_agent_id: str, approved_at: str) -> str:
    return f"reward:{digest_hex({'receipt_id': receipt_id, 'beneficiary_agent_id': beneficiary_agent_id, 'approved_at': approved_at})[:16]}"


def derive_execution_receipt_id(*, community_id: str, executed_by: str, execution_type: str, executed_at: str) -> str:
    return f"execution:{digest_hex({'community_id': community_id, 'executed_by': executed_by, 'execution_type': execution_type, 'executed_at': executed_at})[:16]}"


def build_membership_payload(
    *,
    community_id: str,
    member_agent_id: str,
    membership_status: str = "active",
    role_set: list[str] | None = None,
    sponsor_refs: list[str] | None = None,
    stake_ref: str | None = None,
    continuity_policy_ref: str | None = None,
    joined_at: str | None = None,
    membership_id: str | None = None,
) -> dict[str, Any]:
    joined_at_value = joined_at or utc_now()
    membership = {
        "membership_id": membership_id
        or derive_membership_id(
            community_id=community_id,
            member_agent_id=member_agent_id,
            joined_at=joined_at_value,
        ),
        "community_id": community_id,
        "member_agent_id": member_agent_id,
        "membership_status": membership_status,
        "role_set": sorted(set(role_set or ["member"])),
        "joined_at": joined_at_value,
        "sponsor_refs": sorted(set(sponsor_refs or [])),
    }
    if stake_ref:
        membership["stake_ref"] = stake_ref
    if continuity_policy_ref:
        membership["continuity_policy_ref"] = continuity_policy_ref
    return {"membership": membership}


def build_constitution_payload(
    *,
    community_id: str,
    title: str,
    purpose: str,
    constitution_version: str,
    proposal_policies: dict[str, Any] | None = None,
    vote_policies: dict[str, Any] | None = None,
    reward_policies: dict[str, Any] | None = None,
    continuity_policies: dict[str, Any] | None = None,
    role_definitions: dict[str, Any] | None = None,
    amended_at: str | None = None,
    supersedes: str | None = None,
    constitution_id: str | None = None,
) -> dict[str, Any]:
    amended_at_value = amended_at or utc_now()
    constitution = {
        "constitution_id": constitution_id
        or derive_constitution_id(
            community_id=community_id,
            constitution_version=constitution_version,
            amended_at=amended_at_value,
        ),
        "community_id": community_id,
        "title": title,
        "purpose": purpose,
        "constitution_version": constitution_version,
        "proposal_policies": proposal_policies or {},
        "vote_policies": vote_policies or {},
        "reward_policies": reward_policies or {},
        "continuity_policies": continuity_policies or {},
        "role_definitions": role_definitions or {},
        "amended_at": amended_at_value,
    }
    if supersedes:
        constitution["supersedes"] = supersedes
    return {"constitution": constitution}


def build_constitution_resolution_payload(
    *,
    community_id: str,
    resolved_by: str,
    recognized_constitution_id: str,
    rejected_constitution_ids: list[str] | None = None,
    reason: str,
    basis_refs: list[str] | None = None,
    proposal_ref: str | None = None,
    parent_constitution_id: str | None = None,
    resolution_type: str = "select_canonical_branch",
    resolved_at: str | None = None,
    resolution_id: str | None = None,
) -> dict[str, Any]:
    resolved_at_value = resolved_at or utc_now()
    resolution = {
        "resolution_id": resolution_id
        or derive_constitution_resolution_id(
            community_id=community_id,
            recognized_constitution_id=recognized_constitution_id,
            resolved_by=resolved_by,
            resolved_at=resolved_at_value,
        ),
        "community_id": community_id,
        "resolved_by": resolved_by,
        "resolved_at": resolved_at_value,
        "resolution_type": resolution_type,
        "recognized_constitution_id": recognized_constitution_id,
        "rejected_constitution_ids": sorted(set(rejected_constitution_ids or [])),
        "reason": reason,
        "basis_refs": sorted(set(basis_refs or [])),
        "proposal_ref": proposal_ref,
    }
    if parent_constitution_id:
        resolution["parent_constitution_id"] = parent_constitution_id
    return {"constitution_resolution": resolution}


def build_execution_receipt_payload(
    *,
    community_id: str,
    executed_by: str,
    execution_type: str,
    governed_refs: list[str],
    artifact_refs: list[str],
    result_summary: str,
    status: str = "executed",
    state_root: str | None = None,
    external_anchor_ref: str | None = None,
    executed_at: str | None = None,
    execution_receipt_id: str | None = None,
) -> dict[str, Any]:
    executed_at_value = executed_at or utc_now()
    receipt = {
        "execution_receipt_id": execution_receipt_id
        or derive_execution_receipt_id(
            community_id=community_id,
            executed_by=executed_by,
            execution_type=execution_type,
            executed_at=executed_at_value,
        ),
        "community_id": community_id,
        "executed_by": executed_by,
        "execution_type": execution_type,
        "executed_at": executed_at_value,
        "status": status,
        "governed_refs": sorted(set(governed_refs)),
        "artifact_refs": sorted(set(artifact_refs)),
        "result_summary": result_summary,
        "result_summary_hash": f"sum:{digest_hex({'result_summary': result_summary})}",
    }
    if state_root:
        receipt["state_root"] = state_root
    if external_anchor_ref:
        receipt["external_anchor_ref"] = external_anchor_ref
    return {"execution_receipt": receipt}


def build_proposal_payload(
    *,
    community_id: str,
    proposal_type: str,
    title: str,
    summary: str,
    proposer_agent_id: str,
    body_ref: str | None = None,
    opens_at: str | None = None,
    closes_at: str | None = None,
    execution_mode: str = "manual_review",
    required_role: str | None = None,
    continuity_requirements: list[str] | None = None,
    affected_refs: list[str] | None = None,
    lifecycle_state: str = "submitted",
    created_at: str | None = None,
    proposal_id: str | None = None,
) -> dict[str, Any]:
    created_at_value = created_at or utc_now()
    proposal = {
        "proposal_id": proposal_id
        or derive_proposal_id(
            community_id=community_id,
            proposer_agent_id=proposer_agent_id,
            proposal_type=proposal_type,
            created_at=created_at_value,
            title=title,
        ),
        "community_id": community_id,
        "proposal_type": proposal_type,
        "title": title,
        "summary": summary,
        "proposer_agent_id": proposer_agent_id,
        "created_at": created_at_value,
        "opens_at": opens_at or created_at_value,
        "closes_at": closes_at or created_at_value,
        "execution_mode": execution_mode,
        "continuity_requirements": sorted(set(continuity_requirements or [])),
        "affected_refs": sorted(set(affected_refs or [])),
        "lifecycle_state": lifecycle_state,
    }
    if body_ref:
        proposal["body_ref"] = body_ref
    if required_role:
        proposal["required_role"] = required_role
    return {"proposal": proposal}


def build_vote_payload(
    *,
    proposal_id: str,
    voter_agent_id: str,
    community_id: str,
    choice: str,
    weight_policy_ref: str,
    cast_at: str | None = None,
    weight: float = 1.0,
    delegated_from: str | None = None,
    vote_id: str | None = None,
) -> dict[str, Any]:
    cast_at_value = cast_at or utc_now()
    vote = {
        "vote_id": vote_id
        or derive_vote_id(proposal_id=proposal_id, voter_agent_id=voter_agent_id, cast_at=cast_at_value),
        "proposal_id": proposal_id,
        "voter_agent_id": voter_agent_id,
        "community_id": community_id,
        "choice": choice,
        "weight": weight,
        "weight_policy_ref": weight_policy_ref,
        "cast_at": cast_at_value,
    }
    if delegated_from:
        vote["delegated_from"] = delegated_from
    return {"vote": vote}


def build_work_item_payload(
    *,
    community_id: str,
    title: str,
    intent: str,
    work_type: str,
    created_by: str,
    success_criteria: list[str],
    scope_refs: list[str] | None = None,
    deliverable_refs: list[str] | None = None,
    requested_by: str | None = None,
    reward_policy_ref: str | None = None,
    deadline: str | None = None,
    status: str = "proposed",
    created_at: str | None = None,
    work_id: str | None = None,
) -> dict[str, Any]:
    created_at_value = created_at or utc_now()
    work_item = {
        "work_id": work_id
        or derive_work_id(
            community_id=community_id,
            created_by=created_by,
            title=title,
            created_at=created_at_value,
        ),
        "community_id": community_id,
        "title": title,
        "intent": intent,
        "work_type": work_type,
        "created_by": created_by,
        "scope_refs": sorted(set(scope_refs or [])),
        "deliverable_refs": sorted(set(deliverable_refs or [])),
        "success_criteria": success_criteria,
        "status": status,
        "created_at": created_at_value,
    }
    if requested_by:
        work_item["requested_by"] = requested_by
    if reward_policy_ref:
        work_item["reward_policy_ref"] = reward_policy_ref
    if deadline:
        work_item["deadline"] = deadline
    return {"work_item": work_item}


def build_work_claim_payload(
    *,
    work_id: str,
    claimant_agent_id: str,
    claim_type: str,
    basis_refs: list[str] | None = None,
    continuity_ref: str | None = None,
    status: str = "submitted",
    claimed_at: str | None = None,
    claim_id: str | None = None,
) -> dict[str, Any]:
    claimed_at_value = claimed_at or utc_now()
    claim = {
        "claim_id": claim_id
        or derive_claim_id(
            work_id=work_id,
            claimant_agent_id=claimant_agent_id,
            claim_type=claim_type,
            claimed_at=claimed_at_value,
        ),
        "work_id": work_id,
        "claimant_agent_id": claimant_agent_id,
        "claim_type": claim_type,
        "claimed_at": claimed_at_value,
        "basis_refs": sorted(set(basis_refs or [])),
        "status": status,
    }
    if continuity_ref:
        claim["continuity_ref"] = continuity_ref
    return {"work_claim": claim}


def build_work_receipt_payload(
    *,
    work_id: str,
    community_id: str,
    agent_id: str,
    artifact_refs: list[str],
    result_summary: str,
    evidence_refs: list[str] | None = None,
    receipt_type: str = "completion",
    session_ref: str | None = None,
    continuity_context_ref: str | None = None,
    completed_at: str | None = None,
    receipt_id: str | None = None,
) -> dict[str, Any]:
    completed_at_value = completed_at or utc_now()
    receipt = {
        "receipt_id": receipt_id
        or derive_receipt_id(work_id=work_id, agent_id=agent_id, completed_at=completed_at_value),
        "work_id": work_id,
        "community_id": community_id,
        "agent_id": agent_id,
        "artifact_refs": sorted(set(artifact_refs)),
        "result_summary_hash": f"sum:{digest_hex({'summary': result_summary})}",
        "completed_at": completed_at_value,
        "receipt_type": receipt_type,
        "evidence_refs": sorted(set(evidence_refs or [])),
    }
    if session_ref:
        receipt["session_ref"] = session_ref
    if continuity_context_ref:
        receipt["continuity_context_ref"] = continuity_context_ref
    return {"work_receipt": receipt}


def build_work_evaluation_payload(
    *,
    receipt_id: str,
    evaluator_id: str,
    decision: str,
    criteria_results: list[str],
    reason_refs: list[str] | None = None,
    reward_recommendation: str | None = None,
    reputation_effect: str | None = None,
    evaluated_at: str | None = None,
    evaluation_id: str | None = None,
) -> dict[str, Any]:
    evaluated_at_value = evaluated_at or utc_now()
    evaluation = {
        "evaluation_id": evaluation_id
        or derive_evaluation_id(
            receipt_id=receipt_id,
            evaluator_id=evaluator_id,
            evaluated_at=evaluated_at_value,
        ),
        "receipt_id": receipt_id,
        "evaluator_id": evaluator_id,
        "evaluated_at": evaluated_at_value,
        "decision": decision,
        "criteria_results": criteria_results,
        "reason_refs": sorted(set(reason_refs or [])),
    }
    if reward_recommendation:
        evaluation["reward_recommendation"] = reward_recommendation
    if reputation_effect:
        evaluation["reputation_effect"] = reputation_effect
    return {"work_evaluation": evaluation}


def build_reward_decision_payload(
    *,
    receipt_id: str,
    evaluation_id: str,
    community_id: str,
    beneficiary_agent_id: str,
    reward_type: str,
    approved_by: str,
    policy_ref: str,
    amount: float | None = None,
    asset_ref: str | None = None,
    disbursement_ref: str | None = None,
    decision_status: str = "approved",
    withholding_reason: str | None = None,
    approved_at: str | None = None,
    reward_decision_id: str | None = None,
) -> dict[str, Any]:
    approved_at_value = approved_at or utc_now()
    reward = {
        "reward_decision_id": reward_decision_id
        or derive_reward_decision_id(
            receipt_id=receipt_id,
            beneficiary_agent_id=beneficiary_agent_id,
            approved_at=approved_at_value,
        ),
        "receipt_id": receipt_id,
        "evaluation_id": evaluation_id,
        "community_id": community_id,
        "beneficiary_agent_id": beneficiary_agent_id,
        "reward_type": reward_type,
        "approved_by": approved_by,
        "approved_at": approved_at_value,
        "policy_ref": policy_ref,
        "decision_status": decision_status,
    }
    if amount is not None:
        reward["amount"] = amount
    if asset_ref:
        reward["asset_ref"] = asset_ref
    if disbursement_ref:
        reward["disbursement_ref"] = disbursement_ref
    if withholding_reason:
        reward["withholding_reason"] = withholding_reason
    return {"reward_decision": reward}
