# -*- coding: utf-8 -*-
"""test_divergence —— leoprovorov D(t)/K(t)/p_q 金值判例（含 cell 11 例题）。"""
from orderbook_p4up_lab import divergence as D


def act(verb):
    return {"farmer": [verb], "hands": [], "market": []}


class TestDivergenceCurve:
    def test_cell11_worked_example(self):
        # 五局同拍：3×X、1×Y、1×Z → D=1-3/5=0.4、K=3（cell 11 数学区例题）
        X, Y, Z = act("HARVEST"), act("CARE"), act("WATER")
        curve = D.divergence_curve([[X], [X], [X], [Y], [Z]])
        assert curve[0]["D"] == 0.4 and curve[0]["K"] == 3 and curve[0]["n"] == 5

    def test_all_same_zero(self):
        curve = D.divergence_curve([[act("CARE")], [act("CARE")]])
        assert curve[0]["D"] == 0.0 and curve[0]["K"] == 1

    def test_bundle_collapses_moves_and_qty(self):
        a = {"farmer": ["NORTH"], "hands": [], "market": [["SELL", "WOOL", 6]]}
        b = {"farmer": ["WEST"], "hands": [], "market": [["SELL", "WOOL", 60]]}
        curve = D.divergence_curve([[a], [b]])
        assert curve[0]["D"] == 0.0   # MOVE 并类 + 数量丢弃 → 同 bundle


class TestPSteps:
    def test_p_quantiles(self):
        # t<5 全同（D=0）；t=5 起 s3 脱轨（3-1 分裂 D=0.25）；t=10 起四局四样（D=0.75）
        base = act("HARVEST")
        s1 = [base] * 20
        s2 = [base] * 10 + [act("WATER")] * 10
        s3 = [base] * 5 + [act("CARE")] * 15
        s4 = [base] * 10 + [act("DIG")] * 10
        curve = D.divergence_curve([s1, s2, s3, s4])
        ps = D.p_steps(curve)
        assert ps["p10"] == 5          # D(5)=0.25 > 0.10
        assert ps["p25"] == 10         # D=0.25 不算 >0.25（严格大于）；t=10 起 0.75
        assert ps["p50"] == 10

    def test_never_exceeds_is_none(self):
        curve = D.divergence_curve([[act("A")], [act("A")]])
        ps = D.p_steps(curve)
        assert ps == {"p10": None, "p25": None, "p50": None}

    def test_strict_greater_than(self):
        # D=0.25 恰好不触发 q=0.25
        s = [[act("A")], [act("A")], [act("A")], [act("B")]]
        curve = D.divergence_curve(s)
        assert curve[0]["D"] == 0.25
        assert D.p_steps(curve)["p25"] is None


class TestTapeProfile:
    def test_profile_fields_and_windows(self):
        s1 = [act("A")] * 144 + [act("A")] * 24
        s2 = [act("A")] * 144 + [act("B")] * 24
        prof = D.tape_profile([s1, s2], label="unit")
        assert prof["label"] == "unit" and prof["n_games"] == 2
        assert prof["p10"] == 144 and prof["p25"] == 144
        assert prof["p50"] is None                 # D=0.5 不 > 0.5（严格大于）
        assert prof["mean_D_d0_71"] == 0.0
        assert prof["mean_D_d72_143"] == 0.0
        assert "leoprovorov" in prof["bundle_caliber"]

    def test_window_mean(self):
        curve = [{"t": t, "n": 2, "D": 0.2 if t < 72 else 0.4, "K": 2}
                 for t in range(144)]
        assert D.window_mean_D(curve, 0, 72) == 0.2
        assert D.window_mean_D(curve, 72, 144) == 0.4
        assert D.window_mean_D(curve, 200, 300) is None
