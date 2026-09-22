# -*- coding: utf-8 -*-
"""Track-C (BC) M0-2/M0-3: 样本抽取 + 克隆席过滤.

输入：
  - references/data/online-replays/bc-top/        （顶部选手局，主语料）
  - references/data/online-replays/round*/        （本机语料，高分对手席兜底）
输出（bc_track/data/，gitignored）：
  - samples/<source>-<eid>-s<seat>.json.gz   每席一份训练样本流
  - corpus_manifest.json                     语料台账（局/席/样本数/过滤量）

克隆席过滤（fresh-sweep/web-intel digest：公共 notebook 克隆潮，多队共享
逐字节相同开局）：
  - 开局签名 = 对该席 turns 1..51 的完整动作序列（farmer+hands+market）
    规范序列化的 sha256；
  - 同一签名被 >=3 个不同队伍共享 => 判"量产克隆家族"，非 top 队席剔除；
  - 另做全动作流签名去重（同队镜像局两席全同 => 只留一席）。

配对口径：(steps[t-1][seat].observation, steps[t][seat].action)，与
planner/twin.replay_transition_actions 同一解读。
"""
from __future__ import annotations

import argparse
import glob
import gzip
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bc_schema as S                                     # noqa: E402

SOFTWARE = Path(__file__).resolve().parents[2]
CAMPAIGN = SOFTWARE.parent
REPLAY_TOP = CAMPAIGN / "references" / "data" / "online-replays" / "bc-top"
REPLAY_ROUNDS = CAMPAIGN / "references" / "data" / "online-replays"
DATA = SOFTWARE / "bc_track" / "data" / "samples"
TOP_TEAMS_CSV = (CAMPAIGN / "references" / "data" / "lb-snapshot-20260920"
                 / "kaggriculture-publicleaderboard-2026-09-20T02_21_40.csv")
CLONE_FAMILY_MIN_TEAMS = 3
ROUND_MONEY_GATE = 80_000        # 本机语料兜底席的终局资金门（高分席）


def load_top_teams() -> dict[str, int]:
    import csv
    out = {}
    with open(TOP_TEAMS_CSV, "r", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            try:
                rank = int(row["Rank"])
            except (KeyError, ValueError):
                continue
            if 1 <= rank <= 30:
                out[row["TeamName"]] = rank
    return out


def seat_action_blob(action: dict) -> str:
    """动作 dict -> 规范序列化（签名用；无集合序依赖）。"""
    return json.dumps({"farmer": action.get("farmer"),
                       "hands": action.get("hands") or [],
                       "market": action.get("market") or []},
                      sort_keys=True, separators=(",", ":"))


def opening_signature(replay: dict, seat: int, turns: int = 51) -> str:
    h = hashlib.sha256()
    for t in range(1, min(turns + 1, len(replay["steps"]))):
        entry = replay["steps"][t][seat] or {}
        h.update(seat_action_blob(entry.get("action") or {}).encode())
    return h.hexdigest()[:16]


def full_signature(replay: dict, seat: int) -> str:
    h = hashlib.sha256()
    for t in range(1, len(replay["steps"])):
        entry = replay["steps"][t][seat] or {}
        h.update(seat_action_blob(entry.get("action") or {}).encode())
    return h.hexdigest()[:16]


def extract_game_seat(replay: dict, seat: int) -> dict:
    """一席 -> 样本流 dict（特征已 round 3 位省空间）。"""
    steps = replay["steps"]
    turns = []
    for t in range(1, len(steps)):
        obs = (steps[t - 1][seat] or {}).get("observation") or {}
        action = (steps[t][seat] or {}).get("action") or {}
        if not obs:
            continue
        g = [round(v, 3) for v in S.extract_global_features(obs, seat)]
        farms = obs.get("farms") or []
        me = farms[seat] if seat < len(farms) else {}
        unit_list = []
        positions = [me.get("farmer")] + list(me.get("hands") or [])
        farmer_act = action.get("farmer") or ["PASS"]
        hand_acts = action.get("hands") or []
        for i, pos in enumerate(positions):
            if not pos:
                continue
            uf = [round(v, 3) for v in S.extract_unit_features(obs, seat, pos)]
            act = farmer_act if i == 0 else (
                hand_acts[i - 1] if i - 1 < len(hand_acts) else ["PASS"])
            op_i, arg_i, qty_b = S.encode_unit_action(act or ["PASS"])
            unit_list.append([i == 0, uf, [op_i, arg_i, qty_b]])
        slots = S.encode_market_orders(action.get("market") or [])
        turns.append({"step": t, "g": g, "units": unit_list,
                      "market": [list(x) for x in slots]})
    return {"schema": S.SCHEMA_VERSION, "seat": seat, "turns": turns}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--include-rounds", action="store_true",
                    help="纳入本机语料高分对手席兜底（round*/ 目录）")
    ap.add_argument("--round-money-gate", type=int, default=ROUND_MONEY_GATE)
    args = ap.parse_args(argv)

    DATA.mkdir(parents=True, exist_ok=True)
    top_teams = load_top_teams()
    print(f"[extract] top-30 teams loaded: {len(top_teams)}")

    # ---- 收集候选席 ------------------------------------------------------
    candidates = []          # (source, path, replay_meta, seats_meta)
    metas = {}

    def scan_dir(source: str, pattern: str):
        for path in sorted(glob.glob(str(Path(pattern) / "episode-*.json"))):
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    replay = json.load(handle)
            except (OSError, ValueError) as exc:
                print(f"[extract] unreadable {path}: {exc}")
                continue
            steps = replay.get("steps") or []
            teams = (replay.get("info") or {}).get("TeamNames") or []
            rewards = replay.get("rewards") or [0.0, 0.0]
            if len(steps) < 100 or len(teams) != 2:
                continue
            eid = replay.get("id") or Path(path).stem.split("-")[1]
            metas[(source, str(eid))] = {
                "path": path, "teams": teams,
                "rewards": [float(r or 0) for r in rewards],
                "n_steps": len(steps),
                "seed": (replay.get("info") or {}).get("seed"),
                "mirror": teams[0] == teams[1],
            }

    scan_dir("bc-top", REPLAY_TOP)
    if args.include_rounds:
        for rnd in sorted(p for p in os.listdir(REPLAY_ROUNDS)
                          if p.startswith("round")):
            scan_dir("local", os.path.join(REPLAY_ROUNDS, rnd))

    # ---- 席筛选：top 队席全要；本机语料只取过高分门且非克隆的对手席 ----
    seat_rows = []
    for (source, eid), meta in sorted(metas.items()):
        replay = json.load(open(meta["path"], "r", encoding="utf-8"))
        for seat, team in enumerate(meta["teams"]):
            if source == "bc-top":
                if team in top_teams:
                    seat_rows.append((source, eid, seat, team, meta, replay))
                continue
            money = meta["rewards"][seat]
            if team == "renyxin" or money < args.round_money_gate:
                continue
            seat_rows.append((source, eid, seat, team, meta, replay))

    # ---- 克隆席过滤 ------------------------------------------------------
    sig_teams = defaultdict(set)
    for source, eid, seat, team, meta, replay in seat_rows:
        sig_teams[opening_signature(replay, seat)].add(team)
    fam_sizes = {sig: len(teams) for sig, teams in sig_teams.items()}
    clone_family_sigs = {sig for sig, n in fam_sizes.items()
                         if n >= CLONE_FAMILY_MIN_TEAMS}
    # 全动作流签名去重（同流只留首席）
    seen_full = {}
    kept, dropped_clone, dropped_dup = [], 0, 0
    for source, eid, seat, team, meta, replay in seat_rows:
        sig = opening_signature(replay, seat)
        is_top = team in top_teams
        if sig in clone_family_sigs and not is_top:
            dropped_clone += 1
            continue
        fsig = full_signature(replay, seat)
        key = (fsig,)
        if key in seen_full:
            dropped_dup += 1
            continue
        seen_full[key] = (source, eid, seat)
        kept.append((source, eid, seat, team, meta, replay,
                     sig in clone_family_sigs))
    print(f"[extract] seats kept={len(kept)} clone_dropped={dropped_clone} "
          f"dup_dropped={dropped_dup} clone_families={len(clone_family_sigs)}")

    # ---- 抽取落盘 --------------------------------------------------------
    manifest = {
        "schema": S.SCHEMA_VERSION,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "clone_filter": {"min_teams": CLONE_FAMILY_MIN_TEAMS,
                         "families": len(clone_family_sigs),
                         "dropped_clone": dropped_clone,
                         "dropped_dup": dropped_dup},
        "games": {}, "seats": [],
        "counts": {"games": 0, "seats": 0, "unit_samples": 0,
                   "market_samples": 0, "turns": 0},
    }
    t0 = time.time()
    n_unit = n_mkt = n_turn = 0
    for source, eid, seat, team, meta, replay, in_clone_fam in kept:
        payload = extract_game_seat(replay, seat)
        out_path = DATA / f"{source}-{eid}-s{seat}.json.gz"
        with gzip.open(out_path, "wt", encoding="utf-8") as handle:
            json.dump(payload, handle, separators=(",", ":"))
        n_turn += len(payload["turns"])
        n_unit += sum(len(t["units"]) for t in payload["turns"])
        n_mkt += sum(1 for t in payload["turns"]
                     if any(s[0] for s in t["market"]))
        manifest["seats"].append({
            "file": out_path.name, "source": source, "episode": eid,
            "seat": seat, "team": team,
            "final_money": meta["rewards"][seat],
            "opp_team": meta["teams"][1 - seat],
            "opp_money": meta["rewards"][1 - seat],
            "n_turns": len(payload["turns"]),
            "opening_sig_in_clone_family": in_clone_fam,
            "seed": meta["seed"], "mirror": meta["mirror"],
        })
        gkey = f"{source}:{eid}"
        manifest["games"].setdefault(gkey, {
            "teams": meta["teams"], "rewards": meta["rewards"],
            "n_steps": meta["n_steps"], "seed": meta["seed"],
            "seats_used": []})["seats_used"].append(seat)
        del replay
    manifest["counts"] = {"games": len(manifest["games"]),
                          "seats": len(manifest["seats"]),
                          "unit_samples": n_unit,
                          "market_samples": n_mkt, "turns": n_turn}
    manifest["wall_seconds"] = round(time.time() - t0, 1)
    out = SOFTWARE / "bc_track" / "data" / "corpus_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"[extract] seats={len(manifest['seats'])} games={len(manifest['games'])} "
          f"turns={n_turn} unit_samples={n_unit} market_turns={n_mkt} "
          f"wall={manifest['wall_seconds']}s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
