# Revision brief for the language standards, draft 0.2 (from the lead agent)

## What changed under you

STND.DOCS is now draft 0.3. Its reading copy is `/home/claude/scratch/docs-0.3-draft.md`. It is applied by `/home/claude/pkg/apply8.py`, which also amends STND.INSTR to 1.4. The new provision STND.INSTR.10 has an agent meet each binding provision of an adopted LVL2 standard whose subject is an agent. Rehearse from a fresh copy of the live corpus: `import apply8; apply8.apply(root)` (ledger entries 100 and 101), then apply yours.

The DOCS numbers changed. Update every citation:

| DOCS | Subject |
|---|---|
| 1 | Voice |
| 2 | Explanatory content: terms, examples, reasons, assumptions, limits |
| 3 | Agents kept out |
| 4 | Edit narration kept out |
| 5 | Process records kept out |
| 6 | Governance as subject |
| 7 | Required statements of agent use |
| 8 | American English |
| 9 | Specific statements and the patterns table |
| 10 | Agent writing (binding, GOV.48) |
| 11 | Documentation in step with the work |
| 12 | One name per concept |
| 13 | Checked examples: stated tolerance; the shown result is not replaced by the failing output |
| 14 | Documentation in change review |

## Your task

Read both review files in your scratch directory, `review-cold.md` and `review-pairs.md`. Apply every defect and should-fix finding, and the optional ones where cheap. Write `dispositions-0.1.md` beside them, one row per finding with its disposition. Where you decline a finding, give the reason.

## Decisions common to the three standards

Apply these the same way in each.

1. **Agent-only binding rules (GOV.48).**
   - Where the custodian said "always" and meeting the rule costs only the agent's wording or code form, not a tool or added work, add one binding provision whose subject is an agent. It instantiates GOV.48 plus the Article it serves, on the model of STND.DOCS.10. STND.INSTR.10 delivers it.
   - Example for PY: an agent annotates each parameter and return value of each function it writes or changes.
   - Running a checker or a tool stays a default from CSQ3, because it needs a provisioned tool. Never bind a tool run at CSQ4.
2. **Binding provisions that instantiate PRIME.4** must stay within PRIME.4's list: invalid input, a violated precondition, non-convergence, resource exhaustion, and the silent-continuation forms. Scope any broader rule as a default.
3. **Random numbers (PY, JL):**
   - Functions that draw take a generator object explicitly.
   - Only an entry point (an application main, a test, a script) constructs it from a recorded seed.
   - Global or task-default state is never seeded or drawn from in library code.
   - Streams for parallel parts derive from the root seed by the library's spawning or jump facility, never by seed arithmetic or by hashing. This follows STND.VVUQ.62; read it at `governance/STND/VVUQ/62.md`.
   - Independence evidence comes from NUMER.24.
   - Exact-value references and doctests use a generator whose stream is stable across versions, or show output that does not depend on the draws.
4. **Tolerances (PY, JL):**
   - A comparison within a tolerance states its parameters at the tier of STND.VVUQ.1, with STND.VVUQ.5 for the relative and absolute parts, and its NaN policy (STND.VVUQ.3).
   - Exact comparison is allowed for exact values.
   - Tolerances are named constants with their basis (STND.CODE.10, NUMER.11).
   - Cite STND.VVUQ by ID only where it exists in the corpus.
5. **Doctests:** shown floating-point output is rounded, or compared with a stated tolerance (STND.DOCS.13).
6. **Anomalies (PY; JL where relevant):** a condition that PRIME.4 lists is never reported only through a logger. It is raised, warned, or returned. The logger carries diagnostics.
7. **Notation:** names fixed by the documented notation of NUMER.4 are exempt from case rules (STND.DOCS.12). Say how the linter's naming rules are configured for this.
8. **Version rules:**
   - The rule names its trigger, keeps the STND.DEPS.3 clause "consistent with the rest of the computational environment", and exempts a revision that a hardware contract or qualification fixes.
   - A change of language version is a change of runtime under HW.7 and STND.DEPS.5.
   - Each run records the exact language and library revisions (STND.DEPS.8).
9. **Notes:**
   - Remove every sentence that leaves a choice to the custodian or describes the drafting. State the rule with its reason. Put the decisions only in your final message.
   - State each departure from the custodian's direction, or from the named source (manual, Core Guidelines, PEPs), with its reason.
   - Mark facts that the research did not verify as unverified, or leave them out.
   - Obligations in the Notes are not normative. Move each one into a provision or drop it.
10. **Class onset:** name each provision whose instantiated part STND.CLASS.10 starts at another class (CSQ2, CSQ1, CSQ0), and state that it tightens above the floor (PRIME.15), as HW.EMBED does.
11. **Style:**
    - Section headings must not be "X and Y" by reflex.
    - No "offers", "serves as", or "ensures" tails.
    - Write "may omit", not "omits".
    - Your own text meets STND.DOCS.9.

## Deliverable

Your final message, under 600 words:

- the paths of the revised files;
- the verify result and the remaining findings;
- the count of findings applied and declined;
- the decisions for the custodian, numbered, each with your recommendation;
- open unverified facts.
