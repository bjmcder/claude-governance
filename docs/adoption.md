# Adopting the governance in a project

This guide is for the human owner of a project: the person accountable for the work, who sets its consequence class, grants its authorizations, and decides what agents refer. It covers how a project takes up the governance, how its class is set and later raised, and what the corpus asks of the human at each class. The provisions cited print with `govharness show ID`, and each has a reading copy in [`rendered/`](../rendered/LVL0.md).

## Adopting

1. Install the governance in one of the ways in [installation.md](installation.md). A project that installs nothing can still adopt it by reading the corpus.

2. Decide whether the project needs a project constitution yet. A project that promotes a result, releases software, or drives physical hardware has one (GOV.20). Until then the defaults of STND.DFLT apply (GOV.22, STND.DFLT.1). Most projects start under the defaults at CSQ3 or CSQ4 and write a constitution when they first promote a result. A constitution starts as a copy of `harness/governance/_PROJECT/NAME/`, and STND.PROJ says what each of its sections holds.

3. Set the consequence class. The human owner sets it at inception (GOV.13) and adopts the classification (GOV.24, GOV.50). STND.CLASS.1 gives the test of each class, and STND.CLASS.5 what the record states. In Claude Code, `/governance:classifying-work CSQ3` drafts the record for you to review; it writes nothing.

4. Record the classification. Under the defaults, the classification is an entry of the project's ledger, `records/ledger.jsonl`, that the human owner adopts (STND.DFLT.13), and no agent may append an entry in the human owner's name (STND.DFLT.5). The harness writes the entry in one command, run from the top of the project:

   ```bash
   govharness ledger append "$GOVHARNESS_ROOT" \
       --ledger-file records/ledger.jsonl --ledger-id example-project \
       --type classify --actor "Jane Doe" --role "The Human Owner" \
       --authority GOV.13,GOV.24,STND.DFLT.13 \
       --rationale "Classification: CSQ3. Credible consequence: ... Reliance: ... Row of STND.CLASS.1: CSQ3."
   ```

   The first argument is the corpus, which the command reads and leaves unchanged. With the plugin alone, the same command runs as `PYTHONPATH="<installPath>" python3 -B -m govharness ledger append "<installPath>/governance" ...`, with `installPath` from `claude plugin list --json`. Without the harness, the entry is one line of JSON with the fields of STND.HARN.7, and [`harness/README.md`](../harness/README.md) shows how to compute its hash by hand. Until a class is recorded, an agent that needs it halts that line of work and refers it to you (GOV.13).

5. Tell the project's agents where the governance is. Under the defaults, the agent instructions are the provisions of STND.INSTR (STND.DFLT.21). A few lines in the project's `AGENTS.md` or `CLAUDE.md` name the corpus and the records; [installation.md](installation.md#pointing-other-agents-at-the-governance) has an example.

6. Grant the authorizations that routine work needs. Installing software, changing the system configuration, network access, writes to a remote system, and actuating hardware each need a recorded authorization of the human owner (PRIME.7, GUARD.10). Under the defaults, an agent records an authorization that you give it directly as a ledger entry with itself as actor and your grant quoted (STND.DFLT.17). For a project with a constitution, STND.PROJ.3 proposes a set of standing authorizations that let routine work run unattended.

## Recording an expected class

Work often starts at CSQ3 or CSQ4 and is promoted when someone comes to rely on it. Where you already know the class the work will reach, you may state it, with the use that reaches it, in the rationale of the classification entry. As the corpus stands, that statement is information only: the classification record has no field for an expected class (STND.CLASS.5), and no provision reads one or asks the design to anticipate it. See [Known limitations](#known-limitations).

## Raising the class later

A class attaches to the use of the work. It moves toward CSQ0 whenever reliance or exposure grows, and away from CSQ0 only by your recorded decision (GOV.14). STND.CLASS.7 lists the events that call for a reassessment: growing reliance or exposure, a harm scenario that an agent reports, or an incident that shows a consequence the classification omits. Until you record the reassessment, the work is not relied upon in the use that occasioned it.

To raise the class:

1. Draft the revised classification, with `/governance:classifying-work CSQ2` or by hand.
2. Record it as a new entry of the project's ledger, as in step 4 above.
3. Check what the new class adds. The table of STND.CLASS.10 lists the obligations that apply only from CSQ2, CSQ1, or CSQ0; STND.CLASS.18 gives the reviewer independence of each class; and STND.CLASS.19 has the project audited by the auditor of the new class before the work is relied upon at that class. Work moved to a more severe class meets that class's obligations before it is relied upon at it; nothing is grandfathered (GOV.14).
4. Write a project constitution if the project now promotes results, releases software, or drives hardware (GOV.20).

Nothing is reinstalled. The class lives in the project's records, not in the plugin or the harness, and the next session reads it there.

## What the human is asked to do, by class

The custodian's aim is that the human owner is asked for interaction only on request, or when the work is of CSQ1 or CSQ0. The corpus as it stands asks more than that below CSQ1; the [known limitations](#known-limitations) name the largest cases.

At every class, the prime directives, GUARD, and GOV bind (GOV.10), and these acts are the human owner's:

- executing a reserved action: an irrecoverable action, a bulk action, a bulk retrieval, a monetary transaction, or a hazardous actuation (PRIME.6);
- granting each authorization, for the actions that PRIME.7 lists (GUARD.10);
- deciding each line of work that an agent halts and refers, from its findings and justification statement (PRIME.14, STND.DFLT.20);
- adopting the judgments that set the burden on the work: the classification, promotion of a result, axioms, the hazard analysis, the reserved-action register, estimates for implicit expenditure, and the decision to release or deploy (GOV.50);
- under the defaults, deciding whether work continues after a unit of work halts at its third attempt without progress (STND.DFLT.9), and reporting each governance failure to the custodians from a report an agent drafts (STND.DFLT.12).

The rest depends on the class:

| Class | Review of each change (STND.CLASS.18) | Compliance audit (STND.CLASS.19) | Further acts of the human owner |
| --- | --- | --- | --- |
| CSQ4 | No row of the table applies | When the project is retired, by an actor who did not author the work; an agent is eligible | Recording the class. Promoting a result before it is reported (QA.11) |
| CSQ3 | By an actor other than the author; an agent is eligible | At most 36 months after the classification or the previous audit, and at retirement; an agent is eligible | As for CSQ4. Each result relied upon beyond the author and the unit of work is promoted first (QA.11) |
| CSQ2 | As for CSQ3, and by an actor not directed by the author: a human, or an agent of a different configuration from an authoring agent | Before a result is first relied upon, and at most 24 months after the previous audit; an agent of a different configuration from every authoring agent is eligible | As for CSQ3. The release decision (QA.10) |
| CSQ1 | As for CSQ2, and a human reviews, before each promotion or release, the changes since the previous such review that affect a contract or a reported result | Before the first release, and at most 12 months after the previous audit; an agent of a different configuration is eligible | As for CSQ2. Under the defaults, the work is assured: each of your entries is signed and verified against the signer register (STND.DFLT.23) |
| CSQ0 | As for CSQ1, and a human who did not author the change reviews each change to a safety-related component | Before each release, and at most 6 months after the previous audit, by a human who did not author the work | As for CSQ1. Adopting the hazard analysis (PRIME.13); recording where proof or exhaustive checking is not feasible (STND.CLASS.10); a recorded exercise in which a person resumes the work without the automation (STND.CLASS.10, INTPR.12) |

## Known limitations

The deep review of 2026-10-28 found places where the corpus, read as written, asks more of the human owner than intended or stops an agent outright. Proposed corrections go to the custodian for ratification; until they are ratified and entered in the ledger, the text below describes the corpus as it stands. The findings, with the exact text and the proposed fixes, are in the review's reports: [corpus-core.md](../review-records/deep-review-2026-10-28/corpus-core.md) for those numbered CC and [anthropic-docs.md](../review-records/deep-review-2026-10-28/anthropic-docs.md) for those numbered AD.

### An agent's own operating cost needs an authorized estimate (CC1)

An agent's operating cost is implicit expenditure (GUARD.14), and implicit expenditure proceeds only on an estimate that the human owner authorizes (PRIME.8). No default authorizes one (GOV.22). Read literally, an agent under the defaults holds no authorized estimate for its own cost before any unit of work, at every class. Within the corpus as it stands, you can authorize an estimate for the work, or set the discipline that governs agent cost and record it (GUARD.14); STND.DFLT.26 covers an enforced spending cap.

### Builds and test runs count as bulk actions (CC2)

A destructive action is one that removes or overwrites an item, or alters it other than by appending (the term in STND.DFLT). Before one, an agent lists each item it affects by path (STND.DFLT.24), and a destructive action whose scope is not listed and verified beforehand is a bulk action, reserved to the human owner (GUARD.6, PRIME.6). A build, a test run, a formatter, a code generator, or a package installation overwrites outputs that no one lists in advance. Read literally, each such run is reserved to you at every class. No route around this exists in the corpus short of listing every output before each run.

### Tools that write outside the work halt the agent (CC3)

By default an agent writes only within the top directory of the work (the term Working bounds in STND.DFLT), and a write outside the bounds halts that line of work and refers it (STND.DFLT.25). Compilers, package managers, version control, and interpreters keep caches and configuration under the home directory, and scratch files go to the system's temporary directory. The first build or install halts, and the halt recurs for each new location. The term lets an entry that STND.DFLT.23 accepts open further locations, so you can record one entry that names the cache and temporary locations your tools use.

### Recording CSQ1 or CSQ0 cannot be undone without a signer register (AD2)

Under the defaults, an entry of the human owner that records CSQ1 or CSQ0 makes the work assured, signed or not, and only a signed entry ends that. For assured work, STND.DFLT.23 accepts only entries that you sign and that a verifier confirms against a key in the signer register. No signer register is founded, and the signature feature is not adopted. So once an unsigned entry records CSQ1 or CSQ0, no later entry of yours is accepted: no revision of the class, no lowering, and no lasting authorization. Promotion works up to CSQ2. Record CSQ1 or CSQ0 only after a signer register exists for your ledger.

### The classification is a ledger line that only you can write (AD3)

Under the defaults, the classification is a ledger transaction that you adopt (STND.DFLT.13), and an agent may not append an entry in your name (STND.DFLT.5). An authorization does not need this step, because an agent records the grant you give it (STND.DFLT.17); the classification and each later revision of it do. Until the class is recorded, an agent that needs it halts and refers (GOV.13). With the harness, the entry is the one command in step 4 above; without it, you write and hash a line of JSON by hand.

### Also reported

- No provision lets a classification record an expected class, or asks the design to anticipate one (CC32).
- At CSQ3, each result that a teammate or a second agent builds on is relied upon beyond its author and needs its own recorded promotion (QA.11, CC5).
- What a promotion owes for changes made at the lower class is not settled: read literally, each change is reviewed again at the new independence (GOV.14, STND.CLASS.18, CC7).
