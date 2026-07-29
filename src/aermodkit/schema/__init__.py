"""Versioned AERMOD schema registry."""

from .models import (
    AermodVersion,
    Diagnostic,
    DiagnosticSeverity,
    EvidenceRef,
    KeywordSpec,
    ModelOptionSpec,
    OptionTier,
    ParameterKind,
    ParameterSpec,
    Pathway,
    SourceTypeSpec,
)
from .registry import SchemaRegistry, get_registry

__all__ = [
    "AermodVersion",
    "Diagnostic",
    "DiagnosticSeverity",
    "EvidenceRef",
    "KeywordSpec",
    "ModelOptionSpec",
    "OptionTier",
    "ParameterKind",
    "ParameterSpec",
    "Pathway",
    "SchemaRegistry",
    "SourceTypeSpec",
    "get_registry",
]
