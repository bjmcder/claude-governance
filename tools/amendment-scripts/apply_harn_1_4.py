"""Rehearsable minor amendment: STND.HARN 1.4, round of 2026-10-26 (decisions 3 to 6).

One transaction.
- Decision 5: STND.HARN.18 to STND.HARN.23, STND.HARN.29, and STND.HARN.30 are withdrawn, with the terms Derived
  configuration and Refer and the Notes on them; the harness derives no configuration (unit 0018).
- Decision 3: STND.HARN.9 compares each pin in force, a new term, so that a later transaction whose scope holds
  each path of an earlier one ends the earlier pin.
- Decision 4: STND.HARN.7 lets a scope name a ".md" file, so that README.md and STND/_doc.md can be pinned
  alone; new STND.HARN.31 makes a ".md" file that no scope reaches a FAIL.
- Unit 0017, L5: new STND.HARN.32 makes a checked_by key that names no check a FAIL.
- Decision 6: the revision row records the end of the transition of ledger entry 53.
Runs after the amendments that drop the citations of the withdrawn provisions (STND.DFLT, STND.PROJ, HW.GPU,
HW.QPU). Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding those amendments> ../tools/amendment-scripts/apply_harn_1_4.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:04+00:00"

WITHDRAWN = [18, 19, 20, 21, 22, 23, 29, 30]

FRONT = [
    ('instantiates: ["GOV.26", "GOV.35", "GOV.36", "GOV.37", "GOV.38", "GOV.39", "GOV.48", "QA.7"]\n'
     "rank: null\nwaivable: false\n---",
     'instantiates: ["GOV.26", "GOV.35", "GOV.36", "GOV.37", "GOV.38", "GOV.39", "QA.7"]\n'
     "rank: null\nwaivable: false\nwithdrawn: [" + ", ".join(f'"STND.HARN.{n}"' for n in WITHDRAWN) + "]\n---"),
]

TERMS = [
    ('| Content hash | The digest of the UTF-8 lines "path:digest", one per ".md" file under a "scope", with "/"-separated '
     'paths from the corpus root, ordered by scope path, then part by part in code-point order,',
     '| Content hash | The digest of the UTF-8 lines "path:digest", one for each ".md" file that a "scope" reaches, '
     'with "/"-separated paths from the corpus root, ordered by the first, in code-point order, of the paths of the '
     '"scope" that reach the file, then part by part in code-point order,'),
    ("| Derived configuration | An agent's environment configuration that a harness derives. |\n", ""),
    ("| Item | A document, register, provision, knowledge entry, Lexicon term, or tag. |\n",
     "| Item | A document, register, provision, knowledge entry, Lexicon term, or tag. |\n"
     '| Pin in force | A governance-ledger transaction with a nonempty "scope", for which no later governance-ledger '
     'transaction has a "scope" that reaches each path of the earlier "scope". |\n'),
    ("| Rehearsal |",
     '| Reach | A "scope" reaches a path where one of its paths is that path or a directory above it. |\n'
     "| Rehearsal |"),
    ("| Refer | The response that holds an action until the human owner decides it. |\n", ""),
]

NOTES_1 = [
    ("Assured work, checkpoint, destructive action, session, signer register, and working bounds have the meanings "
     "of STND.DFLT.",
     "Signer register has the meaning of STND.DFLT."),
    (" Work report has the meaning it has in the agent practice profile (AGENT).", ""),
    ("The code accepts type configure on adoption.",
     "A transaction of type configure records a configuration for STND.DFLT.22."),
]

NOTES_2 = (
    "A later transaction whose \"scope\" reaches each path of an "
    "earlier one ends the earlier pin, so that a scope is widened by one transaction over the wider paths "
    "(STND.HARN.9). A transaction over part of a pinned scope ends no pin, so the wider pin goes stale once that "
    "part changes, and a transaction over the whole wider scope is what records the change. Two scopes that share a "
    "path, neither reaching each path of the other, both stay in force, and a change of the shared path stales both until one "
    "transaction reaches both. A transaction over several paths pins them as one "
    "content hash, so each later change of one of them takes a transaction over all of them, while a path pinned "
    "by a transaction of its own changes on its own. A \"scope\" names a directory or a \".md\" file, so "
    "that a file directly under a directory whose subdirectories other transactions pin, and the \"README.md\" of the "
    "corpus root, are each pinned without the files beside them (STND.HARN.7). STND.HARN.31 makes a \".md\" file "
    "that no transaction pins a FAIL, because GOV.36 makes a change made outside the ledger a defect and "
    "STND.HARN.9 sees only the scopes that transactions name. It reaches each \".md\" file, including the "
    "\"README.md\" files and the files of template directories that STND.HARN.5 does not read as items, because the "
    "ledger pins files, not items. It binds, because it instantiates GOV.36, and raises "
    "no floor (GOV.11): it asks of a harness one comparison of the paths of the corpus with the scopes of the "
    "ledger; it asks no decision of the human owner and no new act of a project, and of the custodians only the "
    "transactions that pin the files now outside every scope, because the transaction that GOV.36 already asks for "
    "each change records a scope that reaches the file, as an adoption records the directory of the document it "
    "adopts. STND.HARN.32 binds, because it instantiates GOV.37, and raises no floor "
    "(GOV.11): a key in the field \"checked_by\" identifies a check, and one that names no check resolves to "
    "nothing; the provision asks of a harness one comparison of field values with its own keys, and nothing of the "
    "human owner or of a project. This standard sets no form for a configuration of an agent's environment; "
    "STND.DFLT.22 states when such a configuration displaces a provision.")

HARN7 = [('"scope" (corpus directories whose content it pins)',
          '"scope" (corpus directories and ".md" files whose content it pins)')]

HARN9 = [('Where the content hash of a "scope" differs from the "corpus_hash" of the latest governance-ledger '
          'transaction with that "scope", a harness SHALL report FAIL (GOV.36).',
          'Where the content hash of the "scope" of a pin in force differs from its "corpus_hash", a harness SHALL '
          'report FAIL (GOV.36).')]


def provision(n: int, title: str, section: str, instantiates: list[str], checked_by: list[str], body: str) -> str:
    quoted = ", ".join(f'"{i}"' for i in instantiates)
    keys = ", ".join(f'"{k}"' for k in checked_by)
    return "\n".join([
        "---", f'id: "STND.HARN.{n}"', 'level: "LVL2"', 'kind: "provision"', f'title: "{title}"',
        f'section: "{section}"', 'status: "adopted"', f'adopted: "{DATE}"', 'mode: "binding"',
        "binding_reason: null", f"instantiates: [{quoted}]", "refers_to: []", "rank: null", "waivable: false",
        "defines: []", f"checked_by: [{keys}]", "---", "", body, ""])


HARN31 = provision(
    31, "Unpinned files", "Ledger", ["GOV.36"], ["unpinned"],
    'Where a ".md" file of the corpus is reached by no "scope" of a governance-ledger transaction, a harness SHALL '
    "report FAIL for that file (GOV.36).")

HARN32 = provision(
    32, "Known check keys", "Checks", ["GOV.37"], ["checked-by"],
    'Where the field "checked_by" of a provision names a key that is neither "review" nor a key of a check that the '
    "harness makes, a harness SHALL report FAIL (GOV.37).")

READING = (
    "STND.HARN.18 to STND.HARN.23, STND.HARN.29, and STND.HARN.30 are withdrawn with the terms Derived configuration "
    "and Refer, and this standard sets no form for a configuration of an agent's environment; STND.HARN.7: a "
    "\"scope\" names directories and \".md\" files; STND.HARN.9 compares each pin in force, a new term, so that a "
    "later transaction whose \"scope\" reaches each path of an earlier one ends the earlier pin, with the new term "
    "Reach; the term Content hash counts each \".md\" file that a \"scope\" reaches once, under the first, in "
    "code-point order, of its paths that reach it; new STND.HARN.31: FAIL for a \".md\" file that no \"scope\" of the governance ledger reaches; new STND.HARN.32: FAIL for a "
    "\"checked_by\" key that names no check of the harness")
TRANSITION = ("the transition of ledger entry 53 ends, for STND.HARN.26 to STND.HARN.28 because the harness "
              "implements them, and for STND.HARN.18 because it is withdrawn; a \".md\" file that no \"scope\" "
              "reaches is no defect until the transactions that pin KNOW, TAG, _PROJECT, STND/_doc.md, and README.md "
              "are recorded")
ROW = f"| 1.4 | {DATE} | Minor amendment (GOV.41): {READING}. Transition (GOV.42): {TRANSITION}. |"

RATIONALE = (
    f"Minor amendment of STND.HARN, revision 1.4, ratified by the custodian on {DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it removes the obligations of the withdrawn provisions, alters what STND.HARN.9 "
    "compares, and adds two obligations on a harness. The withdrawn provisions governed only a configuration that a "
    "harness derives, and the harness of this corpus derives none since unit 0018; STND.DFLT.22 still states when "
    "such a configuration displaces a provision, and STND.PROJ.6 and STND.PROJ.7 keep the form of a written "
    "authorization of a remote write. STND.HARN.9 compares the same pins as before wherever no "
    "scope of a later transaction reaches each path of a different earlier scope, which holds for every pin of this "
    "ledger. The transactions that pin KNOW, TAG, _PROJECT, STND/_doc.md, and "
    "README.md, each with its own scope, follow this amendment, since STND.HARN.7 first admits a file as a scope, "
    "and the transition covers those files until they are recorded. "
    "The floor arguments of STND.HARN.31 and STND.HARN.32 are in the Notes. "
    f"Transition (GOV.42): {TRANSITION}. Decisions 3 to 6 of "
    "review-records/round-2026-10-26/decisions.md; records harness/records/units/0016-ledger-fixes.md, "
    "harness/records/units/0017-checks-fixes.md, and harness/records/units/0018-drop-environment.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    for n in WITHDRAWN:
        (root / f"STND/HARN/{n}.md").unlink()
    doc = root / "STND/HARN/_doc.md"
    old_2 = next(line for line in doc.read_text(encoding="utf-8").splitlines()
                 if line.startswith("STND.HARN.29 states when a derived configuration"))
    replace_text(root, "STND/HARN/_doc.md", [*FRONT, *TERMS, *NOTES_1, (old_2, NOTES_2)])
    replace_text(root, "STND/HARN/7.md", HARN7)
    replace_text(root, "STND/HARN/9.md", HARN9)
    (root / "STND/HARN/31.md").write_text(HARN31, encoding="utf-8")
    (root / "STND/HARN/32.md").write_text(HARN32, encoding="utf-8")
    new = ["STND.HARN.31", "STND.HARN.32"]
    res = B.derive_fields(root, new)
    for ident in new:
        if res[ident].unresolved or res[ident].waivable:
            raise ValueError(f"{ident}: {res[ident]}")
    raise_revision(root, "STND/HARN", "1.3", "1.4", ROW)
    B.write_references(root, ["STND.HARN"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.HARN"], scope=["STND/HARN"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.HARN 1.4")
