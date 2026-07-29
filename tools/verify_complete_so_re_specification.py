"""Verify complete AERMOD v26135 SO and RE specifications."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Final

SO_EXPECTED: Final = [
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
]
RE_EXPECTED: Final = [
    "STARTING",
    "GRIDCART",
    "GRIDPOLR",
    "DISCCART",
    "DISCPOLR",
    "EVALCART",
    "ELEVUNIT",
    "INCLUDED",
    "FINISHED",
]
SO_SOURCE_TYPES: Final = {
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
GRIDCART_SECONDARY: Final = {
    "STA",
    "XYINC",
    "XPNTS",
    "YPNTS",
    "ELEV",
    "HILL",
    "FLAG",
    "END",
}
GRIDPOLR_SECONDARY: Final = {
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


def _source_keywords(path: Path, dispatcher_end: int) -> list[str]:
    lines = path.read_text(errors="replace").splitlines()[:dispatcher_end]
    found: list[str] = []
    for line in lines:
        if line[:1].upper() in {"C", "*", "!"}:
            continue
        for value in re.findall(r"KEYWRD\s*\.EQ\.\s*'([^']+)'", line, flags=re.I):
            normalized = value.strip().upper()
            if normalized and normalized not in found:
                found.append(normalized)
    return found


def _bundled(root: Path, pathway: str) -> list[str]:
    aggregate = json.loads((root / f"{pathway.lower()}_pathway.json").read_text())
    records: list[str] = []
    for name in aggregate["record_files"]:
        fragment = json.loads((root / name).read_text())
        records.extend(record["keyword"] for record in fragment["records"])
    return records


def verify(repo: Path, source: Path) -> None:
    root = repo / "src/aermodkit/spec/versions/v26135"
    pathways = (
        ("SO", SO_EXPECTED, "soset.f", 1008),
        ("RE", RE_EXPECTED, "reset.f", 207),
    )
    for pathway, expected, filename, dispatcher_end in pathways:
        discovered = _source_keywords(source / filename, dispatcher_end)
        bundled = _bundled(root, pathway)
        if discovered != expected or bundled != expected:
            raise SystemExit(
                f"{pathway} mismatch: source={discovered!r}, bundled={bundled!r}"
            )

    source_fragment = json.loads((root / "so_framing_location_parameters.json").read_text())
    location = next(
        record for record in source_fragment["records"] if record["keyword"] == "LOCATION"
    )
    if {item["type"] for item in location["source_types"]} != SO_SOURCE_TYPES:
        raise SystemExit("SO source-type set mismatch")

    receptor_fragment = json.loads((root / "re_grids.json").read_text())
    grid_cart = next(
        record for record in receptor_fragment["records"] if record["keyword"] == "GRIDCART"
    )
    grid_polar = next(
        record for record in receptor_fragment["records"] if record["keyword"] == "GRIDPOLR"
    )
    if set(grid_cart["secondary_records"]) != GRIDCART_SECONDARY:
        raise SystemExit("GRIDCART secondary-record mismatch")
    if set(grid_polar["secondary_records"]) != GRIDPOLR_SECONDARY:
        raise SystemExit("GRIDPOLR secondary-record mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    verify(args.repo.resolve(), args.source_root.resolve())


if __name__ == "__main__":
    main()
