"""按场景定义注入故障（电池/风/电机/链路，含回执记录）（shared 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def inject_scenario_fault(conn, scenario: str, level: str, timing: dict):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:inject_scenario_fault")
