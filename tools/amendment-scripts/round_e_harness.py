"""Round e of 2026-10-28, part 1: STND.HARN (ruling E1, R5.3), LVL0 1.7.1 (R6.1), and AGENT (R6.1, CC31).

STND.HARN.24 and STND.HARN.28 become outcomes that a reader checks with or without a harness, and STND.HARN.28 lists
for review only the pairs that rest on a shared matter and the pairs of common instantiation within the change
(HR-12, CP7); its Note on the reviewer cites STND.HARN.28 and STND.CLASS.18 (CP23); the Purpose names the
transactions that a harness enters (CP22). LVL0 and AGENT keep each rule once and cite it elsewhere, with no change
of meaning (CC23 to CC26, CC31, each checked).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
import round_e_base as E  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

# ---------------------------------------------------------------------------------------------------- STND.HARN

HARN_PURPOSE = [(
    "A harness serves governance read-only: it fetches what applies and checks conformance. No work depends on it "
    "(GOV.38).",
    "A harness serves governance: it fetches what applies, checks conformance, and enters the transactions that an "
    "actor directs. It holds no authority of its own, and no work depends on it (GOV.38). STND.HARN.24 and "
    "STND.HARN.28 state outcomes of a change of governance that a reader checks with or without a harness.")]

HARN24 = (
    "Before applying a script that changes a corpus, an actor SHALL confirm, on a copy of the corpus on which the "
    "script has run, that the copy has each property whose absence a check of a harness that meets this standard "
    "reports as FAIL, as the documentation of that harness states the property (GOV.36). A rehearsal of the script "
    "in which no check reports FAIL MAY serve as that confirmation (GOV.36).")

HARN28 = (
    "The record of the review of each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0 "
    "SHALL state, for each pair of provisions of different documents that a row of the table of this provision "
    "gives, at least one of them in a profile or sub-profile and at least one of them a provision that the change "
    "adopts or amends or that instantiates a LVL0 provision that the change amends, whether the two provisions "
    "conflict and whether they address one matter that no shared-matters table gives, with the profile that is to "
    "own it (GOV.26, QA.7). The summary of that record given to the adopter SHALL hold only the pairs found to "
    "conflict and the matters left without an owning profile, and cite the full record (GOV.26).\n\n"
    "| Basis | Pair given |\n"
    "| --- | --- |\n"
    "| Shared matter | The shared-matters tables of the documents in force and of each document that the change "
    "adopts or amends give both provisions for one shared matter. |\n"
    "| Common instantiation | Both provisions are in documents of which the change adopts or amends a provision, "
    "and both instantiate one LVL0 provision outside GOV and the Governing Principles. |")

HARN_NOTE_OLD = ("An agent of a different agent configuration from the author performs that review (QA.8), and the "
                 "adopter sees only its summary.")
HARN_NOTE_NEW = (
    "STND.HARN.28 states what the record of that review and the adopter's summary hold, and STND.CLASS.18 the "
    "independence of its reviewer (QA.8). The pairs of STND.HARN.28 hold a provision that the change adopts or "
    "amends, every provision of a document that it adopts among them: those that rest on a shared matter, which the "
    "shared-matters tables record as one subject of the two provisions, and those of common instantiation within "
    "the change, whose two provisions are both in documents of which the change adopts or amends a provision; a change "
    "that amends several documents and is reviewed as one, as a round of amendments is, pairs the provisions "
    "across them. A change of the Notes alone amends no provision and adds no pair, and a provision that the change "
    "reaches only because it instantiates an amended LVL0 provision pairs on a shared matter alone, so that a change "
    "of LVL0 alone lists the pairs on a shared matter of the provisions that instantiate what it amends. "
    "STND.HARN.24 reaches every check that a harness runs in a rehearsal, the checks of defaults, the logic checks, "
    "and the check of onsets among them, by the property that its documentation states for each. A LVL0 provision "
    "that two "
    "provisions both instantiate is a weak sign of one subject, since most provisions of a profile share one with "
    "most provisions of another, a provision that the change leaves as it was was paired when it was adopted or "
    "last amended, and QA.7 has the change reviewed against this document and the applicable lower governance in "
    "any case. The command `pairs` lists the pairs, and a reader lists them from the shared-matters tables and the "
    "field `instantiates`. STND.HARN.24 and STND.HARN.28 bind, because they instantiate GOV.36 and GOV.26, and "
    "raise no floor (GOV.11): each asks, of a change of governance, an outcome that a reader checks from a copy of "
    "the corpus, a review record, and the tables, and no decision of the human owner; STND.HARN.24 reaches what the "
    "rehearsal reached, and a rehearsal still meets it.")


def edit_harn(root: Path) -> None:
    replace_text(root, "STND/HARN/_doc.md", HARN_PURPOSE + [(HARN_NOTE_OLD, HARN_NOTE_NEW)])
    F.set_body(root, "STND/HARN/24.md", HARN24)
    F.set_body(root, "STND/HARN/28.md", HARN28, defines=["review-pairs"])
    F.check_fields(root, ["STND.HARN.24", "STND.HARN.28"], binding=True)


HARN = E.Step(
    "STND.HARN", edit_harn, True,
    "STND.HARN.24 has the actor that applies a script confirm, on a copy on which the script has run, each property "
    "whose absence a check of a harness that meets this standard reports as FAIL, as the documentation of that "
    "harness states it, with a rehearsal in which no check reports FAIL as one way to confirm it; STND.HARN.28 has "
    "the review record state a verdict for each pair that holds a provision that the change adopts or amends and "
    "that rests on a shared matter, or on a common LVL0 provision where both provisions are in documents of which "
    "the change amends a provision, in place of a harness listing every "
    "pair of the changed document that instantiates one LVL0 provision; the Notes cite "
    "STND.HARN.28 and STND.CLASS.18 for the review in place of a sentence in the indicative, and give the reasons "
    "and the floor argument; the Purpose names the transactions that a harness enters",
    "it alters two obligations, their means and the pairs listed, without altering the motivation or intent of the "
    "governance",
    "No floor is raised or lowered (GOV.11): STND.HARN.24 reaches every check that a rehearsal runs, as before, "
    "so a project with a harness does as before and one without it reads the properties from the documentation; "
    "STND.HARN.28 asks a verdict on "
    "fewer pairs, while GOV.26 and QA.7 still have the change judged against every applicable provision, and "
    "neither provision asks a decision of the human owner",
    "unchanged; both provisions bind",
    "a review recorded before this revision under the wider list of STND.HARN.28 stands",
    f"{E.ruling('E1', 'F1')}; register entries R5.1 (CP7, CP23, HR-12) and R5.3 (CP22)")

# ---------------------------------------------------------------------------------------------------- LVL0 1.7.1

GOV11 = [
    ("is proportioned to the consequence class of the work and the reliance placed on it, NEVER to the setting or "
     "hardware of the work (PRIN.9). The proportionality judgment, which states the consequence class and the "
     "reliance placed on the work, is recorded and adopted by the human owner. Exploratory",
     "is proportioned to the consequence class of the work and the reliance placed on it, both of which the "
     "proportionality judgment states (GOV.50), NEVER to the setting or hardware of the work (PRIN.9). Exploratory"),
    ('cites: ["PRIN.9"]', 'cites: ["GOV.50", "PRIN.9"]'),
]
GOV24 = [
    ("The classification is adopted by the human owner (GOV.50) and revised whenever the work changes in a way a "
     "selector tests.",
     "The classification (GOV.50) is revised whenever the work changes in a way a selector tests."),
]
GOV48 = [
    (" They SHALL NOT grant themselves waivers (GOV.44).", ""),
    ('cites: ["PRIME.15", "INTPR.11", "GOV.44"]', 'cites: ["PRIME.15", "INTPR.11"]'),
]
GUARD4 = [
    ("Every project has a register of reserved actions and of exempt classes (GOV.21), adopted by the human owner "
     "or, absent a project constitution, provided by the defaults (GOV.22).",
     "Every project has a register of reserved actions and of exempt classes (GOV.21, GOV.22)."),
]
GUARD15 = [
    ("Expenditure that would exceed an authorized estimate or operating envelope halts the work incurring it, and "
     "the agent refers it (PRIME.14).",
     "The agent refers each line of work that PRIME.8 halts (PRIME.14)."),
    ('cites: ["PRIME.14"]', 'cites: ["PRIME.8", "PRIME.14"]'),
]
PRIME_DOC = [
    ("Where two prime directives pull apart, the more restrictive reading governs, and an agent halts and refers "
     "(GOV.6, PRIME.14).",
     "Where two prime directives pull apart, GOV.6 and GOV.9 decide which governs and when an agent halts and "
     "refers."),
]

LVL0_READING = (
    "LVL0 keeps each rule once and cites it elsewhere: GOV.11 cites GOV.50 for the adoption of the proportionality "
    "judgment, which the Lexicon defines, in place of restating it; GOV.24 cites GOV.50 for the adoption of the "
    "classification; GOV.48 drops its sentence on waivers that agents grant themselves, which PRIME.1 holds; "
    "GUARD.4 drops the adoption and the "
    "defaults of the register, which GOV.50 and GOV.22 hold; GUARD.15 cites the halt of PRIME.8 in place of "
    "restating it; and the opening of PRIME cites GOV.6 and GOV.9 for prime directives that pull apart")
LVL0_ROW = f"| {{new}} | {F.DATE} | Editorial amendment (GOV.40): {LVL0_READING}; no obligation changes. |"
LVL0_RATIONALE = (
    f"Editorial amendment, revision {{new}}, ratified by the custodian on {F.DATE}: {LVL0_READING}. Each deleted "
    "text is held whole elsewhere at the same or a higher rank: the proportionality judgment is the human owner's "
    "recorded judgment of the class and the reliance (Lexicon), which only the human owner adopts (GOV.50), and "
    "every adoption enters the ledger (GOV.36); the classification is adopted only by the human owner (GOV.50); an "
    "agent never performs the grant of a waiver, for itself or another (PRIME.1, rank 0); the reserved-action "
    "register is adopted only by the human owner (GOV.50) and is provided by the defaults where no constitution "
    "exists (GOV.22); work halts "
    "before an authorized estimate or operating envelope is exceeded (PRIME.8, rank 0), and GUARD.15 keeps the "
    "referral; two prime directives share rank 0, so GOV.6 resolves their conflict and GOV.9 their readings, the "
    "more restrictive governing and the agent halting and referring in both. Alternatives weighed: CC23's change to "
    "PRIME.1, citing GOV.50 for the reserved acts (rejected: GOV.50 does not list the grant of authorizations and "
    "waivers, which PRIME.1 reserves at rank 0, so the change would alter a prime directive); CC24's change to "
    "PRIME.14, citing GOV.6 and GOV.9 for its triggers (rejected: its triggers are its own, and neither provision "
    "lists them). The logic check b.5 of the harness reads the bar on a waiver from PRIME.1 where GOV.48 no longer "
    "states it (unit 0024). Class: editorial, because no obligation, permission, or defined meaning changes. No "
    "floor is raised or lowered (GOV.11). Lower governance affected: none; a provision that instantiates GOV.11, "
    "GOV.24, "
    "GOV.48, GUARD.4, or GUARD.15 keeps its rank and its meaning. Transition (GOV.42): none. Proposal: "
    f"{E.ruling('F1')}, with register entry R6.1 (CC23, CC24, CC25, CC26); {E.RECORD}." + F.AUTHOR)


def apply_lvl0(root: Path, at: str) -> None:
    root = Path(root)
    replace_text(root, "GOV/11.md", GOV11)
    replace_text(root, "GOV/24.md", GOV24)
    replace_text(root, "GOV/48.md", GOV48)
    replace_text(root, "GUARD/4.md", GUARD4)
    replace_text(root, "GUARD/15.md", GUARD15)
    replace_text(root, "PRIME/_doc.md", PRIME_DOC)
    old = E.revision_of(root, "LVL0")
    new = E.next_revision(old, False)
    raise_revision(root, "LVL0", old, new, LVL0_ROW.format(new=new))
    rec = record_transaction(root, Change(
        kind="amend", actor="The Custodian", role="custodians", at=at, authority=["GOV.40"],
        targets=["LVL0", "GOV.11", "GOV.24", "GOV.48", "GUARD.4", "GUARD.15"], scope=E.LVL0_SCOPE,
        rationale=LVL0_RATIONALE.format(new=new)))
    print("seq", rec.entry["seq"], "LVL0", new)


# ---------------------------------------------------------------------------------------------------- AGENT

AGENT45 = [
    (" Where work needs an authentication credential that the provisioned environment does not let the agent use, "
     "the agent SHALL refer to the human owner its need for that credential (PRIME.14).", ""),
    ('instantiates: ["PRIME.10", "PRIME.14"]', 'instantiates: ["PRIME.10"]'),
]
AGENT46 = [
    (" Until the extension is recorded, an agent SHALL NOT retrieve for that effort beyond the bound (GUARD.8).", ""),
]
AGENT_DOC = [
    ("AGENT.45 applies only where the agent seeks to use a credential the environment does not let it use.",
     "An agent that needs a credential that the environment does not let it use needs a privilege beyond what was "
     "provisioned, so it halts that line of work and refers under PRIME.14, and AGENT.45 keeps each credential that "
     "it uses out of every location that outlasts the action; until an extension of a bound is recorded, retrieval "
     "for the effort beyond the bound is bulk retrieval, which GUARD.8 reserves."),
]


def edit_agent(root: Path) -> None:
    replace_text(root, "AGENT/45.md", AGENT45)
    replace_text(root, "AGENT/46.md", AGENT46)
    replace_text(root, "AGENT/_doc.md", AGENT_DOC)
    F.check_fields(root, ["AGENT.45", "AGENT.46"], binding=True)


AGENT = E.Step(
    "AGENT", edit_agent, False,
    "AGENT.45 drops its second sentence, the referral of a credential that the environment does not let the agent "
    "use, which PRIME.14 holds, and AGENT.46 drops its third, the bar on retrieval beyond a bound until its "
    "extension is recorded, which GUARD.8 holds; the Notes cite PRIME.14 and GUARD.8 for both",
    "each dropped sentence restates a provision of LVL0 that binds the same actor at a higher rank: PRIME.14 halts "
    "and refers where a privilege beyond what was provisioned appears necessary, and GUARD.8 reserves retrieval "
    "beyond the bounds of an authorization, so no obligation, permission, or defined meaning changes",
    "No floor is raised or lowered (GOV.11); both provisions stay binding at every class",
    "unchanged",
    "none",
    f"{E.ruling('F1')}; register entry R6.1 (CC31, checked)")
