"""Rehearsable minor amendment: STND.CODE 1.3, round of 2026-10-27 (decisions 1 and 4).

One transaction. New STND.CODE.22 to STND.CODE.26 state for every language the rules on foreign interfaces that
STND.CXX, STND.STDC, STND.PY, STND.JL, and STND.RUST held each for its own language, and Terms define Foreign
interface once. It applies first, since the amendments of the language standards cite the new provisions. Run from
harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_code_1_3.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import fi_common as F  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:00+00:00"

NEW = [
    P(22, "Data at foreign interfaces", "Foreign interfaces", """
Each type of data that crosses a foreign interface SHOULD have, on each side of the interface, the size, the alignment, and the representation that the contract of the interface fixes for it (DSGN.4). Each structure, union, or other compound type whose layout the work declares on one side of a foreign interface SHOULD have its size, its alignment, and the offset of each of its fields compared with the declaration of the other side, by a check during compilation or by a test (DSGN.4).
""", ["DSGN.4"]),
    P(23, "Arrays at foreign interfaces", "Foreign interfaces", """
Each array that crosses a foreign interface SHOULD have, at each call that passes it, the element type, the order of its dimensions, the origin of its indexes, and the strides that the contract of the interface states, or that a test of that call confirms (DSGN.4).
""", ["DSGN.4"]),
    P(24, "Failures crossing foreign interfaces", "Foreign interfaces", """
Unless the contract of a foreign interface states that the interface carries a failure across the foreign code and on to code of the work, each failure raised in code of the work that the interface invokes, and propagated by a mechanism of the language of that code, an exception or a panic among them, SHOULD be caught within that code (DSGN.5). Where the interface carries errors, a failure so caught SHOULD be converted to an error that the interface carries (DSGN.5). Where the interface carries no error, a failure so caught SHOULD be stored in an object that code of the work checks after the invocation returns, and answered there as STND.CODE.14 requires (DSGN.5).
""", ["DSGN.5"], refs=["STND.CODE.14"]),
    P(25, "Ownership at foreign interfaces", "Foreign interfaces", """
Each owned resource that crosses a foreign interface SHOULD have one owner that the contract of the interface states, and be released only by that owner, through the function and the allocator that the contract names for it (DSGN.14). Each owned resource that a foreign interface creates for the work SHOULD pass to an object of the work that owns it and releases it, before each other operation that is able to fail (DSGN.14).
""", ["DSGN.14"]),
    P(26, "Objects that foreign code keeps", "Foreign interfaces", """
Each object of the work that foreign code is able to use after the call that passed it to that code returns SHOULD stay allocated, and reachable from objects of the work, for as long as foreign code is able to use it (DSGN.14).
""", ["DSGN.14"]),
]

PURPOSE = [(
    "and recommends against an assumption of finite values in code that holds such a check (STND.CODE.21).",
    "and recommends against an assumption of finite values in code that holds such a check (STND.CODE.21). It states "
    "what code keeps true at a foreign interface: the types, the layouts, and the arrays that cross it, the failures "
    "that it keeps from crossing, one owner for each owned resource that crosses it, and the lifetime of each object that "
    "foreign code keeps (STND.CODE.22 to STND.CODE.26).")]

TERMS = [(
    "| Execution setting | An option, flag, or variable of a compiler, interpreter, build, or run that changes which "
    "code executes. |\n",
    "| Execution setting | An option, flag, or variable of a compiler, interpreter, build, or run that changes which "
    "code executes. |\n"
    "| Foreign interface | An interface through which code of the work in one language calls, or is called by, code "
    "in the same process that does not follow the rules of that language for ownership, lifetime, and the "
    "propagation of failures, code written in another language among it. A function that the work declares for "
    "such code or loads from it, a function of the work that such code invokes, and a thread that a runtime of such "
    "code starts in code of the work are foreign interfaces. The contract of a foreign interface includes the "
    "declaration of each of its functions in its own language and the documentation of the interface. For "
    "STND.CODE.24 alone, a structured block of a "
    "compiler directive for parallel execution is also a foreign interface, which carries no error and whose "
    "invocation returns at the end of the block. |\n"
    "| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that "
    "code acquires and has to release. |\n")]

NOTES = (
    "Foreign interfaces. The terms Foreign interface and Owned resource are defined here once, and the language "
    "standards import them, the term Foreign interface each naming the constructs of its language that are foreign "
    "interfaces (GOV.31). Code on the other side of a foreign interface does not check what code of the work "
    "assumes of it: the types and the layout of the data that cross, which failures leave a function and how, and "
    "who releases what and when. STND.CODE.22 to STND.CODE.26 state those assumptions as parts of the contract "
    "that DSGN.5 asks for each external component, and the language standards add only what their constructs make "
    "necessary: the representation attribute and the null pointers of STND.RUST.24, the unwinding of STND.RUST.25 "
    "and STND.RUST.26, the release of STND.RUST.27, the interoperable kinds and the strided sections of "
    "STND.FTN.27 and STND.FTN.28, the preserved memory of STND.JL.38, the interrupts of the operator in STND.PY.35 "
    "and STND.JL.39, and the status returns and releases of STND.CXX.21. The two sentences of STND.CODE.22 are the "
    "schema of one type at one boundary (DSGN.4): the second applies to a layout that the work declares again, "
    "apart from the declaration that the other side compiles, and is not applied without the first. A C "
    "declaration of a pointer to elements states no order of dimensions and no strides, so STND.CODE.23 takes them "
    "from the contract or from a test of the call. STND.CODE.24 keeps a failure from crossing code that does not "
    "propagate it: ISO C++ defines no behavior for an exception that unwinds through C frames, the specification "
    "of a structured block of a parallel directive requires an exception raised in it to be caught there, and an "
    "unwinding that enters Rust frames from a non-unwinding declaration is undefined behavior (the Notes of "
    "STND.CXX and STND.RUST). Its three sentences are one remedy and are not applied apart: a failure caught and "
    "neither converted nor stored is discarded, which STND.CODE.7 forbids for a listed failure. STND.PY.35 and "
    "STND.JL.39 store an interrupt of the operator in place of its conversion and raise it again after the foreign "
    "call returns, and the form of STND.CODE.14 in each language answers each other failure so stored. A language "
    "that propagates no failure by a mechanism of its own, Fortran among them, meets STND.CODE.24 with nothing. "
    "STND.CODE.25 gives each owned resource that crosses one owner, as DSGN.14 asks of state, and an owned "
    "resource that the interface predefines has the interface as its owner. Its second sentence applies to an "
    "owned resource that the interface creates for the work, and names its owner on the side of the work; the "
    "first applies to every owned resource that crosses, and the second is not applied without it. STND.CODE.26 "
    "keeps an object that foreign code still uses from being released or collected under it: a callback that "
    "foreign code calls after the data that it reaches is released is its hazard, and STND.CONC.5 governs the same "
    "hazard between concurrent tasks. STND.CODE.22 to STND.CODE.26 apply to the C, Fortran, and Lean source of the "
    "work, and to a hardware description, for each foreign interface that it declares, beside what STND.FTN.27 and "
    "STND.FTN.28 state. The structured block of a parallel directive is a foreign interface for STND.CODE.24 "
    "alone, the one rule that the terms of STND.CXX and STND.STDC applied to it, since the data and the resources "
    "of a block have no contract of an interface that fixes their layout or their owner. STND.CODE.22 and "
    "STND.CODE.23 rest on the schema of each data structure that crosses an interface (DSGN.4), and STND.CODE.24 "
    "on the contract of each external component (DSGN.5), rows that STND.CLASS.10 applies from CSQ2, so they apply "
    "from CSQ2; STND.CODE.25 and STND.CODE.26 rest on DSGN.14 and on no row, and apply from CSQ3.")

CLASS = [(
    "Under STND.CLASS.10, each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, and "
    "STND.CODE.21 instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies from CSQ3; work of CSQ4 omits "
    "it. The onsets of STND.CODE.17, STND.CODE.19, STND.CODE.20, and STND.CODE.21 are stated above.",
    "Under STND.CLASS.10, each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, "
    "STND.CODE.22, STND.CODE.23, and STND.CODE.24 instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies "
    "from CSQ3; work of CSQ4 omits it. The onsets of STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, "
    "STND.CODE.22, STND.CODE.23, and STND.CODE.24 are stated above.")]

READING = (
    "new STND.CODE.22 to STND.CODE.26 (defaults; DSGN.4, DSGN.5, and DSGN.14) state for every language the rules on "
    "foreign interfaces that STND.CXX, STND.STDC, STND.PY, STND.JL, and STND.RUST held each for its own: the types "
    "and the layouts that cross an interface (STND.CODE.22) and its arrays (STND.CODE.23); a failure raised in code "
    "that the interface invokes, caught there unless the contract carries it on, and converted to an error of the "
    "interface or stored and answered after the call (STND.CODE.24); one owner for each owned resource that crosses, "
    "and an object of the work that owns each owned resource that the interface creates for it (STND.CODE.25); and a stated "
    "lifetime for each object that foreign code keeps (STND.CODE.26); Terms define Foreign interface once, with what its contract includes, and Owned resource, from STND.CXX; the "
    "Purpose lists the new provisions; the Notes give their reasons, their reach in each language, and their onsets")
ROW = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CODE, revision 1.3, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it adds five default provisions and two defined meanings. The custodian decided "
    "that the shared rules move here, that the language standards keep only what their languages add, and that the "
    "rules reach every language (decisions 1 and 4). Against the provisions that they replace, the new ones ask "
    "these things more: the alignment of each type and of each compared layout in Python and Julia; the origin of "
    "indexes of an array in Python and Julia; the alignment, the compared layouts of a structure, and the element "
    "type and the strides of an array, of one dimension or more, in C; the arrays of STND.CODE.23, with their "
    "element type and strides, in C++ and Rust; the pass of a foreign resource to its owner before each other "
    "operation that is able to fail in Python and Julia; the lifetime of an object that foreign code keeps in C++, "
    "C, and Rust; the layout rules in C++; and each of the five in Fortran, Lean, and hardware descriptions, where "
    "those have a foreign interface. They ask this less: a call to code in another process is no longer at a "
    "foreign interface, where the terms of STND.PY, STND.JL, and STND.STDC reached it by the words code written in "
    "another language; in C++ and Julia, a failure that the contract of the "
    "interface carries on to code of the work is left uncaught, as STND.PY.35 already allowed, and in C a test of "
    "the call confirms the layout of an array where the contract states it nowhere. Each is a default, a tightening "
    "above the floor that a recorded decision replaces (PRIME.15, GOV.19), so none raises the floor (GOV.11). Class "
    "onsets: STND.CODE.22, STND.CODE.23, and STND.CODE.24 apply from CSQ2, as the provisions on DSGN.4 and DSGN.5 "
    "that they replace did, and STND.CODE.25 and STND.CODE.26 from CSQ3. Transition (GOV.42): existing code "
    "conforms when a change next touches the foreign interface. "
    f"Decisions 1 and 4 of {F.RECORD}; decision 26 of review-records/round-2026-10-25-close/decisions-final.md."
    + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    for p in NEW:
        (root / f"STND/CODE/{p['n']}.md").write_text(B.provision_text("STND.CODE", p, "adopted", F.DATE),
                                                    encoding="utf-8")
    F.check_fields(root, [f"STND.CODE.{p['n']}" for p in NEW])
    replace_text(root, "STND/CODE/_doc.md", PURPOSE + TERMS + CLASS)
    swap_onset = "Under STND.CLASS.10, each default provision other than"
    path = root / "STND/CODE/_doc.md"
    text = path.read_text(encoding="utf-8")
    if text.count(swap_onset) != 1:
        raise ValueError("STND.CODE: the onset paragraph is not unique")
    path.write_text(text.replace(swap_onset, NOTES + "\n\n" + swap_onset, 1), encoding="utf-8")
    F.finish(root, "STND/CODE", "STND.CODE", "1.2", "1.3", ROW, RATIONALE, AT)
