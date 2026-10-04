# test_counterexample_r2.py —— 席位错位反例（R2 快照反例，G1）
# ===========================================================================
# 缺陷（requirements.md R2 / 行为清单 G1）：
#   scripts/planner_offline_bench.py:319 rollout_with_replay_opponent 恒把
#   我方动作注入 seat0（deps["step"](state, [mine, theirs])），me_seat=1 的
#   局数字全为伪影。正确实现仅存 scripts/v143_sellrace_gates.py:91-116
#   rollout_with_replay_opponent_seated（pair[me]=mine 按席位放置）。
#
# 构造方式（无需降级——两大实现调用面小成本即可构造，未走差分子逻辑
# 降级路径；完整复跑条件与本测试一致，不依赖 gitignored 官方语料）：
#   1. 用 kgenv 的引擎通道（kaggle_environments.make，vendored 1.32.7）
#      以固定种子 20260921 生成一局**合成回放**：seat0=恒 PASS 脚本
#      （终局 3000.0）、seat1=每 5 回合买 1 包 WHEAT 种子的状态无关脚本
#      （终局 1570.0）。回放 dict 含 configuration/info.seed/steps/rewards，
#      twin.build_state_from_replay 可直接重建。
#   2. me_seat=1、agent_fn=与生成回放同一脚本的全新实例、对手=回放真实
#      动作流，分别经 bench 与 v143 seated 两通道 rollout 至终局。
#
# 预期（旧代码实测冻结）：
#   * seated 通道精确复现回放真值 [3000.0, 1570.0]（正确语义：
#     我方动作注入我方实际席位 ⇒ 整局逐位重演）；
#   * bench 通道输出 [1570.0, 3000.0]——双席资金恰好互换（我方脚本动作
#     落进对手农场、对手磁带的 PASS 落进我方席位），席位错位伪影。
#
# xfail(strict) 断言：bench 通道 == 回放真值（"我方动作注入到我方实际
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
# ===========================================================================

import pytest

from kaggle_environments import make

SEED = 20260921
EPISODE_STEPS = 720
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

# 合成回放终局真值（脚本 + 种子决定，2026-09-21 实测冻结）。
FROZEN_REPLAY_REWARDS = [3000.0, 1570.0]
# bench 通道 me_seat=1 的错位输出（双席互换伪影，实测冻结）。
FROZEN_BENCH_MISSEATED_FINAL = [1570.0, 3000.0]


def _pass_bot(obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _seed_buyer_bot():
    """状态无关脚本：每第 5 个决策买 1 包 WHEAT 种子（引擎合法动作，
    interpreter _parse_order/_commit_unit 语义：BUY_SEED 扣款进 seeds）。"""
    counter = [0]

    def bot(obs):
        counter[0] += 1
        if counter[0] % 5 == 0:
            return {"farmer": ["PASS"], "hands": [],
                    "market": [["BUY_SEED", "WHEAT", 1]]}
        return {"farmer": ["PASS"], "hands": [], "market": []}

    return bot


def _to_plain(obj):
    """kaggle Struct/list 树 → 纯 dict/list（json 安全）。"""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {key: _to_plain(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(value) for value in obj]
    return obj


@pytest.fixture(scope="module")
def synthetic_replay():
    """经引擎生成合成回放（module 级共享，~2s）。"""
    env = make("kaggriculture",
               configuration={"episodeSteps": EPISODE_STEPS, "seed": SEED,
                              "actTimeout": 60},
               debug=True)
    env.run([_pass_bot, _seed_buyer_bot()])
    final = env.steps[-1]
    assert [s["status"] for s in final] == ["DONE", "DONE"]
    replay = {
        "configuration": _to_plain(env.configuration),
        "info": {"seed": SEED},
        "steps": _to_plain(env.steps),
        "rewards": [float(s["reward"]) for s in final],
    }
    assert replay["rewards"] == FROZEN_REPLAY_REWARDS
    return replay


@pytest.fixture(scope="module")
def twin_deps():
    # 【R2 重定向·迁移】依赖组改经 fn_work make_twin_deps（原
    # planner_offline_bench.make_twin_deps；键契约含 v143 参照通道消费的
    # step/final，引擎装载指纹链 fail-closed 保留）。
    from run_official_bench.rollout_with_replay_opponent import make_twin_deps
    return make_twin_deps()


def _run_bench(deps, replay, me_seat, agent_factory=_seed_buyer_bot):
    # 【R2 重定向·迁移】bench 通道 → fn_work/src/run_official_bench 的
    # seated 实现（原 planner_offline_bench.rollout_with_replay_opponent）。
    # 调用形态随新签名：回放/注入点由通道内重建（幂等；deps 参数保留作
    # 调用面兼容），返回双席终局资金（序=seat0,seat1，无 taken 返回）。
    from run_official_bench.rollout_with_replay_opponent import (
        rollout_with_replay_opponent)
    return rollout_with_replay_opponent(replay, 0, agent_factory(), me_seat)


def _run_seated(deps, replay, me_seat, agent_factory=_seed_buyer_bot):
    import v143_sellrace_gates as v143
    from kaggle_simulations.agent.planner import twin
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    return v143.rollout_with_replay_opponent_seated(
        deps, state, me_seat, agent_factory(), acts, 0)


def test_twin_reproduces_synthetic_replay(synthetic_replay, twin_deps):
    """孪生 sanity：双席全按回放动作流重演 == 回放真值（差分前提）。"""
    from kaggle_simulations.agent.planner import twin
    state = twin.build_state_from_replay(synthetic_replay, 0)
    acts = twin.replay_transition_actions(synthetic_replay)
    state = twin.run_to_end(state, acts)
    assert twin.final_money(state) == FROZEN_REPLAY_REWARDS


def test_seated_rollout_injects_into_actual_seat(synthetic_replay, twin_deps):
    """正确语义（v143:91-116 参照实现）：me_seat=1 的 rollout 精确复现
    回放真值——我方动作注入我方席位、对手由回放磁带驱动。普通断言保绿。"""
    (final, taken) = _run_seated(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS
    assert taken == EPISODE_STEPS - 1


def test_bench_current_misseated_output_frozen(synthetic_replay, twin_deps):
    """对照断言（迁移后 seated 口径）。

    【双口径注记】旧值 [1570.0, 3000.0]（错位口径：旧 bench 恒 seat0
    注入 → 双席资金互换伪影）/ 新值 [3000.0, 1570.0]（seated 口径，
    =回放真值）/ 原因=R2 修复（fn_work 通道上提 v143 seated 语义）。
    FROZEN_BENCH_MISSEATED_FINAL 常量留档为负锚——修复后不得再出此值。
    """
    final = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS
    assert final != FROZEN_BENCH_MISSEATED_FINAL


def test_bench_me_seat0_matches_seated(synthetic_replay, twin_deps):
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
    assert bench_final == seated_final == FROZEN_REPLAY_REWARDS


def test_bench_rollout_injects_into_actual_seat(synthetic_replay, twin_deps):
    """R2 验收面（xfail 转常规·迁移）：bench 通道（fn_work seated 实现）
    对 me_seat=1 也把动作注入实际席位（即与回放真值一致）。

    【双口径注记】旧=strict xfail（旧 bench 恒 seat0 注入 → 互换伪影
    [1570.0, 3000.0]，套件保绿）/ 新=常规通过（原因=R2 修复）。"""
    final = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS
