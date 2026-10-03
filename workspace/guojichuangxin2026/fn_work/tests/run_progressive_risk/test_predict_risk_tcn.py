"""predict_risk_tcn 单测。"""
from __future__ import annotations

import numpy as np
import pytest


def test_forward_shapes_and_short_window():
    from run_progressive_risk.predict_risk_tcn import _build, predict_risk_tcn
    net = _build()
    assert sum(p.numel() for p in net.parameters()) < 2_000_000  # 参数量约束
    x = np.random.default_rng(0).normal(size=(120, 18))
    out = predict_risk_tcn(x, net)
    assert set(out["probs"]) == {"1", "3", "5", "10"}
    assert all(0 <= p <= 1 for p in out["probs"].values())
    assert out["time_to_unsafe_s"] >= 0
    with pytest.raises(ValueError):
        predict_risk_tcn(np.zeros((2, 18)), net)
