# Dispositions: STND.RUST draft 0.1 to draft 0.2

This revision answers `review-cold.md` (cold review) and `review-pairs.md` (pair review, with its Section C), under the lead's decisions 1 to 7 of 2026-10-24.
- Draft 0.2: `draft-0.2.md`.
- Pair list: `pairs-0.2.md`, with 267 pairs.
- Rehearsal: STND.BUILD round, then the Rust round (four transactions), through `REPO/.scratch/rust/rehearse_with_build.py`, because 0.2 cites STND.BUILD. `verify` passes all eight checks. The only findings are 10 g.18 review notices, on .1, .3, .7, .11, .13, .16, .21, .23, .24 and .29. The class-onset paragraph names each of them and says a replacement replaces the provision whole.
- The rehearsed copy is at `REPO/.scratch/rust/rehearsal-0.2/`.

## Renumbering (0.1 to 0.2)

The draft goes from 36 to 33 provisions. Draft 0.1 numbers map to draft 0.2 numbers as follows.

| Draft 0.1 | Draft 0.2 |
| --- | --- |
| 1, 2 | 1, 2 |
| 3 and 4 | 3, merged |
| 5 to 13 | one number lower, 4 to 12 |
| 14, 15, 16 | 13, 14, 15 |
| 17 and 18 | 16, merged |
| 19, 20, 21 | 17, 18, 19 |
| 22 sentences 1 and 2 | 20; sentence 3 deleted |
| 23 to 28 | 21 to 26 |
| 29 | deleted; STND.BUILD.1, .6 and .7 hold it |
| 30 | 27 |
| 31, 32, 33 | 28, 29, 30 |
| 34, 35, 36 | 31, 32, 33 |

Binding provisions are now 6, 13, 14, 15 and 33.

## Cold review

| Finding | Disposition |
| --- | --- |
| D1, direction attributed | Accepted (lead 1). The Notes open with the standing directions as the round brief writes them. Nothing is attributed to the custodian except the PY/JL ruling, which lead 3 asks for. |
| D2, .14 S2 raises the floor | Accepted (lead 2). Now 13 S2. It is narrowed to "each panic that answers a condition that PRIME.4 lists". It asks for "a diagnosis", with no location. It covers "the hook, or ... the handler", so programs without the standard library are reached. |
| D3, .36 too wide | Accepted. Now 33. It is limited to claims in a report, a result or release record, or a review, as STND.CXX.29 is. The Notes say a soundness argument is not such a claim. |
| SF4, .15 compiler only | Accepted. 14 reads "the compiler or a static check", as STND.CXX.17 does. |
| SF5, .16 narrower than CXX.18 | Accepted. 15 S1 forbids each form an execution setting removes, conditionally compiled code included. S2 covers overflow detection for CPS checks as well as untrusted input. |
| SF6, reach of Untrusted input | Accepted (lead 3). The reach is the public interface (new Term), as in PY and JL. The Notes state the PY/JL ruling and that it was made for those two standards. |
| SF7, .25 onset | Accepted. 23 cites DSGN.4 alone, so its onset is CSQ2. |
| SF8, "tighten above the floor" | Accepted. The STND.JL wording is used ("applies only to work that HW binds"). |
| SF9, .22 S3 restates CONC.3/.9 | Accepted. Deleted; the Notes give the hazard as the reason 20 names the protection. |
| SF10, unverified and narrated Notes | Accepted: async drop, the incident, the extract method and the unverified marks are all removed. No unverified fact remains. |
| SF11, .33 names a linter | Accepted. 30 reads "a check that reports"; its S2 is stated as an outcome. |
| SF12, proportion | Accepted. 33 provisions, inside the lead's 31 to 34. The Notes fall from 4,955 to 4,101 words. Merges: .3+.4, .17+.18, and .29 into STND.BUILD. |
| Bundles | .22 resolved by the deletion. .25 now has one onset. .27 is split into two sentences, with the catch folded into S1. .31 (now 28) is down to two sentences. .29 is gone. .12 (now 11) holds on the STND.CXX.21 precedent. Every remaining bundle is named in the Notes. |
| Terms | Lead 5 applied: Soundness condition and Soundness argument replace the Safety terms; the Notes say they are no part of a hazard analysis. Foreign interface is renamed Foreign function interface, and the Notes relate it to the CXX term. Unsafe attribute is no longer circular. Feature becomes Crate feature. The Lock file Term claims a digest only "where the source of a package gives one". |
| Optional .12 S1 | Taken: "without a panic that its own code raises". |
| BUILD overlap | Lead 6 applied. .29 is deleted. 2 is stated "Among the execution settings that STND.BUILD.11 asks". 28 cites STND.BUILD.26. 30's warnings sentence is dropped in favor of STND.BUILD.12. 19 cites STND.BUILD.13 in the Notes. 29 cites STND.BUILD.25 in the Notes. |

## Pair review

| Finding | Disposition |
| --- | --- |
| D1, narration and pending decision in the Notes | Accepted (lead 1). The decision sentences are removed and listed in the report instead. |
| SF1, panic handler without the standard library | Accepted in 13 S2. The Notes cite PRIME.13 and HW.EMBED.4 for a controller's handler. |
| SF2, .16 narrower than CODE.6 | Accepted; same answer as cold SF5. |
| SF3, versions tested | Accepted (lead 4). 1 tests at the oldest release and at the production release, and runs a non-blocking check at the newest toolchain and newest dependencies, as STND.PY.14 and STND.JL.3 do. |
| SF4, lock file | Accepted (lead 4). 29 adds the STND.JL.4 exception for libraries, and the check of 1 against newer revisions is exempt from S3. |
| SF5, logging | Accepted (lead 4). 13 S3 follows STND.PY.22 S3. The Notes state how STND.JL.15 differs. |
| SF6, digest overstated | Accepted; see Terms above. The Notes cite STND.DEPS.6 sentence 3. |
| SF7, vendor report | Accepted; deleted. |
| SF8, primitive types in .25 | Accepted. 23 now reaches only structures, unions and enumerations that the work does not treat as opaque. |
| Optional 1, 2, 3, 4, 5, 6, 7, 9, 11 | Taken. Note on 11: the STND.DRAFT mention is gone from the Notes. Note on 4: 10 reads "Other than in a test". |
| Optional 8 | Taken: the Notes say STND.DEPS.8 still records the revision that built each result. |
| Optional 10 | Answered by the bundle changes above. |
| Optional 12 | Left to the lead at the coalesce. |
| Section C, checks in the shipped build | Lead 4: 19 follows STND.JL.34, not STND.CXX.27. Safe Rust checks every index in every build, so CXX.27's gap (unchecked library preconditions in the shipped build) has no Rust counterpart. The checks a Rust setting removes are governed by 15 and 17 where untrusted input is concerned. |
| Observations 3, 4, 7 | Each now has a sentence in the Notes: no safe state set by a destructor; overflow in a trusted command; crate features that select alternative paths or exclude one another. |
| Observation 8 | Not taken. Hash order, random streams, tolerances, high-assurance code and register types are left to the reconciliation; the lead did not decide them. |

# Dispositions: draft 0.2 to draft 0.3 (`verify-0.2.md`)

Draft 0.3 is `draft-0.3.md`; its pair list is `pairs-0.3.md`, with 267 pairs.
- Rehearsal: BUILD round, then Rust round, through `REPO/.scratch/rust/rehearse_with_build.py`. `verify` passes all eight checks.
- Findings: 8 g.18 notices, on .1, .7, .11, .13, .22, .24, .25 and .30. The onset paragraph names the subject of each.
- Rehearsed copy: `REPO/.scratch/rust/rehearsal-0.3/`. The 0.2 module is archived at `REPO/.scratch/rust/content_rust_v02.py`.

## Renumbering (0.2 to 0.3)

Draft 0.2's provision 16 is split in two: its first two sentences stay as 16 and its third becomes 17, "Reasoned unwrap in library code". Draft 0.2 provisions 17 to 33 move up by one, to 18 to 34. The draft now has 34 provisions; the binding ones are 6, 13, 14, 15 and 34.

| Finding | Disposition |
| --- | --- |
| 1, Defect: .13 S2 | Accepted. It now reads "of each panic that answers a condition that PRIME.4 lists and that no other response of this provision answers". The Notes say a panic answered by a returned error or a visible degradation carries its diagnosis through that response. |
| 2, .33 floor parity | Accepted. The CXX.29 parity clause and the PY.4 parity for .6 are removed from the Floor and Agents paragraphs. The reach of 34 and the cost of 6 go to the custodian in the report. |
| 3, Observation 4 | Accepted. The Arithmetic paragraph now says that overflow in trusted arithmetic that computes a command is a defect under PRIME.4 and DSGN.2, and that CPS.5 does not detect a wrapped value inside its limit. |
| 4, .15 S1 | Accepted, worded as proposed. |
| 5, duties in the Notes | Accepted. The sentence on a check by the reviewer and the human owner is deleted. The seed sentence now reads "STND.CODE.9 covers the seed". |
| 6, attributed ruling | Accepted as the lead allows. The Notes say only what the Notes of STND.JL and STND.PY record of the ruling of 2026-10-23. The Rust question goes to the custodian in the report. |
| 7, "by inference" | Accepted. The unsupported clause is deleted along with its mark. |
| 8, bundles | Accepted. .16 is split (new 16 and 17). .3 S2 is folded into S1, leaving two modals. .13 is kept as one rule, because its three sentences define what counts as a response, as PY.22's do. The bundle sentence now names the actual subject of each provision. |
| 9, onset | Accepted. The DSGN.3 sentence now includes both sentences of the guards provision (now 23). The tests of 1, 8 and 29 "rest on no row and apply from CSQ3". |
| Optional | The Xu study is now "186 reports". The Notes are cut from 4,101 to 3,480 words, mainly in Numerics, Concurrency and the BUILD list. .2 is kept as the Rust list inside STND.BUILD.11. |
| Lead: rationales | `apply_rust.py` and `apply_mnem_rust.py` now carry full rationales in the form of `apply_offld.py` and `apply_conc.py`. TAIL, AT and ROW_AFTER are unchanged. |
