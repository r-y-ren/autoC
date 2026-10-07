"""calibrate_conformal 单测（含合成覆盖率断言）。"""
from __future__ import annotations

import numpy as np
import pytest

from run_progressive_risk.calibrate_conformal import ConformalError, calibrate_conformal


def test_interval_clip_and_missing_table():
    pred = {"probs": {"1": 0.02, "3": 0.5, "5": 0.97, "10": 0.4},
            "time_to_unsafe_s": 7.0}
    out = calibrate_conformal(pred, {"1": 0.05, "3": 0.1, "5": 0.15, "10": 0.2})
    assert out["intervals"]["1"]["lo"] == 0.0            # 下界截 0
    assert out["intervals"]["5"]["hi"] == 1.0            # 上界截 1
    assert out["intervals"]["3"]["width"] == pytest.approx(0.2)
    with pytest.raises(ConformalError):
        calibrate_conformal(pred, {})


def test_synthetic_coverage_target():
    """非一致性分数分位数→区间在留出集上经验覆盖率≈90%（split conformal 语义）。"""
    rng = np.random.default_rng(3)
    cal = rng.normal(0, 0.1, 400)                        # 校准集分数
    q = float(np.quantile(np.abs(cal), 0.9))
    test = rng.normal(0, 0.1, 2000)
    covered = np.mean(np.abs(test) <= q)
    assert 0.86 <= covered <= 0.94


def test_online_calibrator_drift_lift():
    """R18：漂移检出触发分位数上浮；稳态不扰动。"""
    from run_progressive_risk.calibrate_conformal import OnlineCalibrator
    oc = OnlineCalibrator({"1": 0.05, "3": 0.1, "5": 0.15, "10": 0.2},
                          drift_window=20, drift_ratio=0.3, alpha=0.1)
    assert not oc.update([0.1] * 20)                       # 稳态：无刷新
    q0 = oc.quantiles()["5"]
    drifted = oc.update([0.5] * 10)                        # 低→高同窗：漂移触发
    assert drifted and oc.quantiles()["5"] > q0
    assert oc.drift_events >= 1
    assert not oc.update([0.05] * 10)                      # 重置后稳态不扰动
