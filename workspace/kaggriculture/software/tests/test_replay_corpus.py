"""Tests for the m1 replay corpus: profile extractor + integrity validator.

Extractor tests use a synthetic 720-step fixture (deterministic, no network,
no dependence on gitignored raw replays). If real replays exist under
.tmp-corpus/raw, an additional fact-anchored test runs against the top-1
episode (hires 295 / feed 2305u / wheat 2553u verified by hand on 2026-08-29).

Integrity validator tests build a minimal corpus + exports fixture in a temp
dir and assert that official mode FAILs on: missing source provenance,
abnormal episodes entering the archive, missing band layers, manifest sha256
mismatch, premature "consistent" labels. dev mode must tolerate the relaxed
subset.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from kgenv.replay_profile import (
    IntegrityError,
    check_integrity,
    extract_episode_profiles,
    load_replay,
)

def _repo_root(start: Path) -> Path:
    cur = start.resolve()
    while cur != cur.parent:
        if (cur / ".git").exists():
            return cur
        cur = cur.parent
    return cur


REPO = _repo_root(Path(__file__))
SOFTWARE = REPO / "workspace" / "kaggriculture" / "software"
INTEGRITY_SCRIPT = (
    SOFTWARE / "scripts" / "corpus_integrity.py"
)
REAL_EPISODE = REPO / ".tmp-corpus" / "raw" / "episode-102201446-replay.json"

HOURS_PER_DAY = 24
DAYS = 30
STEPS = DAYS * HOURS_PER_DAY
Q = ["NW", "NE", "SW", "SE"]


# --------------------------------------------------------------------------- #
# fixture builders
# --------------------------------------------------------------------------- #
def _farm(money: float, tiles=None, quadrants=("NW",), hires=0):
    rows = tiles if tiles is not None else [[None] * 10 for _ in range(10)]
    return {
        "money": money,
        "tiles": rows,
        "unlocked_quadrants": list(quadrants),
        "hires_today": hires,
        "farmer": [0, 0],
        "hands": [],
    }


def _step(t: int, market0=(), market1=(), money=(3000.0, 3000.0), f0=None, f1=None):
    day, hour = divmod(t, HOURS_PER_DAY)
    obs_common = {
        "day": day,
        "hour": hour,
        "market": {
            "prices": {"WHEAT": 30, "MILK": 50},
            "inventory": {},
        },
        "town": {"unlocked_shops": []},
    }
    f0 = f0 or _farm(money[0])
    f1 = f1 or _farm(money[1])
    entries = []
    for pl, acts, farm, priv in (
        (0, market0, f0, {"shed": {}, "seeds": {}, "inventories": []}),
        (1, market1, f1, {"shed": {}, "seeds": {}, "inventories": []}),
    ):
        obs = dict(obs_common)
        obs["farms"] = [f0, f1]
        obs["player"] = pl
        obs["private"] = priv
        entries.append(
            {
                "action": {"farmer": [], "hands": [], "market": list(acts)},
                "observation": obs,
                "status": "DONE",
                "reward": 0,
                "info": {},
            }
        )
    return entries


def _mk_replay(
    statuses=("DONE", "DONE"),
    n_steps=STEPS,
    teams=("Alpha", "Beta"),
    rewards=(1000.0, 900.0),
    mutate=None,
):
    """Deterministic minimal replay; mutate(t, replay) hook for test cases."""
    steps = [_step(t) for t in range(n_steps)]
    replay = {
        "info": {"TeamNames": list(teams), "EpisodeId": 1, "seed": 42},
        "rewards": list(rewards),
        "statuses": list(statuses),
        "steps": steps,
    }
    if mutate:
        mutate(len(steps), replay)
    return replay


# --------------------------------------------------------------------------- #
# extractor: integrity gate
# --------------------------------------------------------------------------- #
def test_check_integrity_clean_fixture():
    assert check_integrity(_mk_replay()) == []


@pytest.mark.parametrize(
    "label,mutate",
    [
        ("status_error", lambda n, r: r["statuses"].__setitem__(1, "ERROR")),
        ("status_timeout", lambda n, r: r["statuses"].__setitem__(0, "TIMEOUT")),
        (
            "steps_short",
            lambda n, r: r.__setitem__("steps", r["steps"][: n - 1]),
        ),
        ("reward_none", lambda n, r: r["rewards"].__setitem__(0, None)),
        ("reward_nan", lambda n, r: r["rewards"].__setitem__(0, float("nan"))),
        (
            "teams_bad",
            lambda n, r: r["info"].__setitem__("TeamNames", ["Alpha", ""]),
        ),
        ("teams_missing", lambda n, r: r["info"].pop("TeamNames")),
    ],
)
def test_check_integrity_negatives(label, mutate):
    issues = check_integrity(_mk_replay(mutate=mutate))
    assert issues, f"expected integrity issues for {label}"


def test_extract_strict_raises_on_dirty():
    with pytest.raises(IntegrityError):
        extract_episode_profiles(
            _mk_replay(statuses=("DONE", "ERROR")), strict=True
        )


def test_extract_nonstrict_marks_issues():
    res = extract_episode_profiles(
        _mk_replay(statuses=("DONE", "ERROR")), strict=False
    )
    assert res["episode"]["integrity_issues"]


# --------------------------------------------------------------------------- #
# extractor: profile content
# --------------------------------------------------------------------------- #
def _rich_replay():
    """Fixture with a fuller game: sells, feed buys, hires, herd, quadrants."""

    def mutate(n, replay):
        steps = replay["steps"]
        # quadrant NE unlocks at day 5 (t=120) for seat 0
        for t in range(120, n):
            obs = steps[t][0]["observation"]
            obs["farms"][0]["unlocked_quadrants"] = ["NW", "NE"]
        # sheep pasture from day 1 (t=24) on seat 0
        sheep_tile = {
            "kind": "PASTURE",
            "animal": "SHEEP",
            "fed_today": True,
            "placed_day": 1,
        }
        wheat_tile = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "planted_day": 1,
            "yield_units": 1,
        }
        for t in range(24, n):
            obs = steps[t][0]["observation"]
            tiles = obs["farms"][0]["tiles"]
            tiles[0][0] = dict(sheep_tile)
            tiles[0][1] = dict(wheat_tile)
        # money ramps: +100/day seat0, flat seat1
        for t in range(n):
            obs = steps[t][0]["observation"]
            obs["farms"][0]["money"] = 3000.0 + 100 * (t // HOURS_PER_DAY)
        # hires: 2/day every day for seat 0
        for t in range(n):
            obs = steps[t][0]["observation"]
            obs["farms"][0]["hires_today"] = 2
        # actions: sell wheat mid-game (t=300, price 30, qty 10) and in the
        # endgame window (t=700, price 40, qty 5); buy feed wheat t=200 qty 7
        steps[200][0]["action"]["market"] = [["BUY_PRODUCT", "WHEAT", 7]]
        steps[300][0]["action"]["market"] = [["SELL", "WHEAT", 10]]
        steps[700][0]["action"]["market"] = [["SELL", "WHEAT", 5]]
        steps[700][0]["observation"]["market"]["prices"]["WHEAT"] = 40
        # seat 1 sells milk once endgame
        steps[680][1]["action"]["market"] = [["SELL", "MILK", 4]]
        # an escaped-animal empty pasture at end for seat 0 (no animal key)
        empty_pasture = {"kind": "PASTURE"}
        for t in range(600, n):
            obs = steps[t][0]["observation"]
            obs["farms"][0]["tiles"][1][0] = dict(empty_pasture)

    return _mk_replay(rewards=(6000.0, 3000.0), mutate=mutate)


def test_profile_money_and_endgame():
    res = extract_episode_profiles(_rich_replay())
    p0 = res["players"][0]
    assert p0["money"]["opening"] == 3000.0
    assert p0["money"]["final"] == 3000.0 + 100 * (719 // HOURS_PER_DAY)  # 5900
    # 30 day samples, one per day
    assert len(p0["money"]["curve_step_money"]) == 30
    # daily net +100 except day 0 (opening->day end)
    assert p0["money"]["net_cash_by_day"][1] == 100.0
    # endgame window opens at step 672; money at start = 3000+100*28 = 5800
    assert p0["endgame"]["money_at_start"] == 5800.0
    assert p0["endgame"]["gain"] == 100.0


def test_profile_sells_and_prices():
    res = extract_episode_profiles(_rich_replay())
    p0 = res["players"][0]
    wheat = p0["sells"]["per_item"]["WHEAT"]
    assert wheat["qty"] == 15
    assert wheat["orders"] == 2
    assert wheat["price_min"] == 30
    assert wheat["price_max"] == 40
    # quoted revenue: 10*30 + 5*40 = 500; endgame: 5*40 = 200
    assert wheat["quoted_revenue"] == 500
    assert p0["sells"]["total_quoted_revenue"] == 500
    assert p0["sells"]["endgame_quoted_revenue"] == 200
    assert p0["sells"]["endgame_revenue_share"] == pytest.approx(0.4)
    assert p0["sells"]["crop_quoted_revenue"] == 500
    assert p0["sells"]["animal_quoted_revenue"] == 0
    # seat 1 milk sell
    p1 = res["players"][1]
    assert p1["sells"]["per_item"]["MILK"]["qty"] == 4
    assert p1["sells"]["animal_quoted_revenue"] == 200


def test_profile_feed_and_hires():
    res = extract_episode_profiles(_rich_replay())
    p0 = res["players"][0]
    assert p0["external_buys"]["feed_qty"] == 7
    assert p0["external_buys"]["feed_avg_price"] == 30
    assert p0["hires"]["total"] == 60  # 2/day x 30 days
    assert p0["hires"]["avg_per_day"] == pytest.approx(2.0)
    assert p0["op_counts"].get("HIRE", 0) == 0  # hires_today is state, not market op


def test_profile_herd_crops_quadrants():
    res = extract_episode_profiles(_rich_replay())
    p0 = res["players"][0]
    assert p0["herd"]["final"] == {"SHEEP": 1, "EMPTY_STRUCTURE": 1}
    assert p0["herd"]["by_day"][0].get("SHEEP", 0) == 0
    share = p0["crops"]["tile_day_share"]
    assert share["WHEAT"] == 1.0  # only wheat ever planted
    assert p0["land"]["quadrant_unlock_day"] == {"NW": 0, "NE": 5}
    assert p0["land"]["quadrants_final"] == 2


def test_profile_won_and_meta():
    res = extract_episode_profiles(
        _rich_replay(),
        episode_id=99,
        source_url="https://example.test/ep/99",
        capture_date="2026-08-29",
    )
    assert res["episode"]["episode_id"] == 99
    assert res["episode"]["source_url"] == "https://example.test/ep/99"
    p0, p1 = res["players"]
    assert p0["won"] is True and p1["won"] is False
    assert p0["team"] == "Alpha" and p0["opponent"] == "Beta"


# --------------------------------------------------------------------------- #
# extractor vs real replay on disk (skipped when corpus absent)
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not REAL_EPISODE.exists(), reason="raw corpus not on disk")
def test_extractor_real_top1_episode_facts():
    """Anchors against hand-verified facts (2026-08-29): Crop Dusta seat 0."""
    res = extract_episode_profiles(
        load_replay(REAL_EPISODE),
        source_url="https://www.kaggle.com/competitions/kaggriculture/episodes/102201446",
        capture_date="2026-08-29",
    )
    p0 = res["players"][0]
    assert p0["team"] == "Crop Dusta"
    assert p0["hires"]["total"] == 295
    assert p0["external_buys"]["feed_qty"] == 2305
    assert p0["sells"]["per_item"]["WHEAT"]["qty"] == 2553
    assert p0["sells"]["per_item"]["CARROT"]["qty"] == 269
    assert p0["herd"]["animal_buys"] == {"SHEEP": 9, "COW": 3, "GOOSE": 2}
    assert p0["land"]["quadrants_final"] == 3
    assert p0["money"]["final"] == 74662.0


# --------------------------------------------------------------------------- #
# integrity validator (subprocess against tmp fixtures)
# --------------------------------------------------------------------------- #
def _write_min_corpus(root: Path, dirty=False, bands=("top20", "top100", "band_500_900")):
    """Create a minimal but valid corpus + exports; returns key paths."""
    corpus = root / "corpus"
    raw_dir = corpus / "raw"
    raw_dir.mkdir(parents=True)
    exports = root / "exports"
    (exports / "profiles").mkdir(parents=True)

    replay = _mk_replay()
    if dirty:
        replay["statuses"] = ["DONE", "ERROR"]
    raw_file = raw_dir / "episode-1001-replay.json"
    payload = json.dumps(replay)
    raw_file.write_text(payload)
    sha = hashlib.sha256(payload.encode()).hexdigest()

    teams = replay["info"]["TeamNames"]
    manifest = {
        "schema": "m1-replay-corpus-manifest/1.0",
        "capture_date": "2026-08-29",
        "files": [
            {
                "file": "raw/episode-1001-replay.json",
                "episode_id": 1001,
                "sha256": sha,
                "bytes": len(payload.encode()),
                "source_url": "https://example.test/shard/1001.json",
                "source_slug": "kaggle/kaggriculture-episodes-2026-08-28",
                "capture_date": "2026-08-29",
                "teams": teams,
                "team_ranks": [1, 2],
                "team_scores": [3000.0, 2900.0],
                "bands": list(bands),
            }
        ],
    }
    (corpus / "manifest.json").write_text(json.dumps(manifest, indent=1))

    prof0 = {
        "episode_id": 1001,
        "seat": 0,
        "team": teams[0],
        "source_url": "https://example.test/shard/1001.json",
        "capture_date": "2026-08-29",
        "integrity_issues": [],
        "exploratory": True,
        "money": {"final": 1000.0},
    }
    prof1 = dict(prof0, seat=1, team=teams[1], money={"final": 900.0})
    (exports / "profiles" / "ep1001_seat0.json").write_text(json.dumps(prof0))
    (exports / "profiles" / "ep1001_seat1.json").write_text(json.dumps(prof1))

    index = {
        "schema": "m1-replay-profile-index/1.0",
        "episodes": [
            {
                "episode_id": 1001,
                "teams": teams,
                "rewards": [1000.0, 900.0],
                "statuses": ["DONE", "DONE"],
                "steps": 720,
                "bands": list(bands),
                "source_url": "https://example.test/shard/1001.json",
                "capture_date": "2026-08-29",
                "raw_sha256": sha,
                "raw_bytes": len(payload.encode()),
            }
        ],
        "excluded": [],
    }
    (exports / "index.json").write_text(json.dumps(index, indent=1))
    (exports / "exclusions.json").write_text(
        json.dumps({"schema": "m1-exclusions/1.0", "excluded": []}, indent=1)
    )
    (exports / "band_summary.md").write_text(
        "# summary\n\n## Band: top20 (1 episodes, 2 teams)\n\n"
        "_no team reached 3 profiled games; all team-level conclusions stay "
        "exploratory._\n"
    )
    return corpus, exports, manifest


def _run_integrity(corpus: Path, exports: Path, mode="official"):
    proc = subprocess.run(
        [
            sys.executable,
            str(INTEGRITY_SCRIPT),
            "--mode",
            mode,
            "--corpus",
            str(corpus),
            "--exports",
            str(exports),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_integrity_passes_on_valid_corpus(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path)
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 0, out


def test_integrity_fails_on_sha_mismatch(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path)
    raw = corpus / "raw" / "episode-1001-replay.json"
    raw.write_text(raw.read_text() + " ")  # same json, different bytes
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 1 and "sha256 mismatch" in out


def test_integrity_fails_on_dirty_episode_in_archive(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path, dirty=True)
    # dirty episode must NOT pass official or dev
    for mode in ("official", "dev"):
        code, out = _run_integrity(corpus, exports, mode)
        assert code == 1, f"{mode} should fail: {out}"
    assert "statuses" in out


def test_integrity_fails_on_missing_source(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path)
    pf = exports / "profiles" / "ep1001_seat0.json"
    p = json.loads(pf.read_text())
    p.pop("source_url")
    pf.write_text(json.dumps(p))
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 1 and "source_url" in out
    # dev mode tolerates missing provenance
    code_dev, out_dev = _run_integrity(corpus, exports, "dev")
    assert code_dev == 0, out_dev


def test_integrity_fails_on_missing_band(tmp_path):
    corpus, exports, _ = _write_min_corpus(
        tmp_path, bands=("top20", "top100")
    )
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 1 and "band coverage missing: band_500_900" in out
    code_dev, _ = _run_integrity(corpus, exports, "dev")
    assert code_dev == 0


def test_integrity_fails_on_premature_consistent_label(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path)
    (exports / "band_summary.md").write_text(
        "# summary\n\n- **Alpha** (consistent, 1 games): fake\n"
    )
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 1 and "consistent" in out


def test_integrity_fails_on_raw_leak(tmp_path):
    corpus, exports, _ = _write_min_corpus(tmp_path)
    pf = exports / "profiles" / "ep1001_seat0.json"
    p = json.loads(pf.read_text())
    p["steps"] = [[[{"observation": {}}]]]
    pf.write_text(json.dumps(p))
    code, out = _run_integrity(corpus, exports, "official")
    assert code == 1 and "leaked" in out
