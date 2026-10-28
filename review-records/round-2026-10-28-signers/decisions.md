# Round of 2026-10-28 on signer keys: decisions and drafting

The custodian directed on 2026-10-28 that the open item of unit 0016 on the term Accepted signature go ahead, and that the signature feature remain unadopted: no signer register is founded, no anchor file is written, and no signature is required.

As STND.HARN 1.4 reads, an open row for "all" ledgers accepts its key on every ledger, and STND.HARN.10 keeps such a row open. A harness reads the register as it stands, so removing the row would leave each signature that the key made unaccepted. A key with an "all" row is therefore never retired. Closing by a date fails, because the signer writes the timestamp; closing by a Last entry fails across ledgers, because each ledger numbers its own entries.

## Decided, for this round

1. **Per-ledger keys.** Each row among signers names one ledger; a row for "all" ledgers stays only among required signatures. The custodian chose this over the draft of unit 0016, under which a row of one ledger overrides the row for "all" ledgers, since that draft leaves a closed key open on each ledger begun later.

## Drafted, for ratification

- STND.HARN 1.5 (minor): `tools/amendment-scripts/apply_signers_round_2026_10_28.py`, entry 202 in rehearsal; every check passes with the g.18 warning that the corpus already carries.
  - STND.HARN.10: "The Ledger of each row among signers SHALL name one ledger, not "all". A row for "all" ledgers among required signatures SHALL have From entry "1" (GOV.36)." The first sentence is unchanged.
  - The term Accepted signature drops "or "all"".
  - STND.HARN.7 (field "signers") and STND.HARN.13 read the keys that the register leaves open "on the governance ledger" (finding S1 below).
  - The Notes state that a key leaves only by the closing of its row, why a row for "all" ledgers is never closed, which keys the register leaves open, and the floor argument: nothing is asked of a project without a signer register, and of one with a register only a row for each ledger that a key signs; no decision of the human owner.
  - Transition (GOV.42): none, since no signer register exists.
- The harness (unit 0021, `harness/records/units/0021-signer-rows.md`): a signer row for `all` is a register problem and accepts nothing; `with_signer` refuses one; the refusals beside an `all` row are gone; a key with rows on several ledgers is written into the register once.

## Review

`review.md`, by an agent of another configuration: no defect.

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | "The keys it leaves open" (STND.HARN.7, field "signers"; STND.HARN.13) is ambiguous once a key is open on one ledger and closed on another | Fixed, by the reading the harness already had: both read "open on the governance ledger", the only keys able to sign the next transaction of the register; the Notes say so. The review proposed "on at least one ledger", which would list keys that are unable to sign a register transaction. Drafted, for ratification. |
| S2 | The rationale says "ratified by the custodian on 2026-10-28" before ratification | Kept, as in each round: the script is applied only after ratification (CUSTODIAN.md, step 7). |
| O3 | Notes: "a key that signs on several ledgers has a row for each" reads as an obligation | Taken: the clause is dropped. |
| O4 | "name one ledger" could admit a cell of two | Not taken, as the review advises: the Ledger columns read the same way throughout. |

`review-records/harness/review-unit-0021.md`, by an agent of another configuration: no High finding; of 13 mutations, 11 were killed.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 (M) | No test of a row of required signatures for `all` | Fixed: `test_required_row_for_all`; the mutation is killed. |
| 2 (L) | A second armor of a key already held is dropped silently | Fixed: `with_signer` refuses it; tested. |
| 3 (L) | `with_signer_closed` closes each open row of the key on the ledger, whatever its role label | Documented, in the docstring and the README row of `sign close-signer`. |
| 4 (L) | `with_signer_closed` closes a hand-written `all` row | Fixed: refused, citing STND.HARN.10; tested. |
| 5 (L) | The problem-text test checks a substring only | Not taken: optional, and no defect. |
| 6 (L) | `All` passes as a ledger | Fixed: `all` in any case is refused and is a register problem; tested. |
| 13 (mutation) | The role-label test of `_valid_for` was untested (before this unit) | Fixed: a wrong actor is refused; the mutation is killed. |
