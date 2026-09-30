#!/usr/bin/env python3
"""fingerprint_extract.py —— kaggriculture 回放行为指纹提取（2026-10-01 fingerprint-scan）

输入：回放 episode JSON 目录（官方日更/georgymarin/ashok205 通用，720 步 kaggle-environments 格式）。
输出：episodes_features.jsonl —— 每行 = (episode_id, team_name, features)。

特征（对齐 fn_docs hybrid 任务书）：
  day0 磁带：前 8 步（及前 24 步备选）动作序列规范化（市场：类型×品类×量级分桶；农民：指令归并）；
  SELL 行为：首卖步、单均量、每拍卖单数、卖出时点直方图（前/中/后段）、卖出品类分布；
  BUY 行为：BUILD 节奏（首 coop/pasture 步）、种子/动物/商品购买集中度；
  其它：首雇工步、总雇工、BUY_PRODUCT（订单簿买侧）行为、终局 reward/status。
"""
import json, os, sys, hashlib, glob
from collections import Counter
from multiprocessing import Pool

FARMER_KEYWORDS = {
    'PASS','NORTH','SOUTH','EAST','WEST','WATER','FEED','CARE','HARVEST','DIG',
    'BUILD_COOP','BUILD_PASTURE','COLLECT_FERTILIZER','FERTILIZE','PLANT','PLACE',
    'PICKUP','DROP','SELL','BUY',
}
CROPS = {'CARROT','MELON','STRAWBERRY','TOMATO','WHEAT'}
ANIMALS = {'COW','GOOSE','SHEEP'}
PRODUCTS = CROPS | ANIMALS | {'EGG','MILK','WOOL','FERTILIZER'}

def qty_bucket(q):
    if q is None: return 'x'
    q = int(q)
    if q <= 0: return '0'
    if q <= 2: return '1'
    if q <= 5: return '2'
    if q <= 10: return '3'
    if q <= 25: return '4'
    if q <= 50: return '5'
    return '6'

def norm_farmer_tokens(items):
    """农民动作序列 → 规范化 token 列表（PLANT+作物 / PLACE+数字 归并，移动折叠为 MV）"""
    out = []
    toks = [x for x in (items or [])]
    i = 0
    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            up = t.upper()
            if up == 'PLANT' and i+1 < len(toks) and isinstance(toks[i+1], str) and toks[i+1].upper() in PRODUCTS:
                out.append('PLANT_' + toks[i+1].upper()); i += 2; continue
            if up == 'PLACE':
                nxt = toks[i+1] if i+1 < len(toks) else None
                out.append('PLACE'); i += 1
                if isinstance(nxt, str) and nxt.isdigit():
                    # 归并 PLACE 坐标参数为单一 token（保留数字本身：磁带含具体落位）
                    out[-1] = 'PLACE' + nxt; i += 1
                continue
            if up in ('NORTH','SOUTH','EAST','WEST'):
                out.append('MV'); i += 1; continue
            out.append(up); i += 1; continue
        else:
            out.append('F' + str(t)); i += 1
    return out

def norm_market_tokens(items):
    """市场动作 → (TYPE, 品类, 量桶) token 列表"""
    out = []
    for x in (items or []):
        if isinstance(x, list) and x and isinstance(x[0], str):
            typ = x[0].upper()
            prod = x[1].upper() if len(x) > 1 and isinstance(x[1], str) else '-'
            qty = x[2] if len(x) > 2 else None
            if typ in ('SELL','BUY_SEED','BUY_PRODUCT','BUY_ANIMAL'):
                out.append(f'{typ}:{prod}:{qty_bucket(qty)}')
            else:  # BUY_LAND / HIRE / 未知
                out.append(f'{typ}:-:-')
        else:
            out.append('RAW:' + str(x)[:12])
    return out

def step_tokens(p):
    a = p.get('action')
    if isinstance(a, str):
        try: a = json.loads(a)
        except Exception: a = {}
    a = a or {}
    ft = norm_farmer_tokens(a.get('farmer'))
    mt = norm_market_tokens(a.get('market'))
    return ft, mt, a

def process_file(path):
    try:
        with open(path) as f:
            d = json.load(f)
    except Exception as e:
        return {'file': os.path.basename(path), 'error': 'parse:' + str(e)[:80]}
    info = d.get('info', {}) or {}
    teams = info.get('TeamNames') or [p.get('Name') for p in (info.get('Agents') or [])]
    steps = d.get('steps', [])
    rewards = d.get('rewards', [])
    statuses = d.get('statuses', [])
    rec = {
        'file': os.path.basename(path),
        'episode_id': d.get('id') or info.get('EpisodeId'),
        'teams': teams,
        'seed': info.get('seed'),
        'rewards': rewards,
        'statuses': statuses,
        'n_steps': len(steps),
        'players': [],
    }
    for pi, team in enumerate(teams):
        day0_8, day0_24 = [], []
        ft_all = []
        first_sell = None; sell_orders = 0; sell_vol = 0
        sell_third = Counter(); sell_prod = Counter(); sell_qty_list = []
        buy_seed_first = None; seed_c = Counter(); buy_seed_vol = 0
        bp_orders = 0; bp_vol = 0; bp_prod = Counter(); bp_first = None
        ba_orders = 0; ba_vol = 0; ba_animal = Counter(); ba_first = None
        buy_land_steps = []; first_coop = None; first_pasture = None
        coop_n = 0; pasture_n = 0
        first_hire = None; hire_n = 0
        plant_c = Counter(); harvest_n = 0; dig_n = 0; water_n = 0; care_n = 0; feed_n = 0
        tape_full = []
        for si, s in enumerate(steps):
            if pi >= len(s): break
            p = s[pi]
            ft, mt, a_raw = step_tokens(p)
            if si < 24:
                tape_full.append((ft, mt))
            if si < 8:
                day0_8.append((list(ft), list(mt)))
            if si < 24:
                day0_24.append((list(ft), list(mt)))
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
            for t in mt:
                typ = t.split(':')[0]
                if typ == 'SELL':
                    sell_orders += 1
                    if first_sell is None: first_sell = si
                    q = t.rsplit(':', 1)[1]
                    sell_third['early' if si < 240 else ('mid' if si < 480 else 'late')] += 1
                    prod = t.split(':')[1]
                    sell_prod[prod] += 1
                elif typ == 'BUY_SEED':
                    if buy_seed_first is None: buy_seed_first = si
                    seed_c[t.split(':')[1]] += 1
                elif typ == 'BUY_PRODUCT':
                    bp_orders += 1
                    if bp_first is None: bp_first = si
                    bp_prod[t.split(':')[1]] += 1
                elif typ == 'BUY_ANIMAL':
                    ba_orders += 1
                    if ba_first is None: ba_first = si
                    ba_animal[t.split(':')[1]] += 1
                elif typ == 'BUY_LAND':
                    buy_land_steps.append(si)
                elif typ == 'HIRE':
                    hire_n += 1
                    if first_hire is None: first_hire = si
        # 量级需从原始动作取（bucket 丢了均值），二次轻扫卖量
        sell_qty_list = []
        for si, s in enumerate(steps):
            if pi >= len(s): break
            a = s[pi].get('action')
            if isinstance(a, str):
                try: a = json.loads(a)
                except Exception: a = {}
            for x in (a or {}).get('market', []) or []:
                if isinstance(x, list) and x and x[0] == 'SELL':
                    try: sell_qty_list.append(int(x[2]) if len(x) > 2 else 0)
                    except Exception: pass
        tot3 = sum(sell_third.values()) or 1
        player = {
            'team': team, 'pi': pi,
            'reward': rewards[pi] if pi < len(rewards) else None,
            'status': statuses[pi] if pi < len(statuses) else None,
            'day0_8': day0_8, 'day0_24_sig': hashlib.md5(
                json.dumps(day0_24, separators=(',', ':')).encode()).hexdigest()[:10],
            'day0_8_sig': hashlib.md5(
                json.dumps(day0_8, separators=(',', ':')).encode()).hexdigest()[:10],
            'first_sell': first_sell, 'sell_orders': sell_orders,
            'sell_qty_mean': (round(sum(sell_qty_list)/len(sell_qty_list), 2) if sell_qty_list else 0),
            'sell_vol': sum(sell_qty_list),
            'sell_third': {k: round(v/tot3, 3) for k, v in sell_third.items()},
            'sell_top_prods': sell_prod.most_common(5),
            'buy_seed_first': buy_seed_first, 'seed_top': seed_c.most_common(4),
            'bp_orders': bp_orders, 'bp_first': bp_first, 'bp_top': bp_prod.most_common(4),
            'ba_orders': ba_orders, 'ba_first': ba_first, 'ba_top': ba_animal.most_common(4),
            'buy_land_n': len(buy_land_steps), 'buy_land_steps': buy_land_steps[:6],
            'first_coop': first_coop, 'coop_n': coop_n,
            'first_pasture': first_pasture, 'pasture_n': pasture_n,
            'first_hire': first_hire, 'hire_n': hire_n,
            'plant_top': plant_c.most_common(5), 'harvest_n': harvest_n,
            'dig_n': dig_n, 'water_n': water_n, 'care_n': care_n, 'feed_n': feed_n,
        }
        rec['players'].append(player)
    return rec

def main():
    src_dir = sys.argv[1]
    out_path = sys.argv[2]
    files = sorted(glob.glob(os.path.join(src_dir, '*.json')))
    n_workers = min(12, os.cpu_count() or 4)
    done = 0
    with Pool(n_workers) as pool, open(out_path, 'w') as out:
        for rec in pool.imap_unordered(process_file, files, chunksize=2):
            out.write(json.dumps(rec, separators=(',', ':')) + '\n')
            done += 1
            if done % 50 == 0:
                print(f'{done}/{len(files)}', flush=True)
    print(f'DONE {done}/{len(files)} -> {out_path}', flush=True)

if __name__ == '__main__':
    main()
