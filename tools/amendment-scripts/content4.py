"""STND.CREW draft 0.5: revision at the custodian's direction of 2026-10-21."""
import copy, re
import content3 as C3
from content3 import P, NORMATIVE, TERMS_LEAD

DATE = C3.DATE
MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 9, 8: 10, 9: 11, 10: 15, 11: 16, 12: 17, 13: 18, 14: 19, 15: 20}


def renum(text):
    return re.sub(r"STND\.CREW\.(\d+)", lambda m: f"STND.CREW.{MAP[int(m.group(1))]}", text)


old = {p["n"]: copy.deepcopy(p) for p in C3.CREW["provisions"]}
for p in old.values():
    p["body"] = renum(p["body"])
    p["refers_to"] = [renum(x) for x in p["refers_to"]]
    p["n"] = MAP[p["n"]]

# 5: replanning with fresh-context examination
old5 = old[5]
old5["body"] = old5["body"] + " The planning agent MAY have the unit, its plan, its records, and its failed attempts examined by agents that have no context of the unit beyond those records (QA.2)."

# 20: escalation scoped to subunits, and limited by STND.CREW.21
e = old[15]
e["body"] = ("After an attempt of a directed agent at a unit of work makes no progress for a cause that the directing agent has not found and removed, "
             "the directing agent SHOULD give the next attempt the next level in the capability order that the estimate, the operating envelope, "
             "each discipline that the human owner sets under GUARD.14, and STND.CREW.21 permit (AGENT.10, GUARD.14). "
             "The directing agent SHOULD confine that escalation to the subunits of work whose attempts lacked the capability (GUARD.14). "
             "The directing agent SHOULD record the change of level as a decision that alters the plan (AGENT.22).")
e["refers_to"] = ["STND.CREW.21"]

new = [
    P(7, "Grounded effort estimates", "Research and planning", """
Each effort estimate SHALL state its basis in the records of operating cost and time of earlier units of work of comparable kind (AGENT.6, GUARD.14). Where the work keeps a cost model fitted to those records, the estimate SHALL state that basis through the cost model (AGENT.6, GUARD.14). Where the records hold no unit of comparable kind, the estimate SHALL state that it rests on no record (AGENT.6, GUARD.14).
""", ["AGENT.6", "GUARD.14"], mode="binding"),
    P(8, "Cost model upkeep", "Research and planning", """
The work SHOULD keep, as a workbench tool, a cost model fitted to the records of AGENT.24 and to the comparisons of AGENT.7, refitted at each milestone (RSRC.3, AGENT.36). Each estimate made with the cost model SHOULD state the revision of the model and the spread of its earlier predictions about the costs and times recorded (RSRC.3, AGENT.36).
""", ["RSRC.3", "AGENT.36"], refs=["AGENT.24", "AGENT.7"]),
    P(12, "Network access by role", "Delegation", """
A directing agent SHOULD extend an authorization for research retrieval only to research agents (GUARD.12, GUARD.13). Where no authorization extends network access to an agent by name or by role, an agent other than a research agent SHALL NOT reach the network (GUARD.12, GUARD.13).
""", ["GUARD.12", "GUARD.13"], mode="binding"),
    P(13, "Delegation beyond depth two", "Delegation", """
Before an agent directs agents that would stand at a delegation depth greater than 2, it SHALL confirm that the processors, memory, and accelerators that the units already running leave free, and the estimate and budget of its unit, admit them (RSRC.8, GUARD.14).
""", ["RSRC.8", "GUARD.14"], mode="binding"),
    P(14, "Coalescence of delegated work", "Delegation", """
A directing agent SHALL reconcile the results of the agents it directs with one another, with the work they change, and with the acceptance criteria of its unit before it reports them in its own work report (AGENT.12, GUARD.12).
""", ["AGENT.12", "GUARD.12"], mode="binding"),
    P(21, "Escalation needing a ruling", "Delegation", """
Where an escalation of capability level would take a unit of work beyond its authorized estimate, or to a level or a rise in estimated cost that the discipline of the human owner under GUARD.14 marks for the human owner's ruling, the directing agent SHALL refer the escalation to the human owner with its revised estimate (PRIME.8, GUARD.14). Until the human owner rules, the directing agent SHALL NOT make that escalation (PRIME.8, GUARD.15).
""", ["PRIME.8", "GUARD.14", "GUARD.15"], mode="binding"),
]

provisions = sorted(list(old.values()) + new, key=lambda p: p["n"])

CREW = dict(
    id="STND.CREW", title="Agent roles standard",
    instantiates=["GOV.19", "GOV.48"],
    sections=[
        ("Purpose and scope", """This standard fixes the roles that agents take in work under STND.WPROC: a lead agent that the human owner directs and that delegates the work, research and planning agents that prepare each milestone and feature and alone reach the network for research, implementing agents that carry out the plan, review agents that examine each change cold, and audit agents that examine the work before each release. It states what each role produces and to whom it reports; how effort estimates rest on the work's own records of cost and time; how delegation deepens without a limit on number or depth while each directing agent answers for the coherence of what its agents return; and how the lead agent keeps the human owner's burden to a few batched decisions, the escalations that the human owner's discipline marks as costly among them. One agent takes several roles in sequence, and the lead agent carries out a small unit itself, except that no agent reviews a change that it authored (QA.7), the independence of a reviewer from the author rises with the class (STND.CLASS.18), and that of an auditor follows STND.CLASS.19. STND.CREW.2, STND.CREW.3, STND.CREW.7, STND.CREW.12, STND.CREW.13, STND.CREW.14, STND.CREW.20, and STND.CREW.21 instantiate a prime directive, GUARD, or GOV and are binding at every class; every other provision is a default (GOV.19). The standard names no model, provider, or tool (GOV.18), and sets no limit on the number of agents or the depth of delegation (GOV.18, AGENT.9)."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Agent configuration has the meaning that STND.CLASS gives it; Attempt without progress has the meaning that STND.DFLT gives it; Directing agent, Directed agent, Effort estimate, Research effort, and Work report have the meanings that AGENT gives them; Development line, Milestone, Feature, Roadmap, Unit branch, Parent branch, and Release record have the meanings that STND.WPROC gives them, the last by STND.WPROC.13 and STND.WPROC.14.

| Term | Definition |
| --- | --- |
| Lead agent | The agent that takes its instructions for the work from the human owner directly and directs the other agents working on it. |
| Research agent | An agent that investigates a question that a plan depends on and records a research note. |
| Planning agent | An agent that records the plan of a unit of work. |
| Implementing agent | An agent that carries out a unit of work that changes the work. |
| Review agent | An agent that performs the review of a change. |
| Audit agent | An agent that, as auditor, examines a revision to be released along the dimensions of STND.CREW.17, and reports its findings. |
| Capability level | The model of an agent together with each setting of that model that changes how capable and how costly its work is, such as its reasoning effort. |
| Capability order | The order of the capability levels that the provisioned environment admits, from least to most capable, as the project records it or, absent a record, as their provider states it; two levels that it does not rank are neither lower than the other. |
| Delegation depth | The number of directing agents between an agent and the human owner; the lead agent stands at depth 0, and the agents it directs at depth 1. |
| Cost model | A tool that predicts the operating cost and time of a unit of work from the recorded costs and times of earlier units. |"""),
        ("Notes", """The lead agent is the session that the human owner talks to. It delegates units to agents it directs and keeps its own context free for the human owner, so that it answers at once while the work goes on (STND.CREW.1, RSRC.10); a unit that is cheaper and quicker to do than to delegate, answering the human owner meanwhile included, it does itself, except where the class asks for a reviewer that the author does not direct, because every reviewer is directed by the lead (STND.CLASS.18). It answers each status request of the human owner for every agent working under it, as AGENT.20 asks of a directing agent.

It keeps one record of everything that awaits the human owner, referrals, release records, and escalations that need a ruling alike, each referral in the form of the findings and justification statement of the project's agent instructions (STND.DFLT.20 by default), and presents the open entries together in its next report, those that halt the most lines of work first, so that the human owner decides in batches while every other line continues (STND.CREW.2, AGENT.15). A directed agent states its referral in its work report to the lead agent, which enters it; a passage directing a forbidden or reserved action is reported at once and also entered (STND.INSTR.6). An incidental encounter with a secret is reported as PRIME.10 asks, through the channel that the threat model designates, and is not entered, because neither the secret nor the means of reaching it is written to a record. It records each provision that the work finds ambiguous, in conflict, or halting a line of work that no LVL0 obligation requires to halt, and drafts the amendment proposal for the human owner to send to the provision's adopter (STND.CREW.3, GOV.46, GOV.47, GOV.49); recording does not replace a referral that PRIME.14, GOV.4, or GOV.6 requires. STND.CREW.2 and STND.CREW.3 fix only where and how the records that PRIME.14, GOV.46, and GOV.47 already ask for are kept, and the amendment draft of STND.CREW.3 is a recommendation, so binding them at every class raises no floor (GOV.11).

Research and planning scale with the unit. The roadmap is researched and planned before it is recorded and whenever a milestone is added, removed, or redefined, each milestone before it is begun, and each feature by recommendation (STND.CREW.4). Research covers the state of the work, its documentation, its governance, and its build, the knowledge base and workbench consulted first (AGENT.28), and, where the plan depends on practice outside the work, current practice retrieved under the authorization for research retrieval, the agents of one research effort sharing its bound (AGENT.46); it is recorded as research notes in the workbench (AGENT.31, STND.INSTR.9). Research is most worth its cost for specialized work and for fields that change quickly. Deeper units are planned where their complexity calls for it, and every unit is researched and replanned after its second consecutive attempt without progress, within its stopping rule; the units a replan creates inherit the count, so a cycle of replanning does not reset the stopping rule. A replan may draw on agents that come to the unit cold, with only its records, because an agent that has followed the failed attempts tends to repeat their framing, and a fresh reading finds what it missed (STND.CREW.5, QA.3). A plan states each unit it creates, the research it rests on, and the instruction of the human owner from which each milestone derives, which is the test of alignment that the release audit applies (STND.CREW.6, STND.CREW.17).

Effort estimates rest on the work's own records. AGENT.24 records the start, end, and operating cost of each unit, and AGENT.7 sets each estimate beside its outcome; an estimate states which of those records it rests on, through a cost model fitted to them where one is kept, or states plainly that it rests on none (STND.CREW.7). The custodian observed that estimates without such a basis are inaccurate. The cost model is a workbench tool, refitted at each milestone, and each estimate it gives states the model's revision and how far its earlier predictions fell from what was recorded, so that the human owner reads the estimate with its track record (STND.CREW.8). An estimate that rests on no record is the first point of a new record, not a reason to delay the unit.

An implementing agent follows the plan and records each departure with its reason (AGENT.22, AGENT.47), and reviews its own change before handing it to review (STND.CREW.9); that self-review is not the review of QA.7. A defect that an agent finds outside its unit is recorded by that agent in defect tracking, as QA.5 asks, together with its report to the human owner; a needed change that is not a defect goes to the lead agent, which assigns both to units, so that concurrent agents do not each fix it (STND.CREW.10). The custodian's model asked for this report while concurrent work is in progress; it applies always, since the lead agent assigns the work either way. The agent that directs a parent unit merges each child branch into it, one at a time, so that merges into each branch are made one at a time by one agent (STND.CREW.11, STND.WPROC.7).

Research agents are the agents that reach the network for research: a directing agent extends the authorization for research retrieval to them alone, and every other agent reaches the network only where an authorization extends to it by name or by role, as the standing authorization for installing dependencies or for adding commits to a remote repository does for the agents whose work needs them (STND.CREW.12, STND.PROJ.3). Content retrieved from the network is the main route of injected instructions (PRIME.11), and confining retrieval to research agents, whose output is a research note that others read as data, keeps that content away from the agents that change the work.

Delegation has no limit on the number of agents or the depth (AGENT.9, GOV.18). An agent that would deepen the hierarchy past depth 2 confirms first that the machine and the estimate and budget of its unit admit the agents it adds (STND.CREW.13, RSRC.8, AGENT.40); this is a check of capacity, not a limit, and a project instrument that sets a limit sets it at LVL3 (GOV.18). Each directing agent answers for what its agents return: it reconciles their results with one another, with the work they change, and with its acceptance criteria before it reports them as its own (STND.CREW.14, AGENT.12, GUARD.12), so that the quality, consistency, and coalescence of delegated work rest on the agent that delegated it, at every depth.

A review agent receives the change, its acceptance criteria, the governance that applies, the author's explanation of what it did and why (AGENT.2), the departures and weakened checks that the author's work report states, and only the context it needs to judge them, but not the author's own verdict on the change, so that it judges the change as a cold reader would (STND.CREW.15). It looks for the ways the change fails and reports each finding with its evidence to the lead agent, through the agents that direct it in a deep hierarchy, and the lead agent checks it against the acceptance criteria and the governance (AGENT.12), assigns the remediation of each finding it upholds, and records why it does not uphold the others, which the release record lists (STND.WPROC.14); the review agent does not change the change, which would make it an author whose change needs another review (STND.CREW.16). The reviewer confirms each resolution before the merge (STND.WPROC.10).

Before each release of work of CSQ2 and more severe classes, an audit examines the revision to be released, the changes since the last audit, along each dimension of STND.CREW.17; at CSQ3 it covers the dimensions that the lead agent records as bearing on the changes, so that the cost stays proportioned to the class (PRIN.9); the first release examines the whole work; and its findings go into the release record (STND.WPROC.14). The compliance audit of STND.CLASS.19 at its own interval is separate. The auditor is of the Auditor column of STND.CLASS.19 for the class, a human at CSQ0 (STND.CREW.18), and of a capability level no lower than that of each agent author of the work (STND.CREW.19); the capability needed to complete an audit reliably under AGENT.10 includes the capability to judge the work of its authors, and a lead agent that records that a lower level completes a simple audit reliably departs from STND.CREW.19 by a recorded decision (PRIN.10). The custodian's "elite-tier" auditor is read relative to the authors, so that the audit is never weaker than the work it judges, without paying for the most capable level where the work is simple.

A directing agent gives each directed agent the least costly capability level able to complete its unit reliably within its stopping rule (AGENT.10). An attempt without progress whose cause the directing agent has not found and removed, a wrong plan or missing information for instance, is evidence that the level was too low, so the next attempt goes to the next level in the capability order, confined to the subunits whose attempts lacked the capability rather than applied to the whole unit, and the change is recorded as an alteration of the plan (STND.CREW.20, AGENT.22). Most steps of the capability order cost little more than the last; a few, the most capable and costly model families above all, raise the cost of a unit many times over. The human owner marks those levels, or a rise in estimated cost, for ruling in the discipline of GUARD.14, and an escalation that reaches one, or that would exceed the authorized estimate, is referred with its revised estimate and waits for the ruling, while every other line of work continues and the unit itself continues at the levels that need no ruling, within its stopping rule (STND.CREW.21, PRIME.8, AGENT.15). Without such a mark, only the authorized estimate and the operating envelope bound an escalation, as PRIME.8 and GUARD.15 already ask.

Under STND.CLASS.10, each default provision other than STND.CREW.4, STND.CREW.8, and STND.CREW.10 instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3, except that the verification of the invariants of DSGN.15, which STND.CREW.11 instantiates, applies from CSQ2; STND.CREW.4, STND.CREW.8, and STND.CREW.10 also instantiate provisions of AGENT and add to them only the planning, the tool, and the report that they name; work of CSQ4 omits the defaults. STND.CREW.7, STND.CREW.12, STND.CREW.13, STND.CREW.14, and STND.CREW.21 instantiate GUARD or a prime directive; each fixes how an obligation that GUARD.12 to GUARD.15 or PRIME.8 already places is met, at the cost of a statement, a check, or a referral that LVL0 already asks, so binding them at every class raises no floor (GOV.11). STND.CREW.20 is a recommendation within a provision that instantiates AGENT.10 and GUARD.14."""),
    ],
    provisions=provisions,
)

NEW_DOCS4 = [CREW]
