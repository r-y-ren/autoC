# -*- coding: utf-8 -*-
"""R15 单测：judge_mix（正/负/KILLED 判例+敏感度）。"""
import pytest

from orderbook_mix_lab import judge_mix as J


def _game(ep, res, d0=None, d1=None, red=False):
    seats = {}
    if d0 is not None:
        seats["seat0"] = {"delta": d0}
    if d1 is not None:
        seats["seat1"] = {"delta": d1}
    deltas = [v for v in (d0, d1) if v is not None]
    return str(ep), {"res": res, "seats": seats,
                     "game_delta": min(deltas) if deltas else None,
                     "red": red}


def _openloop(per_variant):
    return {"per_variant": per_variant, "summary": {}}


def test_positive_path_with_closedloop():
    games = dict([_game(1, "L", 100, 50), _game(2, "L", 10),
                  _game(3, "L", 30, 20), _game(4, "W", 5)])
    ol = _openloop({"vA": {"games": games}})
    cl = {"per_variant": {"vA": {"rate": 0.75, "median_margin": 40.0,
                                 "wins": 3, "runs": 4, "red_runs": 0}}}
    out = J.judge_mix_verdicts(ol, cl)
    v = out["per_variant"]["vA"]
    assert v["openloop_positive"] is True
    assert v["n_flip"] == 3 and v["n_loss"] == 3
    assert v["loss_delta_median"] == 20     # min 席位 [50,10,20] 的中位
    assert v["variant_positive"] is True
    assert out["overall"] == "POSITIVE" and out["winning_variant"] == "vA"


def test_openloop_positive_but_closedloop_negative():
    games = dict([_game(1, "L", 100, 50), _game(2, "L", 10),
                  _game(3, "L", 30, 20), _game(4, "W", 5)])
    ol = _openloop({"vA": {"games": games}})
    cl = {"per_variant": {"vA": {"rate": 0.25, "median_margin": -40.0,
                                 "wins": 1, "runs": 4, "red_runs": 0}}}
    out = J.judge_mix_verdicts(ol, cl)
    assert out["per_variant"]["vA"]["openloop_positive"] is True
    assert out["per_variant"]["vA"]["variant_positive"] is False
    assert out["overall"] == "NEGATIVE"


def test_negative_paths():
    # ① 翻正不足 2/3；② 胜局违例 3（>2）；③ 中位 ≤0
    g1 = dict([_game(1, "L", 100), _game(2, "L", -10), _game(3, "L", 5),
               _game(4, "L", -20), _game(5, "W", 1)])   # 2/4 翻正
    g2 = dict([_game(5, "L", 100), _game(6, "L", 100), _game(7, "L", 100),
               _game(8, "W", -150), _game(9, "W", -200), _game(10, "W", -120)])
    g3 = dict([_game(11, "L", 100), _game(12, "L", -50), _game(13, "L", -60),
               _game(14, "W", 0)])
    ol = _openloop({"v1": {"games": g1}, "v2": {"games": g2},
                    "v3": {"games": g3}})
    out = J.judge_mix_verdicts(ol, None)
    assert out["per_variant"]["v1"]["openloop_positive"] is False  # 2/4 翻正
    assert out["per_variant"]["v2"]["openloop_positive"] is False  # 违例 3
    assert out["per_variant"]["v3"]["openloop_positive"] is False  # 中位 -50
    assert out["overall"] == "NEGATIVE" and out["winning_variant"] is None


def test_killed_passthrough_and_sensitivity():
    # 3/5 翻正（100,80,20,-5,-8）：2/3 门不过、3/5 门过（敏感度分辨面）
    games = dict([_game(1, "L", 100), _game(2, "L", 80), _game(3, "L", 20),
                  _game(4, "L", -5), _game(5, "L", -8), _game(6, "W", 3)])
    ol = _openloop({"vA": {"games": games}})
    out = J.judge_mix_verdicts(ol, None, killed=True)
    assert out["overall"] == "KILLED"
    s = out["sensitivity"]["vA"]
    assert set(s["min_seat"]) == {"f23_median", "f35_median", "f23_mean"}
    assert s["min_seat"]["f23_median"] is False  # 3×3=9 < 5×2=10
    assert s["min_seat"]["f35_median"] is True   # 3×5=15 ≥ 5×3=15
    assert s["min_seat"]["f23_mean"] is False


def test_fail_closed_on_red_and_empty():
    ol = _openloop({"vA": {"games": dict([_game(1, "L", 100, red=True)])}})
    out = J.judge_mix_verdicts(ol, None)
    assert out["fail_closed"] is True
    out2 = J.judge_mix_verdicts(_openloop({}), None)
    assert out2["overall"] == "NEGATIVE"   # 无变体数据=全败
