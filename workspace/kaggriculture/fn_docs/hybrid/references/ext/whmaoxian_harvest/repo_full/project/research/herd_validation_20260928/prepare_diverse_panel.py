"""Source-reviewed public baselines and a bounded JIT ablation, all development."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];P=D/'new_public_sources'
sha=lambda b:hashlib.sha256(b).hexdigest()
def freeze(name,data):
    p=D/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    return dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data))
salem=(P/'Salem_Ali_inspected.py').read_bytes()
assert sha(salem)=='d39dba50793d9777c990347443bf0c481c78adaea86055f6f6b0600dcfcd9f2e'
assert salem.count(b'    except Exception:\n')==1
instrumented=b"_NP28_REPORT={'errors':0}\n"+salem.replace(b'    except Exception:\n',b"    except Exception:\n        _NP28_REPORT['errors']+=1\n")
instrumented+=b'\n_MP_REPORT=_NP28_REPORT\n'
salem_v=freeze('salem_checked',instrumented)
q45=(P/'prvsiyan_inspected.py').read_bytes();assert sha(q45)=='7aacd7233e5113e41024db0ff85912ab13cbd164e85ed5438af17df25a85b287'
q45_v=freeze('q45_public',q45)
qnet=q45+b"\nassert _ACTIONS[0]['market']==[['BUY_PRODUCT','WHEAT',45]]\nassert _ACTIONS[1]['market'][0]==['SELL','WHEAT',40]\n_ACTIONS[0]['market']=[['BUY_PRODUCT','WHEAT',5]]\n_ACTIONS[1]['market']=_ACTIONS[1]['market'][1:]\n"
qnet_v=freeze('qnet5_experiment',qnet)
jit=next(v for v in json.loads((D/'jit_candidates.json').read_text()) if v['name']=='jit_herd_100')
jitraw=(R/jit['path']).read_bytes();assert sha(jitraw)==jit['sha256']
cap_v=freeze('jit_one',jitraw+b'\n_HG28_CFG=dict(_HG28_CFG,max_swaps=1)\n')
spec=json.loads((D/'herd_extended_design.json').read_text())
variants=[spec['variants'][0],next(v for v in spec['variants'] if v['name']=='yarn_nomilk'),cap_v,salem_v,q45_v,qnet_v]
roster=spec['roster']+[dict(path=salem_v['path'],family='salem_route_mixture',panel='new_lineage_program'),dict(path=q45_v['path'],family='q45_fixed_public',panel='fixed_public_program')]
seeds=[1799657451]+spec['seeds'][:3]
jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('diverse_jobs.json',jobs),('diverse_design.json',dict(variants=variants,roster=roster,seeds=seeds,scope='Development. Salem contains reactive guards and two routes; Q45 is a published fixed-route control, not an independent top-ten program.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
(D/'PUBLIC_SOURCE_NOTICE.md').write_text('Public source credits: Salem Ali, salemali7/harvest-kaggriculture; prvsiyan, prvsiyan/where-the-wheat-remembers-tomorrow-kaggriculture. Sources retrieved through public Kaggle kernel APIs, metadata and hashes in new_public_sources/receipts.json. Notebook cells were not executed. AGENT_B64 was literal-extracted and decoded for source review. Salem evaluation adds only an exception counter; Q45 is literal public code. Qnet5 independently changes two opening orders. Public titles and authors\' reported scores are not verified ratings of these local files.\n',encoding='utf-8')
print(json.dumps(dict(cases=len(jobs),variants=len(variants),opponents=len(roster))),flush=True)
