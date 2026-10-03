"""Resumable official-engine league. Source hashes and seed manifests are immutable.

Seats are clustered by seed in reports: they are not independent samples.
Development and confirmation seeds are generated before selection and kept apart.
"""
import argparse
import contextlib
import gc
import hashlib
import io
import json
import random
import statistics
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def freeze_seeds():
    p = ROOT / 'research/round8/league_seeds.json'
    expected = {split: [int.from_bytes(hashlib.sha256(f'kaggriculture-r8-{split}-{i}'.encode()).digest()[:4], 'big') % 2000000000
                       for i in range(count)]
                for split, count in [('development', 20), ('confirmation', 40), ('reserve', 40)]}
    if p.exists():
        assert json.loads(p.read_text()) == expected
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(expected, indent=2), encoding='utf-8')
    return expected


def telemetry(entry):
    namespace = getattr(entry, '__globals__', {})
    counters, details = {}, {}
    for name, value in namespace.items():
        if isinstance(value, dict) and any(x in name.upper() for x in ['REPORT', 'STATS', 'TELEMETRY']):
            details[name] = {str(k): v for k, v in value.items() if isinstance(v, (int, float, str, bool)) or v is None}
            for key, count in value.items():
                if isinstance(count, (int, float)) and any(x in str(key).lower() for x in ['error', 'fallback']):
                    counters[name + '.' + str(key)] = count
    exposed = getattr(entry, 'telemetry', {})
    details['entry'] = {k:v for k,v in exposed.items() if isinstance(v, (int,float,str,bool)) or v is None}
    for key, count in exposed.items():
        if isinstance(count, (int, float)) and any(x in str(key).lower() for x in ['error', 'fallback']):
            counters['entry.' + str(key)] = count
    chassis = getattr(namespace.get('_IMPL'), 'chassis', None)
    for key, count in getattr(chassis, 'diagnostics', {}).items():
        if isinstance(count, (int, float)) and any(x in str(key).lower() for x in ['error', 'fallback']):
            counters['chassis.' + str(key)] = count
    return {'counters': counters, 'nonzero': {k:v for k,v in counters.items() if v}, 'details': details}


def run_job(job):
    started = time.perf_counter()
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            import kaggle_environments
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
        paths = [job['candidate'], job['opponent']]
        assert [digest(p) for p in paths] == [job['candidate_sha256'], job['opponent_sha256']]
        load_log = io.StringIO()
        with contextlib.redirect_stdout(load_log), contextlib.redirect_stderr(load_log):
            entries = [get_last_callable(Path(p).read_text(encoding='utf-8'), path=str(ROOT / p)) for p in paths]
        ordered = entries[::-1] if job['seat'] else entries
        env = make('kaggriculture', configuration={'seed':job['seed'], 'episodeSteps':720}, debug=True)
        env.run(ordered)
        final = env.steps[-1]
        s = job['seat']
        money = [final[i].observation.farms[i]['money'] for i in (s, 1-s)]
        logs = [(i,l) for step in env.logs for i,l in enumerate(step) if isinstance(l,dict)]
        stderr = [(i,l['stderr'][:1200]) for i,l in logs if l.get('stderr','').strip()]
        ts = [telemetry(e) for e in entries]
        delta = money[0] - money[1]
        result = {**job, 'money':money[0], 'opponent_money':money[1], 'delta':delta,
                  'points':1 if delta>0 else 0 if delta<0 else .5,
                  'states':len(env.steps), 'statuses':[x.status for x in final],
                  'stderr':stderr, 'load_log':load_log.getvalue()[:1200],
                  'telemetry':ts, 'entry_names':[e.__name__ for e in entries],
                  'seconds':round(time.perf_counter()-started,3),
                  'max_action_seconds':max((l.get('duration',0) for i,l in logs if i==s),default=0),
                  'final_carried':sum(sum(v.values()) for v in final[s].observation.private['inventories']),
                  'final_shed':dict(final[s].observation.private['shed']),
                  'shops':list(final[s].observation.town['unlocked_shops']),
                  'environment_version':kaggle_environments.__version__}
        result['valid'] = result['statuses']==['DONE','DONE'] and len(env.steps)==720 and not stderr and not any(t['nonzero'] for t in ts)
        del env, entries, ordered, final
        gc.collect()
        return result
    except Exception:
        return {**job, 'valid':False, 'exception':traceback.format_exc(), 'seconds':time.perf_counter()-started}


def summarize(rows):
    out = {}
    for opp in sorted({r['opponent'] for r in rows}):
        group = [r for r in rows if r['opponent']==opp]
        good = [r for r in group if r.get('valid')]
        by_seed = {}
        for r in good:
            by_seed.setdefault(r['seed'], []).append(r)
        points = [statistics.mean(r['points'] for r in g) for g in by_seed.values()]
        rng = random.Random(20260922)
        means = sorted(statistics.mean(rng.choices(points,k=len(points))) for _ in range(3000)) if points else []
        out[opp] = {'games':len(group), 'valid':len(good), 'worlds':len(by_seed),
                    'wins':sum(r['delta']>0 for r in good), 'losses':sum(r['delta']<0 for r in good),
                    'ties':sum(r['delta']==0 for r in good),
                    'mean_margin':statistics.mean(r['delta'] for r in good) if good else None,
                    'median_margin':statistics.median(r['delta'] for r in good) if good else None,
                    'points':statistics.mean(points) if points else None,
                    'world_bootstrap_points_95': [means[75],means[2924]] if means else None}
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--candidate',default='submissions/release_v7/main.py')
    p.add_argument('--opponents',nargs='+',required=True)
    p.add_argument('--split',choices=['development','confirmation','reserve'],default='development')
    p.add_argument('--count',type=int)
    p.add_argument('--workers',type=int,default=3)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    seeds=freeze_seeds()[a.split][:a.count]
    paths=[a.candidate]+a.opponents
    hashes={x:digest(x) for x in paths}
    out=ROOT/a.output; out.parent.mkdir(parents=True,exist_ok=True)
    manifest={'candidate':a.candidate,'opponents':a.opponents,'hashes':hashes,'split':a.split,'seeds':seeds,'seats':[0,1]}
    mp=out.with_suffix('.manifest.json')
    if mp.exists(): assert json.loads(mp.read_text())==manifest, 'Manifest changed; use a new output filename'
    else: mp.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    ledger=out.with_suffix('.jsonl')
    rows=[json.loads(line) for line in ledger.read_text(encoding='utf-8').splitlines()] if ledger.exists() else []
    done={r['id'] for r in rows}
    jobs=[]
    for seed in seeds:
        for opp in a.opponents:
            for seat in [0,1]:
                j={'candidate':a.candidate,'candidate_sha256':hashes[a.candidate],'opponent':opp,'opponent_sha256':hashes[opp], 'seed':seed,'seat':seat,'split':a.split}
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24]
                if j['id'] not in done: jobs.append(j)
    print(json.dumps({'pending':len(jobs),'existing':len(rows),'worlds':len(seeds)}),flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool, ledger.open('a',encoding='utf-8') as f:
        futures=[pool.submit(run_job,j) for j in jobs]
        for future in as_completed(futures):
            r=future.result(); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps({k:r.get(k) for k in ['seed','seat','opponent','delta','valid','seconds']}),flush=True)
            if len(rows)%10==0 or len(rows)==len(jobs)+len(done):
                out.write_text(json.dumps({'manifest':manifest,'games':len(rows),'summary':summarize(rows)},indent=2),encoding='utf-8')
    print(json.dumps(summarize(rows)),flush=True)


if __name__=='__main__': main()
