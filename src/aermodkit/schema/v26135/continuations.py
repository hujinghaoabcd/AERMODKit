"""Continuation-card families for AERMOD v26135."""

from ..models import ContinuationFamilySpec, Pathway
from .evidence import QRG_RECEPTOR

CONTINUATION_FAMILIES: tuple[ContinuationFamilySpec, ...] = (
    ContinuationFamilySpec(
        pathway=Pathway.RECEPTOR,
        keyword="GRIDCART",
        action_index=1,
        start_tokens=frozenset({"STA"}),
        end_tokens=frozenset({"END"}),
        member_tokens=frozenset({"XYINC", "XPNTS", "YPNTS", "ELEV", "HILL", "FLAG"}),
        evidence=(QRG_RECEPTOR,),
    ),
    ContinuationFamilySpec(
        pathway=Pathway.RECEPTOR,
        keyword="GRIDPOLR",
        action_index=1,
        start_tokens=frozenset({"STA"}),
        end_tokens=frozenset({"END"}),
        member_tokens=frozenset({"ORIG", "DIST", "DDIR", "GDIR", "ELEV", "HILL", "FLAG"}),
        evidence=(QRG_RECEPTOR,),
    ),
)
