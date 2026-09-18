# ===========================================================================
# 【中文·模块导览】planner/plans.py —— DTSP 计划空间 Π（Track-B P2）
# ---------------------------------------------------------------------------
# 职责：把 phase_branch_plan v1.5 的参数包体系编码为可哈希、可序列化的
#   PlanSpec（结构轴 = 开局变体 A/B/C × P1 分支 B1/B2/B3 × 容量档 C1/C2/C3
#   × P3 运行态 × P4 出清档；连续缩放轴 = 作物配额 ±25% × 买地/买畜时点
#   ±1-2 天 × 卖出曲线折扣系数），并提供三件公开机制：
#     1) enumerate_plans(obs_summary) -> list[PlanSpec]
#        按局况粗过滤到 <=120 个候选；过滤规则 R1-R7 逐条显式可审计
#        （返回侧带 enumerate_plans_audited 拿到逐步审计说明）。
#     2) plan_to_knob_overrides(plan) -> dict
#        映射到现役执行器命名空间的真实旋钮名（供执行器消费；P2.5 起经
#        PLANNER_ENABLED/PLANNER_OVERRIDES 惰性旋钮通道覆盖 src 门槛与
#        杠杆，旗关与 v13.8 逐字节等价——不可安全参数化项在【缺口清单】
#        如实列出并写明原因）。
#     3) project_season(plan, obs_summary, pressure=None) -> float
#        整季经济投影器（相对排序机器，非绝对预言——它给 J(plan,ω)
#        矩阵打分用；绝对数字以孪生 rollout 为准）。
# 坐标纪律：不发明新维度——每条轴都出自 docs/phase_branch_plan.md v1.5
#   的既有分支/参数包；引擎常数（地价/畜价/纤维雇工/容量定律系数）出自
#   references/digests/engine-factsheet-2026-09-19.md（文件:行号内嵌）。
# 纪律：stdlib-only、确定性（全部轴为显式元组，无集合迭代序依赖）、
#   非法输入抛带失败示例的显式异常。
# ===========================================================================

from dataclasses import dataclass
import json

# --------------------------------------------------------------------------
# 轴常量（v1.5 坐标系）
# --------------------------------------------------------------------------
OPENING_VARIANTS = ("A", "B", "C")        # v1.5 §3：A=旧爆发 2C+2S（回退包）
                                          #        B=d1/d2 后移（历史）
                                          #        C=d0 1C+2S+开局瓜田（默认）
P1_BRANCHES = ("B1", "B2", "B3")          # v1.5 §4.2：对手 d0 分类三分支
CAPACITY_TIERS = ("C1", "C2", "C3")       # v1.5 §5.1：d6 五问 → 三档
P3_MODES = ("HEALTHY", "CATCHUP")         # v1.5 §6：d12 现金 8k 二选一
P4_TIERS = ("LOW", "MID", "HEAVY")        # v1.5 §6：从容/标准/抢跑
QUOTA_SCALES = (0.8, 1.0, 1.25)           # 作物配额连续缩放 ±25%（任务包）
TIMING_SHIFTS = (-2, -1, 0, 1, 2)         # 买地/买畜时点 ±1-2 天（任务包）
SELL_DISCOUNTS = (0.75, 0.9)              # 卖出曲线折扣系数（悲观成交裕度）
MAX_PLAN_CANDIDATES = 120                 # enumerate 硬上限（任务包）

# 开局成本（v1.5 §3：A=2牛2羊~1800；C=1牛2羊~1400；B=d1/d2 后移，d0≈0）
OPENING_D0_COST = {"A": 1800.0, "B": 0.0, "C": 1400.0}
# d0 日终现金门（v1.5 §3：日终现金 >=500）
OPENING_EOD_CASH_MIN = 500.0

# --------------------------------------------------------------------------
# 引擎/文档常数（出处内嵌；只读，运行期不可变）
# --------------------------------------------------------------------------
# 容量定律。文档口径（v1.5 §5.3）：24 × (1+H) × 0.89 / 3.3、上界 ×0.85；
# 但现役执行器（冻结 v13.8 src/constants.py:629-634）已于 2026-09-04 重定标
# 为 CAP_TURNS_PER_UNIT=2.0 / CAP_UTIL=0.89 / CAP_USE_MAX=0.95——DTSP 的
# 计划剪枝必须与执行器同一把尺子，故这里取现役常量（文档值留档备查）。
CAPACITY_LAW_TURNS_PER_UNIT = 2.0     # v1.5 文档=3.3；现役=2.0（重定标）
CAPACITY_LAW_EFFICIENCY = 0.89        # 两处一致（top-20 锚实测）
CAP_USE_BUDGET = 0.95                 # v1.5 文档=0.85；现役 CAP_USE_MAX=0.95
# 资产单位折算（v1.5 §5.3：作物格=1，胡萝卜=0.5 短窗，牲畜每头=2）
ANIMAL_UNITS = 2
CARROT_UNITS = 0.5
# 象限可种格数（factsheet：tiles[10][10]、4 象限 NE/SW/SE 顺序解锁，
# kaggriculture.py:95-97,712-725 → 100÷4=25）。P2.6 投影器产能耦合用。
TILES_PER_QUADRANT = 25

# 地价（factsheet §5：kaggriculture.py:95-97,712-725——NE $1000/SW $2000/SE $4000，
# 固定顺序解锁）与现役购地日程（src/constants.py:101 LAND_PLAN）。
LAND_PRICES = {"Q2": 1000, "Q3": 2000, "Q4": 4000}
LAND_PLAN_DEFAULT = {1: (4, 1700), 2: (7, 2700)}   # (最迟应购日, 保护基金)
# SE 购地窗（src/constants.py：SE_DUE_DAY=10 / SE_BUY_LAST_DAY=14 / SE_FUND=4600）
SE_DUE_DAY_DEFAULT = 10
SE_BUY_LAST_DAY = 14          # v1.5 §2：d14 结构冻结，SE 末窗 d14 关
SE_FUND_DEFAULT = 4600

# 畜群（factsheet §5：GOOSE $300/COW $400/SHEEP $500；每头日耗 1 麦）
ANIMAL_AVG_COST = 450.0       # 计划层均值（COW/SHEEP 中位；goose 不入计划）
HERD_FEED_WHEAT_PER_HEAD = 1.0
ROLLOUT_FEED_PRICE = 36.0     # 外购饲料护栏价（src/strategy.py ROLLOUT_FEED_PRICE）
# 小麦产量锚（src/constants.py 注释口径：18 格 ≈ 21.6 麦/日）
WHEAT_YIELD_PER_TILE_DAY = 1.2

# 单位日收入锚（v1.5 §5.3 表，价格健康时；melon 为摊销锚——吸收约束另乘
# health_factor，见 project_season）。HERD 为净年金（奶/毛）。
REVENUE_ANCHORS = {"STRAWBERRY": 25.0, "CARROT": 35.0, "WHEAT": 27.0,
                   "MELON": 30.0, "HERD": 40.0}
# 健康吸收基准（v1.5 §5.3 表条件：商铺集健康时各线的日吸收量级；obs 的
# daily_demand 与此相比得 health_factor，钳位 [0.3,1.2]）
REF_DEMAND = {"STRAWBERRY": 8.0, "CARROT": 8.0, "WHEAT": 12.0, "MELON": 1.5,
              "HERD": 8.0}
# 种子价（factsheet §5：kaggriculture.py:11-17）
SEED_PRICES = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100,
               "MELON": 80}
# 雇工日薪总额 ≈ fib(crew+1)-1（factsheet §5：kaggriculture.py:99-101,690-699）
CREW_BASE = 5                 # 开局 5 雇（v1.5 §3）
PLANT_LAST_DAY = 14           # 合法种植末线（factsheet：PLANT_LAST_DAY=14）
STRAW_DEADLINE_DAY = 13       # 草莓 4 产夜满额死线（v1.5 §1 时序即收益）
HIRE_RAMP_PER_DAYS = 3        # 计划层雇工爬坡步长（天）
CAP_USE_MAX_DEFAULT = 0.95    # src/constants.py CAP_USE_MAX（仅投影参考）

# --------------------------------------------------------------------------
# 容量档 → 参数包内容（src/constants.py:255-266 _DEFENSIVE_PLAN/_VOLUME_PLAN、
# src/strategy.py:535 _MIXED_PLAN 的冻结值镜像；执行器=现役 v13.8，规划器
# 只换脑不换手，故 C 档数值与 src 逐字段对齐，不另发明）
# --------------------------------------------------------------------------
TIER_PACKS = {
    "C1": {"pack": "VOLUME_CROP", "pack_dict": "_VOLUME_PLAN",
           "straw_quad_cap": 16, "straw_total_cap": 48, "wheat_money_quad": 8,
           "crew_cap": 15, "herd_ceiling": 17, "melon_total_cap": 12},
    "C2": {"pack": "MIXED", "pack_dict": "_MIXED_PLAN",
           "straw_quad_cap": 12, "straw_total_cap": 33, "wheat_money_quad": 4,
           "crew_cap": 11, "herd_ceiling": 14, "melon_total_cap": 12},
    "C3": {"pack": "DEFENSIVE", "pack_dict": "_DEFENSIVE_PLAN",
           "straw_quad_cap": 8, "straw_total_cap": 24, "wheat_money_quad": 3,
           "crew_cap": 12, "herd_ceiling": 17, "melon_total_cap": 12},
}
# 激活旋钮面：PACK 名 → src/_decide_mode 的模式名（信息性；激活仍由现役
# 门槛决定，见 plan_to_knob_overrides 的【缺口清单】第 5 条）。
PACK_MODE_NAME = {"VOLUME_CROP": "VOLUME_CROP", "MIXED": "MIXED",
                  "DEFENSIVE": "DEFENSIVE"}

# P1 分支 → 畜群节奏差异（v1.5 §4.2；B1 追赶 1 头/天，B2 标准序列，
# B3 避瓜打莓=瓜封顶 12）。计划层只取"畜群目标起点/瓜帽"两个可投影量。
BRANCH_MELON_CAP = {"B1": 12, "B2": 12, "B3": 12}
BRANCH_HERD_START_DAY = {"B1": 1, "B2": 2, "B3": 3}

# --------------------------------------------------------------------------
# PlanSpec
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PlanSpec:
    """一个完整季战略计划（v1.5 坐标系，可哈希/可序列化）。

    字段取值域即上方轴元组；越界值在构造期抛 ValueError（带失败示例）。
    """

    opening: str            # P0 开局变体 A/B/C
    p1_branch: str          # P1 分支 B1/B2/B3
    capacity_tier: str      # P2 容量档 C1/C2/C3
    p3_mode: str            # P3 运行态 HEALTHY/CATCHUP
    p4_clear: str           # P4 出清档 LOW/MID/HEAVY
    quota_scale: float      # 作物配额缩放 ∈ QUOTA_SCALES
    timing_shift: int       # 买地/买畜时点偏移 ∈ TIMING_SHIFTS
    sell_discount: float    # 卖出曲线折扣系数 ∈ SELL_DISCOUNTS

    def __post_init__(self):
        axes = (("opening", OPENING_VARIANTS, self.opening),
                ("p1_branch", P1_BRANCHES, self.p1_branch),
                ("capacity_tier", CAPACITY_TIERS, self.capacity_tier),
                ("p3_mode", P3_MODES, self.p3_mode),
                ("p4_clear", P4_TIERS, self.p4_clear))
        for name, allowed, value in axes:
            if value not in allowed:
                raise ValueError(
                    f"PlanSpec.{name}={value!r} 不在取值域 {allowed} 内"
                    f"（示例：PlanSpec(opening='X',...) 应为 {allowed[0]} 之类）")
        if self.quota_scale not in QUOTA_SCALES:
            raise ValueError(
                f"PlanSpec.quota_scale={self.quota_scale!r} 不在 {QUOTA_SCALES}"
                f" 内（示例：quota_scale=1.3 应改取 {QUOTA_SCALES[-1]}）")
        if self.timing_shift not in TIMING_SHIFTS:
            raise ValueError(
                f"PlanSpec.timing_shift={self.timing_shift!r} 不在 "
                f"{TIMING_SHIFTS} 内（示例：timing_shift=3 应改取 2）")
        if self.sell_discount not in SELL_DISCOUNTS:
            raise ValueError(
                f"PlanSpec.sell_discount={self.sell_discount!r} 不在 "
                f"{SELL_DISCOUNTS} 内（示例：0.5 应改取 {SELL_DISCOUNTS[0]}）")

    def key(self) -> str:
        """规范键（字典序 tie-break 与排序用；浮点两位定格，跨进程稳定）。"""
        return "|".join((
            "P", self.opening, self.p1_branch, self.capacity_tier,
            self.p3_mode, self.p4_clear,
            f"{self.quota_scale:.2f}", f"{self.timing_shift:+d}",
            f"{self.sell_discount:.2f}"))

    def to_dict(self) -> dict:
        """JSON 安全序列化（键固定顺序，json.dumps(sort_keys=True) 稳定）。"""
        return {"opening": self.opening, "p1_branch": self.p1_branch,
                "capacity_tier": self.capacity_tier, "p3_mode": self.p3_mode,
                "p4_clear": self.p4_clear,
                "quota_scale": float(self.quota_scale),
                "timing_shift": int(self.timing_shift),
                "sell_discount": float(self.sell_discount)}

    @classmethod
    def from_dict(cls, d):
        """反序列化（未知键抛错——fail-closed，防静默漂移）。"""
        known = {"opening", "p1_branch", "capacity_tier", "p3_mode",
                 "p4_clear", "quota_scale", "timing_shift", "sell_discount"}
        missing = known - set(d)
        extra = set(d) - known
        if missing:
            raise ValueError(f"PlanSpec.from_dict 缺字段 {sorted(missing)}"
                             f"（示例：{{'opening':'C',...,'sell_discount':0.9}}）")
        if extra:
            raise ValueError(f"PlanSpec.from_dict 未知字段 {sorted(extra)}"
                             f"（示例：'melon_cap' 不是 PlanSpec 字段）")
        return cls(**d)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_json(cls, s: str):
        return cls.from_dict(json.loads(s))


# --------------------------------------------------------------------------
# obs_summary（局况摘要；plain dict，键契约如下，缺键按缺省走保守分支）
#   day: int                      当前天（0-29）
#   money: float                  我方现金
#   herd: int                     我方已放畜群头数
#   crew: int                     我方当前雇工数（hands）
#   crops: {"STRAWBERRY":n,...}   我方在田作物格数（含 TOMATO/CARROT）
#   unlocked_quadrants: int       已解锁象限数（1-4）
#   prices: {item: float}         现价（obs.market.prices）
#   daily_demand: {item: float}   城镇期望日吸收（调用方由引擎 SHOPS 表算）
#   opponent: {"herd":int,"crops":{...},"money":float}
#   opening_played: str|None      历史实际走过的开局变体（R1 过滤用）
#   opp_class: str|None           对手 d0 分类（burst/reduced/deferred/
#                                 melon_first；v1.5 §4.1 分类器口径）
#   d6_checks: [b1..b5]|None      d6 五问（v1.5 §5.1：畜群/现金/莓价吸收/
#                                 首市日 KPI/容量问）
#   p4_tier: str|None             observer P4 三档快照
# --------------------------------------------------------------------------

_DEFAULT_CROPS = {"STRAWBERRY": 0, "WHEAT": 0, "MELON": 0, "CARROT": 0,
                  "TOMATO": 0}


def build_obs_summary(day, money, herd, crops, unlocked_quadrants,
                      prices=None, daily_demand=None, crew=0, opponent=None,
                      opening_played=None, opp_class=None, d6_checks=None,
                      p4_tier=None):
    """构造带缺省的 obs_summary（键契约见上；显式 > 隐式）。"""
    crops_full = dict(_DEFAULT_CROPS)
    for k, v in (crops or {}).items():
        if k not in crops_full:
            raise ValueError(
                f"crops 键 {k!r} 不在 {_DEFAULT_CROPS} 内"
                f"（示例：'PUMPKIN' 应为 'MELON'）")
        crops_full[k] = int(v)
    opp = {"herd": 0, "crops": dict(_DEFAULT_CROPS), "money": 0.0}
    opp.update(opponent or {})
    return {
        "day": int(day), "money": float(money), "herd": int(herd),
        "crew": int(crew), "crops": crops_full,
        "unlocked_quadrants": int(unlocked_quadrants),
        "prices": dict(prices or {}), "daily_demand": dict(daily_demand or {}),
        "opponent": opp, "opening_played": opening_played,
        "opp_class": opp_class, "d6_checks": d6_checks, "p4_tier": p4_tier,
    }


def classify_opponent_opening(day, opp_farm_herd, opp_farm_crops,
                              opp_farm_wheat_tiles=None):
    """v1.5 §4.1 对手 d0 分类器（纯公开状态口径，本模块的审计级重实现）。

    判据（出典 v1.5 §4.1 表）：
      burst         已放畜群 >= 4 头（top-20 116/116 d0 押 4-5 头）
      reduced       畜群 2-3 头（tetsuya 现行形态）
      deferred      畜群 0 且小麦 >= 8 格
      melon_first   d1-3 瓜格 >= 6（可后置判定）
    返回分类字符串或 None（数据不足）。
    """
    herd = int(opp_farm_herd or 0)
    crops = dict(_DEFAULT_CROPS)
    for k, v in (opp_farm_crops or {}).items():
        if k in crops:
            crops[k] = int(v)
    if day <= 3 and crops["MELON"] >= 6:
        return "melon_first"
    if herd >= 4:
        return "burst"
    if 2 <= herd <= 3:
        return "reduced"
    if herd == 0:
        wheat = (opp_farm_wheat_tiles if opp_farm_wheat_tiles is not None
                 else crops["WHEAT"])
        if int(wheat) >= 8:
            return "deferred"
    return "reduced" if herd >= 1 else None


def classify_opening_variant(day0_animals, day0_melon_tiles):
    """由回放 d0 动作反推我方实际走过的开局变体（v1.5 §3 变体定义）：
      A = 旧爆发 2C+2S（4 头畜，~1800）
      C = 1C+2S（3 头）+ 开局瓜田（瓜格 >=6）
      B = 后移（其余）
    """
    animals = int(day0_animals or 0)
    melon = int(day0_melon_tiles or 0)
    if animals >= 4:
        return "A"
    if animals >= 2 and melon >= 6:
        return "C"
    return "B"


# --------------------------------------------------------------------------
# 计划派生量（单一出处：overrides 与投影器共用）
# --------------------------------------------------------------------------


def capacity_law_units(crew: int) -> float:
    """容量定律（v1.5 §5.3）：24 × (1+H) × 0.89 / 3.3。"""
    return 24.0 * (1 + int(crew)) * CAPACITY_LAW_EFFICIENCY \
        / CAPACITY_LAW_TURNS_PER_UNIT


def plan_targets(plan: PlanSpec) -> dict:
    """计划的数值目标视图（overrides/投影共用；全部为确定性纯函数）。"""
    pack = TIER_PACKS[plan.capacity_tier]
    qs = plan.quota_scale

    def scale_cap(value):
        return max(1, int(round(value * qs)))

    straw_total = scale_cap(pack["straw_total_cap"])
    melon_total = scale_cap(min(pack["melon_total_cap"],
                                BRANCH_MELON_CAP[plan.p1_branch]))
    wheat_floor = 18 if plan.p1_branch == "B2" else 16   # v1.5 §4.2：麦底仓 12-18
    herd_target = int(pack["herd_ceiling"])
    land_dues = {
        1: (max(1, LAND_PLAN_DEFAULT[1][0] + plan.timing_shift),
            LAND_PLAN_DEFAULT[1][1]),
        2: (max(1, LAND_PLAN_DEFAULT[2][0] + plan.timing_shift),
            LAND_PLAN_DEFAULT[2][1]),
    }
    se_due = max(1, min(SE_BUY_LAST_DAY,
                        SE_DUE_DAY_DEFAULT + plan.timing_shift))
    return {
        "pack": pack["pack"], "pack_dict": pack["pack_dict"],
        "straw_quad_cap": scale_cap(pack["straw_quad_cap"]),
        "straw_total_cap": straw_total,
        "wheat_money_quad": scale_cap(pack["wheat_money_quad"]),
        "crew_cap": int(pack["crew_cap"]),
        "herd_ceiling": herd_target,
        "melon_total_cap": melon_total,
        "wheat_floor": wheat_floor,
        "land_dues": land_dues, "se_due": se_due,
        "herd_start_day": BRANCH_HERD_START_DAY[plan.p1_branch],
    }


def pack_asset_units(plan: PlanSpec) -> float:
    """计划满配资产单位数（容量定律口径：作物格=1、牲畜每头=2）。"""
    t = plan_targets(plan)
    return (t["straw_total_cap"] + t["wheat_floor"] + t["melon_total_cap"]
            + ANIMAL_UNITS * t["herd_ceiling"])


# --------------------------------------------------------------------------
# 过滤规则（显式可审计：R1-R7 逐条；返回 (plans, audit_notes)）
# --------------------------------------------------------------------------

# 预算分配：离散组合先粗过滤，再与连续网格交叉。连续网格（每离散组合）
# = TIMING_SHIFTS × SELL_DISCOUNTS；离散保留配额 = 120 // 该格大小，
# 多样性序 = 轴序号和升序（保守优先），并按 (tier,quota) 分组轮转插值，
# 保证 C1/C2/C3 各档在预算内均有代表（不因保守序塌缩到单档）。
CONTINUOUS_GRID = tuple((s, d) for s in TIMING_SHIFTS for d in SELL_DISCOUNTS)
DISCRETE_BUDGET = max(1, MAX_PLAN_CANDIDATES // len(CONTINUOUS_GRID))

_AXIS_PRIORITY = {
    "opening": {"C": 0, "A": 1, "B": 2},       # v1.5 默认优先
    "p1_branch": {"B2": 0, "B1": 1, "B3": 2},  # 标准序列优先
    "capacity_tier": {"C3": 0, "C2": 1, "C1": 2},  # 保守档优先
    "p3_mode": {"HEALTHY": 0, "CATCHUP": 1},
    "p4_clear": {"LOW": 0, "MID": 1, "HEAVY": 2},
}


def _discrete_axis_priority(opening, branch, tier, mode, clear):
    return (_AXIS_PRIORITY["opening"][opening]
            + _AXIS_PRIORITY["p1_branch"][branch]
            + _AXIS_PRIORITY["capacity_tier"][tier]
            + _AXIS_PRIORITY["p3_mode"][mode]
            + _AXIS_PRIORITY["p4_clear"][clear])


def enumerate_plans_audited(obs_summary):
    """enumerate_plans 的审计版：返回 (plans, notes)。

    过滤规则（逐条，全部可从 obs_summary 键复算）：
      R1 开局定格：day>=3 且 opening_played 已知 → 只留该变体
         （d0-d2 保留全部——开局尚在进行）。
      R2 分支定格：day>=1 且 opp_class 已知 → burst 只留 B1，
         reduced/deferred 只留 B2，melon_first 只留 B3（v1.5 §4.2 触发表）。
      R3 容量档门：day>=6 且 d6_checks 给定 → C1 需五问全过；C2 需
         q1(畜群)/q2(现金)/q5(容量) 过（v1.5 §5.1 触发表）；C3 恒可选。
      R4 运行态定格：day>=12 → 现金 >=8000 留 HEALTHY 否则 CATCHUP
         （v1.5 §6：d12 现金 8k 分界）。
      R5 出清档定格：day>=22 且 p4_tier 已知 → 只留该档。
      R6 开局现金门：day<=2 → 开局变体 d0 成本 > money-500 者剔除
         （v1.5 §3：日终现金 >=500）。
      R7 容量定律剪枝：quota × 档位满配资产单位 > 容量定律(档位 crew)
         × CAP_USE_BUDGET 的 (tier,quota) 组合剔除（v1.5 §5.3 规则 5；
         系数取现役执行器重定标值，见容量定律常数注释）。
      R8 预算分配：离散组合按 (tier,quota) 分组，组内按多样性序
         （轴序号和升序，同和按 key 字典序）排列，组间轮转插值取前
         DISCRETE_BUDGET 个；与连续网格（时点×折扣）交叉后仍超 120 时按
         (|quota_scale-1|, |timing_shift|, sell_discount 降序, key) 截断。
    """
    notes = []
    day = int(obs_summary.get("day", 0))
    money = float(obs_summary.get("money", 0.0))

    openings = list(OPENING_VARIANTS)
    if day >= 3:
        played = obs_summary.get("opening_played")
        if played in OPENING_VARIANTS:
            openings = [played]
            notes.append(f"R1 开局定格 day={day} -> {played}")
        else:
            notes.append(f"R1 未触发：day={day} 但 opening_played 未知，保留全部变体")
    if day <= 2:
        kept = []
        for op in openings:
            cost = OPENING_D0_COST[op]
            if cost <= money - OPENING_EOD_CASH_MIN:
                kept.append(op)
            else:
                notes.append(
                    f"R6 剔除开局 {op}：d0 成本 {cost} > 现金 {money}-500")
        if kept:
            openings = kept
        else:
            notes.append("R6 全部开局超现金门，回退保底 B（后移不花钱）")
            openings = ["B"]

    branches = list(P1_BRANCHES)
    if day >= 1:
        opp_class = obs_summary.get("opp_class")
        branch_of = {"burst": "B1", "reduced": "B2", "deferred": "B2",
                     "melon_first": "B3"}
        if opp_class in branch_of:
            branches = [branch_of[opp_class]]
            notes.append(f"R2 分支定格 opp_class={opp_class} -> {branches[0]}")
        else:
            notes.append(f"R2 未触发：opp_class={opp_class!r} 未知，保留全部分支")

    tiers = list(CAPACITY_TIERS)
    if day >= 6:
        checks = obs_summary.get("d6_checks")
        if checks is not None and len(checks) == 5:
            passed = [bool(c) for c in checks]
            allowed = set()
            if all(passed):
                allowed.add("C1")
            if passed[0] and passed[1] and passed[4]:
                allowed.update(("C2",))
            allowed.add("C3")
            tiers = [t for t in CAPACITY_TIERS if t in allowed]
            notes.append(f"R3 容量档门 d6_checks={passed} -> {tiers}")
        else:
            notes.append("R3 未触发：d6_checks 缺失/长度非 5，保留全部档位")

    modes = list(P3_MODES)
    if day >= 12:
        want = "HEALTHY" if money >= 8000.0 else "CATCHUP"
        modes = [want]
        notes.append(f"R4 运行态定格 day>=12 money={money} -> {want}")

    clears = list(P4_TIERS)
    if day >= 22:
        tier = obs_summary.get("p4_tier")
        if tier in P4_TIERS:
            clears = [tier]
            notes.append(f"R5 出清档定格 p4_tier={tier}")
        else:
            notes.append("R5 未触发：p4_tier 未知，保留全部出清档")

    # R7 容量定律剪枝（(tier,quota) 级）
    tier_quota = []
    for tier in tiers:
        cap_units = capacity_law_units(TIER_PACKS[tier]["crew_cap"]) \
            * CAP_USE_BUDGET
        for q in QUOTA_SCALES:
            probe = PlanSpec(opening="C", p1_branch="B2", capacity_tier=tier,
                             p3_mode="HEALTHY", p4_clear="LOW",
                             quota_scale=q, timing_shift=0, sell_discount=0.9)
            if pack_asset_units(probe) <= cap_units:
                tier_quota.append((tier, q))
            else:
                notes.append(
                    f"R7 剪枝 tier={tier} quota={q}：满配 "
                    f"{pack_asset_units(probe):.1f} 单位 > 容量定律"
                    f"×{CAP_USE_BUDGET}={cap_units:.1f}")
    if not tier_quota:
        # 全被剪则放宽到最小配额（保底 C3×0.8；审计可见）
        notes.append("R7 全部 (tier,quota) 被剪，回退保底 C3×0.8")
        tier_quota = [("C3", 0.8)]

    # R8 预算分配：离散组合按 (tier,quota) 分组轮转插值（组内多样性序）
    discrete = []
    for op in openings:
        for br in branches:
            for (tier, q) in tier_quota:
                for mo in modes:
                    for cl in clears:
                        discrete.append((op, br, tier, mo, cl, q))

    def _combo_rank(combo):
        return (_discrete_axis_priority(combo[0], combo[1], combo[2],
                                        combo[3], combo[4]),
                PlanSpec(opening=combo[0], p1_branch=combo[1],
                         capacity_tier=combo[2], p3_mode=combo[3],
                         p4_clear=combo[4], quota_scale=combo[5],
                         timing_shift=0, sell_discount=0.9).key())

    groups = {}
    for combo in discrete:
        groups.setdefault((combo[2], combo[5]), []).append(combo)
    for gkey in groups:
        groups[gkey].sort(key=_combo_rank)
    # 组间轮转：第 r 轮优先取分支 P1_BRANCHES[r % 3]（B2 默认 → B1 burst
    # 应答 → B3），保证预算内分支均有代表；组内取该分支多样性序最优的
    # 未选成员，无该分支成员则按序补位。
    selected = []
    chosen = set()
    for round_i in range(len(P1_BRANCHES)):
        if len(selected) >= DISCRETE_BUDGET:
            break
        want_branch = P1_BRANCHES[round_i % len(P1_BRANCHES)]
        for gkey in sorted(groups):
            if len(selected) >= DISCRETE_BUDGET:
                break
            pick = None
            for member in groups[gkey]:
                if member[1] == want_branch and member not in chosen:
                    pick = member
                    break
            if pick is None:
                for member in groups[gkey]:
                    if member not in chosen:
                        pick = member
                        break
            if pick is not None:
                selected.append(pick)
                chosen.add(pick)
    if len(discrete) > len(selected):
        notes.append(f"R8 离散组合 {len(discrete)} > 预算 {DISCRETE_BUDGET}"
                     f"（(tier,quota) 组间轮转插值截断）")
    discrete = selected

    plans = []
    for (op, br, tier, mo, cl, q) in discrete:
        for (s, d) in CONTINUOUS_GRID:
            plans.append(PlanSpec(opening=op, p1_branch=br,
                                  capacity_tier=tier, p3_mode=mo,
                                  p4_clear=cl, quota_scale=q,
                                  timing_shift=s, sell_discount=d))
    # 最终 120 上限截断（确定性优先序：贴近基线的连续旋钮优先）
    if len(plans) > MAX_PLAN_CANDIDATES:
        plans.sort(key=lambda p: (
            abs(p.quota_scale - 1.0), abs(p.timing_shift),
            -p.sell_discount, p.key()))
        notes.append(f"R8 连续交叉 {len(plans)} > {MAX_PLAN_CANDIDATES}，"
                     f"按贴近基线序截断")
        plans = plans[:MAX_PLAN_CANDIDATES]
    plans.sort(key=lambda p: p.key())     # 输出稳定序
    return plans, notes


def enumerate_plans(obs_summary):
    """按局况粗过滤的候选计划集（<=120；规则与审计见 enumerate_plans_audited）。"""
    plans, _ = enumerate_plans_audited(obs_summary)
    return plans


# --------------------------------------------------------------------------
# 旋钮覆盖映射（执行器消费契约）
# --------------------------------------------------------------------------
# 【缺口清单·P2.5 复裁版】原 v13.8 只读缺口经蓝图 m7 修订授权（2026-09-19）
# 已在 src/ 落成惰性旋钮（PLANNER_ENABLED 总旗 + PLANNER_OVERRIDES 寄存器，
# 旗关与现役逐字节等价，scripts/planner_flagoff_golden.py 黄金哈希钉住）。
# 逐项处置（可参数化 6 项中 5 项 = 83%）：
#   1. 卖出曲线折扣系数 →【已参数化】src/market._sell_plan_item 的
#      sell_price_discount（悲观裕度乘在曲线投影上）+ sell_batch_mult
#      （批量杠杆：_sell_overrides.tranche 与 MK-2 黎明日帽）+ 原有
#      SELL_PLAN_HOLD_EDGE（囤货门槛）。
#   2. 买畜时点 →【已参数化】strategy._herd_target 的 herd_day_shift
#      （整条日程沿日历平移）+ market 买畜节奏环的 herd_start_day 起步门
#      + animal_buy_last_day_shift（末窗平移）。
#   3. P0 开局变体 →【不可安全参数化，保留只读】OPENING_SHIFT_SEQ 旋钮
#      存在（src/constants.py:137），但 v1.5 P0 接线被 sprint-A 法证否决
#      （phase_branch_plan §9 遗留项 1；sprint_forensics_0919 §4：v1.5 P0
#      开局减档本地实测 -30.74% 灾难）——把"换开局"交给计划会在黄金季里
#      复现已定案的破产形态。覆盖仅记 PLANNER_LOCAL.opening（信息性）。
#   4. P1 分支 B1/B2/B3 →【已参数化】strategy._b_branch_adjust 的
#      b_branch_force（计划强制分支动作包，越过 d1 分类冻结）。
#   5. 容量档激活 →【已参数化】src/strategy._decide_mode 的 11 个激活
#      门槛键（mode_volume_* / mode_scale_*）+ _d6_checkpoint 的 4 个
#      d6_* 五问键——C 档经 TIER_MODE_GATES 表驱动门槛与参数包内容
#      同步变；参数包 dict 内容本就可覆盖（_VOLUME_PLAN 等点路径）。
#   6. P3 运行态 / P4 出清档 →【已参数化（姿态近似）】P3 的 HEALTHY/
#      CATCHUP 映射到 fuse_money_floor（流动性熔断地板 300→600）与
#      crew_late_day/crew_late_cap（P2.6 起钉在 v13.8 冻结值 24/10——
#      "晚季降编提前 2 天"经 d20 隔离消融证伪，见 _P3_POSTURE 注）——
#      src 的运行态是涌现
#      姿态而非单点开关，此映射为诚实近似；P4 的 LOW/MID/HEAVY 映射到
#      p4_force_tier（强制出清档，越过观测置信门）+ sell_batch_mult。
#      阶段窗 stage_p1_due/p2_freeze/p3_end/p4_end 已开键但本波不接线
#      计划轴（保留轴：d14 冻结 doctrine 由执行器局况自治）。
#
_SELL_HOLD_EDGE_BASE = 1.05    # src/constants.py SELL_PLAN_HOLD_EDGE 默认
_PLANNER_LOCAL_KEYS = ("sell_discount", "animal_buy_day_shift", "p3_mode",
                       "p4_clear", "opening", "p1_branch")

# 容量档 → 激活门槛包（P2.5 新增；C2=v13.8 冻结值逐字段镜像，C1/C3 的
# 偏离值出自 v1.5 §5.1/§5.3 的档位语义：C1=宽田候选提前一拍入场、
# C3=畜牧保守档否决宽田；mode_volume_herd_floor 全档钉 10——v7.2-V1
# seed-103 破产地板是安全不变式不是调参旋钮）。绝对数字以孪生 rollout
# 裁决（bench 判据），此处只定义计划坐标。
TIER_MODE_GATES = {
    "C1": {"vol_day": (5, 13), "vol_price": 100, "vol_demand": 3,
           "vol_herd": 10, "vol_hold_price": 35, "vol_hold_cash": 300,
           "d6_herd": 10, "d6_cash": 600, "d6_price": 100, "d6_demand": 3},
    "C2": {"vol_day": (6, 12), "vol_price": 105, "vol_demand": 4,
           "vol_herd": 10, "vol_hold_price": 40, "vol_hold_cash": 300,
           "d6_herd": 10, "d6_cash": 800, "d6_price": 105, "d6_demand": 4},
    "C3": {"vol_day": (99, 99), "vol_price": 105, "vol_demand": 4,
           "vol_herd": 10, "vol_hold_price": 10 ** 9, "vol_hold_cash": 300,
           "d6_herd": 10, "d6_cash": 800, "d6_price": 105, "d6_demand": 4},
}
# C 档共有的 scale 门槛（v13.8 冻结值；全档同值——SCALE 激活由局况自治，
# 计划不改写，见缺口清单第 6 条保留轴说明）。
_SCALE_GATES_DEFAULT = {"scale_day": (4, 16), "scale_entry_herd": 12,
                        "scale_hold_herd": 14}
# P3 运行态 → 流动性姿态（缺口 6）。P2.6 校准（2026-09-19）：CATCHUP 的
# 晚季降编杆（crew_late_day 24→22）经 d20 隔离消融证伪——两局 CATCHUP 注入
# 点全额损失（−7593/−2004）在退回该杆后归零、退回熔断杆后不变，故
# crew_late 回到 v13.8 冻结值 24/10，CATCHUP 语义保留在熔断地板 600。
# 证据：calibration/d20 P3 隔离（sweep 留痕同期输出）。
_P3_POSTURE = {
    "HEALTHY": {"fuse_money_floor": 300, "crew_late_day": 24,
                "crew_late_cap": 10},
    "CATCHUP": {"fuse_money_floor": 600, "crew_late_day": 24,
                "crew_late_cap": 10},
}
# P4 出清档 → 强制档 + 卖出批量乘数（缺口 6；HEAVY=抢跑倾销 2×日帽、
# LOW=从容 0.75×）。
_P4_CLEAR_GATES = {"LOW": {"p4_force_tier": "low", "sell_batch_mult": 0.75},
                   "MID": {"p4_force_tier": "mid", "sell_batch_mult": 1.0},
                   "HEAVY": {"p4_force_tier": "heavy",
                             "sell_batch_mult": 2.0}}
# 阶段窗保留轴（v13.8 冻结值；全名面显式发射，便于审计与未来接线）。
_STAGE_GATES_DEFAULT = {"stage_p1_due": 6, "stage_p2_freeze": 14,
                        "stage_p3_end": 21, "stage_p4_end": 27}


def plan_to_knob_overrides(plan: PlanSpec) -> dict:
    """PlanSpec → 现役命名空间旋钮覆盖（键=真实旋钮名/点路径）。

    返回值约定：
      - "PLANNER_ENABLED"：DTSP 总旗（exec 装载后置 True 才使覆盖生效；
        旗关恒回默认值——黄金动作哈希保证 v13.8 逐字节等价）。
      - "PLANNER_OVERRIDES.<键>"：写入 src/constants.py 的计划覆盖寄存器
        （_plan_knob 惰性读取；键面=缺口清单 P2.5 处置的 29 键全名面）。
      - 顶层标量键 / "DICT.key" 点路径：直接写命名空间（SE_DUE_DAY、
        _VOLUME_PLAN.straw_total_cap、LAND_PLAN.1 整元组等，语义与测试侧
        main.<KNOB> patch 契约一致）。
      - "PLANNER_LOCAL.*"/"PACK"：信息性键（执行器侧跳过）。
    数值均为确定性取整；容量档镜像自 src 冻结值（见 TIER_PACKS 出处）。
    """
    t = plan_targets(plan)
    d = plan.sell_discount
    gates = TIER_MODE_GATES[plan.capacity_tier]
    posture = _P3_POSTURE[plan.p3_mode]
    clear_gates = _P4_CLEAR_GATES[plan.p4_clear]
    branch = plan.p1_branch
    overrides = {
        "PACK": PACK_MODE_NAME[t["pack"]],
        # —— DTSP 总旗 + 计划覆盖寄存器（旗关等价性的开关面）——
        "PLANNER_ENABLED": True,
        # —— 容量档参数包内容（目标包三字段 + 逐调用读取的 REGIME 常量）——
        f"{t['pack_dict']}.straw_quad_cap": t["straw_quad_cap"],
        f"{t['pack_dict']}.straw_total_cap": t["straw_total_cap"],
        f"{t['pack_dict']}.wheat_money_quad": t["wheat_money_quad"],
        "STRAW_QUAD_CAP_REGIME": t["straw_quad_cap"],
        "STRAW_TOTAL_CAP_REGIME": t["straw_total_cap"],
        # —— 分线封顶（配额缩放同源；HERD/WHEAT 不缩放）——
        "LINE_CAPS.STRAWBERRY": t["straw_total_cap"],
        "LINE_CAPS.MELON": t["melon_total_cap"],
        # —— 买地时点（缺口 2 买地半边）——
        "LAND_PLAN.1": t["land_dues"][1],
        "LAND_PLAN.2": t["land_dues"][2],
        "SE_DUE_DAY": t["se_due"],
        "SE_BUY_LAST_DAY": SE_BUY_LAST_DAY,
        # —— 卖出曲线（缺口 1：价格折扣 + 囤货门槛；批量在 P4 档）——
        "SELL_PLAN_HOLD_EDGE": round(
            _SELL_HOLD_EDGE_BASE + (1.0 - d) * 0.4, 3),
        "PLANNER_OVERRIDES.sell_price_discount": float(d),
        # —— 容量档激活门槛（缺口 5：C 档门槛随计划变）——
        "PLANNER_OVERRIDES.mode_volume_day_start": gates["vol_day"][0],
        "PLANNER_OVERRIDES.mode_volume_day_end": gates["vol_day"][1],
        "PLANNER_OVERRIDES.mode_volume_price_min": gates["vol_price"],
        "PLANNER_OVERRIDES.mode_volume_demand_min": gates["vol_demand"],
        "PLANNER_OVERRIDES.mode_volume_herd_floor": gates["vol_herd"],
        "PLANNER_OVERRIDES.mode_volume_hold_price_min":
            gates["vol_hold_price"],
        "PLANNER_OVERRIDES.mode_volume_hold_cash_min": gates["vol_hold_cash"],
        "PLANNER_OVERRIDES.mode_scale_day_start":
            _SCALE_GATES_DEFAULT["scale_day"][0],
        "PLANNER_OVERRIDES.mode_scale_day_end":
            _SCALE_GATES_DEFAULT["scale_day"][1],
        "PLANNER_OVERRIDES.mode_scale_entry_herd":
            _SCALE_GATES_DEFAULT["scale_entry_herd"],
        "PLANNER_OVERRIDES.mode_scale_hold_herd":
            _SCALE_GATES_DEFAULT["scale_hold_herd"],
        "PLANNER_OVERRIDES.d6_herd_floor": gates["d6_herd"],
        "PLANNER_OVERRIDES.d6_cash_min": gates["d6_cash"],
        "PLANNER_OVERRIDES.d6_straw_price_min": gates["d6_price"],
        "PLANNER_OVERRIDES.d6_straw_demand_min": gates["d6_demand"],
        # —— 阶段窗（保留轴：全名面显式发射，本波不接线计划轴）——
        "PLANNER_OVERRIDES.stage_p1_due": _STAGE_GATES_DEFAULT["stage_p1_due"],
        "PLANNER_OVERRIDES.stage_p2_freeze":
            _STAGE_GATES_DEFAULT["stage_p2_freeze"],
        "PLANNER_OVERRIDES.stage_p3_end": _STAGE_GATES_DEFAULT["stage_p3_end"],
        "PLANNER_OVERRIDES.stage_p4_end": _STAGE_GATES_DEFAULT["stage_p4_end"],
        # —— P3 运行态姿态（缺口 6：熔断地板 + 晚季降编）——
        "PLANNER_OVERRIDES.fuse_money_floor": posture["fuse_money_floor"],
        "PLANNER_OVERRIDES.crew_late_day": posture["crew_late_day"],
        "PLANNER_OVERRIDES.crew_late_cap": posture["crew_late_cap"],
        # —— P4 出清档（缺口 6：强制档 + 批量乘数）——
        "PLANNER_OVERRIDES.p4_force_tier": clear_gates["p4_force_tier"],
        "PLANNER_OVERRIDES.sell_batch_mult": clear_gates["sell_batch_mult"],
        # —— 买畜时点（缺口 2：日程平移 + 起步门 + 末窗平移）——
        "PLANNER_OVERRIDES.herd_day_shift": int(plan.timing_shift),
        "PLANNER_OVERRIDES.herd_start_day":
            max(0, BRANCH_HERD_START_DAY[branch] - 1),
        "PLANNER_OVERRIDES.animal_buy_last_day_shift": int(plan.timing_shift),
        # —— P1 分支强制（缺口 4：计划动作包越过分类的接口位）——
        "PLANNER_OVERRIDES.b_branch_force": branch,
        # —— 规划器本地（信息性；执行器无对应旋钮/不安全参数化项）——
        "PLANNER_LOCAL.sell_discount": float(d),
        "PLANNER_LOCAL.animal_buy_day_shift": int(plan.timing_shift),
        "PLANNER_LOCAL.p3_mode": plan.p3_mode,
        "PLANNER_LOCAL.p4_clear": plan.p4_clear,
        "PLANNER_LOCAL.opening": plan.opening,
        "PLANNER_LOCAL.p1_branch": plan.p1_branch,
    }
    return dict(sorted(overrides.items()))


# --------------------------------------------------------------------------
# 整季经济投影器（相对排序机器；绝对数字以孪生 rollout 为准）
# --------------------------------------------------------------------------


def _fib_day_wage(crew: int) -> float:
    """日薪总额 ≈ fib(crew+1)-1（factsheet §5；crew=0 → 0）。"""
    a, b = 1, 1
    total = 0.0
    for _ in range(max(0, int(crew))):
        total += a
        a, b = b, a + b
    return total


def project_season(plan: PlanSpec, obs_summary, pressure=None) -> float:
    """整季经济投影：返回投影终局资金（相对排序用，非绝对预言）。

    模型（逐日、确定性、引擎常数锚定）：
      收入线：每线日收入 = 目标格数爬坡 × 单位日收入锚 × 吸收健康因子
              × sell_discount × pressure[item]；畜群线按头数与目标爬坡。
      吸收健康：clamp(daily_demand[item]/REF_DEMAND[item], 0.3, 1.2)
              （锚条件=v1.5 §5.3 表的健康商铺集）。
      成本：雇工 fib 日薪、外购饲料（产量不足头数×1麦/日，价 36）、
            买地（LAND 日程 + timing_shift）、买畜（目标爬坡期均摊 450/头）、
            种子（草莓/瓜一次性；小麦 2 日周期折 5/格/日）。
      简化（诚实声明）：不建模棚仓物流/日内外/对手逐回合压价的库存反馈、
            终局存货残值；两者都由 bench 的孪生 rollout 口径兜底。
    pressure: {item: factor}（对手模型供给压价系数，(0,1]；缺省全 1.0）。
    """
    pr = dict(pressure or {})
    t = plan_targets(plan)
    day0 = int(obs_summary.get("day", 0))
    money = float(obs_summary.get("money", 0.0))
    crops = obs_summary.get("crops") or {}
    herd = int(obs_summary.get("herd", 0))
    demand = obs_summary.get("daily_demand") or {}

    def health(item):
        base = REF_DEMAND.get(item, 8.0)
        if base <= 0:
            return 1.0
        return max(0.3, min(1.2, float(demand.get(item, base)) / base))

    def press(item):
        return max(0.0, min(1.0, float(pr.get(item, 1.0))))

    straw0 = int(crops.get("STRAWBERRY", 0))
    wheat0 = int(crops.get("WHEAT", 0))
    melon0 = int(crops.get("MELON", 0))
    carrot0 = int(crops.get("CARROT", 0))
    quads = int(obs_summary.get("unlocked_quadrants", 1))

    # P2.6 校准（2026-09-19，证据=c1_ablation.json/timing_diag.json）：
    #   a) 种植封笔——factsheet PLANT_LAST_DAY=14，day0 已封笔时田线目标=
    #      现状（封笔后新格既种不下也收不成，投影只剩畜群/土地经济）；
    #   b) 时点轴镜像——执行器 herd_day_shift=整条畜群日程沿日历平移，
    #      投影器同尺平移爬坡起点（修正前时点轴 J 零方差、恒被字典序
    #      tie-break 钉在 +0，42/42 注入点从不出现在选中计划）。
    closed = day0 >= PLANT_LAST_DAY
    herd_start = max(0, t["herd_start_day"] + int(plan.timing_shift))
    herd_span = max(1, 11 - t["herd_start_day"])

    for day in range(day0, 30):
        # —— 雇工爬坡（劳力先行：领先资产 <=1 天，v1.5 §5.3 规则 1）——
        crew_target = min(t["crew_cap"], CREW_BASE + max(0, day - day0)
                          // HIRE_RAMP_PER_DAYS)
        crew = max(int(obs_summary.get("crew", CREW_BASE)), crew_target)
        money -= _fib_day_wage(crew)

        # —— 买地（LAND 日程 + SE 窗；P2.6 起 doctrine 日程制、无现金门）——
        # 购地是计划的既定日程（v1.5 §2/LAND_PLAN），投影器是相对排序机器：
        # 现金门槛会把"谁凑得齐 fund"的彩票引入排序（实测反例：修掉种子
        # 幻影成本后，同一 obs 下中性 24223 < 悲观 27234——富变体恰好凑齐
        # 4600 买了对计划无产能价值的 Q4）。到期日早于注入日的按注入日
        # 补记（既定支出、与对手模型无关）；capacity 耦合见下节。
        for quad_key, (due, fund) in t["land_dues"].items():
            charge_day = max(int(due), day0)
            if day == charge_day and quads < 4:
                money -= fund
                quads += 1
        se_charge_day = max(int(t["se_due"]), day0)
        if day == se_charge_day and quads < 4:
            money -= SE_FUND_DEFAULT
            quads += 1

        # —— 田目标爬坡（建设期线性到 d14 冻结；草莓遵守 d13 满额死线；
        #     封笔后目标=现状；产能耦合：目标受已解锁象限 25 格/象限钳制
        #     ——10×10 板 ÷ 4 象限，factsheet tiles[10][10]——买地因此有
        #     真实收入语义，时点轴（买地提前/推后）随之可投影）——
        build_span = max(1, STRAW_DEADLINE_DAY - day0)
        frac = 1.0 if day >= PLANT_LAST_DAY else min(
            1.0, max(0.0, (day - day0) / build_span))
        straw_t = straw0 if closed else t["straw_total_cap"]
        melon_t = melon0 if closed else t["melon_total_cap"]
        wheat_t = wheat0 if closed else t["wheat_floor"]
        capacity = quads * TILES_PER_QUADRANT
        total_t = straw_t + wheat_t + melon_t
        if total_t > capacity:
            k = capacity / total_t
            straw_t = max(straw0, straw_t * k)
            wheat_t = max(wheat0, wheat_t * k)
            melon_t = max(melon0, melon_t * k)
        straw = straw0 + (straw_t - straw0) * frac
        melon = melon0 + (melon_t - melon0) * frac
        wheat = wheat0 + (wheat_t - wheat0) * frac
        carrot = carrot0  # 终盘弹性线（v1.5 §6：d23-27 才连种，投影不扩）
        herd_target = herd if day < herd_start else \
            herd + (t["herd_ceiling"] - herd) * min(
                1.0, max(0.0, (day - herd_start) / herd_span))

        # —— 收入（吸收健康 × 折扣 × 对手压力）——
        money += straw * REVENUE_ANCHORS["STRAWBERRY"] \
            * health("STRAWBERRY") * plan.sell_discount * press("STRAWBERRY")
        money += melon * REVENUE_ANCHORS["MELON"] * health("MELON") \
            * plan.sell_discount * press("MELON")
        money += carrot * REVENUE_ANCHORS["CARROT"] * health("CARROT") \
            * plan.sell_discount * press("CARROT")
        money += wheat * WHEAT_YIELD_PER_TILE_DAY * REVENUE_ANCHORS["WHEAT"] \
            * health("WHEAT") * plan.sell_discount * press("WHEAT")
        money += herd_target * REVENUE_ANCHORS["HERD"] * plan.sell_discount \
            * press("HERD")

        # —— 畜群成本（买畜均摊 + 饲料缺口外购；日程=平移后起点）——
        # P2.6 修正：买畜摊提加窗口守卫（爬坡窗内按 (顶-现)×450/span 摊提、
        # 总额=真实买畜款；修正前无守卫、爬坡完成后仍逐日计提到季末——
        # 幻影摊提使"推迟买畜"套利（时点轴方向被反转成 +2 最优，而 oracle
        # 面内最优 36/42 取 -2），且高顶档被多扣。证据同上。）
        if herd_target > herd and herd_start <= day < herd_start + herd_span:
            money -= max(0.0, t["herd_ceiling"] - herd) * ANIMAL_AVG_COST \
                / herd_span
        wheat_prod = wheat * WHEAT_YIELD_PER_TILE_DAY
        feed_gap = max(0.0, herd_target - wheat_prod)
        money -= feed_gap * ROLLOUT_FEED_PRICE

        # —— 种子成本（小麦 2 日周期 → 5/格/日 恒常；莓/瓜=建植一次性，
        #     只在建设窗 [day0, day0+build_span) 内摊入——P2.6 修正：修正前
        #     该项漏了窗口守卫、被逐日重复计到季末，d10 宽档幻影种子成本
        #     ~7×（C2 计 14000 而实义 2100）、d20 达 20×，是保守偏置
        #     （C1×0/配额 0.8 恒选）的主因；证据 c1_ablation.json：
        #     C1 oracle 面内最优 13/42 胜反应式、mean margin +1539）——
        money -= wheat * (SEED_PRICES["WHEAT"] / 2.0)
        if day < day0 + build_span:
            money -= max(0.0, straw - straw0) * SEED_PRICES["STRAWBERRY"] \
                / build_span
            money -= max(0.0, melon - melon0) * SEED_PRICES["MELON"] \
                / build_span

    return float(money)
