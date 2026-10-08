"""render_console 单测。"""
from __future__ import annotations


def test_console_page_key_elements():
    from launch_demo_session.render_console import render_console
    html = render_console({})
    for needle in ("注入故障", "演示控制台", "waterfall", "事件时间轴", "回放",
                   "scenario", "input type='range'"):
        assert needle in html, needle
    # R26 六区全覆盖：地图航迹/仪表组/色带/注入/设备面板/时间轴
    for zone in ("maptrack", "g-risk", "g-time", "g-energy", "band-s0",
                 "level", "device-panel", "events"):
        assert zone in html, zone


def test_r28_cards_readouts_flow():
    """R28 卡片化+飞行读数+一键流程元素。"""
    from launch_demo_session.render_console import render_console
    html = render_console({})
    for z in ("pickScn", "data-scn='lowbat_headwind'", "data-scn='motor_fail'",
              "g-alt", "g-speed", "flowStart", "flowPause", "一键演示"):
        assert z in html, z
