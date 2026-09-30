#!/usr/bin/env python3
"""band_extract.py —— 羊系带内深切：7 高分队 + 3 低分参照 + 我方 179 局的细粒度行为特征（2026-10-01 band-deepcut）

在 fingerprint_scan.py 基础上新增：day0_24 全日磁带、分日卖流节奏（30 日 orders/qty）、
终局段（480-720）细粒度（卖量峰值/买地/雇工/建设）、末日（>=696）倾泻、钱轨迹检查点、
bp 分段。输出 band-analysis/feats-band.jsonl。

用法：
  band_extract.py parquet  # ashok shards（带内队+低分参照，cap 300/队最近）
  band_extract.py json     # 我方 raw/renyxin-replays/ 179 局
"""
import glob, json, os, sys
from collections import defaultdict
from multiprocessing import Pool

import orjson

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fingerprint_extract import norm_farmer_tokens, norm_market_tokens

HERE = os.path.dirname(os.path.abspath(__file__))
BAND = ['Driz Lo', 'THIRD FARM CLUB', 'redblackbst', 'pensukesan',
        'Hello San Francisco', 'kanno', 'Terry Luo',
        'carlos-tagosaku', 'アルモンド', 'Thomas Tschinkel']
CAP = 300
MONEY_STEPS = [0, 24, 48, 120, 240, 360, 480, 600, 660, 690, 719]


def player_features(pi, team, steps, rewards, statuses, n_steps):
    day0_24 = []
    sell_orders_day = defaultdict(int)
    sell_qty_day = defaultdict(int)
    first_sell = None
    sell_qty_list = []
    sell_prod = defaultdict(int)
    late = defaultdict(int)  # sell_n/sell_qty/sell_qty_max/buyland/hire/coop/pasture/plant/harvest/bp
    last_day = defaultdict(int)
    bp_orders = 0; bp_third = defaultdict(int); bp_qty = []
    buy_land_steps = []
    first_coop = None; first_pasture = None; coop_n = 0; pasture_n = 0
    ba_orders = 0; hire_n = 0; first_hire = None
    plant_c = defaultdict(int)
    for si, s in enumerate(steps):
        if pi >= len(s):
            break
        p = s[pi]
        a = p.get('action')
        if isinstance(a, str):
            try:
                a = orjson.loads(a)
            except Exception:
                a = {}
        a = a or {}
        ft = norm_farmer_tokens(a.get('farmer'))
        mt = norm_market_tokens(a.get('market'))
        day = si // 24
        if si < 24:
            day0_24.append((ft, mt))
        for t in ft:
            if t.startswith('PLANT_'):
                plant_c[t[6:]] += 1
                if si >= 480: late['plant'] += 1
            elif t == 'HARVEST':
                if si >= 480: late['harvest'] += 1
            elif t == 'BUILD_COOP':
                coop_n += 1
                if first_coop is None: first_coop = si
            elif t == 'BUILD_PASTURE':
                pasture_n += 1
                if first_pasture is None: first_pasture = si
        for t in mt:
            if t == 'HIRE:-:-':
                hire_n += 1
                if first_hire is None: first_hire = si
                if si >= 480: late['hire'] += 1
        for x in (a.get('market') or []):
            if not (isinstance(x, list) and x and isinstance(x[0], str)):
                continue
            typ = x[0].upper()
            if typ == 'SELL':
                if first_sell is None: first_sell = si
                sell_orders_day[day] += 1
                q = 0
                try:
                    q = int(x[2]) if len(x) > 2 else 0
                except Exception:
                    pass
                sell_qty_day[day] += q
                sell_qty_list.append(q)
                if len(x) > 1 and isinstance(x[1], str):
                    sell_prod[x[1].upper()] += 1
                if si >= 480:
                    late['sell_n'] += 1; late['sell_qty'] += q
                    late['sell_qty_max'] = max(late['sell_qty_max'], q)
                if si >= 696:
                    last_day['sell_n'] += 1; last_day['sell_qty'] += q
            elif typ == 'BUY_PRODUCT':
                bp_orders += 1
                bp_third['early' if si < 240 else ('mid' if si < 480 else 'late')] += 1
                try:
                    bp_qty.append(int(x[2]) if len(x) > 2 else 0)
                except Exception:
                    pass
            elif typ == 'BUY_LAND':
                buy_land_steps.append(si)
                if si >= 480: late['buyland'] += 1
            elif typ == 'BUY_ANIMAL':
                ba_orders += 1
    # 钱轨迹：从 pi=0 的 observation 取双 farm 钱
    money_at = {}
    try:
        for ms in MONEY_STEPS:
            if ms < n_steps:
                fr = steps[ms][0]['observation']['farms']
                if pi < len(fr):
                    money_at[str(ms)] = fr[pi].get('money')
    except Exception:
        pass
    n_days = max(1, (n_steps + 23) // 24)
    return {
        'team': team, 'pi': pi,
        'reward': rewards[pi] if pi < len(rewards) else None,
        'status': statuses[pi] if pi < len(statuses) else None,
        'day0_24': day0_24,
        'first_sell': first_sell,
        'sell_orders_per_day': [sell_orders_day.get(d, 0) for d in range(n_days)],
        'sell_qty_per_day': [sell_qty_day.get(d, 0) for d in range(n_days)],
        'sell_qty_mean': round(sum(sell_qty_list) / len(sell_qty_list), 2) if sell_qty_list else 0,
        'sell_qty_max': max(sell_qty_list) if sell_qty_list else 0,
        'sell_vol': sum(sell_qty_list),
        'sell_orders': len(sell_qty_list),
        'sell_top_prods': sorted(sell_prod.items(), key=lambda kv: -kv[1])[:6],
        'bp_orders': bp_orders, 'bp_third': dict(bp_third),
        'bp_vol': sum(bp_qty),
        'buy_land_steps': buy_land_steps,
        'first_coop': first_coop, 'coop_n': coop_n,
        'first_pasture': first_pasture, 'pasture_n': pasture_n,
        'first_hire': first_hire, 'hire_n': hire_n,
        'ba_orders': ba_orders,
        'plant_top': sorted(plant_c.items(), key=lambda kv: -kv[1])[:6],
        'late': dict(late), 'last_day': dict(last_day),
        'money_at': money_at,
    }


def episode_features(d, src, eid=None, date=None):
    info = d.get('info') or {}
    teams = info.get('TeamNames') or [p.get('Name') for p in (info.get('Agents') or [])]
    steps = d.get('steps', [])
    rewards = d.get('rewards', [])
    statuses = d.get('statuses', [])
    rec = {
        'src': src, 'episode_id': eid if eid is not None else (d.get('id') or info.get('EpisodeId')),
        'date': date, 'teams': teams, 'seed': info.get('seed'),
        'rewards': rewards, 'n_steps': len(steps), 'players': [],
    }
    for pi, team in enumerate(teams):
        rec['players'].append(player_features(pi, team, steps, rewards, statuses, len(steps)))
    return rec


def work_parquet(job):
    shard_path, sel_ids, out_tmp, date = job
    import pyarrow.parquet as pq
    pf = pq.ParquetFile(shard_path)
    eids = pf.read(columns=['episode_id']).column('episode_id').to_pylist()
    idx_map = {eid: i for i, eid in enumerate(eids)}
    wanted = [idx_map[e] for e in sel_ids if e in idx_map]
    open(out_tmp, 'wb').close()
    n = 0
    with open(out_tmp, 'ab') as out:
        for i in wanted:
            tbl = pf.read_row_group(i, columns=['replay_json'])
            blob = tbl.column('replay_json')[0].as_py()
            try:
                d = orjson.loads(blob)
            except Exception:
                continue
            rec = episode_features(d, src=os.path.basename(shard_path),
                                   eid=eids[i], date=date)
            out.write(orjson.dumps(rec) + b'\n')
            n += 1
    return (os.path.basename(shard_path), n)


def run_parquet():
    import pandas as pd
    e = pd.read_parquet(os.path.join(HERE, 'raw/ashok205-meta/episodes.parquet'))
    e['parts'] = e['participants_json'].apply(orjson.loads)
    targets = set(BAND)
    per_team = defaultdict(list)
    for _, row in e.iterrows():
        for t in row['parts']:
            if t in targets:
                per_team[t].append((str(row['date']), int(row['episode_id']), row['replay_shard']))
    sel = {}
    for t, lst in per_team.items():
        lst.sort()
        take = lst[-CAP:] if len(lst) > CAP else lst
        for date, eid, shard in take:
            sel[eid] = (shard, date)
    print('per-team available:', {t: len(v) for t, v in per_team.items()})
    print('unique episodes:', len(sel))
    by_shard = defaultdict(list)
    for eid, (shard, date) in sel.items():
        by_shard[shard].append((eid, date))
    jobs = []
    for i, (s, ids) in enumerate(sorted(by_shard.items())):
        p = os.path.join(HERE, 'raw/ashok205-shards', s)
        if not os.path.exists(p):
            continue
        jobs.append((p, [x[0] for x in ids], os.path.join(HERE, 'band-analysis/feats-band.jsonl.tmp.%d' % i), ids[0][1]))
    print('shards:', len(jobs))
    out_path = os.path.join(HERE, 'band-analysis/feats-band.jsonl')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with Pool(min(12, os.cpu_count() or 4)) as pool:
        for shard, n in pool.imap_unordered(work_parquet, jobs):
            print(f'{shard}: {n}', flush=True)
    with open(out_path, 'wb') as out:
        for j in jobs:
            try:
                with open(j[2], 'rb') as f:
                    out.write(f.read())
                os.remove(j[2])
            except FileNotFoundError:
                pass
    print('DONE parquet ->', out_path)


def work_json_one(f):
    import re
    with open(f, 'rb') as fh:
        d = orjson.loads(fh.read())
    rec = episode_features(d, src=os.path.basename(os.path.dirname(f)))
    m = re.search(r'episode-(\d+)-replay', os.path.basename(f))
    if m:
        rec['episode_id'] = int(m.group(1))
    # 文件名前缀区分我方两份计分件
    rec['sub'] = 'Cfinal' if 'Cfinal' in os.path.basename(f) else 'S8'
    return orjson.dumps(rec)


def run_json():
    import re, csv
    # 日期：从官方 episodes CSV 反填
    epdate = {}
    for fn in ['raw/episodes-Cfinal-56697824.csv', 'raw/episodes-S8-56708866.csv']:
        with open(os.path.join(HERE, fn), newline='') as f:
            for row in csv.DictReader(f):
                try:
                    epdate[int(row['id'])] = row['createTime'][:10]
                except (TypeError, ValueError):
                    continue
    files = sorted(glob.glob(os.path.join(HERE, 'raw/renyxin-replays/*.json')))
    out_path = os.path.join(HERE, 'band-analysis/feats-renyxin-band.jsonl')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as out:
        with Pool(min(8, os.cpu_count() or 4)) as pool:
            for blob in pool.imap(work_json_one, files, chunksize=4):
                r = orjson.loads(blob)
                d = epdate.get(r['episode_id'])
                if d:
                    r['date'] = d
                out.write(orjson.dumps(r) + b'\n')
    print('DONE json ->', out_path, len(files))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'parquet'
    if mode == 'parquet':
        run_parquet()
    else:
        run_json()
