"""Schema registry loading and lookup."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

from .models import (
    AermodVersion,
    Diagnostic,
    DiagnosticSeverity,
    KeywordSpec,
    ModelOptionSpec,
    Pathway,
    SourceTypeSpec,
)


@dataclass(frozen=True, slots=True)
class SchemaRegistry:
    version: AermodVersion
    keywords: dict[tuple[Pathway, str], KeywordSpec]
    model_options: dict[str, ModelOptionSpec]
    source_types: dict[str, SourceTypeSpec]

    def keyword(self, pathway: Pathway | str, name: str) -> KeywordSpec | None:
        return self.keywords.get((Pathway.parse(pathway), name.upper()))

    def model_option(self, name: str) -> ModelOptionSpec | None:
        return self.model_options.get(name.upper())

    def source_type(self, name: str) -> SourceTypeSpec | None:
        return self.source_types.get(name.upper())

    def canonical_option_order(self, options: Iterable[str]) -> tuple[str, ...]:
        unique = {option.upper() for option in options}
        return tuple(
            sorted(
                unique,
                key=lambda name: (
                    self.model_options[name].order if name in self.model_options else 9999,
                    name,
                ),
            )
        )

    def validate_model_options(self, options: Iterable[str]) -> list[Diagnostic]:
        selected = {option.upper() for option in options}
        diagnostics: list[Diagnostic] = []

        for option in sorted(selected):
            spec = self.model_options.get(option)
            if spec is None:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-SCHEMA-UNKNOWN-MODELOPT",
                        severity=DiagnosticSeverity.ERROR,
                        message=f"MODELOPT contains unknown v{self.version} option {option!r}",
                        pathway=Pathway.CONTROL,
                        keyword="MODELOPT",
                    )
                )
                continue

            if "DFAULT" in selected and spec.allowed_with_dfault is False:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-V26135-DFAULT-CONFLICT",
                        severity=DiagnosticSeverity.ERROR,
                        message=f"{option} cannot be used with DFAULT in AERMOD v{self.version}",
                        pathway=Pathway.CONTROL,
                        keyword="MODELOPT",
                        evidence=spec.evidence,
                    )
                )

            missing_all = spec.requires_all - selected
            if missing_all:
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-V26135-MODELOPT-REQUIRES-ALL",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{option} requires option(s): {', '.join(sorted(missing_all))}"
                        ),
                        pathway=Pathway.CONTROL,
                        keyword="MODELOPT",
                        evidence=spec.evidence,
                    )
                )

            if spec.requires_any and not (spec.requires_any & selected):
                diagnostics.append(
                    Diagnostic(
                        rule_id="AERMODKIT-V26135-MODELOPT-REQUIRES-ANY",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            f"{option} requires one of: "
                            f"{', '.join(sorted(spec.requires_any))}"
                        ),
                        pathway=Pathway.CONTROL,
                        keyword="MODELOPT",
                        evidence=spec.evidence,
                    )
                )

            active_conflicts = spec.conflicts & selected
            for conflict in sorted(active_conflicts):
                if option < conflict:
                    diagnostics.append(
                        Diagnostic(
                            rule_id="AERMODKIT-V26135-MODELOPT-CONFLICT",
                            severity=DiagnosticSeverity.ERROR,
                            message=f"{option} cannot be combined with {conflict}",
                            pathway=Pathway.CONTROL,
                            keyword="MODELOPT",
                            evidence=spec.evidence,
                        )
                    )

        base_methods = selected & {"PVMRM", "OLM", "ARM2"}
        if "TTRM" in selected and base_methods and "TTRM2" not in selected:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-V26135-TTRM-PAIRING",
                    severity=DiagnosticSeverity.ERROR,
                    message="TTRM cannot be paired with PVMRM/OLM/ARM2 unless TTRM2 is used",
                    pathway=Pathway.CONTROL,
                    keyword="MODELOPT",
                )
            )
        if "TTRM" in selected and "TTRM2" in selected:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-V26135-TTRM-TTRM2-CONFLICT",
                    severity=DiagnosticSeverity.ERROR,
                    message="TTRM and TTRM2 cannot be specified together",
                    pathway=Pathway.CONTROL,
                    keyword="MODELOPT",
                )
            )

        return _deduplicate_diagnostics(diagnostics)


@lru_cache(maxsize=None)
def get_registry(version: AermodVersion | int | str = "26135") -> SchemaRegistry:
    parsed = AermodVersion.parse(version)
    if parsed.code == 26135:
        from .v26135 import build_registry

        return build_registry()
    raise KeyError(f"AERMODKit does not yet ship a schema for AERMOD v{parsed}")


def _deduplicate_diagnostics(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple[str, str, int | None]] = set()
    result: list[Diagnostic] = []
    for diagnostic in diagnostics:
        key = (diagnostic.rule_id, diagnostic.message, diagnostic.line)
        if key not in seen:
            seen.add(key)
            result.append(diagnostic)
    return result
