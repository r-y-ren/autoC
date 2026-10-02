"""Run the public Kaggriculture pipeline component."""

import _bootstrap  # noqa: F401
from kaggriculture.training.critic import main

if __name__ == "__main__":
    main()
