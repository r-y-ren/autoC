# -*- coding: utf-8 -*-
"""ablation_r40（B32 修订）：四组件消融诊断——定位 r40 回退源。

责任契约（用户裁决「消融诊断再战」）：四组件=①_route40_select 路由切换
②retape_sell_lots 卖单批量化 ③apply_race_slots 抢价 ④apply_slot_hygiene
清坑；构单件探针 V1-V4+全件对照 V5（+V0=r37 基线）各跑三面（h2h vs r37 /
强臂胜率 / d21-28 段差），出组件×三面效应表→按决策规则留强砍弱（修=机制层
最小修正+单件复测）→重组修复版 r40→judge_r23 六判据全量重判（判据本身零改动）。

【探针口径】探针=判决级（不必过 build 审计/门禁）：
- V0=r37 底版原样（效应基线）；V5=现 r40 全件（①②③④，对照）。
- V1/V3/V4=底版尾部追加探针块：运行时件源码自 runtime_r40.py ast 整段抽取
  （单一真源零手抄，inject_r40 同法）+按需组合包装 _r40p_agent（父层捕获沿
  _R40_PARENT 机制；①按需内嵌续段库字面量）。
- V2=磁带手术（retape_sell_lots 解码 r37 处理后 _encode_routes 编码出变体
  main），无尾块。
- 探针块只含所选件：V1 只走续段选择（只读，_last_select 存证）；V3 只走
  竞速；V4 只走清坑；包装链 fail-safe 语义与 _route40_agent 同款。

【三面口径】（与 judge_r23 判据读数同源同法，探针面自成独立 seed 域）
- h2h：变体 vs r37，n_h2h 独立 seed×双席，_arm_rate seed 口径（胜=两席皆胜）。
- 强臂：变体 vs 榜前 550 强样本（judges 强臂口径=opponents[1:]=2965_adopt/a、
  2965_adopt/b、v48_derivative 三件池化），n_strong seed×双席，_arm_rate。
- 段差：败局 12 局定向重演（build_r40.LOSS_IDS，候选 vs 原局录像双席）逐局
  对同席原局基线自比，d21-28 段资金差中位（judge_r23.segment_stats 同口径）。

【效应表+决策规则留档】组件×三面（h2h_rate/strong_rate/seg_delta_median）
+相对 V0 差分；判定（预绑定，留强砍弱）：
- 保留：h2h ≥ 0.55 或 强臂显著升（strong_rate−V0 ≥ +0.05）；
- 毒药：h2h ≤ 0.45 → 砍或修（修=找机制层因做最小修正，修后单件复测）；
- 中间：保留标注。
- 路由①优先保（用户裁决：强臂正效应已知真金）——①若毒只修切换逻辑
  （保守阈值/无族不切）不许全砍。
不许为凑绿改统计口径；效应表/决策规则/evidence 全落 evidence/ablation_
r40_realrun.json。

【签名】build_probe(variant, out_dir)→探针 main 路径；probe_plans(...)→
三面局表；run_ablation(out_dir=None, workers=16, n_h2h=60, n_strong=30)→
evidence dict（含 effect_table/disposition）；decide_effects(table)→处置表。
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import (Any, Dict, List, Mapping, Optional, Sequence,  # noqa: F401
                    Tuple)

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

from orderbook_r40 import judge_r23 as _j23            # noqa: E402
from orderbook_r40 import build_r40 as _b40            # noqa: E402

R37_MAIN = str(KSIM_DIR / "orderbook_r37" / "build" / "main.py")
FULL_R40_MAIN = str(MODULE_DIR / "build" / "main.py")
RUNTIME_SRC = MODULE_DIR / "runtime_r40.py"

RECORD_VERSION = "r40-ablation/1.0"

#: 四组件名（①②③④）与运行时件源函数名映射（②=磁带手术非运行时件）。
COMPONENTS: Tuple[str, ...] = ("route_select", "sell_lots", "race_slots",
                               "slot_hygiene")
RUNTIME_FUNCS: Dict[str, str] = {
    "route_select": "_route40_select",
    "race_slots": "apply_race_slots",
    "slot_hygiene": "apply_slot_hygiene",
}

#: 探针变体→组件集（V5=全件对照；V0=r37 基线无组件）。
VARIANTS: Dict[str, Tuple[str, ...]] = {
    "V1": ("route_select",),
    "V2": ("sell_lots",),
    "V3": ("race_slots",),
    "V4": ("slot_hygiene",),
    "V5": COMPONENTS,
}

#: 修后单件复测变体（B32 机制修正）：V2f=卖单手术 cross_step=False（只同拍
#: 并单，零时序移动）；V4f=清坑 qty==0 修正（runtime_r40 单一真源已修）。
FIXED_VARIANTS: Dict[str, Tuple[str, ...]] = {
    "V2f": ("sell_lots",),
    "V4f": ("slot_hygiene",),
}
CROSS_STEP_OFF = ("V2f",)        # 只同拍并单的磁带手术变体

#: 三面局量口径（独立 seed；每 seed 双席两局）。
N_H2H_DEFAULT = 60          # h2h vs r37 ≥60 独立 seed
N_STRONG_DEFAULT = 30       # 强臂 ≥30 独立 seed（10 seed × 3 强样本）
H2H_SEED_BASE = 510000      # 与 judge_r23 h2h seed 域同起点（可比性）
STRONG_SEED_BASE = 520000   # 与 judge_r23 强臂 seed 域同起点
STRONG_OPPONENTS: Tuple[str, ...] = (
    "orderbook_2965_adopt/a/main.py",
    "orderbook_2965_adopt/b/main.py",
    "v48_derivative/main.py",
)

#: 决策规则常量（预绑定；留强砍弱）。
T_KEEP_H2H = 0.55           # h2h ≥0.55 → 保留
T_POISON_H2H = 0.45         # h2h ≤0.45 → 毒药（砍或修）
T_STRONG_SIGNIFICANT = 0.05  # 强臂差分 ≥+0.05 → 显著升（保留）

_PREAMBLE = "# ==== r40 消融探针（自动生成，勿手改） %s ====\n"


# --------------------------------------------------------------- 探针构建 --

def _runtime_sources(names: Sequence[str]) -> Dict[str, str]:
    """runtime_r40.py 指定函数源 ast 整段抽取（inject_r40 同法，零手抄）。"""
    src = RUNTIME_SRC.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(RUNTIME_SRC))
    segs: Dict[str, str] = {}
    want = {RUNTIME_FUNCS[n] for n in names}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            seg = ast.get_source_segment(src, node)
            if not seg:
                raise RuntimeError("探针源抽取失败: %s" % node.name)
            segs[node.name] = seg
    missing = sorted(want - set(segs))
    if missing:
        raise RuntimeError("runtime_r40.py 缺函数定义: %s" % missing)
    return segs


def _library_literal() -> str:
    """续段库字面量：从现 r40 块 _R40_LIBRARY 解析（与全件同库，sha 0236c30e…）。"""
    text = Path(FULL_R40_MAIN).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "_R40_LIBRARY"
                for t in node.targets):
            return ast.get_source_segment(text, node) or ""
    raise RuntimeError("现 r40 块内 _R40_LIBRARY 不可得")


def _probe_tail(names: Sequence[str]) -> str:
    """探针尾块：父层捕获+所选运行时件+单参包装（链条只含所选件）。"""
    segs = _runtime_sources(names)
    lines = [_PREAMBLE % ("components=%s" % (tuple(names),)),
             "_R40P_CALLABLES = [v for k, v in list(globals().items())"
             " if callable(v) and not k.startswith(\"__\")]",
             "_R40P_PARENT = _R40P_CALLABLES[-1] if _R40P_CALLABLES else None"]
    if "route_select" in names:
        seg = _library_literal()
        head = "_R40_LIBRARY = "
        if not seg.startswith(head):
            raise RuntimeError("库字面量形态异常: %r" % seg[:40])
        lines.append("_R40P_LIBRARY = " + seg[len(head):])
    body = "\n\n\n".join(segs[RUNTIME_FUNCS[n]] for n in names)
    steps = []
    if "route_select" in names:
        steps.append(
            "    try:\n"
            "        _r40p_agent._last_select = _route40_select(\n"
            "            observation, globals().get(\"_R40P_LIBRARY\"))\n"
            "    except Exception:\n"
            "        pass")
    if "race_slots" in names:
        steps.append(
            "    try:\n"
            "        action = apply_race_slots(observation, action)\n"
            "    except Exception:\n"
            "        pass")
    if "slot_hygiene" in names:
        steps.append(
            "    try:\n"
            "        out = apply_slot_hygiene(observation, action)\n"
            "        if isinstance(out, dict) and isinstance(out.get(\"action\"),\n"
            "                dict):\n"
            "            action = out[\"action\"]\n"
            "    except Exception:\n"
            "        pass")
    agent = (
        'def _r40p_agent(observation):\n'
        '    """探针单参入口：父层动作→所选运行时件链（fail-safe 原样）。"""\n'
        '    parent = globals().get("_R40P_PARENT")\n'
        '    if not callable(parent):\n'
        '        return {"farmer": ["PASS"], "hands": [], "market": []}\n'
        '    try:\n'
        '        action = parent(observation)\n'
        '    except Exception:\n'
        '        return {"farmer": ["PASS"], "hands": [], "market": []}\n'
        '    if not isinstance(action, dict):\n'
        '        return {"farmer": ["PASS"], "hands": [], "market": []}\n'
        + ("\n".join(steps) + "\n" if steps else "")
        + "    return action")
    return "\n\n" + "\n".join(lines) + "\n\n\n" + body + "\n\n\n" + agent + "\n"


def build_probe_text(variant: str) -> str:
    """探针 main 文本：V0=r37 原样；V2=磁带手术；V1/V3/V4=底版+探针尾块；
    V5=现 r40 全件文本；V2f/V4f=修后单件（V2f 只同拍并单、V4f 用已修
    runtime_r40 源）。"""
    if variant == "V5":
        return Path(FULL_R40_MAIN).read_text(encoding="utf-8")
    t37 = Path(R37_MAIN).read_text(encoding="utf-8")
    if variant == "V0":
        return t37
    allv = dict(VARIANTS)
    allv.update(FIXED_VARIANTS)
    if variant not in allv:
        raise ValueError("未知探针变体: %r（仅 %s）"
                         % (variant, sorted(allv)))
    names = allv[variant]
    if names == ("sell_lots",):
        from orderbook_r37 import retape_sheep as _rs
        from orderbook_r40 import retape_lots as _rt
        pkg = _rs._decode_routes(t37)
        lot = _rt.retape_sell_lots(
            pkg, cross_step=variant not in CROSS_STEP_OFF)
        return _rs._encode_routes(t37, lot["routes"])
    return t37 + _probe_tail(names)


def build_probe(variant: str, out_dir: Optional[str] = None) -> str:
    """探针 main 落盘（确定性：同变体同字节）；返回路径。"""
    out = Path(out_dir) if out_dir is not None else \
        MODULE_DIR / "build" / "ablation"
    out.mkdir(parents=True, exist_ok=True)
    text = build_probe_text(variant)
    compile(text, "<probe %s>" % variant, "exec")
    path = out / ("probe_%s.py" % variant.lower())
    path.write_text(text, encoding="utf-8")
    return str(path)


def build_all_probes(out_dir: Optional[str] = None) -> Dict[str, str]:
    """V0-V5 全探针落盘（V5=现 r40 快照，防后续重建覆写对照件）。"""
    out = Path(out_dir) if out_dir is not None else \
        MODULE_DIR / "build" / "ablation"
    out.mkdir(parents=True, exist_ok=True)
    paths: Dict[str, str] = {}
    for v in ("V0", "V1", "V2", "V3", "V4", "V5"):
        if v == "V5":
            snap = out / "probe_v5.py"
            snap.write_text(Path(FULL_R40_MAIN).read_text(encoding="utf-8"),
                            encoding="utf-8")
            compile(snap.read_text(encoding="utf-8"), "<probe V5>", "exec")
            paths[v] = str(snap)
        else:
            paths[v] = build_probe(v, str(out))
    return paths


# --------------------------------------------------------------- 局表面 --

def _arm_specs(cand: str, opp: Dict[str, str], arm: str,
               seeds: Sequence[int], kind: str) -> List[Dict[str, Any]]:
    """单臂局表（judge_r23._league_specs._arm 同构：每 seed 双席，独立 seed）。"""
    specs: List[Dict[str, Any]] = []
    for seed in seeds:
        for seat in (0, 1):
            a = {"type": "python", "path": cand}
            b = dict(opp)
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "ab-%s-%d-s%d" % (arm, seed, seat),
                "seed": int(seed), "kind": kind, "arm": arm,
                "our_seat": seat, "trace": False, "agents": agents})
    return specs


def probe_plans(paths: Mapping[str, str], n_h2h: int = N_H2H_DEFAULT,
                n_strong: int = N_STRONG_DEFAULT,
                corpus: Any = None) -> Dict[str, Any]:
    """全探针三面局表+败局基线（judge_r23 同语料同口径）。"""
    opps = [str(KSIM_DIR / rel) for rel in STRONG_OPPONENTS]
    for p in [R37_MAIN] + opps:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)
    h2h_seeds = [H2H_SEED_BASE + i for i in range(int(n_h2h))]
    per = max(1, int(n_strong) // len(opps))
    strong_arms: List[Tuple[str, str, List[int]]] = []
    for j, p in enumerate(opps):
        label = "%s_%s" % (Path(p).parent.parent.name, Path(p).parent.name)
        strong_arms.append(
            (label, p, [STRONG_SEED_BASE + j * 1000 + i for i in range(per)]))
    items = _j23._load_items(corpus if corpus is not None
                             else list(_b40.LOSS_IDS))
    baselines: Dict[Any, Dict[int, Dict[str, Any]]] = {}
    for it in items:
        replay = json.loads(Path(it["path"]).read_text(encoding="utf-8"))
        per_seat: Dict[int, Dict[str, Any]] = {}
        for seat in (0, 1):
            rows, _meta = _j23._states_from_replay(replay, seat, it["seed"])
            per_seat[seat] = _j23.segment_stats(rows)
        baselines[it["episode"]] = per_seat
    plans: Dict[str, Any] = {}
    for variant, path in sorted(paths.items()):
        specs: List[Dict[str, Any]] = []
        if variant != "V0":          # V0=r37 自我对镜像零信息面，跳过 h2h
            specs.extend(_arm_specs(path, {"type": "python", "path": R37_MAIN},
                                    "%s_h2h_r37" % variant, h2h_seeds,
                                    "h2h"))
        for label, opp_path, seeds in strong_arms:
            specs.extend(_arm_specs(
                path, {"type": "python", "path": opp_path},
                "%s_strong_%s" % (variant, label), seeds, "strong"))
        for it in items:
            tape = {"type": "tape", "actions": it["opp_actions"]}
            cand = {"type": "python", "path": path}
            for seat in (0, 1):
                agents = [cand, tape] if seat == 0 else [tape, cand]
                specs.append({
                    "game_id": "ab-%s-dir-%d-s%d" % (variant, it["episode"],
                                                     seat),
                    "seed": it["seed"], "kind": "directed", "arm":
                        "%s_loss_replay" % variant, "our_seat": seat,
                    "episode": it["episode"], "trace": True,
                    "agents": agents})
        plans[variant] = {"path": path, "specs": specs}
    return {"plans": plans, "items": items, "baselines": baselines,
            "h2h_seeds": h2h_seeds,
            "strong_seeds": {label: list(seeds)
                             for label, _p, seeds in strong_arms}}


def play(specs: Sequence[Dict[str, Any]], workers: int = 16) -> List[Dict[str, Any]]:
    """三面局表并行跑口（judge_r23._play_batch 判决跑口，仿真器快线）。"""
    cfg = {"engine": "sim", "workers": int(workers)}
    return _j23._play_batch(list(specs), cfg)


def _seg_readings(rows: Sequence[Dict[str, Any]],
                  baselines: Dict[Any, Dict[int, Dict[str, Any]]]
                  ) -> Dict[str, Any]:
    """定向局→d21-28 段差/实现单价/有效挂单读数（judge_r23 同口径）。"""
    vals: List[Any] = []
    px: List[Any] = []
    fill: List[Any] = []
    n_red = 0
    for r in rows:
        if r.get("kind") != "directed":
            continue
        if r.get("error"):
            n_red += 1
        base = (baselines.get(r.get("episode")) or {}).get(int(r["our_seat"]))
        try:
            st = _j23.segment_stats(r.get("states") or [], baseline=base)
        except Exception:
            st = None
        vals.append((st or {}).get("seg_delta"))
        px.append((st or {}).get("verdict", {}).get("realized_px_up_pct"))
        fill.append((st or {}).get("fill_rate"))
    med = lambda xs: (round(float(statistics.median(
        [x for x in xs if _j23._num(x) is not None])), 2)
        if any(_j23._num(x) is not None for x in xs) else None)  # noqa: E731
    return {"seg_delta_median": med(vals), "seg_delta_values": vals,
            "realized_px_up_pct_median": med(px), "fill_rate_median": med(fill),
            "n_games": len(vals), "n_red": n_red}


def faces_of(variant: str, rows: Sequence[Dict[str, Any]],
             baselines: Dict[Any, Dict[int, Dict[str, Any]]]) -> Dict[str, Any]:
    """单变体三面读数（h2h/强臂/段差）。"""
    def _of(kind: str, prefix: str = "") -> List[Dict[str, Any]]:
        return [r for r in rows if r.get("kind") == kind
                and (not prefix or str(r.get("arm", "")).startswith(prefix))]
    arm = variant
    h2h_rows = [r for r in rows if r.get("kind") == "h2h"]
    strong_rows = [r for r in rows if r.get("kind") == "strong"]
    h2h = _j23._arm_rate(h2h_rows) if h2h_rows else {"rate": None,
                                                     "n_seeds": 0}
    strong = _j23._arm_rate(strong_rows) if strong_rows else {"rate": None,
                                                              "n_seeds": 0}
    by_opp: Dict[str, Any] = {}
    for r in strong_rows:
        by_opp.setdefault(str(r.get("arm")), []).append(r)
    seg = _seg_readings(_of("directed"), baselines)
    return {"variant": arm, "h2h_rate": h2h.get("rate"),
            "h2h_seeds": h2h.get("n_seeds"), "h2h_detail": h2h,
            "strong_rate": strong.get("rate"),
            "strong_seeds": strong.get("n_seeds"),
            "strong_detail": strong,
            "strong_by_opp": {k: _j23._arm_rate(v)
                              for k, v in sorted(by_opp.items())},
            "seg": seg}


# --------------------------------------------------------------- 效应表 --

def decide_effects(table: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """效应表→逐组件处置（决策规则预绑定：留强砍弱；①优先保）。"""
    base = table.get("V0") or {}
    out: List[Dict[str, Any]] = []
    for comp, variant in (("route_select", "V1"), ("sell_lots", "V2"),
                          ("race_slots", "V3"), ("slot_hygiene", "V4")):
        row = table.get(variant) or {}
        h2h = row.get("h2h_rate")
        strong_delta = None
        if row.get("strong_rate") is not None and \
                base.get("strong_rate") is not None:
            strong_delta = round(float(row["strong_rate"])
                                 - float(base["strong_rate"]), 4)
        seg_delta_delta = None
        if (row.get("seg") or {}).get("seg_delta_median") is not None and \
                (base.get("seg") or {}).get("seg_delta_median") is not None:
            seg_delta_delta = round(
                float(row["seg"]["seg_delta_median"])
                - float(base["seg"]["seg_delta_median"]), 2)
        keep = bool(h2h is not None and h2h >= T_KEEP_H2H) or bool(
            strong_delta is not None and strong_delta >= T_STRONG_SIGNIFICANT)
        poison = bool(h2h is not None and h2h <= T_POISON_H2H)
        if keep:
            decision, why = "keep", ("h2h≥%.2f 或强臂显著升（%+.4f）"
                                     % (T_KEEP_H2H, strong_delta or 0.0))
        elif poison:
            if comp == "route_select":
                decision = "fix"   # ①优先保：毒也只修切换逻辑不全砍
                why = ("毒药但①优先保（用户裁决）——修切换逻辑不全砍"
                       "（保守阈值/无族不切）")
            else:
                decision = "cut_or_fix"
                why = "毒药（h2h≤%.2f）→砍或修（修=机制层最小修正+单件复测）" \
                      % T_POISON_H2H
        else:
            decision, why = "keep_annotated", (
                "中间面（%.2f<h2h<%.2f 且强臂未显著升）→保留标注"
                % (T_POISON_H2H, T_KEEP_H2H) if h2h is not None else
                "h2h 不可得→保留标注")
        out.append({"component": comp, "variant": variant,
                    "h2h_rate": h2h, "strong_rate": row.get("strong_rate"),
                    "strong_delta_vs_v0": strong_delta,
                    "seg_delta_median": (row.get("seg") or {}).get(
                        "seg_delta_median"),
                    "seg_delta_delta_vs_v0": seg_delta_delta,
                    "decision": decision, "why": why})
    return out


def build_effect_table(faces: Mapping[str, Any]) -> Dict[str, Any]:
    """三面读数→效应表（含 V0 基线/V5 对照/逐组件处置）。"""
    table = {v: faces[v] for v in sorted(faces)}
    return {"table": table, "disposition": decide_effects(table),
            "decision_rules": {
                "keep": "h2h≥%.2f 或 强臂差分≥%+.2f（显著升）"
                        % (T_KEEP_H2H, T_STRONG_SIGNIFICANT),
                "poison": "h2h≤%.2f→砍或修（修=机制层最小修正+单件复测）"
                          % T_POISON_H2H,
                "middle": "中间→保留标注",
                "route_priority": "①route_select 优先保：毒也只修切换逻辑"
                                  "（保守阈值/无族不切）不全砍",
            }}


# --------------------------------------------------------------- 编排 --

def run_ablation(out_dir: Optional[str] = None, workers: int = 16,
                 n_h2h: int = N_H2H_DEFAULT,
                 n_strong: int = N_STRONG_DEFAULT,
                 probe_dir: Optional[str] = None) -> Dict[str, Any]:
    """消融实跑：建 V0-V5 探针→三面并行→效应表→evidence 落盘。

    签名意图：输入: 落点/并行度/局量 / 输出: evidence dict（效应表+处置）/
    错误: 局红计入不短路（fail-closed 进读数）。
    """
    root = Path(out_dir) if out_dir is not None else MODULE_DIR
    ev_dir = root / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    paths = build_all_probes(probe_dir)
    plan = probe_plans(paths, n_h2h=n_h2h, n_strong=n_strong)
    rows: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for variant in sorted(plan["plans"]):
        got = play(plan["plans"][variant]["specs"], workers=workers)
        for r in got:
            r["variant"] = variant
            if r.get("error"):
                errors.append({"scope": "game", "variant": variant,
                               "game_id": r.get("game_id"),
                               "error": r.get("error")})
        rows.extend(got)
    faces = {v: faces_of(v, [r for r in rows if r.get("variant") == v],
                         plan["baselines"])
             for v in sorted(plan["plans"])}
    eff = build_effect_table(faces)
    evidence: Dict[str, Any] = {
        "ablation": "ablation_r40", "version": RECORD_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "components": list(COMPONENTS),
        "variants": {v: list(VARIANTS.get(v, ())) for v in sorted(VARIANTS)},
        "probe_paths": paths,
        "probe_sha256": {v: hashlib.sha256(
            Path(p).read_bytes()).hexdigest() for v, p in sorted(paths.items())},
        "config": {"n_h2h": int(n_h2h), "n_strong": int(n_strong),
                   "workers": int(workers), "engine": "sim",
                   "strong_opponents": list(STRONG_OPPONENTS),
                   "corpus": [it["episode"] for it in plan["items"]],
                   "h2h_seed_base": H2H_SEED_BASE,
                   "strong_seed_base": STRONG_SEED_BASE},
        "faces": faces,
        "effect_table": eff,
        "errors": errors,
        "counts": {"games": len(rows),
                   "red": sum(1 for r in rows if r.get("error"))},
    }
    path = ev_dir / "ablation_r40_realrun.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    evidence["evidence_path"] = str(path)
    return evidence


if __name__ == "__main__":                       # 脚本态实跑（判决级）
    ev = run_ablation()
    print(json.dumps({"effect_table": ev["effect_table"]["table"],
                      "disposition": ev["effect_table"]["disposition"],
                      "counts": ev["counts"]},
                     ensure_ascii=False, indent=1))


# ------------------------------------------------------- 修后单件复测 --

def run_retest(out_dir: Optional[str] = None, workers: int = 16,
               n_h2h: int = N_H2H_DEFAULT,
               n_strong: int = N_STRONG_DEFAULT,
               probe_dir: Optional[str] = None) -> Dict[str, Any]:
    """修后单件复测（毒药件机制修正后 V2f/V4f 三面同口径）→处置更新留档。

    签名意图：输入: 落点/并行度/局量 / 输出: evidence dict（复测三面+处置）/
    错误: 局红计入不短路。evidence 落 evidence/ablation_retest_realrun.json。
    """
    root = Path(out_dir) if out_dir is not None else MODULE_DIR
    ev_dir = root / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    out = Path(probe_dir) if probe_dir is not None else \
        MODULE_DIR / "build" / "ablation"
    paths = {v: build_probe(v, str(out)) for v in FIXED_VARIANTS}
    plan = probe_plans(paths, n_h2h=n_h2h, n_strong=n_strong)
    rows: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for variant in sorted(plan["plans"]):
        got = play(plan["plans"][variant]["specs"], workers=workers)
        for r in got:
            r["variant"] = variant
            if r.get("error"):
                errors.append({"scope": "game", "variant": variant,
                               "game_id": r.get("game_id"),
                               "error": r.get("error")})
        rows.extend(got)
    faces = {v: faces_of(v, [r for r in rows if r.get("variant") == v],
                         plan["baselines"])
             for v in sorted(plan["plans"])}
    # 处置复判：复测面映射回规范变体名（V2f→V2、V4f→V4）套同一决策规则，
    # 相对消融 V0 基线（消融 evidence 缺→None 差分）。
    canon = {"V0": _v0_baseline(ev_dir)}
    fixmap = {"V2f": "V2", "V4f": "V4"}
    canon.update({fixmap[v]: f for v, f in faces.items()})
    eff = build_effect_table(canon)
    back = {"V2": "V2f", "V4": "V4f"}
    disposition = [dict(d, variant=back.get(d["variant"], d["variant"]),
                        retested=True)
                   for d in eff["disposition"]
                   if d["variant"] in back]
    base = {"V0": canon["V0"]}
    evidence: Dict[str, Any] = {
        "ablation": "ablation_r40_retest", "version": RECORD_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "fixes": {
            "V2f": "retape_sell_lots cross_step=False（合并合没时机机制修正："
                   "只同拍并单，零时序移动）",
            "V4f": "apply_slot_hygiene 清坑只清 qty==0 真占坑单（站立限价单"
                   "误杀机制修正）",
        },
        "probe_paths": paths,
        "probe_sha256": {v: hashlib.sha256(
            Path(p).read_bytes()).hexdigest() for v, p in sorted(paths.items())},
        "config": {"n_h2h": int(n_h2h), "n_strong": int(n_strong),
                   "workers": int(workers), "engine": "sim",
                   "strong_opponents": list(STRONG_OPPONENTS),
                   "corpus": [it["episode"] for it in plan["items"]]},
        "faces": faces,
        "v0_baseline": base["V0"],
        "disposition": disposition,
        "decision_rules": eff["decision_rules"],
        "errors": errors,
        "counts": {"games": len(rows),
                   "red": sum(1 for r in rows if r.get("error"))},
    }
    path = ev_dir / "ablation_retest_realrun.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    evidence["evidence_path"] = str(path)
    return evidence


def _v0_baseline(ev_dir: Path) -> Dict[str, Any]:
    """V0 基线读数：消融 evidence 的 V0 面（缺→空壳）。"""
    try:
        old = json.loads(
            (ev_dir / "ablation_r40_realrun.json").read_text(encoding="utf-8"))
        return (old.get("faces") or {}).get("V0") or {}
    except Exception:
        return {}
