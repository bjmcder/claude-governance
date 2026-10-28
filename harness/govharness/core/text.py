"""Cut Markdown bodies into sentences, mentions, and identifiers.

Every check reads text the same way: table rows are data, quoted spans
are mentions rather than uses, and sentences end at terminal
punctuation, semicolons, and colons.
"""

from __future__ import annotations

import re

NUMERIC_ID_RE = re.compile(r"\b[A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*\.\d+\b")
SENTENCE_RE = re.compile(r"(?<=[.;:!?])\s+(?=[A-Z(\"“])")
QUOTE_RE = re.compile(r'"[^"\n]*"|“[^”\n]*”')
FENCE_RE = re.compile(r"```.*?```", re.S)
CODE_RE = re.compile(r"`[^`\n]*`")
TABLE_LINE_RE = re.compile(r"^\s*\|")
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")


def without_tables(text: str) -> str:
    """Drop Markdown table rows: a table is data, not a sentence.

    Parameters
    ----------
    text : str
        Markdown text.

    Returns
    -------
    str
        The lines that do not start with ``|``.
    """
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("|")
    )


def split_sentences(text: str) -> list[str]:
    """Split prose on terminal punctuation, semicolons, and colons.

    Parameters
    ----------
    text : str
        Prose.

    Returns
    -------
    list[str]
        Non-empty sentences, stripped.
    """
    return [p.strip() for p in SENTENCE_RE.split(text) if p.strip()]


def ids_in(text: str) -> list[str]:
    """Return the numbered identifiers mentioned in a text, in order.

    Parameters
    ----------
    text : str
        Any text.

    Returns
    -------
    list[str]
        Identifiers such as ``GOV.12``, repeats kept.
    """
    return NUMERIC_ID_RE.findall(text)


def prose_lines(body: str) -> list[str]:
    """Return the prose lines of a body.

    Fenced code, inline code, headings, and table lines are dropped, and
    list markers are removed.

    Parameters
    ----------
    body : str
        Markdown body.

    Returns
    -------
    list[str]
        One entry per non-empty prose line.
    """
    text = CODE_RE.sub(" ", FENCE_RE.sub("\n", body))
    lines = []
    for raw in text.splitlines():
        if TABLE_LINE_RE.match(raw) or raw.lstrip().startswith("#"):
            continue
        line = BULLET_RE.sub("", raw).strip()
        if line:
            lines.append(line)
    return lines


def unquoted(sentence: str) -> str:
    """Remove quoted spans: a quoted expression is mentioned, not used.

    Parameters
    ----------
    sentence : str
        Any text.

    Returns
    -------
    str
        The text with each quoted span replaced by one space.
    """
    return QUOTE_RE.sub(" ", sentence)


def snippet(text: str, start: int, end: int, margin: int = 30) -> str:
    """Return the text around a match, flattened to one line.

    Parameters
    ----------
    text : str
        Text that holds the match.
    start, end : int
        Span of the match.
    margin : int
        Characters kept on each side.

    Returns
    -------
    str
        The surrounding text with newlines replaced by spaces.
    """
    left, right = max(0, start - margin), min(len(text), end + margin)
    return text[left:right].replace("\n", " ").strip()


def normalise_term(term: str) -> str:
    """Lower-case a term, collapse spaces, and drop a plural ``s``.

    Parameters
    ----------
    term : str
        A Lexicon term or a defined name.

    Returns
    -------
    str
        The form used to compare terms.
    """
    term = re.sub(r"\s+", " ", term.strip().lower())
    return (
        term[:-1] if term.endswith("s") and not term.endswith("ss") else term
    )
