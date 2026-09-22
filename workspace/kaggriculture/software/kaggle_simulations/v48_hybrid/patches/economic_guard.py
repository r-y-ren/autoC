"""economic_guard -- v48 混合候选（方案甲）P2 补丁叶：双死价经济护栏（R3）。

独立 stdlib 模块（零 import，不依赖旧树 agent/src、不依赖 v48 基底）。
实现 requirements.md R3：双死价检测 → 否决剧本买畜/建棚步骤；未触发 = 零动作。

==============================================================================
【触发阈值定义与依据】（登记项 1）
==============================================================================
阈值（沿我方 constants.py 语义，模块内自带副本、不 import 旧树）：

    DEAD_PRICE_FLOOR  = {"MILK": 90, "WOOL": 90, "EGG": 30}
    DEAD_PAIR         = ("MILK", "WOOL")     # 判定对：磁带畜线仅依赖此两产品
    DEAD_PRICE_FROM_DAY = 10                 # 曲线可读窗口（constants 同名语义）
    DEAD_PERSIST_STEPS  = 4                  # 双死价须连续持续的帧（step）数

触发 = 同一席位观测上，MILK 与 WOOL 现价**同时**严格低于各自地板（<90），
且该状态已连续保持 >= DEAD_PERSIST_STEPS 帧，且 day >= DEAD_PRICE_FROM_DAY。

依据（灾难局实证 = round23 法证 ep110634204，JOURNAL 2026-09-19 / 
exports/probes/planner_bench/round23_loss_forensics.md §3）：

1) 地板值 90/90/30：我方 constants.py:174 `DEAD_PRICE_FLOOR`（"绝不向死价
   曲线扩产"红线）。灾难局 d13-d17 WOOL 88→43、MILK 114→68 双双跌破 90
   死价线后畜线收入死、12 空棚+5 头拖到终局——即本护栏针对的形态。
2) "两产品同死价"窄化：19 局官方样本中仅 ep110634204 一局出现 MILK+WOOL
   同时 <90（WOOL d13 其余 18 局均在 151-241；MILK 单死价另有 3 局）。
   单死价局畜线的另一条产品线仍在挣钱（110629738 仅 MILK 崩），不得误伤
   ——故单死价、纯 EGG 死价、高价局一律不触发。
3) from-day=10：constants `DEAD_PRICE_FROM_DAY=10`（d10 前曲线不可读，
   早期价格波动不构成死价证据；灾难局双死价实际形成于 d13-d17 窗口）。
4) 持续帧数=4（turnsPerDay=24，约合 1/6 个游戏日）：单帧毛刺（某玩家
   一笔抛售压出的瞬时价）不得触发；灾难局双死价状态自形成后持续数日
   不回。波动局（死 2-3 帧即回升）被此帧数滤除。

判定语义与旧树买畜门（market.py:2186-2201 dead-price freeze）同源：该门
按物种冻结"向自家死价产品扩产"；本护栏把同一红线投影到无市场感知的
v48 磁带上：畜线两条产品曲线（MILK/WOOL）都死时，磁带的买畜/建棚资本
开支整体不可回收 → 否决。EGG 不入判定对：v48 磁带 BUY_ANIMAL 仅含
SHEEP/COW（无 GOOSE 线），蛋价与本基底风险敞口无关。

本护栏**不是**灾难局的挽回机制（§3.3 证明挽回窗口在 d10-d12 的计划注入，
那是 DTSP/P3 的地盘）；它只止损——双死价成形后不再向死市场追加畜线
资本。d10 建棚耗尽现金发生在价格健康期，不在本护栏否决面内。

==============================================================================
【集成缝】（登记项 2，建议，F2 装配时落位）
==============================================================================
v48 策略每步从磁带选出单步动作 dict 返回。建议缝：包装 `_V48_POLICY`
的返回值（每步一次，勿在别处重复调 detect——detect 内部有按席位维护的
连续帧计数，重复调用会重复记帧）：

    step = _V48_POLICY(obs, configuration)      # 基底零改动区不碰
    return vetoe_animal_and_shed_steps([step], obs)[0]

窄缝特性：detect 只读 obs.market.prices/day/step/player；veto 只改写
返回动作里的 BUY_ANIMAL/BUILD_PASTURE；磁带/路由/反克隆/槽位重排/终局
清仓五区不接触。本文件位于 patches/ 独立成叶，互不改他人文件（F1 并行）。

==============================================================================
【回退规则】（登记项 3，fail-safe）
==============================================================================
- detect 的任何异常/缺失字段/类型垃圾 → 返回 False（判为未触发）。
- veto 的任何异常、或 tape_steps 非列表 → 原样返回输入对象（回退剧本）。
- 未触发 → 原样返回**同一对象**（零动作字面保证，可 `is` 验证）。
- 帧计数按席位独立；step 回退（新对局/时钟倒退）自动清零重计。
"""

# ---- 阈值登记（定义与依据见模块头） --------------------------------------
DEAD_PRICE_FLOOR = {"MILK": 90, "WOOL": 90, "EGG": 30}
DEAD_PAIR = ("MILK", "WOOL")
DEAD_PRICE_FROM_DAY = 10
DEAD_PERSIST_STEPS = 4

# 否决面：剧本市场单里的买畜动词 + 单位动作里的建棚动词。
# BUY_LAND/BUY_SEED/HIRE/SELL 等不在否决面（R3 范围 = 买畜/建棚）。
VETO_MARKET_VERBS = ("BUY_ANIMAL",)
VETO_UNIT_VERBS = ("BUILD_PASTURE",)

# 席位级连续帧计数：seat -> {"last_step": int, "run": int}
_STREAKS = {}


def reset_guard_state():
    """清空全部席位帧计数（新对局/测试隔离用）。"""
    _STREAKS.clear()


def _get(obj, key, default=None):
    """attr/item 双通道读取（兼容 dict 与 kaggle Struct 观测）；异常归 default。"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    except Exception:
        return default


def _num(value):
    """数值校验：bool 不算数（防 True==1 伪价）；非数值返回 None。"""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def _pair_dead_now(observation):
    """当帧双死价布尔（不含持续帧判定）：两产品现价同时严格低于地板。"""
    day = _num(_get(observation, "day"))
    if day is None or day < DEAD_PRICE_FROM_DAY:
        return False  # 曲线不可读窗口：任何价格都不构成死价证据
    market = _get(observation, "market")
    prices = _get(market, "prices") if market is not None else None
    if not isinstance(prices, dict):
        return False
    for key in DEAD_PAIR:
        price = _num(prices.get(key))
        floor = DEAD_PRICE_FLOOR.get(key)
        if price is None or floor is None or not price < floor:
            return False
    return True


def _current_step(observation):
    """帧序号：obs.step 优先，缺失时以 day*24+hour 复合（同一 obs 确定性）。"""
    step = _num(_get(observation, "step"))
    if step is not None:
        return int(step)
    day = _num(_get(observation, "day")) or 0
    hour = _num(_get(observation, "hour")) or 0
    return int(day * 24 + hour)


def detect_dead_price_market(observation):
    """双死价判定（R3）。

    输入：当步观测（读 market.prices / day / step / player，兼容 dict 与
    Struct）。输出：bool —— MILK+WOOL 同时 <90 且已连续保持
    DEAD_PERSIST_STEPS 帧且 day>=DEAD_PRICE_FROM_DAY。
    内部按席位维护连续帧计数；step 回退（新对局）自动重置。
    任何异常/缺失 → False（fail-safe：不否决）。
    """
    try:
        seat = _num(_get(observation, "player"))
        seat = 0 if seat is None else int(seat)
        step = _current_step(observation)
        dead = _pair_dead_now(observation)

        st = _STREAKS.get(seat)
        if st is None or step < st["last_step"]:
            st = {"last_step": step, "run": 0}
            _STREAKS[seat] = st
        st["last_step"] = step
        st["run"] = st["run"] + 1 if dead else 0
        return st["run"] >= DEAD_PERSIST_STEPS
    except Exception:
        return False


def _is_verb(cmd, verbs):
    return (
        isinstance(cmd, (list, tuple))
        and len(cmd) >= 1
        and cmd[0] in verbs
    )


def _veto_step(step):
    """单步改写：market 删 BUY_ANIMAL；farmer/hands 槽内 BUILD_PASTURE 换
    ["PASS"]（保槽位对齐）。无任何否决目标时返回**原对象**（步骤级零改动）。
    """
    if not isinstance(step, dict):
        return step
    changed = False
    out = {}
    for key, value in step.items():
        if key == "market" and isinstance(value, list):
            kept = [c for c in value if not _is_verb(c, VETO_MARKET_VERBS)]
            if len(kept) != len(value):
                changed = True
            out[key] = kept
        elif key == "hands" and isinstance(value, list):
            rebuilt = []
            touched = False
            for hand_cmd in value:
                if _is_verb(hand_cmd, VETO_UNIT_VERBS):
                    rebuilt.append(["PASS"])
                    touched = True
                else:
                    rebuilt.append(hand_cmd)
            if touched:
                changed = True
            out[key] = rebuilt
        elif key == "farmer":
            if _is_verb(value, VETO_UNIT_VERBS):
                out[key] = ["PASS"]
                changed = True
            else:
                out[key] = value
        else:
            out[key] = value
    return out if changed else step


def vetoe_animal_and_shed_steps(tape_steps, observation):
    """护栏否决面（R3）：护栏激活时否决剧本中的买畜/建棚步骤。

    - 未激活（detect=False）→ 原样返回**同一列表对象**（零动作字面保证）。
    - 激活 → 返回新列表：market 单删除 BUY_ANIMAL；farmer/hands 槽内
      BUILD_PASTURE 原位替换为 ["PASS"]（手位对齐不破坏）；其余命令与
      无目标步骤原对象原样放行（可 `is` 逐项验证）。
    - tape_steps 非列表 / 任何异常 → 原样返回输入（fail-safe 回退剧本）。
    detect 在此内部每步只调一次（帧计数勿在外部重复喂数，见集成缝）。
    """
    try:
        if not detect_dead_price_market(observation):
            return tape_steps
        if not isinstance(tape_steps, list):
            return tape_steps
        return [_veto_step(step) for step in tape_steps]
    except Exception:
        return tape_steps
