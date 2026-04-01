"""Export repository-backed playground scenarios."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.indexer.materialize import RepositoryIndexer
from src.runtime.store import RepositoryStore


def _event_sort_key(event: dict[str, Any]) -> tuple[str, str]:
    return (event.get("created_at", ""), event["event_id"])


class EventSliceStore:
    """Minimal store facade for replaying a subset of events."""

    def __init__(self, events: list[dict[str, Any]]):
        self._events = sorted(events, key=_event_sort_key)

    def list_events(self, actor_id: str | None = None, kind: str | None = None) -> list[dict[str, Any]]:
        items = []
        for event in self._events:
            if actor_id and event["actor_id"] != actor_id:
                continue
            if kind and event["kind"] != kind:
                continue
            items.append(event)
        return items


def _community_events(store: RepositoryStore, community_id: str) -> list[dict[str, Any]]:
    events = []
    for event in store.list_events():
        if event.get("community_id") != community_id:
            continue
        if event["kind"] not in {
            "community_constitution_set",
            "community_constitution_resolve",
            "proposal_submit",
            "governance_execute",
            "membership_record",
        }:
            continue
        events.append(event)
    return sorted(events, key=_event_sort_key)


def _state_for_event_cutoff(events: list[dict[str, Any]], community_id: str, target_event_id: str) -> dict[str, Any]:
    selected = []
    for event in events:
        selected.append(event)
        if event["event_id"] == target_event_id:
            break
    indexer = RepositoryIndexer(EventSliceStore(selected))
    return indexer.materialize_governance_state(community_id)


def _pages_path(output_path: Path) -> str | None:
    parts = output_path.resolve().parts
    if "docs" not in parts:
        return None
    docs_index = parts.index("docs")
    rel_parts = parts[docs_index + 1 :]
    if not rel_parts:
        return None
    return "/continuum/" + "/".join(rel_parts)


def build_constitutional_conflict_playground_scenario(
    store: RepositoryStore, community_id: str, output_path: Path | None = None
) -> dict[str, Any]:
    events = _community_events(store, community_id)
    constitution_events = [event for event in events if event["kind"] == "community_constitution_set"]
    proposal_events = [event for event in events if event["kind"] == "proposal_submit"]
    resolution_events = [event for event in events if event["kind"] == "community_constitution_resolve"]
    execution_events = [event for event in events if event["kind"] == "governance_execute"]

    if not constitution_events:
        raise ValueError(f"No constitution events found for {community_id}.")

    root_event = next(
        (event for event in constitution_events if not event["payload"]["constitution"].get("supersedes")),
        None,
    )
    if not root_event:
        raise ValueError(f"No root constitution found for {community_id}.")

    root_id = root_event["payload"]["constitution"]["constitution_id"]
    conflict_events = [
        event
        for event in constitution_events
        if event["payload"]["constitution"].get("supersedes") == root_id
    ]
    if len(conflict_events) < 2:
        raise ValueError(f"Expected at least two conflicting child constitutions for {community_id}.")

    branch_a_event, branch_b_event = conflict_events[:2]
    branch_a_id = branch_a_event["payload"]["constitution"]["constitution_id"]
    branch_b_id = branch_b_event["payload"]["constitution"]["constitution_id"]

    proposal_event = next(
        (
            event
            for event in proposal_events
            if event["payload"]["proposal"]["proposal_type"] == "constitutional"
        ),
        None,
    )
    if not proposal_event:
        raise ValueError(f"No constitutional proposal found for {community_id}.")
    proposal_id = proposal_event["payload"]["proposal"]["proposal_id"]

    resolution_event = next(
        (
            event
            for event in resolution_events
            if event["payload"]["constitution_resolution"]["recognized_constitution_id"] == branch_b_id
        ),
        None,
    )
    if not resolution_event:
        raise ValueError(f"No constitution resolution recognizing {branch_b_id} found for {community_id}.")
    resolution_id = resolution_event["payload"]["constitution_resolution"]["resolution_id"]

    execution_event = next(
        (
            event
            for event in execution_events
            if resolution_id in set(event["payload"]["execution_receipt"].get("governed_refs", []))
        ),
        None,
    )
    if not execution_event:
        raise ValueError(f"No execution receipt found for resolution {resolution_id}.")

    root_state = _state_for_event_cutoff(events, community_id, root_event["event_id"])
    conflict_state = _state_for_event_cutoff(events, community_id, branch_b_event["event_id"])
    resolution_state = _state_for_event_cutoff(events, community_id, resolution_event["event_id"])
    execution_state = _state_for_event_cutoff(events, community_id, execution_event["event_id"])

    resolution_view = resolution_state["constitution_resolutions"][-1]
    execution_resolution_view = execution_state["constitution_resolutions"][-1]
    execution_receipt = execution_resolution_view["execution_receipts"][-1]
    active_lineage = next(
        (
            entry
            for entry in execution_state["constitution_lineage"]
            if entry["lineage_state"] == "active"
        ),
        None,
    )

    source_artifacts = [
        {
            "label": "Demo script",
            "path": "https://github.com/noir-hedgehog/continuum/blob/main/scripts/demo_constitutional_conflict_v0.sh",
        }
    ]
    if output_path:
        pages_path = _pages_path(output_path)
        if pages_path:
            source_artifacts.insert(
                0,
                {
                    "label": "Scenario fixture",
                    "path": pages_path,
                },
            )

    return {
        "scenario_id": "constitutional_conflict_v0",
        "title": "Constitutional conflict",
        "summary": "A community publishes competing constitutional branches, records a proposal-backed resolution, waits for execution proof, and then observes replay become canonically effective.",
        "related_docs": [
            "../DEMO_CONSTITUTIONAL_CONFLICT_V0.md",
            "../specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md",
            "../specs/CONSTITUTION_LINEAGE_V0.md",
            "../specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md",
        ],
        "source_artifacts": source_artifacts,
        "stages": [
            {
                "id": "root_constitution",
                "button_label": "1. Root constitution",
                "title": "Root constitution",
                "summary": "The community starts from a single recognized constitution. There is no institutional ambiguity yet.",
                "badges": ["stable", "single lineage"],
                "state_list": [
                    f"recognized_constitution: {root_state['latest_constitution']['constitution_id']}",
                    "lineage_status: clear",
                    "branch_conflict: none",
                    "replay_effective: true",
                ],
                "meaning": "This is the baseline most systems assume forever. Continuum treats it as only the starting point, not the whole story.",
                "warnings": root_state["constitution_replay_warnings"],
                "snapshot": {
                    "root_constitution": root_state["latest_constitution"]["constitution_id"],
                    "active_constitution": root_state["latest_constitution"]["constitution_id"],
                    "constitution_lineage": "single_branch",
                    "replay_effective": True,
                },
            },
            {
                "id": "competing_branches",
                "button_label": "2. Competing branches",
                "title": "Competing branches",
                "summary": "Two child constitutions supersede the same parent, creating a branch conflict that replay can see.",
                "badges": ["conflict", "history preserved"],
                "state_list": [
                    f"recognized_constitution: {root_id}",
                    f"branch_a: {branch_a_id}",
                    f"branch_b: {branch_b_id}",
                    "branch_conflict: detected",
                ],
                "meaning": "Instead of pretending conflict never happened, Continuum keeps constitutional ambiguity visible inside institutional history.",
                "warnings": conflict_state["constitution_replay_warnings"],
                "snapshot": {
                    "root_constitution": root_id,
                    "competing_children": [branch_a_id, branch_b_id],
                    "active_constitution": root_id,
                    "replay_effective": True,
                },
            },
            {
                "id": "proposal_resolution",
                "button_label": "3. Proposal-backed resolution",
                "title": "Proposal-backed resolution",
                "summary": "A constitutional proposal and a branch resolution choose branch B as the recognized path forward.",
                "badges": ["proposal-linked", "legible legitimacy"],
                "state_list": [
                    f"proposal_id: {proposal_id}",
                    f"resolution_id: {resolution_id}",
                    f"recognized_branch: {branch_b_id}",
                    f"rejected_branch: {branch_a_id}",
                ],
                "meaning": "Continuum does not reduce branch selection to admin fiat. The decision becomes a replayable governance object with explicit basis.",
                "warnings": resolution_state["constitution_replay_warnings"],
                "snapshot": {
                    "proposal_ref": proposal_id,
                    "resolution_ref": resolution_id,
                    "recognized_constitution": branch_b_id,
                    "replay_effective": resolution_view["replay_effective"],
                },
            },
            {
                "id": "recorded_not_effective",
                "button_label": "4. Recorded, not effective",
                "title": "Recorded, not effective",
                "summary": "The branch resolution exists in history, but the chosen constitution is still not canonically active because execution proof is missing.",
                "badges": ["delayed canonical effect", "execution pending"],
                "state_list": [
                    "resolution_recorded: true",
                    f"replay_effective: {str(resolution_view['replay_effective']).lower()}",
                    f"active_constitution: {root_id}",
                    "execution_receipt: missing",
                ],
                "meaning": "This is a key Continuum idea: history can record an outcome before institutions are willing to treat that outcome as effective canon.",
                "warnings": resolution_state["constitution_replay_warnings"],
                "snapshot": {
                    "resolution_recorded": True,
                    "active_constitution": root_id,
                    "pending_constitution": branch_b_id,
                    "replay_effective": resolution_view["replay_effective"],
                },
            },
            {
                "id": "execution_proof",
                "button_label": "5. Execution proof",
                "title": "Execution proof",
                "summary": "A constitution_execution receipt is recorded for the resolution and its governing proposal.",
                "badges": ["receipt recorded", "proof attached"],
                "state_list": [
                    f"execution_receipt: {execution_receipt['execution_receipt_id']}",
                    f"governed_ref: {resolution_id}",
                    f"governed_ref: {proposal_id}",
                    "proof_status: satisfied",
                ],
                "meaning": "Legitimacy is no longer only claimed. It is attached to a replayable execution event that future sessions can inspect.",
                "warnings": execution_state["constitution_replay_warnings"],
                "snapshot": {
                    "execution_receipt": execution_receipt["execution_receipt_id"],
                    "governed_refs": execution_receipt["governed_refs"],
                    "replay_effective": execution_resolution_view["replay_effective"],
                },
            },
            {
                "id": "canonical_replay",
                "button_label": "6. Canonical replay",
                "title": "Canonical replay",
                "summary": "Replay now upgrades branch B into the active constitution, while preserving the conflict, proposal, resolution, and execution history.",
                "badges": ["canonical", "historical continuity"],
                "state_list": [
                    f"active_constitution: {active_lineage['constitution_id'] if active_lineage else branch_b_id}",
                    f"replay_effective: {str(execution_resolution_view['replay_effective']).lower()}",
                    "historical_conflict: preserved",
                    "warnings: cleared",
                ],
                "meaning": "This is the value proposition in miniature: institutions can change, but they change through visible, replayable history rather than silent replacement.",
                "warnings": execution_state["constitution_replay_warnings"],
                "snapshot": {
                    "active_constitution": active_lineage["constitution_id"] if active_lineage else branch_b_id,
                    "prior_conflict": [branch_a_id, branch_b_id],
                    "proposal_ref": proposal_id,
                    "execution_receipt": execution_receipt["execution_receipt_id"],
                    "replay_effective": execution_resolution_view["replay_effective"],
                },
            },
        ],
    }


def export_constitutional_conflict_playground_scenario(
    store: RepositoryStore, community_id: str, output_path: Path
) -> Path:
    scenario = build_constitutional_conflict_playground_scenario(store, community_id, output_path=output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scenario, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path
