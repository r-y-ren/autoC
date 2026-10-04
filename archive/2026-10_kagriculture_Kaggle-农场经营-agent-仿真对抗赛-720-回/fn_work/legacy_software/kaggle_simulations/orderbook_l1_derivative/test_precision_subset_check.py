# -*- coding: utf-8 -*-
"""test_precision_subset_check（继承 R10 验收③(b) 子集组）：门③(b) 叶裁决。

合成夹具（不依赖真跑）：按 replay_action_diff 产物契约构造 replay_products，
原局终局态用同字段路径的最小 strip 件（tmp_path 落地，走真提取链路）。
真数据冒烟：语料终局态直读断言 _strip_unplanted_seeds 提取正确（上游
replay_action_diff 仍是桩，不做端到端重演）。
"""

import json
import os

import pytest

import gate_equivalence_precision as gep

_CROPS = list(gep.SEED_PRICE)  # WHEAT/CARROT/TOMATO/STRAWBERRY/MELON
_STRIP_DIR = os.path.normpath(gep._STRIP_DIR_DEFAULT)


# ---- 夹具：最小 strip 件（与语料同字段路径）+ replay_action_diff 产物 ----
def _write_strip(path, my_seat, seeds):
    """写最小 strip 形态件：steps[-1] seat0 槽共享观测含双席 private（INDEX.md
    strip 形态），final.private 同值（终局真值双记录）。返回路径字符串。"""
    teams = ["renyxin", "opp"] if my_seat == 0 else ["opp", "renyxin"]
    zero = {c: 0 for c in _CROPS}
    privates = []
    for s in (0, 1):
        privates.append({
            "inventories": [{}],
            "seeds": dict(seeds) if s == my_seat else dict(zero),
            "shed": {},
        })
    replay = {
        "info": {"TeamNames": list(teams)},
        "teams": list(teams),
        # 真实 strip 形态：终步 = [seat0{action+共享观测}, seat1{action}]——
        # 双席是**同一步的两个槽位**，共享观测在 seat0 槽。
        "steps": [
            [{"action": {}, "observation": {"step": 0, "player": 0}}],
            [{"action": {}, "observation": {
                "step": 719, "day": 30, "hour": 23, "player": 0,
                "private": privates}}, {"action": {}}],
        ],
        "final": {"private": privates},
    }
    with open(path, "w") as fh:
        json.dump(replay, fh)
    return str(path)


def _product(episode, seat, dropped, replay_path):
    """replay_action_diff 产物形态（契约键全带上；dropped 为逐单列表）。"""
    return {
        "episode": episode,
        "seat": seat,
        "identical_mod_seed_drop": True,
        "dropped": [{"step": 700, "crop": crop, "qty": qty}
                    for crop, qty in dropped],
        "l1_final": {},
        "verbatim_final": {},
        "replay_path": replay_path,
    }


def _run(tmp_path, games, episode_seq):
    """games=[(my_seat, unplanted_seeds, dropped_list)]；返回 (got, paths)。"""
    products = []
    for i, (seat, unplanted, dropped) in enumerate(games):
        path = _write_strip(tmp_path / f"strip-{i}.json", seat, unplanted)
        products.append(_product(episode_seq[i], seat, dropped, path))
    return gep.precision_subset_check(products), products


# ---- ① 子集成立 → ok ----
def test_subset_holds_ok(tmp_path):
    got, _ = _run(tmp_path, [(1, {"CARROT": 8, "WHEAT": 4}, [])], [1001])
    assert got["all_ok"] is True
    assert got["violations"] == [] and got["errors"] == []
    game = got["per_game"][0]
    assert game["episode"] == 1001 and game["seat"] == 1 and game["ok"] is True
    assert game["crops"]["CARROT"] == {"dropped": 0, "unplanted": 8, "ok": True}
    assert game["crops"]["WHEAT"] == {"dropped": 0, "unplanted": 4, "ok": True}
    assert game["mode_a"] is False  # 剩种 $200 → 模式乙


# ---- ② 一品项 dropped > unplanted → violation ----
def test_violation_when_dropped_exceeds_unplanted(tmp_path):
    got, _ = _run(
        tmp_path,
        [(0, {"CARROT": 8, "WHEAT": 4}, [("CARROT", 5), ("CARROT", 4)])],
        [1002])  # 同品项两张单汇总 9 > 8（多删一颗=误杀）
    assert got["all_ok"] is False
    assert got["errors"] == []
    assert got["violations"] == [
        {"episode": 1002, "crop": "CARROT", "dropped": 9, "unplanted": 8}]
    game = got["per_game"][0]
    assert game["ok"] is False
    assert game["crops"]["CARROT"] == {"dropped": 9, "unplanted": 8, "ok": False}
    assert game["crops"]["WHEAT"]["ok"] is True  # 未殃及无菜品项
    assert got["per_crop"]["CARROT"]["ok"] is False


# ---- ③ 模式甲局（unplanted≈0，dropped=0）→ ok 且 mode_a 旗标正确 ----
def test_mode_a_game_near_zero(tmp_path):
    got, _ = _run(tmp_path, [
        # 模式甲：剩种 WHEAT×2=$20（≤$30 带）、零截断
        (1, {"WHEAT": 2}, []),
        # 模式乙对照：截 CARROT×8=$160（子集成立，不参与模式甲旗标）
        (0, {"CARROT": 8, "WHEAT": 4}, [("CARROT", 8)]),
    ], [1003, 1004])
    assert got["all_ok"] is True and got["violations"] == []
    mode_a_game, mode_b_game = got["per_game"]
    assert mode_a_game["mode_a"] is True and mode_a_game["dropped_value"] == 0
    assert mode_b_game["mode_a"] is False and mode_b_game["dropped_value"] == 160
    summary = got["summary"]
    assert summary["n_mode_a"] == 1 and summary["mode_a_episodes"] == [1003]
    assert summary["mode_a_games_near_zero"] is True

    # 带内容差钉死：模式甲局（剩种 $30 带边）截 1 颗麦（$10 ≤ 带）→ 旗标仍绿
    got_band, _ = _run(tmp_path, [(1, {"WHEAT": 3}, [("WHEAT", 1)])], [1005])
    assert got_band["all_ok"] is True
    assert got_band["summary"]["mode_a_games_near_zero"] is True

    # 反面（金丝雀）：模式甲局（剩种 WHEAT×2=$20 在带内）截 4 颗=$40 超带
    # ——子集蕴含下超带必伴 violation（dropped 4 > unplanted 2），旗标随判据
    # 一同翻红
    got_over, _ = _run(tmp_path, [(1, {"WHEAT": 2}, [("WHEAT", 4)])], [1006])
    assert got_over["all_ok"] is False
    assert got_over["summary"]["mode_a_games_near_zero"] is False
    assert got_over["violations"] == [
        {"episode": 1006, "crop": "WHEAT", "dropped": 4, "unplanted": 2}]


# ---- ④ error 局 → errors 非空、all_ok=False（fail-closed）----
def test_error_game_fail_closed(tmp_path):
    ok_path = _write_strip(tmp_path / "strip-ok.json", 0, {"CARROT": 8})
    products = [
        _product(2001, 0, [], ok_path),
        {"episode": 2002, "error": "divergence at step 5 (non-BUY_SEED)"},
        # 终局态取不到（episode 号拼不出现存 strip 件）→ 单局异常也归 errors
        {"episode": 29999999, "seat": 1, "dropped": []},
    ]
    got = gep.precision_subset_check(products)
    assert got["all_ok"] is False
    assert got["violations"] == []  # error 局不进 violations
    assert [e["episode"] for e in got["errors"]] == [2002, 29999999]
    assert "divergence at step 5" in got["errors"][0]["error"]
    assert "FileNotFoundError" in got["errors"][1]["error"]
    assert "episode" in got["per_game"][1] and "error" in got["per_game"][1]
    # 空输入=error（防空转绿灯）
    empty = gep.precision_subset_check([])
    assert empty["all_ok"] is False and len(empty["errors"]) == 1


# ---- ⑤ 品项汇总与价值估算正确 ----
def test_per_crop_aggregation_and_value_est(tmp_path):
    got, _ = _run(tmp_path, [
        (1, {"CARROT": 8, "WHEAT": 4}, [("CARROT", 2), ("WHEAT", 1)]),   # $50
        (0, {c: 0 for c in _CROPS}, []),                                  # $0 模式甲
        (1, {"CARROT": 8, "WHEAT": 5, "TOMATO": 2},
         [("CARROT", 3), ("CARROT", 3), ("TOMATO", 1)]),                  # $170
    ], [3001, 3002, 3003])
    assert got["all_ok"] is True
    assert got["per_crop"] == {
        "WHEAT": {"dropped": 1, "unplanted": 9, "ok": True},
        "CARROT": {"dropped": 8, "unplanted": 16, "ok": True},
        "TOMATO": {"dropped": 1, "unplanted": 2, "ok": True},
        "STRAWBERRY": {"dropped": 0, "unplanted": 0, "ok": True},
        "MELON": {"dropped": 0, "unplanted": 0, "ok": True},
    }
    # SEED 票价估值：2×20+1×10 + 0 + (3+3)×20+1×50 = 220
    assert got["summary"]["total_dropped_value_est"] == 220
    assert [g["unplanted_value"] for g in got["per_game"]] == [200, 0, 310]
    assert got["summary"]["n_games"] == 3 and got["summary"]["n_mode_a"] == 1


# ---- 真数据冒烟：语料终局态直读断言提取正确（只测 _strip_unplanted_seeds）----
@pytest.mark.skipif(not os.path.isdir(_STRIP_DIR),
                    reason=f"strip corpus not present: {_STRIP_DIR}")
class TestSmokeRealCorpusExtraction:
    def _strip(self, ep):
        return os.path.join(_STRIP_DIR, f"episode-{ep}-strip.json.gz")

    def test_mode_a_game_all_zero(self):
        # INDEX.md：112429867 我席=1；实测终局我方五品项全 0（模式甲 $0）
        got = gep._strip_unplanted_seeds(self._strip(112429867))
        assert got["seat"] == 1
        assert got["seeds"] == {c: 0 for c in _CROPS}

    def test_mode_b_game_audit_shape(self):
        # 审计模式乙形态：CARROT×8+WHEAT×4=$200（112431033 我席=0）
        got = gep._strip_unplanted_seeds(self._strip(112431033))
        assert got["seat"] == 0
        assert got["seeds"]["CARROT"] == 8 and got["seeds"]["WHEAT"] == 4
        assert sum(gep.SEED_PRICE[c] * n for c, n in got["seeds"].items()) == 200

    def test_seat_given_crosschecks_and_band_edge(self):
        # 给定 seat 与 teams 交叉；112446302 我席=1、剩 WHEAT×3=$30（带边）
        got = gep._strip_unplanted_seeds(self._strip(112446302), seat=1)
        assert got["seeds"]["WHEAT"] == 3 and got["seeds"]["CARROT"] == 0
        with pytest.raises(ValueError):  # 席位交叉失败 → fail-closed
            gep._strip_unplanted_seeds(self._strip(112446302), seat=0)

    def test_full_corpus_mode_split_matches_audit(self):
        # 全 26 局：模式甲（剩种 ≤$30）恰 10 局、模式乙 CARROT×8 级 16 局
        # ——提取面与审计基线（analyses/09 + 2026-09-23 解剖）整体对账。
        n_mode_a = 0
        for name in sorted(os.listdir(_STRIP_DIR)):
            if not name.endswith("-strip.json.gz"):
                continue
            got = gep._strip_unplanted_seeds(os.path.join(_STRIP_DIR, name))
            value = sum(gep.SEED_PRICE[c] * n for c, n in got["seeds"].items())
            if value <= gep.MODE_A_VALUE_BAND:
                n_mode_a += 1
            else:  # 模式乙形态：CARROT×8 + WHEAT×4-10（审计"WHEAT×4-5 级"
                # 为约数，语料实测 15 局 4-5 颗 + 1 局 10 颗=$260，16 局合计
                # ≈$3,345 对账 ~$3,400）
                assert got["seeds"]["CARROT"] == 8
                assert 4 <= got["seeds"]["WHEAT"] <= 10
                assert got["seeds"]["TOMATO"] == 0
        assert n_mode_a == 10

    def test_final_vs_shared_mismatch_fail_closed(self, tmp_path):
        # 终局真值双记录不一致=语料损坏 → ValueError（fail-closed）
        path = _write_strip(tmp_path / "strip-bad.json", 0, {"WHEAT": 2})
        with open(path) as fh:
            replay = json.load(fh)
        replay["final"]["private"][0]["seeds"]["WHEAT"] = 7
        with open(path, "w") as fh:
            json.dump(replay, fh)
        with pytest.raises(ValueError):
            gep._strip_unplanted_seeds(path)
