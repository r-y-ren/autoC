"""原始 MAVLink 消息批→StateFrame（含质量掩码，不插值）（run_ingest 块）。"""
from __future__ import annotations

import math

# 取值域（越界→mask 0）：物理量纲护栏
_BOUNDS = {
    "voltage": (3.0, 34.0), "battery_remaining": (0.0, 100.0), "current": (-5.0, 90.0),
    "hdop": (0.0, 20.0), "sat_count": (0, 60), "rssi": (-120.0, 0.0),
    "roll": (-math.pi, math.pi), "pitch": (-math.pi, math.pi),
    "alt_amsl": (-500.0, 9000.0), "vx": (-60.0, 60.0), "vy": (-60.0, 60.0), "vz": (-30.0, 30.0),
}
_MAX_AGE_S = 2.0
_CROSS_POS_M = 80.0  # GNSS 与本地位置水平差超此值→双源降质


def _get(msg, name):
    return getattr(msg, name, None)


def _put(frame, mask, state, key, value, t, bounds_ok=True):
    if value is None:
        frame[key], mask[key] = None, 0
        return
    ok = bounds_ok
    if key in _BOUNDS:
        lo, hi = _BOUNDS[key]
        try:
            ok = ok and lo <= float(value) <= hi
        except (TypeError, ValueError):
            ok = False
    frame[key] = value
    mask[key] = 1 if ok else 0
    state["last_seen"][key] = t
    if value is not None:
        state["vals"][key] = value


def normalize_telemetry(messages: list, state: dict | None = None, now: float = 0.0) -> dict:
    """消息批（duck-typed：get_type()+属性）→ 20Hz 帧 dict（含 quality_mask）。

    签名微调：state/now 可选参（跨拍新鲜度与回放时间注入），登记于 batches.md。
    缺失字段 None+mask 0；绝不插值。
    """
    if state is None:
        state = {}
    state.setdefault("last_seen", {})
    state.setdefault("prev", {})
    state.setdefault("vals", {})
    frame: dict = {"t": now}
    mask: dict = {"t": 1}
    for msg in messages or []:
        mtype = msg.get_type() if hasattr(msg, "get_type") else getattr(msg, "_type", "?")
        if mtype == "HEARTBEAT":
            _put(frame, mask, state, "mode", getattr(msg, "custom_mode", None), now, True)
            armed = getattr(msg, "base_mode", 0)
            _put(frame, mask, state, "armed", bool(armed & 128), now, True)
        elif mtype == "ATTITUDE":
            for k in ("roll", "pitch", "yaw"):
                _put(frame, mask, state, k, _get(msg, k), now)
            for k in ("rollspeed", "pitchspeed", "yawspeed"):
                _put(frame, mask, state, k, _get(msg, k), now, True)
        elif mtype == "RAW_IMU":
            for ax_ in ("xg", "yg", "zg"):
                _put(frame, mask, state, f"g{ax_[0]}", _get(msg, ax_), now, True)
            for ax_ in ("xac", "yac", "zac"):
                _put(frame, mask, state, f"a{ax_[0]}", _get(msg, ax_), now, True)
        elif mtype == "LOCAL_POSITION_NED":
            _put(frame, mask, state, "vx", _get(msg, "vx"), now)
            _put(frame, mask, state, "vy", _get(msg, "vy"), now)
            _put(frame, mask, state, "vz", _get(msg, "vz"), now)
            state["local_xy"] = (_get(msg, "x"), _get(msg, "y"))
        elif mtype == "GLOBAL_POSITION_INT":
            lat = _get(msg, "lat"); lon = _get(msg, "lon")
            _put(frame, mask, state, "lat",
                 lat / 1e7 if isinstance(lat, (int, float)) else None, now, True)
            _put(frame, mask, state, "lon",
                 lon / 1e7 if isinstance(lon, (int, float)) else None, now, True)
            alt = _get(msg, "alt")
            _put(frame, mask, state, "alt_amsl", alt / 1e3 if isinstance(alt, (int, float)) else None, now)
            state["gps_xy"] = (frame.get("lat"), frame.get("lon"))
        elif mtype == "GPS_RAW_INT":
            _put(frame, mask, state, "gps_fix", _get(msg, "fix_type"), now, True)
            _put(frame, mask, state, "sat_count", _get(msg, "satellites_visible"), now)
            _put(frame, mask, state, "hdop", (lambda e: e / 100 if isinstance(e, (int, float)) else None)(_get(msg, "eph")), now)
        elif mtype in ("SYS_STATUS", "BATTERY_STATUS"):
            if mtype == "SYS_STATUS":
                _put(frame, mask, state, "voltage", (lambda v: v / 1000 if isinstance(v, (int, float)) else None)(_get(msg, "voltage_battery")), now)
                _put(frame, mask, state, "current", (lambda c: c / 100 if isinstance(c, (int, float)) else None)(_get(msg, "current_battery")), now)
                _put(frame, mask, state, "battery_remaining", _get(msg, "battery_remaining"), now)
            else:
                for src, dst in (("voltages", "voltage"), ("battery_remaining", "battery_remaining"), ("current_battery", "current")):
                    v = _get(msg, src)
                    if isinstance(v, list) and v:
                        v = v[0] / 1000 if dst == "voltage" else v
                    _put(frame, mask, state, dst, v, now)
        elif mtype in ("RADIO_STATUS", "RC_CHANNELS"):
            rssi_raw = _get(msg, "rssi")
            rssi = (rssi_raw / 1.94 - 127) if (mtype == "RADIO_STATUS" and isinstance(rssi_raw, (int, float))) else (rssi_raw / 2 - 100 if isinstance(rssi_raw, (int, float)) else None)
            _put(frame, mask, state, "rssi", rssi, now)
            remr = _get(msg, "remrssi")
            if isinstance(remr, (int, float)) and mtype == "RADIO_STATUS":
                _put(frame, mask, state, "rssi_remote", remr / 1.94 - 127, now, True)
        elif mtype == "STATUSTEXT":
            frame.setdefault("status_texts", []).append(str(_get(msg, "text") or ""))
    # 携带最近可信状态：本拍未更新的字段回填上一值，掩码按新鲜度定（不插值、不造数）
    for k, v in list(state["vals"].items()):
        if k not in frame and v is not None:
            age = now - state["last_seen"].get(k, now)
            frame[k] = v
            mask[k] = 1 if age <= _MAX_AGE_S else 0
    # 跨源一致性：GNSS 位移增量 vs 本地 NED 位移增量（坐标系不可直比，比移动量）
    gx, gy = state.get("gps_xy", (None, None))
    lx, ly = state.get("local_xy", (None, None))
    pg = state.get("gps_xy_prev"); pl = state.get("local_xy_prev")
    if None not in (gx, gy, lx, ly) and isinstance(pg, tuple) and isinstance(pl, tuple):
        d_gps = math.hypot((gx - pg[0]) * 111320,
                           (gy - pg[1]) * 111320 * math.cos(math.radians(gx)))
        d_loc = math.hypot(lx - pl[0], ly - pl[1])
        if abs(d_gps - d_loc) > _CROSS_POS_M:  # 两源对位移量的分歧超限→双降质
            mask["lat"] = mask["lon"] = 0
    if gx is not None and gy is not None:
        state["gps_xy_prev"] = (gx, gy)
    if lx is not None and ly is not None:
        state["local_xy_prev"] = (lx, ly)
    frame["quality_mask"] = mask
    return frame
