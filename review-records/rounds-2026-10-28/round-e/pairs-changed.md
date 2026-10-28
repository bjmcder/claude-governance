# Round e of 2026-10-28: pairs whose changed side is a provision of this round

The kept copy is `/tmp/claude-1000/round-e/kept/governance`: the live corpus with rounds a, d, c, o, and e applied through `apply_rounds_2026_10_28.py`. The provisions that this round adds or changes are STND.HARN.24, STND.HARN.28, AGENT.45, AGENT.46, STND.DOCS.8, STND.DRAFT.10, STND.DRAFT.33, STND.WPROC.13, STND.WPROC.16, STND.IDENT.13, HDES.ASIC.12, STND.PROJ.1, STND.PROJ.2, STND.PERF.1, STND.FTN.4, STND.FTN.33, STND.DEPS.4, STND.DEPS.13, STND.DEPS.14, STND.CODE.5, STND.JL.3, STND.RUST.1, and STND.RUST.28, with GOV.11, GOV.24, GUARD.4, and GUARD.15 in LVL0. Two listings are given: under STND.HARN.28 as this round drafts it, which unit 0024 implements, and under the rule in force, with the code of `HEAD`. The withdrawn provisions (STND.CXX.18, STND.STDC.39, STND.STDC.40, STND.LEAN.27, STND.SV.28, STND.PY.14) have no pair, and a change of the Notes alone pairs nothing.

## Under the drafted rule

`python3 -B -m govharness pairs <kept>/governance STND.HARN.24 --with <the other 22 provisions> --amends GOV.11 GOV.24 GUARD.4 GUARD.15`: 56 pairs. No pair conflicts, and no pair addresses a matter that no shared-matters table gives.

| # | Changed side | Other provision | Bases | Verdict |
| --- | --- | --- | --- | --- |
| 1 | AGENT.46 | STND.DRAFT.42 | PRIME.14 | none: the referral that remains is the one STND.DRAFT.42 admits, halting only the line of work that it concerns |
| 2 | HDES.ASIC.12 | AGENT.12 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 3 | HDES.ASIC.12 | AGENT.41 | INTPR.10 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 4 | HDES.ASIC.12 | CPS.4 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 5 | HDES.ASIC.12 | HDES.11 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 6 | HDES.ASIC.12 | HDES.13 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 7 | HDES.ASIC.12 | HDES.3 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 8 | HDES.ASIC.12 | HDES.4 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 9 | HDES.ASIC.12 | HDES.5 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 10 | HDES.ASIC.12 | HDES.6 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 11 | HDES.ASIC.12 | HDES.7 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 12 | HDES.ASIC.12 | HDES.8 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 13 | HDES.ASIC.12 | HDES.FPGA.3 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 14 | HDES.ASIC.12 | HDES.FPGA.4 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 15 | HDES.ASIC.12 | HW.ASIC.3 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 16 | HDES.ASIC.12 | HW.ASIC.4 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 17 | HDES.ASIC.12 | HW.FPGA.3 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 18 | HDES.ASIC.12 | HW.FPGA.4 | matter: design record of a realized design | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 19 | HDES.ASIC.12 | STND.CODE.19 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 20 | HDES.ASIC.12 | STND.CODE.29 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 21 | HDES.ASIC.12 | STND.CODE.34 | INTPR.10, VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 22 | HDES.ASIC.12 | STND.CODE.9 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 23 | HDES.ASIC.12 | STND.DEPS.12 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 24 | HDES.ASIC.12 | STND.DEPS.13 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 25 | HDES.ASIC.12 | STND.DEPS.8 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 26 | HDES.ASIC.12 | STND.FTN.28 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 27 | HDES.ASIC.12 | STND.PERF.11 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 28 | HDES.ASIC.12 | STND.PERF.13 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 29 | HDES.ASIC.12 | STND.PERF.16 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 30 | HDES.ASIC.12 | STND.PERF.22 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 31 | HDES.ASIC.12 | STND.PERF.7 | INTPR.10 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 32 | HDES.ASIC.12 | STND.RUST.33 | INTPR.10, VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 33 | HDES.ASIC.12 | STND.RUST.8 | VV.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 34 | HDES.ASIC.12 | STND.WPROC.15 | REPRO.1 | none: the change adds a conjunction; the fabrication readiness record lists what the partner records, and no partner forbids an item of its list |
| 35 | STND.CREW.13 | AGENT.10 | GUARD.14 | none: the editorial GUARD.15 keeps the referral, and the estimates of AGENT.6 to AGENT.10 are what STND.CREW.13 bounds |
| 36 | STND.CREW.13 | AGENT.6 | GUARD.14 | none: the editorial GUARD.15 keeps the referral, and the estimates of AGENT.6 to AGENT.10 are what STND.CREW.13 bounds |
| 37 | STND.CREW.13 | AGENT.7 | GUARD.14 | none: the editorial GUARD.15 keeps the referral, and the estimates of AGENT.6 to AGENT.10 are what STND.CREW.13 bounds |
| 38 | STND.CREW.13 | AGENT.8 | GUARD.14 | none: the editorial GUARD.15 keeps the referral, and the estimates of AGENT.6 to AGENT.10 are what STND.CREW.13 bounds |
| 39 | STND.CREW.13 | AGENT.9 | GUARD.14 | none: the editorial GUARD.15 keeps the referral, and the estimates of AGENT.6 to AGENT.10 are what STND.CREW.13 bounds |
| 40 | STND.CREW.21 | AGENT.10 | GUARD.14 | none: as for STND.CREW.13 |
| 41 | STND.CREW.21 | AGENT.6 | GUARD.14 | none: as for STND.CREW.13 |
| 42 | STND.CREW.21 | AGENT.7 | GUARD.14 | none: as for STND.CREW.13 |
| 43 | STND.CREW.21 | AGENT.8 | GUARD.14 | none: as for STND.CREW.13 |
| 44 | STND.CREW.21 | AGENT.9 | GUARD.14 | none: as for STND.CREW.13 |
| 45 | STND.DEPS.4 | AGENT.22 | REPRO.7 | none: a grouped reason is a decision record that AGENT.22 does not restrict |
| 46 | STND.DOCS.8 | AGENT.25 | INTPR.12 | none: AGENT.25 asks records when made; spelling does not bear on it |
| 47 | STND.DRAFT.10 | AGENT.25 | INTPR.12 | none: the provision now reaches governance and project instruments, which the records of AGENT.25 are not |
| 48 | STND.DRAFT.33 | AGENT.25 | INTPR.12 | none: the rule is unchanged |
| 49 | STND.DRAFT.42 | AGENT.15 | GUARD.3 | none: AGENT.15 continues the lines of work that a referral does not concern, as STND.DRAFT.42 has it |
| 50 | STND.FTN.33 | AGENT.22 | REPRO.7 | none: a grouped entry is a decision record that AGENT.22 does not restrict |
| 51 | STND.VVUQ.83 | AGENT.3 | PRIME.2 | none: the editorial GUARD.15 changes nothing that STND.VVUQ.83 or the AGENT provisions on claims, checks, and departures rely on |
| 52 | STND.VVUQ.83 | AGENT.4 | PRIME.2 | none: the editorial GUARD.15 changes nothing that STND.VVUQ.83 or the AGENT provisions on claims, checks, and departures rely on |
| 53 | STND.VVUQ.83 | AGENT.47 | PRIME.2 | none: the editorial GUARD.15 changes nothing that STND.VVUQ.83 or the AGENT provisions on claims, checks, and departures rely on |
| 54 | STND.VVUQ.83 | AGENT.5 | PRIME.2 | none: the editorial GUARD.15 changes nothing that STND.VVUQ.83 or the AGENT provisions on claims, checks, and departures rely on |
| 55 | STND.WPROC.16 | AGENT.28 | QA.2 | none: AGENT.28 consults knowledge, and AGENT.39 assesses parallel units; a commit that changes only a shared record is consistent with both |
| 56 | STND.WPROC.16 | AGENT.39 | DSGN.15 | none: AGENT.28 consults knowledge, and AGENT.39 assesses parallel units; a commit that changes only a shared record is consistent with both |

## Under the rule in force

The code of `HEAD` (the rule in force), `pairs <kept>/governance ID` for each of the 27 documents of the round and `pairs <kept>/governance LVL0 --amends GOV.11 GOV.24 GUARD.4 GUARD.15`, keeping the pairs that hold a provision that this round adds or changes: 344 pairs, each counted once. Grouped by changed provision; the verdict of a group applies to each pair in it. No pair conflicts.

### AGENT.45 (7 pairs)

Verdict: none: the dropped sentence restated PRIME.14, which every partner already applies; the prohibition that remains is unchanged.

STND.DFLT.17 (PRIME.10), STND.DFLT.30 (PRIME.10), STND.DFLT.31 (PRIME.10), STND.KNOW.11 (PRIME.10), STND.THRT.3 (PRIME.10), STND.THRT.4 (PRIME.10), STND.THRT.7 (PRIME.10).

### AGENT.46 (7 pairs)

Verdict: none: the dropped sentence restated GUARD.8; the count and the referral that remain are unchanged, and STND.DRAFT.42 and the provisions of STND.CREW and STND.DFLT on referral and reach agree with them.

STND.CREW.14 (PRIME.14), STND.CREW.2 (PRIME.14), STND.DFLT.20 (PRIME.14), STND.DFLT.25 (PRIME.14), STND.DFLT.30 (PRIME.14), STND.DFLT.35 (PRIME.14), STND.DRAFT.42 (PRIME.14).

### HDES.ASIC.12 (254 pairs)

Verdict: none: the change places a conjunction before the last item of a list and changes no meaning; each partner was paired with the same text before.

AGENT.12 (VV.1), AGENT.41 (INTPR.10), CPS.4 (VV.1; matter: design record of a realized design), CPS.6 (VV.1), CPS.7 (REPRO.4), CPS.8 (VV.1), HDES.10 (INTPR.10; VV.1), HDES.11 (VV.1; matter: design record of a realized design), HDES.12 (VV.1), HDES.13 (matter: design record of a realized design), HDES.15 (VV.1), HDES.3 (REPRO.1; matter: design record of a realized design), HDES.4 (matter: design record of a realized design), HDES.5 (INTPR.10; matter: design record of a realized design), HDES.6 (INTPR.10; VV.1; VV.5; matter: design record of a realized design), HDES.7 (VV.1; matter: design record of a realized design), HDES.8 (INTPR.10; VV.1; VV.5; matter: design record of a realized design), HDES.9 (INTPR.10; VV.1), HDES.FPGA.3 (VV.1; matter: design record of a realized design), HDES.FPGA.4 (REPRO.1; REPRO.4; matter: design record of a realized design), HDES.FPGA.5 (VV.1), HW.10 (INTPR.10; VV.1), HW.15 (VV.1), HW.16 (VV.1), HW.17 (INTPR.10; VV.1), HW.18 (INTPR.10), HW.20 (VV.1), HW.3 (REPRO.1), HW.6 (VV.1), HW.7 (INTPR.10), HW.ASIC.3 (REPRO.1; matter: design record of a realized design), HW.ASIC.4 (INTPR.10; VV.1; matter: design record of a realized design), HW.CPU.3 (INTPR.10), HW.EMBED.3 (VV.1), HW.EMBED.4 (VV.1), HW.EMBED.5 (REPRO.1), HW.EMBED.6 (INTPR.10), HW.FPGA.3 (REPRO.1; matter: design record of a realized design), HW.FPGA.4 (INTPR.10; VV.1; matter: design record of a realized design), HW.QPU.3 (REPRO.1), HW.QPU.4 (VV.5), HW.QPU.5 (INTPR.10; VV.1; VV.5), HW.QPU.6 (VV.1), HW.QPU.7 (INTPR.10; VV.1), HW.QPU.8 (INTPR.10; VV.5), MEAS.3 (REPRO.4), MEAS.4 (REPRO.1; REPRO.4), MEAS.5 (INTPR.10), MEAS.6 (INTPR.10), ML.3 (REPRO.1), ML.4 (VV.1; VV.5), ML.5 (INTPR.10; VV.1), ML.6 (INTPR.10), NUMER.11 (VV.1), NUMER.12 (INTPR.10; VV.1), NUMER.13 (VV.1; VV.5), NUMER.14 (VV.1), NUMER.16 (INTPR.10), NUMER.17 (VV.1), NUMER.18 (INTPR.10), NUMER.19 (VV.1), NUMER.20 (INTPR.10), NUMER.21 (VV.5), NUMER.22 (VV.1), NUMER.23 (VV.1), NUMER.24 (VV.1), NUMER.25 (VV.1), NUMER.28 (VV.1), NUMER.29 (VV.1), NUMER.5 (VV.1), NUMER.6 (VV.1), NUMER.7 (VV.1; VV.5), NUMER.8 (VV.1), NUMER.9 (VV.1), STND.ANNEX.10 (VV.1), STND.ANNEX.2 (VV.1), STND.ANNEX.4 (VV.1), STND.ANNEX.9 (VV.1), STND.BUILD.1 (REPRO.1), STND.BUILD.13 (INTPR.10; VV.1), STND.BUILD.14 (REPRO.1), STND.BUILD.2 (REPRO.1), STND.BUILD.20 (REPRO.1), STND.BUILD.23 (REPRO.1), STND.BUILD.25 (REPRO.1; REPRO.4), STND.BUILD.26 (INTPR.10), STND.BUILD.4 (REPRO.1), STND.BUILD.6 (REPRO.1), STND.BUILD.7 (REPRO.1), STND.CLASS.10 (INTPR.10; REPRO.4; VV.1), STND.CLASS.21 (REPRO.4), STND.CLASS.22 (REPRO.1), STND.CLASS.23 (REPRO.1; REPRO.4; VV.1), STND.CODE.19 (VV.1), STND.CODE.29 (REPRO.1), STND.CODE.34 (INTPR.10; VV.1), STND.CODE.9 (REPRO.1), STND.CONC.24 (VV.1), STND.CONC.26 (VV.1), STND.CONC.27 (INTPR.10; VV.1), STND.CONC.28 (VV.1), STND.CXX.13 (VV.1), STND.DEPS.12 (REPRO.1), STND.DEPS.13 (REPRO.1), STND.DEPS.8 (REPRO.1), STND.FTN.28 (VV.1), STND.LEAN.1 (REPRO.1), STND.LEAN.10 (VV.1), STND.LEAN.13 (VV.1), STND.LEAN.14 (VV.1), STND.LEAN.15 (VV.1), STND.LEAN.16 (VV.1), STND.LEAN.17 (INTPR.10; VV.1), STND.LEAN.18 (VV.1), STND.LEAN.19 (VV.1), STND.LEAN.20 (INTPR.10; VV.1), STND.LEAN.21 (REPRO.1; VV.1), STND.LEAN.22 (VV.1), STND.LEAN.23 (INTPR.10; VV.1), STND.LEAN.4 (INTPR.10; VV.1; VV.5), STND.LEAN.6 (VV.1), STND.LEAN.7 (VV.1), STND.LEAN.8 (VV.1), STND.OFFLD.12 (VV.1), STND.OFFLD.26 (VV.1), STND.OFFLD.27 (VV.1), STND.OFFLD.28 (VV.1), STND.OFFLD.29 (VV.1), STND.OFFLD.3 (VV.1), STND.OMP.16 (VV.1), STND.OMP.2 (VV.1), STND.OMP.23 (VV.1), STND.OMP.31 (VV.1), STND.OMP.33 (VV.1), STND.OMP.4 (VV.1), STND.PERF.11 (VV.1), STND.PERF.13 (VV.1), STND.PERF.16 (VV.1), STND.PERF.22 (REPRO.1), STND.PERF.7 (INTPR.10), STND.RUST.33 (INTPR.10; VV.1), STND.RUST.8 (VV.1), STND.STDC.16 (VV.1), STND.STDC.26 (VV.1), STND.STDC.38 (INTPR.10; VV.1), STND.SV.10 (VV.1), STND.SV.11 (VV.1), STND.SV.12 (VV.1), STND.SV.13 (VV.1), STND.SV.15 (VV.1), STND.SV.16 (VV.1), STND.SV.17 (VV.1), STND.SV.18 (INTPR.10; VV.1; VV.5), STND.SV.19 (VV.1), STND.SV.2 (INTPR.10), STND.SV.20 (INTPR.10; VV.1; VV.5), STND.SV.21 (INTPR.10; VV.5), STND.SV.22 (VV.1), STND.SV.23 (REPRO.1), STND.SV.24 (INTPR.10), STND.SV.25 (VV.1), STND.SV.26 (VV.1), STND.TEST.11 (REPRO.1), STND.TEST.12 (VV.1; VV.5), STND.TEST.15 (INTPR.10; VV.1), STND.TEST.16 (REPRO.1), STND.TEST.17 (VV.1), STND.TEST.19 (VV.1), STND.TEST.8 (REPRO.1), STND.TEST.9 (REPRO.1; VV.5), STND.VVUQ.1 (VV.1), STND.VVUQ.10 (VV.1; VV.5), STND.VVUQ.11 (VV.1; VV.5), STND.VVUQ.12 (VV.1; VV.5), STND.VVUQ.13 (VV.1), STND.VVUQ.15 (VV.1), STND.VVUQ.16 (INTPR.10; VV.1; VV.5), STND.VVUQ.17 (VV.1), STND.VVUQ.18 (VV.1), STND.VVUQ.19 (VV.1), STND.VVUQ.2 (VV.1), STND.VVUQ.20 (VV.1; VV.5), STND.VVUQ.21 (VV.1; VV.5), STND.VVUQ.22 (VV.1; VV.5), STND.VVUQ.23 (VV.1; VV.5), STND.VVUQ.24 (VV.1; VV.5), STND.VVUQ.25 (VV.1), STND.VVUQ.26 (VV.1), STND.VVUQ.27 (VV.1), STND.VVUQ.28 (VV.1; VV.5), STND.VVUQ.29 (VV.1), STND.VVUQ.3 (VV.1), STND.VVUQ.31 (VV.1), STND.VVUQ.32 (VV.1), STND.VVUQ.33 (VV.1), STND.VVUQ.34 (VV.1), STND.VVUQ.35 (VV.1), STND.VVUQ.36 (INTPR.10; VV.1), STND.VVUQ.37 (INTPR.10; VV.1), STND.VVUQ.38 (VV.1), STND.VVUQ.39 (VV.1; VV.5), STND.VVUQ.4 (VV.1), STND.VVUQ.40 (VV.1; VV.5), STND.VVUQ.41 (VV.1; VV.5), STND.VVUQ.42 (VV.1; VV.5), STND.VVUQ.43 (VV.1; VV.5), STND.VVUQ.44 (VV.1; VV.5), STND.VVUQ.45 (VV.1; VV.5), STND.VVUQ.46 (VV.1; VV.5), STND.VVUQ.47 (INTPR.10; VV.1; VV.5), STND.VVUQ.48 (INTPR.10; VV.1; VV.5), STND.VVUQ.5 (VV.1), STND.VVUQ.50 (INTPR.10; VV.1), STND.VVUQ.51 (VV.1), STND.VVUQ.52 (VV.1), STND.VVUQ.53 (VV.1), STND.VVUQ.54 (INTPR.10), STND.VVUQ.55 (VV.5), STND.VVUQ.56 (VV.5), STND.VVUQ.57 (VV.1), STND.VVUQ.58 (VV.1), STND.VVUQ.59 (VV.1), STND.VVUQ.6 (VV.1; VV.5), STND.VVUQ.60 (VV.1), STND.VVUQ.61 (VV.1), STND.VVUQ.62 (VV.1), STND.VVUQ.63 (VV.1), STND.VVUQ.64 (VV.1), STND.VVUQ.65 (VV.1), STND.VVUQ.67 (VV.1), STND.VVUQ.68 (VV.1), STND.VVUQ.69 (VV.1), STND.VVUQ.7 (VV.1; VV.5), STND.VVUQ.70 (VV.1), STND.VVUQ.71 (VV.1), STND.VVUQ.72 (VV.1), STND.VVUQ.73 (VV.1), STND.VVUQ.74 (VV.1), STND.VVUQ.76 (VV.1; VV.5), STND.VVUQ.77 (VV.1), STND.VVUQ.79 (VV.1), STND.VVUQ.8 (VV.1), STND.VVUQ.80 (VV.1), STND.VVUQ.81 (VV.1), STND.VVUQ.9 (VV.1; VV.5), STND.WFLOW.24 (REPRO.1; REPRO.4), STND.WFLOW.35 (REPRO.4), STND.WFLOW.36 (REPRO.1), STND.WFLOW.37 (VV.1), STND.WFLOW.38 (VV.1), STND.WFLOW.39 (VV.1), STND.WFLOW.40 (VV.1), STND.WFLOW.6 (REPRO.1), STND.WPROC.15 (REPRO.1).

### STND.CODE.5 (1 pairs)

Verdict: none: NUMER.4 fixes names and notation, not layout; the provision now asks a layout tool only where the means include one.

NUMER.4 (INTPR.1).

### STND.DEPS.13 (9 pairs)

Verdict: none: each partner records the identity of what built or ran a result; the exception added for the checks of STND.DEPS.14 concerns checks, not the builds of results.

HDES.3 (REPRO.1), HDES.FPGA.4 (REPRO.1), HW.3 (REPRO.1), HW.ASIC.3 (REPRO.1), HW.EMBED.5 (REPRO.1), HW.FPGA.3 (REPRO.1), HW.QPU.3 (REPRO.1), MEAS.4 (REPRO.1), ML.3 (REPRO.1).

### STND.DEPS.14 (6 pairs)

Verdict: none: the partners keep evidence current for the hardware, the model, or the hazard analysis, or verify a description; checking the work at the edges of a declared range of its language and dependencies neither requires nor forbids what they ask.

CPS.3 (VV.8), HDES.6 (VV.8), HW.7 (VV.8), HW.CPU.3 (VV.8), HW.EMBED.5 (VV.8), ML.7 (VV.8).

### STND.DEPS.4 (6 pairs)

Verdict: none: one reason for a group of dependencies is a decision record that AGENT.22, HDES.3, ML.3, and the NUMER records of REPRO.7 neither forbid nor duplicate.

AGENT.22 (REPRO.7), HDES.3 (REPRO.9), ML.3 (REPRO.9), NUMER.16 (REPRO.7), NUMER.3 (REPRO.7), NUMER.5 (REPRO.7).

### STND.DOCS.8 (2 pairs)

Verdict: none: the table moved without a change of its rows; AGENT.25 asks records written when made, and NUMER.4 fixes a notation that the exceptions of the first sentence already admit.

AGENT.25 (INTPR.12), NUMER.4 (INTPR.1).

### STND.DRAFT.10 (1 pairs)

Verdict: none: the provision now reaches governance and project instruments, not the records of AGENT.25.

AGENT.25 (INTPR.12).

### STND.DRAFT.33 (1 pairs)

Verdict: none: the rule is unchanged and cites the table that STND.DOCS.8 now holds.

AGENT.25 (INTPR.12).

### STND.FTN.33 (4 pairs)

Verdict: none: an entry for a set of files that share forms and reasons is a decision record of the same content; AGENT.22 and the NUMER records ask nothing of its granularity.

AGENT.22 (REPRO.7), NUMER.16 (REPRO.7), NUMER.3 (REPRO.7), NUMER.5 (REPRO.7).

### STND.JL.3 (8 pairs)

Verdict: none: the checks of each change at the reference version and the prerelease check at an interval neither require nor forbid what the partners ask of contracts, models, hazard analyses, or descriptions.

CPS.3 (VV.8), HDES.3 (REPRO.9), HDES.6 (VV.8), HW.7 (VV.8), HW.CPU.3 (VV.8), HW.EMBED.5 (VV.8), ML.3 (REPRO.9), ML.7 (VV.8).

### STND.PERF.1 (8 pairs)

Verdict: none: an evaluation of a claim under HW.22 adds the repetition, dispersion, and uncertainty that HW.22 does not state, and asks nothing that HW.19, HW.21, the records of HW.CPU, HW.GPU, and HW.QPU, or NUMER.17 forbid.

HW.19 (RSRC.2), HW.21 (RSRC.2), HW.22 (RSRC.4), HW.CPU.4 (RSRC.2; RSRC.4), HW.CPU.5 (RSRC.2), HW.GPU.4 (RSRC.2; RSRC.4), HW.QPU.8 (RSRC.4), NUMER.17 (RSRC.4).

### STND.RUST.1 (8 pairs)

Verdict: none: as for STND.JL.3; the metadata and the checks of each change at the release that builds results are Rust content.

CPS.3 (VV.8), HDES.3 (REPRO.9), HDES.6 (VV.8), HW.7 (VV.8), HW.CPU.3 (VV.8), HW.EMBED.5 (VV.8), ML.3 (REPRO.9), ML.7 (VV.8).

### STND.RUST.28 (2 pairs)

Verdict: none: HDES.3 and ML.3 record what built a result; the review of the build script of an added dependency is a review of the work's inputs that neither forbids.

HDES.3 (REPRO.9), ML.3 (REPRO.9).

### STND.WPROC.16 (4 pairs)

Verdict: none: a commit that changes only a shared record is the protocol for those records; AGENT.39 assesses parallel units, AGENT.28 consults knowledge, and HDES.11 and HW.11 concern clock domains and memory models, other subjects on a common LVL0 provision.

AGENT.28 (QA.2), AGENT.39 (DSGN.15), HDES.11 (DSGN.15), HW.11 (DSGN.15).

### Provisions that instantiate an amended LVL0 provision (16 pairs)

Verdict: none: the amendment of GOV.11, GOV.24, GUARD.4, and GUARD.15 is editorial; these provisions instantiate one of them and keep their meaning, and each pair rests on a common LVL0 provision outside the amended ones.

AGENT.10 with STND.CREW.13 (GUARD.14), AGENT.10 with STND.CREW.21 (GUARD.14), AGENT.15 with STND.DRAFT.42 (GUARD.3), AGENT.3 with STND.VVUQ.83 (PRIME.2), AGENT.4 with STND.VVUQ.83 (PRIME.2), AGENT.47 with STND.VVUQ.83 (PRIME.2), AGENT.5 with STND.VVUQ.83 (PRIME.2), AGENT.6 with STND.CREW.13 (GUARD.14), AGENT.6 with STND.CREW.21 (GUARD.14), AGENT.7 with STND.CREW.13 (GUARD.14), AGENT.7 with STND.CREW.21 (GUARD.14), AGENT.8 with STND.CREW.13 (GUARD.14), AGENT.8 with STND.CREW.21 (GUARD.14), AGENT.9 with STND.CREW.13 (GUARD.14), AGENT.9 with STND.CREW.21 (GUARD.14), NUMER.26 with STND.VVUQ.83 (PRIME.2).
