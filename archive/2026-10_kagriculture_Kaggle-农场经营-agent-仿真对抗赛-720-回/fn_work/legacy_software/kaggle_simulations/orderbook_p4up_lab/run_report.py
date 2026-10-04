# -*- coding: utf-8 -*-
"""run_report —— 六判据 + 磁带基线的样例报告 CLI（判决先行·只读不发射不提交）。

用法（kaggle_simulations/ 目录下）：
  python3 -m orderbook_p4up_lab.run_report \
      --records orderbook_p4up_lab/samples/cohort_tfc_20260923.jsonl \
      [--trajectory traj.json] \
      [--feats-band <feats-band.jsonl> --feats-team "THIRD FARM CLUB"] \
      [--out orderbook_p4up_lab/samples/xray_p4up_sample_report.json]

输出：evidence 风格 JSON（version/task/readings/caveats/_generated_at）+ 控制台摘要。
每条判据输出强制携带 threshold（阈值随判声明纪律，x-ray cell 33）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM = os.path.dirname(_HERE)
if __name__ == "__main__" and _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

from orderbook_p4up_lab import adapters as A          # noqa: E402
from orderbook_p4up_lab import baseline as B          # noqa: E402
from orderbook_p4up_lab import criteria as C          # noqa: E402
from orderbook_p4up_lab import divergence as D        # noqa: E402

RECORD_VERSION = "xray-p4up/1.0"


def _iso_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(records, trajectory=None, timestamps=None,
                 feats_band_path=None, feats_team=None,
                 baseline_path=None) -> dict:
    rep = {
        "version": RECORD_VERSION,
        "task": ("P3 判决尺升级：destbreso X-ray 六判据 + leoprovorov p25 磁带基线"
                 "（判决先行·只读不发射不提交）"),
        "criteria_spec": C.CRITERIA_SPEC,
        "cohort": {
            "n_records": len(records),
            "subjects": sorted({r.team for r in records}),
            "opponents": sorted({r.opp for r in records}),
            "worlds": sorted({(r.world or "UNSPECIFIED") for r in records}),
            "windows": sorted({str(r.window) for r in records}),
        },
        "readings": {},
        "caveats": [],
    }
    if not records:
        rep["readings"]["error"] = "no records"
        rep["_generated_at"] = _iso_now()
        return rep

    # ① GLOBAL vs WITHIN-WORLD
    rep["readings"]["C1_GLOBAL_WITHIN_WORLD"] = C.dual_classification(records)

    # ② 血缘谱 + 基因群
    spec = C.kinship_spectrum(records)
    gg = C.genetic_groups(
        [r.opp_stream for r in records],
        labels=[r.opp for r in records],
        sub_ids=[r.opp_sub for r in records],
        margins=[r.margin for r in records])
    spec["genetic_groups"] = gg["genetic_groups"]
    spec["n_groups"] = gg["n_groups"]
    spec["genetic_threshold"] = gg["threshold"]
    rep["readings"]["C2_KINSHIP_MIRROR"] = spec

    # ③ 收敛三件套
    conv = C.convergence(trajectory or [], timestamps=timestamps)
    rep["readings"]["C3_CONVERGENCE"] = conv

    # ④ 语言指纹
    rep["readings"]["C4_LANGUAGE_FINGERPRINT"] = C.language_fingerprint(records)

    # ⑤ crater（cell 24 口径：样本内最大 |margin| 的决定性一局）
    decisive = max(records, key=lambda r: abs(r.margin))
    cr = C.crater_scan(decisive)
    cr["decisive_episode"] = {"episode": decisive.episode,
                              "margin": decisive.margin,
                              "world": decisive.world,
                              "rule": "样本内最大 |margin| 一局（x-ray cell 24，自报）"}
    rep["readings"]["C5_CRATER"] = cr

    # ⑥ 热图半分闸
    rep["readings"]["C6_BOARD_HALFSPLIT"] = C.board_maps(records)

    # 磁带画像 + 基线分层（leoprovorov 口径：bundle / D(t) / p_q）
    prof = D.tape_profile([r.stream for r in records],
                          label="+".join(sorted({r.team for r in records})))
    rep["tape_profile"] = prof
    # leoprovorov 基线只用胜局 → 同口径子画像并出（对读用）
    wins_only = [r for r in records if r.margin > 0]
    rep["tape_profile_wins_only"] = (
        D.tape_profile([r.stream for r in wins_only],
                       label=prof["label"] + " (wins only, leoprovorov 口径)")
        if wins_only else {"status": "INSUFFICIENT_DATA", "n_games": 0,
                           "note": "cohort 无胜局，基线口径画像不可得"})
    rep["baseline_lookup"] = B.profile_lookup(prof["p10"], prof["p25"], prof["p50"],
                                              baseline=B.load_baseline(baseline_path))
    rep["baseline_lookup_wins_only"] = B.profile_lookup(
        rep["tape_profile_wins_only"].get("p10"),
        rep["tape_profile_wins_only"].get("p25"),
        rep["tape_profile_wins_only"].get("p50"),
        baseline=B.load_baseline(baseline_path)) if wins_only else None

    # 可选：feats-band day0 横断面（第二入口实证）
    if feats_band_path and feats_team:
        rep["feats_band_day0_crosscheck"] = feats_band_crosscheck(
            feats_band_path, feats_team)

    # 限界声明
    wins = [r for r in records if r.margin > 0]
    rep["caveats"] = [
        f"tape_profile 用全部 {len(records)} 局；leoprovorov 基线只用胜局"
        f"（本 cohort 胜局 {len(wins)}），对读时口径差须声明",
        "t<48 可观测盲区：早期一致=引擎确定性（x-ray cell 16）",
        "x-ray 自校准数字（语言锚/宏观形状/用工共识/单位时间预算）全部标'自报'，"
        "本报告未复测",
        "exp066_arena.json 无逐局行（仅对级聚合），未作判据输入（任务候选数据缺项）",
    ]
    rep["_generated_at"] = _iso_now()
    return rep


def feats_band_crosscheck(path: str, team: str) -> dict:
    """feats-band 第二入口：该队 day0 片段的跨局一致度（t<24）。"""
    streams = []
    n_rows = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            for rec in A.feats_row_to_records(row):
                if rec.team == team:
                    streams.append(rec.stream)
                    n_rows += 1
    out = {"team": team, "n_episodes": n_rows, "window": "day0 (t<24)"}
    if n_rows < 2:
        out["status"] = "INSUFFICIENT_DATA"
        return out
    cmp_out = C.compare_streams(streams)
    out.update({
        "status": "OK",
        "varying_frac": round(cmp_out["frac"], 4),
        "first_divergence": cmp_out["first"],
        "cls": C.classify(cmp_out),
        "note": ("t<24 在 t<48 盲区内：一致=磁带预期、不一致=强信号；"
                 "hands 通道缺失（feats-band 口径）"),
    })
    return out


def render_text(rep: dict) -> str:
    L = []
    L.append(f"== {rep['version']} | {rep['task']}")
    coh = rep["cohort"]
    L.append(f"cohort: n={coh['n_records']} subjects={coh['subjects']} "
             f"worlds={len(coh['worlds'])} windows={coh['windows']}")
    r = rep["readings"]
    c1 = r["C1_GLOBAL_WITHIN_WORLD"]
    L.append(f"[C1] GLOBAL={c1['global']['cls']} (vary {c1['global']['varying_frac']:.1%}, "
             f"first t={c1['global']['first_divergence']}) | within-world "
             f"{c1['verdict_counts']} | {c1['gap_diagnosis']}")
    if c1.get("router_hint"):
        L.append(f"     router_hint: {c1['router_hint']}")
    c2 = r["C2_KINSHIP_MIRROR"]
    L.append(f"[C2] mirror {c2['n_mirror']} | sibling {c2['n_sibling']} | "
             f"unrelated {c2['n_unrelated']} | mirror_record {c2['mirror_record']} | "
             f"groups {c2['n_groups']} (threshold plan>=0.95 / genetic>=0.98)")
    c3 = r["C3_CONVERGENCE"]
    if c3["verdict"] == "TOO_FEW":
        L.append(f"[C3] TOO_FEW (n={c3['n']}): {c3.get('note', '')}")
    else:
        L.append(f"[C3] {c3['verdict']} (drift {c3['drift']:+.2f} pts/ep, "
                 f"flips {c3['flips']}, threshold {c3['threshold']}, n={c3['n']})")
    c4 = r["C4_LANGUAGE_FINGERPRINT"]
    if c4.get("bands"):
        bands = " | ".join(f"{k}: r={v['repeat_rate']} H={v['norm_entropy']} "
                           f"k={v['distinct']}" for k, v in c4["bands"].items())
        L.append(f"[C4] class={c4['class']} || {bands}")
    else:
        L.append(f"[C4] {c4['class']} (n={c4['n_episodes']}, floor 8)")
    c5 = r["C5_CRATER"]
    if c5.get("status") == "OK":
        L.append(f"[C5] decisive ep {c5['decisive_episode']['episode']} "
                 f"(margin {c5['decisive_episode']['margin']:+,.0f}) | our craters "
                 f"{c5['totals']['n_our']} dmg {c5['totals']['our_dmg']:,.0f} | theirs "
                 f"{c5['totals']['n_their']} dmg {c5['totals']['their_dmg']:,.0f} "
                 f"(window 24, top60)")
    else:
        L.append(f"[C5] {c5['status']}: {c5.get('note', '')}")
    c6 = r["C6_BOARD_HALFSPLIT"]
    if c6.get("status") == "OK":
        for kind, v in c6["maps"].items():
            L.append(f"[C6] {kind}: half-split r={v['corr_half']} gate={v['gate']} "
                     f"chi2/dof={v['chi2_dof']} top10={v['top10_share']} "
                     f"(gate r>=0.9)")
    else:
        L.append(f"[C6] {c6['status']}: {c6.get('note', '')}")
    tp = rep["tape_profile"]
    bl = rep["baseline_lookup"]
    L.append(f"[TAPE] p10/p25/p50 = {tp['p10']}/{tp['p25']}/{tp['p50']} "
             f"(mean D d0-71 {tp['mean_D_d0_71']} / d72-143 {tp['mean_D_d72_143']}) "
             f"-> tier {bl['tape_tier']} | nearest {bl['nearest_baseline_team']}")
    tpw = rep.get("tape_profile_wins_only") or {}
    if tpw.get("p25") is not None or tpw.get("p10") is not None:
        L.append(f"[TAPE-wins] p10/p25/p50 = {tpw.get('p10')}/{tpw.get('p25')}/"
                 f"{tpw.get('p50')} (n={tpw.get('n_games')}, 基线同口径=仅胜局)")
    if "feats_band_day0_crosscheck" in rep:
        fx = rep["feats_band_day0_crosscheck"]
        L.append(f"[FEATS] day0 crosscheck {fx['team']}: n={fx['n_episodes']} "
                 f"vary {fx.get('varying_frac', '-')} cls {fx.get('cls', '-')}")
    for cav in rep["caveats"]:
        L.append(f"  ! {cav}")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="xray-p4up 六判据样例报告")
    ap.add_argument("--records", required=True, help="compact records JSONL")
    ap.add_argument("--trajectory", help="评分轨迹 JSON {trajectory:[...], timestamps:[...]}")
    ap.add_argument("--feats-band", dest="feats_band", help="feats-band.jsonl（可选第二入口）")
    ap.add_argument("--feats-team", dest="feats_team", help="feats-band 队名过滤")
    ap.add_argument("--baseline", help="opponents_baseline.json 覆盖路径")
    ap.add_argument("--out", help="输出报告 JSON 路径")
    args = ap.parse_args(argv)

    records = A.load_records_jsonl(args.records)
    trajectory = timestamps = None
    if args.trajectory:
        with open(args.trajectory, encoding="utf-8") as fh:
            tj = json.load(fh)
        trajectory = tj.get("trajectory") or []
        raw_ts = tj.get("timestamps") or []
        timestamps = [_dt.datetime.fromisoformat(t) for t in raw_ts] or None

    rep = build_report(records, trajectory=trajectory, timestamps=timestamps,
                       feats_band_path=args.feats_band, feats_team=args.feats_team,
                       baseline_path=args.baseline)
    text = render_text(rep)
    print(text)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        txt_path = os.path.splitext(args.out)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"[written] {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
