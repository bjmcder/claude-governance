# Pairs whose changed side is a provision of the process part

This list was revised after `review.md` and `../reconciliation.md`. The command, run on the kept copy after all three parts, with the current lvl0 module:

```
pairs <copy> STND.DFLT --with AGENT STND.CLASS STND.IDENT STND.WPROC STND.CREW STND.PROJ STND.INSTR
```

It lists 170 pairs. The tool puts the provision of the profile (AGENT) on the "changed side" of each pair. So every listed pair in which either side is a provision that this part changes or adds is reviewed below.

The changed provisions:

- STND.DFLT.5, .7, .15, .17, .18, .19, .20, .23, .33, .36, .37, and .38;
- AGENT.6;
- STND.CLASS.10, .20, and .22;
- STND.IDENT.23;
- STND.CREW.13 and .21;
- STND.PROJ.1, .2, and .3;
- STND.INSTR.11.

No LVL0 provision is amended, so `--amends` does not apply. Hand pairs with LVL0 2.0 follow the table.

| # | Pair | Basis | Verdict | Reason |
| --- | --- | --- | --- | --- |
| 139 | AGENT.6, STND.CREW.13 | GUARD.14 | none | The estimate of AGENT.6 is one of the bounds of PRIME.8 that CREW.13's record checks |
| 140 | AGENT.6, STND.CREW.20 | GUARD.14 | none | The escalation stays within the envelope. The estimate is unaffected |
| 141 | AGENT.6, STND.CREW.21 | GUARD.14, PRIME.8 | none | CREW.21 refers an assignment beyond the bound of PRIME.8, and the one estimate of the direction is such a bound. The two agree |
| 142 | AGENT.6, STND.CREW.22 | GUARD.14 | none | The stopping-bound referral is independent of the estimate |
| 143 | AGENT.6, STND.CREW.7 | GUARD.14, PRIME.8 | none | CREW.7 asks the basis of every estimate, the estimate of the direction included |
| 144 | AGENT.6, STND.DFLT.26 | GUARD.14 | none | A cap is a spending limit, so AGENT.6's second sentence does not arise, and DFLT.26 governs the configuration |
| 145 | AGENT.6, STND.DFLT.33 | GUARD.14, PRIME.8 | none | DFLT.33's entry, made before the work begins, records the figure of the estimate that AGENT.6's second sentence has stated before the work begins. Both use one figure |
| 146 | AGENT.6, STND.PROJ.5 | GUARD.14 | none | PROJ.5 keeps the estimate in force under the discipline it proposes. The Notes now describe AGENT.6's reach correctly (X10) |
| 1, 3, 7 | AGENT.10 with STND.CREW.13, .21, STND.DFLT.33 | GUARD.14 | none | The least costly configuration is independent of the record, the referral, and the entry |
| 12 | AGENT.11, STND.DFLT.7 | QA.1 | none | The brief of AGENT.11 gives the definition of done, and so is the request of a directed agent's unit. DFLT.7's exception covers it |
| 13 | AGENT.11, STND.PROJ.3 | GUARD.12 | none | The new signing row names the roles that it extends to, as GUARD.12 asks. The brief passes it where it extends |
| 14, 30, 44, 48, 89, 98, 103, 109, 135 | AGENT.12, .20, .24, .25, .35, .36, .39, .41, .47 with STND.CLASS.10 | various | none | Only the row of CSQ1 on INTPR.11 changes, and none of these provisions rests on INTPR.11 |
| 19 | AGENT.17, STND.DFLT.17 | GUARD.2 | none | AGENT.17 reads at the start of a session. DFLT.17 reads before each action under a standing grant. They complement each other |
| 78, 108, 136, 138 | AGENT.3, .4, .47, .5 with STND.DFLT.5 | PRIME.2 | none | Only the serialization that the hash covers changes |
| 110, 113, 117, 124 | AGENT.42, .43, .44, .45 with STND.DFLT.17 | PRIME.10 | none | DFLT.17's handling of secrets is unchanged. The credential means of Working bounds read, pass, and store no secret (AGENT.45) |
| 118, 119 | AGENT.44 with STND.DFLT.18, .19 | GUARD.16 | none | The new DFLT.18 row concerns ledger forgery, not the secret store. DFLT.19's hardware wording changes and nothing else |
| 129 | AGENT.46, STND.DFLT.20 | PRIME.14 | none | The list of unsigned entries is added only where CSQ0 or CSQ1 is recorded |
| 130 | AGENT.46, STND.DFLT.23 | PRIME.14 | none | The referral of foreign entries and that of a retrieval bound may share a statement. Neither halts the other's line (AGENT.15) |
| 134 | AGENT.46, STND.DFLT.36 | PRIME.14 | none | DFLT.36 refers an act that the agent cannot place. That referral is independent of the retrieval bound |
| 147, 149, 155, 157, 163, 165 | AGENT.7, .8, .9 with STND.CREW.13, .21 | GUARD.14 | none | The comparison, the overrun report, and the delegation scale are untouched. CREW.21's referral reaches each kind of bound |
| 153, 161, 169 | AGENT.7, .8, .9 with STND.DFLT.33 | GUARD.14 | none | AGENT.8's report agrees with a stated estimate that PRIME.8 halts before. It reaches only a failure of tracking |

## Hand pairs with LVL0 2.0

| Lower provision | LVL0 provision | Verdict | Reason |
| --- | --- | --- | --- |
| STND.DFLT.15, sixth class | GUARD.7 (fourth ground), GUARD.5, GUARD.6, GUARD.9 | none | The class takes the new ground exactly, "on which no reported result rests" included, and adds a digest as the check. References of the history are excluded, and GUARD.6 prevails |
| STND.DFLT.33 | PRIME.8, GOV.36, GOV.22, QA.11 | none | It is the scribe entry of the authorization and of the promotion, with the bound and figure of PRIME.8, and has no secret. GOV.22 has the direction authorize the stated estimate |
| AGENT.6 | PRIME.8, GUARD.14 | none | One estimate bounds all the work of the direction, stated before it begins. A per-task estimate that the owner sets is a spending limit (GUARD.14) |
| STND.DFLT.23, .38, terms Acceptance entry, Accepted point, Foreign entry | PRIME.11, GUARD.2, GOV.36, PRIME.7 | none | An entry of an act of the owner after the accepted point, from any route, gains authority only by the owner's confirmation, by position and hash. The residual is stated in DFLT.18 (GUARD.16) |
| STND.DFLT.36, term Given directly | PRIME.11, PRIN.1, LEX.human-owner, the Preamble | none | It identifies whose messages carry the owner's authority and establishes no ownership. A naming counts only by an accepted entry |
| STND.DFLT.37 | PRIME.9 | none | It places the provisioning record and confines it to the named environment |
| STND.DFLT.19, STND.PROJ.1 row | PRIME.13, GOV.13, GOV.20 | none | "Commands, configures, or powers", as LVL0 now reads |
| Term Working bounds, STND.PROJ.3 signing row | PRIME.10, GUARD.11, GUARD.13, GOV.22, GOV.51 | none | The tool uses the credential only under the owner's authorization, in that action alone. The agent reads, passes, and stores no secret and changes no credential configuration |
| STND.CLASS.20 | QA.11, GOV.11, GOV.13 | none | A promotion of presumed CSQ4 work cites the entry of the owner's direction, which exists |
| STND.CLASS.10, .22 | GOV.48, GOV.14, GOV.20 | none | The row drops the clause that GOV.48 no longer supports. The step applies only before the constitution of GOV.20 |
| STND.IDENT.23 | GOV.37, GOV.41 | none | The duty arises only for a project instrument that carries the mnemonic. A ledger transaction changes the project's register |
| Term Main line, STND.WPROC.12 | GOV.50, QA.10, GUARD.11 | none | The default branch is a main line once the work is released or deployed from it. A release stays the owner's |
| STND.INSTR.11 | PRIME.11, PRIME.13, GUARD.3, GOV.49 | none | A restriction never bars the safe-state command or the steps of GUARD.3, and it gains no power to direct |
| STND.CREW.13, .21, term Lead agent | PRIME.8, PRIME.11 | none | The bounds are PRIME.8's. A named person performs no act of PRIME.1 |
| STND.PROJ.2 | GOV.21, GOV.22 | none | The citation adopts provisions whose content is unchanged, with the rules they rest on |
