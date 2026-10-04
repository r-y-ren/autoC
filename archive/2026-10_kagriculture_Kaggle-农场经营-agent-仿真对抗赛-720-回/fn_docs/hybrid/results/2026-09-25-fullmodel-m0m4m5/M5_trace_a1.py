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
    log = {}
    while not state.env.done and t < len(acts):
        obs = state.seats[me].observation
        raw = agent(ta.structify_obs(obs))
        mine = mid.process(raw, obs, t)
        theirs = acts[t][1-me]
        pair = [theirs, theirs]; pair[me] = mine
        twin.step(state, pair)
        obs2 = state.seats[me].observation
        if obs2.hour == 0 and obs2.day in (0,3,5,7,10,15,20,25,29) and obs2.day not in log:
            f = obs2.farms[me]
            herd = {}
            for row in f['tiles']:
                for tl in row:
                    if isinstance(tl, dict) and 'animal' in tl:
                        herd[tl['animal']] = herd.get(tl['animal'],0)+1
            log[obs2.day] = (round(f['money']), dict(herd), len(f['hands']),
                             dict(obs2.private['shed']))
        t += 1
    print(label, 'finals', twin.final_money(state))
    for d in sorted(log):
        print('  d%-2d' % d, 'money=%-8d herd=%-28s hands=%-3d shed=%s' % (log[d][0], log[d][1], log[d][2], {k:v for k,v in log[d][3].items() if v}))

trace({}, 'B')
trace({'A1': True}, 'A1')
