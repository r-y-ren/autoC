"""mk_hold2.py out.py base.py parent_name key=val ..."""
import sys
out,base,parent=sys.argv[1],sys.argv[2],sys.argv[3]
kv={}
for a in sys.argv[4:]:
    k,v=a.split('=',1);kv[k]=eval(v)
src=open(base,encoding='utf-8').read()+'\n'+open('hold_layer.py',encoding='utf-8').read().replace('_H_PARENT = agent','_H_PARENT = '+parent)
if kv: src+=f'\n_H_CFG.update({kv!r})\n'
src+='\n\ndef kaggle_hold2_final_agent(observation, configuration=None):\n    return hold_agent(observation, configuration)\n'
open(out,'w',encoding='utf-8').write(src);print(out)
