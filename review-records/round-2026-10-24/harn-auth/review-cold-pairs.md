# Cold and pair review: STND.PROJ 1.2 and STND.HARN 1.2 (2026-10-24)

Read-only review of the three scripts, unit 0008, the rehearsed copy `/tmp/rehearsal-2fckuq79/governance`, and the hand-check set.

## Verified by script

- Rehearsal of the round appends entries 117 (PROJ 1.2) and 118 (HARN 1.2). `verify`: all PASS (the existing g.18 notice only). `findings.py`: only two older notes on STND.HARN.28; none on the new provisions.
- `govharness pairs` on the rehearsed copy equals the stored lists. They hold 12 (PROJ) and 15 (HARN) pairs; "18" and "21" are the files' line counts. Each row appears once below, checked by script.
- `git` and `gh` appear in no provision and no Notes; only the example host `git.example.org` does (Optional 2).

## Findings

### Defect

1. **STND.HARN.29 asks for what a derived configuration cannot do.** Sentence 1 has each row met "at the time of the write", but the Notes say a revocation reaches a configuration only when it is derived again, and unit 0008 tests every row except Dates at derivation. The binding text is unmet by its own implementation, and a revoked authorization keeps opening writes until the next derivation. Fix: "meets each row at the time the configuration is derived, and the Dates row at the time of the write"; the Notes state the interval, and the coverage report names it (HARN.19).
2. **No test that the authorization extends to the acting agent (GUARD.12, PRIME.7: "NEVER widened by delegation").** The template has `delegable_to`; STND.PROJ.6 omits it and HARN.29 has no row, and the code does not read it. PROJ.3 extends commits to the lead, implementing, and merging agents; a research agent under the same configuration could push. Fix: add `delegable_to` to PROJ.6 (roles of STND.CREW) and a HARN.29 row "Extension: it extends to the role for which the configuration is derived (GUARD.12)", with GUARD.12 instantiated.

### Should-fix

1. **PROJ.7 `commit` omits PROJ.3's exclusion.** A push to a branch whose update publishes or deploys is a publication (irrevocable always, GUARD.11), yet only the `provisioned` flag marks `commit` irrevocable, so a standing commit to a deploy branch of a provisioned remote passes. Fix: "to a branch whose update neither publishes nor deploys"; such a push is `publish`.
2. **HARN.29 Record row is narrower than STND.DFLT.23, unexplained.** DFLT.17 has the agent enter the owner's grant with itself as actor, and DFLT.23 accepts it for unassured work; HARN.29 refers it. Refusing it is safe (a referral) and defensible, since an agent can forge such an entry, but the Notes must say so, or cite "an entry that STND.DFLT.23 accepts" and drop the Signature row.
3. **Obligations in the indicative in Notes (STND.DRAFT.6, STND.DOCS).** HARN: "the human owner who revokes ... therefore derives and installs the configuration again (STND.HARN.21)": an owner duty, which HARN.21 does not hold. PROJ: "lapses at the earlier of the two" is a rule found in no provision, and the harness checks only the time, so a lapse by condition (PROJ.3) is not enforced; "refers its writes (STND.HARN.19)" should cite HARN.18. Fix: describe effects only; say a revocation is a revoke transaction.
4. **Entry-53 transition ends before its cause exists.** The rationale ends it "because the derivation implements the row (unit 0008)", but the unit says "Review: none yet" (QA.8) and is not installed. Fix: apply the round after the unit is reviewed and merged, or word the end as "from the day the harness of unit 0008 is installed". "Unchanged" for HARN.26 to .28 is correct, but say whether that part has ended (entry 116 cites the `pairs` command).
5. **Rationales read "ratified by the custodian" before any ruling.** The lead sets them at the coalesce; the floor argument of HARN.29 (GOV.11) goes to the custodian as a decision.
6. **Expiry as a timestamp.** GUARD.10 assigns the owner a stated duration, so a time is a form of it, not a new decision. But "until revoked" is not in force under HARN.29, against STND.DRAFT.42 (accept a standing authorization where GUARD.11 allows). Fix: "its expiry, where it has one, later than the write".
7. **Template guidance (STND.DRAFT.11).** The added sentence in `AUTH/1.md` guides the person completing it and must begin "Fill-in guidance:".
8. **Standing test is per file, not per entry.** Row Standing says the authorization "names no kind" marked irrevocable "at the destination it names"; with several destinations, one irrevocable entry would void the others, or be read apart. State "each entry".

### Optional

1. HARN.29 names the form of a default (PROJ.6); allow "or an alternative recorded under GOV.19 with the same fields".
2. The `.git` suffix and host `git` in the Notes example hint at a tool; use `https://example.org/team/work`.

### Cold-review answers

- **Drafting rules:** one modal per sentence, titles unique, cited lists equal (STND.DRAFT.24), no excluded words; the two SHALL sentences of HARN.29 are a bundle never applied apart (say so in the Notes).
- **Class (GOV.41):** both minor: obligations are added (entries 52 and 53 so classed it); none is relaxed.
- **GUARD.11:** per-action authorizations are never relied on, so irrevocable writes always refer; publish and transmit always irrevocable; every kind irrevocable at a destination not provisioned: correct except Should-fix 1.
- **"Provisioned":** the Lexicon leaves it undefined; PROJ.3 already has the owner record it, and the default is `false`, so the field adds no decision. Defensible, not assigned by name.
- **Floor (GOV.11):** HARN.29 asks of the harness checks, plus a record the owner already makes (GUARD.10, DFLT.17); sound but for Defect 2 and Should-fix 2.
- **Agnosticism:** met. **DFLT.16:** PROJ.6 maps one to one (grantor, class and scope as kinds and destination, expiry, standing, recorded). **INSTR:** HARN.29 reads the ledger, never text an agent read (PRIME.11).

## Pair review (method of review-pairs-offld.md)

Columns: # | pair | conflict | unowned | reason. All "no, no" unless stated. Each pair read against the body of the other provision.

| # | Pair | Reason |
| --- | --- | --- |
| P1 | PROJ.3 / AGENT.11 | Proposal of roles; AGENT.11 passes authorizations that extend to the directed agent. Compatible (see Defect 2) |
| P2 | PROJ.4 / AGENT.25 | Form of files; records before the next action. Compatible |
| P3 | PROJ.4 / AGENT.35 | Instrument files with other records. Compatible |
| P4-P8 | PROJ.5 / AGENT.10, .6, .7, .8, .9 | Unchanged cost discipline; the amendment adds nothing to it. Compatible |
| P9 | PROJ.6 / AGENT.25 | The authorize entry precedes the write; no clash |
| P10 | PROJ.6 / AGENT.35 | The file sits with the other records. Compatible |
| P11 | PROJ.7 / AGENT.25 | A closed list of kinds; no record order. Compatible |
| P12 | PROJ.7 / AGENT.35 | Same as P10 |
| H1-H3 | HARN.11, .12, .13 / AGENT.17 | Signature checks; the agent reads authorizations in force. HARN.29 cites HARN.11 for the Signature row; no clash |
| H4-H6 | HARN.17 / HDES.14, HW.8, HW.GPU.3 | Exit status against saturation, fault, and completion status; different subjects (PRIME.4 only) |
| H7-H9 | HARN.19, .20, .21 / AGENT.17 | Reports and installed files against reading authorizations. Compatible |
| H10-H11 | HARN.22 / AGENT.45, .46 | Unattended refusal of Refer outcomes against credential and research-bound referrals; an address with no credential (PROJ.6) agrees with AGENT.45 |
| H12-H14 | HARN.23 / HDES.14, HW.8, HW.GPU.3 | Program failure against saturation, fault, and status; different subjects |
| H15 | HARN.29 / AGENT.17 | The agent's set of authorizations in force can be wider (DFLT.17); the configuration refers the rest. No conflict; Defect 2 |

Hand-check of PROJ.6, .7, HARN.29: GUARD.10 and PRIME.7 met; GUARD.11 (Should-fix 1); GUARD.12 (Defect 2); GUARD.13 (a standing write exists only inside the provisioned environment, so no network authorization arises); GUARD.14, .15, PRIME.8 (no spending); DFLT.16 consistent; DFLT.22 untouched; DFLT.24 and .25 (a destination outside the bounds stays refused or referred); INSTR; AGENT.17, .25, .35, .45; HARN.18 (HARN.29 narrows "in force", and the response stays a referral); HARN.23 untouched.

## Summary

- **Conflicts:** 0 of 27. **Unowned matters:** 0. **Covered:** 27 of 27 once each (12 PROJ, 15 HARN).
- **Not checked:** the harness code beyond `authorizations.py` and the grep for `delegable`; git and gh behavior; whether the signer register accepts a signature on an authorize entry.

## Verdicts

- **STND.PROJ 1.2: adopt after Should-fix 1, 3, 6, 7.** Minor is the right class.
- **STND.HARN 1.2: revise, then adopt.** Minor is the right class; Defects 1 and 2 and Should-fix 2 and 4 block.
