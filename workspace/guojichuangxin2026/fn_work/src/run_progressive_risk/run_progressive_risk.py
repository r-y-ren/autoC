"""渐进风险主循环：基线+组窗+TCN+共形→渐进事件流（run_progressive_risk 块）。"""
from __future__ import annotations

from run_progressive_risk.build_feature_window import build_feature_window
from run_progressive_risk.calibrate_conformal import calibrate_conformal
from run_progressive_risk.check_physical_baseline import check_physical_baseline


def run_progressive_risk(frames, margins_stream, model_config: dict | None = None):
    """帧流→渐进事件生成器；模型缺席=物理基线降级通道（保守告警不升级处置）。"""
    mc = model_config or {}
    model = mc.get("model")           # 已加载 Net（load_model_artifact 产物）
    quantiles = mc.get("quantiles")   # 校准分位数表（缺省→区间退化 [p,p]）
    thresholds = mc.get("thresholds") or {"baseline_persist_s": 5.0}
    buf, emitted = {}, {}
    for f, m in zip(frames, margins_stream):
        t = float(f.get("t", 0))
        buf.setdefault("frames", []).append(f)
        buf["frames"] = buf["frames"][-400:]
        mm = dict(m); mm["t"] = t
        buf.setdefault("margins", []).append(mm)
        buf["margins"] = buf["margins"][-200:]
        base = check_physical_baseline(buf["margins"], thresholds)
        ev = {"type": "progressive", "t": t, "severity": 0,
              "baseline": {k: v["triggered"] for k, v in base.items()},
              "evidence": {"margins_tail": buf["margins"][-3:], "baseline": base}}
        win = build_feature_window(buf["frames"])
        if win is not None and model is not None:
            from run_progressive_risk.predict_risk_tcn import predict_risk_tcn
            pred = predict_risk_tcn(win, model)
            pred["probs"] = pred["probs"]
            if quantiles:
                ev["risk"] = calibrate_conformal(pred, quantiles)
            else:
                ev["risk"] = {"intervals": {k: {"prob": p, "lo": p, "hi": p, "width": 0.0}
                                            for k, p in pred["probs"].items()},
                              "time_to_unsafe_s": pred["time_to_unsafe_s"]}
            p5 = ev["risk"]["intervals"].get("5", {}).get("prob", 0.0)
            ev["severity"] = 1 if p5 > 0.3 else (2 if p5 > 0.6 else 0)
        else:
            trig = [k for k, v in base.items() if v["triggered"]]
            if trig:
                ev["severity"] = 2 if "energy" in trig else 1
                ev["downgraded"] = True   # 质量门控：模型不可用→保守告警不升级
        yield ev
