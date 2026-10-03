# Replay-derived production; sale quantities come from the live own warehouse.
_V10_CASH_ITEMS = ('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
_V10_CASH_REPORT = {'sale_turns': 0, 'requested_units': 0}

def v10_route_cash_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _V10_CASH_REPORT:
            _V10_CASH_REPORT[key] = 0
    action = _V10_EXECUTOR(observation, configuration)
    chassis = _V10_EXECUTOR.chassis
    view = _View(observation, int(observation['player']), chassis.cfg)
    stock = chassis._projected_shed(action, view)
    preserved = [list(o) for o in action.get('market', [])
                 if not (len(o) >= 3 and o[0] == 'SELL' and o[1] in _V10_CASH_ITEMS)]
    capacity = max(0, 10 - len(preserved))
    available = [(item, int(stock.get(item, 0))) for item in _V10_CASH_ITEMS
                 if int(stock.get(item, 0)) > 0]
    available.sort(key=lambda pair: -pair[1] * int(view.prices.get(pair[0], 0)))
    sales = [['SELL', item, quantity] for item, quantity in available[:capacity]]
    if sales:
        _V10_CASH_REPORT['sale_turns'] += 1
        _V10_CASH_REPORT['requested_units'] += sum(o[2] for o in sales)
    action['market'] = sales + preserved
    return action
v10_route_cash_agent.telemetry = _V10_CASH_REPORT
agent = v10_route_cash_agent
