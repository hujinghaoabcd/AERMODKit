"""AERMODKit public API."""

from .schema.models import AermodVersion, Diagnostic, DiagnosticSeverity
from .schema.registry import SchemaRegistry, get_registry
from .semantic.project import AermodProjectModel, SourceRecord, build_project_model
from .syntax.parser import parse_aermod
from .syntax.writer import write_aermod
from .validation.engine import validate_document

__all__ = [
    "AermodProjectModel",
    "AermodVersion",
    "Diagnostic",
    "DiagnosticSeverity",
    "SchemaRegistry",
    "SourceRecord",
    "build_project_model",
    "get_registry",
    "parse_aermod",
    "validate_document",
    "write_aermod",
]

__version__ = "0.1.0a2"
PROJECT_FORMAT_VERSION = "1.0"
