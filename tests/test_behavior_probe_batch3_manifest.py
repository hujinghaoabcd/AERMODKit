import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reference/probes/v26135/batch3/manifest.json"
SOURCE_SEARCHES = ROOT / "reference/probes/v26135/batch3/source-searches.json"

DEPENDENCY_RECORDS = {
    "gdseason",
    "gasdepdf",
    "gdlanuse",
    "gasdepvd",
    "low_wind",
    "awmadwnw",
    "ord_dwnw",
}
ARCFTOPT_CASES = {
    "co_arcftopt_single_control",
    "co_arcftopt_no_payload",
    "co_arcftopt_repeated_same",
    "co_arcftopt_repeated_different",
    "co_arcftopt_extra_fields",
    "co_arcftopt_card_no_alpha",
    "co_arcftopt_card_dfault_alpha",
    "co_arcftsrc_alpha_control",
    "co_arcftsrc_no_alpha",
    "co_arcftsrc_dfault_alpha",
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
    assert set(identifiers) == dependency_ids | ARCFTOPT_CASES | MAXDCONT_CASES
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
        "co_arcftopt_single_control",
        "co_arcftsrc_alpha_control",
        "ou_maxdcont_secondary_rank_control",
    }
    assert controls == expected_controls
    assert all(case["expected_outcome"] in {"accepted", "observe"} for case in cases)
    assert all(str(case["question"]).endswith("?") for case in cases)


def test_aircraft_cases_inline_the_hourly_evidence_file() -> None:
    cases = {str(case["id"]): case for case in _manifest()["cases"]}
    for identifier in (
        "co_arcftsrc_alpha_control",
        "co_arcftsrc_no_alpha",
        "co_arcftsrc_dfault_alpha",
    ):
        support = cases[identifier]["support_files"]
        assert len(support) == 1
        assert support[0]["path"] == "aircraft_hourly.dat"
        lines = str(support[0]["content"]).splitlines()
        assert len(lines) == 6
        assert all(line.startswith("SO HOUREMIS 90 01 01") for line in lines)


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
