"""Check the extended own-state simulator against recorded official terminal steps."""
from pathlib import Path
import contextlib,copy,gzip,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
entry=fa.load('research/macro_population_20260927/long_terminal_v2/start700.py');ns=entry.__globals__
checks=[]
for filename in ('public_113814844.json.gz','public_113880752.json.gz'):
    game=json.loads(gzip.decompress((D/filename).read_bytes()))
    for seat in (0,1):
        for step in range(700,719):
            obs=copy.deepcopy(game['steps'][step][seat]['observation']);obs['step']=step;obs['player']=seat
            action=game['steps'][step+1][seat]['action']
            if any(o and o[0]!='SELL' for o in action.get('market',[])):continue
            result=ns['_lt_call']('simulate',obs,game['configuration'],[action],preserve_final_commands=True)
            observed=game['steps'][step+1][seat]['observation']
            expected_farm={k:v for k,v in observed['farms'][seat].items() if k!='money'}
            assert result['farm']==expected_farm,(filename,seat,step,'farm')
            assert result['private']==observed['private'],(filename,seat,step,'inventory')
            checks.append((filename,seat,step))
report=dict(passed=True,official_single_steps=len(checks),episodes=2,market_empty_slots_supported=True,scope='Own physical state and inventory parity; shared market prices are not modeled.')
(D/'long_terminal_v2_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
