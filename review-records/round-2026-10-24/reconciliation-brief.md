# Reconciliation review of the round of 2026-10-24: brief

Three reviewers each read the whole round on one dimension. Read REPO/tools/round-brief-2026-10-24.md (Common, Review agents) first. REPO is /home/brianm/projects/utils/governance-ledger109. Do not edit any file except your report; keep scratch files in your own new subdirectory of /tmp.

## The round

One script applies the round in ledger order: REPO/tools/amendment-scripts/apply_round_2026_10_24.py (entries 117 to 139 in rehearsal). Rehearse it from REPO/harness/ with `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24.py`; it prints the path of the rehearsed copy. Then compose any reading copy you need from that copy with `compose(read_corpus(root), read_ledger(root), ReadingCopy(id, name))` (imports: `govharness.derive.reading_copy`, `govharness.cli.derived.read_corpus`, `govharness.ledger.chain.read_ledger`), and run `python3 -B -m govharness verify <copy>` and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`.

What the round does:
- Amendments: STND.OMP 1.0.1 (cites STND.OFFLD), STND.CXX 1.1, STND.PY 1.0.1, STND.JL 1.1 (cite STND.CONC), NUMER 1.3 (the random-streams row of NUMER.2), STND.BUILD 1.0.1 (cites STND.WFLOW), STND.CONC 1.0.1 (cites STND.OMP, STND.OFFLD, STND.WFLOW, and the forms of its provisions in the new standards), STND.PROJ 1.2 and STND.HARN 1.2 (authorization format and STND.HARN.29; harness unit 0008, REPO/harness/records/units/0008-remote-write-authorizations.md).
- New standards with their mnemonics: STND.BUILD, STND.WFLOW, STND.STDC (C), STND.RUST, STND.FTN (Fortran), STND.SV (Verilog and SystemVerilog), STND.LEAN (Lean 4).
- Each document's review record is in REPO/review-records/round-2026-10-24/<topic>/ (build, wflow, c, rust, fortran, hdl, lean, amendments, harn-auth): the reviews, the verifications, and dispositions.md.
- The queue of cross-document items is REPO/review-records/round-2026-10-24/reconciliation-queue.md (R1 to R24). Every item must be closed, or stated as a decision for the custodian with a recommendation, at the end of this review.

## Reviewer A: alignment across documents

Check, across all new and amended documents: titles distinct across the corpus; mnemonics and their register rows (order, reasons, STND.IDENT.17 and .18); Terms defined once and imported elsewhere, with no clash (R12, R15: Foreign interface, Untrusted input, Restart state and checkpoint, Step and Workflow, Build, Reporting build, Soundness argument, Panic); no provision of one new standard restating another (overlaps among BUILD, WFLOW, and the language standards: R2, R3, R4, R13); each language standard's answer to the same question compared (R6, R16, R18, R22, R23): revision or edition in force, unsafe or unchecked operations, responses to listed failures and logging, ignored results, untrusted input and its reach, foreign interfaces, lock files and versions tested, checks in shipped builds, naming, random streams; STND.CONC's definition of a concurrent task not narrowed (R9); the STND.CONC 1.0.1 citations of the forms in the new standards correct and complete (R1); References complete (R11, by script: every document named in a document's text is in its References table). Write REPO/review-records/round-2026-10-24/reconciliation-alignment.md.

## Reviewer B: modes, floor, and class onsets

Check, across all new and amended documents: every binding provision listed, with the prime directive, GUARD, GOV, or floor provision it instantiates, and whether it asks more than that provision at the cost of wording or one record (GOV.11, GOV.19), compared with its counterparts in the other language standards; every class-onset paragraph against the table of STND.CLASS.10, read the same way in every document (R8), with each departure listed; no provision that blocks work where a tool or means is unavailable (R10); no owner decision that LVL0 does not assign (STND.DRAFT.42); no ruling attributed to the custodian that the custodian has not made; STND.VVUQ.63 naming a test battery (R19) and the order of output from concurrent tasks (R14): recommend. Write REPO/review-records/round-2026-10-24/reconciliation-floor.md.

## Reviewer C: records and integrity

Check: the full round rehearses and verifies; findings.py on every new and amended document shows no defect; each RATIONALE accurate against its document and its review record, ending with the corpus's tail (R24), citing no entry of this round by number, with the class of each amendment right under GOV.41; the mnemonic register rows in order; each review record complete (reviews, verifications, dispositions) and each blocking finding closed; the harness suite passes (`cd REPO/harness && python3 -B -m unittest discover -s tests`), and unit 0008's record, README, and decision records agree with the code; the items of REPO/HANDOFF.md "Open items" each closed by the round or stated as remaining, with the reason. Compile, from every dispositions.md and every drafter's and reviewer's report, the single numbered list of decisions for the custodian, each with its recommendation, removing duplicates. Write REPO/review-records/round-2026-10-24/reconciliation-records.md and REPO/review-records/round-2026-10-24/decisions-for-the-custodian.md.

## All reviewers

Rank findings Blocking (a broken rule, a factual error, a conflict, an open queue item with no closure) and Should-fix, each with the document, the provision, and the fix. Under 1,500 words. In your final message give the blocking items.
