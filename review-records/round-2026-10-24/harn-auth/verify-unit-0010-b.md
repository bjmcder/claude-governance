# Second verification of unit 0010 (commit e4e57d5)

Suite from `WT/harness`: 201 tests, OK (267 s). Scratch: `/tmp/claude-1000/verify-0010b/`.

## Verdict

N1 and the M1 residual are closed. No High, no Medium. Three Lows.

## Checks

1. **N1, every shape.** `probe.py` runs the `environment` command on a corpus copy, with and without `--accept-unsigned`, with `read_config` patched. All exit 1, write nothing, and show no traceback:
   - entry `5`, `[1]`, `"x"`, `null`: "ledger entry N is no object";
   - scope `5`, `"SIGNR"`, `{...}`, `[{...}]`: "no list of paths";
   - signature `7`, `["a"]`, `null`: "no text";
   - scope `null` on an appended line: chain broken (as in eceabea);
   - empty ledger, missing file, only blank lines: "no transaction of the ledger pins it";
   - `not json`, `garbage`: `Expecting value ...`; invalid UTF-8: the codec message. These come from `parse_ledger` and are caught as `ValueError`. They name no line number and no ledger, but they have a reason.
   - A blank line appended to a valid ledger is ignored and `--accept-unsigned` passes; that is correct.
2. **Anchor.** A `SignerConfig("0"*40)` with no `SIGNR/` is refused with "anchor key" and "--accept-unsigned has no effect", with the option too. Every test that reaches `read_config` is patched (`no_anchor` or an explicit anchor); `/etc/governance` does not exist on this machine, and the early return in `authorized` means no `read_config` call without `--authorization`. Mutant with the anchor ignored fails `test_command_anchor_without_register`.
3. **No widening.** `signed` only gains `trace is not None`; `verified` only gains conjuncts. The unsigned path stays under `not signed`. Mutants in copies: anchor ignored (1 fail); shape check dropped from `read_authorizations` (2 fail); shape check dropped from `verified` (3 errors, TypeError); `trace` left out of `signed` (3 fail). Earlier fixes: the M1 register tests, the M2 note and the L2 `verified` test still run in the suite and pass.
4. **STND.HARN.30.** Two sentences, one SHALL each. Conditions come first. The body cites GUARD.10, PRIME.7, STND.HARN.29, STND.HARN.19, and `instantiates` plus `refers_to` list exactly these. No banned word in the row, body, or Notes ("any" appears only in the record's Options line, not in provision text). No SHALL in the Notes.
5. **Suite.** Passes.

## Findings

### Low

**L1. Trailing condition.** The first sentence ends "...only after the human owner accepts it at the derivation". The brief says to avoid trailing conditions. Fix: "Where the work is not assured, neither the corpus nor its ledger records a signer register, and the human owner has accepted an unsigned authorization at the derivation, a derived configuration MAY rely on it", or keep the SHALL as "Until the human owner accepts ... a derived configuration SHALL NOT rely on ..." (a negated modal flagged for review). The first form changes the modal; the custodian chooses.

**L2. Redundant conjuncts.** Dropping `trace is None and ledger_shape(ledger) is None` from `verified` leaves the removed-register and anchor tests passing (only the malformed-register test errors). `ledger_problems` and the per-authorization signature check already refuse. This is defense in depth, not a hole; a comment saying so, or a test that fixes `verified` alone, would settle it.

**L3. Id check.** The review `0006-retrieval-review.md` mentions an older "STND.HARN.30 Rehearsal before application". The live corpus (`harness/governance/STND/HARN`) ends at 29, so I found no clash. The custodian should check the number at adoption.

## Not checked

The real `/etc/governance/signer.json` path (absent here). A signed, real register end to end. Ruff. A case-insensitive filesystem. A malformed `signer.json` (for example a non-object JSON) that would raise `AttributeError` in `read_config`; the file is outside the agent's reach, so I judge it Low and did not run it.
