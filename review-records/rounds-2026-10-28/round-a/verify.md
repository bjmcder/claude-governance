# Round a, 2026-10-28: cold verification

**Ran** commit 04b4725 on `/tmp/claude-1000/rva2/governance` (entries 203 to 207): `verify` PASS, with only the existing g.18 warning; `pairs` (66, 19, 718, 12, and 6); and `compose --all`, diffed against the first review's copy.

**Defects.** D1 to D3 are closed. D4 is closed, but it opens a new conflict (finding 1).

**Should-fix.** S1 to S10 are done as stated, and so are O1 to O3. The STND.DFLT rationale now states its transition.

**Custodian items.** The five left are truly open: 3 interprets LVL0, 4 reads GUARD.5 on the agent's own intermediate changes, and the rulings leave 10, 11, and 15 open.

## Findings

**1. Defect: the write exclusion catches the tool memory store (B2).** The term Instruction file covers "a file that the provisioned environment presents to an agent as standing instructions at the start of a session". A store that its tool loads at session start is therefore an instruction file. Two things follow:
- The Working bounds leave out "each instruction file (STND.INSTR)" for writing, so the agent cannot write the notes that STND.DFLT.6 and STND.INSTR.8 place in the store.
- STND.INSTR.11 could adopt the store, against INTPR.5; only the Notes forbid it.

In the STND.INSTR term, replace "A file that the provisioned environment presents" with "A file, other than a file of a tool memory store, that the provisioned environment presents".

**2. Should-fix: STND.DFLT.35 misses a change of revision (PRIME.7).** An agent can raise the pinned revision of a named package in the configuration and then install it under STND.DFLT.34. That is the route D1 closed for new packages. Replace "a package, or a source of packages," with "a package, a revision of a package, or a source of packages,".

**3. Optional: wording in STND.DFLT.34.** "other than an addition to it that STND.DFLT.35 refers" can be read as reaching only an addition that was actually referred. Then an agent that breaches STND.DFLT.35 escapes the exception. Replace it with "other than an addition to it of a kind that STND.DFLT.35 halts".

The other probes found nothing. The narrowed exempt class covers no change by another actor, and doubt falls to GUARD.2. A scribed classification makes work assured once the owner's key is listed, after which only signed entries lower the class, so nothing locks. Secret locations stay out altogether, and no write opens the agent's tier configuration or its network sources.
