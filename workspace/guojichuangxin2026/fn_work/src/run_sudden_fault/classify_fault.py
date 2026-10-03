"""轻量分类器判故障来源（电机/电调/链路瞬断/未知）（run_sudden_fault 块，规约见 fn_docs/responsibility.md）。"""
from __future__ import annotations


def classify_fault(features, classifier):
    """桩：签名与意图见责任文档。"""
    raise NotImplementedError("unimplemented:fn:classify_fault")
