"""Smoke boot: self-contained boot check for the Kaggriculture software stack.

Runs the exact Validation-Episode path (file-based submission agent playing
against itself on the official engine), plus output-contract checks, then
exits with a status code:

    0  all phases passed
    1  any phase failed
    2  watchdog timeout exceeded

Usage (from repo root or workspace/kaggriculture/software):
    python workspace/kaggriculture/software/smoke_boot.py
"""

from __future__ import annotations

import os
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

TIMEOUT_SECONDS = 300
WATCHDOG = True


def _watchdog():
    time.sleep(TIMEOUT_SECONDS)
    print(f"FAIL: watchdog timeout after {TIMEOUT_SECONDS}s", flush=True)
    os._exit(2)


def phase_env_boot() -> bool:
    """Official engine imports and boots; built-in agents load."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"episodeSteps": 24, "seed": 1},
               debug=True)
    env.run(["starter", "pass"])
    final = env.steps[-1]
    ok = all(s["status"] == "DONE" for s in final) and len(env.steps) == 24
    print(f"phase_env_boot: engine boot + 24-step episode -> "
          f"rewards={[s['reward'] for s in final]} ok={ok}")
    return ok


def release_episode_ok(result, expected_steps=720) -> bool:
    """Smoke/release verdict: completion always, liveness for full episodes."""
    activity = result.get("activity") or {}
    return (
        result.get("statuses") == ["DONE", "DONE"]
        and result.get("turns_played") == expected_steps
        and activity.get("completion_ok") is True
        and (expected_steps != 720 or activity.get("activity_ok") is True)
    )


def phase_submission_selfplay() -> bool:
    """Submission file agent vs itself (Validation-Episode style)."""
    from kgenv.arena import load_submission_agent
    from kgenv.engine import run_episode
    main_py = os.path.join(HERE, "kaggle_simulations", "agent", "main.py")
    if not os.path.isfile(main_py):
        print(f"phase_submission_selfplay: FAIL missing {main_py}")
        return False
    ok_all = True
    agent = load_submission_agent(main_py)
    # 2 short episodes + 1 full-length release episode.
    for seed, steps in ((7, 96), (8, 96), (9, 720)):
        result = run_episode(agent, agent, seed=seed, episode_steps=steps)
        statuses = result["statuses"]
        rewards = result["rewards"]
        ok = release_episode_ok(result, expected_steps=steps) and \
            all(isinstance(r, (int, float)) for r in rewards)
        activity = result.get("activity", {})
        print(f"phase_submission_selfplay: seed={seed} steps={steps} "
              f"rewards={rewards} statuses={statuses} "
              f"activity_ok={activity.get('activity_ok')} ok={ok}")
        ok_all = ok_all and ok
    return ok_all


def phase_contract() -> bool:
    """Match-result contract + replay-log write round-trip."""
    from kgenv.engine import run_episode, episode_contract_ok
    from kgenv.arena import load_submission_agent, run_match, write_replay_log
    import json, tempfile

    sub = load_submission_agent()
    res = run_match(sub, "starter", seed=42, episode_steps=48,
                    label_a="submission", label_b="starter")
    ok = res["contract_ok"] and res["winner_label"] in ("submission", "starter", None)
    with tempfile.TemporaryDirectory() as td:
        p = write_replay_log(td, [res])
        with open(p, encoding="utf-8") as f:
            entry = json.loads(f.readline())
        ok = ok and entry["players"] == ["submission", "starter"] \
            and entry["seed"] == 42 and len(entry["rewards"]) == 2
    print(f"phase_contract: run_match contract ok={res['contract_ok']}, "
          f"replay log round-trip ok={ok}")
    return ok


def phase_gym() -> bool:
    """Gym-style wrapper loop advances and reports money."""
    from kgenv.gym_env import KaggricultureGym
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    obs = env.reset(seed=3)
    ok = obs is not None and "farms" in obs
    for _ in range(48):
        _, reward, terminated, info = env.step(
            {"farmer": ["PASS"], "hands": [], "market": []})
        if terminated:
            break
    ok = ok and info.get("day", 0) >= 1 and isinstance(info.get("money"), list)
    print(f"phase_gym: stepped to day={info.get('day')} "
          f"money={info.get('money')} ok={ok}")
    return ok


def main() -> int:
    if WATCHDOG:
        t = threading.Thread(target=_watchdog, daemon=True)
        t.start()
    t0 = time.perf_counter()
    phases = [
        ("env_boot", phase_env_boot),
        ("submission_selfplay", phase_submission_selfplay),
        ("contract", phase_contract),
        ("gym", phase_gym),
    ]
    results = {}
    for name, fn in phases:
        try:
            results[name] = fn()
        except Exception as exc:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            results[name] = False
    dt = time.perf_counter() - t0
    all_ok = all(results.values())
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print(f"smoke_boot: {'PASS' if all_ok else 'FAIL'} "
          f"({dt:.1f}s, phases={len(results)})")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
