"""Small independent review of archived R5; never changes released agents.

This is functional paired-seat evidence, not a leaderboard rating estimator.
"""
import ast
import hashlib
import json
import tarfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from league_round9 import run_job


def main():
    package = ROOT / 'submissions/release_v10_r5/submission.tar.gz'
    candidate = ROOT / 'submissions/release_v10_r5/main.py'
    with tarfile.open(package, 'r:gz') as archive:
        members = archive.getmembers()
        assert all(m.isfile() and Path(m.name).name == m.name for m in members)
        archived = archive.extractfile('main.py').read()
    assert archived == candidate.read_bytes()
    compile(archived.decode('utf-8'), 'archive/main.py', 'exec')
    tree = ast.parse(archived)
    defined = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    seeds = [int.from_bytes(hashlib.sha256(
        f'r5-independent-review-20261001-{i}'.encode()).digest()[:4], 'big') % 2000000000
        for i in range(2)]
    prior = set()
    for path in (ROOT / 'research').glob('round*/league_seeds.json'):
        for values in json.loads(path.read_text(encoding='utf-8')).values():
            prior.update(values)
    assert not prior.intersection(seeds)
    opponents = ['release_v9', 'release_v10_r4_2']
    jobs = []
    for opponent in opponents:
        source = ROOT / 'submissions' / opponent / 'main.py'
        for seed in seeds:
            for seat in (0, 1):
                jobs.append(dict(candidate=str(candidate),
                    candidate_sha256=hashlib.sha256(archived).hexdigest(),
                    opponent=str(source),
                    opponent_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    seed=seed, seat=seat, split='independent-functional-review'))
    manifest = dict(archive_sha256=hashlib.sha256(package.read_bytes()).hexdigest(),
                    source_sha256=hashlib.sha256(archived).hexdigest(),
                    official_entry_expected=defined[-1], seeds=seeds,
                    overlap_with_previous_league_seeds=0, jobs=jobs)
    directory = ROOT / 'results/r5_review_20261001'
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    rows = []
    with ProcessPoolExecutor(max_workers=4) as pool, (directory / 'games.jsonl').open('w', encoding='utf-8') as handle:
        for future in as_completed([pool.submit(run_job, job) for job in jobs]):
            row = future.result()
            rows.append(row)
            handle.write(json.dumps(row) + '\n')
            handle.flush()
            print(json.dumps({k:row.get(k) for k in ('seed','seat','opponent','delta','valid','max_action_seconds')}), flush=True)
    summary = dict(games=len(rows), valid=sum(r.get('valid', False) for r in rows),
                   per_opponent={}, note='Only two fresh worlds per opponent, both seats. Cannot estimate general win rate or Kaggle score.')
    for opponent in opponents:
        chosen = [r for r in rows if Path(r['opponent']).parent.name == opponent]
        summary['per_opponent'][opponent] = dict(
            wins=sum(r.get('delta',0)>0 for r in chosen),
            losses=sum(r.get('delta',0)<0 for r in chosen),
            ties=sum(r.get('delta',0)==0 for r in chosen),
            margins=[r.get('delta') for r in chosen],
            mean_margin=sum(r.get('delta',0) for r in chosen)/len(chosen))
    summary['max_action_seconds'] = max(r.get('max_action_seconds',0) for r in rows)
    summary['entry_names'] = list({r['entry_names'][0] for r in rows if r.get('entry_names')})
    (directory / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
