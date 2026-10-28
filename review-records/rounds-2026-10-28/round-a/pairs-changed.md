# Round a of 2026-10-28: pairs on a changed side (STND.HARN.28)

Listed by `pairs` on the kept copy after the round (as revised after the cold review), for each changed document; only the pairs whose changed side is a provision this round changes or adds. STND.DFLT.15, STND.DFLT.23, STND.DFLT.34, STND.INSTR.11, STND.HARN.6, and STND.HARN.7 appear in no pair: no profile provision instantiates an LVL0 provision they instantiate outside GOV and PRIN, or shares a matter with them. The pair numbers are those of the AGENT listing (687 to 694 for AGENT.6) and of the STND.DFLT listing after STND.DFLT.35 was added.

The conflict the review found between the first exempt class of STND.DFLT.15 and STND.INSTR.2 (D2) is closed: the class now reaches a file only where it differs from its committed state by the agent's own changes in the current unit of work, so another actor's uncommitted changes stay under STND.INSTR.2.

| # | Changed side | Other side | LVL0 | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | STND.DFLT.11 | HDES.3 | REPRO.9 | none | HDES.3 keeps the design record of external components; STND.DFLT.11 reviews the pinned revision of the dependency the unit changes. Both apply. |
| 2 | STND.DFLT.11 | ML.3 | REPRO.9 | none | ML.3 records a model's pretrained sources; no overlap with the review of a changed dependency. |
| 4 | STND.DFLT.17 | AGENT.17 | GUARD.2 | none | AGENT.17 reads the authorizations in force before the first change of a session; STND.DFLT.17 says which an agent relies on, unchanged by this round. |
| 5 | STND.DFLT.17 | AGENT.42 | PRIME.10 | none | STND.DFLT.17 quotes an act without each secret it contains; AGENT.42 treats doubtful information as a secret, so a doubtful item is left out of the quotation. |
| 6 | STND.DFLT.17 | AGENT.43 | PRIME.10 | none | An entry without the secret commits none (AGENT.43). |
| 7 | STND.DFLT.17 | AGENT.44 | PRIME.10 | none | A secret the act contains goes to the store of AGENT.44, not the entry. |
| 8 | STND.DFLT.17 | AGENT.45 | PRIME.10 | none | A credential in a grant is written to no persistent location; the entry omits it. |
| 10 | STND.DFLT.19 | AGENT.44 | GUARD.16 | none | AGENT.44 protects the secret store as the threat model requires; the table of STND.DFLT.18 names secrets, so the store is no unnamed asset and STND.DFLT.19 halts nothing for it. |
| 12 | STND.DFLT.20 | AGENT.45 | PRIME.14 | none | The referral of AGENT.45 takes the form of STND.DFLT.20; the new sentence adds one recommended next step while an unsigned entry records CSQ0 or CSQ1. |
| 13 | STND.DFLT.20 | AGENT.46 | PRIME.14 | none | As for AGENT.45. |
| 50 | STND.DFLT.32 | AGENT.11 | GUARD.12 | none | STND.DFLT.32 proposes each authorization with the agents to which it extends; AGENT.11 passes to a directed agent each authorization that extends to it. Complementary. |
| 51 | STND.DFLT.33 | AGENT.10 | GUARD.14 | none | AGENT.10 governs the configuration a directing agent gives a directed agent where no discipline is set; STND.DFLT.33 names the act of the human owner that authorizes the cost of a configuration the owner names or accepts, and sets no discipline. A directing agent's own choices stay under AGENT.10. |
| 52 | STND.DFLT.33 | AGENT.6 | GUARD.14 | none | AGENT.6 states the estimate where the cost is measurable; STND.DFLT.33 makes the direction its authorization. The AGENT Notes say so. |
| 53 | STND.DFLT.33 | AGENT.7 | GUARD.14 | none | AGENT.7 reports the cost incurred beside the estimate; the estimate is the one the direction authorized. |
| 54 | STND.DFLT.33 | AGENT.8 | GUARD.14 | none | AGENT.8 reports an overrun of the estimate; STND.DFLT.33 does not revise the estimate, and PRIME.8 still halts before an envelope is exceeded. |
| 55 | STND.DFLT.33 | AGENT.9 | GUARD.14 | none | AGENT.9 permits delegation within project limits; the direction covers the agents it names or accepts, and a directing agent that adds agents beyond the estimate refers under STND.CREW.21. |
| 56 | STND.DFLT.35 | AGENT.45 | PRIME.14 | none | STND.DFLT.35 refers an addition of a package or source to the recorded configuration; AGENT.45 refers a need for a credential. Two referrals, each in the form of STND.DFLT.20. |
| 57 | STND.DFLT.35 | AGENT.46 | PRIME.14 | none | AGENT.46 refers a bound on research retrieval; no overlap with an addition to the configuration. |
| 59 | STND.DFLT.5 | AGENT.3 | PRIME.2 | none | STND.DFLT.5 bars an entry naming the human owner as actor; AGENT.3 marks claims in reports. No shared subject. |
| 60 | STND.DFLT.5 | AGENT.4 | PRIME.2 | none | As for AGENT.3. |
| 61 | STND.DFLT.5 | AGENT.47 | PRIME.2 | none | As for AGENT.3. |
| 62 | STND.DFLT.5 | AGENT.5 | PRIME.2 | none | As for AGENT.3. |
| 63 | STND.DFLT.5 | NUMER.26 | PRIME.2 | none | NUMER.26 concerns repeated stochastic comparisons. No shared subject. |
| 64 | STND.DFLT.6 | AGENT.17 | INTPR.5 | none | AGENT.17 reads the agent's notes in the working-notes workspace, which now includes each tool memory store; the record that names the store's location is how the agent finds it. |
| INSTR 1 | STND.INSTR.6 | AGENT.44 | GUARD.16 | none | STND.INSTR.6 reports injected passages; AGENT.44 keeps secrets in a store. No shared subject. |
| INSTR 3 | STND.INSTR.8 | AGENT.17 | INTPR.5 | none | As for pair 62. |
| AGENT 9 | AGENT.11 | STND.CREW.12 | GUARD.12 | none | STND.CREW.12 adds the role and depth to the brief of AGENT.11; the location of the agent instructions is one more item. |
| AGENT 10 | AGENT.11 | STND.CREW.14 | GUARD.12 | none | STND.CREW.14 carries directed agents' reports; no overlap with the brief's content. |
| AGENT 11 | AGENT.11 | STND.DFLT.32 | GUARD.12 | none | As for pair 50. |
| AGENT 12 | AGENT.11 | STND.DFLT.7 | QA.1 | none | STND.DFLT.7 commits the criteria before the first attempt; AGENT.11 gives them to the directed agent. |
| AGENT 13 | AGENT.11 | STND.PROJ.3 | GUARD.12 | none | STND.PROJ.3 states the roles each proposed authorization extends to; AGENT.11 passes the extended ones on. |
| AGENT 687 | AGENT.6 | STND.CREW.13 | GUARD.14 | none | STND.CREW.13 records that the authorized estimate or envelope admits the cost of agents at depth 3 or more; where the cost of a unit is not measurable there is no estimate and nothing to admit, and the envelope alternative stands. |
| AGENT 688 | AGENT.6 | STND.CREW.20 | GUARD.14 | none | STND.CREW.20 escalates within the operating envelope; independent of whether an estimate was stated. |
| AGENT 689 | AGENT.6 | STND.CREW.21 | GUARD.14 | none | STND.CREW.21 refers an assignment beyond the authorized estimate; without a measurable cost there is no estimate to exceed, and the levels marked for ruling still refer. |
| AGENT 690 | AGENT.6 | STND.CREW.22 | GUARD.14 | none | STND.CREW.22 shapes the referral of STND.CREW.21; as above. |
| AGENT 691 | AGENT.6 | STND.CREW.7 | GUARD.14 | none | STND.CREW.7 binds an agent that states an estimate; where AGENT.6 asks for none, STND.CREW.7 asks nothing. |
| AGENT 692 | AGENT.6 | STND.DFLT.26 | GUARD.14 | none | STND.DFLT.26 applies within an adopted cap; no overlap with when an estimate is stated. |
| AGENT 693 | AGENT.6 | STND.DFLT.33 | GUARD.14 | none | As for pair 52. |
| AGENT 694 | AGENT.6 | STND.PROJ.5 | GUARD.14 | none | STND.PROJ.5 proposes a discipline that keeps AGENT.6 in force for every unit; AGENT.6 in force now asks for an estimate where the cost is measurable, which is what GUARD.14 estimates. The proposal's words still read correctly through AGENT.6's condition. |
| PROJ 1 | STND.PROJ.3 | AGENT.11 | GUARD.12 | none | As for pair AGENT 13. |
