"""DUT 串口链路：解析串口 JSON 行（契约见 contracts/sw-hw-interface.md）。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DutSample:
    link: str            # "wifi" | "nrf24"
    seq: int
    ts_ms: int
    per: float
    tx_n: int
    err_n: int
    rssi_dbm: float | None = None    # 仅 wifi
    arc_avg: float | None = None     # 仅 nrf24
    plos_cnt: int | None = None      # 仅 nrf24
    fw: str = ""


def parse_dut_line(raw: bytes) -> DutSample:
    """一行 JSON → DutSample；字段缺失/seq 回退跳变 → 抛 ValueError（上层记 gap 事件）。"""
    raise NotImplementedError("unimplemented:fn:parse_dut_line")


def open_links(ports: dict[str, str]) -> dict:
    """按 {link: 串口名} 打开串口（115200 8N1）；打不开 → 抛 OSError。"""
    raise NotImplementedError("unimplemented:fn:open_links")
