# -*- coding: utf-8 -*-
"""build_route_library（R23 L2）：续段库构建。

责任契约：历史对局（败局 12 局+胜局+top-30 回放）按"开局长相族"（前 144 步
宏观指纹聚类，623 族口径）提取好路线续段（step144 后段）；败局世界定向补路由
（牛奶流/羊毛流/鹅蛋流对手开局族覆盖率审计）；输出紧凑库+构建审计。

【族键量化与拼接口径】（与 runtime_r40._route40_select 两件共同约定）
  family_key = "<hires>|<land_buys>|<tiles_by_crop>|<首二店>"
  - hires：前 144 步（步标 0..143）累计雇工数——观察面口径：farms[我方].hands
    计数正增量逐步累计（起点=步标 0 计数；日结清零后复雇计复雇）。
  - land_buys：同窗累计买地次数——unlocked_quadrants 计数正增量逐步累计。
  - tiles_by_crop：step144 当拍各作物地块数有序元组——(count 降序, 作物名
    升序) 渲染 "CROP:n,...",无作物="NONE"（计 crop 非空的地块格）。
  - 首二店：step144 当拍 town.unlocked_shops[:2] 串（"+" 连接，空="NONE"）。
  例："25|0|MELON:12,STRAWBERRY:4,WHEAT:3|BAKERY+FARMERS_MARKET"。
  replay 约定：entry t 的观察=步标 t（step 字段或 day*24+hour，实测 77 局两座
  席全同）；步标错位/缺步标→解析失败即抛。

【route 可得性口径】route=磁带路由 id（r37 磁带 41 条，int）。每局按"局的
  路由锁存"复刻推断：r37 _router 于 step>=144 以 unlocked_shops[:2] 店对锁存
  （无 YARN→_R108_SHOP_ROUTES 缺省 100 / 含 YARN→_R110_OLD_SHOPS 缺省 0；
  _V92_TABLE 覆盖；'YARN_STORE' 在店对且 rkey 命中 _V93_ROUTE_BY_RIVAL 时特例；
  rkey=(round(对手 step2 资金,3), int(market.inventory.WHEAT@step2))）。表来源：
  family_cfg["shop_route_map"]（严格模式，仅该表，未命中→"unknown"）或
  family_cfg["latch_main"]/自动发现 ../orderbook_r37/build/main.py 解码
  _R108_DATA 复刻全式；表不可得→全 "unknown"。unknown 局入族统计
  （n_games/win_rate/margin_mean）但不进 segments 与 best_route 选优。

【margin 口径】margin=终局资金差（我方−对手，结局口径；W/L=margin>0 为胜）；
  续段 margin=step144→终局资金差增量（我方−对手）。家族 margin_mean=终局
  margin 均值；segments.margin_mean=续段 margin 均值；best_route=该族胜局中
  续段 margin_mean 最优的 route id（同 route 胜局续段 margin 均值最大；并列取
  胜局多者、再取 route id 小者；无带 route 胜局→None）。

【败局世界口径】按 analysis24 三型对手阈值（family_cfg["defeat_thresholds"]
  可调）把败局族归入 defeat_worlds，一局可入多世界：
  - milk_flow：对手 COW≥6 且 MILK 收入占比≥0.30（占对手总流入；实测 12 败局
    谱系 0.094↔0.448 天然分界）
  - wool_flow：对手 SHEEP≥10；- goose_flow：对手 GOOSE≥5
  对手阵容取 replay 末拍观察；MILK 收入占比=对手 SELL 流水按 qty×挂牌价加权
  归因的 MILK 流入/总流入。covered=该世界败局族全部在 families 里有胜局
  best_route（空家族列表→False）。

库结构（与 _route40_select 两件共同约定）：
  {"version": "routelib/1.0", "families": {族键: 族项}, "default": 族项,
   "defeat_worlds": {世界: {"families": [...], "covered": bool}},
   "build_audit": {"n_games","n_families","coverage","uncovered_families",
                   "library_sha"}}
  族项={"n_games","win_rate","best_route","margin_mean",
        "segments": {str(route_id): {"n","win_rate","margin_mean"}}}
  返回 {"library": 库, "build_audit": 构建审计}；fail-closed：语料 <min_games
  （默认 30 局）或解析失败→抛。
"""
from __future__ import annotations

import ast
import base64
import hashlib
import json
import re
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPLAY_GLOB = "episode-*-replay.json"
MIN_GAMES_DEFAULT = 30
DEFAULT_OUR_NAME = "renyxin"
LIBRARY_VERSION = "routelib/1.0"
REVEAL_STEP = 144
DEFAULT_DEFEAT_THRESHOLDS: Dict[str, Dict[str, float]] = {
    "milk_flow": {"COW": 6, "MILK_share": 0.30},
    "wool_flow": {"SHEEP": 10},
    "goose_flow": {"GOOSE": 5},
}
DEFEAT_WORLDS = ("milk_flow", "wool_flow", "goose_flow")
_R37_MAIN_REL = ("orderbook_r37", "build", "main.py")
_BLOB_RE = re.compile(
    r"_R108_DATA\s*=\s*json\.loads\(zlib\.decompress\(base64\.b85decode\('([^']+)'\)\)\)")


def _jl(x: Any) -> Any:
    """replay 内嵌 JSON 串解码（非串原样返回）。"""
    return json.loads(x) if isinstance(x, str) else x


def _mean(vals: List[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def _step_label(obs: Dict[str, Any]) -> int:
    """观察步标：step 字段或 day*24+hour（与 r37 _step_of 同式）。"""
    raw = obs.get("step")
    if raw is not None:
        return int(raw)
    return int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))


def _farm_view(obs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], int]:
    """观察→(我方 farm, 对手 farm, player 座位)。"""
    farms = _jl(obs.get("farms"))
    if not isinstance(farms, list) or len(farms) != 2:
        raise ValueError("farms 须为 2 座席 list")
    seat = int(obs.get("player", 0))
    if seat not in (0, 1):
        raise ValueError("player 座位非法")
    for f in farms:
        if not isinstance(f, dict):
            raise ValueError("farm 须为 dict")
    return farms[seat], farms[1 - seat], seat


def _tiles_by_crop(farm: Dict[str, Any]) -> Dict[str, int]:
    """step144 时点各作物地块数（crop 非空的地块格计数）。"""
    crops: Dict[str, int] = {}
    for row in (_jl(farm.get("tiles")) or []):
        if not isinstance(row, list):
            continue
        for cell in row:
            if isinstance(cell, dict) and cell.get("crop"):
                c = str(cell["crop"])
                crops[c] = crops.get(c, 0) + 1
    return crops


def _family_key(hires: int, land_buys: int, tiles_by_crop: Dict[str, int],
                shops: List[str]) -> str:
    """族键量化拼接（口径见模块 docstring；与运行时逐字同式）。"""
    tiles_str = ",".join(
        "%s:%d" % (crop, n) for crop, n in
        sorted((tiles_by_crop or {}).items(), key=lambda kv: (-kv[1], kv[0]))) or "NONE"
    shops_str = "+".join(str(s) for s in list(shops or [])[:2]) or "NONE"
    return "%d|%d|%s|%s" % (int(hires), int(land_buys), tiles_str, shops_str)


def _load_latch(family_cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """路由锁存表加载（口径见模块 docstring）；表不可得→None（全 unknown）。"""
    if family_cfg.get("shop_route_map") is not None:
        raw = family_cfg["shop_route_map"]
        if not isinstance(raw, dict):
            raise ValueError("shop_route_map 须为 dict")
        table = {}
        for k, v in raw.items():
            parts = tuple(str(k).split("+"))
            if len(parts) != 2:
                raise ValueError("shop_route_map 键须为 'SHOP1+SHOP2': %r" % (k,))
            table[parts] = int(v)
        return {"strict": True, "shop_routes": table, "old_shops": {}, "v92": {},
                "v93": {}}
    main_path = family_cfg.get("latch_main")
    explicit = main_path is not None
    if main_path is None:
        cand = Path(__file__).resolve().parent.parent.joinpath(*_R37_MAIN_REL)
        main_path = cand if cand.exists() else None
    if main_path is None or not Path(main_path).exists():
        return None
    try:
        text = Path(main_path).read_text(encoding="utf-8")
        tables = _parse_latch_tables(text)
    except Exception as exc:
        if explicit:
            raise ValueError("路由锁存表解析失败 %s: %r" % (main_path, exc)) from exc
        return None
    tables["strict"] = False
    return tables


def _parse_latch_tables(text: str) -> Dict[str, Any]:
    """r37 main 文本→锁存四表（复刻 _router 组合口径）。"""
    m = _BLOB_RE.search(text)
    if not m:
        raise ValueError("r37 main 无 _R108_DATA blob")
    data = json.loads(zlib.decompress(base64.b85decode(m.group(1))))
    if not isinstance(data, dict) or not isinstance(data.get("shops"), list):
        raise ValueError("_R108_DATA 形态非法")
    shop_routes = {}
    for r in data["shops"]:
        if not isinstance(r, dict) or not isinstance(r.get("shops"), list):
            raise ValueError("shops 表行形态非法")
        shop_routes[tuple(r["shops"])] = int(r["route"])

    def _table(name: str) -> Dict[Any, int]:
        mm = re.search(r"^%s\s*=\s*(\{.*\})\s*$" % name, text, re.M)
        if not mm:
            raise ValueError("r37 main 缺 %s" % name)
        val = ast.literal_eval(mm.group(1))
        if not isinstance(val, dict):
            raise ValueError("%s 须为 dict" % name)
        return val

    return {"shop_routes": shop_routes,
            "old_shops": _table("_R110_OLD_SHOPS"),
            "v92": _table("_V92_TABLE"),
            "v93": _table("_V93_ROUTE_BY_RIVAL")}


def _latch_route(latch: Optional[Dict[str, Any]], shops: List[str],
                 rkey: Any) -> Any:
    """局的路由锁存推断；不可推断→"unknown"。"""
    if latch is None:
        return "unknown"
    pair = tuple(list(shops or [])[:2])
    if latch.get("strict"):
        route = latch["shop_routes"].get(pair)
        return int(route) if route is not None else "unknown"
    use_new = pair.count("YARN_STORE") <= 0
    route = latch["shop_routes"].get(pair, 100) if use_new else \
        latch["old_shops"].get(pair, 0)
    route = latch["v92"].get(pair, route)
    if "YARN_STORE" in pair and rkey in latch["v93"]:
        route = latch["v93"][rkey]
    return int(route)


def _collect_replays(game_dir: Any) -> List[str]:
    """语料收集：目录（episode-*-replay.json）或显式文件；按 episode 去重。"""
    if isinstance(game_dir, (str, Path)):
        items = [game_dir]
    else:
        items = list(game_dir or [])
    if not items:
        raise ValueError("game_dir 为空")
    out: List[str] = []
    seen = set()
    for item in items:
        p = Path(item)
        if p.is_dir():
            cand = sorted(p.glob(REPLAY_GLOB))
        elif p.is_file():
            cand = [p]
        else:
            raise ValueError("语料路径不存在: %s" % p)
        for f in cand:
            mm = re.match(r"episode-(\d+)-replay\.json$", f.name)
            key = mm.group(1) if mm else f.name
            if key in seen:
                continue
            seen.add(key)
            out.append(str(f))
    return out


def _opponent_profile(opp_farm: Dict[str, Any]) -> Dict[str, int]:
    """对手阵容计数（末拍观察 PASTURE/COOP 地块上的动物）。"""
    counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in (_jl(opp_farm.get("tiles")) or []):
        if not isinstance(row, list):
            continue
        for cell in row:
            if isinstance(cell, dict) and cell.get("animal"):
                a = str(cell["animal"])
                counts[a] = counts.get(a, 0) + 1
    return counts


def _parse_game(path: str, our_name: str,
                latch: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """单局提取（开局指纹族/结局 W/L/margin/route 可得性/败局世界画像）。"""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError("replay 解析失败 %s: %r" % (path, exc)) from exc
    if not isinstance(data, dict):
        raise ValueError("replay 须为 dict: %s" % path)
    names = ((data.get("info") or {}).get("TeamNames")) or []
    if our_name not in names or len(names) != 2:
        raise ValueError("replay 无我方座位 %r: %s" % (our_name, path))
    our = names.index(our_name)
    steps = data.get("steps")
    if not isinstance(steps, list) or len(steps) < REVEAL_STEP + 1:
        raise ValueError("replay 步数不足 %d: %s" % (REVEAL_STEP, path))

    hires = 0
    land = 0
    hands_prev: Optional[int] = None
    uq_prev: Optional[int] = None
    margin_144 = 0.0
    crops_144: Dict[str, int] = {}
    shops_144: List[str] = []
    rkey = None
    opp_income: Dict[str, float] = {}
    inflow_total = 0.0
    opp_money_prev: Optional[float] = None
    our_money_last = 0.0
    opp_money_last = 0.0
    opp_farm_last: Dict[str, Any] = {}

    for t, entry in enumerate(steps):
        if not isinstance(entry, list) or len(entry) != 2 or \
                not all(isinstance(e, dict) for e in entry):
            raise ValueError("replay entry 形态非法 @%d: %s" % (t, path))
        obs = _jl(entry[our].get("observation"))
        if not isinstance(obs, dict):
            raise ValueError("replay 观察缺失 @%d: %s" % (t, path))
        if _step_label(obs) != t:
            raise ValueError("replay 步标错位 @%d: %s" % (t, path))
        farm, opp_farm, _seat = _farm_view(obs)
        try:
            money = float(farm.get("money", 0.0))
            opp_money = float(opp_farm.get("money", 0.0))
        except (TypeError, ValueError) as exc:
            raise ValueError("replay 资金非法 @%d: %s" % (t, path)) from exc
        hands = len(_jl(farm.get("hands")) or [])
        uq = len(_jl(farm.get("unlocked_quadrants")) or [])
        if t < REVEAL_STEP:
            if hands_prev is not None:
                if hands > hands_prev:
                    hires += hands - hands_prev
                if uq > uq_prev:
                    land += uq - uq_prev
            hands_prev, uq_prev = hands, uq
        elif t == REVEAL_STEP:
            crops_144 = _tiles_by_crop(farm)
            shops_144 = list(_jl((obs.get("town") or {})).get("unlocked_shops")
                            or [])[:2]
            margin_144 = money - opp_money
        if t == 2:
            try:
                rkey = (round(float(opp_money), 3),
                        int(_jl((obs.get("market") or {})).get("inventory", {})
                            .get("WHEAT")))
            except (TypeError, ValueError):
                rkey = None
        if opp_money_prev is not None and opp_money > opp_money_prev:
            inflow = opp_money - opp_money_prev
            inflow_total += inflow
            action = _jl(entry[1 - our].get("action")) or {}
            prices = _jl((_jl(entry[1 - our].get("observation")) or {})
                         .get("market") or {}).get("prices") or {}
            weights: Dict[str, float] = {}
            for cmd in (action.get("market") or []):
                if isinstance(cmd, list) and len(cmd) >= 3 and cmd[0] == "SELL":
                    item = str(cmd[1])
                    weights[item] = weights.get(item, 0.0) + \
                        max(0, int(cmd[2])) * float(prices.get(item, 1))
            wsum = sum(weights.values())
            if wsum > 0:
                for item, w in weights.items():
                    opp_income[item] = opp_income.get(item, 0.0) + inflow * w / wsum
        opp_money_prev = opp_money
        our_money_last, opp_money_last, opp_farm_last = money, opp_money, opp_farm

    margin = our_money_last - opp_money_last
    seg_margin = margin - margin_144
    prof = _opponent_profile(opp_farm_last)
    milk_share = (opp_income.get("MILK", 0.0) / inflow_total) if inflow_total > 0 else 0.0
    try:
        episode = int((data.get("info") or {}).get("EpisodeId"))
    except (TypeError, ValueError):
        mm = re.match(r"episode-(\d+)-replay\.json$", Path(path).name)
        if not mm:
            raise ValueError("replay 无 episode id: %s" % path)
        episode = int(mm.group(1))
    return {
        "episode": episode,
        "file": path,
        "family_key": _family_key(hires, land, crops_144, shops_144),
        "win": margin > 0,
        "margin": margin,
        "seg_margin": seg_margin,
        "route": _latch_route(latch, shops_144, rkey),
        "opp": {"COW": prof.get("COW", 0), "SHEEP": prof.get("SHEEP", 0),
                "GOOSE": prof.get("GOOSE", 0), "MILK_share": milk_share},
    }


def _agg_family(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """族项聚合（口径见模块 docstring）。"""
    n = len(rows)
    wins = [r for r in rows if r["win"]]
    segments: Dict[str, Dict[str, Any]] = {}
    by_route: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        if r["route"] == "unknown":
            continue
        by_route.setdefault(str(r["route"]), []).append(r)
    for rid, rs in sorted(by_route.items()):
        segments[rid] = {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r["win"]) / len(rs),
            "margin_mean": _mean([r["seg_margin"] for r in rs]),
        }
    win_margins: Dict[Any, List[float]] = {}
    for r in wins:
        if r["route"] == "unknown":
            continue
        win_margins.setdefault(r["route"], []).append(r["seg_margin"])
    best_route = None
    if win_margins:
        best_route = max(win_margins,
                         key=lambda rid: (_mean(win_margins[rid]),
                                          len(win_margins[rid]), -int(rid)))
    return {
        "n_games": n,
        "win_rate": len(wins) / n if n else 0.0,
        "best_route": best_route,
        "margin_mean": _mean([r["margin"] for r in rows]),
        "segments": segments,
    }


def build_route_library(game_dir: Any, family_cfg: Any = None) -> Dict[str, Any]:
    """续段库构建：开局长相聚类→好路线续段提取→败局世界补路由+覆盖率审计。

    签名意图：输入: 回放/对局目录+分族配置 / 输出: {library, build_audit} /
    错误: 语料不足或聚类失败即抛。

    family_cfg（可选 dict）：our_name（默认 "renyxin"）、min_games（默认 30）、
    defeat_thresholds（默认见 DEFAULT_DEFEAT_THRESHOLDS）、shop_route_map
    （严格锁存表 "SHOP1+SHOP2"→route id）、latch_main（r37 main 路径）。族键
    量化拼接/margin/败局世界口径见模块 docstring。
    """
    cfg = dict(family_cfg or {})
    our_name = str(cfg.get("our_name", DEFAULT_OUR_NAME))
    min_games = int(cfg.get("min_games", MIN_GAMES_DEFAULT))
    thresholds = {w: dict(DEFAULT_DEFEAT_THRESHOLDS[w]) for w in DEFEAT_WORLDS}
    for w, th in (cfg.get("defeat_thresholds") or {}).items():
        if w in thresholds and isinstance(th, dict):
            thresholds[w].update(th)
    latch = _load_latch(cfg)

    paths = _collect_replays(game_dir)
    games = [_parse_game(p, our_name, latch) for p in paths]
    if len(games) < min_games:
        raise ValueError("语料不足: %d 局 < %d 局" % (len(games), min_games))
    games.sort(key=lambda g: g["episode"])

    families_rows: Dict[str, List[Dict[str, Any]]] = {}
    for g in games:
        families_rows.setdefault(g["family_key"], []).append(g)
    families = {k: _agg_family(rows)
                for k, rows in sorted(families_rows.items())}
    default = _agg_family(games)

    defeat_worlds: Dict[str, Dict[str, Any]] = {}
    for world in DEFEAT_WORLDS:
        defeat_worlds[world] = {"families": [], "covered": False}
    for g in games:
        if g["win"]:
            continue
        prof, th = g["opp"], thresholds
        worlds = []
        if prof["COW"] >= th["milk_flow"]["COW"] and \
                prof["MILK_share"] >= th["milk_flow"]["MILK_share"]:
            worlds.append("milk_flow")
        if prof["SHEEP"] >= th["wool_flow"]["SHEEP"]:
            worlds.append("wool_flow")
        if prof["GOOSE"] >= th["goose_flow"]["GOOSE"]:
            worlds.append("goose_flow")
        for w in worlds:
            defeat_worlds[w]["families"].append(g["family_key"])
    for world in DEFEAT_WORLDS:
        fams = sorted(set(defeat_worlds[world]["families"]))
        defeat_worlds[world]["families"] = fams
        defeat_worlds[world]["covered"] = bool(fams) and all(
            families[f]["best_route"] is not None for f in fams)

    lib_core = {
        "version": LIBRARY_VERSION,
        "families": families,
        "default": default,
        "defeat_worlds": defeat_worlds,
    }
    lib_sha = hashlib.sha256(json.dumps(
        lib_core, sort_keys=True, ensure_ascii=False,
        separators=(",", ":")).encode("utf-8")).hexdigest()
    uncovered = sorted(k for k, v in families.items()
                       if v["best_route"] is None)
    build_audit = {
        "n_games": len(games),
        "n_families": len(families),
        "coverage": (len(families) - len(uncovered)) / len(families),
        "uncovered_families": uncovered,
        "library_sha": lib_sha,
    }
    library = dict(lib_core)
    library["build_audit"] = build_audit
    return {"library": library, "build_audit": build_audit}
