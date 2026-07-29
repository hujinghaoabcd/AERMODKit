import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reference/probes/v26135/batch3/manifest.json"
SOURCE_SEARCHES = ROOT / "reference/probes/v26135/batch3/source-searches.json"
AIRCRAFT_HOURLY = ROOT / "reference/probes/v26135/batch3/aircraft_hourly.dat"

DEPENDENCY_RECORDS = {
    "gdseason",
    "gasdepdf",
    "gdlanuse",
    "gasdepvd",
    "low_wind",
    "awmadwnw",
    "ord_dwnw",
}
AIRCRAFT_CASES = {
    "co_arcft_valid_control",
    "co_arcftopt_no_payload",
    "co_arcftopt_repeated_same",
    "co_arcftopt_repeated_different",
    "co_arcftopt_extra_fields",
    "co_arcft_no_alpha",
    "co_arcft_dfault_alpha",
    "co_arcft_missing_arcftsrc",
    "co_arcft_missing_houremis",
    "co_arcftsrc_without_arcftopt",
}
MAXDCONT_CASES = {
    "ou_maxdcont_secondary_rank_control",
    "ou_maxdcont_secondary_rank_unit",
    "ou_maxdcont_thresh_control",
    "ou_maxdcont_thresh_unit",
}


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_batch3_manifest_has_expected_unique_cases() -> None:
    payload = _manifest()
    cases = payload["cases"]
    assert isinstance(cases, list)
    identifiers = [str(case["id"]) for case in cases]

    dependency_ids = {
        f"co_{record}_{suffix}"
        for record in DEPENDENCY_RECORDS
        for suffix in ("alpha_control", "no_alpha", "dfault_alpha")
    }
    assert set(identifiers) == dependency_ids | AIRCRAFT_CASES | MAXDCONT_CASES
    assert len(identifiers) == len(set(identifiers)) == 35


def test_batch3_controls_and_observation_targets_are_explicit() -> None:
    cases = _manifest()["cases"]
    controls = {
        str(case["id"])
        for case in cases
        if case["expected_outcome"] == "accepted"
    }
    expected_controls = {
        f"co_{record}_alpha_control" for record in DEPENDENCY_RECORDS
    } | {
        "co_arcft_valid_control",
        "ou_maxdcont_secondary_rank_control",
        "ou_maxdcont_thresh_control",
    }
    assert controls == expected_controls
    assert all(case["expected_outcome"] in {"accepted", "observe"} for case in cases)
    assert all(str(case["question"]).endswith("?") for case in cases)


def test_aircraft_cases_use_ordered_hourly_and_aircraft_cards() -> None:
    cases = {str(case["id"]): case for case in _manifest()["cases"]}
    ordered_cases = AIRCRAFT_CASES - {
        "co_arcft_missing_arcftsrc",
        "co_arcft_missing_houremis",
        "co_arcftsrc_without_arcftopt",
    }
    for identifier in ordered_cases:
        replacements = [
            str(item["replacement"])
            for item in cases[identifier]["replace_line_once"]
        ]
        hourly_index = replacements.index("   HOUREMIS aircraft_hourly.dat AREA")
        source_index = replacements.index("   ARCFTSRC AREA")
        assert hourly_index < source_index


def test_aircraft_hourly_support_file_is_frozen() -> None:
    lines = AIRCRAFT_HOURLY.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 6
    assert all(line.startswith("SO HOUREMIS 90 01 01") for line in lines)
    assert all(" AREA " in line for line in lines)


def test_maxdcont_filenames_fit_the_official_field_limit() -> None:
    cases = {
        str(case["id"]): case
        for case in _manifest()["cases"]
        if str(case["id"]).startswith("ou_maxdcont")
    }
    for case in cases.values():
        replacement = str(case["replace_line_once"][-1]["replacement"])
        filename = next(token for token in replacement.split() if token.startswith("../Outputs/"))
        assert len(filename) < 40


def test_batch3_source_searches_cover_target_diagnostics() -> None:
    payload = json.loads(SOURCE_SEARCHES.read_text(encoding="utf-8"))
    identifiers = {str(item["id"]) for item in payload["searches"]}
    assert identifiers == {
        "dfault-conflict-e196",
        "alpha-required-e198",
        "alpha-required-e133",
        "aircraft-dfault-e204",
        "aircraft-arcftopt-missing-e821",
        "aircraft-hourly-missing-e823",
        "arcftopt-dispatch",
        "maxdcont-handler",
    }


def test_official_executable_hash_matches_retained_evidence() -> None:
    assets = _manifest()["official_assets"]
    assert assets["executable_sha256"] == (
        "599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da"
    )
    assert assets["fixture_artifact_id"] == 8701857473
