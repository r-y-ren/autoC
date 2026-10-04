# -*- coding: utf-8 -*-
"""R18 测试面：forensic（cxtb 触发法证组 + 麦簇五点扫描组）。

用合成 main（含真实锚行）+注入假 driver（按装载 tag 区分基线/变体），
不跑 twin 重演——实跑面由 CLI（S2）承载。
"""
import os

import pytest

from orderbook_tomato_forensic import build_r36 as b36
from orderbook_tomato_forensic import forensic as fx

R34A_MAIN = b36.R34A_MAIN


# ---------------------------------------------------------------------------
# 合成件
# ---------------------------------------------------------------------------
CXTB_MAIN = """
_CXTB_REPORT = {'cxtb_calls': 0, 'cxtb_opened': 0, 'cxtb_blocked': 0,
                'cxtb_errors': 0, 'cxtb_features': []}


def _cxd_agent(obs, configuration=None):
    if int(obs.get('step', -1)) == 432:
        _CXTB_REPORT['cxtb_calls'] += 1
        opened = bool(obs.get('open'))
        _CXTB_REPORT['cxtb_opened' if opened else 'cxtb_blocked'] += 1
        _CXTB_REPORT['cxtb_features'].append(
            {'opened': opened, 'base': False, 'revenue': obs.get('revenue', 0)})
    return {'farmer': ['PASS'], 'market': [], 'tag': __name__}
"""

CXTB_MAIN_DEAD = """
_CXTB_REPORT = {'cxtb_calls': 0, 'cxtb_opened': 0, 'cxtb_blocked': 0,
                'cxtb_errors': 0, 'cxtb_features': []}


def _cxd_agent(obs, configuration=None):
    return {'farmer': ['PASS'], 'market': []}
"""

WHEAT_MAIN = """
class final_price_guard(object):
    pass


final_price_guard.telemetry={"sale_price_threshold":31}
# Correctly last-bound visible-price sale guard experiment; threshold=31.


def _guard(obs, action):
    try:
        if obs.get('step') == 91:
            price = float(obs.get('price', 0))
            if price < 31:
                action = dict(action, cancelled=True)
    except Exception:
        pass
    return action


def _cxd_agent(obs, configuration=None):
    return _guard(obs, {'farmer': ['PASS'], 'market': [], 'tag': __name__})
"""


def _synth_replay(episode, seat=0, price91=30.0, margins=None, res="L"):
    rep = {"info": {"TeamNames": ["renyxin", "rival"], "EpisodeId": episode},
           "rewards": [1.0, 0.0], "steps": [], "_seat": seat,
           "_price91": price91, "_margins": margins or {}, "_res": res}
    return rep


def _install_corpus(monkeypatch, games, replays):
    """替换 phase_v 语料装载面（forensic 经 _pv 引用共享）。"""
    by_ep = {g["episode"]: g for g in games}
    monkeypatch.setattr(fx._pv, "_load_audit_games", lambda: games)
    monkeypatch.setattr(fx._pv, "_replay_path",
                        lambda rd, ep: f"synthetic:{ep}")
    def _load(path):
        ep = int(path.split(":")[1])
        return replays[ep]
    monkeypatch.setattr(fx._pv, "_load_replay", _load)
    return by_ep


# ---------------------------------------------------------------------------
# cxtb 组
# ---------------------------------------------------------------------------
def _cxtb_driver_factory(trigger=True):
    def driver(replay, agent, seat):
        obs = {"step": 432, "open": trigger, "revenue": 12000 if trigger else 4035}
        agent(obs)
        stream = [{"farmer": ["PASS"], "market":
                   [["BUY_SEED", "TOMATO", 10]]} if trigger and i == 432 else {}
                  for i in range(720)]
        if trigger:
            stream.append({"farmer": ["PASS"], "market":
                           [["SELL", "TOMATO", 80]]})
        margin = 100.0 if trigger else -50.0
        return {"margin": margin, "status": "DONE", "stream": stream}
    return driver


def test_cxtb_forensic_fires_and_face_alive(tmp_path, monkeypatch):
    games = [{"episode": 1, "seat": 0, "res": "W", "margin": 100.0},
             {"episode": 2, "seat": 0, "res": "L", "margin": -50.0}]
    replays = {1: _synth_replay(1), 2: _synth_replay(2)}
    _install_corpus(monkeypatch, games, replays)
    result = fx.forensic_cxtb_trigger(
        replay_dir=str(tmp_path), r34a_main_path=_write(tmp_path, CXTB_MAIN),
        replay_driver=_cxtb_driver_factory(trigger=True), write_evidence=False)
    assert result["face_alive"] is True
    assert result["fire_rate"] == 1.0
    assert result["fired_games"] == [1, 2]
    fired = next(e for e in result["per_game"] if e["episode"] == 1)
    assert fired["tomato_seed_buys"] == 10
    assert fired["tomato_sell_qty"] == 80
    assert result["revenue_profile"]["n_revenue_ge_9000"] == 2
    assert result["outcome_diff"]["fired"]["n"] == 2


def test_cxtb_forensic_face_dead(tmp_path, monkeypatch):
    games = [{"episode": 1, "seat": 0, "res": "W", "margin": 1.0}]
    replays = {1: _synth_replay(1)}
    _install_corpus(monkeypatch, games, replays)
    result = fx.forensic_cxtb_trigger(
        replay_dir=str(tmp_path), r34a_main_path=_write(tmp_path, CXTB_MAIN_DEAD),
        replay_driver=_cxtb_driver_factory(trigger=False), write_evidence=False)
    assert result["face_alive"] is False
    assert result["call_rate"] == 0.0
    assert result["fire_rate"] == 0.0


def test_cxtb_outcome_diff_groups(tmp_path, monkeypatch):
    games = [{"episode": i, "seat": 0,
              "res": "W" if i == 1 else "L", "margin": 0.0} for i in (1, 2, 3)]
    replays = {i: _synth_replay(i) for i in (1, 2, 3)}
    _install_corpus(monkeypatch, games, replays)

    def driver(replay, agent, seat):
        ep = replay["info"]["EpisodeId"]
        trigger = ep in (1, 2)                    # 1-2 触发、3 调而未触发
        agent({"step": 432, "open": trigger, "revenue": 9000 if trigger else 4000})
        return {"margin": 100.0 if trigger else -50.0, "status": "DONE",
                "stream": []}

    result = fx.forensic_cxtb_trigger(
        replay_dir=str(tmp_path), r34a_main_path=_write(tmp_path, CXTB_MAIN),
        replay_driver=driver, write_evidence=False)
    od = result["outcome_diff"]
    assert od["fired"]["n"] == 2 and od["fired"]["twin_margin_mean"] == 100.0
    assert od["called_not_fired"]["n"] == 1
    assert od["called_not_fired"]["twin_margin_mean"] == -50.0
    assert od["never_called"]["n"] == 0


def _write(tmp_path, text):
    p = tmp_path / "synth_main.py"
    p.write_text(text, encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# wheat 组
# ---------------------------------------------------------------------------
def test_wheat_variant_anchors_unique_on_real_r34a():
    text = open(R34A_MAIN, encoding="utf-8").read()
    assert text.count(b36.WHEAT_CODE_OLD) == 1
    assert text.count(b36.WHEAT_TELEM_OLD) == 1
    assert text.count(b36.WHEAT_COMMENT_OLD) == 1
    assert b36.apply_wheat_threshold(text, 31) == text   # 基线幂等


def _wheat_driver(replay, agent, seat):
    act = agent({"step": 91, "price": replay["_price91"]})
    tag = act["tag"]
    T = 31 if tag.endswith("baseline") else int(tag.rsplit("t", 1)[1])
    margins = replay["_margins"]
    key = str(T) if str(T) in margins else "31"
    return {"margin": margins[key], "status": "DONE",
            "stream": [None] * 91 + [{"farmer": ["PASS"], "market": []}]}


def test_wheat_scan_picks_winner_rule(tmp_path, monkeypatch):
    # 价格 30：31/34/38 触发取消卖（margin 表给 34/38 正 Δ、25/28 等于基线）；
    # 34 在一局胜局翻负 → 剔除；38 中位>0 且不翻负 → adopt。
    games = [{"episode": i, "seat": 0, "res": "W" if i == 1 else "L",
              "margin": 0.0} for i in range(1, 7)]
    replays = {}
    for g in games:
        ep = g["episode"]
        m = {"31": 100.0, "25": 100.0, "28": 100.0,
             "34": (100.0 if ep != 1 else -5.0), "38": 160.0}
        replays[ep] = _synth_replay(ep, price91=30.0, margins=m, res=g["res"])
    _install_corpus(monkeypatch, games, replays)
    corpus = {"games": [dict(g, path=f"synthetic:{g['episode']}") for g in games]}
    result = fx.scan_wheat_step91(
        corpus=corpus, r34a_main_path=_write(tmp_path, WHEAT_MAIN),
        replay_dir=str(tmp_path), replay_driver=_wheat_driver,
        write_evidence=False)
    by_t = {p["threshold"]: p for p in result["points"]}
    assert by_t[25]["delta_median"] == 0.0
    assert by_t[38]["delta_median"] == 60.0
    assert by_t[34]["win_flips_negative"] == [1]
    assert result["adopt"] is True
    assert result["best"]["threshold"] == 38
    assert result["params"] == {"threshold": 38}
    assert by_t[38]["trigger_rate"] == 1.0   # price91=30 < 38


def test_wheat_scan_all_negative_keeps_baseline(tmp_path, monkeypatch):
    games = [{"episode": i, "seat": 0, "res": "L", "margin": 0.0}
             for i in range(1, 7)]
    replays = {}
    for g in games:
        m = {"31": 100.0, "25": 90.0, "28": 95.0, "34": 70.0, "38": 60.0}
        replays[g["episode"]] = _synth_replay(g["episode"], price91=30.0,
                                              margins=m)
    _install_corpus(monkeypatch, games, replays)
    corpus = {"games": [dict(g, path=f"synthetic:{g['episode']}") for g in games]}
    result = fx.scan_wheat_step91(
        corpus=corpus, r34a_main_path=_write(tmp_path, WHEAT_MAIN),
        replay_dir=str(tmp_path), replay_driver=_wheat_driver,
        write_evidence=False)
    assert result["adopt"] is False
    assert result["best"] is None
    assert result["params"] is None


def test_adjudicate_skips_when_face_dead(tmp_path):
    result = fx.adjudicate_cxtb_variants(
        face_alive=False, write_evidence=False)
    assert result["skipped"] and "face_not_alive" in result["skipped"]
    assert result["adopt_stepped"] is False
    assert result["adopt_constants"] in (False, None)
