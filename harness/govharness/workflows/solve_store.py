"""The solve cache on disk: checked solver results, by key (unit 0011).

An entry is the file ``<directory>/<key[:2]>/<key>.json`` holding what
``checks.logic.solvecache.encode_entry`` makes of one solve; the key is
a digest of everything the result depends on, the version of the solver
code included (``solver_version``), so an honest entry is never
replaced by a different one; an entry a run refused is replaced by the
result recomputed. The directory lies outside the corpus and is no
part of the record or of any derived file; deleting it costs only time.

The directory is, in order of precedence, the one passed (the command
option ``--cache-dir``), the environment variable
``GOVHARNESS_CACHE_DIR``, or ``govharness/solves`` under
``XDG_CACHE_HOME`` (when absolute) or ``~/.cache``. The option
``--no-cache`` or a non-empty ``GOVHARNESS_NO_CACHE`` other than ``0``
turns it off.

Every read and write is best effort, and none is trusted: a missing,
unreadable, oversized, or non-regular entry is not loaded, and what is
loaded is checked before reuse (``solvecache.decode_entry``). A write
goes to a new temporary file in the entry's directory, which is then
renamed over the entry, so a reader sees the old entry or the new one
whole, and two processes writing one key leave one of their two equal
entries. Entries are opened relative to their directory, which is
opened without following a symbolic link. Directories are created
private to the account (mode 0700) and entries with mode 0600.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path

from govharness.checks.logic import satlib, solvecache

ENV_DIRECTORY = "GOVHARNESS_CACHE_DIR"
ENV_DISABLE = "GOVHARNESS_NO_CACHE"
XDG_CACHE = "XDG_CACHE_HOME"
SUBDIRECTORY = ("govharness", "solves")
MAX_ENTRY = 1 << 22  # bytes; an honest entry of this corpus is under 2 KiB
KEY_RE = re.compile(r"[0-9a-f]{64}")
_COUNT = itertools.count()  # numbers this process's temporary files
# The modules whose source a result depends on: the solver, and the
# code that keys, serializes, and checks entries. The encoding of the
# corpus as clauses needs no version: its output, the clause set, is in
# every key.
SOURCES = (satlib, solvecache)


def solver_version() -> str | None:
    """Return a digest of the source of the solver code.

    Returns
    -------
    str | None
        SHA-256 over the name and the SHA-256 of each module of
        ``SOURCES``; ``None`` when a source cannot be read, which turns
        the cache off.
    """
    digest = hashlib.sha256()
    for module in SOURCES:
        try:
            source = Path(str(module.__file__)).read_bytes()
        except (OSError, TypeError):
            return None
        digest.update(f"{module.__name__}\0".encode())
        digest.update(hashlib.sha256(source).hexdigest().encode())
        digest.update(b"\n")
    return digest.hexdigest()


@dataclass
class SolveStore:
    """A directory of solve cache entries.

    Parameters
    ----------
    directory : Path
        Absolute directory of the entries.
    version : str
        Digest of the solver code (``solver_version``).
    rejected : dict[str, str]
        Keys of loaded entries that a run refused, with the reason;
        ``workflows.verification`` fills it for the caller to report.
    """

    directory: Path
    version: str
    rejected: dict[str, str] = field(default_factory=dict)

    def path(self, key: str) -> Path:
        """Return the file of one entry.

        Parameters
        ----------
        key : str
            Hexadecimal SHA-256 key.

        Returns
        -------
        Path
            ``<directory>/<key[:2]>/<key>.json``.
        """
        return self.directory / key[:2] / f"{key}.json"

    def inside(self, root: Path) -> bool:
        """Return whether the directory lies inside a corpus root.

        Parameters
        ----------
        root : Path
            Corpus root.

        Returns
        -------
        bool
            True when the directory, its links followed, is the root or
            lies under it.
        """
        return self.directory.resolve().is_relative_to(root.resolve())

    def load(self, keys: list[str]) -> dict[str, bytes]:
        """Read the entries of some keys, skipping any that cannot be read.

        Parameters
        ----------
        keys : list[str]
            Keys to look up.

        Returns
        -------
        dict[str, bytes]
            The bytes of each entry found: a regular file, not a
            symbolic link, of at most ``MAX_ENTRY`` bytes. Its content
            is not trusted here.
        """
        found: dict[str, bytes] = {}
        for key in keys:
            if KEY_RE.fullmatch(key) is None:
                continue
            data = _read_entry(self.path(key))
            if data is not None:
                found[key] = data
        return found

    def save(self, entries: dict[str, bytes]) -> None:
        """Write entries, each by a new temporary file and a rename.

        Parameters
        ----------
        entries : dict[str, bytes]
            Entry by key. A write that fails is dropped, since the
            cache only saves time.
        """
        for key, data in entries.items():
            if KEY_RE.fullmatch(key) is not None:
                _write_entry(self.path(key), data)


def _open_directory(path: Path, create: bool) -> int | None:
    """Open the directory of an entry without following a link.

    Parameters
    ----------
    path : Path
        Directory ``<directory>/<key[:2]>``.
    create : bool
        Whether to create it, and the cache directory, when absent.

    Returns
    -------
    int | None
        A descriptor of the directory; ``None`` when it is absent, is a
        symbolic link, or cannot be opened. The entry is then opened
        relative to it, so a link planted in its place cannot redirect
        a read or a write.
    """
    try:
        if create:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            try:
                path.mkdir(mode=0o700)
            except FileExistsError:
                pass
        return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError:
        return None


def _read_entry(path: Path) -> bytes | None:
    """Return the bytes of an entry file, or None.

    The file is opened without following a symbolic link and without
    blocking, so a planted link or named pipe can neither redirect the
    read nor stall it.

    Parameters
    ----------
    path : Path
        File of the entry.

    Returns
    -------
    bytes | None
        Its content; ``None`` when it is absent, unreadable, not a
        regular file, or larger than ``MAX_ENTRY``.
    """
    folder = _open_directory(path.parent, create=False)
    if folder is None:
        return None
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        handle = os.open(path.name, flags, dir_fd=folder)
    except OSError:
        return None
    finally:
        os.close(folder)
    try:
        info = os.fstat(handle)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_ENTRY:
            return None
        chunks: list[bytes] = []
        size = 0
        while chunk := os.read(handle, 1 << 16):
            size += len(chunk)
            if size > MAX_ENTRY:
                return None
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(handle)


def _write_entry(path: Path, data: bytes) -> None:
    """Write an entry atomically: a new temporary file, then a rename.

    The temporary file is created exclusively, under a name that holds
    the process number and a count, so two processes never share one;
    the rename replaces the entry in one step.

    Parameters
    ----------
    path : Path
        File of the entry.
    data : bytes
        Its content.
    """
    folder = _open_directory(path.parent, create=True)
    if folder is None:
        return
    temporary = ""
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        for _ in range(100):
            temporary = f".{path.stem[:16]}.{os.getpid()}.{next(_COUNT)}.tmp"
            try:
                handle = os.open(temporary, flags, 0o600, dir_fd=folder)
                break
            except FileExistsError:
                continue
        else:
            temporary = ""
            return
        with os.fdopen(handle, "wb") as out:
            out.write(data)
        # On POSIX a rename replaces the entry in one step.
        os.rename(temporary, path.name, src_dir_fd=folder, dst_dir_fd=folder)
        temporary = ""
    except OSError:
        pass
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=folder)
            except OSError:
                pass
        os.close(folder)


def default_directory() -> Path | None:
    """Return the cache directory the environment names.

    Returns
    -------
    Path | None
        ``GOVHARNESS_CACHE_DIR`` when set, else ``govharness/solves``
        under an absolute ``XDG_CACHE_HOME`` or under ``~/.cache``;
        ``None`` when no home directory is known.
    """
    named = os.environ.get(ENV_DIRECTORY, "")
    if named:
        return Path(named)
    base = os.environ.get(XDG_CACHE, "")
    if not base or not Path(base).is_absolute():
        try:
            base = str(Path.home() / ".cache")
        except RuntimeError:
            return None
    return Path(base, *SUBDIRECTORY)


def disabled_by_environment() -> bool:
    """Return whether ``GOVHARNESS_NO_CACHE`` turns the cache off.

    Returns
    -------
    bool
        True when it is set to anything but the empty string or ``0``.
    """
    return os.environ.get(ENV_DISABLE, "") not in {"", "0"}


def supported() -> bool:
    """Return whether the system opens files as the store needs.

    Returns
    -------
    bool
        True where ``os.open``, ``os.rename``, and ``os.unlink`` take a
        directory descriptor and ``os.open`` can refuse to follow a
        symbolic link, as on Linux and the BSDs; elsewhere the cache is
        off.
    """
    return (
        hasattr(os, "O_NOFOLLOW")
        and hasattr(os, "O_DIRECTORY")
        and all(
            call in os.supports_dir_fd
            for call in (os.open, os.rename, os.unlink)
        )
    )


def open_store(
    enabled: bool = True, directory: Path | None = None
) -> SolveStore | None:
    """Return the solve cache to use, or None when it is off.

    Parameters
    ----------
    enabled : bool
        False for ``--no-cache``.
    directory : Path | None
        Directory from ``--cache-dir``; it takes precedence over the
        environment, ``GOVHARNESS_NO_CACHE`` included.

    Returns
    -------
    SolveStore | None
        The store; ``None`` when the cache is off, the system is not
        ``supported``, no directory is known, or the solver source
        cannot be read.
    """
    if not enabled or not supported():
        return None
    if directory is None:
        if disabled_by_environment():
            return None
        directory = default_directory()
        if directory is None:
            return None
    version = solver_version()
    if version is None:
        return None
    return SolveStore(directory.absolute(), version)
