# Package P5: References gaps, judged and closed

Round of 2026-10-25 (close), package P5. Corpus at ledger entry 147. This record covers the 20 documents that `tools/check_refs.py` reports, other than STND.CODE (P1) and STND.MPI (P4).

## How References are derived

`govharness/derive/references.py` (`cited_documents`) reads the text of a document and of its provisions, with the References section removed and quoted spans blanked, and collects:

- provision and term identifiers (`ID_RE`, such as `HW.6` or `LEX.relying-party`) and locators (`LVL0#normative-language`);
- a document identifier written alone in parentheses, such as `(AGENT)` (`DOCUMENT_IN_PARENS_RE`);
- the identifiers in the fields `cites`, `governed_by`, `instantiates`, and `refers_to`.

Each identifier counts toward the document it belongs to. A bare document name, such as "MEAS binds them", is not read, so `references --check` (g.25) passes while `check_refs.py` reports the name. g.25 reads only documents at LVL1 to LVL3 (`checks/drafting/context.py`, groups `self`, `lower`, `draft`). STND.DRAFT.34 asks only documents below LVL0 to hold References. LVL0, its parts, and the entries whose level is null (MNEM, KNOW, TAG and its facets) have no References section.

`check_refs.py` means to drop the revision history, but its pattern reads `## Revision history` while the corpus heading is `## Revision History` (`core.tables.HISTORY_HEADING`). So history rows are read too.

## Gaps

"Real" means that a document at LVL1 to LVL3 names another document as part of its text, so that STND.DRAFT.34 asks for the row. Each real gap is closed by a citation in informative text, from which the row is derived again. No provision body, term, or obligation changes.

| Document | Name | Where | Real | Fix, or reason it is not real |
| --- | --- | --- | --- | --- |
| CPS | MEAS | Terms (Observation, "the term that MEAS defines"); Selector Notes | Yes | Selector Notes cite MEAS.1: "MEAS binds them as well once a reported result rests on them (MEAS.1)." CPS 1.0.1. |
| HDES | HDES.FPGA, HDES.ASIC | Purpose; Selector Notes | Yes | Selector Notes cite HDES.FPGA.1 and HDES.ASIC.1 where the sub-profiles give an attribute of HDES.1. HDES 1.0.2. |
| HDES | HDES.ASIC | Notes on release for fabrication | Yes | Cites HDES.ASIC.12, the fabrication readiness record. HDES 1.0.2. |
| HDES | HW.EMBED | Notes on processors in programmable logic | Yes | Cites HW.EMBED.1: "is not bound by HW.EMBED (HW.EMBED.1)". HDES 1.0.2. |
| HDES.ASIC | HW.ASIC, MEAS | Selector Notes; table of where the rest lives | Yes | Selector Notes cite HW.6, HW.ASIC.4, and MEAS.1, as the table already does for HW.6. HDES.ASIC 1.0.2. The history row 1.0.1 also names both; it is not a citation. |
| HW | HW.CPU, HW.GPU, HW.QPU, HW.EMBED, HW.FPGA, HW.ASIC | Purpose; Selector Notes | Yes | Selector Notes cite the six sub-profile selectors, each of which gives one attribute of HW.1 (STND.DRAFT.36), in the form HDES already uses. HW 1.1.2. |
| HW.CPU | SIMPL | Class-onset Notes: "instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC" | Yes | No HW.CPU provision instantiates SIMPL, so citing it would be false. The sentence now names only the Articles that the provisions instantiate: VV, REPRO, INTPR, DSGN, RSRC. HW.CPU 1.0.1. |
| HW.EMBED | SIMPL | The same sentence | Yes | As HW.CPU: VV, REPRO, INTPR, DSGN, RSRC. HW.EMBED 1.0.2. |
| HW.FPGA | HW.EMBED | Notes on processors in programmable logic | Yes | Cites HW.EMBED.1. HW.FPGA 1.0.1. |
| HW.GPU | HW.CPU | Selector Notes (host code) | Yes | Cites HW.CPU.1. HW.GPU 1.0.1. |
| HW.GPU | DSGN, INTPR, REPRO, SIMPL, VV | The same class-onset sentence | Yes | HW.GPU.4, the only provision the sentence covers, instantiates RSRC alone. The sentence now reads "instantiates only RSRC, inherits its rank and waivability". HW.GPU 1.0.1. |
| HW.QPU | HW.CPU, HW.GPU | Selector Notes (simulation) | Yes | Cites HW.CPU.1 and HW.GPU.1. HW.QPU 1.0.1. |
| HW.QPU | DSGN, SIMPL | The same class-onset sentence | Yes | The provisions instantiate VV, REPRO, INTPR, and RSRC, and the sentence now names those. HW.QPU 1.0.1. |
| ML | AGENT, GUARD | Selector Notes | Yes | The Notes mean the whole documents, so the citation is the parenthesized identifier: "the agent practice profile (AGENT) and the Safeguards Article (GUARD)". ML 1.0.1. |
| STND.CLASS | SIMPL | Body of STND.CLASS.10 ("every obligation of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, and QA") | Yes | The body stays as it is. The Notes state what the table holds: "no part of Simplicity (SIMPL) is among them". STND.CLASS 1.3.1. |
| STND.DFLT | STND.INSTR | Notes ("Command-level practice ... belongs to STND.INSTR") | Yes | Cites STND.INSTR.4 (dry run) and STND.INSTR.5 (halt on a failed step). STND.DFLT 1.5.1. |
| STND.IDENT | MNEM | Body of STND.IDENT.19 and .20; Checks Notes | Yes | Bodies stay as they are. MNEM holds no provision, so the Notes use the parenthesized identifier: "The mnemonic register (MNEM) is the file `MNEM/_doc.md`." STND.IDENT 1.3.3. |
| STND.IDENT | HW.FPGA, TAG.METH, NUMER | Table "Examples of identifiers" | No | The identifiers are examples of a form, not citations. NUMER, in "a space NUMER", is the name of a knowledge space, not the profile. |
| STND.KNOW | KNOW, TAG, TAG.COMP | Notes on the shared knowledge base | Yes | The Notes govern these entries and point the reader to them, so the parenthesized identifiers are used: "(KNOW)", "(TAG)", "The component facet (TAG.COMP)". STND.KNOW 1.0.1. The entries are planned and of level null; no check objects to the rows. |
| LVL0 | SIMPL, RSRC | Normative Language table; the list of LVL0 mnemonics | No | LVL0 holds no References, and STND.DRAFT.34 does not ask it to. The parts are parts of LVL0 itself. |
| LVL0 | STND.DRAFT | Revision History, row 1.2 | No | A history row only, kept by the heading mismatch in `check_refs.py`. |
| PRIME | VV | Body of PRIME.3 | No | An LVL0 part, which has no References; VV is another part of the same constitution. |
| INTPR | VV | Body of INTPR.11 | No | As PRIME. |
| RSRC | SIMPL | Body of RSRC.6 | No | As PRIME. |
| SIMPL | VV | Body of SIMPL.11 | No | As PRIME. |
| MNEM | AGENT, CPS, DSGN, HDES, HW, INTPR, KNOW, LEX, MEAS, ML, NUMER, PRIN, QA, REPRO, RSRC, SIMPL, STND, TAG | Register rows (Mnemonic and Parent columns) | No | The register lists every mnemonic as data. It has level null and no References, and changing it takes a register transaction (STND.IDENT.20, check v.11). |

## Exclusions proposed for unit 0013

When g.25 also reads bare document names, it is meant to agree with the derived table without asking any change for the gaps above that are not real:

1. **Scope.** Read the documents g.25 already reads, those at LVL1 to LVL3. This leaves out LVL0 and its parts, and the entries of level null (MNEM, KNOW, TAG, and its facets). Keep the present exclusion of the name LVL0.
2. **Revision history.** Remove the section by `HISTORY_HEADING`, not by a pattern of its own, so that the heading cannot drift. `tools/check_refs.py` has that bug now.
3. **Tables of examples.** Skip every row of a table whose header names a column `Example`. The only such table is the one in STND.IDENT. The whole row is skipped, because its Item cell ("a space NUMER") also names an identifier in mention.
4. **Mentions.** Keep the present removal of quoted spans and code spans.

`check_refs_0013.py`, in this directory, applies rules 1 to 3. On the rehearsed corpus it reports only STND.CODE and STND.MPI, the gaps of P1 and P4. On the live corpus it reports the 14 real gaps above, plus those two.

## Amending LVL0, for the record

No LVL0 change is proposed. An LVL0 amendment would need:

- a decision of the custodians on a recorded proposal that states the provision, the change, the reason, the alternatives weighed, and the lower governance affected (GOV.40);
- a row in the LVL0 Revision History, citing GOV.40 (not GOV.41), with `revision` in `LVL0/_doc.md` raised from 1.6;
- a ledger transaction of type amend, authority `["GOV.40"]`, target `LVL0` (and any term changed), scope all thirteen LVL0 directories, as in entries 2 to 7.

`ratified_by: "The Custodian"` stays as it is. Closing the LVL0 "gaps" would mean either adding a References section, which STND.DRAFT.34 does not ask of LVL0, or replacing an Article name such as VV in PRIME.3 by one of its provisions. The second narrows what the provision refers to, so it is not editorial under STND.IDENT.3.

## Rehearsal

On a copy of the corpus at entry 147, from `harness/`: `python3 -B -m govharness rehearse <copy> ../tools/amendment-scripts/apply_close_p5.py` appends entries 148 to 161, one per document. Results:

- `verify`: every family PASS. One warning, g.18, is present at entry 147 as well.
- `references --check`: PASS.
- The drafting findings (`tools/findings.py`) are the same as at entry 147, with no finding of class defect.
- `tools/check_refs.py` reports 9 documents. Two are STND.CODE and STND.MPI. The other seven (LVL0, PRIME, INTPR, RSRC, SIMPL, MNEM, STND.IDENT for its examples) are the gaps above that are not real.
- The rehearsal does not touch the live corpus ("source unchanged").

The reading copies in this directory are composed from the rehearsed corpus. Their ledger entry numbers (148 to 161) are those of the rehearsal; the coalesce sets the final ones.
