Role: research agent (note W1). Accessed 2026-10-24. Rules followed: read-only; about 52 retrieval calls (40 page fetches, 8 web searches, 4 failed or redirected) and an estimated 3 MB, inside the 1,500-item and 1,500 MB budget; no paywall touched; failed fetches (HTTP 429 on several GNU make manual pages, 404 on two documentation pages, 403 on one) were not worked around, and no mirror, cache, or archive was used; no credentials; retrieved text treated as data.

# Computational workflows and the resilience of long-running work

## Method caveat

The fetch tool returns a model-written extract of a page, not its text. Every quote below from a web page is therefore an extract and may be a paraphrase. One PDF (Build Systems a la Carte, W14) was saved and searched as full text locally. Several pages were truncated by the tool (Snakemake rules, Slurm configuration, CWL, Kubernetes Job); where an extract said a topic was absent from the portion read, I did not fill the gap from memory, and the item is marked [unverified]. Rows resting on search-result text only are marked "search extract". The GNU make manual could not be read (rate limit), so Make behavior on interrupt and on error rests on no retrieved text. Product names appear only as evidence of a hazard. I did not repeat what `research/concurrency-notes/c3-distributed-resilience.md` (below, C3) holds; I cite it as [C3 n] with its answer-in-brief number or its section.

## What C3 already covers (not repeated)

Retries and duplicate execution as the default of engines, with idempotency keys (C3 answer 1, section 1); success as verified completion, atomic publish by temporary name, rename, and directory sync (C3 answer 2, S37, S38, S42); cache keys over code, parameters, input content, and environment, and the unreliability of mtimes on network storage (C3 answer 3; S10 to S13); deterministic pairing (C3 answer 4); provenance of runs (C3 answer 5; S1, S3); explicit resource limits (C3 answer 6); unanimous-success checkpoints, restart tests, interval formula, silent data corruption (C3 answers 7, 8; S18 to S23, S25); advisory locks, NFS, SQLite, HDF5 SWMR (C3 answer 10); monotonic clocks (C3 answer 11). This note adds the layer between those: the step contract, what a kill leaves behind, the order of signals, how retry policy fails, what a checkpoint file needs on restart, arrays, storage limits, and the human who resumes.

## Answer in brief

1. A step declares every input it reads and every output it writes, and a step that reads or writes an undeclared path is a defect of the workflow, because incremental execution, caching, and cleanup all trust the declaration. A step is hermetic when its output depends on its declared inputs alone. [W1, W2, W3, W7, W14, W15]
2. A step writes its outputs to a name that no consumer reads (a temporary name or a private directory on the same file system as the final name), verifies them, and only then renames them into place. A cross-file-system "rename" is a copy and is not atomic. [W9, W10, W11, C3 S37, S38]
3. A step that a kill interrupts leaves its partial outputs where they cannot be mistaken for results: the engine or the step removes them, or they carry no final name. The next run does not treat the presence of a file as proof of completion. [W2, W3, W14, W17]
4. A zero exit status does not establish completion. Each step checks its declared outputs (existence, nonempty where required, type or schema, and an integrity check where the data are large) before it reports success. [W1, W2, W4; C3 S12]
5. Incremental re-execution decides staleness from content and the full description of the step, not from modification times alone. Timestamps are an approximation that fails under restored backups, copies that preserve times, clock skew, and shared file systems. [W14, W15, W3; C3 S11]
6. A step that is not deterministic (time, random draws, network, directory listing order, parallel completion order) declares it, and its cached result is reused only under a rule the workflow states. Re-running a nondeterministic step in a cached chain can make downstream results disagree with each other. [W15, W16, W7]
7. Retries are bounded in count, spaced by backoff with jitter, applied at one layer of the stack, and classified: a failure known to be permanent (invalid input, a failed validation) is not retried, and a failure known to be a resource kill is not retried unchanged. [W5, W6, W4, W18]
8. A retry never overwrites the record of the failed attempt: attempt number, exit status or signal, node, and logs of every attempt are kept. A requeue that truncates the earlier log erases the evidence. [W8, W10; C3 S14]
9. A long job learns of its end before it comes: the scheduler's warning signal or notice is requested, a handler does only what is safe in a handler (set a flag), and the main thread writes a checkpoint at a safe point and exits with a status that says why. The signal that cannot be caught is assumed to follow. [W8, W9, W12, W13]
10. The time from warning to kill is a measured, configured quantity of the site, not an assumption. A checkpoint that takes longer than that time is not a response to the warning. [W8, W12, W13]
11. Preemption, wall-time limit, memory kill, node failure, and quota exhaustion are distinct events with distinct handling, and the record of the run names which one ended it. A kill by the operating system for memory may leave the rest of the step running with corrupted assumptions. [W8, W11, W19]
12. An application-level checkpoint is written to a temporary name, flushed, verified, then renamed, and the previous valid checkpoint is kept until the new one is verified. A checkpoint that was observed while still being written is truncated on restart. [W20, W21, C3 answer 7]
13. A restart validates the checkpoint before using it: a format version, a code or schema identifier, a size and checksum, and the run identity (inputs and parameters) it belongs to. A checkpoint whose identity differs from the present run is refused, not silently loaded. [W20, W21, W22]
14. A checkpoint format is versioned and readable by the code that follows it for as long as runs that write it can be resumed; a checkpoint is not a long-term archive format, and a checkpoint that executes code on load (a serialized object graph) is trusted only from the run's own storage. [W22, W23]
15. A failure of one part of a job array or a fan-out is recorded per part and does not hide in an aggregate: the set of completed parts is derived from verified outputs, and a rerun executes only the missing parts. [W24, W25]
16. A job array is throttled to the capacity of the shared resource it touches (file system metadata, license, network), and the shared output location of an array has a unique name per part. [W24, W26]
17. Storage is a declared input of a workflow: space and file count (inodes) are estimated before the run, checked at stated points, and the exhaustion of either is a recorded failure. Scratch space that is purged by age is not a place for results or for a checkpoint that a later run needs. [W26, W27, W28]
18. Data staging is a step: it has declared inputs and outputs, verifies what it moved (size, checksum), and is repeatable. A file that was staged and then changed at the source is detected, not assumed unchanged. [W2, W26]
19. Provenance is written by the step at production: input identities (content hashes), code revision, parameters, environment identity, resource request, attempt number, and times. Provenance that the workflow engine reconstructs afterward is labeled so. [W29, W30, W31, REPRO.4]
20. A workflow run is reproducible when the same recorded inputs, run again in a fresh checkout and an equivalent environment, give outputs identical or within a stated tolerance; the claim is tested by running it, because most archived analyses fail when first rerun. [W32, W33, W31]
21. A human resumes a halted workflow from the records, not from memory: the record says which steps completed with which outputs, which failed and why, what state the external world is in, and what decision a person has to make. Resumption starts with a decision, not with the same command. [W2, W8, W25; STND.DFLT.9]
22. Idempotence is tested: a step is run twice on the same inputs, once with a kill at a random point, and the outputs and the effects are compared. [W5, W16, W34]

## Hazard tables

### Declared inputs, outputs, and incremental execution

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Undeclared dependency | A build is hermetic when it depends on specific tool and library versions; the listed sources of nondeterminism include system binaries that vary across hosts and writing to the source tree during the build. | A step reads a file or tool it never declared; a change there triggers no rerun, or the step behaves differently on another host. | Declare inputs, tools, and output locations; forbid writes outside the step's output area. | W15 | Holds in every engine; the mechanism of enforcement is specific |
| Timestamp staleness | Make-style systems use file modification times as a dirty bit; they "require that file timestamps only go forward in time, which can be violated by backup software"; the system is minimal only if no one alters a time without changing content. | An old file restored with an old time hides a changed input; a touched file forces needless work. | Decide staleness from content hashes or recorded traces of inputs and recipe; use times only as a cheap first filter. | W14 | Holds across implementations |
| Cache key omits environment | Nextflow keys a task on input path, timestamp and size, script, container or environment, and session; shared file systems can report unstable timestamps. | Cache hit after the tool changed, or miss after an NFS timestamp wobble. | Key on content and on the environment identity; record the key. | W3; C3 S11 | Specific in detail; the class holds |
| Early cutoff absent | Build systems with early cutoff stop when a rebuilt intermediate is unchanged; Make cannot mark a file clean without marking dependents dirty. | A comment change in a source reruns hours of downstream steps, or the operator avoids rebuilding and keeps stale results. | Choose whether the workflow compares content of intermediates; state the choice. | W14 | Holds across implementations |
| Nondeterministic input pairing | Joining channels without matching keys gives inconsistent inputs; an undeclared closure variable is global and races. | Same inputs, different pairings, results that cannot be reproduced. | Key every merge; no shared mutable variable across tasks. | W3; C3 S11 | Specific to dataflow engines; the class (unordered completion) holds |
| Output checks not declared | CWL requires declared inputs and outputs, validates the output object against the schema, and treats only exit code 0 as success unless `successCodes` says otherwise; Snakemake's `ensure` checks annotated files before success and fails the job on an unexpected empty file. | A step that exits zero with empty or wrong output is accepted, and the error appears three steps later. | Declare output checks per step; failure of a check fails the step. | W4, W2 | Specific in syntax; practice holds |
| Cache reuse across code change | Parsl: code changes do not invalidate cached values (C3 S10). Snakemake hashes code, parameters, inputs, environment (C3 S13). | One engine reuses a result after the code changed; another does not. | Treat the key's contents as part of the workflow contract and record them. | C3 S10, S13 | Specific to engine |

### Atomicity, partial outputs, and kills

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Rename across file systems | `rename` replaces a target atomically; it fails with EXDEV when the paths are not on the same mounted file system, even for one file system mounted twice. | The "move into place" becomes a copy, visible half-written, or the step falls back to a copy without noticing. | Write the temporary file in the destination directory; treat EXDEV as a defect, not a cue to copy. | W10 | Holds on POSIX systems |
| Directory entry not durable | `fsync` of a file "does not necessarily ensure that the entry in the directory" has reached disk; an fsync of the directory is also needed. | After a crash the renamed file is absent or the old one returns. | Sync the file, rename, sync the directory, as in C3 answer 2. | W9; C3 S37 | Holds on POSIX systems |
| Partial output after a kill | Snakemake shadow directories are cleared on success, and `--keep-incomplete` keeps those of failed jobs; log files "are not deleted upon error". | A killed step leaves a final-named file that a later run takes for a result; or leaves a shadow directory that fills the disk. | Write in a private directory; publish by rename; give the next run a rule that distrusts a final name without a completion marker. | W2 | Specific in names; class holds |
| Delete on error not default | Whether Make deletes a target after a failed recipe is controlled by a special target and by interrupt handling [unverified, page not read]. | A truncated target is newer than its inputs, so the next run treats it as current. | State the rule for partial targets; do not depend on a default. | none read | Specific [unverified] |
| Presence as completion | Pegasus detects failure by non-zero exit code, parsed output, timeouts, and missing expected output files (search extract). | A step that must check that an output exists and is whole has only the first test. | Test existence and integrity, as the engine's failure detectors do. | W35 (search extract) | Specific to engine |
| Publish collisions | Nextflow `publishDir` lets the last finishing task overwrite a same-named file at the target. | Two tasks (or two retries) write one published name; the result depends on completion order. | Give each part a unique output name; never publish two attempts to one name. | W3 | Specific to engine; class holds |
| Non-idempotent task | Airflow says tasks "should produce the same outcome on every re-run", advises UPSERT in place of INSERT, warns that storing a file on local disk makes retries harder, and says an input that changes between reruns changes outputs. | A retry duplicates rows or reads moved input. | Write results keyed by the partition or the logical run; read a named version of the input. | W5 | Specific to the example; class holds |

### Retries, backoff, and their limits

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Unbounded or immediate retry | Retries should wait between tries; exponential backoff with a cap is the common pattern, and jitter spreads retries so failed calls do not collide again. | A shared service that is down is hit by every client at once on every interval. | Bound the count, cap the delay, add jitter. | W6 | Holds |
| Retry amplification across layers | Three retries at each of five layers multiply load on a failing database by 243; the chapter on cascading failures proposes a per-request limit and a server-wide retry budget. | One failure becomes dozens of attempts at the bottom; the retry storm keeps the failure alive. | Retry at one layer; keep a retry budget; the engine and the script do not both retry. | W6, W18 | Holds; the numbers are examples |
| Retry of a permanent failure | Nextflow retries on a user-chosen set of exit codes and ends the run otherwise; CWL separates temporary-fail, permanent-fail, and success codes. | A bad input is retried to the limit and the queue wastes hours. | Classify exit statuses by retryability in the workflow description. | W3, W4 | Specific in syntax |
| Retry of a resource kill unchanged | The Nextflow example retries on the status range 137 to 140 and "re-executes" the task; the page does not say the codes mean resource kills [unverified]. A cgroup out-of-memory event kills "one or more of the processes in the step" and marks the step OOM while the step may keep running. | The same request runs out of memory again; or the step continues with a dead helper process and produces a wrong result. | Retry a resource kill only with a changed request or a changed size of work, and treat a partial kill of a step as a failure of the step. | W3, W19 | Specific; the class holds |
| Heisenbug assumption | Gray's report conjectured that most production software faults are transient, so restart and retry mask them; later work argues rare deterministic faults cause much of the downtime (search extract). | Retry hides a deterministic defect for a long time, then the defect appears at scale. | Count and report retries that succeed; a step that needs retries repeatedly is investigated (INTPR.7). | W36 (search extract) | Holds |
| At-least-once semantics | A Kubernetes Job continues to retry the pod until the required number succeed; that a task can run more than once, for example when a pod is evicted after finishing but before the controller records it, comes from general knowledge, not from the page read [unverified]. | A completed task is run again and its external effect is repeated. | Commit the external effect under a unique key (C3 S15). | W37; C3 S15 | Specific to the engine; class holds |
| Requeue restarts the script | A requeued batch script starts again from the beginning with the same job ID; output files open by append or truncate by a configured default. | The second run truncates the first run's log, or appends to it without a separator; a script that assumes a clean directory fails. | Make the script resumable at its start: detect the existing state and continue; name logs per attempt. | W8; C3 S14 | Specific to scheduler; the class holds |

### Signals, preemption, wall-time limits

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Warning signals sent before the kill | Slurm sends SIGCONT and SIGTERM at once to a job selected for preemption, then SIGKILL at the new end time; `KillWait` is the interval between SIGTERM and SIGKILL at a time limit, default 30 s; GraceTime defaults to zero; `--signal` sends a chosen signal a stated number of seconds before the end, to all steps unless the batch shell is named. | A job that expects a long grace sees none; a signal goes to the steps but not to the batch script, so the script's handler never runs. | Request the signal, name its target, and measure the interval; state in the workflow what the job does with it. | W8, W12, W38 | Specific to scheduler; defaults are site-set |
| Uncatchable kill | SIGKILL and SIGSTOP "cannot be caught, blocked, or ignored"; SIGTERM defaults to terminate. | Cleanup code that runs only on a signal never runs on the kill. | Design for the kill: the state on disk is valid at every instant (publish by rename); the handler is an optimization. | W9, W12 | Holds on POSIX systems |
| Unsafe work in a handler | A handler can interrupt a non-reentrant function; calling it again "will operate on inconsistent data"; the page offers async-signal-safe functions or blocking signals. | A handler that writes a checkpoint or logs through stdio corrupts memory or deadlocks. | The handler sets a flag; the main loop checks it at a safe point and writes. | W13 | Holds on POSIX systems |
| Interrupted calls | A blocked call interrupted by a handler restarts only with the restart flag; some calls always fail with EINTR. | A write to the checkpoint short-writes or fails during shutdown without a check. | Check the return of every write in the shutdown path (STND.CONC.1). | W12 | Holds on POSIX systems |
| Warning is not guaranteed | A cloud spot-capacity notice is issued two minutes ahead on a best-effort basis, delivered through instance metadata and an event, and the vendor recommends polling it every 5 seconds; hibernation gives no two-minute warning. | A job that relies on the notice loses the work done since the last checkpoint. | Checkpoint at a regular interval anyway; use the notice to reduce loss, not to replace the interval. | W39 | Specific to provider; the class holds |
| Container shutdown | A pod gets SIGTERM, then SIGKILL when the grace period (30 s by default) ends, counted from deletion and including the pre-stop hook [from an extract that said it summarized general knowledge; unverified against the page]. | Same as above for containerized steps. | State the grace period in the workflow. | W40 | Specific [unverified] |
| Time limit with soft overrun | `OverTimeLimit` treats the limit as soft for a stated number of minutes, default zero. | A job that counts on slack that the site did not configure. | Read the limit from the environment of the job, not a constant. | W38 | Specific to scheduler |
| Memory kill that leaves the step | With `ConstrainRAMSpace` the kernel kills processes in the step and the step "will keep running". | A parallel step continues with a missing rank or worker. | Treat a worker's death as a failure of the step (STND.CONC.2, STND.MPI.6). | W19 | Specific to configuration |

### Checkpoint and restart

C3 holds the all-agree commit, the restart test, the interval, and the climate-model practice. The rows below add what a restart finds.

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Checkpoint observed while incomplete | A maintainer of a checkpoint library replied to a user whose earlier checkpoints failed with I/O errors that the error indicates truncation, "a checkpoint has likely been taken that observed the length of the open context file while it was still incomplete" (2009 list thread). | The newest checkpoint is bad, and so are the earlier ones that shared a file. | One file per generation; never overwrite the only good one; verify before retiring the old. | W20 (list thread) | Specific to the case; the class holds |
| Restart finds invalid metadata | The restart tool of an MPI implementation reports that a local checkpoint has invalid or incomplete metadata, which "usually indicates that the original checkpoint was invalid"; a CFD code reports a premature end of file on restart although the log showed the files written; a hydrodynamics code defines an error for a restart file that was not found or was incomplete and advises checking that the preceding run finished. | The failure appears at the start of the next run, possibly days after the write. | Validate at write (read back, checksum) and at read; write the completion marker last. | W20, W41 (search extracts) | Specific products; the class holds |
| Library holds the checkpoint | SCR does not load a checkpoint "marked as being incomplete"; a parallel file system outage during the final write can leave nothing to scavenge; by default a checkpoint is flushed to the parallel file system after every tenth checkpoint, not every one. | Only the latest cached checkpoints exist when the node set is lost. | Know which generation is on durable storage; record it. | W21 | Specific to the library |
| Transparent checkpointing limits | DMTCP checkpoints a single-host or distributed computation in user space without changing user code; its page names version incompatibilities with an MPI implementation and overhead of mutex wrappers; what cannot be checkpointed was not in the extract. | A checkpoint taken of a process that holds an external connection or an accelerator context restarts into a state that no longer matches the world. | State what the checkpoint excludes (open sockets, accelerator memory, external sessions) and test a restart in a fresh environment. | W42 | Specific [unverified for limits] |
| Checkpoint identity | A restart that loads a file from another run's inputs or a changed code revision continues a different computation. Climate-model restart tests compare a restarted run to a straight run (C3 S23). No source read states a general rule on identity. | A checkpoint from run A resumes run B and produces a plausible, wrong result. | Store the run identity (inputs, parameters, code revision, process count) in the checkpoint and compare on restart. | C3 S23; reasoning | Argued, not sourced |
| Format versioning | Pickle protocols: a higher protocol needs a recent interpreter; the format is "backwards compatible across Python releases provided a compatible pickle protocol is chosen"; default protocol changes across releases. | A checkpoint written after an upgrade cannot be read by the code that must resume the job on the older environment, or the reverse. | Write an explicit format version; keep a reader for each version a resumable run could have written, or declare checkpoints unresumable across a version. | W22 | Specific to the example; class holds |
| Checkpoint that runs code | "The `pickle` module is not secure": malicious data can execute arbitrary code when unpickled; the page recommends signing with a keyed hash to detect tampering. | A checkpoint taken from shared or purged-and-restored storage executes foreign code. | Load checkpoints only from storage the run controls; record a checksum with the run (see GUARD and security provisions for the rest). | W22 | Holds for any format that deserializes objects |
| Restart at changed scale | C3 S23 holds the test at halved counts. | The checkpoint depends on the number of ranks or the decomposition. | State whether the checkpoint is portable across process counts (STND.MPI.22). | C3 S23 | Specific |

### Arrays, fan-out, and the failure of a part

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Aggregate dependency | A Slurm dependency `afterok` on an array waits for all tasks to complete successfully; `afternotok` is satisfied after the array completes with at least one task not successful. | One failed task blocks everything downstream or is detected only after the whole array ends. | Collect per-task status; let downstream steps declare whether they need all parts, a quorum, or a stated subset. | W24 | Specific to scheduler; class holds |
| Order not guaranteed | Array tasks are not ordered; requeued tasks can be created out of order; a requeue can name one element. | A script that depends on order, or on task 0 running first, fails intermittently. | A part depends only on its declared inputs. | W24 | Specific to scheduler |
| Throttle | `--array=0-15%4` caps the tasks running at once; the default maximum array size is 1001, configurable. | A thousand tasks open one shared file or one license at once. | Set the throttle from the capacity of the shared resource, and state it. | W24 | Specific; default is site-set |
| One part's output overwrites another's | Task identity is an index in the environment of the task. | Two parts write one name. | Derive every output name from the part's identity; check uniqueness before submit. | W24, W3 | Holds |
| Rerun of the whole | Rerunning only the failed indices needs the set of completed ones. | The operator reruns all, or a wrong subset. | Derive the missing set from verified outputs, not from scheduler logs alone (scheduler records age out: `MinJobAge` defaults to 300 s in memory). | W38 | Specific to scheduler |
| Node failure | By default Slurm terminates the whole allocation if one node fails; `--no-kill` keeps it. | The whole job is lost for one node; or the job continues without the lost node and its share of work. | Choose and state which, per step type (STND.MPI.6). | W8 | Specific to scheduler |
| Interconnect recovery | A study of one machine found that applications running during an unsuccessful interconnect failover failed at 20% (search extract: "20% versus 0.2%" for successful recoveries). | A recovery procedure is itself a hazard for the jobs it protects. | Treat jobs that overlapped a recovery event as suspect for the record. | W43 (search extract) | Specific to the machine |

### Storage, staging, and quotas

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Purge by age | One center's scratch policy: "Any file not accessed within 8 weeks is subject to deletion"; purge candidates are listed in a file, which "isn't comprehensive". | A checkpoint or intermediate waits in scratch for a human decision and is gone; a resumed workflow finds the cache record but not the file. | Treat scratch as a cache that can vanish; the workflow detects a missing intermediate and regenerates or fails with a clear message; results go to storage without a purge rule. | W27 | Specific to site; the class holds |
| Quota exceeded | "If your scratch usage exceeds your quota, you will not be able to write to the file system until you reduce your usage"; jobs can still be submitted; a separate inode quota limits files and directories; a grace overage of 10 TB for 24 hours exists on one system. | A job starts, runs for hours, and fails at its first checkpoint; or writes fail with an error that a step does not check. | Check free space and inodes at start and before each large write; check every write's return; report quota as a cause. | W26, W28 | Specific to site; the class holds |
| Quota enforced in chunks | In one parallel file system's design (2008 to 2009 decks), quota is granted to storage targets in chunks, so one target can return EDQUOT while the user is far from the limit and other targets still accept writes; the sources are old and current releases were not checked. | A write fails with "quota exceeded" at a total far below the limit; striping decides whether a given file fails. | Treat EDQUOT as possible below the limit; do not retry blindly. | W44 (search extract) | Specific; version not checked |
| Many small files | Inode quota counts every file and directory; the step directory model of an engine creates a directory per task. | A workflow of a million tasks exhausts the file count first. | Estimate file count as well as bytes; bundle small outputs. | W28, W3 | Holds |
| Work directory is state | Nextflow says it is important to preserve both the task cache and the work directories to resume; deleting either re-executes tasks. | A cleanup (including an automated purge) breaks resumption, or resumption silently recomputes at full cost. | Record where the state lives and who may delete it (see cleanup rules of the custodian: archive first). | W45 | Specific to engine; the class holds |
| Staged data change | Airflow notes that an input updated between reruns changes the outputs. | A rerun reads a different input and no step noticed. | Stage by version or hash, and record the hash. | W5 | Holds |

### Provenance and reproduction

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Provenance model | W3C PROV gives a shared vocabulary for "entities, activities, and people involved in producing a piece of data", with serializations and constraint checking; Workflow Run RO-Crate profiles record a process run (Process Run Crate), a workflow run, and the provenance of the execution, implemented by several engines (also C3 S3). | Each engine records differently; a result moved between sites loses its origin. | Record a minimum set (inputs by hash, code revision, parameters, environment, resource request, attempts, times) in a form readable without the engine (REPRO.12, INTPR.9). | W29, W30; C3 S3 | Holds; formats are specific |
| Reconstructed provenance | REPRO.4 already labels reconstructed provenance. | Provenance guessed from logs after the fact looks the same as recorded. | Label it. | REPRO.4 | Holds |
| Build reproducibility definition | A build is reproducible if, with the same source, build environment, and instructions, "any party can recreate bit-by-bit identical copies"; the environment record is "dependencies and their versions, build configuration flags and environment variables"; verification is by comparison of hashes. A hermetic build "always produces the same output for the same inputs". | A workflow claims reproducibility that no one checked. | Reproduce by an independent run and compare; bitwise or within the stated tolerance (REPRO.3). | W15, W46 | Holds for builds; for numerical work, the tolerance applies |
| Addressing by input or by content | Nix computes an input-addressed output's path from the derivation, so a change to a fetch URL changes the path of every dependent; a content-addressed path depends on the output's data, and the manual describes the first as massive rebuilds for a change with no real effect. | The choice decides when a cache hits: addressing by input recomputes, by content stops early. | State which the workflow uses; both need a deterministic step to be sound. | W47 (search extract) | Holds |
| Archived code does not run | 74% of R files in about 2,000 replication datasets crashed on the first re-execution in a clean environment (56% after automatic cleaning); a notebook study found that most notebooks could not be rerun and few reproduced results (24.1% ran and 4% reproduced in one summary; the figures differ between summaries; check before citing); main causes were missing dependencies, hidden state and out-of-order execution, and data access. | Provenance exists, but the environment and the data do not. | Test reproduction on a clean environment on a schedule that the project sets. | W32, W33 | Holds |
| Hidden state in interactive steps | Notebook hidden state and out-of-order execution. | An interactive step is a manual step with no record. | A workflow step is a script run in order from declared inputs (REPRO.10). | W33 | Holds |

### Failure studies

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| System failure rates | A study of LANL data (about 23,000 failures, more than 20 systems): more than half of failures hardware, about 20% software, rates from 20 to 1,000 failures per year per system, Weibull time between failures (search extract). | Assuming exponential failures, or no failures, in the estimate of a long run. | Plan long runs on the measured rate of the system in use, and record it (RSRC.1). | W48 (search extract) | Specific to the 2006 systems; the class holds |
| Failures in workflows at scale | A 2012 failure analysis of workflows on a cloud found failure modeling feasible and failures common as tasks number in the hundreds of thousands (search extract). Pegasus provides retries and a rescue graph for restart (search extract). | Failure is the normal case of a large workflow. | Design for a rescue: the workflow can be restarted from its completed set. | W35 (search extract) | Specific to the system; class holds |
| Failure is not reported | CWL, Snakemake, and Nextflow treat exit status as the unit of failure, so a step that fails to report fails silently. | A wrong result with status 0. | Output checks (practice 4). | W2, W3, W4 | Holds |

I found no study of workflow-level failure causes in HPC with a taxonomy that I could read; see "Not verified".

## Human-in-the-loop resumption

The sources say little about the human beyond these facts: a Snakemake rerun uses a flag for incomplete outputs (C3 S12, S17); a Nextflow resume depends on a session identity and on preserved work directories (W45); a requeued Slurm job restarts the script with the same job ID (W8); Pegasus offers a rescue graph (W35). The remaining practice is reasoned from the corpus rather than from sources:

- The state a person needs is in the artifacts (INTPR.12, INTPR.13): the list of completed steps with verified outputs, the failed step with its attempt records, the checkpoint generation, the resources that the run held, and the external effects already committed.
- A resumption after a halt on repeated failure is a decision (STND.DFLT.9), and the record gives the decision-maker the cause, what was changed, and what a rerun will recompute and cost (RSRC.7).
- A resumption never reuses the same command blindly: the cache, the checkpoint, and the staging area may each have changed since the halt.
- A resumption that changes the code, parameters, or environment is a new run that cites the old one (REPRO.1).

## What the corpus already holds

| Matter | Provisions | Note for the drafter |
| --- | --- | --- |
| Recorded inputs, environment, determinism | REPRO.1, REPRO.2, REPRO.3 | Cover the key of a cache and the claim of reproduction; restate nothing. |
| Provenance written at production; reconstructed provenance labeled | REPRO.4 | Covers the provenance practice (19) in general; a workflow standard names only the per-step content and the attempt record. |
| A workflow is a versioned, reviewed, reproducible artifact; manual steps | REPRO.10 | Covers the workflow description itself. |
| Agent steps recorded as a workflow | REPRO.11 | Covers an agent's work as a workflow; attempts and actions. |
| Retention and readability without the tool | REPRO.12 | Covers records and results; the work directory as state is not named. |
| Operator can learn state and progress; anomalies; diagnostics captured by default | INTPR.6, INTPR.7, INTPR.8 | Cover reporting, stalled progress, resource trends, and the information needed after a failure. |
| Human can resume without automation | INTPR.12, INTPR.13 | Cover human-in-the-loop resumption in general. |
| Self-describing outputs | INTPR.9 | Covers output description; a checkpoint is not an output in this sense unless it is read by another run. |
| Halt, degrade visibly, or safe state on a hardware fault or exhaustion; results across hardware events recorded | HW.8, HW.9 | Cover quota exhaustion only where the capacity is hardware; storage quota is a policy limit, so its treatment is open. |
| Undetected faults | HW.10 | Covers end-to-end checks on results where the hardware contract says a fault goes undetected. |
| Completion of asynchronous operations observed; failures reach the parent | STND.CONC.1, STND.CONC.2 | Cover the check of a step's completion and the halt of dependent tasks. |
| Bounded waits; parent-owned tasks; cancellation; bounded queues; pending operations recorded | STND.CONC.10 to STND.CONC.14, STND.CONC.29 | Cover cancellation, time bounds, and the record of work pending at the end of a run (a step in flight at a kill). The workflow level adds the on-disk state. |
| Execution-wide halt, ended executions observed, error answers | STND.MPI.5, STND.MPI.6, STND.MPI.7 | Cover the halt of a multi-process job and a run time bound where an ended process may not end the others. |
| Shared file protocol; portable representation; process-count dependence | STND.MPI.21, STND.MPI.22 | Cover files written through MPI; checkpoint files not written that way are open. |
| Budgets and their record; reuse or recompute on measured cost | RSRC.1, RSRC.2, RSRC.3, RSRC.7 | RSRC.7 covers the reuse decision for cached results ("Reuse MAY occur only where it preserves correctness and reproducibility, and is recorded where it affects a budget"); the key's content is open. |
| Stopping at the third consecutive attempt without progress; continuing only on a recorded decision of the human owner | STND.DFLT.9 | Governs agent units of work. A workflow retry bound for a job is a separate matter; note that the number three belongs to agent units. |
| Records kept until retirement | STND.DFLT.4 | Covers records and results, not work directories. |
| Agent continues independent lines; shared machine use | AGENT.15, AGENT.40 | Cover independent lines after a halt and starting parallel work only when resources are free. |
| Work process (version control, branches, merges, releases) | STND.WPROC | Concerns the work process of people and agents, not the execution of computations; no provision of it governs a workflow run. |

Open in the corpus as read: the per-step declaration of inputs and outputs; atomic publication of outputs and the treatment of partial outputs; retry classification, bounds, and backoff for jobs; signals before a kill and the response to them; checkpoint validity, identity, and format version; storage and file-count limits as inputs of a run; the state held in work directories; the resumption record. Several may reach an existing provision only by instantiation (DSGN.1 on bounds, PRIME.4 on failure, REPRO.1 on inputs), which is for the drafter to decide under GOV.11 and GOV.31.

## Timeless versus moving

Timeless: write-then-rename on one file system with a directory sync; a partial output is distinguished from a result; content decides staleness; a retry has a bound, a delay, and a layer; a handler sets a flag; the last signal cannot be caught; a checkpoint carries identity, version, and an integrity check; a part's failure is recorded per part; space and file count are limited resources; provenance is written at production; reproduction is tested by running.

Moving: the defaults of engines (retry counts, cache keys, which signals and intervals a scheduler sends, array limits); the names of flags and directives; the grace and notice times of schedulers and providers; the policies of sites for purge and quota; the file formats of checkpoints and their protocol versions; the provenance schemas and their profiles; the design of parallel file system quota; the set of engines. A provision states the outcome and leaves these to the project's record.

## Not verified

- GNU make behavior on error and interrupt (deletion of a partly built target, `.DELETE_ON_ERROR`, `.PRECIOUS`): four fetches of the manual were refused (HTTP 429) or truncated; no text read.
- Whether a retry status range in the Nextflow example means a resource kill; the Kubernetes Job at-least-once statement and backoff defaults (extract said it drew on general knowledge); pod termination order and grace (same).
- Slurm `GraceTime` and `PreemptMode` in the configuration page (truncated before them); the preemption page's note on the intervals between the three signals; whether a checkpoint facility exists in the scheduler (page silent).
- What DMTCP cannot checkpoint (page silent); the 2009 checkpoint-library threads are single user reports.
- All rows marked "search extract": the LANL failure study (W48), Gray's Heisenbug report (W36), the Blue Waters study and its interconnect recovery figures (W43), the Pegasus failure detection (W35), the notebook study figures (W33; two summaries disagree), the Lustre quota design (W44; 2008 to 2009 material, current releases unchecked), Nix addressing (W47).
- No taxonomy of workflow-level failure causes in HPC could be found and read; the Blue Waters application-run field study (5,000,000 runs) was named in a search result but not read.
- The checkpoint identity rule (practice 13) is reasoned, not sourced.
- Any claim about the Lustre, GPFS, or NFS behavior beyond C3 and the rows above.

## Sources

| ID | URL | What it supports |
| --- | --- | --- |
| W1 | https://www.commonwl.org/v1.2/CommandLineTool.html | Declared inputs and outputs (CWL) |
| W2 | https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html | temp, protected, ensure, retries, shadow, incomplete |
| W3 | https://docs.seqera.io/nextflow/process | errorStrategy, maxRetries, backoff, publishDir, task directories |
| W4 | https://www.commonwl.org/v1.2/CommandLineTool.html | Exit code classes, output validation (same page as W1) |
| W5 | https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html | Idempotent tasks, partitions |
| W6 | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter | Backoff, jitter, one retry layer |
| W7 | https://docs.seqera.io/nextflow/cache-and-resume | Cache invalidation causes |
| W8 | https://slurm.schedmd.com/sbatch.html | signal, requeue, open-mode, no-kill, restart count |
| W9 | https://man7.org/linux/man-pages/man2/fsync.2.html | Directory fsync |
| W10 | https://man7.org/linux/man-pages/man2/rename.2.html | Atomic replace, EXDEV |
| W11 | https://slurm.schedmd.com/cgroup.conf.html | Memory kill and step state (see W19) |
| W12 | https://man7.org/linux/man-pages/man7/signal.7.html | SIGKILL uncatchable, EINTR |
| W13 | https://man7.org/linux/man-pages/man7/signal-safety.7.html | Handler safety |
| W14 | https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems.pdf | Make timestamps, minimality, early cutoff (read as full text) |
| W15 | https://bazel.build/basics/hermeticity | Hermetic builds |
| W16 | https://sre.google/sre-book/addressing-cascading-failures/ | Retry limits and budgets |
| W17 | https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html | Same page as W2 |
| W18 | https://sre.google/sre-book/addressing-cascading-failures/ | Same page as W16 |
| W19 | https://slurm.schedmd.com/cgroup.conf.html | OOM event, step keeps running |
| W20 | https://gasnet-bugs.lbl.gov/hypermail/checkpoint/1242.html | Truncated checkpoint thread (search extract) |
| W21 | https://scr.readthedocs.io/en/latest/users/overview.html | Checkpoint validity, flush, fetch |
| W22 | https://docs.python.org/3/library/pickle.html | Protocol versions, unsafe load |
| W23 | https://docs.python.org/3/library/pickle.html | Same page as W22 |
| W24 | https://slurm.schedmd.com/job_array.html | Array dependency, throttle, order, requeue |
| W25 | https://slurm.schedmd.com/job_array.html | Same page as W24 |
| W26 | https://docs.nersc.gov/filesystems/quotas/ | Space and inode quotas, grace |
| W27 | https://docs.nersc.gov/filesystems/scratch/ | Purge by access time, quota effect |
| W28 | https://docs.nersc.gov/filesystems/quotas/ | Same page as W26 |
| W29 | https://www.w3.org/TR/prov-overview/ | PROV |
| W30 | https://www.researchobject.org/workflow-run-crate/ | Run crate profiles |
| W31 | https://reproducible-builds.org/docs/definition/ | Same page as W46 |
| W32 | https://arxiv.org/abs/2103.12793 | R file reruns |
| W33 | https://2019.msrconf.org/details/msr-2019-papers/36/A-Large-scale-Study-about-Quality-and-Reproducibility-of-Jupyter-Notebooks | Notebook reproducibility (search extract) |
| W34 | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter | Idempotency in retries (same page as W6) |
| W35 | https://scitech.group/files/presentations/2015/silva-llnl-pegasus.pdf | Pegasus failure detection and rescue (search extract) |
| W36 | https://people.eecs.berkeley.edu/~fox/summaries/dependable/gray_stop.html | Gray summary (search extract) |
| W37 | https://kubernetes.io/docs/concepts/workloads/controllers/job/ | Job retry |
| W38 | https://slurm.schedmd.com/slurm.conf.html | KillWait, OverTimeLimit, MinJobAge |
| W39 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html | Two-minute notice, best effort |
| W40 | https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ | Pod termination (extract, unverified) |
| W41 | https://wiki.tuflow.com/TUFLOW_Message_2671 | Restart file incomplete (search extract) |
| W42 | https://dmtcp.sourceforge.io/ | Transparent checkpointing |
| W43 | https://www.nokia.com/bell-labs/publications-and-media/publications/resiliency-of-hpc-interconnects-a-case-study-of-interconnect-failures-and-recovery-in-blue-waters | Interconnect recovery (search extract) |
| W44 | https://wiki.old.lustre.org/images/c/c4/Quota_hld.pdf | Quota granting (search extract) |
| W45 | https://docs.seqera.io/nextflow/cache-and-resume | Work directory preservation (same page as W7) |
| W46 | https://reproducible-builds.org/docs/definition/ | Reproducible build definition |
| W47 | https://nix.dev/manual/nix/2.33/store/derivation/outputs/input-address | Input and content addressing (search extract) |
| W48 | https://www.cs.toronto.edu/~bianca/papers/dsn06.pdf | LANL failure study (search extract) |

Several IDs name a page that supports more than one row; those are listed once per use above so that a row's citation reads without a lookup.
