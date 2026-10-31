# Round of 2026-10-31: ratification packet

This packet asks the custodian for every decision the round needs before it is applied. The round carries the corpus findings of the cleanup audit of 2026-10-31 ([findings](findings.md)), drafted on the outcomes of [decisions](decisions.md). Rulings R1 to R11 of the findings were **not ruled before drafting**. Each was drafted as recommended, and each is put to you here.

## What is being ratified

| Part | Carries | Transactions | Record |
| --- | --- | --- | --- |
| lvl0 | LVL0 2.0: S1 to S3, R1, R2, R3, R5, R8, R9, B2, B3, B10, I1, I3 to I5 | 1 (entry 325) | [lvl0](lvl0/decisions.md) |
| tech | CPS 1.1, NUMER 1.5, ML 1.1, STND.VVUQ 1.6, STND.CODE 1.8, STND.DEPS 1.3.1, STND.DOCS 1.0.3, STND.CXX 1.6, STND.PY 1.5.1, STND.RUST 1.5.1: S7, S8, B8, O3, I2, I6, I7 | 10 (326 to 335) | [tech](tech/decisions.md) |
| process | STND.DFLT 1.7, AGENT 1.4, STND.CLASS 1.6, STND.IDENT 1.6, STND.WPROC 1.5, STND.CREW 1.4, STND.PROJ 1.6, STND.INSTR 1.6: R1, R3, R4, R6, R10, B3, B9, O5 to O7, I1, I9, and the lower text that LVL0 2.0 made stale | 8 (336 to 343) | [process](process/decisions.md) |

There are 19 ledger transactions, entries 325 to 343, made by `tools/amendment-scripts/apply_audit_2026_10_31.py`.

Each part was drafted, then cold-reviewed by an agent of another configuration ([lvl0](lvl0/review.md), [tech](tech/review.md), [process](process/review.md)), and fixed. A reconciliation review then read the three parts together ([reconciliation](reconciliation.md)). Its findings are fixed, and a cold verification ([verify](verify.md)) confirmed each fix in the applied text. That verification's four small findings, V1 to V4, are fixed as it proposed, and V5 is reading 2.18 below.

**The applied corpus.**
- `verify` passes every check, with logic, and only the standing g.18 warning.
- `references`, `compose` (both forms), and `ledger check` (343 entries) are clean.
- The full test suite passes on it.
- The onset counts are CSQ0 6, CSQ1 26, CSQ2 166, CSQ3 619.
- The verification found no route by which a compliant agent reaches a condition that PRIME or GUARD prohibit, and no contradiction with LVL0 2.0.

**Already done, needing no ratification.** None of the following changes governance: harness unit 0025 ([record](../../harness/records/units/0025-audit-fixes.md)), and two tests made independent of the corpus state, all merged on branch `audit-2026-10-31`.
- **Fixes:** S9 (the run form `python3 -B -P -m`), S10 (the ledger check reads the line's text, refuses duplicate keys, and holds the exact field set), H1 (reading copies), H4 to H11, H13, I8, and O4 (`onset CSQn --from CSQm`).
- **Removal:** RP1, the two archive copies.

## How to answer

Each item is drafted as recommended. A reply of **"ratify as recommended"** adopts every recommendation, and the scripts are then applied. To depart from one, name it, for example "R5 option (b)" or "2.10 alternative". The script is then changed, rehearsed, and verified again before it is applied.

Part 1 holds the eleven rulings, which change what binds. Part 2 holds the narrower readings that drafting chose. Part 3 lists the residual risks, so that they stand on the record.

---

## Part 1: the rulings

**R1. An agent's own operating cost (S5, B1).** Before this round, a plain task authorized no cost and PRIME.8 halted it, while naming the agents authorized cost with no bound.
- Drafted (PRIME.8, GUARD.14, STND.DFLT.33, AGENT.6):
  - The human owner's direction of work authorizes the operating cost of the agents that carry it out, in a configuration that the owner provisioned.
  - That cost is bounded by a spending limit that the owner sets or the environment enforces, or by the provisioning's fixed cost.
  - Where neither bounds it, the direction authorizes the cost only where it is measurable, and only up to an estimate that the agent states before the work begins, covering all the work of the direction. The agent shows that figure in its first message, and an extension is referred.
  - Every other implicit expenditure keeps the owner-authorized estimate.
- Recommendation: **ratify.** Alternative: keep PRIME.8 as it stands (findings R1 (c)), which halts every unbounded task.

**R2. Physical safety (S2, S3).**
- Drafted: PRIME.13 lets an agent command the designed safe state without authorization, safe range, or estimate. The permission prevails over PRIME.6, .7, and .8, and reaches only the command and its transfer to the hardware's controller.
- Drafted: the Lexicon terms Network access, Bulk retrieval, and Reserved action match GUARD.13, GUARD.8, and PRIME.6. Reserved actuation is what the hazard analysis identifies, and R7 keeps that analysis current for CPS work.
- Recommendation: **ratify.**

**R3. Who instructs, and who is the owner (S6).**
- Drafted (PRIME.11): a person whom the human owner names by a recorded act of the owner's own may instruct, within the scope named. That person names no one else and performs none of the acts of PRIME.1.
- Drafted (STND.DFLT term Given directly, STND.DFLT.36): absent a record, the person who provisioned the agent's environment and directs the agent is taken as the owner. An agent that cannot tell refers.
- Recommendation: **ratify.** Alternative: define "given directly" only, with no presumption and no named persons.

**R4. Ledger entries the owner never saw (S4).**
- Drafted (STND.DFLT terms Accepted point, Acceptance entry, Foreign entry; STND.DFLT.23, .38, .18):
  - An agent appends an acceptance entry before it ends a session in which it appended entries.
  - An entry recording an owner act that lies after the accepted point, and that the agent did not append in its current session, is foreign. This covers a merge, a fetch, another session, or a hand edit, even where the owner directed the merge.
  - A foreign entry counts only once the owner confirms it by position and hash, all of them in one statement.
  - STND.DFLT.18 now states the residual (Part 3).
- Recommendation: **ratify.** Alternatives: an acceptance entry after every append, or signatures (the assured regime).

**R5. Default class and project constitutions (O1, O2).**
- Drafted (GOV.13, GOV.14, GOV.22, QA.11): until the owner records a class, work is treated as CSQ4.
  - The presumption never covers commanding, configuring, or powering physical hardware, nor a use that the record, the request, or the work itself shows to be more severe; those halt and refer.
  - Under the presumption, the owner's direction promotes each result that meets its criteria, for reliance by its author or by the owner.
  - An agent that finds the work relied upon at a more severe class halts that line and refers.
- Drafted (GOV.20): a constitution is required at CSQ1 and CSQ0, for hardware, and on the owner's request. Without one, a release and a promotion beyond QA.11 are the owner's acts under the defaults.
- Recommendation: **ratify.** Alternatives: (b) keep "no default class", and require a constitution for releases at CSQ2 or above; (c) leave both.

**R6. Project mnemonics (B7).** Drafted (STND.IDENT.23): the owner registers a project's mnemonic in the project's own ledger, as a transaction of type `register`, and MNEM stays the custodians'. Recommendation: **ratify.** One consequence: the harness check v.10 must accept such a mnemonic (X7), which is done after ratification.

**R7. CPS minimum class (S7).**
- Drafted (CPS.1, new CPS.10): work on a system that commands, configures, or powers physical hardware is classified CSQ3 or more severe (GOV.12). Where a less severe class is recorded, an agent halts that line and refers.
- Transition: a project that recorded CSQ4 for such work records CSQ3 before the system next drives the hardware.
- Recommendation: **ratify.** Alternative: PRIME.13 carries the revision duty at every class, which amends a prime directive.

**R8. Superuser privilege (B5).**
- Drafted (PRIME.9, STND.DFLT.37): an agent never acquires or escalates privilege, and uses superuser privilege only where the owner provisioned it, within an environment that the owner's provisioning record states is isolated. The record is an accepted ledger entry naming that environment, and it lapses when the provisioning changes.
- Recommendation: **ratify.**

**R9. The floor for work with nothing to test (B6).** Drafted (GOV.10, QA.1): the floor's VV.7 tests reach work that changes code or data, and a definition of done stated in the request meets QA.1 for its unit. Recommendation: **ratify.**

**R10. Credential means (B4).** Drafted (STND.DFLT, term Working bounds): an authorization of a network access, or of the signing of a commit, covers its tool's use of the credential means that the environment provides. The agent reads no secret, passes none to the tool, changes no credential configuration, and requests no output that would show one. Signing is authorized once, through a new row of STND.PROJ.3. Recommendation: **ratify.**

**R11. How an agent enters a scribe entry (H12).** This one concerns the documentation, not the corpus. `docs/adoption.md` says an agent "can enter it for you" but names no route. Unit 0025 added the read-only `ledger check`, so a work ledger can now be checked.
- Option (a): document `govharness ledger append --ledger-file records/ledger.jsonl` as the route by which an agent appends to the project's own ledger. The corpus stays unwritable through the plugin, and no skill gains a write command.
- Option (b): document the line format, so that agents compute entries by hand and check them with `ledger check`.
- Option (c): remove the promise.
- Recommendation: **(a).**

---

## Part 2: readings that drafting chose

| # | Reading | Recommendation | Alternative |
| --- | --- | --- | --- |
| 2.1 | LVL0 revision class: **major (2.0)**, since five prime directives change in reach and a doubtful class takes the higher one (STND.IDENT.4) | Major | Minor (1.9) |
| 2.2 | PRIME.8 counts a direction given through a person named under PRIME.11, within that naming's scope | Keep | Owner's direction only |
| 2.3 | A documentation change is neither code nor data, so it owes no floor tests (INTPR.2) | As drafted | Add "other than documentation alone" |
| 2.4 | A definition of done stated in the request also stands for the acceptance criteria | As drafted | Definition of done only |
| 2.5 | NUMER.5 (sentence 2), .7, .12, .23 (sentence 2), and .25 move to CSQ2, where STND.VVUQ's default methods for them start. A result lacking that evidence at CSQ3 is marked not assessed, or labeled unverified | Move | Keep them at CSQ3, met by "not assessed" plus the unverified label |
| 2.6 | NUMER.5 sentence 3, NUMER.23 sentence 1, NUMER.22, HW.QPU.6, and HDES.ASIC.5 are left as they are | As drafted | Move them too |
| 2.7 | The custodians record a `binding_reason` for STND.DOCS.10, STND.CXX.3, STND.PY.4, and STND.RUST.6 (GOV.19). No reason is recorded for the process-part instantiators of GOV.48, which govern agents, not form | Record | Make the four defaults from CSQ3 |
| 2.8 | CPS.1's minimum class reaches the *work* on such a system, not the whole project | Keep | Whole project |
| 2.9 | One scribe entry per direction (STND.DFLT.33), with no act of the owner | As drafted | The unit's plan record alone, under a custodian interpretation of GOV.36 |
| 2.10 | One acceptance entry per session that appended, and one confirmation per batch | As drafted | An acceptance entry after every append |
| 2.11 | "Provisions" includes starting the agent in an environment provided for that person (STND.DFLT.36 Notes) | As drafted | Presume the directing person alone |
| 2.12 | The signing of a commit is authorized once, through the new STND.PROJ.3 row | As drafted | Read the owner's signing configuration as the grant, which GOV.22 bars |
| 2.13 | INTPR.11 for agent actions applies from CSQ3 (STND.CLASS.10, row CSQ1) | CSQ3 | CSQ1 |
| 2.14 | Re-reading the ledger before relying on a standing grant is placed in STND.DFLT.17, so that STND.PROJ.2 carries it | As drafted | AGENT.17 |
| 2.15 | The agent shows a stated estimate's figure in its first message after the direction | As drafted | A ceiling the owner records once, above which an agent refers before it states an estimate |
| 2.16 | No new STND.PROJ.1 rows; STND.PROJ.2 carries STND.DFLT.36 and .37 instead | No change | Add rows, which raises what every constitution holds |
| 2.17 | AGENT.8 is unchanged, and the halt stays in PRIME.8 | As drafted | Restate the halt in AGENT.8 |
| 2.18 | A session that ends without its acceptance entry (a crash, a lost connection) leaves its own entries foreign, so the next session refers them for one confirmation. This errs on the safe side | As drafted | Let an agent accept its own earlier entries by their actor field, which a forger can write too |

---

## Part 3: residual risks, for the record

1. **A stated estimate is the agent's own figure.** Where nothing else bounds the cost, the agent derives the bound. PRIME.2 requires the estimate to be honest, and you see the figure at once (2.15). For a hard ceiling, set a spending limit or an envelope (GUARD.14).
2. **Isolation rests on your statement** (STND.DFLT.37). The agent cannot check it.
3. **The steps after a revocation** are the agent's judgment, bounded by GUARD.3: only those that leave the work safe and recoverable.
4. **A forger who writes before the accepted point,** in an agent's name, is not caught. The STND.DFLT.18 row marks this "No", and signatures close it.
5. **Explicit CSQ4 for hardware** (X14). An owner who records CSQ4 and leaves the CPS attribute false does not select CPS. PRIME.13, GOV.20, and STND.CLASS.2 still apply.
6. **GOV.20 narrows.** A project of CSQ2 to CSQ4 that releases software no longer needs a constitution. The release itself stays the owner's act (QA.10).

---

## After ratification

The lead, under step 8 of the standing process:
1. Applies `apply_audit_2026_10_31.py` to the live corpus. Then runs `verify`, `ledger check`, `compose --write`, and `compose --all ../rendered`.
2. Updates `docs/` and `README.md`, the three skills (P15), and `harness/README.md`, from the list in `reconciliation.md`, section 5, and the process record. This includes R11 as ruled.
3. Makes the v.10 harness unit for R6 (X7), with tests.
4. Updates `OPEN-ITEMS.md` and merges `audit-2026-10-31` into `main`.

## Ratification

The custodian, 2026-10-31, replied to this packet:

> Ratify as recommended

Every recommendation of Parts 1 and 2 is adopted: rulings R1 to R11 as recommended (R11 option (a)), and readings 2.1 to 2.18 as recommended (2.1: major, LVL0 2.0). The residual risks of Part 3 stand on the record.
