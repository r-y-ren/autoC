"""四类残差通道（惯导创新/姿态跟踪/转速-电流/遥测丢包）（run_sudden_fault 块）。"""
from __future__ import annotations

import math

_CHANNEL_Z = {"pos_vel_innov": 0.0, "att_track": 0.0, "motor_consistency": 0.0, "telem_loss": 0.0}


def build_residuals(frames, raw_telemetry=None):
    """帧序列（取最新帧+近期序列）→ 归一残差通道 dict；缺源通道置 NaN（掩码语义）。"""
    out = {k: math.nan for k in _CHANNEL_Z}
    if not frames:
        return out
    f, hist = frames[-1], frames[-40:]
    # 惯导创新代理：GNSS 位移速度 vs 本地速度模差（两源对运动速度的分歧）
    if f.get("vx") is not None and f.get("lat") is not None and len(hist) >= 5:
        pts = [(h["t"], h["lat"], h.get("lon")) for h in hist[-20:]
               if h.get("lat") is not None and h.get("lon") is not None]
        if len(pts) >= 5 and pts[-1][0] > pts[0][0]:
            dt = pts[-1][0] - pts[0][0]
            dx = (pts[-1][1] - pts[0][1]) * 111320            # 纬度差不乘 cos（cos 只属经度）
            dy = (pts[-1][2] - pts[0][2]) * 111320 * math.cos(math.radians(f["lat"]))
            v_gps = math.hypot(dx / dt, dy / dt)
            v_loc = math.hypot(f.get("vx") or 0, f.get("vy") or 0)
            out["pos_vel_innov"] = min(abs(v_gps - v_loc) / 6.0, 3.0)
    # 姿态跟踪残差代理：巡航期望近悬停，|roll|+|pitch| 超基线的幅度
    if f.get("roll") is not None:
        base = [abs(h.get("roll") or 0) + abs(h.get("pitch") or 0) for h in hist]
        base_avg = sum(base) / len(base) if base else 0.0
        cur = abs(f["roll"]) + abs(f.get("pitch") or 0)
        out["att_track"] = min(max(0.0, (cur - base_avg - 0.08)) / 0.35, 3.0)
    # 转速-电流一致性：合成/真实电机数据缺→NaN（掩码，不参与 CUSUM）
    if f.get("motor_rpm") is not None and f.get("motor_current") is not None:
        exp_i = 0.5 + 0.002 * f["motor_rpm"]
        out["motor_consistency"] = min(abs(f["motor_current"] - exp_i) / 3.0, 3.0)
    # 遥测丢包：本拍 gap 标志的滑窗占比
    gaps = [1 for h in hist if (h.get("telem_gaps") or [False])[0]]
    if hist:
        out["telem_loss"] = min(len(gaps) / max(1, len(hist)) / 0.25, 3.0)
    return out
