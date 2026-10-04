# -*- coding: utf-8 -*-
"""corpus —— R14 语料选择（共享件）。

corpus_select：
  - Phase A：回放目录全量（episode-<id>-replay.json 按局号升序）；
  - Phase B：Phase A 检出的"含可处置 surge 日"败局全集 + 8 抽样胜局
    （r32/r33 胜局池各 4，rng 种子材料串 "20260924r14"——非纯数字，取
    sha256 前 16 hex 转 int 作 random.Random 种子，推导过程入 evidence）。

局集归属：/tmp/kagr_root（回退 /tmp/r33audit）episodes-<tag>-<ref>.json 内
type 含 PUBLIC 的 id → tag（audit_r32r33.py 同口径）。
缺回放的局 = fail-closed 列出（errors 面），不静默放过。
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import random
import re

TEAM_NAME = "renyxin"

REPLAY_RE = re.compile(r"episode-(\d+)-replay\.json$")

# 提交轮次元数据（id→tag）：r32/r33 为 Phase B 胜局抽样池标签，r30/r31 仅标注。
META_SOURCES = (
    ("/tmp/kagr_root", "episodes-r32-56517593.json", "r32"),
    ("/tmp/r33audit", "episodes-r32-56517593.json", "r32"),
    ("/tmp/kagr_root", "episodes-r33-56517991.json", "r33"),
    ("/tmp/r33audit", "episodes-r33-56517991.json", "r33"),
    ("/tmp/r33audit", "episodes-r30-56491673.json", "r30"),
    ("/tmp/r33audit", "episodes-r31-56508268.json", "r31"),
)

# 胜局抽样种子材料（需求原文 rng=random.Random(20260924r14)——材料串非整数，
# 推导：int(sha256("20260924r14").hexdigest()[:16], 16)）。
WIN_SAMPLE_SEED_MATERIAL = "20260924r14"

DEFAULT_REPLAY_DIR = "/tmp/r33audit"


def win_sample_seed(material: str = WIN_SAMPLE_SEED_MATERIAL) -> int:
    """材料串 → 可复现整数种子（推导入 evidence.source.sampling）。"""
    return int(hashlib.sha256(material.encode("utf-8")).hexdigest()[:16], 16)


def discover_replays(replay_dir):
    """回放目录 → [(episode_id:int, abs_path)] 按局号升序；非目录抛 OSError。"""
    path = os.path.abspath(replay_dir)
    if not os.path.isdir(path):
        raise NotADirectoryError(f"replay_dir 不是目录: {path}")
    found = []
    for fp in glob.glob(os.path.join(path, "episode-*-replay.json")):
        m = REPLAY_RE.search(os.path.basename(fp))
        if m:
            found.append((int(m.group(1)), os.path.abspath(fp)))
    found.sort(key=lambda x: x[0])
    return found


def load_replay(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def game_label(replay, tag_map=None):
    """回放头 → {episode, seat, opp, res, margin, tag}（不触 steps，供轻量标注）。

    res：W/L/T 按 rewards 双席比较（renyxin 视角）；renyxin 不在 TeamNames
    → error 键（fail-closed 由调用方处置）。
    """
    info = replay.get("info") or {}
    names = info.get("TeamNames") or replay.get("teams") or []
    episode = info.get("EpisodeId") or replay.get("episode_id")
    out = {"episode": episode, "tag": None, "seat": None, "opp": None,
           "res": None, "margin": None, "error": None}
    if isinstance(tag_map, dict) and episode in tag_map:
        out["tag"] = tag_map[episode]
    if TEAM_NAME not in names:
        out["error"] = f"{TEAM_NAME} not in TeamNames {names!r}"
        return out
    seat = names.index(TEAM_NAME)
    rewards = replay.get("rewards") or []
    if len(rewards) != 2 or rewards[0] is None or rewards[1] is None:
        out["error"] = f"rewards 异常: {rewards!r}"
        return out
    ours, theirs = rewards[seat], rewards[1 - seat]
    out.update({
        "seat": seat,
        "opp": names[1 - seat],
        "res": "W" if ours > theirs else ("L" if ours < theirs else "T"),
        "margin": round(float(ours) - float(theirs), 1),
    })
    return out


def load_tag_map():
    """提交轮次 id→tag（PUBLIC only）；文件缺失跳过该源（标注面非判据面）。"""
    tag_map = {}
    for base, name, tag in META_SOURCES:
        fp = os.path.join(base, name)
        if not os.path.isfile(fp):
            continue
        try:
            with open(fp, "r", encoding="utf-8") as fh:
                rows = json.load(fh)
        except (OSError, ValueError):
            continue
        for e in rows or []:
            if isinstance(e, dict) and "PUBLIC" in str(e.get("type", "")):
                tag_map[int(e["id"])] = tag
    return tag_map


def sample_wins(win_pools, n_per_tag=4, material=WIN_SAMPLE_SEED_MATERIAL):
    """r32/r33 胜局池各抽 n_per_tag 局（种子推导可复现，过程记录返回）。"""
    rng = random.Random(win_sample_seed(material))
    sampled, note = {}, {"seed_material": material,
                         "seed_derivation": 'int(sha256(material).hexdigest()[:16], 16)',
                         "per_tag": {}}
    for tag in ("r32", "r33"):
        pool = sorted(win_pools.get(tag, []))
        take = min(n_per_tag, len(pool))
        picked = rng.sample(pool, take) if take else []
        sampled[tag] = picked
        note["per_tag"][tag] = {"pool": pool, "picked": picked}
    return sampled, note


def corpus_select(replay_dir, phase_a_report=None, n_wins_per_tag=4):
    """语料选择（Phase A 全量 / Phase B 可处置败局全集+抽样胜局）。

    输入：回放目录；Phase B 时给 phase_a_report（phase_a_attribution 产物，
    含逐局 res/treatable 标注）。输出：
      {phase_a: [entry], phase_b: None|{losses, wins}, sampling, errors}
    entry = {episode, path, tag?, seat?, opp?, res?, margin?, treatable?,
    error?}——Phase A 无报告时为轻量清单（episode/path/tag；标签由
    phase_a_attribution 装载时补全，避免整语料二次读盘）。
    Phase B 缺回放 / Phase A 报告缺失 → errors 列出（fail-closed）。
    """
    replay_dir = os.path.abspath(replay_dir)
    errors = []
    found = discover_replays(replay_dir)
    tag_map = load_tag_map()

    phase_a, labels = [], {}
    if phase_a_report:
        labels = {g.get("episode"): g
                  for g in phase_a_report.get("per_game", [])}
    for ep, path in found:
        entry = {"episode": ep, "path": path}
        src = labels.get(ep)
        if src is not None:
            entry.update({k: src.get(k) for k in
                          ("tag", "seat", "opp", "res", "margin", "error",
                           "treatable", "treatable_surge_days", "surge_days")})
            entry["tag"] = entry["tag"] or tag_map.get(ep)
        else:
            entry["tag"] = tag_map.get(ep)
        phase_a.append(entry)

    phase_b, sampling = None, None
    if phase_a_report is not None:
        losses, win_pools = [], {"r32": [], "r33": []}
        for entry in phase_a:
            if entry.get("error"):
                errors.append({"episode": entry["episode"],
                               "error": f"phase_a 解析失败: {entry['error']}"})
                continue
            if entry.get("res") == "L" and entry.get("treatable"):
                losses.append(entry)
            elif entry.get("res") == "W":
                win_pools.setdefault(entry.get("tag"), []).append(entry["episode"])
        sampled, sampling = sample_wins(win_pools, n_wins_per_tag)
        win_eps = sorted(sampled.get("r32", []) + sampled.get("r33", []))
        by_ep = {e["episode"]: e for e in phase_a}
        wins = []
        for ep in win_eps:
            if ep not in by_ep:
                errors.append({"episode": ep, "error": "胜局抽样缺回放件"})
                continue
            wins.append(by_ep[ep])
        phase_b = {"losses": losses, "wins": wins}
    return {"phase_a": phase_a, "phase_b": phase_b, "sampling": sampling,
            "errors": errors}
