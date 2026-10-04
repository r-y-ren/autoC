"""Random search over hybrid engine parameters. usage: sweep.py n_configs seeds workers tag"""
import sys, json, random, os, subprocess, time
from concurrent.futures import ProcessPoolExecutor
import arena

from best_cfg import BEST
BASE = dict(BEST)
BASE.update({'fert_buy_max_price': 0, 'smart_sell': True, 'harvest_guard': True, 'end_animal': True})
SPACE = {
    'max_hands': [11, 12, 13, 14],
    'hand_turns': [15.0, 17.0, 19.0],
    'hold_theta': [0.8, 0.85, 0.9, 0.95],
    'peak_window': [24, 36, 72],
    'liquidate_steps': [12, 24, 40],
    'no_hold_hour': [8, 12, 16, 20],
    'end_keep_hour': [6, 12, 18],
    'guard_hour': [14, 16, 18],
    'night_target': [75, 82, 88],
    'night_harvest_cap': [70, 80, 90],
    'endgame_steps': [14, 22, 30],
    'otw_min': [2.0, 3.0, 4.0],
    'deliver_count': [3, 4, 6, 10],
    'switch': [600, 648, 672],
}


def build(cfg, path):
    sw = cfg.pop('switch')
    ov = dict(BASE)
    ov.update(cfg)
    subprocess.run([sys.executable, 'mk_hybrid.py', path, str(sw), repr(ov)], check=True, capture_output=True)
    cfg['switch'] = sw


def main():
    n, seeds, workers, tag = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(hash(tag) & 0xffff)
    os.makedirs('sweep', exist_ok=True)
    log = open(f'sweep/{tag}.jsonl', 'a')
    for i in range(n):
        cfg = {k: rng.choice(v) for k, v in SPACE.items()}
        path = f'sweep/{tag}_{i}.py'
        build(cfg, path)
        jobs = [(path, 'cand/r2.py', s, seat) for s in range(1000, 1000 + seeds) for seat in (0,)]
        with ProcessPoolExecutor(workers) as p:
            res = list(p.map(arena.run, jobs))
        ok = [r for r in res if 'me' in r]
        ratio = sum(r['me'] for r in ok) / max(1, sum(r['op'] for r in ok))
        rec = dict(i=i, cfg=cfg, ratio=round(ratio, 4), n=len(ok), me=round(sum(r['me'] for r in ok) / max(1, len(ok))))
        log.write(json.dumps(rec) + '\n')
        log.flush()
        print(json.dumps(rec), flush=True)


if __name__ == '__main__':
    main()
