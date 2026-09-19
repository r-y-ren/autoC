# ===========================================================================
# 【中文·模块导览】planner/opponents.py —— DTSP 对手模型集 Ω（Track-B P2）
# ---------------------------------------------------------------------------
# 职责：给 J(plan,ω) 矩阵提供三类对手模型，统一接口：
#     propose_actions(opp_state, day) -> actions   孪生 rollout 中对手席动作
#     supply_pressure(obs_summary) -> {item: factor}  投影器供给压价系数
#     describe() -> str                            模型口径自述（进报告）
#   三类（track-B 文档 §4 组件 4）：
#     a) PassiveExtrapolation  被动延续：对手已观测动作的逐日直方图外推
#        （输入=对手公开 tiles/资金/畜群轨迹 + 已观测市场卖单史）。
#     b) FrozenStylePool       冻结画像池：参数化风格 bot 钩子。画像参数
#        文件缺失时显式 no-op 并标注——不伪造画像（铁律 4 精神）。
#     c) PessimisticFill       悲观成交：在我方卖出时段注入对手倾销单 +
#        成交价折扣系数（对应引擎 per-unit 锁步压价，factsheet §3
#        kaggriculture.py:544-628；折扣默认 0.75 可调）。
# opp_state 契约（plain dict，模型只消费声明的键，缺键走保守分支）：
#   history: [{"day":int, "sells":{item:qty}, "animal_buys":int}, ...]
#            对手逐日已观测动作（回放/observer 账本提取）
#   our_sell_plan: {item: qty}   我方当日计划卖量（PessimisticFill 注入窗）
#   shed: {item: qty}            对手棚仓现货（孪生全态可得；线上侧由
#                                observer 反推，本模块不做二次估计）
#   herd: int                    对手公开畜群头数
#   money: float                 对手公开资金
# 纪律：stdlib-only、确定性（sorted 遍历）、动作永远符合官方 schema
#   （farmer 恰 1 op / hands 每 hand 1 op / market <=10 条，factsheet §3）。
# ===========================================================================

import json
import math
import os

PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

# --------------------------------------------------------------------------
# 内置冻结画像（P2.5 建池：2026-09-19。此前 FrozenStylePool 无画像文件恒
# no-op——首轮 official 复盘的 opponent_model_gap 来源之一。参数全部出自
# 本战役台账实测，出处逐键内嵌；这些都是"对手模型参数"（规划器本地口径，
# 供 J(plan,ω) 排序与孪生注入），不是性能指标，禁止外推为线上成绩。
# ---------------------------------------------------------------------------
# 语料：references/data/online-replays/ 的 cmp-v92 + round8/15/18/19/20/21
# 官方回放（replay_deep_stats 画像，104 个对手席，2026-09-19 抓取/刷新）+
# exports/online/sprint_forensics_0919.md §2/§3（跨代结构对比）。
# 实测聚合（本机 2026-09-19 对上述语料复算）：
#   对手席草莓峰值 median 20 / p75 33 格；瓜峰值 median 12 / p75 18 格；
#   外购饲料量 median 314u / p75 543u（我方同季 77-281u 的 2-40 倍）；
#   d8 畜群 head：全对手 median 5 / p75 8，但 top 赢家带（reward 70-96k）
#   峰值畜群 11-14 且 13-17 头 d8-11 建成（sprint_forensics §2 对手参照行
#   + R3-2 胜者带）。
# --------------------------------------------------------------------------
BUILTIN_STYLE_POOL = (
    {
        # 赢家结构型：top 分段赢家形态——草莓 20-31 + 瓜 12-18 均衡混合，
        # 畜群 d8 前置 13-14 头，外购饲料换奶/毛日收（sprint_forensics_0919
        # §2 对手参照行 + §3 结论 2；crop_pref 权重按 20:12:8 比例）。
        "name": "winner_balanced",
        "herd_target": 14,             # 赢家带峰值 11-14（同 §2）
        "animal": "COW",               # 奶线 d8 窗口（R3-2 建栏节奏）
        "crop_pref": {"STRAWBERRY": 20, "MELON": 12, "WHEAT": 8},
        "daily_sell_cap": 14,          # 莓+瓜日上市上限（吸收带内多批清）
        "herd_due_day": 8,             # 13-17 头 d8-11 前置（R3-2）
        # 压价系数（投影器口径）：其在场即压我方两条高价作物线与畜线
        "pressure": {"STRAWBERRY": 0.85, "MELON": 0.85, "HERD": 0.9},
    },
    {
        # 重小麦压制型：v13.6/13.7 同构的麦底仓独大形态（麦 34 / 莓 9-11 /
        # 萝 0，sprint_forensics_0919 §2 末两行）——作为对手即"小麦供给
        # 压制 + 草莓线薄"的分布；对我方小麦线的压价取 0.7（log 曲线最抗
        # 崩，factsheet §MARKET_PARAMS：WHEAT 上侧=log 幅 0.20）。
        "name": "wheat_suppressor",
        "herd_target": 12,             # round5 review top-band herd median 12
        "animal": "SHEEP",
        "crop_pref": {"WHEAT": 34, "STRAWBERRY": 10},
        "daily_sell_cap": 12,
        "herd_due_day": 8,
        "pressure": {"WHEAT": 0.7, "STRAWBERRY": 0.95, "MELON": 0.95,
                     "HERD": 0.95},
    },
)


def _pass_action():
    """全新 PASS 动作（每次新建，防共享可变）。"""
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _sell_orders(quantities):
    """{item: qty} -> 官方 SELL 订单列表（<=10 条；qty>=1 才生成）。"""
    orders = []
    for item in sorted(quantities):
        qty = int(quantities[item])
        if qty >= 1:
            orders.append(["SELL", item, qty])
    return orders[:10]          # 官方语义：超出静默丢弃（factsheet §3）


class OpponentModel:
    """基类：统一接口 + 名称。子类必须实现 propose_actions。"""

    name = "base"

    def propose_actions(self, opp_state, day):
        raise NotImplementedError(
            f"{type(self).__name__} 未实现 propose_actions"
            f"（示例：propose_actions({{'history': [...]}}, 10)）")

    def supply_pressure(self, obs_summary):
        """投影器供给压价系数 {item: (0,1]}；基类=无压价。"""
        return {}

    def describe(self):
        return self.name


class PassiveExtrapolation(OpponentModel):
    """(a) 被动延续：对手近 window 日卖单直方图均值外推为今日 SELL。

    无历史（冷启动）→ 全 PASS（诚实标注，不编造节奏）。不主动压价：
    supply_pressure 恒 1.0（被动外推不含攻击性）。farmer/hands 恒 PASS
    （其地块操作由引擎按回放/孪生自演化，模型只补市场侧耦合）。
    """

    name = "passive_extrapolation"

    def __init__(self, window=3):
        if int(window) < 1:
            raise ValueError(
                f"window={window!r} 必须 >=1（示例：window=0 应取 3）")
        self.window = int(window)

    def _histogram(self, opp_state):
        """近 window 日 {item: 日均卖量}（逐日直方图、确定性均值）。"""
        history = opp_state.get("history") or []
        recent = [h for h in history
                  if isinstance(h, dict) and h.get("sells")][-self.window:]
        if not recent:
            return {}
        totals = {}
        for h in recent:
            for item in sorted(h.get("sells") or {}):
                qty = h["sells"][item]
                if qty is None:
                    continue
                totals[item] = totals.get(item, 0.0) + float(qty)
        return {item: totals[item] / len(recent) for item in sorted(totals)}

    def propose_actions(self, opp_state, day):
        hist = self._histogram(opp_state)
        if not hist:
            return _pass_action()          # 冷启动：诚实 PASS
        action = _pass_action()
        action["market"] = _sell_orders(hist)
        return action

    def describe(self):
        return (f"被动延续：近 {self.window} 日卖单直方图均值外推；"
                f"冷启动全 PASS")


class FrozenStylePool(OpponentModel):
    """(b) 冻结画像池：从画像参数实例化的风格 bot 钩子（P2.5 起内置双风格）。

    两个来源（互斥）：
      * profile_path（JSON 文件）：{"styles": [{"name": str, "herd_target":
        int, "animal": "COW"|"SHEEP", "crop_pref": {item: weight},
        "daily_sell_cap": int}, ...]}——60 局语料 + round2-21 官方回放建库
        （track-B §4 组件 4）。文件缺失/不可解析 → available=False、
        propose_actions 恒 PASS、describe 显式标注"画像缺失——no-op
        （不伪造）"。
      * use_builtin_pool=True：从 BUILTIN_STYLE_POOL 取第 style_index 个
        内置画像（赢家结构型/重小麦压制型，参数出处见池注释）——不再恒
        no-op；supply_pressure 按画像 pressure 键给投影器真实压价。
    画像键 herd_due_day（可选，缺省 20）：扩栏截止日——内置画像按 d8
    前置带约束买畜窗；文件画像缺该键时保持旧"任何日期可补 1 头"语义。
    """

    name = "frozen_style_pool"

    def __init__(self, profile_path=None, style_index=0,
                 use_builtin_pool=False):
        self.style_index = int(style_index)
        self.style = None
        self.unavailable_reason = None
        self.from_builtin = False
        if use_builtin_pool:
            if not BUILTIN_STYLE_POOL:
                self.unavailable_reason = "内置画像池为空"
            else:
                self.style = dict(BUILTIN_STYLE_POOL[
                    self.style_index % len(BUILTIN_STYLE_POOL)])
                self.from_builtin = True
                prefs = self.style.get("crop_pref") or {}
                if prefs and float(sum(float(v) for v in
                                       prefs.values())) <= 0:
                    self.unavailable_reason = "内置画像 crop_pref 权重之和<=0"
                    self.style = None
        else:
            if not profile_path:
                self.unavailable_reason = "未提供画像参数文件路径"
            else:
                path = os.fspath(profile_path)
                if not os.path.isfile(path):
                    self.unavailable_reason = f"画像参数文件不存在: {path}"
                else:
                    try:
                        with open(path, "r", encoding="utf-8") as handle:
                            data = json.load(handle)
                        styles = data.get("styles") or []
                        if not styles:
                            raise ValueError("画像文件无 styles 数组")
                        self.style = dict(
                            styles[self.style_index % len(styles)])
                        prefs = self.style.get("crop_pref") or {}
                        if prefs and float(sum(
                                float(v) for v in prefs.values())) <= 0:
                            raise ValueError("crop_pref 权重之和 <= 0")
                    except (ValueError, OSError, TypeError) as exc:
                        self.style = None
                        self.unavailable_reason = f"画像参数文件不可解析: {exc}"
        # J 矩阵键（实例级覆盖类名）：内置画像带风格后缀，同池多风格不串键；
        # 文件画像/不可用保持基名（向后兼容既有契约测试）。
        if self.available and self.from_builtin:
            self.name = f"frozen_style_pool:{self.style.get('name', '?')}"

    @property
    def available(self):
        return self.style is not None

    def propose_actions(self, opp_state, day):
        if not self.available:
            return _pass_action()      # 显式 no-op，不伪造画像
        style = self.style
        cap = max(0, int(style.get("daily_sell_cap", 0)))
        action = _pass_action()
        # 卖出：按 crop_pref 权重分配日卖帽（对手棚仓现货钳制）
        shed = opp_state.get("shed") or {}
        prefs = {item: float(w) for item, w in
                 sorted((style.get("crop_pref") or {}).items())}
        total_w = sum(prefs.values())
        quantities = {}
        if cap > 0 and total_w > 0:
            for item, weight in prefs.items():
                want = cap * weight / total_w
                have = float(shed.get(item, 0) or 0)
                qty = int(min(want, have))
                if qty >= 1:
                    quantities[item] = qty
        # 买畜：畜群低于画像目标、现金宽裕且在扩栏窗内补 1 头（确定性；
        # herd_due_day 内嵌 d8 前置带，文件画像缺省 20=旧语义）
        herd_target = int(style.get("herd_target", 0))
        herd_due = int(style.get("herd_due_day", 20))
        herd = int(opp_state.get("herd", 0) or 0)
        money = float(opp_state.get("money", 0) or 0)
        animal = style.get("animal")
        if herd < herd_target and day <= herd_due \
                and money >= 3000 and animal in ("COW", "SHEEP"):
            action["market"] = _sell_orders(quantities) + \
                [["BUY_ANIMAL", animal, 1]]
            action["market"] = action["market"][:10]
        elif quantities:
            action["market"] = _sell_orders(quantities)
        return action

    def supply_pressure(self, obs_summary):
        # 内置画像：按画像 pressure 键压投影器（对手在场即挤占我方线）；
        # 文件画像：不发明压价语义（保持基类口径）。
        if self.available and self.from_builtin:
            return {k: float(v) for k, v in
                    sorted((self.style.get("pressure") or {}).items())}
        return {}

    def describe(self):
        if not self.available:
            return (f"冻结画像池：不可用——{self.unavailable_reason}；"
                    f"propose_actions 恒 PASS（no-op，不伪造画像）")
        if self.from_builtin:
            return (f"冻结画像池[内置]：style={self.style.get('name', '?')} "
                    f"herd_target={self.style.get('herd_target')}"
                    f"(d{self.style.get('herd_due_day', 20)} 前置) "
                    f"crop_pref={sorted(self.style.get('crop_pref') or {})} "
                    f"pressure={sorted(self.style.get('pressure') or {})}"
                    f"（出处：sprint_forensics_0919+cmp 深度统计）")
        return (f"冻结画像池：style={self.style.get('name', '?')} "
                f"herd_target={self.style.get('herd_target')} "
                f"crop_pref={sorted(self.style.get('crop_pref') or {})}")


class PessimisticFill(OpponentModel):
    """(c) 悲观成交：我方卖出时段注入对手倾销单 + 成交价折扣。

    机理（factsheet §3/§4）：双方市场订单 per-unit 锁步交错成交，对手
    同回合 SELL 直接推低我方本回合成交价——模型在我方 our_sell_plan
    非空的日子生成 dump_ratio × 计划量 的对手 SELL（压力测试口径：
    假定对手持有等量倾销库存），并在投影器侧按 price_discount 折扣
    我方该线收入（默认 0.75，可调）。
    """

    name = "pessimistic_fill"

    def __init__(self, dump_ratio=1.0, price_discount=0.75):
        if not 0.0 < float(dump_ratio):
            raise ValueError(
                f"dump_ratio={dump_ratio!r} 必须 >0（示例：0 应取 0.5）")
        if not 0.0 < float(price_discount) <= 1.0:
            raise ValueError(
                f"price_discount={price_discount!r} 必须在 (0,1]"
                f"（示例：1.5 应取 0.75）")
        self.dump_ratio = float(dump_ratio)
        self.price_discount = float(price_discount)

    def propose_actions(self, opp_state, day):
        plan = opp_state.get("our_sell_plan") or {}
        quantities = {}
        for item in sorted(plan):
            qty = plan[item]
            if qty is None:
                continue
            dump = math.ceil(self.dump_ratio * float(qty))
            if dump >= 1:
                quantities[item] = dump
        if not quantities:
            return _pass_action()
        action = _pass_action()
        action["market"] = _sell_orders(quantities)
        return action

    def supply_pressure(self, obs_summary):
        # 投影器口径：我方全部可售线按折扣计（对手可能在我任意卖出日倾销）
        return {"STRAWBERRY": self.price_discount, "MELON": self.price_discount,
                "CARROT": self.price_discount, "WHEAT": self.price_discount,
                "HERD": self.price_discount}

    def describe(self):
        return (f"悲观成交：倾销比 {self.dump_ratio}×我方计划卖量、"
                f"成交价折扣 {self.price_discount}（per-unit 锁步压价口径）")


def build_default_models(history=None, profile_path=None,
                         pessimistic=None):
    """构造 Ω 默认集（track-B §4；P2.5 起内置双风格入池）：
    [被动延续, 冻结画像·赢家结构型, 冻结画像·重小麦压制型, 悲观成交]。
    内置画像实例名带风格后缀，J 矩阵按键聚合不串名。"""
    models = [
        PassiveExtrapolation(),
        FrozenStylePool(use_builtin_pool=True, style_index=0),
        FrozenStylePool(use_builtin_pool=True, style_index=1),
        pessimistic if pessimistic is not None else PessimisticFill(),
    ]
    return models
