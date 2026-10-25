# Cold verification of STND.TEST 0.3, STND.WPROC 1.1, STND.CREW 1.1 (2026-10-25)

**Verdict: not ready until D1 is fixed.** One Defect (a conflict between two provisions), two Should-fix items, three Optional. The 0.2 dispositions are carried out.

## The round as applied

- `rehearse ... apply_round_2026_10_25.py`: 6 entries, seq 142 to 147 (MNEM, PERF, MNEM, TEST, WPROC 1.1, CREW 1.1), stamped at real times (09:14:48 to 09:15:04).
- `verify`: all checks PASS; the only warn is g.18 (bundles of three modals).
- MNEM rows run LEAN, PERF, TEST.
- The TEST Notes cite STND.PERF.23, which exists (regression guards on performance, with one on a quantity).
- `findings.py` on `STND\.(TEST|PERF|WPROC|CREW)`: no defect. All items are review notices, "three modals: confirm the bundle is never applied apart" (CREW, WPROC, PERF.23, TEST.10), plus one g.14 on CREW.13, which this round does not touch.
- `apply_test_round.py` gives the same documents (`diff -r` empty apart from the ledger). Entries differ only in `at`, `hash`, `prev`; rationales are equal.
- Scripted check of every changed provision: modals, banned words, and body IDs against front matter are clean. The reading copy matches the rehearsed bodies.

## Defect

**D1. TEST.10 sentence 2 contradicts TEST.6 at a release.** It says "Each run before the merge of a branch into its parent branch SHOULD hold only the selection that TEST.3, .4, .5 give". The release is a merge of the development line into the main line. TEST.6 asks a full-suite run before the release record. TEST.5 and the Integration depth Term give a main-line merge no depth and no tiers, so the selection is undefined there. Sentence 1 exempts a TEST.6 run; sentence 2 does not. The Notes line "a run of every test there is no full-suite run under STND.TEST.6" reads as if a pre-merge full run does not count.
Fix: sentence 2 opens "Other than a full-suite run under STND.TEST.6, each run before the merge ..."; Notes: "a full-suite run before a release is a run under STND.TEST.6 and not limited by the second sentence." No modal or ID is added.

## Should-fix

- **S1. Rationale of STND.TEST** does not state the pre-merge limit. It says "runs between merges limited to the tests that the changes and the last failures reach (STND.TEST.10)". Add "and runs before a merge to the selection of STND.TEST.5".
- **S2. TEST.11 secret exclusion is ambiguous in reach.** ", a secret excluded" follows only the last list item, and the first assertion (its message) can print a secret. Fix: "... and the output that the assertion judged, each kept without a secret (PRIME.10)".

## Optional

- O1. TEST.10 sentence 3 "holds other tests" has no antecedent and would also catch a TEST.6 run. Fix: "holds a test that sentences 1 and 2 leave out, other than in a full-suite run under STND.TEST.6".
- O2. TEST.5 pairs "tiers ... other than the tests that TEST.4 holds": a tier set against tests. Fix: "..., and the tests that STND.TEST.4 holds from every tier in addition".
- O3. The Notes call PERF.23 "the regression guard on time"; the provision says "a quantity". Fix: "a regression guard on a quantity, time among them".

## Dispositions

- **S1 (full suite):** holds. Both Terms include skipped, disabled, and quarantined tests, so disabling cannot shrink the run. TEST.9 reports their verdicts apart; AGENT.47 and WPROC.13 still carry the disablement. Deleting a test is left to TEST.19.
- **S2:** present in TEST.10, but see D1.
- **S3:** present in TEST.5, with STND.TEST.4 in refers_to. See O2.
- **S4, S7 to S11, O1, O3, O4, X1:** present; STND.DEPS is in References.
- **S5:** see S2 above. The Verdict key Term and TEST.8 exclude secrets.
- **S6:** CREW.9 selects through TEST.3 and TEST.4 in body, Notes, and rationale, with matching refers_to. It is consistent with TEST.10 s1.
- **S12:** both rationales cite the IDENT.3 test and end with the fixed tail.

## Other checks

- **g.18 on TEST.10:** acceptable. Three sentences, three modals, and the Notes say "never applied apart". After D1, the exemption in sentence 2 keeps this true.
- **Notes:** no indicative obligation and no narration found.
- **Class:** WPROC is minor, because the permission of WPROC.9 widens (IDENT.3 "adds, alters, or removes an obligation or permission"). CREW is minor, because CREW.9 and CREW.15 each add an obligation. Neither alters a prime directive, so neither is major, and none is editorial.
- **Not checked:** the custodian ruling of 2026-10-25 (taken from the brief), the WPROC transition claim, and the research notes.
