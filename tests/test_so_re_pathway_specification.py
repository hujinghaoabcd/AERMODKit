from aermodkit.spec import load_pathway_specification

SO_EXPECTED = {
    "STARTING",
    "LOCATION",
    "SRCPARAM",
    "BUILDHGT",
    "BUILDWID",
    "BUILDLEN",
    "XBADJ",
    "YBADJ",
    "PLATFORM",
    "EMISFACT",
    "EMISUNIT",
    "RLEMCONV",
    "PARTDIAM",
    "MASSFRAX",
    "PARTDENS",
    "ELEVUNIT",
    "HOUREMIS",
    "CONCUNIT",
    "DEPOUNIT",
    "AREAVERT",
    "INCLUDED",
    "SRCGROUP",
    "GASDEPOS",
    "METHOD_2",
    "URBANSRC",
    "NO2RATIO",
    "OLMGROUP",
    "PSDGROUP",
    "BACKGRND",
    "BACKUNIT",
    "BGSECTOR",
    "RBARRIER",
    "SBARRIER",
    "VBARRIER",
    "RDEPRESS",
    "BLPINPUT",
    "BLPGROUP",
    "ARCFTSRC",
    "HBPSRCID",
    "FINISHED",
}
RE_EXPECTED = {
    "STARTING",
    "GRIDCART",
    "GRIDPOLR",
    "DISCCART",
    "DISCPOLR",
    "EVALCART",
    "ELEVUNIT",
    "INCLUDED",
    "FINISHED",
}
TEMPORAL = {
    "SEASON": 4,
    "MONTH": 12,
    "HROFDY": 24,
    "WSPEED": 6,
    "SEASHR": 96,
    "HRDOW": 72,
    "HRDOW7": 168,
    "SHRDOW": 288,
    "SHRDOW7": 672,
    "MHRDOW": 864,
    "MHRDOW7": 2016,
}


def test_so_complete_exact_set() -> None:
    specification = load_pathway_specification("SO", "26135")
    assert specification.status == "complete-source-verified-so-pathway-specification"
    assert len(specification.records) == 40
    assert set(specification.keywords) == SO_EXPECTED
    assert len(set(specification.keywords)) == 40


def test_re_complete_exact_set() -> None:
    specification = load_pathway_specification("RE", "26135")
    assert specification.status == "complete-source-verified-re-pathway-specification"
    assert len(specification.records) == 9
    assert set(specification.keywords) == RE_EXPECTED


def test_so_source_types_and_srcparam_signatures() -> None:
    specification = load_pathway_specification("SO")
    location = specification.get_record("LOCATION").data
    source_types = {item["type"] for item in location["source_types"]}
    assert source_types == {
        "POINT",
        "POINTCAP",
        "POINTHOR",
        "VOLUME",
        "AREA",
        "AREAPOLY",
        "AREACIRC",
        "OPENPIT",
        "LINE",
        "BUOYLINE",
        "RLINE",
        "RLINEXT",
        "SWPOINT",
    }
    swpoint = next(item for item in location["source_types"] if item["type"] == "SWPOINT")
    assert "manual-list-omission" in swpoint["status"]

    signatures = specification.get_record("SRCPARAM").data["source_type_signatures"]
    assert signatures["POINT"]["min_values"] == 5
    assert signatures["AREA"]["min_values"] == 3
    assert signatures["AREA"]["max_values"] == 6
    assert signatures["RLINEXT"]["min_values"] == 4
    assert signatures["SWPOINT"]["min_values"] == 6


def test_so_temporal_cardinalities_and_corrected_inventory_records() -> None:
    specification = load_pathway_specification("SO")
    emission_counts = specification.get_record("EMISFACT").data["fields"][2]
    assert emission_counts["required_value_counts"] == TEMPORAL

    background_counts = specification.get_record("BACKGRND").data["fields"][2]
    assert background_counts["required_value_counts"] == {"ANNUAL": 1, **TEMPORAL}
    assert specification.get_record("PLATFORM").data["dependencies"]["requires_modeopt"] == (
        "ALPHA"
    )
    assert specification.get_record("VBARRIER").data["dependencies"][
        "allowed_source_types"
    ] == ["RLINEXT"]


def test_re_grid_state_machines() -> None:
    specification = load_pathway_specification("RE")
    grid_cart = specification.get_record("GRIDCART").data
    grid_polar = specification.get_record("GRIDPOLR").data
    assert set(grid_cart["secondary_records"]) == {
        "STA",
        "XYINC",
        "XPNTS",
        "YPNTS",
        "ELEV",
        "HILL",
        "FLAG",
        "END",
    }
    assert set(grid_polar["secondary_records"]) == {
        "STA",
        "ORIG",
        "DIST",
        "DDIR",
        "GDIR",
        "ELEV",
        "HILL",
        "FLAG",
        "END",
    }
    assert "XYINC or (XPNTS and YPNTS)" in grid_cart["state_machine"]["completion"]
    assert "DDIR or GDIR" in grid_polar["state_machine"]["completion"]


def test_so_re_preservation_policy_and_evidence() -> None:
    preservation_keys = (
        "original_text",
        "comments",
        "blank_lines",
        "case",
        "unknown_fields",
        "unknown_records",
        "include_boundaries",
        "block_continuations",
    )
    for pathway in ("SO", "RE"):
        specification = load_pathway_specification(pathway)
        for key in preservation_keys:
            assert specification.preservation_policy[key] is True
        for record in specification.records:
            assert record.source["file"] in {"soset.f", "reset.f"}
            assert record.data["manual_evidence"]["authority"] == "U.S. EPA SCRAM"
            assert "occurrences" in record.data["fixtures"]


def test_re_elevunit_order_and_finish_requirements_are_explicit() -> None:
    specification = load_pathway_specification("RE")
    elevation_rule = specification.get_record("ELEVUNIT").data["constraints"][0]["rule"]
    assert "first functional RE record" in elevation_rule

    finish_rules = " ".join(
        item["rule"] for item in specification.get_record("FINISHED").data["constraints"]
    )
    assert "No GRIDCART/GRIDPOLR block" in finish_rules
    assert "At least one receptor" in finish_rules
