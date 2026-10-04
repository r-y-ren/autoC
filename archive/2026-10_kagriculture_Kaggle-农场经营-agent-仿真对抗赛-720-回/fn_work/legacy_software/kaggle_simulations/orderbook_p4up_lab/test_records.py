# -*- coding: utf-8 -*-
"""test_records —— 指纹/模型级判例（canon / op / bundle / EpisodeRecord 往返）。"""
from orderbook_p4up_lab import records as R


class TestCanon:
    def test_none_is_pass(self):
        assert R.canon(None) == ("PASS", (), ())
        assert R.canon({}) == ("PASS", (), ())

    def test_full_action(self):
        a = {"farmer": ["PLANT", "MELON"],
             "hands": [["MOVE", "NORTH"], ["CARE"]],
             "market": [["SELL", "WOOL", 6]]}
        assert R.canon(a) == (("PLANT", "MELON"),
                              (("MOVE", "NORTH"), ("CARE",)),
                              (("SELL", "WOOL", 6),))


class TestOp:
    def test_move_directions_collapse(self):
        for v in ("NORTH", "SOUTH", "EAST", "WEST", "MOVE"):
            assert R.op([v]) == ("MOVE", None)

    def test_good_extraction(self):
        assert R.op(["PLANT", "MELON"]) == ("PLANT", "MELON")
        assert R.op(["SELL", "WOOL", 6]) == ("SELL", "WOOL")
        assert R.op(["BUY_LAND"]) == ("BUY_LAND", None)

    def test_none_and_pass(self):
        assert R.op(None) == ("PASS", None)
        assert R.op([]) == ("PASS", None)


class TestBundle:
    def test_quantities_dropped_market_is_set(self):
        a = {"farmer": ["SELL"], "hands": [], "market": [["SELL", "WOOL", 6]]}
        b = {"farmer": ["SELL"], "hands": [], "market": [["SELL", "WOOL", 99]]}
        assert R.bundle_key(a) == R.bundle_key(b)

    def test_market_order_ignored_dup(self):
        a = {"farmer": ["CARE"], "hands": [],
             "market": [["SELL", "WOOL", 1], ["SELL", "WOOL", 1]]}
        b = {"farmer": ["CARE"], "hands": [], "market": [["SELL", "WOOL", 5]]}
        assert R.bundle_key(a) == R.bundle_key(b)

    def test_hands_sorted_and_counted(self):
        a = {"farmer": ["CARE"], "hands": [["HARVEST"], ["WATER"]], "market": []}
        b = {"farmer": ["CARE"], "hands": [["WATER"], ["HARVEST"]], "market": []}
        c = {"farmer": ["CARE"], "hands": [["HARVEST"]], "market": []}
        assert R.bundle_key(a) == R.bundle_key(b)
        assert R.bundle_key(a) != R.bundle_key(c)   # n_hands 进指纹

    def test_move_directions_collapsed(self):
        a = {"farmer": ["NORTH"], "hands": [], "market": []}
        b = {"farmer": ["WEST"], "hands": [], "market": []}
        assert R.bundle_key(a) == R.bundle_key(b)

    def test_jsonable_stable(self):
        a = {"farmer": ["PLANT", "MELON"], "hands": [], "market": [["HIRE"]]}
        assert R.bundle_key_jsonable(a) == R.bundle_key_jsonable(dict(a))


class TestEpisodeRecord:
    def test_compact_roundtrip(self):
        rec = R.EpisodeRecord(episode=42, seat=0, team="A", opp="B", margin=10.0,
                              stream=[{"farmer": ["PASS"], "hands": [], "market": []}],
                              opp_stream=[None], world="X__Y", window=None,
                              lossy_notes=["n1"])
        back = R.EpisodeRecord.from_compact(rec.to_compact())
        assert back.episode == 42 and back.world == "X__Y"
        assert back.stream == rec.stream and back.lossy_notes == ["n1"]

    def test_from_compact_drops_unknown_keys(self):
        d = {"episode": 1, "seat": 0, "team": "A", "opp": "B", "margin": 0.0,
             "stream": [], "opp_stream": [], "future_field": 9}
        back = R.EpisodeRecord.from_compact(d)
        assert not hasattr(back, "future_field")

    def test_new_grid(self):
        g = R.new_grid()
        assert len(g) == 10 and all(len(row) == 10 for row in g)
        assert sum(map(sum, g)) == 0
