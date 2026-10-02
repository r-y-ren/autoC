"""Run the public Kaggriculture pipeline component."""

import _bootstrap  # noqa: F401
import os

if int(os.environ.get("KAGGRICULTURE_PROCESS_COUNT", "1")) > 1:
    import jax

    jax.distributed.initialize(
        coordinator_address=os.environ["KAGGRICULTURE_COORDINATOR"],
        num_processes=int(os.environ["KAGGRICULTURE_PROCESS_COUNT"]),
        process_id=int(os.environ["KAGGRICULTURE_PROCESS_INDEX"]),
        local_device_ids=[0],
    )
from kaggriculture.training.bc import main

if __name__ == "__main__":
    main()
