#!/usr/bin/env python3
"""Cut one Kaggle replay seat into an ES training rung.

Why
---
`scripts/tape_opponent.py` packages a replay seat as a verbatim *engine*
opponent, and the two class-A tapes it cut hold our champion to 50% over 32
games. Those are the opponents the ES has never trained against, and it cannot
train against the tape itself: the fast sim has no action-dict seat to feed
recorded actions to.

What it does have is `sim.market.apply_flow`, which replays a measured per-day
SELL / BUY_PRODUCT table against the live quote curve -- that is how the
`kagg2_flow` and `kaggle_flow` rungs work. This script measures the *same kind*
of table off a single replay seat, so the flow the policy trains against is
that one opponent's, unit for unit, instead of a mean over a field.

The measurement is `scripts/replay_flow.py`'s, verbatim: executed units, in
lockstep with the other seat, bucketed by day. Only the aggregation differs --
one game, not a mean over twelve.

    python scripts/make_tape_rung.py replays/L_103254816.json \
        --ours "OurTeam" -o artifacts/tape_games/103254816.npz
    python scripts/train.py ... --tape-rung artifacts/tape_games/103254816.npz

What the rung is and is not is in `kagg3.es.tape_flow`'s docstring: the market
presence is verbatim, the plan behind it is a `wheat_clone` archetype, and the
trainer draws a scale and a day shift around the table per episode pair.

The `grow` table
----------------
A market footprint alone is only half an opponent. `sim.market.apply_flow`'s
`--tape-flow-backed` clamp asks what the flow seat can actually sell, and the
seat's board is a wheat clone that never holds the strawberry / milk / wool /
fertilizer these tapes trade -- so the clamp deleted the opponent instead of
shrinking it. `grow` is the other half: the units that entered the recorded
seat's shed that day by any route **other** than the market, net of the
non-market ones that left it.

It is read straight off the replay's own per-step shed observation, so it needs
no model of harvest yields, feeding or drops -- every one of those shows up in
the shed, and the market side is already measured::

    shed[d + 1] = shed[d] + grow[d] - sell[d] + buy[d]
    grow[d]     = shed[d + 1] - shed[d] + sell[d] - buy[d]

with `shed[d]` the seat's shed at the *start* of day `d`, which is observation
index `24 * d` (the profiler's day convention: `steps[t]["action"]` produced
`steps[t]["observation"]`, so engine step `t - 1` is day `(t - 1) // 24`). The
season's last boundary has no observation after it -- the engine stops 23 turns
into day 29 -- so day 29 closes on the last observation there is, which is
after every market turn of that day and misses only the day's final unit turn.

`grow` is **signed**: a day that fed more wheat to the animals than it
harvested is a real day. `meta["grow_source"]` records which derivation was
used, `"shed_delta"` (the identity above) or `"actions"` (the fallback below,
executed HARVEST / COLLECT_FERTILIZER units, used only where the replay has no
shed observation for a boundary).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import numpy as np  # noqa: E402

import replay_flow as RF  # noqa: E402
import replay_profile as RP  # noqa: E402
from kagg3.es import kagg2_flow as K2F  # noqa: E402
from kagg3.es import tape_flow as TF  # noqa: E402

#: What a HARVEST on an animal tile puts in the hand, for the `actions`
#: fallback. Crops name themselves (`tile["crop"]`); animals do not.
ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def _shed_row(step, seat):
    """One seat's shed at one observation index, in PRODUCTS order, or None.

    `None` where the replay has no private shed for that seat at that step --
    which is what sends the table to the `actions` fallback rather than
    silently reading a missing shed as an empty one.
    """
    try:
        priv = step[seat]["observation"].get("private") or {}
    except (KeyError, IndexError, TypeError):
        return None
    shed = priv.get("shed")
    if not isinstance(shed, dict):
        return None
    return np.asarray([int(shed.get(p, 0)) for p in RF.PRODUCTS], np.int64)


def _grow_from_actions(steps, seat):
    """Per-day non-market shed inflow counted off the seat's unit actions.

    -> int64 [N_DAYS, n_products]. The fallback for a replay with no shed
    observation. It counts what a HARVEST or a COLLECT_FERTILIZER *produced*
    (the tile's `yield_units`, and one unit of fertilizer), which is what
    reaches the hand; it cannot see the DROP that moves it into the shed on
    some later turn, nor the PICKUP that takes it back out, so it is an upper
    bound on the day's shed inflow and not the identity. `grow_source` says
    which of the two a table was cut with, so a rung built on this is never
    mistaken for one built on the shed.
    """
    ix = {p: i for i, p in enumerate(RF.PRODUCTS)}
    out = np.zeros((RF.N_DAYS, len(RF.PRODUCTS)), np.int64)
    for t in range(1, len(steps)):
        day = (t - 1) // RP.TURNS_PER_DAY
        if day >= RF.N_DAYS:
            continue
        act = steps[t][seat].get("action") or {}
        if not isinstance(act, dict):
            continue
        units = [act.get("farmer") or ["PASS"]]
        hs = act.get("hands") or []
        if isinstance(hs, list):
            units.extend([h if isinstance(h, list) and h else ["PASS"] for h in hs])
        pf = steps[t - 1][0]["observation"]["farms"][seat]
        positions = [tuple(pf["farmer"])] + [tuple(q) for q in (pf.get("hands") or [])]
        for idx, u in enumerate(units):
            if idx >= len(positions) or not isinstance(u, list) or not u:
                continue
            x, y = positions[idx]
            tile = pf["tiles"][y][x]
            if not isinstance(tile, dict):
                continue
            if u[0] == "COLLECT_FERTILIZER":
                out[day, ix["FERTILIZER"]] += 1
            elif u[0] == "HARVEST":
                item = tile.get("crop") or ANIMAL_PRODUCT.get(tile.get("animal"))
                if item in ix:
                    out[day, ix[item]] += int(tile.get("yield_units", 0) or 0)
    return out


def grow_table(path, seat, sell, buy):
    """The seat's per-day non-market shed inflow. -> (grow, source, residual).

    `grow` is int32 [N_DAYS, n_products] and **signed**; `source` is
    `"shed_delta"` or `"actions"`; `residual` is the season-level check on the
    identity -- `shed[last] - shed[0]` minus `sum(grow - sell + buy)` -- which
    is zero to the unit when the shed observations are there, and is what the
    caller asserts before the table is written. It is `None` on the fallback,
    which does not claim the identity.
    """
    with open(path) as fh:
        steps = json.load(fh)["steps"]
    sell = np.asarray(sell, np.int64)
    buy = np.asarray(buy, np.int64)
    # Observation index `24 * d` is the state at the start of day `d`; the last
    # index there is closes day 29 (see the module docstring).
    bounds = []
    for d in range(RF.N_DAYS + 1):
        t = min(RP.TURNS_PER_DAY * d, len(steps) - 1)
        bounds.append(_shed_row(steps[t], seat))
    if any(b is None for b in bounds):
        return np.asarray(_grow_from_actions(steps, seat), np.int32), "actions", None
    sheds = np.stack(bounds)                                   # [N_DAYS+1, P]
    grow = sheds[1:] - sheds[:-1] + sell - buy
    # The identity, forwards: rolling the measured season off the opening shed
    # has to land on every observed boundary, not just the last one.
    roll = sheds[0] + np.cumsum(grow - sell + buy, axis=0)
    if not np.array_equal(roll, sheds[1:]):
        raise SystemExit(f"{path}: the grow identity does not close.")
    residual = sheds[-1] - sheds[0] - (grow - sell + buy).sum(0)
    return np.asarray(grow, np.int32), "shed_delta", residual


def resolve_seat(teams, ours, opponent_team, seat):
    """Which seat to measure. -> int.

    `--seat` wins, then `--opponent-team` (exact, else a unique substring),
    then "the seat that is not `--ours`" -- the same precedence
    `scripts/tape_opponent.py:resolve_seat` uses, so a tape and its rung are
    cut off the same seat by the same words.
    """
    if seat is not None:
        if seat not in (0, 1):
            raise SystemExit(f"--seat {seat}: the board has two seats.")
        return int(seat)
    if opponent_team:
        hits = [i for i, n in enumerate(teams) if n == opponent_team]
        if not hits:
            hits = [i for i, n in enumerate(teams) if opponent_team in (n or "")]
        if len(hits) != 1:
            raise SystemExit(
                f"--opponent-team {opponent_team!r} matched {len(hits)} of {teams}")
        return hits[0]
    hits = [i for i, n in enumerate(teams) if n != ours]
    if len(hits) != 1:
        raise SystemExit(f"cannot infer the opponent seat from {teams}; "
                         f"pass --seat or --opponent-team.")
    return hits[0]


def tape_rung(path, ours="OurTeam", opponent_team=None, seat=None):
    """One replay seat's flow table plus its provenance.

    -> (sell, buy, meta, grow). `grow` is the production the market footprint
    implies, see the module docstring; it is the fourth element rather than the
    third so a caller that only wants the market side keeps its unpacking.
    """
    with open(path) as fh:
        rep = json.load(fh)
    info = rep.get("info", {}) or {}
    teams = list(info.get("TeamNames")
                 or [a.get("Name") for a in info.get("Agents", [])] or [])
    if len(teams) != 2:
        raise SystemExit(f"{path}: expected two team names, got {teams!r}")
    who = resolve_seat(teams, ours, opponent_team, seat)
    episode = int(info.get("EpisodeId") or 0) or os.path.splitext(
        os.path.basename(path))[0].lstrip("LW_")
    # `flow_from_replay` re-reads the file rather than taking the parsed dict;
    # a 30 MB replay read twice is a few seconds and keeps this script off
    # `replay_flow`'s internals.
    _teams, _ours_seat, per_seat = RF.flow_from_replay(path, ours)
    sell, buy = per_seat[who]
    steps = rep["steps"]
    money = steps[-1][0]["observation"]["farms"][who]["money"]
    ours_money = steps[-1][0]["observation"]["farms"][1 - who]["money"]
    grow, grow_source, residual = grow_table(path, who, sell, buy)
    if residual is not None and residual.any():
        raise SystemExit(f"{path}: grow residual {residual.tolist()} is not zero.")
    meta = {
        "episode": episode,
        "grow_source": grow_source,
        "rung": TF.rung_name(episode),
        "seat": who,
        "team": teams[who],
        "opponent": teams[1 - who],
        "final_money": int(money),
        "opponent_final_money": int(ours_money),
        "source": os.path.basename(path),
        "n_games": 1,
    }
    return (np.asarray(sell, np.int32), np.asarray(buy, np.int32), meta,
            np.asarray(grow, np.int32))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("replay", help="Kaggle replay JSON")
    ap.add_argument("--ours", default="OurTeam",
                    help="our team name; the OTHER seat is the one measured")
    ap.add_argument("--opponent-team", help="measure this team (exact, or a "
                                            "unique substring)")
    ap.add_argument("--seat", type=int, help="measure this seat; wins over "
                                             "--opponent-team")
    ap.add_argument("-o", "--out", help="npz to write (default "
                                        "artifacts/tape_games/<episode>.npz)")
    args = ap.parse_args(argv)

    RF._check_product_order()
    sell, buy, meta, grow = tape_rung(args.replay, args.ours,
                                      args.opponent_team, args.seat)
    out = args.out or os.path.join("artifacts", "tape_games",
                                   f"{meta['episode']}.npz")
    TF.save(out, sell, buy, meta, grow=grow)
    tape = TF.load(out)

    sys.stderr.write(
        "%s: seat %d (%s) vs %s, %d coins to %d\n"
        % (meta["rung"], meta["seat"], meta["team"], meta["opponent"],
           meta["final_money"], meta["opponent_final_money"]))
    sys.stderr.write("%-12s %9s %9s   %9s %9s %9s\n"
                     % ("product", "tapeS", "kagg2S", "tapeB", "kagg2B",
                        "tapeGrow"))
    gt = tape.grow.sum(0)
    for i, name in enumerate(RF.PRODUCTS):
        sys.stderr.write("%-12s %9d %9d   %9d %9d %9d\n"
                         % (name, tape.sell_totals[i], K2F.SELL_TOTALS[i],
                            tape.buy_totals[i], K2F.BUY_TOTALS[i], gt[i]))
    sys.stderr.write("%-12s %9d %9d   %9d %9d %9d\n"
                     % ("TOTAL", sum(tape.sell_totals), sum(K2F.SELL_TOTALS),
                        sum(tape.buy_totals), sum(K2F.BUY_TOTALS), gt.sum()))
    sys.stderr.write("grow_source %s\n" % tape.grow_source)
    sys.stderr.write("busiest day %d units (kagg2 %d)\nwrote %s\n"
                     % (tape.max_day_units, K2F.MAX_DAY_UNITS, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
