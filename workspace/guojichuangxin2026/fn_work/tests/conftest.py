"""fn_work 测试引导：把 fn_work/src 插入 sys.path。"""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ---- 测试共用工厂（B2 起）----
import math as _math
import types as _types

import pytest as _pytest


def make_msg(mtype, **kw):
    """构造 duck-typed MAVLink 消息。"""
    return _types.SimpleNamespace(get_type=lambda m=mtype: m, **kw)


def make_imu(t, i):
    a = 9.8 + 0.5 * _math.sin(2 * _math.pi * 20 * t) + (2.0 if i % 97 == 0 else 0)
    return (t, 0.01 * _math.sin(t), 0.01, 0.01, a, 0.0, 9.8)


class FakeSitlConn:
    """合成 SITL 源：预生成消息时间线，每拍泄出 ≤per_tick 条（20Hz 帧消费）。"""

    def __init__(self, duration_s=2.0):
        msgs, t, i = [], 0.0, 0
        while t <= duration_s:
            msgs.append((t, make_msg("ATTITUDE", roll=0.05 * _math.sin(t), pitch=0.0,
                                     yaw=1.2, rollspeed=0.1, pitchspeed=0.0, yawspeed=0.0)))
            imu = make_imu(t, i)
            msgs.append((t, make_msg("RAW_IMU", xg=imu[1], yg=imu[2], zg=imu[3],
                                     xac=imu[4], yac=imu[5], zac=imu[6])))
            msgs.append((t, make_msg("LOCAL_POSITION_NED", x=10 * t, y=0.0, z=-30,
                                     vx=10.0, vy=0.0, vz=0.0)))
            if i % 2 == 0:
                msgs.append((t, make_msg("GLOBAL_POSITION_INT", lat=int((32.0 + 0.0001 * t) * 1e7),
                                         lon=int(118.8 * 1e7), alt=int(50 * 1e3))))
            if i % 4 == 0:
                msgs.append((t, make_msg("GPS_RAW_INT", fix_type=6, satellites_visible=14,
                                         eph=90)))
            if i % 10 == 0:
                drain = max(0.2, 1.0 - 0.25 * t)  # 电量缓降（场景一语义）
                msgs.append((t, make_msg("SYS_STATUS", voltage_battery=int(14800 * (0.5 + drain / 2)),
                                         current_battery=1800, battery_remaining=int(90 * drain))))
            if i % 20 == 0:
                msgs.append((t, make_msg("RADIO_STATUS", rssi=110, remrssi=105, txbuf=90)))
            if i == 0:
                msgs.append((t, make_msg("HEARTBEAT", custom_mode=4, base_mode=209)))
            msgs[-1][1]._timestamp = t
            t += 1.0 / 50.0
            i += 1
        self._msgs = msgs
        self._cursor = 0
        self._budget = 8
        self._served_eof_once = False

    def recv_match(self, blocking=False, **kw):
        if kw.get("type") == "HEARTBEAT" and blocking:
            return make_msg("HEARTBEAT", custom_mode=4, base_mode=209)
        if self._budget <= 0:
            self._budget = 8  # 下一拍预算重置
            return None
        if self._cursor >= len(self._msgs):
            if not self._served_eof_once:
                self._served_eof_once = True
                self._budget = 0
                return None
            return None
        t, m = self._msgs[self._cursor]
        self._cursor += 1
        self._budget -= 1
        return m

    def close(self):
        pass


@_pytest.fixture
def msg_factory():
    return make_msg


@_pytest.fixture
def fake_sitl_factory():
    return FakeSitlConn
