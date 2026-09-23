"""test_gate_h2h（R10 门①）：互胜率口径、fail-closed、装载身份断言与真跑。

真跑只覆盖 4 局（seeds (101,201) 双席位）控制耗时且台账落 tmp（evidence_path
覆写，不写真 evidence/）；16 局全量留给门编排 verify_layer_s_gates。真跑不断言
胜负，只断言结构/DONE/数值型与裁决逻辑一致性。装载身份断言（评审 P0 修复面）：
末 callable 名不符即 GateH2HError"装载身份不符"，绝不开打。
"""

import json
import math
import os

import pytest

import gate_h2h_vs_verbatim as gate

HERE = os.path.dirname(os.path.abspath(__file__))
L1_MAIN = os.path.join(HERE, "main.py")
VERBATIM_MAIN = os.path.abspath(
    os.path.join(HERE, os.pardir, "orderbook_derivative", "main.py"))


def _synth(seed, cand_seat, winner, statuses=("DONE", "DONE")):
    """合成一局 per_game 条目：cand 胜 margin=+10，负=−10，tie=0。"""
    if winner == "cand":
        cand_r, opp_r = 105.0, 95.0
    elif winner == "opp":
        cand_r, opp_r = 95.0, 105.0
    else:
        cand_r = opp_r = 100.0
    rewards = [0.0, 0.0]
    rewards[cand_seat], rewards[1 - cand_seat] = cand_r, opp_r
    return {
        "seed": seed, "cand_seat": cand_seat, "rewards": rewards,
        "statuses": list(statuses),
        "winner": winner if list(statuses) == ["DONE", "DONE"] else None,
        "margin": cand_r - opp_r, "elapsed_s": 0.1,
    }


# ---- ② 互胜率口径单测（合成 per_game，不跑引擎） ----

def test_rate_9w6l1t_passes_at_0_6():
    games = ([_synth(101, i % 2, "cand") for i in range(9)]
             + [_synth(102, i % 2, "opp") for i in range(6)]
             + [_synth(103, 0, "tie")])
    s = gate._summarize(games)
    assert (s["n"], s["wins"], s["losses"], s["ties"]) == (16, 9, 6, 1)
    assert s["rate"] == 0.6  # 9/(9+6)，tie 不计分母
    assert s["all_done"] is True
    assert s["passed"] is True
    assert s["seat_wins"] == {0: 5, 1: 4}  # i%2 席位交替


def test_rate_8w8l_fails_at_0_5():
    games = ([_synth(101, i % 2, "cand") for i in range(8)]
             + [_synth(102, i % 2, "opp") for i in range(8)])
    s = gate._summarize(games)
    assert (s["wins"], s["losses"], s["ties"]) == (8, 8, 0)
    assert s["rate"] == 0.5
    assert s["passed"] is False


# ---- ③ fail-closed：非 DONE / 全平 / 空 ----

def test_non_done_game_fails_closed():
    games = ([_synth(101, 0, "cand") for _ in range(9)]
             + [_synth(102, 1, "opp") for _ in range(6)]
             + [_synth(103, 0, "cand", statuses=("DONE", "TIMEOUT"))])
    s = gate._summarize(games)
    assert s["all_done"] is False
    assert s["passed"] is False  # 即便 9:6 也门红
    assert (s["wins"], s["losses"], s["ties"]) == (9, 6, 0)  # 非 DONE 局不计 W/L/T


def test_all_ties_fail_closed_with_zero_rate():
    s = gate._summarize([_synth(101, 0, "tie"), _synth(101, 1, "tie")])
    assert s["ties"] == 2 and s["wins"] == 0 and s["losses"] == 0
    assert s["rate"] == 0.0  # 无决胜局：分母为零按 0.0（fail-closed）
    assert s["passed"] is False


def test_empty_leads_fail_closed():
    s = gate._summarize([])
    assert s["n"] == 0 and s["rate"] == 0.0 and s["passed"] is False


# ---- ④ 装载身份断言（评审 P0 修复面；合成假 main，不跑引擎） ----

@pytest.mark.parametrize("slot", ["l1", "verbatim"])
def test_loader_identity_mismatch_fails_closed(tmp_path, slot):
    # 假 main 文件末尾 callable 名不符（l1 想要 _cxs_agent / verbatim 想要
    # _cxd_agent）→ GateH2HError"装载身份不符"，fail-closed 不开打。
    bad = tmp_path / "bad_main.py"
    bad.write_text("def _wrong_name_agent(obs):\n    return {}\n",
                   encoding="utf-8")
    good_l1 = tmp_path / "good_l1.py"
    good_l1.write_text("def _cxs_agent(obs):\n    return {}\n",
                       encoding="utf-8")
    good_vb = tmp_path / "good_vb.py"
    good_vb.write_text("def _cxd_agent(obs):\n    return {}\n",
                       encoding="utf-8")
    args = ((str(bad), str(good_vb)) if slot == "l1"
            else (str(good_l1), str(bad)))
    with pytest.raises(gate.GateH2HError, match="装载身份不符"):
        gate.run(args[0], args[1], seeds=(101,),
                 evidence_path=str(tmp_path / "h2h_ev.json"))
    assert not (tmp_path / "h2h_ev.json").exists()   # 未开打即未落台账


def test_loader_missing_file_fails_closed(tmp_path):
    with pytest.raises(gate.GateH2HError, match="装载失败"):
        gate.run(str(tmp_path / "nope.py"), VERBATIM_MAIN, seeds=(101,),
                 evidence_path=str(tmp_path / "h2h_ev.json"))


# ---- ① 真跑 2 seeds × 双席位（4 局，~15s；台账落 tmp） ----

def test_run_real_seeds_101_201_both_seats(tmp_path):
    ev_file = tmp_path / "h2h_evidence.json"
    result = gate.run(L1_MAIN, VERBATIM_MAIN, seeds=(101, 201),
                      evidence_path=str(ev_file))
    assert set(result) == {"n", "wins", "losses", "ties", "rate", "passed",
                           "per_game", "evidence_path"}
    assert result["n"] == 4 == len(result["per_game"])
    combos = set()
    for g in result["per_game"]:
        assert set(g) == {"seed", "cand_seat", "rewards", "statuses",
                          "winner", "margin", "elapsed_s"}
        assert g["seed"] in (101, 201)
        assert g["cand_seat"] in (0, 1)
        combos.add((g["seed"], g["cand_seat"]))
        assert g["statuses"] == ["DONE", "DONE"]
        assert len(g["rewards"]) == 2
        assert all(isinstance(r, (int, float)) and not isinstance(r, bool)
                   and math.isfinite(r) for r in g["rewards"])
        assert g["winner"] in ("cand", "opp", "tie")
        seat = g["cand_seat"]
        assert g["margin"] == pytest.approx(g["rewards"][seat] - g["rewards"][1 - seat])
        assert isinstance(g["elapsed_s"], (int, float)) and g["elapsed_s"] > 0
    assert combos == {(101, 0), (101, 1), (201, 0), (201, 1)}
    assert result["wins"] + result["losses"] + result["ties"] == 4
    decided = result["wins"] + result["losses"]
    expected_rate = round(result["wins"] / decided, 4) if decided else 0.0
    assert result["rate"] == expected_rate
    assert result["passed"] is (expected_rate >= gate.WIN_RATE_THRESHOLD)

    # 台账：落点契约（tmp 覆写，不写真 evidence/）+ 汇总字段与返回一致
    # （round-30 字段名沿用的 ofN=每席位局数）+ 装载身份留痕
    assert result["evidence_path"] == str(ev_file)
    assert ev_file.is_file()
    with open(result["evidence_path"], encoding="utf-8") as fh:
        ev = json.load(fh)
    assert ev["n_games"] == 4 and len(ev["games"]) == 4
    assert ev["cand_wins"] == result["wins"]
    assert ev["opp_wins"] == result["losses"]
    assert ev["ties"] == result["ties"]
    assert ev["all_done"] is True
    assert ev["rate"] == result["rate"]
    assert ev["passed"] == result["passed"]
    assert ev["win_rate_threshold"] == gate.WIN_RATE_THRESHOLD
    assert ev["loader"] == {"semantics": "official-last-callable",
                            "l1_callable": "_cxs_agent",
                            "verbatim_callable": "_cxd_agent"}
    assert (ev["cand_wins_seatA(of2)"] + ev["cand_wins_seatB(of2)"]
            == result["wins"])
    assert ev["mean_margin"] == pytest.approx(
        round(sum(g["margin"] for g in result["per_game"]) / 4, 1))
