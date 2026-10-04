"""Splice a recorded strong opening in front of the planner (off by default).

Every loss autopsy this campaign lands on the same day-10 state: eight hands
and ~4k coins where the top-tier Kaggle seats hold eleven or twelve hands and
~16k.  Hand-written crew ramps lost badly because they were board-blind.  This
module tries the other end of the idea -- replay a *real* strong seat's opening
verbatim for the first `K` days and hand the board to the planner afterwards.

The replay mechanism is `scripts/tape_opponent.py`'s, unchanged: every farm
starts identical (a 10x10 board, NW quadrant empty, three quadrants LOCKED,
farmer at (4, 4)), so a positional tape transfers across seeds; only the town,
the weeds and therefore the prices differ, so a HIRE or BUY that cleared in the
recording may be refused here and the engine drops it silently.  The generated
tape's own `_align` pads or truncates the `hands` list to the live roster,
which is what makes a shortened crew survive rather than invalidate the turn.

Nothing here runs unless `KAGG3_OPENING` is set:

    KAGG3_OPENING="<path to a tape main.py>:<K>"

With the variable unset, `runtime.make_agent` returns exactly the agent it
always returned.

The handover is safe because the planner rebuilds the whole day plan at hour 0
from the live observation.  A momentum-aware `Runtime` does carry dawn market
history, but the splice bypasses that runtime on days `[0, K)`: day `K` is
therefore its first observed dawn and deliberately receives zero market
momentum.  It then sees whatever board the tape left it and starts history from
that observation.
"""

from __future__ import annotations

import inspect
import os

#: Environment variable that turns the splice on: "<main.py path>:<K days>".
ENV_VAR = "KAGG3_OPENING"


def _callable_1arg(fn):
    """Adapt a tape's `agent` to a one-argument call.

    Generated tapes take `(observation, configuration=None)`, kagg2's packaged
    main takes `(obs)` alone; both are handed only the observation here.
    """
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):  # builtins / C callables
        return fn
    required = [p for p in params.values()
                if p.default is inspect.Parameter.empty
                and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    if len(required) >= 2:
        return lambda obs: fn(obs, None)
    return fn


def load_tape(main_py_path):
    """Exec a packaged tape `main.py` and return its `agent`, one-arg adapted.

    `exec` rather than `import`, because that is how `kaggle_environments`
    loads a file agent: the module image the engine sees is the one this
    check exercises, and a tape main is a leaf file with no relative imports.
    """
    path = os.path.abspath(main_py_path)
    with open(path) as fh:
        source = fh.read()
    ns = {"__name__": "kagg3_opening_tape", "__file__": path}
    exec(compile(source, path, "exec"), ns)  # noqa: S102
    fn = ns.get("agent")
    if not callable(fn):
        raise ValueError(f"{path} defines no callable `agent`")
    return _callable_1arg(fn)


class OpeningSplice:
    """Tape for days `[0, k)`, then `runtime_agent` for the rest of the game."""

    def __init__(self, runtime_agent, tape_agent, k):
        self.runtime_agent = runtime_agent
        self.tape_agent = tape_agent
        self.k = int(k)

    def __call__(self, obs, config=None):
        if int(obs.get("day", 0) or 0) < self.k:
            return self.tape_agent(obs)
        return self.runtime_agent(obs, config)


def parse_spec(spec):
    """`"<path>:<K>"` -> `(path, K)`. Rightmost colon, so paths may contain one."""
    path, _, days = str(spec).rpartition(":")
    if not path or not days.strip().lstrip("+-").isdigit():
        raise ValueError(f"{ENV_VAR} must look like '<tape main.py>:<K>', got {spec!r}")
    return path, int(days)


def from_env(runtime_agent, spec=None):
    """Wrap `runtime_agent` if `KAGG3_OPENING` names a tape; else hand it back."""
    spec = os.environ.get(ENV_VAR) if spec is None else spec
    if not spec:
        return runtime_agent
    path, k = parse_spec(spec)
    if k <= 0:
        return runtime_agent
    return OpeningSplice(runtime_agent, load_tape(path), k)
