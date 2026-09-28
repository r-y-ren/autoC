# -*- coding: utf-8 -*-
"""apply_endgame_liquidation（R25 P2 终日清算器）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：step≥648 切换清算
模式（停 BUY 类、仓内可卖品按 −price×qty 降序出清）；steps 712-718 七拍显式
清算序；终拍滞留归零目标；异常→原动作。
"""
from __future__ import annotations

from typing import Any, Dict


def apply_endgame_liquidation(observation: Dict[str, Any],
                              action: Dict[str, Any]) -> Dict[str, Any]:
    """终日清算器。签名意图：输入: observation, action / 输出: action（替换
    market 段）+清算账本 / 错误: 异常→原动作。"""
    raise NotImplementedError("unimplemented:fn:apply_endgame_liquidation")
