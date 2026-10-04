import sys, json
sys.path.insert(0, '/tmp/fullmodel/M5')
import twin_arms as ta
from kaggle_simulations.agent.planner import twin

games = json.load(open('/tmp/fullmodel/M5/games.json'))
g = [x for x in games if str(x['ep']) == '111286146'][0]
replay = json.load(open(g['path']))
me = g['me']
ext, cows = ta.tape_stats(replay, me)
print('tape_ext cum d5/d15/d29:', ext[5], ext[15], ext[29], 'cows cum d4/d7/d29:', cows[4], cows[7], cows[29])
for arm, flags in ta.ARMS.items():
    finals, counters, steps = ta.run_arm(replay, me, flags, ext, cows)
    print(arm, 'finals:', finals, 'margin:', round(finals[me]-finals[1-me]), counters, 'steps', steps)
