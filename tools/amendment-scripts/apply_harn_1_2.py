"""Rehearsable minor amendment: STND.HARN 1.2, the authorizations a derived configuration honors.

New binding STND.HARN.29; the transition of ledger entry 53 for STND.HARN.18 ends once a reviewed harness that
implements it is installed. Needs STND.PROJ 1.2 (apply_proj_1_2.py) first. Run from harness/, so that govharness
imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24_harn.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T19:31:00+00:00"

HARN29 = "\n".join([
    "---",
    'id: "STND.HARN.29"',
    'level: "LVL2"',
    'kind: "provision"',
    'title: "Authorizations a configuration honors"',
    'section: "Environment"',
    'status: "adopted"',
    f'adopted: "{DATE}"',
    'mode: "binding"',
    "binding_reason: null",
    'instantiates: ["GOV.48", "GUARD.2", "GUARD.11", "GUARD.12"]',
    'refers_to: ["STND.HARN.18", "STND.PROJ.6", "STND.PROJ.7", "STND.HARN.11"]',
    "rank: 1",
    "waivable: false",
    "defines: []",
    'checked_by: ["review"]',
    "---",
    "",
    "Where a derived configuration lets a remote write proceed without referral under STND.HARN.18, it SHALL "
    "rely only on an authorization in an instrument file of the form of STND.PROJ.6 that meets each row of the "
    "table of this provision at the derivation of the configuration, and the row Dates also at the time of the write "
    "(GOV.48, GUARD.2, GUARD.11, GUARD.12). A derived configuration SHALL compare the destination, kind, and "
    "branches of a remote write with those that the authorization names as whole values, without patterns "
    "(GUARD.2).",
    "",
    "| Test | The authorization meets it when |",
    "| --- | --- |",
    "| Status | Its status is adopted |",
    "| Grantor | Its grantor is the human owner |",
    "| Extension | Its field delegable_to names the role or agent for which the configuration is derived |",
    "| Record | The chain of the ledger of the corpus that holds the file is intact; the latest transaction of that "
    "ledger whose scope holds the file is of type authorize, names the human owner as actor and the authorization "
    "among its targets, and pins the file's current content; and no later transaction of type revoke names it |",
    "| Signature | Where the work is assured or the corpus holds a signer register, that transaction carries a "
    "signature that STND.HARN.11 accepts |",
    "| Dates | Its date recorded is no later than that transaction and than the derivation, and its expiry, "
    "where it has one, is later than the write |",
    "| Standing | It is standing, and the table of STND.PROJ.7 does not mark irrevocable the kind of the remote "
    "write at the destination of the entry that names it; each entry and kind is tested apart from the others |",
    "| Form | Each field holds a value of the form that STND.PROJ.6 gives |",
    "",
])

NOTES_ANCHOR = "Scripts named in STND.DRAFT and STND.IDENT stay entry points until those standards cite " \
               "`python -m govharness` (GOV.42)."
# The anchor sentence is stale: STND.DRAFT 1.2.1 and STND.IDENT 1.3.2 already name the commands of the harness
# package. It is replaced by one that cites a provision of STND.IDENT, so that References lists it (STND.DRAFT.34).
NOTES_IDENT = ("STND.DRAFT and STND.IDENT name the commands of the harness package that report their checks, among "
               "them the revision checks, which read the revision history of each adopted document (STND.IDENT.6).")
NOTES_NEW = NOTES_IDENT + "\n\n" + (
    "STND.HARN.29 states when a derived configuration relies on an authorization under the row remote-write "
    "of STND.HARN.18; its two sentences are a bundle that is never applied apart. Its rows are tested when the "
    "configuration is derived, and the expiry again at each write, because the configuration is installed where "
    "the agent is unable to alter it and reads no ledger. A revocation therefore reaches a configuration only "
    "when the configuration is derived again and installed; until then, a derivation that still names the "
    "revoked authorization stops with the reason, one that no longer names it differs from the installed "
    "configuration, which the check of STND.HARN.21 reports, and the coverage report of STND.HARN.19 states the "
    "interval. "
    "An authorization per action is never relied on: a configuration that lets one write pass is unable to tell "
    "that write from a repetition of it, so the write is referred and the human owner's answer to the referral "
    "confirms it (PRIME.7, PRIME.14). A standing authorization of an irrevocable remote write has no effect "
    "(GUARD.11), and STND.HARN.29 relies on none. GUARD.11 voids only the irrevocable write, so the row Standing "
    "is tested for each entry and kind of write: an irrevocable one opens nothing and its writes are referred, "
    "and the other entries of the same authorization stand. A malformed entry fails the row Form, and nothing of "
    "that authorization is relied on, because the record then does not state what the human owner granted. The "
    "row Extension applies GUARD.12: an authorization "
    "reaches a directed agent only where it says so, and a configuration is derived for one role or agent. The "
    "row Record is narrower than STND.DFLT.23, which for work that is not assured also accepts an agent's own "
    "entry of a grant (STND.DFLT.17): an agent is able to append such an entry, so a configuration that relied "
    "on it would let an agent open its own writes (PRIME.7), and the write is referred instead, which STND.HARN.18 "
    "allows. The row Signature asks for a signature wherever a signer register exists, since an unsigned entry is "
    "then one that anyone with write access to the ledger is able to make. Whole values are compared because a "
    "pattern, or a comparison of a prefix, admits a destination that the human owner never named; a write whose "
    "destination a configuration is unable to read from the action itself is referred. A configuration that "
    "refers a write which an authorization in force names still meets STND.HARN.18, and its coverage report "
    "states each kind of write that it refers so (STND.HARN.19). STND.HARN.29 binds, because it instantiates "
    "GOV.48, GUARD.2, GUARD.11, and GUARD.12, and raises no floor (GOV.11): it asks of a harness only the reliance on an "
    "authorization as the record states it, entry by entry, which GUARD.2 and GUARD.11 already ask of an agent, "
    "at the cost of wording and "
    "of the checks the harness makes: reading each named authorization file and the ledger that pins it, "
    "verifying signatures where they are required, and comparing each remote write with the authorizations "
    "relied on.")

ROW_READING = ("new STND.HARN.29: a derived configuration that lets a remote write proceed without referral "
               "under STND.HARN.18 relies only on a standing authorization in the form of STND.PROJ.6 that, when "
               "the configuration is derived, is adopted, granted by the human owner, extends to the role or "
               "agent the configuration is derived for (GUARD.12), is pinned in its current content by an "
               "authorize transaction of the human owner in an intact ledger and revoked by no later "
               "transaction, is signed where the work is assured or a signer register exists, was recorded no "
               "later than its transaction and than the derivation, and whose expiry, where it has one, is later than the write; an entry "
               "of a kind that STND.PROJ.7 marks irrevocable at its destination opens nothing (GUARD.11), each "
               "entry and kind tested apart, so that the other entries of the authorization stand; destination, "
               "kind, and branches are compared as whole values; the Notes cite STND.IDENT.6 in place of a stale "
               "sentence on scripts; the transition of ledger entry 53 for "
               "STND.HARN.18 ends once a reviewed harness that implements STND.HARN.29 is installed")
ROW = f"| 1.2 | {DATE} | Minor amendment (GOV.41): {ROW_READING}. |"

RATIONALE = (f"Minor amendment of STND.HARN, revision 1.2, ratified by the custodian on {DATE}: {ROW_READING}. "
             "The change is minor because it adds an obligation on a harness that derives a configuration; it "
             "raises no floor (GOV.11), since it asks of a harness only what GUARD.2, GUARD.11, and GUARD.12 ask "
             "of an agent; the custodian rules at ratification that it raises no floor. Transition (GOV.42): the transition "
             "that ledger entry 53 set for STND.HARN.18, under which a derived configuration that refers every "
             "remote write meets STND.HARN.18, ends on the day a harness that implements STND.HARN.29, reviewed "
             "under QA.8, is installed and its configure entry records it (STND.HARN.20); until then a derived "
             "configuration that refers every remote write meets STND.HARN.18, as entry 53 states, and a "
             "configuration derived by an earlier harness keeps referring every remote write until it is derived "
             "again. This amendment does not decide whether the transition of entry 53 for STND.HARN.26 to "
             "STND.HARN.28 has ended; the harness implements them by the checks m.1 and m.2 and the command "
             "pairs, and the custodian may record its end. Review of STND.HARN.28 by the command pairs and by "
             "reading; cold, pair, and security reviews in review-records/round-2026-10-24/harn-auth/."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/HARN/29.md").write_text(HARN29, encoding="utf-8")
    replace_text(root, "STND/HARN/_doc.md", [(NOTES_ANCHOR, NOTES_NEW)])
    raise_revision(root, "STND/HARN", "1.1", "1.2", ROW)
    tree = read_tree(root)
    for rel, text in rewrite_sections(tree, Corpus(load_entries(tree)), ["STND.HARN"]).items():
        (root / rel).write_text(text, encoding="utf-8")
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.HARN"], scope=["STND/HARN"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.HARN 1.2")
