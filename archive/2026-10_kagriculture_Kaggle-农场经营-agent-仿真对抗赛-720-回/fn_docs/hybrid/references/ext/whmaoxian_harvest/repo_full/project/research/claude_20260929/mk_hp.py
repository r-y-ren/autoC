"""mk_hp.py out.py 'cfg-dict-literal'  -> p40 + high-price layer with _HPX_CFG.update(cfg)"""
import sys
out, cfg = sys.argv[1], sys.argv[2]
src = open('cand/p40.py', encoding='utf-8').read() + '\n' + open('hp_layer.py', encoding='utf-8').read()
src = src.replace('_HPX_CFG = dict(', '_HPX_CFG = dict(**' + cfg + ') if False else dict(', 1) if False else src
src += f'\n_HPX_CFG.update({cfg})\n\n\ndef kaggle_hpx2_final_agent(observation, configuration=None):\n    return hpx_agent(observation, configuration)\n'
open(out, 'w', encoding='utf-8').write(src)
print(out)
