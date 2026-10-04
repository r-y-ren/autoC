"""mk_k.py out.py 'stmts'  -> R4.2 (cand/h9.py) + constant overrides + fresh entry"""
import sys
out, stmts = sys.argv[1], sys.argv[2]
src = open('cand/h9.py', encoding='utf-8').read() + '\n' + stmts.replace(';', '\n') + '\n\n\ndef kaggle_r5k_final_agent(observation, configuration=None):\n    return hpx_agent(observation, configuration)\n'
open(out, 'w', encoding='utf-8').write(src); print(out)
