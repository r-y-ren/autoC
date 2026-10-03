"""Full-action equivalence, reset, key-order and official file-loader checks.

The known development worlds are technical fixtures, not new rating evidence.
"""
import argparse
import contextlib
import gc
import gzip
import hashlib
import io
import json
from pathlib import Path
import time
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2'
OLD=ROOT/'experiments/round8_top2_dsm_strict.py'
NEW=ROOT/'experiments/round8_top2_dsm_compact.py'
OPP=ROOT/'submissions/release_v7/main.py'


def load(path):
    return get_last_callable(path.read_text(encoding='utf-8'),path=str(path))


def fingerprint(actions):
    return hashlib.sha256(json.dumps(actions,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def assert_clean(entry):
    assert not any(entry.telemetry.values()),entry.telemetry


def equivalent():
    old,new=load(OLD),load(NEW)
    games=[]
    total=0
    for seed,seat in ((82001,0),(82003,1)):
        records=[]
        fresh=load(NEW)
        def compare(obs,config=None):
            a=old(obs,config); b=new(obs,config); c=fresh(obs,config)
            assert a==b==c,('action mismatch',seed,seat,obs['step'],a,b,c)
            records.append({'observation':json.loads(json.dumps(obs)),'action':a})
            return b
        env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
        entries=[compare,str(OPP)]
        if seat:
            entries.reverse()
        env.run(entries)
        assert [s.status for s in env.steps[-1]]==['DONE','DONE']
        assert len(env.steps)==720 and len(records)==719
        assert not [x.get('stderr') for logs in env.logs for x in logs if x.get('stderr')]
        for f in (old,new,fresh):assert_clean(f)
        dest=OUT/f'compact_equivalence_seed{seed}_seat{seat}.json.gz'
        dest.write_bytes(gzip.compress(json.dumps(records,separators=(',',':')).encode()))
        games.append({'seed':seed,'seat':seat,'actions':719,'action_sha256':fingerprint([r['action'] for r in records]),'fixture':dest.name,'rewards':[s.reward for s in env.steps[-1]],'old_compact_fresh_compact_equal':True})
        total+=len(records)
        print('equivalent full game',seed,seat,len(records),flush=True)
        del env,records,entries,fresh
        gc.collect()
    del old,new
    gc.collect()
    modes=[]
    for sorted_keys in (False,True):
        # Each pair of entries persists across BOTH matches to test reset.
        old,new=load(OLD),load(NEW)
        checked=0; reference_matches=0
        for game in games:
            records=json.loads(gzip.decompress((OUT/game['fixture']).read_bytes()))
            for index,record in enumerate(records):
                obs=json.loads(json.dumps(record['observation'],sort_keys=sorted_keys))
                a=old(obs); b=new(obs)
                assert a==b,('key order mismatch',sorted_keys,game['seed'],index)
                reference_matches+=a==record['action']
                checked+=1
            del records
        assert checked==1438
        assert_clean(old);assert_clean(new)
        modes.append({'sorted_keys':sorted_keys,'actions_compared':checked,'source_compact_equal':True,'same_as_environment_recorded_actions':reference_matches,'reset_across_two_games':True})
        print('key-order mode',sorted_keys,checked,'reference matches',reference_matches,flush=True)
        del old,new
        gc.collect()
    report={'source_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),'compact_sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),'games':games,'continuous_live_actions_equal':total,'key_order_modes':modes,'note':'Engineering equivalence on known development worlds; not independent strategy validation.'}
    (OUT/'compact_equivalence.json').write_text(json.dumps(report,indent=2),encoding='utf-8')


def cold():
    # Deliberately pass the file path: compile/decompression happens inside the
    # official agent's first callback and is included in its duration log.
    env=make('kaggriculture',configuration={'seed':82005,'episodeSteps':720},debug=True)
    env.run([str(NEW),str(OPP)])
    logs=[row[0] for row in env.logs if row and isinstance(row[0],dict)]
    stderr=[x.get('stderr') for row in env.logs for x in row if x.get('stderr')]
    assert [s.status for s in env.steps[-1]]==['DONE','DONE'] and len(env.steps)==720 and not stderr
    first=logs[0]['duration']; maximum=max(row.get('duration',0) for row in logs)
    result={'compact_sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),'loader':'official file path; compile and embedded-data decompression charged to first callback','seed':82005,'first_action_seconds':first,'max_action_seconds':maximum,'act_timeout':env.configuration.actTimeout,'statuses':[s.status for s in env.steps[-1]],'states':len(env.steps),'stderr':stderr,'rewards':[s.reward for s in env.steps[-1]]}
    (OUT/'compact_cold_load.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
    assert first<1.0,('first callback exceeds competition base limit',first)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cold',action='store_true');a=p.parse_args()
    cold() if a.cold else equivalent()
