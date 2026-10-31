"""Round of 2026-10-31 on the cleanup audit, part process: the process standards and AGENT.

Eight transactions, one per document, after the lvl0 and tech parts, conforming to LVL0 as the lvl0 part amends it:
- STND.DFLT 1.7 (minor): R1 lower part (STND.DFLT.33 and the Notes), R3 lower part (the term Given directly and
  new STND.DFLT.36), R4 (STND.DFLT.23 and the term Foreign entry), R10 (the term Working bounds), B3
  (STND.DFLT.15), O7 (STND.DFLT.20), I1 (STND.DFLT.17), I9 (STND.DFLT.5), new STND.DFLT.38 and a row of
  STND.DFLT.18 (R4), and the conforming STND.DFLT.7, STND.DFLT.19, and new STND.DFLT.37 (the record of PRIME.9).
- AGENT 1.4 (minor): R1 lower part (AGENT.6 and the Notes on AGENT.6 and AGENT.8).
- STND.CLASS 1.6 (minor): O7 (STND.CLASS.22), the conforming STND.CLASS.20 and row of CSQ1 of STND.CLASS.10, and
  the Notes.
- STND.IDENT 1.6 (minor): R6 (STND.IDENT.23).
- STND.WPROC 1.5 (minor): B9 (the term Main line).
- STND.CREW 1.4 (minor): the conforming STND.CREW.13 and STND.CREW.21, the term Lead agent, and the Notes.
- STND.PROJ 1.6 (minor): O5 (STND.PROJ.2 and the Notes), a signing row of STND.PROJ.3, and the conforming row
  Physical hardware of STND.PROJ.1.
- STND.INSTR 1.6 (minor): O6 (STND.INSTR.11).

The order: STND.DFLT first, since every other document of the part cites it or its new text (AGENT and STND.CLASS
cite STND.DFLT.33, .20, and .23); then AGENT, which STND.CREW and STND.CLASS cite; STND.CLASS, which STND.WPROC and
STND.CREW cite; STND.IDENT; STND.WPROC, which STND.CREW cites; STND.CREW; then STND.PROJ and STND.INSTR, which cite
STND.DFLT and are cited by no document of the part. The documents cite each other in cycles, so no order puts every
cited document first.

Run from harness/, through the driver:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_audit_2026_10_31.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_process_dflt as D  # noqa: E402
import audit_process_docs as P  # noqa: E402
import rounds_common as F  # noqa: E402
from apply_audit_lvl0_2026_10_31 import NEW as LVL0_REV  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
RECORD = "review-records/audit-2026-10-31/decisions.md"
PART_RECORD = "review-records/audit-2026-10-31/process/decisions.md"
FINDINGS = "review-records/audit-2026-10-31/findings.md"
REVIEWS = ("review-records/audit-2026-10-31/process/review.md and "
           "review-records/audit-2026-10-31/reconciliation.md")
LVL0 = f"LVL0 {LVL0_REV}"


def cite(findings: str, rulings: str | None = None) -> str:
    """Return the closing citation of a rationale: the findings, the recommendations if any, and the records."""
    word = "Findings" if ("," in findings or " and " in findings) else "Finding"
    text = f"{word} {findings} of {FINDINGS}"
    if rulings:
        text += f"; {rulings} of {FINDINGS}, put to the custodian at ratification"
    return f"{text}; {RECORD}; {PART_RECORD}, with the reviews {REVIEWS}."


def provision(doc_id: str, n: int, title: str, section: str, instantiates: list[str], refers_to: list[str],
              body: str, date: str) -> str:
    """Return the file text of a new binding LVL2 provision; rank and waivable are derived afterwards."""
    ids = lambda xs: "[" + ", ".join(f'"{x}"' for x in xs) + "]"  # noqa: E731
    return "\n".join([
        "---", f'id: "{doc_id}.{n}"', 'level: "LVL2"', 'kind: "provision"', f'title: "{title}"',
        f'section: "{section}"', 'status: "adopted"', f'adopted: "{date}"', 'mode: "binding"',
        "binding_reason: null", f"instantiates: {ids(instantiates)}", f"refers_to: {ids(refers_to)}",
        "rank: null", "waivable: false", "defines: []", 'checked_by: ["review"]', "---", "", body, "",
    ])


TRANSITION = (
    "Transition (GOV.42): work that conformed to the prior revision is not in defect for the period before this "
    "revision is entered, and the conforming of this revision to " + LVL0 + " ends the interval in which LVL0 "
    "governed the stale text (GOV.1). ")

# ------------------------------------------------------------------------------------------------------- STND.DFLT


def apply_dflt(root: Path, at: str) -> None:
    date = at[:10]
    for rel, body, fields in D.BODIES:
        F.set_body(root, rel, body, **fields)
    for n, title, section, inst, refs, body in D.NEW:
        (root / f"STND/DFLT/{n}.md").write_text(
            provision("STND.DFLT", n, title, section, inst, refs, body, date), encoding="utf-8")
    replace_text(root, "STND/DFLT/18.md", [D.DFLT18_ROW])
    replace_text(root, "STND/DFLT/_doc.md", D.DOC)
    F.check_fields(root, D.CHANGED, binding=True)
    reading = D.READING.format(lvl0=LVL0)
    row = f"| 1.7 | {date} | Minor amendment (GOV.41): {reading}. |"
    rationale = (
        f"Minor amendment of STND.DFLT, revision 1.7, ratified by the custodian on {date}: {reading}. Reading: under "
        f"{LVL0}, PRIME.8 authorizes the operating cost of the agents that carry out a direction of work, within a "
        "spending limit, a fixed cost, or an estimate that the agent states before the work begins, and GOV.36, "
        "read restrictively under GOV.9, has that authorization, and under QA.11 the promotion that the direction "
        "makes of presumed CSQ4 work, entered, so STND.DFLT.33 keeps the entry of the direction and no longer "
        "restates a bound; PRIME.11 admits a person whom the human owner names by a recorded act, so the defaults "
        "say what a message given directly is and whose acts an agent takes as the human owner's, without "
        "establishing ownership (PRIN.1), and a naming counts only by an accepted entry; an injected ledger line "
        "gains no authority by whatever route it comes, since every entry of an act of the human owner after the "
        "accepted point that the agent did not append in its session waits for the owner's confirmation, by "
        "position and hash, gathered in one statement, and the acceptance entry that an agent appends at the end of "
        "each session in which it appended an entry keeps its own entries from being foreign to the next; PRIME.9 asks the human owner's provisioning record that an environment is "
        "isolated, and STND.DFLT.37 places it in the ledger and confines it to the environment it names; GUARD.7 adds "
        "the ground of an item that the agent created in the current unit, that the history does not yet hold, on "
        "which no reported result rests, and that no other actor has changed since the agent last wrote it, which "
        "the sixth class takes exactly, with a digest as its check and references of the history excluded; "
        "GOV.13 and GOV.20 now read \"commanding, configuring, or powering\" physical hardware, which STND.DFLT.19 "
        "follows; GUARD.10 "
        "adds revocation, which an agent meets by reading the ledger before each action under a standing grant. "
        "Class: minor under STND.IDENT.3, because obligations, permissions, and defined meanings are added and "
        "altered without altering the motivation or intent of the governance. Floor (GOV.11): every provision of "
        "this standard is binding, since it instantiates GOV.22, and each change either conforms to "
        f"{LVL0} or tightens within it, so that no condition that PRIME or GUARD prohibits becomes reachable: "
        "STND.DFLT.23 accepts fewer unsigned entries than before, and a foreign entry gains authority only by the "
        "human owner's act; STND.DFLT.38 asks one entry per session that appended one; the new row of STND.DFLT.18 "
        "states a residual, forgery up to the accepted point, as unprotected (GUARD.16); STND.DFLT.17 adds the entry before reliance and the reading before each action under a "
        "standing grant, each one record or one read; STND.DFLT.33 asks the one entry that it asked before, now of "
        "each direction, the scribe entry that GOV.36 asks of the authorization of PRIME.8 and of the "
        "promotion of QA.11, without its secrets, and the bound and its figure are PRIME.8's own; STND.DFLT.36 identifies whose messages carry the human "
        "owner's authority only where no accepted entry names another person, takes a naming only from an accepted "
        "entry, refers what it is unable to place, and grants nothing, since the acts stay the human owner's "
        "(PRIME.1); STND.DFLT.37 is one entry of a statement that PRIME.9 already asks, reaching only the "
        "environment it names; STND.DFLT.19 halts for the same hardware that PRIME.13 names; the sixth "
        "exempt class is the ground that GUARD.7 as amended admits, and no more; the term Working bounds admits the tool's use of the credential means "
        "only under an authorization of the human owner, in that action alone, and the agent reads, passes, "
        "and stores no secret and changes none of the configuration of those means (PRIME.10, AGENT.45); STND.DFLT.7 follows QA.1 as amended; STND.DFLT.5 and STND.DFLT.20 add a citation "
        "and a list. No provision asks a decision of the human owner beyond those LVL0 assigns (STND.DRAFT.42): the "
        "confirmation of a foreign entry is the act by which the owner gives an entry authority, asked once per "
        "entry and gathered into one referral. Onset: none; every provision of this standard is binding and carries "
        "no field onset. " + TRANSITION + "A foreign entry already relied upon before this revision is entered is "
        "confirmed at the next action that relies on it, and an authorization given directly before it and not yet "
        "entered is entered before that action; a ledger that predates this revision has no acceptance entry, so its "
        "entries of acts of the human owner are confirmed once, in one statement, when a line of work first relies "
        "on one. " +
        cite("S4, S5, S6, B1, B3, B4, O7, I1, and I9",
             "recommendations R1, R3, R4, and R10") + F.AUTHOR)
    F.finish(root, "STND/DFLT", "STND.DFLT", "1.6.1", "1.7", row, rationale, at)


# ------------------------------------------------------------------------------------------------------------ AGENT


def apply_agent(root: Path, at: str) -> None:
    date = at[:10]
    F.set_body(root, "AGENT/6.md", P.AGENT6, instantiates=["GUARD.14", "PRIME.8"])
    replace_text(root, "AGENT/_doc.md", P.AGENT_DOC)
    F.check_fields(root, ["AGENT.6"], binding=True)
    row = f"| 1.4 | {date} | Minor amendment (GOV.41): {P.AGENT_READING}. |"
    rationale = (
        f"Minor amendment of AGENT, revision 1.4, ratified by the custodian on {date}: {P.AGENT_READING}. Reading: "
        f"under {LVL0}, where neither a spending limit nor a fixed cost bounds an agent's own operating cost, PRIME.8 "
        "authorizes it only where it is measurable and up to an estimate that the agent states before the work "
        "begins; AGENT.6 is the provision that has the agent state an effort estimate, so it now asks for it before "
        "the unit begins in that case even under a discipline of the human owner, and AGENT.8 is unchanged, since "
        "its report of an excess stays true and PRIME.8 itself holds the halt before the estimate. Class: minor "
        "under STND.IDENT.3, because AGENT.6 adds an occasion of its obligation without altering the motivation or "
        "intent of the governance. Floor (GOV.11): AGENT.6 binds at every class, as before, since it instantiates "
        "GUARD.14 and now PRIME.8, which gives it rank 0; it asks only the estimate without which PRIME.8 "
        "authorizes no cost in that case, at the cost of one statement in the plan, so it raises no floor and asks "
        "no decision of the human owner (STND.DRAFT.42). Onset: none; AGENT.6 is non-waivable and carries no field "
        "onset. " + TRANSITION + cite("S5 and B1", "recommendation R1") + F.AUTHOR)
    F.finish(root, "AGENT", "AGENT", "1.3.2", "1.4", row, rationale, at)


# ------------------------------------------------------------------------------------------------------- STND.CLASS


def apply_class(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/CLASS/10.md", P.CLASS10)
    F.set_body(root, "STND/CLASS/20.md", P.CLASS20_BODY, refers_to=["QA.11", "GOV.13", "STND.DFLT.33"])
    replace_text(root, "STND/CLASS/22.md", P.CLASS22)
    replace_text(root, "STND/CLASS/_doc.md", P.CLASS_DOC)
    F.check_fields(root, ["STND.CLASS.20", "STND.CLASS.22"], binding=True)
    F.check_fields(root, ["STND.CLASS.10"])
    reading = P.CLASS_READING.format(lvl0=LVL0)
    row = f"| 1.6 | {date} | Minor amendment (GOV.41): {reading}. |"
    rationale = (
        f"Minor amendment of STND.CLASS, revision 1.6, ratified by the custodian on {date}: {reading}. Reading: "
        f"GOV.48 as {LVL0} reads holds agents to INTPR.11 at the level that GOV.10 and GOV.11 set, so the clause of "
        "STND.CLASS.10 that GOV.48 covers agent actions at every class is untrue; of the two readings, the one "
        "drafted applies INTPR.11 to agent actions from CSQ3, under the first sentence of STND.CLASS.10, and not "
        "from CSQ1, since it keeps more evidence and moves agent actions only out of CSQ4; once work under the "
        "defaults is assured, STND.DFLT.23 accepts only signed entries, which STND.CLASS.22 now makes a step before "
        "reliance at the new class; under QA.11 as amended, the human owner's direction, not a classification, "
        "promotes the results of work whose class GOV.13 presumes, so STND.CLASS.20 has the promotion cite the "
        "entry of that direction, which STND.DFLT.33 makes, and is otherwise unchanged. Class: minor under STND.IDENT.3, because the reach of a part and a step of a "
        "binding provision change, without altering the motivation or intent of the governance. Floor (GOV.11): "
        "STND.CLASS.10 is a default, and its row conforms to the level that LVL0 now gives INTPR.11 for agents, "
        "which is above the floor; STND.CLASS.22 binds at every class and its new step reaches only work made "
        "assured at CSQ1 or CSQ0, where STND.DFLT.23 already bars reliance on an unsigned entry, so it names the act "
        "that already precedes that reliance and raises no floor; STND.CLASS.20 binds at every class, as "
        "before, since it instantiates GOV.11, and asks for presumed work the citation of an entry that exists, "
        "where before it asked one that could not exist. Onset: STND.CLASS.10 keeps the value null, since "
        "it applies at every class, and STND.CLASS.22 is binding and carries no field. " + TRANSITION +
        cite("O1, O7, and I5", "recommendation R5") + F.AUTHOR)
    F.finish(root, "STND/CLASS", "STND.CLASS", "1.5.1", "1.6", row, rationale, at)


# ------------------------------------------------------------------------------------------------------- STND.IDENT


def apply_ident(root: Path, at: str) -> None:
    date = at[:10]
    F.set_body(root, "STND/IDENT/23.md", P.IDENT23, instantiates=["GOV.41", "GOV.37"])
    replace_text(root, "STND/IDENT/_doc.md", P.IDENT_DOC)
    F.check_fields(root, ["STND.IDENT.23"], binding=True)
    row = f"| 1.6 | {date} | Minor amendment (GOV.41): {P.IDENT_READING}. |"
    rationale = (
        f"Minor amendment of STND.IDENT, revision 1.6, ratified by the custodian on {date}: {P.IDENT_READING}. "
        "Reading: GOV.41 has a project's human owner adopt that project's LVL3 instruments, and GOV.37 has mnemonics "
        "held in a register that changes only by ledger transaction; a project's ledger transaction meets GOV.37 "
        "for the project's own mnemonic, so a downstream project names itself, and is able to have the "
        "constitution that GOV.20 asks, without an act of the custodians that LVL0 does not assign them; the duty "
        "arises only where the project adopts an instrument whose identifier carries its mnemonic, and the Notes fix "
        "the transaction as one of type register, with the mnemonic as its one target, so that a harness given the "
        "project's ledger reads it; the register MNEM, and the check v.11 that only the custodians change it, stay as they are. Class: minor under "
        "STND.IDENT.3, because an obligation moves from the custodians to the human owner for one kind of mnemonic, "
        "without altering the motivation or intent of the governance. Floor (GOV.11): STND.IDENT.23 binds at every "
        "class, as before, since it instantiates GOV.41 and GOV.37; the human owner's act replaces the custodians' "
        "for the project's own mnemonic, at the cost of one ledger transaction, and the mnemonic is one that MNEM "
        "does not hold, so that no identifier of the corpus is shadowed; it asks of the owner only an act of GOV.41 "
        "(STND.DRAFT.42). Onset: none; the provision is binding. Transition (GOV.42): none; a project whose "
        "mnemonic the custodians registered keeps it. " + cite("B7", "recommendation R6") + F.AUTHOR)
    F.finish(root, "STND/IDENT", "STND.IDENT", "1.5", "1.6", row, rationale, at)


# ------------------------------------------------------------------------------------------------------- STND.WPROC


def apply_wproc(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/WPROC/_doc.md", P.WPROC_DOC)
    row = f"| 1.5 | {date} | Minor amendment (GOV.41): {P.WPROC_READING}. |"
    rationale = (
        f"Minor amendment of STND.WPROC, revision 1.5, ratified by the custodian on {date}: {P.WPROC_READING}. "
        "Reading: in a fresh project no record says whether the default branch is a branch from which the work is "
        "released or deployed, and GUARD.2 then puts each advance of it in the highest tier, so that every fix ends "
        "with a decision of the human owner; the term now settles that the default branch is no main line until "
        "the human owner records it as one. Class: minor under STND.IDENT.3, because a defined meaning changes "
        "without altering the motivation or intent of the governance. Floor (GOV.11): STND.WPROC.12 binds at every "
        "class and is unchanged; the term narrows the branches it reaches, and no condition that PRIME or GUARD "
        "prohibits becomes reachable, since a release stays the human owner's act (QA.10, GOV.20), a push that "
        "publishes or deploys stays an irrevocable remote write that GUARD.11 authorizes only per action, a merge "
        "into the default branch is a local and reversible change that preserves history (GUARD.5, STND.WPROC.8), "
        "and a branch from which the work is in fact released, other than the default branch, stays a main line. "
        "Onset: none; no provision changes. Transition (GOV.42): none; a project that treats its default branch as "
        "a main line records it as one, by the human owner's act. " + cite("B9") + F.AUTHOR)
    F.finish(root, "STND/WPROC", "STND.WPROC", "1.4", "1.5", row, rationale, at)


# -------------------------------------------------------------------------------------------------------- STND.CREW


def apply_crew(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/CREW/13.md", P.CREW13)
    replace_text(root, "STND/CREW/21.md", P.CREW21)
    replace_text(root, "STND/CREW/_doc.md", P.CREW_DOC)
    F.check_fields(root, ["STND.CREW.13", "STND.CREW.21"], binding=True)
    reading = P.CREW_READING.format(lvl0=LVL0)
    row = f"| 1.4 | {date} | Minor amendment (GOV.41): {reading}. |"
    rationale = (
        f"Minor amendment of STND.CREW, revision 1.4, ratified by the custodian on {date}: {reading}. Reading: "
        f"under {LVL0} a unit of work may have no authorized estimate and no operating envelope, its cost bounded "
        "instead by another spending limit, by a cost that provisioning fixes, or by the estimate that the agent "
        "states before the work begins (PRIME.8), so STND.CREW.13 and the Notes name the bounds of PRIME.8; "
        "PRIME.11 lets a person whom the human owner names instruct within the scope named, so the term Lead agent "
        "reaches an agent that such a person instructs directly. Class: minor under STND.IDENT.3, because the "
        "content of a record and a defined meaning change, without altering the motivation or intent of the "
        "governance. Floor (GOV.11): STND.CREW.13 binds at every class, as before, since it instantiates GUARD.14 "
        "and GUARD.15, and it asks the same one record, against the bounds that PRIME.8 now sets; STND.CREW.21 "
        "binds at every class, as before, and asks the same referral where an assignment would pass the bound of "
        "PRIME.8, whatever kind of bound it is; the term Lead "
        "agent gives a named person no act of PRIME.1, since the record of decisions still goes to the human owner "
        "(STND.CREW.2). Onset: none; STND.CREW.13 is binding, and no default changes. " + TRANSITION +
        cite("S5, B1, and S6", "recommendations R1 and R3") + F.AUTHOR)
    F.finish(root, "STND/CREW", "STND.CREW", "1.3", "1.4", row, rationale, at)


# -------------------------------------------------------------------------------------------------------- STND.PROJ


def apply_proj(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/PROJ/1.md", P.PROJ1)
    replace_text(root, "STND/PROJ/2.md", P.PROJ2)
    replace_text(root, "STND/PROJ/3.md", P.PROJ3)
    replace_text(root, "STND/PROJ/_doc.md", P.PROJ_DOC)
    F.check_fields(root, ["STND.PROJ.1", "STND.PROJ.2", "STND.PROJ.3"], binding=True)
    row = f"| 1.6 | {date} | Minor amendment (GOV.41): {P.PROJ_READING}. |"
    rationale = (
        f"Minor amendment of STND.PROJ, revision 1.6, ratified by the custodian on {date}: {P.PROJ_READING}. "
        "Reading: a constitution that cited STND.DFLT took in STND.DFLT.35 but not STND.DFLT.34, and none of the "
        "authorization provisions, so that, once STND.DFLT.1 ended the defaults, a project that adopted a "
        "constitution lost the build and test permission, the route by which the human owner's acts reach the "
        "ledger, and the entry of directions of work; the citation now carries them, with the rule of "
        "accepted entries and the acceptance entries that STND.DFLT.17 rests on, the identification of the human "
        "owner, and the record of isolation; STND.PROJ.3 proposes the standing authorization of signing that the "
        "term Working bounds of STND.DFLT reads, so that the first referral proposes it; the row Physical hardware "
        "of STND.PROJ.1 takes the words of PRIME.13, as GOV.20 now does. Class: minor under "
        "STND.IDENT.3, because a permission widens without altering the motivation or intent of the governance. "
        "Floor (GOV.11): STND.PROJ.2 binds at every class, as before, since it instantiates GOV.21 and GOV.22; it "
        "widens only what one citation adopts, each provision adopted keeps its own content, and the items that "
        "STND.DFLT does not provide are still stated in full, so no obligation is lowered and none is raised; "
        "STND.PROJ.3 adds a recommendation within a binding provision, which the human owner adopts or not, and the "
        "row of STND.PROJ.1 reaches the hardware that PRIME.13 already governs at every class. "
        "Onset: none; the provisions are binding. Transition (GOV.42): none; a constitution that already states "
        "its sections Identity, Records, and Authorizations in full keeps them. " + cite("O5") + F.AUTHOR)
    F.finish(root, "STND/PROJ", "STND.PROJ", "1.5", "1.6", row, rationale, at)


# ------------------------------------------------------------------------------------------------------- STND.INSTR


def apply_instr(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/INSTR/11.md", P.INSTR11)
    replace_text(root, "STND/INSTR/_doc.md", P.INSTR_DOC)
    F.check_fields(root, ["STND.INSTR.11"], binding=True)
    row = f"| 1.6 | {date} | Minor amendment (GOV.41): {P.INSTR_READING}. |"
    rationale = (
        f"Minor amendment of STND.INSTR, revision 1.6, ratified by the custodian on {date}: {P.INSTR_READING}. "
        "Reading: PRIME.11 denies content instruction authority, and the adoption of STND.INSTR.11 exists so that "
        "content gains no authority; refraining from an action that nothing directs or requires uses no authority, "
        "so only a grant needs adoption, and the human owner's own restriction in an unadopted file has weight "
        "without an entry at each edit. Class: minor under STND.IDENT.3, because a permission is added without "
        "altering the motivation or intent of the governance. Floor (GOV.11): STND.INSTR.11 binds at every class, "
        "as before; the permission reaches only an action that no instruction with authority directs and no "
        "provision of governance requires, and never the command toward the designed safe state or a step of "
        "GUARD.3, so no obligation is lowered and no halt is kept from a safe state, an injected restriction gains no authority "
        "to make the agent act, and each restriction honored is stated in the completion report, where the human "
        "owner sees it. Onset: none; the provision is binding. Transition (GOV.42): none. " + cite("O6") + F.AUTHOR)
    F.finish(root, "STND/INSTR", "STND.INSTR", "1.5.1", "1.6", row, rationale, at)


STEPS = [apply_dflt, apply_agent, apply_class, apply_ident, apply_wproc, apply_crew, apply_proj, apply_instr]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, step in enumerate(STEPS):
        step(root, (start + timedelta(seconds=k)).isoformat())
