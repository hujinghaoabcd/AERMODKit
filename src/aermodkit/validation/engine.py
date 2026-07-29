"""Validation engine for the lossless AST."""

from __future__ import annotations

from collections import Counter

from aermodkit.schema.models import Diagnostic, DiagnosticSeverity, Pathway
from aermodkit.schema.registry import SchemaRegistry, get_registry
from aermodkit.syntax.ast import AermodDocument, RawLine


def validate_document(
    document: AermodDocument,
    *,
    registry: SchemaRegistry | None = None,
) -> list[Diagnostic]:
    registry = registry or get_registry(document.version)
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(_validate_structure(document))
    diagnostics.extend(_validate_keywords(document, registry))
    options = _model_options(document)
    modelopt_lines = document.statements(Pathway.CONTROL, "MODELOPT")
    line = modelopt_lines[0].line if modelopt_lines else None
    diagnostics.extend(_with_line(registry.validate_model_options(options), line))
    diagnostics.extend(_validate_sources(document, registry, options))
    return diagnostics


def _validate_structure(document: AermodDocument) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    counts = Counter(block.pathway for block in document.pathways())
    for pathway, count in counts.items():
        if count > 1:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SYNTAX-DUPLICATE-PATHWAY", severity=DiagnosticSeverity.ERROR, message=f"pathway {pathway.value} appears {count} times", pathway=pathway))
    for node in document.nodes:
        if isinstance(node, RawLine) and node.kind == "outside-pathway":
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SYNTAX-OUTSIDE-PATHWAY", severity=DiagnosticSeverity.WARNING, message="content outside a pathway block is preserved but not interpreted", line=node.line))
    return diagnostics


def _validate_keywords(document: AermodDocument, registry: SchemaRegistry) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for block in document.pathways():
        present = Counter(statement.keyword for statement in block.statements())
        for statement in block.statements():
            spec = registry.keyword(block.pathway, statement.keyword)
            if spec is None:
                diagnostics.append(Diagnostic(rule_id="AERMODKIT-SCHEMA-UNKNOWN-KEYWORD", severity=DiagnosticSeverity.WARNING, message=f"unknown v{registry.version} keyword {statement.keyword}; it will be retained in preserve mode", pathway=block.pathway, keyword=statement.keyword, line=statement.line))
                continue
            argc = len(statement.arguments)
            if argc < spec.min_args or (spec.max_args is not None and argc > spec.max_args):
                expected = f"{spec.min_args}+" if spec.max_args is None else (str(spec.min_args) if spec.min_args == spec.max_args else f"{spec.min_args}..{spec.max_args}")
                diagnostics.append(Diagnostic(rule_id="AERMODKIT-SCHEMA-ARGUMENT-COUNT", severity=DiagnosticSeverity.ERROR, message=f"{block.pathway.value} {statement.keyword} expects {expected} argument(s), got {argc}", pathway=block.pathway, keyword=statement.keyword, line=statement.line, evidence=spec.evidence))
            if not spec.repeatable and present[statement.keyword] > 1:
                diagnostics.append(Diagnostic(rule_id="AERMODKIT-SCHEMA-NONREPEATABLE", severity=DiagnosticSeverity.ERROR, message=f"{statement.keyword} is not repeatable", pathway=block.pathway, keyword=statement.keyword, line=statement.line, evidence=spec.evidence))
                present[statement.keyword] = 1
        for spec in registry.keywords.values():
            if spec.pathway is block.pathway and spec.mandatory and present[spec.name] == 0:
                diagnostics.append(Diagnostic(rule_id="AERMODKIT-SCHEMA-MISSING-MANDATORY", severity=DiagnosticSeverity.ERROR, message=f"missing mandatory {block.pathway.value} keyword {spec.name}", pathway=block.pathway, keyword=spec.name, evidence=spec.evidence))
    return diagnostics


def _model_options(document: AermodDocument) -> set[str]:
    options: set[str] = set()
    for statement in document.statements(Pathway.CONTROL, "MODELOPT"):
        options.update(argument.upper() for argument in statement.arguments)
    return options


def _validate_sources(document: AermodDocument, registry: SchemaRegistry, options: set[str]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    source_types: dict[str, tuple[str, int]] = {}
    for statement in document.statements(Pathway.SOURCE, "LOCATION"):
        if len(statement.arguments) < 2:
            continue
        source_id, type_name = statement.arguments[0], statement.arguments[1].upper()
        if source_id in source_types:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-DUPLICATE-ID", severity=DiagnosticSeverity.ERROR, message=f"duplicate source ID {source_id!r}", pathway=Pathway.SOURCE, keyword="LOCATION", line=statement.line, source_id=source_id))
            continue
        spec = registry.source_type(type_name)
        if spec is None:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-UNKNOWN-TYPE", severity=DiagnosticSeverity.ERROR, message=f"unknown v{registry.version} source type {type_name!r}", pathway=Pathway.SOURCE, keyword="LOCATION", line=statement.line, source_id=source_id))
            continue
        source_types[source_id] = (type_name, statement.line)
        argc = len(statement.arguments)
        if not (spec.location_min_args <= argc <= spec.location_max_args):
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-LOCATION-ARGUMENTS", severity=DiagnosticSeverity.ERROR, message=f"LOCATION for {type_name} expects {spec.location_min_args}..{spec.location_max_args} arguments, got {argc}", pathway=Pathway.SOURCE, keyword="LOCATION", line=statement.line, source_id=source_id, evidence=spec.evidence))
        missing = spec.required_options - options
        if missing:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-REQUIRES-MODELOPT", severity=DiagnosticSeverity.ERROR, message=f"source type {type_name} requires MODELOPT {', '.join(sorted(missing))}", pathway=Pathway.SOURCE, keyword="LOCATION", line=statement.line, source_id=source_id, evidence=spec.evidence))
        if "DFAULT" in options and spec.regulatory_default_compatible is False:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-DFAULT-CONFLICT", severity=DiagnosticSeverity.ERROR, message=f"source type {type_name} cannot be used with DFAULT", pathway=Pathway.SOURCE, keyword="LOCATION", line=statement.line, source_id=source_id, evidence=spec.evidence))

    seen_srcparams: set[str] = set()
    for statement in document.statements(Pathway.SOURCE, "SRCPARAM"):
        if not statement.arguments:
            continue
        source_id = statement.arguments[0]
        entry = source_types.get(source_id)
        if entry is None:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-SRCPARAM-WITHOUT-LOCATION", severity=DiagnosticSeverity.ERROR, message=f"SRCPARAM references {source_id!r} before/without LOCATION", pathway=Pathway.SOURCE, keyword="SRCPARAM", line=statement.line, source_id=source_id))
            continue
        type_name, _ = entry
        spec = registry.source_type(type_name)
        assert spec is not None
        argc = len(statement.arguments)
        if not (spec.srcparam_min_args <= argc <= spec.srcparam_max_args):
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-SRCPARAM-ARGUMENTS", severity=DiagnosticSeverity.ERROR, message=f"SRCPARAM for {type_name} expects {spec.srcparam_min_args}..{spec.srcparam_max_args} arguments, got {argc}", pathway=Pathway.SOURCE, keyword="SRCPARAM", line=statement.line, source_id=source_id, evidence=spec.evidence))
        seen_srcparams.add(source_id)
    for source_id, (type_name, line) in source_types.items():
        if source_id not in seen_srcparams:
            diagnostics.append(Diagnostic(rule_id="AERMODKIT-SOURCE-MISSING-SRCPARAM", severity=DiagnosticSeverity.ERROR, message=f"source {source_id!r} ({type_name}) has no SRCPARAM", pathway=Pathway.SOURCE, keyword="SRCPARAM", line=line, source_id=source_id))
    return diagnostics


def _with_line(diagnostics: list[Diagnostic], line: int | None) -> list[Diagnostic]:
    if line is None:
        return diagnostics
    return [Diagnostic(rule_id=item.rule_id, severity=item.severity, message=item.message, pathway=item.pathway, keyword=item.keyword, line=item.line if item.line is not None else line, source_id=item.source_id, evidence=item.evidence, context=item.context) for item in diagnostics]
