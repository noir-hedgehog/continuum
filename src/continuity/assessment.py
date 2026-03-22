"""Deterministic local continuity assessment for the Continuum bootstrap."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.runtime.canonical import digest_hex
from src.runtime.events import utc_now


CATEGORY_WEIGHTS = {
    "authority_continuity": 0.30,
    "memory_lineage": 0.20,
    "mission_and_charter_continuity": 0.15,
    "execution_lineage": 0.15,
    "social_recognition": 0.10,
    "branch_coherence": 0.10,
}

REPOSITORY_ARTIFACTS = {
    "founding_thesis_present": "docs/FOUNDING_THESIS.md",
    "operating_model_present": "docs/OPERATING_MODEL.md",
    "task_board_present": "docs/TASK_BOARD.md",
    "revision_log_present": "docs/REVISION_LOG.md",
}


@dataclass
class AssessmentContext:
    actor_id: str
    agent_record: dict[str, Any]
    state: dict[str, Any]
    evaluated_event: dict[str, Any] | None
    evaluated_ref: str
    evaluated_ref_type: str
    scope: str


class ContinuityAssessmentEngine:
    """Apply the v0 continuity assessment workflow to repository-local state."""

    def __init__(self, store: Any):
        self.store = store

    def assess(
        self,
        *,
        actor_id: str,
        scope: str = "repository",
        event_id: str | None = None,
        refresh: bool = False,
        assessor_type: str = "runtime",
        assessor_agent_id: str | None = None,
    ) -> dict[str, Any]:
        agent_record = self.store.load_agent(actor_id)
        state = self._load_agent_state(actor_id, refresh=refresh)
        evaluated_event = self._resolve_evaluated_event(actor_id=actor_id, event_id=event_id)
        context = AssessmentContext(
            actor_id=actor_id,
            agent_record=agent_record,
            state=state,
            evaluated_event=evaluated_event,
            evaluated_ref=self._evaluated_ref(evaluated_event, actor_id),
            evaluated_ref_type=self._evaluated_ref_type(evaluated_event),
            scope=scope,
        )
        result = self._build_assessment(
            context=context,
            assessor_type=assessor_type,
            assessor_agent_id=assessor_agent_id,
        )
        self.store.save_assessment(result)
        return result

    def _load_agent_state(self, actor_id: str, refresh: bool) -> dict[str, Any]:
        if not refresh:
            try:
                return self.store.load_agent_state(actor_id)
            except FileNotFoundError:
                pass
        from src.indexer.materialize import RepositoryIndexer

        indexer = RepositoryIndexer(self.store)
        state = indexer.materialize_agent_state(actor_id)
        self.store.save_agent_state(state)
        return state

    def _resolve_evaluated_event(self, *, actor_id: str, event_id: str | None) -> dict[str, Any] | None:
        if event_id:
            event = self.store.load_event(event_id)
            if event["actor_id"] != actor_id:
                raise ValueError(f"Event {event_id} does not belong to actor {actor_id}.")
            return event
        migrations = self.store.list_events(actor_id=actor_id, kind="migration_declare")
        if migrations:
            return migrations[-1]
        checkpoints = self.store.list_events(actor_id=actor_id, kind="memory_checkpoint")
        if checkpoints:
            return checkpoints[-1]
        profiles = self.store.list_events(actor_id=actor_id, kind="agent_profile")
        if profiles:
            return profiles[-1]
        return None

    def _evaluated_ref(self, event: dict[str, Any] | None, actor_id: str) -> str:
        if event is None:
            return actor_id
        payload = event["payload"]
        if event["kind"] == "migration_declare":
            return payload["migration"]["migration_id"]
        if event["kind"] == "memory_checkpoint":
            return payload["checkpoint"]["checkpoint_id"]
        if event["kind"] == "agent_profile":
            return payload["profile"]["agent_id"]
        return event["event_id"]

    def _evaluated_ref_type(self, event: dict[str, Any] | None) -> str:
        if event is None:
            return "repository"
        if event["kind"] == "migration_declare":
            migration_type = event["payload"]["migration"]["migration_type"]
            if migration_type == "session_restart":
                return "session_restart"
            return "migration"
        if event["kind"] == "memory_checkpoint":
            return "checkpoint"
        return "agent_profile"

    def _build_assessment(
        self,
        *,
        context: AssessmentContext,
        assessor_type: str,
        assessor_agent_id: str | None,
    ) -> dict[str, Any]:
        supporting_evidence: list[str] = []
        blocking_issues: list[str] = []
        required_followups: list[str] = []

        artifact_presence = {
            evidence_key: (self.store.root / relative_path).exists()
            for evidence_key, relative_path in REPOSITORY_ARTIFACTS.items()
        }
        if artifact_presence["task_board_present"]:
            supporting_evidence.append("task_board_updated")
        if artifact_presence["revision_log_present"]:
            supporting_evidence.append("revision_log_updated")
        if artifact_presence["founding_thesis_present"] and artifact_presence["operating_model_present"]:
            supporting_evidence.append("repository_reconstruction_complete")
            supporting_evidence.append("same_authority_constraints")
            supporting_evidence.append("active_spec_lineage_preserved")

        latest_profile = context.state.get("latest_profile")
        authority_score = 1.0 if context.agent_record.get("signing_key") and latest_profile else 0.0
        if authority_score:
            supporting_evidence.append("valid_continuity_authority")
        else:
            blocking_issues.append("continuity_authority_missing")

        checkpoint_count = len(context.state.get("checkpoint_lineage", []))
        memory_score = min(1.0, 0.35 + (0.25 * checkpoint_count))
        if checkpoint_count:
            supporting_evidence.append("checkpoint_chain_present")
        else:
            blocking_issues.append("checkpoint_chain_missing")

        mission_score = 1.0 if all(artifact_presence.values()) else 0.45
        if mission_score < 1.0:
            blocking_issues.append("repository_continuity_bundle_incomplete")

        event_count = context.state.get("event_count", 0)
        execution_score = min(1.0, 0.25 + (0.15 * event_count))
        if event_count >= 2:
            supporting_evidence.append("execution_lineage_present")
        else:
            blocking_issues.append("execution_lineage_thin")

        social_score = 0.35
        if context.agent_record.get("operator_disclosure"):
            social_score = 0.55
            supporting_evidence.append("operator_disclosure_stable")
        elif context.evaluated_event and context.evaluated_event.get("community_id"):
            social_score = 0.50
            supporting_evidence.append("community_scope_declared")

        branch_score = 1.0
        canonical_branch_status = "canonical"
        migration = None
        if context.evaluated_event and context.evaluated_event["kind"] == "migration_declare":
            migration = context.evaluated_event["payload"]["migration"]
            migration_type = migration["migration_type"]
            if migration_type in {"agent_split", "agent_merge"}:
                branch_score = 0.25
                canonical_branch_status = "fork_detected"
                blocking_issues.append("canonical_branch_selection_required")
                required_followups.append("select_canonical_branch")

        max_class = "same_agent"
        if migration:
            migration_type = migration["migration_type"]
            if migration_type in {"operator_change", "memory_rewrite"}:
                max_class = "successor_agent"
                blocking_issues.append("strict_identity_preservation_not_met")
            elif migration_type == "key_rotation":
                supporting_evidence.append("declared_key_rotation")
            elif migration_type == "session_restart":
                supporting_evidence.append("session_restart_declared")
                if all(artifact_presence.values()) and checkpoint_count and event_count >= 3:
                    memory_score = max(memory_score, 0.9)
                    execution_score = max(execution_score, 0.9)
            elif migration_type == "memory_restore":
                supporting_evidence.append("memory_restore_declared")

        score = round(
            (authority_score * CATEGORY_WEIGHTS["authority_continuity"])
            + (memory_score * CATEGORY_WEIGHTS["memory_lineage"])
            + (mission_score * CATEGORY_WEIGHTS["mission_and_charter_continuity"])
            + (execution_score * CATEGORY_WEIGHTS["execution_lineage"])
            + (social_score * CATEGORY_WEIGHTS["social_recognition"])
            + (branch_score * CATEGORY_WEIGHTS["branch_coherence"]),
            2,
        )

        continuity_class = self._select_class(
            authority_score=authority_score,
            branch_score=branch_score,
            blocking_issues=blocking_issues,
            score=score,
            max_class=max_class,
        )
        confidence_band = self._confidence_band(score)
        recognition_readiness = self._recognition_readiness(
            continuity_class=continuity_class,
            confidence_band=confidence_band,
            blocking_issues=blocking_issues,
        )

        assessment_source = {
            "actor_id": context.actor_id,
            "evaluated_ref": context.evaluated_ref,
            "scope": context.scope,
            "continuity_class": continuity_class,
            "score": score,
            "assessor_type": assessor_type,
            "assessor_agent_id": assessor_agent_id,
        }
        assessment_id = f"assessment:{digest_hex(assessment_source)[:16]}"
        return {
            "assessment_id": assessment_id,
            "subject_agent_id": context.actor_id,
            "assessed_by_agent_id": assessor_agent_id,
            "evaluated_ref": context.evaluated_ref,
            "evaluated_ref_type": context.evaluated_ref_type,
            "scope": context.scope,
            "continuity_class": continuity_class,
            "confidence_score": score,
            "confidence_band": confidence_band,
            "recognition_readiness": recognition_readiness,
            "canonical_branch_status": canonical_branch_status,
            "blocking_issues": sorted(set(blocking_issues)),
            "supporting_evidence": sorted(set(supporting_evidence)),
            "required_followups": sorted(set(required_followups)),
            "assessed_at": utc_now(),
            "assessor_type": assessor_type,
        }

    def _select_class(
        self,
        *,
        authority_score: float,
        branch_score: float,
        blocking_issues: list[str],
        score: float,
        max_class: str,
    ) -> str:
        if authority_score == 0.0:
            return "unrecognized"
        if branch_score < 0.5:
            return "forked_agent"
        if max_class == "successor_agent":
            return "successor_agent"
        if score >= 0.85:
            return "same_agent"
        if score >= 0.60:
            return "successor_agent"
        if "repository_continuity_bundle_incomplete" in blocking_issues:
            return "unrecognized"
        return "successor_agent"

    def _confidence_band(self, score: float) -> str:
        if score >= 0.85:
            return "high"
        if score >= 0.60:
            return "medium"
        return "low"

    def _recognition_readiness(
        self,
        *,
        continuity_class: str,
        confidence_band: str,
        blocking_issues: list[str],
    ) -> str:
        if continuity_class in {"unrecognized", "revoked"} or confidence_band == "low":
            return "not_ready"
        if continuity_class == "same_agent" and confidence_band == "high" and not blocking_issues:
            return "ready"
        return "needs_review"
