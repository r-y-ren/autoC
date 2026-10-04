"""Compare policies on identical opponent bytes and paired world/seat cases."""
import argparse
import json
import random
import statistics
from pathlib import Path


def read(paths):
    result={}
    for p in paths:
        for line in Path(p).with_suffix('.jsonl').read_text(encoding='utf-8').splitlines():
            r=json.loads(line)
            key=(r['seed'],r['seat'],r['opponent_sha256'])
            if key in result:
                assert result[key]['candidate_sha256']==r['candidate_sha256']
                assert result[key].get('delta')==r.get('delta')
            result[key]=r
    return result


def compare(base,cand, familywise_candidates=1):
    assert isinstance(familywise_candidates, int) and familywise_candidates >= 1
    shared=base.keys()&cand.keys()
    pairs=[]
    for k in sorted(shared):
        a,b=base[k],cand[k]
        if not a['valid'] or not b['valid']:continue
        pairs.append({'seed':k[0],'seat':k[1],'opponent':b['opponent'],
                      'base_margin':a['delta'],'new_margin':b['delta'],
                      'margin_change':b['delta']-a['delta'],
                      'own_cash_change':b['money']-a['money'],
                      'points_change':b['points']-a['points']})
    worlds={}
    for p in pairs:worlds.setdefault(p['seed'],[]).append(p)
    rng=random.Random(20260922)
    metrics={}
    for name in ['margin_change','own_cash_change','points_change']:
        vals=[statistics.mean(r[name] for r in w) for w in worlds.values()]
        samples=sorted(statistics.mean(rng.choices(vals,k=len(vals))) for _ in range(10000)) if vals else []
        metrics[name]={'mean':statistics.mean(vals) if vals else None,
                       'world_bootstrap_95':[samples[250],samples[9749]] if samples else None,
                       'world_bootstrap_familywise_95': [samples[int(250/familywise_candidates)], samples[9999-int(250/familywise_candidates)]] if samples else None,
                       'median_world':statistics.median(vals) if vals else None}
    opponents={}
    for opp in sorted({p['opponent'] for p in pairs}):
        ps=[p for p in pairs if p['opponent']==opp]
        opponents[opp]={'paired_games':len(ps),'margin_change':statistics.mean(p['margin_change'] for p in ps),
                        'points_change':statistics.mean(p['points_change'] for p in ps),
                        'new_wins':sum(p['new_margin']>0 for p in ps),'base_wins':sum(p['base_margin']>0 for p in ps),
                        'improved':sum(p['margin_change']>0 for p in ps),'worse':sum(p['margin_change']<0 for p in ps)}
    return {'paired_games':len(pairs),'worlds':len(worlds),'familywise_candidates':familywise_candidates,'base_unmatched':len(base)-len(shared),'candidate_unmatched':len(cand)-len(shared),
            'invalid_pairs':len(shared)-len(pairs),'metrics':metrics,'opponents':opponents,
            'worst_pairs':sorted(pairs,key=lambda p:p['margin_change'])[:12],
            'best_pairs':sorted(pairs,key=lambda p:p['margin_change'],reverse=True)[:12]}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',nargs='+',required=True);p.add_argument('--candidate',nargs='+',required=True);p.add_argument('--output',required=True)
    p.add_argument('--familywise-candidates',type=int,default=1)
    a=p.parse_args();r=compare(read(a.baseline),read(a.candidate),a.familywise_candidates);Path(a.output).write_text(json.dumps(r,indent=2),encoding='utf-8')
    print(json.dumps({k:r[k] for k in ['paired_games','worlds','invalid_pairs','metrics','opponents']},indent=2))
