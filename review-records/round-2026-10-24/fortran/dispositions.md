# Dispositions: STND.FTN 0.1 to 0.2

Reviews of draft 0.1: review-cold.md (cold review) and review-pairs.md (STND.HARN.28 pair review). Lead decisions 1 to 7 of the revision request are applied as given. The reading copy draft-0.2.md is labeled revision 1.0 because it is composed as the standard would be adopted. The rehearsal applies the BUILD round (apply_build_round.py) first, because 0.2 cites STND.BUILD, and then apply_fortran_round.py. The rehearsal script is .scratch/fortran-draft/rehearse_build_then_fortran.py. `verify` passes all eight checks, `findings.py 'STND\.FTN'` is empty, and the new pair list pairs-0.2.md has 174 pairs.

## Numbering, 0.1 to 0.2

The draft goes from 40 provisions to 36.

| 0.1 | 0.2 | Change |
| --- | --- | --- |
| 1 | 1 | S2 limited to what a processor must report; Term made non-circular |
| 2 | 2 | S1 cut to the Fortran options; cites STND.BUILD.11; retitled "Fortran compiler options" |
| 3 | 3 | Exception for a COMMON statement under 0.2 FTN.12 |
| 4 | deleted | Held by STND.BUILD.2, .3, and .4 (Notes) |
| 5, 38 S1 | 4 | Condition of revision; the static check of 0.1 FTN.38 S1 folded into S2 |
| 6, 7 | 5 | Merged, each sentence with its revision condition; retitled "Implicit typing and argument intent" |
| 8 | 6 | Unchanged |
| 9 | 7 | Unchanged (holds only what f1 holds) |
| 10 | 8 | Unchanged |
| 11 | 9 | "processor" changed to "compiler" |
| 12 | 10 | Exception for default initialization of a component |
| 13 | 11 | Unchanged |
| 14 | 12 | Unchanged |
| 15 | 13 | Condition of revision |
| 16 | 14 | S1 limited to literals that meet an entity of another kind; S2 form valid at every revision |
| 17 | 15 | "untrusted input" (Term) |
| 18, 19 | 16 | Merged; "each main program"; response to a negative answer in the body |
| 20 | 17 | Condition of revision; "functions that classify a value" |
| 33 S2 | 18 | New default "Finite-value compiler options", naming CPS.5 and CPS.9 as STND.CXX.18 does |
| 21 | 19 | Unchanged |
| 22 | 20 | The threadprivate directive and clauses; retitled "Common blocks in OpenMP" |
| 23 | 21 | "fully supports"; "nonblocking operations" |
| 24 | 22 | Nonblocking operations only; condition of revision |
| 25 | 23 | Worded by the MPI condition f1 quotes (subscript triplets, nonblocking) |
| 26 | 24 | Unchanged |
| 27 | 25 | "one place in the work" (valid before modules) |
| 28 | 26 | Unchanged; Notes added |
| 29 | 27 | Condition of revision |
| 30 | 28 | Unchanged |
| 31 | 29 | Binding; form of STND.CXX.16, PY.22, JL.15 |
| 32 | 30 | Binding; reworded as the cold review proposes |
| 33 S1 | 31 | Binding; the check of STND.CODE.6, when it is made, the assumed-size case |
| 34 | 32 | Applies where Fortran code halts; condition of revision; cites STND.MPI.6 |
| 35 | 33 | Exceptions in the body as in STND.PY.6; only shrinks |
| 36, 37 | 34 | Merged; table gains two rows; retitled "Modernizing changes" |
| 38 S2 | deleted | Held by STND.BUILD.12 and STND.CODE.4 |
| 39 | 35 | Conditions on the means; one fixed value |
| 40 | 36 | Run on the host |

## Cold review

| Finding | Disposition |
| --- | --- |
| D1: FTN.35 S2 blocks its own adoption | Accepted (lead 2). 0.2 FTN.33 S2: "Other than an entry that the change that adopts this standard, a change of a compiler or of the revision in force, a revision of this standard, or a change that incorporates external code into the work makes necessary, a change SHOULD NOT add an entry". The closing paragraph of the Notes is deleted. The Notes say that otherwise the list only shrinks. |
| D2: FTN.33 S2 binding on an unverified hazard | Accepted (lead 3). The sentence is now the default 0.2 FTN.18, worded by the documentation of the compiler. Its reason is in the Notes, so no binding sentence rests on the hazard. The binding paragraph is now stated as an argument, and the decision goes to the custodian in the report. |
| D3: obligations in the indicative in the Notes | Accepted. The reading of flags without halting is recast as a hazard (a program that neither halts nor reads them continues without a trace; HW.5). The response to a negative answer is moved into the body of 0.2 FTN.16. The VVUQ.83 sentence and "a project at an earlier revision avoids" are deleted. |
| S4: FTN.32 hard to parse | Accepted as proposed (0.2 FTN.30). |
| S5: FTN.33 S1 against CODE.6 | Accepted (lead 3). 0.2 FTN.31 names "the check that rejects an invalid value", that is, the check of STND.CODE.6, and states when it is made: "at the entry of the untrusted input or, at the latest, before the first use of that value". The Notes give the reason: Fortran has no subscript check that no execution setting removes. They no longer say that the reach is not widened. The reach is now the Term Untrusted input (pair 8). |
| S6: FTN.4 belongs in BUILD | Accepted (lead 1). FTN.4 is deleted. The Notes now describe the compiled interface of a module as a generated file of STND.BUILD, with BUILD.2, .3, and .4 named. BUILD is not asked to change, because its Term Generated file already covers "the interface of a unit that source names". |
| S7: FTN.38 S2 is BUILD.12; S1 repeats FTN.5 and FTN.6 | Accepted. S2 is deleted, and S1 is folded into 0.2 FTN.4 S2. A report of implicit typing needs no check, because IMPLICIT NONE makes it a compile error. |
| S8: FTN.2 S1 restates BUILD.11 and HW.5 | Accepted (lead 1). The sentence is cut to the options that change a default kind or that give locals static storage or an initial value, as the Fortran form of STND.BUILD.11. HW.5 is dropped from its instantiation. |
| S9: FTN.16 S1 disproportionate | Accepted (lead 6). The sentence is limited to literals assigned to, combined with, or passed to an entity of a kind other than default real, "written in the kind of that entity" (a kind parameter, or a D exponent before kinds). |
| S10: FTN.35 arbitrary subset; Term wider; heavy inventory | Accepted. The Term is aligned with the provision. The provision allows one reason for each class of forms. The Notes say that the listed provisions are those decided from the text of one file. The list is 4, 5, 6, 10, 12, 13, 14, and 25 in 0.2 numbers; 0.1 FTN.7 is now part of 0.2 FTN.5. |
| S11: FTN.22 clauses against threadprivate; f1 contradicts itself | Accepted (lead 7). 0.2 FTN.20 names "each threadprivate directive, and each data-sharing clause other than shared". The Notes describe threadprivate as a directive and follow the table row of f1, not its answer in brief; f1 itself is left to its author. The clause rule is quoted from S3 and is not marked unverified. |
| S12: MPI scope beyond f1 | Accepted. 0.2 FTN.22 covers nonblocking operations only. 0.2 FTN.23 is worded by the quoted condition (subscript triplets, nonblocking operations); the Notes mark f1's extension to one-sided and split collective operations as unverified. 0.2 FTN.21 now says "fully supports", as f1 does. |
| S13: no Notes for FTN.27 and FTN.28 | Accepted. A paragraph "Input and output" is added, covering NEWUNIT=, the named units, the preconnected unit on image 1, the processor-dependent order of records, and the absence of a STND.CONC rule. |
| S14: FTN.1 S2 overreaches; Term circular | Accepted. S2 now reads "each form that the numbered syntax rules and constraints of the revision in force do not permit, and each obsolescent form". The Term now reads "the revision of the Fortran standard to which the file is written". |
| O15: fold FTN.36 into FTN.37 | Accepted (0.2 FTN.34, two sentences). |
| O16: "list grows"; Term Processor; FTN.18 values | First two accepted: "has grown at most revisions, and the 2023 revision added none". The Term Processor is removed, and the provisions say "compiler". The values of the modes stay the program's choice, recorded under HW.5. |
| O17: proportion | 36 provisions (lead: about 35). The Notes drop the study extracts S6 to S8 and other sentences. They stay at about 4,400 words, as in 0.1, because the answers to the reviews add text. |

## Pair review

| Finding | Disposition |
| --- | --- |
| 1: indicative obligations in the Notes | Accepted. See cold D3. (a) The closing paragraph is deleted, and the transition rule is in the body of 0.2 FTN.33. (b) The VVUQ.83 sentence is deleted (lead 7). (c) The response is moved into the body of 0.2 FTN.16. |
| 2: "concerns C++ alone" is wrong | Accepted (lead 5). The Notes now say that the directions for C++ and Julia ask for the newest edition or version, which STND.CXX.2 and STND.JL.1 follow, and that the files record none for Fortran. Applying either direction to Fortran is a decision for the custodian, in the report. |
| 3: FTN.9 states half the rule | Not adopted as a provision (lead 6: only what f1 holds). The Notes mark the further restriction on references as not in f1 and unverified. |
| 4: FTN.34 against FTN.31, CPS.4, MPI.6; revision; pure | Accepted (lead 4). 0.2 FTN.32 reads "each halt of Fortran code on a failure ... SHOULD be made by an ERROR STOP statement", under "Where the revision in force provides the ERROR STOP statement". The Notes say that ERROR STOP alone meets STND.MPI.6 only where the contract of STND.MPI.7 says so. They mark the pure-procedure case unverified and point to the return response of 0.2 FTN.29. |
| 5: provisions presuppose a revision | Accepted (lead 6). Conditions are added to 0.2 FTN.4 S1, FTN.5 S1 and S2, FTN.13, FTN.17 S1, FTN.22 S1, FTN.27 S1, and FTN.32. 0.2 FTN.14, FTN.16 S1, and FTN.25 are reworded so that they hold at every revision. The Purpose states the rule, and the Notes say that raising a file's revision is the project's choice. |
| 6: FTN.3 against FTN.14 | Accepted (lead 6). 0.2 FTN.3 S2 excepts "a COMMON statement that gathers the declarations of an existing common block into the one source text of STND.FTN.12". The Notes name module variables as the way out. |
| 7: FTN.33 S2 narrower than CXX.18 | Accepted. 0.2 FTN.18 names STND.CODE.6, CPS.5, and CPS.9 (refers_to). |
| 8: Untrusted input undefined | Accepted (lead 5). A Term Untrusted input is added with the reach of STND.PY and STND.JL: public procedures of modules and procedures with BIND, leaving out external procedures. The Notes say that the ruling of 2026-10-23 was made for STND.PY and STND.JL; its application to Fortran is a decision for the custodian, in the report. |
| 9: FTN.18 and FTN.40 scope | Accepted (lead 6). 0.2 FTN.16 says "each main program". The Notes cover the library case (STND.CONC.17, HW.CPU.3), the thread case (HW.CPU.3, STND.OMP.30), and the device case (STND.OFFLD.14). 0.2 FTN.36 asks for "a run on the host". |
| 10: FTN.33 and assumed-size dummies | Accepted (lead 3). The body adds "or the extent that the caller passes for an assumed-size dummy array", and the Notes give the wrapping remedy. |
| 11: default initialization and SAVE | Accepted. The exception is in 0.2 FTN.10 S1, and the Notes mark the rule unverified. |
| 12: conditions on the means; fixed value | Accepted for 0.2 FTN.35 (both sentences conditioned; "one fixed value", STND.CODE.9). 0.1 FTN.38 S1 is gone. |
| 13: Terms Processor and Legacy list | Accepted. See cold O16 and S10. |
| 14: wording of the Notes | Accepted. (a) The STND.MPI.16 sentence is corrected. (b) Threadprivate is described as a directive. (c) The narration of what the note read is removed, and only marks remain. (d) The look-ahead sentence goes with FTN.4. |
| 15: rows for the table; options and NUMER.5 | Accepted. Two rows are added: a change of the default-kind option, and a loop moved to threads or images (HW.CPU.3). The Notes on the legacy list say that NUMER.5 reads the precision from the options of 0.2 FTN.2. |
| 16 to 21: observations | 20: the Notes say that an entry for incorporated code is able to cite the record of STND.DEPS.11. 21: the onset paragraph is rewritten item by item (lead 7, R8); 0.2 FTN.33 S2 and FTN.1 S1 are placed correctly. 16, 17, 18, and 19 are left to the reconciliation (R14, R15, R16, R22). |
