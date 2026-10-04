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
        t = [rp(item, _q1159) for _q1159 in range(_LO, _HI + 1)]
        _TAB[item] = t
    return t

def warm(items=PRODUCTS):
    """Build the quote tables (about 0.1 s for all 9 items; call once at agent load)."""
    for _q675 in items:
        _tab(_q675)

def _pf_factory(item):
    """-> pf(v): the engine quote at a (possibly fractional) inventory, linearly interpolated between integers."""
    t = _tab(item)
    lo, hi = (_LO, _HI)
    rp = _fsim._raw_price

    def pf(_q1159):
        _q652 = int(_q1159) if _q1159 >= 0 else int(_q1159) - 1
        if lo <= _q652 < hi:
            a = t[_q652 - lo]
            f = _q1159 - _q652
            return a + f * (t[_q652 - lo + 1] - a) if f else a
        a = rp(item, _q652)
        f = _q1159 - _q652
        return a + f * (rp(item, _q652 + 1) - a) if f else a
    return pf

def lot_value(item, _q1159, n):
    """Revenue of an integer lot of n units sold alone from inventory v (engine walk, $1 units add nothing)."""
    return _fsim.sell_walk(item, int(n), int(round(_q1159)))[0]

def make_slots(t0, _q830=12, _q774=48, _q551=13, _q723=LAST):
    """Sale steps of the plan: t0 .. t0+near-1, then steps % 4 == 1 until t0+mid, then one per day at far_hour,
    then `last`.  Returns a sorted list of distinct steps in [t0, last]."""
    s = []
    t = t0
    _q531 = min(_q723, t0 + _q830 - 1)
    while t <= _q531:
        s.append(t)
        t += 1
    t = _q531 + 1
    _q530 = min(_q723, t0 + _q774)
    while t <= _q530:
        if t % 4 == 1:
            s.append(t)
        t += 1
    _q475 = _q530 // TPD
    while True:
        _q1147 = _q475 * TPD + _q551
        if _q1147 > _q723:
            break
        if _q1147 > _q530:
            s.append(_q1147)
        _q475 += 1
    if not s or s[-1] != _q723:
        if _q723 >= t0 and (not s or s[-1] < _q723):
            s.append(_q723)
    return s

def drain_path(inv, shops, t0, _q1106, drain_mode='expected'):
    """Cumulative drains per item: {item: [D(t0), D(t0+1), ..., D(t1)]} where D(t) = units drained after the
    markets of steps t0..t-1 (fsim drain schedule; unknown future shops by drain_mode)."""
    _q1063 = _fsim.MarketSim(dict(inv), list(shops or []), t0, drain_mode=drain_mode)
    base = dict(_q1063.inv)
    _q880 = {_q675: [0.0] for _q675 in PRODUCTS}
    t = t0
    while t < _q1106:
        _q1063.drain()
        t += 1
        for _q675 in PRODUCTS:
            _q880[_q675].append(base[_q675] - _q1063.inv[_q675])
    return _q880

class _ItemPlan:
    """Greedy marginal allocation of one item's units over the slot grid (see the module docstring)."""
    __slots__ = ('item', 'n', 'pf', 'Ib', 'Rpre', 'Rpost', 'avail', 'x', 'lam', 'I', 'mv', 'so', 'sr', 'olos', 'rlos', 'rpost', 'total', 'blocked')

    def __init__(_q1052, item, Ib, Rpre, Rpost, avail, lam, blocked=None):
        _q1052.item = item
        _q1052.n = len(Ib)
        _q1052.pf = _pf_factory(item)
        _q1052.Ib = Ib
        _q1052.Rpre = Rpre
        _q1052.Rpost = Rpost
        _q1052.avail = avail
        _q1052.x = [0] * _q1052.n
        _q1052.lam = lam
        _q1052.total = 0
        _q1052.blocked = blocked or [False] * _q1052.n

    def evaluate(_q1052):
        """Recompute I, losses, suffix sums and MVs for all slots (O(n) quotes)."""
        n, pf, x, lam = (_q1052.n, _q1052.pf, _q1052.x, _q1052.lam)
        Ib, Rpre, Rpost = (_q1052.Ib, _q1052.Rpre, _q1052.Rpost)
        I = [0.0] * n
        olos = [0.0] * n
        rlos = [0.0] * n
        rpost = [0.0] * n
        cum = 0
        for k in range(n):
            _q657 = Ib[k] + cum
            I[k] = _q657
            rp = Rpre[k]
            _q1165 = _q657 + rp
            _q1196 = x[k]
            if _q1196:
                a = pf(_q1165)
                olos[k] = a - pf(_q1165 + _q1196) if a > 1 else 0.0
            _q1163 = _q1165 + _q1196
            _q1013 = Rpost[k]
            _q972 = 0.0
            if rp > 1e-09:
                a = pf(_q657)
                if a > 1:
                    _q972 = a - pf(_q657 + rp)
            _q973 = 0.0
            if _q1013 > 1e-09:
                a = pf(_q1163)
                if a > 1:
                    _q973 = a - pf(_q1163 + _q1013)
            rlos[k] = _q972 + _q973
            rpost[k] = _q973
            cum += _q1196
        so = [0.0] * n
        sr = [0.0] * n
        _q320 = _q321 = 0.0
        for k in range(n - 1, -1, -1):
            so[k] = _q320
            sr[k] = _q321
            _q320 += olos[k]
            _q321 += rlos[k]
        mv = [0.0] * n
        for k in range(n):
            q = pf(I[k] + Rpre[k] + x[k])
            if q <= 1.0:
                mv[k] = q
            else:
                mv[k] = q - so[k] + lam * (rpost[k] + sr[k])
        _q1052.I, _q1052.olos, _q1052.rlos, _q1052.rpost, _q1052.so, _q1052.sr, _q1052.mv = (I, olos, rlos, rpost, so, sr, mv)

    def slack_suffix_min(_q1052):
        """min over j >= k of (avail[j] - X_cum[j]) for every k."""
        n, x, _q345 = (_q1052.n, _q1052.x, _q1052.avail)
        _q1066 = [0] * n
        cum = 0
        for k in range(n):
            cum += x[k]
            _q1066[k] = _q345[k] - cum
        _q880 = [0] * n
        m = 10 ** 9
        for k in range(n - 1, -1, -1):
            if _q1066[k] < m:
                m = _q1066[k]
            _q880[k] = m
        return _q880

    def greedy(_q1052, _q431, _q776=0.0, _q766=400, _q576=None, chunk0=1):
        """Allocate units in MV order: chunk0 units at a time at slot 0 (the decision), `chunk` elsewhere; the
        last slot-0 steps are refined unit by unit.  fix0 = force the slot-0 quantity.  Returns iterations."""
        _q675 = 0
        x = _q1052.x
        if _q576 is not None:
            x[0] = int(_q576)
        _q394 = max(1, int(chunk0))
        while _q675 < _q766:
            _q675 += 1
            _q1052.evaluate()
            _q1073 = _q1052.slack_suffix_min()
            best = -1e+18
            _q365 = -1
            mv = _q1052.mv
            _q367 = _q1052.blocked
            for k in range(_q1052.n):
                if k == 0 and _q576 is not None or _q367[k]:
                    continue
                if _q1073[k] >= 1 and mv[k] > best:
                    best = mv[k]
                    _q365 = k
            if _q365 < 0 or best <= _q776:
                if _q394 > 1 and x[0] > 0 and (_q576 is None):
                    _q349 = min(_q394 - 1, x[0])
                    x[0] -= _q349
                    _q1052.total -= _q349
                    _q394 = 1
                    continue
                break
            c = min(_q394, _q1073[0]) if _q365 == 0 else min(_q431, _q1073[_q365])
            if c < 1:
                c = 1
            x[_q365] += c
            _q1052.total += c
        _q1052.evaluate()
        return _q675

    def move_candidate(_q1052, _q709):
        """Best single-unit move of this item that raises its sales at slots <= km: the least valuable source
        (an allocated slot b > km, or an unsold unit) that can reach a slot a <= km without crossing a slot whose
        availability is fully used (a unit moved from b to a needs slack >= 1 on every slot of [a, b)), and the most
        valuable target a <= km.  Returns (src or None, src_mv, tgt, tgt_mv, room) or None."""
        n, x, _q345, mv = (_q1052.n, _q1052.x, _q1052.avail, _q1052.mv)
        if _q709 < 0:
            return None
        _q1066 = [0] * n
        cum = 0
        for k in range(n):
            cum += x[k]
            _q1066[k] = _q345[k] - cum
        _q751 = [0] * (_q709 + 1)
        m = 10 ** 9
        for k in range(_q709, -1, -1):
            if _q1066[k] < m:
                m = _q1066[k]
            _q751[k] = m
        _q1120 = None
        _q367 = _q1052.blocked
        for k in range(_q709 + 1):
            if _q751[k] >= 1 and (not _q367[k]) and (_q1120 is None or mv[k] > mv[_q1120]):
                _q1120 = k
        if _q1120 is None:
            return None
        best = None
        _q931 = 10 ** 9
        for b in range(_q709 + 1, n):
            if _q931 < 1:
                break
            if x[b] > 0 and (best is None or mv[b] < best[1]):
                best = (b, mv[b], min(_q931, x[b]))
            if _q1066[b] < _q931:
                _q931 = _q1066[b]
        src, _q1085, _q1015 = (None, 0.0, _q931) if best is None else best
        if best is not None and _q931 >= 1 and (0.0 < _q1085):
            src, _q1085, _q1015 = (None, 0.0, _q931)
        if src is None and _q931 < 1:
            return None
        room = min(_q751[_q1120], _q1015)
        if room < 1:
            return None
        return (src, _q1085, _q1120, mv[_q1120], int(room))

    def last_unit_mv(_q1052, k):
        """MV of the last unit placed at slot k (what removing it loses), with the current allocation."""
        if _q1052.x[k] <= 0:
            return None
        _q1052.x[k] -= 1
        _q1052.evaluate()
        _q1159 = _q1052.mv[k]
        _q1052.x[k] += 1
        return _q1159

def plan_value_item(item, Ib, Rpre, Rpost, x, lam=1.0):
    """Exact (engine-walk) value of one item's slot plan x against a frozen rival: returns (own $, rival $,
    own - lam * rival).  Rival lots are rounded to integers (tests / diagnostics)."""
    own = _q1004 = 0.0
    cum = 0
    for k in range(len(x)):
        _q657 = Ib[k] + cum
        rp = int(round(Rpre[k]))
        _q1013 = int(round(Rpost[k]))
        _q972, _q1159 = _fsim.sell_walk(item, rp, int(round(_q657)))
        _q857, _q1159 = _fsim.sell_walk(item, int(x[k]), _q1159)
        _q973, _q1159 = _fsim.sell_walk(item, _q1013, _q1159)
        own += _q857
        _q1004 += _q972 + _q973
        cum += x[k]
    return (own, _q1004, own - lam * _q1004)

class SaleScheduler:

    def __init__(_q1052, lam=1.0, items=GOODS, _q830=12, _q774=48, _q551=13, _q432=12, cap=100, margin=4, _q1002=1.0, _q1003=0.5, _q776=0.0, _q449=('CARROT', 'WHEAT'), _q450=28, _q764=10, _q765=80):
        _q1052.lam = float(lam)
        _q1052.items = tuple(items)
        _q1052.near = int(_q830)
        _q1052.mid = int(_q774)
        _q1052.far_hour = int(_q551)
        _q1052.chunks = max(1, int(_q432))
        _q1052.cap = int(cap)
        _q1052.margin = int(margin)
        _q1052.rho_future = float(_q1002)
        _q1052.rho_idx0 = float(_q1003)
        _q1052.min_mv = float(_q776)
        _q1052.cont_items = tuple(_q449 or ())
        _q1052.cont_last_day = int(_q450)
        _q1052.margin_future = int(_q764)
        _q1052.max_cap_moves = int(_q765)
        _q1052.stats = {'calls': 0, 'ms_sum': 0.0, 'ms_max': 0.0}
        warm(_q1052.items)

    def _item_inputs(_q1052, _q675, _q1070, t0, _q667, _q483, rival, arrivals, _q1095, _q1001, cont_rate):
        n = len(_q1070)
        _q970 = [0.0] * (_q1070[-1] - t0 + 1)
        if rival:
            for s, _q1018 in rival.items():
                if t0 <= s <= _q1070[-1]:
                    _q1159 = _q1018.get(_q675)
                    if _q1159:
                        _q970[s - t0] += float(_q1159)
        a = [0.0] * (_q1070[-1] - t0 + 1)
        if arrivals:
            for s, _q1018 in arrivals.items():
                if t0 < s <= _q1070[-1]:
                    _q1159 = _q1018.get(_q675)
                    if _q1159:
                        a[s - t0] += float(_q1159)
        _q458 = float((cont_rate or {}).get(_q675, 0.0) or 0.0)
        if _q458 > 0 and _q675 in _q1052.cont_items:
            _q476 = t0 // TPD + 3
            for _q475 in range(_q476, _q1052.cont_last_day + 1):
                s = _q475 * TPD
                if t0 < s <= _q1070[-1]:
                    a[s - t0] += _q458
        Ib = [0.0] * n
        Rpre = [0.0] * n
        Rpost = [0.0] * n
        avail = [0] * n
        _q466 = 0.0
        _q464 = float(_q1095)
        _q947 = t0
        for k in range(n):
            _q1064 = _q1070[k]
            Ib[k] = _q667 - _q483[_q1064 - t0] + _q466
            _q1000 = _q1001 if k == 0 else _q1052.rho_future
            _q1009 = _q970[_q1064 - t0]
            Rpre[k] = _q1000 * _q1009
            _q856 = _q1070[k + 1] if k + 1 < n else _q1070[-1] + 1
            _q940 = (1.0 - _q1000) * _q1009
            for s in range(_q1064 + 1, _q856):
                if s - t0 < len(_q970):
                    _q940 += _q970[s - t0]
            Rpost[k] = _q940
            _q466 += _q1009 + (_q940 - (1.0 - _q1000) * _q1009)
            if k > 0:
                for s in range(_q947 + 1, _q1064 + 1):
                    _q464 += a[s - t0]
            avail[k] = int(math.floor(_q464 + 0.5))
            _q947 = _q1064
        avail[0] = int(_q1095)
        for k in range(1, n):
            if avail[k] < avail[k - 1]:
                avail[k] = avail[k - 1]
        return (Ib, Rpre, Rpost, avail)

    def decide(_q1052, step, inv, shops, stock, arrivals=None, rival=None, K=10, shed_total=None, _q1182=None, eod_arrivals=None, cont_rate=None, lam=None, drain_mode='expected', items=None, cash=None, cash_need=None, cash_floor=0.0, k_future=None):
        _q1111 = time.perf_counter()
        t0 = int(step)
        lam = _q1052.lam if lam is None else float(lam)
        items = _q1052.items if items is None else tuple(items)
        K = int(K if K is not None else 10)
        _q880 = {'orders': [], 'now': {}, 'idx0': None, 'plan': {}, 'mv': {}, 'cap': {'violations': 0, 'moves': 0, 'load_max': None}, 'cash': {'violations': 0, 'moves': 0}, 'ms': 0.0}
        if t0 > LAST:
            return _q880
        _q1070 = make_slots(t0, _q1052.near, _q1052.mid, _q1052.far_hour)
        _q483 = drain_path(inv, shops, t0, _q1070[-1] + 1, drain_mode)
        _q704 = k_future or {}
        blocked = [K <= 0 if k == 0 else int(_q704.get(_q1064, 10)) <= 0 for k, _q1064 in enumerate(_q1070)]
        _q926 = {}
        _q1134 = {}
        if arrivals:
            for s, _q1018 in arrivals.items():
                if t0 < s <= _q1070[-1] and _q1018:
                    for _q675, _q1159 in _q1018.items():
                        _q1134[_q675] = _q1134.get(_q675, 0.0) + float(_q1159 or 0.0)
        for _q675 in items:
            _q1031 = int(stock.get(_q675, 0) or 0)
            _q602 = _q1134.get(_q675, 0.0) + (float((cont_rate or {}).get(_q675, 0.0) or 0.0) if _q675 in _q1052.cont_items else 0.0)
            if _q1031 <= 0 and (shed_total is None or _q602 < 0.5):
                continue
            Ib, Rpre, Rpost, avail = _q1052._item_inputs(_q675, _q1070, t0, float(inv.get(_q675, I0)), _q483[_q675], rival, arrivals, _q1031, 1.0, cont_rate)
            _q32 = _ItemPlan(_q675, Ib, Rpre, Rpost, avail, lam, blocked)
            U = avail[-1]
            _q431 = max(1, int(math.ceil(U / float(_q1052.chunks))))
            _q32.greedy(_q431, _q1052.min_mv, chunk0=max(1, int(math.ceil(_q1031 / 8.0))))
            _q926[_q675] = [_q32, _q431, _q1031]
        _q357, idx0 = (0.0, None)
        for _q675, (_q32, _q431, _q1031) in _q926.items():
            _q1191 = _q32.x[0]
            _q971 = _q32.Rpre[0]
            if _q1031 <= 0 or _q971 < 0.05:
                continue
            _q1194 = _q1191 if _q1191 > 0 else min(_q1031, 6)
            pf = _q32.pf
            I = _q32.I[0]
            _q605 = 0.0
            for _q681 in range(_q1194):
                _q605 += pf(I + _q681) - pf(I + _q971 + _q681)
            _q606 = _q971 * (pf(I + 0.5 * _q971) - pf(I + _q1194 + 0.5 * _q971))
            _q607 = _q605 + lam * _q606
            if _q607 > _q357:
                _q357, idx0 = (_q607, _q675)
        if idx0 is not None and _q1052.rho_idx0 < 1.0:
            _q33, _q431, _q1031 = _q926[idx0]
            Ib, Rpre, Rpost, avail = _q1052._item_inputs(idx0, _q1070, t0, float(inv.get(idx0, I0)), _q483[idx0], rival, arrivals, _q1031, _q1052.rho_idx0, cont_rate)
            _q32 = _ItemPlan(idx0, Ib, Rpre, Rpost, avail, lam, blocked)
            _q32.greedy(_q431, _q1052.min_mv, chunk0=max(1, int(math.ceil(_q1031 / 8.0))))
            _q926[idx0][0] = _q32
        if shed_total is not None:
            _q612 = sum((int(stock.get(_q675, 0) or 0) for _q675 in _q926))
            _q1052._capacity(_q926, _q1070, t0, shed_total, _q612, arrivals, _q1182, eod_arrivals, _q880)
        if cash is not None and cash_need:
            _q1052._cash(_q926, _q1070, t0, float(cash), cash_need, float(cash_floor), _q880)
        now = {}
        for _q675, (_q32, _q431, _q1031) in _q926.items():
            _q1191 = min(_q32.x[0], _q1031)
            if _q1191 > 0:
                now[_q675] = _q1191
            _q880['plan'][_q675] = [(_q1070[k], _q32.x[k]) for k in range(_q32.n) if _q32.x[k]]
            _q880['mv'][_q675] = _q32.mv[0]
        if K <= 0:
            now = {}
        _q873 = []
        for _q675, n in now.items():
            _q32 = _q926[_q675][0]
            pf = _q32.pf
            _q1159 = _q32.I[0] + _q32.Rpre[0]
            val = 0.0
            for _q681 in range(n):
                val += pf(_q1159 + _q681)
            _q873.append((0 if _q675 == idx0 else 1, -val, PRODUCTS.index(_q675), _q675, n))
        _q873.sort()
        _q873 = _q873[:max(0, K)]
        _q880['orders'] = [['SELL', _q675, int(n)] for _, _, _, _q675, n in _q873]
        _q880['now'] = {_q675: int(n) for _, _, _, _q675, n in _q873}
        _q880['idx0'] = idx0 if idx0 in _q880['now'] else None
        ms = (time.perf_counter() - _q1111) * 1000.0
        _q880['ms'] = ms
        st = _q1052.stats
        st['calls'] += 1
        st['ms_sum'] += ms
        if ms > st['ms_max']:
            st['ms_max'] = ms
        return _q880

    def _capacity(_q1052, _q926, _q1070, t0, shed_total, _q612, arrivals, _q1182, eod_arrivals, _q880):
        """Shed capacity over the whole horizon (module docstring).  Load after the market of step s plus the
        arrivals of s+1:  load(s) = NG + goods_now + goods arrivals (t0, s+1] - planned goods sales (<= s)
        + [s = hour 23] x the night's non-goods arrivals (the carried WHEAT / FERTILIZER of the end-of-day drop).
        NG = the non-goods units in the shed now (reserves, animals: assumed to stay at this level).  Checked at
        every step until tonight's hour 23 (cap - margin) and at hour 23 of every later day <= 28
        (cap - margin_future).  Violations are repaired by the cheapest moves of planned goods units to an
        earlier slot (cost = MV lost)."""
        _q481 = t0 // TPD
        _q844 = float(shed_total) - float(_q612)
        _q616 = set(_q926)
        _q725 = _q1070[-1]
        _q314 = {}
        _q315 = {}
        if arrivals:
            for s, _q1018 in arrivals.items():
                if t0 < s <= _q725 + 1 and _q1018:
                    g = n = 0.0
                    for _q675, _q1159 in _q1018.items():
                        if _q675 in _q616:
                            g += float(_q1159 or 0.0)
                        else:
                            n += float(_q1159 or 0.0)
                    _q314[s] = g
                    _q315[s] = n
        _q521 = _q481 * TPD + 23 if _q481 < 29 else LAST
        if eod_arrivals is not None and t0 <= _q521 and (_q481 < 29):
            _q314[_q521 + 1] = float(sum((_q1159 for _q675, _q1159 in eod_arrivals.items() if _q675 in _q616)))
            _q315[_q521 + 1] = float(sum((_q1159 for _q675, _q1159 in eod_arrivals.items() if _q675 not in _q616)))
        _q448 = [(s, _q1052.margin, s == _q521 and _q481 < 29) for s in range(t0, min(_q521, LAST) + 1)]
        _q448 += [(_q475 * TPD + 23, _q1052.margin_future, True) for _q475 in range(_q481 + 1, 29)]
        _q794 = len(_q1070)

        def _q711(s):
            if _q1070[0] > s:
                return -1
            lo, hi = (0, _q794 - 1)
            while lo < hi:
                _q774 = (lo + hi + 1) // 2
                if _q1070[_q774] <= s:
                    lo = _q774
                else:
                    hi = _q774 - 1
            return lo
        _q328 = sorted(_q314)
        moves = _q1162 = 0
        load_max = -1e+18
        for s, _q763, _q846 in _q448:
            _q709 = _q711(s)
            if _q709 < 0:
                continue
            _q407 = float(_q1052.cap - _q763)
            _q341 = 0.0
            for _q1087 in _q328:
                if _q1087 > s + 1:
                    break
                _q341 += _q314[_q1087]
            _q543 = _q315.get(s + 1, 0.0) if _q846 else 0.0
            while True:
                sold = 0
                for _q675, _q922 in _q926.items():
                    x = _q922[0].x
                    for k in range(_q709 + 1):
                        sold += x[k]
                load = _q844 + float(_q612) + _q341 - sold + _q543
                _q487 = load - _q407
                if _q487 <= 1e-09 or moves >= _q1052.max_cap_moves:
                    if load > load_max:
                        load_max = load
                    break
                _q1162 += 1
                best = None
                for _q675, _q922 in _q926.items():
                    _q770 = _q922[0].move_candidate(_q709)
                    if _q770 is None:
                        continue
                    src, _q1085, _q1120, _q1121, room = _q770
                    cost = _q1085 - _q1121
                    if best is None or cost < best[0]:
                        best = (cost, _q675, src, _q1120, room)
                if best is None:
                    if load > load_max:
                        load_max = load
                    break
                cost, _q675, src, _q1120, room = best
                c = int(max(1, min(room, math.ceil(_q487), _q926[_q675][1])))
                _q32 = _q926[_q675][0]
                if src is not None:
                    _q32.x[src] -= c
                else:
                    _q32.total += c
                _q32.x[_q1120] += c
                _q32.evaluate()
                moves += 1
        _q880['cap']['violations'] = _q1162
        _q880['cap']['moves'] = moves
        _q880['cap']['load_max'] = load_max

    def _cash(_q1052, _q926, _q1070, t0, cash, need, floor, _q880):
        """Funding constraint: for every step s from t0 to tonight's hour 23 (the last market on day 29) or to the
        last step in `need` (e.g. tomorrow's hours 0-1: the morning hires are paid before any sale slot opens),
        cash + planned goods revenue (slots <= s) - sum(need[t0..s]) >= floor.  need = {step: net $ the caller
        pays at that step (planned purchases / hires / land minus its other sales)}.  Revenue of a planned lot ~
        x * quote(middle of the lot).  Violations are repaired by moving planned goods units to an earlier slot
        (or selling unsold ones) at the least MV cost per $ raised."""
        _q481 = t0 // TPD
        _q521 = _q481 * TPD + 23 if _q481 < 29 else LAST
        _q522 = max([_q521] + [int(k) for k in need if int(k) >= t0])
        steps = [s for s in range(t0, min(_q522, LAST) + 1)]
        _q465 = []
        _q319 = 0.0
        for s in steps:
            _q319 += float(need.get(s, 0.0) or 0.0)
            _q465.append(_q319)
        if not steps or max(_q465) <= cash - floor:
            return
        _q794 = len(_q1070)

        def _q711(s):
            if _q1070[0] > s:
                return -1
            lo, hi = (0, _q794 - 1)
            while lo < hi:
                _q774 = (lo + hi + 1) // 2
                if _q1070[_q774] <= s:
                    lo = _q774
                else:
                    hi = _q774 - 1
            return lo

        def _q997(_q709):
            _q1133 = 0.0
            for _q675, _q922 in _q926.items():
                _q32 = _q922[0]
                for k in range(_q709 + 1):
                    _q1196 = _q32.x[k]
                    if _q1196:
                        _q1133 += _q1196 * _q32.pf(_q32.I[k] + _q32.Rpre[k] + 0.5 * _q1196)
            return _q1133
        moves = _q1162 = 0
        for _q652, s in enumerate(steps):
            _q709 = _q711(s)
            if _q709 < 0:
                continue
            while True:
                _q608 = _q465[_q652] - cash + floor - _q997(_q709)
                if _q608 <= 1e-06 or moves >= _q1052.max_cap_moves:
                    break
                _q1162 += 1
                best = None
                for _q675, _q922 in _q926.items():
                    _q32 = _q922[0]
                    _q770 = _q32.move_candidate(_q709)
                    if _q770 is None:
                        continue
                    src, _q1085, _q1120, _q1121, room = _q770
                    q = _q32.pf(_q32.I[_q1120] + _q32.Rpre[_q1120] + _q32.x[_q1120])
                    if q <= 1.0:
                        continue
                    cost = (_q1085 - _q1121) / q
                    if best is None or cost < best[0]:
                        best = (cost, _q675, src, _q1120, room, q)
                if best is None:
                    break
                cost, _q675, src, _q1120, room, q = best
                c = int(max(1, min(room, math.ceil(_q608 / q))))
                _q32 = _q926[_q675][0]
                if src is not None:
                    _q32.x[src] -= c
                else:
                    _q32.total += c
                _q32.x[_q1120] += c
                _q32.evaluate()
                moves += 1
        _q880['cash']['violations'] = _q1162
        _q880['cash']['moves'] = moves

def room_guard(sells, _q1056, carried_end, levels=None, cap_target=96, hinge=('TOMATO', 'CARROT'), _q873=None):
    """Hour-23 safety net (pd_market 'protect' guard with room_hinge_last True): add SELL units until the shed
    after this market plus tonight's drop fits cap_target.  sells = [['SELL', item, n], ...] (not mutated);
    levels = {item: protected units} for WHEAT / FERTILIZER (tomorrow's feed leg / FERTILIZE earmark).
    Pass order: EGG + WHEAT / FERTILIZER above their protected level, the protected WHEAT / FERTILIZER, CARROT /
    TOMATO, then MELON, WOOL, MILK, STRAWBERRY.  Returns a new list (added units merged into existing orders,
    new orders appended)."""
    _q757 = levels or {}
    sold = {}
    for _q857 in sells:
        sold[_q857[1]] = sold.get(_q857[1], 0) + int(_q857[2])
    after = sum((int(_q1159) for k, _q1159 in _q1056.items())) - sum((min(sold.get(k, 0), int(_q1056.get(k, 0))) for k in sold))
    _q881 = after + int(carried_end) - int(cap_target)
    if _q881 <= 0:
        return [list(_q857) for _q857 in sells]
    _q903 = _q873 or ([(_q675, _q757.get(_q675, 0)) for _q675 in ('EGG', 'FERTILIZER', 'WHEAT')], [('WHEAT', 0), ('FERTILIZER', 0)], [(_q675, 0) for _q675 in ('CARROT', 'TOMATO')], [(_q675, 0) for _q675 in ('MELON', 'WOOL', 'MILK', 'STRAWBERRY')])
    _q324 = {}
    for _q614 in _q903:
        for _q675, level in _q614:
            if _q881 <= 0:
                break
            _q630 = int(_q1056.get(_q675, 0)) - sold.get(_q675, 0) - _q324.get(_q675, 0) - int(level)
            k = min(max(0, _q630), _q881)
            if k > 0:
                _q324[_q675] = _q324.get(_q675, 0) + k
                _q881 -= k
    _q992 = []
    for _q857 in sells:
        _q860 = list(_q857)
        if _q860[1] in _q324:
            _q860[2] = int(_q860[2]) + _q324.pop(_q860[1])
        _q992.append(_q860)
    for _q675, k in _q324.items():
        _q992.append(['SELL', _q675, int(k)])
    return _q992