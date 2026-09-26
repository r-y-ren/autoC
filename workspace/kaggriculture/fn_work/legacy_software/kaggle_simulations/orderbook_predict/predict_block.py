# -*- coding: utf-8 -*-
"""predict_block（R21 运行时链，注入包内）。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
_predict_agent（单参官方入口，父层=_r37_agent 链）→ infer_rival_sells（净卖
反推：公开库存差分−自家成交−确定性城镇消费，$1 地板为下界）→ match_sellflow
（卖流库检索：首二店+step-2 身份指纹）→ extrapolate_sells（差分外推 1-2 步
写入 opponent_plan 容器）→ apply_dodge（预测倾销→我方卖单错峰/减量）。
置信不足→不动作 fail-safe；只动卖单时点/量。本文件源文本由
inject_predict_block 追加进包内（含内嵌库数据）。
"""
from __future__ import annotations

from typing import Any, Dict


def _predict_agent(observation: Dict[str, Any]) -> Dict[str, Any]:
    """入口包装：父层取动作→推断账→写 opponent_plan→避让→返回。

    任何异常→父层动作原样（fail-safe）；step==0 复位推断账与计划容器。

    签名意图：输入: observation / 输出: 调整后 action /
    错误: 异常→父层动作原样。
    """
    raise NotImplementedError("unimplemented:fn:_predict_agent")


def infer_rival_sells(observation: Dict[str, Any], own_fills: Any) -> Dict[str, Any]:
    """净卖反推：market.inventory 差分−自家成交−确定性城镇消费
    （shop_interval=4/center_interval=24）→对手上一步净卖量/品类；
    $1 地板成交不入库存→结果记下界标志；跨步账本供外推。

    签名意图：输入: observation（逐步调用）+自有成交账 /
    输出: {item: {net_qty, lower_bound}} / 错误: 字段缺失→空账不抛。
    """
    raise NotImplementedError("unimplemented:fn:infer_rival_sells")


def match_sellflow(observation: Dict[str, Any], library: Any) -> Dict[str, Any]:
    """卖流库检索：键=（unlocked_shops[:2] 组合，step-2 身份指纹[对手 money,
    WHEAT inv]）；取当前步窗 ±w 的对手 SELL 分布；无键→回退全局分布；
    置信=样本数与分布集中度。

    签名意图：输入: observation+库 / 输出: {matches, confidence} /
    错误: 库缺失→confidence=0。
    """
    raise NotImplementedError("unimplemented:fn:match_sellflow")


def extrapolate_sells(inference: Any, matches: Any, plan: Any) -> Dict[str, Any]:
    """差分外推：净卖推断+卖流匹配合成对手未来 1-2 步预期 SELL 单
    （品类+量+步位），写入 opponent_plan 容器对应步位（["SELL",item,qty]）；
    置信低于阈值→不写（fail-safe 不动作）。

    签名意图：输入: 推断账+匹配结果+plan 容器 / 输出: {written, skipped} /
    错误: 容器畸形→不写不抛。
    """
    raise NotImplementedError("unimplemented:fn:extrapolate_sells")


def apply_dodge(observation: Dict[str, Any], action: Dict[str, Any],
                predictions: Any) -> Dict[str, Any]:
    """避让：预测对手 1-2 步内集中抛售某品（置信足）→我方本步该品 SELL 单
    顺延至其抛售后（保槽位置 [] 或减量改单）或减量；预测未达标/置信不足→
    零动作；不碰买种养单、不动 HARVEST/FEED/CARE、不改槽位出口截断。

    签名意图：输入: observation, action, 预测结果 / 输出: 调整后 action+避让账 /
    错误: 异常→原动作。
    """
    raise NotImplementedError("unimplemented:fn:apply_dodge")
