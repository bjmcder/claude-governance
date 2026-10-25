# From P2 to P1 (2026-10-25)

Nothing in STND.CODE 1.2 blocks P2. One non-blocking point, in STND.CXX 1.2:

1. **STND.CXX Notes, checking paragraph.** The new sentence says that STND.JL.34 and STND.RUST.20 ask for no library checks in the reporting configuration "because Julia and safe Rust check each index in every build unless code removes the check where it states why the check holds (STND.JL.18, STND.RUST.3)". For Julia this holds only per location: the option `--check-bounds=no` removes every bounds check of a session, dependencies included, with no reason stated anywhere. P2 adds STND.JL.36 (default, from CSQ1, as STND.CXX.27): the production configuration leaves bounds checking on outside `@inbounds`, unless a measurement and a decision record show its cost. Suggested fix: cite STND.JL.36 beside STND.JL.18 in that sentence, or limit the claim to safe Rust and to Julia under STND.JL.36.
