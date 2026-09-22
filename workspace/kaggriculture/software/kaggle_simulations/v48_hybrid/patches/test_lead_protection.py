"""test_lead_protection -- P4 补丁叶 lead_protection 的单元测试（R8 F4a）。

覆盖面（口径登记见 lead_protection.py 模块头）：
  A. estimate 用例组：直读口径（双席 money 互见，引擎探针前置事实）/
     降级代理口径（我方资金+库存估值 vs 对手资金+动物产出代理，含
     days_left 收缩）/ unobservable / error。
  B. plan 用例组：717-718 清仓窗让位（原对象 identity）/ step 不可知
     让位 / lead 门 / 非保护时点零足迹 / 拆批量帽 / 投影门（在跌任意
     时点、稳定/无投影只当日末）/ 补发线数帽 / 本帧已卖线跳过 /
     fail-safe。
  C. build 编排组：触发边界（day=24、lead=3000 等值即触发）与未触发
     （day<24 / lead<3000 / 无库存视图 / 观测垃圾 / 抛异常观测）一律
     原对象返回；触发帧补发且剧本单透传不改动；day=None 按 step 回推；
     确定性（同 obs 两次调用同输出）。

运行：python -m pytest <本文件> -q
"""

import pytest

import lead_protection as lp


# ---- 构造小件 --------------------------------------------------------------
def make_farm(money, tiles=None):
    return {"money": money, "tiles": tiles or [], "hands": [],
            "farmer": [0, 0], "unlocked_quadrants": ["NW"], "hires_today": 0}


def make_obs(step=582, player=0, me_money=50000.0, opp_money=46000.0,
             shed=None, prices=None, inventory=None, opp_tiles=None):
    """标准双席观测（形态=引擎探针实测键结构）。step=582 即 d24 h6。"""
    return {
        "step": step, "player": player,
        "farms": [make_farm(me_money), make_farm(opp_money, opp_tiles)],
        "market": {"prices": prices if prices is not None else
                   {"MELON": 250, "WHEAT": 25},
                   "inventory": inventory if inventory is not None else
                   {"MELON": 10000, "WHEAT": 10000}},
        "town": {"unlocked_shops": ["YARN_STORE"]},
        "private": {"shed": shed if shed is not None else {"MELON": 30},
                    "seeds": {}, "inventories": [{}]},
    }


# ===========================================================================
# A. estimate 用例组
# ===========================================================================
def test_estimate_direct_positive_seat0():
    est = lp.estimate_lead_margin(make_obs(), 24)
    assert est == {"lead": 4000.0, "basis": "farms_money_direct"}


def test_estimate_direct_seat1_view():
    # seat1 视角：我席=farms[1]=46000，对手=farms[0]=50000 → lead=-4000
    obs = make_obs(step=583, player=1)
    est = lp.estimate_lead_margin(obs, 24)
    assert est["basis"] == "farms_money_direct"
    assert est["lead"] == pytest.approx(-4000.0)


def test_estimate_direct_negative_lead():
    obs = make_obs(me_money=40000.0, opp_money=46000.0)
    est = lp.estimate_lead_margin(obs, 24)
    assert est["lead"] == pytest.approx(-6000.0)


def test_estimate_direct_ignores_day():
    assert (lp.estimate_lead_margin(make_obs(), 24)["lead"]
            == lp.estimate_lead_margin(make_obs(), 29)["lead"])


def test_estimate_proxy_shed_valuation():
    # 对手 money 不可读（None）→ 降级代理：me 10000 + WHEAT 10×25 − 0
    obs = make_obs(me_money=10000.0, opp_money=None, shed={"WHEAT": 10})
    est = lp.estimate_lead_margin(obs, 24)
    assert est["basis"] == "money_shed_proxy"
    assert est["lead"] == pytest.approx(10000.0 + 250.0)


def test_estimate_proxy_animal_flow_exact():
    # 对手地块 COW+SHEEP+GOOSE、day=24（days_left=6）：
    # (160/2 + 200/3 + 50/1) × 6 = 1180.0
    tiles = [[{"animal": "COW"}, {"animal": "SHEEP"}, {"animal": "GOOSE"}]]
    obs = make_obs(me_money=10000.0, opp_money=None, shed={},
                   opp_tiles=tiles)
    est = lp.estimate_lead_margin(obs, 24)
    assert est["basis"] == "money_shed_proxy"
    assert est["lead"] == pytest.approx(10000.0 - 1180.0)


def test_estimate_proxy_days_left_shrinks():
    tiles = [[{"animal": "COW"}]]
    lead24 = lp.estimate_lead_margin(
        make_obs(me_money=10000.0, opp_money=None, shed={},
                 opp_tiles=tiles), 24)["lead"]
    lead29 = lp.estimate_lead_margin(
        make_obs(me_money=10000.0, opp_money=None, shed={},
                 opp_tiles=tiles), 29)["lead"]
    assert lead24 == pytest.approx(10000.0 - 80.0 * 6)
    assert lead29 == pytest.approx(10000.0 - 80.0 * 1)
    assert lead29 > lead24


def test_estimate_unobservable_empty_obs():
    est = lp.estimate_lead_margin({}, 24)
    assert est == {"lead": None, "basis": "unobservable"}


def test_estimate_unobservable_none_obs():
    est = lp.estimate_lead_margin(None, 24)
    assert est == {"lead": None, "basis": "unobservable"}


def test_estimate_error_swallowed():
    class RaisingFarm(dict):
        def get(self, key, default=None):
            raise RuntimeError("boom")

    farm = RaisingFarm()
    farm["money"] = 1.0        # 真值非空，确保 .get 被实际触达
    obs = {"player": 0, "farms": [farm, make_farm(46000.0)]}
    est = lp.estimate_lead_margin(obs, 24)
    assert est == {"lead": None, "basis": "error"}


# ===========================================================================
# B. plan 用例组
# ===========================================================================
FALLING = {"MELON": (250.0, 240.0)}
STABLE = {"MELON": (250.0, 250.0)}


def test_plan_terminal_window_identity():
    sells = [["SELL", "MELON", 10]]
    for step in (717, 718, 719):
        assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells,
                                        4000.0, step=step) is sells


def test_plan_unknown_step_identity():
    sells = [["SELL", "MELON", 10]]
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells, 4000.0,
                                     step=None) is sells


def test_plan_lead_gate_identity():
    sells = [["SELL", "MELON", 10]]
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells, 2999.99,
                                     step=582) is sells
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells, None,
                                     step=582) is sells


def test_plan_non_protective_hour_identity():
    sells = [["SELL", "MELON", 10]]
    for hour in (5, 7, 11, 13, 17, 19, 21):
        step = 24 * 24 + hour
        assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells,
                                        4000.0, step=step) is sells


def test_plan_split_qty_cap():
    out = lp.plan_protective_sells({"MELON": 100}, FALLING, [], 4000.0,
                                   step=582)
    assert out == [["SELL", "MELON", 4]]


def test_plan_falling_emits_any_protective_hour():
    for hour in (6, 12, 18):
        step = 24 * 24 + hour
        out = lp.plan_protective_sells({"MELON": 30}, FALLING, [], 4000.0,
                                       step=step)
        assert out == [["SELL", "MELON", 4]]


def test_plan_stable_only_last_protective_hour():
    for hour in (6, 12):
        step = 24 * 24 + hour
        assert lp.plan_protective_sells({"MELON": 30}, STABLE, [], 4000.0,
                                        step=step) == []
    out = lp.plan_protective_sells({"MELON": 30}, STABLE, [], 4000.0,
                                   step=24 * 24 + 18)
    assert out == [["SELL", "MELON", 4]]


def test_plan_no_projection_treated_stable():
    assert lp.plan_protective_sells({"MELON": 30}, {}, [], 4000.0,
                                    step=582) == []
    assert lp.plan_protective_sells({"MELON": 30}, {}, [], 4000.0,
                                    step=594) == [["SELL", "MELON", 4]]


def test_plan_max_lines_and_order():
    inv = {"MELON": 30, "WHEAT": 100, "WOOL": 8, "MILK": 5, "EGG": 4,
           "CARROT": 3}
    out = lp.plan_protective_sells(inv, {}, [], 4000.0, step=594)
    # 全部按无投影=稳定线在 h18 发射；帽=4 线；序=(-qty, name)
    assert [o[1] for o in out] == ["WHEAT", "MELON", "WOOL", "MILK"]
    assert all(o[2] == 4 for o in out)


def test_plan_skips_lines_selling_now():
    sells = [["SELL", "MELON", 40]]
    out = lp.plan_protective_sells({"MELON": 30, "WHEAT": 10}, FALLING,
                                   sells, 4000.0, step=582)
    # MELON 本帧 tape 已卖 → 跳过；WHEAT 无投影=稳定 → h6 不发 → 无补发
    assert out == [["SELL", "MELON", 40]]


def test_plan_fail_safe_bad_step():
    sells = [["SELL", "MELON", 10]]
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells, 4000.0,
                                     step="abc") is sells


def test_plan_fail_safe_raising_projection():
    class RaisingProj(dict):
        def get(self, key, default=None):
            raise RuntimeError("boom")

    sells = []
    assert lp.plan_protective_sells({"MELON": 30}, RaisingProj(), sells,
                                     4000.0, step=582) is sells


# ===========================================================================
# C. build 编排组
# ===========================================================================
TAPE = [["SELL", "WHEAT", 10]]


def test_build_not_triggered_day_below_24():
    obs = make_obs(step=23 * 24 + 6)
    assert lp.build_lead_protection(obs, 23, TAPE) is TAPE


def test_build_not_triggered_lead_below_3000():
    obs = make_obs(me_money=5999.0, opp_money=3000.0)   # lead=2999
    assert lp.build_lead_protection(obs, 24, TAPE) is TAPE


def test_build_boundary_day24_lead3000_triggers():
    obs = make_obs(me_money=7000.0, opp_money=4000.0,   # lead=3000 等值
                   inventory={"MELON": 15000, "WHEAT": 10000})  # 过剩→h6 卖
    out = lp.build_lead_protection(obs, 24, TAPE)
    assert out is not TAPE
    assert out[:1] == TAPE
    assert ["SELL", "MELON", 4] in out


def test_build_boundary_day23_high_lead_identity():
    obs = make_obs(step=23 * 24 + 6)
    assert lp.build_lead_protection(obs, 23, TAPE) is TAPE


def test_build_terminal_window_identity():
    for step in (717, 718):
        obs = make_obs(step=step)
        assert lp.build_lead_protection(obs, 29, TAPE) is TAPE


def test_build_active_just_before_717():
    obs = make_obs(step=714)          # d29 h18，保护时点且 <717
    out = lp.build_lead_protection(obs, 29, TAPE)
    assert ["SELL", "MELON", 4] in out


def test_build_hour20_no_emission_identity():
    obs = make_obs(step=716)          # d29 h20 非保护时点 → 零足迹
    assert lp.build_lead_protection(obs, 29, TAPE) is TAPE


def test_build_day_none_derived_from_step():
    obs = make_obs(step=582,          # step//24 = 24
                   inventory={"MELON": 15000, "WHEAT": 10000})
    out = lp.build_lead_protection(obs, None, TAPE)
    assert ["SELL", "MELON", 4] in out


def test_build_step_unknown_identity():
    obs = make_obs(step=None)
    obs.pop("step")
    assert lp.build_lead_protection(obs, 24, TAPE) is TAPE


def test_build_no_shed_view_identity():
    obs = make_obs()
    obs["private"] = {"seeds": {}, "inventories": [{}]}
    assert lp.build_lead_protection(obs, 24, TAPE) is TAPE


def test_build_fail_safe_none_obs():
    assert lp.build_lead_protection(None, 24, TAPE) is TAPE


def test_build_fail_safe_raising_obs():
    class RaisingObs(dict):
        def get(self, key, default=None):
            raise RuntimeError("boom")

    assert lp.build_lead_protection(RaisingObs(), 24, TAPE) is TAPE


def test_build_glut_pulls_melon_to_hour6():
    # 市场过剩（MELON 库存 15000 > I0 10000）→ 投影下移 → h6 尽早卖
    obs = make_obs(step=582, inventory={"MELON": 15000, "WHEAT": 10000})
    out = lp.build_lead_protection(obs, 24, TAPE)
    assert ["SELL", "MELON", 4] in out


def test_build_balanced_market_waits_until_hour18():
    obs = make_obs(step=582, inventory={"MELON": 10000, "WHEAT": 10000})
    assert lp.build_lead_protection(obs, 24, TAPE) is TAPE   # h6 零足迹
    obs = make_obs(step=594, inventory={"MELON": 10000, "WHEAT": 10000})
    out = lp.build_lead_protection(obs, 24, TAPE)
    assert ["SELL", "MELON", 4] in out


def test_build_tape_orders_untouched_and_not_mutated():
    tape = [["SELL", "MELON", 40], ["SELL", "WHEAT", 10]]
    snapshot = [list(o) for o in tape]
    # WHEAT 本帧 tape 已卖 → 跳过；MELON 同因跳过 → 无补发=原对象
    obs = make_obs(step=582, shed={"MELON": 30, "WHEAT": 10},
                   inventory={"MELON": 15000, "WHEAT": 10000})
    assert lp.build_lead_protection(obs, 24, tape) is tape
    assert tape == snapshot


def test_build_triggered_does_not_mutate_input():
    tape = [["SELL", "WHEAT", 10]]
    snapshot = [list(o) for o in tape]
    obs = make_obs(step=582, inventory={"MELON": 15000, "WHEAT": 10000})
    out = lp.build_lead_protection(obs, 24, tape)
    assert out is not tape
    assert tape == snapshot               # 入参原对象内容不被改动
    assert out[:1] == tape and out[1] == ["SELL", "MELON", 4]


def test_build_deterministic():
    obs = make_obs(step=582, inventory={"MELON": 15000, "WHEAT": 10000})
    a = lp.build_lead_protection(obs, 24, TAPE)
    b = lp.build_lead_protection(obs, 24, TAPE)
    assert a == b
