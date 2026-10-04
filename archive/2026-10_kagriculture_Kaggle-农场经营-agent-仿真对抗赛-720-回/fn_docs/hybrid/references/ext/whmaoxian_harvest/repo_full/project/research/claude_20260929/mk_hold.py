"""mk_hold.py out.py base.py key=val ..."""
import sys
out,base=sys.argv[1],sys.argv[2]
kv={}
for a in sys.argv[3:]:
    k,v=a.split('=');kv[k]=eval(v)
src=open(base,encoding='utf-8').read()+'\n'+open('hold_layer.py',encoding='utf-8').read()
if kv: src+=f'\n_H_CFG.update({kv!r})\n'
open(out,'w',encoding='utf-8').write(src);print(out)
