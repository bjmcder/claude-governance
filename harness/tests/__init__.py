"""Tests of the governance harness, laid out like the package.

Run from ``harness/``, the directory that holds ``govharness/`` and
``tests/``::

    python3 -B -m unittest discover -s tests -t .

The fast subset, under 20 s, for an installer::

    python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main \\
        tests.test_architecture tests.test_conventions

A mutation test damages an in-memory or temporary copy of the corpus in
one known way and asserts that the named check reports it: evidence of
detection against a known injected defect. A test that compares only
with earlier output is labeled a regression guard (VV.7).
"""

import atexit
import os
import shutil
import tempfile

# The solve cache of every test run lies in a fresh directory, removed
# at exit, so that the tests that verify share solver results (unit
# 0011); without the variable there is no cache (unit 0022), and the
# tests of the cache name their own directories.
_SOLVE_CACHE = tempfile.mkdtemp(prefix="govharness-test-cache-")
os.environ["GOVHARNESS_CACHE"] = _SOLVE_CACHE
atexit.register(shutil.rmtree, _SOLVE_CACHE, True)
