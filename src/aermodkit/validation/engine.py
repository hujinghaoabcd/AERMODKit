"""Validation engine for the lossless AST."""

from __future__ import annotations

from aermodkit.schema.models import Diagnostic, Pathway
from aermodkit.schema.registry import SchemaRegistry, get_registry
from aermodkit.syntax.ast import AermodDocument

from .cross_rules import validate_cross_pathway_rules
from .schema_rules import validate_continuations, validate_keywords, validate_structure
from .source_rules import validate_sources
from .utils import deduplicate, model_options, with_line


def validate_document(
    document: AermodDocument,
    *,
    registry: SchemaRegistry | None = None,
) -> list[Diagnostic]:
    registry = registry or get_registry(document.version)
    options = model_options(document)
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(validate_structure(document))
    diagnostics.extend(validate_keywords(document, registry, options))
    diagnostics.extend(validate_continuations(document, registry))
    diagnostics.extend(validate_cross_pathway_rules(document, options))
    modelopt_lines = document.statements(Pathway.CONTROL, "MODELOPT")
    line = modelopt_lines[0].line if modelopt_lines else None
    diagnostics.extend(with_line(registry.validate_model_options(options), line))
    diagnostics.extend(validate_sources(document, registry, options))
    return deduplicate(diagnostics)
