"""Event builders for the Continuum bootstrap."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from src.runtime.canonical import digest_hex
from src.runtime.identifiers import derive_event_id, generate_domain_id
from src.runtime.signing import sign_pre_sign_image, verify_pre_sign_image
from src.schemas.registry import (
    CHECKPOINT_SCOPES,
    ENVELOPE_REQUIRED_FIELDS,
    MIGRATION_TYPES,
    PAYLOAD_REQUIRED_FIELDS,
    PAYLOAD_ROOTS,
    SCHEMA_VERSION,
)


def utc_now() -> str:
    fixed = os.getenv("CONTINUUM_NOW")
    if fixed:
        value = fixed.strip()
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:  # pragma: no cover
            raise ValueError(
                "Invalid CONTINUUM_NOW value; expected ISO-8601 timestamp like 2026-05-12T00:00:00Z"
            ) from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def artifact_refs(paths: list[str]) -> list[dict[str, str]]:
    return [{"ref": path, "ref_type": "artifact", "relationship": "supports"} for path in paths]


def build_event(
    *,
    kind: str,
    actor_id: str,
    signing_key: str,
    secret_hex: str,
    payload: dict[str, Any],
    refs: list[dict[str, str]] | None = None,
    created_at: str | None = None,
    community_id: str | None = None,
) -> dict[str, Any]:
    if kind not in PAYLOAD_ROOTS:
        raise ValueError(f"Unsupported event kind: {kind}")
    pre_sign_image: dict[str, Any] = {
        "kind": kind,
        "actor_id": actor_id,
        "created_at": created_at or utc_now(),
        "payload": payload,
        "refs": refs or [],
        "signing_key": signing_key,
        "schema_version": SCHEMA_VERSION,
    }
    if community_id:
        pre_sign_image["community_id"] = community_id
    envelope = {
        "event_id": derive_event_id(pre_sign_image),
        **pre_sign_image,
        "signature": sign_pre_sign_image(pre_sign_image, secret_hex),
    }
    validate_event(envelope, secret_hex)
    return envelope


def validate_event(envelope: dict[str, Any], secret_hex: str) -> None:
    missing = [field for field in ENVELOPE_REQUIRED_FIELDS if field not in envelope]
    if missing:
        raise ValueError(f"Envelope missing required fields: {missing}")
    payload_root = PAYLOAD_ROOTS.get(envelope["kind"])
    if not payload_root:
        raise ValueError(f"Unsupported event kind: {envelope['kind']}")
    payload = envelope["payload"]
    if payload_root not in payload:
        raise ValueError(f"Payload missing root `{payload_root}` for kind `{envelope['kind']}`.")
    object_payload = payload[payload_root]
    missing_payload = [field for field in PAYLOAD_REQUIRED_FIELDS[payload_root] if field not in object_payload]
    if missing_payload:
        raise ValueError(f"{payload_root} payload missing required fields: {missing_payload}")
    pre_sign_image = {
        key: envelope[key]
        for key in ("kind", "actor_id", "created_at", "payload", "refs", "signing_key", "schema_version")
    }
    if "community_id" in envelope:
        pre_sign_image["community_id"] = envelope["community_id"]
    expected_event_id = derive_event_id(pre_sign_image)
    if envelope["event_id"] != expected_event_id:
        raise ValueError("Event identifier does not match canonical pre-sign image.")
    if not verify_pre_sign_image(pre_sign_image, envelope["signature"], secret_hex):
        raise ValueError("Event signature verification failed.")


def build_profile_payload(agent_id: str, display_name: str, description: str, operator_disclosure: str | None) -> dict[str, Any]:
    profile = {
        "agent_id": agent_id,
        "display_name": display_name,
        "description": description,
    }
    if operator_disclosure:
        profile["operator_disclosure"] = operator_disclosure
    return {"profile": profile}


def build_checkpoint_payload(
    *,
    agent_id: str,
    scope: str,
    summary: str,
    state_root: str | None = None,
    checkpoint_uri: str | None = None,
    prev_checkpoint_id: str | None = None,
    checkpoint_id: str | None = None,
) -> dict[str, Any]:
    if scope not in CHECKPOINT_SCOPES:
        raise ValueError(f"Unsupported checkpoint scope: {scope}")
    summary_hash = f"sum:{digest_hex({'summary': summary})}"
    checkpoint = {
        "checkpoint_id": checkpoint_id or generate_domain_id("checkpoint", slug_scope(agent_id)),
        "agent_id": agent_id,
        "scope": scope,
        "summary_hash": summary_hash,
        "state_root": state_root or f"root:{digest_hex({'scope': scope, 'summary': summary})}",
    }
    if checkpoint_uri:
        checkpoint["checkpoint_uri"] = checkpoint_uri
    if prev_checkpoint_id:
        checkpoint["prev_checkpoint_id"] = prev_checkpoint_id
    return {"checkpoint": checkpoint}


def build_migration_payload(
    *,
    agent_id: str,
    migration_type: str,
    from_ref: str,
    to_ref: str,
    reason: str,
    evidence: list[str],
    expected_continuity_class: str,
    effective_at: str | None = None,
    prev_migration_id: str | None = None,
    migration_id: str | None = None,
) -> dict[str, Any]:
    if migration_type not in MIGRATION_TYPES:
        raise ValueError(f"Unsupported migration type: {migration_type}")
    migration = {
        "migration_id": migration_id or generate_domain_id("migration", slug_scope(agent_id)),
        "agent_id": agent_id,
        "migration_type": migration_type,
        "effective_at": effective_at or utc_now(),
        "from_ref": from_ref,
        "to_ref": to_ref,
        "reason": reason,
        "evidence": evidence,
        "expected_continuity_class": expected_continuity_class,
    }
    if prev_migration_id:
        migration["prev_migration_id"] = prev_migration_id
    return {"migration": migration}


def slug_scope(agent_id: str) -> str:
    return agent_id.replace(":", "-")
