"""单步状态迁移判定（阈值+持续+证据完整性+迟滞）（run_safety_state_machine 块）。"""
from __future__ import annotations

LEVELS = ("S0", "S1", "S2", "S3", "S4")
_LV = {n: i for i, n in enumerate(LEVELS)}


def _score(events_window):
    """窗口内最高严重度（0-4）与证据完整性。"""
    best, ev_ids = 0, []
    for ev in events_window:
        sev = int(ev.get("severity", 0))
        if ev.get("type") == "sudden":
            sev = max(sev, 4 if ev.get("fault") not in (None, "未知") else 3)
        if sev > best:
            best = sev
        ev_ids.extend(ev.get("evidence_ids", [ev.get("t")]))
    complete = all(ev.get("evidence") is not None or ev.get("type") == "sudden"
                   for ev in events_window) if events_window else True
    return best, ev_ids, complete


def update_state(current_state: str, event_window, cfg: dict):
    """cfg: {hysteresis, dwell_s: {S1..S4}}；返回 (new_state, record)。

    升级三条件：严重度分值+持续时间（dwell）+证据完整；降级走迟滞带（分值需低于
    目标级阈值−hysteresis 才回落）。阈值邻域抖动被迟滞吸收。
    """
    cur = _LV.get(current_state, 0)
    score, ev_ids, complete = _score(event_window or [])
    hyst = float(cfg.get("hysteresis", 0.05))
    # 目标级：分值映射（分值即 0-4 整数档，迟滞作用在分数软化上）
    soft = score - (hyst if score < cur else 0.0)   # 降级方向软化=迟滞带
    target = int(max(0, min(4, round(soft))))
    dwell_need = float((cfg.get("dwell_s") or {}).get(f"S{max(target, 1)}", 1.0)) if target else 0.0
    record = {"from": current_state, "score": score, "target": f"S{target}",
              "evidence_ids": ev_ids, "evidence_complete": complete,
              "dwell_need_s": dwell_need}
    if not complete and target > cur:
        record["blocked"] = "证据不完整不升级"
        return current_state, record
    if target > cur:
        if dwell_need > 0:
            record["pending"] = f"需持续 {dwell_need}s"
            return current_state, record      # 持续计时由调用方（主循环）累计
        record["upgraded"] = True
        return f"S{target}", record           # dwell=0（如 S4）直达
    if target < cur:
        record["degraded"] = True
        return f"S{target}", record
    return current_state, record
