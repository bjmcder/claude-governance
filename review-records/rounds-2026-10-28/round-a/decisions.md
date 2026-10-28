# Round a of 2026-10-28: the defaults and the agent instructions

This round carries rulings A1 to A5, B1, and B2 of `review-records/deep-review-2026-10-28/rulings.md`, each on the reading given in its section "Rulings of the custodian, 2026-10-28", and the register entries R1.4 to R1.7, AD5, and R5.4, with CC14, CC21, and CP18. The module is `tools/amendment-scripts/apply_round_a_2026_10_28.py`, run through `apply_rounds_2026_10_28.py`. Five transactions, in citation order: STND.DFLT 1.6, STND.INSTR 1.5, AGENT 1.2, STND.PROJ 1.3, STND.HARN 1.6. The round was reviewed cold (`review.md`), revised, verified cold (`verify.md`), and revised again; the section "Review and dispositions" gives each finding's fate. Nothing here is in force until the custodian ratifies it and the script runs.

## Rulings carried

### A1. Operating cost

**Reading drafted.** The human owner's direction of work, naming, or accepting a plan that names, the agents and the configuration of each, authorizes the operating cost of the units it covers (PRIME.8); the agent enters the direction by the scribe route of A3; an operating envelope stays available, and a cap under STND.DFLT.26 still governs where one exists. PRIME.8 and GUARD.14 are unchanged.

**New STND.DFLT.33, Operating-cost authorization (binding: GOV.22, GOV.36, GUARD.14, PRIME.8):**

> Where the human owner directs work and names, or accepts a plan that names, the agents that carry it out and the configuration of each, an agent SHALL rely on that direction as the authorization, under PRIME.8, of the operating cost of each unit of work that the direction covers, in that configuration and within each operating envelope that an entry that STND.DFLT.23 accepts adopts (GOV.22, GUARD.14, PRIME.8). An agent SHALL enter that direction as an authorization under STND.DFLT.17 (GOV.22, GOV.36).

**The STND.DFLT Note** "Without a cap adopted under STND.DFLT.26, PRIME.8 requires an authorized estimate." now reads that the direction of STND.DFLT.33 is the authorization of PRIME.8 for the units it covers, that the estimate of AGENT.6, where the cost is measurable, is the one monitored (GUARD.14), that a cap under STND.DFLT.26 bounds it where one exists, that the direction is the human owner's own act so no default authorizes an estimate (GOV.22), and that acceptance is never implied (PRIME.7). The Purpose adds that STND.DFLT.33 names the act of the human owner that authorizes the cost. The AGENT Note on AGENT.6 says that the direction authorizes the cost of the units it covers and that an estimate under AGENT.6 is authorized only where the direction accepts the plan that states it.

**Why GOV.22 is kept and PRIME.8 and GUARD.14 are not amended.** GOV.22 bars a default from authorizing an estimate. STND.DFLT.33 authorizes nothing: it names the act, the human owner's direction, that is the authorization, and has the agent rely on it and record it, as STND.DFLT.17 already does for a grant given directly in session. PRIME.8's "estimate that the human owner authorizes" is met by the estimate the plan states under AGENT.6, where the cost is measurable, which the direction accepting that plan authorizes; where no cost is measurable, GUARD.14 estimates nothing, and the direction authorizes the configuration it names. GUARD.14's "Absent such a discipline, an agent uses the least costly configuration" now has work that proceeds, which it presumed. Neither LVL0 text changes.

**AGENT.6 (CC21):** "Where the operating cost of a unit of work is measurable and the human owner has set no discipline under GUARD.14, the agent that executes the unit SHALL state an effort estimate in the record of the unit's plan (QA.2, GUARD.14)."

### A2. Builds, installs, and test runs

**Reading drafted.** A build, an install, or a test run within the working bounds, against the configuration that the work records under version control, or otherwise authorized, is permitted, and that configuration is the list of STND.DFLT.24; installing a package the recorded configuration does not name, and a build or test run beyond the working bounds, halts and is referred. GUARD.5 and GUARD.6 unchanged.

**New STND.DFLT.34, Builds, installs, and test runs (binding: GOV.22, GUARD.6):**

> Within the working bounds (STND.DFLT.25), an agent MAY run a build, an install, or a test run against the configuration that the work records for it under version control, other than an addition to it of a kind that STND.DFLT.35 halts, or under an authorization that covers the run (GOV.22, GUARD.6). For such a run, the locations that the configuration names as written, and those in which the run's tools keep caches or state, each with symbolic links resolved, SHALL be the list of STND.DFLT.24 (GOV.22, GUARD.6).

**New STND.DFLT.35, Additions to recorded configuration (binding: GOV.22, PRIME.7, PRIME.14), closing D1:**

> Where an agent would add to the configuration of STND.DFLT.34 a package, a revision of a package, or a source of packages, that no authorization covers and that the human owner did not give it directly (STND.DFLT.17), the agent SHALL halt that line of work and refer it (GOV.22, PRIME.7, PRIME.14).

A change to the recorded configuration that adds a package or a source, or changes the pinned revision of a package, is itself the installation of a package the configuration did not name; STND.DFLT.35 halts the addition, and STND.DFLT.34 never reaches an install of what an agent added on its own, whether or not the agent referred it. The run beyond the working bounds is STND.DFLT.25. The Notes quote the ruling, name both halts, say that a downloading install is also network access (GUARD.13), and say that regenerable outputs fall in the third exempt class.

**CC14, the first exempt class of STND.DFLT.15:** "change or removal of a file under version control whose last committed state is verified recoverable and from which it differs only by changes that the agent made in the current unit of work;". Another actor's uncommitted changes stay under STND.INSTR.2 (D2).

**Why GUARD.6 and GUARD.7 are met.** GUARD.6 reserves a destructive action "whose full scope is not enumerated and verified before execution". The list is the locations the recorded configuration names as written (an output directory counting as its contents, term Bulk item) with the caches and state of the run's tools, links resolved; version control keeps the configuration reviewed (QA.7) and readable before the run, which is the verification. Regenerable outputs are the third exempt class (GUARD.7). GUARD.5 is met by the first exempt class as reworded: the committed state is the verified recoverable prior state for the agent's own changes alone.

### A3. The scribe route

**Reading drafted.** Option (a): the agent enters each act the human owner gives it directly, quoting the act without its secrets, with the human owner as the actor of the act and itself as scribe; STND.DFLT.23 accepts such entries for work that is not assured; STND.DFLT.5 stays; STND.HARN.6 and .7 are limited to the governance ledger and to ledgers a harness is asked to read.

**STND.DFLT.17, retitled Entered acts and reliance (binding: GOV.22, GOV.36, GUARD.2, GUARD.10, PRIME.10):**

> An agent SHALL enter, as a ledger entry with itself as actor, each act that the human owner gives it directly and that governance requires to be recorded, and no act as the human owner's that the human owner did not give it directly, stating the human owner as the actor of the act and quoting the act and each proposal that the act accepts, without each secret that it contains (GOV.22, GOV.36, GUARD.10, PRIME.10). An agent SHALL rely only on an authorization given it directly in its current session, extended to it under GUARD.12, or carried by an entry that STND.DFLT.23 accepts (GOV.22, GUARD.2).

The Notes list the acts governance requires to be recorded: an authorization and its revocation (GUARD.10), a waiver (GOV.44), a ruling (GOV.3), the classification and its revision (GOV.24, STND.DFLT.13), a promotion (QA.11), a release (QA.10), an adoption (GOV.41), the adoption of an instruction file (STND.INSTR), the direction of STND.DFLT.33, a decision to continue halted work (STND.DFLT.9), a change of the stopping rule (QA.3), the choice of a cost discipline (GUARD.14), the replacement of a default (GOV.19), and a decision that raises the floor (GOV.11); a direction that governance does not require to be recorded is not entered.

**STND.DFLT.23, second sentence:** "Where the work is not assured, each entry that names the human owner as actor or records an act of the human owner under STND.DFLT.17 SHALL be accepted (GOV.22, GOV.36)."

**STND.DFLT.5:** the second sentence gains PRIME.2 (R1.7) and is otherwise unchanged; the prohibition of S2 sits in STND.DFLT.17 ("and no act as the human owner's that the human owner did not give it directly"), because a second item under STND.DFLT.5's SHALL NOT would be a negated list (STND.DRAFT.15, check g.11).

**STND.HARN.6:** "The governance ledger, and each ledger that a harness is asked to read or append to, SHALL be a UTF-8 file of one transaction per line, …". **STND.HARN.7:** "Each transaction of the governance ledger, or of a ledger that a harness is asked to read or append to, SHALL hold exactly the fields …". The STND.HARN Notes say that a work ledger kept under STND.DFLT.5 alone has the form that provision gives, and takes the form of STND.HARN once a harness is asked to read or append to it (CP18, O3).

**The actor of the entry and the actor of the act.** STND.DFLT.5 bars an agent from appending an entry that names the human owner as actor; STND.DFLT.17 has the agent as the actor of the entry and states the human owner as the actor of the act within it. The Notes make the distinction explicit, so that STND.DFLT.5 reads on the entry's actor as it always did, and say that STND.DFLT.17's "no act … not given directly" and STND.DFLT.5 close the two ways an agent would grant itself an authorization (PRIME.7).

**The harness.** `verify` reads only the root `ledger.jsonl` (`govharness/ledger/chain.py`, `read_ledger`); a work ledger is read only by `sign check LEDGER --ledger-id ID` and appended to only by `ledger append --ledger-file PATH --ledger-id ID` (`govharness/cli/records.py`), each a case of a harness asked to read or append to it. No check reads a work ledger unasked, so no code changes under unit 0025, and no check's verdict on the live corpus changes. The fast test subset passes (46 tests).

### A4. CSQ1 without a signer register

**Reading drafted.** An entry recording CSQ1 or CSQ0 makes the work assured only once a signer register exists; until then the classification stands as recorded, and each referral names founding the register as the next step. Signatures stay unadopted.

**Term Assured work:** "Work for which an entry that names the human owner as actor, or that records an act of the human owner under STND.DFLT.17, records CSQ0 or CSQ1 as the consequence class, the signer register lists a key of the human owner for the work's ledger, and no entry later than that classification that STND.DFLT.23 accepts for assured work records a less severe class." A classification the agent enters as scribe reaches assured work (D3).

**STND.DFLT.20, second sentence:** "Where the work is not assured and an entry that names the human owner as actor, or that records an act of the human owner under STND.DFLT.17, records CSQ0 or CSQ1, the statement SHALL name the founding of the signer register as a recommended next step (GOV.22, PRIME.14)."

**The Note** "an entry of the human owner, signed or not, makes work assured, and only a signed one ends that" now says that such an entry, or the agent's entry of the owner's act, makes work assured once the register lists a key of that owner for the work's ledger, that only a signed entry then ends that, that until the register is founded the class stands as recorded, every entry of the human owner is accepted, and each referral names the founding as a recommended next step, and that a forged pre-register entry makes the work assured once the key is listed and a signed entry then ends that, so nothing locks (O1). Transition: a project that recorded CSQ0 or CSQ1 without a register is no longer assured until the register lists a key of its owner; its class stands as recorded.

### A5. Write bounds

**Term Working bounds, the default:** "by default, the top directory of the work, each temporary location, each file and directory that the agent or its run creates in the system's temporary directory, and each location in which installed software keeps its caches, state, or configuration by the convention of its operating system or tool, and for reading also the installed software and the account's files; the default leaves out, for writing, each configuration that settles the tier of an agent's actions or otherwise governs an agent (GUARD.2, PRIME.7), each instruction file (STND.INSTR), and each setting that enables a check of security or integrity, selects a source or destination of network access, or runs a program without a request; and it leaves out altogether the store of AGENT.44, each location that holds secrets or credentials by the convention of its operating system or tool, and each location that the threat model or an entry that STND.DFLT.23 accepts names as holding secrets, credentials, or other data it marks as protected (PRIME.10)." The two later sentences of the term are unchanged.

The exclusions for writing (D4) are named by outcome, and match the machine-local row of STND.PROJ.3: whatever governs the agent, its permission and instruction configuration among it, instruction files, and the settings for integrity checks, network sources and destinations, and programs run without a request, so that no write of an agent widens its own authority; an agent proposes a change to such a file or setting by a referral. What others created in the system's temporary directory stays outside the bounds (S5).

### B1. Instruction files

**Reading drafted.** Option (b): an instruction file the human owner adopts, through the scribe route, is part of the agent instructions, read as adopted governance; STND.INSTR.6 reaches only content met while working; no product named.

**Term Instruction file (STND.INSTR):** "A file, other than a file of a tool memory store, that the provisioned environment presents to an agent as standing instructions at the start of a session, identified by its path." A store its tool loads at session start is therefore no instruction file: no adoption under STND.INSTR.11 names it, and the exclusion of instruction files from the write bounds (D4) leaves it in.

**New STND.INSTR.11, Instruction files (binding: GOV.48, GOV.36, PRIME.11, GOV.49):**

> Where the human owner adopts an instruction file by a ledger transaction that names the file by its path and its content by a revision under version control or a digest, the agent instructions SHALL include that file in that content (GOV.48, GOV.36, PRIME.11). An agent SHALL treat each instruction file whose content no adoption names as content without instruction authority, and name each such file in the completion report of STND.INSTR.7 (GOV.48, PRIME.11, GOV.49).

The adoption is a ledger transaction (GOV.36), which under the defaults is the scribe route of STND.DFLT.17 and under a constitution the project's own ledger (S6).

**STND.INSTR.6:** "An agent SHALL state in its completion report (STND.INSTR.7) each passage that purports to direct an agent in content that it meets in the course of its work, a tool memory store included, and that carries no instruction authority, and each such passage that the completion reports of the agents it directs state (GOV.48, PRIME.11). Where a passage of such content, or of an instruction file that no adoption names, directs an action that a prime directive or GUARD forbids or reserves, the agent SHALL report that passage to the human owner when it finds it (GOV.48, PRIME.11, GUARD.16)."

The Notes say what an instruction file is in an environment, that a skill or an extension the environment loads the same way is one to the extent that it directs, that the adoption is the human owner's LVL3 act (GOV.41) binding path and content so that another actor's edit carries no authority until adopted (GOV.49), that an adopted file lies outside the working bounds for writing and an agent proposes a change to it by a referral, that an adopted file relaxes nothing (GOV.20, GOV.9), and that a file whose content no adoption names is data, named once in the completion report, with a passage of it that directs a forbidden or reserved action reported at once (STND.INSTR.6).

### B2. Tool memory store

**Term Tool memory store (STND.DFLT), with the three conditions the ruling fixes:** "A store of an agent's notes that a tool of the agent keeps outside the work and across sessions, at a location that a record of the work names, holding no secret and no other data that the threat model protects against disclosure (PRIME.10), and lying within the working bounds for that agent." The second condition is against disclosure (S8), because the default table protects the work itself against change, which a notes store does not threaten. STND.INSTR's Terms take the meaning from STND.DFLT, as STND.HARN takes Signer register.

**STND.DFLT.6:** "The working-notes workspace SHALL be the directory "notes" at the top of the work, together with each tool memory store (GOV.22, INTPR.5)." **STND.INSTR.8:** "… in the working-notes workspace or a tool memory store, and out of code comments and human-facing documentation …". Making the store part of the workspace brings INTPR.5 to it: human-readable, no instruction authority, never the only record (INTPR.13). The store's content carries no instruction authority (INTPR.5, PRIME.11); a file of it is no instruction file, so no adoption under STND.INSTR.11 names it, and a passage of it that purports to direct an agent is content met in the course of the work under STND.INSTR.6, stated in the completion report and, where it directs a forbidden or reserved action, reported at once; the human owner gives such text authority only by placing it in an instruction file and adopting that file (S7, verification finding 1). With A5, a store that its tool keeps in a conventional state location is within the bounds for writing.

## Register entries carried

| Entry | Sources | Drafted |
| --- | --- | --- |
| R1.1 | CC1, CC21 | A1 above; AGENT.6 conditional on a measurable cost. |
| R1.2 | CC2, CC14 | A2 above; the first exempt class. |
| R1.3 | CC3 | A5 above. |
| R1.4 | CC8, CC18 | New STND.DFLT.32, Proposal of standing authorizations (binding: GOV.22, GUARD.10, GUARD.11, GUARD.12): "Where a unit of work first needs an action of a class of the table of STND.PROJ.3, an agent SHALL propose to the human owner, in the findings and justification statement by which it refers that action (STND.DFLT.20), each standing authorization of that table that the work needs, with its scope, its duration, and the agents to which it extends (GOV.22, GUARD.10, GUARD.11, GUARD.12)." It cites the table and copies none of it. New row of STND.PROJ.3: "Reading from a private remote repository \| Where the human owner records that repository as part of the provisioned environment, retrieval of the commits, branches, and tags that the work does not yet hold, within a volume per retrieval that the authorization states, to bring the work current with them, for as long as the repository meets that record \| The lead agent, implementing agents, and each agent that merges into a branch of the work" (S9: a whole history is bulk retrieval, GUARD.8). The STND.PROJ Notes say the row is network access (GUARD.13) distinct from research retrieval. |
| R1.5 | CC29, checked | Confirmed: STND.DFLT.19 read "an asset or threat source that the table of STND.DFLT.18 omits", and Asset is defined only in STND.THRT (grep over the corpus). Now: "Where the work comes to hold irreplaceable data, to drive physical hardware, or to write to a system outside the provisioned environment, and the table of STND.DFLT.18 does not name that asset with the threat that the work brings to it, an agent SHALL halt that line of work and refer it (GOV.22, GUARD.16)." The STND.DFLT Terms say "Asset has the meaning that STND.THRT gives it"; no provision of the corpus cites a section locator, so the term is taken by that sentence rather than by a citation in the body. |
| R1.6 | CC13 | STND.DFLT.11: "its actor SHALL review the pinned revision of each dependency that the unit changes before the unit is judged done". |
| R1.7 | CC27 refuted; F1 | PRIME.2 added to the second sentence of STND.DFLT.5 and its `instantiates`. Citation fit (STND.DRAFT.23): a forged entry misrepresents evidence and its status, which PRIME.2 bars; the sentence makes that specific without relaxing it. |
| AD5 | AD5 | AGENT.11: "… its scope, the location of the agent instructions that govern it, and each authorization that extends to it under GUARD.12 (GUARD.12, QA.1, GOV.48)." |
| R5.4 | CC28 | STND.INSTR Notes: "… are the project's choice; where the work is assured, a configuration that displaces a provision is recorded under STND.DFLT.22." |
| R5.2 | CP18 | A3 above, STND.HARN.6 and .7. |

## Floor arguments (GOV.11)

Every provision of STND.DFLT and STND.INSTR binds because it instantiates GOV.22 or GOV.48 (GOV.10); AGENT.6 and AGENT.11 bind through GUARD.14 and GUARD.12. For each provision that gains or changes an obligation:

- **STND.DFLT.17:** widens what the agent enters from grants to every act the human owner gives it directly that governance requires to be recorded, and bars entering any other act as the owner's. The obligation falls on the agent, costs the human owner nothing, and removes the hand-written ledger line; GOV.36 already has each such act entered.
- **STND.DFLT.20, second sentence:** one recommended next step in a referral that PRIME.14 already requires, only while an unsigned entry records CSQ0 or CSQ1.
- **STND.DFLT.23:** accepts more entries; a permission.
- **STND.DFLT.32:** a proposal inside the referral PRIME.14 already requires, with content GUARD.10 already requires of an authorization; the human owner adopts or declines (STND.DRAFT.42 asks no decision beyond GUARD.10's).
- **STND.DFLT.33:** the agent relies on an act the human owner makes anyway, and enters it; no decision is required of the human owner, and routine work proceeds at every class where it halted before.
- **STND.DFLT.34:** a permission, and the identification of the list; lowers the overhead of every build and test run.
- **STND.DFLT.35:** states where PRIME.7 and PRIME.14 already halt; no new obligation of the work.
- **STND.DFLT.6, STND.DFLT.15, STND.INSTR.8:** widen a permission; the first exempt class only for the agent's own changes.
- **STND.DFLT.11, STND.DFLT.19, STND.INSTR.6, AGENT.6, STND.HARN.6, STND.HARN.7:** narrow an obligation; STND.INSTR.6's second sentence keeps the at-once report for an unadopted instruction file, which the old first sentence reached.
- **STND.DFLT.5:** a citation; the obligation is unchanged.
- **STND.INSTR.11:** the first sentence takes effect only on the human owner's own adoption, an act GOV.41 assigns and no provision requires; the second falls on the agent and replaces listing every passage of a file with naming the file.
- **AGENT.11:** one more item in a brief the directing agent already writes; GOV.48 already binds the directed agent.
- **STND.PROJ.3:** a recommendation within a binding provision, adopted or declined by the human owner.

## A2, A3, and B1 against PRIME.6, PRIME.7, PRIME.10, PRIME.11, and GUARD.5 to GUARD.7

| | A2 (STND.DFLT.34, STND.DFLT.35, STND.DFLT.15) | A3 (STND.DFLT.17, STND.DFLT.23) | B1 (STND.INSTR.11, STND.INSTR.6) |
| --- | --- | --- | --- |
| PRIME.6 | A run against the recorded configuration is enumerated (GUARD.6) and its outputs regenerable (GUARD.7), so it is no reserved action; a run whose outputs the list does not reach stays unlisted and reserved. | An agent executes no reserved action by entering an act; the act is the human owner's, and an entry records it. | An adopted file is lower governance (GOV.20) and relaxes nothing, so it authorizes no reserved action to an agent (PRIME.6, GOV.9). |
| PRIME.7 | The install that STND.DFLT.34 permits reproduces, within the working bounds, the dependency set the work's records already carry (REPRO.9); adding a package or a source to that set is itself an install the records did not name, which STND.DFLT.35 halts and refers unless an authorization covers it or the human owner gave it directly, so an agent cannot write the package in and then install it. A downloading install is also network access (GUARD.13). The reading of PRIME.7 relied on is put to the custodian below. | An agent grants, extends, and infers nothing for itself: STND.DFLT.17 enters an act the human owner gave, and no act the owner did not give; STND.DFLT.23 accepts the entry only as the record of that act; STND.DFLT.5 still bars an entry in the human owner's name, and PRIME.7 still bars inferring a grant from silence. | Adoption is the human owner's act (GOV.41, GOV.36); an agent adopts nothing (GOV.49); an adopted file is outside the working bounds for writing, and a file an agent edits has content no adoption names, so it is data. |
| PRIME.10 | A tool's cache or state location is within the bounds only where it holds no secrets or credentials (A5); the exclusions of the term stand. | The act and each accepted proposal are quoted without each secret they contain. | An instruction file holds no secret by PRIME.10; a tool memory store holds no secret and nothing protected against disclosure. |
| PRIME.11 | Unchanged. | Unchanged; an entry is a record, not an instruction. | PRIME.11 is unchanged: the file carries authority only by the human owner's adoption, which is the owner's instruction; a file no adoption names is data; a passage met in the work that purports to direct is still stated, and a forbidden or reserved direction, in such content or in an unadopted instruction file, is still reported at once. |
| GUARD.5 | The committed state is the verified recoverable prior state for the agent's own changes in the current unit alone; another actor's uncommitted changes stay under STND.INSTR.2; an irrecoverable action stays reserved. | Not touched. | Not touched. |
| GUARD.6 | The recorded configuration's locations with the tools' caches and state, links resolved, are the enumeration; GUARD.6 is unchanged and still prevails over every exemption. | Not touched. | Not touched. |
| GUARD.7 | Regenerable outputs are the third class; the first class names its recoverable state. | Not touched. | Not touched. |

## For the custodian at ratification

The review's table of the seventeen items of the first draft was followed where sound; the twelve it marks resolved or merged are listed under "Review and dispositions". Five true questions remain, each drafted as recommended.

1. **A2, PRIME.7 and installs (item 3).** The MAY of STND.DFLT.34 reaches an install only on the reading that PRIME.7's "installs software or dependencies" means adding software to the provisioned environment or a dependency to the work, not reproducing within the working bounds the set the records name; STND.DFLT.35 keeps the addition of a package or source under PRIME.7. The custodian is asked to adopt this as an interpretation of PRIME.7 under GOV.3, which binds every project. Alternative: PRIME.7 read strictly, every install needing the authorization of STND.PROJ.3, and STND.DFLT.34 reaching builds and test runs only. Recommended: the interpretation, which the ruling's words ("installs … permitted if done against the stated configuration") give.
2. **A2, GUARD.5 and uncommitted edits (item 4, narrowed by D2).** The first exempt class names the last committed state as the recoverable prior state of a file that differs from it only by the agent's own changes in the current unit, so an agent's successive edits are not each a reserved overwrite, while any other uncommitted change stays protected. Recommended: as drafted.
3. **B1, what adoption binds (item 10).** The path and the content (a revision or a digest), so an edit by another actor, or by an agent, has authority only once the human owner adopts it; each change of a file costs one adoption. Alternative: the path alone, which lets another person's edit inherit the owner's authority, the objection the rulings raise to option (a). Recommended: content.
4. **B1, unadopted files (item 11, with S6).** Named once in the completion report, not passage by passage; a passage of such a file that directs a forbidden or reserved action is still reported at once (STND.INSTR.6, second sentence). Recommended: as drafted.
5. **R1.5, the halt (item 15).** STND.DFLT.19 halts for the three cases only where the table of STND.DFLT.18 does not name the asset with the threat the work brings; the threat condition goes beyond R1.5's words, so that an outside system written to under the threat the table already names ("Action beyond authorization") does not halt twice. Alternative: the three cases halt whenever the table omits the asset, which halts every outside write under STND.DFLT.19 as well as under PRIME.7. Recommended: as drafted.

## Review and dispositions

The cold review is `review.md`. One row per finding.

| Finding | Disposition |
| --- | --- |
| D1, STND.DFLT.34 lets an agent add a package to the configuration and install it | Fixed, tighter than proposed: new STND.DFLT.35 halts and refers the addition itself of a package or a source that no authorization covers and the human owner did not give directly (STND.DFLT.17), and STND.DFLT.34 excludes an addition that STND.DFLT.35 refers, so the MAY never reaches an agent's own addition. A separate provision rather than a third sentence, to keep STND.DFLT.34 at two modals. |
| D2, the first exempt class reaches the owner's uncommitted changes | Fixed as proposed: "and from which it differs only by changes that the agent made in the current unit of work". The pair conflict with STND.INSTR.2 is closed. |
| D3, a scribed classification never makes work assured | Fixed as proposed, in the term Assured work and in STND.DFLT.20: "or that records an act of the human owner under STND.DFLT.17". The Note says the same. |
| D4, the bounds open the agent's own permissions, instruction files, and network sources to writing | Fixed, by outcome: the default leaves out for writing each configuration that settles the tier of an agent's actions or otherwise governs an agent (GUARD.2, PRIME.7), each instruction file (STND.INSTR), and each setting that enables a check of security or integrity, selects a source or destination of network access, or runs a program without a request; the secret locations stay out altogether. The Note says no write of an agent widens its own authority and that a change is proposed by referral. |
| S1, STND.DFLT.17 omits waivers and revocations and ledgers every decision | Fixed: "each act … that governance requires to be recorded", quoting "the act and each proposal that the act accepts"; the acts are listed in the Notes. "where it accepts one" was reworded after g.12 read it as a trailing condition. |
| S2, STND.DFLT.5 should bar an entry stating an act the owner did not give | Fixed, placed in STND.DFLT.17 ("and no act as the human owner's that the human owner did not give it directly"): a second item under STND.DFLT.5's SHALL NOT is a negated list (STND.DRAFT.15, g.11), and a third sentence would add a g.18 notice. The Note names both bars. |
| S3, implicit acceptance | Fixed as proposed in STND.DFLT.33 ("names, or accepts a plan that names,") and in the AGENT Note; the STND.DFLT Note adds that acceptance is never implied (PRIME.7). |
| S4, links unresolved and caches unlisted | Fixed as proposed: the list is the locations the configuration names as written and those in which the run's tools keep caches or state, each with symbolic links resolved. |
| S5, the system temporary directory | Fixed as proposed in the term; the Note says what others created there stays outside. |
| S6, STND.INSTR.11 under a constitution, the second sentence, the at-once report | Fixed, all three as proposed: "by a ledger transaction" with GOV.36 instantiated; "treat each instruction file whose content no adoption names"; STND.INSTR.6's second sentence reaches "such content, or … an instruction file that no adoption names". |
| S7, the Note against INTPR.5 | Fixed as proposed; the memory store is no longer read as an instruction file to the extent it directs. |
| S8, the term's second condition | Fixed as proposed: "holding no secret and no other data that the threat model protects against disclosure". |
| S9, whole history is bulk | Fixed as proposed in the row and the STND.PROJ Note. |
| S10, the rationale's "none;" and the Note attributing the reading to the custodian | Fixed, both. |
| O1, a forged pre-register entry | Taken, in the Note: nothing locks. |
| O2, the third exempt class and a downloading install | Taken, in the Note (GUARD.7, GUARD.13). |
| O3, "asked to read or append to" | Taken, in STND.HARN.6, STND.HARN.7, the Note, and the rationale. |
| Custodian items 1, 2, 8, 12, 16, 17 | Resolved as the review's table says: 1 by the A1 ruling; 2 by S3; 8 by option (a)'s "every referral"; 12 by B1 and S7; 16 by F1; 17 by O3. |
| Custodian items 5 and 6 | Merged and resolved by S1. |
| Custodian item 7 | Resolved by A4 and O1. |
| Custodian item 9 | Resolved toward R1.3 by S5. |
| Custodian items 13 and 14 | Merged into S7 and S9. |
| Custodian items 3, 4, 10, 11, 15 | Kept, above: 3 as an interpretation of PRIME.7 for the custodian to adopt; 4 narrowed by D2; 11 with S6. |

The cold verification is `verify.md`; its three findings:

| Finding | Disposition |
| --- | --- |
| V1, Defect: a tool memory store loaded at session start is an instruction file, so D4 bars writing it and STND.INSTR.11 could adopt it | Fixed: the term Instruction file excludes "a file of a tool memory store", so the store stays within the write bounds under B2's conditions and no adoption names it. Its content carries no instruction authority unless placed in an instruction file that the human owner adopts (INTPR.5, PRIME.11); STND.INSTR.6's first sentence now names a tool memory store among the content met in the course of the work, so directing text found in it is stated in the completion report and, where it directs a forbidden or reserved action, reported at once. The STND.INSTR and STND.DFLT Notes say so. |
| V2, Should-fix: STND.DFLT.35 misses a change of the pinned revision | Fixed as proposed: "a package, a revision of a package, or a source of packages"; the Note and the rationale say the same. |
| V3, Optional: "that STND.DFLT.35 refers" reads as only an addition actually referred | Taken: "of a kind that STND.DFLT.35 halts", so an agent that breaches STND.DFLT.35 gains nothing from STND.DFLT.34. |

## Checks

- `ROUNDS=apply_round_a_2026_10_28 python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`: entries 203 to 207 appended; every check PASS, logic PASS with the one g.18 warning the corpus carries; source unchanged.
- Kept copy under `/tmp/claude-1000/round-a-kept/`: `references --check` PASS; `compose --check` lists the six reading copies as stale because the kept copy has no `rendered/` beside it, which the lead rebuilds after ratification (standing process, step 8); `pairs` for the five documents, verdicts in `pairs-changed.md`, no conflict; `findings.py` over the changed provisions finds only the notices the live corpus already carries (g.12 twice on the second sentence of STND.INSTR.6, which the round extends, and once on the fourth row of STND.PROJ.3). The new notices the revision raised, g.11 on STND.DFLT.5 and g.12 on STND.DFLT.17, were fixed (S1, S2 above).
- Self-check: one modal per sentence, at most two per provision in every provision of this round; conditions before clauses; none of the banned words; titles of at most five words, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to` (the checks `ids` and `references` pass).
- Harness: no code changed; fast subset 46 tests OK.

## Left to the lead

- The STND.DEPS Notes sentence "the last trigger narrows that of STND.DFLT.11, which reviews every direct dependency, to the pinned revision that the unit changes" describes the old STND.DFLT.11; after this round the two say the same. STND.DEPS is outside this round's scope; one editorial sentence.
- `rendered/` and `OPEN-ITEMS.md` after ratification.
