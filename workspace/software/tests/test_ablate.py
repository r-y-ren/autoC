"""Paired ablation harness tests (campaign III r3-P0).

Grid completeness, pairing semantics, merge-gate indicator computation
(including counterexamples), frozen-champion decode integrity, and a small
real-engine integration run (short episodes) that must produce identical
games for champion-vs-champion -- every pair a tie, verdict MERGEABLE.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

SOFTWARE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.eval_contract import ContractError  # noqa: E402


def _load_ablate():
    spec = importlib.util.spec_from_file_location(
        "ablate_module", os.path.join(SOFTWARE_ROOT, "scripts", "ablate.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ablate = _load_ablate()


# --------------------------------------------------------------------------- #
# grid completeness
# --------------------------------------------------------------------------- #
def test_build_grid_is_complete_cross_product():
    grid = ablate.build_ablation_grid(["cow_baron", "scale_ranch"], [101, 102])
    assert len(grid) == 8  # 2 opponents x 2 seeds x 2 seats
    keys = {(g["opponent"], g["seed"], g["seat"]) for g in grid}
    assert keys == {
        ("cow_baron", 101, "AB"), ("cow_baron", 101, "BA"),
        ("cow_baron", 102, "AB"), ("cow_baron", 102, "BA"),
        ("scale_ranch", 101, "AB"), ("scale_ranch", 101, "BA"),
        ("scale_ranch", 102, "AB"), ("scale_ranch", 102, "BA"),
    }


def _game(side, opponent, seed, seat, margin):
    return {"side": side, "opponent": opponent, "seed": seed, "seat": seat,
            "margin": margin,
            "outcome": "W" if margin > 0 else ("L" if margin < 0 else "T")}


def _full_grid_games(opponents, seeds, cand_margin, champ_margin=None):
    champ_margin = cand_margin if champ_margin is None else champ_margin
    games = []
    for opp in opponents:
        for seed in seeds:
            for seat in ("AB", "BA"):
                games.append(_game("cand", opp, seed, seat, cand_margin))
                games.append(_game("champion", opp, seed, seat, champ_margin))
    return games


def test_validate_grid_rejects_missing_duplicate_and_foreign_games():
    opponents, seeds = ["cow_baron"], [101]
    games = _full_grid_games(opponents, seeds, 100.0)
    ablate.validate_grid_completeness(games, opponents, seeds)  # passes

    missing = [g for g in games if not (g["side"] == "champion"
                                        and g["seat"] == "BA")]
    with pytest.raises(ContractError):
        ablate.validate_grid_completeness(missing, opponents, seeds)

    duplicate = games + [_game("cand", "cow_baron", 101, "AB", 5.0)]
    with pytest.raises(ContractError):
        ablate.validate_grid_completeness(duplicate, opponents, seeds)

    foreign = games + [_game("cand", "melon_hoarder", 101, "AB", 5.0)]
    with pytest.raises(ContractError):
        ablate.validate_grid_completeness(foreign, opponents, seeds)


# --------------------------------------------------------------------------- #
# pairing semantics
# --------------------------------------------------------------------------- #
def test_pair_cells_diffs_margins_per_cell():
    games = [
        _game("cand", "cow_baron", 101, "AB", 12000.0),
        _game("champion", "cow_baron", 101, "AB", 9000.0),   # +3000 -> W
        _game("cand", "cow_baron", 101, "BA", -2000.0),
        _game("champion", "cow_baron", 101, "BA", 1000.0),   # -3000 -> L
        _game("cand", "scale_ranch", 102, "AB", 500.0),
        _game("champion", "scale_ranch", 102, "AB", 500.0),  # 0 -> T
    ]
    pairs = ablate.pair_cells(games)
    by_key = {(p["opponent"], p["seed"], p["seat"]): p for p in pairs}
    assert by_key[("cow_baron", 101, "AB")]["pair_diff"] == 3000.0
    assert by_key[("cow_baron", 101, "AB")]["outcome"] == "W"
    assert by_key[("cow_baron", 101, "BA")]["pair_diff"] == -3000.0
    assert by_key[("cow_baron", 101, "BA")]["outcome"] == "L"
    assert by_key[("scale_ranch", 102, "AB")]["outcome"] == "T"


# --------------------------------------------------------------------------- #
# merge gate indicators (with counterexamples)
# --------------------------------------------------------------------------- #
OPPS4 = ["crop_rotator", "template_wheat", "self_feed_ranch", "scale_ranch"]


def test_gate_metrics_pool_worst_and_disaster():
    # candidate: 3 style wins + 1 style loss + 1 gate-bot loss by disaster
    games = [
        _game("cand", "crop_rotator", 101, "AB", 1000),
        _game("cand", "crop_rotator", 101, "BA", 1000),
        _game("cand", "template_wheat", 101, "AB", 1000),
        _game("cand", "template_wheat", 101, "BA", -500),
        _game("cand", "self_feed_ranch", 101, "AB", 1000),
        _game("cand", "self_feed_ranch", 101, "BA", 1000),
        _game("cand", "scale_ranch", 101, "AB", -400),
        _game("cand", "scale_ranch", 101, "BA", 1000),
        _game("cand", "cow_baron", 101, "AB", -20000),  # disaster loss
        _game("cand", "cow_baron", 101, "BA", 20000),
    ]
    gate = ablate.side_gate_metrics(games, "cand", OPPS4 + ["cow_baron"])
    # style pool: 6W-2L over 8 -> 0.75
    assert gate["new_style_pool_win_rate"] == 0.75
    assert gate["new_style_pool_games"] == 8
    # worst per-opponent: template_wheat / scale_ranch both 0.5
    assert gate["worst_opponent_win_rate"] == 0.5
    assert gate["worst_opponent"] in ("template_wheat", "scale_ranch")
    # disasters: 1 of 10 games below -15000
    assert gate["disaster_rate"] == 0.1
    assert gate["record"] == {"W": 7, "L": 3, "T": 0}


def test_disaster_boundary_is_strictly_below_margin():
    games = [_game("cand", "crop_rotator", 101, "AB", -15000.0),
             _game("cand", "crop_rotator", 101, "BA", -15000.1)]
    gate = ablate.side_gate_metrics(games, "cand", ["crop_rotator"])
    # exactly -15000 is a plain loss, not a disaster; -15000.1 is
    assert gate["disaster_games"] == 1
    assert gate["disaster_rate"] == 0.5


def test_merge_verdict_counterexamples():
    def gate(pool, worst, disaster):
        return {"new_style_pool_win_rate": pool,
                "worst_opponent_win_rate": worst,
                "disaster_rate": disaster}

    # all three hold -> mergeable
    v = ablate.merge_verdict(gate(0.8, 0.6, 0.05), gate(0.8, 0.6, 0.05))
    assert v["mergeable"] is True
    # better pool but worse worst opponent -> NOT mergeable
    v = ablate.merge_verdict(gate(0.9, 0.5, 0.0), gate(0.8, 0.6, 0.0))
    assert v["mergeable"] is False
    assert v["checks"]["worst_opponent_win_rate"] is False
    assert v["checks"]["new_style_pool_win_rate"] is True
    # equal pool/worst but higher disaster rate -> NOT mergeable
    v = ablate.merge_verdict(gate(0.9, 0.6, 0.1), gate(0.9, 0.6, 0.05))
    assert v["mergeable"] is False
    assert v["checks"]["disaster_rate"] is False
    # ties everywhere (champion vs champion) -> mergeable
    v = ablate.merge_verdict(gate(0.5, 0.5, 0.0), gate(0.5, 0.5, 0.0))
    assert v["mergeable"] is True


# --------------------------------------------------------------------------- #
# champion decode integrity
# --------------------------------------------------------------------------- #
def test_decode_frozen_champion_sha_matches_manifest():
    path, sha = ablate.decode_frozen_champion()
    try:
        manifest = json.load(open(ablate.FROZEN_MANIFEST, encoding="utf-8"))
        assert sha == manifest["frozen_snapshot"]["decoded_sha256"]
        assert os.path.isfile(path)
        head = open(path, "rb").read(64)
        assert b"Kaggriculture submission agent" in head
    finally:
        os.unlink(path)


def test_decode_frozen_champion_rejects_tampered_snapshot(tmp_path):
    import base64
    raw = open(ablate.FROZEN_SNAPSHOT, "rb").read()
    data = bytearray(base64.b64decode(raw))
    data[len(data) // 2] ^= 0x01  # flip one decoded byte
    tampered = tmp_path / "tampered.b64"
    tampered.write_bytes(base64.b64encode(bytes(data)))
    with pytest.raises(ContractError):
        ablate.decode_frozen_champion(str(tampered))


def test_parse_seeds_and_pool_validation():
    assert ablate.parse_seeds("101-104") == [101, 102, 103, 104]
    assert ablate.parse_seeds("201,203") == [201, 203]
    with pytest.raises(ContractError):
        ablate.parse_seeds("101-999")     # outside both seed domains
    with pytest.raises(ContractError):
        ablate.parse_seeds("101,101")     # duplicates
    pool, formal = ablate.parse_pool("required")
    # v7: wheat_straw_monster joined the ablation required pool (guard
    # opponent, outside the five new-style members) -- 10 opponents now
    assert formal is True and len(pool) == 10
    pool, formal = ablate.parse_pool("cow_baron,scale_ranch")
    assert formal is False and pool == ["cow_baron", "scale_ranch"]
    with pytest.raises(ContractError):
        ablate.parse_pool("cow_baron,not_a_bot")


def test_out_path_locked_to_ablations_dir():
    base = Path(ablate.ABLATIONS_DIR).resolve()
    ok = ablate.resolve_out_path("", "r4-layer1")
    assert ok == base / "r4-layer1.json"
    ok = ablate.resolve_out_path("my-run.json", "x")
    assert ok == base / "my-run.json"
    with pytest.raises(ContractError):
        ablate.resolve_out_path(str(base.parent / "eval_results.json"), "x")
    with pytest.raises(ContractError):
        ablate.resolve_out_path("C:/windows/temp/evil.json", "x")


# --------------------------------------------------------------------------- #
# real-engine integration: champion vs champion must tie every cell
# --------------------------------------------------------------------------- #
def test_champion_vs_champion_short_grid_all_ties():
    """Same bytes on both sides -> identical games -> all pairs tie ->
    MERGEABLE (the harness's semantic self-check)."""
    champ_path, champ_sha, _label = ablate.resolve_champion("frozen")
    try:
        agent = ablate.load_submission_agent(champ_path)
        games = ablate.run_ablation(agent, agent,
                                    {"scale_ranch": ablate.OPPONENTS["scale_ranch"]},
                                    seeds=[101], episode_steps=120, log=lambda *_: None)
        ablate.validate_grid_completeness(games, ["scale_ranch"], [101])
        pairs = ablate.pair_cells(games)
        assert len(pairs) == 2  # AB + BA
        for pair in pairs:
            assert pair["cand_margin"] == pair["champ_margin"]
            assert pair["outcome"] == "T"
        cand_gate = ablate.side_gate_metrics(games, "cand", ["scale_ranch"])
        champ_gate = ablate.side_gate_metrics(games, "champion", ["scale_ranch"])
        verdict = ablate.merge_verdict(cand_gate, champ_gate)
        assert verdict["mergeable"] is True
        assert cand_gate["record"] == champ_gate["record"]
    finally:
        for path in list(ablate._TEMP_FILES):
            os.unlink(path)
            ablate._TEMP_FILES.remove(path)
