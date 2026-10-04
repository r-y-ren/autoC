import sys
out=sys.argv[1]; kv=sys.argv[2] if len(sys.argv)>2 else '{}'
src=open('cand/r2.py',encoding='utf-8').read()+'\n'+open('care_layer.py',encoding='utf-8').read()+f'\n_CRX_CFG.update({kv})\n'
open(out,'w',encoding='utf-8').write(src);print(out)
