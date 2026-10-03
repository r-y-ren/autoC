"""R10 顶层：SITL 链路退化注入（安航云盾联动：实测 PER-功率台阶 → ArduPilot SITL）。"""

from __future__ import annotations


def inject_profile(run_dir: str, sitl_host: str = "127.0.0.1:5760") -> None:
    """读 run 的 PER 台阶 → pymavlink 注入 SITL 链路丢包/时延；产出联调记录入 run 目录。"""
    raise NotImplementedError("unimplemented:fn:inject_profile")
