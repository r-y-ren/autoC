
_EXP303_RESOURCE_RUN = None
_EXP303_RESOURCE_PRICES = None
_EXP303_RESOURCES = None

def _exp303_resources(run, prices):
    global _EXP303_RESOURCE_RUN, _EXP303_RESOURCE_PRICES, _EXP303_RESOURCES
    key = tuple(prices.items())
    if _EXP303_RESOURCE_RUN is run and _EXP303_RESOURCE_PRICES == key:
        return _EXP303_RESOURCES
    snapshots = []
    for offset in range(len(run['rows'])):
        farm, private = run['states'][offset]
        entries = []
        for y, row in enumerate(farm['tiles']):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict): continue
                harvest, fertilizer = None, None
                if tile.get('yield_units',0) > 0:
                    item = tile.get('crop') if tile.get('kind') == 'PLANT' else ANIMALS.get(tile.get('animal'),{}).get('product')
                    mature = item and ('animal' in tile or (START+offset)//24-tile['planted_day'] >= CROPS[item]['first_yield_day'])
                    if mature: harvest = prices[item]*tile['yield_units']
                if tile.get('fertilizer_available') and 'animal' in tile: fertilizer = prices['FERTILIZER']
                if harvest is not None or fertilizer is not None: entries.append(((x,y),harvest,fertilizer))
        snapshots.append(entries)
    _EXP303_RESOURCE_RUN, _EXP303_RESOURCE_PRICES, _EXP303_RESOURCES = run, key, snapshots
    return snapshots

def _proposals(run, actor, prices, max_per_actor):
    """One/two resource bundles plus direct carry closure, replacing a baseline suffix."""
    owners = {}
    for event in run['events']:
        if 'acquired' in event:
            owners.setdefault((tuple(event['xy']), event['op']), set()).add(event['actor'])
    proposals = []
    seen = set()
    horizon = len(run['rows'])
    for offset in range(horizon):
        farm, private = run['states'][offset]
        pos = tuple(farm['farmer'] if actor == 0 else farm['hands'][actor - 1])
        inventory = private['inventories'][actor]
        carried = sum((prices.get(item, 0) * count for item, count in inventory.items()))
        prefix_deposits = run['rows'][offset - 1]['deposited_by_actor'][actor] if offset else {}
        future_deposits = run['rows'][-1]['deposited_by_actor'][actor]
        obligation = sum((prices.get(item, 0) * (count - prefix_deposits.get(item, 0)) for item, count in future_deposits.items()))
        bundles = []
        for xy, harvest, fertilizer in _exp303_resources(run, prices)[offset]:
            operations, value = [], 0
            if harvest is not None and (not owners.get((xy, 'HARVEST'), set()) - {actor}):
                operations.append(['HARVEST']); value += harvest
            if fertilizer is not None and (not owners.get((xy, 'COLLECT_FERTILIZER'), set()) - {actor}):
                operations.append(['COLLECT_FERTILIZER']); value += fertilizer
            if operations:
                distance = abs(pos[0]-xy[0])+abs(pos[1]-xy[1])+len(operations)+_R150_HOME_DISTANCE[xy]
                if distance <= horizon-offset: bundles.append((xy,operations,value,distance))
        bundles.sort(key=lambda b: (-b[2] / b[3], -b[2], b[0]))
        variants = [([], carried)] if carried else []
        for xy, ops, value, _ in bundles[:6]:
            variants.append(([(xy, ops)], carried + value))
        for first in bundles[:3]:
            for second in bundles[:3]:
                if first[0] != second[0]:
                    variants.append(([(first[0], first[1]), (second[0], second[1])], carried + first[2] + second[2]))
        for stops, value in variants:
            route, cursor = ([], pos)
            for xy, ops in stops:
                route += _walk(cursor, xy) + ops
                cursor = xy
            route += _return(cursor)
            if len(route) > horizon - offset:
                continue
            route += [['PASS']] * (horizon - offset - len(route))
            key = (offset, tuple((tuple(c) for c in route)))
            if key not in seen:
                seen.add(key)
                proposals.append((value - obligation, offset, route, len(stops)))
    proposals.sort(key=lambda p: (-p[0], p[1], p[2]))
    direct = [p for p in proposals if p[3] == 0 and p[0] > 0][:2]
    chosen = direct + [p for p in proposals if p not in direct]
    return chosen[:max_per_actor]