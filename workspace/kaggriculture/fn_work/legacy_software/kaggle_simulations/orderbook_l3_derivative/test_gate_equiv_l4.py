"""test_gate_equiv_l4（R13 门③）：四面裁决矩阵与 run 接线。

不真跑重演（26 局全量两路重演+终态提取留给 verify 编排正式跑批）：
① 裁决矩阵——_aggregate_verdict_l3 纯函数直喂合成双路+终态产物：全过→绿；
   死种合计 $500+$500=$1000（>$900）→结果面红（边界 $450+$450=$900 恰过）；
   某局 l3 终局 < L1→结果面红；在田株数减产→结果面红（饿死零容忍面）；
   差异步 647<648→形态面红（L3 单窗硬界，无 v3 双窗参数）；error 局→两面俱
   红（fail-closed）；subset/cases 红→各自拉红门；空记录集→四面俱红。
② run 接线——monkeypatch L1 叶（replay_action_diff/precision_subset_check）
   + 本门终态提取与构造用例假件 + 合成语料目录：逐局两路重演（cand=l3 与
   cand=L1、control 均 verbatim）、终态提取仅在 (a) 路成形局做（l3+L1 两遍）、
   净回收净算（减量 消失/出现对 → 净额进 subset dropped 面）、limit 子集、空
   语料 fail-closed、evidence 协议 4.0 结构（per_game 双路+终态产物+四面
   指标）。③ constructed_cases_l3 真跑（无引擎，夹具直驱）：七件全过。"""

import json
import os

import pytest

import gate_equivalence_l3 as g  # noqa: E402  (自带 L1/L2/HERE sys.path 自举)

# 合成哨兵（三 callable 装载一次跨局复用的身份断言用）。
_L3 = lambda obs: {}   # noqa: E731
_L1 = lambda obs: {}   # noqa: E731
_VB = lambda obs: {}   # noqa: E731

_SUMMARY_ROW_KEYS = {
    "episode", "seat", "error", "form_ok", "n_violations",
    "steps_boundary_ok", "min_divergence_step", "kind_counts", "appear_count",
    "n_dropped", "dropped_value_est", "net_recovery_value_est",
    "final_face_ok", "l3_final", "l1_final", "verbatim_final", "final_delta",
    "dead_seeds_value", "dead_seeds", "starve_ok", "n_starve_violations",
    "starve_violations", "l3_plants", "l1_plants", "l3_shed", "l1_shed"}


# ---------------------------------------------------------------------------
# 合成夹具（run 双路+终态产物契约形态；terminal 桶名 l3/l1）
# ---------------------------------------------------------------------------
def _form_product(episode, seat=0, *, l3_final=1000.0, verbatim_final=980.0,
                  dropped=None, appear=None, extra_divs=None):
    """(a) 路产物（cand=l3/control=verbatim）：divergences=消失+出现（步≥648）。"""
    dropped = dropped or []
    divergences = [{"step": e["step"], "kind": "buy_seed_disappear",
                    "detail": f'["BUY_SEED","{e["crop"]}",{e["qty"]}]"'
                              "（verbatim 有 l3 无）",
                    "crop": e["crop"], "qty": e["qty"]} for e in dropped]
    for d in (appear or []):
        divergences.append({"step": d["step"], "kind": "buy_seed_appear",
                            "detail": f'["BUY_SEED","{d["crop"]}",{d["qty"]}]"'
                                      "（l3 有 verbatim 无，减量保单分解面）",
                            "crop": d["crop"], "qty": d["qty"]})
    divergences.extend(extra_divs or [])
    return {"episode": episode, "seat": seat, "game_pass": True,
            "divergences": divergences, "n_divergences": len(divergences),
            "n_violations": 0, "dropped": dropped, "first_divergence": None,
            "l1_final": l3_final, "verbatim_final": verbatim_final,
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


def _term(*, seeds=None, plants=None, shed=None, inventories=None, money=1000.0):
    """终态产物（_seated_terminal 契约形态；seeds 逐品补 0，value=Σqty×票价）。"""
    seeds = seeds or {}
    normalized = {crop: seeds.get(crop, 0) for crop in g._l1.SEED_PRICE}
    return {"final_money": money, "seeds": normalized,
            "seeds_value": sum(q * g._l1.SEED_PRICE[c]
                               for c, q in normalized.items()),
            "plants": dict(plants or {}), "shed": dict(shed or {}),
            "inventories": dict(inventories or {})}


def _record(episode, *, l3_final=1000.0, l1_final=990.0,
            verbatim_final=980.0, dropped=None, appear=None,
            extra_divs=None, dead_value=0, seat=0,
            l3_plants=None, l1_plants=None, l3_shed=None, l1_shed=None):
    return {"episode": episode, "seat": seat, "error": None,
            "form": _form_product(episode, seat, l3_final=l3_final,
                                  verbatim_final=verbatim_final,
                                  dropped=dropped, appear=appear,
                                  extra_divs=extra_divs),
            "result": _result_product(episode, seat, l1_final=l1_final,
                                      verbatim_final=verbatim_final),
            "terminal": {
                "l3": _term(seeds={"CARROT": dead_value // 20} if dead_value
                            else None, plants=l3_plants, shed=l3_shed),
                "l1": _term(plants=l1_plants, shed=l1_shed)}}


def _subset_ok():
    return {"all_ok": True, "per_game": [], "per_crop": {}, "violations": [],
            "errors": [], "summary": {"n_games": 0, "n_violations": 0,
                                      "n_errors": 0}}


def _cases_ok_l3():
    cases = {name: {"pass": True, "evidence": "ok"} for name in (
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c4_clamp_trigger_demand_plus_two", "c5_day28_swap_no_starve",
        "c6_clamp_fallback_returns_buffer", "c7_mode_a_dormant_zero_footprint")}
    cases["c3_s671_boundary"] = {
        "truncate_side": {"pass": True, "evidence": "ok"},
        "keep_side": {"pass": True, "evidence": "ok"}, "pass": True}
    cases["all_pass"] = True
    return cases


# ---------------------------------------------------------------------------
# ① 裁决矩阵（纯函数直喂）
# ---------------------------------------------------------------------------
def test_gate_equiv_l3_matrix():
    # 全绿基线：两局（一局带 WHEAT 整单消失+死种 $40）→ 四面全绿。
    records = [_record(1),
               _record(2, dropped=[{"step": 700, "crop": "WHEAT", "qty": 2}],
                       dead_value=40,
                       l3_plants={"CARROT": 3}, l1_plants={"CARROT": 3})]
    got = g._aggregate_verdict_l3(records, _subset_ok(), _cases_ok_l3())
    assert got["passed"] is True
    assert got["form_face"]["ok"] is True and got["result_face"]["ok"] is True
    assert got["form_face"]["appear_total"] == 0
    assert got["result_face"]["dead_seeds_total_value"] == 40
    assert got["result_face"]["starve_free"] is True
    assert got["n_errors"] == 0
    row = got["per_game_summary"][1]
    assert row["dropped_value_est"] == 20            # WHEAT×2 × $10
    assert row["net_recovery_value_est"] == 20       # 无 appear：净回收=dropped
    assert row["final_delta"] == pytest.approx(10.0)  # l3 1000 − L1 990
    assert row["form_ok"] is True and row["final_face_ok"] is True
    assert row["starve_ok"] is True and row["n_starve_violations"] == 0
    assert set(row) == _SUMMARY_ROW_KEYS
    assert row["l3_final"] == 1000.0 and row["l1_final"] == 990.0

    # 死种合计 $500+$500=$1000 > $900 → 结果面红（形态面不串红）；
    # 边界单局 CARROT×45=$900 恰过帽（≤ 含端）。
    red = g._aggregate_verdict_l3([_record(1, dead_value=500),
                                   _record(2, dead_value=500)],
                                  _subset_ok(), _cases_ok_l3())
    assert red["result_face"]["ok"] is False and red["passed"] is False
    assert red["result_face"]["dead_seeds_total_value"] == 1000
    assert red["result_face"]["dead_seeds_cap"] == g.DEAD_SEEDS_VALUE_CAP == 900
    assert red["form_face"]["ok"] is True
    edge = g._aggregate_verdict_l3([_record(1, dead_value=900)],
                                   _subset_ok(), _cases_ok_l3())
    assert edge["result_face"]["dead_seeds_total_value"] == 900
    assert edge["result_face"]["ok"] is True and edge["passed"] is True

    # 逐局 l3 终局 < L1 → 结果面红（final_delta<0 定位行）。
    below = g._aggregate_verdict_l3(
        [_record(1), _record(2, l3_final=989.5, l1_final=990.0)],
        _subset_ok(), _cases_ok_l3())
    assert below["result_face"]["ok"] is False
    assert below["result_face"]["finals_ok"] is False
    assert below["result_face"]["n_final_face_games_red"] == 1
    assert below["per_game_summary"][1]["final_face_ok"] is False
    assert below["per_game_summary"][1]["final_delta"] == pytest.approx(-0.5)
    assert below["form_face"]["ok"] is True and below["passed"] is False

    # 饿死零容忍：在田 CARROT 5→4 + shed WHEAT 3→2 → 两条 violation 结果面红。
    starve = g._aggregate_verdict_l3(
        [_record(1, l3_plants={"CARROT": 4, "WHEAT": 1},
                 l1_plants={"CARROT": 5, "WHEAT": 1},
                 l3_shed={"WHEAT": 2}, l1_shed={"WHEAT": 3}),
         _record(2)], _subset_ok(), _cases_ok_l3())
    assert starve["result_face"]["starve_free"] is False
    assert starve["result_face"]["n_starve_games_red"] == 1
    assert starve["result_face"]["ok"] is False and starve["passed"] is False
    assert starve["form_face"]["ok"] is True
    violations = {(v["bucket"], v["item"]): v
                  for v in starve["result_face"]["starve_violations"]}
    assert set(violations) == {("plants", "CARROT"), ("shed", "WHEAT")}
    row = starve["per_game_summary"][0]
    assert row["starve_ok"] is False and row["n_starve_violations"] == 2
    assert row["l3_plants"] == {"CARROT": 4, "WHEAT": 1}
    assert row["l1_shed"] == {"WHEAT": 3}
    # 等产不减产（l3 多产）不算红：净面只禁减。
    ok = g._aggregate_verdict_l3(
        [_record(1, l3_plants={"CARROT": 6}, l1_plants={"CARROT": 5})],
        _subset_ok(), _cases_ok_l3())
    assert ok["result_face"]["starve_free"] is True

    # 步界：差异步 647 < 648 → 形态面红（L3 单窗硬界；结果面不串红）。
    breach = g._aggregate_verdict_l3(
        [_record(1, appear=[{"step": 647, "crop": "CARROT", "qty": 1}])],
        _subset_ok(), _cases_ok_l3())
    assert breach["form_face"]["ok"] is False
    assert breach["form_face"]["n_boundary_breach_games"] == 1
    assert breach["form_face"]["criteria"]["step_boundary"]["threshold"] == 648
    assert breach["per_game_summary"][0]["min_divergence_step"] == 647
    assert breach["result_face"]["ok"] is True
    # 648 恰在界内（≥648 含端）。
    edge_step = g._aggregate_verdict_l3(
        [_record(1, appear=[{"step": 648, "crop": "CARROT", "qty": 1}])],
        _subset_ok(), _cases_ok_l3())
    assert edge_step["form_face"]["ok"] is True

    # violation 形态（market 等形态外 kind）→ 形态面红。
    violation = g._aggregate_verdict_l3(
        [_record(1, extra_divs=[{"step": 680, "kind": "market",
                                 "detail": "synthetic RED"}])],
        _subset_ok(), _cases_ok_l3())
    assert violation["form_face"]["ok"] is False
    assert violation["form_face"]["n_violation_games"] == 1
    assert violation["per_game_summary"][0]["n_violations"] == 1

    # error 局：两面俱红（fail-closed；数值面 None）。
    errors = [_record(1),
              {"episode": 2, "seat": None, "error": None, "form": None,
               "result": None, "terminal": None},
              _record(3, dead_value=10)]
    errors[1]["form"] = {"error": "装载/语料失败: boom"}
    errored = g._aggregate_verdict_l3(errors, _subset_ok(), _cases_ok_l3())
    assert errored["n_errors"] == 1
    assert errored["form_face"]["ok"] is False
    assert errored["result_face"]["ok"] is False and errored["passed"] is False
    row = errored["per_game_summary"][1]
    assert "boom" in row["error"]
    assert row["form_ok"] is False and row["final_face_ok"] is None
    assert row["l3_final"] is None and row["dead_seeds_value"] is None
    assert row["starve_ok"] is None

    # 终态面缺失（form 成形但 terminal None）→ 该局红。
    ill = g._aggregate_verdict_l3([_record(1), dict(_record(2), terminal=None)],
                                  _subset_ok(), _cases_ok_l3())
    assert ill["n_errors"] == 1
    assert "terminal face missing" in ill["per_game_summary"][1]["error"]

    # subset/cases 红 → 各自拉红门（两面绿不保过）。
    bad_subset = dict(_subset_ok(), all_ok=False)
    sub = g._aggregate_verdict_l3([_record(1)], bad_subset, _cases_ok_l3())
    assert sub["form_face"]["ok"] and sub["result_face"]["ok"]
    assert sub["subset"] is False and sub["passed"] is False
    bad_cases = _cases_ok_l3()
    bad_cases["c6_clamp_fallback_returns_buffer"] = {
        "pass": False, "evidence": "fixture raised"}
    bad_cases["all_pass"] = False
    case_red = g._aggregate_verdict_l3([_record(1)], _subset_ok(), bad_cases)
    assert case_red["cases"] is False and case_red["passed"] is False

    # 空记录集 → 四面俱红（防空转绿灯）。
    empty = g._aggregate_verdict_l3([], _subset_ok(), _cases_ok_l3())
    assert empty["passed"] is False
    assert empty["form_face"]["ok"] is False
    assert empty["result_face"]["ok"] is False


def test_net_recovery_netting_pairs_reused_from_v3():
    # 净回收净算（v3 部件 import 复用）：减量单 8→1 分解为 消失8+出现1 →
    # 净回收 7；纯整单消失净回收=原量；appear>消失 的品项不入表（净买入）。
    divergences = [
        {"step": 700, "kind": "buy_seed_disappear", "crop": "CARROT", "qty": 8},
        {"step": 700, "kind": "buy_seed_appear", "crop": "CARROT", "qty": 1},
        {"step": 705, "kind": "buy_seed_disappear", "crop": "WHEAT", "qty": 2},
        {"step": 706, "kind": "buy_seed_appear", "crop": "TOMATO", "qty": 3},
    ]
    assert g._net_recovery_by_crop(divergences) == {"CARROT": 7, "WHEAT": 2}
    products = [{"episode": 1, "seat": 0, "divergences": divergences,
                 "dropped": [{"step": 700, "crop": "CARROT", "qty": 8},
                             {"step": 705, "crop": "WHEAT", "qty": 2}],
                 "replay_path": "/synthetic/episode-1-strip.json.gz"},
                {"error": "装载/语料失败: boom"}]
    netted = g._netted_recovery_products(products)
    assert netted[1] is products[1]                   # error 局原样透传
    assert netted[0]["dropped"] == [
        {"step": 700, "crop": "CARROT", "qty": 7},    # step 取该品项最小消失步
        {"step": 705, "crop": "WHEAT", "qty": 2}]


# ---------------------------------------------------------------------------
# ② run 接线（monkeypatch L1 叶 + 本门终态/构造用例假件；合成语料目录）
# ---------------------------------------------------------------------------
def _fake_corpus(tmp_path, episodes):
    corpus = tmp_path / "eps"
    corpus.mkdir()
    for ep in episodes:
        (corpus / f"episode-{ep}-strip.json.gz").write_bytes(b"")
    return str(corpus)


def _patch_leaves(monkeypatch, form_by_ep, result_by_ep, l3_term_by_ep=None,
                  l1_term_by_ep=None, subset=None, diff_calls=None,
                  term_calls=None, subset_seen=None):
    l3_term_by_ep = l3_term_by_ep if l3_term_by_ep is not None else {}
    l1_term_by_ep = l1_term_by_ep if l1_term_by_ep is not None else {}
    term_calls = [] if term_calls is None else term_calls

    def fake_diff(replay_path, cand, control):
        ep = g._l1._episode_from_path(replay_path)
        if diff_calls is not None:
            diff_calls.append((ep, cand, control,
                               os.path.basename(replay_path)))
        return (form_by_ep[ep] if cand is _L3 else result_by_ep[ep])

    def fake_terminal(replay_path, agent_fn):
        ep = g._l1._episode_from_path(replay_path)
        term_calls.append((ep, agent_fn))
        if agent_fn is _L3:
            outcome = l3_term_by_ep.get(ep, _term())
        else:
            outcome = l1_term_by_ep.get(ep, _term())
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    def fake_subset(products):
        if subset_seen is not None:
            subset_seen.append(list(products))
        return subset if subset is not None else _subset_ok()

    monkeypatch.setattr(g._l1, "replay_action_diff", fake_diff)
    monkeypatch.setattr(g._l1, "precision_subset_check", fake_subset)
    monkeypatch.setattr(g, "constructed_cases_l3", _cases_ok_l3)
    monkeypatch.setattr(g, "_seated_terminal", fake_terminal)


def test_run_wiring_two_routes_terminal_and_evidence(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400002, 112400001])    # 乱序落盘
    form = {112400001: _form_product(112400001, l3_final=1005.0),
            112400002: _form_product(
                112400002, l3_final=1005.0,
                dropped=[{"step": 700, "crop": "CARROT", "qty": 8}],
                appear=[{"step": 700, "crop": "CARROT", "qty": 1}])}
    result = {112400001: _result_product(112400001, l1_final=1000.0),
              112400002: _result_product(112400002, l1_final=998.0)}
    diff_calls, term_calls, subset_seen = [], [], []
    _patch_leaves(monkeypatch, form, result,
                  l3_term_by_ep={112400001: _term(),
                                 112400002: _term(seeds={"CARROT": 2},
                                                  plants={"CARROT": 3})},
                  l1_term_by_ep={112400001: _term(),
                                 112400002: _term(plants={"CARROT": 3})},
                  diff_calls=diff_calls, term_calls=term_calls,
                  subset_seen=subset_seen)
    ev = tmp_path / "evidence.json"
    got = g.run(corpus, _L3, _L1, _VB, evidence_path=str(ev))

    assert got["passed"] is True
    assert got["form_face"]["ok"] and got["result_face"]["ok"]
    assert got["subset"] is True and got["cases"] is True
    # 逐局两路重演：局号升序 × (cand=l3 / cand=L1)，control 恒 verbatim，
    # 三 callable 装载一次跨局复用（同一对象喂每局）。
    assert [(c[0], c[1], c[2]) for c in diff_calls] == [
        (112400001, _L3, _VB), (112400001, _L1, _VB),
        (112400002, _L3, _VB), (112400002, _L1, _VB)]
    assert len({id(c[1]) for c in diff_calls if c[1] is not _VB}) == 2
    # 终态提取仅在 (a) 路成形局做：l3（死种+饿死面）与 L1（饿死对照）各一遍。
    assert term_calls == [(112400001, _L3), (112400001, _L1),
                          (112400002, _L3), (112400002, _L1)]
    assert got["result_face"]["dead_seeds_total_value"] == 40
    assert got["result_face"]["starve_free"] is True
    row2 = got["per_game_summary"][1]
    assert row2["dropped_value_est"] == 160            # CARROT×8 × $20（原始消失）
    assert row2["net_recovery_value_est"] == 140       # 净回收 7 × $20
    assert row2["final_delta"] == pytest.approx(1005.0 - 998.0)
    # 返回契约键
    assert set(got) >= {"passed", "form_face", "result_face", "subset",
                        "cases", "per_game_summary", "n_errors",
                        "evidence_path"}
    assert got["n_errors"] == 0

    # 净回收净算进 subset 面：减量 8→1 对 → dropped=净额 7（appear 不入回收）。
    assert len(subset_seen) == 1
    assert subset_seen[0][1]["dropped"] == [
        {"step": 700, "crop": "CARROT", "qty": 7}]
    assert subset_seen[0][0]["dropped"] == []

    # evidence 协议 4.0：per_game 双路+终态产物 + 四面指标 + 步界登记
    assert got["evidence_path"] == str(ev) and os.path.isfile(ev)
    with open(ev, encoding="utf-8") as fh:
        evd = json.load(fh)
    assert evd["protocol"] == "orderbook-l3-equivalence/4.0"
    assert evd["inputs"]["n_replays"] == 2
    assert evd["inputs"]["step_boundary"] == 648
    assert evd["inputs"]["l3_main"] == "<callable>"
    assert [r["episode"] for r in evd["per_game"]] == [112400001, 112400002]
    assert evd["per_game"][0]["form"] == form[112400001]
    assert evd["per_game"][1]["result"] == result[112400002]
    assert evd["per_game"][1]["terminal"]["l3"]["seeds_value"] == 40
    assert evd["per_game"][1]["terminal"]["l1"]["plants"] == {"CARROT": 3}
    assert evd["verdict"] == {"form_face": True, "result_face": True,
                              "subset": True, "cases": True, "passed": True}
    assert evd["form_face"]["criteria"]["step_boundary"]["threshold"] == 648
    assert evd["result_face"]["dead_seeds_total_value"] == 40
    assert evd["result_face"]["dead_seeds_cap"] == 900
    assert evd["result_face"]["starve_free"] is True
    assert evd["cases"]["all_pass"] is True
    assert evd["subset"]["all_ok"] is True
    assert evd["subset_netting"]["note"]


def test_run_dead_seeds_cap_900_wiring(tmp_path, monkeypatch):
    # 死种帽 900 接线：两局各死种 $500（CARROT×25）→ 合计 $1000 → 结果面红。
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    form = {ep: _form_product(ep) for ep in (112400001, 112400002)}
    result = {ep: _result_product(ep) for ep in (112400001, 112400002)}
    _patch_leaves(monkeypatch, form, result,
                  l3_term_by_ep={ep: _term(seeds={"CARROT": 25})
                                 for ep in (112400001, 112400002)})
    got = g.run(corpus, _L3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["result_face"]["dead_seeds_total_value"] == 1000
    assert got["result_face"]["ok"] is False and got["passed"] is False
    assert got["form_face"]["ok"] is True              # 面间不串红


def test_run_terminal_extraction_error_fails_closed(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001])
    form = {112400001: _form_product(112400001)}
    result = {112400001: _result_product(112400001)}
    term_calls = []
    _patch_leaves(monkeypatch, form, result,
                  l3_term_by_ep={112400001: RuntimeError("engine boom")},
                  term_calls=term_calls)
    got = g.run(corpus, _L3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert term_calls == [(112400001, _L3)]           # l3 侧提取尝试过即红
    assert got["n_errors"] == 1                       # 终态不可读=该局红
    assert got["passed"] is False
    assert "engine boom" in got["per_game_summary"][0]["error"]


def test_run_terminal_skipped_when_form_route_errored(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    form = {112400001: _form_product(112400001),
            112400002: {"error": "装载/语料失败: route-a boom"}}
    result = {112400001: _result_product(112400001),
              112400002: _result_product(112400002)}
    diff_calls, term_calls = [], []
    _patch_leaves(monkeypatch, form, result, diff_calls=diff_calls,
                  term_calls=term_calls)
    got = g.run(corpus, _L3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert [c[0] for c in diff_calls] == [112400001, 112400001,
                                          112400002, 112400002]  # 两路照跑
    assert term_calls == [(112400001, _L3), (112400001, _L1)]  # (a) 路红局不取终态
    assert got["n_errors"] == 1 and got["passed"] is False


def test_run_limit_takes_first_n_games(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002, 112400003])
    form = {ep: _form_product(ep) for ep in (112400001, 112400002, 112400003)}
    result = {ep: _result_product(ep)
              for ep in (112400001, 112400002, 112400003)}
    diff_calls = []
    _patch_leaves(monkeypatch, form, result, diff_calls=diff_calls)
    got = g.run(corpus, _L3, _L1, _VB, limit=1,
                evidence_path=str(tmp_path / "ev.json"))
    assert len(diff_calls) == 2                        # 1 局 × 两路
    assert got["per_game_summary"][0]["episode"] == 112400001
    with open(got["evidence_path"], encoding="utf-8") as fh:
        assert json.load(fh)["inputs"]["limit"] == 1


def test_run_empty_corpus_fail_closed(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    got = g.run(str(empty), _L3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False                     # 防空转绿灯
    assert got["n_errors"] == 1
    assert "语料发现失败" in got["per_game_summary"][0]["error"]


def test_run_bad_dir_fail_closed(tmp_path):
    got = g.run(str(tmp_path / "no-such-dir"), _L3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False and got["n_errors"] == 1
    assert "NotADirectoryError" in got["per_game_summary"][0]["error"]


def test_run_load_failure_error_per_game(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002])
    monkeypatch.setattr(
        g._l1, "replay_action_diff",
        lambda *a: pytest.fail("装载失败不应逐局进真重演"))
    monkeypatch.setattr(g._l1, "precision_subset_check",
                        lambda ps: _subset_ok())
    monkeypatch.setattr(g, "constructed_cases_l3", _cases_ok_l3)
    got = g.run(corpus, "/nonexistent/l3.py", "/nonexistent/l1.py",
                "/nonexistent/vb.py", evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False and got["n_errors"] == 2
    assert all("装载/语料失败" in row["error"]
               for row in got["per_game_summary"])
    assert [row["episode"] for row in got["per_game_summary"]] == [
        112400001, 112400002]                         # error 局号从文件名回填


# ---------------------------------------------------------------------------
# ③ constructed_cases_l3 真跑（夹具直驱，无引擎）
# ---------------------------------------------------------------------------
def test_constructed_cases_l3_seven_cases():
    got = g.constructed_cases_l3()
    assert set(got) == {
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c3_s671_boundary", "c4_clamp_trigger_demand_plus_two",
        "c5_day28_swap_no_starve", "c6_clamp_fallback_returns_buffer",
        "c7_mode_a_dormant_zero_footprint", "all_pass"}
    assert got["all_pass"] is True
    for name in ("c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
                 "c4_clamp_trigger_demand_plus_two", "c5_day28_swap_no_starve",
                 "c6_clamp_fallback_returns_buffer",
                 "c7_mode_a_dormant_zero_footprint"):
        assert got[name]["pass"] is True, (name, got[name]["evidence"])
    assert got["c3_s671_boundary"]["pass"] is True
    assert got["c3_s671_boundary"]["truncate_side"]["pass"] is True
    assert got["c3_s671_boundary"]["keep_side"]["pass"] is True
