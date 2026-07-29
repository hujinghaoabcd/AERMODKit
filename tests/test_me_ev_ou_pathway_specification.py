from __future__ import annotations

import json
from importlib.resources import files

import pytest

from aermodkit.spec import load_pathway_specification

ME = [
    'STARTING',
    'SURFFILE',
    'PROFFILE',
    'SURFDATA',
    'UAIRDATA',
    'STARTEND',
    'DAYRANGE',
    'WDROTATE',
    'SITEDATA',
    'PROFBASE',
    'WINDCATS',
    'SCIMBYHR',
    'NUMYEARS',
    'NOTURB',
    'NOTURBST',
    'NOTURBCO',
    'NOSA',
    'NOSW',
    'NOSAST',
    'NOSWST',
    'NOSACO',
    'NOSWCO',
    'FINISHED',
]

EV = [
    'STARTING',
    'EVENTPER',
    'EVENTLOC',
    'INCLUDED',
    'FINISHED',
]

OU = [
    'STARTING',
    'RECTABLE',
    'MAXTABLE',
    'DAYTABLE',
    'MAXIFILE',
    'POSTFILE',
    'PLOTFILE',
    'TOXXFILE',
    'SEASONHR',
    'RANKFILE',
    'EVALFILE',
    'SUMMFILE',
    'FILEFORM',
    'MAXDAILY',
    'MXDYBYYR',
    'MAXDCONT',
    'NOHEADER',
    'FINISHED',
]

EXPECTED = {"ME": ME, "EV": EV, "OU": OU}

@pytest.mark.parametrize("pathway", ["ME", "EV", "OU"])
def test_complete_pathway_exact_order(pathway: str) -> None:
    spec = load_pathway_specification(pathway, "26135")
    assert list(spec.keywords) == EXPECTED[pathway]
    assert spec.status.startswith("complete-source-verified-")


def test_me_mandatory_and_turbulence_contract() -> None:
    me = load_pathway_specification("ME", "26135")
    for keyword in ["SURFFILE", "PROFFILE", "SURFDATA", "UAIRDATA", "PROFBASE"]:
        assert me.get_record(keyword).required
    windcats = me.get_record("WINDCATS")
    assert windcats.data["fields"][0]["type"] == "exactly five increasing reals"
    assert me.get_record("NOTURB").repeatability == "mutually-exclusive-single-selection"


def test_event_pairing_and_event_output_mode() -> None:
    ev = load_pathway_specification("EV", "26135")
    assert ev.get_record("EVENTPER").required
    assert ev.get_record("EVENTLOC").required
    root = files("aermodkit.spec.versions").joinpath("v26135")
    payload = json.loads(root.joinpath("event_output_mode.json").read_text(encoding="utf-8"))
    keywords = [record["keyword"] for record in payload["records"]]
    assert keywords == ["STARTING", "EVENTOUT", "FILEFORM", "FINISHED"]
    assert payload["completion"]["mandatory"] == ["STARTING", "EVENTOUT", "FINISHED"]


def test_output_controls_and_dependencies() -> None:
    ou = load_pathway_specification("OU", "26135")
    assert ou.get_record("FILEFORM").repeatability == "once"
    assert ou.get_record("NOHEADER").repeatability == "once"
    dependencies = ou.get_record("MAXDCONT").data["dependencies"]
    assert "NO2AVE" in dependencies["requires_pollutant_mode"]
    assert ou.get_record("EVALFILE").data["dependencies"]["requires_receptor"] == "EVALCART"


def test_all_records_preserve_unknown_trailing_fields() -> None:
    for pathway in EXPECTED:
        for record in load_pathway_specification(pathway, "26135").records:
            assert record.data["preservation"]["unknown_trailing_fields"] is True
