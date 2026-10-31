# Cleanup audit of 2026-10-31

## Scope and method

The audit covers the corpus at ledger entry 324 (commit 9b7d3b9), the harness package, the Claude Code plugin and its three skills, the documentation in `docs/`, and the repository around them. Four reviewers read in parallel, each read-only, on one slice: the constitution (LVL0 and the Lexicon); the documents an agent operates under day to day (AGENT, STND.DFLT, STND.CLASS, STND.PROJ, STND.INSTR, STND.WPROC, STND.WFLOW, STND.CREW, STND.THRT, STND.KNOW, and the skills); the LVL1 profiles and the technical LVL2 standards; and the harness code, plugin, and documentation. The coordinating session checked the repository and re-read the source text of each finding marked "confirmed" below, and reproduced S9 and S10 on copies. Each reviewer was asked for four kinds of finding: conditions that PRIME or GUARD prohibit, constructs that block work, burden on the human owner at CSQ3 and CSQ4, and inconsistencies and gaps. Out of scope by direction: the unadopted signature feature, the planned KNOW and TAG, the harness's lack of an enforcement layer, and offload annexes. The findings exclude what the rulings of 2026-10-28 already settled: the scribe route for the owner's acts (A3), instruction-file adoption (B1), and the development-branch exclusion from Main line.

State at the start: `verify` passes (3.8 s, only the expected g.18 warning). `compose --check`, `compose --all ../rendered --check`, `references --check`, and `manifests --check` are clean. The fast tests pass (48 in 13 s). The full suite passes in a full checkout (230 tests, 365 s). In a copy that holds only `harness/`, 2 tests fail (H13).

Severity: **High** means a compliant agent can reach a condition that PRIME or GUARD prohibits, or ordinary work cannot proceed. **Medium** means a real failure in a plausible case. **Low** means drift, wording, or a narrow case.

## Safety (S)

| ID | Sev. | Location | Evidence | Scenario | Fix direction | Ruling |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | High | GUARD.7 | "GUARD.5 does not apply to an action unless it belongs to a class the register records as exempt" (confirmed) | Read literally, GUARD.5 applies only to exempt classes, so every non-exempt destructive action leaves the PRIME.6 reservation. Only GUARD.5's own first sentence and GOV.9 rescue the intended reading. | "GUARD.5 does not apply to an action that belongs to a class …" | no |
| S2 | High | PRIME.13 against PRIME.6, .7, .8, GUARD.3, GOV.6 | PRIME.13: "An agent MAY command the designed safe state whenever it chooses". PRIME.7: actuation "only under a recorded authorization". PRIME.6 reserves actuation the hazard analysis "identifies as hazardous or irreversible". GUARD.3: safe-halt steps only "within its authority". | These provisions are of equal rank. GOV.6 hands the conflict to the more restrictive provision. Three ways it goes wrong: a monitoring agent with no actuation authorization halts and refers instead of commanding the safe state; an irreversible e-stop counts as reserved; an exhausted cost estimate halts work before the safe state is reached, although PRIME.13 says "halting NEVER leaves physical hardware outside it". | PRIME.13 states that commanding the designed safe state is never reserved, needs no authorization or estimate, and prevails over PRIME.6, .7, .8. | R2 |
| S3 | High | LEX.network-access against GUARD.13; LEX.bulk-retrieval against GUARD.8; LEX.reserved-action against PRIME.6 | LEX.network-access excludes everything "other than over the channel that carries the agent's own instructions". GUARD.13 includes "transfer through tools offered over the channel". LEX.bulk-retrieval drops "in whole" and the clause about retrieval that no authorization bounds. LEX reserves "hazardous or irreversible actuation" outright, while PRIME.6 reserves only what the hazard analysis identifies. (confirmed) | LEX/_doc says lower governance uses these terms "in exactly this sense". So a lower provision can treat server-side web tools as outside network access. Separately, an incomplete hazard analysis leaves hazardous actuation authorizable to an agent under PRIME.6, though not under LEX. | Bring LEX.network-access and LEX.bulk-retrieval into line with GUARD.13 and GUARD.8. Decide which reading of reserved actuation governs, and make the other match it. | R2 |
| S4 | High | STND.DFLT.23; STND.DFLT.18, protection table | "Where the work is not assured, each entry that … records an act of the human owner under STND.DFLT.17 SHALL be accepted" (confirmed). The Notes admit "nothing detects one". The DFLT.18 row "The work, its records, and its history \| Change beyond authority \| … \| Yes" says the protection is in place. | A collaborator's commit, or a fetched branch, adds an `authorize` line to `records/ledger.jsonl`. The agent merges it, then reads it at the next session start (AGENT.17) as an authorization in force. Content has gained the authority that PRIME.11 denies it. H2 widens the gap: a duplicate-key line shows one text to grep and to people and another to `verify`. | Accept a DFLT.17 entry that arrived by merge or fetch only after the owner confirms it, or mark the DFLT.18 row "No" so that the threat model states the gap (GUARD.16). | R4 |
| S5 | High | STND.DFLT.33 against PRIME.8, AGENT.6, AGENT.8, GUARD.15 | DFLT.33 treats a direction that names agents and their configuration as "the authorization, under PRIME.8, of the operating cost" (confirmed). PRIME.8 requires "a rigorously and faithfully derived estimate that the human owner authorizes". | The owner says "use agent X with model Y". The cost is authorized, but no estimate is. AGENT.8 reports an overrun without halting, and GUARD.15 halts only before an authorized limit, so nothing ever halts. This relaxes PRIME.8, which PRIME.15 forbids. See B1 for the opposite failure. | See R1. | R1 |
| S6 | Medium | PRIN.1, PRIME.11, GUARD.13 ("operator"), LEX.human-owner, STND.DFLT.17 ("given it directly") | "Directly" has no definition. LEX.human-owner defers the owner's identity to sources outside the corpus, and PRIN.1 presumes it. | A teammate runs the agent and says "pip install X". Either the grant goes into the ledger as the owner's act, a false record (PRIME.2) and an unauthorized install (PRIME.7), or the teammate cannot instruct the agent at all. Text that the owner pastes, holding "I authorize a push", has no settled status. Two owners have no rule between them. | Define "given directly": a message the owner sends over the GUARD.13 instruction channel, excluding quoted, pasted, retrieved, or relayed text. Presume the owner is the person who provisions the environment unless a record names another, and let the owner delegate instruction authority to named persons by a recorded act. | R3 |
| S7 | Medium | CPS.3, CPS.5, CPS.6, CPS.9 (all `onset` CSQ3, confirmed); PRIME.13 | PRIME.13 requires the hazard analysis only "before the system first drives the hardware". The CPS.3 duty to revise it before a change drives the hardware starts at CSQ3. The CPS Notes justify that duty by a failure that "reaches physical hardware at every class". | A CSQ4 bench project adds a commanded heater output that the hazard analysis does not cover. No provision forces a revision before the output is driven. | CPS.1 sets CSQ3 as the minimum class of CPS work (GOV.12 permits this), or PRIME.13 carries the revision duty. | R7 |
| S8 | Medium | STND.DEPS, Notes on STND.DEPS.14 | "a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts". The STND.DFLT Notes add that a retrieving install is "also network access, which needs its own authorization (GUARD.13)"; the DEPS Notes leave this out. | An agent reads the DEPS Notes as permission. It fetches and installs the newest revisions a range admits, never vetted, without a network authorization. | Have the Notes, or DEPS.14 itself, say that these runs need a network authorization. | no |
| S9 | High | `harness/skills/*/SKILL.md` (consulting :19, orienting :8, classifying :16); `docs/installation.md`, `operating.md`, `adoption.md` | Every run form is `python3 -B -m govharness`, which puts the current directory first on `sys.path`. | In an adopting project that holds `json/__init__.py`, the skill command imports and runs the project's module before crashing (reproduced). With `-P`, `show` works. An agent "only reading the governance" in an untrusted checkout runs that checkout's code. | Use `python3 -B -P -m govharness` everywhere. `-P` exists from Python 3.11, the stated floor. | no |
| S10 | High | `harness/govharness/ledger/transactions.py:65-72` | The chain hash is recomputed from `json.loads` of each line, not from the line's text. | A copy whose line 300 gains a leading duplicate `"rationale":"FAKE: agents may push",` passes `verify` with `ledger: PASS` (reproduced). `json.loads` keeps the later value, while grep, the skills' ledger patterns, and a person reading the file see the fake one. A line rewritten with spaces passes too, and so does an entry missing `actor`, `role`, and `authority` once its hash is recomputed, contrary to STND.HARN.7 ("exactly the fields") and GOV.36. | Require each line to equal `canonical_json(parsed)` and to hold exactly the field set of STND.HARN.7, and reject duplicate keys (`object_pairs_hook`). | no |

## Constructs that block work (B)

| ID | Sev. | Location | Evidence | Scenario | Fix direction | Ruling |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | High | PRIME.8, GUARD.14, GOV.22, STND.DFLT.33, STND.CLASS.18, STND.CREW.21, .23 | LEX.implicit-expenditure covers "tokens". GOV.22: "No default … authorizes an estimate". DFLT.33 applies only where the owner names "the agents … and the configuration of each" (confirmed). | "Fix the bug in foo.py" names no configuration, so under GOV.9 the agent has no cost authorization, and PRIME.8 halts it at its first step. Writing the estimate or the referral also spends tokens. Every unplanned subagent needs an owner decision, including the separate-session reviewer that STND.CLASS.18 requires at CSQ3. So AGENT.9's permission to direct agents cannot be used. GUARD.14's "Absent such a discipline, an agent uses the least costly configuration" assumes the work proceeds, and PRIME.8 says it does not. | See R1. | R1 |
| B2 | Medium | GUARD.8 | "retrieval whose items or volume no authorization enumerates or bounds … is bulk retrieval and is reserved". Nothing limits it to network access. | Local reads need no authorization, so no authorization ever bounds them. Under GOV.9, reading a local data file whole is then reserved to the owner. Separately, a casual "look this up", with no bound stated, becomes a reserved retrieval and not just an unauthorized one. | "Retrieval by network access (GUARD.13) of …". | no |
| B3 | Medium | GUARD.9 against GUARD.7; STND.DFLT.15 | "Before every permitted change to data or history, an agent confirms that a recoverable prior state exists." | Exempt classes such as temporary and regenerable items have no recoverable prior state by definition. A file the agent created this unit and has not yet committed has none either, so editing it again is irrecoverable and reserved. The first class of DFLT.15 needs a "last committed state". | Exempt the GUARD.7 classes from GUARD.9, and add to DFLT.15 a default class for items that the agent created in the current unit of work. | no |
| B4 | Medium | STND.DFLT, term Working bounds and its Notes; GOV.51; STND.DFLT.25 | The bounds leave out "each location that holds secrets or credentials", and the Notes name the key directories of secure-shell and privacy-guard tools. | In a repository with signed commits, every `git commit` reads the privacy-guard home, so it halts. `git push` over secure shell reads its configuration and known hosts, so it halts even after the owner says "push it". The grant opens no credential location. | An authorization of a network access or a commit covers its tool's use of the credential means the environment provides, without the agent reading the secret. | R10 |
| B5 | Medium | PRIME.9 | "NEVER acquires, escalates to, or uses elevated privilege, superuser privilege included, even within an isolated environment" | An agent provisioned as root in a container, a common default, uses superuser privilege with every action, so it can do nothing. | Bar acquiring or escalating to privilege beyond what was provisioned, and require the owner's provisioning to be the only route to superuser privilege. | R8 |
| B6 | Medium | GOV.10 floor, QA.1, VV.7, STND.DFLT.7 | The floor holds "a definition of done for each unit of work (QA.1)" and "tests for basic correctness and regressions (VV.7)". QA.1 reaches every "task, subtask", and DFLT.7 has it "committed". | Read-only investigation, a question answered, and a documentation change have nothing to test, so the requirement cannot be met. At CSQ4 every subtask also needs a committed definition of done. | Limit VV.7 at the floor to changes of code or data, and let a definition of done stated in the request count. | R9 |
| B7 | Medium | STND.IDENT.23; STND.PROJ template | "The custodians SHALL register each mnemonic, including the mnemonic of each project" (confirmed) | A downstream project needs a constitution to release (GOV.20). It cannot have one until the custodians of this corpus register its mnemonic, a decision LVL0 does not assign to its owner and that the owner cannot make. | Let the human owner register a project's mnemonic in the project's own records, and keep the corpus register for the corpus. | R6 |
| B8 | Medium | STND.CXX.3 against STND.CXX.2 and STND.STDC.3 | CXX.3's exception lists "the compiler, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain" but not "the dependency", which STDC.3 lists (confirmed). CXX.3 binds at every class. | A third-party header fails to compile at the newest edition. No decision record allows the agent to lower the edition, even at CSQ4, so it halts and refers. | Add "the dependency" to both sentences of CXX.3 and to the exception of CXX.2. | no |
| B9 | Low | STND.WPROC.12; term Main line | Every advance of a main line needs an owner decision to release. In a fresh project, no record says whether the default branch is a branch "from which the work is released or deployed". | GUARD.2 puts the advance in the highest tier, so every bug fix ends with an owner merge decision. | Absent a record, the default branch is not a main line until the owner records otherwise. | no |
| B10 | Low | GUARD.1 | The free tier covers only actions "that its instructions call for". | Under GOV.9, a routine step that the instructions do not name, such as reading a neighboring file or running a linter, falls into the catch-all that needs authorization. | "… that its instructions call for or that the unit of work they direct needs". | no |

## Burden on the human owner (O)

| ID | Sev. | Location | Evidence | Scenario | Fix direction | Ruling |
| --- | --- | --- | --- | --- | --- | --- |
| O1 | Medium | GOV.13, GOV.22, QA.11, LEX.reported-result; STND.CLASS.19 | "No class is assumed by default" (confirmed). The agent is the result's author, so handing a result to the owner for reliance takes it "beyond its author". | Routine work does not halt. The first result the owner relies on does halt, until the owner states a classification, selector attributes included; under the 2026-10-28 scribe route, one chat message does it. STND.CLASS.19 has no audit interval for an unclassified project. | Presume CSQ4 until a class is recorded, or count delivery to the directing owner as not "beyond its author". | R5 |
| O2 | Medium | GOV.20; LEX.release; GOV.42 | A project constitution is required of every project that "releases software" (confirmed), at any class. | A CSQ4 utility published once needs a full LVL3 constitution covering the fourteen mechanisms of GOV.21. GOV.42 then has the owner re-conform it at every change the custodians make. | Let a release under the defaults be an owner act, and require a constitution only at CSQ1 and CSQ0, or on request. | R5 |
| O3 | Medium | NUMER.5, .7, .12, .23, .25 (`onset` CSQ3); STND.VVUQ.20 to .44 (CSQ2); STND.VVUQ Notes | The NUMER Notes say each provision "costs one statement, one record, or one message". The VVUQ Notes say "work of CSQ3 meets NUMER through the core". The CSQ3 core covers none of NUMER.7, .12, .13, .23, or .25. | An internal fit with error bars at CSQ3 owes a rounding-error bound under conditioning, convergence evidence for its sample uncertainty, and stated false-rejection and detection probabilities, with no default method to follow below CSQ2. The HW selector is true for anything run on a CPU, so ordinary analysis work also selects NUMER. | Move these parts to CSQ2, or let "not assessed" plus the unverified label (PRIME.3) meet them at CSQ3. Correct the VVUQ Notes either way. | no |
| O4 | Medium | `onset` command; skills consulting-governance :65 and classifying-work :34 | "What does reclassification to CSQn add? \| `onset ROOT CSQn`". The list is not cumulative (CSQ0: 6 lines, CSQ1: 26, CSQ2: 161, CSQ3: 622; confirmed), and it leaves out the rows of the STND.CLASS.10 table, the human review of STND.CLASS.18, and the audit of STND.CLASS.19. | A move from CSQ4 to CSQ1 shows 26 items, and the rest is missed. | Make `onset` take the current class and list everything between it and the new one, with the CLASS.10 rows, or reword both skills. | no |
| O5 | Medium | STND.PROJ.2 and Notes; STND.DFLT.1 | A constitution that cites STND.DFLT takes in DFLT.2 to 12, 14, 15, 18 to 22, 24, 27 to 31, and 35, but not 13, 16, 17, 23, 25, 26, 32, 33, or 34. DFLT.1 then stops the defaults from applying. | An owner who adopts a constitution in order to release keeps the halt of DFLT.35 but loses the build-and-test permission of DFLT.34, the scribe route of DFLT.17, and the cost route of DFLT.33. PRIME.8 then halts unless the owner adopts PROJ.5. | Carry DFLT.34 into Reserved actions, and DFLT.16, .17, .32, .33 into Authorizations. | no |
| O6 | Low | STND.INSTR.11 | An unadopted instruction file is "content without instruction authority". Adoption names a revision or a digest. | The owner's own `CLAUDE.md` line "do not edit vendor/" carries no weight until a ledger entry adopts it, and every edit needs re-adoption. | Let an agent honor a restriction in an unadopted instruction file as the more restrictive reading. Only grants of authority need adoption. | no |
| O7 | Low | STND.DFLT.23, Assured work; STND.CLASS.22; STND.DFLT.20 | Once the work is assured, only signed entries are accepted. | When the signer register lists the owner's key, every earlier unsigned grant, instruction-file adoption, and cost direction stops counting, even mid-action, and no referral says so. This matters only once signatures are adopted. | Say so in STND.CLASS.22 and in the DFLT.20 referral, and list the entries to re-sign. | no |

## Inconsistencies and gaps (I)

| ID | Sev. | Location | Evidence and fix direction |
| --- | --- | --- | --- |
| I1 | Medium | GUARD.10, AGENT.17, STND.DFLT.17 | Authorizations have no revocation rule at LVL0, and no rule for expiry or revocation in mid-action. AGENT.17 reads the authorizations in force only before the session's first change, so a revocation entered from a parallel session goes unseen. DFLT.17 lets an agent rely on a grant given "in its current session" without saying when it must be entered; after compaction the grant survives only in the agent's own summary. Fix: revocation in GUARD.10; enter a grant before first relying on it; re-read the ledger before each action that relies on a standing grant; after expiry, permit the steps that leave the work safe and recoverable. |
| I2 | Medium | STND.CODE.30 against STND.VVUQ.82, .83 | CODE.30: a reported result "SHOULD be independent of that order", with no tolerance. Against the determinism direction, it reads as the provision that VVUQ.82 excepts, one requiring bitwise identity. Fix: "independent of that order, or its dependence declared as run-to-run variation (REPRO.3) and within the tolerance of its comparison", following STND.BUILD.15. |
| I3 | Low | GOV.14 against GOV.13, GOV.50; QA.11 | GOV.14: the class "moves toward CSQ0 whenever reliance or exposure grows", which reads as automatic, while only the owner sets the class. It is unclear whether QA.11's "work of CSQ3 or CSQ4" means the recorded class or the actual one. Fix: the recorded class governs until the owner reclassifies. |
| I4 | Low | PRIME.14 against GOV.13 | PRIME.14 halts "when a consequence class it needs is not recorded", which is wider than GOV.13's four cases (promote, release, deploy, drive hardware). Fix: cite GOV.13's list. |
| I5 | Low | GOV.48 against GOV.10, GOV.11 | GOV.48 binds agents to INTPR.11 "for every action". GOV.10 and GOV.11 make INTPR proportioned above the floor. Fix: make GOV.48 agree with the floor. |
| I6 | Low | STND.RUST.6, STND.DOCS.10; GOV.19 | Both instantiate GOV.48, so both bind at CSQ4, with `binding_reason: null` (confirmed) and no ruling. The RUST Notes admit as much. GOV.19 makes a provision of form a default unless the reason is recorded, and all five GOV.48 provisions lack `binding_reason`. Fix: record the reasons, or make them defaults from CSQ3. |
| I7 | Low | ML, term Learned model use | Taken literally, the agent's own model meets the term. The exclusion is only in informative Selector text. Fix: move the exclusion into the term or into ML.1. |
| I8 | Low | `harness/skills/orienting-to-governance/SKILL.md` | "An authorization states its scope, duration, and the agents to which it extends (STND.DFLT.16, GUARD.12)". The field for the agents is in STND.DFLT.32. Fix: cite DFLT.32. |
| I9 | Low | STND.DFLT.5 | The rule fixes "the SHA-256 hash of the previous entry" but not the serialization the hash covers, so a hand-built work ledger can disagree with STND.HARN. Fix: cite the serialization of STND.HARN.6, or state it. |

## Harness, plugin, and documentation (H)

None of these needs a ruling except H12. Each is a harness unit with a test.

| ID | Sev. | Location | Evidence and fix direction |
| --- | --- | --- | --- |
| H1 | Medium | `harness/govharness/derive/reading_copy.py:244-247` | The composer always writes `{mode}. Instantiates {list}.`, so every LVL0 provision in `rendered/` reads ". Instantiates ." (186 lines across 11 files), and 57 provisions without a mode, in 15 files, read ". Instantiates GOV.25, GOV.26." and the like. `compose --check` cannot catch this, since it compares against the same output. Fix: write only the parts that exist, test a LVL0 provision and a provision without a mode, and rebuild `rendered/`. |
| H2 | High | `ledger/transactions.py:65-72` | S10. |
| H3 | High | skills, docs | S9. |
| H4 | Medium | `docs/adoption.md:18`; `ledger/chain.py:175` | `ledger append --ledger-file records/ledger.jsonl` without `records/` ends in an uncaught `FileNotFoundError`. Fix: exit 2 with a message, and have the step say `mkdir records`. |
| H5 | Medium | `verify`, `sign check` | The harness cannot check a project's work ledger. `sign check` demands SIGNR, and `verify` reads only the corpus ledger. Fix: a read-only `verify --ledger-file PATH` that checks the chain, or the manual check documented in `adoption.md`. |
| H6 | Medium | `checks/manifests.py:28` | With the manifests check made always PASS, the full suite still passes (230 tests). Fix: a test that a stale or missing `MANIFEST.csv` fails `verify`. |
| H7 | Low | `cli/main.py:263` | `find ROOT --in-force remote` and `context remote --in-force write` exit 2, "unrecognized arguments". Fix: `parse_intermixed_args`. |
| H8 | Low | `cli/query.py:58` and following | `--limit 0` reports "no item holds a word", which is false. `--limit -2` drops two matches. A negative `--budget` is accepted. Fix: limit at least 1, budget at least 0. |
| H9 | Low | `query/retrieval.py:65` | `WORD_RE` is `[a-z0-9]`, so "naïve" matches nothing and "ünïcødé" splits into single letters. Fix: `\w`. |
| H10 | Low | `cli/reports.py:194` | `check ROOT --out-dir ROOT/report` writes three files into the corpus, and `verify` then exits 2. Fix: refuse it, as `--cache` already is. |
| H11 | Low | `docs/installation.md:376-383` | The AGENTS.md snippet names a vendored corpus path but gives `govharness show ID`, which fails when the package is not installed and `GOVHARNESS_ROOT` is unset. Fix: give the `PYTHONPATH=… python3 -B -P -m govharness show <path> ID` form. |
| H12 | Medium | `docs/adoption.md:13` and step 5; STND.DFLT.17 | The docs say "An agent can enter it for you", but no document says how. The plugin gives the agent no write path, by design, so an agent would compute a hash-chained line by hand, which H5 then leaves unchecked. Ruling R11. |
| H13 | Low | drift | `docs/README.md:12` promises a "known limitations" section that `adoption.md` lacks. `docs/installation.md:231` leaves `onset` out of the commands that read `GOVHARNESS_ROOT`. `harness/README.md:118` says "g.1 to g.24", but the code also has g.0. The fast subset is said to take "about ten seconds" and takes 13. `--help` shows "(unit 0022)" and "(unit 0023)", process references in user-facing text. `test_references.LiveCorpus` needs `../tools/check_refs.py`, and the rendered-copies test needs `../rendered`; both fail in an installed plugin. Fix: skip them when those files are absent. |

## Repository (R)

| ID | Sev. | Location | Evidence and fix direction |
| --- | --- | --- | --- |
| RP1 | Low | `review-records/review-records-ledger100-105.tar.xz`, `review-records-ledger106-109.tar.xz` | Archive copies committed under the old "archive first" rule. The cleanup direction of 2026-10-24 keeps no archive copies, and git history holds both. Fix: delete them. |

## Rulings for the custodian

Each ruling below changes LVL0 or decides the shape of a mechanism. Every other finding is a drafting fix that needs only ratification.

**R1. Operating cost (S5, B1).** Under PRIME.8, a plain task authorizes no cost, so work halts. Meanwhile DFLT.33 authorizes cost with no bound once the owner names the agents.
- (a) In PRIME.8: the owner's direction of work, in the configuration the owner provisioned, authorizes that work's operating cost within any enforced cap or envelope. An estimate is required only where the cost can be measured, and is reported when it is exceeded.
- (b) Keep PRIME.8. Have DFLT.33 cover a bare direction in the agent's current configuration and its AGENT.10 delegates, up to a default envelope that the direction states or accepts.
- (c) Leave both as they are.

*Recommendation: (a).* It removes the halt on every task and closes the unbounded case. A provisioned cap stays the hard limit. It amends a prime directive, which is the owner's act.

**R2. Physical safety at LVL0 (S2, S3).** Should commanding the designed safe state prevail over PRIME.6, .7, and .8? And should every hazardous or irreversible actuation be reserved (the LEX reading), or only what the hazard analysis identifies (the PRIME.6 reading)?

*Recommendation:* yes, the safe state prevails. On the second question, keep PRIME.6's reading, since only an adopted analysis makes "hazardous" decidable, and make LEX match it. Pair that with S7 (R7), so that the analysis cannot go stale.

**R3. Who instructs and who is the owner (S6).**
- (a) Define "given directly". Presume the owner is the person who provisions the environment. Let the owner name delegates by a recorded act.
- (b) Define "given directly" only.

*Recommendation: (a).*

**R4. Ledger entries that arrive by merge or fetch (S4).**
- (a) Accept an act of the owner that arrived from outside the session only after the owner confirms it.
- (b) Accept it, and record the gap honestly in the DFLT.18 table.

*Recommendation: (a).* It costs one confirmation per foreign grant, and it closes an injection route to authority.

**R5. Default class and releases (O1, O2).**
- (a) Presume CSQ4 until a class is recorded, and require a constitution only at CSQ1 and CSQ0, or on request.
- (b) Keep "no default class", and require a constitution only for releases at CSQ2 or above.
- (c) Leave both as they are.

*Recommendation: (a).* It matches the low-ceremony default. GOV.22's "No default … sets a consequence class" would need the same amendment.

**R6. Project mnemonics (B7).** Should the owner register a project's mnemonic in the project's own records, without a custodian act? *Recommendation: yes.*

**R7. CPS minimum class (S7).**
- (a) CPS.1 sets CSQ3 as the minimum class of work that the CPS profile selects.
- (b) PRIME.13 carries the revision duty at every class.

*Recommendation: (a).* It needs no LVL0 change.

**R8. Superuser privilege in a provisioned environment (B5).** Should an agent that the owner provisioned with superuser privilege inside an isolated environment be able to act? *Recommendation: yes. Bar acquiring or escalating privilege, not using what was provisioned.*

**R9. The floor for work with nothing to test (B6).** Limit VV.7 at the floor to changes of code or data, and accept a definition of done stated in the request? *Recommendation: yes.*

**R10. Credential means under an authorization (B4).** Should an authorization of a push or a signed commit cover its tool's use of the credential means the environment provides, without the agent reading the secret? *Recommendation: yes.*

**R11. How an agent enters a scribe entry (H12).**
- (a) Document `govharness ledger append --ledger-file records/ledger.jsonl` as the route for a project's work ledger. The corpus stays unwritable through the plugin.
- (b) Document the line format, and have agents compute entries by hand.
- (c) Remove the promise from the docs.

*Recommendation: (a), together with H5.* (b) brings hand-computed hashes that nothing checks.

## Checked and sound

- **Instruction authority.** Content, the knowledge base, and notes carry none (PRIME.11, GOV.32, INTPR.5).
- **Circumvention.** Decomposition, delegation, and the channel's tools are closed (PRIME.12).
- **No self-grant.** An agent cannot grant itself, or widen by delegation (PRIME.7, GUARD.12, GOV.49).
- **Irrevocable writes.** These need a per-action authorization (GUARD.11). History rewrites are in no exempt class, and GUARD.6 prevails over every exemption.
- **Incidental secrets.** PRIME.10 handles them soundly.
- **Physical harm.** It is never an agent's determination (GOV.15).
- **Tighten-only.** It holds, along with inherited non-waivability (PRIME.15, GOV.17; checks l.1 to l.5 pass).
- **Default mechanisms.** The defaults supply every GOV.21 mechanism, and routine edit, test, and commit work does not halt for want of a class.
- **Owner availability.** AGENT.15 keeps other lines of work going while the owner is away, and STND.CREW.2 batches the owner's decisions.
- **Agnosticism.** None of the 721 provision bodies in the profiles and technical standards names a vendor, product, tool version, or recommended configuration. Notes name tools only to explain a hazard. STND.OFFLD names no framework.
- **Shared matters.** No matter has two owners.
- **Newest-edition rule.** It stays confined to STND.CXX.2.
- **Determinism and races.** Determinism matches the direction everywhere except STND.CODE.30 (I2), and races are treated as defects.
- **The plugin.** It has no hooks, commands, agents, MCP configuration, settings, or `allowed-tools`. No skill tells an agent to write. Every `show` target in the skills resolves.
- **Read-only commands.** They write nothing, and the solve cache is opt-in, with unsafe locations refused.
- **Exit codes.** They match the documentation.
- **Tamper detection.** Edits, cut tails, and unpinned files are caught. The manual checks in steps 4 and 5 of `harness/README.md` reproduce the ledger hashes.
- **Query robustness.** `show` handles all 1442 identifiers without a crash.
