
# Round 11 experiment: shop-backed, physically serviced sheep expansion.
# This file is appended to a byte-for-byte copy of frozen V9 by the builder.
# It deliberately uses only visible shops, cash, inventory, farms and the
# parent's already chosen orders. It never predicts a future shop draw.
_R11E_PARENT = round9_slack_agent
_R11E_STATE = {}
_R11E_REPORT = dict(purchases=0, land_confirmed=0, sheep_placed=0,
                    crew_hired=0, feed_requests=0, care_requests=0,
                    wool_harvest_requests=0, fertilizer_collect_requests=0,
                    sale_units=0, budget_declines=0, hire_shortfalls=0,
                    order_declines=0, errors=0)
_R11E_SITES = ((5, 5), (5, 6), (6, 5))
_R11E_HOME = ((4, 4), (5, 4), (4, 5), (5, 5))


def _r11e_walk(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ['EAST' if x < tx else 'WEST']
    if y != ty:
        return ['SOUTH' if y < ty else 'NORTH']
    return None


def _r11e_home(pos):
    return min(_R11E_HOME, key=lambda p: (abs(pos[0] - p[0]) + abs(pos[1] - p[1]), _R11E_HOME.index(p)))


def _r11e_parent_cost(obs, orders):
    farm = obs['farms'][int(obs['player'])]
    hires = int(farm['hires_today'])
    lands = len(farm['unlocked_quadrants'])
    cost = 0
    seeds = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50,
             'STRAWBERRY': 100, 'MELON': 80}
    animals = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
    for order in orders:
        if not order:
            continue
        op = order[0]
        if op == 'HIRE':
            cost += _v219_fib(hires)
            hires += 1
        elif op == 'BUY_LAND' and lands < 4:
            cost += (1000, 2000, 4000)[lands - 1]
            lands += 1
        elif len(order) >= 3:
            quantity = max(0, int(order[2]))
            if op == 'BUY_SEED':
                cost += quantity * seeds.get(order[1], 0)
            elif op == 'BUY_ANIMAL':
                cost += quantity * animals.get(order[1], 0)
            elif op == 'BUY_PRODUCT':
                cost += quantity * (int(obs['market']['prices'][order[1]]) + 10)
    return cost, hires


def _r11e_no_future_native_hires(obs):
    seat = int(obs['player'])
    native = _IMPL.chassis.players.get(seat)
    if not native:
        return False
    tape = _IMPL.chassis.routes[native['route']]
    end = min((int(obs['step']) // 24 + 1) * 24, 719)
    return not any(order and order[0] == 'HIRE'
                   for step in range(int(obs['step']) + 1, end)
                   for order in tape[step].get('market', []))


def _r11e_request(obs, action, state):
    step = int(obs['step'])
    day, hour = divmod(step, 24)
    if day < 11 or day > 29 or hour > 5 or state.get('requested_day') == day:
        return action
    farm = obs['farms'][int(obs['player'])]
    private = obs['private']
    orders = list(action.get('market') or [])
    if any(order and order[0] == 'HIRE' for order in orders) or not _r11e_no_future_native_hires(obs):
        return action
    if not _ig_standard(None):
        return action
    first = not state.get('committed')
    if first:
        # Observe the already executed native third-land purchase. A fourth
        # quadrant alone is never bought: three animals and a crew are funded.
        if step != 266 or set(farm['unlocked_quadrants']) != {'NW', 'NE', 'SW'}:
            return action
        if 'YARN_STORE' not in obs['town']['unlocked_shops']:
            return action
        if int(obs['market']['prices']['WOOL']) < 180:
            return action
        if sum(private['shed'].values()) > 85:
            return action
        extra = [['BUY_LAND'], ['BUY_ANIMAL', 'SHEEP', 3], ['HIRE']]
    else:
        if day == 11 or 'SE' not in farm['unlocked_quadrants']:
            return action
        alive = sum(isinstance(farm['tiles'][y][x], dict) and
                    farm['tiles'][y][x].get('animal') == 'SHEEP'
                    for x, y in _R11E_SITES)
        if alive <= 0:
            return action
        # Unit actions precede the market. Buy the supplemental feed at hire
        # time, then pick it up on the following callback.
        extra = ([['BUY_PRODUCT', 'WHEAT', alive]] if day < 29 else []) + [['HIRE']]
    if len(orders) + len(extra) > 10:
        _R11E_REPORT['order_declines'] += 1
        return action
    parent_cost, next_hire = _r11e_parent_cost(obs, orders)
    extra_cost = (5500 if first else 0) + _v219_fib(next_hire)
    if not first and day < 29:
        extra_cost += alive * (int(obs['market']['prices']['WHEAT']) + 10)
    if int(farm['money']) < parent_cost + extra_cost + (3000 if first else 1000):
        _R11E_REPORT['budget_declines'] += 1
        return action
    actor = len(farm['hands']) + 1 + sum(order == ['HIRE'] for order in orders)
    state['pending'] = (step, actor, first)
    state['requested_day'] = day
    if first:
        state['committed'] = True
        _R11E_REPORT['purchases'] += 1
    return dict(action, market=orders + extra)


def _r11e_worker(obs, actor, first):
    step = int(obs['step'])
    day, hour = divmod(step, 24)
    farm = obs['farms'][int(obs['player'])]
    private = obs['private']
    pos = tuple(([farm['farmer']] + farm['hands'])[actor])
    inv = private['inventories'][actor]
    shed = private['shed']
    if first:
        existing = sum(isinstance(farm['tiles'][y][x], dict) and
                       farm['tiles'][y][x].get('animal') == 'SHEEP'
                       for x, y in _R11E_SITES)
        if existing == 3:
            return ['PASS']
        if int(inv.get('SHEEP', 0)) == 0:
            home = _r11e_home(pos)
            return _r11e_walk(pos, home) or (
                ['PICKUP', 'SHEEP', min(3 - existing, int(shed.get('SHEEP', 0)))]
                if int(shed.get('SHEEP', 0)) > 0 else ['PASS'])
        for x, y in _R11E_SITES:
            tile = farm['tiles'][y][x]
            if tile is None or (isinstance(tile, dict) and tile.get('kind') == 'PASTURE'
                                and not tile.get('animal')):
                return _r11e_walk(pos, (x, y)) or (
                    ['BUILD_PASTURE'] if tile is None else ['PLACE', 'SHEEP', 1])
        return ['PASS']
    sites = [(x, y, farm['tiles'][y][x]) for x, y in _R11E_SITES]
    alive = [(x, y, tile) for x, y, tile in sites
             if isinstance(tile, dict) and tile.get('animal') == 'SHEEP']
    if day < 29:
        unfed = [(x, y) for x, y, tile in alive if not tile.get('fed_today')]
        if unfed and int(inv.get('WHEAT', 0)) <= 0:
            home = _r11e_home(pos)
            return _r11e_walk(pos, home) or (
                ['PICKUP', 'WHEAT', min(len(unfed), int(shed.get('WHEAT', 0)))]
                if int(shed.get('WHEAT', 0)) > 0 else ['PASS'])
        if unfed:
            target = min(unfed, key=lambda p: abs(pos[0]-p[0])+abs(pos[1]-p[1]))
            command = _r11e_walk(pos, target) or ['FEED']
            if command == ['FEED']:
                _R11E_REPORT['feed_requests'] += 1
            return command
        uncared = [(x, y) for x, y, tile in alive
                   if tile.get('fed_today') and not tile.get('cared_today')]
        if uncared:
            target = min(uncared, key=lambda p: abs(pos[0]-p[0])+abs(pos[1]-p[1]))
            command = _r11e_walk(pos, target) or ['CARE']
            if command == ['CARE']:
                _R11E_REPORT['care_requests'] += 1
            return command
    cargo = int(inv.get('WOOL', 0)) + int(inv.get('FERTILIZER', 0))
    home = _r11e_home(pos)
    if cargo and (hour >= 18 or cargo >= 8):
        return _r11e_walk(pos, home) or (
            ['PLACE', 'WOOL', int(inv['WOOL'])] if inv.get('WOOL', 0)
            else ['PLACE', 'FERTILIZER', int(inv['FERTILIZER'])])
    if hour < 18:
        wool = [(x, y) for x, y, tile in alive if int(tile.get('yield_units', 0)) > 0]
        if wool:
            target = min(wool, key=lambda p: abs(pos[0]-p[0])+abs(pos[1]-p[1]))
            command = _r11e_walk(pos, target) or ['HARVEST']
            if command == ['HARVEST']:
                _R11E_REPORT['wool_harvest_requests'] += 1
            return command
        # Do not fill a nearly saturated shared shed with marginal fertilizer.
        if sum(shed.values()) < 90:
            fertilizer = [(x, y) for x, y, tile in alive if tile.get('fertilizer_available')]
            if fertilizer:
                target = min(fertilizer, key=lambda p: abs(pos[0]-p[0])+abs(pos[1]-p[1]))
                command = _r11e_walk(pos, target) or ['COLLECT_FERTILIZER']
                if command == ['COLLECT_FERTILIZER']:
                    _R11E_REPORT['fertilizer_collect_requests'] += 1
                return command
    if cargo:
        return _r11e_walk(pos, home) or (
            ['PLACE', 'WOOL', int(inv['WOOL'])] if inv.get('WOOL', 0)
            else ['PLACE', 'FERTILIZER', int(inv['FERTILIZER'])])
    return ['PASS']


def _r11e_apply(obs, action, state):
    step = int(obs['step'])
    day = step // 24
    farm = obs['farms'][int(obs['player'])]
    if state.get('day') != day:
        state['day'] = day
        state['worker'] = None
    pending = state.pop('pending', None)
    if pending is not None:
        requested_step, actor, first = pending
        if step == requested_step + 1 and len(farm['hands']) >= actor and (
                not first or 'SE' in farm['unlocked_quadrants']):
            state['worker'] = (actor, first)
            _R11E_REPORT['crew_hired'] += 1
            if first:
                _R11E_REPORT['land_confirmed'] += 1
        else:
            _R11E_REPORT['hire_shortfalls'] += 1
    action = _r11e_request(obs, action, state)
    worker = state.get('worker')
    if worker is None:
        return action
    actor, first = worker
    if actor > len(farm['hands']):
        return action
    old_sites = sum(isinstance(farm['tiles'][y][x], dict) and
                    farm['tiles'][y][x].get('animal') == 'SHEEP'
                    for x, y in _R11E_SITES)
    if old_sites > state.get('seen_sheep', 0):
        _R11E_REPORT['sheep_placed'] += old_sites - state.get('seen_sheep', 0)
        state['seen_sheep'] = old_sites
    commands = [list(action.get('farmer') or ['PASS'])] + [list(x) for x in action.get('hands', [])]
    commands += [['PASS'] for _ in range(len(farm['hands']) + 1 - len(commands))]
    commands[actor] = _r11e_worker(obs, actor, first)
    revised = dict(action, farmer=commands[0], hands=commands[1:])
    # Physical PLACE happens before market. Only sell what the revised action
    # projects into the shed; keep all native buy/hire orders in their positions.
    if commands[actor][0] == 'PLACE' and commands[actor][1] in ('WOOL', 'FERTILIZER'):
        item = commands[actor][1]
        before = int(obs['private']['shed'].get(item, 0))
        projected = projected_shed(revised, FarmView(obs))
        after = int(projected.get(item, 0))
        added = max(0, after - before)
        orders = [list(o) for o in revised.get('market', [])]
        planned = sum(int(o[2]) for o in orders if len(o) >= 3 and o[:2] == ['SELL', item])
        extra = min(added, max(0, after - planned))
        if extra:
            old = next((o for o in orders if len(o) >= 3 and o[:2] == ['SELL', item]), None)
            if old is not None:
                old[2] += extra
            elif len(orders) < 10:
                orders.append(['SELL', item, extra])
            else:
                extra = 0
            if extra:
                revised['market'] = orders
                _R11E_REPORT['sale_units'] += extra
    return revised


def round11_early_expansion_agent(observation, configuration=None):
    step = int(observation['step'])
    seat = int(observation['player'])
    if step == 0:
        _R11E_STATE[seat] = {'committed': False, 'day': -1, 'requested_day': -1,
                             'worker': None, 'seen_sheep': 0}
        for key in _R11E_REPORT:
            _R11E_REPORT[key] = 0
    action = _R11E_PARENT(observation, configuration)
    if not _ig_standard(configuration):
        return action
    state = _R11E_STATE.setdefault(seat, {'committed': False, 'day': -1,
                                           'requested_day': -1, 'worker': None,
                                           'seen_sheep': 0})
    try:
        return _r11e_apply(observation, action, state)
    except Exception:
        _R11E_REPORT['errors'] += 1
        return action


round11_early_expansion_agent.telemetry = _R11E_REPORT
