"""Read-only active-candidate identity self-check (works from repo root).

Usage:
    python workspace/kaggriculture/software/scripts/check_candidate_identity.py

Loads workspace/kaggriculture/software/active_candidate.json, re-derives every referenced
identity from the artifacts (working main.py SHA, frozen snapshot decode,
published holdout export/seed manifest, vendored engine wheel, runtime) and
validates the README machine projection.  Exit 0 only when everything,
including the README projection, is consistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.candidate_identity import (  # noqa: E402
    CandidateIdentityError,
    validate_active_candidate,
)


def main() -> int:
    manifest_path = SOFTWARE_ROOT / "active_candidate.json"
    readme_path = SOFTWARE_ROOT / "README.md"
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL cannot read active candidate manifest: {exc}")
        return 1
    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL cannot read README: {exc}")
        return 1
    try:
        payload = validate_active_candidate(payload,
                                            software_root=SOFTWARE_ROOT,
                                            readme_text=readme_text)
    except CandidateIdentityError as exc:
        print(f"FAIL {exc}")
        return 1
    working = payload["working"]
    frozen = payload["last_promoted_frozen"]
    holdout = payload["published_holdout"]
    print("candidate identity: PASS "
          f"(working={working['status']} {working['sha256'][:12]}..., "
          f"frozen={frozen['sha256'][:12]}..., "
          f"published_attempt={holdout['attempt_index']}, "
          "readme projection ok)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
