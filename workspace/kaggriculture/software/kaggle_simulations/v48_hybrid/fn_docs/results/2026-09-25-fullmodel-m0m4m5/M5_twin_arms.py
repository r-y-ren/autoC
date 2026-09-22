#!/usr/bin/env python3
"""M5 twin-arm runner: strategy-adjustment verdict experiments.

Design: our seat runs the real v48_derivative agent (bit-identical tape regenerator,
verified), wrapped in a middleware that post-processes its BUY/HIRE/SELL unit-ops
per adjustment hypothesis (A1/A2/A3/A4/combo). Opponent seat replays the tape
verbatim. Baseline arm must reproduce tape rewards exactly (validity gate).
"""
import sys, os, json, glob, copy, time
sys.path.insert(0, '/tmp/fullmodel/M5')
from _paths import setup, V48H, SOFTWARE
setup()
from kaggle_simulations.agent.planner import twin
from kgenv.arena import load_submission_agent

AGENT_PATH = os.path.join(SOFTWARE, 'kaggle_simulations', 'v48_derivative', 'main.py')
REPLAY_DIR = os.path.join(V48H, 'fn_docs', 'results', 'replays-lead-collapse')
HOURS = 24

class ObsStruct(dict):
    def __getattr__(self, name):
        try: return self[name]
        except KeyError as e: raise AttributeError(name) from e

def structify_obs(obs):
    keys = ("farms","market","town","day","hour","step","player","private","remainingOverageTime")
    out = ObsStruct()
    for k in keys:
        v = getattr(obs, k, None)
        if v is not None or hasattr(obs, k): out[k] = v
    for k in getattr(obs, "__slots__", ()):
        if k not in out and hasattr(obs, k): out[k] = getattr(obs, k)
    if out.get("step") is None and out.get("day") is not None:
        out["step"] = int(out["day"]) * HOURS + int(out.get("hour") or 0)
    return out

_bundle_keys = set()
def fresh_agent():
    for k in list(_bundle_keys):
        sys.modules.pop(k, None)
    pre = set(sys.modules)
    ag = load_submission_agent(AGENT_PATH)
    _bundle_keys.update(set(sys.modules) - pre)
    return ag

def tape_stats(replay, me):
    acts = twin.replay_transition_actions(replay)
    ext_cum = [0.0]*30; cows_cum = [0]*30
    for t, pair in enumerate(acts):
        d = t // HOURS
        for o in (pair[me].get('market') or []):
            if o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT':
                ext_cum[d] += o[2]
            elif o[0] == 'BUY_ANIMAL' and o[1] == 'COW':
                cows_cum[d] += 1
    for d in range(1, 30):
        ext_cum[d] += ext_cum[d-1]; cows_cum[d] += cows_cum[d-1]
    return ext_cum, cows_cum

class Mid:
    """Hypothesis middleware over agent actions."""
    def __init__(self, flags, tape_ext_cum, tape_cows_cum):
        self.f = flags
        self.tape_ext = tape_ext_cum; self.tape_cows = tape_cows_cum
        self.pending_cows = 0; self.cows_so_far = 0; self.ext_so_far = 0.0
        self.seeds_bought = 0
        self.counters = {}
    def bump(self, k, n=1):
        self.counters[k] = self.counters.get(k, 0) + n
    def allowed_ext(self, day):
        return 0.6875 * self.tape_ext[min(day, 29)]
    def process(self, action, obs, t):
        day = t // HOURS
        a = copy.deepcopy(action)
        f = obs.farms; pr = obs.private
        me = obs.player
        farm = f[me]
        market = a.get('market') or []
        shed = dict(pr['shed'])
        # ---- PLACEBO: minimal perturbation (trim 1 wheat unit, one shot d8-9) ----
        if self.f.get('PLACEBO') and 8 <= day <= 9:
            for o in market:
                if o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT' and o[2] > 1:
                    o[2] -= 1; self.bump('PLACEBO_trim'); break
        # ---- A1: cow delay d0-4 -> d5-7 ----
        if self.f.get('A1'):
            kept_mk = []
            for o in market:
                if day <= 4 and o[0] == 'BUY_ANIMAL' and o[1] == 'COW':
                    self.pending_cows += 1; self.bump('A1_suppressed')
                else:
                    kept_mk.append(o)
            market = kept_mk
            for o in market:
                if o[0] == 'BUY_ANIMAL' and o[1] == 'COW':
                    self.cows_so_far += 1
            if 5 <= day <= 7 and self.pending_cows > 0:
                target = self.tape_cows[min(day, 29)]
                gap = min(self.pending_cows, target - self.cows_so_far)
                room = 10 - len(market)
                inj = max(0, min(gap, room))
                for _ in range(inj):
                    market.append(['BUY_ANIMAL', 'COW'])
                self.cows_so_far += inj; self.pending_cows -= inj
                self.bump('A1_injected', inj)
        else:
            pass
        # ---- A3: external wheat dependency 0.48 -> 0.33 ----
        if self.f.get('A3'):
            shed_wheat_total = shed.get('WHEAT', 0) + sum(inv.get('WHEAT', 0) for inv in pr['inventories'])
            survival = shed_wheat_total < 4
            kept = []
            for o in market:
                if o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT' and not survival:
                    allow = self.allowed_ext(day) - self.ext_so_far
                    if allow <= 0:
                        self.bump('A3_dropped', o[2]); continue
                    n = min(int(o[2]), int(allow))
                    if n < o[2]: self.bump('A3_trimmed', o[2]-n)
                    if n > 0:
                        kept.append(['BUY_PRODUCT','WHEAT',n]); self.ext_so_far += n
                else:
                    if o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT':
                        self.ext_so_far += o[2]
                    kept.append(o)
            market = kept
        else:
            for o in market:
                if o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT':
                    self.ext_so_far += o[2]
        # ---- A2: clearing windows ----
        if self.f.get('A2'):
            if day in (10, 11):
                room = 10 - len(market)
                for item in ('MILK', 'MELON'):
                    if room <= 0: break
                    avail = shed.get(item, 0)
                    if avail > 0:
                        q = min(avail, 3)
                        market.append(['SELL', item, q]); shed[item] -= q; room -= 1
                        self.bump('A2_d10_uprate', q)
            if day >= 28:
                market = [o for o in market if o[0] not in ('BUY_ANIMAL','BUY_SEED','BUY_PRODUCT')]
                for item in ('MELON','WOOL','MILK','STRAWBERRY','FERTILIZER','TOMATO','EGG','CARROT','WHEAT'):
                    if len(market) >= 10: break
                    avail = shed.get(item, 0)
                    if avail > 0:
                        market.append(['SELL', item, avail]); shed[item] = 0
                        self.bump('A2_d2829_clear', avail)
        # ---- A4: CARE/FEED priority (fill wasted PASS ops) ----
        if self.f.get('A4'):
            units = [farm['farmer']] + [list(h) for h in farm['hands']]
            ops = [a.get('farmer')] + [x for x in (a.get('hands') or [])]
            farmer_op = a.get('farmer'); hands_ops = a.get('hands') or []
            all_ops = [farmer_op] + hands_ops
            for i, (pos, op) in enumerate(zip(units, all_ops)):
                if not op or op[0] != 'PASS': continue
                tl = farm['tiles'][pos[1]][pos[0]]
                if not (isinstance(tl, dict) and 'animal' in tl): continue
                inv = pr['inventories'][i] if i < len(pr['inventories']) else {}
                if not tl.get('fed_today') and inv.get('WHEAT', 0) > 0:
                    new = ['FEED']; self.bump('A4_feed_fill')
                elif not tl.get('cared_today'):
                    new = ['CARE']; self.bump('A4_care_fill')
                else:
                    continue
                if i == 0: a['farmer'] = new
                else: hands_ops[i-1] = new
            a['hands'] = hands_ops
        a['market'] = market
        return a

def run_arm(replay, me, flags, tape_ext_cum, tape_cows_cum, want_stream=False):
    state = twin.build_state_from_replay(replay, 0)
    acts = twin.replay_transition_actions(replay)
    agent = fresh_agent()
    mid = Mid(flags, tape_ext_cum, tape_cows_cum)
    stream = []
    t = 0
    while not state.env.done and t < len(acts):
        obs = state.seats[me].observation
        so = structify_obs(obs)
        raw = agent(so)
        mine = mid.process(raw, obs, t)
        theirs = acts[t][1-me]
        if want_stream: stream.append((t, copy.deepcopy(mine)))
        pair = [theirs, theirs]; pair[me] = mine
        twin.step(state, pair)
        t += 1
    finals = twin.final_money(state)
    return finals, mid.counters, t

ARMS = {
    'B':    {},
    'PLACEBO': {'PLACEBO': True},
    'A1':   {'A1': True},
    'A2':   {'A2': True},
    'A3':   {'A3': True},
    'A4':   {'A4': True},
    'COMBO':{'A1': True, 'A2': True, 'A3': True, 'A4': True},
}

def main():
    games = json.load(open('/tmp/fullmodel/M5/games.json'))
    out = {}
    for g in games:
        ep = str(g['ep']); fp = g['path']; me = g['me']; kind = g['kind']
        replay = json.load(open(fp))
        tape_ext, tape_cows = tape_stats(replay, me)
        rec = {'ep': ep, 'kind': kind, 'me': me, 'tape_rewards': replay['rewards'], 'arms': {}}
        for arm, flags in ARMS.items():
            t0 = time.time()
            finals, counters, steps = run_arm(replay, me, flags, tape_ext, tape_cows)
            rec['arms'][arm] = {
                'finals': finals, 'ours': finals[me], 'opp': finals[1-me],
                'margin': finals[me] - finals[1-me],
                'counters': counters, 'steps': steps,
                'wall_s': round(time.time()-t0, 2)}
            print(f"  {ep} {arm}: ours={finals[me]:.0f} opp={finals[1-me]:.0f} "
                  f"margin={finals[me]-finals[1-me]:.0f} {counters} ({rec['arms'][arm]['wall_s']}s)", flush=True)
        out[ep] = rec
        b = rec['arms']['B']
        rec['valid'] = (abs(b['finals'][0]-replay['rewards'][0]) < 1e-6 and
                        abs(b['finals'][1]-replay['rewards'][1]) < 1e-6)
        print(f"{ep} kind={kind} valid_baseline={rec['valid']}", flush=True)
    with open('/tmp/fullmodel/M5/arm_results.json', 'w') as h:
        json.dump(out, h, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
