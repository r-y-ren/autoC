"""rollout_with_replay_opponent 真实行为测试（R2 seated 通道）。

覆盖（对齐 fn_docs/responsibility.md run_official_bench 块该节核验命令）：
① R2 快照反例复刻（合成回放生成方式复刻自 snapshot_tests/
   test_counterexample_r2.py——引擎固定种子 20260921，seat0=恒 PASS→3000.0、
   seat1=每 5 回合买 1 包 WHEAT 种子→1570.0；不 import snapshot_tests）：
   me_seat=1 → [3000.0, 1570.0]；me_seat=0 → 同序双通道一致（返回序与
   我方席位解耦，两席人格各自复刻时同出 [3000.0, 1570.0]）。
② 注入点语义：d0（注入 0）与中间步（注入 100）各一——中间步先按官方
   动作流重演至该步、我方 callable 自该步起接管 me_seat 席。
③ 回放缺失抛 ValueError；指纹不符抛 TwinFingerprintError（篡改 wheel
   副本经 make_twin_deps(wheel_path=..., force_reload=True) 实测）。
"""

import pytest

from kaggle_environments import make

from run_official_bench.rollout_with_replay_opponent import (
    TwinFingerprintError,
    make_twin_deps,
    rollout_with_replay_opponent,
)

SEED = 20260921
EPISODE_STEPS = 720

# 合成回放终局真值（脚本 + 种子决定，与 snapshot_tests 冻结口径一致）。
FROZEN_REPLAY_REWARDS = [3000.0, 1570.0]
# 旧 bench 通道 me_seat=1 的错位输出（双席互换伪影，冻结口径）——本通道
# 不得再出此值。
FROZEN_BENCH_MISSEATED_FINAL = [1570.0, 3000.0]


def _pass_bot(obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _seed_buyer_bot():
    """状态无关脚本：每第 5 个决策买 1 包 WHEAT 种子（与回放生成脚本同源）。"""
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
# ① R2 快照反例复刻
# ---------------------------------------------------------------------------

def test_r2_counterexample_me_seat1_seated_truth(synthetic_replay):
    """me_seat=1 + 我方 callable=生成回放 seat1 的同源脚本 → 精确复现回放
    真值 [3000.0, 1570.0]（我方动作注入我方实际席位）；显式区别于旧 bench
    错位伪影 [1570.0, 3000.0]。"""
    final = rollout_with_replay_opponent(
        synthetic_replay, 0, _seed_buyer_bot(), 1)
    assert final == FROZEN_REPLAY_REWARDS
    assert final != FROZEN_BENCH_MISSEATED_FINAL


def test_me_seat0_same_seat_ordered_output(synthetic_replay):
    """me_seat=0 + 我方 callable=seat0 人格（恒 PASS）→ 同序输出
    [3000.0, 1570.0]：返回序=(seat0, seat1) 与我方席位解耦——两席人格
    各自复刻时 me_seat∈{0,1} 同出真值序。"""
    final0 = rollout_with_replay_opponent(
        synthetic_replay, 0, _pass_bot, 0)
    final1 = rollout_with_replay_opponent(
        synthetic_replay, 0, _seed_buyer_bot(), 1)
    assert final0 == final1 == FROZEN_REPLAY_REWARDS


# ---------------------------------------------------------------------------
# ② 注入点语义（d0 与中间步各一；d0 已由 ① 覆盖，此处为中间步）
# ---------------------------------------------------------------------------

def test_injection_point_midgame_splices_agent_from_step(synthetic_replay):
    """注入 100：注入态=官方动作流重演至第 100 步（seat1 磁带已买
    20 包 WHEAT 种子 → 3000-200=2800），我方 callable（恒 PASS）自该步起
    接管 seat1 → 不再买种子。me_seat=0 人格复刻（磁带本就全 PASS）仍精确
    复现真值，验证中间注入态重建与动作流拼接两侧各自正确。"""
    # 中间注入 + 席位接管（seat1 自 100 步起换人格 → 终局停在 2800.0）
    final_takeover = rollout_with_replay_opponent(
        synthetic_replay, 100, _pass_bot, 1)
    assert final_takeover[0] == 3000.0
    assert final_takeover[1] == 2800.0
    assert final_takeover != FROZEN_REPLAY_REWARDS
    # 中间注入 + 人格复刻（seat0 磁带恒 PASS，callable 同人格）→ 精确真值
    final_replay_persona = rollout_with_replay_opponent(
        synthetic_replay, 100, _pass_bot, 0)
    assert final_replay_persona == FROZEN_REPLAY_REWARDS


def test_injection_point_d0_full_season(synthetic_replay):
    """d0 注入（injection_point=0）：自初态起我方接管——me_seat=1 同源
    脚本整季重演（快照反例主口径，与 ① 互为独立断言面）。"""
    final = rollout_with_replay_opponent(
        synthetic_replay, 0, _seed_buyer_bot(), 1)
    assert final == FROZEN_REPLAY_REWARDS


# ---------------------------------------------------------------------------
# ③ 错误面：回放缺失 / 指纹不符
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_replay", [None, {}, {"steps": []},
                                        {"configuration": {}, "steps": []}])
def test_replay_missing_raises(bad_replay):
    """回放缺失（None/非含 steps 映射/空 steps）→ ValueError，不触引擎。"""
    with pytest.raises(ValueError, match="回放缺失"):
        rollout_with_replay_opponent(bad_replay, 0, _pass_bot, 1)


def test_invalid_me_seat_raises(synthetic_replay):
    with pytest.raises(ValueError, match="me_seat"):
        rollout_with_replay_opponent(synthetic_replay, 0, _pass_bot, 2)


def test_fingerprint_mismatch_raises(synthetic_replay, tmp_path):
    """指纹不符抛：vendored wheel 的篡改副本（末字节翻转）经
    make_twin_deps(wheel_path=..., force_reload=True) → build 内
    twin.load_engine 的 fail-closed sha256 校验拒绝加载，异常原样传播。"""
    wheel = _vendored_wheel()
    data = bytearray(wheel.read_bytes())
    data[-1] ^= 0xFF
    bad = tmp_path / wheel.name
    bad.write_bytes(bytes(data))
    deps = make_twin_deps(wheel_path=str(bad), force_reload=True)
    with pytest.raises(TwinFingerprintError):
        rollout_with_replay_opponent(
            synthetic_replay, 0, _seed_buyer_bot(), 1, deps=deps)


def _vendored_wheel():
    """定位 vendored wheel（自测试文件上溯战役根；只读，不 import 旧树
    scripts/）。"""
    from pathlib import Path

    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists()
               for name in ("blueprint.md", "software", "fn_docs")):
            wheels = sorted((candidate / "software" / "vendor").glob("*.whl"))
            assert len(wheels) == 1, f"期望唯一 vendored wheel, got {wheels}"
            return wheels[0]
    raise AssertionError("未找到战役根（blueprint.md+software+fn_docs）")
