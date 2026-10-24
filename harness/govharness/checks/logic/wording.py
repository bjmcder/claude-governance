"""Extract the facts about wording: barred expressions, normative words,
and the Lexicon.
"""

from __future__ import annotations

import re
from typing import Any

from govharness.core.corpus import Corpus
from govharness.core.locators import heading_slug
from govharness.core.text import (
    normalise_term,
    split_sentences,
    without_tables,
)

QUOTED_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
CAPITALIZED_RE = re.compile(r"\b(?:SHALL NOT|SHALL|SHOULD|NEVER|MAY)\b")


def extract_excluded(corpus: Corpus) -> dict[str, Any]:
    """Collect the expressions LVL0 itself bars.

    The drafting standard's own table is read by the drafting checks;
    ``advisory`` stays empty here.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, Any]
        ``strict`` maps phrases LVL0 itself bars to their source;
        ``advisory`` is empty.
    """
    strict: dict[str, str] = {}
    advisory: dict[str, str] = {}
    sources = [("LVL0", corpus.body("LVL0"), strict)]
    for source, text, bucket in sources:
        for sentence in split_sentences(text):
            if not re.search(r"\bexcluded\b|\bNEVER used\b", sentence):
                continue
            for quoted in QUOTED_RE.findall(sentence):
                if not quoted.isupper():
                    bucket.setdefault(quoted.strip().lower(), source)
    for phrase in strict:
        advisory.pop(phrase, None)
    return {"strict": strict, "advisory": advisory}


def _strip_quotes(text: str) -> str:
    """Remove quoted spans and table rows: both mention, not use.

    Parameters
    ----------
    text : str
        Markdown body.

    Returns
    -------
    str
        The text without table rows and with quoted spans blanked.
    """
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
    return QUOTED_RE.sub(" ", "\n".join(lines))


def scan_phrases(
    corpus: Corpus, phrases: dict[str, str]
) -> list[dict[str, str]]:
    """Find uses of the phrases outside quotation marks.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    phrases : dict[str, str]
        Phrase to the document that bars it.

    Returns
    -------
    list[dict[str, str]]
        Hits with source id, phrase, and a short snippet.
    """
    hits: list[dict[str, str]] = []
    for entry in corpus.entries:
        text = _strip_quotes(entry.body)
        for phrase in phrases:
            pattern = rf"(?<![\w-]){re.escape(phrase)}(?![\w-])"
            for match in re.finditer(pattern, text, re.IGNORECASE):
                left = max(0, match.start() - 40)
                right = min(len(text), match.end() + 40)
                hits.append(
                    {
                        "source": str(entry.meta["id"]),
                        "phrase": phrase,
                        "snippet": text[left:right].replace("\n", " "),
                    }
                )
    return hits


def extract_normative(corpus: Corpus) -> dict[str, Any]:
    """Collect uses of SHOULD, prefer, and the normative-table words.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, Any]
        ``should`` and ``prefer`` hits in provisions; ``table_words``
        from the Normative Language table; ``unused_words`` that no
        provision body uses; ``term_obligations`` capitalized normative
        words inside Lexicon definitions.
    """
    provisions = corpus.provisions()
    out: dict[str, Any] = {"should": [], "prefer": []}
    for entry in provisions:
        text = without_tables(entry.body)
        for key, pattern in (
            ("should", r"\bshould\b"),
            ("prefer", r"\bprefer\w*"),
        ):
            for match in re.finditer(pattern, text, re.IGNORECASE):
                left = max(0, match.start() - 40)
                right = min(len(text), match.end() + 40)
                out[key].append(
                    {
                        "source": str(entry.meta["id"]),
                        "snippet": text[left:right].replace("\n", " "),
                    }
                )
    words: list[str] = []
    section = corpus.body("LVL0").split("## Normative Language")[-1]
    section = section.split("## Revision History")[0]
    for line in section.splitlines():
        if line.startswith("|") and "---" not in line:
            first = line.strip("|").split("|")[0].strip()
            if first.lower() != "word or phrase":
                words += [w.strip() for w in first.split(",")]
    out["table_words"] = [w for w in words if len(w.split()) <= 3 and w]
    joined = " ".join(e.body for e in provisions).lower()
    out["unused_words"] = [
        w
        for w in out["table_words"]
        if not re.search(
            rf"\b{re.escape(w.lower()).replace('is ', '(?:is|are) ', 1)}\b",
            joined,
        )
    ]
    out["term_obligations"] = [
        {"source": str(t.meta["id"]), "word": m.group(0)}
        for t in corpus.terms()
        for m in CAPITALIZED_RE.finditer(t.body)
    ]
    return out


def extract_terms(corpus: Corpus) -> dict[str, Any]:
    """Collect Lexicon facts: duplicates, bad targets, unused terms.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, Any]
        ``count``, ``incomplete`` (terms missing a field),
        ``duplicates``, ``bad_targets`` (``governed_by`` that is not an
        existing non-Lexicon entry), and ``unused`` (terms no provision
        body uses).
    """
    terms = corpus.terms()
    sections = set(re.findall(r"^## (.+)$", corpus.body("LVL0"), re.M))
    slugs = {heading_slug(s) for s in sections}
    index: dict[str, list[str]] = {}
    incomplete: list[str] = []
    bad_targets: list[dict[str, str]] = []
    for term in terms:
        tid = str(term.meta["id"])
        index.setdefault(
            normalise_term(str(term.meta.get("term", ""))), []
        ).append(tid)
        if not all(term.meta.get(k) for k in ("term", "group", "governed_by")):
            incomplete.append(tid)
        for target in term.meta.get("governed_by") or []:
            entry = corpus.by_id.get(target)
            if target in sections or (
                target.startswith("LVL0#")
                and target.partition("#")[2] in slugs
            ):
                continue
            if entry is None or entry.meta.get("kind") == "term":
                bad_targets.append({"term": tid, "target": target})
    provision_text = " ".join(e.body for e in corpus.provisions()).lower()
    unused = []
    for term in terms:
        stem = normalise_term(str(term.meta.get("term", "")))
        pattern = rf"\b{re.escape(stem)}s?\b".replace(r"\ ", r"[ -]")
        if not re.search(pattern, provision_text):
            unused.append(str(term.meta["id"]))
    return {
        "count": len(terms),
        "incomplete": incomplete,
        "duplicates": {k: v for k, v in index.items() if len(v) > 1},
        "bad_targets": bad_targets,
        "unused": unused,
    }
