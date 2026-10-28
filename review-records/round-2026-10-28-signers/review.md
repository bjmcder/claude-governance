# Cold review: STND.HARN 1.5 (signer rows per ledger)

## What I ran

Read CUSTODIAN.md, decisions.md, the script, STND.HARN (_doc, 7, 10 to 13, 17), STND.DFLT (_doc, 23), GOV.11, STND.IDENT.3, AGENT.17, and unit 0016 (M1). Applied the script to a copy at `/tmp/claude-1000/rv1/governance`. `verify` passes (g.18 warning only, which decisions.md says the corpus already carries; HARN.10 has three modals). `pairs STND.HARN` lists six pairs. Diffed _doc.md. Confirmed no `SIGNR` exists in the repository.

## Findings

### Defect

None.

### Should-fix

1. **"Keys the register leaves open" is now ambiguous (STND.HARN.7 field "signers", STND.HARN.13).** Under "all" rows, a key was open or not. With per-ledger rows a key may be open on `work-a` and closed on `governance`. STND.HARN.13 reads on governance-ledger transactions only. Its test "an accepted signature by a key in the previous one's signers" still holds, because the term requires a row for that ledger, so no key is wrongly accepted. But the second sentence ("the keys it leaves open differ from the last one's signers") does not say which ledger decides. Text at fault, HARN.13: "or the keys it leaves open differ from the last one's". Replacement: "or the keys it leaves open on at least one ledger differ from the last one's". STND.HARN.7 "the keys the register then leaves open, by fingerprint" takes the same words: "the keys the register then leaves open on at least one ledger, by fingerprint". Both are small edits that stay minor. If the custodian prefers the amendment to touch HARN.10 only, the Notes should say which reading holds.

2. **Rationale: "ratified by the custodian on 2026-10-28" (RATIONALE and `ROW` "Minor amendment" row).** decisions.md rules decision 1 and records the rest as "Drafted, for ratification". The rationale states the ratification as done. That is correct only if the script is applied after ratification (CUSTODIAN.md step 7). Apply it only then. If the rationale is written before, replace "ratified by the custodian on 2026-10-28" with "ratified by the custodian on the date of this entry" or drop it.

### Optional

3. Notes: "and a key that signs on several ledgers has a row for each." This reads as an obligation in the indicative. HARN.10 and the term already imply it. Replace with nothing, or "a row for one ledger accepts the key on that ledger only."

4. HARN.10: "SHALL name one ledger, not "all"" could be read to permit a cell "a, b". The Ledger column of the other tables has the same wording, so I do not press it.

## Answers to the brief

1. A key stays accepted after all its rows are closed only if a row for a ledger is missing, and then it was never accepted there. Old behavior lost: one row for all ledgers covered ledgers begun later without a register edit. The custodian chose that loss (decision 1), and the Notes state it. A required-signatures row for "all" with From "1" is coherent with HARN.11, which names "ledger or all" for required rows only, and the actor test is by Role label per ledger. HARN.13 reads correctly except for finding 1.
2. Notes: true; no narration of drafting; the floor argument is sound (nothing asked without a register; with one, a row per ledger in place of a row for all; no owner decision), assuming GOV.36 is the only instantiation, which it is.
3. Drafting: one modal per sentence, three in HARN.10; conditions before clauses; no banned words; body identifiers (GOV.36) equal instantiates plus refers_to; title unchanged.
4. Minor under IDENT.3 (alters an obligation and a defined meaning). Revision row and rationale state only the change, except finding 2. "Signatures stay unadopted" matches the 2026-10-28 direction, and OPEN-ITEMS cites the 2026-10-26 deferral. Transition none is justified, since no signer register or anchor file exists.
5. Pairs: HARN.11, 12, 13 vs AGENT.17 (read the record first), no conflict. HARN.17 vs HDES.14, HW.8, HW.GPU.3: HARN.17 is unchanged and unrelated to this change, no conflict. HARN.10, 11, 13 vs STND.DFLT.23 ("lists for that owner and ledger"): no conflict, and now closer. The term Signer register ("each listed for the ledgers it signs"): consistent.

## Question for the custodian

Is a key "open" for HARN.13 when it is open on any one ledger (finding 1), or only on the governance ledger?
