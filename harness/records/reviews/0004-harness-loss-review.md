# Review 0004: governance without a harness

Independent review (QA.7). Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `53afcf5`: STND.HARN 0.3 as `drafts/harn-0.1-tools/build_harn.py` generates it, and the STND.DFLT 1.2 proposal `drafts/dflt-1.2-tools/dflt_12.py` |
| Reviewer | Claude (independent review agent); not the author of either change |
| Directive | "In the event the harness code is lost or inoperable, the governance documents still apply." |
| Scope | Every provision whose obligation could lapse, or become impossible to meet, without a harness or a derived configuration: STND.HARN 1 to 29, STND.DFLT (5, 15, 17, 22 to 26, Terms), STND.INSTR, the Checks sections of STND.DRAFT and STND.IDENT, GOV.35 to GOV.39, INTPR.12, GUARD.2; the new text against STND.DRAFT; README.md, governance/README.md, pointer.md |
| Result | STND.HARN 0.4 (redrafted, STND.IDENT.10); STND.DFLT 1.2 proposal revised and rehearsed, not applied; no amendment proposed to another adopted document |

## Findings

Severity: Medium means an obligation lapses, or rests on an agent's judgment, when a harness or configuration is lost or inoperable, or a record would be false. Low means a restatement, a stale or inexact statement, or a non-actor bound.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | STND.DFLT.22 (1.1) displaced a provision on the record alone, so a lost or inoperable configuration left STND.DFLT.24 and STND.DFLT.25 displaced with nothing enforcing them. The proposal's condition "installed as the entry records and in operation" named no decider, and "in operation" needs the agent's judgment (GUARD.2) | Fixed in `dflt_12.py`: "and that configuration is confirmed"; the Terms define Confirmed: found, in the current session and by a verifier the agent is unable to alter, installed as the entry that records it states. With no verifier, the provision applies |
| 2 | Medium | The fifth exempt class of STND.DFLT.15 rested on the record alone. A checkpoint mechanism that stops working left changes exempt with no checkpoint, unlike classes 1 and 2, which require verification | Fixed in `dflt_12.py`: ", and that mechanism is confirmed" |
| 3 | Medium | No provision required a derived configuration to fail closed. The adapter turns a guard failure into a refusal (`\|\| exit 2`, review 0003 finding 13), but a replacement harness could drop it, so a configuration confirmed at session start that later loses its program would let actions through while provisions stay displaced | Fixed: STND.HARN.29 "Fail-closed configuration" (PRIME.4, rank 0). A guard that misses its 10 s timeout still lets the call proceed in Claude Code; `coverage.md` states that gap (STND.HARN.22) |
| 4 | Medium | STND.HARN.29 "Harness unavailable" (0.3). What it meant, that governance applies and can be audited without a harness, is GOV.38 with INTPR.12. As a new duty it was ill-defined: "operable" and "relies on" have no criterion. It was inexact, since checks need the anchor file outside the corpus, `gpg`, and hashing, not only reading. For an agent it invited self-verification of signatures, which STND.DFLT.17 bars (a verifier it is unable to alter) | Removed. The Checks section says that an actor performs a check by hand from its provision, and README.md shows how. Its number goes to finding 3, as draft renumbering allows (review 0002) |
| 5 | Medium | `dflt_12.py` fixed `at` at `2026-10-10T00:00:00+00:00`, before entries 40 and 41 (16:04 UTC), so the ledger would run backwards and record a false time that PRIME.5 keeps forever; the rationale fixed the date of ratification too | Fixed: the history row date and `at` come from one UTC clock at application (check v.4 compares them); the rationale names no date |
| 6 | Low | The Purpose sentence restated GOV.38, as review 0002 finding 15 removed before. Before DFLT 1.2 it was also false of a configuration (finding 1) | Removed; the Notes on STND.DFLT.22 state the condition "confirmed" |
| 7 | Low | STND.HARN.25 bound "the configuration", a non-actor that is lost with the configuration | Recast: "a harness SHALL derive a configuration that refuses ...", like STND.HARN.21. The agent's duty to halt and refer (PRIME.14) is unaffected |
| 8 | Low | The term Anchor file tied the file to "the account that runs the harness", which no account is without a harness | "the account that checks the ledger" |
| 9 | Low | README.md "without software" gave no way to check signatures, the anchor, or a configuration, and its corpus-hash line was inexact (order, no final line feed) | Rewritten as eight steps with commands. Tested on the live ledger: all 41 entry hashes and links, all 7 latest pins, and one entry signed with a scratch key (`gpg: Good signature`) |
| 10 | Low | README.md and pointer.md still described STND.HARN as 28 provisions at 0.2; governance/README.md accepted a replacement "once it regenerates the existing manifests byte for byte", against STND.HARN.28, and named `../tools/` | Updated |
| 11 | Low | `build_harn.py` docstring named 0.2 | Fixed |
| 12 | Low | DFLT 1.2 rationale: accurate for the old scope, but it now needs to cover two provisions and record "in operation" as an alternative weighed | Rewritten. Class minor (STND.IDENT.3) confirmed: a displacement and an exemption narrow, no principle changes |

## Considered, no change

- STND.HARN.7 to 17 and 21 to 24 bind a harness or an adapter. Without one, nothing is derived or reported. The ledger, register, and anchor stay checkable by hand (README steps 4 to 6), and the sources of the rows of STND.HARN.21 bind the agent throughout.
- STND.HARN.26: the checks of a rehearsal may be performed by hand. A script that needs the package does not run without it, and the change is then made by hand under GOV.40 and GOV.36.
- STND.DFLT.5 and 23: met by hand (`sha256sum`, `gpg`). STND.DFLT.17: without a verifier the agent relies only on direct or GUARD.12 authorizations, which is more restrictive. STND.DFLT.24 and 25 apply unless displaced under STND.DFLT.22 as amended. Working bounds: a lost configuration opens nothing, so the default bounds apply. STND.DFLT.26: a spending cap is not derived by a harness.
- STND.INSTR: STND.INSTR.2 defers to STND.DFLT.15 as amended; STND.INSTR.7 reports the last run of each check, or none.
- The Checks sections of STND.DRAFT and STND.IDENT are informative. Naming scripts there creates no obligation.
- GOV.35 to 39, INTPR.12, and GUARD.2 are the basis of the fixes and need no change.

## Consequences and code findings (not fixed)

| # | Severity | Finding |
| --- | --- | --- |
| C1 | Low | `environment --check` confirms installed files and programs, not the checkpoint mechanism the entry names (Claude Code checkpoints). Under DFLT 1.2 the fifth class then needs another verifier, such as the human owner |
| C2 | Low | The harness in the work is alterable by the agent's account, so it is not a verifier that the agent is unable to alter. Until one is installed outside the work, the human owner confirms, and otherwise the provisions apply. This is restrictive and intended |
| C3 | Low | Order: apply DFLT 1.2 before adopting STND.HARN 0.4, whose Notes use "confirmed"; then `compose --write`, and refresh the project's reading copy of STND.DFLT |

## Results

| Check | Result |
| --- | --- |
| `python3 -B -m govharness verify governance` | ids, mnemonics, references, manifests, ledger, templates, status, logic: PASS; ledger 41 entries |
| `check governance --no-z3 --out-dir <scratch>` | exit 0; no FAIL or WARN; no finding on STND.HARN in `logic_report.md` or `drafting_punch_list.md`; l.3 confirms the ranks (HARN.29: 0) |
| `manifests --check`, `references --check`, `compose --check` | stale: 0; PASS; stale: 0 |
| `rehearse governance drafts/dflt-1.2-tools/dflt_12.py` | all eight checks PASS on the copy; one entry appended (seq 42); source unchanged. Applied to a scratch copy, `check` reports no new finding on STND.DFLT |
| `TMPDIR=<scratch> python3 -B -m unittest discover -s tests -t .` | 112 tests, OK |

## Verdict

Accepted as STND.HARN 0.4 for the custodian's decision, with the revised STND.DFLT 1.2 proposal to ratify and apply first. With both, no provision found lapses when the harness or a derived configuration is lost or inoperable. A displacement or exemption that depends on a configuration ends when no verifier confirms it, a derived configuration fails closed, and every check can be performed by hand.
