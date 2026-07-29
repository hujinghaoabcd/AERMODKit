from pathlib import Path

from aermodkit import build_project_model, get_registry, parse_aermod, validate_document, write_aermod
from aermodkit.schema import Pathway

FIXTURE = Path(__file__).parent / "fixtures" / "v26135" / "minimal_all_pathways.inp"

EXPECTED = {
    Pathway.CONTROL: {
        "TITLEONE", "TITLETWO", "MODELOPT", "AVERTIME", "URBANOPT", "POLLUTID",
        "HALFLIFE", "DCAYCOEF", "GASDEPDF", "GASDEPVD", "GDLANUSE", "GDSEASON",
        "LOW_WIND", "AWMADWNW", "ORD_DWNW", "NO2EQUIL", "NO2STACK", "NOX_FILE",
        "NOX_UNIT", "NOXVALUE", "NOXSECTR", "NOX_VALS", "ARMRATIO", "O3SECTOR",
        "OZONEFIL", "OZONEVAL", "O3VALUES", "OZONUNIT", "FLAGPOLE", "ARCFTOPT",
        "RUNORNOT", "EVENTFIL", "SAVEFILE", "INITFILE", "MULTYEAR", "DEBUGOPT",
        "ERRORFIL",
    },
    Pathway.SOURCE: {
        "ELEVUNIT", "LOCATION", "RLEMCONV", "SRCPARAM", "BUILDHGT", "BUILDLEN",
        "BUILDWID", "XBADJ", "YBADJ", "AREAVERT", "RBARRIER", "RDEPRESS",
        "SBARRIER", "BLPINPUT", "URBANSRC", "EMISFACT", "EMISUNIT", "CONCUNIT",
        "DEPOUNIT", "PARTDIAM", "MASSFRAX", "PARTDENS", "METHOD_2", "GASDEPOS",
        "NO2RATIO", "HOUREMIS", "BGSECTOR", "BACKGRND", "BACKUNIT", "INCLUDED",
        "OLMGROUP", "BLPGROUP", "PSDGROUP", "HBPSRCID", "ARCFTSRC", "PLATFORM",
        "SRCGROUP",
    },
    Pathway.RECEPTOR: {"ELEVUNIT", "GRIDCART", "GRIDPOLR", "DISCCART", "DISCPOLR", "EVALCART", "INCLUDED"},
    Pathway.METEOROLOGY: {
        "SURFFILE", "PROFFILE", "SURFDATA", "UAIRDATA", "SITEDATA", "PROFBASE",
        "STARTEND", "DAYRANGE", "NUMYEARS", "NOSA", "NOSACO", "NOSAST", "NOSW",
        "NOSWCO", "NOSWST", "NOTURB", "NOTURBCO", "NOTURBST", "SCIMBYHR",
        "WDROTATE", "WINDCATS",
    },
    Pathway.EVENT: {"EVENTPER", "EVENTLOC", "INCLUDED"},
    Pathway.OUTPUT: {
        "RECTABLE", "MAXTABLE", "DAYTABLE", "MAXIFILE", "POSTFILE", "PLOTFILE",
        "TOXXFILE", "RANKFILE", "EVALFILE", "SEASONHR", "MAXDAILY", "MXDYBYYR",
        "MAXDCONT", "SUMMFILE", "FILEFORM", "NOHEADER", "EVENTOUT",
    },
}


def test_complete_v26135_keyword_sets() -> None:
    registry = get_registry("26135")
    for pathway, names in EXPECTED.items():
        assert {spec.name for spec in registry.pathway_keywords(pathway)} == names


def test_multi_pathway_fixture_is_known_lossless_and_semantic() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    document = parse_aermod(text)
    assert write_aermod(document, mode="preserve") == text
    assert not [statement for block in document.pathways() for statement in block.statements() if not statement.known]
    errors = [issue for issue in validate_document(document) if issue.severity.value == "error"]
    assert errors == []

    model = build_project_model(document)
    assert model.pollutant == "NO2"
    assert model.model_options == frozenset({"DFAULT", "CONC", "ELEV"})
    assert model.sources[0].source_id == "STACK1"
    assert model.sources[0].source_type == "POINT"
    assert model.meteorology["SURFFILE"] == (("met/site.sfc",),)
    assert model.document is document


def test_gridcart_continuation_requires_end() -> None:
    text = """RE STARTING
RE GRIDCART G1 STA
RE GRIDCART G1 XYINC 0 2 10 0 2 10
RE FINISHED
"""
    messages = [issue.message for issue in validate_document(parse_aermod(text))]
    assert "GRIDCART network G1 has no END record" in messages


def test_keyword_dependencies_and_ordering() -> None:
    text = """CO STARTING
CO MODELOPT DFAULT CONC ELEV
CO AVERTIME 1
CO POLLUTID NO2
CO SAVEFILE restart.sav
CO MULTYEAR 2
CO RUNORNOT RUN
CO FINISHED
OU STARTING
OU RANKFILE 1 ALL rank.dat
OU FINISHED
"""
    messages = [issue.message for issue in validate_document(parse_aermod(text))]
    assert any("SAVEFILE cannot be combined with MULTYEAR" in message for message in messages)
    assert any("RANKFILE requires keyword(s): MAXTABLE" in message for message in messages)
