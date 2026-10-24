"""Derive every ``MANIFEST.csv`` of the corpus, bottom-up.

Each manifest lists the directory's own document (``_doc.md``), its
leaf entries, and its subdirectories. A subdirectory row carries the
SHA-256 of that subdirectory's manifest, so the root manifest's rows pin
the whole tree. The root manifest lists the top-level mnemonics; it is
not the mnemonic register, which is ``MNEM/_doc.md`` (STND.IDENT.19).
Manifests are generated and informative only (GOV.39).
"""

from __future__ import annotations

import csv
import io
from pathlib import PurePosixPath

from govharness.core.corpus import CURRENT, Tree
from govharness.core.entry import (
    DOC_FILE,
    MANIFEST_FILE,
    README_FILE,
    TEMPLATE_PREFIX,
    parse_entry,
    path_to_id,
)
from govharness.core.hashing import sha256_bytes

COLUMNS = ["id", "kind", "level", "title", "status", "path", "sha256", "bytes"]
Summary = tuple[str, int]


def _leaf_key(path: PurePosixPath) -> tuple[int, int, str]:
    """Order ``_doc.md`` first, then numbered entries, then slugs.

    Parameters
    ----------
    path : PurePosixPath
        A Markdown file.

    Returns
    -------
    tuple[int, int, str]
        Sort key.
    """
    stem = path.stem
    if path.name == DOC_FILE:
        return (0, 0, "")
    return (1, int(stem), "") if stem.isdigit() else (2, 0, stem)


def _row(tree: Tree, file: PurePosixPath) -> dict[str, str]:
    """Build the manifest row for one Markdown entry.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    file : PurePosixPath
        The entry's path relative to the root.

    Returns
    -------
    dict[str, str]
        Cells by column.
    """
    meta, _ = parse_entry(tree.text(file))
    data = tree.files[file]
    return {
        "id": path_to_id(file),
        "kind": str(meta.get("kind", "")),
        "level": str(meta.get("level") or ""),
        "title": str(meta.get("title") or meta.get("term") or ""),
        "status": str(meta.get("status", "")),
        "path": file.name,
        "sha256": sha256_bytes(data),
        "bytes": str(len(data)),
    }


def _children(tree: Tree, directory: PurePosixPath) -> list[PurePosixPath]:
    """Return the subdirectories of a directory, templates excluded.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    directory : PurePosixPath
        A directory of the tree.

    Returns
    -------
    list[PurePosixPath]
        Subdirectories, sorted by name.
    """
    return sorted(
        d
        for d in tree.directories
        if d != CURRENT
        and d.parent == directory
        and not d.name.startswith(TEMPLATE_PREFIX)
    )


def render_manifest(
    tree: Tree,
    directory: PurePosixPath,
    child_summaries: dict[PurePosixPath, Summary],
) -> str:
    """Render one directory's manifest text.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    directory : PurePosixPath
        Directory whose manifest is rendered.
    child_summaries : dict[PurePosixPath, Summary]
        Manifest hash and total Markdown bytes already computed for each
        subdirectory.

    Returns
    -------
    str
        CSV text with a header row and LF line endings.
    """
    leaves = [
        f
        for f in tree.files
        if f.parent == directory
        and f.name.endswith(".md")
        and f.name != README_FILE
    ]
    rows = [_row(tree, f) for f in sorted(leaves, key=_leaf_key)]
    for sub in _children(tree, directory):
        doc = sub / DOC_FILE
        meta = parse_entry(tree.text(doc))[0] if doc in tree.files else {}
        digest, size = child_summaries[sub]
        rows.append(
            {
                "id": path_to_id(doc),
                "kind": str(meta.get("kind", "directory")),
                "level": str(meta.get("level") or ""),
                "title": str(meta.get("title") or ""),
                "status": str(meta.get("status", "")),
                "path": f"{sub.name}/",
                "sha256": digest,
                "bytes": str(size),
            }
        )
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _markdown_bytes(tree: Tree, directory: PurePosixPath) -> int:
    """Return the size of every Markdown file at or below a directory.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    directory : PurePosixPath
        A directory of the tree.

    Returns
    -------
    int
        Total bytes, template and README files included.
    """
    depth = len(directory.parts)
    return sum(
        len(data)
        for f, data in tree.files.items()
        if f.name.endswith(".md") and f.parts[:depth] == directory.parts
    )


def build_manifests(tree: Tree) -> dict[PurePosixPath, str]:
    """Compute every manifest without writing.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.

    Returns
    -------
    dict[PurePosixPath, str]
        Manifest path relative to the root, to its expected text.
    """
    expected: dict[PurePosixPath, str] = {}
    summaries: dict[PurePosixPath, Summary] = {}
    directories = [
        d
        for d in tree.directories
        if not any(p.startswith(TEMPLATE_PREFIX) for p in d.parts)
    ]
    # Deepest first, so that each parent finds its children's hashes.
    for directory in sorted(
        directories, key=lambda d: len(d.parts), reverse=True
    ):
        text = render_manifest(tree, directory, summaries)
        expected[directory / MANIFEST_FILE] = text
        summaries[directory] = (
            sha256_bytes(text.encode()),
            _markdown_bytes(tree, directory),
        )
    return expected


def stale_manifests(tree: Tree) -> dict[PurePosixPath, str]:
    """Return the derived manifests whose file is missing or differs.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.

    Returns
    -------
    dict[PurePosixPath, str]
        Expected text by manifest path, in path order.
    """
    return {
        path: text
        for path, text in sorted(build_manifests(tree).items())
        if path not in tree.files or tree.text(path) != text
    }
