# -*- coding: utf-8 -*-
"""verify_r37_gates（R19/R20 L1）：全量门禁 fail-closed。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
四门沿 r30 管线（合规四轴核查/装载 last-callable=_r37_agent/双席 DONE+
单步<1s/确定性双跑/体积身份链）+ h2h vs r34a 在飞件 ≥0.55（seated 双席位、
独立局数 n 报，席位翻转不双计）+ 饿死零容忍 + 谱系（v48/v4b 各 8 局无负）；
evidence 落 evidence/。
"""
from __future__ import annotations

from typing import Any, Dict


def verify_r37_gates(pkg_path: str) -> Dict[str, Any]:
    """全量门禁 fail-closed 全跑不短路。

    签名意图：输入: r37 包 / 输出: 各门结果+overall / 错误: fail-closed。
    """
    raise NotImplementedError("unimplemented:fn:verify_r37_gates")
