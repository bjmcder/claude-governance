"""Rehearsable minor amendment: STND.JL 1.3, round of 2026-10-27 (decisions 1 to 3).

One transaction. STND.JL.4 is withdrawn, its outcome being STND.DEPS.12; STND.JL.37, STND.JL.40, and STND.JL.41
are withdrawn, their outcomes being STND.CODE.22, STND.CODE.23, and STND.CODE.25; STND.JL.38 keeps only its
`GC.@preserve` block, and STND.JL.39 only the Julia form of STND.CODE.24 for an `InterruptException`. Terms import
Foreign interface from STND.CODE and Lock file from STND.DEPS. Runs after STND.PY 1.2 and STND.RUST 1.2, which no
longer cite STND.JL.4, and before STND.CXX 1.3. Run from harness/:
    python3 -B -m govharness rehearse <corpus holding those amendments> ../tools/amendment-scripts/apply_jl_1_3.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:08+00:00"

JL38 = (
    "Each pointer to memory that Julia manages, which the work takes by `pointer` or by another function that "
    "returns the address of such memory, SHOULD be used only inside a `GC.@preserve` block that names each object "
    "that owns that memory (DSGN.14).")
JL39 = (
    "Where a Julia function that foreign code invokes through a pointer that `@cfunction` makes catches an "
    "`InterruptException` under STND.CODE.24, that exception SHOULD be stored in place of its conversion, and thrown "
    "again after the foreign call returns, as STND.JL.16 asks in place of a throw within the callback (DSGN.5).")

SWAPS = [
    ("its bounds, checks, manifests, and run records (STND.JL.1 to STND.JL.5);",
     "its bounds, checks, and run records (STND.JL.1, STND.JL.2, STND.JL.3, and STND.JL.5);"),
    ("and foreign interfaces (STND.JL.37 to STND.JL.41).",
     "and memory and interrupts at foreign interfaces (STND.JL.38 and STND.JL.39)."),
    ("Qualified revision has the meaning that STND.DEPS gives it;",
     "Foreign interface has the meaning that STND.CODE gives it, and a call by `ccall` or `@ccall`, and a Julia "
     "function that the work passes to foreign code by a pointer that `@cfunction` makes, are foreign interfaces; "
     "Qualified revision and Lock file have the meanings that STND.DEPS gives them, and the manifest file of an "
     "environment is its lock file;"),
    ("| Foreign interface | An interface through which Julia code of the work calls, or is called by, code written in "
     "another language, a call by `ccall` or `@ccall` and a Julia function that the work passes to such code by a "
     "pointer that `@cfunction` makes among them. |\n", ""),
    ("so STND.JL.1 to STND.JL.4 separate the reference version, the bounds, the revisions checked, and the "
     "manifests.",
     "so STND.JL.1, STND.JL.2, and STND.JL.3 separate the reference version, the bounds, and the revisions checked, "
     "and STND.DEPS.12 keeps the manifests under version control."),
    ("A manifest named for a Julia version is the manifest file of STND.JL.4 where it exists,",
     "A manifest named for a Julia version is the manifest file of its environment where it exists,"),
    ("STND.JL.37, STND.JL.39, and STND.JL.41 instantiate the schemas of DSGN.4 and the external contracts of DSGN.5, "
     "which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.JL.38 and STND.JL.40 rest on no row and apply "
     "from CSQ3.",
     "STND.JL.39 instantiates the external contracts of DSGN.5, which STND.CLASS.10 applies from CSQ2, and applies "
     "from CSQ2; STND.JL.38 rests on no row and applies from CSQ3."),
]

NOTES_FI = (
    "Foreign interfaces. STND.CODE.22 to STND.CODE.26 hold for Julia the types, the layouts, and the arrays that "
    "cross a foreign interface, the failures kept from crossing it, and the owner and the lifetime of what crosses "
    "it, and STND.JL.38 and STND.JL.39 add the Julia forms that they need (DSGN.4, DSGN.5, DSGN.14). No C header is "
    "used in a call of a C function, so the Julia types and call signatures alone state what the header declares, "
    "and an inconsistency is able to work on one system and fail or produce indeterminate results on another (a2, "
    "S13); the types that a `ccall` or `@ccall` states are the Julia side of the first sentence of STND.CODE.22. "
    "Base names the C types by aliases: `Cint` is `Int32` on every system, while `Clong` and `Cwchar_t` among "
    "others differ between systems (a2, S13). A test compares the layout of a struct with the foreign declaration "
    "through `sizeof` and `fieldoffset` (unverified), the comparison of the second sentence of STND.CODE.22. That a "
    "view of an array is able to have a stride other than one is unverified for each array type. `GC.@preserve` "
    "marks objects as in use during an expression, which unsafe code needs where the expression uses memory that "
    "one of them owns, and without it the memory behind a pointer taken by `pointer` is able to be collected before "
    "its use (STND.JL.38); the object that `@cfunction` returns for a closure is kept alive by the work until all "
    "uses of it are done (a2, S11 and S13), which STND.CODE.26 asks. STND.JL.18 already asks the reason for each "
    "function whose name begins with `unsafe_`, `unsafe_wrap` and `unsafe_load` among them. A callback exposed "
    "through `@cfunction` throws no error in the manual's practice, because an error returns control to the Julia "
    "runtime unexpectedly and is able to leave the program in an undefined state (a2, S13), so STND.CODE.24 "
    "catches each exception in the callback. An `InterruptException` so caught is stored and thrown again after the "
    "foreign call returns (STND.JL.39), the place where STND.JL.16 is met without a throw through foreign code; "
    "each other exception so caught is answered as STND.JL.15, the Julia form of STND.CODE.14, gives.")

READING = (
    "STND.JL.4 is withdrawn, its outcome being STND.DEPS.12 for every language; STND.JL.37, STND.JL.40, and "
    "STND.JL.41 are withdrawn, their outcomes being STND.CODE.22, STND.CODE.25, and STND.CODE.23 for every "
    "language; the front matter lists the four as withdrawn; STND.JL.38 keeps only its `GC.@preserve` block, the "
    "lifetime of an object that foreign code keeps being STND.CODE.26; STND.JL.39 keeps only the storing of an "
    "`InterruptException` in place of its conversion, and its throw after the foreign call returns, the Julia form "
    "of STND.CODE.24; Terms import Foreign interface from STND.CODE, naming the Julia constructs that are foreign "
    "interfaces, and Lock file from STND.DEPS, the manifest file of an environment being its lock file, and drop "
    "this standard's own definition; the Purpose, and the Notes on versions, foreign interfaces, and onsets, follow")
ROW = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.JL, revision 1.3, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it removes provisions, alters two, and alters a defined meaning. The custodian "
    "decided that the shared rules move to STND.CODE and STND.DEPS and that the provisions they cover wholly are "
    "withdrawn (decisions 1 to 3). Julia code keeps each outcome of the withdrawn provisions and sentences: the "
    "committed manifest through STND.DEPS.12, in the same form, the manifest being the lock file of its "
    "environment; the types and the compared layouts through STND.CODE.22, which adds the alignment; the arrays "
    "through STND.CODE.23, which adds the origin of indexes; one owner of each foreign resource through "
    "STND.CODE.25, which adds the pass to that owner before each other operation that is able to fail; and the "
    "references that foreign code relies on through STND.CODE.26. STND.JL.39 keeps its treatment of an "
    "`InterruptException`; the catch, the conversion, and the storing of each other exception are those of "
    "STND.CODE.24, which also leaves uncaught a failure that the contract of the interface carries on to code of "
    "the work. The withdrawn identifiers are listed in the field withdrawn and are never given to another "
    "provision (STND.IDENT.14). Each provision concerned is a default, so none raises the floor (GOV.11). Class "
    "onsets: STND.JL.38 from CSQ3 and STND.JL.39 from CSQ2, as before. Transition (GOV.42): none. "
    f"Decisions 1 to 3 of {F.RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    F.withdraw(root, "STND/JL", "STND.JL", [4, 37, 40, 41])
    F.set_body(root, "STND/JL/38.md", JL38)
    F.set_body(root, "STND/JL/39.md", JL39, title="Julia interrupts in foreign callbacks",
               refers_to=["STND.CODE.24", "STND.JL.16"])
    F.check_fields(root, ["STND.JL.38", "STND.JL.39"])
    replace_text(root, "STND/JL/_doc.md", SWAPS)
    F.swap_para(root, "STND/JL/_doc.md", "Foreign interfaces. STND.JL.37 to STND.JL.41", NOTES_FI)
    F.finish(root, "STND/JL", "STND.JL", "1.2", "1.3", ROW, RATIONALE, AT)
