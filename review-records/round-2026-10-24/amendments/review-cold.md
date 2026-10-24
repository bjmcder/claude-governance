# Cold review of the six amendments (round of 2026-10-24)

## Verified by script
- `govharness verify` passes all eight checks on `.scratch/amendments/work` (ledger 121) and `.scratch/amendments/full` (ledger 124, with STND.WFLOW at 123).
- `findings.py` on both copies, filtered to the six documents plus STND.WFLOW: 37 findings, all g.18/g.11 review notes, and the live corpus gives the same 37. None names a provision this round changes (STND.CXX.15, CXX.23, JL.27, NUMER.2).
- Each `<ID>-draft.md` is identical to `compose(...)` over the rehearsed copy. Each `<ID>.diff` equals `diff -u` of `rendered/<ID>.md` against the draft.
- NUMER.2 in the rehearsal carries NUMER.24 in `refers_to` and the new row. Its columns are Matter | Owning profile | Provisions, as in HW.2, and the owned row sits among the owned rows. The count of owned matters was six and is now seven (precision, convergence, uncertainty, approximation, tolerance, derivatives, streams).
- No history row or RATIONALE cites an entry number not yet fixed. Cited entries 112, 114, 116 exist in the ledger, and entry 112's rationale does assign the streams matter to NUMER.
- The onsets that the new Notes state agree with the CONC, OFFLD, and OMP onset paragraphs: CONC.3, .6, .16, .23 are CSQ3 and CONC.25 is CSQ2. Each OMP form takes the onset of the OFFLD provision it cites.
- Not checked: the STND.DOCS.9 pattern table (by eye only), and the pair lists (outside this task).

## Class under GOV.41
All six are correct. OMP, PY, CONC change only Purpose, Notes, References (editorial). CXX (CXX.15 and CXX.23 lose text), JL (JL.27 loses a sentence), and NUMER (a normative table gains a row; same class as 1.1 and 1.2) are minor. No onset changes and no floor is raised.

## STND.OMP 1.0.1 (editorial)
No Defect and no Should-fix.
- Optional: the OFFLD-form sentence copies OFFLD's Notes word for word, including "its second sentence of STND.OFFLD.1 and STND.OFFLD.3". It lost OFFLD's glosses "on static data on a device" and "on the requires directive", so "the first ... the second" in the sentence on OMP.27 and OMP.28 is hard to read. Restore the glosses.
- Checked: all ten mappings (OMP.3, .23 to .32) match OFFLD's own Notes. OMP.30 stays a provision for a reason that holds, since OFFLD.14 says "device code" and OMP.30 also covers host-run target regions. Every kept provision carries OpenMP names.

Verdict: accept.

## STND.CXX 1.1 (minor)
- Defect (factual): the new Note says STND.CONC.3 has the object follow a stated protection "by a facility that the memory model ... defines as ordering accesses". CONC.3 asks that only where the protection orders by synchronization, and the CONC Notes say confinement and immutability need none. The RATIONALE has the same slip ("handlers included, to follow one stated protection by a facility"). Fix: "STND.CONC.3 has each shared mutable object follow one stated protection, and a protection by synchronization use a facility that the memory model ... defines as ordering accesses; in C++ those facilities are ...". In the RATIONALE, "which the dropped sentence restated" becomes "of which the dropped sentence stated the synchronization case".
- Should-fix: the dropped CXX.23 S1 required synchronization for every conflicting access, which is narrower than CONC.3 (which also admits confinement, immutability, and message transfer). The history row and RATIONALE say "restated". Say "stated the synchronization case of", so the record does not claim identity.
- Optional: the title "Synchronization of shared state" now fits only the handler rule. The Note repeats "(STND.CXX.23)" twice in one sentence. The onset sentence says CXX.26 "cites" CONC.25, but only the Notes do.
- Checked: CXX.15 and CXX.23 remove only text that CONC.6 and CONC.3 hold, and CXX.15 keeps DSGN.1 content (owner, validity, failure). CXX.26 S2 is kept for a real reason: it asks for the race-detecting build wherever C++ runs in more than one thread, while CONC.25 applies only where the means of the work include one. HW.11 is dropped only where its sentence was dropped.

Verdict: accept after the Defect fix.

## STND.PY 1.0.1 (editorial)
- Should-fix: the Note and RATIONALE say PY.17 "adds the Python means, a generator that a facility of the generator library derives". The PY.17 text names no Python construct, so the true added content is the wider scope (work divided into parts, separate runs included). Fix: drop "adds the Python means" and keep the scope argument. That argument is sound, because CONC.23 reaches only concurrent tasks of one run.
- Optional: PY.17 and JL.24 are not cited from their bodies, while CXX.23 and JL.27 now are. The inconsistency follows from keeping PY editorial. Say so in the Note if the custodian wants it.
- Checked: no provision text changes, onset unchanged, References row added.

Verdict: accept.

## STND.JL 1.1 (minor)
- Should-fix: as for CXX, JL.27 S2 ("a lock or atomic operations") is narrower than CONC.3, so "restated" in the row and RATIONALE should read "stated the lock and atomic case of". The retained Note sentence "a lock or atomic operations among them" matches the CONC Terms definition of Protection.
- Optional: the retained sentence on partition "declared under HW.12 and REPRO.3" could cite STND.CONC.21 and STND.CONC.22, which now hold it. JL.27's title is still apt.
- Optional: "STND.MPI ... govern distributed computing where they apply" is hedged enough. It could say "message passing" to avoid implying Julia's distributed facilities are MPI.
- Checked: the JL.27 S1 kept (it names `Threads.threadid()`) and cited to CONC.16 S2 (correct sentence). JL.24 kept for scope. The onset sentence is right. The new References rows (CONC, MPI, OFFLD, HW.GPU) are all cited in the text. OFFLD.2 and HW.GPU.3 are correct targets.

Verdict: accept.

## NUMER 1.3 (minor)
- No Defect and no Should-fix. The Note states the custodian's assignment as the ledger records it, and does not claim a ruling that was not made.
- Optional: the row's provision column lists only NUMER.24, while the streams matter also has CONC.23 and VVUQ.62. That is right for an owning table (LVL1 lists its own provisions), and the Note says where the other two live.

Verdict: accept.

## STND.CONC 1.0.1 (editorial, after STND.WFLOW)
- Defect (factual): "STND.OFFLD.9 to STND.OFFLD.14 ... govern [the memory of accelerators]". OFFLD.14 is floating-point state across the boundary, and OFFLD.13 is the memory scope of synchronization. Fix: "STND.OFFLD.9 to STND.OFFLD.12 and STND.OFFLD.21 to STND.OFFLD.23".
- Should-fix: `STND.WFLOW.34` is a number citation into a draft that may be renumbered. WFLOW.34 is now "File system guarantees relied upon", which matches. Recheck at adoption, or cite "STND.WFLOW" alone.
- Should-fix: the reading-copy headers carry rehearsal entry numbers (OMP 117, CXX 118, PY 119, JL 120, NUMER 121, CONC 124). The WFLOW draft says it is entry 118. Regenerate every draft after the lead fixes the order.
- Optional: "directive-based threading with OpenMP" names a specification in a Purpose that says the standard names no language, library, or platform. Drop "with OpenMP".
- Checked: OMP.7 is the OpenMP form of CONC.16 (tied tasks, threadprivate across scheduling points). The CXX.23 and CXX.15 descriptions fit CXX 1.1. The History row and RATIONALE give no WFLOW entry number.

Verdict: accept after the Defect fix.

## Other stale text in STND.CONC from this round's standards
None is false. These are incomplete or in tension, all Optional unless noted.
1. Notes on CONC.1: "HW.GPU.3 ... and STND.MPI.5 ... remain its forms". STND.OFFLD (cites CONC.1) and STND.WFLOW (jobs as asynchronous operations) are also forms.
2. Notes on CONC.25: "STND.CXX.26 and STND.MPI.25 are the forms ... for C++ and for MPI". STND.OMP.32, STND.OFFLD.30, and the STND.STDC, STND.FTN, STND.RUST drafts have forms or cite it.
3. Notes on CONC.16: only JL.27 and OMP.7 are named. The STND.RUST draft states the work-stealing case as a CONC.16 form.
4. Notes on CONC.23: "STND.PY.17 and STND.JL.24 state the same". STND.OFFLD cites CONC.23 as well.
5. Terms and Purpose: the STND.SV draft says it does not make a simulation process a concurrent task, though the Term ("another sequence of execution of the work that runs, or is able to run, while another has not completed") could be read to include one. Add a sentence to the Purpose or Terms (or a Term note) on event-driven simulation, or leave STND.SV's carve-out as its own scope statement.
6. Notes on CONC.28: STND.LEAN.19 is the correspondence statement that CONC.28 asks of a model. It is not named.
7. STND.BUILD: nothing stale.
