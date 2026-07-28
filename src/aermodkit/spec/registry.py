"""Load version metadata bundled with AERMODKit.

This registry is deliberately small. It is the seed of a future versioned schema layer,
not a claim that the v26135 keyword specification is already complete.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from typing import Final

from .model_version import ModelVersion

_DEFAULT_VERSION: Final = ModelVersion("26135")


@dataclass(frozen=True, slots=True)
class VersionMetadata:
    """Traceable metadata for one supported EPA release."""

    version: ModelVersion
    release_date: date
    authority: str
    status: str
    schema_completeness: str
    notes: tuple[str, ...]


def get_default_version() -> ModelVersion:
    """Return the default modelling release used for new projects."""

    return _DEFAULT_VERSION


def get_supported_versions() -> tuple[ModelVersion, ...]:
    """Return versions with bundled metadata, sorted oldest to newest."""

    root = files("aermodkit.spec.versions")
    versions: list[ModelVersion] = []
    for child in root.iterdir():
        if child.is_dir() and child.name.startswith("v"):
            try:
                versions.append(ModelVersion(child.name))
            except ValueError:
                continue
    return tuple(sorted(versions))


def load_metadata(version: str | ModelVersion | None = None) -> VersionMetadata:
    """Load bundled metadata for a model version.

    Raises
    ------
    LookupError
        If AERMODKit has no metadata bundle for the requested version.
    """

    resolved = _DEFAULT_VERSION if version is None else ModelVersion.parse(version)
    resource = files("aermodkit.spec.versions").joinpath(f"v{resolved.code}", "metadata.json")
    if not resource.is_file():
        raise LookupError(f"unsupported AERMOD metadata version: {resolved}")

    payload = json.loads(resource.read_text(encoding="utf-8"))
    return VersionMetadata(
        version=resolved,
        release_date=date.fromisoformat(payload["release_date"]),
        authority=str(payload["authority"]),
        status=str(payload["status"]),
        schema_completeness=str(payload["schema_completeness"]),
        notes=tuple(str(item) for item in payload.get("notes", [])),
    )
