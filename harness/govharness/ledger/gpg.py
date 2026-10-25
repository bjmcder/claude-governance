"""Run ``gpg`` to sign and verify, and read the signer configuration.

This is the one module that starts processes, reads the environment, or
reads the signer configuration (decision 0001, DSGN.16). Verification
runs ``gpg`` with a fixed ``PATH`` against a throwaway keyring of the
registered keys, in a temporary directory that only this module writes.

The configuration names the anchor key that founds the signer register,
the ``gpg`` binary, and, optionally, the head of the corpus ledger: the
sequence number and hash of an entry the ledger must still hold, so
that entries cut from its end are seen. The human owner keeps it where
the agent's account cannot write it (``CONFIG_PATH``). A file or binary
that the running user is able to alter is ignored, because a check
settles reliance only when the agent relying on it is unable to alter
the verifier or its anchor.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

CONFIG_PATH = Path("/etc/governance/signer.json")
DEFAULT_GPG = "/usr/bin/gpg"
GPG_ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
REJECTED_STATUS = {
    "BADSIG",
    "ERRSIG",
    "EXPSIG",
    "EXPKEYSIG",
    "REVKEYSIG",
    "KEYREVOKED",
    "NO_PUBKEY",
}


@dataclass
class SignerConfig:
    """Verifier settings kept outside the work.

    Parameters
    ----------
    anchor : str | None
        Fingerprint of the key that founds the signer register.
    gpg : str
        Absolute path of the ``gpg`` binary.
    head : object
        The head pin of the corpus ledger as the file gives it,
        ``{"seq": N, "hash": H}``, or ``None``; it is checked, malformed
        or not, by ``transactions.head_problems``.
    """

    anchor: str | None = None
    gpg: str = DEFAULT_GPG
    head: object = None


def unalterable(path: Path) -> bool:
    """Return True when the running user can alter neither a path nor a
    directory above it.

    Parameters
    ----------
    path : Path
        File to test.

    Returns
    -------
    bool
        Whether the file exists and no part of its path, nor of the
        path its symbolic links lead to, is writable; a link is as safe
        as the place it leads to.
    """
    real = path.resolve()
    parts = {path, *path.parents, real, *real.parents}
    return path.exists() and not any(os.access(p, os.W_OK) for p in parts)


def read_config(path: Path | None = None) -> SignerConfig:
    """Return the signer configuration, or defaults where it is not safe.

    Parameters
    ----------
    path : Path | None
        Configuration file; ``None`` uses ``CONFIG_PATH``.

    Returns
    -------
    SignerConfig
        The anchor, the ``gpg`` path, and the head pin, taken only from
        a file, and a binary, that the running user is unable to alter;
        otherwise no anchor, so that the founding check fails, and no
        head pin.
    """
    path = path or CONFIG_PATH
    if not unalterable(path):
        return SignerConfig()
    data = json.loads(path.read_text(encoding="utf-8"))
    gpg = str(data.get("gpg", DEFAULT_GPG))
    return SignerConfig(
        data.get("anchor"),
        gpg if unalterable(Path(gpg)) else DEFAULT_GPG,
        data.get("head"),
    )


def sign_digest(
    digest: str, key: str, gnupg_home: Path | None = None, gpg: str = "gpg"
) -> str:
    """Return an armored detached signature of a digest.

    Parameters
    ----------
    digest : str
        Entry digest from ``entry_digest``.
    key : str
        Key identifier or fingerprint in the signer's keyring.
    gnupg_home : Path | None
        Keyring directory; ``None`` uses the signer's default.
    gpg : str
        The ``gpg`` binary of the signer.

    Returns
    -------
    str
        The armored signature.

    Raises
    ------
    RuntimeError
        If ``gpg`` fails.
    """
    command = [gpg, "--batch", "--yes", "--armor", "--detach-sign"]
    command += ["--local-user", key, "--output", "-"]
    if gnupg_home is not None:
        command[1:1] = ["--homedir", str(gnupg_home)]
    done = subprocess.run(
        command, input=digest.encode(), capture_output=True, check=False
    )
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace").strip())
    return done.stdout.decode()


def parse_status(status: str, returncode: int) -> str | None:
    """Return the primary fingerprint of one good, valid signature.

    Parameters
    ----------
    status : str
        Output of ``gpg --status-fd 1 --verify``.
    returncode : int
        Exit code of that run.

    Returns
    -------
    str | None
        The fingerprint, or ``None`` unless exactly one good and valid
        signature is reported and no rejection is.
    """
    if returncode != 0:
        return None
    lines = [
        line.split()
        for line in status.splitlines()
        if line.startswith("[GNUPG:] ")
    ]
    kinds = [parts[1] for parts in lines if len(parts) > 1]
    if (
        kinds.count("GOODSIG") != 1
        or kinds.count("VALIDSIG") != 1
        or REJECTED_STATUS & set(kinds)
    ):
        return None
    valid = next(parts for parts in lines if parts[1] == "VALIDSIG")
    return valid[11] if len(valid) >= 12 else valid[2]


def _gpg_home(tmp: str) -> list[str]:
    """Create a throwaway keyring and return its option prefix.

    Parameters
    ----------
    tmp : str
        Temporary directory that holds the keyring.

    Returns
    -------
    list[str]
        ``gpg`` options that select the keyring and forbid prompts.
    """
    home = Path(tmp) / "g"
    home.mkdir(mode=0o700)
    return ["--homedir", str(home), "--batch", "--no-autostart"]


def signing_fingerprint(
    digest: str, signature: str, keys: dict[str, str], gpg: str
) -> str | None:
    """Return the primary fingerprint of a valid signature, or None.

    Parameters
    ----------
    digest : str
        Entry digest the signature claims to cover.
    signature : str
        Armored detached signature.
    keys : dict[str, str]
        Armored public keys to verify against, by fingerprint.
    gpg : str
        Absolute path of the ``gpg`` binary.

    Returns
    -------
    str | None
        Fingerprint of the primary key that made a good signature.
    """
    if not keys or not signature:
        return None
    with tempfile.TemporaryDirectory(prefix="sg") as tmp:
        base = [gpg, *_gpg_home(tmp)]
        subprocess.run(
            [*base, "--import"],
            input="\n".join(keys.values()).encode(),
            capture_output=True,
            check=False,
            env=GPG_ENV,
        )
        data, sig = Path(tmp) / "d", Path(tmp) / "d.asc"
        data.write_text(digest, encoding="utf-8")
        sig.write_text(signature, encoding="utf-8")
        done = subprocess.run(
            [*base, "--status-fd", "1", "--verify", str(sig), str(data)],
            capture_output=True,
            check=False,
            env=GPG_ENV,
        )
    return parse_status(done.stdout.decode(errors="replace"), done.returncode)


def key_fingerprint(armored: str, gpg: str = DEFAULT_GPG) -> str | None:
    """Return the primary fingerprint of one armored public key.

    Parameters
    ----------
    armored : str
        Armored public key.
    gpg : str
        Absolute path of the ``gpg`` binary.

    Returns
    -------
    str | None
        The fingerprint, or ``None`` if the text holds no key.
    """
    with tempfile.TemporaryDirectory(prefix="sg") as tmp:
        done = subprocess.run(
            [
                gpg,
                *_gpg_home(tmp),
                "--with-colons",
                "--import-options",
                "show-only",
                "--import",
            ],
            input=armored.encode(),
            capture_output=True,
            check=False,
            env=GPG_ENV,
        )
    for line in done.stdout.decode(errors="replace").splitlines():
        if line.startswith("fpr:"):
            return line.split(":")[9]
    return None
