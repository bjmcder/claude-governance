# Dispositions of reviews A and B, round of 2026-10-26

Every finding of `review-a.md` and `review-b.md`, and what the scripts now do about it. After the fixes, the rehearsal of `apply_round_2026_10_26.py` appends entries 176 to 182, every check passes with the two warnings the corpus already carries, the source is unchanged, and the drafting findings differ from the live corpus only by the two g.8 review findings on the withdrawn STND.HARN.29.

## Review A (STND.HARN, STND.DFLT, STND.PROJ, HW.GPU, HW.QPU)

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | STND.HARN.31 reads as "no scope names any file" | Fixed: "Where a ".md" file of the corpus is reached by no "scope" of a governance-ledger transaction, a harness SHALL report FAIL for that file (GOV.36)." |
| 2 | Pin in force: "its paths" ambiguous | Fixed: "...no later governance-ledger transaction has a "scope" that reaches each path of the earlier "scope"." |
| 3 | Content hash counts a file twice when two paths of one scope reach it | Fixed in the term: "one for each ".md" file that a "scope" reaches ... ordered by the first path of the "scope" that reaches the file". The code follows (draft-status, owed item 1) |
| 4 | One relation phrased three ways | Fixed: new term Reach ("A "scope" reaches a path where one of its paths is that path or a directory above it"), used by the Content hash, Pin in force, STND.HARN.31, and the Notes |
| 5 | Notes on pins overstate, and omit overlapping scopes | Fixed with the reviewer's wording, and the sentence on two scopes that share a path |
| 6 | Notes omit STND.HARN.31's reach of README.md and template directories | Fixed: sentence added, with the reason that the ledger pins files, not items |
| 7 | No transition for STND.HARN.31 in the revision row | Fixed: the row's transition says a file that no scope reaches is no defect until the five pin transactions are recorded; the rationale says why they follow |
| 8 | HW.GPU, HW.QPU sentence states an obligation in the indicative | Fixed with the reviewer's wording |
| 9 | STND.PROJ Notes: "in every case", "every reader decides alike" | Fixed with the reviewer's wording |
| 10 | STND.HARN.32: circular key wording; "Registered" suggests a register | Wording fixed ("a key of a check that the harness makes"); title now "Known check keys", since Register is a Lexicon term. The basis stays GOV.38: an unknown key is the harness claiming a check it does not make |
| 11 | "The code accepts type configure on adoption" | Fixed: "A transaction of type configure records a configuration for STND.DFLT.22." |
| Q | Decision 4 said one transaction first; decision 6 said no change of text | For the custodian at ratification (below) |

## Review B (STND.DRAFT, STND.IDENT)

| # | Finding | Disposition |
| --- | --- | --- |
| D1 | Cited document: the exclusions contradict the corpus, since they apply in the code to bare names only | Fixed: the exclusions apply to a name by identifier alone; "the identifier LVL0 alone never counts" |
| D2 | "a column headed Example" against the code, which drops the whole table | Fixed: "a table with a column headed Example" |
| S1 | "alone or in parentheses" misleads | Fixed: "named in their text by its identifier alone"; the section Checks says "the document's identifier written alone in parentheses" |
| S2 | L9 wording ambiguous where a check enforces provisions of both modes | Fixed with the reading of the harness: "a binding provision of this standard names the check in its field `checked_by`"; for the custodian (below) |
| S3 | Floor arguments missing for the widened term and STND.IDENT.24 | Fixed: both rationales carry an argument, put to the custodian at ratification |
| S4 | "full stop" not American; the term omits ends of list items and table cells | Fixed: "a period, a question mark, or an exclamation point, or at the end of a paragraph, a list item, or a table cell". The remaining differences of the code (a period before a lowercase letter or a backtick; splits at semicolons and colons) are owed item 8 |
| S5 | STND.DRAFT.3 "entries are expressions" undecidable | Fixed: "Outside a column whose entries are modals or excluded expressions" |
| S6 | Checks, v.8 description incomplete | Fixed with the reviewer's wording |
| S7 | v.8 verifies STND.DRAFT.22 only in part | The rationale says so; `checked_by` keeps l.1 and v.8 |
| O1 | STND.IDENT.12 also exempts a planned document | The row and rationale say "a draft or a planned document" |
| O2 | STND.IDENT.24 "its parts" | Fixed: "a part named in its field `parts`" |

## Verification (`verify.md`)

| # | Finding | Disposition |
| --- | --- | --- |
| D1 | The term Cited document and the section Checks disagree on what a bare name needs | Put to the custodian on 2026-10-26, who chose that a row suffices (decision 1, as clarified). The section Checks now says that the command derives the row of a document named by its identifier alone and that g.25 fails where the table lacks it; the rationale says the harness asked for a citation until now. The code follows (draft-status, owed item 9) |
| S1 | Content hash: "first" in what order | Fixed: "ordered by the first, in code-point order, of the paths of the "scope" that reach the file" |
| S2 | Entry 53's transition also names STND.HARN.23 | Not changed: entry 53 names STND.HARN.23 in its account of the change, and its transition clause covers only STND.HARN.26 to .28 and STND.HARN.18 |
| S3 | "neither reaching the other" applies Reach to a scope | Fixed: "neither reaching each path of the other" |
| S4 | STND.HARN.32 fails on its own key until the code exists | The code lands before the round is applied (draft-status, Order of application), so no transition is needed |
| O1 | OPEN-ITEMS line on what is drafted | Corrected when the items close |
| O3 | "put to the custodian at ratification" reads stale once recorded | Fixed: removed from the rationales of STND.HARN, STND.DRAFT, and STND.IDENT; the arguments stay |
| O2, O4 | Reach beside STND.DFLT.25; the basis GOV.38 | No change; the basis is in the questions below |

## Reconciliation (`reconciliation.md`)

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | The term and the section Checks make a loop | As verification D1 |
| S2 | The STND.HARN row omits the changed Content hash | Fixed in the row |
| S3 | Rationales say both "ratified" and "put to the custodian at ratification" | As verification O3 |
| S4 | The STND.IDENT row omits the change of its section Checks | Fixed in the row |
| S5 | Rows 176 to 179 say "STND.HARN 1.4 withdraws" before entry 180 | Not changed: the round is applied as one, and an entry number in a row would be wrong if another entry came first |
| O1, O2 | Reach in STND.HARN.7 and .13; the first sentence on pins | No change: outside the round's scope, and explanation only |
| O3 | Content hash order | As verification S1 |
| O4 | STND.DFLT.22 unchanged | The STND.DFLT rationale says so |

## Second verification (`verify-2.md`)

No defect. Every row above and every answer of `decisions.md` reads as stated.

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | The floor argument of STND.HARN.31 overstates for the custodians | Fixed with the reviewer's wording: of the custodians only the transactions that pin the files now outside every scope |
| S2 | The STND.DRAFT floor argument: "beyond that row" | Fixed: "no new act of a project, because the command references writes the row" |
| S3 | The STND.HARN row: "first of its paths" | Fixed: "the first, in code-point order, of its paths that reach it" |
| O1 | The STND.HARN rationale: "no two scopes overlap" | Fixed with the reviewer's wording |
| O2 | The STND.DRAFT section Checks restates the term | Fixed with the reviewer's wording |

## Ratification

The custodian ratified the round on 2026-10-26, on condition of a second cold verification with no defect (`decisions.md`, answer 7), which `verify-2.md` gives.

## For the custodian at ratification

1. **Decision 4.** It said one transaction first pins the five paths. The draft records five transactions, each with its own scope, after STND.HARN 1.4: a file can be a scope only once STND.HARN.7 says so, and one transaction over five paths would tie them to one content hash, so that every later change of one would need a transaction over all five. The revision row records a transition for the files until then.
2. **Decision 6.** It said one transaction with no change of text. The draft records the end of the transition of entry 53 in the revision row of STND.HARN 1.4, which is a transaction, and the end then stands in the document's own history. A separate annotate transaction is the alternative.
3. **The section Checks of STND.DRAFT (L9).** The draft takes the harness's reading: a finding in another document fails where a binding provision of STND.DRAFT names the check. The other reading would fail a finding only where the provision in which it stands is binding.
4. **Floor arguments** of STND.HARN.31, STND.HARN.32, STND.IDENT.24, and the widened term Cited document, in the Notes and rationales.
5. **The basis of STND.HARN.32.** GOV.38 (a harness implements governance and holds no authority of its own), since an unknown key is the harness claiming a check it does not make. GOV.37, the basis of STND.HARN.16, is the alternative the reviewers named.
6. **Pinning before STND.HARN 1.4.** `KNOW`, `TAG`, and `_PROJECT` are directories and could be pinned before STND.HARN 1.4, as decision 4 first said; only `STND/_doc.md` and `README.md` need STND.HARN.7 to admit a file. The draft pins all five after, with one transition, so that the five follow one rule.
7. **The field `last_provision` (unit 0017, H1).** Left out of the round, because it means a transaction for every document (draft-status). Leave it to a later round, or drop it.
8. **The five pin transactions** are scripted and rehearsed in this round, at its end with the code, and applied right after the seven amendments.
