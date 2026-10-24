"""Rehearsable minor amendment: STND.CXX 1.1, citing STND.CONC (one transaction).

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_cxx_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:01:00+00:00"

# STND.CXX.15: the statement of concurrent safety is cited from STND.CONC.6, not restated.
CXX15 = [
    ('refers_to: ["STND.CODE.3"]', 'refers_to: ["STND.CODE.3", "STND.CONC.6"]'),
    ("In addition to what STND.CODE.3 asks, that comment SHOULD state the owner and the period of validity of each "
     "pointer, reference, view, and iterator that the declaration returns or keeps beyond the call, each C++ "
     "exception or error value by which it reports failure, and whether concurrent calls to it are safe (DSGN.1).",
     "In addition to what STND.CODE.3 and STND.CONC.6 ask, that comment SHOULD state the owner and the period of "
     "validity of each pointer, reference, view, and iterator that the declaration returns or keeps beyond the "
     "call, and each C++ exception or error value by which it reports failure (DSGN.1)."),
]

# STND.CXX.23: the first sentence stated the synchronization case of STND.CONC.3; the C++ rule for handlers stays.
CXX23 = [
    ('instantiates: ["DSGN.15", "HW.11"]', 'instantiates: ["DSGN.15"]'),
    ('refers_to: []', 'refers_to: ["STND.CONC.3"]'),
    ("Code that accesses an object from more than one thread, interrupt handler, or signal handler SHOULD order each "
     "conflicting access by an atomic operation, by a synchronization facility of the standard library or of the "
     "target, or by a facility of a library whose contract states its ordering (DSGN.15, HW.11). Where no "
     "synchronization facility of the target orders the accesses to an object that a signal or interrupt handler "
     "shares with the code it interrupts, that object SHOULD be a lock-free atomic object or, for a signal handler, "
     "an object of type volatile std::sig_atomic_t (DSGN.15).",
     "Where no synchronization facility of the target orders the accesses to an object that a signal or interrupt "
     "handler shares with the code it interrupts, that object SHOULD be a lock-free atomic object or, for a signal "
     "handler, an object of type volatile std::sig_atomic_t (DSGN.15, STND.CONC.3)."),
]

DOC = [
    ("C++ written as a hardware description is code under this standard, and HDES governs its realization.",
     "C++ written as a hardware description is code under this standard, and HDES governs its realization, whose "
     "design record HDES.3 asks."),
    ("STND.CXX.4 keeps the extensions that a foreign interface requires, those of a compiler for device code among "
     "them.",
     "STND.CXX.4 keeps the extensions that a foreign interface requires, those of a compiler for device code among "
     "them. The general rules for the settings of each compilation and for the warnings that fail the checks of a "
     "change, of which STND.CXX.4 and STND.CXX.25 are the C++ forms, belong to the standard for building software, "
     "which holds them for every language."),
    ("only the C++ rules at their boundaries.",
     "only the C++ rules at their boundaries. The rules of concurrency that hold for every language are in "
     "STND.CONC, which this standard cites and does not restate."),
    ("and the definition does not repeat it (STND.CXX.15).",
     "and the definition does not repeat it (STND.CXX.15). That contract includes the statement of STND.CONC.6, "
     "whether concurrent calls to the interface are safe and the condition under which they are, which "
     "STND.CXX.15 cites and does not restate (GOV.31)."),
    ("A handler shares lock-free",
     "STND.CONC.3 has each shared mutable object, handlers among the tasks that access it, follow one stated "
     "protection, and a protection by synchronization use a facility that the memory model of the language or "
     "library, or the ordering model of the hardware contract, defines as ordering accesses; in C++ those facilities are atomic operations and the synchronization "
     "facilities of the standard library, of the target, and of a library whose contract states its ordering, and "
     "`volatile` is none of them (CP.8). C++ adds one rule for handlers: a handler shares "
     "lock-free"),
    ("rules for them belong to standards for those models, which are not yet drafted.",
     "STND.CONC holds the rules of concurrency that hold for every model and language, and the standard of each "
     "model holds the rules of that model."),
    ("which STND.CXX.26 excludes by failing at the first detection.",
     "which STND.CXX.26 excludes by failing at the first detection. The second sentence of STND.CXX.26 is the C++ "
     "form of STND.CONC.25: in C++ the check that detects data races is a build of the code, asked wherever the "
     "work runs its code in more than one thread, and STND.CONC.25 has those tests fail at its first detection and "
     "run under a detection of lock-order inversions and deadlocks where the means of the work include one."),
    ("STND.CXX.26 instantiates the verification of DSGN.15, applied from CSQ2.",
     "STND.CXX.26 instantiates the verification of DSGN.15, applied from CSQ2. The provisions of STND.CONC that "
     "STND.CXX.15 and STND.CXX.23 cite, and of which the Notes give STND.CXX.26 as a form, take the same onsets, STND.CONC.3 and STND.CONC.6 from CSQ3 "
     "and STND.CONC.25 from CSQ2, so the citations move no rule to another class."),
]

READING = ("STND.CXX cites STND.CONC for the model-neutral part of its concurrency rules. STND.CXX.23 drops its "
           "first sentence, which stated the synchronization case of STND.CONC.3 without C++ content, and keeps its rule for "
           "objects shared with signal and interrupt handlers, citing STND.CONC.3 and instantiating DSGN.15 alone; "
           "STND.CXX.15 cites STND.CONC.6 in place of restating that the comment states whether concurrent calls are "
           "safe; the Notes name the C++ facilities that order accesses, give the second sentence of STND.CXX.26 as "
           "the C++ form of STND.CONC.25, describe the standards of other models as adopted, name STND.CXX.4 and "
           "STND.CXX.25 as the C++ forms of the general rules for build settings and warnings, and cite HDES.3 for "
           "the design record of a realization; References lists STND.CONC and HDES")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CXX to revision 1.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.CONC in ledger entry 112: {READING}. The change is minor and not editorial because STND.CXX.23 loses a "
    "sentence that stated an obligation and the citation of HW.11, and STND.CXX.15 loses an item of its list, so "
    "the text of two defaults changes, and with it what a project replaces when it replaces one of them (REPRO.7). "
    "The obligations of the work do not change: STND.CONC.3 asks each access to a shared mutable object, handlers "
    "included, to follow one stated protection, and a protection by synchronization to use a facility that the memory "
    "model or the hardware contract defines as ordering, of which the dropped sentence stated the synchronization "
    "case, and STND.CONC.6 asks the contract at the declaration to state "
    "whether concurrent calls are safe. The second sentence of STND.CXX.26 stays, because it asks a build that "
    "detects data races wherever C++ code runs in more than one thread, which STND.CONC.25 asks only where the means "
    "of the work include such a check. Class onsets unchanged: STND.CXX.15 and STND.CXX.23 from CSQ3, STND.CXX.26 "
    "from CSQ2. No floor is raised (GOV.11). Transition (GOV.42): none, because no obligation of the work changes. "
    "Review of STND.HARN.28 by the command pairs; record review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/CXX/15.md", CXX15)
    replace_text(root, "STND/CXX/23.md", CXX23)
    B.derive_fields(root, ["STND.CXX.15", "STND.CXX.23"])
    replace_text(root, "STND/CXX/_doc.md", DOC)
    raise_revision(root, "STND/CXX", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.CXX"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CXX"], scope=["STND/CXX"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CXX 1.1")
