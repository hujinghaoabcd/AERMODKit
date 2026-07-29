from aermodkit import parse_aermod, validate_document


def messages(text: str) -> list[str]:
    return [issue.message for issue in validate_document(parse_aermod(text))]


def test_scim_requires_scimbyhr_and_annual() -> None:
    text = """CO STARTING
CO MODELOPT SCIM CONC ELEV
CO AVERTIME 1
CO POLLUTID OTHER
CO RUNORNOT RUN
CO FINISHED
ME STARTING
ME SURFFILE x.sfc
ME PROFFILE x.pfl
ME SURFDATA 1 2024
ME UAIRDATA 2 2024
ME PROFBASE 0
ME FINISHED
"""
    result = messages(text)
    assert "MODELOPT SCIM requires ME SCIMBYHR" in result
    assert "MODELOPT SCIM requires ANNUAL in AVERTIME" in result


def test_alpha_source_keyword_requires_alpha() -> None:
    text = """CO STARTING
CO MODELOPT CONC ELEV
CO AVERTIME 1
CO POLLUTID OTHER
CO RUNORNOT RUN
CO FINISHED
SO STARTING
SO LOCATION P1 POINT 0 0
SO SRCPARAM P1 1 10 300 5 1
SO PLATFORM P1 15
SO SRCGROUP ALL P1
SO FINISHED
"""
    assert "PLATFORM requires MODELOPT ALPHA" in messages(text)
