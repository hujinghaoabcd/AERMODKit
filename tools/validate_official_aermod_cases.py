"""Run and compare official AERMOD v26135 regression cases.

This tool expects an already materialized EPA fixture tree containing ``inputs/``,
``meteorology/``, and ``Outputs/`` plus a compiled AERMOD executable. It keeps
expected and generated outputs separate and treats the PM10 MULTYEAR cases as an
ordered dependency chain.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

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
    r"HIGHEST VALUE IS\s+([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?)"
)
_DATE_PAREN_RE = re.compile(r"\(\d{8}\)")
_COORD_RE = re.compile(r"AT\s*\([^)]*\)")
_PM10_CHAIN = (
    "testpm10_1986",
    "testpm10_1987",
    "testpm10_1988",
    "testpm10_1989",
    "testpm10_1990",
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


def _compare_main_output(expected: Path, generated: Path) -> dict[str, object]:
    expected_lines = _read_lines(expected)
    generated_lines = _read_lines(generated)
    result: dict[str, object] = {
        "expected_line_count": len(expected_lines),
        "generated_line_count": len(generated_lines),
        "line_count_equal": len(expected_lines) == len(generated_lines),
        "canonical_text_identical": False,
        "canonical_diff_lines": None,
        "structure_diff_lines": None,
        "metric_values_compared_on_diff_lines": 0,
        "metric_mismatch_count": 0,
        "metric_max_abs": 0.0,
        "metric_max_rel": 0.0,
    }
    if len(expected_lines) != len(generated_lines):
        return result

    difference_count = 0
    structure_count = 0
    compared_values = 0
    absolute_differences: list[float] = []
    relative_differences: list[float] = []

    for expected_line, generated_line in zip(expected_lines, generated_lines, strict=True):
        if expected_line == generated_line:
            continue
        difference_count += 1
        if _NUMBER_RE.sub("<N>", expected_line) != _NUMBER_RE.sub("<N>", generated_line):
            structure_count += 1
        expected_values = _output_values(expected_line)
        generated_values = _output_values(generated_line)
        if not expected_values or len(expected_values) != len(generated_values):
            continue
        compared_values += len(expected_values)
        for expected_value, generated_value in zip(
            expected_values, generated_values, strict=True
        ):
            if expected_value == generated_value:
                continue
            absolute = abs(expected_value - generated_value)
            relative = absolute / max(abs(expected_value), abs(generated_value), 1e-300)
            absolute_differences.append(absolute)
            relative_differences.append(relative)

    result.update(
        {
            "canonical_text_identical": difference_count == 0,
            "canonical_diff_lines": difference_count,
            "structure_diff_lines": structure_count,
            "metric_values_compared_on_diff_lines": compared_values,
            "metric_mismatch_count": len(absolute_differences),
            "metric_max_abs": max(absolute_differences, default=0.0),
            "metric_max_rel": max(relative_differences, default=0.0),
        }
    )
    return result


def _copy_support_files(source_inputs: Path, target_inputs: Path, executable: Path) -> None:
    target_inputs.mkdir(parents=True, exist_ok=True)
    for item in source_inputs.iterdir():
        if item.is_dir() or item.suffix.lower() == ".inp" or item.name.lower() == "aermod.exe":
            continue
        shutil.copy2(item, target_inputs / item.name)
    shutil.copy2(executable, target_inputs / "aermod.exe")
    os.chmod(target_inputs / "aermod.exe", 0o755)


def _prepare_workspace(
    root: Path, source_inputs: Path, meteorology: Path, executable: Path
) -> tuple[Path, Path]:
    if root.exists():
        shutil.rmtree(root)
    inputs = root / "inputs"
    outputs = root / "generated_outputs"
    for directory in (inputs, outputs, root / "postfiles", root / "plotfiles"):
        directory.mkdir(parents=True, exist_ok=True)
    (root / "Outputs").symlink_to(outputs.name, target_is_directory=True)
    (root / "meteorology").symlink_to(meteorology, target_is_directory=True)
    _copy_support_files(source_inputs, inputs, executable)
    return inputs, outputs


def _run_case(inputs: Path, outputs: Path, input_file: Path) -> dict[str, object]:
    shutil.copy2(input_file, inputs / input_file.name)
    main_output = outputs / f"{input_file.stem}.out"
    started = time.monotonic()
    completed = subprocess.run(
        ["./aermod.exe", input_file.name, f"../Outputs/{main_output.name}"],
        cwd=inputs,
        capture_output=True,
        timeout=900,
        check=False,
    )
    elapsed = time.monotonic() - started
    data = main_output.read_bytes() if main_output.exists() else b""
    return {
        "case": input_file.stem,
        "returncode": completed.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "success_marker": b"AERMOD Finishes Successfully" in data,
        "unsuccessful_marker": b"UN-Successfully" in data,
        "main_output_exists": main_output.exists(),
        "main_output": str(main_output),
        "stdout": completed.stdout.decode("latin1", errors="replace"),
        "stderr": completed.stderr.decode("latin1", errors="replace"),
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate(fixtures: Path, executable: Path, output: Path) -> list[dict[str, object]]:
    source_inputs = fixtures / "inputs"
    expected_outputs = fixtures / "Outputs"
    shared_meteorology = output / "official_meteorology"
    output.mkdir(parents=True, exist_ok=True)
    if not shared_meteorology.exists():
        shutil.copytree(fixtures / "meteorology", shared_meteorology)

    input_files = sorted(source_inputs.glob("*.inp"), key=lambda path: path.name.lower())
    rows: list[dict[str, object]] = []

    for input_file in input_files:
        if input_file.stem in _PM10_CHAIN:
            continue
        workspace = output / "cases" / input_file.stem
        inputs, generated_outputs = _prepare_workspace(
            workspace, source_inputs, shared_meteorology, executable
        )
        run = _run_case(inputs, generated_outputs, input_file)
        generated = generated_outputs / f"{input_file.stem}.out"
        run.update(
            {
                "execution_mode": "isolated",
                **_compare_main_output(
                    expected_outputs / f"{input_file.stem}.out", generated
                ),
            }
        )
        rows.append(run)

    chain_root = output / "chains" / "pm10_multiyear"
    inputs, generated_outputs = _prepare_workspace(
        chain_root, source_inputs, shared_meteorology, executable
    )
    for stem in _PM10_CHAIN:
        input_file = source_inputs / f"{stem}.inp"
        run = _run_case(inputs, generated_outputs, input_file)
        generated = generated_outputs / f"{stem}.out"
        run.update(
            {
                "execution_mode": "multiyear-chain",
                **_compare_main_output(expected_outputs / f"{stem}.out", generated),
            }
        )
        rows.append(run)

    rows.sort(key=lambda row: str(row["case"]).lower())
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = validate(args.fixtures.resolve(), args.executable.resolve(), args.output.resolve())
    report_dir = args.output.resolve() / "comparison_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "results.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )
    _write_csv(report_dir / "results.csv", rows)
    failed = [
        row
        for row in rows
        if row["returncode"] != 0
        or not row["success_marker"]
        or row["unsuccessful_marker"]
        or not row["main_output_exists"]
    ]
    summary = {"cases": len(rows), "successful": len(rows) - len(failed), "failed": failed}
    (report_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
