# Review 0006: read-only retrieval and STND.HARN 0.6

Independent review (QA.7). Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `dcbf150`: unit 0005 (`govharness/query/`, `govharness/cli/query.py`, `tests/query/`, README "Fetching governance") and STND.HARN 0.6 as `drafts/harn-0.1-tools/build_harn.py` generates it |
| Reviewer | Claude (independent review agent); not the author of the change |
| Directive | "The point of the code harness is to facilitate read-only transactions that fetch the relevant parts and cross references of the governance without having to search or load excess data into context. It is not to impede development." |
| Method | Ten agent questions run against the live corpus (deleting files, pushing to a remote, installing a dependency, before a commit, halting and referring, drafting a provision, the class of the work, signatures, a Lexicon term, `LVL0#normative-language`); every stem group of the corpus vocabulary listed and read; the architecture test probed with a write and an upward import in `query` (both caught) |

## Findings

Severity: Medium means a query returns excess or misses governance that applies, or a provision contradicts another or the floor. Low means an inexact, stale, or untested statement.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | `show LVL0#normative-language` printed all of LVL0 (12 KB, with the Preamble and revision history), and `show` of any document printed its whole body. `find` and `context` scored a document as one text, so its length outranked provisions: "drafting provision" returned ten documents and no provision | Documents are split into sections. A locator shows its section (5.8 KB for Normative Language). A document shows its lead text and names its sections by locator and its items (LVL0: 0.5 KB; STND.HARN: 1.9 KB). Sections are searched one by one |
| 2 | Medium | Cited by was padded by document text that is not a cross reference. LVL0's revision history made LVL0 cite 24 items, STND.DFLT's history made it cite GOV.41, and the Mechanisms table and the Checks section named the documents' own items. A reader was sent to a 5 to 10 KB document | Citations from a document's text are recorded per section. A revision history and a References table are not listed as citing, nor is a document's mention of its own items. Cited by names the section (`STND.DFLT#mechanisms-and-their-provisions`), not the document. References tables are not counted: they are derived from the citations (STND.DRAFT.34) |
| 3 | Medium | The stemmer matched every word that began with the query's stem. False positives: "sign" found signal and significant, "work" workflow and workspace, "refer" reference, "commit" commitment, "act" actuation, "use" user. False negatives: "dependency" missed dependencies, "referring" missed refer and refers. Hyphenated words were one token, so "read only" missed "read-only" | Both sides are stemmed and compared equal. "ies"/"ied" become "y", and a final doubled consonant is made single, so committed and commit, and installed and install, meet. Hyphenated words split; identifiers stay whole |
| 4 | Medium | `find push remote` printed nothing and exited 1, although remote write is governed. One absent word emptied the result | Where no item holds every word, `find` returns those that hold the most, under a note. An empty result says so on stderr. `context` uses the same search, so `every` is removed |
| 5 | Low | Raw counts ranked long texts first. "consequence class" and "class work" put long sections ahead of GOV.12 | Text hits count up to 3 per word, and the shorter text breaks ties. Title words now include the parts of the identifier and the provision's section, so the STND.DRAFT provisions match "drafting" |
| 6 | Low | Lineage ignored `parent`, so HW.ASIC showed no profile. A locator in `instantiates` became the whole of LVL0 (STND.DRAFT.1, "Implements: LVL0"). "Implements" misnamed a term's `governed_by`. The `cites` field was read, but `parent` was not | "Governed by" follows `instantiates`, `governed_by`, and `parent`, and keeps the locator `LVL0#normative-language`. LVL0's `cites` are not followed upward. Checked for LVL0 (GUARD.6: none), LVL1 (HW.ASIC: HW), LVL2 (STND.INSTR.4: GOV.48, GUARD.6), and LEX (LEX.bulk-action: GUARD.6) |
| 7 | Low | A planned or draft item's heading printed its status twice. Lists sorted as text (GOV.13 before GOV.6). `NAMED_CAP` hid names behind a count, and the docstring of `citations` claimed text order for a sorted list | Status is printed once. Lists sort by number. The cap is removed: names come from at most eight matches and their citations (at most 14 in the sampled questions, at a budget of 1 500 characters). Docstrings are corrected |
| 8 | Medium | STND.HARN 0.6 gave number 28, freed by Replacement acceptance, to Item retrieval. `governance/README.md` still said "STND.HARN.28 states when a replacement is relied on" | Renumbered with retrieval first (below). The README line now names the queries |
| 9 | Medium | STND.HARN.31 "Read-only queries" restated GOV.36, under which a change outside the ledger is a defect. Read literally, it also forbade any file a harness writes, such as a cache. That is a design choice with no floor reason, and it impedes development | Removed. Its place is taken by Whole text (GOV.39): a text is returned in full or named only, never cut. That is the property a reader relies on (GOV.39: "before relying on a provision, an actor reads its full text") |
| 10 | Medium | STND.HARN.28 used "implements", which is not defined, and named no locator. Its "each item ... that cites it" would require revision-history rows. STND.HARN.30 prescribed the method ("and of the items those cite") and "name the rest", which a cap breaks | Item retrieval names what the fields and the returned text cite, and every provision, term, knowledge entry, and tag that cites the item; a harness may name more. Topic retrieval states the outcome (within the reader's size, best matches first) and leaves the method open |
| 11 | Medium | STND.HARN.21 was made conditional ("Where a harness derives…"). STND.HARN.25 (Unattended referral) and STND.HARN.29 (Configuration failure) still made a harness derive a configuration whatever the case. That contradicts the condition and the Purpose: no work depends on a harness | Both now bind "a configuration that a harness derives" (now STND.HARN.28 and STND.HARN.29) |
| 12 | Low | The Purpose did not say that queries and checks are read-only. Retrieval, the purpose, came last (28 to 31), and Configuration failure (29) sat inside Rehearsal's range | Purpose rewritten (below). Renumbered: Retrieval 1 to 3, Corpus 4 to 6, Ledger 7 to 12, Signatures 13 to 18, Generated content 19 to 20, Checks 21 to 23, Environment 24 to 29, Rehearsal 30 to 31. `RANKS` follows, and l.3 confirms it. The code, tests, README.md, and governance/README.md are updated. Decision 0002 gets an appended adjustment. Earlier reviews, units, and drafts keep the numbers of the revisions they record (PRIME.5) |
| 13 | Low | The README command table had no `show`, `find`, or `context`, and "Not yet built" still said "There is no query engine". README.md and pointer.md gave STND.HARN as revision 0.5 with 29 provisions, and pointer.md omitted the `query` layer. The README cited STND.HARN.31 for "read-only" | Updated. The README states that the search matches words, not meanings |
| 14 | Low | The tests did not cover locators, documents, cited-by exclusions, lineage by level, or the fallback. One test passed only through the prefix match ("delete" against "delegated") | 11 tests, each naming its behavior and reference (VV.7): locators, documents, cited-by exclusions, lineage at each level, stems both ways, the fallback, the budget, and whole texts |

## STND.HARN 0.6 as revised

Purpose: "A harness serves governance read-only. Its queries return an item or section with its cross references, or the governance on a topic, so that a reader loads only what applies; its checks report whether the corpus and the ledgers conform. It holds no authority, and no work depends on it: governance applies whether or not a harness runs, and without one an actor reads the corpus and performs each check by hand (GOV.38, INTPR.12). Separately, a harness regenerates content, appends transactions to ledgers, and can derive the configuration of an agent's environment (GOV.48). This standard fixes the queries, the form of the corpus and the ledgers (GOV.35, GOV.36), the checks, the signatures, and the generated content (GOV.37, GOV.39), and the derivation of an environment. Every provision is binding, because each instantiates a floor obligation (GOV.10)."

New retrieval provisions:

- **1 Item retrieval:** given an identifier or a locator, a harness returns the item or section, with the identifier and title of each item its fields or the returned text cite, and of each provision, term, knowledge entry, and tag that cites it (GOV.38).
- **2 Topic retrieval:** given words and a size, it returns, within that size, items and sections that hold the words, best matches first (GOV.38).
- **3 Whole text:** it returns a provision, term, knowledge entry, tag, or section in full, or by its identifier or locator alone (GOV.39).

## Considered, no change

- **Options.** `--expand` fetches an item and the text it relies on in one call. `--in-force` leaves out drafts. `--limit` and `--budget` set the size. Each has a present use. No index file and no new dependency. A query takes about 0.3 s.
- **Questions in full sentences.** There are no stop words or synonyms (SIMPL.3). "what applies before a commit" matches common words, and "before commit" finds STND.DFLT.7. The README says to give keywords. "push" finds nothing because the corpus says "remote write". `find` says so and returns the closest items.
- **STND.HARN.21 Stable check keys** (formerly 18) is kept. Provisions name check keys in `checked_by`, so a silent rename or reuse would change what a provision cites (GOV.37), and renames are rare.
- **STND.HARN.30 Rehearsal before application** is kept. It binds only a script that changes a corpus, and its checks may be done by hand.
- **Architecture.** `query` is layer 2 and imports only `core`. The effects scan forbids it to read or write, and a probe with a `write_text` call and an import of `cli` failed four architecture tests.
- `governance-README.md` at the root is the baseline copy, which this unit does not touch.

## Results

| Check | Result |
| --- | --- |
| unit tests | 123 tests, OK |
| `ruff check --select E,F,W,I,UP --line-length 79 govharness tests tools` | clean |
| `check governance --no-z3` | exit 0; no FAIL or WARN; punch list unchanged (87 lines, no STND.HARN finding) |
| `verify governance` | all PASS; ledger 41 entries |
| `manifests --check`, `references --check`, `compose --check` | stale: 0; PASS |

Sample sizes: `find governance delete files` is 39 bytes (STND.INSTR.3). `show governance PRIME.14` is 1.8 KB, with 3 citations and 17 citing items. `context governance remote write --budget 3000` is 3.4 KB: six whole texts and twelve named.

## Verdict

Accepted with the fixes for the custodian's decision. The queries now return the governance that applies, with its cross references, and no whole long document. STND.HARN 0.6 states that queries and checks are read-only and that no work depends on a harness. No provision makes a harness derive a configuration, and the draft is consistent with GOV.35 to GOV.39, STND.DRAFT, and STND.IDENT under the logic checks.
