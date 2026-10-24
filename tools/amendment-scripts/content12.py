"""STND.VVUQ 1.3 (minor amendment): declared run-to-run variation is no defect, and determinism is an
option, from the custodian's direction of 2026-10-24 for every parallel execution model."""
from content3 import P

DATE = "2026-10-24"

VVUQ82 = P(82, "Declared variation in comparisons", "Comparison tiers", """
Where every source of a difference between compared results is stated in the declaration of run-to-run variation of a compared execution path (HW.12) or in the records of the compared runs, and the difference lies within the agreement that the acceptance criterion of the comparison fixed under STND.VVUQ.1 before the comparison, the difference SHOULD NOT be treated as a defect (REPRO.3, VV.3). Other than where an acceptance criterion of the work, or a provision that applies at its consequence class, requires bitwise identity, a change SHOULD NOT be made only to remove such a difference (REPRO.3, RSRC.4). An execution path MAY offer a mode without run-to-run variation (REPRO.3).
""", ["REPRO.3", "VV.3", "RSRC.4"], refs=["HW.12", "STND.VVUQ.1"])

VVUQ83 = P(83, "Agent conduct toward known variation", "Comparison tiers", """
Where every source of a difference between compared results is stated in the record of the work, and the difference lies within the agreement that the work fixed for the comparison, an agent SHALL NOT, on its own initiative, change the work only to remove that difference (GOV.11, GOV.48). Where the work states no acceptance criterion of bitwise identity, an agent SHALL NOT, on its own initiative, extend a unit of work only to make results identical across numbers of threads, numbers of processes, or hardware models (GOV.11, GOV.48). An agent SHALL state in its work report each difference that it leaves under this provision, with its source (PRIME.2, GOV.48).
""", ["GOV.11", "GOV.48", "PRIME.2"], mode="binding")

ANCHOR = "A result judged against a tolerance loosened after the result was seen remains unverified (QA.12)."
NOTE = (" The custodian directs, for every parallel execution model, that strict determinism be an option where it is feasible and not a requirement unless the acceptance criterion of the work or its consequence class demands it. "
        "A difference whose every source is declared under HW.12 or recorded with the compared runs, and which lies within the agreement that the acceptance criterion fixed before the comparison, is therefore no defect (STND.VVUQ.82); known jitter between thread counts, process counts, or a processor and an accelerator is settled by that declaration or record and the tier of STND.VVUQ.1. A difference beyond that agreement, or one that remains with the declared sources held fixed, falls outside STND.VVUQ.82, and loosening its tolerance is the decision that STND.VVUQ.8 governs. STND.VVUQ.83 holds agents to the same direction at every class, CSQ4 included, where the other provisions of this standard may be omitted: it forbids only work that an agent starts on its own initiative to remove such a difference, and costs one line of its work report, so that, as the custodian ruled at ratification, it raises no floor (GOV.11, PRIN.10). As the custodian distinguishes, a true race condition is a correctness defect, which DSGN.15 and HW.11 govern and which neither provision excuses, while variation from an order of launch, scheduling, or gathering that is otherwise safe is not of itself a defect. "
        "A deterministic mode is permitted as an option, and bitwise identity, where an acceptance criterion asks for it, is reached as STND.VVUQ.2 states.")
PURPOSE_OLD = "Every provision, its numbers included, is a default (GOV.19) and a recommendation,"
PURPOSE_NEW = "STND.VVUQ.83 instantiates GOV.11 and GOV.48 and is binding on agents at every class; every other provision, its numbers included, is a default (GOV.19) and a recommendation,"
VVUQ_DOC_EDITS = [(ANCHOR, ANCHOR + NOTE), (PURPOSE_OLD, PURPOSE_NEW)]

VVUQ_ROW = ("| 1.3 | " + DATE + " | Minor amendment (GOV.41): new STND.VVUQ.82 treats a difference between compared results that declared run-to-run variation explains, within the agreement of its tier, as no defect; discourages changes made only to remove it unless an acceptance criterion or the consequence class requires bitwise identity; and admits a deterministic mode as an option; new STND.VVUQ.83, binding on agents (GOV.48), forbids an agent to change or extend the work on its own initiative only to remove such a difference, and has it state each difference it leaves. |")
