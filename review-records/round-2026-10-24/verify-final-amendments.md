# Review of STND.CONC 1.1, STND.VVUQ 1.4, STND.CXX 1.1.1 (2026-10-24)

Subject: `.scratch/fixpass2/governance-final`, the three apply scripts, the reading copies. No Defect found.

## Verified by script
- `govharness verify`: eight checks PASS. `findings.py`: no defect-class finding; CONC.30, VVUQ.2, VVUQ.63 raise none (g.14 numbers and g.18 bundles are old text).
- Rationales of ledger entries 122 (VVUQ), 128 (CXX), 139 (CONC) end with the fixed tail. Entries 114 (OMP) and 116 (OFFLD) are as the CONC rationale says.
- Pair lists regenerated with `govharness pairs` equal the `-pairs-final.md` files for CONC.30 (8 pairs), VVUQ.2 (65), VVUQ.63 (59): none missing or extra.
- CONC.30: unique title, one modal, condition first, no banned word, instantiates DSGN.15 and REPRO.3 only (default holds), no product.

## 1. STND.CONC 1.1

**Should-fix**
1. *STND.FTN.26 is not exactly "the form of" CONC.30.* FTN.26 says code SHOULD NOT rely on the order of records that DO CONCURRENT iterations or images write to one file. CONC.30 asks that the order be stated, fixed by a protocol or declared as variation. For images a synchronization can fix the order; CONC.30 then allows reliance, FTN.26 still forbids it. FTN.26 and the FTN Notes do not cite CONC.30. Fix: write "STND.FTN.26 is the Fortran case of STND.CONC.30 in which no protocol fixes the order; it asks that code not rely on it."
2. *Partial restatement not argued (GOV.31).* REPRO.3 already requires declared variation, and HW.12 (binding) has each path declare the variation of its concurrent scheduling. Fix: one Notes sentence saying CONC.30 adds the scope (writes to one output) and the alternative of an order that a protocol fixes.

**Optional**: the Notes sentence cites no source, unlike the other paragraphs (cite the language standards or mark unverified). STND.MPI has no form for ranks writing to one output; say so.

**Checked.** Onset: DSGN.15 states a protocol from CSQ3 (its verification is the CSQ2 row); REPRO.3 has no row; CSQ3 is right, as for CONC.3. Class minor (new default above the floor; precedents STND.DFLT 1.1, STND.HARN 1.1). Floor not raised, since it asks what REPRO.3 asks. Not binding. Transition argued. DO CONCURRENT appears only in the Notes.

**Pairs (8).** AGENT.39 (agent work; DSGN.15 only), HDES.11 and HW.11 (verification of a protocol; CONC.30 asks none), HW.12 (binding, scheduling variation; compatible, see should-fix 2), NUMER.11 (run-to-run tolerance; compatible), HDES.3 and ML.3 (regenerable, differences declared; compatible), NUMER.24 (unrelated). Conflicts 0; unowned 0.

## 2. STND.VVUQ 1.4

**Should-fix**
1. *The rationale says more than the text.* It says the record of the work already names the battery. The old VVUQ.63 required no record; "named with its revision in the record of the work" is a new small duty (the transition sentence half admits it). Minor still holds. Fix: say the text adds the record of battery and revision, at the cost of one entry of the kind REPRO.2 asks for tools; drop the clause that the record already names it.
2. *Loosened without a word on strength.* "A published battery" is met by a weak one; the old text named the most demanding. A reviewer cannot decide the outcome as GOV.18 wants. Fix: add to the Notes that the battery is at least as demanding as the use of the generator warrants (NUMER.24), or state in the rationale that the loosening is deliberate.

**Optional**: "able to be repeated as it ran" reads better as "repeated as it ran".

**Checked.**
- *Class.* Minor with an editorial part is right: a default's text changes what it asks (GOV.41; REPRO.7), and the editorial part rides in the higher class.
- *Editorial part.* STND.DFLT defines Checkpoint as "a copy of an item's prior state that the provisioned environment keeps outside the scope of an action", another sense, so the replacement is justified. Condition, modal, and instantiated IDs of VVUQ.2 and its table row are unchanged. No "checkpoint" or "restart" remains in STND.VVUQ except the revision row.
- *Citations.* ML.2 owns the record (ML.3) and the error and domain (ML.4 to ML.7) of a learned model; MEAS.2 owns acquisition, calibration, and uncertainty. Accurate; References lists ML and MEAS.
- *Agnostic.* BigCrush and TestU01 appear in the Notes only, without a version. Onset unchanged (CSQ3).

**Pairs (124).** Read in full: HW.12, NUMER.11, NUMER.24, ML.3, HDES.3, HW.15 to HW.18, NUMER.3, .7, .17, .19, .22, .25, .26, .28, .29, AGENT.5, MEAS.7, HW.6, HDES.4. VVUQ.63 and NUMER.24 (DSGN.17, REPRO.3, VV.1): the interleaved-stream test supports the independence evidence of NUMER.24 and does not restate it. VVUQ.2 with HW.12, NUMER.11, HDES.3, ML.3 (REPRO.3): fixed summation and complete saved state are ways to the identity or declared difference they ask. The other pairs (AGENT.12, CPS.4/6/8, HDES.*, HDES.ASIC.*, HDES.FPGA.*, HW.10, HW.20, HW.ASIC.4, HW.EMBED.3/4, HW.FPGA.4, HW.QPU.5-7, ML.4, ML.5, NUMER.5/6/8/9/12-14/23) share VV.1 or VV.3 only. Conflicts 0; unowned 0.

## 3. STND.CXX 1.1.1

**Optional**
1. The CXX.27 sentence is a double negative. Fix: "STND.CXX.27 also reaches a build whose only report is the verdict of a test, which the term Reporting build leaves out."
2. It states a reading: whether a test verdict is "a result" in CXX.27 is interpreted, not written. STND.BUILD's Notes say only that CXX.27 "keeps the library's production checks in reporting builds"; reporting builds are a subset of CXX.27's builds, so the two do not conflict. It states how CXX.27 is read, not what it asks, so it stays editorial.
3. The imported Reporting build is used only in the Notes. An import adds a defined meaning where editorial rows promise "no defined meaning changes". It is harmless and disclosed. Naming "the term Reporting build of STND.BUILD" without the import would be cleaner.

**Checked.** Only `_doc.md` changes (Notes, Terms, References, revision row); CXX.4, .25, .27 are untouched, so no obligation changes. BUILD.11 (settings of each compilation unit and link step) and BUILD.12 (warnings fail the checks, each tool) match CXX.4 and CXX.25; the Notes of STND.BUILD name them as those forms (CXX.25 matches only the first sentence of BUILD.12, and the CXX text says the rule "reaches further", which is true). Relation against content_build.py: Reporting build is "a build from which the work reports a result other than the verdict of a test, or makes a release"; CXX.27 is "each build from which the work reports a result or makes a release". Every reporting build is a CXX.27 build; the reverse fails only for test verdicts. Accurate. Editorial is the right class.

## Not checked
- Research notes and primary sources behind the Notes (c1 to c4, f1).
- Pairs were judged by subject group; I wrote no per-row verdict for the 132 pairs.
