from pathlib import Path
import ast,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
load=lambda name:[json.loads(line) for line in (OUT/name).read_text(encoding='utf-8').splitlines()]
a=load('opening_results.jsonl');b=load('generation2_results.jsonl')
key=lambda r:(r['candidate'],r['opponent'],r['seed'],r['seat'])
index={key(r):r for r in a};different=[]
for row in b:
    prior=index.get(key(row))
    if prior and (prior['money']!=row['money'] or prior['action_hash']!=row['action_hash']):
        different.append(dict(candidate=row['candidate'],opponent=row['opponent'],seed=row['seed'],seat=row['seat'],
            first_money=prior['money'],second_money=row['money'],same_shops=prior['shops']==row['shops'],
            first_checkpoints=prior.get('checkpoints'),second_checkpoints=row.get('checkpoints')))
(OUT/'repeatability_differences.json').write_text(json.dumps(different,indent=2),encoding='utf-8')
print('Repeated-case differences',len(different),flush=True)
for row in different:print({k:v for k,v in row.items() if 'checkpoints' not in k},flush=True)
text=(ROOT/'submissions/release_v10/main.py').read_text(encoding='utf-8')
for n in ast.walk(ast.parse(text)):
    if isinstance(n,ast.Constant) and isinstance(n.value,str) and 'perf_counter' in n.value:
        lines=n.value.splitlines()
        for i,line in enumerate(lines):
            if any(word in line for word in ('perf_counter','deadline','time_budget')):
                print('embedded timer',i,'\n'.join(lines[max(0,i-2):i+4]),flush=True)
