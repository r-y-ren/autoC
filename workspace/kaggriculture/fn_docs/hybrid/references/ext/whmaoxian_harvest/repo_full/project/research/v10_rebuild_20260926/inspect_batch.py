from pathlib import Path
import argparse,collections,json,statistics
p=argparse.ArgumentParser();p.add_argument('path');a=p.parse_args()
rows=[json.loads(line) for line in Path(a.path).read_text(encoding='utf-8').splitlines()]
groups=collections.defaultdict(list)
for row in rows:groups[(row['candidate'],row.get('panel'))].append(row)
for (name,panel),group in groups.items():
    good=[r for r in group if r.get('valid')]
    print(Path(name).parent.name+'/'+Path(name).name,panel,len(group),
        'W/T/L',sum(r['margin']>0 for r in good),sum(r['margin']==0 for r in good),sum(r['margin']<0 for r in good),
        'margin',round(statistics.mean(r['margin'] for r in good),1) if good else None,'invalid',len(group)-len(good),flush=True)
print('Complete records',len(rows),flush=True)
