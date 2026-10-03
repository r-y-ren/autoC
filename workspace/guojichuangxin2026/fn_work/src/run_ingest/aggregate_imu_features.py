"""短窗口高频 IMU→RMS/峰值/频带能量/偏置变化（run_ingest 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def aggregate_imu_features(samples: list, window: dict):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:aggregate_imu_features")
