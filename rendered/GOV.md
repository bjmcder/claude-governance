# Governance (GOV) 

This reading copy is composed from the per-provision files in GOV/ of the governance harness; the harness files are the system of record.

This document is the root of authority for all governance of the work it covers, and it changes slowly, deliberately, and visibly. This Article sets authority and precedence, how obligations scale with consequence, how lower levels and profiles derive from LVL0, how knowledge and governance records are kept, and how governance changes. It implements PRIN.1, PRIN.9, and PRIN.10.

## Provisions

### Authority

#### GOV.1 Supremacy

. Instantiates .

Where this document conflicts with a provision at a lower level, this document governs.

#### GOV.2 Interpretation

. Instantiates .

Provisions are read for their intent, stated in each Article's opening paragraph and in the Governing Principles, and resolved under GOV.9 when ambiguous. A provision of LVL0 or LVL1 is NEVER read to require a particular language, library, tool, technology, platform, process, or method; such a reading is wrong.

#### GOV.3 Rulings

. Instantiates .

The human owner interprets this document for a project and rules on questions referred to it. Each ruling is recorded, governs the project, and MAY be appealed to the custodians, whose recorded interpretations bind every project.

#### GOV.4 Principle conflicts

. Instantiates .

Where a provision addresses a matter expressly, it states what the principles require in that matter; a principle supplies the reading only where the provisions are silent or ambiguous. An apparent conflict between a principle and a provision is referred to the human owner for review and ruling (GOV.3), and the ruling is reported to the custodians as an amendment proposal (GOV.40).

### Precedence

#### GOV.5 Order of precedence

. Instantiates .

The prime directives outrank every other provision. The Articles then rank as follows, highest first: (a) safety, security, and data integrity (GUARD); (b) correctness and honest evidence (VV); (c) reproducibility and traceability (REPRO); (d) interpretability and situational awareness (INTPR); (e) contractual, modular design (DSGN); (f) simplicity (SIMPL); (g) resources (RSRC); (h) process (QA). A provision below LVL0 ranks with the LVL0 provision it instantiates. The Governing Principles are not ranked, and GOV governs how all provisions apply and is not ranked. The order in which provisions appear carries no rank.

#### GOV.6 Recorded concession

. Instantiates .

When two provisions of different rank conflict, the higher-ranked governs; when provisions of equal rank conflict, the more restrictive governs, and an agent halts and refers (PRIME.14). The lower-ranked yields only to the minimum extent required, and only for as long as the conflict lasts, and the concession is recorded.

#### GOV.7 Verification cost

. Instantiates .

Verification cost NEVER justifies skipping verification. A component too expensive to verify by one means is verified by a cheaper one (VV.1); if no means exists, its results are reported as unverified (PRIME.3).

#### GOV.8 Hardware constraints

. Instantiates .

A footprint, timing, precision, or power limit imposed by the executing hardware is part of the contract (DSGN.5) and is honored as correctness; it belongs to VV rather than competing with it.

#### GOV.9 Ambiguity

. Instantiates .

When a provision of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or QA admits two readings, the reading that produces more evidence governs; among readings equal in evidence, the more explicit; among those, the simpler. The reading applies at the level the consequence class sets (GOV.11); an ambiguity in a floor obligation itself resolves to the reading that produces more evidence. When a prime directive, a provision of GUARD or GOV, or a permission for an agent's action admits two readings, the more restrictive governs, and an agent unable to tell halts and refers (PRIME.14). A reading so resolved governs until the provision is interpreted (GOV.3) or amended (GOV.40), and the judgment is recorded (PRIN.10).

### Consequence and proportionality

#### GOV.10 Floor

. Instantiates .

Every piece of work, at every consequence class, meets a floor: the prime directives; GUARD and GOV; source under version control (REPRO.5); a definition of done for each unit of work (QA.1); documentation enough for a human and an agent to understand its purpose and use (INTPR.2); and tests for basic correctness and regressions (VV.7). At the floor, the mechanisms the prime directives, GUARD, and GOV require are met by the defaults (GOV.22).

#### GOV.11 Proportioned obligations

. Instantiates .

Above the floor, every obligation of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, and QA, and of every lower provision that instantiates one, is proportioned to the consequence class of the work and the reliance placed on it, both of which the proportionality judgment states (GOV.50), NEVER to the setting or hardware of the work (PRIN.9). Exploratory overhead is kept as low as the floor allows, and lower governance SHALL NOT raise the floor except by a recorded project decision naming the consequence that warrants it.

#### GOV.12 Consequence classes

. Instantiates .

The consequence class of work is the most severe class reached by the worst credible consequence of an error in it, harm included, or by the reliance placed on it. The classes, most severe first, are:
- **CSQ0 Safety-critical.** An error is able to cause injury, death, or severe environmental harm, directly or through a safety decision the output informs.
- **CSQ1 Mission-critical.** An error is able to cause major, hard-to-reverse loss, such as destroyed equipment, irreplaceable data or samples, a failed campaign, or large cost, without credible injury; or the output is relied upon outside the project or by systems that act unattended.
- **CSQ2 Relied upon.** An error is able to cause wrong decisions or designs, recoverable with substantial rework; the output is relied upon beyond its author.
- **CSQ3 Internal.** An error wastes effort and is caught cheaply and reversed; the output is relied upon only by its author or immediate team, feeding work that is verified later.
- **CSQ4 Exploratory.** An error costs nothing beyond the author's own time; nothing is relied upon without promotion (QA.11).

Detailed criteria for each class are LVL2 standards. A profile MAY require work in its domain to be classified at least as severe as a stated class.

#### GOV.13 Class assignment

. Instantiates .

The human owner sets the project's consequence class at inception, as the most severe class of the uses then made of its outputs, and MAY revise it throughout the project's life. Where a more severe use is planned, the classification records the class of that use as the expected class, adopted with the classification (GOV.24) and setting no class before that use begins (GOV.14). The human owner MAY record a less severe class for a component shown to be isolated from the more severe outputs. No class is assumed by default: where none is recorded, the work meets the floor (GOV.10), and an agent that needs the class to promote, release, deploy, or drive physical hardware halts that line of work and refers (PRIME.14).

#### GOV.14 Class follows use

. Instantiates .

A consequence class attaches to the use of work, not to its code. The class moves toward CSQ0 whenever reliance or exposure grows, and away from CSQ0 only by recorded decision of the human owner. Work moved to a more severe class meets that class's obligations before it is relied upon at that class; nothing is grandfathered.

#### GOV.15 Physical harm

. Instantiates .

Where the human owner states that a credible path to physical harm exists, the work is CSQ0 whatever the other dimensions indicate. An agent NEVER makes that determination; it MAY warn the human owner of scenarios that are able to pose physical harm.

### Levels and derivation

#### GOV.16 Levels

. Instantiates .

Governance is organized in four levels, each adopted by a narrower authority than the one above it: LVL0, this constitution; LVL1, profiles of domain obligations; LVL2, standards and defaults that apply across projects; and LVL3, the instruments of one project. Only LVL0 carries constitutional force in its own right; every lower level binds by derivation (PRIME.15).

#### GOV.17 Inherited force

. Instantiates .

A provision below LVL0 inherits the rank and waivability of the provisions it instantiates and SHALL NOT be assigned a lower rank or a looser waivability. A provision that instantiates a prime directive is non-waivable.

#### GOV.18 Specificity downstream

. Instantiates .

Choices of language, library, tool, technology, platform, process, and method belong at LVL2 and LVL3. LVL0 and LVL1 name none of them, so a change to those choices leaves LVL0 and LVL1 unchanged. A limit, beyond those this document sets, on the number of agents that an agent directs, on the depth of delegation, or on network access made to retrieve information for research belongs at LVL3 alone.

#### GOV.19 Binding and default

. Instantiates .

Each LVL2 provision is marked binding or default. A provision is marked binding only where it instantiates a prime directive, GUARD, or a floor obligation (GOV.10), or where the custodians record why uniformity across projects requires it; every other LVL2 provision, including every provision of form or style, is a default. A binding provision is only tightened below it; a default provision MAY be replaced at LVL3 by an alternative that meets the same higher-level outcome, recorded as a decision (REPRO.7).

#### GOV.20 Project constitution

. Instantiates .

Every project that promotes a result other than through its adopted classification (QA.11), releases software, or drives physical hardware has a project constitution: a LVL3 instrument that inherits from and aligns with the levels above it, cites the provisions it instantiates, adds only project-specific obligations, and relaxes none (PRIME.15).

#### GOV.21 Project mechanisms

. Instantiates .

The project constitution defines the mechanisms this document requires of every project: the work process (QA.2), the stopping rule (QA.3), defect tracking (QA.4), review (QA.7), correction propagation (QA.13), incident handling (QA.15), dependency management (REPRO.9), retention (REPRO.12), the classification and consequence class (GOV.13, GOV.24), the working-notes workspace (INTPR.5), the threat model (GUARD.16), the reserved-action register (GUARD.4), the authorization mechanism (GUARD.10), and the agent instructions (PRIME.14, GOV.48).

#### GOV.22 Defaults

. Instantiates .

Work without a project constitution operates under defaults that the custodians adopt as LVL2 standards. No default grants an authorization, adopts a hazard analysis, sets a consequence class, or authorizes an estimate; only the human owner does.

### Profiles

#### GOV.23 Universality

. Instantiates .

The prime directives and General Articles are stated as outcomes that every domain and every piece of hardware is able to satisfy. They bind all covered work, whether or not a profile applies.

#### GOV.24 Classification

. Instantiates .

Each project's classification records its consequence class and the attributes of its work that profile selectors test. The classification (GOV.50) is revised whenever the work changes in a way a selector tests.

#### GOV.25 Profile selection

. Instantiates .

Every profile whose selector is true for a project's classification binds that project in full, and a project MAY select more than one. A conflict between selected profiles resolves under the order of precedence (GOV.5).

#### GOV.26 Profile consistency

. Instantiates .

Each profile states its selector, which is decidable from classification attributes, and cites the LVL0 provisions each of its provisions instantiates. It defines its own terms without redefining a LVL0 term, and it contradicts no other profile.

#### GOV.27 Sub-profiles

. Instantiates .

A sub-profile inherits its parent profile in full and adds only obligations specific to its subtype.

#### GOV.28 Profile admission

. Instantiates .

A profile or sub-profile is admitted, without amendment to LVL0, when it meets GOV.26 and the custodians adopt it (GOV.41). Projects whose classification it selects conform within a recorded transition period (GOV.42).

#### GOV.29 Unprofiled work

. Instantiates .

Covered work in a domain no profile addresses is governed by LVL0, and by the nearest profile applied by analogy, with the choice of analogue recorded, until a profile for it is admitted.

#### GOV.30 Constitutional scope

. Instantiates .

This document binds computational and cyber-physical systems and the work done on them, which is the covered work. General business and web software are outside it until an admitted profile whose selector names that software brings it in; from then on, LVL0 binds it in full. Matters the Preamble assigns to parallel governance are outside this document, and no provision is read to govern them.

#### GOV.31 Profile pruning

. Instantiates .

A profile provision that restates a higher provision without domain-specific content is removed. A profile for a retired domain or hardware type is retained only while results produced under it remain in use (REPRO.1).

### Knowledge

#### GOV.32 Knowledge without authority

. Instantiates .

Acquired knowledge, such as methods, prior art, research and negative results, lessons learned, and trends, is kept in a knowledge base apart from governance. A knowledge entry informs the work and NEVER governs it; it carries no instruction authority (PRIME.11). An entry that SHOULD bind becomes a provision only by adoption at the lowest level able to hold it.

#### GOV.33 Reliance ceiling

. Instantiates .

Each knowledge entry records its evidence and its evidence level, from EVD0 verified through EVD3 anecdotal. The evidence level caps the most severe consequence class at which the entry is relied upon without fresh verification; the ceiling for each level is a LVL2 standard. Reliance above the ceiling requires the evidence VV requires at the class concerned.

#### GOV.34 Knowledge lifecycle

. Instantiates .

A knowledge entry is established only on review by an actor other than its author and is revalidated on a recorded schedule. It is superseded or retracted, NEVER altered in place (PRIME.5), and everything that relies on it is notified (QA.13).

### Governance records

#### GOV.35 Corpus

. Instantiates .

The text of every provision at every level is kept in plain, versioned files that a human is able to read without special software. This corpus is authoritative; every rendered document, index, and manifest is generated from it and NEVER substitutes for it.

#### GOV.36 Ledger

. Instantiates .

Every change to governance at every level, and every adoption, classification, authorization, waiver, ruling, and promotion, is entered as a transaction in an append-only, tamper-evident ledger that records its actor, role, authority, and rationale. The current state of governance is derivable from the corpus and the ledger alone. A change made outside the ledger is a defect.

#### GOV.37 Stable identifiers

. Instantiates .

Every provision, knowledge entry, and tag has a stable identifier that is NEVER reused or renumbered. Identifiers are built from mnemonics, so that an identifier names its document or Article; the identifier scheme is a LVL2 standard. An ordinal scale appends one digit to its mnemonic, numbered from 0 for the highest authority, severity, or strength (LVL0, CSQ0, EVD0). Mnemonics are held in a register that changes only by ledger transaction. Section, level, and rank are attributes of a provision, not parts of its identifier.

#### GOV.38 Harness

. Instantiates .

Software that stores, checks, renders, or serves governance holds no authority of its own; it implements governance and is governed as software. If it is lost, the corpus, the manifests, and the ledger remain sufficient for a human skilled in the art to read, apply, and audit governance (INTPR.12).

#### GOV.39 Manifests

. Instantiates .

A manifest lists provisions or knowledge entries for lookup and is informative; before relying on a provision, an actor reads its full text. A manifest that does not match the corpus it was generated from is stale and is regenerated before use.

### Change

#### GOV.40 Amendment

. Instantiates .

A provision of this document is added, altered, or removed only by decision of the custodians, on a recorded proposal stating the provision, the change, the reason, the alternatives weighed, and the lower governance affected. A change takes effect when recorded in this document's revision history and entered in the ledger (GOV.36).

#### GOV.41 Adoption

. Instantiates .

The custodians adopt this document, the LVL1 profiles, and the LVL2 standards; they MAY delegate a standard to an owner they name, who then adopts it. A project's human owner adopts that project's LVL3 instruments.

#### GOV.42 Transition

. Instantiates .

Each adopter reviews the lower provisions a change affects and conforms them within a transition period the custodians record; work conforming to the prior revision during that period is not in defect.

#### GOV.43 Versioned governance

. Instantiates .

Governance at every level is versioned, reviewed, and attributed as code is (REPRO.5, QA.7), and its history is preserved (PRIME.5).

#### GOV.44 Waiver

. Instantiates .

Above the floor (GOV.10), a waiver MAY relieve an obligation of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or QA, or of a lower provision that instantiates one, for a named component, for a stated reason and duration, by a recorded decision of the human owner. A waiver names the provision, the risk accepted, and the condition under which it expires. Relying on an expired waiver is a defect. A waiver is the form an exception under PRIN.10 takes when it departs from a provision.

#### GOV.45 Non-waivable obligations

. Instantiates .

The Governing Principles, the prime directives, GUARD, GOV, the floor (GOV.10), and every provision at every level that instantiates a prime directive SHALL NOT be waived.

#### GOV.46 Constitutional review

. Instantiates .

This document is reread in full at an interval the custodians record, and each profile and standard is reviewed at an interval its adopter records. Each review records whether a provision has been routinely waived, ignored, or found ambiguous; each such finding is an amendment proposal.

#### GOV.47 Compliance audit

. Instantiates .

Each project's compliance with this document and its lower governance is audited at an interval proportioned to its consequence class. The project reports its waivers, rulings, recorded ambiguities, and governance failures to the custodians.

### Agents in governance

#### GOV.48 Agents bound

. Instantiates .

Agents acting on covered work are governed by agent instructions derived under PRIME.15, and are held to the prime directives, GUARD, and INTPR.11 for every action.

#### GOV.49 No self-adoption

. Instantiates .

An agent SHALL NOT adopt, put into force, or alter in force governance, whatever its level, its own instructions included. It MAY draft and propose changes, which only their adopter (GOV.41) adopts.

#### GOV.50 Owner-adopted judgments

. Instantiates .

Judgments that set the burden on the work are adopted only by the human owner, and an agent MAY draft them: the classification, consequence class, and proportionality judgment (GOV.11, GOV.13, GOV.24); promotion (QA.11); axioms (VV.9); the hazard analysis (PRIME.13); the reserved-action register and its exempt classes (GUARD.4, GUARD.7); estimates for implicit expenditure (PRIME.8); and the decision to release or deploy (QA.10).

#### GOV.51 Agent designation

. Instantiates .

Software that meets the definition of an agent, or that is not shown to execute only a fixed specification, is treated as an agent until the human owner records otherwise. Software an agent invokes acts within that agent's tiers and authority (PRIME.12).
