"""test_gate_equiv_v2（R11 门③）：三面裁决矩阵与 run 接线。

不真跑重演（26 局全量重演留给 verify 编排正式跑批；真跑预算让渡门① 4 局）：
① 裁决矩阵——_aggregate_verdict 纯函数直喂合成双路产物：全过→绿；
   appear 总数 3（>2）→形态面红；死种合计 >$900→结果面红；v2 终局 < L1
   一局→结果面红；violation 形态/步界破缺→形态面红；error 局→两面俱红
   （fail-closed）；subset/cases 红→各自拉红门。② run 接线——monkeypatch
   L1 叶（replay_action_diff/precision_subset_check）+ 本门死种提取与构造
   用例假件 + 合成语料目录：逐局两路重演（cand=v2 与 cand=L1、control 均
   verbatim）、死种仅在 (a) 路成形局提取、limit 子集、空语料 fail-closed、
   evidence 协议 2.0 结构（per_game 双路产物+四面指标）。③ constructed_
   cases_v2 真跑（无引擎，夹具直驱）：五件全过。"""

import json
import os

import pytest

import gate_equivalence_v2 as g  # noqa: E402  (自带 L1_DIR/HERE sys.path 自举)

# 合成哨兵（三 callable 装载一次跨局复用的身份断言用）。
_V2 = lambda obs: {}   # noqa: E731
_L1 = lambda obs: {}   # noqa: E731
_VB = lambda obs: {}   # noqa: E731

_SUMMARY_ROW_KEYS = {
    "episode", "seat", "error", "form_ok", "n_violations",
    "steps_boundary_ok", "min_divergence_step", "kind_counts", "appear_count",
    "n_dropped", "dropped_value_est", "final_face_ok", "v2_final",
    "l1_final", "verbatim_final", "final_delta", "dead_seeds_value",
    "dead_seeds"}


# ---------------------------------------------------------------------------
# 合成夹具（run 双路产物契约形态）
# ---------------------------------------------------------------------------
def _form_product(episode, seat=0, *, v2_final=1000.0, verbatim_final=980.0,
                  dropped=None, appear=None, extra_divs=None):
    """(a) 路产物（cand=v2/control=verbatim）：divergences=删除+回买（步≥648）。"""
    dropped = dropped or []
    divergences = [{"step": e["step"], "kind": "buy_seed_disappear",
                    "detail": f'["BUY_SEED","{e["crop"]}",{e["qty"]}]"'
                              "（verbatim 有 v2 无）",
                    "crop": e["crop"], "qty": e["qty"]} for e in dropped]
    for d in (appear or []):
        divergences.append({"step": d["step"], "kind": "buy_seed_appear",
                            "detail": f'["BUY_SEED","{d["crop"]}",{d["qty"]}]"'
                                      "（v2 有 verbatim 无，回买面）",
                            "crop": d["crop"], "qty": d["qty"]})
    divergences.extend(extra_divs or [])
    return {"episode": episode, "seat": seat, "game_pass": True,
            "divergences": divergences, "n_divergences": len(divergences),
            "n_violations": 0, "dropped": dropped, "first_divergence": None,
            "l1_final": v2_final, "verbatim_final": verbatim_final,
            "steps_compared": 719,
            "replay_path": f"/synthetic/episode-{episode}-strip.json.gz"}


def _result_product(episode, seat=0, *, l1_final=990.0, verbatim_final=980.0):
    """(b) 路产物（cand=L1/control=verbatim）：裁决面只消费 l1_final。"""
    return {"episode": episode, "seat": seat, "game_pass": True,
            "divergences": [], "n_divergences": 0, "n_violations": 0,
            "dropped": [], "first_divergence": None,
            "l1_final": l1_final, "verbatim_final": verbatim_final,
            "steps_compared": 719,
            "replay_path": f"/synthetic/episode-{episode}-strip.json.gz"}


def _record(episode, *, v2_final=1000.0, l1_final=990.0,
            verbatim_final=980.0, dropped=None, appear=None,
            extra_divs=None, dead_value=0, seat=0):
    return {"episode": episode, "seat": seat, "error": None,
            "form": _form_product(episode, seat, v2_final=v2_final,
                                  verbatim_final=verbatim_final,
                                  dropped=dropped, appear=appear,
                                  extra_divs=extra_divs),
            "result": _result_product(episode, seat, l1_final=l1_final,
                                      verbatim_final=verbatim_final),
            "dead_seeds": {"seeds": {"CARROT": max(dead_value // 20, 0)},
                           "value": dead_value}}


def _subset_ok():
    return {"all_ok": True, "per_game": [], "per_crop": {}, "violations": [],
            "errors": [], "summary": {"n_games": 0, "n_violations": 0,
                                      "n_errors": 0}}


def _cases_ok():
    return {name: {"pass": True, "evidence": "ok"} for name in (
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c4_net_covered_buyback_deleted",
        "c5_net_short_true_future_plant_kept")}


def _cases_ok_v2():
    cases = _cases_ok()
    cases["c3_s671_boundary"] = {
        "truncate_side": {"pass": True, "evidence": "ok"},
        "keep_side": {"pass": True, "evidence": "ok"}, "pass": True}
    cases["all_pass"] = True
    return cases


# ---------------------------------------------------------------------------
# ① 裁决矩阵（纯函数直喂）
# ---------------------------------------------------------------------------
def test_matrix_all_green_passes():
    records = [_record(1), _record(
        2, dropped=[{"step": 700, "crop": "WHEAT", "qty": 2}], dead_value=40)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v2())
    assert got["passed"] is True
    assert got["form_face"]["ok"] is True and got["result_face"]["ok"] is True
    assert got["form_face"]["appear_total"] == 0
    assert got["result_face"]["dead_seeds_total_value"] == 40
    assert got["n_errors"] == 0
    row = got["per_game_summary"][1]
    assert row["dropped_value_est"] == 20        # WHEAT×2 × $10
    assert row["final_delta"] == pytest.approx(10.0)   # v2 1000 − L1 990
    assert row["form_ok"] is True and row["final_face_ok"] is True
    assert set(row) == _SUMMARY_ROW_KEYS


def test_matrix_appear_total_over_cap_fails_form_face():
    # R11 硬指标：26 局 buy_seed_appear 总数 ≤2（计数=回买单数，逐差异记录一
    # 单）——第 1 局 2 单+第 2 局 1 单=3 → 形态面红（结果面不串红）。
    records = [
        _record(1, appear=[{"step": 660, "crop": "CARROT", "qty": 1},
                           {"step": 661, "crop": "WHEAT", "qty": 1}]),
        _record(2, appear=[{"step": 662, "crop": "WHEAT", "qty": 1}])]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v2())
    assert got["form_face"]["appear_total"] == 3
    assert got["form_face"]["ok"] is False
    assert got["passed"] is False
    assert got["result_face"]["ok"] is True      # 面间不串红
    assert [row["appear_count"] for row in got["per_game_summary"]] == [2, 1]


def test_matrix_dead_seeds_over_cap_fails_result_face():
    # R11 硬指标：终局死种合计 ≤$900——$700+$210=$910 → 结果面红（形态面绿）。
    records = [_record(1, dead_value=700), _record(2, dead_value=210)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v2())
    assert got["result_face"]["dead_seeds_total_value"] == 910
    assert got["result_face"]["dead_seeds_cap"] == g.DEAD_SEEDS_VALUE_CAP
    assert got["result_face"]["ok"] is False and got["passed"] is False
    assert got["form_face"]["ok"] is True


def test_matrix_v2_below_l1_one_game_fails_result_face():
    # R11 硬指标：逐局 v2 终局资金 ≥ L1——单局破缺即红，定位行 final_delta<0。
    records = [_record(1), _record(2, v2_final=989.5, l1_final=990.0)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v2())
    assert got["result_face"]["ok"] is False
    assert got["result_face"]["n_final_face_games_red"] == 1
    row = got["per_game_summary"][1]
    assert row["final_face_ok"] is False
    assert row["final_delta"] == pytest.approx(-0.5)
    assert got["form_face"]["ok"] is True        # 结果面破缺不拉红形态面
    assert got["passed"] is False


def test_matrix_violation_and_boundary_fail_form_face():
    violation = _record(1, extra_divs=[{"step": 680, "kind": "market",
                                        "detail": "synthetic RED"}])
    got = g._aggregate_verdict([violation], _subset_ok(), _cases_ok_v2())
    assert got["form_face"]["ok"] is False
    assert got["form_face"]["n_violation_games"] == 1
    # 步界破缺（647 < 648）：形态合法但早差异 → 形态面红。
    breach = _record(2, appear=[{"step": 647, "crop": "CARROT", "qty": 1}])
    got = g._aggregate_verdict([breach], _subset_ok(), _cases_ok_v2())
    assert got["form_face"]["ok"] is False
    assert got["form_face"]["n_boundary_breach_games"] == 1
    row = got["per_game_summary"][0]
    assert row["n_violations"] == 0 and row["steps_boundary_ok"] is False


def test_matrix_error_game_fail_closed_both_faces():
    records = [_record(1),
               {"episode": 2, "seat": None, "error": None, "form": None,
                "result": None, "dead_seeds": None},
               _record(3, dead_value=10)]
    records[1]["form"] = {"error": "装载/语料失败: boom"}
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v2())
    assert got["n_errors"] == 1                  # 任一路 error → 该局红
    assert got["form_face"]["ok"] is False and got["result_face"]["ok"] is False
    assert got["passed"] is False
    row = got["per_game_summary"][1]
    assert "boom" in row["error"]
    assert row["form_ok"] is False and row["final_face_ok"] is None
    assert row["v2_final"] is None and row["dead_seeds_value"] is None


def test_matrix_subset_or_cases_red_fail_gate():
    records = [_record(1)]
    bad_subset = dict(_subset_ok(), all_ok=False)
    got = g._aggregate_verdict(records, bad_subset, _cases_ok_v2())
    assert got["form_face"]["ok"] and got["result_face"]["ok"]
    assert got["subset"] is False and got["passed"] is False
    bad_cases = _cases_ok_v2()
    bad_cases["c4_net_covered_buyback_deleted"] = {"pass": False,
                                                   "evidence": "fixture raised"}
    bad_cases["all_pass"] = False
    got = g._aggregate_verdict(records, _subset_ok(), bad_cases)
    assert got["cases"] is False and got["passed"] is False


def test_matrix_empty_records_fail_closed():
    got = g._aggregate_verdict([], _subset_ok(), _cases_ok_v2())
    assert got["passed"] is False                # 非空记录集是绿灯前置
    assert got["form_face"]["ok"] is False and got["result_face"]["ok"] is False


# ---------------------------------------------------------------------------
# ② run 接线（monkeypatch L1 叶 + 本门死种/构造用例假件；合成语料目录）
# ---------------------------------------------------------------------------
def _fake_corpus(tmp_path, episodes):
    corpus = tmp_path / "eps"
    corpus.mkdir()
    for ep in episodes:
        (corpus / f"episode-{ep}-strip.json.gz").write_bytes(b"")
    return str(corpus)


def _patch_leaves(monkeypatch, form_by_ep, result_by_ep, dead_by_ep=None,
                  subset=None, diff_calls=None, dead_calls=None):
    dead_by_ep = dead_by_ep if dead_by_ep is not None else {}
    dead_calls = dead_calls if dead_calls is not None else []

    def fake_diff(replay_path, cand, control):
        ep = g._l1._episode_from_path(replay_path)
        if diff_calls is not None:
            diff_calls.append((ep, cand, control,
                               os.path.basename(replay_path)))
        return (form_by_ep[ep] if cand is _V2 else result_by_ep[ep])

    def fake_dead(replay_path, v2_fn):
        ep = g._l1._episode_from_path(replay_path)
        dead_calls.append((ep, v2_fn))
        outcome = dead_by_ep.get(ep)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome if outcome is not None else {"seeds": {},
                                                    "value": 0}

    monkeypatch.setattr(g._l1, "replay_action_diff", fake_diff)
    monkeypatch.setattr(g._l1, "precision_subset_check",
                        lambda ps: subset if subset is not None
                        else _subset_ok())
    monkeypatch.setattr(g, "constructed_cases_v2", _cases_ok_v2)
    monkeypatch.setattr(g, "_v2_dead_seeds", fake_dead)


def test_run_wiring_two_routes_and_evidence(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400002, 112400001])    # 乱序落盘
    form = {112400001: _form_product(112400001, v2_final=1005.0),
            112400002: _form_product(
                112400002, v2_final=1005.0,
                dropped=[{"step": 700, "crop": "CARROT", "qty": 2}])}
    result = {112400001: _result_product(112400001, l1_final=1000.0),
              112400002: _result_product(112400002, l1_final=998.0)}
    diff_calls, dead_calls = [], []
    _patch_leaves(monkeypatch, form, result,
                  dead_by_ep={112400001: {"seeds": {}, "value": 0},
                              112400002: {"seeds": {"CARROT": 2}, "value": 40}},
                  diff_calls=diff_calls, dead_calls=dead_calls)
    ev = tmp_path / "evidence.json"
    got = g.run(corpus, _V2, _L1, _VB, evidence_path=str(ev))

    assert got["passed"] is True
    assert got["form_face"]["ok"] and got["result_face"]["ok"]
    assert got["subset"] is True and got["cases"] is True
    # 逐局两路重演：局号升序 × (cand=v2 / cand=L1)，control 恒 verbatim，
    # 三 callable 装载一次跨局复用（同一对象喂每局）。
    assert [(c[0], c[1], c[2]) for c in diff_calls] == [
        (112400001, _V2, _VB), (112400001, _L1, _VB),
        (112400002, _V2, _VB), (112400002, _L1, _VB)]
    assert len({id(c[1]) for c in diff_calls if c[1] is not _VB}) == 2
    # 死种仅在 (a) 路成形局提取（v2_fn 身份）
    assert dead_calls == [(112400001, _V2), (112400002, _V2)]
    assert got["result_face"]["dead_seeds_total_value"] == 40
    row2 = got["per_game_summary"][1]
    assert row2["dropped_value_est"] == 40        # CARROT×2 × $20
    assert row2["final_delta"] == pytest.approx(1005.0 - 998.0)
    # 返回契约键
    assert set(got) >= {"passed", "form_face", "result_face", "subset",
                        "cases", "per_game_summary", "n_errors",
                        "evidence_path"}
    assert got["n_errors"] == 0

    # evidence 协议 2.0：per_game 双路产物 + 四面指标 + 输入登记
    assert got["evidence_path"] == str(ev) and os.path.isfile(ev)
    with open(ev, encoding="utf-8") as fh:
        evd = json.load(fh)
    assert evd["protocol"] == "orderbook-l11-equivalence/2.0"
    assert evd["inputs"]["n_replays"] == 2
    assert evd["inputs"]["v2_main"] == "<callable>"
    assert [r["episode"] for r in evd["per_game"]] == [112400001, 112400002]
    assert evd["per_game"][0]["form"] == form[112400001]
    assert evd["per_game"][1]["result"] == result[112400002]
    assert evd["per_game"][1]["dead_seeds"] == {"seeds": {"CARROT": 2},
                                                "value": 40}
    assert evd["verdict"] == {"form_face": True, "result_face": True,
                              "subset": True, "cases": True, "passed": True}
    assert evd["form_face"]["appear_total"] == 0
    assert evd["result_face"]["dead_seeds_total_value"] == 40
    assert evd["cases"]["all_pass"] is True
    assert evd["subset"]["all_ok"] is True


def test_run_dead_extraction_error_fails_closed(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001])
    form = {112400001: _form_product(112400001)}
    result = {112400001: _result_product(112400001)}
    dead_calls = []
    _patch_leaves(monkeypatch, form, result,
                  dead_by_ep={112400001: RuntimeError("engine boom")},
                  dead_calls=dead_calls)
    got = g.run(corpus, _V2, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert dead_calls == [(112400001, _V2)]      # 提取尝试过
    assert got["n_errors"] == 1                  # 死种不可读=该局红
    assert got["passed"] is False
    row = got["per_game_summary"][0]
    assert "engine boom" in row["error"]


def test_run_dead_skipped_when_form_route_errored(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    form = {112400001: _form_product(112400001),
            112400002: {"error": "装载/语料失败: route-a boom"}}
    result = {112400001: _result_product(112400001),
              112400002: _result_product(112400002)}
    diff_calls, dead_calls = [], []
    _patch_leaves(monkeypatch, form, result, diff_calls=diff_calls,
                  dead_calls=dead_calls)
    got = g.run(corpus, _V2, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert [c[0] for c in diff_calls] == [112400001, 112400001,
                                          112400002, 112400002]  # 两路照跑
    assert dead_calls == [(112400001, _V2)]      # (a) 路红局不再取死种
    assert got["n_errors"] == 1 and got["passed"] is False


def test_run_limit_takes_first_n_games(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002, 112400003])
    form = {ep: _form_product(ep) for ep in (112400001, 112400002, 112400003)}
    result = {ep: _result_product(ep)
              for ep in (112400001, 112400002, 112400003)}
    diff_calls = []
    _patch_leaves(monkeypatch, form, result, diff_calls=diff_calls)
    got = g.run(corpus, _V2, _L1, _VB, limit=1,
                evidence_path=str(tmp_path / "ev.json"))
    assert len(diff_calls) == 2                  # 1 局 × 两路
    assert got["per_game_summary"][0]["episode"] == 112400001
    with open(got["evidence_path"], encoding="utf-8") as fh:
        assert json.load(fh)["inputs"]["limit"] == 1


def test_run_empty_corpus_fail_closed(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    got = g.run(str(empty), _V2, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False                # 防空转绿灯
    assert got["n_errors"] == 1
    assert "语料发现失败" in got["per_game_summary"][0]["error"]


def test_run_bad_dir_fail_closed(tmp_path):
    got = g.run(str(tmp_path / "no-such-dir"), _V2, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False and got["n_errors"] == 1
    assert "NotADirectoryError" in got["per_game_summary"][0]["error"]


def test_run_load_failure_error_per_game(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    monkeypatch.setattr(
        g._l1, "replay_action_diff",
        lambda *a: pytest.fail("装载失败不应逐局进真重演"))
    monkeypatch.setattr(g._l1, "precision_subset_check", lambda ps: _subset_ok())
    monkeypatch.setattr(g, "constructed_cases_v2", _cases_ok_v2)
    got = g.run(corpus, "/nonexistent/v2.py", "/nonexistent/l1.py",
                "/nonexistent/vb.py", evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False and got["n_errors"] == 2
    assert all("装载/语料失败" in row["error"]
               for row in got["per_game_summary"])
    assert [row["episode"] for row in got["per_game_summary"]] == [
        112400001, 112400002]                    # error 局号从文件名回填


# ---------------------------------------------------------------------------
# ③ constructed_cases_v2 真跑（夹具直驱，无引擎）
# ---------------------------------------------------------------------------
def test_constructed_cases_v2_five_cases():
    got = g.constructed_cases_v2()
    assert set(got) == {
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c3_s671_boundary", "c4_net_covered_buyback_deleted",
        "c5_net_short_true_future_plant_kept", "all_pass"}
    for name in ("c1_no_trunc_when_future_plant",
                 "c2_trunc_when_no_opportunity",
                 "c4_net_covered_buyback_deleted",
                 "c5_net_short_true_future_plant_kept"):
        assert got[name]["pass"] is True, name
        assert got[name]["evidence"]
    c3 = got["c3_s671_boundary"]
    assert c3["pass"] is True
    assert c3["truncate_side"]["pass"] is True
    assert c3["keep_side"]["pass"] is True
    assert got["all_pass"] is True
