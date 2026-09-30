# -*- coding: utf-8 -*-
"""build_prod（d1prod lab）：产线重生成（磁带手术）+ 三闸 + 守恒审计 + 断言协同。

红线（任务 D1）：**保留卖面现状（不碰焦窗/门层）**——既有市场单零改写/零删除/
零移动；唯一例外=加法系**追加** SELL EGG（goose_additive 既证"市场单仅追加"
清棚供养教义，B4b 棚溢毁麦→FEED 断粮→逃逸死因），审计单列 append-only。

变体手术（econ_solve.variant_menu 消费；四家族）：
1. fert_selfuse(rate)【肥料循环利用】：作物格 PASS 步→FERTILIZE（3 日效期隔
   离、窗口 age∈[1,5]、同格同窗不重施；引擎语义=棚存 1 袋、须同日 WATER）——
   自用 46%/放量 54%（D5 配比解）；投放由产出侧分流，卖单不动（少倾销不砸价）。
2. mw_trim(n)【奶毛减投】：branch 晚波 SHEEP 链→GOOSE（gl.convert_chain，
   WOOL 投放-1；蛋吸收 log=sink 补）+ goose_rhythm（仅鹅格 COLLECT→HARVEST
   补收蛋节奏，产线侧）。
3. additive(n_add)【26 头加法系/蛋麦配比】：goose_additive 纯加法件复用
   （BUY_LAND/BUY_ANIMAL/HIRE/合成手放养巡游），D5 买畜波次 d6-9、COOP 聚
   象限 0-1 近棚簇（逐路由空格探测）；市场单仅追加。
4. combo=fert_selfuse+additive 叠加。

每变体：孪生三闸（现金 min≥0/劳动 realized≥基线/棚容 held≤结构格，回滚 ≤3）
+ gl.audit_variant 量守恒/槽守恒/共享段恒等 + 卖面不变式审计 + gf.regen_assertions
断言协同（_GP_PLAN 计划表驱动）+ gf.assertion_probe 只读探针。
确定性：纯函数+固定序。CLI：python build_prod.py [--variants a,b]。
只写 orderbook_d1prod_lab/。
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import io
import json
import os
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))
if str(KSIM_DIR / "orderbook_goose_fullplan_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_fullplan_lab"))
if str(KSIM_DIR / "orderbook_goose_add_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_add_lab"))
_KAGGSIM = KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src" / "src-python"
if str(_KAGGSIM) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM))

from orderbook_r37 import retape_sheep as rs  # noqa: E402
import goose_line as gl  # noqa: E402
import goose_fullplan as gf  # noqa: E402  （regen_assertions/assertion_probe/gate_route/goose_rhythm/labor_table）
import goose_additive as ga  # noqa: E402  （RouteEditor/build_plans/apply_route 纯加法件）

BASE_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
BUILD_DIR = HERE / "build"
EVID_DIR = HERE / "evidence"

TRUNK = 144
TAIL = 648
N_STEPS = 719
MAX_ROLLBACK = 3
# 作物窗口（引擎 CROPS sha bc8a5487）：one-shot WHEAT age2-4/CARROT age2-3/
# MELON age6-12；ongoing TOMATO/STRAWBERRY 生产日施肥。施肥窗 age∈[1,5] 覆盖
# one-shot 全窗 + ongoing 前段；同格 3 日效期内不重施（fertilized_until_day）。
FERT_AGE_MIN, FERT_AGE_MAX = 1, 5
FERT_SPACING = 3
SELL_VERBS = ("SELL",)


# ============================================================ 肥料自用手术 ==
def _tile_crops(pkg, rid):
    """作物格种植周期：tile -> [plant_step,...]（同格多轮作；tr.events 全量口径，
    tile_visits 不含 PLANT/WATER/FERTILIZE——Track.tile_visits 过滤集限制）。"""
    tr = gl.Track(pkg, rid)
    pl = {tuple(t) for t in tr.placements()}
    crops = collections.defaultdict(list)
    for s, u, op, p, args in tr.events:
        if op == "PLANT" and tuple(p) not in pl:
            crops[tuple(p)].append(s)
    return tr, crops


def fert_selfuse(pkg, rid, rate, table, stats, n_collect):
    """作物格闲置 PASS 步→FERTILIZE：自用率≈rate×收集量（D5 46/54 配比解）。

    约束：FERTILIZE 须立于 PLANT 格；3 日效期同格不重施；窗口 age∈[1,5]；
    超收集量（棚存不足=引擎静默 no-op）不投。仅动产线 ops，卖单零触碰。
    """
    tr, crops = _tile_crops(pkg, rid)
    idxs = pkg["routes"][rid]
    # 单元步进动作与所在格
    unit_op = {}
    for s in range(TRUNK, TAIL):
        a = pkg["actions"][idxs[s]]
        for u, op in [("F", a.get("farmer") or ["PASS"])] + \
                     [("h%d" % k, h) for k, h in enumerate(a.get("hands") or [])
                      if isinstance(h, list)]:
            unit_op[(s, u)] = list(op) if op else ["PASS"]
    # 现有 FERTILIZE 落格日历（含既有件；tr.events 口径）
    fert_days = collections.defaultdict(set)
    for s, u, op, p, _args in tr.events:
        if op == "FERTILIZE":
            fert_days[tuple(p)].add(s // 24)
    # 目标件数=rate×收集量（自用/放量配比）
    target = int(round(rate * n_collect))
    have = sum(1 for op in unit_op.values() if op and op[0] == "FERTILIZE")
    need = max(0, target - have)
    # 候选：PASS 步立于作物格，格龄∈窗口，3 日隔离
    cands = []
    for (s, u), op in sorted(unit_op.items()):
        if op != ["PASS"]:
            continue
        p = tr.pos_at.get((s, u))
        if not p or tuple(p) not in crops:
            continue
        d = s // 24
        ages = [d - (ps // 24) for ps in crops[tuple(p)]]
        age = min(ages, key=lambda x: abs(x - 3))
        if not (FERT_AGE_MIN <= age <= FERT_AGE_MAX):
            continue
        if any(abs(d - dd) < FERT_SPACING for dd in fert_days[tuple(p)]):
            continue
        cands.append((s, u, tuple(p), d))
    for s, u, tile, d in cands:
        if need <= 0:
            break
        idxs2, _i, act = gl._cow(pkg, rid, s)
        old = None
        if u == "F":
            old = list(act.get("farmer") or [])
            act["farmer"] = ["FERTILIZE"]
        else:
            k = int(u[1:])
            hands = act.setdefault("hands", [])
            while len(hands) <= k:
                hands.append(["PASS"])
            old = list(hands[k])
            hands[k] = ["FERTILIZE"]
        gl._commit(pkg, idxs2, s, act, table, rid, "fert_selfuse",
                   {"unit": u, "tile": list(tile), "day": d, "from": old,
                    "to": ["FERTILIZE"]})
        fert_days[tile].add(d)
        stats["fert_selfuse_ops"] += 1
        need -= 1
    stats["fert_target"] = target
    stats["fert_have_before"] = have
    stats["fert_unmet"] = need
    return stats


# ============================================================ 奶毛减投 ==
def mw_trim(pkg, rid, n, table, stats):
    """branch 晚波 SHEEP（或 COW）链→GOOSE ×n：WOOOL 投放-1/蛋吸收补。"""
    if n <= 0:
        return stats
    chains = gl.route_chains(pkg, rid)
    before_goose = {tuple(c["tile"]) for c in chains
                    if c["species"] == "GOOSE" and c.get("tile")}
    branch = [c for c in chains if c["pl_step"] >= TRUNK]
    need = n
    for from_sp in ("SHEEP", "COW"):
        while need > 0:
            cand = [c for c in branch if c["species"] == from_sp and c.get("tile")]
            if not cand:
                break
            ch = cand[-1]
            rc = gl.convert_chain(pkg, rid, ch, "GOOSE", table)
            if rc != "ok":
                stats["convert_blocked"] += 1
                break
            branch.remove(ch)
            need -= 1
            stats["converted"] += 1
    # 收蛋节奏仅补**新换**鹅格（既有鹅格基线节奏不动=劳动预算红线）
    ch2 = gl.route_chains(pkg, rid)
    new_tiles = [c["tile"] for c in ch2 if c["species"] == "GOOSE" and c.get("tile")
                 and tuple(c["tile"]) not in before_goose]
    if new_tiles:
        gf.goose_rhythm(pkg, rid, new_tiles, table, stats)
    return stats


# ============================================================ 加法系 ==
def _occupied_tiles(pkg, rid):
    tr = gl.Track(pkg, rid)
    occ = set()
    for t in tr.placements():
        occ.add(tuple(t))
    for tile, bs in tr.builds().items():
        if bs:
            occ.add(tuple(tile))
    for _s, _u, op, p, _args in tr.events:
        if op in ("PLANT", "WATER", "HARVEST"):
            occ.add(tuple(p))
    for t in ga.SHED_TILES:
        occ.add(tuple(t))
    return occ


def d5_goose_tiles(pkg, rid):
    """D5 聚象限 0-1（y≤4）近棚空格簇；不足回落 SE 近棚簇（ga 原件）。"""
    occ = _occupied_tiles(pkg, rid)
    shed = (4, 4)
    free = [(x, y) for y in range(10) for x in range(10) if (x, y) not in occ]
    top = [t for t in free if t[1] <= 4]
    top.sort(key=lambda t: (abs(t[0] - shed[0]) + abs(t[1] - shed[1]), t))
    if len(top) >= 10:
        return top[:10]
    return list(ga.GOOSE_TILES)


def additive_route(pkg_base, work, rid, n_add, table, stats, plan_cache):
    """纯加法：ga.build_plans/apply_route 复用（市场单仅追加）。

    波次：现金门控（SE 锁地 4000+首波鹅）——D5 d6-9 波次被本磁带现金曲线否决
    （d10 首个大回款、d11 才买得起地+鹅），wave 窗=ga 原件 [6,17) 门控实取。
    落位：SE 近棚紧凑簇（Q0-2 被作物/畜群占满，实测空格全在 SE=聚簇非散布）。"""
    ga.GOOSE_TILES = d5_goose_tiles(pkg_base, rid)
    base_roll = plan_cache["rolls"][rid]
    plan = ga.build_plans(pkg_base, [rid], {rid: base_roll}, n_add)[rid]
    if not plan["waves"]:
        stats["additive_no_wave"] += 1
        plan_cache["plans"][rid] = plan
        return stats
    sub = ga.apply_route(pkg_base, work, rid, plan, table)
    stats.update(sub)
    plan_cache["plans"][rid] = plan
    return stats


# ============================================================ 卖面审计 ==
def sell_face_audit(pkg_base, pkg_var, allow_append_egg):
    """卖面不变式（红线=保留卖面现状）：**SELL 单逐拍逐槽逐字不变**（产线侧手术
    零触碰卖面）；唯一白名单=加法系追加 SELL EGG（清棚供养，append-only）。
    买单内容改写（convert_chain 换种）与追加（BUY_*/HIRE）=产线侧合法手术，
    单独计数登记（不属卖面）。"""
    sell_ok = True
    appended = collections.Counter()
    buy_rewrites = 0
    violations = []
    cap_ok = True
    prefix_ok = True
    for rid in pkg_base["routes"]:
        ib, iw = pkg_base["routes"][rid], pkg_var["routes"][rid]
        for s in range(N_STEPS):
            mb = pkg_base["actions"][ib[s]].get("market") or []
            mw = pkg_var["actions"][iw[s]].get("market") or []
            bs = [o for o in mb if isinstance(o, list) and o and o[0] in SELL_VERBS]
            vs = [o for o in mw if isinstance(o, list) and o and o[0] in SELL_VERBS]
            extra = vs[len(bs):]
            if vs[:len(bs)] != bs:
                sell_ok = False
                violations.append((rid, s, "sell_rewritten"))
            for o in extra:
                if not (allow_append_egg and o[1] == "EGG"):
                    sell_ok = False
                    violations.append((rid, s, "sell_appended:%s" % (o[1],)))
            for o in mw[len(mb):]:
                key = "%s:%s" % (o[0], o[1] if len(o) > 1 else "")
                appended[key] += 1
            if len(mw) > 10:
                cap_ok = False
            if len(mw) < len(mb):
                prefix_ok = False
            for i, o in enumerate(mw):
                if i < len(mb) and o != mb[i]:
                    buy_rewrites += 1
    return {"sell_orders_invariant": sell_ok,
            "n_sell_violations": len(violations),
            "violations_sample": violations[:5],
            "appended_orders": dict(appended),
            "buy_order_rewrites_chain_convert": buy_rewrites,
            "additive_slot_caliber": {"orders_append_only": bool(prefix_ok),
                                      "market_cap_10": bool(cap_ok)},
            "sell_appended_only_egg": all(
                (k.startswith("SELL:") and k == "SELL:EGG") or not k.startswith("SELL:")
                for k in appended)}


# ============================================================ 包写盘 ==
def write_package(vid, main_text, base_text, table):
    d = BUILD_DIR / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "main.py").write_text(main_text, encoding="utf-8")
    main_bytes = main_text.encode("utf-8")
    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w:gz") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    tar_bytes = tar_buf.getvalue()
    (d / "submission.tar.gz").write_bytes(tar_bytes)
    man = {
        "form": vid, "entry": "_hs_agent",
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes),
        "diff_scope": "_R108_DATA blob + 外壳断言重生成块（_GP_PLAN）——产线 ops 手术"
                      "+（加法系）市场单仅追加；既有卖面零改写",
        "n_change_rows": len(table),
    }
    (d / "build_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    return d, man


# ============================================================ 主构建 ==
def build_one(vid, spec, base_text, pkg_base, base_rolls):
    """单变体构建：手术→孪生三闸（回滚 ≤3）→守恒/卖面审计→断言协同→写盘。"""
    t0 = time.perf_counter()
    from kaggsim.serve import Serve  # noqa: WPS433
    rids = sorted(pkg_base["routes"], key=lambda k: int(k))
    n_collect = {}
    for rid in rids:
        tr = gl.Track(pkg_base, rid)
        n_collect[rid] = sum(1 for _tile, vs in tr.tile_visits().items()
                             for _s, _u, op in vs if op == "COLLECT_FERTILIZER")
    work = copy.deepcopy(pkg_base)
    table = []
    stats = collections.Counter()
    route_rows = []
    rollback_rows = []
    srv = Serve()
    try:
        for rid in rids:
            n_rb = 0
            while True:
                work["routes"][rid] = list(pkg_base["routes"][rid])
                table[:] = [r for r in table if r["route"] != rid]
                sub = []
                st = collections.Counter()
                # 手术（按家族；回滚=减档）
                if spec["fert_u"] > 0:
                    fert_selfuse(work, rid, max(0.0, spec["fert_u"] - 0.12 * n_rb),
                                 sub, st, n_collect[rid])
                if spec["mw_trim"] > 0:
                    mw_trim(work, rid, max(0, spec["mw_trim"] - n_rb), sub, st)
                if spec["g_add"] > 0:
                    plan_cache = {"rolls": base_rolls, "plans": {}}
                    additive_route(pkg_base, work, rid,
                                   max(0, spec["g_add"] - 2 * n_rb), sub, st, plan_cache)
                table.extend(sub)
                stats.update(st)
                v = gl._rollout(work, rid, 780010, srv=srv)
                row = gf.gate_route(base_rolls[rid], v)
                row["route"] = rid
                row["n_rollbacks"] = n_rb
                row["stats"] = dict(st)
                if row["ok"] or n_rb >= MAX_ROLLBACK:
                    route_rows.append(row)
                    break
                n_rb += 1
                rollback_rows.append(
                    {"route": rid, "iter": n_rb,
                     "why": {"cash_ok": row["cash_ok"], "labor_ok": row["labor_ok"],
                             "cap_ok": row["cap_ok"],
                             "min_money": [row["min_money_base"], row["min_money_var"]],
                             "realized": [row["realized_base"], row["realized_var"]]}})
                stats.subtract(st)
                stats = +stats
        rs._pool_residue_sweep(work)
        rows = []
        for rid in rids:
            arch = collections.Counter(c["species"] for c in gl.route_chains(work, rid))
            rows.append({"route": rid, "target": dict(arch)})
        audit = gl.audit_variant(pkg_base, work, table, rows)
    finally:
        srv.close()
    audit["sell_face"] = sell_face_audit(pkg_base, work,
                                         allow_append_egg=(spec["g_add"] > 0))
    if spec["g_add"] > 0:
        # 加法系槽口径（goose_additive 既证）：市场单仅追加 + ≤10 帽；legacy
        # 槽审计不识别加法追加 → 以加法口径判定（尾段共享组发散=追加手术写时
        # 复制解组，goose_add 基线 56 处既证；trunk 零扰动）
        adv = audit["sell_face"]["additive_slot_caliber"]
        audit["slot_ok_legacy"] = audit.get("slot_ok")
        audit["slot_ok"] = bool(adv["orders_append_only"] and adv["market_cap_10"]
                               and audit["sell_face"]["sell_orders_invariant"])
    n_fert_base = {}
    for rid in rids:
        tr = gl.Track(pkg_base, rid)
        n_fert_base[rid] = sum(1 for _s, _u, op, _p, _a in tr.events if op == "FERTILIZE")
    n_converted = sum(1 for r in table if r["kind"] == "fert_selfuse")
    audit["fert_disposition"] = {
        "target_rate": spec["fert_u"],
        "ops_converted": n_converted,
        "collect_total": sum(n_collect.values()),
        "fert_ops_base_total": sum(n_fert_base.values()),
        "achieved_rate": round((sum(n_fert_base.values()) + n_converted)
                               / max(1, sum(n_collect.values())), 3)}

    # ---- 断言协同（_GP_PLAN 计划表驱动）----
    new_blob = rs._encode_routes(base_text, work)
    final_text, assert_regen = gf.regen_assertions(new_blob, work)
    pkg_dir, man = write_package(vid, final_text, base_text, table)
    probe = gf.assertion_probe(pkg_dir / "main.py")
    labor = {rid: gf.labor_table(work, rid) for rid in rids[:3]}

    out = {
        "variant": vid, "spec": spec,
        "stats": dict(stats),
        "n_table_rows": len(table),
        "n_bad_routes": sum(1 for r in route_rows if not r["ok"]),
        "route_gates_summary": {
            "routes": len(route_rows),
            "ok": sum(1 for r in route_rows if r["ok"]),
            "cash_ok": sum(1 for r in route_rows if r["cash_ok"]),
            "labor_ok": sum(1 for r in route_rows if r["labor_ok"]),
            "cap_ok": sum(1 for r in route_rows if r["cap_ok"]),
            "twin_money_mean_base": round(sum(r["final_money_base"] for r in route_rows)
                                          / max(1, len(route_rows)), 1),
            "twin_money_mean_var": round(sum(r["final_money_var"] for r in route_rows)
                                         / max(1, len(route_rows)), 1),
        },
        "rollbacks": rollback_rows[:12],
        "audit": {k: audit[k] for k in ("conservation", "slot_ok", "shared_seg")
                  if k in audit},
        "audit_conservation_match": sum(1 for c in audit.get("conservation", [])
                                        if c.get("match")),
        "sell_face": audit["sell_face"],
        "fert_disposition": audit["fert_disposition"],
        "assert_regen": {k: assert_regen[k] for k in ("regenerated", "new_invariants",
                                                      "semantics")},
        "assert_probe": probe,
        "manifest": man,
        "pkg_dir": str(pkg_dir),
        "labor_sample": {k: {"animal_share": v["animal_share"],
                             "op_lines": v["op_lines"]} for k, v in labor.items()},
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    return out, work


def main(variants_sel=None):
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    import econ_solve as es  # noqa: WPS433
    base_text = BASE_MAIN.read_text(encoding="utf-8")
    pkg_base = rs._decode_routes(base_text)
    rids = sorted(pkg_base["routes"], key=lambda k: int(k))
    from kaggsim.serve import Serve  # noqa: WPS433
    srv = Serve()
    try:
        base_rolls = {rid: gl._rollout(pkg_base, rid, 780010, srv=srv) for rid in rids}
    finally:
        srv.close()
    rows = es.enumerate_solve()
    menu = es.variant_menu(rows)
    sel = variants_sel or list(menu)
    out = {
        "version": "d1-build/1.0",
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "redline": "保留卖面现状：既有市场单零改写；唯一追加=加法系 SELL EGG"
                   "（清棚供养，append-only）；不碰焦窗/门层代码面",
        "variants": {},
    }
    for vid in sel:
        if vid not in menu:
            continue
        spec = {"g_add": menu[vid]["g_add"], "mw_trim": menu[vid]["mw_trim"],
                "fert_u": menu[vid]["fert_u"]}
        print("build", vid, spec, flush=True)
        rec, _w = build_one(vid, spec, base_text, pkg_base, base_rolls)
        out["variants"][vid] = rec
        print("  bad_routes:", rec["n_bad_routes"], "probe:", rec["assert_probe"].get("passed"),
              "twin:", rec["route_gates_summary"]["twin_money_mean_base"], "->",
              rec["route_gates_summary"]["twin_money_mean_var"],
              "elapsed:", rec["elapsed_s"], flush=True)
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    (EVID_DIR / "build_prod.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", default="")
    args = ap.parse_args()
    sel = [v for v in args.variants.split(",") if v] or None
    main(sel)
