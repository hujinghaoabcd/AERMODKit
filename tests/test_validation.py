from aermodkit import DiagnosticSeverity, parse_aermod, validate_document


def messages(text: str) -> list[str]:
    return [item.message for item in validate_document(parse_aermod(text))]


def test_unknown_keyword_warns_but_is_preserved() -> None:
    text = """CO STARTING
CO MODELOPT DFAULT CONC ELEV
CO AVERTIME 1
CO POLLUTID NO2
CO FUTUREKW X
CO RUNORNOT RUN
CO FINISHED
"""
    diagnostics = validate_document(parse_aermod(text))
    warning = next(item for item in diagnostics if item.keyword == "FUTUREKW")
    assert warning.severity is DiagnosticSeverity.WARNING


def test_dfault_rejects_alpha_and_alpha_options() -> None:
    text = """CO STARTING
CO MODELOPT DFAULT ALPHA HBP CONC ELEV
CO AVERTIME 1
CO POLLUTID SO2
CO RUNORNOT RUN
CO FINISHED
"""
    result = messages(text)
    assert any("ALPHA cannot be used with DFAULT" in item for item in result)
    assert any("HBP cannot be used with DFAULT" in item for item in result)


def test_ttrm2_requires_alpha_and_base_method() -> None:
    text = """CO STARTING
CO MODELOPT TTRM2 CONC ELEV
CO AVERTIME 1
CO POLLUTID NO2
CO RUNORNOT RUN
CO FINISHED
"""
    result = messages(text)
    assert any("TTRM2 requires option(s): ALPHA" in item for item in result)
    assert any("TTRM2 requires one of" in item for item in result)


def test_chemistry_methods_are_mutually_exclusive() -> None:
    text = """CO STARTING
CO MODELOPT DFAULT CONC ELEV OLM PVMRM
CO AVERTIME 1
CO POLLUTID NO2
CO RUNORNOT RUN
CO FINISHED
"""
    assert any("OLM cannot be combined with PVMRM" in item for item in messages(text))


def test_swpoint_requires_alpha_and_exact_parameters() -> None:
    text = """CO STARTING
CO MODELOPT CONC ELEV
CO AVERTIME 1
CO POLLUTID OTHER
CO RUNORNOT RUN
CO FINISHED
SO STARTING
SO LOCATION SW1 SWPOINT 100 200 0
SO SRCPARAM SW1 1.0 10 20 40 15 90
SO SRCGROUP ALL SW1
SO FINISHED
"""
    result = messages(text)
    assert any("source type SWPOINT requires MODELOPT ALPHA" in item for item in result)
    assert not any("SRCPARAM for SWPOINT expects" in item for item in result)


def test_rlineext_argument_contract() -> None:
    text = """CO STARTING
CO MODELOPT ALPHA CONC ELEV
CO AVERTIME 1
CO POLLUTID NO2
CO RUNORNOT RUN
CO FINISHED
SO STARTING
SO LOCATION RD1 RLINEXT 0 0 0 100 0 0 5
SO SRCPARAM RD1 0.001 4 12 1.5
SO SRCGROUP ALL RD1
SO FINISHED
"""
    result = messages(text)
    assert not any(item.startswith("LOCATION for RLINEXT expects") for item in result)
    assert not any(item.startswith("SRCPARAM for RLINEXT expects") for item in result)
