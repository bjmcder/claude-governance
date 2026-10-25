# Message Passing Interface standard (STND.MPI) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 109 (2026-10-24); revised to 1.0.1 in entry 149 (2026-10-25). This reading copy is composed from the per-provision files in STND/MPI/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice that is specific to the use of the Message Passing Interface (MPI), in every language in which the work calls it. It adds to STND.CODE, HW, NUMER, and STND.VVUQ only what MPI makes necessary. It covers the facilities that the work uses, the record of each parallel execution, the thread support level, and the error handlers (STND.MPI.1, STND.MPI.2, STND.MPI.3, and STND.MPI.4); the answer to each error that MPI reports and the end of a parallel execution when one of its processes halts or ends (STND.MPI.5, STND.MPI.6, and STND.MPI.7); the conduct of libraries toward the communicators, error handlers, process-wide state, and handles of their callers (STND.MPI.8, STND.MPI.9, STND.MPI.10, and STND.MPI.11); point-to-point messages, their protocol, buffering, type signatures, nondeterministic matching, and the lifetime of nonblocking operations (STND.MPI.12, STND.MPI.13, STND.MPI.14, STND.MPI.15, and STND.MPI.16); collective operations and their reductions (STND.MPI.17, STND.MPI.18, and STND.MPI.19); one-sided communication (STND.MPI.20); parallel input and output (STND.MPI.21 and STND.MPI.22); threads (STND.MPI.23); and tests (STND.MPI.24 and STND.MPI.25).

STND.MPI.5 and STND.MPI.6 instantiate PRIME.4 and HW.8, so they are binding and apply at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is platform, implementation, and tool agnostic: it names no MPI implementation, launcher, checker, platform, or revision of the MPI standard, and refers to the MPI standard at the revision that the work's implementation documents (GOV.18). Transfers of accelerator memory through MPI are governed by HW.GPU and the boundary contracts of HW; rules for directive-based threading and device offload belong to their own standards; and the C++ rules for the interface to MPI are in STND.CXX.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Execution setting has the meaning that STND.CODE gives it. Communicator, group, datatype, type signature, request, window, file, session, error handler, collective operation, standard-mode send, synchronous send, matched probe, conflicting access, and thread support level have the meanings that the MPI standard gives them.

| Term | Definition |
| --- | --- |
| MPI standard | The Message Passing Interface standard, at the revision that the MPI implementation of the work documents as the one it implements; where the work admits more than one MPI implementation, the earliest of the revisions that they document. |
| MPI implementation | A library that provides the interface of the MPI standard to the processes of the work, together with the launcher that starts those processes. |
| Process | A process of the operating system that calls MPI, as the MPI standard uses the word. |
| Parallel execution | The processes that one start of a program that uses MPI creates, with each process that they create or connect to through MPI during the run. |
| Program | The component of the work that holds the entry point of the processes of a parallel execution. |
| Library | A component of the work that another component calls through its interface and that does not hold the entry point of a process. |
| Message protocol | Of a component: the point-to-point, collective, and one-sided operations by which its processes exchange data, with the order in which each process issues them. |
| MPI handle | A handle by which code refers to a communicator, group, datatype, reduction operation, request, window, file, info object, error handler, or session. |
| Predefined handle | An MPI handle that the MPI implementation provides without a call of the work that creates its object, a null handle included. |

## Notes

The custodian's directions of 2026-10-23 set the scope: point-to-point messages, collective operations, one-sided communication, parallel input and output, error handling, the conduct of libraries, tests, and the thread support level of codes that combine MPI with threads. They keep transfers of accelerator memory under HW.GPU, leave directive-based threading and accelerator rules to their own standards, and keep the C++ interface rules in STND.CXX. They ask that results which depend on the number of processes or on the order of reduction be declared and compared within a stated tolerance, and that bitwise identity across process counts, where a project makes it an acceptance criterion, be met by a fixed or order-independent combination. They make the standard platform, implementation, and tool agnostic, so the provisions state outcomes, and the term MPI standard refers to the revision that the work's implementation documents. The source is the project's research note claude/research/parallel-models.md (sections 2.1, 3.1, 3.4, 3.5, 5, and 6.3), which rests on the report of the MPI standard; a fact that the note does not support is marked unverified.

The standard adds MPI content to provisions that already hold the outcome, and does not restate them (GOV.31). HW.3 asks for the record of each execution path, HW.4 for its hardware contract, HW.8 for the response to a fault, a lost message among them, HW.11 for the verification of a protocol for shared state, and HW.12 for the declaration of run-to-run variation. Where an implementation chooses at run time among algorithms that differ in delivered arithmetic, HW.5 asks for the range of that arithmetic, which is the basis for the size of the variation that STND.MPI.18 declares. HW.CPU.3 governs the floating-point control state of each thread, and HW.CPU.4 and HW.CPU.5 govern the thread counts and oversubscription of codes that run threads in each process. STND.CODE.7 forbids discarding a failure that PRIME.4 lists, and STND.CODE.2 brings inputs through interfaces. STND.VVUQ.1 gives the tier of each comparison and STND.VVUQ.2 the rule for reductions under bitwise identity, with tolerances on a basis that NUMER.11 gives. In C++, an MPI handle is held by a resource handle under STND.CXX.5 and STND.CXX.20, a failed free is reported under STND.CXX.21, and a C++ exception does not leave a user-defined reduction operation, an error handler function, or another callback that MPI invokes (STND.CXX.22). A buffer in accelerator memory that MPI reads or writes is at a boundary between execution paths (HW.13), and the completion of the offloaded work that fills it is governed by HW.GPU.3. A parallel execution whose processes run on more than one hardware model crosses a boundary of HW.13 at each message between them, and the conversion of datatypes that MPI performs is able to enter that boundary contract through the permission of the second sentence of HW.13. As this standard's own reading of those defaults, the run of HW.CPU.4 and HW.CPU.5 is taken as all the processes of a parallel execution on one node, whose threads share its processors.

The term MPI standard takes the revision that the implementation documents, because that is the revision whose behavior the implementation provides and the work relies on (STND.MPI.1). Where the work admits more than one implementation, the earliest documented revision is the one that all of them provide; the report of the latest revision states that each valid program of the revision before it remains valid. A facility that the MPI standard marks as deprecated is able to be removed in a later revision, so STND.MPI.1 keeps it out, and an extension of one implementation is recorded with the behavior of the work where it is absent. The record of STND.MPI.2 holds the library loaded at run time because a program built against one binary interface of MPI is able to load another implementation of it, and holds the placement of processes and the execution settings of the implementation because an implementation chooses at run time among algorithms for a collective operation by message size, process count, and settings, and the choice changes the order of reduction (parallel-models.md, section 3.4). STND.MPI.3 asks for the thread support level that the program needs and a comparison with the level provided, because thread support is optional for an implementation and a program that runs threads above the level provided has behavior that the MPI standard does not define; once the comparison detects a shortfall, the response is that of PRIME.4, which STND.CODE.7 keeps from being discarded. The text on sessions in the MPI standard advises against requesting the single-threaded level. STND.MPI.4 states the error handlers because the defaults differ by kind of object: errors on a communicator are fatal unless the program changes the handler, errors that belong to no object are raised on the communicator of the process itself in later revisions (unverified), and files opened through MPI return their errors to the caller by default (unverified in the research note), so an error of parallel input and output passes unseen unless the code checks it.

STND.MPI.5, STND.MPI.6, STND.MPI.7, and STND.MPI.16 close the gaps G1 and G2 of the research note. An error of a nonblocking or persistent operation is reported at its completion, so a request that is never completed loses the error. The MPI standard permits freeing an active send request (unverified), which loses its errors in the same way; with a handler that returns errors, STND.MPI.5 has each such operation completed, so that STND.CODE.7 applies to its error. The MPI standard does not describe the state of the program after an error, so code that receives one does not go on communicating as if none occurred. A process that halts alone leaves the others blocked in a receive or a collective operation that it never joins, which is a silent hang: HW.8 asks the execution path to halt, and this standard reads the path of a parallel execution as all its processes. STND.MPI.6 leaves each other process the responses that PRIME.4 admits: it halts, ended by the abort facility or by its own halt, or it learns of the halt, among other routes through MPI, its own message protocol, a signal from the launcher, or a supervising process, and degrades visibly or enters a designed safe state, as a coordinating process that reassigns the work of a halted worker does. The abort facility of MPI on a communicator that spans the execution is meant to end them; the abort handler of the MPI standard bound to a session ends only the local process (parallel-models.md, section 3.1), so a program built on sessions ends the others by another means. Output that a process has written but not flushed when the execution is aborted is able to be lost (unverified), which is why STND.MPI.6 has the write of the diagnosis completed first. That the diagnosis persists after the execution is the diagnostics of INTPR.8, and STND.MPI.7 asks for it as a default. The MPI standard does not require the error handler that makes errors fatal to write a diagnosis, and its abort is a best attempt (unverified), so STND.MPI.7 has the hardware contract state whether that handler writes one. A process that crashes does not reach that code. Launchers commonly end every process when one ends without finalizing MPI, but the MPI standard does not promise it (unverified), so STND.MPI.7 has the hardware contract state the behavior of the implementation and launcher, and a run without that assurance carries a limit on its duration or on the time a process waits without progress.

STND.MPI.5 and STND.MPI.6 instantiate PRIME.4 and HW.8 and so bind at every class, CSQ4 included. Neither raises the floor (GOV.11), as the custodian ruled at ratification (PRIN.10), for these reasons. STND.MPI.5 asks that each error that MPI reports be answered, before a result relies on it, by a response that PRIME.4 lists, which PRIME.4 already requires. Its first sentence costs nothing where the fatal handler writes a diagnosis, and otherwise one error handler that writes one and ends the execution. Its second sentence applies only where the work chose a handler that returns errors, and costs a completion call where code would otherwise free an active request or leave it incomplete. STND.MPI.6 asks that a halt not leave the other processes blocked, which is the silent continuation that PRIME.4 forbids, and leaves each of them every response that PRIME.4 admits. It costs one call of the abort facility, or of the means used in its place, and the completion of one write of the diagnosis to a place that the operator reads, which the actionable diagnosis of PRIME.4 already asks. The persistence of the diagnosis would raise the floor at CSQ4, and is a default (STND.MPI.7). Without these two provisions, the failure of one process passes as a hang and the error of a nonblocking operation is never seen.

The provisions on libraries close gap G4. They follow the published community policies for libraries of scientific software that the research note found (parallel-models.md, section 4): a library takes its communicator from its caller, leaves the caller's error handling unchanged, has no hardwired abort, and frees the communicators and datatypes it creates. A library that names the predefined communicator of all processes is unable to run on part of them, and one that sends point-to-point messages on the communicator it receives shares the tags of its caller, which a derived communicator keeps apart (STND.MPI.8). Collective operations match by order and not by tag, so a library that communicates only by collective operations issued in its caller's order (STND.MPI.17) uses its caller's communicator and saves the collective operation that deriving one costs. A library that changes the error handler of its caller's communicator changes how the caller's own errors are answered (STND.MPI.9), and one that ends the parallel execution takes that decision from the program, which STND.MPI.6 then governs. The initialization and finalization of the world model of MPI, a buffer attached to the process for buffered sends, and the default error handler of files apply to the whole process (STND.MPI.10); later revisions also attach buffers to a communicator or a session (unverified). A session is the means by which a library initializes MPI for itself, so STND.MPI.10 leaves each session to the library that opens it; at a revision without sessions, the world model is the only initialization. Ownership of a handle passes with a return value, a new communicator among them, and the new owner frees it (STND.MPI.11). Freeing a predefined handle is a defect (STND.MPI.11); that the MPI standard calls it erroneous for each kind of handle is unverified.

STND.MPI.12 and STND.MPI.13 close gap G3. A message protocol shares no state, so DSGN.15 and HW.11 do not clearly ask for an argument that it completes; STND.MPI.12 asks for the statement and the argument, and accepts tests under the deadlock check of STND.MPI.25 where no argument is stated. The MPI standard asks a process to progress its communication while it is blocked in MPI and leaves progress during computation open, so an argument that a nonblocking operation or a passive-target access completes while its partner computes rests only on what the MPI standard guarantees (STND.MPI.12). The MPI standard calls a program unsafe when it completes only if the implementation buffers its sends, and lets a standard-mode send be replaced by a synchronous send without changing a correct program, so a run with each send performed as a synchronous send exposes reliance on buffering (STND.MPI.13). Where an implementation has an execution setting that disables buffering, a run under that setting exposes the same reliance. Messages from one sender to one destination do not overtake one another on one communicator, which makes a single-threaded protocol deterministic without wildcard receives; a wildcard source or tag, a completion of one of a set of requests chosen by MPI, a cancellation, and sends from more than one thread make the order of matching vary between runs (STND.MPI.15). A mismatched type signature and a receive buffer shorter than the message are common defects; a truncated message is an error (STND.MPI.14). The buffer of a pending operation is not changed or released, and the buffer of a pending receive is not read, until a completion call reports the operation complete (STND.MPI.16); the research note marks the buffer rule as long-standing practice that it did not confirm in the report.

Every member of a group calls the collective operations on a communicator in the same order; a blocking collective operation does not match a nonblocking one, and nonblocking collective operations match in the order in which they start (STND.MPI.17). Whether a collective operation synchronizes the processes depends on the implementation, and code that works only if a broadcast synchronizes is erroneous. For reductions, the MPI standard only recommends to implementations that the same arguments in the same order give the same result, and results change with the number of processes and with the implementation (parallel-models.md, section 3.4). A reduction operation declared as not commutative is applied in the order of the ranks, but the grouping of its applications is still the implementation's choice (unverified). STND.MPI.18 has each result that depends on these declared, and covers runs that differ only in the items that STND.MPI.2 records, which HW.12 and REPRO.3, written for identical recorded inputs, do not reach. The custodian directs, for every parallel execution model, that strict determinism be an option where it is feasible and not a requirement unless the acceptance criterion of the work or its consequence class demands it; a declared dependence on the number of processes that stays within the agreement that the acceptance criterion fixed is therefore no defect, and STND.VVUQ.82 recommends against a change made only to remove it, while STND.VVUQ.83 forbids an agent to make one on its own initiative. STND.MPI.19 applies STND.VVUQ.2 to reductions across processes: partial results of blocks of the problem that do not depend on the number of processes, combined in a fixed order, or an order-independent combination, give the same bits at every process count. Tier 1 of STND.VVUQ.1 admits no difference of process count, so for a comparison across process counts it points to tier 3. Where the acceptance criterion fixed under VV.3 is bitwise identity across process counts, that criterion governs the comparison, which STND.MPI.19 judges by identical bits, and the tier of STND.VVUQ.1 does not lower it. For a stochastic method, identity across process counts also needs each random stream keyed to one of those blocks, since a stream keyed to a rank changes with the number of processes (DSGN.17). Fixing the implementation, its settings, and the placement of processes, which the record of STND.MPI.2 holds, makes a reduction of the implementation repeatable at one process count only as far as the implementation follows that recommendation.

A window has a memory model, separate or unified, that the implementation reports for it (unverified), and conflicting accesses within one epoch, a load or store by a process to the memory among them, those of other processes on a node through a shared-memory window included (unverified), have outcomes that the MPI standard does not define (STND.MPI.20). Concurrent accumulate operations on one location combine in an order that varies between runs, which STND.MPI.18 declares. Parallel input and output is not atomic by default, and conflicting accesses from different processes are ordered by atomic mode or by a synchronization, a barrier between two synchronizations of the file among them (unverified), which STND.MPI.21 states. A file written in the native representation of one platform is not portable; the MPI standard defines a portable representation (unverified), and STND.MPI.22 asks for it, or a description of the file, for a file that another run, platform, or tool reads. STND.CONC.30 has the order in which concurrent tasks write to one output or one record stated, as an order that a protocol of those tasks fixes or as a variation that the record of that output declares, and the processes of a parallel execution are concurrent tasks under STND.CONC. The MPI standard leaves to the implementation and its launcher whether and how the standard output and standard error of each process reach the operator, and the lines that different processes write arrive there in an order that varies between runs (unverified); one process that writes the output that the others send it, in an order that the message protocol of STND.MPI.12 states, fixes that order. A collective write through the shared file pointer of a file places the data of the processes in the order of their ranks, a noncollective write through it places them in the order in which the processes reach their writes, and a write at an offset that the protocol computes places them where the protocol states (unverified). The first and the last fix the order of the records, and the order that the second gives is a variation that the record of the file declares (STND.CONC.30). Where two accesses conflict, the atomic mode or the synchronization that STND.MPI.21 asks also fixes their order, so one statement of the protocol of the file meets both provisions; records written to disjoint parts of a file are no conflicting accesses, and only STND.CONC.30 reaches their order.

The rules for threads come from the MPI standard: threads order their collective operations on one communicator, two threads waiting on one request is erroneous, and a probe followed by a receive is unsafe where other threads receive on the communicator, which a matched probe avoids (STND.MPI.23). An error handler is able to run on a thread other than the one that made the failing call.

STND.MPI.24 runs each component on at least three numbers of processes, among them one process where the message protocol admits it, so that a defect that appears only in serial or only in parallel is found, and on a number that divides the problem unevenly where the decomposition admits one, which exercises the handling of remainders. A protocol that needs at least two processes starts at the smallest number it admits, with no decision record. The tier of each comparison comes from STND.VVUQ.1, which admits rounding through parallel decomposition at tier 3 for a path without rounding-dependent branches, and STND.MPI.19 replaces it with identical bits where bitwise identity across process counts is the criterion. Run-time correctness checkers for MPI detect mismatched collective operations and type signatures, deadlock, buffers that overlap, and requests and handles left incomplete or unfreed (parallel-models.md, section 3.5); STND.MPI.25 asks for a check that decides those outcomes, and the project chooses the check. A check too costly for each change is deferred under RSRC.12 to the latest point at which its result is still needed.

Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or a provision of HW or NUMER, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row: the contract of STND.MPI.7 and the reliance that STND.MPI.17 limits (DSGN.5), and the type signatures of STND.MPI.14 and the representation of STND.MPI.22 (DSGN.4), from CSQ2; the argument and the tests of the second and third sentences of STND.MPI.12, the run without buffering of STND.MPI.13, and the run-time checks of STND.MPI.25, which verify the invariants of a protocol (DSGN.15), from CSQ2; the limit and report of STND.MPI.7, which report an anomaly to the operator (INTPR.7), and the persistent diagnosis of STND.MPI.7 (INTPR.8), from CSQ1. The statement of a protocol in the first sentence of STND.MPI.12 and in STND.MPI.20, STND.MPI.21, and STND.MPI.23 applies from CSQ3, while the verification of their invariants stays with DSGN.15 and HW.11. Each part that rests on HW applies only to work that HW binds. No default instantiates a prime directive, the Safeguards Article (GUARD), GOV, or a floor obligation, and no default raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| HW.GPU | Accelerators |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Environment

#### STND.MPI.1 MPI facilities used

Default. Instantiates SIMPL.6, REPRO.7.

Each call that the work makes to MPI SHOULD use a facility that the MPI standard defines and does not mark as deprecated (SIMPL.6). Where the work calls an extension of its MPI implementation, a decision record SHOULD state the extension, the reason for its use, and the behavior of the work on an MPI implementation that lacks it (REPRO.7).

#### STND.MPI.2 MPI execution path record

Default. Instantiates HW.3, REPRO.2.

Among the items that HW.3 asks of the record of each result, the record of each result that a parallel execution computes SHOULD give the MPI implementation and its revision, the library of the MPI implementation that the processes load at run time, the number of processes and of nodes, the placement of the processes on the nodes, the thread support level provided, and each execution setting of the MPI implementation that the run sets (HW.3, REPRO.2).

#### STND.MPI.3 Thread support level

Default. Instantiates SIMPL.6, DSGN.1, DSGN.15.

Each program SHOULD request at the initialization of MPI the thread support level that its use of threads requires, and state that level in its contract (SIMPL.6, DSGN.1). Before its first communication, each program SHOULD compare the thread support level that MPI provides with the level that it requested (DSGN.1). The threads of each process SHOULD call MPI only as the thread support level provided permits (DSGN.15).

#### STND.MPI.4 Stated error handlers

Default. Instantiates SIMPL.6, DSGN.1.

Before its first communication, each program SHOULD set the error handler of each predefined communicator that it uses or on which MPI raises errors that belong to no object, and the error handler that files opened through MPI receive by default (SIMPL.6). Each communicator, window, file, and session that the work creates SHOULD carry an error handler that the work sets or that the contract of its creator states it inherits (SIMPL.6, DSGN.1).

### Failures

#### STND.MPI.5 MPI errors answered

Binding. Instantiates PRIME.4, HW.8.

Each error that an MPI operation of the work reports SHALL be answered, before a result that depends on that operation is reported or relied upon, by an error handler that ends each process of the parallel execution with a diagnosis, or by code of the work that responds to it as PRIME.4 and HW.8 require (PRIME.4, HW.8). Where the error handler of a communicator, window, file, or session returns errors to the caller, the work SHALL complete each nonblocking or persistent operation on that object, and each access epoch of a window, by a call that returns its errors, before a result that depends on that operation is reported or relied upon (PRIME.4).

#### STND.MPI.6 Execution-wide halt

Binding. Instantiates PRIME.4, HW.8.

Where a process of a parallel execution halts on a condition that PRIME.4 lists or on a fault that HW.8 governs, each other process of that execution SHALL halt, or receive notice of that halt and respond to it as PRIME.4 requires (PRIME.4, HW.8). A process that ends the other processes of its parallel execution SHALL first complete the write of its diagnosis to a place that the operator reads (PRIME.4).

#### STND.MPI.7 Ended executions observed

Default. Instantiates HW.4, DSGN.5, INTPR.7, INTPR.8.

The hardware contract of each execution path that uses MPI SHOULD state whether, under its MPI implementation, the end of one process of a parallel execution without the finalization of MPI ends the other processes of that execution, and whether the error handler that makes errors fatal writes a diagnosis (HW.4, DSGN.5). Where that contract does not establish that such an end ends the other processes, each run of that path SHOULD carry a stated limit on its duration, or on the time that a process waits without progress, at which the run ends with a report to the operator (INTPR.7). The diagnosis of each halt of a parallel execution SHOULD be written to a record that persists beyond that execution (INTPR.8).

### Libraries

#### STND.MPI.8 Communicators from the caller

Default. Instantiates DSGN.14, DSGN.9.

Each library that communicates through MPI SHOULD take each communicator on which it communicates, or the session or group from which it derives one, from its caller through its interface (DSGN.14, DSGN.9). A library SHOULD NOT name in its own code a predefined communicator that spans more than its own process (DSGN.14). Where a library sends point-to-point messages, it SHOULD carry them on a communicator that it derives from the one it receives and that no other component uses (DSGN.14).

#### STND.MPI.9 Caller's error handlers kept

Default. Instantiates DSGN.14, DSGN.1.

A library SHOULD leave unchanged the error handler of each communicator, window, file, and session that it did not create (DSGN.14). Where its contract does not state that it ends the parallel execution, a library SHOULD report each failure that it detects to its caller (DSGN.1).

#### STND.MPI.10 Process-wide MPI state

Default. Instantiates DSGN.14.

Where its contract does not state otherwise, a library SHOULD leave to the program the initialization and the finalization of the world model of MPI, and each setting of MPI that applies to the whole process (DSGN.14). A library whose contract states that it initializes the world model SHOULD first query whether the world model is initialized and whether it has been finalized (DSGN.14). A library SHOULD leave the world model, and each session, that another component initialized to that component to finalize (DSGN.14).

#### STND.MPI.11 Owned MPI handles

Default. Instantiates DSGN.14.

Each MPI handle other than a request that the work creates SHOULD have one owner, which frees it before its process finalizes MPI or the session that holds it (DSGN.14). Code SHOULD NOT free a predefined handle (DSGN.14). Code SHOULD NOT free an MPI handle that another component owns (DSGN.14).

### Point-to-point messages

#### STND.MPI.12 Stated message protocol

Default. Instantiates DSGN.15, DSGN.1, DSGN.5.

Each message protocol of the work SHOULD be stated, at its implementation or in a design record that its implementation cites, with the order in which each process issues its operations (DSGN.15, DSGN.1). That statement SHOULD carry an argument that each process completes the protocol for each input in the regime of use, relying on no progress of MPI outside MPI calls beyond what the MPI standard guarantees (DSGN.15, DSGN.5). Where the statement carries no such argument, each test that runs the protocol SHOULD run under the check of deadlock of STND.MPI.25 (DSGN.15).

#### STND.MPI.13 No reliance on buffering

Default. Instantiates DSGN.15.

Each message protocol of the work SHOULD complete with each standard-mode send performed as a synchronous send (DSGN.15). The tests of each message protocol SHOULD include a passing run in which each standard-mode send is performed as a synchronous send, or in which the MPI implementation buffers no message (DSGN.15).

#### STND.MPI.14 Message type signatures

Default. Instantiates DSGN.4.

The type signature of the data that each receiving operation names SHOULD match that of the data that its matching operation sends, as the MPI standard defines the match (DSGN.4). The buffer of each receive SHOULD hold the longest message that the message protocol lets its matching sends carry (DSGN.4). Where a receive accepts messages of more than one length, the receiving code SHOULD obtain the length of each message from its status before it reads the data (DSGN.4).

#### STND.MPI.15 Nondeterministic matching

Default. Instantiates HW.12, REPRO.3.

Where a message protocol receives with a wildcard source or tag, completes one of a set of requests that MPI chooses, cancels an operation, or sends from more than one thread to one destination on one communicator, the declaration of run-to-run variation of HW.12 SHOULD state the order of matching or completion that varies between runs (HW.12, REPRO.3). Each result that such a protocol computes SHOULD be shown independent of that order within a declared tolerance, or carry in its record the order that occurred (REPRO.3).

#### STND.MPI.16 Nonblocking operation lifetimes

Default. Instantiates DSGN.1, DSGN.14.

Until a completion call reports a nonblocking or persistent operation complete, its buffer SHOULD stay allocated and unwritten by the process that started it (DSGN.1). Until a completion call reports a receive complete, the process that started it SHOULD NOT read its buffer (DSGN.1). Each process SHOULD complete each request that it starts, and free each persistent request, before it finalizes MPI or exits (DSGN.14).

### Collectives

#### STND.MPI.17 Collective call order

Default. Instantiates DSGN.1, DSGN.15, DSGN.5.

The members of the group of a communicator, window, or file SHOULD call the collective operations on it, those that create or free a communicator, window, or file included, in the same order, each in the same blocking, nonblocking, or persistent form, with the arguments that the MPI standard requires to agree (DSGN.1, DSGN.15). Code SHOULD rely on no synchronization of the processes by a collective operation beyond what the MPI standard guarantees for that operation (DSGN.5).

#### STND.MPI.18 Process-count dependence declared

Default. Instantiates REPRO.3, HW.12.

The declaration of run-to-run variation of each execution path that uses MPI SHOULD state each result that changes with the number of processes, with the decomposition of the problem among them, or with the order in which a reduction or concurrent accumulate operations combine values, and the size of that change or that its size is not established (REPRO.3, HW.12).

#### STND.MPI.19 Fixed-order collective reductions

Default. Instantiates NUMER.11, REPRO.3, VV.3.

Where bitwise identity across numbers of processes is an acceptance criterion, each reduction across processes that STND.VVUQ.2 covers SHOULD combine, in an order that the work fixes, partial results of blocks of the problem defined independently of the number of processes, or use an order-independent combination (NUMER.11, REPRO.3, VV.3). Where bitwise identity across numbers of processes is an acceptance criterion, each comparison between runs at different numbers of processes SHOULD judge identical bits (VV.3).

### One-sided communication

#### STND.MPI.20 Window synchronization protocol

Default. Instantiates DSGN.15, HW.11.

Each window SHOULD have a stated protocol that gives, for each pair of conflicting accesses to its memory, by one-sided operations or by loads and stores of a process to that memory, the synchronization that orders them under the memory model of the window that MPI reports (DSGN.15, HW.11).

### Parallel input and output

#### STND.MPI.21 Shared file access

Default. Instantiates DSGN.15.

Where processes write to a file that other processes access through the parallel input and output of MPI, the stated protocol of that file SHOULD give, for each pair of conflicting accesses from different processes, the atomic mode or the synchronization that orders them under the consistency semantics of the MPI standard (DSGN.15).

#### STND.MPI.22 Parallel file representation

Default. Instantiates DSGN.4, REPRO.12, INTPR.9, REPRO.3.

Each file that the work writes through the parallel input and output of MPI for reading by another run, platform, or tool SHOULD use a data representation that the MPI standard defines as portable, or carry a description of its layout and representation that a human reads without the producing software (DSGN.4, REPRO.12, INTPR.9). The record of such a file SHOULD state whether its content depends on the number of processes that wrote it (REPRO.3).

### Threads

#### STND.MPI.23 Threads sharing MPI objects

Default. Instantiates DSGN.15.

Where more than one thread of a process calls MPI, the stated protocol of the process SHOULD order the collective operations that its threads start on each communicator, window, and file (DSGN.15). Each request SHOULD be waited on or tested by at most one thread at a time (DSGN.15). A thread that probes for a message on a communicator on which other threads of its process receive SHOULD use a matched probe and receive the message that it matched (DSGN.15).

### Tests

#### STND.MPI.24 Tests across process counts

Default. Instantiates VV.1, REPRO.3, VV.3.

The tests of each component that uses MPI SHOULD run it on at least three numbers of processes that its message protocol admits, among them the smallest that it admits, or on each number that it admits, whichever set is smaller (VV.1, REPRO.3). Where the decomposition of the component admits a number of processes that divides its problem unevenly, one of those numbers SHOULD do so (VV.1). Where STND.MPI.19 does not govern a comparison of results between those runs, the comparison SHOULD judge agreement within a tolerance of the tier that STND.VVUQ.1 gives (VV.3, REPRO.3).

#### STND.MPI.25 MPI correctness checks

Default. Instantiates DSGN.3, DSGN.15.

Among the checks of each change to the code of the work that calls MPI, its tests SHOULD run under a check that fails the test at the first detection of a mismatch of collective operations or of type signatures, a deadlock, an overlap of the buffers of pending operations, or a request or MPI handle left incomplete or not freed at the finalization of MPI (DSGN.3, DSGN.15).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the Notes name the form of STND.CONC.30 for MPI: the processes of a parallel execution are concurrent tasks under STND.CONC; the order in which the lines of different processes reach the operator varies unless one process writes the output that the others send it in an order that the message protocol states; a collective write through the shared file pointer and a write at an offset that the protocol computes fix the order of the records of a file, while a noncollective write through the shared file pointer gives a variation that the record of the file declares; and STND.MPI.21, on conflicting accesses, and STND.CONC.30 do not conflict, one statement of the protocol of a file meeting both; the class paragraph cites GUARD, which it named without a References row; References lists GUARD and STND.CONC; no obligation changes. |
