"""Structured diagnostics shared by parsers, validators, runners, and user interfaces."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    """Diagnostic severity in increasing order of consequence."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A machine-readable problem or advisory tied to model context.

    The shape is UI-agnostic. Future GIS applications can use ``geometry_ref`` to
    select a map feature, while CLI and web clients can render the same object.
    """

    code: str
    severity: Severity
    message: str
    processor: str | None = None
    pathway: str | None = None
    object_type: str | None = None
    object_id: str | None = None
    field: str | None = None
    documentation_reference: str | None = None
    source_code_reference: str | None = None
    geometry_ref: str | None = None
    suggested_fix: str | None = None
    context: Mapping[str, Any] | None = None

    @property
    def blocks_execution(self) -> bool:
        """Return whether the diagnostic should prevent deterministic execution."""

        return self.severity in {Severity.ERROR, Severity.FATAL}
