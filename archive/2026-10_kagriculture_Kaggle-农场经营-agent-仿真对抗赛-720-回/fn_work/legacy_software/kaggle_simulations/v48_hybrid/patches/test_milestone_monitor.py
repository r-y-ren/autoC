# -*- coding: utf-8 -*-
"""test_milestone_monitor -- P3 剧本健康监测的单元测试（R4 验收：触发面 + 只动卖单 +
正常局零动作 + 异常回退）。纯 pytest，无外部依赖。

观测夹具按基底 v23.state_encoder 消费的引擎形态构造（dict 观测：
farms[player].{money, tiles, hands, unlocked_quadrants}、private.shed、step）。
"""

import milestone_monitor as mm


def make_obs(
    *,
    day=10,
    step=None,
    money=6000.0,
    quadrants=3,
    hands=12,
    cows=11,
    shed=None,
    player=0,
):
    """健康局形态的最小引擎观测；各字段可覆写以构造偏离局。"""
    if step is None:
        step = day * mm.TURNS_PER_DAY + 18  # 日后半（late_day=True）
    tiles = [
        {"kind": "PASTURE", "animal": "COW" if i < cows else None, "yield_units": 6}
        for i in range(max(cows, 4))
    ]
    farm = {
        "money": money,
        "hands": [{} for _ in range(hands)],
        "unlocked_quadrants": list(range(quadrants)),
        "tiles": [tiles],
    }
    return {
        "step": step,
        "day": day,
        "player": player,
        "farms": [farm],
        "town": {"unlocked_shops": ["FARMERS_MARKET"]},
        "market": {"inventory": {}, "prices": {}},
        "private": {"shed": dict(shed or {}), "seeds": {}},
    }


def deviated(money=800.0, day=10):
    return mm.assess_milestone_deviation(make_obs(day=day, money=money, cows=3), day)


# ---------------------------------------------------------------------------
# assess：正常局零动作
# ---------------------------------------------------------------------------

class TestAssessHealthy:
    def test_outside_window_zero_action(self):
        """窗口外（d5/d13）即便状态灾难也不评估不偏离（回退 F3）。"""
        for day in (5, 13):
            obs = make_obs(day=day, money=0.0, quadrants=1, hands=0, cows=0)
            result = mm.assess_milestone_deviation(obs, day)
            assert result["deviated"] is False
            assert result["detail"]["window"] is False

    def test_healthy_d10_late_day(self):
        result = mm.assess_milestone_deviation(make_obs(day=10), 10)
        assert result["deviated"] is False
        assert result["detail"]["failed"] == []

    def test_healthy_d11_d12(self):
        for day in (11, 12):
            money = 6000.0 if day == 11 else 3000.0  # d12 地板 2500 上方
            obs = make_obs(day=day, money=money, hands=13, cows=11, shed={"MELON": 0})
            result = mm.assess_milestone_deviation(obs, day)
            assert result["deviated"] is False

    def test_morning_gating_no_false_positive(self):
        """日内在途（step%24<12、资金谷值、雇工未满员、地2 未购）不误报。"""
        obs = make_obs(day=10, step=10 * 24 + 3, money=100.0, quadrants=2, hands=2, cows=9)
        assert mm.assess_milestone_deviation(obs, 10)["deviated"] is False
        # 同状态挪到日后半 → 偏离（门控对照）
        obs_late = make_obs(day=10, step=10 * 24 + 18, money=100.0, quadrants=2, hands=2, cows=9)
        result = mm.assess_milestone_deviation(obs_late, 10)
        assert result["deviated"] is True
        assert set(result["detail"]["failed"]) == {"money", "crew_hands"}

    def test_boundary_days_in_window(self):
        assert mm.assess_milestone_deviation(make_obs(day=10), 10)["detail"]["window"] is True
        assert mm.assess_milestone_deviation(make_obs(day=12), 12)["detail"]["window"] is True

    def test_determinism_same_input_same_output(self):
        obs = make_obs(day=11, money=800.0, cows=3, shed={"MELON": 30})
        assert mm.assess_milestone_deviation(obs, 11) == mm.assess_milestone_deviation(obs, 11)


# ---------------------------------------------------------------------------
# assess：偏离局触发面
# ---------------------------------------------------------------------------

class TestAssessDeviated:
    def test_low_money_deviates(self):
        result = mm.assess_milestone_deviation(make_obs(day=10, money=800.0), 10)
        assert result["deviated"] is True
        assert "money" in result["detail"]["failed"]
        check = result["detail"]["checks"]["money"]
        assert check["expected"] == 6000.0 and check["floor"] == 3000.0

    def test_money_at_floor_not_deviated(self):
        assert mm.assess_milestone_deviation(make_obs(day=10, money=3000.0), 10)["deviated"] is False

    def test_land_herd_crew_deviations(self):
        """资金健康但里程碑资产未兑现（d11：地2 未买、畜线未点火、crew 塌）。"""
        obs = make_obs(day=11, money=6000.0, quadrants=1, hands=2, cows=3)
        result = mm.assess_milestone_deviation(obs, 11)
        assert result["deviated"] is True
        assert set(result["detail"]["failed"]) == {"land_quadrants", "crew_hands", "cow_herd"}

    def test_d10_land_floor_2_no_false_positive(self):
        """d10 象限=2（地2 当日购买在途/刚执行）不误报；d11 同状态才报。"""
        assert mm.assess_milestone_deviation(make_obs(day=10, quadrants=2), 10)["deviated"] is False
        assert mm.assess_milestone_deviation(make_obs(day=11, quadrants=2), 11)["deviated"] is True

    def test_melon_residual_d11_d12(self):
        for day in (11, 12):
            obs = make_obs(day=day, money=6000.0 if day == 11 else 3000.0,
                           hands=13, shed={"MELON": 30})
            result = mm.assess_milestone_deviation(obs, day)
            assert result["deviated"] is True
            assert "melon_residual" in result["detail"]["failed"]

    def test_melon_residual_d10_not_checked(self):
        """d10 flush 在途，棚仓 MELON 45 不触发残留检查。"""
        obs = make_obs(day=10, shed={"MELON": 45})
        assert mm.assess_milestone_deviation(obs, 10)["deviated"] is False

    def test_seat1_observation(self):
        obs = make_obs(day=10, money=800.0, player=1)
        obs["farms"].append(obs["farms"].pop(0))  # 让席位 1 指向灾难 farm
        result = mm.assess_milestone_deviation(obs, 10)
        assert result["deviated"] is True


# ---------------------------------------------------------------------------
# assess：异常回退
# ---------------------------------------------------------------------------

class TestAssessFailSafe:
    def test_none_observation(self):
        result = mm.assess_milestone_deviation(None, 10)
        assert result["deviated"] is False
        assert "error" in result["detail"]

    def test_empty_farms(self):
        result = mm.assess_milestone_deviation({"step": 258, "farms": []}, 10)
        assert result["deviated"] is False
        assert "error" in result["detail"]

    def test_garbage_day(self):
        result = mm.assess_milestone_deviation(make_obs(), "ten")
        assert result["deviated"] is False
        assert "error" in result["detail"]

    def test_never_raises(self):
        for bad in (None, 42, "x", {"farms": None}, {"step": "x", "farms": [{}]}):
            assert mm.assess_milestone_deviation(bad, 10)["deviated"] is False


# ---------------------------------------------------------------------------
# adjust：偏离局只动卖单
# ---------------------------------------------------------------------------

class TestAdjustDeviated:
    SELLS = [
        ["SELL", "FERTILIZER", 4],
        ["SELL", "WHEAT", 10],
        ["SELL", "MELON", 30],
        ["SELL", "MILK", 6],
    ]

    def test_postpones_nonurgent_keeps_cashflow(self):
        """money=800 ≥ CASH_FLOOR：仅肥料（日结现金流）保留，其余推迟。"""
        out = mm.adjust_sell_timing(list(self.SELLS), deviated(money=800.0))
        assert out == [["SELL", "FERTILIZER", 4]]

    def test_cash_critical_keeps_largest_sufficient(self):
        """money=100 < $600：缺口 $500 → 保守估值最大的 MELON(7500) 一张补足。"""
        out = mm.adjust_sell_timing(list(self.SELLS), deviated(money=100.0))
        assert out == [["SELL", "FERTILIZER", 4], ["SELL", "MELON", 30]]

    def test_explicit_urgent_marker_kept(self):
        sells = [["SELL", "WOOL", 24, True], ["SELL", "WHEAT", 10]]
        out = mm.adjust_sell_timing(sells, deviated(money=800.0))
        assert out == [["SELL", "WOOL", 24, True]]

    def test_unrecognized_orders_kept_untouched(self):
        sells = [["BUY_PRODUCT", "WHEAT", 8], ["SELL"], "garbage", None]
        out = mm.adjust_sell_timing(list(sells), deviated(money=800.0))
        assert out == sells  # F5：不识别 → 原样保留

    def test_empty_sells(self):
        assert mm.adjust_sell_timing([], deviated()) == []

    def test_missing_money_detail(self):
        """detail 无 money（外来 deviation dict）→ 缺口保留不启用，仅 U1 生效。"""
        out = mm.adjust_sell_timing(list(self.SELLS), {"deviated": True, "detail": {}})
        assert out == [["SELL", "FERTILIZER", 4]]


# ---------------------------------------------------------------------------
# adjust：正常局零动作 / 异常回退
# ---------------------------------------------------------------------------

class TestAdjustZeroAction:
    def test_not_deviated_returns_same_object(self):
        sells = [["SELL", "WHEAT", 10]]
        ok = mm.assess_milestone_deviation(make_obs(day=10), 10)
        assert mm.adjust_sell_timing(sells, ok) is sells  # identity：原样返回

    def test_deviated_with_detail_none_postpones(self):
        """deviated=True 但 detail=None（外来形态）→ 仍执行推迟（仅 U1 生效）。"""
        sells = [["SELL", "WHEAT", 10], ["SELL", "FERTILIZER", 4]]
        out = mm.adjust_sell_timing(sells, {"deviated": True, "detail": None})
        assert out == [["SELL", "FERTILIZER", 4]]

    def test_non_dict_or_falsy_deviation_identity(self):
        sells = [["SELL", "WHEAT", 10]]
        for deviation in (
            {"deviated": False, "detail": {}},
            {},
            None,
            "nope",
        ):
            assert mm.adjust_sell_timing(sells, deviation) is sells

    def test_adjust_fail_safe_on_garbage_detail(self):
        """detail 取值中抛异常 → 被吞 → 原样返回（回退 F2）。"""

        class BoomDetail(dict):
            def get(self, key, default=None):
                raise RuntimeError("boom")

        sells = [["SELL", "WHEAT", 10]]
        deviation = {"deviated": True, "detail": BoomDetail()}
        assert mm.adjust_sell_timing(sells, deviation) is sells

    def test_adjust_fail_safe_on_non_iterable_sells(self):
        assert mm.adjust_sell_timing(None, deviated()) is None


# ---------------------------------------------------------------------------
# 集成缝证据：只动 SELL 槽位，产线步骤零触碰
# ---------------------------------------------------------------------------

class TestSeamOnlySells:
    def test_documented_seam_leaves_production_untouched(self):
        """按模块头集成缝公式组装：farmer/hands/BUY 槽位逐字不动，仅 SELL 被换。"""
        action = {
            "farmer": ["HIRE", "MOVE_N"],
            "hands": [["HARVEST", 3, 4], ["WATER", 1, 2]],
            "market": [
                ["BUY_PRODUCT", "WHEAT", 8],
                ["SELL", "WHEAT", 10],
                ["SELL", "FERTILIZER", 4],
                ["SELL", "MELON", 30],
            ],
        }
        farmer_before, hands_before = action["farmer"], action["hands"]
        deviation = deviated(money=800.0)

        def _is_sell(order):
            return isinstance(order, (list, tuple)) and order[:1] == ["SELL"]

        sells_in = [o for o in action["market"] if _is_sell(o)]
        kept = mm.adjust_sell_timing(sells_in, deviation)
        sell_iter = iter(kept)
        rebuilt = []
        for order in action["market"]:
            if not _is_sell(order):
                rebuilt.append(order)  # 非 SELL 槽位原位保留
                continue
            kept_order = next(sell_iter, None)
            if kept_order is not None:  # 被推迟的 SELL 槽位直接收缩
                rebuilt.append(kept_order)
        action["market"] = rebuilt
        assert action["farmer"] is farmer_before  # 产线（farmer 步骤）零触碰
        assert action["hands"] is hands_before    # 产线（单位步骤）零触碰
        assert action["market"] == [
            ["BUY_PRODUCT", "WHEAT", 8],          # 非卖市场单（P2 的面）零触碰
            ["SELL", "FERTILIZER", 4],            # 紧急现金流保留
        ]


# ---------------------------------------------------------------------------
# 契约钉子：预期表/阈值登记值
# ---------------------------------------------------------------------------

class TestContractPins:
    def test_window(self):
        assert (mm.WINDOW_FIRST_DAY, mm.WINDOW_LAST_DAY) == (10, 12)

    def test_milestone_table_values(self):
        quadrants_floors = {d: mm.MILESTONE_TABLE[d]["quadrants_floor"] for d in (10, 11, 12)}
        assert quadrants_floors == {10: 2, 11: 3, 12: 3}
        assert mm.MILESTONE_TABLE[10]["hands_floor"] == 10
        assert mm.MILESTONE_TABLE[11]["hands_floor"] == 11
        assert all(mm.MILESTONE_TABLE[d]["cows_floor"] == 9 for d in (10, 11, 12))
        assert mm.MILESTONE_TABLE[10]["melon_residual_limit"] is None
        assert mm.MILESTONE_TABLE[11]["melon_residual_limit"] == 20
        assert mm.MILESTONE_TABLE[12]["melon_residual_limit"] == 20

    def test_money_floors_derive_from_ratio(self):
        for day, expected in ((10, 6000.0), (11, 6000.0), (12, 5000.0)):
            floor = round(expected * mm.MONEY_DEVIATION_RATIO, 2)
            obs = make_obs(day=day, money=floor - 0.01,
                           hands=13 if day > 10 else 12, shed={"MELON": 0})
            assert mm.assess_milestone_deviation(obs, day)["deviated"] is True

    def test_cash_floor_and_base_price_registered(self):
        assert mm.CASH_FLOOR == 600.0
        assert mm.BASE_PRICE["MELON"] == 250.0
        assert mm.BASE_PRICE["FERTILIZER"] == 100.0
