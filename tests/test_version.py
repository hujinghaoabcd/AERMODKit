from aermodkit import ModelVersion, __version__


def test_package_version_is_bootstrap_version() -> None:
    assert __version__ == "0.0.1.dev0"


def test_model_version_normalizes_prefix() -> None:
    version = ModelVersion("v26135")
    assert version.code == "26135"
    assert str(version) == "v26135"
    assert version.release_year == 2026
    assert version.julian_day == 135
