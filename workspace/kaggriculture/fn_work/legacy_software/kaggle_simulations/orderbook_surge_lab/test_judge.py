# -*- coding: utf-8 -*-
"""test_judge —— 判据级裁决组（构造正/负/边界判例）。"""
from orderbook_surge_lab import judge as J

ARMS = J.ARMS


def _pb_game(ep, res, treatable, deltas, red_arm=None):
    """构造 phase_b per_game 条目：deltas={arm: (seat0Δ, seat1Δ)}。"""
    arms = {}
    for s in (0, 1):
        seat = arms[f"seat{s}"] = {"surge_days": [1], "control":
                                   {"margin": 0.0}}
        for arm in ARMS:
            if red_arm == arm and s == 0:
                seat[arm] = {"error": "boom", "red": True}
                continue
            d = deltas.get(arm)
            if d is None:
                seat[arm] = {"error": "absent", "red": True}
                continue
            seat[arm] = {"margin": d[s], "delta": d[s], "status": "DONE",
                         "steps_n": 719, "red": False,
                         "zerofootprint_wrapper": {"ok": True},
                         "zerofootprint_stream": {"binding_ok": True,
                                                  "first_alien_diff": None}}
    return {"episode": ep, "res": res, "treatable": treatable, "arms": arms}


def _pb_result(games):
    return {"per_game": games, "summary": {"n_games": len(games),
                                           "n_replays": 0, "n_red": 0,
                                           "budget_stopped": False}}


def _pa_report(games):
    return {"per_game": [{"episode": g["episode"], "res": g["res"],
                          "treatable": g["treatable"]} for g in games]}


class TestJudgeVerdicts:
    def test_positive_arm_and_overall(self):
        games = [
            _pb_game(1, "L", True, {"A1": (50.0, 30.0), "A2": (10.0, -5.0),
                                    "A3": (50.0, 30.0)}),
            _pb_game(2, "L", True, {"A1": (60.0, 40.0), "A2": (-3.0, -1.0),
                                    "A3": (60.0, 40.0)}),
            _pb_game(3, "L", True, {"A1": (55.0, 35.0), "A2": (10.0, -5.0),
                                    "A3": (70.0, 20.0)}),
            _pb_game(4, "W", False, {a: (0.0, 0.0) for a in ARMS}),
        ]
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["overall"] == "POSITIVE"
        assert out["per_arm"]["A1"]["positive"] is True
        assert out["per_arm"]["A1"]["n_sig"] == 3
        assert out["per_arm"]["A1"]["n_pos"] == 3
        assert out["per_arm"]["A2"]["positive"] is False   # 0/3 局为正
        assert out["per_arm"]["A2"]["n_pos"] == 0
        assert out["winning_arm"] in ("A1", "A3")
        assert not out["fail_closed"]

    def test_two_thirds_boundary_is_positive(self):
        games = [
            _pb_game(1, "L", True, {"A1": (5.0, 1.0)}),
            _pb_game(2, "L", True, {"A1": (5.0, 2.0)}),
            _pb_game(3, "L", True, {"A1": (-1.0, -2.0)}),  # 1/3 局非正
            _pb_game(4, "W", False, {"A1": (-90.0, 0.0)}),  # 无害带内
        ]
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["per_arm"]["A1"]["positive"] is True   # 2/3 恰过线
        sens = out["sensitivity"]["A1"]["min_seat"]
        assert sens["d0_f23"] is True and sens["d0_f34"] is False

    def test_harm_violation_blocks(self):
        games = [
            _pb_game(1, "L", True, {"A1": (100.0, 80.0)}),
            _pb_game(2, "W", False, {"A1": (-150.0, -120.0)}),  # 跌破 -100
        ]
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["per_arm"]["A1"]["positive"] is False
        assert out["per_arm"]["A1"]["n_harm_violations"] == 1
        assert out["overall"] == "NEGATIVE"

    def test_all_negative(self):
        games = [
            _pb_game(1, "L", True, {a: (-1.0, -2.0) for a in ARMS}),
            _pb_game(2, "L", True, {a: (-3.0, -1.0) for a in ARMS}),
            _pb_game(3, "L", True, {a: (-2.0, -4.0) for a in ARMS}),
        ]
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["overall"] == "NEGATIVE"
        assert out["winning_arm"] is None
        assert all(not out["per_arm"][a]["positive"] for a in ARMS)

    def test_killed_a(self):
        out = J.judge_verdicts(_pb_result([]),
                               {"per_game": []}, killed_a=True)
        assert out["overall"] == "KILLED_A"

    def test_red_game_fail_closed(self):
        games = [
            _pb_game(1, "L", True, {"A1": (5.0, 5.0), "A2": (5.0, 5.0),
                                    "A3": (5.0, 5.0)}),
        ]
        games[0]["arms"]["seat1"] = {"error": "control failed"}
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["fail_closed"] is True
        # 数据不可用局不计显著局
        assert all(out["per_arm"][a]["n_sig"] == 0 for a in ARMS)

    def test_min_seat_aggregation_conservative(self):
        # 席位不一致（一正一负）→ 局级 min<0 不计正局
        games = [_pb_game(1, "L", True, {"A1": (100.0, -20.0)})]
        out = J.judge_verdicts(_pb_result(games), _pa_report(games))
        assert out["per_arm"]["A1"]["n_pos"] == 0
        assert out["per_arm"]["A1"]["sig_delta_median"] == -20.0
