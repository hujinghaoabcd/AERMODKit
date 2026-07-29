from datetime import date

import pytest

from aermodkit import get_default_version, get_supported_versions
from aermodkit.spec import load_metadata


def test_default_version_is_registered() -> None:
    default = get_default_version()
    assert default in get_supported_versions()


def test_v26135_metadata_is_explicitly_partial() -> None:
    metadata = load_metadata("26135")
    assert metadata.release_date == date(2026, 7, 9)
    assert "partial source-verified" in metadata.schema_completeness
    assert "CO pathway batch 1" in metadata.schema_completeness


def test_unknown_version_fails_loudly() -> None:
    with pytest.raises(LookupError):
        load_metadata("99999")
