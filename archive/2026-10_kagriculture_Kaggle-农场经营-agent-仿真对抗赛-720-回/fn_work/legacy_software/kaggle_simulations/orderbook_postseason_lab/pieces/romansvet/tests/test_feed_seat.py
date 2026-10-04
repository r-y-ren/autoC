"""The Kaggle episode feed omits an agent's `index` when it is 0 -> seat 0.

`ListEpisodes` serialises `episodes[].agents[]` with proto3 default-omission, so
the seat-0 entry has NO `index` key at all.  A reader that defaults the missing
key to 1 reads our own row as the opponent's
(docs/strategy/2026-09-16-nbintel2.md, docs/strategy/2026-09-16-seatfix.md).
These tests pin the shared helper and keep the defect from coming back by
static scan of every feed reader on disk.
"""
import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEAT_PY = ROOT / "S" / "kaggle" / "seat.py"

_spec = importlib.util.spec_from_file_location("kagg_feed_seat", SEAT_PY)
seat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(seat)

OURS = 56277270
THEIRS = 56212726

#: our submission in seat 0 -- the feed OMITS `"index": 0`
EP_WE_ARE_SEAT0 = {
    "id": 108000001, "state": "COMPLETED", "type": "EPISODE_TYPE_PUBLIC",
    "agents": [
        {"id": 1, "submissionId": OURS, "reward": 151578, "updatedScore": 2000.0},
        {"id": 2, "submissionId": THEIRS, "reward": 140691, "index": 1,
         "updatedScore": 3100.0},
    ],
}
#: our submission in seat 1 -- only the seat-1 entry carries an `index`
EP_WE_ARE_SEAT1 = {
    "id": 108000002, "state": "COMPLETED", "type": "EPISODE_TYPE_PUBLIC",
    "agents": [
        {"id": 3, "submissionId": THEIRS, "reward": 99126, "updatedScore": 3100.0},
        {"id": 4, "submissionId": OURS, "reward": 115705, "index": 1,
         "updatedScore": 2000.0},
    ],
}
#: self-play validation: both seats are the same submission, so there is no opponent
EP_VALIDATION = {
    "id": 108000003, "state": "COMPLETED", "type": "EPISODE_TYPE_VALIDATION",
    "agents": [
        {"id": 5, "submissionId": OURS, "reward": 65110},
        {"id": 6, "submissionId": OURS, "reward": 65476, "index": 1},
    ],
}


def test_missing_index_is_seat_zero():
    assert seat.agent_index(EP_WE_ARE_SEAT0["agents"][0]) == 0
    assert seat.agent_index(EP_WE_ARE_SEAT0["agents"][1]) == 1
    # an explicit 0 and a falsy 0 both read as seat 0
    assert seat.agent_index({"index": 0}) == 0


def test_our_seat_and_opp_seat_both_ways():
    assert seat.our_seat(EP_WE_ARE_SEAT0, OURS) == 0
    assert seat.opp_seat(EP_WE_ARE_SEAT0, OURS) == 1
    assert seat.our_seat(EP_WE_ARE_SEAT1, OURS) == 1
    assert seat.opp_seat(EP_WE_ARE_SEAT1, OURS) == 0
    # the seats are complements, whichever entry carries the `index`
    for ep in (EP_WE_ARE_SEAT0, EP_WE_ARE_SEAT1):
        assert seat.our_seat(ep, OURS) + seat.opp_seat(ep, OURS) == 1


def test_rating_column_reads_the_other_agent():
    """the rating a picker banks must be THEIRS in both seat layouts"""
    for ep in (EP_WE_ARE_SEAT0, EP_WE_ARE_SEAT1):
        assert seat.opp_agent(ep, OURS)["updatedScore"] == 3100.0
        assert seat.our_agent(ep, OURS)["updatedScore"] == 2000.0


def test_several_of_our_own_subs_and_validation():
    assert seat.our_seat(EP_WE_ARE_SEAT1, [OURS, 56276165]) == 1
    assert seat.opp_agent(EP_VALIDATION, OURS) is None
    assert seat.opp_seat(EP_VALIDATION, OURS) is None
    assert seat.our_seat({"agents": []}, OURS) is None


def test_no_reader_defaults_a_missing_index_to_anything_but_zero():
    """static guard: every `index` read on a feed agent must default to 0"""
    bad = []
    pat = re.compile(r"""get\(\s*["']index["']\s*(?:,\s*([^)]*?)\s*)?\)""")
    for d in ("S", "scripts", "src", "tests"):
        for p in sorted((ROOT / d).rglob("*.py")):
            if "_recovered" in p.parts or "localarm" in p.parts:
                continue
            for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
                for m in pat.finditer(line):
                    dflt = (m.group(1) or "").strip()
                    if dflt not in ("0",):
                        bad.append(f"{p.relative_to(ROOT)}:{n}: default {dflt!r}")
    assert not bad, "feed `index` read without a 0 default:\n" + "\n".join(bad)
