"""`--real-gate-pinned`: the gate judges on the live games themselves.

An opponent package cut with `scripts/tape_opponent.py --with-town` replays a
real Kaggle episode move for move, and the only randomness the engine still
draws for itself is the end-of-day shop -- which `scripts/town_inject.py` pins
from the schedule named by `KAGG3_TOWN_SCHEDULE`. With the town pinned the
engine reproduces the live game *to the coin*, for every seed and in either
seat, so the gate's usual apparatus -- a seed count, a replicate, a fresh base,
a paired t -- is answering a lottery that is no longer being run.

What is left is a deterministic set of live replicas and one question: which of
the games we actually played would this candidate have flipped. These tests pin
that: the default path is byte-identical to the gate that shipped before the
flag, a pinned leg is exactly one game per opponent per seat played (both by
default, seat 0 alone under `--real-gate-pinned-seats 1`) on the fixed seed,
the schedule reaches the eval through the environment, and the verdict is a
count of flips and drops -- named by tape id in `real_gate.log`.

Every eval here is a *fake* `eval_vs_baselines.py` whose per-game outcomes this
file dictates, so nothing starts the real engine.
"""
from __future__ import annotations

import json
import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest

from kagg3.es.train import RealGate, pinned_tally, pinned_tape_id

#: `scripts/eval_vs_baselines.py:CSV_HEADER`, spelled out rather than imported
#: so a change to it fails here instead of being agreed to by construction.
HEADER = ["seed", "opponent", "seat", "mine", "theirs",
          "moves", "move_turns", "noops", "unsold", "quads"]

#: A stand-in for the evaluator. It plays no game: the (mine, theirs) of every
#: (opponent, seat) comes from `outcomes.json`, keyed by the first element of
#: the theta it was handed, so a test can say exactly which games each policy
#: won. It records its argv AND the town-schedule variable it was launched
#: with, which is the only way the pin reaches the engine.
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
ap.add_argument("--seats", type=int, default=2)
ap.add_argument("--csv")
a = ap.parse_args()

run = os.path.dirname(os.path.abspath(a.csv))
tag = str(int(np.load(a.theta)[0]))
with open(os.path.join(run, "fake_calls.jsonl"), "a") as fh:
    fh.write(json.dumps({"argv": sys.argv[1:], "tag": tag,
                         "town": os.environ.get("KAGG3_TOWN_SCHEDULE")}) + "\\n")

table = json.load(open(os.path.join(run, "outcomes.json")))[tag]
rows = []
for i, opp in enumerate(a.opponents):
    for s in range(int(a.games)):
        for seat in range(a.seats):
            mine, theirs = table[opp]
            rows.append([a.seed_base + s, opp, seat, mine, theirs, 0, 0, 0, 0, 4])
with open(a.csv, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow({header})
    w.writerows(rows)
'''.replace("{header}", repr(HEADER))

#: Three pinned tapes, named the way `artifacts/panel_opp_town` names them.
TAPES = ["t/opponent_tape_111/main.py", "t/opponent_tape_222/main.py",
         "t/opponent_tape_333/main.py"]


class _Fake:
    """A gate factory whose evals are the fake script above."""

    def __init__(self, tmp_path):
        self.root = str(tmp_path)
        self.script = os.path.join(self.root, "fake_eval.py")
        with open(self.script, "w") as fh:
            fh.write(FAKE_EVAL)
        self.run = os.path.join(self.root, "run")
        os.makedirs(self.run, exist_ok=True)
        self.schedule = os.path.join(self.root, "town_schedules.json")
        with open(self.schedule, "w") as fh:
            json.dump({"111": [[3, "BAKERY"]], "222": [[4, "PET_CAFE"]],
                       "333": [[5, "YARN_STORE"]]}, fh)

    def outcomes(self, table):
        """`{theta tag: {opponent: (mine, theirs)}}` for the next evals."""
        with open(os.path.join(self.run, "outcomes.json"), "w") as fh:
            json.dump(table, fh)

    def gate(self, opponent=None, **kw):
        kw.setdefault("workers", 1)
        kw.setdefault("seed_base", 20260825)
        return RealGate(self.run, opponent or TAPES, script=self.script,
                        python=sys.executable, cwd=self.root, **kw)

    def calls(self):
        p = os.path.join(self.run, "fake_calls.jsonl")
        if not os.path.isfile(p):
            return []
        with open(p) as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def log(self):
        with open(os.path.join(self.run, "real_gate.log")) as fh:
            return fh.read()


@pytest.fixture
def fake(tmp_path):
    return _Fake(tmp_path)


def _settle(gate):
    """Block until the in-flight eval exits, then take its verdict.

    A *test* may wait; the trainer never does (`poll` is a `waitpid(WNOHANG)`).
    """
    assert gate.proc is not None, "nothing in flight"
    gate.proc.wait()
    return gate.poll()


def _round(fake, cand, inc, **kw):
    """One pinned round: `cand` and `inc` are `{opponent: (mine, theirs)}`.

    The incumbent is seated as the gate's record theta, so the round pairs --
    which is what a candidate after the first one always faces.
    """
    fake.outcomes({"1": cand, "2": inc})
    gate = fake.gate(pinned=fake.schedule, **kw)
    gate.record_theta = np.array([2.0], np.float32)
    gate.propose(np.array([1.0], np.float32), 10)
    assert _settle(gate) is None, "the candidate leg decides nothing alone"
    return gate, _settle(gate)


def _table(*results):
    """`{opponent: (mine, theirs)}` from a win/loss letter per tape."""
    out = {}
    for opp, r in zip(TAPES, results):
        out[opp] = (110_000.0, 100_000.0) if r == "W" else (100_000.0, 110_000.0)
    return out


# ------------------------------------------------------- the default path

def test_the_unpinned_gate_launches_the_argv_it_always_did(fake):
    """Off (the default), nothing changes: the same flags, the same games, and
    no town variable in the child's environment. `pinned=None` has to be the
    run that came before the flag, byte for byte."""
    fake.outcomes({"1": _table("W", "W", "W")})
    gate = fake.gate(games=3)
    gate.propose(np.array([1.0], np.float32), 7)
    res = _settle(gate)
    assert res["accepted"] is True
    call, = fake.calls()
    assert call["argv"] == [
        "--theta", gate.theta_path, "--opponents", *TAPES,
        "--games", "3", "--workers", "1",
        "--seed-base", "20260825", "--csv", gate.csv_path]
    assert call["town"] is None
    assert gate.pinned is None and gate.min_flips == 1


# -------------------------------------------------------- the pinned leg

def test_a_pinned_leg_is_one_game_per_opponent_per_seat_on_the_fixed_seed(fake):
    """The set is not a draw. Every opponent is played once, in both seats, on
    `--real-gate-seed-base` -- and both legs of the round play the same one, or
    the two readings would not be the same games."""
    _gate, res = _round(fake, _table("W", "W", "L"), _table("W", "L", "L"))
    cand, inc = fake.calls()
    for call in (cand, inc):
        assert call["argv"][call["argv"].index("--games") + 1] == "1"
        assert call["argv"][call["argv"].index("--seed-base") + 1] == "20260825"
        assert "--seed-per-opponent" not in call["argv"]
    assert res["pinned_n"] == len(TAPES) * 2 == res["games"]
    assert res["games"] == 6


def test_the_default_pinned_leg_still_plays_both_seats_of_every_board(fake):
    """`--real-gate-pinned-seats` defaults to 2, and at 2 the argv carries no
    `--seats` at all -- so the pinned gate that shipped before the flag
    launches the same command it always did, and its 3 tapes are 6 games."""
    gate, res = _round(fake, _table("W", "W", "L"), _table("W", "L", "L"))
    assert gate.pinned_seats == 2 and gate.seats == 2
    for call in fake.calls():
        assert "--seats" not in call["argv"]
    assert res["games"] == res["pinned_n"] == len(TAPES) * 2 == 6


def test_one_seat_plays_each_board_once_and_says_so_in_the_log(fake):
    """`--real-gate-pinned-seats 1` hands the evaluator `--seats 1`, which
    plays seat 0 and stops. The set is then N games for N tapes -- a game IS a
    board -- and both legs of the round play the same one, or the two readings
    would not be the same boards. The log's header says which mode ran,
    because a count of flips means a different thing in each."""
    gate, res = _round(fake, _table("W", "W", "L"), _table("W", "L", "L"),
                       pinned_seats=1)
    assert gate.pinned_seats == 1 and gate.seats == 1
    cand, inc = fake.calls()
    for call in (cand, inc):
        assert call["argv"][call["argv"].index("--seats") + 1] == "1"
        assert call["argv"][call["argv"].index("--games") + 1] == "1"
        assert call["argv"][call["argv"].index("--seed-base") + 1] == "20260825"
    assert res["games"] == res["pinned_n"] == len(TAPES) == 3
    # One tape changed hands, and it is worth one flip rather than two.
    assert (res["pinned_flips"], res["pinned_drops"]) == (1, 0)
    assert res["pinned_flipped"] == ["222/0"]
    assert "pinned mode seats: 1" in fake.log()
    assert "1 game x 1 seat)" in fake.log()
    assert "3 boards" in fake.log()


def test_an_unpinned_gate_never_drops_a_seat(fake):
    """The seat is only redundant because the town is pinned. On a drawn board
    the two seats are two different games and the pair is what cancels the
    seat bias, so `seats` ignores the flag when `pinned` is off -- and an
    out-of-range value is refused at construction rather than passed on to an
    evaluator that would reject it mid-run."""
    assert fake.gate(pinned_seats=1).seats == 2
    with pytest.raises(ValueError, match="expected 1 or 2"):
        fake.gate(pinned=fake.schedule, pinned_seats=0)


def test_the_schedule_reaches_the_eval_through_the_environment(fake):
    """`KAGG3_TOWN_SCHEDULE` is the whole mechanism: `eval_vs_baselines._play`
    hands it to `town_inject.install_from_env(opponent)` before every game, and
    that is what makes the engine reproduce the live town. If it does not reach
    the child, the tapes play under a freshly drawn town and the set stops
    being a replica of anything."""
    gate, _res = _round(fake, _table("W", "W", "W"), _table("W", "W", "W"))
    for call in fake.calls():
        assert call["town"] == os.path.abspath(fake.schedule)
    assert gate.pinned == os.path.abspath(fake.schedule)


def test_pinned_mode_makes_the_lottery_flags_inert(fake):
    """A deterministic game has nothing to replicate, no second base to be
    fresh on and no standard error to test, so those flags are dropped rather
    than obeyed -- and the gate says which ones it dropped."""
    gate = fake.gate(pinned=fake.schedule, games=24, replicate=True,
                     replicate_games=48, fresh=True, seed_per_opponent=True,
                     paired_t=1.7)
    assert (gate.games, gate.replicate_games) == (1, 1)
    assert gate.replicate is False and gate.fresh is False
    assert gate.seed_per_opponent is False and gate.paired_t == 0.0
    assert "--real-gate-replicate" in gate.pinned_ignored
    assert "--real-gate-paired-t" in gate.pinned_ignored
    fake.outcomes({"1": _table("W", "W", "W")})
    gate.propose(np.array([1.0], np.float32), 3)
    _settle(gate)
    assert "pinned mode IGNORES" in fake.log()


# ------------------------------------------------------ flips and drops

def test_flips_and_drops_are_counted_on_a_synthetic_table():
    """The accounting, on rows nothing had to play: a flip is a game the
    incumbent did not win and the candidate did, a drop is the reverse, and
    `cand_wins - inc_wins` is exactly `flips - drops` -- which is why the rule
    can be stated in either currency. Ties are losses for the flip count (the
    leaderboard scores `mine > theirs`) but half a win for the rates."""
    def rows(*pairs):
        return {(20260825, TAPES[i], seat): pairs[i]
                for i in range(len(pairs)) for seat in (0, 1)}

    t = pinned_tally(rows((110., 100.), (100., 110.), (100., 100.)),
                     rows((100., 110.), (100., 110.), (110., 100.)))
    assert (t["n"], t["cand_wins"], t["inc_wins"]) == (6, 2, 2)
    assert (t["flips"], t["drops"]) == (2, 2)
    assert t["flipped"] == ["111/0", "111/1"]
    assert t["dropped"] == ["333/0", "333/1"]
    assert t["cand_wins"] - t["inc_wins"] == t["flips"] - t["drops"]
    assert t["cand_win"] == pytest.approx((2 + 0.5 * 2) / 6)
    assert pinned_tally({}, rows((1., 2.))) is None
    assert pinned_tally(rows((1., 2.)), {(1, "other", 0): (1., 2.)}) is None
    assert pinned_tape_id("a/opponent_tape_105228357/main.py") == "105228357"


def test_the_tally_over_one_row_per_board_counts_each_flip_once():
    """The same accounting on a one-seat table: N boards, N rows, and a board
    that changes hands moves the counts by one rather than two. This is the
    arithmetic `--real-gate-min-flips` is read in under
    `--real-gate-pinned-seats 1`, so a threshold of 2 there asks for two live
    games, where at two seats it asks for one played twice."""
    def rows(*pairs):
        return {(20260825, TAPES[i], 0): pairs[i] for i in range(len(pairs))}

    t = pinned_tally(rows((110., 100.), (100., 110.), (100., 100.)),
                     rows((100., 110.), (100., 110.), (110., 100.)))
    assert (t["n"], t["cand_wins"], t["inc_wins"]) == (3, 1, 1)
    assert (t["flips"], t["drops"]) == (1, 1)
    assert t["flipped"] == ["111/0"] and t["dropped"] == ["333/0"]
    assert t["cand_wins"] - t["inc_wins"] == t["flips"] - t["drops"]
    assert t["cand_win"] == pytest.approx((1 + 0.5) / 3)
    # Half the rows of the two-seat reading of the same three boards, and
    # every rate identical -- which is what makes the second seat redundant.
    both = {(20260825, TAPES[i], seat): p
            for i, p in enumerate(((110., 100.), (100., 110.), (100., 100.)))
            for seat in (0, 1)}
    both_inc = {(20260825, TAPES[i], seat): p
                for i, p in enumerate(((100., 110.), (100., 110.), (110., 100.)))
                for seat in (0, 1)}
    two = pinned_tally(both, both_inc)
    assert two["n"] == 2 * t["n"]
    assert two["flips"] == 2 * t["flips"] and two["drops"] == 2 * t["drops"]
    assert two["cand_win"] == pytest.approx(t["cand_win"])
    assert two["cand_margin"] == pytest.approx(t["cand_margin"])


@pytest.mark.parametrize(
    "cand,inc,min_flips,accepted",
    [(("W", "L", "L"), ("L", "L", "L"), 1, True),    # one flip, nothing back
     (("W", "L", "L"), ("L", "W", "L"), 1, False),   # one flip, one drop
     (("W", "W", "L"), ("L", "W", "W"), 1, False),   # 2 flips, 2 drops: net 0
     (("W", "W", "L"), ("L", "L", "W"), 1, True),    # 4 flips, 2 drops
     (("W", "W", "L"), ("L", "L", "W"), 3, False),   # ... but not 3 net
     (("W", "L", "L"), ("W", "L", "L"), 0, False)])  # identical: nothing moved
def test_the_acceptance_rule_turns_on_net_flips(fake, cand, inc, min_flips,
                                                accepted):
    """The boundaries. Net flips must reach `--real-gate-min-flips` AND the
    candidate must win strictly more of the set -- the second condition is
    what keeps `min_flips 0` from accepting a theta that changed nothing.
    Every tape is played in both seats, so a tape that changes hands is worth
    two."""
    gate, res = _round(fake, _table(*cand), _table(*inc), min_flips=min_flips)
    assert res["accepted"] is accepted
    assert res["accepted"] == (gate.record_theta[0] == 1.0)
    assert (res["pinned_flips"] - res["pinned_drops"] >= min_flips
            and res["pinned_wins"] > res["pinned_incumbent_wins"]) is accepted


def test_the_log_names_the_tapes_that_changed_hands(fake):
    """A pinned verdict's interesting fact is *which* live games moved: each is
    an episode an operator can pull up and read. Win rates are recoverable from
    the counts; the ids are not recoverable from anything."""
    _round(fake, _table("W", "W", "L"), _table("L", "W", "W"))
    log = fake.log()
    assert "FLIPS +2 DROPS -2" in log
    assert "flipped: 111/0 111/1" in log
    assert "dropped: 333/0 333/1" in log
    assert "-> refuse" in log


def test_the_margin_metric_still_decides_on_coins(fake):
    """`--real-gate-metric margin` keeps its rule, measured on the incumbent's
    own reading of these same games rather than on a bar from another set: a
    candidate that flips nothing but gains coins is accepted, and
    `--real-gate-min-gain` is still the size of the gain it must show."""
    cand = {t: (120_000.0, 100_000.0) for t in TAPES}
    inc = {t: (110_000.0, 100_000.0) for t in TAPES}
    _, res = _round(fake, cand, inc, metric="margin")
    assert res["pinned_flips"] == res["pinned_drops"] == 0
    assert res["accepted"] is True
    _, res = _round(fake, cand, inc, metric="margin", min_gain=20_000.0)
    assert res["accepted"] is False


# ------------------------------------------------- what an acceptance moves

def test_a_pinned_acceptance_hands_the_next_round_the_accepted_theta(fake):
    """An accepted candidate becomes the bar: its numbers AND its theta.

    The pinned verdict is final -- the replicate that confirms an unpinned
    acceptance is a second reading of a deterministic game and is switched off
    (`__init__`) -- so `_decide_pinned` has to do everything `_confirm` does in
    default mode. Two rounds on one gate say it did: the second round's
    incumbent leg replays the theta the first round accepted, not the one the
    run started on, and `res["theta"]` is the candidate's (it is what
    `Trainer._poll_real_gate` writes into `best_abs_theta`).
    """
    fake.outcomes({"1": _table("W", "W", "L"),    # round 1's candidate
                   "2": _table("L", "L", "L"),    # the init incumbent
                   "3": _table("W", "W", "W")})   # round 2's candidate
    gate = fake.gate(pinned=fake.schedule, pinned_seats=1, metric="win")
    gate.record_theta = np.array([2.0], np.float32)
    gate.propose(np.array([1.0], np.float32), 10)
    assert _settle(gate) is None
    first = _settle(gate)
    assert first["accepted"] is True
    assert float(np.asarray(first["theta"])[0]) == 1.0
    assert gate.have_record is True and gate.accepts == 1
    # The bar is the candidate's own reading of the set, not the init's.
    assert gate.record_theta[0] == 1.0
    assert gate.win == pytest.approx(2 / 3) and gate.record_gen == 10

    gate.propose(np.array([3.0], np.float32), 20)
    assert _settle(gate) is None
    second = _settle(gate)
    # The incumbent leg of round 2 played theta "1" -- the accepted record.
    assert [c["tag"] for c in fake.calls()] == ["1", "2", "3", "1"]
    assert second["paired_win"] == pytest.approx(2 / 3)
    assert second["accepted"] is True and gate.record_theta[0] == 3.0


def test_a_pinned_acceptance_lets_best_abs_npy_be_written(fake):
    """The gate's record is the whole of the question `best_abs.npy` asks.

    `best_abs` (the in-sim threshold) is `NO_BEST` on exactly the resume that
    retires the in-sim record while the gate keeps its real-engine bar, and
    the old guard `math.isfinite(best_abs) and gate.have_record` then refused
    to write the file for the rest of the run -- so a pinned acceptance moved
    `best_abs_theta` in memory and the deliverable on disk stayed the init
    theta (flow150, gen 42). Ungated the rule is unchanged.
    """
    from train import record_theta_ready

    assert record_theta_ready(float("-inf"), None) is False
    assert record_theta_ready(1234.0, None) is True

    fake.outcomes({"1": _table("W", "W", "L"), "2": _table("L", "L", "L")})
    gate = fake.gate(pinned=fake.schedule, pinned_seats=1, metric="win")
    gate.record_theta = np.array([2.0], np.float32)
    assert record_theta_ready(float("-inf"), gate) is False, \
        "no verdict yet: the file waits for the real engine"
    gate.propose(np.array([1.0], np.float32), 10)
    assert _settle(gate) is None
    assert _settle(gate)["accepted"] is True
    assert record_theta_ready(float("-inf"), gate) is True


def test_a_pinned_acceptance_clears_the_run_that_earns_a_recentre(fake):
    """`--real-gate-recentre K` still counts, and an acceptance resets it.

    Pinned mode switches off the replicate, and `recentre_due` refuses to fire
    while one is owed -- so this checks the flag is armed rather than wedged:
    one refused periodic candidate at `recentre=1` is due, and the acceptance
    that follows puts the count back to zero (the centre would be sent to the
    theta the gate just took, not to a stale one).
    """
    fake.outcomes({"1": _table("L", "L", "L"),    # the centre, refused
                   "2": _table("W", "W", "L"),    # the incumbent
                   "3": _table("W", "W", "W")})   # a record, accepted
    gate = fake.gate(pinned=fake.schedule, pinned_seats=1, metric="win",
                     every=5, recentre=1)
    gate.record_theta = np.array([2.0], np.float32)
    gate.have_record = True
    gate.win, gate.margin, gate.n = 1.0, 10_000.0, 3
    gate.propose(np.array([1.0], np.float32), 10, source="periodic")
    assert _settle(gate) is None
    assert _settle(gate)["accepted"] is False
    assert gate.periodic_rejects == 1 and gate.recentre_due() is True

    gate.propose(np.array([3.0], np.float32), 20)
    assert _settle(gate) is None
    assert _settle(gate)["accepted"] is True
    assert gate.periodic_rejects == 0 and gate.recentre_due() is False


def test_a_settled_gate_leaves_no_pending_nomination_behind(fake):
    """`real_gate_pending.npy` is a live nomination or it is not there.

    `load` reads it only when `pending_gen` names a generation, so a fossil
    was harmless -- but it is the file an operator reads to see what the gate
    is working on, and after flow150's acceptance it still held the decided
    candidate.
    """
    fake.outcomes({"1": _table("W", "W", "L"), "2": _table("L", "L", "L")})
    gate = fake.gate(pinned=fake.schedule, pinned_seats=1, metric="win")
    gate.record_theta = np.array([2.0], np.float32)
    gate.propose(np.array([1.0], np.float32), 10)
    gate.save()
    assert os.path.isfile(gate.pending_path), "a nomination is in flight"
    assert _settle(gate) is None
    assert _settle(gate)["accepted"] is True
    gate.save()
    assert json.load(open(gate.json_path))["pending_gen"] is None
    assert not os.path.isfile(gate.pending_path)
