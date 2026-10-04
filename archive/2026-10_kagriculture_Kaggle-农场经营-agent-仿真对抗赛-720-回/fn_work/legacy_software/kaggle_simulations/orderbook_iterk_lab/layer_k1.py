# -*- coding: utf-8 -*-
"""layer_k1（iterk K1 防御层）：羊毛剪毛相位错峰——只做防御面。

责任口径（任务 K1）：把羊毛剪毛（HARVEST 取 WOOL）时序从公开相位
（d17/20/23/26/29）错开；**最小磁带手术**形态（运行时层不可行判据：H1 磁带
12 单元逐拍满编，无跨日空闲跑可借，运行时层无未来排程无法安全改道——静态
走位手术是唯一保链路可达的实现）。**量守恒零跨拍**：
- 量守恒=每格剪毛刀次与羊毛总量不变（每产毛单位仍被收一次；只平移相位，
  不丢刀不补刀）；
- 零跨拍=市场单槽零触碰（742943 空槽位次语义：订单槽不删/不移/不填，
  R23/R26 红线沿用）；手术只改单元指令（HARVEST 让刀/落刀 + 空闲拍走位）。
- d29 刀不挪（29+off 出季丢刀=违量守恒；d29 产毛只能 d29 收）——错峰覆盖
  d17/20/23/26 → d+1/d+2（d+1 优先=最小位移；目标日须落在产毛窗 [b+6,29]）。
- 逐刀独立手术、失败保原刀（per-cut fallback，绝不半途丢刀）；走位落点=
  retape_shear_phase._place_walk 先例（空闲跑 round/trail 形+走位链可达）。

复用（不改写）：orderbook_r37.retape_sheep（_decode_routes/_encode_routes/
_derive_grid_info/_shear_cells/_cow_action/_commit_action/_set_unit）+
orderbook_predict.retape_shear_phase（_cut_unit/_place_walk）。

读数件：
- static_shear_day_counts(pkg)：磁带口径逐日刀次（41 路由合计，错开前后对照）；
- shear_day_counts_from_sink(sink)：实跑口径逐日剪毛数（HARVEST 取 WOOL=
  单元 HARVEST 落在 yield_units>0 动物格；judgment 追踪槽口径）。
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_KSIM = str(Path(__file__).resolve().parent.parent)
if _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)
from orderbook_r37 import retape_sheep as _rs  # noqa: E402
from orderbook_predict import retape_shear_phase as _sp  # noqa: E402

RECORD_VERSION = "layer-k1/1.0"
# 公开相位（R22 毛期口径 d17/20/23/26/29 型）；d29=季末保留刀（量守恒）。
PUBLIC_PHASE: Tuple[int, ...] = (17, 20, 23, 26, 29)
MOVE_DAYS: Tuple[int, ...] = (17, 20, 23, 26)
KEEP_DAYS: Tuple[int, ...] = (29,)
DEFAULT_TARGETS: Tuple[int, ...] = (1, 2)   # d+1 优先，d+2 兜底（皆错开公开相）
FIRST_YIELD = 6
LAST_DAY = 29


# ------------------------------------------------------------- 手术 --
def retape_phase_offset(pkg: Dict[str, Any],
                        targets: Sequence[int] = DEFAULT_TARGETS,
                        move_days: Sequence[int] = MOVE_DAYS,
                        first_yield: int = FIRST_YIELD,
                        last_day: int = LAST_DAY) -> Dict[str, Any]:
    """毛期错峰手术（逐刀独立、失败保原刀、量守恒零跨拍）。

    签名意图：输入: 磁带路由包（_decode_routes 形）+偏移目标日序 / 输出:
    {routes, change_table, stats} / 错误: 入口形态非法即抛（fail-closed）。

    语义：
    - 每格羊剪毛刀（HARVEST 造访，_shear_cells 格位口径）落在 move_days
      （默认 d17/20/23/26）→ 依次尝试 targets 偏移日（默认 d+1 优先）：
      落点日须在产毛窗 [buy_day+first_yield, last_day] 且走位可达
      （_place_walk：空闲跑 round 形 2m+1≤span / trail 形单程驻留）；
      成功=源刀让刀（原 HARVEST→['PASS']）+落刀（走位链+HARVEST 写入空闲拍）；
      全失败=保原刀（change_table reason 记 no-move）。
    - KEEP_DAYS（d29）与非相位刀不动；市场单槽零触碰；源动作写时复制
      （_cow_action/_commit_action 池 append，路由指针改指新件）。
    - 术后静态核算：逐格刀次数守恒（n_cuts 不变=量守恒的结构面），违者抛。

    输出 change_table 逐行 {route, kind:"shear_phase", item:"WOOL", cell,
    from_day, to_day, from_step, to_step, unit, reason}；to_day==from_day=
    未挪（reason 起 "no-move"）。
    """
    if not isinstance(pkg, dict):
        raise TypeError("pkg must be dict, got %s" % type(pkg).__name__)
    _rs._check_package(pkg)
    work = copy.deepcopy(pkg)                 # 输入零改动（写时复制）
    grid = _rs._derive_grid_info(work)
    change_table: List[Dict[str, Any]] = []
    stats = {"cells": 0, "phase_cuts": 0, "moved": 0, "no_move": 0,
             "kept_d29": 0, "kept_other": 0, "by_target": {}}

    for rid in sorted(work["routes"], key=lambda k: int(k)):
        if rid not in grid:
            continue
        idxs = work["routes"][rid]
        g = grid[rid]
        pos: Dict[Tuple[int, str], Any] = g["unit_pos"]
        used: set = set()
        for c in sorted(g["cells"], key=repr):
            stats["cells"] += 1
            seq = [work["actions"][i] for i in idxs]
            info = _rs._shear_cells(seq, g)[c]
            b = int(info["buy_day"])
            cuts: List[Tuple[int, str]] = []
            for s in sorted(info["cuts"]):
                u = _sp._cut_unit(seq, s, c, pos)
                if u is not None:
                    cuts.append((s, u))
            for s, u in cuts:
                d = s // 24
                if d in KEEP_DAYS:
                    stats["kept_d29"] += 1
                    continue
                if d not in move_days:
                    stats["kept_other"] += 1
                    continue
                stats["phase_cuts"] += 1
                landed = None
                for off in targets:
                    tday = d + int(off)
                    if not (b + first_yield <= tday <= last_day):
                        continue
                    r = _sp._place_walk(work, idxs, rid, c, tday, pos, used)
                    if r is not None:
                        landed = (tday, r[0], r[1])
                        break
                if landed is None:
                    stats["no_move"] += 1
                    change_table.append({
                        "route": rid, "kind": "shear_phase", "item": "WOOL",
                        "cell": c, "from_day": d, "to_day": d,
                        "from_step": s, "to_step": s, "unit": u,
                        "reason": ("no-move: offset targets %s 不可行"
                                   "（出季/走位不可达），保原刀" % (list(targets),)),
                    })
                    continue
                tday, tstep, tunit = landed
                # 源刀让刀（写时复制）
                _, _, act = _rs._cow_action(work, rid, s)
                _rs._set_unit(act, u, ["PASS"])
                _rs._commit_action(work, idxs, s, act)
                stats["moved"] += 1
                key = "d%d->d%d" % (d, tday)
                stats["by_target"][key] = stats["by_target"].get(key, 0) + 1
                change_table.append({
                    "route": rid, "kind": "shear_phase", "item": "WOOL",
                    "cell": c, "from_day": d, "to_day": tday,
                    "from_step": s, "to_step": tstep,
                    "unit": u, "to_unit": tunit,
                    "reason": ("shear_phase offset: 剪毛刀 d%d@step%d 让刀，"
                               "落刀 d%d@step%d（unit %s→%s；量守恒零跨拍）"
                               % (d, s, tday, tstep, u, tunit)),
                })

    # ---- 术后静态核算：逐格刀次数守恒（量守恒结构面）----
    pre = _cell_cut_counts(pkg)
    post = _cell_cut_counts(work)
    if pre != post:
        bad = [k for k in set(pre) | set(post) if pre.get(k) != post.get(k)]
        raise RuntimeError("量守恒红：术后逐格刀次不守恒 %s" % bad[:6])
    # ---- 零跨拍核算：市场单槽逐格不变 ----
    if not _market_slots_identical(pkg, work):
        raise RuntimeError("零跨拍红：市场单槽被触碰")
    return {"routes": work, "change_table": change_table, "stats": stats}


def _cell_cut_counts(pkg: Dict[str, Any]) -> Dict[Tuple[Any, Any], int]:
    """逐 (route, cell) 刀次（_shear_cells n_cuts 口径）。"""
    grid = _rs._derive_grid_info(pkg)
    out: Dict[Tuple[Any, Any], int] = {}
    for rid in grid:
        seq = [pkg["actions"][i] for i in pkg["routes"][rid]]
        for c, v in _rs._shear_cells(seq, grid[rid]).items():
            out[(rid, repr(c))] = int(v["n_cuts"])
    return out


def _market_slots_identical(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """市场单槽逐槽恒等（零跨拍核算）：动作池差集内 market 列表须相等。"""
    if len(a["routes"]) != len(b["routes"]):
        return False
    for rid in a["routes"]:
        ia, ib = a["routes"][rid], b["routes"][rid]
        if len(ia) != len(ib):
            return False
        for x, y in zip(ia, ib):
            ma = a["actions"][x].get("market")
            mb = b["actions"][y].get("market")
            if ma != mb:
                return False
    return True


# ------------------------------------------------------------- 读数 --
def static_shear_day_counts(pkg: Dict[str, Any]) -> Dict[str, int]:
    """磁带口径逐日刀次（全部路由合计；刀=羊格 HARVEST 造访，_shear_cells）。"""
    grid = _rs._derive_grid_info(pkg)
    out: Dict[str, int] = {}
    for rid in sorted(grid, key=lambda k: int(k)):
        seq = [pkg["actions"][i] for i in pkg["routes"][rid]]
        for c, v in _rs._shear_cells(seq, grid[rid]).items():
            for s in v["cuts"]:
                d = s // 24
                out[str(d)] = out.get(str(d), 0) + 1
    return dict(sorted(out.items(), key=lambda kv: int(kv[0])))


def shear_day_counts_from_sink(sink: Any) -> Dict[str, int]:
    """实跑口径逐日剪毛数（HARVEST 取 WOOL=单元 HARVEST 落在 yield>0 动物格）。

    口径：追踪槽 (step, obs, act)；单元位=obs 起拍位（farmer/hands）；
    HARVEST 落格=该单元起拍所站格；格为 dict 且含 animal 且 yield_units>0
    =一次真剪毛（取毛）计当日一刀。异常条目跳过（fail-safe）。
    """
    out: Dict[str, int] = {}
    for entry in (sink or []):
        try:
            step, obs, act = entry[0], entry[1], entry[2]
            if not isinstance(obs, dict) or not isinstance(act, dict):
                continue
            day = int(step) // 24
            player = int(obs.get("player", 0))
            farms = obs.get("farms") or []
            if not (isinstance(farms, (list, tuple)) and 0 <= player < len(farms)):
                continue
            farm = farms[player]
            if not isinstance(farm, dict):
                continue
            tiles = farm.get("tiles") or []
            pos_f = farm.get("farmer")
            pos_h = farm.get("hands") or []
            units = [("F", pos_f)] + [("h%d" % i, p)
                                      for i, p in enumerate(pos_h)]
            ops = []
            fu = act.get("farmer")
            if isinstance(fu, list):
                ops.append(("F", fu))
            for i, h in enumerate(act.get("hands") or []):
                if isinstance(h, list):
                    ops.append(("h%d" % i, h))
            posmap = dict(units)
            for u, op in ops:
                if not (isinstance(op, list) and op and op[0] == "HARVEST"):
                    continue
                p = posmap.get(u)
                if not (isinstance(p, (list, tuple)) and len(p) >= 2):
                    continue
                x, y = int(p[0]), int(p[1])
                if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
                    continue
                tile = tiles[y][x]
                if isinstance(tile, dict) and tile.get("animal") \
                        and float(tile.get("yield_units", 0) or 0) > 0:
                    out[str(day)] = out.get(str(day), 0) + 1
        except Exception:
            continue
    return dict(sorted(out.items(), key=lambda kv: int(kv[0])))
