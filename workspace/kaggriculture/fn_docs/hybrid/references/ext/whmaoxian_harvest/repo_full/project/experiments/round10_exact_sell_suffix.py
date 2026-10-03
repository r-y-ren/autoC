# Round 10 isolated experiment. Retain V9's model, but optimize all eligible
# contiguous SELL blocks jointly against one fixed opponent order list.
import itertools as _r10x_it

_R10X_LIMIT = 720
_R10X_REPORT = {'calls': 0, 'changed': 0, 'joint_blocks': 0,
                'skipped_budget': 0, 'evaluations': 0, 'model_gain': 0.0,
                'errors': 0}


def _r10x_exact_reorder(obs, action):
    market = action.get('market') or []
    if len(market) < 2:
        return action
    orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
    blocks = []
    i = 0
    while i < len(orders):
        order = orders[i]
        if order and order[0] == 'SELL':
            j = i
            while j < len(orders) and orders[j] and orders[j][0] == 'SELL':
                j += 1
            if 2 <= j - i <= 6:
                blocks.append((i, j))
            i = j
        else:
            i += 1
    if not blocks:
        return action

    alternatives = []
    total = 1
    for i, j in blocks:
        block = orders[i:j]
        seen = set()
        unique = []
        for perm in _r10x_it.permutations(block):
            key = tuple(tuple(o) for o in perm)
            if key not in seen:
                seen.add(key)
                unique.append(perm)
        alternatives.append(unique)
        total *= len(unique)
        if total > _R10X_LIMIT:
            _R10X_REPORT['skipped_budget'] += 1
            return _v44y_reorder(obs, action)

    _R10X_REPORT['calls'] += 1
    if len(blocks) > 1:
        _R10X_REPORT['joint_blocks'] += 1
    stock = {k: max(0, int(v)) for k, v in
             projected_shed(action, FarmView(obs)).items()}
    inv0 = {k: int(v) for k, v in obs['market']['inventory'].items()}
    params = _v44y_params(obs)
    # Crucially, this opponent model stays fixed over the entire search.
    margin = _v44y_factor_margin(orders, inv0, stock, params)
    base = best = margin(orders)
    best_orders = None
    for choice in _r10x_it.product(*alternatives):
        cand = list(orders)
        for (i, j), perm in zip(blocks, choice):
            cand[i:j] = perm
        if cand == orders:
            continue
        _R10X_REPORT['evaluations'] += 1
        value = margin(cand)
        if value > best + 0.5:
            best, best_orders = value, cand
    if best_orders is None:
        return action
    _R10X_REPORT['changed'] += 1
    _R10X_REPORT['model_gain'] += best - base
    return dict(action, market=best_orders)


# V9's final ordering layer remains at the same position in the agent stack.
# Only its search is replaced; the latest idle-worker wrapper remains untouched.
_R10X_ORIGINAL_FINAL_MARKET = round9_final_market_agent


def round9_final_market_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _R9M_REPORT:
            _R9M_REPORT[key] = 0
        for key in _R10X_REPORT:
            _R10X_REPORT[key] = 0 if isinstance(_R10X_REPORT[key], int) else 0.0
    action = _R9M_PARENT(observation, configuration)
    if int(observation['step']) >= 216 and _ig_standard(configuration):
        try:
            result = _r10x_exact_reorder(observation, action)
            _R9M_REPORT['changes'] += int(result != action)
            return result
        except Exception:
            _R10X_REPORT['errors'] += 1
    return action


_R9S_PARENT = round9_final_market_agent


def round10_exact_sell_agent(observation, configuration=None):
    return round9_slack_agent(observation, configuration)


round10_exact_sell_agent.telemetry = _R10X_REPORT
