"""AERMODKit public API.

The EPA executable remains the numerical source of truth.  AERMODKit provides
version-aware configuration, lossless runstream parsing, validation, GIS data
preparation, execution orchestration, and result handling around that core.
"""

from .schema.models import AermodVersion, Diagnostic, DiagnosticSeverity
from .schema.registry import SchemaRegistry, get_registry
from .syntax.parser import parse_aermod
from .syntax.writer import write_aermod
from .validation.engine import validate_document

__all__ = [
    "AermodVersion",
    "Diagnostic",
    "DiagnosticSeverity",
    "SchemaRegistry",
    "get_registry",
    "parse_aermod",
    "validate_document",
    "write_aermod",
]

__version__ = "0.1.0a1"
PROJECT_FORMAT_VERSION = "1.0"
