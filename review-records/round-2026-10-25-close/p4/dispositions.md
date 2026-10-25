# Dispositions of the P4 review (2026-10-25)

These answer `review.md` in this folder. The revised scripts are `apply_offld_1_0_1.py`, `apply_mpi_1_0_1.py`, `apply_omp_1_0_2.py`, `apply_harn_1_3.py`, and `apply_close_p4.py` in `tools/amendment-scripts/`. The reading copies after the fixes are `<ID>-0.2.md`, and the `-0.1` copies are kept as the record of the reviewed draft.

## Defect

1. **The citation of unit 0012.** Resolved by the merge of unit 0012 into main (commit 91ed2fa). `harness/records/units/0012-expiry-horizon.md` exists, and the citation in the STND.HARN rationale is right. The Notes sentence on the expiry follows that record's "P4 routing" item, with the change of Should-fix 4.

## Should-fix

1. **A ruling written in advance.** Fixed.
   - The rationale no longer says that the custodian rules. It now says: "The floor arguments and the reading of STND.DRAFT.42 in the Notes are put to the custodian at ratification." The lead records the ruling after ratification.
   - The Notes now put reading (a) as an argument: "STND.HARN.30 is meant to require no decision of the human owner other than an assigned one (STND.DRAFT.42)", and the acceptance "is read as part of the grant that GUARD.10 reserves".
2. **STND.DFLT.23 and STND.DFLT.5 in the floor argument.** Fixed. The reviewer's text is adopted, with one sentence added to give the reason: a configuration that relied on such an entry without the acceptance would rest on the conduct of the agents it constrains (PRIME.7). The Signature paragraph also notes that STND.DFLT.5 forbids the unsigned authorize that names the human owner. The floor argument now also states that reliance is never required, so a harness that never relies meets STND.HARN.30, and an owner who withholds the acceptance bears only the referrals of STND.HARN.18.
3. **A rule in the Notes in the indicative.** Fixed in the row.
   - The row Signature now also requires a signature where "an entry of its ledger is not an object or has a scope that is not a list of paths or a signature that is not text". This is `ledger_shape` in `derive/environment/authorizations.py`, which `register_trace` counts as a trace and `authorized` in `cli/environment.py` uses to set `signed`.
   - An absent scope or an absent signature passes there, as in the code. "Cannot" was avoided because it is a review-class word of STND.DRAFT.7.
   - The Notes give only the reason: such an entry is able to hide the signs of a register.
4. **"Referred" for a refused derivation.** Fixed. The Notes now say that the harness "derives no configuration that relies on that authorization", in both the expiry sentence and the sentence on the acceptance. Each adds that a configuration that refers those writes meets STND.HARN.18.

## Optional

- **Relative clause in the first sentence of HARN.30.** Kept, as the reviewer suggests. It restricts the object and is no condition.
- **Per-action authorizations named as unsigned.** No change: this is code, and harmless.
- **OFFLD Notes.** Adopted: "reach offloaded work in a performance evaluation, as they reach all other code". The first filling of caches and memory, which STND.PERF.12 names and STND.OFFLD.31 does not, goes to the custodian as a content question (decision 2). No change is made here, since it would add to an obligation.
- **Transition in row 1.3.** Adopted: "Transition (GOV.42): none." ends the row.
- **A variant for options (b) and (c).** `OPTION` in `apply_harn_1_3.py` selects "a" (the default) or "c".
  - Option "c" leaves out STND.HARN.30 and its Notes, keeps the row and the expiry sentence, and says that a harness that refuses an unaccepted unsigned authorization still meets STND.HARN.29. It rehearses with `verify` passing.
  - Option "b" needs a change to the code, so it has no variant.
- **"Article of safeguards".** Aligned with P5 (`apply_ml_1_0_1.py`). The MPI class paragraph now reads "the Safeguards Article (GUARD)". GUARD is cited, so References lists it, as for the other language standards.
- **Names of the reading copies.** The revision is in each copy's heading. The `-0.N` suffix numbers the drafts of this package, as the lead asked.

## Results after the fixes

- `apply_close_p4.py` rehearsed on entry 147 appends entries 148 to 151, and `verify` passes all eight checks. Its one warning, g.18, was already there on the live corpus.
- `findings.py` on the whole corpus gives the same findings as the live corpus: no defect, and nothing on a changed provision.
- `check_refs.py` reports 0 missing rows for the four documents.
- The pair lists are unchanged (byte-identical).

## Reconciliation review, S6

The history row and the rationale of STND.HARN 1.3 did not mention that the row Signature now says "the transaction of the row Record" where it said "that transaction". Both now do. The rationale adds that the wording changed because the row's own conditions also speak of ledger entries, and that it tests the same transaction. After a fresh rehearsal of `apply_close_p4.py`, `verify` passes all eight checks, `findings.py` matches the live corpus, and `check_refs.py` reports 0 missing rows. The reading copy is `STND.HARN-0.3.md`.

## Verification of the reconciliation fixes

1. **The option c rationale.** Under `OPTION = "c"`, the rationale of `apply_harn_1_3.py` no longer cites a reading of STND.DRAFT.42. It says that the floor argument of the Notes goes to the custodian, that STND.HARN.29 asks for no act of the human owner and so the amendment rests on no reading of STND.DRAFT.42, and that a harness that refuses an unaccepted unsigned authorization is a stricter reading of STND.HARN.29. The text under option a is unchanged.
2. **OFFLD Notes (reconciliation A, S10).** The Notes and the history row no longer say that the second sentences of STND.PERF.12 and STND.PERF.14 hold "the same outcomes". They name what those sentences hold, and state that STND.PERF.12 names the first filling of caches and memory among the costs of first use, which STND.OFFLD.31 does not. A record of offloaded work that states initialization and compilation at load meets STND.OFFLD.31. No obligation is added, which leaves decision 2 open.

`apply_close_p4.py` was rehearsed with each option. In both, `verify` passes all eight checks, `findings.py` matches the live corpus, and `check_refs.py` reports 0 missing rows for the four documents. Under option c, the STND.HARN Notes do not cite STND.DRAFT.42. Reading copies (option a): `STND.OFFLD-0.3.md` and `STND.HARN-0.4.md`.
