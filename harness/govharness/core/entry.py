"""One governance file: front matter, body, and identifier mapping.

A stable identifier maps to a path by turning dots into slashes:
``GOV.12`` lives at ``GOV/12.md``, and a document identifier such as
``HW.FPGA`` lives at ``HW/FPGA/_doc.md``. Every file starts with a small
front-matter block, one ``key: JSON value`` per line between ``---``
lines, followed by Markdown text.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import PurePath
from typing import Any

DOC_FILE = "_doc.md"
MANIFEST_FILE = "MANIFEST.csv"
LEDGER_FILE = "ledger.jsonl"
README_FILE = "README.md"
TEMPLATE_PREFIX = "_"

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


@dataclass
class Entry:
    """One governance file: its front matter, body, and location.

    Parameters
    ----------
    path : PurePath
        File path relative to the corpus root.
    meta : dict[str, Any]
        Parsed front matter.
    body : str
        Markdown text after the front matter.
    """

    path: PurePath
    meta: dict[str, Any] = field(default_factory=dict)
    body: str = ""


def path_to_id(rel_path: PurePath) -> str:
    """Map a relative file path back to its stable identifier.

    Parameters
    ----------
    rel_path : PurePath
        Path relative to the corpus root.

    Returns
    -------
    str
        The identifier the path encodes.
    """
    parts = list(rel_path.parts)
    if parts[-1] == DOC_FILE:
        return ".".join(parts[:-1])
    parts[-1] = parts[-1].removesuffix(".md")
    return ".".join(parts)


def parse_entry(text: str) -> tuple[dict[str, Any], str]:
    """Parse file text into front matter and body.

    Parameters
    ----------
    text : str
        File contents.

    Returns
    -------
    tuple[dict[str, Any], str]
        The front-matter mapping and the Markdown body.

    Raises
    ------
    ValueError
        If the text has no front-matter block or a field is malformed.
    """
    match = FRONT_RE.match(text)
    if match is None:
        raise ValueError("missing front matter")
    meta: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        key, sep, raw = line.partition(": ")
        if not sep:
            raise ValueError(f"malformed front-matter line: {line!r}")
        meta[key] = json.loads(raw)
    return meta, match.group(2).strip()


def in_template(rel_path: PurePath) -> bool:
    """Return True when a file lies in a template directory.

    Parameters
    ----------
    rel_path : PurePath
        File path relative to the corpus root.

    Returns
    -------
    bool
        Whether a directory above the file starts with ``_``; such
        directories are templates, not part of the corpus.
    """
    return any(p.startswith(TEMPLATE_PREFIX) for p in rel_path.parts[:-1])
