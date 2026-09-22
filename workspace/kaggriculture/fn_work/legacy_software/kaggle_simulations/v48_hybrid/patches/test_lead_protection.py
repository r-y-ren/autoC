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


# ===========================================================================
# D. plan armed 用例组（R8-v2）
# ===========================================================================
def test_plan_armed_bypasses_lead_gate():
    # armed=True：lead=1600<3000 仍发射（触发已由编排入口并集判定）
    out = lp.plan_protective_sells({"MELON": 30}, FALLING, [], 1600.0,
                                   step=582, armed=True)
    assert out == [["SELL", "MELON", 4]]


def test_plan_armed_none_lead_still_deferred():
    sells = [["SELL", "MELON", 10]]
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, sells, None,
                                    step=582, armed=True) is sells


def test_plan_unarmed_default_keeps_v1_gate():
    # armed=False（缺省）：lead<3000 不发（v1 防御门保持）
    assert lp.plan_protective_sells({"MELON": 30}, FALLING, [], 2999.99,
                                    step=582) == []


# ===========================================================================
# E. build v2 用例组（回撤臂 + 峰寄存器 + 并集）
# ===========================================================================
def _drawdown_obs(day, me, opp, glut=True):
    step = day * 24 + 6
    inv = {"MELON": 15000, "WHEAT": 10000} if glut else \
        {"MELON": 10000, "WHEAT": 10000}
    return make_obs(step=step, me_money=me, opp_money=opp, inventory=inv)


def test_build_drawdown_arm_triggers():
    # d15 峰 5000 → d16 回撤至 2900（peak-lead=2100>=2000 且 lead>=1500）
    reg = {}
    obs_peak = _drawdown_obs(15, 58000.0, 53000.0)          # lead=5000 新峰
    assert lp.build_lead_protection(obs_peak, 15, TAPE, register=reg) is TAPE
    assert reg == {"peak_lead": 5000.0}
    obs_drop = _drawdown_obs(16, 55900.0, 53000.0)          # lead=2900
    out = lp.build_lead_protection(obs_drop, 16, TAPE, register=reg)
    assert out is not TAPE and ["SELL", "MELON", 4] in out


def test_build_drawdown_boundary_equality_triggers():
    reg = {"peak_lead": 5000.0}
    obs = _drawdown_obs(15, 53000.0, 50000.0)               # lead=3000, dd=2000
    out = lp.build_lead_protection(obs, 15, TAPE, register=reg)
    assert ["SELL", "MELON", 4] in out


def test_build_drawdown_just_below_threshold_identity():
    reg = {"peak_lead": 5000.0}
    obs = _drawdown_obs(15, 53001.0, 50000.0)               # lead=3001, dd=1999
    assert lp.build_lead_protection(obs, 15, TAPE, register=reg) is TAPE


def test_build_drawdown_lead_gate_identity():
    # 回撤 3500>=2000 但 lead=1400<1500（仍领先不足）→ 不触发
    reg = {"peak_lead": 5000.0}
    obs = _drawdown_obs(15, 51400.0, 50000.0)
    assert lp.build_lead_protection(obs, 15, TAPE, register=reg) is TAPE


def test_build_drawdown_day_gate_identity_but_peak_tracked():
    # d14（<15）回撤形态在场 → 不触发；但峰值仍并入寄存器
    reg = {}
    obs = _drawdown_obs(14, 55000.0, 50000.0)               # lead=5000
    assert lp.build_lead_protection(obs, 14, TAPE, register=reg) is TAPE
    assert reg == {"peak_lead": 5000.0}
    obs_drop = _drawdown_obs(14, 52500.0, 50000.0)          # dd=2500, d14
    assert lp.build_lead_protection(obs_drop, 14, TAPE,
                                    register=reg) is TAPE


def test_build_peak_register_tracks_monotone_max():
    reg = {}
    for me, opp in ((52000.0, 50000.0), (56000.0, 50000.0),
                    (54000.0, 50000.0), (60000.0, 50000.0)):
        lp.build_lead_protection(_drawdown_obs(15, me, opp), 15, TAPE,
                                 register=reg)
    assert reg == {"peak_lead": 10000.0}
    # 新峰帧回撤=0 → 臂 A 不触发（峰值帧零回撤语义）
    assert lp.build_lead_protection(_drawdown_obs(15, 60000.0, 50000.0),
                                    15, TAPE, register=reg) is TAPE


def test_build_union_d24_arm_independent_of_register():
    # 臂 B 不依赖寄存器：register=None、day=24、lead=3000 → 触发（v1 路径）
    obs = make_obs(step=582, me_money=7000.0, opp_money=4000.0,
                   inventory={"MELON": 15000, "WHEAT": 10000})
    out = lp.build_lead_protection(obs, 24, TAPE)
    assert ["SELL", "MELON", 4] in out


def test_build_union_both_arms_same_frame():
    # 同帧双臂同时满足（d24、lead 3200、dd 2500）→ 触发一次（并集语义）
    reg = {"peak_lead": 5700.0}
    obs = _drawdown_obs(24, 53200.0, 50000.0)
    out = lp.build_lead_protection(obs, 24, TAPE, register=reg)
    assert out is not TAPE and ["SELL", "MELON", 4] in out


def test_build_register_none_drawdown_inert():
    # register=None：每帧临时寄存器 → 回撤恒 0 → 臂 A 退化，仅臂 B 可触发
    obs = _drawdown_obs(16, 55900.0, 53000.0)               # lead=2900<3000
    assert lp.build_lead_protection(obs, 16, TAPE) is TAPE
    assert lp.build_lead_protection(obs, 16, TAPE, register=None) is TAPE


def test_build_register_garbage_treated_as_none():
    # 非法寄存器类型 → 当 None 处理（fail-safe，臂 A 退化）
    obs = _drawdown_obs(16, 55900.0, 53000.0)
    assert lp.build_lead_protection(obs, 16, TAPE,
                                    register="garbage") is TAPE


def test_build_register_not_mutated_on_nonmeasurable_frame():
    # lead 不可估帧（unobservable：无 money 无 shed 无动物）→ 寄存器原样不动
    reg = {"peak_lead": 5000.0}
    obs = {"step": 16 * 24 + 6, "player": 0, "farms": [],
           "market": {"prices": {}, "inventory": {}}, "town": {}}
    lp.build_lead_protection(obs, 16, TAPE, register=reg)
    assert reg == {"peak_lead": 5000.0}


def test_build_register_survives_error_frame():
    # 抛异常观测帧 → 原单返回；寄存器不被破坏（跨帧续用）
    reg = {"peak_lead": 5000.0}

    class RaisingObs(dict):
        def get(self, key, default=None):
            raise RuntimeError("boom")

    assert lp.build_lead_protection(RaisingObs(), 16, TAPE,
                                    register=reg) is TAPE
    assert reg == {"peak_lead": 5000.0}
    obs_drop = _drawdown_obs(16, 55900.0, 53000.0)
    out = lp.build_lead_protection(obs_drop, 16, TAPE, register=reg)
    assert ["SELL", "MELON", 4] in out


def test_build_drawdown_terminal_window_identity():
    reg = {"peak_lead": 20000.0}
    obs = make_obs(step=717, me_money=15000.0, opp_money=5000.0)
    assert lp.build_lead_protection(obs, 29, TAPE, register=reg) is TAPE


def test_build_v2_config_override():
    # config 经参数传入（模块纯函数）：收紧回撤槛至 2500 → 2100 回撤不触发
    reg = {"peak_lead": 5000.0}
    obs = _drawdown_obs(16, 55900.0, 53000.0)               # dd=2100
    out = lp.build_lead_protection(obs, 16, TAPE, register=reg)
    assert ["SELL", "MELON", 4] in out
    reg2 = {"peak_lead": 5000.0}
    assert lp.build_lead_protection(obs, 16, TAPE,
                                    config={"trigger_drawdown_min": 2500.0},
                                    register=reg2) is TAPE


def test_build_deterministic():
    obs = make_obs(step=582, inventory={"MELON": 15000, "WHEAT": 10000})
    a = lp.build_lead_protection(obs, 24, TAPE)
    b = lp.build_lead_protection(obs, 24, TAPE)
    assert a == b
