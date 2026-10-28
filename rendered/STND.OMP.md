# OpenMP standard (STND.OMP) 1.1

Adopted by The Custodian as revision 1.0 in ledger entry 114 (2026-10-24); revised to 1.0.1 in entry 117 (2026-10-24), 1.0.2 in entry 174 (2026-10-25), 1.0.3 in entry 192 (2026-10-27), 1.0.4 in entry 216 (2026-10-28), and 1.1 in entry 276 (2026-10-28). This reading copy is composed from the per-provision files in STND/OMP/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice that is specific to the use of OpenMP, in every language in which the work uses it, on the host and on devices. It adds to STND.CONC, STND.OFFLD, STND.CODE, HW, and STND.VVUQ only what the directive model of OpenMP makes necessary. It covers the facilities that the work uses, the support of its implementations, the record of each run, and correctness without OpenMP (STND.OMP.1, STND.OMP.2, STND.OMP.3, and STND.OMP.4); the data environment of constructs (STND.OMP.5, STND.OMP.6, STND.OMP.7, and STND.OMP.8); the synchronization of teams (STND.OMP.9, STND.OMP.10, STND.OMP.11, STND.OMP.12, and STND.OMP.13); tasks and cancellation (STND.OMP.14, STND.OMP.15, and STND.OMP.16); reductions and schedules (STND.OMP.17 and STND.OMP.18); the runtime and the conduct of libraries (STND.OMP.19, STND.OMP.20, STND.OMP.21, and STND.OMP.22); offload to devices (STND.OMP.23 to STND.OMP.30); and tests (STND.OMP.31, STND.OMP.32, and STND.OMP.33).

Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The failures of OpenMP code are governed by provisions that already bind at every class: PRIME.4 for silent continuation past an error, STND.CONC.1 and STND.CONC.2 for asynchronous work and the failures of tasks, STND.CODE.7 for failures that code receives, HW.8 for faults, and HW.GPU.3 for offloaded work; STND.OMP.16 gives the OpenMP means where code relies on cancellation. The standard is compiler, vendor, implementation, and tool agnostic: its provisions name no implementation, compiler, runtime, checker, or revision of the OpenMP specification, which they take at the revision that the work's implementation documents, and they name directives, clauses, and routines of OpenMP by name and not by section (GOV.18). The rules of concurrency that hold for every model are in STND.CONC; the model-neutral rules of accelerator offload are in STND.OFFLD; and the C++ rules for exceptions at the boundary of a construct are in STND.CXX.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Concurrent task, Shared mutable object, Protection, Data race, and Lock have the meanings that STND.CONC gives them; an OpenMP task is a concurrent task, and so is each thread of a team. Execution path has the meaning that HW gives it. Directive, construct, region, structured block, clause, contention group, task, explicit task, tied task, untied task, deferred task, included task, merged task, task scheduling point, cancellation point, data environment, data-sharing attribute, private, threadprivate, internal control variable, worksharing construct, barrier, device, host device, device construct, target region, map, reference count, and memory scope have the meanings that the OpenMP specification gives them.

| Term | Definition |
| --- | --- |
| OpenMP specification | The OpenMP Application Programming Interface specification, at the revision that the OpenMP implementation of the work documents as the one it implements; where the work admits more than one OpenMP implementation, the earliest of the revisions that they document. |
| OpenMP implementation | A compiler that translates the directives of OpenMP for the work, together with the runtime library that executes them. |
| Feature | A directive, a clause, a modifier, a routine, or an environment variable of OpenMP. |
| Team | The set of threads that execute one parallel region, as the OpenMP specification defines it. |
| Offload policy | The setting of the OpenMP runtime that decides whether target regions run on the host: ending the run where a device construct finds no available or supported device, running every target region on the host, or falling back to the host by default. |
| Mandatory offload | The offload policy that ends the run where a device construct finds no available or supported device. |

## Notes

The provisions rest on the core of OpenMP that is stable across the recent revisions of the specification and its public drafts: fork and join, worksharing, tasks, data-sharing attributes, reductions, atomics, and the memory model that an earlier revision rebuilt. The latest technical report toward the next revision, a preview, adds features, deprecates one form of the atomic construct, and removes nothing (research/openmp-notes/r1-spec-trajectory.md). The drafts of the next revision renumber the chapters of the specification, so the provisions name directives and clauses and never sections. The term OpenMP specification takes the revision that the implementation documents, as STND.MPI does for MPI. The research notes are r1 to r4 of research/openmp-notes/; a fact that they do not support is marked unverified.

The standard adds OpenMP content to provisions that already hold the outcome, and does not restate them (GOV.31). STND.CONC holds the rules that hold for every model, and an OpenMP thread or task is a concurrent task under it: the protection of shared state (STND.CONC.3), the ordering of atomics (STND.CONC.4), the lifetimes of objects used by reference (STND.CONC.5), lock order (STND.CONC.7), the parent that waits for its tasks (STND.CONC.12), task migration and thread identity (STND.CONC.16), the conduct of libraries toward pools and settings of the whole process (STND.CONC.17), pools sized together on one node (STND.CONC.18), child processes of threaded programs (STND.CONC.19), the dependence of results on the number of threads and the combination of reductions where bitwise identity is the criterion (STND.CONC.21 and STND.CONC.22), tests at several numbers of threads (STND.CONC.24), run-time detection of data races (STND.CONC.25), and the order of the writes of concurrent tasks to one output or one record (STND.CONC.30). This standard gives their OpenMP forms only where OpenMP sets a trap of its own. HW.3 asks for the settings of a run that are able to affect its result; HW.CPU.3 governs the floating-point control state of each thread of a team, HW.CPU.4 records the threads of a run, and HW.CPU.5 reports oversubscription. HW.4 has the hardware contract of a path state the memory that the path relies on; HW.GPU.3 has offloaded work complete before its results are relied upon, HW.GPU.4 records data moved to and from devices, HW.13 and HW.14 govern what crosses between the host and a device, and HW.15 to HW.17 verify a device path against the reference path. STND.CODE.24 governs an exception that reaches the boundary of a structured block, and STND.MPI.3 the thread support level that a program combining OpenMP with MPI requests.

The specification does not require an implementation to detect data races, deadlocks, or programs that do not conform, and gives a data race an unspecified result (r2, corrections; r4). In one validation suite, 18 percent of the tests of one revision for C and C++, and 2 percent of those of the revision after it, passed on all five compilers tried, with results that changed between releases of one compiler (r4); no documentation of an implementation that the research read claims full support of the two latest published revisions that the research read, and support is documented feature by feature, in some cases for each language and device (r1). So neither a revision number nor a clean compilation shows that a feature works (STND.OMP.2). The latest published revision that the research read removed the features that the three revisions before it deprecated, among them the master construct, the environment variable and routine that enabled nested parallelism, and the minus operator of reductions, so a deprecated feature is a removal waiting to happen; that revision also undeprecated one form of the destroy clause of the depobj construct, which the revision before it had deprecated (r1). STND.OMP.1 judges deprecation by every later revision, published or in public draft, because the term OpenMP specification takes the earliest revision that the implementations of the work document. The initial values of most of the internal control variables that STND.OMP.3 names are implementation defined (r2), and the environment variables of OpenMP display them, which is what the record of STND.OMP.3 needs. The specification admits a program that is correct in parallel and wrong when built without OpenMP (r2, section 7), and STND.OMP.4 has the documentation of a component say which it is.

In a parallel construct, each variable that the region references and that has no attribute of its own is shared, so a scratch variable declared outside the construct becomes a data race; in C and C++ the index of an inner loop declared outside the construct stays shared; and in a task, a variable not shared in the enclosing context becomes firstprivate, so the writes of the task to it are lost (r2, section 1). A default clause of none, and a defaultmap clause of none for target constructs, make each such omission checkable (r2, r3), which is what STND.OMP.5 asks where a construct admits such a clause. A private copy starts with an undefined value; the original of a privatized variable has an unspecified value after the construct unless a lastprivate, reduction, or copyprivate clause defines it; and a lastprivate variable that the sequentially last iteration does not assign has an unspecified value (STND.OMP.6). A threadprivate variable keeps its value between parallel regions only where neither region is nested, the teams have the same size and binding, dynamic adjustment is off, and no pause or teams construct intervenes; a copyin clause copies the value of the primary thread to every thread of the team (unverified in r1 to r4), so it does not restore a value that differs between threads. An untied task that accesses threadprivate storage does not conform, and nothing assures a task that a threadprivate value survives a task scheduling point (r2, rule 8); the qualification of STND.OMP.7, a point at which another task is able to run on its thread, is an inference from that rule (STND.OMP.7, the OpenMP form of STND.CONC.16). A routine that shares its local variables with tasks and returns before they complete leaves them a dangling reference; the specification leaves that lifetime to the code that creates the tasks (STND.OMP.8, the OpenMP form of STND.CONC.5 and STND.CONC.12). The procedures of Fortran with initialized local variables or with the attribute SAVE have static storage, which is shared, so a call from several threads without a protection is a data race (r2, sections 1 and 9).

The specification requires that barriers and worksharing regions be reached by every thread of a team or by none, in the same order, so one inside control flow that differs between threads deadlocks (STND.OMP.9). A nowait clause lets threads proceed without a flush, and the values of lastprivate and reduction clauses are then defined only after a later synchronization; a masked region has no implied flush at its entry or exit (STND.OMP.10). An atomic construct without a memory-order clause behaves as relaxed, so a flag set by an atomic write does not publish the data written before it. That default differs from the default of the languages whose atomics order by default, which is why STND.OMP.11 asks for an ordering clause, or for an ordering default declared by a requires directive, where STND.CONC.4 would otherwise expect sequential consistency. A flush with a list does not order accesses to other variables, and the Examples call it extremely error prone (STND.OMP.11). The specification requires every access to a location that is able to run in parallel with an atomic access to it to be atomic; a critical construct or a lock does not exclude an atomic access; and an atomic access to a location that is not aligned to its size has implementation-defined behavior (r2) (STND.OMP.12). A signal handler shares state with the code that it interrupts, and STND.OMP.22 keeps OpenMP out of handlers, so STND.OMP.12 keeps atomic constructs off a location that a handler accesses, and the standard of the base language governs the access of the handler to it (STND.CXX.23 for C++); whether OpenMP atomics and those of the base language order one another on one location is not established in r1 to r4. Every unnamed critical construct shares one name, so unrelated critical sections exclude one another; a critical region inside another of the same name does not conform, and the specification warns that this is not sufficient to prevent deadlock; and a lock used across contention groups has unspecified behavior (STND.OMP.13).

The specification requires the items of depend clauses that order two tasks to name identical or disjoint storage; a taskwait waits only for the children of the task that encounters it, so data written by their descendants needs a taskgroup or a barrier; and a detached task completes only when its event is fulfilled, so an error path that skips the fulfillment hangs the program (STND.OMP.14). Recursive creation of tasks without a cutoff is able to reach the limit of the implementation on unassigned tasks, and the tasks inside a final task are included. A task that the implementation includes or defers, or a task with a mergeable clause that it merges into its parent, gives different results where code depends on the difference (STND.OMP.15). STND.VVUQ.82 governs a declared variation within the agreement that the acceptance criterion fixed, among them the order in which task reductions combine values. A cancel construct does nothing unless cancellation is enabled, which it is not at the start of a run; in a canceled region, the values of lastprivate and reduction clauses are undefined and locks are not released (r2). Where a failure, a bound of a wait (STND.CONC.10), or an early exit (STND.CONC.12) is answered by a cancellation that the run has not enabled, the run continues as if no cancellation were requested, which PRIME.4 forbids for a failure; STND.OMP.16 is the OpenMP means.

The specification leaves unspecified how many times, and in what order, the combiner of a declared reduction runs, so a combiner that is not associative and commutative gives results that depend on the schedule (STND.OMP.17). A static schedule, or an order clause with the reproducible modifier, gives the same mapping of iterations to threads for the same numbers of iterations and threads, but does not fix the order in which a reduction combines its partial results; with no schedule clause, the latest published revision that the research read behaves as if the schedule were auto, and the revision before it leaves the schedule implementation defined (STND.OMP.18). The writes that the threads of a team make to one output appear in the order in which the threads reach them, and a static schedule or the reproducible modifier fixes which thread runs each iteration and not when it runs, so neither fixes that order (by inference from STND.OMP.18). An ordered region runs in the order of the iterations of its loop, so the writes inside it appear in that order, at the cost of serializing that part of the loop (r2); a critical construct or a lock keeps two writes from interleaving and leaves their order to the schedule (by inference). An ordered region, or a single thread that writes what the others computed, is a protocol that fixes the order of output, and the record of the output declares each other order as a variation (STND.CONC.30). No provision of this standard asks for or forbids an order of output, so STND.CONC.30 applies to OpenMP without an OpenMP form.

The routines that set the number of threads or dynamic adjustment set the internal control variable of the current task, which every later region of the caller inherits, so a library that calls them changes the behavior of its caller (STND.OMP.19, the OpenMP form of STND.CONC.17). A team is able to have fewer threads than requested (STND.OMP.20). A branch or a longjmp that leaves a structured block does not conform, and a cancellation transfers control to the end of the canceled region (unverified in r1 to r4), which STND.OMP.21 admits; STND.CODE.24 governs exceptions. The specification lets a signal handler execute only directives and routines with the property of being safe in a signal handler; in the latest published revision that the research read only the entry points of tools have it, by inference from a search of that property (r2, section 6) (STND.OMP.22). The Examples of the specification warn that the resources of an OpenMP runtime may have unexpected side effects for a later call that creates a child by copying the process, and point to the routine that pauses those resources (r2, section 5); STND.CONC.19 governs.

The rules for offload rest on research/openmp-notes/r3-offload.md. A target region runs on the host when no device is available or supported, or when its if clause is false, and under the default offload policy it does so silently; mandatory offload ends the run instead where no device is available or supported, but a false if clause still runs the region on the host, by inference from r3; the report that the second alternative of STND.OMP.23 asks is not part of the first, and HW.19, HW.9, and the test of the path on the host in its second sentence cover the false if clause (STND.OMP.23). A device number that does not conform ends the run under mandatory offload, and otherwise has behavior that depends on the internal control variables; the default device is itself set by the environment (unverified in r1 to r4), so a number obtained from it is checked like any other; the specification pairs the routine that allocates device memory with the routine that releases it, and that routine returns a null pointer on failure, which STND.CODE.7, PRIME.4, and HW.8 already have code check (r3) (STND.OMP.24). Wrong map and nowait clauses were the main causes of mapping errors in one study (r4): a scalar referenced in a target region is firstprivate, so the writes of the device to it are lost; a pointer whose target is not mapped keeps its host address; a structure mapped in part and referenced in full does not conform; an update of data that is not present on the device does nothing unless it carries the present modifier; and a copy back to the host happens at the release of the last mapping of the data, or under the always modifier or an update construct, and not at the end of a nested mapping that the reference count keeps (STND.OMP.25 and STND.OMP.26). The device copy of a variable that a declare target directive names is initialized once, at an unspecified point, and the two copies diverge without an update; whether a variable of static storage is visible on a device without such a directive is implementation defined (STND.OMP.27). A device that does not meet a requires directive of the program is not a supported device, so code that relies on memory shared between host and device falls back to the host, or fails, on a device with separate memory, and one implementation documents dropping such devices; the specification requires every compilation unit with device code to declare the same requirements; and shared memory still needs synchronization between host and device (STND.OMP.28). The default memory scope of an atomic construct is the device, so an atomic construct without a wider scope does not order accesses between host threads and device threads (STND.OMP.29). The floating-point environment inside and after a target region is unspecified, and the mathematical functions and the contraction of operations on a device differ from those of the host (STND.OMP.30); HW.5 has the hardware contract state the delivered arithmetic of each path, and STND.VVUQ.1 gives the tier of a comparison between them. Most of these rules are specific to the directive model of OpenMP. STND.OFFLD holds the rules of offload that hold for every programming model, and this standard gives their OpenMP forms (GOV.31): STND.OMP.23 is the OpenMP form of STND.OFFLD.2, and its second sentence of STND.OFFLD.1 and STND.OFFLD.3; the first sentence of STND.OMP.24 of the second sentence of STND.OFFLD.23, and its second sentence of STND.OFFLD.10; STND.OMP.25 and STND.OMP.26 of STND.OFFLD.9, STND.OFFLD.10, and STND.OFFLD.11; the first sentence of STND.OMP.27 of STND.OFFLD.9; the second sentence of STND.OMP.28 of STND.OFFLD.12; STND.OMP.29 of STND.OFFLD.13; STND.OMP.30 of STND.OFFLD.14; STND.OMP.31 of STND.OFFLD.2 and STND.OFFLD.3; STND.OMP.32 of STND.OFFLD.30; and the last items of STND.OMP.3, the offload policy and the devices that the run uses, of STND.OFFLD.25. The second sentence of STND.OMP.27, on static data on a device, and the first sentence of STND.OMP.28, on the requires directive, have no form in STND.OFFLD: the first is specific to OpenMP, and HW.4 holds the second for every model. STND.OMP.30 reaches further than STND.OFFLD.14, which concerns device code and a floating-point environment that host code sets, so it stays a provision and not a citation: the specification leaves the floating-point environment unspecified inside and after a target region, and STND.OMP.30 governs every target region, so it also covers a target region that runs on the host, which is not device code in the sense of STND.OFFLD, and an environment that a target region sets, on which host code after the region would otherwise rely. Each provision of STND.OFFLD that has an OpenMP form here takes the class onset of that form, so the citations move no rule of this standard to another class.

A run under mandatory offload keeps a silent run on the host from passing as a device run, and a run on the host alone keeps the path on the host from decaying (STND.OMP.31). A detector of data races sees offloaded regions only when they run on the host, and errors of mapping, stale data among them, escape race detectors; in one study no single tool caught every class of anomaly studied, so a check of mapping errors is a separate check (STND.OMP.32; r4). A dynamic detector sees only the schedules that occurred, so a schedule or a binding of threads that the tests never set is never checked (r4; STND.OMP.33). STND.CONC.24 asks for tests at three or more numbers of threads, among them the smallest that a component admits, or at each number that it admits, whichever set is smaller, and STND.CONC.25 for run-time detection of data races where the means exist.

No OpenMP coding standard comparable to the safety and security coding standards of languages was found; one safety standard for C++ forbids pragmas outright, and one for C asks that each be documented and justified (r4). The literature on OpenMP for systems of high integrity proposes a restricted subset of OpenMP, a static allocation of tasks, memory bounded and allocated before parallel execution, and the exclusion of constructs whose order is not deterministic, as the basis of a subset small enough to be certified (r4).

Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, VV, or a provision of HW, and applies from the class that its field `onset` gives, which work of CSQ4 may omit; the features of the first sentence of STND.OMP.2, and the requires directive and the variant of STND.OMP.28, are rules of the form of code and apply from CSQ3, the last with HW.19, a part that carries out HW.4, HW.5, HW.11, HW.13, or HW.14 starts with that provision at CSQ2, and the sentences of each provision with three modals share one onset. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| HW.GPU | Accelerators |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.MPI | Message Passing Interface standard |
| STND.OFFLD | Accelerator offload standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Environment

#### STND.OMP.1 OpenMP facilities used

Default, from CSQ3. Instantiates SIMPL.4, REPRO.7.

Each feature that the work uses SHOULD be one that the OpenMP specification defines and that no later revision of the specification, published or in public draft, marks as deprecated (SIMPL.4). Where the work uses an extension of its OpenMP implementation, a decision record SHOULD state the extension, the reason for its use, and the behavior of the work on an OpenMP implementation that lacks it (REPRO.7).

#### STND.OMP.2 Implemented features only

Default, from CSQ3; sentence 2 from CSQ2. Instantiates DSGN.5, VV.1.

Each feature that the work uses SHOULD be one that the documentation of each OpenMP implementation that the work admits states as implemented for the language and the device of that use (DSGN.5). Each such feature SHOULD be exercised by a test of the work on each OpenMP implementation that the work admits (DSGN.5, VV.1).

#### STND.OMP.3 OpenMP run record

Default, from CSQ3. Instantiates HW.3, REPRO.2.

Among the items that HW.3 asks of the record of each result, the record of each result that code using OpenMP computes SHOULD give the OpenMP implementation and its revision, the runtime library loaded at run time, the value at the start of the run, and after each change that the code makes to it, of each internal control variable that sets the number of threads, their binding and places, dynamic adjustment, the number of active levels of parallelism, the policy of waiting threads, the size of the stacks of threads, the run-time schedule, cancellation, and the default device, and the offload policy and the devices that the run uses (HW.3, REPRO.2).

#### STND.OMP.4 Correctness with OpenMP disabled

Default, from CSQ3. Instantiates SIMPL.6, DSGN.1, VV.1.

The documentation of each component that uses OpenMP SHOULD state whether the component builds, and computes its results within their stated tolerances, with OpenMP disabled (SIMPL.6, DSGN.1). Where that documentation states so, the checks of each change SHOULD build and test the component with OpenMP disabled (VV.1).

### Data environment

#### STND.OMP.5 Explicit data-sharing attributes

Default, from CSQ3. Instantiates SIMPL.6, DSGN.14.

Each construct that creates a data environment SHOULD give each variable that its region references an explicit or a predetermined data-sharing attribute (SIMPL.6, DSGN.14). Where a construct admits a clause that makes an implicit data-sharing attribute or map an error, the construct SHOULD carry that clause (SIMPL.6).

#### STND.OMP.6 Private and last values

Default, from CSQ3. Instantiates DSGN.14.

Where no clause initializes a private copy of a variable, code SHOULD write that copy before it reads it (DSGN.14). Where no clause of a construct defines the value of an original variable that the construct privatizes, code SHOULD NOT rely on that value after the construct (DSGN.14). Each variable of a lastprivate clause SHOULD be assigned in the iteration or the section that is sequentially last, or carry the conditional modifier (DSGN.14).

#### STND.OMP.7 Threadprivate persistence

Default, from CSQ3. Instantiates DSGN.14.

Where code relies on the value of a threadprivate variable persisting from one parallel region to another, those regions SHOULD meet the conditions under which the OpenMP specification makes it persist (DSGN.14). Each task that accesses threadprivate storage SHOULD be a tied task (DSGN.14). A task SHOULD NOT rely on the value of a threadprivate variable persisting across a task scheduling point of that task at which another task is able to run on its thread (DSGN.14).

#### STND.OMP.8 Shared locals and explicit tasks

Default, from CSQ3. Instantiates DSGN.14.

A routine that shares one of its local variables with an explicit task SHOULD complete, before it returns, a taskwait or a taskgroup that waits for that task (DSGN.14).

### Synchronization

#### STND.OMP.9 Uniform team constructs

Default, from CSQ3. Instantiates DSGN.15.

The threads of each team SHOULD encounter the same worksharing and barrier regions, in the same order (DSGN.15). Each worksharing and barrier construct SHOULD be reached under conditions that hold alike for every thread of its team (DSGN.15).

#### STND.OMP.10 Consumers of nowait regions

Default, from CSQ3. Instantiates DSGN.15.

Where a construct carries a nowait clause, each read by another thread of data that its region writes, and each read of a lastprivate or reduction result of that region, SHOULD follow a synchronization that completes that region (DSGN.15). Each read by another thread of data that a masked region writes SHOULD follow a synchronization that follows that region (DSGN.15).

#### STND.OMP.11 Atomic memory order clauses

Default, from CSQ3; sentence 1 from CSQ2. Instantiates DSGN.15, HW.11.

Each atomic construct that orders accesses to other data between threads SHOULD carry a memory-order clause that orders them, or rely on a default memory order that orders them and that a requires directive of its compilation unit declares (DSGN.15, HW.11). Code SHOULD NOT use a flush construct with a list (DSGN.15).

#### STND.OMP.12 Locations accessed atomically

Default, from CSQ3. Instantiates DSGN.15.

Where an access is able to run in parallel with an atomic construct on the same storage location, that access SHOULD be an atomic construct (DSGN.15). Each storage location that an atomic construct accesses SHOULD be aligned to a multiple of its size (DSGN.15). Code SHOULD NOT use an atomic construct to access a storage location that a signal handler accesses (DSGN.15).

#### STND.OMP.13 Critical names and lock scope

Default, from CSQ3. Instantiates DSGN.15.

Each critical construct SHOULD carry a name for the shared mutable objects that it protects (DSGN.15). Where a critical region is able to run inside another, the two SHOULD carry different names (DSGN.15). Each OpenMP lock SHOULD be set and unset only by threads of the contention group in which it was initialized (DSGN.15).

### Tasks

#### STND.OMP.14 Task dependences, waits, and events

Default, from CSQ3. Instantiates DSGN.15.

The items of the depend clauses that order two tasks SHOULD name identical or disjoint storage (DSGN.15). Before code reads data that tasks write, it SHOULD complete a wait that covers each task that writes that data, its descendants included (DSGN.15). The event of each detached task SHOULD be fulfilled on every path of the code that holds it, failures included (DSGN.15).

#### STND.OMP.15 Bounded task creation

Default, from CSQ3. Instantiates RSRC.1, DSGN.1.

Each recursive creation of tasks SHOULD stop deferring tasks at a stated cutoff (RSRC.1, DSGN.1). The results of code that creates tasks SHOULD be the same, within the agreement that the acceptance criterion fixes, whether each task is deferred or included (DSGN.1, STND.VVUQ.82). Each task with a mergeable clause SHOULD give the same results, within that agreement, whether or not it is merged (DSGN.1).

#### STND.OMP.16 Cancellation enabled and tested

Default, from CSQ3. Instantiates DSGN.15, VV.1.

Where code relies on a cancel construct, each run of that code outside its tests SHOULD have cancellation enabled (DSGN.15). The tests of code that relies on a cancel construct SHOULD run it with cancellation enabled, and with cancellation disabled to show that the code does not pass over the disabled state silently (VV.1). Where a region is able to be canceled, each task of it SHOULD release each lock that it holds before it reaches a cancellation point (DSGN.15).

### Reductions and schedules

#### STND.OMP.17 Declared reduction properties

Default, from CSQ3. Instantiates DSGN.1, REPRO.7.

Each declared reduction SHOULD state, at its declaration, why its combiner is associative and commutative within the tolerance that judges its results, and why its initializer is an identity of its combiner (DSGN.1, REPRO.7).

#### STND.OMP.18 Reproducible iteration mapping

Default, from CSQ3. Instantiates REPRO.3.

Where a result relies on the mapping of the iterations of a loop to threads, the loop SHOULD carry a schedule or an order clause under which the OpenMP specification makes that mapping reproducible (REPRO.3). Code SHOULD NOT rely on such a clause to fix the order in which a reduction combines values (REPRO.3).

### Runtime and libraries

#### STND.OMP.19 Caller's control variables kept

Default, from CSQ3. Instantiates DSGN.14.

Where its contract does not state otherwise, a library SHOULD leave each internal control variable of its caller unchanged, and set a property of a region that it creates only through a clause of its own construct (DSGN.14).

#### STND.OMP.20 Team size as obtained

Default, from CSQ3. Instantiates DSGN.1.

Code SHOULD size the state that it keeps for each thread of a team from the number of threads that the team has, obtained inside its region, and not from the number that it requested (DSGN.1).

#### STND.OMP.21 Structured block exits

Default, from CSQ3. Instantiates DSGN.1.

Code SHOULD leave the structured block of a construct only through the end of that block, or by ending the program (DSGN.1).

#### STND.OMP.22 Signal handlers without OpenMP

Default, from CSQ3. Instantiates DSGN.15.

A signal handler SHOULD NOT contain an OpenMP directive (DSGN.15). A signal handler SHOULD NOT call an OpenMP routine (DSGN.15).

### Offload

#### STND.OMP.23 Device placement enforced

Default, from CSQ3. Instantiates HW.19, HW.9, HW.15, VV.1.

Each run that relies on a target region running on a device SHOULD run under mandatory offload, or confirm from inside the region that it ran on a device and report each region that ran on the host (HW.19, HW.9). Each if clause of a device construct SHOULD have its path on the host stated and tested (HW.15, VV.1).

#### STND.OMP.24 Device numbers and allocations

Default, from CSQ3; sentence 2 from CSQ2. Instantiates DSGN.1, DSGN.14, HW.13.

Each device number that code passes to a device construct or to a routine SHOULD be the host device, or one that the code has checked against the number of devices that the runtime reports (DSGN.1). Storage that a device memory routine allocates SHOULD be released exactly once, after its last use, on every path, failures included, by the routine that the OpenMP specification pairs with the routine that allocated it (DSGN.14, HW.13).

#### STND.OMP.25 Structures and pointers on devices

Default, from CSQ2. Instantiates DSGN.4, HW.13.

Where a target region references a member of a structure, its maps SHOULD cover the whole structure or each member that it references (DSGN.4, HW.13). Where a target region dereferences a pointer, the storage that the pointer addresses SHOULD be mapped, and the pointer attached to it on the device (DSGN.4, HW.13). A pointer attached on a device SHOULD keep its value while it is mapped (DSGN.4, HW.13).

#### STND.OMP.26 Balanced and present mappings

Default, from CSQ2. Instantiates DSGN.14, HW.13, HW.14.

Each mapping that code starts outside a structured data construct SHOULD be ended exactly once on every path, failures included (DSGN.14, HW.13). Each update of data on a device on which a result relies SHOULD carry the present modifier (HW.14). Where a result relies on data copied back from a device, the copy SHOULD be one that the reference count of that data does not suppress: the release of the last mapping of that data under a map type that copies it back, an update construct, or an always modifier (HW.13).

#### STND.OMP.27 Device copies of global variables

Default, from CSQ2. Instantiates DSGN.14, DSGN.5, HW.13.

Where a result relies on a variable that a declare target directive names, each write of one copy of that variable SHOULD be carried to the other copy by an update construct, or by a map with an always modifier, before the other copy is read (DSGN.14, HW.13). Each variable of static storage that a target region uses SHOULD be named in a declare target directive, or mapped (DSGN.5, HW.13).

#### STND.OMP.28 Shared memory reliance

Default, from CSQ3. Instantiates DSGN.5, HW.19.

Where a component relies on memory shared between the host and a device, each of its compilation units that contains device code SHOULD declare that reliance by a requires directive with the same clauses (DSGN.5). Where no device that a run uses meets the requires directive of a component that relies on shared memory, the run SHOULD end with a report to the operator, or run a variant of the component that maps its data (DSGN.5, HW.19).

#### STND.OMP.29 Host and device atomics

Default, from CSQ2. Instantiates DSGN.15, HW.11.

Each atomic construct that orders accesses between threads of the host and threads of a device SHOULD carry a memory scope that includes both (DSGN.15, HW.11).

#### STND.OMP.30 Floating-point state on devices

Default, from CSQ2. Instantiates DSGN.5, HW.5.

Code SHOULD rely on a floating-point environment only within the host code or the target region that sets it (DSGN.5, HW.5).

### Tests

#### STND.OMP.31 Offload test runs

Default, from CSQ3. Instantiates VV.1, HW.15.

The tests of each target region SHOULD run it under mandatory offload, run it on the host alone under each OpenMP implementation that supports such a run, and compare each result with a reference computed on the host within a tolerance of the tier that STND.VVUQ.1 gives (VV.1, HW.15).

#### STND.OMP.32 Mapping checks

Default, from CSQ2. Instantiates DSGN.15, HW.14.

Where the means of the work include a check that detects at run time data missing from a device, stale on it, or mapped in error, the tests of each change to code with target regions SHOULD run under that check (DSGN.15, HW.14).

#### STND.OMP.33 Schedules and bindings tested

Default, from CSQ3. Instantiates VV.1.

The tests of code that uses OpenMP SHOULD run under each schedule and each binding of threads to places that the runs of the work set through internal control variables (VV.1).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.0.1 | 2026-10-24 | Editorial amendment (GOV.41): the Purpose and the Notes cite STND.OFFLD, adopted in ledger entry 116, in place of a planned standard for offload; the Notes give the provision of STND.OFFLD of which each of STND.OMP.23 to STND.OMP.32 and the last items of STND.OMP.3 is the OpenMP form, and state why STND.OMP.30 stays a provision; and References lists STND.OFFLD; no obligation changes. |
| 1.0.2 | 2026-10-25 | Editorial amendment (GOV.41): the Notes list STND.CONC.30 among the provisions of STND.CONC that hold for the threads and tasks of OpenMP, and name its OpenMP form: neither a static schedule nor the reproducible modifier fixes the order of the writes of a team to one output; an ordered region fixes it, at the cost of serializing that part of the loop, and a single thread that writes what the others computed fixes it too; a critical construct or a lock prevents interleaving without fixing the order; and no provision of the standard conflicts with STND.CONC.30; no obligation changes. |
| 1.0.3 | 2026-10-27 | Editorial amendment (GOV.41): the Notes cite STND.CODE.24 in place of STND.CXX.22, which STND.CXX 1.3 withdraws, for an exception that reaches the boundary of a structured block; no obligation, permission, or defined meaning changes. |
| 1.0.4 | 2026-10-28 | Editorial amendment (GOV.41): the Notes name the revisions of the OpenMP specification by their order, an earlier revision, the revision after it, the latest published revision that the research read, and the next revision, in place of their numbers, which ruling D1 takes out of the Notes; no obligation, permission, or defined meaning changes. |
| 1.1 | 2026-10-28 | Minor amendment (GOV.41): the first sentence of STND.OMP.2 and STND.OMP.28 apply from CSQ3, as rules of the form of code, the second with HW.19; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
