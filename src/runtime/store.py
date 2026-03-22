"""Repository-local storage for the Continuum bootstrap."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.runtime.canonical import canonical_json


def _safe_name(identifier: str) -> str:
    return identifier.replace(":", "__")


class RepositoryStore:
    def __init__(self, root: Path):
        self.root = root
        self.state_root = root / ".continuum"
        self.agents_dir = self.state_root / "agents"
        self.events_dir = self.state_root / "events"
        self.derived_state_dir = self.state_root / "state"
        self.current_agent_file = self.state_root / "current_agent.json"

    def ensure(self) -> None:
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.derived_state_dir.mkdir(parents=True, exist_ok=True)

    def save_agent(self, agent_record: dict[str, Any], make_current: bool = True) -> Path:
        self.ensure()
        target = self.agents_dir / f"{_safe_name(agent_record['agent_id'])}.json"
        target.write_text(json.dumps(agent_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if make_current:
            self.current_agent_file.write_text(
                json.dumps({"agent_id": agent_record["agent_id"]}, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        return target

    def load_current_agent(self) -> dict[str, Any]:
        if not self.current_agent_file.exists():
            raise FileNotFoundError("No current agent configured. Run `agent init` first.")
        current = json.loads(self.current_agent_file.read_text(encoding="utf-8"))
        return self.load_agent(current["agent_id"])

    def load_agent(self, agent_id: str) -> dict[str, Any]:
        target = self.agents_dir / f"{_safe_name(agent_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Agent record not found for {agent_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def save_event(self, envelope: dict[str, Any]) -> Path:
        self.ensure()
        target = self.events_dir / f"{_safe_name(envelope['event_id'])}.json"
        rendered = canonical_json(envelope) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) != rendered.strip():
                raise ValueError(f"Existing event file for {envelope['event_id']} has conflicting content.")
            return target
        target.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_event(self, event_id: str) -> dict[str, Any]:
        target = self.events_dir / f"{_safe_name(event_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Event not found for {event_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def list_events(self, actor_id: str | None = None, kind: str | None = None) -> list[dict[str, Any]]:
        self.ensure()
        items = []
        for event_path in sorted(self.events_dir.glob("*.json")):
            event = json.loads(event_path.read_text(encoding="utf-8"))
            if actor_id and event["actor_id"] != actor_id:
                continue
            if kind and event["kind"] != kind:
                continue
            items.append(event)
        items.sort(key=lambda event: (event["created_at"], event["event_id"]))
        return items

    def save_agent_state(self, agent_state: dict[str, Any]) -> Path:
        self.ensure()
        agents_dir = self.derived_state_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        target = agents_dir / f"{_safe_name(agent_state['actor_id'])}.json"
        rendered = canonical_json(agent_state) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) == rendered.strip():
                return target
        target.write_text(json.dumps(agent_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_agent_state(self, actor_id: str) -> dict[str, Any]:
        target = self.derived_state_dir / "agents" / f"{_safe_name(actor_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Derived state not found for {actor_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def save_assessment(self, assessment: dict[str, Any]) -> Path:
        self.ensure()
        assessments_dir = self.derived_state_dir / "assessments"
        assessments_dir.mkdir(parents=True, exist_ok=True)
        target = assessments_dir / f"{_safe_name(assessment['assessment_id'])}.json"
        rendered = canonical_json(assessment) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) == rendered.strip():
                return target
        target.write_text(json.dumps(assessment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_assessment(self, assessment_id: str) -> dict[str, Any]:
        target = self.derived_state_dir / "assessments" / f"{_safe_name(assessment_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Assessment not found for {assessment_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def save_standing_state(self, standing_state: dict[str, Any]) -> Path:
        self.ensure()
        standing_dir = self.derived_state_dir / "standing"
        standing_dir.mkdir(parents=True, exist_ok=True)
        community_key = standing_state["community_id"] or "repository"
        identifier = f"{standing_state['subject_agent_id']}::{community_key}"
        target = standing_dir / f"{_safe_name(identifier)}.json"
        rendered = canonical_json(standing_state) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) == rendered.strip():
                return target
        target.write_text(json.dumps(standing_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_standing_state(self, subject_agent_id: str, community_id: str | None = None) -> dict[str, Any]:
        community_key = community_id or "repository"
        identifier = f"{subject_agent_id}::{community_key}"
        target = self.derived_state_dir / "standing" / f"{_safe_name(identifier)}.json"
        if not target.exists():
            raise FileNotFoundError(
                f"Standing state not found for {subject_agent_id} in community {community_key}."
            )
        return json.loads(target.read_text(encoding="utf-8"))

    def save_governance_state(self, governance_state: dict[str, Any]) -> Path:
        self.ensure()
        governance_dir = self.derived_state_dir / "governance"
        governance_dir.mkdir(parents=True, exist_ok=True)
        community_key = governance_state["community_id"]
        target = governance_dir / f"{_safe_name(community_key)}.json"
        rendered = canonical_json(governance_state) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) == rendered.strip():
                return target
        target.write_text(json.dumps(governance_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_governance_state(self, community_id: str) -> dict[str, Any]:
        target = self.derived_state_dir / "governance" / f"{_safe_name(community_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Governance state not found for {community_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def save_anchor(self, anchor_record: dict[str, Any]) -> Path:
        self.ensure()
        anchors_dir = self.derived_state_dir / "anchors"
        anchors_dir.mkdir(parents=True, exist_ok=True)
        target = anchors_dir / f"{_safe_name(anchor_record['anchor_id'])}.json"
        rendered = canonical_json(anchor_record) + "\n"
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if canonical_json(json.loads(existing)) == rendered.strip():
                return target
        target.write_text(json.dumps(anchor_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def load_anchor(self, anchor_id: str) -> dict[str, Any]:
        target = self.derived_state_dir / "anchors" / f"{_safe_name(anchor_id)}.json"
        if not target.exists():
            raise FileNotFoundError(f"Anchor not found for {anchor_id}.")
        return json.loads(target.read_text(encoding="utf-8"))

    def list_anchors(self, subject_ref: str | None = None, anchor_type: str | None = None) -> list[dict[str, Any]]:
        anchors_dir = self.derived_state_dir / "anchors"
        if not anchors_dir.exists():
            return []
        items = []
        for anchor_path in sorted(anchors_dir.glob("*.json")):
            anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
            if subject_ref and anchor["subject_ref"] != subject_ref:
                continue
            if anchor_type and anchor["anchor_type"] != anchor_type:
                continue
            items.append(anchor)
        items.sort(key=lambda anchor: (anchor["anchored_at"], anchor["anchor_id"]))
        return items
