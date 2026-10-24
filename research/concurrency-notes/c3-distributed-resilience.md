Role: research agent (note C3). Accessed 2026-10-24. Rules followed: read-only; 88 items, under 10 MB; no paywall circumvented; three failed fetches (openshmem.org host unresolved, a GROMACS list archive failed TLS, one HDF5 page 404) not worked around; retrieved text treated as data.

# Distributed and long-running execution beyond MPI, and concurrent access to shared files

**Method caveat.** The fetch tool returns model-written extracts, not pages. For five PDFs (FAIR workflows, Spark RDD, Cores that don't count, Cappello 2014, ALICE) I extracted text locally and read the cited passages; Linux man pages and the UPC++ guide were downloaded and searched directly. "Search extract" marks rows resting only on search-result text. MPI is out of scope except at its seams.

## Answer in brief

1. Assume any task may run zero, one, or several times: engines retry by default (Ray 3, Spark 4 attempts plus optional speculative copies, Slurm requeue restarts the script). External effects must be idempotent or committed once under a unique attempt key; retries are bounded and recorded. [S5, S6, S14, S15]
2. A result is valid when complete and verified, not when the exit status is zero. Publish atomically (write temporary, flush, rename, flush directory) and make partial outputs detectable. [S12, S37, S38, S42]
3. Cache and resume decisions key on everything that affects output (code, parameters, input content, environment), not names or timestamps alone. [S10, S11, S13]
4. Task graphs and input pairing are deterministic, or the run states which results may vary and by how much. [S11, S18]
5. Each run leaves provenance naming workflow version, components, inputs, environment, and attempts. [S1, S3]
6. Time, memory, and storage limits are explicit, and hitting one is a recorded failure. [S9, S14]
7. A checkpoint counts only if every participant succeeded, it holds all state needed to continue (including random number state), and its integrity is checkable. Restarts are shown to reproduce the uninterrupted run, bitwise or within a stated tolerance. [S18, S22, S23]
8. Hardware is not fail-stop: silent data corruption is measured in production fleets, so critical results need end-to-end checks (checksums, invariants or algorithm-based checks, redundancy). [S18, S20, S21]
9. Code on one-sided, PGAS, or task runtimes states its ordering, completion, visibility, and progress assumptions; these models do not order messages, puts, or callbacks unless told to. [S27-S33]
10. Shared-file access is correct only where the storage's guarantees were checked: NFS gives close-to-open consistency, locks are advisory and losable, concurrent NFS appends corrupt, and SQLite WAL and HDF5 SWMR need local or write-ordered POSIX storage. [S36, S39, S40, S44-S48]
11. Durations use a monotonic clock; records use UTC plus clock source; cross-node order comes from sequence numbers or logical clocks, never wall-clock comparison. [S54-S56]
12. In composed runtimes one layer owns each resource; per-node totals of processes, threads, and accelerator contexts are bounded, affinity is recorded, and silent fallbacks are detected. [S58-S62]

## 1. Task-based and workflow execution

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Retries | Ray retries 3 times on worker death; application exceptions retried only if enabled. No mention of side effects. | Current docs | S5 |
| Lost objects | Ray rebuilds lost objects from lineage only while the owner lives. | Current docs | S4 |
| Duplicate attempts | Spark: 4 attempts by default; speculation relaunches slow tasks; committer algorithm 2 "may cause a correctness issue." | Current docs | S6 |
| Determinism assumed | RDDs come only from "deterministic operations"; immutability makes straggler backup tasks safe. | NSDI 2012 | S7 |
| Poison tasks, coordinator loss | Dask marks a task "bad" after it kills 3 workers; scheduler state is not persisted; impure functions may differ on recomputation. | Current docs | S8 |
| Exhaustion | Dask kills a worker at 95% memory; tasks are "cancelled mid-execution and rescheduled elsewhere." | Current docs | S9 |
| Requeue | Requeued Slurm jobs restart "from its beginning with the same job ID"; the time-limit signal may come 60 s early. | Current docs | S14 |
| Cache keys | Parsl: code changes "will not invalidate cached values"; caching suits only deterministic apps. | Current docs | S10 |
| Cache keys | Nextflow hashes input path, mtime, size, script, environment; NFS "may report inconsistent file timestamps"; a closure variable without `def` races; unkeyed channel merges give nondeterministic inputs. | Current docs; strict parser since 25.04 | S11 |
| Rerun rules | Snakemake uses mtimes plus code, parameters, environment, small-file checksums; zero exit counts as success even with empty output unless `ensure` is used; `--rerun-incomplete` reruns flagged outputs. | Current docs; flag via search extract | S12, S17 |
| Job hash | Snakemake hashes "code, parameters, raw input files, software environment and the hashes of its dependencies." | 2021 paper | S13 |
| Idempotency keys | A caller-supplied request identifier stored atomically with the result returns the original outcome on retry. | Industry practice | S15 |
| FAIR workflows | Identifiers per version (F1.2) and component (F1.1); "detailed provenance of the workflow and of the products" (R1.3). | Sci. Data 2025 | S1 |
| Run provenance | Workflow Run RO-Crate, aligned to W3C PROV, implemented in six engines. | PLOS ONE 2024 | S3 |
| Community | 2024 summit asks for a FAIR workflow maturity model; heterogeneous and multi-facility execution remain open. | Oct 2024 | S2 |
| Rerun failure | 74% of about 9,000 archived R files failed on re-execution. | 2022 (search extract) | S16 |

Recurring failure modes: duplicated side effects from retries and speculation; partial outputs accepted as success; stale cache hits; nondeterministic pairing; coordinator state loss; resource kills that look like ordinary retries.

## 2. Resilience of long runs

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Practice | Production fail-stop tolerance is rollback from checkpoints; application-level checkpointing is "the most popular approach," since programmers know the critical data. | 2014 update | S18 |
| Multilevel | Node-local, partner, and file-system levels (SCR, FTI, VeloC) cut checkpoint cost. | 2014; VeloC (search extract) | S18, S26 |
| Consistency | Classic coordinated protocols are rare in production because checkpoints at a global synchronization point coordinate implicitly. | 2014; survey (search extract) | S18, S24 |
| All-agree commit | SCR reports success only if every process passed `valid=1`. | Current docs | S22 |
| Interval | Near sqrt(2 x checkpoint cost x MTBF), less checkpoint cost (Young, Daly). | Search extract | S25 |
| Restart test | Climate tests require a restarted run to match a straight run bit for bit (ERS), also at halved process and thread counts (ERP, PEM, PET). | Current docs | S23 |
| Missing state | Reused random seed on restart reportedly distorted a thermostat. | 2008; not read | S65 |
| SDC rate | "A few mercurial cores per several thousand machines"; the "only symptom is an erroneous computation." | HotOS 2021 | S20 |
| SDC rate | Hundreds of affected CPUs in hundreds of thousands of machines; "systemic issue across generations." | 2021 | S21 |
| SDC detection | Replication needs bitwise determinism, which asynchrony erodes; ABFT covers specific kernels; "exascale is highly unlikely to be viable without error detection." | 2014 update; DOE workshop 2012 | S18, S19 |

Practical: application-level checkpoints at a consistent point, committed only on unanimous success, checksummed, two generations kept; a periodic restart test; cheap invariant checks (conservation, residuals, checksums) as SDC detectors.

## 3. PGAS and other distributed models

The hazard classes match threads and messages (races, deadlock, partial failure, nondeterminism), but some hazards differ in kind.

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Progress dependence | UPC++ has no hidden threads; futures ready and RPCs run only inside progress calls; a thread in an OpenMP barrier never services UPC++ work, causing deadlock. | Current guide | S27 |
| No implicit order | UPC++: "no implicit point-to-point ordered delivery"; two puts may complete out of order. | Current guide | S27 |
| Order vs completion | OpenSHMEM fence orders puts per destination; quiet is needed across destinations. | Open MPI docs | S28 |
| Collective allocation | `shmem_malloc` needs identical sizes on all PEs, or addresses may differ. | Open MPI docs | S29 |
| Remote races, atomics | Conflicting RMA gives indeterminate values; data in an atomic domain must be accessed only through it. | Current guide | S27 |
| Same model | Chapel: a racy program "is not a valid program"; multi-locale consistency equals single-locale. | Current spec | S30 |
| Segments | Coarray data defined in one image's segment must not be touched in an unordered segment elsewhere. | Search extract | S31 |
| Partial failure | Failed images are noticed at different times; statements without `STAT=` may hang. | Search extract | S32 |
| Reordering | Charm++ does not guarantee message order; priorities are hints. | Search extract | S33 |
| Coherence modes | Legion's default preserves program order; relaxed modes hand synchronization to the application. | Search extract | S34 |
| Replay | HPX replay and replicate-and-vote presume tasks are safe to rerun. | Search extract | S35 |

Specific in kind: completion that depends on the target entering the runtime; separate ordering, completion, and visibility for one-sided operations; collective symmetric allocation; mixed atomic and plain access to one remote datum; runtime-chosen order and migration making floating-point results schedule-dependent; failure discovered at different times.

## 4. Concurrent access to files and shared data

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| NFS | Close-to-open only; "not designed to support true cluster file system cache coherence without some type of application serialization"; client timestamps lag. | Linux man page | S36 |
| Durability | File `fsync` does not persist the directory entry; sync the directory too. | Linux man page | S37 |
| Atomic replace | `rename` replaces the target atomically. | Linux man page | S38 |
| Append | `O_APPEND` "may lead to corrupted files on NFS" with several appenders. | Linux man page | S39 |
| Locks | POSIX record locks are per process: closing any descriptor drops all, threads share them; NFS locks can be lost. Open-file-description locks avoid the close problem. flock over NFS is emulated. | Linux man pages | S40, S41 |
| Crash consistency | 60 vulnerabilities in 11 applications, some silent; several fixes added a missing directory `fsync`. | OSDI 2014 | S42 |
| fsync failure | No studied application recovered correctly from every `fsync` failure. | ATC 2020 (search extract) | S43 |
| SQLite | Network-file-system locks "have been known to operate incorrectly," causing corruption; WAL "does not work over a network filesystem"; one thread's close() cancels others' locks. | Current docs | S44-S46 |
| HDF5 SWMR | Needs POSIX `write()` ordering; writer may only append to or modify existing datasets; readers poll and refresh; NFS and SMB excluded. | Current docs; guide (search extract) | S47, S48 |
| Parallel HDF5, netCDF | Metadata-changing calls are collective with identical arguments; netCDF unlimited-dimension writes reportedly collective. | Current docs; search extract | S49, S51 |
| Locking disabled | Turning off HDF5 locking "may lead to data corruption" under concurrent access. | Search extract | S50 |
| Lustre, GPFS | Lustre `localflock` is client-local only; GPFS non-overlapping writers proceed, overlapping ones revoke tokens. | Search extract | S52, S53 |

In practice: lost updates through NFS caching, corrupted shared logs, databases corrupted by locks that do nothing, truncated files after crashes, torn reads where write order is not honored.

## 5. Time in distributed runs

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Clocks | `CLOCK_REALTIME` jumps and is slewed by NTP; `CLOCK_MONOTONIC` cannot be set; `CLOCK_TAI` avoids leap steps. | Linux man page | S54 |
| Causality | Happened-before is a partial order; logical clocks give a consistent total order; drift can only be bounded. | 1978 (search extract) | S55 |
| Trace skew | Unsynchronized clocks put receives before sends; drift varies, so linear correction fails on long runs. | 2007 to 2013 (search extract) | S56 |
| Bounded wait | Spanner orders commits by waiting out a known uncertainty bound. | 2012 (secondary) | S57 |
| File times | Engines deciding on mtimes misjudge freshness on NFS. | Current docs | S11, S36 |

## 6. Heterogeneous composition

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Oversubscription | 8 workers x 8 OpenMP threads = 64 threads on 8 CPUs; joblib's process backend caps inner threads, its thread backend cannot. | Current docs | S58 |
| Nested runtimes | Limits can fail across distinct OpenMP runtimes; Intel and LLVM OpenMP in one process "is known to cause problems." | Current README | S59 |
| Cross-runtime deadlock | A thread blocked in one runtime does not progress another. | Current guide | S27 |
| Affinity | Slurm binds when its plugin is on; "inconsistent options generally result in errors"; `--overcommit` allows several tasks per CPU. | Current docs | S60 |
| Shared GPUs | Ending an MPS client unsynchronized leaves server and clients undefined; a missing daemon reportedly means running without MPS, a silent fallback. | Current docs; slides (search extract) | S61, S62 |
| Workflow plus MPI | Pilot-job assumptions "do not translate to the MPI context"; Flux nests schedulers so each level owns its share. | Search extract | S63, S64 |

Seams fail when two layers each think they own cores, GPUs, or progress; the remedy is one declared owner per resource and a recorded effective layout.

## Outcomes a standard could require

| Outcome | Why | Source | Scope |
| --- | --- | --- | --- |
| Retried or requeued units have idempotent effects or commit once under a unique attempt key; retries are bounded and recorded. | Defaults run work more than once. | S5, S6, S14, S15 | Model-neutral |
| Success means verified complete outputs, published atomically and durably; partial outputs are detectable. | Empty output with zero exit; torn files. | S12, S37, S42 | Model-neutral |
| Cached results are keyed on all result-affecting inputs, including code and environment, and the key is recorded. | Stale caches; unreliable timestamps. | S10, S11, S13 | Model-neutral |
| The run states whether results depend on schedule, and the tolerance if so. | Nondeterministic pairing and schedules. | S11, S18 | Model-neutral |
| Each run records version, components, inputs, environment, attempts, and resource layout as machine-readable provenance. | FAIR R1.3, F1.2. | S1, S3 | Model-neutral |
| Resource limits are declared and breaches reported as such. | Silent kill and reschedule. | S9, S14 | Model-neutral |
| Checkpoints commit only on unanimous success, carry integrity checks and complete state, and a prior good one is kept. | Partial or incomplete checkpoints. | S18, S22 | Model-neutral |
| A restart test matches the uninterrupted run, bitwise or within stated tolerance, at changed process counts where supported. | Restart bugs are silent. | S23 | Model-neutral |
| Long or critical runs apply and record end-to-end checks against silent corruption. | Measured fleet SDC rates. | S20, S21 | Model-neutral |
| Code documents ordering, completion, visibility, and progress assumptions; symmetric allocations are collective and identical. | No implicit order; progress-dependent completion. | S27-S29 | Specific to PGAS and task runtimes |
| Participant failure is handled by status checks or documented as fatal. | Hangs on failed images. | S32 | Model-neutral; form varies |
| Shared-file access names the storage guarantees it needs and is checked against the target; no concurrent NFS appends, embedded-database write sharing, or write-order-dependent modes on network storage. | NFS, SQLite, HDF5 limits. | S36, S39, S44-S48 | Specific to shared file systems |
| Locks relied on for correctness are shown to be enforced on the target storage. | Advisory, process-wide, losable locks. | S40, S44, S52 | Specific to file locking |
| Monotonic clocks for durations; UTC plus clock source in records; order from sequence or logical clocks. | Jumps and skew. | S54-S56 | Model-neutral |
| Per-node totals of processes, threads, and accelerator contexts are bounded and recorded, with one owner per resource and fallbacks reported. | Oversubscription, nested runtimes. | S58-S62 | Specific to composed runtimes |

## Unverified

- Search extracts only: S16, S17 (flag), S25, S26, S31-S35, S43, S48 (NFS exclusion), S50-S53, S55-S57, S62 (fallback), S63, S64.
- S65 (restart seed report): fetch failed, not read.
- Nextflow retry defaults, and whether Snakemake deletes incomplete outputs: not found.

## Sources

| ID | URL | What it supports |
| --- | --- | --- |
| S1 | https://arxiv.org/abs/2410.03490 | FAIR workflows |
| S2 | https://arxiv.org/abs/2410.14943 | Summit 2024 |
| S3 | https://arxiv.org/abs/2312.07852 | Run provenance |
| S4 | https://docs.ray.io/en/latest/ray-core/fault-tolerance.html | Ray lineage |
| S5 | https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html | Ray retries |
| S6 | https://spark.apache.org/docs/latest/configuration.html | Spark attempts |
| S7 | https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf | RDD determinism |
| S8 | https://distributed.dask.org/en/stable/resilience.html | Dask failures |
| S9 | https://distributed.dask.org/en/stable/worker-memory.html | Dask memory |
| S10 | https://parsl.readthedocs.io/en/stable/userguide/workflows/checkpoints.html | Parsl caching |
| S11 | https://docs.seqera.io/nextflow/cache-and-resume | Nextflow resume |
| S12 | https://snakemake.readthedocs.io/en/stable/project_info/faq.html | Snakemake reruns |
| S13 | https://f1000research.com/articles/10-33/v2 | Snakemake hash |
| S14 | https://slurm.schedmd.com/sbatch.html | Requeue, signal |
| S15 | https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ | Idempotency keys |
| S16 | https://arxiv.org/abs/2103.12793 | Rerun failures |
| S17 | https://manpages.ubuntu.com/manpages/jammy/man1/snakemake.1.html | Incomplete flag |
| S18 | https://charm.cs.illinois.edu/newPapers/14-39/paper.pdf | Exascale resilience |
| S19 | https://www.osti.gov/biblio/1176844 | DOE workshop |
| S20 | https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s01-hochschild.pdf | Mercurial cores |
| S21 | https://arxiv.org/abs/2102.11245 | Fleet SDC |
| S22 | https://scr.readthedocs.io/en/latest/users/api.html | Checkpoint commit |
| S23 | https://noresm-docs.readthedocs.io/en/noresm2/testing/testing.html | Restart tests |
| S24 | https://cs.cornell.edu/courses/cs717/2001fa/papers/alvisi-survey.pdf | Rollback taxonomy |
| S25 | https://graal.ens-lyon.fr/~abenoit/CR02/papers/daly.pdf | Interval |
| S26 | https://arxiv.org/abs/2103.02131 | VeloC |
| S27 | https://upcxx.lbl.gov/docs/html/guide.html | UPC++ semantics |
| S28 | https://docs.open-mpi.org/en/main/man-openshmem/man3/shmem_fence.3.html | Fence, quiet |
| S29 | https://docs.open-mpi.org/en/main/man-openshmem/man3/shmem_malloc.3.html | Symmetric allocation |
| S30 | https://chapel-lang.org/docs/language/spec/memory-consistency-model.html | Chapel model |
| S31 | https://www.intel.com/content/www/us/en/docs/fortran-compiler/developer-guide-reference/2025-2/execution-segments-for-images.html | Segments |
| S32 | https://www.intel.com/content/www/us/en/docs/fortran-compiler/developer-guide-reference/2025-2/failed-images.html | Failed images |
| S33 | https://lists.siebelschool.illinois.edu/lists/arc/charm/2011-09/msg00079.html | Charm++ order |
| S34 | https://legion.stanford.edu/overview | Legion coherence |
| S35 | https://hpx-docs.stellar-group.org/latest/html/libs/full/resiliency_distributed/docs/index.html | HPX replay |
| S36 | https://man7.org/linux/man-pages/man5/nfs.5.html | NFS coherence |
| S37 | https://man7.org/linux/man-pages/man2/fsync.2.html | Directory fsync |
| S38 | https://man7.org/linux/man-pages/man2/rename.2.html | Atomic rename |
| S39 | https://man7.org/linux/man-pages/man2/open.2.html | NFS append |
| S40 | https://man7.org/linux/man-pages/man2/fcntl_locking.2.html | Lock pitfalls |
| S41 | https://man7.org/linux/man-pages/man2/flock.2.html | flock on NFS |
| S42 | https://cs.uwaterloo.ca/~alkiswan/papers/alice-osdi14.pdf | Crash consistency |
| S43 | https://www.usenix.org/conference/atc20/presentation/rebello | fsync failures |
| S44 | https://www.sqlite.org/useovernet.html | SQLite network |
| S45 | https://www.sqlite.org/howtocorrupt.html | SQLite corruption |
| S46 | https://www.sqlite.org/wal.html | WAL one host |
| S47 | https://support.hdfgroup.org/documentation/hdf5-docs/advanced_topics/intro_SWMR.html | SWMR rules |
| S48 | https://support.hdfgroup.org/archive/support/HDF5/docNewFeatures/SWMR/HDF5_SWMR_Users_Guide.pdf | SWMR and NFS |
| S49 | https://support.hdfgroup.org/documentation/hdf5-docs/hdf5_topics/CollectiveCallsInParallel.html | Collective calls |
| S50 | https://confluence.ecmwf.int/spaces/UDOC/pages/278549648/HPC2020+Reading+a+NetCDF+or+HDF5+file+gets+stuck | Locking off |
| S51 | https://docs.unidata.ucar.edu/netcdf-c/4.8.1/parallel_io.html | netCDF parallel |
| S52 | https://manpages.org/mountlustre/8 | Lustre locks |
| S53 | https://arxiv.org/abs/1904.03997 | GPFS locking |
| S54 | https://man7.org/linux/man-pages/man2/clock_gettime.2.html | Clocks |
| S55 | https://amturing.acm.org/p558-lamport.pdf | Logical clocks |
| S56 | https://fs.hlrs.de/projects/rabenseifner/publ/Dagstuhl07341.BeckerDaniel.Slides.pdf | Trace skew |
| S57 | https://www.cs.princeton.edu/courses/archive/spr24/cos418/docs/L17-spanner-pt1.pdf | Commit wait |
| S58 | https://scikit-learn.org/stable/computing/parallelism.html | Oversubscription |
| S59 | https://github.com/joblib/threadpoolctl | Mixed OpenMP |
| S60 | https://slurm.schedmd.com/mc_support.html | Affinity |
| S61 | https://docs.nvidia.com/deploy/mps/when-to-use-mps.html | MPS hazards |
| S62 | https://www.olcf.ornl.gov/wp-content/uploads/2021/06/MPS_ORNL_20210817.pdf | MPS fallback |
| S63 | https://parsl.readthedocs.io/en/latest/userguide/apps/mpi_apps.html | Workflow plus MPI |
| S64 | https://computing.llnl.gov/projects/flux | Nested scheduling |
| S65 | https://mailman-1.sys.kth.se/pipermail/gromacs.org_gmx-developers/2008-April/002497.html | Restart seed (not read) |
