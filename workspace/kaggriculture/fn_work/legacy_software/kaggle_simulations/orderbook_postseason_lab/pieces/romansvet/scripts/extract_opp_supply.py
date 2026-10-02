#!/usr/bin/env python3
"""Measure the opponent supply curve S[turn, product] off the tape library.

The opponents that beat us on Kaggle are open-loop scripts: their market row
is a recording, so their SELL / BUY_PRODUCT volumes are fixed by turn and
product whatever board they land on.  A tape opponent
(`scripts/tape_opponent.py`) is that recording verbatim, so the volumes can be
read straight out of `_TAPE` -- no engine, no replay.

`S[t, p] = mean over tapes of (SELL units - BUY_PRODUCT units)` at engine step
`t` for product `p`, in `spec.PRODUCTS` order.  Positive = supply the other
seat adds to the shared market before our order at `t` resolves; negative =
supply it drains.  Those are exactly the two ops that move `market inventory`
(`sim/market.py: _inventory_orders`); BUY_SEED / BUY_ANIMAL / HIRE / BUY_LAND
are fixed-price and never touch it.

Recorded, not executed: a SELL the engine clipped to the seat's shed, or a
BUY it refused for want of cash, still counts here at its recorded size.  The
planner wants a *forecast*, and the recorded row is the only thing that is
board-independent; the `OPP_SUPPLY_SCALE` knob at the use site is where the
shortfall is priced.

Usage:
    python scripts/extract_opp_supply.py --out artifacts/opp_supply
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import numpy as np  # noqa: E402

from kagg3 import spec  # noqa: E402

TURNS = spec.EPISODE_STEPS          # 720
NP_ = spec.N_PRODUCTS               # 9

BAND6 = ["105443859", "105442685", "105441843", "105441481", "105592028", "105400600"]
WALL6 = ["105780913", "105792697", "105793641", "105795631", "105797930", "105798370"]
FLOOD6 = ["105750519", "105753355", "105760790", "105754313", "105755280", "105769099"]

#: Products the report calls out by name, in reporting order.
MAIN = ["WHEAT", "MILK", "WOOL", "EGG", "MELON", "STRAWBERRY", "TOMATO",
        "CARROT", "FERTILIZER"]


def load_tape(main_py: Path):
    """The tape's action list, by exec of the generated module."""
    ns: dict = {}
    exec(compile(main_py.read_text(), str(main_py), "exec"), ns)  # noqa: S102
    return ns["_TAPE"], ns.get("_EPISODE"), ns.get("_SOURCE_TEAM"), ns.get("_SOURCE_MONEY")


def tape_rows(tape):
    """(sell[TURNS, 9], buy[TURNS, 9]) of recorded market-inventory orders."""
    sell = np.zeros((TURNS, NP_), np.int32)
    buy = np.zeros((TURNS, NP_), np.int32)
    for t, action in enumerate(tape[:TURNS]):
        for order in (action.get("market") or []):
            if len(order) < 3:
                continue                      # HIRE / BUY_LAND
            op, item, n = order[0], order[1], int(order[2])
            ix = spec.ITEM_IX.get(item)
            if ix is None or ix >= NP_:
                continue                      # seeds / animals: fixed price
            if op == "SELL":
                sell[t, ix] += n
            elif op == "BUY_PRODUCT":
                buy[t, ix] += n
    return sell, buy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default="artifacts/panel_opp")
    ap.add_argument("--out", default="artifacts/opp_supply")
    ap.add_argument("--top10", default=None,
                    help="file of tape main.py paths, one per line")
    args = ap.parse_args()

    root = Path(args.tapes)
    dirs = sorted(d for d in root.iterdir()
                  if d.is_dir() and d.name.startswith("opponent_tape_"))
    eps, nets, sells, buys, teams = [], [], [], [], []
    for d in dirs:
        tape, ep, team, money = load_tape(d / "main.py")
        s, b = tape_rows(tape)
        eps.append(str(ep))
        teams.append(team)
        sells.append(s)
        buys.append(b)
        nets.append(s - b)
    net = np.stack(nets).astype(np.float32)        # [T tapes, 720, 9]
    sell = np.stack(sells).astype(np.float32)
    buy = np.stack(buys).astype(np.float32)
    ix = {e: i for i, e in enumerate(eps)}

    top10 = []
    if args.top10 and Path(args.top10).exists():
        for line in Path(args.top10).read_text().split():
            m = re.search(r"opponent_tape_(\d+)", line)
            if m:
                top10.append(m.group(1))

    def subset(names):
        return [ix[n] for n in names if n in ix]

    sets = {"pop": list(range(len(eps))),
            "band6": subset(BAND6), "wall6": subset(WALL6),
            "flood6": subset(FLOOD6), "top10": subset(top10)}
    sets["band6_wall6_top10"] = sorted(set(sets["band6"]) | set(sets["wall6"])
                                       | set(sets["top10"]))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"n_tapes": len(eps), "turns": TURNS,
                "products": list(spec.PRODUCTS),
                "note": "S[turn, product] = mean recorded SELL - BUY_PRODUCT units",
                "sets": {}}
    for name, idxs in sets.items():
        if not idxs:
            continue
        curve = net[idxs].mean(0).astype(np.float32)
        np.save(out / f"S_{name}.npy", curve)
        manifest["sets"][name] = {
            "n": len(idxs),
            "episodes": [eps[i] for i in idxs],
            "file": f"S_{name}.npy",
            "total_net_units": float(curve.sum()),
        }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # ---------------------------------------------------------------- report
    day_net = net.reshape(len(eps), spec.N_DAYS, spec.TURNS_PER_DAY, NP_).sum(2)
    print(f"tapes: {len(eps)}  turns: {TURNS}  products: {NP_}")
    print(f"mean net units per tape per game: {net.sum(axis=(1, 2)).mean():.1f} "
          f"(sell {sell.sum(axis=(1, 2)).mean():.1f}, buy {buy.sum(axis=(1, 2)).mean():.1f})")
    print()
    print("cross-tape sd of DAILY net units (mean over days) / mean |daily net|:")
    for name in MAIN:
        p = spec.ITEM_IX[name]
        col = day_net[:, :, p]
        sd = col.std(0)
        mu = col.mean(0)
        peak = int(np.argmax(np.abs(mu)))
        print(f"  {name:<11} mean/day {mu.mean():7.2f}  sd/day {sd.mean():7.2f}  "
              f"cv {sd.mean() / max(abs(mu.mean()), 1e-9):6.2f}  "
              f"peak day {peak} mean {mu[peak]:.2f} sd {sd[peak]:.2f}")
    print()
    print("population mean net units by day (all products summed):")
    tot = day_net.mean(0).sum(1)
    print("  " + " ".join(f"d{d}:{tot[d]:.1f}" for d in range(spec.N_DAYS)))
    print()
    print("turn profile within a day (population mean, all products, all days):")
    hour = net.reshape(len(eps), spec.N_DAYS, spec.TURNS_PER_DAY, NP_).mean(0).sum((0, 2))
    print("  " + " ".join(f"h{h}:{hour[h]:.1f}" for h in range(spec.TURNS_PER_DAY)))
    print()
    for name in ("pop", "band6", "wall6", "flood6", "top10", "band6_wall6_top10"):
        if name in manifest["sets"]:
            print(f"saved {name:<18} n={manifest['sets'][name]['n']:<3} "
                  f"net units/game={manifest['sets'][name]['total_net_units']:.1f}")


if __name__ == "__main__":
    main()
