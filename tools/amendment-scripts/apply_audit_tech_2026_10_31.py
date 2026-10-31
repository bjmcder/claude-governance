"""Round of 2026-10-31 on the cleanup audit, part tech: the profiles and technical standards (S7, S8, B8, O3, I2, I6, I7).

Ten transactions, one per document, in citation order: the profiles first, then the standards that cite them.
- CPS 1.1 (minor): CPS.1 has work on a system that commands physical hardware classified CSQ3 or a more severe
  class (S7, recommendation R7); the Notes give the reason and the floor argument.
- NUMER 1.5 (minor): NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 apply from CSQ2
  by their field onset (O3); the Notes give the reason for the departure from the rule of STND.CLASS.
- ML 1.1 (minor): the term Learned model use leaves out the model through which an agent does the work, which the
  informative Selector text alone said before (I7).
- STND.VVUQ 1.5.2 (editorial): the Notes no longer say that work of CSQ3 meets NUMER through the core (O3).
- STND.CODE 1.8 (minor): STND.CODE.30 admits a dependence on the order of iteration that is declared as run-to-run
  variation and lies within the tolerance of each comparison that judges the result (I2).
- STND.DEPS 1.3.1 (editorial): the Notes on STND.DEPS.14 say that a run that retrieves a revision from outside the
  provisioned environment is network access (S8).
- STND.DOCS 1.0.3 (editorial): STND.DOCS.10 records its binding reason (I6).
- STND.CXX 1.6 (minor): STND.CXX.2 and STND.CXX.3 except an edition that a dependency fixes (B8), and STND.CXX.3
  records its binding reason (I6).
- STND.PY 1.5.1 (editorial): STND.PY.4 records its binding reason (I6).
- STND.RUST 1.5.1 (editorial): STND.RUST.6 records its binding reason (I6).

The order among the standards: STND.VVUQ cites only profiles among the documents of this part; STND.CODE holds the
practice of every language, which the language standards follow; STND.DEPS and STND.DOCS follow, then the language
standards. The standards cite each other in cycles, so no order puts every cited document first.

Run from harness/, through the driver:
    PARTS=apply_audit_tech_2026_10_31 python3 -B -m govharness rehearse governance \
        ../tools/amendment-scripts/apply_audit_2026_10_31.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
RECORD = "review-records/audit-2026-10-31/decisions.md"
PART_RECORD = "review-records/audit-2026-10-31/tech/decisions.md"
FINDINGS = "review-records/audit-2026-10-31/findings.md"


def cite(findings: str, ruling: str | None = None) -> str:
    """Return the closing citation of a rationale: the findings, the ruling if one, and the records."""
    text = f"Finding {findings} of {FINDINGS}" if "," not in findings and " and " not in findings \
        else f"Findings {findings} of {FINDINGS}"
    if ruling:
        text += f"; recommendation {ruling} of {FINDINGS}, put to the custodian at ratification"
    return f"{text}; {RECORD}; {PART_RECORD}."


def reason_field(text: str) -> tuple[str, str]:
    """Return the replacement that records a binding reason in place of the null field."""
    return ("binding_reason: null", f"binding_reason: {json.dumps(text, ensure_ascii=False)}")


# ------------------------------------------------------------------------------------------------------------ CPS 1.1

CPS1 = [
    ('instantiates: ["GOV.25", "GOV.26"]', 'instantiates: ["GOV.25", "GOV.26", "GOV.12", "PRIME.14"]'),
    ("This profile SHALL bind a project whose classification makes at least one attribute of the table of this "
     "provision true (GOV.25, GOV.26).",
     "This profile SHALL bind a project whose classification makes at least one attribute of the table of this "
     "provision true (GOV.25, GOV.26). Work on a system that commands, configures, or powers physical hardware "
     "SHALL be classified CSQ3 or a more severe class (GOV.12). Where a class less severe than CSQ3 is recorded "
     "for such work, an agent SHALL halt that line of work and refer it to the human owner (PRIME.14)."),
]

CPS_DOC = [
    ("cites PRIME.13 without instantiating it, so that the floor stays where LVL0 puts it.",
     "cites PRIME.13 without instantiating it, so that the floor stays where LVL0 puts it. CPS.1 has work on a "
     "system that commands, configures, or powers physical hardware classified CSQ3 or a more severe class, as "
     "GOV.12 lets a profile "
     "require of work in its domain: a wrong command is able to damage the hardware it drives, or what that "
     "hardware acts on, a loss beyond the author's own time that the consequence test of CSQ3 in STND.CLASS.1 "
     "counts, and the minimum keeps CPS.3 to CPS.9 in reach of all such work, the revision of the hazard analysis "
     "before an uncovered change first drives the hardware among them. The human owner sets that class "
     "(STND.CLASS.1); an agent that finds a less severe class recorded for such work halts that line of work and "
     "refers it, so that the CSQ3 content of this profile is not left out under a class that the profile does not "
     "admit, and the referral asks the owner only for the classification that STND.CLASS.1 already asks. A credible "
     "path to injury, or to a major and "
     "hard-to-reverse loss, still sets CSQ0 or CSQ1 (STND.CLASS.1), and a component that the classification records "
     "as isolated from every such system keeps the class recorded for it (GOV.13)."),
    ("because the failure that such content prevents reaches physical hardware at every class, where PRIME.13 and "
     "PRIME.4 hold. No provision raises the floor (GOV.11).",
     "because the failure that such content prevents reaches physical hardware at every class, where PRIME.13 and "
     "PRIME.4 hold. No provision raises the floor (GOV.11): the minimum class of CPS.1 is the one that GOV.12 lets "
     "a profile require, and the floor of GOV.10 holds for such work unchanged."),
]

CPS_READING = (
    "CPS.1 has work on a system that commands, configures, or powers physical hardware classified CSQ3 or a more "
    "severe class, as GOV.12 lets a profile require of work in its domain, so that CPS.3 to CPS.9, and with them the "
    "revision of the hazard analysis before an uncovered change first drives the hardware, reach all such work, and "
    "has an agent that finds a less severe class recorded for such work halt that line of work and refer it "
    "(PRIME.14); the Notes give the reason and the floor argument")


def apply_cps(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "CPS/1.md", CPS1)
    replace_text(root, "CPS/_doc.md", CPS_DOC)
    F.check_fields(root, ["CPS.1"], binding=True)
    row = f"| 1.1 | {date} | Minor amendment (GOV.41): {CPS_READING}. |"
    rationale = (
        f"Minor amendment of CPS, revision 1.1, ratified by the custodian on {date}: {CPS_READING}. Reading: GOV.12 "
        "provides that a profile MAY require work in its domain to be classified at least as severe as a stated "
        "class, and STND.CLASS.1 has the human owner set the class that a selected profile requires; the domain "
        "items of CPS are the systems that command, configure, or power physical hardware, the reach of the "
        "attribute Physical hardware control, so the minimum reaches work on such a system and leaves a component "
        "recorded as isolated from them under GOV.13; the classification stays the human owner's act, and an agent "
        "that finds a less severe class recorded for such work halts that line of work and refers it (PRIME.14), so "
        "that the CSQ3 content of the profile is not silently left out under the recorded class. The change is minor "
        "under "
        "STND.IDENT.3 because it adds an obligation, without altering the motivation or intent of the governance. "
        "Floor (GOV.11): the floor is the set of GOV.10, which holds at every class and is unchanged; the minimum "
        "places work of the domain in a class by the means that GOV.12 itself gives a profile, and the obligations "
        "that it brings to work that was CSQ4, CPS.3 to CPS.9 among them, are the obligations above the floor that "
        "GOV.11 proportions to CSQ3. It proportions them to the consequence, not to the setting or hardware of the "
        "work (PRIN.9): a wrong command is able to damage the hardware it drives, a loss beyond the author's own "
        "time that the consequence test of CSQ3 in STND.CLASS.1 counts and that STND.CLASS.2 already counts met in "
        "doubt. The obligations fall on work at the decisions that the human owner already makes, the "
        "classification and the adoption of the hazard analysis under PRIME.13, and ask of the owner no decision "
        "beyond those LVL0 assigns (STND.DRAFT.42); the referral of the second sentence asks only for the "
        "classification that STND.CLASS.1 already asks, and it instantiates PRIME.14, which holds at every class. "
        "Alternative weighed: PRIME.13 carrying the revision duty at "
        "every class, which amends a prime directive and is put to the custodian with the recommendation. "
        "Transition (GOV.42): a project whose classification records CSQ4 for work on a system that commands, "
        "configures, or powers physical hardware records CSQ3 or a more severe class for it before that system next "
        "drives the hardware; the referral of an agent that meets such a record is the occasion for it, and until the "
        "class is recorded the work, conforming to revision 1.0.2, is not in defect. "
        + cite("S7", "R7") + F.AUTHOR)
    F.finish(root, "CPS", "CPS", "1.0.2", "1.1", row, rationale, at)


# ---------------------------------------------------------------------------------------------------------- NUMER 1.5

ONSET_PART2 = ('onset: "CSQ3"', 'onset: ["CSQ3", ["sentence 2", "CSQ2"]]')
ONSET_CSQ2 = ('onset: "CSQ3"', 'onset: "CSQ2"')

NUMER_DOC = [(
    "because each costs one statement, one record, or one message and the error it exposes is silent at every class.",
    "because each costs one statement, one record, or one message and the error it exposes is silent at every class. "
    "NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 apply from CSQ2, a departure "
    "from the rule of STND.CLASS: an order test, an estimate of rounding error under conditioning, a showing that "
    "the working precision keeps that error within the required precision, evidence that a statistical uncertainty "
    "has settled as the samples grow, and the error rates of a statistical criterion each cost an analysis or added "
    "computations rather than one statement, and STND.VVUQ gives its default method for each only from CSQ2. The "
    "core of STND.VVUQ still reaches two of them at CSQ3: STND.VVUQ.7 places a tolerance within its bracket, with "
    "the required precision as the departure to detect, and tiers 3 and 5 of the table of STND.VVUQ.1 rest the "
    "agreement of a comparison on an estimate of rounding error and on a criterion with stated error rates; HW.QPU.6 "
    "and HDES.ASIC.5 keep the content of NUMER.23 and NUMER.25 at CSQ3 within their domains. VV.1, VV.5, NUMER.13, "
    "and PRIME.3 hold for these results at CSQ3 in full, so a result of CSQ3 that lacks the evidence that a moved "
    "part would supply has the component concerned marked not assessed under NUMER.13, and carries the label "
    "unverified of PRIME.3 where it lacks the evidence that VV requires. The third sentence of NUMER.5 keeps CSQ3 "
    "and governs a record of the working precision that work below CSQ2 keeps by choice."),
]

NUMER_READING = (
    "NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 apply from CSQ2 by their field "
    "onset, in place of CSQ3, and the Notes give the reason for the departure from the rule of STND.CLASS: each asks "
    "an analysis or added computations whose default methods are those of STND.VVUQ beyond its core")


def apply_numer(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "NUMER/5.md", [ONSET_PART2])
    replace_text(root, "NUMER/7.md", [ONSET_CSQ2])
    replace_text(root, "NUMER/12.md", [ONSET_CSQ2])
    replace_text(root, "NUMER/23.md", [ONSET_PART2])
    replace_text(root, "NUMER/25.md", [ONSET_CSQ2])
    replace_text(root, "NUMER/_doc.md", NUMER_DOC)
    row = f"| 1.5 | {date} | Minor amendment (GOV.41): {NUMER_READING}. |"
    rationale = (
        f"Minor amendment of NUMER, revision 1.5, ratified by the custodian on {date}: {NUMER_READING}. Reading: "
        "the default methods for each part moved, STND.VVUQ.20 to STND.VVUQ.24 for NUMER.7, STND.VVUQ.36 and "
        "STND.VVUQ.37 for NUMER.12, STND.VVUQ.9, STND.VVUQ.36, STND.VVUQ.37, and STND.VVUQ.38 for the second "
        "sentence of NUMER.5, the second sentence of STND.VVUQ.61 for the second sentence of NUMER.23, and "
        "STND.VVUQ.33 to STND.VVUQ.35 and STND.VVUQ.65 for NUMER.25, start at CSQ2, and the core that applies "
        "from CSQ3 gives a method for none of them, reaching NUMER.12 and NUMER.25 only through tiers 3 and 5 of "
        "STND.VVUQ.1 and through STND.VVUQ.7, so that the Notes of STND.CLASS admit a more severe class for each; a "
        "result of CSQ3 without the evidence that a moved part would supply has the component marked not assessed "
        "(NUMER.13), and carries the label unverified where it lacks the evidence that VV requires (PRIME.3). The change is minor under STND.IDENT.3 because it alters the class from which five obligations "
        "apply, without altering the motivation or intent of the governance. Floor (GOV.11): moving an onset from "
        "CSQ3 to CSQ2 narrows a waivable default to more severe work, so it lowers no floor and raises none; the "
        "floor of GOV.10 is unchanged, and VV.1, VV.5, and PRIME.3, which these parts serve, apply to work of CSQ3 "
        "in full under STND.CLASS.10. Onset: NUMER.7, NUMER.12, and NUMER.25 \"CSQ2\"; NUMER.5 and NUMER.23 "
        "[\"CSQ3\", [\"sentence 2\", \"CSQ2\"]]. Transition (GOV.42): none; work of CSQ3 that meets these parts "
        "is not in defect, and work of CSQ2 or a more severe class owes them as before. " + cite("O3") + F.AUTHOR)
    F.finish(root, "NUMER", "NUMER", "1.4.1", "1.5", row, rationale, at)


# ------------------------------------------------------------------------------------------------------------- ML 1.1

ML_DOC = [
    ("| Learned model use | An attribute, true when the classification records that a learned model sits, or is "
     "admitted to sit, on a path that affects a result the work reports or relies on, or physical hardware. |",
     "| Learned model use | An attribute, true when the classification records that a learned model sits, or is "
     "admitted to sit, on a path that affects a result the work reports or relies on, or physical hardware. A "
     "learned model in its use as the model through which an agent does the work does not make the attribute "
     "true. That exclusion does not reach a learned model that the work builds, trains, or runs as part of what it "
     "delivers, even when it is the model of an agent. |"),
    ("The models through which agents do the work are governed by the agent practice profile (AGENT) and the "
     "Safeguards Article (GUARD), not by this profile.",
     "The term Learned model use leaves out the model through which an agent does the work, which the agent "
     "practice profile (AGENT) and the Safeguards Article (GUARD) govern, and keeps a learned model that the work "
     "builds, trains, or runs as part of what it delivers, even when an agent uses that model too."),
]

ML_READING = (
    "the term Learned model use leaves out a learned model in its use as the model through which an agent does the "
    "work, an exclusion that only the informative Selector text stated before, and keeps a learned model that the "
    "work builds, trains, or runs as part of what it delivers, even when it is the model of an agent; the Selector "
    "text cites the term")


def apply_ml(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "ML/_doc.md", ML_DOC)
    row = f"| 1.1 | {date} | Minor amendment (GOV.41): {ML_READING}. |"
    rationale = (
        f"Minor amendment of ML, revision 1.1, ratified by the custodian on {date}: {ML_READING}. Reading: taken "
        "literally, the agent's own model sits on the path of every result that the agent produces, so the "
        "attribute was true for every project in which an agent works, against the Selector text; the term now "
        "says what the Selector text said, and bounds it, so that a project that builds, trains, or runs a learned model "
        "as part of what it delivers, an agent among such products, keeps the attribute. The change is "
        "minor under STND.IDENT.3 because it alters a defined meaning, without altering the motivation or intent "
        "of the governance. Floor (GOV.11): the change raises no obligation; it narrows the selector of this "
        "profile to the reach that its Notes always gave it, and the agent's model stays under GOV.48, AGENT, and "
        "GUARD, which this profile never carried. Transition (GOV.42): none; a classification that recorded the "
        "attribute only for the agent's model may drop it at its next revision. " + cite("I7") + F.AUTHOR)
    F.finish(root, "ML", "ML", "1.0.2", "1.1", row, rationale, at)


# ----------------------------------------------------------------------------------------------------- STND.VVUQ 1.5.2

VVUQ_DOC = [(
    "the methods of high-assurance numerics, from error budgets and noise floors to multiplicity control and order "
    "tests at several levels, start at CSQ2, so that work of CSQ3 meets NUMER through the core, while the "
    "obligations of LVL0 that the other provisions serve apply to it in full.",
    "the methods of high-assurance numerics, from error budgets and noise floors to multiplicity control and order "
    "tests at several levels, start at CSQ2, as do NUMER.7, NUMER.12, NUMER.25, and the second sentences of "
    "NUMER.5 and NUMER.23, whose default methods are among them. Work of CSQ3 meets each other provision of NUMER "
    "through the core where the core reaches it, and otherwise by a method that the work chooses or by the "
    "statement that the provision admits, a component of NUMER.13 marked not assessed among them, while the "
    "obligations of LVL0 that the other provisions serve apply to it in full. For a comparison that takes tier 3, "
    "the table of STND.VVUQ.1 gives a tolerance set from an estimate of rounding error of the kind that NUMER.12 "
    "describes, and for one that takes tier 5, a criterion with a stated probability of rejecting a correct result "
    "and a stated detection power, the content of NUMER.25."),
]

VVUQ_READING = (
    "the Notes say that NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 start at CSQ2 "
    "with their default methods, and that work of CSQ3 meets each other provision of NUMER through the core where "
    "the core reaches it and otherwise by a method of its choice or by the statement that the provision admits, in "
    "place of saying that work of CSQ3 meets NUMER through the core")


def apply_vvuq(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/VVUQ/_doc.md", VVUQ_DOC)
    row = (f"| 1.5.2 | {date} | Editorial amendment (GOV.41): {VVUQ_READING}; no obligation, permission, or "
           "defined meaning changes. |")
    rationale = (
        f"Editorial amendment of STND.VVUQ, revision 1.5.2, ratified by the custodian on {date}: {VVUQ_READING}. "
        "Reading: the core that applies from CSQ3 gives no method for NUMER.7, NUMER.12, NUMER.13, NUMER.23, or "
        "NUMER.25, so the Notes claimed more than the core does; NUMER 1.5 moves the parts whose methods start at "
        "CSQ2, and NUMER.13 is met at CSQ3 by its markings. The change is editorial under STND.IDENT.3 because only "
        "the Notes change, and no obligation, permission, or defined meaning of this document changes. Floor "
        "(GOV.11): unchanged. Transition (GOV.42): none. " + cite("O3") + F.AUTHOR)
    F.finish(root, "STND/VVUQ", "STND.VVUQ", "1.5.1", "1.5.2", row, rationale, at)


# ------------------------------------------------------------------------------------------------------ STND.CODE 1.8

CODE30 = [(
    "each reported result on whose path the collection lies SHOULD be independent of that order (REPRO.3).",
    "each reported result on whose path the collection lies SHOULD be independent of that order, or have its "
    "dependence on that order declared as run-to-run variation and lie within the tolerance of each comparison "
    "that judges it (REPRO.3)."),
]

CODE_DOC = [(
    "a set of strings in Python and a `Dict` or a `Set` in Julia (the Notes of STND.PY and STND.JL).",
    "a set of strings in Python and a `Dict` or a `Set` in Julia (the Notes of STND.PY and STND.JL). Its second "
    "sentence asks no bitwise identity: a result that depends on such an order meets it once that dependence is "
    "declared as run-to-run variation and lies within the tolerance of each comparison that judges the result, as "
    "STND.BUILD.15 admits for the output of a build step, and STND.VVUQ.82 then treats the difference as no "
    "defect."),
]

CODE_READING = (
    "the second sentence of STND.CODE.30 also admits a reported result whose dependence on the order of iteration "
    "of a collection is declared as run-to-run variation and lies within the tolerance of each comparison that "
    "judges it (REPRO.3), as STND.BUILD.15 does for the output of a build step, so that it asks no bitwise "
    "identity, and the Notes say so")


def apply_code(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/CODE/30.md", CODE30)
    replace_text(root, "STND/CODE/_doc.md", CODE_DOC)
    row = f"| 1.8 | {date} | Minor amendment (GOV.41): {CODE_READING}. |"
    rationale = (
        f"Minor amendment of STND.CODE, revision 1.8, ratified by the custodian on {date}: {CODE_READING}. "
        "Reading: REPRO.3 admits outputs identical within a declared tolerance and outputs whose variation is "
        "declared, so a default that read as asking bitwise identity of every result on such a path went beyond "
        "the direction on determinism that STND.VVUQ.82 and STND.VVUQ.83 carry; the onset stays CSQ3. The change "
        "is minor under STND.IDENT.3 because it widens a recommendation, without altering the motivation or intent "
        "of the governance. Floor (GOV.11): the change narrows a waivable default and raises nothing; undeclared "
        "variation stays a defect under REPRO.3. Transition (GOV.42): none. " + cite("I2") + F.AUTHOR)
    F.finish(root, "STND/CODE", "STND.CODE", "1.7", "1.8", row, rationale, at)


# ---------------------------------------------------------------------------------------------------- STND.DEPS 1.3.1

DEPS_DOC = [(
    "so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts.",
    "so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts; a run of "
    "such a check that retrieves a revision from outside the provisioned environment is also network access, which "
    "needs its own authorization (GUARD.13), as the Notes of STND.DFLT say of every install that retrieves."),
]

DEPS_READING = (
    "the Notes on STND.DEPS.14 say that a run of its checks that retrieves a revision from outside the provisioned "
    "environment is also network access, which needs its own authorization (GUARD.13)")


def apply_deps(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/DEPS/_doc.md", DEPS_DOC)
    row = (f"| 1.3.1 | {date} | Editorial amendment (GOV.41): {DEPS_READING}; no obligation, permission, or defined "
           "meaning changes. |")
    rationale = (
        f"Editorial amendment of STND.DEPS, revision 1.3.1, ratified by the custodian on {date}: {DEPS_READING}. "
        "Reading: the Notes said that such a check adds nothing that STND.DFLT.35 halts, which an agent could read "
        "as leave to fetch, while GUARD.13 makes every retrieval from outside the provisioned environment network "
        "access; the Notes now say what the Notes of STND.DFLT already say. The change is editorial under "
        "STND.IDENT.3 because only the Notes change, and no obligation, permission, or defined meaning of this "
        "document changes. Floor (GOV.11): unchanged. Transition (GOV.42): none. " + cite("S8") + F.AUTHOR)
    F.finish(root, "STND/DEPS", "STND.DEPS", "1.3", "1.3.1", row, rationale, at)


# ---------------------------------------------------------------------------------------------------- STND.DOCS 1.0.3

CARRY = ("; as a binding provision it reaches every agent in every project, since STND.INSTR.10 has an agent meet "
         "each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48), so ")

DOCS10_REASON = (
    "The human owner and the reviewers of every project verify the text that an agent writes against the work "
    "(INTPR.1), and inflated or generic prose, notes about the agent, and known false statements defeat that check "
    "at every class" + CARRY + "each reader relies on agent-written text without first learning the class of the "
    "work, while the spelling, content, and patterns stay each project's through the alternatives "
    "it adopts.")

DOCS_DOC = [(
    "It binds by its own force (GOV.48); STND.INSTR.10 carries it",
    "It binds by its own force (GOV.48), for the reason of uniformity across projects that its field "
    "`binding_reason` records (GOV.19); STND.INSTR.10 carries it"),
]

BINDING_ROW = ("{p} records in its field binding_reason why uniformity across projects requires it to bind (GOV.19), "
               "for the custodians to adopt with this revision, and the Notes cite the field")


def binding_rationale(doc: str, rev: str, date: str, reading: str, prov: str, extra: str = "") -> str:
    return (
        f"Editorial amendment of {doc}, revision {rev}, ratified by the custodian on {date}: {reading}. Reading: "
        f"{prov} instantiates GOV.48, a provision of GOV and so of the floor (GOV.10), and binds by that lineage "
        "under the first limb of GOV.19; it is also a rule of the form of the work that agents write, which GOV.19 "
        "names among the defaults, and recording the reason of uniformity meets GOV.19 on either reading, as the "
        "field does for STND.DRAFT.35 to STND.DRAFT.41. The provision is kept binding rather than made a default "
        "from CSQ3, because a default could be omitted at CSQ4 and the outcome that it guards is lost at every "
        f"class.{extra} The change is editorial under STND.IDENT.3 because no obligation, permission, or defined "
        f"meaning changes. Floor (GOV.11): unchanged; {prov} binds as before. Transition (GOV.42): none. "
        + cite("I6") + F.AUTHOR)


def apply_docs(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/DOCS/10.md", [reason_field(DOCS10_REASON)])
    replace_text(root, "STND/DOCS/_doc.md", DOCS_DOC)
    reading = BINDING_ROW.format(p="STND.DOCS.10")
    row = (f"| 1.0.3 | {date} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    F.finish(root, "STND/DOCS", "STND.DOCS", "1.0.2", "1.0.3", row,
             binding_rationale("STND.DOCS", "1.0.3", date, reading, "STND.DOCS.10"), at)


# ------------------------------------------------------------------------------------------------------ STND.CXX 1.6

CXX2 = [(
    "Other than for an edition that STND.CODE.19, a hardware contract, or a qualification of the toolchain fixes,",
    "Other than for an edition that STND.CODE.19, a dependency, a hardware contract, or a qualification of the "
    "toolchain fixes,"),
]

CXX3_REASON = (
    "An agent that meets a compiler error in any project is able to clear it by lowering the edition, which loses "
    "the edition in force silently" + CARRY + "each lowering is visible in a decision record in every project, at "
    "the cost of one sentence, while the edition itself stays each project's (STND.CXX.2 or its "
    "alternative).")

CXX3_BODY = (
    "Other than in a change whose decision record names the compiler, the dependency, the high-assurance coding "
    "standard, the hardware contract, or the qualification of the toolchain that requires it, an agent SHALL NOT "
    "lower the edition in force for a translation unit (GOV.48, DSGN.3). Other than in a change whose decision record "
    "names the compiler, the dependency, the high-assurance coding standard, the hardware contract, or the "
    "qualification of the toolchain that requires it, an agent SHALL NOT state for a translation unit that it "
    "creates an edition older than the edition that STND.CXX.2, or the alternative that a project instrument adopts "
    "in its place, gives (GOV.48, DSGN.3).")

CXX_DOC = [
    ("STND.CXX.3 instantiates GOV.48, binds agents alone, and is binding at every class;",
     "STND.CXX.3 instantiates GOV.48, binds agents alone, and is binding at every class, for the reason of "
     "uniformity across projects that its field `binding_reason` records (GOV.19);"),
    ("while the decision record that the provision accepts costs one sentence.",
     "while the decision record that the provision accepts costs one sentence. That record names the cause among "
     "those that STND.STDC.3 admits for C: the compiler, a dependency whose source does not compile at the edition "
     "in force, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain; "
     "STND.CXX.2 leaves out of its recommendation the edition that a dependency fixes."),
]

CXX_READING = (
    "STND.CXX.2 leaves out of its recommendation an edition that a dependency fixes, and STND.CXX.3 admits a "
    "decision record that names the dependency that requires a lower edition, as STND.STDC.3 does for C (B8); "
    "STND.CXX.3 records in its field binding_reason why uniformity across projects requires it to bind (GOV.19), "
    "for the custodians to adopt with this revision (I6); the Notes follow")


def apply_cxx(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/CXX/2.md", CXX2)
    F.set_body(root, "STND/CXX/3.md", CXX3_BODY, binding_reason=CXX3_REASON)
    replace_text(root, "STND/CXX/_doc.md", CXX_DOC)
    row = f"| 1.6 | {date} | Minor amendment (GOV.41): {CXX_READING}. |"
    rationale = (
        f"Minor amendment of STND.CXX, revision 1.6, ratified by the custodian on {date}: {CXX_READING}. Reading: "
        "a third-party header that fails to compile at the newest edition left an agent no decision record that "
        "allowed the lower edition, even at CSQ4, so it halted and referred; STND.STDC.3 already names the "
        "dependency among the causes, and STND.CXX.2 and STND.CXX.3 now name it too. STND.CXX.3 instantiates "
        "GOV.48, a provision of GOV and so of the floor (GOV.10), and binds by that lineage under the first limb of "
        "GOV.19; recording the reason of uniformity meets GOV.19 also on the reading that a rule of the form of the "
        "work is a default unless the custodians record why uniformity requires otherwise, and it stays binding "
        "rather than becoming a default from CSQ3, because a default could be omitted at CSQ4, where the "
        "custodian's direction on the edition would be lost silently. The change is minor under STND.IDENT.3 "
        "because it widens the exception of a binding prohibition and of a recommendation, without altering the "
        "motivation or intent of the governance. Floor (GOV.11): the change raises nothing; the exception costs the "
        "one decision record that STND.CXX.3 already asks, and that STND.CXX.3 raises no floor is the custodian's "
        "ruling of 2026-10-23, which the Notes cite. Transition (GOV.42): none. " + cite("B8 and I6") + F.AUTHOR)
    F.finish(root, "STND/CXX", "STND.CXX", "1.5", "1.6", row, rationale, at)


# ------------------------------------------------------------------------------------------------------ STND.PY 1.5.1

PY4_REASON = (
    "Code that an agent writes moves between projects and between classes, and an annotation costs the agent only "
    "the form of that code while its absence costs a rewrite at each reclassification" + CARRY + "agent-written "
    "Python is ready in every project for the checker that the project adopts, while "
    "the form stays each project's through the alternative it adopts in place of STND.PY.3.")

PY_DOC = [(
    "so STND.PY.4 binds every agent at every class by its own force (GOV.48), and STND.INSTR.10",
    "so STND.PY.4 binds every agent at every class by its own force (GOV.48), for the reason of uniformity across "
    "projects that its field `binding_reason` records (GOV.19), and STND.INSTR.10"),
]


def apply_py(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/PY/4.md", [reason_field(PY4_REASON)])
    replace_text(root, "STND/PY/_doc.md", PY_DOC)
    reading = BINDING_ROW.format(p="STND.PY.4")
    row = (f"| 1.5.1 | {date} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    extra = " That STND.PY.4 raises no floor is the custodian's ruling of 2026-10-23, which the Notes cite."
    F.finish(root, "STND/PY", "STND.PY", "1.5", "1.5.1", row,
             binding_rationale("STND.PY", "1.5.1", date, reading, "STND.PY.4", extra), at)


# ---------------------------------------------------------------------------------------------------- STND.RUST 1.5.1

RUST6_REASON = (
    "Unsafe code that an agent writes without its soundness argument compiles and passes its tests in every "
    "project, while it leaves a reviewer nothing to check the code against" + CARRY + "the reviewers of every "
    "project find the argument at agent-written unsafe code, while its form stays each "
    "project's (STND.RUST.3 or its alternative).")

RUST_DOC = [(
    "STND.RUST.6 binds every agent at every class by its own force (GOV.48), and STND.INSTR.10",
    "STND.RUST.6 binds every agent at every class by its own force (GOV.48), for the reason of uniformity across "
    "projects that its field `binding_reason` records (GOV.19), and STND.INSTR.10"),
]


def apply_rust(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/RUST/6.md", [reason_field(RUST6_REASON)])
    replace_text(root, "STND/RUST/_doc.md", RUST_DOC)
    reading = BINDING_ROW.format(p="STND.RUST.6")
    row = (f"| 1.5.1 | {date} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    F.finish(root, "STND/RUST", "STND.RUST", "1.5", "1.5.1", row,
             binding_rationale("STND.RUST", "1.5.1", date, reading, "STND.RUST.6"), at)


STEPS = [apply_cps, apply_numer, apply_ml, apply_vvuq, apply_code, apply_deps, apply_docs, apply_cxx, apply_py,
         apply_rust]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, step in enumerate(STEPS):
        step(root, (start + timedelta(seconds=k)).isoformat())
