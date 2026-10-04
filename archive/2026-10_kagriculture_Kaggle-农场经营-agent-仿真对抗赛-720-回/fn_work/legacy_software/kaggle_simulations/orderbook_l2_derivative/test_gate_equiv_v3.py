"""test_gate_equiv_v3（R12 门③）：四面裁决矩阵与 run 接线。

不真跑重演（26 局全量两路重演+终态提取留给 verify 编排正式跑批）：
① 裁决矩阵——_aggregate_verdict 纯函数直喂合成双路+终态产物：全过→绿；
   死种合计 600（>$500）→结果面红；某局 v3 终局 < L1→结果面红；在田株数
   减产→结果面红（饿死零容忍面）；差异步 640<window 648→形态面红（同产物
   在 window=600 下界过——双窗阈值参数化）；error 局→两面俱红（fail-closed）；
   subset/cases 红→各自拉红门；空记录集→四面俱红。② run 接线——monkeypatch
   L1 叶（replay_action_diff/precision_subset_check）+ 本门终态提取与构造用例
   假件 + 合成语料目录：逐局两路重演（cand=v3 与 cand=L1、control 均
   verbatim）、终态提取仅在 (a) 路成形局做（v3+L1 两遍）、净回收净算（减量
   消失/出现对 → 净额进 subset dropped 面）、limit 子集、空语料 fail-closed、
   evidence 协议 3.0 结构（per_game 双路+终态产物+四面指标）。③
   constructed_cases_v3 真跑（无引擎，夹具直驱）：九件全过。"""

import json
import os

import pytest

import gate_equivalence_v3 as g  # noqa: E402  (自带 L1_DIR/HERE sys.path 自举)

# 合成哨兵（三 callable 装载一次跨局复用的身份断言用）。
_V3 = lambda obs: {}   # noqa: E731
_L1 = lambda obs: {}   # noqa: E731
_VB = lambda obs: {}   # noqa: E731

_SUMMARY_ROW_KEYS = {
    "episode", "seat", "error", "form_ok", "n_violations",
    "steps_boundary_ok", "min_divergence_step", "kind_counts", "appear_count",
    "n_dropped", "dropped_value_est", "net_recovery_value_est",
    "final_face_ok", "v3_final", "l1_final", "verbatim_final", "final_delta",
    "dead_seeds_value", "dead_seeds", "starve_ok", "n_starve_violations",
    "starve_violations", "v3_plants", "l1_plants", "v3_shed", "l1_shed"}


# ---------------------------------------------------------------------------
# 合成夹具（run 双路+终态产物契约形态）
# ---------------------------------------------------------------------------
def _form_product(episode, seat=0, *, v3_final=1000.0, verbatim_final=980.0,
                  dropped=None, appear=None, extra_divs=None):
    """(a) 路产物（cand=v3/control=verbatim）：divergences=消失+出现（步≥窗界）。"""
    dropped = dropped or []
    divergences = [{"step": e["step"], "kind": "buy_seed_disappear",
                    "detail": f'["BUY_SEED","{e["crop"]}",{e["qty"]}]"'
                              "（verbatim 有 v3 无）",
                    "crop": e["crop"], "qty": e["qty"]} for e in dropped]
    for d in (appear or []):
        divergences.append({"step": d["step"], "kind": "buy_seed_appear",
                            "detail": f'["BUY_SEED","{d["crop"]}",{d["qty"]}]"'
                                      "（v3 有 verbatim 无，减量保单分解面）",
                            "crop": d["crop"], "qty": d["qty"]})
    divergences.extend(extra_divs or [])
    return {"episode": episode, "seat": seat, "game_pass": True,
            "divergences": divergences, "n_divergences": len(divergences),
            "n_violations": 0, "dropped": dropped, "first_divergence": None,
            "l1_final": v3_final, "verbatim_final": verbatim_final,
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


def _record(episode, *, v3_final=1000.0, l1_final=990.0,
            verbatim_final=980.0, dropped=None, appear=None,
            extra_divs=None, dead_value=0, seat=0,
            v3_plants=None, l1_plants=None, v3_shed=None, l1_shed=None):
    return {"episode": episode, "seat": seat, "error": None,
            "form": _form_product(episode, seat, v3_final=v3_final,
                                  verbatim_final=verbatim_final,
                                  dropped=dropped, appear=appear,
                                  extra_divs=extra_divs),
            "result": _result_product(episode, seat, l1_final=l1_final,
                                      verbatim_final=verbatim_final),
            "terminal": {
                "v3": _term(seeds={"CARROT": dead_value // 20} if dead_value
                            else None, plants=v3_plants, shed=v3_shed),
                "l1": _term(plants=l1_plants, shed=l1_shed)}}


def _subset_ok():
    return {"all_ok": True, "per_game": [], "per_crop": {}, "violations": [],
            "errors": [], "summary": {"n_games": 0, "n_violations": 0,
                                      "n_errors": 0}}


def _cases_ok_v3():
    cases = {name: {"pass": True, "evidence": "ok"} for name in (
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c4_covered_buyback_reduced_to_zero",
        "c5_short_true_future_plant_kept", "c6_8to1_forensic",
        "c7_margin_backstop_reactive_overshoot", "c8_empty_slot_ignored",
        "c9_window600_drip")}
    cases["c3_s671_boundary"] = {
        "truncate_side": {"pass": True, "evidence": "ok"},
        "keep_side": {"pass": True, "evidence": "ok"}, "pass": True}
    cases["all_pass"] = True
    return cases


# ---------------------------------------------------------------------------
# ① 裁决矩阵（纯函数直喂）
# ---------------------------------------------------------------------------
def test_matrix_all_green_passes():
    records = [_record(1),
               _record(2, dropped=[{"step": 700, "crop": "WHEAT", "qty": 2}],
                       dead_value=40,
                       v3_plants={"CARROT": 3}, l1_plants={"CARROT": 3})]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["passed"] is True
    assert got["form_face"]["ok"] is True and got["result_face"]["ok"] is True
    assert got["form_face"]["appear_total"] == 0
    assert got["result_face"]["dead_seeds_total_value"] == 40
    assert got["result_face"]["starve_free"] is True
    assert got["n_errors"] == 0
    row = got["per_game_summary"][1]
    assert row["dropped_value_est"] == 20            # WHEAT×2 × $10
    assert row["net_recovery_value_est"] == 20       # 无 appear：净回收=dropped
    assert row["final_delta"] == pytest.approx(10.0)  # v3 1000 − L1 990
    assert row["form_ok"] is True and row["final_face_ok"] is True
    assert row["starve_ok"] is True and row["n_starve_violations"] == 0
    assert set(row) == _SUMMARY_ROW_KEYS


def test_matrix_dead_seeds_600_fails_result_face():
    # R12 硬指标：终局死种合计 ≤$500——$300+$300=$600 → 结果面红（形态面绿）。
    records = [_record(1, dead_value=300), _record(2, dead_value=300)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["result_face"]["dead_seeds_total_value"] == 600
    assert got["result_face"]["dead_seeds_cap"] == g.DEAD_SEEDS_VALUE_CAP == 500
    assert got["result_face"]["ok"] is False and got["passed"] is False
    assert got["form_face"]["ok"] is True            # 面间不串红


def test_matrix_v3_below_l1_one_game_fails_result_face():
    # R12 硬指标：逐局 v3 终局资金 ≥ L1——单局破缺即红，定位行 final_delta<0。
    records = [_record(1), _record(2, v3_final=989.5, l1_final=990.0)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["result_face"]["ok"] is False
    assert got["result_face"]["finals_ok"] is False
    assert got["result_face"]["n_final_face_games_red"] == 1
    row = got["per_game_summary"][1]
    assert row["final_face_ok"] is False
    assert row["final_delta"] == pytest.approx(-0.5)
    assert got["form_face"]["ok"] is True            # 结果面破缺不拉红形态面
    assert got["passed"] is False


def test_matrix_infield_plants_drop_fails_result_face():
    # R12 硬指标（饿死零容忍）：v3 vs L1 终态在田株数/收获产物逐品项不减——
    # 在田 CARROT 5→4 减产 + shed WHEAT 3→2 减产 = 两条 violation，结果面红。
    records = [_record(1, v3_plants={"CARROT": 4, "WHEAT": 1},
                       l1_plants={"CARROT": 5, "WHEAT": 1},
                       v3_shed={"WHEAT": 2}, l1_shed={"WHEAT": 3}),
               _record(2)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["result_face"]["starve_free"] is False
    assert got["result_face"]["n_starve_games_red"] == 1
    assert got["result_face"]["ok"] is False and got["passed"] is False
    assert got["form_face"]["ok"] is True            # 饿死面红不拉红形态面
    violations = {(v["bucket"], v["item"]): v
                  for v in got["result_face"]["starve_violations"]}
    assert set(violations) == {("plants", "CARROT"), ("shed", "WHEAT")}
    assert violations[("plants", "CARROT")]["v3"] == 4
    assert violations[("shed", "WHEAT")]["l1"] == 3
    row = got["per_game_summary"][0]
    assert row["starve_ok"] is False
    assert row["n_starve_violations"] == 2
    assert row["v3_plants"] == {"CARROT": 4, "WHEAT": 1}
    assert row["l1_shed"] == {"WHEAT": 3}
    # 等产不减产（v3 多产）不算红：净面只禁减。
    ok = g._aggregate_verdict(
        [_record(1, v3_plants={"CARROT": 6}, l1_plants={"CARROT": 5})],
        _subset_ok(), _cases_ok_v3())
    assert ok["result_face"]["starve_free"] is True


def test_matrix_boundary_step_below_window_fails_form_face():
    # R12 形态面：全部差异步 ≥ window（双窗参数）——步 640 < 648 → 形态面红；
    # 同产物在 window=600 下界过（600 窗阈值参数化）。
    breach = _record(1, appear=[{"step": 640, "crop": "CARROT", "qty": 1}])
    got = g._aggregate_verdict([breach], _subset_ok(), _cases_ok_v3(), window=648)
    assert got["form_face"]["ok"] is False
    assert got["form_face"]["n_boundary_breach_games"] == 1
    assert got["form_face"]["criteria"]["step_boundary"]["threshold"] == 648
    row = got["per_game_summary"][0]
    assert row["n_violations"] == 0 and row["steps_boundary_ok"] is False
    assert row["min_divergence_step"] == 640
    assert got["result_face"]["ok"] is True           # 面间不串红
    got600 = g._aggregate_verdict([breach], _subset_ok(), _cases_ok_v3(),
                                  window=600)
    assert got600["form_face"]["ok"] is True          # 640 ≥ 600：600 窗放行


def test_matrix_violation_kind_fails_form_face():
    violation = _record(1, extra_divs=[{"step": 680, "kind": "market",
                                        "detail": "synthetic RED"}])
    got = g._aggregate_verdict([violation], _subset_ok(), _cases_ok_v3())
    assert got["form_face"]["ok"] is False
    assert got["form_face"]["n_violation_games"] == 1
    assert got["per_game_summary"][0]["n_violations"] == 1


def test_matrix_error_game_fail_closed_both_faces():
    records = [_record(1),
               {"episode": 2, "seat": None, "error": None, "form": None,
                "result": None, "terminal": None},
               _record(3, dead_value=10)]
    records[1]["form"] = {"error": "装载/语料失败: boom"}
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["n_errors"] == 1                       # 任一路 error → 该局红
    assert got["form_face"]["ok"] is False and got["result_face"]["ok"] is False
    assert got["passed"] is False
    row = got["per_game_summary"][1]
    assert "boom" in row["error"]
    assert row["form_ok"] is False and row["final_face_ok"] is None
    assert row["v3_final"] is None and row["dead_seeds_value"] is None
    assert row["starve_ok"] is None


def test_matrix_terminal_ill_typed_fail_closed():
    # 终态面缺失/畸形（form 成形但 terminal None）→ 该局红（不静默当绿）。
    records = [_record(1),
               dict(_record(2), terminal=None)]
    got = g._aggregate_verdict(records, _subset_ok(), _cases_ok_v3())
    assert got["n_errors"] == 1
    assert "terminal face missing" in got["per_game_summary"][1]["error"]
    assert got["passed"] is False


def test_matrix_subset_or_cases_red_fail_gate():
    records = [_record(1)]
    bad_subset = dict(_subset_ok(), all_ok=False)
    got = g._aggregate_verdict(records, bad_subset, _cases_ok_v3())
    assert got["form_face"]["ok"] and got["result_face"]["ok"]
    assert got["subset"] is False and got["passed"] is False
    bad_cases = _cases_ok_v3()
    bad_cases["c6_8to1_forensic"] = {"pass": False, "evidence": "fixture raised"}
    bad_cases["all_pass"] = False
    got = g._aggregate_verdict(records, _subset_ok(), bad_cases)
    assert got["cases"] is False and got["passed"] is False


def test_matrix_empty_records_fail_closed():
    got = g._aggregate_verdict([], _subset_ok(), _cases_ok_v3())
    assert got["passed"] is False                     # 非空记录集是绿灯前置
    assert got["form_face"]["ok"] is False and got["result_face"]["ok"] is False


def test_net_recovery_netting_pairs():
    # 净回收净算：减量单 8→1 分解为 消失8+出现1 → 净回收 7（appear 不入回收）；
    # 纯整单消失（无 appear）净回收=原量；appear>消失 的品项不入表（净买入）。
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
    assert netted[0]["replay_path"] == products[0]["replay_path"]


# ---------------------------------------------------------------------------
# ② run 接线（monkeypatch L1 叶 + 本门终态/构造用例假件；合成语料目录）
# ---------------------------------------------------------------------------
def _fake_corpus(tmp_path, episodes):
    corpus = tmp_path / "eps"
    corpus.mkdir()
    for ep in episodes:
        (corpus / f"episode-{ep}-strip.json.gz").write_bytes(b"")
    return str(corpus)


def _patch_leaves(monkeypatch, form_by_ep, result_by_ep, v3_term_by_ep=None,
                  l1_term_by_ep=None, subset=None, diff_calls=None,
                  term_calls=None, subset_seen=None):
    v3_term_by_ep = v3_term_by_ep if v3_term_by_ep is not None else {}
    l1_term_by_ep = l1_term_by_ep if l1_term_by_ep is not None else {}
    term_calls = [] if term_calls is None else term_calls

    def fake_diff(replay_path, cand, control):
        ep = g._l1._episode_from_path(replay_path)
        if diff_calls is not None:
            diff_calls.append((ep, cand, control,
                               os.path.basename(replay_path)))
        return (form_by_ep[ep] if cand is _V3 else result_by_ep[ep])

    def fake_terminal(replay_path, agent_fn):
        ep = g._l1._episode_from_path(replay_path)
        term_calls.append((ep, agent_fn))
        if agent_fn is _V3:
            outcome = v3_term_by_ep.get(ep, _term())
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
    monkeypatch.setattr(g, "constructed_cases_v3", _cases_ok_v3)
    monkeypatch.setattr(g, "_seated_terminal", fake_terminal)


def test_run_wiring_two_routes_terminal_and_evidence(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400002, 112400001])    # 乱序落盘
    form = {112400001: _form_product(112400001, v3_final=1005.0),
            112400002: _form_product(
                112400002, v3_final=1005.0,
                dropped=[{"step": 700, "crop": "CARROT", "qty": 8}],
                appear=[{"step": 700, "crop": "CARROT", "qty": 1}])}
    result = {112400001: _result_product(112400001, l1_final=1000.0),
              112400002: _result_product(112400002, l1_final=998.0)}
    diff_calls, term_calls, subset_seen = [], [], []
    _patch_leaves(monkeypatch, form, result,
                  v3_term_by_ep={112400001: _term(),
                                 112400002: _term(seeds={"CARROT": 2},
                                                  plants={"CARROT": 3})},
                  l1_term_by_ep={112400001: _term(),
                                 112400002: _term(plants={"CARROT": 3})},
                  diff_calls=diff_calls, term_calls=term_calls,
                  subset_seen=subset_seen)
    ev = tmp_path / "evidence.json"
    got = g.run(corpus, _V3, _L1, _VB, evidence_path=str(ev))

    assert got["passed"] is True
    assert got["form_face"]["ok"] and got["result_face"]["ok"]
    assert got["subset"] is True and got["cases"] is True
    # 逐局两路重演：局号升序 × (cand=v3 / cand=L1)，control 恒 verbatim，
    # 三 callable 装载一次跨局复用（同一对象喂每局）。
    assert [(c[0], c[1], c[2]) for c in diff_calls] == [
        (112400001, _V3, _VB), (112400001, _L1, _VB),
        (112400002, _V3, _VB), (112400002, _L1, _VB)]
    assert len({id(c[1]) for c in diff_calls if c[1] is not _VB}) == 2
    # 终态提取仅在 (a) 路成形局做：v3（死种+饿死面）与 L1（饿死对照）各一遍。
    assert term_calls == [(112400001, _V3), (112400001, _L1),
                          (112400002, _V3), (112400002, _L1)]
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

    # evidence 协议 3.0：per_game 双路+终态产物 + 四面指标 + 窗口登记
    assert got["evidence_path"] == str(ev) and os.path.isfile(ev)
    with open(ev, encoding="utf-8") as fh:
        evd = json.load(fh)
    assert evd["protocol"] == "orderbook-l2-equivalence/3.0"
    assert evd["inputs"]["n_replays"] == 2
    assert evd["inputs"]["window"] == 648
    assert evd["inputs"]["v3_main"] == "<callable>"
    assert [r["episode"] for r in evd["per_game"]] == [112400001, 112400002]
    assert evd["per_game"][0]["form"] == form[112400001]
    assert evd["per_game"][1]["result"] == result[112400002]
    assert evd["per_game"][1]["terminal"]["v3"]["seeds_value"] == 40
    assert evd["per_game"][1]["terminal"]["l1"]["plants"] == {"CARROT": 3}
    assert evd["verdict"] == {"form_face": True, "result_face": True,
                              "subset": True, "cases": True, "passed": True}
    assert evd["form_face"]["criteria"]["step_boundary"]["threshold"] == 648
    assert evd["result_face"]["dead_seeds_total_value"] == 40
    assert evd["result_face"]["starve_free"] is True
    assert evd["cases"]["all_pass"] is True
    assert evd["subset"]["all_ok"] is True
    assert evd["subset_netting"]["note"]


def test_run_window600_threshold_parametrized(tmp_path, monkeypatch):
    # 双窗阈值接线：同产物（差异步 620）在 window=600 绿、window=648 红。
    corpus = _fake_corpus(tmp_path, [112400001])
    form = {112400001: _form_product(
        112400001, appear=[{"step": 620, "crop": "CARROT", "qty": 1}])}
    result = {112400001: _result_product(112400001)}
    _patch_leaves(monkeypatch, form, result)
    got600 = g.run(corpus, _V3, _L1, _VB, window=600,
                   evidence_path=str(tmp_path / "ev600.json"))
    assert got600["form_face"]["ok"] is True and got600["passed"] is True
    assert got600["form_face"]["criteria"]["step_boundary"]["threshold"] == 600
    got648 = g.run(corpus, _V3, _L1, _VB, window=648,
                   evidence_path=str(tmp_path / "ev648.json"))
    assert got648["form_face"]["ok"] is False and got648["passed"] is False
    with open(got600["evidence_path"], encoding="utf-8") as fh:
        assert json.load(fh)["inputs"]["window"] == 600


def test_run_terminal_extraction_error_fails_closed(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001])
    form = {112400001: _form_product(112400001)}
    result = {112400001: _result_product(112400001)}
    term_calls = []
    _patch_leaves(monkeypatch, form, result,
                  v3_term_by_ep={112400001: RuntimeError("engine boom")},
                  term_calls=term_calls)
    got = g.run(corpus, _V3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert term_calls == [(112400001, _V3)]           # v3 侧提取尝试过即红
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
    got = g.run(corpus, _V3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert [c[0] for c in diff_calls] == [112400001, 112400001,
                                          112400002, 112400002]  # 两路照跑
    assert term_calls == [(112400001, _V3), (112400001, _L1)]  # (a) 路红局不取终态
    assert got["n_errors"] == 1 and got["passed"] is False


def test_run_limit_takes_first_n_games(tmp_path, monkeypatch):
    corpus = _fake_corpus(tmp_path, [112400001, 112400002, 112400003])
    form = {ep: _form_product(ep) for ep in (112400001, 112400002, 112400003)}
    result = {ep: _result_product(ep)
              for ep in (112400001, 112400002, 112400003)}
    diff_calls = []
    _patch_leaves(monkeypatch, form, result, diff_calls=diff_calls)
    got = g.run(corpus, _V3, _L1, _VB, limit=1,
                evidence_path=str(tmp_path / "ev.json"))
    assert len(diff_calls) == 2                        # 1 局 × 两路
    assert got["per_game_summary"][0]["episode"] == 112400001
    with open(got["evidence_path"], encoding="utf-8") as fh:
        assert json.load(fh)["inputs"]["limit"] == 1


def test_run_empty_corpus_fail_closed(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    got = g.run(str(empty), _V3, _L1, _VB,
                evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False                     # 防空转绿灯
    assert got["n_errors"] == 1
    assert "语料发现失败" in got["per_game_summary"][0]["error"]


def test_run_bad_dir_fail_closed(tmp_path):
    got = g.run(str(tmp_path / "no-such-dir"), _V3, _L1, _VB,
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
    monkeypatch.setattr(g, "constructed_cases_v3", _cases_ok_v3)
    got = g.run(corpus, "/nonexistent/v3.py", "/nonexistent/l1.py",
                "/nonexistent/vb.py", evidence_path=str(tmp_path / "ev.json"))
    assert got["passed"] is False and got["n_errors"] == 2
    assert all("装载/语料失败" in row["error"]
               for row in got["per_game_summary"])
    assert [row["episode"] for row in got["per_game_summary"]] == [
        112400001, 112400002]                         # error 局号从文件名回填


# ---------------------------------------------------------------------------
# ③ constructed_cases_v3 真跑（夹具直驱，无引擎）
# ---------------------------------------------------------------------------
def test_constructed_cases_v3_nine_cases():
    got = g.constructed_cases_v3()
    assert set(got) == {
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c3_s671_boundary", "c4_covered_buyback_reduced_to_zero",
        "c5_short_true_future_plant_kept", "c6_8to1_forensic",
        "c7_margin_backstop_reactive_overshoot", "c8_empty_slot_ignored",
        "c9_window600_drip", "all_pass"}
    for name in ("c1_no_trunc_when_future_plant",
                 "c2_trunc_when_no_opportunity",
                 "c4_covered_buyback_reduced_to_zero",
                 "c5_short_true_future_plant_kept", "c6_8to1_forensic",
                 "c7_margin_backstop_reactive_overshoot",
                 "c8_empty_slot_ignored", "c9_window600_drip"):
        assert got[name]["pass"] is True, name
        assert got[name]["evidence"]
    c3 = got["c3_s671_boundary"]
    assert c3["pass"] is True
    assert c3["truncate_side"]["pass"] is True
    assert c3["keep_side"]["pass"] is True
    assert got["all_pass"] is True
