"""离线训练管线：样本生成（按架次分组防泄漏）→轻量 TCN checkpoint（run_progressive_risk 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def train_tcn(data_dirs: list, train_config: dict):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:train_tcn")
