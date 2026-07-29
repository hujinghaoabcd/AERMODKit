#!/usr/bin/env python3
"""Apply reviewed Batch 4 evidence to the four affected v26135 record fragments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION_ROOT = ROOT / "src/aermodkit/spec/versions/v26135"
RESULT_FILE = "reference/probes/v26135/batch4/result.json"
CASE_FILE = "reference/probes/v26135/batch4/case-evidence.csv"
RUN_ID = 30479954822
ARTIFACT_ID = 8735323902


def load(name: str) -> dict[str, Any]:
    return json.loads((VERSION_ROOT / name).read_text(encoding="utf-8"))


def save(name: str, payload: dict[str, Any]) -> None:
    (VERSION_ROOT / name).write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def record(payload: dict[str, Any], keyword: str) -> dict[str, Any]:
    matches = [item for item in payload["records"] if item["keyword"] == keyword]
    if len(matches) != 1:
        raise ValueError(f"expected one {keyword} record, found {len(matches)}")
    return matches[0]


def evidence(cases: list[str], **extra: object) -> dict[str, object]:
    value: dict[str, object] = {
        "result_file": RESULT_FILE,
        "case_evidence_file": CASE_FILE,
        "workflow_run_id": RUN_ID,
        "artifact_id": ARTIFACT_ID,
        "cases": cases,
    }
    value.update(extra)
    return value


def apply_platform() -> None:
    name = "so_geometry_platform_building.json"
    payload = load(name)
    item = record(payload, "PLATFORM")
    item["constraints"] = [
        {"rule": "One PLATFORM record per source; non-point source types are rejected."},
        {"rule": "The record must be processed before source-group cards; the source-definition ordering rule remains active."},
        {"rule": "The official v26135 handler accepts additional numeric payload fields, converts them, and assigns only the first three PLATFORM values. Extra numeric fields are preservation-only and must not become semantic parameters."},
        {"rule": "PLATFORM and PRIME building parameters cannot be applied to the same source."},
    ]
    item["diagnostics"] = [
        {"severity": "error", "code": "198", "condition": "ALPHA absent"},
        {"severity": "error", "code": "208", "condition": "a required or trailing PLATFORM payload field is nonnumeric"},
        {"severity": "error", "code": "631", "condition": "non-point source"},
        {"severity": "error", "code": "632", "condition": "duplicate source PLATFORM"},
        {"severity": "error", "code": "633", "condition": "PLATFORM and PRIME building inputs target the same source"},
    ]
    item["official_behavior_evidence"] = evidence(
        [
            "so_platform_valid_control",
            "so_platform_one_extra_numeric",
            "so_platform_two_extra_numeric",
            "so_platform_one_extra_text",
            "so_platform_duplicate_same_source",
            "so_platform_nonpoint_area",
            "so_platform_prime_conflict",
        ],
        boundary="Executable evidence covers up to two trailing numeric fields. They are accepted but semantically ignored; the syntax layer must preserve them verbatim.",
    )
    item["evidence_status"] = "v26135-source-manual-and-official-executable-verified"
    save(name, payload)


def apply_background() -> None:
    name = "so_chemistry_background.json"
    payload = load(name)
    item = record(payload, "BACKGRND")
    item["constraints"] = [
        {"rule": "Global and sector-specific values follow current sector fallback semantics."},
        {"rule": "Static vector length must exactly match time_flag; HOURLY uses an external file."},
        {"rule": "One non-HOURLY vector is retained per scope/time-flag slot; repeating an already filled slot is rejected with E231."},
        {"rule": "Only one HOURLY background file is accepted per global/sector scope; a second file is rejected with E168 and E501."},
        {"rule": "HOURLY and non-HOURLY records may coexist in either order. Hourly observations are primary and non-HOURLY values substitute missing hourly observations."},
    ]
    item["diagnostics"] = [
        {"severity": "error", "code": "203", "condition": "invalid time flag or sector"},
        {"severity": "error", "code": "231", "condition": "a global or sector static background vector attempts to refill an already populated slot"},
        {"severity": "error", "code": "260", "condition": "wrong number of values"},
        {"severity": "error", "code": "168/501", "condition": "a second HOURLY background file is supplied for the same scope"},
    ]
    item["official_behavior_evidence"] = evidence(
        [
            "so_backgrnd_global_annual_control",
            "so_backgrnd_global_duplicate_same",
            "so_backgrnd_global_duplicate_different",
            "so_backgrnd_sector_annual_control",
            "so_backgrnd_sector_duplicate_same",
            "so_backgrnd_sector_duplicate_different",
            "so_backgrnd_hourly_only_control",
            "so_backgrnd_static_only_control",
            "so_backgrnd_static_then_hourly",
            "so_backgrnd_hourly_then_static",
            "so_backgrnd_hourly_duplicate_different_files",
        ],
        order_comparison={
            "normalized_equal": True,
            "static_then_hourly_sha256": "2cea37d8b70122866e0b20c29b92aa937c2f550a2f909e6709e296f175c40468",
            "hourly_then_static_sha256": "2cea37d8b70122866e0b20c29b92aa937c2f550a2f909e6709e296f175c40468",
        },
        boundary="Order equality removes only case titles, paths, dates, and times; it does not normalize concentration results.",
    )
    item["evidence_status"] = "v26135-source-manual-fixture-and-official-executable-verified"
    save(name, payload)


def apply_grids() -> None:
    name = "re_grids.json"
    payload = load(name)
    for keyword in ("GRIDCART", "GRIDPOLR"):
        item = record(payload, keyword)
        item["constraints"].extend(
            [
                {"rule": "Within an active block, secondary lines accept three lexical forms: keyword and NetID omitted; keyword omitted with NetID repeated; or fully explicit pathway keyword plus NetID. The original lexical form must be preserved."},
                {"rule": "A different NetID inside an active block is rejected with E170 and may cause follow-on incomplete-block diagnostics."},
            ]
        )
        diagnostics = item["diagnostics"]
        existing = [entry for entry in diagnostics if str(entry.get("code")) == "170"]
        if existing:
            existing[0]["condition"] = "secondary line names a different NetID or invalid secondary keyword inside the active block"
        else:
            diagnostics.insert(0, {"severity": "error", "code": "170", "condition": "secondary line names a different NetID or invalid secondary keyword inside the active block"})
        base = f"re_{keyword.lower()}"
        item["official_behavior_evidence"] = evidence(
            [
                f"{base}_keyword_and_id_omitted_control",
                f"{base}_keyword_omitted_id_present",
                f"{base}_full_explicit_control",
                f"{base}_wrong_id_in_active_block",
            ],
            source_rule="A recognized field-3 secondary keyword inherits PNETID; field 3 equal to PNETID shifts the secondary keyword to field 4.",
        )
        item["evidence_status"] = "v26135-source-manual-fixture-and-official-executable-verified"
    save(name, payload)


def apply_discrete() -> None:
    name = "re_discrete_include_finish.json"
    payload = load(name)
    for keyword, prefix in (("DISCCART", "re_disccart"), ("DISCPOLR", "re_discpolr")):
        item = record(payload, keyword)
        first = (
            "Accepted field positions depend on active ELEV/FLAT and FLAGPOLE options."
            if keyword == "DISCCART"
            else "The source ID defines the polar origin; accepted optional positions depend on terrain and flagpole options."
        )
        item["constraints"] = [
            {"rule": first},
            {"rule": "Terrain or flagpole values supplied while their option is inactive are accepted with W229 and ignored semantically, but must remain in the loss-aware syntax representation."},
            {"rule": "When an active conditional option lacks its required positional values, the shared handler emits W228."},
        ]
        item["diagnostics"] = [
            entry for entry in item["diagnostics"] if str(entry.get("code")) != "228/229"
        ] + [
            {"severity": "warning", "code": "228", "condition": "a field required by an active ELEV or FLAGPOLE option is missing"},
            {"severity": "warning", "code": "229", "condition": "terrain or flagpole fields are supplied while the corresponding option is inactive; values are ignored semantically"},
        ]
        cases = [
            "re_disccart_flat_no_flag_control",
            "re_disccart_flat_no_flag_terrain_extra",
            "re_disccart_flat_no_flag_terrain_and_flag_extra",
            "re_disccart_flat_flag_control",
            "re_disccart_flat_flag_terrain_extra",
            "re_disccart_elev_no_flag_control",
            "re_disccart_elev_no_flag_flag_extra",
            "re_disccart_elev_flag_control",
        ] if prefix == "re_disccart" else [
            "re_discpolr_flat_no_flag_control",
            "re_discpolr_flat_no_flag_extra",
            "re_discpolr_flat_flag_control",
            "re_discpolr_flat_flag_terrain_extra",
            "re_discpolr_elev_no_flag_control",
            "re_discpolr_elev_no_flag_extra",
        ]
        item["official_behavior_evidence"] = evidence(
            cases, boundary="W229 means semantically ignored, not syntactically discardable."
        )
        item["evidence_status"] = "v26135-source-manual-fixture-and-official-executable-verified"
    save(name, payload)


def main() -> int:
    apply_platform()
    apply_background()
    apply_grids()
    apply_discrete()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
