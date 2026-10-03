"""读 YAML 配置→模式校验→冻结配置对象（shared 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml


class ConfigError(Exception):
    """配置缺失或校验失败；消息带字段名。"""


DEFAULTS: dict[str, Any] = {
    "run": {"root": "runs", "hz": 20},
    "scenarios": {
        "lowbat_headwind": {"kind": "progressive", "battery_drain_x": 2.0, "wind_ms": 6.0,
                            "levels": {"low": 1.4, "mid": 2.2, "high": 3.2}},
        "motor_fail": {"kind": "sudden", "motor": 1,
                       "levels": {"low": 0.4, "mid": 0.7, "high": 1.0}},
        "link_degrade": {"kind": "link", "drop_rate": {"low": 0.1, "mid": 0.3, "high": 0.6}},
    },
    "thresholds": {"energy_margin": 0.15, "nav": 0.4, "link": 0.5, "control": 0.4,
                   "baseline_persist_s": 5.0, "conformal_cov": 0.9},
    "state_machine": {"hysteresis": 0.05,
                      "dwell_s": {"S1": 2.0, "S2": 2.0, "S3": 1.0, "S4": 0.0}},
    "models": {"tcn": "checkpoints/tcn.pt", "classifier": "checkpoints/clf.pkl"},
    "devices": {"modules": [{"name": "sdr", "type": "usrp"}, {"name": "jetson", "type": "ssh"}],
                "replay": {"spectrum": "fixtures/spectrum_replay.npz"}},
    "spectrum": {"center_hz": 2.44e9, "rate_hz": 20e6, "fft": 1024, "frame_fps": 5,
                 "channels": [{"name": "ch6", "lo": 2.426e9, "hi": 2.448e9}], "alert_db": 6.0},
    "sitl": {"mode": "synthetic", "px4_dir": "", "airframe": "gz_x500"},
}


@dataclass(frozen=True)
class Config:
    run: dict = field(default_factory=dict)
    scenarios: dict = field(default_factory=dict)
    thresholds: dict = field(default_factory=dict)
    state_machine: dict = field(default_factory=dict)
    models: dict = field(default_factory=dict)
    devices: dict = field(default_factory=dict)
    spectrum: dict = field(default_factory=dict)
    sitl: dict = field(default_factory=dict)


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise ConfigError("根节点必须为映射")
    for sec in ("run", "scenarios", "thresholds"):
        if not isinstance(data.get(sec), dict) or not data[sec]:
            raise ConfigError(f"配置节缺失或为空: {sec}")
    hz = data["run"].get("hz")
    if not isinstance(hz, (int, float)) or isinstance(hz, bool) or hz <= 0:
        raise ConfigError("run.hz 必须为正数")
    for name, sc in data["scenarios"].items():
        if not isinstance(name, str) or not name:
            raise ConfigError("场景名必须为非空字符串")
        if not isinstance(sc, dict) or "kind" not in sc:
            raise ConfigError(f"scenarios.{name}.kind 缺失")
    if not 0 < float(data["thresholds"].get("conformal_cov", 0.9)) < 1:
        raise ConfigError("thresholds.conformal_cov 必须在 (0,1)")


def load_config(path: str | None = None) -> Config:
    """默认配置与 YAML 覆盖深合并→校验→冻结 Config；失败抛 ConfigError（带字段名）。"""
    data: dict[str, Any] = {}
    if path is not None:
        try:
            with open(path, encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        except FileNotFoundError as exc:
            raise ConfigError(f"配置文件不存在: {path}") from exc
        except yaml.YAMLError as exc:
            raise ConfigError(f"YAML 解析失败: {exc}") from exc
    merged = _deep_merge(DEFAULTS, data)
    _validate(merged)
    return Config(**merged)
