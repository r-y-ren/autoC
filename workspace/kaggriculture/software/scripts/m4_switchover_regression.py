#!/usr/bin/env python
"""Phase-B M4 switchover regression (scheduler design §7 M4 gate).

Protocol (per seed, both seats self-play):
  A: ROUTE_EXECUTOR_ENABLED=False  (v11.5 lineage: v72 authority)
  B: ROUTE_EXECUTOR_ENABLED=True   (four-layer pipeline live)
Then compares:
  * escapes        -- day-over-day herd DECREASES (the engine has no animal
                      sales, so any decrease is an escape).  NOTE: the
                      endgame stop-feeding policy (FM-O4) lets terminal
                      animals escape BY DESIGN, so the gate is non-
                      inferiority (B <= A), not absolute zero.
  * eod_overflow   -- shed+carried > 100 at any EOD snapshot (proxy via
                      telemetry shed_overflow max); M4 gate: not worse than A
  * rewards        -- non-inferiority: mean(B) >= mean(A) - 5%
  * determinism    -- B run twice -> byte-identical action sequences
  * contract       -- all statuses DONE, no engine errors

--golden-only: skip the A/B, just freeze the current build's action-sequence
hashes (golden baseline) into exports/probes/m4_golden.json.

M5 NOTE (2026-09-03): the A/B mode is RETIRED -- v72 and the execution flag
were deleted with the transition code (scheduler §3.3/§7), so there is no
A arm to compare against.  The A/B verdict of record lives in
exports/probes/m4_switchover_ab.json (final: structural PASS, rewards 93%,
disclosed in JOURNAL).  Use --golden-only for determinism/golden freezes.

Usage:
  python scripts/m4_switchover_regression.py [--seeds 7,8,9,101] [--golden-only]
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
from kgenv.engine import run_episode  # noqa: E402

AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"
STATE_NAMES = ("_MISSION_SHADOW", "_ROUTE_STATE", "_STATE", "_TARGETS",
               "_PLAN_MEM", "_STAGE_MEM", "_MARKET_MEM", "_OPP_OBSERVER",
               "_INTERFERENCE_MEM", "_SELL_PLAN_MEM", "_REPLAN_MEM",
               "_D29_SELL_QUEUE", "_INTERFERENCE_LOG",
               "_SELL_BATCH_EMITTED", "_ASSIGN_MEM")


def load_module():
    spec = importlib.util.spec_from_file_location("m4_main", AGENT_MAIN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_module_state(module):
    for name in STATE_NAMES:
        st = getattr(module, name, None)
        if isinstance(st, dict):
            st.clear()
        elif isinstance(st, list):
            del st[:]
    if hasattr(module, "reset_telemetry"):
        module.reset_telemetry()


def run_episode_probe(module, seed, steps):
    """One episode: returns metrics + per-turn action hashes.

    Escapes split (per this docstring's own FM-O4 note: the endgame
    stop-feeding policy lets terminal animals escape BY DESIGN): a herd
    drop OBSERVED on day D is caused by the (D-1) EOD refresh; drops
    from the stop-feed window onward (D-1 >= ENDGAME_DAY-1, i.e. the
    engine's no-feed-by-policy days) are counted separately as
    endgame_terminal and reported, not gated.  Everything before that
    window is a hard escape -- a genuine feeding failure -- and IS the
    gate (B <= A).
    """
    endgame_from = getattr(module, "ENDGAME_DAY", 28) - 1
    metrics = {"escapes": 0, "escapes_endgame": 0, "statuses": None,
               "rewards": None, "turns": 0}
    hashes = []
    herd_prev = {0: None, 1: None}
    overflow_max = 0

    def make_wrapped():
        def wrapped(obs):
            action = module.agent(obs)
            try:
                metrics["turns"] += 1
                hashes.append(hashlib.sha256(json.dumps(
                    action, sort_keys=True).encode()).hexdigest()[:12])
                player = int(module._get(obs, "player", 0))
                day = int(module._get(obs, "day", 0))
                farm = module._get(obs, "farms", [{}] * (player + 1))[player]
                herd = sum(1 for row in module._get(farm, "tiles", []) or []
                           for t in row
                           if isinstance(t, dict) and "animal" in t)
                prev = herd_prev.get(player)
                herd_prev[player] = herd
                if prev is not None and herd < prev:
                    if day - 1 >= endgame_from:
                        metrics["escapes_endgame"] += prev - herd
                    else:
                        metrics["escapes"] += prev - herd
                private = module._get(obs, "private", {}) or {}
                shed = sum(v for v in (module._get(private, "shed", {})
                                       or {}).values()
                           if isinstance(v, (int, float)))
                invs = module._get(private, "inventories", []) or []
                carried = sum(v for inv in invs if inv
                              for v in inv.values()
                              if isinstance(v, (int, float)) and v > 0)
                overflow_max = max(overflow_max, shed + carried - 100) \
                    if False else 0  # placeholder replaced below
            except Exception:
                pass
            return action
        return wrapped

    # overflow tracked via telemetry is simpler & already maintained
    wrapped0 = make_wrapped()
    result = run_episode(wrapped0, wrapped0, seed, episode_steps=steps)
    metrics["statuses"] = result["statuses"]
    metrics["rewards"] = result["rewards"]
    snap = module.telemetry_snapshot()
    overflow = 0
    for seat, pstate in (snap.get("players") or {}).items():
        for day, day_state in (pstate.get("days") or {}).items():
            overflow = max(overflow, int(day_state.get("shed_overflow", 0)))
    metrics["overflow_max"] = overflow
    metrics["action_hash"] = hashlib.sha256(
        "|".join(hashes).encode()).hexdigest()
    return metrics


def run_ab(module, seeds, steps):
    out = {"seeds": seeds, "episodes": []}
    for seed in seeds:
        reset_module_state(module)
        module.ROUTE_EXECUTOR_ENABLED = False
        a = run_episode_probe(module, seed, steps)
        reset_module_state(module)
        module.ROUTE_EXECUTOR_ENABLED = True
        b = run_episode_probe(module, seed, steps)
        reset_module_state(module)
        module.ROUTE_EXECUTOR_ENABLED = True
        b2 = run_episode_probe(module, seed, steps)
        out["episodes"].append({
            "seed": seed, "A_off": a, "B_on": b,
            "B_deterministic": b["action_hash"] == b2["action_hash"],
        })
    eps = out["episodes"]
    mean_a = sum(e["A_off"]["rewards"][0] + e["A_off"]["rewards"][1]
                 for e in eps) / len(eps)
    mean_b = sum(e["B_on"]["rewards"][0] + e["B_on"]["rewards"][1]
                 for e in eps) / len(eps)
    escapes_b = sum(e["B_on"]["escapes"] for e in eps)
    escapes_a = sum(e["A_off"]["escapes"] for e in eps)
    escapes_b_end = sum(e["B_on"]["escapes_endgame"] for e in eps)
    escapes_a_end = sum(e["A_off"]["escapes_endgame"] for e in eps)
    overflow_b = max(e["B_on"]["overflow_max"] for e in eps)
    overflow_a = max(e["A_off"]["overflow_max"] for e in eps)
    verdict = {
        "mean_reward_A": round(mean_a, 1), "mean_reward_B": round(mean_b, 1),
        "reward_delta_pct": round((mean_b - mean_a) / max(1.0, mean_a) * 100, 2),
        "escapes_A": escapes_a, "escapes_B": escapes_b,
        "escapes_A_endgame": escapes_a_end,
        "escapes_B_endgame": escapes_b_end,
        "overflow_A": overflow_a, "overflow_B": overflow_b,
        "all_done": all("DONE" in e["B_on"]["statuses"] for e in eps),
        "deterministic": all(e["B_deterministic"] for e in eps),
    }
    verdict["pass"] = (verdict["all_done"] and verdict["deterministic"]
                       and escapes_b <= escapes_a
                       and overflow_b <= overflow_a
                       and mean_b >= mean_a * 0.95)
    out["verdict"] = verdict
    return out


def run_golden(module, seeds, steps):
    frozen = {}
    for seed in seeds:
        reset_module_state(module)
        m = run_episode_probe(module, seed, steps)
        frozen[str(seed)] = m["action_hash"]
    return {"schema": "m4-golden/1.0", "action_hash": frozen}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default="7,8,9,101")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--golden-only", action="store_true")
    args = ap.parse_args()
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    module = load_module()
    if args.golden_only:
        payload = run_golden(module, seeds, args.episode_steps)
        dest = SOFTWARE / "exports" / "probes" / "m4_golden.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        print(json.dumps(payload, indent=1))
        print(f"[m4-golden] frozen -> {dest}")
        return
    if not hasattr(module, "ROUTE_EXECUTOR_ENABLED"):
        sys.exit("[m4-ab] RETIRED at M5: v72 and the flag are deleted; "
                 "use --golden-only (see docstring)")
    payload = run_ab(module, seeds, args.episode_steps)
    dest = SOFTWARE / "exports" / "probes" / "m4_switchover_ab.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(
        {k: v for k, v in payload.items() if k != "episodes"} |
        {"episode_digest": [
            {"seed": e["seed"],
             "rewards_A": e["A_off"]["rewards"],
             "rewards_B": e["B_on"]["rewards"],
             "escapes_A": e["A_off"]["escapes"],
             "escapes_B": e["B_on"]["escapes"],
             "overflow_A": e["A_off"]["overflow_max"],
             "overflow_B": e["B_on"]["overflow_max"],
             "B_deterministic": e["B_deterministic"]}
            for e in payload["episodes"]]}, indent=1), encoding="utf-8")
    print(json.dumps(payload["verdict"], indent=1))
    print(f"[m4-ab] -> {dest}")


if __name__ == "__main__":
    main()
