---
id: "STND.THRT"
level: "LVL2"
kind: "standard"
title: "Threat-model template"
status: "adopted"
revision: "1.0"
adopted: "2026-10-20"
adopted_by: "The Custodian"
instantiates: ["GOV.21", "GUARD.16"]
rank: null
waivable: false
---

## Purpose and scope

This standard fixes the form and minimum content of the threat model that a project constitution holds (GUARD.16, GOV.21): a table of assets, threats, sources, and protection, carrying at least the rows of the defaults (STND.DFLT.18) and a row for compromise of fetched components; the protected data, the readers trusted with secrets, and the channel for reporting a secret (PRIME.10); how alteration of the records is detected (PRIME.5); the events that call for a proposal to review it; the separation of its sensitive part (GUARD.18); and two secure practices that every actor follows unless the threat model records an alternative (GUARD.17). Every provision but STND.THRT.8 instantiates a prime directive or GUARD, so it is binding and applies at every class; STND.THRT.8 is a default. No provision names a tool (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Asset | A thing of value to the work that a threat model names: source, data, results, records, credentials, hardware, people, or a system the work reaches. |
| Control | A means that prevents a threat to an asset or detects its occurrence. |
| Protected data | A location or kind of data that a threat model lists under STND.THRT.3. A row that the project protects names a protected asset, which is not by that alone protected data. |

## Notes

The rows of STND.DFLT.18 are the minimum because each protected row there rests on a prime directive: change beyond authority on PRIME.5 and PRIME.7, disclosure of secrets on PRIME.10, action beyond authorization on PRIME.7 and PRIME.9, injected instructions on PRIME.11 and GUARD.16, and fabricated evidence on PRIME.2. STND.THRT.2 adds the row for compromise of fetched components through their supply chain, against which the integrity and advisory provisions of the dependency policy are the controls. A fetched component is an asset the work depends on, so the row for fetched components governs for it over the row of STND.DFLT.18 that leaves compromise of the work and the provisioned environment unprotected. A project adds rows and protects more; it does not unprotect those. For a project whose constitution adopts this standard, STND.THRT.2, with the integrity and advisory provisions of the dependency policy, protects more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites these standards is the recorded decision (GOV.11). The rows that the project marks as not protected are the separate statement of what it does not attempt to protect (GUARD.16).

STND.THRT.3 makes concrete the protected data that PRIME.10 and the working bounds of STND.DFLT refer to, a store of AGENT.44 and its readers included where the work keeps one, and keeps the list readable, because an agent avoids only what it is able to see. It also names whom the threat model trusts with a secret, the test that the term Secret of AGENT and STND.THRT.4 rely on. STND.THRT.4 gives the secret-report channel of PRIME.10, which the threat model states as the human owner directly where it designates no other; the channel is one that no untrusted reader sees, so that the report does not itself disclose. STND.THRT.5 asks only that the project say how alteration is detected, by chained hashes, signatures, or another means of its choice.

The events of STND.THRT.6 always change exposure; GUARD.16 still asks for a review at every other change of exposure. A routine retrieval from a new site changes exposure only where the site is of a kind of source that the threat model does not name. The actor that brings an event about or learns of it records it and proposes the change it calls for; the human owner adopts the revised threat model, and every line of work that the event does not concern continues (AGENT.15). Coming to hold irreplaceable data, or an asset or source of threat that the model omits, is one of these events, the counterpart under a project constitution of STND.DFLT.19. A review before each release is recommended.

STND.THRT.7 keeps the sensitive part of a threat model apart, outside version control and every record and readable only by those the threat model trusts with it, so that the access controls of GUARD.18, to the extent the human owner records as practical, restrict only that part, while every actor reads the rest, which INTPR.12 needs. The part stays out of versioned records, because PRIME.10 bars secrets there; the rest cites it, and each change to it is entered in the ledger by reference (GOV.36). STND.THRT.8 is a default proportioned to class under REPRO.13, applying from CSQ3 under STND.CLASS.10.

STND.THRT.9 carries the two practices of the undivided draft it replaces that LVL0 does not already state: least privilege for each account, key, and token that the work provisions, and no weakening of a security or integrity check to make an action succeed, other than the recorded routes of QA.6, VV.3, and STND.CODE.4, each stated in the work report. The others, no secrets in source and records, validation of untrusted input, and integrity of fetched components, are PRIME.10, DSGN.2, and the dependency policy. Work without a project constitution uses the threat model of STND.DFLT.18 and STND.DFLT.19.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.DFLT | Defaults |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
