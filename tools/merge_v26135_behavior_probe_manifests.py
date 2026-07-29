#!/usr/bin/env python3
"""Merge one base behavior-probe manifest with case fragments and patches."""

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
    if raw_cases is None:
        return []
    if not isinstance(raw_cases, list):
        raise ValueError(f"{context}.cases must be an array")
    result: list[dict[str, Any]] = []
    for index, item in enumerate(raw_cases):
        result.append(_object(item, context=f"{context}.cases[{index}]"))
    return result


def _patches(payload: dict[str, Any], *, context: str) -> list[dict[str, Any]]:
    raw_patches = payload.get("case_patches")
    if raw_patches is None:
        return []
    if not isinstance(raw_patches, list):
        raise ValueError(f"{context}.case_patches must be an array")
    result: list[dict[str, Any]] = []
    for index, item in enumerate(raw_patches):
        result.append(_object(item, context=f"{context}.case_patches[{index}]"))
    return result


def _apply_patch(case: dict[str, Any], patch: dict[str, Any], *, context: str) -> None:
    raw_deletions = patch.get("delete_replace_line_contains", [])
    if not isinstance(raw_deletions, list) or not all(
        isinstance(item, str) and item for item in raw_deletions
    ):
        raise ValueError(f"{context}.delete_replace_line_contains must be a string array")

    mutations = case.get("replace_line_once")
    if not isinstance(mutations, list):
        raise ValueError(f"case {case.get('id')!r} has no replace_line_once array")
    for contains in raw_deletions:
        matches = [
            index
            for index, item in enumerate(mutations)
            if isinstance(item, dict) and item.get("contains") == contains
        ]
        if len(matches) != 1:
            raise ValueError(
                f"{context} expected one mutation containing {contains!r}, found {len(matches)}"
            )
        del mutations[matches[0]]


def merge_manifests(base_path: Path, fragment_paths: list[Path]) -> dict[str, Any]:
    """Return a validated merged manifest without modifying the source files."""

    base = _object(
        json.loads(base_path.read_text(encoding="utf-8")),
        context=str(base_path),
    )
    merged = deepcopy(base)
    merged_cases = list(_cases(merged, context=str(base_path)))

    evidence: list[dict[str, str]] = [{"role": "base", "path": base_path.as_posix()}]
    for fragment_path in fragment_paths:
        fragment = _object(
            json.loads(fragment_path.read_text(encoding="utf-8")),
            context=str(fragment_path),
        )
        if str(fragment.get("model_version")) != str(merged.get("model_version")):
            raise ValueError(f"{fragment_path} model_version does not match base")

        appended = _cases(fragment, context=str(fragment_path))
        patches = _patches(fragment, context=str(fragment_path))
        if not appended and not patches:
            raise ValueError(f"{fragment_path} contains neither cases nor case_patches")
        merged_cases.extend(appended)

        by_id = {str(case.get("id", "")): case for case in merged_cases}
        for index, patch in enumerate(patches):
            identifier = str(patch.get("id", ""))
            if not identifier or identifier not in by_id:
                raise ValueError(f"{fragment_path}.case_patches[{index}] has unknown id")
            _apply_patch(
                by_id[identifier],
                patch,
                context=f"{fragment_path}.case_patches[{index}]",
            )

        role = "case-and-patch-fragment" if appended and patches else (
            "case-fragment" if appended else "case-patch-fragment"
        )
        evidence.append({"role": role, "path": fragment_path.as_posix()})

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
