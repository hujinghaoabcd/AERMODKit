"""Complete MODELOPT registry for AERMOD v26135."""

from ..models import ModelOptionSpec, OptionTier
from .evidence import QRG_CONTROL

E = (QRG_CONTROL,)


def option(
    name: str,
    tier: OptionTier,
    order: int,
    *,
    allowed_with_dfault: bool | None = None,
    requires_all: frozenset[str] = frozenset(),
    requires_any: frozenset[str] = frozenset(),
    conflicts: frozenset[str] = frozenset(),
    applicable_source_types: frozenset[str] = frozenset(),
    description: str = "",
) -> ModelOptionSpec:
    return ModelOptionSpec(
        name=name,
        tier=tier,
        order=order,
        allowed_with_dfault=allowed_with_dfault,
        requires_all=requires_all,
        requires_any=requires_any,
        conflicts=conflicts,
        applicable_source_types=applicable_source_types,
        description=description,
        evidence=E,
    )


MODEL_OPTIONS: tuple[ModelOptionSpec, ...] = (
    option("DFAULT", OptionTier.CONTROL_FLAG, 10, allowed_with_dfault=True),
    option(
        "ALPHA", OptionTier.CONTROL_FLAG, 20, allowed_with_dfault=False,
        conflicts=frozenset({"DFAULT"}),
    ),
    option(
        "BETA", OptionTier.CONTROL_FLAG, 30, allowed_with_dfault=False,
        conflicts=frozenset({"DFAULT"}),
        description="v26135 defines the flag but includes no BETA options.",
    ),
    option("CONC", OptionTier.PROCESSING, 40, allowed_with_dfault=True),
    option("AREADPLT", OptionTier.NON_REGULATORY, 50, allowed_with_dfault=False),
    option("FLAT", OptionTier.NON_REGULATORY, 60, allowed_with_dfault=False),
    option("NOSTD", OptionTier.NON_REGULATORY, 70, allowed_with_dfault=False),
    option("NOCHKD", OptionTier.NON_REGULATORY, 80, allowed_with_dfault=False),
    option("NOWARN", OptionTier.PROCESSING, 90, allowed_with_dfault=True),
    option("SCREEN", OptionTier.NON_REGULATORY, 100, allowed_with_dfault=False),
    option("SCIM", OptionTier.NON_REGULATORY, 110, allowed_with_dfault=False),
    option("NOMINO3", OptionTier.REGULATORY, 120, allowed_with_dfault=True),
    option(
        "RLINEFDH", OptionTier.ALPHA, 130, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}),
        applicable_source_types=frozenset({"RLINE", "RLINEXT"}),
    ),
    option("ELEV", OptionTier.REGULATORY, 140, allowed_with_dfault=True),
    option("WARNCHKD", OptionTier.PROCESSING, 150, allowed_with_dfault=True),
    option("NOURBTRAN", OptionTier.NON_REGULATORY, 160, allowed_with_dfault=False),
    option("VECTORWS", OptionTier.REGULATORY, 170, allowed_with_dfault=True),
    option(
        "PSDCREDIT", OptionTier.ALPHA, 180, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA", "PVMRM"}),
        conflicts=frozenset({"OLM", "ARM2", "TTRM", "TTRM2", "GRSM"}),
    ),
    option("FASTALL", OptionTier.NON_REGULATORY, 190, allowed_with_dfault=False),
    option("FASTAREA", OptionTier.NON_REGULATORY, 200, allowed_with_dfault=False),
    option(
        "GRSM", OptionTier.REGULATORY, 210, allowed_with_dfault=None,
        conflicts=frozenset({"PVMRM", "OLM", "ARM2", "TTRM", "TTRM2"}),
    ),
    option(
        "TTRM", OptionTier.ALPHA, 220, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}), conflicts=frozenset({"GRSM"}),
    ),
    option(
        "TTRM2", OptionTier.ALPHA, 230, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}),
        requires_any=frozenset({"PVMRM", "OLM", "ARM2"}),
        conflicts=frozenset({"GRSM", "TTRM"}),
    ),
    option(
        "PVMRM", OptionTier.REGULATORY, 240, allowed_with_dfault=True,
        conflicts=frozenset({"OLM", "ARM2", "GRSM"}),
    ),
    option(
        "OLM", OptionTier.REGULATORY, 250, allowed_with_dfault=True,
        conflicts=frozenset({"PVMRM", "ARM2", "GRSM"}),
    ),
    option(
        "ARM2", OptionTier.REGULATORY, 260, allowed_with_dfault=True,
        conflicts=frozenset({"PVMRM", "OLM", "GRSM"}),
    ),
    option("DEPOS", OptionTier.PROCESSING, 270, allowed_with_dfault=True),
    option("DDEP", OptionTier.PROCESSING, 280, allowed_with_dfault=True),
    option("WDEP", OptionTier.PROCESSING, 290, allowed_with_dfault=True),
    option(
        "DRYDPLT", OptionTier.PROCESSING, 300, allowed_with_dfault=True,
        conflicts=frozenset({"NODRYDPLT"}),
    ),
    option(
        "WETDPLT", OptionTier.PROCESSING, 310, allowed_with_dfault=True,
        conflicts=frozenset({"NOWETDPLT"}),
    ),
    option(
        "NODRYDPLT", OptionTier.PROCESSING, 320, allowed_with_dfault=True,
        conflicts=frozenset({"DRYDPLT"}),
    ),
    option(
        "NOWETDPLT", OptionTier.PROCESSING, 330, allowed_with_dfault=True,
        conflicts=frozenset({"WETDPLT"}),
    ),
    option(
        "AREAMNDR", OptionTier.ALPHA, 340, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}),
        applicable_source_types=frozenset({"AREA", "AREAPOLY", "AREACIRC", "LINE"}),
    ),
    option(
        "HBP", OptionTier.ALPHA, 350, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}),
        applicable_source_types=frozenset({"POINT", "POINTCAP", "POINTHOR"}),
    ),
    option(
        "BAREDGE", OptionTier.ALPHA, 360, allowed_with_dfault=False,
        requires_all=frozenset({"ALPHA"}),
        applicable_source_types=frozenset({"RLINEXT"}),
    ),
)
