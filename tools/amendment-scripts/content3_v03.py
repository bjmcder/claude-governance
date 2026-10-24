"""Step 3, first round: STND.WPROC (work process) and STND.CREW (agent roles), draft 0.2."""

from content import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-20"

# ================================================================ STND.WPROC
WPROC = dict(
    id="STND.WPROC", title="Work process standard",
    instantiates=["GOV.19", "GOV.21"],
    sections=[
        ("Purpose and scope", """This standard is the part of a work process (QA.2) that the version history carries, for covered work under version control. It records each unit of work, from the roadmap down to the smallest fix, beside its change, and keeps the records shared across units on the development line; carries each unit on its own branch; integrates concurrent work up the branch hierarchy, each merge preceded by an update from the parent, the checks the change affects, and its review; and makes each advance of the main line a release that the human owner decides. The agent roles standard gives the planning, review, and audit stages that complete the work process. STND.WPROC.12 and STND.WPROC.13 instantiate GOV.50 or a prime directive and are binding at every class, the second asking only what the release decision and AGENT.47 already rest on; every other provision is a default (GOV.19), which a project instrument replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). The defaults apply to work with or without a project constitution; for work without one, STND.DFLT.7 to STND.DFLT.10 still give the definition of done, the contents of records, the stopping bound, and the defect schedule, which these provisions complement. Below the release, no provision asks the human owner for a decision (STND.DRAFT.42). The standard uses the concepts of branch and merge that version-control systems share and names no system or tool (GOV.18)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Unit of work, Release, and Review have the meanings the Lexicon gives them; Agent configuration has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Branch | A line of the version history of the work that changes apart from the others until it is merged. |
| Merge | The combination of the changes of one branch into another so that the history of the target contains every commit of the source, recorded in that history without rewriting it. |
| Main line | Each branch from which the work is released or deployed. |
| Development line | The branch, made from the main line, into which completed units of work are integrated before a release, and whose update makes no revision available for use beyond development. |
| Unit branch | The branch on which one unit of work is carried out. |
| Parent branch | The branch from which another branch was made. |
| Roadmap | The recorded, ordered set of milestones of the work, each with its definition of done. |
| Milestone | A unit of work that the roadmap names, whose completion a release delivers. |
| Feature | A unit of work within a milestone or within another feature. |
| Release record | The record on which the human owner decides a release, with the content that STND.WPROC.13 and STND.WPROC.14 give. |
| Permanent name | A name for one revision that is never moved to another revision or reused. |"""),
        ("Notes", """The work breakdown and the branch hierarchy are one structure. The roadmap names milestones; a milestone divides into features, and a feature into features of its own, to whatever depth the work needs; each unit that changes the work has a branch made from its parent unit's branch, or from the development line where the parent has none (STND.WPROC.5), and is merged back only into that branch, one merge at a time (STND.WPROC.7). Concurrent units therefore meet only at their common parent: siblings never merge into each other, and each picks up its siblings' merged work by merging its parent into itself (STND.WPROC.8). The branch hierarchy, with one merge at a time into each branch, is the protocol for concurrent change that DSGN.15 and AGENT.39 ask for; its invariant, that every branch's history contains its parent's state at its last update, is read from the history itself. The history need not be linear. Rewriting or force-overwriting history is reserved to the human owner (GUARD.5, PRIME.6), so agents combine work by merges, never by rewriting branches, and a merge keeps every commit of its source, so the attribution of STND.WPROC.2 survives. Merged branches stay; the deletion of a remote branch or of a permanent name is outside the standing authorizations that STND.PROJ.3 proposes.

Records follow the work they concern (STND.WPROC.4). A unit's record, created on its parent's branch before the unit branch is made, travels with the branch, so the unit's agents read it, its research notes, and its records of AGENT.22 to AGENT.25 where they work, and the records reach the development line by the merges that carry the work; each directing agent writes the records of the units it directs on its own branch (AGENT.21). Only the records shared across units are kept on the development line and changed there one change at a time: the ledger, whose hash chain would fork if two branches appended to it (PRIME.5, GOV.36), the roadmap, defect tracking, and the record of decisions awaiting the human owner. A unit record holds dated entries, so its status changes by a new entry rather than an edit (STND.WPROC.1), and it is read from the repository itself, without a separate tracker, surviving the loss of every tool (INTPR.12). A project that uses a tracker as well records its identifiers in the unit record. A halted unit's record states the halt and its reason (GUARD.3).

A fix branches from the most upstream branch that its defect affects: a defect in a released revision is fixed from the main line, released, and reaches the development line and each branch below it as each merges its parent into itself, while the development line continues on its other work meanwhile (AGENT.15); a defect found only in a unit's own change is fixed on that unit's branch (STND.WPROC.6).

Before a branch is merged into its parent, the parent's current state is merged into it, which is where conflicts are resolved; a resolution is part of the change that the checks and the review then judge (STND.WPROC.8 to STND.WPROC.10). A conflict that the records of the two units do not decide goes to the lead agent, which refers it only where it needs a decision of the human owner. If the parent moves again before the merge by a change to its work rather than to the shared records, the update and checks are repeated, and the repeated review concerns what the new update changed, a conflict resolution above all. A check too costly for every merge, such as a long stochastic run or a synthesis, is deferred to the release under RSRC.12, recorded in the unit record, and run on the revision released. The review of each merge is recorded with its reviewer and configuration, at the agent rows of STND.CLASS.18: the CSQ2 row for work of CSQ2 and more severe classes, the CSQ3 row otherwise. The human reviews that the CSQ1 and CSQ0 rows add fall before the release, which QA.7 requires, and the release record carries them (STND.WPROC.14), so that no merge below the release waits on a human. Each finding is resolved and confirmed by the reviewer, or recorded in defect tracking with whether it blocks release, before the merge.

An agent then merges into any parent other than a main line without a decision of the human owner (STND.WPROC.11). A project that wants per-merge approval at some class states it as a tighter project rule. Pushing a merge to a remote repository is a remote write that proceeds under a standing authorization of the kind STND.PROJ.3 proposes, where the human owner has granted one; otherwise only the push is referred.

Advancing a main line releases a revision, because a main line is a branch from which the work is used beyond its development; a branch that supports an older release is a main line too. The human owner decides each advance at every class (GOV.50, QA.10, STND.WPROC.12). The revision exists before it is named: it is made on the development line or on a fix branch after that branch merged the main line into itself (STND.WPROC.8), so that the advance moves the main line to it without creating a revision that no one approved; the first revision of a new main line is not an advance. The decision is recorded, names the revision, and, where an agent carries it out, is the per-action authorization that GUARD.11 asks for the advance, its publication where the work has a remote, and its permanent name. A blocking defect recorded or a waiver expired after the decision stops the advance, as QA.10 asks. The custodian's first model had the human owner execute the merge at CSQ2 and above; the decision that names the revision keeps the same control at the cost of one record, and the human owner remains free to execute it.

The proposal states, at every class, the revision and what the work reports of its units state under AGENT.47 (STND.WPROC.13), because the release decision is the human owner's (GOV.50) and AGENT.47 instantiates PRIME.2, so that no release rests on an unstated basis. From CSQ3, the release record puts first the items on which the decision turns and gives the rest of what QA.10 asks (STND.WPROC.14); among the records that other provisions require for the release are the dependencies left unchecked under STND.DEPS.7, the human reviews of the CSQ1 and CSQ0 rows of STND.CLASS.18, the analysis of STND.CLASS.17 at CSQ0, and a record that a profile requires, such as that of HDES.ASIC.12, each cited rather than restated. The release record and the decision entry follow the named revision on the development line, so the released revision does not contain them. Each release carries a permanent name in the history (STND.WPROC.15).

Under STND.CLASS.10, each default provision instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3, except that the verification of the invariants of a protocol for shared state, which DSGN.15 asks and STND.WPROC.7 and STND.WPROC.8 instantiate, applies from CSQ2; work of CSQ4 omits them. STND.WPROC.12 and STND.WPROC.13 apply at every class through GOV.50 and AGENT.47 and ask nothing that those provisions do not already rest on. No provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Unit records in history", "Records", """
Each unit of work SHOULD have a unit record of dated entries that states its definition of done, its acceptance criteria, its plan, and its status, under an identifier that its branch and its commits carry, created on the branch from which its unit branch is made (QA.2).
""", ["QA.2"]),
        P(2, "Attribution of commits", "Records", """
Each commit SHOULD name the unit of work it serves and, beyond the attribution that REPRO.5 asks, identify an agent author's configuration by a reference to the record of REPRO.11 (REPRO.11).
""", ["REPRO.11"], refs=["REPRO.5"]),
        P(3, "Main and development lines", "Branches", """
The version history of the work SHOULD hold a main line and a development line made from it (QA.2).
""", ["QA.2"]),
        P(4, "Location of records", "Records", """
The ledger, the roadmap, defect tracking, and the record of decisions awaiting the human owner SHOULD be kept on the development line, each change made on the current state of that line and one change at a time (QA.2, REPRO.12). The records of a unit of work that has a branch SHOULD be kept on that branch until it is merged (QA.2, REPRO.12). The records of a unit of work that has no branch SHOULD be kept on the development line (QA.2, REPRO.12).
""", ["QA.2", "REPRO.12"]),
        P(5, "Unit branches", "Branches", """
Each unit of work that changes the work, other than the fix of a defect under STND.WPROC.6, SHOULD be carried out on a unit branch made from the branch of its parent unit (QA.2). A unit of work whose parent unit has no branch SHOULD have its unit branch made from the development line (QA.2).
""", ["QA.2"], refs=["STND.WPROC.6"]),
        P(6, "Branches for fixes", "Branches", """
A fix of a defect SHOULD be carried out on a branch made from the most upstream branch that the defect affects, and merged into that branch (QA.4, VV.8). Each branch descended from that branch that carries the defect SHOULD receive the fix by the merge of its parent branch into it (QA.13, VV.8).
""", ["QA.4", "QA.13", "VV.8"]),
        P(7, "Hierarchical integration", "Integration", """
Other than for the update of STND.WPROC.8, a unit branch SHOULD be merged only into its parent branch, one merge at a time into the same branch (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"], refs=["STND.WPROC.8"]),
        P(8, "Parent update before merge", "Integration", """
Before a branch is merged into its parent branch, the current state of the parent branch SHOULD be merged into it (QA.2, DSGN.15). Where the parent branch changes after that update by a change outside the records of STND.WPROC.4, the update and the checks and review of STND.WPROC.9 and STND.WPROC.10 SHOULD be repeated before the merge (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"], refs=["STND.WPROC.4", "STND.WPROC.9", "STND.WPROC.10"]),
        P(9, "Checks before merge", "Integration", """
Before a branch is merged into its parent branch, each check that the change is able to affect, other than a check deferred to the release under RSRC.12 and recorded in the unit record, SHOULD pass on the branch as updated under STND.WPROC.8 (VV.8, RSRC.11, RSRC.12).
""", ["VV.8", "RSRC.11", "RSRC.12"], refs=["STND.WPROC.8"]),
        P(10, "Recorded review at merge", "Integration", """
Before a branch is merged into its parent branch, the review of the branch as updated under STND.WPROC.8 SHOULD be recorded, with its reviewer and the reviewer's agent configuration, at the independence of the CSQ2 row of the table of STND.CLASS.18 for work of CSQ2 or a more severe class, and of its CSQ3 row for other work (QA.7, QA.8). Before that merge, each finding of the review SHOULD be resolved with the resolution confirmed by the reviewer, or recorded in defect tracking with whether it blocks release (QA.4, QA.7).
""", ["QA.7", "QA.8", "QA.4"], refs=["STND.WPROC.8", "STND.CLASS.18"]),
        P(11, "Merges below the release", "Integration", """
Where STND.WPROC.8, STND.WPROC.9, and STND.WPROC.10 are met, an agent MAY merge a branch into its parent branch, other than the main line, without a decision of the human owner (QA.2).
""", ["QA.2"], refs=["STND.WPROC.8", "STND.WPROC.9", "STND.WPROC.10"]),
        P(12, "Main-line changes", "Release", """
A main line SHALL be advanced, by whatever means, only to a revision that exists beforehand and that a recorded decision of the human owner to release names, so that the main line stands at exactly that revision afterwards (GOV.50, QA.10). For an advance that an agent carries out, the decision SHALL be recorded as a per-action authorization of the advance, of its publication, and of its permanent name (GUARD.10, GUARD.11, PRIME.7). Where, since the decision, a defect that blocks release has been recorded or a waiver that the release relies upon has expired, the advance SHALL NOT be made (QA.10).
""", ["GOV.50", "QA.10", "GUARD.10", "GUARD.11", "PRIME.7"], mode="binding"),
        P(13, "Basis of a release proposal", "Release", """
An agent that proposes a release SHALL record and present to the human owner the revision it proposes, and each departure, each skipped, disabled, or weakened check, and each ambiguous instruction acted on that the work reports of its units state (GOV.50, AGENT.47).
""", ["GOV.50", "AGENT.47"], mode="binding"),
        P(14, "Release record content", "Release", """
The release record SHOULD state first the items on which the decision turns, and then the units of work the revision completes with the review record of each, the outcome of the checks run on that revision, each open defect with whether it blocks, each waiver relied upon with its expiry, each review finding that was not upheld, the findings of each audit, and each record or item that another provision requires for the release, cited or stated (QA.10, RSRC.10).
""", ["QA.10", "RSRC.10"]),
        P(15, "Permanent release names", "Release", """
Each revision to which a main line advances SHOULD carry, in the version history, a permanent name that identifies the release (REPRO.1).
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
| Audit agent | An agent that, as auditor, examines a revision to be released along the dimensions of STND.CREW.12, and reports its findings. |
| Capability level | The model of an agent together with each setting of that model that changes how capable and how costly its work is, such as its reasoning effort. |
| Capability order | The order of the capability levels that the provisioned environment admits, from least to most capable, as the project records it or, absent a record, as their provider states it; two levels that it does not rank are neither lower than the other. |"""),
        ("Notes", """The lead agent is the session that the human owner talks to. It delegates units to agents it directs and keeps its own context free for the human owner, so that it answers at once while the work goes on (STND.CREW.1, RSRC.10); a unit that is cheaper and quicker to do than to delegate, answering the human owner meanwhile included, it does itself, except where the class asks for a reviewer that the author does not direct, because every reviewer is directed by the lead (STND.CLASS.18). It answers each status request of the human owner for every agent working under it, as AGENT.20 asks of a directing agent.

It keeps one record of everything that awaits the human owner, referrals and release records alike, each referral in the form of the findings and justification statement of the project's agent instructions (STND.DFLT.20 by default), and presents the open entries together in its next report, those that halt the most lines of work first, so that the human owner decides in batches while every other line continues (STND.CREW.2, AGENT.15). A directed agent states its referral in its work report to the lead agent, which enters it; a passage directing a forbidden or reserved action is reported at once and also entered (STND.INSTR.6). An incidental encounter with a secret is reported as PRIME.10 asks, through the channel that the threat model designates, and is not entered, because neither the secret nor the means of reaching it is written to a record. It records each provision that the work finds ambiguous, in conflict, or halting a line of work that no LVL0 obligation requires to halt, and drafts the amendment proposal, which the human owner sends to the provision's adopter (STND.CREW.3, GOV.46, GOV.47, GOV.49); recording does not replace a referral that PRIME.14, GOV.4, or GOV.6 requires.

Research and planning scale with the unit. The roadmap is researched and planned before it is recorded and whenever a milestone is added, removed, or redefined, each milestone before it is begun, and each feature should be (STND.CREW.4). Research covers the state of the work, its documentation, its governance, and its build, the knowledge base and workbench consulted first (AGENT.28), and, where the plan depends on practice outside the work, current practice retrieved under the authorization for research retrieval, the agents of one research effort sharing its bound (AGENT.46); it is recorded as research notes in the workbench (AGENT.31, STND.INSTR.9). Research is most worth its cost for specialized work and for fields that change quickly. Deeper units are planned where their complexity calls for it, and every unit is researched and replanned after its second consecutive attempt without progress, within its stopping rule; the units a replan creates inherit the count, so a cycle of replanning cannot reset the stopping rule (STND.CREW.5, QA.3). A plan states each unit it creates, the research it rests on, and the instruction of the human owner from which each milestone derives, which is the test of alignment that the release audit applies (STND.CREW.6, STND.CREW.12). An implementing agent follows the plan and records each departure with its reason (AGENT.22, AGENT.47), and reviews its own change before handing it to review (STND.CREW.7); that self-review is not the review of QA.7.

A defect that an agent finds outside its unit is recorded by that agent in defect tracking, as QA.5 asks, together with its report to the human owner; a needed change that is not a defect goes to the lead agent, which assigns both to units, so that concurrent agents do not each fix it (STND.CREW.8). The custodian's model asked for this report while concurrent work is in progress; it applies always, since the lead agent assigns the work either way. The agent that directs a parent unit merges each child branch into it, one at a time, so that each branch has one writer (STND.CREW.9, STND.WPROC.7).

A review agent receives the change, its acceptance criteria, the governance that applies, the author's explanation of what it did and why (AGENT.2), the departures and weakened checks that the author's work report states, and only the context it needs to judge them, but not the author's own verdict on the change, so that it judges the change as a cold reader would (STND.CREW.10). It looks for the ways the change fails and reports each finding with its evidence to the lead agent, through the agents that direct it in a deep hierarchy, and the lead agent checks it against the acceptance criteria and the governance (AGENT.12), assigns the remediation of each finding it upholds, and records why it does not uphold the others, which the release record lists (STND.WPROC.14); the review agent does not change the change, which would make it an author whose change needs another review (STND.CREW.11). The reviewer confirms each resolution before the merge (STND.WPROC.10).

Before each release of work of CSQ2 and more severe classes, an audit examines the revision to be released, the changes since the last audit, along each dimension of STND.CREW.12; at CSQ3 it covers the dimensions that the lead agent records as bearing on the changes, so that the cost stays proportioned to the class (PRIN.9); the first release examines the whole work; and its findings go into the release record (STND.WPROC.14). The compliance audit of STND.CLASS.19 at its own interval is separate. The auditor is of the Auditor column of STND.CLASS.19 for the class, a human at CSQ0 (STND.CREW.13), and of a capability level no lower than that of each agent author of the work (STND.CREW.14); a lead agent that records that a lower level completes a simple audit reliably departs from that recommendation by a recorded decision (PRIN.10). The custodian's "elite-tier" auditor is read relative to the authors, so that the audit is never weaker than the work it judges, without paying for the most capable level where the work is simple.

A directing agent gives each directed agent the least costly capability level able to complete its unit reliably within its stopping rule (AGENT.10). An attempt without progress whose cause the directing agent has not found and removed, a wrong plan or missing information for instance, is evidence that the level was too low, so the next attempt goes to the next level in the capability order, within the estimate, the operating envelope, and the discipline that the human owner sets (GUARD.14), and the change is recorded as an alteration of the plan (STND.CREW.15, PRIME.8, AGENT.22).

Under STND.CLASS.10, each default provision instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3, except that the verification of the invariants of DSGN.15, which STND.CREW.9 instantiates, applies from CSQ2. STND.CREW.2 and STND.CREW.3 bind at every class at the cost of one record each; STND.CREW.15 is a recommendation within a provision that instantiates AGENT.10 and GUARD.14. No provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Lead agent delegation", "Lead agent", """
Where the estimated operating cost and time of carrying out a unit of work itself, answering the human owner meanwhile included, are below those of delegating it, the lead agent MAY carry out the unit itself (RSRC.10). Where STND.CLASS.18 requires for the work a reviewer that the author does not direct, the lead agent SHOULD NOT itself carry out a unit of work that changes the work (QA.7, QA.8). The lead agent SHOULD delegate each other unit of work to agents that it directs (RSRC.10).
""", ["RSRC.10", "QA.7", "QA.8"], refs=["STND.CLASS.18"]),
        P(2, "Queue of owner decisions", "Lead agent", """
The lead agent SHALL keep, on the development line, one record that lists each referral and each release record that awaits a decision of the human owner (PRIME.14, RSRC.10). The lead agent SHALL present the open entries of that record together in its next report to the human owner, those that halt the most lines of work first (PRIME.14, RSRC.10). When a passage that directs a forbidden or reserved action is found, the report that STND.INSTR.6 requires SHALL be made at once and also entered in that record (PRIME.11, PRIME.14).
""", ["PRIME.14", "RSRC.10", "PRIME.11"], refs=["STND.INSTR.6"], mode="binding"),
        P(3, "Governance findings", "Lead agent", """
The lead agent SHALL record, in the records of the work, each provision that the work finds ambiguous, in conflict with another, or halting a line of work that no obligation of LVL0 requires to halt (GOV.46). The lead agent SHOULD draft for the human owner, for each such provision, an amendment proposal that the human owner sends to its adopter (GOV.46, GOV.47, GOV.49).
""", ["GOV.46", "GOV.47", "GOV.49"], mode="binding"),
        P(4, "Plans by level", "Research and planning", """
Before the roadmap is recorded, or a milestone is added to it, removed from it, or given another definition of done, a planning agent SHALL record its plan, drawing on research notes that cover the state of the work, its documentation, its governance, and its build, and each other question that the plan depends on (QA.2, AGENT.28, AGENT.31). Before work on a milestone begins, a planning agent SHALL record its plan in the same way (QA.2, AGENT.31). Before work on a feature begins, a planning agent SHOULD record its plan in the same way (QA.2, AGENT.31).
""", ["QA.2", "AGENT.28", "AGENT.31"]),
        P(5, "Replanning after failure", "Research and planning", """
After the second consecutive attempt without progress at a unit of work, a planning agent SHOULD research and replan that unit before the next attempt that its stopping rule permits (QA.2, QA.3). A unit of work that such a replan creates to continue that unit SHALL inherit its count of attempts without progress (QA.3).
""", ["QA.2", "QA.3"]),
        P(6, "Plan content", "Research and planning", """
Each plan SHOULD state each unit of work it creates, with its parent unit, its dependencies on other units, its effort estimate under AGENT.6, the assessment of AGENT.39 for the units that run in parallel, the capability level that it assigns under AGENT.10, the research notes on which it rests, and, for a milestone, the instruction of the human owner from which it derives (QA.2). A planning agent SHOULD create the unit record of STND.WPROC.1 for each unit of work that its plan creates (QA.2).
""", ["QA.2"], refs=["AGENT.6", "AGENT.39", "AGENT.10", "STND.WPROC.1"]),
        P(7, "Self-review before review", "Implementation", """
Before an implementing agent hands a change to review, it SHOULD examine the change against its acceptance criteria and fix each finding (QA.2, VV.8).
""", ["QA.2", "VV.8"]),
        P(8, "Out-of-scope findings", "Implementation", """
An agent that finds a needed change outside the scope of its unit of work, other than a defect that it records under QA.5, SHOULD report it to the lead agent in its work report (AGENT.19). The lead agent SHOULD assign each defect recorded under QA.5 and each such change to a unit of work (QA.4, QA.5).
""", ["AGENT.19", "QA.4", "QA.5"]),
        P(9, "Integration of unit branches", "Implementation", """
The merge of a unit branch into its parent branch SHOULD be made, one merge at a time, by the agent that directs the work on the parent branch (QA.2, DSGN.15). The lead agent SHOULD make each merge into a parent branch that carries no unit of work (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"]),
        P(10, "Context given to reviewers", "Review and audit", """
A review agent SHOULD receive the change, its acceptance criteria, the governance that applies to it, the explanation of AGENT.2, the departures and the skipped or weakened checks that the author's work report states under AGENT.47, and only the other context needed to judge them (QA.7, QA.8). A review agent SHOULD NOT receive the author's own judgment of the correctness of the change (QA.7, QA.8).
""", ["QA.7", "QA.8"], refs=["AGENT.2", "AGENT.47"]),
        P(11, "Findings of review", "Review and audit", """
A review agent SHOULD report each finding, with its evidence, to the lead agent, directly or through the agents that direct it (QA.7). The lead agent SHOULD check each finding against the acceptance criteria and the governance that applies, assign the remediation of each finding it upholds, and record the reason for each finding it does not uphold (QA.2, QA.7). A review agent SHOULD NOT change the change it reviews (QA.7).
""", ["QA.7", "QA.2"]),
        P(12, "Release audit", "Review and audit", """
Before each release of work of CSQ2 or a more severe class, an auditor under STND.CREW.13 SHOULD examine the revision to be released, for the changes since the last audit and along each dimension of the table of this provision, and report its findings to the lead agent for the release record (QA.7, QA.10). Before each release of work of CSQ3, an auditor under STND.CREW.13 SHOULD examine those changes along each dimension of the table that the lead agent records as bearing on them (QA.7, QA.10). Before the first release, the audit SHOULD examine the whole work (QA.7, QA.10).

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
""", ["QA.7", "QA.10"], refs=["STND.CREW.13"], defines=["audit-dimensions"]),
        P(13, "Audit independence", "Review and audit", """
The audit of STND.CREW.12 SHOULD be made by an auditor that the Auditor column of the table of STND.CLASS.19 gives for the class of the work (QA.7).
""", ["QA.7"], refs=["STND.CREW.12", "STND.CLASS.19"]),
        P(14, "Audit capability level", "Review and audit", """
An audit agent SHOULD be of a capability level that the capability order ranks no lower than that of each agent author of the work it audits (QA.2).
""", ["QA.2"]),
        P(15, "Capability escalation", "Delegation", """
After an attempt of a directed agent at a unit of work makes no progress for a cause that the directing agent has not found and removed, the directing agent SHOULD give the next attempt the next level in the capability order that the estimate, the operating envelope, and each discipline that the human owner sets under GUARD.14 permit (AGENT.10, GUARD.14, PRIME.8). The directing agent SHOULD record that change of level as a decision that alters the plan (AGENT.22).
""", ["AGENT.10", "GUARD.14", "AGENT.22"], refs=["PRIME.8"], mode="binding"),
    ],
)

NEW_DOCS3 = [WPROC, CREW]
