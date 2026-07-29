"""Load versioned, source-verified pathway specifications."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.resources import files
from types import MappingProxyType
from typing import Any, cast

from .model_version import ModelVersion
from .registry import get_default_version


@dataclass(frozen=True, slots=True)
class RecordSpecification:
    """One keyword record from a versioned pathway specification."""

    keyword: str
    required: bool
    repeatability: str
    syntax: tuple[str, ...]
    evidence_status: str
    source: Mapping[str, object]
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class PathwaySpecification:
    """A validated partial or complete specification for one AERMOD pathway."""

    schema_version: int
    model_version: ModelVersion
    pathway: str
    batch: int
    status: str
    records: tuple[RecordSpecification, ...]
    preservation_policy: Mapping[str, object]

    @property
    def keywords(self) -> tuple[str, ...]:
        """Return keyword names in the source specification order."""

        return tuple(record.keyword for record in self.records)

    def get_record(self, keyword: str) -> RecordSpecification:
        """Return a record by keyword, or raise ``LookupError``."""

        normalized = keyword.strip().upper()
        for record in self.records:
            if record.keyword == normalized:
                return record
        raise LookupError(f"keyword {normalized!r} is not in the {self.pathway} specification")


def _mapping(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise ValueError(f"{context} keys must be strings")
    return cast(dict[str, Any], value)


def _string(value: object, *, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} must be a non-empty string")
    return value


def _integer(value: object, *, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{context} must be an integer")
    return value


def _boolean(value: object, *, context: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{context} must be a boolean")
    return value


def _string_tuple(value: object, *, context: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{context} must be a non-empty string array")
    return tuple(_string(item, context=f"{context}[]") for item in value)


def _parse_record(value: object, *, index: int) -> RecordSpecification:
    raw = _mapping(value, context=f"records[{index}]")
    keyword = _string(raw.get("keyword"), context=f"records[{index}].keyword").upper()
    if keyword != raw["keyword"]:
        raise ValueError(f"records[{index}].keyword must be uppercase")
    source = _mapping(raw.get("source"), context=f"records[{index}].source")
    return RecordSpecification(
        keyword=keyword,
        required=_boolean(raw.get("required"), context=f"records[{index}].required"),
        repeatability=_string(
            raw.get("repeatability"), context=f"records[{index}].repeatability"
        ),
        syntax=_string_tuple(raw.get("syntax"), context=f"records[{index}].syntax"),
        evidence_status=_string(
            raw.get("evidence_status"), context=f"records[{index}].evidence_status"
        ),
        source=MappingProxyType(source),
        data=MappingProxyType(raw),
    )


def load_pathway_specification(
    pathway: str,
    version: str | ModelVersion | None = None,
) -> PathwaySpecification:
    """Load and validate a bundled pathway specification.

    The current v26135 CO file is explicitly partial. Loading it means that the
    included records are source-verified; it does not imply that all CO records or
    the complete AERMOD runstream are implemented.
    """

    resolved = get_default_version() if version is None else ModelVersion.parse(version)
    normalized_pathway = pathway.strip().upper()
    if not normalized_pathway or not normalized_pathway.isalnum():
        raise ValueError("pathway must be a non-empty alphanumeric identifier")

    version_root = files("aermodkit.spec.versions").joinpath(f"v{resolved.code}")
    resource = version_root.joinpath(f"{normalized_pathway.lower()}_pathway.json")
    if not resource.is_file():
        raise LookupError(
            f"no bundled {normalized_pathway} pathway specification for AERMOD {resolved}"
        )

    payload = _mapping(json.loads(resource.read_text(encoding="utf-8")), context="root")
    payload_version = ModelVersion(_string(payload.get("model_version"), context="model_version"))
    if payload_version != resolved:
        raise ValueError(
            f"pathway specification version {payload_version} does not match requested {resolved}"
        )
    payload_pathway = _string(payload.get("pathway"), context="pathway").upper()
    if payload_pathway != normalized_pathway:
        raise ValueError(
            f"pathway specification {payload_pathway!r} does not match requested "
            f"{normalized_pathway!r}"
        )

    batch = _integer(payload.get("batch"), context="batch")
    record_files = _string_tuple(payload.get("record_files"), context="record_files")
    raw_records: list[object] = []
    for record_filename in record_files:
        if "/" in record_filename or "\\" in record_filename:
            raise ValueError("record_files entries must be basenames")
        fragment_resource = version_root.joinpath(record_filename)
        if not fragment_resource.is_file():
            raise ValueError(f"missing pathway record fragment: {record_filename}")
        fragment = _mapping(
            json.loads(fragment_resource.read_text(encoding="utf-8")),
            context=record_filename,
        )
        fragment_version = _string(
            fragment.get("model_version"), context=f"{record_filename}.model_version"
        )
        fragment_pathway = _string(
            fragment.get("pathway"), context=f"{record_filename}.pathway"
        ).upper()
        fragment_batch = _integer(
            fragment.get("batch"), context=f"{record_filename}.batch"
        )
        if fragment_version != resolved.code:
            raise ValueError(f"{record_filename} has the wrong model version")
        if fragment_pathway != normalized_pathway:
            raise ValueError(f"{record_filename} has the wrong pathway")
        if fragment_batch < 1 or fragment_batch > batch:
            raise ValueError(
                f"{record_filename} batch {fragment_batch} is not valid for aggregate batch {batch}"
            )
        fragment_records = fragment.get("records")
        if not isinstance(fragment_records, list) or not fragment_records:
            raise ValueError(f"{record_filename}.records must be a non-empty array")
        raw_records.extend(fragment_records)

    records = tuple(_parse_record(item, index=index) for index, item in enumerate(raw_records))
    keywords = tuple(record.keyword for record in records)
    if len(set(keywords)) != len(keywords):
        raise ValueError("pathway specification contains duplicate keywords")

    scope = _mapping(payload.get("scope"), context="scope")
    included = _string_tuple(scope.get("included_keywords"), context="scope.included_keywords")
    if included != keywords:
        raise ValueError("scope.included_keywords must exactly match records order")

    preservation = _mapping(payload.get("preservation_policy"), context="preservation_policy")
    return PathwaySpecification(
        schema_version=_integer(payload.get("schema_version"), context="schema_version"),
        model_version=resolved,
        pathway=normalized_pathway,
        batch=batch,
        status=_string(payload.get("status"), context="status"),
        records=records,
        preservation_policy=MappingProxyType(preservation),
    )
