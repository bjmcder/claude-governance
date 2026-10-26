# Review A: STND.HARN 1.4, STND.DFLT 1.5.2, STND.PROJ 1.2.1, HW.GPU 1.0.2, HW.QPU 1.0.2

## Verified by running

- Applied the round to a scratch copy (`/tmp/claude-1000/revA/gov`): entries 176 to 182, `verify` passes with the two known warnings (`unpinned`, g.18). `findings.py` on my documents shows only pre-existing review findings.
- Searched the copy for `STND.HARN.18` to `.23`, `.29`, `.30`: they remain only in the STND.HARN revision history and in ledger rationales. No other document, Note, References table, Lexicon term or `instantiates` list cites them. No remaining STND.HARN provision uses the removed terms (Derived configuration, Refer, work report, working bounds). STND.DFLT.22 and .23 and STND.INSTR read coherently. `configure` stays in STND.HARN.7 and no ledger entry uses it; STND.DFLT.22 still records a configuration, so it is not orphaned.
- Pins: a script over the live ledger and the rehearsed ledger gives the old set (latest entry per scope) and the new set (Pin in force) as 41 and 41, identical. No two distinct scopes overlap, and none of the five planned scopes (`KNOW`, `TAG`, `_PROJECT`, `STND/_doc.md`, `README.md`) overlaps a scope in use. The rationale's claim holds.
- Entry 53: m.1 and m.2 (`checks/combination.py`) and `pairs` implement STND.HARN.26 to .28, including the uncited-owner row of .27. The row's account of the end is accurate.
- `pairs` on the rehearsed corpus lists no changed provision (HARN.7, .9, .31, .32 absent; GOV is excluded as a basis). `pairs-changed.md` is confirmed. Another adopted document addresses the matters of the new provisions only as follows: STND.DRAFT's definition of `checked_by` (line 57) and HARN.32 agree, and no check already flags an unknown key. No conflict.
- Every `checked_by` key in the corpus is registered except `checked-by` itself (owed by the code). Titles are unique and short.

## Defect

1. **STND.HARN.31 is ambiguous and, read literally, nearly empty.** Text: `Where no "scope" of a governance-ledger transaction names a ".md" file of the corpus or a directory above it, a harness SHALL report FAIL`. "A .md file" is indefinite, so it reads as "no scope names any .md file". Decision 4 and the check mean each file. Replace with: `Where a ".md" file of the corpus is neither named by a "scope" of a governance-ledger transaction nor under a directory that one names, a harness SHALL report FAIL for that file (GOV.36).`
2. **Pin in force: the pronoun "its" can point to the later scope.** Text: `for which no later governance-ledger transaction has a "scope" that holds each of its paths, as that path or a directory above it`. Read as the later scope's own paths, the test is always true and every later transaction ends every earlier pin. Replace with: `for which no later governance-ledger transaction has a "scope" with, for each path of the earlier "scope", that path or a directory above it.`

## Should-fix

3. **Content hash with overlapping paths.** The term says "one per .md file that a path of a scope names or holds", but the code gives a file two lines when one scope holds `STND/HARN` and `STND/HARN/7.md` (hash differs from the directory alone; tested). File scopes now make this reachable, and the text does not say which path orders such a file. Add after "holds": `, each file once, ordered by the first path that reaches it`. The code then follows (owed).
4. **Three phrasings of one relation.** The Content hash says "names or holds", the Pin in force says "holds ... as that path or a directory above it", and HARN.31 says "names ... or a directory above it". In the Pin in force "holds" includes equality, and in the Content hash it excludes it. Use one form; the replacement of item 2 and of item 1 follows the Pin in force, and in the Content hash write `that a path of a "scope" is, or lies under`.
5. **Notes on pins overstate.** Text: `A transaction over part of a pinned scope ends no pin, and the wider pin then no longer matches the content of its scope, so a pinned scope is not narrowed.` The wider pin goes stale only if the part changed (a transaction over part with no content change leaves it matching), and "is not narrowed" reads as a prohibition in the indicative. Replace with: `A transaction over part of a pinned scope ends no pin, so the wider pin goes stale once that part changes, and a transaction over the whole wider scope is what records it.` Also add the case of two scopes that share a path with neither holding the other: `Two scopes that share a path, neither holding the other, both stay in force, and a change of the shared path stales both until one transaction holds both.` The other cases (same scope twice, wider after narrower, several paths, file scopes) are described truly.
6. **Notes on HARN.31 omit its reach.** HARN.5 reads README.md files and template directories as non-items, and HARN.31 reaches them (decision 4 asks for `README.md` and `_PROJECT/`, so the reach is right). The floor argument "which GOV.36 already asks for each change" is weakest there. Add: `STND.HARN.31 reaches each ".md" file, including the README.md files and the files of template directories that STND.HARN.5 does not read as items, because the ledger pins files, not items.`
7. **No transition for HARN.31 in the revision row.** The rationale says it takes effect once the five pin transactions are recorded, but the row (the lasting record) has only the entry 53 transition. Between entries 180 and the pins, text and corpus disagree. Add to the row: `Transition (GOV.42): a ".md" file that no "scope" reaches is no defect until the transactions that pin KNOW, TAG, _PROJECT, STND/_doc.md, and README.md are recorded.`
8. **HW.GPU and HW.QPU new sentence states an obligation in the indicative.** Text: `Without an authorization in force that covers it, each submission halts for a referral (PRIME.7, PRIME.14).` It follows from PRIME.7 and PRIME.14, but it restates them (GOV.31). Replace with: `A submission that no authorization in force covers is one that PRIME.7 and PRIME.14 have the agent halt and refer.`

## Optional

9. STND.PROJ Notes: `a time stated with it bounds the authorization in every case` loses its reason. Use: `a time stated with it still bounds the authorization.` Also `a form that every reader decides alike` overstates; `a form that a reader decides by comparison` is safe.
10. STND.HARN.32: "key of a check of the harness" is checkable but circular; `a key of a check that the harness makes` is clearer. "Registered" in the title suggests a register that does not exist; `Known check keys` avoids it. GOV.38 (software holds no authority) is a thin basis; GOV.37 (stable keys, as HARN.16) may fit better. Custodian's call.
11. HARN Notes `The code accepts type configure on adoption.` could say that STND.DFLT.22 records a configuration, which is why the type stays.

## Checked and sound

Withdrawal is clean (field `withdrawn`, terms, Notes, `instantiates`, citations). Classes are right: HARN minor, the four others editorial (Notes only). Revision rows and rationales say what changed, and none writes a ruling not made. HARN.32's floor argument is sound. The new Notes pass the STND.DRAFT word and modal checks, and the changed provision bodies are clean.

## For the custodian

- Decision 4 says "one transaction first pins" the five paths. The draft makes five transactions after HARN 1.4 (file scopes need HARN.7). Is that order and number acceptable?
- Decision 6 says "one transaction, with no change of text". The draft puts the end of entry 53 in the HARN 1.4 row, in a transaction that changes text. Should it be a separate transaction?
