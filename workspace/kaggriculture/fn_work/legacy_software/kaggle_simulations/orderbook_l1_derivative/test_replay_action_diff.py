"""test_replay_action_diff（门③(a) 叶专属测试）。

三组用例（2026-09-23 语料实测基线）：
  ① 真局 seated 重演（3 局，控制耗时）：112433355(seat0)/112446302(seat1)
     有截断——identical_mod_seed_drop=True 且 dropped 逐条对得上原局该步
     BUY_SEED 订单（形态恰为 BUY_SEED 消失），且 l1_final−verbatim_final
     == 被截订单票价合计（纯减法的资金面推论）；112429867 无截断——空集
     合法（identical=True、dropped=[]）。
  ② 差异注入（截取前 8 步的小 strip + 假 callable，秒级）：改一张 SELL
     数量 → identical=False 且 first_divergence.kind="market"；改 hands →
     kind="hands"；BUY_SEED 改量（非整单消失）→ kind="market"（形态严格
     性：减量购买不是允许形态）。
  ③ 异常路径 fail-closed：坏文件/缺我方队名/坏 main 路径 → {"error": …}。

真局耗时实测：每局 ~1.8-2.5s（含双 main 官方装载与 verbatim 对照重演），
3 局合计 ~7s；注入/异常用例合计 <2s；本文件全量 ~9s（2026-09-23 实测
~9.4s，26 局全量参考值 49.2s）。
"""

import copy
import gzip
import json
import os

import pytest

import gate_equivalence_precision as g

_HERE = os.path.dirname(os.path.abspath(__file__))
_STRIP_DIR = g._STRIP_DIR_DEFAULT
L1_MAIN = os.path.join(_HERE, "main.py")
VERBATIM_MAIN = os.path.normpath(
    os.path.join(_HERE, "..", "orderbook_derivative", "main.py"))

# ① 用局挑选依据（2026-09-23 26 局全跑实测）：112433355 截 WHEAT×1($10)
# 且全程一致；112446302 截 WHEAT×3($30) 且全程一致；112429867 无截断。
EP_WITH_DROPS = ("112433355", "112446302")
EP_NO_DROP = "112429867"


def _strip_path(ep):
    path = os.path.join(_STRIP_DIR, f"episode-{ep}-strip.json.gz")
    if not os.path.isfile(path):
        pytest.skip(f"strip 语料不在本机: {path}")
    return path


def _my_recorded_buy_seeds(replay, me):
    """原局我席 BUY_SEED 订单真值表：{step: [(crop, qty), …]}。"""
    actions = g._twin().replay_transition_actions(replay)
    table = {}
    for t, pair in enumerate(actions):
        for order in (pair[me] or {}).get("market") or []:
            if g._is_buy_seed(order):
                table.setdefault(t, []).append((order[1], int(order[2])))
    return table


# ---------------------------------------------------------------------------
# ① 真局 seated 重演（耗时 ~7s）
# ---------------------------------------------------------------------------
def test_real_episodes_seed_drop_form():
    for ep in EP_WITH_DROPS:
        result = g.replay_action_diff(_strip_path(ep), L1_MAIN, VERBATIM_MAIN)
        assert "error" not in result, (ep, result.get("error"))
        assert set(result) >= {
            "episode", "seat", "identical_mod_seed_drop", "dropped",
            "first_divergence", "l1_final", "verbatim_final",
            "steps_compared"}
        assert result["episode"] == int(ep)
        assert result["identical_mod_seed_drop"] is True
        assert result["first_divergence"] is None
        assert result["steps_compared"] == 719  # 整季 720 步条目=719 转移
        assert result["dropped"], f"{ep} 应有截断（2026-09-23 实测基线）"
        # dropped 逐条恰为原局该步真实存在的 BUY_SEED 订单（纯消失形态）
        with gzip.open(_strip_path(ep), "rt", encoding="utf-8") as fh:
            replay = json.load(fh)
        me = result["seat"]
        truth = _my_recorded_buy_seeds(replay, me)
        value = 0
        for entry in result["dropped"]:
            assert set(entry) == {"step", "crop", "qty"}
            assert (entry["crop"], entry["qty"]) in truth.get(entry["step"], [])
            value += entry["qty"] * g.SEED_PRICE[entry["crop"]]
        # 纯减法的资金面推论：未花出的种子钱原样留在终局
        assert round(result["l1_final"] - result["verbatim_final"], 6) == value


def test_real_episode_empty_drop_is_legal():
    result = g.replay_action_diff(_strip_path(EP_NO_DROP), L1_MAIN, VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    assert result["identical_mod_seed_drop"] is True
    assert result["dropped"] == []
    assert result["first_divergence"] is None
    assert result["l1_final"] == result["verbatim_final"]


# ---------------------------------------------------------------------------
# ② 差异注入（小 strip + 假 callable；verbatim 走真 callable 对照）
# ---------------------------------------------------------------------------
def _tiny_strip(tmp_path, n_steps=8):
    """截取 112429867 前 n_steps 步（head 逐字 + n-1 转移）写普通 json。"""
    with gzip.open(_strip_path(EP_NO_DROP), "rt", encoding="utf-8") as fh:
        replay = json.load(fh)
    replay["steps"] = replay["steps"][:n_steps]
    out = tmp_path / "tiny-strip.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(replay, fh)
    return str(out), replay


def _mutated_stream_callable(replay, me, mutate):
    """假 callable：逐字重放原局我席动作流，但先经 mutate(stream) 注入差异。"""
    stream = [copy.deepcopy((pair[me] or {}))
              for pair in g._twin().replay_transition_actions(replay)]
    target_step = mutate(stream)

    def fake(obs):
        return stream[int(obs["step"])]
    return fake, target_step


def _bump_first_sell_qty(stream):
    """把流里第一张 SELL 单数量 +1；返回注入步号。"""
    for t, action in enumerate(stream):
        for order in action.get("market") or []:
            if isinstance(order, (list, tuple)) and order and order[0] == "SELL":
                order[2] = int(order[2]) + 1
                return t
    raise AssertionError("注入夹具失配：前 8 步无 SELL 单")


def _bump_hands(stream):
    """把流里第一个非空 hands 改成 ['PASS']；返回注入步号。"""
    for t, action in enumerate(stream):
        if action.get("hands"):
            action["hands"] = [["PASS"]] * len(action["hands"])
            return t
    raise AssertionError("注入夹具失配：前 8 步无 hands 动作")


def _reduce_first_buy_seed(stream):
    """把流里第一张 BUY_SEED 数量减 1（非整单消失=不允许形态）；返回步号。"""
    for t, action in enumerate(stream):
        for order in action.get("market") or []:
            if g._is_buy_seed(order):
                order[2] = int(order[2]) - 1
                return t
    raise AssertionError("注入夹具失具：前 8 步无 BUY_SEED 单")


@pytest.mark.parametrize("mutate,expected_kind", [
    (_bump_first_sell_qty, "market"),
    (_bump_hands, "hands"),
    (_reduce_first_buy_seed, "market"),
])
def test_injected_divergence_flagged(tmp_path, mutate, expected_kind):
    tiny, replay = _tiny_strip(tmp_path)
    me = g._my_seat(replay)
    fake, target_step = _mutated_stream_callable(replay, me, mutate)
    result = g.replay_action_diff(tiny, fake, VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    assert result["identical_mod_seed_drop"] is False
    fd = result["first_divergence"]
    assert set(fd) == {"step", "kind", "detail"}
    assert fd["step"] == target_step
    assert fd["kind"] == expected_kind
    assert isinstance(fd["detail"], str) and fd["detail"]
    assert result["steps_compared"] == target_step + 1  # 判异类那步计入即停


# ---------------------------------------------------------------------------
# ③ 异常路径 fail-closed
# ---------------------------------------------------------------------------
def test_missing_replay_file_is_error():
    result = g.replay_action_diff(
        "/nonexistent/episode-0-strip.json.gz", L1_MAIN, VERBATIM_MAIN)
    assert set(result) == {"error"}
    assert "装载/语料失败" in result["error"]


def test_corrupted_gz_is_error(tmp_path):
    bad = tmp_path / "episode-0-strip.json.gz"
    bad.write_bytes(b"\x1f\x8b not-really-gzip")
    result = g.replay_action_diff(str(bad), L1_MAIN, VERBATIM_MAIN)
    assert set(result) == {"error"}
    assert "装载/语料失败" in result["error"]


def test_replay_without_our_team_is_error(tmp_path):
    _, replay = _tiny_strip(tmp_path, n_steps=8)
    replay["teams"] = ["alice", "bob"]
    replay["info"]["TeamNames"] = ["alice", "bob"]
    alien = tmp_path / "alien.json"
    with open(alien, "w", encoding="utf-8") as fh:
        json.dump(replay, fh)
    result = g.replay_action_diff(str(alien), L1_MAIN, VERBATIM_MAIN)
    assert set(result) == {"error"}
    assert "renyxin" in result["error"]


def test_bad_main_path_is_error(tmp_path):
    tiny, _ = _tiny_strip(tmp_path, n_steps=8)
    result = g.replay_action_diff(tiny, "/nonexistent/main.py", VERBATIM_MAIN)
    assert set(result) == {"error"}
    assert "装载/语料失败" in result["error"]
