# -*- coding: utf-8 -*-
"""test_baseline —— 基线 JSON 完整性 + 分层/最近邻判例。"""
import json
import os

from orderbook_p4up_lab import baseline as B

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                    "opponents_baseline.json")


class TestBaselineData:
    def _load(self):
        with open(DATA, encoding="utf-8") as fh:
            return json.load(fh)

    def test_eleven_teams_with_hard_data(self):
        d = self._load()
        assert len(d["teams"]) == 11
        for row in d["teams"]:
            for f in ("team", "wins", "p10", "p25", "p50", "tape_tier"):
                assert f in row, f"{row.get('team')} missing {f}"
        names = [r["team"] for r in d["teams"]]
        assert "THIRD FARM CLUB" in names and "M & M & P & Q" in names

    def test_p_values_match_cell16_rows(self):
        # cell 16 ROWS 硬数据抽查（自报值必须逐字对齐）
        by = {r["team"]: r for r in self._load()["teams"]}
        assert (by["THIRD FARM CLUB"]["wins"], by["THIRD FARM CLUB"]["p10"],
                by["THIRD FARM CLUB"]["p25"], by["THIRD FARM CLUB"]["p50"]) == (88, 145, 145, 146)
        assert (by["Majkel1337"]["wins"], by["Majkel1337"]["p25"]) == (234, 4)
        assert (by["feel the agi"]["p10"], by["feel the agi"]["p25"],
                by["feel the agi"]["p50"]) == (6, 151, 151)
        assert by["M & M & P & Q"]["p25"] == 1

    def test_source_and_caliber_declared(self):
        d = self._load()
        assert d["self_reported"] is True
        src = d["source"]
        assert src["fetched"] == "2026-10-02"
        assert "leoprovorov" in src["kernel"]
        assert "cell 16" in src["cell"]
        assert "p_q_definition" in d["caliber"]
        assert d["caliber"]["shop_unlocks"] == [72, 144, 216]
        assert any("强度" in c or "strength" in c for c in d["caveats"])

    def test_published_window_means_present(self):
        d = self._load()
        wm = d["published_window_means_self_reported"]
        assert wm["THIRD FARM CLUB"] == {"d0_71": 0.004, "d72_143": 0.007}
        assert wm["Majkel1337"] == {"d0_71": 0.424, "d72_143": 0.651}


class TestTapeTier:
    def test_boundaries(self):
        assert B.tape_tier(1) == "DAY0_FIRE"
        assert B.tape_tier(4) == "DAY0_FIRE"
        assert B.tape_tier(5) == "EARLY_FORK"
        assert B.tape_tier(71) == "EARLY_FORK"
        assert B.tape_tier(72) == "SHOP1_FORK"
        assert B.tape_tier(143) == "SHOP1_FORK"
        assert B.tape_tier(144) == "SIX_DAY_TAPE"
        assert B.tape_tier(999) == "SIX_DAY_TAPE"

    def test_none(self):
        assert B.tape_tier(None) is None


class TestProfileLookup:
    def test_nearest_team(self):
        out = B.profile_lookup(145, 145, 146)
        assert out["nearest_baseline_team"]["team"] == "THIRD FARM CLUB"
        assert out["tape_tier"] == "SIX_DAY_TAPE"
        assert out["baseline_self_reported"] is True

    def test_fire_case(self):
        out = B.profile_lookup(1, 1, 2)
        assert out["tape_tier"] == "DAY0_FIRE"
        assert out["nearest_baseline_team"]["team"] == "M & M & P & Q"

    def test_no_p25(self):
        out = B.profile_lookup(None, None, None)
        assert out["tape_tier"] is None and out["nearest_baseline_team"] is None

    def test_self_check_rule_present(self):
        out = B.profile_lookup(50, 50, 50)
        assert "白花" in out["self_check_rule"] and "过刚" in out["self_check_rule"]
