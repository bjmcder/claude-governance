# STND.HARN.28 pair review: HW 1.1.1 (2026-10-24)

## Basis
The diff changes only `HW/_doc.md`: revision 1.1 to 1.1.1; an informative Note sentence group after the first HW.8 sentence; a References row `STND.MPI`; a revision-history row. The script makes the same edits and records a GOV.41 entry. No numbered `N.md` file changes and no provision body changes (HW.8 and all others are untouched); Terms, Selector and HW.2 are untouched.

So in none of the 1469 pairs does provision text change on either side, and each pair's prior status stands on the review that last covered it:
- Other side adopted or amended after HW 1.1 (ledger 89, 2026-10-19, the last provision change, HW.20): STND.CODE, THRT, KNOW, DEPS, PROJ, WPROC, CREW, DOCS, CXX, PY, JL, ANNEX, MPI, and the DFLT, INSTR and VVUQ amendments (ledger 90-109). Their adoption reviews saw HW at 1.1 text.
- Other side older (AGENT, HDES*, HW.*, CPS, MEAS, ML, NUMER, VVUQ, CLASS, HARN): covered by the HW 1.1 amendment (ledger 89, "command pairs for HW") and the adoption reviews of ledger 64-88.
The basis holds for all pairs except where the new Note discusses a provision; those are below. Limit: ledger 89 and 92 record only "command pairs", and I found no per-pair record for them; I rely on the ledger's statement and did not re-read the 1469 pairs.

## Pairs examined individually
| # | Provisions | Conflict | Unowned | Reason |
|---|---|---|---|---|
| 1396 | HW.8 / STND.MPI.5 | no | no | MPI.5 instantiates PRIME.4 and HW.8: an MPI error is answered by an error handler ending each process with a diagnosis, or by code responding as HW.8 requires. Agrees with the Note. Matter is HW.8's (HW.2, hardware contract of an execution path). |
| 1397 | HW.8 / STND.MPI.6 | no | no | Both say the other processes halt, or receive notice and respond as PRIME.4 requires. The fixes from the MPI pair review (dispositions C1, C2: safe state kept open; diagnosis written first) are in the adopted text. The Note cites MPI.6 for the route, which it states. |
| 1374 | HW.8 / CPS.4 | no | no | CPS.4 verifies the safe state on loss of logic, communication or power. A whole-run response is a safe state of the run, which CPS.4 verifies; HW.8's three responses stay. Owners: CPS (safe state), HW (HW.8). |
| 1381 | HW.8 / HW.EMBED.4 | no | no | EMBED.4 already states output states "after a halt under HW.8"; a halt caused by a peer is the same halt. |
| 1384 | HW.8 / HW.GPU.3 | no | no | GPU.3 handles offload errors "as HW.8 requires ... through another execution path". Compatible. |
| 1376-1380, 1382, 1383 | HW.8 / HDES.5, HDES.7, HW.ASIC.4, HW.CPU.3, HW.EMBED.3, HW.EMBED.6, HW.FPGA.4 | no | no | Contract-content provisions of the same matter; none speaks of halts across processes. |
| rest of 1375-1401 | HW.8 / HDES.14, NUMER.5, CODE, CXX, JL, PY, HARN | no | no | Each instantiates PRIME.4 for its domain; none states the extent of the halting path. Read at provision level only. |

No pair lists HW.8 with a HW.QPU provision; HW.QPU's halt/safe-state content is not engaged.

## Tension noted (not a conflict)
The Note says the execution path "is the whole run". HW's Term defines a path as one component on one hardware type, and HW's Notes say mixed-hardware code binds each part by its sub-profile, joined by HW.13 and HW.14. A run on CPU and GPU ranks is several paths in the Term, so the sentence reads as a rule for the extent of the response, not a redefinition. Optional rewording: "the response that HW.8 asks for applies to the whole run." No obligation changes.

## Unowned matter
None. The Note adds no matter: the response to a halt is HW.8's, which HW.2 gives to HW. STND.MPI is not a profile and has no shared-matters table.

## Summary for the adopter
Conflicting pairs: none. Matters without an owning profile: none.

## Not verified
Per-pair records of earlier adoptions (ledger 64-109); the 1469 pairs were not each re-read; the amendment script was not run.
