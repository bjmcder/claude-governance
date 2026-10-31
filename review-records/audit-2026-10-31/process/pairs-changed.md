# Pairs whose changed side is a provision of the process part

The command, run on the kept copy after all three parts:

```
pairs <copy> STND.DFLT --with AGENT STND.CLASS STND.IDENT STND.WPROC STND.CREW STND.PROJ STND.INSTR
```

It lists 169 pairs. The tool puts the provision of the profile (AGENT) on the "changed side" of each pair. So every listed pair in which either side is a provision that this part changes or adds is reviewed below. The changed provisions are STND.DFLT.5, .7, .15, .17, .20, .23, .33, .36, and .37, AGENT.6, STND.CLASS.10 and .22, STND.IDENT.23, STND.CREW.13, STND.PROJ.2, and STND.INSTR.11. No LVL0 provision is amended, so `--amends` does not apply. After the table come hand pairs with the LVL0 2.0 provisions that each change rests on.

| # | Pair | Basis | Verdict | Reason |
| --- | --- | --- | --- | --- |
| 138 | AGENT.6, STND.CREW.13 | GUARD.14 | none | The estimate of AGENT.6 is one of the bounds of PRIME.8 that the record of CREW.13 checks |
| 139 | AGENT.6, STND.CREW.20 | GUARD.14 | none | The escalation stays within the operating envelope, and the estimate is unaffected |
| 140 | AGENT.6, STND.CREW.21 | GUARD.14, PRIME.8 | none | CREW.21 refers an assignment beyond an authorized estimate. Where the AGENT.6 estimate is the stated estimate of PRIME.8, PRIME.8 itself halts before it and refers the extension, so the two never ask opposite things |
| 141 | AGENT.6, STND.CREW.22 | GUARD.14 | none | The referral of the stopping bound is independent of when the estimate is stated |
| 142 | AGENT.6, STND.CREW.7 | GUARD.14, PRIME.8 | none | CREW.7 asks the basis of every estimate, the stated one of PRIME.8 included |
| 143 | AGENT.6, STND.DFLT.26 | GUARD.14 | none | Where a cap is adopted, it is a spending limit, so AGENT.6's new occasion does not arise and DFLT.26 governs the configuration |
| 144 | AGENT.6, STND.DFLT.33 | GUARD.14, PRIME.8 | none | DFLT.33's entry, before the work begins, names which bound applies, the estimate of each unit under AGENT.6 among them. The estimate itself is stated in the plan before each unit begins. Neither asks the other's content |
| 145 | AGENT.6, STND.PROJ.5 | GUARD.14 | none | The discipline that PROJ.5 proposes keeps the AGENT.6 estimate for every unit, and so meets the new occasion |
| 1 | AGENT.10, STND.CREW.13 | GUARD.14 | none | The least costly configuration and the depth record are independent |
| 7 | AGENT.10, STND.DFLT.33 | GUARD.14 | none | The entry of the direction does not bear on the choice of configuration |
| 12 | AGENT.11, STND.DFLT.7 | QA.1 | none | The brief of AGENT.11 gives the definition of done, and so is the request of a directed agent's unit. DFLT.7's exception then covers it without a commit, consistent with QA.1 |
| 14, 30, 44, 48, 89, 98, 103, 109, 134 | AGENT.12, .20, .24, .25, .35, .36, .39, .41, .47 with STND.CLASS.10 | VV.1, INTPR.6, RSRC.3, INTPR.12, REPRO.12, REPRO.10, DSGN.15, INTPR.10 | none | Only the row of CSQ1 on INTPR.11 changes. None of these provisions rests on INTPR.11 |
| 19 | AGENT.17, STND.DFLT.17 | GUARD.2 | none | AGENT.17 reads the authorizations in force at the start of a session. DFLT.17 adds the read before each action under a standing grant. Both rely on the record (GUARD.2) |
| 78, 108, 135, 137 | AGENT.3, .4, .47, .5 with STND.DFLT.5 | PRIME.2 | none | DFLT.5 changes only in the serialization that its hash covers |
| 110, 113, 117, 124 | AGENT.42, .43, .44, .45 with STND.DFLT.17 | PRIME.10 | none | DFLT.17's handling of secrets in an entry is unchanged. The credential means of the term Working bounds write no credential anywhere (AGENT.45), and the agent reads none |
| 129 | AGENT.46, STND.DFLT.20 | PRIME.14 | none | The list of unsigned entries is added only where CSQ0 or CSQ1 is recorded. The referral for a bound of research retrieval keeps its form |
| 130 | AGENT.46, STND.DFLT.23 | PRIME.14 | none | A referral for foreign entries and a referral for a retrieval bound may go in one statement, and neither halts the other's line (AGENT.15) |
| 146, 154, 162 | AGENT.7, .8, .9 with STND.CREW.13 | GUARD.14 | none | The comparison, the overrun report, and the delegation scale are untouched by the change of CREW.13 from "the authorized estimate or the operating envelope" to "each bound of PRIME.8" |
| 152, 160, 168 | AGENT.7, .8, .9 with STND.DFLT.33 | GUARD.14 | none | AGENT.8's report of an excess is consistent with a stated estimate before which PRIME.8 halts. It then reaches only a failure of tracking |

## Hand pairs with LVL0 2.0

| Lower provision | LVL0 provision | Verdict | Reason |
| --- | --- | --- | --- |
| STND.DFLT.33 | PRIME.8, GOV.36, QA.11 | none | The entry restates no bound. It names the bound that PRIME.8 sets. It records the authorization and the promotion that GOV.36 lists (reading 1) |
| STND.DFLT.36, term Given directly | PRIME.11, PRIN.1, LEX.human-owner, the Preamble | none | The provision identifies whose messages carry the owner's authority, and establishes no ownership. Quoted, relayed, and retrieved text is data, as PRIME.11 says |
| STND.DFLT.17 | GUARD.10, PRIME.7 | none | The entry precedes reliance, and a revocation is found before each standing action. The agent grants itself nothing |
| STND.DFLT.23, term Foreign entry | PRIME.11, GUARD.2, GOV.36 | none | An entry gains authority only by the owner's act. Content that arrives by a merge or a fetch stays data until confirmed |
| STND.DFLT.15 (sixth class) | GUARD.5, GUARD.6, GUARD.7, GUARD.9 | none | Its ground is GUARD.7's recoverable prior state. History is excluded, and GUARD.6 prevails |
| Term Working bounds | PRIME.10, GUARD.13, GOV.22, GOV.51 | none | The tool, acting within the agent's authority (GOV.51), uses the credential under the owner's authorization of the action. The agent reads no secret, and no default grants the authorization |
| STND.DFLT.37 | PRIME.9 | none | It places the provisioning record and adds no condition |
| STND.DFLT.7 | QA.1, GOV.10 | none | It follows QA.1 |
| AGENT.6 | PRIME.8, GUARD.14, GUARD.15 | none | The estimate is the one that PRIME.8 makes the bound, stated before the unit begins |
| STND.CLASS.10 | GOV.48, GOV.11, INTPR.11 | none | The row drops the clause that GOV.48 no longer supports. Agent actions fall under the first sentence, from CSQ3 |
| STND.CLASS.22 | GOV.14, GOV.20 | none | The step applies only in the interval before the constitution that GOV.20 asks at CSQ1 and CSQ0 |
| STND.IDENT.23 | GOV.37, GOV.41 | none | A ledger transaction of the project changes the project's own register, as GOV.37 requires. The owner adopts the project's instruments (GOV.41) |
| Term Main line, with STND.WPROC.12 | GOV.50, QA.10, GUARD.11 | none | A release stays the owner's decision, and a publishing push stays per action |
| STND.INSTR.11 | PRIME.11, GOV.49 | none | Refraining uses no instruction authority. No unadopted content gains the power to direct an action |
| STND.CREW.13, term Lead agent | PRIME.8, PRIME.11 | none | The bounds are PRIME.8's. A named person instructs within scope and performs no act of PRIME.1 |
| STND.PROJ.2 | GOV.21, GOV.22 | none | The citation adopts provisions whose content is unchanged |
