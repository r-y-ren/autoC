"""mk_h.py out.py wheat_gate margin 'fert-items-dict' [extra stmts]  -> R3 + guard(margin, gate) + hp layer"""
import sys
out, gate, margin, items = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
extra = sys.argv[5] if len(sys.argv) > 5 else ''
patch = f'''
_NGTX_CFG.update(hours=tuple(range(0,24)),margin={margin},order=('WHEAT','FERTILIZER'))
_NGTX_ORIG = _ngtx_apply
def _ngtx_apply(obs, action):
    out = _NGTX_ORIG(obs, action)
    try:
        if out is action or int(obs.get('step', 0)) % 24 in (22, 23):
            return out
        px = int(((obs.get('market') or {{}}).get('prices') or {{}}).get('WHEAT', 0))
        if px >= {gate}:
            return out
        base = [list(o) for o in (action.get('market') or []) if isinstance(o, list) and o]
        extra = [o for o in out['market'][len(base):] if o[1] != 'WHEAT']
        if not extra:
            return action
        out = dict(out)
        out['market'] = base + extra
        return out
    except Exception:
        return out
def kaggle_cfg_final_agent(observation, configuration=None):
    return endx_agent(observation, configuration)
'''
src = open('cand/combo2.py', encoding='utf-8').read() + '\n' + patch + '\n' + open('hp_layer.py', encoding='utf-8').read()
src += f"\n_HPX_CFG.update(dict(items={items}))\n{extra}\n\n\ndef kaggle_hpx2_final_agent(observation, configuration=None):\n    return hpx_agent(observation, configuration)\n"
open(out, 'w', encoding='utf-8').write(src)
print(out)
