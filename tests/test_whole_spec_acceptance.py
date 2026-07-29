import json
from pathlib import Path

from aermodkit.spec import evaluate_v26135_whole_spec

ROOT = Path(__file__).resolve().parents[1]


def test_v26135_record_set_gate_passes() -> None:
    acceptance = evaluate_v26135_whole_spec(ROOT / "reference/coverage")

    assert acceptance.record_set_gate_passed
    assert not acceptance.behavior_probe_gate_passed
    assert not acceptance.syntax_implementation_ready
    assert len(acceptance.pathways) == 7
    assert sum(item.bundled_count for item in acceptance.pathways) == 138
    assert all(item.accepted for item in acceptance.pathways)


def test_v26135_probe_inventory_is_explicit() -> None:
    acceptance = evaluate_v26135_whole_spec(ROOT / "reference/coverage")

    assert acceptance.probes.total == 19
    assert acceptance.probes.executed == 7
    assert acceptance.probes.source_resolved == 1
    assert acceptance.probes.official_executable_pending == 11
    assert len({str(item["id"]) for item in acceptance.probes.entries}) == 19


def test_v26135_acceptance_serialization_is_stable() -> None:
    acceptance = evaluate_v26135_whole_spec(ROOT / "reference/coverage")

    first = acceptance.to_dict()
    second = acceptance.to_dict()
    assert first == second
    assert first["record_set_gate_passed"] is True
    assert first["behavior_probe_gate_passed"] is False


def test_committed_v26135_acceptance_report_is_current() -> None:
    acceptance = evaluate_v26135_whole_spec(ROOT / "reference/coverage")
    committed = json.loads(
        (ROOT / "reference/coverage/v26135-whole-spec-acceptance.json").read_text(
            encoding="utf-8"
        )
    )

    assert committed == acceptance.to_dict()
