"""fp.sched - optimizing receding-horizon SALE scheduler (Kaggriculture).  Original work, Shawn404, 28 Sep 2026.

Pure Python (no numpy, no engine import, no file access).  Uses tools/fp/fsim.py for the engine's exact quote curve
and the town drains.  Each turn it plans every sale of every item from now to the end of the game against the
forecast market path (our own future supply, the rival's expected sales, the drains) and sends only this turn's
SELL orders (receding horizon: the next turn re-plans with fresh observations).

OBJECTIVE (per item i, frozen rival forecast r_i(t), our supply a_i(t), drains d_i(t)):
    maximise   J = sum_t [ our revenue_i(t) ] - lam * sum_t [ rival revenue_i(t) ]
    subject to cumulative availability (a unit is sold only after it reached the shed), every unit sold by step
    718 or never (unsold = $0), shed capacity (load after the market + the next arrivals <= cap - margin until
    tonight's end-of-day drop), at most K SELL orders this turn.
  Market facts used (fsim / engine): the quote depends on the item's market inventory; a SELL adds +1 per unit sold
  above $1; drains subtract fixed amounts (shops every 4 steps, town centre every 24).  Hence a unit sold at step t
  raises the inventory of EVERY later step by 1 (permanent impact) and the loss it causes to a later lot of n units
  starting at inventory v telescopes to p(v) - p(v + n).  The marginal value of one more unit at slot k is
      MV_k = p(v_us_k + x_k)                                    the unit's own quote (behind our x_k units at k)
             - sum_{j>k} [p(v_us_j) - p(v_us_j + x_j)]           our later lots re-priced one unit down
             + lam * ( [p(v_rv_k) - p(v_rv_k + Rpost_k)]           the rival's same-slot units that trade after ours
                       + sum_{j>k} [rival pre + post lots re-priced] )
  with I_k = inv0 - drains(t0..s_k) + rival sales before s_k + our units before k, v_us_k = I_k + Rpre_k (rival
  units of step s_k that trade before ours: rho x r(s_k)), v_rv_k = v_us_k + x_k, Rpost_k = the rival's units of
  (s_k, s_{k+1}) plus (1 - rho) r(s_k).  (A unit at the $1 floor adds no inventory: MV = 1, no impact.)

METHOD (per turn, per item with stock now or any forecast arrival):
  slots: every step of the next `near` steps, then 4-step blocks (sale step = the first market after a shop tick,
  step % 4 == 1) until `mid` steps ahead, then one slot per day at hour `far_hour`, and the last market (718).
  Greedy marginal allocation: repeatedly give the next chunk of units to the feasible slot with the largest MV
  (feasible = the cumulative availability is never exceeded and the slot has a SELL order slot), ceil(stock / 8)
  units at slot 0 (the decision, refined unit by unit at the end), chunks of ceil(units / chunks) elsewhere; stop
  when the best MV <= min_mv (never sell a unit that is worth more unsold).
  Index: pass 1 plans every item with the rival first at every step (rho = 1: conservative); the item whose lead
  over the rival this step is worth most (our lot's price gain + lam x the rival's loss) gets index 0 and is
  re-planned with rho0 = rho_idx0 (0.5 = a tie at the same index: unit alternation); the other sells follow by value.
  Capacity (whole horizon): load after the market of s + the arrivals of s+1 <= cap - margin at every step until
  tonight's hour 23 (exact carried goods at hour 23) and <= cap - margin_future at hour 23 of every later day (day
  29: mid-day drops only); goods from the plans, non-goods held at today's level + each night's carried non-goods.
  Cash: cash + planned goods revenue - net purchase needs >= cash_floor at every step of `cash_need` (today and
  tomorrow's hours 0-1: the morning hires are paid before any sale slot opens).  Both are repaired by the cheapest
  moves of planned units to an earlier slot (move_candidate: a move from slot b to a needs spare availability on
  every slot of [a, b); cost = MV lost, per $ raised for cash).  room_guard() mirrors pd_market's protect-mode
  hour-23 guard as the layer's safety net.
  Order window: at most K SELL orders now (the caller merges purchases / hires / C9 rows); k_future marks the near
  steps without a free slot (e.g. hour 0 full of HIREs); the dropped items are re-planned next turn.

API
---
    from tools.fp.sched import SaleScheduler, room_guard, plan_value_item
    sch = SaleScheduler(lam=1.0, items=GOODS, near=12, mid=48, far_hour=13, chunks=12, cap=100, margin=4,
                        margin_future=10, rho_future=1.0, rho_idx0=0.5, min_mv=0.0, cont_items=('CARROT', 'WHEAT'),
                        cont_last_day=28, max_cap_moves=80)
    res = sch.decide(step, inv, shops, stock, arrivals=None, rival=None, K=10, shed_total=None, withdraw=None,
                     eod_arrivals=None, cont_rate=None, lam=None, drain_mode='expected', items=None, cash=None,
                     cash_need=None, cash_floor=0.0, k_future=None)
        step      obs step t0 being acted on (orders run in the market of t0)
        inv       {item: market inventory at t0} (obs.market.inventory);  shops = obs.town.unlocked_shops
        stock     {item: units we may sell now} = shed at MARKET time (after this turn's unit commands) minus the
                  caller's reserves / holds (WHEAT / FERTILIZER feed and FERTILIZE keeps)
        arrivals  {step: {item: units}} our goods first sellable at step (> t0), e.g. OwnForecast(obs).supply(H)
                  (the t0 entry is ignored: `stock` already holds this turn's drops)
        rival     {step: {item: units}} the rival's expected sales (RivalModel.forecast); None = no rival
        K         SELL orders allowed this turn (10 - the purchases / hires the caller keeps)
        shed_total units in the shed at market time, all items (reserves and animals included) - capacity pass;
                  None = no capacity pass
        withdraw  {step: {item: units}} planned pickups from the shed (feed wheat ...), capacity only
        eod_arrivals {item: units} exact goods the units carry into tonight's drop (hour 23: the layer knows them);
                  replaces the forecast arrivals at the next h0 for the capacity pass
        cont_rate {item: units/day}: continuation supply for short-cycle crops beyond the forecast's reach
                  (future plantings the own forecaster cannot see), added from day t0//24 + 3 until day 28
        k_future  {step: SELL order slots expected at that step} for the next steps (the caller's planned purchases
                  / hires fill the rest of the 10-order window); a step with 0 slots takes no planned sale
        lam       override of the rival weight for this call
        cash      our money now; cash_need = {step: net $ we pay at that step (planned purchases, hires, land minus
                  our other sales), today and optionally tomorrow's hours 0-1 (morning hires come before any sale
                  slot)}: planned goods sales keep cash + revenue - need >= cash_floor over those steps
      -> {'orders': [['SELL', item, n], ...] (index order, <= K), 'now': {item: n}, 'idx0': item or None,
          'plan': {item: [(slot_step, units), ...]}, 'mv': {item: MV at slot 0},
          'cap': {'violations': n, 'moves': n, 'load_max': x}, 'cash': {'violations': n, 'moves': n}, 'ms': cpu ms}
    room_guard(sells, shed1, carried_end, levels=None, cap_target=96, order=None)
        -> sells + the units pd_market's 'protect' guard (room_hinge_last True) would add at hour 23 so that
           shed after the market + tonight's drop <= cap_target (EGG / WHEAT / FERT above level, protected WHEAT /
           FERT, CARROT / TOMATO, then MELON, WOOL, MILK, STRAWBERRY); order = custom passes [(item, level), ...].
    make_slots(t0, ...), drain_path(inv, shops, t0, t1), lot_value(item, v, n), warm()
    plan_value_item(item, Ib, Rpre, Rpost, x, lam): exact engine-walk value of one item's slot plan (tests).

CPU: decide() mean ~8-10 ms, p95 ~13-16 ms, max ~70 ms on recorded games (with the forecasts ~15-18 ms per turn);
tests tools/tmp/fp/sched/test_sched.py / test_hook.py, value and profile in results/portable/fp_sched.txt.
No look-ahead: decide() uses only its arguments (the observation, our own forecasts / plan, the rival forecast).
"""
import math
import time
try:
    from . import fsim as _fsim
except ImportError:
    try:
        import fp_fsim as _fsim
    except ImportError:
        import fsim as _fsim
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
GOODS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
LAST = 718
TPD = 24
I0 = 10000
_LO, _HI = (5000, 17000)
_TAB = {}

def _tab(item):
    t = _TAB.get(item)
    if t is None:
        rp = _fsim._raw_price
        t = [rp(item, _q1233) for _q1233 in range(_LO, _HI + 1)]
        _TAB[item] = t
    return t

def warm(items=PRODUCTS):
    """Build the quote tables (about 0.1 s for all 9 items; call once at agent load)."""
    for it in items:
        _tab(it)

def _pf_factory(item):
    """-> pf(v): the engine quote at a (possibly fractional) inventory, linearly interpolated between integers."""
    t = _tab(item)
    lo, hi = (_LO, _HI)
    rp = _fsim._raw_price

    def pf(_q1233):
        _q712 = int(_q1233) if _q1233 >= 0 else int(_q1233) - 1
        if lo <= _q712 < hi:
            a = t[_q712 - lo]
            f = _q1233 - _q712
            return a + f * (t[_q712 - lo + 1] - a) if f else a
        a = rp(item, _q712)
        f = _q1233 - _q712
        return a + f * (rp(item, _q712 + 1) - a) if f else a
    return pf

def lot_value(item, _q1233, n):
    """Revenue of an integer lot of n units sold alone from inventory v (engine walk, $1 units add nothing)."""
    return _fsim.sell_walk(item, int(n), int(round(_q1233)))[0]

def make_slots(t0, _q894=12, _q836=48, _q606=13, _q785=LAST):
    """Sale steps of the plan: t0 .. t0+near-1, then steps % 4 == 1 until t0+mid, then one per day at far_hour,
    then `last`.  Returns a sorted list of distinct steps in [t0, last]."""
    s = []
    t = t0
    _q586 = min(_q785, t0 + _q894 - 1)
    while t <= _q586:
        s.append(t)
        t += 1
    t = _q586 + 1
    _q585 = min(_q785, t0 + _q836)
    while t <= _q585:
        if t % 4 == 1:
            s.append(t)
        t += 1
    _q530 = _q585 // TPD
    while True:
        _q1221 = _q530 * TPD + _q606
        if _q1221 > _q785:
            break
        if _q1221 > _q585:
            s.append(_q1221)
        _q530 += 1
    if not s or s[-1] != _q785:
        if _q785 >= t0 and (not s or s[-1] < _q785):
            s.append(_q785)
    return s

def drain_path(inv, shops, t0, _q1177, drain_mode='expected'):
    """Cumulative drains per item: {item: [D(t0), D(t0+1), ..., D(t1)]} where D(t) = units drained after the
    markets of steps t0..t-1 (fsim drain schedule; unknown future shops by drain_mode)."""
    _q1133 = _fsim.MarketSim(dict(inv), list(shops or []), t0, drain_mode=drain_mode)
    base = dict(_q1133.inv)
    _q946 = {it: [0.0] for it in PRODUCTS}
    t = t0
    while t < _q1177:
        _q1133.drain()
        t += 1
        for it in PRODUCTS:
            _q946[it].append(base[it] - _q1133.inv[it])
    return _q946

class _ItemPlan:
    """Greedy marginal allocation of one item's units over the slot grid (see the module docstring)."""
    __slots__ = ('item', 'n', 'pf', 'Ib', 'Rpre', 'Rpost', 'avail', 'x', 'lam', 'I', 'mv', 'so', 'sr', 'olos', 'rlos', 'rpost', 'total', 'blocked')

    def __init__(_q1120, item, Ib, Rpre, Rpost, avail, lam, blocked=None):
        _q1120.item = item
        _q1120.n = len(Ib)
        _q1120.pf = _pf_factory(item)
        _q1120.Ib = Ib
        _q1120.Rpre = Rpre
        _q1120.Rpost = Rpost
        _q1120.avail = avail
        _q1120.x = [0] * _q1120.n
        _q1120.lam = lam
        _q1120.total = 0
        _q1120.blocked = blocked or [False] * _q1120.n

    def evaluate(_q1120):
        """Recompute I, losses, suffix sums and MVs for all slots (O(n) quotes)."""
        n, pf, x, lam = (_q1120.n, _q1120.pf, _q1120.x, _q1120.lam)
        Ib, Rpre, Rpost = (_q1120.Ib, _q1120.Rpre, _q1120.Rpost)
        I = [0.0] * n
        olos = [0.0] * n
        rlos = [0.0] * n
        rpost = [0.0] * n
        cum = 0
        for k in range(n):
            _q718 = Ib[k] + cum
            I[k] = _q718
            rp = Rpre[k]
            _q1240 = _q718 + rp
            _q1271 = x[k]
            if _q1271:
                a = pf(_q1240)
                olos[k] = a - pf(_q1240 + _q1271) if a > 1 else 0.0
            _q1238 = _q1240 + _q1271
            _q1081 = Rpost[k]
            _q1038 = 0.0
            if rp > 1e-09:
                a = pf(_q718)
                if a > 1:
                    _q1038 = a - pf(_q718 + rp)
            _q1039 = 0.0
            if _q1081 > 1e-09:
                a = pf(_q1238)
                if a > 1:
                    _q1039 = a - pf(_q1238 + _q1081)
            rlos[k] = _q1038 + _q1039
            rpost[k] = _q1039
            cum += _q1271
        so = [0.0] * n
        sr = [0.0] * n
        _q370 = _q371 = 0.0
        for k in range(n - 1, -1, -1):
            so[k] = _q370
            sr[k] = _q371
            _q370 += olos[k]
            _q371 += rlos[k]
        mv = [0.0] * n
        for k in range(n):
            q = pf(I[k] + Rpre[k] + x[k])
            if q <= 1.0:
                mv[k] = q
            else:
                mv[k] = q - so[k] + lam * (rpost[k] + sr[k])
        _q1120.I, _q1120.olos, _q1120.rlos, _q1120.rpost, _q1120.so, _q1120.sr, _q1120.mv = (I, olos, rlos, rpost, so, sr, mv)

    def slack_suffix_min(_q1120):
        """min over j >= k of (avail[j] - X_cum[j]) for every k."""
        n, x, _q397 = (_q1120.n, _q1120.x, _q1120.avail)
        _q1136 = [0] * n
        cum = 0
        for k in range(n):
            cum += x[k]
            _q1136[k] = _q397[k] - cum
        _q946 = [0] * n
        m = 10 ** 9
        for k in range(n - 1, -1, -1):
            if _q1136[k] < m:
                m = _q1136[k]
            _q946[k] = m
        return _q946

    def greedy(_q1120, _q485, _q838=0.0, _q828=400, _q630=None, chunk0=1):
        """Allocate units in MV order: chunk0 units at a time at slot 0 (the decision), `chunk` elsewhere; the
        last slot-0 steps are refined unit by unit.  fix0 = force the slot-0 quantity.  Returns iterations."""
        it = 0
        x = _q1120.x
        if _q630 is not None:
            x[0] = int(_q630)
        _q447 = max(1, int(chunk0))
        while it < _q828:
            it += 1
            _q1120.evaluate()
            _q1143 = _q1120.slack_suffix_min()
            best = -1e+18
            _q417 = -1
            mv = _q1120.mv
            _q419 = _q1120.blocked
            for k in range(_q1120.n):
                if k == 0 and _q630 is not None or _q419[k]:
                    continue
                if _q1143[k] >= 1 and mv[k] > best:
                    best = mv[k]
                    _q417 = k
            if _q417 < 0 or best <= _q838:
                if _q447 > 1 and x[0] > 0 and (_q630 is None):
                    _q401 = min(_q447 - 1, x[0])
                    x[0] -= _q401
                    _q1120.total -= _q401
                    _q447 = 1
                    continue
                break
            c = min(_q447, _q1143[0]) if _q417 == 0 else min(_q485, _q1143[_q417])
            if c < 1:
                c = 1
            x[_q417] += c
            _q1120.total += c
        _q1120.evaluate()
        return it

    def move_candidate(_q1120, _q771):
        """Best single-unit move of this item that raises its sales at slots <= km: the least valuable source
        (an allocated slot b > km, or an unsold unit) that can reach a slot a <= km without crossing a slot whose
        availability is fully used (a unit moved from b to a needs slack >= 1 on every slot of [a, b)), and the most
        valuable target a <= km.  Returns (src or None, src_mv, tgt, tgt_mv, room) or None."""
        n, x, _q397, mv = (_q1120.n, _q1120.x, _q1120.avail, _q1120.mv)
        if _q771 < 0:
            return None
        _q1136 = [0] * n
        cum = 0
        for k in range(n):
            cum += x[k]
            _q1136[k] = _q397[k] - cum
        _q813 = [0] * (_q771 + 1)
        m = 10 ** 9
        for k in range(_q771, -1, -1):
            if _q1136[k] < m:
                m = _q1136[k]
            _q813[k] = m
        _q1193 = None
        _q419 = _q1120.blocked
        for k in range(_q771 + 1):
            if _q813[k] >= 1 and (not _q419[k]) and (_q1193 is None or mv[k] > mv[_q1193]):
                _q1193 = k
        if _q1193 is None:
            return None
        best = None
        _q997 = 10 ** 9
        for b in range(_q771 + 1, n):
            if _q997 < 1:
                break
            if x[b] > 0 and (best is None or mv[b] < best[1]):
                best = (b, mv[b], min(_q997, x[b]))
            if _q1136[b] < _q997:
                _q997 = _q1136[b]
        src, _q1155, _q1083 = (None, 0.0, _q997) if best is None else best
        if best is not None and _q997 >= 1 and (0.0 < _q1155):
            src, _q1155, _q1083 = (None, 0.0, _q997)
        if src is None and _q997 < 1:
            return None
        room = min(_q813[_q1193], _q1083)
        if room < 1:
            return None
        return (src, _q1155, _q1193, mv[_q1193], int(room))

    def last_unit_mv(_q1120, k):
        """MV of the last unit placed at slot k (what removing it loses), with the current allocation."""
        if _q1120.x[k] <= 0:
            return None
        _q1120.x[k] -= 1
        _q1120.evaluate()
        _q1233 = _q1120.mv[k]
        _q1120.x[k] += 1
        return _q1233

def plan_value_item(item, Ib, Rpre, Rpost, x, lam=1.0):
    """Exact (engine-walk) value of one item's slot plan x against a frozen rival: returns (own $, rival $,
    own - lam * rival).  Rival lots are rounded to integers (tests / diagnostics)."""
    own = _q1072 = 0.0
    cum = 0
    for k in range(len(x)):
        _q718 = Ib[k] + cum
        rp = int(round(Rpre[k]))
        _q1081 = int(round(Rpost[k]))
        _q1038, _q1233 = _fsim.sell_walk(item, rp, int(round(_q718)))
        _q922, _q1233 = _fsim.sell_walk(item, int(x[k]), _q1233)
        _q1039, _q1233 = _fsim.sell_walk(item, _q1081, _q1233)
        own += _q922
        _q1072 += _q1038 + _q1039
        cum += x[k]
    return (own, _q1072, own - lam * _q1072)

class SaleScheduler:

    def __init__(_q1120, lam=1.0, items=GOODS, _q894=12, _q836=48, _q606=13, _q486=12, cap=100, margin=4, _q1070=1.0, _q1071=0.5, _q838=0.0, _q504=('CARROT', 'WHEAT'), _q505=28, _q826=10, _q827=80):
        _q1120.lam = float(lam)
        _q1120.items = tuple(items)
        _q1120.near = int(_q894)
        _q1120.mid = int(_q836)
        _q1120.far_hour = int(_q606)
        _q1120.chunks = max(1, int(_q486))
        _q1120.cap = int(cap)
        _q1120.margin = int(margin)
        _q1120.rho_future = float(_q1070)
        _q1120.rho_idx0 = float(_q1071)
        _q1120.min_mv = float(_q838)
        _q1120.cont_items = tuple(_q504 or ())
        _q1120.cont_last_day = int(_q505)
        _q1120.margin_future = int(_q826)
        _q1120.max_cap_moves = int(_q827)
        _q1120.stats = {'calls': 0, 'ms_sum': 0.0, 'ms_max': 0.0}
        warm(_q1120.items)

    def _item_inputs(_q1120, it, _q1140, t0, _q729, _q538, rival, arrivals, _q1166, _q1069, cont_rate):
        n = len(_q1140)
        _q1036 = [0.0] * (_q1140[-1] - t0 + 1)
        if rival:
            for s, _q1086 in rival.items():
                if t0 <= s <= _q1140[-1]:
                    _q1233 = _q1086.get(it)
                    if _q1233:
                        _q1036[s - t0] += float(_q1233)
        a = [0.0] * (_q1140[-1] - t0 + 1)
        if arrivals:
            for s, _q1086 in arrivals.items():
                if t0 < s <= _q1140[-1]:
                    _q1233 = _q1086.get(it)
                    if _q1233:
                        a[s - t0] += float(_q1233)
        _q513 = float((cont_rate or {}).get(it, 0.0) or 0.0)
        if _q513 > 0 and it in _q1120.cont_items:
            _q531 = t0 // TPD + 3
            for _q530 in range(_q531, _q1120.cont_last_day + 1):
                s = _q530 * TPD
                if t0 < s <= _q1140[-1]:
                    a[s - t0] += _q513
        Ib = [0.0] * n
        Rpre = [0.0] * n
        Rpost = [0.0] * n
        avail = [0] * n
        _q521 = 0.0
        _q519 = float(_q1166)
        prev = t0
        for k in range(n):
            _q1134 = _q1140[k]
            Ib[k] = _q729 - _q538[_q1134 - t0] + _q521
            _q1068 = _q1069 if k == 0 else _q1120.rho_future
            _q1077 = _q1036[_q1134 - t0]
            Rpre[k] = _q1068 * _q1077
            _q921 = _q1140[k + 1] if k + 1 < n else _q1140[-1] + 1
            _q1007 = (1.0 - _q1068) * _q1077
            for s in range(_q1134 + 1, _q921):
                if s - t0 < len(_q1036):
                    _q1007 += _q1036[s - t0]
            Rpost[k] = _q1007
            _q521 += _q1077 + (_q1007 - (1.0 - _q1068) * _q1077)
            if k > 0:
                for s in range(prev + 1, _q1134 + 1):
                    _q519 += a[s - t0]
            avail[k] = int(math.floor(_q519 + 0.5))
            prev = _q1134
        avail[0] = int(_q1166)
        for k in range(1, n):
            if avail[k] < avail[k - 1]:
                avail[k] = avail[k - 1]
        return (Ib, Rpre, Rpost, avail)

    def decide(_q1120, step, inv, shops, stock, arrivals=None, rival=None, K=10, shed_total=None, _q1257=None, eod_arrivals=None, cont_rate=None, lam=None, drain_mode='expected', items=None, cash=None, cash_need=None, cash_floor=0.0, k_future=None):
        _q1182 = time.perf_counter()
        t0 = int(step)
        lam = _q1120.lam if lam is None else float(lam)
        items = _q1120.items if items is None else tuple(items)
        K = int(K if K is not None else 10)
        _q946 = {'orders': [], 'now': {}, 'idx0': None, 'plan': {}, 'mv': {}, 'cap': {'violations': 0, 'moves': 0, 'load_max': None}, 'cash': {'violations': 0, 'moves': 0}, 'ms': 0.0}
        if t0 > LAST:
            return _q946
        _q1140 = make_slots(t0, _q1120.near, _q1120.mid, _q1120.far_hour)
        _q538 = drain_path(inv, shops, t0, _q1140[-1] + 1, drain_mode)
        _q766 = k_future or {}
        blocked = [K <= 0 if k == 0 else int(_q766.get(_q1134, 10)) <= 0 for k, _q1134 in enumerate(_q1140)]
        _q992 = {}
        _q1207 = {}
        if arrivals:
            for s, _q1086 in arrivals.items():
                if t0 < s <= _q1140[-1] and _q1086:
                    for it, _q1233 in _q1086.items():
                        _q1207[it] = _q1207.get(it, 0.0) + float(_q1233 or 0.0)
        for it in items:
            _q1099 = int(stock.get(it, 0) or 0)
            _q658 = _q1207.get(it, 0.0) + (float((cont_rate or {}).get(it, 0.0) or 0.0) if it in _q1120.cont_items else 0.0)
            if _q1099 <= 0 and (shed_total is None or _q658 < 0.5):
                continue
            Ib, Rpre, Rpost, avail = _q1120._item_inputs(it, _q1140, t0, float(inv.get(it, I0)), _q538[it], rival, arrivals, _q1099, 1.0, cont_rate)
            _q32 = _ItemPlan(it, Ib, Rpre, Rpost, avail, lam, blocked)
            U = avail[-1]
            _q485 = max(1, int(math.ceil(U / float(_q1120.chunks))))
            _q32.greedy(_q485, _q1120.min_mv, chunk0=max(1, int(math.ceil(_q1099 / 8.0))))
            _q992[it] = [_q32, _q485, _q1099]
        _q409, idx0 = (0.0, None)
        for it, (_q32, _q485, _q1099) in _q992.items():
            _q1266 = _q32.x[0]
            _q1037 = _q32.Rpre[0]
            if _q1099 <= 0 or _q1037 < 0.05:
                continue
            _q1269 = _q1266 if _q1266 > 0 else min(_q1099, 6)
            pf = _q32.pf
            I = _q32.I[0]
            _q662 = 0.0
            for _q743 in range(_q1269):
                _q662 += pf(I + _q743) - pf(I + _q1037 + _q743)
            _q663 = _q1037 * (pf(I + 0.5 * _q1037) - pf(I + _q1269 + 0.5 * _q1037))
            _q664 = _q662 + lam * _q663
            if _q664 > _q409:
                _q409, idx0 = (_q664, it)
        if idx0 is not None and _q1120.rho_idx0 < 1.0:
            _q33, _q485, _q1099 = _q992[idx0]
            Ib, Rpre, Rpost, avail = _q1120._item_inputs(idx0, _q1140, t0, float(inv.get(idx0, I0)), _q538[idx0], rival, arrivals, _q1099, _q1120.rho_idx0, cont_rate)
            _q32 = _ItemPlan(idx0, Ib, Rpre, Rpost, avail, lam, blocked)
            _q32.greedy(_q485, _q1120.min_mv, chunk0=max(1, int(math.ceil(_q1099 / 8.0))))
            _q992[idx0][0] = _q32
        if shed_total is not None:
            _q669 = sum((int(stock.get(it, 0) or 0) for it in _q992))
            _q1120._capacity(_q992, _q1140, t0, shed_total, _q669, arrivals, _q1257, eod_arrivals, _q946)
        if cash is not None and cash_need:
            _q1120._cash(_q992, _q1140, t0, float(cash), cash_need, float(cash_floor), _q946)
        now = {}
        for it, (_q32, _q485, _q1099) in _q992.items():
            _q1266 = min(_q32.x[0], _q1099)
            if _q1266 > 0:
                now[it] = _q1266
            _q946['plan'][it] = [(_q1140[k], _q32.x[k]) for k in range(_q32.n) if _q32.x[k]]
            _q946['mv'][it] = _q32.mv[0]
        if K <= 0:
            now = {}
        _q938 = []
        for it, n in now.items():
            _q32 = _q992[it][0]
            pf = _q32.pf
            _q1233 = _q32.I[0] + _q32.Rpre[0]
            val = 0.0
            for _q743 in range(n):
                val += pf(_q1233 + _q743)
            _q938.append((0 if it == idx0 else 1, -val, PRODUCTS.index(it), it, n))
        _q938.sort()
        _q938 = _q938[:max(0, K)]
        _q946['orders'] = [['SELL', it, int(n)] for _, _, _, it, n in _q938]
        _q946['now'] = {it: int(n) for _, _, _, it, n in _q938}
        _q946['idx0'] = idx0 if idx0 in _q946['now'] else None
        ms = (time.perf_counter() - _q1182) * 1000.0
        _q946['ms'] = ms
        st = _q1120.stats
        st['calls'] += 1
        st['ms_sum'] += ms
        if ms > st['ms_max']:
            st['ms_max'] = ms
        return _q946

    def _capacity(_q1120, _q992, _q1140, t0, shed_total, _q669, arrivals, _q1257, eod_arrivals, _q946):
        """Shed capacity over the whole horizon (module docstring).  Load after the market of step s plus the
        arrivals of s+1:  load(s) = NG + goods_now + goods arrivals (t0, s+1] - planned goods sales (<= s)
        + [s = hour 23] x the night's non-goods arrivals (the carried WHEAT / FERTILIZER of the end-of-day drop).
        NG = the non-goods units in the shed now (reserves, animals: assumed to stay at this level).  Checked at
        every step until tonight's hour 23 (cap - margin) and at hour 23 of every later day <= 28
        (cap - margin_future).  Violations are repaired by the cheapest moves of planned goods units to an
        earlier slot (cost = MV lost)."""
        _q536 = t0 // TPD
        _q908 = float(shed_total) - float(_q669)
        _q673 = set(_q992)
        _q787 = _q1140[-1]
        _q364 = {}
        _q365 = {}
        if arrivals:
            for s, _q1086 in arrivals.items():
                if t0 < s <= _q787 + 1 and _q1086:
                    g = n = 0.0
                    for it, _q1233 in _q1086.items():
                        if it in _q673:
                            g += float(_q1233 or 0.0)
                        else:
                            n += float(_q1233 or 0.0)
                    _q364[s] = g
                    _q365[s] = n
        _q576 = _q536 * TPD + 23 if _q536 < 29 else LAST
        if eod_arrivals is not None and t0 <= _q576 and (_q536 < 29):
            _q364[_q576 + 1] = float(sum((_q1233 for it, _q1233 in eod_arrivals.items() if it in _q673)))
            _q365[_q576 + 1] = float(sum((_q1233 for it, _q1233 in eod_arrivals.items() if it not in _q673)))
        _q503 = [(s, _q1120.margin, s == _q576 and _q536 < 29) for s in range(t0, min(_q576, LAST) + 1)]
        _q503 += [(_q530 * TPD + 23, _q1120.margin_future, True) for _q530 in range(_q536 + 1, 29)]
        _q858 = len(_q1140)

        def _q773(s):
            if _q1140[0] > s:
                return -1
            lo, hi = (0, _q858 - 1)
            while lo < hi:
                _q836 = (lo + hi + 1) // 2
                if _q1140[_q836] <= s:
                    lo = _q836
                else:
                    hi = _q836 - 1
            return lo
        _q380 = sorted(_q364)
        moves = _q1236 = 0
        load_max = -1e+18
        for s, _q825, _q910 in _q503:
            _q771 = _q773(s)
            if _q771 < 0:
                continue
            _q460 = float(_q1120.cap - _q825)
            _q393 = 0.0
            for _q1157 in _q380:
                if _q1157 > s + 1:
                    break
                _q393 += _q364[_q1157]
            _q598 = _q365.get(s + 1, 0.0) if _q910 else 0.0
            while True:
                sold = 0
                for it, _q988 in _q992.items():
                    x = _q988[0].x
                    for k in range(_q771 + 1):
                        sold += x[k]
                load = _q908 + float(_q669) + _q393 - sold + _q598
                _q542 = load - _q460
                if _q542 <= 1e-09 or moves >= _q1120.max_cap_moves:
                    if load > load_max:
                        load_max = load
                    break
                _q1236 += 1
                best = None
                for it, _q988 in _q992.items():
                    _q832 = _q988[0].move_candidate(_q771)
                    if _q832 is None:
                        continue
                    src, _q1155, _q1193, _q1194, room = _q832
                    cost = _q1155 - _q1194
                    if best is None or cost < best[0]:
                        best = (cost, it, src, _q1193, room)
                if best is None:
                    if load > load_max:
                        load_max = load
                    break
                cost, it, src, _q1193, room = best
                c = int(max(1, min(room, math.ceil(_q542), _q992[it][1])))
                _q32 = _q992[it][0]
                if src is not None:
                    _q32.x[src] -= c
                else:
                    _q32.total += c
                _q32.x[_q1193] += c
                _q32.evaluate()
                moves += 1
        _q946['cap']['violations'] = _q1236
        _q946['cap']['moves'] = moves
        _q946['cap']['load_max'] = load_max

    def _cash(_q1120, _q992, _q1140, t0, cash, need, floor, _q946):
        """Funding constraint: for every step s from t0 to tonight's hour 23 (the last market on day 29) or to the
        last step in `need` (e.g. tomorrow's hours 0-1: the morning hires are paid before any sale slot opens),
        cash + planned goods revenue (slots <= s) - sum(need[t0..s]) >= floor.  need = {step: net $ the caller
        pays at that step (planned purchases / hires / land minus its other sales)}.  Revenue of a planned lot ~
        x * quote(middle of the lot).  Violations are repaired by moving planned goods units to an earlier slot
        (or selling unsold ones) at the least MV cost per $ raised."""
        _q536 = t0 // TPD
        _q576 = _q536 * TPD + 23 if _q536 < 29 else LAST
        _q577 = max([_q576] + [int(k) for k in need if int(k) >= t0])
        steps = [s for s in range(t0, min(_q577, LAST) + 1)]
        _q520 = []
        _q369 = 0.0
        for s in steps:
            _q369 += float(need.get(s, 0.0) or 0.0)
            _q520.append(_q369)
        if not steps or max(_q520) <= cash - floor:
            return
        _q858 = len(_q1140)

        def _q773(s):
            if _q1140[0] > s:
                return -1
            lo, hi = (0, _q858 - 1)
            while lo < hi:
                _q836 = (lo + hi + 1) // 2
                if _q1140[_q836] <= s:
                    lo = _q836
                else:
                    hi = _q836 - 1
            return lo

        def _q1065(_q771):
            _q1206 = 0.0
            for it, _q988 in _q992.items():
                _q32 = _q988[0]
                for k in range(_q771 + 1):
                    _q1271 = _q32.x[k]
                    if _q1271:
                        _q1206 += _q1271 * _q32.pf(_q32.I[k] + _q32.Rpre[k] + 0.5 * _q1271)
            return _q1206
        moves = _q1236 = 0
        for _q712, s in enumerate(steps):
            _q771 = _q773(s)
            if _q771 < 0:
                continue
            while True:
                _q665 = _q520[_q712] - cash + floor - _q1065(_q771)
                if _q665 <= 1e-06 or moves >= _q1120.max_cap_moves:
                    break
                _q1236 += 1
                best = None
                for it, _q988 in _q992.items():
                    _q32 = _q988[0]
                    _q832 = _q32.move_candidate(_q771)
                    if _q832 is None:
                        continue
                    src, _q1155, _q1193, _q1194, room = _q832
                    q = _q32.pf(_q32.I[_q1193] + _q32.Rpre[_q1193] + _q32.x[_q1193])
                    if q <= 1.0:
                        continue
                    cost = (_q1155 - _q1194) / q
                    if best is None or cost < best[0]:
                        best = (cost, it, src, _q1193, room, q)
                if best is None:
                    break
                cost, it, src, _q1193, room, q = best
                c = int(max(1, min(room, math.ceil(_q665 / q))))
                _q32 = _q992[it][0]
                if src is not None:
                    _q32.x[src] -= c
                else:
                    _q32.total += c
                _q32.x[_q1193] += c
                _q32.evaluate()
                moves += 1
        _q946['cash']['violations'] = _q1236
        _q946['cash']['moves'] = moves

def room_guard(sells, _q1125, carried_end, levels=None, cap_target=96, hinge=('TOMATO', 'CARROT'), _q938=None):
    """Hour-23 safety net (pd_market 'protect' guard with room_hinge_last True): add SELL units until the shed
    after this market plus tonight's drop fits cap_target.  sells = [['SELL', item, n], ...] (not mutated);
    levels = {item: protected units} for WHEAT / FERTILIZER (tomorrow's feed leg / FERTILIZE earmark).
    Pass order: EGG + WHEAT / FERTILIZER above their protected level, the protected WHEAT / FERTILIZER, CARROT /
    TOMATO, then MELON, WOOL, MILK, STRAWBERRY.  Returns a new list (added units merged into existing orders,
    new orders appended)."""
    _q819 = levels or {}
    sold = {}
    for _q922 in sells:
        sold[_q922[1]] = sold.get(_q922[1], 0) + int(_q922[2])
    after = sum((int(_q1233) for k, _q1233 in _q1125.items())) - sum((min(sold.get(k, 0), int(_q1125.get(k, 0))) for k in sold))
    _q947 = after + int(carried_end) - int(cap_target)
    if _q947 <= 0:
        return [list(_q922) for _q922 in sells]
    _q969 = _q938 or ([(it, _q819.get(it, 0)) for it in ('EGG', 'FERTILIZER', 'WHEAT')], [('WHEAT', 0), ('FERTILIZER', 0)], [(it, 0) for it in ('CARROT', 'TOMATO')], [(it, 0) for it in ('MELON', 'WOOL', 'MILK', 'STRAWBERRY')])
    _q376 = {}
    for _q671 in _q969:
        for it, level in _q671:
            if _q947 <= 0:
                break
            _q688 = int(_q1125.get(it, 0)) - sold.get(it, 0) - _q376.get(it, 0) - int(level)
            k = min(max(0, _q688), _q947)
            if k > 0:
                _q376[it] = _q376.get(it, 0) + k
                _q947 -= k
    _q1060 = []
    for _q922 in sells:
        _q925 = list(_q922)
        if _q925[1] in _q376:
            _q925[2] = int(_q925[2]) + _q376.pop(_q925[1])
        _q1060.append(_q925)
    for it, k in _q376.items():
        _q1060.append(['SELL', it, int(k)])
    return _q1060