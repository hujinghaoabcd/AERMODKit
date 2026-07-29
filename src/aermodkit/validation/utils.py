"""Shared validation helpers."""

from __future__ import annotations

from dataclasses import replace

from aermodkit.schema.models import Diagnostic, Pathway
from aermodkit.syntax.ast import AermodDocument


def model_options(document: AermodDocument) -> set[str]:
    return {
        argument.upper()
        for statement in document.statements(Pathway.CONTROL, "MODELOPT")
        for argument in statement.arguments
    }


def with_line(diagnostics: list[Diagnostic], line: int | None) -> list[Diagnostic]:
    if line is None:
        return diagnostics
    return [replace(item, line=item.line if item.line is not None else line) for item in diagnostics]


def deduplicate(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple[str, str, int | None, str | None]] = set()
    result: list[Diagnostic] = []
    for item in diagnostics:
        key = (item.rule_id, item.message, item.line, item.source_id)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
