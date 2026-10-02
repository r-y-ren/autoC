"""Pin JAX float32 matmuls to true float32, without importing JAX.

On Ampere and later, XLA lowers a float32 matmul to TF32 tensor cores by
default. TF32 keeps 10 mantissa bits, so the policy's forward pass lands
~3.5e-3 away from the same weights evaluated in numpy -- measured on this
network, `default` precision gives |jax - numpy| = 3.48e-03 while `highest`
gives 1.91e-06, which is ordinary float32 rounding (numpy f32 vs f64 is
9.9e-07).

That gap is not cosmetic. Every quantity in `core/brain.py` is
`floor(continuous * integer_count)`, so a product landing near an integer
decides between N and N-1. At 3.5e-3 the backends disagree often enough to be
near-certain across a 30-day season: the shipped agent would play moves the
trained agent never would.

Why an environment variable rather than `jax.config.update`:

* `kagg3/__init__.py` is shipped verbatim inside the submission archive, which
  must not import jax at all -- gate 3 enforces that, and the competition
  runtime has 1.6 vCPU to spare.
* An `import jax` side-effect only fires for whoever imports the module that
  carries it. Hanging it off `kagg3/sim` meant `from kagg3.core import brain`
  ran at TF32, so a gate could silently measure the wrong arithmetic -- which
  is worse than no gate.

JAX reads its config from the environment at import time, so setting the
variable before jax is first imported covers every entry point without this
module knowing anything about jax. `setdefault` leaves a deliberate override in
place. If jax somehow got imported first, it is corrected directly.
"""

import os
import sys

PRECISION = "highest"


def pin() -> None:
    os.environ.setdefault("JAX_DEFAULT_MATMUL_PRECISION", PRECISION)
    jax = sys.modules.get("jax")
    if jax is not None:  # imported before us; the env var is already too late
        jax.config.update("jax_default_matmul_precision", PRECISION)


pin()
