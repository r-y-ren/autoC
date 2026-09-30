# -*- coding: utf-8 -*-
"""_bisect3_repro（s2prod lab 判决补件）：原代理 _bisect/_bisect2 排查点复现判定。

背景：_bisect.py/_bisect2.py（18:34/18:37）针对当时 apply_route_s2 6 参签名写的
排查件，排查点=①加法手术后 held 动物丢格（hires-only/ops-no-wheat/buf60 三分法）
②基底手位被覆写（base hand clobbers）③动物格 FEED 日丢失（断粮死因）。
build_s2.py 终稿（19:12）签名已改 7 参（need/safe 现金安全），原脚本已 TypeError。
本件以**完整 build_one 路径**（含 clear_tile_plants/goose_rhythm）复跑 ②③ + ①
held 对照，判定三死因（错位/断粮/偷麦）是否已修。只读判定，不写工件。
"""
import sys, copy, collections
from pathlib import Path
sys.path.insert(0, '..'); sys.path.insert(0, '../orderbook_goose_lab')
sys.path.insert(0, '../orderbook_goose_fullplan_lab')
sys.path.insert(0, '../orderbook_goose_add_lab'); sys.path.insert(0, '.')
from orderbook_r37 import retape_sheep as rs
import goose_line as gl
import build_s2 as B

base = rs._decode_routes(Path('../orderbook_composite_lab/build/c_final/main.py').read_text())
B._load_pos(base, ['0'])
from kaggsim.serve import Serve
srv = Serve()
vb = gl._rollout(base, '0', 780010, srv=srv)
print('base held', dict(vb['held']), 'final_money', vb['final_money'])

w = copy.deepcopy(base)
tbl = []
stats = collections.Counter()
# 忠实复刻 build_one：route 0、n_r=8+(0%3)-1=7（与 build_s2.json 一致）
rec = B.build_one(w, tbl, stats, '0', 8, base, vb, srv)
g = rec['route_gates']
print('build_one ok', g['ok'], 'held_var', g['held_var'],
      'realized', g['realized_base'], '->', g['realized_var'],
      'final_money_var', g['final_money_var'])
v = gl._rollout(w, '0', 780010, srv=srv)
bt = {tuple(x[:2]) for x in vb['tiles_with_animal']}
vt = {tuple(x[:2]) for x in v['tiles_with_animal']}
print('re-rollout held', dict(v['held']), 'final_money', v['final_money'],
      'stranded', v['stranded_animals'])
print('lost animal tiles:', sorted(bt - vt))

# ---- 排查点②：基底手位覆写（clobber）----
ib = base['routes']['0']
iw = w['routes']['0']
clobber = []
for s in range(719):
    ab = base['actions'][ib[s]]
    aw = w['actions'][iw[s]]
    bh = ab.get('hands') or []
    nh = aw.get('hands') or []
    for k in range(min(len(bh), len(nh))):
        if bh[k] != nh[k]:
            clobber.append((s, k, bh[k], nh[k]))
print('base hand clobbers:', len(clobber))
for c in clobber[:12]:
    print('  ', c)

# ---- 排查点③：动物格 FEED 日丢失 ----
def feed_days(pkg, tile):
    tr = gl.Track(pkg, '0')
    d = collections.defaultdict(set)
    for s, u, op in tr.tile_visits().get(tile, []):
        d[s // 24].add(op)
    return {day: sorted(ops) for day, ops in sorted(d.items())}

lost_total = 0
for tile in sorted(bt | vt):
    fb = feed_days(base, tile)
    fw = feed_days(w, tile)
    lost = [d for d in fb if d not in fw or ('FEED' in fb[d] and 'FEED' not in fw[d])]
    if lost:
        lost_total += len(lost)
        print('tile', tile, 'lost feed days:', lost[:6])
print('lost feed-day count total:', lost_total)
srv.close()
