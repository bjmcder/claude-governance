"""The result model: one result per check, collected in a report.

A status is ``PASS`` (claim verified), ``FAIL`` (claim violated),
``WARN`` (worth a look), or ``INFO`` (a listing for a reader).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

LIST_CAP = 25


@dataclass
class CheckResult:
    """Outcome of one check.

    Parameters
    ----------
    key : str
        Check key such as ``a.1`` or ``manifests``.
    title : str
        What the check establishes.
    status : str
        ``PASS``, ``FAIL``, ``WARN``, or ``INFO``.
    details : list[str]
        Evidence lines in Markdown.
    """

    key: str
    title: str
    status: str
    details: list[str] = field(default_factory=list)


@dataclass
class Report:
    """Check results in the order they were reported.

    Parameters
    ----------
    results : list[CheckResult]
        Results so far.
    """

    results: list[CheckResult] = field(default_factory=list)

    def add(
        self,
        key: str,
        title: str,
        status: str,
        details: Iterable[str] = (),
    ) -> CheckResult:
        """Record a result, dropping empty detail lines.

        Parameters
        ----------
        key : str
            Check key.
        title : str
            Check title.
        status : str
            Result status.
        details : Iterable[str]
            Evidence lines.

        Returns
        -------
        CheckResult
            The recorded result.
        """
        result = CheckResult(key, title, status, [d for d in details if d])
        self.results.append(result)
        return result

    def failures(self) -> list[CheckResult]:
        """Return the results whose status is ``FAIL``.

        Returns
        -------
        list[CheckResult]
            Failed results, in report order.
        """
        return [r for r in self.results if r.status == "FAIL"]

    def warnings(self) -> list[CheckResult]:
        """Return the results whose status is ``WARN``.

        Returns
        -------
        list[CheckResult]
            Warned results, in report order.
        """
        return [r for r in self.results if r.status == "WARN"]

    def render(self, header: list[str]) -> str:
        """Render the report as Markdown text.

        Parameters
        ----------
        header : list[str]
            Lines placed under the title.

        Returns
        -------
        str
            A summary table and one section per result.
        """
        out = ["# Logic and consistency report", "", *header, ""]
        out += ["| Check | Status | Title |", "| --- | --- | --- |"]
        out += [f"| {r.key} | {r.status} | {r.title} |" for r in self.results]
        out.append("")
        for result in self.results:
            out.append(f"## {result.key} — {result.title} [{result.status}]")
            out.append("")
            out.extend(result.details or ["(no details)"])
            out.append("")
        return "\n".join(out)


def capped(lines: list[str], limit: int = LIST_CAP) -> list[str]:
    """Return at most a limited number of lines, noting the rest.

    Parameters
    ----------
    lines : list[str]
        Evidence lines.
    limit : int
        Most lines kept.

    Returns
    -------
    list[str]
        The first ``limit`` lines and a count of those omitted.
    """
    if len(lines) <= limit:
        return lines
    return [*lines[:limit], f"- (+{len(lines) - limit} more)"]
