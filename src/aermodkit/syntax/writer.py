"""Preserve and canonical writers for AERMOD runstreams."""

from __future__ import annotations

from typing import Literal

from aermodkit.schema.models import Pathway
from aermodkit.schema.registry import SchemaRegistry, get_registry

from .ast import AermodDocument, PathwayBlock, RawLine, Statement

WriteMode = Literal["preserve", "canonical"]
PATHWAY_ORDER = {
    Pathway.CONTROL: 10,
    Pathway.SOURCE: 20,
    Pathway.RECEPTOR: 30,
    Pathway.METEOROLOGY: 40,
    Pathway.EVENT: 50,
    Pathway.OUTPUT: 60,
}


def write_aermod(
    document: AermodDocument,
    *,
    mode: WriteMode = "preserve",
    registry: SchemaRegistry | None = None,
) -> str:
    registry = registry or get_registry(document.version)
    if mode == "preserve":
        lines = _preserve_lines(document)
    elif mode == "canonical":
        lines = _canonical_lines(document, registry)
    else:
        raise ValueError(f"unknown writer mode {mode!r}")
    text = "\n".join(lines)
    if document.trailing_newline:
        text += "\n"
    return text


def _preserve_lines(document: AermodDocument) -> list[str]:
    lines: list[str] = []
    for node in document.nodes:
        if isinstance(node, RawLine):
            lines.append(node.text)
        else:
            lines.append(node.starting_text)
            for child in node.nodes:
                lines.append(child.text if isinstance(child, RawLine) else child.original_text)
            if node.finished_text is not None:
                lines.append(node.finished_text)
    return lines


def _canonical_lines(document: AermodDocument, registry: SchemaRegistry) -> list[str]:
    lines: list[str] = []
    leading_raw = [node for node in document.nodes if isinstance(node, RawLine)]
    lines.extend(raw.text for raw in leading_raw)

    blocks = sorted(document.pathways(), key=lambda block: PATHWAY_ORDER[block.pathway])
    for block in blocks:
        lines.append(f"{block.pathway.value} STARTING")
        raw_nodes = [node for node in block.nodes if isinstance(node, RawLine)]
        lines.extend(raw.text for raw in raw_nodes)

        statements = [node for node in block.nodes if isinstance(node, Statement)]
        statements.sort(key=lambda item: _statement_sort_key(item, registry))
        for statement in statements:
            lines.append(_canonical_statement(statement, registry))
        lines.append(f"{block.pathway.value} FINISHED")
    return lines


def _statement_sort_key(statement: Statement, registry: SchemaRegistry) -> tuple[int, int, str]:
    spec = registry.keyword(statement.pathway, statement.keyword)
    return (
        0 if spec is not None else 1,
        spec.order if spec is not None else 9999,
        statement.keyword,
    )


def _canonical_statement(statement: Statement, registry: SchemaRegistry) -> str:
    if not statement.known:
        return statement.original_text.strip()
    arguments = statement.arguments
    if statement.pathway is Pathway.CONTROL and statement.keyword == "MODELOPT":
        arguments = registry.canonical_option_order(arguments)
    suffix = f" {' '.join(arguments)}" if arguments else ""
    return f"{statement.pathway.value} {statement.keyword}{suffix}"
