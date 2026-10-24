"""Rehearsable minor amendment: STND.JL 1.1, citing STND.CONC (one transaction).

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_jl_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:03:00+00:00"

# STND.JL.27: the second sentence stated the lock and atomic case of STND.CONC.3; the Julia form of STND.CONC.16 stays.
JL27 = [
    ('instantiates: ["DSGN.15"]', 'instantiates: ["DSGN.14"]'),
    ('refers_to: []', 'refers_to: ["STND.CONC.16"]'),
    ("Code SHOULD NOT select per-task state by the value of `Threads.threadid()` (DSGN.15). Each mutable value that "
     "one task changes while another task reads or changes it SHOULD be guarded by a lock or accessed by atomic "
     "operations (DSGN.15).",
     "Code SHOULD NOT select per-task state by the value of `Threads.threadid()` (DSGN.14, STND.CONC.16)."),
]

DOC = [
    ("and the checks that confirm them at each change (STND.JL.32 to STND.JL.35).",
     "and the checks that confirm them at each change (STND.JL.32 to STND.JL.35). The rules of concurrency that hold "
     "for every language are in STND.CONC, which this standard cites and does not restate."),
    ("so the parts of parallel work take their streams from a facility of STND.VVUQ.62 (STND.JL.24).",
     "so the parts of parallel work take their streams from a facility of STND.VVUQ.62 (STND.JL.24). STND.JL.24 is "
     "the Julia form of STND.CONC.23, which keys each stream of a computation divided among concurrent tasks to a "
     "part defined independently of the number of tasks and of the task that computes it; STND.JL.24 reaches each "
     "division of work into parts, parts run as separate runs included, which STND.CONC.23 does not reach."),
    ("Concurrency. Tasks migrate between threads, so state chosen by `Threads.threadid()`, including a buffer or a "
     "generator, is shared by the tasks that the scheduler moves, and `threadid()` exceeds `nthreads()` while the "
     "interactive pool is in use (STND.JL.27). `push!` and insertion into a `Dict` from two tasks need a lock,",
     "Concurrency. STND.CONC holds the rules of concurrency that hold for every language, and this standard adds "
     "only their Julia forms (GOV.31). STND.JL.27 is the Julia form of the second sentence of STND.CONC.16: tasks "
     "migrate between threads, so state chosen by `Threads.threadid()`, including a buffer or a generator, is shared "
     "by the tasks that the scheduler moves, and `threadid()` exceeds `nthreads()` while the interactive pool is in "
     "use. STND.CONC.3 has each object that one task changes while another reads or changes it follow one stated "
     "protection, a lock or atomic operations among them: `push!` and insertion into a `Dict` from two tasks need a "
     "lock,"),
    ("STND.JL.27 asks for the protocol of DSGN.15 from CSQ3; the verification of its invariants, which STND.CLASS.10 "
     "starts at CSQ2, stays with DSGN.15.",
     "STND.JL.27, the Julia form of the second sentence of STND.CONC.16, instantiates DSGN.14 as that provision "
     "does, rests on no row, and applies from CSQ3; the protection of state that tasks share is STND.CONC.3, and the "
     "verification of its invariants, which STND.CLASS.10 starts at CSQ2, stays with DSGN.15. STND.CONC.3, "
     "STND.CONC.16, and STND.CONC.23 apply from CSQ3, as "
     "STND.JL.27 and STND.JL.24 do, so the citations move no rule to another class."),
    ("Distributed computing, GPU packages, ahead-of-time compilation with trimming, and Pkg apps are outside this "
     "standard; STND.CODE and the project instruments govern them.",
     "Distributed computing, GPU packages, ahead-of-time compilation with trimming, and Pkg apps are outside this "
     "standard. STND.OFFLD and HW.GPU govern offload to accelerators from Julia, from the placement of offloaded "
     "work (STND.OFFLD.2) to its completion (HW.GPU.3), and STND.MPI and STND.CONC govern distributed computing "
     "where they apply, the halt of one process of a run among it (STND.MPI.6, STND.CONC.2); STND.CODE and the "
     "project instruments govern the rest."),
]

READING = ("STND.JL.27 drops its second sentence, which stated the lock and atomic case of STND.CONC.3 without "
           "Julia content, cites STND.CONC.16, of whose second sentence its first is the Julia form, and instantiates "
           "DSGN.14, as STND.CONC.16 does, in place of DSGN.15; the class paragraph states its onset on that basis; the Notes cite "
           "STND.CONC.3 for the protection of state that tasks share, with the Julia examples, and STND.CONC.23 as "
           "the model-neutral rule of which STND.JL.24 is the Julia form, and cite STND.OFFLD and HW.GPU for offload "
           "and STND.MPI and STND.CONC for distributed computing in place of STND.CODE and the project instruments "
           "alone; References lists STND.CONC, STND.MPI, STND.OFFLD, and HW.GPU")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.JL to revision 1.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.CONC in ledger entry 112: {READING}. The change is minor and not editorial because STND.JL.27 loses a "
    "sentence that stated an obligation, so the text of a default changes, and with it what a project replaces "
    "when it replaces that default (REPRO.7). The obligations of the work do not change: STND.CONC.3 asks each "
    "access to a shared mutable object to follow one stated protection, among them a lock and atomic operations, "
    "of which the dropped sentence stated the lock and atomic case. The first sentence of STND.JL.27 stays, because it names the Julia "
    "facility, `Threads.threadid()`, by which code selects state by the identity of a thread. It instantiates "
    "DSGN.14, as STND.CONC.16 does, because the rule concerns which state a task owns and not a protocol of shared "
    "state; DSGN.14 rests on no row of STND.CLASS.10, so its onset stays CSQ3. STND.JL.24 stays, "
    "because it reaches work divided into parts that are not concurrent tasks of one run, which STND.CONC.23 does "
    "not. Class onsets unchanged: STND.JL.24 and STND.JL.27 from CSQ3. No floor is raised (GOV.11). Transition "
    "(GOV.42): none, because no obligation of the work changes. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/JL/27.md", JL27)
    B.derive_fields(root, ["STND.JL.27"])
    replace_text(root, "STND/JL/_doc.md", DOC)
    raise_revision(root, "STND/JL", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.JL"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.JL"], scope=["STND/JL"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.JL 1.1")
