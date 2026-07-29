#!/usr/bin/env python3
"""Run one manifest-defined AERMOD v26135 official behavior-probe batch.

This is an evidence-collection harness, not the AERMODKit application runner.
It supports retained fixture decks, preparation runs that generate later inputs,
isolated case workspaces, source-range extraction, and machine-readable evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

_DIAGNOSTIC_RE = re.compile(
    r"^\s*([A-Z]{2})\s+([EWI]\d{3})\s+(\d+)\s+([A-Z0-9_]+):\s*(.*)$",
    re.IGNORECASE,
)
_SUCCESS_MARKER = "aermod finishes successfully"
_UNSUCCESSFUL_MARKER = "un-successfully"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def _prepare_common_workspace(root: Path, fixtures: Path, executable: Path) -> Path:
    if root.exists():
        shutil.rmtree(root)

    inputs = root / "inputs"
    for directory in (
        inputs,
        root / "Outputs",
        root / "meteorology",
        root / "postfiles",
        root / "plotfiles",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    for item in (fixtures / "inputs").iterdir():
        is_support_file = (
            item.is_file()
            and item.suffix.lower() != ".inp"
            and item.name.lower() != "aermod.exe"
        )
        if is_support_file:
            _copy_file(item, inputs / item.name)

    for item in (fixtures / "meteorology").iterdir():
        if item.is_file():
            _copy_file(item, root / "meteorology" / item.name)

    executable_copy = inputs / "aermod.exe"
    shutil.copy2(executable, executable_copy)
    os.chmod(executable_copy, 0o755)
    return inputs


def _replace_line_once(lines: list[str], contains: str, replacement: str) -> None:
    indexes = [index for index, line in enumerate(lines) if contains in line]
    if len(indexes) != 1:
        raise ValueError(f"expected one line containing {contains!r}, found {len(indexes)}")
    lines[indexes[0] : indexes[0] + 1] = replacement.splitlines()


def _replace_regex_once(lines: list[str], pattern: str, replacement: str) -> None:
    regex = re.compile(pattern, re.IGNORECASE)
    indexes = [index for index, line in enumerate(lines) if regex.search(line)]
    if len(indexes) != 1:
        raise ValueError(f"expected one line matching {pattern!r}, found {len(indexes)}")
    lines[indexes[0] : indexes[0] + 1] = replacement.splitlines()


def _delete_line_once(lines: list[str], contains: str) -> None:
    indexes = [index for index, line in enumerate(lines) if contains in line]
    if len(indexes) != 1:
        raise ValueError(f"expected one line containing {contains!r}, found {len(indexes)}")
    del lines[indexes[0]]


def _resolve_base(
    *,
    fixtures: Path,
    output_root: Path,
    definition: dict[str, Any],
) -> Path:
    if "base_input" in definition:
        return fixtures / "inputs" / str(definition["base_input"])

    source = definition.get("base_from_preparation")
    if not isinstance(source, dict):
        raise ValueError("definition needs base_input or base_from_preparation")

    preparation_id = str(source["id"])
    relative_path = Path(str(source["path"]))
    return output_root / "preparations" / preparation_id / relative_path


def _materialize_deck(
    *,
    fixtures: Path,
    output_root: Path,
    definition: dict[str, Any],
    destination: Path,
) -> Path:
    base = _resolve_base(
        fixtures=fixtures,
        output_root=output_root,
        definition=definition,
    )
    if not base.is_file():
        raise FileNotFoundError(f"base deck not found: {base}")

    raw = base.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    lines = (
        raw.decode("latin1")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .split("\n")
    )

    for mutation in definition.get("replace_line_once", []):
        _replace_line_once(
            lines,
            str(mutation["contains"]),
            str(mutation["replacement"]),
        )
    for mutation in definition.get("replace_regex_once", []):
        _replace_regex_once(
            lines,
            str(mutation["pattern"]),
            str(mutation["replacement"]),
        )
    for contains in definition.get("delete_line_once", []):
        _delete_line_once(lines, str(contains))

    destination.write_bytes(newline.join(lines).encode("latin1"))
    return base


def _parse_diagnostics(paths: list[Path]) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    seen: set[tuple[str, str, int, str, str]] = set()

    for path in paths:
        text = path.read_bytes().decode("latin1", errors="replace")
        for line in text.splitlines():
            match = _DIAGNOSTIC_RE.match(line)
            if match is None:
                continue

            key = (
                match.group(1).upper(),
                match.group(2).upper(),
                int(match.group(3)),
                match.group(4).upper(),
                match.group(5).strip(),
            )
            if key in seen:
                continue
            seen.add(key)
            diagnostics.append(
                {
                    "file": path.name,
                    "pathway": key[0],
                    "code": key[1],
                    "line": key[2],
                    "module": key[3],
                    "message": key[4],
                    "raw": line.rstrip(),
                }
            )
    return diagnostics


def _workspace_files(workspace: Path) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for path in sorted(item for item in workspace.rglob("*") if item.is_file()):
        result.append(
            {
                "path": path.relative_to(workspace).as_posix(),
                "size": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    return result


def _markers(main_output: bytes) -> tuple[bool, bool]:
    normalized = main_output.decode("latin1", errors="replace").casefold()
    return _SUCCESS_MARKER in normalized, _UNSUCCESSFUL_MARKER in normalized


def _classification(
    *,
    returncode: int,
    success_marker: bool,
    unsuccessful_marker: bool,
    diagnostics: list[dict[str, object]],
) -> str:
    has_error = any(str(item["code"]).startswith("E") for item in diagnostics)
    if has_error or unsuccessful_marker:
        return "rejected"
    if returncode == 0 and success_marker:
        return "accepted"
    return "indeterminate"


def _run_definition(
    *,
    fixtures: Path,
    executable: Path,
    output_root: Path,
    definition: dict[str, Any],
    namespace: str,
) -> dict[str, object]:
    identifier = str(definition["id"])
    workspace = output_root / namespace / identifier
    inputs = _prepare_common_workspace(workspace, fixtures, executable)

    for copy_spec in definition.get("support_copies", []):
        source = inputs / str(copy_spec["source"])
        destination = inputs / str(copy_spec["destination"])
        shutil.copy2(source, destination)

    deck = inputs / f"{identifier}.inp"
    base = _materialize_deck(
        fixtures=fixtures,
        output_root=output_root,
        definition=definition,
        destination=deck,
    )
    main_output_path = workspace / "Outputs" / f"{identifier}.out"

    started = time.monotonic()
    completed = subprocess.run(
        [str(inputs / "aermod.exe"), deck.name, f"../Outputs/{identifier}.out"],
        cwd=inputs,
        capture_output=True,
        timeout=int(definition.get("timeout_seconds", 900)),
        check=False,
    )
    elapsed = time.monotonic() - started

    (workspace / "stdout.txt").write_bytes(completed.stdout)
    (workspace / "stderr.txt").write_bytes(completed.stderr)
    main_output = main_output_path.read_bytes() if main_output_path.exists() else b""

    diagnostic_files = [
        path
        for path in (workspace / "Outputs").iterdir()
        if path.is_file()
        and ("ERROR" in path.name.upper() or path.suffix.lower() == ".err")
    ]
    if main_output_path.exists():
        diagnostic_files.insert(0, main_output_path)

    diagnostics = _parse_diagnostics(diagnostic_files)
    success_marker, unsuccessful_marker = _markers(main_output)
    observed = _classification(
        returncode=completed.returncode,
        success_marker=success_marker,
        unsuccessful_marker=unsuccessful_marker,
        diagnostics=diagnostics,
    )
    expected = str(definition.get("expected_outcome", "observe"))
    required_files = [Path(str(path)) for path in definition.get("required_files", [])]
    missing_required_files = [
        path.as_posix() for path in required_files if not (workspace / path).is_file()
    ]
    expectation_met = (
        (expected == "observe" or observed == expected)
        and not missing_required_files
    )

    base_source = (
        {"kind": "fixture", "path": base.name}
        if "base_input" in definition
        else {
            "kind": "preparation",
            "path": base.relative_to(output_root).as_posix(),
        }
    )
    result: dict[str, object] = {
        "id": identifier,
        "question": str(definition["question"]),
        "base_source": base_source,
        "expected_outcome": expected,
        "observed_outcome": observed,
        "expectation_met": expectation_met,
        "returncode": completed.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "main_output_exists": main_output_path.exists(),
        "success_marker": success_marker,
        "unsuccessful_marker": unsuccessful_marker,
        "diagnostics": diagnostics,
        "diagnostic_codes": sorted({str(item["code"]) for item in diagnostics}),
        "required_files": [path.as_posix() for path in required_files],
        "missing_required_files": missing_required_files,
        "files": _workspace_files(workspace),
    }
    (workspace / "definition-result.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def _extract_source_snippets(
    *,
    source_root: Path,
    output_root: Path,
    requests: dict[str, Any],
) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    destination_root = output_root / "source-snippets"
    destination_root.mkdir(parents=True, exist_ok=True)

    for filename, raw_ranges in requests.items():
        ranges = [(int(pair[0]), int(pair[1])) for pair in raw_ranges]
        matches = list(source_root.rglob(filename))
        if len(matches) != 1:
            raise ValueError(
                f"expected one {filename} under {source_root}, found {len(matches)}"
            )

        source = matches[0]
        lines = source.read_text(encoding="latin1", errors="replace").splitlines()
        rendered: list[str] = []
        for start, end in ranges:
            rendered.append(f"===== {filename}:{start}-{end} =====")
            for line_number in range(start, min(end, len(lines)) + 1):
                rendered.append(f"{line_number:6d} {lines[line_number - 1]}")
            rendered.append("")

        destination = destination_root / f"{filename}.probe-ranges.txt"
        destination.write_text("\n".join(rendered), encoding="utf-8")
        evidence.append(
            {
                "file": filename,
                "source_path": source.relative_to(source_root).as_posix(),
                "source_sha256": _sha256(source),
                "ranges": [[start, end] for start, end in ranges],
                "snippet_path": destination.relative_to(output_root).as_posix(),
                "snippet_sha256": _sha256(destination),
            }
        )
    return evidence


def _count_outcomes(results: list[dict[str, object]]) -> dict[str, int]:
    return {
        "items": len(results),
        "accepted": sum(item["observed_outcome"] == "accepted" for item in results),
        "rejected": sum(item["observed_outcome"] == "rejected" for item in results),
        "indeterminate": sum(
            item["observed_outcome"] == "indeterminate" for item in results
        ),
        "expectations_met": sum(bool(item["expectation_met"]) for item in results),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--git-sha", default="unknown")
    args = parser.parse_args()

    fixtures = args.fixtures.resolve()
    executable = args.executable.resolve()
    source_root = args.source_root.resolve()
    source_archive = args.source_archive.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("manifest.cases must be a non-empty array")

    preparations = manifest.get("preparations", [])
    if not isinstance(preparations, list):
        raise ValueError("manifest.preparations must be an array")

    source_requests = manifest.get("source_snippets", {})
    if not isinstance(source_requests, dict):
        raise ValueError("manifest.source_snippets must be an object")

    source_evidence = _extract_source_snippets(
        source_root=source_root,
        output_root=output,
        requests=source_requests,
    )
    preparation_results = [
        _run_definition(
            fixtures=fixtures,
            executable=executable,
            output_root=output,
            definition=definition,
            namespace="preparations",
        )
        for definition in preparations
    ]
    case_results = [
        _run_definition(
            fixtures=fixtures,
            executable=executable,
            output_root=output,
            definition=definition,
            namespace="cases",
        )
        for definition in cases
    ]

    executable_sha256 = _sha256(executable)
    expected_executable_sha256 = str(
        manifest["official_assets"]["executable_sha256"]
    )
    executable_hash_matches_expected = (
        executable_sha256 == expected_executable_sha256
    )

    summary: dict[str, object] = {
        "schema_version": 1,
        "model_version": str(manifest["model_version"]),
        "batch": str(manifest["batch"]),
        "git_sha": args.git_sha,
        "official_assets": {
            "executable_path": executable.name,
            "executable_size": executable.stat().st_size,
            "executable_sha256": executable_sha256,
            "expected_executable_sha256": expected_executable_sha256,
            "executable_hash_matches_expected": executable_hash_matches_expected,
            "source_archive_path": source_archive.name,
            "source_archive_size": source_archive.stat().st_size,
            "source_archive_sha256": _sha256(source_archive),
        },
        "source_evidence": source_evidence,
        "preparations": preparation_results,
        "cases": case_results,
        "totals": {
            "preparations": _count_outcomes(preparation_results),
            "cases": _count_outcomes(case_results),
        },
    }
    (output / "batch-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    infrastructure_failures = [
        item
        for item in [*preparation_results, *case_results]
        if item["expected_outcome"] != "observe" and not item["expectation_met"]
    ]
    if not executable_hash_matches_expected:
        raise SystemExit(
            "official executable SHA-256 did not match retained v26135 evidence"
        )
    return 1 if infrastructure_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
