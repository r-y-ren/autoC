# -*- coding: utf-8 -*-
"""票 03·方案 B（解码约束）：市场头 state-grounded 解码 shim.

A2+schema1.2 后的残余阻塞（eval_v3 归因）：市场头 item 头 argmax 死咬
WHEAT——WOOL 16 + MELON 6 囤积整季不卖，SELL WHEAT×45 反而把喂羊口粮
卖光（羊 d10 逃光）。本 shim 在解码端加三条状态锚定约束（票面方案 B：
"市场头解码加自回归/预算约束"）：

  1. SELL 锚定棚存：SELL 的 item 改为棚内库存最大者（平局取字典序，
     确定性），数量 clip 到实际库存；棚空则丢弃该卖单。
  2. HIRE 槽间自回归去重：同一动作内重复的 HIRE 只保留首个（跨回合
     不限——专家日雇 3+ 是常态；首版误写成"当日一次"，已修正）。
  3. BUY 预算掩码：单价×数量 > 现金 → 降数量；降到 0 丢弃。

BC 预测的"是否下单/下多少"保留原语义——只修 item 选择与可执行性。
单位动作透传不动。

用法：policy = MarketDecodePolicy(OpeningScriptPolicy(...))
"""
from __future__ import annotations

from bc_policy import to_plain_obs

# 引擎固定价（factsheet §5：种子价 / 动物买价）
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
              "STRAWBERRY": 100, "MELON": 80}
ANIMAL_PRICE = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
PRODUCT_BUYS = ("WHEAT", "FERTILIZER")     # 引擎仅此两者可 BUY_PRODUCT


class MarketDecodePolicy:
    """官方语义 callable 包装：只改 market 订单解码，其余透传。"""

    def __init__(self, base, collect_stats=True):
        self.base = base
        self.collect_stats = collect_stats
        self.rewritten_sell = 0
        self.dropped = 0

    def __call__(self, obs):
        action = self.base(obs)
        plain = to_plain_obs(obs)
        seat = int(plain.get("player") or 0)
        farms = plain.get("farms") or []
        farm = farms[seat] if seat < len(farms) else {}
        shed = dict((plain.get("private") or {}).get("shed") or {})
        money = float(farm.get("money") or 0)
        prices = (plain.get("market") or {}).get("prices") or {}

        out = []
        for o in action.get("market") or []:
            if not isinstance(o, (list, tuple)) or not o:
                continue
            op = o[0]
            if op == "SELL":
                item = None
                best = 0
                for k in sorted(shed):                 # 确定性平局打破
                    v = int(shed.get(k) or 0)
                    if v > best:
                        best = v
                        item = k
                if item is None:
                    if self.collect_stats:
                        self.dropped += 1
                    continue
                qty = int(o[2]) if len(o) >= 3 and o[2] else 1
                qty = max(1, min(qty, best))
                if o[1] != item and self.collect_stats:
                    self.rewritten_sell += 1
                out.append(["SELL", item, qty])
            elif op == "HIRE":
                if any(x and x[0] == "HIRE" for x in out):
                    if self.collect_stats:
                        self.dropped += 1
                    continue
                out.append(["HIRE"])
            elif op == "BUY_SEED":
                item = o[1] if len(o) >= 2 else None
                price = SEED_PRICE.get(item)
                if price is None:
                    continue
                qty = int(o[2]) if len(o) >= 3 and o[2] else 1
                qty = min(qty, int(money // price))
                if qty < 1:
                    if self.collect_stats:
                        self.dropped += 1
                    continue
                money -= price * qty
                out.append(["BUY_SEED", item, qty])
            elif op == "BUY_ANIMAL":
                item = o[1] if len(o) >= 2 else None
                price = ANIMAL_PRICE.get(item)
                if price is None:
                    continue
                qty = int(o[2]) if len(o) >= 3 and o[2] else 1
                qty = min(qty, int(money // price))
                if qty < 1:
                    if self.collect_stats:
                        self.dropped += 1
                    continue
                money -= price * qty
                out.append(["BUY_ANIMAL", item, qty])
            elif op == "BUY_PRODUCT":
                item = o[1] if len(o) >= 2 else None
                if item not in PRODUCT_BUYS:
                    continue
                # 买后报价 ≈ 现价 + 冲击；预算按现价 ×1.3 裕度
                price = float(prices.get(item) or 0) * 1.3
                if price <= 0:
                    price = 30.0
                qty = int(o[2]) if len(o) >= 3 and o[2] else 1
                qty = min(qty, int(money // price))
                if qty < 1:
                    if self.collect_stats:
                        self.dropped += 1
                    continue
                money -= price * qty
                out.append(["BUY_PRODUCT", item, qty])
            else:
                out.append(list(o))
        action = dict(action)
        action["market"] = out[:10]
        return action

    def __getattr__(self, name):
        return getattr(self.base, name)
