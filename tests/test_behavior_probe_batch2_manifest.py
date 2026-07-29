import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_MANIFEST = ROOT / "reference/probes/v26135/batch2/manifest.json"
ADDITIONAL_CASES = ROOT / "reference/probes/v26135/batch2/additional-cases.json"

EXPECTED_TEMPORAL_CASES = {
    "co_o3values_month_complete_control",
    "co_o3values_month_incomplete",
    "co_nox_vals_month_complete_control",
    "co_nox_vals_month_incomplete",
    "co_o3values_sector_month_complete_control",
    "co_o3values_sector_month_incomplete",
    "co_nox_vals_sector_month_complete_control",
    "co_nox_vals_sector_month_incomplete",
}
EXPECTED_EVENT_CASES = {
    "ou_event_fileform_exp_nondfault_control",
    "ou_event_fileform_exp_dfault_other_control",
    "ou_event_fileform_fix_dfault_so2_control",
    "ou_event_fileform_exp_dfault_so2",
}
EXPECTED_VBARRIER_CASES = {
    "so_vbarrier_all_min_control",
    "so_vbarrier_all_max_control",
    "so_vbarrier_ht_below_min",
    "so_vbarrier_ht_above_max",
    "so_vbarrier_wt_below_min",
    "so_vbarrier_wt_above_max",
    "so_vbarrier_lai_below_min",
    "so_vbarrier_lai_above_max",
    "so_vbarrier_lm_below_min",
    "so_vbarrier_lm_above_max",
    "so_vbarrier_same_side_first_closer",
    "so_vbarrier_same_side_second_closer",
    "so_vbarrier_second_all_min_control",
    "so_vbarrier_second_all_max_control",
    "so_vbarrier_same_side_equal_distance",
}
EXPECTED_CASES = EXPECTED_TEMPORAL_CASES | EXPECTED_EVENT_CASES | EXPECTED_VBARRIER_CASES


def _manifest() -> dict[str, object]:
    payload = json.loads(BASE_MANIFEST.read_text(encoding="utf-8"))
    fragment = json.loads(ADDITIONAL_CASES.read_text(encoding="utf-8"))
    payload["cases"].extend(fragment["cases"])
    return payload


def test_batch2_manifest_has_expected_unique_cases() -> None:
    payload = _manifest()
    cases = payload["cases"]
    assert isinstance(cases, list)
    identifiers = [str(case["id"]) for case in cases]

    assert set(identifiers) == EXPECTED_CASES
    assert len(identifiers) == len(set(identifiers)) == 27


def test_batch2_has_one_event_input_preparation() -> None:
    payload = _manifest()
    preparations = payload["preparations"]
    assert isinstance(preparations, list)
    assert len(preparations) == 1

    preparation = preparations[0]
    assert preparation["id"] == "event_input_seed"
    assert preparation["expected_outcome"] == "accepted"
    assert preparation["required_files"] == ["Outputs/event_batch2_base.inp"]


def test_batch2_controls_are_explicit_and_targets_observe() -> None:
    payload = _manifest()
    cases = payload["cases"]
    controls = {
        case["id"] for case in cases if case["expected_outcome"] == "accepted"
    }

    assert controls == {
        "co_o3values_month_complete_control",
        "co_nox_vals_month_complete_control",
        "co_o3values_sector_month_complete_control",
        "co_nox_vals_sector_month_complete_control",
        "so_vbarrier_all_min_control",
        "so_vbarrier_all_max_control",
        "so_vbarrier_second_all_min_control",
        "so_vbarrier_second_all_max_control",
        "ou_event_fileform_exp_nondfault_control",
        "ou_event_fileform_exp_dfault_other_control",
        "ou_event_fileform_fix_dfault_so2_control",
    }
    assert all(case["expected_outcome"] in {"accepted", "observe"} for case in cases)
    assert all(str(case["question"]).endswith("?") for case in cases)


def test_batch2_source_ranges_cover_target_handlers() -> None:
    payload = _manifest()
    snippets = payload["source_snippets"]

    assert set(snippets) == {"coset.f", "soset.f", "evset.f", "ouset.f"}
    assert [559, 680] in snippets["coset.f"]
    assert [8529, 8731] in snippets["soset.f"]
    assert [776, 900] in snippets["evset.f"]
    assert [3206, 3295] in snippets["ouset.f"]


def test_official_executable_hash_matches_retained_evidence() -> None:
    payload = _manifest()
    assets = payload["official_assets"]

    assert assets["executable_sha256"] == (
        "599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da"
    )
    assert assets["fixture_artifact_id"] == 8701857473
