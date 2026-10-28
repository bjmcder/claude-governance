# Round of 2026-10-28 on the reach of GOV.20: cold verification

Reviewer of `review.md`, checking the fixes of commit db78dc4 on a fresh copy at `/tmp/claude-1000/rvg20b/governance`.

## What I ran

`rehearse governance ../tools/amendment-scripts/apply_constitution_round_2026_10_28.py`: appended 323 and 324, every check PASS, logic PASS with the standing g.18 warning, source unchanged. The module applied to the fresh copy: `verify` all PASS; `references --check` PASS; `show GOV.20` prints the drafted sentence unchanged from the draft, with `cites` QA.11 and PRIME.15; `show STND.DFLT#notes` and the file both carry the new Note. The diff 12acab5..db78dc4 touches only the script, `decisions.md`, and `review.md`. Entries 323 and 324 were read whole from the copy's ledger.

## Dispositions

| # | Finding | Current text | Verdict |
| --- | --- | --- | --- |
| 1 | "the custodian directed an amendment" | Entry 323: "a ruling under GOV.3 that reads GOV.20 so without a text change (rejected: under GOV.9 the more restrictive reading of the text would keep governing every reader who has not seen the ruling)"; "directed an amendment" is absent from both entries. `decisions.md`, "The ruling", quotes the recommendation whole ("My recommendation is to have GOV.20 apply only to promotions beyond the one QA.11 makes at classification. A `rule` reading it that way would do the same. ..."), which names no instrument, so the record now claims nothing the ruling does not contain | closed |
| 2 | Floor argument claimed the reach "as at entry 202" | Entry 323: "Floor (GOV.11): the change narrows a LVL0 obligation of the floor, on the custodian's ruling under GOV.40, which GOV.11 does not bar, since GOV.11 bars lower governance from raising the floor; a project that promotes a result by its human owner's recorded act, releases software, or drives physical hardware has a project constitution, as at ledger entry 202, and a project of CSQ3 or CSQ4 whose results are relied upon only as QA.11 admits has none, where at entry 202 that reliance needed a promotion by recorded act and so a constitution; ..." `decisions.md`, "Floor argument", opens the same way | closed |
| 3 | Changes outside the corpus not all listed | `decisions.md`, "Other text ...": step 5 of `docs/adoption.md` reworded to "promotes a result other than through its adopted classification"; "Known limitations" and its step-2 pointer removed; the `OPEN-ITEMS.md` item removed; `rendered/GOV.md`, `rendered/LVL0.md`, `rendered/STND.DFLT.md`, and `harness/rendered/defaults.md` rebuilt | closed |
| 4 | The Note had work promoting through "its" classification | Copy, `STND/DFLT/_doc.md` line 62: "A project without a project constitution promotes a result only through its adopted classification (GOV.20), so its work is relied upon beyond its author only as QA.11 admits for work of CSQ3 or CSQ4." The row 1.6.1 and entry 324 read the same ("the Notes say that a project without a project constitution promotes a result only through its adopted classification, so that its work is relied upon beyond its author only as QA.11 admits ..., in place of saying that work without one is relied upon by no one beyond its author") | closed |
| 5 | Source of the recommendation unrecorded | `decisions.md`, "The ruling": "The lead put the recommendation to the custodian in the conversation of 2026-10-28, after the documentation update at commit 15c9a06", then the quotation. Entries 323 and 324 close with "Proposal: the recommendation of 2026-10-28 quoted in review-records/round-2026-10-28-constitution/decisions.md, on the item of OPEN-ITEMS.md, \"Corpus, for a later round\"." before the authorship sentence | closed |
| 6 | Reason for reading 2 | `decisions.md`, reading 2: "The qualifier cannot attach to the other two items, since neither is done through a classification, and GOV.9 gives a GOV provision its more restrictive reading." | closed |
| 7 | The "releases software" limb | "Left to a later round": nothing drafted; the lead adds the question to `OPEN-ITEMS.md` | as agreed, not for this round |
| 8 | Self-check omitted two rules | `decisions.md`, "Checks": "It uses \"Every\", which is not a word of STND.DRAFT.17. Its one condition, the relative clause, precedes the main clause, as before." | closed |

## New defects

None. The provision text, the revision rows, the scope, targets, and authorities of both transactions, and the citation order are as reviewed. The round is ready for ratification.
