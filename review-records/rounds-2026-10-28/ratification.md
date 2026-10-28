# Rounds of 2026-10-28: ratification packet

This packet asks the custodian for every decision the five rounds need before they are applied. The rounds carry the rulings of 2026-10-28 on the deep review ([rulings](../deep-review-2026-10-28/rulings.md), last section).

## What is being ratified

| Round | Carries | Transactions | Record |
| --- | --- | --- | --- |
| a | A1 to A5, B1, B2: defaults, operating cost, installs, write bounds, instruction authority, memory store | 6 | [round-a](round-a/decisions.md) |
| d | D1 and the language and systems entries: one provision per outcome across languages | 15 | [round-d](round-d/decisions.md) |
| c | C1 to C8: classes, the expected class, promotion, review independence | 21 | [round-c](round-c/decisions.md) |
| o | C7 and the register's onset entries: the field `onset` (unit 0023) | 43 | [round-o](round-o/decisions.md) |
| e | E1 and the rest: the harness's place, review pairs (unit 0024), withdrawals | 35 | [round-e](round-e/decisions.md) |

There are 120 ledger transactions, entries 203 to 322.

Each round was drafted, cold-reviewed and fixed, then verified. A reconciliation review then read the five together ([reconciliation](reconciliation.md)). Its findings are fixed and [verified](reconciliation-verify.md). The verification's one new finding, which moved c.5 from a Note into the row of STND.CLASS.19, is fixed as it proposed.

The applied corpus passes every check, with only the standing g.18 warning. The onset counts are CSQ0 2, CSQ1 22, CSQ2 157, CSQ3 618.

**The net burden, after all five rounds:**
- No act of the human owner is added at CSQ3 or CSQ4 beyond what the rulings ask.
- No blocker, circular requirement or undefined term was found.
- No floor is raised without a recorded decision, and no binding provision is lowered.

## How to answer

Each item below is drafted as recommended. A reply of **"ratify as recommended"** adopts every recommendation. To depart from one, name it, for example "a.3 option (b)". The script is then changed and re-rehearsed before it is applied.

Part 1 holds the readings that bind widely or change ratified text. Part 2 holds readings that are narrow or that confirm a drafting choice.

---

## Part 0: confirmations of the rulings and the process

**0.1 The readings of A1, A2 and B2.** The rounds drafted the rulings on these readings (rulings.md, last section):
- **A1:** your direction of a unit of work, naming or accepting the agents and their configuration, authorizes its operating cost. A standing envelope or an adopted cap still governs where one exists.
- **A2:** a build, an install or a test run is permitted when it is:
  - within the working bounds;
  - against the configuration that the work records under version control, or otherwise authorized.

  Installing a package that the recorded configuration doesn't name, or a build or test run beyond the working bounds, halts and is referred.
- **B2:** the memory store is a defined term (Tool memory store), with fixed conditions, so every reader applies it alike.

Recommendation: confirm.

**0.2 The order of the rounds.** Ruling F2 set the order: classes and promotion (C), then the language standards (D). The driver applies d before c instead, because round c's edits to STND.CODE and the language standards are anchored on round d's text. The result is the same single packet. Recommendation: accept the order a, d, c, o, e.

---

## Part 1: readings that bind widely or change ratified text

**a.1 What "installs" means in PRIME.7.**
- *Context:* ruling A2 permits installs against the stated configuration. PRIME.7 reserves "installs software or dependencies". The two meet only if PRIME.7's words mean adding something new, not reproducing the recorded set.
- *Drafted:* an interpretation of PRIME.7 under GOV.3, recorded as one `rule` transaction (entry 204). An install of the recorded set is not an install under PRIME.7; adding a package or a source still is (STND.DFLT.35). It binds every project.
- *Options:*
  - (a) adopt the interpretation;
  - (b) read PRIME.7 strictly, so every install needs an authorization (STND.PROJ.3) and STND.DFLT.34 covers only builds and test runs.
- *Recommendation:* (a). It is what the ruling's words give. Under (b), every fresh checkout's install is a referral.

**a.3 What adopting an instruction file binds (B1).**
- *Context:* an instruction file (CLAUDE.md, a skill and the like) directs agents only once you adopt it.
- *Drafted:* adoption names the path *and* the content, as a revision or a digest. An edit by anyone else has authority only after you adopt the new content, at one adoption per change of the file.
- *Options:*
  - (a) path and content;
  - (b) the path alone, so a later edit by another person inherits your authority.
- *Recommendation:* (a). Option (b) is the objection the rulings raised.

**c.1 Defining "team" (C5).**
- *Context:* GOV.12 and QA.11 turn on "the immediate team" without defining it. Its width decides how often work must be promoted.
- *Drafted:* a team is the actors acting on the work under the direction of its human owner. A larger project with several groups under one owner is one team.
- *Options:*
  - (a) define it;
  - (b) leave it undefined, as GOV.12 does.
- *Recommendation:* (a).

**c.2 The two design-for-upgrade defaults at CSQ4 (C2, C4).**
- *Context:* STND.CLASS.21 (design anticipates the expected class) and the records of STND.CLASS.23 exist for work that records an expected class.
- *Drafted:* work of CSQ4 still meets both, but only where an expected class is recorded. Your entry of that class is the decision GOV.11 asks for.
- *Options:*
  - (a) both at CSQ4 where an expected class is recorded;
  - (b) STND.CLASS.21 from CSQ3 only, and the records alone at CSQ4.
- *Recommendation:* (a). A design-for-upgrade default that CSQ4 omits does nothing for work that starts at CSQ4. Without an expected class, nothing changes.

**c.3 The onset of STND.CODE.20 (C2 asks your confirmation).**
- *Drafted:* the deviation record starts from CSQ1, and the marker that lets it be found starts earlier, at CSQ3. This revisits the onset ratified for C++ (STND.CXX 1.1) and C (STND.STDC.1).
- *Recommendation:* confirm.

**o.1 Where the field `onset` keeps a ratified onset against the new rule.**
- *Context:* round o's rule gives each default the class of its row in STND.CLASS.10, or CSQ3. Some forty provisions and parts had ratified onsets that are less strict. Examples: reports to the operator at CSQ3, the cores of HW and NUMER, and the C++ checks STND.CXX.24, .26 and .27 (this also settles e.6).
- *Options:*
  - (a) keep each ratified onset, with its reason in the Notes;
  - (b) apply the rule strictly, moving those parts to CSQ2, CSQ1 or CSQ0.
- *Recommendation:* (a). It changes no onset the rulings didn't name, and (b) would make CSQ3 work heavier.

**o.2 Moves to CSQ3 beyond the review's lists.**
- *Context:* nine rules of code form (in STND.CODE, CONC, MPI, OFFLD and OMP) and three protocol rules (STND.CREW.11, STND.WPROC.7 and .8) ask for no schema, contract or invariant verification.
- *Drafted:* all twelve move from CSQ2 to CSQ3.
- *Options:*
  - (a) move them;
  - (b) keep them at CSQ2, each with a reason.
- *Recommendation:* (a). Parts that carry out a CSQ2 hardware provision or rely on a hardware contract stay at CSQ2.

**e.1 What a change confirms before it is applied (STND.HARN.24).**
- *Context:* the old text required the outcome a rehearsal confirms. The rulings make the harness optional, so the text names an outcome instead.
- *Drafted:* the actor confirms each property whose absence a check of a harness meeting STND.HARN reports as FAIL, as that harness's documentation states it. This keeps every check: defaults, logic checks and onsets. A change applied where no harness exists owes nothing here.
- *Options:*
  - (a) as drafted;
  - (b) only the properties that provisions name in `checked_by`, which drops the default, logic and onset checks and lowers a binding provision;
  - (c) the reviewer's corpus-only text, which asks something even with no harness but loses the logic checks.
- *Recommendation:* (a). Choose (c) if an outcome that holds without any harness weighs more than the logic checks.

**e.2 Review pairs counted by amended provision (E1).**
- *Context:* STND.HARN.28 puts pairs of provisions to review before a change.
- *Drafted:* a pair holds at least one provision the change adopts or amends. A pair on a shared LVL0 provision needs both provisions in touched documents. A change of the Notes alone pairs nothing. This round lists 44 pairs.
- *Options:*
  - (a) as drafted;
  - (b) every provision of every touched document, which gives 6,763 pairs for this round.
- *Recommendation:* (a). The two agree for a single new document; NUMER gives 92 pairs under either.

**e.3 How often a declared dependency range is checked (CL7, put to you by round d).**
- *Drafted:* the checks at the oldest and newest revisions a declared range admits run at each release, under one default in STND.DEPS for every language. The newest-revision check is a SHOULD.
- *Costs:*
  - Rust and Julia move from each change to each release. Python gains the SHOULD.
  - Under round a's write bounds, scheduling the check is your setting to make. So the SHOULD costs a project one act of yours, or one recorded decision to replace the default.
- *Options:*
  - (a) each release, SHOULD;
  - (b) the same, worded "at each release, or at each change where the configuration states it";
  - (c) each release, with CL7's MAY, which costs no act.
- *Recommendation:* (a): one rule, at the point where dependents rely on the range. Choose (c) if one act per Python project is too much.

---

## Part 2: narrow readings and drafting choices

Each is drafted as recommended. The full text is in the round's record.

| Item | Question | Recommended (drafted) | Alternative |
| --- | --- | --- | --- |
| a.2 | GUARD.5 and uncommitted edits | The last commit is the recoverable state of a file that differs only by the agent's own edits in this unit; other uncommitted changes stay protected | Each successive edit is a reserved overwrite |
| a.4 | Unadopted instruction files | Named once in the completion report; a passage directing a forbidden or reserved action is still reported at once | Reported passage by passage |
| a.5 | When STND.DFLT.19 halts | Only where the threat table doesn't already name the asset with that threat, so no write halts twice | Halt whenever the table omits the asset |
| c.4 | The basis of an estimate in AGENT.39 | "An effort estimate in the form of AGENT.6 that states its basis" | Cite STND.CREW.7 from AGENT, so an LVL1 provision cites LVL2 |
| c.5 | The agent auditor of STND.CLASS.19 at CSQ1 and CSQ2 | The row asks another model or instruction revision, whatever its tools, as C6 asks of a CSQ2 reviewer; it reaches no CSQ3 or CSQ4 work | Keep the bare term, so a difference of tools alone qualifies |
| o.3 | Completion arguments (STND.MPI.12 s2, STND.CONC.11 s1) | Both at CSQ3; the deadlock tests stay at CSQ2 | Both at CSQ2 |
| o.4 | The VVUQ core | At CSQ3, STND.VVUQ.64 judges fresh-seed tests by the acceptance criterion | Add STND.VVUQ.33 to the core (one field) |
| e.4 | Execution paths (CS9) | Recorded where the Architecture section names, so a new hardware type needs no decision of yours | Keep them in the classification |
| e.5 | Build scripts of Rust dependencies (CL9) | Review each added dependency's build script; a changed one is reviewed with its pinned revision (STND.DEPS.4) | Review every build script a lock-file change adds or alters |
| d.1a | "Elsewhere a default" (D1, finite values) | The annotation only, which adds no reach | A new default for every floating-point check |
| d.4a | Unstable hash values and orders (STND.CODE.30) | Reach C, C++, Rust, Fortran and Lean too, as a default from CSQ3 | Python and Julia only |
| d.6a | STND.LEAN.1 | Keep; it also pins the toolchain and checkers for proof work | Reduce it, as CL8 proposed |
| d.7a | Static checks for Rust (STND.CODE.32) | Only checks among the work's means | Any check able to decide |
| d.10a | Documents named in provisions (CL14) | The Julia manual's style guide, the Python typing specification and the OpenMP specification stay named, as part of the definition of the language or model; the third-party guides move to the repository configuration | Move these three to the configuration too |
| d.13a | QA.12 in STND.PERF.18 | In `refers_to`, not `instantiates` | Instantiate it |
| d.14a | Offload tests (STND.OFFLD.27) | May serve as STND.CONC.24's tests across task counts | No relaxation |
| d.18 | Lowering the language edition (CL24): binding in C++ (STND.CXX.3), a default in C (STND.STDC.3) | Leave the two modes; the C++ rule rests on the newest-edition rule of STND.CXX.2, which C lacks | Make STND.STDC.3 bind as STND.CXX.3 does |

Settled by later rounds, so not asked: d.7b (round o replaced the onset paragraph) and d.17a (CL21 is wholly round c's). e.6 is answered by o.1.

---

## Not carried, for the record

- **CC23 and CC24's parts in PRIME.1, PRIME.7 and PRIME.14:** they would change prime directives.
- **LEX.standard's "which may name tools and methods":** it is LVL0, outside the brief, and conflicts with nothing.
- **CP26 (STND.CREW.14), and CC25 (STND.CLASS.20 and STND.DFLT.13):** outside the brief, and not copies.

## After ratification

The lead:
1. applies the driver to the live corpus;
2. rebuilds the reading copies;
3. updates the README counts, OPEN-ITEMS and docs/adoption.md "Known limitations";
4. runs the full tests;
5. merges `rounds-2026-10-28` to main and tags `ledger-322` locally.

Nothing is pushed (F3).

## Ratification

The custodian, 2026-10-28: "proceed in full as recommended".

Every item of Parts 0, 1, and 2 is ratified as recommended: the readings of A1, A2, and B2 are confirmed, the order a, d, c, o, e is accepted, and each reading takes its recommended option, so the rounds are applied as drafted.
