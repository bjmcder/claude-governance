# Fortran standard (STND.FTN) 1.4

Adopted by The Custodian as revision 1.0 in ledger entry 134 (2026-10-24); revised to 1.1 in entry 151 (2026-10-25), 1.1.1 in entry 190 (2026-10-27), 1.2 in entry 217 (2026-10-28), 1.3 in entry 270 (2026-10-28), and 1.4 in entry 312 (2026-10-28). This reading copy is composed from the per-provision files in STND/FTN/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.FTN.18, STND.FTN.29, and STND.FTN.37.

## Purpose and scope

This standard holds the coding practice that is specific to Fortran, in source written to every revision of the Fortran standard, classic and modern. It adds to STND.CODE, STND.DOCS, STND.BUILD, STND.CONC, STND.MPI, STND.OMP, NUMER, and HW only what the language makes necessary. It covers the revision in force, the options of compilers, and deleted and obsolescent forms (STND.FTN.1, STND.FTN.2, and STND.FTN.3); interfaces and the association of arguments (STND.FTN.4 to STND.FTN.8); defined values, implied and explicit SAVE, and storage association (STND.FTN.9 to STND.FTN.12); kinds, literal constants, and floating-point exceptions (STND.FTN.13 to STND.FTN.17); parallel execution in DO CONCURRENT and OpenMP (STND.FTN.19 and STND.FTN.20); the Fortran forms of the hazards of MPI (STND.FTN.21 to STND.FTN.24); input and output (STND.FTN.25 and STND.FTN.26); interoperability with C (STND.FTN.27 and STND.FTN.28); failures (STND.FTN.30, STND.FTN.31, and STND.FTN.32); legacy source and its modernization without a change of results (STND.FTN.33 and STND.FTN.34); and the checks of Fortran code at run time (STND.FTN.35 and STND.FTN.36).

STND.FTN.30 and STND.FTN.31 instantiate PRIME.4, so they are binding and apply at every class. The rules of code that hold for every language, the responses to a listed failure, the checks that no execution setting removes, and the convention of names among them, are in STND.CODE (STND.CODE.14 to STND.CODE.35), and this standard gives their Fortran forms. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is agnostic of compiler, vendor, platform, tool, and revision of the Fortran standard: it names the statements, attributes, specifiers, and intrinsic modules of the language, and no compiler, option, or revision, and the repository configuration chooses the revision and the compilers (GOV.18). A provision that names a facility that not every revision provides applies where the revision in force provides it, as its condition states.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that STND.CODE gives them. For the term Untrusted input, the values that a procedure receives through its dummy arguments are its arguments, and each procedure that a module of the work makes public, by an attribute, by a statement, or by default, and each procedure of the work with the BIND attribute, is in the public interface that the term Untrusted input of STND.CODE takes in. Compilation unit and Checking build have the meanings that STND.BUILD gives them. Concurrent task and Protection have the meanings that STND.CONC gives them; each image, each thread that runs an OpenMP parallel region, and each iteration of a DO CONCURRENT construct is a concurrent task. MPI standard and MPI implementation have the meanings that STND.MPI gives them, and nonblocking operation and MPI datatype the meanings that the MPI standard gives them. Data-sharing clause has the meaning that the OpenMP specification of STND.OMP gives it. Program unit, scoping unit, main program, module, submodule, procedure, interface body, explicit interface, dummy argument, dummy data object, actual argument, common block, storage association, default initialization, assumed-shape array, assumed-size array, explicit-shape array, array section, subscript triplet, kind type parameter, literal constant, intrinsic module, image, locality specifier, C descriptor, unit, and preconnected have the meanings that the Fortran standard gives them.

| Term | Definition |
| --- | --- |
| Fortran standard | The international standard of the Fortran programming language, ISO/IEC 1539-1, at the revision that the text names, or otherwise at the revision in force. |
| Revision in force | Of a source file of Fortran: the revision of the Fortran standard to which the file is written. |
| Deleted form | A feature of Fortran that a published revision of the Fortran standard lists as deleted. |
| Obsolescent form | A feature of Fortran that the revision in force, or a later published revision of the Fortran standard, lists as obsolescent. |
| Extension | A form of Fortran source that a compiler of the work accepts and that the revision in force does not define; a deleted form that a compiler accepts is an extension. |
| Legacy list | The list, in the repository configuration, of the entries of STND.FTN.33: each source file of Fortran, or each set of such files that a directory or a pattern of names gives, that uses a form that the check of STND.FTN.1 reports, or that does not meet a provision that STND.FTN.33 names, with those forms and provisions and their reasons. |
| Modernizing change | A change to Fortran source that replaces forms of that source by other forms and is meant to leave the results of the work unchanged. |

## Notes

Direction and sources. The custodian's order of standards of 2026-10-24 lists a standard for Fortran, classic and modern, and the standing directions keep each standard agnostic of platform, compiler, vendor, implementation, and tool, and timeless, with strict determinism an option where it is feasible and not a requirement unless the acceptance criterion of the work or its consequence class demands it (STND.VVUQ.82, STND.VVUQ.83). The provisions therefore name the constructs of the language and no compiler, option, or revision. The custodian's directions for C++ and for Julia ask for the newest edition or version, which STND.CXX.2 and STND.JL.1 follow; no direction of the custodian that the corpus records asks the same for Fortran, so STND.FTN.1 has the repository configuration state the revision in force of each file and prefers no revision. This standard defines Revision in force, of a source file and of the Fortran standard, apart from the Edition in force of STND.CXX, which is of a translation unit and of the ISO C++ standard, so that each term keeps the scope of its own standard. A provision that names a facility of a later revision carries the condition that the revision in force provides it, as the first sentence of STND.FTN.19 does; a file at an earlier revision meets such a provision through a modernizing change that raises its revision in force, which is the project's choice. The source is research/fortran-notes/f1-fortran-language.md, which cites the clause numbers of the J3 working document of the latest revision that it read (its S1), able to differ from the published text; a statement that the note marks as inference, or that it does not support, is marked unverified. The note research/round-addenda/a1-confirmations.md (a1) confirms the facts on initialization and the SAVE attribute from the same working document. The Fortran standard calls a compiler, its run-time library, and the computing system together a processor; the provisions say compiler, and STND.DEPS.8 records the revision of each compiler with each result.

The standard adds Fortran content to provisions that already hold the outcome, and does not restate them (GOV.31). STND.DOCS governs the documentation and the comments of Fortran source, from the reader they are written for (STND.DOCS.1) to their agreement with the code (STND.DOCS.11), and this standard sets no form of documentation comment. STND.BUILD holds the build. The compiled interface of a module is a generated file of STND.BUILD, which a build step writes and a later step reads as the interface of a unit that the source names: STND.BUILD.2 derives those inputs from the USE statements and the submodules of the source, STND.BUILD.3 keeps an incremental build equal to a clean one, and STND.BUILD.4 makes the file again only by its generator, so a stale interface does not reach a later compilation. STND.BUILD.11 states each setting that is able to change a result, and STND.FTN.2 names the ones that Fortran adds; STND.BUILD.12 fails the checks of a change on each warning of the toolchain; and STND.BUILD.13 keeps the checking builds of STND.FTN.35 apart. NUMER.5 records the working precision, which in Fortran is the kind of each real entity (STND.FTN.13); STND.VVUQ.1, STND.VVUQ.3, and STND.VVUQ.5 set each comparison within a tolerance, and STND.CODE.31 has the comparison state their parameters, which Fortran, with no intrinsic comparison within a tolerance, states in the expression; HW.5 and HW.CPU.3 state and restore the floating-point control state; and NUMER.16 and NUMER.17 govern an option that trades accuracy for speed. STND.CONC holds the rules of concurrency for every model, STND.MPI and STND.OMP the rules of those models, STND.CODE.22 to STND.CODE.26 the rules of each foreign interface, and STND.CXX.21 the C++ side of one.

Revisions and compilers. A conforming processor is able to report each obsolescent form and each form that the numbered syntax rules and constraints do not permit, the deleted forms among them (S1 4.2), which is what the check of STND.FTN.1 asks; conformance "does not ensure that a program will execute consistently on all or any" processors (S1 4.2), which is why STND.FTN.1 and STND.DEPS.8 concern the compilers as well as the revision. The deleted forms include the real DO variable, PAUSE, ASSIGN, the H edit descriptor, the arithmetic IF, and the nonblock DO (S1 B.1, B.2); the obsolescent forms include fixed source form, the computed GO TO, statement functions, ENTRY, the labeled DO, COMMON, EQUIVALENCE, the specific names of intrinsic functions, and FORALL (S1 B.3). The list has grown at most revisions, and the latest revision that the note read added none (S2), so the term Obsolescent form takes the later published revisions as well, while the check of STND.FTN.1 reports only the forms that the revision in force lists. A deleted form that a compiler still accepts is an extension, which STND.FTN.2 records and STND.FTN.3 keeps out of new and altered statements. A conversion of a file from fixed to free source form is a modernizing change of its own. The exception in the second sentence of STND.FTN.3 lets a change gather the declarations of an existing common block into the one source text of STND.FTN.12; the replacement of the block by module variables, a row of STND.FTN.34, removes the form. That compilers offer options that change the default kinds, or give local variables static storage or an initial value, is unverified; such an option changes the meaning of conforming source without a change to it (STND.FTN.2).

Interfaces. With an implicit interface the compiler does not compare actual and dummy arguments, and a mismatch of type, kind, rank, or number is a program error that the Fortran standard does not require a processor to diagnose; an explicit interface is required in 20 situations, assumed-shape, pointer, allocatable, optional, and VALUE arguments among them (S1 15.4.2.2). An interface body written for an external procedure repeats the error that it is meant to prevent unless it is compared with the definition, which the second sentence of STND.FTN.4 asks; a reference that reaches no explicit interface is the report that the same check makes, and STND.BUILD.12 fails the change on it. Where the compilers and tools of the work offer neither check, the second sentence asks nothing, and the first still asks an explicit interface at each reference. Implicit typing makes a misspelled name a new variable (S1 8.7); an internal or module procedure takes the implicit typing of its host and an interface body does not, by the rules of host association (unverified) (STND.FTN.5). A dummy argument of intent OUT is undefined on entry, an allocatable one is deallocated on entry, and one of a derived type with default initialization is reset (STND.FTN.5, STND.FTN.9). Under sequence association, "the rank and shape of the actual argument need not agree with the rank and shape of the dummy argument, but the number of elements in the dummy argument shall not exceed the number of elements in the element sequence of the actual argument" (S1 15.5.2.12); an assumed-size array has no extent in its last dimension against which to check a subscript, and a leading extent that differs between caller and callee reads another element (STND.FTN.6). Interfaces of C and of libraries outside the work fix the form in the exception.

Aliasing. While an entity is associated with a dummy argument, it is changed only through that dummy, except in the stated cases of POINTER and TARGET dummies; for CALL SUB(A(1:5), A(3:9)), "the array section A(3:5) cannot be defined, redefined, or become undefined" through either dummy (S1 15.5.2.14 and its Note 2). The compiler is free to keep values in registers or to reorder, the program is not conforming, and no diagnosis is required, so the failure shows at one level of optimization and not at another (STND.FTN.7). A further restriction of the same clause on references through other names during the call is unverified, and STND.FTN.7 does not state it. A discontiguous actual argument for an explicit-shape, assumed-size, or CONTIGUOUS dummy is able to be passed by a copy in and out (S1 Note 6 of 15.5.2.5), so a pointer or a C address that a callee keeps for such a dummy designates a temporary after the return (STND.FTN.8). The Fortran standard admits pointers that alias a TARGET dummy only in the cases that it states (S1 15.5.2.14); STND.FTN.8 is the simpler rule, and a project that relies on those cases replaces it by a recorded decision.

Defined values and saved state. Local variables, function results, dummies of intent OUT, newly allocated variables, and LOCAL variables of DO CONCURRENT have no defined value until assigned, and the Fortran standard asks no processor to detect the use (S1 4.2, 11.1.7.5); private copies under OpenMP are covered by STND.OMP.6 (STND.FTN.9). Explicit initialization of a variable that is not in a common block "implies the SAVE attribute" (a1, 8.4 paragraph 3), and a variable that a DATA statement initializes has the SAVE attribute (a1, 8.6.7), so REAL :: s = 0.0 in a subroutine sets s once and keeps its value between calls, and the OpenMP specification treats such a local as shared (S3); this has held since the revision that introduced free source form, and before that it was processor dependent (S1 4.3.8). STND.FTN.10 makes the attribute visible where the author meant it and puts a value meant for each call in an assignment. Unlike explicit initialization, the default initialization of a component of a derived type does not imply that the object has the SAVE attribute (a1, 7.5.4.6), so the first sentence of STND.FTN.10 excepts a variable that only default initialization initializes; that note read the working document of the latest revision alone, and that earlier revisions agree is unverified. A variable with the SAVE attribute, a module variable, and a variable in a common block are shared mutable objects under STND.CONC whenever concurrent tasks access them and one writes, which STND.CONC.3 governs; STND.FTN.11 names them because Fortran shares them without a declaration that shows it. A pure procedure meets STND.FTN.11 by construction, since the Fortran standard forbids it to define such variables and a processor diagnoses the violation (S1 15.7). COMMON and EQUIVALENCE are "error-prone" and "can inhibit performance" (S1 B.3.11): declarations of one block that differ between scoping units overlay storage silently, and one INCLUDE line for each block gives one declaration; a block declared outside a main program or a module is saved in each scoping unit that declares it (S1 8.5.16) (STND.FTN.12).

Kinds and constants. The values of kind parameters are not specified by the language, so a literal kind number is not portable, and SELECTED_REAL_KIND maps a precision and a range to a kind (S1, S4 20.1.9) (STND.FTN.13). A real literal constant without a kind parameter is of default kind whatever the variable it initializes, and "the significand may be written with more digits than a processor will use" (S1 7.4.3.3), so 0.1 stored in a variable of a wider kind carries the rounding error of the default kind. The first sentence of STND.FTN.14 therefore reaches the literals that meet an entity of another kind, written with a kind parameter or with a D exponent for double precision. Where an operation combines real operands of different kinds with the same precision or range, the kind of the result is processor dependent (S1 10.1.9.3 and Annex A); the second sentence of STND.FTN.14 asks an explicit conversion for every mixed operation, which also shows the precision on which the code relies. Fortran has no checked integer arithmetic in the language, unlike Julia (STND.JL.17); the behavior of an integer result outside the range of its kind is not established (inference, unverified), and STND.FTN.15 asks the check in either case.

Floating-point exceptions. Halting "is not precise and may occur any time after the exception has occurred", and the initial halting mode is processor dependent (S1 17.6), which is why STND.FTN.16 has the main program set it and HW.5 records it in the delivered arithmetic; a halt names a location near the cause, not at it. A library has no start of its own: a library that sets the modes changes the state of its caller, which STND.CONC.17 asks a library to leave unchanged and the third sentence of HW.CPU.3 asks restored before control returns to code that the hardware contract does not cover. HW.CPU.3 confirms the state in each thread or pool that computes, and STND.OMP.30 and STND.OFFLD.14 keep code from relying on a floating-point environment outside the host code or region that sets it, so a mode set at the start of the main program says nothing of a target region, and the run of STND.FTN.36 is a run on the host. An intrinsic procedure leaves the flags of overflow, division by zero, and invalid operation as they were on entry (S1 17.5), and the procedures that save and restore the floating-point status are the Fortran means of HW.CPU.3; whether a processor restores the halting and rounding modes at the return from a procedure of the work is unverified. A program that neither halts at these exceptions nor reads their flags continues past an invalid operation without a trace, which is why HW.5 has the hardware contract state the handling of non-finite values. The support of the IEEE modules is a property of the processor and the kind, which the IEEE_SUPPORT inquiry functions report (STND.FTN.16). Halting is among the facilities that a processor is free not to support, so STND.FTN.36 asks its run where the compiler and the host of the work support halting at these exceptions, and a work without that support is not blocked. The relations <, <=, >, and >= signal on a NaN, and == and /= are quiet (S1 C.1, 17.11), so under halting at invalid operation an ordered comparison of a NaN halts the program; a quiet comparison lets a NaN reach a branch without a trace, which is why the second sentence of STND.FTN.17 reaches only the comparisons that code is designed to make on a NaN (STND.FTN.17). A test of x /= x for a NaN is one that an option assuming finite values is able to remove, a hazard that is unverified for Fortran compilers. STND.CODE.21 keeps code that holds a required check of such a value from an option that, by the documentation of its compiler, lets the compiler assume finite values, in every language, Fortran included, at the cost of one choice of option for a file that holds such a check.

Parallel execution. The constraints of DO CONCURRENT forbid RETURN, image control statements, branches out of the construct, references to impure procedures, and the procedures that change floating-point modes and flags, and a processor diagnoses them; the locality of a variable is LOCAL, LOCAL_INIT, REDUCE, SHARED, or unspecified; a LOCAL variable is undefined at the start of each iteration; REDUCE combines "in any order"; a variable of unspecified locality that more than one iteration defines is undefined after the construct; and a SHARED variable that one iteration defines and another references breaks the rules without a diagnosis (S1 11.1.7.5). The construct does not promise parallel execution, so STND.CONC.11 keeps its iterations from waiting on one another. DEFAULT(NONE) makes each omission of a locality a constraint that the compiler checks (STND.FTN.19); locality specifiers came with a recent revision and REDUCE with the revision after it (S1 C.1, S2), and a variable declared in a BLOCK construct inside the body is local to its iteration (unverified). STND.CONC.21 and STND.CONC.22 govern a result that depends on the order in which REDUCE combines values or on the number of threads that a compiler uses, and STND.CONC.24 the tests at several numbers of threads where an option runs the iterations in parallel. Images are concurrent tasks: image control statements, events, and atomic subroutines are the synchronization that STND.CONC.3 asks for coarrays; ERROR STOP ends every image (S1 11.4), which STND.CONC.2 asks of a halt; and a failed image, in the revisions that define it, changes the control flow of the other images (S1), and a status that reports it is answered under STND.FTN.30. Under OpenMP, STND.OMP.5, STND.OMP.6, and STND.OMP.7 govern data-sharing, and the Notes of STND.OMP already state that procedures with saved or initialized locals share them; STND.FTN.11 states the same for every model. Members of a common block named in a clause other than shared "no longer have a Fortran storage association with the common block" (S3) (STND.FTN.20); how a threadprivate directive names a common block is not settled by the sources and is unverified.

MPI. STND.MPI says nothing of Fortran, and the MPI standard states that its Fortran bindings are "a property of an MPI library together with the Fortran compiler suite" (S4 20.1.7). A compiler assumes that a local variable does not change across a call that does not receive it, so it is able to keep a buffer in a register across the wait and to "schedule the load of buf earlier than typed in the source" (S4 20.1.17.1); the ASYNCHRONOUS attribute, in a BLOCK construct or a procedure of limited scope as the example of S1 C.13 shows, or the routine that synchronizes registers after the wait, prevents it, and the MPI implementation reports through a constant whether its binding protects such buffers (STND.FTN.22). Where the implementation reports that it does not support array sections, "the use of Fortran arrays with subscript triplets as actual choice buffer arguments in any nonblocking MPI operation ... may cause undefined behavior" (S4 20.1.12), because the copy that the compiler makes is released at the return of the call, before the operation completes. STND.MPI.16 asks the buffer of a pending operation to stay allocated and unwritten until its completion, which such a copy does not do, and STND.FTN.23 keeps the copy from arising; whether the same holds for one-sided and split collective operations is unverified. The module mpi_f08 is the only binding that, by the MPI standard, the Fortran standard fully supports, and the include file mpif.h gives implicit interfaces with no checking of arguments and is deprecated by a recent revision (S4 20.1.5, 20.1.10); STND.MPI.1 keeps a deprecated facility out, STND.FTN.4 keeps out a binding with implicit interfaces, and STND.FTN.21 asks for the binding that the Fortran standard fully supports. The MPI datatypes for Fortran data are defined by kind, through the precision and range of SELECTED_REAL_KIND, and match only for equal precision and range (S4 20.1.9), which STND.FTN.24 adds to the type signatures of STND.MPI.14.

Input and output. A unit number is a nonnegative integer that the program chooses, and numbers chosen by hand in two components collide; a library that connects a unit by a fixed number shares that number with its caller, the hidden coupling of DSGN.14. The NEWUNIT= specifier of later revisions lets the compiler choose the number, and ISO_FORTRAN_ENV names the preconnected units INPUT_UNIT, OUTPUT_UNIT, and ERROR_UNIT; input from the unit of an asterisk is preconnected on image 1 alone (S1 12.5.5, 12.6.4.3) (STND.FTN.25). The order of the records that different iterations of DO CONCURRENT write to one sequential file is processor dependent (S1 11.1.7.5, Annex A), and the records of different images are not ordered by the language (S1 12.5, 16.10.2) (STND.FTN.26); output gathered from the parallel parts and written by one image in a fixed order is one remedy. STND.FTN.26 is the Fortran form of STND.CONC.30: the constraints of DO CONCURRENT forbid image control statements and references to impure procedures, so no protocol of its iterations orders their records, while image control statements are able to order the writes of images, which the second sentence of STND.FTN.26 admits.

Interoperability with C. BIND(C), the kinds of ISO_C_BINDING, C_PTR, and the C descriptor define the boundary; later revisions let an interoperable procedure take allocatable, pointer, optional, assumed-shape, and assumed-rank dummies (S1 18, C.1). The extents and strides in a C descriptor have the C type ptrdiff_t and not default integer, the layout of the descriptor is fixed only through its functions, and a LOGICAL of default kind is not interoperable (S1 18) (STND.FTN.27). A test with an array section of a stride other than one exercises the descriptor where errors of stride hide (STND.FTN.28). STND.FTN.27 and STND.FTN.28 give the Fortran forms of STND.CODE.22 and STND.CODE.23.

Failures. Fortran has no exceptions, so the responses that PRIME.4 admits are a halt with a diagnosis, the designed safe state, a visible degradation, and the return of the condition, which a subroutine makes in a status argument because it has no result (STND.CODE.14, whose pass of the condition to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of the language that propagates it takes in Fortran the result of a function and the status argument). Without a STAT=, IOSTAT=, or CMDSTAT= specifier, an error of an ALLOCATE, an input or output statement, or a command ends the program by error termination, a halt whose diagnosis is the processor's (unverified); with the specifier, the program receives the condition (STND.FTN.30), and the ERRMSG= and IOMSG= specifiers give the text of a diagnosis. A failed allocation is resource exhaustion, and an input record that does not match its format is invalid input; an end of file that the code expects is not a condition that PRIME.4 lists, and STND.CODE.12 governs a status that code discards for another reason. Checks of subscripts against bounds are a facility of the compiler, set by an execution setting, and the Fortran standard requires no processor to diagnose an out-of-range subscript, so the check of STND.CODE.6 for an untrusted subscript is a test in the code (STND.FTN.31). It is made where the untrusted input enters, or, for a bound that is not known there, at the first point at which the bound is known. An assumed-size dummy has no extent in its last dimension, so its test is against the extent that the caller passes; where an interface that a library fixes passes none, a procedure of the work that takes the extent and calls the library is one remedy. STND.CODE defines the term Untrusted input once for every language, and the Terms of this standard place in the public interface that the term takes in each procedure that a module makes public, an entity of a module being public unless the module makes it private, and each procedure with the BIND attribute, as STND.PY and STND.JL place the functions of their public interfaces. The custodian's ruling of 2026-10-23 that this reach raises no floor was made for STND.PY and STND.JL, and the ratification of 2026-10-24 extended the reach to this standard. An external procedure that the documentation or the repository configuration names for use by code outside the work is in the interface for outside use of STND.CODE, and the paragraph on the floor argues that reach; an external procedure that nothing names is not, which keeps out the external procedures that in legacy code are the internal structure of a program. ERROR STOP initiates error termination of every image (S1 11.4), where STOP initiates normal termination, so a halt on a failure by ERROR STOP keeps a workflow from reading it as a normal end (STND.FTN.32); the exit status that a compiler reports for each is unverified. ERROR STOP ends the images of one Fortran program, and each process of an MPI execution is a program of its own, so ERROR STOP alone meets STND.MPI.6 only where the hardware contract of STND.MPI.7 states that the end of one process ends the others (unverified for each MPI implementation). Whether ERROR STOP is permitted in a pure procedure depends on the revision (unverified), and the return of the condition under STND.CODE.14 remains open there.

Legacy source and modernization. A conversion of source form, IMPLICIT NONE with each name declared, a computed GO TO replaced by SELECT CASE, and a labeled DO replaced by END DO change no result by the semantics of the language; the steps that are able to change one are the rows of STND.FTN.34. That an intrinsic reduction, SUM among them, combines in an order of the processor's choice is unverified. Columns of fixed-form source past the last significant position are ignored, so a conversion to free form that keeps them makes them part of the statement (inference from the significance of position 72, unverified). The legacy list follows the list of exempted modules of STND.PY.6: existing source enters it at the change that adopts this standard, a change of a compiler or of the revision in force, or a revision of this standard that adds a provision the list names, and otherwise the list only shrinks. The provisions that it names are those that a check or a reviewer decides from the text of one file; the others concern the behavior of code at a call or a run, which no entry for a file states. One reason serves a class of forms, so an entry for a file in fixed form that uses COMMON throughout states its reason once for each. An entry names one file, or a directory or a pattern of names whose files share its forms and reasons, so that a legacy code of thousands of files in one form needs one entry; an entry widened to further files is an entry added, which STND.FTN.33 admits only on the occasions that it names. An entry for external code that the work incorporates is able to cite as its reason the record of STND.DEPS.11, which keeps that code apart. A file that the list holds for STND.FTN.13 or STND.FTN.14 takes its working precision from the default kinds that the options of STND.FTN.2 set, which is where the record of NUMER.5 reads it.

Checks. A processor is able to report the obsolescent forms, the forms that the numbered syntax rules and constraints do not permit, an unsupported kind, inconsistent use of names, and a nonstandard intrinsic procedure or module (S1 4.2), so the numbered constraints are checkable during compilation (STND.FTN.1, STND.FTN.4). The rules that the Fortran standard states without a constraint are not: overlap of arguments, use of an undefined value, a subscript out of range, a shape that sequence association mismatches, an integer out of range, and unsynchronized access. They are checked by the runs of STND.FTN.35 and STND.FTN.36, by STND.CONC.25 for data races, and by review. A check that the Fortran standard does not require is able to be absent from a compiler, which is why STND.FTN.35 has conditions; each such build is a checking build of STND.BUILD.13, and the fixed value of its second sentence keeps the verdict of a test the same on each run, as STND.CODE.9 asks. This standard has no counterpart of STND.CXX.27, or of the default of STND.JL that keeps the checking of bounds in the configuration that reports results: Fortran defines no checked mode of the language or of its intrinsic procedures, a check of subscripts against bounds is a facility of a compiler that the Fortran standard does not require, so STND.FTN.31 keeps the check of each untrusted subscript in the code, where no execution setting removes it, and STND.FTN.35 runs the checks that a compiler provides in the tests.

Names. The research note retrieved no convention of names that the Fortran standard fixes, and that none exists is unverified, so STND.CODE.28 leaves the convention of Fortran source to the repository configuration and keeps the names that the notation of NUMER.4 fixes, and this standard adds no table.

Binding provisions. STND.FTN.30 and STND.FTN.31 instantiate PRIME.4 and bind at every class, CSQ4 included. The argument that neither raises the floor (GOV.11) is this. STND.CODE.14 admits in Fortran the result of a function and the status argument, an argument that the caller passes to receive the condition, and admits no other pass to the caller. STND.FTN.30 asks the response that PRIME.4 already requires to a listed condition that a status reports, which STND.CODE.7 keeps from being discarded, at the cost of one test of the status. STND.FTN.31 asks the check of STND.CODE.6 in the one form that no execution setting removes in Fortran, at the cost of one test for each untrusted subscript; the term Untrusted input reaches the values that a procedure made public by a module receives, the reach that STND.PY and STND.JL give the arguments of their public interfaces, because such a procedure is called by code that the module does not see and that the threat model does not record as trusted; the custodian's ruling of 2026-10-23 on that reach was made for STND.PY and STND.JL, and the ratification of 2026-10-24 extended it to this standard on this argument. The same argument holds for an external procedure that the documentation or the repository configuration names for use by code outside the work, which the term of STND.CODE adds to that reach: code that the work does not see calls it, and STND.FTN.31 asks, for a subscript that such a procedure receives, the check that DSGN.2 already asks where untrusted input enters, in the form that no execution setting removes, at the cost of one test for each such subscript; an external procedure that nothing names for such use stays outside the reach. Without them, a failed allocation or read under a status specifier, or a subscript from untrusted input, passes silently.

Class onset. Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, REPRO, VV, INTPR, or a provision of NUMER or HW, and applies from the class that its field `onset` gives, which work of CSQ4 may omit, the rules of the form of code at an interface among them at CSQ3; its part that rests on NUMER or HW applies only to work that those profiles bind, and the floating-point settings and tests of STND.FTN.16 and STND.FTN.17 apply from CSQ3 through the provisions of LVL0 that they also instantiate, a tightening above the floor (PRIME.15) for work that HW binds, since each asks a statement, a setting, a check, or a test that needs no hardware contract. No default raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.JL | Julia standard |
| STND.MPI | Message Passing Interface standard |
| STND.OFFLD | Accelerator offload standard |
| STND.OMP | OpenMP standard |
| STND.PY | Python standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Revision and options

#### STND.FTN.1 Revision in force

Default, from CSQ3. Instantiates REPRO.2, SIMPL.6, DSGN.3.

The repository configuration SHOULD state the revision in force of each source file of Fortran, with each option by which each compiler of the work is set to that revision (REPRO.2, SIMPL.6). Each change SHOULD pass a check in which a compiler of the work reports each form of the Fortran source that the numbered syntax rules and constraints of the revision in force do not permit, and each obsolescent form, and that fails on each such form that the legacy list does not hold for its file (DSGN.3).

#### STND.FTN.2 Fortran compiler options

Default, from CSQ3. Instantiates SIMPL.6, REPRO.2, REPRO.7.

Among the execution settings that STND.BUILD.11 has it state for each compilation unit of Fortran, the repository configuration SHOULD name each option of the compiler that changes a default kind, or that gives local variables static storage or an initial value (SIMPL.6, REPRO.2). Where Fortran source uses an extension, the repository configuration SHOULD state each compiler of the work that accepts that extension and the documentation in which the compiler gives its meaning (SIMPL.6, REPRO.7).

#### STND.FTN.3 Deleted and obsolescent forms

Default, from CSQ3. Instantiates SIMPL.6.

Each statement that a change adds to Fortran source or alters SHOULD use only forms that the revision in force defines (SIMPL.6). Other than the fixed source form of a file that the legacy list holds, and a COMMON statement that gathers the declarations of an existing common block into the one source text of STND.FTN.12, each statement that a change adds to Fortran source or alters SHOULD NOT use an obsolescent form (SIMPL.6).

### Interfaces and arguments

#### STND.FTN.4 Explicit interfaces

Default, from CSQ3. Instantiates DSGN.1, DSGN.3.

Where the revision in force provides explicit interfaces, each procedure that Fortran source of the work references SHOULD have an explicit interface at each reference, from a module, by host association, or from an interface body (DSGN.1, DSGN.3). Where the means of the work include a static check that reports each reference to a procedure without an explicit interface, or one that compares each interface body of a procedure that the work defines outside a module with the definition of that procedure, each change SHOULD pass each such check (DSGN.3).

#### STND.FTN.5 Implicit typing and argument intent

Default, from CSQ3. Instantiates SIMPL.6, DSGN.3, DSGN.1.

Where the revision in force provides the IMPLICIT NONE statement, each program unit and each interface body of Fortran source SHOULD contain it (SIMPL.6, DSGN.3). Where the revision in force provides the INTENT attribute, each dummy data object of a procedure that the work defines in Fortran SHOULD have the INTENT attribute or the VALUE attribute (DSGN.1).

#### STND.FTN.6 Assumed-size dummy arrays

Default, from CSQ3. Instantiates DSGN.4.

Other than in an interface that a library outside the work or a procedure with the BIND attribute fixes, a dummy argument SHOULD NOT be an assumed-size array (DSGN.4).

#### STND.FTN.7 Argument aliasing

Default, from CSQ3. Instantiates DSGN.1.

While an entity is associated with a dummy argument that has neither the POINTER attribute nor the TARGET attribute, code SHOULD change the value or the allocation status of that entity, or of a part of it, only through that dummy argument (DSGN.1).

#### STND.FTN.8 Pointers to dummy arguments

Default, from CSQ3. Instantiates DSGN.14.

A pointer that a procedure associates with a dummy argument without the POINTER attribute, or with a part of one, SHOULD NOT be referenced after that procedure returns (DSGN.14). A C address that a procedure obtains for a dummy argument without the POINTER attribute, or for a part of one, SHOULD NOT be used after that procedure returns (DSGN.14).

### Values and storage

#### STND.FTN.9 Values defined before reference

Default, from CSQ3. Instantiates DSGN.1, SIMPL.6.

Code SHOULD NOT reference the value of a variable at a point at which the Fortran standard leaves that variable undefined (DSGN.1). Code SHOULD NOT rely on an initial value that an option of a compiler gives a variable (SIMPL.6).

#### STND.FTN.10 Explicit SAVE of initialized locals

Default, from CSQ3. Instantiates SIMPL.6, DSGN.14.

Other than a variable that only the default initialization of a component of its type initializes, each local variable of a procedure that its declaration or a DATA statement initializes SHOULD have the SAVE attribute stated in its declaration or in a SAVE statement of that procedure (SIMPL.6). Where a procedure relies on a value of a local variable at each entry to it, the procedure SHOULD assign that value in its executable part (DSGN.14).

#### STND.FTN.11 Saved state in concurrent calls

Default, from CSQ3. Instantiates DSGN.15, DSGN.14.

Where more than one concurrent task is able to execute a procedure at once, the procedure SHOULD define a variable with the SAVE attribute, a module variable, or a variable in a common block only under the protection that STND.CONC.3 states for that variable (DSGN.15, DSGN.14).

#### STND.FTN.12 Common block declarations

Default, from CSQ3. Instantiates DSGN.4, DSGN.14.

Each common block SHOULD be declared, with the same members in the same order and of the same types, kinds, and shapes, by one source text that each scoping unit that declares the block includes (DSGN.4). In each scoping unit other than a main program or a module, each common block that the scoping unit declares SHOULD have the SAVE attribute (DSGN.14).

### Kinds and floating point

#### STND.FTN.13 Named kind parameters

Default, from CSQ3. Instantiates SIMPL.6, NUMER.5, REPRO.2.

Where the revision in force provides kind type parameters, each declaration of a real or a complex entity in Fortran source SHOULD give its kind by a named constant (SIMPL.6, NUMER.5). Each such named constant SHOULD take its value, in one module of the work, from an intrinsic function that selects a kind by its precision and range or from a named constant of an intrinsic module (REPRO.2, NUMER.5).

#### STND.FTN.14 Kinds in literals and operations

Default, from CSQ3. Instantiates SIMPL.6, NUMER.5.

Each real literal constant that is assigned to, combined with, or passed to a real or complex entity of a kind other than default real SHOULD be written in the kind of that entity (SIMPL.6, NUMER.5). Where an intrinsic operation combines real or complex operands of different kinds, code SHOULD convert one of them explicitly, by an intrinsic conversion function, to the kind on which the computation relies (SIMPL.6, NUMER.5).

#### STND.FTN.15 Integer range checks

Default, from CSQ3. Instantiates DSGN.2.

Where integer arithmetic on untrusted input is able to exceed the range of its kind, code SHOULD check, before the operation, that its result stays within that range (DSGN.2).

#### STND.FTN.16 Halting modes and IEEE support

Default, from CSQ3. Instantiates SIMPL.6, HW.5.

Each main program SHOULD set at its start, by the procedures of the intrinsic module IEEE_EXCEPTIONS or by an option of its compiler that the repository configuration states, whether it halts at invalid operation, at overflow, and at division by zero (SIMPL.6, HW.5). Where code relies on a facility of an intrinsic IEEE module for a kind, it SHOULD confirm, by the inquiry function of that module for that facility, that the facility is supported for that kind, and respond to a negative answer by a response that STND.CODE.14 lists (SIMPL.6, HW.5).

#### STND.FTN.17 Non-finite tests and comparisons

Default, from CSQ3. Instantiates SIMPL.6, HW.5.

Where the revision in force provides the intrinsic module IEEE_ARITHMETIC, code SHOULD test whether a real value is a NaN or an infinity only by the functions of that module that classify a value (SIMPL.6, HW.5). Where a program halts at invalid operation, each comparison that its code is designed to make on a NaN SHOULD be one that the Fortran standard defines as signaling no exception on a NaN (SIMPL.6).

### Parallel execution

#### STND.FTN.19 DO CONCURRENT locality

Default, from CSQ3. Instantiates SIMPL.6, DSGN.15.

Where the revision in force provides locality specifiers, each DO CONCURRENT construct SHOULD carry the locality specifier DEFAULT(NONE) (SIMPL.6). Each variable that an iteration of a DO CONCURRENT construct defines SHOULD be local to that iteration, have REDUCE locality, or be defined only at elements of an array that no other iteration of the construct references or defines (DSGN.15).

#### STND.FTN.20 Common blocks in OpenMP

Default, from CSQ3. Instantiates DSGN.14.

Where code relies on the storage association among the members of a common block, each data-sharing clause other than shared that names members of that block SHOULD name the whole block in their place (DSGN.14).

### MPI

#### STND.FTN.21 Fortran binding of MPI

Default, from CSQ3. Instantiates DSGN.3, HW.3, REPRO.2.

Where the MPI implementation of the work provides the Fortran binding of MPI that, by the MPI standard, the Fortran standard fully supports, Fortran code SHOULD call MPI through that binding (DSGN.3). Among the items of STND.MPI.2, the record of each result that Fortran code computes with MPI SHOULD give the Fortran binding of MPI that the code uses, and whether the MPI implementation reports for that binding that it protects the buffers of nonblocking operations and that it supports array sections as buffers (HW.3, REPRO.2).

#### STND.FTN.22 Asynchronous MPI buffers

Default, from CSQ3. Instantiates DSGN.14.

Where the revision in force provides the ASYNCHRONOUS attribute, each variable that is the buffer of a pending nonblocking operation of MPI SHOULD have that attribute in each scoping unit that references it between the start and the completion of that operation (DSGN.14). Where the MPI implementation reports that its Fortran binding does not protect the buffers of nonblocking operations, code SHOULD call, after each completion call and before it accesses the buffer, the routine that the MPI standard gives for the synchronization of registers, with that buffer as its argument (DSGN.14).

#### STND.FTN.23 Array sections in nonblocking operations

Default, from CSQ3. Instantiates DSGN.14.

Where the MPI implementation reports that its Fortran binding does not support array sections as buffers, code SHOULD NOT pass an array section with a subscript triplet as the buffer of a nonblocking operation of MPI (DSGN.14).

#### STND.FTN.24 MPI datatypes of Fortran kinds

Default, from CSQ3. Instantiates DSGN.4.

Each MPI datatype that describes Fortran data of an intrinsic type SHOULD be the datatype that the MPI standard gives for the type and the kind type parameter that declare that data (DSGN.4).

### Input and output

#### STND.FTN.25 Unit numbers of connections

Default, from CSQ3. Instantiates DSGN.14, SIMPL.6.

Each unit that Fortran code connects by an OPEN statement SHOULD take its number from the NEWUNIT= specifier, or from one place in the work that assigns each unit number of the work once (DSGN.14). Code SHOULD refer to a preconnected unit by an asterisk or by a named constant of the intrinsic module ISO_FORTRAN_ENV, and not by a literal number (SIMPL.6).

#### STND.FTN.26 Order of parallel output records

Default, from CSQ3. Instantiates REPRO.3.

Code SHOULD NOT rely on the order of the records that different iterations of one DO CONCURRENT construct write to one file (REPRO.3, STND.CONC.30). Other than an order that a protocol of the images fixes, code SHOULD NOT rely on the order of the records that different images write to one file (REPRO.3, STND.CONC.30).

### Interoperability with C

#### STND.FTN.27 C interoperable interfaces

Default, from CSQ3. Instantiates DSGN.3, DSGN.1, DSGN.4.

Where the revision in force provides the BIND attribute, each procedure through which Fortran code and C code call one another SHOULD have that attribute, with its Fortran interface declared once, in one module of the work (DSGN.3, DSGN.1). Each dummy argument of such a procedure SHOULD have the type, and the kind that the intrinsic module ISO_C_BINDING names, that interoperate with the type that the C declaration of the procedure gives the corresponding parameter (DSGN.4).

#### STND.FTN.28 Descriptors across the C boundary

Default, from CSQ3. Instantiates VV.1.

Where a procedure with the BIND attribute passes an array by a C descriptor, its tests SHOULD pass across that procedure an array section with a stride other than one (VV.1).

### Failures

#### STND.FTN.30 Status specifiers answered

Binding. Instantiates PRIME.4.

Where a STAT=, IOSTAT=, or CMDSTAT= specifier, or the status argument of an intrinsic procedure, receives a value that reports a condition that PRIME.4 lists, code SHALL respond to that condition as STND.CODE.14 requires before it relies on the outcome of that statement or call (PRIME.4).

#### STND.FTN.31 Unremovable Fortran input checks

Binding. Instantiates PRIME.4, DSGN.2.

Where untrusted input supplies a subscript, the check that rejects an invalid value of it SHALL be a test in the code that no execution setting removes, made against the bounds of the array or the extent that the caller passes for an assumed-size dummy array, at the entry of the untrusted input or at the first point after it at which that bound is known (PRIME.4, DSGN.2, STND.CODE.6).

#### STND.FTN.32 Halts by ERROR STOP

Default, from CSQ3. Instantiates SIMPL.6.

Where the revision in force provides the ERROR STOP statement, each halt of Fortran code on a failure, other than one by the abort facility of MPI under STND.MPI.6, SHOULD be made by an ERROR STOP statement whose stop code or message states the diagnosis (SIMPL.6).

### Legacy source

#### STND.FTN.33 Legacy source list

Default, from CSQ3. Instantiates REPRO.7, DSGN.3.

Where a source file of Fortran uses a form that the check of STND.FTN.1 reports, or does not meet STND.FTN.4, STND.FTN.5, STND.FTN.6, STND.FTN.10, STND.FTN.12, STND.FTN.13, STND.FTN.14, or STND.FTN.25, the repository configuration SHOULD hold, in the legacy list, an entry that names that file, or a directory or a pattern of names whose files share its forms and reasons, with those forms and provisions and a reason for each provision and for each class of forms (REPRO.7). Other than an entry that the change that adopts this standard, a change of a compiler or of the revision in force, a revision of this standard, or a change that incorporates external code into the work makes necessary, a change SHOULD NOT add an entry to the legacy list (DSGN.3).

#### STND.FTN.34 Modernizing changes

Default, from CSQ3. Instantiates VV.3, VV.8, REPRO.7.

Each modernizing change SHOULD be verified by running the tests that carry the evidence of the code that it touches before and after the change, and by judging their results by a comparison, with its tier of STND.VVUQ.1 and its tolerance, that a record states before the change (VV.3, VV.8). Where a change makes a replacement that the table of this provision lists, that replacement SHOULD be made in a change of its own, whose record states the results that the replacement is able to change and the acceptance criterion that judges them (REPRO.7, VV.3).

| Replacement | What it is able to change |
| --- | --- |
| A kind parameter added to a real literal constant, or a real entity of default kind given another kind | The value of the constant, and the precision of the arithmetic that uses it |
| A change of a compiler option that sets a default kind | The kind of each entity declared without one, and so each result that uses it |
| An initialization that implies the SAVE attribute replaced by an assignment at entry, or the SAVE attribute removed | The value that a local variable holds at entry to a later call |
| An explicit-shape or assumed-size dummy array made assumed-shape | Whether the procedure receives the storage of its actual argument or a copy of it |
| A common block or an EQUIVALENCE statement replaced by module variables, by a derived type, or by the TRANSFER intrinsic function | The value that one name holds after a definition through another name that storage association overlaid |
| A loop replaced by an array expression, an intrinsic reduction, or a DO CONCURRENT construct | The order of floating-point operations |
| A loop moved to threads or to images | The order of floating-point operations, and the floating-point control state under which its operations run (HW.CPU.3) |
| An extension, a deleted form among them, replaced by a form that the revision in force defines | The behavior that a compiler gave the extension, the number of iterations of a loop with a real DO variable among them |
| An explicit interface given to a procedure that a reference called with an actual argument that disagreed with its dummy argument | The values that the procedure receives from that reference |

### Checking

#### STND.FTN.35 Run-time Fortran checks

Default, from CSQ3. Instantiates DSGN.3.

Where a compiler of the work provides a build that checks at run time each subscript against its bounds, and each reference to a pointer or an allocatable variable against its association or allocation status, the tests of each change SHOULD run in that build and fail at the first detection (DSGN.3). Where a compiler of the work provides a build that reports each reference to an undefined value, or one that gives each variable without a defined initial value one fixed value that shows in results, the tests SHOULD also run in that build (DSGN.3).

#### STND.FTN.36 Floating-point exceptions under test

Default, from CSQ3. Instantiates DSGN.3.

Where the compiler and the host of the work support halting at an invalid operation, an overflow, and a division by zero, the tests of code that does not rely on continuing past them SHOULD include a run on the host that halts at the first of them and reports the point at which it halted (DSGN.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.1 | 2026-10-25 | Minor amendment (GOV.41): STND.FTN.18 is withdrawn, its outcome being the first sentence of STND.CODE.21 for every language, and the front matter lists it as withdrawn; Terms import Untrusted input from STND.CODE, delete this standard's own definition, and place each procedure that a module makes public and each procedure with the BIND attribute in the public interface that the term takes in, so that the reach ratified on 2026-10-24 stays; STND.FTN.29 and STND.FTN.31 cite STND.CODE.14 and STND.CODE.6, of which they are the Fortran forms, with their text otherwise unchanged; STND.FTN.26 cites STND.CONC.30, of which it is the Fortran form, and admits an order of the records of images that a protocol of the images fixes; new STND.FTN.37 (default, from CSQ3) leaves the convention of names to the repository configuration and keeps the names that the notation of NUMER.4 fixes, the rule of decision 9 of 2026-10-24; the Purpose cites STND.CODE for the rules of code that hold for every language and lists STND.FTN.37; the Notes cite STND.CODE.14 in place of STND.CXX.16, which STND.CXX 1.2 withdraws, and STND.CODE.21 in place of STND.FTN.18, give the reason that this standard has no counterpart of STND.CXX.27 and of the default of STND.JL on bounds checking in the configuration that reports results, state the reach of the term on the ratification of 2026-10-24 with the floor argument for an external procedure that the documentation or the repository configuration names, give the reason for the naming rule, and add INTPR to the class onsets. |
| 1.1.1 | 2026-10-27 | Editorial amendment (GOV.41): the Notes cite STND.CODE.22 to STND.CODE.26 for the rules of each foreign interface in place of STND.CXX.20 and STND.CXX.22, which STND.CXX 1.3 withdraws, and name STND.FTN.27 and STND.FTN.28 the Fortran forms of STND.CODE.22 and STND.CODE.23; no obligation, permission, or defined meaning changes. |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): STND.FTN.29 is withdrawn, STND.CODE.14 holding the Fortran responses, the status argument among them, and STND.FTN.37 is withdrawn, its outcome being STND.CODE.28 for every language, and the front matter lists both as withdrawn; STND.FTN.16 and STND.FTN.30 cite STND.CODE.14 in place of STND.FTN.29; the Purpose, the Notes on failures, comparisons, names, and the binding provisions follow; the Notes name the revisions of the Fortran standard by their order in place of their numbers, which ruling D1 takes out of the Notes; References drop STND.LEAN and STND.STDC. |
| 1.3 | 2026-10-28 | Minor amendment (GOV.41): STND.FTN.6, the first sentence of STND.FTN.12, STND.FTN.24, and the second sentence of STND.FTN.27 apply from CSQ3, as rules of the form of code; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.4 | 2026-10-28 | Minor amendment (GOV.41): the second sentence of STND.FTN.4 asks each change to pass a static check of explicit interfaces, or of interface bodies against their definitions, only where the means of the work include it; an entry of the legacy list of STND.FTN.33 names one file, or a directory or a pattern of names whose files share its forms and reasons, and the term Legacy list and the Notes follow. |
