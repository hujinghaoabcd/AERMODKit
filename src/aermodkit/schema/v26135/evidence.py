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

QRG_CONTROL = EvidenceRef(
    identifier="EPA-AERMOD-QRG-26135-CO",
    title="Quick Reference for AERMOD – Version 26135, Control Pathway",
    url=QRG_URL,
    pages=(1, 2, 3),
)
QRG_SOURCE = EvidenceRef(
    identifier="EPA-AERMOD-QRG-26135-SO",
    title="Quick Reference for AERMOD – Version 26135, Source Pathway",
    url=QRG_URL,
    pages=(12, 13),
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
