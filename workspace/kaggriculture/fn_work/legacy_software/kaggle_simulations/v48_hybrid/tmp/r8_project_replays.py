# -*- coding: utf-8 -*-
# 【中文】R8 F4a 语料归档器：14 局领先崩塌回放最小投影 + 孪生保真验证。
# 投影口径（依据 twin.py 消费面实读，2026-09-22）：
#   build_state_from_replay/new_state_from_replay_head 只读 steps[0] 双席完整
#   observation + configuration + info.seed；replay_transition_actions 只读
#   steps[t>=1][seat].action。故投影 = head 原样 + 后续步仅保留 action，
#   附 _min_projection 溯源元数据（原件 sha256/体积/投影日）。
# 保真验证：投影件 build_state_from_replay(0) + run_to_end(自身动作流)
#   终局双席资金 == 原件 rewards（逐位），否则该局标记 FAIL 不归档。
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYB = os.path.dirname(HERE)
KSIM = os.path.dirname(HYB)
SOFTWARE = os.path.dirname(KSIM)
CAMP = os.path.dirname(SOFTWARE)
for _p in (SOFTWARE,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

from kaggle_simulations.agent.planner import twin  # noqa: E402 旧树只读

TIMELINES = os.path.join(HYB, "fn_docs", "results",
                         "2026-09-24-loss-timelines.json")
OUT_DIR = os.path.join(HYB, "fn_docs", "results", "replays-lead-collapse")
SRC_DIRS = ("/tmp/r26full", "/tmp/r27full")
PEAK_MIN = 1000.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def project(replay, src_path):
    steps = replay["steps"]
    slim_steps = [steps[0]]
    for t in range(1, len(steps)):
        slim_steps.append([{"action": (steps[t][0] or {}).get("action")},
                           {"action": (steps[t][1] or {}).get("action")}])
    out = {k: replay[k] for k in ("configuration", "info", "rewards",
                                  "statuses", "id", "name", "description",
                                  "title") if k in replay}
    out["steps"] = slim_steps
    out["_min_projection"] = {
        "tool": "v48_hybrid/tmp/r8_project_replays.py",
        "projected_utc": "2026-09-22",
        "source_file": os.path.basename(src_path),
        "source_sha256": sha256_file(src_path),
        "source_bytes": os.path.getsize(src_path),
        "rule": ("steps[0] verbatim; steps[t>=1] keep seat action only; "
                 "twin consumer face = build_state_from_replay + "
                 "replay_transition_actions"),
    }
    return out


def verify_final_money(slim, bundle):
    state = twin.build_state_from_replay(slim, 0, bundle)
    actions = twin.replay_transition_actions(slim)
    twin.run_to_end(state, actions)
    return twin.final_money(state)


def main():
    timelines = json.load(open(TIMELINES))
    losses = timelines["corpus"]["derivative"]["losses"]
    sel = [g for g in losses
           if (g.get("max_lead_day_amount") or {}).get("amount", 0)
           >= PEAK_MIN]
    print(f"selected {len(sel)} lead-collapse games (peak>={PEAK_MIN})")
    bundle = twin.load_engine()
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    for g in sorted(sel, key=lambda x: -x["max_lead_day_amount"]["amount"]):
        ep = g["ep"]
        src = None
        for base in SRC_DIRS:
            cand = os.path.join(base, f"episode-{ep}-replay.json")
            if os.path.exists(cand):
                src = cand
                break
        if src is None:
            report.append({"ep": ep, "status": "SOURCE_MISSING"})
            continue
        replay = json.load(open(src))
        slim = project(replay, src)
        fm = verify_final_money(slim, bundle)
        ok = ([float(v) for v in fm]
              == [float(v) for v in replay.get("rewards", [])])
        dst = os.path.join(OUT_DIR, f"episode-{ep}-replay.json")
        if ok:
            with open(dst, "w", encoding="utf-8") as h:
                json.dump(slim, h, ensure_ascii=False, separators=(",", ":"))
        report.append({
            "ep": ep, "status": "OK" if ok else "FIDELITY_FAIL",
            "final_money": fm, "rewards": replay.get("rewards"),
            "src_bytes": os.path.getsize(src),
            "slim_bytes": os.path.getsize(dst) if ok else None,
            "src_dir": os.path.basename(os.path.dirname(src)),
        })
        print(json.dumps(report[-1], ensure_ascii=False))
    n_ok = sum(1 for r in report if r["status"] == "OK")
    total = sum(r["slim_bytes"] or 0 for r in report)
    print(f"SUMMARY ok={n_ok}/{len(report)} total_slim_bytes={total}")
    with open(os.path.join(HERE, "r8_replay_projection_report.json"),
              "w", encoding="utf-8") as h:
        json.dump(report, h, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
