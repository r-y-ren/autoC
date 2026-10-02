"""PD - day planner implementing the DSM rule book R1-R8 for days >= D (Original work, Shawn404, 25 Sep 2026).

    rules = load_rules()                    # embedded DSM tables (results/portable/wf31_rules_*_DSM.json)
    plan = plan_day(state, rules, D=11)     # state = pd_state.parse_obs(obs) at hour 0 (any hour works)

plan_day returns a dict:
  active        False before day D (the tape runs) - then nothing else is filled
  targets       {y: {...}} per product y in S T C W cow sheep goose: window, DSM rule value, planted so far in the
                window, remaining, today's quota (after caps / capacity / cash), intended window total
  ops           [(op, (x, y), arg)] PLANT / BUILD_COOP / BUILD_PASTURE / PLACE / CLEAR for pd_tasks.due_tasks
  land          [(hour, quadrant)] BUY_LAND orders (R7)
  hires         hands to hire today (R8, sized to the day's task-turns)
  orders        {hour: [market orders]} purchases sequenced by cash (HIRE, feed WHEAT, BUY_LAND, BUY_ANIMAL,
                BUY_SEED, FERTILIZER); sales are not planned here (pd_market)
  deferred      purchases the cash could not cover today
  cash          {'start', 'spend_today', 'projection': [(day, closing cash)], 'min'}
  fert_wheat    R5 flag for pd_tasks
  tasks         pd_tasks.due_tasks(state, plan) for the executor; task_turns, units_needed
Rules (wf31_rules.txt / wf31_design.txt section 2):
  R1 tomatoes by the additive window rule (PIZ +7.1, FRM +3.0 on days 9-11 ...), days <= 20, standing cap = the
     day-20 target 8.6 + 5.9 x tomato shops (+2);
  R2 carrots by the additive window rule (PET +7-9 per window, FRM joins late), days <= 27;
  R3 strawberries on days 12-17 only (additive rule with own -0.6/-0.3 and rival -0.10 terms), standing cap;
  R4 animals by the additive window rules (geese BAK +4.3, sheep YRN +6.6, cows milk shops), standing caps;
  R5 wheat fills the remaining free tiles (feed + sales), fertilised when the fertiliser quote <= $55;
  R6 no melons;
  R7 land: next quadrant when the planned tiles exceed the free tiles and cash covers the price plus the day
     (SE not before step 266);
  R8 hands sized to the day's task-turns, the plan scaled down (wheat first) to the executor's capacity.
Within a window, strawberries, animals and the day-18 tomato block are front-loaded (DSM: 75-95% on the window's
first day); other crops are spread evenly over the window's remaining days.
CS B1 (27 Sep, cfg alloc='wheat_first', default None = the allocation above): a protected wheat rotation W* first, the
quota crops on the rest, age-3 fertilised wheat cut and replanted in one chain, its own capacity trim (_wf_alloc,
results/portable/sys_design.txt 6.1 + REVIEW RV6 step 4).  Purchasing is unchanged in both modes.
P8 (28 Sep, cfg no_geese / tom_cap / herd_mult / herd_cap / late_tc_prio / wheat_bias, all off by default): the anti-DSM
volume style (bigger cow + sheep herds, no geese, few tomatoes, more wheat) and DSM's late wheat -> tomato / carrot
rotation; results/portable/p8_plan.txt.
"""
import math
from pd_state import CROPS, ANIMALS, SHOP_TYPES, FINAL_DAY, QUAD_TILES, LAND_PRICES, LAND_ORDER, access_dist, quadrant_of, hire_cost, fib
import pd_tasks as PT
ADDITIVE = {'S_6_8': (1.333, 0.316, 7.674, -0.576, 7.067, 1.535, 6.559, 7.536), 'T_6_8': (0.004, 0.302, -0.044, 0.014, -0.027, -0.012, -0.034, -0.011), 'C_6_8': (0.043, -0.028, -0.05, -0.051, -0.128, 1.175, -0.033, -0.155), 'W_6_8': (10.711, 11.442, 1.758, 10.889, 2.259, 9.231, 2.54, 1.796), 'cow_6_8': (1.796, 5.177, 1.441, 0.533, 4.508, 1.846, 4.784, 1.518), 'sheep_6_8': (0.244, -0.07, 0.059, 6.823, -0.085, 0.173, -0.058, 0.042), 'goose_6_8': (2.292, 0.1, 2.09, -0.893, -0.132, 2.323, -0.147, 2.124), 'S_9_11': (3.704, 3.423, 11.843, 3.598, 12.325, 3.264, 12.256, 11.033, -0.747, -0.157), 'T_9_11': (2.837, 7.103, 0.334, 2.704, 0.034, 2.104, 0.843, 3.015, 0.949, -0.045), 'C_9_11': (0.24, -0.139, 0.217, -0.14, -0.523, 9.802, 0.145, -0.026, 0.628, 0.43), 'W_9_11': (16.222, 14.367, 11.999, 14.311, 12.719, 9.336, 10.665, 10.727, -0.663, 0.059), 'cow_9_11': (0.633, 2.298, 0.793, 0.7, 2.425, 0.614, 2.533, 0.751, -0.242, -0.088), 'sheep_9_11': (0.834, 0.645, 0.818, 6.593, 0.741, 0.849, 0.723, 0.794, -0.739, -0.032), 'goose_9_11': (4.311, 1.291, 3.243, 0.042, 1.037, 3.4, 1.109, 2.896, -0.632, -0.029), 'S_12_14': (2.533, 2.188, 8.895, 2.212, 8.968, 2.303, 8.934, 7.989, -0.598, -0.1), 'T_12_14': (2.046, 5.564, 0.439, 1.077, -0.23, 1.029, 0.604, 3.466, -0.374, -0.092), 'C_12_14': (0.607, -0.608, -0.182, 0.229, -0.707, 9.096, 0.16, 0.618, 0.148, 0.187), 'W_12_14': (7.53, 4.737, 5.468, 4.402, 5.33, 1.341, 3.656, 2.773, 0.178, -0.054), 'cow_12_14': (0.062, 0.602, 0.11, 0.125, 0.662, 0.117, 0.797, 0.1, -0.101, -0.021), 'sheep_12_14': (0.48, 0.329, 0.416, 4.33, 0.351, 0.47, 0.458, 0.36, -0.478, -0.058), 'goose_12_14': (0.028, -0.008, 0.026, 0.003, 0.029, 0.01, -0.0, 0.013, -0.003, -0.004), 'S_15_17': (1.32, 0.792, 4.743, 0.933, 4.589, 1.29, 4.671, 4.073, -0.313, -0.097), 'T_15_17': (1.561, 4.307, 0.293, 0.842, 0.074, 0.59, 0.493, 2.818, -0.288, -0.035), 'C_15_17': (1.15, -0.587, -0.506, 0.62, -0.904, 7.816, -0.194, 0.621, 0.206, 0.014), 'W_15_17': (6.248, 3.839, 4.773, 4.69, 4.345, 1.691, 2.59, 1.163, -0.005, -0.003), 'cow_15_17': (0.027, 0.131, 0.032, 0.049, 0.156, 0.042, 0.152, 0.04, -0.03, -0.008), 'sheep_15_17': (0.244, 0.115, 0.213, 2.568, 0.259, 0.187, 0.176, 0.189, -0.297, -0.044), 'goose_15_17': (0.015, 0.021, 0.019, 0.003, 0.008, 0.004, -0.004, 0.006, -0.004, -0.002), 'T_18_20': (1.147, 2.451, 1.102, 0.363, 0.583, 0.652, 0.801, 2.445, -0.084, -0.081), 'C_18_20': (1.087, -0.37, -0.072, 0.64, -0.791, 7.225, 0.14, 1.016, 0.372, -0.1), 'W_18_20': (5.41, 3.608, 3.397, 3.842, 4.215, 1.625, 1.666, 0.954, 0.213, -0.072), 'cow_18_20': (0.018, 0.12, 0.013, 0.024, 0.124, 0.013, 0.107, 0.034, -0.01, -0.026), 'sheep_18_20': (0.197, 0.211, 0.059, 1.387, 0.08, 0.092, 0.054, 0.136, -0.151, -0.071), 'T_21_23': (-0.011, -0.002, 0.009, -0.015, -0.016, -0.026, -0.002, 0.009, 0.004, -0.0), 'C_21_23': (1.942, -0.323, 1.008, 0.513, -0.537, 7.607, 0.411, 3.331, 0.496, -0.282), 'W_21_23': (4.708, 6.171, 3.689, 3.539, 4.001, 0.363, 2.602, 1.831, 0.29, -0.15), 'sheep_21_23': (0.052, 0.035, 0.065, 0.491, 0.037, -0.032, 0.032, 0.016, -0.082, -0.003), 'T_24_27': (0.003, 0.013, 0.003, -0.002, -0.004, -0.003, 0.006, 0.006, -0.002, 0.0), 'C_24_27': (1.985, 1.286, 2.141, 0.873, 0.146, 8.771, 2.601, 6.771, 0.433, -0.46), 'W_24_27': (5.14, 4.8, 3.196, 3.64, 3.966, 1.301, 1.911, 1.217, 0.231, -0.083), 'sheep_24_27': (0.009, 0.007, 0.018, 0.09, -0.015, -0.002, -0.011, -0.008, -0.023, 0.009), 'goose_24_27': (0.005, 0.003, 0.002, -0.003, 0.0, -0.004, 0.001, 0.001, -0.0, -0.001)}
STANDING = {'P_STRAWBERRY_d8': (11.007, 6.722, -0.046, 1.769), 'P_STRAWBERRY_d11': (12.149, 9.376, -0.086, 1.952), 'P_STRAWBERRY_d14': (12.192, 8.977, -0.036, 2.294), 'P_STRAWBERRY_d17': (10.062, 8.358, 0.001, 3.399), 'P_STRAWBERRY_d20': (-2.348, 6.515, 0.112, 4.705), 'P_STRAWBERRY_d23': (-1.651, 4.389, -0.021, 4.449), 'P_STRAWBERRY_d26': (-2.191, 2.851, -0.001, 3.613), 'P_TOMATO_d8': (-0.05, 0.191, 0.0, 0.347), 'P_TOMATO_d11': (3.901, 4.307, 0.014, 3.058), 'P_TOMATO_d14': (5.076, 5.84, 0.057, 3.657), 'P_TOMATO_d17': (6.155, 6.032, 0.079, 4.218), 'P_TOMATO_d20': (8.577, 5.897, -0.024, 4.028), 'P_TOMATO_d23': (6.607, 3.019, -0.075, 3.234), 'P_TOMATO_d26': (4.782, 1.58, -0.03, 2.414), 'P_CARROT_d8': (-0.074, 0.446, -0.186, 0.932), 'P_CARROT_d11': (-0.29, 4.67, 0.839, 4.403), 'P_CARROT_d14': (-1.146, 4.502, 0.666, 4.954), 'P_CARROT_d17': (-1.594, 4.229, 0.437, 4.961), 'P_CARROT_d20': (-0.942, 4.832, 0.298, 5.971), 'P_CARROT_d23': (2.221, 6.228, 0.049, 7.59), 'P_CARROT_d26': (10.461, 7.125, -0.197, 7.427), 'A_COW_d8': (4.699, 3.418, 0.029, 0.821), 'A_COW_d11': (3.718, 2.802, 0.325, 1.252), 'A_COW_d14': (2.891, 1.945, 0.46, 1.494), 'A_COW_d17': (1.743, 1.556, 0.575, 1.728), 'A_COW_d20': (0.82, 1.778, 0.487, 1.739), 'A_COW_d23': (-0.069, 1.652, 0.513, 1.794), 'A_COW_d26': (-0.778, 1.817, 0.364, 1.853), 'A_SHEEP_d8': (2.643, 6.725, 0.173, 0.709), 'A_SHEEP_d11': (2.426, 6.569, 0.145, 0.633), 'A_SHEEP_d14': (1.854, 4.936, 0.306, 0.916), 'A_SHEEP_d17': (1.659, 4.074, 0.355, 1.304), 'A_SHEEP_d20': (1.728, 3.785, 0.281, 1.556), 'A_SHEEP_d23': (1.24, 3.228, 0.304, 1.899), 'A_SHEEP_d26': (0.273, 3.293, 0.224, 1.935), 'A_GOOSE_d8': (0.717, 1.782, 0.071, 1.682), 'A_GOOSE_d11': (4.324, 2.18, 0.552, 2.143), 'A_GOOSE_d14': (3.397, 1.425, 0.462, 2.188), 'A_GOOSE_d17': (3.407, 1.15, 0.471, 2.248), 'A_GOOSE_d20': (3.017, 1.147, 0.463, 2.196), 'A_GOOSE_d23': (2.974, 0.991, 0.441, 2.204), 'A_GOOSE_d26': (2.966, 0.881, 0.425, 2.188), 'P_WHEAT_d8': (8.753, -0.582, -0.213, 3.901), 'P_WHEAT_d11': (26.181, 2.331, 0.151, 4.347), 'P_WHEAT_d14': (19.063, 2.154, 0.068, 5.064), 'P_WHEAT_d17': (14.569, 1.225, 0.1, 4.789), 'P_WHEAT_d20': (17.106, 1.735, 0.051, 6.235), 'P_WHEAT_d23': (20.306, 2.308, 0.002, 7.687), 'P_WHEAT_d26': (18.737, 1.71, 0.05, 7.842)}
WINDOWS = ((6, 8), (9, 11), (12, 14), (15, 17), (18, 20), (21, 23), (24, 27))
PRODUCTS_Y = ('S', 'T', 'C', 'W', 'cow', 'sheep', 'goose')
CROP_OF = {'S': 'STRAWBERRY', 'T': 'TOMATO', 'C': 'CARROT', 'W': 'WHEAT'}
ANIMAL_OF = {'cow': 'COW', 'sheep': 'SHEEP', 'goose': 'GOOSE'}
ITEM_OF = {'S': 'STRAWBERRY', 'T': 'TOMATO', 'C': 'CARROT', 'W': 'WHEAT', 'cow': 'MILK', 'sheep': 'WOOL', 'goose': 'EGG'}
LAST_DAY = {'S': 17, 'T': 20, 'C': 27, 'W': 26, 'cow': 20, 'sheep': 23, 'goose': 20}
FIRST_DAY = {'S': 9}
FRONT_LOADED = {'S', 'cow', 'sheep', 'goose'}
STRUCT = {'GOOSE': 'COOP', 'COW': 'PASTURE', 'SHEEP': 'PASTURE'}
QUAD_PEN = {'S': {'NW': 0.0, 'NE': 0.0, 'SW': 0.6, 'SE': 0.8}, 'T': {'SW': 0.0, 'NW': 0.4, 'SE': 0.5, 'NE': 1.0}, 'C': {'SW': 0.0, 'SE': 0.1, 'NW': 0.5, 'NE': 1.0}, 'W': {'NW': 0.0, 'NE': 0.0, 'SW': 0.0, 'SE': 0.0}, 'A': {'NE': 0.0, 'SW': 0.0, 'NW': 0.2, 'SE': 0.6}}
DIST_W = {'A': 1.0, 'T': 0.8, 'S': 0.6, 'C': 0.4, 'W': 0.15}
WF_DIST_W = {'A': 1.0, 'W': 0.4, 'C': 0.4, 'S': 0.3, 'T': 0.15}
WF_LAST_DAY = {'W': 27, 'C': 27}
WF_WSTAR = (1.2, 0.2, 0.3)
WF_LAND_Q = {'T': 0.55, 'goose': 0.6}
WF_FILL_C = (20, 27)
WF_CAP = (24.0, 22.3)
CFG = {'max_hands': 12, 'min_hands': 2, 'turns_per_task': 2.2, 'l2_done_share': 0.85, 'turns_per_unit': 24, 'reserve': 60.0, 'haircut': 0.75, 'fert_buy_max': 60, 'se_step': 266, 'wheat_feed_rate': 0.8, 's_first_day': 9, 'w_feed_tiles': None, 'animals': True, 'last_day': None, 'task_opts': None, 'land_after_trim': False, 'prev_hires': None, 'target_mult': None, 'land_steps': None, 'hire_ladder': None, 'fert_wheat_q': 55, 'place_shed': False, 'cash_defer': False, 'alloc': None, 'wf_wstar': None, 'wf_wstar_last': 27, 'wf_w_margin': 4, 'wf_fill_carrot': WF_FILL_C, 'wf_tpt': 1.95, 'wf_l2': 1.0, 'wf_fert_crops': None, 'wf_cap': None, 'wf_dist_w': None, 'wf_quota_land': None, 'wf_last_day': None, 'wf_s_prio': False, 'cow_gate': None, 'no_geese': False, 'tom_cap': None, 'herd_mult': None, 'herd_cap': None, 'late_tc_prio': None, 'wheat_bias': None}

def load_rules(_q750=None):
    _q376 = dict(ADDITIVE)
    _q1163 = dict(STANDING)
    if _q750:
        import json
        import os
        a = json.load(open(os.path.join(_q750, 'wf31_rules_additive_DSM.json')))
        _q376 = {k: tuple(_q1233['beta']) for k, _q1233 in a.items()}
        t = json.load(open(os.path.join(_q750, 'wf31_rules_targets_DSM.json')))
        _q1163 = {k: (_q1233['a'], _q1233['b'], _q1233['c'], _q1233['sd']) for k, _q1233 in t.items()}
    return {'additive': _q376, 'standing': _q1163, 'cfg': dict(CFG)}

def window_of(day):
    for _q531, _q532 in WINDOWS:
        if _q531 <= day <= _q532:
            return (_q531, _q532)
    return None

def shop_vector(shop_counts):
    return [float(shop_counts.get(t, 0)) for t in SHOP_TYPES]

def rule_value(rules, _q1272, _q1255, shop_counts, own, rival):
    b = rules['additive'].get('%s_%d_%d' % (_q1272, _q1255[0], _q1255[1]))
    if b is None:
        return 0.0
    _q1233 = sum((_q413 * _q1270 for _q413, _q1270 in zip(b[:8], shop_vector(shop_counts))))
    if len(b) > 8:
        _q1233 += b[8] * own + b[9] * rival
    _q1201 = (rules.get('cfg') or {}).get('target_mult')
    if _q1201 and _q1272 in _q1201 and (_q1233 > 0):
        _q1233 *= float(_q1201[_q1272])
    _q1031 = (rules.get('cfg') or {}).get('_qscale')
    if _q1031 and _q1272 in _q1031 and (_q1233 > 0):
        _q1233 *= float(_q1031[_q1272])
    _q702 = _herd_mult(rules, _q1272)
    if _q702 is not None and _q1233 > 0:
        _q1233 *= _q702
    return _q1233

def _herd_mult(rules, _q1272):
    """P8 cfg herd_mult factor of product y (an animal), or None."""
    _q702 = (rules.get('cfg') or {}).get('herd_mult')
    if not _q702 or _q1272 not in ANIMAL_OF:
        return None
    f = _q702.get(ANIMAL_OF[_q1272], _q702.get(_q1272))
    return None if f is None else float(f)

def shops_at_day(shops, day, today):
    """Shops open at hour 0 of `day` (<= today): the town reveals one shop on days 3, 6, 9, ..., 24 (max 8), in
    order, so the first day // 3 entries of today's list."""
    n = min(len(shops), day // 3)
    _q946 = {}
    for s in shops[:n]:
        _q946[s] = _q946.get(s, 0) + 1
    return _q946

def _stock_now(state, _q1272):
    if _q1272 in CROP_OF:
        return state.crop_tiles(CROP_OF[_q1272])
    return state.n_animals(ANIMAL_OF[_q1272])

def _rival_now(state, _q1272):
    _q1036 = state.rival
    if _q1272 in CROP_OF:
        return _q1036.crop_tiles.get(CROP_OF[_q1272], 0)
    return _q1036.animals.get(ANIMAL_OF[_q1272], 0)

def _planted_between(state, _q1272, _q531, _q532):
    if _q1272 in CROP_OF:
        return state.planted_in(CROP_OF[_q1272], _q531, _q532)
    return state.placed_in(ANIMAL_OF[_q1272], _q531, _q532)

def _rival_planted_between(state, _q1272, _q531, _q532):
    _q1036 = state.rival
    key = CROP_OF.get(_q1272) or ANIMAL_OF.get(_q1272)
    src = _q1036.planted_by_day if _q1272 in CROP_OF else _q1036.placed_by_day
    return sum((n for (k, _q530), n in src.items() if k == key and _q531 <= _q530 <= _q532))

def standing_cap(rules, _q1272, state, day):
    """DSM standing-capacity target (+2) for the next census day >= today (R5 view), or None."""
    key = {'S': 'P_STRAWBERRY', 'T': 'P_TOMATO', 'cow': 'A_COW', 'sheep': 'A_SHEEP', 'goose': 'A_GOOSE'}.get(_q1272)
    if key is None:
        return None
    item = {'S': 'STRAWBERRY', 'T': 'TOMATO', 'cow': 'MILK', 'sheep': 'WOOL', 'goose': 'EGG'}[_q1272]
    if _q1272 == 'T':
        _q477 = 20
    else:
        _q477 = next((_q530 for _q530 in (11, 14, 17, 20, 23, 26) if _q530 >= day), 26)
    f = rules['standing'].get('%s_d%d' % (key, _q477))
    if f is None:
        return None
    a, b, c, _ = f
    _q1233 = a + b * state.demand(item) + c * _rival_now(state, _q1272) + 2.0
    _q1201 = (rules.get('cfg') or {}).get('target_mult')
    if _q1201 and _q1272 in _q1201:
        _q1233 *= float(_q1201[_q1272])
    _q1031 = (rules.get('cfg') or {}).get('_qscale')
    if _q1031 and _q1272 in _q1031:
        _q1233 *= float(_q1031[_q1272])
    _q702 = _herd_mult(rules, _q1272)
    if _q702 is not None:
        _q1233 *= _q702
    return _q1233

def window_targets(state, rules, day=None, D=None):
    """{y: info} for the window containing `day` (default today), with the rule evaluated on the shops open at the
    window's first day and the own / rival stock at the end of the day before it (reconstructed from planted days).

    Carry-over: the handover days D = 11 / 14 / 17 are LAST days of windows, so a capacity-trimmed remainder would be
    lost; the shortfall of the previous window (its rule minus its plantings, recomputed statelessly) is planted on
    the first day of the next window ('carry'), and later days of that window do not count the carried plantings
    against the window's own target.  Only for windows whose last day was run by PD (>= D)."""
    day = state.day if day is None else day
    _q1255 = window_of(day)
    _q946 = {}
    if _q1255 is None:
        return _q946
    _q531, _q532 = _q1255
    _q1111 = shops_at_day(state.shops, _q531, day)
    _q742 = WINDOWS.index(_q1255)
    prev = WINDOWS[_q742 - 1] if _q742 > 0 else None
    if prev is not None and D is not None and (prev[1] < D):
        prev = None
    for _q1272 in PRODUCTS_Y:
        carry = 0
        if prev is not None and _q1272 != 'W' and (_first_day(_q1272, rules) <= prev[1] <= _ld(_q1272, rules)):
            _q955, _q956 = prev
            _q994 = _planted_between(state, _q1272, _q955, _q956)
            _q951 = max(0, _stock_now(state, _q1272) - _planted_between(state, _q1272, _q955, day - 1))
            _q1074 = max(0, _rival_now(state, _q1272) - _rival_planted_between(state, _q1272, _q955, day - 1))
            _q1093 = rule_value(rules, _q1272, prev, shops_at_day(state.shops, _q955, day), _q951, _q1074)
            carry = max(0, int(round(_q1093)) - _q994)
        _q995 = _planted_between(state, _q1272, _q531, day - 1)
        planted = _q995 - (min(carry, _planted_between(state, _q1272, _q531, _q531)) if day > _q531 else 0)
        own0 = max(0, _stock_now(state, _q1272) - _q995)
        _q1073 = max(0, _rival_now(state, _q1272) - _rival_planted_between(state, _q1272, _q531, day - 1))
        _q1095 = rule_value(rules, _q1272, _q1255, _q1111, own0, _q1073)
        _q946[_q1272] = {'window': _q1255, 'rule': _q1095, 'own0': own0, 'rival0': _q1073, 'planted': planted, 'remaining': max(0, int(round(_q1095)) - planted), 'carry': carry if day == _q531 else 0}
    return _q946

def _ripe_for_reuse(_q513, day):
    if _q513.ongoing:
        return False
    if _q513.decaying:
        return True
    if not _q513.harvestable():
        return False
    if _q513.crop == 'WHEAT':
        return _q513.age >= 3
    if _q513.crop == 'CARROT':
        return _q513.age >= 3
    if _q513.crop == 'MELON':
        return _q513.age >= 12 or (_q513.age >= 10 and _q513.units >= 6)
    return False

def _free_inventory(state, _q905, _q782):
    """[(xy, prep_cost, kind, not_before)] tiles a PLANT/BUILD can use today."""
    day = state.day
    inv = []
    for xy in state.empty:
        inv.append((xy, 0, 'empty', 0))
    for xy in state.weeds:
        inv.append((xy, 1, 'weed', 0))
    for xy, _q513 in state.crops.items():
        if _q513.ongoing and _q513.prods_left == 0:
            inv.append((xy, 1 + (_q513.units > 0), 'spent', 0))
        elif _ripe_for_reuse(_q513, day):
            inv.append((xy, 1 + (0 if _q513.age >= CROPS[_q513.crop]['myd'] else 1), 'ripe', 0))
    for q in _q905:
        for xy in QUAD_TILES[q]:
            if xy in state.locked:
                inv.append((xy, 0, 'new', _q782[q] + 1))
    return inv

def _animal_neighbour_bonus(state, xy):
    x, _q1272 = xy
    n = 0
    for _q573, _q574 in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (x + _q573, _q1272 + _q574) in state.animals or (x + _q573, _q1272 + _q574) in state.structures:
            n += 1
    return 0.3 * n

def _score(state, xy, _q1012, _q671, _q553=None):
    q = quadrant_of(*xy)
    s = _q1012 * 0.7 + access_dist(xy) * (DIST_W if _q553 is None else _q553)[_q671] + 2.0 * QUAD_PEN[_q671][q]
    if _q671 == 'A':
        s -= _animal_neighbour_bonus(state, xy)
    return s

def _crop_units(crop, fert=True):
    return {'WHEAT': 5.0 if fert else 4.0, 'CARROT': 3.6 if fert else 3.0, 'TOMATO': 7.0 if fert else 4.0, 'STRAWBERRY': 7.4 if fert else 4.0, 'MELON': 6.0}[crop]

def _planting_schedule(crop, day):
    """[(harvest day, units)] of a planting on `day` under DSM husbandry (only days <= FINAL_DAY)."""
    if crop == 'WHEAT':
        _q1113 = [(day + 3, 5.0)]
    elif crop == 'CARROT':
        _q1113 = [(day + 3, 3.6)]
    elif crop == 'TOMATO':
        _q1113 = [(day + a, 1.75) for a in (8, 9, 10, 11)]
    elif crop == 'STRAWBERRY':
        _q1113 = [(day + a, 1.85) for a in (10, 12, 14, 16)]
    else:
        _q1113 = [(day + 10, 6.0)]
    return [(_q530, _q1221) for _q530, _q1221 in _q1113 if _q530 <= FINAL_DAY]

def _animal_rate(animal):
    """(first harvest day offset, units per day) with ~75% care."""
    return {'GOOSE': (5, 1.75), 'COW': (9, 1.25), 'SHEEP': (7, 1.08)}[animal]

def project_cash(state, plan, rules):
    """Closing cash for each day from today to FINAL_DAY under the plan: today's purchases, then a steady state of
    today's hires, the window quotas (current shops) and the yields of what stands plus what is planned, sold one day
    after harvest at haircut x current quote (wheat first feeds the animals; a feed deficit is bought)."""
    cfg = rules['cfg']
    day = state.day
    _q690 = cfg['haircut']
    px = state.prices
    days = list(range(day, FINAL_DAY + 1))
    _q725 = {_q530: 0.0 for _q530 in days}
    _q1151 = {_q530: 0.0 for _q530 in days}
    wheat = {_q530: 0.0 for _q530 in days}

    def _q377(item, _q530, _q1221):
        if _q530 > FINAL_DAY:
            return
        _q534 = min(FINAL_DAY, max(day, _q530 + (0 if _q530 == FINAL_DAY else 1)))
        if item == 'WHEAT':
            wheat[max(day, min(FINAL_DAY, _q530))] += _q1221
            return
        _q725[_q534] += _q1221 * float(px.get(item, 0)) * _q690
    for item, n in state.shed.items():
        if item in ANIMALS or item == 'FERTILIZER':
            continue
        if item == 'WHEAT':
            wheat[day] += n
            continue
        _q725[day] += 0.5 * n * float(px.get(item, 0)) * _q690
        if day + 1 <= FINAL_DAY:
            _q725[day + 1] += 0.5 * n * float(px.get(item, 0)) * _q690
    for _q513 in state.crops.values():
        if _q513.ongoing:
            _q474 = CROPS[_q513.crop]
            _q629 = _q474['fyd'] - 1
            _q741 = _q474['interval']
            if _q513.units > 0:
                _q377(_q513.crop, day, _q513.units)
            k = _q513.prods_done
            for _q712 in range(_q513.prods_left):
                a = _q629 + _q741 * (k + _q712)
                _q377(_q513.crop, _q513.planted_day + a + 1, 1.75)
        else:
            _q1221 = PT._future_units(_q513, day)
            _q692 = max(day, _q513.planted_day + {'WHEAT': 3, 'CARROT': 3, 'MELON': 10}[_q513.crop])
            _q377(_q513.crop, _q692, _q1221)
    _q860 = len(state.animals)
    for _q388 in state.animals.values():
        _q932, _q1044 = _animal_rate(_q388.animal)
        if _q388.units:
            _q377(_q388.product, day, _q388.units)
        start = max(day + 1, _q388.placed_day + _q932)
        for _q530 in range(start, FINAL_DAY + 1):
            _q377(_q388.product, _q530, _q1044)
        for _q530 in range(day + 1, FINAL_DAY + 1):
            _q725[_q530] += 0.45 * float(px.get('FERTILIZER', 0)) * _q690
    _q1151[day] += plan.get('spend_today', 0.0)
    for op, xy, arg in plan.get('ops', ()):
        if op == 'PLANT':
            for _q530, _q1221 in _planting_schedule(arg, day):
                _q377(arg, _q530, _q1221)
        elif op == 'PLACE':
            _q932, _q1044 = _animal_rate(arg)
            for _q530 in range(day + _q932, FINAL_DAY + 1):
                _q377(ANIMALS[arg]['product'], _q530, _q1044)
            _q860 += 1
    hands = plan.get('hires', 0)
    _q535 = hire_cost(0, hands)
    _q658 = plan.get('future_daily', {})
    for _q530 in days[1:]:
        _q1151[_q530] += _q535
        for _q1272, _q984 in _q658.get(_q530, {}).items():
            if _q1272 in CROP_OF:
                crop = CROP_OF[_q1272]
                _q1151[_q530] += _q984 * CROPS[crop]['seed']
                for _q539, _q1221 in _planting_schedule(crop, _q530):
                    _q377(crop, _q539, _q1221 * _q984)
            else:
                a = ANIMAL_OF[_q1272]
                _q1151[_q530] += _q984 * ANIMALS[a]['cost']
                _q932, _q1044 = _animal_rate(a)
                for _q539 in range(_q530 + _q932, FINAL_DAY + 1):
                    _q377(ANIMALS[a]['product'], _q539, _q1044 * _q984)
                _q860 += _q984
    stock = 0.0
    _q1262 = float(px.get('WHEAT', 25))
    for _q530 in days:
        stock += wheat[_q530]
        need = _q860 * cfg['wheat_feed_rate'] if _q530 > day else 0.0
        if stock >= need:
            stock -= need
            if stock > 20:
                _q725[_q530] += (stock - 20) * _q1262 * _q690
                stock = 20.0
        else:
            _q1151[_q530] += (need - stock) * (_q1262 + 2)
            stock = 0.0
    cash = state.money
    _q946 = []
    for _q530 in days:
        cash = cash - _q1151[_q530] + _q725[_q530]
        _q946.append((_q530, round(cash, 1)))
    return _q946

def _ld(_q1272, rules):
    """Last planting day of y (cfg last_day over LAST_DAY)."""
    _q922 = rules['cfg'].get('last_day') if isinstance(rules, dict) and 'cfg' in rules else None
    if _q922 and _q1272 in _q922:
        return _q922[_q1272]
    return LAST_DAY[_q1272]

def _first_day(_q1272, rules):
    if _q1272 == 'S':
        return rules['cfg'].get('s_first_day', FIRST_DAY['S'])
    return FIRST_DAY.get(_q1272, 0)

def _quota_today(_q1272, _q727, day, rules, state):
    _q531, _q532 = _q727['window']
    if day > _ld(_q1272, rules) or day < _first_day(_q1272, rules):
        return 0
    rem = _q727['remaining']
    carry = _q727.get('carry', 0)
    if rem <= 0 and carry <= 0:
        return 0
    _q785 = min(_q532, _ld(_q1272, rules))
    _q537 = max(1, _q785 - day + 1)
    if _q1272 in FRONT_LOADED or (_q1272 == 'T' and _q531 == 18):
        q = rem
    else:
        q = int(math.ceil(rem / _q537))
    q += carry
    cap = standing_cap(rules, _q1272, state, day)
    if cap is not None:
        q = min(q, max(0, int(math.floor(cap)) - _stock_now(state, _q1272)))
    return max(0, q)

def _future_daily(state, rules, day, D):
    """Expected plantings per day for the days after today (cash projection only): the additive rule of each later
    window at today's shops, own stock = today's standing, spread evenly over the window."""
    _q946 = {}
    for _q531, _q532 in WINDOWS:
        if _q532 <= day:
            continue
        for _q1272 in PRODUCTS_Y:
            if _q1272 == 'W':
                continue
            _q1233 = rule_value(rules, _q1272, (_q531, _q532), state.shop_counts, _stock_now(state, _q1272), _rival_now(state, _q1272))
            if _q1233 <= 0.5:
                continue
            days = [_q530 for _q530 in range(max(_q531, day + 1), min(_q532, _ld(_q1272, rules)) + 1) if _q530 >= _first_day(_q1272, rules)]
            if not days:
                continue
            _q983 = _q1233 / len(days) * (len(days) / float(_q532 - _q531 + 1))
            for _q530 in days:
                _q946.setdefault(_q530, {})[_q1272] = _q983
    return _q946

def _wf_ripe(_q513, day):
    """Wheat-first reuse rule: wheat at age 4, or at age 3 when fertilised (fert_until >= today: the age-3 WATER adds +2,
    DSM cuts 50% at age 3 with 4.97 u); carrots at age 3; melons / decaying crops as _ripe_for_reuse."""
    if _q513.ongoing:
        return False
    if _q513.decaying:
        return True
    if not _q513.harvestable():
        return False
    if _q513.crop == 'WHEAT':
        return _q513.age >= 4 or (_q513.age == 3 and _q513.fert_until >= day)
    if _q513.crop == 'CARROT':
        return _q513.age >= 3
    if _q513.crop == 'MELON':
        return _q513.age >= 12 or (_q513.age >= 10 and _q513.units >= 6)
    return False

def _wf_free(state, _q905, _q782):
    """[(xy, prep_cost, kind, not_before, cls)]: _free_inventory with the wheat-first reuse rule; cls 'wh' = ripe
    rotation wheat, 'freed' = spent strawberry / tomato (harvested + dug on its last harvest day) or another ripe crop,
    'open' = empty / weed / newly bought tile."""
    day = state.day
    inv = []
    for xy in state.empty:
        inv.append((xy, 0, 'empty', 0, 'open'))
    for xy in state.weeds:
        inv.append((xy, 1, 'weed', 0, 'open'))
    for xy, _q513 in state.crops.items():
        if _q513.ongoing and _q513.prods_left == 0:
            inv.append((xy, 1 + (_q513.units > 0), 'spent', 0, 'freed'))
        elif _wf_ripe(_q513, day):
            inv.append((xy, 1 + (0 if _q513.age >= CROPS[_q513.crop]['myd'] else 1), 'ripe', 0, 'wh' if _q513.crop == 'WHEAT' else 'freed'))
    for q in _q905:
        for xy in QUAD_TILES[q]:
            if xy in state.locked:
                inv.append((xy, 0, 'new', _q782[q] + 1, 'open'))
    return inv

def _wf_qscale(state, c):
    """{y: quota factor} from the owned land (unlocked tiles + today's due fixed-step quadrants): 1 - (1 - f3) x missing
    quadrants (f3 = the 3-quadrant factor of wf_quota_land), within [0.1, 1]; None when the table is empty."""
    _q1183 = c.get('wf_quota_land')
    if _q1183 is None:
        _q1183 = WF_LAND_Q
    if not _q1183:
        return None
    owned = len(QUAD_TILES) * 25 - len(state.locked)
    _q814 = c.get('land_steps') or {}
    for _q1032 in LAND_ORDER[max(0, state.n_quads - 1):]:
        if _q1032 in _q814 and int(_q814[_q1032]) <= 24 * state.day + 23:
            owned += 25
        else:
            break
    short = max(0, 100 - owned) / 25.0
    return {_q1272: max(0.1, min(1.0, 1.0 - (1.0 - float(f)) * short)) for _q1272, f in _q1183.items()}

def _wf_alloc(state, rules, c, plan, _q1034, _q584, _q905, _q782, _q1205, _q780):
    """CS B1 tile allocation + capacity trim (cfg alloc 'wheat_first').  Returns (ops, n_state, max_units) - the last
    two as the default mode computes them for the R8 hires - and fills plan['wheat'].

    W* (the protected rotation) = clamp(round(a x (animals + today's placements)), round(fl x owned), round(cp x owned))
    with (a, fl, cp) = wf_wstar, on days <= min(wf_wstar_last, last W day).  need = W* - wheat standing tonight without
    today's plantings (young wheat, unripe age-3 wheat); the quota crops (animals' BUILDs first, then T, S, C) may use at
    most (free tiles - need) tiles, so the rotation can always be rebuilt to W* tonight.  Ripe wheat tiles are ranked by
    the wheat score: the best `need` are 'inside W*' (only T and S may take them - the rotation then moves to an open
    tile), the rest 'above W*'.  Every free tile left is planted: wheat (rotation tiles first, a harvested tile gets
    WATER? -> HARVEST -> PLANT -> WATER in one chain by pd_tasks), on the carrot-fill days carrots once standing wheat
    reaches W* + wf_w_margin.  Trim: load = level>=2 state tasks (x wf_l2, level 3 in full; FERTILIZE only on
    wf_fert_crops) + animal ops + each planting's exact extra chain ops (pd_tasks chain length minus the tile's counted
    state tasks); capacity =
    (farmer turns + turns per hand x hands) / wf_tpt; order wheat above W*, carrots, wheat down to the floor, S, T."""
    day = state.day
    dw = dict(WF_DIST_W)
    dw.update(c.get('wf_dist_w') or {})
    free = _wf_free(state, _q905, _q782)
    owned = len(QUAD_TILES) * 25 - len(state.locked) + 25 * len(_q905)
    _q366, _q634, _q512 = c.get('wf_wstar') or WF_WSTAR
    _q1259 = _ld('W', rules)
    _q860 = len(state.animals) + sum((_q1034.get(_q1272, 0) for _q1272 in ANIMAL_OF))
    if day <= min(_q1259, int(c.get('wf_wstar_last', 27))):
        floor = int(round(_q634 * owned))
        wstar = max(floor, min(int(round(_q512 * owned)), int(round(_q366 * _q860))))
    else:
        floor = wstar = 0
    _q1246 = c.get('wheat_bias')
    if _q1246 is not None:
        floor = max(0, int(round(floor * float(_q1246))))
        wstar = max(0, int(round(wstar * float(_q1246))))
    _q818 = c.get('late_tc_prio')
    _q818 = _q818 is not None and day >= int(_q818)
    _q648 = set((f[0] for f in free))
    stand0 = sum((1 for xy, _q513 in state.crops.items() if _q513.crop == 'WHEAT' and xy not in _q648))
    need = max(0, wstar - stand0) if day <= _q1259 else 0
    _q1111 = {}

    def _q1114(f, g):
        k = (g, f[0])
        _q1233 = _q1111.get(k)
        if _q1233 is None:
            _q1233 = _score(state, f[0], f[1], g, dw) + 0.5 * f[3] / 24.0
            _q1111[k] = _q1233
        return _q1233
    _q491 = {}
    wh = sorted((f for f in free if f[4] == 'wh'), key=lambda f: (_q1114(f, 'W'), f[0]))
    for _q712, f in enumerate(wh):
        _q491[f[0]] = 'wh_in' if _q712 < need else 'wh_up'
    for f in free:
        if f[4] != 'wh':
            _q491[f[0]] = f[4]
    budget = max(0, len(free) - need)
    _q1231 = set()

    def _q987(g, _q1198):
        for _q1197 in _q1198:
            best, _q417 = (None, None)
            for f in free:
                if f[0] in _q1231 or _q491[f[0]] not in _q1197:
                    continue
                k = (_q1114(f, g), f[0])
                if _q417 is None or k < _q417:
                    best, _q417 = (f, k)
            if best is not None:
                _q1231.add(best[0])
                return best
        return None
    ops = []
    _q799 = budget
    for _q1272 in ('goose', 'cow', 'sheep'):
        a = ANIMAL_OF[_q1272]
        k = STRUCT[a]
        _q965 = int(state.shed.get(a, 0))
        for _q712 in range(_q1034[_q1272]):
            if _q584[k]:
                ops.append(('PLACE', _q584[k].pop(0), a))
                continue
            if _q799 <= 0 and _q712 >= _q965:
                break
            t = _q987('A', (('open', 'freed', 'wh_up'),) + ((('wh_in',),) if _q712 < _q965 else ()))
            if t is None:
                break
            _q799 -= 1
            ops.append(('BUILD_' + k, t[0], None))
            ops.append(('PLACE', t[0], a))
    _q1199 = (('freed',), ('wh_up',), ('wh_in',), ('open',))
    _q1198 = {'T': _q1199, 'S': _q1199, 'C': (('freed',), ('wh_up',), ('open',))}
    if _q818:
        _q1198['C'] = _q1198['C'] + (('wh_in',),)
    _q993 = []
    sp = c.get('wf_s_prio')
    _q647 = ('S', 'T') if sp == 'ST' else ('S',) if sp else ()
    if _q818:
        _q647 = tuple(_q647) + tuple((_q1272 for _q1272 in ('T', 'C') if _q1272 not in _q647))
    for _q1272 in ('S', 'T', 'C') if sp else ('T', 'S', 'C'):
        for _ in range(_q1034[_q1272]):
            if _q799 <= 0 and _q1272 not in _q647:
                break
            t = _q987(_q1272, _q1198[_q1272])
            if t is None:
                break
            _q799 -= 1
            _q993.append((_q1272, t))
    cf = c.get('wf_fill_carrot', WF_FILL_C)
    _q475 = bool(cf) and cf[0] <= day <= min(cf[1], _ld('C', rules))
    margin = int(c.get('wf_w_margin', 4))
    rest = sorted((f for f in free if f[0] not in _q1231), key=lambda f: (0 if _q491[f[0]] in ('wh_in', 'wh_up') else 1, _q1114(f, 'W'), f[0]))
    _q919 = 0
    for f in rest:
        if day <= _q1259 and (not _q475 or stand0 + _q919 < wstar + margin):
            _q993.append(('W', f))
            _q919 += 1
        elif _q475:
            _q993.append(('C', f))
    _q404 = PT.due_tasks(state, dict(_q1205, land=plan['land']))
    _q776 = c['l2_done_share']
    _q885 = sum((1 for t in _q404 if t.level >= 2)) * _q776 + sum((1 for t in _q404 if t.level >= 3)) * (1 - _q776)
    _q777 = float(c.get('wf_l2', 1.0))
    _q610 = c.get('wf_fert_crops')
    _q1158 = {}
    _q886 = 0.0
    _q682 = set()
    for t in _q404:
        w = _q777 if t.level == 2 else 1.0 if t.level >= 3 else 0.0
        if _q610 is not None and t.op == 'FERTILIZE':
            _q513 = state.crops.get(t.xy)
            if _q513 is None or _q513.crop not in _q610:
                w = 0.0
        if w:
            _q886 += w
            _q1158[t.xy] = _q1158.get(t.xy, 0.0) + w
        if t.op == 'HARVEST' and t.level >= 2:
            _q682.add(t.xy)
    _q825 = {}
    if _q993:
        _q1017 = PT.due_tasks(state, dict(_q1205, land=plan['land'], ops=[('PLANT', t[0], 'WHEAT') for _, t in _q993]))
        chain = {}
        for t in _q1017:
            if t.src == 'plan' and (not (t.op == 'FERTILIZE' and t.level < 2)):
                chain[t.xy] = chain.get(t.xy, 0) + 1
        for _, t in _q993:
            _q825[t[0]] = max(1.0, chain.get(t[0], 2) - _q1158.get(t[0], 0.0))
    hands = c['max_hands'] if _q780 is None else min(_q780, c['max_hands'])
    _q1179, _q1180 = c.get('wf_cap') or WF_CAP
    cap_tasks = (float(_q1179) + float(_q1180) * hands) / float(c.get('wf_tpt', 1.95))
    _q861 = sum((1 for _q922 in ops if _q922[0] == 'PLACE')) * 4 + sum((1 for _q922 in ops if _q922[0].startswith('BUILD')))

    def load():
        return _q886 + _q861 + sum((_q825[t[0]] for _, t in _q993))
    trimmed = {'W': 0, 'C': 0, 'S': 0, 'T': 0}
    _q1181 = ('W+', 'W-', 'C', 'S', 'T') if _q818 else ('W+', 'C', 'W-', 'S', 'T')
    while _q993 and load() > cap_tasks:
        _q1161 = stand0 + sum((1 for _q1280, _ in _q993 if _q1280 == 'W'))
        for g in _q1181:
            if g == 'W+' and _q1161 <= wstar:
                continue
            if g == 'W-' and _q1161 <= floor:
                continue
            _q1272 = g[0]
            _q717 = [_q712 for _q712, (_q1280, _) in enumerate(_q993) if _q1280 == _q1272]
            if _q717:
                _q993.pop(_q717[-1])
                trimmed[_q1272] += 1
                break
        else:
            break
    for _q1272, t in _q993:
        ops.append(('PLANT', t[0], CROP_OF[_q1272]))
    plan['ops'] = ops
    plan['w_keep'] = None
    _q919 = sum((1 for _q1280, _ in _q993 if _q1280 == 'W'))
    planted = set((t[0] for _, t in _q993))
    kept = sum((1 for f in wh if f[0] not in planted and f[0] not in _q682))
    plan['wheat'] = {'wstar': wstar, 'floor': floor, 'owned': owned, 'stand0': stand0, 'need': need, 'free': len(free), 'ripe_w': len(wh), 'budget': budget, 'quota_tiles': budget - _q799, 'plant_w': _q919, 'tonight': stand0 + _q919 + kept, 'cap_tasks': round(cap_tasks, 1), 'load': round(load(), 1), 'trimmed': trimmed, 'qscale': c.get('_qscale')}
    _q830 = 1 + (c['max_hands'] if _q780 is None else _q780)
    return (ops, _q885, _q830)

def plan_day(state, rules=None, D=11, cfg=None):
    rules = rules or load_rules()
    c = dict(rules['cfg'])
    if cfg:
        c.update(cfg)
    rules = dict(rules, cfg=c)
    _q1248 = c.get('alloc') == 'wheat_first'
    if _q1248:
        _q795 = dict(WF_LAST_DAY if c.get('wf_last_day') is None else c['wf_last_day'])
        _q795.update(c.get('last_day') or {})
        c['last_day'] = _q795
        _q1031 = _wf_qscale(state, c)
        if _q1031:
            c['_qscale'] = _q1031
    day = state.day
    plan = {'day': day, 'D': D, 'active': day >= D, 'ops': [], 'land': [], 'hires': 0, 'orders': {}, 'deferred': [], 'targets': {}, 'fert_wheat': float(state.prices.get('FERTILIZER', 100)) <= c.get('fert_wheat_q', 55)}
    _q1205 = dict(c.get('task_opts') or {})
    plan.update(_q1205)
    if day < D:
        return plan
    _q780 = None
    _q779 = c.get('hire_ladder')
    if _q779 is not None:
        try:
            _q1233 = _q779.get(day, _q779.get(str(day))) if isinstance(_q779, dict) else _q779[min(day, len(_q779) - 1)]
            _q780 = None if _q1233 is None else max(0, int(_q1233))
        except (IndexError, TypeError, ValueError):
            _q780 = None
    wt = window_targets(state, rules, day, D)
    _q1034 = {_q1272: 0 for _q1272 in PRODUCTS_Y}
    for _q1272, _q727 in wt.items():
        q = _quota_today(_q1272, _q727, day, rules, state)
        if _q1272 == 'W':
            q = 0
        if _q1272 in ANIMAL_OF and (not c.get('animals', True)):
            q = 0
        _q1034[_q1272] = q
    _q480 = c.get('cow_gate')
    if _q480:
        if day < int(_q480.get('min_day', 0)):
            _q1034['cow'] = 0
        elif _q480.get('max_new') is not None:
            _q1034['cow'] = max(0, min(_q1034['cow'], int(_q480['max_new']) - state.placed_in('COW', D, day)))
    if c.get('no_geese'):
        _q1034['goose'] = 0
    if c.get('tom_cap') is not None:
        _q1034['T'] = max(0, min(_q1034['T'], int(c['tom_cap'])))
    if c.get('place_shed') and day <= 27:
        for _q1272 in ('goose', 'cow', 'sheep'):
            _q1034[_q1272] = max(_q1034[_q1272], int(state.shed.get(ANIMAL_OF[_q1272], 0)))
    _q691 = c.get('herd_cap')
    if _q691:
        for _q1272 in ('goose', 'cow', 'sheep'):
            a = ANIMAL_OF[_q1272]
            _q459 = _q691.get(a, _q691.get(_q1272))
            if _q459 is None:
                continue
            _q722 = int(state.shed.get(a, 0))
            owned = state.n_animals(a) + _q722 + sum((int(_q712.get(a, 0) or 0) for _q712 in state.inventories))
            _q1034[_q1272] = max(0, min(_q1034[_q1272], _q722 + max(0, int(_q459) - owned)))
    if c.get('animals', True) == 'existing':
        _q646 = {'COOP': sum((1 for k in state.structures.values() if k == 'COOP')), 'PASTURE': sum((1 for k in state.structures.values() if k == 'PASTURE'))}
        for _q1272 in ('goose', 'cow', 'sheep'):
            k = STRUCT[ANIMAL_OF[_q1272]]
            _q1034[_q1272] = min(_q1034[_q1272], _q646[k])
            _q646[k] -= _q1034[_q1272]
    _q584 = {'COOP': [xy for xy, k in state.structures.items() if k == 'COOP'], 'PASTURE': [xy for xy, k in state.structures.items() if k == 'PASTURE']}
    _q898 = sum((_q1034[_q1272] for _q1272 in ('S', 'T', 'C')))
    for _q1272 in ('cow', 'sheep', 'goose'):
        a = ANIMAL_OF[_q1272]
        _q898 += max(0, _q1034[_q1272] - len(_q584[STRUCT[a]]))
    _q905, _q782 = ([], {})
    _q868 = len(_free_inventory(state, [], {}))
    _q811 = _q898 + sum((sum(_q1233.values()) for _q530, _q1233 in _future_daily(state, rules, day, D).items() if _q530 <= day + 2))
    money = state.money
    _q403 = hire_cost(0, c['max_hands']) + 200.0
    n_quads = state.n_quads
    staff_cap = None
    if c.get('land_after_trim') and n_quads < 4:
        _q433 = PT.due_tasks(state, dict(_q1205, land=[]))
        _q918 = sum((1 for t in _q433 if t.level >= 2)) * c['l2_done_share'] + sum((1 for t in _q433 if t.level >= 3)) * (1 - c['l2_done_share'])
        _q849 = 1 + c['max_hands']
        _q456 = _q849 * c['turns_per_unit'] / c['turns_per_task'] - 2 * _q849 / c['turns_per_task']
        _q890 = sum((_q1034[_q1272] for _q1272 in ('cow', 'sheep', 'goose'))) * 4
        staff_cap = max(0, int((_q456 - _q918 - _q890) // 2.5))
        plan['staff_cap'] = staff_cap
    _q816 = c.get('land_steps') or {}
    while n_quads < 4:
        price = LAND_PRICES[n_quads - 1]
        _q1032 = ('NE', 'SW', 'SE')[n_quads - 1]
        hour = 0
        if _q1032 in _q816:
            _q1100 = int(_q816[_q1032])
            hour = max(0, _q1100 - 24 * day)
            if _q1100 > 24 * day + 23 or (hour == 0 and money < price):
                break
            money -= price
            _q905.append(_q1032)
            _q782[_q1032] = hour
            plan['land'].append((hour, _q1032))
            _q868 += 25
            n_quads += 1
            continue
        if _q1032 == 'SE':
            hour = max(0, c['se_step'] - 24 * day)
            if hour > 20:
                break
            if staff_cap is not None:
                if min(_q811, staff_cap) + 4 <= _q868:
                    break
                if c.get('prev_hires') is not None and int(c['prev_hires']) >= c['max_hands']:
                    break
        if _q811 + 4 <= _q868:
            break
        if money < price + _q403 + c['reserve']:
            break
        money -= price
        _q905.append(_q1032)
        _q782[_q1032] = hour
        plan['land'].append((hour, _q1032))
        _q868 += 25
        n_quads += 1
    if _q1248:
        ops, _q885, _q830 = _wf_alloc(state, rules, c, plan, _q1034, _q584, _q905, _q782, _q1205, _q780)
    else:
        free = _free_inventory(state, _q905, _q782)
        _q1231 = set()
        ops = []
        _q1043 = {}

        def _q1186(_q671, allow=None):
            _q815 = _q1043.get(_q671)
            if _q815 is None:
                _q815 = sorted(free, key=lambda f: (_score(state, f[0], f[1], _q671) + 0.5 * f[3] / 24.0, f[0]))
                _q815.reverse()
                _q1043[_q671] = _q815
            for _q712 in range(len(_q815) - 1, -1, -1):
                f = _q815[_q712]
                if f[0] in _q1231:
                    _q815.pop(_q712)
                    continue
                if allow is not None and (not allow(f)):
                    continue
                _q815.pop(_q712)
                _q1231.add(f[0])
                return f
            return None
        for _q1272 in ('goose', 'cow', 'sheep'):
            a = ANIMAL_OF[_q1272]
            k = STRUCT[a]
            n = _q1034[_q1272]
            for _ in range(n):
                if _q584[k]:
                    xy = _q584[k].pop(0)
                    ops.append(('PLACE', xy, a))
                    continue
                t = _q1186('A')
                if t is None:
                    break
                ops.append(('BUILD_' + k, t[0], None))
                ops.append(('PLACE', t[0], a))
        _q993 = []
        for _q1272 in ('T', 'S', 'C'):
            for _ in range(_q1034[_q1272]):
                t = _q1186(_q1272)
                if t is None:
                    break
                _q993.append((_q1272, t))
        if day <= _ld('W', rules):
            while True:
                t = _q1186('W', allow=lambda f: not (f[2] == 'ripe' and f[1] >= 2))
                if t is None:
                    break
                _q993.append(('W', t))
        _q404 = PT.due_tasks(state, dict(_q1205, land=plan['land']))
        _q885 = sum((1 for t in _q404 if t.level >= 2)) * c['l2_done_share'] + sum((1 for t in _q404 if t.level >= 3)) * (1 - c['l2_done_share'])
        _q985 = {'empty': 2, 'new': 2, 'weed': 3, 'spent': 3.5, 'ripe': 3}
        _q861 = sum((1 for _q922 in ops if _q922[0] == 'PLACE')) * 4 + sum((1 for _q922 in ops if _q922[0].startswith('BUILD')))
        _q830 = 1 + (c['max_hands'] if _q780 is None else _q780)
        cap_tasks = _q830 * c['turns_per_unit'] / c['turns_per_task'] - 2 * _q830 / c['turns_per_task']

        def load(_q988):
            return _q885 + _q861 + sum((_q985[t[2]] for _, t in _q988))
        _q939 = ('W', 'C', 'S', 'T')
        w_keep = 0
        if c.get('w_feed_tiles'):
            _q860 = len(state.animals) + sum((1 for _q922 in ops if _q922[0] == 'PLACE'))
            _q1278 = sum((1 for _q513 in state.crops.values() if _q513.crop == 'WHEAT' and _q513.age < CROPS['WHEAT']['myd'] and (not _q513.decaying)))
            _q1249 = c['w_feed_tiles'] * (1.0 if c.get('wheat_bias') is None else float(c['wheat_bias']))
            w_keep = max(0, int(math.ceil(_q1249 * _q860)) - _q1278)
        plan['w_keep'] = w_keep
        while _q993 and load(_q993) > cap_tasks:
            _q888 = sum((1 for _q1280, _ in _q993 if _q1280 == 'W'))
            for _q1272 in _q939:
                if _q1272 == 'W' and _q888 <= w_keep:
                    continue
                _q717 = [_q712 for _q712, (_q1280, _) in enumerate(_q993) if _q1280 == _q1272]
                if _q717:
                    _q993.pop(_q717[-1])
                    break
            else:
                break
        for _q1272, t in _q993:
            ops.append(('PLANT', t[0], CROP_OF[_q1272]))
        plan['ops'] = ops
    tasks = PT.due_tasks(state, plan)
    _q883 = sum((1 for t in tasks if t.src == 'plan')) + _q885
    turns = _q883 * c['turns_per_task'] + 2 * _q830
    units_needed = int(math.ceil(turns / float(c['turns_per_unit'])))
    hands = max(c['min_hands'], min(c['max_hands'], units_needed - 1)) if _q780 is None else _q780
    _q940 = []
    _q1151 = 0.0
    cash = state.money
    deferred = []
    reserve = c['reserve']
    _q476 = bool(c.get('cash_defer'))

    def _q453(cost):
        return _q476 or cash - _q1151 - cost >= reserve
    _q784 = {}

    def _q440():
        nonlocal _q1151
        _q764 = []
        for hour, _q1032 in plan['land']:
            price = LAND_PRICES[('NE', 'SW', 'SE').index(_q1032)]
            if _q1032 in _q816:
                _q1151 += price
                _q784.setdefault(hour, []).append(['BUY_LAND'])
                _q764.append((hour, _q1032))
                continue
            if _q453(price):
                _q1151 += price
                _q784.setdefault(hour, []).append(['BUY_LAND'])
                _q764.append((hour, _q1032))
            else:
                deferred.append(['BUY_LAND', _q1032])
        if len(_q764) < len(plan['land']):
            _q812 = {q for _, q in plan['land']} - {q for _, q in _q764}
            plan['ops'] = [_q922 for _q922 in plan['ops'] if quadrant_of(*_q922[1]) not in _q812 or _q922[1] not in state.locked]
            plan['land'] = _q764
    _q684 = 0
    while _q684 < hands and _q453(fib(state.hires_today + _q684)):
        _q1151 += fib(state.hires_today + _q684)
        _q684 += 1
    _q940 += [['HIRE'] for _ in range(_q684)]
    if _q684 < hands:
        deferred.append(['HIRE', hands - _q684])
    plan['hires'] = _q684
    if _q816:
        _q440()
    _q893 = PT.needs(tasks)
    _q1253 = state.shed.get('WHEAT', 0) + 0.5 * sum((state.crops[t.xy].units for t in tasks if t.op == 'HARVEST' and t.xy in state.crops and (state.crops[t.xy].crop == 'WHEAT')))
    _q616 = int(max(0, _q893.get('WHEAT', 0) - _q1253))
    _q1262 = float(state.prices.get('WHEAT', 25)) + 1
    if _q616:
        k = min(_q616, max(0, int((cash - _q1151 - reserve) // _q1262)) if not _q476 else _q616, state.shed_room)
        if k > 0:
            _q940.append(['BUY_PRODUCT', 'WHEAT', k])
            _q1151 += k * _q1262
        if k < _q616:
            deferred.append(['BUY_PRODUCT', 'WHEAT', _q616 - k])
    if not _q816:
        _q440()
    _q439 = {}
    for op, xy, arg in plan['ops']:
        if op == 'PLACE':
            _q439[arg] = _q439.get(arg, 0) + 1
    shed_room = state.shed_room - sum((_q922[2] for _q922 in _q940 if _q922[0] == 'BUY_PRODUCT'))
    _q563 = {}
    for a, n in _q439.items():
        _q688 = state.shed.get(a, 0)
        _q758 = max(0, n - _q688)
        k = 0
        while k < _q758 and _q453(ANIMALS[a]['cost']) and (shed_room > 0):
            _q1151 += ANIMALS[a]['cost']
            k += 1
            shed_room -= 1
        if k:
            _q940.append(['BUY_ANIMAL', a, k])
        if k < _q758:
            deferred.append(['BUY_ANIMAL', a, _q758 - k])
            _q563[a] = _q758 - k
    if _q563:
        keep = []
        for _q922 in reversed(plan['ops']):
            if _q922[0] == 'PLACE' and _q563.get(_q922[2], 0) > 0:
                _q563[_q922[2]] -= 1
                continue
            keep.append(_q922)
        keep.reverse()
        plan['ops'] = keep
    _q1116 = {}
    for op, xy, arg in plan['ops']:
        if op == 'PLANT':
            _q1116[arg] = _q1116.get(arg, 0) + 1
    _q564 = {}
    for crop in ('STRAWBERRY', 'TOMATO', 'CARROT', 'WHEAT'):
        n = max(0, _q1116.get(crop, 0) - state.seeds.get(crop, 0))
        if not n:
            continue
        k = min(n, max(0, int((cash - _q1151 - reserve) // CROPS[crop]['seed']))) if not _q476 else n
        if k:
            _q940.append(['BUY_SEED', crop, k])
            _q1151 += k * CROPS[crop]['seed']
        if k < n:
            deferred.append(['BUY_SEED', crop, n - k])
            _q564[crop] = n - k
    if _q564:
        keep = []
        for _q922 in reversed(plan['ops']):
            if _q922[0] == 'PLANT' and _q564.get(_q922[2], 0) > 0:
                _q564[_q922[2]] -= 1
                continue
            keep.append(_q922)
        keep.reverse()
        plan['ops'] = keep
    _q643 = float(state.prices.get('FERTILIZER', 100))
    _q601 = _q893.get('FERTILIZER', 0) - state.shed.get('FERTILIZER', 0) - sum((1 for t in tasks if t.op == 'COLLECT_FERTILIZER'))
    if _q601 > 0 and _q643 <= c['fert_buy_max']:
        k = min(_q601, max(0, int((cash - _q1151 - reserve) // (_q643 + 1))), max(0, shed_room))
        if k:
            _q940.append(['BUY_PRODUCT', 'FERTILIZER', k])
            _q1151 += k * (_q643 + 1)
    _q698 = [_q922 for _q922 in _q940 if _q922[0] == 'HIRE']
    _q441 = [_q922 for _q922 in _q940 if _q922[0] != 'HIRE']
    h0 = list(_q784.get(0, [])) + _q698[:8]
    _q1082 = max(0, 10 - len(h0))
    h0 += _q441[:_q1082]
    pending = _q698[8:] + _q441[_q1082:]
    orders = {0: h0}
    h = 1
    while pending or any((k >= h for k in _q784)):
        _q522 = list(_q784.get(h, [])) + pending
        if _q522:
            orders[h] = _q522[:10]
        pending = _q522[10:]
        h += 1
        if h > 23:
            break
    plan['orders'] = orders
    plan['deferred'] = deferred
    plan['spend_today'] = _q1151
    _q625 = {'S': 0, 'T': 0, 'C': 0, 'W': 0, 'cow': 0, 'sheep': 0, 'goose': 0}
    for op, xy, arg in plan['ops']:
        if op == 'PLANT':
            _q625[{_q1233: k for k, _q1233 in CROP_OF.items()}[arg]] += 1
        elif op == 'PLACE':
            _q625[{_q1233: k for k, _q1233 in ANIMAL_OF.items()}[arg]] += 1
    _q658 = _future_daily(state, rules, day, D)
    plan['future_daily'] = _q658
    for _q1272, _q727 in wt.items():
        _q531, _q532 = _q727['window']
        rest = 0
        carry = _q727.get('carry', 0)
        _q1203 = max(0, _q625[_q1272] - carry)
        if _q1272 != 'W' and _first_day(_q1272, rules) <= day <= _ld(_q1272, rules):
            if day < min(_q532, _ld(_q1272, rules)) or day + 1 <= _ld(_q1272, rules):
                rest = max(0, _q727['remaining'] - _q1203)
        cap = standing_cap(rules, _q1272, state, day)
        plan['targets'][_q1272] = dict(_q727, quota=_q1034.get(_q1272, 0), today=_q625[_q1272], today_window=_q1203, rest=rest, window_total=_q727['planted'] + _q1203 + rest, cap=None if cap is None else round(cap, 2), active=_first_day(_q1272, rules) <= day <= _ld(_q1272, rules))
    _q1022 = project_cash(state, plan, rules)
    plan['cash'] = {'start': state.money, 'spend_today': round(_q1151, 1), 'projection': _q1022, 'min': min((_q1233 for _, _q1233 in _q1022)) if _q1022 else state.money}
    plan['tasks'] = PT.due_tasks(state, plan)
    plan['task_turns'] = int(turns)
    plan['units_needed'] = units_needed
    return plan