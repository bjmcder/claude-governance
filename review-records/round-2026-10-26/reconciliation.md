# Reconciliation review of the round of 2026-10-26

## Verified by running

- `rehearse governance apply_round_2026_10_26.py`: entries 176 to 182, every check passes, warnings only `unpinned` (5 paths) and g.18, source unchanged. A kept copy (`/tmp/claude-1000/recon/gov`) was diffed against the live corpus: only the six documents, their manifests, the eight deleted STND.HARN files, and the two new ones (STND.HARN.31, .32; STND.IDENT.24) differ.
- Corpus-wide grep for STND.HARN.18 to .23, .29, .30 on that copy: they remain only in the STND.HARN field `withdrawn`, its revision rows 1.1 to 1.4, and the ledger. No References table, `instantiates`, Note, or Lexicon entry cites them. "Derived configuration" and "Refer" occur nowhere else; STND.DFLT.22 and .23 carry no HARN citation.
- Term search over every Terms table and `LEX/`: Reach, Pin in force, Sentence, and Cited document are each defined once and clash with nothing. `scope_hash` reads sorted scope paths, which the Content hash wording follows.
- Experiment: in a copy, HW.GPU names STND.CXX bare. g.25 fails with the row absent, and fails with the row present ("references table not cited STND.CXX; text names STND.CXX without a citation").

## Terms and agreement

- Reach does not sit badly beside STND.DFLT.25 ("Bounds of reach"). STND.DFLT.25 uses the word in its ordinary sense, STND.HARN uses it only for ledger scopes, and STND.HARN cites STND.DFLT only for the signer register. No change needed.
- STND.HARN.7, .9, .31 and the terms Content hash, Pin in force, and Reach agree. STND.IDENT.12, .14, and .24 agree (STND.IDENT.14 covers a document's own provisions, STND.IDENT.24 those of its parts). STND.DRAFT.34 and the Checks section disagree in one point (Should-fix 1).
- STND.HARN.13 and STND.HARN.7 say "scoping the signer register" without the term Reach. Optional 1.

## Defect

None found.

## Should-fix

1. **STND.DRAFT, term Cited document and Checks, leave a loop.** The term and STND.DRAFT.34 make a bare-named document one whose row the table must hold, yet a row without a citation also fails g.25 (see the experiment). Text at fault: "so g.25 also fails where the text names a document by its bare identifier and cites it nowhere; a citation of the document fixes the table." Replace with: "so g.25 also fails where the text names a document by its bare identifier and cites it nowhere, whether or not the table lists it; a citation of the document is what satisfies the check."
2. **STND.HARN 1.4 row omits the changed term Content hash.** The reading lists STND.HARN.7, .9, the new terms, and .31 and .32, but not that the term now counts each ".md" file once, under the first path of the scope that reaches it. Insert after "with the new term Reach;" in READING of `apply_harn_1_4.py`: `the term Content hash counts each ".md" file that a "scope" reaches once, ordered by the first path of the "scope" that reaches it;`.
3. **Ledger rationales of STND.HARN, STND.DRAFT, and STND.IDENT write a pending step as future.** Each opens "ratified by the custodian on 2026-10-26" and then says "are put to the custodian at ratification" or "the argument is put to the custodian at ratification". Once applied, the permanent record contradicts itself, and no earlier entry has such a clause. Delete these clauses (STND.HARN: "and are put to the custodian at ratification"; STND.IDENT: "; the argument is put to the custodian at ratification"; STND.DRAFT: ", the argument is put to the custodian at ratification, with the reading of the section Checks, which follows the harness") and leave the floor arguments. The questions stay in `dispositions.md`.
4. **STND.IDENT 1.4 row omits the Checks change.** The STND.DRAFT row names its Checks changes; the STND.IDENT row does not name the new v.8 description. Append to READING: `; the section Checks describes v.8 as reading the field withdrawn of the constitution for the provisions of its parts`.
5. **Order of rows 176 to 179.** The rows of STND.DFLT, STND.PROJ, HW.GPU, and HW.QPU say "since STND.HARN 1.4 withdraws", and STND.HARN 1.4 is entry 180. This breaks no check, because no withdrawn identifier is cited at any step. Wording `since STND.HARN 1.4 (entry 180) withdraws` would make the order explicit. See Optional 3.

## Optional

1. STND.HARN.13 and STND.HARN.7: "scoping the signer register" could read "whose "scope" reaches the signer register" if the custodian wants the new term used throughout.
2. STND.HARN Notes, first sentence on pins, repeats the term Pin in force nearly word for word. It is explanation, not a provision, so GOV.31 is not broken. It could begin "The effect of STND.HARN.9: a later transaction ...".
3. Content hash: "the first path of the "scope"" means first in code-point order. State it: `ordered by the first path of the "scope", in code-point order, that reaches the file`.
4. Decision 5 lists STND.DFLT.22 among what is amended. STND.DFLT.22 cites no withdrawn provision and stays unchanged; the STND.DFLT rationale could say so in one clause.

## Withdrawal, records, ordering

No citation of the withdrawn identifiers remains outside revision histories and the ledger. Nothing depends on them or on the removed terms (STND.DFLT.22, STND.DFLT.23, STND.INSTR read coherently). The `configure` type remains in STND.HARN.7 with its explanatory sentence. Outside the corpus, `harness/README.md` still cites them; it is owed (draft-status item 11). The order of transactions 176 to 182 leaves no state that cites a withdrawn identifier. Rationales and rows agree with `decisions.md`, and none writes a ruling not made.

## Questions for the custodian (`dispositions.md` list)

The four listed are stated fairly, with these gaps:

1. Question 1 (decision 4) gives file scopes as the reason for the pin transactions following STND.HARN 1.4. That holds for STND.HARN/_doc.md and README.md only; KNOW, TAG, and _PROJECT are directories and could be pinned before STND.HARN 1.4, as decision 4 says, without a transition. Add this alternative.
2. Missing: the `last_provision` field (unit 0017, H1) is listed as in scope in `decisions.md` but left out of the round (`draft-status.md`). `dispositions.md` should ask: "Leave the field `last_provision` to a later round?"
3. Missing: should the five pin transactions be scripted and rehearsed inside this round, or recorded after it? The scripts of the round do not hold them.
