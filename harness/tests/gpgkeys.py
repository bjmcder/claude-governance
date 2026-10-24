"""Throwaway ``gpg`` keyrings for the signature tests.

This module imports nothing from the package, so the equivalence harness
can build signed inputs without the code it compares.
"""

from __future__ import annotations

import secrets
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def keyring() -> Iterator[Path]:
    """Create a throwaway ``gpg`` keyring whose agent sockets fit.

    A socket path holds at most 107 bytes, so the keyring gets a short
    name directly in the temporary directory, and the agent opens no
    extra or browser socket, whose names are the longest. The agent is
    stopped and the keyring removed afterwards.

    Yields
    ------
    Path
        The keyring directory.
    """
    base = Path(tempfile.gettempdir())
    while True:
        home = base / f"g{secrets.token_hex(2)}"
        try:
            home.mkdir(mode=0o700)
            break
        except FileExistsError:
            continue
    (home / "gpg-agent.conf").write_text(
        "extra-socket none\nbrowser-socket none\n", encoding="utf-8"
    )
    try:
        yield home
    finally:
        subprocess.run(
            ["gpgconf", "--homedir", str(home), "--kill", "all"],
            capture_output=True,
            check=False,
        )
        shutil.rmtree(home, ignore_errors=True)


def make_key(home: Path, name: str) -> tuple[str, str]:
    """Generate a signing key; return its fingerprint and armored key.

    Parameters
    ----------
    home : Path
        Keyring directory.
    name : str
        User name of the key.

    Returns
    -------
    tuple[str, str]
        Fingerprint and armored public key.
    """
    base = ["gpg", "--homedir", str(home), "--batch", "--passphrase", ""]
    subprocess.run(
        [*base, "--quick-gen-key", f"{name} <{name}@example.invalid>"]
        + ["ed25519", "sign", "never"],
        capture_output=True,
        check=True,
    )
    listing = subprocess.run(
        [*base, "--with-colons", "--list-keys", name],
        capture_output=True,
        check=True,
    ).stdout.decode()
    fpr = next(
        x.split(":")[9] for x in listing.splitlines() if x.startswith("fpr:")
    )
    armored = subprocess.run(
        [*base, "--armor", "--export", fpr], capture_output=True, check=True
    ).stdout.decode()
    return fpr, armored
