"""Rehearsable minor amendment: STND.CONC 1.1, citing the standards that hold forms of its provisions, with a new
default on the order of output of concurrent tasks.

One transaction. It cites STND.OMP, STND.OFFLD, STND.WFLOW, STND.BUILD, STND.STDC, STND.RUST, STND.FTN, STND.SV,
and STND.LEAN, so it applies after all of them: apply_round_2026_10_24.py runs it after the new standards. It is
not part of apply_round_2026_10_24_amend.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T21:30:00+00:00"

DOC = [
    ("and the planned standards for directive-based threading and for accelerator offload hold theirs once adopted.",
     "STND.OMP holds those for directive-based threading, and STND.OFFLD those for accelerator "
     "offload."),
    ("Workflows of many runs, retried tasks, checkpoints, and access to shared files and storage belong to a planned "
     "standard of their own;",
     "Workflows of many runs, retried tasks, restart state, and access to shared files and storage belong to "
     "STND.WFLOW, whose STND.WFLOW.32 holds the guarantees of shared file systems on which work relies;"),
    ("the memory of accelerators belongs to HW.GPU and to the standard for offload.",
     "the memory of accelerators belongs to HW.GPU and to STND.OFFLD, whose STND.OFFLD.9 to STND.OFFLD.12 and "
     "STND.OFFLD.21 to STND.OFFLD.23 govern it."),
    ("and the directive-based threading standard has a form for its tasks.",
     "and STND.OMP.7 is its form for the tasks of OpenMP. The Notes of STND.RUST apply STND.CONC.15, STND.CONC.16, "
     "and STND.CONC.17 to blocking on an executor, to state local to a thread, and to executors as pools."),
    ("STND.CXX.23 is its form for C++.",
     "STND.CXX.23 is its form for objects that C++ code shares with signal and interrupt handlers. STND.STDC.35 is "
     "its form for adjacent bit-fields in C, STND.FTN.11 for the variables that Fortran shares without a declaration "
     "that shows it, STND.RUST.21 for an unsafe implementation of `Send` or `Sync`, which names the protection, and "
     "STND.OFFLD.5 for host storage that an asynchronous transfer reads. The Notes of STND.SV read STND.SV.5 to "
     "STND.SV.8 as the protection by scheduling for the processes of a simulation, which STND.SV reads as concurrent "
     "tasks, and STND.SV.5 and STND.SV.7 cite STND.CONC.3."),
    ("Whether concurrent calls to an interface are safe is part of its contract, as STND.CXX.15 already asks of C++ "
     "(STND.CONC.6).",
     "Whether concurrent calls to an interface are safe is part of its contract (STND.CONC.6), and in C++ that "
     "contract is the declaration comment of STND.CXX.15."),
    ("and those two provisions remain its forms for their models.",
     "and those two provisions remain its forms for their models. STND.OFFLD takes each submission of offloaded "
     "work, and STND.WFLOW each job that a workflow submits to a scheduler, as an asynchronous operation under it; "
     "the Notes of STND.RUST apply STND.CONC.1 and STND.CONC.2 to a spawned thread that panics or whose join handle "
     "is dropped, and those of STND.SV to each concurrent task of a testbench."),
    ("which is the reading of HW.8 that the Notes of HW give for a run of several processes and that STND.MPI.6 "
     "states for MPI.",
     "which is the reading of HW.8 that the Notes of HW give for a run of several processes and that STND.MPI.6 "
     "states for MPI. STND.OFFLD.8 is the way by which STND.CONC.2 reaches device code, whose threads have the "
     "submitting host code as their parent, and the Notes of STND.FTN read ERROR STOP, which ends every image, as "
     "the halt that it asks."),
    ("the hazard of the lifetime of captured data that c4 finds across models (STND.CONC.5).",
     "the hazard of the lifetime of captured data that c4 finds across models (STND.CONC.5). STND.OMP.8 is the form "
     "of STND.CONC.5 and STND.CONC.12 for the local variables that a routine shares with explicit tasks of OpenMP."),
    ("and a callback is such code (STND.CONC.8).",
     "and a callback is such code (STND.CONC.8). STND.RUST.23 makes STND.CONC.8 mechanical for asynchronous Rust, "
     "where a static check reports each guard of a lock held across a suspension point."),
    ("so the third sentence of STND.CONC.11 keeps such waits out (c4, hazard 6).",
     "so the second sentence of STND.CONC.11 keeps such waits out (c4, hazard 6). STND.OFFLD.18 is its form for the "
     "groups of one submission to an accelerator, and the Notes of STND.FTN apply it to the iterations of a DO "
     "CONCURRENT construct."),
    ("and code that swallows a cancellation keeps its caller from ending (STND.CONC.13).",
     "and code that swallows a cancellation keeps its caller from ending (STND.CONC.13). STND.RUST.22 adds what the "
     "cancellation of a future by its drop makes necessary in Rust, the statement of whether the future is "
     "cancellation safe among it."),
    ("changes the behavior of its caller (STND.CONC.17).",
     "changes the behavior of its caller (STND.CONC.17). STND.OMP.19 is its form for the internal control variables "
     "of OpenMP, and the Notes of STND.FTN apply it to a library that sets the floating-point modes of its caller."),
    ("STND.PY.17 and STND.JL.24 state the same for their languages, and STND.VVUQ.62 gives the construction of the "
     "streams.",
     "STND.PY.17 and STND.JL.24 state the same for their languages, STND.SV.23 is the form of STND.CONC.23 and "
     "STND.VVUQ.62 for the random stimulus of a testbench, and STND.VVUQ.62 gives the construction of the streams. "
     "Records that concurrent tasks write to one file or one log appear in the order in which the tasks reach their "
     "writes, which the schedule sets unless a protocol of the tasks fixes it; a declared variation of that order is "
     "no defect under REPRO.3, and a result that relies on an order that nothing fixes rests on undeclared "
     "variation (STND.CONC.30). REPRO.3 already asks that variation be declared, and HW.12 has each execution path "
     "declare whether the scheduling of its concurrent work varies; STND.CONC.30 adds the scope, the writes of "
     "concurrent tasks to one output, and the alternative of an order that a protocol of those tasks fixes. "
     "STND.FTN.26 is the Fortran case of STND.CONC.30 in which no protocol fixes the order: it asks that code not "
     "rely on the order of the records that the iterations of a DO CONCURRENT construct and the images of a Fortran "
     "program write to one file."),
    ("and the record of operations left pending at the end of a run (STND.CONC.29).",
     "the record of operations left pending at the end of a run (STND.CONC.29); and the order of the writes of "
     "concurrent tasks to one output or one record (STND.CONC.30)."),
    ("on which they and the provisions of HW that they instantiate rest.",
     "on which they and the provisions of HW that they instantiate rest. STND.CONC.30 states the order that a "
     "protocol fixes, or the variation that a record declares, and not how the invariants of that protocol are "
     "verified, so it applies from CSQ3, as STND.CONC.3 does."),
    ("STND.CXX.26 and STND.MPI.25 are the forms of STND.CONC.25 for C++ and for MPI.",
     "STND.CXX.26 and STND.MPI.25 are the forms of STND.CONC.25 for C++ and for MPI; it applies to C and to Fortran "
     "by its own scope, as the Notes of STND.STDC and STND.FTN say. STND.OMP.32 runs the tests of target regions "
     "under a check of mapping errors, which escape detectors of data races, and STND.OFFLD.30 runs the tests of "
     "device code under the checks of device code that the means of the work include. STND.RUST.33 states the "
     "limits of a check of unsafe code as STND.CONC.27 does, one record meets STND.STDC.38 and STND.CONC.27 for data "
     "races in C, and the second sentence of STND.BUILD.13 makes STND.CONC.27 specific for the parts of the work "
     "linked without a check. STND.LEAN.19, with the row Code that runs of STND.LEAN.4, is the statement of "
     "correspondence that STND.CONC.28 asks of a Lean model."),
]

NEW = P(30, "Output order of concurrent tasks", "Results", """
Where concurrent tasks write to one output or one record, the order in which their writes appear there SHOULD be stated, as an order that a protocol of those tasks fixes or as a variation that the record of that output declares (DSGN.15, REPRO.3).
""", ["DSGN.15", "REPRO.3"])

NEW_READING = ("new STND.CONC.30, a default from CSQ3 (DSGN.15, REPRO.3), has the order in which the writes of concurrent "
               "tasks to one output or one record appear stated, as an order that a protocol of the tasks fixes or as a "
               "variation that the record of the output declares; the Purpose lists it, the Notes give its reason "
               "and what it adds to REPRO.3 and HW.12, and name STND.FTN.26 as its Fortran case in which no protocol fixes "
               "the order, and the class paragraph states its onset")

READING = ("the Purpose and the Notes cite STND.OMP, adopted in ledger entry 114, STND.OFFLD, adopted in ledger "
           "entry 116, and STND.WFLOW in place of the planned standards for directive-based threading, for "
           "accelerator offload, and for workflows, with STND.WFLOW.32 for the guarantees of shared file systems "
           "and STND.OMP.7 as the OpenMP form of STND.CONC.16, and say restart state where the Purpose said "
           "checkpoints, a word that the corpus defines as a copy of prior state; they describe STND.CXX.23 and STND.CXX.15 as "
           "they read after STND.CXX 1.1; the Notes name the provisions of STND.OFFLD, STND.OMP, STND.WFLOW, "
           "STND.RUST, STND.STDC, STND.FTN, STND.SV, STND.LEAN, and STND.BUILD that are forms or applications of "
           "provisions of STND.CONC, among them STND.SV.5 to STND.SV.8, which the Notes of STND.SV read as the "
           "protection of STND.CONC.3 for simulation processes, and STND.LEAN.19 for STND.CONC.28, and correct a "
           "reference to the third sentence of STND.CONC.11, which has two; References lists each of those standards")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {NEW_READING}; {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CONC to revision 1.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.OMP in ledger entry 114, of STND.OFFLD in ledger entry 116, and of STND.WFLOW, STND.BUILD, STND.STDC, "
    f"STND.RUST, STND.FTN, STND.SV, and STND.LEAN in this round: {NEW_READING}; {READING}. The change is minor "
    "because it adds a default provision, and so an obligation of the work above the floor; the citations alter "
    "only the informative Purpose, Notes, and References. STND.CONC.30 rests on DSGN.15, whose statement of a "
    "protocol applies from CSQ3 while the verification of its invariants waits for the CSQ2 row, and on REPRO.3, "
    "which rests on no row, so it applies from CSQ3; it asks only the statement of an order or the declaration of "
    "a variation that DSGN.15 and REPRO.3 already ask, so no floor is raised (GOV.11), and STND.FTN.26 holds its "
    "Fortran cases. Transition (GOV.42): none, because existing work meets the new default when a change next "
    "touches a component whose concurrent tasks write to one output or record. Review of STND.HARN.28 by the "
    "command pairs; record review-records/round-2026-10-24/amendments/ and "
    "review-records/round-2026-10-24/fixpass.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/CONC/30.md").write_text(B.provision_text("STND.CONC", NEW, "adopted", DATE), encoding="utf-8")
    res = B.derive_fields(root, ["STND.CONC.30"])
    if res["STND.CONC.30"].forced or res["STND.CONC.30"].unresolved:
        raise ValueError(f"STND.CONC.30: {res['STND.CONC.30']}")
    replace_text(root, "STND/CONC/_doc.md", DOC)
    raise_revision(root, "STND/CONC", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.CONC"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CONC"], scope=["STND/CONC"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CONC 1.1")
