"""mk_cfg.py out.py base.py 'python statements'  -> base + statements + fresh final entry wrapping endx_agent"""
import sys
out,base,stmts=sys.argv[1],sys.argv[2],sys.argv[3]
src=open(base,encoding='utf-8').read()+'\n'+stmts.replace(';','\n')+'\n\n\ndef kaggle_cfg_final_agent(observation, configuration=None):\n    return endx_agent(observation, configuration)\n'
open(out,'w',encoding='utf-8').write(src);print(out)
