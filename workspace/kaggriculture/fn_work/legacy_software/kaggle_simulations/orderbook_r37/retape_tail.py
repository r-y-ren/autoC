# -*- coding: utf-8 -*-
"""retape_tail_savings（R20 L2）：磁带手术·尾盘负空间。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
d28（step 672）起删除 CARE 指令、d29（step 696）起删除 FEED 与闲置 HIRE
指令（省人工/饲料）；动物格 HARVEST（剪毛/收奶/收蛋）与卖单照旧（存量资产
变现不砍）；输出删除清单入变更表。
"""
from __future__ import annotations

from typing import Any, Dict


def retape_tail_savings(tape_routes: Dict[str, Any]) -> Dict[str, Any]:
    """尾盘 CARE/FEED/闲置 HIRE 修剪+删除清单输出。

    签名意图：输入: 磁带 / 输出: {routes, removed}（修剪后磁带+删除清单） /
    错误: 误删 HARVEST/卖单/d28 前 FEED-CARE 指令即抛。
    """
    raise NotImplementedError("unimplemented:fn:retape_tail_savings")
