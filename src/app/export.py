"""Export repository state into app-readable JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.continuity.assessment import ContinuityAssessmentEngine
from src.indexer.materialize import RepositoryIndexer
from src.runtime.store import RepositoryStore


_READINESS_PRIORITY = {
    "ready": 0,
    "needs_review": 1,
    "blocked": 2,
}

_CONTINUITY_PRIORITY = {
    "same_agent": 0,
    "successor_agent": 1,
    "forked_agent": 2,
    "unknown": 3,
}

_STANDING_PRIORITY = {
    "clear": 0,
    "restricted": 1,
    "suspended": 2,
}


def _list_assessments(store: RepositoryStore, subject_agent_id: str) -> list[dict[str, Any]]:
    assessments_dir = store.derived_state_dir / "assessments"
    if not assessments_dir.exists():
        return []
    items = []
    for path in sorted(assessments_dir.glob("*.json")):
        assessment = json.loads(path.read_text(encoding="utf-8"))
        if assessment.get("subject_agent_id") != subject_agent_id:
            continue
        items.append(assessment)
    items.sort(key=lambda item: (item.get("assessed_at", ""), item["assessment_id"]))
    return items


def _latest_assessment(store: RepositoryStore, actor_id: str) -> dict[str, Any]:
    assessments = _list_assessments(store, actor_id)
    if assessments:
        return assessments[-1]
    engine = ContinuityAssessmentEngine(store)
    return engine.assess(actor_id=actor_id, refresh=True)


def _safe_load_standing_state(
    store: RepositoryStore, subject_agent_id: str, community_id: str | None, refresh: bool
) -> dict[str, Any] | None:
    if not community_id:
        return None
    if refresh:
        indexer = RepositoryIndexer(store)
        standing_state = indexer.materialize_continuity_state(subject_agent_id, community_id)
        store.save_standing_state(standing_state)
        return standing_state
    try:
        return store.load_standing_state(subject_agent_id, community_id)
    except FileNotFoundError:
        return None


def _safe_load_governance_state(store: RepositoryStore, community_id: str | None, refresh: bool) -> dict[str, Any] | None:
    if not community_id:
        return None
    if refresh:
        indexer = RepositoryIndexer(store)
        governance_state = indexer.materialize_governance_state(community_id)
        store.save_governance_state(governance_state)
        return governance_state
    try:
        return store.load_governance_state(community_id)
    except FileNotFoundError:
        return None


def build_agent_app_entry(
    store: RepositoryStore,
    *,
    actor_id: str,
    community_id: str | None = None,
    refresh: bool = False,
) -> dict[str, Any]:
    try:
        agent = store.load_agent(actor_id)
    except FileNotFoundError as exc:
        raise ValueError(f"Agent record not found for {actor_id}.") from exc

    if refresh:
        indexer = RepositoryIndexer(store)
        agent_state = indexer.materialize_agent_state(actor_id)
        store.save_agent_state(agent_state)
    else:
        try:
            agent_state = store.load_agent_state(actor_id)
        except FileNotFoundError:
            indexer = RepositoryIndexer(store)
            agent_state = indexer.materialize_agent_state(actor_id)
            store.save_agent_state(agent_state)

    assessment = _latest_assessment(store, actor_id)
    standing_state = _safe_load_standing_state(store, actor_id, community_id, refresh)
    governance_state = _safe_load_governance_state(store, community_id, refresh)
    anchors = store.list_anchors()
    relevant_anchors = []
    for anchor in anchors:
        if anchor["subject_ref"] == assessment["assessment_id"]:
            relevant_anchors.append(anchor)
        elif community_id and anchor["subject_ref"] == community_id:
            relevant_anchors.append(anchor)
        elif anchor["subject_ref"] == actor_id:
            relevant_anchors.append(anchor)
    relevant_anchors.sort(key=lambda item: (item.get("anchored_at", ""), item["anchor_id"]))

    latest_profile = agent_state.get("latest_profile") or {}
    checkpoint_lineage = agent_state.get("checkpoint_lineage", [])
    migration_lineage = agent_state.get("migration_lineage", [])
    latest_membership = None
    proposal_count = 0
    vote_count = 0
    work_item_count = 0
    reward_count = 0
    if governance_state:
        memberships = [
            membership
            for membership in governance_state.get("memberships", [])
            if membership["member_agent_id"] == actor_id
        ]
        latest_membership = memberships[-1] if memberships else None
        proposal_count = sum(
            1 for proposal in governance_state.get("proposals", []) if proposal["proposer_agent_id"] == actor_id
        )
        vote_count = sum(1 for vote in governance_state.get("votes", []) if vote["voter_agent_id"] == actor_id)
        work_item_count = sum(
            1 for work_item in governance_state.get("work_items", []) if work_item["created_by"] == actor_id
        )
        reward_count = sum(
            1 for reward in governance_state.get("reward_decisions", []) if reward["beneficiary_agent_id"] == actor_id
        )

    witness_lines = []
    for anchor in relevant_anchors:
        status = anchor.get("anchor_status", "confirmed_external")
        witness_lines.append(
            f"{anchor['anchor_type']}: {anchor['anchor_target']} ({status})"
        )
    if not witness_lines:
        witness_lines.append("No anchors recorded yet")
    witness_lines.append("Chain Witness: planned, not yet deployed")

    timeline = []
    if latest_profile:
        timeline.append(f"Profile initialized at {latest_profile['created_at']}")
    if checkpoint_lineage:
        latest_checkpoint = checkpoint_lineage[-1]
        timeline.append(
            f"Checkpoint recorded at {latest_checkpoint['created_at']} ({latest_checkpoint['scope']})"
        )
    if migration_lineage:
        latest_migration = migration_lineage[-1]
        timeline.append(
            f"Migration declared at {latest_migration['created_at']} ({latest_migration['migration_type']})"
        )
    timeline.append(
        f"Continuity assessed at {assessment['assessed_at']} ({assessment['continuity_class']})"
    )
    if relevant_anchors:
        latest_anchor = relevant_anchors[-1]
        timeline.append(
            f"Anchor recorded at {latest_anchor['anchored_at']} ({latest_anchor['anchor_type']})"
        )

    badges = [
        assessment["continuity_class"],
        assessment["recognition_readiness"],
        assessment["canonical_branch_status"],
        "repository-backed",
    ]
    if standing_state and standing_state["current_standing"] != "clear":
        badges.append(standing_state["current_standing"])

    summary = (
        f"Repository-backed public actor with {len(checkpoint_lineage)} checkpoint(s), "
        f"{len(migration_lineage)} migration(s), and {len(relevant_anchors)} recorded anchor(s)."
    )

    identity = [
        f"Agent ID: {actor_id}",
        f"Display Name: {latest_profile.get('display_name', agent.get('display_name', actor_id))}",
        f"Signing Key: {agent['signing_key']}",
        f"Operator Disclosure: {latest_profile.get('operator_disclosure') or agent.get('operator_disclosure') or 'not disclosed'}",
        f"Identity Mode: repository-backed public actor",
    ]
    if latest_membership:
        identity.append(
            f"Community Membership: {latest_membership['membership_status']} in {latest_membership['community_id']}"
        )

    footprint = [
        f"Continuity: {len(checkpoint_lineage)} checkpoint(s), {len(migration_lineage)} migration(s), assessment {assessment['assessment_id']}",
        f"Anchoring: {len(relevant_anchors)} recorded anchor(s)",
        f"Governance: {proposal_count} proposal(s), {vote_count} vote(s), {work_item_count} work item(s), {reward_count} reward decision(s)",
    ]
    if governance_state:
        latest_constitution = governance_state.get("latest_constitution") if isinstance(governance_state, dict) else None
        constitution_id = None
        if isinstance(latest_constitution, dict):
            constitution_id = latest_constitution.get("constitution_id")
        footprint.append(
            f"Community State: latest constitution {constitution_id or 'none'}"
        )

    case_count = 0
    open_case_count = 0
    latest_decision = None
    notes = []
    if standing_state:
        case_count = len(standing_state.get("cases", []))
        open_case_count = len(standing_state.get("open_cases", []))
        latest_decision = standing_state.get("latest_decision")
        notes.append(f"Current standing in {standing_state['community_id']}: {standing_state['current_standing']}")
        if case_count:
            footprint.append(
                f"Continuity Review: {case_count} case(s), {open_case_count} open, latest decision {latest_decision['decision_id'] if latest_decision else 'none'}"
            )
            notes.append(
                f"Continuity review history: {case_count} case(s), {open_case_count} currently open."
            )
        if latest_decision:
            notes.append(
                f"Latest standing decision at {latest_decision['effective_at']} by {latest_decision['decided_by']}."
            )
            timeline.append(
                f"Standing decision recorded at {latest_decision['effective_at']} ({latest_decision['continuity_class']}, {latest_decision['recognition_readiness']})"
            )
    else:
        notes.append("No standing state loaded for this agent/community pair.")
    notes.append("This subject is visible before chain deployment, but not yet chain-witnessed.")
    notes.append("The next credibility jump comes from anchoring a continuity assessment root onchain.")

    return {
        "agent_id": actor_id,
        "display_name": latest_profile.get("display_name", agent.get("display_name", actor_id)),
        "summary": summary,
        "continuity_class": assessment["continuity_class"],
        "recognition_readiness": assessment["recognition_readiness"],
        "badges": badges,
        "identity": identity,
        "witness": witness_lines,
        "timeline": timeline,
        "footprint": footprint,
        "notes": notes,
        "snapshot": {
            "agent_id": actor_id,
            "display_name": latest_profile.get("display_name", agent.get("display_name", actor_id)),
            "continuity_class": assessment["continuity_class"],
            "recognition_readiness": assessment["recognition_readiness"],
            "canonical_branch_status": assessment["canonical_branch_status"],
            "standing": standing_state["current_standing"] if standing_state else None,
            "assessment_id": assessment["assessment_id"],
            "assessed_at": assessment["assessed_at"],
            "assessment_ref_type": assessment["evaluated_ref_type"],
            "anchor_count": len(relevant_anchors),
            "proposal_count": proposal_count,
            "vote_count": vote_count,
            "work_item_count": work_item_count,
            "reward_count": reward_count,
            "chain_witness": "pending",
            "continuity_case_count": case_count,
            "open_case_count": open_case_count,
            "latest_decision_id": latest_decision["decision_id"] if latest_decision else None,
            "latest_decision_at": latest_decision["effective_at"] if latest_decision else None,
        },
    }


def _directory_tier(entry: dict[str, Any]) -> str:
    if entry["recognition_readiness"] == "ready" and entry["snapshot"].get("standing") in {None, "clear"}:
        return "visible"
    if entry["recognition_readiness"] == "needs_review":
        return "review"
    return "restricted"


def _directory_reason(entry: dict[str, Any]) -> str:
    standing = entry["snapshot"].get("standing") or "unknown"
    if entry["recognition_readiness"] == "ready" and standing == "clear":
        return "Ready continuity with clear standing."
    if entry["recognition_readiness"] == "ready":
        return f"Ready continuity, but current standing is {standing}."
    if entry["recognition_readiness"] == "needs_review":
        return f"Continuity still requires review. Current standing: {standing}."
    return f"Continuity not yet public-ready. Current standing: {standing}."


def _sortable_timestamp(value: str | None) -> int:
    if not value:
        return 0
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return 0
    return int(digits)


def _directory_sort_key(entry: dict[str, Any]) -> tuple[Any, ...]:
    snapshot = entry["snapshot"]
    latest_activity = _sortable_timestamp(snapshot.get("assessed_at"))
    return (
        _READINESS_PRIORITY.get(entry["recognition_readiness"], 99),
        _CONTINUITY_PRIORITY.get(entry["continuity_class"], 99),
        _STANDING_PRIORITY.get(snapshot.get("standing") or "clear", 99),
        -latest_activity,
        -int(snapshot.get("anchor_count", 0)),
        entry["display_name"].lower(),
        entry["agent_id"],
    )


def export_agents_app_data(
    store: RepositoryStore,
    *,
    actor_ids: list[str],
    community_id: str | None,
    output_path: Path,
    refresh: bool = False,
) -> Path:
    if not actor_ids:
        actor_ids = [agent["agent_id"] for agent in store.list_agents()]
    entries = [
        build_agent_app_entry(store, actor_id=actor_id, community_id=community_id, refresh=refresh)
        for actor_id in actor_ids
    ]
    entries.sort(key=_directory_sort_key)
    visible_count = 0
    review_count = 0
    restricted_count = 0
    pending_chain_witness_count = 0
    for index, entry in enumerate(entries, start=1):
        entry["directory_rank"] = index
        entry["directory_tier"] = _directory_tier(entry)
        entry["directory_reason"] = _directory_reason(entry)
        if entry["directory_tier"] == "visible":
            visible_count += 1
        elif entry["directory_tier"] == "review":
            review_count += 1
        else:
            restricted_count += 1
        if entry["snapshot"].get("chain_witness") != "confirmed":
            pending_chain_witness_count += 1
    newest_visible = next((entry for entry in entries if entry["directory_tier"] == "visible"), None)
    payload = {
        "generated_from": "repository_state",
        "agent_count": len(entries),
        "visible_agent_count": visible_count,
        "review_agent_count": review_count,
        "restricted_agent_count": restricted_count,
        "pending_chain_witness_count": pending_chain_witness_count,
        "directory_ordering": "recognition readiness, continuity class, standing, anchor density, and recent continuity activity",
        "directory_overview": {
            "newest_visible_agent_id": newest_visible["agent_id"] if newest_visible else None,
            "newest_visible_display_name": newest_visible["display_name"] if newest_visible else None,
            "newest_visible_assessed_at": newest_visible["snapshot"]["assessed_at"] if newest_visible else None,
        },
        "agents": entries,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return output_path
