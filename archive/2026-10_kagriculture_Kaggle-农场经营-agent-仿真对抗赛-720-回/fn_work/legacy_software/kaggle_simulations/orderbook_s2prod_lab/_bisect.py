import sys, copy
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
vb = gl._rollout(base, '0', 780010, srv=srv)
print('base', dict(vb['held']))
tiles, _ = B.pick_coop_tiles(base, '0', 8)
INF = lambda d: 10 ** 6
Orig = ga.RouteEditor


class HiresOnly(Orig):
    def add_market(self, step, orders):
        keep = [o for o in orders if o and o[0] == 'HIRE']
        if keep:
            Orig.add_market(self, step, keep)


class NoPickupWheat(Orig):
    pass


def run(cls, tag, n=4):
    ga.RouteEditor = cls
    w = copy.deepcopy(base)
    tbl = []
    plan = B._route_plan(base, '0', n, tiles[:n])
    B.apply_route_s2(base, w, '0', plan, tbl, INF)
    v = gl._rollout(w, '0', 780010, srv=srv)
    bt = {tuple(x[:2]) for x in vb['tiles_with_animal']}
    vt = {tuple(x[:2]) for x in v['tiles_with_animal']}
    print(tag, dict(v['held']), 'lost', sorted(bt - vt),
          'placed', plan.get('placed'))
    ga.RouteEditor = Orig
    return w, plan


run(HiresOnly, 'A hires-only')
# B: ops without any PICKUP WHEAT (my hands never touch shed wheat)
import goose_additive as ga2


class OpsNoWheat(Orig):
    def add_market(self, step, orders):
        keep = [o for o in orders if o and o[0] == 'HIRE']
        if keep:
            Orig.add_market(self, step, keep)


# monkeypatch set_op to strip PICKUP WHEAT from my ops
_orig_set = Orig.set_op


def set_op_no_wheat(self, step, hand, op):
    if op and op[0] == 'PICKUP' and len(op) > 1 and op[1] == 'WHEAT':
        op = ['PASS']
    _orig_set(self, step, hand, op)


OpsNoWheat.set_op = set_op_no_wheat
run(OpsNoWheat, 'B ops-no-wheat-pickup')
# C: full but wheat buffer huge (60) at evening
B.WHEAT_BUFFER_QTY = 60
run(Orig, 'C full-buf60')
B.WHEAT_BUFFER_QTY = 8
srv.close()
