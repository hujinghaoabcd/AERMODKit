"""Complete pathway keyword registry for EPA AERMOD v26135.

Pathway ``STARTING``/``FINISHED`` records are syntax markers and therefore live
in the lossless parser rather than this statement-keyword registry.
"""

from ..models import KeywordSpec, ParameterKind, ParameterSpec, Pathway
from .evidence import (
    QRG_CONTROL,
    QRG_EVENT,
    QRG_METEOROLOGY,
    QRG_OUTPUT,
    QRG_RECEPTOR,
    QRG_SOURCE,
    USER_GUIDE_APPENDIX,
)

P = ParameterSpec

EVIDENCE = {
    Pathway.CONTROL: (QRG_CONTROL, USER_GUIDE_APPENDIX),
    Pathway.SOURCE: (QRG_SOURCE, USER_GUIDE_APPENDIX),
    Pathway.RECEPTOR: (QRG_RECEPTOR, USER_GUIDE_APPENDIX),
    Pathway.METEOROLOGY: (QRG_METEOROLOGY, USER_GUIDE_APPENDIX),
    Pathway.EVENT: (QRG_EVENT, USER_GUIDE_APPENDIX),
    Pathway.OUTPUT: (QRG_OUTPUT, USER_GUIDE_APPENDIX),
}


def kw(
    pathway: Pathway,
    name: str,
    minimum: int = 0,
    maximum: int | None = 0,
    *,
    repeatable: bool = False,
    mandatory: bool = False,
    mandatory_unless: frozenset[str] = frozenset(),
    requires_keywords: frozenset[str] = frozenset(),
    requires_options: frozenset[str] = frozenset(),
    conflicts_keywords: frozenset[str] = frozenset(),
    first_if_present: bool = False,
    must_be_last: bool = False,
    order: int = 1000,
    path: bool = False,
    notes: tuple[str, ...] = (),
) -> KeywordSpec:
    parameters = (P("filename", ParameterKind.PATH),) if path else ()
    return KeywordSpec(
        pathway=pathway,
        name=name,
        parameters=parameters,
        min_args=minimum,
        max_args=maximum,
        repeatable=repeatable,
        mandatory=mandatory,
        mandatory_unless=mandatory_unless,
        requires_keywords=requires_keywords,
        requires_options=requires_options,
        conflicts_keywords=conflicts_keywords,
        first_if_present=first_if_present,
        must_be_last=must_be_last,
        order=order,
        evidence=EVIDENCE[pathway],
        notes=notes,
    )


CO = Pathway.CONTROL
SO = Pathway.SOURCE
RE = Pathway.RECEPTOR
ME = Pathway.METEOROLOGY
EV = Pathway.EVENT
OU = Pathway.OUTPUT
ALPHA = frozenset({"ALPHA"})

CONTROL_KEYWORDS = (
    kw(CO, "TITLEONE", 1, None, order=10),
    kw(CO, "TITLETWO", 1, None, order=20),
    kw(CO, "MODELOPT", 1, None, mandatory=True, order=30),
    kw(CO, "AVERTIME", 1, None, mandatory=True, order=40),
    kw(CO, "URBANOPT", 2, 4, repeatable=True, order=50),
    kw(CO, "POLLUTID", 1, 2, mandatory=True, order=60),
    kw(CO, "HALFLIFE", 1, 1, order=70),
    kw(CO, "DCAYCOEF", 1, 1, order=80),
    kw(CO, "GASDEPDF", 1, 1, requires_options=ALPHA, order=90),
    kw(CO, "GASDEPVD", 1, 1, requires_options=ALPHA, order=100),
    kw(CO, "GDLANUSE", 36, 36, requires_options=ALPHA, order=110),
    kw(CO, "GDSEASON", 12, 12, requires_options=ALPHA, order=120),
    kw(CO, "LOW_WIND", 3, 3, requires_options=ALPHA, order=130),
    kw(CO, "AWMADWNW", 1, None, requires_options=ALPHA, order=140),
    kw(CO, "ORD_DWNW", 1, None, requires_options=ALPHA, order=150),
    kw(CO, "NO2EQUIL", 1, 1, order=160),
    kw(CO, "NO2STACK", 1, 1, order=170),
    kw(CO, "NOX_FILE", 1, 4, path=True, order=180),
    kw(CO, "NOX_UNIT", 1, 1, order=190),
    kw(CO, "NOXVALUE", 1, 1, repeatable=True, order=200),
    kw(CO, "NOXSECTR", 2, None, repeatable=True, order=210),
    kw(CO, "NOX_VALS", 2, None, repeatable=True, order=220),
    kw(CO, "ARMRATIO", 2, 2, repeatable=True, order=230),
    kw(CO, "O3SECTOR", 2, None, repeatable=True, order=240),
    kw(CO, "OZONEFIL", 1, 1, path=True, order=250),
    kw(CO, "OZONEVAL", 1, 1, repeatable=True, order=260),
    kw(CO, "O3VALUES", 1, None, repeatable=True, order=270),
    kw(CO, "OZONUNIT", 1, 1, order=280),
    kw(CO, "FLAGPOLE", 1, 1, order=290),
    kw(CO, "ARCFTOPT", 1, None, order=300),
    kw(CO, "RUNORNOT", 1, 1, mandatory=True, order=800),
    kw(CO, "EVENTFIL", 1, 1, path=True, order=810),
    kw(CO, "SAVEFILE", 1, 1, path=True, conflicts_keywords=frozenset({"MULTYEAR"}), order=820),
    kw(CO, "INITFILE", 1, 1, path=True, conflicts_keywords=frozenset({"MULTYEAR"}), order=830),
    kw(CO, "MULTYEAR", 1, 1, conflicts_keywords=frozenset({"SAVEFILE", "INITFILE"}), order=840),
    kw(CO, "DEBUGOPT", 1, None, repeatable=True, order=850),
    kw(CO, "ERRORFIL", 1, 1, path=True, order=860),
)

SOURCE_KEYWORDS = (
    kw(SO, "ELEVUNIT", 1, 1, first_if_present=True, order=10),
    kw(SO, "LOCATION", 4, 9, repeatable=True, mandatory=True, mandatory_unless=frozenset({"INCLUDED"}), order=20),
    kw(SO, "RLEMCONV", 0, 0, order=25),
    kw(SO, "SRCPARAM", 3, 7, repeatable=True, mandatory=True, mandatory_unless=frozenset({"INCLUDED"}), order=30),
    kw(SO, "BUILDHGT", 37, 37, repeatable=True, order=40),
    kw(SO, "BUILDLEN", 37, 37, repeatable=True, order=50),
    kw(SO, "BUILDWID", 37, 37, repeatable=True, order=60),
    kw(SO, "XBADJ", 37, 37, repeatable=True, order=70),
    kw(SO, "YBADJ", 37, 37, repeatable=True, order=80),
    kw(SO, "AREAVERT", 3, None, repeatable=True, order=90),
    kw(SO, "RBARRIER", 5, None, repeatable=True, requires_options=ALPHA, order=100),
    kw(SO, "RDEPRESS", 4, None, repeatable=True, requires_options=ALPHA, order=110),
    kw(SO, "SBARRIER", 3, None, repeatable=True, requires_options=ALPHA, order=120),
    kw(SO, "BLPINPUT", 6, 6, order=130),
    kw(SO, "URBANSRC", 2, None, repeatable=True, order=140),
    kw(SO, "EMISFACT", 3, None, repeatable=True, order=150),
    kw(SO, "EMISUNIT", 2, 2, repeatable=True, order=160),
    kw(SO, "CONCUNIT", 2, 2, repeatable=True, order=170),
    kw(SO, "DEPOUNIT", 2, 2, repeatable=True, order=180),
    kw(SO, "PARTDIAM", 2, None, repeatable=True, order=190),
    kw(SO, "MASSFRAX", 2, None, repeatable=True, order=200),
    kw(SO, "PARTDENS", 2, None, repeatable=True, order=210),
    kw(SO, "METHOD_2", 2, None, repeatable=True, requires_options=ALPHA, order=220),
    kw(SO, "GASDEPOS", 4, 5, repeatable=True, requires_options=ALPHA, order=230),
    kw(SO, "NO2RATIO", 2, 2, repeatable=True, order=240),
    kw(SO, "HOUREMIS", 2, 2, repeatable=True, path=True, order=250),
    kw(SO, "BGSECTOR", 3, None, repeatable=True, order=260),
    kw(SO, "BACKGRND", 2, None, repeatable=True, order=270),
    kw(SO, "BACKUNIT", 1, 1, order=280),
    kw(SO, "INCLUDED", 1, 1, repeatable=True, path=True, order=290),
    kw(SO, "OLMGROUP", 2, None, repeatable=True, order=300),
    kw(SO, "BLPGROUP", 2, None, repeatable=True, requires_keywords=frozenset({"BLPINPUT"}), order=310),
    kw(SO, "PSDGROUP", 2, None, repeatable=True, must_be_last=True, order=970),
    kw(SO, "HBPSRCID", 1, None, repeatable=True, requires_options=frozenset({"HBP"}), order=330),
    kw(SO, "ARCFTSRC", 1, None, repeatable=True, order=340),
    kw(SO, "PLATFORM", 2, None, repeatable=True, requires_options=ALPHA, order=350),
    kw(SO, "SRCGROUP", 2, None, repeatable=True, must_be_last=True, order=980),
)

RECEPTOR_KEYWORDS = (
    kw(RE, "ELEVUNIT", 1, 1, first_if_present=True, order=10),
    kw(RE, "GRIDCART", 2, None, repeatable=True, order=20),
    kw(RE, "GRIDPOLR", 2, None, repeatable=True, order=30),
    kw(RE, "DISCCART", 2, 5, repeatable=True, order=40),
    kw(RE, "DISCPOLR", 3, 6, repeatable=True, order=50),
    kw(RE, "EVALCART", 6, 7, repeatable=True, order=60),
    kw(RE, "INCLUDED", 1, 1, repeatable=True, path=True, order=70),
)

METEOROLOGY_KEYWORDS = (
    kw(ME, "SURFFILE", 1, 1, mandatory=True, order=10, path=True),
    kw(ME, "PROFFILE", 1, 1, mandatory=True, order=20, path=True),
    kw(ME, "SURFDATA", 2, 5, mandatory=True, order=30),
    kw(ME, "UAIRDATA", 2, 5, mandatory=True, order=40),
    kw(ME, "SITEDATA", 2, 5, order=50),
    kw(ME, "PROFBASE", 1, 2, mandatory=True, order=60),
    kw(ME, "STARTEND", 6, 8, order=70),
    kw(ME, "DAYRANGE", 1, None, repeatable=True, order=80),
    kw(ME, "NUMYEARS", 1, 1, order=90),
    kw(ME, "NOSA", 0, 0, order=100),
    kw(ME, "NOSACO", 0, 0, order=110),
    kw(ME, "NOSAST", 0, 0, order=120),
    kw(ME, "NOSW", 0, 0, order=130),
    kw(ME, "NOSWCO", 0, 0, order=140),
    kw(ME, "NOSWST", 0, 0, order=150),
    kw(ME, "NOTURB", 0, 0, order=160),
    kw(ME, "NOTURBCO", 0, 0, order=170),
    kw(ME, "NOTURBST", 0, 0, order=180),
    kw(ME, "SCIMBYHR", 2, 4, order=190),
    kw(ME, "WDROTATE", 1, 1, order=200),
    kw(ME, "WINDCATS", 5, 5, order=210),
)

EVENT_KEYWORDS = (
    kw(EV, "EVENTPER", 5, 5, repeatable=True, mandatory=True, mandatory_unless=frozenset({"INCLUDED"}), order=10),
    kw(EV, "EVENTLOC", 5, 8, repeatable=True, mandatory=True, mandatory_unless=frozenset({"INCLUDED"}), order=20),
    kw(EV, "INCLUDED", 1, 1, repeatable=True, path=True, order=30),
)

OUTPUT_KEYWORDS = (
    kw(OU, "RECTABLE", 2, None, repeatable=True, order=10),
    kw(OU, "MAXTABLE", 2, 2, repeatable=True, order=20),
    kw(OU, "DAYTABLE", 1, None, repeatable=True, order=30),
    kw(OU, "MAXIFILE", 4, 5, repeatable=True, path=True, order=40),
    kw(OU, "POSTFILE", 4, 5, repeatable=True, path=True, order=50),
    kw(OU, "PLOTFILE", 3, 5, repeatable=True, path=True, order=60),
    kw(OU, "TOXXFILE", 3, 4, repeatable=True, path=True, order=70),
    kw(OU, "RANKFILE", 3, 4, repeatable=True, requires_keywords=frozenset({"MAXTABLE"}), path=True, order=80),
    kw(OU, "EVALFILE", 2, 3, repeatable=True, path=True, order=90),
    kw(OU, "SEASONHR", 2, 3, repeatable=True, path=True, order=100),
    kw(OU, "MAXDAILY", 2, 3, repeatable=True, path=True, order=110),
    kw(OU, "MXDYBYYR", 2, 3, repeatable=True, path=True, order=120),
    kw(OU, "MAXDCONT", 4, 6, repeatable=True, path=True, order=130),
    kw(OU, "SUMMFILE", 1, 1, path=True, order=140),
    kw(OU, "FILEFORM", 1, 1, order=150),
    kw(OU, "NOHEADER", 1, None, repeatable=True, order=160),
    kw(OU, "EVENTOUT", 1, 1, path=True, order=170),
)

KEYWORDS: tuple[KeywordSpec, ...] = (
    CONTROL_KEYWORDS
    + SOURCE_KEYWORDS
    + RECEPTOR_KEYWORDS
    + METEOROLOGY_KEYWORDS
    + EVENT_KEYWORDS
    + OUTPUT_KEYWORDS
)
