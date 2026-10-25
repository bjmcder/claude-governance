"""Rehearsable minor amendment: STND.JL 1.2, on STND.CODE 1.2 and the sibling list of decision 10 (one transaction).

It imports Untrusted input from STND.CODE and deletes its own definition, keeping the declared names and the
indices valid by construction as Julia content; cites STND.CODE.6 from STND.JL.13 and STND.CODE.14 from STND.JL.15;
and adds STND.JL.36 (default, bounds checks in the production configuration) and STND.JL.37 to STND.JL.39
(defaults, foreign interfaces). It applies after STND.CODE 1.2, which it cites: apply_close_p2.py runs it after
apply_close_p1.py and apply_py_1_1.py, whose STND.PY.35 its Notes name. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.2> ../tools/amendment-scripts/apply_jl_1_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:25:00+00:00"

# ------------------------------------------------------------------ changed provisions: citations only

JL13 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.6"]'),
    ("A check of untrusted input SHALL NOT be written with `@assert` (PRIME.4, DSGN.2).",
     "A check of untrusted input SHALL NOT be written with `@assert` (PRIME.4, DSGN.2, STND.CODE.6)."),
]
JL15 = [
    ('refers_to: ["PRIME.13"]', 'refers_to: ["PRIME.13", "STND.CODE.14"]'),
    ("degrade visibly with a diagnosis, or return the condition in its result (PRIME.4).",
     "degrade visibly with a diagnosis, or return the condition in its result (PRIME.4, STND.CODE.14)."),
]

# ------------------------------------------------------------------ new provisions

NEW = [
    P(36, "Bounds checks in production", "Checking", """
The production configuration SHOULD leave bounds checking on for all code other than code inside `@inbounds` (DSGN.2). Where a measurement shows that bounds checking exceeds a stated budget, a decision record SHOULD state the measurement and the setting of the production configuration that turns bounds checking off (RSRC.4, REPRO.7).
""", ["DSGN.2", "RSRC.4", "REPRO.7"]),
    P(37, "Julia foreign call types", "Foreign interfaces", """
The type of each argument and of the result that a `ccall` or `@ccall` of the work states SHOULD have the size and the representation of the type that the foreign declaration of the function gives it (DSGN.4). Each struct whose layout the Julia source declares for a foreign interface SHOULD have its size and the offset of each of its fields compared with the foreign declaration by a test (DSGN.4). Each array that the work passes to foreign code by a pointer to its elements SHOULD have, at the call, the element type, the order of dimensions, and the strides that the foreign declaration states (DSGN.4).
""", ["DSGN.4"]),
    P(38, "Julia memory across foreign calls", "Foreign interfaces", """
Each pointer to memory that Julia manages, other than an argument that a `ccall` converts for the duration of that call, SHOULD be used only inside a `GC.@preserve` block that names each object that owns that memory (DSGN.14). Each Julia object that foreign code is able to use after the call that passed it to that code returns, a closure behind a pointer that `@cfunction` makes among them, SHOULD stay referenced by the work for as long as foreign code is able to use it (DSGN.14). Each resource that foreign code creates for the work SHOULD be released by the function that the contract of the interface names, through an object of the work that owns it (DSGN.14).
""", ["DSGN.14"]),
    P(39, "Julia exceptions in foreign callbacks", "Foreign interfaces", """
Each Julia function that foreign code invokes through a pointer that `@cfunction` makes SHOULD catch each exception thrown within it (DSGN.5). Where the foreign interface carries errors, an exception so caught SHOULD be converted to an error that the interface carries (DSGN.5). Where the foreign interface carries no error, an exception so caught SHOULD be stored in an object that code of the work checks after the foreign call returns, and answered there as STND.JL.15 requires (DSGN.5).
""", ["DSGN.5"], refs=["STND.JL.15"]),
]

# ------------------------------------------------------------------ the document

PURPOSE = [
    ("and the checks that confirm them at each change (STND.JL.32 to STND.JL.35).",
     "the checks that confirm them at each change, and the bounds checks of the production configuration "
     "(STND.JL.32 to STND.JL.36); and foreign interfaces (STND.JL.37, STND.JL.38, and STND.JL.39)."),
    ("STND.JL.13 gives STND.CODE.6, and STND.JL.14 and STND.JL.15 give STND.CODE.7, their forms in Julia's "
     "constructs;",
     "STND.JL.13 gives STND.CODE.6, STND.JL.15 gives STND.CODE.14, and STND.JL.14 and STND.JL.15 give STND.CODE.7, "
     "their forms in Julia's constructs;"),
]

TERMS = [
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that "
     "STND.CODE gives them; each function that a package of the work declares by `export` or by `public` is one "
     "that this standard places in the public interface of the work under the term Untrusted input, and an index "
     "that `eachindex`, `axes`, or `CartesianIndices` of the indexed array produces is valid by construction and is "
     "not untrusted input;"),
    ("| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each "
     "function that a package of the work declares by `export` or by `public`, other than data from a source that "
     "the threat model of the project records as trusted. An index that `eachindex`, `axes`, or `CartesianIndices` of "
     "the indexed array produces is valid by construction and is not untrusted input. |\n", ""),
    ("| Type piracy | The definition of a method of a function that no module of the work defines, with no owned "
     "type among the types of its arguments. |",
     "| Type piracy | The definition of a method of a function that no module of the work defines, with no owned "
     "type among the types of its arguments. |\n"
     "| Foreign interface | An interface through which Julia code of the work calls, or is called by, code written "
     "in another language, a call by `ccall` or `@ccall` and a Julia function that the work passes to such code by "
     "a pointer that `@cfunction` makes among them. |"),
]

NOTES = [
    # Versions: the edition of high-assurance code (STND.CODE.19)
    ("A qualified revision stays, because no other revision is admissible without new evidence.",
     "A qualified revision stays, because no other revision is admissible without new evidence; STND.CODE.19 fixes, "
     "for high-assurance code, a version of Julia that its high-assurance coding standard covers and for which its "
     "toolchain is validated, and the third sentence of STND.JL.1 keeps that version as a qualified revision."),
    # Failures: the reach of the term, STND.CODE.6, .14, .15, .16
    ("which also holds that the reach of the term Untrusted input to the arguments of each declared public function "
     "raises no floor.",
     "which also holds that the reach of the term Untrusted input to the arguments of each declared public function "
     "raises no floor. STND.CODE defines the term once, and the Terms above place each declared function in the "
     "public interface of the work that the definition names, so the reach stays the one of the ruling; the "
     "functions that the documentation or the repository configuration names for use outside the work belong to it "
     "as well. STND.CODE.6 states for every language the outcome of which STND.JL.13 gives the Julia forms, "
     "`@assert`, a `@boundscheck` block, and an index that `@inbounds` leaves unchecked. STND.CODE.16 keeps in every "
     "build each check that CPS.5 or CPS.9 requires where those apply, so a `@boundscheck` block, which "
     "`--check-bounds=no` removes, does not hold such a check either. STND.PY has no counterpart of the third "
     "sentence of STND.JL.13, because the Python interpreter checks each index in every mode, and its Notes say so."),
    ("STND.JL.15 lists the responses of PRIME.4 once, and STND.JL.14 refers to it.",
     "STND.JL.15 lists the responses of PRIME.4 once, in the Julia form of STND.CODE.14, and STND.JL.14 refers to "
     "it. STND.CODE.15 asks nothing of Julia until a form of declaration under which an ignored result is diagnosed "
     "is among the means of the work, and STND.CODE.7 still forbids discarding a listed failure."),
    # Checking: STND.JL.36 against STND.CXX.27 (sibling list)
    ("which is why STND.JL.34 states the setting.",
     "which is why STND.JL.34 states the setting. Julia checks the bounds of each index in every session, other "
     "than inside `@inbounds`, whose reason STND.JL.18 asks for at each location, and other than under the option "
     "`--check-bounds=no`, which removes the checks of the whole session, those of its dependencies included, "
     "where no location states a reason. STND.JL.36 is therefore the Julia counterpart of STND.CXX.27, which asks "
     "each reporting build of C++ to enable the checks of its standard library: it asks the production "
     "configuration to leave bounds checking on, other than inside `@inbounds`, unless a measurement against a "
     "stated budget and a decision record show its cost, and STND.JL.34 then tests that configuration as it is."),
    # Foreign interfaces (sibling list), before the class paragraph
    ("Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN,",
     "Foreign interfaces. STND.JL.37, STND.JL.38, and STND.JL.39 give the Julia forms of what STND.CXX.20 and "
     "STND.CXX.22, STND.RUST.24 to STND.RUST.27, and STND.FTN.27 and STND.FTN.28 state for their languages: types "
     "that match the foreign declaration, memory with one owner and a stated lifetime, and exceptions kept from "
     "crossing into foreign code (DSGN.4, DSGN.14, DSGN.5). A `ccall` reads no C header: it converts each argument "
     "to the type that the call states and reads the result as the stated type, so a type that differs in size from "
     "the foreign declaration passes or returns a wrong value without an error (unverified). Base names the C types "
     "by aliases, `Cint`, `Csize_t`, and `Cdouble` among them, whose sizes follow the platform (unverified), and "
     "`sizeof` and `fieldoffset` give the layout of a struct that a test compares with the foreign declaration. An "
     "array is stored in column-major order, and a view of it is able to have a stride other than one (unverified "
     "for each array type), which is why STND.JL.37 asks for the order and the strides at the call, as STND.FTN.28 "
     "tests them for Fortran. A `ccall` keeps its arguments alive for the duration of the call, while a pointer "
     "taken by `pointer` and used after the expression that took it is valid only while `GC.@preserve` roots its "
     "owner, and a function pointer that `@cfunction` makes from a closure is valid only while the closure is "
     "referenced (unverified); STND.JL.38 asks for both. STND.JL.18 already asks the reason for each function whose "
     "name begins with `unsafe_`, `unsafe_wrap` and `unsafe_load` among them. A Julia exception thrown in a function "
     "that foreign code invokes through `@cfunction` would unwind through frames of that code, which the code does "
     "not expect (unverified), so STND.JL.39 catches it in the callback and has it answered after the foreign call "
     "returns, as STND.JL.15 requires; an `InterruptException` so stored is thrown again there, as STND.JL.16 asks. "
     "The rule is stated alike for C++, Rust, Python, and Julia (STND.CXX.22, STND.RUST.25, STND.PY.35, "
     "STND.JL.39).\n\n"
     "Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN,"),
    ("STND.JL.11 and STND.JL.33 ask for mechanical checks (DSGN.3) from CSQ3;",
     "STND.JL.36 instantiates the checking of DSGN.2 that STND.CLASS.10 applies from CSQ1, as STND.CXX.27 does, and "
     "applies from CSQ1. STND.JL.37 and STND.JL.39 instantiate the schemas of DSGN.4 and the external contracts of "
     "DSGN.5, which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.JL.38 rests on no row and applies "
     "from CSQ3. STND.JL.11 and STND.JL.33 ask for mechanical checks (DSGN.3) from CSQ3;"),
]

READING = (
    "Terms import Untrusted input from STND.CODE and drop this standard's own definition, and place each function "
    "that a package of the work declares by `export` or by `public` in the public interface of the work that the "
    "definition of STND.CODE names, so the reach stays the same, and keep the index that `eachindex`, `axes`, or "
    "`CartesianIndices` produces as valid by construction; Terms define Foreign interface; STND.JL.13 cites "
    "STND.CODE.6, and STND.JL.15 STND.CODE.14, for the rule of which each is the Julia form, and neither changes "
    "otherwise; new STND.JL.36 (default, DSGN.2, RSRC.4, and REPRO.7) has the production configuration leave bounds "
    "checking on outside `@inbounds` unless a measurement and a decision record show its cost, the Julia "
    "counterpart of STND.CXX.27; new STND.JL.37, STND.JL.38, and STND.JL.39 (defaults, DSGN.4, DSGN.14, and DSGN.5) "
    "give the types, the lifetime and ownership of memory, and the exceptions of callbacks at foreign interfaces; "
    "the Purpose lists them; the Notes cite the provisions of STND.CODE of which this standard gives Julia forms, "
    "and state the facts and the onset of each new provision")

ROW = f"| 1.2 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.JL to revision 1.2, ratified by the custodian on {DATE}, on STND.CODE 1.2 and the "
    f"list of differences among sibling language standards of the ratification of 2026-10-24: {READING}. The change "
    "is minor because it adds four defaults. The import of Untrusted input changes no obligation: the definition of "
    "STND.CODE, with the declared names that the Terms place in the public interface, has the reach of the "
    "definition it replaces, together with each function that the documentation or the repository configuration "
    "names, the reach that the ratification of 2026-10-24 gave the term; the index valid by construction stays "
    "outside it. The citations in STND.JL.13 and STND.JL.15 change their references and not their outcome, and keep "
    "the language forms of the ruling of 2026-10-23. Sibling list: STND.JL.13 stays as ruled, and the Notes of "
    "STND.PY give the reason why Python has no counterpart of its third sentence; STND.JL.36 is the counterpart of "
    "STND.CXX.27, because the option `--check-bounds=no` removes the bounds checks of a whole session where no "
    "location states a reason; logging as the only visible degradation stays as ruled, by decision 7 of that "
    "ratification; STND.JL.37 to STND.JL.39 are the counterparts of STND.CXX.20, STND.CXX.22, STND.RUST.24 to "
    "STND.RUST.27, STND.FTN.27, and STND.FTN.28. Class onsets: STND.JL.36 from CSQ1, as STND.CXX.27; STND.JL.37 and "
    "STND.JL.39 from CSQ2; STND.JL.38 from CSQ3; no other onset changes. No floor is raised (GOV.11). Transition "
    "(GOV.42): existing work meets the new defaults when a change next touches the production configuration or the "
    "foreign interface concerned. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-25-close/p2/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/JL/13.md", JL13)
    replace_text(root, "STND/JL/15.md", JL15)
    for p in NEW:
        (root / f"STND/JL/{p['n']}.md").write_text(B.provision_text("STND.JL", p, "adopted", DATE), encoding="utf-8")
    replace_text(root, "STND/JL/_doc.md", PURPOSE + TERMS + NOTES)
    ids = ["STND.JL.13", "STND.JL.15"] + [f"STND.JL.{p['n']}" for p in NEW]
    res = B.derive_fields(root, ids)
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    for p in NEW:
        if res[f"STND.JL.{p['n']}"].forced:
            raise ValueError(f"STND.JL.{p['n']}: forced binding, drafted as a default")
    raise_revision(root, "STND/JL", "1.1", "1.2", ROW)
    B.write_references(root, ["STND.JL"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.JL"], scope=["STND/JL"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.JL 1.2")
