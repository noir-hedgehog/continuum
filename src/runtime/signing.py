"""Local signing helpers for the bootstrap prototype."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any

from src.runtime.canonical import canonical_json


def generate_secret_hex() -> str:
    return secrets.token_hex(32)


def sign_pre_sign_image(pre_sign_image: dict[str, Any], secret_hex: str) -> str:
    key = bytes.fromhex(secret_hex)
    payload = canonical_json(pre_sign_image).encode("utf-8")
    digest = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return f"sig:{digest}"


def verify_pre_sign_image(pre_sign_image: dict[str, Any], signature: str, secret_hex: str) -> bool:
    return hmac.compare_digest(signature, sign_pre_sign_image(pre_sign_image, secret_hex))
