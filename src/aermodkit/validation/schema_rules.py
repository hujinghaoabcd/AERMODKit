"""Document structure, keyword, and continuation-family rules."""

from __future__ import annotations

from collections import Counter

from aermodkit.schema.models import (
    ContinuationFamilySpec,
    Diagnostic,
    DiagnosticSeverity,
)
from aermodkit.schema.registry import SchemaRegistry
from aermodkit.syntax.ast import AermodDocument, RawLine, Statement


def validate_structure(document: AermodDocument) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    counts = Counter(block.pathway for block in document.pathways())
    for pathway, count in counts.items():
        if count > 1:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SYNTAX-DUPLICATE-PATHWAY",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"pathway {pathway.value} appears {count} times",
                    pathway=pathway,
                )
            )
    for node in document.nodes:
        if isinstance(node, RawLine) and node.kind == "outside-pathway":
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SYNTAX-OUTSIDE-PATHWAY",
                    severity=DiagnosticSeverity.WARNING,
                    message="content outside a pathway block is preserved but not interpreted",
                    line=node.line,
                )
            )
    return diagnostics


def validate_keywords(
    document: AermodDocument,
    registry: SchemaRegistry,
    options: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for block in document.pathways():
        statements = block.statements()
        present = Counter(statement.keyword for statement in statements)
        present_names = set(present)
        first_statement = statements[0] if statements else None

        for statement_index, statement in enumerate(statements):
            spec = registry.keyword(block.pathway, statement.keyword)
            if spec is None:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-UNKNOWN-KEYWORD",
                        severity=DiagnosticSeverity.WARNING,
                        message=(
                            f"unknown v{registry.version} keyword {statement.keyword}; "
                            "it will be retained in preserve mode"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                    )
                )
                continue

            argc = len(statement.arguments)
            if argc < spec.min_args or (spec.max_args is not None and argc > spec.max_args):
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-ARGUMENT-COUNT",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{block.pathway.value} {statement.keyword} expects "
                            f"{_expected_args(spec.min_args, spec.max_args)} argument(s), "
                            f"got {argc}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
            if not spec.repeatable and present[statement.keyword] > 1:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-NONREPEATABLE",
                        severity=DiagnosticSeverity.ERROR,
                        message=f"{statement.keyword} is not repeatable",
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
                present[statement.keyword] = 1

            missing_keywords = spec.requires_keywords - present_names
            if missing_keywords:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-KEYWORD-DEPENDENCY",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{statement.keyword} requires keyword(s): "
                            f"{', '.join(sorted(missing_keywords))}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
            missing_options = spec.requires_options - options
            if missing_options:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-OPTION-DEPENDENCY",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{statement.keyword} requires MODELOPT "
                            f"{', '.join(sorted(missing_options))}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
            active_conflicts = spec.conflicts_keywords & present_names
            if active_conflicts:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-KEYWORD-CONFLICT",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{statement.keyword} cannot be combined with "
                            f"{', '.join(sorted(active_conflicts))}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
            if spec.first_if_present and first_statement is not statement:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-KEYWORD-ORDER-FIRST",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{statement.keyword} must be the first keyword in "
                            f"{block.pathway.value}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )
            later_keywords = {item.keyword for item in statements[statement_index + 1 :]}
            if spec.must_be_last and (later_keywords - {statement.keyword}):
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-KEYWORD-ORDER-LAST",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{statement.keyword} must be the final keyword family in "
                            f"{block.pathway.value}"
                        ),
                        pathway=block.pathway,
                        keyword=statement.keyword,
                        line=statement.line,
                        evidence=spec.evidence,
                    )
                )

        for spec in registry.pathway_keywords(block.pathway):
            exempt = bool(spec.mandatory_unless & present_names)
            if spec.mandatory and present[spec.name] == 0 and not exempt:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-MISSING-MANDATORY",
                        severity=DiagnosticSeverity.ERROR,
                        message=f"missing mandatory {block.pathway.value} keyword {spec.name}",
                        pathway=block.pathway,
                        keyword=spec.name,
                        evidence=spec.evidence,
                    )
                )
    return diagnostics


def validate_continuations(
    document: AermodDocument,
    registry: SchemaRegistry,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for family in registry.continuation_families.values():
        open_networks: set[str] = set()
        for statement in document.statements(family.pathway, family.keyword):
            if len(statement.arguments) <= family.action_index:
                continue
            network_id = statement.arguments[0].upper()
            action = statement.arguments[family.action_index].upper()
            if action in family.start_tokens:
                if network_id in open_networks:
                    diagnostics.append(
                        _continuation_issue(
                            family,
                            statement,
                            f"{family.keyword} network {network_id} is started more than once",
                        )
                    )
                open_networks.add(network_id)
            elif action in family.end_tokens:
                if network_id not in open_networks:
                    diagnostics.append(
                        _continuation_issue(
                            family,
                            statement,
                            f"{family.keyword} network {network_id} ends without STA",
                        )
                    )
                else:
                    open_networks.remove(network_id)
            elif action in family.member_tokens:
                if network_id not in open_networks:
                    diagnostics.append(
                        _continuation_issue(
                            family,
                            statement,
                            f"{family.keyword} {action} for {network_id} occurs outside STA/END",
                        )
                    )
            else:
                diagnostics.append(
                    _continuation_issue(
                        family,
                        statement,
                        f"unknown {family.keyword} continuation action {action!r}",
                    )
                )
        for network_id in sorted(open_networks):
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-SYNTAX-CONTINUATION-UNCLOSED",
                    severity=DiagnosticSeverity.ERROR,
                    message=f"{family.keyword} network {network_id} has no END record",
                    pathway=family.pathway,
                    keyword=family.keyword,
                    evidence=family.evidence,
                )
            )
    return diagnostics


def _continuation_issue(
    family: ContinuationFamilySpec,
    statement: Statement,
    message: str,
) -> Diagnostic:
    return Diagnostic(
        rule_id="AERMODKIT-SYNTAX-CONTINUATION",
        severity=DiagnosticSeverity.ERROR,
        message=message,
        pathway=family.pathway,
        keyword=family.keyword,
        line=statement.line,
        evidence=family.evidence,
    )


def _expected_args(minimum: int, maximum: int | None) -> str:
    if maximum is None:
        return f"{minimum}+"
    if minimum == maximum:
        return str(minimum)
    return f"{minimum}..{maximum}"
