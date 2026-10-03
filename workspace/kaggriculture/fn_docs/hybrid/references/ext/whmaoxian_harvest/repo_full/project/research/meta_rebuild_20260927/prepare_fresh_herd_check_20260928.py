"""Lock two challengers before drawing a new unfiltered evaluation panel."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((R/BASE).read_bytes())=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants=[]
for name,p in [('r2',R/BASE),('g3_robust',D/'candidates/g3_robust.py'),('h4_ripe',D/'candidates/h4_ripe.py')]:
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes())))
lock=dict(locked_utc=datetime.now(timezone.utc).isoformat(),variants=variants,scope='Source lock before new world generation. No further changes to these source paths.',acceptance='Check whole-world paired score-rate uncertainty, both seats, each opponent, errors and plan breaks. This panel cannot establish an online rating by itself.')
p=D/'fresh_herd_check_20260928_lock.json';assert not p.exists();p.write_text(json.dumps(lock,indent=2))
prior=json.loads((D/'repeat_screen_20260928_design.json').read_text());seen={r['seed'] for r in prior['inspected_initial_worlds']}
seen.update(json.loads((D/'herd_extended_20260928_design.json').read_text())['seeds']);seen.add(1799657451)
rng=random.Random(202609281430);seeds=[]
while len(seeds)<32:
    seed=rng.randrange(1,2147483647)
    if seed not in seen and seed not in seeds:seeds.append(seed)
roster=json.loads((D/'herd_g3_20260928_design.json').read_text())['roster']
proxies=json.loads((R/'research/v10_top10_20260926/study_opponents.json').read_text())
for op in proxies:
    if op['family']=='top_style_05':roster.append(dict(path=op['path'],family=op['family'],panel='reserved_responsive_proxy'))
jobs=[]
