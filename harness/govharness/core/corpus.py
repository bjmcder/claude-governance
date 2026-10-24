"""Read the corpus from disk and index its entries.

This is the one module that reads corpus files (decision 0001, DSGN.16).
``read_tree`` takes a snapshot of every file under a root, so that the
checks and derivations above it compute on data and never touch the
disk. Files are decoded as UTF-8 with universal newlines, as
``Path.read_text`` decodes them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from govharness.core.entry import (
    DOC_FILE,
    README_FILE,
    Entry,
    in_template,
    parse_entry,
)
from govharness.core.hashing import sha256_bytes

CURRENT = PurePosixPath(".")


def decode(data: bytes) -> str:
    """Decode file bytes as ``Path.read_text`` does.

    Parameters
    ----------
    data : bytes
        Raw file contents.

    Returns
    -------
    str
        UTF-8 text with ``\\r\\n`` and ``\\r`` turned into ``\\n``.
    """
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


@dataclass(frozen=True)
class Tree:
    """Every directory and file under a corpus root, read once.

    Parameters
    ----------
    directories : tuple[PurePosixPath, ...]
        Directories relative to the root, sorted; the root is ``.``.
    files : dict[PurePosixPath, bytes]
        Contents of every file, by path relative to the root.
    """

    directories: tuple[PurePosixPath, ...]
    files: dict[PurePosixPath, bytes] = field(default_factory=dict)

    def text(self, rel: PurePosixPath) -> str:
        """Return one file decoded as text.

        Parameters
        ----------
        rel : PurePosixPath
            Path relative to the root.

        Returns
        -------
        str
            The decoded contents.

        Raises
        ------
        KeyError
            If the tree holds no such file.
        """
        return decode(self.files[rel])

    def markdown(self) -> list[PurePosixPath]:
        """Return the paths of every Markdown file, sorted.

        Returns
        -------
        list[PurePosixPath]
            Files whose name ends in ``.md``, templates included.
        """
        return sorted(p for p in self.files if p.name.endswith(".md"))


def read_tree(root: Path) -> Tree:
    """Snapshot every directory and file under a corpus root.

    Parameters
    ----------
    root : Path
        Corpus root directory.

    Returns
    -------
    Tree
        Relative directories and file contents.
    """
    directories = [CURRENT]
    files: dict[PurePosixPath, bytes] = {}
    for path in sorted(root.rglob("*")):
        rel = PurePosixPath(path.relative_to(root).as_posix())
        if path.is_dir():
            directories.append(rel)
        elif path.is_file():
            files[rel] = path.read_bytes()
    return Tree(tuple(directories), files)


def load_entries(tree: Tree) -> list[Entry]:
    """Parse every governance file of a tree.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus.

    Returns
    -------
    list[Entry]
        Entries sorted by path; template directories and README files
        are excluded.

    Raises
    ------
    ValueError
        If a file has malformed front matter.
    """
    entries: list[Entry] = []
    for rel in tree.markdown():
        if in_template(rel) or rel.name == README_FILE:
            continue
        meta, body = parse_entry(tree.text(rel))
        entries.append(Entry(rel, meta, body))
    return entries


@dataclass
class Corpus:
    """Indexed view of the corpus entries.

    Parameters
    ----------
    entries : list[Entry]
        Every loaded entry; the view may be held in memory only.
    """

    entries: list[Entry]
    by_id: dict[str, Entry] = field(init=False)
    parts: list[str] = field(init=False)

    def __post_init__(self) -> None:
        """Index entries by identifier and read the LVL0 part list."""
        self.by_id = {str(e.meta["id"]): e for e in self.entries}
        root = self.by_id.get("LVL0")
        self.parts = list(root.meta.get("parts", [])) if root else []

    def provisions(self, part: str | None = None) -> list[Entry]:
        """Return provision entries, optionally of one part.

        Parameters
        ----------
        part : str | None
            Top-level mnemonic, or ``None`` for every part.

        Returns
        -------
        list[Entry]
            Entries of kind ``provision``, in path order.
        """
        return [
            e
            for e in self.entries
            if e.meta.get("kind") == "provision"
            and (part is None or e.path.parts[0] == part)
        ]

    def terms(self) -> list[Entry]:
        """Return the Lexicon term entries.

        Returns
        -------
        list[Entry]
            Entries of kind ``term``, in path order.
        """
        return [e for e in self.entries if e.meta.get("kind") == "term"]

    def body(self, stable_id: str | None) -> str:
        """Return an entry's body, or an empty string if it is absent.

        Parameters
        ----------
        stable_id : str | None
            Identifier of the entry.

        Returns
        -------
        str
            The Markdown body.
        """
        entry = self.by_id.get(stable_id or "")
        return entry.body if entry else ""

    def document_of(self, entry: Entry) -> Entry | None:
        """Return the document (``_doc.md``) in an entry's directory.

        Parameters
        ----------
        entry : Entry
            Any entry.

        Returns
        -------
        Entry | None
            The document entry, or ``None`` when the directory has none.
        """
        wanted = entry.path.parent / DOC_FILE
        return next((e for e in self.entries if e.path == wanted), None)


def provision_key(entry: Entry) -> tuple[str, int]:
    """Return the sort key of a provision: its part, then its number.

    Parameters
    ----------
    entry : Entry
        A provision.

    Returns
    -------
    tuple[str, int]
        Top-level mnemonic and number (0 for a slug).
    """
    stem = entry.path.stem
    return entry.path.parts[0], int(stem) if stem.isdigit() else 0


def read_corpus(root: Path) -> Corpus:
    """Load and index the corpus at a root.

    Parameters
    ----------
    root : Path
        Corpus root directory.

    Returns
    -------
    Corpus
        The indexed entries.
    """
    return Corpus(load_entries(read_tree(root)))


def read_text(path: Path) -> str:
    """Read one corpus file as text.

    Parameters
    ----------
    path : Path
        File to read.

    Returns
    -------
    str
        Its UTF-8 contents.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    return path.read_text(encoding="utf-8")


def read_optional_text(path: Path) -> str | None:
    """Read one corpus file as text, if it exists.

    Parameters
    ----------
    path : Path
        File to read.

    Returns
    -------
    str | None
        Its UTF-8 contents, or ``None`` when there is no such file.
    """
    return read_text(path) if path.exists() else None


def inside_root(rel: str) -> bool:
    """Return True when a relative path cannot leave the corpus root.

    Parameters
    ----------
    rel : str
        Path relative to the root, such as a ledger scope ``STND/DRAFT``.

    Returns
    -------
    bool
        Whether the path is relative and has no ``..`` part, so that a
        scope pins only content of the corpus (GOV.36).
    """
    pure = PurePosixPath(rel)
    return not pure.is_absolute() and ".." not in pure.parts


def is_directory(root: Path, rel: str) -> bool:
    """Return True when a path under the root names a directory.

    Parameters
    ----------
    root : Path
        Corpus root.
    rel : str
        Path relative to the root, such as a ledger scope ``STND/DRAFT``.

    Returns
    -------
    bool
        Whether the path lies inside the root and the directory exists.
    """
    return inside_root(rel) and (root / rel).is_dir()


def has_directory(tree: Tree, rel: str) -> bool:
    """Return True when a snapshot holds a directory at a relative path.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus.
    rel : str
        Path relative to the root, such as a ledger scope ``STND/DRAFT``.

    Returns
    -------
    bool
        Whether the path lies inside the root and names a directory.
    """
    return inside_root(rel) and PurePosixPath(rel) in tree.directories


def scope_hash(tree: Tree, prefixes: list[str]) -> str:
    """Hash every Markdown file of a snapshot under some scope paths.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus.
    prefixes : list[str]
        Scope paths: top-level directories or subpaths such as
        ``STND/DRAFT``. A path that leaves the root contributes nothing.

    Returns
    -------
    str
        SHA-256 over the ``path:digest`` lines of the included files,
        scope by scope in sorted order and by path within a scope;
        manifests are not Markdown and are excluded.
    """
    lines: list[str] = []
    for prefix in sorted(p for p in prefixes if inside_root(p)):
        parts = PurePosixPath(prefix).parts
        lines += [
            f"{rel.as_posix()}:{sha256_bytes(tree.files[rel])}"
            for rel in tree.markdown()
            if rel.parts[: len(parts)] == parts
        ]
    return sha256_bytes("\n".join(lines).encode())


def corpus_hash(root: Path, prefixes: list[str]) -> str:
    """Hash every Markdown file under some scope paths of a corpus.

    Parameters
    ----------
    root : Path
        Corpus root directory.
    prefixes : list[str]
        Scope paths, as for ``scope_hash``.

    Returns
    -------
    str
        The ``scope_hash`` of a snapshot of the root, the value a
        transaction pins as ``corpus_hash``.
    """
    return scope_hash(read_tree(root), prefixes)


def tree_digests(root: Path) -> dict[str, str]:
    """Return the SHA-256 of every file under a root, and its directories.

    Parameters
    ----------
    root : Path
        Any directory, such as a corpus root.

    Returns
    -------
    dict[str, str]
        By POSIX path relative to the root: the digest of each file, and
        ``directory`` for each directory, so that an added or removed
        empty directory shows as well.
    """
    tree = read_tree(root)
    found = {rel.as_posix(): "directory" for rel in tree.directories}
    found.update(
        (rel.as_posix(), sha256_bytes(data))
        for rel, data in tree.files.items()
    )
    return found
