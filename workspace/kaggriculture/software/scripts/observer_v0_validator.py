#!/usr/bin/env python
"""OBS-4: offline V0 validator (opp_supply_observer_design.md §5.1).

Steps official replay JSONs through the agent's observer using ONLY legal
per-seat observation fields, then scores the estimates against the replay
ground truth (each seat's private.shed/inventories -- readable OFFLINE
only, never inside the agent):

  Gate 1  Ch0 integer accounting: share of (seat, day, item) samples where
          the Ch0-exact opponent net flow equals the opponent's submitted
          net orders, on normal-price days -- must be >= 95% (calibrates
          the sampling hour; closes E4).
  Gate 2  turning points: |est turning day - true turning day| <= 1 day
          (median), and magnitude error at turning days <= 30%.
  Gate 3  report: per-item final/MAE/max held error, floor-price segment
          ($1 days) split out.

Usage:
  python scripts/observer_v0_validator.py --replays GLOB [GLOB ...]
      [--out exports/probes/observer_v0.json]
"""
import argparse
import glob
import importlib.util
import json
import statistics
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"


def load_module(path=AGENT_MAIN):
    spec = importlib.util.spec_from_file_location("v0_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_stream(data):
    """Yield per-seat legal observations + submitted market orders."""
    for step in (data.get("steps") or [])[1:]:
        for seat in (0, 1):
            entry = step[seat] or {}
            obs = entry.get("observation")
            if not obs:
                continue
            action = entry.get("action") or {}
            yield seat, obs, list(action.get("market") or [])


def true_held(private, item):
    """Ground truth: opponent's un-monetized holding (shed + carried)."""
    if not private:
        return 0
    shed = private.get("shed") or {}
    total = shed.get(item, 0) or 0
    for inv in private.get("inventories") or []:
        if inv:
            total += inv.get(item, 0) or 0
    return total


def score(samples):
    """Pure aggregation (unit-tested).  samples: list of dicts with keys
    {seat, day, item, ch0_net, submitted_net, price, est_held, true_held}.

    Gate-1 scope note: samples whose day saw ANY submitted BUY of the item
    are excluded -- the engine may reject/partially fill BUY orders, so
    submitted != the executed flow that Ch0 actually measured (executed
    quantities are not offline-recoverable); that noise is not an
    accounting error.  Days 0-1 are warm-up (first-window center-draw
    phase, E4) and also excluded.  Flat est series (max < 1) never reach
    gate 2.
    """
    normal = [s for s in samples if s["price"] is not None
              and s["price"] > 1 and s["day"] > 1
              and s["item"] != "FERTILIZER"
              and not s.get("had_buys")]
    floor = [s for s in samples if s["price"] is not None
             and s["price"] <= 1]
    exact = [s for s in normal if s["ch0_net"] is not None
             and s["ch0_net"] == s["submitted_net"]]
    gate1 = {
        "normal_samples": len(normal),
        "exact": len(exact),
        "share": round(len(exact) / len(normal), 4) if normal else None,
        "pass": bool(normal) and len(exact) / len(normal) >= 0.95,
    }
    # turning points per (seat, item) with a meaningful true series
    # series must be PER REPLAY: keying by (seat, item) alone merged 60
    # episodes' same-day rows into one mashed series and the argmax
    # turning day compared jumps across unrelated games (the W1 verdict's
    # absurd 38-220 "day" lags were this metric bug, not observer error)
    series = {}
    for s in samples:
        key = (s.get("replay", ""), s["seat"], s["item"])
        series.setdefault(key, []).append(s)
    lags = []
    mag_errs = []
    for key, rows in series.items():
        rows.sort(key=lambda r: r["day"])
        truth = [r["true_held"] for r in rows]
        est = [r["est_held"] for r in rows]
        if max(truth or [0]) < 5 or len(rows) < 5 or max(est or [0]) < 1:
            continue
        t_turn = max(range(len(truth) - 1),
                     key=lambda i: abs(truth[i + 1] - truth[i]))
        e_turn = max(range(len(est) - 1),
                     key=lambda i: abs(est[i + 1] - est[i]))
        lags.append(abs(e_turn - t_turn))
        base = max(1, truth[t_turn + 1])
        mag_errs.append(abs(est[e_turn + 1] - truth[t_turn + 1]) / base)
    gate2 = {
        "n_series": len(lags),
        "median_lag_days": round(statistics.median(lags), 2) if lags else None,
        "magnitude_err_median": round(statistics.median(mag_errs), 4)
        if mag_errs else None,
        "pass": bool(lags) and statistics.median(lags) <= 1.0
        and statistics.median(mag_errs) <= 0.30,
    }
    by_item = {}
    for s in samples:
        by_item.setdefault(s["item"], []).append(
            abs((s["est_held"] or 0) - (s["true_held"] or 0)))
    gate3 = {
        "per_item_mae": {k: round(statistics.mean(v), 2)
                         for k, v in sorted(by_item.items()) if v},
        "per_item_max": {k: max(v) for k, v in sorted(by_item.items())
                         if v},
        "floor_segment_samples": len(floor),
    }
    return {"gate1_ch0_exact": gate1, "gate2_turning": gate2,
            "gate3_held_report": gate3,
            "overall_pass": bool(gate1["pass"] and gate2["pass"])}


def run_replay(module, data, samples, replay_id=""):
    module._OPP_OBSERVER.clear()
    module._MARKET_MEM.clear()
    last_day = {0: -1, 1: -1}
    opp_orders_today = {0: {}, 1: {}}       # seat -> item -> net units
    opp_buys_today = {0: set(), 1: set()}   # seat -> items bought today
    prev_obs = {0: None, 1: None}
    for seat, obs, orders in replay_stream(data):
        day = obs.get("day", 0)
        prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
        day_changed = day != last_day[seat] and last_day[seat] >= 0
        # feed the observer FIRST (legal fields only; self-deduped): at a
        # day boundary its account covers YESTERDAY's window, so the flow
        # and held it just produced pair with YESTERDAY's submitted orders
        module._opp_observer_update(obs, obs.get("private") or {})
        if day_changed:
            for item in module.BASE_PRICE:
                if item not in module.MARKET_PARAMS_EMB:
                    continue
                st = module._OPP_OBSERVER.get(seat) or {}
                flow = st.get("flow_hist", {}).get(item) or [None]
                price = (prev_obs[seat] or {}).get("_price", {}).get(item)
                samples.append({
                    "replay": replay_id, "seat": seat,
                    "day": last_day[seat], "item": item,
                    "ch0_net": flow[-1] if flow[-1] is not None else None,
                    "submitted_net": opp_orders_today[seat].get(item, 0),
                    "had_buys": item in opp_buys_today[seat],
                    "price": price,
                    "est_held": (st.get("held") or {}).get(item, 0),
                    "true_held": true_held(
                        (prev_obs[seat] or {}).get("_private"), item),
                })
            opp_orders_today[seat] = {}
            opp_buys_today[seat] = set()
        module._opp_note_orders(seat, day, obs.get("hour", 0), orders,
                                prices)
        opp = 1 - seat
        for o in orders:
            if isinstance(o, list) and len(o) >= 3 and o[0] in (
                    "SELL", "BUY_PRODUCT") and o[1] in module.BASE_PRICE:
                sign = 1 if o[0] == "SELL" else -1
                opp_orders_today[opp][o[1]] = \
                    opp_orders_today[opp].get(o[1], 0) + sign * o[2]
                if o[0] == "BUY_PRODUCT":
                    opp_buys_today[opp].add(o[1])
        prev_obs[seat] = {"_private": obs.get("private"),
                          "_price": dict(prices)}
        last_day[seat] = day


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--replays", nargs="+", required=True)
    ap.add_argument("--out", default=str(
        SOFTWARE / "exports" / "probes" / "observer_v0.json"))
    args = ap.parse_args()
    files = []
    for pattern in args.replays:
        files.extend(sorted(glob.glob(pattern)))
    module = load_module()
    samples = []
    used = 0
    for path in files:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not data.get("steps"):
            continue
        run_replay(module, data, samples, replay_id=Path(path).stem)
        used += 1
    verdict = score(samples)
    payload = {"schema": "observer-v0/1.0", "replays": used,
               "samples": len(samples), "verdict": verdict}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    print(f"[observer-v0] {used} replays, {len(samples)} samples -> {out}")


if __name__ == "__main__":
    main()
