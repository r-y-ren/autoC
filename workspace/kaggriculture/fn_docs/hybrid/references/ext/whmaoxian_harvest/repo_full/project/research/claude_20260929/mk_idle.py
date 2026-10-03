import sys
out=sys.argv[1]; kv=sys.argv[2] if len(sys.argv)>2 else '{}'
src=open('cand/r2.py',encoding='utf-8').read()+'\n'+open('idle_layer.py',encoding='utf-8').read()+f'\n_IDF_CFG.update({kv})\n'
open(out,'w',encoding='utf-8').write(src);print(out)
