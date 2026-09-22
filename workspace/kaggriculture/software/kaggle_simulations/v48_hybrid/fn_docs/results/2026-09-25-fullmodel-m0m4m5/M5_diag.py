import sys, json, glob, os
sys.path.insert(0, '/tmp/fullmodel/M5')
from _paths import setup, V48H
setup()
from kaggle_simulations.agent.planner import twin
from collections import defaultdict

REPLAY_DIR = V48H + '/fn_docs/results/replays-lead-collapse'
files = sorted(glob.glob(REPLAY_DIR + '/episode-*-replay.json'))
print(len(files), 'defeat replays')

rows = []
for fp in files:
    ep = os.path.basename(fp).split('-')[1]
    replay = json.load(open(fp))
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    # our seat: team renyxin — not in min projection? use info TeamNames
    teams = (replay.get('info') or {}).get('TeamNames') or ['?','?']
    me = 1 if (len(teams)>1 and teams[1]=='renyxin') else 0
    # scan tape for our stream stats
    ext_cum = [0]*30; cows_by_d = [0]*30; wheat_sell_d10 = 0; milk_sell_d10=0; melon_sell_d10=0
    pass_animal = 0; pass_empty = 0; care_miss_days = 0; feed_miss_days = 0
    herd_prev = 0
    day_care = defaultdict(int); day_feed = defaultdict(int)
    for t, pair in enumerate(acts):
        d = t // 24
        a = pair[me]
        mk = a.get('market') or []
        for o in mk:
            if o[0]=='BUY_PRODUCT' and o[1]=='WHEAT': ext_cum[d]+= o[2]
            if o[0]=='BUY_ANIMAL' and o[1]=='COW': cows_by_d[d]+=1
            if d in (10,11) and o[0]=='SELL':
                if o[1]=='WHEAT': wheat_sell_d10+=o[2]
                if o[1]=='MILK': milk_sell_d10+=o[2]
                if o[1]=='MELON': melon_sell_d10+=o[2]
        # unit ops context — need state; do it via stepping (already stepping below)
    # step through and count PASS context at day 3..12 and care/feed misses
    state = twin.build_state_from_replay(replay, 0)
    for t, pair in enumerate(acts):
        d = t // 24
        obs = state.seats[me].observation
        f = obs.farms[me]; pr = obs.private
        a = pair[me]
        if 3 <= d <= 12:
            farmr = f['farmer']
            units = [farmr] + [h for h in f['hands']]
            ops = [a.get('farmer')] + [x for x in (a.get('hands') or [])]
            for pos, op in zip(units, ops):
                if op and op[0]=='PASS':
                    tl = f['tiles'][pos[1]][pos[0]]
                    if isinstance(tl,dict) and 'animal' in tl: pass_animal+=1
                    elif tl is None: pass_empty+=1
        twin.step(state, list(pair))
        # after step: count EOD care/feed coverage: at hour 23 post-step? simpler: sample at next day hour0
        obs2 = state.seats[me].observation
        if obs2.hour == 0 and t+1 < len(acts):
            nd = obs2.day
            if 5 <= nd <= 28:
                herd = 0; uncared_unfed = 0; unfed = 0
                for row in obs2.farms[me]['tiles']:
                    for tl in row:
                        if isinstance(tl,dict) and 'animal' in tl:
                            herd += 1
                day_care[nd-1] = herd  # placeholder
    rows.append(dict(ep=ep, me=me, teams=teams, ext_total=sum(ext_cum),
                     ext_cum_15=sum(ext_cum[:16]), cows_d04=sum(cows_by_d[:5]), cows_d07=sum(cows_by_d[:8]),
                     cows_total=sum(cows_by_d),
                     wheat_sell_d10=wheat_sell_d10, milk_sell_d10=milk_sell_d10, melon_sell_d10=melon_sell_d10,
                     pass_animal=pass_animal, pass_empty=pass_empty))
for r in rows:
    print(r)
