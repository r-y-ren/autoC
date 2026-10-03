#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.generate_jamming.generate_jamming import generate_jamming
p = argparse.ArgumentParser(); p.add_argument("--scenario", required=True)
p.add_argument("--dry-run", action="store_true"); p.add_argument("--out", default="runs")
a = p.parse_args()
try:
    res = generate_jamming(None, dry_run=a.dry_run, out_dir=Path(a.out))
    print(res); sys.exit(0)
except NotImplementedError as e:
    print(f"[scaffold] {e}"); sys.exit(3)
