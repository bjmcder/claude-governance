"""Rehearsable minor amendment: STND.PY 1.2, round of 2026-10-27 (decisions 1 to 3).

One transaction. STND.PY.33 is withdrawn, its outcome being STND.DEPS.12; STND.PY.34, STND.PY.36, and STND.PY.37
are withdrawn, their outcomes being STND.CODE.22, STND.CODE.23, STND.CODE.25, and STND.CODE.26; STND.PY.35 keeps
only the Python form of STND.CODE.24 for KeyboardInterrupt and SystemExit. Terms import Foreign interface from
STND.CODE and Lock file from STND.DEPS. Runs after STND.CODE 1.3 and STND.DEPS 1.1, and before STND.JL 1.3, STND.RUST
1.2, and STND.CXX 1.3, whose provisions the Notes no longer cite. Run from harness/:
    python3 -B -m govharness rehearse <corpus holding those amendments> ../tools/amendment-scripts/apply_py_1_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:06+00:00"

PY35 = (
    "Where a Python callable that a foreign interface invokes catches KeyboardInterrupt or SystemExit under "
    "STND.CODE.24, that exception SHOULD be stored in place of its conversion, and raised again after the foreign "
    "call returns, as STND.PY.28 asks (DSGN.5).")

SWAPS = [
    ("the declared and checked releases of Python and of the work's dependencies, and the lock files of the "
     "environments that produce reported results (STND.PY.13, STND.PY.14, and STND.PY.33);",
     "the declared and checked releases of Python and of the work's dependencies (STND.PY.13 and STND.PY.14);"),
    ("and foreign interfaces (STND.PY.34 to STND.PY.37).",
     "and the interrupts of the operator in code that a foreign interface invokes (STND.PY.35)."),
    ("Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and "
     "High-assurance coding standard have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, "
     "High-assurance coding standard, and Foreign interface have the meanings that STND.CODE gives them, and a "
     "function of a compiled extension module, a function that the work loads from a shared library while it runs, "
     "and a Python callable that the work passes to such code are foreign interfaces; Lock file has the meaning "
     "that STND.DEPS gives it;"),
    ("| Lock file | The file that records, for an environment of the work, the exact revision of each package that "
     "its installation resolves and, where the source of a package gives one, its integrity digest. |\n", ""),
    ("| Foreign interface | An interface through which Python code of the work calls, or is called by, code written "
     "in another language, a function of a compiled extension module, a function that the work loads from a shared "
     "library while it runs, and a Python callable that the work passes to such code among them. |\n", ""),
    ("STND.PY.33 keeps a lock file that the tools of the work write under version control wherever the work reports "
     "results, as STND.JL.4 does for a Julia manifest, so that the revisions of a run are those of its source; it "
     "asks for no lock file where the tools write none. STND.RUST.30 differs: it asks that each Rust lock file be "
     "under version control without the condition on reported results, and that builds use the revisions that it "
     "records and fail on a lock file that does not match the package metadata. The term Lock file has the wording "
     "of the term of STND.RUST, with an environment in place of a set of crates built together, because a Python "
     "installation resolves the packages of an environment. ",
     "STND.DEPS.12 keeps a lock file that the tools of the work write under version control wherever an "
     "environment of the work produces reported results, so that the revisions of a run are those of its source; it "
     "asks for no lock file where the tools write none. "),
    ("STND.PY.34, STND.PY.35, and STND.PY.37 instantiate the schemas of DSGN.4 and the external contracts of DSGN.5, "
     "which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.PY.33 and STND.PY.36 rest on no row and apply "
     "from CSQ3.",
     "STND.PY.35 instantiates the external contracts of DSGN.5, which STND.CLASS.10 applies from CSQ2, and applies "
     "from CSQ2."),
]

NOTES_FI = (
    "Foreign interfaces. STND.CODE.22 to STND.CODE.26 hold for Python the types, the layouts, and the arrays that "
    "cross a foreign interface, the failures kept from crossing it, and the owner and the lifetime of what crosses "
    "it, and STND.PY.35 adds the Python form of the interrupts of the operator (DSGN.4, DSGN.5, DSGN.14). A compiled "
    "extension module is built against the declarations of the foreign code, so that its compiler checks the types "
    "of each call (unverified for each build tool). A library that loads a shared library while the program runs "
    "reads no header, and takes the types of each call from what the Python source declares to it, or from "
    "defaults where it is given none (unverified for each library). The ctypes module of the standard library is "
    "unable to determine the signature of a foreign function, checks no number of arguments where none are "
    "declared, and assumes that a function returns a C int unless its result type is declared; incorrect arguments "
    "are able to corrupt memory or crash the interpreter (a2, S8). These hazards are why STND.CODE.22 reaches the "
    "type of each argument and of the result of a function that the Python source declares to such a library, and "
    "the layout of each structure that it declares. A slice of an array is a view whose elements are not always "
    "adjacent in memory (unverified for each array library), and STND.CODE.23 reaches the strides of an array "
    "passed by a pointer to its elements. What a foreign interface does with an exception that a Python callback "
    "raises is unverified for each interface, so STND.CODE.24 asks for the catch unless the contract of the "
    "interface, its documentation among it, states that the exception is passed on. KeyboardInterrupt and "
    "SystemExit are the stop of the operator and the exit of the program, so STND.PY.35 stores them in place of "
    "their conversion and raises them again after the foreign call returns, as STND.PY.28 asks of a handler; each "
    "other exception so caught is answered as STND.PY.22, the Python form of STND.CODE.14, gives. The ctypes module "
    "keeps no reference to a callback object, which the garbage collector is then able to free while C code still "
    "holds it, crashing the program when the callback is made (a2, S8); whether a buffer passed to foreign code is "
    "kept alive is unverified for each interface. STND.CODE.26 asks the work to keep each such object reachable, a "
    "buffer and a callable among them, and STND.CODE.25 gives each resource that foreign code creates one owner.")

READING = (
    "STND.PY.33 is withdrawn, its outcome being STND.DEPS.12 for every language; STND.PY.34, STND.PY.36, and "
    "STND.PY.37 are withdrawn, their outcomes being STND.CODE.22, STND.CODE.23, STND.CODE.25, and STND.CODE.26 for "
    "every language; the front matter lists the four as withdrawn; STND.PY.35 keeps only the storing of "
    "KeyboardInterrupt and SystemExit in place of their conversion, and their raise after the foreign call returns, "
    "the Python form of STND.CODE.24; Terms import Foreign interface from STND.CODE, naming the Python constructs "
    "that are foreign interfaces, and Lock file from STND.DEPS, and drop this standard's own definitions; the "
    "Purpose, and the Notes on versions, foreign interfaces, and onsets, follow")
ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.PY, revision 1.2, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it removes provisions, alters one, and alters two defined meanings. The "
    "custodian decided that the shared rules move to STND.CODE and STND.DEPS and that the provisions they cover "
    "wholly are withdrawn (decisions 1 to 3). Python code keeps each outcome of the withdrawn provisions: the "
    "committed lock file through STND.DEPS.12, in the same form; the declared types and the compared layouts through "
    "STND.CODE.22, which adds the alignment; the arrays through STND.CODE.23, which adds the origin of indexes; one "
    "owner of each foreign resource through STND.CODE.25, which adds the pass to that owner before each other "
    "operation that is able to fail; and the references that foreign code relies on through STND.CODE.26. "
    "STND.PY.35 keeps its treatment of KeyboardInterrupt and SystemExit; the catch, the conversion, and the storing "
    "of each other exception are those of STND.CODE.24, whose exception for an interface that carries the failure "
    "on is the one that STND.PY.35 stated. The withdrawn identifiers are listed in the field withdrawn and are never "
    "given to another provision (STND.IDENT.14). Each provision concerned is a default, so none raises the floor "
    "(GOV.11). Class onsets: STND.PY.35 applies from CSQ2, as before. Transition (GOV.42): none. "
    f"Decisions 1 to 3 of {F.RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    F.withdraw(root, "STND/PY", "STND.PY", [33, 34, 36, 37])
    F.set_body(root, "STND/PY/35.md", PY35, title="Python interrupts in foreign callbacks",
               refers_to=["STND.CODE.24", "STND.PY.28"])
    F.check_fields(root, ["STND.PY.35"])
    replace_text(root, "STND/PY/_doc.md", SWAPS)
    F.swap_para(root, "STND/PY/_doc.md", "Foreign interfaces. STND.PY.34 to STND.PY.37", NOTES_FI)
    F.finish(root, "STND/PY", "STND.PY", "1.1", "1.2", ROW, RATIONALE, AT)
