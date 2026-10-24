# Unit 0005: read-only retrieval of governance

## Deviation

The custodian redirected the work mid-turn ("the point of the code harness is to facilitate read-only transactions that fetch the relevant parts and cross references of the governance without having to search or load excess data into context"); the code was written against that statement, and this definition of done after it, contrary to STND.DFLT.7. Recorded and reported (STND.INSTR.7).

## Definition of done

1. `show ID` prints an item's text with the identifier and title of each item it implements (upward through `instantiates` and `governed_by`), each other item it cites, and each item that cites it; `--expand` adds the text of what it cites.
2. `find WORDS` lists the items that hold every word, by stem, ranked by words held, words in the title, and occurrences.
3. `context WORDS --budget N` prints in full the best matches and the items they cite, within N characters, names at most 12 more, and does not follow a document's citations.
4. All three load the corpus once, change no file, and sit in layer 2 (`govharness.query`) with the CLI in layer 4.
5. Tests, ruff, and `verify` pass.

## Record

- Done: `govharness/query/graph.py`, `govharness/query/retrieval.py`, `govharness/cli/query.py`; `tests/query/test_retrieval.py` (7 tests); architecture layer `query: 2`; README section "Fetching governance".
- Audit: 1 to 3 met by the tests; 4 met by `tests/test_architecture.py`; 5 met: 119 tests OK, ruff clean, verify PASS. A query answers in about 0.3 s on the current corpus.
