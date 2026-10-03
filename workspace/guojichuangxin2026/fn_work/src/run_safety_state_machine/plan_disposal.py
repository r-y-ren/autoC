"""三方案（返航/备降/原地降落）能源校验→建议+明细（run_safety_state_machine 块）。"""
from __future__ import annotations

import math

_RANGE_M = 9000.0


def _dist(a, b):
    return math.hypot((a[0] - b[0]) * 111320 * math.cos(math.radians(a[0])),
                      (a[1] - b[1]) * 111320)


def plan_disposal(state, margins, mission_context):
    """mission_context: {home, alternates: [(lat,lon,cond)], geofence, wind_ms, battery_remaining, position, gps_ok, link_ok}。

    低电量+逆风：返航须能源高于保留裕量；GNSS+链路双退化：禁依赖远程连续控制的策略。
    返回 {action, reason, options: [{name, ok, why, energy_need_pct}]}。
    """
    mc = mission_context or {}
    pos = mc.get("position")
    home = mc.get("home")
    batt = mc.get("battery_remaining")
    wind = float(mc.get("wind_ms", 0.0))
    gps_ok, link_ok = mc.get("gps_ok", True), mc.get("link_ok", True)
    options = []

    def need_pct(dist_m):
        return (dist_m / _RANGE_M * 100.0) * (1.0 + 0.015 * max(0.0, wind)) + 10.0

    if pos and home and batt is not None:
        d_home = _dist(pos, home)
        rtl_need = need_pct(d_home)
        ok = batt >= rtl_need
        why = (f"返航能耗 {rtl_need:.0f}% vs 余量 {batt:.0f}%"
               + ("" if ok else "——低电量逆风下返航能源不足，禁止"))
        options.append({"name": "返航", "ok": ok, "why": why, "energy_need_pct": rtl_need})
    for i, alt in enumerate(mc.get("alternates") or []):
        d = _dist(pos, alt[:2]) if pos else 0.0
        n = need_pct(d)
        cond_ok = alt[2] if len(alt) > 2 else True
        options.append({"name": f"备降点{i+1}", "ok": batt >= n and cond_ok,
                        "why": f"能耗 {n:.0f}%（落点条件{'可' if cond_ok else '不可'}用）",
                        "energy_need_pct": n})
    land_ok = gps_ok or mc.get("position_known", True)
    options.append({"name": "原地安全降落", "ok": land_ok,
                    "why": "不依赖远程链路；GNSS 未知时为盲降（最后手段）",
                    "energy_need_pct": 2.0})
    # 远程依赖策略在双退化时剔除
    if not (gps_ok and link_ok):
        for o in options:
            if o["name"] == "返航" and not link_ok:
                o["ok"] = False
                o["why"] += "；链路退化禁依赖远程连续控制"
    feas = [o for o in options if o["ok"]]
    if not feas:
        action, reason = "原地安全降落（最后手段）", "无可行方案，执行保守降落"
    else:
        feas.sort(key=lambda o: (0 if o["name"] == "返航" else 1, o["energy_need_pct"]))
        action, reason = feas[0]["name"], f"能耗最优可行方案（{feas[0]['why']}）"
    return {"action": action, "reason": reason, "options": options,
            "state": state, "degraded_condition": {"gps": gps_ok, "link": link_ok}}
