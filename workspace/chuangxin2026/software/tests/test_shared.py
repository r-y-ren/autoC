"""shared：scenario 数据类契约+桩。"""

from __future__ import annotations

import pytest

from linkbench.shared import clock, safety, scenario, sigmf_io


def test_scenario_dataclasses():
    inj = scenario.InjectionSpec(["cw"], 2422e6, 1e3)
    assert inj.power_start_db == -5.0 and inj.power_step_db == 5.0  # GB 42590 默认口径
    sc = scenario.ScenarioSpec(meta={}, dut_links=[], injection=None,
                               criteria=scenario.CriteriaSpec(),
                               safety=scenario.SafetySpec(),
                               record=scenario.RecordSpec())
    assert sc.injection is None


def test_stubs():
    with pytest.raises(NotImplementedError):
        scenario.load_scenario("scenarios/smoke.yaml")
    with pytest.raises(NotImplementedError):
        sigmf_io.write_sigmf("x", None, [])
    with pytest.raises(NotImplementedError):
        clock.now_ms()
    with pytest.raises(NotImplementedError):
        safety.EstopManager().fire("test")
