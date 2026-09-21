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
    import planner_offline_bench as bench
    return bench.make_twin_deps()


def _run_bench(deps, replay, me_seat, agent_factory=_seed_buyer_bot):
    import planner_offline_bench as bench
    from kaggle_simulations.agent.planner import twin
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    return bench.rollout_with_replay_opponent(
        deps, state, me_seat, agent_factory(), acts, 0)


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
    """对照断言：bench 通道 me_seat=1 的当前（错位）输出 = 双席资金互换。"""
    (final, taken) = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_BENCH_MISSEATED_FINAL
    assert final != FROZEN_REPLAY_REWARDS
    assert taken == EPISODE_STEPS - 1


def test_bench_me_seat0_matches_seated(synthetic_replay, twin_deps):
    """me_seat=0 时 bench 与 seated 逐字节同（错位仅在 me_seat=1 显形）。

    用 seat0 的回放人格（恒 PASS bot）驱动我方席：两通道都把动作注入
    seat0、对手席由回放 seat1 磁带驱动 → 双双精确复现回放真值。"""
    bench_final, _ = _run_bench(twin_deps, synthetic_replay, 0,
                                agent_factory=lambda: _pass_bot)
    seated_final, _ = _run_seated(twin_deps, synthetic_replay, 0,
                                  agent_factory=lambda: _pass_bot)
    assert bench_final == seated_final == FROZEN_REPLAY_REWARDS


@pytest.mark.xfail(
    strict=True,
    reason="R2 快照反例：旧 bench.rollout_with_replay_opponent 恒 mine→seat0"
           "（席位错位），新结构上提 seated 通道后此测试应 XPASS")
def test_bench_rollout_injects_into_actual_seat(synthetic_replay, twin_deps):
    """R2 验收面：bench 通道对 me_seat=1 也应把动作注入实际席位
    （即与回放真值一致）。旧代码输出互换伪影 → 此断言失败。"""
    (final, _taken) = _run_bench(twin_deps, synthetic_replay, 1)
    assert final == FROZEN_REPLAY_REWARDS
