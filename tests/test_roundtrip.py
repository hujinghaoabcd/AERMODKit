from aermodkit import parse_aermod, write_aermod


TEXT = """** project comment
CO STARTING
  TITLEONE  Lossless test
  MODELOPT   ELEV CONC DFAULT
  AVERTIME 1 ANNUAL
  POLLUTID NO2
  FUTUREKW alpha beta
  RUNORNOT RUN
CO FINISHED

SO STARTING
! preserve this source comment
SO LOCATION STACK1 POINT 500 600 12
SO SRCPARAM STACK1 1.2 50 400 15 2
SO INCLUDED \"folder with spaces/sources.inc\"
SO SRCGROUP ALL STACK1
SO FINISHED
"""


def test_preserve_roundtrip_is_exact() -> None:
    document = parse_aermod(TEXT)
    assert write_aermod(document, mode="preserve") == TEXT
    unknown = document.statements("CO", "FUTUREKW")[0]
    assert not unknown.known
    included = document.statements("SO", "INCLUDED")[0]
    assert included.arguments == ("folder with spaces/sources.inc",)


def test_canonical_output_is_stable_and_orders_model_options() -> None:
    first = write_aermod(parse_aermod(TEXT), mode="canonical")
    second = write_aermod(parse_aermod(first), mode="canonical")
    assert first == second
    assert "CO MODELOPT DFAULT CONC ELEV" in first
    assert "FUTUREKW alpha beta" in first
