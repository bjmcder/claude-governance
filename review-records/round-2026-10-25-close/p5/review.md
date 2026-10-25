# Cold review of package P5 (References gaps, 14 editorial amendments)

## Verdict
No Defect. Two Should-fix items on wording, three Optional. Adopt after the Should-fix edits.

## Verified by script
- Fresh rehearsal gives entries 148 to 161, one per document. The source corpus is unchanged.
- `verify`: all families PASS; the only warning is the g.18 warning present at entry 147. `references --check`: PASS.
- `findings.py` on the 14 documents prints nothing, on the copy and on the live corpus.
- `check_refs.py`: 48 documents checked; only STND.CODE and STND.MPI remain (P1, P4).
- A diff of the copy against the live corpus (ledger and manifests aside) shows only the intended lines: citations, References rows, revision field, history row. No provision file changes.
- All 14 rationales end with the exact tail, cite GOV.41, hold a Transition sentence, and cite no entry but "entry 15" in the tail. Revisions are right (IDENT 1.3.2 to 1.3.3; EMBED, HDES.ASIC, HDES 1.0.1 to 1.0.2; HW 1.1.1 to 1.1.2; DFLT 1.5 to 1.5.1; CLASS 1.3 to 1.3.1; the rest 1.0 to 1.0.1). History rows match the rationales. Reading copies carry the amended sentences.

## 1. Editorial under STND.IDENT.3
I read `instantiates` of every provision of the four sub-profiles:

| Sub-profile | Articles instantiated (not selector or shared matters) | New sentence |
| --- | --- | --- |
| HW.CPU | DSGN, REPRO, VV, INTPR, RSRC | VV, REPRO, INTPR, DSGN, RSRC: match |
| HW.EMBED | RSRC, VV, DSGN, REPRO, INTPR | same five: match |
| HW.GPU | RSRC (HW.GPU.4; HW.GPU.3 is PRIME.4, named separately) | RSRC alone: match |
| HW.QPU | REPRO, VV, INTPR, RSRC | VV, REPRO, INTPR, RSRC: match |

No provision instantiates SIMPL, and none in HW.GPU or HW.QPU instantiates DSGN. The dropped names remove nothing from the closure that fixes rank, waivability, and onset. The CSQ statements after them are untouched, so the onset meaning is unchanged.

## 2. Citations
All hold what the sentence draws on.
- HW.CPU.1, HW.GPU.1, HW.QPU.1, HW.EMBED.1, HW.FPGA.1, HW.ASIC.1, HDES.FPGA.1, HDES.ASIC.1, and MEAS.1 are selectors with the attribute in question. HW.EMBED.1 reads with the HW Terms, where Embedded controller excludes programmable logic.
- HDES.ASIC.12 is the Fabrication readiness record; HW.6 is Contract evidence; HW.ASIC.4 is Fabricated-device evidence; STND.INSTR.4 is the dry run and .5 the halt on a failed step.
- AGENT is "Agent practice" and GUARD "Safeguards". KNOW, TAG, and TAG.COMP exist (planned, level null) and their titles match the rows.
- The sentences read naturally. The KNOW sentence is reworded so that the identifier is parenthesized; its sense is kept.

## 3. Gaps judged not real
- g.25 (`references_listed`) scans units of group BELOW. `cut_units` builds informative or body units only for entries at LVL1 to LVL3 that are not terms. LVL0 provisions go to group `lvl0`, and level-null entries (MNEM, KNOW, TAG) are never cut. So "LVL1 to LVL3" describes g.25 exactly. STND.DRAFT.34 reads "Each document below LVL0"; applying that to level-null entries is a reading, and a sound one.
- LVL0 parts (PRIME, INTPR, RSRC, SIMPL) name each other as parts of one constitution. The LVL0 history row names STND.DRAFT in a row only. MNEM is a register of data.
- STND.IDENT examples: the table has an Example column, its identifiers are forms, and "a space NUMER" names a knowledge space. `references --check` passes without rows for them.

## 4. Notes
Every added or changed sentence is an indicative description of what a cited provision holds. None states an obligation or narrates drafting.

## Findings

### Defect
None.

### Should-fix
1. **Garbled clause in four rationales** (HW.CPU, HW.EMBED, HW.QPU: "names exactly the Articles that the field instantiates of those provisions lists"; HW.GPU: "the Article that the field instantiates of HW.GPU.4 lists"). Fix: "the Articles that the `instantiates` fields of those provisions list" and, for HW.GPU, "the Article that the `instantiates` field of HW.GPU.4 lists". Edit the four `apply_hw_*` scripts.
2. **STND.DFLT rationale** glosses INSTR.4 and INSTR.5 as "the dry runs and the halt on a failed step", while the Notes say "shell guards and dry runs". Fix: "the dry run (STND.INSTR.4) and the halt on a failed step (STND.INSTR.5), which are the guards and dry runs that the Notes assign to STND.INSTR".

### Optional
1. STND.CLASS: "no part of Simplicity (SIMPL) is among them" is a new, true statement, but "them" is loose after the semicolon and a later SIMPL row would falsify it. Alternative: "The table holds no part of Simplicity (SIMPL)."
2. HW.1: "each defined here, which the sub-profiles each give one of" is stiff. Alternative: "each defined here and given by one sub-profile". HDES uses the same form, so keep it if parity matters.
3. STND.KNOW: "its tag vocabulary (TAG)" may attach to the space. Alternative: "and the tag vocabulary of that corpus (TAG)".

## Could not check
- Whether the custodian reads "below LVL0" as excluding level-null entries (the lead has scoped the check so).
- The Notes class-onset lists of HW.ASIC, HW.FPGA, HDES.ASIC, and HDES.FPGA, which P5 does not touch.
