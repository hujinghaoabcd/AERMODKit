"""Download and inventory official EPA AERMOD reference archives.

This utility is intended for a controlled GitHub Actions job. It records hashes and
ZIP metadata without committing the large EPA archives to the repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import time
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

_CHUNK_SIZE = 1024 * 1024
_MAX_SELECTED_FILE_SIZE = 2 * 1024 * 1024
_MAX_SELECTED_TOTAL_SIZE = 120 * 1024 * 1024
_SELECTED_SUFFIXES = {
    ".bat",
    ".cmd",
    ".csv",
    ".err",
    ".inp",
    ".json",
    ".md",
    ".out",
    ".plt",
    ".pst",
    ".sh",
    ".txt",
}


@dataclass(frozen=True, slots=True)
class AssetSpec:
    """One canonical EPA archive to download and inventory."""

    asset_id: str
    filename: str
    url: str
    retain_archive: bool = False
    extract_all: bool = False


@dataclass(frozen=True, slots=True)
class AssetResult:
    """Recorded facts for one downloaded archive."""

    asset_id: str
    filename: str
    url: str
    downloaded_at: str
    size_bytes: int
    sha256: str
    content_type: str | None
    content_length_header: str | None
    last_modified: str | None
    etag: str | None
    zip_entry_count: int
    selected_file_count: int
    selected_total_bytes: int


ASSETS = (
    AssetSpec(
        asset_id="aermod-source",
        filename="aermod_source.zip",
        url=(
            "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
            "aermod_source.zip"
        ),
        retain_archive=True,
        extract_all=True,
    ),
    AssetSpec(
        asset_id="sample-run",
        filename="AERMOD_Sample_Run.zip",
        url=(
            "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
            "AERMOD_Sample_Run.zip"
        ),
    ),
    AssetSpec(
        asset_id="test-cases",
        filename="aermod_test_cases.zip",
        url=(
            "https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/"
            "aermod_test_cases.zip"
        ),
    ),
)


def _download(spec: AssetSpec, destination: Path) -> tuple[dict[str, str], str]:
    """Download one asset with retries and return response headers and SHA256."""

    request = urllib.request.Request(
        spec.url,
        headers={"User-Agent": "AERMODKit-reference-snapshot/0.1"},
    )
    partial = destination.with_suffix(destination.suffix + ".part")
    last_error: Exception | None = None

    for attempt in range(1, 4):
        try:
            digest = hashlib.sha256()
            with urllib.request.urlopen(request, timeout=120) as response:
                headers = {key.lower(): value for key, value in response.headers.items()}
                with partial.open("wb") as stream:
                    while chunk := response.read(_CHUNK_SIZE):
                        stream.write(chunk)
                        digest.update(chunk)
            partial.replace(destination)
            return headers, digest.hexdigest()
        except Exception as exc:  # pragma: no cover - network-dependent retry path
            last_error = exc
            partial.unlink(missing_ok=True)
            if attempt < 3:
                time.sleep(5 * attempt)

    raise RuntimeError(f"failed to download {spec.url}") from last_error


def _safe_relative_path(name: str) -> Path | None:
    """Return a traversal-safe relative path for a ZIP entry."""

    candidate = PurePosixPath(name)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    parts = [part for part in candidate.parts if part not in {"", "."}]
    return Path(*parts) if parts else None


def _write_zip_index(asset_id: str, archive: Path, output_dir: Path) -> int:
    """Write a deterministic CSV inventory for one ZIP archive."""

    index_path = output_dir / "indexes" / f"{asset_id}.csv"
    index_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive) as zip_file, index_path.open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "asset_id",
                "path",
                "is_directory",
                "uncompressed_size",
                "compressed_size",
                "crc32",
                "modified_time",
                "compression_method",
            ]
        )
        entries = zip_file.infolist()
        for info in entries:
            writer.writerow(
                [
                    asset_id,
                    info.filename,
                    info.is_dir(),
                    info.file_size,
                    info.compress_size,
                    f"{info.CRC:08x}",
                    "-".join(str(part) for part in info.date_time),
                    info.compress_type,
                ]
            )
    return len(entries)


def _extract_selected(
    asset_id: str,
    archive: Path,
    output_dir: Path,
    *,
    extract_all: bool,
) -> tuple[int, int]:
    """Extract source files or a bounded set of small text fixtures."""

    target_root = output_dir / "selected" / asset_id
    selected_count = 0
    selected_bytes = 0

    with zipfile.ZipFile(archive) as zip_file:
        for info in zip_file.infolist():
            if info.is_dir():
                continue
            relative_path = _safe_relative_path(info.filename)
            if relative_path is None:
                continue
            if not extract_all:
                if relative_path.suffix.lower() not in _SELECTED_SUFFIXES:
                    continue
                if info.file_size > _MAX_SELECTED_FILE_SIZE:
                    continue
                if selected_bytes + info.file_size > _MAX_SELECTED_TOTAL_SIZE:
                    continue

            destination = target_root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zip_file.open(info) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target)
            selected_count += 1
            selected_bytes += info.file_size

    return selected_count, selected_bytes


def _write_summary(output_dir: Path, results: list[AssetResult]) -> None:
    """Write JSON and Markdown summaries."""

    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "authority": "U.S. EPA SCRAM",
        "model_version": "26135",
        "assets": [asdict(result) for result in results],
    }
    (output_dir / "asset-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# AERMOD v26135 official archive snapshot",
        "",
        "Generated by GitHub Actions from canonical U.S. EPA SCRAM URLs.",
        "Large sample/test archives are indexed but are not retained in this artifact.",
        "",
        "| Asset | Bytes | SHA256 | ZIP entries | Selected files |",
        "|---|---:|---|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| `{result.filename}` | {result.size_bytes} | `{result.sha256}` | "
            f"{result.zip_entry_count} | {result.selected_file_count} |"
        )
    lines.append("")
    (output_dir / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def create_snapshot(output_dir: Path) -> None:
    """Create the complete reference snapshot."""

    output_dir.mkdir(parents=True, exist_ok=True)
    downloads_dir = output_dir / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    results: list[AssetResult] = []

    for spec in ASSETS:
        archive = downloads_dir / spec.filename
        headers, sha256 = _download(spec, archive)
        zip_entry_count = _write_zip_index(spec.asset_id, archive, output_dir)
        selected_count, selected_bytes = _extract_selected(
            spec.asset_id,
            archive,
            output_dir,
            extract_all=spec.extract_all,
        )
        results.append(
            AssetResult(
                asset_id=spec.asset_id,
                filename=spec.filename,
                url=spec.url,
                downloaded_at=datetime.now(UTC).isoformat(),
                size_bytes=archive.stat().st_size,
                sha256=sha256,
                content_type=headers.get("content-type"),
                content_length_header=headers.get("content-length"),
                last_modified=headers.get("last-modified"),
                etag=headers.get("etag"),
                zip_entry_count=zip_entry_count,
                selected_file_count=selected_count,
                selected_total_bytes=selected_bytes,
            )
        )
        if spec.retain_archive:
            retained = output_dir / "retained" / spec.filename
            retained.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archive, retained)
        archive.unlink()

    downloads_dir.rmdir()
    _write_summary(output_dir, results)


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    create_snapshot(args.output)


if __name__ == "__main__":
    main()
