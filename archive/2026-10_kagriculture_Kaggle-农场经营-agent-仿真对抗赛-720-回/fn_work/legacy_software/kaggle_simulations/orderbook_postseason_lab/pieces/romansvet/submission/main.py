"""Kaggriculture submission entrypoint.

Weights in theta.npy are the output of OpenAI-ES over a bit-exact JAX
reimplementation of this environment; nothing here is hand-tuned strategy. The
forward pass is pure numpy and runs once per in-game day.

The turn loop itself is NOT written out here: `agent` only builds the macro
observation and hands the turn to `kagg3.agent.runtime.Runtime`, the same class
the repo's own evaluations drive. This file used to carry a hand-copy of
`Runtime.act`, and the copy fell a patch behind the original -- silently, because
the switch that patch serves was off. Delegation makes that class of drift
impossible: there is one act path, and the archive vendors it.
"""

import inspect
import os
import sys

import numpy as np


def _locate():
    """Directory this agent was loaded from.

    kaggle_environments execs the file through `compile(raw, path, "exec")` with a
    bare globals dict, so `__file__` is absent -- but the compiled code object
    keeps the real path, and the loader only puts the agent's directory on
    sys.path for the duration of that exec. Recover it here and keep it.
    """
    cands = []
    try:
        cands.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    fn = inspect.currentframe().f_code.co_filename
    if fn and not fn.startswith("<"):
        cands.append(os.path.dirname(os.path.abspath(fn)))
    cands.append("/kaggle_simulations/agent")
    cands.append(os.getcwd())
    for c in cands:
        if os.path.isfile(os.path.join(c, "theta.npy")):
            return c
    return cands[0]


_HERE = _locate()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from kagg3 import spec
from kagg3.agent import parse, runtime as _runtime
from kagg3.core import brain

_THETA = np.load(os.path.join(_HERE, "theta.npy")).astype(np.float32)

# The residual action head [ACTIONRL]: a 2x64 numpy MLP that may move the
# planner's plant / animal / hire / hold counts inside a fixed clamp, and is
# re-clamped by `plan._residual_override` on the other side. `residual_on()`
# loads the weights lazily on the first planned day, so the import graph here
# is unchanged and this file still imports nothing but numpy.
from kagg3.core import plan as _plan

_plan.RESIDUAL_ON = True
_plan.RESIDUAL_HEAD = os.path.join(_HERE, "residual_head.npz")

_RUNTIMES = {}


def _macro(obs, player, view, prev_mkt_inv):
    opp = obs["farms"][1 - player]
    vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
    po = brain.PolicyObs(
        day=np.int32(view.day), money=view.money,
        opp_money=np.int32(opp["money"]),
        kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
        t_day=view.t_day, t_yield=view.t_yield,
        shed=view.shed, seeds=view.seeds,
        nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
        mkt_inv=parse.parse_market(obs)[0], price=view.price,
        shops=parse.parse_town(obs),
        # Public: every farm's tiles carry planted_day / placed_day and
        # yield_units; only observation["private"] is withheld. Feeds
        # brain.production_forecast's opponent half.
        opp_t_day=vo.t_day, opp_t_yield=vo.t_yield,
        prev_mkt_inv=prev_mkt_inv,
    )
    return brain.decide(np, _THETA, po)


# NOTE: this must remain the LAST callable defined in the module -- the loader
# picks the final callable in the exec namespace as the agent.
def agent(observation, configuration=None):
    # One `Runtime` per seat, exactly as `runtime.make_agent` keeps them; the
    # splice wrapper `make_agent` adds on top is applied by the build instead,
    # so an OFF package never imports `opening`.
    player = observation.get("player", 0)
    rt = _RUNTIMES.get(player)
    if rt is None:
        rt = _RUNTIMES[player] = _runtime.Runtime(_macro, pass_prev_mkt_inv=True)
    return rt.act(observation, configuration)
