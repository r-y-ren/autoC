"""Verify an external H2H artifact without running any games."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SOFTWARE_ROOT.parents[1]
sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.eval_contract import ContractError  # noqa: E402
from kgenv.external_h2h_contract import (  # noqa: E402
    schema_validate_external,
    validate_external_h2h,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--schema", type=Path,
                        default=SOFTWARE_ROOT / "exports" / "external_h2h_schema.json")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        schema_validate_external(payload, args.schema)
        report = validate_external_h2h(payload, software_root=REPO_ROOT)
    except (OSError, ValueError, ContractError) as exc:
        print(f"external H2H: FAIL ({exc})", file=sys.stderr)
        return 1
    print("external H2H: PASS "
          f"({report['actual_games']} games, {report['opponents']} opponents, "
          f"{report['seeds']} seeds, AB={report['ab_games']} BA={report['ba_games']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
