# -*- coding: utf-8 -*-
"""run_r38_iteration（R21 L0）：编排。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
build_sellflow_library 建库 → build_r38 产 r38 件 → judge_predict_replay
判决（26 败局[晚崩 15 局重点]+10 胜局对照+闭环副证）→ 判正才
verify_r38_gates 五门 → 全绿交发射（standing 台账）；判负→收档不建发射版。
evidence 四件+台账。
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


def run_r38_iteration() -> Dict[str, Any]:
    """编排：建库→构建→判决→（判正才）门禁→发射裁决；evidence 四件+台账。

    签名意图：输入: 无（CLI） / 输出: {library, build, judgment, gates, verdict} /
    错误: fail-closed。
    """
    raise NotImplementedError("unimplemented:fn:run_r38_iteration")
