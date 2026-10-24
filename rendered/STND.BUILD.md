# Build standard (STND.BUILD) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 124 (2026-10-24); revised to 1.0.1 in entry 127 (2026-10-24). This reading copy is composed from the per-provision files in STND/BUILD/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice of building software that holds for every build tool and every language: how the work turns its source and its other inputs into the outputs that it runs, tests, and releases. It adds to REPRO, STND.DEPS, STND.CODE, HW, STND.OFFLD, and the language standards only what building makes necessary. It covers the inputs of build steps (STND.BUILD.1 to STND.BUILD.7); configure steps, cross builds, and the targets of device code (STND.BUILD.8, STND.BUILD.9, and STND.BUILD.10); the settings that change results, warnings, and checking builds (STND.BUILD.11, STND.BUILD.12, and STND.BUILD.13); reproducible outputs (STND.BUILD.14 to STND.BUILD.19); release archives, build scripts, and test data (STND.BUILD.20, STND.BUILD.21, and STND.BUILD.22); build caches (STND.BUILD.23 and STND.BUILD.24); and the build record and the build configurations under check (STND.BUILD.25 and STND.BUILD.26).

The steps that build software are governed by this standard; STND.WFLOW governs the publication, retry, restart, storage, and resumption around them. No provision binds. Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The verification of each fetched component before its use binds at every class through STND.DEPS.6, and this standard adds nothing to that floor. The standard is agnostic of build tool, language, compiler, platform, and vendor: its provisions name none of them and no revision of a specification (GOV.18). The forms of these rules for one language belong to the standard of that language, which cites this standard for the general rule: STND.CXX.4 and STND.CXX.25 hold C++ forms of STND.BUILD.11 and of the first sentence of STND.BUILD.12.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration and Execution setting have the meanings that STND.CODE gives them; Fetched component, Integrity digest, and Dependency record have the meanings that STND.DEPS gives them, and an integrity digest is used here also of an input or an output of a build step; Accelerator, Hardware model, and Runtime library have the meanings that HW gives them; and Device code has the meaning that STND.OFFLD gives it. Each output of a build that the work runs, tests, or distributes is a result in the sense of the Lexicon. A toolchain matrix of STND.CXX lists toolchains in the sense of this standard.

| Term | Definition |
| --- | --- |
| Build | The sequence of build steps by which the tools of the work turn its source and its other inputs into the outputs that the work runs, tests, or distributes. |
| Build step | One run of one tool in a build, which reads inputs and writes outputs. |
| Build description | The part of the repository configuration that states the build steps of the work, their inputs and outputs, and its build configurations. |
| Declared input | Of a build step: an input that the build description, or a record that a tool writes at each run of the step, states as an input of that step. |
| Build configuration | A named set of the options, execution settings, toolchain, and target platform with which the build description builds the work. |
| Configure step | A build step that detects properties of the build host or of the target platform, and writes from them inputs of later build steps. |
| Build tree | The directory into which a build writes its outputs and its generated files. |
| Clean build | A build into an empty build tree that takes no output from a build cache. |
| Incremental build | A build that runs again, in a build tree that an earlier build wrote, only the build steps whose declared inputs changed since that build. |
| Reporting build | A build from which the work reports a result other than the verdict of a test, or makes a release. |
| Build host | The machine, with its operating system, on which the build steps of a build run. |
| Target platform | The hardware model and operating system on which an output of a build runs. |
| System root | The headers, libraries, and other files of the target platform from which a build compiles and links code for that platform. |
| Toolchain | Of a build step: the compilers, linkers, archivers, interpreters, generators, and other tools that the step runs, with the system root from which they take the files of the target platform. |
| Compilation unit | The source that one run of a compiler or translator reads as one input, with the files that it includes, as that compiler or translator defines it. |
| Generated file | A file that a build step, or a tool run before the build, produces from other inputs, and that a later build step reads as source or as the interface of a unit that source names. |
| Build script | A file of commands or code that a build runs to carry out its configure steps or its other build steps, code that a compiler loads and runs during compilation included. |
| Build record | The record of one build, with the content that the table of STND.BUILD.25 gives. |
| Release archive | A file that a release distributes and from which others build the work. |
| Build cache | A store of outputs of build steps from which a build takes an output in place of running the step that produced it. |
| Checking build | A build whose outputs carry checks at run time, of memory accesses, undefined behavior, or data races among them, that no reporting build carries. |

## Notes

The provisions rest on what the research note finds to hold across build tools: a build is a function from its inputs to its outputs, and an input missing from its declarations makes it wrong without an error; incremental and parallel builds expose the missing declarations; time, order, locale, and path enter the outputs unless the build removes them; a pin by content holds where a pin by name moves; the default of a compiler option belongs to a compiler and a language mode, not to the language; a release archive is not the repository; a cache is correct when its key holds every input; and a build host does not run code of the target platform in a cross build (research/build-notes/b1-build-systems.md, "Timeless versus moving"). The Notes name a tool only to show a hazard. Facts that the research note marks unverified do not appear in a provision.

A build is a sequence of steps that produces a result, and REPRO.10 governs it at LVL0 as it governs every such sequence. Between this standard and STND.WFLOW the rule is this: the steps that build software are governed by STND.BUILD, and STND.WFLOW governs the publication, retry, restart, storage, and resumption around them. A build that runs as one step of a larger workflow is a step of that workflow under STND.WFLOW, and its own build steps are governed here. STND.BUILD.23 is the build form of STND.WFLOW.6: it keys a stored output on the content of the inputs of its step, as STND.WFLOW.6 keys a stored output of a workflow step, and adds the revision of each tool and the variables of the environment that a build step reads, which a build cache that keys only on files leaves out.

The standard adds build content to provisions that already hold the outcome, and does not restate them (GOV.31). REPRO.1 has every result regenerable from recorded inputs, REPRO.2 the properties of the computational environment that affect results recorded, which is where a project states what the environment of its builds holds, REPRO.3 undeclared variation a defect, REPRO.4 provenance written at production, REPRO.9 each dependency enumerated at its exact revision, and REPRO.10 the build description versioned and reviewed; QA.7 has each change to it reviewed. STND.DEPS.6 verifies each fetched component against its integrity digest before use, at every class; STND.DEPS.8 records the revision of each compiler and interpreter with each result; STND.DEPS.10 lets lock files serve as the dependency record. STND.CODE.6 keeps each check of untrusted input in every build, so no build configuration removes one, and STND.CXX.18 keeps a required check of a floating-point value from a unit compiled under an option that assumes finite values. HW.3 identifies the execution path of each result, HW.5 has the hardware contract state each option that sets its delivered arithmetic, and STND.ANNEX.5 lists among what the citing contract states each build setting that admits approximation, changes rounding, flushes subnormal values, or enables traps; one statement serves HW.5 and STND.BUILD.11 where the contract cites the repository configuration. HW.7 has the evidence current for the settings and libraries in use, and has each run confirm at its start the properties on which its results rely. STND.OFFLD.24 records the hardware models for which a build holds device code, and STND.OMP.4 has a component that uses OpenMP built and tested without it where its documentation says that it works so. STND.VVUQ.82 has a difference whose every source is stated, and that lies within the agreement fixed before a comparison, not treated as a defect, and admits a mode without run-to-run variation as an option; STND.VVUQ.83 keeps an agent from changing the work on its own initiative only to remove such a difference.

The forms of these rules for one language belong to the standard of that language, which cites this standard for the general rule. STND.CXX.4 and STND.CXX.25 are the C++ forms of STND.BUILD.11 and of the first sentence of STND.BUILD.12. The rules here are the wider: STND.BUILD.11 also asks the values that the toolchain takes by default, in one place, and the settings of each link step, and STND.BUILD.12 reaches each tool of the toolchain and not only the compilers. STND.CXX.26 runs the tests of C++ code in checking builds, and STND.CXX.27 keeps the library's production checks in reporting builds; a verdict of a test that a checking build runs is a result of the checks of a change, and the term Reporting build leaves it out. The outcomes hold for a language whose source names its units by a module or a crate and not by a file (STND.BUILD.2), for code that a compiler loads and runs during compilation (STND.BUILD.9 and STND.BUILD.21), and for a build script written by hand (STND.BUILD.1, STND.BUILD.7, and STND.BUILD.21). Where an interpreter runs source that nothing compiles ahead of the run, the settings of the run belong to the standard of the language, as STND.JL.5 holds them for Julia, and STND.BUILD.11 reaches each step that compiles or translates. A translation unit of STND.CXX is a compilation unit in the sense of this standard.

A dependency that exists in what a build does and not in what it declares gives two failures: an incremental build omits a command that it needs, so a change does not reach the outputs, and a parallel build runs steps in an order that the declarations do not fix, so it races. One study found more than 1.2 million such dependencies, of six root causes, in four mature projects, and 21 cases in one project in which a target depended on generated code and not on its generator, so outputs were built and shipped from outdated contents (b1, section 1, S20); another cites dependency errors as the most prevalent errors of build scripts (S21); and an earlier essay put it as "Incomplete Makefiles are wrong Makefiles" (S22) (STND.BUILD.1 and STND.BUILD.3). The command line of a step is among its inputs, so a change of an option rebuilds what it affects (S23) (STND.BUILD.1). A list of included files kept by hand drifts from the source, and the tool that reads the files, or one that scans the source, finds them at each run (S20, S21, S23) (STND.BUILD.2). A unit that source names by a module or a crate is read through an interface file that a compiler wrote when it compiled that unit; that file is a generated file under STND.BUILD.4, and the order of compilation follows from the source as STND.BUILD.2 asks. A build whose outputs differ only when it runs incrementally or in parallel, beyond what its record declares, has a defect in what it declares, and its variation is undeclared variation, which REPRO.3 makes a defect (STND.BUILD.3); a difference whose source and extent the build record declares, the output of a tool that embeds an identifier of its own run among them, is not a defect. A generated file edited by hand loses the edit at its next generation, and is a source that no review of its generator sees (S20, S17) (STND.BUILD.4 and STND.BUILD.5). Where generating a held file again at each change exceeds its worth, RSRC.12 lets the check of STND.BUILD.5 run at release. A build that writes into the source tree changes the revision that REPRO.1 names, and a build tree apart from it lets two or more build configurations of one source tree coexist (S12, S18) (STND.BUILD.6); the update of a generated file that the version history holds, made by running its generator, is the one write into the source tree that STND.BUILD.6 admits.

A fetch inside a build step makes the outputs depend on what a remote system returns at that moment: a name of a branch or tag moves, a service goes away, and the step has no pinned digest to compare against. One distribution's policy forbids network access to other hosts in its required build targets, with one exception, and one build tool's documentation advises a commit hash over a branch or tag name and says that its disconnected mode does not prevent network access on the first run (S17, S9b); a hermetic build isolates the build from changes to the host (S18) (STND.BUILD.7). Isolation of build steps from the host is one means of meeting STND.BUILD.1 and STND.BUILD.7, and the standard asks for the outcome, each input read only where it is declared. STND.DEPS.6 binds the verification of what is fetched, and STND.BUILD.7 adds only that the fetch happens before the build and that a missing input stops the build in place of a fetch. A build step that an agent runs and that reaches a system outside the provisioned environment is network access, which PRIME.7 already binds to an authorization; that is why STND.BUILD.7 is a default and asks for no authorization of its own.

A configure step that detects a library, a header, or a feature of the host makes the same source build differently on two hosts, and a property found absent removes a feature silently (S23, S19) (STND.BUILD.8). Required or recorded, and settable by an option, the property becomes a declared input. A configure step that runs a test program on the build host learns nothing of a target platform that the build host does not run, so in a cross build each such property has a declared value or a test that compiles and does not run; a tool that the build compiles and then runs during the build is code for the build host, and compiled for the target platform it does not run there (b1, section 4, S9). Code that a compiler loads and runs during compilation, a macro that runs as code or a plug-in of the compiler among it, is code for the build host in the same way (STND.BUILD.9). One build tool treats a build of device code that names no hardware model as an error, and accepts a value that takes the set from the accelerators present on the build host, so that a build on a host without accelerators fails or builds for none; a build of device code holds compiled code for each named hardware model and, optionally, intermediate code that a runtime library compiles at load (S9d, S24) (STND.BUILD.10). A target of device code often names a family of hardware models, and the statement of STND.BUILD.10 gives the targets in the form that the compiler takes. A rule that takes the set from the accelerators of the build host meets STND.BUILD.10, and the record of STND.OFFLD.24 and the Hosts row of STND.BUILD.25 then show what was built and where. A build without code for the accelerator installed where it runs is found at the start of a run by the confirmation of HW.7.

The default of an option that changes results belongs to a compiler and a language mode: one compiler leaves multiply and add uncontracted in a standards-conforming mode of C and contracts them otherwise, and another documents one default of contraction for each of two accelerator languages and a third for its other languages (S5, S13). One option lets the compiler assume that no argument or result is a not-a-number or an infinity (S5), which is why STND.CXX.18 keeps it from a unit that holds a required check of such a value; an option bundle that relaxes floating-point semantics is set by its own name or by one optimization level, which that compiler documents as disregarding strict compliance with the language standard (S5). In one study, compilations of one library and its examples across compilers and options gave 1,086 instances of differing results, and in five examples a vendor's link step introduced variation whatever the optimization level (S28) (STND.BUILD.11). A setting left to the default of the toolchain is a setting whose value the repository configuration does not show and a change of toolchain changes silently, so the first sentence of STND.BUILD.11 states its value. The link step is among the places where a setting changes results: in one compiler, the option bundle that relaxes floating-point semantics links startup code that flushes subnormal values for every library in the process, and another documents that its option for unsafe mathematics, given at link time, may include startup files that change the default floating-point control word (S13, S5) (the second sentence of STND.BUILD.11). The name of a build configuration does not say what it holds, and one build tool's default build type is often an empty string (S12b), which is why the build record gives the values of the settings.

A warning that fails the checks of a change costs its author one fix where the toolchain is fixed and known. A release archive whose build fails on warnings by default fails for each party that builds it with a compiler newer than the release that adds a warning, and one compiler's documentation advises against enabling every warning that it offers, since newer warnings vary in quality (S13); the maintainers of two projects decided against failing on warnings by default in their release archives for that reason, which are opinions and not studies (S25, a secondary source) (STND.BUILD.12). The second sentence of STND.BUILD.12 limits the failure of a build on a warning to the toolchains on which the checks of the release ran, so that the build description makes that behavior explicit for each toolchain (SIMPL.6). A finding that STND.CODE.4 suppresses at its location, with its reason, is not reported, and so fails no check under STND.BUILD.12. A detector of invalid memory accesses needs its option at compilation and at link, and slows a run about twofold; a detector of data races generally needs every part of the program compiled with it, and code compiled without it gives missed races or false reports (S10b, S11) (STND.BUILD.13). Outputs of a checking build mixed with those of a reporting build give a result from a build configuration that nobody measured, which is why a checking build keeps its own build tree. STND.CONC.25 runs concurrency checks at run time, and STND.CONC.27 has the record of a verification state what its method does not cover, which the second sentence of STND.BUILD.13 makes specific for the parts of the work linked without a check. Whether two detectors are able to run in one build is marked unverified in the research note, and no provision depends on it.

A build is reproducible if, given the same source, build environment, and build instructions, every party that holds them is able to recreate bitwise identical copies of the specified outputs, and the project states what the environment holds (S1, S1b). Archives, documentation, and binaries embed the time of the build unless the build takes one instant from its source, and one convention, which the note reports as widely adopted, passes that instant to each tool as a variable of the environment (S2) (STND.BUILD.14). The order in which a file system lists a directory is not consistent, a wildcard in a build rule takes that order, and the collation of a sort depends on the locale (S4, S7) (STND.BUILD.15). The locale changes the format of dates, the order of a sort, and the encoding of text (S7) (STND.BUILD.16). Compilers record source paths in debug information and in the names of files that the source prints, and either a fixed path, recorded as part of the environment, or a mapping of the path in the outputs removes the difference (S3, S5b) (STND.BUILD.17). A random seed, a generated identifier, or the order of a hash table in a tool that a build runs changes the outputs from one run to the next unless a declared input fixes it (S3) (STND.BUILD.18). Each of STND.BUILD.14 to STND.BUILD.18 admits the two outcomes of REPRO.3 that apply to a build: the source of the variation removed, or the variation declared in the build record with its source and its extent. Bitwise identity of builds is an option, not a requirement, unless an acceptance criterion or the consequence class demands it (STND.VVUQ.82). STND.BUILD.19 asks for the comparison that shows whether the outputs agree, and its second sentence for the declaration that REPRO.3 asks of each output that differs. The comparison follows from the definition of S1 and the hazards of section 1 of the note, and no source of the note gives its cost; RSRC.12 lets it run at release and not at each change. An output compared bitwise needs no tolerance; a tolerance on a numerical output of a build rests on NUMER.11.

In the compromise of a compression library disclosed in 2024, the first stage of the attack was in the release archives and not in the repository; a changed macro file of the build injected a script that ran at the end of the configure step; the script checked the architecture, the compiler, and the packaging before it acted; and the payload sat in files of test data that no test used (S16). Four lessons hold for every build tool: a release archive is not the repository, so a file of the archive that the revision does not hold is reviewed by no one unless the release produces it again and compares (STND.BUILD.20); a build script runs with the privileges of whoever builds, so it is code, whether written by hand or generated (STND.BUILD.21); test data is able to carry code, so a step that produces a delivered output does not read it (STND.BUILD.22); and a payload that tests its environment before acting is hard for an investigator to reproduce, which a build record of each host makes easier (STND.BUILD.25). STND.BUILD.20 governs the release archives of the work. A release archive of a dependency that the work builds is a fetched component under STND.DEPS.6, and whether the work builds it from the archive or from the revision of its repository is a choice of the dependency record under STND.DEPS.1. Build-time code of a dependency is part of that dependency, which STND.DEPS governs. STND.BUILD.20 is a default: the supply-chain row of STND.THRT.2 covers the fetched components that the work depends on and not the work's own release archives, so a binding form would rest on no row of the threat model and would raise the floor (GOV.11). STND.BUILD.22 has effect where the repository configuration marks test data, which a project that keeps its tests in their own directories does by naming those directories.

A remote cache that does not track a tool installed outside the build's own inputs lets two machines give different outputs under the same key, and a variable of the environment counts only where it is listed; the same documentation advises that only the system that runs the checks write to the cache (S18b, S26) (STND.BUILD.23 and STND.BUILD.24). RSRC.7 admits reuse only where it preserves correctness and reproducibility, which a key that holds every declared input and a store that only checked builds write give. A key that holds every input of a step that reads a secret holds that secret or a digest of it, which a store shared between hosts discloses, so the second sentence of STND.BUILD.23 keeps the outputs of such a step out of the cache, stored and served (PRIME.10). An output that a build cache outside the provisioned environment serves is transferred into it from outside; STND.BUILD.23 and STND.BUILD.24 hold the build's part, and the term Fetched component of STND.DEPS decides whether STND.DEPS.6 also applies to it. A cache that served a wrong output is not able to show which other entries are wrong, so the second sentence of STND.BUILD.24 stops all reads from it; the cache stays as the evidence from which QA.13 identifies what relied on it, and its later disposal, after an archive of it, is an irrecoverable action under GUARD.5, reserved to the human owner (PRIME.6), unless an exempt class of STND.DFLT.15 applies to it.

The build record gathers in one record what REPRO.1, REPRO.2, STND.DEPS.8, and STND.OFFLD.24 ask of a build, and adds the items that the sources show to change the outputs of a build: the linker and the other tools of the toolchain, the system root, the build host, the detected properties, the settings, the environment, and the digests of the outputs. One distribution's record of a build gives the architecture of the build machine, the installed packages that might affect the build, the environment variables known to affect it, and digests of all files that make up the build, and a framework of supply-chain levels adds the external parameters and the resolved dependencies (S6, S19) (STND.BUILD.25). PRIME.10 keeps every secret out of a record and out of an environment capture, so the Environment row names a variable that holds a secret without its value. The integrity digest of an output links it to its build record, and a result whose record gives that digest, or the identity of its computational environment as REPRO.1 asks, traces through the build record to each input of the build. For a realization of a hardware design, the design record of HDES.3 is the record of its transformation steps, and a second record of the same step does not arise. A record that lists each item and names no tool is the form that holds across build tools. A matrix of build configurations is a declared set with a rule for each failure, and the axes that change results are the toolchains, the build configurations, the checking builds, the target platforms, the hardware models of device code, and the optional features, of which a build without OpenMP (STND.OMP.4) and the oldest and newest declared releases (STND.PY.14) are two instances (S29) (STND.BUILD.26). A combination left out for its cost is a regime that the checks do not cover, and the second sentence of STND.BUILD.26 states it as INTPR.10 asks; a release inside a declared range whose oldest and newest members a build configuration builds is stated by stating that range once, as the same sentence admits.

Under STND.CLASS.10, each provision instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, QA, or HW.5, and applies from CSQ3; work of CSQ4 may omit it. The part of a provision that rests on a row of the table of STND.CLASS.10 applies from the class of that row. STND.BUILD.21 rests on REPRO.10, the versioning and review of each workflow, and applies from CSQ2. The second sentence of STND.BUILD.25 rests on REPRO.4 and applies from CSQ2. The second sentence of STND.BUILD.26 documents a limit of what the checks cover, rests on INTPR.10, and applies from CSQ2. The comparisons of STND.BUILD.3, STND.BUILD.5, STND.BUILD.19, and STND.BUILD.20 compare outputs of the work with other outputs of the work, and not with a reference oracle, and ask for no regeneration by another actor under QA.9, so they rest on no row and apply from CSQ3. The second sentence of STND.BUILD.24 rebuilds the outputs that a found fault reaches, as QA.13 asks, and asks for no mechanism that tracks dependencies between results, which the row of QA.14 covers, so it applies from CSQ3. STND.BUILD.10 declares the targets for which a build compiles, under SIMPL.6, and states no behavior of hardware that a result relies on, which a contract of DSGN.5 states, so it applies from CSQ3. The first sentence of STND.BUILD.12 asks for a mechanical check (DSGN.3) and applies from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0, stays with that row. The second sentence of STND.BUILD.12 declares behavior under SIMPL.6 and applies from CSQ3. The second sentence of STND.BUILD.13 states what the checks of a checking build do not cover, a limit of validity of a verification (INTPR.10), and applies from CSQ2, as STND.CONC.27 does; it asks for neither a reference oracle nor a proof, which the rows of VV.1 cover. STND.BUILD.11 instantiates HW.5, which the Notes of HW apply from CSQ3. Every other provision and sentence rests on no row and applies from CSQ3. No provision binds, and none raises the floor (GOV.11): each is a default that asks only what REPRO, DSGN, SIMPL, RSRC, INTPR, VV, QA, or HW.5 already ask, at the cost of wording, a setting, a check, or one record, and the verification of fetched components, the authorization of network access, and the exclusion of secrets from records already bind through STND.DEPS.6, PRIME.7, and PRIME.10.

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES | Hardware design |
| HW | Execution hardware |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.ANNEX | Hardware type annex |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DFLT | Defaults |
| STND.JL | Julia standard |
| STND.OFFLD | Accelerator offload standard |
| STND.OMP | OpenMP standard |
| STND.PY | Python standard |
| STND.THRT | Threat-model template |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| STND.WFLOW | Workflow and long-run resilience standard |
| VV | Correctness |

## Provisions

### Inputs

#### STND.BUILD.1 Declared inputs of build steps

Default. Instantiates REPRO.1, SIMPL.6.

The declared inputs of each build step SHOULD include each file, tool, execution setting, and variable of the environment that the step reads and that is able to change one of its outputs (REPRO.1, SIMPL.6).

#### STND.BUILD.2 Inputs derived from the source

Default. Instantiates REPRO.1, SIMPL.6.

Where a build step reads files, modules, or other units that its source names, the declaration of what it reads as inputs of that step SHOULD be derived from the source at each run of the step, by the tool that reads it or by a tool that scans it (REPRO.1, SIMPL.6).

#### STND.BUILD.3 Schedule-independent build outputs

Default. Instantiates REPRO.3, QA.4.

The outputs of an incremental build, and of a build that runs its steps in parallel, SHOULD be the same as those of a clean build that runs its steps one at a time from the same declared inputs, within the variation that the build record declares (REPRO.3). Each difference beyond that variation SHOULD be recorded in defect tracking as a defect of the build (REPRO.3, QA.4).

#### STND.BUILD.4 Generated files and generators

Default. Instantiates REPRO.1.

Each generated file SHOULD be the output of a build step whose declared inputs include its generator and each input of that generator (REPRO.1). A generated file SHOULD be changed only by running its generator again (REPRO.1).

#### STND.BUILD.5 Generated files under version control

Default. Instantiates VV.8, REPRO.3.

Where the version history of the work holds a generated file, the checks of each change SHOULD generate that file again from its declared inputs and fail on each difference from the file held that the build record does not declare as variation (VV.8, REPRO.3).

#### STND.BUILD.6 Builds outside the source tree

Default. Instantiates REPRO.1, DSGN.16.

Other than the update of a generated file that the version history holds, made by running its generator, each build SHOULD write its outputs and its generated files only into its build tree, apart from the source tree (REPRO.1, DSGN.16).

#### STND.BUILD.7 Fetching apart from building

Default. Instantiates REPRO.1, SIMPL.6.

Each fetched component that a build reads SHOULD be fetched before the build begins, by a step apart from the build (REPRO.1). Where a declared input of a build step is absent, the build SHOULD stop with a diagnostic that names that input (SIMPL.6).

### Configuration

#### STND.BUILD.8 Detected configuration properties

Default. Instantiates SIMPL.6, REPRO.2.

Each property of the build host or of the target platform that a configure step detects, and that is able to change a result, SHOULD be either required by the build description, so that its absence stops the build, or recorded as absent in the build record (SIMPL.6, REPRO.2). The build description SHOULD let an option of the build set each such property in place of its detection (SIMPL.6).

#### STND.BUILD.9 Configuration of cross builds

Default. Instantiates SIMPL.6.

Where the build host does not run code of the target platform, each property of the target platform that a configure step uses SHOULD come from a value that the build description or an option of the build declares, or from a test that runs no code of the target platform (SIMPL.6). Where a build compiles a tool that a later build step runs on the build host, or code that a compiler loads and runs during compilation, the build description SHOULD state the toolchain and the execution settings of that code apart from those of the code for the target platform (SIMPL.6).

#### STND.BUILD.10 Stated device code targets

Default. Instantiates SIMPL.6.

The repository configuration SHOULD state, for each build of device code, each hardware model of accelerator for which the build compiles code, and whether the build adds code for a runtime library to compile at load (SIMPL.6). Where the repository configuration states, for a build of device code, neither such a hardware model nor a rule that takes the hardware models from the accelerators of the build host, that build SHOULD stop with a diagnostic (SIMPL.6).

### Settings

#### STND.BUILD.11 Result-affecting build settings

Default. Instantiates SIMPL.6, REPRO.2, HW.5.

The repository configuration SHOULD state, in one place for each compilation unit, each execution setting of the compilation of that unit that is able to change a result, with its value, a value that the toolchain takes by default included (SIMPL.6, REPRO.2, HW.5). The repository configuration SHOULD state, in one place for each link step, each execution setting of that step that is able to change a result, a setting that changes the floating-point control state of the whole process included (SIMPL.6, HW.5).

#### STND.BUILD.12 Warnings in checks and releases

Default. Instantiates DSGN.3, SIMPL.6.

The checks of each change SHOULD fail on each warning that a tool of the toolchain reports on the work's own source, at a set of warnings that the repository configuration records (DSGN.3). The build description that a release archive holds SHOULD make a warning fail a build only under a toolchain on which the checks of that release ran (SIMPL.6).

#### STND.BUILD.13 Checking builds kept apart

Default. Instantiates SIMPL.6, VV.1, INTPR.10.

Each checking build SHOULD be a build configuration that is named apart from the build configuration of each reporting build, and that writes into a build tree of its own (SIMPL.6). The record of each checking build SHOULD state each check that it adds, and each part of the work that it links without that check (VV.1, INTPR.10).

### Reproducibility

#### STND.BUILD.14 Embedded build instant

Default. Instantiates REPRO.1, REPRO.3.

Each date or time that a build step embeds in an output SHOULD either be an instant that the build takes from its source revision or from a declared input, or be declared in the build record as a variation of that output (REPRO.1, REPRO.3).

#### STND.BUILD.15 Fixed order of inputs

Default. Instantiates REPRO.3.

Each output of a build step that depends on the order of the inputs of that step SHOULD either take that order from an explicit list or a sort under a collation that the build description states, or be declared in the build record as varying with that order (REPRO.3).

#### STND.BUILD.16 Locale and time zone of builds

Default. Instantiates REPRO.2, REPRO.3.

Each build step whose output depends on the locale or the time zone SHOULD either run under a locale and a time zone that the build description sets, or have that output declared in the build record as varying with them (REPRO.2, REPRO.3).

#### STND.BUILD.17 Build paths in outputs

Default. Instantiates REPRO.2, REPRO.3.

Each path of the build tree or of the source tree that a build step embeds in an output SHOULD be a path at which the build record states that the build ran, a path to which the build description maps it in the outputs, or a variation of that output that the build record declares (REPRO.2, REPRO.3).

#### STND.BUILD.18 Randomness in build steps

Default. Instantiates DSGN.17, REPRO.3.

Where a build step uses randomness that is able to change an output, that randomness SHOULD either be fixed by a seed among its declared inputs, or be declared in the build record as a variation of that output (DSGN.17, REPRO.3).

#### STND.BUILD.19 Build comparisons at release

Default. Instantiates REPRO.3, VV.8, QA.4.

The checks of each release SHOULD compare the outputs of two clean builds made from the same declared inputs at different times, and compare the outputs of an incremental build and of a parallel build with those of a clean build that runs its steps one at a time (REPRO.3, VV.8). Each difference between the outputs of the two clean builds SHOULD be stated in the build record with its source, or recorded in defect tracking as a defect (REPRO.3, QA.4).

### Releases

#### STND.BUILD.20 Release archives from the revision

Default. Instantiates REPRO.1, VV.8, REPRO.3.

Each release archive SHOULD be produced by a build step of the build description from the revision that its release names (REPRO.1). The checks of each release SHOULD produce again, from that revision, each file of its release archives that the revision does not hold, and fail on each difference from the file in the archive that the build record does not declare as variation (VV.8, REPRO.3).

#### STND.BUILD.21 Build scripts as code

Default. Instantiates REPRO.10, QA.7.

Each build script of the work SHOULD either be held under version control and reviewed as code of the work at each change to it, or be generated by a build step from inputs that are so held and reviewed (REPRO.10, QA.7).

#### STND.BUILD.22 Exclusion of test data

Default. Instantiates DSGN.8.

A build step that produces an output that the work delivers SHOULD NOT read a file that the repository configuration marks as test data (DSGN.8).

### Caches

#### STND.BUILD.23 Build cache keys

Default. Instantiates RSRC.7, REPRO.1.

A build cache SHOULD serve an output only under a key that holds the identity and revision of each tool of the build step that produced it, the execution settings of that step, a digest of the value of each variable of the environment that the step reads and that is able to change its outputs, and the integrity digest of each of its other declared inputs (RSRC.7, REPRO.1). Where a build step reads a secret, the outputs of that step SHOULD be kept out of each build cache, neither stored in it nor served from it (RSRC.7, PRIME.10).

#### STND.BUILD.24 Shared build cache writers

Default. Instantiates RSRC.7, QA.13.

Each build cache that more than one host reads SHOULD accept outputs only from the builds that the checks of the work run (RSRC.7). Where an output that a build cache served is found wrong, the work SHOULD stop taking outputs from that cache, keep the cache until each output that relied on it is identified, and build again each output that it served and on which a result still relies (RSRC.7, QA.13).

### Records

#### STND.BUILD.25 Build record

Default. Instantiates REPRO.1, REPRO.2, REPRO.4.

Each reporting build SHOULD have one build record with the content of the table of this provision (REPRO.1, REPRO.2). The build SHOULD write that record with its outputs, at their production (REPRO.4).

| Item | Content |
| --- | --- |
| Source | The revision of the source, and whether the source tree held changes that the revision does not hold |
| Configuration | The build configuration; each option that the build was given, with its value, other than an option that holds a secret, which the record names without its value (PRIME.10); and each property that its configure steps detected, with its value or its absence |
| Toolchain | Beside the revisions that STND.DEPS.8 asks for, each linker, archiver, generator, and other tool that a build step ran, with its revision, and the system root, with its identity |
| Hosts | The build host, by its operating system and hardware model; the target platform; and, where the build took its hardware models of device code from the accelerators of the build host, the identity of that host |
| Settings | The value of each execution setting that is able to change a result, for each compilation unit and each link step |
| Environment | Each variable of the environment that a build step read and that is able to change an output, with its value, other than a variable that holds a secret, which the record names without its value (PRIME.10); the locale and the time zone; the instant that the build embedded; and the build path or the mapping applied to it |
| Dependencies | Each resolved dependency with its revision and integrity digest, or a citation of the dependency record that gives them |
| Device code | What STND.OFFLD.24 asks of the record of a build of device code |
| Outputs | The integrity digest of each output that the build delivers or from which the work reports a result |
| Kind of build | Whether the build was clean or incremental, and each output that it took from a build cache |
| Declared variation | Each output that differs between builds from the same declared inputs, with the kinds of build between which it differs, its source, and its extent |

#### STND.BUILD.26 Build configurations under check

Default. Instantiates VV.8, INTPR.10.

The repository configuration SHOULD state each build configuration that the checks of the work build and test (VV.8). Where the work admits a toolchain, a target platform, a hardware model of device code, or an optional feature that no such build configuration builds, the repository configuration SHOULD state it as unchecked, or state the declared range that holds it and whose oldest and newest members a build configuration builds (INTPR.10).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.0.1 | 2026-10-24 | Editorial amendment (GOV.41): the Purpose and the Notes cite STND.WFLOW where they named the standard for computational workflows in words, the Notes name STND.BUILD.23 as the build form of STND.WFLOW.6, and References lists STND.WFLOW; no obligation changes. |
