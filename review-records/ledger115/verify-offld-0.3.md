# Delta verification of STND.OFFLD 0.3 (2026-10-24)

**Verdict: not ready.** One blocking item (N1), a one-clause fix in the Notes.

Script checks on the rehearsed copy: `verify` passes eight of eight; `findings.py` gives only the expected g.18 notice for OFFLD.7. The rehearsed bodies of OFFLD.7, .10, and .17 match the 0.3 reading copy. I diffed 0.2 and 0.3: eight Notes edits and three body edits, all listed in the dispositions.

## Status

| Item | Status |
| --- | --- |
| B1 in-order queue | Done. Matches o1 (in-order rule; SYCL out-of-order default) |
| B2 migration | Partly. See N1 |
| B2 cache | Done. "one vendor's runtime" matches o3 (per-user, size limit, "specific to that vendor") |
| B2 non-finite | Done. 1.01 percent of outcomes in o3 |
| B3 OFFLD.7 S1 | Done. One condition in each sentence |
| B3 OFFLD.10 | Done. The condition opens the sentence. One modal |
| B4 resubmission | Done, with a preference (P2) |
| S1 OFFLD.5 hazard | Done. Marked an inference |
| S2 CONC.3 wording | Done. No claim that the host is a concurrent task |
| S3 processes | Partly (P3) |
| S4 onset paragraph | Done, with a preference (P4) |
| S5 OFFLD.17 S2 | Done. One condition |
| S6 masks | Done. Limited to one programming model |
| RATIONALE | Matches 0.3. The stale phrase is replaced in line 24 and the ledger |
| Optional CONC.11 | Kept, with a reason. Accepted |

## Blocking

- **N1. Unsupported claim left in the Notes (the second half of B2).** The Notes say that on oversubscription "the run continues with no error and is able to thrash (o1, H4)". o1 H4 supports "thrashes" and, for legacy systems, "cannot allocate more managed memory than the physical size of GPU memory". Nothing in o1 says the run continues with no error. The row says the same code "faults, thrashes, or runs correctly depending on hardware". The old text had the same flaw and the fix kept it. Cut "with no error" or mark it as an inference. For example: "the runtime library migrates it on demand, which o1 reports can thrash, and on a legacy system does not allow".

## Preferences

- **P1.** OFFLD.7 S1 and S2 say "later", and the anchor is the error named in the condition. That is clear enough. No change.
- **P2.** The resubmission sentence ("is one through another context or another process") reads as a duty. Write "a resubmission that complies with STND.OFFLD.7 cannot be one through that context". "Another process" is not a consequence of OFFLD.7.
- **P3.** Review item S3 asked to restrict context sharing to components and libraries of one process. The text "where they share a context" is correct but still lists processes, which cannot share a context.
- **P4.** "apply from CSQ2, the three sentences of STND.OFFLD.7 together" trails the list and is ambiguous. Write "apply from CSQ2 (the three sentences of STND.OFFLD.7 apply together)".
- **P5.** OFFLD.10 now reads as release once the work completes, where 0.2 said "after". A pool that keeps an allocation for reuse is in tension. Not a conflict, because the provision is a default under REPRO.7.

## Rules and conflicts

Changed sentences contain no banned word and no second condition, and each has one modal. Titles are unchanged. No change adds a restatement of CONC, HW, or ANNEX, and no change adds a conflict. All the Notes sentences touched are in the indicative as descriptions of the sources or of the provisions, apart from P2.
