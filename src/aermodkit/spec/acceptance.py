"""Deterministic whole-spec acceptance for one AERMOD release."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any, cast

from .pathway import load_pathway_specification

_PATHWAY_REPORTS: tuple[tuple[str, str, int], ...] = (
    ("CO", "v26135-co-source-exact-match.json", 39),
    ("SO", "v26135-so-source-exact-match.json", 40),
    ("RE", "v26135-re-source-exact-match.json", 9),
    ("ME", "v26135-me-source-exact-match.json", 23),
    ("EV", "v26135-ev-source-exact-match.json", 5),
    ("OU", "v26135-ou-source-exact-match.json", 18),
)
_EVENT_REPORT = ("OU/EVENT", "v26135-event-output-source-exact-match.json", 4)
_PROBE_CATALOGS: tuple[tuple[str, str], ...] = (
    ("CO", "v26135-co-official-behavior-probes.json"),
    ("SO/RE", "v26135-so-re-official-behavior-probes.json"),
    ("ME/EV/OU", "v26135-me-ev-ou-official-behavior-probes.json"),
)
_REQUIRED_PRESERVATION = frozenset(
    {"original_text", "comments", "case", "unknown_fields"}
)


@dataclass(frozen=True, slots=True)
class PathwayAcceptance:
    """Acceptance result for one executable dispatcher."""

    pathway: str
    expected_count: int
    source_count: int
    bundled_count: int
    exact_set_match: bool
    framing_valid: bool
    syntax_present: bool
    preservation_policy_present: bool
    source_report: str

    @property
    def accepted(self) -> bool:
        """Return whether the dispatcher passes the record-level gate."""

        return (
            self.source_count == self.expected_count
            and self.bundled_count == self.expected_count
            and self.exact_set_match
            and self.framing_valid
            and self.syntax_present
            and self.preservation_policy_present
        )


@dataclass(frozen=True, slots=True)
class ProbeSummary:
    """Normalized state of the retained official-executable probe catalog."""

    total: int
    executed: int
    source_resolved: int
    official_executable_pending: int
    entries: tuple[Mapping[str, object], ...]

    @property
    def complete(self) -> bool:
        """Return whether every retained probe has a final result."""

        return self.official_executable_pending == 0


@dataclass(frozen=True, slots=True)
class WholeSpecAcceptance:
    """Deterministic acceptance report for the complete v26135 dispatcher surface."""

    schema_version: int
    model_version: str
    acceptance_scope: str
    pathways: tuple[PathwayAcceptance, ...]
    probes: ProbeSummary

    @property
    def record_set_gate_passed(self) -> bool:
        """Return whether all dispatcher record sets pass acceptance."""

        return all(item.accepted for item in self.pathways)

    @property
    def behavior_probe_gate_passed(self) -> bool:
        """Return whether all retained behavior probes have final evidence."""

        return self.probes.complete

    @property
    def syntax_implementation_ready(self) -> bool:
        """Return whether all gates preceding the production syntax layer are complete."""

        return self.record_set_gate_passed and self.behavior_probe_gate_passed

    def to_dict(self) -> dict[str, object]:
        """Return a stable JSON-serializable representation."""

        pathway_rows = []
        for pathway in self.pathways:
            row = asdict(pathway)
            row["accepted"] = pathway.accepted
            pathway_rows.append(row)
        probe_data: dict[str, object] = {
            "total": self.probes.total,
            "executed": self.probes.executed,
            "source_resolved": self.probes.source_resolved,
            "official_executable_pending": self.probes.official_executable_pending,
            "entries": [dict(entry) for entry in self.probes.entries],
            "complete": self.probes.complete,
        }
        return {
            "schema_version": self.schema_version,
            "model_version": self.model_version,
            "acceptance_scope": self.acceptance_scope,
            "record_set_gate_passed": self.record_set_gate_passed,
            "behavior_probe_gate_passed": self.behavior_probe_gate_passed,
            "syntax_implementation_ready": self.syntax_implementation_ready,
            "totals": {
                "dispatcher_count": len(self.pathways),
                "primary_record_count": sum(item.bundled_count for item in self.pathways),
                "accepted_dispatchers": sum(item.accepted for item in self.pathways),
            },
            "pathways": pathway_rows,
            "behavior_probes": probe_data,
        }


def _object(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{context} must be an object with string keys")
    return cast(dict[str, Any], value)


def _string_list(value: object, *, context: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{context} must be a string array")
    return cast(list[str], value)


def _integer(payload: Mapping[str, object], names: Sequence[str], *, context: str) -> int:
    for name in names:
        value = payload.get(name)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    raise ValueError(f"{context} has no integer field among {tuple(names)!r}")


def _exact_match(payload: Mapping[str, object]) -> bool:
    explicit = payload.get("exact_set_match", payload.get("exact_match"))
    if isinstance(explicit, bool):
        return explicit
    missing = _string_list(payload.get("missing", []), context="missing")
    extra = _string_list(payload.get("extra", []), context="extra")
    return not missing and not extra


def _event_output() -> tuple[tuple[str, ...], Mapping[str, object], tuple[tuple[str, ...], ...]]:
    resource = files("aermodkit.spec.versions").joinpath("v26135/event_output_mode.json")
    payload = _object(json.loads(resource.read_text(encoding="utf-8")), context="event output")
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("event output records must be a non-empty array")
    keywords: list[str] = []
    syntax: list[tuple[str, ...]] = []
    for index, item in enumerate(records):
        record = _object(item, context=f"event output records[{index}]")
        keyword = record.get("keyword")
        if not isinstance(keyword, str):
            raise ValueError(f"event output records[{index}].keyword must be a string")
        keywords.append(keyword)
        syntax.append(
            tuple(
                _string_list(
                    record.get("syntax"), context=f"event output {keyword}.syntax"
                )
            )
        )
    preservation = _object(payload.get("preservation_policy"), context="event output preservation")
    return tuple(keywords), preservation, tuple(syntax)


def _normalize_probe(scope: str, raw: object) -> Mapping[str, object]:
    probe = _object(raw, context=f"{scope} probe")
    probe_id = probe.get("id")
    if not isinstance(probe_id, str) or not probe_id:
        raise ValueError(f"{scope} probe id must be a non-empty string")
    raw_status = probe.get("status")
    status = raw_status if isinstance(raw_status, str) else "cataloged-not-executed"
    if status == "source-resolved":
        classification = "source-resolved"
    elif status.startswith("executed-"):
        classification = "executed"
    else:
        classification = "official-executable-pending"
    normalized: dict[str, object] = {
        "scope": scope,
        "id": probe_id,
        "status": status,
        "classification": classification,
    }
    for key in ("target", "question", "priority", "records"):
        if key in probe:
            normalized[key] = probe[key]
    return normalized


def _load_probes(reference_root: Path) -> ProbeSummary:
    entries: list[Mapping[str, object]] = []
    for scope, filename in _PROBE_CATALOGS:
        payload = _object(
            json.loads((reference_root / filename).read_text(encoding="utf-8")),
            context=filename,
        )
        raw_probes = payload.get("probes")
        if not isinstance(raw_probes, list):
            raise ValueError(f"{filename}.probes must be an array")
        entries.extend(_normalize_probe(scope, item) for item in raw_probes)
    classifications = [str(item["classification"]) for item in entries]
    return ProbeSummary(
        total=len(entries),
        executed=classifications.count("executed"),
        source_resolved=classifications.count("source-resolved"),
        official_executable_pending=classifications.count("official-executable-pending"),
        entries=tuple(entries),
    )


def evaluate_v26135_whole_spec(reference_root: Path) -> WholeSpecAcceptance:
    """Evaluate the complete v26135 record-level specification and probe gates."""

    reference_root = reference_root.resolve()
    pathways: list[PathwayAcceptance] = []
    for pathway, filename, expected_count in _PATHWAY_REPORTS:
        report = _object(
            json.loads((reference_root / filename).read_text(encoding="utf-8")),
            context=filename,
        )
        specification = load_pathway_specification(pathway, "26135")
        source_count = _integer(
            report, ("source_dispatch_count", "source_count"), context=filename
        )
        bundled_count = _integer(
            report, ("schema_count", "bundled_count"), context=filename
        )
        report_keywords = report.get("bundled_primary_keywords", report.get("bundled_keywords"))
        report_order_matches = True
        if report_keywords is not None:
            report_order_matches = tuple(
                _string_list(report_keywords, context=f"{filename}.bundled keywords")
            ) == specification.keywords
        preservation_keys = {
            key for key, value in specification.preservation_policy.items() if value is True
        }
        pathways.append(
            PathwayAcceptance(
                pathway=pathway,
                expected_count=expected_count,
                source_count=source_count,
                bundled_count=bundled_count,
                exact_set_match=_exact_match(report) and report_order_matches,
                framing_valid=(
                    specification.keywords.count("STARTING") == 1
                    and specification.keywords.count("FINISHED") == 1
                ),
                syntax_present=all(record.syntax for record in specification.records),
                preservation_policy_present=_REQUIRED_PRESERVATION <= preservation_keys,
                source_report=filename,
            )
        )

    event_pathway, event_filename, event_expected_count = _EVENT_REPORT
    event_report = _object(
        json.loads((reference_root / event_filename).read_text(encoding="utf-8")),
        context=event_filename,
    )
    event_keywords, event_preservation, event_syntax = _event_output()
    report_event_keywords = tuple(
        _string_list(
            event_report.get("bundled_keywords"),
            context=f"{event_filename}.bundled_keywords",
        )
    )
    event_preservation_keys = {
        key for key, value in event_preservation.items() if value is True
    }
    pathways.append(
        PathwayAcceptance(
            pathway=event_pathway,
            expected_count=event_expected_count,
            source_count=_integer(event_report, ("source_count",), context=event_filename),
            bundled_count=_integer(event_report, ("bundled_count",), context=event_filename),
            exact_set_match=_exact_match(event_report) and report_event_keywords == event_keywords,
            framing_valid=(
                event_keywords.count("STARTING") == 1
                and event_keywords.count("FINISHED") == 1
            ),
            syntax_present=all(event_syntax),
            preservation_policy_present=_REQUIRED_PRESERVATION <= event_preservation_keys,
            source_report=event_filename,
        )
    )
    return WholeSpecAcceptance(
        schema_version=1,
        model_version="26135",
        acceptance_scope="source-dispatched primary record-level specification",
        pathways=tuple(pathways),
        probes=_load_probes(reference_root),
    )
