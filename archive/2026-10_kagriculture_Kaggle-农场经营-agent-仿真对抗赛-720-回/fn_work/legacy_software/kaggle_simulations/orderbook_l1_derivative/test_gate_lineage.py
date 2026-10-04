"""test_gate_lineage（R10 门②验收）：①真跑 1 局结构断言 ②合成裁决单测 ③fail-closed。

24 局全量（三对手×8）留给门编排（verify_layer_s_gates），本文件只做接线冒烟：
真跑恰 1 局 vs v48 纯件（seed 101 单席 ~4s），断言结构与内部一致性、不断言胜负。
"""

import json
import os

import pytest

import gate_lineage_strength as gls

_HERE = os.path.dirname(os.path.abspath(__file__))
_SW = os.path.dirname(os.path.dirname(_HERE))  # legacy_software
_L1_MAIN = os.path.join(_HERE, "main.py")
_V48_PURE = os.path.join(_SW, "kaggle_simulations", "opponents", "v48_main.py")

_GAME_KEYS = {"seed", "cand_seat", "rewards", "statuses", "winner", "margin",
              "elapsed_s"}
_SUMMARY_KEYS = {"n", "wins", "losses", "ties", "all_done", "per_game"}


def _done_game(winner, seed=101, cand_seat=0):
    """合成一局正常 DONE 局（winner∈cand/opp/tie，margin 与符号自洽）。"""
    base = 90000.0
    margin = {"cand": 3000.0, "opp": -3000.0, "tie": 0.0}[winner]
    rewards = [base + margin, base] if cand_seat == 0 else [base, base + margin]
    return {"seed": seed, "cand_seat": cand_seat, "rewards": rewards,
            "statuses": ["DONE", "DONE"], "winner": winner, "margin": margin,
            "elapsed_s": 4.0}


# ---- ① 真跑 1 局 vs v48 纯件：结构 + 内部一致性（不断言胜负） ----


def test_one_real_game_vs_v48_pure_structure():
    # 装载语义先决：门走官方 last-callable，对 L1 取 _cxs_agent（层 S 运行时入口），
    # 而非具名 agent()（v55 核心，无层 D/S——round-30 gate_note 记录的分歧面）。
    assert gls._load_entry(_L1_MAIN, "l1_main").__name__ == "_cxs_agent"

    # 台账护栏：run() 写固定路径 evidence——冒烟前备份既有台账（编排全量跑出的
    # 证据不被本测试覆盖丢失），冒烟后还原；测试自产台账不留盘（全量落盘是门
    # 编排的事，盘上留 1 局残账反而易被误读成门②已跑）。
    backup = None
    if os.path.isfile(gls.EVIDENCE_PATH):
        with open(gls.EVIDENCE_PATH, "rb") as fh:
            backup = fh.read()
    try:
        _assert_smoke_structure()
    finally:
        if backup is not None:
            with open(gls.EVIDENCE_PATH, "wb") as fh:
                fh.write(backup)
        elif os.path.isfile(gls.EVIDENCE_PATH):
            os.remove(gls.EVIDENCE_PATH)


def _assert_smoke_structure():
    got = gls.run(_L1_MAIN, {"v48-pure": _V48_PURE}, per_opponent_n=1)
    assert set(got) == {"per_opponent", "passed", "evidence_path"}
    assert got["evidence_path"] == gls.EVIDENCE_PATH
    assert os.path.isfile(got["evidence_path"])

    opp = got["per_opponent"]["v48-pure"]
    assert set(opp) == _SUMMARY_KEYS
    assert opp["n"] == 1 and len(opp["per_game"]) == 1
    assert opp["wins"] + opp["losses"] + opp["ties"] == 1  # 1 局恰入一类
    assert opp["all_done"] is True

    game = opp["per_game"][0]
    assert set(game) == _GAME_KEYS  # h2h 台账同款七字段，无多余键
    assert game["seed"] == 101 and game["cand_seat"] == 0
    assert game["statuses"] == ["DONE", "DONE"]
    assert game["winner"] in ("cand", "opp", "tie")
    assert isinstance(game["elapsed_s"], (int, float)) and game["elapsed_s"] > 0
    r0, r1 = game["rewards"]
    assert isinstance(r0, float) and isinstance(r1, float)
    # 裁决自洽：winner 与 margin 符号、margin 与席位序 rewards 一致
    if game["winner"] == "cand":
        assert game["margin"] == pytest.approx(r0 - r1, abs=0.1) and game["margin"] > 0
    elif game["winner"] == "opp":
        assert game["margin"] == pytest.approx(r0 - r1, abs=0.1) and game["margin"] < 0
    else:
        assert game["margin"] == 0 and r0 == r1
    # 台账落盘与内存逐字一致；门红绿与 per_game 裁决一致
    with open(got["evidence_path"], "r", encoding="utf-8") as fh:
        assert json.load(fh) == got["per_opponent"]
    assert got["passed"] == (opp["losses"] == 0 and opp["all_done"])


# ---- ② 裁决单测（合成，不碰引擎）：0 负→PASS；1 负→FAIL；平局不计负 ----


def test_adjudicate_zero_losses_passes():
    summary = gls._adjudicate([_done_game("cand"), _done_game("tie"),
                               _done_game("cand", seed=102, cand_seat=1)])
    assert summary == {"n": 3, "wins": 2, "losses": 0, "ties": 1, "all_done": True}
    assert summary["losses"] == 0 and summary["all_done"]  # 门②口径：PASS


def test_adjudicate_one_loss_fails_gate():
    summary = gls._adjudicate([_done_game("cand"), _done_game("opp"),
                               _done_game("tie")])
    assert summary["losses"] == 1 and summary["wins"] == 1 and summary["ties"] == 1
    assert not (summary["losses"] == 0 and summary["all_done"])  # 任一负局→门红


def test_adjudicate_ties_are_not_losses():
    # 平局允许：全平不失门（门②只禁负局）
    summary = gls._adjudicate([_done_game("tie"), _done_game("tie", seed=102)])
    assert summary == {"n": 2, "wins": 0, "losses": 0, "ties": 2, "all_done": True}


def test_adjudicate_abnormal_game_never_counts_as_tie():
    # 非 DONE 局/对局异常局：不进 w/l/t、不记平，all_done=False 强制门红
    abnormal = {"seed": 102, "cand_seat": 1, "rewards": None, "statuses": None,
                "winner": None, "margin": None, "elapsed_s": None,
                "error": "RuntimeError: boom"}
    summary = gls._adjudicate([_done_game("cand"), abnormal])
    assert summary == {"n": 2, "wins": 1, "losses": 0, "ties": 0, "all_done": False}
    assert not (summary["losses"] == 0 and summary["all_done"])  # fail-closed


def test_seed_seat_pairs_ladder():
    # 缺省 8 局=seeds 101-104 双席位（seed 主序、席位次序）；n 可调且阶梯扩位
    assert gls._seed_seat_pairs(1) == [(101, 0)]
    assert gls._seed_seat_pairs(8) == [(seed, seat)
                                       for seed in (101, 102, 103, 104)
                                       for seat in (0, 1)]
    assert gls._seed_seat_pairs(9)[-1] == (201, 0)  # 第 9 局进入 201 块
    assert gls._seed_seat_pairs(16)[-1] == (204, 1)  # 16 局=dev+reg 双席位


# ---- ③ fail-closed：opponents 空 / 装载失败 / 入参不可裁 → 异常 ----


def test_empty_opponents_rejected():
    with pytest.raises(gls.GateLineageError):
        gls.run(_L1_MAIN, {}, per_opponent_n=8)
    with pytest.raises(gls.GateLineageError):
        gls.run(_L1_MAIN, {"v48-pure": _V48_PURE}, per_opponent_n=0)


def test_load_failure_fail_closed():
    # L1 侧路径不存在
    with pytest.raises(gls.GateLineageError):
        gls.run("/nonexistent/l1/main.py", {"v48-pure": _V48_PURE},
                per_opponent_n=1)
    # 对手侧路径不存在
    with pytest.raises(gls.GateLineageError):
        gls.run(_L1_MAIN, {"bad": "/nonexistent/opponent.py"}, per_opponent_n=1)
    # 文件存在但无 callable 入口
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write("X = 1\n")  # 纯赋值、无 callable
        no_call = fh.name
    try:
        with pytest.raises(gls.GateLineageError):
            gls.run(_L1_MAIN, {"bad": no_call}, per_opponent_n=1)
    finally:
        os.unlink(no_call)
