import pytest

from aermodkit.spec import load_pathway_specification

EXPECTED_CO = {
    "STARTING",
    "TITLEONE",
    "TITLETWO",
    "MODELOPT",
    "AVERTIME",
    "POLLUTID",
    "HALFLIFE",
    "DCAYCOEF",
    "FLAGPOLE",
    "RUNORNOT",
    "EVENTFIL",
    "SAVEFILE",
    "INITFILE",
    "MULTYEAR",
    "ERRORFIL",
    "GDSEASON",
    "GASDEPDF",
    "GDLANUSE",
    "GASDEPVD",
    "DEBUGOPT",
    "URBANOPT",
    "OZONEVAL",
    "O3VALUES",
    "OZONEFIL",
    "OZONUNIT",
    "NO2STACK",
    "NO2EQUIL",
    "LOW_WIND",
    "O3SECTOR",
    "ARMRATIO",
    "AWMADWNW",
    "ORD_DWNW",
    "NOXSECTR",
    "NOXVALUE",
    "NOX_VALS",
    "NOX_UNIT",
    "NOX_FILE",
    "ARCFTOPT",
    "FINISHED",
}


def test_v26135_co_is_complete_source_verified() -> None:
    specification = load_pathway_specification("co", "26135")
    assert specification.pathway == "CO"
    assert specification.batch == 3
    assert specification.status == "complete-source-verified-co-pathway-specification"
    assert len(specification.records) == 39
    assert set(specification.keywords) == EXPECTED_CO
    assert len(set(specification.keywords)) == 39


def test_co_required_records_match_finished_checks() -> None:
    specification = load_pathway_specification("CO")
    required = {record.keyword for record in specification.records if record.required}
    assert required == {
        "STARTING",
        "FINISHED",
        "TITLEONE",
        "MODELOPT",
        "AVERTIME",
        "POLLUTID",
        "RUNORNOT",
    }


def test_modelopt_all_source_tokens_have_explicit_status() -> None:
    specification = load_pathway_specification("CO")
    model = specification.get_record("MODELOPT")
    allowed = set(model.data["fields"][0]["allowed_values"])
    statuses = model.data["option_status"]
    assert isinstance(statuses, dict)
    assert set(statuses) == allowed
    assert len(statuses) == 40
    assert statuses["BETA"]["guide_status"] == "no actual BETA options in v26135"
    assert statuses["ROMBERG"]["class"] == "legacy-source-token"


def test_temporal_background_cardinalities_match() -> None:
    specification = load_pathway_specification("CO")
    expected = {
        "ANNUAL": 1,
        "SEASON": 4,
        "MONTH": 12,
        "HROFDY": 24,
        "WSPEED": 6,
        "SEASHR": 96,
        "HRDOW": 72,
        "HRDOW7": 168,
        "SHRDOW": 288,
        "SHRDOW7": 672,
        "MHRDOW": 864,
        "MHRDOW7": 2016,
    }
    for keyword in ("O3VALUES", "NOX_VALS"):
        record = specification.get_record(keyword)
        assert record.data["fields"][1]["required_value_counts"] == expected


def test_deposition_shapes_and_alpha_boundaries() -> None:
    specification = load_pathway_specification("CO")
    assert specification.get_record("GDSEASON").data["fields"][0]["exact_items"] == 12
    assert specification.get_record("GDLANUSE").data["fields"][0]["exact_items"] == 36
    assert specification.get_record("GASDEPVD").data["fields"][0]["warning_above"] == 0.05
    for keyword in (
        "GDSEASON",
        "GASDEPDF",
        "GDLANUSE",
        "GASDEPVD",
        "LOW_WIND",
        "AWMADWNW",
        "ORD_DWNW",
        "ARCFTOPT",
    ):
        assert specification.get_record(keyword).data["dependencies"]["requires_modeopt"] == "ALPHA"


def test_low_wind_and_downwash_option_catalogs() -> None:
    specification = load_pathway_specification("CO")
    low = specification.get_record("LOW_WIND")
    assert low.data["fields"][0]["default"] == 0.2
    assert low.data["fields"][4]["maximum"] == 48.0
    awma = specification.get_record("AWMADWNW").data["fields"][0]["allowed_values"]
    assert set(awma) == {
        "AWMAUEFF",
        "AWMAENTRAIN",
        "AWMAUTURB",
        "AWMAUTURBHX",
        "STREAMLINE",
        "STREAMLINED",
    }
    assert set(specification.get_record("ORD_DWNW").data["fields"][0]["allowed_values"]) == {
        "ORDUEFF",
        "ORDTURB",
        "ORDCAV",
    }


def test_all_records_have_source_and_evidence_status() -> None:
    specification = load_pathway_specification("CO")
    for record in specification.records:
        assert record.source["file"] == "coset.f"
        assert record.evidence_status
        assert record.syntax


def test_complete_stage_records_have_current_manual_and_fixture_fields() -> None:
    specification = load_pathway_specification("CO")
    for keyword in specification.keywords[-15:]:
        record = specification.get_record(keyword)
        assert record.data["manual_evidence"]["authority"] == "U.S. EPA SCRAM"
        assert "occurrences" in record.data["fixtures"]


def test_preservation_policy_is_loss_aware() -> None:
    specification = load_pathway_specification("CO")
    for key in (
        "original_text",
        "comments",
        "blank_lines",
        "case",
        "unknown_fields",
        "unknown_records",
    ):
        assert specification.preservation_policy[key] is True


def test_unknown_pathway_fails_loudly() -> None:
    with pytest.raises(LookupError):
        load_pathway_specification("ZZ", "26135")
