"""Replaceable local anchor export helpers."""

from __future__ import annotations

from typing import Any

from src.runtime.canonical import DIGEST_ALGORITHM, digest_hex
from src.runtime.events import utc_now


ANCHOR_TYPES = {
    "continuity_assessment_root",
    "agent_state_root",
    "standing_state_root",
    "governance_state_root",
}


def build_anchor_record(
    *,
    anchor_type: str,
    subject_ref: str,
    root_hash: str,
    anchor_target: str,
    anchored_at: str | None = None,
) -> dict[str, Any]:
    anchored_at_value = anchored_at or utc_now()
    anchor_source = {
        "anchor_type": anchor_type,
        "subject_ref": subject_ref,
        "root_hash": root_hash,
        "anchor_target": anchor_target,
        "anchored_at": anchored_at_value,
    }
    return {
        "anchor_id": f"anchor:{digest_hex(anchor_source)[:16]}",
        "anchor_type": anchor_type,
        "subject_ref": subject_ref,
        "root_hash": root_hash,
        "anchored_at": anchored_at_value,
        "anchor_target": anchor_target,
        "anchor_digest_algorithm": DIGEST_ALGORITHM,
    }


class LocalAnchorAdapter:
    """Reference adapter that records local witness anchors in-repository."""

    def __init__(self, target_name: str = "local_witness_v0"):
        self.target_name = target_name

    def export(
        self,
        *,
        anchor_type: str,
        subject_ref: str,
        root_hash: str,
        anchored_at: str | None = None,
    ) -> dict[str, Any]:
        return build_anchor_record(
            anchor_type=anchor_type,
            subject_ref=subject_ref,
            root_hash=root_hash,
            anchor_target=f"adapter:{self.target_name}",
            anchored_at=anchored_at,
        )
