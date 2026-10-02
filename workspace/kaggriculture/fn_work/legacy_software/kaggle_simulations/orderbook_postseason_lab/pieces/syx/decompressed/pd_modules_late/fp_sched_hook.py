"""fp.sched_hook - glue between the coordinated planner (tools/portable/pd_layer.py) and the fp sale scheduler.
Original work, Shawn404, 28 Sep 2026.  Pure Python (no numpy, no engine import, no file access at call time).

One FPContext per seat.  The submission wrapper (HYA2 / HYA3 main.py) creates it at import and calls observe() on
EVERY turn from step 0 (the rival model needs the whole public history: opening features, harvests, sales); the
planner's market step (pd_layer._pd_market, knob _PD_FP_SCHED) calls sells() to replace the rule-based SELLs of the
scheduled goods; everything else of the market list (WHEAT controller / C9 FERTILIZER rows, purchases, hires,
the order window) stays with the planner.

API
---
    from tools.fp.sched_hook import FPContext
    ctx = FPContext(player=None, lam=1.0, items=GOODS, rival_params=None, long_every=12, short_h=36,
                    sched_kw=None, own_mode='planner', own_lags=None, cash_floor=300.0)
        rival_params: the rival_params.json dict (a bundle must pass it: no file access);  own_lags: the
        ownfc_lags.LAGS dict (a bundle must pass it: ownfc imports its tables lazily at call time)
    ctx.observe(obs, own_orders=None)       # every turn, before acting; own_orders = our market list of the previous
                                            # turn (None: the list given to note_orders() last turn)
    ctx.note_orders(market_list)            # after acting (the wrapper passes the final market list)
    merged, info = ctx.sells(obs, shed1, rule_sells, K=10, room_items=None, carried_end=0, cash=None,
                             cash_need=None, levels=None, cap_target=96, pd_state=None, guard=True, k_future=None)
        shed1       our shed at MARKET time (pd_market.shed_after_units(...)[0]: after this turn's unit commands)
        rule_sells  the planner's SELL list for this step (pd_market.sale_orders + the layer's edits); its orders for
                    items outside ctx.items (WHEAT / FERTILIZER) are kept as they are, the scheduled goods are replaced
        room_items  hour 23: {item: units} the units carry into tonight's drop (the layer's room_items / carried_end)
        cash / cash_need  money now / {step: $} today's planned purchases net of other sales (see sched.decide)
        k_future    {step: free SELL slots} of the next steps (10 - planned purchases / hires at that step)
        levels      {item: protected units} of WHEAT / FERTILIZER for the hour-23 room guard (pd_market.room_levels)
      -> merged SELL list (scheduled goods first, in the scheduler's index order, then the planner's other SELLs),
         info = the scheduler's result dict (+ 'ms_total' incl. the forecasts)
    ctx.telemetry  -> {'turns', 'sells_calls', 'ms_sum', 'ms_max', 'errors', 'last_error'}

Timing (tools/tmp/fp/sched/test_hook.py on recorded games): observe ~0.15 ms per turn; sells ~10-20 ms mean incl.
OwnForecast (~1 ms), the rival forecasts (short H=36 every call, the long one every long_every steps) and the
scheduler; worst turn < 100 ms.  No look-ahead: only the observations and our own orders are used.
"""
import time
try:
    from . import sched as _sched
    from . import ownfc as _ownfc
    from . import rival as _rival
except ImportError:
    import fp_sched as _sched
    import fp_ownfc as _ownfc
    import fp_rival as _rival
GOODS = _sched.GOODS
LAST = 718
TPD = 24

def _g(_q922, k, _q530=None):
    if isinstance(_q922, dict):
        return _q922.get(k, _q530)
    try:
        return getattr(_q922, k, _q530)
    except Exception:
        return _q530

class FPContext:

    def __init__(_q1120, player=None, lam=1.0, items=GOODS, rival_params=None, long_every=12, short_h=36, sched_kw=None, own_mode='planner', own_lags=None, cash_floor=300.0):
        _q1120.items = tuple(items)
        _q1120.cash_floor = float(cash_floor)
        _q1120.own_lags = own_lags
        _q1120.rm = _rival.RivalModel(params=rival_params, player=player)
        _q1120.sch = _sched.SaleScheduler(lam=lam, items=_q1120.items, **sched_kw or {})
        _q1120.long_every = int(long_every)
        _q1120.short_h = int(short_h)
        _q1120.own_mode = own_mode
        _q1120.long_fc = {}
        _q1120.long_at = -10 ** 9
        _q1120.last_orders = None
        _q1120.prev = None
        _q1120.arr_hist = {}
        _q1120.telemetry = {'turns': 0, 'sells_calls': 0, 'ms_sum': 0.0, 'ms_max': 0.0, 'errors': 0, 'last_error': ''}

    def observe(_q1120, _q928, own_orders=None):
        try:
            _q937 = own_orders if own_orders is not None else _q1120.last_orders
            _q1120.rm.observe(_q928, own_orders=_q937)
            step = int(_g(_q928, 'step', 0) or 0)
            _q1016 = _g(_q928, 'private', {}) or {}
            shed = dict(_g(_q1016, 'shed', {}) or {})
            carry = {}
            for _q530 in _g(_q1016, 'inventories', []) or []:
                try:
                    for k, _q1233 in dict(_q530).items():
                        carry[k] = carry.get(k, 0) + int(_q1233 or 0)
                except (TypeError, ValueError):
                    pass
            if _q1120.prev is not None and _q1120.prev[0] == step - 1:
                _q1057 = {}
                for _q922 in (_q937 or [])[:10]:
                    if isinstance(_q922, (list, tuple)) and len(_q922) >= 3 and (_q922[0] == 'SELL'):
                        try:
                            _q1057[_q922[1]] = _q1057.get(_q922[1], 0) + int(_q922[2])
                        except (TypeError, ValueError):
                            pass
                _q1086 = {}
                _q975 = _q1120.prev[2] if len(_q1120.prev) > 2 else {}
                for it in _q1120.items:
                    _q408 = int(_q1120.prev[1].get(it, 0) or 0)
                    now = int(shed.get(it, 0) or 0)
                    sold = min(_q1057.get(it, 0), _q408 + int(_q975.get(it, 0) or 0))
                    a = now - _q408 + sold
                    if a > 0:
                        _q1086[it] = a
                if _q1086:
                    _q1120.arr_hist[step] = _q1086
                for s in [s for s in _q1120.arr_hist if s < step - 72]:
                    del _q1120.arr_hist[s]
            _q1120.prev = (step, {it: shed.get(it, 0) for it in _q1120.items}, {it: carry.get(it, 0) for it in _q1120.items})
            _q1120.telemetry['turns'] += 1
        except Exception as _q575:
            _q1120.telemetry['errors'] += 1
            _q1120.telemetry['last_error'] = ('observe %r' % (_q575,))[:200]

    def note_orders(_q1120, orders):
        _q1120.last_orders = [list(_q922) for _q922 in orders or [] if isinstance(_q922, (list, tuple))]

    def rival_forecast(_q1120, t):
        if t - _q1120.long_at >= _q1120.long_every or not _q1120.long_fc:
            _q1120.long_fc = _q1120.rm.forecast(H=LAST + 1 - t)
            _q1120.long_at = t
        short = _q1120.rm.forecast(H=_q1120.short_h)
        _q946 = {s: _q1233 for s, _q1233 in _q1120.long_fc.items() if s >= t + _q1120.short_h}
        _q946.update(short)
        return _q946

    def cont_rate(_q1120, t, _q1149=48):
        _q1206 = {}
        for s, _q1086 in _q1120.arr_hist.items():
            if t - _q1149 <= s < t:
                for it, _q1233 in _q1086.items():
                    _q1206[it] = _q1206.get(it, 0.0) + _q1233
        return {it: _q1233 * TPD / float(_q1149) for it, _q1233 in _q1206.items()}

    def sells(_q1120, _q928, _q1125, _q1094, K=10, room_items=None, carried_end=0, cash=None, cash_need=None, levels=None, cap_target=96, pd_state=None, _q675=True, k_future=None):
        t0 = time.perf_counter()
        step = int(_g(_q928, 'step', 0) or 0)
        hour = step % TPD
        day = step // TPD
        market = _g(_q928, 'market', {}) or {}
        inv = dict(_g(market, 'inventory', {}) or {})
        shops = list(_g(_g(_q928, 'town', {}) or {}, 'unlocked_shops', []) or [])
        stock = {it: int(_q1125.get(it, 0) or 0) for it in _q1120.items if int(_q1125.get(it, 0) or 0) > 0}
        _q610 = _ownfc.OwnForecast(_q928, pd_state=pd_state, mode=_q1120.own_mode, lags=_q1120.own_lags)
        supply = _q610.supply(LAST + 1 - step)
        supply.pop(step, None)
        _q1067 = _q1120.rival_forecast(step)
        _q588 = dict(room_items) if room_items is not None and hour == 23 and (day < 29) else None
        _q775 = {}
        if cash is not None and cash_need:
            _q775 = {'cash': float(cash), 'cash_need': cash_need, 'cash_floor': _q1120.cash_floor}
        if k_future:
            _q775['k_future'] = k_future
        _q1060 = _q1120.sch.decide(step, inv, shops, stock, arrivals=supply, rival=_q1067, K=K, shed_total=sum((int(_q1233) for _q1233 in _q1125.values())), eod_arrivals=_q588, cont_rate=_q1120.cont_rate(step), **_q775)
        _q668 = [list(_q922) for _q922 in _q1060['orders']]
        rest = [list(_q922) for _q922 in _q1094 or [] if isinstance(_q922, (list, tuple)) and len(_q922) >= 3 and (_q922[1] not in _q1120.items)]
        _q835 = _q668 + rest
        if _q675 and hour == 23 and (day < 29):
            _q835 = _sched.room_guard(_q835, _q1125, carried_end, levels=levels, cap_target=cap_target)
        ms = (time.perf_counter() - t0) * 1000.0
        _q1060['ms_total'] = ms
        tl = _q1120.telemetry
        tl['sells_calls'] += 1
        tl['ms_sum'] += ms
        if ms > tl['ms_max']:
            tl['ms_max'] = ms
        return (_q835, _q1060)