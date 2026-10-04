"""迁移登记——run_submission_agent · _exec_chain/planner/wave_script（B13，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/planner/wave_script.py（旧树冻结，零字节变更）
源 sha256: b2cd9dc2661140cd48a159699e0167d23d32633538d99e9999cdc422d3b8e66b
剥离清单（R10 死码不迁）: 无——零剥离——wave_script.py 无 R10 清单内符号（WAVE_CAL 为本件自持的权威日历镜像，与 src/wave.py 剥离项无消费关系）。
形态: 本文件 = 旧模块的迁移副本，落位 _exec_chain/planner/（planner 通道件，
  由 load_agent_modules 装载窗内 exec 成模块对象绑为 _wave 注入
  run_dawn_planner 命名空间——旧 `from . import wave_script as _wave` 的 exec 链等形）。
  除本登记头外源码逐字复制（stdlib 绝对导入在 exec 下原样成立）。
上游: R1（fn_docs/responsibility.md 功能块 run_submission_agent · run_dawn_planner）
"""

# ===========================================================================
# 【中文·模块导览】planner/wave_script.py —— DTSP 剧本候选（v15「点火重构」M-C）
# ---------------------------------------------------------------------------
# 职责：把"验证过的波次日历剧本"作为 DTSP 黎明三选一的比较候选之一
#   （{wave-script 当前段, identity 守成, 旋钮变体}，孪生 rollout 仲裁 +
#   τ 闸沿用）。纪律（战略裁决 2026-09-20）：
#     * 剧本自身不进 rollout 重规划（它是验证过的）——沙盒侧剧本行为由
#       src/wave.py 经 "PLANNER_OVERRIDES.wave_mode" 旋钮执行，本模块不
#       发射任何日程重排；
#     * rollouts 只裁"剧本 vs 守成 vs 变体"。
# 权威日历表唯一出处 = src/wave.py（沙盒与线上同一消费面）；本模块只保
#   持一份"尾段投影镜像"（日历常数与 src 逐值一致，tests/test_wave_script.
#   py 钉住两表面等价）——planner 不 import src（P3 纪律：planner 包独立
#   装载，src 沙盒由 runtime.build_sandbox_agent 装载）。
# 纪律：stdlib-only、确定性、无 I/O。
# ===========================================================================

# 剧本候选的规范键（参与 rollout 聚合/排序/tie-break，与其他 PlanSpec 键
# 同一命名空间且必然字典序可排；"WAVE|" 前缀保证与 "P|..." 键不相撞）。
WAVE_KEY = "WAVE|v15|ignition"

# 剧本模式的注入面：总旗（_plan_knob 读寄存器的前置）+ 唯一模式键——
# src/wave.py 的全部消费点读 _plan_knob("wave_mode", WAVE_ENABLED)。
WAVE_KNOB_OVERRIDES = {"PLANNER_ENABLED": True,
                       "PLANNER_OVERRIDES.wave_mode": True}

# ---- 尾段投影镜像（与 src/wave.py 权威表逐值一致；测试钉住）--------------
# 出处：v48 default 逐日表 + island-ga envelope + 2945 VE1（模块头详注）。
WAVE_CAL = {
    "crew_ladder": ((0, 5), (5, 6), (8, 8), (10, 12), (11, 13), (13, 12)),
    "opening_herd": {"COW": 2, "SHEEP": 2},
    "herd_waves": {6: {"COW": 5}},
    "herd_waves_yarn": {11: {"SHEEP": 6}},
    "land_waves": {1: (6, 1300), 2: (10, 2300)},
    "flush": {"WOOL": (6, 7, 8), "MELON": (10, 11)},
    "milk_flush_from": 8,
    "melon_tiles": 7,
    "glut": {"MELON": 3.6, "WOOL": 3.2, "STRAWBERRY": 2.0, "MILK": 2.0},
    "d0_cost": 2 * 400 + 2 * 500 + 7 * 80 + 9 * 10,   # 2530（过夜 ≤600 ✓）
}

# 相对排序锚（单位日收入，来源 plans.REVENUE_ANCHORS 同量级；仅用于
# rollout 尾段的"余季延续"打分，与 project_season 同为相对排序机器）。
_ANCHOR = {"WOOL": 40.0, "MILK": 40.0, "STRAWBERRY": 25.0, "MELON": 30.0}


class WaveCandidate:
    """剧本候选（duck-typed PlanSpec：key()/to_dict() 同接口；wave=True
    供 runtime 分派 knob_overrides()/tail_score()）。"""

    wave = True

    def key(self) -> str:
        return WAVE_KEY

    def to_dict(self) -> dict:
        return {"wave": True, "key": WAVE_KEY}

    def knob_overrides(self) -> dict:
        """沙盒/线上注入面：只开剧本总闸（src/wave.py 承载全部行为）。"""
        return dict(WAVE_KNOB_OVERRIDES)

    def tail_score(self, tail_summary) -> float:
        """rollout 地平线末态的"剧本余季延续"投影（相对排序用）。

        tail_summary: plans.build_obs_summary 键面的局况摘要。模型：
          crew 阶梯对应的畜群波次年金（WOOL/MILK 流）+ 在田莓线年金，
          按 tail 日对齐剧本日历；不建模对手（与投影器同一诚实声明）。
        """
        if not tail_summary:
            return 0.0
        day = int(tail_summary.get("day", 0) or 0)
        herd = int(tail_summary.get("herd", 0) or 0)
        crops = tail_summary.get("crops") or {}
        straw = int(crops.get("STRAWBERRY", 0) or 0)
        # 剧本口径的畜群波次年金：按剩余夜晚数折年金（首产已建成的部分）。
        herd_income = min(herd, 16) * _ANCHOR["MILK"] * max(0, 28 - day) * 0.5
        straw_income = straw * _ANCHOR["STRAWBERRY"] * max(0, 28 - day) * 0.5
        return float(herd_income + straw_income)


def wave_candidate() -> WaveCandidate:
    """剧本候选工厂（dawn 三选一比较集恒含）。"""
    return WaveCandidate()
