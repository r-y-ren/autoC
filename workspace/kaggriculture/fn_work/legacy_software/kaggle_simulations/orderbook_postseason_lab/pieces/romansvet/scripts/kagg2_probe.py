"""Why does kagg2 beat some of our thetas and lose to others? Instrumented games.

`scripts/eval_vs_baselines.py` reports the margin and nothing about *how* it
was earned. kaggriculture2/main.py carries three opponent-signature overlays
that only switch on against a herd that looks a particular way -- the MD
counter (`_v17_is_md_family`, latches from step 160 on
`(quadrants>=2 and cows>=4 and sheep<=2) or cows>=9` read off *our* public
board, then front-runs our predicted MELON/MILK/STRAWBERRY/WOOL sells at
twice the predicted size), the R5 counter (`_v17_is_r5_family`, from step 24
on `sheep>=4 and cows<=3`) and the clone preemption (`_preempt_shift`, steps
120-680, gated on `_clone_distance(obs) <= 6`). This script plays the same
games the tracker plays and writes down, per game, which of those fired.

Nothing here may change what kagg2 does, or the numbers stop being about the
tracker's games. Two properties keep that true:

* The opponent is loaded exactly the way `kaggle_environments.agent`'s
  `callable_agent` loads a file agent -- same source text, same
  `get_last_callable(raw, path=path)`, same `__raw_path__` on the
  configuration, same argument-count trim -- so kagg2 gets a freshly exec'd
  module image per game, which is what a fresh `env.run` gives it in the
  tracker too. Its module-level `_V17_*_STATE` dicts therefore start empty in
  every game, whether or not the worker process is reused.
* Everything this file adds is a *read*. The two counter wrappers call the
  original and return its return value untouched; the preempt count, the
  latches and the branch are read out of kagg2's own module dicts after the
  agent has already returned its action; the clone distance and the herd
  signature are recomputed by calling kagg2's own pure helpers on the
  observation it was handed. Every recorder is wrapped in a bare `except`, so
  a bug in the instrumentation cannot push kagg2 down its own PASS fallback.

The proof that this holds is the `--check` flag: it diffs the per-game
mine/theirs against an archived `artifacts/kagg2_games/*.csv` row for row.
Same seeds, same seats, same money, or the probe is not measuring the games
the tracker measured.

Usage:
    scripts/kagg2_probe.py --theta T.npy --csv OUT.csv [--games 24]
        [--workers 3] [--kagg2 ../kaggriculture2/main.py]
        [--check artifacts/kagg2_games/flow4_10133.csv]
"""
import argparse, csv, os, sys, time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, "src")
# Appended for the same reason `eval_vs_baselines` appends it: the only names
# resolved through it are this repo's own sibling scripts.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eval_vs_baselines as ev
import plan_stats

#: Steps at which the herd signature kagg2 reads off our board is written down.
#: 160 is the first step the MD latch is allowed to fire, so `cows160` is the
#: composition that decides the game; the rest show where the herd went.
SIG_STEPS = (160, 200, 280, 400, 560, 700)

#: The four products both counters front-run.
COUNTER_ITEMS = ("MELON", "MILK", "STRAWBERRY", "WOOL")

CSV_HEADER = (
    "seed", "seat", "mine", "theirs", "margin", "win",
    "md_target", "md_latch_step", "md_fire_steps", "md_fire_qty",
    "r5_target", "r5_latch_step", "r5_fire_steps", "r5_fire_qty",
    "preempt_steps", "preempt_qty", "clone_min", "clone_mean",
    "branch",
    "cows160", "sheep160", "quads160",
    "cows_max", "sheep_min160", "quads_max",
    "cows_end", "sheep_end", "quads_end", "hands_end",
    "steps", "max_act_ms",
) + tuple(f"sig{s}" for s in SIG_STEPS)


def _sell_totals(action):
    """{item: quantity} over the SELL orders of a market list, read-only."""
    out = {}
    try:
        for order in (action.get("market") or []):
            if len(order) >= 3 and order[0] == "SELL":
                out[order[1]] = out.get(order[1], 0) + max(0, int(order[2] or 0))
    except Exception:
        pass
    return out


class Kagg2Probe:
    """A file agent that is kagg2, plus a notebook of what kagg2 did."""

    def __init__(self, path):
        self.path = path
        # `build_agent` falls back to the string itself when the path cannot be
        # read; a missing opponent should be a loud failure here instead.
        with open(path, "r", encoding="utf-8") as fh:
            self.raw = fh.read()
        self.fn = None
        self.g = None
        self.seat = None
        self.reset()

    def reset(self):
        self.md_latch = -1
        self.r5_latch = -1
        self.md_fire_steps = self.md_fire_qty = 0
        self.r5_fire_steps = self.r5_fire_qty = 0
        self.preempt_steps = self.preempt_qty = 0
        self.clone_min = 10 ** 9
        self.clone_sum = 0.0
        self.clone_n = 0
        self.branch = ""
        self.sig = {}
        self.cows_max = -1
        self.quads_max = -1
        self.sheep_min160 = 10 ** 9
        self.last_step = -1
        self.errors = 0

    # -- the agent the engine calls -------------------------------------
    def agent(self, observation, configuration):
        if self.fn is None:
            from kaggle_environments.agent import get_last_callable
            self.fn = get_last_callable(self.raw, path=self.path)
            self.g = self.fn.__globals__
            self._install()
        try:
            configuration["__raw_path__"] = self.path
        except Exception:
            pass
        args = [observation, configuration]
        if hasattr(self.fn, "__code__") and hasattr(self.fn.__code__, "co_argcount"):
            args = args[: self.fn.__code__.co_argcount]
        action = self.fn(*args)
        try:
            self._record(observation)
        except Exception:
            self.errors += 1
        return action

    # -- instrumentation -------------------------------------------------
    def _install(self):
        """Replace the two counters with pass-through recorders.

        `agent()` resolves them as module globals on every call, so rebinding
        the name is enough. The wrapper returns exactly what the original
        returned -- the recording is a comparison of two SELL tallies, both
        read out of dicts the original does not share with its result
        (`_v17_md_counter`/`_v17_r5_counter` both `_copy_action` first).
        """
        for name, slot in (("_v17_md_counter", "md"), ("_v17_r5_counter", "r5")):
            original = self.g.get(name)
            if original is None:
                continue
            self.g[name] = self._recorder(original, slot)

    def _recorder(self, original, slot):
        def wrapped(obs, action, step):
            try:
                before = _sell_totals(action)
            except Exception:
                before = None
            out = original(obs, action, step)
            if before is not None:
                try:
                    after = _sell_totals(out)
                    extra = sum(
                        max(0, after.get(k, 0) - before.get(k, 0)) for k in COUNTER_ITEMS
                    )
                    if extra > 0:
                        setattr(self, slot + "_fire_steps",
                                getattr(self, slot + "_fire_steps") + 1)
                        setattr(self, slot + "_fire_qty",
                                getattr(self, slot + "_fire_qty") + extra)
                except Exception:
                    self.errors += 1
            return out
        return wrapped

    def _record(self, obs):
        g = self.g
        seat = g["_seat"](obs)
        self.seat = seat
        step = int(g["_e279_step"](obs))
        self.last_step = step

        if g["_V17_MD_STATE"][seat].get("target") and self.md_latch < 0:
            self.md_latch = step
        if g["_V17_R5_STATE"][seat].get("target") and self.r5_latch < 0:
            self.r5_latch = step

        # `_repay_shift` clears the due at the top of the next step, so a
        # non-empty due after the action was built means the preemption fired
        # on this step -- and the due *is* the quantity it pulled forward.
        due = g["_SHIFT_STATE"][seat].get("due") or {}
        if due:
            self.preempt_steps += 1
            self.preempt_qty += sum(max(0, int(v or 0)) for v in due.values())

        expert = g["_E279_STATE"][seat].get("expert")
        if expert:
            self.branch = str(expert)

        if g["_PREEMPT_START"] <= step < g["_PREEMPT_STOP"]:
            distance = g["_clone_distance"](obs)
            self.clone_min = min(self.clone_min, distance)
            self.clone_sum += distance
            self.clone_n += 1

        if step >= 160:
            cows, sheep, quads = g["_v17_md_signature"](obs)
            self.cows_max = max(self.cows_max, cows)
            self.quads_max = max(self.quads_max, quads)
            self.sheep_min160 = min(self.sheep_min160, sheep)
            if step in SIG_STEPS:
                self.sig[step] = (cows, sheep, quads)

    def row(self):
        clone_mean = (self.clone_sum / self.clone_n) if self.clone_n else ""
        return {
            "md_target": int(self.md_latch >= 0),
            "md_latch_step": self.md_latch,
            "md_fire_steps": self.md_fire_steps,
            "md_fire_qty": self.md_fire_qty,
            "r5_target": int(self.r5_latch >= 0),
            "r5_latch_step": self.r5_latch,
            "r5_fire_steps": self.r5_fire_steps,
            "r5_fire_qty": self.r5_fire_qty,
            "preempt_steps": self.preempt_steps,
            "preempt_qty": self.preempt_qty,
            "clone_min": self.clone_min if self.clone_n else "",
            "clone_mean": f"{clone_mean:.2f}" if self.clone_n else "",
            "branch": self.branch,
            "cows160": self.sig.get(160, ("", "", ""))[0],
            "sheep160": self.sig.get(160, ("", "", ""))[1],
            "quads160": self.sig.get(160, ("", "", ""))[2],
            "cows_max": self.cows_max,
            "sheep_min160": self.sheep_min160 if self.sheep_min160 < 10 ** 9 else "",
            "quads_max": self.quads_max,
            "steps": self.last_step + 1,
            **{f"sig{s}": "|".join(str(v) for v in self.sig.get(s, ()))
               for s in SIG_STEPS},
        }


def _play(job):
    seed, seat, theta_path, kagg2_path = job
    from kaggle_environments import make
    from kagg3.agent import runtime

    macro = plan_stats.make_macro(np.load(theta_path).astype(np.float32))
    me = runtime.make_agent(macro)
    probe = Kagg2Probe(kagg2_path)

    env = make("kaggriculture", configuration={"seed": int(seed)})
    agents = [me, probe.agent] if seat == 0 else [probe.agent, me]
    # Forced on, not inferred: the tracker seats kagg2 as a file agent, so its
    # games all run with this repo's `kagg3` hidden. The probe seats the same
    # source through a callable, and has to hide the same modules to be
    # playing the same game.
    with ev._vendored_imports(True):
        env.run(agents)

    last = env.steps[-1][0].observation
    money = [f["money"] for f in last["farms"]]
    mine, theirs = (money[0], money[1]) if seat == 0 else (money[1], money[0])
    win = 1.0 if mine > theirs else (0.5 if mine == theirs else 0.0)
    ours = last["farms"][seat]
    cows = sheep = 0
    for row in (ours["tiles"] or []):
        for tile in (row or []):
            if isinstance(tile, dict):
                cows += int(tile.get("animal") == "COW")
                sheep += int(tile.get("animal") == "SHEEP")
    kagg2_seat = 1 - seat
    durations = [log[kagg2_seat].get("duration", 0.0)
                 for log in env.logs if len(log) > kagg2_seat]

    out = {
        "seed": int(seed), "seat": seat, "mine": mine, "theirs": theirs,
        "margin": mine - theirs, "win": win,
        "cows_end": cows, "sheep_end": sheep,
        "quads_end": len(ours["unlocked_quadrants"] or []),
        "hands_end": len(ours["hands"] or []),
        "max_act_ms": f"{1000 * max(durations or [0.0]):.1f}",
    }
    out.update(probe.row())
    if probe.errors:
        out["branch"] = (out["branch"] or "?") + f"!err{probe.errors}"
    return out


def _check(csv_path, rows):
    """Diff the probe's games against an archived tracker CSV, row for row."""
    want = {}
    with open(csv_path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["opponent"] == "starter":
                continue
            want[(int(r["seed"]), int(r["seat"]))] = (float(r["mine"]), float(r["theirs"]))
    bad = missing = 0
    for row in rows:
        key = (int(row["seed"]), int(row["seat"]))
        if key not in want:
            missing += 1
            continue
        if (float(row["mine"]), float(row["theirs"])) != want[key]:
            bad += 1
            print(f"  MISMATCH seed={key[0]} seat={key[1]} "
                  f"probe=({row['mine']},{row['theirs']}) archive={want[key]}")
    matched = len(rows) - missing
    print(f"check vs {csv_path}: {matched}/{len(rows)} games matched by (seed,seat), "
          f"{bad} money mismatches, {missing} not in archive")
    return bad == 0 and matched > 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--games", type=int, default=24, help="seeds (x2 seats)")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--seed-base", type=int, default=20260825,
                    help="must match remote_eval_kagg2.sh to reuse its games")
    ap.add_argument("--kagg2", default="../kaggriculture2/main.py")
    ap.add_argument("--check", help="archived tracker CSV to diff mine/theirs against")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed_base)
    seeds = rng.integers(0, 2 ** 31 - 1, args.games)
    jobs = [(s, seat, args.theta, args.kagg2) for s in seeds for seat in (0, 1)]

    t0 = time.time()
    with ProcessPoolExecutor(args.workers) as ex:
        rows = list(ex.map(_play, jobs))

    with open(args.csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, CSV_HEADER)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    margins = [r["margin"] for r in rows]
    latched = [r for r in rows if r["md_target"]]
    print(f"{len(rows)} games in {time.time()-t0:.0f}s  theta={args.theta}")
    print(f"  mean margin {np.mean(margins):+.0f}   win "
          f"{100*np.mean([r['win'] for r in rows]):.1f}%   "
          f"md latch {len(latched)}/{len(rows)}   "
          f"r5 latch {sum(r['r5_target'] for r in rows)}/{len(rows)}   "
          f"preempt>0 {sum(1 for r in rows if r['preempt_steps'] > 0)}/{len(rows)}")
    if args.check:
        ok = _check(args.check, rows)
        print("SANITY:", "PASS" if ok else "FAIL")
        if not ok:
            sys.exit(2)
