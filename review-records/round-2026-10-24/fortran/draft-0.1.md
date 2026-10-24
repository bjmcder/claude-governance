# Fortran standard (STND.FTN) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/FTN/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that is specific to Fortran, in source written to every revision of the Fortran standard, classic and modern. It adds to STND.CODE, STND.DOCS, STND.CONC, STND.MPI, STND.OMP, NUMER, and HW only what the language makes necessary. It covers the revision in force, the options of processors, deleted and obsolescent forms, and the compilation of modules (STND.FTN.1 to STND.FTN.4); interfaces and declarations, with the association of arguments (STND.FTN.5 to STND.FTN.10); defined values, implied and explicit SAVE, and storage association (STND.FTN.11 to STND.FTN.14); kinds, literal constants, and floating-point exceptions (STND.FTN.15 to STND.FTN.20); parallel execution in DO CONCURRENT and OpenMP (STND.FTN.21 and STND.FTN.22); the Fortran forms of the hazards of MPI (STND.FTN.23 to STND.FTN.26); input and output (STND.FTN.27 and STND.FTN.28); interoperability with C (STND.FTN.29 and STND.FTN.30); failures (STND.FTN.31 to STND.FTN.34); legacy source and its modernization without a change of results (STND.FTN.35, STND.FTN.36, and STND.FTN.37); and the checks of Fortran code (STND.FTN.38, STND.FTN.39, and STND.FTN.40).

STND.FTN.31, STND.FTN.32, and STND.FTN.33 instantiate PRIME.4, so they are binding and apply at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is agnostic of processor, vendor, platform, tool, and revision of the Fortran standard: it names the statements, attributes, specifiers, and intrinsic modules of the language, and no compiler, option, or revision, and the repository configuration chooses the revision and the processors (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them. Concurrent task and Protection have the meanings that STND.CONC gives them; each image, each thread that runs an OpenMP parallel region, and each iteration of a DO CONCURRENT construct that a processor executes in parallel with another is a concurrent task. MPI standard and MPI implementation have the meanings that STND.MPI gives them, and nonblocking operation, persistent operation, one-sided operation, split collective operation, and MPI datatype the meanings that the MPI standard gives them. Data-sharing clause has the meaning that the OpenMP specification of STND.OMP gives it. Program unit, scoping unit, main program, module, submodule, procedure, interface body, explicit interface, dummy argument, dummy data object, actual argument, common block, storage association, assumed-shape array, assumed-size array, explicit-shape array, array section, contiguous, kind type parameter, literal constant, intrinsic module, image, locality specifier, C descriptor, unit, and preconnected have the meanings that the Fortran standard gives them.

| Term | Definition |
| --- | --- |
| Fortran standard | The international standard of the Fortran programming language, ISO/IEC 1539-1, at the revision that the text names, or otherwise at the revision in force. |
| Revision in force | Of a source file of Fortran: the revision of the Fortran standard to which the repository configuration states that the file is written and checked. |
| Processor | A compiler of Fortran, with the run-time library that executes the code it compiles, that the repository configuration names as building Fortran source of the work. |
| Deleted form | A feature of Fortran that a published revision of the Fortran standard lists as deleted. |
| Obsolescent form | A feature of Fortran that the revision in force, or a later published revision of the Fortran standard, lists as obsolescent. |
| Extension | A form of Fortran source that a processor accepts and that the revision in force does not define; a deleted form that a processor accepts is an extension. |
| Legacy list | The list, in the repository configuration, of the entries of STND.FTN.35: each source file of Fortran that does not meet this standard, with each form and each provision of its shortfall and the reason that each stays. |
| Modernizing change | A change to Fortran source that replaces forms of that source by other forms and is meant to leave the results of the work unchanged. |

## Notes

Direction and sources. The custodian's order of standards of 2026-10-24 lists a standard for Fortran, classic and modern, and the standing directions keep each standard agnostic of platform, processor, vendor, implementation, and tool, and timeless, with strict determinism an option where it is feasible and not a requirement unless the acceptance criterion of the work or its consequence class demands it (STND.VVUQ.82, STND.VVUQ.83). The provisions therefore name the constructs of the language and no processor, option, or revision, and the term Revision in force leaves the revision to the repository configuration (GOV.18); no provision prefers the newest revision, as STND.CXX.2 does for C++ on a direction that concerns C++ alone. The source is research/fortran-notes/f1-fortran-language.md, which read the J3 working document of the 2023 revision (its S1) and cites clause numbers of that document, which are able to differ from the published text; a statement that the note marks as inference, or that it does not support, is marked unverified here. A processor in the sense of the Fortran standard includes the computing system; the term Processor of this standard is the compiler and run-time library that the repository configuration names, and STND.DEPS.8 records the revision of each with each result.

The standard adds Fortran content to provisions that already hold the outcome, and does not restate them (GOV.31). STND.CODE.3 asks for the contract at each declaration, and in Fortran the explicit interface, the intent of each dummy argument, and its kind carry it (STND.FTN.5 and STND.FTN.7); STND.CODE.4 names the static checks, and STND.FTN.38 says which Fortran gives; STND.CODE.5 names a tool for layout, and fixed source form is an obsolescent form (STND.FTN.3); STND.CODE.6 and STND.CODE.7 keep checks of untrusted data and forbid discarding a listed failure, and STND.FTN.32 and STND.FTN.33 give their Fortran forms; STND.CODE.10 asks for named constants with their units and sources, physical constants among them; and STND.CODE.13 groups the statements of each procedure into steps, in Fortran as in every language. STND.DOCS governs the documentation and the comments of Fortran source, and this standard sets no form of documentation comment for Fortran. NUMER.5 records the working precision, which in Fortran is the kind of each real entity (STND.FTN.15); STND.VVUQ.1, STND.VVUQ.3, and STND.VVUQ.5 set each comparison within a tolerance, and Fortran has no intrinsic comparison within a tolerance whose defaults would need a provision, as those of STND.PY.20 and STND.JL.21 do; HW.5 and HW.CPU.3 state and restore the floating-point control state; NUMER.16 and NUMER.17 govern a processor option that trades accuracy for speed; and NUMER.27 the capability to compute derivatives, which in Fortran rests on generic interfaces or parameterized types. STND.CONC holds the rules of concurrency for every model, STND.MPI and STND.OMP the rules of those models, and STND.CXX.20, STND.CXX.21, and STND.CXX.22 the C++ side of a foreign boundary.

Revisions and processors. Fortran was first standardized in 1966 and revised in 1978, 1991, 1997, 2004, 2010, 2018, and 2023 (S2 of the note), with the informal names FORTRAN 77 to Fortran 2023. A revision keeps all but a few features of the one before it, and a feature is made obsolescent before it is deleted (S1 4.4.1). A conforming processor is able to report each obsolescent form and each form that the numbered syntax rules and constraints do not permit, the deleted forms among them (S1 4.2), which is what the check of STND.FTN.1 asks; conformance "does not ensure that a program will execute consistently on all or any" processors (S1 4.2), so the repository configuration names the processors as well as the revision. The deleted forms are the real and double precision DO variable, a branch to an END IF from outside its block, PAUSE, ASSIGN with the assigned GO TO and assigned formats, the H edit descriptor, vertical format control, the arithmetic IF, and the nonblock DO (S1 B.1, B.2). The obsolescent forms include fixed source form, the alternate return, the computed GO TO, statement functions, assumed-length character functions, CHARACTER* declarations, ENTRY, the labeled DO, COMMON, EQUIVALENCE, BLOCK DATA, the specific names of intrinsic functions, and FORALL (S1 B.3); the list grows with each revision, so the term Obsolescent form takes the later published revisions too, and a project at an earlier revision avoids a form already marked. The check of STND.FTN.1 reports the forms of the revision in force, and review decides the rest. A deleted form that a processor still accepts is an extension, which STND.FTN.2 records and STND.FTN.3 keeps out of new statements; a statement that a change alters counts as added. A change that converts a file from fixed to free source form is a modernizing change of its own. Options of a processor that change the default kinds, give local variables static storage or an initial value, or relax floating-point semantics change the meaning of conforming source without a change to it (STND.FTN.2); that processors offer such options is from processor documentation that the note did not read, and is unverified. The compiled interface of a module comes from compiling the module, and a stale one gives wrong calls; how a build tracks compiled interfaces is specific to each processor (STND.FTN.4). The custodian's order of standards also lists a standard for builds, which is able to take STND.FTN.4 once it is adopted.

Interfaces. With an implicit interface the processor does not compare actual and dummy arguments, and a mismatch of type, kind, rank, or number is a program error that the Fortran standard does not require a processor to diagnose; an explicit interface is required in 20 situations, assumed-shape, pointer, allocatable, optional, and VALUE arguments among them (S1 15.4.2.2). A static study of scientific code, read by the note from a search extract only, reports interface inconsistencies in about one of seven interfaces of FORTRAN 77 code against one of 37 in C (S6, unverified). An interface body written for an external procedure is checked against its definition, since it otherwise repeats the error that it is meant to prevent (STND.FTN.5). Implicit typing makes a misspelled name a new variable (S1 8.7); an internal or module procedure takes the implicit typing of its host, and an interface body does not, by the rules of host association, which the note does not quote and which are unverified here (STND.FTN.6). The EXTERNAL form of IMPLICIT NONE in later revisions requires each external procedure to be declared (S1 8.7), which the explicit interfaces of STND.FTN.5 already give. A dummy argument of intent OUT is undefined on entry, an allocatable one is deallocated on entry, and one of a derived type with default initialization is reset (STND.FTN.7, STND.FTN.11). Under sequence association, "the rank and shape of the actual argument need not agree with the rank and shape of the dummy argument, but the number of elements in the dummy argument shall not exceed the number of elements in the element sequence of the actual argument" (S1 15.5.2.12); an assumed-size array has no extent in its last dimension against which to check a subscript, and a leading extent that differs between caller and callee reads another element (STND.FTN.8). Interfaces of C and of libraries outside the work fix the form in the exception.

Aliasing. While an entity is associated with a dummy argument, it is changed only through that dummy, except for the stated cases of POINTER and TARGET dummies; for CALL SUB(A(1:5), A(3:9)), "the array section A(3:5) cannot be defined, redefined, or become undefined" through either dummy (S1 15.5.2.14 and its Note 2). The processor is free to keep values in registers or reorder, the program is not conforming, and no diagnosis is required, so the failure shows at one level of optimization and not at another (STND.FTN.9). The rule is the assumption that the language lets the processor make at every call, which STND.CXX.24 and STND.JL.18 ask code to state where code makes such an assumption itself; in Fortran the rule is stated once in STND.FTN.9, and not at each call. The note names no run-time check that detects overlapping arguments. A discontiguous actual argument for an explicit-shape, assumed-size, or CONTIGUOUS dummy is able to be passed by a copy in and out (S1 Note 6 of 15.5.2.5), so a pointer or a C address that a callee keeps for such a dummy designates a temporary after the return (STND.FTN.10). The Fortran standard admits pointers that alias a TARGET dummy only in the cases that it states (S1 15.5.2.14); STND.FTN.10 is the simpler rule, and a project that relies on those cases replaces it by a recorded decision.

Defined values and saved state. Local variables, function results, dummies of intent OUT, newly allocated variables, and LOCAL variables of DO CONCURRENT have no defined value until assigned, and the Fortran standard asks no processor to detect the use (S1 4.2, 11.1.7.5); private copies under OpenMP are covered by STND.OMP.6 (STND.FTN.11). One forum thread, read from an extract, describes zero in one build mode and stale values in another, which is why the second sentence of STND.FTN.11 excludes reliance on a value that an option supplies (S8, anecdotal). Initialization of a variable "implies the SAVE attribute" (S1 8.6.7), so REAL :: s = 0.0 in a subroutine sets s once and keeps its value between calls, and the OpenMP specification treats such a local as shared (S3); this has held since Fortran 90, and before that it was processor dependent (S1 4.3.8). STND.FTN.12 makes the attribute visible where the author meant it and puts a value meant for each call in an assignment. A variable with the SAVE attribute, a module variable, and a variable in a common block are shared mutable objects under STND.CONC whenever concurrent tasks access them and one writes, which STND.CONC.3 governs; STND.FTN.13 names them because Fortran shares them without a declaration that shows it. A pure procedure meets STND.FTN.13 by construction, since the Fortran standard forbids it to define such variables and a processor diagnoses the violation (S1 15.7). COMMON and EQUIVALENCE are "error-prone" and "can inhibit performance" (S1 B.3.11): declarations of one block that differ between scoping units overlay storage silently, and one INCLUDE line for each block gives one declaration; a block declared outside a main program or a module is saved in each scoping unit that declares it (S1 8.5.16) (STND.FTN.14). Replacing COMMON by module variables, and EQUIVALENCE by TRANSFER or a derived type, is a row of STND.FTN.37.

Kinds and constants. The values of kind parameters are not specified by the language, so a literal kind number is not portable, and SELECTED_REAL_KIND maps a precision and a range to a kind (S1, S4 20.1.9) (STND.FTN.15). A real literal constant without a kind parameter is of default kind whatever the variable it initializes, and "the significand may be written with more digits than a processor will use" (S1 7.4.3.3), so 0.1 stored in a variable of a wider kind carries the rounding error of the default kind; a FORTRAN 77 processor was permitted to supply more precision in a DATA statement, and later revisions forbid it (S1 4.3.8). Where an operation combines real operands of different kinds with the same precision or range, the kind of the result is processor dependent (S1 10.1.9.3 and Annex A); STND.FTN.16 asks an explicit conversion for every mixed operation, which also shows the precision on which the code relies. Fortran has no checked integer arithmetic in the language, unlike Julia (STND.JL.17); the note found no statement of the behavior of an integer result outside the range of its kind, by a search of the text that it calls inference (unverified), and STND.FTN.17 asks the check in either case. The intrinsic function OUT_OF_RANGE of later revisions is one means of the check (S1 C.1).

Floating-point exceptions. Halting "is not precise and may occur any time after the exception has occurred", and the initial halting mode is processor dependent (S1 17.6), so a program states its mode (STND.FTN.18), HW.5 records it in the delivered arithmetic, and a halt names a location near the cause, not at it. An intrinsic procedure leaves the flags of overflow, division by zero, and invalid operation as they were on entry (S1 17.5); the procedures that save and restore the floating-point status are the means of HW.CPU.3 in Fortran, and whether a processor restores the halting and rounding modes at the return from a procedure of the work is not settled by the note (unverified). A procedure that changes the modes or flags is not permitted inside DO CONCURRENT (S1 C1145, C1146), and the note does not establish whether the flags are kept per thread (inference, unverified), which STND.OMP.30 and HW.CPU.3 leave to the scope that sets the state. Code that detects these exceptions without halting reads the flags after the operations that are able to signal them and before it relies on their results, and HW.5 states which regime the path uses. The support of the IEEE modules is a property of the processor and the kind, which the IEEE_SUPPORT inquiry functions report (STND.FTN.19); a negative answer is a precondition violation, answered as STND.FTN.31 requires. The relations <, <=, >, and >= signal on a NaN, and == and /= are quiet (S1 C.1, 17.11), so under halting at invalid operation an ordered comparison of a NaN halts the program (STND.FTN.20). A test of x /= x for a NaN is one that an option assuming finite values is able to remove, a hazard that the Notes of STND.CXX state for C++ compilers and that is unverified for Fortran processors, which is why STND.FTN.20 asks the IEEE inquiry functions and STND.FTN.33 excludes the option for a file that holds a required check.

Parallel execution. The constraints of DO CONCURRENT forbid RETURN, image control statements, branches out of the construct, references to impure procedures, and the procedures that change floating-point modes and flags, and a processor diagnoses them; the locality of a variable is LOCAL, LOCAL_INIT, REDUCE, SHARED, or unspecified; a LOCAL variable is undefined at the start of each iteration; REDUCE combines "in any order"; a variable of unspecified locality that more than one iteration defines is undefined after the construct; and a SHARED variable that one iteration defines and another references breaks the rules without a diagnosis (S1 11.1.7.5). The construct does not promise parallel execution, so STND.CONC.11 keeps its iterations from waiting on one another. DEFAULT(NONE) makes each omission of a locality a constraint that the processor checks (STND.FTN.21); locality specifiers came with the 2018 revision and REDUCE with the 2023 revision (S1 C.1, S2), and a variable declared in a BLOCK construct inside the body is local to its iteration at every revision that has DO CONCURRENT (unverified in the note). STND.CONC.21 and STND.CONC.22 govern a result that depends on the order in which REDUCE combines values or on the number of threads that a processor uses, and STND.CONC.24 the tests at several numbers of threads where a processor option runs the iterations in parallel. Images are concurrent tasks: image control statements, events, and atomic subroutines are the synchronization that STND.CONC.3 asks for coarrays; ERROR STOP ends every image (S1 11.4), which STND.CONC.2 asks of a halt and STND.FTN.34 uses; and a failed image, in the revisions that define it, changes the control flow of the other images (S1), and a status that reports it is answered under STND.FTN.32. Under OpenMP, STND.OMP.5, STND.OMP.6, and STND.OMP.7 govern data-sharing, and the Notes of STND.OMP already state that procedures with saved or initialized locals share them; STND.FTN.13 states the same for every model. Members of a common block named in a clause other than shared "no longer have a Fortran storage association with the common block" (S3), and a threadprivate common block is named as a block (STND.FTN.22). A private pointer starts with an undefined association (r2), and an allocatable list item was admitted in private and firstprivate clauses only from a later revision of the OpenMP specification (S3); and the first sentence of STND.OMP.6 covers both when allocation and association are read as writes of the copy. A clause that names a whole assumed-size array is rejected by the OpenMP implementation, and the indices of loops in a parallel region are private by rule, so neither needs a provision. The include file of OpenMP routines is deprecated by a recent revision (r1), which STND.OMP.1 keeps out, and its module gives the explicit interfaces of STND.FTN.5. The note read the OpenMP specification at revision 5.2 and takes the later text from r2.

MPI. STND.MPI says nothing of Fortran, and the MPI standard states that its Fortran bindings are "a property of an MPI library together with the Fortran compiler suite" (S4 20.1.7). A processor assumes that a local variable does not change across a call that does not receive it, so it is able to keep a buffer in a register across the wait and to "schedule the load of buf earlier than typed in the source" (S4 20.1.17.1); the ASYNCHRONOUS attribute, in a BLOCK construct or a procedure of limited scope as the example of S1 C.13 shows, or the routine that synchronizes registers after the wait, prevents it, and the MPI implementation reports through a constant whether its binding protects such buffers (STND.FTN.24). An array section with a subscript triplet given as the buffer of a nonblocking operation "may cause undefined behavior" where the implementation does not report support of array sections (S4 20.1.12), because the copy that the processor makes is released at the return of the call, before the operation completes; STND.MPI.16 keeps a buffer allocated only where code sees it, and STND.FTN.25 keeps the copy from arising. The module mpi_f08 is the only binding that the Fortran standard fully supports, and the include file mpif.h gives implicit interfaces with no checking of arguments and is deprecated by a recent revision (S4 20.1.5, 20.1.10); STND.MPI.1 keeps a deprecated facility out, STND.FTN.5 keeps out a binding with implicit interfaces, and STND.FTN.23 asks for the binding that the MPI standard states as consistent with the Fortran standard. The MPI datatypes for Fortran data are defined by kind, through the precision and range of SELECTED_REAL_KIND, and match only for equal precision and range (S4 20.1.9), which STND.FTN.26 adds to the type signatures of STND.MPI.14. A LOGICAL argument is not interoperable with C, and the value of .TRUE. is compiler dependent (S4 20.1.5); the handles of mpi_f08 are derived types, and their conversion to and from the handles of C and of the older bindings is by the functions of the MPI standard.

Interoperability with C. BIND(C), the kinds of ISO_C_BINDING, C_PTR, and the C descriptor define the boundary; later revisions let an interoperable procedure take allocatable, pointer, optional, assumed-shape, and assumed-rank dummies (S1 18, C.1). The extents and strides in a C descriptor have the C type ptrdiff_t and not default integer, the layout of the descriptor is fixed only through its functions, and a LOGICAL of default kind is not interoperable (S1 18) (STND.FTN.29). A test with an array section of a stride other than one exercises the descriptor where errors of stride hide (STND.FTN.30). The C declarations of such procedures belong in one header of the work, which the standards of C and C++ govern on their side; STND.CXX.20, STND.CXX.21, and STND.CXX.22 keep C++ exceptions and resources from crossing the boundary, and a C standard is in the custodian's order of standards.

Failures. Fortran has no exceptions, so the responses that PRIME.4 admits are a halt with a diagnosis, the designed safe state, a visible degradation, and the return of the condition in a status argument or a result (STND.FTN.31). Without a STAT=, IOSTAT=, or CMDSTAT= specifier, an error of an ALLOCATE, an input or output statement, or a command ends the program by error termination, a halt whose diagnosis is the processor's (a rule of the Fortran standard that the note does not quote, unverified in the note); with the specifier, the program receives the condition and answers it (STND.FTN.32), and the ERRMSG= and IOMSG= specifiers give the text of the diagnosis. A failed allocation is resource exhaustion, and an input record that does not match its format is invalid input; an end of file that the code expects is not a condition that PRIME.4 lists, and STND.CODE.12 governs a status that code discards for another reason. Checks of subscripts against bounds are a facility of the processor, set by an execution setting, and the Fortran standard requires no processor to diagnose an out-of-range subscript, so a check of an untrusted subscript is written as a test in the code (STND.FTN.33); the reach of untrusted data is that of STND.CODE.6, which this standard does not widen. The second sentence of STND.FTN.33 is the Fortran form of the second sentence of STND.CXX.18. A STOP statement initiates normal termination, and ERROR STOP ends every image with error termination (S1 11.4), so a halt on a failure by ERROR STOP keeps a workflow from reading it as a normal end (STND.FTN.34); the exit status that a processor reports for each is not in the note and is unverified.

Legacy source and modernization. Steps that change no result by the semantics of the language are a conversion of source form checked by identical output, IMPLICIT NONE with each name declared, a common block replaced by module variables with the same declarations in the same order and with SAVE, a computed GO TO replaced by SELECT CASE, a labeled DO replaced by END DO, specific intrinsic names replaced by generic names, and external procedures moved into a module, which exposes mismatches and so changes a result that was wrong (section 7 of the note). The steps that are able to change a result are the rows of STND.FTN.37. That an intrinsic reduction, SUM among them, combines in an order of the processor's choice is stated by the note without a quotation and is unverified. Columns of fixed-form source past the last significant position are ignored, so a conversion to free form that keeps them makes them part of the statement, by the note's inference from the significance of position 72 (unverified). One study of climate models finds that old features of Fortran are still in use and proposes metrics for the changes a program needs (S7, from an abstract extract, unverified); the comparison before and after each step, under a criterion stated first, is the practice that STND.FTN.36 asks (VV.3, STND.VVUQ.1). Under STND.VVUQ.82 and STND.VVUQ.83, a difference within the declared variation is no defect, and an agent does not change the work only to remove it. The legacy list follows the list of exempted modules of STND.PY.6: existing source enters it at the change that adopts this standard, and leaves it by modernizing changes; a change that incorporates external Fortran code is governed by STND.DEPS.11, which keeps that code apart. The studies of defects in Fortran codes read by the note are a static study of FORTRAN 77 of the 1990s (S6, extract only) and a study of defect densities of climate models with no classification by feature (S5); no study classifies defects of Fortran by language feature, so the hazards rest on what the Fortran standard leaves undefined.

Checks. A processor is able to report the obsolescent forms, the forms that the numbered syntax rules and constraints do not permit, an unsupported kind, inconsistent use of names, and a nonstandard intrinsic procedure or module (S1 4.2), so the numbered constraints are checkable during compilation (STND.FTN.1, STND.FTN.38). The rules that the Fortran standard states without a constraint are not: overlap of arguments, use of an undefined value, a subscript out of range, a shape that sequence association mismatches, an integer out of range, and unsynchronized access. They are checked by the runs of STND.FTN.39 and STND.FTN.40, by STND.CONC.25 for data races, and by review. A check that the Fortran standard does not require is able to be absent from a processor, which is why the second sentence of STND.FTN.39 has a condition; STND.CXX.26 is the model.

Binding provisions. STND.FTN.31, STND.FTN.32, and STND.FTN.33 instantiate PRIME.4 and bind at every class, CSQ4 included. None asks for work that PRIME.4 does not (GOV.11). STND.FTN.31 lists the responses that PRIME.4 admits, in the form that STND.CXX.16, STND.PY.22, and STND.JL.15 give them. STND.FTN.32 asks the response that PRIME.4 already requires to a listed condition that a status reports, which STND.CODE.7 keeps from being discarded, at the cost of one test of the status. The first sentence of STND.FTN.33 asks the check of STND.CODE.6 in the one form that no execution setting removes in Fortran, at the cost of one test for each untrusted subscript, and the second asks one choice of option for a file that holds a required check. Without them, a failed allocation or read under a status specifier, or a subscript from untrusted data, passes silently.

Class onset. Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, REPRO, VV, or a provision of NUMER or HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row: STND.FTN.8, the first sentence of STND.FTN.14, STND.FTN.26, and the second sentence of STND.FTN.29 rest on DSGN.4 and apply from CSQ2. STND.FTN.13 and the second sentence of STND.FTN.21 state what a protocol uses, and not how its invariants are verified, which DSGN.15 starts at CSQ2, so they apply from CSQ3. STND.FTN.17 checks preconditions where untrusted data enters, which DSGN.2 asks from CSQ3, not the postconditions that STND.CLASS.10 starts at CSQ1. STND.FTN.1, STND.FTN.5, STND.FTN.6, the first sentence of STND.FTN.23, the first sentence of STND.FTN.29, the second sentence of STND.FTN.35, STND.FTN.38, STND.FTN.39, and STND.FTN.40 ask for mechanical checks under DSGN.3 from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0, stays with that row. STND.FTN.30 is a test under VV.1 that compares with no reference oracle produced without the implementation that it judges, and applies from CSQ3. Each sentence that cites NUMER.5, HW.3, or HW.5 also cites a provision of LVL0 through which it applies to all work from CSQ3, the part that rests on NUMER or HW applying only to work that those profiles bind. Every other provision rests on no row and applies from CSQ3. No provision has three modals. No default raises the floor (GOV.11).

Existing Fortran source enters the legacy list at the change that adopts this standard, and meets the provisions that the list names for it by modernizing changes.

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.JL | Julia standard |
| STND.MPI | Message Passing Interface standard |
| STND.OMP | OpenMP standard |
| STND.PY | Python standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Revision and build

#### STND.FTN.1 Revision in force

Default. Instantiates REPRO.2, SIMPL.6, DSGN.3.

The repository configuration SHOULD state the revision in force of each source file of Fortran, with each option by which each processor of the work is set to that revision (REPRO.2, SIMPL.6). Each change SHOULD pass a check in which a processor of the work reports each form of the Fortran source that the revision in force does not define or lists as obsolescent, and that fails on each such form that the legacy list does not hold for its file (DSGN.3).

#### STND.FTN.2 Stated processor options

Default. Instantiates SIMPL.6, REPRO.2, HW.5, REPRO.7.

The repository configuration SHOULD state, for each source file of Fortran, each option of its processor that changes a default kind, the storage or the initial value of local variables, the floating-point semantics or the contraction of operations, or the target instruction set (SIMPL.6, REPRO.2, HW.5). Where Fortran source uses an extension, the repository configuration SHOULD state each processor of the work that accepts that extension and the documentation in which the processor gives its meaning (SIMPL.6, REPRO.7).

#### STND.FTN.3 Deleted and obsolescent forms

Default. Instantiates SIMPL.6.

Each statement that a change adds to Fortran source or alters SHOULD use only forms that the revision in force defines (SIMPL.6). Other than the fixed source form of a file that the legacy list holds, each statement that a change adds to Fortran source or alters SHOULD NOT use an obsolescent form (SIMPL.6).

#### STND.FTN.4 Module compilation order

Default. Instantiates DSGN.7, VV.8.

The build of Fortran source SHOULD derive the order in which it compiles program units from their USE statements and from the ancestry of their submodules (DSGN.7). At each change to the interface of a module, the build SHOULD recompile each program unit that uses that module, directly or through another module (VV.8).

### Interfaces and arguments

#### STND.FTN.5 Explicit interfaces

Default. Instantiates DSGN.1, DSGN.3.

Each procedure that Fortran source of the work references SHOULD have an explicit interface at each reference, from a module, by host association, or from an interface body (DSGN.1, DSGN.3). Where an interface body declares a procedure that the work defines outside a module, a static check SHOULD compare that interface body with the definition of the procedure at each change to either (DSGN.3).

#### STND.FTN.6 Implicit typing excluded

Default. Instantiates SIMPL.6, DSGN.3.

Each program unit and each interface body of Fortran source SHOULD contain an IMPLICIT NONE statement (SIMPL.6, DSGN.3).

#### STND.FTN.7 Declared argument intent

Default. Instantiates DSGN.1.

Each dummy data object of a procedure that the work defines in Fortran SHOULD have the INTENT attribute or the VALUE attribute (DSGN.1).

#### STND.FTN.8 Assumed-size dummy arrays

Default. Instantiates DSGN.4.

Other than in an interface that a library outside the work or a procedure with the BIND attribute fixes, a dummy argument SHOULD NOT be an assumed-size array (DSGN.4).

#### STND.FTN.9 Argument aliasing

Default. Instantiates DSGN.1.

While an entity is associated with a dummy argument that has neither the POINTER attribute nor the TARGET attribute, code SHOULD change the value or the allocation status of that entity, or of a part of it, only through that dummy argument (DSGN.1).

#### STND.FTN.10 Pointers to dummy arguments

Default. Instantiates DSGN.14.

A pointer that a procedure associates with a dummy argument without the POINTER attribute, or with a part of one, SHOULD NOT be referenced after that procedure returns (DSGN.14). A C address that a procedure obtains for a dummy argument without the POINTER attribute, or for a part of one, SHOULD NOT be used after that procedure returns (DSGN.14).

### Values and storage

#### STND.FTN.11 Values defined before reference

Default. Instantiates DSGN.1, SIMPL.6.

Code SHOULD NOT reference the value of a variable at a point at which the Fortran standard leaves that variable undefined (DSGN.1). Code SHOULD NOT rely on an initial value that an option of a processor gives a variable (SIMPL.6).

#### STND.FTN.12 Explicit SAVE of initialized locals

Default. Instantiates SIMPL.6, DSGN.14.

Each local variable of a procedure that its declaration or a DATA statement initializes SHOULD have the SAVE attribute stated in its declaration or in a SAVE statement of that procedure (SIMPL.6). Where a procedure relies on a value of a local variable at each entry to it, the procedure SHOULD assign that value in its executable part (DSGN.14).

#### STND.FTN.13 Saved state in concurrent calls

Default. Instantiates DSGN.15, DSGN.14.

Where more than one concurrent task is able to execute a procedure at once, the procedure SHOULD define a variable with the SAVE attribute, a module variable, or a variable in a common block only under the protection that STND.CONC.3 states for that variable (DSGN.15, DSGN.14).

#### STND.FTN.14 Common block declarations

Default. Instantiates DSGN.4, DSGN.14.

Each common block SHOULD be declared, with the same members in the same order and of the same types, kinds, and shapes, by one source text that each scoping unit that declares the block includes (DSGN.4). In each scoping unit other than a main program, a module, or a submodule, each common block that the scoping unit declares SHOULD have the SAVE attribute (DSGN.14).

### Kinds and floating point

#### STND.FTN.15 Named kind parameters

Default. Instantiates SIMPL.6, NUMER.5, REPRO.2.

Each declaration of a real or a complex entity in Fortran source SHOULD give its kind by a named constant (SIMPL.6, NUMER.5). Each such named constant SHOULD take its value, in one module of the work, from an intrinsic function that selects a kind by its precision and range or from a named constant of an intrinsic module (REPRO.2, NUMER.5).

#### STND.FTN.16 Kinds in literals and operations

Default. Instantiates SIMPL.6, NUMER.5.

Each real literal constant, the real parts of a complex literal constant included, SHOULD carry a kind parameter (SIMPL.6, NUMER.5). Where an intrinsic operation combines real or complex operands of different kinds, code SHOULD convert one of them explicitly, by an intrinsic conversion function with a kind argument (SIMPL.6, NUMER.5).

#### STND.FTN.17 Integer range checks

Default. Instantiates DSGN.2.

Where integer arithmetic on untrusted data is able to exceed the range of its kind, code SHOULD check, before the operation, that its result stays within that range (DSGN.2).

#### STND.FTN.18 Floating-point halting modes

Default. Instantiates SIMPL.6, HW.5.

Each program SHOULD set the halting modes of invalid operation, overflow, and division by zero at its start, by the procedures of the intrinsic module IEEE_EXCEPTIONS or by an option of its processor that the repository configuration states (SIMPL.6, HW.5).

#### STND.FTN.19 IEEE support confirmed

Default. Instantiates SIMPL.6, HW.5.

Where code relies on a facility of an intrinsic IEEE module for a kind, it SHOULD confirm, by the inquiry function of that module for that facility, that the processor supports the facility for that kind (SIMPL.6, HW.5).

#### STND.FTN.20 Non-finite tests and comparisons

Default. Instantiates SIMPL.6, HW.5.

Code SHOULD test whether a real value is a NaN or an infinity only by the functions of the intrinsic module IEEE_ARITHMETIC that classify a value (SIMPL.6, HW.5). Where a program halts at invalid operation, each comparison of values that are able to be NaN SHOULD be one that the Fortran standard defines as signaling no exception on a NaN (SIMPL.6).

### Parallel execution

#### STND.FTN.21 DO CONCURRENT locality

Default. Instantiates SIMPL.6, DSGN.15.

Where the revision in force provides locality specifiers, each DO CONCURRENT construct SHOULD carry the locality specifier DEFAULT(NONE) (SIMPL.6). Each variable that an iteration of a DO CONCURRENT construct defines SHOULD be local to that iteration, have REDUCE locality, or be defined only at elements of an array that no other iteration of the construct references or defines (DSGN.15).

#### STND.FTN.22 Common blocks in OpenMP clauses

Default. Instantiates DSGN.14.

Where code relies on the storage association among the members of a common block, each data-sharing clause of OpenMP other than shared that privatizes members of that block SHOULD name the whole block (DSGN.14).

### MPI

#### STND.FTN.23 Fortran binding of MPI

Default. Instantiates DSGN.3, HW.3, REPRO.2.

Where the MPI implementation of the work provides the Fortran binding of MPI that the MPI standard states as consistent with the Fortran standard, Fortran code SHOULD call MPI through that binding (DSGN.3). Among the items of STND.MPI.2, the record of each result that Fortran code computes with MPI SHOULD give the Fortran binding of MPI that the code uses, and whether the MPI implementation reports for that binding that it protects the buffers of pending operations and that it supports array sections as buffers (HW.3, REPRO.2).

#### STND.FTN.24 Asynchronous MPI buffers

Default. Instantiates DSGN.14.

Each variable that is the buffer of a pending nonblocking, persistent, or one-sided operation of MPI, or of a split collective operation, SHOULD have the ASYNCHRONOUS attribute in each scoping unit that references it between the start and the completion of that operation (DSGN.14). Where the MPI implementation reports that its Fortran binding does not protect such buffers, code SHOULD call, after each completion call and before it accesses the buffer, the routine that the MPI standard gives for the synchronization of registers, with that buffer as its argument (DSGN.14).

#### STND.FTN.25 Array sections in pending operations

Default. Instantiates DSGN.14.

Where the MPI implementation does not report that its Fortran binding supports array sections as buffers, each buffer that Fortran code passes to a nonblocking, persistent, or one-sided operation of MPI, or to a split collective operation, SHOULD be contiguous (DSGN.14).

#### STND.FTN.26 MPI datatypes of Fortran kinds

Default. Instantiates DSGN.4.

Each MPI datatype that describes Fortran data of an intrinsic type SHOULD be the datatype that the MPI standard gives for the type and the kind type parameter that declare that data (DSGN.4).

### Input and output

#### STND.FTN.27 Unit numbers of connections

Default. Instantiates DSGN.14, SIMPL.6.

Each unit that Fortran code connects by an OPEN statement SHOULD take its number from the NEWUNIT= specifier, or from one module of the work that assigns each unit number of the work once (DSGN.14). Code SHOULD refer to a preconnected unit by an asterisk or by a named constant of the intrinsic module ISO_FORTRAN_ENV, and not by a literal number (SIMPL.6).

#### STND.FTN.28 Order of parallel output records

Default. Instantiates REPRO.3.

Code SHOULD NOT rely on the order of the records that different iterations of one DO CONCURRENT construct write to one file (REPRO.3). Code SHOULD NOT rely on the order of the records that different images write to one file (REPRO.3).

### Interoperability with C

#### STND.FTN.29 C interoperable interfaces

Default. Instantiates DSGN.3, DSGN.1, DSGN.4.

Each procedure through which Fortran code and C code call one another SHOULD have the BIND attribute, with its Fortran interface declared once, in one module of the work (DSGN.3, DSGN.1). Each dummy argument of such a procedure SHOULD have the type, and the kind that the intrinsic module ISO_C_BINDING names, that interoperate with the type that the C declaration of the procedure gives the corresponding parameter (DSGN.4).

#### STND.FTN.30 Descriptors across the C boundary

Default. Instantiates VV.1.

Where a procedure with the BIND attribute passes an array by a C descriptor, its tests SHOULD pass across that procedure an array section with a stride other than one (VV.1).

### Failures

#### STND.FTN.31 Fortran responses to listed failures

Binding. Instantiates PRIME.4.

Where Fortran code detects a condition that PRIME.4 lists, it SHALL halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or return the condition to its caller in a status argument or in its result (PRIME.4).

#### STND.FTN.32 Status specifiers answered

Binding. Instantiates PRIME.4.

Before code relies on the outcome of a statement whose STAT=, IOSTAT=, or CMDSTAT= specifier, or of a call of an intrinsic procedure whose status argument, receives a value that reports a condition that PRIME.4 lists, it SHALL respond to that condition as STND.FTN.31 requires (PRIME.4).

#### STND.FTN.33 Unremovable Fortran input checks

Binding. Instantiates PRIME.4, DSGN.2.

Where a subscript or a substring position derives from untrusted data, code SHALL reject an invalid value of it, before its use, by a test that no execution setting removes, against the bounds of the array or the length of the string (PRIME.4, DSGN.2). A source file that holds a check of a floating-point value that STND.CODE.6 requires SHALL NOT be compiled with an option that lets the processor assume that floating-point values are finite (PRIME.4).

#### STND.FTN.34 Halts by ERROR STOP

Default. Instantiates SIMPL.6.

Other than by the abort facility of MPI under STND.MPI.6, Fortran code SHOULD halt on a failure by an ERROR STOP statement whose stop code or message states the diagnosis (SIMPL.6).

### Legacy source

#### STND.FTN.35 Legacy source list

Default. Instantiates REPRO.7, DSGN.3.

Where a source file of Fortran uses a form that the check of STND.FTN.1 reports, or does not meet STND.FTN.5, STND.FTN.6, STND.FTN.7, STND.FTN.8, STND.FTN.12, STND.FTN.14, STND.FTN.15, STND.FTN.16, or STND.FTN.27, the repository configuration SHOULD hold an entry for that file in the legacy list, with each such form and provision and the reason that each stays (REPRO.7). Other than a change that incorporates external code into the work, a change SHOULD NOT add an entry to the legacy list (DSGN.3).

#### STND.FTN.36 Modernizing changes verified

Default. Instantiates VV.3, VV.8.

Before each modernizing change, a record SHOULD state the comparison, with its tier of STND.VVUQ.1 and its tolerance, that judges the results of the tests carrying the evidence of the code that the change touches (VV.3). Each modernizing change SHOULD be verified by running those tests before and after it and judging their results by that comparison (VV.8).

#### STND.FTN.37 Result-changing replacements

Default. Instantiates REPRO.7, VV.3.

Where a change makes a replacement that the table of this provision lists, that replacement SHOULD be made in a change of its own, whose record states the results that the replacement is able to change and the acceptance criterion that judges them (REPRO.7, VV.3).

| Replacement | What it is able to change |
| --- | --- |
| A kind parameter added to a real literal constant, or a real entity of default kind given another kind | The value of the constant, and the precision of the arithmetic that uses it |
| An initialization that implies the SAVE attribute replaced by an assignment at entry, or the SAVE attribute removed | The value that a local variable holds at entry to a later call |
| An explicit-shape or assumed-size dummy array made assumed-shape | Whether the procedure receives the storage of its actual argument or a copy of it |
| A common block or an EQUIVALENCE statement replaced by module variables, by a derived type, or by the TRANSFER intrinsic function | The value that one name holds after a definition through another name that storage association overlaid |
| A loop replaced by an array expression, an intrinsic reduction, or a DO CONCURRENT construct | The order of floating-point operations |
| An extension, a deleted form among them, replaced by a form that the revision in force defines | The behavior that a processor gave the extension, the number of iterations of a loop with a real DO variable among them |
| An explicit interface given to a procedure that a reference called with an actual argument that disagreed with its dummy argument | The values that the procedure receives from that reference |

### Checking

#### STND.FTN.38 Fortran static checks

Default. Instantiates DSGN.3.

The static checks that the repository configuration names for Fortran under STND.CODE.4 SHOULD include, at a recorded set of options of each processor of the work, a report of each reference to a procedure without an explicit interface, of each disagreement in type, kind, rank, or number between actual and dummy arguments across source files, and of each implicitly typed name (DSGN.3). Other than a warning on a form or a provision that an entry of the legacy list holds, each warning of a processor on the Fortran source of the work SHOULD fail the checks of the change that causes it (DSGN.3).

#### STND.FTN.39 Run-time Fortran checks

Default. Instantiates DSGN.3.

Among the checks of each change to the Fortran code of the work, its tests SHOULD run in a build that checks at run time each subscript and each substring range against its bounds, and each reference to a pointer or an allocatable variable against its association or allocation status, and that fails the test at the first detection (DSGN.3). Where a processor of the work provides a build that reports each reference to an undefined value, or one that gives each variable without a defined initial value a value that shows in results, the tests SHOULD also run in that build (DSGN.3).

#### STND.FTN.40 Floating-point exceptions under test

Default. Instantiates DSGN.3.

Where code of the work does not rely on continuing past an invalid operation, an overflow, or a division by zero, its tests SHOULD include a run that halts at the first of them and reports its location (DSGN.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
