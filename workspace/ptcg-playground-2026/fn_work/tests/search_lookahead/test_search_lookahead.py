"""search_lookahead v0.1 叶子增厚的语义锁定测试(状态/清场/牌库/终局折价/混乱)"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))  # references 相对路径

from learn import search_lookahead as sl


def _P(prize=0, deck=30, bench=0, hp=200, **st):
    p = {"prize": list(range(prize)), "deckCount": deck, "handCount": 5, "bench": [{}] * bench,
         "active": [{"id": 1, "hp": hp}]}
    p.update({k: bool(st.get(k, False)) for k in
              ("poisoned", "burned", "asleep", "paralyzed", "confused")})
    return p


def _obs(my, opp, result=-1, your=0):
    return {"current": {"yourIndex": your, "result": result, "players": [my, opp]}}


def test_terminal_and_prize_nonlinear():
    assert sl.state_value(_obs(_P(), _P()), 0) != 1000.0  # 未终局不给终局值
    assert sl.state_value(_obs(_P(), _P(), result=0), 0) == 1000.0
    assert sl.state_value(_obs(_P(), _P(), result=1), 0) == -1000.0
    # §5.3:中间进度相对线性打折、越接近拿完边际越高(凸)
    g = sl._prize_score
    assert g(6) - g(5) > g(1) - g(0)          # 第 6 张边际 > 第 1 张
    assert sl._W_PRIZE * g(3) < 30.0           # 3 张领先低于线性 30 分
    v_lead5 = sl.state_value(_obs(_P(prize=5), _P(prize=4)), 0)
    v_lead1 = sl.state_value(_obs(_P(prize=1), _P(prize=0)), 0)
    assert v_lead5 > 2.0 * v_lead1             # 第 5 张边际≈第 1 张的 3 倍(非线性接近胜利)


def test_status_flow_and_lock():
    neutral = sl.state_value(_obs(_P(), _P()), 0)
    opp_poison = sl.state_value(_obs(_P(), _P(poisoned=True)), 0)
    my_poison = sl.state_value(_obs(_P(poisoned=True), _P()), 0)
    assert opp_poison > neutral > my_poison     # 毒 10/回合进期望伤害流
    assert sl.state_value(_obs(_P(), _P(burned=True)), 0) > opp_poison  # 灼伤 20>毒 10
    # 睡/麻=禁攻禁撤(行动锁):锁对方加分,被锁减分
    assert sl.state_value(_obs(_P(), _P(asleep=True)), 0) > neutral
    assert sl.state_value(_obs(_P(paralyzed=True), _P()), 0) < neutral


def test_fossil_status_immune(monkeypatch):
    monkeypatch.setattr(sl, "_card", lambda cid: {"hp": 380, "pokemonType": 2})
    assert sl.state_value(_obs(_P(poisoned=True, burned=True), _P()), 0) == \
           sl.state_value(_obs(_P(), _P()), 0)  # 化石免疫状态(§6.2 简化假设)


def test_confusion_folds_into_threat(monkeypatch):
    monkeypatch.setattr(sl, "_card", lambda cid: {"hp": 380, "pokemonType": 1})
    monkeypatch.setattr(sl, "_attacks_of", lambda c: [{"damage": 999}])
    monkeypatch.setattr(sl, "_eff_damage", lambda base, a, b: 999)
    neutral = sl.state_value(_obs(_P(), _P()), 0)
    my_confused = sl.state_value(_obs(_P(confused=True), _P()), 0)
    opp_confused = sl.state_value(_obs(_P(), _P(confused=True)), 0)
    assert my_confused < neutral < opp_confused  # 我方混乱威胁打 5 折+自伤期望
    # 睡/麻禁攻→威胁 0(对方睡着打不了我)
    assert sl.state_value(_obs(_P(), _P(asleep=True)), 0) > neutral


def test_board_risk_and_deck_fatigue():
    neutral = sl.state_value(_obs(_P(), _P()), 0)
    assert sl.state_value(_obs(_P(bench=3), _P(bench=1)), 0) > neutral  # 存量差独立权重
    # 后备空+出战濒死=高危(§7.4)
    danger = sl.state_value(_obs(_P(hp=50), _P()), 0)
    safe = sl.state_value(_obs(_P(hp=300), _P()), 0)
    assert danger < safe
    assert sl.state_value(_obs(_P(bench=1, hp=50), _P()), 0) > danger + 1.0  # 有后备不触发
    # 牌库差进疲劳项(权重 2.0):余牌多者占优
    assert sl.state_value(_obs(_P(deck=50), _P(deck=10)), 0) > neutral
    assert sl.state_value(_obs(_P(deck=10), _P(deck=50)), 0) < neutral
    # 长盘衰减:我方牌库枯竭时慢转换项(如血差)折价
    lead = sl.state_value(_obs(_P(deck=50, hp=380), _P(deck=50, hp=1)), 0)
    starved = sl.state_value(_obs(_P(deck=3, hp=380), _P(deck=3, hp=1)), 0)
    assert starved < lead
