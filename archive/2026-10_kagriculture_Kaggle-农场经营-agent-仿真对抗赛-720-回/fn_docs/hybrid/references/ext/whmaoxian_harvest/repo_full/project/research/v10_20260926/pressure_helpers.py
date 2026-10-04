# Public-state market-pressure experiment. No network or private rival input.
_V10_ADV_HORIZON = 12
_V10_ADV_THRESHOLD = 4
_V10_ADV_REPORT = {'pressure_plans': 0, 'errors': 0}

def _v10_pressure_plan(obs, plan, protected):
    step = int(obs['step']); seat = int(obs['player'])
    stock = _OR2_STATE.get(seat, {}).get('stock', {})
    shops = obs.get('town', {}).get('unlocked_shops', [])
    result = []
    for t, item, quantity in plan:
        if t - step <= _ADV_LOOK and item != protected:
            result.append((t, item, quantity)); continue
        if step < 216:
            continue
        per_tick = 0
        for shop in shops:
            goods = _OR2_SHOPS.get(shop, ())
            if item in goods:
                per_tick += 2 if len(goods) == 1 else 1
        demand = per_tick * sum(x % 4 == 0 for x in range(step, t))
        demand += sum(x % 24 == 0 for x in range(step, t))
        if int(stock.get(item, 0)) >= max(_V10_ADV_THRESHOLD, 2 * demand):
            result.append((t, item, quantity))
            _V10_ADV_REPORT['pressure_plans'] += 1
    return result
