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

def _get(_q857, k, _q475=None):
    if isinstance(_q857, dict):
        return _q857.get(k, _q475)
    g = getattr(_q857, 'get', None)
    if callable(g):
        try:
            return g(k, _q475)
        except TypeError:
            pass
    return getattr(_q857, k, _q475)

class _Tables:
    """Normalised, int-keyed view of one mode of the LAGS dict (with fallback to the other mode)."""

    def __init__(_q1052, _q25, mode):
        other = 'tape' if mode == 'planner' else 'planner'
        A, B = (_q25.get(mode, {}), _q25.get(other, {}))

        def _q921(key, item):
            _q1159 = A.get(key, {}).get(item)
            return _q1159 if _q1159 else B.get(key, {}).get(item)
        _q1052.P1, _q1052.S1, _q1052.P2, _q1052.P2rem, _q1052.cfrac = ({}, {}, {}, {}, {})
        _q1052.shed_frac, _q1052.hage, _q1052.p_fert, _q1052.p2_ong, _q1052.p2_cov, _q1052.anim = ({}, {}, {}, {}, {}, {})
        for _q675 in PRODUCTS:
            _q475 = _q921('P1', _q675)
            if _q475:
                _q888 = [0.0] * (LMAX + 1)
                for k, _q1159 in _q475.items():
                    _q888[min(LMAX, int(k))] += _q1159
                s = sum(_q888) or 1.0
                _q888 = [x / s for x in _q888]
                _q1052.P1[_q675] = _q888
                S = [0.0] * (LMAX + 2)
                _q319 = 0.0
                for _q652 in range(LMAX, -1, -1):
                    _q319 += _q888[_q652]
                    S[_q652] = _q319
                _q1052.S1[_q675] = S
            for key, _q512 in (('P2', _q1052.P2), ('P2rem', _q1052.P2rem)):
                _q475 = _q921(key, _q675)
                if _q475:
                    _q1112 = {}
                    for _q637, dist in _q475.items():
                        _q637 = int(_q637)
                        _q376 = TPD - _q637
                        _q319 = {}
                        for k, _q1159 in dist.items():
                            k = min(int(k), _q376)
                            _q319[k] = _q319.get(k, 0.0) + float(_q1159)
                        s = sum(_q319.values()) or 1.0
                        _q1112[_q637] = [(k, _q1159 / s) for k, _q1159 in sorted(_q319.items())]
                    _q512[_q675] = _q1112
            _q475 = _q921('carry_frac', _q675)
            if _q475:
                _q589 = {int(h): float(_q1159) for h, _q1159 in _q475.items()}
                _q771 = sum(_q589.values()) / len(_q589)
                _q1052.cfrac[_q675] = [_q589.get(h, _q771) for h in range(TPD)]
            _q1159 = A.get('shed_frac', {}).get(_q675, B.get('shed_frac', {}).get(_q675))
            _q1052.shed_frac[_q675] = 1.0 if _q1159 is None else float(_q1159)
        for c in ('WHEAT', 'CARROT', 'MELON'):
            _q475 = _q921('hage', c) or {}
            _q1052.hage[c] = {_q555: sorted(((int(k), float(_q1159)) for k, _q1159 in dist.items())) for _q555, dist in _q475.items()}
            _q1159 = A.get('p_fert', {}).get(c, B.get('p_fert', {}).get(c))
            _q1052.p_fert[c] = 0.0 if _q1159 is None else float(_q1159)
        for c in ('TOMATO', 'STRAWBERRY'):
            for key, _q512, _q492 in (('p2_ong', _q1052.p2_ong, 0.5), ('p2_cov', _q1052.p2_cov, 0.95)):
                _q1159 = A.get(key, {}).get(c, B.get(key, {}).get(c))
                _q512[c] = _q492 if _q1159 is None else float(_q1159)
        for _q336 in ANIMALS:
            _q1159 = A.get('anim', {}).get(_q336) or B.get('anim', {}).get(_q336) or {}
            _q1052.anim[_q336] = {k: float(_q1159.get(k, _DEF_ANIM[k])) for k in _DEF_ANIM}
        _q1052._conv = {}

    def from_anchor(_q1052, item, _q520):
        """Arrival offsets (hours after the anchor, h0 of the anchor day) of a unit ready at the anchor and not yet
        harvested e hours after it: [(offset, prob)], offsets >= e.  Cached."""
        key = (item, _q520)
        _q970 = _q1052._conv.get(key)
        if _q970 is not None:
            return _q970
        P1, _q54, P2 = (_q1052.P1.get(item), _q1052.S1.get(item), _q1052.P2.get(item))
        _q319 = {}
        if P1 is None or P2 is None:
            _q319[_q520] = 1.0
        else:
            _q526 = min(_q520, LMAX)
            surv = _q54[_q526]
            if surv <= 1e-09:
                for _q719, _q888 in P2.get(_q520 % TPD, P2.get(0, [(0, 1.0)])):
                    _q319[_q520 + _q719] = _q319.get(_q520 + _q719, 0.0) + _q888
            else:
                for _q26 in range(_q526, LMAX + 1):
                    w = P1[_q26]
                    if w <= 0.0:
                        continue
                    w /= surv
                    _q27 = max(_q26, _q520)
                    for _q719, _q888 in P2.get(_q27 % TPD, ()):
                        _q857 = _q27 + _q719
                        _q319[_q857] = _q319.get(_q857, 0.0) + w * _q888
        _q970 = sorted(_q319.items())
        _q1052._conv[key] = _q970
        return _q970

    def surv(_q1052, item, _q520):
        S = _q1052.S1.get(item)
        if S is None:
            return 1.0
        return S[min(max(_q520, 0), LMAX)]
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

    def __init__(_q1052, _q863, pd_state=None, mode='planner', lags=None, shed_capacity=100, planned=None, _q573=718, _q572=717):
        _q1052.mode = mode
        _q1052.T = _tables(mode, lags)
        _q1052.cap = shed_capacity
        _q1052.final_step = _q573
        _q1052.final_dump = _q572
        if pd_state is not None:
            me = pd_state.me
            step = pd_state.step
            tiles = pd_state.tiles
            shed = dict(pd_state.shed)
            _q672 = [dict(_q652) for _q652 in pd_state.inventories]
        else:
            me = int(_get(_q863, 'player', 0) or 0)
            step = _get(_q863, 'step', None)
            if step is None:
                step = TPD * int(_get(_q863, 'day', 0) or 0) + int(_get(_q863, 'hour', 0) or 0)
            step = int(step)
            farms = _get(_q863, 'farms', None) or []
            _q552 = farms[me] if len(farms) > me else {}
            tiles = _get(_q552, 'tiles', None) or []
            _q950 = _get(_q863, 'private', None) or {}
            shed = {k: int(_q1159) for k, _q1159 in (_get(_q950, 'shed', None) or {}).items() if _q1159}
            _q672 = [dict(_q652) for _q652 in _get(_q950, 'inventories', None) or []]
        _q1052.t = step
        _q1052.day, _q1052.hour = divmod(step, TPD)
        _q1052.shed = shed
        _q1052.inventories = _q672
        _q1052.lots = []
        _q1052._n_animals = 0
        _q1052._unfed_today = 0
        _q1052._build(tiles, planned or ())
        _q1052._memo = {}

    def _lot(_q1052, item, units, anchor, kind, xy=None):
        if units <= 1e-09:
            return
        _q520 = max(0, _q1052.t - anchor)
        _q1052.lots.append({'item': item, 'units': units, 'anchor': anchor, 'elapsed': _q520, 'kind': kind, 'xy': xy})

    def _build(_q1052, tiles, planned):
        day, hour, T = (_q1052.day, _q1052.hour, _q1052.T)
        for _q1197, _q1018 in enumerate(tiles):
            for x, t in enumerate(_q1018):
                if not isinstance(t, dict):
                    continue
                if t.get('kind') == 'PLANT' and t.get('crop') in CROPS:
                    _q1052._crop(t, (x, _q1197))
                elif t.get('animal') in ANIMALS:
                    _q1052._animal(t, (x, _q1197))
        h = hour
        for inv in _q1052.inventories:
            for _q675, n in inv.items():
                if _q675 not in PRODUCTS or not n:
                    continue
                _q589 = T.cfrac.get(_q675)
                _q1147 = n * (_q589[h] if _q589 else 1.0)
                if _q1147 > 1e-09:
                    _q1052.lots.append({'item': _q675, 'units': _q1147, 'anchor': _q1052.t, 'elapsed': 0, 'kind': 'carried', 'xy': None})
        for kind, _q475, n in planned:
            if kind in CROPS:
                _q549 = {'kind': 'PLANT', 'crop': kind, 'planted_day': int(_q475), 'watered_today': False, 'consecutive_unwatered': 1, 'yield_units': 0 if CROPS[kind][4] else 1, 'max_lifespan_step': -1, 'fertilized_until_day': -1}
                for _ in range(int(n)):
                    _q1052._crop(_q549, None, kind_tag='planned')
            elif kind in ANIMALS:
                _q549 = {'animal': kind, 'placed_day': int(_q475), 'yield_units': 0, 'fed_today': False, 'cared_today': False, 'pending_care_bonus': 0, 'fertilizer_available': False, 'consecutive_unfed': 0}
                for _ in range(int(n)):
                    _q1052._animal(_q549, None, kind_tag='planned')

    def _crop(_q1052, t, xy, kind_tag=None):
        c = t['crop']
        fyd, myd, _q679, _q789, ongoing = CROPS[c]
        day, T = (_q1052.day, _q1052.T)
        _q912 = int(t.get('planted_day', day))
        age = day - _q912
        units = int(t.get('yield_units', 0) or 0)
        watered = bool(t.get('watered_today'))
        _q598 = t.get('fertilized_until_day', -1)
        _q598 = -1 if _q598 is None else int(_q598)
        if ongoing:
            _q574 = _q912 + fyd
            _q952 = [_q574 + k * _q679 for k in range(_q789)]
            _q904 = [D for D in _q952 if D <= day]
            if units > 0:
                _q1052._lot(c, units, TPD * (_q904[-1] if _q904 else day), kind_tag or 'tile', xy)
            _q893, _q892 = (T.p2_ong[c], T.p2_cov[c])
            held = units
            for D in _q952:
                if D <= day or D > FINAL_DAY:
                    continue
                _q913 = D - 1
                if _q913 == day:
                    if _q598 >= day:
                        _q662 = 2.0 if watered else 1.0 + _q892
                    else:
                        _q662 = 1.0 + _q893
                else:
                    _q662 = 1.0 + (_q892 if _q598 >= _q913 else _q893)
                if held + _q662 > _q789:
                    _q662 = max(0.0, _q789 - held)
                held = 0
                _q1052._lot(c, _q662, TPD * D, kind_tag or 'future', xy)
            return
        _q1190 = (myd + 1) // 2
        mls = t.get('max_lifespan_step', -1)
        mls = -1 if mls is None else int(mls)
        if mls >= 0 and _q1052.t >= mls:
            _q1052._lot(c, units, TPD * day, kind_tag or 'tile', xy)
            return
        if _q598 >= day:
            _q436 = (('F', 1.0),)
        elif age > _q1190 or (age == _q1190 and watered):
            _q436 = (('U', 1.0),)
        else:
            pf = T.p_fert[c]
            _q436 = (('F', pf), ('U', 1.0 - pf))
        _q682 = age + 1 if watered else age
        _q523 = _q1052.hour
        for _q555, _q909 in _q436:
            if _q909 <= 0.0:
                continue
            _q330 = T.hage[c].get(_q555) or T.hage[c].get('U') or T.hage[c].get('F') or [(myd, 1.0)]
            _q401 = []
            for A, _q898 in _q330:
                if A < age:
                    continue
                w = _q898 * (T.surv(c, _q523) if A == age else 1.0)
                if w > 0:
                    _q401.append((A, w))
            if not _q401:
                _q401 = [(max(age, fyd), 1.0)]
            s = sum((w for _, w in _q401))
            for A, w in _q401:
                A = max(A, fyd)
                _q1147 = units
                for _q681 in range(max(_q682, _q1190), min(A, myd) + 1):
                    _q1143 = _q555 == 'F' or _q912 + _q681 <= _q598
                    _q1147 = min(_q789, _q1147 + (2 if _q1143 else 1))
                D = _q912 + A
                if D > FINAL_DAY:
                    continue
                _q1052._lot(c, _q1147 * _q909 * w / s, TPD * D, kind_tag or ('tile' if D <= day else 'future'), xy)

    def _animal(_q1052, t, xy, kind_tag=None):
        _q336 = t['animal']
        fyd, _q679, _q789, prod = ANIMALS[_q336]
        day, T = (_q1052.day, _q1052.T)
        _q32 = T.anim[_q336]
        _q923 = int(t.get('placed_day', day))
        units = int(t.get('yield_units', 0) or 0)
        fed, cared = (bool(t.get('fed_today')), bool(t.get('cared_today')))
        bank = float(t.get('pending_care_bonus', 0) or 0)
        if _q923 <= day:
            _q1052._n_animals += 1
            if not fed:
                _q1052._unfed_today += 1
        _q574 = _q923 + fyd
        if units > 0:
            k = (day - _q574) // _q679 if day >= _q574 else 0
            _q723 = _q574 + k * _q679 if day >= _q574 else day
            _q1052._lot(prod, units, TPD * _q723, kind_tag or 'tile', xy)
        _q1054 = T.shed_frac.get('FERTILIZER', 1.0)
        if _q923 < day and t.get('fertilizer_available'):
            _q1052._lot('FERTILIZER', _q1054, TPD * day, 'fert', xy)
        for D in range(max(day + 1, _q923 + 1), FINAL_DAY + 1):
            _q1052._lot('FERTILIZER', _q32['collect'] * _q1054, TPD * D, 'fert', xy)
        D = _q574 if _q574 > day else _q574 + ((day - _q574) // _q679 + 1) * _q679
        held = units
        after = None
        while D <= FINAL_DAY:
            _q913 = D - 1
            if after is None:
                if _q913 == day:
                    _q374 = bank if fed else bank * _q32['fed_prod']
                    after = 1.0 if fed and cared else _q32['fc_prod']
                else:
                    today = 1.0 if fed and cared else _q32['fc_non']
                    if _q923 > day:
                        today, bank = (0.0, 0.0)
                    _q359 = max(0, _q913 - max(day, _q923 - 1) - 1)
                    _q525 = bank + today + _q359 * _q32['fc_non']
                    _q374 = _q32['fed_prod'] * _q525
                    after = _q32['fc_prod']
            else:
                _q374 = _q32['fed_prod'] * (after + (_q679 - 1) * _q32['fc_non'])
                after = _q32['fc_prod']
            _q1147 = 1.0 + _q374
            if held + _q1147 > _q789:
                _q1147 = max(0.0, _q789 - held)
            held = 0
            _q1052._lot(prod, _q1147, TPD * D, kind_tag or 'future', xy)
            D += _q679

    def _lot_dist(_q1052, lot):
        """[(step, prob)] arrival distribution of one lot (steps >= t)."""
        T, t = (_q1052.T, _q1052.t)
        _q675 = lot['item']
        if lot['kind'] == 'carried':
            _q594, _q558 = (_q1052.final_step, max(_q1052.final_dump, t))
            _q1112 = T.P2rem.get(_q675)
            _q753 = [(t + _q970, _q888) for _q970, _q888 in _q1112.get(_q1052.hour, _q1112.get(0))] if _q1112 else [(TPD * (_q1052.day + 1), 1.0)]
            return [(s if s <= _q594 else _q558, _q888) for s, _q888 in _q753]
        A = lot['anchor']
        _q520 = lot['elapsed']
        _q594, _q558 = (_q1052.final_step, max(_q1052.final_dump, t))
        return [(A + _q857 if A + _q857 <= _q594 else _q558, _q888) for _q857, _q888 in T.from_anchor(_q675, _q520)]

    def supply(_q1052, H, q=None):
        key = (H, q)
        m = _q1052._memo.get(key)
        if m is not None:
            return m
        t, end = (_q1052.t, min(_q1052.t + H - 1, _q1052.final_step))
        _q880 = {}
        for lot in _q1052.lots:
            _q1147 = lot['units']
            _q675 = lot['item']
            if lot['anchor'] > end:
                continue
            dist = _q1052._lot_dist(lot)
            if q is None:
                for s, _q888 in dist:
                    if t <= s <= end:
                        _q475 = _q880.setdefault(s, {})
                        _q475[_q675] = _q475.get(_q675, 0.0) + _q1147 * _q888
            else:
                _q319 = 0.0
                for s, _q888 in dist:
                    _q319 += _q888
                    if _q319 >= q - 1e-12:
                        if t <= s <= end:
                            _q475 = _q880.setdefault(s, {})
                            _q475[_q675] = _q475.get(_q675, 0.0) + _q1147
                        break
        _q1052._memo[key] = _q880
        return _q880

    def totals(_q1052, H, q=None):
        _q1133 = {}
        for _q475 in _q1052.supply(H, q).values():
            for _q675, _q1147 in _q475.items():
                _q1133[_q675] = _q1133.get(_q675, 0.0) + _q1147
        return _q1133

    def cum(_q1052, H, q=None):
        sup = _q1052.supply(H, q)
        _q880 = {_q675: [0.0] * H for _q675 in PRODUCTS}
        for _q675 in PRODUCTS:
            _q319 = 0.0
            _q1018 = _q880[_q675]
            for _q652 in range(H):
                _q319 += sup.get(_q1052.t + _q652, {}).get(_q675, 0.0)
                _q1018[_q652] = _q319
        return _q880

    def harvestable(_q1052, H):
        """Production schedule without labour lag: units ready on the tile at their anchor step (past-ready units at t)."""
        _q880 = {}
        end = _q1052.t + H - 1
        for lot in _q1052.lots:
            if lot['kind'] in ('carried',):
                continue
            s = max(_q1052.t, lot['anchor'])
            if s > end:
                continue
            _q475 = _q880.setdefault(s, {})
            _q475[lot['item']] = _q475.get(lot['item'], 0.0) + lot['units']
        return _q880

    def feed_demand(_q1052, H):
        """Wheat the animals eat: today's unfed standing animals now, then 1 per animal-day at h0 (planned lots and
        animals still in the shed / carried are counted from the next day)."""
        _q880 = {}
        pending = sum((n for k, n in _q1052.shed.items() if k in ANIMALS))
        pending += sum((n for inv in _q1052.inventories for k, n in inv.items() if k in ANIMALS))
        if _q1052._unfed_today:
            _q880[_q1052.t] = {'WHEAT': float(_q1052._unfed_today)}
        n = _q1052._n_animals + pending
        for D in range(_q1052.day + 1, FINAL_DAY + 1):
            s = TPD * D
            if s > _q1052.t + H - 1 or s > _q1052.final_step:
                break
            if n:
                _q880[s] = {'WHEAT': float(n)}
        return _q880

    def capacity_path(_q1052, _q1036, H=None, _q391=None, _q1182='feed', _q486=True):

        def _q851(x):
            _q880 = {}
            for s, _q1159 in (x or {}).items():
                if isinstance(_q1159, dict):
                    _q880[int(s)] = dict(_q1159)
                elif isinstance(_q1159, (list, tuple)):
                    _q475 = {}
                    for _q675, n in _q1159:
                        _q475[_q675] = _q475.get(_q675, 0) + n
                    _q880[int(s)] = _q475
                else:
                    _q880[int(s)] = {None: float(_q1159)}
            return _q880
        S, B = (_q851(_q1036), _q851(_q391))
        if H is None:
            _q723 = max(list(S) + list(B) + [_q1052.t + 47])
            H = _q723 - _q1052.t + 1
        W = _q1052.feed_demand(H) if _q1182 == 'feed' else _q851(_q1182)
        sup = _q1052.supply(H)
        stock = {k: float(_q1159) for k, _q1159 in _q1052.shed.items()}
        load = float(sum(stock.values()))
        cap = float(_q1052.cap)
        _q992 = {'load': {}, 'room': {}, 'overflow': {}, 'short': {}, 'blocked': {}}
        peak = load
        _q914 = {}
        for s in range(_q1052.t, _q1052.t + H):
            for _q675, _q1147 in sup.get(s, {}).items():
                _q1114 = min(_q1147, max(0.0, cap - load))
                if _q1147 - _q1114 > 1e-09:
                    _q992['overflow'][s] = _q992['overflow'].get(s, 0.0) + (_q1147 - _q1114)
                stock[_q675] = stock.get(_q675, 0.0) + _q1114
                load += _q1114
            for _q675, n in W.get(s, {}).items():
                w = min(float(n), stock.get(_q675, 0.0))
                stock[_q675] = stock.get(_q675, 0.0) - w
                load -= w
            if _q486 and _q914:
                for _q675 in list(_q914):
                    f = min(_q914[_q675], stock.get(_q675, 0.0))
                    if f > 0:
                        stock[_q675] -= f
                        load -= f
                        _q914[_q675] -= f
                    if _q914[_q675] <= 1e-09:
                        del _q914[_q675]
            for _q675, n in S.get(s, {}).items():
                if _q675 is None:
                    sold = min(float(n), load)
                    load -= sold
                    short = float(n) - sold
                else:
                    sold = min(float(n), stock.get(_q675, 0.0))
                    stock[_q675] = stock.get(_q675, 0.0) - sold
                    load -= sold
                    short = float(n) - sold
                if short > 1e-09:
                    _q992['short'].setdefault(s, {})[_q675] = short
                    if _q486 and _q675 is not None:
                        _q914[_q675] = _q914.get(_q675, 0.0) + short
            for _q675, n in B.get(s, {}).items():
                b = min(float(n), max(0.0, cap - load))
                if float(n) - b > 1e-09:
                    _q992['blocked'][s] = _q992['blocked'].get(s, 0.0) + float(n) - b
                if _q675 is not None:
                    stock[_q675] = stock.get(_q675, 0.0) + b
                load += b
            _q992['load'][s] = load
            _q992['room'][s] = cap - load
            peak = max(peak, load)
        _q992['stock'] = {k: _q1159 for k, _q1159 in stock.items() if _q1159 > 1e-09}
        _q992['unfilled'] = {k: _q1159 for k, _q1159 in _q914.items() if _q1159 > 1e-09}
        _q992['peak'] = peak
        _q992['feasible'] = not _q992['overflow'] and (not _q992['short'])
        return _q992