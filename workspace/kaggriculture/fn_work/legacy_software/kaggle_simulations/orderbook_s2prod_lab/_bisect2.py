import sys, copy, collections
from pathlib import Path
sys.path.insert(0, '..'); sys.path.insert(0, '../orderbook_goose_lab')
sys.path.insert(0, '../orderbook_goose_fullplan_lab')
sys.path.insert(0, '../orderbook_goose_add_lab'); sys.path.insert(0, '.')
from orderbook_r37 import retape_sheep as rs
import goose_line as gl, goose_additive as ga
import build_s2 as B

base = rs._decode_routes(Path('../orderbook_composite_lab/build/c_final/main.py').read_text())
B._load_pos(base, ['0'])
from kaggsim.serve import Serve
srv = Serve()
tiles, _ = B.pick_coop_tiles(base, '0', 8)
INF = lambda d: 10 ** 6
Orig = ga.RouteEditor
w = copy.deepcopy(base)
tbl = []
plan = B._route_plan(base, '0', 4, tiles[:4])
B.apply_route_s2(base, w, '0', plan, tbl, INF)


def feed_days(pkg, tile):
    tr = gl.Track(pkg, '0')
    d = collections.defaultdict(set)
    for s, u, op in tr.tile_visits().get(tile, []):
        d[s // 24].add(op)
    return {day: sorted(ops) for day, ops in sorted(d.items())}


for tile in [(4, 1), (6, 4), (2, 3)]:
    fb = feed_days(base, tile)
    fw = feed_days(w, tile)
    lost = [d for d in fb if d not in fw or ('FEED' in fb[d] and 'FEED' not in fw[d])]
    print('tile', tile, 'lost feed days:', lost)
    for d in lost[:3]:
        print('   base', d, fb.get(d), '| new', fw.get(d))
# hand-list lengths at steps where my ops wrote
ib = base['routes']['0']
iw = w['routes']['0']
changed = [s for s in range(719) if base['actions'][ib[s]] != w['actions'][iw[s]]]
clobber = []
for s in changed:
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
srv.close()
