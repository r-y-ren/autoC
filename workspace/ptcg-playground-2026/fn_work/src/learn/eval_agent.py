"""状态评估型 agent（fna-006）：奖赏差期望为通货的评分骨架，权重=可整定旋钮（ES 候选）

引擎深读战略翻译（docs/methodology/engine-deep-parse.md）：
- KO=奖赏竞速（普通1/ex2）；一击线>期望伤害；能量附着 1/回合=输出节奏；retreat=节奏成本
"""
from __future__ import annotations

import json

_CARDS = None
_ATTACKS = None

# 默认旋钮（v0 拍脑袋初值——ES 整定对象；血统：档案 §七 战略翻译，样本=0，置信=低）
W = {
    "oneshot": 6.0,       # 本回合一击线（奖赏直接到手）
    "damage": 1.2,        # 伤害进度
    "covered": 0.8,       # 能量已够
    "attach_progress": 2.0,  # 附着推进攻击就绪
    "evolve": 1.5,        # 进化（HP/伤害跃迁）
    "play": 0.9,          # 打出训练家/特性
    "retreat_penalty": -1.2,
    "retreat_escape": 2.5,   # 濒死逃脱
    "end": 0.0,
}


def load_db():
    global _CARDS, _ATTACKS
    if _CARDS is None:
        _CARDS = {c["cardId"]: c for c in json.load(open("references/engine/cabt-cards.json"))}
        _ATTACKS = {a["attackId"]: a for a in json.load(open("references/engine/cabt-attacks.json"))}


def _card(cid):
    load_db()
    return _CARDS.get(cid) if isinstance(cid, int) else None


def _prize_value(card):
    if not card:
        return 1.0
    return 2.0 if (card.get("ex") or card.get("megaEx")) else 1.0


def _effective_damage(attack, my_card, opp_card):
    if not attack:
        return 0
    dmg = attack.get("damage") or 0
    if opp_card and my_card and opp_card.get("weakness") is not None \
            and opp_card.get("weakness") == my_card.get("pokemonType"):
        dmg *= 2
    return dmg


def make_agent(weights=None, deck=None):
    Wt = dict(W)
    if weights:
        Wt.update(weights)
    if deck is None:
        from kaggle_environments.envs.cabt import cabt
        deck = list(cabt.deck)

    def agent(obs, config=None):
        sel = (obs or {}).get("select")
        if sel is None:
            return list(deck)
        opts = sel.get("option") or []
        mc = int(sel.get("maxCount") or 0)
        mn = int(sel.get("minCount") or 0)
        if not opts or mc <= 0:
            return []
        if sel.get("context") != 0:  # 非 MAIN：效果分辨率，保守取前 mn..mc
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

        # 我方主动位濒死判定（对手可一击）
        doomed = 0.0
        if isinstance(opp_active, dict) and isinstance(my_active, dict):
            my_hp = my_active.get("hp") or 999
            for aid in (opp_card.get("attacks") or []):
                a = _ATTACKS.get(aid)
                if not a:
                    continue
                cost = len(a.get("energies") or [])
                have = len(opp_active.get("energies") or [])
                if have >= cost and _effective_damage(a, opp_card, my_card) >= my_hp:
                    doomed = 1.0
                    break

        scores = []
        for i, o in enumerate(opts):
            if not isinstance(o, dict):
                scores.append(0.0)
                continue
            t = o.get("type")
            s = 0.0
            if t == 13:  # ATTACK
                a = _ATTACKS.get(o.get("attackId"))
                cost = len(a.get("energies") or []) if a else 0
                have = len(my_active.get("energies") or []) if isinstance(my_active, dict) else 0
                covered = have >= cost
                eff = _effective_damage(a, my_card, opp_card)
                opp_hp = (opp_active.get("hp") or 0) if isinstance(opp_active, dict) else 0
                if covered:
                    s += Wt["covered"]
                    if eff >= opp_hp > 0:
                        s += Wt["oneshot"] * _prize_value(opp_card)
                    s += Wt["damage"] * eff / 100.0
                else:
                    s -= 2.0  # 能量不够硬打=浪费输出位（引擎会禁？ATTACK 不应出现）——防御
            elif t == 8:  # ATTACH（目标=area/index 指的宝可梦）
                s += Wt["attach_progress"]
            elif t == 9:  # EVOLVE
                s += Wt["evolve"]
            elif t in (7, 10, 15):  # PLAY/ABILITY/SKILL
                s += Wt["play"]
            elif t == 12:  # RETREAT
                s += Wt["retreat_penalty"] + (Wt["retreat_escape"] if doomed else 0.0)
            elif t == 14:  # END
                s += Wt["end"]
            elif t == 11:  # DISCARD（代价）
                s -= 0.5
            elif t in (1, 2):  # YES/NO
                s += 0.2 if t == 1 else -0.2
            scores.append(s)

        order = sorted(range(len(opts)), key=lambda i: -scores[i])
        k = mc
        out = order[:k]
        return out[:mc] if mn <= 0 else (out[:max(mn, min(len(out), mc))] + [i for i in range(len(opts)) if i not in out])[:mc]

    return agent
