"""Freeze study-only public streams; never use held-out episodes in this build."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'research/top10/study_market_streams.json').read_text())
compact = [{k: r[k] for k in ('shops', 'events', 'profiles')} for r in data]
extension = '''
# Experimental extension, 2026-09-21: public top-ten sale pattern matching.
# Original Apache-2.0 attribution above is retained. Study provenance is external.
# Decisions depend only on visible current farms and previously observed sales.
import json as _t10_json
_T10_ROWS = _t10_json.loads(DATA_LITERAL)
for _t10_row in _T10_ROWS:
    _t10_row['ev'] = {(t, i): q for t, i, q in _t10_row.pop('events')}
_T10_PARENT_FORECAST = _v92_p_forecast
_T10_PARENT_AGENT = _e363_agent
_T10_STATS = {'top10_forecasts': 0}

def _t10_score(ev, seen, step):
    lo = step - 240
    m = f = 0
    for t, i in ev:
        if lo <= t < step - 1:
            if any((t + d, i) in seen for d in (-1, 0, 1)):
                m += 1
            else:
                f += 1
    miss = sum(1 for t, i in seen if lo <= t < step - 1
               and not any((t + d, i) in ev for d in (-1, 0, 1)))
    return m - .5 * f - .5 * miss, m, f

def _v92_p_forecast(obs, st):
    base = _T10_PARENT_FORECAST(obs, st)
    step = int(obs['step'])
    if not 240 <= step < 680:
        return base
    seen = st['obs']
    best_score = max((_t10_score(e, seen, step)[0] for e in base), default=-1000) + 2
    best = None
    current = {}
    for row in obs['farms'][1 - int(obs['player'])]['tiles']:
        for tile in row:
            item = tile.get('animal') or tile.get('crop')
            if item:
                current[item] = current.get(item, 0) + 1
    shops = list(obs['town']['unlocked_shops'][:2])
    for donor in _T10_ROWS:
        if donor['shops'] != shops:
            continue
        profile = donor['profiles'][str(step // 24 * 24)]
        distance = sum(abs(current.get(k, 0) - profile.get(k, 0)) for k in current.keys() | profile.keys())
        if distance > .35 * max(1, sum(current.values()), sum(profile.values())):
            continue
        score, matches, false = _t10_score(donor['ev'], seen, step)
        if matches >= 6 and matches >= .8 * (matches + false) and score > best_score:
            best, best_score = donor['ev'], score
    if best is not None:
        _T10_STATS['top10_forecasts'] += 1
        return [best]
    return base

def submission_v6_agent(obs, config=None):
    if int(obs.get('step', 0)) == 0:
        _T10_STATS['top10_forecasts'] = 0
    return _T10_PARENT_AGENT(obs, config)

submission_v6_agent.telemetry = _e350_collections.ChainMap(_T10_STATS, _T10_PARENT_AGENT.telemetry)
agent = submission_v6_agent
'''.replace('DATA_LITERAL', repr(json.dumps(compact, separators=(',', ':'))))
(ROOT / 'experiments/v6_top10_market.py').write_bytes((ROOT / 'external/ahmed_v53.py').read_bytes() + extension.encode())
print('Built study-only candidate')
