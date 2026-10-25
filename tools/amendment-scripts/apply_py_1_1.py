"""Rehearsable minor amendment: STND.PY 1.1, on STND.CODE 1.2 and the sibling list of decision 10 (one transaction).

It imports Untrusted input from STND.CODE and deletes its own definition; cites STND.CODE.14 from STND.PY.22 and
STND.CODE.6 from STND.PY.25; and adds STND.PY.32 (binding, the hook for an exception that no handler catches),
STND.PY.33 (default, committed lock files), and STND.PY.34 to STND.PY.36 (defaults, foreign interfaces). It applies
after STND.CODE 1.2, which it cites: apply_close_p2.py runs it after apply_close_p1.py. Run from harness/, so that
govharness imports:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.2> ../tools/amendment-scripts/apply_py_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:20:00+00:00"

# ------------------------------------------------------------------ changed provisions: citations and the clause of STND.CODE.19

PY22 = [
    ('refers_to: ["PRIME.13"]', 'refers_to: ["PRIME.13", "STND.CODE.14"]'),
    ("degrade visibly with a diagnosis, or return the condition in its result (PRIME.4).",
     "degrade visibly with a diagnosis, or return the condition in its result (PRIME.4, STND.CODE.14)."),
]
PY14 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.19"]'),
    ("The checks of each release of a distributed package SHOULD run on the oldest declared release of Python",
     "Other than for a release of Python that STND.CODE.19 fixes, the checks of each release of a distributed "
     "package SHOULD run on the oldest declared release of Python"),
]
PY25 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.6"]'),
    ("Code SHALL NOT check untrusted input with an assert statement (PRIME.4, DSGN.2).",
     "Code SHALL NOT check untrusted input with an assert statement (PRIME.4, DSGN.2, STND.CODE.6)."),
]

# ------------------------------------------------------------------ new provisions

NEW = [
    P(32, "Hooks for uncaught exceptions", "Reporting", """
Where the work replaces a hook that the interpreter calls for an exception that no handler catches, or for one that it is unable to raise, that hook SHALL deliver to the operator, or to the record of the run, a diagnosis of each such exception that answers a condition that PRIME.4 lists (PRIME.4, STND.CODE.14).
""", ["PRIME.4"], refs=["STND.CODE.14"], mode="binding"),
    P(33, "Committed Python lock files", "Versions", """
Where the work reports results, the lock file of each environment that produces them SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9). A distributed package whose own environment produces no reported result MAY keep its lock file out of version control (REPRO.9).
""", ["REPRO.1", "REPRO.9"]),
    P(34, "Python foreign function types", "Foreign interfaces", """
Where a foreign interface does not check the calls of the work against the declaration of a foreign function in its own language, the Python source SHOULD declare the type of each argument and of the result of that function as that declaration gives them (DSGN.4). Each structure whose layout the Python source declares for a foreign interface SHOULD have its size and the offset of each of its fields compared with the foreign declaration by a test (DSGN.4). Each array that the work passes to foreign code by a pointer to its elements SHOULD have, at the call, the element type, the order of dimensions, and the contiguity that the foreign declaration states (DSGN.4).
""", ["DSGN.4"]),
    P(35, "Python exceptions in foreign callbacks", "Foreign interfaces", """
Where foreign code invokes a Python callable of the work through a foreign interface that does not pass a Python exception on to the code of the work, that callable SHOULD catch each exception raised within it (DSGN.5). Where that interface carries errors, an exception so caught SHOULD be converted to an error that the interface carries (DSGN.5). Where that interface carries no error, an exception so caught SHOULD be stored in an object that code of the work checks after the foreign call returns, and answered there as STND.PY.22 requires (DSGN.5).
""", ["DSGN.5"], refs=["STND.PY.22"]),
    P(36, "Python objects held by foreign code", "Foreign interfaces", """
Each Python object that foreign code is able to use after the call that passed it to that code returns, a buffer or a callable among them, SHOULD stay referenced by an object of the work for as long as foreign code is able to use it (DSGN.14). Each resource that foreign code creates for the work SHOULD be released by the function that the contract of the interface names, through an object of the work that owns it (DSGN.14).
""", ["DSGN.14"]),
]

# ------------------------------------------------------------------ the document

PURPOSE = [
    ("the declared and checked releases of Python and of the work's dependencies (STND.PY.13 and STND.PY.14);",
     "the declared and checked releases of Python and of the work's dependencies, and the lock files of the "
     "environments that produce reported results (STND.PY.13, STND.PY.14, and STND.PY.33);"),
    ("reporting from library code (STND.PY.21 and STND.PY.22);",
     "reporting from library code, and the hooks that report an exception that no handler catches (STND.PY.21, "
     "STND.PY.22, and STND.PY.32);"),
    ("and the handling of failures (STND.PY.25 to STND.PY.31). STND.PY.22, STND.PY.25, STND.PY.27, and STND.PY.30 "
     "instantiate PRIME.4,",
     "the handling of failures (STND.PY.25 to STND.PY.31); and foreign interfaces (STND.PY.34, STND.PY.35, and "
     "STND.PY.36). STND.PY.22, STND.PY.25, STND.PY.27, STND.PY.30, and STND.PY.32 instantiate PRIME.4,"),
    ("These five are binding and apply at every class. STND.PY.22 states the one set of responses to a condition "
     "that PRIME.4 lists, and the other provisions refer to it.",
     "These six are binding and apply at every class. STND.PY.22 states the one set of responses to a condition "
     "that PRIME.4 lists, in the Python form of STND.CODE.14, and the other provisions refer to it. The provisions "
     "of STND.CODE hold for Python as for every language, and the Notes give their Python forms."),
]

TERMS = [
    ("Repository configuration and Static check have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that "
     "STND.CODE gives them;"),
    ("each of them whose own name and enclosing names carry no leading underscore. |",
     "each of them whose own name and enclosing names carry no leading underscore. Each function and method of the "
     "public interface belongs to the public interface that the term Untrusted input of STND.CODE takes in. |"),
    ("| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each "
     "function of the public interface, other than data from a source that the threat model of the project records "
     "as trusted. |",
     "| Lock file | A file that records, for an environment of the work, the exact revision of each package that its "
     "installer resolves from the declared dependencies and, where the source of a package gives one, its integrity "
     "digest. |\n"
     "| Foreign interface | An interface through which Python code of the work calls, or is called by, code written "
     "in another language, a function of a compiled extension module, a function that the work loads from a shared "
     "library while it runs, and a Python callable that the work passes to such code among them. |"),
]

NOTES = [
    # Versions: the lock file (sibling list) and the edition of high-assurance code (STND.CODE.19)
    ("the lock file of the package installer is the exact record of those revisions (STND.DEPS.10).",
     "the lock file of the package installer is the exact record of those revisions (STND.DEPS.10). STND.PY.33 "
     "keeps that lock file under version control wherever the work reports results, as STND.JL.4 does for a Julia "
     "manifest and STND.RUST.30 for a Rust lock file, so that the revisions of a run are those of its source. A "
     "distributed package whose own environment produces no reported result leaves its dependents to resolve their "
     "own environments, and its checks run on the combinations of STND.PY.14; that such a package commits no lock "
     "file is common practice (unverified). PEP 751, a standard of status Final, specifies a common format for lock "
     "files, named pylock.toml (a2, S9 and S10); which installers read or write it is unverified, and a format of a "
     "project tool's own is a lock file in the sense of the term where it records each exact revision. STND.CODE.19 "
     "fixes, for high-assurance code, a release of Python that its high-assurance coding standard covers and for "
     "which each tool that runs that code holds the validation that the work requires; that release is a qualified "
     "revision, which STND.DEPS.3 leaves fixed, and STND.PY.14 yields to it by its own text."),
    # Reporting: the hook for an uncaught exception (sibling list)
    ("A warning of a category that the default filters hide, DeprecationWarning outside the main module, "
     "PendingDeprecationWarning, ImportWarning, and ResourceWarning among them, is silent and does not count.",
     "A warning of a category that the default filters hide, DeprecationWarning outside the main module, "
     "PendingDeprecationWarning, ImportWarning, and ResourceWarning among them, is silent and does not count. An "
     "exception other than SystemExit that is raised and not caught reaches the hook that the sys module holds for "
     "it, just before the program exits, and one that the run method of a thread raises reaches the hook that the "
     "threading module holds; the default hooks print the traceback and the exception to the standard error stream "
     "(a2, S1 and S2). STND.PY.32 is the Python counterpart of the second "
     "sentence of STND.RUST.13: it asks a hook that the work installs in their place, to write the exception to a "
     "log or to a report among them, to deliver the diagnosis of each listed condition that reaches it, and work "
     "that keeps the default hooks meets it unchanged. The hook of the sys module that the interpreter calls when an "
     "exception has occurred and Python has no way to handle it, in a finalizer among them, is such a hook (a2, "
     "S1)."),
    # Assertions: STND.CODE.6, .14, .15, .16, the reach of the term, and the index item of the sibling list
    ("Assertions. STND.PY.25, STND.PY.27, and STND.PY.30 are the Python forms of STND.CODE.6 and STND.CODE.7, each "
     "limited to the conditions that PRIME.4 lists.",
     "Assertions. STND.PY.22 is the Python form of STND.CODE.14, whose pass of a condition to the caller a raised "
     "exception makes in Python, and STND.PY.25, STND.PY.27, and STND.PY.30 are the "
     "Python forms of STND.CODE.6 and STND.CODE.7, each limited to the conditions that PRIME.4 lists. STND.CODE.15 "
     "asks nothing of Python until a form of declaration under which an ignored result is diagnosed is among the "
     "means of the work, and STND.CODE.7 still forbids discarding a listed failure."),
    ("is the custodian's ruling of 2026-10-23 (PRIN.10). A run-time check of an invariant or postcondition that the "
     "work relies on is written as a raise statement for the same reason (STND.PY.26).",
     "is the custodian's ruling of 2026-10-23 (PRIN.10). STND.CODE defines the term once, and the term Public "
     "interface places the functions and methods of that interface in the public interface that the term takes in, "
     "so the reach of the ruling stays; the functions that the documentation or the repository configuration names "
     "for use outside the work belong to the interface for outside use of that term as well, a widening that the "
     "Notes of STND.CODE put to the custodian. The optimizing mode, set by an option of the command line or by an "
     "environment variable, removes assert statements and the code that depends on the value of __debug__ (a2, "
     "S3 and S5). A run-time check of an "
     "invariant or postcondition that the work relies on is written as a raise statement for the same reason "
     "(STND.PY.26), and STND.CODE.16 binds the same for each check that CPS.5 or CPS.9 requires where those apply. "
     "STND.JL.13 binds a check of each index that derives from untrusted input, because an annotation or an "
     "execution setting of Julia removes the bounds checks of its indexing. A built-in sequence raises IndexError "
     "for an index outside its range (a2, S6 and S7), a response that STND.PY.22 admits, and the optimizing mode "
     "leaves that check in place, since it removes only assert statements and code that depends on __debug__; "
     "whether each array library checks its indices in the same way is unverified. This standard therefore has no "
     "counterpart of that sentence. A negative index from minus the length to minus one selects from the end of a "
     "sequence and raises nothing, and a slice raises nothing whatever its bounds (a2, S6); where "
     "the contract of a function excludes it, only a check of the function under DSGN.2 rejects it. Code that a "
     "compiler translates from Python source is able to index without bounds checks, by default or by an option "
     "(unverified for each compiler); STND.PY.31 asks the reason for each such use, and STND.CODE.6 keeps an "
     "execution setting from removing a check of untrusted input there."),
    # Relaxed checks: the third sentence of STND.CODE.16
    ("remove a check or relax the arithmetic, so each carries its reason (STND.PY.31).",
     "remove a check or relax the arithmetic, so each carries its reason (STND.PY.31). Where code compiled under "
     "such an option holds a check of a floating-point value that STND.CODE.6 governs, STND.CODE.21 recommends "
     "against an option that lets the compiler assume finite values, beside the reason that STND.PY.31 asks."),
    # Foreign interfaces (sibling list), before the floor paragraph
    ("Floor. STND.PY.22 asks for the responses that PRIME.4 already requires,",
     "Foreign interfaces. STND.PY.34, STND.PY.35, and STND.PY.36 give the Python forms of what STND.CXX.20 and "
     "STND.CXX.22, STND.RUST.24 to STND.RUST.27, and STND.FTN.27 and STND.FTN.28 state for their languages: types "
     "that match the foreign declaration, exceptions kept from crossing into foreign code, and memory with one owner "
     "and a stated lifetime (DSGN.4, DSGN.5, DSGN.14). A compiled extension module is built against the declarations "
     "of the foreign code, so its compiler checks the types of each call. A library that loads a shared library "
     "while the program runs reads no declaration, and converts each argument and the result by the types that the "
     "Python source declares, or by defaults where it declares none. The ctypes module of the standard library "
     "is unable to determine the signature of a foreign function, checks no number of arguments where none are "
     "declared, and assumes that a function returns a C int unless its result type is declared; incorrect arguments "
     "are able to corrupt memory or crash the interpreter (a2, S8). A pointer read as an int is truncated on a "
     "platform where a pointer is wider (unverified), and these hazards are why STND.PY.34 asks for each type. A slice of an array is a view whose elements are not always adjacent in memory, and foreign code "
     "that reads a pointer to its first element as a contiguous block reads other elements (unverified for each "
     "array library); a conversion to a contiguous array of the declared element type before the call meets "
     "STND.PY.34. Where a foreign interface does not pass a Python exception on to the code of the work, the foreign "
     "caller of a Python callback does not see the failure; what each interface does with such an exception is "
     "unverified, so STND.PY.35 states the outcome: the callback "
     "catches the exception, and the work converts it to the error of the interface or answers it after the "
     "foreign call returns (STND.PY.22). An interface that passes the exception on, the C interface of an "
     "extension module among them, is outside STND.PY.35. The ctypes module keeps no reference to a callback "
     "object, which the garbage collector is then able to free while C code still holds it, crashing the program "
     "when the callback is made (a2, S8); whether a buffer passed to foreign code is kept alive is unverified for "
     "each interface. STND.PY.36 asks the work to keep the reference. A with "
     "statement makes the release of a resource that foreign code allocates visible at the interface, and a finalizer "
     "runs at a time that the language does not fix (unverified). The rule that an exception or a panic is caught "
     "inside a callback and answered after the foreign call returns is now stated alike for C++, Rust, Python, and "
     "Julia (STND.CXX.22, STND.RUST.25, STND.PY.35, STND.JL.39).\n\n"
     "Floor. STND.PY.22 asks for the responses that PRIME.4 already requires,"),
    ("They bind at every class, CSQ4 included, as PRIME.4 does.",
     "They bind at every class, CSQ4 included, as PRIME.4 does. STND.PY.32 reaches only a listed condition whose "
     "exception no handler caught, which already ends a thread or the program, and asks only for the actionable "
     "diagnosis that PRIME.4 names, at the cost of the wording of a hook that the work installs; without it a "
     "replaced hook is able to end the program on a listed failure without a diagnosis. It asks for no work that "
     "PRIME.4 does not, so it raises no floor (GOV.11); no ruling of the custodian covers it, and the argument is "
     "the one that the ratification of 2026-10-24 accepted for the second sentence of STND.RUST.13. It binds at "
     "every class, CSQ4 included."),
    # Class onset
    ("STND.PY.26 instantiates the run-time checking of VV.10 and DSGN.2, which STND.CLASS.10 applies from CSQ1, and "
     "applies from CSQ1.",
     "STND.PY.26 instantiates the run-time checking of VV.10 and DSGN.2, which STND.CLASS.10 applies from CSQ1, and "
     "applies from CSQ1. STND.PY.34 and STND.PY.35 instantiate the schemas of DSGN.4 and the external contracts of "
     "DSGN.5, which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.PY.33 and STND.PY.36 rest on no row "
     "and apply from CSQ3."),
]

READING = (
    "Terms import Untrusted input, and Execution setting, from STND.CODE and drop this standard's own definition of "
    "Untrusted input, and the term Public interface places its functions and methods in the public interface that "
    "the term Untrusted input of STND.CODE takes in; Terms define Lock file and Foreign interface; STND.PY.22 cites "
    "STND.CODE.14, and STND.PY.25 STND.CODE.6, for the rule of which each is the Python form, and neither changes "
    "otherwise; STND.PY.14 yields to a release of Python that STND.CODE.19 fixes; new STND.PY.32 (binding, PRIME.4) has a hook that the work "
    "installs for an exception that no handler catches, or that the interpreter is unable to raise, deliver the diagnosis of each listed condition, the Python "
    "counterpart of the second sentence of STND.RUST.13; new STND.PY.33 (default, REPRO.1 and REPRO.9) keeps the "
    "lock file of each environment that produces reported results under version control, as STND.JL.4 and "
    "STND.RUST.30 do; new STND.PY.34, STND.PY.35, and STND.PY.36 (defaults, DSGN.4, DSGN.5, and DSGN.14) give the "
    "types, the exceptions of callbacks, and the lifetime and ownership of memory at foreign interfaces; the "
    "Purpose lists them; the Notes cite the provisions of STND.CODE of which this standard gives Python forms, "
    "give the reason why this standard has no counterpart of the third sentence of STND.JL.13, and state the facts, "
    "the floor argument of STND.PY.32, and the onset of each new provision")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.PY to revision 1.1, ratified by the custodian on {DATE}, on STND.CODE 1.2 and the "
    f"list of differences among sibling language standards of the ratification of 2026-10-24: {READING}. The change "
    "is minor because it adds one binding provision and four defaults, and a clause to the default STND.PY.14. The "
    "import of Untrusted input keeps the reach of the definition it replaces, the arguments of each function of the "
    "public interface that this standard defines, and adds each function that the documentation or the repository "
    "configuration names for use outside the work, a widening that the Notes of STND.CODE put to the custodian. "
    "STND.PY.14 yields to STND.CODE.19, as STND.CXX.2 does, so that the newest releases it checks do not displace "
    "the release that a high-assurance coding standard and a validated toolchain fix. The citations in STND.PY.22 and STND.PY.25 change their references and not their outcome, and keep the "
    "language forms of the ruling of 2026-10-23. Sibling list: the third sentence of STND.JL.13 has no Python "
    "counterpart, because the interpreter checks each index in every mode, and the Notes say so; logging as the only "
    "visible degradation stays as ruled, by decision 7 of that ratification; STND.PY.32 is the counterpart of the "
    "second sentence of STND.RUST.13; STND.PY.33 is the counterpart of STND.JL.4 and STND.RUST.30; STND.PY.34 to "
    "STND.PY.36 are the counterparts of STND.CXX.20, STND.CXX.22, STND.RUST.24 to STND.RUST.27, STND.FTN.27, and "
    "STND.FTN.28. Class onsets: STND.PY.32 binds at every class; STND.PY.34 and STND.PY.35 from CSQ2; STND.PY.33 and "
    "STND.PY.36 from CSQ3; no other onset changes. Floor (GOV.11): STND.PY.32 reaches only a listed condition whose "
    "exception no handler caught and asks only for the actionable diagnosis that PRIME.4 names, at the cost of the "
    "wording of a hook that the work installs; no ruling covers it for Python, and the custodian decides it (R22). "
    "The defaults raise no floor. Transition (GOV.42): existing work meets the new defaults, and STND.PY.32, when a "
    "change next touches the component concerned. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-25-close/p2/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/PY/22.md", PY22)
    replace_text(root, "STND/PY/14.md", PY14)
    replace_text(root, "STND/PY/25.md", PY25)
    for p in NEW:
        (root / f"STND/PY/{p['n']}.md").write_text(B.provision_text("STND.PY", p, "adopted", DATE), encoding="utf-8")
    replace_text(root, "STND/PY/_doc.md", PURPOSE + TERMS + NOTES)
    ids = ["STND.PY.14", "STND.PY.22", "STND.PY.25"] + [f"STND.PY.{p['n']}" for p in NEW]
    res = B.derive_fields(root, ids)
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    for p in NEW:
        forced = res[f"STND.PY.{p['n']}"].forced
        if forced != (p["mode"] == "binding"):
            raise ValueError(f"STND.PY.{p['n']}: mode {p['mode']} but forced {forced}")
    raise_revision(root, "STND/PY", "1.0.1", "1.1", ROW)
    B.write_references(root, ["STND.PY"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.PY"], scope=["STND/PY"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.PY 1.1")
