# Dependencies of the harness code (REPRO.9)

| Component | Revision | License | Reason carried | Required |
| --- | --- | --- | --- | --- |
| Python | 3.11 or later (3.13 at unit 0001) | PSF-2.0 | Language and standard library of every module and test | Yes |
| GnuPG (`gpg`, `gpg-agent`, `gpgconf`) | 2.4 (2.4.4 at unit 0001) | GPL-3.0-or-later | Signs ledger entries and verifies signatures (`ledger/gpg.py`); the signature tests and the equivalence harness generate throwaway keys and stop their agent with `gpgconf` | Only for signing, signature checks, and their tests |
| z3-solver | as installed (5.1.0 at unit 0001) | MIT | Faster proofs for checks f; the built-in DPLL solver gives the same verdicts | No |
| ruff | 0.16.8 | MIT | Lint for unit acceptance; not imported | Development only |

Review: each unit that changes a dependency reviews the pinned revision of every direct dependency (STND.DFLT.11).
