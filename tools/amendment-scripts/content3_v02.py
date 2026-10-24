"""Step 3, first round: STND.WPROC (work process) and STND.CREW (agent roles), draft 0.2."""

from content import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-20"

# ================================================================ STND.WPROC
WPROC = dict(
    id="STND.WPROC", title="Work process standard",
    instantiates=["GOV.19", "GOV.21"],
    sections=[
        ("Purpose and scope", """This standard is the part of a work process (QA.2) that the version history carries, for covered work under version control. It records each unit of work, from the roadmap down to the smallest fix, in the records of the development line; carries each unit on its own branch; integrates concurrent work up the branch hierarchy, each merge preceded by an update from the parent, the checks the change affects, and its review; and makes each advance of the main line a release that the human owner decides. The agent roles standard gives the planning, review, and audit stages that complete the work process. STND.WPROC.12 and STND.WPROC.13 instantiate GOV.50 or a prime directive and are binding at every class; every other provision is a default (GOV.19), which a project instrument replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). The defaults apply to work with or without a project constitution; for work without one, STND.DFLT.7 to STND.DFLT.10 still give the definition of done, the contents of records, the stopping bound, and the defect schedule, which these provisions complement. Below the release, no provision asks the human owner for a decision (STND.DRAFT.42). The standard uses the concepts of branch and merge that version-control systems share and names no system or tool (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Unit of work, Release, and Review have the meanings the Lexicon gives them; Agent configuration has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Branch | A line of the version history of the work that changes apart from the others until it is merged. |
| Merge | The combination of the changes of one branch into another so that the history of the target contains every commit of the source, recorded in that history without rewriting it. |
| Main line | The branch from which the work is released or deployed. |
| Development line | The branch, made from the main line, into which completed units of work are integrated before a release, and whose update makes no revision available for use beyond development. |
| Unit branch | The branch on which one unit of work is carried out. |
| Parent branch | The branch from which another branch was made. |
| Roadmap | The recorded, ordered set of milestones of the work, each with its definition of done. |
| Milestone | A unit of work that the roadmap names, whose completion a release delivers. |
| Feature | A unit of work within a milestone or within another feature. |
| Release record | The record on which the human owner decides a release, with the content that STND.WPROC.13 gives. |"""),
        ("Notes", """The work breakdown and the branch hierarchy are one structure. The roadmap names milestones; a milestone divides into features, and a feature into features of its own, to whatever depth the work needs; each unit that changes the work has a branch made from its parent unit's branch, or from the development line where the parent has none (STND.WPROC.5), and is merged back only into that branch, one merge at a time (STND.WPROC.7). Concurrent units therefore meet only at their common parent: siblings never merge into each other, and each picks up its siblings' merged work by merging its parent into itself (STND.WPROC.8). The branch hierarchy, with one merge at a time into each branch, is the protocol for concurrent change that DSGN.15 and AGENT.39 ask for; its invariant, that every branch's history contains its parent's state at its last update, is read from the history itself. The history need not be linear. Rewriting or force-overwriting history is reserved to the human owner (GUARD.5, PRIME.6), so agents combine work by merges, never by rewriting branches, and a merge keeps every commit of its source, so the attribution of STND.WPROC.2 survives. Deleting a branch or a permanent name is a destructive remote or bulk action that no standing authorization covers (STND.PROJ.3); merged branches stay.

The records of the work live on the development line (STND.WPROC.4): the roadmap, each unit record, defect tracking, the record of referrals, research notes, and the ledger. Kept there and changed one change at a time, an append-only record never forks between branches, so the hash chain of a ledger and the order of entries survive (PRIME.5, GOV.36), and every agent and the human owner read one current state. A unit record holds dated entries, its definition of done, acceptance criteria, plan, and status, so its status changes by a new entry rather than an edit (STND.WPROC.1), and it is read from the repository itself, without a separate tracker, surviving the loss of every tool (INTPR.12). A project that uses a tracker as well records its identifiers in the unit record. A halted unit's record states the halt and its reason (GUARD.3).

A fix branches from the most upstream branch that its defect affects: a defect in a released revision is fixed from the main line, released, and reaches the development line and each branch below it as each merges its parent into itself; a defect found only in a unit's own change is fixed on that unit's branch (STND.WPROC.6).

Before a branch is merged into its parent, the parent's current state is merged into it, which is where conflicts are resolved; a resolution is part of the change that the checks and the review then judge (STND.WPROC.8 to STND.WPROC.10). A conflict that the records of the two units do not decide goes to the lead agent, which refers it only where it needs a decision of the human owner. If the parent moves again before the merge, the update, checks, and review are repeated. A check too costly for every merge, such as a long stochastic run or a synthesis, is deferred to the release under RSRC.12, recorded in the unit record, and run on the revision released (STND.WPROC.13). The review is recorded with its reviewer and configuration, so that the independence that STND.CLASS.18 requires for the class is read from the record; its CSQ1 row is a human review batched before each release, and its CSQ0 row a human review of each change to a safety-related component. Each finding is resolved and confirmed by the reviewer, or recorded in defect tracking with whether it blocks release, before the merge.

An agent then merges into any parent other than the main line without a decision of the human owner (STND.WPROC.11). A project that wants per-merge approval at some class states it as a tighter project rule. Pushing a merge to a remote repository is a remote write that proceeds under a standing authorization of the kind STND.PROJ.3 proposes, where the human owner has granted one; otherwise only the push is referred.

An advance of the main line, by merge, fast-forward, or commit, releases a revision, because the main line is the branch from which the work is used beyond its development. The human owner decides it at every class (GOV.50, QA.10, STND.WPROC.12). The decision is recorded, names the revision, and, where an agent is to carry it out, is the per-action authorization that GUARD.11 asks for the advance, its publication, and its permanent name; afterwards the main line stands at exactly that revision, so the development line merges the main line into itself before the revision is proposed. The custodian's first model had the human owner execute the merge at CSQ2 and above; the decision that names the revision keeps the same control at the cost of one record, and the human owner remains free to execute it. The proposal is a release record that puts first the items on which the decision turns (STND.WPROC.13); it carries, among the items other provisions require of the record of a release, the dependencies left unchecked under STND.DEPS.7, the human review of the CSQ1 row of STND.CLASS.18, and the hazard analysis of STND.CLASS.17 at CSQ0, and cites a record that a profile requires, such as that of HDES.ASIC.12, rather than restating it. Each release carries a permanent name in the history (STND.WPROC.14).

Under STND.CLASS.10, each default provision instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3; work of CSQ4 omits it. STND.WPROC.12 applies at every class, because the release decision is the human owner's at every class (GOV.50). STND.WPROC.13 applies at every class through AGENT.47, which tightens QA.10 at CSQ3 and CSQ4 at the cost of one record per release, so that no release rests on an unstated basis (PRIME.15). No other provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Unit records in history", "Records", """
Each unit of work SHOULD have a unit record of dated entries that states its definition of done, its acceptance criteria, its plan, and its status, under an identifier that its branch and its commits carry (QA.2).
""", ["QA.2"]),
        P(2, "Attribution of commits", "Records", """
Each commit SHOULD name the unit of work it serves and its author, and, for an agent author, identify the agent's configuration by a reference to the record of REPRO.11 (REPRO.11).
""", ["REPRO.11"]),
        P(3, "Main and development lines", "Branches", """
The version history of the work SHOULD hold a main line and a development line made from it (QA.2).
""", ["QA.2"]),
        P(4, "Records on the development line", "Records", """
The records of the work, the roadmap, the unit records, defect tracking, and the ledger included, SHOULD be kept on the development line and changed there one change at a time (QA.2, REPRO.12).
""", ["QA.2", "REPRO.12"]),
        P(5, "Unit branches", "Branches", """
Each unit of work that changes the work, other than the fix of a defect under STND.WPROC.6, SHOULD be carried out on a unit branch made from the branch of its parent unit (QA.2). A unit of work whose parent unit has no branch SHOULD have its unit branch made from the development line (QA.2).
""", ["QA.2"], refs=["STND.WPROC.6"]),
        P(6, "Fix branches", "Branches", """
A fix of a defect SHOULD be carried out on a branch made from the most upstream branch that the defect affects, and merged into that branch (QA.4, VV.8). Each branch descended from that branch that carries the defect SHOULD receive the fix by the merge of its parent branch into it (QA.13, VV.8).
""", ["QA.4", "QA.13", "VV.8"]),
        P(7, "Hierarchical integration", "Integration", """
A unit branch SHOULD be merged only into its parent branch, one merge at a time (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"]),
        P(8, "Parent update before merge", "Integration", """
Before a branch is merged into its parent branch, the current state of the parent branch SHOULD be merged into it (QA.2, DSGN.15). Where the parent branch changes after that update, the update and the checks and review of STND.WPROC.9 and STND.WPROC.10 SHOULD be repeated before the merge (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"], refs=["STND.WPROC.9", "STND.WPROC.10"]),
        P(9, "Checks before merge", "Integration", """
Before a branch is merged into its parent branch, each check that the change is able to affect, other than a check deferred to the release under RSRC.12 and recorded in the unit record, SHOULD pass on the branch as updated under STND.WPROC.8 (VV.8, RSRC.11, RSRC.12).
""", ["VV.8", "RSRC.11", "RSRC.12"], refs=["STND.WPROC.8"]),
        P(10, "Recorded review at merge", "Integration", """
Before a branch is merged into its parent branch, the review of the branch as updated under STND.WPROC.8 that STND.CLASS.18 requires SHOULD be recorded, with its reviewer and the reviewer's agent configuration (QA.7, QA.8). Before that merge, each finding of the review SHOULD be resolved with the resolution confirmed by the reviewer, or recorded in defect tracking with whether it blocks release (QA.4, QA.7).
""", ["QA.7", "QA.8", "QA.4"], refs=["STND.WPROC.8", "STND.CLASS.18"]),
        P(11, "Merges below the release", "Integration", """
Where STND.WPROC.8, STND.WPROC.9, and STND.WPROC.10 are met, an agent MAY merge a branch into its parent branch, other than the main line, without a decision of the human owner (QA.2).
""", ["QA.2"], refs=["STND.WPROC.8", "STND.WPROC.9", "STND.WPROC.10"]),
        P(12, "Main-line changes", "Release", """
The main line SHALL be advanced, whether by merge, by fast-forward, or by commit, only to a revision that a recorded decision of the human owner to release names (GOV.50, QA.10). For an advance that an agent carries out, the decision SHALL be recorded as a per-action authorization of the advance, of its publication, and of its permanent name (GUARD.10, GUARD.11, PRIME.7). After the advance, the main line SHALL stand at the revision that the decision names (QA.10).
""", ["GOV.50", "QA.10", "GUARD.10", "GUARD.11", "PRIME.7"], mode="binding"),
        P(13, "Release record", "Release", """
An agent that proposes a release SHALL record and present to the human owner a release record that states first the items on which the decision turns, and then the revision, the units of work it completes, the outcome of the checks run on that revision, each check or review of those units that failed, was skipped, or was weakened, each open defect with whether it blocks, each waiver relied upon with its expiry, each departure that their work reports state, the findings of each audit, and each item that another provision requires the record of a release to state (QA.10, GOV.50, AGENT.47, RSRC.10).
""", ["QA.10", "GOV.50", "AGENT.47", "RSRC.10"], mode="binding"),
        P(14, "Permanent release names", "Release", """
Each revision to which the main line advances SHOULD carry, in the version history, a permanent name that identifies the release (REPRO.1).
""", ["REPRO.1"]),
    ],
)

# ================================================================ STND.CREW
CREW = dict(
    id="STND.CREW", title="Agent roles standard",
    instantiates=["GOV.19", "GOV.48"],
    sections=[
        ("Purpose and scope", """This standard fixes the roles that agents take in work under the work process standard: a lead agent that the human owner directs and that delegates the work, research and planning agents that prepare each milestone and feature, implementing agents that carry out the plan, review agents that examine each change cold, and audit agents that examine the work before each release. It states what each role produces and to whom it reports, and how the lead agent keeps the human owner's burden to a few batched decisions. One agent takes several roles in sequence, and the lead agent carries out a small unit itself, except that no agent reviews a change that it authored (QA.7), the independence of a reviewer from the author rises with the class (STND.CLASS.18), and that of an auditor follows STND.CLASS.19. STND.CREW.2, STND.CREW.3, and STND.CREW.15 instantiate a prime directive, GUARD, or GOV and are binding at every class; every other provision is a default (GOV.19). The standard names no model, provider, or tool (GOV.18), and sets no limit on the number of agents or the depth of delegation (GOV.18, AGENT.9)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Agent configuration has the meaning that STND.CLASS gives it; Attempt without progress has the meaning that STND.DFLT gives it; Main line, Milestone, Feature, Roadmap, Unit branch, Parent branch, and Release record have the meanings that the work process standard gives them, the last by STND.WPROC.13.

| Term | Definition |
| --- | --- |
| Lead agent | The agent that takes its instructions for the work from the human owner directly and directs the other agents working on it. |
| Research agent | An agent that investigates a question that a plan depends on and records a research note. |
| Planning agent | An agent that records the plan of a unit of work. |
| Implementing agent | An agent that carries out a unit of work that changes the work. |
| Review agent | An agent that performs the review of a change. |
| Audit agent | An agent that examines a revision to be released along the dimensions of STND.CREW.12, and reports its findings. |
| Capability level | The model of an agent together with each setting of that model that changes how capable and how costly its work is, such as its reasoning effort. |
| Capability order | The order of the capability levels that the provisioned environment admits, from least to most capable, as the project records it or, absent a record, as their provider states it. |"""),
        ("Notes", """The lead agent is the session that the human owner talks to. It delegates units to agents it directs and keeps its own context free for the human owner, so that it answers at once while the work goes on (STND.CREW.1); a unit that is cheaper and quicker to do than to delegate, answering the human owner meanwhile included, it does itself, except where the class asks for a reviewer that the author does not direct, because every reviewer is directed by the lead (STND.CLASS.18). It answers each status request of the human owner for every agent working under it, as AGENT.20 asks of a directing agent.

It keeps one record of everything that awaits the human owner, referrals and release records alike, each referral in the form of the findings and justification statement of the project's agent instructions (STND.DFLT.20 by default), and presents the open entries together in its next report, those that halt the most lines of work first, so that the human owner decides in batches while every other line continues (STND.CREW.2, AGENT.15). A directed agent states its referral in its work report to the lead agent, which enters it; an incidental encounter with a secret (PRIME.10) and a passage directing a forbidden or reserved action (STND.INSTR.6) are reported at once and also entered. It records each provision that the work finds ambiguous, in conflict, or halting a line of work that no LVL0 obligation requires to halt, and drafts the amendment proposal, which the human owner sends to the provision's adopter (STND.CREW.3, GOV.46, GOV.47, GOV.49); recording does not replace a referral that PRIME.14, GOV.4, or GOV.6 requires.

Research and planning scale with the unit. The roadmap and each milestone are researched and planned before they are recorded or begun, and each feature should be (STND.CREW.4). Research covers the state of the work, its documentation, its governance, and its build, the knowledge base and workbench consulted first (AGENT.28), and, where the plan depends on practice outside the work, current practice retrieved under the authorization for research retrieval, the agents of one research effort sharing its bound (AGENT.46); it is recorded as research notes in the workbench (AGENT.31, STND.INSTR.9). Research is most worth its cost for specialized work and for fields that change quickly. Deeper units are planned where their complexity calls for it, and every unit is researched and replanned after its second consecutive attempt without progress, within its stopping rule; the units a replan creates inherit the count, so a cycle of replanning cannot reset the stopping rule (STND.CREW.5, QA.3). A plan states each unit it creates, the research it rests on, and the instruction of the human owner from which each milestone derives, which is the test of alignment that the release audit applies (STND.CREW.6, STND.CREW.12). An implementing agent follows the plan and records each departure with its reason (AGENT.22, AGENT.47), and reviews its own change before handing it to review (STND.CREW.7); that self-review is not the review of QA.7.

A defect that an agent finds outside its unit is recorded by that agent in defect tracking, as QA.5 asks, together with its report to the human owner; a needed change that is not a defect goes to the lead agent, which assigns both to units, so that concurrent agents do not each fix it (STND.CREW.8). The custodian's model asked for this report while concurrent work is in progress; it applies always, since the lead agent assigns the work either way. The agent that directs a parent unit merges each child branch into it, one at a time, so that each branch has one writer (STND.CREW.9, STND.WPROC.7).

A review agent receives the change, its acceptance criteria, the governance that applies, the departures and weakened checks that the author's work report states, and only the context it needs to judge them, without the author's reasoning, so that it judges the change as a cold reader would (STND.CREW.10). It looks for the ways the change fails and reports each finding with its evidence to the lead agent, which checks it (AGENT.12), assigns the remediation of each finding it upholds, and records why it does not uphold the others; the review agent does not change the change, which would make it an author whose change needs another review (STND.CREW.11). The reviewer confirms each resolution before the merge (STND.WPROC.10).

An audit examines the revision to be released, the changes since the last audit, along each dimension of STND.CREW.12, the first release examining the whole work, and its findings go into the release record (STND.WPROC.13). The auditor is of the Auditor column of STND.CLASS.19 for the class, a human at CSQ0 (STND.CREW.13), and of a capability level no lower than that of each agent author of the work, unless the lead agent records that a lower level completes the audit reliably (STND.CREW.14). The custodian's "elite-tier" auditor is read relative to the authors, so that the audit is never weaker than the work it judges, without paying for the most capable level where the work is simple.

A directing agent gives each directed agent the least costly capability level able to complete its unit reliably within its stopping rule (AGENT.10). An attempt without progress whose cause the directing agent has not found and removed, a wrong plan or missing information for instance, is evidence that the level was too low, so the next attempt goes to the next level in the capability order, within the estimate and the operating envelope, and the change is recorded as an alteration of the plan (STND.CREW.15, PRIME.8, AGENT.22).

Under STND.CLASS.10, each default provision instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3. STND.CREW.2 and STND.CREW.3 bind at every class at the cost of one record each; STND.CREW.15 is a recommendation within a provision that instantiates AGENT.10 and GUARD.14. No provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Lead agent delegation", "Lead agent", """
Where the estimated operating cost and time of carrying out a unit of work itself, answering the human owner meanwhile included, are below those of delegating it, the lead agent MAY carry out the unit itself (INTPR.6). Where STND.CLASS.18 requires for the work a reviewer that the author does not direct, the lead agent SHOULD NOT itself carry out a unit of work that changes the work (QA.7, QA.8). The lead agent SHOULD delegate each other unit of work to agents that it directs (INTPR.6).
""", ["INTPR.6", "QA.7", "QA.8"], refs=["STND.CLASS.18"]),
        P(2, "Queue of owner decisions", "Lead agent", """
The lead agent SHALL keep, in the records of the work, one record of each referral and each release record that awaits a decision of the human owner (PRIME.14, RSRC.10). The lead agent SHALL present the open entries of that record together in its next report to the human owner, those that halt the most lines of work first (PRIME.14, RSRC.10). A report that PRIME.10 or STND.INSTR.6 requires when its matter is found SHALL be made at once and also entered in that record (PRIME.10, PRIME.14).
""", ["PRIME.14", "RSRC.10", "PRIME.10"], refs=["STND.INSTR.6"], mode="binding"),
        P(3, "Governance findings", "Lead agent", """
The lead agent SHALL record, in the records of the work, each provision that the work finds ambiguous, in conflict with another, or halting a line of work that no obligation of LVL0 requires to halt (GOV.46). The lead agent SHOULD draft for the human owner, for each such provision, an amendment proposal that the human owner sends to its adopter (GOV.46, GOV.47, GOV.49).
""", ["GOV.46", "GOV.47", "GOV.49"], mode="binding"),
        P(4, "Plans by level", "Research and planning", """
Before the roadmap is recorded or changed, a planning agent SHALL record its plan, drawing on research notes that cover the state of the work, its documentation, its governance, and its build, and each other question that the plan depends on (QA.2, AGENT.28, AGENT.31). Before work on a milestone begins, a planning agent SHALL record its plan in the same way (QA.2, AGENT.31). Before work on a feature begins, a planning agent SHOULD record its plan in the same way (QA.2, AGENT.31).
""", ["QA.2", "AGENT.28", "AGENT.31"]),
        P(5, "Replanning after failure", "Research and planning", """
After the second consecutive attempt without progress at a unit of work, a planning agent SHOULD research and replan that unit before the next attempt that its stopping rule permits (QA.2, QA.3). A unit of work that such a replan creates to continue that unit SHALL inherit its count of attempts without progress (QA.3).
""", ["QA.2", "QA.3"]),
        P(6, "Plan content", "Research and planning", """
Each plan SHOULD state each unit of work it creates, with its parent unit, its dependencies on other units, its effort estimate under AGENT.6, the assessment of AGENT.39 for the units that run in parallel, the capability level that it assigns under AGENT.10, the research notes on which it rests, and, for a milestone, the instruction of the human owner from which it derives (QA.2). Each plan SHOULD create the unit record of STND.WPROC.1 for each unit of work it creates (QA.2).
""", ["QA.2"], refs=["AGENT.6", "AGENT.39", "AGENT.10", "STND.WPROC.1"]),
        P(7, "Self-review before review", "Implementation", """
Before an implementing agent hands a change to review, it SHOULD examine the change against its acceptance criteria and fix each finding (QA.2, VV.8).
""", ["QA.2", "VV.8"]),
        P(8, "Out-of-scope findings", "Implementation", """
An agent that finds a needed change outside the scope of its unit of work, other than a defect that it records under QA.5, SHOULD report it to the lead agent in its work report (AGENT.19). The lead agent SHOULD assign each defect recorded under QA.5 and each such change to a unit of work (QA.4, QA.5).
""", ["AGENT.19", "QA.4", "QA.5"]),
        P(9, "Integration of unit branches", "Implementation", """
The merge of a unit branch into its parent branch SHOULD be made by the agent that directs the parent unit, one merge at a time (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"]),
        P(10, "Context given to reviewers", "Review and audit", """
A review agent SHOULD receive the change, its acceptance criteria, the governance that applies to it, the departures and the skipped or weakened checks that the author's work report states under AGENT.47, and only the other context needed to judge them, without the author's reasoning (QA.7, QA.8).
""", ["QA.7", "QA.8"], refs=["AGENT.47"]),
        P(11, "Findings of review", "Review and audit", """
A review agent SHOULD report each finding, with its evidence, to the lead agent (QA.7). The lead agent SHOULD check each finding against the acceptance criteria, assign the remediation of each finding it upholds, and record the reason for each finding it does not uphold (QA.2, QA.7). A review agent SHOULD NOT change the change it reviews (QA.7).
""", ["QA.7", "QA.2"]),
        P(12, "Release audit", "Review and audit", """
Before each release, an audit agent SHOULD examine the revision to be released, for the changes since the last audit and along each dimension of the table of this provision, and report its findings to the lead agent for the release record (QA.7, QA.10). Before the first release, the audit SHOULD examine the whole work (QA.7, QA.10).

| Dimension |
| --- |
| Alignment with the instructions of the human owner |
| Conformance to the governance that applies |
| Alignment with the roadmap and the recorded plans |
| Support of each claim by evidence |
| Correctness, mathematical soundness included |
| Coverage of the acceptance criteria by tests |
| Performance against the stated budgets |
| Safety, the currency of the hazard analysis included |
| Security, the currency of the threat model included |
| Dependencies, their pinned revisions and advisories included |
| Reproducibility of results |
| Consistency of documentation with the work |
""", ["QA.7", "QA.10"], defines=["audit-dimensions"]),
        P(13, "Audit independence", "Review and audit", """
The audit of STND.CREW.12 SHOULD be made by an auditor that the Auditor column of the table of STND.CLASS.19 gives for the class of the work (QA.7).
""", ["QA.7"], refs=["STND.CREW.12", "STND.CLASS.19"]),
        P(14, "Audit capability level", "Review and audit", """
An audit agent SHOULD be of a capability level no lower in the capability order than that of each agent author of the work it audits (QA.2). Where the lead agent records that a lower capability level completes an audit reliably, the audit agent MAY be of that level (QA.2).
""", ["QA.2"]),
        P(15, "Capability escalation", "Delegation", """
After an attempt of a directed agent at a unit of work makes no progress for a cause that the directing agent has not found and removed, the directing agent SHOULD give the next attempt the next level in the capability order that the estimate and the operating envelope of the work permit (AGENT.10, GUARD.14, PRIME.8). The directing agent SHOULD record that change of level as a decision that alters the plan (AGENT.22).
""", ["AGENT.10", "GUARD.14", "PRIME.8", "AGENT.22"], mode="binding"),
    ],
)

NEW_DOCS3 = [WPROC, CREW]
