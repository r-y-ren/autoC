"""四类残差通道（惯导创新/姿态跟踪/转速-电流/遥测丢包）（run_sudden_fault 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def build_residuals(frames, raw_telemetry):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:build_residuals")
