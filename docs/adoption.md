# Adopting the governance in a project

This guide is for the human owner of a project: the person accountable for the work, who sets its consequence class, grants its authorizations, and decides what agents refer. It covers how a project takes up the governance, how its class is set and later raised, and what the corpus asks of the human at each class. The provisions cited print with `govharness show ID`, and each has a reading copy in [`rendered/`](../rendered/LVL0.md).

## Adopting

1. Install the governance in one of the ways in [installation.md](installation.md). A project that installs nothing can still adopt it by reading the corpus.

2. Decide whether the project needs a project constitution yet. A project that promotes a result other than through its adopted classification, releases software, or drives physical hardware has one (GOV.20). At CSQ3 or CSQ4, the adopted classification promotes each result that meets its acceptance criteria for reliance by its author or immediate team (QA.11), so that reliance needs no constitution. Until then the defaults of STND.DFLT apply (GOV.22, STND.DFLT.1). A constitution starts as a copy of `harness/governance/_PROJECT/NAME/`, and STND.PROJ says what each of its sections holds. A constitution may adopt STND.DFLT by one citation for most of its sections and state in full only the rest (STND.PROJ.2).

3. Set the consequence class. The human owner sets it at inception, as the most severe class of the uses then made of the work's outputs (GOV.13), and adopts the classification (GOV.24, GOV.50). STND.CLASS.1 gives the test of each class, and STND.CLASS.5 what the record states. Where a more severe use is already planned, the record also states the expected class; see [Recording an expected class](#recording-an-expected-class). In Claude Code, `/governance:classifying-work CSQ3` drafts the record for you to review; it writes nothing.

4. Record the classification. Under the defaults, the classification is a record that the human owner adopts by a transaction of the project's ledger, `records/ledger.jsonl` (STND.DFLT.13). An agent can enter it for you: tell the agent in its session that you adopt the draft, and it enters your act as a ledger entry with itself as actor, naming you as the actor of the act and quoting your adoption and the draft (STND.DFLT.17). Such an entry is accepted for work that is not assured (STND.DFLT.23). An agent never appends an entry that names you as its actor (STND.DFLT.5).

   You can also append the entry yourself. The harness does it in one command, run from the top of the project:

   ```bash
   govharness ledger append "$GOVHARNESS_ROOT" \
       --ledger-file records/ledger.jsonl --ledger-id example-project \
       --type classify --actor "Jane Doe" --role "The Human Owner" \
       --authority GOV.13,GOV.24,STND.DFLT.13 \
       --rationale "Classification: CSQ3. Credible consequence: ... Reliance: ... Row of STND.CLASS.1: CSQ3."
   ```

   The first argument is the corpus, which the command reads and leaves unchanged. With the plugin alone, the same command runs as `PYTHONPATH="<installPath>" python3 -B -m govharness ledger append "<installPath>/governance" ...`, with `installPath` from `claude plugin list --json`. Without the harness, an entry states what STND.DFLT.5 lists. A ledger that the harness reads or appends to also takes the form of STND.HARN.6 and STND.HARN.7, and [`harness/README.md`](../harness/README.md#reading-and-applying-the-corpus-without-software) shows how to compute an entry's hash by hand.

   Until a class is recorded, the work meets the floor (GOV.10). An agent halts and refers to you only a line of work that needs the class to promote, release, deploy, or drive physical hardware (GOV.13).

5. Tell the project's agents where the governance is. Under the defaults, the agent instructions are the provisions of STND.INSTR (STND.DFLT.21). A few lines in the project's `AGENTS.md` or `CLAUDE.md` name the corpus and the records; [installation.md](installation.md#pointing-other-agents-at-the-governance) has an example. Such a file is an instruction file, and it joins the agent instructions only once you adopt it by a ledger transaction that names its path and its content, by a revision under version control or a digest; each change to its content needs a new adoption (STND.INSTR.11). An agent can enter the adoption for you, as in step 4. Until then, an agent treats the file as content without instruction authority and names it in its completion report.

6. Direct the work, and grant the authorizations it needs.
   - When you direct work and name the agents that carry it out and the configuration of each, or accept a plan that names them, your direction authorizes the operating cost of the units of work it covers. An agent enters the direction as an authorization (STND.DFLT.33).
   - Under the defaults, an agent may run a build, an install, or a test run within the working bounds against the configuration that the work records under version control (STND.DFLT.34). Ledger entry 204 records the custodian's reading of PRIME.7 that permits such an install. The locations that the configuration names as written, with the caches and state of the run's tools, are the run's list of affected items (STND.DFLT.34). A run that writes only there is listed before it starts and is not a bulk action (GUARD.6).
   - Adding a package, a revision of a package, or a package source that no authorization covers halts and comes to you (STND.DFLT.35), as does a read or write outside the working bounds (STND.DFLT.25). The term Working bounds of STND.DFLT states what the bounds take in by default and what they leave out for writing.
   - Network access, writes to a remote system, other changes to the installed software or the system configuration, and actuating hardware each need a recorded authorization of the human owner (PRIME.7, GUARD.10). The first time a unit of work needs an action of a class that the table of STND.PROJ.3 lists, the agent's referral proposes the standing authorizations the work needs, for you to grant or decline (STND.DFLT.32). An agent enters each authorization you give it directly (STND.DFLT.17). For a project with a constitution, the agent that drafts it proposes the standing authorizations of the table of STND.PROJ.3 in the section Authorizations.
   - Some defaults need a setting that the working bounds keep from an agent's writing, such as a setting that runs a program without a request. Where the work declares a range of revisions of its language or of a dependency, STND.DEPS.14 asks for a check that runs at an interval the repository configuration sets. You make that setting, or record a decision that replaces the default (GOV.19).

## Recording an expected class

Work often starts at CSQ3 or CSQ4 and is reclassified when someone comes to rely on it at a more severe class. Where a more severe use is planned, the classification states the expected class and the use that would occasion it (GOV.13, STND.CLASS.5). The expected class is adopted with the classification, in the same act, and sets no class before that use begins (GOV.13).

Recording an expected class asks two things of the work, which work of CSQ4 does not omit (STND.CLASS.10):

- The design admits, without rework, the parts that the expected class will ask for, and a decision record gives the reason for each choice that the expected class drives. Before the reclassification, the work may omit each record that only the expected class requires, other than the records of the next point (STND.CLASS.21).
- Work of CSQ4 keeps the records that the table of STND.CLASS.23 lists, from the basis of each tolerance to lock files and toolchain revisions.

Without an expected class, neither applies.

## Raising the class later

A class attaches to the use of the work. It moves toward CSQ0 whenever reliance or exposure grows, and away from CSQ0 only by your recorded decision (GOV.14). STND.CLASS.7 lists the events that call for a reassessment: growing reliance or exposure, a harm scenario that an agent reports, or an incident that shows a consequence the classification omits. Until you record the reassessment, the work is not relied upon in the use that occasioned it.

To raise the class:

1. Draft the revised classification, with `/governance:classifying-work CSQ2` or by hand.
2. Record it as a new entry of the project's ledger, as in step 4 above.
3. Check what the new class adds. `govharness onset CSQ2` lists each provision, and each part of a provision, that applies from CSQ2 by its field `onset`, and the table of STND.CLASS.10 lists the parts of LVL0 that apply only from CSQ2, CSQ1, or CSQ0. STND.CLASS.18 gives the reviewer of each class, and STND.CLASS.19 the auditor.
4. Before the work is relied upon at the new class, bring the work done at the lower class up to it (GOV.14). STND.CLASS.22 lists the steps, from regenerating each result whose record lacks an input to the audit of STND.CLASS.19 and the repeat of each check tied to an earlier event, and says when existing source takes up a default of form or style.
5. Write a project constitution if the project now promotes a result other than through its adopted classification, releases software, or drives hardware (GOV.20).

The audit falls once, before work moved to CSQ2 or a more severe class is first relied upon at that class, and then at the interval of the new class (STND.CLASS.19). A move from CSQ4 to CSQ3 needs no audit of its own.

Nothing is reinstalled. The class lives in the project's records, not in the plugin or the harness, and the next session reads it there.

## What the human is asked to do, by class

The custodian's aim is that the human owner is asked for interaction only on request, or when the work is of CSQ1 or CSQ0. Below CSQ1, what remains are the acts listed for every class. An agent enters each act that you give it directly in the ledger (STND.DFLT.17), so, until the work is assured, none of them needs a ledger line written by hand.

At every class, the prime directives, GUARD, and GOV bind (GOV.10), and these acts are the human owner's:

- under the defaults, directing the work: naming, or accepting a plan that names, the agents and the configuration of each, which authorizes the operating cost of the units of work it covers (STND.DFLT.33);
- executing a reserved action: an irrecoverable action, a bulk action, a bulk retrieval, a monetary transaction, or a hazardous actuation (PRIME.6);
- granting each authorization, for the actions that PRIME.7 lists (GUARD.10); under the defaults, builds, installs, and test runs against the recorded configuration need none (STND.DFLT.34), and a package, revision, or source added to that configuration comes to you unless an authorization covers it (STND.DFLT.35);
- deciding each line of work that an agent halts and refers, from its findings and justification statement (PRIME.14, STND.DFLT.20), including the standing authorizations that an agent proposes when the work first needs an action of a class that STND.PROJ.3 lists (STND.DFLT.32);
- adopting the judgments that set the burden on the work: the classification, with its expected class where a more severe use is planned, promotion of a result, axioms, the hazard analysis, the reserved-action register, estimates for implicit expenditure, and the decision to release or deploy (GOV.13, GOV.50);
- adopting each instruction file that is to direct the project's agents, once for each content (STND.INSTR.11);
- under the defaults, deciding whether work continues after a unit of work halts at its third attempt without progress (STND.DFLT.9), and reporting each governance failure to the custodians from a report an agent drafts (STND.DFLT.12).

The rest depends on the class:

| Class | Review of each change (STND.CLASS.18) | Compliance audit (STND.CLASS.19) | Further acts of the human owner |
| --- | --- | --- | --- |
| CSQ4 | No row of the table applies | When the project is retired, by an actor who did not author the work; an agent is eligible | Recording the class. Reassessing it when reliance on the work grows (STND.CLASS.7); STND.CLASS.1 gives the reliance each class admits |
| CSQ3 | By an actor other than the author: a human, or an agent of any configuration in a session other than the author's, whose context holds nothing of the author's sessions beyond the records of the work | At most 36 months after the classification or the previous audit, and at retirement, by an actor who did not author the work; an agent is eligible | As for CSQ4. A result relied upon only by you and your team, through work verified before reliance, needs no promotion of its own: the adopted classification is its promotion (STND.CLASS.1, QA.11). Your team is the people and agents acting on the work under your direction (the term Team of STND.CLASS) |
| CSQ2 | As for CSQ3, and by an actor the author does not direct: a human, or, where the author is an agent, an agent whose configuration differs from the author's in its model or its instruction revision; a difference of tools alone does not count | Before a result is first relied upon, and at most 24 months after the previous audit, by an actor who did not author the work; an agent auditor differs from every authoring agent in its model or its instruction revision | As for CSQ3. Promoting each result relied upon beyond your team, or other than through verified work (QA.11). Stating in the classification the amount above which a loss counts as a cost (STND.CLASS.3) |
| CSQ1 | As for CSQ2, and a human reviews, before each promotion or release, the changes since the previous such review that affect a contract or a reported result | Before the first release, and at most 12 months after the previous audit, by an auditor as for CSQ2 | As for CSQ2. Under the defaults, each referral names founding a signer register as a recommended next step (STND.DFLT.20). Once the register lists your key for the work's ledger, the work is assured: only entries that name you as actor and carry your verified signature are accepted, so you append them yourself (STND.DFLT.23) |
| CSQ0 | As for CSQ1, and a human who did not author the change reviews each change to a safety-related component | Before each release, and at most 6 months after the previous audit, by a human who did not author the work | As for CSQ1. Adopting the hazard analysis (PRIME.13); recording where proof or exhaustive checking is not feasible (STND.CLASS.10); a recorded exercise in which a person resumes the work without the automation (STND.CLASS.10, INTPR.12) |
