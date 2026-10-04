"""A bounded, fixed-count loop the planner can run on either backend.

numpy runs a Python loop. The simulator installs `jax.lax.fori_loop` through
`install` when it is imported (see sim/rollout.py), so a body that runs a
hundred times compiles once instead of being unrolled a hundred times inside
the day scan. `core` itself never imports jax: the submission's
forbidden-import gate parses every shipped file for import statements, and
the numpy path must stay numpy even when the simulator is loaded in the same
process (the equivalence tests do exactly that).
"""

from __future__ import annotations

import numpy as np

_impl = None


def install(fn):
    """`fn(n_iter, body, carry) -> carry`, a traced loop for non-numpy backends."""
    global _impl
    _impl = fn


def repeat(xp, n_iter, body, carry):
    """`carry = body(carry)` repeated `n_iter` times."""
    if _impl is None or xp is np:
        for _ in range(n_iter):
            carry = body(carry)
        return carry
    return _impl(n_iter, body, carry)
