"""Archive only the current round's code, evidence, frozen opponents and handoff."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
CHECKPOINTS = ROOT / "checkpoints"


def selected_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in (
        "research/round10/**/*",
        "research/round11/**/*",
        "research/round11*",
        "results/round10_*",
        "results/round11/**/*",
        "experiments/round10*",
        "experiments/round11*",
        "external/round10/**/*",
        "build_round10*.py",
        "build_round11*.py",
        "*round10*.py",
        "arena_round11.py",
        "CONTINUE_ROUND10.md",
        "research/round9/league_seeds.json",
        "submissions/release_v8/main.py",
        "submissions/release_v9/main.py",
        "submissions/release_v9/submission.tar.gz",
        "external/round9/frontier/main.py",
        "external/round8/master2965/main.py",
        "experiments/round8_top2_dsm_strict.py",
        "league_round9.py",
        "compare_round8.py",
    ):
        for path in ROOT.glob(pattern):
            if path.is_file() and "__pycache__" not in path.parts:
                paths.add(path)
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    frozen_v9 = ROOT / "submissions/release_v9/main.py"
    assert hashlib.sha256(frozen_v9.read_bytes()).hexdigest() == (
        "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
    )
    CHECKPOINTS.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive = CHECKPOINTS / f"round10_{stamp}.zip"
    assert not archive.exists()
    items = []
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=6) as zip_file:
        for path in selected_paths():
            relative = path.relative_to(ROOT).as_posix()
            raw = path.read_bytes()
            zip_file.writestr(relative, raw)
            items.append({"path": relative, "bytes": len(raw),
                          "sha256": hashlib.sha256(raw).hexdigest()})
        manifest = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "root": str(ROOT),
            "environment": "kaggle-environments==1.32.7",
            "files": items,
            "note": "Round 10 confirmation and reserve remain unused; Round 11 confirmation and reserve stay locked until one development candidate is frozen.",
        }
        zip_file.writestr("CHECKPOINT_MANIFEST.json", json.dumps(manifest, indent=2))
    record = {"archive": str(archive), "file_count": len(items),
              "archive_bytes": archive.stat().st_size,
              "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "created_at_utc": manifest["created_at_utc"]}
    (CHECKPOINTS / "round10_latest.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
