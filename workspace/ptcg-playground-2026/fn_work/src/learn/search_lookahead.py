"""搜索前瞻 v0(fna-022/fna-010):引擎 search API rollout 行动选优。

设计(借鉴 ronniepiku/bot/search.py 的贪心折叠 MDP 思路,Apache-2.0):
- 只在我方决策点分支(优先 MAIN ctx=0),强制子选择与对手回合用贪心策略折叠;
- 每个候选项:search_begin(确定化)→ 走我方这步 → 贪心 rollout 到"我方再决策/终局/步数帽";
- 叶子=奖赏竞速状态评估(档案 §二 J 数学+W/R 有效伤害);异常/超预算=回退贪心。
- 隐藏信息预测 v0:基础怪+能量填充(数量对齐);对手模型后续用 meta 牌组换。

实测(2026-10-06):单次 12 步 rollout ≈1ms;活局内搜索与本地对局引擎共存无冲突。
"""
from __future__ import annotations

import copy
import time

from learn import cg_search

_FILL_P, _FILL_E = 89, 3  # Grookey(基础怪) / Basic {W} 能量
_STEP_CAP = 12
_TIME_CAP_S = 1.2  # 单次决策搜索总预算


def _fill(n):
    return [_FILL_P] + [_FILL_E] * max(0, int(n or 0) - 1)


def _pick(sel: dict) -> list[int]:
    opts = sel.get("option") or []
    mc = int(sel.get("maxCount") or 0)
    mn = int(sel.get("minCount") or 0)
    if not opts:
        return []
    k = max(mn, min(mc if mc > 0 else 1, len(opts)))
    return list(range(k))


def _pick_greedy(sel: dict, my_seat: int) -> list[int]:
    """折叠策略:能攻击就攻击(对己方/对方同律),否则守 min/max 取前排。"""
    opts = sel.get("option") or []
    mc = int(sel.get("maxCount") or 0)
    mn = int(sel.get("minCount") or 0)
    if not opts:
        return []
    k = max(mn, min(mc if mc > 0 else 1, len(opts)))
    atk = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("attackId") is not None]
    if atk:
        return atk[:k]
    return list(range(k))


def _card(cid):
    from learn.bc_policy_v4 import _card as _c
    return _c(cid)


def _eff_damage(base, my_card, opp_card):
    from learn.bc_policy_v4 import eff_damage
    return eff_damage(base, my_card, opp_card)


def _attacks_of(card):
    from learn.bc_policy_v4 import load_db
    _, attacks = load_db()
    out = []
    for aid in ((card or {}).get("attacks") or []):
        a = attacks.get(aid)
        if a:
            out.append(a)
    return out


def state_value(obs: dict, my_i: int) -> float:
    """叶子状态价值(我方视角):奖赏竞速为主轴,血量差+一击威胁为辅。"""
    cur = obs.get("current") or {}
    players = cur.get("players") or []
    my = players[my_i] if len(players) > my_i else {}
    opp = players[1 - my_i] if len(players) > 1 - my_i else {}
    res = cur.get("result")
    if isinstance(res, int) and res >= 0:
        return 1000.0 if res == my_i else -1000.0
    prize_adv = len(my.get("prize") or []) - len(opp.get("prize") or [])  # prize=已拿走的奖赏(开局 0)
    my_a = (my.get("active") or [None])[0] or {}
    opp_a = (opp.get("active") or [None])[0] or {}
    my_hp = (my_a.get("hp") or 0) / 380.0
    opp_hp = (opp_a.get("hp") or 0) / 380.0
    my_c, opp_c = _card(my_a.get("id")), _card(opp_a.get("id"))

    def threat(atk_card, def_card, def_p):
        t = 0.0
        for a in _attacks_of(atk_card):
            eff = _eff_damage(a.get("damage") or 0, atk_card, def_card)
            if eff >= (def_p.get("hp") or 0) > 0:
                t = max(t, 1.0)
        return t

    my_shot = threat(my_c, opp_c, opp_a)
    opp_shot = threat(opp_c, my_c, my_a)
    fatigue = ((my.get("deckCount") or 0) - (opp.get("deckCount") or 0)) / 60.0
    return 10.0 * prize_adv + 2.0 * (my_hp - opp_hp) + 3.0 * (my_shot - opp_shot) + 0.5 * fatigue


def choose_with_search(obs: dict, deck: list[int], context: int = 0) -> list[int]:
    """在当前选择点用 rollout 选优;任何失败回退贪心。仅对给定 context 启用搜索。"""
    sel = (obs or {}).get("select") or {}
    if sel.get("context") != context:
        return _pick(sel)
    opts = sel.get("option") or []
    if not opts:
        return []
    mc = int(sel.get("maxCount") or 0)
    mn = int(sel.get("minCount") or 0)
    k = max(mn, min(mc if mc > 0 else 1, len(opts)))
    cur = obs.get("current") or {}
    my_i = cur.get("yourIndex", 0) or 0
    players = cur.get("players") or []
    my = players[my_i] if len(players) > my_i else {}
    opp = players[1 - my_i] if len(players) > 1 - my_i else {}
    preds = dict(
        your_deck=_fill(my.get("deckCount") or 0),
        your_prize=_fill(len(my.get("prize") or [])),
        opponent_deck=_fill(opp.get("deckCount") or 0),
        opponent_prize=_fill(len(opp.get("prize") or [])),
        opponent_hand=_fill(opp.get("handCount") or 0),
        opponent_active=[],
    )
    t0 = time.time()
    best_score, best = None, None
    # 多选(maxCount>1)v0 只按贪心;搜索用于单选决策点
    if k != 1:
        return _pick(sel)
    for i in range(len(opts)):
        if time.time() - t0 > _TIME_CAP_S:
            break
        try:
            st = cg_search.search_begin(copy.deepcopy(obs), **preds)
            sid = st["searchId"]
            s = cg_search.search_step(sid, [i])
            n = 0
            while n < _STEP_CAP:
                o = s["observation"]
                nxt = o.get("select")
                cur2 = o.get("current") or {}
                if nxt is None or (isinstance(cur2.get("result"), int) and cur2["result"] >= 0):
                    break
                # 轮到我方决策才停;敌方回合/强制选择继续折叠
                # (敌我凭 current.yourIndex 判——搜索态里它随换手翻转)
                if nxt.get("context") == context and cur2.get("yourIndex") == my_i:
                    break
                s = cg_search.search_step(sid, _pick_greedy(nxt, my_i))
                n += 1
            v = state_value(s["observation"], my_i)
            cg_search.search_release(sid)
            if best_score is None or v > best_score:
                best_score, best = v, i
        except Exception:
            continue
    if best is None:
        return _pick(sel)
    return [best]


def make_search_agent(deck: list[int], context: int = 0):
    def agent(obs, config=None):
        sel = (obs or {}).get("select")
        if sel is None:
            return list(deck)
        return choose_with_search(obs, deck, context=context)
    return agent
