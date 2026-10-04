# -*- coding: utf-8 -*-
"""judge_sheep_league（R20 L1）+ count_shearings（L2）：判决联赛线。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
离线真交易联赛 300-500 局（配置局数）：r37 vs r34a 主对双席位+强对手样本
（分析22 败局对手谱系）+mirror 对；逐局 WL+剪毛刀次+照顾覆盖率；聚合判据
出 evidence JSON。判据（R20 ②）：剪毛 5 刀达成、h2h vs r34a ≥0.55、
胜局对照不翻负；care_rate/feed_rate 为观测指标不进门槛。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence


def judge_sheep_league(r37_pkg: str, r34a_pkg: str, opponents: Sequence[str],
                       n_games: int) -> Dict[str, Any]:
    """300-500 局联赛跑批+逐局 WL/刀次/分组胜率聚合。

    签名意图：输入: r37 包+r34a 包+对手清单+局数配置 / 输出: evidence JSON
    （逐局 WL/刀次/分组胜率） / 错误: fail-closed。

    口径钉（R20 判决联赛编排；实现与测试同钉）：
    - 语义=离线真交易联赛（双席活件对打，非录像开环）：主对 r37 vs r34a
      在飞件 + 强对手样本 + mirror（r37 vs r37）。强对手样本=分析22 败局
      对手谱系（其公开代码不可得），以本仓最强可得件代理（对手清单传入：
      r33 variant_tuned/r30 orderbook_derivative/v48_derivative），evidence
      .method 注明代理关系。
    - 局设计：seed 集显式（evidence.config.arms 记录，逐局可复跑）；每独立
      seed 双席位各一局（r37 坐 seat0 一局+seat1 一局）；**席位翻转不双计**
      ——统计按独立 seed 数 n 报，h2h 判据按独立 seed 算（分析20 playbook
      教训：席位翻转对为同一局镜像重放，有效样本=seed 数）。
    - 局数配置 n_games（可关键字传入）=总对局数（双席计）；须为 ≥2 偶数。
      独立种子预算 budget=n_games//2：强样本各臂与 mirror 各 max(1,
      12.5% 半分四舍五入) 种子，主对吃余数；每臂 ≥1 独立种子否则 ValueError
      （fail-closed）。验收区间 300-500 记 config.in_acceptance_range（观测）。
    - 装载=官方 last-callable 内存 exec 每局全新命名空间（R18 method note，
      phase_b.load_l3_callable 只调用不重写）；r37 逐局全新装载，mirror 局
      两席各一次独立装载（双活件）。
    - 引擎=官方 kaggle_environments kaggriculture 场景，seed 显式逐局传入
      （kgenv.engine.run_episode 同参同语义；为捕获逐局状态行，内联等价
      循环后读 env.steps）。
    - 行来源=对打过程逐步状态行：env.steps[t][seat]（与 replay steps 同构）
      → parse_states._parse_entry，产出 parse_episode_states 同构双席行
      {step, seat, action, money, hands, animals_grid, tiles, inventory}；
      逐局喂 count_shearings 我方席（r37）行——刀次/照顾覆盖率归属 r37 群。
    - 刀次口径（对齐 retape_sheep 术后双不变量①②）：逐局双指标=
      shearings_rounds（剪毛刀轮数=count_shearings shearings.round_count）
      + shearings_per_sheep_min（每羊刀次下限=per_sheep 各只 min；per_sheep
      为 None=按只不可归属→该指标 None，判据臂 fail-closed）。
    - 逐局记录：WL（r37 视角，winner=ours/opp/tie）+双刀次指标+
      care_rate/feed_rate 覆盖率；count_shearings UNKNOWN→该局红
      （fail-closed）；刀次低=判据信号非局错，不标红。
    - 聚合判据（R20 ②，用户批准口径）：①剪毛 5 刀达成=刀轮 min≥5 ∧
      每羊 min≥5（全体局逐局可归属，缺一即红；与 retape 静态核算①②同构）；
      ②联赛 h2h vs r34a ≥0.55——主对 seed 级：胜=两席局皆胜、平=席位分歧
      或皆平、负=皆负，rate=(胜+0.5平)/独立局；无决胜 seed rate=0.0
      fail-closed；③胜局不翻负=胜率判承载（与②同源判定，criteria_notes
      注明，不另设门槛）。care_rate/feed_rate 观测不进门槛；强手带胜率
      +5pp 观测（基线=分析20/22 r34a 强带 ≥90k 胜率 37-16=69.8%，代理臂
      对比仅观测）。刀次分布=min/median/达标率（rounds≥5）双臂（刀轮/每羊）
      +分组胜率（强样本/mirror，同 seed 级口径）入账。
    - overall=criteria ∧ 零红局 ∧ 零 errors（fail-closed）；单局失败（引擎
      抛/装载抛/非终局/count_shearings UNKNOWN）标红计入 errors，不短路全跑。
    - evidence dict 由本函数返回、不落盘（台账写入归实跑编排，防测试覆写
      真台账——R19 judge 同则）；source.rerun_command 记可复跑命令+seed 清单。
    """
    import hashlib
    import os
    import sys
    import time
    from datetime import datetime, timezone

    _ksim = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _ksim not in sys.path:
        sys.path.insert(0, _ksim)   # 兄弟包可从任意 CWD 导入（R19 先例）

    try:
        from orderbook_r37 import parse_states
    except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑
        import parse_states
    from orderbook_surge_lab import phase_b
    import kaggle_environments

    EPISODE_STEPS = 720
    H2H_THRESHOLD = 0.55
    SHEARING_TARGET = 5.0
    STRONG_BASELINE_RATE = 0.698
    STRONG_TARGET_PP = 5.0
    ACCEPTANCE_RANGE = (300, 500)
    MAIN_SEED_BASE, STRONG_SEED_BASE = 1000, 2000
    STRONG_SEED_STRIDE, MIRROR_SEED_BASE = 100, 9000

    def _bad(msg):
        return ValueError(f"联赛输入缺失/不合法：{msg}")

    # ---- 预检输入（fail-closed） -----------------------------------------
    def _abspath(p, label):
        if not isinstance(p, str) or not p.strip():
            raise _bad(f"{label} 非字符串路径：{p!r}")
        ap = os.path.abspath(p)
        if not os.path.isfile(ap):
            raise _bad(f"{label} 文件不存在：{ap}")
        return ap

    r37_path = _abspath(r37_pkg, "r37 包")
    r34a_path = _abspath(r34a_pkg, "r34a 包")
    if isinstance(opponents, (str, bytes)):
        raise _bad(f"opponents 应为路径序列，实为 {type(opponents).__name__}")
    opp_paths = []
    for raw in (opponents or []):
        ap = _abspath(raw, "对手清单条目")
        if ap in opp_paths:
            raise _bad(f"对手清单条目重复：{ap}")
        opp_paths.append(ap)
    if not opp_paths:
        raise _bad("对手清单为空（需强对手样本清单）")
    if isinstance(n_games, bool) or not isinstance(n_games, int):
        raise _bad(f"n_games 应为 int，实为 {n_games!r}")
    if n_games < 2 or n_games % 2:
        raise _bad(f"n_games 须为 ≥2 偶数（每独立 seed 双席位各一局），实为 {n_games!r}")

    # ---- 局数配置→臂/种子（seed 集显式） ---------------------------------
    def _half_up(x):
        return int(x + 0.5)

    budget = n_games // 2
    strong_each = max(1, _half_up(budget * 0.125))
    mirror_n = max(1, _half_up(budget * 0.125))
    main_n = budget - strong_each * len(opp_paths) - mirror_n
    if main_n < 1:
        raise _bad(f"n_games={n_games} 过小：主对/强样本/mirror 每臂至少 1 "
                   f"独立种子×2 席（对手 {len(opp_paths)} 件需 ≥ "
                   f"{2 * (len(opp_paths) + 2)} 局）")
    main_seeds = [MAIN_SEED_BASE + i for i in range(main_n)]
    strong_arms = [{"opponent": p,
                    "seeds": [STRONG_SEED_BASE + j * STRONG_SEED_STRIDE + i
                              for i in range(strong_each)]}
                   for j, p in enumerate(opp_paths)]
    mirror_seeds = [MIRROR_SEED_BASE + i for i in range(mirror_n)]

    plan = []
    for seed in main_seeds:
        for our_seat in (0, 1):
            plan.append({"group": "main", "opponent": r34a_path,
                         "seed": seed, "our_seat": our_seat})
    for arm in strong_arms:
        for seed in arm["seeds"]:
            for our_seat in (0, 1):
                plan.append({"group": "strong", "opponent": arm["opponent"],
                             "seed": seed, "our_seat": our_seat})
    for seed in mirror_seeds:
        for our_seat in (0, 1):
            plan.append({"group": "mirror", "opponent": r37_path,
                         "seed": seed, "our_seat": our_seat})

    # ---- 小工具 ---------------------------------------------------------
    def _num(v):
        return (float(v) if isinstance(v, (int, float))
                and not isinstance(v, bool) else None)

    def _knife_metrics(cnt):
        """count_shearings 输出 → (shearings_rounds, shearings_per_sheep_min)。

        口径=本函数 docstring「刀次口径」：round_count=刀轮；per_sheep 各只
        min=每羊下限（空 dict=0.0 无羊无刀，None=按只不可归属→不可核算）。
        标量 shearings（合成桩/旧口径）退化：两指标同值。UNKNOWN→(None, None)。
        """
        if not isinstance(cnt, dict) or cnt.get("unknown") \
                or cnt.get("verdict") == "UNKNOWN":
            return (None, None)
        v = cnt.get("shearings")
        if not isinstance(v, dict):
            n = _num(v)
            return (n, n) if n is not None else (None, None)
        rounds = _num(v.get("round_count"))
        if rounds is None and isinstance(v.get("rounds"), (list, tuple)):
            rounds = float(len(v["rounds"]))
        if rounds is None:
            rounds = _num(v.get("rounds")) or _num(v.get("per_game"))
        ps = v.get("per_sheep")
        if isinstance(ps, dict):
            vals = [x for x in (_num(x) for x in ps.values()) if x is not None]
            pmin = min(vals) if vals else 0.0
        elif ps is None:
            pmin = None
        else:
            pmin = _num(ps)
        return (rounds, pmin)

    def _median(vals):
        s = sorted(vals)
        n = len(s)
        if not n:
            return None
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0

    def _sha256(path):
        if not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    # ---- 逐局对打（单局失败标红计入，不短路全跑） -------------------------
    def _play(entry):
        rec = {"group": entry["group"], "opponent": entry["opponent"],
               "seed": entry["seed"], "our_seat": entry["our_seat"],
               "red": False, "error": None}
        t0 = time.perf_counter()
        try:
            r37_agent = phase_b.load_l3_callable(r37_path)
            opp_agent = phase_b.load_l3_callable(
                r37_path if entry["group"] == "mirror" else entry["opponent"])
            agents = ([r37_agent, opp_agent] if entry["our_seat"] == 0
                      else [opp_agent, r37_agent])
            env = kaggle_environments.make(
                "kaggriculture",
                configuration={"episodeSteps": EPISODE_STEPS,
                               "seed": int(entry["seed"]),
                               "actTimeout": 60.0},
                debug=True)
            env.run(agents)
            steps = getattr(env, "steps", None)
            if not isinstance(steps, list) or len(steps) < 2:
                raise RuntimeError(
                    f"引擎状态帧异常：frames={0 if not isinstance(steps, list) else len(steps)}")
            rewards = [float(steps[-1][s].get("reward")) for s in (0, 1)]
            statuses = [str(steps[-1][s].get("status")) for s in (0, 1)]
            rows = []
            for t, pair in enumerate(steps):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise RuntimeError(f"引擎状态帧席位异常：steps[{t}]")
                for seat in (0, 1):
                    rows.append(parse_states._parse_entry(t, seat, pair[seat]))
            rec["rewards"] = rewards
            rec["statuses"] = statuses
            rec["margin"] = (rewards[entry["our_seat"]]
                             - rewards[1 - entry["our_seat"]])
            our_rows = [row for row in rows
                        if row.get("seat") == entry["our_seat"]]
            rec["n_rows"] = len(our_rows)
            cnt = count_shearings(our_rows)
            rounds, pmin = _knife_metrics(cnt)
            rec["shearings_rounds"] = rounds
            rec["shearings_per_sheep_min"] = pmin
            rec["care_rate"] = (_num(cnt.get("care_rate"))
                                if isinstance(cnt, dict) else None)
            rec["feed_rate"] = (_num(cnt.get("feed_rate"))
                                if isinstance(cnt, dict) else None)
            if statuses != ["DONE", "DONE"]:
                rec["red"] = True
                rec["note"] = f"非终局 statuses：{statuses}"
            elif rounds is None and pmin is None:
                rec["red"] = True
                rec["note"] = "count_shearings UNKNOWN（刀次不可核算）→fail-closed 红"
            else:
                if rewards[0] > rewards[1]:
                    wseat = 0
                elif rewards[1] > rewards[0]:
                    wseat = 1
                else:
                    wseat = None
                rec["winner_seat"] = wseat
                rec["winner"] = ("tie" if wseat is None
                                 else "ours" if wseat == entry["our_seat"]
                                 else "opp")
        except Exception as exc:  # 单局崩=红局入账，不向上抛（fail-closed 留痕）
            rec["red"] = True
            rec["error"] = f"{type(exc).__name__}: {exc}"
        rec["elapsed_s"] = round(time.perf_counter() - t0, 3)
        return rec

    t0 = time.perf_counter()
    games = [_play(entry) for entry in plan]
    errors = [{"group": g["group"], "opponent": g["opponent"],
               "seed": g["seed"], "our_seat": g["our_seat"],
               "error": g["error"]} for g in games if g.get("error")]

    # ---- 聚合（seed 级=独立局；席位翻转不双计） ---------------------------
    def _block(group_games):
        pairs = {}
        for g in group_games:
            pairs.setdefault(g["seed"], []).append(g)
        run_scores = {"wins": 0, "ties": 0, "losses": 0}
        outcomes = {"win": 0, "draw": 0, "loss": 0, "incomplete": 0}
        for seed in sorted(pairs):
            runs = sorted(pairs[seed], key=lambda r: r["our_seat"])
            for r in runs:
                if r.get("red") or r.get("winner") is None:
                    continue
                if r["winner"] == "ours":
                    run_scores["wins"] += 1
                elif r["winner"] == "tie":
                    run_scores["ties"] += 1
                else:
                    run_scores["losses"] += 1
            if (len(runs) != 2
                    or any(r.get("red") or r.get("winner") is None
                           for r in runs)):
                outcomes["incomplete"] += 1
                continue
            score = sum(1.0 if r["winner"] == "ours"
                        else 0.5 if r["winner"] == "tie" else 0.0
                        for r in runs) / 2.0
            if score == 1.0:
                outcomes["win"] += 1
            elif score == 0.0:
                outcomes["loss"] += 1
            else:
                outcomes["draw"] += 1
        decided = outcomes["win"] + outcomes["draw"] + outcomes["loss"]
        rate = (round((outcomes["win"] + 0.5 * outcomes["draw"]) / decided, 4)
                if decided else 0.0)
        run_decided = (run_scores["wins"] + run_scores["ties"]
                       + run_scores["losses"])
        return {"n_games": len(group_games), "n_independent": len(pairs),
                "seeds": sorted(pairs), "run_scores": run_scores,
                "run_rate": (round((run_scores["wins"]
                                    + 0.5 * run_scores["ties"])
                                   / run_decided, 4) if run_decided else 0.0),
                "seed_outcomes": outcomes, "rate": rate}

    main_games = [g for g in games if g["group"] == "main"]
    strong_games = [g for g in games if g["group"] == "strong"]
    mirror_games = [g for g in games if g["group"] == "mirror"]
    main_b = _block(main_games)
    main_b["h2h_rate"] = main_b["rate"]
    main_b["h2h_threshold"] = H2H_THRESHOLD
    strong_b = _block(strong_games)
    strong_b["per_opponent"] = [
        {"opponent": arm["opponent"],
         **_block([g for g in strong_games if g["opponent"] == arm["opponent"]])}
        for arm in strong_arms]
    strong_b["observation"] = {
        "observation_only": True,
        "rate": strong_b["rate"],
        "baseline_rate": STRONG_BASELINE_RATE,
        "baseline_source": ("分析20/22 r34a 强带（≥90k）胜率 37-16=69.8%"
                            "（败局对手谱系代理臂对比，仅观测不进门槛）"),
        "delta_pp": round((strong_b["rate"] - STRONG_BASELINE_RATE) * 100, 1),
        "target_pp": STRONG_TARGET_PP,
        "meets_target": ((strong_b["rate"] - STRONG_BASELINE_RATE) * 100
                         >= STRONG_TARGET_PP),
    }
    mirror_b = _block(mirror_games)

    def _dist(vals):
        vals = [v for v in vals if v is not None]
        if not vals:
            return {"n": 0, "min": None, "median": None, "achieve_rate": None}
        return {"n": len(vals), "min": min(vals), "median": _median(vals),
                "achieve_rate": round(
                    sum(1 for v in vals if v >= SHEARING_TARGET) / len(vals), 4)}

    def _mean(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    rounds_vals = [g.get("shearings_rounds") for g in games]
    pmin_vals = [g.get("shearings_per_sheep_min") for g in games]
    shearing_b = {
        "threshold": SHEARING_TARGET,
        "rounds": _dist(rounds_vals),
        "per_sheep_min": _dist(pmin_vals),
        "by_group": {grp: {"rounds": _dist([g.get("shearings_rounds")
                                            for g in games
                                            if g["group"] == grp]),
                           "per_sheep_min": _dist(
                               [g.get("shearings_per_sheep_min")
                                for g in games if g["group"] == grp])}
                     for grp in ("main", "strong", "mirror")},
    }
    care_b = {"mean": _mean([g.get("care_rate") for g in games]),
              "by_group": {grp: _mean([g.get("care_rate") for g in games
                                       if g["group"] == grp])
                           for grp in ("main", "strong", "mirror")}}
    feed_b = {"mean": _mean([g.get("feed_rate") for g in games]),
              "by_group": {grp: _mean([g.get("feed_rate") for g in games
                                       if g["group"] == grp])
                           for grp in ("main", "strong", "mirror")}}

    # ---- 判据（R20 ②，用户批准口径） -------------------------------------
    rounds_vals_ok = [v for v in rounds_vals if v is not None]
    pmin_vals_ok = [v for v in pmin_vals if v is not None]
    rounds_arm = bool(rounds_vals_ok) and min(rounds_vals_ok) >= SHEARING_TARGET
    pmin_arm = (len(pmin_vals_ok) == len(games) and bool(pmin_vals_ok)
                and min(pmin_vals_ok) >= SHEARING_TARGET)
    shearing_b["arms"] = {"rounds_min_ge_5": rounds_arm,
                          "per_sheep_min_ge_5": pmin_arm}
    main_decided = sum(main_b["seed_outcomes"][k]
                       for k in ("win", "draw", "loss"))
    crit = {
        "shearings_5_achieved": bool(rounds_arm and pmin_arm),
        "h2h_vs_r34a_ge_055": bool(main_decided > 0
                                   and main_b["h2h_rate"] >= H2H_THRESHOLD),
    }
    crit["win_games_not_flipped"] = crit["h2h_vs_r34a_ge_055"]
    n_red = sum(1 for g in games if g.get("red"))
    overall_pass = bool(all(crit.values()) and not n_red and not errors)

    rerun_cmd = (
        "cd " + _ksim + " && python3 -m pytest orderbook_r37/test_judge_league.py"
        " -q && python3 -c \"import json; from orderbook_r37.judge_league import"
        " judge_sheep_league; ev = judge_sheep_league(" + repr(r37_pkg) + ", "
        + repr(r34a_pkg) + ", " + repr(list(opponents)) + ", n_games="
        + repr(n_games) + "); open('orderbook_r37/evidence/judge_sheep_league"
        ".json', 'w', encoding='utf-8').write(json.dumps(ev, ensure_ascii=False,"
        " indent=1))\"")

    evidence = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pkg_path": r37_path, "pkg_sha256": _sha256(r37_path),
        "r34a_path": r34a_path, "r34a_sha256": _sha256(r34a_path),
        "opponents": [{"path": p, "sha256": _sha256(p)} for p in opp_paths],
        "method": {
            "semantics": ("离线真交易联赛（双席活件对打，非录像开环）：主对 "
                          "r37 vs r34a 在飞件+强对手样本+mirror（r37 vs "
                          "r37）；每独立 seed 双席位各一局，席位翻转不双计"
                          "——统计按独立 seed n 报，h2h 按独立 seed 算"),
            "engine": ("官方 kaggle_environments kaggriculture 场景，seed "
                       "显式逐局传入（kgenv.engine.run_episode 同参同语义；"
                       "为捕获逐局状态行内联等价循环读 env.steps）"),
            "loader": ("官方 last-callable 内存 exec 每局全新命名空间（R18 "
                       "method note，phase_b.load_l3_callable 只调用不重写）"),
            "rows": ("对打过程逐步状态行=parse_episode_states 同构双席行"
                     "（env.steps[t][seat]→parse_states._parse_entry），"
                     "逐局喂 count_shearings 我方席（r37）行"),
            "shearings": ("count_shearings→{shearings:{total,rounds,"
                          "round_count,per_sheep,…},care_rate,feed_rate}；"
                          "逐局双指标=shearings_rounds（刀轮）+"
                          "shearings_per_sheep_min（每羊 min，per_sheep "
                          "None=不可归属→判据臂 fail-closed）；判据=刀轮 "
                          "min≥5 ∧ 每羊 min≥5（对齐 retape_sheep 静态核算"
                          "①②；达标率=rounds≥5 口径）"),
            "h2h": ("主对 seed 级：胜=两席局皆胜、平=席位分歧或皆平、负=皆负；"
                    "rate=(胜+0.5平)/独立局；判据 ≥0.55；无决胜 seed "
                    "rate=0.0 fail-closed"),
            "win_games_not_flipped": ("胜局不翻负=胜率判承载（用户批准口径）："
                                      "由 h2h_vs_r34a_ge_055 同源判定，"
                                      "不另设门槛"),
            "strong_proxy": ("分析22 败局对手谱系公开代码不可得，强对手样本以"
                             "本仓最强可得件代理（r33 variant_tuned/r30 "
                             "orderbook_derivative/v48_derivative）；+5pp "
                             "观测基线=分析20/22 r34a 强带胜率 69.8%"),
            "care_feed": "care_rate/feed_rate 为观测指标，不进门槛",
        },
        "config": {
            "n_games_requested": n_games,
            "n_games_executed": len(games),
            "n_independent_planned": budget,
            "seats_per_seed": 2,
            "acceptance_range": list(ACCEPTANCE_RANGE),
            "in_acceptance_range": bool(ACCEPTANCE_RANGE[0] <= n_games
                                        <= ACCEPTANCE_RANGE[1]),
            "arms": {
                "main": {"opponent": r34a_path, "n_seeds": len(main_seeds),
                         "seeds": main_seeds},
                "strong": [{"opponent": a["opponent"],
                            "n_seeds": len(a["seeds"]), "seeds": a["seeds"]}
                           for a in strong_arms],
                "mirror": {"opponent": r37_path,
                           "n_seeds": len(mirror_seeds),
                           "seeds": mirror_seeds},
            },
        },
        "games": games,
        "aggregate": {"main": main_b, "strong": strong_b, "mirror": mirror_b,
                      "shearings": shearing_b, "care_rate": care_b,
                      "feed_rate": feed_b},
        "overall": {
            "criteria": crit,
            "criteria_notes": {"win_games_not_flipped":
                               "胜局不翻负=胜率判承载：与 h2h_vs_r34a_ge_055 "
                               "同源判定（用户批准口径），不另设门槛"},
            "pass": overall_pass,
            "n_red_games": n_red, "n_errors": len(errors),
            "observations": {"care_rate_mean": care_b["mean"],
                             "feed_rate_mean": feed_b["mean"],
                             "strong_delta_pp":
                                 strong_b["observation"]["delta_pp"]},
        },
        "errors": errors,
        "source": {
            "rerun_command": rerun_cmd,
            "seeds": {"main": main_seeds,
                      "strong": {a["opponent"]: a["seeds"]
                                 for a in strong_arms},
                      "mirror": mirror_seeds},
            "wall_s": round(time.perf_counter() - t0, 1),
            "method_notes": [
                "evidence dict 由本函数返回、不落盘；台账文件归实跑编排写入",
                "seed 集显式固定（config.arms），逐局可复跑",
            ],
        },
    }
    return evidence


def count_shearings(states: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """剪毛刀次统计：数对羊格的动物格 HARVEST（product=WOOL）事件数，按局/
    按只聚合；同出 CARE/FEED 覆盖率（照顾全程观测指标，不进门槛）。

    签名意图：输入: parse_episode_states 输出 /
    输出: {shearings, care_rate, feed_rate} / 错误: 缺字段→UNKNOWN。

    剪毛识别口径（实现与测试同钉；行契约=parse_episode_states 输出逐步双席
    行 {step, seat, action, money, hands, animals_grid, tiles, …}；单元=
    action.farmer（'F'）与 action.hands[i]（'hN'）逐条单元指令，market 订单
    槽不算单元；day=step//24，turnsPerDay=24；先例=retape_sheep.py 链式解剖
    _shear_events/evidence/sheep_tape_dissection.json）：

    - **候选**：每拍 ['HARVEST'] 单元指令=一次候选剪毛。**一刀**=候选中产物
      WOOL 成立者（引擎语义：对羊格 HARVEST，产物 WOOL 入执行者随身）。
    - **链式认领（主口径）**：同席同单元同日（step 严格更后）出现
      ['PLACE','WOOL',…] → 认领该候选为一刀（投放确证产物；Wool 只能来自
      该单元自身羊格 HARVEST，PICKUP WOOL 反向流实测为零——retape_sheep
      先例）。位置不可解析时认领是唯一计刀依据。
    - **单 HARVEST 未见 PLACE WOOL → 按产物推断（选一口径，本实现选定并
      留档）**：单元位置（F=row['farmer']、hN=row['hands'][N]，执行后值；
      HARVEST 不移位）→ 行 animals_grid 该格牲畜=SHEEP → 产物 WOOL 成立，
      计一刀；否则**保守不计**（非羊格=牛/鹅/作物/空格，或位置不可解析），
      全部入 shearings["residuals"] 留档（reason: non_sheep_cell /
      unresolved_position）。弃「保守不计一切未认领候选」口径：会系统性漏计
      批量投放（一拍 PLACE WOOL 覆盖多次 HARVEST 实物常见），且与契约刀次
      定义（对羊格 HARVEST 事件数）相悖。
    - **链认领但羊格直接观测非羊格 → 不计刀（对羊格定义优先）**：该 HARVEST
      未产 WOOL（实证：episode-112938600 席1 (6,2) 空牧栏 HARVEST 被同日
      PLACE WOOL 认领——投放的 WOOL 来自随身存量），reason=
      "chain_contradicted" 留档。
    - **shearings**：{"total": 按局总计刀数（输入行全体）, "rounds": 刀轮=
      剪毛日集合（升序去重）, "round_count", "per_sheep": 按只 {(席,x,y):
      刀数}——从 animals_grid 羊格与单元位置归属；任一刀不可归属（链认领但
      位置不可解析）→ 整体记 None 并入 "unattributed" 留档（不许猜）,
      "residuals": 未计刀候选留档, "unattributed": 已计刀不可归属留档}。
    - **care_rate/feed_rate（观测指标，不进门槛）**：CARE/FEED 指令覆盖率。
      牲畜日=该席该日任一拍 animals_grid 非空；单元日=(席,单元,日) 该单元
      该日有 ≥1 条单元指令；分母=牲畜日上的全体单元日，分子=其中该单元该日
      执行过 ['CARE']（['FEED']）的单元日；比例=分子/分母，分母为 0→None。
    - **错误**：任一行缺关键字段（step/seat/action）、非 dict、step/seat 非
      整型、action 非 dict，或输入为空 → {"shearings": None, "care_rate":
      None, "feed_rate": None, "unknown": True, "verdict": "UNKNOWN"}（与
      replay_guard_verdict 的 UNKNOWN 风格一致，不抛）。animals_grid/hands/
      farmer 等观察子键缺省按空处理，不触发 UNKNOWN。
    """
    turns_per_day = 24

    def _units(action: Any):
        """动作 → [(unit_id, 单元指令)]；'F'=farmer、'hN'=hands 下标。"""
        farmer = action.get("farmer")
        if isinstance(farmer, list) and farmer and isinstance(farmer[0], str):
            yield "F", farmer
        for i, hand in enumerate(action.get("hands") or []):
            if isinstance(hand, list) and hand and isinstance(hand[0], str):
                yield "h%d" % i, hand

    def _unit_pos(row: Dict[str, Any], unit: str) -> Any:
        """单元执行后位置 (x, y)（HARVEST 不移位=收割格位）；不可解析→None。"""
        if unit == "F":
            pos = row.get("farmer")
        else:
            hands = row.get("hands")
            idx = int(unit[1:])
            if not isinstance(hands, list) or idx >= len(hands):
                return None
            pos = hands[idx]
        if isinstance(pos, (list, tuple)) and len(pos) == 2 \
                and not isinstance(pos[0], bool) and not isinstance(pos[1], bool) \
                and isinstance(pos[0], int) and isinstance(pos[1], int):
            return (pos[0], pos[1])
        return None

    def _animal_name(entry: Any) -> Any:
        if isinstance(entry, dict):
            name = entry.get("type", entry.get("animal"))
            return name if isinstance(name, str) and name else None
        return entry if isinstance(entry, str) and entry else None

    rows = list(states or [])
    unknown = False
    beats: list = []
    for row in rows:
        if not isinstance(row, dict):
            unknown = True
            continue
        if "step" not in row or "seat" not in row or "action" not in row:
            unknown = True
            continue
        step, seat, action = row["step"], row["seat"], row["action"]
        if isinstance(step, bool) or not isinstance(step, int) \
                or isinstance(seat, bool) or not isinstance(seat, int) \
                or not isinstance(action, dict):
            unknown = True
            continue
        beats.append((step, seat, row))
    if unknown or not beats:
        return {"shearings": None, "care_rate": None, "feed_rate": None,
                "unknown": True, "verdict": "UNKNOWN"}

    # 拍内单元指令展开 + 链式认领账（PLACE 'WOOL' 步点按 席/单元/日 归档）
    wool_places: Dict[Any, list] = {}
    candidates: list = []       # HARVEST 候选（含格位判定原料）
    care_days: set = set()      # (席, 单元, 日) 执行过 CARE
    feed_days: set = set()      # (席, 单元, 日) 执行过 FEED
    active_days: set = set()    # (席, 单元, 日) 有指令
    livestock_days: set = set() # (席, 日) 有牲畜格
    for step, seat, row in beats:
        day = step // turns_per_day
        grid = row.get("animals_grid")
        if isinstance(grid, dict) and grid:
            livestock_days.add((seat, day))
        for unit, op in _units(action=row["action"]):
            active_days.add((seat, unit, day))
            kind = op[0] if op else None
            if kind == "HARVEST":
                candidates.append({"step": step, "seat": seat, "unit": unit,
                                   "day": day, "pos": _unit_pos(row, unit),
                                   "grid": grid if isinstance(grid, dict) else {}})
            elif kind == "PLACE" and len(op) > 1 and op[1] == "WOOL":
                wool_places.setdefault((seat, unit, day), []).append(step)
            elif kind == "CARE":
                care_days.add((seat, unit, day))
            elif kind == "FEED":
                feed_days.add((seat, unit, day))
    for steps_list in wool_places.values():
        steps_list.sort()

    cuts: list = []
    residuals: list = []
    unattributed: list = []
    for cand in sorted(candidates, key=lambda c: (c["step"], c["seat"], c["unit"])):
        claimed = any(p > cand["step"]
                      for p in wool_places.get((cand["seat"], cand["unit"],
                                                cand["day"]), []))
        cell = _animal_name(cand["grid"].get(cand["pos"])) if cand["pos"] else None
        if cell == "SHEEP":
            cuts.append({**cand, "cell": cand["pos"]})
        elif cell is None and cand["pos"] is None and claimed:
            # 位置不可解析、链认领确证产物 WOOL → 计刀但按只不可归属
            cuts.append({**cand, "cell": None})
            unattributed.append({"step": cand["step"], "seat": cand["seat"],
                                 "unit": cand["unit"], "day": cand["day"],
                                 "reason": "unresolved_position"})
        else:
            if claimed:
                reason = "chain_contradicted"   # 链认领但羊格观测非羊格
            elif cand["pos"] is None:
                reason = "unresolved_position"  # 保守分支：产物不可推断
            else:
                reason = "non_sheep_cell"       # 保守分支：非羊产物
            residuals.append({"step": cand["step"], "seat": cand["seat"],
                              "unit": cand["unit"], "day": cand["day"],
                              "reason": reason})

    rounds = sorted({c["day"] for c in cuts})
    per_sheep: Any = None
    if not unattributed:
        per_sheep = {}
        for cut in cuts:
            key = (cut["seat"], cut["cell"][0], cut["cell"][1])
            per_sheep[key] = per_sheep.get(key, 0) + 1

    def _rate(done: set) -> Any:
        eligible = {(s, u, d) for (s, u, d) in active_days
                    if (s, d) in livestock_days}
        if not eligible:
            return None
        return len(eligible & done) / len(eligible)

    return {
        "shearings": {
            "total": len(cuts),
            "rounds": rounds,
            "round_count": len(rounds),
            "per_sheep": per_sheep,
            "residuals": residuals,
            "unattributed": unattributed,
        },
        "care_rate": _rate(care_days),
        "feed_rate": _rate(feed_days),
        "unknown": False,
        "verdict": None,
    }
