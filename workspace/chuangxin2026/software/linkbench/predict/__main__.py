"""CLI：python -m linkbench.predict --model models/best.onnx --sigmf runs/x/y"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.predict")
    p.add_argument("--model", required=True)
    p.add_argument("--sigmf", required=True)
    args = p.parse_args(argv)
    from linkbench.predict.predictor import predict_styles
    for pred in predict_styles(args.model, args.sigmf):
        print(pred)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
