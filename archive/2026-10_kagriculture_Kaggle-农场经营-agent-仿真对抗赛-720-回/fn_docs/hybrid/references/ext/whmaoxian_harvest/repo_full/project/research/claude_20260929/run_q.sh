cd /c/Users/ASUS/Documents/ChatGPT/kaggriculture/research/claude_20260929
for P in 39 41; do sed "s/if px >= 40:/if px >= $P:/" cand/p40.py > cand/p$P.py; grep -c "px >= $P" cand/p$P.py; done
for P in 39 41; do
python - <<EOF
src=open('cand/p$P.py',encoding='utf-8').read()+'\n'+open('hp_layer.py',encoding='utf-8').read()
src+="\n_HPX_CFG.update(dict(items={'FERTILIZER':(50,5)}))\n\n\ndef kaggle_hpx2_final_agent(observation, configuration=None):\n    return hpx_agent(observation, configuration)\n"
open('cand/q$P.py','w',encoding='utf-8').write(src)
EOF
done
cat all195.txt fresh.txt | tr -d '\r' > all244.txt
../../.venv/Scripts/python.exe surrogate.py MauoXX 30 cand/q39.py cand/q41.py -- $(cat all244.txt) > results/sur_q.txt 2>&1
tail -3 results/sur_q.txt
python - <<'EOF'
import json,collections
eps=set(int(l) for l in open('all244.txt'))
rs=[json.loads(l) for l in open('results/surrogate.jsonl')]
t=collections.defaultdict(dict)
for r in rs:
    if 'me' in r and r['ep'] in eps: t[r['cand']][r['ep']]=r['me']-r['op']
for c in ('cand/r2.py','cand/combo2.py','cand/k24.py','cand/p40.py','cand/h9.py','cand/q39.py','cand/q41.py'):
    v=t[c]; print(c,len(v),'W',sum(x>0 for x in v.values()),'L',sum(x<0 for x in v.values()),'mean',round(sum(v.values())/max(1,len(v))))
EOF
