# -*- coding: utf-8 -*-
"""test_gate_equivalence（门③ run 编排叶专属测试，2026-09-24 双判据口径）。

三组用例：
  ① 合成产物裁决矩阵：_aggregate_verdict 纯函数直喂——全真→PASS；基座反应
     局（允许形态差异 @≥648+终局非负）→ equiv 绿（新口径核心：旧严格口径
     下此类局红）；步界破缺局/结果面负局/violation 局 → 各自仅拉红 equiv；
     error 局 → equiv False 且 n_errors 计数；subset violation → passed
     False；cases 失败 → passed False。
  ② run 端到端接线（monkeypatch 三叶 + 合成语料目录）：升序发现、callable
     装载一次跨局复用、limit 子集、空语料 fail-closed、evidence 落盘结构
     （per_game 全产物逐局保留不截断含 divergences/game_pass、verdict 与
     返回值一致、equiv_detail 双判据台账）。
  ③ 真跑子集（3 局已知 game_pass 语料 symlink 子目录，2026-09-24 实测
     ~6s）：equiv/subset/cases 全绿、逐局 final_delta==dropped_value_est
     （纯减法资金面推论）、三局截断合计 $40。

全量 26 局只在实现验证跑一次（26×~2s+装载 ≈1min，真台账落包内
evidence/equivalence_evidence.json），不进单测——本文件用例一律把
evidence 写到 tmp_path，防覆写真台账。
"""

import json
import os

import pytest

import gate_equivalence_precision as g

_HERE = os.path.dirname(os.path.abspath(__file__))
_STRIP_DIR = g._STRIP_DIR_DEFAULT
L1_MAIN = os.path.join(_HERE, "main.py")
VERBATIM_MAIN = os.path.normpath(
    os.path.join(_HERE, "..", "orderbook_derivative", "main.py"))

# 步界阈值（与 layer_s_block._CXS_FROM 同源；矩阵用例的允许步取 ≥648）
_TH = g._cxs_from()

# per_game_summary 契约键（2026-09-24 双判据口径）
_SUMMARY_ROW_KEYS = {
    "episode", "seat", "error", "game_pass", "identical_mod_seed_drop",
    "n_divergences", "kind_counts", "n_violations", "first_divergence",
    "n_dropped", "dropped_value_est", "l1_final", "verbatim_final",
    "final_delta", "min_divergence_step", "steps_boundary_ok",
    "result_face_ok"}


# ---------------------------------------------------------------------------
# 合成夹具（replay_action_diff 产物契约形态 + (b)(c) 两叶结果形态）
# ---------------------------------------------------------------------------
def _ok_product(episode, seat=0, dropped=None):
    """纯截断局：divergences 全量=buy_seed_disappear，game_pass=True。"""
    dropped = dropped or []
    divergences = [{"step": e["step"], "kind": "buy_seed_disappear",
                    "detail": f'["BUY_SEED","{e["crop"]}",{e["qty"]}]'
                              "（verbatim 有 L1 无）",
                    "crop": e["crop"], "qty": e["qty"]}
                   for e in dropped]
    return {
        "episode": episode, "seat": seat,
        "game_pass": True, "divergences": divergences,
        "n_divergences": len(divergences), "n_violations": 0,
        "steps_boundary_ok": True, "result_face_ok": True,
        "min_divergence_step": (min(e["step"] for e in dropped)
                                if dropped else None),
        "identical_mod_seed_drop": True, "dropped": dropped,
        "first_divergence": None,
        "l1_final": 1000.0 + sum(e["qty"] * g.SEED_PRICE[e["crop"]]
                                 for e in dropped),
        "verbatim_final": 1000.0, "steps_compared": 719,
        "replay_path": f"/synthetic/episode-{episode}-strip.json.gz",
    }


def _reaction_product(episode, seat=0, *, min_step=None, final_delta=10.0):
    """基座反应局（2026-09-24 口径核心样本，实测形态：@662 回买+@669 少卖）。

    divergences=允许形态（buy_seed_disappear/appear/sell_order_change）
    且全部步 ≥648、终局 delta 非负 → game_pass=True；旧严格口径面
    identical_mod_seed_drop=False（(a') RED 诊断留档）。min_step/final_delta
    可调出 步界破缺/结果面负 两类反例。
    """
    steps = {"dis": 652, "app": 662, "sell": 669}
    if min_step is not None:  # 平移首个差异步（647=步界破缺反例）
        shift = min_step - steps["dis"]
        steps = {k: v + shift for k, v in steps.items()}
    divergences = [
        {"step": steps["dis"], "kind": "buy_seed_disappear",
         "detail": '["BUY_SEED","CARROT",3]（verbatim 有 L1 无）',
         "crop": "CARROT", "qty": 3},
        {"step": steps["app"], "kind": "buy_seed_appear",
         "detail": '["BUY_SEED","CARROT",8]（L1 有 verbatim 无，基座回买反应）',
         "crop": "CARROT", "qty": 8},
        {"step": steps["sell"], "kind": "sell_order_change",
         "detail": 'exp=[["SELL","EGG",4]] got=[]'},
    ]
    verdict = g._adjudicate_game(divergences, 1000.0 + final_delta, 1000.0)
    return {
        "episode": episode, "seat": seat,
        "game_pass": verdict["game_pass"], "divergences": divergences,
        "n_divergences": len(divergences),
        "n_violations": verdict["n_violations"],
        "steps_boundary_ok": verdict["steps_boundary_ok"],
        "result_face_ok": verdict["result_face_ok"],
        "min_divergence_step": verdict["min_divergence_step"],
        "identical_mod_seed_drop": False, "dropped": [
            {"step": steps["dis"], "crop": "CARROT", "qty": 3}],
        "first_divergence": verdict["first_divergence"],
        "l1_final": 1000.0 + final_delta, "verbatim_final": 1000.0,
        "steps_compared": 719,
        "replay_path": f"/synthetic/episode-{episode}-strip.json.gz",
    }


def _red_product(episode, seat=0):
    divergences = [{"step": 680, "kind": "market",
                    "detail": "synthetic RED"}]
    return {
        "episode": episode, "seat": seat,
        "game_pass": False, "divergences": divergences,
        "n_divergences": 1, "n_violations": 1,
        "steps_boundary_ok": True, "result_face_ok": True,
        "min_divergence_step": 680,
        "identical_mod_seed_drop": False, "dropped": [],
        "first_divergence": {"step": 680, "kind": "market",
                             "detail": "synthetic RED"},
        "l1_final": 990.0, "verbatim_final": 1000.0, "steps_compared": 681,
        "replay_path": f"/synthetic/episode-{episode}-strip.json.gz",
    }


def _subset_ok():
    return {"all_ok": True, "per_game": [], "per_crop": {}, "violations": [],
            "errors": [], "summary": {"n_games": 0, "n_violations": 0,
                                      "n_errors": 0}}


def _cases_ok():
    return {
        "c1_no_trunc_when_future_plant": {"pass": True, "evidence": "ok"},
        "c2_trunc_when_no_opportunity": {"pass": True, "evidence": "ok"},
        "c3_s671_boundary": {
            "truncate_side": {"pass": True, "evidence": "ok"},
            "keep_side": {"pass": True, "evidence": "ok"},
            "pass": True},
        "all_pass": True,
    }


# ---------------------------------------------------------------------------
# ① 合成产物裁决矩阵（纯函数直喂）
# ---------------------------------------------------------------------------
def test_matrix_all_green_passes():
    got = g._aggregate_verdict(
        [_ok_product(1), _ok_product(
            2, dropped=[{"step": 700, "crop": "WHEAT", "qty": 2}])],
        _subset_ok(), _cases_ok())
    assert got["equiv"] is True and got["subset"] is True
    assert got["cases"] is True and got["passed"] is True
    assert got["n_errors"] == 0 and len(got["per_game_summary"]) == 2
    assert [row["dropped_value_est"] for row in got["per_game_summary"]] == [0, 20]
    assert got["per_game_summary"][1]["final_delta"] == 20.0


def test_matrix_reaction_game_passes_equiv_under_new_criteria():
    # 2026-09-24 口径核心：基座回买/少卖反应局（旧严格口径红）→ equiv 绿
    got = g._aggregate_verdict([_ok_product(1), _reaction_product(2)],
                               _subset_ok(), _cases_ok())
    assert got["equiv"] is True and got["passed"] is True
    row = got["per_game_summary"][1]
    assert row["game_pass"] is True and row["n_violations"] == 0
    assert row["identical_mod_seed_drop"] is False  # (a') 严格面留档仍红
    assert row["n_divergences"] == 3 and row["kind_counts"] == {
        "buy_seed_disappear": 1, "buy_seed_appear": 1,
        "sell_order_change": 1}
    assert row["min_divergence_step"] == 652 and row["final_delta"] == 10.0


def test_matrix_boundary_breach_game_fails_equiv():
    bad = _reaction_product(2, min_step=647)  # 首差异步平移到 647（<648）
    assert bad["n_divergences"] == 3
    got = g._aggregate_verdict([_ok_product(1), bad], _subset_ok(), _cases_ok())
    assert got["equiv"] is False and got["passed"] is False
    row = got["per_game_summary"][1]
    assert row["game_pass"] is False and row["steps_boundary_ok"] is False
    assert row["n_violations"] == 0  # 形态面干净：红在步界
    assert row["first_divergence"]["step"] == 647  # 定位步界破缺


def test_matrix_negative_final_fails_equiv():
    bad = _reaction_product(2, final_delta=-0.5)  # 结果面负（反应面干净）
    got = g._aggregate_verdict([_ok_product(1), bad], _subset_ok(), _cases_ok())
    assert got["equiv"] is False and got["passed"] is False
    row = got["per_game_summary"][1]
    assert row["game_pass"] is False and row["result_face_ok"] is False
    assert row["final_delta"] == -0.5
    assert row["first_divergence"] is None  # 纯结果面破缺无步可指


def test_matrix_one_red_game_breaks_equiv_only():
    got = g._aggregate_verdict([_ok_product(1), _red_product(2)],
                               _subset_ok(), _cases_ok())
    assert got["equiv"] is False and got["passed"] is False
    assert got["subset"] is True and got["cases"] is True  # 面间不串红
    row = got["per_game_summary"][1]
    assert row["game_pass"] is False and row["n_violations"] == 1
    assert row["first_divergence"]["kind"] == "market"
    assert row["final_delta"] == -10.0
    assert got["n_errors"] == 0


def test_matrix_error_game_fail_closed():
    got = g._aggregate_verdict(
        [_ok_product(1), {"episode": 2, "error": "装载/语料失败: boom"}],
        _subset_ok(), _cases_ok())
    assert got["equiv"] is False and got["passed"] is False
    assert got["n_errors"] == 1  # 任一局 error → equiv=False 且 errors 计数
    row = got["per_game_summary"][1]
    assert "boom" in row["error"]
    assert row["game_pass"] is False
    assert row["final_delta"] is None and row["dropped_value_est"] == 0
    assert row["n_divergences"] == 0 and row["kind_counts"] == {}
    assert row["min_divergence_step"] is None


def test_matrix_subset_violation_fails_gate():
    bad = dict(_subset_ok(), all_ok=False,
               violations=[{"episode": 2, "crop": "CARROT",
                            "dropped": 9, "unplanted": 8}])
    got = g._aggregate_verdict([_ok_product(1), _ok_product(2)],
                               bad, _cases_ok())
    assert got["equiv"] is True and got["cases"] is True
    assert got["subset"] is False and got["passed"] is False


def test_matrix_cases_failure_fails_gate():
    bad = _cases_ok()
    bad["c2_trunc_when_no_opportunity"] = {"pass": False,
                                           "evidence": "fixture raised"}
    bad["all_pass"] = False
    got = g._aggregate_verdict([_ok_product(1)], _subset_ok(), bad)
    assert got["equiv"] is True and got["subset"] is True
    assert got["cases"] is False and got["passed"] is False


# ---------------------------------------------------------------------------
# ② run 端到端接线（monkeypatch 三叶；合成语料目录 = 空占位件，内容不走真链路）
# ---------------------------------------------------------------------------
def _fake_corpus(tmp_path, episodes):
    corpus = tmp_path / "eps"
    corpus.mkdir()
    for ep in episodes:
        (corpus / f"episode-{ep}-strip.json.gz").write_bytes(b"")
    return str(corpus)


def _patch_leaves(monkeypatch, products_by_path, subset=None, cases=None):
    calls = []

    def fake_diff(replay_path, l1, vb):
        calls.append((replay_path, l1, vb))
        return products_by_path[os.path.basename(replay_path)]

    monkeypatch.setattr(g, "replay_action_diff", fake_diff)
    monkeypatch.setattr(g, "precision_subset_check",
                        lambda ps: subset if subset is not None else _subset_ok())
    monkeypatch.setattr(g, "constructed_invariant_cases",
                        lambda: cases if cases is not None else _cases_ok())
    return calls


def test_run_wiring_and_evidence_structure(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400002, 112400001])  # 乱序落盘
    products = {
        "episode-112400001-strip.json.gz": _ok_product(112400001),
        "episode-112400002-strip.json.gz": _reaction_product(112400002),
    }
    calls = _patch_leaves(monkeypatch, products)
    ev = tmp_path / "evidence.json"
    f1 = lambda obs: {}
    f2 = lambda obs: {}
    got = g.run(corpus, f1, f2, evidence_path=str(ev))
    # 返回契约键
    assert set(got) >= {"equiv", "subset", "cases", "passed",
                        "per_game_summary", "evidence_path"}
    # 反应局在新口径下绿：equiv 全绿
    assert got["equiv"] is True and got["passed"] is True
    assert got["subset"] is True and got["cases"] is True
    # 局号数值升序发现；callable 装载一次跨局复用（同一对象喂每局）
    assert [os.path.basename(p) for p, _, _ in calls] == [
        "episode-112400001-strip.json.gz",
        "episode-112400002-strip.json.gz"]
    assert len({id(c) for _, c, _ in calls}) == 1
    assert all(c is f1 for _, c, _ in calls)
    assert all(v is f2 for _, _, v in calls)
    # evidence 落盘：per_game 全产物逐局保留（不截断）+ verdict 与返回一致
    assert got["evidence_path"] == str(ev) and os.path.isfile(ev)
    with open(ev, encoding="utf-8") as fh:
        evd = json.load(fh)
    assert evd["per_game"] == [products[
        "episode-112400001-strip.json.gz"], products[
        "episode-112400002-strip.json.gz"]]
    assert evd["verdict"] == {"equiv": True, "subset": True,
                              "cases": True, "passed": True}
    assert evd["inputs"]["n_replays"] == 2
    assert evd["subset"]["all_ok"] is True and evd["cases"]["all_pass"] is True
    assert evd["equiv_detail"]["n_games"] == 2
    assert evd["equiv_detail"]["n_game_pass"] == 2
    assert evd["equiv_detail"]["n_divergent_games"] == 1  # 反应局有差异步
    assert evd["equiv_detail"]["n_violation_games"] == 0
    assert evd["equiv_detail"]["n_errors"] == 0
    # 双判据台账：允许形态/步界（同源阈值）/结果面口径登记
    crit = evd["equiv_detail"]["criteria"]
    assert crit["allowed_kinds"] == list(g.ALLOWED_DIVERGENCE_KINDS)
    assert crit["step_boundary"] == {"threshold": g._cxs_from(),
                                     "source": "layer_s_block._CXS_FROM"}
    assert crit["result_face"] == "l1_final >= verbatim_final per game"
    assert set(got["per_game_summary"][0]) == _SUMMARY_ROW_KEYS


def test_run_limit_takes_first_n_games(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002, 112400003])
    products = {f"episode-{ep}-strip.json.gz": _ok_product(ep)
                for ep in (112400001, 112400002, 112400003)}
    calls = _patch_leaves(monkeypatch, products)
    got = g.run(corpus, lambda o: {}, lambda o: {}, limit=1,
                evidence_path=str(tmp_path / "ev.json"))
    assert len(calls) == 1  # 子集参数化：limit 截前 N 局
    assert got["equiv"] is True and got["passed"] is True
    with open(got["evidence_path"], encoding="utf-8") as fh:
        evd = json.load(fh)
    assert evd["inputs"]["limit"] == 1 and evd["inputs"]["n_replays"] == 1


def test_run_empty_corpus_fail_closed(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    got = g.run(str(empty), lambda o: {}, lambda o: {},
                evidence_path=str(tmp_path / "ev.json"))
    assert got["equiv"] is False and got["passed"] is False
    assert got["n_errors"] == 1  # 语料空 → 单条全局面 error（防空转绿灯）
    assert got["subset"] is False  # 真 precision_subset_check 同步拉红
    assert "语料发现失败" in got["per_game_summary"][0]["error"]


def test_run_bad_dir_fail_closed(tmp_path):
    got = g.run(str(tmp_path / "no-such-dir"), lambda o: {}, lambda o: {},
                evidence_path=str(tmp_path / "ev.json"))
    assert got["equiv"] is False and got["passed"] is False
    assert got["n_errors"] == 1
    assert "NotADirectoryError" in got["per_game_summary"][0]["error"]


def test_run_load_failure_error_per_game(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    monkeypatch.setattr(
        g, "replay_action_diff",
        lambda *a: pytest.fail("装载失败不应逐局进真重演"))
    monkeypatch.setattr(g, "precision_subset_check", lambda ps: _subset_ok())
    monkeypatch.setattr(g, "constructed_invariant_cases", _cases_ok)
    got = g.run(corpus, "/nonexistent/l1.py", "/nonexistent/vb.py",
                evidence_path=str(tmp_path / "ev.json"))
    assert got["equiv"] is False and got["n_errors"] == 2  # 逐局记 error
    assert all("装载/语料失败" in row["error"]
               for row in got["per_game_summary"])
    assert [row["episode"] for row in got["per_game_summary"]] == [
        112400001, 112400002]  # error 局号从文件名回填


def test_run_subset_interface_untouched(tmp_path, monkeypatch):
    """兼容性：precision_subset_check 原样消费新产物面（dropped/episode/
    seat/replay_path/error），本测试喂真 precision_subset_check 验证键兼容。"""
    real_subset = g.precision_subset_check  # 留真件（_patch_leaves 会换假件）
    corpus = _fake_corpus(tmp_path, [112400001])
    products = {"episode-112400001-strip.json.gz": _reaction_product(112400001)}
    calls = _patch_leaves(monkeypatch, products)
    got = g.run(corpus, lambda o: {}, lambda o: {},
                evidence_path=str(tmp_path / "ev.json"))
    assert len(calls) == 1
    # 真 precision_subset_check 吃新产物：dropped=CARROT×3 消费面原样，
    # 缺语料文件 → 单局 error（fail-closed），不因产物新增
    # divergences/game_pass 键而崩（键兼容=可增不可删改）。
    real = real_subset([products["episode-112400001-strip.json.gz"]])
    assert real["summary"]["n_errors"] == 1
    assert real["summary"]["n_games"] == 1
    assert "FileNotFoundError" in real["errors"][0]["error"]
    assert got["subset"] is True  # run 用假 subset 件；真件键兼容已验


# ---------------------------------------------------------------------------
# ③ 真跑子集（3 局已知 game_pass；2026-09-24 实测 ~6s）
# ---------------------------------------------------------------------------
_KNOWN_IDENTICAL = ("112429867", "112433355", "112446302")


@pytest.mark.skipif(not os.path.isdir(_STRIP_DIR),
                    reason=f"strip corpus not present: {_STRIP_DIR}")
def test_run_real_subset_three_known_identical(tmp_path):
    # ① test_replay_action_diff 同挑选依据：112429867 无截断、112433355 截
    # WHEAT×1($10)、112446302 截 WHEAT×3($30)，三局全 game_pass。
    sub = tmp_path / "replays-subset"
    sub.mkdir()
    for ep in _KNOWN_IDENTICAL:
        os.symlink(os.path.join(_STRIP_DIR, f"episode-{ep}-strip.json.gz"),
                   sub / f"episode-{ep}-strip.json.gz")
    got = g.run(str(sub), L1_MAIN, VERBATIM_MAIN,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["equiv"] is True and got["n_errors"] == 0
    assert got["subset"] is True and got["cases"] is True
    assert got["passed"] is True  # 三局小子集：三面全绿
    assert len(got["per_game_summary"]) == 3
    # 纯减法资金面推论 + 三局截断合计 $40（WHEAT×4）
    for row in got["per_game_summary"]:
        assert row["game_pass"] is True
        assert row["identical_mod_seed_drop"] is True
        assert row["first_divergence"] is None
        assert row["steps_boundary_ok"] is True
        assert round(row["final_delta"], 6) == row["dropped_value_est"]
    assert sum(r["dropped_value_est"] for r in got["per_game_summary"]) == 40
    # evidence per_game 全产物在（契约键齐全，不截断）
    with open(got["evidence_path"], encoding="utf-8") as fh:
        evd = json.load(fh)
    assert len(evd["per_game"]) == 3
    for product in evd["per_game"]:
        assert set(product) >= {
            "episode", "seat", "game_pass", "divergences",
            "identical_mod_seed_drop", "dropped", "first_divergence",
            "l1_final", "verbatim_final", "steps_compared", "replay_path"}
    assert evd["equiv_detail"]["n_game_pass"] == 3
    assert evd["subset"]["summary"]["n_games"] == 3
    assert evd["subset"]["summary"]["total_dropped_value_est"] == 40
