"""对手名册单源真值（11 对手池+网格口径），bots/__init__×2、STANDARD_MATRIX_ORDER、EXPECTED_ELO_ORDER、holdout_matrix_order、REQUIRED_OPPONENTS 全部改为引用。

上游: R8, R9（详见 fn_docs/responsibility.md）

实现要点（[改造]件，读旧树 5 处定义+网格定真值）：
- 旧定义站点（等值断言对象，战后统一改引本模块）：
    S1 kgenv/bots/__init__.py:14 STRONG_OPPONENTS（3）
    S2 kgenv/bots/__init__.py:28 ONLINE_STYLE_OPPONENTS（7）
    S3 kgenv/eval_contract.py:20 STANDARD_MATRIX_ORDER（9，含 submission）
    S4 kgenv/regression.py:47 EXPECTED_ELO_ORDER（6）+ :56 FROZEN_POOL
    S5 kgenv/holdout_contract.py HOLDOUT_V2..V5_MATRIX_ORDER +
       holdout_matrix_order(attempt_index)（V1=STANDARD，2/9、3/10、4/11、5/12）
- 网格口径（scripts 侧两站点，不 import 旧 scripts/，测试内字面锚定）：
    G1 scripts/check_eval_contract.py:27 REQUIRED_OPPONENTS（9——m2 期网格：
       11 对手池减 wheat_straw_monster/two_quad_denser）×种子 101-104×AB/BA，
       GATE_GAMES_PER_OPPONENT=8
    G2 scripts/iterate_gate.py:52 REQUIRED_OPPONENTS = GATE(2)+GUARD(2)+
       ONLINE(7) = 11 对手池真值本体（scripts/ablate.py 同一口径重组）
- 11 对手池 = GATE_OPPONENTS + GUARD_OPPONENTS + ONLINE_STYLE_OPPONENTS，
  与 S1∪S2∪{baseline_wheat} 集合一致（三处站点交叉印证）。
- 种子域：development=101-104，regression=201-208（eval_contract 口径）；
  座位协议 AB/BA（build_ab_ba_schedule 口径）。
- single_opponent_roster() 返回整份真值 dict（只读快照，调用方不得改）；
  模块级常量供逐站点精确引用。

适配说明（旧树冻结——物理改线属战后，登记于此）：
- 战后 S1-S5 改为 `from <本包>.single_opponent_roster import ...` 的引用；
  scripts 侧 G1/G2 改引 GRID_REQUIRED_OPPONENTS / OPPONENT_POOL_11。
  本模块为名册唯一真值源，旧 5 处字面在改线完成前以等值断言看护
  （见顶层 unify_contract_sources 与测试字面锚）。
"""

from __future__ import annotations

from typing import Dict, Tuple

__all__ = [
    "SUBMISSION",
    "GATE_OPPONENTS", "GUARD_OPPONENTS", "STRONG_OPPONENTS",
    "ONLINE_STYLE_OPPONENTS", "OPPONENT_POOL_11", "GRID_REQUIRED_OPPONENTS",
    "AUXILIARY_LADDER_OPPONENTS",
    "STANDARD_MATRIX_ORDER", "STANDARD_OFFICIAL_PAIRS_COUNT",
    "EXPECTED_ELO_ORDER", "FROZEN_POOL",
    "HOLDOUT_MATRIX_ORDERS", "DEVELOPMENT_SEEDS", "REGRESSION_SEEDS",
    "SEAT_PROTOCOL", "GRID_GAMES_PER_OPPONENT",
    "single_opponent_roster",
]

SUBMISSION = "submission"

# ---- 分组真值（bots/__init__ S1/S2 + iterate_gate G2 的分组口径） ---- #
GATE_OPPONENTS: Tuple[str, ...] = ("cow_baron", "melon_hoarder")
GUARD_OPPONENTS: Tuple[str, ...] = ("expansionist", "baseline_wheat")
STRONG_OPPONENTS: Tuple[str, ...] = ("cow_baron", "melon_hoarder",
                                     "expansionist")
ONLINE_STYLE_OPPONENTS: Tuple[str, ...] = (
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
    "wheat_straw_monster",
    "two_quad_denser",
)

# ---- 11 对手池真值本体（iterate_gate REQUIRED_OPPONENTS 组装序） ---- #
OPPONENT_POOL_11: Tuple[str, ...] = (GATE_OPPONENTS + GUARD_OPPONENTS +
                                      ONLINE_STYLE_OPPONENTS)
assert len(OPPONENT_POOL_11) == 11  # 11 对手池口径自检（缺一即错）
assert (set(OPPONENT_POOL_11) == set(STRONG_OPPONENTS) | {"baseline_wheat"}
        | set(ONLINE_STYLE_OPPONENTS))  # 三站点分组集合交叉印证

# ---- m2 网格口径（check_eval_contract.py G1 字面序） ---- #
GRID_REQUIRED_OPPONENTS: Tuple[str, ...] = (
    "cow_baron",
    "melon_hoarder",
    "expansionist",
    "baseline_wheat",
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
)

# ---- 阶梯辅件位（greedy_carrot 本地 baseline；starter/random/pass 引擎内置） ---- #
AUXILIARY_LADDER_OPPONENTS: Tuple[str, ...] = ("greedy_carrot", "starter",
                                               "random", "pass")

# ---- 标准矩阵与冻结天梯（eval_contract S3 / regression S4） ---- #
STANDARD_MATRIX_ORDER: Tuple[str, ...] = (
    "submission", "cow_baron", "melon_hoarder", "expansionist",
    "baseline_wheat", "greedy_carrot", "starter", "random", "pass",
)
STANDARD_OFFICIAL_PAIRS_COUNT = 36  # C(9,2)

EXPECTED_ELO_ORDER: Tuple[str, ...] = (
    "submission",
    "baseline_wheat",
    "greedy_carrot",
    "starter",
    "pass",
    "random",
)
FROZEN_POOL = frozenset(EXPECTED_ELO_ORDER)

# ---- holdout 世代矩阵（holdout_contract S5；1=STANDARD） ---- #
HOLDOUT_MATRIX_ORDERS: Dict[int, Tuple[str, ...]] = {
    1: STANDARD_MATRIX_ORDER,
    2: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified"),
    3: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch"),
    4: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch",
        "wheat_straw_monster"),
    5: ("submission", "cow_baron", "melon_hoarder", "expansionist",
        "baseline_wheat", "crop_rotator", "template_wheat",
        "self_feed_ranch", "near_band_diversified", "scale_ranch",
        "wheat_straw_monster", "two_quad_denser"),
}

# ---- 种子域与网格口径（eval_contract / build_ab_ba_schedule / G1） ---- #
DEVELOPMENT_SEEDS: Tuple[int, ...] = (101, 102, 103, 104)
REGRESSION_SEEDS: Tuple[int, ...] = (201, 202, 203, 204, 205, 206, 207, 208)
SEAT_PROTOCOL: Tuple[str, ...] = ("AB", "BA")
GRID_GAMES_PER_OPPONENT = len(DEVELOPMENT_SEEDS) * len(SEAT_PROTOCOL)  # 8


def single_opponent_roster() -> dict:
    """返回对手名册单源真值快照（只读语义；调用方不得原地修改）。

    Returns:
        dict 键集：
          submission / gate_opponents / guard_opponents / strong_opponents /
          online_style_opponents —— 分组真值（tuple）；
          opponent_pool_11 —— 11 对手池本体（GATE+GUARD+ONLINE 组装序）；
          grid —— m2 网格口径：required_opponents(9) + development_seeds +
              seat_protocol + games_per_opponent(8)；
          auxiliary_ladder_opponents —— 阶梯辅件位（greedy_carrot/starter/
              random/pass）；
          standard_matrix_order / standard_official_pairs_count —— S3；
          expected_elo_order / frozen_pool —— S4；
          holdout_matrix_orders —— {世代 1..5: 矩阵序}（S5）；
          regression_seeds —— 201-208。
    """
    return {
        "submission": SUBMISSION,
        "gate_opponents": GATE_OPPONENTS,
        "guard_opponents": GUARD_OPPONENTS,
        "strong_opponents": STRONG_OPPONENTS,
        "online_style_opponents": ONLINE_STYLE_OPPONENTS,
        "opponent_pool_11": OPPONENT_POOL_11,
        "grid": {
            "required_opponents": GRID_REQUIRED_OPPONENTS,
            "development_seeds": DEVELOPMENT_SEEDS,
            "seat_protocol": SEAT_PROTOCOL,
            "games_per_opponent": GRID_GAMES_PER_OPPONENT,
        },
        "auxiliary_ladder_opponents": AUXILIARY_LADDER_OPPONENTS,
        "standard_matrix_order": STANDARD_MATRIX_ORDER,
        "standard_official_pairs_count": STANDARD_OFFICIAL_PAIRS_COUNT,
        "expected_elo_order": EXPECTED_ELO_ORDER,
        "frozen_pool": frozenset(FROZEN_POOL),
        "holdout_matrix_orders": dict(HOLDOUT_MATRIX_ORDERS),
        "regression_seeds": REGRESSION_SEEDS,
    }
