# -*- coding: utf-8 -*-
"""build_sellflow_library（R21 L2）：对手卖流库构建。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
从 86 局逐动作 replay（/tmp/r33audit）提取对手 SELL 事件（步/品类/量），
聚合为按（首二店组合，step-2 身份指纹）键的分布库（步窗-品类-量直方）；
analysis20/22 分层标签作注记；输出可内嵌紧凑数据结构+构建审计（来源 sha/
覆盖局数）。

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

n_episodes 语义：library["global"].n_episodes=n_used（覆盖局数）；每个 key 的
n_episodes=该 key 下至少贡献 1 单 SELL 的对局数（跨局去重）。

fail-closed：语料缺失（目录缺失/无 replay 文件）抛 FileNotFoundError；
解析失败（坏 JSON / 缺 TeamNames|steps / SELL 单畸形 / 指纹字段缺失）抛
ValueError。无 renyxin 席的对局不算解析失败：跳过并计入 n_skipped。
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


def build_sellflow_library(replay_dir: str, labels: Any = None) -> Dict[str, Any]:
    """86 局逐动作 replay → 对手卖流分布库+构建审计。

    签名意图：输入: replay 目录+分层标签 / 输出: {library, build_audit} /
    错误: 语料缺失→FileNotFoundError，解析失败→ValueError（fail-closed）。

    返回结构（库与并行预测引擎共同约定，不得偏离）：
      library = {
        "version": "sellflow/1.0",
        "keys": {"<shop_pair_key>||<fingerprint_key>":
                   {"n_episodes": int,
                    "hist": {"<win>": {"<ITEM>":
                                {"qty_sum": int, "count": int, "qty_max": int}}}}},
        "global": {"n_episodes": int, "hist": {同上}},  # 无键回退
      }
      build_audit = {"replay_dir", "n_files", "n_used", "n_skipped",
                     "total_events", "sha256_of_library"}（labels 非空时附
                     "labels" 注记）。
    """
    files = _discover(replay_dir)

    # key -> {"eps": set(episode_idx), "hist": {...}}；global 无键聚合。
    key_eps: Dict[str, Set[int]] = {}
    key_hist: Dict[str, Dict[str, Any]] = {}
    global_hist: Dict[str, Any] = {}
    n_used = 0
    n_skipped = 0
    total_events = 0

    for ep_idx, path in enumerate(files):
        data = _parse_replay(path)
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
            hist = key_hist.setdefault(full_key, {})
            _bump(hist, win, item, qty)
            _bump(global_hist, win, item, qty)
            seen_keys.add(full_key)
            total_events += 1
        for full_key in seen_keys:
            key_eps.setdefault(full_key, set()).add(ep_idx)
        n_used += 1

    library = {
        "version": "sellflow/1.0",
        "keys": {
            full_key: {
                "n_episodes": len(key_eps.get(full_key, ())),
                "hist": key_hist[full_key],
            }
            for full_key in sorted(key_hist)
        },
        "global": {"n_episodes": n_used, "hist": global_hist},
    }

    lib_json = json.dumps(library, sort_keys=True, separators=(",", ":"))
    sha256 = hashlib.sha256(lib_json.encode("utf-8")).hexdigest()

    build_audit: Dict[str, Any] = {
        "replay_dir": replay_dir,
        "n_files": len(files),
        "n_used": n_used,
        "n_skipped": n_skipped,
        "total_events": total_events,
        "sha256_of_library": sha256,
    }
    if labels is not None:
        # analysis20/22 分层标签作注记（不入 sha）。
        build_audit["labels"] = labels

    return {"library": library, "build_audit": build_audit}
