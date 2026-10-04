
# Round 11 experiment: use an otherwise idle native worker for one guaranteed
# imminent ongoing-crop fertilizer bonus. Appended to an unchanged V9 copy.
_R11F_PARENT = round9_slack_agent
_R11F_STATE = {}
_R11F_REPORT = dict(tasks_started=0, pickups=0, fertilize_requests=0,
                    confirmed_fertilized=0, abandoned=0, errors=0)
_R11F_CROPS = {'STRAWBERRY': (10, 2, 4), 'TOMATO': (8, 1, 4)}
_R11F_MOVES = {'NORTH', 'SOUTH', 'EAST', 'WEST'}


def _r11f_home(pos):
    return _v219_home(pos)


def _r11f_ready(obs):
    """Yield +1 at this day's official refresh, with no yield-cap waste."""
    farm = obs['farms'][int(obs['player'])]
    day = int(obs['step']) // 24
    market = obs['market']
    rival = obs['farms'][1 - int(obs['player'])]
    rival_supply = {crop: sum(isinstance(t, dict) and t.get('crop') == crop
                              for row in rival['tiles'] for t in row)
                    for crop in _R11F_CROPS}
    fert_quote = int(market['prices']['FERTILIZER'])
    result = []
    for y, row in enumerate(farm['tiles']):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            crop = tile.get('crop')
            if crop not in _R11F_CROPS or not tile.get('watered_today'):
                continue
            first, interval, cap = _R11F_CROPS[crop]
            age = day + 1 - int(tile['planted_day'])
            if age < first or (age - first) % interval != 0:
                continue
            if (age - first) // interval >= cap:
                continue
            if int(tile.get('fertilized_until_day', -1)) >= day:
                continue
            if int(tile.get('yield_units', 0)) > cap - 2:
                continue
            inventory = int(market['inventory'][crop])
            quote = _r37_market_price(crop, inventory + 12 + 2 * rival_supply[crop],
                                      market.get('params'))
            if quote < fert_quote + 25:
                continue
            result.append((quote - fert_quote, crop, (x, y)))
    result.sort(reverse=True)
    return result


def _r11f_future_input_reserved(obs, native):
    seat = int(obs['player'])
    tape = _IMPL.chassis.routes[native['route']]
    step = int(obs['step'])
    end = min((step // 24 + 1) * 24, 719)
    for future in tape[step + 1:end]:
        if any(len(c) > 1 and c[:2] == ['PICKUP', 'FERTILIZER']
               for c in [future.get('farmer') or ['PASS'], *(future.get('hands') or [])]):
            return True
    return False


def _r11f_apply(obs, action, state):
    step = int(obs['step'])
    day, hour = divmod(step, 24)
    if day < 11 or day >= 29 or hour > 20:
        return action
    seat = int(obs['player'])
    farm = obs['farms'][seat]
    private = obs['private']
    native = _IMPL.chassis.players.get(seat)
    if not native:
        return action
    _, busy = _r9s_reservations(obs, native)
    reserved_roles = set()
    for state_map in (_V219_STATES, _V233_STATES):
        reserved_roles.update(state_map.get(seat, {}).get('workers', {}))
    commands = [list(action.get('farmer') or ['PASS'])] + [list(c) for c in action.get('hands', [])]
    commands += [['PASS'] for _ in range(len(farm['hands']) + 1 - len(commands))]
    positions = [farm['farmer'], *farm['hands']]
    ready = _r11f_ready(obs)
    eligible = {target for _, _, target in ready}
    task = state.get('task')
    if task:
        actor, target, started = task
        if (started // 24 != day or target not in eligible or actor >= len(positions)
                or actor in busy or actor in reserved_roles or commands[actor] != ['PASS']):
            state['task'] = None
            _R11F_REPORT['abandoned'] += 1
        else:
            pos = tuple(positions[actor])
            inv = private['inventories'][actor]
            if inv.get('FERTILIZER', 0):
                command = _v219_walk(pos, target) or ['FERTILIZE']
                commands[actor] = command
                if command == ['FERTILIZE']:
                    state['check'] = (step + 1, target)
                    state['task'] = None
                    _R11F_REPORT['fertilize_requests'] += 1
                return dict(action, farmer=commands[0], hands=commands[1:])
            can_pick = (int(private['shed'].get('FERTILIZER', 0)) >= 2 and
                        not _r11f_future_input_reserved(obs, native) and
                        not any(len(o) > 1 and o[:2] == ['SELL', 'FERTILIZER']
                                for o in action.get('market', []) if o))
            if can_pick:
                home = _r11f_home(pos)
                command = _v219_walk(pos, home) or ['PICKUP', 'FERTILIZER', 1]
                commands[actor] = command
                if command[0] == 'PICKUP':
                    _R11F_REPORT['pickups'] += 1
                return dict(action, farmer=commands[0], hands=commands[1:])
            # Parent resource obligations take precedence over this detour.
            state['task'] = None
            _R11F_REPORT['abandoned'] += 1
    if not ready:
        return action
    fetch_allowed = (
        int(private['shed'].get('FERTILIZER', 0)) >= 2 and
        not _r11f_future_input_reserved(obs, native) and
        not any(len(o) > 1 and o[:2] == ['SELL', 'FERTILIZER']
                for o in action.get('market', []) if o)
    )
    best = None
    for actor in range(1, len(positions)):
        if actor in busy or actor in reserved_roles or commands[actor] != ['PASS']:
            continue
        inv = private['inventories'][actor]
        carried = int(inv.get('FERTILIZER', 0))
        if carried <= 0 and not fetch_allowed:
            continue
        pos = tuple(positions[actor])
        for gain, crop, target in ready:
            if carried:
                turns = abs(pos[0]-target[0]) + abs(pos[1]-target[1]) + 1
            else:
                home = _r11f_home(pos)
                turns = (abs(pos[0]-home[0]) + abs(pos[1]-home[1]) + 1
                         + abs(home[0]-target[0]) + abs(home[1]-target[1]) + 1)
            if turns > 23-hour:
                continue
            score = (gain / turns, gain, -turns, -actor, target)
            if best is None or score > best[0]:
                best = (score, actor, target, carried)
    if best is None:
        return action
    _, actor, target, carried = best
    pos = tuple(positions[actor])
    if carried:
        command = _v219_walk(pos, target) or ['FERTILIZE']
    else:
        home = _r11f_home(pos)
        command = _v219_walk(pos, home) or ['PICKUP', 'FERTILIZER', 1]
        if command[0] == 'PICKUP':
            _R11F_REPORT['pickups'] += 1
    commands[actor] = command
    _R11F_REPORT['tasks_started'] += 1
    if command == ['FERTILIZE']:
        state['check'] = (step + 1, target)
        _R11F_REPORT['fertilize_requests'] += 1
    else:
        state['task'] = (actor, target, step)
    return dict(action, farmer=commands[0], hands=commands[1:])


def round11_fertilizer_overlay_agent(observation, configuration=None):
    step = int(observation['step'])
    seat = int(observation['player'])
    if step == 0:
        _R11F_STATE[seat] = {'task': None, 'check': None}
        for key in _R11F_REPORT:
            _R11F_REPORT[key] = 0
    action = _R11F_PARENT(observation, configuration)
    if not _ig_standard(configuration):
        return action
    state = _R11F_STATE.setdefault(seat, {'task': None, 'check': None})
    check = state.pop('check', None)
    if check and step == check[0]:
        x, y = check[1]
        tile = observation['farms'][seat]['tiles'][y][x]
        if isinstance(tile, dict) and int(tile.get('fertilized_until_day', -1)) >= step // 24:
            _R11F_REPORT['confirmed_fertilized'] += 1
    try:
        return _r11f_apply(observation, action, state)
    except Exception:
        _R11F_REPORT['errors'] += 1
        return action


round11_fertilizer_overlay_agent.telemetry = _R11F_REPORT
