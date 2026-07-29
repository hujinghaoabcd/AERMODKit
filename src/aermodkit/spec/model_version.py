"""AERMOD release identifier handling."""

from __future__ import annotations

import re
from dataclasses import dataclass

_VERSION_PATTERN = re.compile(r"^(?:v)?(?P<code>\d{5})$", re.IGNORECASE)


@dataclass(frozen=True, order=True, slots=True)
class ModelVersion:
    """Canonical five-digit EPA model release code, for example ``26135``."""

    code: str

    def __post_init__(self) -> None:
        match = _VERSION_PATTERN.fullmatch(self.code.strip())
        if match is None:
            raise ValueError(f"invalid AERMOD version code: {self.code!r}")
        object.__setattr__(self, "code", match.group("code"))

    @classmethod
    def parse(cls, value: str | ModelVersion) -> ModelVersion:
        """Parse a string or return an existing version object."""

        if isinstance(value, ModelVersion):
            return value
        return cls(value)

    @property
    def release_year(self) -> int:
        """Return the four-digit year encoded by the first two digits."""

        return 2000 + int(self.code[:2])

    @property
    def julian_day(self) -> int:
        """Return the Julian release day encoded by the final three digits."""

        return int(self.code[2:])

    def __str__(self) -> str:
        return f"v{self.code}"
