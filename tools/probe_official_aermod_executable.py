"""Probe numerical parity of an AERMOD executable against official fixtures."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

_DATE_RE = re.compile(r"\b\d{2}/\d{2}/\d{2}\b")
_TIME_RE = re.compile(r"\b\d{2}:\d{2}:\d{2}\b")
_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?"
)
_RANK_VALUE_RE = re.compile(
    r"(?:^|\s)\d+\.\s+"
    r"([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?)[cC]?\s*\(\d{8}\)"
)
_HIGHEST_RE = re.compile(
    r"HIGHEST VALUE IS\s+"
    r"([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?)"
)
_DATE_PAREN_RE = re.compile(r"\(\d{8}\)")
_COORD_RE = re.compile(r"AT\s*\([^)]*\)")
_SECTION_RE = re.compile(
    r"\*\*\* THE\s+(.+?)\s+AVERAGE CONCENTRATION\s+"
    r"VALUES FOR SOURCE GROUP:\s*(\S+)"
)


def _canonical_line(line: str) -> str:
    line = _DATE_RE.sub("<DATE>", line.rstrip())
    line = _TIME_RE.sub("<TIME>", line)
    if "**Output Print File:" in line:
        prefix, output_path = line.split(":", 1)
        line = f"{prefix}: {Path(output_path.strip()).name}"
    return line


def _read_lines(path: Path) -> list[str]:
    text = path.read_bytes().decode("latin1", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [_canonical_line(line) for line in text.splitlines()]


def _float(token: str) -> float:
    return float(token.replace("D", "E").replace("d", "e"))


def _output_values(line: str) -> list[float]:
    values = [_float(match.group(1)) for match in _RANK_VALUE_RE.finditer(line)]
    highest = _HIGHEST_RE.search(line)
    if highest:
        values.append(_float(highest.group(1)))
    if "|" in line:
        tail = line.split("|", 1)[1]
        tail = _DATE_PAREN_RE.sub("", tail)
        tail = _COORD_RE.sub("", tail)
        values.extend(_float(token) for token in _NUMBER_RE.findall(tail))
    return values


def _compare_outputs(expected: Path, generated: Path) -> dict[str, Any]:
    expected_lines = _read_lines(expected)
    generated_lines = _read_lines(generated)
    result: dict[str, Any] = {
        "expected_line_count": len(expected_lines),
        "generated_line_count": len(generated_lines),
        "line_count_equal": len(expected_lines) == len(generated_lines),
        "canonical_text_identical": False,
        "canonical_diff_lines": None,
        "metric_mismatch_count": 0,
        "metric_max_abs": 0.0,
        "metric_max_rel": 0.0,
        "max_relative_difference": None,
        "section_summary": [],
    }
    if len(expected_lines) != len(generated_lines):
        return result

    current_section = {"source_group": "other", "table": "other"}
    difference_count = 0
    records: list[dict[str, Any]] = []
    section_records: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for line_number, (expected_line, generated_line) in enumerate(
        zip(expected_lines, generated_lines, strict=True), start=1
    ):
        section_match = _SECTION_RE.search(expected_line)
        if section_match:
            current_section = {
                "source_group": section_match.group(2),
                "table": " ".join(section_match.group(1).split()),
            }
        if expected_line == generated_line:
            continue
        difference_count += 1
        expected_values = _output_values(expected_line)
        generated_values = _output_values(generated_line)
        if not expected_values or len(expected_values) != len(generated_values):
            continue
        for value_index, (expected_value, generated_value) in enumerate(
            zip(expected_values, generated_values, strict=True), start=1
        ):
            if expected_value == generated_value:
                continue
            absolute = abs(expected_value - generated_value)
            relative = absolute / max(abs(expected_value), abs(generated_value), 1e-300)
            record = {
                "line": line_number,
                "value_index": value_index,
                "expected": expected_value,
                "generated": generated_value,
                "absolute_difference": absolute,
                "relative_difference": relative,
                "source_group": current_section["source_group"],
                "table": current_section["table"],
                "expected_line": expected_line,
                "generated_line": generated_line,
            }
            records.append(record)
            key = (record["source_group"], record["table"])
            section_records.setdefault(key, []).append(record)

    records.sort(key=lambda item: item["relative_difference"], reverse=True)
    section_summary = []
    for (source_group, table), items in section_records.items():
        top = max(items, key=lambda item: item["relative_difference"])
        section_summary.append(
            {
                "source_group": source_group,
                "table": table,
                "mismatch_count": len(items),
                "max_absolute_difference": max(
                    item["absolute_difference"] for item in items
                ),
                "max_relative_difference": top["relative_difference"],
                "top_line": top["line"],
            }
        )
    section_summary.sort(
        key=lambda item: item["max_relative_difference"], reverse=True
    )
    result.update(
        {
            "canonical_text_identical": difference_count == 0,
            "canonical_diff_lines": difference_count,
            "metric_mismatch_count": len(records),
            "metric_max_abs": max(
                (record["absolute_difference"] for record in records), default=0.0
            ),
            "metric_max_rel": max(
                (record["relative_difference"] for record in records), default=0.0
            ),
            "max_relative_difference": records[0] if records else None,
            "section_summary": section_summary,
        }
    )
    return result


def _link_or_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def _prepare_workspace(
    root: Path, fixtures: Path, executable: Path, case_name: str
) -> tuple[Path, Path]:
    if root.exists():
        shutil.rmtree(root)
    inputs = root / "inputs"
    outputs = root / "Outputs"
    meteorology = root / "meteorology"
    directories = (
        inputs,
        outputs,
        meteorology,
        root / "postfiles",
        root / "plotfiles",
    )
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    for item in (fixtures / "inputs").iterdir():
        is_support_file = (
            item.is_file()
            and item.suffix.lower() != ".inp"
            and item.name.lower() != "aermod.exe"
        )
        if is_support_file:
            _link_or_copy(item, inputs / item.name)
    for item in (fixtures / "meteorology").iterdir():
        if item.is_file():
            _link_or_copy(item, meteorology / item.name)

    shutil.copy2(fixtures / "inputs" / f"{case_name}.inp", inputs / f"{case_name}.inp")
    executable_copy = inputs / "aermod.exe"
    shutil.copy2(executable, executable_copy)
    os.chmod(executable_copy, 0o755)
    return inputs, outputs


def _run_case(
    fixtures: Path, executable: Path, output_root: Path, case_name: str
) -> dict[str, Any]:
    workspace = output_root / case_name
    inputs, outputs = _prepare_workspace(workspace, fixtures, executable, case_name)
    main_output = outputs / f"{case_name}.out"
    started = time.monotonic()
    completed = subprocess.run(
        [str(inputs / "aermod.exe"), f"{case_name}.inp", f"../Outputs/{case_name}.out"],
        cwd=inputs,
        capture_output=True,
        timeout=900,
        check=False,
    )
    elapsed = time.monotonic() - started
    data = main_output.read_bytes() if main_output.exists() else b""
    result: dict[str, Any] = {
        "case": case_name,
        "returncode": completed.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "success_marker": b"AERMOD Finishes Successfully" in data,
        "unsuccessful_marker": b"UN-Successfully" in data,
        "main_output_exists": main_output.exists(),
        "stdout": completed.stdout.decode("latin1", errors="replace"),
        "stderr": completed.stderr.decode("latin1", errors="replace"),
    }
    if main_output.exists():
        result["comparison"] = _compare_outputs(
            fixtures / "Outputs" / f"{case_name}.out", main_output
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", action="append", dest="cases", required=True)
    args = parser.parse_args()

    fixtures = args.fixtures.resolve()
    executable = args.executable.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    results = [
        _run_case(fixtures, executable, output, case_name)
        for case_name in args.cases
    ]
    summary = {
        "executable": str(executable),
        "cases": results,
    }
    (output / "official-executable-parity.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    failures = [
        result
        for result in results
        if result["returncode"] != 0
        or not result["success_marker"]
        or result["unsuccessful_marker"]
        or not result["main_output_exists"]
    ]
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
