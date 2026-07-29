#!/usr/bin/env python3
"""Verify that the bundled CO schema covers every COCARD primary keyword."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from aermodkit.spec import load_pathway_specification

PATTERN = re.compile(r"KEYWRD\s+\.EQ\.\s+'([^']+)'", re.IGNORECASE)


def main() -> int:
    """Compare source-dispatched and bundled CO keyword sets."""

    parser = argparse.ArgumentParser()
    parser.add_argument("coset", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    source = args.coset.read_text(errors="replace")
    dispatched: list[str] = []
    for value in PATTERN.findall(source):
        keyword = value.strip().upper()
        if keyword not in dispatched:
            dispatched.append(keyword)

    specification = load_pathway_specification("CO", "26135")
    missing = sorted(set(dispatched) - set(specification.keywords))
    extra = sorted(set(specification.keywords) - set(dispatched))
    result = {
        "source_dispatch_count": len(dispatched),
        "schema_count": len(specification.keywords),
        "missing": missing,
        "extra": extra,
        "exact_set_match": not missing and not extra,
        "status": specification.status,
    }
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.json is not None:
        args.json.write_text(rendered + "\n")

    return 0 if result["exact_set_match"] and len(dispatched) == 39 else 1


if __name__ == "__main__":
    raise SystemExit(main())
