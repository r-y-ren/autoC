"""终局奖赏清算求解器（算法格·第一件）——档案 §七 奖赏竞速数学的落地

纯算术前瞻（不依赖引擎状态克隆）：给定可见场面，算"这一击之后奖赏竞速谁赢"。
确定性段（双方攻击/HP/能量全可见）→ 精确解；接进评分器=终局覆盖层。
"""
from __future__ import annotations

import json

_CARDS = None
_ATTACKS = None


def load_db():
    global _CARDS, _ATTACKS
    if _CARDS is None:
        import os
        base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "references", "engine")
        _CARDS = {c["cardId"]: c for c in json.load(open(os.path.join(base, "cabt-cards.json")))}
        _ATTACKS = {a["attackId"]: a for a in json.load(open(os.path.join(base, "cabt-attacks.json")))}
    return _CARDS, _ATTACKS


def _card(cid):
    load_db()
    return _CARDS.get(cid) if isinstance(cid, int) else None


def _prize_value(card):
    return 2.0 if (card and (card.get("ex") or card.get("megaEx"))) else 1.0


def _eff_damage(attack, my_card, opp_card):
    if not attack:
        return 0
    d = attack.get("damage") or 0
    if opp_card and my_card and opp_card.get("weakness") is not None \
            and opp_card.get("weakness") == my_card.get("pokemonType"):
        d *= 2
    return d


def can_ko(attacker_pokemon, defender_pokemon):
    """攻击方能否一击打倒防守方（能量够+伤害足）"""
    if not isinstance(attacker_pokemon, dict) or not isinstance(defender_pokemon, dict):
        return False
    a_card = _card(attacker_pokemon.get("id"))
    d_card = _card(defender_pokemon.get("id"))
    if not a_card or not d_card:
        return False
    have = len(attacker_pokemon.get("energies") or [])
    hp = defender_pokemon.get("hp") or 999
    for aid in (a_card.get("attacks") or []):
        atk = _ATTACKS.get(aid)
        if not atk:
            continue
        cost = len(atk.get("energies") or [])
        if have >= cost and _eff_damage(atk, a_card, d_card) >= hp:
            return True
    return False


def race_bonus(my, opp, my_active, opp_active):
    """奖赏清算覆盖层 → 给 ATTACK 选项的加成（元组：win_now, race_edge, danger）"""
    my_prize = len(my.get("prize") or [])
    opp_prize = len(opp.get("prize") or [])
    my_card = _card(my_active.get("id")) if isinstance(my_active, dict) else None
    opp_card = _card(opp_active.get("id")) if isinstance(opp_active, dict) else None

    win_now = 0.0
    race_edge = 0.0
    danger = 0.0

    # 进攻侧：我这击 KO 且清空奖赏=当场胜利
    if isinstance(opp_active, dict) and isinstance(my_active, dict):
        if can_ko(my_active, opp_active):
            taken = _prize_value(opp_card)
            if my_prize - taken <= 0:
                win_now = 1.0
            else:
                # KO 后对手反击能力（下一手大概率用他替补/主动位打我）
                retaliation = can_ko(opp_active, my_active) or any(
                    can_ko(b, my_active) for b in (opp.get("bench") or []) if isinstance(b, dict))
                if not retaliation and my_prize - taken <= 2:
                    race_edge = 1.0   # 我先收官且他反杀不动=竞速锁定
                elif not retaliation:
                    race_edge = 0.5

    # 防守侧：他一击打倒我的主动位且这会让他清奖赏=当场输
    if isinstance(opp_active, dict) and isinstance(my_active, dict):
        if can_ko(opp_active, my_active):
            my_card_value = _prize_value(my_card)
            if opp_prize - my_card_value <= 0:
                danger = 1.0          # 我的主动位站场=送他当场胜利
            else:
                danger = 0.4          # 被 KO 亏节奏
    return win_now, race_edge, danger
