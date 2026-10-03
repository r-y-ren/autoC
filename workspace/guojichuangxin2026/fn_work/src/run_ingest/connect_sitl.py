"""建立 MAVLink 连接并等到心跳就绪（run_ingest 块）。"""
from __future__ import annotations

_STREAMS = (30, 32, 33, 24, 27, 147, 1)  # ATTITUDE/LOCAL_POS/GLOBAL_POS/GPS_RAW/RAW_IMU/BATTERY/SYS_STATUS


def connect_sitl(endpoint: str, timeout: float = 10.0):
    """endpoint 例：udp:127.0.0.1:14560 / tcp:... / /dev/ttyUSB0；带超时与一次重试。

    返回连接对象（附着心跳元数据 hb_sysid/hb_compid）；两轮均失败抛 ConnectionError。
    """
    from pymavlink import mavutil

    last_err: Exception | None = None
    for _attempt in (1, 2):
        conn = None
        try:
            conn = mavutil.mavlink_connection(endpoint, source_system=221, source_component=1)
            hb = conn.recv_match(type="HEARTBEAT", blocking=True, timeout=timeout)
            if hb is None:
                raise TimeoutError(f"{endpoint} {timeout}s 内无心跳")
            conn.hb_sysid, conn.hb_compid = conn.target_system, conn.target_component
            for sid in _STREAMS:
                conn.mav.request_data_stream_send(
                    conn.target_system, conn.target_component, sid, 20, 1)
            return conn
        except Exception as exc:  # 连接层与超时统一走重试
            last_err = exc
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    raise ConnectionError(f"SITL 连接失败（已重试一次）: {endpoint}: {last_err}")
