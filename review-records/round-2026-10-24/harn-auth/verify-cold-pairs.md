# Verification of the answers to the cold and pair reviews (2026-10-24)

Read: commit ce8674c, the changed scripts, rehearsed copy `/tmp/rehearsal-y2u44tvi/governance`.

## By script

- Rehearsal of the round: entries 117 and 118 append. `verify`: all PASS (the existing g.18 notice only). `findings.py 'STND\.(PROJ|HARN)'`: only the two older notes on STND.HARN.28; none on STND.PROJ.6, .7, or STND.HARN.29.
- `govharness pairs`: STND.PROJ 12 pairs (unchanged, all covered in the earlier record); STND.HARN 16 pairs. The stored lists in the worktree hold 12 and 16 rows.

## Dispositions

| Item | Result |
| --- | --- |
| Defect 1, time of test | Met. HARN.29 sentence 1 tests the rows at derivation and Dates also at the write ; the Notes name the interval; the code compares expiry at the write. |
| Defect 2, GUARD.12 | Met. `delegable_to` is a PROJ.6 field; HARN.29 has the row Extension and instantiates GUARD.12; `--role` exists; `authorizations.py` reads `delegable_to`. |
| Should-fix 1, commit | Met in substance: `commit` is limited to branches whose update neither publishes nor deploys, and `publish` includes such an update. See new item A. |
| Should-fix 2, Record vs DFLT.23 | Met. The Notes say the row is narrower, because an agent can append its own grant entry (PRIME.7), and a referral follows. |
| Should-fix 3, Notes | Met except item B. The owner duty and the "earlier of the two" rule are gone; the condition of lapse is described as untestable for a harness; the referral cites HARN.18. |
| Should-fix 4, transition | Met. The end waits for a QA.8-reviewed harness installed with its configure entry (HARN.20); the status of the HARN.26 to .28 part is left to the custodian, stated as such. |
| Should-fix 5, "ratified" | Open, by design: the lead sets the wording at the coalesce. The rationale now calls the floor ruling the custodian's to make. |
| Should-fix 6, expiry | Met. `until revoked` is admitted; the Dates row reads "where it has one". |
| Should-fix 7, guidance label | Met. The template sentence begins "Fill-in guidance:". |
| Should-fix 8, per entry | Met. The Standing row reads "no entry of it"; the Notes state that one irrevocable entry voids the authorization. |
| Optional 2, example | Met (`https://example.org/team/work`). Optional 1 (alternative form) not taken; no harm. |

## Fresh reading of the changed sentences

- **Drafting rules:** one modal per sentence; cited identifiers equal the instantiates and refers_to lists; no excluded word; the bundle is declared.
- **GUARD.10 to .13, PRIME.7:** the fields name class, scope, duration, extension, and grantor; a per-action authorization is never relied on, and irrevocable kinds always refer; an authorization with no `delegable_to` entry for the role opens nothing (PRIME.7: never widened by delegation). GUARD.13 does not arise: a standing write is possible only inside the provisioned environment. PRIME.8: no spending.
- **STND.DRAFT.42:** `until revoked` removes the only new owner duty; `provisioned` and `delegable_to` repeat what STND.PROJ.3 and GUARD.12 assign, and default to referral.
- **Floor argument of HARN.29:** sound for GUARD.2, GUARD.11, and the Extension row. Record and Signature go beyond DFLT.23 only toward referral, with reasons given. "At the cost of wording" now understates the harness's checks (Optional C).

## New pair

| # | Pair | Conflict | Unowned | Reason |
| --- | --- | --- | --- | --- |
| H15 | HARN.29 / AGENT.11 (basis GUARD.12) | no | no | AGENT.11 has a directing agent give each directed agent the authorizations that extend to it. HARN.29's Extension row has a configuration rely only on one whose `delegable_to` names the role or agent for which it is derived. Same rule from two sides; the row can only refer more. Complementary. |

H16 (HARN.29 / AGENT.17) stands as reviewed before. Pairs covered: 12 of 12 (PROJ), 16 of 16 (HARN); no conflict; no unowned matter.

## New findings

- **A (Should-fix, wording):** the PROJ.7 `commit` row reads "a named branch of a remote repository whose update neither publishes nor deploys": "whose" attaches to the repository. Write "a named branch, whose update neither publishes nor deploys, of a remote repository".
- **B (Optional):** the HARN Notes say "a derivation of the same configuration fails, which the check of STND.HARN.21 shows". A later derivation differs from the installed files; it does not fail. Write "differs from the installed configuration, which the check of STND.HARN.21 reports".
- **C (Optional):** replace "at the cost of wording" in the HARN Notes with "at the cost of wording and of the checks the harness makes".

Not checked: the new guard code and tests (the security review's); whether m.1 and m.2 implement HARN.26 to .28.

## Verdicts

- **STND.PROJ 1.2: adopt**, after A (wording).
- **STND.HARN 1.2: adopt**; B and C are optional. No blocking item. Both await the lead's rationale wording and the custodian's rulings on the floor argument and on the HARN.26 to .28 transition.
