"""run_safety_state_machine 主循环单测（迁移+迟滞+dwell 累计）。"""
from __future__ import annotations

CFG = {"hysteresis": 0.05, "dwell_s": {"S1": 2.0, "S2": 2.0, "S3": 1.0, "S4": 0.0}}
CTX = {"position": (32.0, 118.8), "home": (32.001, 118.8), "battery_remaining": 80,
       "gps_ok": True, "link_ok": True, "alternates": []}


def _events():
    # 正常 5s → 渐进严重度2 持续 3s（过 dwell 2s）→ 突发电机故障
    evs = [{"type": "progressive", "severity": 0, "t": i * 0.5, "evidence": {}} for i in range(10)]
    evs += [{"type": "progressive", "severity": 2, "t": 5 + i * 0.5, "evidence": {"m": 1}}
            for i in range(7)]
    evs += [{"type": "sudden", "severity": 4, "t": 9.0, "fault": "电机异常"}]
    return evs


def test_trajectory_and_advice():
    from run_safety_state_machine.run_safety_state_machine import run_safety_state_machine
    outs = list(run_safety_state_machine(_events(), [{"energy": {"norm": 0.5}}], CTX, CFG))
    states = [o["state"] for o in outs]
    assert states[0] == "S0"
    assert "S2" in states                          # dwell 满足后升级
    assert states[-1] == "S4"                      # 突发直达
    advised = [o for o in outs if o["advice"]]
    assert advised and advised[-1]["advice"]["action"] in ("返航", "备降点1", "原地安全降落")


def test_flap_absorbed_by_hysteresis():
    from run_safety_state_machine.run_safety_state_machine import run_safety_state_machine
    evs = []
    for i in range(40):
        sev = 2 if i % 2 == 0 else 0                # 分值抖动 0/2
        evs.append({"type": "progressive", "severity": sev, "t": i * 0.25,
                    "evidence": {}})
    outs = list(run_safety_state_machine(evs, [], CTX, CFG))
    ups = sum(1 for a, b in zip(outs, outs[1:]) if a["state"] != b["state"])
    assert ups <= 4                                 # 抖动不产生反复横跳
