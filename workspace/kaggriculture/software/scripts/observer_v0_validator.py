#!/usr/bin/env python
"""OBS-4: offline V0 validator (opp_supply_observer_design.md §5.1).

Steps official replay JSONs through the agent's observer using ONLY legal
per-seat observation fields, then scores the estimates against the replay
ground truth (each seat's private.shed/inventories -- readable OFFLINE
only, never inside the agent):

  Gate 1  Ch0 integer accounting: report both requested and reconstructed
          executed net orders.  The hard gate uses executed quantities only
          when the shadow transition is fully attributable; requested is a
          diagnostic comparison, not an execution truth.
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
sys.path.insert(0, str(SOFTWARE))

from kgenv.replay_profile import _s_compare, _s_config, _s_snapshot, _s_step

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
    """Aggregate Ch0 accounting and opponent-held accuracy."""
    normal = [s for s in samples if s["price"] is not None
              and s["price"] > 1 and s["day"] > 1
              and s["item"] != "FERTILIZER"
              and not s.get("had_buys")]
    floor = [s for s in samples if s["price"] is not None
             and s["price"] <= 1]

    def exact_gate(field):
        eligible = [s for s in normal if s.get(field) is not None]
        exact = [s for s in eligible if s["ch0_net"] is not None
                 and s["ch0_net"] == s[field]]
        return {
            "normal_samples": len(eligible),
            "exact": len(exact),
            "share": round(len(exact) / len(eligible), 4)
            if eligible else None,
            "pass": bool(eligible) and len(exact) / len(eligible) >= 0.95,
        }

    gate1_requested = exact_gate("requested_net")
    gate1_filled = exact_gate("filled_net")
    gate1 = dict(gate1_filled)
    gate1["basis"] = "filled"
    gate1["fill_unavailable"] = gate1_filled["normal_samples"] == 0
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
    return {"gate1_ch0_exact": gate1,
            "gate1_requested_exact": gate1_requested,
            "gate1_filled_exact": gate1_filled,
            "gate2_turning": gate2,
            "gate3_held_report": gate3,
            "overall_pass": bool(gate1["pass"] and gate2["pass"])}


def run_replay(module, data, samples, replay_id=""):
    """Replay legal observer inputs and validated shadow fill attribution."""
    module.reset_observer()
    steps = data.get("steps") or []
    if not steps:
        return {"transitions": 0, "attributed": 0, "mismatches": 0}

    cfg = _s_config(data)
    seed = (data.get("info") or {}).get("seed")
    if seed is None:
        seed = (data.get("configuration") or {}).get("seed") or 0
    turns_per_day = max(1, int(cfg["turnsPerDay"]))
    initial_obs = [(steps[0][seat] or {}).get("observation") or {}
                   for seat in (0, 1)]
    state = _s_snapshot(initial_obs[0],
                        [obs.get("private") for obs in initial_obs])
    for seat, obs in enumerate(initial_obs):
        module._opp_observer_update(obs, obs.get("private") or {})

    requested = [{}, {}]
    filled = [{}, {}]
    buys = [set(), set()]
    fill_window_valid = [True, True]
    prev_obs = initial_obs
    attributed = mismatches = 0

    def add_net(bucket, seat, order, quantity_key=None):
        op = order.get("type") if isinstance(order, dict) else order[0]
        item = order.get("item") if isinstance(order, dict) else order[1]
        if op not in ("SELL", "BUY_PRODUCT") or item not in module.BASE_PRICE:
            return
        if isinstance(order, dict):
            n = order.get(quantity_key, 0)
        else:
            n = order[2] if len(order) >= 3 else 0
        if not isinstance(n, (int, float)):
            return
        sign = 1 if op == "SELL" else -1
        bucket[seat][item] = bucket[seat].get(item, 0) + sign * n
        if op == "BUY_PRODUCT":
            buys[seat].add(item)

    for t in range(1, len(steps)):
        entries = [steps[t][seat] or {} for seat in (0, 1)]
        actions = [entry.get("action") or {} for entry in entries]
        actual_obs = [entry.get("observation") or {} for entry in entries]
        pre = prev_obs[0]
        action_day = int(pre.get("day", 0))
        action_hour = int(pre.get("hour", 0))
        step_index = int(pre.get("step", t - 1))
        post_state, attr = _s_step(state, actions, step_index, cfg, seed)
        actual_privates = [obs.get("private") for obs in actual_obs]
        diff = _s_compare(post_state, actual_obs[0], actual_privates)
        fill_valid = not diff
        if fill_valid:
            attributed += 1
            state = post_state
        else:
            mismatches += 1
            state = _s_snapshot(actual_obs[0], actual_privates)

        # steps[t].action was chosen from steps[t-1].observation and belongs
        # to that transition/window, including the action crossing midnight.
        for seat in (0, 1):
            market_orders = list(actions[seat].get("market") or [])
            module._opp_note_orders(seat, action_day, action_hour,
                                    market_orders,
                                    (pre.get("market") or {}).get("prices") or {})
            opponent_view = 1 - seat
            for order in market_orders:
                if isinstance(order, list) and len(order) >= 3:
                    add_net(requested, opponent_view, order)
            if fill_valid:
                fills = list(attr["market"][seat]["orders"])
                module._opp_note_fills(seat, action_day, action_hour, fills)
                for order in fills:
                    add_net(filled, opponent_view, order, "filled")
            else:
                fill_window_valid[opponent_view] = False
                module._opp_note_fills(seat, action_day, action_hour, [],
                                       complete=False)

        for seat, obs in enumerate(actual_obs):
            previous_day = int(prev_obs[seat].get("day", 0))
            day = int(obs.get("day", 0))
            module._opp_observer_update(obs, obs.get("private") or {})
            if day == previous_day:
                continue
            st = module._OPP_OBSERVER.get(seat) or {}
            opponent = 1 - seat
            opponent_private = actual_obs[opponent].get("private") or {}
            prices = (prev_obs[seat].get("market") or {}).get("prices") or {}
            for item in module.BASE_PRICE:
                if item not in module.MARKET_PARAMS_EMB:
                    continue
                hist = st.get("flow_hist", {}).get(item) or [None]
                req = requested[seat].get(item, 0)
                fill = filled[seat].get(item, 0) \
                    if fill_window_valid[seat] and \
                    st.get("order_basis") == "filled" else None
                samples.append({
                    "replay": replay_id, "seat": seat,
                    "day": previous_day, "item": item,
                    "ch0_net": hist[-1] if hist[-1] is not None else None,
                    "requested_net": req, "submitted_net": req,
                    "filled_net": fill,
                    "had_buys": item in buys[seat],
                    "price": prices.get(item),
                    "est_held": (st.get("held") or {}).get(item, 0),
                    "true_held": true_held(opponent_private, item),
                })
            requested[seat] = {}
            filled[seat] = {}
            buys[seat] = set()
            fill_window_valid[seat] = True
        prev_obs = actual_obs

    return {"transitions": max(0, len(steps) - 1),
            "attributed": attributed, "mismatches": mismatches}


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
    attribution = {"transitions": 0, "attributed": 0, "mismatches": 0}
    for path in files:
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not data.get("steps"):
            continue
        stats = run_replay(module, data, samples, replay_id=Path(path).stem)
        for key in attribution:
            attribution[key] += stats[key]
        used += 1
    verdict = score(samples)
    payload = {"schema": "observer-v0/2.0", "replays": used,
               "samples": len(samples), "attribution": attribution,
               "verdict": verdict}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    print(f"[observer-v0] {used} replays, {len(samples)} samples -> {out}")


if __name__ == "__main__":
    main()
