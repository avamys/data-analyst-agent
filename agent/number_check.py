"""Number check: every number in the report must come from a recorded value

A number in the text passes if some recorded value rounds to it at the precision
shown (a share may be written as a percentage; the sign is not compared). Plain
integers up to 10 are not checked: they are mostly category labels, degrees of
freedom and counts of tasks.
"""

import re
from collections.abc import Iterable
from typing import Any

SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")

NUMBER = re.compile(
    r"(?<![\w.])"  # not part of an identifier (eda_1) or another number
    r"(?P<int>\d{1,3}(?:,\d{3})+|\d+)(?P<frac>\.\d+)?"
    r"(?:[eE](?P<exp>[-−+]?\d+)|\s*[×x]\s*10\^?(?P<sup>[-−⁻]?[\d⁰¹²³⁴⁵⁶⁷⁸⁹]+))?"
    r"(?P<pct>\s*%)?"
)
# Conventions rather than results
CONVENTIONAL = {0.05}
# A number inside a recorded string or key, e.g. an interval label "(7.91, 14.454]"
LITERAL = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:[eE]-?\d+)?")
# Removed before scanning: inline code, link and image targets, list markers
NOT_PROSE = re.compile(r"`[^`]*`|\]\([^)]*\)|^\s*\d+\.\s", re.MULTILINE)


def numbers_in(text: str) -> list[tuple[str, float, float, str]]:
    """(as written, value, rounding tolerance, line) for each checked number"""
    found = []
    for line in NOT_PROSE.sub(" ", text).splitlines():
        for m in NUMBER.finditer(line):
            before, after = line[: m.start()].rstrip(), line[m.end() :]
            if before.endswith(("<", ">", "≤", "≥")):
                continue  # a threshold, not a value
            if m["pct"] and re.match(r"\s*(CI|conf)", after, re.IGNORECASE):
                continue  # a confidence level
            digits = m["int"].replace(",", "") + (m["frac"] or "")
            exp = m["exp"] or m["sup"]
            exp = int(exp.translate(SUPERSCRIPTS).replace("−", "-")) if exp else 0
            if not m["frac"] and not exp and not m["pct"] and int(digits) <= 10:
                continue
            value = float(digits) * 10.0**exp
            if value in CONVENTIONAL:
                continue
            decimals = len(m["frac"]) - 1 if m["frac"] else 0
            found.append((m[0].strip(), value, 0.5 * 10.0 ** (exp - decimals), line))
    return found


def recorded_values(obj: Any) -> list[float]:
    """Every number in a fact value, profile or other nested structure"""
    if isinstance(obj, bool):
        return []
    if isinstance(obj, int | float):
        return [abs(float(obj))]
    if isinstance(obj, str):
        return [float(m) for m in LITERAL.findall(obj)]
    if isinstance(obj, dict):
        obj = [*obj.keys(), *obj.values()]  # grouped results are keyed by group
    if isinstance(obj, list | tuple):
        return [v for item in obj for v in recorded_values(item)]
    return []


def code_literals(code: str) -> list[float]:
    """Number literals in analysis code: parameters such as test_size=0.25"""
    return [float(m) for m in LITERAL.findall(code)]


def unmatched_numbers(text: str, values: Iterable[float]) -> list[tuple[str, str]]:
    """(number as written, its line) for numbers no recorded value rounds to"""
    values = sorted({abs(v) for v in values})
    unmatched = []
    for written, number, tol, line in numbers_in(text):
        slack = tol + 1e-9 * number  # float noise, relative: p-values are tiny
        if not any(
            abs(v - number) <= slack or abs(v * 100 - number) <= slack for v in values
        ):
            item = (written, line.strip()[:160])
            if item not in unmatched:
                unmatched.append(item)
    return unmatched
