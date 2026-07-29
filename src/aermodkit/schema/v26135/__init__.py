"""EPA AERMOD v26135 schema."""

from __future__ import annotations

from ..models import AermodVersion
from ..registry import SchemaRegistry
from .keywords import KEYWORDS
from .options import MODEL_OPTIONS
from .sources import SOURCE_TYPES


def build_registry() -> SchemaRegistry:
    return SchemaRegistry(
        version=AermodVersion(26135),
        keywords={(item.pathway, item.name): item for item in KEYWORDS},
        model_options={item.name: item for item in MODEL_OPTIONS},
        source_types={item.name: item for item in SOURCE_TYPES},
    )


__all__ = ["build_registry"]
