# Programmable logic design (HDES.FPGA) 1.0.2

Adopted by The Custodian as revision 1.0 in ledger entry 73 (2026-10-18); revised to 1.0.1 in entry 86 (2026-10-19) and 1.0.2 in entry 251 (2026-10-28). This reading copy is composed from the per-provision files in HDES/FPGA/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This sub-profile holds the obligations specific to designs realized as configurations of programmable logic. It inherits HDES in full and adds only what this realization makes likely to go wrong silently or unsafely before or at loading (GOV.27): a target model, pin assignment, electrical standard, or output state during configuration that does not match the board, a configuration that cannot be traced to its design, and an update that leaves a deployed device unusable or accepts a configuration of unknown origin. Each provision is checked by comparing records or by verifying the design. It names no language, tool, vendor, or device family (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Configuration | The realization of a design as programmable logic: the data that configures a device of a stated model. |
| Target model | The model of programmable logic device, with each variant that changes its timing or electrical models, for which a configuration is produced. |
| Board record | The record of a board of a stated revision, taken from its design record or documented specification or from its inspection, of the device on the board, each connection of its pins, and the electrical level and default state of each connected circuit. |

## Selector

HDES.FPGA.1 states the selector: the attribute Programmable logic design, which HDES defines and which HDES.1 also gives (STND.DRAFT.36). Each provision names a design or its configuration, or a record of one, as its subject (STND.DRAFT.37). Verification on a configured device and execution on it are governed by HW and its sub-profile HW.FPGA.

## Where the rest lives

LVL0 and the documents named here already govern these matters of hardware design, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Design record, contract, verification, equivalence, warnings, timing, crossings, initial state, margins, saturation, mitigation | HDES.3 to HDES.15 |
| Verification on a configured device, and execution on it, a processor realized in it included | HW.6, HW.FPGA |
| Configuring or powering physical hardware | PRIME.7, PRIME.13 |

## Notes

Where a configuration is part of an execution path, HDES.5 marks the properties that rest only on analysis or simulation, behavior at the pins and interaction with the rest of the board among them. Their confirmation on a configured device, or a statement that they are unconfirmed, is asked by HW.FPGA.4; it is outside this sub-profile.

A wrong target model, a pin assigned to the wrong package pin, an output driven at a voltage the board does not expect, or an output that drives an external circuit while the device is still configuring can damage the device or the board on first load. HDES.FPGA.3 checks all four against a board record of each board revision before the first load on it, which costs a comparison of tables. A breadboard front end without a design record has its board record made by inspection. Loading a configuration into a device that commands, configures, or powers physical hardware needs the authorization of PRIME.7 and the owner-adopted hazard analysis and verified safe state of PRIME.13; a load that the hazard analysis marks as hazardous or irreversible is reserved (PRIME.6).

A configuration whose identity is reported, read back, or recorded with the read-back of its write lets every result computed on it name its design record (HDES.FPGA.4), and HW.3 then records it with each result. Where a design is updated through an interface of its deployed system, HDES.FPGA.5 keeps a failed update from leaving the device without a working configuration, typically by a fallback configuration that reports its own identity, and, where outsiders can reach that interface, keeps the device from loading a configuration of unverified origin. Both behaviors are verified on the design, by simulating an interrupted update and a configuration of wrong origin. Signing a configuration needs a key, which an agent does not store beyond the action that uses it (AGENT.45); the signature is applied at the release that the human owner decides (QA.10). A bench board that its programming interface always restores meets HDES.FPGA.5 through that interface. A fallback configuration that drives physical hardware holds it in the designed safe state of PRIME.13.

HDES.FPGA addresses one matter (HDES.FPGA.2): the design record of a realized design, which HDES owns, through HDES.FPGA.3 and HDES.FPGA.4, which cite HDES.3.

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, or DSGN, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HW | Execution hardware |
| HW.FPGA | Field-programmable gate arrays |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| VV | Correctness |

## Provisions

### Application

#### HDES.FPGA.1 Programmable logic design selector

Instantiates GOV.25, GOV.26, GOV.27.

This sub-profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26, GOV.27).

| Attribute | Defined by |
| --- | --- |
| Programmable logic design | HDES |

#### HDES.FPGA.2 Programmable logic design shared matters

Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Design record of a realized design | HDES | HDES.FPGA.3, HDES.FPGA.4 |

### Board interface

#### HDES.FPGA.3 Board check before loading

From CSQ3. Instantiates DSGN.5, DSGN.4, VV.1.

Before a configuration of a design is first loaded into a device on a board of a given revision, the design record under HDES.3 SHALL hold a board record of that revision (DSGN.5). Before a configuration of a design is first loaded into a device on a board of a given revision, its target model, its assignment of pins, and the electrical standard of each input and output SHALL be checked against that board record (DSGN.4, DSGN.5, VV.1). Before a configuration of a design is first loaded into a device on a board of a given revision, the state of each of its outputs during power-on, configuration, and reconfiguration SHALL be checked against that board record (DSGN.4, VV.1).

### Identity

#### HDES.FPGA.4 Configuration identity

From CSQ3. Instantiates REPRO.1, REPRO.4.

Each configuration of a design SHALL carry an identity, reported by the device, read from it, or recorded with the read-back of each write of the configuration to the device or its configuration memory, that traces a result computed on it to the design record of HDES.3 (REPRO.1, REPRO.4).

#### HDES.FPGA.5 Deployed configuration updates

From CSQ3. Instantiates DSGN.5, VV.1.

Where a design's configuration is updated through an interface of its deployed system, each failed or interrupted update SHALL leave the device in a verified configuration that accepts a further update, or in a state from which the deployed system restores such a configuration through an interface it provides (DSGN.5, VV.1). Where that interface is reachable by an actor outside the project, the design SHALL load through it only a configuration whose integrity and origin the device or its deployed system has verified (DSGN.5, VV.1).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative text describes HW.FPGA as adopted, citing HW.FPGA.4; no obligation changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
