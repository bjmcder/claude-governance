"""Tests of the governance harness, laid out like the package.

Run from the repository root::

    python -B -m unittest discover -s tests -t .

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
# at exit, so that tests neither read nor fill the account's own cache
# (unit 0011); the tests of the cache name their own directories.
_SOLVE_CACHE = tempfile.mkdtemp(prefix="govharness-test-cache-")
os.environ["GOVHARNESS_CACHE_DIR"] = _SOLVE_CACHE
atexit.register(shutil.rmtree, _SOLVE_CACHE, True)
