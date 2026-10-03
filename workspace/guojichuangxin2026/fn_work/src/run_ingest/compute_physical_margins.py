"""四类物理余量（能源/导航/链路/控制，raw+归一双份）（run_ingest 块）。"""
from __future__ import annotations

import math

_RANGE_M = 9000.0        # 满电航程基准（可由 config 覆盖）
_RESERVE_PCT = 10.0
_W_PER_MS = 0.015        # 每米/秒逆风的能耗上浮


def _nan():
    return {"raw": math.nan, "norm": math.nan}


def _clamp01(x):
    return max(0.0, min(1.0, x)) if isinstance(x, float) and not math.isnan(x) else math.nan


def _home_dist_m(f, home):
    if home is None or f.get("lat") is None or f.get("lon") is None:
        return None
    hlat, hlon = home
    return math.hypot((f["lat"] - hlat) * 111320,
                      (f["lon"] - hlon) * 111320 * math.cos(math.radians(f["lat"])))


def compute_physical_margins(frames, home_position=None, wind_ms: float = 0.0,
                             consumption: dict | None = None) -> dict:
    """frames: 帧序列（取最新帧为主，序列用于控制余量的振动统计）。"""
    cons = consumption or {}
    rng = float(cons.get("range_m", _RANGE_M))
    out = {"energy": _nan(), "nav": _nan(), "link": _nan(), "control": _nan()}
    if not frames:
        return out
    f = frames[-1]
    # 能源：剩余% - 返航需求%（含逆风上浮）- 保留%
    dist = _home_dist_m(f, home_position)
    if dist is not None and f.get("battery_remaining") is not None:
        need = (dist / rng * 100.0) * (1.0 + _W_PER_MS * max(0.0, wind_ms))
        raw = float(f["battery_remaining"]) - need - _RESERVE_PCT
        out["energy"] = {"raw": raw, "norm": _clamp01((raw + 20.0) / 60.0)}
    # 导航：fix/sat/hdop 合成
    if f.get("gps_fix") is not None and f.get("hdop") is not None:
        fix_f = min(float(f["gps_fix"]) / 6.0, 1.0)
        sat_f = min((f.get("sat_count") or 0) / 12.0, 1.0)
        hdop_f = max(0.0, 1.0 - float(f["hdop"]) / 3.0)
        raw = fix_f * (0.5 + 0.5 * sat_f) * hdop_f
        out["nav"] = {"raw": raw, "norm": _clamp01(raw)}
    # 链路：RSSI 线性映射 + 丢包惩罚（取序列最近 1s 的间隔异常计数）
    if f.get("rssi") is not None:
        r = float(f["rssi"])
        raw = max(0.0, min(1.0, (r + 100.0) / 55.0))
        gaps = sum(1 for g in f.get("telem_gaps", []) if g)
        raw = max(0.0, raw - 0.05 * min(gaps, 5))
        out["link"] = {"raw": raw, "norm": _clamp01(raw)}
    # 控制：姿态速率幅值 + 振动（imu_rms 序列均值）合成（缺则 NaN）
    rates = [abs(x.get("rollspeed") or 0) + abs(x.get("pitchspeed") or 0)
             + abs(x.get("yawspeed") or 0) for x in frames[-20:] if x.get("rollspeed") is not None]
    vibes = [x.get("imu_rms") for x in frames[-20:] if x.get("imu_rms") == x.get("imu_rms")]
    if rates:
        rate_f = max(0.0, 1.0 - (sum(rates) / len(rates)) / 4.0)
        vib_f = max(0.0, 1.0 - (sum(vibes) / len(vibes)) / 12.0) if vibes else None
        raw = rate_f * (vib_f if vib_f is not None else 0.7)
        out["control"] = {"raw": raw, "norm": _clamp01(raw)}
    return out
