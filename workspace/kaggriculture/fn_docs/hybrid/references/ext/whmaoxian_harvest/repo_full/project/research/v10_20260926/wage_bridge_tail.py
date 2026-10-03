# Preserve the native early-day crew when one genuinely spare wheat funds it.
_V10_WAGE_PARENT = round9_slack_agent
_V10_WAGE_REPORT = {'bridges': 0, 'errors': 0}

def v10_wage_bridge_agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _V10_WAGE_REPORT['bridges'] = 0
    action = _V10_WAGE_PARENT(observation, configuration)
    if step >= 72 or step % 24 > 1:
        return action
    orders = [list(o) for o in action.get('market', []) if o]
    if not orders or len(orders) >= 10 or any(o != ['HIRE'] for o in orders):
        return action
    farm = observation['farms'][int(observation['player'])]
    private = observation['private']; cash = float(farm['money'])
    cost = sum(_fib(int(farm['hires_today']) + i) for i in range(len(orders)))
    if cash >= cost or cash + float(observation['market']['prices']['WHEAT']) < cost:
        return action
    feed = sum(1 for row in farm['tiles'] for tile in row
               if isinstance(tile, dict) and tile.get('animal') and not tile.get('fed_today'))
    wheat = int(private['shed'].get('WHEAT', 0)) + sum(int(inv.get('WHEAT', 0)) for inv in private['inventories'])
    available = projected_shed(action, FarmView(observation))
    if wheat <= feed or int(available.get('WHEAT', 0)) < 1:
        return action
    _V10_WAGE_REPORT['bridges'] += 1
    return dict(action, market=[['SELL', 'WHEAT', 1]] + orders)
v10_wage_bridge_agent.telemetry = _V10_WAGE_REPORT
agent = v10_wage_bridge_agent
