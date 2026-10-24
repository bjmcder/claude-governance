"""STND.CODE 1.1 (minor amendment): logical grouping of statements, made language-neutral
at the custodian's ruling of 2026-10-23 on the Python grouping direction."""
from content3 import P

DATE = "2026-10-23"

CODE13 = P(13, "Statements grouped by step", "Source", """
Within the body of a function, a procedure, or a process, statements SHOULD be grouped into blocks that each carry out one step of the computation, with one blank line between consecutive blocks (INTPR.1). Other than a blank line that a tool of STND.CODE.5 inserts, a block SHOULD carry no blank line inside it (INTPR.1). Where the step that a block carries out is not evident from its code, a comment at the head of the block SHOULD state it (INTPR.1).
""", ["INTPR.1"], refs=["STND.CODE.5"])

CODE_DOC_EDITS = [
    ("The language standards that the mnemonic register reserves for Python, C++, and Julia, once adopted, add the conventions of each language.",
     "The language standards of LVL2 add the conventions of each language."),
    ("Code disabled by turning it into a comment is neither active nor retired; the source history keeps it (STND.CODE.11, SIMPL.8).",
     "Code disabled by turning it into a comment is neither active nor retired; the source history keeps it (STND.CODE.11, SIMPL.8). "
     "The custodian directs that code be laid out by the logical grouping of its instructions, so that a reader follows a computation step by step: a blank line ends a step, and a comment names a step whose purpose its code does not show (STND.CODE.13, INTPR.1)."
    ),
]

CODE_ROW = ("| 1.1 | " + DATE + " | Minor amendment (GOV.41): new STND.CODE.13 groups the statements of each body into blocks, one step of the computation each, set apart by one blank line and headed by a comment where the step is not evident; the custodian's grouping direction, first given for Python, applies to every language. |")
