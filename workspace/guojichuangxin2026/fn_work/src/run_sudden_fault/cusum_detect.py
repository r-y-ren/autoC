"""多通道累积和变化检测（越阈+持续拍数确认）（run_sudden_fault 块）。"""
from __future__ import annotations

import math

_DEFAULTS = {"k": 0.15, "h": 1.2, "persist": 3}


def cusum_detect(residual_frames, params: dict | None = None):
    """residual_frames: [{t, **channels}]；返回 {"channels": [...], "t": t} 或 None。

    双侧 CUSUM：S±=max(0, S±+(|x−μ0|∓k))，μ0=0（残差已归一）；越阈 h 且连续 persist 拍确认。
    无状态单遍实现（评估/回放友好）；在线流式包装由 run_sudden_fault 维护。
    """
    p = {**_DEFAULTS, **(params or {})}
    sp: dict[str, float] = {}
    streak: dict[str, int] = {}
    for fr in residual_frames:
        for ch, x in fr.items():
            if ch == "t" or x is None or x != x:
                continue
            x = abs(float(x))
            sp[ch] = max(0.0, sp.get(ch, 0.0) + x - p["k"])
            if sp[ch] > p["h"]:
                streak[ch] = streak.get(ch, 0) + 1
            else:
                streak[ch] = 0
                sp[ch] *= 0.98  # 缓慢泄放，避免慢漂误积累
        ready = sorted(ch for ch, s in streak.items() if s >= p["persist"])
        if ready:
            return {"channels": ready, "t": fr["t"]}
    return None
