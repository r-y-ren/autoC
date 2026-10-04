"""run_official_bench 真实行为测试（B3 顶层，占位改真实）。

合成注入集（1 局×1 注入点×小计划空间；合成回放生成方式复刻
test_rollout_with_replay_opponent.py 的快照反例口径——引擎固定种子
20260921，seat0=恒 PASS→3000.0、seat1=每 5 回合买 1 包 WHEAT→1570.0；
不 import snapshot_tests / 旧树 scripts/）覆盖：
① 主口径裁决输出（DTSP vs 反应式，结构键完整）——DTSP=passer 注入
   seat1 → 3000.0 vs 反应式=同源 seed buyer → 1570.0，Δ=+1430 判不劣；
② 参考口径 offset 分解字段在场且代数恒等（corrected = Δhistory −
   offset，offset = mean(reactive) − mean(truth)）；
③ 异常局 fail-closed 记录（坏回放/坏席位 → 该局记异常不中断，好局
   照常评估）。
另：official 门禁数学（fake deps 无引擎快算：过门 exit 0 / 败门 exit 1
——后者兼走 oracle 归因路径）与前置配置 fail-closed、报告 JSON 可落盘。
"""

import json

import pytest

from kaggle_environments import make

from run_official_bench.run_official_bench import (
    attribute_failure,
    run_official_bench,
    select_injection_steps,
)

SEED = 20260921
EPISODE_STEPS = 720
FROZEN_REPLAY_REWARDS = [3000.0, 1570.0]

# 结构键契约（旧 bench_report.json 行/局/汇总键的 seated 迁移面）
TOP_KEYS = {"mode", "me_seat", "generated_at_utc", "wall_seconds",
            "configuration", "criterion_note", "opponent_models",
            "episodes", "abnormal_episodes", "skipped_episodes", "rows",
            "summary"}
ROW_KEYS = {"episode", "step", "day", "me_seat", "truth_me",
            "twin_resim_me", "twin_noise", "reactive_me", "dtsp_me",
            "dtsp_vs_history", "dtsp_vs_reactive", "best_plan", "n_plans",
            "n_omega", "plan_ranking_top3", "tie_break", "opponent_models",
            "oracle_best", "oracle_key", "judge_fail", "twin_noise_flag",
            "opponent_model_gap", "plan_space_gap", "attribution_reason",
            "round", "mirror", "opponent"}
EPISODE_KEYS = {"episode", "round", "me_seat", "opponent", "mirror",
                "n_injections", "mean_truth_me", "mean_reactive_me",
                "mean_dtsp_me", "dtsp_vs_history", "dtsp_vs_reactive",
                "median_dtsp_vs_reactive", "primary_pass",
                "reactive_vs_history_offset", "dtsp_vs_history_corrected",
                "reference_pass", "gate_pass", "fail_attribution"}
SUMMARY_KEYS = {"episodes_evaluated", "episodes_passed",
                "episodes_passed_reference", "episodes_abnormal",
                "injections_evaluated", "gates_all_pass", "enough_episodes",
                "pooled_mean_dtsp_vs_reactive", "mean_dtsp_vs_history",
                "mean_dtsp_vs_reactive", "attribution_totals", "exit_code"}


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


@pytest.fixture(scope="module")
def bench_run(synthetic_replay, tmp_path_factory):
    """合成基准跑（module 级共享）：1 局（me_seat=1 台面默认）×1 注入点
    （day 0）×1 计划（passer）×1 ω（回放真实对手）；反应式臂=seat1 同源
    seed buyer。真 twin 通道（deps=None 默认组，指纹链照走）。"""
    out_path = tmp_path_factory.mktemp("bench") / "bench_report.json"
    config = {
        "mode": "smoke", "injection_days": [0],
        "episodes": [{"episode": "ep_synth", "replay": synthetic_replay,
                      "round": "synthetic", "opponent": "seed_buyer"}],
        "plan_space": [("passer", lambda: _pass_bot)],
        "reactive_factory": _seed_buyer_bot,
        "out_path": str(out_path),
    }
    report = run_official_bench(config, ["replay_opponent"], 1)
    return report, out_path


# ---------------------------------------------------------------------------
# ① 主口径裁决输出（DTSP vs 反应式，结构键完整）
# ---------------------------------------------------------------------------
def test_primary_criterion_structure_and_values(bench_run):
    """结构键完整（顶层/局/行/汇总四层）+ 主口径数值：反应式=seat1 同源
    persona 复刻真值 1570.0、DTSP=passer 3000.0 → Δ(中位)=+1430 判不劣
    （primary_pass/gate_pass True）；twin 重演核验零偏差。"""
    report, _ = bench_run
    assert set(report) == TOP_KEYS
    assert report["mode"] == "smoke" and report["me_seat"] == 1
    assert len(report["rows"]) == 1 and len(report["episodes"]) == 1
    row = report["rows"][0]
    assert set(row) == ROW_KEYS
    assert row["episode"] == "ep_synth" and row["step"] == 0 \
        and row["day"] == 0 and row["me_seat"] == 1
    assert row["truth_me"] == pytest.approx(1570.0)
    assert row["twin_resim_me"] == pytest.approx(1570.0)   # seated 重演核验
    assert row["twin_noise"] == pytest.approx(0.0, abs=1e-9)
    assert row["reactive_me"] == pytest.approx(1570.0)
    assert row["dtsp_me"] == pytest.approx(3000.0)
    assert row["dtsp_vs_reactive"] == pytest.approx(1430.0)
    assert row["best_plan"] == "passer" and row["n_plans"] == 1
    assert row["judge_fail"] is False
    ep = report["episodes"][0]
    assert set(ep) == EPISODE_KEYS
    assert ep["primary_pass"] is True and ep["gate_pass"] is True
    assert ep["median_dtsp_vs_reactive"] == pytest.approx(1430.0)
    assert report["summary"]["episodes_passed"] == 1
    # smoke 只摇通 harness：门禁值恒 False、退出码 0（旧语义照旧）
    assert report["summary"]["gates_all_pass"] is False
    assert report["summary"]["exit_code"] == 0


def test_report_json_serializable(bench_run):
    """out_path 落盘的报告 JSON 可回读（旧 bench_report.json 输出面）。"""
    report, out_path = bench_run
    assert out_path.is_file()
    reloaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert set(reloaded) == TOP_KEYS
    assert reloaded["summary"]["exit_code"] == report["summary"]["exit_code"]
    assert reloaded["rows"][0]["dtsp_me"] == \
        pytest.approx(report["rows"][0]["dtsp_me"])


# ---------------------------------------------------------------------------
# ② 参考口径 offset 分解字段在场（显式分解 + 代数恒等）
# ---------------------------------------------------------------------------
def test_reference_criterion_offset_decomposition(bench_run):
    """参考口径三字段在场且分解恒等：corrected = mean Δhistory − offset，
    offset = mean(reactive) − mean(truth)。合成局反应式=真值 persona →
    offset=0、corrected=Δhistory=+1430 判不劣。"""
    report, _ = bench_run
    ep = report["episodes"][0]
    for key in ("dtsp_vs_history", "reactive_vs_history_offset",
                "dtsp_vs_history_corrected", "reference_pass"):
        assert key in ep, f"参考口径分解缺字段 {key}"
    assert ep["reactive_vs_history_offset"] == pytest.approx(0.0)
    assert ep["dtsp_vs_history"] == pytest.approx(1430.0)
    assert ep["dtsp_vs_history_corrected"] == \
        pytest.approx(ep["dtsp_vs_history"]
                      - ep["reactive_vs_history_offset"])
    assert ep["reference_pass"] is True
    assert report["summary"]["episodes_passed_reference"] == 1


# ---------------------------------------------------------------------------
# ③ 异常局 fail-closed 记录（坏回放 → 该局记异常不中断）
# ---------------------------------------------------------------------------
def test_abnormal_episode_fail_closed_does_not_interrupt(synthetic_replay):
    """两个异常局（空回放 / 非法 me_seat）各记 abnormal_episodes 留因，
    不中断整批：其后的好局照常评估出双口径裁决行。"""
    config = {
        "mode": "smoke", "injection_days": [0],
        "episodes": [
            {"episode": "ep_bad_replay", "replay": {}},
            {"episode": "ep_bad_seat", "replay": synthetic_replay,
             "me_seat": 7},
            {"episode": "ep_good", "replay": synthetic_replay},
        ],
        "plan_space": [("passer", lambda: _pass_bot)],
        "reactive_factory": _seed_buyer_bot,
    }
    report = run_official_bench(config, ["replay_opponent"], 1)
    abnormal = {a["episode"]: a["error"] for a in report["abnormal_episodes"]}
    assert set(abnormal) == {"ep_bad_replay", "ep_bad_seat"}
    assert "回放缺失" in abnormal["ep_bad_replay"]
    assert "me_seat" in abnormal["ep_bad_seat"]
    # 好局不受异常局影响：照常评估（smoke day0 注入 1 点）
    assert report["summary"]["episodes_evaluated"] == 1
    assert report["summary"]["episodes_abnormal"] == 2
    assert report["summary"]["injections_evaluated"] == 1
    good = next(e for e in report["episodes"] if e["episode"] == "ep_good")
    assert good["primary_pass"] is True and good["reference_pass"] is True
    assert report["summary"]["exit_code"] == 0


# ---------------------------------------------------------------------------
# official 门禁数学（fake deps 快算；败门场景兼走 oracle 归因路径）
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


def _fake_deps(tape_len=100):
    """最小假依赖组（seated 通道契约四键；step_value 累计=假引擎计分）。"""
    tape = [[f"t{i}_s0", f"t{i}_s1"] for i in range(tape_len)]

    def build(replay, step_index):
        return _FakeState()

    def step(state, pair):
        for seat, action in enumerate(pair):
            if isinstance(action, dict):
                state.totals[seat] += action.get("step_value", 0.0)

    return {"build": build,
            "transition_actions": lambda replay: tape,
            "step": step,
            "final": lambda state: list(state.totals)}


def _value_factory(step_value):
    """计划/反应式臂工厂：恒定 step_value 供假引擎累计"终局资金"。"""
    def factory():
        def agent(obs):
            return {"farmer": ["PASS"], "hands": [], "market": [],
                    "step_value": step_value}
        return agent
    return factory


def _official_config(reactive_value):
    fake_replay = {"steps": [None] * 100, "rewards": [0.0, 0.0]}
    return {
        "mode": "official", "injection_days": [0, 1, 2],
        "min_episodes": 1, "primary_gate_wins": 1,
        "episodes": [{"episode": "ep_fake", "replay": fake_replay}],
        "plan_space": [("only", _value_factory(5.0))],
        "reactive_factory": _value_factory(reactive_value),
    }


def test_official_gate_pass_exit_zero():
    """official 过门：3 注入点各 Δ(DTSP−反应式)=6×(5−1)=+24 → 中位不劣、
    pooled mean>0、局数足 → gates_all_pass True / exit_code 0。"""
    report = run_official_bench(_official_config(1.0), ["w"], 1,
                                deps=_fake_deps())
    assert report["summary"]["injections_evaluated"] == 3
    assert report["summary"]["episodes_passed"] == 1
    assert report["summary"]["pooled_mean_dtsp_vs_reactive"] == \
        pytest.approx(24.0)
    assert report["summary"]["gates_all_pass"] is True
    assert report["summary"]["exit_code"] == 0


def test_official_gate_fail_exit_one_with_oracle_attribution():
    """official 败门：反应式 54 > DTSP 30 → Δ=−24 主口径败 → exit_code 1；
    judge_fail 触发 oracle 重演（official 缺省开）——面内唯一候选即选中者
    → 归因落 plan_space_gap（非 opponent_model_gap）。"""
    report = run_official_bench(_official_config(9.0), ["w"], 1,
                                deps=_fake_deps())
    row = report["rows"][0]
    assert row["dtsp_vs_reactive"] == pytest.approx(-24.0)
    assert row["judge_fail"] is True
    assert row["oracle_best"] == pytest.approx(30.0)   # oracle 走 seated 通道
    assert row["opponent_model_gap"] is False
    assert row["plan_space_gap"] is True
    assert report["episodes"][0]["primary_pass"] is False
    assert report["summary"]["gates_all_pass"] is False
    assert report["summary"]["exit_code"] == 1


# ---------------------------------------------------------------------------
# 前置配置 fail-closed（结构性错误整批抛，不留到局级）
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("config, me_seat, match", [
    ({"episodes": [], "plan_space": [], "reactive_factory": _pass_bot},
     1, "计划空间为空"),
    ({"episodes": [], "plan_space": [("p", lambda: _pass_bot)]},
     1, "缺反应式基线工厂"),
    ({"episodes": [], "plan_space": [("p", lambda: _pass_bot)],
      "reactive_factory": _pass_bot}, 2, "me_seat"),
    ({"mode": "official", "injection_days": [10],
      "episodes": [], "plan_space": [("p", lambda: _pass_bot)],
      "reactive_factory": _pass_bot}, 1, ">=3 个注入日"),
])
def test_structural_config_fails_closed(config, me_seat, match):
    with pytest.raises(ValueError, match=match):
        run_official_bench(config, ["w"], me_seat)


def test_empty_omega_fails_closed():
    config = {"episodes": [], "plan_space": [("p", lambda: _pass_bot)],
              "reactive_factory": _pass_bot}
    with pytest.raises(ValueError, match="Ω 为空"):
        run_official_bench(config, [], 1)


# ---------------------------------------------------------------------------
# 迁移纯函数语义抽查（旧码逐句迁移锚点）
# ---------------------------------------------------------------------------
def test_select_injection_steps_clamps_and_dedups():
    """day×24 注入步：钳到 n_steps-2、去重升序（720 步/d 3,10,20 → 72,240,480；
    100 步钳位去重）。"""
    assert select_injection_steps(720, [3, 10, 20]) == [72, 240, 480]
    assert select_injection_steps(100, [3, 10, 20]) == [72, 98]
    with pytest.raises(ValueError, match="太小"):
        select_injection_steps(1, [10])


def test_attribute_failure_priority():
    """归因顺序：pass → twin_noise 优先 → oracle 候选胜出=模型缺口 → 其余
    计划面缺口。"""
    assert attribute_failure(0.0, 100.0, 100.0, 120.0, None, None,
                             "k")["reason"] == "pass"
    noisy = attribute_failure(50.0, 100.0, 100.0, 10.0, None, None, "k")
    assert noisy["twin_noise"] and not noisy["opponent_model_gap"]
    model_gap = attribute_failure(0.0, 100.0, 100.0, 90.0, 140.0, "other",
                                  "k")
    assert model_gap["opponent_model_gap"] and not model_gap["plan_space_gap"]
    space_gap = attribute_failure(0.0, 100.0, 100.0, 90.0, 95.0, "other", "k")
    assert space_gap["plan_space_gap"]      # oracle 95 未越过 reactive+eps
