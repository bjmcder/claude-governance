# Findings log, ledger entries 1 to 45

These findings were kept in the harness README until ledger entry 45, newest first. The ledger and the unit, review, and decision records hold the history that followed.

- STND.DRAFT 1.2.1 and STND.IDENT 1.3.2 (entries 44 and 45) name the
  package commands in their Checks sections, so the entry-point scripts in
  `tools/` are removed (DSGN.6; unit 0001 criterion 7).

- STND.DFLT 1.2 (entry 42) proportions assurance to class: signatures,
  confirmation by a verifier, and a configuration that displaces a
  provision apply only to assured work (CSQ0, CSQ1); for other work an
  unsigned owner entry or an agent's record of a grant is accepted, and a
  recorded configuration or checkpoint mechanism counts only while found
  installed in the session (Terms: Assured work, Operative).

- STND.DFLT 1.1 (entry 40) adds a fifth exempt class: a change or removal
  covered by a checkpoint whose mechanism and actions a signed entry
  records; the Terms define Checkpoint. STND.INSTR 1.1 (entry 41) names no
  tool or method (GOV.18) and defines Dry run; environment means are to be
  derived from the standards and recorded under STND.DFLT.22.

- STND.INSTR 1.0 was adopted on 2026-10-10 (entry 38): eight binding
  provisions of agent practice; the old draft's restatements of LVL0 and its
  default standing authorization were dropped. `test_ledger_pins` then edited
  STND/ANNEX, which no transaction pinned; since the adoption of STND.ANNEX
  1.0 (2026-10-23) it edits TAG.

- STND.DRAFT 1.2 (entry 34) adds STND.DRAFT.34: each document below LVL0
  holds a References table of the documents it cites, derived and checked
  by `references` and g.25. STND.IDENT 1.3.1, STND.CLASS 1.2.2, and
  STND.DFLT 1.0.1 (entries 35 to 37) conform; undivided drafts conform on
  re-derivation.

- STND.DFLT 1.0 was adopted on 2026-10-10 (entry 33), after LVL0 1.5
  (GUARD.7 temporary items, Lexicon Temporary item; entry 30) and the MNEM
  row SIGNR (entry 32). Entry 30 was appended by an agent error before the
  1.5 text reached the corpus: a rehearsal script ran the live ledger tool,
  so entry 30 pins revision 1.4. Entry 31 (type `annotate`) records the
  error and pins revision 1.5; entry 30 is not edited. The amendment
  primitives (`govharness.workflows.amend`) now take the corpus root as
  a parameter, and `rehearse` fails when a script changes the source.

- STND.DFLT 0.2 (2026-10-10) applies the custodian's rulings: no numeric
  bulk size and no time limits; listed scope, bounds of reach, and owner
  signatures. The harness signs ledger entries (`ledger append --sign`,
  `--ledger-id`) and verifies them against SIGNR with an anchor from
  `/etc/governance/signer.json` (`sign check`, `verify`). LVL0 1.5
  (GUARD.7, Temporary item) and the MNEM row SIGNR await ratification
  (`drafts/lvl0-1.5-proposal.md`).

- STND.DFLT 0.1 was drafted on 2026-10-10 and revised after two rounds of
  independent review; it sits in the corpus as a draft awaiting the QA.7
  review. The logic facts no longer read "reserved-action register" as a
  reservation.

- STND.IDENT part two was ratified on 2026-10-10 after an aggressive
  review for padding, atomicity, and consistency: STND.IDENT 1.3 (entry 27,
  STND.IDENT.15 to STND.IDENT.23 and checks v.9 to v.11), the initial
  register MNEM (entry 28, type `register`, 57 rows), and STND.DRAFT 1.1
  (entry 29, the term Locator defers to STND.IDENT.15 and STND.IDENT.16).
  The draft and its build scripts are kept in `drafts/`.

- Every remaining defect in the adopted documents was fixed on 2026-10-10
  by one amendment each, in order: STND.DRAFT 1.0.2 (entry 20, reviewer
  leaves the undefined role words), STND.CLASS 1.1.1 (entry 21, CSQ3
  auditor wording), STND.CLASS 1.2 (entry 22, a credible consequence
  includes foreseeable misuse), LVL0 1.4 (entry 23, Review keeps its
  ordinary meaning outside changes), STND.CLASS 1.2.1 (entry 24, field
  `withdrawn`), and STND.IDENT 1.2 (entry 25, STND.IDENT.14 and check
  v.8). Entry 19 (type `annotate`) records The Custodian as the actor of
  entries 1 to 18 and the agent authorship of their text (REPRO.5); from
  entry 19 every transaction names its actor.

- The global consistency review's governance findings are resolved. The
  custodian ruled under GOV.3 (entry 15, type `rule`) that the adopter's
  recorded decision satisfies the QA.7 review of a revision. Three minor
  amendments followed in order: STND.CLASS 1.1 (entry 16: reliance tests
  follow GOV.12, review drops its CSQ4 row, new STND.CLASS.20 ties the
  proportionality judgment to the classification), LVL0 1.3 (entry 17:
  Reviewer and Standards owner in the Lexicon, Promotion, Amendment, and
  Auditor redefined, NEVER in the list of capitalized words), and
  STND.IDENT 1.1 (entry 18: new STND.IDENT.13 states the ruling, and
  STND.IDENT.6 fixes how amendments are cited). Check e.2 now accepts
  LVL0 section locators in `governed_by`.

- STND.CLASS 0.4 (11 provisions) was reviewed by the custodian under QA.7
  (ledger entry 13, type `review`, scope STND/CLASS) and adopted as
  revision 1.0 (entry 14, type `adopt`, authority GOV.41, scope
  STND/CLASS); adoption changed only the status, revision, adoption dates,
  and revision history. A global consistency review followed; its
  harness and documentation findings are fixed, and its governance
  findings await amendments (see claude/reviews/global-review-2026-10-09.md).

- STND.DRAFT 0.3 (33 provisions) passes its own checks at FAIL severity.
  It was re-derived from the review of 0.1 as 0.2; the SHOULD NOT row of
  its modal table (0.3) follows LVL0 revision 1.1. The custodian reviewed
  0.3 under QA.7, and ledger entry 8 (type `review`, scope STND/DRAFT) pins
  the content reviewed: a later edit to STND/DRAFT fails the ledger check
  until a later transaction with the same scope pins the new content. The review accepts that provisions 3, 14, and
  23 are checked by the reader and that review-class flags remain. The
  custodian then ratified STND.DRAFT: revision 1.0 (ledger entry 9, type
  `adopt`, authority GOV.41, scope STND/DRAFT) changes only the status,
  revision, adoption date, and revision history of 0.3. The scope is the
  one standard, so edits to other standards stay free of its pin. From
  adoption, a defect in a binding numbered provision below LVL0 fails the
  checks; none exists now. STND.IDENT was adopted as 1.0 (ledger entry 10, scope STND/IDENT) with revision numbers only. The six undivided drafts
  are still drafts, and the undivided ones are listed in the g.24 punch
  list.

- Resolved: the lineage check l.4 counted only the prime directives,
  GUARD, and the four named floor obligations as forcing a binding mark,
  although GOV.10 places GOV in the floor too. GOV now forces the mark,
  so a LVL2 provision that instantiates a GOV provision is binding
  without a recorded reason (GOV.19). The drafting of STND.CLASS, whose
  criteria instantiate GOV.12 to GOV.24, exposed it.

- Resolved: the adoption of STND.DRAFT (entry 9) set the status of the
  standard but left its 33 provisions at draft. STND.DRAFT revision 1.0.1
  (entry 11, editorial, approved by the custodian) gives each provision
  the status adopted and the adoption date. The new `status` check of
  `verify` fails when an entry's status differs from its document's,
  so the slip cannot recur. The custodian's review of STND.IDENT under
  QA.7, implicit in its ratification, is recorded as entry 12.

- Resolved: LVL0 did not conform to the drafting standard. Revision 1.1
  (ledger entry 5, minor) added SHOULD NOT to Normative Language. Revision
  1.2 (entry 6, minor) made 42 edits in 40 provisions: excluded expressions
  (DSGN.14, GOV.18, GOV.32, GUARD.7, INTPR.11, INTPR.12, PRIME.4, PRIME.14,
  RSRC.7, RSRC.8, SIMPL.1, VV.4), the review-class words "could" and
  "considered", and the quantifier "any" wherever a plainer word served.
  The one edit that adds meaning is GUARD.18, which now names the human
  owner as the party who records what is practical. Revision 1.2.1 (entry
  7, editorial) replaced four "at will" phrasings of 1.2, which the
  standard reads as SHALL. The lvl0 group of the punch list now holds four
  items for the reader: "sufficient" in GOV.38 and PRIME.14 (the criterion
  is stated), "to the extent" in GUARD.18 (a decider and a record now
  stand with it), and "avoid" in PRIN.8 (a false positive: it is part of
  the obligation SHALL avoid harm).

- Resolved: `LEX.index` contained a capitalized NEVER (check d.6).
  Amended by ledger transaction 2 (GOV.40) as LVL0 revision 1.0.1; the
  logic checks now report no warning. A rebuild from scratch imports the
  current text and then replays the transactions.

- Resolved: owner fields were blank or lower case. `ratified_by` of LVL0
  and every `adopted_by` now name a role (LVL0 revision 1.0.3, ledger
  transaction 4, editorial); the project template names The Human Owner.
  Ledger transactions 1 to 3 keep their blank `actor`, because the ledger
  is append-only (PRIME.5).

- Resolved: the field `version` of profiles and standards was renamed
  `revision`, so every document uses one field (STND.IDENT.7).

- Resolved: provisions used three roles the Lexicon did not define. LVL0
  revision 1.0.2 (ledger transaction 3, GOV.40, editorial) adds `LEX.author`
  (REPRO.5, QA.7, GOV.34), `LEX.adopter` (GOV.41, GOV.42, GOV.46, GOV.49),
  and `LEX.auditor` (QA.2, GOV.47). The three words leave the undefined list
  of STND.DRAFT.29; g.19 now treats them as defined roles.
