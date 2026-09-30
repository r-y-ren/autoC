#!/usr/bin/env python3
"""fingerprint_scan.py —— 从 parquet 分片/JSON 文件流式提取回放指纹（2026-10-01 fingerprint-scan）

用法：
  fingerprint_scan.py --mode parquet --index <episodes.parquet> --shard-dir <dir> --out <out.jsonl> [--cap-per-team N] [--teams-file f]
  fingerprint_scan.py --mode json --dir <json_dir> --out <out.jsonl>

选择逻辑（parquet 模式）：按 episodes.parquet 的 participants_json 选目标队局，
每队取最近 cap 局（按 date, episode_id 排序），跨队去重后按分片读行（每 row_group=1 局）。
"""
import argparse, glob, json, os, sys
from collections import defaultdict
from multiprocessing import Pool

import orjson

# 复用 fingerprint_extract.py 的规范化函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fingerprint_extract import (
    norm_farmer_tokens, norm_market_tokens, qty_bucket,
)

def parse_replay(blob):
    """orjson 解析 replay 字符串/字节 → dict（异常返回 None）"""
    try:
        return orjson.loads(blob)
    except Exception:
        return None

def features_from_replay(d, src):
    """episode dict → 每 player 特征（与 fingerprint_extract.process_file 相同口径）"""
    info = d.get('info') or {}
    teams = info.get('TeamNames') or [p.get('Name') for p in (info.get('Agents') or [])]
    steps = d.get('steps', [])
    rewards = d.get('rewards', [])
    statuses = d.get('statuses', [])
    rec = {
        'src': src,
        'episode_id': d.get('id') or info.get('EpisodeId'),
        'teams': teams,
        'seed': info.get('seed'),
        'rewards': rewards,
        'statuses': statuses,
        'n_steps': len(steps),
        'players': [],
    }
    for pi, team in enumerate(teams):
        day0_8 = []; day0_24 = []
        first_sell = None; sell_orders = 0
        sell_third = defaultdict(int); sell_prod = defaultdict(int); sell_qty_list = []
        buy_seed_first = None; seed_c = defaultdict(int)
        bp_orders = 0; bp_prod = defaultdict(int); bp_first = None; bp_qty = []
        ba_orders = 0; ba_animal = defaultdict(int); ba_first = None
        buy_land_steps = []; first_coop = None; first_pasture = None
        coop_n = 0; pasture_n = 0
        first_hire = None; hire_n = 0
        plant_c = defaultdict(int); harvest_n = 0; dig_n = 0; water_n = 0; care_n = 0; feed_n = 0
        for si, s in enumerate(steps):
            if pi >= len(s): break
            p = s[pi]
            a = p.get('action')
            if isinstance(a, str):
                try: a = orjson.loads(a)
                except Exception: a = {}
            a = a or {}
            ft = norm_farmer_tokens(a.get('farmer'))
            mt = norm_market_tokens(a.get('market'))
            if si < 24:
                day0_24.append((ft, mt))
                if si < 8:
                    day0_8.append((ft, mt))
            for t in ft:
                if t.startswith('PLANT_'): plant_c[t[6:]] += 1
                elif t == 'HARVEST': harvest_n += 1
                elif t == 'DIG': dig_n += 1
                elif t == 'WATER': water_n += 1
                elif t == 'CARE': care_n += 1
                elif t == 'FEED': feed_n += 1
                elif t == 'BUILD_COOP':
                    coop_n += 1
                    if first_coop is None: first_coop = si
                elif t == 'BUILD_PASTURE':
                    pasture_n += 1
                    if first_pasture is None: first_pasture = si
            for x in (a.get('market') or []):
                if not (isinstance(x, list) and x and isinstance(x[0], str)):
                    continue
                typ = x[0].upper()
                if typ == 'SELL':
                    sell_orders += 1
                    if first_sell is None: first_sell = si
                    sell_third['early' if si < 240 else ('mid' if si < 480 else 'late')] += 1
                    if len(x) > 1 and isinstance(x[1], str): sell_prod[x[1].upper()] += 1
                    try: sell_qty_list.append(int(x[2]) if len(x) > 2 else 0)
                    except Exception: pass
                elif typ == 'BUY_SEED':
                    if buy_seed_first is None: buy_seed_first = si
                    if len(x) > 1 and isinstance(x[1], str): seed_c[x[1].upper()] += 1
                elif typ == 'BUY_PRODUCT':
                    bp_orders += 1
                    if bp_first is None: bp_first = si
                    if len(x) > 1 and isinstance(x[1], str): bp_prod[x[1].upper()] += 1
                    try: bp_qty.append(int(x[2]) if len(x) > 2 else 0)
                    except Exception: pass
                elif typ == 'BUY_ANIMAL':
                    ba_orders += 1
                    if ba_first is None: ba_first = si
                    if len(x) > 1 and isinstance(x[1], str): ba_animal[x[1].upper()] += 1
                elif typ == 'BUY_LAND':
                    buy_land_steps.append(si)
                elif typ == 'HIRE':
                    hire_n += 1
                    if first_hire is None: first_hire = si
        tot3 = sum(sell_third.values()) or 1
        rec['players'].append({
            'team': team, 'pi': pi,
            'reward': rewards[pi] if pi < len(rewards) else None,
            'status': statuses[pi] if pi < len(statuses) else None,
            'day0_8': day0_8,
            'first_sell': first_sell, 'sell_orders': sell_orders,
            'sell_qty_mean': (round(sum(sell_qty_list)/len(sell_qty_list), 2) if sell_qty_list else 0),
            'sell_vol': sum(sell_qty_list),
            'sell_third': {k: round(v/tot3, 3) for k, v in sell_third.items()},
            'sell_top_prods': sorted(sell_prod.items(), key=lambda kv: -kv[1])[:5],
            'buy_seed_first': buy_seed_first,
            'seed_top': sorted(seed_c.items(), key=lambda kv: -kv[1])[:4],
            'bp_orders': bp_orders, 'bp_first': bp_first,
            'bp_vol': sum(bp_qty),
            'bp_top': sorted(bp_prod.items(), key=lambda kv: -kv[1])[:4],
            'ba_orders': ba_orders, 'ba_first': ba_first,
            'ba_top': sorted(ba_animal.items(), key=lambda kv: -kv[1])[:4],
            'buy_land_n': len(buy_land_steps), 'buy_land_steps': buy_land_steps[:6],
            'first_coop': first_coop, 'coop_n': coop_n,
            'first_pasture': first_pasture, 'pasture_n': pasture_n,
            'first_hire': first_hire, 'hire_n': hire_n,
            'plant_top': sorted(plant_c.items(), key=lambda kv: -kv[1])[:5],
            'harvest_n': harvest_n, 'dig_n': dig_n, 'water_n': water_n,
            'care_n': care_n, 'feed_n': feed_n,
        })
    return rec

def work_parquet(args):
    shard_path, sel_ids, out_tmp = args
    import pyarrow.parquet as pq
    pf = pq.ParquetFile(shard_path)
    # episode_id 列很小，整列读
    eids = pf.read(columns=['episode_id']).column('episode_id').to_pylist()
    idx_map = {eid: i for i, eid in enumerate(eids)}
    wanted = [idx_map[e] for e in sel_ids if e in idx_map]
    n = 0
    open(out_tmp, 'wb').close()  # 清残留
    with open(out_tmp, 'ab') as out:
        for i in wanted:
            tbl = pf.read_row_group(i, columns=['replay_json'])
            blob = tbl.column('replay_json')[0].as_py()
            d = parse_replay(blob)
            if d is None: continue
            rec = features_from_replay(d, src=os.path.basename(shard_path))
            rec['episode_id'] = eids[i]  # 用分片段的数字局号覆写（JSON 内 id 为 UUID）
            out.write(orjson.dumps(rec) + b'\n')
            n += 1
    return (os.path.basename(shard_path), n)

def work_json_one(f):
    import re
    with open(f, 'rb') as fh:
        d = parse_replay(fh.read())
    if d is None:
        return None
    rec = features_from_replay(d, src=os.path.basename(os.path.dirname(f)))
    m = re.search(r'episode-(\d+)-replay', os.path.basename(f))
    if m:
        rec['episode_id'] = int(m.group(1))
    return orjson.dumps(rec)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['parquet', 'json'])
    ap.add_argument('--index')
    ap.add_argument('--shard-dir')
    ap.add_argument('--dir')
    ap.add_argument('--out', required=True)
    ap.add_argument('--cap-per-team', type=int, default=200)
    ap.add_argument('--teams-file', help='目标队名单（每行一队，精确匹配 TeamNames）')
    args = ap.parse_args()

    if args.mode == 'json':
        files = sorted(glob.glob(os.path.join(args.dir, '*.json')))
        with open(args.out, 'wb') as out:
            with Pool(min(8, os.cpu_count() or 4)) as pool:
                for i, blob in enumerate(pool.imap(work_json_one, files, chunksize=4)):
                    if blob: out.write(blob + b'\n')
                    if (i+1) % 50 == 0: print(f'{i+1}/{len(files)}', flush=True)
        print('DONE json ->', args.out)
        return

    # parquet 模式
    import pandas as pd
    e = pd.read_parquet(args.index)
    e['parts'] = e['participants_json'].apply(orjson.loads)
    targets = set()
    if args.teams_file:
        targets = {l.strip() for l in open(args.teams_file) if l.strip()}
    per_team = defaultdict(list)
    for _, row in e.iterrows():
        for t in row['parts']:
            if t in targets:
                per_team[t].append((str(row['date']), int(row['episode_id']), row['replay_shard']))
    sel = {}
    for t, lst in per_team.items():
        lst.sort()
        take = lst[-args.cap_per_team:] if len(lst) > args.cap_per_team else lst
        for date, eid, shard in take:
            sel[eid] = shard
    print('teams selected:', {t: min(len(v), args.cap_per_team) for t, v in per_team.items()})
    print('unique episodes:', len(sel))
    by_shard = defaultdict(list)
    for eid, shard in sel.items():
        by_shard[shard].append(eid)
    jobs = [(os.path.join(args.shard_dir, s), ids, args.out + '.tmp.%d' % i)
            for i, (s, ids) in enumerate(sorted(by_shard.items()))]
    # 先过滤存在的分片
    jobs_exist = [j for j in jobs if os.path.exists(j[0])]
    print(f'shards: {len(jobs_exist)}/{len(jobs)} exist')
    with Pool(min(12, os.cpu_count() or 4)) as pool, open(args.out, 'wb') as out:
        for shard, n in pool.imap_unordered(work_parquet, jobs_exist):
            print(f'{shard}: {n} episodes', flush=True)
    for j in jobs_exist:
        try:
            with open(j[2], 'rb') as f: out_tmp = f.read()
            with open(args.out, 'ab') as out: out.write(out_tmp)
            os.remove(j[2])
        except FileNotFoundError:
            pass
    print('DONE parquet ->', args.out)

if __name__ == '__main__':
    main()
