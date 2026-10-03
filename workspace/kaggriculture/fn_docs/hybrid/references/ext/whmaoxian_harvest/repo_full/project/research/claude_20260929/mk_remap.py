"""mk_remap.py out.py 'dict-literal {table_route: new_route}' [base]  -> base + router remap (days 6-26) + fresh entry"""
import sys
out, mp = sys.argv[1], sys.argv[2]
base = sys.argv[3] if len(sys.argv) > 3 else 'cand/h9.py'
extra = f'''
_RMX_MAP = {mp}
_RMX_ORIG = _IMPL.chassis.router
def _rmx_router(observation, step, state):
    r = _RMX_ORIG(observation, step, state)
    if 144 <= int(step) < 648 and r in _RMX_MAP:
        return _RMX_MAP[r]
    return r
_IMPL.chassis.router = _rmx_router


def kaggle_rmx_final_agent(observation, configuration=None):
    return hpx_agent(observation, configuration)
'''
open(out, 'w', encoding='utf-8').write(open(base, encoding='utf-8').read() + '\n' + extra)
print(out)
