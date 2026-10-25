# QA.8 review, part C: `harness/govharness/checks/` with its tests

Reviewer C, main at 6391253 or later. Scope: `checks/` (all subpackages), `tests/checks/`, `tests/equivalence/`, `tests/test_architecture.py`, `tests/test_conventions.py`. Scratch: `/tmp/claude-1000/qa8-c/` (fuzzers `fuzz.py`, `fuzz2.py`, `cachefuzz.py`; corpus probes `p*.py`; the AST mutator `mutate.py`; logs `mut_*.log`). Nothing outside it and this report was written. Tests run: `tests/checks` (58, OK), `test_architecture` and `test_conventions` (12, OK). Not run: z3 (not installed), the full suite.

## Findings

### High

**H1. v.8 does not catch a withdrawn trailing provision** (`checks/revisions/family.py:122-132`; STND.IDENT.14).
The gap test is `range(1, max(numbers) + 1) - numbers - gone`. Deleting the highest-numbered provision leaves no gap, so an unlisted withdrawal passes, and the number can then be reused. Repro on an in-memory copy: delete `STND.PERF.26` and leave `withdrawn` alone. No check changes status, although `STND.PERF/_doc.md` still cites `STND.PERF.26` in its text. Deleting `STND.PERF.10` is caught.
Fix: also fail when an identifier with the document's prefix and a number above the maximum is cited anywhere in the corpus (a dangling citation, see L1), or have the document record its provision count.

**H2. g.21 does not see a contraction written with a typographic apostrophe** (`checks/drafting/style.py:17`; STND.DRAFT, "no contractions").
`CONTRACTION_RE` and the person-word lookarounds know only `'`. Repro: append ` The agent doesn’t act.` to `STND.DRAFT.2`. g.21 stays PASS; the straight-quote form fails. The live corpus holds no U+2019, so nothing is hidden today.
Fix: use `['’]` in both patterns.

### Medium

**M1. Content outside every ledger scope can change with only a manifest regeneration** (`checks/ledger.py:58-81`; GOV.36 and STND.HARN.9).
The pin test compares only the scopes that some transaction names. The scopes cover LVL0, the profiles, and STND/*, not `KNOW/`, `TAG/`, `_PROJECT/`, `STND/_doc.md`, `README.md`, or any new top-level directory. Repro on a copy of `governance/`: append a line to each of those, run `manifests --write`, run `verify`. Every case passes (the same edit to `STND/DRAFT/1.md` fails, as it should). The code follows STND.HARN.9 to the letter; the hole is in the specification as well as the check.
Fix: list every `.md` file under the root that no pinned scope covers as FAIL, or as WARN while the area is planned.

**M2. Table cells are never scanned by the drafting checks or by d.1** (`core/text.py:71` `prose_lines` through `drafting/context.py` `_unit`; `logic/wording.py:67`).
STND.DRAFT says the body of a provision "including a table it contains, is normative". Repro: append `| x | The code may not run |` as a table row to `STND.PERF.1` or `STND.DRAFT.1`. d.1 and g.5 stay quiet, while the same words in a sentence fail both. The README documents the skip for d only. I turned the cells of the 23 live provisions that hold prose tables (not the `defines` tables) into sentences and ran g.3, g.4, g.5, g.6, g.10 to g.14, g.21, and g.22: no finding, so there is no latent defect today. By the brief's wording this could be High; I rate it Medium because the standard's own expression tables hold unquoted mentions, so scanning needs a rule for them.
Fix: scan cells outside columns that list expressions, or require the quotation marks of STND.DRAFT.3 there.

**M3. The effect scan of `test_architecture.py` is a denylist** (`tests/test_architecture.py:80-89`, `effects()`).
The README says `checks/` "reads and writes no file", and the test comment says no module opens a network connection. I appended one use to `checks/manifests.py` in a copy and ran the test. Controls fail as they should: `open()`, `subprocess`, `os.listdir`, `Path.read_text`, `builtins.open`, `importlib`, `eval`, `gzip.open`. Passing: `smtplib`, `ftplib`, `sqlite3.connect`, `zipfile.ZipFile`, `fileinput.input`, `multiprocessing.Process`, `threading.Thread`, `logging.FileHandler`, `sys.stdin.read`, `sys.path.append`, `uuid.uuid4`, `f = path.read_text; f()`, and `getattr(path, "read_text")()`.
Fix: for `checks/`, allow a named list of imports and fail on any other.

**M4. v.5 fails a draft that has no adopter yet** (`checks/revisions/adopters.py:99-102`; STND.IDENT.12).
Repro: give `STND.PERF` status draft and revision 0.1, and drop `adopted_by` and `adopted`. Only v.5 fails, with "names no adopter". v.1 to v.4 treat drafts as valid. Workaround: name the intended adopter.
Fix: require the field when `status` is in `ADOPTED`.

**M5. Tests do not hold behavior that the README claims** ("a passing run means the checks can fail").
Mutations of `checks/` that survive the `tests/checks` modules (all of `tests/` for the first row):

| Mutation | Check left unheld |
| --- | --- |
| `structure.py:56` `!=` flipped; `:76-78` the mnemonic filter negated | ids, mnemonics (no test anywhere) |
| `authority.py:164`, `:258`, `:291`, `:330-331`, `:457`, `:485-496` | b.1, b.3 (uncovered parts), b.4 (superset), b.5, b.6, c.3, c.4 |
| `history.py:157` `<=` to `<` | v.3, duplicate revision row |
| `identifiers.py:176` upper bound; `:332-335`; `classes.py:278` | v.10 grade span, near siblings, v.3 major step |
| `modals.py:190`; `context.py:252`, `:418-424` | g.4 "imposes nothing" and status words |
| `expressions.py:140-142`, `:238`, `:248`; `roles.py:49` | g.9 fill-in label, g.12 two conditions, g.17 six-word bound |
| `ledger.py:106` verdict inverted | structural ledger verdict, within `tests/checks` |

I damaged the corpus for b.1, b.5, b.6, c.3, e.1, f.4, and d.1: each fails as it should today. The guards are missing; the code is not wrong. There is no test of f.2 to f.8 or of d.0 and d.3 to d.6.

### Low

- **L1. A dangling citation passes outside provision front matter.** STND.DRAFT.22 is `checked_by: l.1`, which reads only `instantiates` and `refers_to`. The body of `STND.PERF/_doc.md` can cite `GOV.999`; no check changes. In a default provision, g.16 only warns. Fix: a v-type check that every identifier in any body resolves.
- **L2. Nested scopes make a valid sequence fail.** Transaction `HW/CPU`, an edit, then transaction `HW`: ledger FAIL "content changed outside the ledger since seq N: HW/CPU". The reverse order fails too. This matches STND.HARN.9; workaround: one scope per directory.
- **L3. g.4 counts clauses joined by a semicolon as separate sentences.** `A SHALL act; B SHALL act.` passes; g.18 limits the total only.
- **L4. Mnemonic regex** `^[A-Z]{2,5}\d?$` (`structure.py:20`) admits a digit for any directory; STND.IDENT.17 says letters only.
- **L5. `checked_by` is validated only for STND.DRAFT (g.23) and STND.IDENT (v.7).** `AGENT.1` with `["zz.9"]` passes. All 1,043 lower provisions are clean today.
- **L6. `Verification.sections` decides pass or fail from detail lines.** A FAIL result with no details would count as a pass. Unreachable now.
- **L7. `test_conventions.py:63-67` skips positional-only parameters** (`posonlyargs`).
- **L8. The equivalence guard cannot run:** `archive/tools-flat` is absent, and it ends in a `FileNotFoundError` traceback. The README says so.
- **L9. STND.DRAFT's section "Checks" says "the provision concerned is binding"; the code and README mean the provision the check enforces.** A default provision with a g.3 defect fails, because DRAFT.2 is binding. Fix the wording, or the code.

## Checked and sound

**Solver (`satlib.py`, unit 0009).**
- Fuzzed against a brute-force reference: 3 seeds × 15,000 random sets of up to 6 variables and 14 clauses, with duplicate literals, tautologies, empty and unit clauses, plus 1,500 sets of up to 11 variables and 45 clauses. Zero differences in status.
- Models satisfy the clauses and equal an independent rescanning DPLL with the same split order.
- Cores equal a brute-force version of the stated minimisation rule.
- `confirms_core` accepts every honest core and rejected every random other subset (3 per unsatisfiable set).
- Mutation of `satlib.py` (145 sites) against `test_satlib` and `test_solvecache`: every DPLL and propagation line is killed. Survivors are the z3 branches, which cannot run here, and two boundary mutants (`satisfies` key order, `p < total`).

**Solve cache (`solvecache.py`, unit 0011).**
- No reused result went untrusted-checked. A SAT entry is reused only if its model satisfies every clause. An UNSAT entry is reused only if `confirms_core` passes; a z3 core is never reused. Key, format, and backend are compared.
- Fuzz: 6,000 clause sets × 15 forged entries (random bits, random sorted and unsorted position lists, right key and backend): 10,689 accepted, and every one equals the fresh solve in status, core, and positions. A stale entry cannot differ, because the digest covers the clause order, claim, backend, and the source of `satlib`, `solvecache`, and `hashing`.
- The incremental key of `proofs._keys_of` equals `solve_key`; the cached output is built from clause names, not stored text.
- Mutation of `solvecache.py` against `test_solvecache`: only `FORMAT = 1` to 2 survives (equivalent).

**Probes that fail as they should.** a.1 to a.3, b.2 to b.4, c.1 to c.3, c.5, e.1 to e.3, f.1, f.2/f.4 (via a.2, a.3), l.1 to l.5, v.1 to v.4, v.7, v.8 for a middle gap, g.1 to g.3, g.5, g.18, g.22, g.23, and g.25 (locator, `LEX.agent`, parenthesized and bare names). A quote left open or spanning sentences hides nothing, so quote handling fails closed.

**Other.**
- Registry keys are unique and what each check enforces resolves. The severity model matches the README's rule for g (self, lower, advisory groups).
- m.1 and m.2 follow STND.HARN.26 and STND.HARN.27; mutants of `combination.py` survive only in message formatting.
- g.25 matches the record of unit 0013; I did not repeat its review.
- Mutation of `lineage/` (90 sites), `revisions/` (about 270), `logic/authority.py`, `facts.py`, `tiers.py`, `language.py`, and `drafting/` `modals`, `expressions`, `roles`, `style`, `tables`, and (partly) `context`: survivors are as in M5 or equivalent.

## Could not check

- z3.
- The mutation runs of `logic/wording.py`, `logic/proofs.py`, `drafting/family.py`, and `drafting/citations.py` had not finished (the host was overloaded) and were stopped; their survivors, if any, are not listed. Unit 0013's review covers `citations.py`.
- The structural signature logic (`ledger/`, part B).
