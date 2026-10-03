"""render_console 单测。"""
from __future__ import annotations


def test_console_page_key_elements():
    from launch_demo_session.render_console import render_console
    html = render_console({})
    for needle in ("注入故障", "演示控制台", "waterfall", "事件时间轴", "回放",
                   "scenario", "input type='range'"):
        assert needle in html, needle
