# Round of 2026-10-28 on the reach of GOV.20: decisions and drafting

Round c of 2026-10-28 (LVL0 1.7, ledger entry 224) gave QA.11 the sentence "For work of CSQ3 or CSQ4, the adopted classification is the promotion of each result that meets its acceptance criteria (QA.1), for reliance by its author or immediate team alone, feeding work that is verified later (GOV.12)." GOV.20 reads "Every project that promotes a result, releases software, or drives physical hardware has a project constitution". Read together, the two give a project constitution to every project of CSQ3 or CSQ4 with a result that meets its acceptance criteria, although rulings C1 to C8 lowered the ceremony of work at those classes and added none. The Notes of STND.DFLT kept the earlier reach: "work without a project constitution is relied upon by no one beyond its author (GOV.20)". The item is in `OPEN-ITEMS.md`, "Corpus, for a later round", and in `docs/adoption.md`, "Known limitations".

## The ruling

The lead put the recommendation to the custodian in the conversation of 2026-10-28, after the documentation update at commit 15c9a06:

> My recommendation is to have GOV.20 apply only to promotions beyond the one QA.11 makes at classification. A `rule` reading it that way would do the same. It is recorded in `OPEN-ITEMS.md` and stated in the docs' "Known limitations" until then.

The custodian, 2026-10-28, replied:

> i agree with the recommendation on the open items. proceed

The ruling is carried as an amendment of GOV.20, not as a `rule` under GOV.3, so that the text itself restores the reach GOV.20 had before round c. A project has a constitution where it promotes a result other than through the adopted classification of QA.11, releases software, or drives physical hardware.

## Drafted, for ratification

`tools/amendment-scripts/apply_constitution_round_2026_10_28.py`. It makes two transactions, one per document, in citation order, which are entries 323 and 324 in rehearsal. `AT` is the time of application, taken when the module loads. Transaction k takes `AT` plus k seconds, and each revision row is dated by its own transaction.

### LVL0 1.8 (minor, GOV.40; targets LVL0 and GOV.20)

GOV.20, new text (cites `["QA.11", "PRIME.15"]`):

> Every project that promotes a result other than through its adopted classification (QA.11), releases software, or drives physical hardware has a project constitution: a LVL3 instrument that inherits from and aligns with the levels above it, cites the provisions it instantiates, adds only project-specific obligations, and relaxes none (PRIME.15).

Only the first clause changes. The title, "Project constitution", is unchanged. The revision row is "Minor amendment (GOV.40): GOV.20 gives a project constitution to every project that promotes a result other than through its adopted classification, releases software, or drives physical hardware, so that the adopted classification, which QA.11 makes the promotion of each result of work of CSQ3 or CSQ4 that meets its acceptance criteria, asks no project constitution."

The rationale follows the LVL0 entries 224 and 289. It states the provision, the change, the reason, the alternatives weighed, and the lower governance affected (GOV.40), and the class under STND.IDENT.3. The class is minor because the reach of an obligation changes. The rationale also quotes the ruling, gives the floor argument and the transition, and closes, as does the rationale of STND.DFLT, with "Proposal: the recommendation of 2026-10-28 quoted in review-records/round-2026-10-28-constitution/decisions.md, on the item of OPEN-ITEMS.md, "Corpus, for a later round"."

Three alternatives were weighed and rejected:

- A `rule` under GOV.3. Under GOV.9 the more restrictive reading of the text would keep governing every reader who had not seen the ruling.
- Withdrawing the sentence of QA.11. This would undo rulings C1 and C5.
- Keying GOV.20 to the class. A class does not decide whether a project releases software or drives hardware.

### STND.DFLT 1.6.1 (editorial, GOV.41)

The Note, new text:

> No class is set by default (GOV.13), so the rows of STND.CLASS.18 and STND.CLASS.19 have no occasion to act until the human owner records one. A project without a project constitution promotes a result only through its adopted classification (GOV.20), so its work is relied upon beyond its author only as QA.11 admits for work of CSQ3 or CSQ4.

The change is editorial because only the Notes change. The Note cites QA.11 for the extent of the reliance and does not restate it (GOV.31). Transition (GOV.42): none.

### Other text that the change might have made false

A grep of `harness/governance/` for "GOV.20", "constitution", and "beyond its author" found nothing else to change:

- The Lexicon terms Project and Project constitution, STND.PROJ (its Purpose and STND.PROJ.1), the template `_PROJECT/NAME/_doc.md`, and the Notes of STND.INSTR all cite GOV.20 for what a constitution is and holds. That is unchanged.
- GOV.22, and the Notes of STND.THRT and STND.WPROC, speak of work without a constitution and stay true.
- The Note of STND.CLASS on promotion, the CSQ4 entry of GOV.12, the term Reported result, and the row "reported, released, deployed" of Normative Language stay true. Each states the reliance that QA.11 admits.

Outside the corpus, the lead makes these changes after application (standing process, step 8):

- `docs/adoption.md`: "Known limitations" and its pointer in step 2 are removed, and step 5 ("Write a project constitution if the project now promotes results, releases software, or drives hardware (GOV.20)") is reworded to "promotes a result other than through its adopted classification";
- `OPEN-ITEMS.md`: the item is removed;
- the reading copies `rendered/GOV.md`, `rendered/LVL0.md`, `rendered/STND.DFLT.md`, and `harness/rendered/defaults.md` are rebuilt.

## Floor argument (GOV.11)

The change narrows a LVL0 obligation of the floor. It does so on the custodian's ruling under GOV.40, which GOV.11 does not bar, since GOV.11 bars lower governance from raising the floor. Three kinds of project still have a project constitution, as at ledger entry 202:

- a project that promotes a result by its human owner's recorded act;
- a project that releases software;
- a project that drives physical hardware.

The classification admits only the reliance that QA.11 and the CSQ3 test of GOV.12 bound: by the author or the immediate team alone, feeding work verified later. Work without a constitution meets those obligations under the defaults (GOV.22), which provide every mechanism of GOV.21. This is the reduced ceremony that rulings C1 to C8 intended. At entry 202, that reliance needed a promotion of its own, and so a constitution. Now it needs neither. That difference is the purpose of the ruling.

The prime directives, and every other provision of the floor, are unchanged. No obligation is added to work at any class, so no floor is raised.

## Transition (GOV.42)

None. No lower provision needs to conform. A project constitution adopted under LVL0 1.7 or 1.7.1 stays in force. Whether to keep it is its human owner's decision (GOV.41), and no provision asks for one.

## For the custodian at ratification

1. **Wording of the exception.** "Promotes a result other than through its adopted classification (QA.11)" names the act and cites QA.11. It does not repeat the classes. The alternative is "other than through the adopted classification of work of CSQ3 or CSQ4 (QA.11)", which states the classes in GOV.20 as well. Recommendation: the wording as drafted. QA.11 alone fixes the classes at which a classification promotes, and naming them twice would put the same rule in two places (GOV.31).
2. **The order of the list.** The drafted list keeps the order of GOV.20 and of the ruling, so the qualified item comes first. The qualifier cannot attach to the other two items, since neither is done through a classification, and GOV.9 gives a GOV provision its more restrictive reading. The alternative is to move the qualified item last. Recommendation: keep the order, which is the smaller change.

## Left to a later round

The "releases software" limb of GOV.20 (item 7 of `review.md`). Under STND.WPROC.12, a main line advances only on a recorded decision of the human owner to release, and STND.WPROC's defaults apply to work without a constitution. A project of CSQ3 under STND.WPROC therefore releases software at its first main-line advance, and so has a constitution under the second limb of GOV.20. That is the reach at entry 202, outside the ruling, and this round drafts nothing on it. The lead adds to `OPEN-ITEMS.md` the question whether "releases software" means a release beyond the project or every advance of a main line.

## Review

`review.md` is a cold review by an agent of another configuration. It found that the new GOV.20 carries the ruling exactly, and that its pair review found no conflict.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | The LVL0 rationale says the custodian "directed an amendment" | Fixed as proposed: the reason is GOV.9 alone, here and in the script. The recommendation is quoted whole under "The ruling" |
| 2 | The floor argument of the LVL0 rationale claims the reach "as at entry 202" | Fixed as proposed: the rationale states that a CSQ3 or CSQ4 project relied upon only as QA.11 admits has no constitution, where at entry 202 it needed one, and that GOV.11 does not bar the custodian's narrowing |
| 3 | Not every change outside the corpus is listed | Fixed: listed above; the lead makes them after application |
| 4 | The Note gives a classification to work and has work promote | Fixed as proposed, in the module, the row, the rationale, and this record |
| 5 | The record does not say where the recommendation was made | Fixed: quoted whole under "The ruling"; both rationales close with the proposed "Proposal: …" sentence |
| 6 | The reason given for reading 2 | Taken as proposed |
| 7 | The "releases software" limb | Left to a later round, as above |
| 8 | The self-check omits two rules | Taken as proposed |

## Checks

- **Self-check of the drafting rules.**
  - GOV.20 has no modal. Its title has two words.
  - Its body identifiers are QA.11 and PRIME.15, which equal `cites`.
  - It uses "Every", which is not a word of STND.DRAFT.17. Its one condition, the relative clause, precedes the main clause, as before.
  - It uses no expression of STND.DRAFT.7, no qualifier of STND.DRAFT.13, no word of STND.DRAFT.17, and neither "such as" nor "for example".
  - The Note states no obligation in the indicative. It cites the provisions it reads.
- **Rehearsal.** `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_constitution_round_2026_10_28.py` appended 2 entries, 323 and 324. Every check passes: ids, mnemonics, references, manifests, ledger, unpinned, templates, status, checked-by, onset, and logic. The only warning is the g.18 warning that the corpus already carries.
- **Kept copy** (`/tmp/claude-1000/gov20/kept/governance`):
  - `references --check`: PASS.
  - `compose --check`, with `rendered/` beside the copy: only `rendered/defaults.md` is stale. This is expected, since the reading copies are rebuilt after application.
  - `findings.py`: identical to the live corpus (249 findings). There is no finding on GOV.20 or LVL0. The three on STND.DFLT (STND.DFLT.8, STND.DFLT.30, and the role word `manager`) are already in the live corpus.

### Pairs (STND.HARN.28)

| Command | Pairs listed | Verdict |
| --- | --- | --- |
| `pairs <copy> LVL0 --amends GOV.20` | none ("no pair to review before a change of LVL0"). STND.PROJ.1 is the one provision that instantiates GOV.20, so it pairs with nothing | none |
| `pairs <copy> STND.DFLT` | none. Only the Notes change | none |
| `pairs <copy> LVL0 --amends GOV.20 --with STND.DFLT` | none | none |

The one provision that instantiates GOV.20 was also read by hand, since `pairs` listed nothing. STND.PROJ.1 fixes the sections of a constitution once a project has one, and it is consistent with the narrower reach: none.

### Test suite

The suite was run on a detached worktree of the branch at 5275278, with this round applied to its `harness/governance`. It ran 230 tests in 366 s, with 2 failures and no errors. Both failures are in `tests/derive/test_reading_copy.py`:

- `test_rendered_copies_are_current` reports `harness/rendered/defaults.md` as stale.
- `test_repository_rendered_copies_are_current` reports `rendered/GOV.md`, `rendered/LVL0.md`, and `rendered/STND.DFLT.md` as stale.

These tests check that the reading copies are current, and the copies are rebuilt only after application (standing process, step 8). Neither test pins text that this round changes. After `compose governance --write` and `compose governance --all ../rendered` in the worktree, the module's 10 tests pass. No test was changed. When the round is applied, the rebuild of the reading copies regenerates those four files.
