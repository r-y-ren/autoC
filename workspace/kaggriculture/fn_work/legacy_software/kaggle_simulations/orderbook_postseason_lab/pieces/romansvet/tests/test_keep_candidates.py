"""`--keep-candidates`: the thetas the real gate judged, kept with their verdicts.

The gate reuses one candidate file (`real_gate_cand.npy`), so a finished run
holds the *numbers* of every theta it refused (`log.jsonl`) and the weights of
none of them. The flag keeps a copy of each nomination beside an
`index.jsonl` of verdicts, and -- because it is opt-in and a training run is
expensive to perturb -- must be invisible when it is off.

Every eval here is `tests/test_real_gate.py`'s fake `eval_vs_baselines.py`:
CSV numbers dictated by a plan file, no engine, no real games.
"""
from __future__ import annotations

import json
import os
import sys
from types import SimpleNamespace

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import numpy as np
import pytest
import train as T
from test_real_gate import _expect, _Fake, _settle

from kagg3.es.train import CandidateKeeper

THETA_A = np.array([1.0, 2.0, 3.0], np.float32)
THETA_B = np.array([4.0, 5.0, 6.0], np.float32)

#: A clean 2-0 win, and a clean 0-2 loss, in the fake eval's plan language.
WON = {"wins": 2, "losses": 0, "win_margin": 1000.0, "loss_margin": 0.0}
LOST = {"wins": 0, "losses": 2, "win_margin": 0.0, "loss_margin": 1000.0}


@pytest.fixture
def fake(tmp_path):
    return _Fake(tmp_path)


def _index(run):
    p = os.path.join(run, "cands", "index.jsonl")
    if not os.path.isfile(p):
        return []
    with open(p) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def _md5(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def test_off_the_gate_writes_what_it_always_wrote(fake):
    """The default. No keeper, no directory, no line -- a gated run without
    the flag has to be the run that came before the flag existed."""
    g = fake.gate([WON])
    assert g.keeper is None
    g.propose(THETA_A, 7)
    assert _settle(g)["accepted"]
    assert not os.path.exists(os.path.join(fake.run, "cands"))
    g.close()


def test_every_nomination_is_kept_before_its_eval_and_indexed_after(fake):
    """A record and a periodic candidate, one accepted and one refused: both
    thetas on disk *before* the eval that judges them, both still there
    afterwards, and one index line each carrying the numbers the verdict was
    made of."""
    g = fake.gate([WON, LOST])
    g.keeper = CandidateKeeper(fake.run)

    g.propose(THETA_A, 10)                      # an in-sim record nominating
    kept = os.path.join(fake.run, "cands", "g00010_record.npy")
    # Written by `propose`, so it exists while the eval is still running.
    assert np.array_equal(np.load(kept), THETA_A)
    assert _settle(g)["accepted"]

    g.propose(THETA_B, 20, source="periodic")   # the --real-gate-every cadence
    kept_b = os.path.join(fake.run, "cands", "g00020_periodic.npy")
    assert np.array_equal(np.load(kept_b), THETA_B)
    assert not _settle(g)["accepted"]

    rows = _index(fake.run)
    assert [(r["gen"], r["kind"], r["verdict"]) for r in rows] == [
        (10, "record", "accepted"), (20, "periodic", "rejected")]
    assert [r["file"] for r in rows] == ["g00010_record.npy", "g00020_periodic.npy"]
    assert [r["md5"] for r in rows] == [_md5(kept), _md5(kept_b)]
    won_w, won_m = _expect(WON)
    lost_w, lost_m = _expect(LOST)
    assert (rows[0]["win"], rows[0]["margin"]) == (won_w, won_m)
    assert (rows[1]["win"], rows[1]["margin"]) == (lost_w, lost_m)
    # Nothing was measured when the first one was judged, so it had no bar;
    # the second was judged against the first, with `--real-gate-min-gain 0`.
    assert rows[0]["bar"] is None and rows[0]["bar_win"] is None
    assert (rows[1]["bar_win"], rows[1]["bar"]) == (won_w, won_w)
    assert rows[1]["metric"] == "win" and rows[1]["min_gain"] == 0.0
    # Kept, not moved: the accepted theta is still on disk after its verdict.
    assert np.array_equal(np.load(kept), THETA_A)
    g.close()


def test_a_replicate_verdict_lands_on_its_own_candidates_line(fake):
    """`--real-gate-replicate` judges a theta twice, and the second reading is
    a verdict on the *first* one's file: no second copy is kept, and the
    confirm/revert line points back at the nomination's md5."""
    better = dict(WON, win_margin=2000.0)
    g = fake.gate([WON, WON, better, LOST], replicate=True)
    g.keeper = CandidateKeeper(fake.run)

    g.propose(THETA_A, 10)
    assert _settle(g).get("provisional")         # the candidate's own reading
    assert _settle(g)["accepted"]                # its replicate confirms it
    g.propose(THETA_B, 20)
    assert _settle(g).get("provisional")
    assert _settle(g).get("reverted")            # this one's replicate does not

    rows = _index(fake.run)
    assert [(r["gen"], r["source"], r["verdict"]) for r in rows] == [
        (10, "record", "provisional"), (10, "replicate", "replicate-confirmed"),
        (20, "record", "provisional"), (20, "replicate", "replicate-failed")]
    kept = os.path.join(fake.run, "cands", "g00010_record.npy")
    assert [r["file"] for r in rows[:2]] == ["g00010_record.npy"] * 2
    assert [r["md5"] for r in rows[:2]] == [_md5(kept)] * 2
    assert sorted(os.listdir(os.path.join(fake.run, "cands"))) == [
        "g00010_record.npy", "g00020_record.npy", "index.jsonl"]
    g.close()


def test_the_flag_needs_the_gate(tmp_path):
    """Like every other `--real-gate-*` knob: on its own it would silently do
    nothing, so it is refused rather than ignored."""
    args = SimpleNamespace(real_gate=None, keep_candidates=True)
    with pytest.raises(SystemExit, match="--keep-candidates requires --real-gate"):
        T.setup_real_gate(args, None, str(tmp_path))
    # And without it the same call is the no-op it has always been.
    assert T.setup_real_gate(SimpleNamespace(real_gate=None), None,
                             str(tmp_path)) is None
