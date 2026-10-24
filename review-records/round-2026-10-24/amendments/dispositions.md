# Dispositions of the reviews of the six amendments (round of 2026-10-24)

Reviews: `review-cold.md` and `review-pairs.md` in this folder. The scripts are in `tools/amendment-scripts/`.

## Rehearsals after these fixes

- The round, `apply_round_2026_10_24_amend.py`, appends five entries, 117 to 121: STND.OMP 1.0.1, STND.CXX 1.1, STND.PY 1.0.1, STND.JL 1.1, and NUMER 1.3. `verify` passes.
- The full sequence, `.scratch/amendments/rehearse_full_sequence.py`, runs this round, then `apply_build_round.py`, then `apply_wflow_round.py`, then `apply_conc_1_0_1.py`. It appends ten entries; STND.CONC 1.0.1 is entry 126 in that order. `verify` passes.
- STND.BUILD, STND.WFLOW, and STND.CONC alone, `.scratch/amendments/rehearse_wflow_then_conc.py`, appends five entries. `verify` passes.
- `findings.py` gives the same counts as before the round: CONC 5, OMP 9, CXX 11, PY 3, JL 8, NUMER 2. All are g.18 or g.11 notices of class review, and none is a defect.
- The drafts, diffs, and pair lists in this folder have been regenerated. STND.CONC's come from the full-sequence copy; the other five come from the round copy.

## Cold review

| Document | Finding | Class | Disposition |
| --- | --- | --- | --- |
| STND.OMP | The glosses on STND.OMP.27 and STND.OMP.28 were lost | Optional; the coordinator asked for it | Fixed. The sentence again names "on static data on a device" and "on the requires directive". |
| STND.OMP | The mapping sentence copies OFFLD's wording "its second sentence of" | Optional | Kept, so that the mapping reads the same in both standards. |
| STND.CXX | The Note and the RATIONALE describe STND.CONC.3 as if every protection uses an ordering facility | Defect | Fixed with the review's wording. The Note now says each shared mutable object follows one stated protection, and a protection by synchronization uses a facility that the memory model or hardware contract defines as ordering. The RATIONALE now says "of which the dropped sentence stated the synchronization case". |
| STND.CXX | The history row and RATIONALE say the dropped sentence "restated" STND.CONC.3 | Should-fix | Fixed. Both now say it "stated the synchronization case of" STND.CONC.3. |
| STND.CXX | The title "Synchronization of shared state" | Optional | Kept. The remaining rule concerns synchronizing state shared with handlers, and keeping the title avoids moving a locator. |
| STND.CXX | "(STND.CXX.23)" appears twice in one sentence | Optional | Fixed. The sentence now reads "C++ adds one rule for handlers: ... (STND.CXX.23)". |
| STND.CXX | The onset sentence says STND.CXX.26 "cites" STND.CONC.25 | Optional | Fixed. It now says the Notes give STND.CXX.26 as a form of STND.CONC.25. |
| STND.PY | The Note and RATIONALE say STND.PY.17 "adds the Python means" | Should-fix | Fixed. Both now give its wider scope as the reason: every division of work into parts, separate runs included. The Note says STND.PY.17 "states for the work in Python the rule of STND.CONC.23". |
| STND.PY | STND.PY.17 and STND.JL.24 are not cited from their bodies | Optional | Kept, so that STND.PY stays editorial. It is a decision for the custodian: a body citation of STND.CONC.23 would make STND.PY a minor amendment. |
| STND.JL | The history row and RATIONALE say the dropped sentence "restated" STND.CONC.3 | Should-fix | Fixed. Both now say it "stated the lock and atomic case of" STND.CONC.3. |
| STND.JL | The partition sentence could cite STND.CONC.21 and STND.CONC.22 | Optional | Deferred to the coalesce, with the other STND.CONC citations. |
| STND.JL | Say "message passing" rather than "distributed computing" | Optional | Kept. The review judged the hedge "where they apply" enough. |
| NUMER | The table lists only NUMER.24 | Optional | No change. An owning table lists only its own provisions, and the Notes cite STND.CONC.23 and STND.VVUQ.62. |
| STND.CONC | "STND.OFFLD.9 to STND.OFFLD.14" | Defect | Fixed. It now reads "STND.OFFLD.9 to STND.OFFLD.12 and STND.OFFLD.21 to STND.OFFLD.23". |
| STND.CONC | STND.WFLOW.34 cites a draft that may be renumbered | Should-fix | Fixed. STND.WFLOW 0.2 renumbers it to STND.WFLOW.32, and both places now cite STND.WFLOW.32, matching `content_wflow.py`. The number still needs a recheck at adoption. |
| STND.CONC | The reading copies carry rehearsal entry numbers | Should-fix | Open. The lead regenerates the drafts once the order is fixed. In the current full sequence STND.CONC is entry 126. |
| STND.CONC | "directive-based threading with OpenMP" names a specification in the Purpose | Optional; the coordinator asked for it | Fixed. The Purpose now reads "STND.OMP holds those for directive-based threading". |
| STND.CONC | Stale or incomplete items 1 to 6, forms of STND.CONC.1, .16, .23, .25, and .28 in STND.OFFLD, STND.OMP, STND.WFLOW, and the new language standards, and the event-driven simulation question of STND.SV | Optional | Deferred to the coalesce, as the coordinator directed, when the numbers of the new standards are final. |

## Pair review

| Item | Finding | Class | Disposition |
| --- | --- | --- | --- |
| 1 | The STND.JL class paragraph says STND.JL.27 "asks for the protocol of DSGN.15" | Should-fix | Fixed. It now says that STND.JL.27, the Julia form of the second sentence of STND.CONC.16, instantiates DSGN.14 as that provision does, rests on no row, and applies from CSQ3. The protection of shared state is STND.CONC.3, and the verification of its invariants stays with DSGN.15 from CSQ2. |
| 2 | STND.JL.27 could instantiate DSGN.14 | Optional; the coordinator asked for a decision | Done. STND.JL.27 instantiates DSGN.14 in place of DSGN.15 and cites it (DSGN.14, STND.CONC.16). The reason is that the rule concerns which state a task owns, as in STND.CONC.16, and not a protocol of shared state. Its onset stays CSQ3, because DSGN.14 rests on no row of STND.CLASS.10. The history row and RATIONALE say so. One effect: STND.JL.27 loses its three pairs, with AGENT.39, HDES.11, and HW.11, which rested on DSGN.15. No provision of a profile instantiates DSGN.14, so STND.JL.27 now has no STND.HARN.28 pair. STND.JL now has 167 pairs, down from 170. |
| 3 | STND.PY.17 and STND.JL.24 do not say how a part is defined | Optional | Kept, for the same reason as the cold review's citation item: STND.CONC.23 applies on its own, and there is no conflict. A decision for the custodian. |
| 4 | NUMER.2 matter name: "Independence of random streams" | Optional | Kept "Random streams of a computation divided among concurrent tasks", which follows the custodian's assignment at the adoption of STND.CONC. A decision for the custodian. |

## STND.CONC 1.0.1 completed at the coalesce

These items were deferred above, until the numbers of the new standards were final. Each citation below rests on the text of the standard it names: its provision bodies and Notes in `tools/amendment-scripts/content_*.py`, or `rendered/STND.OFFLD.md` and `rendered/STND.OMP.md`. The change stays editorial: it alters only the informative Notes and the derived References.

| Provision of STND.CONC | Forms or applications now named in its Notes | Source in the citing standard |
| --- | --- | --- |
| STND.CONC.1 | STND.OFFLD takes each submission as an asynchronous operation; STND.WFLOW takes each job submitted to a scheduler as one. The Notes of STND.RUST apply it to a thread that panics or whose join handle is dropped, and those of STND.SV to the tasks of a testbench. | OFFLD Terms; WFLOW Terms and Notes; RUST Notes; SV Notes |
| STND.CONC.2 | STND.OFFLD.8, the way the failure reaches device code. The Notes of STND.FTN read ERROR STOP as the halt it asks. | OFFLD Notes; FTN Notes |
| STND.CONC.3 | STND.STDC.35 (bit-fields), STND.FTN.11 (SAVE, module, and common variables), STND.RUST.21 (`Send` and `Sync`), STND.OFFLD.5 (host storage under transfer), and STND.SV.5 to STND.SV.8, the protection for simulation processes | STDC.35 body; FTN Notes; RUST Notes; OFFLD Notes; SV Notes |
| STND.CONC.5, STND.CONC.12 | STND.OMP.8 | OMP Notes |
| STND.CONC.8 | STND.RUST.23, which makes it mechanical | RUST Notes |
| STND.CONC.11 | STND.OFFLD.18. The Notes of STND.FTN apply it to DO CONCURRENT. | OFFLD Notes; FTN Notes |
| STND.CONC.13 | STND.RUST.22 adds what the drop of a future makes necessary | RUST Notes |
| STND.CONC.15 to STND.CONC.17 | The Notes of STND.RUST apply them to executors | RUST Notes |
| STND.CONC.17 | STND.OMP.19. The Notes of STND.FTN apply it to a library that sets floating-point modes. | OMP Notes; FTN Notes |
| STND.CONC.23 | STND.SV.23, the form for the random stimulus of a testbench | SV Notes |
| STND.CONC.25 | It applies to C and Fortran by its own scope. STND.OMP.32 adds the mapping check that race detectors miss, and STND.OFFLD.30 the checks of device code. | STDC and FTN Notes; OMP Notes; OFFLD.30 body |
| STND.CONC.27 | STND.RUST.33. One record meets STND.STDC.38 and STND.CONC.27. The second sentence of STND.BUILD.13 makes STND.CONC.27 specific. | RUST, STDC, and BUILD Notes |
| STND.CONC.28 | STND.LEAN.19, with the row Code that runs of STND.LEAN.4 | LEAN Notes |

Other dispositions:

- **Correction.** The Notes said "the third sentence of STND.CONC.11", but STND.CONC.11 has two sentences. The text now reads "the second sentence".
- **Not named, because the text does not support a form.**
  - The STND.RUST Notes say only that STND.CONC.15 to STND.CONC.17 govern executors and state local to a thread; they name no Rust provision as a form of STND.CONC.16. The cold review had suggested one.
  - The Notes of STND.FTN on STND.CONC.21, STND.CONC.22, and STND.CONC.24 are readings, not forms.
  - The STND.WFLOW Notes on STND.CONC.10, STND.CONC.13, STND.CONC.14, and STND.CONC.29 are also readings, not forms.
- **Cold review item 5, event-driven simulation.** Left to STND.SV. Its Notes apply the Term Concurrent task to simulation processes and the Term Event loop to the kernel, and the new STND.CONC sentence on STND.SV.5 to STND.SV.8 records that reading.
- **STND.WFLOW.32.** Kept as the custodian's coordinator directed. It is "File system guarantees relied upon" in the final `content_wflow.py`.
- **Rehearsal.** `apply_round_2026_10_24.py` gives 23 entries, 117 to 139, with STND.CONC 1.0.1 at entry 137. `verify` passes. `findings.py` on STND.CONC gives 5 g.18 review notes, the same as before the round, and no defect.
  - The rehearsed copy is at `.scratch/amendments/round/governance`.
  - `STND.CONC-draft.md`, `STND.CONC.diff`, and `STND.CONC-pairs.md` (354 pairs) are regenerated from it.
  - References now also lists STND.BUILD, STND.FTN, STND.LEAN, STND.RUST, STND.STDC, STND.SV, and STND.WFLOW.
