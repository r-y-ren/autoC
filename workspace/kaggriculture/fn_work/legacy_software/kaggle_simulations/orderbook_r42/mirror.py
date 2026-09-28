# -*- coding: utf-8 -*-
"""apply_mirror_gate（R25 P3 镜像门控）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：双方公开农场指纹
相等→卖窗提前 2 拍+credit 等额扣减（禁净加卖）；只用公开面不做对手行为预测；
指纹缺失→门不触发；异常→零动作。
"""
from __future__ import annotations

from typing import Any, Dict


def apply_mirror_gate(observation: Dict[str, Any],
                      action: Dict[str, Any]) -> Dict[str, Any]:
    """镜像门控。签名意图：输入: observation, action / 输出: action+credit
    账本 / 错误: 异常→零动作（原样）。"""
    raise NotImplementedError("unimplemented:fn:apply_mirror_gate")
