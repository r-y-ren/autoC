"""Track-B P1 孪生引擎保真测试（planner/twin.py + scripts/twin_fidelity.py）。

三层证据：
  1. 框架交叉核验：同动作流喂官方 kaggle_environments（env.step 慢路径）与
     孪生（解释器直驱），逐步型别敏感逐位比对 + 终局资金相等；
  2. 合成边界单元：空棚/满棚 DROP、动物逃亡、PLANT 原子降级、杂草按种子
     确定性生成、clone 隔离、run_to_end 回调式动作源、终局 DONE/reward 语义；
  3. 官方回放小样本快跑版：4 局 x 2 步点走保真门判据（<60s 预算内），
     语料缺失（gitignored 数据不在机）时按 pytest.skip 跳过。

全程 stdlib-only；不写任何输出文件（CLI 模式测试写 tmp_path）。
"""

from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

import pytest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from kaggle_simulations.agent.planner import twin  # noqa: E402
from kaggle_simulations.agent.planner.twin import (  # noqa: E401,E402
    TwinFingerprintError,
)

SCRIPTS = SOFTWARE / "scripts"
CORPUS_HINT = SOFTWARE.parent / "references" / "data" / "replay-corpus" / "raw"


# --------------------------------------------------------------------------
# 工具：合成回放头（与框架 _initialize 产物同构）
# --------------------------------------------------------------------------
def _synthetic_replay(seed=42, starting_money=3000.0, board=10, sheds=None,
                      seeds=None, tile_patch=None, unlocked=None,
                      episode_steps=720, shops=None):
    bundle = twin.load_engine()
    mod = bundle.module
    tiles = []
    for y in range(board):
        row = []
        for x in range(board):
            quadrant = ("N" if y < board // 2 else "S") + \
                       ("W" if x < board // 2 else "E")
            row.append(None if quadrant == "NW" else "LOCKED")
        tiles.append(row)
    if tile_patch:
        for (y, x), tile in tile_patch.items():
            tiles[y][x] = tile
    quads = ["NW"] + (unlocked or [])

    def farm():
        return {"money": float(starting_money), "tiles": json.loads(json.dumps(tiles)),
                "farmer": [board // 2 - 1, board // 2 - 1], "hands": [],
                "unlocked_quadrants": list(quads), "hires_today": 0}

    def private():
        return {
            "shed": dict.fromkeys(list(mod.PRODUCTS) + list(mod.ANIMALS), 0)
            if sheds is None else json.loads(json.dumps(sheds)),
            "seeds": dict.fromkeys(mod.CROPS, 0)
            if seeds is None else dict(seeds),
            "inventories": [{}],
        }

    market = {
        "inventory": {item: mod.MARKET_PARAMS[item]["I0"] for item in mod.PRODUCTS},
        "prices": {item: mod.MARKET_PARAMS[item]["base"] for item in mod.PRODUCTS},
    }
    head = []
    for player in (0, 1):
        obs = {
            "farms": [farm() for _ in range(2)],
            "market": json.loads(json.dumps(market)),
            "town": {"unlocked_shops": list(shops or [])},
            "day": 0, "hour": 0, "step": 0 if player == 0 else None,
            "player": player, "private": private(),
            "remainingOverageTime": 60,
        }
        head.append({"action": None, "status": "ACTIVE", "reward": 0,
                     "info": {}, "observation": obs})
    cfg = {"episodeSteps": episode_steps, "actTimeout": 1, "boardSize": board,
           "startingMoney": int(starting_money), "maxMarketOrdersPerTurn": 10,
           "turnsPerDay": 24, "shedCapacity": 100, "weedSpawnChance": 0.005,
           "townShopUnlockInterval": 3, "townShopSellInterval": 4,
           "townCenterSellInterval": 24, "seed": None, "farmHandCostMult": 1,
           "marketParams": {}}
    return {"steps": [head], "configuration": cfg, "info": {"seed": seed}}


# --------------------------------------------------------------------------
# 1) 引擎加载与指纹链
# --------------------------------------------------------------------------def test_engine_load_fingerprint_chain():
    bundle = twin.load_engine()
    assert bundle.fingerprint["wheel_sha256"] == twin.WHEEL_SHA256
    assert bundle.fingerprint["scene_py_sha256"] == twin.SCENE_PY_SHA256
    assert callable(bundle.interpreter)
    assert bundle.module.CROPS["WHEAT"]["seed"] == 10


def test_engine_fingerprint_fail_closed(tmp_path):
    bad_wheel = tmp_path / "bad.whl"
    bad_wheel.write_bytes(b"not a wheel")
    with pytest.raises(TwinFingerprintError):
        twin.load_engine(wheel_path=str(bad_wheel),
                         cache_dir=str(tmp_path / "cache"), force_reload=True)
    with pytest.raises(TwinFingerprintError):
        twin.load_engine(wheel_path=str(tmp_path / "missing.whl"),
                         cache_dir=str(tmp_path / "cache"), force_reload=True)


# --------------------------------------------------------------------------
# 2) 框架交叉核验（官方慢路径 vs 孪生快路径，逐步逐位）
# --------------------------------------------------------------------------
def _scripted_actions(rng, observations):
    acts = []
    for obs in observations:
        market = []
        if rng.random() < 0.5:
            market.append(["BUY_SEED", rng.choice(["WHEAT", "CARROT", "MELON"]),
                           rng.randint(1, 5)])
        if rng.random() < 0.4:
            market.append(["SELL", rng.choice(["WHEAT", "CARROT"]),
                           rng.randint(1, 10)])
        if rng.random() < 0.15:
            market.append(["HIRE"])
        if rng.random() < 0.1:
            market.append(["BUY_ANIMAL", "GOOSE", 1])
        if rng.random() < 0.1:
            market.append(["BUY_LAND"])
        farmer = rng.choice([["NORTH"], ["SOUTH"], ["EAST"], ["WEST"], ["PASS"],
                             ["WATER"], ["HARVEST"], ["DIG"], ["PLANT", "WHEAT"]])
        acts.append({"farmer": farmer, "hands": [], "market": market})
    return acts


@pytest.mark.parametrize("seed", [7, 12345])
def test_twin_matches_framework_step_by_step(seed):
    from kaggle_environments import make
    rng = random.Random(seed)
    env = make("kaggriculture",
               configuration={"episodeSteps": 96, "seed": seed}, debug=False)
    fake = {"steps": [env.toJSON()["steps"][0]],
            "configuration": dict(env.configuration),
            "info": {"seed": env.info["seed"]}}
    state = twin.new_state_from_replay_head(fake)
    for t in range(1, 96):
        actions = _scripted_actions(
            rng, [env.state[i].observation for i in (0, 1)])
        env.step(list(actions))
        twin.step(state, list(actions))
        ok, diffs = twin.states_bit_equal(state, {"steps": env.steps}, t)
        assert ok, f"seed={seed} step={t} diffs={diffs}"
    assert twin.final_money(state) == \
        [float(env.steps[-1][i].reward) for i in (0, 1)]


def test_twin_matches_framework_recorded_actions():
    """框架自跑（starter 自对局），孪生按回放动作流重演：逐步逐位一致。"""
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"episodeSteps": 96, "seed": 99}, debug=False)
    env.run(["starter", "starter"])
    replay = env.toJSON()
    state = twin.new_state_from_replay_head(replay)
    actions = twin.replay_transition_actions(replay)
    assert len(actions) == len(replay["steps"]) - 1
    for t in range(1, len(replay["steps"])):
        twin.step(state, actions[t - 1])
        ok, diffs = twin.states_bit_equal(state, replay, t)
        assert ok, f"step={t} diffs={diffs}"
    assert twin.final_money(state) == \
        [float(r) for r in twin.replay_final_rewards(replay)]


# --------------------------------------------------------------------------
# 3) build_state_from_replay / 快照等价 / clone 隔离 / run_to_end 接口
# --------------------------------------------------------------------------
@pytest.mark.parametrize("point", [0, 1, 7, 23, 24, 47, 95])
def test_build_state_from_replay_bitexact(point):
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"episodeSteps": 96, "seed": 5}, debug=False)
    env.run(["starter", "starter"])
    replay = env.toJSON()
    state = twin.build_state_from_replay(replay, point)
    ok, diffs = twin.states_bit_equal(state, replay, point)
    assert ok, f"point={point} diffs={diffs}"


def test_rebuild_snapshots_equals_per_point_build():
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"episodeSteps": 96, "seed": 11}, debug=False)
    env.run(["starter", "starter"])
    replay = env.toJSON()
    points = [1, 23, 24, 48, 95]
    snaps = twin.rebuild_snapshots(replay, points)
    for point in points:
        direct = twin.build_state_from_replay(replay, point)
        a = twin.canonical_json(twin.state_to_canonical(snaps[point]))
        b = twin.canonical_json(twin.state_to_canonical(direct))
        assert a == b, f"point={point}"


def test_clone_isolation_and_price_determinism():
    replay = _synthetic_replay(seed=7)
    state = twin.new_state_from_replay_head(replay)
    actions = [{"farmer": ["EAST"], "hands": [],
                "market": [["BUY_SEED", "WHEAT", 3]]},
               {"farmer": ["WEST"], "hands": [],
                "market": [["BUY_SEED", "CARROT", 2]]}]
    baseline = twin.canonical_json(twin.state_to_canonical(state))
    clone = twin.clone_state(state)
    twin.step(clone, actions)
    assert twin.canonical_json(twin.state_to_canonical(state)) == baseline, \
        "克隆推进不得污染原状态"
    twin.step(state, actions)
    assert twin.canonical_json(twin.state_to_canonical(clone)) == \
        twin.canonical_json(twin.state_to_canonical(state)), \
        "同动作下克隆与原状态必须等价"


def test_run_to_end_policy_callback_and_done_semantics():
    replay = _synthetic_replay(seed=3, episode_steps=48)
    state = twin.new_state_from_replay_head(replay)

    def always_pass(_state):
        return [{"farmer": ["PASS"], "hands": [], "market": []},
                {"farmer": ["PASS"], "hands": [], "market": []}]

    twin.run_to_end(state, always_pass)
    assert [s.status for s in state.seats] == ["DONE", "DONE"]
    # 解释器在 obs.step >= episodeSteps-2 时置 DONE 并写 reward = 终局资金。
    assert state.seats[0].observation.step == 47
    assert [s.reward for s in state.seats] == twin.final_money(state)
    assert twin.final_money(state) == [3000.0, 3000.0]


# --------------------------------------------------------------------------
# 4) 引擎语义边界（合成状态直驱）
# --------------------------------------------------------------------------
def test_drop_empty_and_full_shed_overflow():
    # 空棚 DROP：无随身库存，no-op。
    replay = _synthetic_replay(seed=1)
    state = twin.new_state_from_replay_head(replay)
    twin.step(state, [{"farmer": ["DROP"], "hands": [], "market": []},
                      {"farmer": ["PASS"], "hands": [], "market": []}])
    priv = state.seats[0].observation.private
    assert sum(priv["shed"].values()) == 0
    assert priv["inventories"][0] == {}

    # 满棚溢出：棚已占 98 格、随身 3 WHEAT -> DROP 落棚 2、弃 1（封顶 100）。
    mod = twin.load_engine().module
    sheds = dict.fromkeys(list(mod.PRODUCTS) + list(mod.ANIMALS), 0)
    sheds["WHEAT"] = 98
    replay = _synthetic_replay(seed=1, sheds=sheds)
    state = twin.new_state_from_replay_head(replay)
    state.seats[0].observation.private["inventories"][0]["WHEAT"] = 3
    twin.step(state, [{"farmer": ["DROP"], "hands": [], "market": []},
                      {"farmer": ["PASS"], "hands": [], "market": []}])
    priv = state.seats[0].observation.private
    assert sum(priv["shed"].values()) == 100, "棚必须恰好 100（溢出丢弃）"
    assert priv["shed"]["WHEAT"] == 100 and priv["inventories"][0] == {}


def test_buy_product_blocked_when_shed_full():
    mod = twin.load_engine().module
    sheds = dict.fromkeys(list(mod.PRODUCTS) + list(mod.ANIMALS), 0)
    sheds["FERTILIZER"] = 100
    replay = _synthetic_replay(seed=1, sheds=sheds)
    state = twin.new_state_from_replay_head(replay)
    twin.step(state, [{"farmer": ["PASS"], "hands": [],
                       "market": [["BUY_PRODUCT", "FERTILIZER", 1]]},
                      {"farmer": ["PASS"], "hands": [], "market": []}])
    seat = state.seats[0]
    assert seat.observation.private["shed"]["FERTILIZER"] == 100
    assert seat.observation.farms[0]["money"] == 3000.0, \
        "满棚 BUY_PRODUCT 必须整单失败（钱不变）"


def test_animal_escape_after_two_unfed_days():
    mod = twin.load_engine().module
    # GOOSE placed_day=0, first_yield_day=4：day0 放置、连续两天不喂 ->
    # day1 EOD unfed 计 1、day2 EOD 计 2 -> 逃走、COOP 结构保留。
    coop = {"kind": "COOP", "animal": "GOOSE", "placed_day": 0,
            "yield_units": 0, "consecutive_unfed": 1, "fed_today": False,
            "cared_today": False, "fertilizer_available": False,
            "pending_care_bonus": 0}
    replay = _synthetic_replay(seed=1,
                               tile_patch={(2, 2): dict(coop)},
                               sheds=None)
    # 给一单位 WHEAT 以便第一步喂饲被测逃逸路径的正确性：不喂，直接推 2 天。
    state = twin.new_state_from_replay_head(replay)
    for _ in range(48):  # day0 -> day2 的两个 EOD
        twin.step(state, [{"farmer": ["PASS"], "hands": [], "market": []},
                          {"farmer": ["PASS"], "hands": [], "market": []}])
    tile = state.seats[0].observation.farms[0]["tiles"][2][2]
    assert tile == {"kind": "COOP"}, "连续两天未喂 -> 动物逃走、结构保留"


def test_plant_atomic_downgrade_when_seeds_insufficient():
    replay = _synthetic_replay(seed=1, seeds={"WHEAT": 1})
    state = twin.new_state_from_replay_head(replay)
    # 农夫 (4,4) + 一个 hand 位各报 1 条 PLANT WHEAT，种子仅 1 ->
    # 当回合 PLANT 总需求 2 > 1：两条全部降级 PASS（原子校验）。
    state.seats[0].observation.farms[0]["farmer"] = [4, 4]
    action = {"farmer": ["PLANT", "WHEAT"],
              "hands": [["PLANT", "WHEAT"]], "market": []}
    twin.step(state, [action, {"farmer": ["PASS"], "hands": [], "market": []}])
    tiles = state.seats[0].observation.farms[0]["tiles"]
    assert tiles[4][4] is None, "PLANT 超种子必须整回合降级"
    assert state.seats[0].observation.private["seeds"]["WHEAT"] == 1


def test_market_lockstep_both_sellers_same_price_quotes():
    """双席同回合各卖 2 WHEAT：per-unit 锁步、同库存报价、玩家序提交。
    每席两单分别在库存 10000 / 10002 报价，双边同价。"""
    mod = twin.load_engine().module
    sheds = dict.fromkeys(list(mod.PRODUCTS) + list(mod.ANIMALS), 0)
    sheds["WHEAT"] = 2
    replay = _synthetic_replay(seed=1, sheds=sheds)
    state = twin.new_state_from_replay_head(replay)
    price0 = state.seats[0].observation.market["prices"]["WHEAT"]
    twin.step(state, [{"farmer": ["PASS"], "hands": [],
                       "market": [["SELL", "WHEAT", 2]]},
                      {"farmer": ["PASS"], "hands": [],
                       "market": [["SELL", "WHEAT", 2]]}])
    market = state.seats[0].observation.market
    expected_gain = mod.market_price("WHEAT", 10000) \
        + mod.market_price("WHEAT", 10002)
    assert expected_gain == price0 + mod.market_price("WHEAT", 10002)
    assert state.seats[0].observation.farms[0]["money"] == 3000.0 + expected_gain
    assert state.seats[1].observation.farms[1]["money"] == 3000.0 + expected_gain, \
        "锁步双边同库存报价 -> 双席成交额对称"
    # 4 单成交 +3 库存：step 0 城中心消费（step%24==0）在市阶段之后扣 1 WHEAT。
    assert market["inventory"]["WHEAT"] == 10003
    assert market["prices"]["WHEAT"] < price0, "卖出后价格必须下降"


def test_weed_spawn_deterministic_by_seed():
    """杂草/商店由 seed 按日重播种驱动：同 seed 同轨迹、异 seed 异轨迹。"""
    def weeds_after_three_days(seed):
        replay = _synthetic_replay(seed=seed)
        state = twin.new_state_from_replay_head(replay)
        for _ in range(72):  # 3 个 EOD
            twin.step(state, [{"farmer": ["PASS"], "hands": [], "market": []},
                              {"farmer": ["PASS"], "hands": [], "market": []}])
        farms = state.seats[0].observation.farms
        return [(i, sum(1 for row in f["tiles"] for t in row
                        if isinstance(t, dict) and t.get("kind") == "WEED"))
                for i, f in enumerate(farms)], \
            [f["tiles"] for f in farms]

    weeds_a, tiles_a = weeds_after_three_days(424242)
    weeds_a2, tiles_a2 = weeds_after_three_days(424242)
    weeds_b, tiles_b = weeds_after_three_days(424243)
    assert tiles_a == tiles_a2, "同 seed 必须逐步复现"
    assert tiles_a != tiles_b, "异 seed 杂草轨迹必须不同（p=0.005/格/天）"


# --------------------------------------------------------------------------
# 5) 官方回放小样本（快跑版保真门判据；语料缺失则跳过）
# --------------------------------------------------------------------------
def _corpus_available():
    return CORPUS_HINT.is_dir() and any(CORPUS_HINT.glob("episode-*-replay.json"))


@pytest.mark.skipif(not _corpus_available(), reason="官方回放语料不在本机（gitignored）")
def test_official_replays_small_gate(tmp_path):
    sys.path.insert(0, str(SCRIPTS))
    import twin_fidelity
    games = twin_fidelity.discover_games()
    assert len(games) >= 100, "语料应 >= 100 局"
    picks = [games[0], games[len(games) // 3], games[2 * len(games) // 3],
             games[-1]]
    report = {"pass_games": 0}
    bundle = twin.load_engine()
    for group, path in picks:
        result = twin_fidelity.check_game(path, [100, 540], bundle)
        assert result["pass"], \
            f"{group}/{result['id']}: {json.dumps(result['attribution'], ensure_ascii=False)}"
        report["pass_games"] += 1
    assert report["pass_games"] == len(picks)


@pytest.mark.skipif(not _corpus_available(), reason="官方回放语料不在本机（gitignored）")
def test_cli_smoke_mode_contract(tmp_path):
    """CLI 契约：--mode smoke 退出码 0 且产出 report（summary 可传 '' 跳过）。"""
    out = tmp_path / "fidelity_report.json"
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "twin_fidelity.py"), "--mode", "smoke",
         "--games", "2", "--steps-per-game", "2",
         "--out", str(out), "--summary", ""],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["verdict"]["overall_pass"] is True
    assert payload["verdict"]["games"] == 2
    assert payload["verdict"]["sample_points"] == 4
