# -*- coding: utf-8 -*-
"""R20 测试面：retape_tail_savings（尾盘修剪/不许误删 HARVEST 与卖单）。

test_retape_tail_savings 真测试拆七组（责任契约 fn_docs/hybrid/
responsibility.md【R19/R20 增补】retape_tail_savings 行 + 引擎事实）：
①d28 前 CARE/FEED 不动（违抛）——窗口外 FEED（<696）/CARE（<672）逐槽原样；
  构造误删（篡改输出/伪造删除清单行）→ _audit_removals 抛「误删红」；
②d28+ CARE 删净、d29+ FEED 删净——窗口内逐条删净（单元指令→["PASS"]），
  清单行 item/qty=所省资源（FEED→WHEAT 1、CARE→null）；
③闲置 HIRE 删、有役 HIRE 留——当日登记表（hands 日结归零，第 m 张当日
  HIRE=当日 hands[m]）：hands[m] 雇佣后无指派→删（槽换 []）、有指派→留；
  同日雇佣前 slot m 已有指派=拿不准→保守保留；多 HIRE 同日序对齐钉住；
④HARVEST/卖单逐类不动——动物格 HARVEST 与 SELL/BUY_* 及 PLANT/WATER/移动/
  建造等逐类原样；篡改 HARVEST/卖单/伪造 HARVEST 清单行→抛；
⑤动作池共享不变量——同池件跨路由/同步引用：写时复制，他路由零影响、
  池内共享件零扰动、输入零改动、指针只挪手术步；
⑥动物不饿死边界——引擎日结口径模拟（fed→0 否则 +1，≥2 逃走；日结只到
  d28 末）：d29 停喂最多累计 1 不触发；d27/d28 FEED 若被删（违例）则翻 2
  逃走——正是审计红线；
⑦真 r34a 实跑删除清单计数——evidence/tail_savings_realrun.json 一次性
  产物，测试断言可复算（同源重算深等）+ decode→surgery→encode 往返自检链
  （blob 区间外字节等价/回路一致/可编译/确定性双跑）。
"""
import copy
import hashlib
import json
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r37 import retape_sheep, retape_tail
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import retape_sheep
    import retape_tail


_HERE = Path(__file__).resolve().parent
_R34A_MAIN = _HERE.parent / "orderbook_2965_adopt" / "a" / "main.py"
_EVIDENCE = _HERE / "evidence" / "tail_savings_realrun.json"


# ---------------------------------------------------------------------------
# 构造件：迷你磁带路由包（每步动作独立入池；hands 槽=手号指令）
# ---------------------------------------------------------------------------
def _mk_pkg(steps, farmers=None, hands=None, markets=None, routes=None):
    """构造磁带路由包 {actions, routes, shops}。

    farmers={step: 单元指令}；hands={(step, 手号): 单元指令}；markets=
    {(step, 槽): 订单}（未列槽=既有空槽 []，位次语义保留）。
    """
    farmers = farmers or {}
    hands = hands or {}
    markets = markets or {}
    actions = []
    for s in range(steps):
        max_h = max([i for (x, i) in hands if x == s], default=-1)
        max_m = max([j for (x, j) in markets if x == s], default=-1)
        actions.append({
            "farmer": list(farmers.get(s, ["PASS"])),
            "hands": [list(hands.get((s, i), ["PASS"])) for i in range(max_h + 1)],
            "market": [list(markets.get((s, j), [])) for j in range(max_m + 1)],
        })
    return {"actions": actions, "routes": routes or {"0": list(range(steps))},
            "shops": []}


def _r34a_text():
    return _R34A_MAIN.read_text(encoding="utf-8")


def _view(pkg, rid, step):
    return pkg["actions"][pkg["routes"][rid][step]]


def _removed_keys(out):
    """[(step, kind, unit|slot)] 排序清单（断言用）。"""
    return sorted((e["step"], e["kind"], e["unit"] if e["unit"] is not None
                   else e["slot"]) for e in out["removed"])


def _tail_hire_verdicts(pkg):
    """各路由 d29 HIRE 判定计数 {idle, employed, uncertain}（原磁带口径）。"""
    cnt = {"idle": 0, "employed": 0, "uncertain": 0}
    for rid in pkg["routes"]:
        seq = [pkg["actions"][i] for i in pkg["routes"][rid]]
        for (s, j), m in retape_tail._day_ordinals(seq).items():
            if s < retape_tail.FEED_FROM_STEP:
                continue
            cnt[retape_tail._hire_verdict(seq, s, j, m)] += 1
    return cnt


def _snapshot(main_text, out, before):
    """真 r34a 实跑删除清单计数快照（确定性、可复算；evidence 一次性产物）。"""
    removed = out["removed"]
    by_kind = {"CARE": 0, "FEED": 0, "HIRE": 0}
    by_kind_day = {"CARE": {}, "FEED": {}, "HIRE": {}}
    by_route = {}
    for e in removed:
        day = e["step"] // 24
        by_kind[e["kind"]] += 1
        d = by_kind_day[e["kind"]]
        d[str(day)] = d.get(str(day), 0) + 1
        by_route.setdefault(e["route"], {"CARE": 0, "FEED": 0, "HIRE": 0})
        by_route[e["route"]][e["kind"]] += 1
    feed_kept_d28 = 0
    for rid in before["routes"]:
        seq = [before["actions"][i] for i in before["routes"][rid]]
        for s, a in enumerate(seq):
            if not (672 <= s < 696):
                continue
            for _, op in retape_sheep._units(a):
                if isinstance(op, list) and op and op[0] == "FEED":
                    feed_kept_d28 += 1
    return {
        "source": "orderbook_2965_adopt/a/main.py",
        "source_sha256": hashlib.sha256(main_text.encode("utf-8")).hexdigest(),
        "generated_by": "orderbook_r37/retape_tail.py::retape_tail_savings"
                        "（真 r34a 实跑删除清单计数）",
        "criteria": {
            "care_from_step": 672,
            "feed_from_step": 696,
            "turns_per_day": 24,
            "last_day_boundary_step": 695,
            "idle_hire_rule": "day-local HIRE registry (market order) -> "
                              "hands[ordinal]; employed iff non-PASS assignment "
                              "in (hire_step, day_end]; pre-creation refs => "
                              "uncertain keep; verdict on pre-surgery tape",
            "removal_form": {"unit": "op -> ['PASS']",
                             "market": "HIRE slot -> []"},
        },
        "removed_total": len(removed),
        "by_kind": by_kind,
        "by_kind_day": by_kind_day,
        "by_route": by_route,
        "tail_hire_verdicts": _tail_hire_verdicts(before),
        "d28_feed_kept": feed_kept_d28,
        "pool_actions_before": len(before["actions"]),
        "pool_actions_after": len(out["routes"]["actions"]),
        "routes": len(before["routes"]),
    }


def _r34a_snapshot():
    text = _r34a_text()
    pkg = retape_sheep._decode_routes(text)
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    assert pkg == before
    return text, before, out, _snapshot(text, out, before)


# ---------------------------------------------------------------------------
# 伞面冒烟：三类删除端到端 + 输出形态 + 输入零改动
# ---------------------------------------------------------------------------
def test_retape_tail_savings():
    pkg = _mk_pkg(719,
                  farmers={600: ["FEED"], 672: ["CARE"], 696: ["FEED"]},
                  hands={(700, 1): ["CARE"], (710, 0): ["PASS"]},
                  markets={(700, 2): ["HIRE"], (705, 0): ["SELL", "WOOL", 3]})
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    assert set(out) == {"routes", "removed"}
    assert set(out["routes"]) == {"actions", "routes", "shops"}
    assert _removed_keys(out) == [(672, "CARE", "F"), (696, "FEED", "F"),
                                  (700, "CARE", "h1"), (700, "HIRE", 2)]
    assert pkg == before                       # 输入零改动（写时复制）
    # 手术步改写、非手术步原样；HIRE 槽换 [] 保留位次，卖单不动。
    assert _view(out["routes"], "0", 700) == {
        "farmer": ["PASS"], "hands": [["PASS"], ["PASS"]],
        "market": [[], [], []]}
    assert _view(out["routes"], "0", 600) == before["actions"][600]
    assert _view(out["routes"], "0", 705) == before["actions"][705]


# ---------------------------------------------------------------------------
# ① d28 前 CARE/FEED 不动（违抛）
# ---------------------------------------------------------------------------
def test_pre_d28_feed_care_kept_and_misdeletion_raises():
    pkg = _mk_pkg(719,
                  farmers={600: ["FEED"], 671: ["CARE"], 672: ["FEED"],
                           695: ["FEED"], 700: ["CARE"]},
                  hands={(650, 0): ["CARE"], (660, 1): ["FEED"]})
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    # 仅 d28+ CARE 一条；窗口外 FEED（600/671/672/695）与 CARE（600/650/660/671）
    # 逐槽原样（含 d28 的 FEED——喂养 d28→d29 日结，红线）。
    assert _removed_keys(out) == [(700, "CARE", "F")]
    for s, u in [(600, "F"), (671, "F"), (672, "F"), (695, "F")]:
        assert _view(out["routes"], "0", s)["farmer"] == before["actions"][s]["farmer"]
    assert _view(out["routes"], "0", 650)["hands"][0] == ["CARE"]
    assert _view(out["routes"], "0", 660)["hands"][1] == ["FEED"]
    assert all(e["step"] >= 672 for e in out["removed"] if e["kind"] == "CARE")
    assert all(e["step"] >= 696 for e in out["removed"] if e["kind"] == "FEED")

    # 违抛①：篡改输出（把窗口外 FEED/CARE 删掉）→ 术后对账抛「误删红」。
    for s, op_key in [(600, "farmer"), (671, "farmer")]:
        bad = copy.deepcopy(out["routes"])
        act = _view(bad, "0", s)
        act[op_key] = ["PASS"]
        with pytest.raises(RuntimeError, match="误删红"):
            retape_tail._audit_removals(pkg, bad, out["removed"])
    # 违抛②：伪造删除清单行（d28 前 CARE / 非法 kind）→ 抛。
    for forged in ({"route": "0", "step": 600, "kind": "CARE", "slot": None,
                    "unit": "F", "item": None, "qty": None, "reason": "x"},
                   {"route": "0", "step": 700, "kind": "HARVEST", "slot": None,
                    "unit": "F", "item": None, "qty": None, "reason": "x"}):
        with pytest.raises(RuntimeError, match="误删红"):
            retape_tail._audit_removals(pkg, out["routes"], out["removed"] + [forged])


# ---------------------------------------------------------------------------
# ② d28+ CARE 删净、d29+ FEED 删净
# ---------------------------------------------------------------------------
def test_tail_care_feed_removed_clean():
    pkg = _mk_pkg(719,
                  farmers={600: ["CARE"], 671: ["FEED"], 672: ["CARE"],
                           695: ["FEED"], 696: ["FEED"], 700: ["CARE"],
                           718: ["CARE"]},
                  hands={(650, 0): ["FEED"], (680, 0): ["CARE"],
                         (700, 1): ["FEED"], (718, 2): ["CARE"]})
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    assert _removed_keys(out) == [
        (672, "CARE", "F"), (680, "CARE", "h0"), (696, "FEED", "F"),
        (700, "CARE", "F"), (700, "FEED", "h1"), (718, "CARE", "F"),
        (718, "CARE", "h2")]
    # 删净：输出窗口内无 CARE（≥672）/FEED（≥696）残留。
    seq = [out["routes"]["actions"][i] for i in out["routes"]["routes"]["0"]]
    left = [(s, u, op[0]) for s, a in enumerate(seq) for u, op
            in retape_sheep._units(a) if isinstance(op, list) and op
            and ((op[0] == "CARE" and s >= 672) or (op[0] == "FEED" and s >= 696))]
    assert left == []
    # 清单形态：FEED→WHEAT 1（省饲料）、CARE→null；kind/step/槽位互斥恰一。
    for e in out["removed"]:
        assert set(e) == {"route", "step", "kind", "slot", "unit", "item",
                          "qty", "reason"}
        assert (e["slot"] is None) != (e["unit"] is None)
        if e["kind"] == "FEED":
            assert (e["item"], e["qty"]) == ("WHEAT", 1)
        else:
            assert (e["item"], e["qty"]) == (None, None)
        assert e["reason"].startswith("tail_")
    # 窗口内删点改 ["PASS"]；窗口外原样。
    assert _view(out["routes"], "0", 700) == {
        "farmer": ["PASS"], "hands": [["PASS"], ["PASS"]], "market": []}
    assert _view(out["routes"], "0", 600) == before["actions"][600]
    assert _view(out["routes"], "0", 695) == before["actions"][695]
    assert pkg == before


# ---------------------------------------------------------------------------
# ③ 闲置 HIRE 删、有役 HIRE 留（构造 hands 引用）
# ---------------------------------------------------------------------------
def test_idle_hire_removed_employed_hire_kept():
    # (a) 闲置：当日唯一 HIRE（m=0），其后 hands[0] 无指派 → 删（槽换 []）。
    pkg = _mk_pkg(719, markets={(700, 3): ["HIRE"]})
    out = retape_tail.retape_tail_savings(pkg)
    assert _removed_keys(out) == [(700, "HIRE", 3)]
    assert out["removed"][0]["item"] == "HAND" and out["removed"][0]["qty"] == 1
    assert _view(out["routes"], "0", 700)["market"] == [[], [], [], []]

    # (b) 有役：hands[0] 雇佣后有 HARVEST 指派 → 留，HARVEST 不动。
    pkg = _mk_pkg(719, markets={(700, 0): ["HIRE"]}, hands={(710, 0): ["HARVEST"]})
    out = retape_tail.retape_tail_savings(pkg)
    assert out["removed"] == []
    assert _view(out["routes"], "0", 710)["hands"][0] == ["HARVEST"]
    assert _view(out["routes"], "0", 700)["market"] == [["HIRE"]]

    # (c) 拿不准就不删：同日雇佣步之前 slot 0 已有指派（手尚未诞生，登记
    #     不一致）→ uncertain 保守保留。
    pkg = _mk_pkg(719, markets={(700, 0): ["HIRE"]}, hands={(697, 0): ["NORTH"]})
    out = retape_tail.retape_tail_savings(pkg)
    assert out["removed"] == []
    assert _view(out["routes"], "0", 700)["market"] == [["HIRE"]]

    # (d) 当日序对齐：同日两张 HIRE（m=0/1），hands[1] 有指派→第 2 张留、
    #     hands[0] 无指派→第 1 张删。
    pkg = _mk_pkg(719, markets={(696, 0): ["HIRE"], (696, 1): ["HIRE"]},
                  hands={(705, 1): ["WATER"]})
    out = retape_tail.retape_tail_savings(pkg)
    assert _removed_keys(out) == [(696, "HIRE", 0)]
    assert _view(out["routes"], "0", 696)["market"] == [[], ["HIRE"]]
    assert _view(out["routes"], "0", 705)["hands"] == [["PASS"], ["WATER"]]

    # (e) 窗口外 HIRE（<696）闲置也不删（误删即抛的红线面）。
    pkg = _mk_pkg(719, markets={(695, 0): ["HIRE"]})
    out = retape_tail.retape_tail_savings(pkg)
    assert out["removed"] == []
    assert _view(out["routes"], "0", 695)["market"] == [["HIRE"]]

    # 违抛：把 (b) 的有役 HIRE 硬删（伪造删除）→ 术后对账抛（非闲置 HIRE 被删）。
    pkg = _mk_pkg(719, markets={(700, 0): ["HIRE"]}, hands={(710, 0): ["HARVEST"]})
    bad = copy.deepcopy(pkg)
    _view(bad, "0", 700)["market"][0] = []
    forged = {"route": "0", "step": 700, "kind": "HIRE", "slot": 0, "unit": None,
              "item": "HAND", "qty": 1, "reason": "x"}
    with pytest.raises(RuntimeError, match="误删红"):
        retape_tail._audit_removals(pkg, bad, [forged])


# ---------------------------------------------------------------------------
# ④ HARVEST/卖单逐类不动
# ---------------------------------------------------------------------------
def test_harvest_and_market_orders_untouched():
    pkg = _mk_pkg(719,
                  farmers={672: ["PLANT", "MELON"], 680: ["WATER"],
                           690: ["HARVEST"], 700: ["HARVEST"], 705: ["CARE"],
                           710: ["NORTH"], 718: ["PLACE", "WOOL", 1000]},
                  hands={(675, 0): ["HARVEST"], (700, 1): ["PICKUP", "WOOL"],
                         (700, 8): ["FEED"], (712, 2): ["DROP"],
                         (715, 3): ["COLLECT_FERTILIZER"], (716, 4): ["FERTILIZE"],
                         (717, 5): ["DIG"], (718, 6): ["BUILD_PASTURE"],
                         (718, 7): ["BUILD_COOP"]},
                  markets={(696, 0): ["SELL", "WOOL", 5], (697, 1): ["SELL", "MILK", 2],
                           (700, 2): ["BUY_SEED", "MELON", 3],
                           (700, 3): ["BUY_PRODUCT", "WHEAT", 13],
                           (705, 4): ["BUY_ANIMAL", "COW", 2], (710, 5): ["BUY_LAND"],
                           (718, 6): ["SELL", "EGG", 1000], (718, 7): []})
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    # 仅两处负空间删除（CARE@705、FEED@700 h8）；HARVEST/卖单/BUY_*/空槽/移动/
    # 建造/种植等逐类逐槽原样。
    assert _removed_keys(out) == [(700, "FEED", "h8"), (705, "CARE", "F")]
    assert {e["kind"] for e in out["removed"]} <= {"CARE", "FEED", "HIRE"}
    for s in (690, 700, 718):                       # 动物格 HARVEST 照旧
        if s == 700:
            assert _view(out["routes"], "0", 700)["farmer"] == ["HARVEST"]
            assert _view(out["routes"], "0", 700)["hands"][1] == ["PICKUP", "WOOL"]
            assert _view(out["routes"], "0", 700)["hands"][8] == ["PASS"]
        else:
            assert _view(out["routes"], "0", s) == before["actions"][s]
    for s in (696, 697, 700, 705, 710, 718):        # 一切 market 单照旧
        assert _view(out["routes"], "0", s)["market"] == before["actions"][s]["market"]
    assert _view(out["routes"], "0", 718)["market"][7] == []   # 空槽位次不动
    for s, i in [(675, 0), (712, 2), (715, 3), (716, 4), (717, 5), (718, 6), (718, 7)]:
        assert _view(out["routes"], "0", s)["hands"][i] == \
            before["actions"][s]["hands"][i]
    assert pkg == before

    # 违抛：篡改输出 HARVEST / 卖单 → 术后对账抛「误删红」。
    bad = copy.deepcopy(out["routes"])
    _view(bad, "0", 700)["farmer"] = ["PASS"]
    with pytest.raises(RuntimeError, match="误删红"):
        retape_tail._audit_removals(pkg, bad, out["removed"])
    bad = copy.deepcopy(out["routes"])
    _view(bad, "0", 718)["market"][6][2] = 999
    with pytest.raises(RuntimeError, match="误删红"):
        retape_tail._audit_removals(pkg, bad, out["removed"])


# ---------------------------------------------------------------------------
# ⑤ 动作池共享不变量（他路由不受影响）
# ---------------------------------------------------------------------------
def test_action_pool_shared_copy_on_write():
    shared = {"farmer": ["CARE"], "hands": [["PASS"], ["FEED"]],
              "market": [["HIRE"], ["SELL", "WOOL", 3]]}
    filler = {"farmer": ["PASS"], "hands": [], "market": []}
    pkg = {"actions": [copy.deepcopy(shared), copy.deepcopy(filler)],
           "routes": {"0": [1] * 700 + [0] + [1] * 18,
                      "1": [1] * 600 + [0] + [1] * 118},
           "shops": []}
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    assert pkg == before
    # 路由 0（step 700）手术：CARE/FEED/HIRE 三删；路由 1（step 600）零影响
    # ——同池件窗口外引用不许被顺手删（写时复制核心不变量）。
    assert _removed_keys(out) == [(700, "CARE", "F"), (700, "FEED", "h1"),
                                  (700, "HIRE", 0)]
    assert all(e["route"] == "0" for e in out["removed"])
    assert _view(out["routes"], "1", 600) == shared
    assert _view(out["routes"], "0", 700) == {
        "farmer": ["PASS"], "hands": [["PASS"], ["PASS"]],
        "market": [[], ["SELL", "WOOL", 3]]}
    # 池不变量：共享原件零扰动；新件 append；指针只挪手术步。
    acts = out["routes"]["actions"]
    assert acts[0] == shared and acts[1] == filler
    assert len(acts) == 3
    assert out["routes"]["routes"]["0"][700] == 2
    assert out["routes"]["routes"]["1"][600] == 0
    assert all(i == 1 for k, i in enumerate(out["routes"]["routes"]["0"]) if k != 700)
    assert all(i == 1 for k, i in enumerate(out["routes"]["routes"]["1"]) if k != 600)

    # 同步共享：两路由同步引用同池件 → 各自独立 CoW，视图各自正确。
    pkg2 = {"actions": [copy.deepcopy(shared), copy.deepcopy(filler)],
            "routes": {"0": [1] * 700 + [0] + [1] * 18,
                       "1": [1] * 700 + [0] + [1] * 18},
            "shops": []}
    out2 = retape_tail.retape_tail_savings(pkg2)
    assert len(out2["removed"]) == 6
    for rid in ("0", "1"):
        assert _view(out2["routes"], rid, 700) == {
            "farmer": ["PASS"], "hands": [["PASS"], ["PASS"]],
            "market": [[], ["SELL", "WOOL", 3]]}
    assert out2["routes"]["actions"][0] == shared
    assert len(out2["routes"]["actions"]) == 4


# ---------------------------------------------------------------------------
# ⑥ 动物不饿死边界（d29 停喂最多累计 1 不触发）
# ---------------------------------------------------------------------------
def _simulate_unfed(feed_days, last_refresh_day=28):
    """引擎 _daily_refresh_animals 日结口径：fed_today→0 否则 +=1，≥2 逃走；
    日结只在 d0..d28 末发生（step 695 最后一次；d29→d30 转换不发生）。"""
    c = 0
    mx = 0
    escaped = False
    for d in range(last_refresh_day + 1):
        c = 0 if feed_days.get(d) else c + 1
        mx = max(mx, c)
        escaped = escaped or c >= 2
    return c, mx, escaped


def _feed_days(pkg, rid="0"):
    days = {}
    seq = [pkg["actions"][i] for i in pkg["routes"][rid]]
    for s, a in enumerate(seq):
        for _, op in retape_sheep._units(a):
            if isinstance(op, list) and op and op[0] == "FEED":
                days[s // 24] = True
    return days


def test_no_starvation_boundary():
    # 情形 A：逐日喂养（含 d28/d29）——术后 d29 FEED 删净、d0..d28 喂养日程
    # 逐日不变；模拟 consecutive_unfed 全程 0、不逃走。
    feeds_a = {d * 24: ["FEED"] for d in range(30)}
    pkg = _mk_pkg(719, farmers=feeds_a, hands={(700, 0): ["CARE"]})
    before_days = _feed_days(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    after_days = _feed_days(out["routes"])
    assert before_days == {d: True for d in range(30)}
    assert after_days == {d: True for d in range(29)}      # d29 停喂（已删）
    assert all(e["step"] >= 696 for e in out["removed"] if e["kind"] == "FEED")
    assert _simulate_unfed(after_days) == (0, 0, False)

    # 情形 B（边界钉）：d28 不喂（d28→d29 日结累计 1），d29 的 FEED 被删——
    # 其后无日结，consecutive_unfed 停在 1，最多累计 1 不触发逃走。
    feeds_b = {d * 24: ["FEED"] for d in range(30) if d != 28}
    pkg = _mk_pkg(719, farmers=feeds_b)
    out = retape_tail.retape_tail_savings(pkg)
    assert _removed_keys(out) == [(696, "FEED", "F")]
    c, mx, escaped = _simulate_unfed(_feed_days(out["routes"]))
    assert (c, mx, escaped) == (1, 1, False)

    # 模拟保真对照：若 d27+d28 都不喂（=违例删掉窗口 FEED 的效果），d28→d29
    # 日结翻 2 逃走——正是删除窗（FEED 仅 ≥696）与审计红线的理由。
    assert _simulate_unfed({d: True for d in range(30) if d not in (27, 28)}) \
        == (2, 2, True)
    bad = copy.deepcopy(out["routes"])
    _view(bad, "0", 27 * 24)["farmer"] = ["PASS"]          # 伪删窗口内（d27）FEED
    with pytest.raises(RuntimeError, match="误删红"):
        retape_tail._audit_removals(pkg, bad, out["removed"])


# ---------------------------------------------------------------------------
# ⑦ 真 r34a 实跑删除清单计数（evidence 可复算）+ 往返自检链
# ---------------------------------------------------------------------------
def test_real_r34a_tail_savings_evidence():
    assert _EVIDENCE.exists(), "缺一次性产物 evidence/tail_savings_realrun.json"
    saved = json.loads(_EVIDENCE.read_text(encoding="utf-8"))
    text, before, out, snap = _r34a_snapshot()
    assert snap == saved                      # 一次性产物=可复算（同源重算深等）
    # 计数合理性：逐条在窗、kind 封闭；真磁带尾盘负空间=CARE 删除（d28 纯浪费
    # 加成 613 + d29 166）；r34a 计划本就 d29 停喂（FEED=0）；d29 451 张 HIRE
    # 全有役（逐手有指派，拿不准就不删→0 删）。
    assert snap["removed_total"] == sum(snap["by_kind"].values()) == 779
    assert snap["by_kind"] == {"CARE": 779, "FEED": 0, "HIRE": 0}
    assert snap["by_kind_day"]["CARE"] == {"28": 613, "29": 166}
    assert snap["tail_hire_verdicts"] == {"idle": 0, "employed": 451,
                                          "uncertain": 0}
    assert snap["d28_feed_kept"] == 376      # d28 FEED 全保（饿死边界数据点）
    assert snap["routes"] == 41
    for e in out["removed"]:
        assert e["kind"] == "CARE" and 672 <= e["step"] <= 718
        assert e["unit"] in ("F",) or e["unit"].startswith("h")
    # 路由级计数全覆盖（41 路由逐路由入账）。
    assert set(snap["by_route"]) == set(before["routes"])
    assert sum(v["CARE"] for v in snap["by_route"].values()) == 779


def test_real_r34a_roundtrip_selfcheck():
    text = _r34a_text()
    pkg = retape_sheep._decode_routes(text)
    before = copy.deepcopy(pkg)
    out = retape_tail.retape_tail_savings(pkg)
    assert pkg == before                                  # 输入零改动
    # decode→surgery→encode 往返（retape_sheep 编码器自检链任一不过即抛）：
    # ①blob 区间外逐字节一致 ②回路一致 ③可编译 ④确定性双跑。
    new_text = retape_sheep._encode_routes(text, out["routes"])
    assert retape_sheep._decode_routes(new_text) == out["routes"]
    m_old, m_new = retape_sheep._BLOB_RE.search(text), \
        retape_sheep._BLOB_RE.search(new_text)
    b_old, b_new = text.encode("utf-8"), new_text.encode("utf-8")
    assert b_old[:m_old.span(1)[0]] == b_new[:m_new.span(1)[0]]
    assert b_old[m_old.span(1)[1]:] == b_new[m_new.span(1)[1]:]
    compile(new_text, "<verify>", "exec")
    assert retape_sheep._encode_routes(text, out["routes"]) == new_text
    # 池共享手术的池外证据：手术步=CoW 新件数、其余池件零扰动。
    assert len(out["routes"]["actions"]) - len(before["actions"]) == \
        _pool_growth(out)


def _pool_growth(out):
    """手术步数（CoW 新件数）= 去重后的 (route, step) 删除面。"""
    return len({(e["route"], e["step"]) for e in out["removed"]})
