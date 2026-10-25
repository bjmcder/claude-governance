# Cold and STND.HARN.28 pair review of package P4 (2026-10-25)

I rehearsed fresh (seqs 148 to 151, copy `/tmp/rehearsal-47l1c_sw/governance`); it is identical to `.scratch/p4/governance`.

## Verified by script
- `verify`: eight checks PASS. `findings.py`: 22 g.18 and g.6 notes, the same count as the live corpus, none on STND.HARN.29, .30, or STND.OFFLD.31. `check_refs.py`: 0 missing.
- The reading copies contain every paragraph of the rehearsed files. All four rationales end with the fixed tail once and cite no entry of this round.
- No banned word in the changed Notes. STND.HARN.30 has one SHALL per sentence, a three-word title, and body IDs equal to `instantiates` plus `refers_to`.
- Classes under STND.IDENT.3 are right: OFFLD 1.0.1, MPI 1.0.1, and OMP 1.0.2 editorial; HARN 1.3 minor. STND.PERF.12 and .14 apply from CSQ3, so no citation moves a class.

## Defect
1. **The STND.HARN rationale cites `harness/records/units/0012-expiry-horizon.md`, which exists only in unmerged worktrees.** Fix: cite unit 0010 only, or merge unit 0012 before the apply.

## Should-fix
1. **The rationale pre-writes a ruling.** "The custodian rules at ratification that neither raises the floor, and that the acceptance ... is an assigned decision" settles decision 7 (CUSTODIAN.md forbids this). The Notes also assert reading (a) flatly. Fix: write "The floor argument and the reading of STND.DRAFT.42 in the Notes are put to the custodian at ratification", and have the Notes say "requires no decision of the human owner other than an assigned one".
2. **The floor argument skips STND.DFLT.23 and STND.DFLT.5.** "The record then states no grant of the human owner" meets DFLT.23 sentence 2, which accepts any entry that names the human owner as actor in work that is not assured. Fix, appended to the argument: "STND.HARN.30 does not change what an agent accepts under STND.DFLT.23. It limits what a configuration relies on, and STND.HARN.18 lets a configuration refer the rest. STND.DFLT.5 forbids an agent to append such an entry, and nothing in the record shows that none did."
3. **A rule sits in the Notes in the indicative.** "A ledger that a harness is unable to read for that trace counts as one" is absent from the row Signature, yet the code requires the signature there (`register_trace`, `ledger_shape`). Fix: add "or the ledger cannot be read for these" to the row. The row otherwise matches the code (assured, register, signed entry, scope under `SIGNR`, anchor from a file the account cannot alter).
4. **Two Notes sentences misdescribe the code.** "Without the acceptance ... the writes are referred" and "a harness that refuses ... because the writes are then referred". The code stops the derivation and writes nothing (`read_authorizations` raises). Fix: "derives no configuration with it, or one that refers its writes".

## Optional
- HARN.30 sentence 1 has one condition, first. "only on an authorization that the human owner accepts unsigned at the derivation" restricts the object; a strict reader may count it as trailing. No wording keeps the meaning without it.
- The code names per-action authorizations as relied on unsigned although their writes are referred. Harmless.
- OFFLD Notes: "as they reach all other code" should read "in a performance evaluation, as they reach all other code". PERF.12's second sentence also names the first filling of caches and memory, which OFFLD.31 does not; a content gap for the custodian.
- Rows 1.1 and 1.2 of STND.HARN carry a GOV.42 transition clause; add "Transition (GOV.42): none." to row 1.3.
- If the custodian picks (b) or (c) below, the HARN script needs a variant; a switch that drops STND.HARN.30 and its Notes saves rework.
- "Article of safeguards" occurs nowhere else; align with P5. The reading copies are named `-0.1` but hold 1.0.1, 1.0.1, 1.0.2, 1.3.

## The eight decisions
1. Agree. PERF.12 and .14 leave offloaded work to OFFLD.31, so either sentence dropped leaves a gap.
2. Agree, editorial. 3. Agree; GOV has a row.
4. Agree, a "no change" for the custodian. CONC.30 reaches processes and threads (Term Concurrent task). No MPI or OMP provision orders output. The OMP ordered-region fact is sourced (r2, `ordered` row); the rest is marked "by inference". The MPI facts on forwarded output and the shared file pointer are marked unverified, and the research holds neither. No provision rests on any.
5. Agree: the row narrows what passes unreferred, and a configuration that refers all meets HARN.18.
6. Agree, with Should-fix 2. HARN.30 instantiates GUARD.10 and PRIME.7, so GOV.19 makes it binding. Reliance is optional, so a harness that never relies meets it, and the owner who declines pays only referrals. GUARD.10, .11, PRIME.7 are untouched; no floor rises.
7. **Recommend (a).** HARN.30 requires no owner act, only a condition on reliance; the acceptance is one act per derivation inside the configure act of DFLT.22. (b) puts the cost of a register on all non-assured work, against GOV.11's proportion. (c) leaves the PRIME.7 hole that review of unit 0010 found. Weakness of (a): the flag authenticates nothing, and DRAFT.42 sentence 2 can be read against any added act.
8. Agree for OFFLD, MPI, and OMP. For HARN the harness already implements row and provision, and OPEN-ITEMS says installation is pending (not otherwise verified).

## Pair review
- **Coverage, by script.** `pairs` regenerated for the four documents is byte-identical to the p4 lists, with numbers contiguous and unique (OFFLD 526, MPI 250, OMP 477, HARN 16). The 7 rows of `pairs-changed.md` equal the rows with changed side OFFLD.31 or HARN.29. MPI and OMP change no provision. HARN.30 has no pair: only STND.DFLT, PROJ, and WPROC provisions instantiate GUARD.10 or PRIME.7 (checked over every file).
- **495 to 499, OFFLD.31 against HW.22, HW.CPU.4, HW.GPU.4, HW.QPU.8, NUMER.17.** No conflict, nothing unowned. HW.22 holds claims; OFFLD.31 holds where a timing ends and what it states. HW.CPU.4 and HW.GPU.4 record resource use, not timing. HW.QPU.8 and NUMER.17 share only RSRC.4.
- **15 and 16, HARN.29 against AGENT.11 and AGENT.17.** No conflict. AGENT.11 is the Extension row from the other side. AGENT.17's authorizations "in force" can be wider (DFLT.17), and the configuration refers the rest, as in the 2026-10-24 verdicts.
- **Read, not listed:** HARN.30 against GUARD.10 to .12, PRIME.7, HARN.18, .19, .29, PROJ.6, .7, DRAFT.42, DFLT.5, .16, .17, .22, .23, PROJ.3, WPROC.12. Compatible. HARN.19 gains one reported item. PROJ.6 and .7 need no field, since the acceptance belongs to the derivation. The tensions are DFLT.23 (Should-fix 2) and DRAFT.42 (decision 7).

## Not checked
The drafter's notes (p4 holds no notes file; I read the docstrings and rationales), the harness suite, the installation state, the MPI and OpenMP facts against primary sources, and P5's wording for the same References gap.
