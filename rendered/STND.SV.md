# Verilog and SystemVerilog standard (STND.SV) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 136 (2026-10-24); revised to 1.1 in entry 152 (2026-10-25), 1.1.1 in entry 282 (2026-10-28), and 1.2 in entry 316 (2026-10-28). This reading copy is composed from the per-provision files in STND/SV/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.SV.28.

## Purpose and scope

This standard holds the practice of Verilog and SystemVerilog, in hardware descriptions that are realized and in their verification, that HDES leaves to the language. It adds to HDES, STND.CODE, STND.CONC, STND.VVUQ, and STND.DEPS only what these languages make necessary. It covers the edition of the language and the constructs in use, the settings of simulation, and the separation of the code that is synthesized from the code that only verifies (STND.SV.1 to STND.SV.4); freedom from races by construction under the order of evaluation that the language leaves unspecified (STND.SV.5 to STND.SV.8); agreement of simulation and synthesis in sensitivity, inferred storage, selection, simulation-only constructs, width and sign, and initial values (STND.SV.9 to STND.SV.15); unknown values and the mode of a check of equivalence (STND.SV.16, STND.SV.17, and STND.SV.18); assertions and coverage (STND.SV.19 to STND.SV.22); seeds of random stimulus (STND.SV.23); and the classes of finding that the static checks report, a second route for the check of the netlist and for the verdicts of simulation, and comparisons between simulators (STND.SV.24 to STND.SV.27).

Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). Silent saturation and wrap-around bind at every class through HDES.14 and PRIME.4, and the observed completion and failure of each concurrent task of a testbench bind at every class through STND.CONC.1 and STND.CONC.2, as the responses to a failure that PRIME.4 lists bind through STND.CODE.14 and the checks that CPS.5 or CPS.9 requires are not removable by an execution setting through STND.CODE.16; this standard adds nothing to that floor. The standard is agnostic of simulator, synthesis tool, checker, vendor, and target: its provisions name no tool, no product, and no revision of the language definition, and the repository configuration and the design record choose them (GOV.18). Clock-domain crossings, asynchronous inputs, and the release of asynchronous resets are governed by HDES.11 alone.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Hardware description, Design, Design record, Target, Realization, Transformation step, Netlist, and State element have the meanings that HDES gives them. Repository configuration, Static check, Execution setting, and High-assurance code have the meanings that STND.CODE gives them, and Build step the meaning that STND.BUILD gives it. Concurrent task, Event loop, Shared mutable object, Protection, and Data race have the meanings that STND.CONC gives them.

| Term | Definition |
| --- | --- |
| Language definition | The published definitions of Verilog and SystemVerilog, in each of their revisions. |
| Language edition | Of a source file: the revision of the language definition under which the repository configuration states that each tool reads the file. |
| Synthesized set | The source files of a design, and the parts of files, that a transformation step reads to produce a netlist. |
| Verification set | The source files of the verification of a design, and the parts of files, that no transformation step reads, its testbenches, checkers, and models included. |
| Construct subset | Of a design: the constructs of the language definition that its design record admits in its synthesized set. |
| Simulation process | A procedure, a continuous assignment, a primitive instance, or another construct of a hardware description or of its verification set that a simulator evaluates as one unit when an event to which it is sensitive occurs. |
| Clocked process | A simulation process that an edge of a clock, or of an asynchronous reset, triggers, and that writes state elements. |
| Combinational process | A simulation process that describes logic without storage. |
| Time slot | The events that a simulator processes at one value of simulation time. |
| Simulation race | A data race between simulation processes that one time slot triggers, whose outcome depends on the order in which the simulator evaluates them, where the language definition leaves that order unspecified. |
| Unknown value | The value of a bit of four-state logic that stands for 0 or 1 without stating which. |
| High-impedance value | The value of a bit of four-state logic that no driver drives. |
| Four-state simulation | Simulation in which each bit takes the value 0, 1, the unknown value, or the high-impedance value. |
| Two-state simulation | Simulation in which each bit takes the value 0 or 1 alone, a bit assigned the unknown or the high-impedance value taking one of them by a rule of the simulator. |
| Synthesis directive | A comment, attribute, or setting that changes what a transformation step produces from a construct and leaves the simulation of that construct unchanged. |
| Equivalence mode | The rule by which a check of equivalence compares an unknown value of one representation of a design with the corresponding value of the other. |
| Concurrent assertion | An assertion on a clock that reads the values that its variables held at the start of the time slot of its clock event, and that is evaluated after the design has settled in that time slot. |
| Immediate assertion | An assertion that is evaluated on the current values of its variables when the procedure that holds it reaches it. |

## Notes

The provisions rest on facts that have held since the first revision of the language definition and hold for every event-driven simulator: the order in which a simulator evaluates the simulation processes that one time slot triggers is unspecified; simulation and synthesis read some constructs differently; an unknown value means one thing to a simulator, another to synthesis, and a third to a check of equivalence; a seed reproduces random stimulus only while the structure that draws from it is stable; tools lag the language definition; and tools have defects (research/hdl-notes/h1-verilog-systemverilog.md, "Timeless versus moving"). What still moves, the constructs of each revision, which tools implement which constructs, the reach of two-state simulation, and the names, options, and warnings of tools, is left to the records that STND.SV.1, STND.SV.2, and STND.SV.3 ask for. This standard defines Language edition, of a source file and of the language definition, and does not import the Edition in force of STND.CXX, which is of a translation unit and of the ISO C++ standard and which STND.CXX.4 has the repository configuration state, so that the two terms differ in name as they differ in scope. The research note did not retrieve the published text of the language definition, so each statement of what it says comes from a paper by a participant in the standards work; five of its sources were read as extracts that a retrieval tool wrote, which the note says. A fact that the note does not support is marked unverified.

The standard adds the content of the language to provisions that already hold the outcome, and does not restate them (GOV.31). HDES.3 keeps the design record with the revision, settings, and seeds of each tool of each transformation step, and STND.DEPS.8 records the revision of each synthesis tool with each result. Where a simulator compiles a hardware description or a netlist before it runs it, that compilation is a build step of STND.BUILD, as each automated transformation step is: STND.BUILD.1 governs its declared inputs, and STND.BUILD.11 has the repository configuration state each of its execution settings that is able to change a result. STND.SV.3 has the record of each verification state, for each simulator, whether it runs four-state or two-state simulation, the value that two-state simulation gives a bit assigned the unknown or the high-impedance value, the time precision, and each setting that changes how it evaluates unknown values, whether set at that compilation or at the run; STND.BUILD.11 has the repository configuration state every other execution setting of that compilation that is able to change a result. The netlist that STND.SV.25 simulates is an output of a transformation step, whose record is the design record of HDES.3, as the Notes of STND.BUILD state of the record of transformation steps. HDES.6 asks for verification against the contract with a verdict per property, coverage by a named measure, and each bounded proof or timeout left inconclusive; HDES.8 for a check of the netlist against the verified description, and the parts it leaves uncompared named as unverified; HDES.9 for each warning of a transformation step resolved or matched by a recorded rule, and accepts the evidence of a check of equivalence only where it reads the description as the verification did; HDES.12 for a defined initial state verified from unconstrained states; and HDES.7 and HDES.14 for arithmetic and visible saturation. HDES.11 holds clock-domain crossings, asynchronous inputs, and the release of an asynchronous reset, and this standard cites it and adds nothing to it. Hardware descriptions and testbenches are code under STND.CODE, so the static checks of each change and the suppression of each finding with its reason (STND.CODE.4), a layout tool (STND.CODE.5), a regression test per fix (STND.CODE.8), repeatable verdicts with recorded seeds (STND.CODE.9), and statements grouped by step in each process (STND.CODE.13) already apply, and for high-assurance code the coding standard, the claims of conformance, the edition with the validation of each tool that synthesizes or simulates it, and the deviations (STND.CODE.17 to STND.CODE.20). An intellectual-property block and a library of verification methodology are dependencies under STND.DEPS, with their revisions recorded. The comments and documents of the hardware descriptions and testbenches of the work are work documentation under STND.DOCS, which STND.DOCS.11 keeps in step with them.

Concurrency. STND.CONC applies to each sequence of execution of a simulation that meets its Term Concurrent task: a simulation process runs while others of the same run have not completed, a process of a testbench that is started as a task of its own or that waits on another is one, and the kernel of a simulator, where it runs ready processes one at a time and waits for events between them, fits the Term Event loop. That a testbench starts tasks of its own and waits on others, and that a kernel runs ready processes one at a time, are not in the research note and are unverified. A variable that two simulation processes access, one by a write, is a shared mutable object, and a simulation race is a data race between simulation processes. STND.CONC.3 asks one stated protection for each such object. The protection that the languages give is their scheduling: a nonblocking assignment defers each write of clocked state until every clocked process of the time slot has read, and a nonblocking assignment, a clocking construct, or the scheduling regions that the language reserves for testbench code order a testbench against the design (h1, H1). STND.SV.5 to STND.SV.8 state that protection for the processes of a simulation, as the form that STND.CONC.3 takes for them; a design record that names STND.SV.5 to STND.SV.8 as the protection of the variables that simulation processes share is a record that a declaration is able to cite under STND.CONC.3, and the kind of each assignment and the construct of each procedure show that protection at each access. A provision of STND.CONC that has no subject in a given simulation, a pool or a count of tasks for instance, is vacuous there. STND.CONC.1 and STND.CONC.2 reach each concurrent task of a testbench on whose result its parent relies, and STND.CONC.26 reaches each protocol by which concurrent tasks of a testbench share state or wait on one another. "The order in which the primitives and processes are evaluated is not defined in the language standard", and every implementation exhibits one order of its own (h1, S1 and S2). A dependence of a verdict on that order changes the verdict and lies outside every agreement, so it is a race of the kind that the Notes of STND.CONC call a correctness defect. A dependence of a reported value on that order whose source and size the record declares, and that lies within the agreement that the acceptance criterion fixed before the comparison, is a declared variation under HW.12 and STND.VVUQ.82, and STND.VVUQ.83 keeps an agent from removing it on its own initiative; STND.SV.8 accepts it. A race in simulation differs from a race in the hardware: a glitch, or a latch of set and reset inputs released together, is physical and is handled by the design and by HDES.10 and HDES.11, while a simulation race is a consequence of the event-driven algorithm and is able to make a faulty design pass (h1, S1).

Scheduling. Two clocked processes that hand a value from one to the other by blocking assignment race, because the update of the first is able to precede the read by the second, although synthesis builds two flip-flops from the same code (h1, S2) (STND.SV.5). STND.SV.5 asks nonblocking assignment only for a variable that another process reads, so that a temporary of a clocked procedure stays free to use blocking assignment; one tool treats a variable written by both kinds of assignment as an error by default (h1, S9). The three sentences of STND.SV.5 are one discipline of assignment, the guideline that h1 cites from S1, and apply together. A combinational procedure that reads a variable before it assigns it sees the previous value, and one tool warns that "results may vary between simulators" (h1, S9) (the second sentence of STND.SV.6). A net with more than one driver resolves by the rules of the language, a fact that the research note does not hold and that is unverified, and is not a variable under STND.SV.6; the warnings of such a net fall under HDES.9. A zero delay was once used to place a write after a read, and works only through the ordering that most simulators happen to give; the language later kept it with a region of its own (h1, S1 and S2) (STND.SV.7). In one revision, a variable initialized at its declaration took its value as if from an initial procedure, in an order that the definition did not fix, and a later revision moved those initializations before time zero, so a design that relies on the order at time zero passes under one revision and fails under another; a clock or a reset first driven at time zero is seen by some processes and not by others (h1, S1) (STND.SV.8). A step delay of a clocking construct is the finest time precision of the simulation, so a change of time precision in one file changes the point at which a testbench samples (h1, S1), which is why STND.SV.3 records the time precision.

Simulation and synthesis. A construct that states the intent of a procedure, `always_comb`, `always_latch`, or `always_ff` at the editions that provide them, lets a tool report at compilation a latch or a flip-flop that the author did not intend; the committee record gives as intent that `always_comb` infers neither a latch nor a flip-flop, that `always_ff` infers at least one flip-flop, and that tools may check more, and the exact checks that the language definition requires are unverified (h1, S20 and S9) (STND.SV.9). A sensitivity list written by hand simulates differently from the logic that synthesis builds when it misses a variable, and the wildcard form `@*`, which an early revision added, makes a procedure sensitive to every variable it reads (h1, S6). A selection statement without a default, coded for an AND function, kept its previous output in simulation for an input with an unknown bit, while the netlist gave the correct low value, and the synthesis tools studied gave no warning; whether current tools warn is unverified (h1, S15) (STND.SV.10). A rule of HDES.9 that matches the warnings of inferred latches by kind and source states those latches for STND.SV.10 where it names the procedures that it covers. A pragma comment of the form `full_case` or `parallel_case` makes synthesis assume what simulation never checks, and the qualifiers `unique` and `priority` state the same intent with a check in simulation; used without that check they carry "the same pitfalls as the synthesis full_case pragma" (h1, S6 and S19), which is why STND.SV.13 excludes such a directive and STND.SV.11 fails a test on each reported violation of a qualifier. Directives that keep a synchronizer under HDES.11 or a redundant register under HDES.15 change no selection statement and are outside STND.SV.13 and the Selection row of STND.SV.24. The research note calls the qualifiers later additions to the language, so STND.SV.11, the second sentence of STND.SV.12, and STND.SV.19 apply where the language edition provides the construct; at an edition without the qualifier, a comment that states the intended priority and a check in the testbench are what remains for STND.SV.11 and STND.SV.12, and at an edition without concurrent assertions, a recorded decision under REPRO.7 for STND.SV.19. In `casex` an unknown or high-impedance bit of the selection expression matches every item; in one worked example a stored don't-care value made simulation of the description select one item every time while simulation of the netlist selected the default in 98 percent of cycles (h1, S15) (STND.SV.12). In `casez` an unknown bit of the expression is no wildcard, but overlapping items change the result with their order (h1, S15 and S9). STND.SV.13 keeps a behavior of the contract off a delay, a forced value, and a test for an unknown value, the simulation-only constructs that the note names (h1, answer 8). That synthesis ignores delays is general knowledge that the note marks unverified, so the standard asks no ban of delays in the synthesized set; one simulator documents that it ignores timing checks, reads each delay given as minimum, typical, and maximum values as its typical value, and changes a delayed assignment in a combinational procedure to one without delay, with results that "may differ from other simulators" (h1, S9), which is the delay that the Scheduling row of STND.SV.24 reports. The revision that added signed declarations and the arithmetic shift also changed how values wider than 32 bits are extended, a published test found a synthesis tool that expanded a signed one-bit literal wrongly in a negation, and a later revision changed the result of the relational and equality operators from an integer to a single bit, so the width of an expression depends on the language edition (h1, S6, S11, and S3) (STND.SV.14). STND.SV.14 rests on SIMPL.6 and reaches every extension, truncation, and change of sign in the synthesized set; HDES.7 governs the arithmetic of operations that approximate a real-valued computation, and an explicit truncation that is not the specified function of its operation stays under HDES.14. A declaration initializer or an initial procedure gives a state element a value in simulation whether or not the target gives it that value at power-on, which depends on the target (h1, S9 and S1); HDES.12 holds the obligation, and STND.SV.15 keeps such a value from counting as its evidence, the gap G2 of the note. A statement in the design record that the target gives that value is a property of the target, and HW.6 marks the evidence on which it rests.

Unknown values. An unknown value is a don't-care to synthesis, an unknown to simulation, a wildcard in two forms of selection, and, to a check of equivalence, either a free choice or a value that matches only itself; "The most worrying thing is that there are different semantics!" (h1, S15). A condition that takes the false branch on an unknown value, and a selection that keeps its previous value when no item matches, are optimistic: they hide a defect that a simulation of the netlist or the device shows. Reconvergent logic that turns a known result into an unknown at gate level is pessimistic: it shows a difference that the hardware does not have (h1, S16). Randomized initial values are "a good solution for addressing X-pessimism issues, but not for detecting correct initialization and X-optimism issues" (h1, S16), and one simulator that is mostly two-state turns an assigned unknown into a constant chosen by an option (h1, S9), which is why STND.SV.17 counts neither as its check and STND.SV.3 records which kind of simulation each verdict comes from. STND.SV.17 asks the check where the means of the work include one, so that a work without a proof tool or such a setting is not blocked. That quotation limits what counts as the check of STND.SV.17 for optimism; it leaves the verification from a recorded number of random states that HDES.12 accepts for the defined initial state as it stands. A check of equivalence that lets each unknown value match either value reported the latch example above equivalent to the likely netlist; the author of that study recommends the mode that matches an unknown value only with an unknown value, and the analysis of each failure that passes only in the other mode, and names the two modes "2-state consistency" and "2-state equality", names that differ between tools (h1, S15) (STND.SV.18). An equivalence in a mode that resolves an unknown value otherwise than the simulation did does not interpret the description as the verification did, so the record of the mode is what lets HDES.9 decide whether that evidence counts. The three sentences of STND.SV.18 are one procedure, the record of the mode, the run in the strict mode, and the analysis of its failures, and apply together.

Assertions and coverage. An invariant assertion on two clocks evaluated as values change in one time slot fires falsely when one clock rises before the other falls in that slot; the remedy of the language samples at the start of the time slot and evaluates after the design has settled (h1, S2 and S1), which a concurrent assertion does and an immediate assertion does not (STND.SV.19). "It is a requirement, that code executed by assertions must not be allowed to change the state of the design" (h1, S2). Whether an assertion decides its verdict in simulation, in proof, or in both is the record that S2 and S7 support (the first sentence of STND.SV.20). A proof tries every sequence of inputs that its constraints admit, and a constraint written wrong admits too few, so a proof that holds under an over-constrained environment shows nothing outside it (h1, S16) (the second sentence of STND.SV.20); HDES.6 already leaves a bounded proof inconclusive. Code coverage "can give both optimistic results (claims a branch is covered when it's unreachable) and pessimistic results" (h1, S15), which is the gap G1: HDES.6 asks for a named measure and not for what it counts on an unknown value (STND.SV.21). Coverage defined from the classes that generate stimulus is able to measure the stimulus rather than the design, a practice that the note derives from S3 (h1, H6) (STND.SV.22). The research note retrieved no primary text on vacuous passes of assertions, or on the clock and disabling condition that its answer 18 joins to them, so the standard holds no provision on them; HDES.6 leaves each inconclusive verdict uncovered.

Random stimulus. The language gives each process and object of a testbench its own random generator, seeded hierarchically from one seed, so that an unrelated edit does not disturb another stream; in one study three simulators initialized static processes and objects differently, "none of these implementations follow the standard exactly", and the language definition does not specify the generator (h1, S8). A seed therefore reproduces stimulus on one simulator at one structure of the testbench (STND.SV.23), and a comparison between simulators does not compare stimulus drawn from one seed (STND.SV.27). The streams of the processes of a testbench are the random streams of a computation divided among concurrent tasks, the matter that NUMER.2 gives to NUMER through NUMER.24 from revision 1.3 of NUMER. STND.CONC.23 keys each stream to a part of the computation, independently of the number of tasks and of the task that computes the part, and STND.VVUQ.62 gives the derivation of each stream from a root seed; STND.SV.23 is their form for a testbench. The hierarchical seeding of the language keys a stream to the place of its process or object in the testbench (h1, S8). It meets STND.CONC.23 where each such process or object generates one part of the stimulus and keeps its place whatever the number of tasks; otherwise the derivation of STND.VVUQ.62 from a key of the part is the form of STND.SV.23 that remains. The width of the seed that the language gives is not in the research note and is unverified; a seed narrower than STND.VVUQ.62 asks is a departure from that default under REPRO.7. A constrained random test of a deterministic design judges a verdict per property and compares no estimate of a stochastic result with a tolerance, so it is neither a test of a stochastic result under STND.VVUQ.64 and STND.VVUQ.65 nor a comparison of a stochastic result under NUMER.26, and the coverage of HDES.6 states how far its runs reach. A failed verdict of such a test is a defect of the design or of its verification under the stimulus of that seed, and a later run with another seed that passes leaves that defect in place. A test of a design that compares an estimate with a tolerance, a measured rate of errors among them, compares a stochastic result, and NUMER.26 governs it. STND.SV.23 cites NUMER.24 for the construction of independent streams, which a testbench takes as a default. STND.CODE.9 already asks for the seed in the record of each test; STND.SV.23 adds the derivation of every stream from that seed and the record of a change that alters the stream.

Checks and second routes. A structural analysis "cannot determine if a real issue exists and does not include any sequential analysis" (h1, S16), and one tool sorts its warnings into those of lint alone, those of style, and those that affect simulation (h1, S9). The table of STND.SV.24 states the classes of finding that a run of static checks covers for these languages, from the hazards of the note, and not a tool or its options; which linter runs is configuration. The second sentence of STND.SV.24 makes a class that no tool available to the work reports visible, and the work is not blocked for want of a tool. STND.CODE.4 already has each finding resolved or suppressed at its location with its reason. The warnings of synthesis are warnings of a transformation step under HDES.9, among them an inferred latch, a truncation of width, and a signal with more than one driver. Tools lag the language: users kept to the syntax of the first revision because support for the second "had been so inconsistent", and tools accept in constant expressions functions that the definition forbids (h1, S3); STND.SV.2 records the constructs that a tool does not support or reads differently.

Tools have defects. A random-program tester, run for 18,000 CPU hours on five synthesis tools, found seven programs synthesized wrong and three crashes, with sign handling and width among the causes, and a defect in a simulator used to check; a later tester reported 15 defects in five months, nine confirmed as new (h1, S11 and S12). A defect that synthesis and the check of equivalence share, by reading the description the same way, is hidden from that check (h1, S11). STND.SV.25 adds a second route to the check of HDES.8 when it is a check of equivalence and a simulator reads the netlist: a simulation of the netlist judged against the verdicts of the description, a reference produced without the netlist. A difference that comes from pessimism on the netlist is a finding of its own kind, which S16 classifies apart and removes by initializing the state that holds real unknowns (h1, S16). STND.SV.26 has another simulator, where the work has one, decide again from the record the properties that a realization relies on before that reliance, because one simulator's verdict carries its defects, and admits a proof in its place; counts of defects in simulators beyond S11 rest on slides and a summary and are unverified (h1, S24). A second simulator that is two-state, or that lacks a construct of the design, decides only the properties that rest neither on four-state values nor on that construct, which STND.SV.3 and STND.SV.2 record. A second tool that costs money is an expenditure under PRIME.8, and a work with no second simulator available is outside the first sentence of STND.SV.26.

Names. The research note retrieved no convention of names that the language definition fixes, and that none exists is unverified, so STND.CODE.28 leaves the convention of Verilog and SystemVerilog source to the repository configuration and keeps the names that the notation of NUMER.4 fixes, and this standard adds no table.

The research note retrieved no primary text on the coding of state machines, on interfaces and packages, on the checking of parameters and the semantics of generate constructs, on the styles of reset, or on vacuity, and the standard holds no provision on them. HDES.12 and HDES.15 govern the initial state and the mitigation of faults of a state machine, HDES.11 the release of a reset, and HDES.6 and HDES.12 the verification of reset.

Class onset. Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, DSGN, SIMPL, QA, or a provision of HDES or NUMER, and applies from the class that its field `onset` gives, which work of CSQ4 may omit, where a field that gives CSQ3 for what a reader needs to read a verdict or a coverage figure that HDES.6 or HDES.8 already asks at CSQ3, content that the row of INTPR.10 starts at CSQ2, tightens above the floor (PRIME.15), so that each record to which those sentences add keeps one onset. No provision binds, and no provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HW | Execution hardware |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Language and records

#### STND.SV.1 Language edition stated

Default, from CSQ3. Instantiates REPRO.2, SIMPL.6.

The repository configuration SHOULD state the language edition of each source file of a design and of its verification set (REPRO.2, SIMPL.6). Where a tool that reads such a file offers a setting that selects a revision of the language definition, the repository configuration SHOULD run that tool on the file under the setting for its language edition (REPRO.2, SIMPL.6).

#### STND.SV.2 Construct subset stated

Default, from CSQ3; sentence 2 from CSQ2. Instantiates REPRO.2, HDES.3, DSGN.5, INTPR.10.

The design record under HDES.3 SHOULD state the construct subset of each design (REPRO.2, HDES.3). For each tool on whose output a verdict of HDES.6 or a check of HDES.8 relies, the design record SHOULD state each construct of the design or of its verification set that the documentation of that tool states as unsupported, or as read differently from the language definition (DSGN.5, INTPR.10).

#### STND.SV.3 Simulation settings stated

Default, from CSQ3. Instantiates REPRO.2, HDES.6.

The record of each verification under HDES.6 SHOULD state, for each simulator that it uses, whether that simulator runs four-state or two-state simulation, and, for two-state simulation, the value that it gives a bit assigned the unknown or the high-impedance value (REPRO.2, HDES.6). That record SHOULD state the time precision of each simulation, and each setting of a simulator that changes how it evaluates unknown values (REPRO.2).

#### STND.SV.4 Verification constructs kept apart

Default, from CSQ3. Instantiates SIMPL.6, DSGN.3.

The repository configuration SHOULD list the synthesized set of each design (SIMPL.6). Classes, randomization, data types whose size changes during simulation, program blocks, and hierarchical references SHOULD appear only in the verification set (SIMPL.6, DSGN.3).

### Scheduling

#### STND.SV.5 Assignment kind by process

Default, from CSQ3. Instantiates DSGN.15.

Each variable that a clocked process writes and that another simulation process reads SHOULD be written by nonblocking assignment (DSGN.15, STND.CONC.3). Each variable that a combinational process writes SHOULD be written by blocking assignment (DSGN.15). A variable SHOULD NOT be written by both blocking and nonblocking assignment (DSGN.15).

#### STND.SV.6 Writing processes and reads

Default, from CSQ3. Instantiates DSGN.15, DSGN.14.

Each variable of the synthesized set SHOULD be written by one simulation process alone (DSGN.15, DSGN.14). Each combinational procedure SHOULD assign each variable that it writes before it reads that variable (DSGN.15).

#### STND.SV.7 Order from scheduling regions

Default, from CSQ3. Instantiates DSGN.15.

Each order between simulation processes on which a design or its verification set relies SHOULD come from the kinds of assignment and the scheduling regions that the language definition gives, and not from a delay (DSGN.15, STND.CONC.3). A testbench SHOULD drive the inputs of a design, and sample its outputs, through a facility that the language definition at its language edition orders against the evaluation of the design, a nonblocking assignment, a clocking construct, or the scheduling regions reserved for testbench code among them (DSGN.15).

#### STND.SV.8 Start-up after time zero

Default, from CSQ3. Instantiates DSGN.15, REPRO.3.

Other than a reported value whose dependence the record of the simulation declares as STND.VVUQ.82 provides, the values and verdicts of a simulation SHOULD NOT depend on the order in which the simulator starts procedures, continuous assignments, and declaration initializers at time zero (DSGN.15, REPRO.3). The first transition of each clock and each reset that a testbench drives, to which a simulation process of the design is sensitive, SHOULD occur after time zero (DSGN.15).

### Simulation and synthesis

#### STND.SV.9 Process intent declared

Default, from CSQ3. Instantiates SIMPL.6, DSGN.3.

Where the language edition provides constructs that state that a procedure describes combinational logic, a latch, or clocked storage, each procedure of the synthesized set SHOULD use the construct that states what it describes (SIMPL.6, DSGN.3). Where a combinational procedure of the synthesized set uses no such construct, it SHOULD be made sensitive by a form of sensitivity that includes each variable that the procedure reads (SIMPL.6, DSGN.3).

#### STND.SV.10 Storage only by decision

Default, from CSQ3. Instantiates SIMPL.6, VV.1.

In each combinational procedure of the synthesized set, each variable that the procedure writes SHOULD be assigned on every path through it, by an assignment before its selection statements or by an assignment in each branch (SIMPL.6, VV.1). Each latch that the synthesized set describes SHOULD be stated in the design record with the procedure that describes it, or by a rule of HDES.9 that names that procedure (SIMPL.6).

#### STND.SV.11 Selection qualifiers checked

Default, from CSQ3. Instantiates SIMPL.6, VV.1.

Where the language edition provides qualifiers that state that the items of a selection statement are mutually exclusive or tested in order of priority, each selection statement whose items are meant to be so SHOULD state it by the qualifier that simulation checks (SIMPL.6, VV.1). Each violation of such a qualifier that a simulation under HDES.6 reports SHOULD fail the test that ran it (VV.1).

#### STND.SV.12 Wildcard selection limited

Default, from CSQ3. Instantiates VV.1, SIMPL.6.

The synthesized set SHOULD hold no selection statement that matches an unknown value of its selection expression as a wildcard (VV.1). Where the language edition provides the qualifier of STND.SV.11, each selection statement of the synthesized set whose items hold wildcard bits and overlap SHOULD state their priority by that qualifier (SIMPL.6).

#### STND.SV.13 Simulation-only constructs

Default, from CSQ3. Instantiates VV.1, SIMPL.6.

Each behavior that the contract of a design under HDES.4 states SHOULD be independent of each delay, each forced value, and each test for an unknown value in the source (VV.1). The synthesized set SHOULD hold no synthesis directive that changes the logic that a transformation step produces from a selection statement (SIMPL.6, VV.1).

#### STND.SV.14 Explicit width and sign

Default, from CSQ3. Instantiates SIMPL.6.

Where an assignment or an operation of the synthesized set extends, truncates, or changes the sign of a value, the source SHOULD state that extension, truncation, or change explicitly (SIMPL.6).

#### STND.SV.15 Initial values as evidence

Default, from CSQ3. Instantiates VV.1, HDES.12.

Where the design record does not state that the target gives a state element at power-on the value that a declaration initializer or an initial procedure of the synthesized set gives it in simulation, the verification of HDES.12 SHOULD NOT rely on that value (VV.1, HDES.12). The verification of HDES.12 SHOULD NOT count a value that a simulator gives a state element at the start of a simulation as a value that the design sets (VV.1, HDES.12).

### Unknown values

#### STND.SV.16 Intended unknown values

Default, from CSQ3. Instantiates SIMPL.6, VV.1.

Each assignment of an unknown value in the synthesized set SHOULD be stated, at its location or in the design record, as the assignment of a value on which the design does not rely (SIMPL.6). The verification of HDES.6 SHOULD show, for each such assignment, that it is unreachable, or that the value it assigns reaches no output or state element on which a behavior of the contract relies (VV.1).

#### STND.SV.17 Masked unknown values detected

Default, from CSQ3. Instantiates VV.1, HDES.6.

Where the means of the work include a check, by proof or by simulation under a setting that evaluates both values of an unknown control, that reports each condition and selection of the synthesized set whose simulation turns an unknown value of its control into a known result, the verification of HDES.6 SHOULD include that check (VV.1, HDES.6). A simulation from randomized initial values, or under two-state simulation, SHOULD NOT be counted as that check (VV.1).

#### STND.SV.18 Equivalence mode stated

Default, from CSQ3. Instantiates VV.5, INTPR.10, VV.1, HDES.8.

The record of each check of equivalence under HDES.8 SHOULD state its equivalence mode (VV.5, INTPR.10). Where the tool of such a check provides a mode that matches an unknown value only with an unknown value, the check SHOULD run in that mode (VV.1, HDES.8). Where such a check fails in that mode, each output and state element on which it fails SHOULD be resolved, or shown by a simulation of the netlist or by a proof to behave as the verification of HDES.6 shows the hardware description to behave (VV.1, HDES.8).

### Assertions and coverage

#### STND.SV.19 Sampled assertions

Default, from CSQ3. Instantiates DSGN.15, VV.1.

Where the language edition provides concurrent assertions, each assertion that decides in simulation a property relating values that change at a clock event SHOULD be a concurrent assertion on that clock (DSGN.15, VV.1). The action of an assertion SHOULD NOT write a variable of the design (VV.1).

#### STND.SV.20 Assertion and assumption records

Default, from CSQ3. Instantiates VV.5, INTPR.10, HDES.6, VV.1.

The record of the verification of HDES.6 SHOULD state, for each assertion that decides a verdict, whether it decides that verdict in simulation, in proof, or in both (VV.5, INTPR.10, HDES.6). Each assumption on the inputs of a design under which a proof of HDES.6 holds SHOULD be stated in the record of that proof, with the limit or property of the contract under HDES.4 that admits it (VV.1, INTPR.10).

#### STND.SV.21 Coverage counting stated

Default, from CSQ3. Instantiates VV.5, INTPR.10, HDES.6.

Each coverage figure that the record of HDES.6 states SHOULD state whether its measure counts a branch taken on an unknown value of its condition, and whether it counts items that no reachable state of the design reaches (VV.5, INTPR.10, HDES.6). Each item that a coverage figure excludes SHOULD be listed in that record with its reason (VV.5, INTPR.10).

#### STND.SV.22 Functional coverage from the contract

Default, from CSQ3. Instantiates VV.1, HDES.6.

Each item of functional coverage that the record of HDES.6 counts SHOULD be defined from a property or a limit of the contract under HDES.4, apart from the code that generates stimulus (VV.1, HDES.6).

### Random stimulus

#### STND.SV.23 Seeded random stimulus

Default, from CSQ3. Instantiates REPRO.1, REPRO.3, NUMER.24, VV.3.

Each stream of random values that a testbench draws SHOULD be keyed to the part of the stimulus that it generates, as STND.CONC.23 asks, and derived from the seed that the record of the run states, by the hierarchical seeding of the language definition or by a derivation that STND.VVUQ.62 recommends (REPRO.1, REPRO.3, NUMER.24). Where a change alters the stimulus that a recorded seed generates in a test that runs at that seed, the record of that change SHOULD state it (REPRO.3, VV.3).

### Checks and second routes

#### STND.SV.24 Static check classes

Default, from CSQ3; sentence 2 from CSQ2. Instantiates DSGN.3, INTPR.10.

The static checks that the repository configuration names for each hardware description and its verification set SHOULD report each finding of each class of the table of this provision that a tool available to the work reports (DSGN.3). The repository configuration SHOULD name each class of the table that no tool available to the work reports (INTPR.10).

| Class | Findings |
| --- | --- |
| Scheduling | A variable of the synthesized set that more than one simulation process writes; a variable written by both blocking and nonblocking assignment; a blocking assignment, in a clocked process, to a variable that another simulation process reads; a delay in a combinational procedure; a variable that a combinational procedure reads before it writes it |
| Inferred storage | A latch or a flip-flop inferred from a procedure whose construct states combinational logic; a latch that neither the design record nor a rule of HDES.9 states; a combinational procedure whose sensitivity is listed by hand |
| Selection | A variable that a combinational procedure does not assign on every path; a selection statement that matches an unknown value of its expression as a wildcard; overlapping items of a selection statement without a stated priority; a synthesis directive on a selection statement |
| Width and sign | An extension, truncation, or change of sign that an assignment or an operation makes without stating it |
| Construct sets | A construct of STND.SV.4 in the synthesized set; a construct outside the construct subset or the language edition of its file |

#### STND.SV.25 Netlist simulated after equivalence

Default, from CSQ2. Instantiates VV.1.

Where a simulator available to the work reads the netlist that a check of equivalence under HDES.8 compares, a simulation of that netlist SHOULD run a set of tests of the verification of HDES.6 that the record of that verification lists, and give each of them the verdict that the test gives on the hardware description (VV.1).

#### STND.SV.26 Second simulator for reliance

Default, from CSQ1. Instantiates VV.1, QA.9.

Where a simulator other than the one that decided a property of the contract of a design by simulation alone in the verification of HDES.6 is available to the work, that simulator SHOULD decide the property again from the record of that verification, with the same verdict, before a realization of the design is first relied upon or submitted for fabrication (VV.1, QA.9). A proof of such a property MAY take the place of its decision by that other simulator (VV.1).

#### STND.SV.27 Simulator comparisons and seeds

Default, from CSQ3. Instantiates REPRO.3.

A comparison of the results of two simulators SHOULD NOT rely on their drawing the same random values from the same seed (REPRO.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.1 | 2026-10-25 | Minor amendment (GOV.41): new STND.SV.28 (default, from CSQ3) leaves the convention of names in the source files of a design and of its verification set to the repository configuration and keeps the names that the notation of NUMER.4 fixes, the rule of decision 9 of 2026-10-24; the Purpose lists it and names STND.CODE.14 and STND.CODE.16 among the provisions that bind at every class; Terms import High-assurance code from STND.CODE; the Notes cite STND.CODE.17 to STND.CODE.20 for high-assurance code and give the reason for the naming rule and its class onset. |
| 1.1.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields, and the tightening of the five sentences that add to a verdict or a figure is kept; no obligation, permission, or defined meaning changes. |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): STND.SV.28 is withdrawn, STND.CODE.28 holding the convention of names for Verilog and SystemVerilog source as for every language, and the front matter lists it as withdrawn; the Purpose and the Notes cite STND.CODE.28. |
