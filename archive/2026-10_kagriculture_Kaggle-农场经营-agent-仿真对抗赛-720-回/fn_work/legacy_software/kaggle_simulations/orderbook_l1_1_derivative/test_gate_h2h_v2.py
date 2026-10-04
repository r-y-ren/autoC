"""test_gate_h2h_v2（R11 门①）：接线与互胜口径。

真跑只覆盖 4 局（seeds (101,201) 双席位 vs L1，ref_seeds=() 跳过参考面）控制
耗时且台账落 tmp（evidence_path 覆写，不写真 evidence/）；16+8 全量留给门编排
verify_l11_gates。真跑不断言胜负，只断言结构/DONE/装载身份（双侧均
_cxs_agent——v2 候选单测态装载：verbatim 基座源 + v2 块源 exec 到同一命名空
间，末 callable=_cxs_agent，宿主捕获=基座 _cxd_agent，与 build 注入态同构）
与裁决逻辑一致性。合成面：互胜率矩阵（passed 只随主面翻转）+ 参考面只记账
不进门 + 期望名/种子/台账路径接线。"""

import json
import math
import os
import sys

import pytest

import gate_h2h_vs_l1 as gate  # noqa: E402  (自带 L1_DIR sys.path 自举)

import gate_h2h_vs_verbatim as base  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)
L1_MAIN = os.path.join(KSIM, "orderbook_l1_derivative", "main.py")
VERBATIM_MAIN = os.path.join(KSIM, "orderbook_derivative", "main.py")
V2_BLOCK = os.path.join(HERE, "layer_s_block_v2.py")

_RESULT_KEYS = {"n", "wins", "rate", "passed", "ref_face", "evidence_path"}

# v2 候选哨兵（合成接线用；真跑用 _v2_callable() 的真装载件）。
_V2_SENTINEL = lambda obs: {}  # noqa: E731


def _v2_callable():
    """v2 候选单测态装载：verbatim 基座源 + v2 块源 exec 到同一命名空间。

    与 build 注入态同构（块首宿主捕获取到基座 _cxd_agent，末 callable=
    _cxs_agent）；装载纪律沿 L1 官方 last-callable 复刻（__name__ 防主守卫、
    exec 目录临时入 sys.path、不落 __pycache__）。"""
    ns = {"__name__": "v2_agent_under_test", "__file__": VERBATIM_MAIN}
    exec_dir = os.path.dirname(VERBATIM_MAIN)
    sys.path.insert(0, exec_dir)
    old_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        with open(VERBATIM_MAIN, "r", encoding="utf-8") as fh:
            exec(compile(fh.read(), VERBATIM_MAIN, "exec"), ns)
        with open(V2_BLOCK, "r", encoding="utf-8") as fh:
            exec(compile(fh.read(), V2_BLOCK, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
        sys.dont_write_bytecode = old_bytecode
    callables = [v for v in ns.values() if callable(v)]
    assert getattr(callables[-1], "__name__", None) == "_cxs_agent"
    return callables[-1]


# ---------------------------------------------------------------------------
# 合成接线（monkeypatch L1 门① run 为契约假件：区分主面/参考面按期望名集）
# ---------------------------------------------------------------------------
_MAIN_PAYLOAD = {"n_games": 16, "n": 16, "wins": 9, "losses": 6, "ties": 1,
                 "rate": 0.6, "passed": True}
_REF_PAYLOAD = {"n_games": 8, "n": 8, "wins": 2, "losses": 6, "ties": 0,
                "rate": 0.25, "passed": False}


def _install_fake_base(monkeypatch, main_payload=None, ref_payload=None,
                       calls=None):
    """L1 门① run 假件：按 verbatim 期望名集辨面（主面 _cxs_agent / 参考面
    _cxd_agent），落证据件（契约 mimic），返回 payload。"""
    main_payload = _MAIN_PAYLOAD if main_payload is None else main_payload
    ref_payload = _REF_PAYLOAD if ref_payload is None else ref_payload

    def fake_run(cand, opp, seeds=None, evidence_path=None,
                 l1_expected_names=None, verbatim_expected_names=None):
        is_ref = (frozenset(verbatim_expected_names or ())
                  == gate.VERBATIM_EXPECTED_CALLABLES)
        if calls is not None:
            calls.append({
                "face": "ref" if is_ref else "main", "cand": cand, "opp": opp,
                "seeds": tuple(seeds or ()),
                "evidence_path": evidence_path,
                "l1_expected_names": frozenset(l1_expected_names or ()),
                "verbatim_expected_names": frozenset(
                    verbatim_expected_names or ())})
        payload = dict(ref_payload if is_ref else main_payload)
        payload["evidence_path"] = evidence_path      # 契约 mimic：返回台账路径
        os.makedirs(os.path.dirname(evidence_path), exist_ok=True)
        with open(evidence_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
        return dict(payload)

    monkeypatch.setattr(base, "run", fake_run)


def test_wiring_two_faces_and_expected_names(tmp_path, monkeypatch):
    """主面（v2 vs L1，双侧 _cxs_agent，16 局种子）+ 参考面（vs verbatim，
    _cxs_agent/_cxd_agent，101-104）各一调用；台账路径主件/参考件分开。"""
    calls = []
    _install_fake_base(monkeypatch, calls=calls)
    ev = tmp_path / "h2h_evidence.json"
    result = gate.run(_V2_SENTINEL, L1_MAIN, VERBATIM_MAIN,
                      evidence_path=str(ev))
    assert [c["face"] for c in calls] == ["main", "ref"]

    main_call = calls[0]
    assert main_call["cand"] is _V2_SENTINEL          # v2 为 cand
    assert main_call["opp"] == L1_MAIN                # L1 为对手
    assert main_call["seeds"] == tuple(gate.DEFAULT_SEEDS)   # 16 局缺省种子
    assert main_call["l1_expected_names"] == frozenset({"_cxs_agent"})
    assert main_call["verbatim_expected_names"] == frozenset({"_cxs_agent"})
    assert main_call["evidence_path"] == str(ev)

    ref_call = calls[1]
    assert ref_call["cand"] is _V2_SENTINEL
    assert ref_call["opp"] == VERBATIM_MAIN
    assert ref_call["seeds"] == tuple(gate.DEFAULT_REF_SEEDS)  # 8 局参考面
    assert ref_call["l1_expected_names"] == frozenset({"_cxs_agent"})
    assert ref_call["verbatim_expected_names"] == frozenset({"_cxd_agent"})
    assert ref_call["evidence_path"] == str(tmp_path / "h2h_ref_evidence.json")

    assert set(result) == _RESULT_KEYS
    assert (result["n"], result["wins"], result["rate"]) == (16, 9, 0.6)
    assert result["evidence_path"] == str(ev)


def test_ref_face_bookkept_but_not_gating(tmp_path, monkeypatch):
    """参考面只记账不进门：ref rate=0.25（远低阈值）而主面 0.6 → 门①仍绿；
    ref_face 摘要入返回值与主台账件。"""
    _install_fake_base(monkeypatch)
    ev = tmp_path / "h2h_evidence.json"
    result = gate.run(_V2_SENTINEL, L1_MAIN, VERBATIM_MAIN,
                      evidence_path=str(ev))
    assert result["passed"] is True                    # 只随主面
    assert result["ref_face"]["rate"] == 0.25
    assert result["ref_face"]["n"] == 8
    assert result["ref_face"]["gating"] is False
    assert result["ref_face"]["evidence_path"] == str(
        tmp_path / "h2h_ref_evidence.json")
    with open(ev, encoding="utf-8") as fh:             # 主台账增记参考面摘要
        evidence = json.load(fh)
    assert evidence["ref_face"] == result["ref_face"]
    assert (tmp_path / "h2h_ref_evidence.json").is_file()


@pytest.mark.parametrize("main_rate, main_passed", [
    (0.55, True),    # 恰阈值（9W/…计 11/20 → 0.55）
    (0.5, False),    # 低于阈值
])
def test_pass_matrix_follows_main_face(tmp_path, monkeypatch, main_rate,
                                       main_passed):
    """互胜率矩阵（合成）：passed 只随主面 rate 翻转，参考面恒不进门。"""
    wins = 11 if main_rate == 0.55 else 10
    losses = 9 if main_rate == 0.55 else 10
    _install_fake_base(
        monkeypatch,
        main_payload={"n": 20, "wins": wins, "losses": losses,
                      "rate": main_rate, "passed": main_passed})
    result = gate.run(_V2_SENTINEL, L1_MAIN, VERBATIM_MAIN,
                      evidence_path=str(tmp_path / "h2h_evidence.json"))
    assert result["rate"] == main_rate
    assert result["passed"] is main_passed
    assert result["ref_face"]["rate"] == _REF_PAYLOAD["rate"]


def test_ref_face_skippable_for_real_run_budget(tmp_path, monkeypatch):
    """ref_seeds=() 跳过参考面（单测真跑局数控制通道）：单调用 + skipped 记账。"""
    calls = []
    _install_fake_base(monkeypatch, calls=calls)
    result = gate.run(_V2_SENTINEL, L1_MAIN, VERBATIM_MAIN, seeds=(101,),
                      ref_seeds=(), evidence_path=str(tmp_path / "ev.json"))
    assert [c["face"] for c in calls] == ["main"]
    assert calls[0]["seeds"] == (101,)                 # 主面种子显式参数化
    assert result["ref_face"]["n"] == 0
    assert result["ref_face"]["skipped"] is True
    assert result["ref_face"]["gating"] is False
    assert result["ref_face"]["evidence_path"] is None
    assert not (tmp_path / "h2h_ref_evidence.json").exists()


def test_identity_mismatch_propagates_fail_closed(tmp_path):
    """装载身份断言经 L1 门透传（fail-closed 不开打；本测试不装假件，直接走
    真 run）：v2 侧末 callable 名不符 → GateH2HError 上抛，未开打未落台账。"""
    bad = tmp_path / "bad_v2.py"
    bad.write_text("def _wrong_name_agent(obs):\n    return {}\n",
                   encoding="utf-8")
    with pytest.raises(base.GateH2HError, match="装载身份不符"):
        gate.run(str(bad), L1_MAIN, VERBATIM_MAIN, seeds=(101,), ref_seeds=(),
                 evidence_path=str(tmp_path / "ev.json"))


# ---------------------------------------------------------------------------
# 真跑 2 seeds × 双席位 vs L1（4 局；台账落 tmp；不断言胜负）
# ---------------------------------------------------------------------------
def test_run_real_seeds_101_201_both_seats_vs_l1(tmp_path):
    v2 = _v2_callable()
    ev = tmp_path / "h2h_evidence.json"
    result = gate.run(v2, L1_MAIN, VERBATIM_MAIN, seeds=(101, 201),
                      ref_seeds=(), evidence_path=str(ev))
    assert set(result) == _RESULT_KEYS
    assert result["n"] == 4
    assert result["ref_face"]["skipped"] is True
    assert result["evidence_path"] == str(ev)

    with open(result["evidence_path"], encoding="utf-8") as fh:
        evidence = json.load(fh)
    assert evidence["n_games"] == 4 and len(evidence["games"]) == 4
    assert evidence["all_done"] is True
    # 装载身份留痕：双侧均 _cxs_agent（v2 cand / L1 对手）
    assert evidence["loader"] == {"semantics": "official-last-callable",
                                  "l1_callable": "_cxs_agent",
                                  "verbatim_callable": "_cxs_agent"}
    combos = set()
    for game in evidence["games"]:
        assert set(game) == {"seed", "cand_seat", "rewards", "statuses",
                             "winner", "margin", "elapsed_s"}
        assert game["statuses"] == ["DONE", "DONE"]
        assert game["seed"] in (101, 201) and game["cand_seat"] in (0, 1)
        combos.add((game["seed"], game["cand_seat"]))
        assert all(isinstance(r, (int, float)) and not isinstance(r, bool)
                   and math.isfinite(r) for r in game["rewards"])
        assert game["winner"] in ("cand", "opp", "tie")
        seat = game["cand_seat"]
        assert game["margin"] == pytest.approx(
            game["rewards"][seat] - game["rewards"][1 - seat])
    assert combos == {(101, 0), (101, 1), (201, 0), (201, 1)}
    # 裁决一致性：rate/passed 与台账汇总结论同源
    wins = evidence["cand_wins"]
    losses = evidence["opp_wins"]
    decided = wins + losses
    assert result["wins"] == wins
    assert result["rate"] == (round(wins / decided, 4) if decided else 0.0)
    assert result["passed"] is (
        evidence["all_done"] and result["rate"] >= gate.WIN_RATE_THRESHOLD)
    # 主台账件增记参考面摘要（skipped 形态）
    assert evidence["ref_face"]["skipped"] is True
