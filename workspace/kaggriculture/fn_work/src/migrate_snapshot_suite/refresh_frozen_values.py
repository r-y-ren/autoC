"""仅更新受 R2/R3 修复影响的冻结值（select 名字序→值序、bench 错位→seated），每处留旧值/新值/原因双口径注记，其余冻结值零改动。

上游: R1（详见 fn_docs/responsibility.md）

实现要点（[改造]件，W1 收口）：
- 作用面=迁移目标目录（<战役根>/fn_work/tests/snapshot/ 的九文件副本或其
  tmp 副本）；旧 snapshot_tests/ 只读，本函数绝不触碰源套件。
- 白名单圈禁：只许改 test_counterexample_r2.py / test_counterexample_r3.py
  / test_planner_select_characterization.py 三件（R2/R3 修复影响面）；
  agent 整局旗关冻结、评级、契约、台账四测试文件与 README 零字节改动
  （调用方 migrate_snapshot_suite 另行做逐字节比对复核）。
- 变更全部走锚定编辑表 _EDITS：每条 = 文件 + 唯一锚文本（old）+ 新文本
  （new）+ 注记。锚文本必须恰出现一次（fail-closed），因此白名单文件内
  除编辑块外的每一个字节都保持原样——"其余冻结值零改动"是结构保证，
  不靠自觉。三类编辑：
    value         冻结值刷新（名字序→值序 / 错位→seated），逐条双口径注记
                  （旧值/新值/原因=R2/R3 修复）落入文件正文与返回注记；
    xfail_convert R2/R3 快照反例的 strict xfail 装饰器摘除、断言转常规
                  （fn_work 实现应通过它们）；
    redirect      R2/R3 相关 import 重定向（select/bench → fn_work 实现，
                  路径经 sys.path 由迁移版 conftest 装配，不写字面战役路径）
                  与随实现签名变化的调用面适配——非冻结值变更，不入注记。
- 影响清单纪律：impact_list 是编辑授权面。value/xfail_convert 编辑的
  (file, locator) 必须逐条被 impact_list 授权，impact_list 也不得含无
  对应编辑的项或白名单外文件——任何越界即 ValueError 且不写任何文件
  （先全量校验后落盘，fail-closed）。
- 重复应用防御：锚文本在已刷新副本中不再命中 → ValueError（幂等性归
  migrate_snapshot_suite 的复制步保证：每次自源套件全新复制后再刷新）。
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "SUITE_FILES", "WHITELIST", "UNTOUCHED_FILES", "DEFAULT_IMPACT_LIST",
    "PROTECTED_ANCHORS", "check_protected_anchors", "refresh_frozen_values",
]

# 快照套件九文件（conftest.py 在迁移时由 migrate_snapshot_suite 重写为双根
# 装配版，不属本函数职责；其余八件自源复制）
SUITE_FILES = (
    "conftest.py",
    "README.md",
    "test_agent_characterization.py",
    "test_counterexample_r2.py",
    "test_counterexample_r3.py",
    "test_eval_contract_rules.py",
    "test_kgenv_rating_snapshots.py",
    "test_online_probe_gate_rules.py",
    "test_planner_select_characterization.py",
)

# R2/R3 修复影响面（白名单）：唯一许可本函数改动的文件
WHITELIST = (
    "test_counterexample_r2.py",
    "test_counterexample_r3.py",
    "test_planner_select_characterization.py",
)

# 逐字节不动件（冻结值零改动的对照面；conftest 除外——迁移时重写）
UNTOUCHED_FILES = (
    "README.md",
    "test_agent_characterization.py",
    "test_eval_contract_rules.py",
    "test_kgenv_rating_snapshots.py",
    "test_online_probe_gate_rules.py",
)

# 刷新后必须仍在场的受保护冻结字面量（跨口径不变的锚：输入构造、常量、
# worst_case/weighted/退化尺寸/输入校验/K1 阈值与回放真值等）
PROTECTED_ANCHORS = {
    "test_counterexample_r2.py": (
        "FROZEN_REPLAY_REWARDS = [3000.0, 1570.0]",
        "FROZEN_BENCH_MISSEATED_FINAL = [1570.0, 3000.0]",
        'env = make("kaggriculture",',
    ),
    "test_counterexample_r3.py": (
        "CASE_A = {WB: 60.0, WS: 100.0, PE: 10.0, PF: 70.0}",
        "CASE_B = {WB: 80.0, WS: 5.0, PE: 40.0, PF: 1.0}",
        'assert _value_order_trimmed_mean(CASE_A) == 65.0',
    ),
    "test_planner_select_characterization.py": (
        'assert AGGREGATION_STRATEGIES == ("trimmed_mean", "worst_case", "weighted")',
        "assert DEFAULT_TRIM_FRACTION == 0.25",
        "assert IDENTITY_TIEBREAK_TAU == 0.005",
        'assert aggregate_scores(CASE_A, strategy="worst_case") == 10.0',
        ") == 68.75",
        "assert aggregate_scores({PF: 42.5}) == 42.5",
        "assert aggregate_scores({\"a\": 1.0, \"b\": 3.0}) == 2.0",
        'assert aggregate_scores(p1, strategy="worst_case") == 10.0',
        'assert aggregate_scores(p2, strategy="worst_case") == 50.0',
        'match="trim_fraction"',
    ),
}


# ---------------------------------------------------------------------------
# 锚定编辑表（唯一事实源：迁移副本与源件的全部差异都在这些块内）
# ---------------------------------------------------------------------------

def _e(file, kind, locator, old, new,
       old_value="", new_value="", reason=""):
    return {"file": file, "kind": kind, "locator": locator, "old": old,
            "new": new, "old_value": old_value, "new_value": new_value,
            "reason": reason}


_EDITS = [
    # ======================= test_counterexample_r2.py =====================
    _e("test_counterexample_r2.py", "note", "<module-header>",
       """# xfail(strict) 断言：bench 通道 == 回放真值（"我方动作注入到我方实际
# 席位"的正确语义）。旧代码失败（套件绿）；R2 修复后 XPASS ⇒ strict
# 套件变红 = 提示反例已修、可迁移。对照断言（普通、保绿）固化 bench
# 当前错位输出与 seated 正确输出。
# ===========================================================================""",
       """# xfail(strict) 断言：bench 通道 == 回放真值（"我方动作注入到我方实际
# 席位"的正确语义）。旧代码失败（套件绿）；R2 修复后 XPASS ⇒ strict
# 套件变红 = 提示反例已修、可迁移。对照断言（普通、保绿）固化 bench
# 当前错位输出与 seated 正确输出。
# ---------------------------------------------------------------------------
# 【迁移记录 2026-09-21 · migrate_snapshot_suite（W1 收口）】本文件随套件
# 迁入 fn_work/tests/snapshot/：bench 通道重定向至 fn_work/src/
# run_official_bench 的 seated 实现（R2 已修），strict xfail 转常规断言，
# 对照冻结值按 seated 口径刷新（逐处双口径注记：旧值/新值/原因）；
# seated 参照臂与 twin 仍指向旧树（当前真值）。旧 snapshot_tests/ 原件
# 不动（仍钉错位口径旧值）。
# ==========================================================================="""),
    _e("test_counterexample_r2.py", "redirect", "twin_deps",
       """@pytest.fixture(scope="module")
def twin_deps():
    import planner_offline_bench as bench
    return bench.make_twin_deps()""",
       """@pytest.fixture(scope="module")
def twin_deps():
    # 【R2 重定向·迁移】依赖组改经 fn_work make_twin_deps（原
    # planner_offline_bench.make_twin_deps；键契约含 v143 参照通道消费的
    # step/final，引擎装载指纹链 fail-closed 保留）。
    from run_official_bench.rollout_with_replay_opponent import make_twin_deps
    return make_twin_deps()"""),
    _e("test_counterexample_r2.py", "redirect", "_run_bench",
       """def _run_bench(deps, replay, me_seat, agent_factory=_seed_buyer_bot):
    import planner_offline_bench as bench
    from kaggle_simulations.agent.planner import twin
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    return bench.rollout_with_replay_opponent(
        deps, state, me_seat, agent_factory(), acts, 0)""",
       """def _run_bench(deps, replay, me_seat, agent_factory=_seed_buyer_bot):
    # 【R2 重定向·迁移】bench 通道 → fn_work/src/run_official_bench 的
    # seated 实现（原 planner_offline_bench.rollout_with_replay_opponent）。
    # 调用形态随新签名：回放/注入点由通道内重建（幂等；deps 参数保留作
    # 调用面兼容），返回双席终局资金（序=seat0,seat1，无 taken 返回）。
    from run_official_bench.rollout_with_replay_opponent import (
        rollout_with_replay_opponent)
    return rollout_with_replay_opponent(replay, 0, agent_factory(), me_seat)"""),
    _e("test_counterexample_r2.py", "value",
       "test_bench_current_misseated_output_frozen",
       '''def test_bench_current_misseated_output_frozen(synthetic_replay, twin_deps):
    """对照断言：bench 通道 me_seat=1 的当前（错位）输出 = 双席资金互换。"""
    (final, taken) = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_BENCH_MISSEATED_FINAL
    assert final != FROZEN_REPLAY_REWARDS
    assert taken == EPISODE_STEPS - 1''',
       '''def test_bench_current_misseated_output_frozen(synthetic_replay, twin_deps):
    """对照断言（迁移后 seated 口径）。

    【双口径注记】旧值 [1570.0, 3000.0]（错位口径：旧 bench 恒 seat0
    注入 → 双席资金互换伪影）/ 新值 [3000.0, 1570.0]（seated 口径，
    =回放真值）/ 原因=R2 修复（fn_work 通道上提 v143 seated 语义）。
    FROZEN_BENCH_MISSEATED_FINAL 常量留档为负锚——修复后不得再出此值。
    """
    final = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS
    assert final != FROZEN_BENCH_MISSEATED_FINAL''',
       old_value="[1570.0, 3000.0]（错位口径）",
       new_value="[3000.0, 1570.0]（seated 口径）",
       reason="R2"),
    _e("test_counterexample_r2.py", "redirect",
       "test_bench_me_seat0_matches_seated",
       '''def test_bench_me_seat0_matches_seated(synthetic_replay, twin_deps):
    """me_seat=0 时 bench 与 seated 逐字节同（错位仅在 me_seat=1 显形）。

    用 seat0 的回放人格（恒 PASS bot）驱动我方席：两通道都把动作注入
    seat0、对手席由回放 seat1 磁带驱动 → 双双精确复现回放真值。"""
    bench_final, _ = _run_bench(twin_deps, synthetic_replay, 0,
                                agent_factory=lambda: _pass_bot)
    seated_final, _ = _run_seated(twin_deps, synthetic_replay, 0,
                                  agent_factory=lambda: _pass_bot)
    assert bench_final == seated_final == FROZEN_REPLAY_REWARDS''',
       '''def test_bench_me_seat0_matches_seated(synthetic_replay, twin_deps):
    """me_seat=0 时 bench 与 seated 逐字节同（错位仅在 me_seat=1 显形）。

    用 seat0 的回放人格（恒 PASS bot）驱动我方席：两通道都把动作注入
    seat0、对手席由回放 seat1 磁带驱动 → 双双精确复现回放真值。
    【R2 迁移·口径注记】bench 臂改走 fn_work seated 通道（返回仅双席
    终局资金，无 taken）；seated 臂仍经旧树 v143 参照实现；原因=R2 修复
    不改 me_seat=0 语义（旧值=新值=回放真值，此断言无值变化）。"""
    bench_final = _run_bench(twin_deps, synthetic_replay, 0,
                             agent_factory=lambda: _pass_bot)
    seated_final, _ = _run_seated(twin_deps, synthetic_replay, 0,
                                  agent_factory=lambda: _pass_bot)
    assert bench_final == seated_final == FROZEN_REPLAY_REWARDS'''),
    _e("test_counterexample_r2.py", "xfail_convert",
       "test_bench_rollout_injects_into_actual_seat",
       '''@pytest.mark.xfail(
    strict=True,
    reason="R2 快照反例：旧 bench.rollout_with_replay_opponent 恒 mine→seat0"
           "（席位错位），新结构上提 seated 通道后此测试应 XPASS")
def test_bench_rollout_injects_into_actual_seat(synthetic_replay, twin_deps):
    """R2 验收面：bench 通道对 me_seat=1 也应把动作注入实际席位
    （即与回放真值一致）。旧代码输出互换伪影 → 此断言失败。"""
    (final, _taken) = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS''',
       '''def test_bench_rollout_injects_into_actual_seat(synthetic_replay, twin_deps):
    """R2 验收面（xfail 转常规·迁移）：bench 通道（fn_work seated 实现）
    对 me_seat=1 也把动作注入实际席位（即与回放真值一致）。

    【双口径注记】旧=strict xfail（旧 bench 恒 seat0 注入 → 互换伪影
    [1570.0, 3000.0]，套件保绿）/ 新=常规通过（原因=R2 修复）。"""
    final = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS''',
       old_value="strict xfail（旧 bench 恒 seat0 注入 → 互换伪影）",
       new_value="常规通过（fn_work seated 实现）",
       reason="R2"),
    # ======================= test_counterexample_r3.py =====================
    _e("test_counterexample_r3.py", "redirect", "<module-import>",
       '''import pytest

from kaggle_simulations.agent.planner.select import aggregate_scores''',
       '''# 【R3 重定向·迁移】select 实现 → fn_work/src/robust_selection（值序
# 裁切修复所在包）；xfail 转常规后本文件不再使用 pytest。
from robust_selection.aggregate_scores import aggregate_scores'''),
    _e("test_counterexample_r3.py", "xfail_convert",
       "test_value_order_trimmed_mean_case_a",
       '''@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：旧 select.py 按名字序裁切（悲观模型恒被裁），"
           "新结构改为值序裁切后此测试应 XPASS")
def test_value_order_trimmed_mean_case_a():
    assert aggregate_scores(CASE_A) == 65.0''',
       '''def test_value_order_trimmed_mean_case_a():
    # 【xfail 转常规·迁移】旧=strict xfail（名字序裁切，断言失败保绿）/
    # 新=常规通过（原因=R3 修复：fn_work 值序裁切）。
    assert aggregate_scores(CASE_A) == 65.0''',
       old_value="strict xfail（名字序裁切，断言失败）",
       new_value="常规通过（值序裁切）",
       reason="R3"),
    _e("test_counterexample_r3.py", "xfail_convert",
       "test_value_order_trimmed_mean_case_b_pessimistic_restored",
       '''@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：旧 select.py 按名字序裁切（悲观模型恒被裁），"
           "新结构改为值序裁切后此测试应 XPASS")
def test_value_order_trimmed_mean_case_b_pessimistic_restored():
    assert aggregate_scores(CASE_B) == 22.5''',
       '''def test_value_order_trimmed_mean_case_b_pessimistic_restored():
    # 【xfail 转常规·迁移】旧=strict xfail / 新=常规通过（原因=R3 修复）。
    assert aggregate_scores(CASE_B) == 22.5''',
       old_value="strict xfail（名字序裁切，断言失败）",
       new_value="常规通过（值序裁切）",
       reason="R3"),
    _e("test_counterexample_r3.py", "xfail_convert",
       "test_pessimistic_score_moves_aggregate_under_value_order",
       '''@pytest.mark.xfail(
    strict=True,
    reason="R3 快照反例：值序裁切下悲观模型分数变动必须改变聚合值；"
           "旧代码（名字序恒裁 pessimistic_fill）无感，新结构应 XPASS")
def test_pessimistic_score_moves_aggregate_under_value_order():
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    # 值序：lo → 裁 {10,70} 保留 [50,60] → 55.0；
    #       hi → 裁 {50,70} 保留 [60,65] → 62.5。两者必须不同。
    assert aggregate_scores(lo) == 55.0
    assert aggregate_scores(hi) == 62.5
    assert aggregate_scores(lo) != aggregate_scores(hi)''',
       '''def test_pessimistic_score_moves_aggregate_under_value_order():
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    # 值序：lo → 裁 {10,70} 保留 [50,60] → 55.0；
    #       hi → 裁 {50,70} 保留 [60,65] → 62.5。两者必须不同。
    # 【xfail 转常规·迁移】旧=strict xfail / 新=常规通过（原因=R3 修复）。
    assert aggregate_scores(lo) == 55.0
    assert aggregate_scores(hi) == 62.5
    assert aggregate_scores(lo) != aggregate_scores(hi)''',
       old_value="strict xfail（名字序恒裁 pessimistic_fill 无感）",
       new_value="常规通过（值序下悲观分数变动改变聚合）",
       reason="R3"),
    _e("test_counterexample_r3.py", "note", "<contrast-section-comment>",
       '''# ---------------------------------------------------------------------------
# 对照断言：旧代码当前行为（名字序裁切），普通断言保绿。
# 修复 R3 时这三条会变红——届时按 README 迁移约定更新冻结值。
# ---------------------------------------------------------------------------''',
       '''# ---------------------------------------------------------------------------
# 对照断言（迁移后按值序口径刷新）：逐条双口径注记留档（旧名字序值 →
# 新值序值）；旧 snapshot_tests/ 原件仍钉名字序旧值不动。
# ---------------------------------------------------------------------------'''),
    _e("test_counterexample_r3.py", "value",
       "test_current_name_order_behavior_case_a",
       '''def test_current_name_order_behavior_case_a():
    assert aggregate_scores(CASE_A) == 35.0''',
       '''def test_current_name_order_behavior_case_a():
    # 【双口径注记】旧值 35.0（名字序裁切：裁 {ws=100, pf=70} 保留
    # [60,10]）/ 新值 65.0（值序裁切：裁 {10,100} 保留 [60,70]）/
    # 原因=R3 修复。
    assert aggregate_scores(CASE_A) == 65.0''',
       old_value="35.0（名字序裁切）",
       new_value="65.0（值序裁切）",
       reason="R3"),
    _e("test_counterexample_r3.py", "value",
       "test_current_name_order_behavior_case_b",
       '''def test_current_name_order_behavior_case_b():
    assert aggregate_scores(CASE_B) == 60.0''',
       '''def test_current_name_order_behavior_case_b():
    # 【双口径注记】旧值 60.0（名字序：裁 {ws=5, pf=1} 保留 [80,40]）/
    # 新值 22.5（值序：裁 {1,80} 保留 [5,40]——悲观信号恢复效力）/
    # 原因=R3 修复。
    assert aggregate_scores(CASE_B) == 22.5''',
       old_value="60.0（名字序裁切）",
       new_value="22.5（值序裁切）",
       reason="R3"),
    _e("test_counterexample_r3.py", "value",
       "test_current_pessimistic_zero_effect",
       '''def test_current_pessimistic_zero_effect():
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    assert aggregate_scores(lo) == aggregate_scores(hi) == 60.0''',
       '''def test_current_pessimistic_zero_effect():
    # 【双口径注记】旧值 lo==hi==60.0（名字序恒裁 pessimistic_fill →
    # 悲观零效力）/ 新值 lo=55.0、hi=62.5 且 lo!=hi（值序：悲观分数
    # 变动恢复改变聚合）/ 原因=R3 修复。
    lo = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    hi = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    assert aggregate_scores(lo) == 55.0
    assert aggregate_scores(hi) == 62.5
    assert aggregate_scores(lo) != aggregate_scores(hi)''',
       old_value="lo==hi==60.0（悲观零效力）",
       new_value="lo=55.0、hi=62.5 且 lo!=hi（悲观恢复效力）",
       reason="R3"),
    # ============== test_planner_select_characterization.py ===============
    _e("test_planner_select_characterization.py", "redirect",
       "<module-import>",
       '''import pytest

from kaggle_simulations.agent.planner.select import (
    AGGREGATION_STRATEGIES,
    DEFAULT_TRIM_FRACTION,
    IDENTITY_TIEBREAK_TAU,
    aggregate_scores,
    robust_select,
)''',
       '''import pytest

# 【R3 重定向·迁移】select 实现 → fn_work/src/robust_selection（值序
# 裁切修复所在包）；函数名 robust_select→robust_selection（对齐包名，
# 调用点随迁改名）；受影响冻结值按值序口径刷新，逐处双口径注记。
from robust_selection.aggregate_scores import (
    AGGREGATION_STRATEGIES,
    DEFAULT_TRIM_FRACTION,
    aggregate_scores,
)
from robust_selection.robust_selection import (
    IDENTITY_TIEBREAK_TAU,
    robust_selection,
)'''),
    _e("test_planner_select_characterization.py", "note", "<module-header>",
       '''# 冻结值全部手算复核（2026-09-21，Python 3.14.7 实测一致）。
# ===========================================================================''',
       '''# 冻结值全部手算复核（2026-09-21，Python 3.14.7 实测一致）。
# ---------------------------------------------------------------------------
# 【迁移记录 2026-09-21 · migrate_snapshot_suite（W1 收口）】本文件随套件
# 迁入 fn_work/tests/snapshot/：select 断言重定向至 fn_work/src/
# robust_selection（R3 值序裁切），受影响冻结值按值序口径刷新、逐处双
# 口径注记；其余冻结值（模块常量/worst_case/weighted/退化尺寸/输入
# 校验/K1 守成语义）不变。旧 snapshot_tests/ 原件不动（仍钉名字序旧值）。
# ==========================================================================='''),
    _e("test_planner_select_characterization.py", "value",
       "test_aggregate_trimmed_mean_name_order_cut",
       '''def test_aggregate_trimmed_mean_name_order_cut():
    # 现行行为：按名字序裁切。Ω=4 → trim=floor(4*0.25)=1，
    # 名字序值向量 [100.0(ws), 60.0(wb), 10.0(pe), 70.0(pf)]
    # → kept=values[1:3]=[60.0, 10.0] → 35.0。
    assert aggregate_scores(CASE_A) == 35.0''',
       '''def test_aggregate_trimmed_mean_name_order_cut():
    # 【双口径注记】旧值 35.0（名字序裁切：值向量 [100.0(ws), 60.0(wb),
    # 10.0(pe), 70.0(pf)] → kept=[60.0,10.0]）/ 新值 65.0（值序裁切：
    # 排序 [10,60,70,100] → kept=[60,70]）/ 原因=R3 修复。
    assert aggregate_scores(CASE_A) == 65.0''',
       old_value="35.0（名字序裁切）",
       new_value="65.0（值序裁切）",
       reason="R3"),
    _e("test_planner_select_characterization.py", "value",
       "test_pessimistic_fill_zero_effect_under_name_order_cut",
       '''def test_pessimistic_fill_zero_effect_under_name_order_cut():
    # G2/R3 的行为后果：pessimistic_fill 名字序恒最后 → 恒被裁。
    # 只改 pessimistic 分数（10.0 → 65.0，跨越保留段），聚合值纹丝不动。
    p1 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    p2 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    # 名字序 [ws:60, wb:50, pe:70, pf:*] → kept=[50.0, 70.0] → 60.0。
    assert aggregate_scores(p1) == 60.0
    assert aggregate_scores(p2) == 60.0
    # 对照：worst_case 聚合能感知 pessimistic 变动（缺陷仅在 trimmed_mean）。
    assert aggregate_scores(p1, strategy="worst_case") == 10.0
    assert aggregate_scores(p2, strategy="worst_case") == 50.0''',
       '''def test_pessimistic_fill_zero_effect_under_name_order_cut():
    # 【双口径注记】旧值 p1==p2==60.0（G2/R3 行为后果：pessimistic_fill
    # 名字序恒最后 → 恒被裁，只改 pessimistic 分数聚合纹丝不动）/
    # 新值 p1=55.0、p2=62.5 且 p1!=p2（值序：p1 排序 [10,50,60,70] →
    # kept=[50,60]；p2 排序 [50,60,65,70] → kept=[60,65]——悲观分数
    # 恢复效力）/ 原因=R3 修复。
    p1 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 10.0}
    p2 = {WB: 50.0, WS: 60.0, PE: 70.0, PF: 65.0}
    assert aggregate_scores(p1) == 55.0
    assert aggregate_scores(p2) == 62.5
    assert aggregate_scores(p1) != aggregate_scores(p2)
    # 对照（值不变）：worst_case 聚合感知 pessimistic 变动。
    assert aggregate_scores(p1, strategy="worst_case") == 10.0
    assert aggregate_scores(p2, strategy="worst_case") == 50.0''',
       old_value="p1==p2==60.0（名字序恒裁 pessimistic_fill）",
       new_value="p1=55.0、p2=62.5 且 p1!=p2（悲观恢复效力）",
       reason="R3"),
    _e("test_planner_select_characterization.py", "value",
       "test_robust_select_ranking_and_aggregates_frozen",
       '''def test_robust_select_ranking_and_aggregates_frozen():
    j_matrix = {
        "anchor_conservative": dict(CASE_A),
        # 名字序 [ws:30, wb:20, pe:25, pf:22] → kept=[20,25] → 22.5。
        "plan_expand_herd": {WB: 20.0, WS: 30.0, PE: 25.0, PF: 22.0},
    }
    result = robust_select(j_matrix)
    assert result["best"] == "anchor_conservative"
    assert result["aggregates"] == {"anchor_conservative": 35.0,
                                    "plan_expand_herd": 22.5}
    assert result["ranking"] == [("anchor_conservative", 35.0),
                                 ("plan_expand_herd", 22.5)]
    assert result["strategy"] == "trimmed_mean"
    assert result["tie_break"] is None''',
       '''def test_robust_select_ranking_and_aggregates_frozen():
    j_matrix = {
        "anchor_conservative": dict(CASE_A),
        # 【双口径注记】plan_expand_herd 旧值 22.5（名字序 [ws:30, wb:20,
        # pe:25, pf:22] → kept=[20,25]）/ 新值 23.5（值序 [20,22,25,30] →
        # kept=[22,25]）。
        "plan_expand_herd": {WB: 20.0, WS: 30.0, PE: 25.0, PF: 22.0},
    }
    result = robust_selection(j_matrix)
    # 【双口径注记】anchor_conservative 旧值 35.0 / 新值 65.0（值序裁切，
    # CASE_A 同源）/ 原因=R3 修复；排序与 best 结论不变（65.0 > 23.5）。
    assert result["best"] == "anchor_conservative"
    assert result["aggregates"] == {"anchor_conservative": 65.0,
                                    "plan_expand_herd": 23.5}
    assert result["ranking"] == [("anchor_conservative", 65.0),
                                 ("plan_expand_herd", 23.5)]
    assert result["strategy"] == "trimmed_mean"
    assert result["tie_break"] is None''',
       old_value="aggregates {35.0, 22.5}",
       new_value="aggregates {65.0, 23.5}",
       reason="R3"),
    _e("test_planner_select_characterization.py", "value",
       "test_robust_select_tie_breaks_on_lexicographic_key",
       '''def test_robust_select_tie_breaks_on_lexicographic_key():
    j_matrix = {"b_plan": dict(CASE_A), "a_plan": dict(CASE_A)}
    result = robust_select(j_matrix)
    assert result["best"] == "a_plan"
    assert result["tie_break"] is not None
    assert "2 个计划聚合值并列 35.0" in result["tie_break"]
    assert "'a_plan'" in result["tie_break"]''',
       '''def test_robust_select_tie_breaks_on_lexicographic_key():
    j_matrix = {"b_plan": dict(CASE_A), "a_plan": dict(CASE_A)}
    result = robust_selection(j_matrix)
    assert result["best"] == "a_plan"
    assert result["tie_break"] is not None
    # 【双口径注记】并列聚合值旧值 35.0 / 新值 65.0（值序裁切）/
    # 原因=R3 修复；决胜语义不变（key 字典序取 'a_plan'）。
    assert "2 个计划聚合值并列 65.0" in result["tie_break"]
    assert "'a_plan'" in result["tie_break"]''',
       old_value="并列 35.0（名字序）",
       new_value="并列 65.0（值序）",
       reason="R3"),
    _e("test_planner_select_characterization.py", "value",
       "test_robust_select_identity_tiebreak_k1_gate",
       '''def test_robust_select_identity_tiebreak_k1_gate():
    # K1 近平守成：challenger 聚合 1001.5（名字序 kept=[wb:999, pe:1004]）
    # 对 identity_hold=1000.0 边际 1.5 < tau*1000=5.0 → 恒选守成点。
    j_matrix = {
        "identity_hold": {WB: 1000.0, WS: 1000.0, PE: 1000.0, PF: 1000.0},
        "challenger": {WB: 999.0, WS: 1002.0, PE: 1004.0, PF: 1005.0},
    }
    result = robust_select(j_matrix, identity_key="identity_hold")
    assert result["aggregates"] == {"challenger": 1001.5,
                                    "identity_hold": 1000.0}
    assert result["best"] == "identity_hold"
    assert result["tie_break"] is not None
    assert "K1 近平守成" in result["tie_break"]
    # ranking 保持原序（守成裁决不改 ranking）。
    assert result["ranking"][0] == ("challenger", 1001.5)''',
       '''def test_robust_select_identity_tiebreak_k1_gate():
    # K1 近平守成：【双口径注记】challenger 聚合旧值 1001.5（名字序
    # kept=[999,1004]）/ 新值 1003.0（值序排序 [999,1002,1004,1005] →
    # kept=[1002,1004]）；对 identity_hold=1000.0 边际旧 1.5 / 新 3.0，
    # 均 < tau*1000=5.0 → 恒选守成点（K1 冻结语义不变）/ 原因=R3 修复。
    j_matrix = {
        "identity_hold": {WB: 1000.0, WS: 1000.0, PE: 1000.0, PF: 1000.0},
        "challenger": {WB: 999.0, WS: 1002.0, PE: 1004.0, PF: 1005.0},
    }
    result = robust_selection(j_matrix, identity_key="identity_hold")
    assert result["aggregates"] == {"challenger": 1003.0,
                                    "identity_hold": 1000.0}
    assert result["best"] == "identity_hold"
    assert result["tie_break"] is not None
    assert "K1 近平守成" in result["tie_break"]
    # ranking 保持原序（守成裁决不改 ranking）。
    assert result["ranking"][0] == ("challenger", 1003.0)''',
       old_value="challenger 聚合 1001.5（边际 1.5）",
       new_value="challenger 聚合 1003.0（边际 3.0）",
       reason="R3"),
    _e("test_planner_select_characterization.py", "redirect",
       "test_robust_select_input_order_independent",
       '''def test_robust_select_input_order_independent():
    # 输入 dict 顺序不影响结果（全排序显式键）。
    items = [("z_plan", dict(CASE_A)), ("a_plan", {WB: 20.0, WS: 30.0,
                                                   PE: 25.0, PF: 22.0})]
    r1 = robust_select(dict(items))
    r2 = robust_select(dict(reversed(items)))
    assert r1 == r2''',
       '''def test_robust_select_input_order_independent():
    # 输入 dict 顺序不影响结果（全排序显式键；无值变化，仅调用名随迁）。
    items = [("z_plan", dict(CASE_A)), ("a_plan", {WB: 20.0, WS: 30.0,
                                                   PE: 25.0, PF: 22.0})]
    r1 = robust_selection(dict(items))
    r2 = robust_selection(dict(reversed(items)))
    assert r1 == r2'''),
]

# ---------------------------------------------------------------------------
# 影响清单（编辑授权面）：value/xfail_convert 编辑逐条对应；调用方（含
# migrate_snapshot_suite 与镜像测试）以本常量为标准入参。
# ---------------------------------------------------------------------------
DEFAULT_IMPACT_LIST = [
    {"file": e["file"], "locator": e["locator"], "reason": e["reason"]}
    for e in _EDITS
    if e["kind"] in ("value", "xfail_convert")
]


# 反向锚：受影响旧断言字面量不得残留（刷新后应为值序/seated 新值）
_RETIRED_ANCHORS = {
    "test_planner_select_characterization.py": (
        "assert aggregate_scores(CASE_A) == 35.0",
        'assert "2 个计划聚合值并列 35.0" in result["tie_break"]',
    ),
    "test_counterexample_r3.py": (
        "assert aggregate_scores(CASE_A) == 35.0",
        "assert aggregate_scores(CASE_B) == 60.0",
        "== aggregate_scores(hi) == 60.0",
    ),
    "test_counterexample_r2.py": (
        "import planner_offline_bench as bench",
        "@pytest.mark.xfail",
    ),
}


def _anchor_violations(texts: dict) -> list:
    """对 {文件名: 文本} 映射做锚校验（在场锚 + 退役锚 + 字面路径禁令）。"""
    violations = []
    for name, anchors in PROTECTED_ANCHORS.items():
        text = texts.get(name)
        if text is None:
            violations.append(f"{name}: 文件缺失")
            continue
        for anchor in anchors:
            if anchor not in text:
                violations.append(f"{name}: 受保护冻结字面量缺失: {anchor!r}")
    for name, anchors in _RETIRED_ANCHORS.items():
        text = texts.get(name)
        if text is None:
            continue
        for anchor in anchors:
            if anchor in text:
                violations.append(f"{name}: 应替换的旧字面量仍在场: {anchor!r}")
    for name in WHITELIST:
        text = texts.get(name)
        if text is None:
            continue
        for banned in ("workspace/", "autoC"):
            if banned in text:
                violations.append(f"{name}: 引入字面路径片段 {banned!r}")
    return violations


def check_protected_anchors(target_dir) -> list:
    """校验受保护冻结字面量仍在场（对磁盘上的套件目录；空=通过）。

    覆盖三层：白名单三件内跨口径不变的在场锚（输入构造/常量/真值与负
    锚）；"旧名字序断言字面量必须已被替换"的退役锚；字面战役路径禁令
    （R20；环境名 "kaggriculture" 是 kaggle 环境 id，不属路径，不算违例）。
    """
    base = Path(target_dir)
    texts = {}
    for name in WHITELIST:
        path = base / name
        if path.is_file():
            texts[name] = path.read_text(encoding="utf-8")
    return _anchor_violations(texts)


def refresh_frozen_values(impact_list, target_dir) -> tuple:
    """把迁移副本中受 R2/R3 修复影响的冻结值刷新为新口径（就地写回）。

    Args:
        impact_list: 影响清单，逐条 {"file", "locator", "reason"}——value/
            xfail_convert 类编辑的逐条授权面（DEFAULT_IMPACT_LIST 即标准值）。
        target_dir: 套件副本目录（九文件齐备；源 snapshot_tests/ 只读，
            本函数不触碰源件）。

    Returns:
        (changed_files, annotations)：changed_files=实际改写的白名单文件
        名列表（排序）；annotations=逐处变更注记 dict 列表，键
        {kind, file, locator, old_value, new_value, reason}（kind∈
        {value, xfail_convert}；redirect/note 类结构变更不入注记、由文件
        内【迁移记录】/【R2·R3 重定向】注自述）。

    Raises:
        ValueError: 影响清单含白名单外文件 / 清单项无对应编辑 / 编辑未被
            清单授权（影响清单外冻结值变动）/ 锚文本非唯一命中 / 副本缺
            件。一律先全量校验后落盘（fail-closed，失败时零写入）。
    """
    base = Path(target_dir)

    # ---- ① 影响清单静态校验（零写入）----
    if not impact_list:
        raise ValueError("影响清单为空：refresh_frozen_values 需逐条授权"
                         "（标准值=DEFAULT_IMPACT_LIST）")
    authorized = set()
    for entry in impact_list:
        if not isinstance(entry, dict) or \
                not {"file", "locator", "reason"} <= set(entry):
            raise ValueError(f"影响清单项形状非法（需 file/locator/reason）:"
                             f" {entry!r}")
        if entry["file"] not in WHITELIST:
            raise ValueError(
                f"影响清单越界：{entry['file']} 不在白名单 {WHITELIST} 内"
                f"（agent 整局旗关冻结/评级/契约/台账零改动）")
        authorized.add((entry["file"], entry["locator"]))
    annotated_edits = [e for e in _EDITS
                       if e["kind"] in ("value", "xfail_convert")]
    for entry in impact_list:
        key = (entry["file"], entry["locator"])
        if not any((e["file"], e["locator"]) == key for e in annotated_edits):
            raise ValueError(
                f"影响清单项无对应修复点: {entry['file']}::{entry['locator']}"
                f"（清单必须与已知 R2/R3 影响面一一对应，不得空授权）")
    for edit in annotated_edits:
        if (edit["file"], edit["locator"]) not in authorized:
            raise ValueError(
                f"影响清单外冻结值变动被拒: "
                f"{edit['file']}::{edit['locator']}（编辑表中存在该修复点"
                f"但清单未授权；标准值=DEFAULT_IMPACT_LIST）")

    # ---- ② 读入白名单副本并逐条锚定替换（仍在内存，零写入）----
    contents = {}
    for name in WHITELIST:
        path = base / name
        if not path.is_file():
            raise ValueError(f"迁移副本缺件: {path}（先复制九文件再刷新）")
        contents[name] = path.read_text(encoding="utf-8")
    for edit in _EDITS:
        text = contents[edit["file"]]
        hits = text.count(edit["old"])
        if hits != 1:
            raise ValueError(
                f"锚文本命中 {hits} 次（需恰 1 次）: {edit['file']} @"
                f"{edit['locator']}——副本不是源套件原貌或已被刷新过"
                f"（幂等重入请自源重新复制）")
        contents[edit["file"]] = text.replace(edit["old"], edit["new"], 1)

    # ---- ③ 受保护字面量复核（对内存中的刷新后文本；零写入阶段内完成）----
    violations = _anchor_violations(contents)
    if violations:
        raise ValueError("受保护冻结字面量校验失败（零写入回退）: "
                         + "; ".join(violations))

    # ---- ④ 落盘（至此才产生副作用）----
    for name in WHITELIST:
        (base / name).write_text(contents[name], encoding="utf-8",
                                 newline="")

    changed = sorted({e["file"] for e in _EDITS})
    annotations = [
        {"kind": e["kind"], "file": e["file"], "locator": e["locator"],
         "old_value": e["old_value"], "new_value": e["new_value"],
         "reason": e["reason"]}
        for e in annotated_edits
    ]
    return changed, annotations
