# -*- coding: utf-8 -*-
"""run_r37_iteration（R19/R20 L0）：编排。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
build_r37 产 r37 合一件（白名单三件：守卫块/羊时序/尾盘修剪）→
judge_cash_guard_replay（6 灾难局+10 胜局对照重演）+ judge_sheep_league
（300-500 局联赛）→ verify_r37_gates fail-closed 全跑 → 判决+门禁全绿
交发射（standing 代执行+台账留痕，Error 即停）；任一红即停不发射。
evidence 三件（build 审计/replay 判决/联赛判决）+门禁台账。
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

EVIDENCE_DIR = os.path.join(HERE, "evidence")


def run_r37_iteration() -> Dict[str, Any]:
    """编排：构建→判决两件→门禁→发射裁决；evidence 三件+台账。

    签名意图：输入: 无（CLI） / 输出: {build, judgments, gates, verdict} /
    错误: fail-closed（任一红即停不发射）。
    """
    raise NotImplementedError("unimplemented:fn:run_r37_iteration")
