"""Lossless AST for AERMOD input runstreams."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias

from aermodkit.schema.models import AermodVersion, Pathway


@dataclass(slots=True)
class RawLine:
    """Blank, comment, or otherwise unparsed text preserved verbatim."""

    text: str
    line: int
    kind: str = "raw"


@dataclass(slots=True)
class Statement:
    pathway: Pathway
    keyword: str
    arguments: tuple[str, ...]
    original_text: str
    line: int
    known: bool

    def __post_init__(self) -> None:
        self.keyword = self.keyword.upper()


BlockNode: TypeAlias = RawLine | Statement


@dataclass(slots=True)
class PathwayBlock:
    pathway: Pathway
    starting_text: str
    starting_line: int
    nodes: list[BlockNode] = field(default_factory=list)
    finished_text: str | None = None
    finished_line: int | None = None

    def statements(self, keyword: str | None = None) -> list[Statement]:
        result = [node for node in self.nodes if isinstance(node, Statement)]
        if keyword is not None:
            target = keyword.upper()
            result = [node for node in result if node.keyword == target]
        return result


DocumentNode: TypeAlias = RawLine | PathwayBlock


@dataclass(slots=True)
class AermodDocument:
    version: AermodVersion
    nodes: list[DocumentNode] = field(default_factory=list)
    trailing_newline: bool = True
    project_format_version: str = "1.0"

    def pathways(self, pathway: Pathway | str | None = None) -> list[PathwayBlock]:
        blocks = [node for node in self.nodes if isinstance(node, PathwayBlock)]
        if pathway is not None:
            target = Pathway.parse(pathway)
            blocks = [block for block in blocks if block.pathway is target]
        return blocks

    def statements(self, pathway: Pathway | str, keyword: str | None = None) -> list[Statement]:
        result: list[Statement] = []
        for block in self.pathways(pathway):
            result.extend(block.statements(keyword))
        return result
