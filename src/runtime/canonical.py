"""Canonical serialization helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any


# v0 spec target is BLAKE3-256. The bootstrap stays stdlib-only and uses
# BLAKE2b-256 until the repo adopts an external BLAKE3 dependency.
DIGEST_ALGORITHM = "blake2b-256"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_hex(value: Any) -> str:
    data = canonical_json(value).encode("utf-8")
    return hashlib.blake2b(data, digest_size=32).hexdigest()
