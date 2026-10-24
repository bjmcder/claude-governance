"""Digests and the canonical JSON form that the ledger hashes."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def sha256_bytes(data: bytes) -> str:
    """Return the hexadecimal SHA-256 digest of some bytes.

    Parameters
    ----------
    data : bytes
        Bytes to hash.

    Returns
    -------
    str
        Lowercase hexadecimal digest.
    """
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> str:
    """Serialize a value deterministically for hashing and the ledger.

    Parameters
    ----------
    obj : Any
        JSON-compatible value.

    Returns
    -------
    str
        Compact JSON with sorted keys and Unicode kept as is.
    """
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def ledger_entry_hash(entry: dict[str, Any]) -> str:
    """Hash a ledger entry over every field except ``hash`` itself.

    Parameters
    ----------
    entry : dict[str, Any]
        Ledger entry, with or without ``hash``.

    Returns
    -------
    str
        SHA-256 of the canonical JSON of the other fields.
    """
    return sha256_bytes(
        canonical_json(
            {k: v for k, v in entry.items() if k != "hash"}
        ).encode()
    )
