"""Online probe sampling contract (workflow, not bot behavior).

Launch ledgers at ``exports/online/roundN_ledger.json`` are submit-time
snapshots. They may keep ``status=PENDING``. Completion is a separate
sampling record at ``exports/online/sampling/roundN_sampling.json``,
filled from official Kaggle CLI episode lists + replay JSON.

Local quickwin / vendored self-play is a catastrophe diagnostic only.
It is not strength evidence and must not authorize the next submit.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

PROTOCOL = "online-probe-sampling/1.0"
FIRST_SAMPLING_ROUND = 20
DEFAULT_TEAM = "renyxin"
HOURS_PER_DAY = 24
EXPECTED_STEPS = 720
LAUNCH_LEDGER_RE = re.compile(r"^round(\d+)_ledger\.json$")
SAMPLING_RE = re.compile(r"^round(\d+)_sampling\.json$")
CROP_KEYS = ("WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO")


class OnlineProbeError(ValueError):
    """Raised when the next-round online gate fails closed."""


def software_root_from(start: Path | None = None) -> Path:
    cur = (start or Path(__file__)).resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur, *cur.parents]:
        if (candidate / "kaggle_simulations").is_dir() and (
                candidate / "exports" / "online").is_dir():
            return candidate
    return Path(__file__).resolve().parents[1]


def launch_ledger_dir(root: Path) -> Path:
    return root / "exports" / "online"


def sampling_dir(root: Path) -> Path:
    return root / "exports" / "online" / "sampling"


def replay_dir(campaign_root: Path, round_no: int) -> Path:
    # 2026-09-23 大整合：references 已并入 fn_docs/（新布局优先，旧布局兼容）
    for prefix in ("fn_docs/references", "references"):
        d = campaign_root / prefix / "data" / "online-replays" / f"round{round_no}"
        if (campaign_root / prefix / "data").is_dir() or prefix == "references":
            return d
    raise FileNotFoundError("references/data 不可定位（新旧布局均未找到）")


def campaign_root_from_software(root: Path) -> Path:
    # 2026-09-23 大整合：software 可位于 <campaign>/software（旧）或
    # <campaign>/fn_work/legacy_software（新）——按特征上溯定战役根，不猜层级。
    for cand in (root.parent, *root.parents):
        if (cand / "fn_docs").is_dir() and (cand / "fn_work").is_dir():
            return cand
        if (cand / "blueprint.md").exists() and (cand / "software").is_dir():
            return cand
    raise FileNotFoundError(f"campaign root 不可定位（自 {root} 上溯无新旧布局特征）")


def list_launch_rounds(root: Path) -> dict[int, Path]:
    found: dict[int, Path] = {}
    directory = launch_ledger_dir(root)
    if not directory.is_dir():
        return found
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = LAUNCH_LEDGER_RE.match(path.name)
        if match:
            found[int(match.group(1))] = path
    return found


def list_sampling_rounds(root: Path) -> dict[int, Path]:
    found: dict[int, Path] = {}
    directory = sampling_dir(root)
    if not directory.is_dir():
        return found
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = SAMPLING_RE.match(path.name)
        if match:
            found[int(match.group(1))] = path
    return found


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OnlineProbeError(f"expected object in {path}")
    return value


def submission_ref_of(ledger: dict[str, Any]) -> int | None:
    candidate = ledger.get("candidate")
    if isinstance(candidate, dict) and candidate.get("submission_ref") is not None:
        return int(candidate["submission_ref"])
    if ledger.get("submission_ref") is not None:
        return int(ledger["submission_ref"])
    return None


def launch_status_of(ledger: dict[str, Any]) -> str:
    candidate = ledger.get("candidate")
    if isinstance(candidate, dict):
        for key in ("status", "status_at_record"):
            if candidate.get(key):
                return str(candidate[key])
    return str(ledger.get("status") or "")


def check_replay_integrity(replay: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    info = replay.get("info") or {}
    teams = info.get("TeamNames")
    if not isinstance(teams, list) or len(teams) != 2 or any(
            not isinstance(name, str) or not name for name in teams):
        issues.append("bad TeamNames")
    statuses = replay.get("statuses")
    if not isinstance(statuses, list) or len(statuses) != 2 or any(
            status != "DONE" for status in statuses):
        issues.append(f"statuses={statuses}")
    steps = replay.get("steps")
    if not isinstance(steps, list) or len(steps) != EXPECTED_STEPS:
        n_steps = len(steps) if isinstance(steps, list) else "missing"
        issues.append(f"steps={n_steps}")
    rewards = replay.get("rewards")
    if not isinstance(rewards, list) or len(rewards) != 2 or any(
            not isinstance(reward, (int, float)) or math.isnan(reward)
            for reward in rewards):
        issues.append(f"rewards={rewards}")
    return issues


def _tile_crop_and_herd(tiles: Any) -> tuple[dict[str, int], int]:
    crops = {crop: 0 for crop in CROP_KEYS}
    herd = 0
    if not isinstance(tiles, list):
        return crops, herd
    for row in tiles:
        if not isinstance(row, list):
            continue
        for cell in row:
            if not isinstance(cell, dict):
                continue
            kind = cell.get("kind")
            if kind == "PLANT":
                crop = cell.get("crop")
                if crop in crops:
                    crops[crop] += 1
            elif kind in ("PASTURE", "COOP") and cell.get("animal"):
                herd += 1
    return crops, herd


def summarize_seat_day0_and_curves(replay: dict[str, Any], seat: int) -> dict[str, Any]:
    steps = replay.get("steps") or []
    plants_d0 = {crop: 0 for crop in CROP_KEYS}
    plants_total = {crop: 0 for crop in CROP_KEYS}
    harvest = 0
    water = 0
    standing: dict[int, dict[str, Any]] = {}
    peak_herd = 0
    money_by_day: dict[int, float] = {}
    for t, step in enumerate(steps):
        if not isinstance(step, list) or len(step) <= seat:
            continue
        entry = step[seat] if isinstance(step[seat], dict) else {}
        obs = entry.get("observation") or {}
        farms = obs.get("farms") or []
        farm = farms[seat] if len(farms) > seat and isinstance(farms[seat], dict) else {}
        day = obs.get("day", t // HOURS_PER_DAY)
        act = entry.get("action") or {}
        units = [act.get("farmer") or []] + list(act.get("hands") or [])
        for unit in units:
            if not unit:
                continue
            op = unit[0]
            if op == "PLANT" and len(unit) >= 2:
                crop = unit[1]
                if crop in plants_total:
                    plants_total[crop] += 1
                    if day == 0:
                        plants_d0[crop] += 1
            elif op == "HARVEST":
                harvest += 1
            elif op == "WATER":
                water += 1
        money = farm.get("money")
        if isinstance(money, (int, float)):
            money_by_day[int(day)] = float(money)
        if obs.get("hour") == HOURS_PER_DAY - 1 or t == len(steps) - 1:
            crops, herd = _tile_crop_and_herd(farm.get("tiles"))
            peak_herd = max(peak_herd, herd)
            standing[int(day)] = {"crops": crops, "herd": herd}
    def at(day: int, key: str, default=0):
        rec = standing.get(day) or {}
        if key == "herd":
            return rec.get("herd", default)
        crops = rec.get("crops") or {}
        return crops.get(key, default) if isinstance(crops, dict) else default
    return {
        "plants_d0": plants_d0,
        "plants_d0_total": sum(plants_d0.values()),
        "plants_total": plants_total,
        "plants_season": sum(plants_total.values()),
        "harvest": harvest,
        "water": water,
        "peak_herd": peak_herd,
        "wheat_d7": at(7, "WHEAT"),
        "wheat_d12": at(12, "WHEAT"),
        "berry_d7": at(7, "STRAWBERRY"),
        "berry_d12": at(12, "STRAWBERRY"),
        "herd_d0": at(0, "herd"),
        "herd_d8": at(8, "herd"),
        "money_d7": money_by_day.get(7),
        "money_d11": money_by_day.get(11),
        "money_d12": money_by_day.get(12),
    }


def classify_replay(replay: dict[str, Any], our_team: str = DEFAULT_TEAM) -> dict[str, Any]:
    info = replay.get("info") or {}
    teams = list(info.get("TeamNames") or [])
    rewards = list(replay.get("rewards") or [None, None])
    episode_id = info.get("EpisodeId")
    issues = check_replay_integrity(replay)
    record: dict[str, Any] = {
        "id": episode_id,
        "teams": teams,
        "rewards": rewards,
        "statuses": replay.get("statuses"),
        "nsteps": len(replay.get("steps") or []),
        "integrity": "PASS" if not issues else "FAIL",
        "integrity_issues": issues,
    }
    if teams.count(our_team) == 2:
        record.update({
            "kind": "validation",
            "our": rewards[0] if rewards else None,
            "opp": rewards[1] if len(rewards) > 1 else None,
            "opp_name": "self",
            "won": None,
        })
        return record
    if our_team not in teams or len(teams) != 2:
        record.update({"kind": "unknown", "won": None})
        return record
    seat = teams.index(our_team)
    opp_seat = 1 - seat
    our = rewards[seat] if len(rewards) > seat else None
    opp = rewards[opp_seat] if len(rewards) > opp_seat else None
    won = None
    if isinstance(our, (int, float)) and isinstance(opp, (int, float)):
        won = our > opp
    summary = summarize_seat_day0_and_curves(replay, seat)
    opp_summary = summarize_seat_day0_and_curves(replay, opp_seat)
    record.update({
        "kind": "public",
        "seat": seat,
        "our": our,
        "opp": opp,
        "opp_name": teams[opp_seat],
        "won": won,
        "margin": (our - opp) if isinstance(our, (int, float))
        and isinstance(opp, (int, float)) else None,
        "ours": summary,
        "opponent": {
            "plants_d0_total": opp_summary["plants_d0_total"],
            "plants_d0": opp_summary["plants_d0"],
            "plants_season": opp_summary["plants_season"],
            "peak_herd": opp_summary["peak_herd"],
            "wheat_d7": opp_summary["wheat_d7"],
            "berry_d12": opp_summary["berry_d12"],
            "money_d11": opp_summary["money_d11"],
        },
    })
    return record


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 1) if values else None


def aggregate_public(games: list[dict[str, Any]]) -> dict[str, Any]:
    public = [g for g in games if g.get("kind") == "public" and g.get("integrity") == "PASS"]
    wins = sum(1 for g in public if g.get("won") is True)
    losses = sum(1 for g in public if g.get("won") is False)
    ours = [float(g["our"]) for g in public if isinstance(g.get("our"), (int, float))]
    opps = [float(g["opp"]) for g in public if isinstance(g.get("opp"), (int, float))]
    margins = [float(g["margin"]) for g in public if isinstance(g.get("margin"), (int, float))]
    d0 = [float(g["ours"]["plants_d0_total"]) for g in public if g.get("ours")]
    d0_opp = [float(g["opponent"]["plants_d0_total"]) for g in public if g.get("opponent")]
    berry_d12 = [float(g["ours"]["berry_d12"]) for g in public if g.get("ours")]
    berry_d12_opp = [float(g["opponent"]["berry_d12"]) for g in public if g.get("opponent")]
    wheat_d7 = [float(g["ours"]["wheat_d7"]) for g in public if g.get("ours")]
    herd_d0 = [float(g["ours"]["herd_d0"]) for g in public if g.get("ours")]
    harvest = [float(g["ours"]["harvest"]) for g in public if g.get("ours")]
    money_d11 = [float(g["ours"]["money_d11"]) for g in public
                 if g.get("ours") and g["ours"].get("money_d11") is not None]
    money_d11_opp = [float(g["opponent"]["money_d11"]) for g in public
                     if g.get("opponent") and g["opponent"].get("money_d11") is not None]
    n = len(public)
    return {
        "public_games": n,
        "record": f"{wins}W-{losses}L",
        "wins": wins,
        "losses": losses,
        "win_rate": round(wins / n, 4) if n else None,
        "our_money_mean": _mean(ours),
        "opp_money_mean": _mean(opps),
        "mean_margin": _mean(margins),
        "axes": {
            "d0_plants_ours": _mean(d0),
            "d0_plants_opp": _mean(d0_opp),
            "wheat_d7_ours": _mean(wheat_d7),
            "berry_d12_ours": _mean(berry_d12),
            "berry_d12_opp": _mean(berry_d12_opp),
            "herd_d0_ours": _mean(herd_d0),
            "harvest_ours": _mean(harvest),
            "money_d11_ours": _mean(money_d11),
            "money_d11_opp": _mean(money_d11_opp),
        },
        "episodes": [
            {
                "id": g.get("id"),
                "result": "W" if g.get("won") else "L",
                "our": g.get("our"),
                "opp": g.get("opp"),
                "opp_name": g.get("opp_name"),
                "margin": g.get("margin"),
                "seat": g.get("seat"),
            }
            for g in public
        ],
    }


def build_sampling_payload(
        *,
        round_no: int,
        submission_ref: int,
        launch_ledger: dict[str, Any],
        games: list[dict[str, Any]],
        public_score: float | None,
        source: dict[str, Any],
        captured_at_utc: str,
        our_team: str = DEFAULT_TEAM,
) -> dict[str, Any]:
    public = aggregate_public(games)
    validation = [g for g in games if g.get("kind") == "validation"]
    failed = [g for g in games if g.get("integrity") != "PASS"]
    if public["public_games"] < 1 and not validation:
        raise OnlineProbeError(
            f"round {round_no}: no usable official games (need public or validation replay)")
    if source.get("replays_are_local_selfplay"):
        raise OnlineProbeError(
            "local self-play cannot complete an online sampling record")
    candidate = launch_ledger.get("candidate") if isinstance(
        launch_ledger.get("candidate"), dict) else {}
    return {
        "schema": PROTOCOL,
        "round": round_no,
        "submission_ref": submission_ref,
        "our_team": our_team,
        "status": "COMPLETE",
        "captured_at_utc": captured_at_utc,
        "candidate": {
            "label": candidate.get("label") or launch_ledger.get("candidate_label"),
            "pkg_sha256": candidate.get("pkg_sha256"),
            "main_sha256": candidate.get("main_sha256") or launch_ledger.get("candidate_sha256"),
            "git_ref": candidate.get("git_ref") or launch_ledger.get("git_ref"),
        },
        "launch_snapshot": {
            "path": f"exports/online/round{round_no}_ledger.json",
            "status_at_submit": launch_status_of(launch_ledger) or "PENDING",
            "note": "launch ledger is a submit-time snapshot and is left unchanged",
        },
        "source": {
            "channel": source.get("channel") or "kaggle-cli",
            "competition": source.get("competition") or "kaggriculture",
            "commands": source.get("commands") or [
                f"kaggle competitions episodes {submission_ref}",
                "kaggle competitions replay <episode_id>",
            ],
            "replay_dir": source.get("replay_dir"),
            "replays_are_local_selfplay": False,
            "local_quickwin_not_adjudication": True,
        },
        "local_quickwin_not_adjudication": True,
        "public_score": public_score,
        "validation": [
            {
                "id": g.get("id"),
                "rewards": g.get("rewards"),
                "integrity": g.get("integrity"),
            }
            for g in validation
        ],
        "public_sampling": public,
        "integrity_failures": [
            {"id": g.get("id"), "issues": g.get("integrity_issues")}
            for g in failed
        ],
        "verdict": (
            f"OFFICIAL SAMPLE {public['record']} over {public['public_games']} public games; "
            "local quickwin/self-play is not this verdict."
        ),
    }


def validate_sampling(payload: dict[str, Any], min_public: int = 3) -> list[str]:
    issues: list[str] = []
    if payload.get("schema") != PROTOCOL:
        issues.append(f"schema={payload.get('schema')}")
    if payload.get("status") != "COMPLETE":
        issues.append(f"status={payload.get('status')}")
    if payload.get("local_quickwin_not_adjudication") is not True:
        issues.append("local_quickwin_not_adjudication must be true")
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    if source.get("replays_are_local_selfplay"):
        issues.append("sampling source is local self-play")
    sampling = payload.get("public_sampling") if isinstance(
        payload.get("public_sampling"), dict) else {}
    n_public = int(sampling.get("public_games") or 0)
    if n_public < min_public:
        issues.append(f"public_games={n_public} < {min_public}")
    if not payload.get("submission_ref"):
        issues.append("missing submission_ref")
    return issues


def next_round_gate(root: Path, min_public: int = 3,
                    first_sampling_round: int = FIRST_SAMPLING_ROUND) -> dict[str, Any]:
    launches = list_launch_rounds(root)
    samplings = list_sampling_rounds(root)
    reasons: list[str] = []
    if not launches:
        reasons.append("no launch ledgers found")
        return {"pass": False, "reasons": reasons, "latest_round": None}

    latest = max(launches)
    covered = []
    missing = []
    for round_no, launch_path in sorted(launches.items()):
        if round_no < first_sampling_round:
            continue
        ledger = load_json(launch_path)
        ref = submission_ref_of(ledger)
        if ref is None:
            reasons.append(f"round {round_no} launch ledger has no submission_ref")
            continue
        sampling_path = samplings.get(round_no)
        if sampling_path is None:
            missing.append(round_no)
            reasons.append(
                f"round {round_no} (ref {ref}) still has no sampling record; "
                "run sync_online_probe.py ingest after kaggle CLI fetch"
            )
            continue
        payload = load_json(sampling_path)
        if int(payload.get("submission_ref") or 0) != int(ref):
            reasons.append(
                f"round {round_no} sampling ref {payload.get('submission_ref')} "
                f"!= launch ref {ref}"
            )
        sample_min = min_public if round_no == latest else 1
        issues = validate_sampling(payload, min_public=sample_min)
        if issues:
            reasons.append(f"round {round_no} sampling incomplete: {'; '.join(issues)}")
        else:
            covered.append(round_no)

    latest_sampling = samplings.get(latest)
    if latest_sampling is None:
        reasons.append(
            f"latest launch round {latest} has no official replay sampling; "
            "do not retune or resubmit from local quickwin"
        )
    report = {
        "pass": not reasons,
        "reasons": reasons,
        "latest_round": latest,
        "sampled_rounds": covered,
        "missing_rounds": missing,
        "rule": (
            "Local quickwin/self-play is not a submit gate. "
            f"Rounds >= {first_sampling_round} require COMPLETE official sampling "
            f"before the next retune/submit; latest round needs >= {min_public} public games."
        ),
    }
    return report


def assert_next_round_allowed(root: Path, min_public: int = 3) -> dict[str, Any]:
    report = next_round_gate(root, min_public=min_public)
    if not report["pass"]:
        raise OnlineProbeError("; ".join(report["reasons"]))
    return report
