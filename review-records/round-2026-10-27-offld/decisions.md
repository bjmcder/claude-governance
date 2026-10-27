# Round of 2026-10-27 on offloaded work: decisions and drafting

The custodian directed on 2026-10-27 that the open item on STND.OFFLD.31 go ahead: decision 27 of `review-records/round-2026-10-25-close/decisions-final.md`, from its item 18, had left for STND.OFFLD's next minor amendment the first filling of caches and memory, which STND.PERF.12 names among the costs of first use and STND.OFFLD.31 does not, though STND.PERF.12 leaves offloaded work to STND.OFFLD.31.

## Drafted, for ratification

1. **STND.OFFLD 1.1 (minor).** The second sentence of STND.OFFLD.31 asks the costs of first use, among them initialization, compilation at load, and the first filling of caches and memory, the words of STND.PERF.12, in place of the costs of a first submission, among them initialization and compilation at load. The Notes say that the two name the same costs, and that a migration of memory at first access is among the first filling of memory. "Costs of first use" reaches beyond the first submission, to the first use of a context, a module, or a buffer, as STND.PERF.12 already does for every other measurement. Transition (GOV.42): a measurement recorded before this amendment needs no new statement. A default; no floor is raised.
2. **STND.PERF 1.0.1 (editorial).** The Notes drop the clause "a later amendment of STND.OFFLD could have STND.OFFLD.31 cite them", which STND.OFFLD 1.0.1 made stale.

Script: `tools/amendment-scripts/apply_offld_round_2026_10_27.py`, two transactions, entries 198 and 199 in rehearsal; every check passes with the g.18 warning that the corpus already carries. The pairs of STND.HARN.28 whose changed side is STND.OFFLD.31 are five: HW.22, HW.CPU.4, HW.GPU.4, HW.QPU.8, and NUMER.17, on RSRC.4.

## Review

`review.md`, by an agent of another configuration: no defect.

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | The transition is not among what is put to the custodian | Taken: item 1 now states it, for ratification. |
| S2 | The Note on memory that migrates on demand does not say whether that migration is a first filling of memory | Fixed: "such a migration at first access is among the first filling of memory that the second sentence of STND.OFFLD.31 names", after the fact, which keeps its mark unverified. |
| O3 | The new sentence of the Notes reads heavily | Fixed: "The two name the same costs of first use, which are initialization, compilation at load, and the first filling of caches and memory, so one record of offloaded work that states them meets both." |
| Q | The reach of "costs of first use" beyond the first submission | Put to the custodian in item 1. |

Rehearsal after the fixes: entries 198 and 199; every check passes with the g.18 warning that the corpus already carries; no drafting finding on STND.OFFLD.
