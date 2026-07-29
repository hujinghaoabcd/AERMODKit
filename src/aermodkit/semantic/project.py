"""Read-only semantic projection over the lossless runstream AST."""

from __future__ import annotations

from dataclasses import dataclass, field

from aermodkit.schema.models import AermodVersion, Pathway
from aermodkit.syntax.ast import AermodDocument, Statement


@dataclass(frozen=True, slots=True)
class SourceRecord:
    source_id: str
    source_type: str
    location_arguments: tuple[str, ...]
    source_parameters: tuple[str, ...] | None
    location_line: int
    srcparam_line: int | None = None


@dataclass(frozen=True, slots=True)
class AermodProjectModel:
    """Semantic view that keeps the original document as its authority."""

    document: AermodDocument
    version: AermodVersion
    model_options: frozenset[str]
    pollutant: str | None
    averaging_periods: tuple[str, ...]
    sources: tuple[SourceRecord, ...]
    meteorology: dict[str, tuple[tuple[str, ...], ...]] = field(default_factory=dict)
    outputs: dict[str, tuple[tuple[str, ...], ...]] = field(default_factory=dict)
    included_files: tuple[tuple[Pathway, str], ...] = ()

    @classmethod
    def from_document(cls, document: AermodDocument) -> AermodProjectModel:
        return cls(
            document=document,
            version=document.version,
            model_options=frozenset(_flatten(document, Pathway.CONTROL, "MODELOPT")),
            pollutant=_first_argument(document, Pathway.CONTROL, "POLLUTID"),
            averaging_periods=tuple(_flatten(document, Pathway.CONTROL, "AVERTIME")),
            sources=_sources(document),
            meteorology=_group_arguments(document, Pathway.METEOROLOGY),
            outputs=_group_arguments(document, Pathway.OUTPUT),
            included_files=tuple(
                (block.pathway, statement.arguments[0])
                for block in document.pathways()
                for statement in block.statements("INCLUDED")
                if statement.arguments
            ),
        )


def build_project_model(document: AermodDocument) -> AermodProjectModel:
    return AermodProjectModel.from_document(document)


def _sources(document: AermodDocument) -> tuple[SourceRecord, ...]:
    params = {
        statement.arguments[0]: statement
        for statement in document.statements(Pathway.SOURCE, "SRCPARAM")
        if statement.arguments
    }
    records: list[SourceRecord] = []
    for statement in document.statements(Pathway.SOURCE, "LOCATION"):
        if len(statement.arguments) < 2:
            continue
        source_id, source_type = statement.arguments[0], statement.arguments[1].upper()
        srcparam = params.get(source_id)
        records.append(
            SourceRecord(
                source_id=source_id,
                source_type=source_type,
                location_arguments=statement.arguments[2:],
                source_parameters=srcparam.arguments[1:] if srcparam else None,
                location_line=statement.line,
                srcparam_line=srcparam.line if srcparam else None,
            )
        )
    return tuple(records)


def _group_arguments(
    document: AermodDocument,
    pathway: Pathway,
) -> dict[str, tuple[tuple[str, ...], ...]]:
    grouped: dict[str, list[tuple[str, ...]]] = {}
    for statement in document.statements(pathway):
        grouped.setdefault(statement.keyword, []).append(statement.arguments)
    return {key: tuple(values) for key, values in grouped.items()}


def _flatten(document: AermodDocument, pathway: Pathway, keyword: str) -> list[str]:
    return [
        argument.upper()
        for statement in document.statements(pathway, keyword)
        for argument in statement.arguments
    ]


def _first_argument(
    document: AermodDocument,
    pathway: Pathway,
    keyword: str,
) -> str | None:
    statements: list[Statement] = document.statements(pathway, keyword)
    return statements[0].arguments[0].upper() if statements and statements[0].arguments else None
