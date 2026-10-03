# Align the inherited public-flow observer with the final executable sell list.
# Rival stock remains an estimate, not access to hidden rival inventories.
_V10_LEDGER_PARENT = v10_pressure_agent
_V10_LEDGER_REPORT = {'corrected_items': 0, 'quantity_difference': 0}

def v10_ledger_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _V10_LEDGER_REPORT:
            _V10_LEDGER_REPORT[key] = 0
    action = _V10_LEDGER_PARENT(observation, configuration)
    state = _OR2_STATE.get(int(observation['player']), {})
    previous = state.get('prev')
    if not previous or previous.get('step') != int(observation['step']):
        return action
    available = projected_shed(action, FarmView(observation))
    own = previous.setdefault('own', {})
    for item in _ADV_ITEMS:
        quantity = sum(max(0, int(o[2])) for o in action.get('market', [])[:10]
                       if len(o) >= 3 and o[:2] == ['SELL', item])
        sold = min(max(0, int(available.get(item, 0))), quantity)
        if sold != int(own.get(item, 0)):
            _V10_LEDGER_REPORT['corrected_items'] += 1
            _V10_LEDGER_REPORT['quantity_difference'] += sold - int(own.get(item, 0))
        own[item] = sold
    return action
v10_ledger_agent.telemetry = _V10_LEDGER_REPORT
agent = v10_ledger_agent
kaggle_submission_agent = v10_ledger_agent
