"""Original work, Shawn404, 28 Sep 2026.

ownfc - forecast of OUR OWN future sellable supply per item per step, and the projected shed load.

Pure Python (no numpy, no engine import, no file access).  Built for the fp sale optimiser: it answers "how many units of
each product will reach our shed, and when, from the assets we already own", using the engine's production rules for
the units and labour-lag tables fitted on our own logged games for the timing (production -> harvest -> shed).
Report + validation: results/portable/fp_own.txt (test script tools/tmp/fp/own/test_ownfc.py).

API
---
    from tools.fp.ownfc import OwnForecast
    fc = OwnForecast(obs, pd_state=None, mode='planner', lags=None, shed_capacity=100, planned=None, final_step=718)
        obs       the agent's observation (dict or Kaggle Struct) at step t = obs.step.  Only OUR OWN farm tiles, our
                  private shed / inventories and obs.step are read (no look-ahead, nothing hidden).
        pd_state  optional tools/pd/pd_state.FarmState of the same observation (its tiles / shed / inventories are reused).
        mode      'planner' (the coordinated planner's labour: P7d / P9 executor) or 'tape' (s24 / s25 tape stack);
                  selects the fitted tables.  Items missing in a mode fall back to the other mode.
        lags      optional table dict (tools/fp/ownfc_lags.LAGS format) to override the built-in tables.
        planned   optional future assets not yet on the farm: [(kind, day, n)], kind = crop ('WHEAT', ...) planted on
                  `day` or animal ('COW', ...) placed on `day`; forecast like standing ones (units from the rules).
        final_step last step whose market can still sell (718: the engine processes obs steps 0..718).
        final_dump step to which arrivals that would land after final_step are moved (717 = h21 of day 29: there is no
                  end-of-day drop on the last day, and our executor dumps its carried goods at h21-22 - RACE1-3 data).

    fc.supply(H, q=None) -> {step: {item: units}}   steps t .. t+H-1, units = expected (float) units that become
        sellable for the FIRST time at that step:  a DROP / PLACE during step s puts goods in the shed before the market
        of step s (same-step sale possible); goods still carried at the end of day d are dropped by the engine after the
        last market of the day and first sellable at step 24(d+1) (verified in kaggriculture.py: _end_of_day runs after
        _process_market; _drop_inventories_to_shed discards what exceeds shedCapacity).
        q in (0, 1): instead of the expectation, each lot is put whole at the q-quantile of its arrival step (q = 0.8
        -> "late" = conservative for sales planning).
    fc.totals(H) -> {item: units}            sum of supply(H)
    fc.cum(H)    -> {item: [cumulative units at t, t+1, ..., t+H-1]}
    fc.harvestable(H) -> {step: {item: units}} production schedule (units ready on the tile, no labour lag)
    fc.lots      [dict(item, units, anchor, elapsed, kind, xy)]  the lots behind the forecast (kind 'tile' | 'future' |
                 'carried' | 'fert' | 'planned'); anchor = step the units are ready (h0 of the production / harvest day).
    fc.feed_demand(H) -> {step: {'WHEAT': units}}  wheat the animals will eat (1 per animal-day; pulled from the shed)
    fc.capacity_path(sales, H=None, buys=None, withdraw='feed', defer=True) -> dict
        sales / buys: {step: {item: n}} (or {step: [(item, n)]}); withdraw: 'feed' (default: feed_demand), None, or a
        {step: {item: n}} dict of shed pickups.  Simulates the shed per step on the EXPECTED supply: arrivals
        (supply(H); overflow above the capacity is lost, as in the engine) -> pickups -> deferred sales -> sales (capped
        by stock) -> buys (capped by room, like the engine's BUY_PRODUCT / BUY_ANIMAL).  defer=True: the part of a sale
        the stock cannot cover is recorded in 'short' and sold as soon as the goods arrive (the realistic load path when
        the planned sale is only a little early); defer=False drops it.  Returns
        {'load': {step: shed units after the market}, 'room': {step: 100 - load}, 'overflow': {step: units lost},
         'short': {step: {item: units a sale could not find at that step}}, 'unfilled': {item: short units never
         filled within H}, 'blocked': {step: units of buys refused}, 'stock': {item: units at the end},
         'peak': max load, 'feasible': no overflow and no short sale}.

Engine rules mirrored (kaggriculture.py): non-ongoing crops (WHEAT / CARROT / MELON) start at 1 unit, +1 (+2 when
fertilised through that day) per WATER on ages [(myd+1)//2, myd], capped at max_yield, harvestable from first_yield_day;
ongoing crops (TOMATO / STRAWBERRY) produce at the end of day d when (d+1-planted-fyd) >= 0 and divisible by the
interval, max_yield productions, +2 only when watered that day and fertilised through d; animals produce 1 at the end
of every interval-th day from placed+fyd (available the next morning), plus the banked care bonus when fed that day
(the bank resets at every production; +1 for every day both fed and cared); fertilizer_available is set every night.
Policy / labour parameters (fitted on RACE1-3, our seats; tools/tmp/fp/own/fit_lags.py): harvest age of non-ongoing crops
by fertiliser class, P(fertilised), P(+2) for ongoing productions, feeding / care / collection rates, and the lag
tables P1 (anchor -> harvest), P2 (harvest hour -> shed arrival), P2rem (carried at hour h -> arrival), carry_frac.
"""
TPD = 24
FINAL_DAY = 29
CROPS = {'WHEAT': (2, 4, 0, 6, False), 'CARROT': (2, 3, 0, 4, False), 'MELON': (10, 12, 0, 6, False), 'TOMATO': (8, 8, 1, 4, True), 'STRAWBERRY': (10, 10, 2, 4, True)}
ANIMALS = {'GOOSE': (4, 1, 4, 'EGG'), 'COW': (8, 2, 6, 'MILK'), 'SHEEP': (6, 3, 6, 'WOOL')}
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
LMAX = 96
_DEF_ANIM = {'fed_prod': 0.9, 'fc_prod': 0.8, 'fc_non': 0.8, 'collect': 0.9}

def _get(_q922, k, _q530=None):
    if isinstance(_q922, dict):
        return _q922.get(k, _q530)
    g = getattr(_q922, 'get', None)
    if callable(g):
        try:
            return g(k, _q530)
        except TypeError:
            pass
    return getattr(_q922, k, _q530)

class _Tables:
    """Normalised, int-keyed view of one mode of the LAGS dict (with fallback to the other mode)."""

    def __init__(_q1120, _q25, mode):
        other = 'tape' if mode == 'planner' else 'planner'
        A, B = (_q25.get(mode, {}), _q25.get(other, {}))

        def _q987(key, item):
            _q1233 = A.get(key, {}).get(item)
            return _q1233 if _q1233 else B.get(key, {}).get(item)
        _q1120.P1, _q1120.S1, _q1120.P2, _q1120.P2rem, _q1120.cfrac = ({}, {}, {}, {}, {})
        _q1120.shed_frac, _q1120.hage, _q1120.p_fert, _q1120.p2_ong, _q1120.p2_cov, _q1120.anim = ({}, {}, {}, {}, {}, {})
        for it in PRODUCTS:
            _q530 = _q987('P1', it)
            if _q530:
                _q954 = [0.0] * (LMAX + 1)
                for k, _q1233 in _q530.items():
                    _q954[min(LMAX, int(k))] += _q1233
                s = sum(_q954) or 1.0
                _q954 = [x / s for x in _q954]
                _q1120.P1[it] = _q954
                S = [0.0] * (LMAX + 2)
                _q369 = 0.0
                for _q712 in range(LMAX, -1, -1):
                    _q369 += _q954[_q712]
                    S[_q712] = _q369
                _q1120.S1[it] = S
            for key, _q567 in (('P2', _q1120.P2), ('P2rem', _q1120.P2rem)):
                _q530 = _q987(key, it)
                if _q530:
                    _q1183 = {}
                    for _q697, dist in _q530.items():
                        _q697 = int(_q697)
                        _q429 = TPD - _q697
                        _q369 = {}
                        for k, _q1233 in dist.items():
                            k = min(int(k), _q429)
                            _q369[k] = _q369.get(k, 0.0) + float(_q1233)
                        s = sum(_q369.values()) or 1.0
                        _q1183[_q697] = [(k, _q1233 / s) for k, _q1233 in sorted(_q369.items())]
                    _q567[it] = _q1183
            _q530 = _q987('carry_frac', it)
            if _q530:
                _q644 = {int(h): float(_q1233) for h, _q1233 in _q530.items()}
                _q833 = sum(_q644.values()) / len(_q644)
                _q1120.cfrac[it] = [_q644.get(h, _q833) for h in range(TPD)]
            _q1233 = A.get('shed_frac', {}).get(it, B.get('shed_frac', {}).get(it))
            _q1120.shed_frac[it] = 1.0 if _q1233 is None else float(_q1233)
        for c in ('WHEAT', 'CARROT', 'MELON'):
            _q530 = _q987('hage', c) or {}
            _q1120.hage[c] = {_q610: sorted(((int(k), float(_q1233)) for k, _q1233 in dist.items())) for _q610, dist in _q530.items()}
            _q1233 = A.get('p_fert', {}).get(c, B.get('p_fert', {}).get(c))
            _q1120.p_fert[c] = 0.0 if _q1233 is None else float(_q1233)
        for c in ('TOMATO', 'STRAWBERRY'):
            for key, _q567, _q547 in (('p2_ong', _q1120.p2_ong, 0.5), ('p2_cov', _q1120.p2_cov, 0.95)):
                _q1233 = A.get(key, {}).get(c, B.get(key, {}).get(c))
                _q567[c] = _q547 if _q1233 is None else float(_q1233)
        for _q388 in ANIMALS:
            _q1233 = A.get('anim', {}).get(_q388) or B.get('anim', {}).get(_q388) or {}
            _q1120.anim[_q388] = {k: float(_q1233.get(k, _DEF_ANIM[k])) for k in _DEF_ANIM}
        _q1120._conv = {}

    def from_anchor(_q1120, item, _q575):
        """Arrival offsets (hours after the anchor, h0 of the anchor day) of a unit ready at the anchor and not yet
        harvested e hours after it: [(offset, prob)], offsets >= e.  Cached."""
        key = (item, _q575)
        _q1036 = _q1120._conv.get(key)
        if _q1036 is not None:
            return _q1036
        P1, _q54, P2 = (_q1120.P1.get(item), _q1120.S1.get(item), _q1120.P2.get(item))
        _q369 = {}
        if P1 is None or P2 is None:
            _q369[_q575] = 1.0
        else:
            _q581 = min(_q575, LMAX)
            surv = _q54[_q581]
            if surv <= 1e-09:
                for _q781, _q954 in P2.get(_q575 % TPD, P2.get(0, [(0, 1.0)])):
                    _q369[_q575 + _q781] = _q369.get(_q575 + _q781, 0.0) + _q954
            else:
                for _q26 in range(_q581, LMAX + 1):
                    w = P1[_q26]
                    if w <= 0.0:
                        continue
                    w /= surv
                    _q27 = max(_q26, _q575)
                    for _q781, _q954 in P2.get(_q27 % TPD, ()):
                        _q922 = _q27 + _q781
                        _q369[_q922] = _q369.get(_q922, 0.0) + w * _q954
        _q1036 = sorted(_q369.items())
        _q1120._conv[key] = _q1036
        return _q1036

    def surv(_q1120, item, _q575):
        S = _q1120.S1.get(item)
        if S is None:
            return 1.0
        return S[min(max(_q575, 0), LMAX)]
_TABLE_CACHE = {}

def _tables(mode, lags):
    if lags is None:
        key = ('builtin', mode)
        t = _TABLE_CACHE.get(key)
        if t is None:
            try:
                from . import ownfc_lags as _L
            except Exception:
                import ownfc_lags as _L
            t = _Tables(_L.LAGS, mode)
            _TABLE_CACHE[key] = t
        return t
    key = (id(lags), mode)
    t = _TABLE_CACHE.get(key)
    if t is None:
        t = _Tables(lags, mode)
        _TABLE_CACHE[key] = t
    return t

class OwnForecast:

    def __init__(_q1120, _q928, pd_state=None, mode='planner', lags=None, shed_capacity=100, planned=None, _q628=718, _q627=717):
        _q1120.mode = mode
        _q1120.T = _tables(mode, lags)
        _q1120.cap = shed_capacity
        _q1120.final_step = _q628
        _q1120.final_dump = _q627
        if pd_state is not None:
            me = pd_state.me
            step = pd_state.step
            tiles = pd_state.tiles
            shed = dict(pd_state.shed)
            _q735 = [dict(_q712) for _q712 in pd_state.inventories]
        else:
            me = int(_get(_q928, 'player', 0) or 0)
            step = _get(_q928, 'step', None)
            if step is None:
                step = TPD * int(_get(_q928, 'day', 0) or 0) + int(_get(_q928, 'hour', 0) or 0)
            step = int(step)
            farms = _get(_q928, 'farms', None) or []
            _q607 = farms[me] if len(farms) > me else {}
            tiles = _get(_q607, 'tiles', None) or []
            _q1016 = _get(_q928, 'private', None) or {}
            shed = {k: int(_q1233) for k, _q1233 in (_get(_q1016, 'shed', None) or {}).items() if _q1233}
            _q735 = [dict(_q712) for _q712 in _get(_q1016, 'inventories', None) or []]
        _q1120.t = step
        _q1120.day, _q1120.hour = divmod(step, TPD)
        _q1120.shed = shed
        _q1120.inventories = _q735
        _q1120.lots = []
        _q1120._n_animals = 0
        _q1120._unfed_today = 0
        _q1120._build(tiles, planned or ())
        _q1120._memo = {}

    def _lot(_q1120, item, units, anchor, kind, xy=None):
        if units <= 1e-09:
            return
        _q575 = max(0, _q1120.t - anchor)
        _q1120.lots.append({'item': item, 'units': units, 'anchor': anchor, 'elapsed': _q575, 'kind': kind, 'xy': xy})

    def _build(_q1120, tiles, planned):
        day, hour, T = (_q1120.day, _q1120.hour, _q1120.T)
        for _q1272, _q1086 in enumerate(tiles):
            for x, t in enumerate(_q1086):
                if not isinstance(t, dict):
                    continue
                if t.get('kind') == 'PLANT' and t.get('crop') in CROPS:
                    _q1120._crop(t, (x, _q1272))
                elif t.get('animal') in ANIMALS:
                    _q1120._animal(t, (x, _q1272))
        h = hour
        for inv in _q1120.inventories:
            for it, n in inv.items():
                if it not in PRODUCTS or not n:
                    continue
                _q644 = T.cfrac.get(it)
                _q1221 = n * (_q644[h] if _q644 else 1.0)
                if _q1221 > 1e-09:
                    _q1120.lots.append({'item': it, 'units': _q1221, 'anchor': _q1120.t, 'elapsed': 0, 'kind': 'carried', 'xy': None})
        for kind, _q530, n in planned:
            if kind in CROPS:
                _q604 = {'kind': 'PLANT', 'crop': kind, 'planted_day': int(_q530), 'watered_today': False, 'consecutive_unwatered': 1, 'yield_units': 0 if CROPS[kind][4] else 1, 'max_lifespan_step': -1, 'fertilized_until_day': -1}
                for _ in range(int(n)):
                    _q1120._crop(_q604, None, kind_tag='planned')
            elif kind in ANIMALS:
                _q604 = {'animal': kind, 'placed_day': int(_q530), 'yield_units': 0, 'fed_today': False, 'cared_today': False, 'pending_care_bonus': 0, 'fertilizer_available': False, 'consecutive_unfed': 0}
                for _ in range(int(n)):
                    _q1120._animal(_q604, None, kind_tag='planned')

    def _crop(_q1120, t, xy, kind_tag=None):
        c = t['crop']
        fyd, myd, _q741, _q852, ongoing = CROPS[c]
        day, T = (_q1120.day, _q1120.T)
        _q978 = int(t.get('planted_day', day))
        age = day - _q978
        units = int(t.get('yield_units', 0) or 0)
        watered = bool(t.get('watered_today'))
        _q654 = t.get('fertilized_until_day', -1)
        _q654 = -1 if _q654 is None else int(_q654)
        if ongoing:
            _q629 = _q978 + fyd
            _q1018 = [_q629 + k * _q741 for k in range(_q852)]
            _q970 = [D for D in _q1018 if D <= day]
            if units > 0:
                _q1120._lot(c, units, TPD * (_q970[-1] if _q970 else day), kind_tag or 'tile', xy)
            _q959, _q958 = (T.p2_ong[c], T.p2_cov[c])
            held = units
            for D in _q1018:
                if D <= day or D > FINAL_DAY:
                    continue
                _q979 = D - 1
                if _q979 == day:
                    if _q654 >= day:
                        _q724 = 2.0 if watered else 1.0 + _q958
                    else:
                        _q724 = 1.0 + _q959
                else:
                    _q724 = 1.0 + (_q958 if _q654 >= _q979 else _q959)
                if held + _q724 > _q852:
                    _q724 = max(0.0, _q852 - held)
                held = 0
                _q1120._lot(c, _q724, TPD * D, kind_tag or 'future', xy)
            return
        _q1265 = (myd + 1) // 2
        mls = t.get('max_lifespan_step', -1)
        mls = -1 if mls is None else int(mls)
        if mls >= 0 and _q1120.t >= mls:
            _q1120._lot(c, units, TPD * day, kind_tag or 'tile', xy)
            return
        if _q654 >= day:
            _q490 = (('F', 1.0),)
        elif age > _q1265 or (age == _q1265 and watered):
            _q490 = (('U', 1.0),)
        else:
            pf = T.p_fert[c]
            _q490 = (('F', pf), ('U', 1.0 - pf))
        _q744 = age + 1 if watered else age
        _q578 = _q1120.hour
        for _q610, _q975 in _q490:
            if _q975 <= 0.0:
                continue
            _q382 = T.hage[c].get(_q610) or T.hage[c].get('U') or T.hage[c].get('F') or [(myd, 1.0)]
            _q454 = []
            for A, _q964 in _q382:
                if A < age:
                    continue
                w = _q964 * (T.surv(c, _q578) if A == age else 1.0)
                if w > 0:
                    _q454.append((A, w))
            if not _q454:
                _q454 = [(max(age, fyd), 1.0)]
            s = sum((w for _, w in _q454))
            for A, w in _q454:
                A = max(A, fyd)
                _q1221 = units
                for _q743 in range(max(_q744, _q1265), min(A, myd) + 1):
                    _q1217 = _q610 == 'F' or _q978 + _q743 <= _q654
                    _q1221 = min(_q852, _q1221 + (2 if _q1217 else 1))
                D = _q978 + A
                if D > FINAL_DAY:
                    continue
                _q1120._lot(c, _q1221 * _q975 * w / s, TPD * D, kind_tag or ('tile' if D <= day else 'future'), xy)

    def _animal(_q1120, t, xy, kind_tag=None):
        _q388 = t['animal']
        fyd, _q741, _q852, prod = ANIMALS[_q388]
        day, T = (_q1120.day, _q1120.T)
        _q32 = T.anim[_q388]
        _q989 = int(t.get('placed_day', day))
        units = int(t.get('yield_units', 0) or 0)
        fed, cared = (bool(t.get('fed_today')), bool(t.get('cared_today')))
        bank = float(t.get('pending_care_bonus', 0) or 0)
        if _q989 <= day:
            _q1120._n_animals += 1
            if not fed:
                _q1120._unfed_today += 1
        _q629 = _q989 + fyd
        if units > 0:
            k = (day - _q629) // _q741 if day >= _q629 else 0
            _q785 = _q629 + k * _q741 if day >= _q629 else day
            _q1120._lot(prod, units, TPD * _q785, kind_tag or 'tile', xy)
        _q1122 = T.shed_frac.get('FERTILIZER', 1.0)
        if _q989 < day and t.get('fertilizer_available'):
            _q1120._lot('FERTILIZER', _q1122, TPD * day, 'fert', xy)
        for D in range(max(day + 1, _q989 + 1), FINAL_DAY + 1):
            _q1120._lot('FERTILIZER', _q32['collect'] * _q1122, TPD * D, 'fert', xy)
        D = _q629 if _q629 > day else _q629 + ((day - _q629) // _q741 + 1) * _q741
        held = units
        after = None
        while D <= FINAL_DAY:
            _q979 = D - 1
            if after is None:
                if _q979 == day:
                    _q427 = bank if fed else bank * _q32['fed_prod']
                    after = 1.0 if fed and cared else _q32['fc_prod']
                else:
                    today = 1.0 if fed and cared else _q32['fc_non']
                    if _q989 > day:
                        today, bank = (0.0, 0.0)
                    _q411 = max(0, _q979 - max(day, _q989 - 1) - 1)
                    _q580 = bank + today + _q411 * _q32['fc_non']
                    _q427 = _q32['fed_prod'] * _q580
                    after = _q32['fc_prod']
            else:
                _q427 = _q32['fed_prod'] * (after + (_q741 - 1) * _q32['fc_non'])
                after = _q32['fc_prod']
            _q1221 = 1.0 + _q427
            if held + _q1221 > _q852:
                _q1221 = max(0.0, _q852 - held)
            held = 0
            _q1120._lot(prod, _q1221, TPD * D, kind_tag or 'future', xy)
            D += _q741

    def _lot_dist(_q1120, lot):
        """[(step, prob)] arrival distribution of one lot (steps >= t)."""
        T, t = (_q1120.T, _q1120.t)
        it = lot['item']
        if lot['kind'] == 'carried':
            _q650, _q613 = (_q1120.final_step, max(_q1120.final_dump, t))
            _q1183 = T.P2rem.get(it)
            _q815 = [(t + _q1036, _q954) for _q1036, _q954 in _q1183.get(_q1120.hour, _q1183.get(0))] if _q1183 else [(TPD * (_q1120.day + 1), 1.0)]
            return [(s if s <= _q650 else _q613, _q954) for s, _q954 in _q815]
        A = lot['anchor']
        _q575 = lot['elapsed']
        _q650, _q613 = (_q1120.final_step, max(_q1120.final_dump, t))
        return [(A + _q922 if A + _q922 <= _q650 else _q613, _q954) for _q922, _q954 in T.from_anchor(it, _q575)]

    def supply(_q1120, H, q=None):
        key = (H, q)
        m = _q1120._memo.get(key)
        if m is not None:
            return m
        t, end = (_q1120.t, min(_q1120.t + H - 1, _q1120.final_step))
        _q946 = {}
        for lot in _q1120.lots:
            _q1221 = lot['units']
            it = lot['item']
            if lot['anchor'] > end:
                continue
            dist = _q1120._lot_dist(lot)
            if q is None:
                for s, _q954 in dist:
                    if t <= s <= end:
                        _q530 = _q946.setdefault(s, {})
                        _q530[it] = _q530.get(it, 0.0) + _q1221 * _q954
            else:
                _q369 = 0.0
                for s, _q954 in dist:
                    _q369 += _q954
                    if _q369 >= q - 1e-12:
                        if t <= s <= end:
                            _q530 = _q946.setdefault(s, {})
                            _q530[it] = _q530.get(it, 0.0) + _q1221
                        break
        _q1120._memo[key] = _q946
        return _q946

    def totals(_q1120, H, q=None):
        _q1206 = {}
        for _q530 in _q1120.supply(H, q).values():
            for it, _q1221 in _q530.items():
                _q1206[it] = _q1206.get(it, 0.0) + _q1221
        return _q1206

    def cum(_q1120, H, q=None):
        sup = _q1120.supply(H, q)
        _q946 = {it: [0.0] * H for it in PRODUCTS}
        for it in PRODUCTS:
            _q369 = 0.0
            _q1086 = _q946[it]
            for _q712 in range(H):
                _q369 += sup.get(_q1120.t + _q712, {}).get(it, 0.0)
                _q1086[_q712] = _q369
        return _q946

    def harvestable(_q1120, H):
        """Production schedule without labour lag: units ready on the tile at their anchor step (past-ready units at t)."""
        _q946 = {}
        end = _q1120.t + H - 1
        for lot in _q1120.lots:
            if lot['kind'] in ('carried',):
                continue
            s = max(_q1120.t, lot['anchor'])
            if s > end:
                continue
            _q530 = _q946.setdefault(s, {})
            _q530[lot['item']] = _q530.get(lot['item'], 0.0) + lot['units']
        return _q946

    def feed_demand(_q1120, H):
        """Wheat the animals eat: today's unfed standing animals now, then 1 per animal-day at h0 (planned lots and
        animals still in the shed / carried are counted from the next day)."""
        _q946 = {}
        pending = sum((n for k, n in _q1120.shed.items() if k in ANIMALS))
        pending += sum((n for inv in _q1120.inventories for k, n in inv.items() if k in ANIMALS))
        if _q1120._unfed_today:
            _q946[_q1120.t] = {'WHEAT': float(_q1120._unfed_today)}
        n = _q1120._n_animals + pending
        for D in range(_q1120.day + 1, FINAL_DAY + 1):
            s = TPD * D
            if s > _q1120.t + H - 1 or s > _q1120.final_step:
                break
            if n:
                _q946[s] = {'WHEAT': float(n)}
        return _q946

    def capacity_path(_q1120, _q1104, H=None, _q444=None, _q1257='feed', _q541=True):

        def _q915(x):
            _q946 = {}
            for s, _q1233 in (x or {}).items():
                if isinstance(_q1233, dict):
                    _q946[int(s)] = dict(_q1233)
                elif isinstance(_q1233, (list, tuple)):
                    _q530 = {}
                    for it, n in _q1233:
                        _q530[it] = _q530.get(it, 0) + n
                    _q946[int(s)] = _q530
                else:
                    _q946[int(s)] = {None: float(_q1233)}
            return _q946
        S, B = (_q915(_q1104), _q915(_q444))
        if H is None:
            _q785 = max(list(S) + list(B) + [_q1120.t + 47])
            H = _q785 - _q1120.t + 1
        W = _q1120.feed_demand(H) if _q1257 == 'feed' else _q915(_q1257)
        sup = _q1120.supply(H)
        stock = {k: float(_q1233) for k, _q1233 in _q1120.shed.items()}
        load = float(sum(stock.values()))
        cap = float(_q1120.cap)
        _q1060 = {'load': {}, 'room': {}, 'overflow': {}, 'short': {}, 'blocked': {}}
        peak = load
        _q980 = {}
        for s in range(_q1120.t, _q1120.t + H):
            for it, _q1221 in sup.get(s, {}).items():
                _q1186 = min(_q1221, max(0.0, cap - load))
                if _q1221 - _q1186 > 1e-09:
                    _q1060['overflow'][s] = _q1060['overflow'].get(s, 0.0) + (_q1221 - _q1186)
                stock[it] = stock.get(it, 0.0) + _q1186
                load += _q1186
            for it, n in W.get(s, {}).items():
                w = min(float(n), stock.get(it, 0.0))
                stock[it] = stock.get(it, 0.0) - w
                load -= w
            if _q541 and _q980:
                for it in list(_q980):
                    f = min(_q980[it], stock.get(it, 0.0))
                    if f > 0:
                        stock[it] -= f
                        load -= f
                        _q980[it] -= f
                    if _q980[it] <= 1e-09:
                        del _q980[it]
            for it, n in S.get(s, {}).items():
                if it is None:
                    sold = min(float(n), load)
                    load -= sold
                    short = float(n) - sold
                else:
                    sold = min(float(n), stock.get(it, 0.0))
                    stock[it] = stock.get(it, 0.0) - sold
                    load -= sold
                    short = float(n) - sold
                if short > 1e-09:
                    _q1060['short'].setdefault(s, {})[it] = short
                    if _q541 and it is not None:
                        _q980[it] = _q980.get(it, 0.0) + short
            for it, n in B.get(s, {}).items():
                b = min(float(n), max(0.0, cap - load))
                if float(n) - b > 1e-09:
                    _q1060['blocked'][s] = _q1060['blocked'].get(s, 0.0) + float(n) - b
                if it is not None:
                    stock[it] = stock.get(it, 0.0) + b
                load += b
            _q1060['load'][s] = load
            _q1060['room'][s] = cap - load
            peak = max(peak, load)
        _q1060['stock'] = {k: _q1233 for k, _q1233 in stock.items() if _q1233 > 1e-09}
        _q1060['unfilled'] = {k: _q1233 for k, _q1233 in _q980.items() if _q1233 > 1e-09}
        _q1060['peak'] = peak
        _q1060['feasible'] = not _q1060['overflow'] and (not _q1060['short'])
        return _q1060