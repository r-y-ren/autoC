# -*- coding: utf-8 -*-
"""adapters —— 两个数据入口 → EpisodeRecord 归一模型。

入口 A（全量）：kaggle-environments 回放 blob（x-ray cell 6 同源格式：
blob["steps"][t][seat] = {"action":..., "observation":...}，blob["info"]["TeamNames"]）。
  关键陷阱（x-ray cell 40）：**拍 t 的动作存 steps[t+1]**，抽流必须 +1 对齐；
  棋盘/钱/价逐拍累计取自 steps[t][0]["observation"]（cell 6 口径）。
入口 B（片段）：ext/fingerprint-scan/band-analysis/feats-band.jsonl 行
（day0_24=[farmer_tokens, market_tokens]，hands 通道缺失、数量已桶化）。
  仅够 day0（t<24）判读；t<48 在可观测盲区内，亲缘/语言类判读必须带盲区声明。

compact JSONL 缓存：replay_to_record 的产物（~60-90KB/局），可入 samples/ 重放。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

from orderbook_p4up_lab.records import EpisodeRecord, PASS_ACTION, new_grid

N_TURNS = 719  # x-ray cell 6：stream 长 719（t=0..718，动作取 steps[t+1]）


def _seat(step, s: int) -> dict:
    """steps[t] 的 s 座席条目：真实回放是按席位索引的 list，兼容 dict 形。"""
    if isinstance(step, list):
        return step[s] if 0 <= s < len(step) else {}
    if isinstance(step, dict):
        return step.get(s) or step.get(str(s)) or {}
    return {}


def _obs_of(step) -> dict:
    return _seat(step, 0).get("observation") or {}


def replay_to_record(blob: dict, episode: Any = None, seat: Optional[int] = None,
                     opp_sub: Optional[Any] = None, date: Optional[str] = None,
                     n_turns: int = N_TURNS) -> EpisodeRecord:
    """回放 blob → EpisodeRecord（全流 719 拍 + 价格/钱/棋盘层）。"""
    steps = blob.get("steps") or []
    info = blob.get("info") or {}
    names = list(info.get("TeamNames") or ["?", "?"])
    if seat is None:
        # 轮转座席：本适配器默认座 0 为 subject；调用方（按 submissionId）应显式传
        seat = 0
    opp_seat = 1 - seat

    stream = [(_seat(steps[t + 1], seat).get("action") if t + 1 < len(steps) else None) or PASS_ACTION
              for t in range(min(n_turns, max(0, len(steps) - 1)))]
    opp_stream = [(_seat(steps[t + 1], opp_seat).get("action") if t + 1 < len(steps) else None) or PASS_ACTION
                  for t in range(min(n_turns, max(0, len(steps) - 1)))]

    # 世界=前两店有序对（cell 6：steps[150] town.unlocked_shops[:2]）
    world = None
    if len(steps) > 150:
        town = _obs_of(steps[150]).get("town") or {}
        shops = list(town.get("unlocked_shops") or [])[:2]
        world = "__".join(shops) if len(shops) == 2 else None

    # 逐拍钱/价（cell 6：st[0].observation 的 farms/me 与 market.prices）
    money_me: List[float] = []
    money_op: List[float] = []
    prices_t: List[Dict[str, float]] = []
    for st in steps:
        o = _obs_of(st)
        farms = o.get("farms") or []
        money_me.append((farms[seat].get("money") or 0) if len(farms) > seat else 0)
        money_op.append((farms[opp_seat].get("money") or 0) if len(farms) > opp_seat else 0)
        prices_t.append(dict(((o.get("market") or {}).get("prices") or {})))

    # 棋盘层（cell 6：逐拍 tiles/位置累计）
    occ, pres, unlocked = new_grid(), new_grid(), new_grid()
    for st in steps:
        o = _obs_of(st)
        farms = o.get("farms") or []
        if len(farms) <= seat:
            continue
        farm = farms[seat]
        for yy, row in enumerate(farm.get("tiles") or []):
            for xx, cell in enumerate(row):
                if cell == "LOCKED":
                    continue
                if yy >= 10 or xx >= 10:
                    continue
                unlocked[yy][xx] += 1
                if isinstance(cell, dict):
                    occ[yy][xx] += 1
        for pos in ([farm.get("farmer")] + list(farm.get("hands") or [])):
            if isinstance(pos, (list, tuple)) and len(pos) == 2:
                px, py = int(pos[0]), int(pos[1])
                if 0 <= px < 10 and 0 <= py < 10:
                    pres[py][px] += 1

    # margin（cell 4：末步 reward 差；缺则 0 并注记）
    margin = 0.0
    lossy: List[str] = []
    if steps:
        last = steps[-1]
        rews = [_seat(last, s).get("reward") or 0 for s in (seat, opp_seat)]
        if any(rews):
            margin = float(rews[0]) - float(rews[1])
        else:
            lossy.append("末步 reward 缺失，margin 记 0")

    return EpisodeRecord(
        episode=episode if episode is not None else info.get("EpisodeId"),
        seat=seat, team=names[seat] if len(names) > seat else "?",
        opp=names[opp_seat] if len(names) > opp_seat else "?",
        margin=margin, stream=stream, opp_stream=opp_stream, world=world,
        opp_sub=opp_sub, date=date, seed=info.get("seed"),
        window=None, prices_t=prices_t, money_me=money_me, money_op=money_op,
        occ=occ, pres=pres, unlocked=unlocked, lossy_notes=lossy)


def _parse_feat_market_token(tok: str) -> Optional[List[Any]]:
    """'SELL:WOOL:2'→['SELL','WOOL','2']；'HIRE:-:-'→['HIRE']；占位 '-' 丢弃。"""
    if not isinstance(tok, str) or not tok:
        return None
    parts = tok.split(":")
    out = [parts[0]] + [p for p in parts[1:] if p and p != "-"]
    return out or None


def feats_row_to_records(row: dict) -> List[EpisodeRecord]:
    """feats-band 行 → 两条 day0 片段记录（两座席各一条 subject 视角）。

    day0_24[i] = [farmer_tokens, market_tokens]（band_extract.py 口径）：
    hands 通道未采集、数量已桶化不可逆、无价格/棋盘层。lossy_notes 全程声明。
    """
    lossy = [
        "feats-band 入口：hands 通道缺失（band_extract 只收 farmer+market token）",
        "数量已桶化（qty_bucket 不可逆），bundle/canon 比较只看品类与动词",
        "无价格/棋盘层：crater（C5）与热图闸（C6）不可判",
        "仅 day0（t<24）：t<48 在可观测盲区内（x-ray cell 16），亲缘读数必带盲区声明",
    ]
    players = row.get("players") or []
    if len(players) < 2:
        return []
    by_seat = {}
    for idx, p in enumerate(players):
        by_seat[p.get("pi", idx)] = p

    def stream_of(pi: int) -> List[Optional[dict]]:
        d0 = (by_seat.get(pi) or {}).get("day0_24") or []
        out_s = []
        for t in range(24):
            if t >= len(d0):
                out_s.append(PASS_ACTION)
                continue
            ft, mt = (list(d0[t]) + [[], []])[:2]
            market = [m for m in (_parse_feat_market_token(x) for x in (mt or [])) if m]
            out_s.append({"farmer": list(ft) or ["PASS"], "hands": [], "market": market})
        return out_s

    rewards = row.get("rewards") or [0, 0]
    out = []
    for pi in (0, 1):
        opp_pi = 1 - pi
        out.append(EpisodeRecord(
            episode=row.get("episode_id"), seat=pi,
            team=(by_seat.get(pi) or {}).get("team", "?"),
            opp=(by_seat.get(opp_pi) or {}).get("team", "?"),
            margin=float(rewards[pi] or 0) - float(rewards[opp_pi] or 0),
            stream=stream_of(pi), opp_stream=stream_of(opp_pi), world=None,
            date=row.get("date"), seed=row.get("seed"), window=24,
            lossy_notes=list(lossy)))
    return out


# ------------------------------------------------- compact JSONL（样本缓存）

def save_records_jsonl(records: Sequence[EpisodeRecord], path: str) -> str:
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r.to_compact(), ensure_ascii=False) + "\n")
    return path


def load_records_jsonl(path: str) -> List[EpisodeRecord]:
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(EpisodeRecord.from_compact(json.loads(line)))
    return out
