"""Replaceable anchor export helpers."""

from __future__ import annotations

from dataclasses import dataclass
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
    anchor_status: str = "confirmed_external",
    anchored_at: str | None = None,
    external_reference: str | None = None,
    target_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    anchored_at_value = anchored_at or utc_now()
    anchor_source = {
        "anchor_type": anchor_type,
        "subject_ref": subject_ref,
        "root_hash": root_hash,
        "anchor_target": anchor_target,
        "anchor_status": anchor_status,
        "anchored_at": anchored_at_value,
        "external_reference": external_reference,
        "target_metadata": target_metadata or {},
    }
    record = {
        "anchor_id": f"anchor:{digest_hex(anchor_source)[:16]}",
        "anchor_type": anchor_type,
        "subject_ref": subject_ref,
        "root_hash": root_hash,
        "anchored_at": anchored_at_value,
        "anchor_target": anchor_target,
        "anchor_status": anchor_status,
        "anchor_digest_algorithm": DIGEST_ALGORITHM,
    }
    if external_reference is not None:
        record["external_reference"] = external_reference
    if target_metadata:
        record["target_metadata"] = target_metadata
    return record


@dataclass
class AnchorExportRequest:
    anchor_type: str
    subject_ref: str
    root_hash: str
    anchored_at: str | None = None


class AnchorAdapter:
    """Thin adapter boundary for local and future external anchor targets."""

    target_name: str

    def export(self, request: AnchorExportRequest) -> dict[str, Any]:
        raise NotImplementedError

    def _build_record(
        self,
        *,
        request: AnchorExportRequest,
        anchor_status: str,
        external_reference: str | None = None,
        target_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_anchor_record(
            anchor_type=request.anchor_type,
            subject_ref=request.subject_ref,
            root_hash=request.root_hash,
            anchor_target=f"adapter:{self.target_name}",
            anchor_status=anchor_status,
            anchored_at=request.anchored_at,
            external_reference=external_reference,
            target_metadata=target_metadata,
        )


class LocalAnchorAdapter(AnchorAdapter):
    """Reference adapter that records local witness anchors in-repository."""

    def __init__(self, target_name: str = "local_witness_v0"):
        self.target_name = target_name

    def export(self, request: AnchorExportRequest) -> dict[str, Any]:
        return self._build_record(
            request=request,
            anchor_status="confirmed_external",
        )


class DryRunExternalAnchorAdapter(AnchorAdapter):
    """Non-networked external adapter that emits the full external record shape."""

    def __init__(self, target_name: str = "dry_run_external_v0"):
        self.target_name = target_name

    def export(self, request: AnchorExportRequest) -> dict[str, Any]:
        external_reference = f"dryrun:{digest_hex({'target': self.target_name, 'root_hash': request.root_hash})[:16]}"
        target_metadata = {
            "submission_mode": "dry_run",
            "target_kind": "external_witness",
            "target_name": self.target_name,
            "network_ref": "dry_run",
        }
        return self._build_record(
            request=request,
            anchor_status="submitted_external",
            external_reference=external_reference,
            target_metadata=target_metadata,
        )
