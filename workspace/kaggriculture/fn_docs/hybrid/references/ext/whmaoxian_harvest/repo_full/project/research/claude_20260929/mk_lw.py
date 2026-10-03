"""mk_lw.py out.py base.py 'cfg-dict'  -> base (R4.x, entry kaggle_hpx2_final_agent) + low-wheat layer"""
import sys
out, base, cfg = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(base, encoding='utf-8').read() + '\n' + open('lowwheat_layer.py', encoding='utf-8').read()
src += f'\n_LWX_CFG.update({cfg})\n\n\ndef kaggle_lwx_final_agent(observation, configuration=None):\n    return lwx_agent(observation, configuration)\n'
open(out, 'w', encoding='utf-8').write(src)
print(out)
