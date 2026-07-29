"""Public package interface for AERMODKit."""

from ._version import __version__
from .diagnostics import Diagnostic, Severity
from .spec import ModelVersion, VersionMetadata, get_default_version, get_supported_versions

__all__ = [
    "Diagnostic",
    "ModelVersion",
    "Severity",
    "VersionMetadata",
    "__version__",
    "get_default_version",
    "get_supported_versions",
]
