"""Regression guard: the package reproduces the flat tools byte for byte,
except where a recorded fix changed behavior on purpose.

Usage::

    python -B tests/equivalence/run_equivalence.py [--work DIR]

This compares the new code only with the earlier code, so it is a
regression guard, not evidence of correctness (VV.7). It runs the
pre-package scripts kept in ``archive/tools-flat/`` (the reference,
unit 0001 criterion 8) and ``python -m govharness`` on identical inputs
and compares the bytes of every output: the standard output and exit
code of ``verify``, ``check --out-dir`` (with its three files),
``manifests --check``, ``references --check``, and ``sign check`` of the
corpus ledger.

The inputs are copies of ``governance/``: the live corpus, one damaged
copy per family (structure, manifests, ledger chain, two kinds of
signature damage, lineage, drafting, revision, identifier, and logic),
and one input per behavior that review 0001 changed on purpose (an
unflagged non-waivable provision, a drafting provision citing a v key,
a renumbered ledger entry, and a root that does not exist). Every copy,
and every output, lives under the work directory, which is created
fresh; the source corpus is only read. The signature inputs are built
with fresh ``gpg`` keys, so their bytes differ from run to run, while
the old and new outputs of one run must still agree.

``INTENDED`` lists each (input, command) whose outputs are meant to
differ, with the reason and the record of the change. Such a pair must
differ in at least one output, so that the listed fix is seen to act;
every other output must be identical.

The report is a Markdown table on standard output with the SHA-256 of
each output (the old one, and the new one where they differ). The exit
code is 1 when an output differs without being intended, or an intended
difference does not occur.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
# The harness runs as a script; the repository root on the path gives it
# the keyring helpers, which import nothing from the package compared.
sys.path.insert(0, str(REPO))
from tests.gpgkeys import keyring, make_key  # noqa: E402

OLD = REPO / "archive" / "tools-flat"
SOURCE = REPO / "governance"
PYTHON = [sys.executable, "-B"]
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
CHECK_FILES = ("logic_report.md", "logic_facts.json", "drafting_punch_list.md")
GARBLED_SIGNATURE = (
    "-----BEGIN PGP SIGNATURE-----\n\ngarbled\n-----END PGP SIGNATURE-----\n"
)
Mutation = Callable[[Path, Path], None]


@dataclass
class Output:
    """One compared output.

    Parameters
    ----------
    input_name : str
        Name of the input corpus.
    command : str
        Command, as ``python -m govharness`` names it.
    name : str
        ``stdout``, ``exit``, or a file name.
    old : bytes
        Output of the flat tools.
    new : bytes
        Output of the package.
    """

    input_name: str
    command: str
    name: str
    old: bytes
    new: bytes

    def digest(self) -> str:
        """Return the SHA-256 of the old output.

        Returns
        -------
        str
            Hexadecimal digest.
        """
        return hashlib.sha256(self.old).hexdigest()


# --- building the damaged inputs ------------------------------------------


def _replace(root: Path, rel: str, old: str, new: str) -> None:
    """Replace every occurrence of a text in one corpus file.

    Parameters
    ----------
    root : Path
        Corpus copy.
    rel : str
        File path relative to the copy.
    old, new : str
        Text replaced and its replacement.

    Raises
    ------
    AssertionError
        If the text does not occur, so that a stale mutation fails
        loudly instead of comparing two undamaged runs.
    """
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, (rel, old)
    path.write_text(text.replace(old, new), encoding="utf-8")


def _entry_hash(entry: dict[str, object]) -> str:
    """Return the ledger hash of an entry, as the ledger defines it.

    Parameters
    ----------
    entry : dict[str, object]
        Ledger entry.

    Returns
    -------
    str
        SHA-256 of the canonical JSON of every field but ``hash``.
    """
    fields = {k: v for k, v in entry.items() if k != "hash"}
    text = json.dumps(
        fields, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(text.encode()).hexdigest()


def _rewrite_ledger(
    root: Path, edit: Callable[[list[dict[str, object]]], None], rechain: bool
) -> None:
    """Edit the ledger entries of a copy and write them back.

    Parameters
    ----------
    root : Path
        Corpus copy.
    edit : Callable[[list[dict[str, object]]], None]
        Changes the entries in place.
    rechain : bool
        Whether to recompute every ``prev`` and ``hash`` afterwards, so
        that only the edit itself is visible.
    """
    path = root / "ledger.jsonl"
    entries = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    edit(entries)
    if rechain:
        previous = None
        for entry in entries:
            entry["prev"] = previous
            entry["hash"] = _entry_hash(entry)
            previous = entry["hash"]
    lines = [
        json.dumps(
            e, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        for e in entries
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def live(root: Path, work: Path) -> None:
    """Leave the copy undamaged.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """


def structure(root: Path, work: Path) -> None:
    """Give a document an identifier that differs from its path, and add
    a top-level directory that is no mnemonic.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "STND/ANNEX/_doc.md", 'id: "STND.ANNEX"', 'id: "STND.ANNX"')
    (root / "Bad1").mkdir()


def manifests(root: Path, work: Path) -> None:
    """Make one manifest row stale.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "STND/DRAFT/MANIFEST.csv", ",Modal set,", ",Modal sets,")


def ledger_chain(root: Path, work: Path) -> None:
    """Alter one ledger entry and break the link of another.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """

    def edit(entries: list[dict[str, object]]) -> None:
        """Alter entry 5's reason; relink entry 7 to a false hash.

        Parameters
        ----------
        entries : list[dict[str, object]]
            Ledger entries; changed in place.
        """
        entries[4]["rationale"] = str(entries[4]["rationale"]) + " altered"
        entries[6]["prev"] = "0" * 64
        entries[6]["hash"] = _entry_hash(entries[6])

    _rewrite_ledger(root, edit, rechain=False)


def signature_unregistered(root: Path, work: Path) -> None:
    """Put a garbled signature on an entry of a corpus without a register.

    The chain is recomputed, so only the signature check can see it.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """

    def edit(entries: list[dict[str, object]]) -> None:
        """Sign entry 12 with garbage.

        Parameters
        ----------
        entries : list[dict[str, object]]
            Ledger entries; changed in place.
        """
        entries[11]["signature"] = GARBLED_SIGNATURE

    _rewrite_ledger(root, edit, rechain=True)


def _old_tool(*args: str) -> None:
    """Run one flat tool to build an input.

    Parameters
    ----------
    *args : str
        Script name and arguments.
    """
    subprocess.run(
        [*PYTHON, *args], cwd=OLD, env=ENV, check=True, capture_output=True
    )


def _register(root: Path, scope: str, key: str, home: Path) -> None:
    """Append a signed register transaction with the flat ledger tool.

    Parameters
    ----------
    root : Path
        Corpus copy.
    scope : str
        Scope the transaction pins.
    key : str
        Fingerprint that signs.
    home : Path
        Keyring directory.
    """
    _old_tool(
        "ledger.py",
        str(root),
        "--type",
        "register",
        "--actor",
        "The Custodian",
        "--role",
        "custodians",
        "--authority",
        "GOV.36",
        "--targets",
        scope,
        "--scope",
        scope,
        "--rationale",
        "Test.",
        "--at",
        "2026-10-10T00:00:00+00:00",
        "--sign",
        key,
        "--gnupg-home",
        str(home),
    )


def signature_forged(root: Path, work: Path) -> None:
    """Found a signer register, then append an entry an intruder signs.

    The register is founded and pinned by the owner's key; the last
    entry carries a signature by a key the register does not hold.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input; holds the owner's public key.
    """
    with keyring() as home:
        _sign_forged(root, work, home)


def _sign_forged(root: Path, work: Path, home: Path) -> None:
    """Build the forged-signature input with keys from one keyring.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    home : Path
        Keyring directory.
    """
    owner, owner_key = make_key(home, "Owner")
    intruder, _ = make_key(home, "Intruder")
    key_file = work / "owner.asc"
    key_file.write_text(owner_key, encoding="utf-8")
    _old_tool(
        "signatures.py",
        "found",
        str(root),
        "--date",
        "2026-10-10",
        "--role",
        "The Custodian",
        "--name",
        "O",
        "--key-file",
        str(key_file),
    )
    _old_tool("build_manifests.py", str(root))
    _register(root, "MNEM", owner, home)
    _register(root, "SIGNR", owner, home)
    _old_tool(
        "ledger.py",
        str(root),
        "--type",
        "annotate",
        "--actor",
        "The Custodian",
        "--role",
        "custodians",
        "--rationale",
        "Forged.",
        "--at",
        "2026-10-10T00:00:00+00:00",
        "--sign",
        intruder,
        "--gnupg-home",
        str(home),
    )


def lineage(root: Path, work: Path) -> None:
    """Mark an instantiator of a prime directive waivable (l.3, l.5).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "STND/DRAFT/19.md", "waivable: false", "waivable: true")


def drafting(root: Path, work: Path) -> None:
    """Use an excluded expression and drop a References row (g.5, g.25).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    path = root / "STND" / "DRAFT" / "2.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.rstrip("\n") + " An actor must record it.\n", encoding="utf-8"
    )
    _replace(root, "STND/CLASS/_doc.md", "| VV | Correctness |\n", "")


def revision(root: Path, work: Path) -> None:
    """Set the LVL0 revision ahead of its history (v.3).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "LVL0/_doc.md", 'revision: "1.5"', 'revision: "1.0.9"')


def identifier(root: Path, work: Path) -> None:
    """Narrow a registered grade scale and cite a malformed identifier.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "MNEM/_doc.md", "| 0 to 3 |", "| 1 to 3 |")
    _replace(
        root, "STND/CLASS/1.md", "refers_to: [", 'refers_to: ["Stnd.class.3", '
    )


def logic(root: Path, work: Path) -> None:
    """Rank VV twice and let a GUARD provision be waived (a, b, f.1).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "GOV/5.md", "process (QA)", "process (VV)")
    path = root / "GUARD" / "9.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.rstrip("\n") + " This MAY be waived.\n", encoding="utf-8"
    )


def unflagged_waiver(root: Path, work: Path) -> None:
    """Drop the ``waivable`` field of a prime directive (b.2).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(root, "PRIME/2.md", "waivable: false\n", "")


def cited_v_key(root: Path, work: Path) -> None:
    """Let a drafting provision cite a revision check (g.23).

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """
    _replace(
        root,
        "STND/DRAFT/1.md",
        'checked_by: ["g.1", "g.2"]',
        'checked_by: ["g.1", "g.2", "v.1"]',
    )


def renumbered_entry(root: Path, work: Path) -> None:
    """Renumber ledger entry 3 as 4 and rebuild every link and hash.

    Parameters
    ----------
    root : Path
        Corpus copy.
    work : Path
        Scratch directory of this input.
    """

    def edit(entries: list[dict[str, object]]) -> None:
        """Give entry 3 the number 4.

        Parameters
        ----------
        entries : list[dict[str, object]]
            Ledger entries; changed in place.
        """
        entries[2]["seq"] = 4

    _rewrite_ledger(root, edit, rechain=True)


INPUTS: dict[str, Mutation] = {
    "live": live,
    "structure": structure,
    "manifests": manifests,
    "ledger-chain": ledger_chain,
    "signature-unregistered": signature_unregistered,
    "signature-forged": signature_forged,
    "lineage": lineage,
    "drafting": drafting,
    "revision": revision,
    "identifier": identifier,
    "logic": logic,
    "unflagged-waiver": unflagged_waiver,
    "cited-v-key": cited_v_key,
    "renumbered-entry": renumbered_entry,
}
# An input whose root is never created.
ABSENT_INPUTS = ("missing-root",)
# The (input, command) pairs whose outputs differ on purpose, with the
# reason. Defects 1 to 4 are those of the record of unit 0001.
NO_REGISTER = (
    "sign check: a corpus without a signer register is a failure line, "
    "not a traceback (defect 3; review 0001)"
)
MISSING = (
    "a root that is no directory is a usage error, exit 2 (defect 4; "
    "review 0001)"
)
INTENDED: dict[tuple[str, str], str] = {
    ("unflagged-waiver", "verify"): (
        "b.2 reports a non-waivable provision with no flag (defect 1; "
        "review 0001)"
    ),
    ("unflagged-waiver", "check --out-dir"): (
        "b.2 reports a non-waivable provision with no flag (defect 1; "
        "review 0001)"
    ),
    ("cited-v-key", "verify"): (
        "g.23 knows every registered key, v.1 included (defect 2; review 0001)"
    ),
    ("cited-v-key", "check --out-dir"): (
        "g.23 knows every registered key, v.1 included (defect 2; review 0001)"
    ),
    ("renumbered-entry", "verify"): (
        "verify compares each sequence number with its position (review 0001)"
    ),
    **{
        ("missing-root", command): MISSING
        for command in (
            "verify",
            "check --out-dir",
            "manifests --check",
            "references --check",
            "sign check",
        )
    },
}
# The built-in solver is compared on two inputs, one satisfiable and one
# not; z3, when importable, serves every other run.
BUILTIN_SOLVER_INPUTS = {"live", "logic"}


# --- running both and comparing -------------------------------------------


def _run(command: list[str], cwd: Path) -> tuple[bytes, bytes]:
    """Run one command and return its output and exit code.

    Parameters
    ----------
    command : list[str]
        The command.
    cwd : Path
        Working directory.

    Returns
    -------
    tuple[bytes, bytes]
        Standard output, and the exit code as text.
    """
    done = subprocess.run(command, cwd=cwd, env=ENV, capture_output=True)
    return done.stdout, str(done.returncode).encode()


def _pair(
    name: str,
    command: str,
    old: list[str],
    new: list[str],
) -> list[Output]:
    """Run the old and the new form of one command.

    Parameters
    ----------
    name : str
        Input name.
    command : str
        Command label.
    old : list[str]
        Arguments of the flat tool, script first.
    new : list[str]
        Arguments of ``python -m govharness``.

    Returns
    -------
    list[Output]
        The standard output and the exit code.
    """
    old_out, old_code = _run([*PYTHON, str(OLD / old[0]), *old[1:]], REPO)
    new_out, new_code = _run([*PYTHON, "-m", "govharness", *new], REPO)
    return [
        Output(name, command, "stdout", old_out, new_out),
        Output(name, command, "exit", old_code, new_code),
    ]


def compare_input(name: str, root: Path, out: Path) -> list[Output]:
    """Run every compared command on one input.

    Parameters
    ----------
    name : str
        Input name.
    root : Path
        Corpus copy.
    out : Path
        Directory for the files that ``check`` writes.

    Returns
    -------
    list[Output]
        Every compared output.
    """
    corpus = str(root)
    results = _pair(name, "verify", ["verify.py", corpus], ["verify", corpus])
    solvers = [("", [])]
    if name in BUILTIN_SOLVER_INPUTS:
        solvers.append((" --no-z3", ["--no-z3"]))
        results += _pair(
            name,
            "verify --no-z3",
            ["verify.py", corpus, "--no-z3"],
            ["verify", "--no-z3", corpus],
        )
    for label, flags in solvers:
        old_dir, new_dir = out / f"old{label}", out / f"new{label}"
        command = f"check --out-dir{label}"
        results += _pair(
            name,
            command,
            ["check_logic.py", corpus, "--out-dir", str(old_dir), *flags],
            ["check", corpus, "--out-dir", str(new_dir), *flags],
        )
        for file in CHECK_FILES:
            results.append(
                Output(
                    name,
                    command,
                    file,
                    _contents(old_dir / file),
                    _contents(new_dir / file),
                )
            )
    results += _pair(
        name,
        "manifests --check",
        ["build_manifests.py", corpus, "--check"],
        ["manifests", corpus, "--check"],
    )
    results += _pair(
        name,
        "references --check",
        ["references.py", corpus, "--check"],
        ["references", corpus, "--check"],
    )
    ledger = str(root / "ledger.jsonl")
    sign = [ledger, "--ledger-id", "governance", "--corpus", corpus]
    results += _pair(
        name,
        "sign check",
        ["signatures.py", "check", *sign],
        ["sign", "check", *sign],
    )
    return results


def _contents(path: Path) -> bytes:
    """Return a file's bytes, or a marker when the run wrote no file.

    Parameters
    ----------
    path : Path
        Output file.

    Returns
    -------
    bytes
        Its contents, or ``<absent>``.
    """
    return path.read_bytes() if path.is_file() else b"<absent>"


def intended(name: str, command: str, root: Path) -> str | None:
    """Return why the outputs of a command on an input may differ.

    Parameters
    ----------
    name : str
        Input name.
    command : str
        Command label.
    root : Path
        The input's corpus root.

    Returns
    -------
    str | None
        The reason from ``INTENDED``, the reason for ``sign check`` on a
        corpus with no signer register, or ``None`` when old and new
        must agree.
    """
    if (name, command) in INTENDED:
        return INTENDED[(name, command)]
    if command == "sign check" and not (root / "SIGNR" / "_doc.md").exists():
        return NO_REGISTER
    return None


def build_inputs(work: Path) -> dict[str, Path]:
    """Copy the corpus once per input and damage each copy.

    Parameters
    ----------
    work : Path
        Fresh work directory.

    Returns
    -------
    dict[str, Path]
        Corpus copy by input name.
    """
    roots: dict[str, Path] = {
        name: work / name / "absent" for name in ABSENT_INPUTS
    }
    for name, mutate in INPUTS.items():
        scratch = work / name
        scratch.mkdir(parents=True)
        root = scratch / "governance"
        shutil.copytree(SOURCE, root)
        mutate(root, scratch)
        roots[name] = root
    return roots


def render(results: list[Output], reasons: dict[tuple[str, str], str]) -> str:
    """Render the comparison as a Markdown table.

    Parameters
    ----------
    results : list[Output]
        Every compared output.
    reasons : dict[tuple[str, str], str]
        Reason by (input, command) for the outputs meant to differ.

    Returns
    -------
    str
        One row per output with its SHA-256 (old, then new where they
        differ) and whether old and new are identical, then the reason
        of each intended difference.
    """
    lines = [
        "| Input | Command | Output | SHA-256 | Identical |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in results:
        key = (r.input_name, r.command)
        if r.old == r.new:
            same = "yes"
        else:
            same = "no, intended" if key in reasons else "NO"
        shown = r.old.decode() if r.name == "exit" else r.digest()
        if r.old != r.new:
            new = r.new.decode() if r.name == "exit" else _digest(r.new)
            shown += f" → {new}"
        lines.append(
            f"| {r.input_name} | `{r.command}` | {r.name} | {shown} | {same} |"
        )
    lines += ["", "Intended differences:", ""]
    lines += [
        f"- {name}, `{command}`: {reason}"
        for (name, command), reason in reasons.items()
    ]
    return "\n".join(lines)


def _digest(data: bytes) -> str:
    """Return the SHA-256 of some bytes.

    Parameters
    ----------
    data : bytes
        Output bytes.

    Returns
    -------
    str
        Hexadecimal digest.
    """
    return hashlib.sha256(data).hexdigest()


def verdicts(
    results: list[Output], reasons: dict[tuple[str, str], str]
) -> tuple[list[Output], list[tuple[str, str]]]:
    """Return the unintended differences and the intended ones missing.

    Parameters
    ----------
    results : list[Output]
        Every compared output.
    reasons : dict[tuple[str, str], str]
        Reason by (input, command) for the outputs meant to differ.

    Returns
    -------
    tuple[list[Output], list[tuple[str, str]]]
        Outputs that differ with no reason, and the (input, command)
        pairs meant to differ whose outputs are all identical.
    """
    stray = [
        r
        for r in results
        if r.old != r.new and (r.input_name, r.command) not in reasons
    ]
    seen = {(r.input_name, r.command) for r in results if r.old != r.new}
    missing = [key for key in reasons if key not in seen]
    return stray, missing


def main() -> int:
    """Build the inputs, compare every output, and print the table.

    Returns
    -------
    int
        1 when an output differs without being intended, or an intended
        difference does not occur; else 0.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--work", type=Path, default=None)
    args = parser.parse_args()
    if args.work is None:
        work = Path(tempfile.mkdtemp(prefix="equivalence-"))
    else:
        args.work.mkdir(parents=True)
        work = args.work
    roots = build_inputs(work / "inputs")
    results: list[Output] = []
    reasons: dict[tuple[str, str], str] = {}
    for name, root in roots.items():
        out = work / "outputs" / name
        out.mkdir(parents=True)
        found = compare_input(name, root, out)
        results += found
        for r in found:
            reason = intended(name, r.command, root)
            if reason is not None:
                reasons[(name, r.command)] = reason
    print(render(results, reasons))
    stray, missing = verdicts(results, reasons)
    print(f"\nWork directory: {work}")
    print(
        f"Outputs compared: {len(results)}; differing: "
        f"{sum(r.old != r.new for r in results)}; not intended: "
        f"{len(stray)}; intended but not seen: {len(missing)}"
    )
    for name, command in missing:
        print(f"intended difference not seen: {name}, `{command}`")
    return 1 if stray or missing else 0


if __name__ == "__main__":
    sys.exit(main())
