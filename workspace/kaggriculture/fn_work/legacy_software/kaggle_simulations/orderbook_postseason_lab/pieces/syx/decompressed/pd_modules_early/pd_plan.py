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

def load_rules(_q688=None):
    _q324 = dict(ADDITIVE)
    _q1092 = dict(STANDING)
    if _q688:
        import json
        import os
        a = json.load(open(os.path.join(_q688, 'wf31_rules_additive_DSM.json')))
        _q324 = {k: tuple(_q1159['beta']) for k, _q1159 in a.items()}
        t = json.load(open(os.path.join(_q688, 'wf31_rules_targets_DSM.json')))
        _q1092 = {k: (_q1159['a'], _q1159['b'], _q1159['c'], _q1159['sd']) for k, _q1159 in t.items()}
    return {'additive': _q324, 'standing': _q1092, 'cfg': dict(CFG)}

def window_of(day):
    for _q476, _q477 in WINDOWS:
        if _q476 <= day <= _q477:
            return (_q476, _q477)
    return None

def shop_vector(shop_counts):
    return [float(shop_counts.get(t, 0)) for t in SHOP_TYPES]

def rule_value(rules, _q1197, _q1180, shop_counts, own, rival):
    b = rules['additive'].get('%s_%d_%d' % (_q1197, _q1180[0], _q1180[1]))
    if b is None:
        return 0.0
    _q1159 = sum((_q361 * _q1195 for _q361, _q1195 in zip(b[:8], shop_vector(shop_counts))))
    if len(b) > 8:
        _q1159 += b[8] * own + b[9] * rival
    _q1128 = (rules.get('cfg') or {}).get('target_mult')
    if _q1128 and _q1197 in _q1128 and (_q1159 > 0):
        _q1159 *= float(_q1128[_q1197])
    _q965 = (rules.get('cfg') or {}).get('_qscale')
    if _q965 and _q1197 in _q965 and (_q1159 > 0):
        _q1159 *= float(_q965[_q1197])
    _q642 = _herd_mult(rules, _q1197)
    if _q642 is not None and _q1159 > 0:
        _q1159 *= _q642
    return _q1159

def _herd_mult(rules, _q1197):
    """P8 cfg herd_mult factor of product y (an animal), or None."""
    _q642 = (rules.get('cfg') or {}).get('herd_mult')
    if not _q642 or _q1197 not in ANIMAL_OF:
        return None
    f = _q642.get(ANIMAL_OF[_q1197], _q642.get(_q1197))
    return None if f is None else float(f)

def shops_at_day(shops, day, today):
    """Shops open at hour 0 of `day` (<= today): the town reveals one shop on days 3, 6, 9, ..., 24 (max 8), in
    order, so the first day // 3 entries of today's list."""
    n = min(len(shops), day // 3)
    _q880 = {}
    for s in shops[:n]:
        _q880[s] = _q880.get(s, 0) + 1
    return _q880

def _stock_now(state, _q1197):
    if _q1197 in CROP_OF:
        return state.crop_tiles(CROP_OF[_q1197])
    return state.n_animals(ANIMAL_OF[_q1197])

def _rival_now(state, _q1197):
    _q970 = state.rival
    if _q1197 in CROP_OF:
        return _q970.crop_tiles.get(CROP_OF[_q1197], 0)
    return _q970.animals.get(ANIMAL_OF[_q1197], 0)

def _planted_between(state, _q1197, _q476, _q477):
    if _q1197 in CROP_OF:
        return state.planted_in(CROP_OF[_q1197], _q476, _q477)
    return state.placed_in(ANIMAL_OF[_q1197], _q476, _q477)

def _rival_planted_between(state, _q1197, _q476, _q477):
    _q970 = state.rival
    key = CROP_OF.get(_q1197) or ANIMAL_OF.get(_q1197)
    src = _q970.planted_by_day if _q1197 in CROP_OF else _q970.placed_by_day
    return sum((n for (k, _q475), n in src.items() if k == key and _q476 <= _q475 <= _q477))

def standing_cap(rules, _q1197, state, day):
    """DSM standing-capacity target (+2) for the next census day >= today (R5 view), or None."""
    key = {'S': 'P_STRAWBERRY', 'T': 'P_TOMATO', 'cow': 'A_COW', 'sheep': 'A_SHEEP', 'goose': 'A_GOOSE'}.get(_q1197)
    if key is None:
        return None
    item = {'S': 'STRAWBERRY', 'T': 'TOMATO', 'cow': 'MILK', 'sheep': 'WOOL', 'goose': 'EGG'}[_q1197]
    if _q1197 == 'T':
        _q424 = 20
    else:
        _q424 = next((_q475 for _q475 in (11, 14, 17, 20, 23, 26) if _q475 >= day), 26)
    f = rules['standing'].get('%s_d%d' % (key, _q424))
    if f is None:
        return None
    a, b, c, _ = f
    _q1159 = a + b * state.demand(item) + c * _rival_now(state, _q1197) + 2.0
    _q1128 = (rules.get('cfg') or {}).get('target_mult')
    if _q1128 and _q1197 in _q1128:
        _q1159 *= float(_q1128[_q1197])
    _q965 = (rules.get('cfg') or {}).get('_qscale')
    if _q965 and _q1197 in _q965:
        _q1159 *= float(_q965[_q1197])
    _q642 = _herd_mult(rules, _q1197)
    if _q642 is not None:
        _q1159 *= _q642
    return _q1159

def window_targets(state, rules, day=None, D=None):
    """{y: info} for the window containing `day` (default today), with the rule evaluated on the shops open at the
    window's first day and the own / rival stock at the end of the day before it (reconstructed from planted days).

    Carry-over: the handover days D = 11 / 14 / 17 are LAST days of windows, so a capacity-trimmed remainder would be
    lost; the shortfall of the previous window (its rule minus its plantings, recomputed statelessly) is planted on
    the first day of the next window ('carry'), and later days of that window do not count the carried plantings
    against the window's own target.  Only for windows whose last day was run by PD (>= D)."""
    day = state.day if day is None else day
    _q1180 = window_of(day)
    _q880 = {}
    if _q1180 is None:
        return _q880
    _q476, _q477 = _q1180
    _q1043 = shops_at_day(state.shops, _q476, day)
    _q680 = WINDOWS.index(_q1180)
    _q947 = WINDOWS[_q680 - 1] if _q680 > 0 else None
    if _q947 is not None and D is not None and (_q947[1] < D):
        _q947 = None
    for _q1197 in PRODUCTS_Y:
        carry = 0
        if _q947 is not None and _q1197 != 'W' and (_first_day(_q1197, rules) <= _q947[1] <= _ld(_q1197, rules)):
            _q889, _q890 = _q947
            _q928 = _planted_between(state, _q1197, _q889, _q890)
            _q885 = max(0, _stock_now(state, _q1197) - _planted_between(state, _q1197, _q889, day - 1))
            _q1006 = max(0, _rival_now(state, _q1197) - _rival_planted_between(state, _q1197, _q889, day - 1))
            _q1025 = rule_value(rules, _q1197, _q947, shops_at_day(state.shops, _q889, day), _q885, _q1006)
            carry = max(0, int(round(_q1025)) - _q928)
        _q929 = _planted_between(state, _q1197, _q476, day - 1)
        planted = _q929 - (min(carry, _planted_between(state, _q1197, _q476, _q476)) if day > _q476 else 0)
        own0 = max(0, _stock_now(state, _q1197) - _q929)
        _q1005 = max(0, _rival_now(state, _q1197) - _rival_planted_between(state, _q1197, _q476, day - 1))
        _q1027 = rule_value(rules, _q1197, _q1180, _q1043, own0, _q1005)
        _q880[_q1197] = {'window': _q1180, 'rule': _q1027, 'own0': own0, 'rival0': _q1005, 'planted': planted, 'remaining': max(0, int(round(_q1027)) - planted), 'carry': carry if day == _q476 else 0}
    return _q880

def _ripe_for_reuse(_q458, day):
    if _q458.ongoing:
        return False
    if _q458.decaying:
        return True
    if not _q458.harvestable():
        return False
    if _q458.crop == 'WHEAT':
        return _q458.age >= 3
    if _q458.crop == 'CARROT':
        return _q458.age >= 3
    if _q458.crop == 'MELON':
        return _q458.age >= 12 or (_q458.age >= 10 and _q458.units >= 6)
    return False

def _free_inventory(state, _q841, _q720):
    """[(xy, prep_cost, kind, not_before)] tiles a PLANT/BUILD can use today."""
    day = state.day
    inv = []
    for xy in state.empty:
        inv.append((xy, 0, 'empty', 0))
    for xy in state.weeds:
        inv.append((xy, 1, 'weed', 0))
    for xy, _q458 in state.crops.items():
        if _q458.ongoing and _q458.prods_left == 0:
            inv.append((xy, 1 + (_q458.units > 0), 'spent', 0))
        elif _ripe_for_reuse(_q458, day):
            inv.append((xy, 1 + (0 if _q458.age >= CROPS[_q458.crop]['myd'] else 1), 'ripe', 0))
    for q in _q841:
        for xy in QUAD_TILES[q]:
            if xy in state.locked:
                inv.append((xy, 0, 'new', _q720[q] + 1))
    return inv

def _animal_neighbour_bonus(state, xy):
    x, _q1197 = xy
    n = 0
    for _q518, _q519 in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (x + _q518, _q1197 + _q519) in state.animals or (x + _q518, _q1197 + _q519) in state.structures:
            n += 1
    return 0.3 * n

def _score(state, xy, _q945, _q614, _q497=None):
    q = quadrant_of(*xy)
    s = _q945 * 0.7 + access_dist(xy) * (DIST_W if _q497 is None else _q497)[_q614] + 2.0 * QUAD_PEN[_q614][q]
    if _q614 == 'A':
        s -= _animal_neighbour_bonus(state, xy)
    return s

def _crop_units(crop, fert=True):
    return {'WHEAT': 5.0 if fert else 4.0, 'CARROT': 3.6 if fert else 3.0, 'TOMATO': 7.0 if fert else 4.0, 'STRAWBERRY': 7.4 if fert else 4.0, 'MELON': 6.0}[crop]

def _planting_schedule(crop, day):
    """[(harvest day, units)] of a planting on `day` under DSM husbandry (only days <= FINAL_DAY)."""
    if crop == 'WHEAT':
        _q1045 = [(day + 3, 5.0)]
    elif crop == 'CARROT':
        _q1045 = [(day + 3, 3.6)]
    elif crop == 'TOMATO':
        _q1045 = [(day + a, 1.75) for a in (8, 9, 10, 11)]
    elif crop == 'STRAWBERRY':
        _q1045 = [(day + a, 1.85) for a in (10, 12, 14, 16)]
    else:
        _q1045 = [(day + 10, 6.0)]
    return [(_q475, _q1147) for _q475, _q1147 in _q1045 if _q475 <= FINAL_DAY]

def _animal_rate(animal):
    """(first harvest day offset, units per day) with ~75% care."""
    return {'GOOSE': (5, 1.75), 'COW': (9, 1.25), 'SHEEP': (7, 1.08)}[animal]

def project_cash(state, plan, rules):
    """Closing cash for each day from today to FINAL_DAY under the plan: today's purchases, then a steady state of
    today's hires, the window quotas (current shops) and the yields of what stands plus what is planned, sold one day
    after harvest at haircut x current quote (wheat first feeds the animals; a feed deficit is bought)."""
    cfg = rules['cfg']
    day = state.day
    _q632 = cfg['haircut']
    px = state.prices
    days = list(range(day, FINAL_DAY + 1))
    _q663 = {_q475: 0.0 for _q475 in days}
    _q1081 = {_q475: 0.0 for _q475 in days}
    wheat = {_q475: 0.0 for _q475 in days}

    def _q325(item, _q475, _q1147):
        if _q475 > FINAL_DAY:
            return
        _q479 = min(FINAL_DAY, max(day, _q475 + (0 if _q475 == FINAL_DAY else 1)))
        if item == 'WHEAT':
            wheat[max(day, min(FINAL_DAY, _q475))] += _q1147
            return
        _q663[_q479] += _q1147 * float(px.get(item, 0)) * _q632
    for item, n in state.shed.items():
        if item in ANIMALS or item == 'FERTILIZER':
            continue
        if item == 'WHEAT':
            wheat[day] += n
            continue
        _q663[day] += 0.5 * n * float(px.get(item, 0)) * _q632
        if day + 1 <= FINAL_DAY:
            _q663[day + 1] += 0.5 * n * float(px.get(item, 0)) * _q632
    for _q458 in state.crops.values():
        if _q458.ongoing:
            _q421 = CROPS[_q458.crop]
            _q574 = _q421['fyd'] - 1
            _q679 = _q421['interval']
            if _q458.units > 0:
                _q325(_q458.crop, day, _q458.units)
            k = _q458.prods_done
            for _q652 in range(_q458.prods_left):
                a = _q574 + _q679 * (k + _q652)
                _q325(_q458.crop, _q458.planted_day + a + 1, 1.75)
        else:
            _q1147 = PT._future_units(_q458, day)
            _q634 = max(day, _q458.planted_day + {'WHEAT': 3, 'CARROT': 3, 'MELON': 10}[_q458.crop])
            _q325(_q458.crop, _q634, _q1147)
    _q796 = len(state.animals)
    for _q336 in state.animals.values():
        _q867, _q978 = _animal_rate(_q336.animal)
        if _q336.units:
            _q325(_q336.product, day, _q336.units)
        start = max(day + 1, _q336.placed_day + _q867)
        for _q475 in range(start, FINAL_DAY + 1):
            _q325(_q336.product, _q475, _q978)
        for _q475 in range(day + 1, FINAL_DAY + 1):
            _q663[_q475] += 0.45 * float(px.get('FERTILIZER', 0)) * _q632
    _q1081[day] += plan.get('spend_today', 0.0)
    for op, xy, arg in plan.get('ops', ()):
        if op == 'PLANT':
            for _q475, _q1147 in _planting_schedule(arg, day):
                _q325(arg, _q475, _q1147)
        elif op == 'PLACE':
            _q867, _q978 = _animal_rate(arg)
            for _q475 in range(day + _q867, FINAL_DAY + 1):
                _q325(ANIMALS[arg]['product'], _q475, _q978)
            _q796 += 1
    hands = plan.get('hires', 0)
    _q480 = hire_cost(0, hands)
    _q602 = plan.get('future_daily', {})
    for _q475 in days[1:]:
        _q1081[_q475] += _q480
        for _q1197, _q918 in _q602.get(_q475, {}).items():
            if _q1197 in CROP_OF:
                crop = CROP_OF[_q1197]
                _q1081[_q475] += _q918 * CROPS[crop]['seed']
                for _q484, _q1147 in _planting_schedule(crop, _q475):
                    _q325(crop, _q484, _q1147 * _q918)
            else:
                a = ANIMAL_OF[_q1197]
                _q1081[_q475] += _q918 * ANIMALS[a]['cost']
                _q867, _q978 = _animal_rate(a)
                for _q484 in range(_q475 + _q867, FINAL_DAY + 1):
                    _q325(ANIMALS[a]['product'], _q484, _q978 * _q918)
                _q796 += _q918
    stock = 0.0
    _q1187 = float(px.get('WHEAT', 25))
    for _q475 in days:
        stock += wheat[_q475]
        need = _q796 * cfg['wheat_feed_rate'] if _q475 > day else 0.0
        if stock >= need:
            stock -= need
            if stock > 20:
                _q663[_q475] += (stock - 20) * _q1187 * _q632
                stock = 20.0
        else:
            _q1081[_q475] += (need - stock) * (_q1187 + 2)
            stock = 0.0
    cash = state.money
    _q880 = []
    for _q475 in days:
        cash = cash - _q1081[_q475] + _q663[_q475]
        _q880.append((_q475, round(cash, 1)))
    return _q880

def _ld(_q1197, rules):
    """Last planting day of y (cfg last_day over LAST_DAY)."""
    _q857 = rules['cfg'].get('last_day') if isinstance(rules, dict) and 'cfg' in rules else None
    if _q857 and _q1197 in _q857:
        return _q857[_q1197]
    return LAST_DAY[_q1197]

def _first_day(_q1197, rules):
    if _q1197 == 'S':
        return rules['cfg'].get('s_first_day', FIRST_DAY['S'])
    return FIRST_DAY.get(_q1197, 0)

def _quota_today(_q1197, _q665, day, rules, state):
    _q476, _q477 = _q665['window']
    if day > _ld(_q1197, rules) or day < _first_day(_q1197, rules):
        return 0
    rem = _q665['remaining']
    carry = _q665.get('carry', 0)
    if rem <= 0 and carry <= 0:
        return 0
    _q723 = min(_q477, _ld(_q1197, rules))
    _q482 = max(1, _q723 - day + 1)
    if _q1197 in FRONT_LOADED or (_q1197 == 'T' and _q476 == 18):
        q = rem
    else:
        q = int(math.ceil(rem / _q482))
    q += carry
    cap = standing_cap(rules, _q1197, state, day)
    if cap is not None:
        q = min(q, max(0, int(math.floor(cap)) - _stock_now(state, _q1197)))
    return max(0, q)

def _future_daily(state, rules, day, D):
    """Expected plantings per day for the days after today (cash projection only): the additive rule of each later
    window at today's shops, own stock = today's standing, spread evenly over the window."""
    _q880 = {}
    for _q476, _q477 in WINDOWS:
        if _q477 <= day:
            continue
        for _q1197 in PRODUCTS_Y:
            if _q1197 == 'W':
                continue
            _q1159 = rule_value(rules, _q1197, (_q476, _q477), state.shop_counts, _stock_now(state, _q1197), _rival_now(state, _q1197))
            if _q1159 <= 0.5:
                continue
            days = [_q475 for _q475 in range(max(_q476, day + 1), min(_q477, _ld(_q1197, rules)) + 1) if _q475 >= _first_day(_q1197, rules)]
            if not days:
                continue
            _q917 = _q1159 / len(days) * (len(days) / float(_q477 - _q476 + 1))
            for _q475 in days:
                _q880.setdefault(_q475, {})[_q1197] = _q917
    return _q880

def _wf_ripe(_q458, day):
    """Wheat-first reuse rule: wheat at age 4, or at age 3 when fertilised (fert_until >= today: the age-3 WATER adds +2,
    DSM cuts 50% at age 3 with 4.97 u); carrots at age 3; melons / decaying crops as _ripe_for_reuse."""
    if _q458.ongoing:
        return False
    if _q458.decaying:
        return True
    if not _q458.harvestable():
        return False
    if _q458.crop == 'WHEAT':
        return _q458.age >= 4 or (_q458.age == 3 and _q458.fert_until >= day)
    if _q458.crop == 'CARROT':
        return _q458.age >= 3
    if _q458.crop == 'MELON':
        return _q458.age >= 12 or (_q458.age >= 10 and _q458.units + (0 if _q458.watered else _q458.water_gain(day)) >= 6)
    return False

def _wf_free(state, _q841, _q720):
    """[(xy, prep_cost, kind, not_before, cls)]: _free_inventory with the wheat-first reuse rule; cls 'wh' = ripe
    rotation wheat, 'freed' = spent strawberry / tomato (harvested + dug on its last harvest day) or another ripe crop,
    'open' = empty / weed / newly bought tile."""
    day = state.day
    inv = []
    for xy in state.empty:
        inv.append((xy, 0, 'empty', 0, 'open'))
    for xy in state.weeds:
        inv.append((xy, 1, 'weed', 0, 'open'))
    for xy, _q458 in state.crops.items():
        if _q458.ongoing and _q458.prods_left == 0:
            inv.append((xy, 1 + (_q458.units > 0), 'spent', 0, 'freed'))
        elif _wf_ripe(_q458, day):
            inv.append((xy, 1 + (0 if _q458.age >= CROPS[_q458.crop]['myd'] else 1), 'ripe', 0, 'wh' if _q458.crop == 'WHEAT' else 'freed'))
    for q in _q841:
        for xy in QUAD_TILES[q]:
            if xy in state.locked:
                inv.append((xy, 0, 'new', _q720[q] + 1, 'open'))
    return inv

def _wf_qscale(state, c):
    """{y: quota factor} from the owned land (unlocked tiles + today's due fixed-step quadrants): 1 - (1 - f3) x missing
    quadrants (f3 = the 3-quadrant factor of wf_quota_land), within [0.1, 1]; None when the table is empty."""
    _q1112 = c.get('wf_quota_land')
    if _q1112 is None:
        _q1112 = WF_LAND_Q
    if not _q1112:
        return None
    owned = len(QUAD_TILES) * 25 - len(state.locked)
    _q752 = c.get('land_steps') or {}
    for _q966 in LAND_ORDER[max(0, state.n_quads - 1):]:
        if _q966 in _q752 and int(_q752[_q966]) <= 24 * state.day + 23:
            owned += 25
        else:
            break
    short = max(0, 100 - owned) / 25.0
    return {_q1197: max(0.1, min(1.0, 1.0 - (1.0 - float(f)) * short)) for _q1197, f in _q1112.items()}

def _wf_alloc(state, rules, c, plan, _q968, _q529, _q841, _q720, _q1132, _q718):
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
    free = _wf_free(state, _q841, _q720)
    owned = len(QUAD_TILES) * 25 - len(state.locked) + 25 * len(_q841)
    _q316, _q580, _q457 = c.get('wf_wstar') or WF_WSTAR
    _q1184 = _ld('W', rules)
    _q796 = len(state.animals) + sum((_q968.get(_q1197, 0) for _q1197 in ANIMAL_OF))
    if day <= min(_q1184, int(c.get('wf_wstar_last', 27))):
        floor = int(round(_q580 * owned))
        wstar = max(floor, min(int(round(_q457 * owned)), int(round(_q316 * _q796))))
    else:
        floor = wstar = 0
    _q1171 = c.get('wheat_bias')
    if _q1171 is not None:
        floor = max(0, int(round(floor * float(_q1171))))
        wstar = max(0, int(round(wstar * float(_q1171))))
    _q756 = c.get('late_tc_prio')
    _q756 = _q756 is not None and day >= int(_q756)
    _q593 = set((f[0] for f in free))
    stand0 = sum((1 for xy, _q458 in state.crops.items() if _q458.crop == 'WHEAT' and xy not in _q593))
    need = max(0, wstar - stand0) if day <= _q1184 else 0
    _q1043 = {}

    def _q1046(f, g):
        k = (g, f[0])
        _q1159 = _q1043.get(k)
        if _q1159 is None:
            _q1159 = _score(state, f[0], f[1], g, dw) + 0.5 * f[3] / 24.0
            _q1043[k] = _q1159
        return _q1159
    _q437 = {}
    wh = sorted((f for f in free if f[4] == 'wh'), key=lambda f: (_q1046(f, 'W'), f[0]))
    for _q652, f in enumerate(wh):
        _q437[f[0]] = 'wh_in' if _q652 < need else 'wh_up'
    for f in free:
        if f[4] != 'wh':
            _q437[f[0]] = f[4]
    budget = max(0, len(free) - need)
    _q1157 = set()

    def _q921(g, _q1125):
        for _q1124 in _q1125:
            best, _q365 = (None, None)
            for f in free:
                if f[0] in _q1157 or _q437[f[0]] not in _q1124:
                    continue
                k = (_q1046(f, g), f[0])
                if _q365 is None or k < _q365:
                    best, _q365 = (f, k)
            if best is not None:
                _q1157.add(best[0])
                return best
        return None
    ops = []
    _q737 = budget
    for _q1197 in ('goose', 'cow', 'sheep'):
        a = ANIMAL_OF[_q1197]
        k = STRUCT[a]
        _q899 = int(state.shed.get(a, 0))
        for _q652 in range(_q968[_q1197]):
            if _q529[k]:
                ops.append(('PLACE', _q529[k].pop(0), a))
                continue
            if _q737 <= 0 and _q652 >= _q899:
                break
            t = _q921('A', (('open', 'freed', 'wh_up'),) + ((('wh_in',),) if _q652 < _q899 else ()))
            if t is None:
                break
            _q737 -= 1
            ops.append(('BUILD_' + k, t[0], None))
            ops.append(('PLACE', t[0], a))
    _q1126 = (('freed',), ('wh_up',), ('wh_in',), ('open',))
    _q1125 = {'T': _q1126, 'S': _q1126, 'C': (('freed',), ('wh_up',), ('open',))}
    if _q756:
        _q1125['C'] = _q1125['C'] + (('wh_in',),)
    _q927 = []
    sp = c.get('wf_s_prio')
    _q592 = ('S', 'T') if sp == 'ST' else ('S',) if sp else ()
    if _q756:
        _q592 = tuple(_q592) + tuple((_q1197 for _q1197 in ('T', 'C') if _q1197 not in _q592))
    for _q1197 in ('S', 'T', 'C') if sp else ('T', 'S', 'C'):
        for _ in range(_q968[_q1197]):
            if _q737 <= 0 and _q1197 not in _q592:
                break
            t = _q921(_q1197, _q1125[_q1197])
            if t is None:
                break
            _q737 -= 1
            _q927.append((_q1197, t))
    cf = c.get('wf_fill_carrot', WF_FILL_C)
    _q422 = bool(cf) and cf[0] <= day <= min(cf[1], _ld('C', rules))
    margin = int(c.get('wf_w_margin', 4))
    rest = sorted((f for f in free if f[0] not in _q1157), key=lambda f: (0 if _q437[f[0]] in ('wh_in', 'wh_up') else 1, _q1046(f, 'W'), f[0]))
    _q854 = 0
    for f in rest:
        if day <= _q1184 and (not _q422 or stand0 + _q854 < wstar + margin):
            _q927.append(('W', f))
            _q854 += 1
        elif _q422:
            _q927.append(('C', f))
    _q352 = PT.due_tasks(state, dict(_q1132, land=plan['land']))
    _q714 = c['l2_done_share']
    _q821 = sum((1 for t in _q352 if t.level >= 2)) * _q714 + sum((1 for t in _q352 if t.level >= 3)) * (1 - _q714)
    _q715 = float(c.get('wf_l2', 1.0))
    _q555 = c.get('wf_fert_crops')
    _q1088 = {}
    _q822 = 0.0
    _q625 = set()
    for t in _q352:
        w = _q715 if t.level == 2 else 1.0 if t.level >= 3 else 0.0
        if _q555 is not None and t.op == 'FERTILIZE':
            _q458 = state.crops.get(t.xy)
            if _q458 is None or _q458.crop not in _q555:
                w = 0.0
        if w:
            _q822 += w
            _q1088[t.xy] = _q1088.get(t.xy, 0.0) + w
        if t.op == 'HARVEST' and t.level >= 2:
            _q625.add(t.xy)
    _q763 = {}
    if _q927:
        _q951 = PT.due_tasks(state, dict(_q1132, land=plan['land'], ops=[('PLANT', t[0], 'WHEAT') for _, t in _q927]))
        chain = {}
        for t in _q951:
            if t.src == 'plan' and (not (t.op == 'FERTILIZE' and t.level < 2)):
                chain[t.xy] = chain.get(t.xy, 0) + 1
        for _, t in _q927:
            _q763[t[0]] = max(1.0, chain.get(t[0], 2) - _q1088.get(t[0], 0.0))
    hands = c['max_hands'] if _q718 is None else min(_q718, c['max_hands'])
    _q1108, _q1109 = c.get('wf_cap') or WF_CAP
    cap_tasks = (float(_q1108) + float(_q1109) * hands) / float(c.get('wf_tpt', 1.95))
    _q797 = sum((1 for _q857 in ops if _q857[0] == 'PLACE')) * 4 + sum((1 for _q857 in ops if _q857[0].startswith('BUILD')))

    def load():
        return _q822 + _q797 + sum((_q763[t[0]] for _, t in _q927))
    trimmed = {'W': 0, 'C': 0, 'S': 0, 'T': 0}
    _q1110 = ('W+', 'W-', 'C', 'S', 'T') if _q756 else ('W+', 'C', 'W-', 'S', 'T')
    while _q927 and load() > cap_tasks:
        _q1091 = stand0 + sum((1 for _q1205, _ in _q927 if _q1205 == 'W'))
        for g in _q1110:
            if g == 'W+' and _q1091 <= wstar:
                continue
            if g == 'W-' and _q1091 <= floor:
                continue
            _q1197 = g[0]
            _q656 = [_q652 for _q652, (_q1205, _) in enumerate(_q927) if _q1205 == _q1197]
            if _q656:
                _q927.pop(_q656[-1])
                trimmed[_q1197] += 1
                break
        else:
            break
    for _q1197, t in _q927:
        ops.append(('PLANT', t[0], CROP_OF[_q1197]))
    plan['ops'] = ops
    plan['w_keep'] = None
    _q854 = sum((1 for _q1205, _ in _q927 if _q1205 == 'W'))
    planted = set((t[0] for _, t in _q927))
    kept = sum((1 for f in wh if f[0] not in planted and f[0] not in _q625))
    plan['wheat'] = {'wstar': wstar, 'floor': floor, 'owned': owned, 'stand0': stand0, 'need': need, 'free': len(free), 'ripe_w': len(wh), 'budget': budget, 'quota_tiles': budget - _q737, 'plant_w': _q854, 'tonight': stand0 + _q854 + kept, 'cap_tasks': round(cap_tasks, 1), 'load': round(load(), 1), 'trimmed': trimmed, 'qscale': c.get('_qscale')}
    _q768 = 1 + (c['max_hands'] if _q718 is None else _q718)
    return (ops, _q821, _q768)

def plan_day(state, rules=None, D=11, cfg=None):
    rules = rules or load_rules()
    c = dict(rules['cfg'])
    if cfg:
        c.update(cfg)
    rules = dict(rules, cfg=c)
    _q1173 = c.get('alloc') == 'wheat_first'
    if _q1173:
        _q733 = dict(WF_LAST_DAY if c.get('wf_last_day') is None else c['wf_last_day'])
        _q733.update(c.get('last_day') or {})
        c['last_day'] = _q733
        _q965 = _wf_qscale(state, c)
        if _q965:
            c['_qscale'] = _q965
    day = state.day
    plan = {'day': day, 'D': D, 'active': day >= D, 'ops': [], 'land': [], 'hires': 0, 'orders': {}, 'deferred': [], 'targets': {}, 'fert_wheat': float(state.prices.get('FERTILIZER', 100)) <= c.get('fert_wheat_q', 55)}
    _q1132 = dict(c.get('task_opts') or {})
    plan.update(_q1132)
    if day < D:
        return plan
    _q718 = None
    _q717 = c.get('hire_ladder')
    if _q717 is not None:
        try:
            _q1159 = _q717.get(day, _q717.get(str(day))) if isinstance(_q717, dict) else _q717[min(day, len(_q717) - 1)]
            _q718 = None if _q1159 is None else max(0, int(_q1159))
        except (IndexError, TypeError, ValueError):
            _q718 = None
    wt = window_targets(state, rules, day, D)
    _q968 = {_q1197: 0 for _q1197 in PRODUCTS_Y}
    for _q1197, _q665 in wt.items():
        q = _quota_today(_q1197, _q665, day, rules, state)
        if _q1197 == 'W':
            q = 0
        if _q1197 in ANIMAL_OF and (not c.get('animals', True)):
            q = 0
        _q968[_q1197] = q
    _q427 = c.get('cow_gate')
    if _q427:
        if day < int(_q427.get('min_day', 0)):
            _q968['cow'] = 0
        elif _q427.get('max_new') is not None:
            _q968['cow'] = max(0, min(_q968['cow'], int(_q427['max_new']) - state.placed_in('COW', D, day)))
    if c.get('no_geese'):
        _q968['goose'] = 0
    if c.get('tom_cap') is not None:
        _q968['T'] = max(0, min(_q968['T'], int(c['tom_cap'])))
    if c.get('place_shed') and day <= 27:
        for _q1197 in ('goose', 'cow', 'sheep'):
            _q968[_q1197] = max(_q968[_q1197], int(state.shed.get(ANIMAL_OF[_q1197], 0)))
    _q633 = c.get('herd_cap')
    if _q633:
        for _q1197 in ('goose', 'cow', 'sheep'):
            a = ANIMAL_OF[_q1197]
            _q406 = _q633.get(a, _q633.get(_q1197))
            if _q406 is None:
                continue
            _q660 = int(state.shed.get(a, 0))
            owned = state.n_animals(a) + _q660 + sum((int(_q652.get(a, 0) or 0) for _q652 in state.inventories))
            _q968[_q1197] = max(0, min(_q968[_q1197], _q660 + max(0, int(_q406) - owned)))
    if c.get('animals', True) == 'existing':
        _q591 = {'COOP': sum((1 for k in state.structures.values() if k == 'COOP')), 'PASTURE': sum((1 for k in state.structures.values() if k == 'PASTURE'))}
        for _q1197 in ('goose', 'cow', 'sheep'):
            k = STRUCT[ANIMAL_OF[_q1197]]
            _q968[_q1197] = min(_q968[_q1197], _q591[k])
            _q591[k] -= _q968[_q1197]
    _q529 = {'COOP': [xy for xy, k in state.structures.items() if k == 'COOP'], 'PASTURE': [xy for xy, k in state.structures.items() if k == 'PASTURE']}
    _q834 = sum((_q968[_q1197] for _q1197 in ('S', 'T', 'C')))
    for _q1197 in ('cow', 'sheep', 'goose'):
        a = ANIMAL_OF[_q1197]
        _q834 += max(0, _q968[_q1197] - len(_q529[STRUCT[a]]))
    _q841, _q720 = ([], {})
    _q804 = len(_free_inventory(state, [], {}))
    _q749 = _q834 + sum((sum(_q1159.values()) for _q475, _q1159 in _future_daily(state, rules, day, D).items() if _q475 <= day + 2))
    money = state.money
    _q351 = hire_cost(0, c['max_hands']) + 200.0
    n_quads = state.n_quads
    staff_cap = None
    if c.get('land_after_trim') and n_quads < 4:
        _q380 = PT.due_tasks(state, dict(_q1132, land=[]))
        _q853 = sum((1 for t in _q380 if t.level >= 2)) * c['l2_done_share'] + sum((1 for t in _q380 if t.level >= 3)) * (1 - c['l2_done_share'])
        _q786 = 1 + c['max_hands']
        _q403 = _q786 * c['turns_per_unit'] / c['turns_per_task'] - 2 * _q786 / c['turns_per_task']
        _q826 = sum((_q968[_q1197] for _q1197 in ('cow', 'sheep', 'goose'))) * 4
        staff_cap = max(0, int((_q403 - _q853 - _q826) // 2.5))
        plan['staff_cap'] = staff_cap
    _q754 = c.get('land_steps') or {}
    while n_quads < 4:
        price = LAND_PRICES[n_quads - 1]
        _q966 = ('NE', 'SW', 'SE')[n_quads - 1]
        hour = 0
        if _q966 in _q754:
            _q1032 = int(_q754[_q966])
            hour = max(0, _q1032 - 24 * day)
            if _q1032 > 24 * day + 23 or (hour == 0 and money < price):
                break
            money -= price
            _q841.append(_q966)
            _q720[_q966] = hour
            plan['land'].append((hour, _q966))
            _q804 += 25
            n_quads += 1
            continue
        if _q966 == 'SE':
            hour = max(0, c['se_step'] - 24 * day)
            if hour > 20:
                break
            if staff_cap is not None:
                if min(_q749, staff_cap) + 4 <= _q804:
                    break
                if c.get('prev_hires') is not None and int(c['prev_hires']) >= c['max_hands']:
                    break
        if _q749 + 4 <= _q804:
            break
        if money < price + _q351 + c['reserve']:
            break
        money -= price
        _q841.append(_q966)
        _q720[_q966] = hour
        plan['land'].append((hour, _q966))
        _q804 += 25
        n_quads += 1
    if _q1173:
        ops, _q821, _q768 = _wf_alloc(state, rules, c, plan, _q968, _q529, _q841, _q720, _q1132, _q718)
    else:
        free = _free_inventory(state, _q841, _q720)
        _q1157 = set()
        ops = []
        _q977 = {}

        def _q1114(_q614, allow=None):
            _q753 = _q977.get(_q614)
            if _q753 is None:
                _q753 = sorted(free, key=lambda f: (_score(state, f[0], f[1], _q614) + 0.5 * f[3] / 24.0, f[0]))
                _q753.reverse()
                _q977[_q614] = _q753
            for _q652 in range(len(_q753) - 1, -1, -1):
                f = _q753[_q652]
                if f[0] in _q1157:
                    _q753.pop(_q652)
                    continue
                if allow is not None and (not allow(f)):
                    continue
                _q753.pop(_q652)
                _q1157.add(f[0])
                return f
            return None
        for _q1197 in ('goose', 'cow', 'sheep'):
            a = ANIMAL_OF[_q1197]
            k = STRUCT[a]
            n = _q968[_q1197]
            for _ in range(n):
                if _q529[k]:
                    xy = _q529[k].pop(0)
                    ops.append(('PLACE', xy, a))
                    continue
                t = _q1114('A')
                if t is None:
                    break
                ops.append(('BUILD_' + k, t[0], None))
                ops.append(('PLACE', t[0], a))
        _q927 = []
        for _q1197 in ('T', 'S', 'C'):
            for _ in range(_q968[_q1197]):
                t = _q1114(_q1197)
                if t is None:
                    break
                _q927.append((_q1197, t))
        if day <= _ld('W', rules):
            while True:
                t = _q1114('W', allow=lambda f: not (f[2] == 'ripe' and f[1] >= 2))
                if t is None:
                    break
                _q927.append(('W', t))
        _q352 = PT.due_tasks(state, dict(_q1132, land=plan['land']))
        _q821 = sum((1 for t in _q352 if t.level >= 2)) * c['l2_done_share'] + sum((1 for t in _q352 if t.level >= 3)) * (1 - c['l2_done_share'])
        _q919 = {'empty': 2, 'new': 2, 'weed': 3, 'spent': 3.5, 'ripe': 3}
        _q797 = sum((1 for _q857 in ops if _q857[0] == 'PLACE')) * 4 + sum((1 for _q857 in ops if _q857[0].startswith('BUILD')))
        _q768 = 1 + (c['max_hands'] if _q718 is None else _q718)
        cap_tasks = _q768 * c['turns_per_unit'] / c['turns_per_task'] - 2 * _q768 / c['turns_per_task']

        def load(_q922):
            return _q821 + _q797 + sum((_q919[t[2]] for _, t in _q922))
        _q874 = ('W', 'C', 'S', 'T')
        w_keep = 0
        if c.get('w_feed_tiles'):
            _q796 = len(state.animals) + sum((1 for _q857 in ops if _q857[0] == 'PLACE'))
            _q1203 = sum((1 for _q458 in state.crops.values() if _q458.crop == 'WHEAT' and _q458.age < CROPS['WHEAT']['myd'] and (not _q458.decaying)))
            _q1174 = c['w_feed_tiles'] * (1.0 if c.get('wheat_bias') is None else float(c['wheat_bias']))
            w_keep = max(0, int(math.ceil(_q1174 * _q796)) - _q1203)
        plan['w_keep'] = w_keep
        while _q927 and load(_q927) > cap_tasks:
            _q824 = sum((1 for _q1205, _ in _q927 if _q1205 == 'W'))
            for _q1197 in _q874:
                if _q1197 == 'W' and _q824 <= w_keep:
                    continue
                _q656 = [_q652 for _q652, (_q1205, _) in enumerate(_q927) if _q1205 == _q1197]
                if _q656:
                    _q927.pop(_q656[-1])
                    break
            else:
                break
        for _q1197, t in _q927:
            ops.append(('PLANT', t[0], CROP_OF[_q1197]))
        plan['ops'] = ops
    tasks = PT.due_tasks(state, plan)
    _q819 = sum((1 for t in tasks if t.src == 'plan')) + _q821
    turns = _q819 * c['turns_per_task'] + 2 * _q768
    units_needed = int(math.ceil(turns / float(c['turns_per_unit'])))
    hands = max(c['min_hands'], min(c['max_hands'], units_needed - 1)) if _q718 is None else _q718
    _q875 = []
    _q1081 = 0.0
    cash = state.money
    deferred = []
    reserve = c['reserve']
    _q423 = bool(c.get('cash_defer'))

    def _q400(cost):
        return _q423 or cash - _q1081 - cost >= reserve
    _q722 = {}

    def _q387():
        nonlocal _q1081
        _q702 = []
        for hour, _q966 in plan['land']:
            price = LAND_PRICES[('NE', 'SW', 'SE').index(_q966)]
            if _q966 in _q754:
                _q1081 += price
                _q722.setdefault(hour, []).append(['BUY_LAND'])
                _q702.append((hour, _q966))
                continue
            if _q400(price):
                _q1081 += price
                _q722.setdefault(hour, []).append(['BUY_LAND'])
                _q702.append((hour, _q966))
            else:
                deferred.append(['BUY_LAND', _q966])
        if len(_q702) < len(plan['land']):
            _q750 = {q for _, q in plan['land']} - {q for _, q in _q702}
            plan['ops'] = [_q857 for _q857 in plan['ops'] if quadrant_of(*_q857[1]) not in _q750 or _q857[1] not in state.locked]
            plan['land'] = _q702
    _q627 = 0
    while _q627 < hands and _q400(fib(state.hires_today + _q627)):
        _q1081 += fib(state.hires_today + _q627)
        _q627 += 1
    _q875 += [['HIRE'] for _ in range(_q627)]
    if _q627 < hands:
        deferred.append(['HIRE', hands - _q627])
    plan['hires'] = _q627
    if _q754:
        _q387()
    _q829 = PT.needs(tasks)
    _q1178 = state.shed.get('WHEAT', 0) + 0.5 * sum((state.crops[t.xy].units for t in tasks if t.op == 'HARVEST' and t.xy in state.crops and (state.crops[t.xy].crop == 'WHEAT')))
    _q561 = int(max(0, _q829.get('WHEAT', 0) - _q1178))
    _q1187 = float(state.prices.get('WHEAT', 25)) + 1
    if _q561:
        k = min(_q561, max(0, int((cash - _q1081 - reserve) // _q1187)) if not _q423 else _q561, state.shed_room)
        if k > 0:
            _q875.append(['BUY_PRODUCT', 'WHEAT', k])
            _q1081 += k * _q1187
        if k < _q561:
            deferred.append(['BUY_PRODUCT', 'WHEAT', _q561 - k])
    if not _q754:
        _q387()
    _q386 = {}
    for op, xy, arg in plan['ops']:
        if op == 'PLACE':
            _q386[arg] = _q386.get(arg, 0) + 1
    shed_room = state.shed_room - sum((_q857[2] for _q857 in _q875 if _q857[0] == 'BUY_PRODUCT'))
    _q508 = {}
    for a, n in _q386.items():
        _q630 = state.shed.get(a, 0)
        _q696 = max(0, n - _q630)
        k = 0
        while k < _q696 and _q400(ANIMALS[a]['cost']) and (shed_room > 0):
            _q1081 += ANIMALS[a]['cost']
            k += 1
            shed_room -= 1
        if k:
            _q875.append(['BUY_ANIMAL', a, k])
        if k < _q696:
            deferred.append(['BUY_ANIMAL', a, _q696 - k])
            _q508[a] = _q696 - k
    if _q508:
        keep = []
        for _q857 in reversed(plan['ops']):
            if _q857[0] == 'PLACE' and _q508.get(_q857[2], 0) > 0:
                _q508[_q857[2]] -= 1
                continue
            keep.append(_q857)
        keep.reverse()
        plan['ops'] = keep
    _q1048 = {}
    for op, xy, arg in plan['ops']:
        if op == 'PLANT':
            _q1048[arg] = _q1048.get(arg, 0) + 1
    _q509 = {}
    for crop in ('STRAWBERRY', 'TOMATO', 'CARROT', 'WHEAT'):
        n = max(0, _q1048.get(crop, 0) - state.seeds.get(crop, 0))
        if not n:
            continue
        k = min(n, max(0, int((cash - _q1081 - reserve) // CROPS[crop]['seed']))) if not _q423 else n
        if k:
            _q875.append(['BUY_SEED', crop, k])
            _q1081 += k * CROPS[crop]['seed']
        if k < n:
            deferred.append(['BUY_SEED', crop, n - k])
            _q509[crop] = n - k
    if _q509:
        keep = []
        for _q857 in reversed(plan['ops']):
            if _q857[0] == 'PLANT' and _q509.get(_q857[2], 0) > 0:
                _q509[_q857[2]] -= 1
                continue
            keep.append(_q857)
        keep.reverse()
        plan['ops'] = keep
    _q588 = float(state.prices.get('FERTILIZER', 100))
    _q546 = _q829.get('FERTILIZER', 0) - state.shed.get('FERTILIZER', 0) - sum((1 for t in tasks if t.op == 'COLLECT_FERTILIZER'))
    if _q546 > 0 and _q588 <= c['fert_buy_max']:
        k = min(_q546, max(0, int((cash - _q1081 - reserve) // (_q588 + 1))), max(0, shed_room))
        if k:
            _q875.append(['BUY_PRODUCT', 'FERTILIZER', k])
            _q1081 += k * (_q588 + 1)
    _q638 = [_q857 for _q857 in _q875 if _q857[0] == 'HIRE']
    _q388 = [_q857 for _q857 in _q875 if _q857[0] != 'HIRE']
    h0 = list(_q722.get(0, [])) + _q638[:8]
    _q1014 = max(0, 10 - len(h0))
    h0 += _q388[:_q1014]
    pending = _q638[8:] + _q388[_q1014:]
    orders = {0: h0}
    h = 1
    while pending or any((k >= h for k in _q722)):
        _q467 = list(_q722.get(h, [])) + pending
        if _q467:
            orders[h] = _q467[:10]
        pending = _q467[10:]
        h += 1
        if h > 23:
            break
    plan['orders'] = orders
    plan['deferred'] = deferred
    plan['spend_today'] = _q1081
    _q570 = {'S': 0, 'T': 0, 'C': 0, 'W': 0, 'cow': 0, 'sheep': 0, 'goose': 0}
    for op, xy, arg in plan['ops']:
        if op == 'PLANT':
            _q570[{_q1159: k for k, _q1159 in CROP_OF.items()}[arg]] += 1
        elif op == 'PLACE':
            _q570[{_q1159: k for k, _q1159 in ANIMAL_OF.items()}[arg]] += 1
    _q602 = _future_daily(state, rules, day, D)
    plan['future_daily'] = _q602
    for _q1197, _q665 in wt.items():
        _q476, _q477 = _q665['window']
        rest = 0
        carry = _q665.get('carry', 0)
        _q1130 = max(0, _q570[_q1197] - carry)
        if _q1197 != 'W' and _first_day(_q1197, rules) <= day <= _ld(_q1197, rules):
            if day < min(_q477, _ld(_q1197, rules)) or day + 1 <= _ld(_q1197, rules):
                rest = max(0, _q665['remaining'] - _q1130)
        cap = standing_cap(rules, _q1197, state, day)
        plan['targets'][_q1197] = dict(_q665, quota=_q968.get(_q1197, 0), today=_q570[_q1197], today_window=_q1130, rest=rest, window_total=_q665['planted'] + _q1130 + rest, cap=None if cap is None else round(cap, 2), active=_first_day(_q1197, rules) <= day <= _ld(_q1197, rules))
    _q956 = project_cash(state, plan, rules)
    plan['cash'] = {'start': state.money, 'spend_today': round(_q1081, 1), 'projection': _q956, 'min': min((_q1159 for _, _q1159 in _q956)) if _q956 else state.money}
    plan['tasks'] = PT.due_tasks(state, plan)
    plan['task_turns'] = int(turns)
    plan['units_needed'] = units_needed
    return plan