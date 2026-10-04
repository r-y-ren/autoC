"""Compile the endgame planner for the current machine; use Linux for Kaggle."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import _bootstrap  # noqa: F401


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compiler", default=os.environ.get("CXX", "c++"))
    args = parser.parse_args()
    import kaggriculture.search

    source = Path(kaggriculture.search.__file__).parent
    output = (args.output or source / "terminal_search.so").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        library = Path(temp) / "terminal_search.so"
        subprocess.run(
            [
                args.compiler,
                "-O3",
                "-std=c++17",
                "-fPIC",
                "-shared",
                "-DNDEBUG",
                "-fno-math-errno",
                "-fno-trapping-math",
                "-ffp-contract=off",
                str(source / "terminal_search.cpp"),
                "-o",
                str(library),
            ],
            check=True,
        )
        library.replace(output)
    print(output)


if __name__ == "__main__":
    main()
