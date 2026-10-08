"""render_device_panel 单测。"""
from __future__ import annotations

from shared.render_device_panel import render_device_panel

REPORT = {
    "devices": [
        {"name": "合成仿真源", "state": "active", "note": "内置"},
        {"name": "USRP B210 频谱站", "state": "replay", "note": "uhd 缺席→回放"},
        {"name": "Jetson Orin NX", "state": "pending", "note": "脚本就绪"},
    ],
    "pending": [{"name": "真机实飞", "status": "待导师批", "note": "档 C"}],
}


def test_two_zones_and_badges():
    html = render_device_panel(REPORT)
    assert "已接设备" in html and "待接入清单" in html
    assert "b-ok" in html and "回放降级" in html and "待设备" in html
    assert "USRP B210" in html and "真机实飞" in html and "档 C" in html
    assert html.count("<table") == 2


def test_empty_report_and_unknown_state():
    html = render_device_panel({})
    assert "无设备报告" in html and "无待接入项" in html
    html2 = render_device_panel({"devices": [{"name": "x", "state": "weird"}]})
    assert "未知" in html2
