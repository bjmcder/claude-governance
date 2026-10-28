"""Round c of 2026-10-28, part 1: LVL0 (GOV.13, QA.11, two Lexicon terms), STND.CLASS, and STND.PROJ.

Rulings C1 to C6 of review-records/deep-review-2026-10-28/rulings.md, on the readings of its section "Rulings of the
custodian, 2026-10-28", with register entries R3.1 to R3.4, R2.3, R2.4, and the STND.CLASS parts of R2.5 and R3.3.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

RULINGS = F.RECORD
RECORD = "review-records/rounds-2026-10-28/round-c/decisions.md"
LVL0_SCOPE = ["LVL0", "PRIN", "PRIME", "GUARD", "VV", "REPRO", "INTPR", "DSGN", "SIMPL", "RSRC", "QA", "GOV", "LEX"]


def ids(xs: list[str]) -> str:
    return "[" + ", ".join(f'"{x}"' for x in xs) + "]"


def provision(doc_id: str, n: int, title: str, section: str, mode: str, instantiates: list[str],
              refers_to: list[str], body: str, defines: list[str] | None = None) -> str:
    """Return the file text of a LVL2 provision; rank and waivable are derived afterwards."""
    return "\n".join([
        "---", f'id: "{doc_id}.{n}"', 'level: "LVL2"', 'kind: "provision"', f'title: "{title}"',
        f'section: "{section}"', 'status: "adopted"', f'adopted: "{F.DATE}"', f'mode: "{mode}"',
        "binding_reason: null", f"instantiates: {ids(instantiates)}", f"refers_to: {ids(refers_to)}",
        "rank: null", "waivable: false", f"defines: {ids(defines or [])}", 'checked_by: ["review"]', "---", "",
        body, "",
    ])


def term(name: str, slug: str, group: str, governed_by: list[str], body: str) -> str:
    """Return the file text of a Lexicon term."""
    return "\n".join([
        "---", f'id: "LEX.{slug}"', 'level: "LVL0"', 'kind: "term"', f'term: "{name}"', f'group: "{group}"',
        'status: "ratified"', f'adopted: "{F.DATE}"', f"governed_by: {ids(governed_by)}", "---", "", body, "",
    ])


# ----------------------------------------------------------------------------------------------------------------
# LVL0 1.7: GOV.13, QA.11, and the terms Expected class and Reclassification
# ----------------------------------------------------------------------------------------------------------------

GOV13 = [
    ("The human owner sets the project's consequence class at inception, as the most severe class of its intended "
     "uses, and MAY revise it throughout the project's life. The human owner MAY record a less severe class for a "
     "component shown to be isolated from the more severe outputs. No class is assumed by default: where none is "
     "recorded, an agent that needs it halts that line of work and refers (PRIME.14).",
     "The human owner sets the project's consequence class at inception, as the most severe class of the uses then "
     "made of its outputs, and MAY revise it throughout the project's life. Where a more severe use is planned, the "
     "classification records the class of that use as the expected class, adopted with the classification (GOV.24) "
     "and setting no class before that use begins (GOV.14). The human owner MAY record a less severe class for a "
     "component shown to be isolated from the more severe outputs. No class is assumed by default: where none is "
     "recorded, the work meets the floor (GOV.10), and an agent that needs the class to promote, release, deploy, or "
     "drive physical hardware halts that line of work and refers (PRIME.14)."),
    ('cites: ["PRIME.14"]', 'cites: ["GOV.24", "GOV.14", "GOV.10", "PRIME.14"]'),
]

QA11 = [
    ("and that the gap is recorded. An agent MAY propose a promotion.",
     "and that the gap is recorded. For work of CSQ3 or CSQ4, the adopted classification is the promotion of each "
     "result that meets its acceptance criteria (QA.1), for reliance by its author or immediate team alone, feeding "
     "work that is verified later (GOV.12). An agent MAY propose a promotion."),
    ('cites: ["PRIME.3", "VV.3", "GOV.11"]', 'cites: ["PRIME.3", "VV.3", "GOV.11", "QA.1", "GOV.12"]'),
]

GOV_GROUP = "Governance (PRIME.1, PRIME.15, GOV)"
EXPECTED_CLASS = term(
    "Expected class", "expected-class", GOV_GROUP, ["GOV.13", "GOV.14"],
    "The consequence class, more severe than the class of the work, of a use of the work that the classification "
    "records as planned; it sets no class before that use begins.")
RECLASSIFICATION = term(
    "Reclassification", "reclassification", GOV_GROUP, ["GOV.14", "GOV.24"],
    "A revision of the classification that moves the consequence class of the work, or of a component, to another "
    "class.")

LVL0_READING = (
    "GOV.13 sets the class at inception as the most severe class of the uses then made of the project's outputs, "
    "records a planned more severe use as the expected class, adopted with the classification and setting no class "
    "before the use begins, and has unclassified work meet the floor until an agent needs the class to promote, "
    "release, deploy, or drive physical hardware; QA.11 makes the adopted classification the promotion, for work of "
    "CSQ3 or CSQ4, of each result that meets its acceptance criteria, for reliance by its author or immediate team "
    "alone, feeding work that is verified later; the Lexicon defines Expected class and Reclassification")
LVL0_ROW = f"| 1.7 | {F.DATE} | Minor amendment (GOV.40): {LVL0_READING}. |"
LVL0_RATIONALE = (
    f"Minor amendment, revision 1.7, ratified by the custodian on {F.DATE}: {LVL0_READING}. Alternatives weighed: a "
    "ruling under GOV.3 that reads GOV.13 this way without a text change (rejected: under GOV.9 the more restrictive "
    "reading of the text would keep governing every reader who has not seen the ruling); leaving a planned use to "
    "set the class at inception (rejected: it defeats the custodian's pattern of starting at CSQ3 or CSQ4 and "
    "promoting later); a separate act of the human owner for the expected class (rejected: one act, the adoption of "
    "the classification, suffices under GOV.50); per-result promotion within the unit of work (rejected: an act of "
    "the human owner for each result in the ordinary flow of CSQ3 work). Class: minor, because obligations and "
    "defined meanings change while no prime directive or principle changes in motivation or intent. No floor is "
    "lowered: GOV.14 still has every obligation of a class met before the work is relied upon at that class; "
    "unclassified work meets the floor (GOV.10) and nothing relies on an unpromoted result beyond its author "
    "(QA.11); the standing promotion reaches only reliance within the CSQ3 test of GOV.12, by a result that meets "
    "the acceptance criteria that QA.1 records before the work at every class, and reliance beyond that test still "
    "needs its own promotion. Lower governance affected: STND.CLASS, STND.PROJ, STND.CODE, HW, STND.CONC, AGENT, "
    "STND.CREW, STND.THRT, STND.WPROC, and the language standards, each amended in the same round; the STND.DFLT "
    "Notes list the classification among the acts entered under STND.DFLT.17, and the expected class travels with "
    f"it. Proposal: {RULINGS}, items C1 and C5, with register entries R3.1 and R2.3; {RECORD}." + F.AUTHOR)


def apply_lvl0(root: Path, at: str) -> None:
    replace_text(root, "GOV/13.md", GOV13)
    replace_text(root, "QA/11.md", QA11)
    (root / "LEX/expected-class.md").write_text(EXPECTED_CLASS, encoding="utf-8")
    (root / "LEX/reclassification.md").write_text(RECLASSIFICATION, encoding="utf-8")
    raise_revision(root, "LVL0", "1.6", "1.7", LVL0_ROW)
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.40"], targets=["LVL0", "GOV.13", "QA.11"],
                                          scope=LVL0_SCOPE, rationale=LVL0_RATIONALE))
    print("seq", rec.entry["seq"], "LVL0 1.7")


# ----------------------------------------------------------------------------------------------------------------
# STND.CLASS 1.4
# ----------------------------------------------------------------------------------------------------------------

CLASS1 = [
    ("or a cost above the amount of STND.CLASS.3. |",
     "or a cost above the amount that STND.CLASS.3 has the classification state. |"),
    ("| CSQ3 | A credible consequence of an error is effort or money lost beyond the author's own time, or a wrong "
     "output that the verification of the work it feeds detects before reliance. | Only the author, or actors of "
     "the same unit of work, rely on the output, and only through work that is verified before it is relied "
     "upon. |",
     "| CSQ3 | A credible consequence of an error is effort or money lost beyond the author's own time, or a wrong "
     "output that the verification of the work it feeds detects before reliance. | Only the author, or the actors "
     "of the author's immediate team, rely on the output, and only through work that is verified before it is "
     "relied upon. |"),
]

CLASS3 = [
    ("The classification SHALL state the amount of money above which a loss counts as a cost for the consequence "
     "test of CSQ1 in the table of STND.CLASS.1 (GOV.24).",
     "Where the class of the project or of a component is CSQ2 or a more severe class, the classification SHALL "
     "state the amount of money above which a loss counts as a cost for the consequence test of CSQ1 in the table "
     "of STND.CLASS.1 (GOV.24)."),
]

CLASS5 = [
    ("and the row of the table of STND.CLASS.1 whose test each meets (GOV.24).",
     "and the row of the table of STND.CLASS.1 whose test each meets (GOV.24). Where a more severe use of the "
     "project or of a component is planned, the classification SHALL state its expected class and the use that "
     "would occasion it (GOV.13, GOV.24)."),
    ('instantiates: ["GOV.24"]', 'instantiates: ["GOV.24", "GOV.13"]'),
]

CLASS7 = [
    ("or an incident shows a credible consequence that the classification omits, the human owner SHALL reassess "
     "the class (GOV.14).",
     "or an incident shows a credible consequence that the classification omits, the human owner SHALL reassess "
     "the class before a result of the work is next promoted, or the work is next released or relied upon at a "
     "more severe class (GOV.14)."),
]

CLASS10 = [
    ("Work of CSQ4 MAY omit every obligation of these Articles above the floor (GOV.11).",
     "Work of CSQ4 MAY omit every obligation of these Articles above the floor, other than STND.CLASS.21 and the "
     "records of STND.CLASS.23 (GOV.11)."),
    ('refers_to: ["GOV.11", "GOV.48"]', 'refers_to: ["GOV.11", "GOV.48", "STND.CLASS.21", "STND.CLASS.23"]'),
]

CLASS18 = [
    ("| CSQ2 | An actor not directed by the author performs the review; where the author is an agent, that actor is "
     "a human or an agent of a different agent configuration. |",
     "| CSQ2 | An actor not directed by the author performs the review; where the author is an agent, that actor is "
     "a human or an agent whose agent configuration differs from the author's in its model or in its instruction "
     "revision, whatever its tools. |"),
    ("| CSQ3 | An actor other than the author; an agent is eligible (QA.7). |",
     "| CSQ3 | An actor other than the author: a human, or an agent, of the author's agent configuration or "
     "another, in a session, other than each session of the author, whose context holds nothing of the author's "
     "sessions except what it reads from the records of the work (QA.7). |"),
]

CLASS19 = [
    ("Before work is relied upon at a more severe class, the project SHALL be audited by the auditor of that class "
     "(GOV.47).",
     "Before work moved to CSQ2 or a more severe class is first relied upon at that class, the project SHALL be "
     "audited by the auditor of that class (GOV.47)."),
]

CLASS21 = provision(
    "STND.CLASS", 21, "Expected class in design", "Assignment", "default",
    ["DSGN.13", "DSGN.4", "DSGN.5", "REPRO.4", "REPRO.7"], ["STND.CLASS.10", "STND.CLASS.23", "GOV.11"],
    "Where the classification records an expected class, the design of the work SHOULD admit, without rework of the "
    "design, the parts of the table of STND.CLASS.10 that apply from that class, and the contracts, schemas, "
    "provenance, language edition and subset, failure channel, dependencies, hardware, reduction order, and kept "
    "reference path that the obligations of that class ask of the work, with the reason for each choice that the "
    "expected class drives recorded in a decision record (DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7). Before the "
    "reclassification, the work MAY omit "
    "each record that only an obligation of the expected class requires, other than the records of STND.CLASS.23 "
    "(GOV.11).")

CLASS22 = provision(
    "STND.CLASS", 22, "Reclassification obligations", "Assignment", "binding",
    ["GOV.14", "REPRO.1", "QA.12", "QA.7", "GOV.47", "GOV.42"], ["STND.CLASS.18", "STND.CLASS.19"],
    "Before work is relied upon at a more severe class, the work done at the less severe class SHALL meet the "
    "obligations of that class through these steps (GOV.14):\n\n"
    "- the regeneration of each result to be relied upon at the new class whose record lacks an input of REPRO.1 "
    "(REPRO.1);\n"
    "- the label unverified on each result to be relied upon at the new class that was judged against criteria set "
    "after it was seen (QA.12);\n"
    "- one review, at the independence of the row of the new class in the table of STND.CLASS.18, of the changes "
    "made since the last review at that independence, taken as one change, against the obligations of the new "
    "class (QA.7);\n"
    "- the audit that STND.CLASS.19 requires before the reliance (GOV.47);\n"
    "- the repetition, before the reliance, of each check that an obligation of the new class ties to an event that "
    "preceded the reclassification (GOV.14).\n\n"
    "Existing source SHALL conform, at the next change that touches it, to each default of form or style that the "
    "new class first applies to it and on whose outcome no reliance at the new class turns (GOV.42).")

CLASS23 = provision(
    "STND.CLASS", 23, "Records below the expected class", "Application by class", "default",
    ["REPRO.1", "REPRO.4", "REPRO.9", "VV.1", "VV.3"],
    ["NUMER.11", "STND.DEPS.12", "STND.DEPS.8", "STND.TEST.19", "MEAS.3", "MEAS.4", "HW.QPU.3"],
    "Where the classification records an expected class, work of CSQ4 SHOULD keep each record of the table of this "
    "provision that the provision beside it would ask of the work at that class, as that provision describes it "
    "(REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3).\n\n"
    "| Record | Provision |\n"
    "| --- | --- |\n"
    "| The basis of each tolerance | NUMER.11 |\n"
    "| The random seeds and the identity of the computational environment of each result | REPRO.1 |\n"
    "| Each lock file | STND.DEPS.12 |\n"
    "| Each toolchain revision | STND.DEPS.8 |\n"
    "| The source of each expected test value | STND.TEST.19 |\n"
    "| Each observation that is unable to be acquired again, as acquired, with its acquisition record | MEAS.3, "
    "MEAS.4 |\n"
    "| Each job on a quantum processor, with its execution record | HW.QPU.3 |",
    defines=["expected-class-records"])

CLASS_DOC = [
    # Purpose and scope.
    ("This standard fixes the criteria that place work in a consequence class (GOV.12), how the classification "
     "records and revises a class (GOV.13, GOV.14, GOV.24), what each class requires above the floor (GOV.11), the "
     "independence of review by class (QA.8), and the interval of compliance audit (GOV.47). STND.CLASS.10 and "
     "STND.CLASS.18 are defaults (GOV.19): a project constitution replaces one by a recorded decision (REPRO.7) with "
     "an alternative that meets the same outcome. The others, STND.CLASS.17 included, are binding, because they "
     "instantiate GOV or a prime directive, which belong to the floor (GOV.10).",
     "This standard fixes the criteria that place work in a consequence class (GOV.12), how the classification "
     "records and revises a class (GOV.13, GOV.14, GOV.24), what each class requires above the floor (GOV.11), the "
     "expected class and what it brings before the work reaches it (GOV.13), what a reclassification owes (GOV.14), "
     "the independence of review by class (QA.8), and the interval of compliance audit (GOV.47). STND.CLASS.10, "
     "STND.CLASS.18, STND.CLASS.21, and STND.CLASS.23 are defaults (GOV.19): a project constitution replaces one by "
     "a recorded decision (REPRO.7) with an alternative that meets the same outcome. The others, STND.CLASS.17 and "
     "STND.CLASS.22 included, are binding, because they instantiate GOV or a prime directive, which belong to the "
     "floor (GOV.10)."),
    # Terms.
    ("This section fixes meaning and imposes no obligation, as the Lexicon does.\n\n| Term | Definition |",
     "This section fixes meaning and imposes no obligation, as the Lexicon does. Session has the meaning that AGENT "
     "gives it.\n\n| Term | Definition |"),
    ("| Agent configuration | The model, the instruction revision, and the tools of an agent, as REPRO.11 records "
     "them. |",
     "| Agent configuration | The model, the instruction revision, and the tools of an agent, as REPRO.11 records "
     "them. |\n"
     "| Team | The actors, persons and agents alike, that act on the work under the direction of its human owner; "
     "an author's immediate team is the team of the work on which the author acts. |"),
    # Reading the standard, first paragraph.
    ("A class attaches to a use of the work, not to its code (GOV.14): the same code is CSQ4 in a notebook, CSQ2 "
     "once an actor other than its author builds on it, and CSQ1 once a relying party outside the project does. "
     "Growth of reliance includes the promotion of a result for a new use, the first output that leaves the "
     "project, and the first command to physical hardware.",
     "A class attaches to a use of the work, not to its code (GOV.14): the same code is CSQ4 in a notebook, CSQ3 "
     "once the author's immediate team builds on it through work verified before reliance, CSQ2 once an actor "
     "beyond that team builds on it, and CSQ1 once a relying party outside the project does. Growth of reliance "
     "includes the promotion of a result for a new use, the first output that leaves the project, and the first "
     "command to physical hardware. The class at inception is that of the uses then made of the work's outputs "
     "(GOV.13), so a project that plans a published result begins at CSQ4 or CSQ3 and reaches CSQ2 by "
     "reclassification before the result is relied upon at that class; the plan is recorded as the expected class "
     "(STND.CLASS.5), which an agent drafts with the classification and the human owner adopts with it in one act "
     "(GOV.50), and which sets no class until the use begins. Where an expected class is recorded, STND.CLASS.21 "
     "has the design leave open the parts of that class that are costly to add later, with the reason for each "
     "choice the expected class drives in a decision record, and STND.CLASS.23 has work of CSQ4 keep the records "
     "that a later reclassification is unable to reconstruct, each as the provision that holds it at CSQ3 describes "
     "it; the human owner's entry of the expected class is the recorded project decision naming the consequence "
     "that GOV.11 asks before lower governance raises the floor, so STND.CLASS.10 excepts the two from what work "
     "of CSQ4 omits, and work with no expected class stays as light as before. Nothing else is owed before the "
     "reclassification. Work that reaches a more severe class meets the obligations of that class for the work "
     "done at the less severe class through the steps of STND.CLASS.22, before it is relied upon there: past "
     "changes are reviewed once as one change at the new independence, against the obligations of the new class, "
     "an audit is held only on a move to CSQ2 or a more severe class, and each check tied to an event that has "
     "passed is repeated; GOV.14 is met, because every obligation of the new class is met before the reliance, "
     "and the one deferral is a default of form or style on whose outcome no reliance turns, which existing "
     "source meets at the next change that touches it. Reclassification names a change of class; promotion names "
     "the human owner's act on a result (QA.11)."),
    # Reading the standard, second paragraph.
    ("Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor.",
     "Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor, "
     "and, where the classification records an expected class, STND.CLASS.21 and the records of STND.CLASS.23."),
    # Reading the standard, last paragraph.
    ("Promotion (QA.11) governs every report of a result at every class, as Normative Language requires; work of "
     "CSQ4 needs no review until it is promoted or released, because it leaves CSQ4 when another actor relies on it.",
     "Promotion (QA.11) governs every report of a result at every class, as Normative Language requires; for work "
     "of CSQ3 or CSQ4, the adopted classification is the promotion of each result that meets its acceptance "
     "criteria for reliance by the author's immediate team through work verified before reliance, the reliance "
     "test of CSQ3 read as GOV.12 writes it, so that no result is promoted one by one below CSQ2, while reliance "
     "beyond that test needs its own promotion. Work of CSQ4 needs no review until it is promoted or released, "
     "because it leaves CSQ4 when another actor relies on it. The CSQ3 row of STND.CLASS.18 counts an agent in a "
     "session other than each of the author's as another actor, of the author's agent configuration or not, "
     "because a session whose context holds nothing of the author's sessions, beyond what the records of the work "
     "carry, examines the change cold; a reset of the author's context inside the authoring run is not such a "
     "session, so an author never reviews its own work. The CSQ2 row asks a different model or a different "
     "instruction revision, since a difference of tools alone leaves the same model reasoning under the same "
     "instructions. The auditor of the rows CSQ1 and CSQ2 of STND.CLASS.19 is read as the CSQ2 row of "
     "STND.CLASS.18 reads the reviewer: an agent whose model or instruction revision differs from that of every "
     "authoring agent, or a human who is not an author of the audited work. STND.CLASS.3 asks the money threshold "
     "once the class is CSQ2 or a more severe one, where a "
     "reclassification to CSQ1 first comes within reach; below CSQ2 the cost limb of the consequence test of CSQ1 "
     "has no stated amount to exceed, so it is not met, and STND.CLASS.2 does not count it met, because the doubt "
     "that provision resolves is doubt about the work and not the absence of an amount that the classification is "
     "not yet asked to state; the other limbs of the test, destroyed equipment, irreplaceable data or samples, and "
     "a failed campaign, still move work of CSQ3 to CSQ1. The audit of STND.CLASS.19 falls once on a move to CSQ2 "
     "or a more severe class, before the first reliance there, and then at the interval of its table. STND.CLASS.7 "
     "has the reassessment made before the next promotion of a result, release, or reliance at a more severe "
     "class, so that reported scenarios accumulate for one act of the human owner, while the use that occasioned a "
     "reassessment waits for it."),
]

CLASS_READING = (
    "GOV.13 as amended in LVL0 revision 1.7 is carried: STND.CLASS.5 has the classification state the expected "
    "class of the project or a component and the use that would occasion it (ruling C1); STND.CLASS.3 asks the "
    "money threshold only where the class is CSQ2 or a more severe class, and the cost limb of the CSQ1 test in "
    "STND.CLASS.1 reads the amount that STND.CLASS.3 has the classification state (CC10); new STND.CLASS.21, a "
    "default, has the design of work with a recorded expected class admit the parts of that class without rework, "
    "with the reason for each choice the expected class drives in a decision record, and owes no other record of "
    "that class before the reclassification (ruling C2); new STND.CLASS.22, binding, has the work done at the less "
    "severe class meet the obligations of the new class before reliance there through one review of the "
    "accumulated changes against those obligations, the regeneration or the label unverified of each result to be "
    "relied upon, the audit of STND.CLASS.19, and each event-tied check repeated, deferring to the next change "
    "that touches the source only a default of form or style on whose outcome no reliance turns, and STND.CLASS.19 "
    "audits once before work moved to CSQ2 or a more severe class is first relied upon there (ruling C3); new "
    "STND.CLASS.23, a default, has work of CSQ4 with a recorded expected class keep the records of its table as the "
    "provisions that hold them at CSQ3 describe them, and STND.CLASS.10 excepts STND.CLASS.21 and those records "
    "from what work of CSQ4 omits (ruling C4); the CSQ3 reliance test of STND.CLASS.1 reads the author's immediate "
    "team, as GOV.12 does, and the Terms define Team (ruling C5); the CSQ3 row of STND.CLASS.18 counts an agent in "
    "a session other than each of the author's, whose context holds nothing of those sessions beyond the records "
    "of the work, as another actor, of the author's configuration or not, Session in the meaning of AGENT, and the "
    "CSQ2 row asks an agent configuration that differs in its model or its instruction revision, whatever its "
    "tools (ruling C6); STND.CLASS.7 has the human owner reassess before a result of the work is next promoted, or "
    "the work is next released or relied upon at a more severe class (CC15)")
CLASS_ROW = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {CLASS_READING}. |"
CLASS_RATIONALE = (
    f"Minor amendment of STND.CLASS, revision 1.4, ratified by the custodian on {F.DATE}: {CLASS_READING}. The "
    "change is minor under STND.IDENT.3 because it adds the obligations of STND.CLASS.22 and the second sentence of "
    "STND.CLASS.5, adds the defaults STND.CLASS.21 and STND.CLASS.23, narrows STND.CLASS.3, STND.CLASS.7, and "
    "STND.CLASS.19, alters the cost limb of the CSQ1 test and the CSQ3 reliance test of STND.CLASS.1 and two rows "
    "of STND.CLASS.18, and adds one defined meaning, without altering the motivation or intent of the governance. "
    "No floor is raised (GOV.11): STND.CLASS.22 "
    "states how GOV.14, which already has every obligation of a class met before reliance at that class, is met "
    "for past work, at less cost than a review of each past change; STND.CLASS.5 adds one entry to a record the "
    "human owner adopts anyway, in the same act (GOV.50); STND.CLASS.21 and STND.CLASS.23 reach work of CSQ4 only "
    "where the classification records an expected class, and the human owner's entry of that class is the recorded "
    "project decision naming the consequence that GOV.11 asks before the floor is raised, so work with no expected "
    "class stays as light as before; every other change narrows an obligation or widens who counts as a reviewer. "
    "Class onsets: STND.CLASS.21 and STND.CLASS.23 apply from CSQ4 where an expected class is recorded, and "
    "STND.CLASS.22 at every reclassification. Transition (GOV.42): a classification adopted before this revision "
    "stands, with no expected class until the human owner adopts one; a project that moved to a more severe class "
    "before this revision meets STND.CLASS.22 before the next reliance at that class. Rulings C1 to C6 of "
    f"{RULINGS}; entries R3.1 to R3.4, R2.3, R2.4, and R2.5 (CC15) of the register; {RECORD}." + F.AUTHOR)


def apply_class(root: Path, at: str) -> None:
    replace_text(root, "STND/CLASS/1.md", CLASS1)
    replace_text(root, "STND/CLASS/3.md", CLASS3)
    replace_text(root, "STND/CLASS/5.md", CLASS5)
    replace_text(root, "STND/CLASS/7.md", CLASS7)
    replace_text(root, "STND/CLASS/10.md", CLASS10)
    replace_text(root, "STND/CLASS/18.md", CLASS18)
    replace_text(root, "STND/CLASS/19.md", CLASS19)
    (root / "STND/CLASS/21.md").write_text(CLASS21, encoding="utf-8")
    (root / "STND/CLASS/22.md").write_text(CLASS22, encoding="utf-8")
    (root / "STND/CLASS/23.md").write_text(CLASS23, encoding="utf-8")
    replace_text(root, "STND/CLASS/_doc.md", CLASS_DOC)
    F.check_fields(root, ["STND.CLASS.5", "STND.CLASS.22"], binding=True)
    F.check_fields(root, ["STND.CLASS.10", "STND.CLASS.21", "STND.CLASS.23"])
    F.finish(root, "STND/CLASS", "STND.CLASS", "1.3.1", "1.4", CLASS_ROW, CLASS_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# STND.PROJ 1.4
# ----------------------------------------------------------------------------------------------------------------

PROJ1 = [
    ("the consequence class (GOV.13); the proportionality judgment (GOV.11) |",
     "the consequence class (GOV.13); where a more severe use is planned, the expected class and the use that would "
     "occasion it (GOV.13); the proportionality judgment (GOV.11) |"),
]

PROJ_DOC = [
    ("A filled copy is a LVL3 instrument that the project's human owner adopts (GOV.41).",
     "A filled copy is a LVL3 instrument that the project's human owner adopts (GOV.41). The Classification "
     "section holds the expected class where a more severe use is planned (GOV.13, STND.CLASS.5), drafted by an "
     "agent with the rest of the classification and adopted with it, so that the human owner makes one act; the "
     "entry sets no class until the use begins, and it is what STND.CLASS.21 and STND.CLASS.23 read."),
]

PROJ_READING = (
    "the Classification row of STND.PROJ.1 holds, where a more severe use is planned, the expected class and the "
    "use that would occasion it (GOV.13)")
PROJ_ROW = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {PROJ_READING}. |"
PROJ_RATIONALE = (
    f"Minor amendment of STND.PROJ, revision 1.4, ratified by the custodian on {F.DATE}: {PROJ_READING}. The change "
    "is minor under STND.IDENT.3 because it adds an item to the content of a section that the binding STND.PROJ.1 "
    "requires, without altering the motivation or intent of the governance. No floor is raised (GOV.11): the entry "
    "is one line of a record the human owner adopts anyway, drafted by an agent (GOV.50), and it sets no class "
    "(GOV.13). Transition (GOV.42): a constitution adopted before this revision records no expected class until "
    f"the human owner adopts one. Ruling C1 of {RULINGS}; entry R3.1 of the register; {RECORD}." + F.AUTHOR)


def apply_proj(root: Path, at: str) -> None:
    replace_text(root, "STND/PROJ/1.md", PROJ1)
    replace_text(root, "STND/PROJ/_doc.md", PROJ_DOC)
    F.finish(root, "STND/PROJ", "STND.PROJ", "1.3", "1.4", PROJ_ROW, PROJ_RATIONALE, at)
