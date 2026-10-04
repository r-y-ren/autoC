"""`--real-gate-paired-t`: the gate stops accepting the board lottery.

Both legs of a `--real-gate-fresh` round play the *same* seed base against the
same field, so every game the candidate played has a twin in the incumbent's
CSV -- and until this flag the gate threw those rows away and compared two
means. That comparison cannot tell a real gain from the board lottery: across
flow96-flow111 nearly every gated "record" failed when replicated locally on
576-832 paired boards, and a seed set of the gate's own size swings a candidate
by +-8 win-rate points on its own. `--real-gate-min-gain` is a fixed bar
guessed against that spread; the per-game paired difference *measures* it.

The tests below are arithmetic on the paired statistic, then the same
end-to-end fake-eval gate `test_real_gate.py` drives -- no engine, seconds to
run.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest

from kagg3.es.train import RealGate, paired_stats, read_eval_games

from test_real_gate import HEADER, _bases, _round, _step, fake  # noqa: F401


def _csv(path, rows, opponent="kagg2"):
    import csv
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        for i, (mine, theirs) in enumerate(rows):
            w.writerow([i, opponent, i % 2, mine, theirs, 0, 0, 0, 0, 4])


# ------------------------------------------------------------- the statistic

def test_the_rows_are_keyed_the_way_paired_ci_keys_them(tmp_path):
    """`(seed, opponent, seat)` -- the same key `scripts/paired_ci.py` pairs
    on, so the gate and the offline confidence interval cannot disagree about
    which two games are the same game."""
    p = str(tmp_path / "a.csv")
    _csv(p, [(10.0, 4.0), (3.0, 9.0)])
    assert read_eval_games(p) == {(0, "kagg2", 0): (10.0, 4.0),
                                  (1, "kagg2", 1): (3.0, 9.0)}
    assert read_eval_games(str(tmp_path / "missing.csv")) is None


def test_a_single_extra_win_out_of_twenty_four_is_one_standard_error(tmp_path):
    """The number the flag exists for. One game in 24 is a paired difference
    of a single +1 among 23 zeros, whose mean is exactly its own standard
    error: t = 1.0, which no honest threshold accepts -- and which the old
    rule took as a record (flow59 accepted 47.7% over 46.9% and confirmed it
    at 46.1%)."""
    cand = {(i, "o", 0): (100.0, 0.0) if i < 13 else (0.0, 100.0)
            for i in range(24)}
    inc = {(i, "o", 0): (100.0, 0.0) if i < 12 else (0.0, 100.0)
           for i in range(24)}
    st = paired_stats(cand, inc)
    assert st["n"] == 24
    assert st["win"] == pytest.approx(1 / 24)
    assert st["t_win"] == pytest.approx(1.0)

    # Six extra wins on the same 24 boards is the same arithmetic and clears
    # a 1.7 threshold, so the test is a test and not a ban.
    cand6 = {(i, "o", 0): (100.0, 0.0) if i < 18 else (0.0, 100.0)
             for i in range(24)}
    assert paired_stats(cand6, inc)["t_win"] == pytest.approx(2.7689, rel=1e-3)


def test_two_identical_readings_are_never_an_improvement(tmp_path):
    """`sd == 0` with a zero mean is t = 0, not a division by zero: two thetas
    that scored the same on every shared game are one reading twice."""
    same = {(i, "o", 0): (100.0, 50.0) for i in range(8)}
    st = paired_stats(same, dict(same))
    assert st["t_win"] == 0.0 and st["t_margin"] == 0.0
    # A constant *non-zero* difference is infinitely significant, correctly:
    # the candidate beat the incumbent on every single board.
    better = {(i, "o", 0): (200.0, 50.0) for i in range(8)}
    assert paired_stats(better, same)["t_margin"] == np.inf


def test_only_the_games_both_legs_played_are_paired():
    """A leg that played other boards contributes nothing; no shared board at
    all is `None`, which the gate refuses rather than waves through."""
    a = {(0, "o", 0): (1.0, 0.0), (1, "o", 0): (1.0, 0.0)}
    b = {(1, "o", 0): (0.0, 1.0), (2, "o", 0): (0.0, 1.0)}
    assert paired_stats(a, b)["n"] == 1
    assert paired_stats(a, {(9, "o", 0): (0.0, 1.0)}) is None


# ------------------------------------------------------------- the gate rule

def _gate(fake, steps, **kw):
    kw.setdefault("replicate", True)
    kw.setdefault("fresh", True)
    kw.setdefault("fresh_seed", 5)
    return fake.gate(steps, **kw)


def _baseline(gate):
    """Take the first record, which is a baseline and unopposed."""
    gate.propose(np.full(3, 1.0, np.float32), 10)
    assert _round(gate)["provisional"] is True
    assert _round(gate)["confirmed"] is True


#: The incumbent's four games, replayed identically every time it is a leg.
INC = _step(2, 2)


def test_off_by_default_the_gate_decides_what_it_always_decided(fake):
    """Every run before the flag: a one-game gain takes the record, and no
    per-game rows are read at all."""
    gate = _gate(fake, [INC, INC, _step(3, 1), INC])
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    res = _round(gate)
    assert gate.paired_t == 0.0
    assert res["provisional"] is True and "paired_t" not in res


def test_a_one_game_gain_is_refused_when_the_pairing_is_asked_for(fake):
    """The same plan, the same 3-1 against a paired 2-2, under t >= 1.7. One
    extra game of four is t = 1.0 (`_signed`, above), and the record does not
    move."""
    gate = _gate(fake, [INC, INC, _step(3, 1), INC], paired_t=1.7)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    res = _round(gate)
    assert res["accepted"] is False and res.get("provisional") is None
    assert res["paired_n"] == 4
    assert res["paired_dwin"] == pytest.approx(0.25)
    assert res["paired_t"] == pytest.approx(1.0)
    # The theta the gate ships is still the one it started with.
    assert gate.record_gen == 10


def test_a_real_gain_still_takes_the_record(fake):
    """The threshold refuses noise, not gains: a candidate that turns two of
    the incumbent's four boards from losses into wins reads t = 1.73 on the
    first pair and t = 2.65 pooled over both, and is confirmed."""
    gate = _gate(fake, [INC, INC,
                        _step(4, 0), INC,       # the first pair
                        _step(4, 0), INC],      # the replicate's pair
                 paired_t=1.7)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    first = _round(gate)
    assert first["provisional"] is True
    assert first["paired_n"] == 4
    assert first["paired_t"] == pytest.approx(3 ** 0.5)  # 1.73 > 1.7
    conf = _round(gate)
    assert conf["paired_n"] == 8                # both bases, one test
    assert conf["paired_t"] == pytest.approx(2.6458, rel=1e-3)
    assert conf["confirmed"] is True and gate.record_gen == 20


def test_the_confirmation_runs_the_test_over_both_bases(fake):
    """A candidate whose second pair gives the gain back does not keep the
    record, even though its first pair cleared the threshold: the confirmation
    pools the two bases and tests them as one set of games."""
    gate = _gate(fake, [INC, INC,
                        _step(4, 0), INC,       # +2 of 4 on the first base
                        _step(0, 4), INC],      # -2 of 4 on the second
                 paired_t=0.9)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    assert _round(gate)["provisional"] is True
    conf = _round(gate)
    assert conf.get("confirmed") is not True
    assert conf["paired_n"] == 8                # both bases, one test
    assert gate.record_gen == 10                # reverted to the incumbent


def test_a_round_with_nothing_to_pair_is_refused_not_waved_through(fake):
    """A gate asked for a significance test and unable to run one has not
    measured an improvement. Here the incumbent's leg is served from the base
    cache, so the round has a paired *reading* but no paired *rows*."""
    gate = _gate(fake, [INC, INC, _step(4, 0)], paired_t=1.7)
    _baseline(gate)
    gate.base_seq -= 2                          # a base the incumbent has played
    gate.propose(np.full(3, 2.0, np.float32), 20)
    res = _round(gate)
    assert res["paired_win"] == 0.5             # the cached reading is there
    assert res["paired_t"] is None              # the rows are not
    assert res["accepted"] is False


def test_a_negative_threshold_is_refused(fake):
    with pytest.raises(ValueError):
        fake.gate([], paired_t=-1.0)


def test_the_threshold_round_trips_through_the_saved_state(fake):
    """A threshold, like `min_gain`: written so a resume can say it changed,
    owned by the command line rather than restored."""
    gate = _gate(fake, [], paired_t=1.7)
    assert gate.state()["paired_t"] == 1.7
    assert RealGate.paired_t_of(gate.state()) == 1.7
    assert RealGate.paired_t_of({}) == 0.0      # a state from before the flag


# ---------------------------------------------------------- the command line

def _args(**kw):
    """The `setup_real_gate` argv namespace, defaulted off."""
    from types import SimpleNamespace
    base = dict(real_gate=False, real_gate_every=0, real_gate_replicate=False,
                real_gate_reset=False, real_gate_fresh=False,
                real_gate_recentre=0, real_gate_min_gain=0.0,
                real_gate_win_floor=None, real_gate_paired_t=0.0,
                real_gate_seed_per_opponent=False, keep_candidates=False,
                real_gate_opponent=os.path.join(ROOT, "scripts", "train.py"),
                real_gate_games=2, real_gate_workers=1,
                real_gate_seed_base=1, real_gate_metric="win", seed=0)
    base.update(kw)
    return SimpleNamespace(**base)


def test_the_flag_needs_the_gate_it_is_a_rule_for(tmp_path):
    import train as T
    with pytest.raises(SystemExit, match="--real-gate-paired-t requires "
                                         "--real-gate:"):
        T.setup_real_gate(_args(real_gate_paired_t=1.7), None, str(tmp_path))


def test_the_flag_needs_the_pairing_it_tests(tmp_path):
    """An unpaired round plays the incumbent on no board of the candidate's,
    so there is nothing to difference and the threshold would be a refusal
    machine. The command line says so instead of running one."""
    import train as T
    with pytest.raises(SystemExit, match="requires --real-gate-fresh"):
        T.setup_real_gate(_args(real_gate=True, real_gate_paired_t=1.7),
                          None, str(tmp_path))


# ------------------------------------------------- the confirmation (flow112)

#: Twelve games a leg, so a round has room for a gain that is not one game.
BAR = _step(6, 6)


def test_the_replicate_round_plays_both_thetas_on_its_own_base(fake):
    """flow112's defect: the replicate re-played only the CANDIDATE, so the
    confirmation pooled its two bases against the incumbent's earlier,
    different ones. A promotion is now four evals -- candidate and incumbent
    on each of two bases -- and the second pair is on the replicate's base."""
    gate = _gate(fake, [BAR, BAR,
                        _step(9, 3), BAR,
                        _step(9, 3), BAR], paired_t=1.7)
    _baseline(gate)
    n0 = len(fake.calls())
    gate.propose(np.full(3, 2.0, np.float32), 20)
    _round(gate)                                    # provisional
    _round(gate)                                    # replicate
    legs = fake.calls()[n0:]
    assert len(legs) == 4                           # cand, inc, cand, inc
    assert [c["theta"][0] for c in legs] == [2.0, 1.0, 2.0, 1.0]
    b = _bases(fake)[n0:]
    assert b[0] == b[1] and b[2] == b[3] and b[0] != b[2]


def test_a_lucky_provisional_round_is_undone_by_the_paired_replicate(fake):
    """The candidate sweeps six of the bar's twelve boards on the first base
    (t = 3.3) and loses six on the second. Pooled over both, the paired
    difference is exactly zero -- so it is not a record, and the theta the
    gate ships is the one it started with."""
    gate = _gate(fake, [BAR, BAR,
                        _step(12, 0), BAR,          # +6 of 12: t = 3.3
                        _step(0, 12), BAR],         # -6 of 12
                 paired_t=1.7)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    first = _round(gate)
    assert first["provisional"] is True
    assert first["paired_t"] == pytest.approx(3.3166, rel=1e-3)

    conf = _round(gate)
    assert conf.get("confirmed") is not True
    assert conf["paired_rounds"] == 2
    assert conf["paired_n"] == 24                   # both rounds, one test
    assert conf["paired_dwin"] == pytest.approx(0.0)
    assert conf["paired_t"] == pytest.approx(0.0)
    assert gate.record_gen == 10                    # reverted to the baseline


def test_two_rounds_that_agree_confirm_the_record(fake):
    """The same gain on both bases: t = 1.92 on the first round and 2.77
    pooled, with a positive paired win difference. That is a record."""
    gate = _gate(fake, [BAR, BAR,
                        _step(9, 3), BAR,           # +3 of 12 on each base
                        _step(9, 3), BAR],
                 paired_t=1.7)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    assert _round(gate)["paired_t"] == pytest.approx(1.9150, rel=1e-3)
    conf = _round(gate)
    assert conf["paired_rounds"] == 2
    assert conf["paired_n"] == 24
    assert conf["paired_dwin"] == pytest.approx(0.25)
    assert conf["paired_t"] == pytest.approx(2.7699, rel=1e-3)
    assert conf["confirmed"] is True and gate.record_gen == 20


def test_a_margin_bought_with_the_head_to_head_bit_is_still_refused(fake):
    """`--real-gate-metric margin` tests the t on coins, so a candidate can
    clear it while losing games. The pooled paired WIN difference is a floor
    on the confirmation whatever the metric ranks on."""
    gate = _gate(fake, [BAR, BAR,
                        # 4 huge wins, 8 narrow losses: coins up, games down
                        _step(4, 8, 90_000.0, 1_000.0), BAR,
                        _step(4, 8, 90_000.0, 1_000.0), BAR],
                 paired_t=1.0, metric="margin")
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    assert _round(gate).get("provisional") is True
    conf = _round(gate)
    assert conf["paired_dmargin"] > 0               # the coins are there
    assert conf["paired_dwin"] < 0                  # the games are not
    assert conf.get("confirmed") is not True
    assert gate.record_gen == 10


def test_an_unpaired_replicate_can_no_longer_confirm(fake):
    """A bar whose theta is unknown (a resumed record file that is gone) has
    no leg to play, so the confirmation has nothing to pair with. It reverts
    instead of pooling the candidate's two bases against the bar's other
    ones -- which is the comparison that promoted flow112's gen 10."""
    gate = _gate(fake, [BAR, BAR, _step(12, 0), BAR, _step(12, 0)],
                 paired_t=1.7)
    _baseline(gate)
    gate.propose(np.full(3, 2.0, np.float32), 20)
    assert _round(gate)["provisional"] is True
    gate.prev_incumbent["theta"] = None             # the bar's theta is lost
    conf = _round(gate)
    assert conf["paired_t"] is None
    assert conf.get("confirmed") is not True
    assert gate.record_gen == 10


# --------------------------------------------- --real-gate-replicate-games

def test_the_replicate_round_may_be_played_on_more_games(fake):
    """The confirmation is the reading that decides, so it is the one worth
    spending on -- and BOTH its legs play the larger count, or the round is
    not a pair."""
    gate = _gate(fake, [BAR, BAR, _step(9, 3), BAR, _step(9, 3), BAR],
                 paired_t=1.7, games=2, replicate_games=7)
    assert gate.replicate_games == 7
    _baseline(gate)
    n0 = len(fake.calls())
    gate.propose(np.full(3, 2.0, np.float32), 20)
    _round(gate); _round(gate)
    got = [int(c["argv"][c["argv"].index("--games") + 1])
           for c in fake.calls()[n0:]]
    assert got == [2, 2, 7, 7]                      # screen small, confirm big


def test_the_replicate_count_defaults_to_the_gate_s_own(fake):
    gate = fake.gate([], games=5)
    assert gate.replicate_games == 5
    assert gate.state()["replicate_games"] == 5
    with pytest.raises(ValueError):
        fake.gate([], replicate_games=0)
