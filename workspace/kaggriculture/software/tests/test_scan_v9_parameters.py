"""Development-only contract tests for the v9 parameter scanner."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
SCANNER = SOFTWARE_ROOT / "scripts" / "scan_v9_parameters.py"
AGENT_V9 = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v9" / "main.py"


def _load_scanner():
    name = f"scan_v9_test_{id(object())}_{len(sys.modules)}"
    spec = importlib.util.spec_from_file_location(name, SCANNER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_grid_builds_cartesian_product():
    scanner = _load_scanner()
    assert scanner.parse_grid(["herd=11,12", "straw=6-7"]) == [
        {"herd": 11, "straw": 6},
        {"herd": 11, "straw": 7},
        {"herd": 12, "straw": 6},
        {"herd": 12, "straw": 7},
    ]


@pytest.mark.parametrize("specs", [[], ["herd=11", "herd=12"]])
def test_parse_grid_rejects_empty_or_duplicate_axes(specs):
    scanner = _load_scanner()
    with pytest.raises(ValueError):
        scanner.parse_grid(specs)


def test_parse_pool_rejects_unknown_opponent():
    scanner = _load_scanner()
    with pytest.raises(ValueError, match="unknown opponents"):
        scanner.parse_pool("template_wheat,not_a_bot")


def test_validate_output_allows_only_development_root(tmp_path, monkeypatch):
    scanner = _load_scanner()
    monkeypatch.setattr(scanner, "DEV_OUTPUT_ROOT", tmp_path)
    forbidden = [
        scanner.SOFTWARE_ROOT / "exports" / "v9.json",
        scanner.SOFTWARE_ROOT / "metrics.json",
        scanner.SOFTWARE_ROOT.parent / "metrics.json",
        tmp_path.parent / "escape.json",
        tmp_path / "nested" / "scan.txt",
    ]
    for path in forbidden:
        with pytest.raises(ValueError):
            scanner.validate_output(path)
    assert scanner.validate_output(tmp_path / "scan.json") == \
        (tmp_path / "scan.json").resolve()


def test_telemetry_totals_do_not_sum_cumulative_fields():
    scanner = _load_scanner()
    snapshot = {"players": {"0": {"days": {
        "1": {"moving_turns": 2, "effective_ops": 1, "pass_count": 0,
              "cross_quadrant_switches": 1, "wheat_harvested": 3,
              "external_feed_bought": 4, "shed_overflow": 1},
        "2": {"moving_turns": 4, "effective_ops": 2, "pass_count": 1,
              "cross_quadrant_switches": 0, "wheat_harvested": 7,
              "external_feed_bought": 9, "shed_overflow": 3},
    }}}}
    totals = scanner.telemetry_totals(snapshot)
    assert totals["moving_turns"] == 6
    assert totals["effective_ops"] == 3
    assert totals["wheat_harvested"] == 7
    assert totals["external_feed_bought"] == 9
    assert totals["shed_overflow"] == 3
    assert totals["movement_to_effective_ratio"] == 2.0


def test_validate_output_rejects_formal_paths(tmp_path):
    scanner = _load_scanner()
    forbidden = [
        scanner.SOFTWARE_ROOT / "exports" / "v9.json",
        scanner.SOFTWARE_ROOT / "metrics.json",
        scanner.SOFTWARE_ROOT.parent / "metrics.json",
    ]
    for path in forbidden:
        with pytest.raises(ValueError, match="probes/v9"):
            scanner.validate_output(path)
    assert scanner.validate_output(scanner.DEV_OUTPUT_ROOT / "scan.json") == \
        (scanner.DEV_OUTPUT_ROOT / "scan.json").resolve()


def test_main_writes_development_schema_and_candidate_identity(tmp_path,
                                                               monkeypatch):
    scanner = _load_scanner()
    monkeypatch.setattr(scanner, "DEV_OUTPUT_ROOT", tmp_path)
    out = tmp_path / "scan.json"

    def fake_run_combo(candidate, knobs, opponents, seeds, serial):
        return {
            "knobs": knobs,
            "games": 2,
            "record": {"W": 1, "L": 1, "T": 0},
            "avg_candidate_reward": 100.0,
            "avg_margin": 0.0,
            "avg_movement_to_effective_ratio": 3.0,
            "details": [],
        }

    monkeypatch.setattr(scanner, "run_combo", fake_run_combo)
    result = scanner.main([
        "--candidate", str(AGENT_V9),
        "--out", str(out),
        "--seeds", "901",
        "--pool", "template_wheat",
        "--grid", "herd=11,12",
    ])

    assert result == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "v9-parameter-scan/1.0"
    assert payload["kind"] == "development-only"
    assert len(payload["candidate"]["sha256"]) == 64
    assert payload["config"]["combinations"] == 2
    assert len(payload["results"]) == 2
    assert payload["results"][0]["record"] == {"W": 1, "L": 1, "T": 0}
