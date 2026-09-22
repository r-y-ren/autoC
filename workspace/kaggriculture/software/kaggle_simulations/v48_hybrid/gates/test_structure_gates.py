# -*- coding: utf-8 -*-
"""structure_gates 真实测试（R9-G3）。

覆盖面（tmp 小样语料/合成序列，不依赖 /tmp/r26full、不装载真实 v6b/v48 包）：
1) 语料扫描与三线选取规则（巨人=锚局+强对手扩展轮转；回归=最窄 W 局；
   经济面=普通对手按 ep 升序且与回归集不相交）；
2) 收入曲线口径（步级正增量按日求和、d14-17 窗峰、窗外峰不计入）；
3) seated 管线金标准：磁带跟随注入 → 终局与回放 rewards 逐位一致；
4) 逐线判据接线（巨人 ok 阈、回归容差、经济门）与裁决 fail-closed。
"""
from __future__ import annotations

import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc                      # noqa: E402
import structure_gates as sg                  # noqa: E402

PASS_ACT = {"farmer": ["PASS"], "hands": [], "market": []}
BUY_ACT = {"farmer": ["PASS"], "hands": [],
           "market": [["BUY_PRODUCT", "WHEAT", 2]]}


def _pass_agent(obs):
    return json.loads(json.dumps(PASS_ACT))


def _buy_agent(obs):
    return json.loads(json.dumps(BUY_ACT))


def _tapes_and_replay(seed, seat_fns, steps=72):
    """短季孪生自打（最小投影形态回放 + 双席动作磁带 + 终局）。"""
    from kaggle_simulations.agent.planner import twin
    head = gc.synthetic_season_head(seed, steps)
    state = twin.new_state_from_replay_head(head)
    replay = json.loads(json.dumps(head))
    replay["info"]["TeamNames"] = ["renyxin", "TestOpp"]
    tapes = [[], []]
    taken = 0
    while not state.env.done and taken < steps:
        pair = []
        for seat, fn in enumerate(seat_fns):
            action = json.loads(json.dumps(
                fn(state.seats[seat].observation)))
            tapes[seat].append(action)
            pair.append(action)
        twin.step(state, pair)
        replay["steps"].append([{"action": pair[0]}, {"action": pair[1]}])
        taken += 1
    finals = twin.final_money(state)
    replay["rewards"] = finals
    return replay, tapes, finals


def _tape_follower(tapes, me_seat):
    def fn(obs):
        step = int(obs.get("step", 0) or 0)
        return json.loads(json.dumps(tapes[me_seat][step]))
    return fn


def _write_corpus(dirs_games):
    """dirs_games: {dir: [(ep, me_seat, opp, rewards)]} → 写回放件
    （rewards 直接落 replay["rewards"]，扫描层消费）。"""
    for d, games in dirs_games.items():
        os.makedirs(d, exist_ok=True)
        for ep, me_seat, opp, rewards in games:
            replay = gc.synthetic_season_head(7)
            replay["info"]["TeamNames"] = (
                ["renyxin", opp] if me_seat == 0 else [opp, "renyxin"])
            replay["rewards"] = list(rewards)
            with open(os.path.join(d, f"episode-{ep}-replay.json"), "w",
                      encoding="utf-8") as h:
                json.dump(replay, h, ensure_ascii=False)


def _mk_games(tmp_path):
    """迷你语料：r26/r27 两目录，含三巨人锚局+强扩展池 5 局+W 局+普通局
    +镜像局（强扩展池 5 局：statma 取 2、fuxi/42 各取 1，覆盖轮转分配）。"""
    d26 = str(tmp_path / "r26")
    d27 = str(tmp_path / "r27")
    g26 = [
        (111653327, 1, "statma", [66000.0, 30000.0]),     # 锚局 L -36k
        # 强扩展池（败局 margin≤-20k，-20k 边界含）
        (900000001, 0, "StrongA", [1000.0, 45000.0]),     # -44000
        (900000002, 0, "StrongB", [2000.0, 36000.0]),     # -34000
        (900000006, 1, "StrongE", [30000.0, 5000.0]),     # -25000
        (900000003, 0, "StrongC", [50000.0, 71000.0]),    # -21000
        (900000004, 0, "StrongD", [3000.0, 23000.0]),     # -20000（含）
        # 轻败局（不入池）
        (900000005, 0, "WeakL", [4000.0, 8000.0]),        # -4000
        # W/T 局（回归集候选按 margin 升序）
        (900000010, 0, "W1", [4000.0, 4000.0]),           # 0 → T 非 W
        (900000011, 0, "W2", [5000.0, 4900.0]),           # +100 最窄
        (900000012, 1, "W3", [4800.0, 5000.0]),           # +200
        (900000013, 0, "W4", [6000.0, 5700.0]),           # +300
        (900000014, 0, "W5", [7000.0, 6600.0]),           # +400
        (900000015, 1, "W6", [7500.0, 8000.0]),           # +500
        (900000016, 0, "W7", [9000.0, 8400.0]),           # +600
        (900000017, 0, "W8", [10000.0, 9300.0]),          # +700
        (900000018, 0, "W9", [11000.0, 10000.0]),         # +1000
        (900000019, 0, "W10", [12000.0, 10500.0]),        # +1500（回归外）
        (900000099, 0, "renyxin", [100.0, 100.0]),        # 镜像局
    ]
    g27 = [
        (111877080, 0, "fuxi", [40000.0, 67000.0]),       # 锚局 L -27k
        (111898825, 0, "42", [50000.0, 75000.0]),         # 锚局 L -25k
        (900000020, 1, "fuxi", [7000.0, 9000.0]),         # 其他对局 W +2k
        (900000021, 0, "42", [9000.0, 6500.0]),           # 其他对局 W +2.5k
        (900000030, 0, "Ord1", [8000.0, 5000.0]),         # 普通局
        (900000031, 1, "Ord2", [6000.0, 9000.0]),
        (900000032, 1, "Ord3", [9500.0, 6000.0]),
    ]
    _write_corpus({d26: g26, d27: g27})
    return d26, d27


# ---------------------------------------------------------------------------
# 1) 扫描与选取规则
# ---------------------------------------------------------------------------
def test_scan_and_selection_rules(tmp_path):
    d26, d27 = _mk_games(tmp_path)
    old, old_pool = sg.CORPUS_DIRS, sg.STRONG_EXT_POOL_FROM
    sg.CORPUS_DIRS = (d26, d27)
    sg.STRONG_EXT_POOL_FROM = d26
    try:
        games = sg.scan_corpus()
        by_ep = {g["ep"]: g for g in games}
        assert by_ep[111653327]["opp"] == "statma"
        assert by_ep[111653327]["me_seat"] == 1
        assert by_ep[111653327]["result"] == "L"
        assert by_ep[900000010]["result"] == "T"          # margin 0 → T
        assert by_ep[900000099]["mirror"] is True
        assert by_ep[900000020]["me_seat"] == 1           # 名单序换位正确

        # 强扩展池：≤-20k 入池（边界含），按严重度稳定排序
        pool_eps = [g["ep"] for g in sg.select_strong_ext_pool(games)]
        assert pool_eps == [900000001, 900000002, 900000006,
                            900000003, 900000004]

        giants = sg.select_giant_games(games)
        # statma：无其他对局 → 锚局 + pool[0:2]
        assert sorted(g["ep"] for g in giants["statma"]) == [
            111653327, 900000001, 900000002]
        # fuxi：其他对局 1 + 锚局 + pool[2:3]
        assert sorted(g["ep"] for g in giants["fuxi"]) == [
            111877080, 900000006, 900000020]
        # 42：其他对局 1 + 锚局 + pool[4:5]
        assert sorted(g["ep"] for g in giants["42"]) == [
            111898825, 900000004, 900000021]

        # 回归集：最窄 8 局 W（+100..+1000；T 局不入）
        assert [g["ep"] for g in sg.select_regression_games(games)] == [
            900000011, 900000012, 900000013, 900000014,
            900000015, 900000016, 900000017, 900000018]

        # 经济面：普通对手（剔巨人名/强扩展/镜像/回归集）按 ep 升序取 6
        econ = sg.select_economic_games(games)
        assert [g["ep"] for g in econ] == [
            900000005, 900000010, 900000019, 900000030,
            900000031, 900000032]
        assert not ({g["ep"] for g in econ}
                    & ({g["ep"] for g in sg.select_regression_games(games)}
                       | {ep for _, ep, _ in sg.GIANT_ANCHORS}))
    finally:
        sg.CORPUS_DIRS = old
        sg.STRONG_EXT_POOL_FROM = old_pool


def test_selection_fail_closed(tmp_path):
    with pytest.raises(ValueError):      # 目录缺失
        sg.scan_corpus((str(tmp_path / "nope"),))
    d = str(tmp_path / "one")
    os.makedirs(d)
    _write_corpus({d: [(900000011, 0, "W2", [5000.0, 4900.0])]})
    games = sg.scan_corpus((d,))
    with pytest.raises(ValueError):      # W 局不足 8
        sg.select_regression_games(games)
    with pytest.raises(ValueError):      # 巨人锚局缺失
        sg.select_giant_games(games)


# ---------------------------------------------------------------------------
# 2) 收入曲线口径
# ---------------------------------------------------------------------------
def test_income_curve_positive_delta_only():
    # 步级序列（24 步/日）：d0 买（负增量不计）、d1 卖 +500 伴买 -100
    # （只计 +500）、d2 持平
    series = [3000.0] * (3 * 24 + 1)
    for i in range(1, 25):        # d0 内买入 -100（维持到日末）
        series[i] = 2900.0
    series[25] = 3400.0           # d1 内卖出 +500
    for i in range(26, len(series)):
        series[i] = 3300.0        # d1 内买入 -100（维持）
    inc = sg._income_curve(series, n_days=5)
    assert inc == [0.0, 500.0, 0.0, 0.0, 0.0]


def test_income_peak_window_semantics():
    # d15 内 +900（计入窗峰），d20 +90000（窗外，不入窗峰但入季峰）
    series = [100.0] * (30 * 24 + 1)
    series[15 * 24 + 3] = 1000.0
    series[20 * 24 + 3] = 90100.0
    inc = sg._income_curve(series)
    lo, hi = sg.ECON_WINDOW
    assert max(inc[lo:hi]) == 900.0
    assert inc[20] == 90000.0
    assert inc.index(max(inc)) == 20


# ---------------------------------------------------------------------------
# 3) seated 管线金标准：磁带跟随 → 终局逐位一致
# ---------------------------------------------------------------------------
def test_seated_rollout_tape_roundtrip(tmp_path):
    replay, tapes, finals = _tapes_and_replay(
        7101, [_buy_agent, _pass_agent])
    p = str(tmp_path / "episode-990001-replay.json")
    with open(p, "w", encoding="utf-8") as h:
        json.dump(replay, h, ensure_ascii=False)
    run = sg.seated_rollout(p, 0, lambda: _tape_follower(tapes, 0),
                            track=True)
    assert run["finals"] == pytest.approx(finals)
    assert run["margin"] == pytest.approx(finals[0] - finals[1])
    assert run["steps"] == len(tapes[0])
    # 短季 72 步（3 日）：d14-17 窗内无收入日 → 窗峰=0（窗存在即取 max）
    assert run["peak_d14_17"] == 0.0
    assert "sheep_eod" in run and "income_curve" in run
    assert run["stream_sha256"]


# ---------------------------------------------------------------------------
# 4) 判据接线 + 裁决 fail-closed
# ---------------------------------------------------------------------------
def test_criteria_thresholds():
    assert (0.0 >= sg.GIANT_OK_MARGIN) is True           # 打平 ok
    assert (-1000.0 >= sg.GIANT_OK_MARGIN) is True       # 差距 1k 边界含
    assert (-1001.0 >= sg.GIANT_OK_MARGIN) is False
    assert (2500.0 - 1000.0 <= sg.REG_TOLERANCE + 1500.0)
    assert (1400.0 >= 2500.0 - sg.REG_TOLERANCE) is False  # 差 1100 不过
    assert (12700.0 >= sg.ECON_GATE) is True
    assert (12699.9 >= sg.ECON_GATE) is False


def test_giant_gate_pipeline_with_stub_loader(tmp_path):
    """小样语料 + stub 装载器：扫描→选取→rollout→判据全链（stub 对局
    回放无转移步 → 终局=初始 3000/3000、margin=0 → 逐局 ok）。"""
    d26, d27 = _mk_games(tmp_path)
    old, old_pool = sg.CORPUS_DIRS, sg.STRONG_EXT_POOL_FROM
    sg.CORPUS_DIRS = (d26, d27)
    sg.STRONG_EXT_POOL_FROM = d26
    try:
        games = sg.scan_corpus()
        _, tapes, _ = _tapes_and_replay(7102, [_pass_agent, _pass_agent])
        res = sg.run_giant_seated_gate(
            games, v6b_loader=lambda: _tape_follower(tapes, 0))
        assert set(res["per_giant"]) == {"statma", "fuxi", "42"}
        for name, v in res["per_giant"].items():
            assert v["games"] >= sg.GIANT_PER_NAME_MIN
            assert all(r["v6b_margin"] == 0.0 for r in v["records"])
        assert res["passed"] is True       # margin=0 逐局打平 → 全过
    finally:
        sg.CORPUS_DIRS = old
        sg.STRONG_EXT_POOL_FROM = old_pool


def _redirect_outputs(monkeypatch, tmp_path):
    monkeypatch.setattr(sg, "VERDICT_PATH", str(tmp_path / "verdict.json"))
    monkeypatch.setattr(sg, "LINE_OUT",
                        {k: str(tmp_path / f"{k}.json")
                         for k in sg.LINE_OUT})


def test_verdict_fail_closed(tmp_path, monkeypatch):
    """语料缺失 → seated 三线 runnable=False；整体 FAIL 且错误入 dict。"""
    _redirect_outputs(monkeypatch, tmp_path)
    monkeypatch.setattr(sg, "scan_corpus",
                        lambda *a, **k: (_ for _ in ()).throw(
                            ValueError("语料目录缺失: /tmp/nope")))
    monkeypatch.setattr(sg, "run_h2h_v48_gate", lambda *a, **k: {
        "passed": True, "games": 16, "wins": 11, "losses": 5, "ties": 0,
        "win_fraction_strict": 0.6875, "avg_margin": 0.0,
        "margin_distribution": {"pos": 11, "neg": 5, "zero": 0}})
    monkeypatch.setattr(sg, "run_fourgate_reference", lambda *a, **k: {
        "passed": True, "identity": {"identity_ok": True},
        "g2b_smoke_artifact": {"consistent": True},
        "load_recheck": {"load_ok": True, "answer_ok": True}})
    verdict = sg.verify_structure_gates()
    assert verdict["overall"] == "FAIL"
    for key in ("giants", "regression", "econ"):
        assert verdict["lines"][key]["runnable"] is False
        assert "语料目录缺失" in verdict["lines"][key]["error"]
        assert verdict["lines"][key]["passed"] is False
    assert verdict["lines"]["h2h"]["passed"] is True
    assert verdict["lines"]["fourgate"]["passed"] is True
    assert verdict["lines"]["h2h"]["summary"]["win_fraction_strict"] == 0.6875
    assert os.path.isfile(verdict["_out_path"])
    assert os.path.isfile(str(tmp_path / "h2h.json"))    # 可执行线落盘


def test_verdict_all_pass(tmp_path, monkeypatch):
    monkeypatch.setattr(sg, "scan_corpus", lambda *a, **k: [])
    stubs = {
        "run_h2h_v48_gate": {"passed": True, "games": 16, "wins": 12,
                             "losses": 4, "ties": 0,
                             "win_fraction_strict": 0.75,
                             "avg_margin": 1.0,
                             "margin_distribution": {"pos": 12, "neg": 4,
                                                     "zero": 0}},
        "run_giant_seated_gate": {"passed": True, "per_giant": {}},
        "run_win_regression_gate": {"passed": True, "games": 8, "n_ok": 8,
                                    "flipped_negative_games": []},
        "run_economic_face": {"passed": True, "games": 6,
                              "best_peak_d14_17": 13000.0},
        "run_fourgate_reference": {
            "passed": True, "identity": {"identity_ok": True},
            "g2b_smoke_artifact": {"consistent": True},
            "load_recheck": {"load_ok": True, "answer_ok": True}},
    }
    for name, stub in stubs.items():
        monkeypatch.setattr(sg, name, lambda *a, _s=stub, **k: dict(_s))
    _redirect_outputs(monkeypatch, tmp_path)
    verdict = sg.verify_structure_gates()
    assert verdict["overall"] == "PASS"
    assert all(v["passed"] for v in verdict["lines"].values())
    assert (verdict["lines"]["econ"]["summary"]["best_peak_d14_17"]
            == 13000.0)
    assert "yarn2_note" in verdict
