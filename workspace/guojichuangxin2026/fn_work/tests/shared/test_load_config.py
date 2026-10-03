"""load_config 单测。"""
from __future__ import annotations

import pytest

from shared.load_config import ConfigError, load_config


def test_default_config_valid():
    cfg = load_config()
    assert cfg.run["hz"] == 20
    assert "lowbat_headwind" in cfg.scenarios
    assert 0 < cfg.thresholds["conformal_cov"] < 1


def test_yaml_override_deep_merge(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text("run: {hz: 50}\nscenarios: {custom: {kind: sudden}}\n", encoding="utf-8")
    cfg = load_config(str(p))
    assert cfg.run["hz"] == 50 and cfg.run["root"] == "runs"
    assert "custom" in cfg.scenarios and "lowbat_headwind" in cfg.scenarios


def test_missing_file_and_bad_fields(tmp_path):
    with pytest.raises(ConfigError):
        load_config(str(tmp_path / "nope.yaml"))
    bad = tmp_path / "bad.yaml"
    bad.write_text("run: {hz: -1}\nscenarios: {a: {kind: x}}\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="hz"):
        load_config(str(bad))
    bad3 = tmp_path / "bad3.yaml"
    bad3.write_text("thresholds: {conformal_cov: 1.5}\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="conformal_cov"):
        load_config(str(bad3))


def test_scenario_kind_required(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text("scenarios: {a: {levels: {}}}\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="kind"):
        load_config(str(p))
