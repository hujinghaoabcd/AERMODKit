"""Cross-keyword and cross-pathway v26135 rules."""

from __future__ import annotations

from aermodkit.schema.models import Diagnostic, DiagnosticSeverity, Pathway
from aermodkit.syntax.ast import AermodDocument


def validate_cross_pathway_rules(
    document: AermodDocument,
    options: set[str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    co = _present(document, Pathway.CONTROL)
    so = _present(document, Pathway.SOURCE)
    re = _present(document, Pathway.RECEPTOR)
    me = _present(document, Pathway.METEOROLOGY)
    ou = _present(document, Pathway.OUTPUT)

    if "HALFLIFE" in co and "DCAYCOEF" in co:
        diagnostics.append(
            Diagnostic(
                rule_id="AERMODKIT-V26135-DECAY-ALTERNATIVES",
                severity=DiagnosticSeverity.WARNING,
                message="HALFLIFE and DCAYCOEF are alternatives; AERMOD uses only the first",
                pathway=Pathway.CONTROL,
                keyword="HALFLIFE",
            )
        )
    if "HBP" in options and "HBPSRCID" not in so:
        diagnostics.append(_missing("HBP requires SO HBPSRCID", Pathway.SOURCE, "HBPSRCID"))
    if "ARCFTOPT" in co and "ARCFTSRC" not in so:
        diagnostics.append(
            _missing("CO ARCFTOPT requires SO ARCFTSRC", Pathway.SOURCE, "ARCFTSRC")
        )
    if "PSDCREDIT" in options and "PSDGROUP" not in so:
        diagnostics.append(
            _missing("PSDCREDIT requires SO PSDGROUP", Pathway.SOURCE, "PSDGROUP")
        )
    if document.pathways(Pathway.SOURCE):
        if "PSDCREDIT" not in options and "SRCGROUP" not in so:
            diagnostics.append(
                _missing(
                    "SO requires SRCGROUP unless PSDCREDIT uses PSDGROUP",
                    Pathway.SOURCE,
                    "SRCGROUP",
                )
            )
        if "PSDCREDIT" in options and "SRCGROUP" in so:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-V26135-PSDCREDIT-GROUP",
                    severity=DiagnosticSeverity.ERROR,
                    message="PSDCREDIT uses PSDGROUP instead of SRCGROUP",
                    pathway=Pathway.SOURCE,
                    keyword="SRCGROUP",
                )
            )
    if "SCIM" in options:
        if "SCIMBYHR" not in me:
            diagnostics.append(
                _missing(
                    "MODELOPT SCIM requires ME SCIMBYHR",
                    Pathway.METEOROLOGY,
                    "SCIMBYHR",
                )
            )
        periods = {
            argument.upper()
            for statement in document.statements(Pathway.CONTROL, "AVERTIME")
            for argument in statement.arguments
        }
        if "ANNUAL" not in periods:
            diagnostics.append(
                Diagnostic(
                    rule_id="AERMODKIT-V26135-SCIM-ANNUAL",
                    severity=DiagnosticSeverity.ERROR,
                    message="MODELOPT SCIM requires ANNUAL in AVERTIME",
                    pathway=Pathway.CONTROL,
                    keyword="AVERTIME",
                )
            )
    if document.pathways(Pathway.RECEPTOR) and not (
        re & {"GRIDCART", "GRIDPOLR", "DISCCART", "DISCPOLR", "EVALCART", "INCLUDED"}
    ):
        diagnostics.append(
            Diagnostic(
                rule_id="AERMODKIT-V26135-RECEPTOR-MISSING",
                severity=DiagnosticSeverity.ERROR,
                message="RE requires a receptor network, discrete/evaluation receptor, or INCLUDED",
                pathway=Pathway.RECEPTOR,
            )
        )
    if "RANKFILE" in ou and "MAXTABLE" not in ou:
        diagnostics.append(
            _missing("OU RANKFILE requires OU MAXTABLE", Pathway.OUTPUT, "MAXTABLE")
        )
    return diagnostics


def _missing(message: str, pathway: Pathway, keyword: str) -> Diagnostic:
    return Diagnostic(
        rule_id="AERMODKIT-V26135-CROSS-PATHWAY-DEPENDENCY",
        severity=DiagnosticSeverity.ERROR,
        message=message,
        pathway=pathway,
        keyword=keyword,
    )


def _present(document: AermodDocument, pathway: Pathway) -> set[str]:
    return {statement.keyword for statement in document.statements(pathway)}
