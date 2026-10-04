# -*- coding: utf-8 -*-
"""judge_r45 及判决面子件（R28 判决线）。

责任契约（fn_docs/hybrid/responsibility.md【R28 增补】）：判决 v28——镜像
压力板（克隆/指纹 ≥0.95 局专组）+Wool Front-Runner 反制臂+26 败局重演+胜局
对照（不翻负）；判据核对（净加卖恒等违例=0 ∧ 镜像胜率 ≥0.55 ∧ 实现价不降
∧ 反制不翻车 ∧ 胜局对照不翻负 ∧ h2h vs r40 ≥0.55）；聚合 evidence JSON。
单局红计入（按负）不短路。

真 trace 链路（实现价两侧读数）：局组 specs 一律 trace=True（judge_r26
._chunk 回行带 reads=realized_price_stats[我方 traced sink]）；候选侧=非基线
臂 reads，基线侧=config 定桩 > 行级 reads_opp > 基线臂（baseline_r40=r40
自镜像）reads——缺任一侧→realized_px_no_drop FAIL（fail-closed）。

复用（跨批契约）：判决机器=orderbook_r40/judge_r23（装载/局规格）+
orderbook_r43/judge_r26（_play 跑局+realized_price_stats 读数，不改写）+
fn_work/tools/sim_bridge；反制对手=orderbook_predict/judge_predict
.make_counter_opponent（Wool Front-Runner 构造先例复用）。

【evidence 契约】{"_generated_at", "source": {"commands", "seed_base"},
"arms": [{"arm","n","wins","losses","ties","mean_margin"}], "criteria": {...},
"verdict"}。口径：席位翻转对折叠独立 seed（gates_r37 _seed_level_summary
同口径：score=两席均分，1→胜/0→负/其余→平，无决胜局率=0 fail-closed）；
单局红按负计入（fail-closed），不短路其余局。

【账本形状（B47 定死）】{"debts": [{"item","qty","due_step","advance_step"}],
"settled": [...]}；净量恒等=逐局逐品 Σadvance=Σsettled（判据=违例 0）。
"""
from __future__ import annotations

import gzip
import json
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
# 26 败局语料在库（R28 判据原文口径）；胜局对照与镜像局组=配置化输入
REPLAY_CORPUS_DEFAULT = (MODULE_DIR.parents[3] / "fn_docs" / "hybrid"
                         / "results" / "replays-r30-26")
RECORD_VERSION = "judge-r45/1.0"
# seed 域错开惯例（64=judge_r26/65=gates_r43/66=judge_r44/67=r45）：
# r45 判决局组=670000 域 +gi*1000 错开；门禁 h2h 另取 678000 独立段（独立 n 报）。
SEED_BASE = 670000
N_SEEDS_DEFAULT = 8
MIRROR_BAR = 0.55            # 镜像压力板胜率门槛
COUNTER_BAR = 0.50           # 反制臂不翻车（不转负）
CONTROL_BAR = 0.50           # 胜局对照不翻负（胜率不降下限）
H2H_BAR = 0.55               # h2h vs r40 门槛（seated 双席位）
NET_IDENTITY_BAR = 0         # 净加卖恒等违例门槛
FINGERPRINT_BAR = 0.95       # 镜像专组克隆/指纹下限
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}
# 基线侧（r40）局组：我方位=r40 自镜像——真 trace 链路下基线实现价的结构来源
BASELINE_ARMS = ("baseline_r40",)
CRITERIA_KEYS = ("net_identity", "mirror_win_rate", "realized_px_no_drop",
                 "counter_not_flipped", "control_not_negative", "h2h_vs_r40")


def judge_r45(package, corpus, config):
    """判决 v28：镜像压力板（克隆/指纹≥0.95 局专组）+Wool Front-Runner 反制臂
    +26 败局重演+胜局对照；五判据=净加卖恒等违例 0∧镜像胜率≥0.55∧实现价不降∧
    反制不翻车∧h2h≥0.55。签名意图：输入: r45 包+语料+配置 / 输出: evidence JSON
    （逐组逐局 WL+Δ+判据表） / 错误: 单局红计入不短路。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    t0 = time.perf_counter()
    seed_base = int(cfg.get("seed_base", SEED_BASE))
    n_default = int(cfg.get("n_seeds", N_SEEDS_DEFAULT))
    source = dict(cfg.get("source") or {})
    source.setdefault("commands", [
        "python3 -m pytest test_build_r45.py test_judge_r45.py "
        "test_gates_r45.py test_run_r45.py -q",
        "python3 -c \"from orderbook_r45 import judge_r45 as j; "
        "j.judge_r45('<pkg>', '<corpus>', config)\"",
    ])
    source["seed_base"] = seed_base
    try:
        # ---- 语料归一（26 败局重演；条目=路径或显式局 dict） ----------------
        replay_games: List[Dict[str, Any]] = []
        corpus_error = None
        entries: List[Any] = []
        if corpus is None:
            if REPLAY_CORPUS_DEFAULT.is_dir():
                entries = sorted(REPLAY_CORPUS_DEFAULT.glob("episode-*.json*"))
            else:
                corpus_error = f"默认语料目录缺失: {REPLAY_CORPUS_DEFAULT}"
        elif isinstance(corpus, (str, Path)):
            p = Path(str(corpus))
            if p.is_dir():
                entries = sorted(p.glob("episode-*.json*"))
            elif p.is_file():
                entries = [p]
            else:
                corpus_error = f"语料路径不存在: {p}"
        else:
            try:
                entries = list(corpus)
            except TypeError:
                corpus_error = "语料不可迭代"
        for i, ent in enumerate(entries):
            try:
                if isinstance(ent, dict):
                    g = dict(ent)
                    g.setdefault("game_id", "replay-%d" % i)
                    g.setdefault("arm", "replay_loss")
                    g.setdefault("seated", False)
                    replay_games.append(g)
                    continue
                path = Path(str(ent))
                if str(path).endswith(".gz"):
                    with gzip.open(path, "rb") as fh:
                        data = json.loads(fh.read().decode("utf-8"))
                else:
                    data = json.loads(path.read_text(encoding="utf-8"))
                seed = data.get("seed")
                if seed is None:
                    seed = (data.get("configuration") or {}).get("seed")
                if seed is None:
                    raise ValueError("缺 seed")
                teams = list(data.get("teams")
                             or (data.get("info") or {}).get("TeamNames") or [])
                our_seat = teams.index("renyxin") if "renyxin" in teams else 0
                opp_seat = 1 - our_seat
                opp_actions = []
                for s in (data.get("steps") or []):
                    act = None
                    if isinstance(s, (list, tuple)) and len(s) > opp_seat:
                        node = s[opp_seat]
                        if isinstance(node, dict):
                            act = node.get("action")
                    opp_actions.append(act if isinstance(act, dict)
                                       else dict(PASS_ACTION))
                ep = data.get("episode_id")
                replay_games.append({
                    "game_id": "replay-%s" % (ep if ep is not None
                                              else path.stem),
                    "seed": int(seed), "our_seat": our_seat, "arm": "replay_loss",
                    "seated": False,
                    "opponent": {"type": "tape", "actions": opp_actions},
                })
            except Exception as exc:
                # 单局红计入（按负）不短路
                replay_games.append({
                    "game_id": "replay-%d" % i, "seed": seed_base + i,
                    "arm": "replay_loss", "seated": False,
                    "error": "%s: %s" % (type(exc).__name__, exc),
                })
        # ---- 局组装配（镜像/反制/败局重演/胜局对照/基线/h2h） --------------
        r40_main = str(cfg.get("r40_main") or (MODULE_DIR.parent
                                               / "orderbook_r40" / "build"
                                               / "main.py"))
        groups = cfg.get("groups")
        if not isinstance(groups, list) or not groups:
            groups = [
                {"arm": "mirror", "n": n_default},        # 克隆/指纹 ≥0.95 专组
                {"arm": "counter", "n": n_default},       # Wool Front-Runner
                {"arm": "replay_loss", "games": replay_games,
                 "seated": False},                        # 26 败局重演
                # 胜局对照（不翻负）：缺省恒入局组；内容=配置化输入（缺→红）
                dict(cfg.get("control") or {}, arm="control_win"),
                # 基线侧（r40 自镜像）：实现价不降的结构基线（真 trace 链路）
                {"arm": "baseline_r40", "n": n_default,
                 "agent": {"type": "python", "path": r40_main},
                 "opponent": {"type": "python", "path": r40_main}},
                {"arm": "h2h_r40", "n": n_default,
                 "opponent": {"type": "python", "path": r40_main}},
            ]
        board = {"groups": groups, "runner": cfg.get("runner"),
                 "seed_base": seed_base, "n": n_default,
                 "counter_config": cfg.get("counter_config"),
                 "run_cfg": cfg.get("run_cfg")}
        board_out = run_mirror_counter_judgment(package, board)
        # ---- 净量恒等（台账缺失→违例计 1，fail-closed） --------------------
        ident = verify_net_identity(cfg.get("traces"), cfg.get("ledger"))
        # ---- 实现价（realized_price_stats 复用 judge_r26，不改写） ---------
        # 真 trace 链路（局组 trace=True→_chunk 回行带 reads）候选/基线两侧
        # 都接通：候选=我方位（非基线臂）reads；基线=config 定桩 > 行级
        # reads_opp > 基线臂（r40 自镜像）reads。
        from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
        cand_px: List[float] = []
        base_pair: List[float] = []
        base_arm: List[float] = []
        for row in (board_out.get("rows") or []):
            if not isinstance(row, dict):
                continue
            is_baseline = row.get("arm") in BASELINE_ARMS
            reads = row.get("reads")
            if not isinstance(reads, dict) and row.get("states") is not None:
                reads = j26.realized_price_stats(row.get("states"))
            if isinstance(reads, dict):
                px = reads.get("realized_px")
                if isinstance(px, (int, float)) and not isinstance(px, bool):
                    (base_arm if is_baseline else cand_px).append(float(px))
            reads_opp = row.get("reads_opp")
            if isinstance(reads_opp, dict):
                pxo = reads_opp.get("realized_px")
                if isinstance(pxo, (int, float)) and not isinstance(pxo, bool):
                    base_pair.append(float(pxo))
        candidate_px = round(sum(cand_px) / len(cand_px), 4) if cand_px else None
        cfg_base = cfg.get("baseline_realized_px")
        if isinstance(cfg_base, (int, float)) and not isinstance(cfg_base, bool):
            baseline_px = float(cfg_base)
        elif base_pair:
            baseline_px = round(sum(base_pair) / len(base_pair), 4)
        elif base_arm:
            baseline_px = round(sum(base_arm) / len(base_arm), 4)
        else:
            baseline_px = None
        # ---- 判据核对（R28 五判据+胜局对照不翻负；阈值分支全 fail-closed） --
        arms_rows = list(board_out.get("arms") or [])
        arms_by = {a.get("arm"): a for a in arms_rows if isinstance(a, dict)}
        mirror_wr = (arms_by.get("mirror") or {}).get("win_rate")
        counter_wr = (arms_by.get("counter") or {}).get("win_rate")
        h2h_wr = (arms_by.get("h2h_r40") or {}).get("win_rate")
        mirror_ok = isinstance(mirror_wr, float) and not isinstance(
            mirror_wr, bool) and mirror_wr >= MIRROR_BAR
        counter_ok = isinstance(counter_wr, float) and not isinstance(
            counter_wr, bool) and counter_wr >= COUNTER_BAR
        h2h_ok = isinstance(h2h_wr, float) and not isinstance(
            h2h_wr, bool) and h2h_wr >= H2H_BAR
        realized_ok = (isinstance(candidate_px, float)
                       and isinstance(baseline_px, float)
                       and candidate_px >= baseline_px)
        net_ok = isinstance(ident.get("violations"), int) and \
            ident["violations"] <= NET_IDENTITY_BAR
        control_row = arms_by.get("control_win") or {}
        control_wr = control_row.get("win_rate")
        control_med = control_row.get("median_margin")
        # 胜局对照不翻负：对照组 Δ 中位 ≥0 或胜率不降（≥0.5）；缺/红→FAIL
        control_ok = (bool(control_row) and not control_row.get("red")
                      and ((isinstance(control_med, (int, float))
                            and not isinstance(control_med, bool)
                            and control_med >= 0)
                           or (isinstance(control_wr, float)
                               and not isinstance(control_wr, bool)
                               and control_wr >= CONTROL_BAR)))
        criteria = {
            "net_identity": {
                "value": ident.get("violations"), "bar": NET_IDENTITY_BAR,
                "verdict": "PASS" if net_ok else "FAIL",
                "detail": (ident.get("detail") or [])[:20]},
            "mirror_win_rate": {
                "value": mirror_wr, "bar": MIRROR_BAR,
                "verdict": "PASS" if mirror_ok else "FAIL"},
            "realized_px_no_drop": {
                "value": {"candidate": candidate_px, "baseline": baseline_px},
                "verdict": "PASS" if realized_ok else "FAIL"},
            "counter_not_flipped": {
                "value": counter_wr, "bar": COUNTER_BAR,
                "verdict": "PASS" if counter_ok else "FAIL"},
            "control_not_negative": {
                "value": {"win_rate": control_wr,
                          "median_margin": control_med},
                "bar": CONTROL_BAR,
                "verdict": "PASS" if control_ok else "FAIL"},
            "h2h_vs_r40": {
                "value": h2h_wr, "bar": H2H_BAR,
                "verdict": "PASS" if h2h_ok else "FAIL"},
        }
        verdict = "POSITIVE" if all(
            c.get("verdict") == "PASS" for c in criteria.values()) else "NEGATIVE"
        evidence = {
            "_generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "version": RECORD_VERSION,
            "source": source,
            "arms": arms_rows,
            "criteria": criteria,
            "verdict": verdict,
            "net_identity": ident,
            "corpus": {"n_replay_games": len(replay_games),
                       "error": corpus_error,
                       "default_dir": str(REPLAY_CORPUS_DEFAULT)},
            "control_not_negative": {
                "present": bool(control_row),
                "win_rate": control_wr,
                "median_margin": control_med,
                "red": bool(control_row.get("red")) if control_row else None,
                "not_negative": bool(control_ok)},
            "board": {"seed_base": board_out.get("seed_base"),
                      "seated": board_out.get("seated"),
                      "independent_seeds": board_out.get("independent_seeds"),
                      "opponents": board_out.get("opponents") or {}},
            "elapsed_s": round(time.perf_counter() - t0, 2),
        }
    except Exception as exc:  # 评估侧 fail-closed：异常→全红 evidence，不抛
        fail = {key: {"value": None, "verdict": "FAIL"} for key in CRITERIA_KEYS}
        evidence = {
            "_generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "version": RECORD_VERSION,
            "source": source,
            "arms": [],
            "criteria": fail,
            "verdict": "NEGATIVE",
            "error": "%s: %s" % (type(exc).__name__, exc),
            "elapsed_s": round(time.perf_counter() - t0, 2),
        }
    out_path = Path(cfg.get("evidence_path") or (MODULE_DIR / "evidence"
                                                / "judge_r45_realrun.json"))
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1,
                                       default=str) + "\n", encoding="utf-8")
        evidence["evidence_path"] = str(out_path)
    except Exception as exc:  # 落盘失败不改判（判据已聚合）
        evidence["evidence_error"] = repr(exc)[:160]
    return evidence


def verify_net_identity(traces, ledger):
    """净量恒等核验：逐局逐品对账'提前卖出量=到期抵扣量'，违例计数（判据=0）
    +明细。签名意图：输入: traced 对局+账本台账 / 输出: {violations, detail} /
    错误: 台账缺失→违例计 1（fail-closed）。台账形态（B47 定死）：
    {"debts": [{"item","qty","due_step","advance_step"}], "settled": [...]}；
    单台账或 {game_id: 台账}；traces 提供逐局对账域（缺→以台账键为准）。"""
    detail: List[Dict[str, Any]] = []
    violations = 0
    checked_items = 0
    # ---- 台账缺失（None/非 dict）→违例计 1（fail-closed） -----------------
    if not isinstance(ledger, dict):
        return {"violations": 1, "detail": [{"kind": "ledger_missing"}],
                "games": 0, "checked_items": 0, "ok": False}
    # ---- 对账域：traces 逐局 id（缺/空→台账键） --------------------------
    games: List[Any] = []
    if traces is not None:
        try:
            seq = list(traces)
        except TypeError:
            seq = []
            violations += 1
            detail.append({"kind": "traces_malformed"})
        for i, rec in enumerate(seq):
            gid = None
            if isinstance(rec, dict):
                gid = rec.get("game_id")
                if gid is None:
                    gid = rec.get("seed")
                if gid is None:
                    gid = rec.get("episode")
            elif isinstance(rec, (list, tuple)):
                gid = rec[0] if rec else None
            else:
                gid = rec
            games.append(gid if gid is not None else "game[%d]" % i)
    single = ("debts" in ledger) or ("settled" in ledger)
    if single:
        if not games:
            games = ["_global"]
        ledger_map = {gid: ledger for gid in games}
    else:
        ledger_map = dict(ledger)
        if not games:
            games = list(ledger_map.keys())
    # ---- 逐局逐品 Σadvance=Σsettled --------------------------------------
    for gid in games:
        entry = ledger_map.get(gid)
        if not isinstance(entry, dict):
            violations += 1
            detail.append({"kind": "ledger_missing", "game_id": gid})
            continue
        debts = entry.get("debts")
        settled = entry.get("settled")
        if not isinstance(debts, list) or not isinstance(settled, list):
            violations += 1
            detail.append({"kind": "ledger_missing", "game_id": gid,
                           "reason": "debts/settled 缺失或非列表"})
            continue
        sums_adv: Dict[str, float] = {}
        sums_set: Dict[str, float] = {}
        for kind, rows, bucket in (("debt", debts, sums_adv),
                                   ("settled", settled, sums_set)):
            for rec in rows:
                item = rec.get("item") if isinstance(rec, dict) else None
                qty = rec.get("qty") if isinstance(rec, dict) else None
                if not isinstance(item, str) or not item or isinstance(
                        qty, bool) or not isinstance(qty, (int, float)):
                    violations += 1
                    detail.append({"kind": "malformed_%s" % kind,
                                   "game_id": gid, "record": str(rec)[:80]})
                    continue
                bucket[item] = bucket.get(item, 0.0) + float(qty)
        for item in sorted(set(sums_adv) | set(sums_set)):
            checked_items += 1
            adv = sums_adv.get(item, 0.0)
            setl = sums_set.get(item, 0.0)
            if abs(adv - setl) > 1e-9:
                violations += 1
                detail.append({"kind": "identity_violation", "game_id": gid,
                               "item": item, "advanced": adv, "settled": setl,
                               "delta": adv - setl})
    return {"violations": violations, "detail": detail, "games": len(games),
            "checked_items": checked_items, "ok": violations == 0}


def run_mirror_counter_judgment(package, board_config):
    """压力面执行：镜像压力板+反制臂局组编排（seated 双席位、独立 seed n 报）。
    签名意图：输入: r45 包+局组配置 / 输出: 逐组 WL+margin / 错误: 组不可跑→
    fail-closed 记红。反制臂=Wool Front-Runner 构造对手（orderbook_predict
    make_counter_opponent 先例复用）；镜像组对手=自克隆（指纹 1.0≥0.95 专组）；
    单局红按负计入（fail-closed）不短路。"""
    cfg = dict(board_config) if isinstance(board_config, dict) else {}
    # ---- 包归一（dict=构建输出/注入钩子；str|Path=包目录或 main） ----------
    if isinstance(package, dict):
        pkg = dict(package)
    elif isinstance(package, (str, Path)):
        p = Path(str(package))
        pkg = {"dir": str(p if p.is_dir() else p.parent)}
    else:
        pkg = {}
    main_path = str(pkg.get("main_path") or (
        Path(str(pkg.get("dir") or (MODULE_DIR / "build"))) / "main.py"))
    runner = cfg.get("runner")
    seed_base = int(cfg.get("seed_base", SEED_BASE))
    n_default = int(cfg.get("n", N_SEEDS_DEFAULT))
    run_cfg = dict(cfg.get("run_cfg") or {})
    groups = cfg.get("groups")
    if not isinstance(groups, list) or not groups:
        groups = [{"arm": "mirror"}, {"arm": "counter"}]
    arms: List[Dict[str, Any]] = []
    all_rows: List[Dict[str, Any]] = []
    opponents: Dict[str, Any] = {}
    errors: List[str] = []
    for gi, group in enumerate(groups):
        arm = "group%d" % gi
        try:
            if not isinstance(group, dict):
                raise ValueError("局组配置非 dict")
            arm = str(group.get("arm") or arm)
            n_group = int(group.get("n", n_default))
            games = group.get("games")
            specs: List[Dict[str, Any]] = []
            pre_red: List[Dict[str, Any]] = []
            seated = bool(group.get("seated", games is None))
            if games is None:
                # ---- 对手构造（镜像=自克隆；反制=Wool Front-Runner）--------
                if arm == "mirror":
                    opp = {"type": "python", "path": main_path,
                           "clone": True, "fingerprint": 1.0,
                           "fingerprint_bar": FINGERPRINT_BAR}
                    opponents[arm] = {"kind": "clone_mirror", "fingerprint": 1.0,
                                      "bar": FINGERPRINT_BAR}
                elif arm == "counter":
                    from orderbook_predict import judge_predict as jp  # noqa: WPS433
                    art = jp.make_counter_opponent(
                        group.get("counter_config")
                        or cfg.get("counter_config"))
                    opponents[arm] = {"kind": art["kind"],
                                      "config": art["config"],
                                      "features": art.get("features")}
                    opp = {"type": "python", "path": None,
                           "counter": opponents[arm]}
                    if runner is None:
                        script_path = (MODULE_DIR / "evidence"
                                       / "counter_wool_front_runner.py")
                        script_path.parent.mkdir(parents=True, exist_ok=True)
                        script_path.write_text(art["script"], encoding="utf-8")
                        opp["path"] = str(script_path)
                else:
                    opp_in = group.get("opponent")
                    if not isinstance(opp_in, dict) or not opp_in:
                        raise ValueError("局组缺对手构造（opponent）")
                    opp = dict(opp_in)
                    opponents[arm] = {"kind": "configured"}
                seeds = group.get("seeds")
                if not isinstance(seeds, list) or not seeds:
                    seeds = [seed_base + gi * 1000 + i for i in range(n_group)]
                # 我方位可覆写（基线臂=r40 自镜像）；trace=True 保 _chunk 回行
                # 带 reads（真 trace 链路：实现价候选/基线两侧都可读数）
                ours = dict(group["agent"]) if isinstance(group.get("agent"),
                                                          dict) else \
                    {"type": "python", "path": main_path}
                for seed in seeds:
                    for seat in (0, 1):
                        others = dict(opp)
                        agents = [ours, others] if seat == 0 else [others, ours]
                        specs.append({
                            "game_id": "%s-%s-s%d" % (arm, seed, seat),
                            "seed": int(seed), "arm": arm, "kind": "board",
                            "our_seat": seat, "trace": True, "agents": agents,
                        })
            else:
                # ---- 显式局组（26 败局重演等：tape 对手/固定席位）----------
                for j, g in enumerate(games):
                    gid = (g.get("game_id") if isinstance(g, dict) else None) \
                        or "%s-%d" % (arm, j)
                    if isinstance(g, dict) and g.get("error"):
                        pre_red.append({"game_id": gid,
                                        "seed": g.get("seed", j), "arm": arm,
                                        "our_seat": g.get("our_seat", 0),
                                        "margin": None,
                                        "error": str(g["error"])})
                        continue
                    if not isinstance(g, dict):
                        pre_red.append({"game_id": gid, "seed": j, "arm": arm,
                                        "our_seat": 0, "margin": None,
                                        "error": "局规格非 dict"})
                        continue
                    spec = dict(g)
                    spec.setdefault("game_id", gid)
                    spec.setdefault("arm", arm)
                    spec.setdefault("kind", "board")
                    spec.setdefault("seed", j)
                    spec.setdefault("trace", True)   # 真 trace 链路（回行带 reads）
                    if "agents" not in spec:
                        opp_in = spec.get("opponent")
                        if not isinstance(opp_in, dict) or not opp_in:
                            pre_red.append({"game_id": gid,
                                            "seed": spec.get("seed", j),
                                            "arm": arm,
                                            "our_seat": spec.get("our_seat", 0),
                                            "margin": None,
                                            "error": "局组缺对手构造（opponent）"})
                            continue
                        ours = dict(group["agent"]) if isinstance(
                            group.get("agent"), dict) else \
                            {"type": "python", "path": main_path}
                        seat = int(spec.get("our_seat", 0) or 0)
                        spec["agents"] = [ours, dict(opp_in)] if seat == 0 \
                            else [dict(opp_in), ours]
                    specs.append(spec)
            if not specs and not pre_red:
                raise ValueError("局组不可跑：无局规格")
            # ---- 跑局（注入 runner=假局组夹具；缺省 judge_r26._play）-------
            rows: List[Dict[str, Any]] = []
            if specs:
                if runner is not None:
                    rows = list(runner(specs, run_cfg))
                else:
                    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
                    rows = list(j26._play(specs, run_cfg))
            rows = [r if isinstance(r, dict) else {"error": "row_malformed"}
                    for r in rows] + pre_red
            # ---- margin 归一（banks+seat 回退）+行登记 ---------------------
            norm_rows: List[Dict[str, Any]] = []
            for row in rows:
                r = dict(row)
                r.setdefault("arm", arm)
                seat = r.get("our_seat", r.get("seat", 0))
                try:
                    seat = int(seat)
                except (TypeError, ValueError):
                    seat = 0
                r["our_seat"] = seat
                m = r.get("margin")
                if isinstance(m, bool) or not isinstance(m, (int, float)):
                    banks = r.get("banks")
                    if isinstance(banks, (list, tuple)) and len(banks) == 2 \
                            and all(isinstance(x, (int, float))
                                    and not isinstance(x, bool) for x in banks):
                        m = float(banks[seat]) - float(banks[1 - seat])
                    else:
                        m = None
                r["margin"] = m
                norm_rows.append(r)
            all_rows.extend(norm_rows)
            # ---- seed 级折叠（席位翻转不双计；单局红按负计入）-------------
            by_seed: Dict[Any, List[Dict[str, Any]]] = {}
            for r in norm_rows:
                key = r.get("seed")
                if key is None:
                    key = r.get("game_id")
                by_seed.setdefault(key, []).append(r)
            wins = losses = ties = incomplete = 0
            seed_margins: List[float] = []
            red_seeds: List[Any] = []
            for key in sorted(by_seed, key=lambda x: str(x)):
                rs = by_seed[key]
                valid = [r for r in rs
                         if r.get("error") is None
                         and isinstance(r.get("margin"), (int, float))
                         and not isinstance(r.get("margin"), bool)]
                ms = [float(r["margin"]) for r in valid]
                if ms:
                    seed_margins.append(sum(ms) / len(ms))
                ok = (len(rs) == 2 and len(valid) == 2) if seated \
                    else (len(valid) >= 1)
                if not ok:
                    losses += 1          # 单局红按负计入（fail-closed）
                    incomplete += 1
                    red_seeds.append(key)
                    continue
                if seated:
                    score = sum(1.0 if m > 0 else 0.5 if m == 0 else 0.0
                                for m in ms) / 2.0
                else:
                    mean_m = sum(ms) / len(ms)
                    score = 1.0 if mean_m > 0 else 0.5 if mean_m == 0 else 0.0
                if score >= 1.0:
                    wins += 1
                elif score <= 0.0:
                    losses += 1
                else:
                    ties += 1
            n = len(by_seed)
            decided = wins + losses + ties
            win_rate = round((wins + 0.5 * ties) / decided, 4) if decided \
                else 0.0
            sorted_m = sorted(seed_margins)
            mid = len(sorted_m) // 2
            median_margin = round(
                (sorted_m[mid] if len(sorted_m) % 2
                 else (sorted_m[mid - 1] + sorted_m[mid]) / 2), 1) \
                if sorted_m else None
            arms.append({
                "arm": arm, "n": n, "wins": wins, "losses": losses,
                "ties": ties,
                "mean_margin": round(sum(seed_margins) / len(seed_margins), 1)
                if seed_margins else None,
                "median_margin": median_margin,
                "win_rate": win_rate, "independent_seeds": True,
                "seated": seated, "incomplete": incomplete,
                "red_seeds": red_seeds[:20],
                "opponent": opponents.get(arm),
                "red": n == 0,
            })
        except Exception as exc:  # 组不可跑→fail-closed 记红
            msg = "%s: %s" % (type(exc).__name__, exc)
            errors.append("%s: %s" % (arm, msg))
            arms.append({"arm": arm, "n": 0, "wins": 0, "losses": 0,
                         "ties": 0, "mean_margin": None, "win_rate": 0.0,
                         "independent_seeds": True, "red": True,
                         "error": msg[:200]})
    return {"arms": arms, "rows": all_rows, "opponents": opponents,
            "seed_base": seed_base, "seated": True,
            "independent_seeds": True, "errors": errors}
