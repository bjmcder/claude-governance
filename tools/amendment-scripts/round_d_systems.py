"""Round d of 2026-10-28: STND.CONC 1.1.1, STND.PERF 1.1, STND.OFFLD 1.2, STND.MPI 1.1, and STND.OMP 1.0.4."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

REC = "review-records/rounds-2026-10-28/round-d/decisions.md"
REG = "review-records/deep-review-2026-10-28/register.md"


def body_of(root: Path, rel: str) -> str:
    return (Path(root) / rel).read_text(encoding="utf-8").partition("\n---\n\n")[2]


def editorial(doc_id: str, new: str, reading: str, cause: str, rulings: str) -> tuple[str, str]:
    row = (f"| {new} | {F.DATE} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    rationale = (
        f"Editorial amendment of {doc_id}, revision {new}, ratified by the custodian on {F.DATE}: {reading}. The "
        f"change is editorial under STND.IDENT.3 because it alters informative Notes only: {cause}, so no "
        f"obligation, permission, or defined meaning of this document changes. Transition (GOV.42): none. {rulings}"
        + F.AUTHOR)
    return row, rationale


# ---------------------------------------------------------------- STND.CONC 1.1.1

CONC_DOC = [
    ("declared with the size of its dependence, as STND.MPI.18 does for processes;",
     "declared with the size of its dependence, the processes of a parallel execution of MPI among those tasks;"),
    ("STND.CONC.22 applies STND.VVUQ.2 across numbers of tasks, as STND.MPI.19 does across numbers of processes:",
     "STND.CONC.22 applies STND.VVUQ.2 across numbers of tasks, numbers of processes among them:"),
    ("STND.PY.17 and STND.JL.24 state the same for their languages,",
     "STND.CODE.29 states the same for each part of divided work in every language, parts run as separate runs "
     "included,"),
    ("(STND.CONC.24, as STND.MPI.24 does for processes)",
     "(STND.CONC.24, for the processes of a parallel execution as for every other kind of task)"),
]
CONC_READING = (
    "the Notes cite STND.CONC.21, STND.CONC.22, and STND.CONC.24 for the processes of a parallel execution in place "
    "of STND.MPI.18, STND.MPI.19, and STND.MPI.24, which STND.MPI 1.1 withdraws, and STND.CODE.29 in place of "
    "STND.PY.17 and STND.JL.24, which STND.PY 1.3 and STND.JL 1.4 withdraw")


def apply_conc(root: Path, at: str) -> None:
    replace_text(Path(root), "STND/CONC/_doc.md", CONC_DOC)
    row, rat = editorial(
        "STND.CONC", "1.1.1", CONC_READING,
        "the provisions that the Notes now cite hold the outcomes of those that they cited, STND.CONC.21, "
        "STND.CONC.22, and STND.CONC.24 for the processes of a parallel execution, which are concurrent tasks under "
        "the term Concurrent task, and STND.CODE.29 for the streams of parts in every language",
        f"Rulings D1 of {F.RECORD}; register entries R6.2 (CL6) and R6.3 (CS7) of {REG}; decisions 4 and 11 of "
        f"{REC}.")
    F.finish(root, "STND/CONC", "STND.CONC", "1.1", "1.1.1", row, rat, at)


# ---------------------------------------------------------------- STND.PERF 1.1

PERF12_BODY = (
    "Where a performance evaluation excludes the start of each run as warm-up, it SHOULD judge steady state by a "
    "criterion recorded before its measurements, and report each run that does not reach that criterion (VV.3). "
    "Each measurement in a performance evaluation SHOULD state whether it includes the costs of first use, among "
    "them initialization, compilation at load, and the first filling of caches and memory (RSRC.4).")
PERF18 = [(
    "or be recorded as a decision under VV.3, with its criterion and the time at which that criterion was set (VV.3).",
    "or be recorded, with its criterion and when it was set, as a criterion set after the summary was seen (VV.3, "
    "QA.12).")]
PERF_DOC = [
    ("STND.OFFLD.31 holds the completion and first-use costs of a measurement of offloaded work,",
     "STND.OFFLD.31 holds the completion of a measurement of offloaded work,"),
    ("STND.OFFLD.31 is the form of the second sentence of STND.PERF.12 and of the second sentence of STND.PERF.14 "
     "for offloaded work, so both sentences leave offloaded work to it, and one record meets both standards.",
     "STND.OFFLD.31 is the form of the second sentence of STND.PERF.14 for offloaded work, which that sentence "
     "leaves to it, and the second sentence of STND.PERF.12 reaches each measurement of offloaded work in a "
     "performance evaluation as it reaches every other."),
    ("an exclusion chosen after the result was seen selects the result; MEAS.7 holds the same for observations, and "
     "where MEAS binds, one record meets both (STND.PERF.18).",
     "an exclusion chosen after the result was seen selects the result, so STND.PERF.18 records it as a criterion "
     "set after the summary was seen, which QA.12 promotes only as unverified; MEAS.7 holds the same for "
     "observations, in the same words, and where MEAS binds, one record meets both (STND.PERF.18)."),
]
PERF_READING = (
    "the second sentence of STND.PERF.12 reaches each measurement in a performance evaluation, offloaded work "
    "included, in place of leaving offloaded work to STND.OFFLD.31, whose second sentence STND.OFFLD 1.2 withdraws; "
    "STND.PERF.18 has an exclusion that follows no criterion recorded before the summary was seen recorded, with "
    "its criterion and when it was set, as a criterion set after the summary was seen, citing QA.12, in the words "
    "of MEAS.7, in place of a decision under VV.3; the Notes follow")
PERF_RATIONALE = (
    f"Minor amendment of STND.PERF, revision 1.1, ratified by the custodian on {F.DATE}: {PERF_READING}. The change "
    "is minor under STND.IDENT.3 because it widens the reach of a default to offloaded work and states the "
    "consequence of a post-hoc exclusion. The costs of first use of offloaded work in a performance evaluation "
    "were asked by the second sentence of STND.OFFLD.31 in the same words, so nothing more is asked there; outside "
    "a performance evaluation, a measurement of offloaded work no longer states them, the narrowing that register "
    "entry R6.3 accepts (CS14). The record that STND.PERF.18 asks is the record that it asked, now read as QA.12 "
    "already reads it, so that one exclusion carries the same consequence in STND.PERF and in MEAS (CS16). QA.12 "
    "stands among the citations as a provision that the default refers to, so that the onset of STND.PERF.18 "
    "stays that of VV.3 and REPRO.6. Each is a default that a recorded decision replaces (GOV.19), so none raises "
    "the floor (GOV.11). Class onset: unchanged, CSQ3. Transition (GOV.42): none. Register entry R6.3 (CS14, "
    f"CS16) of {REG}; decisions 12 and 13 of {REC}." + F.AUTHOR)


def apply_perf(root: Path, at: str) -> None:
    root = Path(root)
    F.set_body(root, "STND/PERF/12.md", PERF12_BODY, refers_to=[])
    replace_text(root, "STND/PERF/18.md", PERF18)
    F.set_body(root, "STND/PERF/18.md", body_of(root, "STND/PERF/18.md"), refers_to=["QA.12"])
    F.check_fields(root, ["STND.PERF.12", "STND.PERF.18"])
    replace_text(root, "STND/PERF/_doc.md", PERF_DOC)
    row = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {PERF_READING}. |"
    F.finish(root, "STND/PERF", "STND.PERF", "1.0.1", "1.1", row, PERF_RATIONALE, at)


# ---------------------------------------------------------------- STND.OFFLD 1.2

OFFLD31_BODY = ("Each measurement of the time of offloaded work SHOULD end at an observed completion of that work "
                "(RSRC.4, STND.PERF.14).")
OFFLD27 = [(
    "Where device code admits more than one size of group, its tests SHOULD run at more than one (VV.1).",
    "Where device code admits more than one size of group, its tests SHOULD run at more than one (VV.1). Tests that "
    "meet the two sentences above MAY serve, for device code, as the tests at more than one number of tasks "
    "that STND.CONC.24 asks (VV.1).")]
OFFLD_DOC = [
    ("These provisions remove none of STND.CONC: its bounded waits (STND.CONC.10), observed cancellation "
     "(STND.CONC.13), and tests at three or more numbers of tasks (STND.CONC.24) still apply to device code, and a "
     "programming model that gives device code no facility for one of them leaves a project a recorded decision "
     "under REPRO.7.",
     "These provisions remove none of STND.CONC: its bounded waits (STND.CONC.10) and observed cancellation "
     "(STND.CONC.13) still apply to device code, and a programming model that gives device code no facility for one "
     "of them leaves a project a recorded decision under REPRO.7. STND.OFFLD.27 is the form of STND.CONC.24 for "
     "device code: the sizes of the problem and of the groups that it tests vary the number of threads and of "
     "groups, and a problem whose size the size of its groups does not divide is the uneven division that "
     "STND.CONC.24 asks for, so its tests serve as those of STND.CONC.24 there, and the third sentence of "
     "STND.CONC.24 still sets the tier of a comparison between them."),
    ("the first access to memory that migrates on demand is likely to pay for migration as well, which o3 did not "
     "retrieve and is unverified, and such a migration at first access is among the first filling of memory that "
     "the second sentence of STND.OFFLD.31 names;",
     "the first access to memory that migrates on demand is likely to pay for migration as well, which o3 did not "
     "retrieve and is unverified, and such a migration at first access is among the first filling of memory that "
     "the second sentence of STND.PERF.12 names;"),
    ("STND.OFFLD.31 is the form for offloaded work of the second sentences of STND.PERF.12 and STND.PERF.14, which "
     "hold the costs of first use and the end of each timed asynchronous operation for every other measurement in a "
     "performance evaluation and leave offloaded work to it. The two name the same costs of first use, which are "
     "initialization, compilation at load, and the first filling of caches and memory, so one record of offloaded "
     "work that states them meets both. It reaches each measurement of the time of offloaded work, in a performance "
     "evaluation or not.",
     "STND.OFFLD.31 is the form for offloaded work of the second sentence of STND.PERF.14, which holds the end of "
     "each timed asynchronous operation for every other measurement in a performance evaluation and leaves "
     "offloaded work to it, and it reaches each measurement of the time of offloaded work, in a performance "
     "evaluation or not. The second sentence of STND.PERF.12 has each measurement in a performance evaluation, of "
     "offloaded work as of other code, state whether it includes the costs of first use, initialization, "
     "compilation at load, and the first filling of caches and memory among them."),
]
OFFLD_READING = (
    "STND.OFFLD.31 keeps its first sentence, the end of each measurement of the time of offloaded work at an "
    "observed completion, and drops its second, the costs of first use, which the second sentence of STND.PERF.12 "
    "now holds for each measurement in a performance evaluation, offloaded work included; STND.OFFLD.27 lets its "
    "tests of device code serve as the tests at more than one number of tasks of STND.CONC.24 for that code; the Notes "
    "state that STND.OFFLD.27 is the form of STND.CONC.24 for device code, and cite STND.PERF.12 for the costs of "
    "first use")
OFFLD_RATIONALE = (
    f"Minor amendment of STND.OFFLD, revision 1.2, ratified by the custodian on {F.DATE}: {OFFLD_READING}. The "
    "change is minor under STND.IDENT.3 because it removes one sentence of a default and adds a permission to "
    "another. The first sentence of STND.OFFLD.31 is offload content that holds outside a performance evaluation "
    "and stays; the second repeated the second sentence of STND.PERF.12, which STND.PERF 1.1 extends to offloaded "
    "work, so in a performance evaluation nothing changes, and outside one a measurement of offloaded work no "
    "longer states the costs of first use, the narrowing that register entry R6.3 accepts (CS14). The tests of "
    "STND.OFFLD.27 vary the sizes of the problem and of the groups, which is how the number of tasks of device code "
    "varies, so one kernel answers to one rule on the counts that its tests run at (CS19); the permission relaxes "
    "STND.CONC.24 for device code, and asks nothing. Each is a default (GOV.19), so none raises the floor "
    "(GOV.11). Class onsets: unchanged, CSQ3. Transition (GOV.42): none. Register entry R6.3 (CS14, CS19) of "
    f"{REG}; decisions 12 and 14 of {REC}." + F.AUTHOR)


def apply_offld(root: Path, at: str) -> None:
    root = Path(root)
    F.set_body(root, "STND/OFFLD/31.md", OFFLD31_BODY, refers_to=["STND.PERF.14"])
    replace_text(root, "STND/OFFLD/27.md", OFFLD27)
    F.set_body(root, "STND/OFFLD/27.md", body_of(root, "STND/OFFLD/27.md"), refers_to=["STND.CONC.24"])
    F.check_fields(root, ["STND.OFFLD.27", "STND.OFFLD.31"])
    replace_text(root, "STND/OFFLD/_doc.md", OFFLD_DOC)
    row = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {OFFLD_READING}. |"
    F.finish(root, "STND/OFFLD", "STND.OFFLD", "1.1", "1.2", row, OFFLD_RATIONALE, at)


# ---------------------------------------------------------------- STND.MPI 1.1

MPI_DOC = [
    ("It adds to STND.CODE, HW, NUMER, and STND.VVUQ only what MPI makes necessary.",
     "It adds to STND.CODE, STND.CONC, HW, NUMER, and STND.VVUQ only what MPI makes necessary."),
    ("collective operations and their reductions (STND.MPI.17, STND.MPI.18, and STND.MPI.19);",
     "the order of collective operations (STND.MPI.17);"),
    ("threads (STND.MPI.23); and tests (STND.MPI.24 and STND.MPI.25).",
     "threads (STND.MPI.23); and the checks of MPI calls at run time (STND.MPI.25). STND.CONC holds for the "
     "processes of a parallel execution, as for every kind of concurrent task, the declaration of each result that "
     "depends on their number, reductions in a fixed order across their numbers, and tests at three or more of their "
     "numbers (STND.CONC.21, STND.CONC.22, and STND.CONC.24)."),
    ("which is the basis for the size of the variation that STND.MPI.18 declares.",
     "which is the basis for the size of the variation that STND.CONC.21 declares."),
    ("STND.MPI.18 has each result that depends on these declared, and covers runs that differ only in the items "
     "that STND.MPI.2 records,",
     "STND.CONC.21 has each result that depends on these declared, the processes being concurrent tasks under "
     "STND.CONC, and covers runs that differ only in the items that STND.MPI.2 records,"),
    ("STND.MPI.19 applies STND.VVUQ.2 to reductions across processes:",
     "STND.CONC.22 applies STND.VVUQ.2 to reductions across processes:"),
    ("that criterion governs the comparison, which STND.MPI.19 judges by identical bits,",
     "that criterion governs the comparison, which STND.CONC.22 judges by identical bits,"),
    ("Concurrent accumulate operations on one location combine in an order that varies between runs, which "
     "STND.MPI.18 declares.",
     "Concurrent accumulate operations on one location combine in an order that varies between runs, which the "
     "declaration of STND.CONC.21 states."),
    ("STND.MPI.24 runs each component on at least three numbers of processes, among them one process where the "
     "message protocol admits it,",
     "STND.CONC.24 runs each component that uses MPI on at least three numbers of processes that its message "
     "protocol admits, among them one process where the protocol admits it,"),
    ("and STND.MPI.19 replaces it with identical bits where bitwise identity across process counts is the criterion.",
     "and STND.CONC.22 replaces it with identical bits where bitwise identity across process counts is the "
     "criterion."),
]
MPI_READING = (
    "STND.MPI.18, STND.MPI.19, and STND.MPI.24 are withdrawn, their outcomes being STND.CONC.21, STND.CONC.22, and "
    "STND.CONC.24 for the processes of a parallel execution, which are concurrent tasks, and the front matter lists "
    "them as withdrawn; the Purpose names STND.CONC among the documents to which this standard adds, and cites the "
    "three provisions of STND.CONC; the Notes cite them in place of the withdrawn provisions")
MPI_RATIONALE = (
    f"Minor amendment of STND.MPI, revision 1.1, ratified by the custodian on {F.DATE}: {MPI_READING}. The change is "
    "minor under STND.IDENT.3 because it removes three provisions. Each was STND.CONC.21, STND.CONC.22, or "
    "STND.CONC.24 with processes in place of tasks: the term Concurrent task names a process, the declaration of "
    "STND.CONC.21 names the order in which values are combined, which covers a reduction and concurrent accumulate "
    "operations, the parts of STND.CONC.22 are the blocks of the problem of STND.MPI.19, and the numbers of tasks "
    "that a component admits under STND.CONC.24 are the numbers of processes that its message protocol admits, so "
    "MPI work keeps each outcome. Each provision concerned is a default (GOV.19), so none raises the floor "
    "(GOV.11). Class onsets: STND.CONC.21, STND.CONC.22, and STND.CONC.24 apply from CSQ3, as the withdrawn "
    "provisions did. The withdrawn identifiers are listed in the field withdrawn and are never given to another "
    f"provision (STND.IDENT.14). Transition (GOV.42): none. Register entry R6.3 (CS7) of {REG}; decision 11 of "
    f"{REC}." + F.AUTHOR)


def apply_mpi(root: Path, at: str) -> None:
    root = Path(root)
    F.withdraw(root, "STND/MPI", "STND.MPI", [18, 19, 24])
    replace_text(root, "STND/MPI/_doc.md", MPI_DOC)
    row = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {MPI_READING}. |"
    F.finish(root, "STND/MPI", "STND.MPI", "1.0.2", "1.1", row, MPI_RATIONALE, at)


# ---------------------------------------------------------------- STND.OMP 1.0.4

OMP_DOC = [
    ("The provisions rest on the core of OpenMP that is stable across the revisions from 5.0 to the drafts of 6.1: "
     "fork and join, worksharing, tasks, data-sharing attributes, reductions, atomics, and the memory model that 5.0 "
     "rebuilt.",
     "The provisions rest on the core of OpenMP that is stable across the recent revisions of the specification and "
     "its public drafts: fork and join, worksharing, tasks, data-sharing attributes, reductions, atomics, and the "
     "memory model that an earlier revision rebuilt."),
    ("The latest technical report toward 6.1, its second preview,",
     "The latest technical report toward the next revision, a preview,"),
    ("The drafts of 6.1 renumber the chapters of the specification,",
     "The drafts of the next revision renumber the chapters of the specification,"),
    ("18 percent of the tests of revision 5.0 for C and C++, and 2 percent of those of 5.1, passed on all five "
     "compilers tried,",
     "18 percent of the tests of one revision for C and C++, and 2 percent of those of the revision after it, passed "
     "on all five compilers tried,"),
    ("claims full support of 5.2 or 6.0,",
     "claims full support of the two latest published revisions that the research read,"),
    ("Revision 6.0 removed the features that 5.0, 5.1, and 5.2 deprecated,",
     "The latest published revision that the research read removed the features that the three revisions before it "
     "deprecated,"),
    ("6.0 also undeprecated one form of the destroy clause of the depobj construct, which 5.2 had deprecated (r1).",
     "that revision also undeprecated one form of the destroy clause of the depobj construct, which the revision "
     "before it had deprecated (r1)."),
    ("with no schedule clause, revision 6.0 behaves as if the schedule were auto, and 5.2 leaves the schedule "
     "implementation defined",
     "with no schedule clause, the latest published revision that the research read behaves as if the schedule were "
     "auto, and the revision before it leaves the schedule implementation defined"),
    ("in revision 6.0 only the entry points of tools have it,",
     "in the latest published revision that the research read only the entry points of tools have it,"),
]
OMP_READING = (
    "the Notes name the revisions of the OpenMP specification by their order, an earlier revision, the revision "
    "after it, the latest published revision that the research read, and the next revision, in place of their "
    "numbers, which ruling D1 takes out of the Notes")


def apply_omp(root: Path, at: str) -> None:
    replace_text(Path(root), "STND/OMP/_doc.md", OMP_DOC)
    row, rat = editorial(
        "STND.OMP", "1.0.4", OMP_READING,
        "each fact stays as the research recorded it, and only the way of naming a revision changes",
        f"Ruling D1 of {F.RECORD}; register entry R7.1 (CS15) of {REG}; decision 15 of {REC}.")
    F.finish(root, "STND/OMP", "STND.OMP", "1.0.3", "1.0.4", row, rat, at)
