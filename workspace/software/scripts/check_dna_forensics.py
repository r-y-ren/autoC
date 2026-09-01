"""Verify offline DNA artifacts without replay, engine, holdout, or network access."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.dna_integrity import IntegrityError, validate_artifacts  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path,
                        default=SOFTWARE_ROOT / "exports" / "replay_dna" / "index.json")
    parser.add_argument("--report", type=Path,
                        default=SOFTWARE_ROOT / "exports" / "replay_dna" / "report.json")
    parser.add_argument("--schema", type=Path,
                        default=SOFTWARE_ROOT / "exports" / "replay_dna" / "dna_schema.json")
    return parser


def main(argv=None, *, software_root: Path = SOFTWARE_ROOT) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = validate_artifacts(args.index, args.report, args.schema,
                                    software_root=software_root)
    except (OSError, ValueError, IntegrityError) as exc:
        print(f"DNA integrity: FAIL ({exc})", file=sys.stderr)
        return 1
    print("DNA integrity: PASS "
          f"({result['samples']} samples, {result['groups']} groups, "
          f"{result['comparisons']} comparisons, {result['source_files']} source files; "
          "offline exploratory)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
