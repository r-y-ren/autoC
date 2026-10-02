"""kagg3: a Kaggriculture agent learned by ES over a bit-exact JAX simulator.

Importing anything under this package pins JAX's float32 matmul precision, so
the trainer and the numpy submission do the same arithmetic. It has to happen
here rather than in `kagg3.sim`: `from kagg3.core import brain` must get the pin
too, and it is the package `__init__` that every such import runs through.

`kagg3.precision` does this by setting an environment variable and never imports
jax, so this file stays safe to ship inside the pure-numpy submission.
"""
from . import precision as _precision

_precision.pin()
