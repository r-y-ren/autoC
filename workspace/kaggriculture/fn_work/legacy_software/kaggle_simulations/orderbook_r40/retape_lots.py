# -*- coding: utf-8 -*-
"""retape_sell_lots（R23 L2）：卖单批量化手术。

责任契约：d21-28 晚季窗磁带 SELL 单合并放大（少而大，目标批量化率对标
胜局对手 ~337 单级）；只动卖单量/槽、不动物品总量（卖出守恒）；越窗/守恒破
→抛；变更表 kind=sell_lots。
"""
from __future__ import annotations

from typing import Any, Dict


def retape_sell_lots(tape_routes: Dict[str, Any],
                     params: Any = None) -> Dict[str, Any]:
    """卖单批量化手术+卖出守恒核算。

    签名意图：输入: 磁带路由表+批量化参数 / 输出: {routes, change_table} /
    错误: 卖出守恒破即抛。
    """
    raise NotImplementedError("unimplemented:fn:retape_sell_lots")
