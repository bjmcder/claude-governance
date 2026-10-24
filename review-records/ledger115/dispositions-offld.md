# Dispositions: STND.OFFLD 0.1 to 0.2

Reviews of draft 0.1: review-cold-offld.md (cold review) and review-pairs-offld.md (STND.HARN.28 pair review). The reading copies are labeled revision 1.0 because they are composed as the standard would be adopted; the drafts are 0.1 and 0.2. Numbering is unchanged from 0.1.

## Cold review

| Finding | Disposition |
| --- | --- |
| D1: STND.OFFLD.21 has two conditions in one sentence | Accepted as suggested: "Before a run submits the work that a budget of accelerator memory covers, the run SHOULD check ...". |
| D2: STND.OFFLD.5, condition after its clause | Accepted as suggested: "Before host code observes the completion of an asynchronous transfer, host code SHOULD NOT write the host storage that the transfer reads." |
| D3: class paragraph leaves STND.OFFLD.17 S2 unplaced; "first sentence" wrong for 14 and 20 | Accepted. The paragraph is rewritten: STND.OFFLD.14 and STND.OFFLD.20 are named whole; STND.OFFLD.17, restructured (S5 below), has its first sentence at CSQ3 (DSGN.15) and its second at CSQ2 (DSGN.5). |
| D4: the mapping of STND.OMP is wrong in places | Accepted. STND.OMP.31 maps to STND.OFFLD.2 and STND.OFFLD.3; the second sentence of STND.OMP.23 to STND.OFFLD.1 and STND.OFFLD.3; STND.OMP.32 to STND.OFFLD.30, which now includes the check of data missing from or stale on an accelerator; the second sentence of STND.OMP.27 and the first of STND.OMP.28 are named as having no form here, with the reason; the onset sentence is limited to provisions that have an OpenMP form. |
| D5: Notes claims unsupported or overstated | Accepted. Each claim is limited to its evidence: the absence of means to report from device code is o4's inference; migration as a first-submission cost is removed from STND.OFFLD.31 and marked unverified in the Notes; the bug study is "27 of the 217 defects in the execution of device code in five projects"; the deadlock is "at 256 groups on every accelerator tested, and at 128 on some"; pinned host memory is removed from the list of timeless facts and given as one runtime library's; the rounding mode is given as one runtime library's, with another model's per-device report; the loss of the device is attributed to a secondary source; the sources of the progress studies are named as o1's S15 and S16. |
| S1: Terms, Parent and Boundary contract unused; reach of STND.CONC.1 and STND.CONC.2 | Accepted. Boundary contract is dropped from the imported terms. The Terms make the host code that makes a submission the parent of the concurrent tasks that execute it, and the Notes say that the reach of STND.CONC.2 into device code is intended, with STND.OFFLD.8 as its means. |
| S2: STND.OFFLD.17 S1 unconditioned; S2 restates the limits row of STND.ANNEX.6 | Accepted. The width sentence is conditioned on device code depending on the number of threads that execute together. The launch-limit sentence is dropped and the Notes cite the limits row of STND.ANNEX.6. |
| S3: STND.OFFLD.22 "capacity" | Accepted: "beyond the memory that the accelerator holds". |
| S4: STND.OFFLD.23 omits the error state | Accepted: "and which of them owns the error state of each context". |
| S5: STND.OFFLD.30 restates STND.CONC.25 and ties itself to a checker's current limit | Accepted as suggested: invalid accesses to memory, data missing from or stale on an accelerator, or barriers that at least one thread of a group does not reach; HW.14 is added for the data check. |
| S6: bundles | Accepted. STND.OFFLD.16 is split: its two sentences on lockstep and convergence stay; the sentence on naming the participants opens STND.OFFLD.17, "Group participants and width". STND.OFFLD.7 keeps its three sentences, and the Notes say they are the consequences of one event and apply together. |
| S7: STND.OFFLD.5 against STND.CONC.3; "after its last use" in STND.OFFLD.10 | Accepted. The Notes call STND.OFFLD.5 the instance of STND.CONC.3 for a transfer. STND.OFFLD.10: "after the completion of the last offloaded work that uses it". |
| S8: "offload form of" labels; onset sentence | Accepted: "by analogy with HW.CPU.5"; the label to STND.CONC.18 is replaced by a sentence naming STND.OFFLD.21 as the nearest counterpart of its sizing; the onset sentence is limited as in D4. |
| Optional: atomics in an unspecified order | Accepted: the Notes say that floating-point accumulation by atomics in an unspecified order is a declared variation under HW.12 and STND.ANNEX.6, and not a race. |
| Optional: programming models without groups | Accepted: the Notes say that STND.OFFLD.15 to STND.OFFLD.18 then have no subject. |
| Optional: omitted research items (peer access, tests per architecture, start-up stack check, checked release status, litmus tests) | Not added. Tests on each hardware model are HW.7 and HW.16; a check of the deployed stack at start is HW.7; a checked release status is STND.CODE.7; peer access and litmus tests are means that a project chooses under STND.OFFLD.13 and STND.CONC.26. |
| Overlaps table | STND.OFFLD.4 S1 overlaps HW.4 in part and is kept for the order of submissions, which HW.4 states only as the memory and ordering model of the path; STND.OFFLD.17 S2 and STND.OFFLD.30 resolved by S2 and S5; the rest the review marks as adding content. |

## Pair review

No listed pair of the 523 conflicts, and no matter is unowned. Observations:

| Observation | Disposition |
| --- | --- |
| 1: "a data race although it is atomic" against the imported term | Accepted: the Notes say that such an atomic does not order accesses with the other task, and that one runtime library documents the pair as racing although both are atomic. |
| 2: onset of STND.OFFLD.17 S2 | Resolved by cold D3. |
| 3: "after its last use"; a release is not a submission | Accepted: STND.OFFLD.10 as in cold S7; the Notes say that a release is not a submission, so STND.OFFLD.10 still has memory released on the path of an error that STND.OFFLD.7 governs. |
| 4: STND.OFFLD.7 and the resubmission of STND.ANNEX.6 | Accepted: the Notes say that a resubmission after such an error goes through a new context or a new process, from inputs held on the host. |
| 5: STND.OFFLD.22, capacity, record, onset | (a) Resolved by cold S3. (b) Not changed: migration changes speed and not results, so HW.9 does not apply, and HW.GPU.4 records its volume; the Notes say so. (c) Kept at CSQ1 on the row of STND.CLASS.10 for INTPR.7, as STND.CONC.10 is; the Notes say that HW applies HW.CPU.5 from CSQ3 by its own choice. |
| 6: HW.3, HW.CPU.4, HW.CPU.5, HW.GPU.4 in no row | No action, as for STND.OMP: HW alone addresses them. |
| 7: STND.OFFLD.23 and STND.CONC.18; mapping of STND.OMP.24 | Accepted: the label is replaced (cold S8), and the mapping is sentence by sentence: the first sentence of STND.OMP.24 to the second of STND.OFFLD.23, its second to STND.OFFLD.10. |
| 8: STND.OFFLD.31, migration; HW.22 | (a) Resolved by cold D5. (b) Accepted: the Notes say that a measurement that leaves out data movement or dispatch does not by itself support a claim that HW.22 governs. |
| 9: STND.OFFLD.28, a failed allocation has no response in the default contract | Accepted: "the response that HW.8 requires or that the hardware contract of its execution path states". |
| 10: STND.OFFLD.17 S1 against a width fixed in the build | Accepted: "or confirm at run time the number that its build fixes for the hardware model". |
| 11: STND.OMP.32 and STND.OMP.23 S2 mappings | Resolved by cold D4 and S5. |
| 12: STND.OFFLD.2 stricter than STND.OMP.23 for several accelerators | No change; noted. |
| 13: STND.CONC.2 S2, STND.CONC.10, STND.CONC.13, STND.CONC.24 for device code | Accepted: the Notes say that these provisions of STND.CONC still apply to device code, and that a programming model with no facility for one of them leaves the project a recorded decision under REPRO.7. |
| 14: STND.OMP does not cite STND.OFFLD | Open item: STND.OMP cites STND.OFFLD at its next revision (HANDOFF). |
| 15: revision label | The reading copies are composed as revision 1.0, the revision of adoption. |
| 16: STND.OFFLD.9 and HW.13 | Accepted: the Notes say that one statement serves both where the boundary contract holds or cites it. |

## Pairs of 0.2

The command pairs gives 526 pairs for 0.2 (pairs-OFFLD-0.2.md): the 523 of 0.1 and 3 new ones (pairs-OFFLD-0.2-delta.md), all from STND.OFFLD.17, which now instantiates DSGN.15 (AGENT.39, HDES.11, HW.11). They go to the cold verification of 0.2 with the provisions whose text changed.

# Dispositions: STND.OFFLD 0.2 to 0.3

Cold verification of draft 0.2, with the three new pairs: verify-offld-0.2.md. The new pairs (104, 109, 121) show no conflict and no unowned matter. Numbering is unchanged; the pairs of 0.3 are those of 0.2.

| Finding | Disposition |
| --- | --- |
| B1: "Work within one queue is ordered" | Accepted: "Work within an in-order queue is ordered, and some programming models make a queue out of order by default, ordering its work only by its dependences". |
| B2: Notes claims beyond the research | Accepted: migration beyond accelerator memory "continues with no error and is able to thrash" (o1, H4); the cache per account is one vendor's runtime; the non-finite check is "in that study ... about one outcome in a hundred". |
| B3: two conditions in STND.OFFLD.7 S1 and STND.OFFLD.10 | Accepted: STND.OFFLD.7 "SHOULD make no later submission through that context" and "a later result of a submission through that context"; STND.OFFLD.10 opens with its condition: "Once the last offloaded work that uses an allocation ... has completed, that allocation or registration SHOULD be released exactly once on every path, failures included." |
| B4: resubmission stated in the indicative | Accepted: recast as the effect of STND.OFFLD.7 on the resubmission that STND.ANNEX.6 admits, with the unverified point named. |
| S: the source of the STND.OFFLD.5 hazard | Accepted: marked an inference from o1's rule for a transfer in the other direction. |
| S: "the instance of STND.CONC.3" against the Terms | Accepted: "the form for a transfer of the protection that STND.CONC.3 asks, since the host storage that a transfer reads is shared with an asynchronous operation". |
| S: processes sharing contexts | Accepted: "where they share a context they share its error state". |
| S: onset paragraph refers to an onset not yet named | Accepted: "... rest on DSGN.5 and apply from CSQ2, the three sentences of STND.OFFLD.7 together". |
| S: STND.OFFLD.17 S2, confirm against what | Accepted: "confirm at run time that the number that its build fixes is that of the hardware model that executes it". |
| S: participants named, generalized from one vendor | Accepted: "the operations among threads that one programming model gives take a mask of their participants". |
| RATIONALE: "after their last use" | Accepted: "released once after the last work that uses them completes". |
| Optional: "the offload form of STND.CONC.11" | Kept: device threads are concurrent tasks under the Terms, so STND.CONC.11 reaches them and STND.OFFLD.18 is its form for a submission. |
