"""Round e of 2026-10-28, part 2: the process and systems documents.

STND.DOCS and STND.DRAFT (one spelling table, CP26; the imperative mood, CP27), STND.WFLOW (agent self-records,
CP13), STND.WPROC (AGENT.47 cited, CP26; writes to shared records, CP15), STND.IDENT (CP28), STND.INSTR (the agent
instructions need not be presented whole, AD9), STND.VVUQ (the research note and the versions, CP17, CP25),
STND.MPI (CS21), HDES and HDES.ASIC (CS20, CS22), the root document STND (CP24), STND.PROJ (one citation of the
defaults, CC20; the execution paths, the residual of CS9), HW (the residual of CS9), STND.CLASS (CC30), and
STND.PERF (CS17).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
import round_e_base as E  # noqa: E402
from govharness.workflows.amend import Change, record_transaction, replace_text  # noqa: E402

F1 = E.ruling("F1")
NONE = "none"
DEFAULTS_FLOOR = "No floor is raised (GOV.11): every provision changed is a default that a recorded decision replaces"
NOTES_FLOOR = "No floor is raised or lowered (GOV.11): only informative text changes"

# ---------------------------------------------------------------------------------------------------- STND.DOCS

SPELLING_TABLE = (
    "| British | American |\n| --- | --- |\n"
    + "".join(f"| {b} | {a} |\n" for b, a in [
        ("behaviour", "behavior"), ("colour", "color"), ("favour", "favor"), ("honour", "honor"),
        ("labour", "labor"), ("neighbour", "neighbor"), ("centre", "center"), ("metre", "meter"),
        ("litre", "liter"), ("fibre", "fiber"), ("analyse", "analyze"), ("organise", "organize"),
        ("recognise", "recognize"), ("minimise", "minimize"), ("maximise", "maximize"), ("optimise", "optimize"),
        ("utilise", "utilize"), ("standardise", "standardize"), ("authorise", "authorize"),
        ("initialise", "initialize"), ("serialise", "serialize"), ("normalise", "normalize"),
        ("catalogue", "catalog"), ("defence", "defense"), ("offence", "offense"), ("grey", "gray"),
        ("programme", "program"), ("artefact", "artifact"), ("judgement", "judgment"), ("ageing", "aging"),
        ("modelling", "modeling"), ("labelling", "labeling"), ("cancelled", "canceled"),
        ("travelling", "traveling"), ("fulfil", "fulfill"), ("enrol", "enroll"), ("whilst", "while"),
        ("amongst", "among")])).rstrip("\n")


def edit_docs(root: Path) -> None:
    rel = "STND/DOCS/8.md"
    replace_text(root, rel, [
        ("of which the tables of STND.DRAFT.33 and of this provision list a part (INTPR.12).",
         "of which the tables of this provision list a part (INTPR.12)."),
        ('refers_to: ["STND.DRAFT.33"]', "refers_to: []"),
        ('defines: ["american-usage"]', 'defines: ["american-usage", "spelling"]'),
    ])
    F.set_body(root, rel, E.body_of(root, rel).rstrip("\n") + "\n\n" + SPELLING_TABLE)
    replace_text(root, "STND/DOCS/_doc.md", [
        ("The tables of STND.DRAFT.33 and STND.DOCS.8 list common differences",
         "The two tables of STND.DOCS.8 list common differences"),
        ("whose provisions STND.DRAFT.33 already covers.",
         "whose provisions STND.DRAFT.33 already covers, with the spelling table of STND.DOCS.8, which the "
         "drafting check of American spelling reads."),
    ])
    F.check_fields(root, ["STND.DOCS.8"])


DOCS = E.Step(
    "STND.DOCS", edit_docs, False,
    "STND.DOCS.8 holds the spelling table that STND.DRAFT.33 held, beside its own table of usage, so that the corpus "
    "keeps one spelling table; its first sentence cites the tables of this provision alone, and the Notes say which "
    "table the drafting check reads",
    "the list of American spellings that STND.DOCS.8 cited, in the tables of STND.DRAFT.33 and of this provision, "
    "is the same list after the table moves, so no obligation, permission, or defined meaning changes",
    NOTES_FLOOR.replace("only informative text changes", "no obligation changes"), "unchanged", NONE,
    f"{F1}; register entry R6.4 (CP26, checked)")

# ---------------------------------------------------------------------------------------------------- STND.DRAFT


def edit_draft(root: Path) -> None:
    rel = "STND/DRAFT/33.md"
    replace_text(root, rel, [
        ('refers_to: []', 'refers_to: ["STND.DOCS.8"]'),
        ('defines: ["spelling"]', "defines: []"),
    ])
    F.set_body(root, rel, "A provision SHALL use American spelling, of which the spelling table of STND.DOCS.8 "
                          "lists a part (INTPR.12).")
    replace_text(root, "STND/DRAFT/10.md", [
        ("A sentence of a document SHALL NOT be written in the imperative mood (INTPR.12).",
         "A sentence of a document of governance or of a project instrument SHALL NOT be written in the "
         "imperative mood (INTPR.12)."),
    ])
    F.check_fields(root, ["STND.DRAFT.10", "STND.DRAFT.33"])


DRAFT = E.Step(
    "STND.DRAFT", edit_draft, True,
    "STND.DRAFT.33 keeps its rule and cites the spelling table of STND.DOCS.8, which now holds the table that it "
    "held, so that the corpus keeps one spelling table; STND.DRAFT.10 reaches a sentence of a document of governance "
    "or of a project instrument, the documents that this standard governs, in place of a sentence of any document",
    "STND.DRAFT.10 states its reach, which the word document left undefined and which work documentation, where "
    "STND.DOCS admits the imperative of installation steps, falls outside (STND.JL Notes: STND.DRAFT.10 concerns "
    "governance text); STND.DRAFT.33 is unchanged in its outcome",
    f"{DEFAULTS_FLOOR}, and STND.DRAFT.10 narrows to the documents it governed in practice",
    "unchanged", NONE, f"{F1}; register entries R6.4 (CP26, checked) and R7.1 (CP27, checked)")

# ---------------------------------------------------------------------------------------------------- STND.WFLOW

WFLOW_DOC = [
    ("A step that a person or an agent performs by hand has its inputs and outputs declared (STND.WFLOW.1),",
     "The record that an agent keeps of its own actions under REPRO.11 is no workflow run under this standard: an "
     "action of an agent or a person is a step only where a workflow description declares it. A step of a workflow "
     "description that a person or an agent performs by hand has its inputs and outputs declared (STND.WFLOW.1),"),
    ("a task that a workflow engine starts, or a step that a person or an agent performs. |",
     "a task that a workflow engine starts, or a step that a person or an agent performs and that a workflow "
     "description declares. |"),
]


def edit_wflow(root: Path) -> None:
    replace_text(root, "STND/WFLOW/_doc.md", WFLOW_DOC)


WFLOW = E.Step(
    "STND.WFLOW", edit_wflow, True,
    "the term Step reaches a step that a person or an agent performs only where a workflow description declares "
    "it, and the Purpose states that the record that an agent keeps of its own actions under REPRO.11 is no "
    "workflow run under this standard, so that STND.WFLOW.1, STND.WFLOW.3, STND.WFLOW.4, and STND.WFLOW.36 no "
    "longer reach each session of an agent, which AGENT and STND.WPROC govern",
    "it alters a defined meaning and so the reach of four defaults",
    f"{DEFAULTS_FLOOR}; the scope narrows, and REPRO.11 still has the steps of an agent recorded, in the form that "
    "AGENT gives",
    "unchanged", NONE, f"{F1}; register entry R6.4 (CP13)")

# ---------------------------------------------------------------------------------------------------- STND.WPROC

WPROC13 = ("An agent that proposes a release SHALL record and present to the human owner the revision it proposes, "
           "and each item that the work reports of its units state under AGENT.47 (GOV.50, AGENT.47).")
WPROC16 = E.provision(
    "STND.WPROC", 16, "Shared records on the development line", "Records", "default", ["QA.2", "DSGN.15"], [],
    "An agent that works on a unit branch SHOULD make each change to the ledger, the roadmap, defect tracking, or "
    "the record of decisions awaiting the human owner as a commit on the development line that changes only that "
    "record (QA.2, DSGN.15).", "CSQ3")
WPROC_DOC = [
    ("and the record of decisions awaiting the human owner. A unit record",
     "and the record of decisions awaiting the human owner. An agent on a unit branch writes one of them by a commit "
     "on the development line that changes only that record, made on the current state of that line (STND.WPROC.4, "
     "STND.WPROC.16); such a commit is no merge, so that STND.WPROC.10 does not reach it, and a commit that finds "
     "the line moved is made again on its new state, which is the protocol for the shared records that DSGN.15 "
     "asks. A unit record"),
]


def edit_wproc(root: Path) -> None:
    F.set_body(root, "STND/WPROC/13.md", WPROC13)
    E.add_provision(root, "STND/WPROC", WPROC16)
    replace_text(root, "STND/WPROC/_doc.md", WPROC_DOC)
    F.check_fields(root, ["STND.WPROC.13"], binding=True)
    F.check_fields(root, ["STND.WPROC.16"])


WPROC = E.Step(
    "STND.WPROC", edit_wproc, True,
    "STND.WPROC.13 has the release proposal present each item that the work reports of its units state under "
    "AGENT.47, in place of restating the list of AGENT.47; new STND.WPROC.16 (default) has an agent on a unit branch "
    "make each change to a shared record as a commit on the development line that changes only that record, and "
    "the Notes state the protocol",
    "STND.WPROC.16 adds a default, the protocol for concurrent writes to the shared records that DSGN.15 asks; the "
    "change to STND.WPROC.13 cites the list of AGENT.47 that it restated, and asks the same items",
    "No floor is raised (GOV.11): STND.WPROC.13 stays binding and asks what AGENT.47 already has the work reports "
    "state, and STND.WPROC.16 is a default that a recorded decision replaces",
    "STND.WPROC.16 from CSQ3, the class of the other defaults on records; the others unchanged", NONE,
    f"{F1}; register entries R6.4 (CP26, checked) and R7.2 (CP15)")

# ---------------------------------------------------------------------------------------------------- STND.IDENT


def edit_ident(root: Path) -> None:
    replace_text(root, "STND/IDENT/13.md", [(
        "Where no review transaction precedes the transaction of a revision, the adopter's decision",
        "Where no review transaction precedes the transaction of a revision whose adopter is not its author, the "
        "adopter's decision")])
    F.check_fields(root, ["STND.IDENT.13"], binding=True)


IDENT = E.Step(
    "STND.IDENT", edit_ident, True,
    "the adopter's decision serves as the QA.7 review of a revision only where the adopter is not the author of "
    "that revision",
    "it narrows a permission, which as written let an adopter who authored a revision review it, against QA.7",
    "No floor is raised (GOV.11): QA.7 already has every change reviewed by an actor other than its author, and the "
    "provision now asks nothing beyond it; the custodian's revisions, which an agent authors, are unaffected",
    "unchanged", NONE, f"{F1}; register entry R7.2 (CP28)")

# ---------------------------------------------------------------------------------------------------- STND.INSTR

INSTR_NOTE = (
    "Its effort estimation and delegation sizing are in the AGENT profile (AGENT.6 to AGENT.10).",
    "Its effort estimation and delegation sizing are in the AGENT profile (AGENT.6 to AGENT.10). No provision asks "
    "that the agent instructions be presented to an agent whole: an environment that loads the provisions that "
    "govern an action when the action needs them serves STND.INSTR.10 as well as one that loads them all at the "
    "start of a session, since GOV.39 has an actor read the full text of a provision before relying on it.")


def edit_instr(root: Path) -> None:
    replace_text(root, "STND/INSTR/_doc.md", [INSTR_NOTE, (
        "The earlier draft's default standing authorization is dropped, because no default grants an authorization "
        "(GOV.22).",
        "This standard proposes no default standing authorization, because no default grants an authorization "
        "(GOV.22).")])


INSTR = E.Step(
    "STND.INSTR", edit_instr, False,
    "the Notes state that no provision asks that the agent instructions be presented to an agent whole, an "
    "environment that loads the provisions that govern an action when it needs them serving STND.INSTR.10, and "
    "a sentence that narrated an earlier draft states the outcome",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE,
    f"{F1}; finding AD9 of review-records/deep-review-2026-10-28/anthropic-docs.md (checked; the brief names it "
    "AD6)")

# ---------------------------------------------------------------------------------------------------- STND.VVUQ

VVUQ_DOC = [
    ("The provisions were synthesized from a research note of 2026-10-11, kept in the project as "
     "claude/research/vvuq-research-notes.md and proposed as a knowledge entry (GOV.32), which surveyed standards "
     "bodies, national laboratories, agencies, and the literature, and logged each retrieval. Where a default number "
     "rests on a source, the note cites it;",
     "The provisions were synthesized from a research note of 2026-10-11, which surveyed standards bodies, national "
     "laboratories, agencies, and the literature, and logged each retrieval; the note is not kept in the project. "
     "Where a default number rests on a source, the table of sources in the Notes gives it;"),
    ("| MCNP 6.3.2 Theory and User Manual, LA-UR-26-23119 Rev. 1 | Current; not opened by the research |",
     "| MCNP Theory and User Manual | Current release; not opened by the research |"),
    ("MCNP4B manual and a CANTEACH chapter; the current MCNP 6.3.2 manual was not opened",
     "an earlier MCNP manual and a CANTEACH chapter; the current MCNP manual was not opened"),
    ("beside BigCrush, the one that STND.VVUQ.63 named before this revision.", "beside BigCrush, the largest."),
]


def edit_vvuq(root: Path) -> None:
    replace_text(root, "STND/VVUQ/_doc.md", VVUQ_DOC)


VVUQ = E.Step(
    "STND.VVUQ", edit_vvuq, False,
    "the Purpose no longer names a research note that the project does not hold and a knowledge entry that was "
    "never made, and says that the table of sources in the Notes gives the source of each default number that "
    "rests on one; the Notes name the manuals of one code without their version numbers, and a sentence that "
    "narrated an earlier revision names the battery by its size",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE,
    f"{F1}; register entry R7.1 (CP17, CP25, checked); the path exists nowhere in the repository or its history")

# ---------------------------------------------------------------------------------------------------- STND.MPI


def edit_mpi(root: Path) -> None:
    replace_text(root, "STND/MPI/_doc.md", [(
        "The source is the project's research note claude/research/parallel-models.md",
        "The source is the project's research note research/parallel-models.md")])


MPI = E.Step(
    "STND.MPI", edit_mpi, False,
    "the Notes give the path of the research note as research/parallel-models.md, where the note is kept",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE, f"{F1}; register entry R7.1 (CS21)")

# ---------------------------------------------------------------------------------------------------- HDES, HDES.ASIC


def edit_hdes(root: Path) -> None:
    replace_text(root, "HDES/_doc.md", [
        ("the technology detail belongs in planned LVL2 standards.",
         "the technology detail belongs in LVL2 standards, STND.SV among them."),
        ("are left to the work and to planned LVL2 standards.",
         "are left to the work and to LVL2 standards, STND.SV among them."),
    ])


HDES = E.Step(
    "HDES", edit_hdes, False,
    "the Purpose and the Notes name STND.SV among the LVL2 standards that hold the detail of a technology, in "
    "place of planned standards, and References lists it",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE, f"{F1}; register entry R7.1 (CS20)")


def edit_hdes_asic(root: Path) -> None:
    replace_text(root, "HDES/ASIC/12.md", [(
        "each condition that HDES.10 states as not analyzed, and each variation that HDES.ASIC.5 states as not "
        "verified, each block",
        "each condition that HDES.10 states as not analyzed, each variation that HDES.ASIC.5 states as not "
        "verified, and each block")])


HDES_ASIC = E.Step(
    "HDES.ASIC", edit_hdes_asic, False,
    "the list of the second sentence of HDES.ASIC.12 places its conjunction before its last item, each block whose "
    "evidence rests only on the contract of an external component",
    "the sentence lists that block as an item, which a block cannot be read otherwise to be, since it is no "
    "variation; no obligation, permission, or defined meaning changes",
    "No floor is raised or lowered (GOV.11)", "unchanged", NONE, f"{F1}; register entry R7.1 (CS22, checked)")

# ---------------------------------------------------------------------------------------------------- STND (root)

STND_OLD = "LVL2 standards apply across projects and may name tools and methods."
STND_NEW = ("LVL2 standards apply across projects and state methods and defaults. They name no product, vendor, or "
            "version; a tool and its version are each project's choice.")
STND_RATIONALE = (
    f"Change of STND/_doc.md, the root document of the standards, planned, ratified and pinned by the custodian on "
    f"{F.DATE}: the text says that LVL2 standards state methods and defaults and name no product, vendor, or "
    "version, a tool and its version being each project's choice, in place of saying that they may name tools. The "
    "document is informative, holds no provision, and has no revision, so the change is recorded as ledger entry "
    "186 pinned the file, by a transaction of its own over that path alone. It states the custodian's standing "
    "direction that standards are agnostic, which each standard already follows (GOV.18 leaves the choice of tools "
    "to LVL2 and LVL3, and a standard leaves it to the project). No floor is raised or lowered (GOV.11). Class "
    f"onset: none. Transition (GOV.42): none. {F1}; register entry R7.1 (CP24); {E.RECORD}." + F.AUTHOR)


def apply_stnd(root: Path, at: str) -> None:
    root = Path(root)
    replace_text(root, "STND/_doc.md", [(STND_OLD, STND_NEW)])
    rec = record_transaction(root, Change(kind="annotate", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.36"], targets=[], scope=["STND/_doc.md"],
                                          rationale=STND_RATIONALE))
    print("seq", rec.entry["seq"], "STND/_doc.md (annotate)")


# ---------------------------------------------------------------------------------------------------- STND.PROJ

PROJ_COVERED = ("Work process, Defects, Review and release, Correction, Incidents, Dependencies, Records, Working "
                "notes, Workbench, Secret store, Access descriptors, Threat model, Reserved actions, Agent "
                "instructions, and Configuration")
PROJ2_ADD = (
    f" A project constitution MAY adopt STND.DFLT by one citation as the content of its sections {PROJ_COVERED}, and "
    "state in full only its other sections and each of these whose content departs from STND.DFLT (GOV.21, "
    "GOV.22).")
PROJ1 = [
    ("the components that hold domain items of each selected profile, with the execution paths of each by hardware "
     "type;",
     "the components that hold domain items of each selected profile;"),
    ("| Architecture | The recorded dependency structure of the components (DSGN.7) |",
     "| Architecture | The recorded dependency structure of the components (DSGN.7), and where the execution paths "
     "of each component are recorded by hardware type |"),
]
PROJ_DOC = [(
    "A section that adopts a provision of STND.DFLT by citation adopts its content as the project's own;",
    "A section that adopts a provision of STND.DFLT by citation adopts its content as the project's own, and one "
    "citation of STND.DFLT adopts it for each section that STND.PROJ.2 names, whose mechanism STND.DFLT provides: "
    "Work process (STND.DFLT.7 to STND.DFLT.9), Defects (STND.DFLT.10), Review and release and Correction, whose "
    "records STND.DFLT.8 gives, Incidents (STND.DFLT.12), Dependencies (STND.DFLT.11), Records (STND.DFLT.2 to "
    "STND.DFLT.5), Working notes (STND.DFLT.6), Workbench (STND.DFLT.28), Secret store (STND.DFLT.29 to "
    "STND.DFLT.31), Access descriptors (STND.DFLT.27), Threat model (STND.DFLT.18 and STND.DFLT.19), Reserved "
    "actions (STND.DFLT.14, STND.DFLT.15, and STND.DFLT.24), Agent instructions (STND.DFLT.20 and STND.DFLT.21), "
    "and Configuration (STND.DFLT.22 and STND.DFLT.35); the other sections, Identity, Classification, Knowledge "
    "base, Authorizations, Architecture, Physical hardware, and Exceptions, hold what only the project states, "
    "though the defaults say where the classification is recorded (STND.DFLT.13) and how an authorization is "
    "recorded and entered (STND.DFLT.16, STND.DFLT.17); the execution paths of each component, by hardware type, "
    "are recorded where the section Architecture names, a record of the work that changes without a decision of "
    "the human owner, while the classification records the value of the attribute of HW.1;")]


def edit_proj(root: Path) -> None:
    rel = "STND/PROJ/2.md"
    F.set_body(root, rel, E.body_of(root, rel).strip() + PROJ2_ADD)
    replace_text(root, rel, [('instantiates: ["GOV.21"]', 'instantiates: ["GOV.21", "GOV.22"]')])
    replace_text(root, "STND/PROJ/1.md", PROJ1)
    replace_text(root, "STND/PROJ/_doc.md", PROJ_DOC + [(
        "A constitution adopted before this revision keeps its authorizations,",
        "A constitution adopted before revision 1.1 of this standard keeps its authorizations,")])
    F.check_fields(root, ["STND.PROJ.1", "STND.PROJ.2"], binding=True)


PROJ = E.Step(
    "STND.PROJ", edit_proj, True,
    f"STND.PROJ.2 lets a project constitution adopt STND.DFLT by one citation as the content of its sections "
    f"{PROJ_COVERED}, whose mechanisms STND.DFLT provides, and state in full only its other sections and those whose "
    "content departs from it, the Notes giving the provisions of STND.DFLT for each; the section Architecture of "
    "STND.PROJ.1 names where the execution paths of each component are recorded by "
    "hardware type, in place of the section Classification listing them, so that a path on a new hardware type "
    "changes no record that the human owner "
    "adopts; the Notes name revision 1.1 where they said this revision",
    "it adds a permission and moves an item from one section to another",
    "No floor is raised or lowered (GOV.11): every mechanism of GOV.21 is still defined, by citation where STND.DFLT "
    "provides it; the classification keeps the value of each attribute that a selector tests (GOV.24), and path "
    "scope still decides which provisions of HW and its sub-profiles reach a component (STND.DRAFT.38), from a "
    "record of the work in place of one the human owner adopts",
    "unchanged; both provisions bind",
    "a classification that lists the execution paths stays valid; the list moves to the Architecture section at "
    "the next revision of the constitution",
    f"{F1}; register entries R7.2 (CC20) and R2.5 (CS9, the residual that "
    "review-records/rounds-2026-10-28/round-c/decisions.md leaves to this round)")

# ---------------------------------------------------------------------------------------------------- HW

HW_DOC = [(
    "the execution paths that the Classification section lists by hardware type (STND.PROJ.1) are the record that "
    "a new path changes, and a classification that admits the hardware types the work plans to use lets an agent "
    "add a path on an admitted type without a further decision of the human owner, and costs nothing before the "
    "path exists.",
    "the execution paths of each component are recorded by hardware type where the section Architecture of the "
    "constitution names (STND.PROJ.1), outside the classification, so that an agent adds a path on a new type to "
    "that record without "
    "a decision of the human owner, and the provisions of the sub-profile of that type reach the path from then "
    "on.")]


def edit_hw(root: Path) -> None:
    replace_text(root, "HW/_doc.md", HW_DOC)


HW = E.Step(
    "HW", edit_hw, False,
    "the Notes say that the execution paths are recorded by hardware type where the section Architecture names, "
    "outside the classification, as STND.PROJ.1 now has it",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE,
    f"{F1}; register entry R2.5 (CS9, the residual of round c)")

# ---------------------------------------------------------------------------------------------------- HW sub-profiles

SUB_OLD = "its provisions reach a component through the execution paths that the classification lists."
SUB_NEW = ("its provisions reach a component through the execution paths of that component, recorded by hardware type "
           "where the section Architecture of the constitution names (STND.PROJ.1).")


def subprofile_step(name: str) -> E.Step:
    """Return the editorial step of one sub-profile of HW, whose Notes follow STND.PROJ.1."""
    doc_id = f"HW.{name}"

    def edit(root: Path) -> None:
        replace_text(root, f"HW/{name}/_doc.md", [(SUB_OLD, SUB_NEW)])

    return E.Step(
        doc_id, edit, False,
        "the Notes say that the provisions reach a component through its execution paths, recorded by hardware "
        "type where the section Architecture of the constitution names, in place of the paths that the "
        "classification lists, as STND.PROJ.1 now has it",
        "only informative text changes", NOTES_FLOOR, "unchanged", NONE,
        f"{F1}; register entry R2.5 (CS9, the residual of round c)")


SUBPROFILES = [subprofile_step(n) for n in ("ASIC", "CPU", "EMBED", "FPGA", "GPU", "QPU")]

# ---------------------------------------------------------------------------------------------------- STND.CLASS

CLASS_DOC = [(
    "and the records of STND.CLASS.23 where the classification records an expected class.",
    "and the records of STND.CLASS.23 where the classification records an expected class. A mechanism of GOV.21 "
    "whose obligation work of CSQ4 may omit, review (QA.7), incident handling (QA.15), and retention (REPRO.12) "
    "among them, costs that work no more than one citation of the defaults (STND.PROJ.2), and the obligation that "
    "it serves applies from the class that STND.CLASS.10 gives.")]


def edit_class(root: Path) -> None:
    replace_text(root, "STND/CLASS/_doc.md", CLASS_DOC)


CLASS = E.Step(
    "STND.CLASS", edit_class, False,
    "the Notes say that a mechanism of GOV.21 whose obligation work of CSQ4 may omit costs that work one citation "
    "of the defaults, and that the obligation it serves applies from the class that STND.CLASS.10 gives",
    "only informative text changes", NOTES_FLOOR, "unchanged", NONE, f"{F1}; finding CC30 (checked; it holds)")

# ---------------------------------------------------------------------------------------------------- STND.PERF


def edit_perf(root: Path) -> None:
    rel = "STND/PERF/1.md"
    F.set_body(root, rel, E.body_of(root, rel).strip()
               + " Each claim that HW.22 governs SHOULD rest on a performance evaluation as well (RSRC.4).")
    replace_text(root, rel, [("refers_to: []", 'refers_to: ["HW.22"]')])
    F.check_fields(root, ["STND.PERF.1"])


PERF = E.Step(
    "STND.PERF", edit_perf, True,
    "STND.PERF.1 has each claim that HW.22 governs, that one execution path is faster or more efficient than "
    "another in a reported result or a release, rest on a performance evaluation, whether or not the code is "
    "performance-sensitive",
    "it adds a recommendation",
    f"{DEFAULTS_FLOOR}; the claim already rests on measurements under HW.22, and the evaluation adds their "
    "repetition, dispersion, and uncertainty",
    "unchanged; the new sentence applies from CSQ3, with the rest of STND.PERF.1", NONE,
    f"{F1}; finding CS17 (checked; it holds)")

STEPS = [DOCS, DRAFT, WFLOW, WPROC, IDENT, INSTR, VVUQ, MPI, HDES, HDES_ASIC]
LATER = [PROJ, HW, *SUBPROFILES, CLASS, PERF]
