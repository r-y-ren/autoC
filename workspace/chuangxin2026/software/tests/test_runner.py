"""R5 runner：步进计划数据类+失效判据桩+顶层桩。"""

from __future__ import annotations

import pytest

from linkbench.runner import fail_criteria, runner, stepper
from linkbench.shared.scenario import CriteriaSpec


def test_step_dataclass():
    st = stepper.Step(index=0, style="cw", power_db=-5.0, duration_s=30.0)
    assert st.style == "cw"


def test_stubs():
    with pytest.raises(NotImplementedError):
        stepper.build_step_plan(None)
    with pytest.raises(NotImplementedError):
        fail_criteria.is_failed([], CriteriaSpec())
    with pytest.raises(NotImplementedError):
        runner.run_scenario("scenarios/smoke.yaml")
