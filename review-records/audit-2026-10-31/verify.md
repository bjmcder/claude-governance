# Cold verification of the round of 2026-10-31 (applied copy `full2`, ledger 325 to 343)

Method: read the applied text in `full2/harness/governance` against each disposition; `diff -r` against live; `verify` on a scratch copy; `findings.py` on both; scan of every changed provision for modal counts per sentence and `such as`/`for example`; scan of ledger rationales 325 to 343.

## Machine checks

- `govharness verify` on a copy of `full2/harness/governance`: exit 0; ids, mnemonics, references, manifests, ledger, unpinned, templates, status, checked-by, onset, logic all PASS. Only warning: g.18 (as before).
- `findings.py ... '.'`: live 249 lines, applied 254. The five new lines are g.18 INFO "three modals" on STND.CLASS.20, STND.DFLT.17, STND.DFLT.23, STND.DFLT.36, STND.INSTR.11 (three modals is the limit, not a breach; disclosed in process/decisions.md "Checks"). The text of the existing g.11 on STND.CXX.3 changed ("the dependency" added), same count. No other difference.
- No sentence of a changed provision carries more than one modal except PRIME.11 sentence 2 (V3) and the unchanged PRIME.14 sentence 3. No provision of the diff carries more than three modals. No `such as`/`for example` in changed text (the one hit, DFLT Notes "Command-level practice, such as shell guards", is unchanged). Body IDs match instantiates + refers_to (references check PASS).
- "LVL0 LVL0": no occurrence in `full2` outside `review-records/`; ledger 325 to 343 have none.

## Ledger rationales 325 to 343

Each opens "... ratified by the custodian on 2026-10-31" (true at application). Every other mention of the custodian is "put to the custodian at ratification", a recommendation ("carry recommendation R1 ..."), "at the custodian's direction" (true: the direction quoted in decisions.md), or the prior ruling of 2026-10-23 (STND.CXX/PY, real). No rationale says the custodian chose an option or ruled R1 to R11. Entry 325 states the class as "major ... put to the custodian ... with the recommendation to rule the class major", correctly unruled.

## Table

| Finding | Disposition | Verified? | Note |
| --- | --- | --- | --- |
| L1 | Fixed | Yes | PRIME.8: "Where no spending limit ... bounds that cost, and the provisioning ... does not fix its cost ..., the direction authorizes it only where the cost is measurable and only up to ... an estimate that the agent states before the work begins." Halt and referral clause present. |
| L2 | Fixed | Yes | Ledger 325 "Class: major ... drafted under STND.IDENT.4 ... in doubt"; LVL0 2.0. |
| L3 | Fixed | Yes | PRIME.11 "by a recorded act of the human owner's own, within the scope that the act names"; "NEVER names another person and NEVER performs the acts that PRIME.1 assigns"; PRIME.8 "within the scope of that naming". |
| L4 | Fixed | Yes | GUARD.10 "takes no further action under it, and on the line of work that relied on it takes only the steps that leave the work in a safe and recoverable state within its remaining authority (GUARD.3)". |
| L5 | Fixed | Yes | GOV.14 "finds the work relied upon at a class more severe than the class recorded or presumed halts that line of work and refers it (PRIME.14) ... exposure ... grown reports"; PRIME.14 trigger names the case. |
| L6 | Fixed | Yes | GOV.13 "that the record, the request, or the work's own content shows"; QA.11 third sentence (owner's direction as promotion of presumed CSQ4 work); LEX.promotion conformed; DFLT Notes line on promotion present. |
| L7 | Fixed | Yes | PRIME.9 and LEX.elevated-privilege: "an environment that the human owner's provisioning record states is isolated"; STND.DFLT.37 places the record. |
| L8 | Fixed | Yes | GOV.20 "a promotion other than one that QA.11 makes of the adopted classification or of the human owner's direction"; "(GOV.22)" gone. |
| L9 | Fixed | Yes (see V2) | PRIME.13 "reaches only the command toward the safe state and the transfer ... which is a transfer that PRIME.7 permits". |
| L10.1 to .6 | Fixed | Yes | GUARD.14 "a per-task estimate or an operating envelope included"; PRIME.8 "spending limit"; PRIME.11 two NEVERs (but see V3); GUARD.1 "the unit of work that its instructions direct"; GOV.22 "records a consequence class (GOV.13)"; LEX.implicit-expenditure "the part that running the agent incurs, and not the cost of a service or capacity that its actions use". |
| L10.7 | Not fixed | Reason holds | LEX.definition-of-done "recorded or stated in the request for the unit" matches QA.1's new sentence; a request is not made a record. |
| T1 | Fixed | Yes | CPS.1 "commands, configures, or powers"; CPS.10 halt-and-refer, rank 0; Notes except CPS.10. |
| T2 | Fixed | Yes | NUMER Notes: "a result of CSQ3 that lacks the evidence that a moved part would supply has the component concerned marked not assessed under NUMER.13, and carries the label unverified of PRIME.3". |
| T3 | Fixed | Yes | STND.RUST.6 and STND.DOCS.10 binding_reason each open with their own reason and cite STND.INSTR.10 / GOV.48. |
| T4 | Fixed | Yes | NUMER Notes name STND.VVUQ.7, tiers 3 and 5 of STND.VVUQ.1, HW.QPU.6, HDES.ASIC.5. |
| T5 | Fixed | Yes | Term Learned model use: "That exclusion does not reach a learned model that the work builds, trains, or runs as part of what it delivers, even when it is the model of an agent." |
| T6 | Not fixed | Reason holds | Rationale 326 says "ratified by the custodian"; true at application. R7 stated as put to the custodian. |
| X12 / VVUQ.64 | Fixed | Yes | "at each class from which those apply, and under the criterion that the acceptance criterion of the test states at every other class"; one SHOULD; conditions not trailing. |
| X13 CPS Purpose | Fixed | Yes | "actuation by an agent, other than commanding the designed safe state, only within an authorized safe range". |
| X11 | Fixed | Yes | GOV.13, GOV.20, CPS Selector, DFLT.19, DFLT Notes use "commands, configures, or powers". |
| P1, P2 | Fixed | Yes | Terms Foreign entry (after the accepted point, not appended in the session), Accepted point ("where the chain of hashes is intact"), DFLT.23 ("lists each by its position and hash"), DFLT.38. See V5. |
| P3 | Fixed | Yes | AGENT.6 sentence 2 "one effort estimate of all of it, within which the estimate of each of its units lies". |
| P4 | Fixed in part | Reason holds | DFLT.17 and .33 "without each secret that it contains"; one entry per direction kept (custodian item 1). |
| P5, X8 | Fixed | Yes | Term Main line, second clause excludes the default branch absent a record or evidence of release or deployment. |
| P6, X9 | Fixed | Yes | PROJ.2 Notes carry DFLT.23 and .38 to Records, .36 to Identity, .37 to Configuration; PROJ.3 signing row ("Signing commits"). |
| P7 | Fixed | Yes | DFLT.36 sentences 2 and 3. |
| P8, X1 | Fixed | Yes | GUARD.7 fourth ground "that the version history does not yet hold, on which no reported result rests, and that no other actor has changed since that agent last wrote it"; DFLT.15 sixth class cites it and excludes "a revision, a branch, a tag, or another reference of the version history". |
| P9 | Fixed | Yes | Working bounds: "the agent itself reads no secret that they hold, passes none to the tool by argument, variable, or file, changes none of the configuration of those means, and requests no output of the tool that would show a secret". |
| P10 | Fixed | Yes | DFLT.37 "only in the environment that it names, with the provisioning that the entry states". |
| P11 | Fixed | Yes (see V4) | INSTR.11 excludes "a command toward the designed safe state (PRIME.13) nor a step of GUARD.3". |
| P12 | Fixed | Yes | IDENT.23 conditional on "an instrument whose identifier carries a mnemonic of the project"; form in Notes. |
| P13 | Fixed | Yes | No doubling. |
| P14 | Fixed | Yes | DFLT.18 row "Entries of the ledger of work that is not assured, up to its accepted point | Forgery, an acceptance entry in an agent's name included | ... | No". |
| P15, X7 | Not fixed (lead's) | Reason holds | Harness and plugin work after ratification. |
| X2 | Fixed | Yes | DFLT Notes "A direction to bring in revisions does not confirm the entries that they add". |
| X3 | Fixed | Yes | GOV.50 "other than an agent's own operating cost"; GOV.22 "authorized by the human owner's direction that PRIME.8 names". |
| X4 | Fixed as directed; residual to custodian | Yes | DFLT.33 second sentence (figure and plan record); GUARD.14 "is a spending limit that the human owner sets"; Notes have the figure shown. Residual (agent states its own cap) is listed in custodian item 7. |
| X5 | Fixed | Yes | CLASS.20 sentence 3 "Where GOV.13 presumes the class, a promotion SHALL cite the entry of the human owner's direction". |
| X6 | Fixed | Yes | CREW.21 refers to "the bound of PRIME.8 on the operating cost of the unit" and "proposed revised estimate or limit". |
| X10 | Fixed, with an inaccuracy | Partly | See V1. |
| X14 | Residual | Reason holds | Explicit CSQ4 for hardware: CPS.10 halts where CPS is selected; otherwise a custodian item. |

## New findings

### V1 (Low) STND.PROJ Notes misdescribe the first sentence of AGENT.6

- Location: `STND/PROJ/_doc.md`, Notes on PROJ.5.
- Quote: "would otherwise set aside AGENT.10, which applies where no discipline is set, and the first sentence of AGENT.6, which applies where a spending limit or a fixed cost bounds the cost, while the second sentence of AGENT.6 applies under every discipline that sets no spending limit".
- Problem: AGENT.6 sentence 1 applies "where ... the human owner has set no discipline under GUARD.14" (and the cost is measurable), whatever bounds the cost. The reconciliation's X10 wording described AGENT.6 as a whole, not its first sentence. The second sentence also needs no fixed cost and no limit enforced by the environment.
- Fix: "... and the first sentence of AGENT.6, which applies where no discipline is set, while the second sentence of AGENT.6 applies whatever discipline is set where neither a spending limit nor a fixed cost bounds the cost".

### V2 (Low) PRIME.13 precedence clause is circular for the transfer

- Quote: "This permission prevails over PRIME.6, PRIME.7, and PRIME.8, and reaches only the command toward the safe state and the transfer that carries the command to the controller of the hardware, which is a transfer that PRIME.7 permits."
- Problem: "prevails over PRIME.7" and "a transfer that PRIME.7 permits" can be read as a fact (so the transfer needs no authorization) or as a limit (so remote hardware with no network authorization is unreachable). The review (L9) meant the limit.
- Fix: "... and the transfer that carries the command to the controller of the hardware, only where that transfer is one that PRIME.7 permits."

### V3 (Low, drafting) PRIME.11 sentence 2 has two modals

- Quote: "A person so named NEVER names another person and NEVER performs the acts that PRIME.1 assigns to the human owner."
- Problem: one modal per sentence (STND.DRAFT). L10.3 added the second NEVER on purpose, but the rule is not met.
- Fix: two sentences, "A person so named NEVER names another person. A person so named NEVER performs the acts that PRIME.1 assigns to the human owner." (Total modals of PRIME.11 stays within three.) A custodian waiver of the rule for coordinate NEVERs is an alternative; PRIME.14 sentence 3 already has three.

### V4 (Low, drafting) STND.INSTR.11 sentence 3 imposes duties under a permission

- Quote: "An agent MAY treat a passage of such a file as forbidding it an action ..., stating the passage in that report, and at once to the actor that directed it for a passage whose honoring halts a line of work".
- Problem: the duty to state the passage, and to state it at once where honoring halts work, carries no modal; a MAY sentence cannot carry an obligation. The provision already has three modals, so a fourth cannot be added.
- Fix: "An agent that treats a passage of such a file as forbidding it an action SHALL state the passage in that report, and SHALL state it at once to the actor that directed it where honoring it halts a line of work", with the permission moved to a new provision STND.INSTR.12 (or sentence 2 and 3 merged into two provisions).

### V5 (Info, for the custodian packet) An unfinished session turns the agent's own entries foreign

- Location: STND.DFLT.38, term Foreign entry, STND.DFLT.23.
- Problem: DFLT.38 asks the acceptance entry "before an agent ends a session", which an aborted or crashed session cannot meet. In the next session every entry of that session that records an owner act is foreign, so a line of work that relies on a standing authorization from it is referred to the owner at CSQ4 for a confirmation by position and hash. This is the intended safe direction (P1) but it is an owner decision at low class that custodian item 2 does not name.
- Fix: add to custodian item 2 "an ungraceful end leaves the session's entries foreign until the owner confirms them; recommendation: as drafted".

## Safety-net questions

- A compliant agent reaching a condition PRIME or GUARD prohibit: none found. Cost is bounded by a limit, a fixed cost, or a stated estimate, with the sole residual that the agent states its own estimate (X4, disclosed, custodian item 7). Privilege (PRIME.9), instruction authority (PRIME.11, DFLT.36 and .23), GUARD.7 fourth ground and DFLT.15 sixth class (history, regenerability, reported results excluded; GUARD.6 prevails) hold.
- Added halts or owner decisions at CSQ3 and CSQ4: PRIME.8 (nothing authorized where the cost is neither bounded nor measurable, directed at L1), GOV.14 and PRIME.14 (reliance above the recorded or presumed class), DFLT.23 (foreign entries, V5), CPS.10 (hardware recorded below CSQ3). Each is directed or confined to a case with a stated cause; none is routine.
- Contradiction with LVL0 2.0: none found. No stale "No class is assumed" or "even within an isolated environment" remains outside revision rows.

## Verdict

Ready for ratification. V1 to V4 are low drafting inaccuracies that may be corrected before the scripts run or passed as known items; V5 is a note for the custodian packet.
