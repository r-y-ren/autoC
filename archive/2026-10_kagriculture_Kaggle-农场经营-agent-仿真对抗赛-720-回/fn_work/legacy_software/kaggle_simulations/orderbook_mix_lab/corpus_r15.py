# -*- coding: utf-8 -*-
"""corpus_r15 —— R15 语料选择器（共享件：编排/开环/闭环共用）。

口径（需求 R15 钉死）：
  - losses26：29 败局排 3 早崩（112844424/112846785/112847952，margin_d10
    判定的早崩局，−21k~−24k 产线差距非 mix 可救）；
  - wins10：r32/r33 胜局池各 5，rng=random.Random(20260925r15)（材料串经
    sha256 前 16 hex 转 int，R14 同款推导，过程入 sampling 记录）；
  - mirror：r33 败局/平局池（|margin|<400 且资金差<2%[|ourF−oppF|/max]）
    独立抽样 5 局（同种子材料，独立 Random 实例）；池不足 5 时取全池并在
    sampling.note 记录（不静默）。
  - 缺回放 = fail-closed 列出（errors 面），不静默放过。

标注源：audit_rows.json（战役根）优先（margin/ourF/oppF/tag/res）；
缺失时回退回放头标注（R14 corpus.game_label），mirror 池资金差判据在
回退面退化为 |margin|<400 单判据（记录于 sampling.fallback_note）。
"""
from __future__ import annotations

import json
import os
import random

from . import _base as B
from orderbook_surge_lab import corpus as _surge_corpus


def _load_audit_rows(audit_rows):
    """audit_rows 输入 → dict（路径或已载 dict；None 走默认路径，缺文件=None）。"""
    if audit_rows is None:
        audit_rows = B.DEFAULT_AUDIT_ROWS
    if isinstance(audit_rows, dict):
        return audit_rows
    if isinstance(audit_rows, str) and os.path.isfile(audit_rows):
        with open(audit_rows, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return None


def _fund_gap(row):
    """资金差 = |ourF−oppF| / max(ourF, oppF)（1e-9 护底）。缺数 → None。"""
    try:
        our, opp = float(row["ourF"]), float(row["oppF"])
    except (KeyError, TypeError, ValueError):
        return None
    if our <= 0 and opp <= 0:
        return None
    return abs(our - opp) / max(our, opp, 1e-9)


def select_corpus_r15(replay_dir, audit_rows=None):
    """R15 语料选择（详见模块头）。输出：
      {losses26, wins10, mirror, sampling, errors}——entry 含
    episode/path/tag/seat/opp/res/margin；缺回放进 errors（fail-closed 面）。
    """
    rows = _load_audit_rows(audit_rows)
    found = _surge_corpus.discover_replays(replay_dir)
    by_ep_path = {ep: path for ep, path in found}
    tag_map = _surge_corpus.load_tag_map()

    labels = {}
    if rows:
        for g in rows.get("games", []):
            labels[int(g["episode"])] = g
    used_audit = bool(labels)

    def _entry(ep):
        row = labels.get(ep) or {}
        return {
            "episode": ep,
            "path": by_ep_path.get(ep),
            "tag": row.get("tag") or tag_map.get(ep),
            "seat": row.get("seat"),
            "opp": row.get("opp"),
            "res": row.get("res"),
            "margin": row.get("margin"),
            "ourF": row.get("ourF"),   # mirror 资金差判据（audit 面）
            "oppF": row.get("oppF"),
        }

    # ---- 全量局集（audit 优先；缺 audit 的局用回放头补标注） ---------------
    eps = sorted(set(by_ep_path) | set(labels))
    labeled = []
    for ep in eps:
        entry = _entry(ep)
        if entry["res"] is None and entry["path"]:
            lab = _surge_corpus.game_label(
                _surge_corpus.load_replay(entry["path"]), tag_map)
            if lab.get("error") is None:
                entry.update({k: lab[k] for k in
                              ("seat", "opp", "res", "margin", "tag")})
        labeled.append(entry)

    errors = [{"episode": e["episode"], "error": "缺回放件"}
              for e in labeled if not e["path"]]

    # ---- losses26 ----------------------------------------------------------
    losses26 = [e for e in labeled
                if e.get("res") == "L" and e["episode"] not in B.EARLY_CRASH
                and e["path"]]
    losses26.sort(key=lambda e: e["episode"])

    # ---- wins10（r32/r33 胜局池各 5，rng 材料 20260925r15） -----------------
    win_pools = {"r32": sorted(e["episode"] for e in labeled
                               if e.get("res") == "W" and e.get("tag") == "r32"
                               and e["path"]),
                 "r33": sorted(e["episode"] for e in labeled
                               if e.get("res") == "W" and e.get("tag") == "r33"
                               and e["path"])}
    rng_wins = random.Random(B.rng_seed())
    picked_wins = {}
    for tag in ("r32", "r33"):
        pool = win_pools[tag]
        picked_wins[tag] = rng_wins.sample(pool, min(5, len(pool)))
    win_eps = sorted(picked_wins["r32"] + picked_wins["r33"])
    by_ep = {e["episode"]: e for e in labeled}
    wins10 = [by_ep[ep] for ep in win_eps]

    # ---- mirror 近亲池（r33 败局/平局 |margin|<400 且资金差<2%，独立抽样） ----
    mirror_pool = []
    for e in labeled:
        if e.get("tag") != "r33" or e.get("res") not in ("L", "T") or not e["path"]:
            continue
        if e.get("margin") is None or abs(float(e["margin"])) >= B.MIRROR_MARGIN_MAX:
            continue
        gap = _fund_gap(e)
        if used_audit and gap is None:
            continue
        if gap is not None and gap >= B.MIRROR_FUND_GAP_MAX:
            continue
        mirror_pool.append(e["episode"])
    mirror_pool.sort()
    rng_mirror = random.Random(B.rng_seed())          # 独立抽样（同种子材料）
    mirror_take = min(5, len(mirror_pool))
    mirror_eps = rng_mirror.sample(mirror_pool, mirror_take) if mirror_take else []
    mirror = [by_ep[ep] for ep in sorted(mirror_eps)]

    sampling = {
        "seed_material": B.RNG_MATERIAL,
        "seed_derivation": "int(sha256(material).hexdigest()[:16], 16)",
        "win_pools": win_pools,
        "picked_wins": picked_wins,
        "mirror_pool": mirror_pool,
        "picked_mirror": sorted(mirror_eps),
        "mirror_criteria": {"tag": "r33", "res_in": ["L", "T"],
                            "abs_margin_lt": B.MIRROR_MARGIN_MAX,
                            "fund_gap_lt": B.MIRROR_FUND_GAP_MAX,
                            "fund_gap_def": "|ourF-oppF|/max(ourF,oppF)"},
        "note": None,
        "fallback_note": None if used_audit else
            "audit_rows 缺失：标注回退回放头，mirror 资金差判据退化（无 ourF/oppF）",
    }
    if len(mirror_pool) < 5:
        sampling["note"] = (f"mirror 近亲池仅 {len(mirror_pool)} 局（<5），"
                            f"取全池参与闭环副证")
    return {"losses26": losses26, "wins10": wins10, "mirror": mirror,
            "sampling": sampling, "errors": errors}
