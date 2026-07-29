#!/usr/bin/env python3
"""Generate deterministic AERMOD v26135 whole-spec acceptance evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from aermodkit.spec import evaluate_v26135_whole_spec


def _markdown(report: dict[str, object]) -> str:
    totals = report["totals"]
    probes = report["behavior_probes"]
    pathways = report["pathways"]
    valid_shape = (
        isinstance(totals, dict)
        and isinstance(probes, dict)
        and isinstance(pathways, list)
    )
    if not valid_shape:
        raise ValueError("acceptance report has an unexpected shape")

    lines = [
        "# AERMOD v26135 whole-spec acceptance",
        "",
        "## Scope",
        "",
        "This report accepts the source-dispatched primary record specification. It does not claim",
        "that the production lexer/CST/writer, semantic model, runner, output parser,",
        "or GIS layers exist. Behavior probes remain a separate prerequisite gate.",
        "",
        "## Gate summary",
        "",
        f"- record-set gate: **{'PASS' if report['record_set_gate_passed'] else 'FAIL'}**",
        "- behavior-probe gate: **{}**".format(
            "PASS" if report["behavior_probe_gate_passed"] else "INCOMPLETE"
        ),
        "- syntax implementation ready: **{}**".format(
            "YES" if report["syntax_implementation_ready"] else "NO"
        ),
        f"- accepted dispatchers: {totals['accepted_dispatchers']}/{totals['dispatcher_count']}",
        f"- source-dispatched primary records: {totals['primary_record_count']}",
        "",
        "## Dispatcher acceptance",
        "",
        (
            "| Dispatcher | Expected | Source | Bundled | Exact set | Framing | Syntax | "
            "Preservation | Result |"
        ),
        "|---|---:|---:|---:|---|---|---|---|---|",
    ]

    def mark(value: object) -> str:
        return "yes" if value is True else "no"

    for item in pathways:
        if not isinstance(item, dict):
            raise ValueError("pathway row must be an object")
        lines.append(
            "| {pathway} | {expected_count} | {source_count} | {bundled_count} | "
            "{exact} | {framing} | {syntax} | {preservation} | {result} |".format(
                pathway=item["pathway"],
                expected_count=item["expected_count"],
                source_count=item["source_count"],
                bundled_count=item["bundled_count"],
                exact=mark(item["exact_set_match"]),
                framing=mark(item["framing_valid"]),
                syntax=mark(item["syntax_present"]),
                preservation=mark(item["preservation_policy_present"]),
                result="PASS" if item["accepted"] else "FAIL",
            )
        )

    lines.extend(
        [
            "",
            "## Retained behavior probes",
            "",
            f"- total: {probes['total']}",
            f"- executed with retained evidence: {probes['executed']}",
            f"- source-resolved: {probes['source_resolved']}",
            f"- official-executable pending: {probes['official_executable_pending']}",
            "",
            "Record-set acceptance therefore passes, but the project remains before the production",
            "loss-aware syntax implementation gate until the retained executable",
            "probes are resolved.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("reference/coverage/v26135-whole-spec-acceptance.json"),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("docs/reference/V26135_WHOLE_SPEC_ACCEPTANCE.md"),
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    report = evaluate_v26135_whole_spec(repo / "reference/coverage").to_dict()
    json_output = repo / args.json_output
    markdown_output = repo / args.markdown_output
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown_output.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps(report["totals"], indent=2))
    return 0 if report["record_set_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
