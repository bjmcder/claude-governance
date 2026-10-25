"""Rehearsable minor amendment: STND.HARN 1.3, unsigned reliance (unit 0010) and the expiry horizon (unit 0012).

One transaction. The row Signature of STND.HARN.29 is brought into agreement with the merged code of unit 0010
(derive/environment/authorizations.py, cli/environment.py): a signature is also required where the ledger shows
a signer register that the corpus lacks, or an anchor file exists. New binding STND.HARN.30 has a configuration
rely on an authorization that no signature can show to be the human owner's only once the human owner accepts it
unsigned at the derivation, and has the coverage report name it; its first sentence carries no trailing condition
(second verification of unit 0010, L1). The Notes give the reasons, the floor arguments, and unit 0012's reason
for an expiry. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_harn_1_3.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:03:00+00:00"

ROW29 = [(
    "| Signature | Where the work is assured or the corpus holds a signer register, that transaction carries a "
    "signature that STND.HARN.11 accepts |",
    "| Signature | Where the work is assured, the corpus holds a signer register, an entry of its ledger carries a "
    "signature or has a scope at or under the directory of the signer register, or an anchor file exists, the "
    "transaction of the row Record carries a signature that STND.HARN.11 accepts |",
)]

HARN30 = "\n".join([
    "---",
    'id: "STND.HARN.30"',
    'level: "LVL2"',
    'kind: "provision"',
    'title: "Unsigned reliance accepted"',
    'section: "Environment"',
    'status: "adopted"',
    f'adopted: "{DATE}"',
    'mode: "binding"',
    "binding_reason: null",
    'instantiates: ["GUARD.10", "PRIME.7"]',
    'refers_to: ["STND.HARN.29", "STND.HARN.19"]',
    "rank: null",
    "waivable: false",
    "defines: []",
    'checked_by: ["review"]',
    "---",
    "",
    "Where the row Signature of STND.HARN.29 requires no signature, a derived configuration SHALL rely under "
    "STND.HARN.29 only on an authorization that the human owner accepts unsigned at the derivation of the "
    "configuration (GUARD.10, PRIME.7). Where a derived configuration relies on an authorization that the human "
    "owner accepted unsigned, the coverage report of that configuration SHALL name the authorization (STND.HARN.19).",
    "",
])

EXPIRY_OLD = "and the coverage report of STND.HARN.19 states the interval."
EXPIRY_NEW = EXPIRY_OLD + (
    " Only an expiry bounds that interval, since the row Dates tests it again at each write, and an authorization "
    "that lapses only when revoked leaves the interval unbounded. A harness that refuses at the derivation an "
    "authorization whose expiry lies beyond a horizon that the harness states, or that lapses only when revoked, "
    "still meets STND.HARN.29, because the writes of that authorization are then referred, which STND.HARN.18 "
    "allows.")

SIGNATURE_OLD = ("The row Signature asks for a signature wherever a signer register exists, since an unsigned entry is "
                 "then one that anyone with write access to the ledger is able to make.")
SIGNATURE_NEW = (
    "The row Signature asks for a signature wherever a signer register exists or existed, since an unsigned entry "
    "is then one that anyone with write access to the ledger is able to make. An entry that carries a signature, or "
    "whose scope lies at or under the directory of the register, shows that a register was founded, so a register "
    "that the ledger records and the corpus lacks was removed, and its absence lifts no signature. An agent that "
    "rewrites the ledger from its first entry on, with the chain recomputed, removes that trace as well; the anchor "
    "file lies outside the agent's reach, so where an anchor file exists the signature stays required although the "
    "register is missing. A ledger that a harness is unable to read for that trace counts as one, which leaves the "
    "writes referred, as STND.HARN.18 allows. Where none of these holds, an agent able to append to the ledger is "
    "able to append an unsigned authorize that names the human owner, and the row Record then does not show who "
    "granted the authorization. STND.HARN.30 therefore has a configuration rely on such an authorization only "
    "where the human owner accepts it unsigned at the derivation, after reading what it opens and before the "
    "configuration is installed where the agent is unable to alter it, and has the coverage report name it "
    "(PRIME.7, GUARD.10). The acceptance authenticates nothing, since an agent that runs a derivation is able to "
    "state it; it makes the reliance a stated act in place of a default, and a signer register removes the need "
    "for it. STND.HARN.30 requires no decision of the human owner: without the acceptance, the writes that the "
    "authorization names are referred, and the acceptance, where the human owner gives it, is part of the grant "
    "that GUARD.10 reserves to the human owner, made once for each derivation and not for each write, so it is an "
    "assigned decision under STND.DRAFT.42.")

FLOOR_OLD = ("reading each named authorization file and the ledger that pins it, verifying signatures where they are "
             "required, and comparing each remote write with the authorizations relied on.")
FLOOR_NEW = (
    "reading each named authorization file, the ledger that pins it, and the anchor file, verifying signatures "
    "where they are required, and comparing each remote write with the authorizations relied on. A configuration "
    "that refers every remote write meets STND.HARN.18, so each case in which the row Signature asks for a "
    "signature only narrows the writes that pass without referral. STND.HARN.30 binds, because it instantiates "
    "GUARD.10 and PRIME.7, and raises no floor (GOV.11): where the record does not show that the human owner "
    "granted an authorization, GUARD.2 lets an agent rely on it only as the record states it, and the record then "
    "states no grant of the human owner, so the writes it names are referred under STND.HARN.18; STND.HARN.30 asks "
    "of a harness a refusal and a line of its coverage report, at the cost of the human owner's acceptance once for "
    "each derivation where no signer register is founded, which takes the place of a referral of each write.")

ROW_READING = ("STND.HARN.29, row Signature: a signature is also required where an entry of the ledger carries a "
               "signature or has a scope at or under the directory of the signer register, or an anchor file exists; "
               "new STND.HARN.30: where the row Signature requires no signature, a derived configuration relies "
               "under STND.HARN.29 only on an authorization that the human owner accepts unsigned at the "
               "derivation, and its coverage report names each one; the Notes give the reasons, read the acceptance "
               "as an assigned decision under STND.DRAFT.42, give the floor arguments, and state that only an expiry "
               "bounds the interval in which a configuration relies on a revoked authorization, and that a harness "
               "that refuses an expiry beyond a horizon it states still meets STND.HARN.29")
ROW = f"| 1.3 | {DATE} | Minor amendment (GOV.41): {ROW_READING}. |"

RATIONALE = (
    f"Minor amendment of STND.HARN, revision 1.3, ratified by the custodian on {DATE}: {ROW_READING}. The change "
    "is minor because the row Signature asks for a signature in more cases and STND.HARN.30 adds an obligation on a "
    "harness that derives a configuration (STND.IDENT.3); the Notes on the expiry horizon alone would be editorial, "
    "and ride in this amendment. The row follows the code of unit 0010 as merged: the trace in the ledger of a "
    "register that the corpus lacks, and the anchor file, which a rewritten ledger does not hide. STND.HARN.30 "
    "follows the proposal of the record of unit 0010, with its first sentence recast so that no condition trails "
    "its clause (STND.DRAFT.16). Neither raises the floor (GOV.11): a configuration that refers every remote write "
    "meets STND.HARN.18, both only narrow the writes that pass without referral, and STND.HARN.30 costs a refusal, "
    "a line of the coverage report, and one acceptance of the human owner for each derivation where no signer "
    "register is founded, in place of a referral of each write. The custodian rules at ratification that neither "
    "raises the floor, and that the acceptance of STND.HARN.30 is an assigned decision under STND.DRAFT.42, being "
    "part of the grant that GUARD.10 and PRIME.7 reserve to the human owner, made once for each derivation and not "
    "for each write. Transition (GOV.42): none, because the harness of this corpus implements the row and "
    "STND.HARN.30 since unit 0010, no derived configuration has been installed, and the transition of ledger entry "
    "53 for STND.HARN.18 ends as revision 1.2 states. Review of STND.HARN.28 by the command pairs; records "
    "harness/records/units/0010-unsigned-authorizations.md, harness/records/units/0012-expiry-horizon.md, and "
    "review-records/round-2026-10-25-close/p4/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/HARN/29.md", ROW29)
    (root / "STND/HARN/30.md").write_text(HARN30, encoding="utf-8")
    res = B.derive_fields(root, ["STND.HARN.29", "STND.HARN.30"])
    for ident in ("STND.HARN.29", "STND.HARN.30"):
        if res[ident].unresolved or res[ident].waivable:
            raise ValueError(f"{ident}: {res[ident]}")
    replace_text(root, "STND/HARN/_doc.md", [(EXPIRY_OLD, EXPIRY_NEW), (SIGNATURE_OLD, SIGNATURE_NEW),
                                             (FLOOR_OLD, FLOOR_NEW)])
    raise_revision(root, "STND/HARN", "1.2", "1.3", ROW)
    B.write_references(root, ["STND.HARN"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.HARN"], scope=["STND/HARN"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.HARN 1.3")
