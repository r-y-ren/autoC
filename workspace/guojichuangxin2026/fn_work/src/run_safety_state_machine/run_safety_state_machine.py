"""状态机主循环：双通道事件→S 态轨迹+处置建议流（run_safety_state_machine 块）。"""
from __future__ import annotations

import time

from run_safety_state_machine.plan_disposal import plan_disposal
from run_safety_state_machine.update_state import update_state


def run_safety_state_machine(events, margins, mission_context, cfg: dict | None = None):
    """事件流+margins→(状态轨迹, 处置建议) 生成器；dwell 由时间戳累计驱动。"""
    cfg = cfg or {"hysteresis": 0.05,
                  "dwell_s": {"S1": 2.0, "S2": 2.0, "S3": 1.0, "S4": 0.0}}
    state, pend_since, ev_buf = "S0", None, []
    for ev in events:
        t = float(ev.get("t", 0.0))
        ev_buf.append(ev)
        ev_buf = [e for e in ev_buf if t - float(e.get("t", 0)) <= 8.0]
        new_state, rec = update_state(state, ev_buf, cfg)
        if rec.get("pending"):
            if pend_since is None:
                pend_since = t
            elif t - pend_since >= float(rec.get("dwell_need_s", 1.0)):
                new_state = rec["target"]
                rec = {**rec, "dwell_met": True}
                pend_since = None
        else:
            pend_since = None
        if new_state != state:
            rec.update({"t": t, "to": new_state})
            state = new_state
        m = margins[-1] if isinstance(margins, list) and margins else {}
        advice = None
        if state in ("S2", "S3", "S4"):
            advice = plan_disposal(state, m, mission_context)
        yield {"t": t, "state": state, "transition": rec if new_state else None,
               "advice": advice}
