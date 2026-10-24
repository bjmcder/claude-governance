"""Rehearsable minor amendment: STND.PROJ 1.2, the form of an authorization of a remote write.

New STND.PROJ.6 (fields) and STND.PROJ.7 (kinds of remote write), both defaults; the project
template's authorization file gains the field remote_writes. Run from harness/, so that
govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_proj_1_2.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T19:30:00+00:00"


def provision(n: int, title: str, body: str, refers_to: list[str]) -> str:
    """Return the file text of a default provision of STND.PROJ under REPRO.12 and INTPR.12."""
    refs = ", ".join(f'"{r}"' for r in refers_to)
    return "\n".join([
        "---",
        f'id: "STND.PROJ.{n}"',
        'level: "LVL2"',
        'kind: "provision"',
        f'title: "{title}"',
        'section: "Form"',
        'status: "adopted"',
        f'adopted: "{DATE}"',
        'mode: "default"',
        "binding_reason: null",
        'instantiates: ["REPRO.12", "INTPR.12"]',
        f"refers_to: [{refs}]",
        "rank: 3",
        "waivable: true",
        "defines: []",
        'checked_by: ["review"]',
        "---",
        "",
        body,
        "",
    ])


PROJ6 = provision(6, "Remote-write authorization fields", "\n".join([
    "Where an authorization covers a remote write, its instrument file SHOULD hold the fields of the table of "
    "this provision, each with a value of the form that its row gives (REPRO.12, INTPR.12).",
    "",
    "| Field | Value |",
    "| --- | --- |",
    "| status | `draft` until the human owner grants the authorization, `adopted` while it is granted, and "
    "`retired` once it is revoked or lapses |",
    "| grantor | The role label of the human owner |",
    "| recorded | The date of the grant, as an ISO 8601 date |",
    "| expires | The time at which the authorization lapses, as an ISO 8601 time with its UTC offset, or `until "
    "revoked` where the duration that the human owner states ends only with a revocation |",
    "| standing | `true` for a standing authorization, and `false` for one per action |",
    "| delegable_to | A list of the roles of agents, or the agents, to which the authorization extends "
    "(GUARD.12) |",
    "| remote_writes | A list of one object per destination, with `destination`, the address by which the "
    "write reaches the destination, in full and without a credential; `kinds`, the kinds of write of the table "
    "of STND.PROJ.7 that the authorization covers there; `branches`, the name of each branch that the kind "
    "commit covers there, or an empty list where the kinds omit commit; and `provisioned`, `true` where the "
    "human owner records the destination as part of the provisioned environment and as readable only by those "
    "whom the threat model trusts, and otherwise `false` |",
]), ["STND.PROJ.7", "GUARD.12"])

PROJ7 = provision(7, "Kinds of remote write", "\n".join([
    "An authorization file SHOULD name each kind of remote write that it covers by a word of the table of this "
    "provision, whose last column marks the kinds whose effect is irrevocable (REPRO.12, INTPR.12, GUARD.11).",
    "",
    "| Kind | Remote write | Effect irrevocable |",
    "| --- | --- | --- |",
    "| commit | Adding commits to a named branch of a remote repository whose update neither publishes nor "
    "deploys, without rewriting or deleting history, a branch, or a tag | At a destination not recorded as "
    "provisioned |",
    "| post | Adding an issue, a comment, or a review to a remote tracker, without editing, closing, or deleting "
    "one | At a destination not recorded as provisioned |",
    "| publish | Publication or release, including an update of a branch whose update publishes or deploys | "
    "Always |",
    "| transmit | Transmission of data beyond the provisioned environment, other than publication or release "
    "| Always |",
    "| other | A remote write of another kind, which the scope of the authorization describes | As the scope "
    "states, and always at a destination not recorded as provisioned |",
]), ["GUARD.11"])

PURPOSE_OLD = "STND.PROJ.4, on the form of the files, is a default (GOV.19)."
PURPOSE_NEW = ("STND.PROJ.4, on the form of the files, and STND.PROJ.6 and STND.PROJ.7, on the form of an "
               "authorization of a remote write and its kinds, are defaults (GOV.19).")

NOTES_ANCHOR = "the proposal asks for no decision that LVL0 does not assign (STND.DRAFT.42)."
NOTES_NEW = NOTES_ANCHOR + "\n\n" + (
    "STND.PROJ.6 and STND.PROJ.7 give an authorization of a remote write a form that a reader and a harness "
    "decide alike, so that a derived configuration is able to let a write that the authorization names by "
    "destination and kind proceed without referral (STND.HARN.18, STND.HARN.29). A destination is named by its "
    "whole address, as in `https://example.org/team/work` for a repository and its tracker, and a write matches "
    "it only as a whole, so that an address that merely begins or ends like it is not covered. The branches of "
    "the kind commit are named for the same reason: STND.PROJ.3 proposes commits only to branches other than "
    "release branches and branches whose update publishes or deploys, and a list of names is what a "
    "configuration is able to compare. Whether the update of a branch publishes or deploys is the human owner's "
    "record, not something a configuration is able to see; a commit to such a branch is of the kind publish, "
    "which GUARD.11 authorizes only per action. An address carries no credential, because delegating access is "
    "the human owner's and a record holds none (AGENT.45, PRIME.10). The field `provisioned` records the "
    "judgment that STND.PROJ.3 already asks of the human owner for a private remote repository; a write to a "
    "destination outside the provisioned environment is a transmission beyond it, which GUARD.11 authorizes only "
    "per action, so the table of STND.PROJ.7 marks every kind irrevocable there. Publication and release are "
    "irrevocable wherever they go (GUARD.11). The marks restate no rule: they apply GUARD.11 to each kind, and a "
    "standing authorization of a marked kind has no effect (GUARD.11, STND.HARN.29). The field `delegable_to` "
    "states the extension that STND.PROJ.3 proposes for each authorization, since an authorization reaches a "
    "directed agent only where it says so (GUARD.12). The field `expires` holds a time, which a harness compares "
    "with the time of each write, or `until revoked`, where the duration that GUARD.10 asks the human owner to "
    "state ends only with a revocation; a condition of lapse in the scope, such as a repository that stops "
    "meeting the human owner's record, is not something a harness is able to test, and a time stated with it "
    "bounds the authorization for a harness. The kind other keeps the list closed while letting an authorization "
    "cover a write that no other row names; a derived configuration that does not know a kind refers its "
    "writes, which STND.HARN.18 allows. STND.PROJ.6 and STND.PROJ.7 are defaults with the onset of REPRO.12 and "
    "INTPR.12 under STND.CLASS.10: they apply from CSQ3, and work of CSQ4 may keep its authorizations in another "
    "form, whose remote writes a derived configuration then refers. Neither raises the floor (GOV.11): GUARD.10 "
    "already asks that an authorization name its class of actions, its scope, and its duration, and GUARD.12 "
    "its extension, and the fields state those for a remote write at the cost of one record.")

ROW_READING = ("new STND.PROJ.6 gives the fields of an authorization file that covers a remote write (status, "
               "grantor, date recorded, expiry as a time with its UTC offset or until revoked, standing or per "
               "action, the roles or agents to which it extends, and one entry per destination naming its whole "
               "address without a credential, its kinds of write, the branches of a commit, and whether the "
               "human owner records it as provisioned), and new STND.PROJ.7 the closed kinds commit, post, "
               "publish, transmit, and other, a commit reaching only branches whose update neither publishes nor "
               "deploys, and marks publication, release, transmission, and every kind at a destination not "
               "recorded as provisioned as irrevocable (GUARD.11); both are defaults; the authorization file of "
               "the project template gains the field remote_writes")
ROW = f"| 1.2 | {DATE} | Minor amendment (GOV.41): {ROW_READING}. |"

TEMPLATE = "_PROJECT/NAME/AUTH/1.md"
TEMPLATE_EDITS = [
    ('spending_envelope: ""\n---', 'spending_envelope: ""\nremote_writes: []\n---'),
    ("Purpose of the authorization.",
     "Purpose of the authorization.\n\nFill-in guidance: for a remote write, `expires` is a time with its UTC "
     "offset or `until revoked`, `delegable_to` lists the roles or agents to which the authorization extends, "
     "and each entry of `remote_writes` is an object with the fields `destination`, `kinds`, `branches`, and "
     "`provisioned` (STND.PROJ.6, STND.PROJ.7)."),
]

RATIONALE = (f"Minor amendment of STND.PROJ, revision 1.2, ratified by the custodian on {DATE}: {ROW_READING}. "
             "The change is minor because it adds two defaults and a template field; no obligation of LVL0 "
             "changes, and neither default raises the floor, since GUARD.10 already asks an authorization to name "
             "its class of actions, scope, and duration, and GUARD.12 its extension (GOV.11). It closes the open "
             "item of STND.HARN.18 together with STND.HARN 1.2. Transition (GOV.42): an authorization recorded "
             "before this revision keeps its effect as its text says; a derived configuration refers its remote "
             "writes until it is recorded again in the form of STND.PROJ.6. Review of STND.HARN.28 by the command "
             "pairs and by reading; cold, pair, and security reviews in review-records/round-2026-10-24/harn-auth/."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/PROJ/6.md").write_text(PROJ6, encoding="utf-8")
    (root / "STND/PROJ/7.md").write_text(PROJ7, encoding="utf-8")
    replace_text(root, "STND/PROJ/_doc.md", [(PURPOSE_OLD, PURPOSE_NEW), (NOTES_ANCHOR, NOTES_NEW)])
    replace_text(root, TEMPLATE, TEMPLATE_EDITS)
    raise_revision(root, "STND/PROJ", "1.1", "1.2", ROW)
    tree = read_tree(root)
    for rel, text in rewrite_sections(tree, Corpus(load_entries(tree)), ["STND.PROJ"]).items():
        (root / rel).write_text(text, encoding="utf-8")
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.PROJ"],
                                          scope=["STND/PROJ"], rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.PROJ 1.2")
