import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reference/probes/v26135/batch1/manifest.json"
EXPECTED_CASES = {
    "control_test3_rline_barrier",
    "so_swpoint_alpha",
    "so_swpoint_no_alpha",
    "so_vbarrier_one",
    "so_vbarrier_two",
    "co_ozonefil_distinct_sectors_control",
    "co_ozonefil_same_sector_duplicate",
    "co_nox_file_distinct_sectors_control",
    "co_nox_file_same_sector_duplicate",
}
EXPECTED_CONTROLS = {
    "control_test3_rline_barrier",
    "co_ozonefil_distinct_sectors_control",
    "co_nox_file_distinct_sectors_control",
}


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_batch1_manifest_has_unique_expected_cases() -> None:
    payload = _manifest()
    cases = payload["cases"]
    assert isinstance(cases, list)
    identifiers = [str(case["id"]) for case in cases]

    assert set(identifiers) == EXPECTED_CASES
    assert len(identifiers) == len(set(identifiers))


def test_batch1_has_explicit_positive_controls() -> None:
    payload = _manifest()
    cases = payload["cases"]
    controls = {
        str(case["id"])
        for case in cases
        if case["expected_outcome"] == "accepted"
    }

    assert controls == EXPECTED_CONTROLS


def test_targeted_probes_do_not_prejudge_official_behavior() -> None:
    payload = _manifest()
    cases = payload["cases"]
    targeted = [case for case in cases if case["id"] not in EXPECTED_CONTROLS]

    assert targeted
    assert all(case["expected_outcome"] == "observe" for case in targeted)
    assert all(str(case["question"]).endswith("?") for case in targeted)


def test_duplicate_file_probes_use_distinct_paths() -> None:
    payload = _manifest()
    cases = {str(case["id"]): case for case in payload["cases"]}

    ozone = cases["co_ozonefil_same_sector_duplicate"]
    nox = cases["co_nox_file_same_sector_duplicate"]
    assert len(ozone["support_copies"]) == 2
    assert len(nox["support_copies"]) == 2
    assert "ozone_a.dat" in str(ozone["replace_line_once"])
    assert "ozone_b.dat" in str(ozone["replace_line_once"])
    assert "nox_a.dat" in str(nox["replace_line_once"])
    assert "nox_b.dat" in str(nox["replace_line_once"])


def test_official_executable_hash_matches_retained_evidence() -> None:
    payload = _manifest()
    assets = payload["official_assets"]

    assert assets["executable_sha256"] == (
        "599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da"
    )
    assert str(assets["executable_url"]).endswith("/aermod_exe.zip")
    assert str(assets["source_url"]).endswith("/aermod_source.zip")
