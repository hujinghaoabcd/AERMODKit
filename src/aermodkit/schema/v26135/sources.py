"""AERMOD v26135 source-type registry."""

from ..models import ParameterKind, ParameterSpec, SourceTypeSpec
from .evidence import QRG_SOURCE, USER_GUIDE_SOURCE

P = ParameterSpec
E = (QRG_SOURCE, USER_GUIDE_SOURCE)

XY = (P("x", ParameterKind.FLOAT, units="m"), P("y", ParameterKind.FLOAT, units="m"))
BASE = (P("base_elevation", ParameterKind.FLOAT, required=False, units="m MSL"),)
LINE_XY = (
    P("x_start", ParameterKind.FLOAT, units="m"),
    P("y_start", ParameterKind.FLOAT, units="m"),
    P("x_end", ParameterKind.FLOAT, units="m"),
    P("y_end", ParameterKind.FLOAT, units="m"),
)

POINT_PARAMS = (
    P("emission_rate", ParameterKind.FLOAT, units="g/s"),
    P("stack_height", ParameterKind.FLOAT, units="m"),
    P("stack_temperature", ParameterKind.FLOAT, units="K"),
    P("exit_velocity", ParameterKind.FLOAT, units="m/s"),
    P("stack_diameter", ParameterKind.FLOAT, units="m"),
)


def source(
    name: str,
    location_required: tuple[ParameterSpec, ...],
    location_optional: tuple[ParameterSpec, ...],
    srcparam_required: tuple[ParameterSpec, ...],
    srcparam_optional: tuple[ParameterSpec, ...] = (),
    *,
    required_options: frozenset[str] = frozenset(),
    regulatory_default_compatible: bool | None = None,
    description: str = "",
) -> SourceTypeSpec:
    return SourceTypeSpec(
        name=name,
        location_required=location_required,
        location_optional=location_optional,
        srcparam_required=srcparam_required,
        srcparam_optional=srcparam_optional,
        required_options=required_options,
        regulatory_default_compatible=regulatory_default_compatible,
        description=description,
        evidence=E,
    )


SOURCE_TYPES: tuple[SourceTypeSpec, ...] = (
    source("POINT", XY, BASE, POINT_PARAMS, regulatory_default_compatible=True),
    source("POINTCAP", XY, BASE, POINT_PARAMS, regulatory_default_compatible=True),
    source("POINTHOR", XY, BASE, POINT_PARAMS, regulatory_default_compatible=True),
    source(
        "VOLUME",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/s"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("sigma_y_initial", ParameterKind.FLOAT, units="m"),
            P("sigma_z_initial", ParameterKind.FLOAT, units="m"),
        ),
        regulatory_default_compatible=True,
    ),
    source(
        "AREA",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("x_length", ParameterKind.FLOAT, units="m"),
        ),
        (
            P("y_length", ParameterKind.FLOAT, required=False, units="m"),
            P("angle", ParameterKind.FLOAT, required=False, units="degree"),
            P("sigma_z_initial", ParameterKind.FLOAT, required=False, units="m"),
        ),
        regulatory_default_compatible=True,
    ),
    source(
        "AREAPOLY",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("vertex_count", ParameterKind.INTEGER),
        ),
        (P("sigma_z_initial", ParameterKind.FLOAT, required=False, units="m"),),
        regulatory_default_compatible=True,
    ),
    source(
        "AREACIRC",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("radius", ParameterKind.FLOAT, units="m"),
        ),
        (
            P("vertex_count", ParameterKind.INTEGER, required=False),
            P("sigma_z_initial", ParameterKind.FLOAT, required=False, units="m"),
        ),
        regulatory_default_compatible=True,
    ),
    source(
        "OPENPIT",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("x_length", ParameterKind.FLOAT, units="m"),
            P("y_length", ParameterKind.FLOAT, units="m"),
            P("pit_volume", ParameterKind.FLOAT, units="m3"),
        ),
        (P("angle", ParameterKind.FLOAT, required=False, units="degree"),),
        regulatory_default_compatible=True,
    ),
    source(
        "LINE",
        LINE_XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("width", ParameterKind.FLOAT, units="m"),
        ),
        (P("sigma_z_initial", ParameterKind.FLOAT, required=False, units="m"),),
        regulatory_default_compatible=True,
    ),
    source(
        "RLINE",
        LINE_XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(s m2)"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("width", ParameterKind.FLOAT, units="m"),
        ),
        (P("sigma_z_initial", ParameterKind.FLOAT, required=False, units="m"),),
        regulatory_default_compatible=True,
    ),
    source(
        "RLINEXT",
        (
            P("x_start", ParameterKind.FLOAT, units="m"),
            P("y_start", ParameterKind.FLOAT, units="m"),
            P("z_start", ParameterKind.FLOAT, units="m"),
            P("x_end", ParameterKind.FLOAT, units="m"),
            P("y_end", ParameterKind.FLOAT, units="m"),
            P("z_end", ParameterKind.FLOAT, units="m"),
        ),
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/(m s)"),
            P("centerline_offset", ParameterKind.FLOAT, units="m"),
            P("width", ParameterKind.FLOAT, units="m"),
            P("sigma_z_initial", ParameterKind.FLOAT, units="m"),
        ),
        required_options=frozenset({"ALPHA"}),
        regulatory_default_compatible=False,
    ),
    source(
        "BUOYLINE",
        LINE_XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/s"),
            P("release_height", ParameterKind.FLOAT, units="m"),
        ),
        regulatory_default_compatible=True,
    ),
    source(
        "SWPOINT",
        XY,
        BASE,
        (
            P("emission_rate", ParameterKind.FLOAT, units="g/s"),
            P("release_height", ParameterKind.FLOAT, units="m"),
            P("building_width", ParameterKind.FLOAT, units="m"),
            P("building_length", ParameterKind.FLOAT, units="m"),
            P("building_height", ParameterKind.FLOAT, units="m"),
            P("building_angle", ParameterKind.FLOAT, units="degree"),
        ),
        required_options=frozenset({"ALPHA"}),
        regulatory_default_compatible=False,
        description="Research sidewash source type introduced in v22112.",
    ),
)
