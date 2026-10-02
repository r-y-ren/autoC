"""Run the public Kaggriculture pipeline component."""

import _bootstrap  # noqa: F401
from kaggriculture.data.search_selfplay import main

if __name__ == "__main__":
    main()
