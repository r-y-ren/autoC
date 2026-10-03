"""统一数据接入主循环：建链收流、归一、IMU 特征、物理余量、落盘（run_ingest 块）。"""
from __future__ import annotations

import json
import time
from pathlib import Path


class IngestError(Exception):
    """连接失败/持续超时；部分数据已落盘。"""


def run_ingest(config: dict, run_dir, stop_condition=None, conn=None, realtime: bool = False):
    """生成 20Hz 统一状态帧的生成器；帧与原始遥测全量落运行目录。

    config: run{hz,endpoint,duration_s,home,wind_ms}; run_dir: open_run_dir 产物。
    conn 可注入（测试/复用）；None 时 connect_sitl。realtime=True 按墙钟节拍（演示用）。
    签名微调：conn/realtime 可选参，登记于 batches.md。
    """
    from run_ingest.aggregate_imu_features import aggregate_imu_features
    from run_ingest.compute_physical_margins import compute_physical_margins
    from run_ingest.connect_sitl import connect_sitl
    from run_ingest.normalize_telemetry import normalize_telemetry

    hz = int(config.get("run", {}).get("hz", 20))
    duration = float(config.get("run", {}).get("duration_s", 60))
    home = config.get("run", {}).get("home")
    wind = float(config.get("run", {}).get("wind_ms", 0.0))
    owned = False
    if conn is None:
        try:
            conn = connect_sitl(config.get("run", {}).get("endpoint", "udp:127.0.0.1:14560"))
        except Exception as exc:
            raise IngestError(f"接入建链失败: {exc}") from exc
        owned = True
    rd = Path(run_dir)
    (rd / "raw").mkdir(exist_ok=True)
    (rd / "frames").mkdir(exist_ok=True)
    raw_fh = open(rd / "raw" / "raw.jsonl", "a", encoding="utf-8")
    frame_fh = open(rd / "frames" / "frames.jsonl", "a", encoding="utf-8")
    state, imu_buf, frames_hist, n = {}, [], [], 0
    tick, t_sim = 1.0 / hz, 0.0
    last_wall = time.monotonic()
    try:
        while t_sim <= duration:
            # 排空当前可读消息
            batch = []
            while True:
                msg = conn.recv_match(blocking=False)
                if msg is None:
                    break
                batch.append(msg)
                ts = getattr(msg, "_timestamp", None)
                raw_fh.write(json.dumps({"type": msg.get_type(),
                                         "t": float(ts) if ts else t_sim}) + "\n")
                if msg.get_type() == "RAW_IMU":
                    ts_imu = getattr(msg, "_timestamp", None)
                    imu_buf.append((float(ts_imu) if ts_imu else t_sim,
                                    getattr(msg, "xg", 0), getattr(msg, "yg", 0),
                                    getattr(msg, "zg", 0), getattr(msg, "xac", 0),
                                    getattr(msg, "yac", 0), getattr(msg, "zac", 0)))
            frame = normalize_telemetry(batch, state, now=round(t_sim, 3))
            # 遥测到达间隔异常（链路余量用）：本拍消息量骤降视为 gap
            expected = max(1, hz // 4)
            frame["telem_gaps"] = [len(batch) < expected // 2]
            imu_buf = [s for s in imu_buf if t_sim - s[0] <= 1.0]
            frame.update(aggregate_imu_features(imu_buf))
            margins = compute_physical_margins(frames_hist + [frame], home, wind)
            frame["margins"] = margins
            frame_fh.write(json.dumps(frame, ensure_ascii=False) + "\n")
            frames_hist.append(frame)
            frames_hist = frames_hist[-40:]
            n += 1
            yield frame
            if stop_condition is not None and stop_condition(n, frame):
                break
            t_sim += tick
            if realtime:
                target = last_wall + tick
                sleep = target - time.monotonic()
                if sleep > 0:
                    time.sleep(sleep)
                last_wall = target
        else:
            pass
    except GeneratorExit:
        pass
    finally:
        raw_fh.close(); frame_fh.close()
        if owned:
            try:
                conn.close()
            except Exception:
                pass
