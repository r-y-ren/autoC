"""mk_ord.py out.py base.py key=val ..."""
import sys
out,base=sys.argv[1],sys.argv[2]
kv={}
for a in sys.argv[3:]:
    k,v=a.split('=',1);kv[k]=eval(v)
src=open(base,encoding='utf-8').read()+'\n'+open('order_layer.py',encoding='utf-8').read()
if kv: src+=f'\n_ORDX_CFG.update({kv!r})\n'
src+='\n\ndef kaggle_ordx_final_agent(observation, configuration=None):\n    return ordx_agent(observation, configuration)\n'
open(out,'w',encoding='utf-8').write(src);print(out)
