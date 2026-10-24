"""Step 3, first round: STND.WPROC (work process) and STND.CREW (agent roles), draft 0.1."""

from content import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-20"

# ================================================================ STND.WPROC
WPROC = dict(
    id="STND.WPROC", title="Work process standard",
    instantiates=["GOV.19", "GOV.21"],
    sections=[
        ("Purpose and scope", """This standard is a work process (QA.2) that applies to work kept under version control, and that a project constitution adopts by citation or replaces with tighter rules. It carries each unit of work, from the roadmap down to the smallest fix, on its own branch, records the unit in the version history beside the change, integrates concurrent work up the branch hierarchy, and makes each merge into the main line a release that the human owner decides. STND.WPROC.2, STND.WPROC.9, and STND.WPROC.10 instantiate a floor obligation or GOV.50 and are binding at every class; every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). Below the release, no provision asks the human owner for a decision (STND.DRAFT.42). The standard uses the concepts of branch and merge that version-control systems share and names no system or tool (GOV.18). The roles that agents take in this process are in the agent roles standard."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Unit of work, Release, and Review have the meanings the Lexicon gives them; Agent configuration has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Branch | A line of the version history of the work that changes apart from the others until it is merged. |
| Merge | The combination of the changes of one branch into another, recorded in the version history without rewriting it. |
| Main line | The branch from which the work is released or deployed. |
| Development line | The branch, made from the main line, into which completed units of work are integrated before a release. |
| Unit branch | The branch on which one unit of work is carried out. |
| Parent branch | The branch from which a unit branch was made. |
| Roadmap | The recorded, ordered set of milestones of the work, each with its definition of done. |
| Milestone | A unit of work that the roadmap names, whose completion a release delivers. |
| Feature | A unit of work within a milestone or within another feature. |
| Release record | The record on which the human owner decides a merge into the main line, with the content that STND.WPROC.10 gives. |"""),
        ("Notes", """The work breakdown and the branch hierarchy are one structure. The roadmap names milestones; a milestone divides into features, and a feature into features of its own, to whatever depth the work needs; each unit that changes the work has a branch made from its parent unit's branch, or from the development line where the parent has none, and is merged back only into that branch (STND.WPROC.4, STND.WPROC.6). Concurrent units therefore meet only at their common parent: siblings never merge into each other, and each picks up its siblings' merged work by merging its parent into itself (STND.WPROC.7). The history need not be linear. Rewriting or force-overwriting history is reserved to the human owner (GUARD.5, PRIME.6), so agents combine work by merges, not by rewriting branches, even branches that no other actor has fetched.

The version history carries the work's tasks. Each unit's record, its definition of done, acceptance criteria, plan, and status, is kept in the version-controlled records under an identifier that the unit's branch and commits carry (STND.WPROC.1, STND.WPROC.2), so that the state of every task is read from the repository itself, without a separate tracker, and survives the loss of every tool (INTPR.12). A project that uses a tracker as well records its identifiers in the unit record.

A fix branches from the most upstream line that its defect affects, so a defect in a released revision is fixed from the main line, released, and merged into the development line, and a defect found only in a feature is fixed on that feature's branch (STND.WPROC.5).

Before a branch is merged into its parent, the parent is merged into it, the checks the change is able to affect pass on the result, and its review is recorded with the independence that STND.CLASS.18 gives for the class (STND.WPROC.7). An agent then merges it into its parent, and into the development line, without a decision of the human owner (STND.WPROC.8); the independence of review rises with the class, CSQ2 asking an actor not directed by the author and, for an agent author, a human or an agent of another configuration. Pushing such a merge to a remote repository is a remote write that the standing authorization recommended by STND.PROJ.3 for commits to branches other than release branches covers.

A merge into the main line releases the revision it merges, because the main line is the branch from which the work is used beyond its development. The human owner decides it at every class (GOV.50, QA.10, STND.WPROC.9), on a release record that the proposing agent prepares, which states what the decision rests on, so that the human owner's review is of one record (STND.WPROC.10). The decision names the revision, and the merge is made of that revision only, by the human owner or by an agent that the decision authorizes (STND.WPROC.9). Each release carries a permanent name in the history (STND.WPROC.11); deleting or moving such a name is reserved (GUARD.5).

Under STND.CLASS.10, each default provision instantiates only QA, VV, REPRO, or RSRC and applies from CSQ3; STND.WPROC.9 and STND.WPROC.10 apply at every class, because the release decision is the human owner's at every class (GOV.50), and STND.WPROC.2 at every class, because version control is the floor (REPRO.5). STND.WPROC.10 tightens QA.10 at CSQ3 and CSQ4 by asking for a release record, at the cost of one record per release, so that no release rests on an unstated basis (PRIME.15). No other provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Unit records in history", "Records", """
Each unit of work SHOULD have its record, its definition of done, acceptance criteria, plan, and status, in the version-controlled records of the work, under an identifier that its branch and its commits carry (QA.2).
""", ["QA.2"]),
        P(2, "Attribution of commits", "Records", """
Each commit SHALL name the unit of work it serves and its author and, for an agent author, the agent's configuration (REPRO.5, REPRO.11).
""", ["REPRO.5", "REPRO.11"], mode="binding"),
        P(3, "Main and development lines", "Branches", """
The work SHOULD keep a main line and a development line made from it (QA.2).
""", ["QA.2"]),
        P(4, "Unit branches", "Branches", """
Each unit of work that changes the work SHOULD be carried out on a unit branch made from the branch of its parent unit (QA.2, DSGN.15). A unit of work whose parent unit has no branch SHOULD have its unit branch made from the development line (QA.2).
""", ["QA.2", "DSGN.15"]),
        P(5, "Fix branches", "Branches", """
A fix of a defect SHOULD be carried out on a branch made from the most upstream branch that the defect affects, and merged into that branch and into each branch descended from it that carries the defect (QA.4, VV.8).
""", ["QA.4", "VV.8"]),
        P(6, "Hierarchical integration", "Integration", """
A unit branch SHOULD be merged only into its parent branch (QA.2, DSGN.15).
""", ["QA.2", "DSGN.15"]),
        P(7, "Merge preconditions", "Integration", """
Before a branch is merged into its parent branch, the current state of the parent branch SHOULD be merged into it (QA.2). Before that merge, the checks that the change is able to affect SHOULD pass on the branch so updated (VV.8, RSRC.11). Before that merge, the review of the change SHOULD be recorded with the independence that STND.CLASS.18 gives for the class of the work (QA.7, QA.8).
""", ["QA.2", "VV.8", "RSRC.11", "QA.7", "QA.8"], refs=["STND.CLASS.18"]),
        P(8, "Merges below the release", "Integration", """
Where STND.WPROC.7 is met, an agent MAY merge a branch into its parent branch, the development line included, without a decision of the human owner (QA.2).
""", ["QA.2"], refs=["STND.WPROC.7"]),
        P(9, "Main-line merges", "Release", """
A merge into the main line SHALL be made only on a decision of the human owner to release the revision it merges, which names that revision (GOV.50, QA.10). The merge SHALL be of the revision that the decision names, made by the human owner or by an agent that the decision authorizes (GOV.50, PRIME.7).
""", ["GOV.50", "QA.10", "PRIME.7"], mode="binding"),
        P(10, "Release record", "Release", """
An agent that proposes a merge into the main line SHALL present to the human owner a release record that states the revision, the units of work it completes, the outcome of each check and review of those units, the findings of each audit, each open defect, and each departure that their work reports state (QA.10, AGENT.47).
""", ["QA.10", "AGENT.47"], mode="binding"),
        P(11, "Permanent release names", "Release", """
Each revision merged into the main line SHOULD carry, in the version history, a permanent name that identifies the release (REPRO.1).
""", ["REPRO.1"]),
    ],
)

# ================================================================ STND.CREW
CREW = dict(
    id="STND.CREW", title="Agent roles standard",
    instantiates=["GOV.19", "GOV.48"],
    sections=[
        ("Purpose and scope", """This standard fixes the roles that agents take in work under STND.WPROC: a lead agent that the human owner directs and that delegates the work, research and planning agents that prepare each milestone and feature, implementing agents that carry out the plan, review agents that examine each change cold, and audit agents that examine the work as a whole. It states what each role produces and to whom it reports, and how the lead agent keeps the human owner's burden to a few batched decisions. One agent takes several roles in sequence, and the lead agent carries out a small unit itself, except that no agent reviews or audits a change that it authored (QA.7), and the independence of a reviewer from the author rises with the class (STND.CLASS.18). STND.CREW.2, STND.CREW.3, and STND.CREW.12 instantiate a prime directive, GUARD, or GOV and are binding at every class; every other provision is a default (GOV.19). The standard names no model, provider, or tool (GOV.18), and sets no limit on the number of agents or the depth of delegation (GOV.18, AGENT.9)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Agent configuration has the meaning that STND.CLASS gives it; Main line, Milestone, Feature, Roadmap, and Release record have the meanings that STND.WPROC gives them.

| Term | Definition |
| --- | --- |
| Lead agent | The agent that takes its instructions for the work from the human owner directly and directs the other agents working on it. |
| Research agent | An agent that investigates a question that a plan depends on and records a research note. |
| Planning agent | An agent that records the plan of a unit of work. |
| Implementing agent | An agent that carries out a unit of work that changes the work. |
| Review agent | An agent that performs the review of a change. |
| Audit agent | An agent that examines the work, or the changes of more than one unit of work, along the dimensions of STND.CREW.10, and reports its findings. |
| Capability level | The model of an agent together with each setting of that model that changes how capable and how costly its work is, such as its reasoning effort. |"""),
        ("Notes", """The lead agent is the session that the human owner talks to. It delegates units to agents it directs and keeps its own context for the human owner, so that it answers at once and the work goes on while it does (STND.CREW.1); a unit that is cheaper and quicker to do than to delegate, it does itself. It answers each status request of the human owner for every agent working under it, as AGENT.20 already asks of a directing agent. It keeps one record of the referrals that await the human owner, each in the form of the findings and justification statement of the project's agent instructions (STND.DFLT.20 by default), and presents them together, most consequential first, so that the human owner decides in batches and every other line of work continues meanwhile (STND.CREW.2, AGENT.15). It records each provision that the work finds ambiguous, in conflict, or blocking without need, and proposes the amendment to the provision's adopter (STND.CREW.3, GOV.46, GOV.49); the adopter decides.

Research and planning scale with the unit. The roadmap and each milestone are researched and planned before work on them begins; each feature should be; a smaller unit is researched and replanned when its second attempt fails without progress, before its stopping rule halts it (STND.CREW.4). Research covers the state of the work, its documentation, its governance, and its build, and, where the plan depends on practice outside the work, current practice, retrieved under the authorization for research retrieval; it is recorded as research notes in the workbench (AGENT.31, STND.INSTR.9). Research is most worth its cost for specialized work and for fields that change quickly. A plan states the units it creates with their definitions of done, acceptance criteria, parents, and dependencies, and the capability level it assigns each (STND.CREW.5); an implementing agent follows it and records each departure with its reason (AGENT.22, AGENT.47).

An implementing agent reviews its own change against the acceptance criteria and fixes what it finds before handing it to review (STND.CREW.6); that self-review is not the review of QA.7. A finding outside its unit goes to the lead agent, which records and assigns it, so that concurrent agents do not each fix it (STND.CREW.7, QA.5).

A review agent receives the change, its acceptance criteria, the governance that applies, and only the context it needs to judge them, and not the author's reasoning, so that it judges the change as a reader would (STND.CREW.8). It looks for the ways the change fails and reports each finding with its evidence to the lead agent, which assigns the remediation; it does not fix the change itself, which would make it an author whose fix needs another review (STND.CREW.9). Its independence of the author rises with the class (STND.CLASS.18).

An audit agent examines the work along the dimensions of STND.CREW.10, before each release the changes since the last audit, and the whole work where the lead agent extends the audit. Because an audit is the last check before a release, its agent is of a capability level at least that of the most capable author of the work it audits (STND.CREW.11), which AGENT.10 allows, since a less capable agent is unable to complete the audit reliably.

A directing agent gives each directed agent the least costly capability level able to complete its unit reliably within its stopping rule (AGENT.10). When an attempt makes no progress, that is evidence that the level was too low, so the next attempt goes to the next more capable level rather than repeating the failed one (STND.CREW.12).

Under STND.CLASS.10, each default provision instantiates only QA, INTPR, or RSRC and applies from CSQ3. STND.CREW.2 and STND.CREW.3 bind at every class at the cost of one record; STND.CREW.12 is a recommendation within a provision that GUARD.14 makes binding. No provision raises the floor (GOV.11)."""),
    ],
    provisions=[
        P(1, "Lead agent delegation", "Lead agent", """
Where the estimated operating cost and time of carrying out a unit of work itself are below those of delegating it, the lead agent MAY carry out the unit itself (INTPR.6, RSRC.10). The lead agent SHOULD delegate each other unit of work to agents that it directs (INTPR.6, RSRC.10).
""", ["INTPR.6", "RSRC.10"]),
        P(2, "Referral record", "Lead agent", """
The lead agent SHALL keep, in one record, each referral of the work that awaits a decision of the human owner, in the form of the findings and justification statement (PRIME.14, RSRC.10). The lead agent SHALL present the open referrals of that record together, in order of their consequence, in its reports to the human owner (PRIME.14, RSRC.10).
""", ["PRIME.14", "RSRC.10"], mode="binding"),
        P(3, "Governance findings", "Lead agent", """
The lead agent SHALL record each provision that the work finds ambiguous, in conflict with another, or blocking without need (GOV.46). The lead agent SHOULD propose to the adopter of each such provision an amendment that resolves the finding (GOV.46, GOV.49).
""", ["GOV.46", "GOV.49"], mode="binding"),
        P(4, "Research and planning depth", "Research and planning", """
Before work on the roadmap or on a milestone begins, a planning agent SHALL record its plan, drawing on the research notes of research agents on each question that the plan depends on (QA.2, AGENT.31). Before work on a feature begins, a planning agent SHOULD record its plan in the same way (QA.2, AGENT.31). After the second consecutive attempt at a unit of work without progress, a planning agent SHOULD research and replan that unit before the next attempt (QA.2, QA.3).
""", ["QA.2", "QA.3", "AGENT.31"], refs=[]),
        P(5, "Plan content", "Research and planning", """
Each plan SHOULD state the units of work it creates, each with its definition of done, acceptance criteria, parent unit, dependencies on other units, and the capability level that it assigns under AGENT.10 (QA.2).
""", ["QA.2"], refs=["AGENT.10"]),
        P(6, "Self-review before review", "Implementation", """
Before an implementing agent hands a change to review, it SHOULD examine the change against its acceptance criteria and fix each finding (QA.2, VV.8).
""", ["QA.2", "VV.8"]),
        P(7, "Out-of-scope findings", "Implementation", """
An agent that finds a defect or a needed change outside the scope of its unit of work SHOULD report it to the lead agent in its work report (QA.5, AGENT.19). The lead agent SHOULD record each such report in defect tracking or the working-notes workspace and assign it (QA.4, QA.5).
""", ["QA.5", "AGENT.19", "QA.4"]),
        P(8, "Context given to reviewers", "Review and audit", """
A review agent SHOULD receive the change, its acceptance criteria, the governance that applies to it, and only the context needed to judge them, without the author's reasoning (QA.7, QA.8).
""", ["QA.7", "QA.8"]),
        P(9, "Findings of review", "Review and audit", """
A review agent SHOULD report each finding, with its evidence, to the lead agent (QA.7). The lead agent SHOULD assign the remediation of each finding to an implementing agent (QA.6). A review agent SHOULD NOT change the change it reviews (QA.7).
""", ["QA.7", "QA.6"]),
        P(10, "Release audit", "Review and audit", """
Before each merge into the main line, an audit agent SHOULD examine the changes since the last audit along each dimension of the table of this provision and report its findings to the lead agent (QA.7, QA.10).

| Dimension |
| --- |
| Conformance to the governance that applies |
| Alignment with the roadmap and the recorded plans |
| Correctness, mathematical soundness included |
| Coverage of the acceptance criteria by tests |
| Performance against the stated budgets |
| Safety |
| Security |
| Reproducibility of results |
| Consistency of documentation with the work |
""", ["QA.7", "QA.10"], defines=["audit-dimensions"]),
        P(11, "Audit capability level", "Review and audit", """
An audit agent SHOULD be of a capability level at least that of the most capable author of the work it audits (QA.8).
""", ["QA.8"]),
        P(12, "Capability escalation", "Delegation", """
After an attempt of a directed agent at a unit of work makes no progress, its directing agent SHOULD give the next attempt the next more capable level available to the work (AGENT.10, GUARD.14).
""", ["AGENT.10", "GUARD.14"], mode="binding"),
    ],
)

NEW_DOCS3 = [WPROC, CREW]
