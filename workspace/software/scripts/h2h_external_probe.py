"""H2H probe: our candidates vs external opponents (v48 / v72 anchor).

Evaluation-only harness (no gate semantics): it does not touch the ablate
contract, REQUIRED_OPPONENTS, or any promotion rule.  It exists to translate
the online class gap into local behaviour terms by playing the public
kaitofukami v48 snapshot and the historical v7.2 online champion (718.6)
against the current submission path on the paired seed domain.

Opponent files live in kaggle_simulations/opponents/ with a PROVENANCE.md;
their bytes are evaluation metadata and must never enter the submission path.

Example:
    python scripts/h2h_external_probe.py --out .tmp-intel/h2h_v48.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(SOFTWARE_ROOT))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import (  # noqa: E402
    AbnormalMatchError,
    load_submission_agent,
    run_match,
)

OPPONENTS_DIR = os.path.join(
    SOFTWARE_ROOT, "kaggle_simulations", "opponents")
SUBMISSION_MAIN = os.path.join(
    SOFTWARE_ROOT, "kaggle_simulations", "agent", "main.py")
DEV_SEEDS = [101, 102, 103, 104]
REG_SEEDS = [201, 202, 203, 204]


def sha256_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def play_pair(cand_path: str, opp_path: str, cand_label: str,
              opp_label: str, seeds: list[int]) -> dict:
    cand = load_submission_agent(cand_path)
    opp = load_submission_agent(opp_path)
    cells = []
    for seed in seeds:
        for seat in ("AB", "BA"):
            t0 = time.time()
            if seat == "AB":
                res = run_match(cand, opp, seed,
                                label_a=cand_label, label_b=opp_label)
                idx = 0
            else:
                res = run_match(opp, cand, seed,
                                label_a=opp_label, label_b=cand_label)
                idx = 1
            cells.append({
                "seed": seed, "seat": seat,
                "cand_reward": float(res["rewards"][idx]),
                "opp_reward": float(res["rewards"][1 - idx]),
                "margin": res["rewards"][idx] - res["rewards"][1 - idx],
                "winner": res["winner_label"],
                "seconds": round(time.time() - t0, 1),
            })
    wins = sum(1 for c in cells if c["winner"] == cand_label)
    losses = sum(1 for c in cells if c["winner"] == opp_label)
    ties = len(cells) - wins - losses
    domains = {}
    for name, dom in (("dev", DEV_SEEDS), ("reg", REG_SEEDS)):
        cs = [c for c in cells if c["seed"] in dom]
        domains[name] = {
            "games": len(cs),
            "wins": sum(1 for c in cs if c["winner"] == cand_label),
            "losses": sum(1 for c in cs if c["winner"] == opp_label),
            "mean_margin": round(sum(c["margin"] for c in cs) / len(cs), 1)
            if cs else None,
        }
    return {
        "candidate": {"path": cand_path, "sha256": sha256_file(cand_path)},
        "opponent": {"path": opp_path, "sha256": sha256_file(opp_path)},
        "summary": {
            "games": len(cells), "wins": wins, "losses": losses,
            "ties": ties,
            "mean_margin": round(sum(c["margin"] for c in cells)
                                 / len(cells), 1),
            "total_margin": round(sum(c["margin"] for c in cells), 1),
            "worst_margin": round(min(c["margin"] for c in cells), 1),
            "domains": domains,
        },
        "cells": cells,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", default=",".join(
        str(s) for s in DEV_SEEDS + REG_SEEDS))
    parser.add_argument("--candidates", default=SUBMISSION_MAIN)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    out = args.out
    if out.is_absolute():
        resolved = out
    else:
        resolved = Path(REPO_ROOT) / out
    if Path(REPO_ROOT) not in resolved.resolve().parents:
        raise ValueError(f"output must stay under repo scratch: {out}")
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    opp_path = os.path.join(OPPONENTS_DIR, "v48_main.py")
    reports = {}
    for cand_path in args.candidates.split(","):
        cand_path = cand_path.strip()
        label = Path(cand_path).parent.name or "submission"
        print(f"=== {label} ({cand_path}) vs v48 ===", flush=True)
        try:
            reports[label] = play_pair(cand_path, opp_path, label,
                                       "v48", seeds)
            s = reports[label]["summary"]
            print(f"  {s['wins']}W-{s['losses']}L-{s['ties']}T "
                  f"mean_margin={s['mean_margin']} "
                  f"worst={s['worst_margin']} domains={s['domains']}",
                  flush=True)
        except AbnormalMatchError as exc:
            print(f"  ABNORMAL: {exc}", file=sys.stderr, flush=True)
            reports[label] = {"error": str(exc)}
    resolved.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "h2h-external/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kind": "development-only",
        "opponent": "v48 (kaitofukami, sha dadee25a...)",
        "reports": reports,
    }
    temp = resolved.with_name(f".{resolved.name}.{os.getpid()}.tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    os.replace(temp, resolved)
    print(f"wrote {resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
