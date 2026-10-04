"""The tracker row's arithmetic: what `scripts/remote_eval_kagg2.sh` used to do
in awk and now does in `scripts/kagg2_track_row.py`.

Pure stdlib and no engine: the point of moving the summary out of awk was that
its two intervals could then be checked against numbers computed by hand, and a
test that had to boot `kaggle_environments` would not be run.
"""
from __future__ import annotations

import ast
import csv
import math
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Appended, not prepended, for the reason `eval_vs_baselines.py` gives: a
# scripts/ directory at sys.path[0] shadows anything in the stdlib that shares
# a name with a file in it.
sys.path.append(os.path.join(ROOT, "scripts"))

import kagg2_track_row as K

#: The `--csv` columns `eval_vs_baselines.py` writes. The replay half
#: (`moves`..`quads`) is here on purpose: the summary must ignore it.
CSV_HEADER = ("seed", "opponent", "seat", "mine", "theirs",
              "moves", "move_turns", "noops", "unsold", "quads")

KAGG2 = "../kaggriculture2/main.py"


def _write_csv(path, rows):
    """`rows` as `(seed, opponent, seat, mine, theirs)`; the replay columns get
    filler, so a reader that mistook one of them for `mine` would be caught."""
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_HEADER)
        for seed, opp, seat, mine, theirs in rows:
            w.writerow([seed, opp, seat, mine, theirs, 111, 22, 3, 4, 5])
    return path


def _seated(per_seed):
    """`read_games`-shaped rows -- `(seed, seat, mine, theirs)` -- with both
    seats of every seed: `per_seed[i] = ((m0, t0), (m1, t1))`."""
    out = []
    for i, (a, b) in enumerate(per_seed):
        out += [(1000 + i, 0, a[0], a[1]), (1000 + i, 1, b[0], b[1])]
    return out


# --------------------------------------------------------------------------
# the CSV contract


def test_the_columns_read_are_the_columns_the_eval_script_writes():
    """Read out of the source text rather than by importing it: importing
    `eval_vs_baselines` pulls in numpy and `kagg3.spec`, and this test is meant
    to stay a millisecond."""
    with open(os.path.join(ROOT, "scripts", "eval_vs_baselines.py")) as fh:
        tree = ast.parse(fh.read())
    header = next(ast.literal_eval(n.value) for n in ast.walk(tree)
                  if isinstance(n, ast.Assign)
                  and getattr(n.targets[0], "id", None) == "CSV_HEADER")
    assert header == CSV_HEADER
    assert set(header[:5]) >= {"seed", "opponent", "seat", "mine", "theirs"}


def test_rows_are_grouped_by_opponent_and_the_replay_columns_are_ignored(tmp_path):
    path = _write_csv(tmp_path / "g.csv",
                      [(7, "starter", 0, 90000, 10000),
                       (7, KAGG2, 0, 60000, 110000),
                       (7, KAGG2, 1, 61000, 111000)])
    by_opp = K.read_games(path)
    assert sorted(by_opp) == sorted(["starter", KAGG2])
    assert by_opp["starter"] == [(7, 0, 90000.0, 10000.0)]
    assert len(by_opp[KAGG2]) == 2


# --------------------------------------------------------------------------
# win rate and its Wilson interval


def test_a_tie_counts_a_half_win():
    assert K.win_score([(1, 0, 5, 4), (1, 1, 5, 5), (2, 0, 4, 5)]) == 1.5


@pytest.mark.parametrize("wins,n,lo,hi", [
    # The plan's §3.5 quotes these to stop anyone over-reading the win column.
    (0, 48, 0.0, 7.4),
    (8, 16, 28.0, 72.0),
    (24, 48, 36.4, 63.6),
])
def test_wilson_matches_the_quoted_intervals(wins, n, lo, hi):
    got_lo, got_hi = K.wilson(wins, n)
    assert round(100 * got_lo, 1) == lo
    assert round(100 * got_hi, 1) == hi


def test_wilson_brackets_the_point_estimate_including_half_wins():
    for wins, n in ((0, 48), (0.5, 48), (17.5, 48), (48, 48)):
        lo, hi = K.wilson(wins, n)
        assert lo <= wins / n <= hi
    assert K.wilson(0, 48)[0] == 0.0            # clamped, never negative
    assert K.wilson(48, 48)[1] == 1.0


# --------------------------------------------------------------------------
# the paired margin interval


def test_the_paired_mean_is_the_game_mean_when_both_seats_are_present():
    mean, _, n = K.paired_margin(
        [(1, 0, 100, 60), (1, 1, 80, 90), (2, 0, 50, 70), (2, 1, 30, 10)])
    assert n == 2                                # seeds, not games
    assert mean == pytest.approx((40 - 10 - 20 + 20) / 4)


def test_pairing_removes_a_seat_effect_the_pooled_interval_would_charge_for():
    """Both seats of a seed share the episode's randomness, so a large, purely
    positional spread is not evidence about the margin. Seat 0 wins by 30 and
    seat 1 loses by 10 in every seed: the per-seed margin is +10 with no spread
    at all, and the interval must be ~0 rather than the ~14 a pooled sd over
    8 'independent' games would report."""
    mean, half, n = K.paired_margin(_seated([((130, 100), (90, 100))] * 4))
    assert n == 4
    assert mean == pytest.approx(10.0)
    assert half == pytest.approx(0.0, abs=1e-9)


def test_the_half_width_is_z_times_the_standard_error_over_seeds():
    per_seed = [10.0, 20.0, 30.0, 60.0]          # mean 30, sd 22.11
    mean, half, n = K.paired_margin(
        _seated([((m, 0.0), (m, 0.0)) for m in per_seed]))
    sd = (sum((d - 30.0) ** 2 for d in per_seed) / 3) ** 0.5
    assert (mean, n) == (pytest.approx(30.0), 4)
    assert half == pytest.approx(1.96 * sd / 2)  # sqrt(4) = 2


def test_one_seed_has_no_interval_rather_than_a_zero_one():
    mean, half, n = K.paired_margin([(1, 0, 100.0, 40.0), (1, 1, 80.0, 40.0)])
    assert (mean, n) == (pytest.approx(50.0), 1)
    assert math.isnan(half)                      # NaN, not a false 0


# --------------------------------------------------------------------------
# the row


def _summary(tmp_path):
    """Two seeds x two seats against each of the two opponents, with a tie in
    one kagg2 game so the half-win rule shows up in the row."""
    rows = [(11, "starter", 0, 120000, 9000), (11, "starter", 1, 110000, 9000),
            (12, "starter", 0, 100000, 9000), (12, "starter", 1, 90000, 9000),
            (11, KAGG2, 0, 60000, 110000), (11, KAGG2, 1, 70000, 100000),
            (12, KAGG2, 0, 50000, 50000), (12, KAGG2, 1, 40000, 120000)]
    path = _write_csv(tmp_path / "g.csv", rows)
    return K.summarise(K.read_games(path), KAGG2)


def test_the_row_separates_the_two_opponents(tmp_path):
    s = _summary(tmp_path)
    assert s["n_games"] == 4                          # kagg2 games only
    assert s["coins_vs_starter"] == pytest.approx(105000.0)
    assert s["coins_vs_kagg2"] == pytest.approx(55000.0)
    assert s["kagg2_coins"] == pytest.approx(95000.0)
    assert s["margin_vs_kagg2"] == pytest.approx(-40000.0)


def test_joint_coins_is_both_farms_and_the_win_rate_counts_the_tie_half(tmp_path):
    s = _summary(tmp_path)
    assert s["joint_coins"] == pytest.approx(s["coins_vs_kagg2"] + s["kagg2_coins"])
    assert s["joint_coins"] == pytest.approx(150000.0)
    assert s["win_pct_vs_kagg2"] == pytest.approx(100 * 0.5 / 4)   # one tie, no win
    assert s["win_lo"] <= s["win_pct_vs_kagg2"] <= s["win_hi"]


def test_a_missing_opponent_is_an_error_not_a_zero(tmp_path):
    path = _write_csv(tmp_path / "g.csv", [(11, "starter", 0, 1, 2)])
    with pytest.raises(SystemExit) as e:
        K.summarise(K.read_games(path), KAGG2)
    assert KAGG2 in str(e.value)


def test_the_first_nine_columns_are_the_old_row_unchanged(tmp_path):
    """Back-compatibility is the whole reason the new columns are appended: a
    reader that splits on tabs and takes fields 1-9 sees exactly what the awk
    summary produced, and the four new fields ride after."""
    assert K.COLUMNS[:9] == ("ts", "run", "gen", "n_games", "coins_vs_starter",
                             "coins_vs_kagg2", "margin_vs_kagg2",
                             "win_pct_vs_kagg2", "kagg2_coins")
    assert K.COLUMNS[9:] == ("margin_ci95", "win_lo", "win_hi", "joint_coins")
    fields = _summary(tmp_path)
    fields.update(ts="2026-08-26T12:00:00+00:00", run="p2s0", gen="7830")
    cells = K.format_row(fields).split("\t")
    assert len(cells) == len(K.COLUMNS)
    assert cells[:9] == ["2026-08-26T12:00:00+00:00", "p2s0", "7830", "4",
                         "105000", "55000", "-40000", "12.5", "95000"]
    assert cells[12] == "150000"                 # joint_coins


# --------------------------------------------------------------------------
# the header comment


def test_a_new_track_file_gets_one_commented_header(tmp_path):
    track = str(tmp_path / "kagg2_track.tsv")
    K.ensure_header(track)
    K.ensure_header(track)
    with open(track) as fh:
        lines = fh.read().splitlines()
    assert lines == [K.header_line()]
    assert lines[0].startswith("# ts\trun\t")


def test_a_legacy_file_keeps_its_rows_and_gains_the_comment_once(tmp_path):
    """The old script wrote a bare 9-column header. Those rows really do have
    nine columns, so the header they were written under is left in place and
    the comment marks where the format widened."""
    track = tmp_path / "kagg2_track.tsv"
    legacy = ("ts\trun\tgen\tn_games\tcoins_vs_starter\tcoins_vs_kagg2\t"
              "margin_vs_kagg2\twin_pct_vs_kagg2\tkagg2_coins")
    track.write_text(legacy + "\n2026-08-25T00:00:00+00:00\tp2s0\t7000\t16\t"
                     "116000\t62000\t-49000\t0.0\t111000\n")
    K.ensure_header(str(track))
    K.ensure_header(str(track))
    lines = track.read_text().splitlines()
    assert lines[0] == legacy                    # untouched
    assert lines[1].startswith("2026-08-25")     # untouched
    assert lines[2] == K.header_line()
    assert sum(1 for line in lines if line.startswith("#")) == 1
