"""normalize_telemetry 单测。"""
from __future__ import annotations

from conftest import make_msg


def test_full_batch_core_fields_ok():
    from run_ingest.normalize_telemetry import normalize_telemetry
    batch = [
        make_msg("HEARTBEAT", custom_mode=4, base_mode=209),
        make_msg("ATTITUDE", roll=0.1, pitch=-0.05, yaw=1.0, rollspeed=0.2, pitchspeed=0.1, yawspeed=-0.1),
        make_msg("SYS_STATUS", voltage_battery=14800, current_battery=1500, battery_remaining=80),
        make_msg("GPS_RAW_INT", fix_type=6, satellites_visible=14, eph=80),
        make_msg("GLOBAL_POSITION_INT", lat=320000000, lon=1188000000, alt=50000),
        make_msg("RADIO_STATUS", rssi=100, remrssi=95, txbuf=80),
    ]
    f = normalize_telemetry(batch, now=1.0)
    m = f["quality_mask"]
    assert f["voltage"] == 14.8 and m["voltage"] == 1
    assert f["hdop"] == 0.8 and m["hdop"] == 1
    assert f["battery_remaining"] == 80 and m["battery_remaining"] == 1
    assert abs(f["rssi"] - (-75.26)) < 0.5


def test_missing_and_out_of_bounds():
    from run_ingest.normalize_telemetry import normalize_telemetry
    f = normalize_telemetry([make_msg("SYS_STATUS", voltage_battery=99000,
                                      current_battery=0, battery_remaining=80)], now=0.5)
    assert f["voltage"] == 99.0 and f["quality_mask"]["voltage"] == 0  # 越界降质
    assert f.get("roll") is None  # 缺失不造数


def test_carry_forward_with_freshness():
    from run_ingest.normalize_telemetry import normalize_telemetry
    state = {}
    normalize_telemetry([make_msg("ATTITUDE", roll=0.1, pitch=0, yaw=0,
                                  rollspeed=0, pitchspeed=0, yawspeed=0)], state, now=0.0)
    f2 = normalize_telemetry([], state, now=1.0)   # 本拍无消息→携带，新鲜
    assert f2["roll"] == 0.1 and f2["quality_mask"]["roll"] == 1
    f3 = normalize_telemetry([], state, now=10.0)  # 超龄→降质
    assert f3["roll"] == 0.1 and f3["quality_mask"]["roll"] == 0


def test_cross_source_displacement_divergence():
    from run_ingest.normalize_telemetry import normalize_telemetry
    state = {}
    # 两拍：GNSS 说移动 ~111m，本地 NED 说没动 → 分歧>80m → lat/lon 降质
    normalize_telemetry([
        make_msg("GLOBAL_POSITION_INT", lat=320000000, lon=1188000000, alt=0),
        make_msg("LOCAL_POSITION_NED", x=0, y=0, z=0, vx=0, vy=0, vz=0)], state, now=0)
    f = normalize_telemetry([
        make_msg("GLOBAL_POSITION_INT", lat=321000000, lon=1188000000, alt=0),
        make_msg("LOCAL_POSITION_NED", x=0, y=0, z=0, vx=0, vy=0, vz=0)], state, now=0.05)
    assert f["quality_mask"]["lat"] == 0
