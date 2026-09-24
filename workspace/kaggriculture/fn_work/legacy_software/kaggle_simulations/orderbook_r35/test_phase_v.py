# -*- coding: utf-8 -*-
"""R17 测试面：phase_v（羊链路/番茄门扫描/路由表三件）。"""
import json
import os

import pytest

from orderbook_r35 import phase_v as pv


# ---------------------------------------------------------------------------
# 夹具：合成最小回放（steps[t][seat]{action, observation}）
# ---------------------------------------------------------------------------
def _sheep_tile(fert=True):
    return {"kind": "PASTURE", "animal": "SHEEP", "fed_today": True,
            "fertilizer_available": fert, "yield_units": 0}


def _wheat_tile(units, fertilized_day=-1):
    return {"kind": "PLANT", "crop": "WHEAT", "yield_units": units,
            "fertilized_until_day": fertilized_day, "watered_today": True}


def _obs(step, tiles=None, money=1000.0, wheat_px=30.0, wheat_inv=9989,
         farmer=(0, 0), shops=None):
    opp_farm = {"farmer": list(farmer), "hands": [], "money": money,
                "tiles": [[None] * 10 for _ in range(10)]}
    for (x, y), tile in (tiles or {}).items():
        opp_farm["tiles"][y][x] = tile
    if shops is None:
        shops = ["YARN_STORE", "BAKERY"] if step >= 144 else []
    return {"step": step, "day": step // 24, "hour": step % 24,
            "farms": [{"farmer": [0, 0], "hands": [], "tiles": []}, opp_farm],
            "market": {"prices": {"WHEAT": wheat_px, "WOOL": 250, "FERTILIZER": 30},
                       "inventory": {"WHEAT": wheat_inv}},
            "town": {"unlocked_shops": shops},
            }


def _step(action0, action1, obs):
    return [{"action": action0, "observation": obs},
            {"action": action1, "observation": dict(obs)}]


def _mini_replay(steps, rewards=(100.0, 200.0), names=("renyxin", "rival"),
                 episode=424242):
    return {"info": {"TeamNames": list(names), "EpisodeId": episode},
            "rewards": list(rewards), "steps": steps}


PASS_ACTION = {"farmer": ["PASS"], "market": []}


def _phase(steps, t, action, tiles, farmer, market=None, wheat_px=30.0):
    """一相动作流：先垫一步 PASS+相 obs（回放 obs[t] 为 t 后状态，动作 a_t
    的落点 obs 在 t-1——垫步保证相首动作也读到相 tile），再发 N 个动作。"""
    steps.append(_step(PASS_ACTION, PASS_ACTION,
                       _obs(t, tiles=tiles, farmer=farmer, wheat_px=wheat_px)))
    steps.append(_step(PASS_ACTION,
                       dict(action, market=market if market is not None
                            else action.get("market", [])),
                       _obs(t + 1, tiles=tiles, farmer=farmer,
                            wheat_px=wheat_px)))
    return steps


def _sheep_chain_steps(collects=22, fertilizes=10, wheat_px=30.0):
    """闭环形态动作流：收肥(肥可用羊格)→麦施→双麦收(施4/未施2)→FEED。"""
    sheep = {(x, 5): _sheep_tile(fert=True) for x in range(2, 5)}
    steps = [_step(PASS_ACTION, PASS_ACTION, _obs(0))]
    for _ in range(collects):
        _phase(steps, len(steps), {"farmer": ["COLLECT_FERTILIZER"]},
               dict(sheep), (2, 5))
    for _ in range(fertilizes):
        _phase(steps, len(steps), {"farmer": ["FERTILIZE"]},
               {**sheep, (2, 2): _wheat_tile(4, 99)}, (2, 2))
    _phase(steps, len(steps), {"farmer": ["HARVEST"]},
           {**sheep, (2, 2): _wheat_tile(4, 99)}, (2, 2),
           market=[["SELL", "WOOL", 100]])
    _phase(steps, len(steps), {"farmer": ["HARVEST"]},
           {**sheep, (3, 2): _wheat_tile(2)}, (3, 2))
    for _ in range(3):
        _phase(steps, len(steps), {"farmer": ["FEED"]}, dict(sheep), (2, 5),
               market=[["BUY_PRODUCT", "WHEAT", 1]], wheat_px=wheat_px)
    steps.append(_step(PASS_ACTION, PASS_ACTION, _obs(len(steps))))
    return steps


def test_dissect_loop_closed():
    m = pv._dissect_one_sheep_game(_mini_replay(_sheep_chain_steps()))
    assert m["collect_fertilizer_actions"] == 22
    assert m["fert_collected_units"] == 22
    assert m["fertilize_on_wheat"] == 10
    assert m["wheat_harvest_fert_units"] == 4
    assert m["wheat_harvest_unfert_units"] == 2
    assert m["feed_on_sheep"] == 3
    assert m["fert_yield_lift"] == pytest.approx(2.0)
    assert m["loop_closed"] is True


def test_dissect_loop_broken():
    steps = [_step(PASS_ACTION, PASS_ACTION, _obs(0))]
    for t in range(1, 8):
        steps.append(_step(PASS_ACTION, {"farmer": ["WATER"], "market": []},
                           _obs(t, tiles={(2, 5): _sheep_tile()})))
    m = pv._dissect_one_sheep_game(_mini_replay(steps))
    assert m["loop_closed"] is False
    assert m["criteria"]["fert_factory"] is False


def test_dissect_feed_economics_broken():
    """羊毛收入为零而麦购大——经济性臂红。"""
    steps = _sheep_chain_steps()
    for st in steps:                                   # 抹掉 SELL WOOL
        st[1]["action"]["market"] = []
    m = pv._dissect_one_sheep_game(_mini_replay(steps))
    assert m["criteria"]["feed_economics"] is False
    assert m["loop_closed"] is False


def test_probe_sheep_paths_injected(tmp_path, monkeypatch):
    def make(ep, closed):
        steps = _sheep_chain_steps() if closed else [
            _step(PASS_ACTION, PASS_ACTION, _obs(0))]
        path = tmp_path / f"episode-{ep}-replay.json"
        path.write_text(json.dumps(_mini_replay(steps, episode=ep)))
        return path

    paths = [make(ep, closed=(ep <= 3)) for ep in (1, 2, 3, 4)]
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))
    res = pv.probe_sheep_fertilizer_loop(replay_paths=paths, write_evidence=True)
    assert res["n_games"] == 4 and res["n_loop_closed"] == 3
    assert res["adopt"] is True and res["params"] == {"sheep_buy": 8}
    assert os.path.isfile(res["evidence_path"])
    res2 = pv.probe_sheep_fertilizer_loop(replay_paths=paths[:2])
    assert res2["adopt"] is False


# ---------------------------------------------------------------------------
# 番茄门扫描
# ---------------------------------------------------------------------------
R34A_FIXTURE = """CROP_MIN_PRICE=70


def _v219_qualifies(obs):
    farm = obs['farm']
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    return True


def _cxd_agent(observation, configuration=None):
    return {'farmer': ['PASS']}
"""


def test_tomato_variant_text_unique_and_exact():
    text = pv._tomato_variant_text(R34A_FIXTURE, 90, 9000)
    assert "CROP_MIN_PRICE=90" in text and "CROP_MIN_PRICE=70" not in text
    assert "farm['money'] < 9000 or" in text and "< 12000 or" not in text
    ns = pv._exec_namespace(text, "fixture")
    assert ns["CROP_MIN_PRICE"] == 90
    assert callable(ns["_cxd_agent"])
    with pytest.raises(pv.PhaseVError):
        pv._tomato_variant_text("CROP_MIN_PRICE=70\n", 90, 9000)


def _tagged_callable_factory():
    orig = pv._callable_from_text

    def from_text_with_tag(text, tag):
        fn = orig(text, tag)
        fn.variant_tag = tag
        return fn

    return orig, from_text_with_tag


def test_scan_tomato_orchestration(tmp_path, monkeypatch):
    main_path = tmp_path / "main.py"
    main_path.write_text(R34A_FIXTURE)
    games = []
    base_margin = {101: -500.0, 102: -300.0, 103: 400.0}
    for ep, res in ((101, "L"), (102, "L"), (103, "W")):
        rp = tmp_path / f"episode-{ep}-replay.json"
        rp.write_text(json.dumps(_mini_replay([_step(PASS_ACTION, PASS_ACTION,
                                                      _obs(0))], episode=ep)))
        games.append({"episode": ep, "seat": 0, "res": res,
                      "margin": base_margin[ep], "path": str(rp)})
    effect = {(90, 9000): {101: +120.0, 102: +80.0, 103: +10.0}}
    orig, tagged = _tagged_callable_factory()

    def fake_driver(replay, fn, seat):
        ep = replay["info"]["EpisodeId"]
        tag = getattr(fn, "variant_tag", "")
        if tag == "r34a_baseline":
            return {"margin": base_margin[ep], "status": "DONE"}
        price = money = None
        for part in tag.split("_"):
            if part.startswith("p") and part[1:].isdigit():
                price = int(part[1:])
            if part.startswith("m") and part[1:].isdigit():
                money = int(part[1:])
        delta = (effect.get((price, money)) or {}).get(ep, 0.0)
        return {"margin": base_margin[ep] + delta, "status": "DONE"}

    monkeypatch.setattr(pv, "_callable_from_text", tagged)
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))
    res = pv.scan_tomato_gate({"games": games}, str(main_path),
                              replay_driver=fake_driver, write_evidence=True)
    assert res["grid"]["n_points"] == 42
    assert len(res["refine"]["results"]) >= 1
    assert res["adopt"] is True
    assert (res["best"]["price"], res["best"]["money"]) == (90, 9000)
    assert res["best"]["delta_median"] == 80.0
    assert res["params"] == {"CROP_MIN_PRICE": 90, "money_gate": 9000}
    assert os.path.isfile(res["evidence_path"])

    effect.clear()                                   # 全零 Δ → 无胜者
    res2 = pv.scan_tomato_gate({"games": games}, str(main_path),
                               replay_driver=fake_driver)
    assert res2["adopt"] is False and res2["params"] is None


def test_scan_tomato_win_flip_blocks_adoption(tmp_path, monkeypatch):
    main_path = tmp_path / "main.py"
    main_path.write_text(R34A_FIXTURE)
    games = []
    base_margin = {201: -500.0, 202: 400.0}
    for ep, res in ((201, "L"), (202, "W")):
        rp = tmp_path / f"episode-{ep}-replay.json"
        rp.write_text(json.dumps(_mini_replay([_step(PASS_ACTION, PASS_ACTION,
                                                      _obs(0))], episode=ep)))
        games.append({"episode": ep, "seat": 0, "res": res,
                      "margin": base_margin[ep], "path": str(rp)})
    orig, tagged = _tagged_callable_factory()

    def driver(replay, fn, seat):
        ep = replay["info"]["EpisodeId"]
        if getattr(fn, "variant_tag", "") == "r34a_baseline":
            return {"margin": base_margin[ep], "status": "DONE"}
        return {"margin": base_margin[ep] + (300.0 if ep == 201 else -900.0),
                "status": "DONE"}

    monkeypatch.setattr(pv, "_callable_from_text", tagged)
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))
    res = pv.scan_tomato_gate({"games": games}, str(main_path),
                              replay_driver=driver)
    assert res["adopt"] is False


# ---------------------------------------------------------------------------
# 路由表
# ---------------------------------------------------------------------------
def _route_replay(ep, rkey, shops2, win):
    obs2 = _obs(2, money=rkey[0], wheat_inv=rkey[1])
    steps = [_step(PASS_ACTION, PASS_ACTION, obs2)]
    for t in range(1, 150):
        steps.append(_step(PASS_ACTION, PASS_ACTION, _obs(t, shops=shops2)))
    rewards = (300.0, 100.0) if win else (100.0, 300.0)
    return _mini_replay(steps, rewards=rewards, episode=ep)


def test_game_fingerprint_and_route_chosen():
    fp = pv._game_fingerprint(_route_replay(500, (900.0, 9989),
                                            ("YARN_STORE", "BAKERY"), win=False))
    assert fp["rkey"] == (900.0, 9989)
    assert fp["shops2"] == ("YARN_STORE", "BAKERY")
    assert fp["res"] == "L"
    tables = {"_R108_SHOP_ROUTES": {("BAKERY", "PET_CAFE"): 5},
              "_R110_OLD_SHOPS": {("YARN_STORE", "BAKERY"): 3},
              "_V92_TABLE": {("YARN_STORE", "BAKERY"): 9},
              "_V93_ROUTE_BY_RIVAL": {(229.0, 9989): 128}}
    assert pv._route_chosen(tables, ("YARN_STORE", "BAKERY"), (900.0, 9989)) == 9
    assert pv._route_chosen(tables, ("YARN_STORE", "BAKERY"), (229.0, 9989)) == 128
    assert pv._route_chosen(tables, ("BAKERY", "PET_CAFE"), (900.0, 9989)) == 5
    assert pv._route_chosen(tables, None, None) is None


R34A_ROUTE_FIXTURE = """_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128}


def _cxd_agent(observation, configuration=None):
    return {'farmer': ['PASS']}
"""

TABLES = {"_R108_SHOP_ROUTES": {("BAKERY", "PET_CAFE"): 5},
          "_R110_OLD_SHOPS": {("YARN_STORE", "BAKERY"): 3},
          "_V92_TABLE": {("YARN_STORE", "BAKERY"): 9},
          "_V93_ROUTE_BY_RIVAL": {(229.0, 9989): 128}}


def _route_corpus(tmp_path, ep0):
    """指纹语料：rkey (900.0,9989) 在 YARN 世两败（默认 9）+ 非 YARN 两胜（5）。"""
    games = []
    specs = [((900.0, 9989), ("YARN_STORE", "BAKERY"), False),
             ((900.0, 9989), ("YARN_STORE", "BAKERY"), False),
             ((900.0, 9989), ("BAKERY", "PET_CAFE"), True),
             ((900.0, 9989), ("BAKERY", "PET_CAFE"), True),
             ((700.0, 9989), ("YARN_STORE", "BAKERY"), True)]
    for i, (rkey, shops2, win) in enumerate(specs):
        ep = ep0 + i
        games.append({"episode": ep, "res": "W" if win else "L", "seat": 0,
                      "margin": 200.0 if win else -200.0,
                      "opp_animals_end": {}})
        (tmp_path / f"episode-{ep}-replay.json").write_text(
            json.dumps(_route_replay(ep, rkey, shops2, win)))
    return games


def test_expand_route_table_flow(tmp_path, monkeypatch):
    main_path = tmp_path / "main.py"
    main_path.write_text(R34A_ROUTE_FIXTURE)
    games = _route_corpus(tmp_path, 300)
    monkeypatch.setattr(pv, "_load_audit_games", lambda: games)
    monkeypatch.setattr(pv, "_replay_path",
                        lambda d, e: str(tmp_path / f"episode-{e}-replay.json"))
    orig, tagged = _tagged_callable_factory()
    monkeypatch.setattr(pv, "_callable_from_text", tagged)
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))

    def driver(replay, fn, seat):
        ep = replay["info"]["EpisodeId"]
        tag = getattr(fn, "variant_tag", "")
        if tag == "r34a_route_baseline":
            return {"margin": -100.0, "status": "DONE"}
        if "r34a_route_variant" in tag and ep in (301, 302):
            return {"margin": -50.0, "status": "DONE"}
        return {"margin": -100.0, "status": "DONE"}

    res = pv.expand_route_table(route_table=TABLES, r34a_main_path=str(main_path),
                                replay_driver=driver, write_evidence=True)
    assert [c["rkey"] for c in res["candidates"]] == [(900.0, 9989)]
    assert res["adopt"] is True
    assert res["params"]["_V93_ROUTE_BY_RIVAL"] == {"(900.0, 9989)": 5}
    assert all(g["delta"] >= pv.ROUTE_DELTA_TOL
               for g in res["replay_verification"]["per_game"])
    assert os.path.isfile(res["evidence_path"])


def test_expand_route_table_regression_drop(tmp_path, monkeypatch):
    main_path = tmp_path / "main.py"
    main_path.write_text(R34A_ROUTE_FIXTURE)
    games = _route_corpus(tmp_path, 400)
    monkeypatch.setattr(pv, "_load_audit_games", lambda: games)
    monkeypatch.setattr(pv, "_replay_path",
                        lambda d, e: str(tmp_path / f"episode-{e}-replay.json"))
    orig, tagged = _tagged_callable_factory()
    monkeypatch.setattr(pv, "_callable_from_text", tagged)
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))

    def driver(replay, fn, seat):
        if getattr(fn, "variant_tag", "") == "r34a_route_baseline":
            return {"margin": -100.0, "status": "DONE"}
        return {"margin": -400.0, "status": "DONE"}      # 扩表一律翻负

    res = pv.expand_route_table(route_table=TABLES, r34a_main_path=str(main_path),
                                replay_driver=driver)
    assert res["adopt"] is False and res["adopted_entries"] == []


def test_phase_v_adjudicate_aggregates(tmp_path, monkeypatch):
    monkeypatch.setattr(pv, "EVIDENCE_DIR", str(tmp_path / "ev"))
    monkeypatch.setattr(pv, "probe_sheep_fertilizer_loop",
                        lambda: {"adopt": True, "params": {"sheep_buy": 8},
                                 "evidence_path": "a.json"})
    monkeypatch.setattr(pv, "scan_tomato_gate",
                        lambda c, m: {"adopt": False, "params": None,
                                      "evidence_path": "b.json"})

    def boom(corpus, route_table, r34a_main_path=None):
        raise RuntimeError("route down")
    monkeypatch.setattr(pv, "expand_route_table", boom)
    res = pv.phase_v_adjudicate()
    assert res["sheep"]["adopt"] is True
    assert res["tomato"]["adopt"] is False
    assert res["route"]["adopt"] is False
    assert len(res["errors"]) == 1
    assert os.path.isfile(res["evidence_path"])
