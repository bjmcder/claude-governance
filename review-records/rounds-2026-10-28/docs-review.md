# Cold review of the documentation update after ledger entry 322

Reviewer: an agent of another configuration from the author (Claude Fable 5.1), 2026-10-28. Scope: the uncommitted changes to `docs/`, `for-agents/`, `harness/README.md`, `harness/skills/`, and `OPEN-ITEMS.md` on branch `rounds-2026-10-28`. `harness/tests/` was left to the other agent. No file of the repository was edited other than this report.

## What was run

- `git diff -- docs for-agents harness/README.md harness/skills OPEN-ITEMS.md`, read whole.
- `python3 -B -m govharness show governance ID` for every provision the changed text cites: STND.CLASS.1, .3, .5, .7, .10, .18 to .23; QA.7, .8, .10, .11, .12; GOV.3, .10, .11, .13, .14, .19, .20, .22, .24, .47, .50; PRIME.6, .7, .11, .13, .14; GUARD.6, .10, .14; INTPR.12; AGENT.15; STND.INSTR.6, .11; STND.PROJ.1 to .3; STND.DEPS.14; STND.HARN.6, .7, .24, .28, .32; STND.CODE.17 to .20; STND.DFLT.1, .2, .5, .6, .9, .12, .13, .16, .17, .20, .21, .23 to .25, .28, .29, .32 to .35; STND.DRAFT.33; the terms Working bounds, Assured work, and Tool memory store of STND.DFLT, the term Team and the Notes of STND.CLASS, the Notes of STND.DFLT, and the section Representation in the harness of STND.DRAFT; ledger entry 204.
- A search of `rendered/` for a term Expected class: none exists in LEX or elsewhere; the words occur only in the title of STND.CLASS.21 and the revision row of LVL0.
- Every identifier cited in the changed files checked for a file in `harness/governance/` (all exist); every withdrawn identifier of the `withdrawn` front-matter fields grepped in the docs, the skills, the READMEs, `for-agents/`, and `OPEN-ITEMS.md` (none cited); "202", "ledger-202", and "entry 202" grepped (none left).
- The targets of entries 203 to 322 intersected with the identifiers the docs cite (GOV.11, GOV.13, GOV.24, PRIME.7, QA.11, and the amended standards), and each such citation re-read against the current text.
- `govharness onset --help`, `pairs --help`, `ledger append --help`: `onset [root] CSQn`, `pairs [--amends ...] [--with ...] [root] ID`, and the `ledger append` options the docs show all exist; `root` defaults to `$GOVHARNESS_ROOT`. `core/onset.py`, `checks/fields.py` (`checked_by`, `onsets_valid`), `cli/query.py` (`run_onset`), and `cited_tables` and `MENTION_COLUMNS` in `checks/drafting/tables.py` exist. `harness/rendered/` holds six files; `harness/records/units/` holds 0023-onset.md and 0024-review-pairs.md; `harness/skills/` holds three skills. Tracked files under `harness/` total 4.1 MB, the repository 20 MB.
- `govharness verify governance`: every check PASS, with the one g.18 warning.
- Skill front matter: `name` 15 to 23 characters, `description` 423 to 476 characters, within the limits of 64 and 1024.
- A scan of the changed files for British spellings and for the forms of the STND.DOCS.9 table: nothing found.

The table "What the human is asked to do, by class" was derived cell by cell from STND.CLASS.18, STND.CLASS.19, STND.CLASS.10, QA.11, GOV.50, PRIME.6, PRIME.7, STND.CLASS.3, STND.CLASS.7, and STND.DFLT.20 and .23. Every review and audit cell agrees with its row. The "Known limitations" item is a real gap: QA.11 makes the adopted classification the promotion of each result of CSQ3 or CSQ4 work that meets its acceptance criteria, GOV.20 gives a constitution to every project that promotes a result, and the Notes of STND.DFLT (line 52 of `rendered/STND.DFLT.md`) still describe work without a constitution as relied upon by no one beyond its author. No Note of STND.CLASS, QA, GOV, or STND.PROJ reads GOV.20 otherwise.

## Defects

1. `docs/adoption.md:39`: "(the term Expected class of the Lexicon)". No such term exists; GOV.13 defines the expected class, its adoption with the classification, and that it sets no class before the use begins. Fix: replace the parenthesis with "(GOV.13)".

2. `docs/adoption.md:84`, CSQ2 cell "Further acts": "The release decision (QA.10)" is listed as an act that CSQ2 adds. QA.10 and GOV.50 make the release decision the human owner's at every class, and line 74 already lists "the decision to release or deploy" among the acts at every class, so the page contradicts itself. Fix: delete "The release decision (QA.10)" from the CSQ2 cell.

## Should-fix

3. `docs/adoption.md:96` ("Read together, these give every classified project a constitution") and `OPEN-ITEMS.md:7` ("so GOV.20 asks a constitution of every classified project"). GOV.20 is reached only through QA.11's standing promotion, which covers work of CSQ3 or CSQ4 that has a result meeting its acceptance criteria; a project of CSQ2 or a more severe class that promotes nothing is not reached. Fix, adoption.md: "Read together, these give a constitution to every project of CSQ3 or CSQ4 whose work has a result that meets its acceptance criteria, while ...". Fix, OPEN-ITEMS.md heading: "A classification at CSQ3 or CSQ4 is a promotion, so GOV.20 asks a constitution of every project of those classes with a result that meets its acceptance criteria."

4. `docs/adoption.md:57`: step 4 restates STND.CLASS.22 nearly whole ("regenerating each result whose record lacks its inputs, labeling unverified ... Existing source takes up a default of form or style ..."). The direction is to cite, not restate. Fix: "Before the work is relied upon at the new class, bring the work done at the lower class up to it (GOV.14). STND.CLASS.22 lists the steps, from regenerating each result whose record lacks an input to the audit of STND.CLASS.19 and the repeat of each check tied to an earlier event, and says when existing source takes up a default of form or style."

5. `docs/adoption.md:34`: the last two sentences restate the term Working bounds ("By default the working bounds take in ... run a program without a request"). Fix: replace them with "The term Working bounds of STND.DFLT states what the bounds take in by default and what they leave out for writing."

6. `docs/adoption.md:66`: "so none of them needs a ledger line written by hand" contradicts the CSQ1 cell at line 85, where assured work has you append entries yourself. Fix: "so, until the work is assured, none of them needs a ledger line written by hand."

7. `docs/adoption.md:33`: "are the run's list of affected items (STND.DFLT.24)". The provision that makes those locations the list is STND.DFLT.34; STND.DFLT.24 only asks for a list. Fix: cite "(STND.DFLT.34)".

8. `docs/adoption.md:35`: "STND.PROJ.3 proposes the standing authorizations in its section Authorizations". STND.PROJ.3 has the agent that drafts the constitution propose them. Fix: "For a project with a constitution, the agent that drafts it proposes the standing authorizations of the table of STND.PROJ.3 in the section Authorizations."

## Optional

9. `docs/adoption.md:83`, CSQ3 cell: "through work verified before reliance" is the reliance test of STND.CLASS.1; QA.11 says "feeding work that is verified later". Cite both: "(STND.CLASS.1, QA.11)".

10. `docs/adoption.md:70`: the operating-cost bullet cites STND.DFLT.33 without "under the defaults", where lines 72 and 76 say it for the other STND.DFLT acts. Fix: begin the bullet "under the defaults, directing the work: ...".

11. `docs/adoption.md:43`: STND.CLASS.21 lets the work omit each record that only the expected class requires "other than the records of STND.CLASS.23"; the bullet drops the exception, which the next bullet then states. Fix: append ", other than the records of the next point" before "(STND.CLASS.21)".

12. `docs/adoption.md:88`: the paragraph on STND.DEPS.14 stands under the class table with no tie to it. Fix: move it to the end of step 6, which is where settings outside the working bounds are introduced.

13. `docs/installation.md:68`: "about 19 MB"; the tracked files total 20 MB. Fix: "about 20 MB".

14. `docs/custodian-guide.md:54` names the g.18 warning on STND.DRAFT.35, .39, and .42 and a six-minute test run. `verify` still reports one g.18 warning; the provisions and the duration were not re-checked here, since the tests were in another agent's hands.
