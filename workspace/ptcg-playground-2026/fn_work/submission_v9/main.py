"""PTCG v9：ES 整定的状态评估 agent（奖赏竞速骨架）——引擎深读档案战略翻译落地"""
import json, os

_DIR = os.path.dirname(os.path.abspath(__file__))
_CARDS = json.load(open(os.path.join(_DIR, "cards.json")))
_ATTACKS = json.load(open(os.path.join(_DIR, "attacks.json")))
W = {"oneshot": 6.0, "damage": -0.04321081733107528, "covered": 0.8, "attach_progress": 2.0, "evolve": 1.5, "play": 0.9, "retreat_penalty": -1.2, "retreat_escape": 1.4189445683853914, "end": 0.0}

DEFAULT_DECK = [721, 721, 722, 722, 722, 722, 723, 723, 723, 723, 1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219, 1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262, 1262] + [3] * 33

def _card(cid):
    return _CARDS.get(str(cid)) if isinstance(cid, int) else None

def _pv(c):
    return 2.0 if (c and c.get("ex")) else 1.0

def _eff(atk, my_c, opp_c):
    if not atk:
        return 0
    d = atk.get("d") or 0
    if opp_c and my_c and opp_c.get("wt") is not None and opp_c.get("wt") == my_c.get("pt"):
        d *= 2
    return d

def agent(obs, config=None):
    sel = (obs or {}).get("select")
    if sel is None:
        return list(DEFAULT_DECK)
    opts = sel.get("option") or []
    mc = int(sel.get("maxCount") or 0)
    mn = int(sel.get("minCount") or 0)
    if not opts or mc <= 0:
        return []
    if sel.get("context") != 0:
        k = max(mn, min(1, mc)) if mn <= 1 else mn
        return list(range(min(k, len(opts))))
    cur = obs.get("current") or {}
    my_i = cur.get("yourIndex", 0) or 0
    players = cur.get("players") or []
    my = players[my_i] if len(players) > my_i else {}
    opp = players[1 - my_i] if len(players) > 1 - my_i else {}
    my_active = (my.get("active") or [None])[0]
    opp_active = (opp.get("active") or [None])[0]
    opp_card = _card(opp_active.get("id")) if isinstance(opp_active, dict) else None
    my_card = _card(my_active.get("id")) if isinstance(my_active, dict) else None
    doomed = 0.0
    if isinstance(opp_active, dict) and isinstance(my_active, dict):
        my_hp = my_active.get("hp") or 999
        for aid in (opp_card.get("at") or []):
            a = _ATTACKS.get(str(aid))
            if a and len(opp_active.get("energies") or []) >= len(a.get("e") or []) and _eff(a, opp_card, my_card) >= my_hp:
                doomed = 1.0
                break
    scores = []
    for o in opts:
        if not isinstance(o, dict):
            scores.append(0.0); continue
        t = o.get("type"); s = 0.0
        if t == 13:
            a = _ATTACKS.get(str(o.get("attackId")))
            cost = len(a.get("e") or []) if a else 0
            have = len(my_active.get("energies") or []) if isinstance(my_active, dict) else 0
            if have >= cost:
                eff = _eff(a, my_card, opp_card)
                opp_hp = (opp_active.get("hp") or 0) if isinstance(opp_active, dict) else 0
                s += W["covered"]
                if eff >= opp_hp > 0:
                    s += W["oneshot"] * _pv(opp_card)
                s += W["damage"] * eff / 100.0
            else:
                s -= 2.0
        elif t == 8: s += W["attach_progress"]
        elif t == 9: s += W["evolve"]
        elif t in (7, 10, 15): s += W["play"]
        elif t == 12: s += W["retreat_penalty"] + (W["retreat_escape"] if doomed else 0.0)
        elif t == 14: s += W["end"]
        elif t == 11: s -= 0.5
        elif t == 1: s += 0.2
        elif t == 2: s -= 0.2
        scores.append(s)
    order = sorted(range(len(opts)), key=lambda i: -scores[i])
    out = order[:mc]
    if mn > 0:
        out = (out[:max(mn, min(len(out), mc))] + [i for i in range(len(opts)) if i not in out])[:mc]
    return out
