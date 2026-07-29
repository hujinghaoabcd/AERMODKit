"""Schema data structures shared by all AERMOD versions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass(frozen=True, order=True, slots=True)
class AermodVersion:
    """A five-digit AERMOD version code such as ``26135``."""

    code: int

    def __post_init__(self) -> None:
        if self.code < 10000 or self.code > 99999:
            raise ValueError(f"AERMOD version must be a five-digit code, got {self.code!r}")

    @classmethod
    def parse(cls, value: AermodVersion | int | str) -> AermodVersion:
        if isinstance(value, cls):
            return value
        text = str(value).strip().lower().removeprefix("v")
        if not text.isdigit() or len(text) != 5:
            raise ValueError(f"invalid AERMOD version {value!r}; expected e.g. '26135'")
        return cls(int(text))

    def __str__(self) -> str:
        return f"{self.code:05d}"


class Pathway(str, Enum):
    CONTROL = "CO"
    SOURCE = "SO"
    RECEPTOR = "RE"
    METEOROLOGY = "ME"
    EVENT = "EV"
    OUTPUT = "OU"

    @classmethod
    def parse(cls, value: Pathway | str) -> Pathway:
        if isinstance(value, cls):
            return value
        return cls(str(value).strip().upper())


class ParameterKind(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    ENUM = "enum"
    PATH = "path"
    TOKEN = "token"


class OptionTier(str, Enum):
    """Program status, not a substitute for jurisdiction-specific approval."""

    CONTROL_FLAG = "control-flag"
    REGULATORY = "regulatory"
    ALPHA = "alpha"
    BETA = "beta"
    NON_REGULATORY = "non-regulatory"
    PROCESSING = "processing"


class DiagnosticSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    identifier: str
    title: str
    url: str
    pages: tuple[int, ...] = ()
    note: str | None = None


@dataclass(frozen=True, slots=True)
class ParameterSpec:
    name: str
    kind: ParameterKind = ParameterKind.TOKEN
    required: bool = True
    units: str | None = None
    choices: tuple[str, ...] = ()
    description: str = ""


@dataclass(frozen=True, slots=True)
class KeywordSpec:
    pathway: Pathway
    name: str
    parameters: tuple[ParameterSpec, ...] = ()
    min_args: int = 0
    max_args: int | None = 0
    repeatable: bool = False
    mandatory: bool = False
    order: int = 1000
    evidence: tuple[EvidenceRef, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.name.upper())
        if self.min_args < 0:
            raise ValueError("min_args cannot be negative")
        if self.max_args is not None and self.max_args < self.min_args:
            raise ValueError("max_args cannot be smaller than min_args")


@dataclass(frozen=True, slots=True)
class ModelOptionSpec:
    name: str
    tier: OptionTier
    order: int
    allowed_with_dfault: bool | None = None
    requires_all: frozenset[str] = frozenset()
    requires_any: frozenset[str] = frozenset()
    conflicts: frozenset[str] = frozenset()
    applicable_source_types: frozenset[str] = frozenset()
    description: str = ""
    evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.name.upper())
        object.__setattr__(self, "requires_all", _upper_set(self.requires_all))
        object.__setattr__(self, "requires_any", _upper_set(self.requires_any))
        object.__setattr__(self, "conflicts", _upper_set(self.conflicts))
        object.__setattr__(
            self,
            "applicable_source_types",
            _upper_set(self.applicable_source_types),
        )


@dataclass(frozen=True, slots=True)
class SourceTypeSpec:
    name: str
    location_required: tuple[ParameterSpec, ...]
    location_optional: tuple[ParameterSpec, ...] = ()
    srcparam_required: tuple[ParameterSpec, ...] = ()
    srcparam_optional: tuple[ParameterSpec, ...] = ()
    required_options: frozenset[str] = frozenset()
    regulatory_default_compatible: bool | None = None
    description: str = ""
    evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.name.upper())
        object.__setattr__(self, "required_options", _upper_set(self.required_options))

    @property
    def location_min_args(self) -> int:
        return 2 + len(self.location_required)

    @property
    def location_max_args(self) -> int:
        return self.location_min_args + len(self.location_optional)

    @property
    def srcparam_min_args(self) -> int:
        return 1 + len(self.srcparam_required)

    @property
    def srcparam_max_args(self) -> int:
        return self.srcparam_min_args + len(self.srcparam_optional)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    rule_id: str
    severity: DiagnosticSeverity
    message: str
    pathway: Pathway | None = None
    keyword: str | None = None
    line: int | None = None
    source_id: str | None = None
    evidence: tuple[EvidenceRef, ...] = ()
    context: dict[str, Any] = field(default_factory=dict)


def _upper_set(values: frozenset[str] | set[str]) -> frozenset[str]:
    return frozenset(str(value).upper() for value in values)
