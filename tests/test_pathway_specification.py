import pytest

from aermodkit.spec import load_pathway_specification


def test_v26135_co_batch_two_is_source_verified_and_partial() -> None:
    specification = load_pathway_specification("co", "26135")
    assert specification.pathway == "CO"
    assert specification.batch == 2
    assert "partial" in specification.status
    assert len(specification.records) == 24


def test_batch_two_composes_batch_one_and_two_fragments() -> None:
    specification = load_pathway_specification("CO")
    assert specification.keywords[:4] == ("STARTING", "FINISHED", "TITLEONE", "TITLETWO")
    assert specification.keywords[-10:] == (
        "HALFLIFE", "DCAYCOEF", "FLAGPOLE", "URBANOPT", "O3SECTOR",
        "OZONEVAL", "OZONEFIL", "NO2EQUIL", "NO2STACK", "ARMRATIO",
    )


def test_co_required_records_match_finished_checks() -> None:
    specification = load_pathway_specification("CO")
    required = {record.keyword for record in specification.records if record.required}
    assert required == {
        "STARTING", "FINISHED", "TITLEONE", "MODELOPT",
        "AVERTIME", "POLLUTID", "RUNORNOT",
    }


def test_debugopt_and_modelopt_catalogs() -> None:
    specification = load_pathway_specification("CO")
    debug_fields = specification.get_record("DEBUGOPT").data["fields"]
    model_fields = specification.get_record("MODELOPT").data["fields"]
    assert isinstance(debug_fields, list)
    assert isinstance(model_fields, list)
    assert len(debug_fields[0]["valid_option_tokens"]) == 23
    assert len(model_fields[0]["allowed_values"]) == 40


def test_decay_records_preserve_source_range_boundary() -> None:
    specification = load_pathway_specification("CO")
    half_life = specification.get_record("HALFLIFE")
    decay = specification.get_record("DCAYCOEF")
    assert "not explicitly constrained" in half_life.data["fields"][0]["source_range"]
    assert "not explicitly constrained" in decay.data["fields"][0]["source_range"]
    assert "mutually exclusive" in half_life.repeatability


def test_urban_and_flagpole_defaults() -> None:
    specification = load_pathway_specification("CO")
    flagpole = specification.get_record("FLAGPOLE")
    urban = specification.get_record("URBANOPT")
    assert flagpole.data["fields"][0]["default"] == 0.0
    assert urban.data["fields"][3]["default"] == 1.0
    assert urban.data["fields"][0]["max_length"] == 8


def test_static_ozone_sector_and_file_rules() -> None:
    specification = load_pathway_specification("CO")
    sector = specification.get_record("O3SECTOR")
    ozone_file = specification.get_record("OZONEFIL")
    ozone_value = specification.get_record("OZONEVAL")
    assert sector.data["fields"][0]["min_items"] == 2
    assert sector.data["fields"][0]["max_items"] == 6
    assert ozone_file.data["fields"][1]["max_length"] == 200
    assert ozone_file.data["fields"][3]["default"] == "FREE"
    assert ozone_value.data["fields"][2]["default"] == "UG/M3"


def test_no2_ratio_defaults_and_source_quirks() -> None:
    specification = load_pathway_specification("CO")
    equilibrium = specification.get_record("NO2EQUIL")
    stack = specification.get_record("NO2STACK")
    arm = specification.get_record("ARMRATIO")
    assert equilibrium.data["fields"][0]["default"] == 0.90
    assert stack.data["fields"][0]["default"] is None
    assert arm.data["fields"][0]["default"] == 0.50
    assert any("trailing extra fields" in item["rule"] for item in arm.data["constraints"])


def test_every_batch_two_record_has_manual_source_and_fixture_evidence() -> None:
    specification = load_pathway_specification("CO")
    for keyword in specification.keywords[-10:]:
        record = specification.get_record(keyword)
        assert record.data["manual_evidence"]["authority"] == "U.S. EPA SCRAM"
        assert record.source["file"] == "coset.f"
        assert "occurrences" in record.data["fixtures"]


def test_unknown_pathway_fails_loudly() -> None:
    with pytest.raises(LookupError):
        load_pathway_specification("ZZ", "26135")
