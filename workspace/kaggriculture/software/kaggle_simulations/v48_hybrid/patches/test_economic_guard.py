"""test_economic_guard -- P2 补丁叶 economic_guard 的单元测试（R3 验收）。

覆盖三类验收面：
  A. 触发面覆盖：构造双死价局必触发；否决只砍买畜/建棚，其余命令与
     无目标步骤逐项原样（`is` 身份验证）。
  B. 正常局零影响：单死价 / 高价 / 波动毛刺 / 早窗 / 纯 EGG 死价
     一律零触发，且 veto 返回同一列表对象（零动作字面保证）。
  C. fail-safe：判定异常 / 观测垃圾 / 磁带垃圾 → 回退剧本原对象。

运行：python -m pytest <本文件> -q
"""

import ast
import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "economic_guard", os.path.join(_HERE, "economic_guard.py"))
eg = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(eg)


def make_obs(day=13, step=None, milk=160, wool=200, egg=50, player=0):
    """最小观测（dict 形态；模块对 dict 与 Struct 双兼容）。"""
    return {
        "step": step if step is not None else day * 24,
        "day": day,
        "hour": 0,
        "player": player,
        "market": {"prices": {"MILK": milk, "WOOL": wool, "EGG": egg}},
    }


def dead_obs(step, day=13, player=0):
    """灾难局形态：MILK 与 WOOL 双双 < 90（ep110634204 d13-d17 实证区间）。"""
    return make_obs(day=day, step=step, milk=88, wool=85, player=player)


def prime_guard(player=0, frames=None, start_step=300, day=13):
    """喂数据把护栏推到激活态（双死价连续 DEAD_PERSIST_STEPS 帧）。"""
    frames = frames if frames is not None else eg.DEAD_PERSIST_STEPS
    last = False
    for i in range(frames):
        last = eg.detect_dead_price_market(dead_obs(start_step + i, day=day,
                                                   player=player))
    return last


# ----------------------------- A. 触发面覆盖 --------------------------------

def test_double_dead_market_triggers_after_persist_frames():
    eg.reset_guard_state()
    results = [eg.detect_dead_price_market(dead_obs(300 + i)) for i in range(6)]
    # 前 3 帧未达持续帧数不触发，第 4 帧起触发并保持
    assert results[:3] == [False, False, False]
    assert results[3:] == [True, True, True]


def test_veto_active_cuts_only_animal_and_pasture_steps():
    eg.reset_guard_state()
    assert prime_guard() is True

    buy_animal_step = {
        "farmer": ["PASS"], "hands": [],
        "market": [["BUY_PRODUCT", "WHEAT", 4], ["HIRE"], ["HIRE"],
                   ["BUY_SEED", "MELON", 7], ["BUY_SEED", "WHEAT", 5],
                   ["BUY_ANIMAL", "SHEEP", 4]],
    }
    land_and_sell_step = {
        "farmer": ["PICKUP", "COW", 5],
        "hands": [["SOUTH"], ["PASS"], ["FEED"], ["EAST"]],
        "market": [["SELL", "MELON", 6], ["BUY_LAND"], ["SELL", "MELON", 6]],
    }
    pasture_step = {
        "farmer": ["FEED"],
        "hands": [["EAST"], ["COLLECT_FERTILIZER"], ["BUILD_PASTURE"],
                  ["PLANT", "STRAWBERRY"], ["WATER"]],
        "market": [["BUY_ANIMAL", "COW", 2], ["SELL", "WOOL", 2]],
    }
    untouched_step = {
        "farmer": ["NORTH"], "hands": [["HARVEST"], ["WATER"]], "market": [],
    }
    tape = [buy_animal_step, land_and_sell_step, pasture_step, untouched_step]

    out = eg.vetoe_animal_and_shed_steps(tape, dead_obs(400))

    # 否决面 1：BUY_ANIMAL 全部消失
    flat_market = [c for s in out for c in s["market"]]
    assert not any(c[0] == "BUY_ANIMAL" for c in flat_market)
    # 否决面 2：BUILD_PASTURE 原位换 PASS，hands 槽位数不变（手位对齐）
    hands = out[2]["hands"]
    assert len(hands) == 5
    assert hands[2] == ["PASS"]
    assert hands[0] is pasture_step["hands"][0]
    # 其余命令逐项原样放行（身份不变）：买地/雇佣/种子/卖单/喂食等
    assert out[0]["market"][:5] == buy_animal_step["market"][:5]
    assert out[0]["market"][0] is buy_animal_step["market"][0]
    assert out[1]["market"] == land_and_sell_step["market"]
    assert out[1]["market"][1] is land_and_sell_step["market"][1]
    assert out[1]["farmer"] is land_and_sell_step["farmer"]
    # 无否决目标的步骤保持原对象（步骤级零改动）
    assert out[3] is untouched_step
    assert out[1] is land_and_sell_step
    # 步数不变
    assert len(out) == 4


def test_veto_replaces_farmer_slot_pasture_with_pass():
    """磁带实测 BUILD_PASTURE 只出现在 hand 槽，farmer 槽按同语义兜底覆盖。"""
    eg.reset_guard_state()
    assert prime_guard() is True
    step = {"farmer": ["BUILD_PASTURE"], "hands": [], "market": []}
    out = eg.vetoe_animal_and_shed_steps([step], dead_obs(401))
    assert out[0]["farmer"] == ["PASS"]


# ----------------------------- B. 正常局零影响 ------------------------------

def test_healthy_market_never_triggers_and_returns_same_object():
    eg.reset_guard_state()
    tape = [{"farmer": ["PASS"], "hands": [],
             "market": [["BUY_ANIMAL", "COW", 1]]}]
    for i in range(30):
        obs = make_obs(step=i, day=i // 24, milk=160, wool=200)
        out = eg.vetoe_animal_and_shed_steps(tape, obs)
        assert out is tape  # 零动作字面保证：同一列表对象
        assert eg.detect_dead_price_market(make_obs(step=100 + i, day=13,
                                                    milk=160, wool=200)) is False


def test_single_dead_side_never_triggers():
    """单死价局（另一条产品线仍在挣钱，110629738 形态）零触发。"""
    eg.reset_guard_state()
    for i in range(20):
        wool_only = make_obs(step=300 + i, day=13, milk=150, wool=85)
        assert eg.detect_dead_price_market(wool_only) is False
        eg.reset_guard_state()
        milk_only = make_obs(step=300 + i, day=13, milk=82, wool=150)
        assert eg.detect_dead_price_market(milk_only) is False
        eg.reset_guard_state()


def test_volatile_blips_never_triggers():
    """波动局：双死价 2-3 帧毛刺后回升，反复循环——持续帧数滤除。"""
    eg.reset_guard_state()
    step = 300
    for cycle in range(5):
        for k in range(3):  # 连续 3 帧双死价（< DEAD_PERSIST_STEPS=4）
            assert eg.detect_dead_price_market(dead_obs(step)) is False
            step += 1
        recovery = make_obs(step=step, day=13, milk=120, wool=140)
        assert eg.detect_dead_price_market(recovery) is False
        step += 1
    tape = [{"farmer": ["PASS"], "hands": [["BUILD_PASTURE"]],
             "market": [["BUY_ANIMAL", "SHEEP", 2]]}]
    assert eg.vetoe_animal_and_shed_steps(tape, dead_obs(step)) is tape


def test_early_window_before_from_day_never_triggers():
    """d10 前曲线不可读（DEAD_PRICE_FROM_DAY=10）：即便双低价也不触发。"""
    eg.reset_guard_state()
    for i in range(20):
        obs = make_obs(step=i, day=8, milk=50, wool=40)
        assert eg.detect_dead_price_market(obs) is False


def test_egg_dead_alone_never_triggers():
    """纯 EGG 死价不入判定对（磁带无 GOOSE 线）。"""
    eg.reset_guard_state()
    for i in range(10):
        obs = make_obs(step=300 + i, day=13, milk=160, wool=200, egg=10)
        assert eg.detect_dead_price_market(obs) is False


def test_boundary_prices_just_at_floor_do_not_trigger():
    """地板价 90 本身不算死价（严格低于，与 constants 冻结语义一致）。"""
    eg.reset_guard_state()
    for i in range(10):
        obs = make_obs(step=300 + i, day=13, milk=90, wool=90)
        assert eg.detect_dead_price_market(obs) is False


# ----------------------------- C. fail-safe ---------------------------------

def test_garbage_observations_fail_closed_to_not_triggered():
    eg.reset_guard_state()
    garbage = [None, 42, "obs", {}, {"market": {}}, {"day": 13},
               {"day": 13, "market": {"prices": "x"}},
               {"day": "x", "market": {"prices": {"MILK": 88, "WOOL": 85}}},
               {"day": 13, "market": {"prices": {"MILK": "cheap",
                                                 "WOOL": 85}}},
               {"day": 13, "market": {"prices": {"MILK": True,
                                                 "WOOL": 85}}}]
    tape = [{"farmer": ["PASS"], "hands": [], "market": []}]
    for obs in garbage:
        assert eg.detect_dead_price_market(obs) is False
        assert eg.vetoe_animal_and_shed_steps(tape, obs) is tape


def test_garbage_tape_returns_input_unchanged_even_when_active():
    eg.reset_guard_state()
    assert prime_guard() is True
    for bad in [None, 42, "steps", {"farmer": ["PASS"]}]:
        assert eg.vetoe_animal_and_shed_steps(bad, dead_obs(500)) is bad
    mixed = ["junk-string", 7, {"farmer": ["BUILD_PASTURE"], "hands": [],
                                "market": [["BUY_ANIMAL", "COW", 1]]}]
    out = eg.vetoe_animal_and_shed_steps(mixed, dead_obs(501))
    assert out[0] == "junk-string" and out[0] is mixed[0]
    assert out[1] is mixed[1]
    assert out[2]["farmer"] == ["PASS"]
    assert out[2]["market"] == []


def test_rewind_resets_streak_for_new_episode():
    """step 回退（新对局/时钟倒退）自动清零：需重新攒满持续帧数。"""
    eg.reset_guard_state()
    assert prime_guard(start_step=300) is True
    # 倒退回早期 step -> 视为新对局重置；单帧双死价不再立即触发
    assert eg.detect_dead_price_market(dead_obs(100)) is False


def test_seats_keep_independent_streaks():
    eg.reset_guard_state()
    for i in range(eg.DEAD_PERSIST_STEPS - 1):
        eg.detect_dead_price_market(dead_obs(300 + i, player=0))
    assert eg.detect_dead_price_market(dead_obs(300, player=1)) is False
    assert eg.detect_dead_price_market(
        dead_obs(300 + eg.DEAD_PERSIST_STEPS - 1, player=0)) is True


def test_module_is_self_contained_stdlib_zero_import():
    """模块零 import（不依赖旧树/基底/任何包），AST 级验证。"""
    with open(os.path.join(_HERE, "economic_guard.py"), "r",
              encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    for node in ast.walk(tree):
        assert not isinstance(node, (ast.Import, ast.ImportFrom)), \
            "economic_guard 必须零 import（独立 stdlib 纯模块）"
