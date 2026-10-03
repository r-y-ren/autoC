"""Freeze and validate the selected v7 candidate without promoting root entrypoints.

Run only after the independent performance panels approve this exact source hash.
The build uses the official last-callable entry and validates the packed bytes.
"""
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'experiments/round7_orderbook_v56.py'
EXPECTED = '273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'
EXPECTED_ENTRY = 'round7_orderbook_v56_agent'
ACTION_LIMIT_SECONDS = 1.0
SOURCES = {
    'Orderbook': 'https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book',
    'V56': 'https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer',
}

# Standard-library-only worker, matching get_last_callable's namespace ordering.
# It does not import Kaggle or third-party packages, and does not use an old alias.
ISOLATED_WORKER = r'''
import contextlib, hashlib, io, json, sys, time
raw = open(sys.argv[1], encoding='utf-8').read()
namespace = {}
initial_stdout = io.StringIO()
load_start = time.perf_counter()
with contextlib.redirect_stdout(initial_stdout):
    exec(compile(raw, sys.argv[1], 'exec'), namespace)
load_seconds = time.perf_counter() - load_start
if initial_stdout.getvalue():
    sys.stderr.write(initial_stdout.getvalue())
entry = [value for value in namespace.values() if callable(value)][-1]
assert entry.__name__ == sys.argv[2], entry.__name__
required = {'seed_errors', 'fertilizer_errors', 'cxd_errors', 'cxtb_errors'}

def error_counters():
    counters = {}
    for name, value in namespace.items():
        if not isinstance(value, dict) or not ('REPORT' in name.upper() or 'STATS' in name.upper()):
            continue
        for key, count in value.items():
            if isinstance(count, (int, float)) and ('error' in str(key).lower() or 'fallback' in str(key).lower()):
                counters[name + '.' + str(key)] = count
    exposed = getattr(entry, 'telemetry', {})
    assert required <= set(exposed), sorted(required - set(exposed))
    for key, count in exposed.items():
        if isinstance(count, (int, float)) and ('error' in key.lower() or 'fallback' in key.lower()):
            counters['entry.' + key] = count
    impl = namespace.get('_IMPL')
    chassis = getattr(impl, 'chassis', None)
    for key, count in getattr(chassis, 'diagnostics', {}).items():
        if isinstance(count, (int, float)) and ('error' in key.lower() or 'fallback' in key.lower()):
            counters['chassis.' + key] = count
    return counters

for index, line in enumerate(sys.stdin):
    record = json.loads(line)
    callback_stdout = io.StringIO()
    started = time.perf_counter()
    with contextlib.redirect_stdout(callback_stdout):
        action = entry(record['obs'], record['cfg'])
    seconds = time.perf_counter() - started
    if callback_stdout.getvalue():
        sys.stderr.write(callback_stdout.getvalue())
    counters = error_counters()
    bad = {key:value for key,value in counters.items() if value != 0}
    state = None
    if int(record['obs']['step']) == 0 or index == 1437:
        state = {'counters':counters,
                 'seed':dict(namespace['_E402_REPORT']),
                 'fertilizer':dict(namespace['_E410_REPORT']),
                 'orderbook':dict(namespace['_CXD_REPORT'])}
    print(json.dumps({'action':action, 'errors':bad, 'seconds':seconds,
                      'state':state, 'entry_name':entry.__name__,
                      'load_seconds':load_seconds if index==0 else None}))
'''


def main():
    source = SOURCE.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED, 'Candidate changed after selection'
    compile(source.decode('utf-8'), str(SOURCE), 'exec')
    release = ROOT / 'submissions/release_v7'
    release.mkdir(parents=True, exist_ok=True)
    # Keep the older notice verbatim as an inherited notice, then identify the
    # precise new source and limited local integration prominently.
    inherited = (ROOT / 'external/one_more_wheat_NOTICE.txt').read_bytes()
    notice = ('''Kaggriculture v7 local integration, 2026-09-22. Apache-2.0.
Base: shiiin9, Your Market List Is an Order Book, including the complete
Ahmed Berat Ozer V55 lineage and all notices embedded in main.py.
https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book
Appended mechanisms: Ahmed Berat Ozer V56 EXP402 remaining-planting seed
budget and EXP410 harvest-aware fertilizer cap.
https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer
Local integration: attach the V56 tail to Orderbook's _cxd_agent, expose
combined telemetry, preserve Orderbook source bytes and its constants.
The repository's Vadim/DSM public-replay research is separate: this artifact
contains no claim of access to either author's private strategy source code.
No leaderboard rating is asserted by this package.

Inherited notices from the preceding public-source release follow verbatim:
--------------------------------------------------------------------------
''').encode('utf-8') + inherited
    payloads = {
        'main.py': source,
        'NOTICE.txt': notice,
        'LICENSE.txt': (ROOT / 'external/one_more_wheat_LICENSE.txt').read_bytes(),
    }
    for name, payload in payloads.items():
        (release / name).write_bytes(payload)
    archive = release / 'submission.tar.gz'
    with archive.open('wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for name, payload in payloads.items():
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(payload), 0o644, 0
                tf.addfile(info, io.BytesIO(payload))
    stage = release / 'validation'
    stage.mkdir(exist_ok=True)
    with tarfile.open(archive) as tf:
        assert tf.getnames() == list(payloads)
        for name, payload in payloads.items():
            assert tf.extractfile(name).read() == payload
    actual = stage / 'main.py'
    actual.write_bytes(source)
    import_output = io.StringIO()
    with contextlib.redirect_stdout(import_output):
        import kaggle_environments
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    (stage / 'environment-import-notices.txt').write_text(import_output.getvalue(), encoding='utf-8')
    official_entry = get_last_callable(source.decode('utf-8'), path=str(actual))
    assert official_entry.__name__ == EXPECTED_ENTRY, official_entry.__name__

    fixtures, expected, games = [], [], []
    for seed, opponent in [(91001, str(actual)), (91002, str(ROOT / 'external/orderbook.py'))]:
        env = make('kaggriculture', configuration={'seed':seed,'episodeSteps':720}, debug=True)
        env.run([str(actual), opponent])
        logs = [entry for row in env.logs for entry in row if isinstance(entry,dict)]
        # Preserve full logs before any assertion; never truncate stderr evidence.
        (stage / f'game-{seed}-logs.json').write_text(json.dumps(env.logs,indent=2),encoding='utf-8')
        stderr = [entry.get('stderr','') for entry in logs if entry.get('stderr','').strip()]
        assert not stderr, f'Agent stderr: see {stage / f"game-{seed}-logs.json"}'
        assert len(env.steps) == 720
        assert [s.status for s in env.steps[-1]] == ['DONE','DONE']
        maximum = max((entry.get('duration',0) for entry in logs),default=0)
        assert maximum < ACTION_LIMIT_SECONDS, (seed, maximum, 'one-second callback budget')
        for t in range(719):
            obs = dict(env.steps[t][0].observation)
            obs['step'] = t
            fixtures.append({'obs':obs,'cfg':dict(env.configuration)})
            action = env.steps[t+1][0].action
            assert set(action) == {'farmer','hands','market'}
            assert len(action['market']) <= 10
            expected.append(action)
        games.append({'seed':seed,'opponent':opponent,'money':[s.reward for s in env.steps[-1]],
                      'statuses':[s.status for s in env.steps[-1]],'states':len(env.steps),
                      'max_action_seconds_both':maximum,'stderr_records':len(stderr)})
        print(json.dumps(games[-1]),flush=True)

    parity = []
    for sorted_keys in (False, True):
        label = 'sorted' if sorted_keys else 'original'
        result = subprocess.run([sys.executable,'-I','-S','-c',ISOLATED_WORKER,str(actual),EXPECTED_ENTRY],
                                input='\n'.join(json.dumps(row,sort_keys=sorted_keys) for row in fixtures),
                                text=True,encoding='utf-8',capture_output=True,timeout=240)
        (stage / f'isolated-{label}-stderr.txt').write_text(result.stderr,encoding='utf-8')
        (stage / f'isolated-{label}-records.jsonl').write_text(result.stdout,encoding='utf-8')
        assert result.returncode == 0, f'Isolated worker failed; see isolated-{label}-stderr.txt'
        assert not result.stderr.strip(), f'Source stderr; see isolated-{label}-stderr.txt'
        records = [json.loads(line) for line in result.stdout.splitlines()]
        assert len(records) == len(expected) == 1438, len(records)
        errors = [(i,row['errors']) for i,row in enumerate(records) if row['errors']]
        assert not errors, errors[:10]
        differences = [i for i,(record,action) in enumerate(zip(records,expected)) if record['action'] != action]
        assert not differences, differences[:10]
        maximum = max(row['seconds'] for row in records)
        assert maximum < ACTION_LIMIT_SECONDS, (label, maximum, 'one-second callback budget')
        snapshots = {str(i):row['state'] for i,row in enumerate(records) if row['state'] is not None}
        # The 720th callback starts the second episode in the SAME namespace.
        assert set(snapshots) == {'0','719','1437'}, snapshots.keys()
        for index in ('0','719'):
            assert all(value == 0 for value in snapshots[index]['seed'].values())
            assert all(value == 0 for value in snapshots[index]['fertilizer'].values())
        parity.append({'sorted_observation_keys':sorted_keys,'matching_actions':len(records),
                       'nonzero_error_counters':len(errors),'entry_name':records[0]['entry_name'],
                       'max_action_seconds':maximum,'source_load_seconds':records[0]['load_seconds'],
                       'state_snapshots':snapshots})
        print(f'Continuous isolated parity passed: {label}, {len(records)} actions.',flush=True)

    report = {'source_sha256':EXPECTED,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
              'archive_members':list(payloads),'games':games,'isolated_checks':parity,
              'third_party_packages_disabled':True,'state_reset_between_episodes':True,
              'observed_callback_limit_seconds':ACTION_LIMIT_SECONDS,
              'timing_scope':'Observed on this host; not a guarantee for every input or Kaggle hardware.'}
    (release / 'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    manifest = {'release':'v7','strategy':'Orderbook plus public V56 seed/fertilizer mechanisms',
                'source_urls':SOURCES,'license':'Apache-2.0; source and inherited notices retained',
                'environment':f'kaggle-environments {kaggle_environments.__version__}',
                'online_score':None,'entry_name':EXPECTED_ENTRY,'source_sha256':EXPECTED,
                'archive_sha256':report['archive_sha256'],'source_bytes':len(source),
                'archive_bytes':archive.stat().st_size,'promotes_root_entrypoints':False}
    (release / 'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('v7 archive verified; root entrypoints were not changed.',flush=True)


if __name__ == '__main__':
    main()
