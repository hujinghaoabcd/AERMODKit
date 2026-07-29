import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reference/probes/v26135/batch4/manifest.json"
SOURCE_SEARCHES = ROOT / "reference/probes/v26135/batch4/source-searches.json"
FRAGMENTS = [
    ROOT / "reference/probes/v26135/batch4/platform-cases.json",
    ROOT / "reference/probes/v26135/batch4/background-cases.json",
    ROOT / "reference/probes/v26135/batch4/grid-cases.json",
    ROOT / "reference/probes/v26135/batch4/discrete-cases.json",
]

PLATFORM_CASES = {
    "so_platform_valid_control",
    "so_platform_one_extra_numeric",
    "so_platform_two_extra_tokens",
    "so_platform_duplicate_same_source",
    "so_platform_nonpoint_area",
}
BACKGROUND_CASES = {
    "so_backgrnd_global_annual_control",
    "so_backgrnd_global_duplicate_same",
    "so_backgrnd_global_duplicate_different",
    "so_backgrnd_sector_annual_control",
    "so_backgrnd_sector_duplicate_same",
    "so_backgrnd_sector_duplicate_different",
    "so_backgrnd_static_then_hourly",
    "so_backgrnd_hourly_then_static",
    "so_backgrnd_hourly_duplicate_different_files",
}
GRID_CASES = {
    "re_gridcart_keyword_and_id_omitted_control",
    "re_gridcart_keyword_omitted_id_present",
    "re_gridcart_full_explicit_control",
    "re_gridcart_wrong_id_in_active_block",
    "re_gridpolr_keyword_and_id_omitted_control",
    "re_gridpolr_keyword_omitted_id_present",
    "re_gridpolr_full_explicit_control",
    "re_gridpolr_wrong_id_in_active_block",
}
DISCRETE_CASES = {
    "re_disccart_flat_no_flag_control",
    "re_disccart_flat_no_flag_terrain_extra",
    "re_disccart_flat_no_flag_terrain_and_flag_extra",
    "re_disccart_flat_flag_control",
    "re_disccart_flat_flag_terrain_extra",
    "re_disccart_elev_no_flag_control",
    "re_disccart_elev_no_flag_flag_extra",
    "re_disccart_elev_flag_control",
}


def _manifest() -> dict[str, object]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cases = list(payload.get("cases", []))
    for fragment in FRAGMENTS:
        cases.extend(json.loads(fragment.read_text(encoding="utf-8"))["cases"])
    payload["cases"] = cases
    return payload


def test_batch4_manifest_has_expected_unique_cases() -> None:
    cases = _manifest()["cases"]
    assert isinstance(cases, list)
    identifiers = [str(case["id"]) for case in cases]
    expected = PLATFORM_CASES | BACKGROUND_CASES | GRID_CASES | DISCRETE_CASES
    assert set(identifiers) == expected
    assert len(identifiers) == len(set(identifiers)) == 30


def test_batch4_controls_and_observation_targets_are_explicit() -> None:
    cases = _manifest()["cases"]
    assert isinstance(cases, list)
    accepted = {
        str(case["id"])
        for case in cases
        if case["expected_outcome"] == "accepted"
    }
    assert accepted == {
        "so_platform_valid_control",
        "so_backgrnd_global_annual_control",
        "so_backgrnd_sector_annual_control",
        "re_gridcart_keyword_and_id_omitted_control",
        "re_gridcart_keyword_omitted_id_present",
        "re_gridcart_full_explicit_control",
        "re_gridpolr_keyword_and_id_omitted_control",
        "re_gridpolr_keyword_omitted_id_present",
        "re_gridpolr_full_explicit_control",
        "re_disccart_flat_no_flag_control",
        "re_disccart_flat_flag_control",
        "re_disccart_elev_no_flag_control",
        "re_disccart_elev_flag_control",
    }
    assert all(case["expected_outcome"] in {"accepted", "observe"} for case in cases)
    assert all(str(case["question"]).endswith("?") for case in cases)


def test_background_hourly_duplicate_uses_isolated_support_copy() -> None:
    cases = {str(case["id"]): case for case in _manifest()["cases"]}
    target = cases["so_backgrnd_hourly_duplicate_different_files"]
    assert target["support_copies"] == [
        {"source": "BG1.dat", "destination": "BG2.dat"}
    ]


def test_grid_variants_cover_implicit_partial_and_explicit_forms() -> None:
    cases = {str(case["id"]): case for case in _manifest()["cases"]}
    cart_lines = {
        str(item["replacement"])
        for identifier in (
            "re_gridcart_keyword_and_id_omitted_control",
            "re_gridcart_keyword_omitted_id_present",
            "re_gridcart_full_explicit_control",
        )
        for item in cases[identifier]["replace_line_once"]
        if "XYINC" in str(item["replacement"])
    }
    assert any(line.lstrip().startswith("XYINC") for line in cart_lines)
    assert any(line.lstrip().startswith("CAR1 XYINC") for line in cart_lines)
    assert any(line.lstrip().startswith("GRIDCART CAR1 XYINC") for line in cart_lines)


def test_batch4_source_searches_cover_handlers_and_diagnostics() -> None:
    payload = json.loads(SOURCE_SEARCHES.read_text(encoding="utf-8"))
    identifiers = {str(item["id"]) for item in payload["searches"]}
    assert identifiers == {
        "platform-handler",
        "platform-nonpoint-e631",
        "platform-duplicate-e632",
        "background-handler",
        "background-sector-handler",
        "background-value-count-e260",
        "gridcart-handler",
        "gridpolr-handler",
        "disccart-handler",
        "discpolr-handler",
        "discrete-conditional-w228",
        "discrete-conditional-w229",
    }


def test_official_executable_hash_matches_retained_evidence() -> None:
    assets = _manifest()["official_assets"]
    assert isinstance(assets, dict)
    assert assets["executable_sha256"] == (
        "599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da"
    )
    assert assets["fixture_artifact_id"] == 8701857473
