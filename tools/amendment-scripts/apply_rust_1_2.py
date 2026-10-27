"""Rehearsable minor amendment: STND.RUST 1.2, round of 2026-10-27 (decisions 1 to 3).

One transaction. STND.RUST.24, STND.RUST.25, and STND.RUST.27 keep only the Rust forms of STND.CODE.22,
STND.CODE.24, and STND.CODE.25; STND.RUST.30 keeps only its builds from the revisions that a committed lock file
records, the commitment being STND.DEPS.12. Terms import Foreign interface from STND.CODE, in place of this
standard's Foreign function interface, and Lock file from STND.DEPS. No provision is withdrawn, so that no state of
the round cites a withdrawn identifier: STND.JL cites STND.RUST.24 to STND.RUST.27. Runs after STND.PY 1.2 and
before STND.JL 1.3 and STND.CXX 1.3. Run from harness/:
    python3 -B -m govharness rehearse <corpus holding those amendments> ../tools/amendment-scripts/apply_rust_1_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:07+00:00"
SECTION = "Foreign interfaces"

RUST24 = (
    "Each structure, union, and enumeration that crosses a foreign interface, by value or behind a pointer, and that "
    "the work does not treat as opaque, SHOULD carry a representation attribute that fixes its layout to that of the "
    "corresponding type of the foreign side (DSGN.4). Each pointer or function pointer that the foreign side is able "
    "to pass as null SHOULD be received as a raw pointer or an optional type, and checked before its conversion to a "
    "reference (DSGN.4).")
RUST25 = (
    "Where STND.CODE.24 lets a panic leave a function of the work that a foreign interface invokes, that function "
    "SHOULD be declared with an ABI under which both sides of the interface admit unwinding (DSGN.5).")
RUST27 = (
    "Each type of the work that is the owner of an owned resource under STND.CODE.25 SHOULD release it in its `Drop` implementation "
    "(DSGN.14).")
RUST30 = (
    "Other than the check against newer revisions of STND.RUST.1, each build of the checks and of each release of a "
    "set of crates whose lock file is under version control SHOULD use the revisions that the lock file records, and "
    "fail on a lock file that does not match the package metadata (REPRO.1).")

TEN = [("at a foreign function interface,", "at a foreign interface,")]

SWAPS = [
    ("foreign function interfaces (STND.RUST.24 to STND.RUST.27); build scripts of dependencies, crate features, and "
     "lock files (STND.RUST.28, STND.RUST.29, and STND.RUST.30);",
     "the Rust forms of the rules of STND.CODE on foreign interfaces (STND.RUST.24 to STND.RUST.27); build scripts "
     "of dependencies, crate features, and builds from the revisions that a lock file records (STND.RUST.28, "
     "STND.RUST.29, and STND.RUST.30);"),
    ("Dependency record has the meaning that STND.DEPS gives it;",
     "Foreign interface has the meaning that STND.CODE gives it, and a function that a block of foreign declarations "
     "declares, a function of the work exported with a foreign ABI, and a callback that the work passes to foreign "
     "code are foreign interfaces; Owned resource has the meaning that STND.CODE gives it; the declaration of a function of the work with an ABI under which both sides "
     "of a foreign interface admit unwinding is a statement of the contract of that interface that it carries a "
     "panic on to code of the work, in the sense of STND.CODE.24; Dependency record and Lock file have the meanings "
     "that STND.DEPS gives them;"),
    ("| Foreign function interface | An interface through which Rust code of the work calls, or is called by, code "
     "that does not follow the Rust rules of ownership, borrowing, and unwinding: a function that a block of foreign "
     "declarations declares, a function of the work exported with a foreign ABI, and a callback that the work passes "
     "to such code. |\n", ""),
    ("| Lock file | The file that records, for a set of crates that the work builds together, the exact revision of "
     "each package that their builds resolve and, where the source of a package gives one, its integrity digest. |\n",
     ""),
    ("The lock file records the exact revision of each package (rs1, section 10, S31), and STND.RUST.30 is the Rust "
     "form of STND.JL.4, with its exception for a crate that other work uses and whose builds produce no reported "
     "result; STND.DEPS.6 has the first fetch record a digest where the publisher gives none. The check of "
     "STND.RUST.1 against newer revisions is the one build of the checks that leaves the lock file, and the three "
     "sentences of STND.RUST.30 are one rule for one file.",
     "The lock file records the exact revision of each package (rs1, section 10, S31); STND.DEPS.12 keeps it under "
     "version control where the crates built together produce reported results, and STND.DEPS.6 has the first "
     "fetch record a digest where the publisher gives none. STND.RUST.30 has each build of the checks and of each "
     "release use the revisions of a committed lock file, and the check of STND.RUST.1 against newer revisions is "
     "the one build of the checks that leaves it."),
    ("STND.RUST.1, STND.RUST.7, STND.RUST.11, STND.RUST.22, STND.RUST.24, STND.RUST.25, and STND.RUST.30 each hold "
     "three modals on one subject: the releases of one crate, what one argument rests on, one destructor and its "
     "release, one future, one type at one boundary, one function that a foreign interface invokes, and one file;",
     "STND.RUST.1, STND.RUST.7, STND.RUST.11, and STND.RUST.22 each hold three modals on one subject: the releases of "
     "one crate, what one argument rests on, one destructor and its release, and one future;"),
    ("a function exported over a foreign function interface among them,",
     "a function exported over a foreign interface among them,"),
]

NOTES_FI = (
    "Foreign interfaces. STND.CODE.22 to STND.CODE.26 hold for Rust the types, the layouts, and the arrays that "
    "cross a foreign interface, the failures kept from crossing it, and the owner and the lifetime of what crosses "
    "it, and STND.RUST.24 to STND.RUST.27 add the Rust forms that they need. A structure has the layout of the "
    "corresponding C type only under the representation attribute that fixes it (rs1, section 8, S28), and the "
    "attribute fixes the rules and not the agreement with a header, so STND.RUST.24 asks for the attribute and the "
    "second sentence of STND.CODE.22 compares the two. References, owning boxes, and function pointers are never "
    "null in Rust, and an empty enumeration used as an opaque foreign type leads the compiler to assume that no "
    "value exists (rs1, section 8). An unwinding that reaches a function declared with a non-unwinding ABI ends the "
    "process, one that enters Rust frames from such a declaration is undefined behavior, and the Rustonomicon calls "
    "the catch of an exception of another language undefined where the Reference calls it unspecified (rs1, "
    "section 3); STND.RUST.26 avoids both readings, and STND.RUST.25 lets a panic leave a function that a foreign "
    "interface invokes only under an ABI that admits its unwinding, the Rust form of the exception that the first "
    "sentence of STND.CODE.24 makes. A panic that STND.CODE.24 has caught and stored is answered as STND.RUST.13, "
    "the Rust form of STND.CODE.14, gives. A type of the work that owns an owned resource releases it in its "
    "`Drop` implementation (STND.RUST.27), so that the release follows from the end of its owner. A callback that "
    "foreign code calls after the Rust data that it reaches is released is the hazard of STND.CODE.26, and falls "
    "under STND.CONC.5 where a concurrent task makes the call. The term Undefined behavior includes foreign code "
    "because its undefined behavior is that of the whole program (rs1, section 8).")

READING = (
    "STND.RUST.24 keeps the representation attribute and the null pointers, its comparison of layouts being the "
    "second sentence of STND.CODE.22; STND.RUST.25 keeps only the ABI that admits unwinding for a panic that "
    "STND.CODE.24 lets leave a function that a foreign interface invokes, the catch, the conversion, and the "
    "storing of a panic being STND.CODE.24; STND.RUST.27 keeps only the release in a `Drop` implementation, the "
    "owner of a resource and the pass to it being STND.CODE.25, and is retitled Owned resources released in Drop; "
    "STND.RUST.30 keeps only the builds from the revisions that a committed lock file records, the commitment being "
    "STND.DEPS.12, and is retitled Builds from locked revisions; STND.RUST.24 to STND.RUST.27 move to the section "
    "Foreign interfaces; Terms import Foreign interface from STND.CODE in place of this standard's Foreign function "
    "interface, naming the Rust constructs that are foreign interfaces and reading a declaration with an ABI that "
    "admits unwinding as a statement of the contract that a panic is carried on, and Lock file from STND.DEPS, and "
    "STND.RUST.10 and the Notes use the imported term; the Purpose, the Notes on foreign interfaces and packages, "
    "and the class onset paragraph, which drops STND.RUST.24, STND.RUST.25, and STND.RUST.30 from the provisions of "
    "three modals, follow")
ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.RUST, revision 1.2, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it alters provisions and two defined meanings. The custodian decided that the "
    "shared rules move to STND.CODE and STND.DEPS, that the language standards keep only what their languages add, "
    "and that the lock-file rule is conditioned on reported results (decisions 1 to 3). No provision is withdrawn: "
    "each of the four keeps Rust content, and STND.JL cites STND.RUST.27 until its own amendment, which follows "
    "this one because this one drops the citation of STND.JL.4, so that a withdrawal here would leave a state of "
    "the round that cites a withdrawn identifier. Rust code keeps each outcome of the "
    "removed sentences through STND.CODE.22, STND.CODE.24, and STND.CODE.25, in the same terms, with the release "
    "limited to the owner that the contract states, where STND.RUST.27 let the side and the allocator that the "
    "contract names release it. A function declared with an ABI under which both sides admit "
    "unwinding still lets a panic leave in place of the catch, since Terms read that declaration as the statement "
    "of the contract that the first sentence of STND.CODE.24 asks; STND.RUST.25 still asks that ABI wherever a "
    "panic leaves. STND.CODE.26 adds the lifetime of an object that foreign code keeps, and the release in `Drop` "
    "of STND.RUST.27 now reaches each owned resource that the work owns under STND.CODE.25, and not only one that a "
    "foreign interface creates for it. "
    "STND.DEPS.12 no longer asks the lock file of a set of crates whose builds produce no reported result, which "
    "the first sentence of STND.RUST.30 asked unless other work used the crates; STND.RUST.30 now reaches the "
    "builds of a set of crates whose lock file is under version control. The term of STND.CODE covers the three "
    "parts of the term Foreign function interface, and adds a thread that a foreign runtime starts in Rust code and, "
    "for STND.CODE.24, a structured block of a parallel directive. Each provision concerned is a default, so none raises the floor "
    "(GOV.11). Class onsets: unchanged; the provisions of three modals that the Notes list are those that still "
    "hold three. Transition (GOV.42): none. "
    f"Decisions 1 to 3 of {F.RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    F.set_body(root, "STND/RUST/24.md", RUST24, section=SECTION)
    F.set_body(root, "STND/RUST/25.md", RUST25, section=SECTION, refers_to=["STND.CODE.24"])
    F.set_body(root, "STND/RUST/26.md", (root / "STND/RUST/26.md").read_text(encoding="utf-8")
               .partition("\n---\n\n")[2], section=SECTION)
    F.set_body(root, "STND/RUST/27.md", RUST27, section=SECTION, title="Owned resources released in Drop",
               refers_to=["STND.CODE.25"])
    F.set_body(root, "STND/RUST/30.md", RUST30, title="Builds from locked revisions", instantiates=["REPRO.1"])
    replace_text(root, "STND/RUST/10.md", TEN)
    F.check_fields(root, ["STND.RUST.24", "STND.RUST.25", "STND.RUST.26", "STND.RUST.27", "STND.RUST.30",
                          "STND.RUST.10"])
    replace_text(root, "STND/RUST/_doc.md", SWAPS)
    F.swap_para(root, "STND/RUST/_doc.md", "Foreign function interfaces. The term Foreign function interface",
                NOTES_FI)
    F.finish(root, "STND/RUST", "STND.RUST", "1.1", "1.2", ROW, RATIONALE, AT)
