"""Build an explicitly unpromoted round-8 candidate and validate its packed bytes.

Run with the venv Python. All matches run sequentially. This is a technical
acceptance check, never a leaderboard/strength approval or an online submission.
The expected hash must match the source selected before this invocation.
"""
import argparse
import contextlib
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parent
FROZEN_HASH = '9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e'
V7_HASH = '273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'
ENTRY = 'round8_production_fusion_agent'
LIMIT_SECONDS = 1.0
SOURCES = {
    'Orderbook': 'https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book',
    'V56': 'https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer',
    'Master2965_v4': 'https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine',
    'production_layout_episode': 'https://www.kaggle.com/competitions/kaggriculture/episodes/111747876',
}

# This exact helper text is used both in the official-game observer and in the
# isolated worker. Numeric globals such as _RELEASE_ERRORS are included, as are
# reports inside literal exec namespaces and the chassis' own diagnostics.
DIAGNOSTICS = r'''
def error_counters(namespace, entry):
    counters = {}
    def inspect(value, path, inherited_error=False, depth=0):
        if depth > 6:
            return
        flagged = inherited_error or any(word in path.lower() for word in ('error', 'fallback'))
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if flagged:
                counters[path] = value
        elif isinstance(value, dict):
            for key, child in value.items():
                inspect(child, path + '.' + str(key), flagged, depth + 1)
    def inspect_namespace(ns, prefix=''):
        for name, value in ns.items():
            if any(word in name.upper() for word in ('REPORT', 'STATS', 'TELEMETRY', 'ERROR', 'FALLBACK')):
                inspect(value, prefix + name)
    inspect_namespace(namespace)
    for name in ('_UNIT_NS', '_PLANNER_NS'):
        if isinstance(namespace.get(name), dict):
            inspect_namespace(namespace[name], name + '.')
    inspect(getattr(entry, 'telemetry', {}), 'entry')
    inspect(getattr(entry, 'routing_telemetry', {}), 'entry.routing_telemetry')
    for name, value in namespace.items():
        if not name.startswith('_'):
            continue
        inspect(getattr(value, 'diagnostics', {}), name + '.diagnostics')
        chassis = getattr(value, 'chassis', None)
        inspect(getattr(chassis, 'diagnostics', {}), name + '.chassis.diagnostics')
    return counters

def state_fingerprints(namespace, observation):
    player = int(observation['player'])
    fingerprints = {}
    def normalized(value):
        if isinstance(value, dict):
            return {str(k):normalized(v) for k,v in value.items()}
        if isinstance(value, (list, tuple)):
            return [normalized(v) for v in value]
        if isinstance(value, set):
            return sorted([normalized(v) for v in value], key=repr)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        raise TypeError(type(value).__name__)
    def add(path, mapping):
        if not isinstance(mapping, dict) or player not in mapping:
            return
        fingerprints[path] = hashlib.sha256(json.dumps(normalized(mapping[player]), sort_keys=True).encode()).hexdigest()
    for name, value in namespace.items():
        if name.upper().endswith(('_STATE', '_STATES')):
            add(name, value)
        if name.startswith('_'):
            for field in ('state', 'players'):
                add(name + '.' + field, getattr(value, field, None))
            chassis = getattr(value, 'chassis', None)
            add(name + '.chassis.players', getattr(chassis, 'players', None))
    return fingerprints

def reset_snapshot(namespace, observation, entry):
    player = int(observation['player'])
    snapshot = {'player':player, 'state_fingerprints':state_fingerprints(namespace, observation),
                'errors':error_counters(namespace, entry)}
    if not all(key in namespace for key in ('_T19_REPORT', '_E402_REPORT', '_E410_REPORT')):
        return snapshot
    state = namespace.get('_V219_STATES', {}).get(player, {})
    snapshot.update({
        'seed': dict(namespace['_E402_REPORT']),
        'fertilizer': dict(namespace['_E410_REPORT']),
        'production': dict(namespace['_T19_REPORT']),
        'production_state': {
            'last_step': state.get('last_step'),
            'day': state.get('day'),
            'workers': len(state.get('workers', {})),
            'seen_plants': len(state.get('seen_plants', set())),
            'committed': bool(state.get('committed', False)),
            't19_enabled': bool(state.get('t19_enabled', False)),
            'pending': bool(state.get('pending') or state.get('t19_pending')),
        },
        'r148_pending_for_player': bool(namespace.get('_R148_PENDING', {}).get(player)),
        # ADV's inherited front_turns is cumulative reporting only; the public
        # source does not reset this statistic. Preserve and disclose it.
        'adv_front_turns_cumulative': namespace.get('_ADV_REPORT', {}).get('front_turns', 0),
    })
    return snapshot

def assert_reset(snapshot):
    assert not any(snapshot['errors'].values())
    if 'production_state' not in snapshot:
        return
    for key in ('seed', 'fertilizer', 'production'):
        assert all(value == 0 for value in snapshot[key].values()), (key, snapshot[key])
    st = snapshot['production_state']
    assert st == {'last_step':0, 'day':-1, 'workers':0, 'seen_plants':0,
                  'committed':False, 't19_enabled':False, 'pending':False}, st
    assert not snapshot['r148_pending_for_player']
'''
exec(DIAGNOSTICS)

ISOLATED_WORKER = r'''
import contextlib, gzip, hashlib, io, json, sys, tarfile, time
assert sys.flags.isolated == 1 and sys.flags.no_site == 1
archive, fixture_file, expected_hash, expected_entry, sorted_keys = sys.argv[1:]
with tarfile.open(archive, 'r:gz') as tf:
    source = tf.extractfile('main.py').read()
assert hashlib.sha256(source).hexdigest() == expected_hash
namespace = {}
initial_stdout = io.StringIO()
loaded = time.perf_counter()
with contextlib.redirect_stdout(initial_stdout):
    exec(compile(source.decode('utf-8'), archive + '/main.py', 'exec'), namespace)
load_seconds = time.perf_counter() - loaded
if initial_stdout.getvalue():
    sys.stderr.write(initial_stdout.getvalue())
entry = [value for value in namespace.values() if callable(value)][-1]
assert entry.__name__ == expected_entry, entry.__name__
''' + DIAGNOSTICS + r'''
with gzip.open(fixture_file, 'rt', encoding='utf-8') as fixture:
    for index, line in enumerate(fixture):
        record = json.loads(line)
        if sorted_keys == 'true':
            record = json.loads(json.dumps(record, sort_keys=True))
        callback_stdout = io.StringIO()
        started = time.perf_counter()
        with contextlib.redirect_stdout(callback_stdout):
            action = entry(record['obs'], record['cfg'])
        seconds = time.perf_counter() - started
        if callback_stdout.getvalue():
            sys.stderr.write(callback_stdout.getvalue())
        counters = error_counters(namespace, entry)
        bad = {key:value for key,value in counters.items() if value != 0}
        snapshot = None
        if int(record['obs']['step']) == 0:
            snapshot = reset_snapshot(namespace, record['obs'], entry)
            assert_reset(snapshot)
            # Behavioral production state must equal the freshly loaded official
            # namespace. Cumulative public reporting is not strategy state.
            assert snapshot['state_fingerprints'] == record['fresh_reset']['state_fingerprints'], ('step0 state fingerprint mismatch', snapshot['state_fingerprints'], record['fresh_reset']['state_fingerprints'])
        if int(record['obs']['step']) == 718:
            snapshot = {'production':dict(namespace.get('_T19_REPORT', {})),
                        'error_counters':counters,
                        'telemetry':dict(getattr(entry, 'telemetry', {}))}
        print(json.dumps({'index':index, 'step':record['obs']['step'],
                          'action':action, 'matches':action == record['expected_action'],
                          'errors':bad, 'seconds':seconds, 'state':snapshot,
                          'entry_name':entry.__name__,
                          'load_seconds':load_seconds if index == 0 else None}))
'''


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def make_notice(label):
    prefix = f'''Kaggriculture {label}: unpromoted candidate, 2026-09-22. Apache-2.0.
Technical acceptance and strength selection are separate. This package makes
no claim to a Kaggle rating, DSM's private code, or Vadim Vasilenko's private code.

Frozen v7 lineage: shiiin9 Orderbook and Ahmed Berat Ozer V56 EXP402/EXP410,
with its complete prior NOTICE retained verbatim below and all embedded source
notices retained in main.py. Full Apache-2.0 text is in LICENSE.txt.

Appended public market source: haideptry, The 2965 Master Hybrid Engine,
notebook version 4:
https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine
Decoded main.py SHA256:
93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f
R148 overflow reclaim: Ahmed Berat Ozer EXP277, Apache-2.0.
ADV sale advance: Ahmed Berat Ozer EXP293, Apache-2.0; mechanism attributed
in that source to sdy623 / jaxa623, Beyond 48-0. Its original attribution is
retained verbatim in main.py.
IG opening guard and cash-sale queue closure: retained from the same public
Master source. The notebook's complete engine is not local original work.
These are the source's embedded license statements; no absent standalone
Master NOTICE/LICENSE or independently verified license metadata is invented.

Local integration/modifications, 2026-09-22, Apache-2.0:
Attach R148/ADV/IG to the frozen v7 entry; expose complete diagnostics; update
the race observer with the final emitted orders. Limit ADV and its frontload
to steps below 696; retain R148/IG at the end of the game.
Local production repair: observed spatial allocation for 19 southeast tomato
plots, learned from public episode 111747876 (yomogii), with observation-based
eligibility, route assignment, hiring budget, maintenance and final delivery.
https://www.kaggle.com/competitions/kaggriculture/episodes/111747876
This is local spatial planning code, not an opponent action replay.
Final local wrapper combines market and production diagnostics only.
Public Master busyaprime seedfloat/terminal fertilizer-knock layers are not
included in this candidate. The separate terminal-input trial is not included.

Complete inherited v7 NOTICE follows verbatim:
--------------------------------------------------------------------------
'''.encode('utf-8')
    return prefix + (ROOT / 'submissions/release_v7/NOTICE.txt').read_bytes()


def run_official_games(actual, validation, trigger_seed, default_seed, expected_entry, require_production):
    imported = io.StringIO()
    with contextlib.redirect_stdout(imported), contextlib.redirect_stderr(imported):
        import kaggle_environments
        from kaggle_environments import make
        import kaggle_environments.agent as agent_module
    (validation / 'environment-import-notices.txt').write_text(imported.getvalue(), encoding='utf-8')
    games, fixtures = [], []
    for game_index, seed in enumerate((trigger_seed, default_seed)):
        # Same seat deliberately exercises step-0 reset of existing per-player
        # state in the later continuous, single-namespace replay.
        observed, callback_seconds, diagnostics = [], [], []
        holder = {}
        original_loader = agent_module.get_last_callable

        def candidate(observation, configuration):
            entry, ns = holder['entry'], holder['namespace']
            row = {'game_index':game_index, 'seed':seed,
                   'obs':copy.deepcopy(dict(observation)),
                   'cfg':copy.deepcopy(dict(configuration))}
            began = time.perf_counter()
            action = entry(observation, configuration)
            callback_seconds.append(time.perf_counter() - began)
            row['expected_action'] = copy.deepcopy(action)
            if int(observation['step']) == 0:
                row['fresh_reset'] = reset_snapshot(ns, observation, entry)
                assert_reset(row['fresh_reset'])
            counters = error_counters(ns, entry)
            bad = {key:value for key,value in counters.items() if value != 0}
            if bad:
                diagnostics.append({'step':observation['step'], 'errors':bad})
            observed.append(row)
            return action

        def observed_loader(raw, fallback=None, path=None):
            started = time.perf_counter()
            loaded = original_loader(raw, fallback=fallback, path=path)
            if path == str(actual):
                assert loaded.__name__ == expected_entry, loaded.__name__
                holder.update(entry=loaded, namespace=loaded.__globals__,
                              load_seconds=time.perf_counter() - started)
                return candidate
            return loaded

        env = make('kaggriculture', configuration={'seed':seed, 'episodeSteps':720}, debug=True)
        # Keep the official FILE-PATH execution path. Its first callback compiles
        # and decompresses the archive member inside the official timer. The
        # passive observer only records inputs, outputs and diagnostics.
        agent_module.get_last_callable = observed_loader
        try:
            env.run([str(actual), str(ROOT / 'submissions/release_v7/main.py')])
        finally:
            agent_module.get_last_callable = original_loader
        entry, ns = holder['entry'], holder['namespace']
        log_path = validation / f'game-{game_index}-{seed}-logs.json'
        write_json(log_path, env.logs)
        logs = [record for row in env.logs for record in row if isinstance(record, dict)]
        errors = [record.get('stderr', '') for record in logs if record.get('stderr', '').strip()]
        maximum = max((record.get('duration', 0) for record in logs), default=0)
        game = {'seed':seed, 'candidate_seat':0, 'opponent':'submissions/release_v7/main.py',
                'opponent_sha256':V7_HASH, 'money':[s.reward for s in env.steps[-1]],
                'states':len(env.steps), 'statuses':[s.status for s in env.steps[-1]],
                'actual_candidate_observations':len(observed),
                'max_action_seconds_both_official':maximum,
                'max_action_seconds_candidate':max(callback_seconds, default=0),
                'first_action_seconds_including_load_official':next(row[0].get('duration', 0) for row in env.logs if row and isinstance(row[0], dict)),
                'source_load_seconds':holder['load_seconds'],
                'execution_mode':'official file-path loader; passive input/output observer',
                'stderr_records':len(errors), 'nonzero_error_counters':diagnostics,
                'production':dict(ns.get('_T19_REPORT', {})),
                'final_error_counters':error_counters(ns, entry),
                'final_telemetry':dict(entry.telemetry)}
        games.append(game)
        write_json(validation / 'official-games.partial.json', games)
        assert not errors, f'Agent stderr: {log_path}'
        assert not diagnostics, diagnostics[:4]
        assert len(env.steps) == 720 and game['statuses'] == ['DONE', 'DONE'], game
        assert len(observed) == 719, len(observed)
        assert maximum < LIMIT_SECONDS, (seed, maximum)
        for step, row in enumerate(observed):
            assert row['obs']['step'] == step
            action = row['expected_action']
            assert action == env.steps[step + 1][0].action
            assert set(action) == {'farmer', 'hands', 'market'}
            assert len(action['market']) <= 10
        fixtures.extend(observed)
        if game_index == 0 and require_production:
            assert game['production'].get('eligible', 0) > 0, 'Requested production-trigger world did not trigger'
            assert game['production'].get('plants', 0) == 19, game['production']
        print(json.dumps({'official_game':game_index, 'seed':seed, 'states':len(env.steps),
                          'money':game['money'], 'production':game['production'],
                          'max_seconds':maximum}), flush=True)
    fixture_path = validation / 'real-observations.jsonl.gz'
    with fixture_path.open('wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
        for row in fixtures:
            gz.write((json.dumps(row, ensure_ascii=False) + '\n').encode('utf-8'))
    checkpoint = {'source_sha256':digest(actual.read_bytes()), 'games':games,
                  'fixture_sha256':digest(fixture_path.read_bytes()), 'observations':len(fixtures),
                  'environment':f'kaggle-environments {kaggle_environments.__version__}'}
    write_json(validation / 'official-games.json', checkpoint)
    return checkpoint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', default='experiments/round8_bounded_production.py')
    parser.add_argument('--stage', default='submissions/candidate_v8')
    parser.add_argument('--expected-sha256', default=FROZEN_HASH)
    parser.add_argument('--entry', default=ENTRY, help='Frozen expected actual last-callable name')
    parser.add_argument('--profile', choices=['bounded-production', 'generic'], default='bounded-production')
    parser.add_argument('--notice-file', help='Required complete attribution NOTICE for a generic candidate')
    parser.add_argument('--license-file', default='submissions/release_v7/LICENSE.txt')
    parser.add_argument('--label', default='candidate_v8')
    parser.add_argument('--trigger-seed', type=int, default=688041503)
    parser.add_argument('--default-seed', type=int, default=0)
    parser.add_argument('--resume', action='store_true', help='Reuse only hash-verified completed official-game fixtures')
    args = parser.parse_args()
    source_path = (ROOT / args.candidate).resolve()
    release = (ROOT / args.stage).resolve()
    assert release.is_relative_to(ROOT / 'submissions'), 'Stage must be inside this workspace submissions directory'
    assert release.name not in {'release_v7', 'release_v6'}, 'Frozen prior releases are immutable'
    source = source_path.read_bytes()
    assert digest(source) == args.expected_sha256, 'Candidate changed after its source hash was frozen'
    v7 = (ROOT / 'submissions/release_v7/main.py').read_bytes()
    assert digest(v7) == V7_HASH
    if args.profile == 'bounded-production':
        assert source.replace(b'\r\n', b'\n').startswith(v7.replace(b'\r\n', b'\n')), 'The bounded-production profile requires the frozen v7 lineage'
    else:
        assert args.notice_file, 'Generic source requires its own audited attribution NOTICE'
    compile(source.decode('utf-8'), str(source_path), 'exec')
    # Never reveal the value of a potentially configured local library path.
    assert 'V92_SELL_LIB' not in os.environ, 'Clear V92_SELL_LIB before validation; external library input is disallowed'
    if release.exists() and any(release.iterdir()):
        previous = json.loads((release / 'build-spec.json').read_text(encoding='utf-8'))
        assert previous['source_sha256'] == args.expected_sha256, 'Refusing to overwrite a different frozen candidate'
    release.mkdir(parents=True, exist_ok=True)
    validation = release / 'validation'
    validation.mkdir(exist_ok=True)
    notice = make_notice(args.label) if args.profile == 'bounded-production' else (ROOT / args.notice_file).read_bytes()
    payloads = {'main.py':source, 'NOTICE.txt':notice,
                'LICENSE.txt':(ROOT / args.license_file).read_bytes()}
    for name, raw in payloads.items():
        (release / name).write_bytes(raw)
    archive = release / 'submission.tar.gz'
    with archive.open('wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for name, data in payloads.items():
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(data), 0o644, 0
                tf.addfile(info, io.BytesIO(data))
    with tarfile.open(archive, 'r:gz') as tf:
        assert tf.getnames() == list(payloads)
        for name, data in payloads.items():
            assert tf.extractfile(name).read() == data
        actual_bytes = tf.extractfile('main.py').read()
    actual = validation / 'packed-main.py'
    actual.write_bytes(actual_bytes)
    assert digest(actual_bytes) == args.expected_sha256
    spec = {'builder':'build_release_round8.py', 'label':args.label,
            'candidate':str(source_path.relative_to(ROOT)).replace('\\', '/'),
            'source_sha256':args.expected_sha256, 'entry_name':args.entry, 'profile':args.profile,
            'archive_sha256':digest(archive.read_bytes()), 'archive_members':list(payloads),
            'trigger_seed':args.trigger_seed, 'default_seed':args.default_seed,
            'promotes_root_entrypoints':False, 'strength_approval':False, 'online_submission':False,
            'V92_SELL_LIB_present':False}
    if args.profile == 'bounded-production':
        spec['v7_prefix_byte_identical'] = source.startswith(v7)
        spec['v7_prefix_text_identical_after_newline_normalization'] = True
        spec['newline_notice'] = 'Frozen candidate uses CRLF; validation preserves its exact frozen bytes. Prior v7 uses LF.'
    write_json(release / 'build-spec.json', spec)
    checkpoint_file = validation / 'official-games.json'
    fixture_path = validation / 'real-observations.jsonl.gz'
    if args.resume and checkpoint_file.exists():
        checkpoint = json.loads(checkpoint_file.read_text(encoding='utf-8'))
        assert checkpoint['source_sha256'] == args.expected_sha256
        assert checkpoint['fixture_sha256'] == digest(fixture_path.read_bytes())
        assert [g['seed'] for g in checkpoint['games']] == [args.trigger_seed, args.default_seed]
        assert checkpoint['observations'] == 1438
    else:
        checkpoint = run_official_games(actual, validation, args.trigger_seed, args.default_seed,
                                        args.entry, args.profile == 'bounded-production')
    parity = []
    child_env = dict(os.environ)
    child_env.pop('V92_SELL_LIB', None)
    for sorted_keys in (False, True):
        label = 'sorted' if sorted_keys else 'original'
        result = subprocess.run([sys.executable, '-I', '-S', '-c', ISOLATED_WORKER,
                                 str(archive), str(fixture_path), args.expected_sha256,
                                 args.entry, str(sorted_keys).lower()],
                                text=True, encoding='utf-8', capture_output=True,
                                timeout=600, env=child_env)
        (validation / f'isolated-{label}-stderr.txt').write_text(result.stderr, encoding='utf-8')
        (validation / f'isolated-{label}-records.jsonl').write_text(result.stdout, encoding='utf-8')
        assert result.returncode == 0, f'Isolated worker failed; see isolated-{label}-stderr.txt'
        assert not result.stderr.strip(), f'Unexpected isolated stderr: isolated-{label}-stderr.txt'
        records = [json.loads(line) for line in result.stdout.splitlines()]
        assert len(records) == 1438, len(records)
        errors = [(i, row['errors']) for i, row in enumerate(records) if row['errors']]
        differences = [i for i, row in enumerate(records) if not row['matches']]
        assert not errors, errors[:10]
        assert not differences, differences[:20]
        maximum = max(row['seconds'] for row in records)
        assert maximum < LIMIT_SECONDS, (label, maximum)
        states = {str(i):row['state'] for i, row in enumerate(records) if row['state'] is not None}
        assert set(states) == {'0', '718', '719', '1437'}, states.keys()
        row = {'sorted_observation_keys':sorted_keys, 'matching_actions':1438,
               'differing_actions':0, 'nonzero_error_fallback_counters':len(errors),
               'entry_name':records[0]['entry_name'], 'max_action_seconds':maximum,
               'source_load_seconds':records[0]['load_seconds'], 'state_snapshots':states,
               'step0_reset_checks':2, 'single_namespace_across_games':True,
               'third_party_packages_disabled':True, 'source_loaded_directly_from_archive':True}
        parity.append(row)
        print(json.dumps({'isolated_parity':label, 'matching_actions':1438,
                          'max_action_seconds':maximum}), flush=True)
    assert digest(source_path.read_bytes()) == args.expected_sha256, 'Source changed during validation'
    report = {**spec, 'technical_acceptance_passed':True, 'strength_approval':False,
              'games':checkpoint['games'], 'isolated_checks':parity,
              'fixture_sha256':checkpoint['fixture_sha256'], 'environment':checkpoint['environment'],
              'step0_state_reset':'Same-player consecutive episodes are action-identical to fresh namespaces; per-player global STATE/STATES and object state/players fingerprints checked against fresh official entries. Known production/seed/fertilizer state also checked when present.',
              'cumulative_statistic_notice':'Inherited ADV front_turns, when present, is a cumulative diagnostic, not reset on step 0; action/state parity is checked independently.',
              'observed_callback_limit_seconds':LIMIT_SECONDS,
              'timing_scope':'Observed on this host and these inputs, not a universal or Kaggle-hardware guarantee.'}
    write_json(release / 'validation.json', report)
    write_json(release / 'manifest.json', {**spec, 'status':'candidate; technical checks passed; strength selection pending',
               'source_bytes':len(source), 'archive_bytes':archive.stat().st_size,
               'source_urls':SOURCES if args.profile == 'bounded-production' else {}, 'license':'See retained full NOTICE/LICENSE and embedded source notices',
               'environment':checkpoint['environment'], 'online_score':None})
    (release / 'README.md').write_text(
        '# Round 8 candidate — not promoted\n\n'
        'This archive passed the bounded technical checks in validation.json. '
        'It has no final strength approval or asserted online rating. The root agent and previous releases are unchanged.\n\n'
        f'Source SHA256: `{args.expected_sha256}`\n\n'
        f'Archive SHA256: `{spec["archive_sha256"]}`\n\n'
        'Validation: two full official games versus v7, 1,438 real observations, '
        'two continuous isolated standard-library-only replays (original and sorted keys), '
        'per-action parity, reset and diagnostic checks. Fixtures and full logs are retained under validation/.\n',
        encoding='utf-8')
    print(json.dumps({'technical_acceptance_passed':True, 'strength_approval':False,
                      'stage':str(release), 'source_sha256':args.expected_sha256,
                      'archive_sha256':spec['archive_sha256']}), flush=True)


if __name__ == '__main__':
    main()
