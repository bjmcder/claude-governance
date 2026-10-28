# Round e of 2026-10-28: the harness's place in the corpus, the cleanups, and the rest

This round carries ruling E1 of `review-records/deep-review-2026-10-28/rulings.md` on the reading of its section "Rulings of the custodian, 2026-10-28" (option (a)), and, under ruling F1 ("The smaller entries are drafted from the reviewers' proposed text"), register entries R5.1, R5.3, R6.1, R6.4, R7.1, and R7.2, finding AD9, the copies that round d left (`round-d/decisions.md`, decisions 1b, 3a, 16, and 18), and the residual of CS9 that round c left (`round-c/decisions.md`, "Left to the lead"). The module is `tools/amendment-scripts/apply_round_e_2026_10_28.py`, with the helpers `round_e_base.py` (the step and its record), `round_e_harness.py` (STND.HARN, LVL0, AGENT), `round_e_process.py` (the process and systems documents), and `round_e_code.py` (the code standards). The harness side is unit 0024 (`harness/records/units/0024-review-pairs.md`). Nothing here is in force until the custodian ratifies it and the script runs.

## Transactions

Thirty-five, one per document, in citation order. Each revision is computed from the field `revision` as rounds a, d, c, and o leave it; the numbers are those of the rehearsal on their present modules.

| # | Document | Revision | Class | What |
| --- | --- | --- | --- | --- |
| 0 | STND.HARN | 1.6 → 1.7 | Minor | .24 and .28 as outcomes a reader checks; .28 narrowed; Note on the reviewer; Purpose |
| 1 | LVL0 | 1.7 → 1.7.1 | Editorial (GOV.40) | GOV.11, GOV.24, GOV.48, GUARD.4, GUARD.15, the opening of PRIME |
| 2 | AGENT | 1.3.1 → 1.3.2 | Editorial | .45 and .46 drop a sentence each; Notes |
| 3 | STND.DOCS | 1.0.1 → 1.0.2 | Editorial | .8 holds the spelling table |
| 4 | STND.DRAFT | 1.6.1 → 1.7 | Minor | .33 cites the table of STND.DOCS.8; .10 reaches governance |
| 5 | STND.WFLOW | 1.1 → 1.2 | Minor | agent self-records out of scope; term Step |
| 6 | STND.WPROC | 1.3 → 1.4 | Minor | .13 cites AGENT.47; new .16 |
| 7 | STND.IDENT | 1.4 → 1.5 | Minor | .13: an adopter who is not the author |
| 8 | STND.INSTR | 1.5 → 1.5.1 | Editorial | Notes: instructions need not be presented whole; one narration |
| 9 | STND.VVUQ | 1.5 → 1.5.1 | Editorial | research note, versions, one narration |
| 10 | STND.MPI | 1.2 → 1.2.1 | Editorial | the path of the research note |
| 11 | HDES | 1.0.3 → 1.0.4 | Editorial | STND.SV cited |
| 12 | HDES.ASIC | 1.0.3 → 1.0.4 | Editorial | a conjunction in .12 |
| 13 | STND (root) | none | `annotate`, GOV.36 | standards name no product, vendor, or version |
| 14 | STND.PROJ | 1.4.1 → 1.5 | Minor | .2 one citation of STND.DFLT; .1 execution paths leave the classification |
| 15 | HW | 1.3 → 1.3.1 | Editorial | Notes on the execution paths |
| 16 to 21 | HW.ASIC, HW.CPU, HW.EMBED, HW.FPGA, HW.GPU, HW.QPU | 1.2 → 1.2.1 (ASIC, CPU, FPGA); 1.1.1 → 1.1.2 (EMBED, GPU, QPU) | Editorial | Notes: the provisions reach a component through its execution paths, recorded where the section Architecture names |
| 22 | STND.CLASS | 1.5 → 1.5.1 | Editorial | Notes on the mechanisms of GOV.21 at CSQ4 |
| 23 | STND.PERF | 1.1.1 → 1.2 | Minor | .1 reaches each claim that HW.22 governs |
| 24 | STND.FTN | 1.3 → 1.4 | Minor | .4 conditioned on the means; .33 entries for sets of files |
| 25 | STND.DEPS | 1.2.1 → 1.3 | Minor | new .14; .13; .4 |
| 26 | STND.CODE | 1.6 → 1.7 | Minor | .5 conditioned on the means; Notes |
| 27 | STND.BUILD | 1.0.4 → 1.0.5 | Editorial | Notes cite STND.CODE.21 and STND.DEPS.14 |
| 28 | STND.SV | 1.1.1 → 1.2 | Minor | .28 withdrawn |
| 29 | STND.STDC | 1.4 → 1.5 | Minor | .39 and .40 withdrawn |
| 30 | STND.LEAN | 1.1.1 → 1.2 | Minor | .27 withdrawn |
| 31 | STND.CXX | 1.4.1 → 1.5 | Minor | .18 withdrawn; one narration |
| 32 | STND.JL | 1.5 → 1.6 | Minor | .3 reduced; one narration |
| 33 | STND.RUST | 1.4 → 1.5 | Minor | .1 reduced; .28; one narration |
| 34 | STND.PY | 1.4 → 1.5 | Minor | .14 withdrawn |

The order: STND.DOCS takes the spelling table before STND.DRAFT gives it up, so that the drafting check always has one. STND.PROJ comes before HW, its six sub-profiles (in identifier order, each recorded under the scope `HW` as every earlier transaction of a sub-profile was), and STND.CLASS, whose Notes cite its new text; as round c leaves them, the six sub-profile Notes say that the provisions reach a component "through the execution paths that the classification lists", which STND.PROJ 1.5 would make false. STND.DEPS adds STND.DEPS.14 before STND.CODE, STND.BUILD, STND.JL, STND.RUST, and STND.PY cite it. Each document that cites a copy drops the citation before the copy is withdrawn: STND.CODE and STND.BUILD before STND.CXX, STND.STDC, and STND.PY; STND.SV before STND.STDC and STND.LEAN; STND.STDC before STND.CXX; STND.RUST before STND.PY. A revision history row is no citation. The root document STND is planned and has no revision, so its change is recorded as ledger entry 186 pinned the file: type `annotate`, authority GOV.36, no target, scope `STND/_doc.md` alone. A transaction is needed, since STND.HARN.9 stales the pin of entry 186 once the file changes; no earlier round changed the text of a document without a revision, so entry 186 is the only model. The composed `STND.md` prints no revision line.

## E1: rehearsal and review pairs (R5.1; CP7, CP23, HR-12)

**STND.HARN.24**, binding (GOV.36), *Rehearsal before application*:

> Before applying a script that changes a corpus, an actor SHALL confirm, on a copy of the corpus on which the script has run, that the copy has each property whose absence a check of a harness that meets this standard reports as FAIL, as the documentation of that harness states the property (GOV.36). A rehearsal of the script in which no check reports FAIL MAY serve as that confirmation (GOV.36).

The reach is the old one: every check that a rehearsal runs and that reports FAIL, the drafting checks of defaults, the logic checks, and the check of onsets included. The first draft reached only the properties that a binding provision gives to a check in its field `checked_by`, which lowered a binding provision (review, Defect 1). A reader confirms the properties by reading them in the documentation of the harness (its list of checks, in `harness/README.md` for this harness) against the copy, without running it; a harness confirms them by a rehearsal. The provision keeps "a script", as CP7's own text does: a change made by hand is outside it, as before, and widening it would add an obligation that no ruling names. The outcome now rests on the documentation of a harness, which reading 1 puts to the custodian.

**STND.HARN.28**, binding (GOV.26, QA.7), *Conflict candidates*:

> The record of the review of each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0 SHALL state, for each pair of provisions of different documents that a row of the table of this provision gives, at least one of them in a profile or sub-profile and at least one of them a provision that the change adopts or amends or that instantiates a LVL0 provision that the change amends, whether the two provisions conflict and whether they address one matter that no shared-matters table gives, with the profile that is to own it (GOV.26, QA.7). The summary of that record given to the adopter SHALL hold only the pairs found to conflict and the matters left without an owning profile, and cite the full record (GOV.26).
>
> | Basis | Pair given |
> | --- | --- |
> | Shared matter | The shared-matters tables of the documents in force and of each document that the change adopts or amends give both provisions for one shared matter. |
> | Common instantiation | Both provisions are in documents of which the change adopts or amends a provision, and both instantiate one LVL0 provision outside GOV and the Governing Principles. |

The duty of a harness to list becomes the content of the review record, which a reader checks from the tables and the field `instantiates`; the old first sentence ("a harness SHALL list") lapsed without a harness (CP7). The third sentence is unchanged. The table is named `review-pairs` in `defines`.

**The Note (CP23)**, in place of "An agent of a different agent configuration from the author performs that review (QA.8), and the adopter sees only its summary.":

> STND.HARN.28 states what the record of that review and the adopter's summary hold, and STND.CLASS.18 the independence of its reviewer (QA.8).

The old sentence stated an obligation in the indicative and named "a different agent configuration", which round c's STND.CLASS.18 now refines (another session at CSQ3; another model or instruction revision at CSQ2). The citation of STND.CLASS.18 leaves the independence to the row of the class of the work. The Notes add the reasons for the narrowing, that a change of the Notes alone pairs nothing, that a provision that the change reaches only by instantiating an amended LVL0 provision pairs on shared matters alone, so that a change of LVL0 alone pairs only on shared matters, that STND.HARN.24 reaches every check of a rehearsal, that `pairs` is one way to list the pairs, and the floor argument.

**Unit 0024** makes `pairs` follow the drafted text: `--with` names the other documents, or provisions, of one change, and a pair of common instantiation needs both provisions in touched documents (code review, Should-fix 1: the first draft tested the other provision alone, so a provision reached only through `--amends` paired with every touched document, 15 pairs of this round among them). An identifier that names no document or provision below LVL0, a LVL0 article without `--amends`, and an `--amends` that names no LVL0 provision exit 1, and so does an empty listing (Should-fix 2 and 3). Counts, before and after:

| Change | Rule in force | Drafted rule |
| --- | --- | --- |
| NUMER | 4,384 | 92 |
| HW | 2,302 | 128 |
| HDES | 2,343 | 137 |
| STND.VVUQ | 4,921 | 0 |
| AGENT | 706 | 0 |
| STND.CODE | 166 | 0 |
| LVL0, amending VV.1 | 12,185 | 339 |
| NUMER, amending VV.1 as well | — | 344 |
| This round | 20,343 in its 34 listings, 369 holding a changed provision | 44 |

The brief and HR-12 give "about 19 pairs" for NUMER. HR-12 counted the pairs whose only basis is a shared matter; 73 more rest on a shared matter and on a common LVL0 provision. The ruling's words, "those on a shared matter", take all 92.

## R5.3: the Purpose of STND.HARN (CP22)

> A harness serves governance: it fetches what applies, checks conformance, and enters the transactions that an actor directs. It holds no authority of its own, and no work depends on it (GOV.38). STND.HARN.24 and STND.HARN.28 state outcomes of a change of governance that a reader checks with or without a harness.

It agrees with LEX.harness ("… and enters transactions; it holds no authority of its own") and with the standing direction: no write command is exposed to an agent, and a transaction is entered only as an actor directs, as the custodian's scripts do.

## R6.1: LVL0 restating itself (CC23, CC24, CC25, CC26 checked; CC31)

LVL0 1.7.1, an editorial amendment in the form of entry 7 (type `amend`, authority GOV.40, the thirteen LVL0 folders as scope, targets LVL0 and the provisions changed). Each change was checked to change no meaning:

| Provision | Old | New | Held whole by |
| --- | --- | --- | --- |
| GOV.11 | "… the reliance placed on it, NEVER to the setting or hardware of the work (PRIN.9). The proportionality judgment, which states the consequence class and the reliance placed on the work, is recorded and adopted by the human owner." | "… the reliance placed on it, both of which the proportionality judgment states (GOV.50), NEVER to the setting or hardware of the work (PRIN.9)." | LEX.proportionality-judgment ("The human owner's recorded judgment of the consequence class of work and the reliance placed on it"); GOV.50 (adopted only by the human owner); GOV.36 (every adoption entered) |
| GOV.24 | "The classification is adopted by the human owner (GOV.50) and revised whenever …" | "The classification (GOV.50) is revised whenever …" | GOV.50 |
| GOV.48 | "… for every action. They SHALL NOT grant themselves waivers (GOV.44)." | "… for every action." | PRIME.1, rank 0: only the human owner performs "granting authorizations and waivers", and "An agent MAY draft and propose these acts and NEVER performs them" |
| GUARD.4 | "… (GOV.21), adopted by the human owner or, absent a project constitution, provided by the defaults (GOV.22)." | "… (GOV.21, GOV.22)." | GOV.50 (the register and its exempt classes); GOV.22; PRIME.1 reserves the acts of GOV.50 at rank 0 |
| GUARD.15 | "Expenditure that would exceed an authorized estimate or operating envelope halts the work incurring it, and the agent refers it (PRIME.14)." | "The agent refers each line of work that PRIME.8 halts (PRIME.14)." | PRIME.8 ("Work halts before an authorized estimate or operating envelope is exceeded"), rank 0 |
| PRIME (opening) | "Where two prime directives pull apart, the more restrictive reading governs, and an agent halts and refers (GOV.6, PRIME.14)." | "Where two prime directives pull apart, GOV.6 and GOV.9 decide which governs and when an agent halts and refers." | GOV.6 (equal rank: the more restrictive governs, halt and refer); GOV.9 (readings of a prime directive) |

GOV.48 is carried (review, Should-fix 4): logic check b.5 read the bar on a self-granted waiver in GOV.48 alone, so unit 0024 has it read the bar from PRIME.1 where GOV.48 no longer states it; its verdict on the live corpus is unchanged (PASS, reading GOV.48), and on the rehearsed corpus it passes reading PRIME.1.

Not carried, each on the text:
- **CC23, PRIME.1.** GOV.50 does not list the grant of authorizations and waivers, which PRIME.1 reserves at rank 0; citing GOV.50 alone would change a prime directive.
- **CC23, PRIME.7.** "NEVER granted, extended, or inferred by an agent for itself" says more than PRIME.1, and CC27's refutation relies on it.
- **CC24, PRIME.14.** Its triggers are its own; GOV.6 and GOV.9 cite PRIME.14 for the halt, and neither lists them, so citing them in place of the triggers would change a prime directive.
- **CC25, beyond GOV.11 and GOV.24.** GOV.13 states the act itself, and STND.CLASS.20 and STND.DFLT.13 are not LVL0; CC25 proposes no change there.

**CC31 (AGENT, checked; it holds).** AGENT.45 drops "Where work needs an authentication credential that the provisioned environment does not let the agent use, the agent SHALL refer to the human owner its need for that credential (PRIME.14)", which PRIME.14 holds ("privilege beyond what was provisioned … appears necessary"), and no longer instantiates PRIME.14. AGENT.46 drops "Until the extension is recorded, an agent SHALL NOT retrieve for that effort beyond the bound (GUARD.8)", which GUARD.8 holds (retrieval beyond the bounds is bulk retrieval, reserved). The AGENT Notes cite both. Editorial: each dropped sentence binds the same actor, at a lower rank, to what LVL0 already asks.

## R6.4: the process standards (CP13; CP26, checked; the spelling table)

**CP13**, STND.WFLOW, Purpose: "The record that an agent keeps of its own actions under REPRO.11 is no workflow run under this standard: an action of an agent or a person is a step only where a workflow description declares it." The term Step ends "… or a step that a person or an agent performs and that a workflow description declares." Minor: a defined meaning narrows; REPRO.11 still has the steps of an agent recorded, in the form AGENT gives.

**CP26**, STND.WPROC.13 (binding): "An agent that proposes a release SHALL record and present to the human owner the revision it proposes, and each item that the work reports of its units state under AGENT.47 (GOV.50, AGENT.47)." The items are those AGENT.47 lists, the readings of an ambiguous instruction among them, which the work reports already hold. CP26's third part, STND.CREW.14, is not in the brief and adds "at once and unchanged", so it is not a copy.

**The spelling table.** STND.DOCS.8 now holds the British and American table of STND.DRAFT.33 whole, beside its own table of usage, and its first sentence cites "the tables of this provision". STND.DRAFT.33 keeps its rule: "A provision SHALL use American spelling, of which the spelling table of STND.DOCS.8 lists a part (INTPR.12)." The two tables are not merged into one: g.22 reads the spelling table word by word, and the rows of the usage table hold annotated groups ("licence (noun), practise (verb), enquiry") that no check reads. The harness reads the table where STND.DRAFT.33 cites it (unit 0024), which is the one change of harness code outside `query/combination.py`, its wiring, and its tests; without it, g.1 and g.22 would lose their table on the rehearsed corpus. STND.DOCS is editorial (the list that STND.DOCS.8 cited is the same list); STND.DRAFT is minor because of STND.DRAFT.10, below.

## R7.1: stale or broken text

| Entry | Status | Drafted |
| --- | --- | --- |
| CP17 | Confirmed; no such file exists in the repository or its history | STND.VVUQ Purpose: "… and logged each retrieval; the note is not kept in the project. Where a default number rests on a source, the table of sources in the Notes gives it; …". The proposal of a knowledge entry, never made, is dropped. |
| CP25 | Checked; holds | STND.VVUQ: "MCNP Theory and User Manual | Current release; not opened by the research"; "an earlier MCNP manual and a CANTEACH chapter; the current MCNP manual was not opened". |
| CS21 | Confirmed | STND.MPI Notes: `research/parallel-models.md`. |
| CS20 | Confirmed | HDES, twice: "LVL2 standards, STND.SV among them"; References gains STND.SV. |
| CS22 | Checked; holds | HDES.ASIC.12, second sentence: "… each condition that HDES.10 states as not analyzed, each variation that HDES.ASIC.5 states as not verified, and each block whose evidence rests only on the contract of an external component". Editorial: a block cannot be read as a variation. |
| CP24 | Confirmed | `STND/_doc.md`: "LVL2 standards apply across projects and state methods and defaults. They name no product, vendor, or version; a tool and its version are each project's choice." CP24's citation of GOV.18 is not used: GOV.18 places the choice of tools at LVL2 and LVL3, so it does not say that standards name none. LEX.standard ("which may name tools and methods") is LVL0 and outside the brief; its "may" admits the narrower practice, so the two do not conflict. |
| CP27 | Checked; holds in part: the STND.JL Notes already read STND.DRAFT.10 as concerning governance text | STND.DRAFT.10: "A sentence of a document of governance or of a project instrument SHALL NOT be written in the imperative mood (INTPR.12)." Minor, since the stated reach changes. |
| CL22 | Confirmed | STND.CXX Notes: "The counterpart of STND.CXX.27 in Julia is STND.JL.36, which keeps …"; STND.JL Notes drop "STND.CXX.27 stays unchanged, and STND.JL.36 is its Julia counterpart." The STND.STDC part no longer stands as CL22 quotes it, and the paragraph that held its successor is rewritten with the withdrawal of STND.STDC.40. |
| CL15 | Confirmed | Already carried by round d (decision 15): no "Julia 1.11" remains. |
| CP17's kin, narration found in this round's documents | — | STND.INSTR: "The earlier draft's default standing authorization is dropped, because …" becomes "This standard proposes no default standing authorization, because no default grants an authorization (GOV.22)."; STND.VVUQ: "the one that STND.VVUQ.63 named before this revision" becomes "the largest"; STND.RUST: "bind as before the round" becomes "bind at every class"; STND.PROJ: "before this revision" names revision 1.1. |

## R7.2: small burdens and gaps

- **CC20**, STND.PROJ.2 (binding), second sentence: "A project constitution MAY adopt STND.DFLT by one citation as the content of its sections Work process, Defects, Review and release, Correction, Incidents, Dependencies, Records, Working notes, Workbench, Secret store, Access descriptors, Threat model, Reserved actions, Agent instructions, and Configuration, and state in full only its other sections and each of these whose content departs from STND.DFLT (GOV.21, GOV.22)." The sections are named, so that the clause is decidable (review, Should-fix 5); the STND.PROJ Notes give the provisions of STND.DFLT for each (STND.DFLT.7 to .9, .10, .8, .12, .11, .2 to .5, .6, .28, .29 to .31, .27, .18 and .19, .14, .15, and .24, .20 and .21, .22 and .35), each found by the LVL0 provision of the row that it instantiates, and say that Identity, Classification, Knowledge base, Authorizations, Architecture, Physical hardware, and Exceptions hold what only the project states. CC20's text named only Identity and Classification as stated in full.
- **CP15**, new STND.WPROC.16 (default; QA.2, DSGN.15; onset CSQ3), *Shared records on the development line*: "An agent that works on a unit branch SHOULD make each change to the ledger, the roadmap, defect tracking, or the record of decisions awaiting the human owner as a commit on the development line that changes only that record (QA.2, DSGN.15)." The Notes: such a commit is no merge, so STND.WPROC.10 does not reach it, and one that finds the line moved is made again on its new state, the protocol of DSGN.15 for these records. CP15's "and needs no review of STND.WPROC.10" is not used: "needs no" is an excluded expression, and STND.WPROC.10 reaches merges alone. STND.WPROC.4 already has three modals, hence a new provision.
- **CP28**, STND.IDENT.13: "Where no review transaction precedes the transaction of a revision whose adopter is not its author, the adopter's decision recorded in that transaction MAY serve as the QA.7 review of that revision (GOV.43)." The corpus's own revisions are authored by an agent and adopted by the custodian, so ledger entry 15 and `F.AUTHOR` still hold.
- **CL19**, a convenience: STND.FTN.4, second sentence, "Where the means of the work include a static check that reports each reference to a procedure without an explicit interface, or one that compares each interface body … with the definition of that procedure, each change SHOULD pass each such check (DSGN.3)."; STND.CODE.5, first sentence, "Where the means of the work include a tool that produces the layout of the source of a language of the work, the repository configuration SHOULD name such a tool for that language (INTPR.1)."
- **CC30 (checked; holds)**: QA.7, QA.15, and REPRO.12 lie above the floor, which work of CSQ4 may omit, while GOV.21 has every constitution define their mechanisms. Carried as a Note of STND.CLASS, not CC30's sentence, which states an obligation in the indicative: "A mechanism of GOV.21 whose obligation work of CSQ4 may omit, review (QA.7), incident handling (QA.15), and retention (REPRO.12) among them, costs that work no more than one citation of the defaults (STND.PROJ.2), and the obligation that it serves applies from the class that STND.CLASS.10 gives."
- **CL9 (checked; holds)**: STND.RUST.28, second sentence, "Before a change that adds a dependency with a build script is relied upon, its review SHOULD examine that build script (SIMPL.4, REPRO.9)." The Notes: a build script that a new revision of a dependency already in the work changes is code of the pinned revision that STND.DEPS.4 reviews.
- **CL20 (checked; holds)**: STND.DEPS.4, second sentence, "Each review SHOULD record why each direct dependency that it leaves at its revision stays there, one reason serving each group of dependencies that share it (REPRO.7, REPRO.9)."; STND.FTN.33, an entry "that names that file, or a directory or a pattern of names whose files share its forms and reasons", with the term Legacy list and the Notes (a widened entry is an entry added).
- **CS17 (checked; holds)**: STND.PERF.1, added "Each claim that HW.22 governs SHOULD rest on a performance evaluation as well (RSRC.4)." HW.22 asks measurements of both paths at a stated size and accuracy but no repetition or dispersion.

## AD9: the agent instructions need not be presented whole

The brief calls this AD6. AD6 of `anthropic-docs.md` is the derived configuration, which round a carried as CC28 (R5.4); the text the brief describes is AD9's. AD9 holds: nothing says the instructions are presented together, and STND.INSTR.10 asks only that an agent meet each provision. STND.INSTR Notes:

> No provision asks that the agent instructions be presented to an agent whole: an environment that loads the provisions that govern an action when the action needs them serves STND.INSTR.10 as well as one that loads them all at the start of a session, since GOV.39 has an actor read the full text of a provision before relying on it.

## Left by round d: the copies withdrawn, and CL7

| Withdrawn | Outcome held by | Citations moved first |
| --- | --- | --- |
| STND.CXX.18 | STND.CODE.21 (binding, every language) | STND.CODE Notes (2), STND.BUILD Notes (2), STND.STDC Purpose and Notes, STND.CXX Purpose, class paragraph, and Notes |
| STND.STDC.40 | STND.CODE.21 | STND.CODE Notes, STND.BUILD Notes (2), STND.STDC Purpose, class paragraph, and Notes |
| STND.STDC.39, STND.LEAN.27, STND.SV.28 | STND.CODE.28 | STND.SV Purpose and Notes; STND.STDC and STND.LEAN Purpose and Notes |
| STND.PY.14 | new STND.DEPS.14 | STND.BUILD Notes, STND.DEPS Notes, STND.RUST Notes, STND.PY Purpose and Notes |

STND.CODE.21 reaches code that holds a check that STND.CODE.6 or STND.CODE.16 governs, which are the checks of untrusted input and of CPS.5 and CPS.9 that STND.CXX.18 and STND.STDC.40 named, at every class; STND.CODE.28 gives the convention of the repository configuration where the standard of a language gives none, with the names that NUMER.4 fixes, at CSQ3. No outcome or onset changes for C, C++, Lean, or SystemVerilog.

**CL7 (checked; holds).** New STND.DEPS.14 (default; VV.8, RSRC.12; onset CSQ3), *Declared range checks*:

> Other than for high-assurance code whose edition and toolchain STND.CODE.19 fixes, the checks of each release of work that declares a range of revisions of its language or of a dependency SHOULD run with the oldest revisions that those ranges admit, together, and with the newest revisions that they admit and that are consistent with one another (VV.8, RSRC.12). Other than for such high-assurance code, a check that reports its failure without blocking a change SHOULD run the tests of such work, at the interval that the repository configuration sets, with the newest stable release of its language and the newest revisions of its dependencies that their declared ranges admit (VV.8).

The cadence is not settled by the text; round d (decision 18) put it to the custodian, and it is reading 3. Drafted: the checks across the range at each release, since RSRC.12 defers verification "to the latest decision point at which its result is still needed" and dependents rely on a declared range through a release, which is the reading the STND.PY Notes already gave ("a deferral of verification under RSRC.12"); a project that runs them at each change meets the default. STND.DEPS.13 excepts the checks of STND.DEPS.14 from the locked revisions. What each language keeps:
- STND.PY.14 is withdrawn; STND.PY.13 keeps the declaration.
- STND.JL.3 keeps the reference version at each change, and "The check of STND.DEPS.14 that reports its failure without blocking a change SHOULD also run the tests on the newest prerelease of Julia (VV.8)."
- STND.RUST.1 keeps the edition and the oldest supported toolchain in the metadata, and the checks of each change at the release that builds results.

For Rust and Julia, the check at the oldest admitted revisions moves from each change to each release; for Python, the check at an interval on the newest revisions is new (reading 2).

## Left by round c: the residual of CS9

Round c made HW.1 one attribute, but the Classification section still listed "the components that hold domain items of each selected profile, with the execution paths of each by hardware type" (STND.PROJ.1), so a path on a new type changed a record that the human owner adopts. STND.PROJ.1 now ends the Classification row at "the components that hold domain items of each selected profile;", and the Architecture row reads "The recorded dependency structure of the components (DSGN.7), and where the execution paths of each component are recorded by hardware type". The section names where the record is kept, as the Notes say the sections do ("The sections ask for what each mechanism is, not for a plan of the work"), so the record changes without a decision of the human owner. The HW Notes follow. The classification keeps the value of the attribute Hardware execution (GOV.24), and path scope decides reach (STND.DRAFT.38). This is reading 3.

## Floor arguments of the provisions that bind (GOV.11)

| Provision | Rests on | Argument |
| --- | --- | --- |
| STND.HARN.24 | GOV.36 | It reaches every check that a rehearsal runs, as the old text did, and admits the rehearsal as the means; a project without a harness reads the properties from the documentation. No decision of the human owner. |
| STND.HARN.28 | GOV.26, QA.7 | A verdict on fewer pairs. GOV.26 still bars a contradiction between profiles, and QA.7 still has the change reviewed against all applicable governance; the pairs dropped rest only on a common LVL0 provision with a provision outside the documents that the change touches, which the review of their own adoption judged. |
| STND.WPROC.13 | GOV.50, AGENT.47 | Presents what AGENT.47 already has the work reports state. |
| STND.IDENT.13 | GOV.43 | Narrows a permission to what QA.7 allows; asks nothing beyond QA.7. |
| STND.PROJ.1, STND.PROJ.2 | GOV.20, GOV.21, GOV.22 | A permission that lowers the cost of a constitution, every mechanism still defined; one item leaves the classification for a record of the work, and the attribute and path scope are unchanged. |
| AGENT.45, AGENT.46; LVL0 | PRIME.10, PRIME.14, GUARD.8; GOV, GUARD | Editorial: the text dropped is held whole by a provision of equal or higher rank. |
| STND.CODE.21 (for C++ and C, after the withdrawals) | PRIME.4, DSGN.2 | Unchanged; it bound before the round, and the withdrawals remove copies. |

Every other provision this round adds or changes is a default that a recorded decision replaces (GOV.19), so none raises the floor.

## For the custodian at ratification

1. **E1, STND.HARN.24's outcome.** Drafted: the actor confirms each property whose absence a check of a harness that meets STND.HARN reports as FAIL, as the documentation of that harness states it, with a rehearsal as one way to confirm. This keeps the reach of the old text, every check of a rehearsal, defaults, logic checks, and onsets included, and lets a reader check it from the documentation without running the harness; but the outcome rests on the documentation of a harness, not on the corpus alone. Alternative: the properties that provisions give to checks in their field `checked_by`, the outcome of the first draft, which the corpus alone states but which drops the checks of defaults outside STND.DRAFT, the logic checks, and the check of onsets, and so lowers a binding provision. **Recommendation: as drafted**, the narrowest text that keeps the reach.
2. **E1, the unit of a change.** The ruling lists "those where both provisions are in documents the change touches". Drafted: a pair holds at least one provision that the change adopts or amends (or that instantiates an amended LVL0 provision), and a pair of common instantiation needs both provisions in documents of which the change adopts or amends a provision; a change of the Notes alone pairs nothing. Alternative: every provision of every document that the change touches, Notes-only changes included. For a single new document the two agree (NUMER: 92). For this round the alternative gives 6,763 pairs against 44. **Recommendation: as drafted**, the reading that keeps the list one a reviewer can judge, which is the reason the ruling gives.
3. **CL7, cadence and strength (round d, decision 18, put it to the custodian).** Cadence: (a) the checks across a declared range at each release (drafted; RSRC.12), a project that runs them at each change meeting the default; (b) at each release, or at each change where the repository configuration states it (round d's wording), which says the same with the choice spelled out. For Rust and Julia, (a) and (b) both move the check at the oldest revisions from each change to each release. Strength of the check at an interval on the newest revisions: SHOULD for every language (drafted; Python gains it), or CL7's MAY (relaxes Rust and Julia). **Recommendation: at each release, and SHOULD**: one rule for every language, at the point where dependents rely on the range, and at the strength that two of the three languages already had.
4. **CS9, the execution paths.** Drafted: they leave the Classification section, and the Architecture section names where they are recorded, so that a path on a new hardware type needs no decision of the human owner; the Notes of HW and its six sub-profiles follow. Alternative: keep them in the classification, with the route that the HW Notes gave, a classification that admits the hardware types the work plans to use. **Recommendation: as drafted**, the outcome that CS9 sought, with the attribute and path scope unchanged.
5. **CL9, the build scripts of Rust dependencies.** Drafted: the review examines the build script of each dependency that a change adds, and a changed build script of a dependency already in the work is reviewed with its pinned revision under STND.DEPS.4. Alternative: keep the review of every build script that a change to the lock file adds or alters, which touches the supply-chain row of the threat model (GUARD.17). **Recommendation: as drafted**; STND.DEPS.4 reviews each pinned revision that a unit changes, so no build script enters unreviewed.
6. **Round o's reading 9, the onset of STND.CXX.24, STND.CXX.26, and STND.CXX.27**, which round o's record defers to this round. (a) CSQ3, as their fields give it under the rule of STND.CLASS.10, a tightening above the floor that the STND.CXX Notes give the reason for; (b) the classes of the rows of STND.STDC.1, CSQ1 for STND.CXX.24 and .27 and CSQ2 for .26. **Recommendation: (a)**; the text as drafted already matches it, so no text changes, and the rows of STND.STDC.1 keep the C readings their own onsets, as ratified for C.

## Review and dispositions

The cold review of the text is `review.md` in this folder; the cold review of unit 0024 is `review-records/harness/review-unit-0024.md`.

| Finding | Disposition |
| --- | --- |
| Text, Defect 1: STND.HARN.24 lowered a binding provision | Fixed: the reach is every check that reports FAIL in a rehearsal, as the documentation of a harness states each, the checks of defaults, the logic checks, and `onset` included; the outcome rests on that documentation, so it is reading 1. |
| Text, Defect 2: six sub-profile Notes contradict STND.PROJ.1 | Fixed: six editorial transactions after HW, in identifier order, each Note citing STND.PROJ.1 for where the paths are recorded. |
| Text, Should-fix 1 (review item 3): the root transaction of STND | Fixed: `annotate` under GOV.36, no target, scope `STND/_doc.md`, as entry 186; `STND.md` prints no revision line. |
| Text, Should-fix 2 (item 4): GOV.48 | Carried: the sentence is dropped, and unit 0024 has b.5 read the bar from PRIME.1 where GOV.48 no longer states it. |
| Text, Should-fix 3 (item 5): CL7's cadence | Put to the custodian, reading 3, with round d's wording as an option. |
| Text, Should-fix 4 (item 6): round o's reading 9 | Reading 6; the drafted text matches the recommended option. |
| Text, Should-fix 5 (item 7): STND.PROJ.2 not decidable | Fixed: the provision names the sections, and the Notes give the provisions of STND.DFLT for each. |
| Text, Optional 8 to 10 | Taken: "and the removal" in STND.STDC; "now" dropped in STND.STDC and STND.CXX; GOV.11 "both of which". |
| Code, Should-fix 1: common instantiation with a provision reached through `--amends` | Fixed: both provisions in touched documents; the round lists 44 pairs (42 by the reviewer's count, plus two from GOV.48, now amended). |
| Code, Should-fix 2 and 3, Optional 4 and 5 | Fixed: an identifier that names no document or provision below LVL0, a LVL0 article without `--amends`, an `--amends` that names no LVL0 provision, and an empty listing exit 1 with one line on the standard error; `--with` and `--amends` take `nargs="+"` with `extend`; the skill row names `--with`. |
| Code, Optional 1 to 3 (survivors) | Tests added for the documents in draft, for GOV and PRIN bases, and for `cited_tables`; the dead guard in `tables.py` is dropped. Optional 6, two long lines of `test_drafting.py`, predates the unit. |

## Checks

- **Rehearsal**, `ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28,apply_round_o_2026_10_28,apply_round_e_2026_10_28 python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`: 119 entries appended (84 of rounds a, d, c, and o; 35 of this round); every check PASS, `onset: PASS`, logic PASS with only the g.18 warning that the corpus carries; source unchanged.
- **Kept copy** `/tmp/claude-1000/round-e/kept/governance`: `references --check` PASS; `compose --check` lists the six reading copies as stale, because the kept copy has no `rendered/` beside it; `verify` as the rehearsal. `pairs` for each of the 33 documents with provisions or Notes changed, for the round as one change, and for LVL0 with `--amends GOV.11 GOV.24 GOV.48 GUARD.4 GUARD.15`: `pairs-changed.md` lists 44 pairs under the drafted rule and 369 under the rule in force, each with its verdict; none conflicts. The composed `STND.md` prints no revision line.
- **Findings**, `tools/findings.py` over every changed document, against the corpus after round o: no new finding; four g.18 notices go (AGENT.46, STND.HARN.28, STND.JL.3, and STND.RUST.1 now hold two modals each).
- **Self-check** of every provision drafted: one modal per sentence and at most three per provision (two at most in each new or changed provision, three in STND.DOCS.8 as before); one condition per sentence, before its clause; none of the excluded expressions of class exact, "such as", "for example", or a quantifier of STND.DRAFT.17 in a provision body ("is to" in STND.HARN.28 is unchanged text, which the substitution test of STND.DRAFT.9 keeps, since "the profile that SHALL own it" changes the sense); titles "Shared records on the development line" and "Declared range checks", at most six words, not verb-initial, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to` (the check `ids` and the drafting checks pass); References rebuilt by the script.
- **Harness**: unit 0024, its tests and mutations in its record. `query/combination.py`, `cli/query.py`, `cli/main.py`, the README row of `pairs`, and the row of the skill; beyond them, `checks/drafting/tables.py`, for the spelling table, and `checks/logic/authority.py` and `facts.py`, for b.5 (GOV.48). No verdict of a check on the live corpus changes: `pairs` is no check, the live STND.DRAFT.33 still holds its table, and b.5 still reads GOV.48 there.

## Not carried

- The parts of CC23 and CC24 named under R6.1, each for the reason given there.
- CP26's STND.CREW.14 and CC25's STND.CLASS.20 and STND.DFLT.13: outside the brief, and not copies.
- LEX.standard's "which may name tools and methods": LVL0, outside the brief; it does not conflict with the root document of the standards.
