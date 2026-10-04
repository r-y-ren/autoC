"""SIMV56: the V56-seat observation built from the sim state equals the engine's at step 0,
and the action encoder is the tape encoder."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "S/simv56"))
sys.path.insert(0, str(ROOT / "src"))


def test_initial_obs_matches_engine():
    import v56sim as V
    from kagg3.sim.state import initial_state
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 1})
    env.reset(2)
    # reset() runs the interpreter once, which initialises farms/market (step 0, nothing applied)
    st = initial_state(np)
    a = {k: np.asarray(getattr(st, k)) for k in V.STATE_KEYS}
    for seat in (0, 1):
        eng = dict(env.state[0].observation)
        eng.update(dict(env.state[seat].observation))
        eng["player"] = seat
        ours = json.loads(json.dumps(V.build_obs(a, seat, [])))
        eng = json.loads(json.dumps(eng))
        for k in ("farms", "private", "market", "town", "day", "hour", "step", "player"):
            if k == "step" and k not in eng:
                continue
            assert ours[k] == eng[k], k


def test_encode_tape_rows():
    import v56sim as V
    from kagg3.core import ops as O
    u, m = V.encode({"farmer": ["WATER"], "hands": [["PLANT", "WHEAT"]],
                     "market": [["SELL", "WHEAT", 3], ["HIRE"], ["BAD"]]})
    assert u[0, 0] == O.OP_WATER and u[0, 1] == O.OP_PLANT and u[1, 1] == 0
    assert m[0, 0] == O.MO_SELL and m[2, 0] == 3 and m[0, 1] == O.MO_HIRE and m[0, 2] == O.MO_NONE
    u, m = V.encode(None)
    assert (u[0] == O.OP_PASS).all() and (m[0] == O.MO_NONE).all()
