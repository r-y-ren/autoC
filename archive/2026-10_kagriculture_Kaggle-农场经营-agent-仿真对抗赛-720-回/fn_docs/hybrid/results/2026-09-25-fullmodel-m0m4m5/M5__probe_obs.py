import sys, json
sys.path.insert(0, '/tmp/fullmodel/M5')
from _paths import setup, V48H, SOFTWARE
setup()
from kaggle_simulations.agent.planner import twin
p = V48H + '/fn_docs/results/replays-lead-collapse/episode-111286146-replay.json'
replay = json.load(open(p))
state = twin.build_state_from_replay(replay, 0)
acts = twin.replay_transition_actions(replay)
for n in range(300):
    twin.step(state, list(acts[n]))
obs = state.seats[1].observation
print('obs attrs:', [a for a in dir(obs) if not a.startswith('_')])
f = obs.farms[1]
print('farm type:', type(f))
tiles = f['tiles'] if isinstance(f, dict) else f.tiles
fp = fa = None
for y,row in enumerate(tiles):
    for x,t in enumerate(row):
        if isinstance(t, dict):
            if t.get('kind')=='PLANT' and fp is None: fp=(y,x,dict(t))
            if 'animal' in t and fa is None: fa=(y,x,dict(t))
print('PLANT tile:', fp)
print('ANIMAL tile:', fa)
pr = obs.private
print('private type:', type(pr))
if isinstance(pr, dict):
    print('shed:', dict(pr['shed']), 'inv0:', dict(pr['inventories'][0]), 'seeds:', dict(pr['seeds']))
farmer = f['farmer'] if isinstance(f, dict) else f.farmer
print('farmer:', farmer, 'money:', f['money'] if isinstance(f,dict) else f.money, 'day/hour:', obs.day, obs.hour)
