# Final verification: HW 1.1.1 and unit 0007

Verified by reading, by applying the script to a copy of the corpus (scratchpad, source untouched), by probe scripts, and by running test_guard + test_environment (66 OK) and tests.test_architecture (10 OK).

## A Findings
1. Optional/residual class risk (HW/_doc.md Notes, line 94). "HW.8 is read as asking the whole run to halt ..." still widens the subject of HW.8 (an execution path, Term "Execution path") to a run, for every multi-process run, MPI or not; only STND.MPI.6 (LVL2, MPI) requires survivors to respond. The wording is a scoped reading and STND.MPI.6 supports it for MPI, so I judge it editorial, but the custodian should ratify knowing this. Fix if doubtful: end the sentence with "in a program that uses the Message Passing Interface" or treat as minor.
2. Optional. "A process that halts ..." is not tied to a hardware fault; HW.8 covers only detected, uncorrected faults and exhaustion. "silent hang" remains true to PRIME.4, so no change required.
Verified accurate: script applied to a copy yields exactly hw-1.1.1.diff (revision, Note, STND.MPI row sorted and titled correctly, history row, ledger seq 110); anchor sits in Notes (informative); no obligation word; American English; no STND.DOCS.9 pattern; row and rationale state the same reading and cite STND.MPI.6; REPRO.5 and entry-15 sentences match the 1.0.1/1.0.2 precedents; AT (12:00) follows entry 109 (08:38). Not checked: `rehearse` itself, `verify`, pair review beyond what review-pairs-hw.md states.

## A Prior findings
| Finding | Status |
|---|---|
| Cold 1 "path is the whole run" redefines subject | Resolved (reworded as scoped reading; residual note A1) |
| Cold 2 "halts alone" overstatement | Resolved |
| Cold 3 "as STND.MPI reads it" in row and rationale | Resolved |
| Cold 4, 5 optional | Resolved (5 met by scoping) |
| Cold 6 class in rationale | Resolved |
| Pairs: tension with Term | Resolved (same rewording) |

## B Findings
1. Should-fix. Shell `chmod` of the store directory, and `rm`/`mv` of an opened secret, pass the guard but fail in the sandbox, because `denyWrite` on the store directory is a read-only mount. Checked with `bwrap --ro-bind`: chmod and rm both return "Read-only file system" (Claude Code's own sandbox not checked). So the restore step of STND.DFLT.30 and the removal of a needless secret (STND.DFLT, AGENT.44) cannot be done by shell, and the file tools have no delete. Neither coverage text (claude_code.py STORE_GAPS) nor DoD 2/4 nor decision 0002 says so; DoD 2 says confirming permissions passes. Fix: state it in STORE_GAPS["write-bounds"], the unit record and decision 0002, or provide another route (refer to the owner).
2. Optional. `cd secrets && cat token` (the opened file) is referred, while `cd secrets && ls` and `cat secrets/token` pass. Cause: the guard keeps all earlier directories and resolves `cd secrets` against each, so `secrets/secrets/...` is read as a closed file. Pre-existing design; fix would be a note or an exemption. Not a bypass.
3. Optional. Audit line 5 says `test_coverage_names_the_gaps` covers the gaps (sandbox only while it runs, unparsed programs, case); the test asserts only the phrase "secret store" in both rows and no `| full |`. Fix: assert on "While the sandbox runs" and "ignores case".
4. Optional. Ruff: no config in the tree; `ruff check govharness tests` reports 57 under defaults, so "ruff clean on changed lines" in audit 6 is unverified by me.
Verified working (probes): store as a link (Read, Grep, cp -r, mv, rm all referred; opened file passes); `cp -r`/`cp -a`/`mv`/`rm -r` of the store referred, also `./secrets/`, trailing slash, `../` spellings, hidden file, globs; mode-000 store (real chmod, not mocked) referred for Grep and cp -r, `ls` and `chmod 700 secrets` pass; store that is a file referred; routine passes: `ls`, `ls -R`, `stat`, `chmod` (also -R) of the store, `cat secrets/token`, `cp secrets/token`, `cp`/`mv` of non-store files, `cp -r src src2`, Grep on a subdirectory outside the store, Glob anywhere; Grep of the work root or with no path is referred only while a closed file exists, as DoD 3 says; with no store option, or a store option but no directory, nothing is referred. Known and admitted gaps, reproduced: `grep -r x secrets`, `find -exec cat`, `tar`, `rsync`, `cat Secrets/key` (case), a link created in the same line. Coverage text matches these.

## B Prior findings
| Finding | Status |
|---|---|
| Defect 1 store as symlink | Resolved |
| Defect 2 `cp -r`/`mv` of store | Resolved |
| Defect 3 unlistable store | Resolved (fails closed, no exception) |
| 4 unparsed programs | Resolved (admitted in text) |
| 5 coverage overclaim, case, link | Resolved |
| 6 missing tests | Resolved (new tests present; DoD audit lines all point to existing tests) |
| 7 null store | Resolved |
| 8 RUF012 | Resolved for that item; ruff overall not verifiable |

## Verdict
A: ready to present for ratification, with A1 disclosed to the custodian.
B: ready after one documentation fix (B1). No guard defect found; the code enforces what the coverage text says, but the text omits that the sandbox blocks the shell chmod and removal that STND.DFLT.30 and AGENT.44 need. B2 to B4 may follow.
