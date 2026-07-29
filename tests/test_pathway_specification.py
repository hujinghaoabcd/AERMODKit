import pytest

from aermodkit.spec import load_pathway_specification


def test_v26135_co_batch_one_is_source_verified_and_partial() -> None:
    specification = load_pathway_specification("co", "26135")

    assert specification.pathway == "CO"
    assert specification.batch == 1
    assert "partial" in specification.status
    assert specification.keywords == (
        "STARTING",
        "FINISHED",
        "TITLEONE",
        "TITLETWO",
        "MODELOPT",
        "AVERTIME",
        "POLLUTID",
        "RUNORNOT",
        "ERRORFIL",
        "EVENTFIL",
        "SAVEFILE",
        "INITFILE",
        "MULTYEAR",
        "DEBUGOPT",
    )


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


def test_debugopt_is_record_repeatable_and_knows_v26135_options() -> None:
    record = load_pathway_specification("CO").get_record("debugopt")
    fields = record.data["fields"]

    assert "record-repeatable" in record.repeatability
    assert isinstance(fields, list)
    option_tokens = fields[0]["valid_option_tokens"]
    assert "VBARRIER" in option_tokens
    assert "AIRCRAFT" in option_tokens
    assert len(option_tokens) == 23


def test_modelopt_catalog_and_multiyear_conflicts_are_explicit() -> None:
    specification = load_pathway_specification("CO")
    modelopt = specification.get_record("MODELOPT")
    multiyear = specification.get_record("MULTYEAR")

    fields = modelopt.data["fields"]
    conflicts = multiyear.data["conflicts"]
    assert isinstance(fields, list)
    assert isinstance(conflicts, list)
    assert len(fields[0]["allowed_values"]) == 40
    assert set(conflicts) == {"SAVEFILE", "INITFILE"}


def test_unknown_pathway_fails_loudly() -> None:
    with pytest.raises(LookupError):
        load_pathway_specification("ZZ", "26135")
