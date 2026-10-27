"""Rehearsable minor amendment: STND.CXX 1.3, round of 2026-10-27 (decision 1).

One transaction. STND.CXX.20 and STND.CXX.22 are withdrawn, their outcomes being STND.CODE.25 and STND.CODE.24 for
every language; STND.CXX.5 cites STND.CODE.25 in place of STND.CXX.20; Terms import Foreign interface from
STND.CODE. Runs last, after every amendment of the round that dropped a citation of STND.CXX.20 or STND.CXX.22.
Run from harness/:
    python3 -B -m govharness rehearse <corpus holding those amendments> ../tools/amendment-scripts/apply_cxx_1_3.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:09+00:00"

CXX5 = [("or of a wrapper under STND.CXX.20 (DSGN.14).",
         "or of an object that owns a foreign resource under STND.CODE.25 (DSGN.14).")]

SWAPS = [
    ("It covers failures, including the option that assumes finite values, the boundaries to code that does not "
     "follow C++ rules, and the terminate handler (STND.CXX.18, STND.CXX.19, STND.CXX.20, STND.CXX.21, STND.CXX.22, "
     "STND.CXX.23, STND.CXX.24, STND.CXX.32, and STND.CXX.33),",
     "It covers failures, including the option that assumes finite values, the status returns and the releases of "
     "foreign functions, and the terminate handler (STND.CXX.18, STND.CXX.19, STND.CXX.21, STND.CXX.23, "
     "STND.CXX.24, STND.CXX.32, and STND.CXX.33),"),
    ("and recorded deviations (STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, "
     "STND.CODE.20, and STND.CODE.21); the Notes give their C++ forms.",
     "and recorded deviations (STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, "
     "STND.CODE.20, and STND.CODE.21), and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26); the "
     "Notes give their C++ forms."),
    ("Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and "
     "High-assurance coding standard have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, "
     "High-assurance coding standard, Foreign interface, and Owned resource have the meanings that STND.CODE gives "
     "them, and a C or "
     "vendor library interface, and a callback or a thread that such a library or a runtime starts, are foreign "
     "interfaces;"),
    ("| Foreign interface | An interface through which C++ code of the work calls, or is called by, code that does "
     "not follow the C++ rules of ownership and exceptions: a C or vendor library interface, a callback or thread "
     "that such a library or a runtime starts, and a structured block of a compiler directive for parallel "
     "execution. |\n", ""),
    ("| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that "
     "code acquires and has to release. |\n", ""),
    ("An owning raw pointer appears only inside a resource handle or in the wrapper of STND.CXX.20,",
     "An owning raw pointer appears only inside a resource handle or in an object that owns a foreign resource "
     "under STND.CODE.25,"),
    ("into its handle before the next call that is able to fail (STND.CXX.20).",
     "into its handle before the next call that is able to fail (STND.CODE.25)."),
    ("STND.CXX.22 keeps a C++ exception out of C frames,", "STND.CODE.24 keeps a C++ exception out of C frames,"),
    ("and STND.CXX.21 and STND.CXX.22 DSGN.5, which STND.CLASS.10 applies from CSQ2.",
     "and STND.CXX.21 DSGN.5, which STND.CLASS.10 applies from CSQ2."),
]

READING = (
    "STND.CXX.20 and STND.CXX.22 are withdrawn, their outcomes being STND.CODE.25 and STND.CODE.24 for every "
    "language, and the front matter lists them as withdrawn; STND.CXX.5 cites STND.CODE.25 in place of "
    "STND.CXX.20; Terms import Foreign interface from STND.CODE, naming the C++ constructs that are foreign "
    "interfaces, and Owned resource, which STND.CODE now defines in the words of this standard, and drop this "
    "standard's own definitions; the Purpose lists STND.CODE.22 to STND.CODE.26 and drops "
    "the withdrawn provisions; the Notes cite STND.CODE.24 and STND.CODE.25 in their place")
ROW = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CXX, revision 1.3, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it removes two provisions and alters a defined meaning. The custodian decided "
    "that the shared rules on foreign interfaces move to STND.CODE and that the provisions they cover wholly are "
    "withdrawn (decision 1). C++ code keeps each outcome of the withdrawn provisions: the pass of a resource that a "
    "foreign interface creates to an object that owns it, before each other operation that is able to fail, "
    "through the second sentence of STND.CODE.25, the resource handle of the work being that object; the release "
    "of no resource that the interface predefines or that another component owns through its first sentence, which "
    "has each resource released only by the owner that the contract states; and the catch, the conversion, and the "
    "storing of a C++ exception through STND.CODE.24, which leaves uncaught an exception that the contract of the "
    "interface carries on to code of the work. STND.CODE.22, STND.CODE.23, and STND.CODE.26 add the layouts, the "
    "arrays, and the lifetime of an object that foreign code keeps to C++. The term of STND.CODE covers each part "
    "of the term of this standard, the structured block of a parallel directive among them for STND.CODE.24, the "
    "one rule that applied to it through STND.CXX.22, and reaches only code in the same process; a structured block "
    "is no longer a foreign interface for STND.CXX.4, STND.CXX.6, STND.CXX.8, or STND.CXX.10, none of which "
    "concerns it. STND.CXX.20 had the foreign resource pass to a resource handle, a type that also defines or "
    "deletes its copy and move operations, and STND.CODE.25 asks an object of the work that owns it and releases "
    "it; STND.CXX.5 has that object release it in its destructor, but no longer asks it to be a resource handle, a "
    "narrowing that the custodian is asked to accept. The withdrawn identifiers are listed in the field withdrawn and are never given "
    "to another provision (STND.IDENT.14). Each provision concerned is a default, so none raises the floor "
    "(GOV.11). Class onsets: STND.CODE.24 applies from CSQ2, as STND.CXX.22 did, and STND.CODE.25 from CSQ3, as "
    f"STND.CXX.20 did. Transition (GOV.42): none. Decision 1 of {F.RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    F.withdraw(root, "STND/CXX", "STND.CXX", [20, 22])
    replace_text(root, "STND/CXX/5.md", CXX5)
    F.set_body(root, "STND/CXX/5.md", (root / "STND/CXX/5.md").read_text(encoding="utf-8").partition("\n---\n\n")[2],
               refers_to=["STND.CODE.25", "STND.CXX.25"])
    F.check_fields(root, ["STND.CXX.5"])
    replace_text(root, "STND/CXX/_doc.md", SWAPS)
    F.finish(root, "STND/CXX", "STND.CXX", "1.2", "1.3", ROW, RATIONALE, AT)
