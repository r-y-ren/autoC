"""Create a bounded, reproducible macro population without touching releases."""
from pathlib import Path
import hashlib,itertools,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
BASE='submissions/release_v10_r2/main.py'
raw=(R/BASE).read_bytes();assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
space=dict(rotation=['native','feed_first','selective','carrot_growth'],herd=['native','keep','expected','selective'],expansion=['native','none','cautious','growth'],hire_cap=[0,10,12,14],initial_care=[False,True])
default={k:v[0] for k,v in space.items()};genomes=[default]
for key,values in space.items():
    for value in values[1:]:genomes.append(dict(default,**{key:value}))
rng=random.Random(20260927)
while len(genomes)<24:
    g=dict(default)
    for key in rng.sample(list(space),rng.choice([2,3])):g[key]=rng.choice(space[key])
    if g not in genomes:genomes.append(g)
folder=D/'population';folder.mkdir(exist_ok=True)
def build(g):
    tag=hashlib.sha256(json.dumps(g,sort_keys=True).encode()).hexdigest()[:12]
    path=folder/f'macro_{tag}.py'
    data=raw+('\n_MP_GENOME='+repr(g)+'\n').encode()+(D/'policy_tail.py.txt').read_bytes()
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    return dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),genome=g)
if __name__=='__main__':
    variants=[build(g) for g in genomes]
    (D/'population_g1.json').write_text(json.dumps(variants,indent=2))
    (D/'search_space.json').write_text(json.dumps(space,indent=2))
