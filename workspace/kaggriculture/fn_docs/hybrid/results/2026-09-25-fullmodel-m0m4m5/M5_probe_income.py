import sys, json
sys.path.insert(0, '/tmp/fullmodel/M5')
import twin_arms as ta
from kaggle_simulations.agent.planner import twin

games = json.load(open('/tmp/fullmodel/M5/games.json'))
g = [x for x in games if str(x['ep']) == '111286146'][0]
replay = json.load(open(g['path']))
me = g['me']
ext, cows = ta.tape_stats(replay, me)

def trace(flags, label):
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    agent = ta.fresh_agent()
    mid = ta.Mid(flags, ext, cows)
    t = 0
    day_inc = [0.0]*30; day_sells = [dict() for _ in range(30)]
    prev_money = 3000.0
    while not state.env.done and t < len(acts):
        obs = state.seats[me].observation
        raw = agent(ta.structify_obs(obs))
        mine = mid.process(raw, obs, t)
        theirs = acts[t][1-me]
        pair = [theirs, theirs]; pair[me] = mine
        # record our sell orders
        d = t // 24
        for o in (mine.get('market') or []):
            if o[0] == 'SELL':
                day_sells[d][o[1]] = day_sells[d].get(o[1], 0) + o[2]
        twin.step(state, pair)
        m = state.seats[me].observation.farms[me]['money']
        day_inc[d] += m - prev_money; prev_money = m
        t += 1
    print(label, 'final', twin.final_money(state)[me])
    for d in range(19, 30):
        print('  d%d inc=%8.0f sells=%s' % (d, day_inc[d], day_sells[d]))

trace({}, 'B')
trace({'A1': True}, 'A1')
