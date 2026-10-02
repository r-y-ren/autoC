"""The in-sim selector is a proxy, and after ~1.5k generations it stops
tracking the thing it stands for: flow23's three consecutive in-sim records
scored 64.6%, 52.1% and 47.9% against the real `kagg2` while the in-sim margin
they were taken on rose monotonically. `best_abs.npy` is what `--promote`
ships, so the deliverable was getting worse on the only measurement that
counts.

`--real-gate` makes the in-sim record a *nomination*: the candidate is played
against a packaged opponent in the real engine and the record moves only if
that number improved. The eval is a real subprocess, so the properties that
matter are as much about plumbing as about the rule -- the trainer must never
block on it, only one may be in flight, a killed run must not leave a worker
pool behind, and a run without the flag must be the run that came before it.

Every eval here is a *fake* `eval_vs_baselines.py`: it writes the same CSV with
numbers this file dictates, so the whole file runs in seconds and no test ever
starts the real engine.
"""
from __future__ import annotations

import json
import os
import signal
import sys
import time
from types import SimpleNamespace

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest
import train as T

from kagg3.es.train import NO_BEST, Config, RealGate, Trainer, read_eval_csv

#: `scripts/eval_vs_baselines.py:CSV_HEADER`, which is the contract the gate
#: reads. Spelled out rather than imported so that a change to it fails *here*
#: -- importing the script would make the two agree by construction.
HEADER = ("seed", "opponent", "seat", "mine", "theirs",
          "moves", "move_turns", "noops", "unsold", "quads")

#: A stand-in for `scripts/eval_vs_baselines.py`: same flags, same CSV, and the
#: per-game numbers come from `fake_plan.json` in the run directory (one entry
#: per eval, consumed in order) instead of from the engine. It also appends its
#: argv and the theta it was handed to `fake_calls.jsonl`, which is how the
#: tests below check *what* was launched.
FAKE_EVAL = '''
import argparse, csv, json, os, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--theta")
ap.add_argument("--opponents", nargs="*")
ap.add_argument("--games", type=int)
ap.add_argument("--workers", type=int)
ap.add_argument("--seed-base", type=int)
ap.add_argument("--seed-per-opponent", action="store_true")
ap.add_argument("--csv")
a = ap.parse_args()

run = os.path.dirname(os.path.abspath(a.csv))
with open(os.path.join(run, "fake_calls.jsonl"), "a") as fh:
    fh.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(),
                         "theta": [float(x) for x in np.load(a.theta)]}) + "\\n")

plan_path = os.path.join(run, "fake_plan.json")
plan = json.load(open(plan_path)) if os.path.isfile(plan_path) else []
step = plan.pop(0) if plan else {"wins": 1, "losses": 1,
                                 "win_margin": 1.0, "loss_margin": 1.0}
with open(plan_path, "w") as fh:
    json.dump(plan, fh)

if step.get("hang"):
    # A pool the parent has to reap: a grandchild in the same process group,
    # exactly as the real script's ProcessPoolExecutor workers are.
    import subprocess
    kid = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
    with open(os.path.join(run, "fake_kid.pid"), "w") as fh:
        fh.write(str(kid.pid))
    import time
    time.sleep(600)
if step.get("rc"):
    sys.exit(int(step["rc"]))           # a crashed eval writes no CSV

rows = ([(100000.0 + float(step["win_margin"]), 100000.0)] * int(step["wins"])
        + [(100000.0, 100000.0 + float(step["loss_margin"]))] * int(step["losses"]))
with open(a.csv, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow({header})
    for i, (mine, theirs) in enumerate(rows):
        # Seeded off the base, like the real evaluator: two bases are two sets
        # of boards, which is what makes a leg pair with its own base's leg and
        # not with another round's.
        w.writerow([a.seed_base + i, a.opponents[0], i % 2, mine, theirs,
                    0, 0, 0, 0, 4])
'''.replace("{header}", repr(list(HEADER)))


def _expect(step):
    """The (win rate, mean margin) a plan entry produces, computed the way the
    gate is *not* allowed to compute it (independently, from the entry)."""
    n = step["wins"] + step["losses"]
    win = step["wins"] / n
    margin = (step["wins"] * step["win_margin"]
              - step["losses"] * step["loss_margin"]) / n
    return win, margin


class _Fake:
    """A gate factory whose evals are the fake script."""

    def __init__(self, tmp_path):
        self.root = tmp_path
        self.script = os.path.join(str(tmp_path), "fake_eval.py")
        with open(self.script, "w") as fh:
            fh.write(FAKE_EVAL)
        self.run = os.path.join(str(tmp_path), "run")
        os.makedirs(self.run, exist_ok=True)

    def plan(self, steps):
        with open(os.path.join(self.run, "fake_plan.json"), "w") as fh:
            json.dump(list(steps), fh)

    def gate(self, steps=(), opponent="opp/main.py", **kw):
        self.plan(steps)
        kw.setdefault("games", 2)
        kw.setdefault("workers", 1)
        kw.setdefault("seed_base", 20260825)
        return RealGate(self.run, opponent, script=self.script,
                        python=sys.executable, cwd=str(self.root), **kw)

    def calls(self):
        p = os.path.join(self.run, "fake_calls.jsonl")
        if not os.path.isfile(p):
            return []
        with open(p) as fh:
            return [json.loads(l) for l in fh if l.strip()]


@pytest.fixture
def fake(tmp_path):
    f = _Fake(tmp_path)
    yield f


def _through(tr):
    """Settle the in-flight eval *through the trainer*.

    The record move is `Trainer._poll_real_gate`'s, so a test about what
    `best_abs_theta` does has to go through it rather than through the gate.
    """
    tr.real_gate.proc.wait()
    tr.last_real_gate = tr._poll_real_gate()
    return tr.last_real_gate


def _settle(gate):
    """Block until the in-flight eval exits, then take its verdict.

    A *test* may wait; the trainer never does. `poll` is a `waitpid(WNOHANG)`
    and returns `None` while the child runs, which is the property
    `test_the_trainer_never_blocks_on_an_eval` pins.
    """
    assert gate.proc is not None, "nothing in flight"
    gate.proc.wait()
    return gate.poll()


# --------------------------------------------------------- reading the CSV

def _write_csv(path, rows):
    import csv as _csv
    with open(path, "w", newline="") as fh:
        w = _csv.writer(fh)
        w.writerow(HEADER)
        for i, (mine, theirs) in enumerate(rows):
            w.writerow([i, "kagg2", i % 2, mine, theirs, 0, 0, 0, 0, 4])


def test_the_csv_is_scored_the_way_the_tracker_scores_it(tmp_path):
    """A tie is half a win -- `eval_vs_baselines.py` and
    `scripts/kagg2_track_row.py` both say so, and a gate that scored it
    otherwise would rank a policy differently from the tracker row an operator
    compares it against."""
    p = str(tmp_path / "g.csv")
    _write_csv(p, [(110_000, 100_000), (100_000, 120_000), (5, 5)])
    win, margin, n = read_eval_csv(p)
    assert (win, n) == (0.5, 3)                     # 1 + 0 + 0.5 over 3
    assert margin == pytest.approx((10_000 - 20_000 + 0) / 3)


def test_an_unreadable_csv_is_no_reading_at_all(tmp_path):
    """`None`, not a zero: a missing or truncated file has to be a *failed*
    eval (the incumbent stands), and 0.0 would be a real reading that loses
    every comparison and would be recorded as one."""
    assert read_eval_csv(str(tmp_path / "nope.csv")) is None
    p = str(tmp_path / "empty.csv")
    _write_csv(p, [])
    assert read_eval_csv(p) is None
    with open(str(tmp_path / "junk.csv"), "w") as fh:
        fh.write("a,b\n1,2\n")
    assert read_eval_csv(str(tmp_path / "junk.csv")) is None


# ------------------------------------------------------------ the subprocess

def test_the_eval_is_the_tracker_s_own_invocation(fake):
    """Same script, same flags, same seed base: a gate row and a tracker row
    have to be the same games, or the two numbers cannot be compared."""
    gate = fake.gate([{"wins": 3, "losses": 1, "win_margin": 8.0,
                       "loss_margin": 2.0}], games=2, workers=3,
                     seed_base=20260825)
    theta = np.arange(5, dtype=np.float32)
    gate.propose(theta, 700)
    res = _settle(gate)

    call, = fake.calls()
    argv = call["argv"]
    assert argv[argv.index("--opponents") + 1] == "opp/main.py"
    assert argv[argv.index("--games") + 1] == "2"
    assert argv[argv.index("--workers") + 1] == "3"
    assert argv[argv.index("--seed-base") + 1] == "20260825"
    assert argv[argv.index("--csv") + 1] == gate.csv_path
    # The candidate is handed over as a file the workers load, and it is the
    # theta that was nominated -- not the trainer's live one, which has moved
    # on by the time the eval finishes.
    assert call["theta"] == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert argv[argv.index("--theta") + 1] == gate.theta_path

    win, margin = _expect({"wins": 3, "losses": 1, "win_margin": 8.0,
                           "loss_margin": 2.0})
    assert (res["win"], res["margin"]) == (win, pytest.approx(margin))
    assert res["gen"] == 700 and res["games"] == 4


def test_one_opponent_is_the_command_line_it_always_was(fake):
    """The field is a superset, not a rewrite: with a single opponent the
    argv is byte-identical to the one the gate built before fields existed, so
    a run started on the old flag measures exactly the games it used to."""
    gate = fake.gate([{"wins": 2, "losses": 2, "win_margin": 1.0,
                       "loss_margin": 1.0}], games=2, workers=1,
                     seed_base=20260825)
    gate.propose(np.zeros(3, np.float32), 11)
    _settle(gate)

    call, = fake.calls()
    assert call["argv"] == [
        "--theta", gate.theta_path, "--opponents", "opp/main.py",
        "--games", "2", "--workers", "1",
        "--seed-base", "20260825", "--csv", gate.csv_path]


def test_the_seed_draw_is_shared_unless_the_flag_asks_otherwise(fake):
    """`--seed-per-opponent` is opt-in and appended, so the argv of a gate
    that does not ask for it is the one every gated run before the flag
    launched (`test_one_opponent_is_the_command_line_it_always_was` pins that
    argv exactly). With it, the evaluator draws a seed list per member of the
    field, and a leg of k opponents samples games*k seeds instead of games --
    which is where a leg's noise lives: the per-seed paired win difference has
    an sd of ~0.165 across seeds and correlates only weakly across opponents.
    """
    gate = fake.gate([_step(2, 2)], opponent="a/main.py,b/main.py")
    assert gate.seed_per_opponent is False
    gate.propose(np.zeros(3, np.float32), 5)
    _settle(gate)
    assert "--seed-per-opponent" not in fake.calls()[-1]["argv"]

    on = fake.gate([_step(3, 1)], opponent="a/main.py,b/main.py",
                   seed_per_opponent=True)
    assert on.seed_per_opponent is True
    on.propose(np.zeros(3, np.float32), 6)
    _settle(on)
    argv = fake.calls()[-1]["argv"]
    assert argv[-1] == "--seed-per-opponent"          # appended, not inserted
    assert argv.count("--seed-per-opponent") == 1
    # And nothing else about the leg moved: same games, same base, same CSV.
    assert argv[argv.index("--games") + 1] == "2"
    assert argv[argv.index("--seed-base") + 1] == "20260825"


def test_the_saved_seed_draw_is_read_but_the_command_line_wins(fake):
    """Like `min_gain`, `seed_per_opponent` is written so a resume can *say*
    it changed and is not restored: it is a draw, not a measurement, and the
    saved bar stays the number it was. A state written before the flag existed
    carries no key, which is the one shared list those legs were played on."""
    gate = fake.gate([], seed_per_opponent=True)
    gate.save()
    with open(os.path.join(gate.run_dir, "real_gate.json")) as fh:
        state = json.load(fh)
    assert state["seed_per_opponent"] is True
    assert RealGate.seed_per_opponent_of(state) is True

    back = fake.gate([], seed_per_opponent=False)
    assert RealGate.seed_per_opponent_of(back.load(gate.run_dir)) is True
    assert back.seed_per_opponent is False

    # The legacy state, which has never heard of the key.
    del state["seed_per_opponent"]
    with open(os.path.join(gate.run_dir, "real_gate.json"), "w") as fh:
        json.dump(state, fh)
    on = fake.gate([], seed_per_opponent=True)
    assert RealGate.seed_per_opponent_of(on.load(gate.run_dir)) is False
    assert on.seed_per_opponent is True
    assert RealGate.seed_per_opponent_of({}) is False
    assert RealGate.seed_per_opponent_of({"seed_per_opponent": None}) is False


def test_a_field_is_one_flag_with_one_argv_entry_per_opponent(fake):
    """One packaged agent is one thing to overfit, so the gate measures
    against a FIELD. `eval_vs_baselines.py` takes `--opponents` as `nargs="*"`
    and plays `--games` seeds x 2 seats against each, pooling them into the
    one CSV `read_eval_csv` scores -- but only if the members arrive as
    separate argv entries. A comma-joined string is accepted by argparse and
    becomes one opponent whose `main.py` does not exist, i.e. a whole gate leg
    that measures nothing, so the absence of a comma is the assertion."""
    gate = fake.gate([{"wins": 3, "losses": 1, "win_margin": 4.0,
                       "loss_margin": 1.0}],
                     opponent="a/main.py,b/main.py")
    assert gate.opponents == ("a/main.py", "b/main.py")
    gate.propose(np.zeros(3, np.float32), 42)
    _settle(gate)

    call, = fake.calls()
    argv = call["argv"]
    i = argv.index("--opponents")
    assert argv[i + 1:i + 3] == ["a/main.py", "b/main.py"]
    assert argv[i + 3] == "--games"          # the list ends where it should
    assert argv.count("--opponents") == 1
    assert [a for a in argv if "," in a] == []


def test_the_field_can_be_given_as_a_list_or_as_one_string(tmp_path):
    """`--real-gate-opponent` spells the field with commas because it is one
    command-line word; `real_gate.json` and `setup_real_gate` hand over a
    list. Both are the same field, and whitespace around a comma is an
    operator's, not a path's."""
    assert RealGate.as_field("a/main.py") == ("a/main.py",)
    assert RealGate.as_field("a/main.py, b/main.py") == ("a/main.py",
                                                         "b/main.py")
    assert RealGate.as_field(["a/main.py", "b/main.py"]) == ("a/main.py",
                                                             "b/main.py")
    assert RealGate.as_field(["a/main.py,b/main.py"]) == ("a/main.py",
                                                          "b/main.py")
    assert RealGate.as_field("") == () and RealGate.as_field(None) == ()
    # And the one-string spelling of the field survives on the attribute the
    # startup line and the older JSON both read.
    g = RealGate(str(tmp_path), ["a/main.py", "b/main.py"])
    assert g.opponent == "a/main.py,b/main.py"


def test_the_trainer_never_blocks_on_an_eval(fake):
    """`poll` returns `None` while the child runs and never waits. The whole
    point of the flag is a 3-minute measurement inside a run whose generations
    cost seconds."""
    gate = fake.gate([{"hang": True}])
    gate.propose(np.zeros(3, np.float32), 1)
    t0 = time.time()
    for _ in range(50):
        assert gate.poll() is None
    assert time.time() - t0 < 5.0
    assert gate.proc is not None and gate.proc.poll() is None
    gate.close()


# --------------------------------------------------------------- the verdict

def _step(wins, losses, win_margin=10_000.0, loss_margin=10_000.0):
    return {"wins": wins, "losses": losses, "win_margin": win_margin,
            "loss_margin": loss_margin}


def test_the_first_reading_is_the_baseline_and_a_worse_one_is_refused(fake):
    """There is nothing to beat until something has been measured, so the
    first result takes the record whatever it says; after that the rule is
    strict improvement."""
    gate = fake.gate([_step(3, 1), _step(1, 3)], games=2)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    first = _settle(gate)
    assert first["accepted"] and first["baseline"] and gate.have_record
    assert (gate.win, gate.record_gen) == (0.75, 10)

    gate.propose(np.full(3, 2.0, np.float32), 20)
    second = _settle(gate)
    assert second["accepted"] is False and second["baseline"] is False
    assert second["incumbent_win"] == 0.75
    # The incumbent is untouched by a refusal, and the counters say which.
    assert (gate.win, gate.record_gen) == (0.75, 10)
    assert (gate.accepts, gate.rejects, gate.evals) == (1, 1, 2)


def test_a_tied_win_rate_is_broken_by_the_margin(fake):
    """48 games resolve the win rate in steps of 1/96, so ties are routine and
    a tie that could not be broken would freeze the record at the first policy
    to reach that rate."""
    gate = fake.gate([_step(2, 2, 10_000.0, 10_000.0),    # 50%, margin 0
                      _step(2, 2, 30_000.0, 10_000.0),    # 50%, margin +10k
                      _step(2, 2, 30_000.0, 10_000.0)])   # 50%, same margin
    gate.propose(np.zeros(3, np.float32), 1)
    _settle(gate)
    assert (gate.win, gate.margin) == (0.5, 0.0)

    gate.propose(np.zeros(3, np.float32), 2)
    assert _settle(gate)["accepted"] is True
    assert (gate.win, gate.margin) == (0.5, 10_000.0)

    # Equal on both is not an improvement: the record is a strict one, or a
    # re-measurement of the same policy would keep taking it.
    gate.propose(np.zeros(3, np.float32), 3)
    assert _settle(gate)["accepted"] is False


def test_metric_margin_selects_on_the_margin_alone(fake):
    """`--real-gate-metric margin` for a run whose objective is the coin gap:
    the same pair of readings goes the other way under `win`."""
    readings = [_step(2, 2, 10_000.0, 10_000.0),          # 50%, 0
                _step(1, 3, 90_000.0, 10_000.0)]          # 25%, +15k
    gate = fake.gate(list(readings), metric="margin")
    gate.propose(np.zeros(3, np.float32), 1)
    _settle(gate)
    gate.propose(np.zeros(3, np.float32), 2)
    assert _settle(gate)["accepted"] is True
    assert gate.win == 0.25 and gate.margin == pytest.approx(15_000.0)

    other = fake.gate(list(readings))                     # metric="win"
    other.propose(np.zeros(3, np.float32), 1)
    _settle(other)
    other.propose(np.zeros(3, np.float32), 2)
    assert _settle(other)["accepted"] is False


# ------------------------------------------------- how big an improvement

def test_the_threshold_is_off_by_default_and_the_old_rule_stands(fake):
    """`--real-gate-min-gain` defaults to 0, and at 0 `beats` is the rule this
    build has always had: strict improvement on the win rate, ties broken by
    the margin, and the first reading of all taking the record unopposed."""
    gate = fake.gate([])
    assert gate.min_gain == 0.0
    assert gate.beats(0.51, 0.0, 0.50, 0.0) is True
    assert gate.beats(0.50, 1.0, 0.50, 0.0) is True          # the tie-break
    assert gate.beats(0.50, 0.0, 0.50, 0.0) is False
    assert gate.beats(0.49, 9e9, 0.50, 0.0) is False
    assert gate.beats(0.0, -9e9, None, None) is True         # the baseline

    # And on the margin metric, likewise.
    m = fake.gate([], metric="margin")
    assert m.beats(0.0, 1.0, 1.0, 0.0) is True
    assert m.beats(1.0, 0.0, 0.0, 0.0) is False


def test_a_gain_under_the_threshold_is_not_an_improvement(fake):
    """The gate reads 128-256 games, where the win rate's sd is 3-4 points, so
    "any excess at all" moves the record on one extra win: flow59 accepted gen
    200 on a paired 47.7% over 46.9% and confirmed it pooled at 46.1%, against
    an incumbent that had read 53.5%. The threshold is the cheap half of a
    significance test -- and it retires the tie-break, because a margin cannot
    make up a win-rate gap the threshold calls too small."""
    gate = fake.gate([], min_gain=0.03)
    assert gate.beats(0.52, 0.0, 0.50, 0.0) is False         # +2pp: noise
    assert gate.beats(0.53, 0.0, 0.50, 0.0) is True          # +3pp: the bar
    assert gate.beats(0.60, 0.0, 0.50, 0.0) is True
    assert gate.beats(0.50, 50_000.0, 0.50, 0.0) is False    # no tie-break
    assert gate.beats(0.0, -9e9, None, None) is True         # still baseline

    # End to end, through a real (fake-scripted) eval: 50% then 75%, which the
    # strict rule takes and a 30-point threshold does not.
    readings = [_step(2, 2), _step(3, 1)]
    strict = fake.gate(list(readings), games=2)
    strict.propose(np.zeros(3, np.float32), 1)
    _settle(strict)
    strict.propose(np.zeros(3, np.float32), 2)
    assert _settle(strict)["accepted"] is True
    assert strict.win == 0.75

    picky = fake.gate(list(readings), games=2, min_gain=0.30)
    picky.propose(np.zeros(3, np.float32), 1)
    assert _settle(picky)["accepted"] is True                # the baseline
    picky.propose(np.zeros(3, np.float32), 2)
    refused = _settle(picky)
    assert refused["accepted"] is False and refused["win"] == 0.75
    assert (picky.win, picky.record_gen) == (0.5, 1)         # bar unmoved


def test_the_threshold_is_in_the_units_of_the_metric(fake):
    """Under `--real-gate-metric margin` the gain is coins, and the win rate
    has no say -- the same asymmetry the metric already had."""
    gate = fake.gate([], metric="margin", min_gain=500.0)
    assert gate.beats(0.0, 10_400.0, 1.0, 10_000.0) is False
    assert gate.beats(0.0, 10_500.0, 1.0, 10_000.0) is True
    assert gate.beats(0.0, 10_500.0, 1.0, 10_000.0) is True
    # A win-rate landslide with a margin that has not moved is still refused.
    assert gate.beats(1.0, 10_000.0, 0.0, 10_000.0) is False
    assert gate.beats(0.0, -9e9, None, None) is True

    # The same numbers under `win`, whose own threshold is a win-rate gap, go
    # the other way -- which is what "in the units of the metric" means. 500
    # coins there would be a threshold no reading can ever clear.
    w = fake.gate([], min_gain=0.03)
    assert w.beats(1.0, 10_000.0, 0.0, 10_000.0) is True
    assert w.beats(0.0, 9e9, 1.0, 10_000.0) is False


def test_a_negative_threshold_is_refused(fake):
    """Below zero it is not a threshold, it is a licence to accept worse."""
    with pytest.raises(ValueError) as e:
        fake.gate([], min_gain=-0.01)
    assert "real_gate_min_gain" in str(e.value)


# ------------------------------------------------- the win rate under margin

def test_the_win_floor_vetoes_a_margin_bought_with_the_head_to_head_bit(fake):
    """`--real-gate-metric margin` ranks on coins alone, so a candidate can
    buy a bigger margin with the bit the leaderboard actually scores: the
    reading this file's own margin test accepts is 50%/0 -> 25%/+15k. The
    margin is the better-powered statistic and stays primary; the floor is a
    veto on top of it. At 0 the win rate may not drop at all."""
    gate = fake.gate([], metric="margin", win_floor=0.0)
    assert gate.win_floor == 0.0
    # Margin up but the win rate down: refused, however many coins.
    assert gate.beats(0.49, 90_000.0, 0.50, 10_000.0) is False
    assert gate.beats(0.25, 9e9, 0.50, 0.0) is False
    # Margin up and the win rate held: the margin decides, as before.
    assert gate.beats(0.50, 20_000.0, 0.50, 10_000.0) is True
    assert gate.beats(0.60, 20_000.0, 0.50, 10_000.0) is True
    # The floor can only veto; it never accepts a margin that did not improve.
    assert gate.beats(0.60, 10_000.0, 0.50, 10_000.0) is False
    assert gate.beats(0.60, 5_000.0, 0.50, 10_000.0) is False
    # And it never touches the baseline: there is no win rate to fall below.
    assert gate.beats(0.0, -9e9, None, None) is True

    # End to end, through a real (fake-scripted) eval: 50%/0 then 25%/+15k,
    # which the bare margin metric takes and the floor refuses.
    readings = [_step(2, 2, 10_000.0, 10_000.0),
                _step(1, 3, 90_000.0, 10_000.0)]
    floored = fake.gate(list(readings), games=2, metric="margin",
                        win_floor=0.0)
    floored.propose(np.zeros(3, np.float32), 1)
    assert _settle(floored)["accepted"] is True              # the baseline
    floored.propose(np.zeros(3, np.float32), 2)
    refused = _settle(floored)
    assert refused["accepted"] is False
    assert refused["win"] == 0.25 and refused["margin"] == 15_000.0
    assert (floored.win, floored.margin, floored.record_gen) == (0.5, 0.0, 1)


def test_the_win_floor_is_slack_and_not_a_ban_on_dropping(fake):
    """The gate reads 128-256 games, where the win rate's own sd is 3-4
    points, so a floor at 0 refuses candidates on noise. The slack is how much
    of a drop this segment will trade for coins: 0.03 is ~one sd."""
    gate = fake.gate([], metric="margin", win_floor=0.03)
    assert gate.beats(0.48, 20_000.0, 0.50, 10_000.0) is True     # -2pp: fine
    assert gate.beats(0.45, 20_000.0, 0.50, 10_000.0) is False    # -5pp: no
    assert gate.beats(0.45, 9e9, 0.50, 10_000.0) is False
    assert gate.beats(0.55, 20_000.0, 0.50, 10_000.0) is True
    # Still only a veto: -2pp with no coins gained is refused by the margin.
    assert gate.beats(0.48, 10_000.0, 0.50, 10_000.0) is False
    assert gate.beats(0.0, -9e9, None, None) is True

    # It composes with the threshold rather than replacing it: the margin gain
    # must clear `min_gain` AND the win rate must stay inside the slack.
    both = fake.gate([], metric="margin", win_floor=0.03, min_gain=500.0)
    assert both.beats(0.48, 10_600.0, 0.50, 10_000.0) is True
    assert both.beats(0.48, 10_400.0, 0.50, 10_000.0) is False    # gain small
    assert both.beats(0.45, 10_600.0, 0.50, 10_000.0) is False    # drop big


def test_without_the_floor_the_margin_metric_is_the_rule_it_was(fake):
    """The default is off, and off is not the same as 0.0 -- a floor at 0 is a
    real setting that refuses a single lost game. And the win metric, which
    ranks on the win rate already, has nothing to floor."""
    bare = fake.gate([], metric="margin")
    assert bare.win_floor is None
    assert bare.beats(0.25, 15_000.0, 0.50, 0.0) is True      # the old rule
    assert fake.gate([]).win_floor is None                    # metric="win"

    with pytest.raises(ValueError) as e:
        fake.gate([], metric="win", win_floor=0.03)
    assert "real_gate_win_floor" in str(e.value)
    with pytest.raises(ValueError) as e:
        fake.gate([], metric="margin", win_floor=-0.01)
    assert "real_gate_win_floor" in str(e.value)


def test_the_saved_win_floor_is_read_but_the_command_line_wins(fake):
    """Wired the way `min_gain` is: written into the state so a resume can say
    it changed, never restored, and `null` (a state written before the flag)
    is the floor switched off rather than a floor of zero."""
    gate = fake.gate([], metric="margin", win_floor=0.03)
    gate.save()
    with open(os.path.join(gate.run_dir, "real_gate.json")) as fh:
        state = json.load(fh)
    assert state["win_floor"] == 0.03
    assert RealGate.win_floor_of(state) == 0.03

    back = fake.gate([], metric="margin", win_floor=0.0)
    assert RealGate.win_floor_of(back.load(gate.run_dir)) == 0.03
    assert back.win_floor == 0.0                    # the ctor value wins

    off = fake.gate([], metric="margin")
    off.save()
    with open(os.path.join(off.run_dir, "real_gate.json")) as fh:
        assert json.load(fh)["win_floor"] is None
    # A state written before the flag existed, and the two spellings of off.
    assert RealGate.win_floor_of({}) is None
    assert RealGate.win_floor_of({"win_floor": None}) is None


def test_a_failed_eval_leaves_the_incumbent_standing(fake):
    """A crashed eval decides nothing. It must not be read as a 0% reading
    (which would be a refusal for the wrong reason) and must not be read as an
    improvement (which would hand the record to a process that never played a
    game)."""
    gate = fake.gate([_step(3, 1), {"rc": 7}, _step(4, 0)])
    gate.propose(np.zeros(3, np.float32), 1)
    _settle(gate)

    gate.propose(np.zeros(3, np.float32), 2)
    bad = _settle(gate)
    assert bad["accepted"] is False and bad["win"] is None
    assert "exited 7" in bad["error"] and gate.failures == 1
    assert (gate.win, gate.record_gen) == (0.75, 1)

    # And the next candidate is measured normally: one failure costs one
    # measurement, not the gate.
    gate.propose(np.zeros(3, np.float32), 3)
    assert _settle(gate)["accepted"] is True
    assert (gate.win, gate.record_gen) == (1.0, 3)


# ----------------------------------------------------------------- the queue

def test_only_the_newest_nomination_waits_for_the_slot(fake):
    """Queue depth 1. An eval is minutes and a record can land every
    `--abs-every` generations, so a FIFO would fall further behind the run
    forever -- and the candidate worth measuring is the newest one."""
    gate = fake.gate([_step(3, 1), _step(4, 0)])
    gate.propose(np.full(2, 1.0, np.float32), 1)
    running = gate.running
    assert running[1] == 1 and gate.pending is None

    gate.propose(np.full(2, 2.0, np.float32), 2)     # queued
    gate.propose(np.full(2, 3.0, np.float32), 3)     # replaces it
    assert gate.running is running                    # the eval is untouched
    assert gate.pending[1] == 3

    first = _settle(gate)
    assert first["gen"] == 1
    # The slot frees and the *latest* candidate goes straight in; gen 2 was
    # never played.
    assert gate.running[1] == 3 and gate.pending is None
    second = _settle(gate)
    assert second["gen"] == 3
    assert [c["theta"][0] for c in fake.calls()] == [1.0, 3.0]


# ---------------------------------------------------------------- the resume

def test_the_gate_state_round_trips_and_keeps_the_unmeasured_candidate(fake):
    """A resume has to bring the incumbent's numbers back, or the first
    candidate of the new segment is compared against nothing and walks in.
    The candidate whose eval the kill interrupted comes back too -- it was
    never measured, so it is still a nomination."""
    gate = fake.gate([_step(3, 1), {"hang": True}])
    gate.propose(np.full(4, 1.0, np.float32), 10)
    _settle(gate)
    gate.propose(np.full(4, 7.0, np.float32), 20)     # in flight, unmeasured
    gate.save()
    gate.close()

    back = fake.gate([], metric="win")
    state = back.load(gate.run_dir)
    assert state["record_gen"] == 10
    assert (back.win, back.margin, back.have_record) == (0.75, gate.margin, True)
    assert (back.accepts, back.rejects, back.evals) == (1, 0, 1)
    assert back.pending[1] == 20
    assert list(back.pending[0]) == [7.0] * 4
    assert RealGate.record_in(gate.run_dir) is True

    # A directory with no gate state is "no gate ran here", not "no record":
    # a checkpoint from a run trained without the flag carries an in-sim
    # record that the new run's baseline eval will measure.
    assert back.load(str(fake.root)) is None
    assert RealGate.record_in(str(fake.root)) is True
    assert RealGate.record_in(str(fake.root), default=False) is False


def test_the_saved_field_round_trips_and_a_legacy_string_still_reads(fake):
    """`real_gate.json` records the field as a list, because that is what the
    bar was measured against and a resume has to be able to tell whether it
    still is. Every gate state written before fields existed holds a bare
    string there, and those checkpoints have to keep resuming."""
    gate = fake.gate([], opponent="a/main.py,b/main.py")
    gate.save()
    with open(os.path.join(gate.run_dir, "real_gate.json")) as fh:
        state = json.load(fh)
    assert state["opponent"] == ["a/main.py", "b/main.py"]
    assert RealGate.field_of(state) == ("a/main.py", "b/main.py")

    # The pre-field spelling, which is still on every checkpoint taken before
    # this flag grew a comma.
    assert RealGate.field_of({"opponent": "../kaggriculture2/main.py"}) == (
        "../kaggriculture2/main.py",)
    assert RealGate.field_of({}) == ()


def test_the_saved_threshold_is_read_but_the_command_line_wins(fake):
    """`min_gain` is written so a resume can *say* the threshold changed, and
    it is not restored, because it is a threshold and not a measurement: the
    segment's own command line decides how big an improvement it wants, the
    way `--real-gate-games` does. A state written before the flag existed
    carries no key, which is the strict rule those runs were gated by."""
    gate = fake.gate([], min_gain=0.03)
    gate.save()
    with open(os.path.join(gate.run_dir, "real_gate.json")) as fh:
        state = json.load(fh)
    assert state["min_gain"] == 0.03
    assert RealGate.min_gain_of(state) == 0.03

    # The ctor value wins over the file: loosened...
    back = fake.gate([], min_gain=0.0)
    assert RealGate.min_gain_of(back.load(gate.run_dir)) == 0.03
    assert back.min_gain == 0.0
    # ...and tightened, from a legacy state that has never heard of the key.
    del state["min_gain"]
    with open(os.path.join(gate.run_dir, "real_gate.json"), "w") as fh:
        json.dump(state, fh)
    tighter = fake.gate([], min_gain=0.05)
    assert RealGate.min_gain_of(tighter.load(gate.run_dir)) == 0.0
    assert tighter.min_gain == 0.05
    assert RealGate.min_gain_of({}) == 0.0
    assert RealGate.min_gain_of({"min_gain": None}) == 0.0


def test_a_resume_re_nominates_the_candidate_it_inherited(fake):
    """The restored nomination is a nomination: the next poll launches it."""
    gate = fake.gate([_step(4, 0)])
    gate.propose(np.full(2, 5.0, np.float32), 30)
    gate.close()                                      # never measured
    gate.save()

    back = fake.gate([_step(4, 0)])
    back.load(gate.run_dir)
    assert back.proc is None
    assert back.poll() is None                        # the launch, not a verdict
    assert back.running[1] == 30
    res = _settle(back)
    assert res["gen"] == 30 and res["accepted"] is True


# --------------------------------------------------------------- the cleanup

def test_close_kills_the_eval_and_its_worker_pool(fake):
    """A killed trainer must not leave `--real-gate-workers` engine processes
    on the host. The child is its own session leader, so one `killpg` takes
    the pool with it -- which is what the grandchild here stands in for."""
    gate = fake.gate([{"hang": True}])
    gate.propose(np.zeros(3, np.float32), 1)
    pid = gate.proc.pid
    assert os.getpgid(pid) == pid, "the eval must be its own process group"

    kid_file = os.path.join(gate.run_dir, "fake_kid.pid")
    for _ in range(500):                      # bounded: the child is starting
        if os.path.isfile(kid_file):
            break
        time.sleep(0.01)
    with open(kid_file) as fh:
        kid = int(fh.read())

    gate.close()
    assert gate.proc is None
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)                       # reaped by `close`'s own wait
    for _ in range(500):
        try:
            os.kill(kid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.01)
    else:
        os.kill(kid, signal.SIGKILL)
        pytest.fail("the eval's worker outlived the gate's close()")

    # The interrupted candidate is not lost; it goes back to the queue.
    assert gate.pending is not None and gate.pending[1] == 1
    gate.close()                              # idempotent


# ------------------------------------------------------ the trainer's record

def _stub_trainer(gate=None, t=1000, last_improve=0):
    tr = Trainer.__new__(Trainer)
    tr.t, tr.last_improve = t, last_improve
    tr.theta = np.zeros(3, np.float32)
    tr.best_abs_theta = np.zeros(3, np.float32)
    tr.best_sim_theta = np.zeros(3, np.float32)
    tr.real_gate = gate
    tr.last_real_gate = None
    return tr


class _Canned:
    """A gate whose verdicts this file dictates."""

    def __init__(self, results, have_record=True):
        self.results, self.have_record = list(results), have_record
        self.proposed = []

    def poll(self):
        return self.results.pop(0) if self.results else None

    def propose(self, theta, gen, source="record"):
        self.proposed.append((np.asarray(theta), gen, source))


def _verdict(accepted, theta=(1.0, 2.0, 3.0)):
    return {"gen": 500, "accepted": accepted, "win": 0.6, "margin": 5.0,
            "games": 48, "baseline": False, "incumbent_win": 0.5,
            "incumbent_margin": 1.0, "rc": 0,
            "theta": np.asarray(theta, np.float32)}


def test_the_record_moves_only_when_the_real_engine_says_so():
    """`best_abs_theta` is what `best_abs.npy`, `--promote`, `--from-best` and
    the stall restart all read. Under the gate it changes here and nowhere
    else."""
    tr = _stub_trainer(_Canned([_verdict(True)]))
    assert tr._poll_real_gate()["accepted"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [1.0, 2.0, 3.0]
    assert tr.last_improve == tr.t

    tr = _stub_trainer(_Canned([_verdict(False)]), last_improve=7)
    tr._poll_real_gate()
    assert list(np.asarray(tr.best_abs_theta)) == [0.0, 0.0, 0.0]
    assert tr.last_improve == 7          # a refusal is not an improvement

    tr = _stub_trainer(_Canned([]))
    assert tr._poll_real_gate() is None  # the usual generation: nothing landed


def test_the_stall_restart_waits_for_a_real_record():
    """The ungated rule would send a run with no gated record yet back to the
    untrained init, because that is what `best_abs_theta` still holds."""
    calls = []
    tr = _stub_trainer(_Canned([], have_record=False))
    tr._maybe_restart = lambda: calls.append("restart")
    tr._gate_restart_check()
    assert calls == []

    tr.real_gate.have_record = True
    tr._gate_restart_check()
    assert calls == ["restart"]

    # A generation whose verdict just took the record has improved, however
    # long the in-sim number has been flat.
    tr.last_real_gate = _verdict(True)
    tr._gate_restart_check()
    assert calls == ["restart"]
    tr.last_real_gate = _verdict(False)
    tr._gate_restart_check()
    assert calls == ["restart", "restart"]


# ---------------------------------------------------------- the replicate

def test_an_acceptance_is_re_measured_before_anything_is_judged_against_it(
        fake):
    """`--real-gate-replicate`. The record is a max over noisy n=48 draws, so
    the incumbent's number is the luckiest one the run happened to take:
    flow28b accepted a candidate at 85.4% and the same theta replicated at
    74.5% on 192 games. The re-measurement jumps the queue -- it *is* the bar,
    and a candidate judged against an un-replicated number is judged against
    noise -- and the bar becomes the pooled reading."""
    gate = fake.gate([_step(3, 1), _step(1, 3), _step(3, 1)], replicate=True)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    first = _settle(gate)
    # Provisional: the reading is the working bar, but the record is not the
    # record until its replicate lands (`_settle_replicate`).
    assert first["accepted"] is False and first["provisional"] is True
    assert (gate.win, gate.margin) == (0.75, 5_000.0)

    # Queued immediately, on the accepted theta and a disjoint seed block.
    assert gate.running[1] == 10 and gate.running[2] == "replicate"
    gate.propose(np.full(3, 2.0, np.float32), 11)      # waits behind it
    assert gate.pending[1] == 11 and gate.running[2] == "replicate"

    rep = _settle(gate)
    call = fake.calls()[1]
    assert call["argv"][call["argv"].index("--seed-base") + 1] == "20260826"
    assert call["theta"] == [1.0, 1.0, 1.0]
    # The reading is the replicate's own; the pooled pair is the new bar.
    # There was no incumbent to fail against, so this one confirms.
    assert rep["source"] == "replicate" and rep["accepted"] is True
    assert (rep["win"], rep["margin"]) == (0.25, pytest.approx(-5_000.0))
    assert rep["replicate_win"] == 0.5
    assert rep["replicate_margin"] == pytest.approx(0.0)
    assert (gate.win, gate.margin) == (0.5, pytest.approx(0.0))
    assert (gate.n, gate.record_gen) == (8, 10)        # two evals of 4 games

    # And the next candidate is judged against the pooled bar: 75%/+5,000 only
    # *ties* the reading that took the record, and would have been refused.
    assert gate.running[1] == 11
    second = _settle(gate)
    assert second["provisional"] is True and gate.record_gen == 11
    assert gate.running[2] == "replicate"             # which owes one too
    gate.close()


def test_the_owed_replicate_survives_the_resume_that_killed_it(fake):
    """A resume must not leave the bar sitting on the single lucky reading it
    was accepted at -- that is the state the flag exists to avoid, and it
    would persist for the rest of the run."""
    gate = fake.gate([_step(3, 1), {"hang": True}], replicate=True)
    gate.propose(np.full(4, 6.0, np.float32), 10)
    _settle(gate)
    assert gate.running[2] == "replicate"             # in flight, unmeasured
    gate.save()
    gate.close()

    with open(os.path.join(gate.run_dir, "real_gate.json")) as fh:
        saved = json.load(fh)
    assert saved["replicate_due"] is True and saved["n"] == 4
    assert saved["win"] == 0.75

    back = fake.gate([_step(1, 3)], replicate=True)
    state = back.load(gate.run_dir)
    assert state["replicate_due"] is True
    assert back.replicate_due[1] == 10                # `record_gen`'s theta
    assert list(back.replicate_due[0]) == [6.0] * 4
    assert (back.win, back.n) == (0.75, 4)

    # It is re-queued, not merely remembered: the next poll launches it, and
    # the bar it lands on is the pooled one.
    assert back.poll() is None
    assert back.running[1] == 10 and back.running[2] == "replicate"
    res = _settle(back)
    assert res["replicate_win"] == 0.5 and back.n == 8


def test_the_reset_drops_the_bar_and_re_measures_the_theta_it_kept(
        tmp_path, monkeypatch):
    """`--real-gate-reset`. A saved bar can stop being comparable -- a
    repackaged opponent, a changed `--real-gate-games`, or simply a reading
    lucky enough that nothing has passed it since. Dropping it keeps the
    theta and re-nominates it, so the next verdict is a fresh baseline rather
    than a comparison against a number nobody can reproduce."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "main.py"
    opp.write_text("# a packaged agent\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.854, "margin": 6_023.0, "n": 48, "record_gen": 900,
                   "have_record": True, "pending_gen": None}, fh)

    tr = _stub_trainer(t=1500)
    tr.best_abs = 5_000.0
    tr.best_abs_theta = np.full(3, 9.0, np.float32)
    gate = T.setup_real_gate(_Args(opponent=str(opp), reset=True), tr,
                             str(tmp_path), resume_dir=str(resume))
    assert (gate.win, gate.margin, gate.record_gen) == (None, None, None)
    assert gate.have_record is False and gate.n == 0
    # The theta is kept and nominated, exactly as an inherited un-measured
    # record is: the first reading of the new segment is the baseline.
    assert gate.pending[1] == 1500
    assert list(gate.pending[0]) == [9.0, 9.0, 9.0]
    assert list(np.asarray(tr.best_abs_theta)) == [9.0, 9.0, 9.0]

    # Without the flag the saved bar stands (and `--real-gate-reset` without
    # the gate is refused at startup rather than silently ignored).
    tr2 = _stub_trainer(t=1500)
    tr2.best_abs = 5_000.0
    kept = T.setup_real_gate(_Args(opponent=str(opp)), tr2, str(tmp_path),
                             resume_dir=str(resume))
    assert (kept.win, kept.n) == (0.854, 48)
    args = _Args(reset=True)
    args.real_gate = False
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(args, _stub_trainer(), str(tmp_path))
    assert "--real-gate-reset" in str(e.value)


def test_a_cold_start_measures_the_theta_it_was_handed(fake, monkeypatch):
    """flow29 was started from a champion that pools 84.4% on the gate's two
    seed bases, and the gate never measured it: the first candidate was gen
    10's in-sim record -- ten ES steps downhill, 70.8% pooled -- which became
    the bar, and `--real-gate-recentre` then pulled the search back onto that
    instead of onto the champion. A theta the run was handed is a candidate
    like any other, and it is the one candidate that exists before the search
    has had a chance to leave it."""
    class _Fed(RealGate):
        def __init__(self, run_dir, opponent, **kw):
            super().__init__(run_dir, opponent, script=fake.script,
                             python=sys.executable, cwd=str(fake.root), **kw)

    monkeypatch.setattr(T, "RealGate", _Fed)
    opp = os.path.join(str(fake.root), "main.py")
    with open(opp, "w") as fh:
        fh.write("# a packaged agent\n")
    fake.plan([_step(3, 1), _step(3, 1), _step(1, 3)])

    tr = _stub_trainer(t=0)
    tr.best_abs = NO_BEST                     # nothing measured in-sim yet
    tr.theta = np.full(3, 4.0, np.float32)    # the champion the run was given
    tr.best_abs_theta = tr.theta
    gate = T.setup_real_gate(_Args(opponent=opp, games=2, workers=1,
                                   replicate=True,
                                   init_theta="champion.npy"),
                             tr, fake.run)
    assert gate.running[1] == 0 and gate.running[2] == "record"

    # The first in-sim record arrives ten generations later and waits its
    # turn rather than replacing the measurement in flight.
    gate.propose(np.full(3, 9.0, np.float32), 10)
    assert gate.pending[1] == 10 and gate.running[1] == 0

    assert _through(tr)["provisional"] is True
    assert list(fake.calls()[0]["theta"]) == [4.0, 4.0, 4.0]
    assert gate.running[2] == "replicate" and gate.pending[1] == 10
    assert _through(tr)["accepted"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [4.0, 4.0, 4.0]
    assert (gate.win, gate.n, gate.record_gen) == (0.75, 8, 0)

    # Only now is the in-sim candidate measured, and it is measured against
    # the champion's pooled number.
    assert gate.running[1] == 10
    assert _settle(gate)["accepted"] is False
    assert list(np.asarray(tr.best_abs_theta)) == [4.0, 4.0, 4.0]


def test_a_resumed_bar_finds_its_theta_in_the_record_file(fake, monkeypatch):
    """flow27h resumed flow27g with `--real-gate-fresh` and ran unpaired: the
    resume retired the in-sim record, which cleared the only thing the gate
    had to identify its incumbent with, so the second leg had no theta to
    play and every verdict fell back to the pooled comparison the flag exists
    to replace. The gate is the only writer of `best_abs.npy` under
    `--real-gate`, so that file *is* the bar's theta -- across the retirement
    too, which moves `best_abs_theta` and not the file."""
    class _Fed(RealGate):
        def __init__(self, run_dir, opponent, **kw):
            super().__init__(run_dir, opponent, script=fake.script,
                             python=sys.executable, cwd=str(fake.root), **kw)

    monkeypatch.setattr(T, "RealGate", _Fed)
    opp = os.path.join(str(fake.root), "main.py")
    with open(opp, "w") as fh:
        fh.write("# a packaged agent\n")
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": 0.75, "margin": 5_000.0, "n": 8, "record_gen": 1030,
                   "have_record": True, "pending_gen": None,
                   "replicate_due": False, "prev_incumbent": None,
                   "base_seq": 4}, fh)
    np.save(os.path.join(fake.run, "best_abs.npy"),
            np.full(3, 6.0, np.float32))

    tr = _stub_trainer(t=4000)
    tr.best_abs = NO_BEST                     # the in-sim record was retired
    tr.best_abs_theta = np.full(3, 9.0, np.float32)      # ...so this is live
    gate = T.setup_real_gate(_Args(opponent=opp, games=2, workers=1,
                                   replicate=True, fresh=True),
                             tr, fake.run, resume_dir=fake.run)
    assert gate.theta_source == "best_abs.npy"
    theta = np.asarray(gate.record_theta)
    assert list(theta[:3]) == [6.0, 6.0, 6.0] and not theta[3:].any()
    assert gate.base_seq == 4                 # and the base sequence carries

    # So the round is a pair: the candidate, then the bar on the same games.
    fake.plan([_step(1, 3), _step(3, 1)])
    gate.propose(np.full(3, 2.0, np.float32), 4040)
    res = _round(gate)
    calls = fake.calls()
    assert len(calls) == 2
    assert calls[0]["theta"][:3] == [2.0, 2.0, 2.0]
    assert calls[1]["theta"][:3] == [6.0, 6.0, 6.0]
    b = _bases(fake)
    assert b[0] == b[1] == res["base"]
    assert (res["paired_win"], res["paired_margin"]) == (0.75, 5_000.0)
    assert res["accepted"] is False


def test_a_recovered_record_theta_re_arms_the_recentre(fake, monkeypatch):
    """flow30c, live: resumed with a gate bar of 80.7% from gen 80 and
    `--real-gate-recentre 3`, refused its own centre 6 times running, and
    never recentred once.

    The retirement above clears `have_record` because the pair (numbers,
    theta) is broken -- and then `best_abs.npy` puts the theta back, which
    makes the pair whole again. Leaving the flag down after that is the bug:
    `have_record` is what arms `recentre_due` and the gated stall restart, so
    the run that most needs to go back to its record is precisely the one
    that cannot. And the jump itself reads `best_abs_theta`, which the
    retirement left on the live centre, so the flag alone would recentre the
    search onto the place it is trying to leave."""
    class _Fed(RealGate):
        def __init__(self, run_dir, opponent, **kw):
            super().__init__(run_dir, opponent, script=fake.script,
                             python=sys.executable, cwd=str(fake.root), **kw)

    monkeypatch.setattr(T, "RealGate", _Fed)
    opp = os.path.join(str(fake.root), "main.py")
    with open(opp, "w") as fh:
        fh.write("# a packaged agent\n")
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": 0.807, "margin": 7_648.0, "n": 96, "record_gen": 80,
                   "have_record": True, "pending_gen": None,
                   "replicate_due": False, "prev_incumbent": None}, fh)
    np.save(os.path.join(fake.run, "best_abs.npy"),
            np.full(3, 6.0, np.float32))

    tr = _stub_trainer(t=4000)
    tr.best_abs = NO_BEST                     # the in-sim record was retired
    tr.theta = np.full(3, 9.0, np.float32)               # the drifted centre
    tr.best_abs_theta = tr.theta                         # ...which is all it left
    gate = T.setup_real_gate(_Args(opponent=opp, games=2, workers=1,
                                   every=20, recentre=1), tr, fake.run,
                             resume_dir=fake.run)

    # Both halves are back: the file's theta *is* the theta the bar was
    # measured on, so the gate has a record again and the trainer holds it.
    assert gate.have_record is True and gate.theta_source == "best_abs.npy"
    best = np.asarray(tr.best_abs_theta)
    assert list(best[:3]) == [6.0, 6.0, 6.0] and not best[3:].any()
    assert list(best) == list(np.asarray(gate.record_theta))
    assert (gate.win, gate.record_gen) == (0.807, 80)
    assert gate.recentre_due() is False        # nothing refused yet

    # One periodic refusal is the whole budget at `--real-gate-recentre 1`.
    fake.plan([_step(1, 3)])
    gate.propose(np.full(3, 3.0, np.float32), 4040, source="periodic")
    res = _settle(gate)
    assert res["accepted"] is False and gate.periodic_rejects == 1
    assert gate.recentre_due() is True

    # And the jump lands on the record, not on the centre it refused.
    tr.cfg = SimpleNamespace(stall_sigma_mult=1.0)
    tr.n = int(best.size)
    tr.sigma, tr.sigma_restarts, tr.sigma_steps = 0.02, 0, 0
    tr._recentre_on_record()
    landed = np.asarray(tr.theta)
    assert list(landed[:3]) == [6.0, 6.0, 6.0] and not landed[3:].any()
    assert tr.last_recentre == {"record_gen": 80, "count": 1}
    assert gate.periodic_rejects == 0 and tr.adam_t == 0


def test_a_record_theta_recovered_one_segment_later_still_re_arms(fake,
                                                                  monkeypatch):
    """flow30d, live: resumed flow30c, whose real_gate.json already carried
    `have_record: false` from the retirement one segment earlier. The theta
    was found in best_abs.npy just the same, but a guard keyed on *this*
    setup having retired the record left the flag down, and the run sat
    through 8 refusals of its centre without recentring."""
    class _Fed(RealGate):
        def __init__(self, run_dir, opponent, **kw):
            super().__init__(run_dir, opponent, script=fake.script,
                             python=sys.executable, cwd=str(fake.root), **kw)

    monkeypatch.setattr(T, "RealGate", _Fed)
    opp = os.path.join(str(fake.root), "main.py")
    with open(opp, "w") as fh:
        fh.write("# a packaged agent\n")
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": 0.807, "margin": 8_416.0, "n": 96, "record_gen": 80,
                   "have_record": False, "periodic_rejects": 8,
                   "pending_gen": None, "replicate_due": False,
                   "prev_incumbent": None}, fh)
    np.save(os.path.join(fake.run, "best_abs.npy"),
            np.full(3, 6.0, np.float32))

    tr = _stub_trainer(t=2500)
    tr.best_abs = NO_BEST
    tr.theta = np.full(3, 9.0, np.float32)
    tr.best_abs_theta = tr.theta
    gate = T.setup_real_gate(_Args(opponent=opp, games=2, workers=1,
                                   every=20, recentre=3), tr, fake.run,
                             resume_dir=fake.run)
    assert gate.have_record is True and gate.theta_source == "best_abs.npy"
    best = np.asarray(tr.best_abs_theta)
    assert list(best[:3]) == [6.0, 6.0, 6.0]
    assert list(best) == list(np.asarray(gate.record_theta))
    # Eight refusals against a budget of three: the recentre is due at once.
    assert gate.periodic_rejects == 8 and gate.recentre_due() is True


def test_a_bar_without_a_theta_is_still_a_bar(fake, monkeypatch):
    """flow28e, live: resumed with a gate bar of 80.2%/+7,648 (n=96), took a
    candidate at 85.4% provisionally, replicated it at 52.1% and *confirmed*
    the pooled 68.8% -- 11pp below the bar it was measured against, and
    `best_abs.npy` moved to it.

    The stash that a revert needs was guarded by `have_record` and a known
    `record_theta`, which are statements about `best_abs.npy`; the resume
    took both away (a retired in-sim record clears `have_record` while the
    gate's real-engine numbers stand) and left the bar undefended. The bar is
    the numbers. A pooled candidate below them reverts whether or not anyone
    knows which theta earned them.
    """
    class _Fed(RealGate):
        """The real gate, wired to this file's fake evaluator."""

        def __init__(self, run_dir, opponent, **kw):
            super().__init__(run_dir, opponent, script=fake.script,
                             python=sys.executable, cwd=str(fake.root), **kw)

    monkeypatch.setattr(T, "RealGate", _Fed)
    opp = os.path.join(str(fake.root), "main.py")
    with open(opp, "w") as fh:
        fh.write("# a packaged agent\n")
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": 0.75, "margin": 5_000.0, "n": 8, "record_gen": 1030,
                   "have_record": True, "pending_gen": None,
                   "replicate_due": False, "prev_incumbent": None}, fh)

    tr = _stub_trainer(t=1500)
    tr.best_abs = NO_BEST                    # the in-sim record was retired...
    tr.best_abs_theta = np.full(3, 9.0, np.float32)      # ...so this is live
    gate = T.setup_real_gate(_Args(opponent=opp, games=2, workers=1,
                                   replicate=True),
                             tr, fake.run, resume_dir=fake.run)
    # The state flow28e was actually in: numbers, no record, no theta for it.
    assert gate.have_record is False and gate.record_theta is None
    assert (gate.win, gate.margin) == (0.75, 5_000.0)
    assert (gate.n, gate.record_gen) == (8, 1030)

    fake.plan([_step(4, 0), _step(0, 4)])     # 100% on one draw, then 0%
    gate.propose(np.full(3, 2.0, np.float32), 2020)
    assert _settle(gate)["provisional"] is True
    assert gate.prev_incumbent is not None    # the bug: nothing was stashed
    assert gate.prev_incumbent["theta"] is None

    # A theta-less incumbent round-trips: the numbers are what a resume
    # landing mid-replicate has to be able to revert to.
    gate.save()
    back = RealGate(fake.run, opp, games=2, replicate=True,
                    script=fake.script, python=sys.executable,
                    cwd=str(fake.root))
    back.load(fake.run)
    assert back.prev_incumbent["record_gen"] == 1030
    assert back.prev_incumbent["theta"] is None
    assert not os.path.isfile(back.prev_path)

    rev = _settle(gate)
    assert rev["reverted"] is True and rev["accepted"] is False
    assert rev["replicate_win"] == 0.5        # pooled, and below the bar
    assert (rev["restored_win"], rev["restored_gen"]) == (0.75, 1030)
    # Nothing to put back: a provisional record never moved `best_abs_theta`,
    # and `_poll_real_gate` skips a `None` restore.
    assert rev["restore_theta"] is None
    assert (gate.win, gate.margin) == (0.75, 5_000.0)
    assert (gate.n, gate.record_gen) == (8, 1030)
    assert gate.have_record is False and gate.reverts == 1


# --------------------------------------------------------- the fresh pairing

def _bases(fake):
    """The seed base every eval so far was run on."""
    return [int(c["argv"][c["argv"].index("--seed-base") + 1])
            for c in fake.calls()]


def _round(gate):
    """Settle legs until the round produces a verdict.

    A `--real-gate-fresh` round is two evals -- the candidate, then the
    incumbent on the same base -- and only the second one decides.
    """
    for _ in range(4):
        res = _settle(gate)
        if res is not None:
            return res
    raise AssertionError("the round never produced a verdict")


def test_the_pair_is_played_on_the_same_fresh_seeds(fake):
    """Two fixed bases are two things to overfit: flow27g's confirmed record
    pooled 83.3% on the gate's own bases and 62.5% on another (n=192), while
    the champion is 76-85% everywhere. So every nomination draws a fresh base
    and the incumbent is replayed on it -- and the decision is that pair, not
    the incumbent's pooled report."""
    gate = fake.gate([_step(3, 1), _step(3, 1),          # the incumbent, twice
                      _step(4, 0),                        # a candidate: 100%
                      _step(4, 0, 20_000.0)],             # ...and so is the bar
                     replicate=True, fresh=True, fresh_seed=7)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    assert _round(gate)["provisional"] is True            # nothing to pair with
    assert _round(gate)["confirmed"] is True
    assert (gate.win, gate.n) == (0.75, 8)

    gate.propose(np.full(3, 2.0, np.float32), 20, source="periodic")
    res = _round(gate)
    b = _bases(fake)
    assert len(set(b[:3])) == 3                           # a fresh base each
    assert b[3] == b[2]                                   # the pair, together
    calls = fake.calls()
    assert calls[2]["theta"] == [2.0, 2.0, 2.0]           # candidate first
    assert calls[3]["theta"] == [1.0, 1.0, 1.0]           # then the incumbent

    # 100%/+10,000 beats the incumbent's *pooled* 75%/+5,000 and would have
    # taken the record on the old rule. On the same games the incumbent also
    # went 100%, by a wider margin, so it does not.
    assert res["base"] == b[2] and res["win"] == 1.0
    assert (res["paired_win"], res["paired_margin"]) == (1.0, 20_000.0)
    assert res["accepted"] is False and res.get("provisional") is None
    assert gate.periodic_rejects == 1
    # The incumbent's report grows with every base it is played on; the
    # decision above did not use it.
    assert res["incumbent_win"] == pytest.approx((0.75 * 8 + 1.0 * 4) / 12)
    assert gate.n == 12


def test_a_base_the_incumbent_has_already_played_costs_no_second_eval(fake):
    """The pairing doubles the gate's cost, so a reading it already has is a
    leg it must not spend -- and the cache is what a resume carries, together
    with the counter that makes the base sequence continue rather than
    replay."""
    gate = fake.gate([_step(3, 1), _step(3, 1), _step(1, 3)],
                     replicate=True, fresh=True, fresh_seed=11)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    _round(gate)
    _round(gate)
    first, second = _bases(fake)
    assert sorted(gate.base_results) == sorted([str(first), str(second)])

    # Rewind the counter so the next draw is a base the incumbent has already
    # been played on: one eval for the round, not two.
    gate.base_seq -= 2
    gate.propose(np.zeros(3, np.float32), 20)
    res = _round(gate)
    assert _bases(fake) == [first, second, first]
    assert res["base"] == first and res["accepted"] is False
    assert (res["paired_win"], res["paired_margin"]) == (0.75, 5_000.0)

    # The counter and the cache both survive the resume, so the next base is
    # one the run has not selected on.
    gate.save()
    back = RealGate(gate.run_dir, "opp/main.py", games=2, replicate=True,
                    fresh=True, fresh_seed=11, script=fake.script,
                    python=sys.executable, cwd=str(fake.root))
    state = back.load(gate.run_dir)
    assert state["base_seq"] == gate.base_seq
    assert back.base_results == gate.base_results
    # It continues the sequence from the saved counter; a gate that forgot it
    # would restart at the first base and hand the run games it has already
    # selected on.
    assert back._next_base() == second != first


def test_the_confirmation_is_the_pair_pooled_over_both_fresh_bases(fake):
    """The replicate is paired too, and confirmation is the pooled comparison
    of the two thetas over the two bases. A candidate that won its first pair
    on one lucky base and lost the second does not keep the record."""
    gate = fake.gate([_step(3, 1), _step(3, 1),        # the incumbent, twice
                      _step(4, 0), _step(2, 2),        # round 1: 100% vs 50%
                      _step(0, 4), _step(4, 0)],       # round 2: 0% vs 100%
                     replicate=True, fresh=True, fresh_seed=3)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    _round(gate)
    _round(gate)
    assert (gate.win, gate.n, gate.record_gen) == (0.75, 8, 10)

    gate.propose(np.full(3, 5.0, np.float32), 30)
    prov = _round(gate)
    assert prov["provisional"] is True and prov["paired_win"] == 0.5
    assert gate.prev_incumbent["record_gen"] == 10

    rev = _round(gate)
    b = _bases(fake)
    assert b[4] == b[5] and b[4] not in b[:4]          # a second fresh pair
    assert fake.calls()[5]["theta"] == [1.0, 1.0, 1.0]  # the bar, replayed
    # Pooled over both bases: the candidate 50%, the incumbent 75%.
    assert rev["replicate_win"] == 0.5
    assert rev["reverted"] is True and rev["accepted"] is False
    assert (gate.win, gate.record_gen) == (0.75, 10)
    assert list(gate.record_theta) == [1.0, 1.0, 1.0]
    assert gate.reverts == 1


def _saved_bar(fake, win=0.20, margin=-2_000.0, record=True, theta=6.0):
    """A gate state on disk: a confirmed bar, optionally with its theta in
    `best_abs.npy` beside it -- which is what a resumed run finds."""
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": win, "margin": margin, "n": 8, "record_gen": 40,
                   "have_record": True, "pending_gen": None,
                   "replicate_due": False, "prev_incumbent": None,
                   "base_seq": 2}, fh)
    if record:
        np.save(os.path.join(fake.run, "best_abs.npy"),
                np.full(3, theta, np.float32))


def _reloaded(fake, fit=None, **kw):
    """A second gate over the same run directory, restored from its state."""
    kw.setdefault("games", 2)
    kw.setdefault("workers", 1)
    back = RealGate(fake.run, "opp/main.py", script=fake.script,
                    python=sys.executable, cwd=str(fake.root), **kw)
    back.load(fake.run, fit=fit)
    return back


def test_the_record_s_own_theta_comes_back_with_the_gate_state(fake):
    """`load` restored the *displaced* incumbent's theta and never the
    record's, so a resumed gate held a bar with nothing to play for it. The
    gate is the only writer of `best_abs.npy`, so the file beside the state is
    that theta -- read through the caller's layout adapter, like every other
    theta a checkpoint carries."""
    _saved_bar(fake)
    back = _reloaded(fake, replicate=True, fresh=True, fresh_seed=7,
                     fit=lambda a: np.concatenate([a, np.zeros(2, np.float32)]))
    theta = np.asarray(back.record_theta)
    assert list(theta[:3]) == [6.0, 6.0, 6.0] and not theta[3:].any()
    assert back.theta_source == "best_abs.npy"
    assert back.have_record is True and back.win == 0.20


def test_a_bar_whose_record_file_is_gone_loads_without_a_theta(fake):
    """The numbers are still a bar (`test_a_bar_without_a_theta_is_still_a_bar`
    is the rest of that story); what must not happen is a theta invented for
    them, so a missing file leaves the field as it was."""
    _saved_bar(fake, record=False)
    back = _reloaded(fake, replicate=True, fresh=True, fresh_seed=7)
    assert back.record_theta is None and back.theta_source == "unknown"
    assert back.have_record is True and back.win == 0.20


def test_a_resumed_fresh_round_still_plays_the_incumbent_s_leg(fake):
    """The bug, end to end: with no `record_theta` the round is the
    candidate's leg alone and the verdict falls out of a comparison against
    the incumbent's pooled level from bases the candidate never played. Here
    that fallback would *accept* (50% against a pooled 20%) and the pairing
    refuses (50% against the incumbent's 75% on the very same games), which is
    the whole difference `--real-gate-fresh` exists to make."""
    _saved_bar(fake)
    back = _reloaded(fake, replicate=True, fresh=True, fresh_seed=7)
    fake.plan([_step(2, 2), _step(3, 1)])     # the candidate, then the bar
    back.propose(np.full(3, 2.0, np.float32), 60)

    assert _settle(back) is None              # one leg decides nothing
    res = _round(back)
    calls = fake.calls()
    assert len(calls) == 2
    assert calls[0]["theta"] == [2.0, 2.0, 2.0]
    assert calls[1]["theta"] == [6.0, 6.0, 6.0]      # the record file's theta
    b = _bases(fake)
    assert b[0] == b[1] == res["base"]        # the same games, both legs

    assert (res["paired_win"], res["paired_margin"]) == (0.75, 5_000.0)
    assert res["win"] == 0.5
    assert res["accepted"] is False and res.get("provisional") is None
    assert back.record_theta is not None and back.record_gen == 40


def test_a_provisional_record_keeps_its_theta_across_the_resume(fake):
    """The live flow61/flow62 state: a resume *between* a provisional
    acceptance and its replicate. `best_abs.npy` has not moved (that is what
    "provisional" means) and `have_record` is False, so the record file cannot
    supply the theta -- but the owed replicate's theta *is* the record theta
    at that moment, which is where `_decide_round` left it. `_confirm` only
    flips the flag, so a gate that came back without it confirmed a bar it
    could not play, and every later candidate was decided against the pooled
    level instead of against the bar on its own games."""
    with open(os.path.join(fake.run, "real_gate.json"), "w") as fh:
        json.dump({"win": 0.5, "margin": 1_000.0, "n": 4, "record_gen": 70,
                   "have_record": False, "pending_gen": None,
                   "replicate_due": True, "replicate_source": "record",
                   "prev_incumbent": None, "base_seq": 2,
                   "base_results": {"111": [0.5, 1_000.0, 4]}}, fh)
    np.save(os.path.join(fake.run, "real_gate_replicate.npy"),
            np.full(3, 8.0, np.float32))
    back = _reloaded(fake, replicate=True, fresh=True, fresh_seed=5)
    assert not os.path.isfile(os.path.join(fake.run, "best_abs.npy"))
    assert list(np.asarray(back.record_theta)) == [8.0, 8.0, 8.0]
    assert back.theta_source == "real_gate_replicate.npy"
    assert back.have_record is False          # the confirmation is still owed
    assert list(np.asarray(back.replicate_due[0])) == [8.0, 8.0, 8.0]

    # The owed replicate lands first and confirms the provisional record.
    fake.plan([_step(3, 1), _step(1, 3), _step(3, 1)])
    assert back.poll() is None                # the slot is taken by it
    res = _round(back)
    assert res["confirmed"] is True and back.have_record is True
    assert list(np.asarray(back.record_theta)) == [8.0, 8.0, 8.0]

    # ...so the next candidate is a pair, and the second leg is that theta.
    back.propose(np.full(3, 2.0, np.float32), 90)
    res = _round(back)
    calls = fake.calls()
    assert calls[-2]["theta"] == [2.0, 2.0, 2.0]
    assert calls[-1]["theta"] == [8.0, 8.0, 8.0]
    b = _bases(fake)
    assert b[-1] == b[-2] == res["base"]
    assert (res["paired_win"], res["paired_margin"]) == (0.75, 5_000.0)
    assert res["accepted"] is False and res.get("provisional") is None


# ----------------------------------------------------------- the re-centre

def _restartable(gate, t=500):
    """A stub with the fields a restart moves: theta, Adam, sigma, the clock."""
    import jax.numpy as jnp

    tr = _stub_trainer(gate, t=t, last_improve=t - 400)
    tr.n = 3
    tr.cfg = Config(stall_sigma_mult=2.0, restart_stall=1_000)
    tr.theta = jnp.full(3, 7.0)
    tr.best_abs_theta = jnp.full(3, 3.0)
    tr.m, tr.v, tr.adam_t = jnp.full(3, 0.5), jnp.full(3, 0.25), 40
    tr.sigma, tr.sigma_restarts, tr.sigma_steps = 0.02, 0, 0
    return tr


def test_a_run_of_refused_centres_puts_the_search_back_on_the_record(fake):
    """The gate filters but does not steer: on flow27c/28c/27d every periodic
    candidate after the record scored below the bar, because the gradient that
    moves the centre is in-sim and the bar is not. `--real-gate-recentre K`
    answers a run of refusals with the move `_maybe_restart` already makes for
    the in-sim version of the same problem -- the *same* move, through the
    shared helper, or a resume would rebuild sigma from a restart that never
    ran."""
    gate = fake.gate([_step(3, 1), _step(1, 3), _step(1, 3), _step(1, 3)],
                     every=5, recentre=2)
    tr = _restartable(gate)

    gate.propose(np.full(3, 1.0, np.float32), 10)     # the record
    assert _settle(gate)["accepted"] is True
    assert gate.periodic_rejects == 0 and gate.recentre_due() is False

    gate.propose(np.zeros(3, np.float32), 15, source="periodic")
    assert _settle(gate)["accepted"] is False
    assert gate.periodic_rejects == 1 and gate.recentre_due() is False

    gate.propose(np.zeros(3, np.float32), 20, source="periodic")
    _settle(gate)
    assert gate.periodic_rejects == 2 and gate.recentre_due() is True

    tr._recentre_on_record()
    assert list(np.asarray(tr.theta)) == [3.0, 3.0, 3.0]   # the record's theta
    assert not np.asarray(tr.m).any() and not np.asarray(tr.v).any()
    assert tr.adam_t == 0                     # or the first step is 3.16x lr
    assert (tr.sigma, tr.sigma_restarts, tr.sigma_steps) == (0.04, 1, 1)
    assert tr.last_improve == tr.t
    assert tr.last_recentre == {"record_gen": 10, "count": 2}
    # The run of refusals is over, whatever happens next.
    assert gate.periodic_rejects == 0 and gate.recentre_due() is False

    # An in-sim record being refused says something about that record, not
    # about the centre, so it does not count towards the next one.
    gate.propose(np.zeros(3, np.float32), 25)              # source="record"
    assert _settle(gate)["accepted"] is False
    assert gate.periodic_rejects == 0


def test_the_counter_survives_the_resume_and_a_confirmation_clears_it(fake):
    """The counter is a run of refusals *since the last confirmation*, and
    both halves have to hold across a checkpoint: a resume that forgot it
    would restart the count, and a confirmation that did not clear it would
    re-centre on the strength of candidates the record has already beaten."""
    gate = fake.gate([_step(3, 1), _step(3, 1),       # the record + its replicate
                      _step(1, 3),                    # a periodic refusal
                      _step(4, 0), _step(0, 4),       # provisional, then reverted
                      _step(4, 0), _step(4, 0)],      # provisional, then confirmed
                     every=5, recentre=3, replicate=True)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    _settle(gate)                                      # provisional
    assert _settle(gate)["confirmed"] is True          # ...confirmed
    assert (gate.win, gate.n, gate.periodic_rejects) == (0.75, 8, 0)

    gate.propose(np.zeros(3, np.float32), 15, source="periodic")
    _settle(gate)
    assert gate.periodic_rejects == 1

    gate.save()
    back = RealGate(gate.run_dir, "opp/main.py", games=2, every=5, recentre=3,
                    replicate=True, script=fake.script, python=sys.executable,
                    cwd=str(fake.root))
    assert back.load(gate.run_dir)["periodic_rejects"] == 1
    assert back.periodic_rejects == 1 and back.recentre_due() is False

    # A provisional acceptance that is then reverted is a refusal of the
    # centre like any other -- the one that costs the most, since the centre
    # briefly held the record.
    gate.propose(np.full(3, 2.0, np.float32), 20, source="periodic")
    assert _settle(gate)["provisional"] is True
    assert gate.recentre_due() is False                # never mid-replicate
    assert _settle(gate)["reverted"] is True
    assert gate.periodic_rejects == 2

    # And a confirmation ends the run of them.
    gate.propose(np.full(3, 3.0, np.float32), 25, source="periodic")
    _settle(gate)
    assert _settle(gate)["confirmed"] is True
    assert gate.periodic_rejects == 0 and gate.recentre_due() is False


# ------------------------------------------------- the provisional record

def test_the_record_moves_on_the_replicate_and_not_on_the_acceptance(fake):
    """Under `--real-gate-replicate` an acceptance is provisional: what moves
    `best_abs_theta` -- and so `best_abs.npy`, `--promote` and the stall clock
    -- is the *confirmation*, so every theta the file ever holds has been
    measured twice."""
    gate = fake.gate([_step(3, 1), _step(3, 1),       # incumbent + its replicate
                      _step(4, 0), _step(4, 0)],      # challenger + its replicate
                     replicate=True)
    tr = _stub_trainer(gate, t=100, last_improve=0)

    gate.propose(np.full(3, 1.0, np.float32), 10)
    prov = _through(tr)
    assert prov["accepted"] is False and prov["provisional"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [0.0, 0.0, 0.0]
    # `have_record` is what gates writing `best_abs.npy` at all, so the file
    # is not written for a provisional record either.
    assert gate.have_record is False and tr.last_improve == 0

    conf = _through(tr)
    assert conf["accepted"] is True and conf["confirmed"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [1.0, 1.0, 1.0]
    assert gate.have_record is True and tr.last_improve == tr.t
    assert (gate.win, gate.n, gate.record_gen) == (0.75, 8, 10)

    # The same again for a challenger, which now has a pooled bar to clear.
    tr.last_improve = 7
    gate.propose(np.full(3, 2.0, np.float32), 20)
    assert _through(tr)["provisional"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [1.0, 1.0, 1.0]
    assert tr.last_improve == 7
    assert _through(tr)["accepted"] is True
    assert list(np.asarray(tr.best_abs_theta)) == [2.0, 2.0, 2.0]
    assert (gate.win, gate.n, gate.record_gen) == (1.0, 8, 20)
    assert tr.last_improve == tr.t
    gate.close()


def test_a_record_that_fails_its_replicate_gives_the_bar_back(fake):
    """flow27c: a candidate read 79.2%/+7,022 on one n=48 draw, beat an
    incumbent pooled over n=96 at 78.1%/+6,135, replicated at 60.4% and left
    the run pooled at 69.8%/+5,291 -- the record got worse and the bar
    dropped with it. Confirmation compares pooled with pooled, and a
    candidate that cannot clear the incumbent that way is reverted: the bar,
    the generation and the theta all go back."""
    gate = fake.gate([_step(3, 1), _step(3, 1),       # incumbent: pooled 75%
                      _step(4, 0), _step(0, 4)],      # a lucky draw, then the truth
                     replicate=True)
    tr = _stub_trainer(gate, t=100)
    gate.propose(np.full(3, 1.0, np.float32), 10)
    _through(tr)
    _through(tr)
    assert (gate.win, gate.margin, gate.n) == (0.75, 5_000.0, 8)
    tr.last_improve = 7

    gate.propose(np.full(3, 2.0, np.float32), 20)
    prov = _through(tr)
    assert prov["provisional"] is True
    assert gate.prev_incumbent["record_gen"] == 10        # held, not discarded
    assert (gate.win, gate.n) == (1.0, 4)                 # the working bar

    # A resume landing here has to be able to revert too, or the crash itself
    # would confirm the candidate.
    gate.save()
    back = RealGate(gate.run_dir, "opp/main.py", games=2, replicate=True,
                    script=fake.script, python=sys.executable,
                    cwd=str(fake.root))
    back.load(gate.run_dir)
    assert back.prev_incumbent["record_gen"] == 10
    assert list(back.prev_incumbent["theta"]) == [1.0, 1.0, 1.0]
    assert back.replicate_due[1] == 20

    rev = _through(tr)
    assert rev["reverted"] is True and rev["accepted"] is False
    assert rev["replicate_win"] == 0.5                    # the candidate, pooled
    assert (rev["restored_win"], rev["restored_gen"]) == (0.75, 10)
    assert (gate.win, gate.margin) == (0.75, 5_000.0)
    assert (gate.n, gate.record_gen) == (8, 10)
    assert list(gate.record_theta) == [1.0, 1.0, 1.0]
    # `best_abs_theta` never moved, so `best_abs.npy` -- written from it at the
    # next checkpoint -- is the file it already was.
    assert list(np.asarray(tr.best_abs_theta)) == [1.0, 1.0, 1.0]
    assert tr.last_improve == 7                           # not an improvement
    assert gate.prev_incumbent is None and gate.reverts == 1


# ------------------------------------------------------- the periodic offer

def test_the_cadence_nominates_the_search_centre_when_the_gate_is_idle(fake):
    """In-sim records dry up -- most runs take their last inside the first
    ~1.5k generations -- and a gate fed by records alone then idles on an
    incumbent older than everything the run has learned since. Every
    `--real-gate-every` generations the centre itself is offered, and the
    verdict says which kind of candidate it judged."""
    gate = fake.gate([_step(3, 1), _step(4, 0)], every=5)
    tr = _stub_trainer(gate, t=4)
    tr.theta = np.full(3, 4.0, np.float32)

    tr._nominate_centre()
    assert gate.running is None and gate.pending is None    # 4 % 5 != 0

    tr.t = 5
    tr.theta = np.full(3, 5.0, np.float32)
    tr._nominate_centre()
    assert gate.running[1] == 5 and gate.running[2] == "periodic"
    res = _settle(gate)
    assert res["source"] == "periodic" and res["accepted"] is True
    assert list(fake.calls()[-1]["theta"]) == [5.0, 5.0, 5.0]  # the centre

    # ...and again at the next multiple, not in between.
    for t in (6, 7, 8, 9):
        tr.t = t
        tr._nominate_centre()
    assert gate.running is None and gate.pending is None
    tr.t = 10
    tr._nominate_centre()
    assert gate.running[1] == 10
    assert _settle(gate)["source"] == "periodic"

    # An in-sim record's nomination is a "record" whatever the cadence says.
    gate.propose(np.zeros(3, np.float32), 15)
    assert gate.running[2] == "record"
    gate.close()


def test_the_cadence_yields_to_an_eval_and_to_a_waiting_candidate(fake):
    """Queue depth 1 is the gate's whole cost model. The cadence adds
    nominations, never pressure: while the single slot is busy it says
    nothing, and it must never replace an in-sim record waiting in the one
    pending place with the live centre."""
    gate = fake.gate([{"hang": True}], every=5)
    tr = _stub_trainer(gate, t=5)

    gate.propose(np.full(3, 1.0, np.float32), 1)          # a record, in flight
    tr._nominate_centre()
    assert gate.due(5) is False
    assert gate.running[1] == 1 and gate.pending is None   # untouched

    gate.propose(np.full(3, 2.0, np.float32), 3)          # a record, waiting
    tr._nominate_centre()
    assert gate.due(5) is False
    assert gate.pending[1] == 3 and gate.pending[2] == "record"
    gate.close()

    # A periodic candidate is not carried across a resume: it is the centre of
    # a generation the resumed run has already left, and the cadence offers a
    # fresh one within N generations.
    other = fake.gate([], every=5)
    other.propose(np.full(3, 8.0, np.float32), 5, source="periodic")
    other.close()
    other.save()
    assert other.state()["pending_gen"] is None
    back = fake.gate([], every=5)
    back.load(other.run_dir)
    assert back.pending is None


def test_the_cadence_is_off_unless_the_flag_asks_for_it(fake, tmp_path):
    """Default 0 is the run that came before the flag: records are the only
    thing the gate ever measures. Generation 0 is never due either -- on a
    cold run that is the untrained init."""
    off = fake.gate([], every=0)
    tr = _stub_trainer(off)
    for t in (1, 5, 100, 1000):
        tr.t = t
        tr._nominate_centre()
    assert off.due(1000) is False
    assert off.running is None and off.pending is None

    on = fake.gate([], every=5)
    assert on.due(0) is False
    with pytest.raises(ValueError):
        RealGate(str(tmp_path), "x.py", every=-1)

    # And the flag is refused without the gate it nominates to, at startup
    # rather than as a silently ignored setting.
    args = _Args()
    args.real_gate, args.real_gate_every = False, 200
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(args, _stub_trainer(), str(tmp_path))
    assert "--real-gate-every requires --real-gate" in str(e.value)


# --------------------------------------------------------------- the driver

class _Args:
    """`scripts/train.py`'s parsed flags, as far as the gate reads them."""

    def __init__(self, **kw):
        self.real_gate = True
        self.real_gate_opponent = kw.pop("opponent", None)
        self.real_gate_games = kw.pop("games", 24)
        self.real_gate_workers = kw.pop("workers", 4)
        self.real_gate_seed_base = kw.pop("seed_base", 20260825)
        self.real_gate_metric = kw.pop("metric", "win")
        self.real_gate_every = kw.pop("every", 0)
        self.real_gate_replicate = kw.pop("replicate", False)
        self.real_gate_reset = kw.pop("reset", False)
        self.real_gate_recentre = kw.pop("recentre", 0)
        self.real_gate_fresh = kw.pop("fresh", False)
        self.real_gate_min_gain = kw.pop("min_gain", 0.0)
        self.real_gate_win_floor = kw.pop("win_floor", None)
        self.real_gate_seed_per_opponent = kw.pop("seed_per_opponent", False)
        self.__dict__.update(kw)


class _NoLaunch(RealGate):
    """The real gate with its subprocess disabled: these tests are about what
    `setup_real_gate` decides, not about running an eval."""

    def _launch(self):
        pass


def test_the_flag_off_is_the_run_that_came_before_it(tmp_path):
    """No gate object, nothing attached to the trainer, and `Trainer`'s own
    default is `None` -- which is what every `__new__` stub in the other test
    files relies on."""
    tr = _stub_trainer()
    tr.real_gate = None
    args = _Args()
    args.real_gate = False
    assert T.setup_real_gate(args, tr, str(tmp_path)) is None
    assert tr.real_gate is None
    assert Trainer.real_gate is None and Trainer.last_real_gate is None


def test_an_inherited_record_is_measured_before_it_can_veto_anything(
        tmp_path, monkeypatch):
    """A run resuming a checkpoint written *without* the flag has a record but
    no real number for it. Measuring it first is what makes the first
    candidate's comparison mean something -- and it is nominated, not waited
    on."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "main.py"
    opp.write_text("# a packaged agent\n")
    run = tmp_path / "run"
    run.mkdir()
    resume = tmp_path / "old"
    resume.mkdir()

    tr = _stub_trainer(t=1200)
    tr.best_abs = 5_000.0
    tr.best_abs_theta = np.full(3, 9.0, np.float32)
    gate = T.setup_real_gate(_Args(opponent=str(opp)), tr, str(run),
                             resume_dir=str(resume))
    assert tr.real_gate is gate and gate.have_record is False
    assert gate.pending[1] == 1200
    assert list(gate.pending[0]) == [9.0, 9.0, 9.0]

    # A cold start has no record to baseline, so nothing is nominated: the
    # first in-sim record of the run is the baseline.
    cold = _stub_trainer()
    cold.best_abs = NO_BEST
    g2 = T.setup_real_gate(_Args(opponent=str(opp)), cold, str(run))
    assert g2.pending is None and g2.win is None


def test_a_resumed_gate_does_not_re_measure_its_own_incumbent(
        tmp_path, monkeypatch):
    """The numbers are in `real_gate.json`; re-measuring would spend three
    minutes to learn what the file says, and would overwrite an incumbent with
    a fresh noisy reading of it."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "main.py"
    opp.write_text("# a packaged agent\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.66, "margin": 4_200.0, "record_gen": 900,
                   "have_record": True, "pending_gen": None}, fh)
    np.save(str(resume / "best_sim.npy"), np.full(3, 4.0, np.float32))

    tr = _stub_trainer(t=1500)
    tr.best_abs = 5_000.0
    gate = T.setup_real_gate(_Args(opponent=str(opp)), tr, str(tmp_path),
                             resume_dir=str(resume))
    assert (gate.win, gate.margin, gate.record_gen) == (0.66, 4_200.0, 900)
    assert gate.have_record is True and gate.pending is None
    # The in-sim record's theta is restored beside it, so `best_sim.npy` keeps
    # tracking the in-sim selector across the resume -- through `_fit_layout`,
    # like every other theta a checkpoint carries, so one written under an
    # older parameter layout comes back zero-padded rather than refused.
    sim = np.asarray(tr.best_sim_theta)
    assert list(sim[:3]) == [4.0, 4.0, 4.0] and not sim[3:].any()


def test_a_retired_record_keeps_the_bar_and_gives_up_the_theta(
        tmp_path, monkeypatch):
    """A ladder change (or `--reset-best`) retires the in-sim record and puts
    `best_abs_theta` back on the live theta. The gate's numbers survive it --
    they are real-engine numbers and the ladder change did not move the real
    engine -- but the claim that `best_abs.npy` holds a gated record does not,
    or the next in-sim record would write an unmeasured theta there."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "main.py"
    opp.write_text("# a packaged agent\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.66, "margin": 4_200.0, "record_gen": 900,
                   "have_record": True, "pending_gen": None}, fh)

    tr = _stub_trainer(t=1500)
    tr.best_abs = NO_BEST                     # what the reset leaves behind
    gate = T.setup_real_gate(_Args(opponent=str(opp)), tr, str(tmp_path),
                             resume_dir=str(resume))
    assert gate.have_record is False
    assert (gate.win, gate.margin) == (0.66, 4_200.0)
    assert gate.pending is None               # nothing worth baselining


def test_a_missing_opponent_is_refused_at_startup(tmp_path):
    """Minutes into a multi-hour run, not hours: the gate is useless without
    the opponent and the failure would otherwise surface as a silent stream of
    failed evals."""
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(_Args(opponent=str(tmp_path / "nope.py")),
                          _stub_trainer(), str(tmp_path))
    assert "real-gate-opponent" in str(e.value)
    with pytest.raises(ValueError):
        RealGate(str(tmp_path), "x.py", metric="coins")


def test_every_member_of_the_field_is_checked_and_the_bad_one_is_named(
        tmp_path, monkeypatch):
    """A field is as useless as a single opponent when one member is a typo,
    and the operator has to be told *which* -- a run that fails on the fourth
    path is otherwise a run that fails on "the opponent"."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    good = tmp_path / "good_main.py"
    good.write_text("# a packaged agent\n")
    bad = str(tmp_path / "typo_main.py")
    tr = _stub_trainer()
    tr.best_abs = 5_000.0
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(_Args(opponent=f"{good},{bad}"), tr, str(tmp_path))
    assert bad in str(e.value) and str(good) not in str(e.value)
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(_Args(opponent=""), _stub_trainer(), str(tmp_path))
    assert "real-gate-opponent" in str(e.value)


def test_a_resume_that_changes_the_field_is_refused_without_a_reset(
        tmp_path, monkeypatch):
    """The bar is a measurement against a field, so a segment that swaps the
    field is judging this field's candidates against the last field's number
    -- which is not a comparison. Refuse, and say which flag makes it legal."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    a, b = tmp_path / "a_main.py", tmp_path / "b_main.py"
    a.write_text("# a\n")
    b.write_text("# b\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.8, "margin": 5_000.0, "n": 48, "record_gen": 900,
                   "have_record": True, "pending_gen": None,
                   "opponent": [str(a)]}, fh)

    def _tr():
        tr = _stub_trainer(t=1500)
        tr.best_abs = 5_000.0
        tr.best_abs_theta = np.full(3, 9.0, np.float32)
        return tr

    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(_Args(opponent=f"{a},{b}"), _tr(), str(tmp_path),
                          resume_dir=str(resume))
    assert "--real-gate-reset" in str(e.value) and str(b) in str(e.value)

    # The field the bar was taken on resumes exactly as before -- including
    # the legacy spelling of a one-member field, a bare string.
    kept = T.setup_real_gate(_Args(opponent=str(a)), _tr(), str(tmp_path),
                             resume_dir=str(resume))
    assert (kept.win, kept.opponents) == (0.8, (str(a),))
    with open(str(resume / "real_gate.json")) as fh:
        legacy = json.load(fh)
    legacy["opponent"] = str(a)
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump(legacy, fh)
    old = T.setup_real_gate(_Args(opponent=str(a)), _tr(), str(tmp_path),
                            resume_dir=str(resume))
    assert old.win == 0.8

    # And the reset is the way to move the field: the bar goes, the record
    # theta stays and is re-nominated against the new one.
    fresh = T.setup_real_gate(_Args(opponent=f"{a},{b}", reset=True), _tr(),
                              str(tmp_path), resume_dir=str(resume))
    assert fresh.opponents == (str(a), str(b))
    assert (fresh.win, fresh.have_record) == (None, False)
    assert fresh.pending[1] == 1500


def test_a_resume_may_change_the_threshold_and_is_told_that_it_did(
        tmp_path, monkeypatch, capsys):
    """Unlike the field, the threshold is not part of what the bar *is*: the
    saved number stays a comparable measurement whatever this segment decides
    it wants to see before moving the record. So a change is legal -- no
    `--real-gate-reset`, no re-measurement -- and the run says so on one line,
    because the acceptance rate of every row after it changes with it."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "opp_main.py"
    opp.write_text("# opp\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.535, "margin": 3_080.0, "n": 128,
                   "record_gen": 200, "have_record": True, "pending_gen": None,
                   "opponent": [str(opp)]}, fh)      # written before the flag

    def _tr():
        tr = _stub_trainer(t=1500)
        tr.best_abs = 5_000.0
        tr.best_abs_theta = np.full(3, 9.0, np.float32)
        return tr

    gate = T.setup_real_gate(_Args(opponent=str(opp), min_gain=0.03), _tr(),
                             str(tmp_path), resume_dir=str(resume))
    assert (gate.min_gain, gate.win, gate.have_record) == (0.03, 0.535, True)
    out = capsys.readouterr().out
    assert "0 -> 0.03" in out and "win-rate points" in out

    # Resuming with the threshold the file records is not a change, and says
    # nothing.
    gate.save(str(resume))
    same = T.setup_real_gate(_Args(opponent=str(opp), min_gain=0.03), _tr(),
                             str(tmp_path), resume_dir=str(resume))
    assert same.min_gain == 0.03
    assert "acceptance threshold" not in capsys.readouterr().out


def test_a_resume_may_change_the_seed_draw_and_is_told_that_it_did(
        tmp_path, monkeypatch, capsys):
    """`--real-gate-seed-per-opponent` is wired the way `--real-gate-min-gain`
    is: the command line owns it, a resume that changes it is legal, and the
    change is printed because the games after the line are drawn differently.
    Without the gate the flag is refused rather than silently ignored."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "opp_main.py"
    opp.write_text("# opp\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.535, "margin": 3_080.0, "n": 128,
                   "record_gen": 200, "have_record": True, "pending_gen": None,
                   "opponent": [str(opp)]}, fh)     # written before the flag

    def _tr():
        tr = _stub_trainer(t=1500)
        tr.best_abs = 5_000.0
        tr.best_abs_theta = np.full(3, 9.0, np.float32)
        return tr

    gate = T.setup_real_gate(_Args(opponent=str(opp), seed_per_opponent=True),
                             _tr(), str(tmp_path), resume_dir=str(resume))
    assert (gate.seed_per_opponent, gate.win) == (True, 0.535)
    out = capsys.readouterr().out
    assert "shared -> per opponent" in out

    # Resuming on the draw the file records says nothing.
    gate.save(str(resume))
    same = T.setup_real_gate(_Args(opponent=str(opp), seed_per_opponent=True),
                             _tr(), str(tmp_path), resume_dir=str(resume))
    assert same.seed_per_opponent is True
    assert "seeds" not in capsys.readouterr().out

    args = _Args(seed_per_opponent=True)
    args.real_gate = False
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(args, _stub_trainer(), str(tmp_path))
    assert "--real-gate-seed-per-opponent requires --real-gate" in str(e.value)


def test_a_negative_threshold_is_refused_at_startup(tmp_path):
    """And the flag needs a gate to be a threshold on."""
    opp = tmp_path / "opp_main.py"
    opp.write_text("# opp\n")
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(_Args(opponent=str(opp), min_gain=-1.0),
                          _stub_trainer(), str(tmp_path))
    assert "--real-gate-min-gain must be >= 0" in str(e.value)

    args = _Args(min_gain=0.03)
    args.real_gate = False
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(args, _stub_trainer(), str(tmp_path))
    assert "--real-gate-min-gain requires --real-gate" in str(e.value)


def test_the_win_floor_needs_the_metric_it_protects(tmp_path, monkeypatch):
    """Under `--real-gate-metric win` the win rate already decides, so a floor
    on it is a no-op -- and a no-op that reads like a protection is worse than
    an error. Refused at startup, along with a negative slack and the flag
    without the gate. 0.0 is a *setting*, so none of these may be a truthiness
    test that silently lets it through."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "opp_main.py"
    opp.write_text("# opp\n")

    for floor in (0.0, 0.03):
        with pytest.raises(SystemExit) as e:
            T.setup_real_gate(_Args(opponent=str(opp), win_floor=floor),
                              _stub_trainer(), str(tmp_path))
        assert "--real-gate-win-floor requires --real-gate-metric margin" \
            in str(e.value)

    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(
            _Args(opponent=str(opp), metric="margin", win_floor=-0.01),
            _stub_trainer(), str(tmp_path))
    assert "--real-gate-win-floor must be >= 0" in str(e.value)

    args = _Args(metric="margin", win_floor=0.0)
    args.real_gate = False
    with pytest.raises(SystemExit) as e:
        T.setup_real_gate(args, _stub_trainer(), str(tmp_path))
    assert "--real-gate-win-floor requires --real-gate" in str(e.value)

    # And with the metric it protects it is simply plumbed through.
    tr = _stub_trainer(t=1500)
    tr.best_abs = 5_000.0
    tr.best_abs_theta = np.full(3, 9.0, np.float32)
    gate = T.setup_real_gate(
        _Args(opponent=str(opp), metric="margin", win_floor=0.03),
        tr, str(tmp_path))
    assert gate.win_floor == 0.03


def test_a_resume_may_change_the_win_floor_and_is_told_that_it_did(
        tmp_path, monkeypatch, capsys):
    """Like the threshold: the floor is what this segment will tolerate, not
    part of what the saved bar measured, so a change is legal and only has to
    be said out loud."""
    monkeypatch.setattr(T, "RealGate", _NoLaunch)
    opp = tmp_path / "opp_main.py"
    opp.write_text("# opp\n")
    resume = tmp_path / "old"
    resume.mkdir()
    with open(str(resume / "real_gate.json"), "w") as fh:
        json.dump({"win": 0.535, "margin": 3_080.0, "n": 128,
                   "record_gen": 200, "have_record": True, "pending_gen": None,
                   "opponent": [str(opp)]}, fh)     # written before the flag

    def _tr():
        tr = _stub_trainer(t=1500)
        tr.best_abs = 5_000.0
        tr.best_abs_theta = np.full(3, 9.0, np.float32)
        return tr

    args = dict(opponent=str(opp), metric="margin", win_floor=0.03)
    gate = T.setup_real_gate(_Args(**args), _tr(), str(tmp_path),
                             resume_dir=str(resume))
    assert (gate.win_floor, gate.win) == (0.03, 0.535)
    assert "win floor off -> 0.03" in capsys.readouterr().out

    # Resuming on the floor the file records says nothing...
    gate.save(str(resume))
    same = T.setup_real_gate(_Args(**args), _tr(), str(tmp_path),
                             resume_dir=str(resume))
    assert same.win_floor == 0.03
    assert "win floor" not in capsys.readouterr().out

    # ...and turning it off is a change like any other.
    off = T.setup_real_gate(_Args(opponent=str(opp), metric="margin"), _tr(),
                            str(tmp_path), resume_dir=str(resume))
    assert off.win_floor is None
    assert "win floor 0.03 -> off" in capsys.readouterr().out


# ------------------------------------------------------- the untouched files

def test_a_checkpoint_is_the_one_the_flag_did_not_change(tmp_path):
    """`state.npz` carries no gate field: the gate's state is a sidecar JSON
    precisely so that a run without `--real-gate` writes the checkpoint it
    wrote before the flag existed, and so that a gated checkpoint resumes on a
    build that has never heard of it."""
    import jax
    import jax.numpy as jnp

    tr = Trainer.__new__(Trainer)
    tr.n = 3
    tr.theta = jnp.zeros(3)
    tr.champion, tr.champion_score = jnp.zeros(3), 1.0
    tr.pool = [jnp.zeros(3)]
    tr.archetypes, tr.archetype_names = [], []
    tr.rung_weights = np.ones(0)
    tr.arch_handicap = np.zeros((0, 2), np.int32)
    tr.holdout_thetas = ()
    tr.m, tr.v, tr.t, tr.adam_t = jnp.zeros(3), jnp.zeros(3), 5, 5
    tr.key = jax.random.PRNGKey(0)
    tr.best_abs, tr.best_abs_theta = 1.0, jnp.zeros(3)
    tr.best_sim_theta = jnp.ones(3)
    tr.best_hold = NO_BEST
    tr.rng = np.random.default_rng(0)
    tr.sigma, tr.sigma_restarts, tr.sigma_steps = 0.02, 0, 0
    tr.last_improve, tr.replicate_rejects = 0, 0
    tr.cfg = Config()

    T.save_state(str(tmp_path), tr, gen=5, elapsed=1.0)
    keys = set(np.load(str(tmp_path / "state.npz")).files)
    assert not [k for k in keys if "real" in k or "sim" in k]
    assert keys == {
        "theta", "champion", "champion_score", "pool", "archetypes",
        "archetype_names", "ladder_sig", "m", "v", "t", "adam_t", "key",
        "gen", "best_abs", "best_abs_theta", "best_hold", "rng_state",
        "sigma", "sigma_restarts", "sigma_steps", "last_improve",
        # `--slot-rotation carry`'s running credit: where in the rotation the
        # ladder is, which is run state exactly as `sigma_restarts` is. Empty
        # under `--slot-rotation fixed`.
        "replicate_rejects", "slot_credit", "elapsed"}
