"""check_physical_baseline 单测。"""
from __future__ import annotations


def _m(t, energy):
    return {"t": t, "energy": {"norm": energy}, "nav": {"norm": 0.8},
            "link": {"norm": 0.8}, "control": {"norm": 0.8}}


def test_sustained_shrink_triggers_and_flap_does_not():
    from run_progressive_risk.check_physical_baseline import check_physical_baseline
    seq = [_m(i * 0.25, 0.5 if i < 10 else 0.1) for i in range(40)]  # 低 7.5s
    out = check_physical_baseline(seq, {"energy_margin": 0.15, "baseline_persist_s": 5.0})
    assert out["energy"]["triggered"] and out["energy"]["evidence_span_s"] >= 5.0
    flap = [_m(i * 0.5, 0.1 if i % 2 == 0 else 0.9) for i in range(40)]  # 抖动不累计
    out2 = check_physical_baseline(flap, {"baseline_persist_s": 5.0})
    assert not out2["energy"]["triggered"]
