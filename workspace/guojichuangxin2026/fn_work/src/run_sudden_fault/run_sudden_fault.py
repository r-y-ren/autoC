"""突发故障主循环：残差→CUSUM→分类→突发事件流（run_sudden_fault 块）。"""
from __future__ import annotations

from run_sudden_fault.build_residuals import build_residuals
from run_sudden_fault.classify_fault import classify_fault
from run_sudden_fault.cusum_detect import cusum_detect

_WINDOW = 40


def run_sudden_fault(frames, raw_telemetry=None, classifier=None, params: dict | None = None):
    """帧流→突发事件生成器；未确认期静默。事件含首触发/确认时刻与检测时延。"""
    hist, res_hist, onset = [], {}, None
    for f in frames:
        hist.append(f)
        hist = hist[-_WINDOW:]
        r = build_residuals(hist, raw_telemetry)
        r["t"] = f.get("t", 0.0)
        res_hist.setdefault("rows", []).append(r)
        res_hist["rows"] = res_hist["rows"][-_WINDOW:]
        conf = cusum_detect(res_hist["rows"], params)
        if conf is not None:
            if onset is None:
                onset = conf["t"]
            # 确认窗统计→分类
            win = res_hist["rows"][-8:]
            feats = {"ch_mean": {}, "ch_max": {}}
            for ch in ("pos_vel_innov", "att_track", "motor_consistency", "telem_loss"):
                xs = [w[ch] for w in win if w.get(ch) == w.get(ch)]
                feats["ch_mean"][ch] = sum(xs) / len(xs) if xs else 0.0
                feats["ch_max"][ch] = max(xs) if xs else 0.0
            cls = classify_fault(feats, classifier)
            yield {"type": "sudden", "t": conf["t"], "t_confirm": conf["t"], "t_onset_est": onset,
                   "channels": conf["channels"], "fault": cls["fault"],
                   "confidence": cls["confidence"], "classify_path": cls["path"],
                   "latency_s": round(conf["t"] - onset, 3)}
            res_hist["rows"] = []  # 确认后复位，等待下一突变
            onset = None             # 时延按事件各自计
