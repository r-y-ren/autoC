"""inject_scenario_fault 单测。"""
from __future__ import annotations

import pytest

from shared.inject_scenario_fault import InjectError, inject_scenario_fault


class Synthetic:
    scenario_defs = {"motor_fail": {"kind": "sudden", "motor": 1,
                                    "levels": {"low": 0.4, "mid": 0.7, "high": 1.0}}}

    def inject_scenario(self, scenario, level, params):
        return {"applied": params}


class ParamLink:
    target_system, target_component = 1, 1

    class mav:
        @staticmethod
        def param_set_send(sys, comp, name, value):
            ParamLink.sent.append((name.decode() if isinstance(name, bytes) else name, value))
    sent = []


def test_synthetic_path_receipt():
    r = inject_scenario_fault(Synthetic(), "motor_fail", "mid", {"phase": "cruise", "at_s": 12})
    assert r["path"] == "synthetic" and r["params"]["failure_motor1"] == 0.7
    assert r["timing"] == {"phase": "cruise", "at_s": 12}


def test_param_set_path_and_fallback_defs():
    r = inject_scenario_fault(ParamLink(), "lowbat_headwind", "mid", {})
    assert r["path"] == "param_set"
    assert any(k.startswith("sim_") for k, _ in ParamLink.sent)


def test_no_path_raises():
    with pytest.raises(InjectError):
        inject_scenario_fault(object(), "unknown_scenario", "mid", {})
