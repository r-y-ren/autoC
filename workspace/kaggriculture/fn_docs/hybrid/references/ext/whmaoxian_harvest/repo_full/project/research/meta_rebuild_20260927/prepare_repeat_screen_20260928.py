"""Declare demand-stratified DEVELOPMENT fixtures before inspecting their outcomes."""
from pathlib import Path
import contextlib,copy,hashlib,io,json,random,sys
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
sha=lambda b:hashlib.sha256(b).hexdigest()
def first_shops(seed):
    agents=[fa.load(BASE),fa.load(BASE)];state,env=fa.new_game(seed)
    for step in range(144):
        for i in (0,1):
            state[i].observation.step=step
            state[i].action=agents[i](copy.deepcopy(state[i].observation),env.configuration)
        fa.engine.interpreter(state,env)
    return list(state[0].observation.town['unlocked_shops'])

if __name__=='__main__':
    design_path=D/'repeat_screen_20260928_design.json'
    assert not design_path.exists(),'Screen already prepared; preserve declared design.'
    pool=random.Random(202609281217).sample(range(1,2147483647),96)
    selected=[];inspected=[];counts={True:0,False:0}
    for seed in pool:
        shops=first_shops(seed);flag='YARN_STORE' in shops
        inspected.append(dict(seed=seed,shops=shops))
        if counts[flag]<(6 if flag else 2):selected.append(seed);counts[flag]+=1
        if counts=={True:6,False:2}:break
    assert len(selected)==8,(counts,inspected)
    variants=json.loads((D/'repeat_v2_design_20260928.json').read_text())['variants']
    variants=[v for v in variants if v['name']!='repeat_v2_repair']
    for v in variants:
        if v['name']=='repeat_v2_care':
            data=(R/v['path']).read_bytes()+b'\n_MP_REPORT=_K28S_REPORT\n'
            p=D/'candidates/repeat_v2_care_audited.py';assert not p.exists();p.write_bytes(data)
            v.update(name='repeat_v2_care_audited',path=p.relative_to(R).as_posix(),sha256=sha(data))
    for name,p in [('r2',R/BASE),('care_only',D/'candidates/late_care.py')]:
        variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes())))
    roster=json.loads((D/'midgame_herd_design.json').read_text())['roster']
    proxies=json.loads((R/'research/v10_top10_20260926/study_opponents.json').read_text())
    for op in proxies:
        if op['family'] in ('top_style_01','top_style_04'):
            roster.append(dict(path=op['path'],family=op['family'],panel='responsive_proxy'))
    jobs=[]
    for seed in selected:
        for op in roster:
            for v in variants:
                for seat in (0,1):
                    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
    record=dict(variants=variants,roster=roster,seeds=selected,inspected_initial_worlds=inspected,cases=len(jobs),scope='DEVELOPMENT: six Yarn worlds and two non-Yarn controls, selected by R2-prefix shop observations only. No outcome-based world selection. Not representative rating evaluation.')
    design_path.write_text(json.dumps(record,indent=2));(D/'repeat_screen_20260928_jobs.json').write_text(json.dumps(jobs,indent=2))
    print(json.dumps(dict(cases=len(jobs),worlds=len(selected),inspected=len(inspected),selected=[r for r in inspected if r['seed'] in selected])),flush=True)
    runner=(D/'league_live_20260928.py').read_text()
    marker="if __name__=='__main__':";assert runner.count(marker)==1
    runner=runner.replace(marker,(D/'paired_report_20260928.txt').read_text()+'\n'+marker)
    marker='groups=score(rows))';assert runner.count(marker)==1
    runner=runner.replace(marker,'groups=score(rows),paired=paired_report(rows))')
    output_runner=D/'league_paired_20260928.py';compile(runner,str(output_runner),'exec')
    if output_runner.exists():assert output_runner.read_text()==runner
    else:output_runner.write_text(runner)
