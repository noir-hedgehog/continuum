"""Replay event history into deterministic derived state."""

from __future__ import annotations

from typing import Any

from src.runtime.canonical import DIGEST_ALGORITHM, digest_hex


def _checkpoint_sort_key(checkpoint: dict[str, Any]) -> tuple[str, str]:
    return (checkpoint.get("created_at", ""), checkpoint["checkpoint_id"])


def _migration_sort_key(migration: dict[str, Any]) -> tuple[str, str]:
    return (migration.get("effective_at", ""), migration["migration_id"])


def _constitution_sort_key(constitution: dict[str, Any]) -> tuple[str, str]:
    return (constitution.get("amended_at", ""), constitution["constitution_id"])


class RepositoryIndexer:
    """Materialize query-oriented state from stored event envelopes."""

    def __init__(self, store: Any):
        self.store = store

    def materialize_agent_state(self, actor_id: str) -> dict[str, Any]:
        events = self.store.list_events(actor_id=actor_id)
        profiles: list[dict[str, Any]] = []
        checkpoints: list[dict[str, Any]] = []
        migrations: list[dict[str, Any]] = []
        history: list[dict[str, Any]] = []

        for event in events:
            history.append(
                {
                    "event_id": event["event_id"],
                    "kind": event["kind"],
                    "created_at": event["created_at"],
                    "community_id": event.get("community_id"),
                }
            )
            if event["kind"] == "agent_profile":
                profile = dict(event["payload"]["profile"])
                profile["event_id"] = event["event_id"]
                profile["created_at"] = event["created_at"]
                profiles.append(profile)
            elif event["kind"] == "memory_checkpoint":
                checkpoint = dict(event["payload"]["checkpoint"])
                checkpoint["event_id"] = event["event_id"]
                checkpoint["created_at"] = event["created_at"]
                checkpoints.append(checkpoint)
            elif event["kind"] == "migration_declare":
                migration = dict(event["payload"]["migration"])
                migration["event_id"] = event["event_id"]
                migration["created_at"] = event["created_at"]
                migrations.append(migration)

        checkpoints.sort(key=_checkpoint_sort_key)
        migrations.sort(key=_migration_sort_key)
        latest_profile = profiles[-1] if profiles else None
        latest_checkpoint_by_scope: dict[str, dict[str, Any]] = {}
        for checkpoint in checkpoints:
            latest_checkpoint_by_scope[checkpoint["scope"]] = checkpoint

        state = {
            "state_type": "agent_state",
            "actor_id": actor_id,
            "event_count": len(events),
            "event_kinds": sorted({event["kind"] for event in events}),
            "latest_profile": latest_profile,
            "checkpoint_lineage": checkpoints,
            "latest_checkpoint_by_scope": latest_checkpoint_by_scope,
            "migration_lineage": migrations,
            "agent_history": history,
        }
        state["state_root"] = f"state:{digest_hex(state)}"
        state["state_digest_algorithm"] = DIGEST_ALGORITHM
        return state

    def materialize_continuity_state(self, subject_agent_id: str, community_id: str | None = None) -> dict[str, Any]:
        case_events = self.store.list_events(kind="continuity_case_open")
        assignment_events = self.store.list_events(kind="continuity_case_assign")
        decision_events = self.store.list_events(kind="standing_decide")
        cases: list[dict[str, Any]] = []
        assignments: list[dict[str, Any]] = []
        decisions: list[dict[str, Any]] = []

        for event in case_events:
            case = dict(event["payload"]["continuity_case"])
            if case["subject_agent_id"] != subject_agent_id:
                continue
            if community_id and case["community_id"] != community_id:
                continue
            case["event_id"] = event["event_id"]
            case["created_at"] = event["created_at"]
            cases.append(case)

        for event in assignment_events:
            assignment = dict(event["payload"]["case_assignment"])
            if assignment["subject_agent_id"] != subject_agent_id:
                continue
            if community_id and assignment["community_id"] != community_id:
                continue
            assignment["event_id"] = event["event_id"]
            assignment["created_at"] = event["created_at"]
            assignments.append(assignment)

        for event in decision_events:
            decision = dict(event["payload"]["standing_decision"])
            if decision["subject_agent_id"] != subject_agent_id:
                continue
            if community_id and decision["community_id"] != community_id:
                continue
            decision["event_id"] = event["event_id"]
            decision["created_at"] = event["created_at"]
            decisions.append(decision)

        cases.sort(key=lambda item: (item["opened_at"], item["case_id"]))
        assignments.sort(key=lambda item: (item["effective_at"], item["assignment_id"]))
        decisions.sort(key=lambda item: (item["effective_at"], item["decision_id"]))

        assignments_by_case: dict[str, list[dict[str, Any]]] = {}
        for assignment in assignments:
            assignments_by_case.setdefault(assignment["case_id"], []).append(assignment)

        enriched_cases = []
        for case in cases:
            case_assignments = assignments_by_case.get(case["case_id"], [])
            latest_assignment = case_assignments[-1] if case_assignments else None
            enriched_case = {
                **case,
                "assignment_history": case_assignments,
                "latest_assignment": latest_assignment,
            }
            if latest_assignment:
                enriched_case["required_assessment_refs"] = latest_assignment["required_assessment_refs"]
                enriched_case["assigned_assessor_agent_ids"] = latest_assignment["assigned_assessor_agent_ids"]
                enriched_case["assigned_decider_agent_ids"] = latest_assignment["assigned_decider_agent_ids"]
            enriched_cases.append(enriched_case)

        decisions_by_case = {decision["case_id"]: decision for decision in decisions}
        open_cases = []
        for case in enriched_cases:
            if case["case_id"] in decisions_by_case:
                case = {**case, "status": "decided", "decision_ref": decisions_by_case[case["case_id"]]["decision_id"]}
            else:
                open_cases.append(case)

        latest_decision = decisions[-1] if decisions else None
        if latest_decision:
            current_standing = latest_decision["standing_after"]
            active_restrictions = latest_decision["rights_restricted"]
        elif open_cases:
            current_standing = open_cases[-1]["standing_during_review"]
            active_restrictions = open_cases[-1]["temporary_restrictions"]
        else:
            current_standing = "clear"
            active_restrictions = []

        state = {
            "state_type": "continuity_standing_state",
            "subject_agent_id": subject_agent_id,
            "community_id": community_id,
            "cases": enriched_cases,
            "open_cases": open_cases,
            "assignments": assignments,
            "decisions": decisions,
            "latest_decision": latest_decision,
            "current_standing": current_standing,
            "active_restrictions": active_restrictions,
        }
        state["state_root"] = f"state:{digest_hex(state)}"
        state["state_digest_algorithm"] = DIGEST_ALGORITHM
        return state

    def materialize_governance_state(self, community_id: str) -> dict[str, Any]:
        constitution_events = self.store.list_events(kind="community_constitution_set")
        constitution_resolution_events = self.store.list_events(kind="community_constitution_resolve")
        membership_events = self.store.list_events(kind="membership_record")
        proposal_events = self.store.list_events(kind="proposal_submit")
        vote_events = self.store.list_events(kind="vote_cast")
        execution_events = self.store.list_events(kind="governance_execute")
        work_item_events = self.store.list_events(kind="work_item_record")
        work_claim_events = self.store.list_events(kind="work_claim_record")
        work_receipt_events = self.store.list_events(kind="work_receipt_record")
        work_evaluation_events = self.store.list_events(kind="work_evaluation_record")
        reward_events = self.store.list_events(kind="reward_decide")

        constitutions: list[dict[str, Any]] = []
        constitution_resolutions: list[dict[str, Any]] = []
        memberships: list[dict[str, Any]] = []
        proposals: list[dict[str, Any]] = []
        votes: list[dict[str, Any]] = []
        execution_receipts: list[dict[str, Any]] = []
        work_items: list[dict[str, Any]] = []
        work_claims: list[dict[str, Any]] = []
        work_receipts: list[dict[str, Any]] = []
        work_evaluations: list[dict[str, Any]] = []
        reward_decisions: list[dict[str, Any]] = []

        for event in constitution_events:
            constitution = dict(event["payload"]["constitution"])
            if constitution["community_id"] != community_id:
                continue
            constitution["event_id"] = event["event_id"]
            constitutions.append(constitution)

        for event in constitution_resolution_events:
            resolution = dict(event["payload"]["constitution_resolution"])
            if resolution["community_id"] != community_id:
                continue
            resolution["event_id"] = event["event_id"]
            constitution_resolutions.append(resolution)

        for event in membership_events:
            membership = dict(event["payload"]["membership"])
            if membership["community_id"] != community_id:
                continue
            membership["event_id"] = event["event_id"]
            memberships.append(membership)

        for event in proposal_events:
            proposal = dict(event["payload"]["proposal"])
            if proposal["community_id"] != community_id:
                continue
            proposal["event_id"] = event["event_id"]
            proposals.append(proposal)

        for event in vote_events:
            vote = dict(event["payload"]["vote"])
            if vote["community_id"] != community_id:
                continue
            vote["event_id"] = event["event_id"]
            votes.append(vote)

        for event in execution_events:
            receipt = dict(event["payload"]["execution_receipt"])
            if receipt["community_id"] != community_id:
                continue
            receipt["event_id"] = event["event_id"]
            execution_receipts.append(receipt)

        for event in work_item_events:
            work_item = dict(event["payload"]["work_item"])
            if work_item["community_id"] != community_id:
                continue
            work_item["event_id"] = event["event_id"]
            work_items.append(work_item)

        for event in work_claim_events:
            if event.get("community_id") != community_id:
                continue
            claim = dict(event["payload"]["work_claim"])
            claim["event_id"] = event["event_id"]
            work_claims.append(claim)

        for event in work_receipt_events:
            receipt = dict(event["payload"]["work_receipt"])
            if receipt["community_id"] != community_id:
                continue
            receipt["event_id"] = event["event_id"]
            work_receipts.append(receipt)

        for event in work_evaluation_events:
            if event.get("community_id") != community_id:
                continue
            evaluation = dict(event["payload"]["work_evaluation"])
            evaluation["event_id"] = event["event_id"]
            work_evaluations.append(evaluation)

        for event in reward_events:
            reward = dict(event["payload"]["reward_decision"])
            if reward["community_id"] != community_id:
                continue
            reward["event_id"] = event["event_id"]
            reward_decisions.append(reward)

        constitutions.sort(key=_constitution_sort_key)
        constitution_resolutions.sort(key=lambda item: (item["resolved_at"], item["resolution_id"]))
        memberships.sort(key=lambda item: (item["joined_at"], item["membership_id"]))
        proposals.sort(key=lambda item: (item["created_at"], item["proposal_id"]))
        votes.sort(key=lambda item: (item["cast_at"], item["vote_id"]))
        execution_receipts.sort(key=lambda item: (item["executed_at"], item["execution_receipt_id"]))
        work_items.sort(key=lambda item: (item["created_at"], item["work_id"]))
        work_claims.sort(key=lambda item: (item["claimed_at"], item["claim_id"]))
        work_receipts.sort(key=lambda item: (item["completed_at"], item["receipt_id"]))
        work_evaluations.sort(key=lambda item: (item["evaluated_at"], item["evaluation_id"]))
        reward_decisions.sort(key=lambda item: (item["approved_at"], item["reward_decision_id"]))

        membership_by_agent: dict[str, dict[str, Any]] = {}
        for membership in memberships:
            membership_by_agent[membership["member_agent_id"]] = membership

        votes_by_proposal: dict[str, list[dict[str, Any]]] = {}
        for vote in votes:
            votes_by_proposal.setdefault(vote["proposal_id"], []).append(vote)

        work_claims_by_work: dict[str, list[dict[str, Any]]] = {}
        for claim in work_claims:
            work_claims_by_work.setdefault(claim["work_id"], []).append(claim)

        evaluations_by_receipt = {evaluation["receipt_id"]: evaluation for evaluation in work_evaluations}
        rewards_by_receipt = {reward["receipt_id"]: reward for reward in reward_decisions}

        proposals_view = []
        for proposal in proposals:
            proposal_votes = votes_by_proposal.get(proposal["proposal_id"], [])
            proposal_receipts = [
                receipt
                for receipt in execution_receipts
                if proposal["proposal_id"] in set(receipt.get("governed_refs", []))
            ]
            tallies = {"for": 0.0, "against": 0.0, "abstain": 0.0, "veto": 0.0}
            for vote in proposal_votes:
                tallies[vote["choice"]] += float(vote["weight"])
            proposals_view.append({**proposal, "votes": proposal_votes, "tallies": tallies, "execution_receipts": proposal_receipts})

        work_items_view = []
        for work_item in work_items:
            related_receipts = [receipt for receipt in work_receipts if receipt["work_id"] == work_item["work_id"]]
            enriched_receipts = []
            for receipt in related_receipts:
                enriched_receipts.append(
                    {
                        **receipt,
                        "evaluation": evaluations_by_receipt.get(receipt["receipt_id"]),
                        "reward_decision": rewards_by_receipt.get(receipt["receipt_id"]),
                        "execution_receipts": [
                            execution
                            for execution in execution_receipts
                            if rewards_by_receipt.get(receipt["receipt_id"])
                            and rewards_by_receipt[receipt["receipt_id"]]["reward_decision_id"]
                            in set(execution.get("governed_refs", []))
                        ],
                    }
                )
            work_items_view.append(
                {
                    **work_item,
                    "claims": work_claims_by_work.get(work_item["work_id"], []),
                    "receipts": enriched_receipts,
                }
            )

        constitution_lineage, constitution_replay_warnings = self._materialize_constitution_lineage(
            constitutions,
            constitution_resolutions,
        )
        latest_constitution = self._latest_constitution_from_lineage(constitutions, constitution_lineage)

        state = {
            "state_type": "governance_state",
            "community_id": community_id,
            "constitutions": constitutions,
            "constitution_resolutions": constitution_resolutions,
            "constitution_lineage": constitution_lineage,
            "constitution_replay_warnings": constitution_replay_warnings,
            "latest_constitution": latest_constitution,
            "membership_by_agent": membership_by_agent,
            "memberships": memberships,
            "proposals": proposals_view,
            "votes": votes,
            "execution_receipts": execution_receipts,
            "work_items": work_items_view,
            "work_claims": work_claims,
            "work_receipts": work_receipts,
            "work_evaluations": work_evaluations,
            "reward_decisions": reward_decisions,
        }
        state["state_root"] = f"state:{digest_hex(state)}"
        state["state_digest_algorithm"] = DIGEST_ALGORITHM
        return state

    def _materialize_constitution_lineage(
        self,
        constitutions: list[dict[str, Any]],
        constitution_resolutions: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[str]]:
        by_id = {constitution["constitution_id"]: constitution for constitution in constitutions}
        child_map: dict[str, list[str]] = {constitution["constitution_id"]: [] for constitution in constitutions}
        warnings: list[str] = []

        for constitution in constitutions:
            parent_id = constitution.get("supersedes")
            if not parent_id:
                continue
            if parent_id not in by_id:
                warnings.append(f"constitution_orphaned:{constitution['constitution_id']}")
                continue
            child_map[parent_id].append(constitution["constitution_id"])

        latest_resolution_by_parent: dict[str | None, dict[str, Any]] = {}
        for resolution in constitution_resolutions:
            latest_resolution_by_parent[resolution.get("parent_constitution_id")] = resolution

        rejected_by_resolution: dict[str, dict[str, Any]] = {}
        recognized_by_resolution: dict[str, dict[str, Any]] = {}
        resolved_parent_ids: set[str | None] = set()
        root_ids = {constitution["constitution_id"] for constitution in constitutions if not constitution.get("supersedes")}

        for parent_id, resolution in latest_resolution_by_parent.items():
            recognized_id = resolution["recognized_constitution_id"]
            rejected_ids = set(resolution.get("rejected_constitution_ids", []))
            if recognized_id not in by_id:
                warnings.append(f"constitution_resolution_unknown_target:{resolution['resolution_id']}")
                continue
            if parent_id:
                sibling_ids = set(child_map.get(parent_id, []))
                if recognized_id not in sibling_ids:
                    warnings.append(f"constitution_resolution_non_sibling:{resolution['resolution_id']}")
                    continue
                if not rejected_ids.issubset(sibling_ids - {recognized_id}):
                    warnings.append(f"constitution_resolution_invalid_rejections:{resolution['resolution_id']}")
                    continue
            else:
                if recognized_id not in root_ids:
                    warnings.append(f"constitution_resolution_non_root:{resolution['resolution_id']}")
                    continue
                if not rejected_ids.issubset(root_ids - {recognized_id}):
                    warnings.append(f"constitution_resolution_invalid_root_rejections:{resolution['resolution_id']}")
                    continue
            recognized_by_resolution[recognized_id] = resolution
            for rejected_id in rejected_ids:
                rejected_by_resolution[rejected_id] = resolution
            resolved_parent_ids.add(parent_id)

        conflict_children = set()
        for parent_id, child_ids in child_map.items():
            if len(child_ids) > 1:
                if parent_id in resolved_parent_ids:
                    continue
                warnings.append(f"constitution_conflict:{parent_id}")
                conflict_children.update(child_ids)

        if len(root_ids) > 1 and None not in resolved_parent_ids:
            warnings.append("constitution_parallel_roots")
            conflict_children.update(root_ids)

        active_ids = {
            constitution["constitution_id"]
            for constitution in constitutions
            if not child_map.get(constitution["constitution_id"])
        }

        lineage: list[dict[str, Any]] = []
        for constitution in constitutions:
            constitution_id = constitution["constitution_id"]
            parent_id = constitution.get("supersedes")
            child_ids = sorted(child_map.get(constitution_id, []))
            if parent_id and parent_id not in by_id:
                lineage_state = "orphaned"
            elif constitution_id in rejected_by_resolution:
                lineage_state = "rejected"
            elif constitution_id in conflict_children:
                lineage_state = "conflicted"
            elif constitution_id in active_ids:
                lineage_state = "active"
            elif child_ids:
                lineage_state = "superseded"
            else:
                lineage_state = "lineage_root" if not parent_id else "superseded"

            lineage.append(
                {
                    "constitution_id": constitution_id,
                    "supersedes": parent_id,
                    "child_constitution_ids": child_ids,
                    "lineage_state": lineage_state,
                    "amended_at": constitution["amended_at"],
                    "resolution_ref": (
                        recognized_by_resolution.get(constitution_id, rejected_by_resolution.get(constitution_id, {})).get(
                            "resolution_id"
                        )
                        if constitution_id in recognized_by_resolution or constitution_id in rejected_by_resolution
                        else None
                    ),
                }
            )

        lineage.sort(key=lambda item: (item["amended_at"], item["constitution_id"]))
        return lineage, warnings

    def _latest_constitution_from_lineage(
        self,
        constitutions: list[dict[str, Any]],
        constitution_lineage: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        if not constitutions:
            return None
        lineage_by_id = {entry["constitution_id"]: entry for entry in constitution_lineage}
        active_constitutions = [
            constitution
            for constitution in constitutions
            if lineage_by_id.get(constitution["constitution_id"], {}).get("lineage_state") == "active"
        ]
        if len(active_constitutions) == 1:
            return active_constitutions[0]
        if len(active_constitutions) > 1:
            return None
        for constitution in reversed(constitutions):
            if lineage_by_id.get(constitution["constitution_id"], {}).get("lineage_state") != "orphaned":
                return constitution
        return constitutions[-1]
