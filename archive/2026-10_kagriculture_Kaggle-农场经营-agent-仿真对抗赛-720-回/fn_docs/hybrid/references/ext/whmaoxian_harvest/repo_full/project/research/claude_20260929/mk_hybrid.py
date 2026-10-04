"""Build a hybrid: R2 plays until SWITCH step, then the reactive engine takes over.
usage: mk_hybrid.py out.py switch_step [engine-overrides-dict]"""
import sys

out, switch = sys.argv[1], int(sys.argv[2])
overrides = sys.argv[3] if len(sys.argv) > 3 else "{}"
r2 = open('cand/r2.py', encoding='utf-8').read()
eng = ''.join(open(f'engine/{p}', encoding='utf-8').read() for p in
              ('farm.py', 'p2_plan.py', 'p3_tasks.py', 'p4_units.py', 'p5_market.py', 'p6_blueprint.py'))
assert "'''" not in eng
src = r2 + '\n\n# ---- hybrid wrapper (2026-09-29): R2 opening, reactive engine afterwards\n'
src += "_HY_R2 = kaggle_submission_agent\n"
src += "_HY_ENG_SRC = r'''" + eng + "'''\n"
src += "_HY_ENG = {'__name__': 'hy_engine'}\nexec(compile(_HY_ENG_SRC, 'hy_engine', 'exec'), _HY_ENG)\n"
src += f"_HY_ENG['OVERRIDES'].update({overrides})\n"
src += f"_HY_SWITCH = {switch}\n"
src += '''

def hybrid_agent(observation, configuration=None):
    step = int(observation.get("step", 0) or 0)
    if step < _HY_SWITCH:
        return _HY_R2(observation, configuration)
    try:
        seat = int(observation.get("player", 0) or 0)
        if _HY_ENG["BLUEPRINT"].get(seat) is None or step == _HY_SWITCH:
            try:
                ch = _IMPL.chassis
                route = ch.players.get(seat, {}).get("route")
                tape = ch.routes.get(route) or next(iter(ch.routes.values()))
                end = ch.routes.get(2)
                _HY_ENG["BLUEPRINT"][seat] = _HY_ENG["tape_plantings"](tape, (648, end) if end else None)
                _HY_ENG["OPP_SELLS"][seat] = _HY_ENG["tape_sells"](tape, (648, end) if end else None)
            except Exception:
                _HY_ENG["BLUEPRINT"][seat] = {}
        return _HY_ENG["act"](observation, configuration)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}


hybrid_submission_agent = hybrid_agent
'''
open(out, 'w', encoding='utf-8').write(src)
print(out, len(src))
