"""Extract neural weights, optionally enabling sequential masks for adaptation."""

import argparse
from pathlib import Path
import _bootstrap  # noqa: F401


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--sequential-masks", action="store_true", help="enable Final B masks; does not train the model"
    )
    args = parser.parse_args()
    from kaggriculture.checkpoints import export_policy

    export_policy(args.checkpoint, args.output, sequential=True if args.sequential_masks else None)


if __name__ == "__main__":
    main()
