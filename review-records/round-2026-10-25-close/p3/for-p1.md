# From P3 to P1, through the lead (2026-10-25)

Not blocking. P3 0.5 withdraws two provisions that the STND.CODE Notes of P1 0.3 name; the rehearsal passes, since the harness does not check Notes, but the reconciliation review will flag the names.

1. **STND.RUST.14 (withdrawn, if the custodian takes P3 decision 4).** The Ignored results paragraph of STND.CODE says the reading "lowers the reach that STND.RUST.14 and the C reading of STND.STDC 1.0 gave the outcome ... and STND.RUST.14 keeps its own form". Suggested: "... lowers the reach that STND.RUST 1.0 and the C reading of STND.STDC 1.0 gave the outcome, which accepted any compiler or static check that diagnoses an ignored value; the must_use attribute is the form in Rust, and STND.RUST 1.1 holds no provision of its own on ignored results". If the custodian keeps RUST.14 instead (WITHDRAW_RUST14 = False in apply_rust_1_1.py), the present sentence stands.
2. **STND.FTN.18 (withdrawn).** The Required checks paragraph says "while STND.FTN.18 holds the outcome as a default for Fortran". Suggested: "while STND.CODE.21 holds it as a default for Fortran, as for every other language without a binding form".
