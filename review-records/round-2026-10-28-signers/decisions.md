# Round of 2026-10-28 on signer keys: decisions and drafting

The custodian directed on 2026-10-28 that the open item of unit 0016 on the term Accepted signature go ahead, and that the signature feature remain unadopted: no signer register is founded, no anchor file is written, and no signature is required.

As STND.HARN 1.4 reads, an open row for "all" ledgers accepts its key on every ledger, and STND.HARN.10 keeps such a row open. A harness reads the register as it stands, so removing the row would leave each signature that the key made unaccepted. A key with an "all" row is therefore never retired. Closing by a date fails, because the signer writes the timestamp; closing by a Last entry fails across ledgers, because each ledger numbers its own entries.

## Decided, for this round

1. **Per-ledger keys.** Each row among signers names one ledger; a row for "all" ledgers stays only among required signatures. The custodian chose this over the draft of unit 0016, under which a row of one ledger overrides the row for "all" ledgers, since that draft leaves a closed key open on each ledger begun later.

## Drafted, for ratification

- STND.HARN 1.5 (minor): `tools/amendment-scripts/apply_signers_round_2026_10_28.py`, entry 202 in rehearsal; every check passes with the g.18 warning that the corpus already carries.
  - STND.HARN.10: "The Ledger of each row among signers SHALL name one ledger, not "all". A row for "all" ledgers among required signatures SHALL have From entry "1" (GOV.36)." The first sentence is unchanged.
  - The term Accepted signature drops "or "all"".
  - The Notes state that a key leaves only by the closing of its row, why a row for "all" ledgers is never closed, and the floor argument: nothing is asked of a project without a signer register, and of one with a register only a row for each ledger that a key signs; no decision of the human owner.
  - Transition (GOV.42): none, since no signer register exists.
- The harness (unit 0021, `harness/records/units/0021-signer-rows.md`): a signer row for `all` is a register problem and accepts nothing; `with_signer` refuses one; the refusals beside an `all` row are gone; a key with rows on several ledgers is written into the register once.
