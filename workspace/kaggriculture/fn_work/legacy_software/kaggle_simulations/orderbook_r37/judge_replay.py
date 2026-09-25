# -*- coding: utf-8 -*-
"""judge_cash_guard_replay（R19 L1）+ replay_guard_verdict（L2）：判决重演线。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
本地官方引擎重放 6 局灾难局（112938600/112968467/112976582/113002280/
113094793/113099386）+10 胜局对照（同窗抽样），r37 件对原局实况逐局双席位
各演一遍（排除座位效应）；逐局三指标（d2 前牲畜逃走/BUY_ANIMAL 失败/
d1 h0 现金）+对照终局资金差。判据（R19 ②）：死牛 0、买牲畜失败 0、
d1 h0 现金≥4、对照资金 l1 非负。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence


def judge_cash_guard_replay(pkg_path: str, corpus: Sequence[str]) -> Dict[str, Any]:
    """6 灾难局+10 对照局重放并聚合三指标出 evidence JSON。

    签名意图：输入: r37 包+语料局单 / 输出: evidence JSON（逐局三指标+对照
    终局资金差） / 错误: 单局重放失败标红计入，不短路全跑。

    口径钉（R19 判决重演编排；实现与测试同钉）：
    - 语义=r37 活件 vs 原局对手的录像动作（开环，R15 先例）；同局双席位各
      演一遍（r37 坐我方席一局+坐对手席一局互换，排除座位效应）；装载=
      官方 last-callable 内存 exec 每局全新命名空间（R18 method note，
      phase_b.load_l3_callable 只调用不重写）；引擎=twin 前向走子
      （agent.planner.twin，保真已验：全录像动作流逐拍与 replay 逐位一致）。
    - 语料条目 corpus[i]：全数字段=episode id（replay 按
      /tmp/r33audit→/tmp/kagr22 缓存查找，缺则 kaggle CLI 拉至 /tmp/kagr22）；
      含路径/".json"=replay 文件直用（测试注入面）。条目级预检不合法/文件
      缺失→ValueError（语料缺失/不合法，报错含条目）；单局重放（拉取/解析/
      装载/twin 重演/verdict）失败→标红计入 errors，不短路全跑。
    - 灾难/对照分席：episode id ∈ 固定灾难局 6 件（112938600/112968467/
      112976582/113002280/113094793/113099386）→灾难局；其余→对照局。
    - baseline_final：对照局=原局实况该席终局资金（replay 原始记录末拍
      farms[seat].money，经 parse_episode_states 取，与 rewards 核对入账）；
      逐席自比（r37 坐哪席就与该席原局实况比）；灾难局不传基线
      （final_delta=None，三指标为判据）。
    - 逐局三指标=replay_guard_verdict（行契约=parse_episode_states 同构双席
      行；rerun 行 step=原生 si、money=farms[seat].money 执行后值、action=该
      拍执行动作（si=0 取 replay 头拍记录，si≥1=twin 走子执行对），行席位标
      0/1 整数、our_seat=r37 坐席）。
    - 聚合判据（R19 ②）：灾难臂=三指标实数——died_before_d2 合计=0、
      buy_failed 合计=0、cash_d1h0 全跑 min≥4；对照臂=「对照资金 l1 非负」
      ——l1=被测件终局资金差（r37−实况）逐局逐席 min≥0（不劣于原版/胜局不
      翻负口径，R10「逐局终局资金 l1≥verbatim（结果面非负）」同源用语）；
      合计口径（final_delta sum）作敏感度并列入账。overall=四判据 ∧ 零红局
      ∧ 零 errors（fail-closed）。
    - evidence（返回 dict，不落盘——台账写入归编排/实跑，防测试覆写真台账）：
      {generated_at, pkg_path/sha256, method, corpus(语料清单), games(逐局
      三指标+对照资金差), aggregate, overall, errors, source(可复跑命令)}。
    """
    import hashlib
    import json
    import os
    import re
    import subprocess
    import sys
    import time
    from datetime import datetime, timezone

    _ksim = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _ksim not in sys.path:
        sys.path.insert(0, _ksim)   # 兄弟包可从任意 CWD 导入（R20 先例）

    disaster_ids = (112938600, 112968467, 112976582,
                    113002280, 113094793, 113099386)
    cache_dirs = ("/tmp/r33audit", "/tmp/kagr22")
    pull_dir = "/tmp/kagr22"
    kaggle_bin = "/home/renyxin/.local/bin/kaggle"
    episode_re = re.compile(r"episode-(\d+)-replay\.json$")

    try:
        from orderbook_r37 import parse_states
    except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑
        import parse_states
    from agent.planner import twin
    from orderbook_surge_lab import phase_b

    def _bad_corpus(msg):
        return ValueError(f"语料缺失/不合法：{msg}")

    # ---- 预检语料（条目级；不合法即抛，报错含条目） -----------------------
    if not corpus:
        raise _bad_corpus("corpus 为空（需 6 灾难局+10 对照局语料局单）")
    entries = []
    seen = set()
    for raw in corpus:
        if not isinstance(raw, str) or not raw.strip():
            raise _bad_corpus(f"条目非字符串路径/局号：{raw!r}")
        item = raw.strip()
        is_path = (os.sep in item or item.endswith(".json"))
        if is_path:
            path = os.path.abspath(item)
            if not os.path.isfile(path):
                raise _bad_corpus(f"replay 文件不存在：{path}")
            m = episode_re.search(os.path.basename(path))
            ep_guess = int(m.group(1)) if m else None
            entries.append({"entry": item, "kind": "path", "path": path,
                            "episode_guess": ep_guess})
        else:
            if not item.isdigit():
                raise _bad_corpus(f"条目既非局号亦非 replay 路径：{item!r}")
            entries.append({"entry": item, "kind": "episode",
                            "episode_guess": int(item), "path": None})
        key = entries[-1]["episode_guess"], entries[-1]["path"]
        if key in seen:
            raise _bad_corpus(f"语料条目重复：{item!r}")
        seen.add(key)

    def _resolve_replay(entry):
        """episode id → replay 路径（缓存→kaggle CLI 拉）；path 直用。"""
        if entry["kind"] == "path":
            return entry["path"], "given", None
        ep = entry["episode_guess"]
        for d in cache_dirs:
            cand = os.path.join(d, f"episode-{ep}-replay.json")
            if os.path.isfile(cand) and os.path.getsize(cand) > 1000:
                return cand, "cache", None
        os.makedirs(pull_dir, exist_ok=True)
        target = os.path.join(pull_dir, f"episode-{ep}-replay.json")
        env = os.environ.copy()
        try:
            tok = subprocess.run([kaggle_bin, "auth", "print-access-token"],
                                 capture_output=True, text=True, timeout=60)
            if tok.returncode == 0 and tok.stdout.strip():
                env["KAGGLE_API_TOKEN"] = tok.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass  # 无 token 注入则走默认 kaggle.json 凭证（429 回退口径）
        for _attempt in (1, 2):
            try:
                p = subprocess.run(
                    [kaggle_bin, "competitions", "replay", str(ep),
                     "-p", pull_dir],
                    capture_output=True, text=True, timeout=600, env=env)
            except (OSError, subprocess.SubprocessError) as exc:
                p = None
                pull_err = f"{type(exc).__name__}: {exc}"
            else:
                pull_err = (p.stderr or "").strip()[-200:]
            if (p is not None and p.returncode == 0 and os.path.isfile(target)
                    and os.path.getsize(target) > 1000):
                return target, "pulled", None
            time.sleep(5)
        return target, "pull_failed", pull_err or "kaggle competitions replay 失败"

    def _extract_rows(state, actions, our_labels):
        """twin 状态+该拍动作对 → parse 同构双席行（si 由调用方定）。"""
        farms = state.seats[0].observation.farms
        rows = []
        for i in range(2):
            farm = farms[i]
            animals, tiles = parse_states._extract_grids(
                f"farms[{i}].tiles", farm.get("tiles"))
            rows.append({"step": actions[0], "seat": i,
                         "action": actions[1][i],
                         "money": farm.get("money"),
                         "hands": farm.get("hands"),
                         "farmer": farm.get("farmer"),
                         "animals_grid": animals, "tiles": tiles,
                         "_label": our_labels[i]})
        return rows

    def _run_seat(replay, agent, seat, steps0):
        """单局单席 seated 重演（对手=录像开环），产逐步双席行。"""
        bundle = twin.load_engine()
        state = twin.build_state_from_replay(replay, 0, bundle)
        recorded = twin.replay_transition_actions(replay)
        if not recorded:
            raise ValueError("replay 无转移动作流")
        labels = ("seat0", "seat1")
        rows = _extract_rows(state, (0, steps0), labels)
        taken = 0
        while not state.env.done and taken < len(recorded):
            obs = phase_b._obs_dict(state, seat)
            mine = agent(obs)
            pair = [recorded[taken][1 - seat]] * 2
            pair[seat] = mine
            twin.step(state, pair)
            taken += 1
            rows.extend(_extract_rows(state, (taken, pair), labels))
        return rows

    def _pull_command(ep):
        return (f"KAGGLE_API_TOKEN=$({kaggle_bin} auth print-access-token "
                f"2>/dev/null) {kaggle_bin} competitions replay {ep} "
                f"-p {pull_dir}")

    # ---- 逐局重演（单局失败标红计入，不短路全跑） -------------------------
    t0 = time.perf_counter()
    games, errors = [], []
    corpus_listing = []
    for entry in entries:
        ep_guess = entry["episode_guess"]
        rec = {"entry": entry["entry"], "entry_kind": entry["kind"],
               "episode": ep_guess}
        try:
            path, source, pull_err = _resolve_replay(entry)
            rec["replay_path"] = path
            rec["replay_source"] = source
            if source == "pull_failed":
                raise RuntimeError(f"replay 拉取失败：{pull_err}")
            with open(path, "r", encoding="utf-8") as fh:
                replay = json.load(fh)
            ep = int((replay.get("info") or {}).get("EpisodeId") or ep_guess)
            rec["episode"] = ep
            teams = list((replay.get("info") or {}).get("TeamNames") or [])
            kind = "disaster" if ep in disaster_ids else "control"
            rec["kind"] = kind
            # 基线：原局实况逐席终局资金（replay 原始记录末拍，rewards 核对）
            base_rows = parse_states.parse_episode_states(path)
            baseline = {}
            for row in base_rows:
                baseline[row["seat"]] = row["money"]
            rewards = replay.get("rewards")
            rec["baseline_final"] = {str(k): v for k, v in baseline.items()}
            if isinstance(rewards, list) and len(rewards) == 2:
                rec["rewards"] = [float(x) for x in rewards]
            steps0 = [(replay["steps"][0][i] or {}).get("action")
                      for i in range(2)]
            runs, game_red, game_err = {}, False, None
            for seat in (0, 1):
                try:
                    agent = phase_b.load_l3_callable(pkg_path)
                    rows = _run_seat(replay, agent, seat, steps0)
                    base = baseline.get(seat) if kind == "control" else None
                    verd = replay_guard_verdict(rows, baseline_final=base,
                                                our_seat=seat)
                    is_red = verd["verdict"] == "UNKNOWN"
                    runs["seat%d" % seat] = {
                        "r37_seat": seat, "our_seat": seat,
                        "teams": teams,
                        "died_before_d2": verd["died_before_d2"],
                        "buy_failed": verd["buy_failed"],
                        "cash_d1h0": verd["cash_d1h0"],
                        "final_delta": verd["final_delta"],
                        "baseline_final": base,
                        "verdict": verd["verdict"], "red": is_red,
                        "n_rows": len(rows)}
                    game_red = game_red or is_red
                except Exception as exc:  # 单席失败=红局入账
                    runs["seat%d" % seat] = {
                        "r37_seat": seat, "our_seat": seat, "teams": teams,
                        "error": f"{type(exc).__name__}: {exc}", "red": True}
                    game_red = True
                    game_err = f"{type(exc).__name__}: {exc}"
            game = {"episode": ep, "kind": kind, "teams": teams,
                    "replay_path": path, "replay_source": source,
                    "runs": runs, "red": game_red, "error": game_err}
        except Exception as exc:  # 单局重放失败标红计入，不短路全跑
            rec["kind"] = ("disaster" if ep_guess in disaster_ids
                           else "control")
            rec["red"] = True
            rec["error"] = f"{type(exc).__name__}: {exc}"
            game = {"episode": ep_guess, "kind": ("disaster"
                    if ep_guess in disaster_ids else "control"),
                    "replay_path": entry.get("path"), "runs": {},
                    "red": True, "error": rec["error"]}
        corpus_listing.append(rec)
        games.append(game)
        if game.get("red") and game.get("error"):
            errors.append({"episode": game.get("episode"),
                           "error": game["error"]})

    # ---- 聚合（三指标实数+对照资金 l1） -----------------------------------
    def _runs_of(kind):
        out = []
        for g in games:
            if g.get("kind") != kind:
                continue
            for key in ("seat0", "seat1"):
                r = (g.get("runs") or {}).get(key)
                if r and not r.get("red") and r.get("error") is None:
                    out.append((g["episode"], key, r))
        return out

    d_runs = _runs_of("disaster")
    c_runs = _runs_of("control")
    died_sum = sum(int(r["died_before_d2"]) for _, _, r in d_runs)
    buy_sum = sum(int(r["buy_failed"]) for _, _, r in d_runs)
    cash_vals = [r["cash_d1h0"] for _, _, r in d_runs
                 if isinstance(r["cash_d1h0"], (int, float))]
    cash_min = min(cash_vals) if cash_vals else None
    deltas = [(ep, key, r["final_delta"]) for ep, key, r in c_runs
              if isinstance(r["final_delta"], (int, float))]
    delta_min = min((d for _, _, d in deltas), default=None)
    delta_sum = round(sum(d for _, _, d in deltas), 2) if deltas else None
    n_red = sum(1 for g in games if g.get("red"))
    crit = {
        "died_before_d2_zero": died_sum == 0,
        "buy_failed_zero": buy_sum == 0,
        "cash_d1h0_ge_4": (cash_min is not None and cash_min >= 4),
        "control_final_delta_nonneg": (delta_min is not None
                                       and delta_min >= 0),
    }
    overall_pass = bool(all(crit.values()) and not n_red and not errors)

    def _sha256(path):
        if not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    evidence = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pkg_path": os.path.abspath(pkg_path),
        "pkg_sha256": _sha256(os.path.abspath(pkg_path)),
        "method": {
            "semantics": ("r37 活件 vs 原局对手录像动作（开环）；逐局双席位各演"
                          "一遍（r37 坐我方席/对手席互换各一局，排除座位效应）"),
            "loader": "官方 last-callable 内存 exec 每局全新命名空间（R18 method note）",
            "engine": ("agent.planner.twin 前向走子（保真实测：全录像动作流逐拍"
                       "与 replay 逐位一致、终局资金=rewards）"),
            "baseline": ("对照局 baseline_final=原局实况该席终局资金（replay 原始"
                         "记录末拍 farms[seat].money），逐席自比；灾难局不传基线"),
            "l1": ("对照资金 l1 非负=l1（被测件终局资金差 r37−实况）逐局逐席 "
                   "min≥0（不劣于原版/胜局不翻负口径）；合计口径 sum 作敏感度入账"),
            "rows": ("rerun 行=parse_episode_states 同构双席行（step=原生 si、"
                     "money=执行后值、action=该拍执行动作），verdict=同文件 L2"),
        },
        "corpus": {"entries": corpus_listing,
                   "disaster_ids": list(disaster_ids),
                   "n_disaster": sum(1 for g in games
                                     if g.get("kind") == "disaster"),
                   "n_control": sum(1 for g in games
                                    if g.get("kind") == "control")},
        "games": games,
        "aggregate": {
            "disaster": {"n_games": sum(1 for g in games
                                        if g.get("kind") == "disaster"),
                         "n_runs": len(d_runs),
                         "died_before_d2_sum": died_sum,
                         "buy_failed_sum": buy_sum,
                         "cash_d1h0_min": cash_min,
                         "cash_d1h0_values": cash_vals},
            "control": {"n_games": sum(1 for g in games
                                       if g.get("kind") == "control"),
                        "n_runs": len(c_runs),
                        "final_delta_l1_min": delta_min,
                        "final_delta_sum_sensitivity": delta_sum,
                        "final_delta_per_run": [
                            {"episode": ep, "seat": key, "final_delta": d}
                            for ep, key, d in deltas],
                        "n_negative": sum(1 for _, _, d in deltas if d < 0)},
        },
        "overall": {"pass": overall_pass, "criteria": crit,
                    "n_red_games": n_red, "n_errors": len(errors)},
        "errors": errors,
        "source": {
            "rerun_command": ("cd " + os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))) + " && python3 -m pytest "
                "orderbook_r37/test_judge_replay.py -q && python3 -c "
                "\"from orderbook_r37.judge_replay import judge_cash_guard_replay; "
                "import json; print(json.dumps(judge_cash_guard_replay("
                "'orderbook_r37/build/main.py', CORPUS), ensure_ascii=False))\""),
            "replay_pull_command": _pull_command("<episode_id>"),
            "replay_cache_dirs": list(cache_dirs),
            "replay_pull_dir": pull_dir,
            "method_notes": [
                "对照局=analysis20_rows.json r34a 胜局同窗抽样（固定 rng 记 "
                "evidence 的 sampling 块，实跑编排写台账时随附）",
                "evidence dict 由本函数返回、不落盘；台账文件归实跑编排写入",
            ],
            "wall_s": round(time.perf_counter() - t0, 1),
        },
    }
    return evidence


def replay_guard_verdict(
    states: Sequence[Dict[str, Any]],
    baseline_final: Any = None,
    *,
    our_seat: Any = "renyxin",
) -> Dict[str, Any]:
    """单局三指标核算：d2 前牲畜逃走计数（格上牲畜消失+consecutive_unfed
    轨迹吻合）、BUY_ANIMAL 失败计数（提交后未成交）、d1 h0 现金值；对照局加
    终局资金差（r37−实况）。

    签名意图：输入: parse_episode_states 输出 /
    输出: {died_before_d2, buy_failed, cash_d1h0, final_delta, verdict} /
    错误: 缺字段→verdict=UNKNOWN。

    口径钉（实现与测试同钉；行契约=parse_episode_states 输出逐步双席行
    {step, seat, action, money, hands, animals_grid, tiles, …}）：
    - 席位：逐行按 seat 分席，对手席整行不计；默认我方席="renyxin"（席位名
      从行取，可参数化 our_seat）。day=step//24（turnsPerDay=24）。
    - animals_grid={(x,y): 牲畜条目}，条目 type=牲畜名（缺省回退 animal），
      consecutive_unfed/fed_today 子键有则带、缺即省略。
    - died_before_d2：同席相邻拍某 (x,y) 由有牲畜变无牲畜=消失；饿逃轨迹
      吻合=该牲畜 consecutive_unfed 达逃走线（引擎日结：未喂 +1、≥2 逃走；
      观测最大 ≥2 或末见 ≥1——末见 1 经日结终跳即达 2，末见 0 判非饿逃）。
      行全程未带该子键→FEED 推断：日结日对（day(末见拍)−1、day(末见拍)）
      两日全席 FEED 动作 0=连续两日无 FEED（FEED 无格位信息，退化席级）。
      d2 前窗口=末见拍/首缺拍任一 day<2（日界穿越计入——analysis22 死亡戳
      day2,h0 为观测拍，事件在 d1 日结，灾难死牛恰此形）。
    - buy_failed：我方动作含 BUY_ANIMAL 单（逐单计）。成交判据=对照前后
      money+animals_grid：前=提交拍的前一拍（动作观测源拍），后=提交拍与
      下一拍（兼容动作生效拍口径）；钱扣（money 下降）或该牲畜上格
      （animals_grid 该牲畜头数增加）任一出现=成交，全程皆无=静默丢弃计入。
    - cash_d1h0：step==24 拍（d1 hour0）我方 money（该拍执行后值）。
    - final_delta：终局资金差=r37 终局 money−实况基线；基线取可选第二参
      baseline_final（签名微调登记；裁定弃「行首携带 baseline 元数据」选项，
      两者选一以此为准）；无基线→None。终局 money=我方末拍 money。
    - verdict={"pass": died_before_d2==0 and buy_failed==0 and cash_d1h0>=4}；
      缺关键字段（step/seat/money/action/animals_grid）或缺 step 24 拍
      →verdict="UNKNOWN"（不抛；缺字段时指标尽力核算、钱臂不参与）。
    """
    turns_per_day = 24
    d1_h0_step = 24
    escape_line = 2
    pass_cash_min = 4

    def _animal_name(entry: Any) -> Any:
        if isinstance(entry, dict):
            name = entry.get("type", entry.get("animal"))
            return name if isinstance(name, str) and name else None
        return entry if isinstance(entry, str) and entry else None

    def _grid_map(grid: Any) -> Dict[Any, Any]:
        out: Dict[Any, Any] = {}
        if isinstance(grid, dict):
            for key, entry in grid.items():
                if isinstance(key, (tuple, list)) and len(key) == 2:
                    out[(key[0], key[1])] = entry
        elif isinstance(grid, (list, tuple)):
            for entry in grid:
                if isinstance(entry, dict) and "x" in entry and "y" in entry:
                    out[(entry["x"], entry["y"])] = entry
        return out

    def _iter_ops(action: Any) -> Any:
        if isinstance(action, dict):
            for value in action.values():
                yield from _iter_ops(value)
        elif isinstance(action, (list, tuple)):
            if action and isinstance(action[0], str):
                yield list(action)
            else:
                for value in action:
                    yield from _iter_ops(value)

    def _count_animals(grid: Dict[Any, Any], item: Any) -> int:
        n = 0
        for entry in grid.values():
            name = _animal_name(entry)
            if name is not None and (item is None or name == item):
                n += 1
        return n

    def _is_num(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    unknown = False
    beats = []
    for row in (states or []):
        if not isinstance(row, dict) or "step" not in row or "seat" not in row:
            unknown = True
            continue
        if row["seat"] != our_seat:
            continue
        for key in ("money", "action", "animals_grid"):
            if key not in row or row[key] is None:
                unknown = True
        money = row.get("money")
        if not _is_num(money):
            unknown = True
            money = None
        beats.append({
            "step": row["step"],
            "day": row["step"] // turns_per_day,
            "money": money,
            "grid": _grid_map(row.get("animals_grid")),
            "ops": list(_iter_ops(row.get("action"))),
        })
    beats.sort(key=lambda beat: beat["step"])

    # 1) d2 前牲畜逃走：格上牲畜消失 + 饿逃轨迹吻合 + day<2 窗口。
    died_before_d2 = 0
    alive: Dict[Any, Dict[str, Any]] = {}
    feed_days: set = set()
    for idx, beat in enumerate(beats):
        if any(op[0] == "FEED" for op in beat["ops"]):
            feed_days.add(beat["day"])
        grid = beat["grid"]
        if idx > 0:
            prev = beats[idx - 1]
            for pos, info in list(alive.items()):
                if _animal_name(grid.get(pos)) is not None:
                    continue
                if info["saw_cu"]:
                    hunger = (info["max_cu"] >= escape_line
                              or info["last_cu"] >= 1)
                else:
                    day_end = prev["day"]
                    hunger = ((day_end - 1) not in feed_days
                              and day_end not in feed_days)
                if hunger and (prev["day"] < 2 or beat["day"] < 2):
                    died_before_d2 += 1
                del alive[pos]
        for pos, entry in grid.items():
            if _animal_name(entry) is None:
                continue
            info = alive.get(pos)
            if info is None:
                info = {"max_cu": 0, "last_cu": 0, "saw_cu": False}
                alive[pos] = info
            cu = entry.get("consecutive_unfed") if isinstance(entry, dict) else None
            if _is_num(cu):
                info["saw_cu"] = True
                info["max_cu"] = max(info["max_cu"], int(cu))
                info["last_cu"] = int(cu)

    # 2) BUY_ANIMAL 失败：逐单对照前后 money+animals_grid，全程无成交痕迹=丢单。
    buy_failed = 0
    for idx, beat in enumerate(beats):
        buys = [op for op in beat["ops"] if op[0] == "BUY_ANIMAL"]
        if not buys:
            continue
        prev = beats[idx - 1] if idx > 0 else beat
        nxt = beats[idx + 1] if idx + 1 < len(beats) else beat
        for op in buys:
            item = op[1] if len(op) > 1 and isinstance(op[1], str) else None
            pre_m, now_m, next_m = prev["money"], beat["money"], nxt["money"]
            money_dropped = ((now_m is not None and pre_m is not None
                              and now_m < pre_m)
                             or (next_m is not None and pre_m is not None
                                 and next_m < pre_m))
            c_pre = _count_animals(prev["grid"], item)
            on_grid = (_count_animals(beat["grid"], item) > c_pre
                       or _count_animals(nxt["grid"], item) > c_pre)
            if not (money_dropped or on_grid):
                buy_failed += 1

    # 3) d1 h0 现金（step 24 拍执行后值）。
    cash_d1h0 = None
    for beat in beats:
        if beat["step"] == d1_h0_step and beat["money"] is not None:
            cash_d1h0 = beat["money"]
            break

    # 4) 对照终局资金差（r37−实况）。
    final_delta = None
    if baseline_final is not None and beats and beats[-1]["money"] is not None:
        final_delta = beats[-1]["money"] - baseline_final

    if unknown or cash_d1h0 is None:
        verdict: Any = "UNKNOWN"
    else:
        verdict = {"pass": died_before_d2 == 0 and buy_failed == 0
                   and cash_d1h0 >= pass_cash_min}
    return {"died_before_d2": died_before_d2, "buy_failed": buy_failed,
            "cash_d1h0": cash_d1h0, "final_delta": final_delta,
            "verdict": verdict}
