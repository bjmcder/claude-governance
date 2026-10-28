"""Round o of 2026-10-28, the text: the onset rule of STND.CLASS.10, the field in STND.DRAFT, and the Notes of
each document whose onset paragraph becomes one sentence citing STND.CLASS.10 and the fields (ruling C7).

Each edit of the Notes is computed from the text as the earlier rounds leave it, so that the module runs again
after a revision of round c: a paragraph is found by its opening words, and within it a run of sentences, from
the one that opens with FIRST to the one that opens with LAST, is replaced by one sentence. Every sentence outside
the run is kept as it stands. A sentence ends at terminal punctuation followed by a capital letter.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from govharness.workflows.amend import replace_text  # noqa: E402

SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z(`\"])")
GIVES = "applies from the class that its field `onset` gives"
OMIT = "which work of CSQ4 may omit"
CSQ3_TIGHTENS = ("where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more "
                 "severe class tightens above the floor (PRIME.15)")


def _paragraph(paras: list[str], rel: str, start: str) -> int:
    hits = [i for i, p in enumerate(paras) if p.startswith(start)]
    if len(hits) != 1:
        raise ValueError(f"{rel}: {start[:60]!r} opens {len(hits)} paragraphs, not one")
    return hits[0]


def _sentence(sentences: list[str], rel: str, start: str) -> int:
    hits = [i for i, s in enumerate(sentences) if s.startswith(start)]
    if len(hits) != 1:
        raise ValueError(f"{rel}: {start[:60]!r} opens {len(hits)} sentences, not one")
    return hits[0]


def recast(root: Path, rel: str, start: str, first: str, last: str, new: str) -> None:
    """Replace the run of sentences FIRST to LAST of the paragraph that opens with START by NEW."""
    path = Path(root) / rel
    paras = path.read_text(encoding="utf-8").split("\n\n")
    i = _paragraph(paras, rel, start)
    sentences = SENTENCE_END.split(paras[i])
    a, b = _sentence(sentences, rel, first), _sentence(sentences, rel, last)
    if b < a:
        raise ValueError(f"{rel}: {last[:40]!r} precedes {first[:40]!r}")
    sentences[a:b + 1] = [new] if new else []
    paras[i] = " ".join(sentences)
    path.write_text("\n\n".join(p for p in paras if p), encoding="utf-8")


def insert_after(root: Path, rel: str, start: str, new: str) -> None:
    """Add the paragraph NEW after the paragraph that opens with START."""
    path = Path(root) / rel
    paras = path.read_text(encoding="utf-8").split("\n\n")
    i = _paragraph(paras, rel, start)
    paras.insert(i + 1, new)
    path.write_text("\n\n".join(paras), encoding="utf-8")


def profile(head: str, reason: str) -> str:
    """The one sentence of a profile whose fields keep a tightening above the floor."""
    return (f"{head}, inherits their rank and waivability (GOV.17), and {GIVES} under STND.CLASS.10, "
            f"{CSQ3_TIGHTENS}, because {reason}.")


SELECTOR = "Every provision other than the selector and the shared-matters provision instantiates only"
EACH_SELECTOR = "Each provision other than the selector and the shared-matters provision instantiates only"
SILENT = "its check runs without a person and the failure it prevents is silent at every class"

# ------------------------------------------------------------------------------------------------------------
# The Notes of each document: (paragraph start, first sentence, last sentence, the one sentence) per edit, and
# (old, new) pairs of replace_text for a clause inside a sentence.
# ------------------------------------------------------------------------------------------------------------

NOTES: dict[str, list[tuple]] = {
    "AGENT": [
        ("A provision inherits the rank and waivability", "Every waivable provision (AGENT.2,",
         "Every waivable provision (AGENT.2,",
         f"Every waivable provision is proportioned to class and {GIVES} under STND.CLASS.10."),
    ],
    "CPS": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, DSGN, INTPR, or QA",
                 "the failure that such content prevents reaches physical hardware at every class, where PRIME.13 "
                 "and PRIME.4 hold")),
    ],
    "HDES": [
        ("HDES.14 states how PRIME.4 applies", "Every other provision except HDES.1 and HDES.2",
         "Each such provision tightens above the floor",
         profile("Every other provision except HDES.1 and HDES.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or "
                 "RSRC", SILENT)),
    ],
    "HDES.ASIC": [
        (SELECTOR, SELECTOR, "Here an error found after submission",
         profile(f"{SELECTOR} VV, REPRO, INTPR, or DSGN",
                 f"{SILENT}, and an error found after submission cannot be corrected on that run")),
    ],
    "HDES.FPGA": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, or DSGN", SILENT)),
    ],
    "HW": [
        ("HW.8 states how PRIME.4 applies", "Every other provision except HW.1 and HW.2 instantiates",
         "At CSQ3 a hardware contract therefore holds",
         f"Every other provision except HW.1 and HW.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC, "
         f"inherits their rank and waivability (GOV.17), and {GIVES} under STND.CLASS.10, so that the hardware "
         "contract of HW.4 and the delivered arithmetic, the evidence, and the currency with which HW.5 to HW.7 fill "
         "it start together at CSQ2, with the contract that DSGN.5 asks, while the identity record of HW.3 and the "
         "variation declaration of HW.12, which cost one record each and which a later reclassification needs, start "
         "at CSQ3."),
    ],
    "HW.ASIC": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, or INTPR", SILENT)),
    ],
    "HW.CPU": [
        (EACH_SELECTOR, EACH_SELECTOR, "HW.CPU.5 tightens above CSQ1",
         f"{EACH_SELECTOR} VV, REPRO, INTPR, DSGN, or RSRC, inherits their rank and waivability (GOV.17), and "
         f"{GIVES} under STND.CLASS.10, the confirmation of HW.CPU.3 with the delivered arithmetic of HW.5 that it "
         "confirms, HW.CPU.4 adding to the record that RSRC.2 and RSRC.4 ask only in the runs that keep it, and "
         "HW.CPU.5 tightening above CSQ1, from which STND.CLASS.10 applies INTPR.7, at the cost of one message."),
    ],
    "HW.EMBED": [
        (EACH_SELECTOR, EACH_SELECTOR, "HW.EMBED.4 applies from CSQ3 although",
         f"{EACH_SELECTOR} VV, REPRO, INTPR, DSGN, or RSRC, inherits their rank and waivability (GOV.17), and "
         f"{GIVES} under STND.CLASS.10, {CSQ3_TIGHTENS} for outputs that drive physical hardware, at the cost of one "
         "statement in a record for HW.EMBED.6 and of the stated outputs at reset and halt for HW.EMBED.4."),
    ],
    "HW.FPGA": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, or INTPR", SILENT)),
    ],
    "HW.GPU": [
        ("HW.GPU.3 instantiates PRIME.4", "Every other provision except the selector",
         "Under STND.CLASS.10, HW.GPU.4 applies from CSQ3",
         "Every other provision except the selector and the shared-matters provision instantiates only RSRC, "
         f"inherits its rank and waivability (GOV.17), and {GIVES} under STND.CLASS.10, HW.GPU.4 only in the runs "
         "that track or measure resource use under RSRC.2 and RSRC.4."),
    ],
    "HW.QPU": [
        (EACH_SELECTOR, EACH_SELECTOR, "HW.QPU.5, HW.QPU.7, and HW.QPU.8 apply from CSQ3",
         f"{EACH_SELECTOR} VV, REPRO, INTPR, or RSRC, inherits their rank and waivability (GOV.17), and {GIVES} "
         "under STND.CLASS.10, where a field that gives CSQ3 for a statement that the row of INTPR.10 starts at CSQ2 "
         "tightens above the floor (PRIME.15) at the cost of one statement in a record."),
    ],
    "MEAS": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, INTPR, or QA",
                 "each costs a record and the failure it prevents is silent at every class")),
    ],
    "ML": [
        (SELECTOR, SELECTOR, "Each such provision tightens above the floor",
         profile(f"{SELECTOR} VV, REPRO, DSGN, or INTPR", SILENT)),
    ],
    "NUMER": [
        ("Every provision other than NUMER.1, NUMER.2, and NUMER.26", "Every provision other than NUMER.1",
         "Every provision other than NUMER.1",
         "Every provision other than NUMER.1, NUMER.2, and NUMER.26 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, "
         f"or RSRC, inherits their rank and waivability (GOV.17), and {GIVES} under STND.CLASS.10."),
    ],
    "STND.ANNEX": [
        ("Under STND.CLASS.10, each provision instantiates only DSGN.5", "Under STND.CLASS.10, each provision",
         "STND.ANNEX.3 instantiates only DSGN.5 and HW.4",
         "Under STND.CLASS.10, each provision instantiates only DSGN.5, REPRO.2, REPRO.3, and VV.1, and the provisions "
         f"HW.4, HW.5, HW.6, HW.12, and HW.EMBED.4 that instantiate them, and {GIVES}, {OMIT}."),
    ],
    "STND.BUILD": [
        ("Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL", "Under STND.CLASS.10, each provision",
         "Every other provision and sentence rests on no row",
         "Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, QA, or HW.5, and "
         f"{GIVES}, {OMIT}."),
    ],
    "STND.CODE": [
        ("Ignored results.", "STND.CODE.35 rests on the contract", "STND.CODE.35 rests on the contract", ""),
        ("Finite values.", "STND.CODE.27 instantiates the check", "STND.CODE.27 instantiates the check", ""),
        ("Rules for every language.", "STND.CODE.28 to STND.CODE.32 rest on no row",
         "Each is a default, a tightening above the floor",
         "STND.CODE.28 to STND.CODE.32 are defaults, each a tightening above the floor that a recorded decision "
         "replaces (PRIME.15, GOV.19), so none raises the floor (GOV.11)."),
        ("Claims of soundness.", "STND.CODE.34 states the limits", "STND.CODE.34 states the limits",
         "STND.CODE.34 is a default, a tightening above the floor that a recorded decision replaces (PRIME.15, "
         "GOV.19), so it raises no floor (GOV.11)."),
        ("Foreign interfaces.", "STND.CODE.22 and STND.CODE.23 rest on the schema",
         "STND.CODE.22 and STND.CODE.23 rest on the schema", ""),
        ("Under STND.CLASS.10, each default provision other than STND.CODE.17", "Under STND.CLASS.10, each default",
         "The onsets of STND.CODE.17",
         f"Under STND.CLASS.10, each default provision {GIVES}, {OMIT}, and STND.CODE.21 binds at every class; the "
         "rules of the form of code at a foreign interface, the declaration of STND.CODE.35, and the catch of "
         "STND.CODE.24 apply from CSQ3, since each costs nothing when the code is written and a rewrite of each "
         "interface when it first applies at a reclassification, while the comparison of layouts in the second "
         "sentence of STND.CODE.22 compares two declarations under the schema of DSGN.4 and starts at CSQ2."),
    ],
    "STND.CONC": [
        ("Under STND.CLASS.10, each default instantiates only DSGN, VV", "Under STND.CLASS.10, each default",
         "The sentences of each provision with three modals",
         "Under STND.CLASS.10, each default instantiates only DSGN, VV, REPRO, INTPR, RSRC, or a provision of HW or "
         f"NUMER, and {GIVES}, {OMIT}; the protections, orderings, lock rules, and lifecycle rules state what a "
         "protocol uses and not how its invariants are verified (DSGN.15), the argument of STND.CONC.11 concerns "
         "completion, and the facility of STND.CONC.19 is a rule of the form of code, so they apply from CSQ3, and "
         "the sentences of each provision with three modals share one onset."),
    ],
    "STND.CREW": [
        ("Under STND.CLASS.10, each default provision other than STND.CREW.4", "Under STND.CLASS.10, each default",
         "Under STND.CLASS.10, each default",
         f"Under STND.CLASS.10, each default provision {GIVES}, {OMIT}, STND.CREW.4, STND.CREW.8, and STND.CREW.10 "
         "with the provisions of AGENT that they also instantiate, to which they add only the planning, the cost "
         "model, and the report that they name."),
    ],
    "STND.CXX": [
        ("STND.CODE.14 lists the responses", "It instantiates INTPR.8, the diagnostics", "It instantiates INTPR.8",
         ""),
        ("Under STND.CLASS.10, each default instantiates only VV, REPRO", "Under STND.CLASS.10, each default",
         "The provisions of STND.CODE that the defaults cite keep",
         "Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or a provision of "
         f"HW, CPS, or NUMER, and {GIVES}, {OMIT}, where a field that gives CSQ3 for a part that the table of "
         "STND.CLASS.10 starts at a more severe class, the stated requirement of STND.CXX.13, the verification of "
         "STND.CXX.26, and the checks of STND.CXX.24 and STND.CXX.27, tightens above the floor (PRIME.15) at the "
         "cost of a type, a check that a tool runs, or a statement."),
        ("Under STND.CLASS.10, each default instantiates only VV, REPRO", "STND.CXX.33 is a default that instantiates",
         "STND.CXX.33 is a default that instantiates", ""),
    ],
    "STND.DEPS": [
        ("Under STND.CLASS.10, every default provision applies from CSQ3", "Under STND.CLASS.10",
         "Under STND.CLASS.10",
         f"Under STND.CLASS.10, every default provision {GIVES}, {OMIT}, STND.DEPS.5 asking for something only where "
         "a contract of DSGN.5 exists, and STND.DEPS.10, a permission, carries no field."),
    ],
    "STND.DOCS": [
        ("Under STND.CLASS.10, STND.DOCS.2", "Under STND.CLASS.10", "STND.DOCS.6 and STND.DOCS.7 are permissions",
         f"Under STND.CLASS.10, each default {GIVES}, {OMIT}, and STND.DOCS.6 and STND.DOCS.7 are permissions, which "
         "STND.CLASS.10 does not stage and which carry no field."),
    ],
    "STND.FTN": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "No provision has three modals.",
         "Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, REPRO, VV, INTPR, or a provision of NUMER "
         f"or HW, and {GIVES}, {OMIT}, the rules of the form of code at an interface among them at CSQ3, and its part "
         "that rests on NUMER or HW applies only to work that those profiles bind."),
    ],
    "STND.JL": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.JL.5, STND.JL.19, and STND.JL.34 instantiate",
         "Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, RSRC, or a "
         f"provision of NUMER, HW, or HW.CPU, and {GIVES}, {OMIT}; the part of each default that rests on NUMER, "
         "HW.7, or HW.CPU.3 applies only to work that those profiles bind, the store of STND.JL.39 applies from CSQ3 "
         "with the catch of STND.CODE.24, and a field that gives CSQ3 to STND.JL.5, STND.JL.19, or STND.JL.34, which "
         "also instantiate the contracts of DSGN.5, tightens above the floor (PRIME.15) for that work at the cost of "
         "a record or one run of the tests."),
    ],
    "STND.LEAN": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.LEAN.5 instantiates PRIME.2",
         f"Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, or SIMPL, and {GIVES}, {OMIT}, "
         "while STND.LEAN.5 instantiates PRIME.2 and binds at every class, CSQ4 included."),
    ],
    "STND.MPI": [
        ("Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR", "Under STND.CLASS.10",
         "Each part that rests on HW applies only",
         "Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or a provision of HW or "
         f"NUMER, and {GIVES}, {OMIT}; the matched type signatures of STND.MPI.14 and the reliance that STND.MPI.17 "
         "limits are rules of the form of code and apply from CSQ3, the argument of completion of STND.MPI.12 "
         "starts with that of STND.CONC.11, the run-time checks that verify the invariants of a protocol start at "
         "CSQ2 (DSGN.15), and each part that rests on HW applies only to work that HW binds."),
    ],
    "STND.OFFLD": [
        ("Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR",
         "Under STND.CLASS.10", "STND.PERF.12 and STND.PERF.14 also apply",
         "Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, or a provision "
         f"of HW, and {GIVES}, {OMIT}; a rule of the form of code that follows the documentation of a runtime "
         "library or the hardware applies from CSQ3, and a part that carries out HW.5, HW.11, HW.13, or HW.14, or "
         "relies on a limit that the hardware contract states, starts with that contract at CSQ2."),
    ],
    "STND.OMP": [
        ("Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, VV", "Under STND.CLASS.10",
         "The sentences of each provision with three modals",
         "Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, VV, or a provision of HW, "
         f"and {GIVES}, {OMIT}; the requires directive and the variant of STND.OMP.28 are rules of the form of code "
         "and apply from CSQ3 with HW.19, a part that carries out HW.4, HW.5, HW.11, HW.13, or HW.14 starts with that "
         "provision at CSQ2, and the sentences of each provision with three modals share one onset."),
    ],
    "STND.PERF": [
        ("Under STND.CLASS.10, each provision instantiates only VV", "Under STND.CLASS.10",
         "Every other provision and sentence rests on no row",
         "Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, SIMPL, RSRC, or AGENT.40, and "
         f"{GIVES}, {OMIT}."),
    ],
    "STND.PY": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.PY.5 asks for type checking",
         "Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, RSRC, or a "
         f"provision of NUMER, and {GIVES}, {OMIT}, the store of STND.PY.35 at CSQ3 with the catch of STND.CODE.24."),
    ],
    "STND.RUST": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.RUST.3, STND.RUST.4, STND.RUST.7",
         "Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or a provision "
         f"of HW, and {GIVES}, {OMIT}; the representation attribute of STND.RUST.24 and the unwinding of "
         "STND.RUST.25 and STND.RUST.26 apply from CSQ3 with the other rules of the form of code, and the part that "
         "rests on HW.5 or HW.7 applies only to work that HW binds."),
    ],
    "STND.STDC": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.STDC.28 and the other defaults rest",
         "Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, RSRC, VV, or a provision of "
         f"HW, and {GIVES}, {OMIT}, the extent of STND.STDC.7 at CSQ3 with the other rules of the form of code, and "
         "the rows of STND.STDC.1 apply from the classes that its table gives."),
    ],
    "STND.SV": [
        ("Class onset. Under STND.CLASS.10", "Under STND.CLASS.10", "STND.SV.28 instantiates INTPR.1",
         "Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, DSGN, SIMPL, QA, or a provision of "
         f"HDES or NUMER, and {GIVES}, {OMIT}, where a field that gives CSQ3 for what a reader needs to read a "
         "verdict or a coverage figure that HDES.6 or HDES.8 already asks at CSQ3, content that the row of INTPR.10 "
         "starts at CSQ2, tightens above the floor (PRIME.15), so that each record to which those sentences add "
         "keeps one onset."),
    ],
    "STND.TEST": [
        ("Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, RSRC, or QA", "Under STND.CLASS.10",
         "Every other provision and sentence rests on no row",
         "Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, RSRC, or QA, and "
         f"{GIVES}, {OMIT}; at CSQ3 a statement of the repository configuration meets STND.TEST.2, the derivation "
         "by a tool being the mechanism that tracks dependencies between results, which the row of QA.14 asks from "
         "CSQ2, and the tiers, the integration depths, and the records of selection, reuse, omission, and reason "
         "start at CSQ2, so that work of CSQ3 that runs its suite whole owes its verdicts and none of these "
         "records."),
    ],
    "STND.WFLOW": [
        ("Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, or QA",
         "Under STND.CLASS.10", "Every other provision and sentence rests on DSGN.1",
         "Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, or QA, and "
         f"{GIVES}, {OMIT}; the machinery of a long campaign of runs, the staleness rule, the engine records valid "
         "after a forced end, the storage budget, the state of work directories, the resumption record, and the "
         "tests of a clean area and of a resumption, starts at CSQ2 with the provenance of STND.WFLOW.35, and the "
         "attempt records of STND.WFLOW.15 at CSQ1, so that a workflow of CSQ3 owes its declarations, the checks of "
         "its outputs, its retries, and its restart state."),
        ("A shared vocabulary of provenance", "Its second sentence rests on REPRO.12",
         "Its second sentence rests on REPRO.12",
         "Its second sentence qualifies the provenance of its first sentence, so the two sentences share one onset."),
    ],
    "STND.WPROC": [
        ("Under STND.CLASS.10, each default provision instantiates only", "Under STND.CLASS.10",
         "Under STND.CLASS.10",
         f"Under STND.CLASS.10, each default provision {GIVES}, {OMIT}, and STND.WPROC.11, a permission, carries no "
         "field."),
    ],
}

# Clauses inside a sentence, as (old, new) for replace_text; each old text occurs once.
CLAUSES: dict[str, list[tuple[str, str]]] = {
    "STND.KNOW": [("are defaults (GOV.19) that apply from CSQ3.",
                   "are defaults (GOV.19) that apply from the class that their field `onset` gives under "
                   "STND.CLASS.10.")],
    "STND.PROJ": [("are defaults with the onset of REPRO.12 and INTPR.12 under STND.CLASS.10: they apply from CSQ3,",
                   "are defaults that apply from the class that their field `onset` gives under STND.CLASS.10,")],
    "STND.PY": [("which STND.CONC.23 does not reach; both apply from CSQ3.", "which STND.CONC.23 does not reach.")],
    "STND.WFLOW": [(" are that mechanism within one workflow and apply from CSQ2.",
                    " are that mechanism within one workflow.")],
}

VVUQ_NOTE = (
    f"Under STND.CLASS.10, each default {GIVES}, {OMIT}, and STND.VVUQ.83 binds at every class. The core that "
    "applies from CSQ3, STND.VVUQ.1, STND.VVUQ.3, STND.VVUQ.5, STND.VVUQ.7, STND.VVUQ.13, STND.VVUQ.17, "
    "STND.VVUQ.62, STND.VVUQ.64, and STND.VVUQ.82, with the basis of each tolerance that NUMER.11 asks, chooses the "
    "tier of each comparison, handles values that are not finite, states each tolerance with its relative and "
    "absolute parts within its bracket, keeps asserted checks and regression guards, and builds and tests random "
    "streams; the methods of high-assurance numerics, from error budgets and noise floors to multiplicity control "
    "and order tests at several levels, start at CSQ2, so that work of CSQ3 meets NUMER through the core, while the "
    "obligations of LVL0 that the other provisions serve apply to it in full. No default raises the floor (GOV.11).")

CLASS10 = [("which applies from the class that the table gives (GOV.11).",
            "which applies from the class that the table gives, and each part of a provision below LVL0 to which "
            "the field `onset` of that provision gives a class, which applies from that class (GOV.11).")]

CLASS_NOTE = (
    "Below LVL0, the field `onset` of a provision (STND.DRAFT#representation-in-the-harness) states the class from "
    "which each of its parts applies, and STND.CLASS.10 gives the field its force. The fields follow one rule: a part "
    "applies from the row of the table of STND.CLASS.10 whose named item the part asks for, a reference oracle, a "
    "schema, a contract, a documented limit of validity, or another item of the column Part, and otherwise from "
    "CSQ3. A part that instantiates the obligation of a row without asking for its item applies from CSQ3, so that "
    "a rule of the form of code that rests on DSGN.4 or DSGN.5, and the catch of a failure before it crosses a "
    "foreign frame, apply from CSQ3 with the other defaults of form: each costs nothing when the code is written, "
    "and a rewrite of each interface when it first applies at a reclassification. Where a field departs from the "
    "rule, the Notes of its document give the reason: a less severe class tightens above the floor (PRIME.15), and "
    "a more severe class keeps the methods of a standard beyond its core out of work of CSQ3, while the obligation "
    "of LVL0 that such a part serves applies at CSQ3 in full. A binding provision, a provision that applies at every "
    "class, and a permission carry no field.")

DRAFT_FIELD = (
    "- `onset`: the class from which the provision applies under STND.CLASS.10, written as one class, `\"CSQ3\"`, "
    "or, where a part starts at a more severe class than the rest, as a list of the class of the provision followed "
    "by one pair of a part and its class for each such part, `[\"CSQ3\", [\"sentence 2\", \"CSQ2\"]]`. A part is "
    "`sentence N`, the Nth sentence of the body outside its tables, counted at terminal punctuation, or `row CELL`, "
    "the row of a table of the body whose first cell is CELL. The class of the provision is CSQ0 to CSQ3, or CSQ4 in "
    "a list, for a provision that applies at every class except its named parts. A binding provision, a provision "
    "of LVL0, a provision that applies whole at every class, and a permission carry no field. The harness fails a "
    "malformed value, a field on another item, and a part that the body does not hold.")
DRAFT_AFTER = "- `checked_by`: the checks that verify the provision."

STDC1 = [("| STND.CXX.7 | CSQ2 |", "| STND.CXX.7 | CSQ3 |")]


def apply_notes(root: Path, doc_id: str) -> None:
    """Make the edits of the Notes of one document."""
    root = Path(root)
    rel = f"{doc_id.replace('.', '/')}/_doc.md"
    for start, first, last, new in NOTES.get(doc_id, []):
        recast(root, rel, start, first, last, new)
    if doc_id in CLAUSES:
        replace_text(root, rel, CLAUSES[doc_id])
    if doc_id == "STND.VVUQ":
        replace_text(root, rel, [("\n\n## References\n", f"\n\n{VVUQ_NOTE}\n\n## References\n")])
    if doc_id == "STND.CLASS":
        replace_text(root, "STND/CLASS/10.md", CLASS10)
        insert_after(root, rel, "Work of CSQ3 meets the seven proportioned Articles", CLASS_NOTE)
    if doc_id == "STND.DRAFT":
        path = Path(root) / rel
        lines = path.read_text(encoding="utf-8").split("\n")
        hits = [i for i, line in enumerate(lines) if line.startswith(DRAFT_AFTER)]
        if len(hits) != 1:
            raise ValueError(f"{rel}: {len(hits)} lines open with the field checked_by")
        lines.insert(hits[0] + 1, DRAFT_FIELD)
        path.write_text("\n".join(lines), encoding="utf-8")
    if doc_id == "STND.STDC":
        replace_text(root, "STND/STDC/1.md", STDC1)
