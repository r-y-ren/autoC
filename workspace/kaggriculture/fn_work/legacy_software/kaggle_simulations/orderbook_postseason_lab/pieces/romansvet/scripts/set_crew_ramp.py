"""Write the crew-ramp genes (`g10`/`gb10`) of a theta by hand.

The ramp is four pre-activation numbers the head emits off its hidden layer
(`policy.Outputs.ramp`), decoded in `brain.decide` as

    crew_top   = CREW_TARGET_MAX * relu(tanh(ramp[0]))      # hands
    crew_mid   = CREW_MID_MAX    * sigmoid(ramp[1])         # day
    crew_steep = CREW_STEEP_MAX  * sigmoid(ramp[2])         # logits/day
    target(d)  = clip(qfloor(crew_top * sigmoid(crew_steep * (d - crew_mid))),
                      0, spec.MAX_HANDS)
    defer      = clip(qfloor(DEFER_ONE * relu(tanh(ramp[3]))), 0, DEFER_ONE)

`ramp = gh @ g10 + gb10`, so **zeroing `g10` and writing `gb10` alone** makes
the ramp a function of the day and of nothing else -- the same curve on every
board, which is what "twelve hands by day ten" means as a claim. That is what
this script does: `g10` (128 params) to zero, `gb10` (4 params) to the encoded
knobs, and not one index outside `[offset(g10), N_PARAMS)` touched.

    scripts/set_crew_ramp.py --theta in.npy --out out.npy \
        --hands 12 --by-day 10 --defer saturated

The knobs are solved rather than guessed: `top` sits just above `--hands` so
the logistic's floor is exactly that number, the midpoint defaults to half of
`--by-day`, and the steepness is the one that puts the curve over `--hands` on
`--by-day`. The result is then **verified through the real decode**
(`brain.decide`, not a re-implementation of it) and the solve retried with a
wider margin if the day the caller asked for came back short, so the printed
table is what the planner will read and not what the algebra hoped for.
"""
from __future__ import annotations

import argparse
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import numpy as np

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO

#: Prices at the market's own starting inventory. The ramp reads none of them
#: -- `_check_board_free` proves that -- but `PolicyObs` is a contract and a
#: nonsense price would make the decode's other fields nonsense too.
BASE_PRICE = np.array([spec.market_price(p, spec.MARKET_I0) for p in spec.PRODUCTS],
                      np.int32)


def _obs(day: int, money: int = 200_000) -> brain.PolicyObs:
    """A blank owned board on `day`, with a purse too big to bind anything."""
    z = np.zeros(spec.N_TILES, np.int32)
    return brain.PolicyObs(
        day=np.int32(day), money=np.int32(money), opp_money=np.int32(3_000),
        kind=np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32), occ=z - 1,
        opp_kind=np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32), opp_occ=z - 1,
        t_day=z.copy(), t_yield=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        nquad=np.int32(4), opp_nquad=np.int32(4),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=BASE_PRICE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def decode(theta, money: int = 200_000):
    """`[(crew_target, animal_defer)]` for days 0..N_DAYS-1, via `brain.decide`."""
    th = np.asarray(theta, np.float32)
    rows = []
    for day in range(spec.N_DAYS):
        m = brain.decide(np, th, _obs(day, money))
        rows.append((int(m.crew_target), int(m.animal_defer)))
    return rows


def _logit(p: float) -> float:
    return float(np.log(p / (1.0 - p)))


def saturated_defer() -> float:
    """Smallest tidy `ramp[3]` whose decode is exactly `DEFER_ONE`.

    Searched, not derived: `_qfloor`'s guard is `max(QUANT_EPS, QUANT_REL*|x|)`
    and `tanh` saturates in float32, so where the product crosses `DEFER_ONE`
    is a property of the arithmetic and is better measured than reasoned about.
    """
    base = np.zeros(PO.N_PARAMS, np.float32)
    base[PO.offset("gb10")] = 4.0            # a height, so the target is non-zero
    for x in np.arange(1.0, 16.01, 0.25):
        th = base.copy()
        th[PO.offset("gb10") + 3] = x
        if decode(th)[0][1] == brain.DEFER_ONE:
            return float(x)
    raise SystemExit("no ramp[3] in [1, 16] saturates the deferral")


def solve(hands: int, by_day: int, mid_day, steep, defer_pre: float, margin: float):
    """Encode "`hands` hands by day `by_day`" into the four pre-activations.

    `margin` is how far over `hands` the curve is asked to sit on `by_day`;
    `main` widens it and re-solves if the real decode comes back one short,
    which is the only thing quantisation can plausibly do here.
    """
    if not 1 <= hands < spec.MAX_HANDS:
        raise SystemExit(f"--hands must be in 1..{spec.MAX_HANDS - 1}")
    if not 0 <= by_day < spec.N_DAYS:
        raise SystemExit(f"--by-day must be in 0..{spec.N_DAYS - 1}")
    mid = 0.5 * by_day if mid_day is None else float(mid_day)
    mid = float(np.clip(mid, 0.01 * spec.N_DAYS, 0.99 * spec.N_DAYS))
    if mid >= by_day:
        raise SystemExit("--mid-day must be strictly before --by-day")

    top = hands + 0.5                                   # so floor(top) == hands
    if steep is None:
        want = min(0.9995, (hands + margin) / top)
        k = _logit(want) / (by_day - mid)
    else:
        k = float(steep)
    k = float(np.clip(k, 1e-3, brain.CREW_STEEP_MAX - 1e-3))

    gb = np.zeros(PO.N_CREW_RAMP_OUT, np.float32)
    gb[0] = np.arctanh(top / brain.CREW_TARGET_MAX)
    gb[1] = _logit(mid / brain.CREW_MID_MAX)
    gb[2] = _logit(k / brain.CREW_STEEP_MAX)
    gb[3] = defer_pre
    return gb, {"top": top, "mid": mid, "steep": k}


def _table(rows) -> str:
    return "\n".join("  day %2d  target %2d  defer %3d" % (d, t, f)
                     for d, (t, f) in enumerate(rows))


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--theta", required=True, help="input .npy")
    ap.add_argument("--out", required=True, help="output .npy")
    ap.add_argument("--hands", type=int, required=True, help="crew the ramp asks for")
    ap.add_argument("--by-day", type=int, required=True, help="day it asks for them by")
    ap.add_argument("--mid-day", type=float, default=None,
                    help="logistic midpoint in days (default: half of --by-day)")
    ap.add_argument("--steep", type=float, default=None,
                    help="logits/day in 0..%.1f (default: solved from the two above)"
                         % brain.CREW_STEEP_MAX)
    ap.add_argument("--defer", default="0",
                    help="animal deferral: 'saturated', or a fraction of DEFER_ONE in [0,1)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing --out")
    a = ap.parse_args()

    if os.path.exists(a.out) and not a.force:
        raise SystemExit(f"{a.out} exists (pass --force to overwrite)")

    src = np.load(a.theta)
    if src.ndim != 1:
        raise SystemExit(f"{a.theta} is not a flat theta: {src.shape}")
    theta = np.asarray(PO.pad(np.asarray(src, np.float32)), np.float32)
    before = decode(theta)

    if str(a.defer).strip().lower() in ("sat", "saturated", "max"):
        defer_pre = saturated_defer()
    else:
        frac = float(a.defer)
        if not 0.0 <= frac < 1.0:
            raise SystemExit("--defer must be 'saturated' or a fraction in [0, 1)")
        defer_pre = 0.0 if frac == 0.0 else float(np.arctanh(frac))

    o10, ob10 = PO.offset("g10"), PO.offset("gb10")
    out = theta.copy()
    out[o10:ob10] = 0.0                      # the ramp is the day's and nothing else

    knobs, after = None, None
    for margin in (0.05, 0.15, 0.30, 0.50):
        gb, knobs = solve(a.hands, a.by_day, a.mid_day, a.steep, defer_pre, margin)
        out[ob10:PO.N_PARAMS] = gb
        after = decode(out)
        if after[a.by_day][0] >= a.hands or a.steep is not None:
            break

    # Nothing outside the ramp block moved -- the whole point of the script.
    assert out[:o10].tobytes() == theta[:o10].tobytes(), "a gene outside g10 changed"
    assert out.shape == theta.shape and out.dtype == theta.dtype

    # The curve is the day's and not the board's, now that `g10` is zero.
    lo, hi = decode(out, money=3_000), decode(out, money=500_000)
    assert lo == after == hi, "the ramp still reads the board -- g10 is not zero"

    print(f"in   {a.theta}")
    print(f"out  {a.out}")
    print("knobs  top=%.3f hands  mid=%.2f d  steep=%.3f logits/d  defer_pre=%.3f"
          % (knobs["top"], knobs["mid"], knobs["steep"], defer_pre))
    print("gb10   " + "  ".join("%+.6f" % v for v in out[ob10:PO.N_PARAMS]))
    print("g10    zeroed (%d params)" % (ob10 - o10))
    print("BEFORE\n" + _table(before))
    print("AFTER\n" + _table(after))
    got = after[a.by_day][0]
    print("check  day %d target = %d (asked %d)%s"
          % (a.by_day, got, a.hands, "" if got >= a.hands else "   *** SHORT ***"))
    print("check  peak target = %d over the season, defer = %d/%d"
          % (max(t for t, _ in after), after[0][1], brain.DEFER_ONE))
    print("check  bytes outside [%d, %d) identical to the input" % (o10, PO.N_PARAMS))

    np.save(a.out, out)


if __name__ == "__main__":
    main()
