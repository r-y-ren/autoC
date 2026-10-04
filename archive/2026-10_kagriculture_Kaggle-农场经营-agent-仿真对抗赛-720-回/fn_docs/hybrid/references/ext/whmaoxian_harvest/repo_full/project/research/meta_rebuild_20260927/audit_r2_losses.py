"""Reproduce recent public R2 losses and inspect execution without changing agents."""
from pathlib import Path
import contextlib,copy,gzip,hashlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1];O=D/'r2_feedback'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
source='submissions/release_v10_r2/main.py';expected='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert hashlib.sha256((R/source).read_bytes()).hexdigest()==expected
reports=[]
for row in json.loads((O/'selection.json').read_text()):
    game=json.loads(gzip.decompress((O/f"{row['episode']}.json.gz").read_bytes()));seat=row['seat'];entry=fa.load(source)
    differences=[];matched=0;daily=[];failed={};commands_total={}
    for step in range(719):
        obs=copy.deepcopy(game['steps'][step][seat]['observation']);obs['step']=step
        recorded=game['steps'][step+1][seat]['action'];actual=entry(copy.deepcopy(obs),game['configuration'])
        if actual==recorded:matched+=1
        elif len(differences)<10:differences.append(dict(step=step,actual=actual,recorded=recorded))
        farm=copy.deepcopy(obs['farms'][seat]);private=copy.deepcopy(obs['private'])
        units=[recorded.get('farmer') or ['PASS']]+list(recorded.get('hands',[]))
        for actor,command in enumerate(units[:len(farm['hands'])+1]):
            op=command[0] if command else 'PASS';commands_total[op]=commands_total.get(op,0)+1
            before=copy.deepcopy((farm,private))
            fa.engine._apply_unit_action(farm,private,actor,command,10,step//24,24,100)
            if (farm,private)==before and op not in ('PASS','NORTH','SOUTH','EAST','WEST'):
                failed[op]=failed.get(op,0)+1
        if step%24==23 or step==718:
            farms=game['steps'][step+1][seat]['observation']['farms'];daily.append(dict(step=step+1,cash=[f['money'] for f in farms],margin=farms[seat]['money']-farms[1-seat]['money']))
    ns=entry.__globals__;diagnostics=fa.diagnostics(entry)
    selected_reports={k:copy.deepcopy(ns.get(k,{})) for k in ('_T19_REPORT','_V219_REPORT','_CXTB_REPORT','_CS_REPORT','_HD2_REPORT','_CA_REPORT','_UPGRADE_STATS','_ALT_REPORT','_CL_REPORT')}
    snapshots=[]
    for step in (144,240,360,480,600,719):
        obs=game['steps'][step][seat]['observation'];farms=[]
        for f in obs['farms']:
            mix={}
            for tiles in f['tiles']:
                for t in tiles:
                    if isinstance(t,dict):
                        name=t.get('animal') or t.get('crop') or t.get('kind');mix[name]=mix.get(name,0)+1
            farms.append(dict(cash=f['money'],land=f['unlocked_quadrants'],mix=mix))
        snapshots.append(dict(step=step,farms=farms,own_shed=obs['private']['shed']))
    result=dict(row,matched=matched,total=719,differences=differences,nonzero_error_diagnostics=diagnostics,daily=daily,failed_physical_actions=failed,physical_action_totals=commands_total,controller_reports=selected_reports,snapshots=snapshots)
    reports.append(result)
    (O/'execution_audit.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    print(json.dumps(dict(episode=row['episode'],margin=row['margin'],matched=matched,errors=diagnostics,failed_actions=failed,reports=selected_reports,daily_margins=[r['margin'] for r in daily],last_farms=snapshots[-1]['farms'])),flush=True)
