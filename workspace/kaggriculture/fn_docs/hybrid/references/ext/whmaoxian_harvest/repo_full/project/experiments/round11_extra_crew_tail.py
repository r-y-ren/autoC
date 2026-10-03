
# Round 11 experiment: a separately funded, single-purpose crop-bonus hand.
# Frozen V9 native workers and its existing order sequence are not rewritten.
_R11C_PARENT = round9_slack_agent
_R11C_STATE = {}
_R11C_REPORT = dict(requested_hires=0, confirmed_hires=0, bought_fertilizer=0,
                    pickup_requests=0, water_requests=0, fertilizer_requests=0,
                    confirmed_fertilizer=0, abandoned=0, errors=0)
_R11C_CROPS = {'STRAWBERRY': (10, 2, 4), 'TOMATO': (8, 1, 4)}
_R11C_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))


def _r11c_future_native_hires(obs):
    native = _IMPL.chassis.players.get(int(obs['player']))
    if not native:
        return True
    tape = _IMPL.chassis.routes[native['route']]
    step = int(obs['step'])
    end = min((step // 24 + 1) * 24, 719)
    return any(o and o[0] == 'HIRE' for a in tape[step + 1:end]
               for o in a.get('market', []))


def _r11c_parent_cost(obs, orders):
    farm = obs['farms'][int(obs['player'])]
    hires = int(farm['hires_today'])
    land = len(farm['unlocked_quadrants'])
    cost = 0
    for order in orders:
        if not order:
            continue
        op = order[0]
        if op == 'HIRE':
            cost += _v219_fib(hires)
            hires += 1
        elif op == 'BUY_LAND' and land < 4:
            cost += (1000, 2000, 4000)[land - 1]
            land += 1
        elif len(order) >= 3:
            q = max(0, int(order[2]))
            if op == 'BUY_PRODUCT':
                cost += q * (int(obs['market']['prices'][order[1]]) + 10)
            elif op == 'BUY_SEED':
                cost += q * {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50,
                             'STRAWBERRY': 100, 'MELON': 80}.get(order[1], 0)
            elif op == 'BUY_ANIMAL':
                cost += q * {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}.get(order[1], 0)
    return cost, hires


def _r11c_targets(obs):
    day = int(obs['step']) // 24
    farm = obs['farms'][int(obs['player'])]
    rival = obs['farms'][1-int(obs['player'])]
    market = obs['market']
    rival_supply = {crop: sum(isinstance(t, dict) and t.get('crop') == crop
                              for row in rival['tiles'] for t in row)
                    for crop in _R11C_CROPS}
    out = []
    for y, row in enumerate(farm['tiles']):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get('crop') not in _R11C_CROPS:
                continue
            crop = tile['crop']
            first, interval, count = _R11C_CROPS[crop]
            age = day + 1 - int(tile['planted_day'])
            if age < first or (age-first)%interval or (age-first)//interval >= count:
                continue
            if int(tile.get('fertilized_until_day', -1)) >= day:
                continue
            if int(tile.get('yield_units', 0)) > count - 2:
                continue
            if int(tile.get('consecutive_unwatered', 0)) >= 2:
                continue
            forecast_inventory = int(market['inventory'][crop]) + 12 + 2*rival_supply[crop]
            quote = _r37_market_price(crop, forecast_inventory, market.get('params'))
            out.append((quote, crop, (x, y)))
    out.sort(reverse=True)
    return out


def _r11c_request(obs, action, state):
    step = int(obs['step'])
    day, hour = divmod(step, 24)
    if not 11 <= day <= 27 or hour > 7 or state.get('requested_day') == day:
        return action
    if _r11c_future_native_hires(obs):
        return action
    farm = obs['farms'][int(obs['player'])]
    orders = list(action.get('market') or [])
    if any(o and o[0] == 'HIRE' for o in orders) or len(orders) + 2 > 10:
        return action
    if sum(obs['private']['shed'].values()) > 90:
        return action
    targets = _r11c_targets(obs)
    if not targets:
        return action
    parent_cost, next_hire = _r11c_parent_cost(obs, orders)
    hire = _v219_fib(next_hire)
    fertilizer = int(obs['market']['prices']['FERTILIZER']) + 10
    if int(farm['money']) < parent_cost + hire + fertilizer + 1000:
        return action
    # A native input pickup on the next turn has first claim on the shed.
    native = _IMPL.chassis.players[int(obs['player'])]
    tape = _IMPL.chassis.routes[native['route']]
    following = tape[step+1]
    parent_next_need = sum(int(c[2]) if len(c)>2 else 1
                           for c in [following.get('farmer') or ['PASS'],
                                     *(following.get('hands') or [])]
                           if len(c)>1 and c[:2] == ['PICKUP','FERTILIZER'])
    sold_now = sum(int(o[2]) for o in orders if len(o)>=3 and o[:2]==['SELL','FERTILIZER'])
    bought_now = sum(int(o[2]) for o in orders if len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER'])
    available_next = max(0, int(obs['private']['shed'].get('FERTILIZER',0)) - sold_now) + bought_now + 1
    if available_next <= parent_next_need:
        return action
    chosen = None
    for quote, crop, target in targets:
        if quote < hire + fertilizer + 25:
            continue
        worst_distance = max(abs(x-target[0])+abs(y-target[1]) for x,y in _R11C_ACCESS)
        # One callback to hire, then pickup, walk, WATER if needed, FERTILIZE.
        required = 1 + worst_distance + 1 + (0 if farm['tiles'][target[1]][target[0]].get('watered_today') else 1)
        if required > 23-hour:
            continue
        chosen = target
        break
    if chosen is None:
        return action
    actor = len(farm['hands']) + 1
    state['pending'] = (step, actor, chosen)
    state['requested_day'] = day
    _R11C_REPORT['requested_hires'] += 1
    return dict(action, market=orders+[['BUY_PRODUCT','FERTILIZER',1],['HIRE']])


def _r11c_work(obs, action, state):
    task = state.get('task')
    if not task:
        return action
    actor, target, begun = task
    step = int(obs['step'])
    day, hour = divmod(step, 24)
    farm = obs['farms'][int(obs['player'])]
    if day != begun//24 or actor > len(farm['hands']):
        state['task'] = None
        _R11C_REPORT['abandoned'] += 1
        return action
    x,y = target
    tile = farm['tiles'][y][x]
    if (not isinstance(tile,dict) or tile.get('crop') not in _R11C_CROPS or
            int(tile.get('fertilized_until_day',-1)) >= day):
        state['task'] = None
        _R11C_REPORT['abandoned'] += 1
        return action
    positions = [farm['farmer'], *farm['hands']]
    pos = tuple(positions[actor])
    inv = obs['private']['inventories'][actor]
    if int(inv.get('FERTILIZER',0)) <= 0:
        home = _v219_home(pos)
        command = _v219_walk(pos,home) or (
            ['PICKUP','FERTILIZER',1] if int(obs['private']['shed'].get('FERTILIZER',0))>0
            else ['PASS'])
        if command[0] == 'PICKUP':
            _R11C_REPORT['pickup_requests'] += 1
    else:
        command = _v219_walk(pos,target)
        if command is None:
            if not tile.get('watered_today'):
                command = ['WATER']
                _R11C_REPORT['water_requests'] += 1
            else:
                command = ['FERTILIZE']
                _R11C_REPORT['fertilizer_requests'] += 1
                state['check'] = (step+1,target,day)
                state['task'] = None
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) for c in action.get('hands',[])]
    commands += [['PASS'] for _ in range(len(positions)-len(commands))]
    # Only the hand appended by this overlay can be overridden.
    commands[actor] = command
    return dict(action, farmer=commands[0], hands=commands[1:])


def round11_extra_crew_agent(observation, configuration=None):
    step = int(observation['step'])
    seat = int(observation['player'])
    if step == 0:
        _R11C_STATE[seat] = {'task':None, 'pending':None, 'check':None, 'requested_day':-1}
        for key in _R11C_REPORT:
            _R11C_REPORT[key] = 0
    action = _R11C_PARENT(observation, configuration)
    if not _ig_standard(configuration):
        return action
    state = _R11C_STATE.setdefault(seat, {'task':None,'pending':None,'check':None,'requested_day':-1})
    check = state.pop('check', None)
    if check and step == check[0]:
        x,y = check[1]
        tile = observation['farms'][seat]['tiles'][y][x]
        if isinstance(tile,dict) and int(tile.get('fertilized_until_day',-1)) >= check[2]+2:
            _R11C_REPORT['confirmed_fertilizer'] += 1
    pending = state.pop('pending',None)
    if pending:
        expected_step,actor,target = pending
        if (step==expected_step+1 and
                len(observation['farms'][seat]['hands'])>=actor):
            state['task'] = (actor,target,expected_step)
            _R11C_REPORT['confirmed_hires'] += 1
        else:
            _R11C_REPORT['abandoned'] += 1
    try:
        action = _r11c_work(observation,action,state)
        if not state.get('task'):
            action = _r11c_request(observation,action,state)
        return action
    except Exception:
        _R11C_REPORT['errors'] += 1
        return action


round11_extra_crew_agent.telemetry = _R11C_REPORT
