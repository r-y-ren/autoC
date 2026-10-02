"""Package the current champion and push it to the competition.

Requires Kaggle API credentials, which this machine does not have by default:
put your token at ~/.kaggle/kaggle.json (chmod 600), or export KAGGLE_USERNAME
and KAGGLE_KEY.

Refuses to submit unless the release gates have been run, because the whole
point of the gates is that a divergence here is silent.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMPETITION = "kaggriculture"


def have_credentials() -> bool:
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True
    return (pathlib.Path.home() / ".kaggle" / "kaggle.json").exists()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default=str(ROOT / "artifacts" / "theta.npy"))
    ap.add_argument("--message", default=None)
    ap.add_argument("--skip-gates", action="store_true",
                    help="submit without re-running the release gates (not advised)")
    args = ap.parse_args()

    if not have_credentials():
        print("No Kaggle credentials found.\n"
              "  Put your token at ~/.kaggle/kaggle.json (chmod 600), or export\n"
              "  KAGGLE_USERNAME and KAGGLE_KEY, then re-run.", file=sys.stderr)
        return 2

    if not args.skip_gates:
        print("running release gates...", flush=True)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)
        if r.returncode != 0:
            print("gates failed; not submitting", file=sys.stderr)
            return 1

    sys.path.insert(0, str(ROOT / "scripts"))
    import package_submission as pkg

    out = ROOT / "dist" / "submission.tar.gz"
    pkg.build(pathlib.Path(args.theta), out)
    bad = pkg.forbidden_imports()
    if bad:
        print("FORBIDDEN IMPORTS:", *bad, sep="\n  ", file=sys.stderr)
        return 1

    msg = args.message
    if msg is None:
        log = ROOT / "artifacts" / "run3" / "log.jsonl"
        gen = champ = "?"
        if log.exists():
            last = json.loads(log.read_text().strip().splitlines()[-1])
            gen, champ = last.get("gen"), last.get("champ")
        msg = f"ES self-play, gen {gen}, ladder win {champ}"

    cmd = ["kaggle", "competitions", "submit", "-c", COMPETITION,
           "-f", str(out), "-m", msg]
    print(" ".join(cmd), flush=True)
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
