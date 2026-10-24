"""Governance harness: checks, derived files, and workflows for a corpus.

The corpus under ``governance/`` is the system of record. This package
only checks it, derives files from it, and records transactions in its
ledger (GOV.38). The layers, lowest first, are ``core``, ``ledger``,
``checks`` and ``derive``, ``workflows``, and ``cli``; a module imports
only from its own layer or a lower one (decision 0001, DSGN.7).
"""
