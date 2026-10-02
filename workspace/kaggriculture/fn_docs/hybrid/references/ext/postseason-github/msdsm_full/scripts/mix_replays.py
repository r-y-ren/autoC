"""Run the public Kaggriculture pipeline component."""

import _bootstrap  # noqa: F401
from kaggriculture.data.mix_replays import main

if __name__ == "__main__":
    main()
