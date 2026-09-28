# -*- coding: utf-8 -*-
"""judge_r26 及判决面子件（R26）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：仪器四件套内置——
安慰剂臂（纯重编码件 vs r40 恒等）→单件消融（三组件各单独件，逐件效应>0
才保留）→全件配对联赛（r43 vs r40 同 seed 双席 traced）；分项=实现价 ≥0.88
∧ 终局钱 ≥10.5 万/局 ∧ stranding≈0；总判=h2h ≥0.55；聚合 evidence。
"""
from __future__ import annotations

from typing import Any, Dict


def judge_r26(package: Any, corpus: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """判决 v26（安慰剂+消融+配对，分项+总判）。签名意图：输入: r43 包+
    语料+配置 / 输出: evidence JSON / 错误: 单局红计入不短路。"""
    raise NotImplementedError("unimplemented:fn:judge_r26")


def realized_price_stats(states: Any) -> Dict[str, Any]:
    """实现价读数（逐局逐席）。签名意图：输入: traced 对局 / 输出:
    {realized_px, terminal_money, stranding} / 错误: 缺字段→UNKNOWN。"""
    raise NotImplementedError("unimplemented:fn:realized_price_stats")
