# -*- coding: utf-8 -*-
"""R23 运行时三件（注入包内）。

责任契约：_route40_select（step144 续段选择）/apply_race_slots（同回合
卖单竞速）/apply_slot_hygiene（队列补洞）。本文件源文本由 inject_r40_block
追加进包内（含内嵌续段库）。
"""
from __future__ import annotations

from typing import Any, Dict


def _route40_select(observation: Dict[str, Any], library: Any = None) -> Dict[str, Any]:
    """step144 续段选择：按当局开局长相族（前 144 步宏观指纹）查库选路线
    续段；无族命中→回退现行 _router 店对逻辑；只读选择不改磁带主体。

    签名意图：输入: observation+库 / 输出: {route, family, confidence} /
    错误: 库缺→回退默认路由。
    """
    raise NotImplementedError("unimplemented:fn:_route40_select")


def apply_race_slots(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """同回合卖单竞速：我方 SELL 单前移至市场表前部槽（对手挂单前成交；
    沿空槽位次语义+V57 资金序不变量）；只动 SELL 槽序。

    签名意图：输入: observation, action / 输出: 调整后 action /
    错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:apply_race_slots")


def apply_slot_hygiene(observation: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """队列补洞：识别零执行占坑单（上一拍挂出未成交）→清坑+后位有效单前移
    补洞（空槽位次语义不破坏）；只动自家市场单。

    签名意图：输入: observation, action / 输出: 调整后 action+补洞账 /
    错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:apply_slot_hygiene")
