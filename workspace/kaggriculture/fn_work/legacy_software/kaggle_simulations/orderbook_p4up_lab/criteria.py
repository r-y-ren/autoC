# -*- coding: utf-8 -*-
"""criteria —— destbreso X-ray 六判据的工具级移植（纯 stdlib，数值口径不动）。

出处：fn_docs/hybrid/references/ext/closing-kernels/destbreso-xray/x-ray-your-agent.ipynb
（2026-10-02 实抓归档，provenance.md：无许可证声明，作者明示 fork 自用 cell 0）。
判据定义可引用；本文件代码=忠实移植改写（去 matplotlib/pandas，输出 JSON 化）。
x-ray 自校准数字一律在 CRITERIA_SPEC['calibration'] 标"自报"，不作我方读数。

六判据（编号=任务 P3 判决尺升级）：
  ① dual_classification   GLOBAL vs WITHIN-WORLD 判定差（cell 13/14）
  ② kinship_*             血缘谱镜像线 plan≥0.95 + BARCODE 分叉日（cell 16/17/19）
  ③ convergence           收敛三件套，阈值随判声明（cell 32/33）
  ④ speech_fingerprint    语言指纹 SCRIPT/BRANCHER/SCHEDULER 三分（cell 36/37）
  ⑤ crater_scan           crater 卖压判据（cell 24/25）
  ⑥ board_maps            热图半分相关 r≥0.9 反伪影闸（cell 26/27）

阈值随判纪律（cell 33）："a verdict quoted without its threshold is not a verdict"
——每条判据输出强制携带 threshold 字段。
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import statistics
from typing import Any, Dict, List, Optional, Sequence

from orderbook_p4up_lab.records import PASS_ACTION, canon

# ---------------------------------------------------------------- 判据元数据

CRITERIA_SPEC: Dict[str, Dict[str, Any]] = {
    "C1_GLOBAL_WITHIN_WORLD": {
        "name": "GLOBAL vs WITHIN-WORLD 判定差",
        "definition": (
            "同一批局的逐拍动作流读两遍：GLOBAL=全体互比；WITHIN-WORLD=按世界"
            "（前两店有序对）分组、只在组内互比。店路由器在 t=72/144 随店抽分叉，"
            "全局看像狂适应、世界内近乎全同；真 live policy 世界内也分叉。"
            "两次读数之差即诊断。"
        ),
        "inputs": "各局 stream（逐拍 action dict，canon 指纹）+ world 分组键",
        "outputs": (
            "global{cls,frac,first,chan}；within_world[]{world,n,cls,frac,first}；"
            "verdict_counts；gap_diagnosis；router_hint"
        ),
        "thresholds": (
            "classify 截断：varying==0→PURE_REPLAY；plan(farmer+hands)变动为0 且 "
            "frac<0.25→REPAIRING_SCRIPT；frac<0.10→REPAIRING_SCRIPT；否则 ADAPTIVE"
            "（x-ray cell 14 代码常量，自报）；router 窗提示 first∈[70,146] 贴 t=72/144 "
            "店抽（cell 14，自报）"
        ),
        "calibration": (
            "自报（cell 13-15）：shop router 全局狂适应/世界内全同；种子与反应不可全分离，"
            "分世界组=先剥掉最大的 seed 效应（店抽）"
        ),
        "limits": "t<48 为可观测盲区（引擎确定性，一切 agent 同拍同令）；world 键缺失时 WITHIN-WORLD 不可读",
    },
    "C2_KINSHIP_MIRROR": {
        "name": "血缘谱镜像线 + BARCODE 分叉日",
        "definition": (
            "一局回放同时留下对战双方动作流：PLAN 一致度（farmer+hands 相同拍占比）认家族；"
            "WHOLE 一致度（+market）1.000=同录；BARCODE=每日 d1-4 重锚窗计划+结构市单签名"
            "×30 天，首个不一致日=分叉日。镜像线 plan≥0.95；sibling 0.5-0.95；"
            "基因群=开局窗（t<144）plan 一致 ≥0.98 连通分量。"
        ),
        "inputs": "mine/opp 逐拍动作流 + margin + episode 标识（opp_sub 可选）",
        "outputs": (
            "kin_rows[]{plan,whole,bands,fork_day,res,margin}；n_mirror/n_sibling/n_unrelated；"
            "mirror_record/mirror_margins；genetic_groups[]{group,games,record,margin_med,...}"
        ),
        "thresholds": (
            "mirror=plan≥0.95；sibling=0.5≤plan<0.95（cell 17，自报）；基因群阈值 0.98、"
            "开局窗 PRE=144（cell 19，自报）；BARCODE 窗=每日 h=1..4、30 天（cell 17）"
        ),
        "calibration": "自报（cell 16）：t48 前无可观测差异，早期一致=引擎确定性不是亲缘；a group you only tie is your own chassis",
        "limits": (
            "BARCODE 仅认 STRUCT(HIRE/BUY_LAND/BUY_ANIMAL)+PROV(BUY_SEED/BUY_PRODUCT) 市单"
            "（cell 17 口径）；镜像局两座位非独立，战绩读数应带 design effect 1+φ 置信修正"
            "（georgymarin cell 32 口径，mining §2.4）"
        ),
    },
    "C3_CONVERGENCE": {
        "name": "收敛三件套（DRIFT/SIGN FLIPS/n）",
        "definition": (
            "评分是否已停：DRIFT=近 WIN 局评分变化均值（单位=pts/episode，绝不用墙钟）；"
            "SIGN FLIPS=非零逐局 delta 变号次数；n=已评局数。"
            "WARMING UP=漂移超阈且无变号；SETTLED=漂移≤阈且至少一次变号；否则 SETTLING。"
            "配对速率故意不进判决（匹配器调度所致），只换算'多久后再读数'。"
        ),
        "inputs": "按时间序的逐局评分轨迹 traj（updatedScore 序列）；可选 endTime 序列（配对速率）",
        "outputs": "verdict；drift；flips；n；threshold；window；rating_now；pairing_rate*/reread_eta_h*",
        "thresholds": (
            "THRESH=1.0 pts/episode（x-ray cell 33 写死，随判声明，自报）；"
            "WIN=min(20, n-1)；n<4 不判（'the rating is a rumour'）"
        ),
        "calibration": "自报（cell 32）：批量更新语义下按分钟平均会误读，按 episode 平均才对；配对速率衰减=匹配器认为你已就位",
        "limits": "阈值是决策不是常数，复用时可换但必须随判声明；无轨迹数据时不判",
    },
    "C4_LANGUAGE_FINGERPRINT": {
        "name": "语言指纹 SCRIPT/BRANCHER/SCHEDULER 三分",
        "definition": (
            "把拍当话语：5 连非空拍=短语（丢移动/PASS/数量，PLANT/PICKUP/PLACE 保品类参数，"
            "市单 HIRE/BUY_LAND 光杆、其余 verb:good）；按日带 6-11/12-19/20-29 统计"
            "每局短语在其余局复现（≥半数局出现）占比的中位=repeat_rate，附归一化熵。"
            "冻script 全带≈1.0；逐局即兴≈0.0；brancher 前段持干后段融掉。"
        ),
        "inputs": "≥8 局全流（覆盖 t≥144 拍；不足 8 局不读）",
        "outputs": "bands{(6-11),(12-19),(20-29)}{repeat_rate,norm_entropy,distinct}；class",
        "thresholds": (
            "类目截断：r0≥0.95 且 r1≥0.7→SCRIPT；r0≥0.5 且 r1<0.5→BRANCHER；"
            "r0<0.5→SCHEDULER；其余 MIXED；任一带 None→INSUFFICIENT-SIGNAL（cell 37，自报）；"
            "局数地板 8（cell 37）"
        ),
        "calibration": (
            "自报 2026-09-04（cell 36）：磁带族 1.00/0.91-1.00/0.74-0.91；カワシギ 0.89/0.15/0.00；"
            "keiz 0.75/0/0；tetsuya & yuanzhe zhou 0.02/0/0；Crop Dusta 0/0/0；"
            "盲测对手工逆向过的 8 局恢复全部 7 个已知分叉点（精确率全对，零漏零误）"
        ),
        "limits": "语言类目不是强度（'language only, not strength'）；短语窗跨非空拍连续，空拍不打断语义但占位不计",
    },
    "C5_CRATER": {
        "name": "crater 卖压判据",
        "definition": (
            "市场共享，卖单即武器：一方大卖砸价后 window 拍内另一方同品卖出=crater。"
            "红=对手卖进我砸的坑、蓝=我卖进对手的坑。一阶伤害=victim 数量×吃掉的价差，"
            "读作坑的大小而非因果转移。"
        ),
        "inputs": "对战双方逐拍动作流 + 逐拍价格表 prices_t（每品价格）",
        "outputs": "our_craters[]{t0,t1,prod,dmg}；their_craters[]{...}；totals{dmg,n}",
        "thresholds": (
            "window=24 拍；卖方按单笔价值 qty×px 取 top=60（cell 25 代码常量，自报）；"
            "dmg≤0 或无后继卖单的不计"
        ),
        "calibration": "自报（cell 24）：读作 size of the hole，不作因果转移；配对图取样本内最大 |margin| 一局",
        "limits": "需逐拍价格序列；无价格数据不判；一阶口径忽略回补/跨品替代",
    },
    "C6_BOARD_HALFSPLIT": {
        "name": "热图半分相关 r≥0.9 反伪影闸",
        "definition": (
            "棋盘是 10x10 而非袋子：occupancy=逐拍有物格计数、presence=farmer+hands 位置计数。"
            "热图永远显得有结构，故双控制：卡方 vs 均匀 + top10 格质量占比；"
            "半分相关=局交替分两堆比图，r≥+0.9 才信，低于约 +0.9 当一季噪声。"
        ),
        "inputs": "各局 10x10 occ/pres/unlocked 网格（逐拍累计）",
        "outputs": "per_kind{corr_half,gate,chi2_dof,top10_share,flat_share,n_cells,n_episodes}",
        "thresholds": "gate=r≥+0.9（cell 26/27 自述，自报）；卡方按 unlocked 格自由度 n_cells-1",
        "calibration": "自报（cell 2 注）：稠密棋盘层 n=16 半分 r 0.99 即稳",
        "limits": "半分按局交替（不是随机）；局数不足时 den=0 → corr 不可算，闸=NOT_COMPUTABLE",
    },
}

# ---------------------------------------------------------------- ① 双重分类

CHANNELS = ("farmer", "hands", "market")


def compare_streams(streams: Sequence[Sequence[Optional[dict]]]) -> Dict[str, Any]:
    """x-ray cell 14：多流逐拍比，返回变动拍数/首分叉拍/分通道变动。"""
    if not streams:
        return {"turns": 0, "varying": 0, "frac": 0.0, "first": None,
                "chan": {c: 0 for c in CHANNELS}}
    n = min(len(s) for s in streams)
    chan = {c: 0 for c in CHANNELS}
    first = None
    varying = 0
    for t in range(n):
        acts = [canon(s[t]) for s in streams]
        if len(set(acts)) > 1:
            varying += 1
            if first is None:
                first = t
            for i, c in enumerate(CHANNELS):
                if len({a[i] for a in acts}) > 1:
                    chan[c] += 1
    return {"turns": n, "varying": varying, "frac": varying / max(1, n),
            "first": first, "chan": chan}


def classify(cmp_out: Dict[str, Any]) -> str:
    """x-ray cell 14 classify()：PURE_REPLAY/REPAIRING_SCRIPT/ADAPTIVE。"""
    plan_moves = cmp_out["chan"]["farmer"] + cmp_out["chan"]["hands"]
    if cmp_out["varying"] == 0:
        return "PURE_REPLAY"
    if plan_moves == 0 and cmp_out["frac"] < 0.25:
        return "REPAIRING_SCRIPT"
    if cmp_out["frac"] < 0.10:
        return "REPAIRING_SCRIPT"
    return "ADAPTIVE"


def dual_classification(records) -> Dict[str, Any]:
    """判据①：GLOBAL 全体互比 + WITHIN-WORLD 组内互比，差=诊断。"""
    streams = [r.stream for r in records]
    g = compare_streams(streams)
    gcls = classify(g)

    by_world: Dict[str, List] = collections.defaultdict(list)
    for r in records:
        by_world[r.world if r.world else "UNSPECIFIED"].append(r.stream)

    rows = []
    for w in sorted(by_world):
        ss = by_world[w]
        if len(ss) < 2:
            rows.append({"world": w, "n": len(ss), "cls": "(one episode)",
                         "frac": None, "first": None})
            continue
        cw = compare_streams(ss)
        rows.append({"world": w, "n": len(ss), "cls": classify(cw),
                     "frac": round(cw["frac"], 4), "first": cw["first"]})

    multi = [r_ for r_ in rows if r_["n"] >= 2]
    verdict_counts = dict(collections.Counter(r_["cls"] for r_ in multi))

    within_adaptive = any(r_["cls"] == "ADAPTIVE" for r_ in multi)
    global_adaptive = gcls == "ADAPTIVE"
    if within_adaptive:
        gap = ("WITHIN_WORLD_ADAPTIVE: 世界内也分叉=真 live policy（或对手把其逼离脚本）；"
               "取高变动世界进决策树提取追因")
    elif global_adaptive and multi:
        gap = ("SHOP_ROUTER_SIGNATURE: 全局像适应、世界内近乎全同=路由分叉（随店抽），"
               "非反应式；其可预测底稿=各世界的多数流")
    elif global_adaptive and not multi:
        gap = "GLOBAL_ADAPTIVE_BUT_NO_WORLD_REPEAT: 无同世界重复局，世界内读数不可得"
    else:
        gap = f"GLOBAL_{gcls}: 两读数一致，按 {gcls} 处置"

    router_hint = None
    if global_adaptive and g["first"] is not None and 70 <= g["first"] <= 146:
        router_hint = (f"首个分叉 t={g['first']} 落 [70,146]，贴 t=72/144 店抽=ROUTING "
                       f"痕迹（x-ray cell 14 提示，自报）")

    return {
        "criteria": "C1_GLOBAL_WITHIN_WORLD",
        "global": {"cls": gcls, "varying_frac": round(g["frac"], 4),
                   "first_divergence": g["first"], "channels": g["chan"],
                   "turns": g["turns"], "n_streams": len(streams)},
        "within_world": rows,
        "verdict_counts": verdict_counts,
        "gap_diagnosis": gap,
        "router_hint": router_hint,
        "threshold": {"classify_frac_repair": 0.25, "classify_frac_low": 0.10,
                      "router_window": [70, 146],
                      "source": "x-ray cell 14 代码常量（自报）"},
    }


# ---------------------------------------------------------------- ② 血缘谱

STRUCT = {"HIRE", "BUY_LAND", "BUY_ANIMAL"}
PROV = {"BUY_SEED", "BUY_PRODUCT"}
MIRROR_LINE = 0.95
SIBLING_FLOOR = 0.50
GENETIC_PRE = 144
GENETIC_THRESH = 0.98


def barcode_band(stream, day: int, pass_sentinel=None) -> str:
    """x-ray cell 17 band()：day 的 h=1..4 重锚窗签名（计划+结构/补给市单）。"""
    ps = pass_sentinel or PASS_ACTION
    sig = []
    for h in range(1, 5):
        t = day * 24 + h
        a = stream[t] if t < len(stream) else ps
        m = [[o[0], o[1] if len(o) > 1 else None]
             for o in (a.get("market") or []) if o and o[0] in STRUCT | PROV]
        sig.append([a.get("farmer"), a.get("hands"), m])
    return hashlib.md5(json.dumps(sig, sort_keys=True).encode()).hexdigest()


def barcode(stream) -> List[str]:
    return [barcode_band(stream, d) for d in range(30)]


def plan_whole_agreement(mine, opp) -> Dict[str, float]:
    """PLAN（farmer+hands）与 WHOLE（+market）一致度。"""
    n = min(len(mine), len(opp))
    if n == 0:
        return {"plan": 0.0, "whole": 0.0, "turns": 0}
    mc = [canon(a) for a in mine[:n]]
    oc = [canon(a) for a in opp[:n]]
    plan = sum(1 for a, b in zip(mc, oc) if a[:2] == b[:2]) / n
    whole = sum(1 for a, b in zip(mc, oc) if a == b) / n
    return {"plan": round(plan, 3), "whole": round(whole, 3), "turns": n}


def kinship_row(record) -> Dict[str, Any]:
    """x-ray cell 17 kin 一行。"""
    ag = plan_whole_agreement(record.stream, record.opp_stream)
    mb, ob = barcode(record.stream), barcode(record.opp_stream)
    shared = sum(1 for x, y in zip(mb, ob) if x == y)
    fork = next((d for d, (x, y) in enumerate(zip(mb, ob)) if x != y), None)
    res = "W" if record.margin > 0 else ("L" if record.margin < 0 else "T")
    plan = ag["plan"]
    return {"episode": record.episode, "opp": record.opp, "opp_sub": record.opp_sub,
            "res": res, "margin": record.margin, "plan": plan,
            "whole": ag["whole"], "bands": f"{shared}/30", "fork_day": fork}


def kinship_spectrum(records) -> Dict[str, Any]:
    """判据②：镜像线/sibling/无关三分 + 镜像战绩 + BARCODE 分叉日。"""
    kin = [kinship_row(r) for r in records]
    kin.sort(key=lambda k: -k["plan"])
    mirrors = [k for k in kin if k["plan"] >= MIRROR_LINE]
    siblings = [k for k in kin if SIBLING_FLOOR <= k["plan"] < MIRROR_LINE]
    unrelated = len(kin) - len(mirrors) - len(siblings)
    mm = [k["margin"] for k in mirrors]
    mirror_record = (f"{sum(1 for x in mm if x > 0)}W-"
                     f"{sum(1 for x in mm if x < 0)}L-{sum(1 for x in mm if x == 0)}T"
                     if mirrors else None)
    return {
        "criteria": "C2_KINSHIP_MIRROR",
        "kin_rows": kin,
        "n_mirror": len(mirrors), "n_sibling": len(siblings),
        "n_unrelated": unrelated,
        "mirror_record": mirror_record,
        "mirror_margins_sorted": sorted(mm),
        "threshold": {"mirror_line": MIRROR_LINE,
                      "sibling_band": [SIBLING_FLOOR, MIRROR_LINE],
                      "source": "x-ray cell 17（自报）"},
    }


def genetic_groups(streams, labels=None, sub_ids=None, margins=None) -> Dict[str, Any]:
    """x-ray cell 19：开局窗 plan 一致 ≥0.98 连通分量=基因群。"""
    streams = list(streams)
    n_ep = len(streams)
    labels = list(labels or ["?"] * n_ep)
    sub_ids = list(sub_ids or [None] * n_ep)
    margins = list(margins if margins is not None else [0.0] * n_ep)
    pre = min(GENETIC_PRE, min((len(s) for s in streams), default=0))
    pre_c = [[canon(a)[:2] for a in s[:pre]] for s in streams]

    def pre_agree(i, j):
        if pre == 0:
            return 0.0
        return sum(1 for a, b in zip(pre_c[i], pre_c[j]) if a == b) / pre

    parent = list(range(n_ep))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n_ep):
        for j in range(i + 1, n_ep):
            if pre_agree(i, j) >= GENETIC_THRESH:
                parent[find(i)] = find(j)

    groups: Dict[int, List[int]] = collections.defaultdict(list)
    for i in range(n_ep):
        groups[find(i)].append(i)

    gtab = []
    for _, idxs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        ms = sorted(margins[i] for i in idxs)
        subs = {sub_ids[i] for i in idxs}
        names = [labels[i] for i in idxs]
        wg = sum(1 for m in ms if m > 0)
        lg = sum(1 for m in ms if m < 0)
        gtab.append({
            "group": f"G{len(gtab) + 1}", "games": len(idxs),
            "submissions": len(subs),
            "lead": collections.Counter(names).most_common(1)[0][0],
            "record": f"W{wg}-L{lg}-T{len(ms) - wg - lg}",
            "margin_med": ms[len(ms) // 2], "worst": ms[0], "best": ms[-1]})
    return {
        "criteria": "C2_KINSHIP_MIRROR",
        "genetic_groups": gtab,
        "n_groups": len(gtab),
        "window_turns": pre,
        "threshold": {"genetic_plan": GENETIC_THRESH, "pre_window": GENETIC_PRE,
                      "source": "x-ray cell 19（自报）"},
    }


# ---------------------------------------------------------------- ③ 收敛三件套

DEFAULT_CONVERGENCE_THRESH = 1.0  # pts/episode；x-ray cell 33；随判声明


def convergence(traj, threshold: float = DEFAULT_CONVERGENCE_THRESH,
                timestamps=None) -> Dict[str, Any]:
    """判据③：DRIFT+SIGN FLIPS+n 三件套；阈值随判声明；配对速率不进判决。"""
    traj = list(traj)
    out: Dict[str, Any] = {
        "criteria": "C3_CONVERGENCE",
        "threshold": threshold,
        "threshold_source": "x-ray cell 33（自报；'a verdict quoted without its threshold is not a verdict'）",
        "n": len(traj),
    }
    if len(traj) < 4:
        out.update({"verdict": "TOO_FEW", "drift": None, "flips": None,
                    "window": None,
                    "note": f"only {len(traj)} rated episodes: too few to classify, "
                            "the rating is a rumour"})
        return out
    win = min(20, len(traj) - 1)
    deltas = [b - a for a, b in zip(traj[-win - 1:-1], traj[-win:])]
    drift = sum(deltas) / len(deltas)
    nz = [d for d in deltas if d != 0]
    flips = sum(1 for a, b in zip(nz, nz[1:]) if (a > 0) != (b > 0))
    if abs(drift) > threshold and flips == 0:
        verdict = "WARMING UP"
    elif abs(drift) > threshold:
        verdict = "SETTLING"
    else:
        verdict = "SETTLED" if flips >= 1 else "SETTLING"
    out.update({"verdict": verdict, "drift": round(drift, 3), "flips": flips,
                "window": win, "rating_now": traj[-1]})
    if timestamps:
        ts = sorted(timestamps)
        if len(ts) >= 3:
            span_h = max(1.0, (ts[-1] - ts[0]).total_seconds() / 3600)
            last24 = sum(1 for t in ts
                         if (ts[-1] - t).total_seconds() <= 24 * 3600) / min(24.0, span_h)
            out["pairing_rate_lifetime_per_h"] = round(len(ts) / span_h, 2)
            out["pairing_rate_last24_per_h"] = round(last24, 2)
            if last24 > 0:
                out["reread_eta_h"] = round(win / last24, 1)
            out["pairing_note"] = ("配对速率不进判决（匹配器调度所致）；reread_eta=drift 窗长/当前"
                                   "速率=何时再读数（cell 32）")
    return out


# ---------------------------------------------------------------- ④ 语言指纹

LANG_DROP = {"PASS", "NORTH", "SOUTH", "EAST", "WEST"}
LANG_ARG = {"PLANT", "PICKUP", "PLACE"}
LANG_BANDS = [(6, 11), (12, 19), (20, 29)]
LANG_FLOOR_N = 8


def _lang_tok(a: Optional[dict]) -> Optional[str]:
    act = a or {}
    toks = []
    for u in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
        if not u or u[0] in LANG_DROP:
            continue
        toks.append(f"{u[0]}:{u[1]}" if u[0] in LANG_ARG and len(u) > 1 else u[0])
    for o in act.get("market") or []:
        if not o:
            continue
        if o[0] in ("HIRE", "BUY_LAND"):
            toks.append(o[0])
        elif len(o) > 1:
            toks.append(f"{o[0]}:{o[1]}")
    return "+".join(sorted(toks)) if toks else None


def _lang_grams(acts, n: int = 5) -> Dict[Any, set]:
    seq = [(t // 24, tok) for t, a in enumerate(acts)
           if (tok := _lang_tok(a)) and t // 24 >= 6]
    out = {b: set() for b in LANG_BANDS}
    for i in range(len(seq) - n + 1):
        day = seq[i][0]
        for lo, hi in LANG_BANDS:
            if lo <= day <= hi:
                out[(lo, hi)].add(tuple(t for _, t in seq[i:i + n]))
                break
    return out


def speech_fingerprint(episodes, n: int = 5) -> Dict[Any, Dict[str, Any]]:
    per = [_lang_grams(a, n) for a in episodes]
    rows_out: Dict[Any, Dict[str, Any]] = {}
    for b in LANG_BANDS:
        counts: collections.Counter = collections.Counter()
        for g in per:
            for gram in g[b]:
                counts[gram] += 1
        half = max(2, len(episodes) // 2)
        common = {g for g, c in counts.items() if c >= half}
        rates = [len(g[b] & common) / len(g[b]) for g in per if g[b]]
        total = sum(counts.values())
        hn = 0.0
        if total and len(counts) > 1:
            h = -sum((c / total) * math.log(c / total) for c in counts.values())
            hn = h / math.log(len(counts))
        rows_out[b] = {
            "repeat_rate": round(statistics.median(rates), 3) if rates else None,
            "norm_entropy": round(hn, 3), "distinct": len(counts)}
    return rows_out


def speech_class(fp: Dict[Any, Dict[str, Any]]) -> str:
    r = [fp[b]["repeat_rate"] for b in LANG_BANDS]
    if any(x is None for x in r):
        return "INSUFFICIENT-SIGNAL"
    if r[0] >= 0.95 and r[1] >= 0.7:
        return "SCRIPT (a frozen plan; observation changes at most repairs)"
    if r[0] >= 0.5 and r[1] < 0.5:
        return "BRANCHER (commits to a trunk, forks on what it observes)"
    if r[0] < 0.5:
        return "SCHEDULER (composes its plan per game)"
    return "MIXED (a script with adaptive patches, or a composer with rituals)"


def language_fingerprint(records) -> Dict[str, Any]:
    """判据④：跨局语言指纹三分。地板 8 局（cell 37）。"""
    streams = [r.stream for r in records]
    out: Dict[str, Any] = {
        "criteria": "C4_LANGUAGE_FINGERPRINT",
        "n_episodes": len(streams),
        "threshold": {"class_cutoffs": {"SCRIPT": "r0>=0.95 & r1>=0.7",
                                        "BRANCHER": "r0>=0.5 & r1<0.5",
                                        "SCHEDULER": "r0<0.5"},
                      "floor_n": LANG_FLOOR_N,
                      "bands": [list(b) for b in LANG_BANDS],
                      "source": "x-ray cell 37（自报）"},
        "calibration_self_reported": (
            "自报 2026-09-04（cell 36）：tapes 1.00/0.91-1.00/0.74-0.91；カワシギ 0.89/0.15/0.00；"
            "keiz 0.75/0/0；tetsuya & yuanzhe zhou 0.02/0/0；Crop Dusta 0/0/0"),
    }
    if len(streams) < LANG_FLOOR_N:
        out.update({"class": "INSUFFICIENT-SIGNAL", "bands": None,
                    "note": f"{len(streams)} episodes: below the 8-episode floor for "
                            "cross-game statistics"})
        return out
    fp = speech_fingerprint(streams)
    out["bands"] = {f"d{b[0]:02d}-{b[1]:02d}": fp[b] for b in LANG_BANDS}
    out["class"] = speech_class(fp)
    return out


# ---------------------------------------------------------------- ⑤ crater

def money_events(stream, prices_t) -> List[Dict[str, Any]]:
    """x-ray cell 25 _mf_events：逐拍市单展开为带价事件。"""
    out = []
    for t, act in enumerate(stream):
        if not isinstance(act, dict):
            continue
        for m in (act.get("market") or []):
            if not (isinstance(m, list) and len(m) >= 2):
                continue
            qty = int(m[2]) if len(m) >= 3 and str(m[2]).lstrip("-").isdigit() else 1
            px = (prices_t[t] or {}).get(m[1], 0) if t < len(prices_t) else 0
            out.append({"t": t, "verb": m[0], "prod": m[1], "qty": qty,
                        "px": px, "value": qty * px})
    return out


def find_craters(sellers, victims, prices_t, window: int = 24,
                 top: int = 60) -> List[Dict[str, Any]]:
    """x-ray cell 25 _mf_craters：大卖后 window 拍内对侧同品卖出=crater。"""
    out = []
    for e in sorted((x for x in sellers if x["verb"] == "SELL"),
                    key=lambda x: -x["value"])[:top]:
        p0 = (prices_t[e["t"]] or {}).get(e["prod"], 0) if e["t"] < len(prices_t) else 0
        later = [o for o in victims if o["verb"] == "SELL" and o["prod"] == e["prod"]
                 and e["t"] < o["t"] <= e["t"] + window]
        if not later:
            continue
        dmg = sum(o["qty"] * max(0, p0 - o["px"]) for o in later)
        if dmg <= 0:
            continue
        out.append({"t0": e["t"], "t1": max(o["t"] for o in later),
                    "prod": e["prod"], "dmg": dmg})
    out.sort(key=lambda c: -c["dmg"])
    return out


def crater_scan(record, window: int = 24, top: int = 60) -> Dict[str, Any]:
    """判据⑤：我砸的坑对手卖进（红）/ 对手砸的坑我卖进（蓝）。"""
    out: Dict[str, Any] = {
        "criteria": "C5_CRATER",
        "episode": record.episode,
        "threshold": {"window_turns": window, "top_sellers": top,
                      "source": "x-ray cell 25（自报）"},
    }
    if not record.prices_t:
        out.update({"status": "INSUFFICIENT_DATA",
                    "note": "无逐拍价格序列 prices_t，crater 不可判"})
        return out
    me = money_events(record.stream, record.prices_t)
    op_ = money_events(record.opp_stream, record.prices_t)
    ours = find_craters(me, op_, record.prices_t, window, top)[:6]
    theirs = find_craters(op_, me, record.prices_t, window, top)[:6]
    out.update({
        "status": "OK",
        "our_craters": ours,
        "their_craters": theirs,
        "totals": {"our_dmg": sum(c["dmg"] for c in ours),
                   "their_dmg": sum(c["dmg"] for c in theirs),
                   "n_our": len(ours), "n_their": len(theirs)},
        "reading": "一阶伤害=victim 数量×吃掉的价差；读作 size of the hole，非因果转移（cell 24）",
    })
    return out


# ---------------------------------------------------------------- ⑥ 热图半分闸

HALFSPLIT_GATE = 0.9


def _corr(a: List[List[int]], b: List[List[int]]) -> Optional[float]:
    xa = [v for row in a for v in row]
    xb = [v for row in b for v in row]
    ma = sum(xa) / len(xa)
    mb = sum(xb) / len(xb)
    num = sum((p - ma) * (q - mb) for p, q in zip(xa, xb))
    den = (sum((p - ma) ** 2 for p in xa) * sum((q - mb) ** 2 for q in xb)) ** 0.5
    return None if den == 0 else num / den


def _uniformity(grid, unlocked) -> Optional[Dict[str, Any]]:
    vals = [grid[y][x] for y in range(10) for x in range(10) if unlocked[y][x] > 0]
    tot = sum(vals)
    if not vals or tot == 0:
        return None
    exp = tot / len(vals)
    chi = sum((v - exp) ** 2 / exp for v in vals)
    top = sum(sorted(vals, reverse=True)[:10])
    return {"n_cells": len(vals), "chi2_dof": round(chi / max(1, len(vals) - 1), 2),
            "top10_share": round(top / tot, 4),
            "flat_share": round(min(10, len(vals)) / len(vals), 4)}


def _acc(grid, add):
    for y in range(10):
        for x in range(10):
            grid[y][x] += add[y][x]


def board_maps(records) -> Dict[str, Any]:
    """判据⑥：occupancy/presence 热图 + 半分相关闸 + 均匀性双控制。"""
    halves = {"occ": [[[0] * 10 for _ in range(10)] for _ in range(2)],
              "pres": [[[0] * 10 for _ in range(10)] for _ in range(2)]}
    unlocked = [[0] * 10 for _ in range(10)]
    used = 0
    for k, r in enumerate(records):
        if r.occ is None or r.pres is None:
            continue
        used += 1
        h = k % 2
        _acc(halves["occ"][h], r.occ)
        _acc(halves["pres"][h], r.pres)
        if r.unlocked is not None:
            _acc(unlocked, r.unlocked)

    out: Dict[str, Any] = {
        "criteria": "C6_BOARD_HALFSPLIT",
        "n_episodes": used,
        "threshold": {"gate_r": HALFSPLIT_GATE,
                      "source": "x-ray cell 26/27（自报）：'below about +0.9, read the map "
                                "as one season's noise'"},
    }
    if used == 0:
        out["status"] = "INSUFFICIENT_DATA"
        out["note"] = "无棋盘网格（occ/pres）数据，热图闸不可判"
        return out

    kinds = {}
    for kind in ("occ", "pres"):
        grid = [[halves[kind][0][y][x] + halves[kind][1][y][x]
                 for x in range(10)] for y in range(10)]
        r = _corr(halves[kind][0], halves[kind][1])
        uni = _uniformity(grid, unlocked)
        gate = ("NOT_COMPUTABLE" if r is None else
                ("TRUST" if r >= HALFSPLIT_GATE else "NOISE"))
        kinds[{"occ": "occupancy", "pres": "presence"}[kind]] = {
            "corr_half": (round(r, 4) if r is not None else None),
            "gate": gate,
            "chi2_dof": uni["chi2_dof"] if uni else None,
            "top10_share": uni["top10_share"] if uni else None,
            "flat_share": uni["flat_share"] if uni else None,
            "n_cells": uni["n_cells"] if uni else 0,
        }
    out["status"] = "OK"
    out["maps"] = kinds
    return out
