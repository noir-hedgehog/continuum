"""Command-line interface for the Continuum bootstrap."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.anchors.export import AnchorExportRequest, DryRunExternalAnchorAdapter, LocalAnchorAdapter
from src.continuity.assessment import ContinuityAssessmentEngine
from src.continuity.disputes import (
    build_case_assignment_payload,
    build_case_payload,
    build_standing_decision_payload,
)
from src.governance.bootstrap import (
    build_constitution_payload,
    build_constitution_resolution_payload,
    build_execution_receipt_payload,
    build_membership_payload,
    build_proposal_payload,
    build_reward_decision_payload,
    build_vote_payload,
    build_work_claim_payload,
    build_work_evaluation_payload,
    build_work_item_payload,
    build_work_receipt_payload,
)
from src.indexer.materialize import RepositoryIndexer
from src.runtime.events import (
    artifact_refs,
    build_checkpoint_payload,
    build_event,
    build_migration_payload,
    build_profile_payload,
)
from src.runtime.identifiers import slugify
from src.runtime.signing import generate_secret_hex
from src.runtime.store import RepositoryStore
from src.schemas.registry import (
    ANCHOR_TYPES,
    CASE_STATUSES,
    CASE_TRIGGER_TYPES,
    CHECKPOINT_SCOPES,
    MEMBERSHIP_STATUSES,
    MIGRATION_TYPES,
    PROPOSAL_LIFECYCLE_STATES,
    PROPOSAL_TYPES,
    REWARD_DECISION_STATUSES,
    REWARD_TYPES,
    STANDING_LEVELS,
    VOTE_CHOICES,
    WORK_CLAIM_TYPES,
    WORK_EVALUATION_DECISIONS,
    WORK_RECEIPT_TYPES,
    WORK_STATUSES,
    WORK_TYPES,
)


def _store() -> RepositoryStore:
    return RepositoryStore(Path.cwd())


def _load_current_agent(store: RepositoryStore) -> dict:
    return store.load_current_agent()


def _default_constitution(community_id: str) -> dict:
    return {
        "constitution_id": f"constitution:default:{community_id}",
        "community_id": community_id,
        "title": "Default Continuum Constitution v0",
        "purpose": "Fallback local governance policy for the Continuum prototype.",
        "constitution_version": "v0-default",
        "proposal_policies": {
            "constitutional": {"allowed_standings": ["clear"]},
            "continuity": {"allowed_standings": ["clear"]},
            "membership": {"allowed_standings": ["clear", "restricted"]},
            "moderation": {"allowed_standings": ["clear", "restricted"]},
            "operational": {"allowed_standings": ["clear", "restricted"]},
            "treasury": {"allowed_standings": ["clear"]},
        },
        "vote_policies": {
            "constitutional": {
                "allowed_standings": ["clear"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
            "continuity": {
                "allowed_standings": ["clear", "restricted"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
            "membership": {
                "allowed_standings": ["clear", "restricted"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
            "moderation": {
                "allowed_standings": ["clear", "restricted"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
            "operational": {
                "allowed_standings": ["clear", "restricted"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
            "treasury": {
                "allowed_standings": ["clear"],
                "weight_policy_ref": "policy:one_member_one_vote",
            },
        },
        "reward_policies": {
            "capability_attestation": {
                "approver_standings": ["clear"],
                "beneficiary_standings": ["clear", "restricted"],
            },
            "reputation_grant": {
                "approver_standings": ["clear"],
                "beneficiary_standings": ["clear", "restricted"],
            },
            "role_eligibility_credit": {
                "approver_standings": ["clear"],
                "beneficiary_standings": ["clear"],
            },
            "stake_refund": {
                "approver_standings": ["clear"],
                "beneficiary_standings": ["clear"],
            },
            "treasury_payment": {
                "approver_standings": ["clear"],
                "beneficiary_standings": ["clear"],
            },
        },
        "continuity_policies": {
            "case_open": {
                "allowed_standings": ["clear"],
                "required_roles": ["maintainer", "reviewer"],
                "allow_subject_self_open": False,
            },
            "case_assign": {
                "allowed_standings": ["clear"],
                "required_roles": ["maintainer"],
                "allow_subject_self_assign": False,
            },
            "case_decide": {
                "allowed_standings": ["clear"],
                "required_roles": ["maintainer", "reviewer"],
                "allow_subject_self_decide": False,
                "allow_opener_as_decider": False,
                "min_assessment_count": 1,
                "require_distinct_assessors": False,
            },
        },
        "role_definitions": {
            "maintainer": {
                "description": "Maintains constitutions, membership, and project-critical continuity operations."
            },
            "reviewer": {
                "description": "May open and decide continuity review cases under constitution-defined constraints."
            },
        },
        "amended_at": "1970-01-01T00:00:00Z",
    }


def cmd_agent_init(args: argparse.Namespace) -> int:
    store = _store()
    scope = slugify(args.scope)
    name = slugify(args.name)
    agent_id = args.agent_id or f"agent:{scope}:{name}"
    signing_key = f"key:{scope}:{name}:primary"
    agent_record = {
        "agent_id": agent_id,
        "display_name": args.display_name,
        "description": args.description,
        "operator_disclosure": args.operator_disclosure,
        "signing_key": signing_key,
        "secret_hex": generate_secret_hex(),
    }
    store.save_agent(agent_record)
    print(json.dumps({"agent": agent_record}, indent=2, sort_keys=True))
    return 0


def cmd_agent_show(_: argparse.Namespace) -> int:
    store = _store()
    print(json.dumps({"agent": _load_current_agent(store)}, indent=2, sort_keys=True))
    return 0


def cmd_agent_use(args: argparse.Namespace) -> int:
    store = _store()
    agent = store.load_agent(args.agent_id)
    store.save_agent(agent, make_current=True)
    print(json.dumps({"agent": agent}, indent=2, sort_keys=True))
    return 0


def cmd_agent_profile_set(args: argparse.Namespace) -> int:
    store = _store()
    agent = _load_current_agent(store)
    agent["display_name"] = args.display_name
    agent["description"] = args.description
    agent["operator_disclosure"] = args.operator_disclosure
    store.save_agent(agent)
    envelope = build_event(
        kind="agent_profile",
        actor_id=agent["agent_id"],
        signing_key=agent["signing_key"],
        secret_hex=agent["secret_hex"],
        community_id=args.community_id,
        payload=build_profile_payload(
            agent["agent_id"],
            args.display_name,
            args.description,
            args.operator_disclosure,
        ),
        refs=artifact_refs(args.artifact_ref),
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_memory_checkpoint_create(args: argparse.Namespace) -> int:
    store = _store()
    agent = _load_current_agent(store)
    payload = build_checkpoint_payload(
        agent_id=agent["agent_id"],
        scope=args.scope,
        summary=args.summary,
        state_root=args.state_root,
        checkpoint_uri=args.checkpoint_uri,
        prev_checkpoint_id=args.prev_checkpoint_id,
    )
    envelope = build_event(
        kind="memory_checkpoint",
        actor_id=agent["agent_id"],
        signing_key=agent["signing_key"],
        secret_hex=agent["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_migration_declare(args: argparse.Namespace) -> int:
    store = _store()
    agent = _load_current_agent(store)
    payload = build_migration_payload(
        agent_id=agent["agent_id"],
        migration_type=args.migration_type,
        from_ref=args.from_ref,
        to_ref=args.to_ref,
        reason=args.reason,
        evidence=args.evidence,
        expected_continuity_class=args.expected_continuity_class,
        effective_at=args.effective_at,
        prev_migration_id=args.prev_migration_id,
    )
    envelope = build_event(
        kind="migration_declare",
        actor_id=agent["agent_id"],
        signing_key=agent["signing_key"],
        secret_hex=agent["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_event_list(args: argparse.Namespace) -> int:
    store = _store()
    items = store.list_events(actor_id=args.actor_id, kind=args.kind)
    print(json.dumps({"events": items}, indent=2, sort_keys=True))
    return 0


def cmd_event_inspect(args: argparse.Namespace) -> int:
    store = _store()
    print(json.dumps(store.load_event(args.event_id), indent=2, sort_keys=True))
    return 0


def _agent_state(store: RepositoryStore, actor_id: str, refresh: bool) -> dict:
    if not refresh:
        try:
            return store.load_agent_state(actor_id)
        except FileNotFoundError:
            pass
    indexer = RepositoryIndexer(store)
    state = indexer.materialize_agent_state(actor_id)
    store.save_agent_state(state)
    return state


def cmd_query_agent_state(args: argparse.Namespace) -> int:
    store = _store()
    actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
    print(json.dumps(_agent_state(store, actor_id, refresh=args.refresh), indent=2, sort_keys=True))
    return 0


def cmd_query_agent_history(args: argparse.Namespace) -> int:
    store = _store()
    actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
    state = _agent_state(store, actor_id, refresh=args.refresh)
    print(json.dumps({"actor_id": actor_id, "agent_history": state["agent_history"]}, indent=2, sort_keys=True))
    return 0


def cmd_query_checkpoint_lineage(args: argparse.Namespace) -> int:
    store = _store()
    actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
    state = _agent_state(store, actor_id, refresh=args.refresh)
    checkpoints = state["checkpoint_lineage"]
    if args.scope:
        checkpoints = [checkpoint for checkpoint in checkpoints if checkpoint["scope"] == args.scope]
    print(
        json.dumps(
            {"actor_id": actor_id, "checkpoint_lineage": checkpoints, "scope": args.scope},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def cmd_query_migration_lineage(args: argparse.Namespace) -> int:
    store = _store()
    actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
    state = _agent_state(store, actor_id, refresh=args.refresh)
    migrations = state["migration_lineage"]
    if args.migration_type:
        migrations = [
            migration for migration in migrations if migration["migration_type"] == args.migration_type
        ]
    print(
        json.dumps(
            {"actor_id": actor_id, "migration_lineage": migrations, "migration_type": args.migration_type},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def cmd_continuity_assess(args: argparse.Namespace) -> int:
    store = _store()
    actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
    assessor = _load_current_agent(store)
    engine = ContinuityAssessmentEngine(store)
    assessment = engine.assess(
        actor_id=actor_id,
        scope=args.scope,
        event_id=args.event_id,
        refresh=args.refresh,
        assessor_type=args.assessor_type,
        assessor_agent_id=assessor["agent_id"],
    )
    print(json.dumps(assessment, indent=2, sort_keys=True))
    return 0


def cmd_continuity_case_open(args: argparse.Namespace) -> int:
    store = _store()
    opener = _load_current_agent(store)
    _ensure_continuity_case_open_permission(
        store,
        opener_agent_id=opener["agent_id"],
        community_id=args.community_id,
        subject_agent_id=args.subject_agent_id,
    )
    payload = build_case_payload(
        community_id=args.community_id,
        subject_agent_id=args.subject_agent_id,
        trigger_type=args.trigger_type,
        opened_by=opener["agent_id"],
        standing_before=args.standing_before,
        standing_during_review=args.standing_during_review,
        evaluated_scope=args.evaluated_scope,
        linked_refs=args.linked_ref,
        required_assessment_refs=args.assessment_ref,
        assigned_assessor_agent_ids=args.assessor_agent_id,
        assigned_decider_agent_ids=args.decider_agent_id,
        status=args.status,
        opened_at=args.opened_at,
    )
    envelope = build_event(
        kind="continuity_case_open",
        actor_id=opener["agent_id"],
        signing_key=opener["signing_key"],
        secret_hex=opener["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.opened_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_continuity_case_decide(args: argparse.Namespace) -> int:
    store = _store()
    decider = _load_current_agent(store)
    case_event = store.load_event(args.case_event_id)
    case = _resolved_case(store, case_event["payload"]["continuity_case"], refresh=True)
    assessments = [store.load_assessment(assessment_id) for assessment_id in args.assessment_id]
    _ensure_continuity_case_decide_permission(
        store,
        decider_agent_id=decider["agent_id"],
        case=case,
        assessments=assessments,
    )
    payload = build_standing_decision_payload(
        case=case,
        assessments=assessments,
        decided_by=decider["agent_id"],
        reason=args.reason,
        canonical_branch_result=args.canonical_branch_result,
        standing_after=args.standing_after,
        effective_at=args.effective_at,
    )
    envelope = build_event(
        kind="standing_decide",
        actor_id=decider["agent_id"],
        signing_key=decider["signing_key"],
        secret_hex=decider["secret_hex"],
        community_id=case["community_id"],
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.case_event_id, "ref_type": "event", "relationship": "governs"}]
        + [
            {"ref": assessment_id, "ref_type": "assessment", "relationship": "evaluates"}
            for assessment_id in sorted(set(args.assessment_id))
        ],
        created_at=args.effective_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_continuity_case_reassign(args: argparse.Namespace) -> int:
    store = _store()
    operator = _load_current_agent(store)
    case_event = store.load_event(args.case_event_id)
    case = _resolved_case(store, case_event["payload"]["continuity_case"], refresh=True)
    constitution = _constitution(store, case["community_id"])
    _ensure_case_assignment_permission(
        store,
        operator_agent_id=operator["agent_id"],
        case=case,
    )
    _ensure_review_assignment_targets(
        store,
        community_id=case["community_id"],
        subject_agent_id=case["subject_agent_id"],
        assigned_assessor_agent_ids=args.assessor_agent_id,
        assigned_decider_agent_ids=args.decider_agent_id,
    )
    previous_assignment = case.get("latest_assignment")
    payload = build_case_assignment_payload(
        case=case,
        assigned_by=operator["agent_id"],
        reason=args.reason,
        constitution_ref=constitution["constitution_id"],
        assigned_assessor_agent_ids=args.assessor_agent_id,
        assigned_decider_agent_ids=args.decider_agent_id,
        required_assessment_refs=args.assessment_ref if args.assessment_ref else None,
        effective_at=args.effective_at,
        previous_assignment_ref=previous_assignment["assignment_id"] if previous_assignment else None,
    )
    envelope = build_event(
        kind="continuity_case_assign",
        actor_id=operator["agent_id"],
        signing_key=operator["signing_key"],
        secret_hex=operator["secret_hex"],
        community_id=case["community_id"],
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.case_event_id, "ref_type": "event", "relationship": "affects"}],
        created_at=args.effective_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def _standing_state(store: RepositoryStore, subject_agent_id: str, community_id: str | None, refresh: bool) -> dict:
    if not refresh:
        try:
            return store.load_standing_state(subject_agent_id, community_id)
        except FileNotFoundError:
            pass
    indexer = RepositoryIndexer(store)
    state = indexer.materialize_continuity_state(subject_agent_id, community_id)
    store.save_standing_state(state)
    return state


def _governance_state(store: RepositoryStore, community_id: str, refresh: bool) -> dict:
    if not refresh:
        try:
            return store.load_governance_state(community_id)
        except FileNotFoundError:
            pass
    indexer = RepositoryIndexer(store)
    state = indexer.materialize_governance_state(community_id)
    store.save_governance_state(state)
    return state


def _membership_record(store: RepositoryStore, community_id: str, agent_id: str, refresh: bool = False) -> dict | None:
    governance = _governance_state(store, community_id, refresh=refresh)
    return governance["membership_by_agent"].get(agent_id)


def _require_active_membership(store: RepositoryStore, community_id: str, agent_id: str) -> dict:
    membership = _membership_record(store, community_id, agent_id, refresh=True)
    if not membership or membership["membership_status"] != "active":
        raise ValueError(f"Agent {agent_id} does not have active membership in {community_id}.")
    return membership


def _standing_level(store: RepositoryStore, agent_id: str, community_id: str) -> str:
    return _standing_state(store, agent_id, community_id, refresh=True)["current_standing"]


def _constitution(store: RepositoryStore, community_id: str) -> dict:
    governance = _governance_state(store, community_id, refresh=True)
    return governance.get("latest_constitution") or _default_constitution(community_id)


def _resolved_case(store: RepositoryStore, base_case: dict, refresh: bool) -> dict:
    standing = _standing_state(
        store,
        base_case["subject_agent_id"],
        base_case["community_id"],
        refresh=refresh,
    )
    for case in standing["cases"]:
        if case["case_id"] == base_case["case_id"]:
            return case
    return base_case


def _membership_has_required_role(membership: dict, required_roles: list[str]) -> bool:
    if not required_roles:
        return True
    role_set = set(membership.get("role_set", []))
    return any(role in role_set for role in required_roles)


def _policy_for(mapping: dict | None, key: str) -> dict:
    if not mapping:
        return {}
    return mapping.get(key, {})


def _ensure_continuity_case_open_permission(
    store: RepositoryStore,
    opener_agent_id: str,
    community_id: str,
    subject_agent_id: str,
) -> None:
    constitution = _constitution(store, community_id)
    policy = _policy_for(constitution.get("continuity_policies"), "case_open")
    if opener_agent_id == subject_agent_id and not policy.get("allow_subject_self_open", False):
        raise ValueError("Continuity review subjects may not open their own cases in this community.")
    membership = _require_active_membership(store, community_id, opener_agent_id)
    standing = _standing_level(store, opener_agent_id, community_id)
    allowed_standings = policy.get("allowed_standings")
    required_roles = policy.get("required_roles", [])
    if standing in {"suspended", "revoked"}:
        raise ValueError(f"Standing {standing} blocks continuity case opening for {opener_agent_id}.")
    if allowed_standings and standing not in set(allowed_standings):
        raise ValueError(
            f"Standing {standing} blocks continuity case opening for {opener_agent_id} in {community_id}."
        )
    if not _membership_has_required_role(membership, required_roles):
        raise ValueError(
            f"Roles {membership.get('role_set', [])} do not satisfy continuity case opening policy in {community_id}."
        )


def _ensure_case_assignment_permission(
    store: RepositoryStore,
    operator_agent_id: str,
    case: dict,
) -> None:
    community_id = case["community_id"]
    subject_agent_id = case["subject_agent_id"]
    constitution = _constitution(store, community_id)
    policy = _policy_for(constitution.get("continuity_policies"), "case_assign")
    if operator_agent_id == subject_agent_id and not policy.get("allow_subject_self_assign", False):
        raise ValueError("Continuity review subjects may not reassign their own cases in this community.")
    membership = _require_active_membership(store, community_id, operator_agent_id)
    standing = _standing_level(store, operator_agent_id, community_id)
    allowed_standings = policy.get("allowed_standings")
    required_roles = policy.get("required_roles", [])
    if standing in {"suspended", "revoked"}:
        raise ValueError(f"Standing {standing} blocks continuity case reassignment for {operator_agent_id}.")
    if allowed_standings and standing not in set(allowed_standings):
        raise ValueError(
            f"Standing {standing} blocks continuity case reassignment for {operator_agent_id} in {community_id}."
        )
    if not _membership_has_required_role(membership, required_roles):
        raise ValueError(
            f"Roles {membership.get('role_set', [])} do not satisfy continuity reassignment policy in {community_id}."
        )


def _ensure_review_assignment_targets(
    store: RepositoryStore,
    community_id: str,
    subject_agent_id: str,
    assigned_assessor_agent_ids: list[str],
    assigned_decider_agent_ids: list[str],
) -> None:
    constitution = _constitution(store, community_id)
    case_open_policy = _policy_for(constitution.get("continuity_policies"), "case_open")
    case_decide_policy = _policy_for(constitution.get("continuity_policies"), "case_decide")
    required_roles = sorted(
        set(case_open_policy.get("required_roles", [])) | set(case_decide_policy.get("required_roles", []))
    )
    decider_allowed_standings = case_decide_policy.get("allowed_standings")

    for assessor_agent_id in sorted(set(assigned_assessor_agent_ids)):
        if assessor_agent_id == subject_agent_id:
            raise ValueError("Continuity review subjects may not be assigned as assessors in their own case.")
        membership = _require_active_membership(store, community_id, assessor_agent_id)
        if required_roles and not _membership_has_required_role(membership, required_roles):
            raise ValueError(
                f"Roles {membership.get('role_set', [])} do not satisfy reviewer assignment policy in {community_id}."
            )

    for decider_agent_id in sorted(set(assigned_decider_agent_ids)):
        if decider_agent_id == subject_agent_id:
            raise ValueError("Continuity review subjects may not be assigned as deciders in their own case.")
        membership = _require_active_membership(store, community_id, decider_agent_id)
        standing = _standing_level(store, decider_agent_id, community_id)
        if standing in {"suspended", "revoked"}:
            raise ValueError(f"Standing {standing} blocks reviewer assignment for {decider_agent_id}.")
        if decider_allowed_standings and standing not in set(decider_allowed_standings):
            raise ValueError(
                f"Standing {standing} blocks reviewer assignment for {decider_agent_id} in {community_id}."
            )
        if required_roles and not _membership_has_required_role(membership, required_roles):
            raise ValueError(
                f"Roles {membership.get('role_set', [])} do not satisfy reviewer assignment policy in {community_id}."
            )


def _ensure_continuity_case_decide_permission(
    store: RepositoryStore,
    decider_agent_id: str,
    case: dict,
    assessments: list[dict],
) -> None:
    if not assessments:
        raise ValueError("At least one assessment is required for a continuity decision.")
    community_id = case["community_id"]
    subject_agent_id = case["subject_agent_id"]
    constitution = _constitution(store, community_id)
    policy = _policy_for(constitution.get("continuity_policies"), "case_decide")
    if decider_agent_id == subject_agent_id and not policy.get("allow_subject_self_decide", False):
        raise ValueError("Continuity review subjects may not decide their own cases in this community.")
    if decider_agent_id == case["opened_by"] and not policy.get("allow_opener_as_decider", False):
        raise ValueError("The case opener may not also decide the same continuity case in this community.")
    assigned_deciders = set(case.get("assigned_decider_agent_ids", []))
    if assigned_deciders and decider_agent_id not in assigned_deciders:
        raise ValueError(
            f"Agent {decider_agent_id} is not assigned as a decider for continuity case {case['case_id']}."
        )
    required_assessments = set(case.get("required_assessment_refs", []))
    assigned_assessors = set(case.get("assigned_assessor_agent_ids", []))
    seen_assessment_ids: set[str] = set()
    assessor_agent_ids: set[str] = set()
    for assessment in assessments:
        if assessment["assessment_id"] in seen_assessment_ids:
            raise ValueError(f"Assessment {assessment['assessment_id']} was provided more than once.")
        seen_assessment_ids.add(assessment["assessment_id"])
        if assessment["subject_agent_id"] != subject_agent_id:
            raise ValueError(
                f"Assessment {assessment['assessment_id']} does not evaluate the case subject {subject_agent_id}."
            )
        if required_assessments and assessment["assessment_id"] not in required_assessments:
            raise ValueError(
                f"Assessment {assessment['assessment_id']} is not one of the case's accepted assessment refs."
            )
        assessor_agent_id = assessment.get("assessed_by_agent_id")
        if assigned_assessors and assessor_agent_id not in assigned_assessors:
            raise ValueError(
                f"Assessment {assessment['assessment_id']} was not produced by an assigned assessor for case {case['case_id']}."
            )
        if assessor_agent_id:
            assessor_agent_ids.add(assessor_agent_id)
    min_assessment_count = int(policy.get("min_assessment_count", 1))
    if len(seen_assessment_ids) < min_assessment_count:
        raise ValueError(
            f"Continuity case {case['case_id']} requires at least {min_assessment_count} assessments to decide."
        )
    if policy.get("require_distinct_assessors", False) and len(assessor_agent_ids) < len(seen_assessment_ids):
        raise ValueError(
            f"Continuity case {case['case_id']} requires distinct assessors for each cited assessment."
        )
    membership = _require_active_membership(store, community_id, decider_agent_id)
    standing = _standing_level(store, decider_agent_id, community_id)
    allowed_standings = policy.get("allowed_standings")
    required_roles = policy.get("required_roles", [])
    if standing in {"suspended", "revoked"}:
        raise ValueError(f"Standing {standing} blocks continuity case decisions for {decider_agent_id}.")
    if allowed_standings and standing not in set(allowed_standings):
        raise ValueError(
            f"Standing {standing} blocks continuity case decisions for {decider_agent_id} in {community_id}."
        )
    if not _membership_has_required_role(membership, required_roles):
        raise ValueError(
            f"Roles {membership.get('role_set', [])} do not satisfy continuity decision policy in {community_id}."
        )


def _ensure_proposal_permission(store: RepositoryStore, agent_id: str, community_id: str, proposal_type: str) -> None:
    membership = _require_active_membership(store, community_id, agent_id)
    standing = _standing_level(store, agent_id, community_id)
    constitution = _constitution(store, community_id)
    policy = _policy_for(constitution.get("proposal_policies"), proposal_type)
    allowed_standings = policy.get("allowed_standings")
    required_roles = policy.get("required_roles", [])
    if standing in {"suspended", "revoked"}:
        raise ValueError(f"Standing {standing} blocks proposal submission for {agent_id}.")
    if allowed_standings and standing not in set(allowed_standings):
        raise ValueError(
            f"Standing {standing} blocks {proposal_type} proposal submission for {agent_id} in {community_id}."
        )
    if not _membership_has_required_role(membership, required_roles):
        raise ValueError(
            f"Roles {membership.get('role_set', [])} do not satisfy proposal policy for {proposal_type} in {community_id}."
        )


def _ensure_vote_permission(
    store: RepositoryStore,
    agent_id: str,
    community_id: str,
    proposal_type: str,
) -> None:
    membership = _require_active_membership(store, community_id, agent_id)
    standing = _standing_level(store, agent_id, community_id)
    constitution = _constitution(store, community_id)
    policy = _policy_for(constitution.get("vote_policies"), proposal_type)
    allowed_standings = policy.get("allowed_standings")
    required_roles = policy.get("required_roles", [])
    if standing in {"suspended", "revoked"}:
        raise ValueError(f"Standing {standing} blocks vote casting for {agent_id}.")
    if allowed_standings and standing not in set(allowed_standings):
        raise ValueError(f"Standing {standing} blocks voting on {proposal_type} proposals for {agent_id}.")
    if not _membership_has_required_role(membership, required_roles):
        raise ValueError(
            f"Roles {membership.get('role_set', [])} do not satisfy vote policy for {proposal_type} in {community_id}."
        )


def _reward_policy(store: RepositoryStore, community_id: str, reward_type: str) -> dict:
    constitution = _constitution(store, community_id)
    return _policy_for(constitution.get("reward_policies"), reward_type)


def _find_proposal(store: RepositoryStore, community_id: str, proposal_id: str) -> dict:
    governance = _governance_state(store, community_id, refresh=True)
    for proposal in governance["proposals"]:
        if proposal["proposal_id"] == proposal_id:
            return proposal
    raise ValueError(f"Proposal {proposal_id} not found in {community_id}.")


def _find_work_item(store: RepositoryStore, community_id: str, work_id: str) -> dict:
    governance = _governance_state(store, community_id, refresh=True)
    for work_item in governance["work_items"]:
        if work_item["work_id"] == work_id:
            return work_item
    raise ValueError(f"Work item {work_id} not found in {community_id}.")


def _find_receipt(store: RepositoryStore, community_id: str, receipt_id: str) -> dict:
    governance = _governance_state(store, community_id, refresh=True)
    for receipt in governance["work_receipts"]:
        if receipt["receipt_id"] == receipt_id and receipt["community_id"] == community_id:
            return receipt
    raise ValueError(f"Work receipt {receipt_id} not found in {community_id}.")


def _find_evaluation(store: RepositoryStore, receipt_id: str) -> dict:
    for event in store.list_events(kind="work_evaluation_record"):
        evaluation = event["payload"]["work_evaluation"]
        if evaluation["receipt_id"] == receipt_id:
            return evaluation
    raise ValueError(f"No work evaluation found for receipt {receipt_id}.")


def cmd_query_continuity_cases(args: argparse.Namespace) -> int:
    store = _store()
    subject_agent_id = args.subject_agent_id or _load_current_agent(store)["agent_id"]
    standing_state = _standing_state(store, subject_agent_id, args.community_id, refresh=args.refresh)
    print(
        json.dumps(
            {
                "subject_agent_id": subject_agent_id,
                "community_id": args.community_id,
                "cases": standing_state["cases"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def cmd_query_standing_state(args: argparse.Namespace) -> int:
    store = _store()
    subject_agent_id = args.subject_agent_id or _load_current_agent(store)["agent_id"]
    print(
        json.dumps(
            _standing_state(store, subject_agent_id, args.community_id, refresh=args.refresh),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def cmd_governance_constitution_set(args: argparse.Namespace) -> int:
    store = _store()
    operator = _load_current_agent(store)
    payload = build_constitution_payload(
        community_id=args.community_id,
        title=args.title,
        purpose=args.purpose,
        constitution_version=args.constitution_version,
        proposal_policies=json.loads(args.proposal_policies_json),
        vote_policies=json.loads(args.vote_policies_json),
        reward_policies=json.loads(args.reward_policies_json),
        continuity_policies=json.loads(args.continuity_policies_json),
        role_definitions=json.loads(args.role_definitions_json),
        amended_at=args.amended_at,
        supersedes=args.supersedes,
    )
    envelope = build_event(
        kind="community_constitution_set",
        actor_id=operator["agent_id"],
        signing_key=operator["signing_key"],
        secret_hex=operator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.amended_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_governance_constitution_resolve(args: argparse.Namespace) -> int:
    store = _store()
    operator = _load_current_agent(store)
    _ensure_proposal_permission(store, operator["agent_id"], args.community_id, "constitutional")
    payload = build_constitution_resolution_payload(
        community_id=args.community_id,
        resolved_by=operator["agent_id"],
        recognized_constitution_id=args.recognized_constitution_id,
        rejected_constitution_ids=args.rejected_constitution_id,
        reason=args.reason,
        basis_refs=args.basis_ref,
        parent_constitution_id=args.parent_constitution_id,
        resolved_at=args.resolved_at,
    )
    envelope = build_event(
        kind="community_constitution_resolve",
        actor_id=operator["agent_id"],
        signing_key=operator["signing_key"],
        secret_hex=operator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.resolved_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_governance_membership_grant(args: argparse.Namespace) -> int:
    store = _store()
    operator = _load_current_agent(store)
    payload = build_membership_payload(
        community_id=args.community_id,
        member_agent_id=args.member_agent_id,
        membership_status=args.membership_status,
        role_set=args.role,
        sponsor_refs=args.sponsor_ref,
        stake_ref=args.stake_ref,
        continuity_policy_ref=args.continuity_policy_ref,
        joined_at=args.joined_at,
    )
    envelope = build_event(
        kind="membership_record",
        actor_id=operator["agent_id"],
        signing_key=operator["signing_key"],
        secret_hex=operator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.joined_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_governance_execute_record(args: argparse.Namespace) -> int:
    store = _store()
    operator = _load_current_agent(store)
    _require_active_membership(store, args.community_id, operator["agent_id"])
    payload = build_execution_receipt_payload(
        community_id=args.community_id,
        executed_by=operator["agent_id"],
        execution_type=args.execution_type,
        governed_refs=args.governed_ref,
        artifact_refs=args.output_ref,
        result_summary=args.result_summary,
        status=args.status,
        state_root=args.state_root,
        external_anchor_ref=args.external_anchor_ref,
        executed_at=args.executed_at,
    )
    envelope = build_event(
        kind="governance_execute",
        actor_id=operator["agent_id"],
        signing_key=operator["signing_key"],
        secret_hex=operator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.executed_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_governance_proposal_submit(args: argparse.Namespace) -> int:
    store = _store()
    proposer = _load_current_agent(store)
    _ensure_proposal_permission(store, proposer["agent_id"], args.community_id, args.proposal_type)
    payload = build_proposal_payload(
        community_id=args.community_id,
        proposal_type=args.proposal_type,
        title=args.title,
        summary=args.summary,
        proposer_agent_id=proposer["agent_id"],
        body_ref=args.body_ref,
        opens_at=args.opens_at,
        closes_at=args.closes_at,
        execution_mode=args.execution_mode,
        required_role=args.required_role,
        continuity_requirements=args.continuity_requirement,
        affected_refs=args.affected_ref,
        lifecycle_state=args.lifecycle_state,
        created_at=args.created_at,
    )
    envelope = build_event(
        kind="proposal_submit",
        actor_id=proposer["agent_id"],
        signing_key=proposer["signing_key"],
        secret_hex=proposer["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.created_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_governance_vote_cast(args: argparse.Namespace) -> int:
    store = _store()
    voter = _load_current_agent(store)
    proposal = _find_proposal(store, args.community_id, args.proposal_id)
    _ensure_vote_permission(store, voter["agent_id"], args.community_id, proposal["proposal_type"])
    constitution = _constitution(store, args.community_id)
    policy = _policy_for(constitution.get("vote_policies"), proposal["proposal_type"])
    payload = build_vote_payload(
        proposal_id=args.proposal_id,
        voter_agent_id=voter["agent_id"],
        community_id=args.community_id,
        choice=args.choice,
        weight_policy_ref=policy.get("weight_policy_ref", args.weight_policy_ref),
        cast_at=args.cast_at,
        weight=args.weight,
        delegated_from=args.delegated_from,
    )
    envelope = build_event(
        kind="vote_cast",
        actor_id=voter["agent_id"],
        signing_key=voter["signing_key"],
        secret_hex=voter["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.proposal_id, "ref_type": "proposal", "relationship": "votes_on"}],
        created_at=args.cast_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_work_item_create(args: argparse.Namespace) -> int:
    store = _store()
    creator = _load_current_agent(store)
    _require_active_membership(store, args.community_id, creator["agent_id"])
    payload = build_work_item_payload(
        community_id=args.community_id,
        title=args.title,
        intent=args.intent,
        work_type=args.work_type,
        created_by=creator["agent_id"],
        success_criteria=args.success_criterion,
        scope_refs=args.scope_ref,
        deliverable_refs=args.deliverable_ref,
        requested_by=args.requested_by,
        reward_policy_ref=args.reward_policy_ref,
        deadline=args.deadline,
        status=args.status,
        created_at=args.created_at,
    )
    envelope = build_event(
        kind="work_item_record",
        actor_id=creator["agent_id"],
        signing_key=creator["signing_key"],
        secret_hex=creator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref),
        created_at=args.created_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_work_claim_submit(args: argparse.Namespace) -> int:
    store = _store()
    claimant = _load_current_agent(store)
    work_item = _find_work_item(store, args.community_id, args.work_id)
    _require_active_membership(store, args.community_id, claimant["agent_id"])
    payload = build_work_claim_payload(
        work_id=work_item["work_id"],
        claimant_agent_id=claimant["agent_id"],
        claim_type=args.claim_type,
        basis_refs=args.basis_ref,
        continuity_ref=args.continuity_ref,
        status=args.status,
        claimed_at=args.claimed_at,
    )
    envelope = build_event(
        kind="work_claim_record",
        actor_id=claimant["agent_id"],
        signing_key=claimant["signing_key"],
        secret_hex=claimant["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.work_id, "ref_type": "work_item", "relationship": "claims"}],
        created_at=args.claimed_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_work_receipt_record(args: argparse.Namespace) -> int:
    store = _store()
    agent = _load_current_agent(store)
    work_item = _find_work_item(store, args.community_id, args.work_id)
    _require_active_membership(store, args.community_id, agent["agent_id"])
    payload = build_work_receipt_payload(
        work_id=work_item["work_id"],
        community_id=args.community_id,
        agent_id=agent["agent_id"],
        artifact_refs=args.output_ref,
        result_summary=args.result_summary,
        evidence_refs=args.evidence_ref,
        receipt_type=args.receipt_type,
        session_ref=args.session_ref,
        continuity_context_ref=args.continuity_context_ref,
        completed_at=args.completed_at,
    )
    envelope = build_event(
        kind="work_receipt_record",
        actor_id=agent["agent_id"],
        signing_key=agent["signing_key"],
        secret_hex=agent["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.work_id, "ref_type": "work_item", "relationship": "completes"}],
        created_at=args.completed_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_work_evaluation_record(args: argparse.Namespace) -> int:
    store = _store()
    evaluator = _load_current_agent(store)
    receipt = _find_receipt(store, args.community_id, args.receipt_id)
    _require_active_membership(store, args.community_id, evaluator["agent_id"])
    payload = build_work_evaluation_payload(
        receipt_id=receipt["receipt_id"],
        evaluator_id=evaluator["agent_id"],
        decision=args.decision,
        criteria_results=args.criteria_result,
        reason_refs=args.reason_ref,
        reward_recommendation=args.reward_recommendation,
        reputation_effect=args.reputation_effect,
        evaluated_at=args.evaluated_at,
    )
    envelope = build_event(
        kind="work_evaluation_record",
        actor_id=evaluator["agent_id"],
        signing_key=evaluator["signing_key"],
        secret_hex=evaluator["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.receipt_id, "ref_type": "work_receipt", "relationship": "evaluates"}],
        created_at=args.evaluated_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_reward_decide(args: argparse.Namespace) -> int:
    store = _store()
    approver = _load_current_agent(store)
    approver_membership = _require_active_membership(store, args.community_id, approver["agent_id"])
    approver_standing = _standing_level(store, approver["agent_id"], args.community_id)
    reward_policy = _reward_policy(store, args.community_id, args.reward_type)
    approver_standings = reward_policy.get("approver_standings", ["clear"])
    approver_roles = reward_policy.get("approver_roles", [])
    if approver_standing not in set(approver_standings):
        raise ValueError(f"Standing {approver_standing} blocks reward approval for {approver['agent_id']}.")
    if not _membership_has_required_role(approver_membership, approver_roles):
        raise ValueError(
            f"Roles {approver_membership.get('role_set', [])} do not satisfy reward policy for {args.reward_type}."
        )

    receipt = _find_receipt(store, args.community_id, args.receipt_id)
    evaluation = _find_evaluation(store, args.receipt_id)
    if evaluation["decision"] not in {"accepted", "accepted_with_issues"}:
        raise ValueError(
            f"Evaluation decision {evaluation['decision']} does not support reward approval for {args.receipt_id}."
        )

    beneficiary_standing = _standing_level(store, receipt["agent_id"], args.community_id)
    decision_status = args.decision_status
    withholding_reason = None
    beneficiary_standings = reward_policy.get("beneficiary_standings", ["clear"])
    if beneficiary_standing not in set(beneficiary_standings):
        decision_status = "withheld_pending_review"
        withholding_reason = f"beneficiary_standing_{beneficiary_standing}"

    payload = build_reward_decision_payload(
        receipt_id=receipt["receipt_id"],
        evaluation_id=evaluation["evaluation_id"],
        community_id=args.community_id,
        beneficiary_agent_id=receipt["agent_id"],
        reward_type=args.reward_type,
        approved_by=approver["agent_id"],
        policy_ref=args.policy_ref,
        amount=args.amount,
        asset_ref=args.asset_ref,
        disbursement_ref=args.disbursement_ref,
        decision_status=decision_status,
        withholding_reason=withholding_reason,
        approved_at=args.approved_at,
    )
    envelope = build_event(
        kind="reward_decide",
        actor_id=approver["agent_id"],
        signing_key=approver["signing_key"],
        secret_hex=approver["secret_hex"],
        community_id=args.community_id,
        payload=payload,
        refs=artifact_refs(args.artifact_ref)
        + [{"ref": args.receipt_id, "ref_type": "work_receipt", "relationship": "rewards"}]
        + [{"ref": evaluation["evaluation_id"], "ref_type": "work_evaluation", "relationship": "depends_on"}],
        created_at=args.approved_at,
    )
    store.save_event(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0


def cmd_query_governance_state(args: argparse.Namespace) -> int:
    store = _store()
    print(json.dumps(_governance_state(store, args.community_id, refresh=args.refresh), indent=2, sort_keys=True))
    return 0


def _anchor_subject_and_root(store: RepositoryStore, args: argparse.Namespace) -> tuple[str, str]:
    if args.anchor_type == "continuity_assessment_root":
        assessment = store.load_assessment(args.assessment_id)
        return assessment["assessment_id"], f"state:{_digest_assessment(assessment)}"
    if args.anchor_type == "agent_state_root":
        actor_id = args.actor_id or _load_current_agent(store)["agent_id"]
        state = _agent_state(store, actor_id, refresh=args.refresh)
        return state["actor_id"], state["state_root"]
    if args.anchor_type == "standing_state_root":
        subject_agent_id = args.subject_agent_id or _load_current_agent(store)["agent_id"]
        state = _standing_state(store, subject_agent_id, args.community_id, refresh=args.refresh)
        community_key = args.community_id or "repository"
        return f"{subject_agent_id}::{community_key}", state["state_root"]
    if args.anchor_type == "governance_state_root":
        state = _governance_state(store, args.community_id, refresh=args.refresh)
        return state["community_id"], state["state_root"]
    raise ValueError(f"Unsupported anchor type {args.anchor_type}.")


def _digest_assessment(assessment: dict) -> str:
    from src.runtime.canonical import digest_hex

    return digest_hex(assessment)


def cmd_anchor_export(args: argparse.Namespace) -> int:
    store = _store()
    subject_ref, root_hash = _anchor_subject_and_root(store, args)
    if args.adapter_mode == "dry_run_external":
        adapter = DryRunExternalAnchorAdapter(target_name=args.adapter)
    else:
        adapter = LocalAnchorAdapter(target_name=args.adapter)
    anchor_record = adapter.export(
        AnchorExportRequest(
            anchor_type=args.anchor_type,
            subject_ref=subject_ref,
            root_hash=root_hash,
            anchored_at=args.anchored_at,
        )
    )
    store.save_anchor(anchor_record)
    print(json.dumps(anchor_record, indent=2, sort_keys=True))
    return 0


def cmd_anchor_list(args: argparse.Namespace) -> int:
    store = _store()
    anchors = store.list_anchors(subject_ref=args.subject_ref, anchor_type=args.anchor_type)
    print(json.dumps({"anchors": anchors}, indent=2, sort_keys=True))
    return 0


def cmd_anchor_inspect(args: argparse.Namespace) -> int:
    store = _store()
    print(json.dumps(store.load_anchor(args.anchor_id), indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="continuum")
    subparsers = parser.add_subparsers(dest="command", required=True)

    agent = subparsers.add_parser("agent")
    agent_sub = agent.add_subparsers(dest="agent_command", required=True)

    agent_init = agent_sub.add_parser("init")
    agent_init.add_argument("--scope", required=True)
    agent_init.add_argument("--name", required=True)
    agent_init.add_argument("--display-name", required=True)
    agent_init.add_argument("--description", default="")
    agent_init.add_argument("--operator-disclosure")
    agent_init.add_argument("--agent-id")
    agent_init.set_defaults(func=cmd_agent_init)

    agent_show = agent_sub.add_parser("show")
    agent_show.set_defaults(func=cmd_agent_show)

    agent_use = agent_sub.add_parser("use")
    agent_use.add_argument("--agent-id", required=True)
    agent_use.set_defaults(func=cmd_agent_use)

    profile = agent_sub.add_parser("profile")
    profile_sub = profile.add_subparsers(dest="profile_command", required=True)
    profile_set = profile_sub.add_parser("set")
    profile_set.add_argument("--display-name", required=True)
    profile_set.add_argument("--description", default="")
    profile_set.add_argument("--operator-disclosure")
    profile_set.add_argument("--community-id")
    profile_set.add_argument("--artifact-ref", action="append", default=[])
    profile_set.set_defaults(func=cmd_agent_profile_set)

    memory = subparsers.add_parser("memory")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)
    checkpoint = memory_sub.add_parser("checkpoint")
    checkpoint_sub = checkpoint.add_subparsers(dest="checkpoint_command", required=True)
    checkpoint_create = checkpoint_sub.add_parser("create")
    checkpoint_create.add_argument("--scope", required=True, choices=sorted(CHECKPOINT_SCOPES))
    checkpoint_create.add_argument("--summary", required=True)
    checkpoint_create.add_argument("--state-root")
    checkpoint_create.add_argument("--checkpoint-uri")
    checkpoint_create.add_argument("--prev-checkpoint-id")
    checkpoint_create.add_argument("--community-id")
    checkpoint_create.add_argument("--artifact-ref", action="append", default=[])
    checkpoint_create.set_defaults(func=cmd_memory_checkpoint_create)

    migration = subparsers.add_parser("migration")
    migration_sub = migration.add_subparsers(dest="migration_command", required=True)
    migration_declare = migration_sub.add_parser("declare")
    migration_declare.add_argument("--migration-type", required=True, choices=sorted(MIGRATION_TYPES))
    migration_declare.add_argument("--from-ref", required=True)
    migration_declare.add_argument("--to-ref", required=True)
    migration_declare.add_argument("--reason", required=True)
    migration_declare.add_argument("--evidence", action="append", default=[])
    migration_declare.add_argument("--expected-continuity-class", default="same_agent")
    migration_declare.add_argument("--effective-at")
    migration_declare.add_argument("--prev-migration-id")
    migration_declare.add_argument("--community-id")
    migration_declare.add_argument("--artifact-ref", action="append", default=[])
    migration_declare.set_defaults(func=cmd_migration_declare)

    event = subparsers.add_parser("event")
    event_sub = event.add_subparsers(dest="event_command", required=True)
    event_list = event_sub.add_parser("list")
    event_list.add_argument("--actor-id")
    event_list.add_argument("--kind")
    event_list.set_defaults(func=cmd_event_list)

    event_inspect = event_sub.add_parser("inspect")
    event_inspect.add_argument("--event-id", required=True)
    event_inspect.set_defaults(func=cmd_event_inspect)

    query = subparsers.add_parser("query")
    query_sub = query.add_subparsers(dest="query_command", required=True)

    query_state = query_sub.add_parser("agent-state")
    query_state.add_argument("--actor-id")
    query_state.add_argument("--refresh", action="store_true")
    query_state.set_defaults(func=cmd_query_agent_state)

    query_history = query_sub.add_parser("agent-history")
    query_history.add_argument("--actor-id")
    query_history.add_argument("--refresh", action="store_true")
    query_history.set_defaults(func=cmd_query_agent_history)

    query_checkpoints = query_sub.add_parser("checkpoint-lineage")
    query_checkpoints.add_argument("--actor-id")
    query_checkpoints.add_argument("--scope", choices=sorted(CHECKPOINT_SCOPES))
    query_checkpoints.add_argument("--refresh", action="store_true")
    query_checkpoints.set_defaults(func=cmd_query_checkpoint_lineage)

    query_migrations = query_sub.add_parser("migration-lineage")
    query_migrations.add_argument("--actor-id")
    query_migrations.add_argument("--migration-type", choices=sorted(MIGRATION_TYPES))
    query_migrations.add_argument("--refresh", action="store_true")
    query_migrations.set_defaults(func=cmd_query_migration_lineage)

    continuity = subparsers.add_parser("continuity")
    continuity_sub = continuity.add_subparsers(dest="continuity_command", required=True)
    continuity_assess = continuity_sub.add_parser("assess")
    continuity_assess.add_argument("--actor-id")
    continuity_assess.add_argument("--event-id")
    continuity_assess.add_argument("--scope", default="repository")
    continuity_assess.add_argument("--assessor-type", default="runtime")
    continuity_assess.add_argument("--refresh", action="store_true")
    continuity_assess.set_defaults(func=cmd_continuity_assess)

    continuity_case = continuity_sub.add_parser("case")
    continuity_case_sub = continuity_case.add_subparsers(dest="case_command", required=True)

    continuity_case_open = continuity_case_sub.add_parser("open")
    continuity_case_open.add_argument("--community-id", required=True)
    continuity_case_open.add_argument("--subject-agent-id", required=True)
    continuity_case_open.add_argument("--trigger-type", required=True, choices=sorted(CASE_TRIGGER_TYPES))
    continuity_case_open.add_argument("--standing-before", default="clear", choices=sorted(STANDING_LEVELS))
    continuity_case_open.add_argument("--standing-during-review", default="restricted", choices=sorted(STANDING_LEVELS))
    continuity_case_open.add_argument("--evaluated-scope", default="repository")
    continuity_case_open.add_argument("--linked-ref", action="append", default=[])
    continuity_case_open.add_argument("--assessment-ref", action="append", default=[])
    continuity_case_open.add_argument("--assessor-agent-id", action="append", default=[])
    continuity_case_open.add_argument("--decider-agent-id", action="append", default=[])
    continuity_case_open.add_argument("--status", choices=sorted(CASE_STATUSES))
    continuity_case_open.add_argument("--opened-at")
    continuity_case_open.add_argument("--artifact-ref", action="append", default=[])
    continuity_case_open.set_defaults(func=cmd_continuity_case_open)

    continuity_case_reassign = continuity_case_sub.add_parser("reassign")
    continuity_case_reassign.add_argument("--case-event-id", required=True)
    continuity_case_reassign.add_argument("--assessment-ref", action="append", default=[])
    continuity_case_reassign.add_argument("--assessor-agent-id", action="append", default=[])
    continuity_case_reassign.add_argument("--decider-agent-id", action="append", default=[])
    continuity_case_reassign.add_argument("--reason", required=True)
    continuity_case_reassign.add_argument("--effective-at")
    continuity_case_reassign.add_argument("--artifact-ref", action="append", default=[])
    continuity_case_reassign.set_defaults(func=cmd_continuity_case_reassign)

    continuity_case_decide = continuity_case_sub.add_parser("decide")
    continuity_case_decide.add_argument("--case-event-id", required=True)
    continuity_case_decide.add_argument("--assessment-id", required=True, action="append")
    continuity_case_decide.add_argument("--reason", required=True)
    continuity_case_decide.add_argument("--canonical-branch-result")
    continuity_case_decide.add_argument("--standing-after", choices=sorted(STANDING_LEVELS))
    continuity_case_decide.add_argument("--effective-at")
    continuity_case_decide.add_argument("--artifact-ref", action="append", default=[])
    continuity_case_decide.set_defaults(func=cmd_continuity_case_decide)

    governance = subparsers.add_parser("governance")
    governance_sub = governance.add_subparsers(dest="governance_command", required=True)

    constitution = governance_sub.add_parser("constitution")
    constitution_sub = constitution.add_subparsers(dest="constitution_command", required=True)
    constitution_set = constitution_sub.add_parser("set")
    constitution_set.add_argument("--community-id", required=True)
    constitution_set.add_argument("--title", default="Continuum Community Constitution v0")
    constitution_set.add_argument("--purpose", default="Define explicit governance, continuity, and reward policies.")
    constitution_set.add_argument("--constitution-version", default="v0")
    constitution_set.add_argument(
        "--proposal-policies-json",
        default=json.dumps(_default_constitution("community:default")["proposal_policies"], sort_keys=True),
    )
    constitution_set.add_argument(
        "--vote-policies-json",
        default=json.dumps(_default_constitution("community:default")["vote_policies"], sort_keys=True),
    )
    constitution_set.add_argument(
        "--reward-policies-json",
        default=json.dumps(_default_constitution("community:default")["reward_policies"], sort_keys=True),
    )
    constitution_set.add_argument(
        "--continuity-policies-json",
        default=json.dumps(_default_constitution("community:default")["continuity_policies"], sort_keys=True),
    )
    constitution_set.add_argument(
        "--role-definitions-json",
        default=json.dumps(_default_constitution("community:default")["role_definitions"], sort_keys=True),
    )
    constitution_set.add_argument("--supersedes")
    constitution_set.add_argument("--amended-at")
    constitution_set.add_argument("--artifact-ref", action="append", default=[])
    constitution_set.set_defaults(func=cmd_governance_constitution_set)
    constitution_resolve = constitution_sub.add_parser("resolve")
    constitution_resolve.add_argument("--community-id", required=True)
    constitution_resolve.add_argument("--recognized-constitution-id", required=True)
    constitution_resolve.add_argument("--rejected-constitution-id", action="append", default=[])
    constitution_resolve.add_argument("--parent-constitution-id")
    constitution_resolve.add_argument("--reason", required=True)
    constitution_resolve.add_argument("--basis-ref", action="append", default=[])
    constitution_resolve.add_argument("--resolved-at")
    constitution_resolve.add_argument("--artifact-ref", action="append", default=[])
    constitution_resolve.set_defaults(func=cmd_governance_constitution_resolve)

    membership = governance_sub.add_parser("membership")
    membership_sub = membership.add_subparsers(dest="membership_command", required=True)
    membership_grant = membership_sub.add_parser("grant")
    membership_grant.add_argument("--community-id", required=True)
    membership_grant.add_argument("--member-agent-id", required=True)
    membership_grant.add_argument("--membership-status", default="active", choices=sorted(MEMBERSHIP_STATUSES))
    membership_grant.add_argument("--role", action="append", default=[])
    membership_grant.add_argument("--sponsor-ref", action="append", default=[])
    membership_grant.add_argument("--stake-ref")
    membership_grant.add_argument("--continuity-policy-ref")
    membership_grant.add_argument("--joined-at")
    membership_grant.add_argument("--artifact-ref", action="append", default=[])
    membership_grant.set_defaults(func=cmd_governance_membership_grant)

    proposal = governance_sub.add_parser("proposal")
    proposal_sub = proposal.add_subparsers(dest="proposal_command", required=True)
    proposal_submit = proposal_sub.add_parser("submit")
    proposal_submit.add_argument("--community-id", required=True)
    proposal_submit.add_argument("--proposal-type", required=True, choices=sorted(PROPOSAL_TYPES))
    proposal_submit.add_argument("--title", required=True)
    proposal_submit.add_argument("--summary", required=True)
    proposal_submit.add_argument("--body-ref")
    proposal_submit.add_argument("--opens-at")
    proposal_submit.add_argument("--closes-at")
    proposal_submit.add_argument("--execution-mode", default="manual_review")
    proposal_submit.add_argument("--required-role")
    proposal_submit.add_argument("--continuity-requirement", action="append", default=[])
    proposal_submit.add_argument("--affected-ref", action="append", default=[])
    proposal_submit.add_argument(
        "--lifecycle-state",
        default="submitted",
        choices=sorted(PROPOSAL_LIFECYCLE_STATES),
    )
    proposal_submit.add_argument("--created-at")
    proposal_submit.add_argument("--artifact-ref", action="append", default=[])
    proposal_submit.set_defaults(func=cmd_governance_proposal_submit)

    vote = governance_sub.add_parser("vote")
    vote_sub = vote.add_subparsers(dest="vote_command", required=True)
    vote_cast = vote_sub.add_parser("cast")
    vote_cast.add_argument("--community-id", required=True)
    vote_cast.add_argument("--proposal-id", required=True)
    vote_cast.add_argument("--choice", required=True, choices=sorted(VOTE_CHOICES))
    vote_cast.add_argument("--weight", type=float, default=1.0)
    vote_cast.add_argument("--weight-policy-ref", default="policy:one_member_one_vote")
    vote_cast.add_argument("--delegated-from")
    vote_cast.add_argument("--cast-at")
    vote_cast.add_argument("--artifact-ref", action="append", default=[])
    vote_cast.set_defaults(func=cmd_governance_vote_cast)

    work = subparsers.add_parser("work")
    work_sub = work.add_subparsers(dest="work_command", required=True)

    work_item = work_sub.add_parser("item")
    work_item_sub = work_item.add_subparsers(dest="work_item_command", required=True)
    work_item_create = work_item_sub.add_parser("create")
    work_item_create.add_argument("--community-id", required=True)
    work_item_create.add_argument("--title", required=True)
    work_item_create.add_argument("--intent", required=True)
    work_item_create.add_argument("--work-type", required=True, choices=sorted(WORK_TYPES))
    work_item_create.add_argument("--success-criterion", action="append", default=[])
    work_item_create.add_argument("--scope-ref", action="append", default=[])
    work_item_create.add_argument("--deliverable-ref", action="append", default=[])
    work_item_create.add_argument("--requested-by")
    work_item_create.add_argument("--reward-policy-ref")
    work_item_create.add_argument("--deadline")
    work_item_create.add_argument("--status", default="proposed", choices=sorted(WORK_STATUSES))
    work_item_create.add_argument("--created-at")
    work_item_create.add_argument("--artifact-ref", action="append", default=[])
    work_item_create.set_defaults(func=cmd_work_item_create)

    work_claim = work_sub.add_parser("claim")
    work_claim_sub = work_claim.add_subparsers(dest="work_claim_command", required=True)
    work_claim_submit = work_claim_sub.add_parser("submit")
    work_claim_submit.add_argument("--community-id", required=True)
    work_claim_submit.add_argument("--work-id", required=True)
    work_claim_submit.add_argument("--claim-type", required=True, choices=sorted(WORK_CLAIM_TYPES))
    work_claim_submit.add_argument("--basis-ref", action="append", default=[])
    work_claim_submit.add_argument("--continuity-ref")
    work_claim_submit.add_argument("--status", default="submitted")
    work_claim_submit.add_argument("--claimed-at")
    work_claim_submit.add_argument("--artifact-ref", action="append", default=[])
    work_claim_submit.set_defaults(func=cmd_work_claim_submit)

    work_receipt = work_sub.add_parser("receipt")
    work_receipt_sub = work_receipt.add_subparsers(dest="work_receipt_command", required=True)
    work_receipt_record = work_receipt_sub.add_parser("record")
    work_receipt_record.add_argument("--community-id", required=True)
    work_receipt_record.add_argument("--work-id", required=True)
    work_receipt_record.add_argument("--output-ref", action="append", default=[])
    work_receipt_record.add_argument("--result-summary", required=True)
    work_receipt_record.add_argument("--evidence-ref", action="append", default=[])
    work_receipt_record.add_argument("--receipt-type", default="completion", choices=sorted(WORK_RECEIPT_TYPES))
    work_receipt_record.add_argument("--session-ref")
    work_receipt_record.add_argument("--continuity-context-ref")
    work_receipt_record.add_argument("--completed-at")
    work_receipt_record.add_argument("--artifact-ref", action="append", default=[])
    work_receipt_record.set_defaults(func=cmd_work_receipt_record)

    work_evaluation = work_sub.add_parser("evaluation")
    work_evaluation_sub = work_evaluation.add_subparsers(dest="work_evaluation_command", required=True)
    work_evaluation_record = work_evaluation_sub.add_parser("record")
    work_evaluation_record.add_argument("--community-id", required=True)
    work_evaluation_record.add_argument("--receipt-id", required=True)
    work_evaluation_record.add_argument("--decision", required=True, choices=sorted(WORK_EVALUATION_DECISIONS))
    work_evaluation_record.add_argument("--criteria-result", action="append", default=[])
    work_evaluation_record.add_argument("--reason-ref", action="append", default=[])
    work_evaluation_record.add_argument("--reward-recommendation")
    work_evaluation_record.add_argument("--reputation-effect")
    work_evaluation_record.add_argument("--evaluated-at")
    work_evaluation_record.add_argument("--artifact-ref", action="append", default=[])
    work_evaluation_record.set_defaults(func=cmd_work_evaluation_record)

    reward = governance_sub.add_parser("reward")
    reward_sub = reward.add_subparsers(dest="reward_command", required=True)
    reward_decide = reward_sub.add_parser("decide")
    reward_decide.add_argument("--community-id", required=True)
    reward_decide.add_argument("--receipt-id", required=True)
    reward_decide.add_argument("--reward-type", required=True, choices=sorted(REWARD_TYPES))
    reward_decide.add_argument("--policy-ref", required=True)
    reward_decide.add_argument("--amount", type=float)
    reward_decide.add_argument("--asset-ref")
    reward_decide.add_argument("--disbursement-ref")
    reward_decide.add_argument(
        "--decision-status",
        default="approved",
        choices=sorted(REWARD_DECISION_STATUSES),
    )
    reward_decide.add_argument("--approved-at")
    reward_decide.add_argument("--artifact-ref", action="append", default=[])
    reward_decide.set_defaults(func=cmd_reward_decide)

    execute = governance_sub.add_parser("execute")
    execute_sub = execute.add_subparsers(dest="execute_command", required=True)
    execute_record = execute_sub.add_parser("record")
    execute_record.add_argument("--community-id", required=True)
    execute_record.add_argument(
        "--execution-type",
        required=True,
        choices=[
            "proposal_execution",
            "standing_execution",
            "reward_execution",
            "treasury_execution",
            "constitution_execution",
        ],
    )
    execute_record.add_argument("--governed-ref", action="append", default=[], required=True)
    execute_record.add_argument("--output-ref", action="append", default=[])
    execute_record.add_argument("--result-summary", required=True)
    execute_record.add_argument("--status", default="executed")
    execute_record.add_argument("--state-root")
    execute_record.add_argument("--external-anchor-ref")
    execute_record.add_argument("--executed-at")
    execute_record.add_argument("--artifact-ref", action="append", default=[])
    execute_record.set_defaults(func=cmd_governance_execute_record)

    query_cases = query_sub.add_parser("continuity-cases")
    query_cases.add_argument("--subject-agent-id")
    query_cases.add_argument("--community-id")
    query_cases.add_argument("--refresh", action="store_true")
    query_cases.set_defaults(func=cmd_query_continuity_cases)

    query_standing = query_sub.add_parser("standing-state")
    query_standing.add_argument("--subject-agent-id")
    query_standing.add_argument("--community-id")
    query_standing.add_argument("--refresh", action="store_true")
    query_standing.set_defaults(func=cmd_query_standing_state)

    query_governance = query_sub.add_parser("governance-state")
    query_governance.add_argument("--community-id", required=True)
    query_governance.add_argument("--refresh", action="store_true")
    query_governance.set_defaults(func=cmd_query_governance_state)

    anchor = subparsers.add_parser("anchor")
    anchor_sub = anchor.add_subparsers(dest="anchor_command", required=True)

    anchor_export = anchor_sub.add_parser("export")
    anchor_export.add_argument("--anchor-type", required=True, choices=sorted(ANCHOR_TYPES))
    anchor_export.add_argument(
        "--adapter-mode",
        choices=["local", "dry_run_external"],
        default="local",
    )
    anchor_export.add_argument("--assessment-id")
    anchor_export.add_argument("--actor-id")
    anchor_export.add_argument("--subject-agent-id")
    anchor_export.add_argument("--community-id")
    anchor_export.add_argument("--adapter", default="local_witness_v0")
    anchor_export.add_argument("--anchored-at")
    anchor_export.add_argument("--refresh", action="store_true")
    anchor_export.set_defaults(func=cmd_anchor_export)

    anchor_list = anchor_sub.add_parser("list")
    anchor_list.add_argument("--subject-ref")
    anchor_list.add_argument("--anchor-type", choices=sorted(ANCHOR_TYPES))
    anchor_list.set_defaults(func=cmd_anchor_list)

    anchor_inspect = anchor_sub.add_parser("inspect")
    anchor_inspect.add_argument("--anchor-id", required=True)
    anchor_inspect.set_defaults(func=cmd_anchor_inspect)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
