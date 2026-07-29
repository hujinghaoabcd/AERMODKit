"""Lossless AERMOD runstream parser."""

from __future__ import annotations

from aermodkit.schema.models import AermodVersion, Pathway
from aermodkit.schema.registry import SchemaRegistry, get_registry

from .ast import AermodDocument, PathwayBlock, RawLine, Statement
from .lexer import classify_raw_line, split_tokens


def parse_aermod(
    text: str,
    *,
    version: AermodVersion | int | str = "26135",
    registry: SchemaRegistry | None = None,
) -> AermodDocument:
    """Parse a runstream without discarding comments or unknown statements."""

    registry = registry or get_registry(version)
    document = AermodDocument(
        version=registry.version,
        trailing_newline=text.endswith(("\n", "\r")),
    )
    current: PathwayBlock | None = None

    for line_number, original in enumerate(text.splitlines(), start=1):
        raw_kind = classify_raw_line(original)
        if raw_kind is not None:
            raw = RawLine(original, line_number, raw_kind)
            if current is None:
                document.nodes.append(raw)
            else:
                current.nodes.append(raw)
            continue

        tokens = split_tokens(original)
        marker = _pathway_marker(tokens)
        if marker is not None:
            pathway, action = marker
            if action == "STARTING":
                if current is not None:
                    raise ValueError(
                        f"line {line_number}: {pathway.value} STARTING before "
                        f"{current.pathway.value} FINISHED"
                    )
                current = PathwayBlock(pathway, original, line_number)
                document.nodes.append(current)
            else:
                if current is None or current.pathway is not pathway:
                    raise ValueError(
                        f"line {line_number}: {pathway.value} FINISHED has no matching block"
                    )
                current.finished_text = original
                current.finished_line = line_number
                current = None
            continue

        if current is None:
            document.nodes.append(RawLine(original, line_number, "outside-pathway"))
            continue

        pathway, keyword, arguments = _statement_parts(current.pathway, tokens)
        spec = registry.keyword(pathway, keyword)
        current.nodes.append(
            Statement(
                pathway=pathway,
                keyword=keyword,
                arguments=arguments,
                original_text=original,
                line=line_number,
                known=spec is not None,
            )
        )

    if current is not None:
        raise ValueError(
            f"line {current.starting_line}: {current.pathway.value} STARTING without FINISHED"
        )
    return document


def _pathway_marker(tokens: tuple[str, ...]) -> tuple[Pathway, str] | None:
    if len(tokens) < 2:
        return None
    try:
        pathway = Pathway.parse(tokens[0])
    except ValueError:
        return None
    action = tokens[1].upper()
    if action not in {"STARTING", "FINISHED"}:
        return None
    return pathway, action


def _statement_parts(
    current_pathway: Pathway,
    tokens: tuple[str, ...],
) -> tuple[Pathway, str, tuple[str, ...]]:
    if not tokens:
        raise ValueError("internal parser error: empty statement")
    try:
        prefixed = Pathway.parse(tokens[0])
    except ValueError:
        prefixed = None

    if prefixed is not None:
        if prefixed is not current_pathway:
            raise ValueError(
                f"statement pathway prefix {prefixed.value} does not match "
                f"open {current_pathway.value} block"
            )
        if len(tokens) < 2:
            raise ValueError("pathway prefix must be followed by a keyword")
        return prefixed, tokens[1].upper(), tokens[2:]
    return current_pathway, tokens[0].upper(), tokens[1:]
