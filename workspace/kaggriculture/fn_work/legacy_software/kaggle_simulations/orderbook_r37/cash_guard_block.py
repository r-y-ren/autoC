# -*- coding: utf-8 -*-
"""cash_guard_block（R19 运行时三件套，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
_r37_agent（尾块捕获入口，fail-safe）→ _r37_cash_guard（现金下限判定：
d0 日终窗 ≥12 金[硬底线 4=d1 三张 HIRE 价 1+1+2]、BUY_ANIMAL 提交前 ≥500
金[引擎丢单线 400/400/500]）→ _r37_defer_low_priority（触线顺延低优先级
购买）。动作集合不变量：只顺延/删减购买类单，不新增动作、不动物格
HARVEST 与卖单。本文件源文本由 inject_cash_guard_block 追加进包内。
"""
from __future__ import annotations

from typing import Any, Dict


def _r37_agent(observation: Dict[str, Any], base_action: Dict[str, Any]) -> Dict[str, Any]:
    """尾块捕获入口：取基座动作→交 _r37_cash_guard 调整→返回同构 action。

    动作集合不变量：只顺延/删减购买类单，不新增动作、不动 HARVEST 与卖单；
    任何异常→基座动作原样返回（fail-safe）；step==0 复位层内缓存（顺延账）。

    签名意图：输入: observation, base_action / 输出: 调整后 action /
    错误: 异常→入口兜底回退基座动作。
    """
    raise NotImplementedError("unimplemented:fn:_r37_agent")


def _r37_cash_guard(observation: Dict[str, Any], base_action: Dict[str, Any],
                    floors: Dict[str, Any]) -> Dict[str, Any]:
    """现金下限判定：识别当前步适用下限（①d0 日终窗 step23 前最后动作 ≥12；
    ②BUY_ANIMAL 提交前 ≥500）；触线→交 _r37_defer_low_priority，不触线原样
    放行；下限为可配置常数（判决标定，硬底线 4 不可破）。

    签名意图：输入: observation, base_action, floors /
    输出: {hit_floor, adjusted_action} / 错误: 状态读取失败→不干预原样返回。
    """
    raise NotImplementedError("unimplemented:fn:_r37_cash_guard")


def _r37_defer_low_priority(observation: Dict[str, Any], action: Dict[str, Any],
                            hit_floor: Any) -> Dict[str, Any]:
    """触线处置：按低优先级顺延——先缓 BUY_SEED（MELON 80 金/粒优先，按订单
    尾序删缓），BUY_ANIMAL 现金不足 500 整单顺延至现金达标步重试（保留意图入
    顺延账，不永久删除）；HIRE（4 金硬开销）与 FEED/CARE/卖单/动物格 HARVEST
    序一律不动；处置后须满足触发下限，一次不够→继续顺延直至达标。

    签名意图：输入: observation, action, hit_floor /
    输出: 顺延后 action+顺延账更新 / 错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:_r37_defer_low_priority")
