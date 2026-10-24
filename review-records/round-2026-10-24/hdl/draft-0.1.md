# Verilog and SystemVerilog standard (STND.SV) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/SV/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice of Verilog and SystemVerilog, in hardware descriptions that are realized and in their verification, that HDES leaves to the language. It adds to HDES, STND.CODE, STND.VVUQ, and STND.DEPS only what these languages make necessary. It covers the edition of the language and the constructs in use, the settings of simulation, and the separation of the files that are synthesized from those that only verify (STND.SV.1 to STND.SV.4); freedom from races by construction under the order of evaluation that the language leaves unspecified (STND.SV.5 to STND.SV.8); agreement of simulation and synthesis in sensitivity, inferred storage, selection, delays, width and sign, and initial values (STND.SV.9 to STND.SV.15); unknown values and the mode of a check of equivalence (STND.SV.16, STND.SV.17, and STND.SV.18); assertions and coverage (STND.SV.19 to STND.SV.22); seeds of constrained random stimulus (STND.SV.23); and the classes of finding that the static checks report, with a second route for the check of the netlist and for the verdicts of simulation (STND.SV.24, STND.SV.25, and STND.SV.26).

Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). Silent saturation and wrap-around bind at every class through HDES.14 and PRIME.4, and this standard adds nothing to that floor. The standard is agnostic of simulator, synthesis tool, checker, vendor, and target: its provisions name no tool, no product, and no revision of the language definition, and the repository configuration and the design record choose them (GOV.18). Clock-domain crossings, asynchronous inputs, and the release of asynchronous resets are governed by HDES.11 alone.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Hardware description, Design, Design record, Target, Realization, Transformation step, Netlist, Reference model, State element, and Clock domain have the meanings that HDES gives them. Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them.

| Term | Definition |
| --- | --- |
| Language definition | IEEE 1364 and IEEE 1800, in each of their revisions, which define Verilog and SystemVerilog. |
| Edition in force | Of a source file: the revision of the language definition under which the repository configuration states that each tool reads the file. |
| Synthesized set | The source files of a design that a transformation step reads to produce a netlist. |
| Verification set | The source files of the verification of a design, its testbenches, checkers, and models included, that no transformation step reads. |
| Construct subset | Of a design: the constructs of the language definition that its design record admits in its synthesized set. |
| Simulation process | A procedure, a continuous assignment, a primitive instance, or another construct of a hardware description or of its verification set that a simulator evaluates as one unit when an event to which it is sensitive occurs. |
| Clocked process | A simulation process that an edge of a clock, or of an asynchronous reset, triggers, and that writes state elements. |
| Combinational process | A simulation process that describes logic without storage, each variable that it writes being a function of the values that it reads when it runs. |
| Time slot | The events that a simulator processes at one value of simulation time. |
| Simulation race | A dependence of a value or a verdict of a simulation on the order in which the simulator evaluates simulation processes that one time slot triggers, where the language definition leaves that order unspecified. |
| Unknown value | The value of a bit of four-state logic that stands for 0 or 1 without stating which. |
| High-impedance value | The value of a bit of four-state logic that no driver drives. |
| Four-state simulation | Simulation in which each bit takes the value 0, 1, the unknown value, or the high-impedance value. |
| Two-state simulation | Simulation in which each bit takes the value 0 or 1 alone, a bit assigned the unknown or the high-impedance value taking one of them by a rule of the simulator. |
| Synthesis directive | A comment, attribute, or setting that changes what a transformation step produces from a construct and leaves the simulation of that construct unchanged. |
| Equivalence mode | The rule by which a check of equivalence compares an unknown value of one representation of a design with the corresponding value of the other. |
| Concurrent assertion | An assertion on a clock that reads the values that its variables held at the start of the time slot of its clock event, and that is evaluated after the design has settled in that time slot. |
| Immediate assertion | An assertion that is evaluated on the current values of its variables when the procedure that holds it reaches it. |
| Constrained random stimulus | Stimulus that a testbench draws from random generators under constraints that it states. |

## Notes

The provisions rest on facts that have held since the first revision of the language definition and hold for every event-driven simulator: the order in which a simulator evaluates the simulation processes that one time slot triggers is unspecified; simulation and synthesis read some constructs differently; an unknown value means one thing to a simulator, another to synthesis, and a third to a check of equivalence; a seed reproduces random stimulus only while the structure that draws from it is stable; tools lag the language definition; and tools have defects (research/hdl-notes/h1-verilog-systemverilog.md, "Timeless versus moving"). What still moves, the constructs of each revision, which tools implement which constructs, the reach of two-state simulation, and the names, options, and warnings of tools, is left to the records that STND.SV.1, STND.SV.2, and STND.SV.3 ask for. The research note did not retrieve the text of IEEE 1364 or IEEE 1800, so each statement of what the language definition says comes from a paper by a participant in the standards work; five of its sources were read as extracts that a retrieval tool wrote, which the note says. A fact that the note does not support is marked unverified.

The standard adds the content of the language to provisions that already hold the outcome, and does not restate them (GOV.31). HDES.3 keeps the design record with the revision, settings, and seeds of each tool of each transformation step, and STND.DEPS.8 records the revision of each synthesis tool with each result. HDES.6 asks for verification against the contract with a verdict per property, coverage by a named measure, and each bounded proof or timeout left inconclusive; HDES.8 for a check of the netlist against the verified description, and the parts it leaves uncompared named as unverified; HDES.9 for each warning of a transformation step resolved or matched by a recorded rule, and accepts the evidence of a check of equivalence only where it reads the description as the verification did; HDES.12 for a defined initial state verified from unconstrained states; and HDES.7 and HDES.14 for arithmetic and visible saturation. HDES.11 holds clock-domain crossings, asynchronous inputs, and the release of an asynchronous reset, and this standard cites it and adds nothing to it. Hardware descriptions and testbenches are code under STND.CODE, so the static checks of each change and the suppression of each finding with its reason (STND.CODE.4), a layout tool (STND.CODE.5), a regression test per fix (STND.CODE.8), repeatable verdicts with recorded seeds (STND.CODE.9), and statements grouped by step in each process (STND.CODE.13) already apply. STND.VVUQ.64 and STND.VVUQ.65 hold fixed-seed and fresh-seed tests; STND.VVUQ.82 and STND.VVUQ.83 hold a declared variation within the agreement of its acceptance criterion as no defect. An intellectual-property block and a library of verification methodology are dependencies under STND.DEPS, with their revisions recorded, and STND.DOCS governs their documentation.

The languages define the order of evaluation within a time slot only in part. "The order in which the primitives and processes are evaluated is not defined in the language standard", and every implementation exhibits one order of its own (h1, S1 and S2). A simulation race is the form that a data race of STND.CONC takes in event-driven simulation: two simulation processes access one variable in one time slot, at least one by a write, and nothing in the scheduling that the language definition gives orders them. The custodian's direction on determinism applies as it reads: a declared variation within the agreed tolerance is no defect, and a simulation race is a true race, which is a defect. The protection that orders the accesses is the scheduling of the language: a nonblocking assignment defers each write of clocked state until every clocked process of the time slot has read, and a clocking construct, or the scheduling regions that the language reserves for testbench code, orders a testbench against the design (h1, H1). STND.SV.5 to STND.SV.8 state that protection for the simulation processes of a design and of its testbench, which is the form that STND.CONC.3 takes for them; this standard does not make each simulation process a concurrent task of STND.CONC, whose provisions on locks, pools, and numbers of tasks have no subject in such a simulation. A simulator that itself runs in parallel, and software that a testbench calls, are concurrent software under STND.CONC. A race in simulation differs from a race in the hardware: a glitch, or a latch of set and reset inputs released together, is physical and is handled by the design and by HDES.10 and HDES.11, while a simulation race is a consequence of the event-driven algorithm and is able to make a faulty design pass (h1, S1).

Two clocked processes that hand a value from one to the other by blocking assignment race, because the update of the first is able to precede the read by the second, although synthesis builds two flip-flops from the same code (h1, S2) (STND.SV.5). STND.SV.5 asks nonblocking assignment only for a variable that another process reads, so that a temporary of a clocked procedure stays free to use blocking assignment; one tool treats a variable written by both kinds of assignment as an error by default (h1, S9). The three sentences of STND.SV.5 are one discipline of assignment, the guideline that h1 cites from S1, and apply together. A zero delay was once used to place a write after a read, and works only through the ordering that most simulators happen to give; the language later kept it with a region of its own (h1, S1 and S2) (STND.SV.7). In one revision, a variable initialized at its declaration took its value as if from an initial procedure, in an order that the definition did not fix, and a later revision moved those initializations before time zero, so a design that relies on the order at time zero passes under one revision and fails under another; a clock or a reset first driven at time zero is seen by some processes and not by others (h1, S1) (STND.SV.8). A step delay of a clocking construct is the finest time precision of the simulation, so a change of time precision in one file changes the point at which a testbench samples (h1, S1), which is why STND.SV.3 records the time precision.

A construct that states the intent of a procedure, `always_comb`, `always_latch`, or `always_ff` at the editions that provide them, lets a tool report at compilation a latch or a flip-flop that the author did not intend; the committee record gives as intent that `always_comb` infers neither a latch nor a flip-flop, that `always_ff` infers at least one flip-flop, and that tools may check more, and the exact checks that the language definition requires are unverified (h1, S20 and S9) (STND.SV.9). A sensitivity list written by hand simulates differently from the logic that synthesis builds when it misses a variable, and the wildcard form `@*`, which an early revision added, makes a procedure sensitive to every variable it reads (h1, S6). A selection statement without a default, coded for an AND function, kept its previous output in simulation for an input with an unknown bit, while the netlist gave the correct low value, and the synthesis tools studied gave no warning; whether current tools warn is unverified (h1, S15) (STND.SV.10). A pragma comment of the form `full_case` or `parallel_case` makes synthesis assume what simulation never checks, and the qualifiers `unique` and `priority` state the same intent with a check in simulation; used without that check they carry "the same pitfalls as the synthesis full_case pragma" (h1, S6 and S19), which is why STND.SV.13 excludes such a directive and STND.SV.11 fails a test on each reported violation of a qualifier. In `casex` an unknown or high-impedance bit of the selection expression matches every item; in one worked example a stored don't-care value made simulation of the description select one item every time while simulation of the netlist selected the default in 98 percent of cycles (h1, S15) (STND.SV.12). In `casez` an unknown bit of the expression is no wildcard, but overlapping items change the result with their order (h1, S15 and S9). A delay, a forced value, and a test for an unknown value have no counterpart in the logic that synthesis builds; one simulator that compiles the description documents that it ignores timing checks and reads each delay given as minimum, typical, and maximum values as its typical value (h1, S9), and that synthesis ignores delays is general knowledge that the note marks unverified (STND.SV.13). The revision that added signed declarations and the arithmetic shift also changed how values wider than 32 bits are extended, a published test found a synthesis tool that expanded a signed one-bit literal wrongly in a negation, and a later revision changed the result of the relational and equality operators from an integer to a single bit, so the width of an expression depends on the edition in force (h1, S6, S11, and S3) (STND.SV.14). A declaration initializer or an initial procedure gives a state element a value in simulation whether or not the target gives it that value at power-on, which depends on the target (h1, S9 and S1); HDES.12 holds the obligation, and STND.SV.15 keeps such a value from counting as its evidence, the gap G2 of the note.

An unknown value is a don't-care to synthesis, an unknown to simulation, a wildcard in two forms of selection, and, to a check of equivalence, either a free choice or a value that matches only itself; "The most worrying thing is that there are different semantics!" (h1, S15). A condition that takes the false branch on an unknown value, and a selection that keeps its previous value when no item matches, are optimistic: they hide a defect that a simulation of the netlist or the device shows. Reconvergent logic that turns a known result into an unknown at gate level is pessimistic: it shows a difference that the hardware does not have (h1, S16). Randomized initial values are "a good solution for addressing X-pessimism issues, but not for detecting correct initialization and X-optimism issues" (h1, S16), and one simulator that is mostly two-state turns an assigned unknown into a constant chosen by an option (h1, S9), which is why STND.SV.17 counts neither as its check and STND.SV.3 records which kind of simulation each verdict comes from. A check of equivalence that lets each unknown value match either value reported the latch example above equivalent to the likely netlist; the author of that study recommends the mode that matches an unknown value only with an unknown value, and the analysis of each failure that passes only in the other mode, and names the two modes "2-state consistency" and "2-state equality", names that differ between tools (h1, S15) (STND.SV.18). An equivalence in a mode that resolves an unknown value otherwise than the simulation did does not interpret the description as the verification did, so the record of the mode is what lets HDES.9 decide whether that evidence counts. The three sentences of STND.SV.18 are one procedure, the record of the mode, the run in the strict mode, and the analysis of its failures, and apply together.

An invariant assertion on two clocks evaluated as values change in one time slot fires falsely when one clock rises before the other falls in that slot; the remedy of the language samples at the start of the time slot and evaluates after the design has settled (h1, S2 and S1), which a concurrent assertion does and an immediate assertion does not (STND.SV.19). "It is a requirement, that code executed by assertions must not be allowed to change the state of the design" (h1, S2). A proof tries every sequence of inputs that its constraints admit, and a constraint written wrong admits too few, so a proof that holds under an over-constrained environment shows nothing outside it (h1, S16) (STND.SV.20); HDES.6 already leaves a bounded proof inconclusive. Code coverage "can give both optimistic results (claims a branch is covered when it's unreachable) and pessimistic results" (h1, S15), which is the gap G1: HDES.6 asks for a named measure and not for what it counts on an unknown value (STND.SV.21). Coverage defined from the classes that generate stimulus measures the stimulus and not the design, a practice that the note derives from S3 (h1, H6) (STND.SV.22). The research note retrieved no primary text on vacuous passes of assertions, so the standard holds no provision on them; HDES.6 leaves each inconclusive verdict uncovered.

The language gives each process and object of a testbench its own random generator, seeded hierarchically from one seed, so that an unrelated edit does not disturb another stream; in one study three simulators initialized static processes and objects differently, "none of these implementations follow the standard exactly", and the language definition does not specify the generator (h1, S8). A seed therefore reproduces stimulus on one simulator at one structure of the testbench (STND.SV.23), and a comparison between simulators on one seed is meaningless (STND.SV.26). STND.CODE.9 and STND.VVUQ.64 already ask for the seed in the record of each test; STND.SV.23 adds the derivation of every stream from that seed and the record of a change that alters the stream.

A structural analysis "cannot determine if a real issue exists and does not include any sequential analysis" (h1, S16), and one tool sorts its warnings into those of lint alone, those of style, and those that affect simulation (h1, S9). The table of STND.SV.24 states the classes of finding that a run of static checks covers for these languages, from the hazards of the note, and not a tool or its options; which linter runs is configuration. STND.CODE.4 already has each finding resolved or suppressed at its location with its reason. The warnings of synthesis are warnings of a transformation step under HDES.9, among them an inferred latch, a truncation of width, and a signal with more than one driver. Tools lag the language: users kept to the syntax of the first revision because support for the second "had been so inconsistent", and tools accept in constant expressions functions that the definition forbids (h1, S3); STND.SV.2 records the constructs that a tool does not support or reads differently.

Tools have defects. A random-program tester, run for 18,000 CPU hours on five synthesis tools, found seven programs synthesized wrong and three crashes, with sign handling and width among the causes, and a defect in a simulator used to check; a later tester reported 15 defects in five months, nine confirmed as new (h1, S11 and S12). A defect that synthesis and the check of equivalence share, by reading the description the same way, is hidden from that check (h1, S11). STND.SV.25 adds a second route to the check of HDES.8 when it is a check of equivalence: a simulation of the netlist that reads the description through a simulator rather than through the reading that synthesis and the check share. A difference that comes from pessimism on the netlist is a finding of its own kind, which S16 classifies apart and removes by initializing the state that holds real unknowns (h1, S16). STND.SV.26 decides the properties that a realization relies on by a second simulator or by proof before that reliance, because one simulator's verdict carries its defects; counts of defects in simulators beyond S11 rest on slides and a summary and are unverified (h1, S24). A second simulator that is two-state, or that lacks a construct of the design, decides only the properties that rest neither on four-state values nor on that construct, which STND.SV.3 and STND.SV.2 record. A second tool that costs money is an expenditure under PRIME.8, and a project with no second simulator available is left a recorded decision under REPRO.7.

The research note retrieved no primary text on the coding of state machines, on interfaces and packages, on the checking of parameters and the semantics of generate constructs, on the styles of reset, or on vacuity, and the standard holds no provision on them. HDES.12 and HDES.15 govern the initial state and the mitigation of faults of a state machine, HDES.11 the release of a reset, and HDES.6 and HDES.12 the verification of reset.

Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, DSGN, SIMPL, QA, or a provision of HDES, and applies from CSQ3, the onset of HDES; work of CSQ4 may omit it. Each provision that adds language content to a provision of HDES takes the onset of that provision, so that a citation moves no rule to another class. STND.SV.5 to STND.SV.8 and STND.SV.19 instantiate DSGN.15 and state what a protocol of scheduling uses, not how its invariants are verified, so they apply from CSQ3. Some provisions apply at CSQ3 content of obligations that STND.CLASS.10 first asks at CSQ2: a contract for each external component and for hardware (DSGN.5), in STND.SV.2 and STND.SV.10, and documentation of the limits of validity (INTPR.10), in STND.SV.2, STND.SV.3, STND.SV.18, STND.SV.20, and STND.SV.21. Each such provision tightens above the floor (PRIME.15), as the same content does in HDES, because its check runs without a person and the failure it prevents is silent at every class. STND.SV.25 and STND.SV.26 rest on the row of STND.CLASS.10 for QA.9, a regeneration by another system before reliance, and apply from CSQ1. No provision binds, and no provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.DEPS | Dependency policy |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Language and records

#### STND.SV.1 Edition in force stated

Default. Instantiates REPRO.2, SIMPL.6.

The repository configuration SHOULD state the edition in force of each source file of a design and of its verification set (REPRO.2, SIMPL.6). Where a tool that reads such a file offers a setting that selects a revision of the language definition, the repository configuration SHOULD run that tool on the file under the setting for its edition in force (REPRO.2, SIMPL.6).

#### STND.SV.2 Construct subset stated

Default. Instantiates REPRO.2, DSGN.5, INTPR.10, HDES.3.

The design record under HDES.3 SHOULD state the construct subset of each design (REPRO.2, DSGN.5). For each tool on whose output a verdict of HDES.6 or a check of HDES.8 relies, the design record SHOULD state each construct of the design or of its verification set that the documentation of that tool states as unsupported, or as read differently from the language definition (DSGN.5, INTPR.10).

#### STND.SV.3 Simulation settings stated

Default. Instantiates REPRO.2, INTPR.10, HDES.6.

The record of each verification under HDES.6 SHOULD state, for each simulator that it uses, whether that simulator runs four-state or two-state simulation, and, for two-state simulation, the value that it gives a bit assigned the unknown or the high-impedance value (REPRO.2, INTPR.10). That record SHOULD state the time precision of each simulation, and each setting of a simulator that changes how it evaluates unknown values (REPRO.2).

#### STND.SV.4 Verification constructs kept apart

Default. Instantiates SIMPL.6, DSGN.3.

The repository configuration SHOULD list the synthesized set of each design (SIMPL.6). Classes, randomization, data types whose size changes during simulation, program blocks, and hierarchical references SHOULD appear only in the verification set (SIMPL.6, DSGN.3).

### Scheduling

#### STND.SV.5 Assignment kind by process

Default. Instantiates DSGN.15.

Each variable that a clocked process writes and that another simulation process reads SHOULD be written by nonblocking assignment (DSGN.15). Each variable that a combinational process writes SHOULD be written by blocking assignment (DSGN.15). A variable SHOULD NOT be written by both blocking and nonblocking assignment (DSGN.15).

#### STND.SV.6 One writing process per variable

Default. Instantiates DSGN.15, DSGN.14.

Each variable of the synthesized set SHOULD be written by one simulation process alone (DSGN.15, DSGN.14).

#### STND.SV.7 Order from scheduling regions

Default. Instantiates DSGN.15.

Each order between simulation processes on which a design or its verification set relies SHOULD come from the kinds of assignment and the scheduling regions that the language definition gives, and not from a delay (DSGN.15). A testbench SHOULD drive the inputs of a design, and sample its outputs, through a facility that the language definition at its edition in force orders against the evaluation of the design, a nonblocking assignment, a clocking construct, or the scheduling regions reserved for testbench code among them (DSGN.15).

#### STND.SV.8 Start-up after time zero

Default. Instantiates DSGN.15, REPRO.3.

The values and verdicts of a simulation SHOULD NOT depend on the order in which the simulator starts procedures, continuous assignments, and declaration initializers at time zero (DSGN.15, REPRO.3). The first transition of each clock and each reset that a testbench drives, to which a simulation process of the design is sensitive, SHOULD occur after time zero (DSGN.15).

### Simulation and synthesis

#### STND.SV.9 Process intent declared

Default. Instantiates SIMPL.6, DSGN.3.

Where the edition in force provides constructs that state that a procedure describes combinational logic, a latch, or clocked storage, each procedure of the synthesized set SHOULD use the construct that states what it describes (SIMPL.6, DSGN.3). Where a combinational procedure of the synthesized set uses no such construct, it SHOULD be made sensitive to each variable that it reads by the form of the language that includes them all (SIMPL.6, DSGN.3).

#### STND.SV.10 Storage only by decision

Default. Instantiates SIMPL.6, VV.1, DSGN.5.

In each combinational procedure of the synthesized set, each variable that the procedure writes SHOULD be assigned on every path through it, by an assignment before its selection statements or by an assignment in each branch (SIMPL.6, VV.1). Each latch that the synthesized set describes SHOULD be stated in the design record, with the procedure that describes it (SIMPL.6, DSGN.5).

#### STND.SV.11 Selection qualifiers checked

Default. Instantiates SIMPL.6, VV.1.

Where the items of a selection statement are meant to be mutually exclusive, or to be tested in order of priority, the statement SHOULD state that by the qualifier of the language definition that simulation checks (SIMPL.6, VV.1). Each violation of such a qualifier that a simulation under HDES.6 reports SHOULD fail the test that ran it (VV.1).

#### STND.SV.12 Wildcard selection limited

Default. Instantiates VV.1, SIMPL.6.

The synthesized set SHOULD hold no selection statement that matches an unknown value of its selection expression as a wildcard (VV.1). Where the items of a selection statement of the synthesized set hold wildcard bits and overlap, the statement SHOULD state their priority by the qualifier of STND.SV.11 (SIMPL.6).

#### STND.SV.13 Constructs read alike

Default. Instantiates VV.1.

Each behavior that the contract of a design under HDES.4 states SHOULD rest only on constructs of the synthesized set that simulation and the transformation steps of its realization read alike, a delay, a forced value, and a test for an unknown value not being among them (VV.1). The synthesized set SHOULD hold no delay in a procedure, and no synthesis directive that changes the logic that a transformation step produces from a selection statement (VV.1).

#### STND.SV.14 Explicit width and sign

Default. Instantiates SIMPL.6, HDES.7.

Where an assignment or an operation of the synthesized set extends, truncates, or changes the sign of a value, the source SHOULD state that extension, truncation, or change explicitly (SIMPL.6, HDES.7).

#### STND.SV.15 Initial values as evidence

Default. Instantiates VV.1, HDES.12.

Where the design record does not state that the target gives a state element at power-on the value that a declaration initializer or an initial procedure of the synthesized set gives it in simulation, the verification of HDES.12 SHOULD NOT rely on that value (VV.1, HDES.12). The verification of HDES.12 SHOULD NOT count a value that a simulator gives a state element at the start of a simulation as a value that the design sets (VV.1, HDES.12).

### Unknown values

#### STND.SV.16 Intended unknown values

Default. Instantiates SIMPL.6, VV.1.

Each assignment of an unknown value in the synthesized set SHOULD be stated, at its location or in the design record, as the assignment of a value on which the design does not rely (SIMPL.6). The verification of HDES.6 SHOULD show, for each such assignment, that it is unreachable, or that the value it assigns reaches no output or state element on which a behavior of the contract relies (VV.1).

#### STND.SV.17 Masked unknown values detected

Default. Instantiates VV.1, HDES.6.

The verification of HDES.6 SHOULD include a check, by proof or by simulation under a setting that evaluates both values of an unknown control, that reports each condition and selection of the synthesized set whose simulation turns an unknown value of its control into a known result (VV.1, HDES.6). A simulation from randomized initial values, or under two-state simulation, SHOULD NOT be counted as that check (VV.1).

#### STND.SV.18 Equivalence mode stated

Default. Instantiates VV.5, INTPR.10, VV.1, HDES.8.

The record of each check of equivalence under HDES.8 SHOULD state its equivalence mode (VV.5, INTPR.10). Where the tool of such a check provides a mode that matches an unknown value only with an unknown value, the check SHOULD run in that mode (VV.1, HDES.8). Where such a check fails in that mode, each output and state element on which it fails SHOULD be resolved, or shown by a simulation of the netlist or by a proof to behave as the verification of HDES.6 shows the hardware description to behave (VV.1, HDES.8).

### Assertions and coverage

#### STND.SV.19 Sampled assertions

Default. Instantiates DSGN.15, VV.1.

Where a property of the contract of a design relates values that change at a clock event, the assertion that decides it in simulation SHOULD be a concurrent assertion on that clock (DSGN.15, VV.1). The action of an assertion SHOULD NOT write a variable of the design (VV.1).

#### STND.SV.20 Assertion and assumption records

Default. Instantiates VV.5, INTPR.10, HDES.6, VV.1.

The record of the verification of HDES.6 SHOULD state, for each assertion that decides a verdict, its clock or that it has none, the condition that disables it, and whether it decides that verdict in simulation, in proof, or in both (VV.5, INTPR.10, HDES.6). Each assumption on the inputs of a design under which a proof of HDES.6 holds SHOULD be stated in the record of that proof, with the limit or property of the contract under HDES.4 that admits it (VV.1, INTPR.10).

#### STND.SV.21 Coverage counting stated

Default. Instantiates VV.5, INTPR.10, HDES.6.

Each coverage figure that the record of HDES.6 states SHOULD state whether its measure counts a branch taken on an unknown value of its condition, and whether it counts items that no reachable state of the design reaches (VV.5, INTPR.10, HDES.6). Each item that a coverage figure excludes SHOULD be listed in that record with its reason (VV.5, INTPR.10).

#### STND.SV.22 Functional coverage from the contract

Default. Instantiates VV.1, HDES.6.

Each item of functional coverage that the record of HDES.6 counts SHOULD be defined from a property or a limit of the contract under HDES.4, apart from the code that generates stimulus (VV.1, HDES.6).

### Random stimulus

#### STND.SV.23 Seeded random stimulus

Default. Instantiates REPRO.1, REPRO.3, VV.3.

Each process and object of a testbench that draws random values SHOULD take its seed from the seed that the record of the run states, by the seeding that the language definition gives it or by a seed that the testbench derives from that one (REPRO.1, REPRO.3). Where a change alters the stimulus that a recorded seed generates in a fixed-seed test of STND.VVUQ.64, the record of that change SHOULD state it (REPRO.3, VV.3).

### Checks and second routes

#### STND.SV.24 Static check classes

Default. Instantiates DSGN.3.

The static checks that the repository configuration names for each hardware description and its verification set SHOULD report each finding of each class of the table of this provision (DSGN.3).

| Class | Findings |
| --- | --- |
| Scheduling | A variable of the synthesized set that more than one simulation process writes; a variable written by both blocking and nonblocking assignment; a blocking assignment, in a clocked process, to a variable that another simulation process reads; a delay in a procedure of the synthesized set; a variable that a combinational procedure reads before it writes it |
| Inferred storage | A latch or a flip-flop inferred from a procedure whose construct states combinational logic; a latch that the design record does not state; a combinational procedure whose sensitivity is listed by hand |
| Selection | A variable that a combinational procedure does not assign on every path; a selection statement that matches an unknown value of its expression as a wildcard; overlapping items of a selection statement without a stated priority; a synthesis directive |
| Width and sign | An extension, truncation, or change of sign that an assignment or an operation makes without stating it |
| Construct sets | A construct of STND.SV.4 in the synthesized set; a construct outside the construct subset or the edition in force of its file |

#### STND.SV.25 Netlist simulated after equivalence

Default. Instantiates VV.1, QA.9.

Where the check of HDES.8 for a realization is a check of equivalence, a simulation of the netlist that it checks SHOULD also run a set of the tests of HDES.6 that the design record states, and give each of them the verdict that the test gives on the hardware description (VV.1, QA.9).

#### STND.SV.26 Second simulator or proof

Default. Instantiates VV.1, QA.9, REPRO.3.

Before a realization of a design is first relied upon or submitted for fabrication, each property of its contract that the verification of HDES.6 decides by simulation alone SHOULD also be decided, with the same verdict, by a simulator other than the one that decided it or by proof (VV.1, QA.9). A comparison of the results of two simulators SHOULD NOT rely on their drawing the same random values from the same seed (REPRO.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
