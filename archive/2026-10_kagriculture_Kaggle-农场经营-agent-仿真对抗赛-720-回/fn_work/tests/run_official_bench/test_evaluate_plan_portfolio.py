"""evaluate_plan_portfolio 真实行为测试（B3，占位改真实）。

小合成计划集（2 计划×2 对手）+ 合成回放（生成方式复刻
test_rollout_with_replay_opponent.py 的快照反例口径——引擎固定种子
20260921，seat0=恒 PASS→3000.0、seat1=每 5 回合买 1 包 WHEAT→1570.0；
不 import snapshot_tests / 旧树 scripts/）覆盖：
① 逐计划逐对手 seated rollout：记录型假 callable/假 deps 断言——每
   (计划,ω) 恰一次 rollout（build 计数=注入点）、我方动作落 me_seat
   席（obs 席位 + pair 槽位双侧）、注入点原样透传；
② 聚合走 robust_selection：委托 spy（恰一次、J 矩阵/参数原位）+ 值序
   语义（反键字典序：分高者胜）；
③ 枚举帽截断：超帽截断保持枚举序 + identity 守成点豁免恒在；
④ j_matrix 键完整：计划键 × ω 名全覆盖。
另：真引擎端到端（me_seat=1 分值=我席终局，R2 修复口径）与空计划空间
经下层 fail-closed。
"""

import pytest

from kaggle_environments import make

import run_official_bench.evaluate_plan_portfolio as epp
from run_official_bench.evaluate_plan_portfolio import (
    MAX_PLAN_CANDIDATES,
    evaluate_plan_portfolio,
)

SEED = 20260921
EPISODE_STEPS = 720
FROZEN_REPLAY_REWARDS = [3000.0, 1570.0]


def _pass_bot(obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _seed_buyer_bot():
    """状态无关脚本：每第 5 个决策买 1 包 WHEAT 种子（与回放生成同源）。"""
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
    """经引擎生成合成回放（module 级共享；生成方式复刻快照反例测试）。"""
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


# ---------------------------------------------------------------------------
# 记录型假件（假 deps / 假计划执行器）——seated 通道契约的最小实现
# ---------------------------------------------------------------------------
class _FakeEnvConfig:
    episodeSteps = 6                       # 假引擎每 rollout 只推 6 步


class _FakeEnv:
    def __init__(self):
        self.configuration = _FakeEnvConfig()
        self.done = False


class _FakeSeat:
    def __init__(self, seat):
        self.observation = type("Obs", (), {"seat_tag": seat})()


class _FakeState:
    def __init__(self):
        self.env = _FakeEnv()
        self.seats = [_FakeSeat(0), _FakeSeat(1)]
        self.totals = [0.0, 0.0]


def _fake_deps(tape_len=720):
    """记录型假依赖组：build 记注入步、step 记逐位动作对（并按
    step_value 累计各席"终局资金"——假引擎语义，分值可控）、
    transition_actions 产可识别的双席动作流磁带。"""
    calls = {"build": [], "steps": []}
    tape = [[f"opp_t{i}_s0", f"opp_t{i}_s1"] for i in range(tape_len)]

    def build(replay, step_index):
        calls["build"].append(step_index)
        return _FakeState()

    def transition_actions(replay):
        return tape

    def step(state, pair):
        calls["steps"].append(list(pair))
        for seat, action in enumerate(pair):
            if isinstance(action, dict):
                state.totals[seat] += action.get("step_value", 0.0)

    def final(state):
        return list(state.totals)

    deps = {"build": build, "transition_actions": transition_actions,
            "step": step, "final": final}
    return deps, calls, tape


def _recording_agent(marker, step_value, log):
    """记录型计划执行器工厂（契约第二元=0 参工厂，逐 rollout 全新装载）：
    工厂每次产新 agent；agent 记所见 obs 席位，返回带可识别标记的动作
    （step_value 供假引擎累计"终局资金"）。"""
    def factory():
        def agent(obs):
            log.append({"seat_tag": obs.seat_tag, "marker": marker})
            return {"farmer": ["PASS"], "hands": [], "market": [],
                    "marker": marker, "step_value": step_value}
        return agent
    return factory


# ---------------------------------------------------------------------------
# ① 逐计划逐对手 seated rollout（me_seat 透传）+ ④ j_matrix 键完整
# ---------------------------------------------------------------------------
def test_per_plan_per_opponent_seated_rollout_me_seat_passthrough(
        synthetic_replay):
    """2 计划×2 裸名 ω → 恰 4 次 seated rollout（build 计数=注入点 100，
    注入点原样透传）；我方 callable 只见 me_seat=1 的 obs、动作只落
    pair[1]（我席槽），对席槽=回放动作流 [100..] 的 s0 位；J 矩阵键=
    计划键 × ω 名全覆盖。"""
    deps, calls, _tape = _fake_deps()
    my_log = []
    plans = [("plan_a", _recording_agent("A", 10.0, my_log)),
             ("plan_z", _recording_agent("Z", 3.0, my_log))]
    omega = ["omega_replay_1", "omega_replay_2"]
    result = evaluate_plan_portfolio(
        plans, omega, 100, synthetic_replay, 1, deps=deps)
    assert calls["build"] == [100, 100, 100, 100]      # 4 rollout，注入点透传
    assert {e["seat_tag"] for e in my_log} == {1}      # 我方 callable 只见我席
    assert len(my_log) == 4 * 6                        # 每 rollout 6 步
    for pair in calls["steps"]:
        assert pair[0].startswith("opp_t") and pair[0].endswith("_s0")
        assert pair[1]["marker"] in ("A", "Z")         # 我方动作在 me_seat=1 槽
    assert set(result["j_matrix"]) == {"plan_a", "plan_z"}
    for scores in result["j_matrix"].values():
        assert set(scores) == set(omega)
    assert result["n_plans"] == 2 and result["n_omega"] == 2
    assert result["j_matrix"]["plan_a"]["omega_replay_1"] == \
        pytest.approx(60.0)                            # 6 步 × step_value 10
    assert result["aggregates"]["plan_z"] == pytest.approx(18.0)


# ---------------------------------------------------------------------------
# ② 聚合走 robust_selection（值序语义）
# ---------------------------------------------------------------------------
def test_aggregation_delegates_to_robust_selection_value_order(
        synthetic_replay, monkeypatch):
    """委托 spy：robust_selection 恰被调一次、收到完整 J 矩阵与聚合参数；
    值序语义：plan_z 聚合 60 > plan_a 18 → best=plan_z（反键字典序——
    "plan_a" 字典序更小但分低不胜）；me_seat=0 补充透传（我方动作落
    pair[0]、对席读回放流 s1 位）。"""
    deps, calls, _tape = _fake_deps()
    spy = []
    real = epp.robust_selection

    def spying(j_matrix, **kwargs):
        spy.append((j_matrix, kwargs))
        return real(j_matrix, **kwargs)

    monkeypatch.setattr(epp, "robust_selection", spying)
    plans = [("plan_a", _recording_agent("A", 3.0, [])),
             ("plan_z", _recording_agent("Z", 10.0, []))]
    result = evaluate_plan_portfolio(
        plans, ["omega_1"], 0, synthetic_replay, 0, deps=deps,
        strategy="trimmed_mean")
    assert len(spy) == 1
    j_matrix, kwargs = spy[0]
    assert j_matrix == result["j_matrix"]
    assert kwargs["strategy"] == "trimmed_mean"
    assert result["best"] == "plan_z"
    assert [key for key, _ in result["ranking"]] == ["plan_z", "plan_a"]
    assert result["aggregates"]["plan_a"] == pytest.approx(18.0)
    assert result["aggregates"]["plan_z"] == pytest.approx(60.0)
    for pair in calls["steps"]:                        # me_seat=0 槽位透传
        assert pair[0]["marker"] in ("A", "Z")
        assert pair[1].startswith("opp_t") and pair[1].endswith("_s1")


# ---------------------------------------------------------------------------
# ③ 枚举帽截断（+ identity 守成点豁免）
# ---------------------------------------------------------------------------
def test_plan_cap_truncation_and_identity_exemption(synthetic_replay):
    deps, _calls, _tape = _fake_deps()
    plans = [("p1", _recording_agent("P1", 1.0, [])),
             ("p2", _recording_agent("P2", 1.0, [])),
             ("p3_identity", _recording_agent("P3", 1.0, []))]
    # 超帽截断：帽 2 → 只评 2 个（保持枚举序取前帽）
    result = evaluate_plan_portfolio(
        plans, ["omega"], 0, synthetic_replay, 1, deps=deps, plan_cap=2)
    assert result["n_plans"] == 2 and result["capped"] is True
    assert set(result["j_matrix"]) <= {"p1", "p2", "p3_identity"}
    # identity 豁免：守成点排在帽外也恒在（换入末位，总数仍=帽）
    result_id = evaluate_plan_portfolio(
        plans, ["omega"], 0, synthetic_replay, 1, deps=deps, plan_cap=2,
        identity_key="p3_identity")
    assert "p3_identity" in result_id["j_matrix"]
    assert result_id["n_plans"] == 2
    # 帽内不截断；缺省帽=120（旧树 plans.py:57 MAX_PLAN_CANDIDATES 照旧）
    result_full = evaluate_plan_portfolio(
        plans, ["omega"], 0, synthetic_replay, 1, deps=deps)
    assert result_full["capped"] is False and result_full["n_plans"] == 3
    assert MAX_PLAN_CANDIDATES == 120


# ---------------------------------------------------------------------------
# Ω 模型驱动对手席（(名, callable) 形态经 deps["step"] 包装就位）
# ---------------------------------------------------------------------------
def test_model_opponent_drives_opposite_seat_via_deps(synthetic_replay):
    deps, calls, _tape = _fake_deps()
    my_log, opp_log = [], []
    plans = [("plan_m", _recording_agent("M", 1.0, my_log))]
    omega = [("aggressive", _recording_agent("OPP", 0.0, opp_log))]
    evaluate_plan_portfolio(
        plans, omega, 0, synthetic_replay, 1, deps=deps)
    assert {e["seat_tag"] for e in opp_log} == {0}     # ω 只见对席 obs
    assert {e["seat_tag"] for e in my_log} == {1}      # 我方只见 me_seat 席
    for pair in calls["steps"]:
        assert pair[0]["marker"] == "OPP"              # 对手槽被 ω 覆写
        assert pair[1]["marker"] == "M"                # 我方槽仍是我方输出


# ---------------------------------------------------------------------------
# 真引擎端到端：分值=我席终局资金（R2 修复口径）
# ---------------------------------------------------------------------------
def test_real_engine_end_to_end_seated_scores(synthetic_replay):
    """真 twin 通道（deps=None 默认组，指纹链照走）：me_seat=1 注入 0，
    buyer=逐 rollout 新建的 seat1 人格→两 ω 同为 1570.0（我席真值；旧恒
    seat0 错位通道会记成对席 3000.0 伪影；共享状态执行器会串态成
    1560.0——工厂逐 rollout 重建即防此）、passer=恒不买→3000.0；两裸名
    ω（回放对手）键完整；值序 best=passer（反键字典序）。"""
    plans = [("buyer", _seed_buyer_bot), ("passer", lambda: _pass_bot)]
    result = evaluate_plan_portfolio(
        plans, ["omega_a", "omega_b"], 0, synthetic_replay, 1)
    assert result["j_matrix"]["buyer"] == \
        {"omega_a": 1570.0, "omega_b": 1570.0}
    assert result["j_matrix"]["passer"] == \
        {"omega_a": 3000.0, "omega_b": 3000.0}
    assert result["best"] == "passer"
    assert result["n_plans"] == 2 and result["n_omega"] == 2


# ---------------------------------------------------------------------------
# 空计划空间：经下层 fail-closed（错误: 无自设面）
# ---------------------------------------------------------------------------
def test_empty_plan_space_fails_closed_via_delegation(synthetic_replay):
    deps, _calls, _tape = _fake_deps()
    with pytest.raises(ValueError, match="空 J 矩阵"):
        evaluate_plan_portfolio(
            [], ["omega"], 0, synthetic_replay, 1, deps=deps)
