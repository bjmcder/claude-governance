# Decisions of the custodian, round of 2026-10-27

The custodian's answers of 2026-10-27 on the first item of `OPEN-ITEMS.md`: foreign interfaces in STND.CODE, decision 26 of `review-records/round-2026-10-25-close/decisions-final.md`, from finding S5 and S4 of `reconciliation-alignment.md` of that round. These decide what the round drafts. They do not ratify any text: each amendment is still drafted, self-checked, rehearsed, reviewed, and presented for ratification under the standing process of `CUSTODIAN.md`.

## Decided, for this round

1. **Extent.** STND.CODE gains the language-neutral rules on foreign interfaces as defaults, with one term Foreign interface. The provisions of the language standards that those rules cover wholly are withdrawn, as STND.CXX.16 and others were on 2026-10-25, and the others keep only what their language adds. The terms Foreign interface of STND.CXX, STND.STDC, STND.PY, and STND.JL, and Foreign function interface of STND.RUST, give way to the one of STND.CODE.
2. **Home of lock files.** STND.DEPS defines Lock file once, and holds the shared rule on committing it.
3. **Form of the lock-file rule.** The rule asks a committed lock file only of an environment or a build that produces reported results, the form of STND.PY.33 and STND.JL.4, so that it carries the least burden. A package that other work uses, and that produces no reported result itself, may leave its lock file uncommitted. The third sentence of STND.RUST.30, on builds from the locked revisions, stays a Rust rule.
4. **Reach.** The STND.CODE rules apply to every language, as STND.CODE does by its scope: C, Fortran, Lean, and hardware descriptions gain the defaults where they have a foreign interface.

## Ratification of 2026-10-27

After the cold and pair reviews A and B, the cold verification, the reconciliation review, and a last cold verification, none with an open defect, the custodian ratified the round as drafted, accepting the twelve drafting choices at the end of `dispositions.md`.
