"""Fit descriptive Bradley-Terry/Davidson ratings from recorded games."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.bradley_terry import RatingError, fit_ratings  # noqa: E402
from kgenv.eval_contract import ContractError, atomic_publish_json  # noqa: E402
from kgenv.external_h2h_contract import (  # noqa: E402
    schema_validate_external,
    validate_external_h2h,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True,
                        help="JSON containing games or pair_counts")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=200)
    parser.add_argument("--bootstrap-seed", type=int, default=20260831)
    parser.add_argument("--regularization", type=float, default=1e-4)
    parser.add_argument("--tier-margin", type=float, default=0.3)
    parser.add_argument("--max-iterations", type=int, default=400)
    parser.add_argument("--require-ab-ba", action="store_true",
                        help="require exactly one AB and BA row per pair and seed")
    parser.add_argument("--allow-nonconverged", action="store_true",
                        help="diagnostic only; output remains unrated")
    return parser

def _reject_repository_output(output: Path) -> None:
    repo_root = SOFTWARE_ROOT.parents[1]
    target = output.resolve()
    external_root = (SOFTWARE_ROOT / "exports" / "external").resolve()
    try:
        inside_repo = target.is_relative_to(repo_root.resolve())
        inside_external = target.is_relative_to(external_root)
    except AttributeError:
        inside_repo = str(target).startswith(str(repo_root.resolve()) + os.sep)
        inside_external = str(target).startswith(str(external_root) + os.sep)
    if inside_repo and not inside_external:
        raise RatingError("repository output must stay under workspace/software/exports/external")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        _reject_repository_output(args.output)
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RatingError("input must be a JSON object")
        games = payload.get("games")
        pair_counts = payload.get("pair_counts")
        if not isinstance(games, list) and not isinstance(pair_counts, list):
            raise RatingError("input must contain games or pair_counts")
        schema_version = payload.get("schema_version")
        if isinstance(schema_version, str) and schema_version.startswith("external-h2h/"):
            schema_path = SOFTWARE_ROOT / "exports" / "external_h2h_schema.json"
            schema_validate_external(payload, schema_path)
            validate_external_h2h(payload, software_root=SOFTWARE_ROOT.parents[1])
            games = payload["games"]
        report = fit_ratings(
            games if isinstance(games, list) else None,
            pair_counts=pair_counts if isinstance(pair_counts, list) else None,
            bootstrap_samples=args.bootstrap,
            bootstrap_seed=args.bootstrap_seed,
            regularization=args.regularization,
            tier_margin=args.tier_margin,
            max_iterations=args.max_iterations,
            require_ab_ba=args.require_ab_ba,
            allow_nonconverged=args.allow_nonconverged,
        )
        report.update({
            "descriptive_only": True,
            "holdout_generalization_claim": False,
            "publishable": False,
            "publication_status": ("diagnostic_only_nonconverged" if not report["converged"]
                                    else "descriptive_only"),
            "input_path": str(args.input),
            "method_note": "batch order-independent BT/Davidson; bootstrap clusters by seed",
        })
        args.output.parent.mkdir(parents=True, exist_ok=True)
        atomic_publish_json(
            args.output,
            report,
            lambda value: None,
        )
    except (OSError, ValueError, RatingError, ContractError) as exc:
        print(f"BT/Davidson fit failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote descriptive {report['model']} report: {args.output} "
          f"({report['game_count']} games, converged={report['converged']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
