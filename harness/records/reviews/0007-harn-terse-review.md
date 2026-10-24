# Review 0007: STND.HARN 0.7 verbosity cut

Independent review (QA.7) and edit. Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `bb0ea4d`: STND.HARN 0.7 (27 provisions) as `drafts/harn-0.7-tools/build_harn.py` generates it |
| Reviewer | Claude (independent review agent); not the author of the change |
| Directive | "Aggressively reduce the verbosity", under the standing instruction "aggressively minimize verbosity, maximize atomicity, and validate for global consistency" |
| Method | Each provision read against its parents (GOV.35 to GOV.39, GOV.48, PRIME.4/5/6/7/9/14, GUARD.2), STND.DFLT 1.2, STND.INSTR.3, and STND.DRAFT; the signature provisions read against `govharness/ledger/signatures.py` and `register.py`; reading copy counted with `wc -w` |

## Result

Reading copy: 2,269 words before, 1,585 after (30.1% fewer). Revision stays 0.7. Provisions: 27 before, 25 after.

| New | Title | Was |
| --- | --- | --- |
| 1 | Item retrieval | 1 |
| 2 | Topic retrieval | 2 |
| 3 | Whole text | 3 |
| 4 | Item files | 4, 5 |
| 5 | Files read as items | 6 |
| 6 | Ledger file | 7 |
| 7 | Transaction fields | 8, 9 |
| 8 | Chain integrity | 10 |
| 9 | Content pin | 11 |
| 10 | Signer register form | 12 |
| 11 | Signature acceptance | 13 |
| 12 | Look-alike actors | 14 |
| 13 | Register chain | 15 |
| 14 | Manifest form | 16 |
| 15 | Stale content | 17 |
| 16 | Stable check keys | 18 |
| 17 | Failure status | 19 |
| 18 | Environment outcomes | 20 |
| 19 | Coverage report | 21 |
| 20 | Configuration entry | 22 |
| 21 | Installed configuration | 23 |
| 22 | Unattended referral | 24 |
| 23 | Configuration failure | 25 |
| 24 | Rehearsal before application | 26 |
| 25 | Rehearsal isolation | 27 |

Sections: Corpus (1 to 5), Ledger (6 to 13), Checks (14 to 17), Environment (18 to 23), Rehearsal (24 and 25). `RANKS` follows; l.3 confirms it. Code, tests, README.md, and pointer.md are renumbered. Records and earlier drafts keep their numbers (PRIME.5).

## Findings

Severity: Medium means the text and the code disagree on a FAIL, or text restates a higher provision. Low means excess words or an inexact statement.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | Register chain (0.7: 15) did not state a FAIL that `check_signatures` reports: a signer register with no governance-ledger transaction that founds it | Fixed in 13: "Where the signer register exists without such a transaction, or the keys it leaves open differ from the last one's "signers"" |
| 2 | Medium | Signer register form (0.7: 12) omitted two rules that `read_register` enforces as register problems, which fail the ledger check: a signer row for "all" has Last entry "none", and a requirement row for "all" has From entry "1". The harness failed a register that the text allowed | Fixed in 10, second sentence |
| 3 | Medium | Text restating LVL0 or another standard. Purpose: "It holds no authority, and no work depends on it; without one, an actor reads the corpus and checks by hand" (GOV.38) and "Every provision is binding, because each instantiates a floor obligation" (GOV.10, STND.DRAFT.25). The section Normative and informative parts restated STND.DRAFT.6, and the Terms lead sentence restated the Lexicon preface. Notes: "A configuration displaces a provision of STND.DFLT only as STND.DFLT.22 states" restated STND.DFLT.22 | Removed. Purpose is now one sentence |
| 4 | Low | Terms not needed. Adapter was used once; 19 now binds the harness for each derived configuration. Broken chain was used once and is inlined in 8. Refuse is plain English and is already used as a verb in 22 and 23. Operative was listed as a STND.DFLT term but no provision used it | Removed |
| 5 | Low | Provisions used session (0.7: 24) and destructive action (0.7: table of 20) without saying they carry the STND.DFLT meanings | Added to the Notes list |
| 6 | Low | The transaction-type table glossed self-evident names in 16 rows. The field table spent a Required column on 13 rows of "Always" | Types are listed in the "type" field of 7, and the table is now one sentence. Only "signers" and "ledger" state their condition. The meaning of configure is carried by 20 ("A "configure" entry that a harness drafts for STND.DFLT.22") |
| 7 | Low | The field list in prose put the numerals "1" and "8601" in a provision sentence (g.14) | "from one", and the term Timestamp holds "ISO 8601" |
| 8 | Low | Notes that a reader does not need: the README mapping, the only adapter (decision record 0002), and the blank actor of entries 1 to 18, which ledger entry 19 already records | Removed. The anchor default, the code's later acceptance of configure, and the transition note on the scripts (GOV.42) are kept |
| 9 | Low | Wording: 23's "whose program" (draft) misread as the action's own program; 20's "the digest of each installed file and each checkpoint mechanism" read as a digest of a mechanism; 12's "is non-ASCII" read as wholly non-ASCII | Kept or restored as "a program it runs", "each installed file with its digest", "holds a non-ASCII character" |
| 10 | Low | Item retrieval: the code also lists documents and sections that cite an item. A broader text would also cover revision-history rows (review 0006, finding 10) | Kept the 0.7 floor: each provision, term, knowledge entry, and tag that cites it |
| 11 | Low | README step 7 still said "as the 1.2 proposal amends them", but STND.DFLT 1.2 is adopted (entry 42) | Now reads "revision 1.2" |
| 12 | Low | Open. Configuration failure (23) refuses an action when a program the configuration runs fails, for assured work. The Claude Code guard runs with a 10 s timeout, and a timeout lets the call proceed at every class. The coverage report states this as a condition (19), but 23 has no exception | Not changed. Custodian to choose: state the exception in 23, or treat a timeout as a gap that 19 reports |
| 13 | Low | Open. STND.CLASS, STND.DFLT, STND.DRAFT, STND.IDENT, and STND.INSTR keep the section Normative and informative parts and the Terms lead sentence. STND.HARN no longer does, so the documents now have different layouts | Custodian to choose: remove them from the siblings at their next amendment, or restore them here (adds 30 words) |

## Merges and atomicity

- **4 Item files** merges Item paths and Item format. It has one subject, the file of an item, and two SHALLs that are always applied together when an item is written. `checked_by` is `ids` and `review`.
- **7 Transaction fields** takes in Transaction types: the type is the content of one field.
- Not merged: 8 and 9 (different checks), 19 and 21 (one reports coverage, the other installed state), 24 and 25 (one binds an actor, the other a harness).

## Code agreement (signatures)

- **11 Signature acceptance** reports FAIL where a transaction is signed or required and lacks an accepted signature. `_entry_failures` fails a signature that does not verify, a verified key that `_valid_for` rejects, and a required row (`applies`, Actor, From entry not above `seq`) with no valid key. Its `fpr` is set exactly when the signature is accepted, so the two agree. A signed entry with no register fails both in the code ("no signer register") and in the text (no row can accept the signature).
- **12 Look-alike actors** matches `not actor.isascii() or _spoofed(...)`, where the labels are the signer Role labels and the required Actors, each NFKC-normalized, stripped, and case-folded. The code runs it only when a register exists.
- **13 Register chain** matches `_register_change`. The founding transaction must be signed by the anchor key and each later one by a key in the previous "signers", where the key is one that verifiably signed and may sign (`fpr`). After the loop, a missing founding transaction fails (finding 1), and so do open signers that differ from the last list.

## Results

| Check | Result |
| --- | --- |
| `check governance --no-z3` | exit 0; 54 PASS, no FAIL or WARN; no STND.HARN finding in `logic_report.md` or `drafting_punch_list.md` (punch list 87 lines, as before). STND.HARN.8 appears only in the c.1 classification table (PASS), as 0.7's 10 and 18 did |
| `verify governance` | all PASS; ledger 42 entries |
| `manifests --check`, `references --check`, `compose --check` | stale: 0; PASS |
| unit tests | 123 tests, OK |
| `ruff check --select E,F,W,I,UP --line-length 79 govharness tests tools` | clean |

## Verdict

Accepted for presentation to the custodian as STND.HARN 0.7. Every obligation the custodian kept is still stated, except where it only restated a higher text (finding 3). Findings 1 and 2 bring the text in line with the code. Findings 12 and 13 are left for the custodian to decide.
