"""The solve cache on disk: checked solver results, by key (unit 0011).

An entry is the file ``<directory>/<key[:2]>/<key>.json`` holding what
``checks.logic.solvecache.encode_entry`` makes of one solve; the key is
a digest of everything the result depends on, the version of the solver
code included (``solver_version``), so an honest entry is never
replaced by a different one; an entry a run refused is replaced by the
result recomputed. The directory lies outside the corpus and is no
part of the record or of any derived file; deleting it costs only time.

The cache is opt-in (unit 0022): the directory is the one passed (the
command option ``--cache DIR``), else the one the environment variable
``GOVHARNESS_CACHE`` names; where neither names one, there is no cache
and nothing is written anywhere.

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

import errno
import hashlib
import itertools
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path

from govharness.checks.logic import satlib, solvecache
from govharness.core import hashing

ENV_DIRECTORY = "GOVHARNESS_CACHE"
MAX_ENTRY = 1 << 22  # bytes; an honest entry of this corpus is under 2 KiB
KEY_RE = re.compile(r"[0-9a-f]{64}")
_COUNT = itertools.count()  # numbers this process's temporary files
# The modules whose source a result depends on: the solver, and the
# code that keys, serializes, and checks entries, with the canonical
# JSON it uses. The encoding of the corpus as clauses needs no version:
# its output, the clause set, is in every key.
SOURCES = (satlib, solvecache, hashing)
# The error that means an entry, or its directory, is not there at all.
ABSENT = {errno.ENOENT}


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
    skipped : dict[str, str]
        Keys whose entry file is present but was not read, with the
        reason; ``load`` fills it for the caller to report.
    """

    directory: Path
    version: str
    rejected: dict[str, str] = field(default_factory=dict)
    skipped: dict[str, str] = field(default_factory=dict)

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
            is not trusted here. An entry present but not read is
            recorded in ``skipped``.
        """
        found: dict[str, bytes] = {}
        for key in keys:
            if KEY_RE.fullmatch(key) is None:
                continue
            data, reason = _read_entry(self.path(key))
            if data is not None:
                found[key] = data
            elif reason:
                self.skipped[key] = reason
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


def _open_directory(path: Path, create: bool) -> tuple[int | None, str]:
    """Open the directory of an entry without following a link.

    Parameters
    ----------
    path : Path
        Directory ``<directory>/<key[:2]>``.
    create : bool
        Whether to create it, and the cache directory, when absent.

    Returns
    -------
    tuple[int | None, str]
        A descriptor of the directory and an empty reason; or ``None``
        with an empty reason when it is absent, and with the reason
        (a symbolic link, unreadable) when it was not opened. The entry
        is then opened relative to it, so a link planted in its place
        cannot redirect a read or a write.
    """
    try:
        if create:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            try:
                path.mkdir(mode=0o700)
            except FileExistsError:
                pass
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        return os.open(path, flags), ""
    except OSError as error:
        # Linux refuses a link opened as a directory with ENOTDIR.
        linked = error.errno in {errno.ELOOP, errno.ENOTDIR}
        if linked and path.is_symlink():
            return None, "its directory is a symbolic link"
        return None, _reason(error, "its directory")


def _reason(error: OSError, what: str) -> str:
    """Name why a file of the cache could not be opened.

    Parameters
    ----------
    error : OSError
        The error of ``os.open``.
    what : str
        What was opened, such as ``its directory``.

    Returns
    -------
    str
        Empty when the file is absent; else a short reason.
    """
    if error.errno in ABSENT:
        return ""
    if error.errno == errno.ELOOP:
        return f"{what} is a symbolic link"
    name = errno.errorcode.get(error.errno or 0, "error")
    return f"{what} cannot be opened ({name})"


def _read_entry(path: Path) -> tuple[bytes | None, str]:
    """Return the bytes of an entry file, or None with the reason.

    The file is opened without following a symbolic link and without
    blocking, so a planted link or named pipe can neither redirect the
    read nor stall it.

    Parameters
    ----------
    path : Path
        File of the entry.

    Returns
    -------
    tuple[bytes | None, str]
        Its content and an empty reason; or ``None`` with an empty
        reason when it is absent, and with the reason when it is
        present but a link, unreadable, not a regular file, or larger
        than ``MAX_ENTRY``.
    """
    folder, reason = _open_directory(path.parent, create=False)
    if folder is None:
        return None, reason
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        handle = os.open(path.name, flags, dir_fd=folder)
    except OSError as error:
        return None, _reason(error, "the entry")
    finally:
        os.close(folder)
    too_large = f"the entry is larger than {MAX_ENTRY} bytes"
    try:
        info = os.fstat(handle)
        if not stat.S_ISREG(info.st_mode):
            return None, "the entry is not a regular file"
        if info.st_size > MAX_ENTRY:
            return None, too_large
        chunks: list[bytes] = []
        size = 0
        while chunk := os.read(handle, 1 << 16):
            size += len(chunk)
            if size > MAX_ENTRY:
                return None, too_large
            chunks.append(chunk)
        return b"".join(chunks), ""
    except OSError as error:
        return None, _reason(error, "the entry") or "the entry vanished"
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
    folder, _ = _open_directory(path.parent, create=True)
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
        ``GOVHARNESS_CACHE`` when set; ``None`` otherwise, which is no
        cache.

    Raises
    ------
    ValueError
        If ``GOVHARNESS_CACHE`` is relative: it would name another
        directory from each working directory, a rehearsal's among them.
    """
    named = os.environ.get(ENV_DIRECTORY, "")
    if not named:
        return None
    if not Path(named).is_absolute():
        raise ValueError(
            f"{ENV_DIRECTORY} must be an absolute path, not {named!r}"
        )
    return Path(named)


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


def open_store(directory: Path | None = None) -> SolveStore | None:
    """Return the solve cache to use, or None when there is none.

    Parameters
    ----------
    directory : Path | None
        Directory from ``--cache DIR``; it takes precedence over the
        environment. A relative one is made absolute against the
        working directory now, when the command starts.

    Returns
    -------
    SolveStore | None
        The store; ``None`` when neither the option nor
        ``GOVHARNESS_CACHE`` names a directory, the system is not
        ``supported``, or the solver source cannot be read.

    Raises
    ------
    ValueError
        If ``GOVHARNESS_CACHE`` is relative (``default_directory``).
    """
    if not supported():
        return None
    if directory is None:
        directory = default_directory()
        if directory is None:
            return None
    version = solver_version()
    if version is None:
        return None
    return SolveStore(directory.absolute(), version)
