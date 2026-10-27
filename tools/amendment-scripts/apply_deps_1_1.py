"""Rehearsable minor amendment: STND.DEPS 1.1, round of 2026-10-27 (decisions 2 and 3).

One transaction. Terms define Lock file once, and new STND.DEPS.12 keeps under version control the lock file of
each environment or build that produces reported results, the rule that STND.PY.33 and STND.JL.4 held for their
languages and the first sentences of STND.RUST.30 for Rust. It applies before the amendments of STND.PY, STND.JL,
and STND.RUST, which cite it. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_deps_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import fi_common as F  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:01+00:00"

DEPS12 = P(12, "Lock files under version control", "Records", """
Where the tools of the work write a lock file for an environment or a build that produces reported results, that lock file SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9).
""", ["REPRO.1", "REPRO.9"])

PURPOSE = [(
    "how fetched components are verified, and what the dependency record holds.",
    "how fetched components are verified, what the dependency record holds, and which lock files are kept under "
    "version control.")]

TERMS = [(
    "| Integrity digest | A cryptographic hash of the exact content of a component, recorded so that a later copy "
    "is checked against it. |\n",
    "| Integrity digest | A cryptographic hash of the exact content of a component, recorded so that a later copy "
    "is checked against it. |\n"
    "| Lock file | The file that records, for an environment or a set of packages that the work installs or builds "
    "together, the exact revision of each package that their resolution selects and, where the source of a package "
    "gives one, its integrity digest. |\n")]

NOTES = [(
    "STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity.",
    "STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity. A lock "
    "file records the revisions that an environment or a build resolved, so that a result is regenerated with the "
    "same packages (REPRO.1); STND.DEPS.12 keeps it under version control where the environment or the build "
    "produces reported results, and asks for no lock file where the tools write none. A package that other work "
    "uses, and whose own environments and builds produce no reported result, leaves its dependents to resolve their "
    "own, and STND.DEPS.12 does not reach its lock file. STND.PY, STND.JL, and STND.RUST name the lock files of "
    "their languages, the manifest of a Julia environment among them, and STND.RUST.30 adds builds from the "
    "revisions that a committed lock file records.")]

READING = (
    "Terms define Lock file once, for an environment or a set of packages installed or built together; new "
    "STND.DEPS.12 (default, REPRO.1 and REPRO.9) keeps under version control the lock file that the tools of the "
    "work write for an environment or a build that produces reported results, the rule that STND.PY.33 and "
    "STND.JL.4 held for their languages and the first two sentences of STND.RUST.30 for Rust; the Purpose and the "
    "Notes name it")
ROW = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.DEPS, revision 1.1, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it adds a default provision and a defined meaning. The custodian decided that "
    "STND.DEPS holds the term and the rule, and that the rule takes the form of STND.PY.33 and STND.JL.4, "
    "conditioned on reported results, so that it carries the least burden (decisions 2 and 3). For Python and Julia "
    "it asks what those provisions asked. For Rust it no longer asks the lock file of a set of crates whose builds "
    "produce no reported result, which the first sentence of STND.RUST.30 asked unless the crates were used by "
    "other work; the third sentence of STND.RUST.30 stays a Rust rule. It applies to every other language whose "
    "tools write a lock file. It is a default that a recorded decision replaces (GOV.19), so it raises no floor "
    "(GOV.11). Class onset: from CSQ3, as every default of this standard. Transition (GOV.42): an existing lock file "
    "of an environment that produces reported results is committed at the next change of that environment. "
    f"Decisions 2 and 3 of {F.RECORD}; finding S4 of "
    "review-records/round-2026-10-25-close/reconciliation-alignment.md." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/DEPS/12.md").write_text(B.provision_text("STND.DEPS", DEPS12, "adopted", F.DATE),
                                          encoding="utf-8")
    F.check_fields(root, ["STND.DEPS.12"])
    replace_text(root, "STND/DEPS/_doc.md", PURPOSE + TERMS + NOTES)
    F.finish(root, "STND/DEPS", "STND.DEPS", "1.0", "1.1", ROW, RATIONALE, AT)
