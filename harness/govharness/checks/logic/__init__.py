"""The logic checks (0, a to f): facts the corpus asserts about itself.

``facts``, ``tiers``, and ``wording`` extract facts from the provision
text and front matter; ``authority`` and ``language`` judge them
(checks 0 and a to e); ``proofs`` encodes them as clauses and proves
the structural claims (check f) with ``satlib``.
"""
