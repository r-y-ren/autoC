"""test_replay_action_diff（门③(a) 叶专属测试，2026-09-24 双判据口径）。

五组用例（语料实测基线 2026-09-23/24）：
  ① 真局 seated 重演（4 局，控制耗时）：112433355(seat0)/112446302(seat1)
     有截断——divergences 全量恰为 buy_seed_disappear、game_pass=True、
     dropped 逐条对得上原局该步 BUY_SEED 订单、l1_final−verbatim_final ==
     被截订单票价合计（纯减法的资金面推论）；112429867 无截断——空集合法
     （divergences=[]、game_pass=True）；112432199 基座回买反应局——全量
     枚举=5×buy_seed_disappear+1×buy_seed_appear@662（同步出现拆两条 kind）、
     步界 652≥648、final_delta=+10、game_pass=True 且 (a') 严格面 False。
  ② 分类器矩阵（纯函数直喂，秒级）：允许形态三 kind 各自/组合/改量分解、
     violation 形态（farmer/hands/非种子非卖单/重排/结构异常/键集/形态）。
  ③ 局级双判据矩阵（_adjudicate_game 纯函数直喂）：步界/结果面/violation
     三轴独立红、first_divergence 定位语义。
  ④ 差异注入（截取前 8 步的小 strip + 假 callable，秒级）：改 SELL 数量 →
     sell_order_change（早步=步界破缺定位）；改 hands → violation kind="hands"；
     BUY_SEED 改量 → 消失+出现两条（改量单分解）；全量枚举不提前停。
  ⑤ 异常路径 fail-closed：坏文件/缺我方队名/坏 main 路径 → {"error": …}。

真局耗时实测：每局 ~2s（含双 main 官方装载与 verbatim 对照重演），4 局
合计 ~8s；注入/矩阵/异常用例合计 <3s（2026-09-24 实测本文件全量 ~10.5s，
26 局全量参考值 ~50s）。
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

# ① 用局挑选依据（2026-09-23/24 语料实测）：112433355 截 WHEAT×1($10)
# 且全程一致；112446302 截 WHEAT×3($30) 且全程一致；112429867 无截断；
# 112432199 基座回买反应局（截 5 单 @652-662，@662 回买 CARROT×8，
# final_delta +10——旧严格口径红、新双判据绿）。
EP_WITH_DROPS = ("112433355", "112446302")
EP_NO_DROP = "112429867"
EP_REACTION = "112432199"


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
# ① 真局 seated 重演（耗时 ~8s）
# ---------------------------------------------------------------------------
def test_real_episodes_seed_drop_form():
    for ep in EP_WITH_DROPS:
        result = g.replay_action_diff(_strip_path(ep), L1_MAIN, VERBATIM_MAIN)
        assert "error" not in result, (ep, result.get("error"))
        assert set(result) >= {
            "episode", "seat", "game_pass", "divergences",
            "identical_mod_seed_drop", "dropped", "first_divergence",
            "l1_final", "verbatim_final", "steps_compared", "replay_path",
            "n_divergences", "n_violations", "steps_boundary_ok",
            "result_face_ok", "min_divergence_step"}
        assert result["episode"] == int(ep)
        assert result["game_pass"] is True
        assert result["first_divergence"] is None  # 无取消格差异（violation 定位用）
        assert result["steps_compared"] == 719  # 全量枚举：整季 720 步条目=719 转移
        assert result["dropped"], f"{ep} 应有截断（2026-09-23 实测基线）"
        # 全量枚举：divergences 恰为纯 BUY_SEED 消失形态，逐条=dropped
        assert result["n_divergences"] == len(result["dropped"])
        assert all(d["kind"] == "buy_seed_disappear"
                   for d in result["divergences"])
        assert result["identical_mod_seed_drop"] is True  # (a') 严格面留档
        # 步界：全部差异步 ≥ _CXS_FROM 同源阈值
        threshold = g._cxs_from()
        assert result["steps_boundary_ok"] is True
        assert result["min_divergence_step"] >= threshold
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
        # 纯减法的资金面推论：未花出的种子钱原样留在终局（结果面非负）
        assert result["result_face_ok"] is True
        assert round(result["l1_final"] - result["verbatim_final"], 6) == value


def test_real_episode_empty_drop_is_legal():
    result = g.replay_action_diff(_strip_path(EP_NO_DROP), L1_MAIN, VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    assert result["game_pass"] is True
    assert result["divergences"] == [] and result["dropped"] == []
    assert result["n_divergences"] == 0 and result["n_violations"] == 0
    assert result["first_divergence"] is None
    assert result["min_divergence_step"] is None
    assert result["l1_final"] == result["verbatim_final"]


def test_real_reaction_episode_full_enumeration():
    """基座回买反应局（旧严格口径红 → 新双判据绿，2026-09-24 口径核心样本）。

    全量枚举实测（2026-09-24）：5×buy_seed_disappear（@652/656/657/658/662）
    + 1×buy_seed_appear@662（CARROT×8 回买）——@662 同步出现 BUY_SEED 差异
    拆两条 kind；步界 652≥648；final_delta=+10（结果面非负）；无 violation。
    """
    result = g.replay_action_diff(_strip_path(EP_REACTION), L1_MAIN,
                                  VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    assert result["game_pass"] is True
    assert result["n_violations"] == 0
    assert result["first_divergence"] is None
    assert result["steps_boundary_ok"] is True
    assert result["min_divergence_step"] == 652
    kinds = [d["kind"] for d in result["divergences"]]
    assert kinds.count("buy_seed_disappear") == 5
    assert kinds.count("buy_seed_appear") == 1
    assert set(kinds) <= set(g.ALLOWED_DIVERGENCE_KINDS)
    # @662 同步：消失(CARROT,3) 与 出现(CARROT,8) 拆两条 kind
    at_662 = [d for d in result["divergences"] if d["step"] == 662]
    assert {(d["kind"], d.get("crop"), d.get("qty")) for d in at_662} == {
        ("buy_seed_disappear", "CARROT", 3),
        ("buy_seed_appear", "CARROT", 8)}
    # dropped=消失汇总（subset 消费面兼容）；(a') 严格面 False（有回买形态）
    assert len(result["dropped"]) == 5
    assert result["identical_mod_seed_drop"] is False
    assert result["result_face_ok"] is True
    assert round(result["l1_final"] - result["verbatim_final"], 6) == 10.0


# ---------------------------------------------------------------------------
# ② 分类器矩阵（_classify_divergence 纯函数直喂）
# ---------------------------------------------------------------------------
def _act(market, farmer=None, hands=None):
    return {"farmer": farmer or [], "hands": hands or [], "market": market}


_BS_W1 = ["BUY_SEED", "WHEAT", 1]
_BS_C3 = ["BUY_SEED", "CARROT", 3]
_BS_C8 = ["BUY_SEED", "CARROT", 8]
_SELL_E4 = ["SELL", "EGG", 4]
_SELL_E5 = ["SELL", "EGG", 5]


def _kinds(records):
    return [r["kind"] for r in records]


def test_classifier_pure_disappear():
    got = g._classify_divergence(_act([_BS_W1, _SELL_E4]),
                                 _act([_SELL_E4]))
    assert _kinds(got) == ["buy_seed_disappear"]
    assert got[0]["crop"] == "WHEAT" and got[0]["qty"] == 1
    assert "verbatim 有 L1 无" in got[0]["detail"]


def test_classifier_pure_appear():
    got = g._classify_divergence(_act([_SELL_E4]), _act([_BS_C8, _SELL_E4]))
    assert _kinds(got) == ["buy_seed_appear"]
    assert got[0]["crop"] == "CARROT" and got[0]["qty"] == 8


def test_classifier_qty_change_splits_disappear_and_appear():
    # 改量单（3→2）分解为 消失(3)+出现(2) 两条允许形态（多重集差语义）
    got = g._classify_divergence(_act([_BS_C3]), _act([["BUY_SEED", "CARROT", 2]]))
    assert _kinds(got) == ["buy_seed_disappear", "buy_seed_appear"]
    assert got[0]["qty"] == 3 and got[1]["qty"] == 2


def test_classifier_duplicate_orders_counted_per_unit():
    # 同名单两份消失一份：多重集差逐单一条（不能整类合并）
    got = g._classify_divergence(_act([_BS_C3, _BS_C3, _SELL_E4]),
                                 _act([_BS_C3, _SELL_E4]))
    assert _kinds(got) == ["buy_seed_disappear"]


def test_classifier_sell_sequence_change():
    # SELL 序列任何差（品/量/序）= sell_order_change 一条
    for l1_market in ([_SELL_E5], [], [_SELL_E4, _SELL_E5]):
        got = g._classify_divergence(_act([_SELL_E4]), _act(l1_market))
        assert _kinds(got) == ["sell_order_change"], l1_market


def test_classifier_seed_and_sell_same_step_split_two_kinds():
    got = g._classify_divergence(_act([_SELL_E4]), _act([_BS_C8, _SELL_E5]))
    assert set(_kinds(got)) == {"buy_seed_appear", "sell_order_change"}  # 拆两条


def test_classifier_farmer_hands_diff_is_violation():
    for field in ("farmer", "hands"):
        expected = _act([], farmer=[["PLANT", "CARROT", 0, 0]])
        mutated = _act([], farmer=[["PLANT", "CARROT", 0, 0]])
        mutated[field] = [["PASS"]]
        got = g._classify_divergence(expected, mutated)
        assert _kinds(got) == [field], field  # 单位动作变化=violation（kind=字段名）


def test_classifier_non_seed_non_sell_market_change_is_violation():
    base = _act([["HIRE", "FARMER", 0, 0]])
    for mutated_market in ([], [["HIRE", "FARMER", 1, 0]],
                           [["BUY_PRODUCT", "EGG", 1]]):
        got = g._classify_divergence(base, _act(mutated_market))
        assert _kinds(got) == ["market"], mutated_market


def test_classifier_buy_seed_reorder_is_violation():
    # 多重集同、槽位序变：不可归入允许形态 → fail-closed violation
    got = g._classify_divergence(_act([_BS_W1, _BS_C3, _SELL_E4]),
                                 _act([_BS_C3, _BS_W1, _SELL_E4]))
    assert _kinds(got) == ["market"]
    assert "不可归入允许形态" in got[0]["detail"]


def test_classifier_malformed_seed_order_is_violation():
    got = g._classify_divergence(_act([_SELL_E4]),
                                 _act([["BUY_SEED", "CARROT", "many"], _SELL_E4]))
    assert _kinds(got) == ["market"]
    assert "结构异常" in got[0]["detail"]


def test_classifier_shape_and_keys_violations():
    assert _kinds(g._classify_divergence([], _act([]))) == ["action_shape"]
    assert _kinds(g._classify_divergence(_act([]), {"market": []})) == [
        "action_keys"]


# ---------------------------------------------------------------------------
# ③ 局级双判据矩阵（_adjudicate_game 纯函数直喂；步界阈值=648 同源）
# ---------------------------------------------------------------------------
_TH = 648
_D_LATE = [{"step": 662, "kind": "buy_seed_appear", "detail": "d"},
           {"step": 669, "kind": "sell_order_change", "detail": "d"}]


def test_adjudicate_allowed_late_nonnegative_passes():
    got = g._adjudicate_game(_D_LATE, 1010.0, 1000.0)
    assert got["game_pass"] is True and got["first_divergence"] is None
    assert got["n_violations"] == 0 and got["steps_boundary_ok"] is True
    assert got["result_face_ok"] is True and got["min_divergence_step"] == 662
    assert got["threshold"] == _TH


def test_adjudicate_boundary_breach_fails_and_localizes():
    early = {"step": 647, "kind": "buy_seed_disappear", "detail": "d"}
    got = g._adjudicate_game(_D_LATE + [early], 1000.0, 1000.0)
    assert got["game_pass"] is False and got["steps_boundary_ok"] is False
    assert got["n_violations"] == 0  # 形态面干净：红在步界
    assert got["first_divergence"] == early  # 定位=步界破缺的首个早差异


def test_adjudicate_violation_kind_fails_and_localizes():
    bad = {"step": 700, "kind": "market", "detail": "d"}
    got = g._adjudicate_game(_D_LATE + [bad], 1010.0, 1000.0)
    assert got["game_pass"] is False and got["n_violations"] == 1
    assert got["first_divergence"] == bad  # violation 定位（不受早于它的允许差异占位）


def test_adjudicate_result_face_negative_fails():
    got = g._adjudicate_game(_D_LATE, 990.0, 1000.0)
    assert got["game_pass"] is False and got["result_face_ok"] is False
    assert got["first_divergence"] is None  # 纯结果面破缺无步可指


def test_adjudicate_missing_finals_fail_closed():
    got = g._adjudicate_game(_D_LATE, None, 1000.0)
    assert got["game_pass"] is False and got["result_face_ok"] is False


def test_adjudicate_agent_exception_is_violation():
    exc = {"step": 710, "kind": "agent_exception", "detail": "boom"}
    got = g._adjudicate_game(_D_LATE + [exc], 1000.0, 1000.0)
    assert got["game_pass"] is False and got["first_divergence"] == exc


def test_adjudicate_empty_divergences_equal_finals_passes():
    got = g._adjudicate_game([], 1000.0, 1000.0)
    assert got["game_pass"] is True and got["min_divergence_step"] is None


# ---------------------------------------------------------------------------
# ④ 差异注入（小 strip + 假 callable；verbatim 走真 callable 对照）
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
    """把流里第一张 BUY_SEED 数量减 1（改量单=消失+出现分解）；返回步号。"""
    for t, action in enumerate(stream):
        for order in action.get("market") or []:
            if g._is_buy_seed(order):
                order[2] = int(order[2]) - 1
                return t
    raise AssertionError("注入夹具失配：前 8 步无 BUY_SEED 单")


@pytest.mark.parametrize("mutate,expected_kinds,expected_n_violations", [
    (_bump_first_sell_qty, ["sell_order_change"], 0),
    (_bump_hands, ["hands"], 1),
    (_reduce_first_buy_seed, ["buy_seed_disappear", "buy_seed_appear"], 0),
])
def test_injected_divergence_full_enumeration(tmp_path, mutate,
                                              expected_kinds,
                                              expected_n_violations):
    tiny, replay = _tiny_strip(tmp_path)
    me = g._my_seat(replay)
    fake, target_step = _mutated_stream_callable(replay, me, mutate)
    result = g.replay_action_diff(tiny, fake, VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    # 全量枚举：全部差异收齐（注入步恰为 expected_kinds，无其他差异步）
    at_target = [d for d in result["divergences"] if d["step"] == target_step]
    assert _kinds(at_target) == expected_kinds
    assert all(d["step"] == target_step for d in result["divergences"])
    assert result["n_divergences"] == len(result["divergences"])
    # 早期注入步（<648）= 步界破缺：局红，first_divergence 定位到注入步
    assert target_step < g._cxs_from()
    assert result["steps_boundary_ok"] is False
    assert result["game_pass"] is False
    fd = result["first_divergence"]
    assert set(fd) >= {"step", "kind", "detail"}
    assert fd["step"] == target_step
    assert fd["kind"] == expected_kinds[0]
    assert isinstance(fd["detail"], str) and fd["detail"]
    assert result["n_violations"] == expected_n_violations
    # 不再首异即停：比较覆盖全流（tiny strip 8 步=7 转移全比完）
    assert result["steps_compared"] == 7


def test_injected_dropped_tracks_disappear_entries_only(tmp_path):
    # 改量单分解后 dropped 只记消失份（subset 消费面语义不变）
    tiny, replay = _tiny_strip(tmp_path)
    me = g._my_seat(replay)
    fake, target_step = _mutated_stream_callable(replay, me,
                                                 _reduce_first_buy_seed)
    result = g.replay_action_diff(tiny, fake, VERBATIM_MAIN)
    assert "error" not in result, result.get("error")
    assert len(result["dropped"]) == 1
    assert result["dropped"][0]["step"] == target_step
    with gzip.open(_strip_path(EP_NO_DROP), "rt", encoding="utf-8") as fh:
        truth = _my_recorded_buy_seeds(json.load(fh), me)
    crop, qty = truth[target_step][0]
    assert result["dropped"][0] == {"step": target_step, "crop": crop,
                                    "qty": qty}


# ---------------------------------------------------------------------------
# ⑤ 异常路径 fail-closed
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
