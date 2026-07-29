from aermodkit.schema import AermodVersion, OptionTier, get_registry


def test_version_parser() -> None:
    assert AermodVersion.parse("v26135") == AermodVersion(26135)
    assert str(AermodVersion(26135)) == "26135"


def test_v26135_registers_all_source_types() -> None:
    registry = get_registry("26135")
    assert set(registry.source_types) == {"POINT", "POINTCAP", "POINTHOR", "VOLUME", "AREA", "AREAPOLY", "AREACIRC", "OPENPIT", "LINE", "RLINE", "RLINEXT", "BUOYLINE", "SWPOINT"}
    assert registry.source_type("RLINEXT").required_options == frozenset({"ALPHA"})
    assert registry.source_type("SWPOINT").required_options == frozenset({"ALPHA"})


def test_v26135_registers_complete_modelopt_set() -> None:
    registry = get_registry("26135")
    assert set(registry.model_options) == {"DFAULT", "ALPHA", "BETA", "CONC", "AREADPLT", "FLAT", "NOSTD", "NOCHKD", "NOWARN", "SCREEN", "SCIM", "NOMINO3", "RLINEFDH", "ELEV", "WARNCHKD", "NOURBTRAN", "VECTORWS", "PSDCREDIT", "FASTALL", "FASTAREA", "GRSM", "TTRM", "TTRM2", "PVMRM", "OLM", "ARM2", "DEPOS", "DDEP", "WDEP", "DRYDPLT", "WETDPLT", "NODRYDPLT", "NOWETDPLT", "AREAMNDR", "HBP", "BAREDGE"}
    assert registry.model_option("BETA").tier is OptionTier.CONTROL_FLAG
