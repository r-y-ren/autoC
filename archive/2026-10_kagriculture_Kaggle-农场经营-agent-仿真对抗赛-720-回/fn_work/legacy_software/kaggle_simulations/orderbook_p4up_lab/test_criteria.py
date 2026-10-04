# -*- coding: utf-8 -*-
"""test_criteria —— 六判据判例（构造正/负/边界，含手算金值）。"""
import collections

from orderbook_p4up_lab import criteria as C
from orderbook_p4up_lab.records import EpisodeRecord


def act(farmer="PASS", hands=(), market=()):
    return {"farmer": [farmer], "hands": [list(h) for h in hands],
            "market": [list(m) for m in market]}


def rec(stream, opp_stream=None, world="W1", margin=1.0, episode=1,
        prices_t=None, occ=None, pres=None, unlocked=None, team="ME", opp="OPP"):
    return EpisodeRecord(
        episode=episode, seat=0, team=team, opp=opp, margin=margin,
        stream=stream, opp_stream=opp_stream if opp_stream is not None
        else [act()] * len(stream), world=world, prices_t=prices_t,
        occ=occ, pres=pres, unlocked=unlocked)


def uniform(n, template):
    return [dict(template) for _ in range(n)]


# ---------------------------------------------------------------- ① 双重分类

class TestCompareStreams:
    def test_identical(self):
        s = uniform(10, act("HARVEST"))
        out = C.compare_streams([s, list(s)])
        assert out["varying"] == 0 and out["frac"] == 0.0 and out["first"] is None

    def test_channel_attribution(self):
        a = uniform(4, act("HARVEST"))
        b = uniform(4, act("HARVEST"))
        b[2] = act("HARVEST", market=[["SELL", "WOOL", 1]])   # 仅 market 差
        out = C.compare_streams([a, b])
        assert out["varying"] == 1 and out["first"] == 2
        assert out["chan"] == {"farmer": 0, "hands": 0, "market": 1}

    def test_empty_streams(self):
        out = C.compare_streams([[], []])
        assert out["turns"] == 0 and out["varying"] == 0


class TestClassify:
    def _c(self, varying, frac, plan_moves):
        chan = {"farmer": plan_moves, "hands": 0, "market": varying}
        return {"turns": 100, "varying": varying, "frac": frac, "first": 1,
                "chan": chan}

    def test_pure_replay(self):
        assert C.classify(self._c(0, 0.0, 0)) == "PURE_REPLAY"

    def test_repairing_market_only(self):
        # market-only 变动 20%（<0.25）→ REPAIRING_SCRIPT
        assert C.classify(self._c(20, 0.20, 0)) == "REPAIRING_SCRIPT"

    def test_repairing_low_frac(self):
        # plan 有动但 frac 5%（<0.10）→ REPAIRING_SCRIPT
        assert C.classify(self._c(5, 0.05, 5)) == "REPAIRING_SCRIPT"

    def test_adaptive(self):
        assert C.classify(self._c(30, 0.30, 30)) == "ADAPTIVE"


class TestDualClassification:
    def test_shop_router_signature(self):
        # 两个世界各自全同、彼此不同 → 全局 ADAPTIVE、世界内 PURE_REPLAY
        s1 = uniform(20, act("HARVEST"))
        s2 = uniform(20, act("CARE"))
        records = [rec(s1, world="A__B"), rec(list(s1), world="A__B"),
                   rec(s2, world="C__D"), rec(list(s2), world="C__D")]
        out = C.dual_classification(records)
        assert out["global"]["cls"] == "ADAPTIVE"
        assert out["verdict_counts"] == {"PURE_REPLAY": 2}
        assert "SHOP_ROUTER_SIGNATURE" in out["gap_diagnosis"]

    def test_within_world_adaptive(self):
        # 同世界内也分叉 → WITHIN_WORLD_ADAPTIVE
        s1 = uniform(20, act("HARVEST"))
        s2 = uniform(20, act("HARVEST"))
        s2[5] = act("CARE")
        s2[6] = act("CARE")
        s2[7] = act("CARE")
        records = [rec(s1, world="A__B"), rec(s2, world="A__B")]
        out = C.dual_classification(records)
        assert out["verdict_counts"].get("ADAPTIVE") == 1
        assert "WITHIN_WORLD_ADAPTIVE" in out["gap_diagnosis"]

    def test_router_hint_window(self):
        s1 = [act("HARVEST")] * 100
        s2 = [act("HARVEST")] * 100
        for t in range(80, 92):          # 12% 拍 plan 变动 → ADAPTIVE
            s2[t] = act("CARE")
        records = [rec(s1, world="A__B"), rec(s2, world="A__B")]
        out = C.dual_classification(records)
        assert out["global"]["cls"] == "ADAPTIVE"
        assert out["router_hint"] is not None and "t=80" in out["router_hint"]

    def test_threshold_carried(self):
        out = C.dual_classification([rec(uniform(5, act()))])
        assert out["threshold"]["classify_frac_repair"] == 0.25
        assert out["threshold"]["classify_frac_low"] == 0.10


# ---------------------------------------------------------------- ② 血缘谱

class TestKinship:
    def test_plan_vs_whole(self):
        mine = uniform(10, act("HARVEST", hands=[["CARE"]], market=[["SELL", "WOOL", 1]]))
        opp = uniform(10, act("HARVEST", hands=[["CARE"]], market=[["SELL", "WOOL", 9]]))
        ag = C.plan_whole_agreement(mine, opp)
        assert ag["plan"] == 1.0            # farmer+hands 全同
        assert ag["whole"] == 0.0           # market 数量不同 → canon 不同

    def test_barcode_fork_day(self):
        # day 0-4 重锚窗同、day 5 起市单分叉 → fork_day=5
        def mk(prod_from_5):
            s = []
            for d in range(30):
                for h in range(24):
                    if h == 1:
                        prod = "WHEAT" if d < 5 else prod_from_5
                        s.append(act(market=[["BUY_SEED", prod, 1]]))
                    else:
                        s.append(act())
            return s
        mb, ob = C.barcode(mk("WHEAT")), C.barcode(mk("MELON"))
        shared = sum(1 for x, y in zip(mb, ob) if x == y)
        assert shared == 5
        fork = next(d for d, (x, y) in enumerate(zip(mb, ob)) if x != y)
        assert fork == 5

    def test_spectrum_mirror_sibling_unrelated(self):
        base = [act("HARVEST")] * 30
        mirror = list(base)                                   # plan 1.0
        sib = [act("HARVEST") if i % 2 == 0 else act("CARE") for i in range(30)]
        other = [act("WATER")] * 30                           # plan 0.0
        records = [rec(base, opp_stream=mirror, margin=5.0, episode=1),
                   rec(base, opp_stream=sib, margin=-3.0, episode=2),
                   rec(base, opp_stream=other, margin=0.0, episode=3)]
        out = C.kinship_spectrum(records)
        assert out["n_mirror"] == 1 and out["n_sibling"] == 1
        assert out["n_unrelated"] == 1
        assert out["mirror_record"] == "1W-0L-0T"
        assert out["threshold"]["mirror_line"] == 0.95

    def test_genetic_groups_union_find(self):
        open_a = [act("HARVEST")] * 144
        open_b = [act("CARE")] * 144
        s_a1 = open_a + [act("WATER")] * 10
        s_a2 = open_a + [act("CARE")] * 10
        s_b1 = open_b + [act("WATER")] * 10
        s_b2 = open_b + [act("CARE")] * 10
        s_u = [act("PASS")] * 154
        out = C.genetic_groups([s_a1, s_a2, s_b1, s_b2, s_u],
                               labels=["a", "a", "b", "b", "u"],
                               margins=[10, -5, 3, 3, 0])
        sizes = sorted(g["games"] for g in out["genetic_groups"])
        assert sizes == [1, 2, 2]
        assert out["threshold"]["genetic_plan"] == 0.98
        big = [g for g in out["genetic_groups"] if g["games"] == 2]
        assert all(g["record"].startswith("W1-L1") or g["record"] == "W2-L0-T0"
                   for g in big)


# ---------------------------------------------------------------- ③ 收敛

class TestConvergence:
    def test_warming_up(self):
        traj = [1000 + 10 * i for i in range(20)]
        out = C.convergence(traj)
        assert out["verdict"] == "WARMING UP"
        assert out["drift"] == 10.0 and out["flips"] == 0
        assert out["threshold"] == 1.0 and out["n"] == 20

    def test_settled(self):
        traj = [1000 + (1.0 if i % 2 else 0.0) for i in range(20)]
        out = C.convergence(traj)
        assert out["verdict"] == "SETTLED"
        assert out["flips"] >= 1 and abs(out["drift"]) <= 1.0

    def test_settling_drift_with_flips(self):
        traj = [1000, 1020, 1005, 1025, 1010, 1030, 1015, 1035]
        out = C.convergence(traj)
        assert out["verdict"] == "SETTLING" and out["flips"] > 0

    def test_settling_flat_no_flips(self):
        traj = [1000.0] * 8
        out = C.convergence(traj)
        assert out["verdict"] == "SETTLING" and out["drift"] == 0.0

    def test_too_few(self):
        out = C.convergence([1, 2, 3])
        assert out["verdict"] == "TOO_FEW" and out["n"] == 3

    def test_custom_threshold_stated(self):
        traj = [1000 + 2 * i for i in range(10)]
        out = C.convergence(traj, threshold=5.0)
        assert out["threshold"] == 5.0        # 阈值随判声明
        assert out["verdict"] == "SETTLING"   # |drift|=2 <= 5 且无变号

    def test_pairing_rate_not_in_verdict(self):
        import datetime as dt
        traj = [1000 + 10 * i for i in range(10)]
        ts = [dt.datetime(2026, 10, 1) + dt.timedelta(hours=2 * i) for i in range(10)]
        out = C.convergence(traj, timestamps=ts)
        assert out["verdict"] == "WARMING UP"
        assert out["pairing_rate_lifetime_per_h"] > 0
        assert "reread_eta_h" in out
        assert "不进判决" in out["pairing_note"]


# ---------------------------------------------------------------- ④ 语言指纹

def _lang_stream(day_pattern, n_days=30, dense=2):
    """day_pattern(day) -> token-producing action or None（None=空拍）。"""
    s = []
    for d in range(n_days):
        for h in range(24):
            if h % max(1, 24 // dense) == 0:
                s.append(day_pattern(d))
            else:
                s.append(None)
    return s


class TestLanguage:
    def test_script_frozen(self):
        eps = [_lang_stream(lambda d: act("HARVEST")) for _ in range(8)]
        out = C.language_fingerprint([rec(s) for s in eps])
        assert out["class"].startswith("SCRIPT")
        for b in out["bands"].values():
            assert b["repeat_rate"] == 1.0

    def test_brancher_trunk_then_melt(self):
        # 干到 d17（含 (12,19) 带前半），d17 起逐局即兴 → BRANCHER
        def pat(i):
            def f(d):
                if d < 17:
                    return act("HARVEST")
                return act(f"X{i}{d}")
            return f
        eps = [_lang_stream(pat(i)) for i in range(8)]
        out = C.language_fingerprint([rec(s) for s in eps])
        assert out["class"].startswith("BRANCHER")
        assert out["bands"]["d06-11"]["repeat_rate"] >= 0.95
        assert out["bands"]["d12-19"]["repeat_rate"] < 0.5

    def test_scheduler_composed(self):
        def pat(i):
            return lambda d: act(f"Y{i}{d}")
        eps = [_lang_stream(pat(i)) for i in range(8)]
        out = C.language_fingerprint([rec(s) for s in eps])
        assert out["class"].startswith("SCHEDULER")
        assert out["bands"]["d06-11"]["repeat_rate"] < 0.5

    def test_floor_8(self):
        eps = [_lang_stream(lambda d: act("HARVEST")) for _ in range(7)]
        out = C.language_fingerprint([rec(s) for s in eps])
        assert out["class"] == "INSUFFICIENT-SIGNAL" and out["bands"] is None

    def test_no_late_days_insufficient(self):
        eps = [[act("HARVEST")] * 100 for _ in range(8)]   # 全部 t<144
        out = C.language_fingerprint([rec(s) for s in eps])
        assert out["class"] == "INSUFFICIENT-SIGNAL"

    def test_speech_class_rules(self):
        fp = {(6, 11): {"repeat_rate": 0.7}, (12, 19): {"repeat_rate": 0.7},
              (20, 29): {"repeat_rate": 0.5}}
        assert C.speech_class(fp).startswith("MIXED")
        fp2 = {(6, 11): {"repeat_rate": 0.96}, (12, 19): {"repeat_rate": 0.71},
               (20, 29): {"repeat_rate": 0.5}}
        assert C.speech_class(fp2).startswith("SCRIPT")
        fp3 = {(6, 11): {"repeat_rate": None}, (12, 19): {"repeat_rate": 1},
               (20, 29): {"repeat_rate": 1}}
        assert C.speech_class(fp3) == "INSUFFICIENT-SIGNAL"

    def test_threshold_carried(self):
        out = C.language_fingerprint([rec([act()])])
        assert out["threshold"]["floor_n"] == 8
        assert "自报" in out["calibration_self_reported"]


# ---------------------------------------------------------------- ⑤ crater

class TestCrater:
    def test_our_crater_dmg_first_order(self):
        # 我 t=50 大卖 WOOL 砸价 100→60；对手 t=60 卖 5 件 → dmg=5*40=200
        mine = [act()] * 300
        mine[50] = act(market=[["SELL", "WOOL", 10]])
        opp = [act()] * 300
        opp[60] = act(market=[["SELL", "WOOL", 5]])
        prices = [{"WOOL": 100, "MILK": 80} for _ in range(300)]
        for t in range(51, 300):
            prices[t]["WOOL"] = 60
        out = C.crater_scan(rec(mine, opp_stream=opp, prices_t=prices))
        assert out["status"] == "OK"
        assert out["our_craters"][0] == {"t0": 50, "t1": 60, "prod": "WOOL", "dmg": 200}
        assert out["their_craters"] == []

    def test_their_crater(self):
        opp = [act()] * 300
        opp[100] = act(market=[["SELL", "MILK", 8]])
        mine = [act()] * 300
        mine[110] = act(market=[["SELL", "MILK", 4]])
        prices = [{"WOOL": 100, "MILK": 80} for _ in range(300)]
        for t in range(101, 300):
            prices[t]["MILK"] = 50
        out = C.crater_scan(rec(mine, opp_stream=opp, prices_t=prices))
        assert out["their_craters"][0]["dmg"] == 4 * 30
        assert out["our_craters"] == []

    def test_window_boundary(self):
        # victim 在 t0+25（>24 窗）卖出 → 不计
        mine = [act()] * 300
        mine[50] = act(market=[["SELL", "WOOL", 10]])
        opp = [act()] * 300
        opp[75] = act(market=[["SELL", "WOOL", 5]])
        prices = [{"WOOL": 100} for _ in range(300)]
        for t in range(51, 300):
            prices[t]["WOOL"] = 60
        out = C.crater_scan(rec(mine, opp_stream=opp, prices_t=prices))
        assert out["our_craters"] == [] and out["their_craters"] == []

    def test_no_prices_insufficient(self):
        out = C.crater_scan(rec([act()] * 10, prices_t=None))
        assert out["status"] == "INSUFFICIENT_DATA"
        assert out["threshold"]["window_turns"] == 24


# ---------------------------------------------------------------- ⑥ 热图半分闸

def _grid(cells):
    g = [[0] * 10 for _ in range(10)]
    for (y, x), v in cells.items():
        g[y][x] = v
    return g


def _board_rec(occ, pres, unlocked, episode):
    return rec([act()], occ=occ, pres=pres, unlocked=unlocked, episode=episode)


class TestBoardMaps:
    def _unlocked(self):
        return _grid({(y, x): 1 for y in range(10) for x in range(10)})

    def test_half_split_trust(self):
        occ = _grid({(0, 0): 10, (9, 9): 4})
        recs = [_board_rec(occ, occ, self._unlocked(), i) for i in range(6)]
        out = C.board_maps(recs)
        assert out["status"] == "OK"
        assert out["maps"]["occupancy"]["gate"] == "TRUST"
        assert out["maps"]["occupancy"]["corr_half"] == 1.0
        assert out["maps"]["occupancy"]["top10_share"] == 1.0
        assert out["threshold"]["gate_r"] == 0.9

    def test_half_split_noise(self):
        a = _grid({(0, 0): 10})
        b = _grid({(9, 9): 10})
        recs = []
        for i in range(6):
            recs.append(_board_rec(a if i % 2 == 0 else b,
                                   a if i % 2 == 0 else b,
                                   self._unlocked(), i))
        out = C.board_maps(recs)
        assert out["maps"]["occupancy"]["gate"] == "NOISE"
        assert out["maps"]["occupancy"]["corr_half"] < 0.9

    def test_not_computable(self):
        zero = _grid({})
        recs = [_board_rec(zero, zero, self._unlocked(), i) for i in range(4)]
        out = C.board_maps(recs)
        assert out["maps"]["occupancy"]["gate"] == "NOT_COMPUTABLE"

    def test_no_grids_insufficient(self):
        out = C.board_maps([rec([act()])])
        assert out["status"] == "INSUFFICIENT_DATA"


# ---------------------------------------------------------------- spec 完整性

class TestSpec:
    def test_all_six_present_with_required_fields(self):
        assert len(C.CRITERIA_SPEC) == 6
        for key, spec in C.CRITERIA_SPEC.items():
            for f in ("name", "definition", "inputs", "outputs", "thresholds",
                      "calibration", "limits"):
                assert spec.get(f), f"{key}.{f} missing"

    def test_self_reported_marks(self):
        for spec in C.CRITERIA_SPEC.values():
            assert ("自报" in spec["calibration"]
                    or "自报" in spec["thresholds"])
