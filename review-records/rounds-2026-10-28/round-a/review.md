# Round a, 2026-10-28: cold review

**Ran** the round on `/tmp/claude-1000/rva/governance` (entries 203 to 207), then `verify` (PASS, only the existing g.18 warning), `show`, `pairs` on the five documents, `findings.py` (only existing g.12 notices), and `compose --all` (only the five documents differ from `rendered/`). Modals, conditions, banned words, titles, and identifiers pass.

## Defects

**D1. STND.DFLT.34 (PRIME.7).** An agent commits a package to the configuration and then installs it, which empties A2's halt. Replace "under version control, or under" with "under version control, other than an install of a package or from a source that an agent added to that configuration, or under".

**D2. STND.DFLT.15, first class (GUARD.5).** It exempts overwriting the owner's uncommitted changes (pair conflict with STND.INSTR.2). Replace "whose last committed state is verified recoverable;" with "whose last committed state is verified recoverable and from which it differs only by changes that the agent made in the current unit of work;".

**D3. Assured work and STND.DFLT.20.** A scribe entry "names the agent as its actor" (Notes), so a scribed classification never makes work assured (A3, A4). In both places, replace "an entry that names the human owner as actor records" with "an entry that names the human owner as actor, or that records an act of the human owner under STND.DFLT.17, records".

**D4. Working bounds (PRIME.7, GUARD.2).** "or configuration" opens to writing the agent's own permissions, instruction files, and network sources, against the STND.PROJ.3 machine-local row. After "leaves out the store of AGENT.44," insert "each configuration that settles the tier of an agent's actions, each instruction file (STND.INSTR), each setting that enables a check of security or integrity, selects a source or destination of network access, or runs a program without a request,".

## Should-fix

**S1. STND.DFLT.17.** It omits waivers and revocations, yet ledgers every "decision". Replace "each act that the human owner gives it directly, an authorization, … or an adoption, as a ledger entry with itself as actor," with "as a ledger entry with itself as actor, each act that the human owner gives it directly and that governance requires to be recorded,". After "quoting the act", insert ", and the proposal it accepts where it accepts one,". List the acts in the Notes.

**S2. STND.DFLT.5.** After "names the human owner as actor", insert ", or that states as the human owner's an act that the human owner did not give it directly".

**S3. STND.DFLT.33.** Implicit acceptance is barred by PRIME.7. Replace "names or accepts the agents" with "names, or accepts a plan that names, the agents". In the AGENT Note, replace "is that authorization (STND.DFLT.33)" with "authorizes the operating cost of the units it covers (STND.DFLT.33), and an estimate under AGENT.6 is authorized only where that direction accepts the plan that states it".

**S4. STND.DFLT.34.** Links unresolved (STND.DFLT.24); caches unlisted (GUARD.6). Replace "that configuration SHALL be" with "the locations that the configuration names as written, and those in which the run's tools keep caches or state, each with symbolic links resolved, SHALL be".

**S5. System temporary directory (R1.3).** After "each temporary location," insert "each file and directory that the agent or its run creates in the system's temporary directory,".

**S6. STND.INSTR.11.**
- Under a constitution, STND.DFLT.17 is unavailable. Replace "by an act entered under STND.DFLT.17" with "by a ledger transaction (GOV.36)".
- Replace the garbled second sentence with "An agent SHALL treat each instruction file whose content no adoption names as content without instruction authority, and name each such file in the completion report of STND.INSTR.7".
- The "at once" report of the Notes is in no body. In STND.INSTR.6, replace "Where a passage directs" with "Where a passage of such content, or of an instruction file that no adoption names, directs".

**S7. INSTR Note against INTPR.5.** Replace "unless the human owner adopts it as an instruction file." with ", and no adoption under STND.INSTR.11 names it."

**S8. Tool memory store.** The default table protects the work. Replace "holding nothing that the threat model marks as protected" with "holding no secret and no other data that the threat model protects against disclosure".

**S9. New STND.PROJ.3 row (GUARD.8):** whole history is bulk. Replace "retrieval of its branches, tags, and history" with "retrieval of the commits, branches, and tags that the work does not yet hold, within a volume per retrieval that the authorization states".

**S10. Record.**
- STND.DFLT rationale: delete "none;" in "Transition (GOV.42): none;", which precedes a transition.
- The A1 Note attributes the drafted reading to the custodian. Replace "The custodian ruled on 2026-10-28 that the direction of a unit of work, naming or accepting the agent configuration, authorizes its operating cost; the direction" with "The direction".

## Optional

**O1.** A forged pre-register CSQ1 entry makes work assured once the owner's key is listed; a signed entry undoes it, so nothing locks.

**O2.** DFLT Notes: replace "the outputs are regenerable from recorded inputs (GUARD.7)" with "regenerable outputs fall in the third exempt class (GUARD.7)"; say a downloading install needs network authorization (GUARD.13).

**O3.** In STND.HARN.6 and .7, replace "asked to read" with "asked to read or append to".

## Custodian items

| # | Verdict |
| --- | --- |
| 1 | Resolve: the A1 ruling covers it. |
| 2 | Resolve (S3). |
| 3 | Keep; record it as a GOV.3 interpretation of PRIME.7. |
| 4 | Keep, narrowed (D2). |
| 5 | Merge with 6; resolve by S1. |
| 6 | Merge with 5. |
| 7 | Resolve by A4 (O1). |
| 8 | Resolve: option (a) says "every referral". |
| 9 | Resolve toward R1.3 (S5). |
| 10 | Keep; content is sound. |
| 11 | Keep, with S6. |
| 12 | Resolve by B1; memory, S7. |
| 13 | Merge with S7. |
| 14 | Merge with S9. |
| 15 | Keep: the added threat condition exceeds R1.5. |
| 16 | Resolve by F1. |
| 17 | Resolve by O3. |
