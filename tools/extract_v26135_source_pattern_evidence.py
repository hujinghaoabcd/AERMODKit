#!/usr/bin/env python3
"""Extract exact diagnostic call contexts from the official AERMOD source tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _object(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{context} must be an object with string keys")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    config = _object(
        json.loads(args.config.read_text(encoding="utf-8")),
        context=str(args.config),
    )
    raw_searches = config.get("searches")
    if not isinstance(raw_searches, list) or not raw_searches:
        raise ValueError("config.searches must be a non-empty array")

    source_files = sorted(
        path
        for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".f", ".f90", ".for"}
    )
    file_cache: dict[Path, list[str]] = {}
    results: list[dict[str, object]] = []

    for index, raw_search in enumerate(raw_searches):
        search = _object(raw_search, context=f"searches[{index}]")
        identifier = str(search.get("id", ""))
        pattern = str(search.get("pattern", ""))
        if not identifier or not pattern:
            raise ValueError(f"searches[{index}] needs id and pattern")
        context_lines = int(search.get("context_lines", 8))
        regex = re.compile(pattern, re.IGNORECASE)
        matches: list[dict[str, object]] = []

        for path in source_files:
            lines = file_cache.setdefault(
                path,
                path.read_text(encoding="latin1", errors="replace").splitlines(),
            )
            for line_index, line in enumerate(lines):
                if regex.search(line) is None:
                    continue
                start_index = max(0, line_index - context_lines)
                end_index = min(len(lines), line_index + context_lines + 1)
                matches.append(
                    {
                        "file": path.relative_to(source_root).as_posix(),
                        "source_sha256": _sha256(path),
                        "line": line_index + 1,
                        "context_start": start_index + 1,
                        "context_end": end_index,
                        "context": [
                            f"{number:6d} {lines[number - 1]}"
                            for number in range(start_index + 1, end_index + 1)
                        ],
                    }
                )

        if not matches:
            raise ValueError(f"source search {identifier!r} found no matches")
        results.append(
            {
                "id": identifier,
                "pattern": pattern,
                "matches": matches,
            }
        )

    payload = {
        "schema_version": 1,
        "model_version": str(config.get("model_version", "26135")),
        "source_root": source_root.name,
        "searches": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
