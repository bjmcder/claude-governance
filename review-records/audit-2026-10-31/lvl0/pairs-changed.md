# Round of 2026-10-31, part lvl0: pairs on a changed side (STND.HARN.28)

`pairs` was run on the kept copy after the part, for the one changed document:

```
pairs <copy> LVL0 --amends PRIME.8 PRIME.9 PRIME.11 PRIME.13 PRIME.14 GUARD.1 GUARD.7 GUARD.8 GUARD.9 GUARD.10 GUARD.14 QA.1 QA.11 GOV.10 GOV.13 GOV.14 GOV.20 GOV.22 GOV.48
```

It lists no pair: "no pair to review before a change of LVL0". For a change of LVL0 alone, the changed side holds the provisions below LVL0 that instantiate an amended provision, and these pair only on a shared matter. None of them is on a shared-matters table with a provision of another document.

Since the tool lists nothing, each provision below LVL0 that instantiates an amended LVL0 provision was read by hand against the new LVL0 text, as in the round of 2026-10-28 on GOV.20. The provisions that instantiate GOV.22 or GOV.48 were read only where the change to GOV.22 (the class) or to GOV.48 (INTPR.11) reaches their subject. "Stale" means that the provision does not conflict with the new LVL0 text, but its text or its Notes state something the change makes untrue, or it keeps a halt that the change removes. Each stale item is carried in "For the process part" of `decisions.md` in this folder.

| # | Lower provision | Amended LVL0 | Verdict | Reason |
| --- | --- | --- | --- | --- |
| 1 | STND.DFLT.33 | PRIME.8, GUARD.14 | none (stale) | Its case is a direction that names the agents and their configuration. It falls inside the new PRIME.8, which covers every direction in a configuration that the owner provisioned. It authorizes nothing beyond PRIME.8, so it relaxes nothing, but it is now redundant except for the entry under STND.DFLT.17. Decided for the process part (R1, lower part). |
| 2 | STND.CREW.21 | PRIME.8, GUARD.14 | none | It acts only where an authorized estimate exists, or where the owner's discipline marks a level. Both remain possible under the new PRIME.8, and the referral still precedes a revision that only the owner makes. |
| 3 | STND.CREW.7 | PRIME.8, GUARD.14 | none | It gives the basis of an estimate whenever one is stated. GUARD.14 still has one stated where the cost is measurable. |
| 4 | STND.CREW.13 | GUARD.14 | none (stale) | Before depth 3, it asks for a record that "the authorized estimate or the operating envelope of its unit admits" the cost. Under the new PRIME.8 a unit can have neither, since the direction authorizes the cost and the limits bound it. CREW.13 then bars depth 3 or more. It tightens and does not conflict, but it keeps a halt that R1 removes. |
| 5 | STND.CREW.20, STND.CREW.22 | GUARD.14 | none | Recommendations on escalation within the envelope and the referral. No change of subject. |
| 6 | AGENT.6 | GUARD.14 | none (stale) | It states an effort estimate where the cost is measurable, which matches GUARD.14. Where no spending limit or fixed cost bounds the work, that estimate is PRIME.8's stated bound and must precede the work. The AGENT Note that reads it with STND.DFLT.33 is stale. |
| 7 | AGENT.7 | GUARD.14 | none | It reports the cost beside the estimate. |
| 8 | AGENT.8 | GUARD.14 | none (stale) | It reports an overrun of the effort estimate. Where that estimate is the one that PRIME.8's fourth sentence has the agent state, the work instead halts before the estimate is exceeded and the extension is referred. Elsewhere, the report is GUARD.14's anomaly report. The decision has the process part conform it. |
| 9 | AGENT.9, AGENT.10 | GUARD.14 | none | Delegation within project limits, and the least costly configuration absent a discipline. GUARD.14 keeps both. |
| 10 | STND.DFLT.26 | GUARD.14 | none | An enforced cap adopted as the envelope is a limit that the environment enforces and that the owner sets, so PRIME.8 halts before it. |
| 11 | STND.PROJ.5 | GUARD.14 | none | It proposes a discipline. The owner's choice stays under GUARD.14. |
| 12 | STND.CREW.2, STND.CREW.23, STND.INSTR.6, STND.THRT.2 | PRIME.11 | none | Each treats content as data. A person named under PRIME.11 instructs over the instruction channel and is not content. |
| 13 | STND.INSTR.11 | PRIME.11 | none | Adoption of an instruction file is an adoption of governance (PRIME.1), which a named person does not perform. |
| 14 | STND.CLASS.17 | PRIME.13 | none | It tests the hazard responses at CSQ0. The permission to command the safe state does not touch it. |
| 15 | AGENT.46, STND.CREW.14, STND.CREW.2, STND.DFLT.20, STND.DFLT.25, STND.DFLT.30, STND.DFLT.35, STND.DRAFT.42 | PRIME.14 | none | Only the trigger on class changes. None of them cites that trigger. |
| 16 | AGENT.14 | GUARD.1 | none | The wider free tier makes free the unnamed routine steps that AGENT.14 already asks no approval for. |
| 17 | STND.DFLT.15, STND.DFLT.29 | GUARD.7 | none | S1 corrects the wording only. The sense that the exempt classes rely on is unchanged. |
| 18 | AGENT.46 | GUARD.8 | none | Research retrieval is network access, so it stays within GUARD.8. |
| 19 | STND.INSTR.2 | GUARD.9 | none | It already confines the preservation of a prior state to items that no exempt class of STND.DFLT.15 covers. That is now GUARD.9's own reach. |
| 20 | STND.DFLT.16, STND.DFLT.17, STND.DFLT.32, STND.PROJ.3, STND.WPROC.12 | GUARD.10 | none | The fields of an entry, its recording, the proposals, and per-action release authorizations. A revocation is an act that STND.DFLT.17 already enters (its Notes list "an authorization and its revocation"). I1's re-reading of grants is decided for the process part. |
| 21 | STND.CLASS.1, STND.CLASS.5, STND.CLASS.6 | GOV.13 | none | The owner's criteria, the record, and isolated components. The presumption applies only until the owner records a class. |
| 22 | STND.CLASS.7 | GOV.14 | none | It has the owner reassess on growth, and bars reliance in the occasioning use until then. The new GOV.14 halts the line that supports that reliance, which agrees with CLASS.7. |
| 23 | STND.CLASS.22 | GOV.14 | none | The obligations owed before reliance at a more severe class are unchanged. |
| 24 | STND.PROJ.1 | GOV.20 | none | It fixes the sections of a constitution once a project has one. |
| 25 | STND.DFLT.13, STND.PROJ.2 | GOV.22 | none | The classification is still the owner's record. The presumption is GOV.13's, not a default. |
| 26 | STND.INSTR.1 to .11, STND.DFLT.21, AGENT.11, STND.CXX.3, STND.DOCS.10, STND.PY.4, STND.RUST.6, STND.VVUQ.83 | GOV.48 | none | Each rests on the agent instructions or the "every action" reach of GOV.48 for its own subject, not on INTPR.11. |
| 27 | STND.CLASS.10 (cites GOV.48; does not instantiate it) | GOV.48 | conflict (stale clause) | Its CSQ1 row reads "Recording and verification of automated decisions other than agent actions, which GOV.48 covers at every class (INTPR.11)". After I5, GOV.48 no longer covers agent actions at every class, so the clause is untrue. Under the first sentence of CLASS.10, INTPR.11 for agent actions then applies from CSQ3. The process part must strike or restate the clause (see `decisions.md`). |
| 28 | AGENT.11 | QA.1 | none | It passes the definition of done and the acceptance criteria to a directed agent, whatever states them. |
| 29 | STND.DFLT.7 | QA.1 | none (stale) | It asks the definition of done and acceptance criteria "committed before its first attempt", for every unit. It tightens QA.1 and does not conflict. But under the defaults it keeps for every unit the commit that R9 removes from the floor (B6). |
| 30 | STND.KNOW.1 | QA.11 | none | An entry of kind Result states whether the result is promoted. The owner's direction under the presumption is a promotion (QA.11, LEX.promotion), so the entry says promoted. |
