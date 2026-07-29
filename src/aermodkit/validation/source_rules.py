"""Source identity, source-type, and parameter-card validation."""

from __future__ import annotations

from aermodkit.schema.models import Diagnostic, DiagnosticSeverity, Pathway
from aermodkit.schema.registry import SchemaRegistry
from aermodkit.syntax.ast import AermodDocument


def validate_sources(
    document: AermodDocument,
    registry: SchemaRegistry,
    options: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    source_types: dict[str, tuple[str, int]] = {}

    for statement in document.statements(Pathway.SOURCE, "LOCATION"):
        if len(statement.arguments) < 2:
            continue
        source_id, type_name = statement.arguments[0], statement.arguments[1].upper()
        if source_id in source_types:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-DUPLICATE-ID",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"duplicate source ID {source_id!r}",
                    pathway=Pathway.SOURCE,
                    keyword="LOCATION",
                    line=statement.line,
                    source_id=source_id,
                )
            )
            continue
        spec = registry.source_type(type_name)
        if spec is None:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-UNKNOWN-TYPE",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"unknown v{registry.version} source type {type_name!r}",
                    pathway=Pathway.SOURCE,
                    keyword="LOCATION",
                    line=statement.line,
                    source_id=source_id,
                )
            )
            continue

        source_types[source_id] = (type_name, statement.line)
        argc = len(statement.arguments)
        if not (spec.location_min_args <= argc <= spec.location_max_args):
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-LOCATION-ARGUMENTS",
                    severity=DiagnosticSeverity.ERROR,
                    message=(
                        f"LOCATION for {type_name} expects {spec.location_min_args}.."
                        f"{spec.location_max_args} arguments, got {argc}"
                    ),
                    pathway=Pathway.SOURCE,
                    keyword="LOCATION",
                    line=statement.line,
                    source_id=source_id,
                    evidence=spec.evidence,
                )
            )
        missing = spec.required_options - options
        if missing:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-REQUIRES-MODELOPT",
                    severity=DiagnosticSeverity.ERROR,
                    message=(
                        f"source type {type_name} requires MODELOPT "
                        f"{', '.join(sorted(missing))}"
                    ),
                    pathway=Pathway.SOURCE,
                    keyword="LOCATION",
                    line=statement.line,
                    source_id=source_id,
                    evidence=spec.evidence,
                )
            )
        if "DFAULT" in options and spec.regulatory_default_compatible is False:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-DFAULT-CONFLICT",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"source type {type_name} cannot be used with DFAULT",
                    pathway=Pathway.SOURCE,
                    keyword="LOCATION",
                    line=statement.line,
                    source_id=source_id,
                    evidence=spec.evidence,
                )
            )

    seen_srcparams: set[str] = set()
    for statement in document.statements(Pathway.SOURCE, "SRCPARAM"):
        if not statement.arguments:
            continue
        source_id = statement.arguments[0]
        entry = source_types.get(source_id)
        if entry is None:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-SRCPARAM-WITHOUT-LOCATION",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"SRCPARAM references {source_id!r} before/without LOCATION",
                    pathway=Pathway.SOURCE,
                    keyword="SRCPARAM",
                    line=statement.line,
                    source_id=source_id,
                )
            )
            continue
        type_name, _ = entry
        spec = registry.source_type(type_name)
        assert spec is not None
        argc = len(statement.arguments)
        if not (spec.srcparam_min_args <= argc <= spec.srcparam_max_args):
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-SRCPARAM-ARGUMENTS",
                    severity=DiagnosticSeverity.ERROR,
                    message=(
                        f"SRCPARAM for {type_name} expects {spec.srcparam_min_args}.."
                        f"{spec.srcparam_max_args} arguments, got {argc}"
                    ),
                    pathway=Pathway.SOURCE,
                    keyword="SRCPARAM",
                    line=statement.line,
                    source_id=source_id,
                    evidence=spec.evidence,
                )
            )
        seen_srcparams.add(source_id)

    for source_id, (type_name, line) in source_types.items():
        if source_id not in seen_srcparams:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SOURCE-MISSING-SRCPARAM",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"source {source_id!r} ({type_name}) has no SRCPARAM",
                    pathway=Pathway.SOURCE,
                    keyword="SRCPARAM",
                    line=line,
                    source_id=source_id,
                )
            )
    return diagnostics
