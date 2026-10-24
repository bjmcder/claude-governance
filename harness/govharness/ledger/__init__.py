"""Layer 1: ledger transactions, the hash chain, and signatures.

``ledger/chain.py`` reads and appends ledger files; ``ledger/gpg.py``
runs ``gpg``, reads the signer configuration, and consults the
environment. ``register.py`` checks each registered key and
``signatures.py`` verifies signatures by calling ``ledger/gpg.py``;
``transactions.py`` is pure computation.
"""
