"""Extract the current AERMET 26135 / AERMOD 26135 official test fixtures."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

_ARCHIVE_URL = (
    "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
    "aermod_test_cases.zip"
)
_EXPECTED_ARCHIVE_SHA256 = (
    "fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8"
)
_PREFIX = "aermet26135_aermod26135/"
_ALLOWED_DIRECTORIES = ("inputs/", "meteorology/", "Outputs/")
_ALLOWED_SUFFIXES = {
    ".bat",
    ".dat",
    ".dbg",
    ".emi",
    ".err",
    ".fil",
    ".inp",
    ".log",
    ".out",
    ".pfl",
    ".rnk",
    ".sav",
    ".sfc",
    ".sh",
    ".so",
    ".sum",
    ".txt",
}
_CHUNK_SIZE = 1024 * 1024


def _download(destination: Path) -> tuple[dict[str, str], str]:
    """Download the official test archive and return headers and SHA256."""

    request = urllib.request.Request(
        _ARCHIVE_URL,
        headers={"User-Agent": "AERMODKit-current-test-fixtures/0.1"},
    )
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=180) as response:
        headers = {key.lower(): value for key, value in response.headers.items()}
        with destination.open("wb") as stream:
            while chunk := response.read(_CHUNK_SIZE):
                stream.write(chunk)
                digest.update(chunk)
    return headers, digest.hexdigest()


def _safe_path(name: str) -> Path | None:
    """Return a traversal-safe relative path."""

    candidate = PurePosixPath(name)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return Path(*candidate.parts)


def _is_selected(path: str) -> bool:
    """Return whether an archive entry belongs to the current regression set."""

    normalized = path.replace("\\", "/")
    if not normalized.startswith(_PREFIX):
        return False
    relative = normalized[len(_PREFIX) :]
    if not relative.startswith(_ALLOWED_DIRECTORIES):
        return False
    return PurePosixPath(relative).suffix.lower() in _ALLOWED_SUFFIXES


def create_snapshot(output_dir: Path) -> None:
    """Download, verify, index, and extract the current official regression set."""

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / "aermod_test_cases.zip"
    headers, archive_sha256 = _download(archive)
    if archive_sha256 != _EXPECTED_ARCHIVE_SHA256:
        raise RuntimeError(
            "official test archive SHA256 changed: "
            f"expected {_EXPECTED_ARCHIVE_SHA256}, received {archive_sha256}"
        )

    fixtures_root = output_dir / "fixtures"
    index_path = output_dir / "current-fixtures.csv"
    entries: list[dict[str, object]] = []

    with zipfile.ZipFile(archive) as zip_file:
        for info in zip_file.infolist():
            if info.is_dir() or not _is_selected(info.filename):
                continue
            safe_path = _safe_path(info.filename)
            if safe_path is None:
                continue
            relative = Path(*PurePosixPath(info.filename).parts[1:])
            destination = fixtures_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zip_file.open(info) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target)
            entries.append(
                {
                    "path": info.filename.replace("\\", "/"),
                    "relative_path": relative.as_posix(),
                    "size_bytes": info.file_size,
                    "compressed_size": info.compress_size,
                    "crc32": f"{info.CRC:08x}",
                    "suffix": relative.suffix.lower(),
                }
            )

    with index_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "authority": "U.S. EPA SCRAM",
        "configuration": "aermet26135_aermod26135",
        "archive_url": _ARCHIVE_URL,
        "archive_size_bytes": archive.stat().st_size,
        "archive_sha256": archive_sha256,
        "http_last_modified": headers.get("last-modified"),
        "http_etag": headers.get("etag"),
        "fixture_count": len(entries),
        "fixture_total_bytes": sum(int(entry["size_bytes"]) for entry in entries),
        "directories": list(_ALLOWED_DIRECTORIES),
        "suffixes": sorted(_ALLOWED_SUFFIXES),
    }
    (output_dir / "current-fixtures-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    archive.unlink()


def main() -> None:
    """CLI entry point."""

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    create_snapshot(args.output)


if __name__ == "__main__":
    main()
