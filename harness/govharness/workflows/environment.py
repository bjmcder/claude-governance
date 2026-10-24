"""Check the installed configuration of an agent's environment.

STND.HARN.21 requires the harness to report each installed
configuration file, and each program the configuration runs, that is
missing, differs from its generation, or is alterable by the account
that runs the harness. Run it from the agent's account, so that "able
to alter" means that account.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from govharness.core.corpus import read_optional_text
from govharness.ledger.gpg import unalterable

INSTALL_PREFIX = PurePosixPath("root")


def installed_problems(
    files: dict[PurePosixPath, str],
    install_root: Path,
    programs: tuple[str, ...] = (),
) -> list[str]:
    """Return a problem line for each generated file not installed safely.

    Parameters
    ----------
    files : dict[PurePosixPath, str]
        Generated files by path relative to the output directory; those
        under ``root/`` are installed.
    install_root : Path
        Directory the paths under ``root/`` are installed beneath,
        ``/`` in use.
    programs : tuple[str, ...]
        Absolute paths of the programs the configuration runs, such as
        the hook's interpreter.

    Returns
    -------
    list[str]
        One line per missing, differing, or alterable file or program;
        empty when every one is current and out of the account's reach.
    """
    problems: list[str] = []
    for rel, text in sorted(files.items()):
        if rel.parts[:1] != INSTALL_PREFIX.parts:
            continue
        path = install_root / rel.relative_to(INSTALL_PREFIX)
        installed = read_optional_text(path)
        if installed is None:
            problems.append(f"missing: {path}")
        elif installed != text:
            problems.append(f"differs from its generation: {path}")
        elif not unalterable(path):
            problems.append(f"alterable by this account: {path}")
    for program in programs:
        path = install_root / program.lstrip("/")
        if not unalterable(path):
            problems.append(f"program missing or alterable: {path}")
    return problems
