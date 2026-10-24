"""Tests of the governance harness, laid out like the package.

Run from the repository root::

    python -B -m unittest discover -s tests -t .

A mutation test damages an in-memory or temporary copy of the corpus in
one known way and asserts that the named check reports it: evidence of
detection against a known injected defect. A test that compares only
with earlier output is labeled a regression guard (VV.7).
"""
