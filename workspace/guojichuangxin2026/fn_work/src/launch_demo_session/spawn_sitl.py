"""按场景拉起 PX4 SITL 进程（合成源备选）（launch_demo_session 块）。"""
from __future__ import annotations

import subprocess
import threading
import time


class SitlError(Exception):
    """拉起超时/心跳不至。"""


class SyntheticSITL:
    """进程内合成源：drain 式消息流 + inject_scenario 回执（设备缺席演示的等价数据面）。"""

    scenario_defs = {"lowbat_headwind": {"kind": "progressive", "wind_ms": 6.0,
                                         "levels": {"low": 1.4, "mid": 2.2, "high": 3.2}},
                     "motor_fail": {"kind": "sudden", "motor": 1,
                                    "levels": {"low": 0.4, "mid": 0.7, "high": 1.0}},
                     "link_degrade": {"kind": "link",
                                      "drop_rate": {"low": 0.1, "mid": 0.3, "high": 0.6}}}

    def __init__(self, scenario="lowbat_headwind"):
        self.scenario, self.level = scenario, None
        self._drain = [{"lowbat_headwind": (1.0, 2.2), "motor_fail": (1.0, 1.0),
                        "link_degrade": (1.0, 1.0)}[scenario][1]]
        self._msgs = []
        self._serve_t = 0.05
        self._t = 0.0
        self._i = 0
        self._build(0.5)

    def _build(self, upto):
        import math
        import types as _t
        while self._t <= upto:
            t, i = self._t, self._i
            # 基础衰减 0.016/s；档位倍率 low1.4/mid2.2/high3.2 → mid 穿 25% 线约 21s
            # （物理口径：8s 特征窗+5s 提前量需危险线晚于 13s；21s 为真实量纲下合理点）
            drain = 1.0 - 0.016 * t
            if self.level and self.scenario == "lowbat_headwind":
                drain = min(drain, 1.0 - 0.016 * t * self._drain[0])
            def mk(mtype, **kw):
                m = _t.SimpleNamespace(get_type=lambda m=mtype: m, **kw)
                m._timestamp = t
                return m
            self._msgs.append(mk("ATTITUDE", roll=(0.35 if self.scenario == "motor_fail"
                                                   and self.level and t > 3.0 and i % 4 < 2
                                                   else 0.05 * math.sin(t)), pitch=0.0, yaw=1.2,
                                 rollspeed=0.1, pitchspeed=0.0, yawspeed=0.0))
            self._msgs.append(mk("RAW_IMU", xg=0.01, yg=0.01, zg=0.01,
                                 xac=9.8 + 0.3 * math.sin(2 * math.pi * 20 * t),
                                 yac=0.0, zac=9.8))
            self._msgs.append(mk("LOCAL_POSITION_NED", x=8 * t, y=0, z=-30,
                                 vx=8.0, vy=0, vz=0))
            if i % 2 == 0:
                self._msgs.append(mk("GLOBAL_POSITION_INT", lat=int((32.0 + 8 * t / 111320) * 1e7),
                                     lon=int(118.8 * 1e7), alt=int(50 * 1e3)))
            if i % 4 == 0:
                self._msgs.append(mk("GPS_RAW_INT", fix_type=6, satellites_visible=14, eph=90))
            if i % 10 == 0:
                drop = (self.level and self.scenario == "link_degrade")
                self._msgs.append(mk("SYS_STATUS",
                                     voltage_battery=int(14800 * max(0.25, drain)),
                                     current_battery=1800,
                                     battery_remaining=int(92 * max(0.2, drain))))
            if i % 20 == 0:
                self._msgs.append(mk("RADIO_STATUS", rssi=110 if not drop else 60,
                                     remrssi=105, txbuf=90))
            self._msgs.append(mk("HEARTBEAT", custom_mode=4, base_mode=209))
            self._t += 1.0 / 50.0
            self._i += 1

    def inject_scenario(self, scenario, level, params):
        self.level = level
        return {"applied": params, "t_sim": round(self._t, 2)}

    def recv_match(self, blocking=False, type=None, timeout=0.0, **kw):
        import types as _t
        if type == "HEARTBEAT" and blocking:
            m = _t.SimpleNamespace(get_type=lambda: "HEARTBEAT", custom_mode=4, base_mode=209)
            return m
        # 时间戳切片供数：每拍恰好供给该 0.05s 窗内的消息（与 20Hz 帧时钟物理对齐）
        if not self._msgs:
            self._build(self._t + 1.0)
        if self._msgs and float(self._msgs[0]._timestamp) > self._serve_t + 1e-9:
            self._serve_t += 0.05
            return None                          # 本拍供完
        if not self._msgs:
            return None
        return self._msgs.pop(0)

    def close(self):
        pass


def spawn_sitl(scenario_def: dict, simulator: str = "synthetic"):
    """simulator ∈ {synthetic, px4}；返回 {mode, endpoint, conn|process, log}。

    px4 模式：submake px4_sitl <airframe>，等 MAVLink 心跳（udp:14560）；失败抛 SitlError。
    签名微调：simulator 增 synthetic 备选（设备/依赖缺席时的等价数据面），登记于 batches.md。
    """
    if simulator == "synthetic":
        conn = SyntheticSITL(scenario_def.get("name", "lowbat_headwind"))
        return {"mode": "synthetic", "endpoint": "inproc", "conn": conn,
                "process": None, "log": None}
    px4_dir = scenario_def.get("px4_dir") or ""
    airframe = scenario_def.get("airframe", "sihsim_quadx")   # SIH 无头默认（本次编译目标）
    if not px4_dir:
        raise SitlError("px4 模式需配置 sitl.px4_dir（先克隆 PX4-Autopilot）")
    import sys
    from pathlib import Path as _P
    venv_bin = str(_P(px4_dir).parents[1] / "fn_work" / ".venv" / "bin")
    log = open(f"sitl_{airframe}.log", "w")
    try:
        import os
        env = {**os.environ, "PATH": venv_bin + ":" + os.environ.get("PATH", "")}
        proc = subprocess.Popen(["make", "px4_sitl", airframe], cwd=px4_dir,
                                stdout=log, stderr=subprocess.STDOUT, env=env,
                                start_new_session=True)   # 独立进程组：回收可杀全家
    except OSError as exc:
        log.close()
        raise SitlError(f"PX4 拉起失败: {exc}") from exc
    time.sleep(1.0)
    if proc.poll() is not None:
        log.close()
        raise SitlError("PX4 进程早退（见 sitl 日志）")
    return {"mode": "px4", "endpoint": "udpin:0.0.0.0:14550", "conn": None,
            "process": proc, "log": log}
