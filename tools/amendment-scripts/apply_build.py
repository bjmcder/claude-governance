"""Rehearsable adoption script: STND.BUILD 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_build as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.BUILD, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard hold the practice of build systems for every build tool and language, agnostic of"
    " build tool, compiler, and platform and timeless, with CMake, the Autotools, and Makefiles as evidence and not as"
    " subjects, restating nothing that REPRO, STND.DEPS, STND.CODE, HW, STND.OFFLD, STND.OMP, or the language standards"
    " hold: 26 provisions, all defaults, build tool, language, compiler, platform, and vendor agnostic. Every input of"
    " a build step declared and derived from the source where its source names it, outputs of incremental and parallel"
    " builds the same as those of a clean serial build within declared variation, generated files produced from their"
    " generators and checked where the version history holds them, builds written outside the source tree, and"
    " fetching done before the build with a missing input stopping it (STND.BUILD.1 to STND.BUILD.7); detected"
    " properties required or recorded and settable, cross builds configured without running target code and with"
    " tools for the build host built apart, and the targets of device code stated (STND.BUILD.8 to STND.BUILD.10);"
    " each execution setting able to change a result stated in one place for each compilation unit and each link"
    " step, warnings failing the checks of a change and failing a build from a release archive only under a checked"
    " toolchain, and checking builds kept apart from reporting builds (STND.BUILD.11 to STND.BUILD.13); embedded"
    " instants, the order of inputs, locale and time zone, embedded paths, and randomness either fixed or declared as"
    " variation, and two clean builds and the incremental and parallel builds compared at each release (STND.BUILD.14"
    " to STND.BUILD.19); release archives produced from the revision that they name with their files not in the"
    " revision produced again and compared, build scripts held and reviewed as code, and test data kept from the steps"
    " that produce delivered outputs (STND.BUILD.20 to STND.BUILD.22); build caches keyed on every input, with no"
    " output of a step that reads a secret, written only by checked builds, and kept as evidence when an output that"
    " they served is found wrong (STND.BUILD.23 and STND.BUILD.24); and one build record written with the outputs of"
    " each reporting build, with no secret in it, and the build configurations under check stated (STND.BUILD.25 and"
    " STND.BUILD.26). No provision binds and none raises the floor (GOV.11): each asks only what REPRO, DSGN, SIMPL,"
    " RSRC, INTPR, VV, QA, or HW.5 already ask, at the cost of wording, a setting, a check, or one record, and the"
    " verification of fetched components, the authorization of network access, and the exclusion of secrets from"
    " records already bind through STND.DEPS.6, PRIME.7, and PRIME.10. The steps that build software are governed by"
    " this standard, and the standard for computational workflows governs the publication, retry, restart, storage,"
    " and resumption around them. Transition (GOV.42): none, because no project instrument cites a draft of it. Review"
    " of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and a verification of each"
    " revised draft; record review-records/round-2026-10-24/build/. The review found no conflict among the listed"
    " pairs and no matter left without an owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_BUILD:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/BUILD"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
