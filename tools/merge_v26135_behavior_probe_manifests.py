#!/usr/bin/env python3
"""Merge one base behavior-probe manifest with case-only fragments."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


def _object(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{context} must be an object with string keys")
    return value


def _cases(payload: dict[str, Any], *, context: str) -> list[dict[str, Any]]:
    raw_cases = payload.get("cases")
    if not isinstance(raw_cases, list):
        raise ValueError(f"{context}.cases must be an array")
    result: list[dict[str, Any]] = []
    for index, item in enumerate(raw_cases):
        result.append(_object(item, context=f"{context}.cases[{index}]"))
    return result


def merge_manifests(base_path: Path, fragment_paths: list[Path]) -> dict[str, Any]:
    """Return a validated merged manifest without modifying the source files."""

    base = _object(
        json.loads(base_path.read_text(encoding="utf-8")),
        context=str(base_path),
    )
    merged = deepcopy(base)
    merged_cases = list(_cases(merged, context=str(base_path)))

    evidence: list[dict[str, str]] = [
        {"role": "base", "path": base_path.as_posix()}
    ]
    for fragment_path in fragment_paths:
        fragment = _object(
            json.loads(fragment_path.read_text(encoding="utf-8")),
            context=str(fragment_path),
        )
        if str(fragment.get("model_version")) != str(merged.get("model_version")):
            raise ValueError(f"{fragment_path} model_version does not match base")
        merged_cases.extend(_cases(fragment, context=str(fragment_path)))
        evidence.append({"role": "case-fragment", "path": fragment_path.as_posix()})

    identifiers = [str(case.get("id", "")) for case in merged_cases]
    if any(not identifier for identifier in identifiers):
        raise ValueError("every merged case needs a non-empty id")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("merged case ids must be unique")

    merged["cases"] = merged_cases
    merged["manifest_composition"] = evidence
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--fragment", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    merged = merge_manifests(args.base.resolve(), [path.resolve() for path in args.fragment])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
