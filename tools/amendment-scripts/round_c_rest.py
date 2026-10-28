"""Round c of 2026-10-28, part 2: the standards and profiles that cite the new STND.CLASS provisions, and the human
round trips of register entries R2.2, R2.5, R2.6, and R2.7.

STND.CODE (ruling C2, the onset of STND.CODE.20); HW and its six sub-profiles (C2, C8, CS9); NUMER (C8); STND.CONC
(C2); AGENT (R2.2, CC19); STND.CREW (CP11, CP14, CP20, R7.3); STND.THRT (CC22); STND.WPROC (CP16); and the Notes of
STND.JL, STND.PY, STND.RUST, and STND.STDC (C3).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402
from round_c_class import RECORD, RULINGS  # noqa: E402

# ----------------------------------------------------------------------------------------------------------------
# STND.CODE 1.5
# ----------------------------------------------------------------------------------------------------------------

CODE20 = [
    ("Each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the "
     "deviation procedure of that standard requires, at its location under one marker that the repository "
     "configuration names or in a decision record that the location cites, with the identifier of the rule, the "
     "reason, and the evidence that the code stays correct (REPRO.7).",
     "For work of CSQ1 or CSQ0, each deviation from a rule of the high-assurance coding standard of STND.CODE.17 "
     "SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that "
     "the repository configuration names or in a decision record that the location cites, with the identifier of "
     "the rule, the reason, and the evidence that the code stays correct (REPRO.7). Other work that adopts such a "
     "standard SHOULD mark each deviation at its location under that marker (REPRO.7)."),
]

CODE_DOC = [
    ("STND.CODE.20 asks the record of each deviation wherever such a standard is adopted (REPRO.7).",
     "STND.CODE.20 asks the record of each deviation of work of CSQ1 or CSQ0, and the marker alone of other work "
     "that adopts such a standard (REPRO.7). Where the classification records an expected class of CSQ1 or CSQ0, "
     "STND.CLASS.21 has the design not preclude the subset, the edition, the failure channel, and the dependencies "
     "that STND.CODE.17, STND.CODE.19, and STND.DEPS.1 ask at that class, with the reason for each such choice in a "
     "decision record, and asks no other record of that class before the reclassification than the records of "
     "STND.CLASS.23; the marker of STND.CODE.20 is the one thing of this standard kept earlier, so that the "
     "reclassification finds each deviation by a search and the record that STND.CLASS.22 then owes is written "
     "once."),
    ("These onsets depart from STND.CLASS.10. STND.CODE.17 and STND.CODE.19 apply from CSQ1, earlier than the CSQ0 "
     "rows of DSGN.3 and VV.1 that they tighten, and STND.CODE.20 applies wherever a high-assurance coding standard "
     "is adopted, CSQ4 included, though STND.CLASS.10 lets work of CSQ4 omit an obligation above the floor. The "
     "custodian ratified these onsets for C++ with the provisions on high-assurance code that STND.CXX 1.1 held and "
     "that STND.CODE.17, STND.CODE.19, and STND.CODE.20 now state, and for C through STND.STDC.1.",
     "These onsets depart from STND.CLASS.10. STND.CODE.17 and STND.CODE.19 apply from CSQ1, earlier than the CSQ0 "
     "rows of DSGN.3 and VV.1 that they tighten; the record of STND.CODE.20 applies from CSQ1 with them, and its "
     "marker alone applies wherever a high-assurance coding standard is adopted, CSQ4 included. The custodian "
     "ratified the onsets of STND.CODE.17 and STND.CODE.19 for C++ with the provisions on high-assurance code that "
     "STND.CXX 1.1 held, and for C through STND.STDC.1; the record of STND.CODE.20 was ratified then as applying "
     "wherever such a standard is adopted, and revision 1.5 moves it to CSQ1 under the custodian's ruling of "
     "2026-10-28 on design for the expected class, which minimizes what is owed before a reclassification."),
    ("and the record of STND.CODE.20 reaches work of CSQ4 only where that work has chosen to adopt a high-assurance "
     "coding standard, at the cost of one record for each deviation from it.",
     "and the marker of STND.CODE.20 reaches work of CSQ4 only where that work has chosen to adopt a high-assurance "
     "coding standard, at the cost of one marker for each deviation from it."),
]

CODE_READING = (
    "the deviation record of STND.CODE.20 applies to work of CSQ1 or CSQ0, and other work that adopts a "
    "high-assurance coding standard marks each deviation at its location under the marker alone; the Notes cite "
    "STND.CLASS.21 for the design of work with a recorded expected class")
CODE_ROW = f"| 1.5 | {F.DATE} | Minor amendment (GOV.41): {CODE_READING}. |"
CODE_RATIONALE = (
    f"Minor amendment of STND.CODE, revision 1.5, ratified by the custodian on {F.DATE}: {CODE_READING}. The change "
    "is minor under STND.IDENT.3 because it narrows a default and adds a recommendation, without altering the "
    "motivation or intent of the governance. No floor is raised (GOV.11): the record is owed later than before, and "
    "the marker is one token at each deviation. Class onset: the record of STND.CODE.20 from CSQ1, with "
    "STND.CODE.17 and STND.CODE.19; the marker wherever such a standard is adopted, as the record was. This revisits "
    "the onset that the custodian ratified for C++ with STND.CXX 1.1 and for C with STND.STDC.1, under ruling C2. "
    "Transition (GOV.42): a deviation recorded before this revision keeps its record. Ruling C2 of "
    f"{RULINGS}; entry R3.2 of the register, with CL21 and CL26; {RECORD}." + F.AUTHOR)


def apply_code(root: Path, at: str) -> None:
    replace_text(root, "STND/CODE/20.md", CODE20)
    replace_text(root, "STND/CODE/_doc.md", CODE_DOC)
    F.finish(root, "STND/CODE", "STND.CODE", "1.4", "1.5", CODE_ROW, CODE_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# HW 1.2
# ----------------------------------------------------------------------------------------------------------------

ATTRIBUTES = [
    "General-purpose processor execution", "Accelerator execution", "Quantum processor execution",
    "Embedded controller execution", "Programmable logic execution", "Integrated circuit execution",
]
TYPES = {
    "General-purpose processor execution": "a general-purpose processor",
    "Accelerator execution": "an accelerator",
    "Quantum processor execution": "a quantum processor",
    "Embedded controller execution": "an embedded controller",
    "Programmable logic execution": "programmable logic",
    "Integrated circuit execution": "an integrated circuit",
}


def attribute_row(name: str) -> str:
    return (f"| {name} | An attribute, true when the classification records that a component of the work whose "
            f"behavior affects a result the work reports or relies on executes, or is admitted to execute, on "
            f"{TYPES[name]}. |\n")


OPERATOR = "to the operator of a run during which one acts and otherwise in the record of the run"

HW1 = [
    ("\n".join(f"| {name} | HW |" for name in ATTRIBUTES), "| Hardware execution | HW |"),
]

HW19 = [
    ("the path SHALL report the fallback to the operator at its first occurrence in the run (INTPR.7).",
     f"the path SHALL report the fallback at its first occurrence in the run, {OPERATOR} (INTPR.7)."),
]

HW21 = [
    ("and report each overrun to the operator (RSRC.2, RSRC.3, INTPR.7).",
     f"and report each overrun {OPERATOR} (RSRC.2, RSRC.3, INTPR.7)."),
]

HW_DOC = [
    ('selector: "Binds when a component of the work executes, or is admitted to execute, on a hardware type that '
     'HW.1 names (HW.1)."',
     'selector: "Binds when a component of the work executes, or is admitted to execute, on a hardware type (HW.1)."'),
] + [(attribute_row(name), "") for name in ATTRIBUTES] + [
    ("| Hardware contract | The contract of an execution path:",
     "| Hardware execution | An attribute, true when the classification records that a component of the work whose "
     "behavior affects a result the work reports or relies on executes, or is admitted to execute, on a hardware "
     "type. |\n"
     "| Hardware contract | The contract of an execution path:"),
    ("| Hardware type | One of the kinds of execution hardware for which the selector table of HW.1 gives an "
     "attribute. |",
     "| Hardware type | One of the kinds of execution hardware for which this profile holds a sub-profile: "
     "general-purpose processors, accelerators, quantum processors, embedded controllers, programmable logic, and "
     "integrated circuits. |"),
    ("HW.1 states the selector: one attribute per hardware type, each defined here, which the sub-profiles each "
     "give one of (HW.CPU.1, HW.GPU.1, HW.QPU.1, HW.EMBED.1, HW.FPGA.1, HW.ASIC.1, STND.DRAFT.36).",
     "HW.1 states the selector: one attribute, Hardware execution, defined here, which the selector of each "
     "sub-profile gives as well (HW.CPU.1, HW.GPU.1, HW.QPU.1, HW.EMBED.1, HW.FPGA.1, HW.ASIC.1, STND.DRAFT.36), so "
     "that the hardware types on which the work executes are a matter of its execution paths and not of an "
     "attribute each, and path scope alone decides which sub-profile's provisions reach a component."),
    ("Each attribute is also true where the classification records that a component whose behavior affects a "
     "result the work reports or relies on is admitted to execute on that type. Adding a hardware type otherwise "
     "revises the classification, which the human owner adopts (GOV.24, GOV.50); a classification that admits the "
     "hardware types the work plans to use lets an agent add a path on an admitted type without a further decision "
     "of the human owner, and costs nothing before the path exists.",
     "The attribute is also true where the classification records that such a component is admitted to execute on "
     "a hardware type. No selector tests the type, so a path on a new hardware type revises no attribute; the "
     "execution paths that the Classification section lists by hardware type (STND.PROJ.1) are the record that a "
     "new path changes, and a classification that admits the hardware types the work plans to use lets an agent "
     "add a path on an admitted type without a further decision of the human owner, and costs nothing before the "
     "path exists."),
    ("Each sub-profile's selector restates its attribute from HW.1.",
     "Each sub-profile's selector gives the attribute of HW.1."),
    ("Hardware of a kind that no attribute names is governed by LVL0",
     "Hardware of a kind that Hardware type does not name is governed by LVL0"),
    ("Both reports therefore tighten above the class at which INTPR.7 applies, at the cost of one message each.",
     "Both reports therefore tighten above the class at which INTPR.7 applies, at the cost of one message each; "
     "each goes to the operator of a run during which one acts, and otherwise into the record of the run, since an "
     "unattended run has no operator to receive a message and its record is what a reader examines afterward. "
     "Where the classification records an expected class, STND.CLASS.21 has the design not preclude the hardware, "
     "the reference path (HW.15), the reduction order, and the bounds (HW.20) that the obligations of that class "
     "ask of the work, with the reason for each such choice in a decision record, and asks no other record of that "
     "class before the reclassification than the records of STND.CLASS.23."),
]

HW_READING = (
    "HW.1 gives one attribute, Hardware execution, which the Terms define and the selector of each sub-profile gives "
    "as well, in place of one attribute per hardware type, and Hardware type names the kinds for which the profile "
    "holds a sub-profile (CS9); HW.19 and HW.21 report to the operator of a run during which one acts and otherwise "
    "in the record of the run (CS8); the Notes cite STND.CLASS.21 for the design of work with a recorded expected "
    "class")
HW_ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {HW_READING}. |"
HW_RATIONALE = (
    f"Minor amendment of HW, revision 1.2, ratified by the custodian on {F.DATE}: {HW_READING}. The change is minor "
    "under STND.IDENT.3 because it alters the selector, two obligations, and two defined meanings, without altering "
    "the motivation or intent of the governance. No floor is raised (GOV.11): the profile binds where it bound, "
    "since a component that executes on hardware of one of the six types made one of the six attributes true, and "
    "a provision about an execution path on one type still imposes nothing on a component with no path on that "
    "type; a report into the record of a run asks less of an unattended run than a message no one receives, and "
    "INTPR.7 is met by the record where no operator acts. Class onsets: unchanged. Transition (GOV.42): a "
    "classification adopted before this revision that makes one of the six attributes true makes Hardware "
    "execution true. Ruling C8 (CS8) of "
    f"{RULINGS}, and entry R2.5 (CS9) of the register under ruling F1; {RECORD}." + F.AUTHOR)


def apply_hw(root: Path, at: str) -> None:
    replace_text(root, "HW/1.md", HW1)
    replace_text(root, "HW/19.md", HW19)
    replace_text(root, "HW/21.md", HW21)
    replace_text(root, "HW/_doc.md", HW_DOC)
    F.finish(root, "HW", "HW", "1.1.2", "1.2", HW_ROW, HW_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# The six sub-profiles: HW.CPU 1.1, HW.GPU 1.1, HW.QPU 1.1, HW.EMBED 1.1, HW.FPGA 1.1, HW.ASIC 1.1
# ----------------------------------------------------------------------------------------------------------------

SUBPROFILES = [
    # folder, attribute, old selector field, plural type, old revision
    ("CPU", "General-purpose processor execution",
     "Binds when a component of the work executes, or is admitted to execute, on a general-purpose processor "
     "(HW.CPU.1).", "general-purpose processors", "1.0.1"),
    ("GPU", "Accelerator execution",
     "Binds when a component of the work executes, or is admitted to execute, on an accelerator (HW.GPU.1).",
     "accelerators", "1.0.2"),
    ("QPU", "Quantum processor execution",
     "Binds when a component of the work executes, or is admitted to execute, on a quantum processor (HW.QPU.1).",
     "quantum processors", "1.0.2"),
    ("EMBED", "Embedded controller execution",
     "Binds when a component of the work executes, or is admitted to execute, on an embedded controller "
     "(HW.EMBED.1).", "embedded controllers", "1.0.2"),
    ("FPGA", "Programmable logic execution",
     "Binds when the work executes on programmable logic (HW.FPGA.1).", "programmable logic", "1.0.1"),
    ("ASIC", "Integrated circuit execution",
     "Binds when the work executes on integrated circuits (HW.ASIC.1).", "integrated circuits", "1.0"),
]

CPU5 = [
    ("the path SHALL report the excess to the operator at its first occurrence in the run (INTPR.7, RSRC.2).",
     f"the path SHALL report the excess at its first occurrence in the run, {OPERATOR} (INTPR.7, RSRC.2)."),
]

CPU_DOC = [
    ("HW.CPU.5 reports oversubscription when it first occurs, in every run, because the report costs one message.",
     "HW.CPU.5 reports oversubscription when it first occurs, in every run, because the report costs one message; "
     "it goes to the operator of a run during which one acts, and otherwise into the record of the run."),
]


def subprofile_reading(folder: str, plural: str) -> str:
    return (f"the selector of HW.{folder}.1 gives the attribute Hardware execution of HW.1 in place of its own, so "
            f"that path scope alone decides which provisions reach a component, each provision naming an execution "
            f"path on {plural} as its subject (CS9)")


def apply_subprofile(root: Path, folder: str, attribute: str, old_selector: str, plural: str, old_rev: str,
                     at: str) -> None:
    doc_id = f"HW.{folder}"
    replace_text(root, f"HW/{folder}/1.md", [(f"| {attribute} | HW |", "| Hardware execution | HW |")])
    new_selector = (f"Binds with HW, when a component of the work executes, or is admitted to execute, on a hardware "
                    f"type ({doc_id}.1); its provisions name execution paths on {plural}.")
    replace_text(root, f"HW/{folder}/_doc.md", [
        (f'selector: "{old_selector}"', f'selector: "{new_selector}"'),
        (f"{doc_id}.1 states the selector: the attribute {attribute}, which HW defines and which HW.1 also gives "
         "(STND.DRAFT.36).",
         f"{doc_id}.1 states the selector: the attribute Hardware execution, which HW defines and which HW.1 gives "
         "(STND.DRAFT.36), so that the sub-profile binds with HW and its provisions reach a component through the "
         "execution paths that the classification lists."),
    ])
    stale = {
        "FPGA": ("so HW.EMBED does not bind its firmware (HW.EMBED.1).",
                 "so no provision of HW.EMBED reaches its firmware (HW.EMBED.1)."),
        "ASIC": ("is not an integrated circuit under HW, and this sub-profile does not bind it.",
                 "is not an integrated circuit under HW, and no provision of this sub-profile reaches it."),
    }
    if folder in stale:
        replace_text(root, f"HW/{folder}/_doc.md", [stale[folder]])
    reading = subprofile_reading(folder, plural)
    if folder == "CPU":
        replace_text(root, "HW/CPU/5.md", CPU5)
        replace_text(root, "HW/CPU/_doc.md", CPU_DOC)
        reading += ("; HW.CPU.5 reports to the operator of a run during which one acts and otherwise in the record "
                    "of the run (CS8)")
    row = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {reading}. |"
    rationale = (
        f"Minor amendment of {doc_id}, revision 1.1, ratified by the custodian on {F.DATE}: {reading}. The change is "
        "minor under STND.IDENT.3 because it alters the selector, without altering the motivation or intent of the "
        "governance. No floor is raised (GOV.11): the sub-profile binds with HW, as GOV.27 has it inherit HW in "
        "full, and each of its provisions names an execution path on its hardware type as its subject "
        "(STND.DRAFT.38), so it imposes nothing on a component with no such path, which is what the attribute of "
        "its own decided before. Class onsets: unchanged. Transition (GOV.42): none. Entry R2.5 (CS9) of the "
        f"register under ruling F1 of {RULINGS}"
        + ("; ruling C8 (CS8)" if folder == "CPU" else "") + f"; {RECORD}." + F.AUTHOR)
    # The pin of HW covers its sub-profiles, so a sub-profile's transaction pins the whole HW tree, as the earlier
    # sub-profile amendments did.
    raise_revision(root, f"HW/{folder}", old_rev, "1.1", row)
    B.write_references(root, [doc_id])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.41"], targets=[doc_id], scope=["HW"],
                                          rationale=rationale))
    print("seq", rec.entry["seq"], doc_id, "1.1")


def subprofile_steps():
    def make(args):
        return lambda root, at: apply_subprofile(root, *args, at)
    return [make(args) for args in SUBPROFILES]


# ----------------------------------------------------------------------------------------------------------------
# NUMER 1.4
# ----------------------------------------------------------------------------------------------------------------

NUMER18 = [
    ("the departure SHALL be reported to the operator during the run (INTPR.10, INTPR.7).",
     f"the departure SHALL be reported during the run, {OPERATOR} (INTPR.10, INTPR.7)."),
]

NUMER_DOC = [
    ("NUMER.26 states how PRIME.2 applies to stochastic comparisons and binds at every class, adding nothing to the "
     "floor that PRIME.2 does not already hold.",
     "NUMER.26 states how PRIME.2 applies to stochastic comparisons and binds at every class, adding nothing to the "
     "floor that PRIME.2 does not already hold. NUMER.18 reports a departure from the domain of validity during the "
     "run to the operator of a run during which one acts, and otherwise in the record of the run, since an "
     "unattended run has no operator to receive a message and its record is what a reader examines afterward "
     "(INTPR.7)."),
]

NUMER_READING = (
    "NUMER.18 reports a departure from the domain of validity to the operator of a run during which one acts and "
    "otherwise in the record of the run (CS8)")
NUMER_ROW = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {NUMER_READING}. |"
NUMER_RATIONALE = (
    f"Minor amendment of NUMER, revision 1.4, ratified by the custodian on {F.DATE}: {NUMER_READING}. The change is "
    "minor under STND.IDENT.3 because it alters an obligation, without altering the motivation or intent of the "
    "governance. No floor is raised (GOV.11): a report into the record of a run asks less of an unattended run than "
    "a message no one receives, and INTPR.7 is met by the record where no operator acts. Class onset: unchanged. "
    f"Transition (GOV.42): none. Ruling C8 (CS8) of {RULINGS}; entry R2.6 of the register; {RECORD}." + F.AUTHOR)


def apply_numer(root: Path, at: str) -> None:
    replace_text(root, "NUMER/18.md", NUMER18)
    replace_text(root, "NUMER/_doc.md", NUMER_DOC)
    F.finish(root, "NUMER", "NUMER", "1.3", "1.4", NUMER_ROW, NUMER_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# STND.CONC 1.1.2
# ----------------------------------------------------------------------------------------------------------------

CONC_DOC = [
    ("The sentences of each provision with three modals share one onset, so that the provision applies as one "
     "bundle. No default raises the floor (GOV.11).",
     "The sentences of each provision with three modals share one onset, so that the provision applies as one "
     "bundle. No default raises the floor (GOV.11). Where the classification records an expected class at which an "
     "acceptance criterion asks bitwise identity across numbers of tasks, STND.CLASS.21 has the design not preclude "
     "the fixed-order or order-independent combination of STND.CONC.22, with the reason for the choice in a "
     "decision record, and asks no other record of that class before the reclassification than the records of "
     "STND.CLASS.23."),
]

CONC_READING = (
    "the Notes cite STND.CLASS.21 for the design of work with a recorded expected class, on the combination order "
    "of STND.CONC.22")
CONC_ROW = (f"| 1.1.2 | {F.DATE} | Editorial amendment (GOV.41): {CONC_READING}; no obligation, permission, or "
            "defined meaning changes. |")
CONC_RATIONALE = (
    f"Editorial amendment of STND.CONC, revision 1.1.2, ratified by the custodian on {F.DATE}: {CONC_READING}. The "
    "change is editorial under STND.IDENT.3 because no obligation, permission, or defined meaning of this document "
    f"changes. Transition (GOV.42): none. Ruling C2 of {RULINGS}; entry R3.2 of the register, with CS12; {RECORD}."
    + F.AUTHOR)


def apply_conc(root: Path, at: str) -> None:
    replace_text(root, "STND/CONC/_doc.md", CONC_DOC)
    F.finish(root, "STND/CONC", "STND.CONC", "1.1.1", "1.1.2", CONC_ROW, CONC_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# AGENT 1.3
# ----------------------------------------------------------------------------------------------------------------

AGENT39 = [
    ("and, from a measured baseline or a recorded decision of the human owner, that running the units together",
     "and, from a measured baseline, an effort estimate under AGENT.6 that states its basis, or a recorded decision "
     "of the human owner, that running the units together"),
    ('refers_to: ["QA.2"]', 'refers_to: ["QA.2", "AGENT.6"]'),
]

AGENT23 = [
    ("Where the provisioned environment records a network access with these items in a record that the agent is "
     "unable to alter, an agent MAY cite that record in place of its own (REPRO.11).",
     "Where the provisioned environment records a network access with these items in a record that the agent is "
     "unable to alter, or a transcript of its session that the agent did not edit shows the access, with each of "
     "these items that the transcript lacks stated once for the session or beside the access, an agent MAY cite "
     "that record or transcript in place of its own (REPRO.11)."),
]

AGENT_DOC = [
    ("AGENT.23 records each attempt, refused ones included; the vocabulary of access descriptors belongs to the "
     "defaults standard or a project instrument.",
     "AGENT.23 records each attempt, refused ones included; the vocabulary of access descriptors belongs to the "
     "defaults standard or a project instrument. A transcript of the session that the agent did not edit, as a "
     "tool of the agent keeps one, shows each access with its address, its time, and the direction of transfer, "
     "and the items it lacks, the authorization relied on and the access descriptor among them, are stated once "
     "where they hold for every access of the session, and beside the access otherwise, so that an agent at CSQ3 "
     "writes no seven-item record before each next step."),
    ("AGENT.39 and AGENT.40 make parallel work safe and efficient: an assessment before it begins, and units "
     "started on a shared machine as soon as, and only while, it is able to serve them.",
     "AGENT.39 and AGENT.40 make parallel work safe and efficient: an assessment before it begins, and units "
     "started on a shared machine as soon as, and only while, it is able to serve them. The first parallel "
     "delegation of a project has no measured baseline, so AGENT.39 accepts an effort estimate under AGENT.6 that "
     "states its basis, which the agent roles standard grounds in the records of comparable units or in stated "
     "reasoning, and asks no decision of the human owner for it."),
    ("a reading resting on GOV.9 and GOV.17 and recorded as a judgment (PRIN.10) until the custodians interpret "
     "GOV.11 for such provisions.",
     "a reading resting on GOV.9 and GOV.17 and recorded as a judgment (PRIN.10) until the custodians interpret "
     "GOV.11 for such provisions; for AGENT.39 the question no longer affects the burden, since an effort estimate "
     "that states its basis is a basis the agent itself supplies at every class, so that the provision binding at "
     "every class asks no measured baseline and no decision of the human owner."),
]

AGENT_READING = (
    "AGENT.39 accepts an effort estimate under AGENT.6 that states its basis, beside a measured baseline and a "
    "recorded decision of the human owner, as the basis of the assessment that running units together costs less "
    "than running them in sequence (CP8); AGENT.23 accepts a transcript of the session that the agent did not edit "
    "in place of the record of each access it shows, an item the transcript lacks stated once for the session or "
    "beside the access (CC19); the Notes say so, and that the question left to the custodians on GOV.11 no longer "
    "affects the burden of AGENT.39")
AGENT_ROW = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {AGENT_READING}. |"
AGENT_RATIONALE = (
    f"Minor amendment of AGENT, revision 1.3, ratified by the custodian on {F.DATE}: {AGENT_READING}. The change is "
    "minor under STND.IDENT.3 because it widens two permissions, without altering the motivation or intent of the "
    "governance. No floor is raised (GOV.11): AGENT.39 binds at every class as before and now accepts a basis the "
    "agent supplies, so the first parallel delegation needs no decision of the human owner; AGENT.23 still records "
    "every item of each access, by a transcript the agent did not edit where one shows it. Transition (GOV.42): "
    f"none. Entries R2.2 (CP8) and R2.6 (CC19) of the register, under rulings F1 and C8 of {RULINGS}; {RECORD}."
    + F.AUTHOR)


def apply_agent(root: Path, at: str) -> None:
    replace_text(root, "AGENT/39.md", AGENT39)
    replace_text(root, "AGENT/23.md", AGENT23)
    replace_text(root, "AGENT/_doc.md", AGENT_DOC)
    F.check_fields(root, ["AGENT.39", "AGENT.23"], binding=True)
    F.finish(root, "AGENT", "AGENT", "1.2", "1.3", AGENT_ROW, AGENT_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# STND.CREW 1.2
# ----------------------------------------------------------------------------------------------------------------

CREW3 = [
    ("The lead agent SHOULD draft for the human owner, for each such provision, an amendment proposal for the human "
     "owner to send to its adopter (GOV.46, GOV.47, GOV.49).",
     "The lead agent SHOULD draft, for each such provision, an amendment proposal, which goes to the provision's "
     "adopter with the report of GOV.47 (GOV.46, GOV.47, GOV.49)."),
]

CREW10 = [
    ("The lead agent SHOULD assign to a unit of work each defect recorded under QA.5 that the finder does not fix, "
     "and each such change (QA.4, QA.5).",
     "The lead agent SHOULD assign to a unit of work each defect recorded under QA.5 that the finder does not fix, "
     "and each such change, and present to the human owner together, in its next report, the reports of those "
     "defects that QA.5 asks (QA.4, QA.5)."),
]

CREW23 = [
    ("An agent that has made a network access under an authorization for read-only research retrieval SHOULD "
     "change no part of the work, other than records, in the session in which it made that access (PRIME.11, "
     "GUARD.16).",
     "An agent that has made a network access under an authorization for read-only research retrieval SHALL change "
     "no part of the work, other than records, in the session in which it made that access (PRIME.11, GUARD.16). "
     "For this provision, a context that holds none of the retrieved content, other than through a research note, "
     "SHALL count as a session other than that one (PRIME.11)."),
]

CREW_DOC = [
    ("and drafts the amendment proposal for the human owner to send to the provision's adopter (STND.CREW.3, "
     "GOV.46, GOV.47, GOV.49);",
     "and drafts the amendment proposal, which goes to the provision's adopter with the project's report under "
     "GOV.47 rather than through the human owner one by one (STND.CREW.3, GOV.46, GOV.47, GOV.49);"),
    ("A defect that an agent finds outside its unit is recorded by that agent in defect tracking, as QA.5 asks, "
     "together with its report to the human owner; a needed change",
     "A defect that an agent finds outside its unit is recorded by that agent in defect tracking, as QA.5 asks, and "
     "the lead agent presents the reports of such defects to the human owner together in its next report, since "
     "QA.5 sets no time for the report; a needed change"),
    ("A lead agent that carries out research itself, where the work has no delegation, records the research note "
     "and continues the work in a new session.",
     "A lead agent that carries out research itself, where the work has no delegation, records the research note "
     "and continues the work in a new session; a context that holds none of the retrieved content other than "
     "through that note is a new session, so that no round trip to the human owner is needed to start one."),
    ("STND.CREW.23 is a recommendation;",
     "STND.CREW.23 asks the separation that PRIME.11 already makes, retrieved content reaching the work only as "
     "data, at the cost of a fresh context, which counts as a new session;"),
]

CREW_READING = (
    "STND.CREW.3 has the amendment proposal go to the provision's adopter with the report of GOV.47 (CP20); "
    "STND.CREW.10 has the lead agent present the reports that QA.5 asks of its agents to the human owner together "
    "in its next report (CP11); STND.CREW.23 uses SHALL, the modal its binding mode needs, and counts a context "
    "that holds none of the retrieved content other than through a research note as a new session (CP14, R7.3)")
CREW_ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {CREW_READING}. |"
CREW_RATIONALE = (
    f"Minor amendment of STND.CREW, revision 1.2, ratified by the custodian on {F.DATE}: {CREW_READING}. The change "
    "is minor under STND.IDENT.3 because it alters two recommendations and gives one obligation the modal of its "
    "mode, without altering the motivation or intent of the governance. No floor is raised (GOV.11): STND.CREW.3 "
    "and STND.CREW.10 take two round trips to the human owner out of ordinary work, since QA.5 and GOV.47 set no "
    "time for the report and the proposal; STND.CREW.23 states how PRIME.11 is met for content retrieved from the "
    "network, at the cost of a fresh context, which is a new session, so that it asks no decision of the human "
    "owner and halts no line of work. Transition (GOV.42): none. Entries R2.5 (CP11, CP14, CP20) and R7.3 of the "
    f"register, under ruling F1 of {RULINGS}; {RECORD}." + F.AUTHOR)


def apply_crew(root: Path, at: str) -> None:
    replace_text(root, "STND/CREW/3.md", CREW3)
    replace_text(root, "STND/CREW/10.md", CREW10)
    replace_text(root, "STND/CREW/23.md", CREW23)
    replace_text(root, "STND/CREW/_doc.md", CREW_DOC)
    F.finish(root, "STND/CREW", "STND.CREW", "1.1", "1.2", CREW_ROW, CREW_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# STND.THRT 1.1
# ----------------------------------------------------------------------------------------------------------------

THRT6 = [
    ("the actor SHALL record the event and propose to the human owner each change of the threat model that the "
     "event calls for (GUARD.16).",
     "the actor SHALL record the event and propose to the human owner, as an item of its next report, each change "
     "of the threat model that the event calls for (GUARD.16)."),
]

THRT_DOC = [
    ("The actor that brings an event about or learns of it records it and proposes the change it calls for; the "
     "human owner adopts the revised threat model, and every line of work that the event does not concern "
     "continues (AGENT.15).",
     "The actor that brings an event about or learns of it records it and proposes the change it calls for as an "
     "item of its next report, not as a referral; until the human owner adopts the revised threat model, the model "
     "as adopted governs, and every line of work that the event does not concern continues (AGENT.15)."),
]

THRT_READING = (
    "STND.THRT.6 has the actor propose each change of the threat model that an event calls for as an item of its "
    "next report, and the Notes say that the model as adopted governs until the human owner adopts the change "
    "(CC22)")
THRT_ROW = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {THRT_READING}. |"
THRT_RATIONALE = (
    f"Minor amendment of STND.THRT, revision 1.1, ratified by the custodian on {F.DATE}: {THRT_READING}. The change "
    "is minor under STND.IDENT.3 because it alters an obligation, without altering the motivation or intent of the "
    "governance. No floor is raised (GOV.11): GUARD.16 asks a review whenever exposure changes, and the proposal "
    "still reaches the human owner, in the next report rather than at once, so that an event of CSQ3 or CSQ4 work "
    "halts nothing. Transition (GOV.42): none. Entry R2.5 (CC22) of the register under ruling F1 of "
    f"{RULINGS}; {RECORD}." + F.AUTHOR)


def apply_thrt(root: Path, at: str) -> None:
    replace_text(root, "STND/THRT/6.md", THRT6)
    replace_text(root, "STND/THRT/_doc.md", THRT_DOC)
    F.finish(root, "STND/THRT", "STND.THRT", "1.0", "1.1", THRT_ROW, THRT_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# STND.WPROC 1.2
# ----------------------------------------------------------------------------------------------------------------

WPROC_DOC = [
    ("| Main line | Each branch from which the work is released or deployed. |",
     "| Main line | Each branch from which the work is released or deployed; a branch drawn on only within "
     "development, for the reliance that the CSQ3 reliance test of STND.CLASS.1 admits, is not one. |"),
    ("Advancing a main line releases a revision, because a main line is a branch from which the work is used beyond "
     "its development; a branch that supports an older release is a main line too.",
     "Advancing a main line releases a revision, because a main line is a branch from which the work is used beyond "
     "its development; a branch that supports an older release is a main line too. A branch drawn on only within "
     "development, for the reliance that the CSQ3 reliance test of STND.CLASS.1 admits, is not a main line, so a "
     "push to it is no release decision and an agent merges into it as STND.WPROC.11 provides."),
]

WPROC_READING = (
    "the term Main line excludes a branch drawn on only within development, for the reliance that the CSQ3 "
    "reliance test of STND.CLASS.1 admits (CP16)")
WPROC_ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {WPROC_READING}. |"
WPROC_RATIONALE = (
    f"Minor amendment of STND.WPROC, revision 1.2, ratified by the custodian on {F.DATE}: {WPROC_READING}. The "
    "change is minor under STND.IDENT.3 because it alters a defined meaning, without altering the motivation or "
    "intent of the governance. No floor is raised (GOV.11): a release is still the human owner's decision "
    "(QA.10, STND.WPROC.12), and a branch that releases or deploys is still a main line; the term now says that "
    "team use within development, which CSQ3 admits, is not a release. Transition (GOV.42): none. Ruling C8 (CP16) "
    f"of {RULINGS}; entry R2.6 of the register; {RECORD}." + F.AUTHOR)


def apply_wproc(root: Path, at: str) -> None:
    replace_text(root, "STND/WPROC/_doc.md", WPROC_DOC)
    F.finish(root, "STND/WPROC", "STND.WPROC", "1.1", "1.2", WPROC_ROW, WPROC_RATIONALE, at)


# ----------------------------------------------------------------------------------------------------------------
# The language Notes: STND.JL 1.4.1, STND.PY 1.3.1, STND.RUST 1.3.1, STND.STDC 1.3.1
# ----------------------------------------------------------------------------------------------------------------

TRANSITION = "; on a reclassification, STND.CLASS.22 governs."

LANGS = [
    ("JL", "1.4", "1.4.1",
     "Existing Julia source conforms to the default provisions when a change next touches it.",
     f"Existing Julia source conforms to the default provisions when a change next touches it{TRANSITION}"),
    ("PY", "1.3", "1.3.1",
     "Existing source conforms when a change next touches it, other than the strict checking of STND.PY.5, which "
     "existing modules reach through the list of STND.PY.6.",
     "Existing source conforms when a change next touches it, other than the strict checking of STND.PY.5, which "
     f"existing modules reach through the list of STND.PY.6{TRANSITION}"),
    ("RUST", "1.3", "1.3.1",
     "Existing Rust source conforms to the default provisions when a change next touches it.",
     f"Existing Rust source conforms to the default provisions when a change next touches it{TRANSITION}"),
    ("STDC", "1.3", "1.3.1",
     "Existing C source conforms to the default provisions when a change next touches it.",
     f"Existing C source conforms to the default provisions when a change next touches it{TRANSITION}"),
]


def apply_lang(root: Path, folder: str, old_rev: str, new_rev: str, old: str, new: str, at: str) -> None:
    doc_id = f"STND.{folder}"
    replace_text(root, f"STND/{folder}/_doc.md", [(old, new)])
    reading = ("the Notes keep their sentence on existing source and add that STND.CLASS.22 governs on a "
               "reclassification")
    row = (f"| {new_rev} | {F.DATE} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    rationale = (
        f"Editorial amendment of {doc_id}, revision {new_rev}, ratified by the custodian on {F.DATE}: {reading}. The "
        "change is editorial under STND.IDENT.3 because no obligation, permission, or defined meaning of this "
        f"document changes. Transition (GOV.42): none. Ruling C3 of {RULINGS}; entry R3.3 of the register, with "
        f"CL12; {RECORD}." + F.AUTHOR)
    F.finish(root, f"STND/{folder}", doc_id, old_rev, new_rev, row, rationale, at)


def lang_steps():
    def make(args):
        return lambda root, at: apply_lang(root, *args, at)
    return [make(args) for args in LANGS]
