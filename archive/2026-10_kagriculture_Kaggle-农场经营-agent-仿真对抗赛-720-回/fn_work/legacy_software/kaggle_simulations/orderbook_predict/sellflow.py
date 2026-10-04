# -*- coding: utf-8 -*-
"""build_sellflow_library（R22 增补 v2）：对手卖流库构建（top-30 新鲜回放+辅助合并）。

责任契约（fn_docs/hybrid/responsibility.md【R22 增补】）：
卖流库构建 v2——输入改 top-30 新鲜回放（旧 86 局库降为辅助键合并）；键口径沿
v1（店对|m钱_w麦）；新增"历史命中率"字段（240 回合 ≥3 命中 ≥70% 置信门的
数据面）。

v2 输入口径：
  - 新鲜回放（replay_dir）：逐局解析后按时间序取最新 30 局建主库；语料 <30 局
    →ValueError（fail-closed）。时间序=replay 顶层/info 的 createTime 串
    （ISO 定长字典序）优先，缺该字段时以 episode id 序代（r37 线上 55 局实测
    id 序≡createTime 序，55→30 截取等价）。全部文件均解析（坏 JSON/结构缺失
    →ValueError，不静默跳过）后再截取。
  - 辅助库（旧 86 局回放）：env SELLFLOW_AUX_REPLAY_DIR 指定目录（未设置=
    /tmp/r33audit；置空串=无辅助库），按 v1 口径建库后与新库按键合并；辅助目录
    与 replay_dir 同路径时跳过合并（防自并双计）；辅助语料解析失败同样抛。
  合并口径（键=shop_pair_key||fingerprint_key，沿 v1）：同键 n_episodes/
  qty_sum/count 计数相加、qty_max 取 max；history_hits/hit_rate 以新库为主
  （新库缺省→合并条目缺省=旧库兼容形态，match v2 对缺字段条目按 v1 采纳）；
  global 条目同口径合并。

history_hits/hit_rate 计算口径（简单可测；字段命名/落位对齐 match_sellflow v2
的条目级读取：keys[<键>] 与 global 条目内 n_episodes/hist 旁）：
  对每个库条目的每个步窗桶 win=step//48，取该窗内 TOP-1 品目（qty_sum 最大，
  同量取品名字典序小者）预期量=均单量（qty_sum/count）；在该条目的样本回放
  （=条目 n_episodes 的局集合）中逐局统计"该窗该品实际对手卖出量落在预期
  ±50%（含界）内"：history_hits=命中（局×窗）样本对数，hit_rate=
  hits/样本对数（样本对数=局数×窗数）；样本对 ≥3 才置字段，否则字段缺省。
  命中字段只算新鲜回放样本（辅助库 v1 口径无字段，合并后仍以新库为主）。
  "240 回合 ≥3 命中 ≥70%"为 match_sellflow 侧消费门（history_hits≥3 且
  hit_rate≥0.70 才采纳远端信号），本件只负责数据面。

键口径（与并行的 match_sellflow 检索实现共同约定，不得偏离）：
  full_key = f"{shop_pair_key}||{fingerprint_key}"
  - shop_pair_key：事件发生步 observation.town.unlocked_shops[:2] 的字符串化。
      * >=2 店：<首店>|<第二店>，如 "BAKERY|YARN_STORE"（可重复名照拼）。
      * ==1 店（step<144 店未全开）："OPEN1:<首店>"。
      * ==0 店（step<144 店未全开）："EARLY"。
    （按 replay 内 town 观测逐步取"当时"首二店组合，故 step<144 自然落到
     OPEN1/EARLY 档，无需硬编码步号。）
  - fingerprint_key：step-2 拍（步下标 2）对手 (money, market.inventory.WHEAT)
    量化串 "m<money>_w<wheat>"（money/wheat 各取整）；replay 步数 <3 时以
    step0 观测替代（头拍回退）。money 取自对手席 farms[opponent_seat].money，
    wheat 取自共享 market.inventory.WHEAT。

对手席：info.TeamNames 判定，"我方席=renyxin" 之外的席位为对手（对手是相对
概念，逐局定席；renyxin 可在 0/1 任一席）。SELL 事件=对手 action.market 中
["SELL",item,qty] 单（空槽 [] 跳过）。步窗 win=str(step//48)（719 步→15 窗）。

n_episodes 语义：library["global"].n_episodes=n_used（新鲜覆盖局数，合并后含
辅助局数）；每个 key 的 n_episodes=该 key 下至少贡献 1 单 SELL 的对局数（跨局
去重；合并=新旧计数相加）。

fail-closed：语料缺失（目录缺失/无 replay 文件）抛 FileNotFoundError；
新鲜语料 <30 局抛 ValueError；解析失败（坏 JSON / 缺 TeamNames|steps / SELL
单畸形 / 指纹字段缺失）抛 ValueError。无 renyxin 席的对局不算解析失败：跳过
并计入 n_skipped（辅助语料计 n_aux_skipped）。
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
from typing import Any, Dict, List, Set, Tuple

# replay 文件名两种形态都收：episode-<id>.replay.json / episode-<id>-replay.json
_REPLAY_NAME = re.compile(r"^episode-.*(?:\.replay\.json|-replay\.json)$")
_FINGERPRINT_STEP = 2  # step-2 拍（下标 2）；replay 步数 <3 时回退 step0
_WINDOW = 48  # 步窗=step//48（半天窗）
_MIN_CORPUS = 30  # 新鲜语料下限（<30 局 fail-closed）
_TOP_N = 30  # 按时间序取最新 30 局建主库
_AUX_ENV = "SELLFLOW_AUX_REPLAY_DIR"  # 辅助库目录（未设=/tmp/r33audit；空串=无）
_AUX_DEFAULT = "/tmp/r33audit"
_HITS_MIN_SAMPLES = 3  # 样本对 ≥3 才置 history_hits/hit_rate
_HITS_BAND = 0.5  # 预期 ±50%（含界）内算命中
_VERSION = "sellflow/2.0"


def _discover(replay_dir: str) -> List[str]:
    """枚举 replay 语料；目录缺失/无文件→fail-closed 抛。"""
    if not os.path.isdir(replay_dir):
        raise FileNotFoundError(f"sellflow: replay_dir 不存在: {replay_dir}")
    names = [
        os.path.join(replay_dir, n)
        for n in os.listdir(replay_dir)
        if _REPLAY_NAME.match(n)
    ]
    files = sorted(names)
    if not files:
        raise FileNotFoundError(f"sellflow: 未发现 replay 语料: {replay_dir}")
    return files


def _episode_id(path: str, data: Dict[str, Any]) -> int:
    """episode id（info.EpisodeId 优先，缺省取文件名首段数字）。"""
    info = data.get("info") or {}
    ep = info.get("EpisodeId")
    if isinstance(ep, int):
        return ep
    m = re.search(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def _time_key(path: str, data: Dict[str, Any]) -> Tuple[int, str, int]:
    """时间序键（升序=由旧到新，取末 30=最新 30）。

    createTime（顶层或 info，ISO 定长串字典序）优先；缺该字段以 episode id 序
    代（r37 语料实测 id 序≡createTime 序）。两种形态混杂时带 createTime 者
    排后（视为更新）。
    """
    info = data.get("info") or {}
    ct = data.get("createTime")
    if not isinstance(ct, str) or not ct:
        ct = info.get("createTime")
    ep = _episode_id(path, data)
    if isinstance(ct, str) and ct:
        return (1, ct, ep)
    return (0, "", ep)


def _shop_pair_key(unlocked: List[str]) -> str:
    """unlocked_shops[:2] → shop_pair_key（0/1 店→EARLY/OPEN1 档）。"""
    if len(unlocked) >= 2:
        return f"{unlocked[0]}|{unlocked[1]}"
    if len(unlocked) == 1:
        return f"OPEN1:{unlocked[0]}"
    return "EARLY"


def _bump(hist: Dict[str, Any], win: str, item: str, qty: int) -> None:
    """直方桶累加：qty_sum/count/qty_max。"""
    bucket = (
        hist.setdefault(win, {})
        .setdefault(item, {"qty_sum": 0, "count": 0, "qty_max": 0})
    )
    bucket["qty_sum"] += qty
    bucket["count"] += 1
    if qty > bucket["qty_max"]:
        bucket["qty_max"] = qty


def _parse_replay(path: str) -> Dict[str, Any]:
    """读单局 replay → 顶层 dict；坏 JSON/结构缺失→fail-closed 抛。"""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"sellflow: 解析失败 {os.path.basename(path)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"sellflow: 解析失败 {os.path.basename(path)}: 非对象")
    info = data.get("info")
    if not isinstance(info, dict) or not isinstance(info.get("TeamNames"), list):
        raise ValueError(f"sellflow: 解析失败 {os.path.basename(path)}: 缺 info.TeamNames")
    if not isinstance(data.get("steps"), list) or not data["steps"]:
        raise ValueError(f"sellflow: 解析失败 {os.path.basename(path)}: 缺/空 steps")
    return data


def _read_fingerprint_at(steps: List[Any], fp_step: int, opp_seat: int) -> str:
    """单拍读 (money, WHEAT) → 指纹串；字段缺失→抛（供回退链用）。"""
    obs = steps[fp_step][opp_seat]["observation"]
    money = obs["farms"][opp_seat]["money"]
    wheat = obs["market"]["inventory"]["WHEAT"]
    return f"m{int(round(float(money)))}_w{int(round(float(wheat)))}"


def _fingerprint_key(steps: List[Any], opp_seat: int) -> str:
    """step-2 拍（回退 step0）对手 (money, WHEAT inv) → 量化指纹串。

    step-2（下标 2）优先；该拍不可用（步数不足/字段缺失）时以 step0 头拍观测
    替代；两拍都不可用→fail-closed 抛。
    """
    candidates = []
    if len(steps) > _FINGERPRINT_STEP:
        candidates.append(_FINGERPRINT_STEP)
    candidates.append(0)
    last_exc: Exception | None = None
    for fp_step in candidates:
        try:
            return _read_fingerprint_at(steps, fp_step, opp_seat)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            last_exc = exc
    raise ValueError(f"sellflow: 指纹字段缺失: {last_exc}") from last_exc


def _extract_sells(steps: List[Any], opp_seats: List[int]) -> List[Tuple[int, str, int, str]]:
    """对手 SELL 单 → [(step, item, qty, shop_pair_key), ...]。

    空槽/非 SELL 单跳过；player/action/observation 为 null（局末无动作等合法态）
    时按无单处理，不视为解析失败。SELL 单畸形（<3 元/量非数）→fail-closed 抛。
    """
    events: List[Tuple[int, str, int, str]] = []
    for i, step in enumerate(steps):
        if not isinstance(step, (list, tuple)):
            continue
        for seat in opp_seats:
            if seat >= len(step):
                continue
            player = step[seat]
            if not isinstance(player, dict):
                continue  # null 席位：无动作可提
            action = player.get("action") or {}
            obs = player.get("observation") or {}
            orders = action.get("market") or []
            if not isinstance(orders, list):
                orders = []
            unlocked = (obs.get("town") or {}).get("unlocked_shops") or []
            sp_key = _shop_pair_key([str(u) for u in unlocked])
            for order in orders:
                if not order:  # 空槽跳过
                    continue
                if not isinstance(order, list):
                    raise ValueError(f"sellflow: SELL/单畸形 @step{i} seat{seat}: {order!r}")
                if order[0] == "SELL":
                    if len(order) < 3:
                        raise ValueError(f"sellflow: SELL 单畸形 @step{i} seat{seat}: {order!r}")
                    try:
                        qty = int(round(float(order[2])))
                    except (TypeError, ValueError) as exc:
                        raise ValueError(f"sellflow: SELL 量非法 @step{i}: {order!r}") from exc
                    events.append((i, str(order[1]), qty, sp_key))
    return events


def _aggregate(pairs: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
    """多局 replay（v1 口径）→ 原始聚合：键直方+局集合+（局×窗×品）实际量。

    返回 {"key_eps","key_hist","key_epwi","global_eps","global_hist",
    "global_epwi","n_used","n_skipped","total_events"}；epwi=每局每窗每品实际
    对手卖出量（history_hits 数据面）。
    """
    key_eps: Dict[str, Set[int]] = {}
    key_hist: Dict[str, Dict[str, Any]] = {}
    key_epwi: Dict[str, Dict[str, Dict[str, Dict[int, int]]]] = {}
    global_eps: Set[int] = set()
    global_hist: Dict[str, Any] = {}
    global_epwi: Dict[str, Dict[str, Dict[str, Dict[int, int]]]] = {}
    n_used = 0
    n_skipped = 0
    total_events = 0

    for ep_idx, (_path, data) in enumerate(pairs):
        team_names = data["info"]["TeamNames"]
        # 对手席=非 renyxin 席（相对概念，逐局定席）。
        renyxin_seats = [i for i, nm in enumerate(team_names) if nm == "renyxin"]
        opp_seats = [i for i, nm in enumerate(team_names) if nm != "renyxin"]
        if not renyxin_seats or not opp_seats:
            # 无 renyxin 席→跳过该局并计数留档（非解析失败）。
            n_skipped += 1
            continue

        steps = data["steps"]
        fp_key = _fingerprint_key(steps, opp_seats[0])
        events = _extract_sells(steps, opp_seats)

        seen_keys: Set[str] = set()
        for (step_i, item, qty, sp_key) in events:
            full_key = f"{sp_key}||{fp_key}"
            win = str(step_i // _WINDOW)
            _bump(key_hist.setdefault(full_key, {}), win, item, qty)
            _bump(global_hist, win, item, qty)
            for epwi in (
                key_epwi.setdefault(full_key, {}).setdefault(win, {}).setdefault(item, {}),
                global_epwi.setdefault(win, {}).setdefault(item, {}),
            ):
                epwi[ep_idx] = epwi.get(ep_idx, 0) + qty
            seen_keys.add(full_key)
            total_events += 1
        for full_key in seen_keys:
            key_eps.setdefault(full_key, set()).add(ep_idx)
        global_eps.add(ep_idx)  # global 样本=覆盖局集合（对齐其 n_episodes）
        n_used += 1

    return {
        "key_eps": key_eps,
        "key_hist": key_hist,
        "key_epwi": key_epwi,
        "global_eps": global_eps,
        "global_hist": global_hist,
        "global_epwi": global_epwi,
        "n_used": n_used,
        "n_skipped": n_skipped,
        "total_events": total_events,
    }


def _hit_stats(
    hist: Dict[str, Any],
    eps: Set[int],
    epwi: Dict[str, Dict[str, Dict[str, Dict[int, int]]]],
) -> Tuple[int, int]:
    """条目级历史命中：(history_hits, 样本对数)。

    每窗 TOP-1 品目（qty_sum 最大，同量取品名字典序小者）预期=均单量；
    逐局实际量（该窗该品，缺省 0）落在预期 ±50%（含界）内记命中；样本对=
    局数×窗数。
    """
    hits = 0
    samples = 0
    for win in sorted(hist):
        bucket = hist[win]
        if not bucket:
            continue
        top_item = sorted(bucket, key=lambda it: (-bucket[it]["qty_sum"], it))[0]
        rec = bucket[top_item]
        expected = rec["qty_sum"] / rec["count"] if rec["count"] else 0.0
        band = _HITS_BAND * expected + 1e-9  # 含界（±50%）
        per_item = (epwi.get(win) or {}).get(top_item) or {}
        for ep in eps:
            actual = per_item.get(ep, 0)
            samples += 1
            if abs(actual - expected) <= band:
                hits += 1
    return hits, samples


def _make_entry(
    n_episodes: int,
    hist: Dict[str, Any],
    eps: Set[int],
    epwi: Dict[str, Dict[str, Dict[str, Dict[int, int]]]],
    with_hits: bool,
) -> Dict[str, Any]:
    """条目形 {"n_episodes","hist"[,"history_hits","hit_rate"]}。

    with_hits=False（辅助库 v1 口径）不置命中字段；样本对 <3 不置字段=旧库
    兼容形态。
    """
    entry: Dict[str, Any] = {"n_episodes": n_episodes, "hist": hist}
    if with_hits:
        hits, samples = _hit_stats(hist, eps, epwi)
        if samples >= _HITS_MIN_SAMPLES:
            entry["history_hits"] = hits
            entry["hit_rate"] = hits / samples
    return entry


def _merge_hist(h_new: Dict[str, Any], h_old: Dict[str, Any]) -> Dict[str, Any]:
    """直方按键合并：qty_sum/count 相加、qty_max 取 max。"""
    out: Dict[str, Any] = {w: {i: dict(b) for i, b in items.items()}
                           for w, items in h_new.items()}
    for win, items in h_old.items():
        for item, rec in items.items():
            bucket = out.setdefault(win, {}).setdefault(
                item, {"qty_sum": 0, "count": 0, "qty_max": 0}
            )
            bucket["qty_sum"] += rec["qty_sum"]
            bucket["count"] += rec["count"]
            bucket["qty_max"] = max(bucket["qty_max"], rec["qty_max"])
    return out


def _merge_entries(new_e: Dict[str, Any], old_e: Dict[str, Any]) -> Dict[str, Any]:
    """新旧条目按键合并：同键计数相加、命中字段以新库为主（新库缺省→缺省）。"""
    out: Dict[str, Any] = {}
    for key in sorted(set(new_e) | set(old_e)):
        n_rec, o_rec = new_e.get(key), old_e.get(key)
        if n_rec is not None and o_rec is not None:
            rec: Dict[str, Any] = {
                "n_episodes": n_rec["n_episodes"] + o_rec["n_episodes"],
                "hist": _merge_hist(n_rec["hist"], o_rec["hist"]),
            }
            if "history_hits" in n_rec:
                rec["history_hits"] = n_rec["history_hits"]
                rec["hit_rate"] = n_rec["hit_rate"]
        elif n_rec is not None:
            rec = n_rec
        else:
            rec = o_rec
        out[key] = rec
    return out


def build_sellflow_library(replay_dir: str, labels: Any = None) -> Dict[str, Any]:
    """top-30 新鲜回放+辅助旧库 → 对手卖流分布库（v2）+构建审计。

    签名意图：输入: 新回放目录+辅助库（env SELLFLOW_AUX_REPLAY_DIR，默认
    /tmp/r33audit）+分层标签 / 输出: {library, build_audit} /
    错误: 语料 <30 局→ValueError，解析失败→ValueError，语料缺失→
    FileNotFoundError（fail-closed）。

    返回结构（与 match_sellflow v2 共同约定，不得偏离）：
      library = {
        "version": "sellflow/2.0",
        "keys": {"<shop_pair_key>||<fingerprint_key>":
                   {"n_episodes": int,
                    "hist": {"<win>": {"<ITEM>":
                                {"qty_sum": int, "count": int, "qty_max": int}}},
                    "history_hits": int, "hit_rate": float}},  # 样本对≥3 才有
        "global": {"n_episodes": int, "hist": {同上}, ...同可选命中字段},
      }
      build_audit = {"replay_dir", "n_files", "n_selected", "n_used",
                     "n_skipped", "total_events", "aux_replay_dir",
                     "n_aux_files", "n_aux_used", "n_aux_skipped",
                     "n_aux_events", "sha256_of_library"}（labels 非空时附
                     "labels" 注记）。total_events=n_aux_events=各自语料事件数
                     （global 直方 count 总和=两者之和）。
    """
    files = _discover(replay_dir)
    if len(files) < _MIN_CORPUS:
        raise ValueError(
            f"sellflow: 语料 <30 局: {len(files)} < {_MIN_CORPUS} ({replay_dir})"
        )

    # 全量解析（fail-closed）→ 时间序升序 → 取最新 30 局建主库。
    parsed = []
    for path in files:
        data = _parse_replay(path)
        parsed.append((_time_key(path, data), path, data))
    parsed.sort(key=lambda t: t[0])
    selected = parsed[-_TOP_N:]
    fresh = _aggregate([(p, d) for (_k, p, d) in selected])

    # 主库条目（含命中字段；样本对 <3 缺省=旧库兼容形态）。
    fresh_entries: Dict[str, Any] = {
        key: _make_entry(
            len(fresh["key_eps"].get(key, ())),
            fresh["key_hist"][key],
            fresh["key_eps"].get(key, set()),
            fresh["key_epwi"].get(key, {}),
            with_hits=True,
        )
        for key in sorted(fresh["key_hist"])
    }
    fresh_entries["global"] = _make_entry(
        fresh["n_used"],
        fresh["global_hist"],
        fresh["global_eps"],
        fresh["global_epwi"],
        with_hits=True,
    )

    # 辅助库（旧 86 局）：v1 口径建库→按键合并；同路径防自并双计。
    aux_dir = os.environ.get(_AUX_ENV, _AUX_DEFAULT)
    if aux_dir == "":
        aux_dir = None
    n_aux_files = n_aux_used = n_aux_skipped = n_aux_events = 0
    aux_entries: Dict[str, Any] = {}
    if (
        aux_dir
        and os.path.isdir(aux_dir)
        and os.path.realpath(aux_dir) != os.path.realpath(replay_dir)
    ):
        aux_files = [
            os.path.join(aux_dir, n)
            for n in sorted(os.listdir(aux_dir))
            if _REPLAY_NAME.match(n)
        ]
        if aux_files:
            aux = _aggregate([(p, _parse_replay(p)) for p in aux_files])
            n_aux_files = len(aux_files)
            n_aux_used = aux["n_used"]
            n_aux_skipped = aux["n_skipped"]
            n_aux_events = aux["total_events"]
            aux_entries = {
                key: _make_entry(
                    len(aux["key_eps"].get(key, ())),
                    aux["key_hist"][key],
                    aux["key_eps"].get(key, set()),
                    aux["key_epwi"].get(key, {}),
                    with_hits=False,
                )
                for key in sorted(aux["key_hist"])
            }
            aux_entries["global"] = _make_entry(
                aux["n_used"],
                aux["global_hist"],
                aux["global_eps"],
                aux["global_epwi"],
                with_hits=False,
            )

    merged = _merge_entries(fresh_entries, aux_entries)
    library = {
        "version": _VERSION,
        "keys": {k: merged[k] for k in sorted(merged) if k != "global"},
        "global": merged.get("global") or dict(fresh_entries["global"]),
    }

    lib_json = json.dumps(library, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False)  # 与 pack AST 重算口径统一（评审 P3）
    sha256 = hashlib.sha256(lib_json.encode("utf-8")).hexdigest()

    build_audit: Dict[str, Any] = {
        "replay_dir": replay_dir,
        "n_files": len(files),
        "n_selected": len(selected),
        "n_used": fresh["n_used"],
        "n_skipped": fresh["n_skipped"],
        "total_events": fresh["total_events"],
        "aux_replay_dir": aux_dir,
        "n_aux_files": n_aux_files,
        "n_aux_used": n_aux_used,
        "n_aux_skipped": n_aux_skipped,
        "n_aux_events": n_aux_events,
        "sha256_of_library": sha256,
    }
    if labels is not None:
        # analysis20/22 分层标签作注记（不入 sha）。
        build_audit["labels"] = labels

    return {"library": library, "build_audit": build_audit}
