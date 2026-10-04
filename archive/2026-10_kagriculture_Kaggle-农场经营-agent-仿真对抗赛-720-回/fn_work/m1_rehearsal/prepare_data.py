#!/usr/bin/env python3
"""prepare_data.py —— M1 预测器可行性预演：回放语料 → 市场时序数据集（2026-10-03, dff20b-5）

任务定义（主任务）：下一拍市场价格预测。
  输入（t 拍可观察的公开状态窗口）：各品价格/库存偏差/净成交量(推断)/城镇排水向量/时间/商店数/双方金钱
  输出：t+1 拍 9 品价格（等价于预测 delta = price[t+1] - price[t]）

回放步进约定（已在本语料 20 局上实证校准，见 README）：
  - steps[t][pi].action 是"产生了 observation[t]"的动作（act+1 约定，5755:170 判别）；
  - inv[t+1] = inv[t] + committed_trades(action@steps[t+1]) - drain(step=t)；
  - drain(step): step%4==0 每家已解锁商店排其单品（单品类店×2）；step%12==0 城中心全品各-1（除 FERTILIZER）
    ——区间取自回放 configuration（townShopSellInterval=4, townCenterSellInterval=12）；
  - price[t] = market_price(inv[t])（引擎确定性定价；1.32.2 与本地 1.32.2 缓存在 CARROT/TOMATO/EGG
    的 hinge 支有 ±1-2 版本差，故引擎先验基线用"训练集标定的 inv→price 映射"而非硬编码公式）。

净成交量 net_comm[s] = inv[s] - inv[s-1] + drain(s-1)（s=0 记 0）：
  这是线上 t 拍可从公开状态直接推断的量（对手机密订单只能事后经库存轨迹推断），无泄漏。

用法（本机 /tmp/m1env，需 pyarrow orjson numpy）：
  python prepare_data.py --shards <fingerprint-scan/raw/ashok205-shards> --out data/
"""
import argparse
import glob
import hashlib
import json
import os
from collections import Counter
from multiprocessing import Pool

import numpy as np
import orjson
import pyarrow.parquet as pq

PRODS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
PIDX = {p: i for i, p in enumerate(PRODS)}
I0 = 10000
N_STEPS = 720
SHOPS_TABLE = {
    "BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"], "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"], "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
SHOP_INTERVAL = 4   # 回放 configuration 实测
CENTER_INTERVAL = 12


def drain_vec(shops, step):
    d = np.zeros(9, dtype=np.int16)
    if step % SHOP_INTERVAL == 0:
        for sh in shops:
            for it in SHOPS_TABLE.get(sh, []):
                d[PIDX[it]] += 2 if len(SHOPS_TABLE[sh]) == 1 else 1
    if step % CENTER_INTERVAL == 0:
        for p in PRODS:
            if p != "FERTILIZER":
                d[PIDX[p]] += 1
    return d


def requested_trades_vec(steps, t, n_players):
    """action@steps[t] 的请求净交易（SELL +, BUY_PRODUCT -），仅用于统计 committed/请求残差。"""
    tr = np.zeros(9, dtype=np.int32)
    for pi in range(n_players):
        a = steps[t][pi].get("action")
        if isinstance(a, str):
            try:
                a = orjson.loads(a)
            except Exception:
                a = {}
        for x in (a or {}).get("market", []) or []:
            if isinstance(x, list) and len(x) >= 3 and x[0] in ("SELL", "BUY_PRODUCT") and isinstance(x[1], str):
                j = PIDX.get(x[1].upper())
                if j is None:
                    continue
                try:
                    q = int(x[2])
                except (TypeError, ValueError):
                    continue
                tr[j] += q if x[0] == "SELL" else -q
    return tr


def extract_episode(blob):
    """单局 → (meta, prices, inv_dev, drain, net_comm, shops_n, money) 或 (meta, None)。"""
    d = orjson.loads(blob)
    steps = d.get("steps", [])
    info = d.get("info") or {}
    teams = info.get("TeamNames") or [p.get("Name") for p in (info.get("Agents") or [])]
    rewards = d.get("rewards") or []
    statuses = d.get("statuses") or []
    eid = d.get("id") or info.get("EpisodeId")
    meta = {
        "episode_id": eid,
        "teams": teams,
        "rewards": rewards,
        "statuses": statuses,
        "n_steps": len(steps),
        "seed": info.get("seed"),
    }
    if len(steps) != N_STEPS:
        return meta, None, None
    try:
        obs0 = steps[0][0]["observation"]
        if "market" not in obs0 or obs0["market"]["prices"].get("WHEAT") is None:
            return meta, None, None
        n_players = len(steps[0])
    except Exception:
        return meta, None, None

    prices = np.zeros((N_STEPS, 9), dtype=np.int16)
    inv_dev = np.zeros((N_STEPS, 9), dtype=np.int16)
    drain = np.zeros((N_STEPS, 9), dtype=np.int16)
    net_comm = np.zeros((N_STEPS, 9), dtype=np.int16)
    shops_n = np.zeros(N_STEPS, dtype=np.int16)
    money = np.zeros((N_STEPS, 2), dtype=np.int32)
    req_resid = Counter()  # requested vs inferred-committed 残差统计
    try:
        for t in range(N_STEPS):
            st = steps[t]
            obs = st[0]["observation"]
            m = obs["market"]
            pr = m["prices"]; inv = m["inventory"]
            for p, j in PIDX.items():
                prices[t, j] = pr[p]
                inv_dev[t, j] = inv[p] - I0
            shops = (obs.get("town") or {}).get("unlocked_shops") or []
            shops_n[t] = len(shops)
            drain[t] = drain_vec(shops, t)
            farms = obs.get("farms") or []
            for k in range(min(2, len(farms))):
                money[t, k] = int(round(farms[k].get("money") or 0))
            if t > 0:
                prev = steps[t - 1][0]["observation"]["market"]["inventory"]
                committed = np.zeros(9, dtype=np.int32)
                for p, j in PIDX.items():
                    committed[j] = inv[p] - prev[p] + drain[t - 1, j]
                net_comm[t] = committed.astype(np.int16)
                req = requested_trades_vec(steps, t, n_players)
                diff = committed - req
                req_resid["cells"] += 9
                req_resid["match"] += int((diff == 0).sum())
    except Exception as e:
        return meta, None, None
    return meta, (prices, inv_dev, drain, net_comm, shops_n, money), dict(req_resid)


def work_rowgroup(job):
    shard_path, rg, eid = job
    pf = pq.ParquetFile(shard_path)
    tbl = pf.read_row_group(rg, columns=["replay_json"])
    blob = tbl.column("replay_json")[0].as_py()
    meta, pack, resid = extract_episode(blob)
    meta["episode_id"] = eid
    return meta, pack, resid


def split_of(eid):
    h = int(hashlib.md5(str(eid).encode()).hexdigest()[:8], 16) % 100
    return "train" if h < 80 else ("val" if h < 90 else "test")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    shard_files = sorted(glob.glob(os.path.join(args.shards, "*.parquet")))
    assert shard_files, "no parquet shards"
    jobs = []
    shard_of = {}
    for sp in shard_files:
        pf = pq.ParquetFile(sp)
        eids = pf.read(columns=["episode_id"]).column("episode_id").to_pylist()
        shard_of[os.path.basename(sp)] = pf.metadata.num_rows
        for rg, eid in enumerate(eids):
            jobs.append((sp, rg, eid))
    print(f"shards={len(shard_files)} episodes={len(jobs)}", flush=True)

    packs = {"train": [], "val": [], "test": []}
    metas = {"train": [], "val": [], "test": []}
    resid_tot = Counter()
    skipped = Counter()
    done = 0
    with Pool(args.workers) as pool:
        for meta, pack, resid in pool.imap_unordered(work_rowgroup, jobs, chunksize=16):
            done += 1
            resid_tot.update({k: v for k, v in resid.items()}) if resid else None
            if pack is None:
                skipped[str(meta.get("n_steps"))] += 1
                meta["valid"] = False
            else:
                sp = split_of(meta["episode_id"])
                packs[sp].append(pack)
                meta["valid"] = True
                meta["split"] = sp
                metas[sp].append(meta)
            if done % 2000 == 0:
                print(f"  {done}/{len(jobs)} skipped={sum(skipped.values())}", flush=True)

    summary = {"n_jobs": len(jobs), "skipped": dict(skipped),
               "req_vs_committed": {"cells": resid_tot.get("cells", 0), "match": resid_tot.get("match", 0)}}
    for sp in ("train", "val", "test"):
        n = len(packs[sp])
        if n == 0:
            continue
        out = {
            "prices": np.stack([p[0] for p in packs[sp]]),
            "inv_dev": np.stack([p[1] for p in packs[sp]]),
            "drain": np.stack([p[2] for p in packs[sp]]),
            "net_comm": np.stack([p[3] for p in packs[sp]]),
            "shops_n": np.stack([p[4] for p in packs[sp]]),
            "money": np.stack([p[5] for p in packs[sp]]),
        }
        for name, arr in out.items():
            np.save(os.path.join(args.out, f"{sp}_{name}.npy"), arr)
        with open(os.path.join(args.out, f"manifest_{sp}.jsonl"), "wb") as f:
            for m in metas[sp]:
                f.write(orjson.dumps(m) + b"\n")
        summary[sp] = {"episodes": n, "windows_per_ep": N_STEPS - 16}
        print(f"{sp}: {n} episodes saved", flush=True)

    team_c = Counter()
    for sp in ("train", "val", "test"):
        for m in metas[sp]:
            for t in m["teams"]:
                team_c[t] += 1
    summary["team_top20"] = team_c.most_common(20)
    summary["team_unique"] = len(team_c)
    with open(os.path.join(args.out, "summary.json"), "wb") as f:
        f.write(orjson.dumps(summary, option=orjson.OPT_INDENT_2))
    print("requested-vs-committed cell match rate:",
          resid_tot.get("match", 0), "/", resid_tot.get("cells", 0))
    print("DONE ->", args.out)


if __name__ == "__main__":
    main()
