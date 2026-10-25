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

# ------------------------------------------------------------------ changed provisions: citations and the clause of STND.CODE.19

JL1 = [
    ('refers_to: ["STND.DEPS.3"]', 'refers_to: ["STND.CODE.19", "STND.DEPS.3"]'),
    ("The reference version SHOULD be the latest stable minor version of Julia",
     "Other than for a version that STND.CODE.19 fixes, the reference version SHOULD be the latest stable minor "
     "version of Julia"),
]
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
The type of each argument and of the result that a `ccall` or `@ccall` of the work states SHOULD have the size and the representation of the type that the foreign declaration of the function gives it (DSGN.4). Each struct whose layout the Julia source declares for a foreign interface SHOULD have its size and the offset of each of its fields compared with the foreign declaration by a test (DSGN.4).
""", ["DSGN.4"]),
    P(38, "Julia memory across foreign calls", "Foreign interfaces", """
Each pointer to memory that Julia manages, which the work takes by `pointer` or by another function that returns the address of such memory, SHOULD be used only inside a `GC.@preserve` block that names each object that owns that memory (DSGN.14). Each Julia object that foreign code is able to use after the call that passed it to that code returns, the object that `@cfunction` returns for a closure among them, SHOULD stay referenced by the work for as long as foreign code is able to use it (DSGN.14).
""", ["DSGN.14"]),
    P(39, "Julia exceptions in foreign callbacks", "Foreign interfaces", """
Each Julia function that foreign code invokes through a pointer that `@cfunction` makes SHOULD catch each exception thrown within it (DSGN.5). Where the foreign interface carries errors, an exception so caught, other than an `InterruptException`, SHOULD be converted to an error that the interface carries (DSGN.5). Each other exception so caught SHOULD be stored in an object that code of the work checks after the foreign call returns, and answered there, an `InterruptException` by being thrown again, as STND.JL.16 asks in place of a throw within the callback, and each other exception as STND.JL.15 requires (DSGN.5).
""", ["DSGN.5"], refs=["STND.JL.16", "STND.JL.15"]),
    P(40, "Julia owners of foreign resources", "Foreign interfaces", """
Each resource that foreign code creates for the work SHOULD have one owner that the contract of the interface states, and be released by the function that the contract names, through an object of the work that owns it (DSGN.14).
""", ["DSGN.14"]),
    P(41, "Julia arrays at foreign calls", "Foreign interfaces", """
Each array that the work passes to foreign code by a pointer to its elements SHOULD have, at the call, the element type, the order of dimensions, and the strides that the documentation of the foreign function states, or those that a test of that call confirms (DSGN.4).
""", ["DSGN.4"]),
]

# ------------------------------------------------------------------ the document

PURPOSE = [
    ("and the checks that confirm them at each change (STND.JL.32 to STND.JL.35).",
     "the checks that confirm them at each change, and the bounds checks of the production configuration "
     "(STND.JL.32 to STND.JL.36); and foreign interfaces (STND.JL.37 to STND.JL.41)."),
    ("STND.JL.13 gives STND.CODE.6, and STND.JL.14 and STND.JL.15 give STND.CODE.7, their forms in Julia's "
     "constructs;",
     "STND.JL.13 gives STND.CODE.6, STND.JL.15 gives STND.CODE.14, and STND.JL.14 and STND.JL.15 give STND.CODE.7, "
     "their forms in Julia's constructs;"),
]

TERMS = [
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that "
     "STND.CODE gives them; each function that a package of the work declares by `export` or by `public` belongs to "
     "the public interface that the term Untrusted input of STND.CODE takes in, and an index "
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
    # Arithmetic: STND.CODE.21 for `@fastmath`
    ("`muladd` fuses where the hardware allows, so its result depends on the machine.",
     "`muladd` fuses where the hardware allows, so its result depends on the machine. STND.CODE.21 recommends "
     "against an annotation that, by its documentation, lets the compiler assume finite values in code that holds a "
     "check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs; whether the documentation of "
     "`@fastmath` states that assumption is unverified."),
    # Versions: the edition of high-assurance code (STND.CODE.19)
    ("A qualified revision stays, because no other revision is admissible without new evidence.",
     "A qualified revision stays, because no other revision is admissible without new evidence; STND.CODE.19 fixes, "
     "for high-assurance code, a version of Julia that its high-assurance coding standard covers and for which each "
     "tool that runs that code holds the validation that the work requires; STND.JL.1 yields to it by its own text, "
     "and its third sentence keeps that version as a qualified revision."),
    # Failures: the reach of the term, STND.CODE.6, .14, .15, .16
    ("which also holds that the reach of the term Untrusted input to the arguments of each declared public function "
     "raises no floor.",
     "which also holds that the reach of the term Untrusted input to the arguments of each declared public function "
     "raises no floor. STND.CODE defines the term once, and the Terms above place each declared function in the "
     "public interface that the term takes in, so the reach of the ruling is kept; STND.CODE adds the functions "
     "that the documentation or the repository configuration names for use outside the work. A module "
     "exports names and marks names as public, and the keyword `public` marks a name as part of the public API "
     "without exporting it, from Julia 1.11 (a2, S14); that an exported name is public is the reading of this "
     "standard. STND.CODE.6 states for every language the outcome of which STND.JL.13 gives the Julia forms, "
     "`@assert`, a `@boundscheck` block, and an index that `@inbounds` leaves unchecked. STND.CODE.16 keeps in every "
     "build each check that CPS.5 or CPS.9 requires where those apply, so a `@boundscheck` block, which "
     "`--check-bounds=no` removes, does not hold such a check either. The option emits bounds checks always "
     "under `yes`, never under `no`, and under the default `auto` respects `@inbounds`, which is able to return "
     "incorrect results, crash, or corrupt memory for an index out of bounds (a2, S11 and S12). STND.PY has no counterpart of the third "
     "sentence of STND.JL.13, because the Python interpreter checks each index in every mode, and its Notes say so."),
    ("STND.JL.15 lists the responses of PRIME.4 once, and STND.JL.14 refers to it.",
     "STND.JL.15 lists the responses of PRIME.4 once, in the Julia form of STND.CODE.14, and STND.JL.14 refers to "
     "it; a thrown exception is the pass of a condition to the caller that STND.CODE.14 admits. STND.CODE.15 asks nothing of Julia until a form of declaration under which an ignored result is diagnosed "
     "is among the means of the work, and STND.CODE.7 still forbids discarding a listed failure."),
    # Checking: STND.JL.36 against STND.CXX.27 (sibling list)
    ("which is why STND.JL.34 states the setting.",
     "which is why STND.JL.34 states the setting. Under the default setting of `--check-bounds`, Julia emits "
     "bounds checks other than inside `@inbounds`, whose reason STND.JL.18 asks for at each location, and under "
     "`--check-bounds=no` it emits none for the session (a2, S12), where no location states a reason; that the "
     "same holds for each array type of a package is unverified. STND.JL.36 is therefore the Julia counterpart of STND.CXX.27, which asks "
     "each reporting build of C++ to enable the checks of its standard library: it asks the production "
     "configuration to leave bounds checking on, other than inside `@inbounds`, unless a measurement against a "
     "stated budget and a decision record show its cost, and STND.JL.34 then tests that configuration as it is."),
    # Foreign interfaces (sibling list), before the class paragraph
    ("Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN,",
     "Foreign interfaces. STND.JL.37 to STND.JL.41 give the Julia forms of what STND.CXX.20 and STND.CXX.22, "
     "STND.RUST.24 to STND.RUST.27, and STND.FTN.27 and STND.FTN.28 state for their languages: types and layouts "
     "that match the foreign declaration, memory with a stated lifetime and resources with one owner, and "
     "exceptions kept from crossing into foreign code (DSGN.4, DSGN.14, DSGN.5). No C header is used in a call of "
     "a C function, so the Julia types and call signatures alone state what the header declares, and an "
     "inconsistency is able to work on one system and fail or produce indeterminate results on another (a2, S13). "
     "Base names the C types by aliases: `Cint` is `Int32` on every system, while `Clong` and `Cwchar_t` among "
     "others differ between systems (a2, S13). A test compares the layout of a struct with the foreign declaration "
     "through `sizeof` and `fieldoffset` (unverified); the two sentences of STND.JL.37 are applied apart where the "
     "work declares no struct. A C declaration of a pointer to elements states no order of dimensions and no "
     "strides, so STND.JL.41 takes them from the documentation of the foreign function or from a test, as "
     "STND.FTN.28 tests a section with a stride other than one; that a view of an array is able to have a stride "
     "other than one is unverified for each array type. `GC.@preserve` marks objects as in use during an "
     "expression, which unsafe code needs where the expression uses memory that one of them owns, and without it "
     "the memory behind a pointer taken by `pointer` is able to be collected before its use; the object that "
     "`@cfunction` returns for a closure is kept alive by the work until all uses of it are done (a2, S11 and S13). "
     "STND.JL.38 asks for both, and STND.JL.40 for one owner of each resource that foreign code creates, as "
     "STND.RUST.27 does. STND.JL.18 already asks the reason for each function whose name begins with `unsafe_`, "
     "`unsafe_wrap` and `unsafe_load` among them. A callback exposed through `@cfunction` throws no error in the "
     "manual's practice, because an error returns control to the Julia runtime unexpectedly and is able to leave "
     "the program in an undefined state (a2, S13), so STND.JL.39 catches each exception in the callback. Its three "
     "sentences are one remedy and are not applied apart: an exception caught and neither converted nor stored is "
     "discarded, which STND.CODE.7 forbids for a listed failure, and an `InterruptException` is thrown again after "
     "the foreign call returns, the place where STND.JL.16 is met without a throw through foreign code. "
     "STND.CXX.22, STND.RUST.25, STND.PY.35, and STND.JL.39 take the same steps for an exception or a panic in a "
     "callback: catch it there, then convert it to the error of the interface or answer it after the foreign call "
     "returns.\n\n"
     "Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN,"),
    ("STND.JL.11 and STND.JL.33 ask for mechanical checks (DSGN.3) from CSQ3;",
     "STND.JL.36 instantiates the checking of DSGN.2 that STND.CLASS.10 applies from CSQ1, as STND.CXX.27 does, and "
     "applies from CSQ1. STND.JL.37, STND.JL.39, and STND.JL.41 instantiate the schemas of DSGN.4 and the external "
     "contracts of DSGN.5, which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.JL.38 and STND.JL.40 "
     "rest on no row and apply from CSQ3. STND.JL.11 and STND.JL.33 ask for mechanical checks (DSGN.3) from CSQ3;"),
]

READING = (
    "Terms import Untrusted input from STND.CODE and drop this standard's own definition, and place each function "
    "that a package of the work declares by `export` or by `public` in the public interface that the term of "
    "STND.CODE takes in, and keep the index that `eachindex`, `axes`, or "
    "`CartesianIndices` produces as valid by construction; Terms define Foreign interface; STND.JL.13 cites "
    "STND.CODE.6, and STND.JL.15 STND.CODE.14, for the rule of which each is the Julia form, and neither changes "
    "otherwise; STND.JL.1 yields to a version of Julia that STND.CODE.19 fixes; new STND.JL.36 (default, DSGN.2, RSRC.4, and REPRO.7) has the production configuration leave bounds "
    "checking on outside `@inbounds` unless a measurement and a decision record show its cost, the Julia "
    "counterpart of STND.CXX.27; new STND.JL.37 to STND.JL.41 (defaults, DSGN.4, DSGN.14, and DSGN.5) give the "
    "types and layouts, the lifetime of memory, the exceptions of callbacks, the ownership of resources, and the "
    "layout of arrays at foreign interfaces; "
    "the Purpose lists them; the Notes cite the provisions of STND.CODE of which this standard gives Julia forms, "
    "and state the facts and the onset of each new provision")

ROW = f"| 1.2 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.JL to revision 1.2, ratified by the custodian on {DATE}, on STND.CODE 1.2 and the "
    f"list of differences among sibling language standards of the ratification of 2026-10-24: {READING}. The change "
    "is minor because it adds six defaults and a clause to the default STND.JL.1. The import of Untrusted input "
    "keeps the reach of the definition it replaces, the arguments of each declared function, and adds each function "
    "that the documentation or the repository configuration names for use outside the work, through STND.JL.13 as "
    "well; the custodian decides that widening with STND.CODE 1.2, and if it is declined, the documentation clause "
    "leaves the term of STND.CODE and this standard holds unchanged; the index valid by construction stays outside it. STND.JL.1 yields to "
    "STND.CODE.19, as STND.CXX.2 does, so that the latest stable version does not displace the version that a "
    "high-assurance coding standard and a validated toolchain fix. The citations in STND.JL.13 and STND.JL.15 change their references and not their outcome, and keep "
    "the language forms of the ruling of 2026-10-23. Sibling list: STND.JL.13 stays as ruled, and the Notes of "
    "STND.PY give the reason why Python has no counterpart of its third sentence; STND.JL.36 is the counterpart of "
    "STND.CXX.27, because the option `--check-bounds=no` removes the bounds checks of a whole session where no "
    "location states a reason; logging as the only visible degradation stays as ruled, by decision 7 of that "
    "ratification; STND.JL.37 to STND.JL.41 are the counterparts of STND.CXX.20, STND.CXX.22, STND.RUST.24 to "
    "STND.RUST.27, STND.FTN.27, and STND.FTN.28. Class onsets: STND.JL.36 from CSQ1, as STND.CXX.27; STND.JL.37, "
    "STND.JL.39 and STND.JL.41 from CSQ2; STND.JL.38 and STND.JL.40 from CSQ3; no other onset changes. No floor is raised (GOV.11). Transition "
    "(GOV.42): existing work meets the new defaults when a change next touches the production configuration or the "
    "foreign interface concerned. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-25-close/p2/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/JL/1.md", JL1)
    replace_text(root, "STND/JL/13.md", JL13)
    replace_text(root, "STND/JL/15.md", JL15)
    for p in NEW:
        (root / f"STND/JL/{p['n']}.md").write_text(B.provision_text("STND.JL", p, "adopted", DATE), encoding="utf-8")
    replace_text(root, "STND/JL/_doc.md", PURPOSE + TERMS + NOTES)
    ids = ["STND.JL.1", "STND.JL.13", "STND.JL.15"] + [f"STND.JL.{p['n']}" for p in NEW]
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
