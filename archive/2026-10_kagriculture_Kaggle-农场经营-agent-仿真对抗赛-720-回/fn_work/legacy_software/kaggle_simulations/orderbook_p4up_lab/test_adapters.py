# -*- coding: utf-8 -*-
"""test_adapters —— 回放 blob 入口（t+1 对齐/世界/价格/棋盘）与 feats-band 入口判例。"""
import json
import os
import tempfile

from orderbook_p4up_lab import adapters as A


def _obs(money0=0, money1=0, prices=None, tiles0=None, farmer0=None,
         hands0=None, shops=None):
    farm0 = {"money": money0, "tiles": tiles0 if tiles0 is not None
             else [[None] * 10 for _ in range(10)],
             "farmer": farmer0 or [0, 0], "hands": hands0 or []}
    farm1 = {"money": money1, "tiles": [[None] * 10 for _ in range(10)],
             "farmer": [9, 9], "hands": []}
    obs = {"farms": [farm0, farm1],
           "market": {"prices": prices or {}}, "day": 0}
    if shops is not None:
        obs["town"] = {"unlocked_shops": shops}
    return obs


def make_blob(n_steps=720):
    steps = []
    for t in range(n_steps):
        a0 = {"farmer": [f"F{t}"], "hands": [], "market": []}
        a1 = {"farmer": [f"G{t}"], "hands": [], "market": []}
        steps.append({0: {"action": a0, "observation": _obs(money0=t, money1=2 * t),
                          "reward": None},
                      1: {"action": a1, "observation": _obs(money0=t, money1=2 * t),
                          "reward": None}})
    # 世界层：t=150 前两店（短 blob 无此层）
    if n_steps > 150:
        steps[150][0]["observation"]["town"] = {"unlocked_shops": ["PET_CAFE", "FARMERS_MARKET"]}
    # 末步 reward → margin
    steps[-1][0]["reward"] = 1000.0
    steps[-1][1]["reward"] = 900.0
    return {"info": {"TeamNames": ["ALPHA", "BETA"], "EpisodeId": 777, "seed": 42},
            "steps": steps}


class TestReplayToRecord:
    def test_turn_shift_and_streams(self):
        blob = make_blob()
        r = A.replay_to_record(blob, episode=777, seat=0)
        # 拍 t 的动作存 steps[t+1]（cell 40）
        assert r.stream[0]["farmer"] == ["F1"]
        assert r.stream[5]["farmer"] == ["F6"]
        assert r.opp_stream[5]["farmer"] == ["G6"]
        assert len(r.stream) == 719 and len(r.opp_stream) == 719

    def test_world_money_prices(self):
        blob = make_blob()
        r = A.replay_to_record(blob, episode=777, seat=0)
        assert r.world == "PET_CAFE__FARMERS_MARKET"
        assert r.money_me[10] == 10 and r.money_op[10] == 20
        assert r.prices_t is not None and len(r.prices_t) == 720

    def test_margin_from_last_reward(self):
        blob = make_blob()
        r0 = A.replay_to_record(blob, episode=777, seat=0)
        r1 = A.replay_to_record(blob, episode=777, seat=1)
        assert r0.margin == 100.0 and r1.margin == -100.0
        assert r0.team == "ALPHA" and r1.team == "BETA"
        assert r0.opp == "BETA" and r1.opp == "ALPHA"

    def test_board_grids(self):
        blob = make_blob()
        tiles = [[None] * 10 for _ in range(10)]
        tiles[2][3] = {"crop": "WHEAT"}          # 有物格
        tiles[4][4] = "LOCKED"                   # 锁格不计
        blob["steps"][5][0]["observation"]["farms"][0]["tiles"] = tiles
        blob["steps"][5][0]["observation"]["farms"][0]["farmer"] = [3, 2]   # (x,y)
        blob["steps"][5][0]["observation"]["farms"][0]["hands"] = [[4, 4]]
        r = A.replay_to_record(blob, episode=777, seat=0)
        assert r.occ[2][3] >= 1                  # (y=2,x=3)
        assert r.occ[4][4] == 0                  # LOCKED 不计有物
        # unlocked 逐拍非 LOCKED 格 +1：第 5 拍该格 LOCKED → 少计 1
        assert r.unlocked[2][3] == 720 and r.unlocked[4][4] == 719
        assert r.pres[2][3] >= 1                 # farmer (3,2) → pres[2][3]
        assert r.pres[4][4] >= 1                 # hand (4,4)

    def test_short_blob_truncates(self):
        blob = make_blob(n_steps=50)
        r = A.replay_to_record(blob, episode=1, seat=0)
        assert len(r.stream) == 49
        assert r.world is None                   # 无 t=150 → 无世界键


class TestFeatsRow:
    ROW = {
        "src": "replays_2026-08-09.parquet", "episode_id": 91458068,
        "date": "2026-08-09", "teams": ["T1", "T2"], "seed": 5,
        "rewards": [100.0, 90.0], "n_steps": 720,
        "players": [
            {"team": "T1", "pi": 0, "reward": 100.0,
             "day0_24": [[["PASS"], []],
                         [["PICKUP", "COW", "F1"], ["SELL:WOOL:2", "HIRE:-:-"]]]},
            {"team": "T2", "pi": 1, "reward": 90.0,
             "day0_24": [[["PASS"], []], [["PASS"], []]]},
        ],
    }

    def test_two_seat_records(self):
        recs = A.feats_row_to_records(self.ROW)
        assert len(recs) == 2
        r0, r1 = recs
        assert (r0.team, r0.opp, r0.margin) == ("T1", "T2", 10.0)
        assert (r1.team, r1.opp, r1.margin) == ("T2", "T1", -10.0)
        assert r0.window == 24 and len(r0.stream) == 24

    def test_token_parsing(self):
        r0 = A.feats_row_to_records(self.ROW)[0]
        turn1 = r0.stream[1]
        assert turn1["farmer"] == ["PICKUP", "COW", "F1"]
        assert turn1["hands"] == []              # feats 入口无 hands 通道
        assert turn1["market"] == [["SELL", "WOOL", "2"], ["HIRE"]]

    def test_lossy_notes(self):
        r0 = A.feats_row_to_records(self.ROW)[0]
        assert any("hands" in n for n in r0.lossy_notes)
        assert any("桶化" in n for n in r0.lossy_notes)
        assert any("盲区" in n for n in r0.lossy_notes)

    def test_short_day0_padded_with_pass(self):
        row = json.loads(json.dumps(self.ROW))
        row["players"][0]["day0_24"] = [[["PASS"], []]]
        r0 = A.feats_row_to_records(row)[0]
        assert r0.stream[1]["farmer"] == ["PASS"]


class TestCompactJsonl:
    def test_roundtrip(self):
        blob = make_blob(n_steps=30)
        recs = [A.replay_to_record(blob, episode=1, seat=0)]
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "recs.jsonl")
            A.save_records_jsonl(recs, p)
            back = A.load_records_jsonl(p)
        assert len(back) == 1 and back[0].episode == 1
        assert back[0].stream == recs[0].stream
        assert back[0].occ == recs[0].occ
