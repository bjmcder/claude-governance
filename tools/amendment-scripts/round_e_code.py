"""Round e of 2026-10-28, part 3: the code standards, in citation order.

STND.FTN (CL19, CL20), STND.DEPS (one default for checks across declared ranges, CL7; CL20), STND.CODE (CL19; the
Notes drop the copies), STND.BUILD (its Notes cite STND.CODE.21 and STND.DEPS.14), STND.SV, STND.STDC, STND.LEAN, and
STND.CXX (the copies of STND.CODE.21 and STND.CODE.28 that round d left withdrawn), STND.JL (CL7, CL22), STND.RUST
(CL7, CL9), and STND.PY (CL7). Each document drops its citations of a provision before the document that holds that
provision withdraws it.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
import round_e_base as E  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

F1 = E.ruling("F1")
D1 = E.ruling("D1", "F1")
ROUND_D = "review-records/rounds-2026-10-28/round-d/decisions.md"
NONE = "none"
DEFAULTS_FLOOR = "No floor is raised (GOV.11): every provision changed is a default that a recorded decision replaces"
WITHDRAWN_ORDER = ("The withdrawn identifiers are listed in the field withdrawn and not reused (GOV.37); no "
                   "document cites them after the earlier transactions of this round")

# ---------------------------------------------------------------------------------------------------- STND.FTN

FTN4 = [(
    "Each change SHOULD pass a static check that reports each reference to a procedure without an explicit "
    "interface, and that compares each interface body of a procedure that the work defines outside a module with "
    "the definition of that procedure (DSGN.3).",
    "Where the means of the work include a static check that reports each reference to a procedure without an "
    "explicit interface, or one that compares each interface body of a procedure that the work defines outside a "
    "module with the definition of that procedure, each change SHOULD pass each such check (DSGN.3).")]
FTN33 = [(
    "the repository configuration SHOULD hold an entry for that file in the legacy list, with those forms and "
    "provisions",
    "the repository configuration SHOULD hold, in the legacy list, an entry that names that file, or a directory or "
    "a pattern of names whose files share its forms and reasons, with those forms and provisions")]
FTN_DOC = [
    ("| Legacy list | The list, in the repository configuration, of the entries of STND.FTN.33: each source file of "
     "Fortran that uses",
     "| Legacy list | The list, in the repository configuration, of the entries of STND.FTN.33: each source file of "
     "Fortran, or each set of such files that a directory or a pattern of names gives, that uses"),
    ("which the second sentence of STND.FTN.4 asks; a reference that reaches no explicit interface is the report that "
     "the same check makes, and STND.BUILD.12 fails the change on it.",
     "which the second sentence of STND.FTN.4 asks; a reference that reaches no explicit interface is the report that "
     "the same check makes, and STND.BUILD.12 fails the change on it. Where the compilers and tools of the work offer "
     "neither check, the second sentence asks nothing, and the first still asks an explicit interface at each "
     "reference."),
    ("One reason serves a class of forms, so an entry for a file in fixed form that uses COMMON throughout states its "
     "reason once for each.",
     "One reason serves a class of forms, so an entry for a file in fixed form that uses COMMON throughout states its "
     "reason once for each. An entry names one file, or a directory or a pattern of names whose files share its "
     "forms and reasons, so that a legacy code of thousands of files in one form needs one entry; an entry widened "
     "to further files is an entry added, which STND.FTN.33 admits only on the occasions that it names."),
]


def edit_ftn(root: Path) -> None:
    replace_text(root, "STND/FTN/4.md", FTN4)
    replace_text(root, "STND/FTN/33.md", FTN33)
    replace_text(root, "STND/FTN/_doc.md", FTN_DOC)
    F.check_fields(root, ["STND.FTN.4", "STND.FTN.33"])


FTN = E.Step(
    "STND.FTN", edit_ftn, True,
    "the second sentence of STND.FTN.4 asks each change to pass a static check of explicit interfaces, or of "
    "interface bodies against their definitions, only where the means of the work include it; an entry of the "
    "legacy list of STND.FTN.33 names one file, or a directory or a pattern of names whose files share its forms "
    "and reasons, and the term Legacy list and the Notes follow",
    "it alters two recommendations, conditioning one on the means of the work and letting one entry serve a set "
    "of files",
    f"{DEFAULTS_FLOOR}; both changes lighten work at every class", "unchanged", NONE,
    f"{F1}; register entry R7.2 (CL19, a convenience, not a blocker; CL20, checked)")

# ---------------------------------------------------------------------------------------------------- STND.DEPS

DEPS14 = E.provision(
    "STND.DEPS", 14, "Declared range checks", "Revisions", "default", ["VV.8", "RSRC.12"],
    ["STND.CODE.19"],
    "Other than for high-assurance code whose edition and toolchain STND.CODE.19 fixes, the checks of each release "
    "of work that declares a range of revisions of its language or of a dependency SHOULD run with the oldest "
    "revisions that those ranges admit, together, and with the newest revisions that they admit and that are "
    "consistent with one another (VV.8, RSRC.12). Other than for such high-assurance code, a check that reports its "
    "failure without blocking a change SHOULD run the tests of such work, at the interval that the repository "
    "configuration sets, with the newest stable release of its language and the newest revisions of its "
    "dependencies that their declared ranges admit (VV.8).", "CSQ3")
DEPS13 = [
    ("Other than a check that the standard of its language asks to run at revisions other than those that the lock "
     "file records,",
     "Other than a check that STND.DEPS.14 or the standard of its language asks to run at revisions other than those "
     "that the lock file records,"),
    ("refers_to: []", 'refers_to: ["STND.DEPS.14"]'),
]
DEPS4 = [(
    "Each review SHOULD record why each dependency that it leaves at its revision stays there (REPRO.7, REPRO.9).",
    "Each review SHOULD record why each direct dependency that it leaves at its revision stays there, one reason "
    "serving each group of dependencies that share it (REPRO.7, REPRO.9).")]
DEPS_DOC = [
    ("and which revisions the builds of the checks and of the releases use.",
     "which revisions the builds of the checks and of the releases use, and on which revisions of a declared range "
     "the checks of a release run."),
    ("the last trigger is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit "
     "changes.",
     "the last trigger is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit "
     "changes. Each review records a reason for each direct dependency that it leaves at its revision, one reason "
     "serving a group of dependencies that share it, since a transitive dependency stays where the direct "
     "dependency that needs it holds it (STND.DEPS.4).\n\n"
     "A declared range of revisions that no check confirms drifts from the code: a dependent that resolves the "
     "oldest revision that the range admits meets a failure that the builds of the work never saw. STND.DEPS.14 "
     "runs the checks of each release on the oldest revisions that the declared ranges admit, together, and on "
     "the newest revisions that are consistent with one another, and runs a check at an interval, without blocking "
     "a change, on the newest revisions, so that a break that a new release of the language or of a dependency "
     "brings is seen before a release relies on it. The checks across the range run at release, the latest point "
     "at which their result is needed, since dependents rely on a declared range through a release (RSRC.12). Work "
     "that declares no range, as an application whose environment a lock file fixes, owes nothing under "
     "STND.DEPS.14. STND.PY, STND.JL, and STND.RUST keep only what their languages add: the declaration of the "
     "oldest releases of a Python package, the reference version and the newest prerelease of Julia, and the "
     "edition and the oldest supported toolchain that the metadata of a Rust crate states."),
    ("the checks that a language standard runs at other revisions, on the oldest declared releases of STND.PY.14 and "
     "STND.RUST.1 and on the newer revisions that STND.RUST.1 and STND.JL.3 ask, leave the lock file.",
     "the checks of STND.DEPS.14, on the oldest and the newest revisions that a declared range admits, and those "
     "that a language standard runs at other revisions, on the newest prerelease of Julia that STND.JL.3 asks, "
     "leave the lock file."),
]


def edit_deps(root: Path) -> None:
    E.add_provision(root, "STND/DEPS", DEPS14)
    replace_text(root, "STND/DEPS/13.md", DEPS13)
    replace_text(root, "STND/DEPS/4.md", DEPS4)
    replace_text(root, "STND/DEPS/_doc.md", DEPS_DOC)
    F.check_fields(root, ["STND.DEPS.4", "STND.DEPS.13", "STND.DEPS.14"])


DEPS = E.Step(
    "STND.DEPS", edit_deps, True,
    "new STND.DEPS.14 (default) runs the checks of each release of work that declares a range of revisions of its "
    "language or of a dependency on the oldest revisions that the ranges admit and on the newest consistent ones, "
    "and a check at an interval, without blocking a change, on the newest revisions, high-assurance code apart, in "
    "place of three cadences in STND.PY.14, STND.JL.3, and STND.RUST.1; STND.DEPS.13 excepts those checks from the "
    "locked revisions; STND.DEPS.4 records a reason for each direct dependency that a review leaves at its "
    "revision, one reason serving a group; the Purpose and the Notes follow",
    "it adds a default that holds one outcome for every language and alters two",
    f"{DEFAULTS_FLOOR}; for Python, the check at an interval on the newest revisions is new, and for Rust and Julia "
    "the checks on the oldest revisions move from each change to each release, the latest point at which their "
    "result is needed (RSRC.12)",
    "STND.DEPS.14 from CSQ3, the class of STND.PY.14, STND.JL.3, and STND.RUST.1; the others unchanged",
    "a project whose checks run across the range at each change meets STND.DEPS.14",
    f"{D1}; register entries R6.2 (CL7, checked, which {ROUND_D} decision 18 leaves to this round) and R7.2 (CL20, "
    "checked)")

# ---------------------------------------------------------------------------------------------------- STND.CODE

CODE5 = [(
    "The repository configuration SHOULD name, for each language of the work, a tool that produces the layout of "
    "its source (INTPR.1).",
    "Where the means of the work include a tool that produces the layout of the source of a language of the work, "
    "the repository configuration SHOULD name such a tool for that language (INTPR.1).")]
CODE_DOC = [
    ("A layout that a named tool produces and confirms costs the reviewer nothing (STND.CODE.5).",
     "A layout that a named tool produces and confirms costs the reviewer nothing (STND.CODE.5); for a language "
     "whose tools offer no such layout, STND.CODE.5 asks nothing."),
    ("The words differ from those of STND.CXX.18 as ruled for C++,",
     "The words differ from those that the custodian ruled for C++,"),
    (" STND.CXX.18 and STND.STDC.40 state the rule of STND.CODE.21 for C++ and for C.", ""),
    ("A check that runs the tests on a newest release without blocking a change, as STND.RUST.1 and STND.JL.3 ask,",
     "A check that runs the tests on a newest release without blocking a change, as STND.DEPS.14 asks,"),
]


def edit_code(root: Path) -> None:
    replace_text(root, "STND/CODE/5.md", CODE5)
    replace_text(root, "STND/CODE/_doc.md", CODE_DOC)
    F.check_fields(root, ["STND.CODE.5"])


CODE = E.Step(
    "STND.CODE", edit_code, True,
    "STND.CODE.5 has the repository configuration name a tool that produces the layout of the source of a language "
    "only where the means of the work include one; the Notes cite STND.DEPS.14 for the check at an interval on the "
    "newest releases and drop the citations of STND.CXX.18 and STND.STDC.40, which state STND.CODE.21 for C++ and C",
    "it conditions a recommendation on the means of the work",
    f"{DEFAULTS_FLOOR}; the change lightens work in a language whose tools offer no layout", "unchanged", NONE,
    f"{F1}; register entry R7.2 (CL19, a convenience, not a blocker); {ROUND_D} decisions 1b and 16")

# ---------------------------------------------------------------------------------------------------- STND.BUILD

BUILD_DOC = [
    ("under a setting that lets the compiler assume finite values, which STND.CXX.18 states for C++ and STND.STDC.40 "
     "for C.",
     "under a setting that lets the compiler assume finite values, in every language, C and C++ included."),
    ("which is why STND.CODE.21 forbids it for code that holds a required check of such a value, and STND.CXX.18 and "
     "STND.STDC.40 state the same for C++ and C code;",
     "which is why STND.CODE.21 forbids it, in every language, for code that holds a required check of such a "
     "value;"),
    ("and the oldest and newest declared releases (STND.PY.14) are two instances",
     "and the oldest and newest revisions that a declared range admits (STND.DEPS.14) are two instances"),
]


def edit_build(root: Path) -> None:
    replace_text(root, "STND/BUILD/_doc.md", BUILD_DOC)


BUILD = E.Step(
    "STND.BUILD", edit_build, False,
    "the Notes say that STND.CODE.21 forbids, in every language, a setting that lets the compiler assume finite "
    "values for code that holds a required check, in place of naming STND.CXX.18 and STND.STDC.40, which a later "
    "transaction of this round withdraws, and cite STND.DEPS.14 for the oldest and newest revisions of a declared "
    "range in place of STND.PY.14",
    "only informative text changes", "No floor is raised or lowered (GOV.11): only informative text changes",
    "unchanged", NONE, f"{F1}; {ROUND_D} decisions 1b, 16, and 20")

# ---------------------------------------------------------------------------------------------------- STND.SV

SV_DOC = [
    ("seeds of random stimulus (STND.SV.23); the classes of finding",
     "seeds of random stimulus (STND.SV.23); and the classes of finding"),
    ("and comparisons between simulators (STND.SV.24 to STND.SV.27); and the conventions of names (STND.SV.28).",
     "and comparisons between simulators (STND.SV.24 to STND.SV.27)."),
    ("so STND.SV.28 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do, "
     "keeps the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, and adds no table.",
     "so STND.CODE.28 leaves the convention of Verilog and SystemVerilog source to the repository configuration and "
     "keeps the names that the notation of NUMER.4 fixes, and this standard adds no table."),
]


def edit_sv(root: Path) -> None:
    replace_text(root, "STND/SV/_doc.md", SV_DOC)
    F.withdraw(root, "STND/SV", "STND.SV", [28])


WITHDRAW_BECAUSE = "it removes a default, whose outcome STND.CODE.28 holds for every language"
WITHDRAW_FLOOR = ("No floor is raised or lowered (GOV.11): STND.CODE.28 holds the same outcome, a convention of names "
                  "that the repository configuration names where the standard of a language gives none, with the "
                  "names that the notation of NUMER.4 fixes, at the same onset")

SV = E.Step(
    "STND.SV", edit_sv, True,
    "STND.SV.28 is withdrawn, STND.CODE.28 holding the convention of names for Verilog and SystemVerilog source as "
    "for every language, and the front matter lists it as withdrawn; the Purpose and the Notes cite STND.CODE.28",
    WITHDRAW_BECAUSE, WITHDRAW_FLOOR, "unchanged; STND.CODE.28 applies from CSQ3, as STND.SV.28 did",
    f"none. {WITHDRAWN_ORDER}", f"{D1}; {ROUND_D} decision 3a")

# ---------------------------------------------------------------------------------------------------- STND.STDC

STDC_DOC = [
    (" states for C the binding form of STND.CXX.18 on the option that assumes finite values (STND.STDC.40),", ""),
    ("signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), the "
     "checks of C code (STND.STDC.37 and STND.STDC.38), and names (STND.STDC.39).",
     "signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), and the "
     "checks of C code (STND.STDC.37 and STND.STDC.38)."),
    ("STND.STDC.2 and STND.STDC.40 instantiate PRIME.4 and are binding at every class.",
     "STND.STDC.2 instantiates PRIME.4 and is binding at every class."),
    ("STND.CODE.21 forbids it in every language for code that holds a check that the floor requires, and "
     "STND.STDC.40 states the same for C, in the words of STND.CXX.18.",
     "STND.CODE.21 forbids it in every language, C included, for code that holds a check that the floor requires."),
    ("so STND.STDC.39 leaves the convention to the repository configuration and keeps the names that the notation of "
     "NUMER.4 fixes, the rule that STND.CODE.28 states for every language, and adds no table;",
     "so STND.CODE.28 leaves the convention of C source to the repository configuration and keeps the names that the "
     "notation of NUMER.4 fixes, and this standard adds no table;"),
    ("STND.STDC.40 keeps for C the binding form of STND.CXX.18, which the same ratification applied to C through the "
     "table of STND.STDC.2, at the cost of one choice of option for a unit that holds a required check.",
     "The same ratification applied to C the binding rule on the option that assumes finite values, which "
     "STND.CODE.21 states for every language, at the cost of one choice of option for a unit that holds a "
     "required check."),
    ("the removal of a test by isnan or isfinite under it is unverified, and the ratification of 2026-10-24 kept the "
     "binding form for C, which STND.CODE.21 now states for every language. Both bind at every class.",
     "and the removal of a test by isnan or isfinite under it is unverified. STND.STDC.2 and STND.CODE.21 bind at "
     "every class."),
]


def edit_stdc(root: Path) -> None:
    replace_text(root, "STND/STDC/_doc.md", STDC_DOC)
    F.withdraw(root, "STND/STDC", "STND.STDC", [39, 40])


STDC = E.Step(
    "STND.STDC", edit_stdc, True,
    "STND.STDC.39 and STND.STDC.40 are withdrawn, STND.CODE.28 holding the convention of names and STND.CODE.21 the "
    "rule on the option that assumes finite values for C as for every language, and the front matter lists them "
    "as withdrawn; the Purpose, the class paragraph, and the Notes cite STND.CODE.21 and STND.CODE.28",
    "it removes a binding provision and a default, whose outcomes STND.CODE.21 and STND.CODE.28 hold for every "
    "language",
    "No floor is raised or lowered (GOV.11): STND.CODE.21 binds at every class, as STND.STDC.40 did, for code that "
    "holds a check that STND.CODE.6 or STND.CODE.16 governs, which are the checks of untrusted input and of CPS.5 "
    "and CPS.9 that STND.STDC.40 named, and STND.CODE.28 holds the convention of names at the onset of "
    "STND.STDC.39",
    "unchanged", f"none. {WITHDRAWN_ORDER}", f"{D1}; {ROUND_D} decisions 1b, 3a, and 16")

# ---------------------------------------------------------------------------------------------------- STND.LEAN

LEAN_DOC = [
    ("Lean programs (STND.LEAN.26 and STND.LEAN.27);", "Lean programs (STND.LEAN.26);"),
    ("STND.LEAN.27 leaves the convention to the repository configuration and keeps the names that the notation of "
     "NUMER.4 fixes, the rule that STND.CODE.28 states for every language.",
     "STND.CODE.28 leaves the convention of Lean source to the repository configuration and keeps the names that the "
     "notation of NUMER.4 fixes."),
]


def edit_lean(root: Path) -> None:
    replace_text(root, "STND/LEAN/_doc.md", LEAN_DOC)
    F.withdraw(root, "STND/LEAN", "STND.LEAN", [27])


LEAN = E.Step(
    "STND.LEAN", edit_lean, True,
    "STND.LEAN.27 is withdrawn, STND.CODE.28 holding the convention of names for Lean source as for every language, "
    "and the front matter lists it as withdrawn; the Purpose and the Notes cite STND.CODE.28",
    WITHDRAW_BECAUSE, WITHDRAW_FLOOR, "unchanged; STND.CODE.28 applies from CSQ3, as STND.LEAN.27 did",
    f"none. {WITHDRAWN_ORDER}", f"{D1}; {ROUND_D} decision 3a")

# ---------------------------------------------------------------------------------------------------- STND.CXX

CXX_DOC = [
    ("It covers failures, including the option that assumes finite values, the failed release of an owned resource, "
     "and the terminate handler (STND.CXX.18, STND.CXX.19,",
     "It covers failures, including the failed release of an owned resource and the terminate handler "
     "(STND.CXX.19,"),
    ("STND.CXX.18 instantiates PRIME.4, and STND.CXX.3 instantiates GOV.48 and binds agents alone; these two are "
     "binding at every class.",
     "STND.CXX.3 instantiates GOV.48, binds agents alone, and is binding at every class; STND.CODE.21 binds for C++ "
     "the rule on the option that assumes finite values."),
    ("which is why STND.CXX.18 and STND.CODE.21 forbid such an option for a unit holding a required check of that "
     "kind.",
     "which is why STND.CODE.21 forbids such an option for a unit holding a required check of that kind."),
    ("STND.CXX.18 states for a translation unit of C++ the rule that STND.CODE.21 binds in every language.",
     "STND.CODE.21 binds for a translation unit of C++ the rule on the option that assumes finite values."),
    ("The counterpart of STND.CXX.27 in Julia is a default of the Julia standard, added with this revision, that keeps",
     "The counterpart of STND.CXX.27 in Julia is STND.JL.36, which keeps"),
    (" STND.CXX.18 binds at every class, CSQ4 included, and costs one choice of compiler option for a unit that holds "
     "a required check.", ""),
    ("That STND.CXX.3 and STND.CXX.18 raise no floor (GOV.11) is the custodian's ruling of 2026-10-23 (PRIN.10).",
     "That STND.CXX.3 raises no floor (GOV.11), and that the rule on the option that assumes finite values, which "
     "STND.CODE.21 states, raises none, is the custodian's ruling of 2026-10-23 (PRIN.10)."),
]


def edit_cxx(root: Path) -> None:
    replace_text(root, "STND/CXX/_doc.md", CXX_DOC)
    F.withdraw(root, "STND/CXX", "STND.CXX", [18])


CXX = E.Step(
    "STND.CXX", edit_cxx, True,
    "STND.CXX.18 is withdrawn, STND.CODE.21 binding the rule on the option that assumes finite values for C++ as for "
    "every language, and the front matter lists it as withdrawn; the Purpose, the class paragraph, and the Notes "
    "cite STND.CODE.21, and the Notes name STND.JL.36 as the Julia counterpart of STND.CXX.27 in place of narrating "
    "its drafting",
    "it removes a binding provision whose outcome STND.CODE.21 holds for every language",
    "No floor is raised or lowered (GOV.11): STND.CODE.21 binds at every class, as STND.CXX.18 did, for code that "
    "holds a check that STND.CODE.6 or STND.CODE.16 governs, which are the checks of untrusted input and of CPS.5 "
    "and CPS.9 that STND.CXX.18 named",
    "unchanged", f"none. {WITHDRAWN_ORDER}",
    f"{D1}; register entry R7.1 (CL22); {ROUND_D} decisions 1b and 16")

# ---------------------------------------------------------------------------------------------------- STND.JL

JL3 = (
    "Other than where a qualified revision fixes it, the Julia revision of the production configuration and of the "
    "checks of each change SHOULD be the latest patch release of the reference version (VV.8, REPRO.9). The check of "
    "STND.DEPS.14 that reports its failure without blocking a change SHOULD also run the tests on the newest "
    "prerelease of Julia (VV.8).")
JL_DOC = [
    ("STND.JL.1 and the third sentence of STND.JL.3 yield to it by their own text, and its third sentence keeps that "
     "version as a qualified revision.",
     "STND.JL.1 and STND.DEPS.14 yield to it by their own text, and its third sentence keeps that version as a "
     "qualified revision."),
    ("and STND.JL.3 then checks the earliest version that its bounds admit as well (GOV.19).",
     "and STND.DEPS.14 then checks, at each release, the earliest version that its bounds admit as well (GOV.19)."),
    ("The scheduled check on the newest stable release and on the prerelease shows a coming change",
     "The scheduled check on the newest stable release (STND.DEPS.14) and on the prerelease (STND.JL.3) shows a "
     "coming change"),
    (" STND.CXX.27 stays unchanged, and STND.JL.36 is its Julia counterpart.", ""),
]


def edit_jl(root: Path) -> None:
    F.set_body(root, "STND/JL/3.md", JL3, refers_to=["STND.DEPS.14"])
    replace_text(root, "STND/JL/_doc.md", JL_DOC)
    F.check_fields(root, ["STND.JL.3"])


JL = E.Step(
    "STND.JL", edit_jl, True,
    "STND.JL.3 keeps the reference version of Julia for the checks of each change, and has the check of "
    "STND.DEPS.14 at an interval also run on the newest prerelease, its check of the earliest admitted version and "
    "of the newest stable release moving to STND.DEPS.14; the Notes follow, and drop a sentence that narrated the "
    "drafting of STND.JL.36",
    "it alters a default, the check of the earliest admitted version moving from each change to each release",
    f"{DEFAULTS_FLOOR}; the check of the earliest admitted version runs at each release, the latest point at which "
    "its result is needed (RSRC.12)",
    "unchanged; STND.DEPS.14 applies from CSQ3, as STND.JL.3 did", NONE,
    f"{D1}; register entries R6.2 (CL7, checked) and R7.1 (CL22); {ROUND_D} decision 18")

# ---------------------------------------------------------------------------------------------------- STND.RUST

RUST1 = (
    "The package metadata of each crate of the work SHOULD state its edition and the oldest release of the Rust "
    "toolchain that it supports (SIMPL.6, REPRO.9). The checks of each change SHOULD build and test each crate of "
    "the work with the release of the toolchain that builds the reported results and the releases of the work "
    "(VV.8).")
RUST28 = [(
    "Before a change that alters the lock file is relied upon, its review SHOULD examine each build script that the "
    "change adds or alters, those of each dependency that it adds included (SIMPL.4, REPRO.9).",
    "Before a change that adds a dependency with a build script is relied upon, its review SHOULD examine that build "
    "script (SIMPL.4, REPRO.9).")]
RUST_DOC = [
    ("so the claims of Rust code bind as before the round.", "so the claims of Rust code bind at every class."),
    ("so STND.RUST.1 tests at that release and at the release that builds results and releases, and runs a "
     "non-blocking check at the newest stable release and the newest revisions of the dependencies, as STND.PY.14 "
     "and STND.JL.3 do;",
     "so STND.RUST.1 has the package metadata state it and STND.DEPS.14 tests at it at each release, and at the "
     "newest stable release and the newest revisions of the dependencies at an interval, without blocking a change, "
     "while STND.RUST.1 tests each change at the release that builds results and releases;"),
    ("The third sentence of STND.RUST.1 leaves that code out,", "STND.DEPS.14 leaves that code out,"),
    ("STND.BUILD.21 reviews the build scripts of the work as code, and STND.RUST.28 adds the record and the review for "
     "those of dependencies, the evidence on exposure to compromise that STND.DEPS.1 weighs.",
     "STND.BUILD.21 reviews the build scripts of the work as code, and STND.RUST.28 adds the record of those of "
     "dependencies and the review of the build script of each dependency that a change adds, the evidence on "
     "exposure to compromise that STND.DEPS.1 weighs; a build script that a new revision of a dependency already in "
     "the work changes is code of the pinned revision that STND.DEPS.4 reviews."),
    ("and the check of STND.RUST.1 against newer revisions is the one build of the checks that leaves it.",
     "and the checks of STND.DEPS.14 against the oldest and the newer revisions are the builds of the checks that "
     "leave it."),
    ("STND.RUST.1, STND.RUST.7, STND.RUST.11, and STND.RUST.22 each hold three modals on one subject: the releases of "
     "one crate, what one argument rests on,",
     "STND.RUST.7, STND.RUST.11, and STND.RUST.22 each hold three modals on one subject: what one argument rests on,"),
]


def edit_rust(root: Path) -> None:
    F.set_body(root, "STND/RUST/1.md", RUST1, refers_to=[])
    replace_text(root, "STND/RUST/28.md", RUST28)
    replace_text(root, "STND/RUST/_doc.md", RUST_DOC)
    F.check_fields(root, ["STND.RUST.1", "STND.RUST.28"])


RUST = E.Step(
    "STND.RUST", edit_rust, True,
    "STND.RUST.1 keeps the edition and the oldest supported toolchain in the package metadata and the checks of "
    "each change at the release that builds results and releases, its checks at the oldest release and its check "
    "at an interval on the newest releases moving to STND.DEPS.14; the second sentence of STND.RUST.28 has a "
    "review examine the build script of each dependency that a change adds, the build script that a new revision "
    "of a dependency already in the work changes being code of the pinned revision that STND.DEPS.4 reviews; the "
    "Notes follow, and one sentence of the class paragraph no longer narrates an earlier round",
    "it alters two defaults",
    f"{DEFAULTS_FLOOR}; the check at the oldest release runs at each release, the latest point at which its result "
    "is needed (RSRC.12), and the review of a changed build script of an existing dependency is that of its pinned "
    "revision",
    "unchanged; STND.DEPS.14 applies from CSQ3, as STND.RUST.1 did", NONE,
    f"{D1}; register entry R6.2 (CL7, checked); finding CL9 (checked; it holds); {ROUND_D} decision 18")

# ---------------------------------------------------------------------------------------------------- STND.PY

PY_DOC = [
    ("the declared and checked releases of Python and of the work's dependencies (STND.PY.13 and STND.PY.14);",
     "the declared releases of Python and of the work's dependencies (STND.PY.13), which STND.DEPS.14 checks;"),
    ("and on the newest combination that its declared ranges admit (STND.PY.14).",
     "and on the newest combination that its declared ranges admit (STND.DEPS.14)."),
    ("and its checks run on the combinations of STND.PY.14;",
     "and its checks run on the combinations of STND.DEPS.14;"),
    ("and STND.PY.14 yields to it by its own text.", "and STND.DEPS.14 yields to it by its own text."),
    ("Running the checks of STND.PY.14 at release,", "Running the checks of STND.DEPS.14 at release,"),
]


def edit_py(root: Path) -> None:
    replace_text(root, "STND/PY/_doc.md", PY_DOC)
    F.withdraw(root, "STND/PY", "STND.PY", [14])


PY = E.Step(
    "STND.PY", edit_py, True,
    "STND.PY.14 is withdrawn, STND.DEPS.14 holding the checks of each release on the oldest declared releases and "
    "on the newest consistent ones for every language, and the front matter lists it as withdrawn; the Purpose and "
    "the Notes cite STND.DEPS.14",
    "it removes a default whose outcome STND.DEPS.14 holds for every language",
    f"{DEFAULTS_FLOOR}; STND.DEPS.14 asks the same checks of each release of a distributed package, which declares "
    "its ranges under STND.PY.13, and adds the check at an interval on the newest revisions",
    "unchanged; STND.DEPS.14 applies from CSQ3, as STND.PY.14 did", f"none. {WITHDRAWN_ORDER}",
    f"{D1}; register entry R6.2 (CL7, checked); {ROUND_D} decisions 16 and 18")

STEPS = [FTN, DEPS, CODE, BUILD, SV, STDC, LEAN, CXX, JL, RUST, PY]
