# Review B, round of 2026-10-27: STND.PY 1.2, STND.RUST 1.2, STND.JL 1.3

## Verified by running

- Rehearsal: entries 188 to 197, every check PASS, only the existing g.18 warning, source unchanged. `verify` on an applied scratch copy: PASS.
- `show` on the eight changed provisions and STND.CODE.22 to .26, STND.DEPS.12: one modal per sentence, no banned body word (regex), titles of six words or fewer, body identifiers match citations. The References tables list STND.CODE and STND.DEPS.
- No citation of a withdrawn identifier remains outside revision rows and the field `withdrawn`. "Foreign function interface" appears nowhere in the corpus after the round. Foreign interface is defined once (STND.CODE) and Lock file once (STND.DEPS) as table rows.
- `pairs` for STND.PY, STND.RUST, STND.JL on the scratch copy: the changed-side counts equal `pairs-changed.md` (PY.35 24, RUST.24 5, RUST.25 24, RUST.30 10, JL.39 24). The other sides are hardware, design, and record provisions; they address contracts or records, not the language rule. HW.13 and HW.14 (layout at a hardware boundary) complement STND.RUST.24. No conflict.
- Modal counts of RUST.1, .7, .11, .22, .24, .25, .30 (Defect 1).

## Defect

1. **Stale onset claim in STND.RUST, Class onset.** Text at fault: "STND.RUST.1, STND.RUST.7, STND.RUST.11, STND.RUST.22, STND.RUST.24, STND.RUST.25, and STND.RUST.30 each hold three modals on one subject: the releases of one crate, what one argument rests on, one destructor and its release, one future, one type at one boundary, one function that a foreign interface invokes, and one file;". After the round STND.RUST.24 holds two modals, and STND.RUST.25 and STND.RUST.30 hold one each (counted), so the sentence is false for three of seven. The rationale's "Class onsets: unchanged" is untrue of it. Replacement: "STND.RUST.1, STND.RUST.7, STND.RUST.11, and STND.RUST.22 each hold three modals on one subject: the releases of one crate, what one argument rests on, one destructor and its release, and one future;". Add to the rationale: "the class onset paragraph drops STND.RUST.24, STND.RUST.25, and STND.RUST.30 from the provisions of three modals".

2. **The rationale of STND.RUST 1.2 says an outcome is kept that is narrowed.** Text: "Rust code keeps each outcome of the removed sentences through STND.CODE.22, STND.CODE.24, and STND.CODE.25, in the same terms". The earlier STND.RUST.25 let a function "be declared with an ABI under which both sides of the interface admit unwinding" in place of the catch, with no statement in a contract. Now a panic may leave only where the contract states that the interface carries it on (STND.CODE.24, first sentence, which STND.RUST.25 cites), so an unwinding ABI without that statement no longer complies. This tightens Rust; `draft-status.md` item 4 cites STND.RUST.25 as precedent for a relaxation. Replacement, after "in the same terms,": "except that an ABI that admits unwinding no longer takes the place of the catch unless the contract of the interface states that the interface carries a panic on to code of the work (a narrowing of the first sentence of the earlier STND.RUST.25),". See the question below.

## Should-fix

1. **Retitles are not recorded.** The revision rows and rationales of all three standards omit that STND.PY.35 ("Python exceptions in foreign callbacks" to "Python interrupts in foreign callbacks"), STND.JL.39 (likewise "Julia interrupts in foreign callbacks"), STND.RUST.27 ("Ownership across foreign interfaces" to "Foreign resources released in Drop"), and STND.RUST.30 ("Committed lock files" to "Builds from locked revisions") change title. Add to each row, for example in STND.PY: "STND.PY.35 is retitled Python interrupts in foreign callbacks;".

2. **Widening of STND.RUST.27 not stated.** "Each type of the work that owns a resource under STND.CODE.25 SHOULD release it in its `Drop` implementation" reaches each resource the work owns under STND.CODE.25, where the earlier text reached only one "that a foreign function interface creates for the work". Append to the rationale: "; the release in `Drop` now reaches each resource that the work owns under STND.CODE.25".

3. **Python declared types, narrowed.** The earlier STND.PY.34 required the Python source to "declare the type of each argument and of the result" of a foreign function. STND.CODE.22 asks only that each type have "the size, the alignment, and the representation that the contract of the interface fixes". A library default that happens to match now complies. The rationale says "the declared types ... through STND.CODE.22". Replacement: "the types through STND.CODE.22, which asks the representation that the contract fixes and no longer the declaration".

## Optional

1. `draft-status.md` says "130 pairs"; the table has 131 rows. Replacement: "lists the 131 pairs".
2. The Notes cite STND.CODE.22 to .26 correctly by sentence, and every sourced fact and "(unverified)" mark survives. The sentence "as a requirements file is that pins" in STND.PY Versions predates the round and is ungrammatical; the round could fix it: "as a requirements file does that pins".

## Kept outcomes

- Each kept provision keeps only language content, reads correctly beside its STND.CODE cite, and restates nothing.
- Onsets: STND.PY.35 and STND.JL.39 from CSQ2 (DSGN.5), STND.JL.38 and STND.RUST.27 from CSQ3, as before.
- The Terms entry "the manifest file of an environment is its lock file" fits Manifest.toml. STND.DEPS.12 leaves nothing that STND.PY.33 and STND.JL.4 asked.

## Question for the custodian

Does STND.RUST.25 narrow, as intended, so that a Rust function declared with an unwinding ABI complies only where the contract states that the interface carries a panic on (Defect 2)? If not, STND.CODE.24 needs a clause that admits an unwinding ABI in place of the catch.
