# Workflow and long-run resilience standard (STND.WFLOW) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/WFLOW/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice that makes a run of a computational workflow correct, resumable, and traceable: a run of many steps over files and jobs, and a long job that a scheduler or a platform is able to end before its work completes. A single long job is a workflow of one step. It adds to REPRO, INTPR, DSGN, RSRC, HW, STND.CONC, and STND.MPI only what workflows and long runs make necessary. It covers the declarations of steps, their effects, and their repetition (STND.WFLOW.1 to STND.WFLOW.5); staleness and reuse (STND.WFLOW.6); the publication of outputs and the partial outputs of an attempt (STND.WFLOW.7 to STND.WFLOW.10); retries and the record of attempts (STND.WFLOW.11 to STND.WFLOW.16); the ends of jobs, notice, and grace (STND.WFLOW.17 to STND.WFLOW.20); restart state (STND.WFLOW.21 to STND.WFLOW.28); sets of parts and the failure of a part (STND.WFLOW.29 to STND.WFLOW.31); storage, staging, and work directories (STND.WFLOW.32 to STND.WFLOW.36); provenance, resumption, and clocks (STND.WFLOW.37 to STND.WFLOW.40); and tests (STND.WFLOW.41 to STND.WFLOW.44).

Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The observation of the completion of each job and each step, the reach of a failure of one part or process to the others, and the loud answer to an exhausted resource, storage included, bind at every class through STND.CONC.1, STND.CONC.2, STND.MPI.6, HW.8, and PRIME.4, and this standard adds nothing to that floor. The standard is agnostic of workflow engine, scheduler, file system, platform, and tool: its provisions name no engine, scheduler, file system, format, or revision of a specification (GOV.18). Concurrency inside one program belongs to STND.CONC, the work process of agents and people to STND.WPROC, and the halt of a job of several processes that communicate by message passing to STND.MPI; this standard cites them and does not restate them.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Workflow, Input, Result, Record, Provenance, Effect, State, Temporary item, Computational environment, and Relying party have the meanings that the Lexicon gives them. Capacity has the meaning that HW gives it. Concurrent task and Asynchronous operation have the meanings that STND.CONC gives them; each job that a workflow submits to a scheduler is an asynchronous operation, and each step that runs while another step of the same workflow run has not completed is a concurrent task.

| Term | Definition |
| --- | --- |
| Step | A part of a workflow that runs as one unit from its declared inputs to its declared outputs: a command, a script, a job, or a task that a workflow engine starts. |
| Workflow description | The versioned text from which a workflow engine runs a workflow: its steps, their declarations, and its rules of staleness, reuse, and retry. |
| Declaration | Of a step: the part of the workflow description that names the inputs, outputs, checks, and effects of that step. |
| Workflow engine | The software that runs the steps of a workflow from its workflow description, decides which steps to run, and records their attempts; a script that runs steps in a fixed order is one. |
| Workflow run | One execution of a workflow, from its start or from a resumption to its completion or its halt. |
| Resumption | The start of a workflow run that continues a halted or ended workflow run from its records and outputs, without running again the steps that completed. |
| Attempt | One execution of a step from its start to its end; a retry, a requeue, or a resumption that runs the step again starts another. |
| Retry | An attempt that a layer of a workflow starts after an earlier attempt of the same step failed or was ended. |
| Reuse key | The value from which a workflow decides that a stored output of a step is current. |
| Final name | The name under which a consumer of an output of a step reads it. |
| Partial output | Data that an attempt writes and that has not passed the completion checks of its step. |
| Part | One of a set of steps that a workflow starts from one declaration over different inputs: a task of a job array, or one branch of a fan-out. |
| Job | A unit of execution that a scheduler starts with a grant of resources and a limit on its duration, and that the scheduler is able to end, preempt, or requeue. |
| Scheduler | The software of a computing system that grants jobs their resources, and starts, preempts, requeues, and ends them. |
| Forced end | An end of a process that the process is unable to catch, block, or delay. |
| Notice of end | A signal or message by which a scheduler or a platform tells a job, before a forced end, that the forced end follows. |
| Grace period | The time between a notice of end and the forced end that follows it. |
| Restart state | The state of a computation that a job writes to storage so that a later job continues the computation from it in place of starting again. |
| Generation | One complete write of the restart state of a computation. |
| Work directory | Storage in which a workflow keeps the intermediates, caches, partial outputs, and records of its steps between steps and between workflow runs. |

## Notes

The custodian's order of standards of 2026-10-24 places a separate standard for workflows and the resilience of long runs after STND.OFFLD, and the custodian's directions of that date keep each standard agnostic and timeless and keep the directions on determinism (STND.VVUQ.82 and STND.VVUQ.83): strict determinism is an option where it is feasible, not a requirement unless the acceptance criterion or the consequence class demands it, and a declared variation within the agreement of the acceptance criterion is no defect. The sources are the research notes research/workflow-notes/w1-workflows-and-resilience.md (below, w1) and research/concurrency-notes/c3-distributed-resilience.md (below, c3). Their fetch tool returned extracts written by a model in place of the text of pages, and rows that rest on the text of search results are marked so in the notes; a fact that the notes mark unverified, or that rests on a search extract, is marked unverified here. Sources are cited by the identifier of the row that a sentence relies on; w1 gives one page more than one identifier. The products that the sources describe appear here only as evidence of a hazard.

The standard adds to provisions that already hold the outcome, and does not restate them (GOV.31). REPRO.1 to REPRO.3 hold the recorded inputs, the environment, and the declaration of variation; REPRO.4 holds provenance written at production and the label of provenance reconstructed afterward; REPRO.10 makes the workflow description a versioned, reviewed artifact and a result of unrecorded manual steps unreproducible; REPRO.12 and STND.DFLT.4 hold the retention and readability of records; RSRC.1 to RSRC.3 hold budgets and their record, and RSRC.7 the decision to reuse or recompute; INTPR.6 to INTPR.8 hold the report of state, anomalies, among them a resource that trends toward exhaustion, and diagnostics; INTPR.12 and INTPR.13 hold the resumption of the work by a person from its artifacts; QA.9 holds regeneration by another actor. STND.CONC.1 has the completion of each asynchronous operation, each job submitted to a scheduler included, observed by a call or callback that reports its failure before a result relies on it; STND.CONC.2 has the failure of a concurrent task reach its parent and the tasks that wait on it; STND.CONC.10, STND.CONC.13, and STND.CONC.14 bound waits, pass cancellations on, and bound queues and pools; and STND.CONC.29 records the operations left pending at the end of a run. STND.MPI.5 to STND.MPI.7 hold the halt of a job whose processes communicate by message passing and the limit on the duration of a run in which an ended process does not end the others; STND.MPI.21 and STND.MPI.22 hold the files that such a job writes through the parallel input and output of MPI. HW.8 has an exhausted capacity of hardware answered as PRIME.4 requires, HW.9 states in the record of a result the hardware events across which it was computed, the failure of a node among them, and HW.10 has results checked where a fault goes undetected, the silent corruption of data that c3 reports from production fleets (c3, S20 and S21) among them. STND.CODE.7 forbids discarding a reported failure, the failed or short write in the path of shutdown that w1 reports included (w1, W12). STND.VVUQ.2 has a restart judged by bitwise identity hold the complete state of the computation. STND.DFLT.9 and QA.3 bound the attempts of a unit of work; the number three in STND.DFLT.9 belongs to units of work and not to the retries of a step.

STND.WPROC governs the work process of agents and people, and no provision of it governs a workflow run; an agent that runs a workflow does so inside a unit of work that STND.WPROC and AGENT govern. A build system that runs the steps of a workflow is a workflow engine under this standard; the building of software belongs to the planned standard for builds. The concurrency of the steps of one workflow run is governed by STND.CONC: a step that runs while another has not completed is a concurrent task, and a job is an asynchronous operation, so STND.CONC.1 and STND.CONC.2 bind them at every class.

A step that reads a file or a tool that it does not declare reruns on no change there and behaves differently on another host, and the declaration of each step is what incremental execution, caching, and cleanup trust (w1, W15) (STND.WFLOW.1). The declared inputs of a part do not include the order in which the parts of its set start, so STND.WFLOW.1 also keeps a part from relying on that order, which one scheduler does not guarantee (w1, W24). A step whose output depends on the time, on random draws, on the network, on the order of a directory listing, or on the order in which parallel work completes declares it under REPRO.3; a workflow that reruns such a step and keeps the stored outputs of its consumers combines outputs of two attempts that disagree (w1, answer 6) (STND.WFLOW.2). A declared variation within the agreement of the acceptance criterion is no defect, so STND.WFLOW.2 asks for a rule of reuse and not for determinism. A step that exits with a status of zero and writes an empty or wrong output is accepted by an engine that judges by exit status alone, and the error appears steps later; two published workflow languages let a declaration state checks of outputs that fail the step (w1, W2 and W4) (STND.WFLOW.3). A step whose check of an output fails and that still reports success continues silently past a detected error, which PRIME.4 forbids at every class; STND.WFLOW.3 adds which checks run, which lies above the floor. Engines run a task more than once by default: one retries on the death of a worker, another runs four attempts and optional speculative copies, and a scheduler that requeues a job starts its script again from the beginning (c3, S5, S6, and S14) (STND.WFLOW.4 and STND.WFLOW.5). A key that a caller supplies and that the receiving system stores atomically with the result returns the first outcome on a retry (c3, S15); one orchestration framework asks for tasks that give the same outcome on every rerun and writes by partition in place of appending (w1, W5). That a task of one controller of containers runs more than once when it is evicted after it finishes and before its completion is recorded is unverified (w1, W37). DSGN.16 confines effects to declared places, and STND.WFLOW.4 names the place of each effect of a step that is able to run again. A write to a remote system by an agent proceeds only under an authorization (PRIME.7), and a retry repeats it within the scope of that authorization.

Build systems that use the times at which files were modified as the mark of a stale file require that those times only move forward, which backup software violates, and they are minimal only where no one changes a time without changing content; a build system with early cutoff stops where a rebuilt intermediate is unchanged (w1, W14, read as full text). One engine keys a task on the path, time, and size of its inputs, its script, and its environment, and shared file systems are able to report times that differ between reads; another does not invalidate a cached value when its code changes (w1, W3; c3, S10 and S11) (STND.WFLOW.6). A key over inputs recomputes every dependent of a changed input, and a key over the content of each output stops at an unchanged one (w1, W47, a search extract, unverified); STND.WFLOW.6 has the description state which the workflow uses, and RSRC.7 admits reuse only where it preserves correctness and reproducibility. A time is able to serve as a first filter before a comparison of content.

A rename replaces its target atomically only within one mounted file system, and fails across two, even for one file system mounted twice; a step that then copies the file leaves it visible while half written (w1, W10) (STND.WFLOW.7). On the systems that w1 read, a temporary name in the directory of the final name meets STND.WFLOW.7, and a copy made after a failed rename does not. A sync of a file does not make the entry of its name in a directory durable, which needs a sync of the directory as well, and one study found 60 vulnerabilities to a crash in 11 applications, the fixes of several of which added a missing sync of a directory (w1, W9; c3, S37 and S42) (STND.WFLOW.8). A step that a forced end interrupts leaves a file under its final name that a later run takes for a result, or leaves a private directory that fills the disk; one engine keeps logs on error, and whether a common build tool deletes a target after a failed recipe by default is unverified (w1, W2) (STND.WFLOW.9). In one engine, the task that finishes last overwrites a published file of the same name (w1, W3), and two attempts of one step that both complete give one final name two writers unless STND.WFLOW.7 publishes only one of them (STND.WFLOW.10). The removal of a partial output by the workflow engine is an act of the software; its removal by an agent is an action that GUARD.5 and GUARD.6 govern, exempt under STND.DFLT.15 only where the item was recorded as temporary from its creation, and GUARD.6 prevails over that exemption for a removal whose scope is not enumerated and verified first.

Retries without a delay strike a shared service that is down from every caller at once, and a delay that grows to a cap with a random part spreads them (w1, W6) (STND.WFLOW.12). Three retries at each of five layers multiply the load on a failing service by 243, and the chapter that reports it proposes a limit of retries for each request and a budget of retries for each server; w1 draws from it the practice of retrying at one layer (w1, W16 and W18) (STND.WFLOW.13). The last sentence of PRIME.7 binds an agent's authorized remote access to the limits that the remote side publishes, which STND.WFLOW.12 serves for every retrying layer; the delay and its random part keep the load that retries put on a shared service within the behavior that its contract under DSGN.5 states for the regime of use. Published workflow languages separate the exit statuses that a retry clears from those that end the run (w1, W3 and W4) (STND.WFLOW.11); an invalid input, a failed check of an output, and a defect that recurs on identical inputs are not cleared by a retry. The same request for memory runs out of memory again, and whether the range of statuses that one engine's example retries means a kill for memory is unverified (w1, W3) (STND.WFLOW.14). A retry also hides a defect: a report conjectured that most faults of production software are transient, and later work argues that rare deterministic faults cause much of the downtime (w1, W36, a search extract, unverified), so a failure that a later attempt clears is an anomaly to follow (STND.WFLOW.15). A requeued job of one scheduler starts its script again with the same identifier, and its output files open by append or by truncation according to a default that the site sets, so the second attempt truncates the log of the first or appends to it without a mark (w1, W8) (STND.WFLOW.16).

One scheduler sends a signal that a process is able to catch to a job chosen for preemption and an uncatchable one at its new end, with an interval at the limit on duration whose default is 30 seconds; it sends a signal that the job requests a stated number of seconds before the end, to the steps of the job unless the request names the batch shell, so that a handler in the script does not run (w1, W8, W12, and W38). One provider of rented capacity gives a notice two minutes before it reclaims a machine, on a basis that it does not guarantee, and none before one kind of suspension (w1, W39); the grace period of one controller of containers is unverified (w1, W40). A limit that one scheduler treats as soft for a stated number of minutes has a default of zero (w1, W38). STND.WFLOW.17 therefore has the notice, its recipients, and the grace period stated from the configuration of the computing system or a measurement, and the limit read at run time; STND.WFLOW.18 has the write that answers a notice fit the grace period, and STND.WFLOW.21 keeps the interval of writes where a notice is given, since a notice is not guaranteed. The uncatchable signal is assumed to follow, so the state on storage is valid at every instant without code that runs at the end: STND.WFLOW.7, STND.WFLOW.8, and STND.WFLOW.22 hold that for outputs and restart state, and STND.WFLOW.20 for the records, caches, and indexes of the workflow engine. A handler that interrupts a function that is not reentrant and calls it again operates on inconsistent data (w1, W13) (STND.WFLOW.19). A handler of a signal is a concurrent task under STND.CONC, so STND.CONC.3 governs the objects it shares with the main code; STND.OMP.22 is a form of STND.WFLOW.19 for OpenMP, and STND.CONC.17 keeps a library from changing the handling of signals of its caller. Under one configuration of one scheduler, a kill for memory ends processes of a step while the step keeps running (w1, W19); STND.CONC.2 and STND.MPI.6 have the other processes of that step halt or answer the halt, at every class.

The word checkpoint commonly names what this standard calls restart state; STND.DFLT defines Checkpoint as a copy of an item's prior state kept before an action, so this standard uses another term. The interval between writes of restart state near which the expected loss is least depends on the cost of a write and the mean time between failures (c3, S25, a search extract, unverified) (STND.WFLOW.21); RSRC.7 decides reuse or recompute on measured cost, and the interval is that decision for one job. In one report to the mailing list of a library of checkpoints, earlier generations that shared a file were found truncated, and the reply attributed it to a checkpoint that observed a file while it was still being written (w1, W20, a single report) (STND.WFLOW.22). One library of checkpoints reports success only where every process passes a flag of validity (c3, S22), does not load a checkpoint that is marked incomplete, and by default copies to the parallel file system only every tenth checkpoint (w1, W21) (STND.WFLOW.23). A transparent checkpointer of processes does not state, in what w1 read, what it fails to capture; a restart into a state that holds an open connection or the context of an accelerator no longer matches the world (w1, W42, unverified for its limits) (STND.WFLOW.24). A reused seed of random numbers on restart reportedly distorted a thermostat in one simulation code (c3, S65, not read, unverified); STND.VVUQ.2 has a restart judged by bitwise identity hold the states of its random streams, and STND.WFLOW.24 has every restart state state what it holds. STND.MPI.22 states whether a file written through MPI depends on the number of processes that wrote it, and STND.WFLOW.24 asks the same of each restart state. The rule that a restart state records the identity of its run and is refused where that identity differs (STND.WFLOW.25 and STND.WFLOW.26) is reasoned in w1 and not sourced: a restart that loads the state of another run, or of another revision of its code, continues another computation and gives a plausible and wrong result. Restart state that a forced end, a purge, a restore, or another run is able to have changed since its write is data that enters the run from storage the run did not hold at every instant, so STND.WFLOW.26 and STND.WFLOW.28 check it where it enters, as the first sentence of DSGN.2 asks. The default protocol of one serialization format changes between releases of its language, and a format that executes code when it loads is not secure against data from another source (w1, W22) (STND.WFLOW.27 and STND.WFLOW.28); the threat model of GUARD.16 and the practice of GUARD.17 govern the rest. Restart state is not an archive format: a result that a later run reads from it is a record that REPRO.12 governs.

In one scheduler, a dependency on a whole array waits for every task to succeed, and another is satisfied after the array completes with at least one task that failed; the tasks of an array are not ordered, a requeue is able to name one element, the number of tasks that run at once is able to be capped, and the scheduler keeps the record of an ended job in memory for a period whose default is 300 seconds (w1, W24 and W38) (STND.WFLOW.29 to STND.WFLOW.31). The set of completed parts derived from checked outputs survives the loss of those records. STND.WFLOW.31 is the analogue, for the jobs of a workflow, of the bounded pools of STND.CONC.14, and AGENT.40 governs the starting of parallel units of work by agents on a shared machine.

One computing center blocks every write by an account whose usage exceeds its quota of storage, while it still accepts submissions; a separate quota counts files and directories; and its scratch storage makes each file not accessed within 8 weeks subject to deletion (w1, W26 to W28) (STND.WFLOW.32 and STND.WFLOW.33). By the reasoning of w1, a workflow of a million tasks in an engine that makes one directory for each task exhausts the count of files before the space (w1, W28 and W3). In the design of one parallel file system, quota is granted to storage targets in portions, so that a write fails for quota while the account is below its limit (w1, W44, from material of 2008 and 2009, unverified for current releases). A quota is a limit of policy and not a capacity in the sense of HW, so PRIME.4 governs its exhaustion directly and HW.8 governs a full device; INTPR.7 already has a trend of storage toward either reported while intervention is still possible, and STND.WFLOW.32 adds the budget and the check at the start. A shared network file system gives consistency from close to open only, its locks are advisory and able to be lost, concurrent appends through it are able to corrupt files, one embedded database states that one of its modes does not work over a network file system, and one mode of a scientific file format requires storage that orders writes as POSIX does, which excludes network file systems by a search extract (unverified) (c3, S36, S39, S40, and S44 to S48) (STND.WFLOW.34); STND.MPI.21 is the form of STND.WFLOW.34 for the parallel input and output of MPI. An input updated between reruns changes the outputs without notice (w1, W5), so a step that stages data declares its source as an input under STND.WFLOW.1 and keys it under STND.WFLOW.6, and STND.WFLOW.35 checks the copy. One engine resumes only where its cache of tasks and its work directories are both kept (w1, W45), so a cleanup of a work directory, by a person, an agent, or a purge, breaks a resumption or makes it compute everything again (STND.WFLOW.36). Work directories are records only where a record cites them; a temporary item is one that no record cites. An agent that cleans a work directory acts under GUARD.5 and GUARD.6, and STND.DFLT.14 sets no size of bulk action, so the agent enumerates and verifies the scope before it removes anything.

A shared vocabulary of provenance names the entities, activities, and people that produce data, and published profiles record the run of a process and of a workflow in a form that several engines implement (w1, W29 and W30; c3, S3) (STND.WFLOW.37). STND.WFLOW.37 lists the content for one step that the general provision REPRO.4 does not name, the attempt and the reuse key among them. The resumption of a halted workflow by a person rests on the record of STND.WFLOW.38, which w1 reasons from INTPR.12 and INTPR.13 and supports with no source (w1, section on resumption by a person): a resumption that runs the same command again finds a cache, a restart state, and a staging area that each are able to have changed. STND.WFLOW.38 asks for no decision of the human owner (STND.DRAFT.42); where the halt is that of a unit of work at its bound, STND.DFLT.9 already has continuation begin on a recorded decision of the human owner. A clock of the time of day jumps and is slewed, and a monotonic clock is not set (c3, S54); unsynchronized clocks on different nodes put the receipt of a message before its send in traces (c3, S56, a search extract, unverified) (STND.WFLOW.40). A resumption after a change of its code, parameters, or environment is a new workflow run under REPRO.1, and the reuse key of STND.WFLOW.6 decides which outputs of the halted run it reuses (STND.WFLOW.39).

In one study, 74 percent of the R files in about 2,000 replication datasets failed on their first run again in a clean environment, and 56 percent after automatic cleaning (w1, W32); the figures of a study of notebooks differ between its summaries and are unverified (w1, W33). STND.WFLOW.41 runs a workflow from its declared inputs alone, which finds an undeclared input, and QA.9 still has results regenerated by another actor from CSQ1. Tests of climate models require a run restarted from its restart state to match a run without the interruption bit for bit, also at halved numbers of processes and threads (c3, S23) (STND.WFLOW.43); STND.VVUQ.1 gives the tier of the comparison from the differences between the two runs, tier 1 where the restart state is complete and the runs share their numbers of processes. Idempotence is tested by running a step twice, once after a forced end at a varied point (w1, answer 22) (STND.WFLOW.42), and a resumption by halting a workflow run and resuming it (STND.WFLOW.44).

Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, or VV, and applies from CSQ3; work of CSQ4 may omit it. The part of a provision that rests on a row of the table of STND.CLASS.10 applies from the class of that row. The second sentence of STND.WFLOW.12, the first sentence of STND.WFLOW.17, STND.WFLOW.34, and the first sentence of STND.WFLOW.40 rest on DSGN.5, and STND.WFLOW.37, whose two sentences apply together, on REPRO.4, and they apply from CSQ2. The second sentence of STND.WFLOW.15 rests on INTPR.7, and STND.WFLOW.16 and the second sentence of STND.WFLOW.40 on INTPR.8, and they apply from CSQ1. STND.WFLOW.26, STND.WFLOW.28, and STND.WFLOW.35 check data where it enters the run from storage, which the first sentence of DSGN.2 asks in full from CSQ3, and apply from CSQ3; the checking of postconditions that DSGN.2 asks from CSQ1 is not among them. STND.WFLOW.7, STND.WFLOW.19, and STND.WFLOW.23 state what a protocol of shared state uses, and not how its invariants are verified, so they apply from CSQ3. The tests of STND.WFLOW.41 to STND.WFLOW.44 are tests under VV.1, and none of them compares with a reference oracle produced without the implementation that it judges, so they apply from CSQ3. Every other provision and sentence rests on DSGN.1, DSGN.6, DSGN.14, DSGN.16, SIMPL.6, REPRO.1, REPRO.3, REPRO.12, RSRC.1, RSRC.2, RSRC.7, INTPR.9, INTPR.12, or INTPR.13 and on no row, and applies from CSQ3. No provision raises the floor (GOV.11): the completion of jobs and steps, the failures of parts and processes, the exhaustion of resources, and discarded failures are governed by STND.CONC.1, STND.CONC.2, STND.MPI.6, HW.8, STND.CODE.7, and PRIME.4, which already bind at every class.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.MPI | Message Passing Interface standard |
| STND.OMP | OpenMP standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Steps

#### STND.WFLOW.1 Step inputs and outputs declared

Default. Instantiates DSGN.1, DSGN.16.

The declaration of each step SHOULD name each file, dataset, parameter, and tool that the step reads, the computational environment in which it runs, and each output that it writes, by its name or by a stated rule that derives its name (DSGN.1, DSGN.16). Each step SHOULD read and write only what its declaration names and the work area that the workflow gives it (DSGN.16).

#### STND.WFLOW.2 Varying steps under reuse

Default. Instantiates REPRO.3, RSRC.7.

Where the declaration of variation that REPRO.3 asks shows that an output of a step varies between attempts on identical inputs, the workflow description SHOULD state the rule under which the workflow reuses a stored output of that step (REPRO.3, RSRC.7). Where a workflow runs such a step again, it SHOULD also run again each step that depends on an output of that step, directly or through other steps (REPRO.3).

#### STND.WFLOW.3 Step completion checks

Default. Instantiates DSGN.1.

The declaration of each step SHOULD state the checks by which the workflow judges each of its outputs complete: its presence at least, and each property of its size, type, or schema on which a consumer relies (DSGN.1). A workflow SHOULD count a step as completed only on the exit status of its last attempt together with the passing of those checks by each output that the step declares (DSGN.1).

#### STND.WFLOW.4 Effects beyond declared outputs

Default. Instantiates DSGN.16, DSGN.1.

The declaration of each step SHOULD state each effect that the step makes beyond its declared outputs, among them a write to a database or to a remote system, a message, and a submission of further work (DSGN.16). Where a step is able to run more than once in one workflow run, each such effect SHOULD be made under a key unique to that step in that workflow run that the receiving system checks, or by a step that the workflow does not run again (DSGN.1).

#### STND.WFLOW.5 Steps repeatable after interruption

Default. Instantiates DSGN.1, REPRO.3.

After an attempt of a step ends at an arbitrary point, each later attempt of that step SHOULD give the outputs, within the variation that REPRO.3 declares for them, and the effects that a single attempt run to completion gives (DSGN.1, REPRO.3).

### Staleness and reuse

#### STND.WFLOW.6 Staleness rule stated

Default. Instantiates SIMPL.6, RSRC.7, REPRO.1.

The workflow description SHOULD state the rule by which the workflow decides whether a stored output of a step is current, and whether an output that a step produces again unchanged leaves current the steps that consume it (SIMPL.6, RSRC.7). That rule SHOULD decide from a reuse key over the content of each input that the step declares, the code and the parameters of the step, and the identity of its computational environment, and not from the times at which files were modified alone (RSRC.7, REPRO.1).

### Publication and partial outputs

#### STND.WFLOW.7 Outputs published atomically

Default. Instantiates DSGN.15, DSGN.1.

Each step SHOULD write each output under a name that no consumer reads (DSGN.15). After an output passes the checks of its step, the step or the workflow SHOULD give it its final name by one operation that the storage of the output makes atomic (DSGN.1, DSGN.15).

#### STND.WFLOW.8 Outputs durable before completion

Default. Instantiates DSGN.1.

Before a step counts as completed, each of its outputs that a later workflow run reads SHOULD be durable on its storage, the entry of its final name included (DSGN.1).

#### STND.WFLOW.9 Partial outputs distinguished

Default. Instantiates DSGN.1.

The workflow description SHOULD state how a workflow run tells a partial output from a completed output: by the absence of its final name, by a marker of completion that the step writes last, or by the record of completed steps (DSGN.1). Where a file under a final name lacks the evidence of completion that the workflow description states, the workflow SHOULD treat it as a partial output (DSGN.1).

#### STND.WFLOW.10 Distinct output names

Default. Instantiates DSGN.14.

Each final name that a workflow run writes SHOULD belong to exactly one of its steps or parts (DSGN.14). Before the first part of a set starts, the workflow SHOULD confirm that the rule from which the names of the outputs of its parts derive gives distinct names to distinct parts (DSGN.14).

### Retries and attempts

#### STND.WFLOW.11 Retryable failures classified

Default. Instantiates DSGN.1.

The declaration of each step that a workflow retries SHOULD classify the failures of its attempts, by exit status, signal, or reported cause, into those that a retry is able to clear and those that it is not (DSGN.1). A workflow SHOULD retry a step only after a failure that its declaration classifies as one that a retry is able to clear (DSGN.1).

#### STND.WFLOW.12 Bounded retries and backoff

Default. Instantiates DSGN.1, DSGN.5.

Each step that a workflow retries SHOULD have a stated bound on the number of its attempts in one workflow run (DSGN.1). Where the attempts of more than one step or part reach one shared service, the delay before each retry SHOULD grow with the number of the attempt up to a stated cap, and carry a random part (DSGN.5).

#### STND.WFLOW.13 One retrying layer

Default. Instantiates SIMPL.6.

The retries of each step SHOULD be made by exactly one of the layers that run the step, among them the workflow engine, the scheduler, and the step itself, as the workflow description states (SIMPL.6).

#### STND.WFLOW.14 Exhaustion not retried unchanged

Default. Instantiates RSRC.1.

Where an attempt ends on the exhaustion of a resource that its request bounds, each retry of that step SHOULD change the request or the amount of work of the attempt (RSRC.1).

#### STND.WFLOW.15 Retries counted and followed

Default. Instantiates RSRC.2, INTPR.7.

The record of the resource use of each workflow run SHOULD hold the count of retries of each step, by the class of failure that occasioned them (RSRC.2). Each failure of an attempt that a later attempt of the same step clears SHOULD count as an anomaly (INTPR.7).

#### STND.WFLOW.16 Attempt records kept

Default. Instantiates INTPR.8.

The record of each workflow run SHOULD hold, for each attempt of each step, its number, its start and end times, the node on which it ran, its resource request, its exit status or the signal that ended it, the event that ended it, and its log (INTPR.8). Each attempt SHOULD write its record and its log under a name that identifies the attempt, beside those of earlier attempts (INTPR.8).

### Ends of jobs

#### STND.WFLOW.17 Notice and grace stated

Default. Instantiates DSGN.5, SIMPL.6.

For each job that a scheduler is able to end before its work completes, the workflow description SHOULD state the notice of end that the scheduler gives, the processes of the job that receive it, and the grace period, from the configuration of the computing system or from a measurement (DSGN.5). Where a job bounds its work by the time left before the limit on its duration, it SHOULD read that limit from its scheduler at run time (SIMPL.6).

#### STND.WFLOW.18 Response to notice of end

Default. Instantiates DSGN.1, RSRC.1.

Where a notice of end reaches a process of a job, that process SHOULD end at its next safe point with a status that states the notice as the cause (DSGN.1). Where a job answers a notice of end by writing restart state, the time that the write takes in the regime of use SHOULD be less than the grace period (RSRC.1).

#### STND.WFLOW.19 Signal handlers that defer

Default. Instantiates DSGN.15.

Each handler of a signal or of a notice of end SHOULD only record the notice for the main code of its process to act on at a safe point, or call only functions that the platform documents as safe in a handler (DSGN.15).

#### STND.WFLOW.20 Engine records valid after forced end

Default. Instantiates DSGN.14.

Each record of completed steps, cache, and index that a later workflow run reads SHOULD remain valid after a forced end at every point of the run that writes it, without code that runs at that end (DSGN.14).

### Restart state

#### STND.WFLOW.21 Restart state interval

Default. Instantiates RSRC.7.

Each job that writes restart state SHOULD write it at a stated interval, chosen from the measured cost of a write and the rate at which the computing system ends jobs before their work completes (RSRC.7). Where the scheduler of a job gives notice of end, the job SHOULD still write restart state at that interval (RSRC.7).

#### STND.WFLOW.22 Restart state generations

Default. Instantiates DSGN.1.

Each job SHOULD write each generation of its restart state as STND.WFLOW.7 and STND.WFLOW.8 ask of an output, under a name distinct from that of each earlier generation (DSGN.1). Each job SHOULD keep its last valid generation until it has checked the integrity and the completeness of a newer one (DSGN.1).

#### STND.WFLOW.23 Restart state across processes

Default. Instantiates DSGN.15.

Where more than one process writes parts of one generation of restart state, that generation SHOULD count as valid only after each of those processes has written its part and checked it (DSGN.15).

#### STND.WFLOW.24 Restart state contents stated

Default. Instantiates DSGN.14, REPRO.3.

The documentation of each job that writes restart state SHOULD state the state of the computation that the restart state holds, the states of its random streams included, each part of that state that it omits, among them open connections, the contents of accelerator memory, and sessions with external systems, and how a restart restores or reestablishes each omitted part (DSGN.14). That documentation SHOULD state whether a restart at another number of processes or with another division of the computation is admitted (REPRO.3).

#### STND.WFLOW.25 Restart state identity recorded

Default. Instantiates REPRO.1.

Each generation of restart state SHOULD record a checksum of its content and the identity of the run that wrote it: its inputs, its parameters, the revision of its code, and its number of processes (REPRO.1).

#### STND.WFLOW.26 Restart state checked before use

Default. Instantiates DSGN.2.

Before a job continues from a generation of restart state, it SHOULD check the integrity, the completeness, and the format version of that generation, and that the identity that the generation records matches the present run in each item on which the continued computation depends (DSGN.2). Where at least one of those checks fails, the job SHOULD NOT continue from that generation (DSGN.2).

#### STND.WFLOW.27 Restart state format versions

Default. Instantiates DSGN.6.

Each generation of restart state SHOULD carry the version of its format (DSGN.6). Each revision of the code of a job SHOULD read each format version written by a run that is still able to be resumed, or refuse it with a report that names the version (DSGN.6).

#### STND.WFLOW.28 Restart state that executes code

Default. Instantiates DSGN.2.

Where loading restart state executes code that the restart state holds, the job SHOULD load only restart state that lies on storage that the run controls and whose content matches a digest that the run recorded apart from it (DSGN.2).

### Sets of parts

#### STND.WFLOW.29 Completed parts from checked outputs

Default. Instantiates DSGN.1, RSRC.7.

A workflow SHOULD decide the completed parts of each set of parts from their checked outputs, and not from the records of the scheduler alone (DSGN.1). After a failure of parts, a rerun of the set SHOULD run only the parts that are not completed (RSRC.7).

#### STND.WFLOW.30 Consumers of parts state needs

Default. Instantiates DSGN.1, INTPR.9.

The declaration of each step that consumes the outputs of a set of parts SHOULD state whether it requires every part, a stated number of parts, or a stated subset (DSGN.1). Where such a step proceeds without every part, the record of its result SHOULD name each missing part (INTPR.9).

#### STND.WFLOW.31 Parts bounded by shared limits

Default. Instantiates RSRC.1.

Where the parts of a set use a shared resource with a limit, among them the service of a file system that holds the names of its files, a license, and a network service, the number of those parts that run at once SHOULD have a stated bound set from that limit (RSRC.1).

### Storage and work directories

#### STND.WFLOW.32 Storage in the run budget

Default. Instantiates RSRC.1.

The budget of each workflow SHOULD state, for each file system on which a workflow run writes, the space and the number of files and directories that the run occupies at its largest, at the problem size of the budget (RSRC.1). Before a workflow run starts its first step, it SHOULD check that the free space and the quotas of space and of files on each such file system meet that budget (RSRC.1).

#### STND.WFLOW.33 Storage purged by policy

Default. Instantiates REPRO.12.

Where a file system removes files by age or by another policy of its site, each result, record, and restart state that a later run or a relying party needs beyond the period of that policy SHOULD be kept on other storage (REPRO.12).

#### STND.WFLOW.34 File system guarantees relied upon

Default. Instantiates DSGN.5.

Where steps or processes of a workflow share a file or a directory, the workflow description SHOULD state each guarantee of the file system on which that sharing relies, among them the consistency of reads on one node after writes on another, the enforcement of locks, atomic appends, and atomic renames, and the evidence that the file system in use provides each such guarantee (DSGN.5). Where a file system in use does not give a guarantee on which a sharing relies, the workflow SHOULD move that sharing to storage that gives it, or to a protocol that does not rely on it (DSGN.5).

#### STND.WFLOW.35 Staged copies verified

Default. Instantiates DSGN.2.

Before a consumer reads a copy of data that a step makes from one storage system to another, the step SHOULD confirm the copy against its source by a checksum, or by a check of the transfer that covers its content (DSGN.2).

#### STND.WFLOW.36 Work directory state stated

Default. Instantiates DSGN.14.

The workflow description SHOULD state each location in which the workflow keeps state on which a later workflow run relies, among them its caches, its records of completed steps, its restart state, and the work areas of its steps, with the lifetime of that state and the items of it that are temporary items (DSGN.14). Each cleanup that the workflow engine or a scheduled task makes in such a location SHOULD remove only the items that the workflow description states as temporary items (DSGN.14).

### Records and resumption

#### STND.WFLOW.37 Provenance of step outputs

Default. Instantiates REPRO.4, REPRO.1, REPRO.12, INTPR.9.

The provenance that REPRO.4 asks of each output of a step SHOULD give the reuse key and the identity of the content of each input, the revision of the code of the step, its parameters, the identity of its computational environment, its resource request, the attempt that wrote it, and its start and end times (REPRO.4, REPRO.1). That provenance SHOULD be readable by a human without the workflow engine (REPRO.12, INTPR.9).

#### STND.WFLOW.38 Resumption record

Default. Instantiates INTPR.12, INTPR.13.

The record of each workflow run SHOULD state, in a form that an actor reads without the workflow engine, each step completed with its checked outputs, each failed step with its attempts and their causes, the latest generation of restart state on durable storage, each effect beyond declared outputs already made, and the steps that a resumption runs again (INTPR.12, INTPR.13).

#### STND.WFLOW.39 Resumption after a change

Default. Instantiates REPRO.1.

Where the code, the parameters, or the computational environment of a workflow changes between a halt and a resumption, the record of the resumed workflow run SHOULD state each change and cite the halted workflow run (REPRO.1).

#### STND.WFLOW.40 Clocks in workflow records

Default. Instantiates DSGN.5, INTPR.8.

Each duration that a workflow measures, among them the bounds of waits and the delays of retries, SHOULD be measured by a clock that the system does not set or step (DSGN.5). The record of a workflow run SHOULD order events on different nodes by sequence numbers or by the dependences between steps, and not by a comparison of the clocks of those nodes (INTPR.8).

### Tests

#### STND.WFLOW.41 Workflow run from a clean area

Default. Instantiates VV.1.

The tests of each workflow SHOULD include a workflow run from its declared inputs alone, on a work directory that holds nothing from an earlier workflow run (VV.1).

#### STND.WFLOW.42 Interrupted attempts under test

Default. Instantiates VV.1.

The tests of each step that a workflow retries, or that a scheduler is able to start again, SHOULD run it after an attempt ended by a forced end at a point that the tests vary, and compare its outputs and effects with those of a single attempt run to completion (VV.1).

#### STND.WFLOW.43 Restarts under test

Default. Instantiates VV.1, REPRO.3.

The tests of each job that writes restart state SHOULD end a run after a generation is written, continue it from that generation, and compare its results with those of a run without the interruption at the tier that STND.VVUQ.1 gives for the differences between the two runs (VV.1, REPRO.3). Where the job admits a restart at another number of processes, its tests SHOULD also continue a run at such a number (VV.1).

#### STND.WFLOW.44 Resumption under test

Default. Instantiates VV.1.

The tests of each workflow SHOULD include a workflow run that halts after a stated set of its steps and a resumption of it, and show that the resumption runs again only the steps that its staleness rule finds not current, and that its results agree with those of a workflow run without the halt (VV.1).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
