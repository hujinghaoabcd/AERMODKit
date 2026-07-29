"""Official evidence references for the v26135 schema."""

from ..models import EvidenceRef

QRG_URL = (
    "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
    "aermod_quick-reference-guide.pdf"
)
USER_GUIDE_URL = (
    "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
    "aermod_userguide.pdf"
)
MCB19_URL = (
    "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_mcb19.pdf"
)


def qrg(identifier: str, pathway: str, pages: tuple[int, ...]) -> EvidenceRef:
    return EvidenceRef(
        identifier=identifier,
        title=f"Quick Reference for AERMOD – Version 26135, {pathway} Pathway",
        url=QRG_URL,
        pages=pages,
    )


QRG_CONTROL = qrg("EPA-AERMOD-QRG-26135-CO", "Control", tuple(range(1, 12)))
QRG_SOURCE = qrg("EPA-AERMOD-QRG-26135-SO", "Source", tuple(range(12, 19)))
QRG_RECEPTOR = qrg("EPA-AERMOD-QRG-26135-RE", "Receptor", (19, 20, 21))
QRG_METEOROLOGY = qrg("EPA-AERMOD-QRG-26135-ME", "Meteorology", (22, 23))
QRG_EVENT = qrg("EPA-AERMOD-QRG-26135-EV", "Event", (24,))
QRG_OUTPUT = qrg("EPA-AERMOD-QRG-26135-OU", "Output", (25, 26, 27))

USER_GUIDE_APPENDIX = EvidenceRef(
    identifier="EPA-AERMOD-UG-26135-APPENDIX-A",
    title="User's Guide for AERMOD v26135, Appendix A input keyword summary",
    url=USER_GUIDE_URL,
    pages=tuple(range(259, 310)),
)
USER_GUIDE_SOURCE = EvidenceRef(
    identifier="EPA-AERMOD-UG-26135-SOURCE",
    title="User's Guide for AERMOD, source pathway sections 3.3.1–3.3.2.12",
    url=USER_GUIDE_URL,
    pages=(132, 133, 164, 165),
)
MCB19 = EvidenceRef(
    identifier="EPA-AERMOD-MCB19",
    title="Model Change Bulletin 19, AERMOD version 26135",
    url=MCB19_URL,
    pages=(1, 2, 3),
)
