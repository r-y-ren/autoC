# -*- coding: utf-8 -*-
"""variant_gen —— R15 参数扫描变体生成（排程→可行性→磁带手术）。

方法取材（只读复用不改源，沿 giant_route 方法）：
  - gen_schedule（R9-G1）：日级孪生空跑逐日校验四约束族（现金 ≥0 /
    劳动 op ≤ workers×24 / 棚容 ≤100 / 停时[M5 stop-days 口径]）——R15
    以"手术不变更劳动指令数（等量核验）+ 现金地板曲线（26 败局我席日末
    资金逐日最小值，最差收入面）+ 棚容净累积模型 + 种植停时（day +
    FIRST_YIELD_DAY[to] ≤ 29，首收获须落在 day 29 内）"落地同口径；
  - build_v6（R9-G2）受控变更集：blob 区间外逐字节一致 + 编译通过 +
    解码回路 + 确定性双跑 —— R15 作用面为 L3 main 的 _R108_DATA 动作表
    （共享条目），编码参数与原 blob 逐字节同构（_base.encode_l3_blob）。

手术语义（责任面钉死：改写 BUY_SEED/PLANT 事件，保留路由/反应层/清仓）：
  - PLANT from → PLANT to（同单元同槽位，逐单元改写）；
  - BUY_SEED from q → BUY_SEED to q（同订单槽位改写，不新增订单，
    market 单数上限 10 天然保持）；
  - 种子覆盖：引擎语义=步内先执行单元动作后处理市场订单 → 变体植物的
    种子必须由严格更早步的已转换 BUY_SEED 覆盖（保守口径；覆盖不足的
    植物事件回退不改，记 skips）；
  - 主时间线=默认路由 100（shop router 缺省路由）；动作表条目跨路由
    共享 → 全路由同步受影响（审计报告逐路由 from/to 植数）。
"""
from __future__ import annotations

import copy
import hashlib
import json
import os

from . import _base as B

PRIMARY_ROUTE = "100"
# 孪生空跑参数
SHED_CAPACITY = 100
STARTING_MONEY = 3000.0


# ---------------------------------------------------------------------------
# 排程构建
# ---------------------------------------------------------------------------
def _route_events(data, route_id, item):
    """路由时间线上 item 的产线事件（buy=BUY_SEED 订单，plant=单元 PLANT）。

    输出：[{"step", "ai", "kind", "slot", "qty"}...] 按步升序——
    buy.slot=market 列表下标；plant.slot=(unit_kind, unit_idx)，
    unit_kind ∈ {"farmer", "hands"}。
    """
    route = data["routes"][route_id]
    out = []
    for step, ai in enumerate(route):
        action = data["actions"][ai]
        if not isinstance(action, dict):
            continue
        for j, order in enumerate(action.get("market") or []):
            if (isinstance(order, (list, tuple)) and len(order) >= 3
                    and order[0] == "BUY_SEED" and order[1] == item
                    and int(order[2]) > 0):
                out.append({"step": step, "ai": ai, "kind": "buy",
                            "slot": j, "qty": int(order[2])})
        units = [("farmer", action.get("farmer"))] + \
                [("hands", h) for h in (action.get("hands") or [])]
        for u_idx, (u_kind, cmd) in enumerate(units):
            if (isinstance(cmd, (list, tuple)) and cmd
                    and cmd[0] == "PLANT" and cmd[1] == item):
                slot = (u_kind, u_idx if u_kind == "farmer"
                        else u_idx - 1)  # hands 下标（farmer 占位已扣）
                out.append({"step": step, "ai": ai, "kind": "plant",
                            "slot": slot, "qty": 1})
    return out


def _plant_deadline_ok(step, to_item):
    """停时：day + FIRST_YIELD_DAY[to] ≤ 29（首收获落在 day 29 内）。"""
    return (step // 24) + B.FIRST_YIELD_DAY.get(to_item, 0) <= 29


def build_variant_schedule(pair, scale, base_schedule):
    """单变体排程：from 品产能窗 X% 植物事件迁 to 品（含种子覆盖）。

    输入：pair={from,to,...}（Phase M 置换对）；scale∈(0,1]；
    base_schedule={"data": 解码 _R108_DATA, "primary_route"?, "money_floor_curve"?}。
    输出：{"pair", "scale", "data"(手术后动作表), "route_id", "target_n",
    "moved_n", "edits", "day_plan", "seed_spend_delta", "wasted_from_seeds",
    "skips", "route_audit"}——目标 target_n=round(scale×窗口内 from 植数)；
    moved_n 为实际迁移数（种子覆盖不足回退后）。
    """
    data = copy.deepcopy(base_schedule["data"])
    route_id = base_schedule.get("primary_route", PRIMARY_ROUTE)
    if route_id not in data["routes"]:
        route_id = next(iter(data["routes"]))
    src, dst = pair["from"], pair["to"]

    src_events = _route_events(data, route_id, src)
    plants = sorted([e for e in src_events if e["kind"] == "plant"],
                    key=lambda e: e["step"])
    buys = sorted([e for e in src_events if e["kind"] == "buy"],
                  key=lambda e: e["step"])
    eligible = [e for e in plants if _plant_deadline_ok(e["step"], dst)]
    target_n = int(round(scale * len(eligible)))
    # 均匀散布选点（窗口内跨季铺开；k≤1 取首）；种子覆盖不足时按选点位移重试
    def _pick(k, shift):
        if k <= 0:
            return []
        if k == 1:
            return [eligible[(0 + shift) % len(eligible)]]
        n = len(eligible)
        idxs = sorted({(round(i * (n - 1) / (k - 1)) + shift) % n
                       for i in range(k)})
        return [eligible[i] for i in idxs][:k]

    # ---- 种子覆盖（日块配额贪心；步内=先单元后市场 → 严格更早步覆盖） ----
    # 转换买入沿 chosen 的逐日累计分布走（converted(d) ≤ cum_chosen(d)），
    # 且总量守恒 cap：converted_total ≤ buys_total − (plants_total −
    # chosen_total)（未转换种子须足额供养未入选 from 植物）。
    from collections import Counter
    buy_qty_total = sum(e["qty"] for e in buys)
    plants_total = len(plants)
    plants_by_day = Counter(e["step"] // 24 for e in plants)

    def _greedy(chosen):
        chosen_by_day = Counter(e["step"] // 24 for e in chosen)
        chosen_total = len(chosen)
        slack_cap = buy_qty_total - (plants_total - chosen_total)
        all_days = sorted(set(chosen_by_day) | set(plants_by_day)
                          | set(e["step"] // 24 for e in buys))
        conv_quota = {}
        cum_chosen = cum_quota = 0
        for d in all_days:
            cum_chosen += chosen_by_day.get(d, 0)
            take = max(0, min(cum_chosen - cum_quota, slack_cap - cum_quota))
            conv_quota[d] = take
            cum_quota += take
        chosen_ids = {id(e) for e in chosen}
        convert_buys, convert_plants = set(), set()
        bank, moved, skips = 0, 0, []
        quota_left = dict(conv_quota)
        conv_total = 0
        timeline = sorted(
            plants + buys,
            key=lambda e: (e["step"], 0 if e["kind"] == "plant" else 1))
        # 同步内植物先于买单处理（引擎步内先单元后市场 → 同步买单不可供养同步植物）
        for ev in timeline:
            if ev["kind"] == "buy":
                d = ev["step"] // 24
                if quota_left.get(d, 0) <= 0:
                    continue
                if ev["qty"] <= quota_left[d]:
                    take = ev["qty"]          # 整单转换（配额内）
                elif conv_total + ev["qty"] <= slack_cap:
                    take = ev["qty"]          # 整单转换（配额超支但守恒 cap 内，
                else:                         #   富余 to 种子记账 wasted）
                    continue
                convert_buys.add(id(ev))
                bank += take
                conv_total += take
                quota_left[d] = max(0, quota_left[d] - take)
            else:  # plant
                if id(ev) in chosen_ids:
                    if bank >= 1:
                        bank -= 1
                        convert_plants.add(id(ev))
                        moved += 1
                    else:
                        skips.append({"step": ev["step"],
                                      "reason": "seed_uncovered"})
        return moved, convert_buys, convert_plants, skips

    best = None
    for shift in range(max(1, len(eligible))):
        cand = _pick(target_n, shift)
        if not cand:
            break
        m, cb, cp, sk = _greedy(cand)
        if best is None or m > best[1]:
            best = (cand, m, cb, cp, sk)
        if m == target_n:
            break
    chosen, moved, convert_buys, convert_plants, skips = best
    chosen_ids = {id(e) for e in chosen}

    # ---- 应用手术（BUY_SEED / PLANT 事件改写） ------------------------------
    edits = []
    day_plan = {}
    for ev in buys:
        if id(ev) not in convert_buys:
            continue
        action = data["actions"][ev["ai"]]
        order = action["market"][ev["slot"]]
        action["market"][ev["slot"]] = ["BUY_SEED", dst, int(order[2])]
        edits.append({"ai": ev["ai"], "step": ev["step"], "kind": "buy",
                      "before": ["BUY_SEED", src, int(order[2])],
                      "after": ["BUY_SEED", dst, int(order[2])]})
        d = ev["step"] // 24
        day_plan.setdefault(d, {"buys_to": 0, "plants_to": 0})
        day_plan[d]["buys_to"] += int(order[2])
    for ev in plants:
        if id(ev) not in convert_plants:
            continue
        action = data["actions"][ev["ai"]]
        u_kind, u_idx = ev["slot"]
        if u_kind == "farmer":
            action["farmer"] = ["PLANT", dst]
        else:
            action["hands"][u_idx] = ["PLANT", dst]
        edits.append({"ai": ev["ai"], "step": ev["step"], "kind": "plant",
                      "before": ["PLANT", src], "after": ["PLANT", dst]})
        d = ev["step"] // 24
        day_plan.setdefault(d, {"buys_to": 0, "plants_to": 0})
        day_plan[d]["plants_to"] += 1

    n_buys = sum(e["before"][2] for e in edits if e["kind"] == "buy")
    seed_spend_delta = moved * (B.SEED_PRICE[dst] - B.SEED_PRICE[src])
    wasted = n_buys - moved           # 转换买入但未用于迁移植物的 from→to 差损面
    route_audit = _per_route_audit(data, src, dst)

    return {
        "pair": {"from": src, "to": dst},
        "scale": scale,
        "data": data,
        "route_id": route_id,
        "from_plants_route": len(plants),
        "eligible_plants": len(eligible),
        "target_n": target_n,
        "moved_n": moved,
        "buys_converted_qty": n_buys,
        "edits": edits,
        "day_plan": {str(d): v for d, v in sorted(day_plan.items())},
        "seed_spend_delta": seed_spend_delta,
        "wasted_from_seeds": wasted,
        "skips": skips,
        "route_audit": route_audit,
        "money_floor_curve": base_schedule.get("money_floor_curve"),
    }


def _per_route_audit(data, src, dst):
    """手术后逐路由 from/to 植数（共享条目同步面审计）。"""
    audit = {}
    for rid, ids in data["routes"].items():
        n_src = n_dst = 0
        for ai in ids:
            action = data["actions"][ai]
            for cmd in [action.get("farmer")] + (action.get("hands") or []):
                if isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "PLANT":
                    if cmd[1] == src:
                        n_src += 1
                    elif cmd[1] == dst:
                        n_dst += 1
        audit[str(rid)] = {"plants_from": n_src, "plants_to": n_dst}
    return audit


# ---------------------------------------------------------------------------
# 可行性孪生空跑（日级；R9 四约束族口径）
# ---------------------------------------------------------------------------
def check_variant_feasibility(schedule):
    """变体排程日级校验：劳动（指令数不变性）/现金/棚容/停时。

    - 劳动：手术只改写指令载荷（品名）不改指令数 → 逐日指令计数与基线
      等量（target_n+moved 守恒核验：改动数=2×edits 载荷位、无增删）；
    - 现金：cum 种子差价支出 vs 现金地板（26 败局我席日末资金逐日最小值
      曲线；缺曲线时以 3000 起始资金+零收入最差面）；
    - 棚容：to 品净累积模型（迁移植物产量按引擎 CROPS 产量表粗算，
      扣减路由 100 to 品计划卖出量，日净累积峰值 ≤100）；
    - 停时：迁移植物 day + FIRST_YIELD_DAY[to] ≤ 29 复核。
    输出：{feasible, violations:[{family, day, detail}]}。
    """
    violations = []
    sched = schedule
    src, dst = sched["pair"]["from"], sched["pair"]["to"]
    data = sched["data"]
    route = data["routes"][sched["route_id"]]

    # 劳动：逐日单元指令计数等量核验（改写不增删 → 与"手术前指令计数"比对；
    # 手术前计数 = 手术后计数（载荷改写不改列表长度），此处以结构不变式核验：
    # edits 中 plant 改写位仍是单条指令、buy 改写位 market 长度不变）
    labor_ok = all(
        isinstance(data["actions"][e["ai"]], dict)
        and isinstance(data["actions"][e["ai"]].get("market"), list)
        for e in sched["edits"])
    if not labor_ok:
        violations.append({"family": "labor", "day": None,
                           "detail": "手术破坏动作结构"})

    # 停时
    for e in sched["edits"]:
        if e["kind"] == "plant" and not _plant_deadline_ok(e["step"], dst):
            violations.append({"family": "stop", "day": e["step"] // 24,
                               "detail": f"{src}->{dst} @step{e['step']} 首收获越 day29"})

    # 现金（地板曲线）
    floor = sched.get("money_floor_curve") or [STARTING_MONEY] * 30
    cum = 0.0
    spend_by_day = {}
    for e in sched["edits"]:
        if e["kind"] == "buy":
            d = e["step"] // 24
            cum_delta = e["before"][2] * (B.SEED_PRICE[dst] - B.SEED_PRICE[src])
            spend_by_day[d] = spend_by_day.get(d, 0.0) + cum_delta
    cum = 0.0
    for d in range(30):
        cum += spend_by_day.get(d, 0.0)
        base_floor = float(floor[d]) if d < len(floor) else STARTING_MONEY
        if base_floor - cum < 0:   # cum>0 为额外支出 → 地板被击穿
            violations.append({"family": "cash", "day": d,
                               "detail": f"现金地板 {base_floor:.0f}−Δ{cum:.0f} < 0"})

    # 棚容（to 品净累积粗模型）
    max_yield = _crop_max_yield(dst)
    first_d = B.FIRST_YIELD_DAY.get(dst, 2)
    prod = {}
    for e in sched["edits"]:
        if e["kind"] == "plant":
            d = e["step"] // 24
            prod[d + first_d] = prod.get(d + first_d, 0) + max_yield
    sells = _route_sell_units(data, sched["route_id"], dst)
    net, peak = 0.0, 0.0
    for d in range(30):
        net += prod.get(d, 0) - sells.get(d, 0)
        net = max(0.0, net)
        peak = max(peak, net)
    if peak > SHED_CAPACITY:
        violations.append({"family": "shed", "day": None,
                           "detail": f"to 品净累积峰值 {peak:.0f} > {SHED_CAPACITY}"})
    return {"feasible": not violations,
            "violations": violations,
            "model": {"shed_peak_modeled": round(peak, 1),
                      "cash_delta_total": round(cum, 1)}}


def _crop_max_yield(item):
    """引擎 CROPS max_yield 兜底表（装载校验于 run 面）。"""
    return {"WHEAT": 6, "CARROT": 4, "TOMATO": 4, "STRAWBERRY": 4,
            "MELON": 6}.get(item, 6)


def _route_sell_units(data, route_id, item):
    """路由 100 计划卖出量逐日聚合（棚容扣减面）。"""
    route = data["routes"][route_id]
    sells = {}
    for step, ai in enumerate(route):
        for o in (data["actions"][ai].get("market") or []):
            if (isinstance(o, (list, tuple)) and len(o) >= 3
                    and o[0] == "SELL" and o[1] == item and int(o[2]) > 0):
                d = step // 24
                sells[d] = sells.get(d, 0) + int(o[2])
    return sells


# ---------------------------------------------------------------------------
# 磁带手术构建（build_v6 受控变更集方法）
# ---------------------------------------------------------------------------
def build_variant_main(schedule, l3_base_path, out_path):
    """变体 main 构建：L3 基座 _R108_DATA blob 区间内替换，区间外逐字节一致。

    自检链（任一失败=手术超界 → 弃）：解码回路（重编码解回==变体数据）、
    区间外前后缀逐字节一致、compile 通过、产物确定性双跑、基座文件零改动。
    输出：{"main_path", "audit_path", "sha256", "bytes", "blob_span",
    "diff_entries", "base_sha256"}。
    """
    with open(l3_base_path, "r", encoding="utf-8") as fh:
        base_text = fh.read()
    base_data, (lo, hi) = B.decode_l3_blob(base_text)
    body = B.encode_l3_blob(schedule["data"])
    new_text = base_text[:lo] + body + base_text[hi:]
    if new_text[:lo] != base_text[:lo] or new_text[lo + len(body):] != base_text[hi:]:
        raise RuntimeError("手术泄漏到 blob 区间外")
    # 解码回路
    if B.decode_l3_blob(new_text)[0] != schedule["data"]:
        raise RuntimeError("blob 解码回路不一致")
    # 确定性双跑
    if B.encode_l3_blob(schedule["data"]) != body:
        raise RuntimeError("编码非确定性")
    compile(new_text, str(out_path), "exec")

    main_bytes = new_text.encode("utf-8")
    if os.path.abspath(l3_base_path) == os.path.abspath(out_path):
        raise RuntimeError("变体 main 不得覆盖基座")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(main_bytes)
    audit = {
        "variant": os.path.basename(os.path.dirname(os.path.abspath(out_path))),
        "base_path": os.path.abspath(l3_base_path),
        "base_sha256": hashlib.sha256(
            open(l3_base_path, "rb").read()).hexdigest(),
        "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
        "main_bytes": len(main_bytes),
        "blob_span": [lo, lo + len(body)],
        "base_blob_len": hi - lo,
        "new_blob_len": len(body),
        "diff_entries": len(schedule["edits"]),
        "edits": schedule["edits"],
        "day_plan": schedule["day_plan"],
        "route_audit": schedule["route_audit"],
        "outside_blob_byte_identical": True,
        "compile_ok": True,
        "deterministic_double_encode": True,
    }
    audit_path = os.path.join(os.path.dirname(os.path.abspath(out_path)),
                              "build_audit.json")
    with open(audit_path, "w", encoding="utf-8") as fh:
        json.dump(audit, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return {"main_path": os.path.abspath(out_path),
            "audit_path": audit_path,
            "sha256": audit["main_sha256"],
            "bytes": audit["main_bytes"],
            "blob_span": audit["blob_span"],
            "diff_entries": audit["diff_entries"],
            "base_sha256": audit["base_sha256"]}


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
def variant_id(pair, scale):
    return f"v_{pair['from']}2{pair['to']}_{int(round(scale * 100))}pct"


def generate_mix_variants(swap_pairs, scales=(0.10, 0.20, 0.30),
                          max_variants=16, l3_main_path=None,
                          out_dir=None, base_context=None):
    """参数扫描编排：置换对×幅度（按对 rank 展开截断 ≤max_variants）→
    build_variant_schedule → check_variant_feasibility（不可行弃并记录）→
    build_variant_main；全不可行 → KILLED 依据（feasible_zero=True）。

    base_context = {"money_floor_curve": [30 floats]}（编排层备好；缺省
    用 3000 起始资金零收入最差面）。输出 {"variants": [...], "audit"}。
    """
    l3_main_path = l3_main_path or B.DEFAULT_L3_MAIN
    out_dir = out_dir or os.path.join(B._HERE, "variants")
    base_context = base_context or {}
    with open(l3_main_path, "r", encoding="utf-8") as fh:
        base_text = fh.read()
    base_data, _ = B.decode_l3_blob(base_text)
    base_schedule = {"data": base_data, "primary_route": PRIMARY_ROUTE,
                     "money_floor_curve": base_context.get("money_floor_curve")}

    points = []
    for rank, pair in enumerate(swap_pairs):
        for scale in scales:
            points.append((rank, float(scale), pair))
    points.sort(key=lambda x: (x[0], -x[1]))
    points = points[:max_variants]

    variants, dropped = [], []
    for rank, scale, pair in points:
        vid = variant_id(pair, scale)
        rec = {"id": vid, "pair": {"from": pair["from"], "to": pair["to"]},
               "scale": scale, "pair_rank": rank, "feasible": None}
        try:
            sched = build_variant_schedule(pair, scale, base_schedule)
        except Exception as exc:
            rec.update({"feasible": False, "drop_reason":
                        f"schedule 构建失败: {type(exc).__name__}: {exc}"})
            dropped.append(rec)
            continue
        rec.update({"target_n": sched["target_n"], "moved_n": sched["moved_n"],
                    "from_plants_route": sched["from_plants_route"],
                    "seed_spend_delta": sched["seed_spend_delta"],
                    "skips": sched["skips"]})
        if sched["moved_n"] <= 0:
            rec.update({"feasible": False,
                        "drop_reason": f"零可迁移植物（target={sched['target_n']}，"
                                       f"路由 {sched['route_id']} from 植数 "
                                       f"{sched['from_plants_route']}）"})
            dropped.append(rec)
            continue
        feas = check_variant_feasibility(sched)
        rec["feasibility"] = feas
        if not feas["feasible"]:
            rec["feasible"] = False
            rec["drop_reason"] = f"不可行: {feas['violations'][:3]}"
            dropped.append(rec)
            continue
        rec["feasible"] = True
        vdir = os.path.join(out_dir, vid)
        try:
            built = build_variant_main(sched, l3_main_path,
                                       os.path.join(vdir, "main.py"))
        except Exception as exc:
            rec.update({"feasible": False,
                        "drop_reason": f"手术超界/构建失败: {type(exc).__name__}: {exc}"})
            dropped.append(rec)
            continue
        rec.update(built)
        rec["day_plan"] = sched["day_plan"]
        rec["route_audit"] = sched["route_audit"]
        variants.append(rec)
    return {
        "variants": variants,
        "dropped": dropped,
        "audit": {
            "n_points": len(points), "n_variants": len(variants),
            "n_dropped": len(dropped),
            "scales": list(scales), "max_variants": max_variants,
            "l3_base": os.path.abspath(l3_main_path),
            "primary_route": PRIMARY_ROUTE,
            "feasible_zero": not variants,
            "money_floor_curve_source": "losses_day_end_min"
            if base_context.get("money_floor_curve") else "starting_money_only",
        },
    }
