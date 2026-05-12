"""Identifier helpers."""

from __future__ import annotations

import os
import re
import uuid
from typing import Any

from src.runtime.canonical import digest_hex


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", lowered)
    return normalized.strip("-") or "default"


def generate_domain_id(family: str, scope: str, token: str | None = None) -> str:
    env_token = os.getenv("CONTINUUM_DOMAIN_TOKEN")
    if token:
        authoring_token = token
    elif env_token:
        authoring_token = digest_hex({"family": family, "scope": scope, "token": env_token})[:12]
    else:
        authoring_token = uuid.uuid4().hex[:12]
    return f"{family}:{scope}:{authoring_token}"


def derive_event_id(pre_sign_image: dict[str, Any]) -> str:
    return f"evt:{digest_hex(pre_sign_image)}"
