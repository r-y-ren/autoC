# -*- coding: utf-8 -*-
"""judge_predict_replay（R21 L1→R22 改造）+ flip_stats（L2→v2）+
make_counter_opponent（R22 改4）：判决线。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】+【R22 增补·判决段】）：
重放 26 败局（starve strip 语料；晚段崩 15 局为重点）+10 胜局对照，活件
对原局实况逐局双席位各演一遍；聚合判据出 evidence；闭环副证（h2h vs
r37 主对+r34a 辅对，独立 seed n、席位翻转不双计）+**反制模拟臂**（
make_counter_opponent 件 8-16 局×2：r39 与 r37 各对打同配置反制件）。
判据（R22 六判据）：①胜局对照不翻负 ∧ ②晚崩局翻正 ≥1/3 ∧ ③闭环 h2h
≥0.55 ∧ ④动作降量（预测写入合计≤1000、dodge 推迟语义=0）∧ ⑤反制臂胜率
不降（r39 vs 反制 ≥ r37 vs 反制）∧ ⑥realized 价不跌（草莓 delta_px≥0）。
"""
from __future__ import annotations

from typing import Any, Dict, Sequence

# 撞车品项优先序（R21 契约：STRAWBERRY 优先，其次 MILK/WOOL/MELON）
COLLISION_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON")


def judge_predict_replay(pkg_path: str, corpus: Sequence[str],
                         bench: Any = None) -> Dict[str, Any]:
    """26 败局+10 对照重演+闭环副证+反制模拟臂，聚合六判据出 evidence JSON。

    签名意图：输入: r39 包+语料局单+副证配置 / 输出: evidence JSON（逐局翻转/
    realized 价/避让次数/动作降量面/副证 h2h/反制臂） / 错误: 单局失败标红
    计入不短路。

    口径钉（R21 判决编排；实现与测试同钉）：
    - 语义=活件（r39）vs 原局对手录像动作（开环，R15/R19 先例）；逐局双席位各
      演一遍（r38 坐席0 一局+坐席1 一局互换，排除座位效应）；装载=官方
      last-callable 内存 exec 每局全新命名空间（R18 method note，
      phase_b.load_l3_callable 只调用不重写；活件末 callable=_predict_agent）；
      引擎=agent.planner.twin 前向走子（R19 judge_replay 同款，保真已验）。
    - 语料条目 corpus[i]：全数字=episode id（replay 按 /tmp/kagr24→
      /tmp/kagr22→/tmp/r33audit 缓存查找，缺则 kaggle CLI 拉至 /tmp/kagr24：
      先注入 KAGGLE_API_TOKEN，遇 429/失败退回默认凭证再试一次）；含路径分隔
      符或".json"=replay 文件直用（测试注入面）。条目级预检不合法/文件缺失/
      重复→ValueError（语料缺失/不合法，报错含条目）；单局重放（拉取/解析/
      装载/twin 重演/flip_stats/闭环局）失败→标红计入 errors，不短路全跑。
    - 语料分席（胜局对照臂 vs 败局臂）：按原局实况结局判——replay rewards
      我方队（TeamNames 含 "renyxin"，缺则席0）终局资金 < 对席→kind="loss"
      （败局），否则 "control"（胜局对照）；与「26 败局+10 对照」语料设计恒等。
    - baseline（原局基线，逐席自比——R19「坐哪席就与该席原局实况比」同源）：
      final_money=原局该席终局资金（replay 末拍 farms[seat].money，与 rewards
      核对入账）；margin_d10/margin_d20/margin_final=原局我方队视角资金差
      （day 10/20 日终=step day*24+23 截尾，analysis20_rows 同口径；对 26
      败局实物已复核恒等），供 flip_stats 晚崩判定；sell_flow=原局该席 SELL
      事件流（逐动作，供避让/抢跑动作差分）；realized=原局逐席逐品项实现价
      （供 realized 提升观测）。
    - 逐局逐席统计=flip_stats（本文件 L2 v2；行契约=parse 同构双席行，rerun
      行由 _run_seat 产，含 prices/inventory 子键；第三参=运行内账 internal
      =_internal_account(_predict_agent) 的 written/plan/credit_debited/
      dodge_log 痕迹，产 fire_count/dodge_postpone_count/credit_debited）。
      run 记录=flip_stats 输出+{our_seat, n_rows, red, error, internal}。
    - 局级合成（mix_lab/R14 先例「局级 Δ=双席位 min >0，保守主口径」）：
      Δmargin=重演该席终局资金差−原局该席终局资金差（margin 口径）；
      局级 Δ=双席 min；晚崩局「翻正」=局级 Δ>0（R15「翻正（Δmargin>0）」
      同源用语）；敏感度并列入账（双席皆胜/原席位 Δ>0 计数）。
    - 聚合判据（R22 六判据，用户批准）：①胜局对照不翻负=对照局逐局逐席
      final_delta（重演终局资金−原局基线）min≥0（R19「对照资金 l1 非负/
      胜局不翻负」同源口径）；②晚崩局翻正 ≥1/3=n_flipped*3 ≥ n_late
      （n_late=晚崩局数，期望 15；≥5 翻正）；③闭环 h2h ≥0.55=主对（vs r37）
      seed 级 rate ≥ 0.55；④动作降量=重演臂 fire_count 合计≤1000 且
      dodge_postpone_count 合计=0（有红局/缺计数→fail-closed False）；
      ⑤反制臂胜率不降=counter_r39 rate ≥ counter_r37 rate（独立 seed、双臂
      皆有决胜局，缺→False）；⑥realized 价不跌=STRAWBERRY delta_px 均值≥0
      （须有草莓样本，缺→False）。realized 提升（delta_px_gain）仍为观测。
    - 反制模拟臂（R22 改4 接线）：make_counter_opponent 件（同一件同配置）
      落盘临时件经 phase_b.load_l3_callable 装载（与 v1 闭环副证装载同路），
      r39（=pkg）与 r37（=counter_baseline，缺省=main_opponent）各对打，
      n_games_counter_r39/r37 ∈ 8-16 偶数局、独立 seed（缺省 43000/44000 基），
      seed 级聚合席位翻转不双计（_h2h_arm 同构）；件生成失败→最简 PASS
      对手（kind=pass_fallback 留档）。
    - 闭环副证（h2h vs r37 主对+r34a 辅对）：双活件真交易（kaggle_environments
      kaggriculture，seed 显式逐局传入，episodeSteps=720）；每独立 seed 双席位
      各一局，**席位翻转不双计**——统计按独立 seed n 报（judge_league 同构）：
      胜=两席皆胜、平=席位分歧或皆平、负=皆负，rate=(胜+0.5平)/独立局；
      无决胜 seed rate=0.0 fail-closed。主对判据承载；辅对（r34a）仅观测。
    - bench（副证配置，可选 dict，缺省=验收档）：{"main_opponent",
      "secondary_opponent", "n_games_main"(缺省16，≥2 偶数),
      "n_games_secondary"(缺省8), "seeds_main", "seeds_secondary",
      "enabled"(缺省True), "counter_config"(缺省{}，make_counter_opponent
      配置), "n_games_counter_r39"/"n_games_counter_r37"(缺省8，8-16 偶数),
      "seeds_counter_r39"(缺省 43000 基)/"seeds_counter_r37"(缺省 44000 基),
      "counter_baseline"(缺省=main_opponent)}；非法即 ValueError（fail-closed）。
    - evidence dict 由本函数返回、不落盘（台账写入归实跑编排，防测试覆写真
      台账——R19/R20 judge 同则）；重叠语料（a22 灾难局 ⊂ r34a 败局）聚合按
      唯一 episode 去重计，条目级逐条留痕；source 记可复跑命令+seed 清单。
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
        sys.path.insert(0, _ksim)   # 兄弟包可从任意 CWD 导入（R19/R20 先例）

    try:
        from orderbook_r37 import parse_states
    except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑
        import parse_states
    from agent.planner import twin
    from orderbook_surge_lab import phase_b

    H2H_THRESHOLD = 0.55
    LATE_FLIP_NUM, LATE_FLIP_DEN = 1, 3   # 晚崩局翻正 ≥1/3
    FIRE_THRESHOLD = 1000                # 动作降量：预测写入合计上限（R22 ④）
    EPISODE_STEPS = 720
    MAIN_SEED_BASE, SECONDARY_SEED_BASE = 41000, 42000
    COUNTER_R39_BASE, COUNTER_R37_BASE = 43000, 44000
    cache_dirs = ("/tmp/kagr24", "/tmp/kagr22", "/tmp/r33audit")
    pull_dir = "/tmp/kagr24"
    kaggle_bin = "/home/renyxin/.local/bin/kaggle"
    episode_re = re.compile(r"episode-(\d+)-replay\.json$")
    _ksim_here = _ksim

    def _bad_corpus(msg):
        return ValueError(f"语料缺失/不合法：{msg}")

    def _sha256(path):
        if not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    # ---- 副证配置（bench；缺省=验收档，非法即抛） ------------------------
    def _bench_cfg(raw):
        if raw is None:
            raw = {}
        if not isinstance(raw, dict):
            raise ValueError(f"副证配置应为 dict，实为 {type(raw).__name__}")

        def _path(key, default):
            val = raw.get(key, default)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"副证配置 {key} 非字符串路径：{val!r}")
            return os.path.abspath(val)

        def _games(key, default):
            val = raw.get(key, default)
            if isinstance(val, bool) or not isinstance(val, int):
                raise ValueError(f"副证配置 {key} 应为 int，实为 {val!r}")
            if val < 2 or val % 2:
                raise ValueError(f"副证配置 {key} 须为 ≥2 偶数（每 seed 双席），实为 {val!r}")
            return val

        def _seeds(key, base, n_games):
            val = raw.get(key)
            if val is None:
                return [base + i for i in range(n_games // 2)]
            if not isinstance(val, (list, tuple)) or not val:
                raise ValueError(f"副证配置 {key} 应为非空 int 列表：{val!r}")
            out = []
            for s in val:
                if isinstance(s, bool) or not isinstance(s, int):
                    raise ValueError(f"副证配置 {key} 含非 int 种子：{s!r}")
                out.append(int(s))
            return out

        n_main = _games("n_games_main", 16)
        n_sec = _games("n_games_secondary", 8)

        def _counter_games(key, default):
            val = raw.get(key, default)
            if isinstance(val, bool) or not isinstance(val, int):
                raise ValueError(f"副证配置 {key} 应为 int，实为 {val!r}")
            if val < 8 or val > 16 or val % 2:
                raise ValueError(f"副证配置 {key} 须为 8-16 偶数（每 seed 双席），"
                                 f"实为 {val!r}")
            return val

        n_cr39 = _counter_games("n_games_counter_r39", 8)
        n_cr37 = _counter_games("n_games_counter_r37", 8)
        counter_config = raw.get("counter_config")
        if counter_config is None:
            counter_config = {}
        if not isinstance(counter_config, dict):
            raise ValueError(f"副证配置 counter_config 应为 dict，实为 "
                             f"{type(counter_config).__name__}")
        enabled = raw.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ValueError(f"副证配置 enabled 应为 bool，实为 {enabled!r}")
        main_opp = _path("main_opponent",
                         os.path.join(_ksim_here, "orderbook_r37",
                                      "build", "main.py"))
        return {
            "enabled": enabled,
            "main_opponent": main_opp,
            "secondary_opponent": _path("secondary_opponent",
                                        os.path.join(_ksim_here,
                                                     "orderbook_2965_adopt",
                                                     "a", "main.py")),
            "seeds_main": _seeds("seeds_main", MAIN_SEED_BASE, n_main),
            "seeds_secondary": _seeds("seeds_secondary",
                                      SECONDARY_SEED_BASE, n_sec),
            "counter_config": dict(counter_config),
            "n_games_counter_r39": n_cr39,
            "n_games_counter_r37": n_cr37,
            "seeds_counter_r39": _seeds("seeds_counter_r39",
                                        COUNTER_R39_BASE, n_cr39),
            "seeds_counter_r37": _seeds("seeds_counter_r37",
                                        COUNTER_R37_BASE, n_cr37),
            "counter_baseline": _path("counter_baseline", main_opp),
        }

    cfg = _bench_cfg(bench)

    # ---- 反制对手件（R22 改4；配置畸形即抛，fail-closed 早失败） ---------
    counter_artifact = make_counter_opponent(cfg["counter_config"])

    # ---- 预检语料（条目级；不合法即抛，报错含条目） -----------------------
    if not corpus:
        raise _bad_corpus("corpus 为空（需 26 败局+10 胜局对照语料局单）")
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
        base_cmd = [kaggle_bin, "competitions", "replay", str(ep),
                    "-p", pull_dir]
        pull_err = ""
        for mode in ("token", "default"):   # 429/失败退默认凭证（用户口径）
            env = os.environ.copy()
            if mode == "token":
                try:
                    tok = subprocess.run([kaggle_bin, "auth",
                                          "print-access-token"],
                                         capture_output=True, text=True,
                                         timeout=60)
                    if tok.returncode == 0 and tok.stdout.strip():
                        env["KAGGLE_API_TOKEN"] = tok.stdout.strip()
                except (OSError, subprocess.SubprocessError):
                    pass  # 无 token 注入则直接走默认 kaggle.json 凭证
            else:
                env.pop("KAGGLE_API_TOKEN", None)
            try:
                p = subprocess.run(base_cmd, capture_output=True, text=True,
                                   timeout=600, env=env)
            except (OSError, subprocess.SubprocessError) as exc:
                p = None
                pull_err = f"{type(exc).__name__}: {exc}"
            else:
                pull_err = (p.stderr or p.stdout or "").strip()[-200:]
            if (p is not None and p.returncode == 0 and os.path.isfile(target)
                    and os.path.getsize(target) > 1000):
                return target, "pulled", None
            time.sleep(5)
        return target, "pull_failed", pull_err or "kaggle competitions replay 失败"

    def _pull_command(ep):
        return (f"KAGGLE_API_TOKEN=$({kaggle_bin} auth print-access-token "
                f"2>/dev/null) {kaggle_bin} competitions replay {ep} "
                f"-p {pull_dir}")

    # ---- 原局实况统计（原始 replay 直取：基线+卖流+实现价） ---------------
    def _jload(x):
        return json.loads(x) if isinstance(x, str) else x

    def _orig_inv(priv):
        """private → shed+seeds+随身合计（parse_states._inventory 同口径）。"""
        priv = _jload(priv) or {}
        total = {}
        for part in ("shed", "seeds"):
            sub = _jload(priv.get(part)) or {}
            for k, v in dict(sub).items():
                total[k] = total.get(k, 0) + v
        for sub in (_jload(priv.get("inventories")) or []):
            for k, v in dict(sub or {}).items():
                total[k] = total.get(k, 0) + v
        return total

    def _sell_ops(action):
        """动作 → [(item, qty)]（market SELL 单；dict 动作或裸列表皆容）。"""
        if isinstance(action, dict):
            market = action.get("market")
        elif isinstance(action, (list, tuple)):
            market = action
        else:
            return
        for op in (market or []):
            if (isinstance(op, (list, tuple)) and len(op) >= 3
                    and op[0] == "SELL" and isinstance(op[1], str)):
                try:
                    qty = int(op[2])
                except (TypeError, ValueError):
                    continue
                if qty > 0:
                    yield op[1], qty

    def _original_stats(replay, ep_guess):
        """原始 replay → 基线统计（终局资金/我方队视角 margin 探针/逐席卖流/
        逐席逐品项实现价）。day 终=step day*24+23 截尾（analysis20 同口径）。"""
        info = replay.get("info") or {}
        ep = int(info.get("EpisodeId") or ep_guess or 0)
        teams = list(info.get("TeamNames") or [])
        our_team_seat = teams.index("renyxin") if "renyxin" in teams else 0
        steps = replay.get("steps") or []
        if not steps:
            raise ValueError("replay 无 steps")

        def _farm(si, seat):
            obs = (steps[si][seat] or {}).get("observation") or {}
            farms = _jload(obs.get("farms")) or []
            return farms[seat] if seat < len(farms) else {}

        def _money(si, seat):
            v = _farm(si, seat).get("money")
            return float(v) if isinstance(v, (int, float)) else None

        def _day_end_money(day, seat):
            si = min(day * 24 + 23, len(steps) - 1)
            return _money(si, seat)

        def _prices(si, seat):
            obs = (steps[si][seat] or {}).get("observation") or {}
            market = _jload(obs.get("market")) or {}
            prices = _jload(market.get("prices")) or {}
            return {k: float(v) for k, v in dict(prices).items()
                    if isinstance(v, (int, float))}

        final_by_seat = {}
        for seat in (0, 1):
            val = _money(len(steps) - 1, seat)
            if val is None:
                r = replay.get("rewards")
                val = float(r[seat]) if isinstance(r, list) and len(r) == 2 else 0.0
            final_by_seat[seat] = val
        rewards = replay.get("rewards")
        if isinstance(rewards, list) and len(rewards) == 2:
            for seat in (0, 1):
                if isinstance(rewards[seat], (int, float)):
                    final_by_seat[seat] = float(rewards[seat])
        m_our = final_by_seat[our_team_seat] - final_by_seat[1 - our_team_seat]
        probes = {}
        for label, day in (("margin_d10", 10), ("margin_d20", 20)):
            v0 = _day_end_money(day, our_team_seat)
            v1 = _day_end_money(day, 1 - our_team_seat)
            probes[label] = (v0 - v1) if (v0 is not None and v1 is not None) else None
        probes["margin_final"] = m_our
        res = ("L" if final_by_seat[our_team_seat]
               < final_by_seat[1 - our_team_seat] else
               ("W" if final_by_seat[our_team_seat]
                > final_by_seat[1 - our_team_seat] else "T"))
        kind = "loss" if res == "L" else "control"

        sell_flow_by_seat = {0: {}, 1: {}}
        px_acc = {0: {}, 1: {}}
        prev_inv = {0: None, 1: None}
        for si in range(len(steps)):
            for seat in (0, 1):
                action = (steps[si][seat] or {}).get("action")
                sells = list(_sell_ops(action))
                obs = (steps[si][seat] or {}).get("observation") or {}
                inv_now = _orig_inv(obs.get("private"))
                prices = _prices(si, seat) if sells else {}
                stock_hi = {}
                inv_prev = prev_inv[seat] or {}
                for k in set(inv_prev) | set(inv_now):
                    stock_hi[k] = max(inv_prev.get(k, 0), inv_now.get(k, 0))
                for item, qty in sells:
                    flow = sell_flow_by_seat[seat].setdefault(item, [])
                    flow.append([si, qty])
                    ex = max(0, min(qty, stock_hi.get(item, 0)))
                    stock_hi[item] = stock_hi.get(item, 0) - ex
                    if ex > 0:
                        acc = px_acc[seat].setdefault(
                            item, {"qty": 0.0, "val": 0.0, "priced_qty": 0.0})
                        acc["qty"] += ex
                        px = prices.get(item)
                        if px is not None:
                            acc["val"] += ex * px
                            acc["priced_qty"] += ex
                prev_inv[seat] = inv_now
        realized_px_by_seat = {0: {}, 1: {}}
        for seat in (0, 1):
            for item, acc in px_acc[seat].items():
                realized_px_by_seat[seat][item] = (
                    round(acc["val"] / acc["qty"], 2)
                    if acc["qty"] > 0 and acc["priced_qty"] == acc["qty"]
                    else None)
        return {"episode": ep, "teams": teams, "our_team_seat": our_team_seat,
                "res": res, "kind": kind, "final_by_seat": final_by_seat,
                "probes": probes,
                "sell_flow_by_seat": sell_flow_by_seat,
                "realized_px_by_seat": realized_px_by_seat,
                "rewards": rewards if isinstance(rewards, list) else None}

    # ---- twin 前向走子（R19 judge_replay 同构） ---------------------------
    def _extract_rows(state, actions, prices=True):
        """twin 状态+该拍动作对 → parse 同构双席行（含 inventory/prices 子键）。"""
        obs0 = state.seats[0].observation
        farms = obs0.farms
        market = getattr(obs0, "market", None)
        if isinstance(market, str):
            market = json.loads(market)
        px = {}
        if prices and isinstance(market, dict):
            px = {k: float(v) for k, v in ((market or {}).get("prices") or {}).items()
                  if isinstance(v, (int, float))}
        rows = []
        for i in range(2):
            farm = farms[i] if i < len(farms) else {}
            animals, tiles = parse_states._extract_grids(
                f"farms[{i}].tiles", farm.get("tiles") or [])
            obs_i = state.seats[i].observation
            if hasattr(obs_i, "private"):
                priv = obs_i.private
            elif isinstance(obs_i, dict):
                priv = obs_i.get("private")
            else:
                priv = None
            if isinstance(priv, str):
                priv = json.loads(priv)
            inv = None
            if isinstance(priv, dict):
                try:
                    inv = parse_states._inventory(f"farms[{i}].private", priv)
                except Exception:            # 棚仓臂尽力，缺→None
                    inv = None
            rows.append({"step": actions[0], "seat": i,
                         "action": actions[1][i],
                         "money": farm.get("money"),
                         "hands": farm.get("hands"),
                         "farmer": farm.get("farmer"),
                         "animals_grid": animals, "tiles": tiles,
                         "inventory": inv,
                         "prices": dict(px) if px else None})
        return rows

    def _run_seat(replay, agent, seat, steps0):
        """单局单席 seated 重演（对手=录像开环），产逐步双席行。"""
        bundle = twin.load_engine()
        state = twin.build_state_from_replay(replay, 0, bundle)
        recorded = twin.replay_transition_actions(replay)
        if not recorded:
            raise ValueError("replay 无转移动作流")
        rows = _extract_rows(state, (0, steps0))
        taken = 0
        while not state.env.done and taken < len(recorded):
            obs = phase_b._obs_dict(state, seat)
            mine = agent(obs)
            pair = [recorded[taken][1 - seat]] * 2
            pair[seat] = mine
            twin.step(state, pair)
            taken += 1
            rows.extend(_extract_rows(state, (taken, pair)))
        return rows

    def _internal_account(agent):
        """运行内账观测（_predict_agent 痕迹面，v2）。

        输出 {"dodges", "plan_entries", "written", "plan", "dodge_log",
        ["credit_debited"]}：written/plan/dodge_log 供 flip_stats v2 计
        fire_count/dodge_postpone_count/credit_debited（写入痕迹计数）；
        非预测件（痕迹属性全缺）→None。
        """
        try:
            log = getattr(agent, "_dodge_log", None)
            plan = getattr(agent, "_opponent_plan", None)
            written = getattr(agent, "_written", None)
            credit_debited = getattr(agent, "_credit_debited", None)
            if (log is None and plan is None and written is None
                    and credit_debited is None):
                return None
            n_plan = 0
            clean_plan = []
            for slot in (plan or []):
                if isinstance(slot, dict):
                    clean_plan.append(slot)
                    if (slot.get("market") or []):
                        n_plan += 1
            out = {"dodges": len(log or []), "plan_entries": n_plan,
                   "written": [w for w in (written or [])
                               if isinstance(w, dict)],
                   "plan": clean_plan,
                   "dodge_log": [e for e in (log or [])
                                 if isinstance(e, dict)]}
            if credit_debited is not None:
                out["credit_debited"] = credit_debited
            return out
        except Exception:
            return None

    # ---- 逐局重演（单局失败标红计入，不短路全跑） -------------------------
    def _replay_game(entry):
        rec = {"entry": entry["entry"], "entry_kind": entry["kind"],
               "episode": entry["episode_guess"]}
        try:
            path, source, pull_err = _resolve_replay(entry)
            rec["replay_path"] = path
            rec["replay_source"] = source
            if source == "pull_failed":
                raise RuntimeError(f"replay 拉取失败：{pull_err}")
            with open(path, "r", encoding="utf-8") as fh:
                replay = json.load(fh)
            stats = _original_stats(replay, entry["episode_guess"])
            rec.update(episode=stats["episode"], kind=stats["kind"],
                       res=stats["res"], teams=stats["teams"],
                       our_team_seat=stats["our_team_seat"],
                       rewards=stats["rewards"])
            rec["baseline"] = {
                "final_by_seat": {str(k): v for k, v
                                  in stats["final_by_seat"].items()},
                "margin_d10": stats["probes"]["margin_d10"],
                "margin_d20": stats["probes"]["margin_d20"],
                "margin_final": stats["probes"]["margin_final"]}
            steps0 = [(replay["steps"][0][i] or {}).get("action")
                      for i in range(2)]
            runs, game_red, game_err = {}, False, None
            for seat in (0, 1):
                try:
                    agent = phase_b.load_l3_callable(pkg_path)
                    rows = _run_seat(replay, agent, seat, steps0)
                    base = {
                        "our_seat": seat,
                        "kind": stats["kind"],
                        "final_money": stats["final_by_seat"][seat],
                        "opp_final_money": stats["final_by_seat"][1 - seat],
                        "margin_d10": stats["probes"]["margin_d10"],
                        "margin_d20": stats["probes"]["margin_d20"],
                        "margin_final": stats["probes"]["margin_final"],
                        "sell_flow": stats["sell_flow_by_seat"][seat],
                        "realized": {item: {"our_px":
                                            stats["realized_px_by_seat"][seat].get(item),
                                            "opp_px":
                                            stats["realized_px_by_seat"][1 - seat].get(item)}
                                     for item in COLLISION_ITEMS},
                    }
                    internal = _internal_account(agent)
                    verd = flip_stats(rows, base, internal)
                    run = {"our_seat": seat, "teams": stats["teams"],
                           "flip": verd["flip"], "realized": verd["realized"],
                           "dodges": verd["dodges"],
                           "front_runs": verd["front_runs"],
                           "fire_count": verd["fire_count"],
                           "dodge_postpone_count":
                               verd["dodge_postpone_count"],
                           "credit_debited": verd["credit_debited"],
                           "final_delta": verd["final_delta"],
                           "verdict": verd["verdict"],
                           "internal": internal,
                           "n_rows": len(rows)}
                    run["red"] = verd["verdict"] == "UNKNOWN"
                    run["error"] = None
                    game_red = game_red or run["red"]
                    runs["seat%d" % seat] = run
                except Exception as exc:  # 单席失败=红局入账
                    runs["seat%d" % seat] = {
                        "our_seat": seat, "teams": stats["teams"],
                        "error": f"{type(exc).__name__}: {exc}", "red": True}
                    game_red = True
                    game_err = f"{type(exc).__name__}: {exc}"
            game = {"entry": rec["entry"], "episode": stats["episode"],
                    "kind": stats["kind"], "res": stats["res"],
                    "teams": stats["teams"],
                    "our_team_seat": stats["our_team_seat"],
                    "replay_path": path, "replay_source": source,
                    "baseline": rec["baseline"],
                    "runs": runs, "red": game_red, "error": game_err}
        except Exception as exc:  # 单局重放失败标红计入，不短路全跑
            err = f"{type(exc).__name__}: {exc}"
            rec["red"] = True
            rec["error"] = err
            game = {"entry": rec["entry"],
                    "episode": entry["episode_guess"],
                    "kind": None, "our_team_seat": None,
                    "replay_path": entry.get("path"),
                    "runs": {}, "red": True, "error": err}
        return rec, game

    # ---- 闭环副证（h2h 双活件；seed 级、席位翻转不双计） ------------------
    def _h2h_arm(opp_path, arm_label, seeds, ours_path=None):
        import kaggle_environments
        ours_path = ours_path or pkg_path
        games = []
        for seed in seeds:
            for our_seat in (0, 1):
                rec = {"arm": arm_label, "seed": int(seed),
                       "our_seat": our_seat, "red": False, "error": None}
                t0 = time.perf_counter()
                try:
                    ours = phase_b.load_l3_callable(ours_path)
                    theirs = phase_b.load_l3_callable(opp_path)
                    agents = ([ours, theirs] if our_seat == 0
                              else [theirs, ours])
                    env = kaggle_environments.make(
                        "kaggriculture",
                        configuration={"episodeSteps": EPISODE_STEPS,
                                       "seed": int(seed),
                                       "actTimeout": 60.0},
                        debug=True)
                    env.run(agents)
                    steps = getattr(env, "steps", None)
                    if not isinstance(steps, list) or len(steps) < 2:
                        raise RuntimeError("引擎状态帧异常")
                    rewards = [float(steps[-1][s].get("reward"))
                               for s in (0, 1)]
                    statuses = [str(steps[-1][s].get("status"))
                                for s in (0, 1)]
                    rec["rewards"] = rewards
                    rec["statuses"] = statuses
                    rec["margin"] = rewards[our_seat] - rewards[1 - our_seat]
                    if statuses != ["DONE", "DONE"]:
                        rec["red"] = True
                        rec["note"] = f"非终局 statuses：{statuses}"
                    else:
                        if rewards[0] > rewards[1]:
                            wseat = 0
                        elif rewards[1] > rewards[0]:
                            wseat = 1
                        else:
                            wseat = None
                        rec["winner_seat"] = wseat
                        rec["winner"] = ("tie" if wseat is None
                                         else "ours" if wseat == our_seat
                                         else "opp")
                except Exception as exc:  # 单局崩=红局入账，不短路
                    rec["red"] = True
                    rec["error"] = f"{type(exc).__name__}: {exc}"
                rec["elapsed_s"] = round(time.perf_counter() - t0, 3)
                games.append(rec)
        # seed 级聚合（席位翻转不双计：统计按独立 seed n 报）
        pairs = {}
        for g in games:
            pairs.setdefault(g["seed"], []).append(g)
        run_scores = {"wins": 0, "ties": 0, "losses": 0}
        outcomes = {"win": 0, "draw": 0, "loss": 0, "incomplete": 0}
        for seed in sorted(pairs):
            runs_ = sorted(pairs[seed], key=lambda r: r["our_seat"])
            for r in runs_:
                if r.get("red") or r.get("winner") is None:
                    continue
                if r["winner"] == "ours":
                    run_scores["wins"] += 1
                elif r["winner"] == "tie":
                    run_scores["ties"] += 1
                else:
                    run_scores["losses"] += 1
            if (len(runs_) != 2
                    or any(r.get("red") or r.get("winner") is None
                           for r in runs_)):
                outcomes["incomplete"] += 1
                continue
            score = sum(1.0 if r["winner"] == "ours"
                        else 0.5 if r["winner"] == "tie" else 0.0
                        for r in runs_) / 2.0
            if score == 1.0:
                outcomes["win"] += 1
            elif score == 0.0:
                outcomes["loss"] += 1
            else:
                outcomes["draw"] += 1
        decided = outcomes["win"] + outcomes["draw"] + outcomes["loss"]
        rate = (round((outcomes["win"] + 0.5 * outcomes["draw"]) / decided, 4)
                if decided else 0.0)
        return {"arm": arm_label, "opponent": os.path.abspath(opp_path),
                "opponent_sha256": _sha256(os.path.abspath(opp_path)),
                "ours": os.path.abspath(ours_path),
                "ours_sha256": _sha256(os.path.abspath(ours_path)),
                "n_games": len(games), "n_independent": len(pairs),
                "seeds": sorted(pairs), "run_scores": run_scores,
                "seed_outcomes": outcomes, "rate": rate,
                "h2h_rate": rate, "h2h_threshold": H2H_THRESHOLD,
                "games": games}

    # ---- 全量跑（重演臂+闭环臂；单局失败标红计入不短路） ------------------
    t0 = time.perf_counter()
    games, errors, corpus_listing = [], [], []
    for entry in entries:
        rec, game = _replay_game(entry)
        corpus_listing.append(rec)
        games.append(game)
        if game.get("red") and game.get("error"):
            errors.append({"episode": game.get("episode"),
                           "entry": game.get("entry"),
                           "error": game["error"]})

    h2h_blocks = {"main": None, "secondary": None}
    if cfg["enabled"]:
        for arm_label, opp, seeds in (
                ("main", cfg["main_opponent"], cfg["seeds_main"]),
                ("secondary", cfg["secondary_opponent"],
                 cfg["seeds_secondary"])):
            try:
                block = _h2h_arm(opp, arm_label, seeds)
            except Exception as exc:  # 臂级崩=红块入账，不短路
                block = {"arm": arm_label, "opponent": opp,
                         "error": f"{type(exc).__name__}: {exc}",
                         "rate": 0.0, "h2h_rate": 0.0,
                         "h2h_threshold": H2H_THRESHOLD, "games": [],
                         "seed_outcomes": {"win": 0, "draw": 0, "loss": 0,
                                           "incomplete": 0},
                         "n_games": 0, "n_independent": 0, "seeds": [],
                         "run_scores": {"wins": 0, "ties": 0, "losses": 0}}
                errors.append({"arm": arm_label,
                               "error": block["error"]})
            h2h_blocks[arm_label] = block

    # ---- 反制模拟臂（make_counter_opponent 件；同件同配置对打 r39/r37） --
    counter_blocks = {"r39": None, "r37": None}
    counter_meta = {
        "kind": counter_artifact.get("kind"),
        "config": counter_artifact.get("config"),
        "features": counter_artifact.get("features"),
        "script_path": None, "script_sha256": None,
        "script": counter_artifact.get("script"),
    }
    if cfg["enabled"]:
        import tempfile
        cdir = tempfile.mkdtemp(prefix="counter_opp_")
        cpath = os.path.join(cdir, "counter_opponent.py")
        with open(cpath, "w", encoding="utf-8") as fh:
            fh.write(counter_artifact["script"])
        counter_meta["script_path"] = cpath
        counter_meta["script_sha256"] = _sha256(cpath)
        for arm_key, ours_path, seeds in (
                ("r39", pkg_path, cfg["seeds_counter_r39"]),
                ("r37", cfg["counter_baseline"],
                 cfg["seeds_counter_r37"])):
            try:
                block = _h2h_arm(cpath, "counter_" + arm_key, seeds,
                                 ours_path=ours_path)
            except Exception as exc:  # 臂级崩=红块入账，不短路
                block = {"arm": "counter_" + arm_key, "opponent": cpath,
                         "ours": os.path.abspath(ours_path),
                         "error": f"{type(exc).__name__}: {exc}",
                         "rate": 0.0, "h2h_rate": 0.0,
                         "h2h_threshold": H2H_THRESHOLD, "games": [],
                         "seed_outcomes": {"win": 0, "draw": 0, "loss": 0,
                                           "incomplete": 0},
                         "n_games": 0, "n_independent": 0, "seeds": [],
                         "run_scores": {"wins": 0, "ties": 0, "losses": 0}}
                errors.append({"arm": "counter_" + arm_key,
                               "error": block["error"]})
            counter_blocks[arm_key] = block

    # ---- 聚合（唯一局去重；判据=R21 ②） ---------------------------------
    unique_games, dup_notes = [], []
    seen_ep = set()
    for g in games:
        ep = g.get("episode")
        key = ep if ep is not None else ("entry", g.get("entry"))
        if key in seen_ep:
            dup_notes.append({"episode": ep, "entry": g.get("entry"),
                              "note": "语料条目与前条同一局（a22 灾难局 ⊂ "
                                      "r34a 败局重叠），聚合按唯一局去重计"})
            continue
        seen_ep.add(key)
        unique_games.append(g)

    loss_views, control_views = [], []
    for g in unique_games:
        runs = [r for r in (g.get("runs") or {}).values()
                if isinstance(r, dict) and not r.get("red")]
        ok = len(runs) == 2 and not g.get("red")
        deltas = [r["flip"]["delta_margin"] for r in runs
                  if isinstance(r.get("flip"), dict)
                  and isinstance(r["flip"].get("delta_margin"), (int, float))]
        dmin = min(deltas) if deltas else None
        late = (runs[0]["flip"]["late_collapse"] if runs
                and isinstance(runs[0].get("flip"), dict) else None)
        view = {"episode": g.get("episode"), "entry": g.get("entry"),
                "kind": g.get("kind"), "res": g.get("res"),
                "late_collapse": late,
                "dominant_segment": (runs[0]["flip"].get("dominant_segment")
                                     if runs and isinstance(runs[0].get("flip"),
                                                           dict) else None),
                "lead_then_lost": (runs[0]["flip"].get("lead_then_lost")
                                   if runs and isinstance(runs[0].get("flip"),
                                                         dict) else None),
                "delta_margin_by_seat": {r["our_seat"]: r["flip"]["delta_margin"]
                                         for r in runs
                                         if isinstance(r.get("flip"), dict)},
                "delta_margin_min": dmin,
                "flipped": (dmin > 0) if dmin is not None else None,
                "flipped_orig_seat": None,
                "flipped_win": None,
                "red": g.get("red"), "complete": ok}
        if ok and g.get("our_team_seat") is not None:
            orig = view["delta_margin_by_seat"].get(g["our_team_seat"])
            view["flipped_orig_seat"] = (orig > 0) if orig is not None else None
            wins = [r["flip"].get("rerun_win") for r in runs
                    if isinstance(r.get("flip"), dict)]
            view["flipped_win"] = bool(wins) and all(wins)
        if g.get("kind") == "control":
            fds = [r.get("final_delta") for r in runs
                   if isinstance(r.get("final_delta"), (int, float))]
            view["final_delta_min"] = min(fds) if fds else None
            view["final_delta_by_seat"] = {r["our_seat"]: r.get("final_delta")
                                           for r in runs}
            view["not_flipped_negative"] = (
                view["final_delta_min"] >= 0
                if view["final_delta_min"] is not None else None)
            control_views.append(view)
        else:
            loss_views.append(view)

    late_views = [v for v in loss_views if v["late_collapse"]]
    flipped_late = [v for v in late_views if v["flipped"]]
    n_late = len(late_views)
    n_flipped = len(flipped_late)
    ctrl_fds = [v["final_delta_min"] for v in control_views
                if v["final_delta_min"] is not None and v["complete"]]
    ctrl_min = min(ctrl_fds) if ctrl_fds else None
    ctrl_sum = round(sum(ctrl_fds), 2) if ctrl_fds else None
    main_rate = (h2h_blocks["main"] or {}).get("h2h_rate", 0.0)
    main_decided = sum(((h2h_blocks["main"] or {}).get("seed_outcomes") or {})
                       .get(k, 0) for k in ("win", "draw", "loss"))
    ctr_r39 = counter_blocks["r39"] or {}
    ctr_r37 = counter_blocks["r37"] or {}
    rate_r39 = float(ctr_r39.get("h2h_rate") or 0.0)
    rate_r37 = float(ctr_r37.get("h2h_rate") or 0.0)
    dec_r39 = sum((ctr_r39.get("seed_outcomes") or {}).get(k, 0)
                  for k in ("win", "draw", "loss"))
    dec_r37 = sum((ctr_r37.get("seed_outcomes") or {}).get(k, 0)
                  for k in ("win", "draw", "loss"))

    # 观测面：realized 价 + 避让/抢跑 + 动作降量（fire/推迟/减记）
    realized_obs, dodge_total, front_total = [], 0, 0
    int_dodge_total, int_plan_total, int_n = 0, 0, 0
    fire_total, fire_max, postpone_total, credit_total = 0, None, 0, 0.0
    n_fire_missing = 0
    for g in unique_games:
        for r in (g.get("runs") or {}).values():
            if not isinstance(r, dict) or r.get("red"):
                continue
            rz = r.get("realized") or {}
            if rz.get("item") and rz.get("delta_px") is not None:
                realized_obs.append({
                    "episode": g.get("episode"), "our_seat": r.get("our_seat"),
                    "item": rz.get("item"), "our_px": rz.get("our_px"),
                    "opp_px": rz.get("opp_px"),
                    "delta_px": rz.get("delta_px"),
                    "delta_px_gain": rz.get("delta_px_gain")})
            if isinstance(r.get("dodges"), (int, float)):
                dodge_total += int(r["dodges"])
            if isinstance(r.get("front_runs"), (int, float)):
                front_total += int(r["front_runs"])
            acc = r.get("internal")
            if isinstance(acc, dict):
                int_n += 1
                int_dodge_total += int(acc.get("dodges") or 0)
                int_plan_total += int(acc.get("plan_entries") or 0)
            fv = r.get("fire_count")
            if isinstance(fv, int) and not isinstance(fv, bool):
                fire_total += fv
                fire_max = fv if fire_max is None else max(fire_max, fv)
            else:
                n_fire_missing += 1
            pv = r.get("dodge_postpone_count")
            if isinstance(pv, (int, float)) and not isinstance(pv, bool):
                postpone_total += int(pv)
            else:
                n_fire_missing += 1
            cv = r.get("credit_debited")
            if isinstance(cv, (int, float)) and not isinstance(cv, bool):
                credit_total += float(cv)
    gain_vals = [v["delta_px_gain"] for v in realized_obs
                 if isinstance(v.get("delta_px_gain"), (int, float))]
    delta_vals = [v["delta_px"] for v in realized_obs
                  if isinstance(v.get("delta_px"), (int, float))]
    straw_vals = [v["delta_px"] for v in realized_obs
                  if v.get("item") == "STRAWBERRY"
                  and isinstance(v.get("delta_px"), (int, float))]

    # ---- 六判据（R22） --------------------------------------------------
    crit = {
        "control_not_flipped": bool(ctrl_fds and ctrl_min is not None
                                    and ctrl_min >= 0),
        "late_flip_ge_third": bool(n_late > 0
                                   and n_flipped * LATE_FLIP_DEN
                                   >= n_late * LATE_FLIP_NUM),
        "h2h_vs_r37_ge_055": bool(main_decided > 0
                                  and main_rate >= H2H_THRESHOLD),
        "action_throttle": bool(n_fire_missing == 0
                                and fire_total <= FIRE_THRESHOLD
                                and postpone_total == 0),
        "counter_arm_not_worse": bool(dec_r39 > 0 and dec_r37 > 0
                                      and rate_r39 >= rate_r37),
        "realized_px_not_down": bool(straw_vals
                                     and sum(straw_vals) / len(straw_vals)
                                     >= 0),
    }
    n_red = sum(1 for g in games if g.get("red"))
    overall_pass = bool(all(crit.values()) and not n_red and not errors)

    evidence = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pkg_path": os.path.abspath(pkg_path),
        "pkg_sha256": _sha256(os.path.abspath(pkg_path)),
        "method": {
            "semantics": ("活件（r39）vs 原局对手录像动作（开环）；逐局双席位各"
                          "演一遍（坐席0/坐席1 互换各一局，排除座位效应）"),
            "loader": ("官方 last-callable 内存 exec 每局全新命名空间（R18 "
                       "method note；活件末 callable=_predict_agent）"),
            "engine": "agent.planner.twin 前向走子（R19 judge_replay 同款）",
            "baseline": ("baseline_final=原局实况该席终局资金（replay rewards/"
                         "末拍 farms[seat].money），逐席自比；margin_d10/d20="
                         "我方队视角日终资金差（step day*24+23 截尾，"
                         "analysis20_rows 同口径）"),
            "late_collapse": ("晚崩判定=loss_phase 主导段口径（analysis22 "
                              "group_stats.loss_phase_rule 同源：主导=最负段 "
                              "of (d10−0, d20−d10, final−d20)，late_d20_end "
                              "=晚崩；预期 15/20）；次级标志 lead_then_lost"
                              "=（margin_d10>0 或 margin_d20>0）留档"),
            "flip": ("翻正=R15「翻正（Δmargin>0）」同源——Δmargin=重演该席终局"
                     "资金差−原局该席资金差，局级 Δ=双席 min（mix_lab/R14 "
                     "保守主口径）；敏感度并列双席皆胜/原席位计数"),
            "control": ("胜局对照不翻负=final_delta（重演终局资金−原局基线）"
                        "逐局逐席 min≥0（R19「对照资金 l1 非负/胜局不翻负」"
                        "同源口径）"),
            "realized": ("撞车品项序 STRAWBERRY/MILK/WOOL/MELON 取首个双席皆"
                         "卖品项；实现价=Σ(成交截断量×该拍挂牌价)/Σ成交截断量"
                         "（成交截断=邻拍库存差分 max 截断，a22_dissect 同构）；"
                         "delta_px_gain 提升=观测指标不进门槛，判据⑥=草莓 "
                         "delta_px（我−对手实现价）均值≥0"),
            "dodge_frontrun": ("避让/抢跑=动作差分痕迹计数（逐品项步序 FIFO "
                               "对齐原局该席卖单流：提前=抢跑、顺延/减量/删除"
                               "=避让、新增=抢跑痕迹）；另记运行内账观测"
                               "（_predict_agent._dodge_log/_opponent_plan）"),
            "h2h": ("闭环副证=双活件真交易（kaggle_environments kaggriculture，"
                    "seed 显式）；主对 vs r37（判据承载）+辅对 vs r34a（观测）；"
                    "seed 级聚合、席位翻转不双计：胜=两席皆胜、平=分歧或皆平、"
                    "负=皆负，rate=(胜+0.5平)/独立局"),
            "counter_arm": ("反制模拟臂=make_counter_opponent 件（Wool "
                            "Front-Runner：嗅探羊提交/剪毛窗→提前 1-2 回合"
                            "集中倒毛+Anti-Shock）同件同配置对打 r39/r37，"
                            "8-16 局/件、独立 seed、seed 级聚合同 h2h；判据"
                            "⑤=两臂 rate 对比不降"),
            "action_throttle": ("动作降量判据④=重演臂 fire_count 合计≤1000"
                                "（预测写入，运行内账/plan 写入痕迹计）且 "
                                "dodge_postpone_count 合计=0（v2 无推迟语义）"),
        },
        "corpus": {"entries": corpus_listing,
                   "n_entries": len(entries),
                   "n_loss_entries": sum(1 for g in games
                                         if g.get("kind") == "loss"),
                   "n_control_entries": sum(1 for g in games
                                            if g.get("kind") == "control"),
                   "n_unique_games": len(unique_games),
                   "duplicates": dup_notes},
        "games": games,
        "aggregate": {
            "losses": {
                "n_games": len(loss_views),
                "n_late": n_late, "n_flipped": n_flipped,
                "flip_ratio": (round(n_flipped / n_late, 4)
                               if n_late else None),
                "threshold": f"{LATE_FLIP_NUM}/{LATE_FLIP_DEN}",
                "criterion_met": crit["late_flip_ge_third"],
                "expected_late": 15,
                "n_flipped_win_sensitivity": sum(
                    1 for v in loss_views if v["flipped_win"]),
                "n_flipped_orig_seat_sensitivity": sum(
                    1 for v in loss_views if v["flipped_orig_seat"]),
                "n_lead_then_lost": sum(1 for v in loss_views
                                        if v["lead_then_lost"]),
                "per_game": loss_views,
            },
            "controls": {
                "n_games": len(control_views),
                "n_runs": sum(1 for v in control_views
                              for _ in v.get("final_delta_by_seat", {})),
                "final_delta_min": ctrl_min,
                "final_delta_sum_sensitivity": ctrl_sum,
                "n_negative": sum(1 for v in control_views
                                  if v["final_delta_min"] is not None
                                  and v["final_delta_min"] < 0),
                "criterion_met": crit["control_not_flipped"],
                "per_game": control_views,
            },
            "realized_observation": {
                "observation_only": True, "n": len(realized_obs),
                "mean_delta_px": (round(sum(delta_vals) / len(delta_vals), 2)
                                  if delta_vals else None),
                "mean_delta_px_gain": (round(sum(gain_vals) / len(gain_vals), 2)
                                       if gain_vals else None),
                "per_run": realized_obs,
            },
            "dodge_frontrun": {
                "observation_only": True,
                "dodges_total": dodge_total,
                "front_runs_total": front_total,
                "internal_dodges_total": (int_dodge_total if int_n else None),
                "internal_plan_entries_total": (int_plan_total
                                                if int_n else None),
            },
            "action_throttle": {
                "fire_count_total": fire_total,
                "fire_count_max": fire_max,
                "fire_threshold": FIRE_THRESHOLD,
                "dodge_postpone_total": postpone_total,
                "credit_debited_total": round(credit_total, 2),
                "n_missing_counts": n_fire_missing,
                "criterion_met": crit["action_throttle"],
            },
            "counter_arm": {
                "kind": counter_meta["kind"],
                "config": counter_meta["config"],
                "features": counter_meta["features"],
                "script_path": counter_meta["script_path"],
                "script_sha256": counter_meta["script_sha256"],
                "script": counter_meta["script"],
                "arms": counter_blocks,
                "rate_r39": rate_r39, "rate_r37": rate_r37,
                "n_decided_r39": dec_r39, "n_decided_r37": dec_r37,
                "independent_seeds": True,
                "criterion_met": crit["counter_arm_not_worse"],
            },
            "h2h": h2h_blocks,
        },
        "overall": {
            "criteria": crit,
            "criteria_notes": {
                "control_not_flipped": ("对照资金逐局逐席 min≥0（R19 同源）"),
                "late_flip_ge_third": ("晚崩局翻正 ≥1/3：局级 Δ=双席 min>0"
                                       "（R15/mix_lab 同源）"),
                "h2h_vs_r37_ge_055": ("主对 seed 级 rate≥0.55；辅对 r34a 仅"
                                      "观测"),
                "action_throttle": ("动作降量：重演臂预测写入合计≤1000 且 "
                                    "dodge 推迟语义合计=0（v2 无推迟语义，"
                                    "非零即回归；缺计数 fail-closed）"),
                "counter_arm_not_worse": ("反制臂胜率不降：r39 vs 反制 ≥ "
                                          "r37 vs 反制（独立 seed、双臂皆有"
                                          "决胜局，缺→False）"),
                "realized_px_not_down": ("realized 价不跌：STRAWBERRY "
                                         "delta_px 均值≥0（须有草莓样本）"),
            },
            "pass": overall_pass,
            "verdict": "POSITIVE" if overall_pass else "NEGATIVE",
            "n_red_games": n_red, "n_errors": len(errors),
            "observations": {
                "mean_delta_px_gain": (round(sum(gain_vals) / len(gain_vals), 2)
                                       if gain_vals else None),
                "mean_delta_px": (round(sum(delta_vals) / len(delta_vals), 2)
                                  if delta_vals else None),
                "strawberry_delta_px_mean": (
                    round(sum(straw_vals) / len(straw_vals), 2)
                    if straw_vals else None),
                "dodges_total": dodge_total,
                "front_runs_total": front_total,
                "fire_count_total": fire_total,
                "dodge_postpone_total": postpone_total,
                "credit_debited_total": round(credit_total, 2),
                "h2h_secondary_rate": ((h2h_blocks["secondary"] or {})
                                       .get("h2h_rate")),
                "counter_rate_r39": rate_r39,
                "counter_rate_r37": rate_r37,
            },
        },
        "errors": errors,
        "source": {
            "rerun_command": (
                "cd " + os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))) + " && python3 -m pytest "
                "orderbook_predict/test_judge_predict.py -q && python3 -c "
                "\"import json; from orderbook_predict.judge_predict import "
                "judge_predict_replay; ev = judge_predict_replay("
                + repr(os.path.abspath(pkg_path)) + ", CORPUS); open("
                "'orderbook_predict/evidence/judge_predict_v2_realrun.json', "
                "'w', encoding='utf-8').write(json.dumps(ev, "
                "ensure_ascii=False, indent=1))\""),
            "replay_pull_command": _pull_command("<episode_id>"),
            "replay_cache_dirs": list(cache_dirs),
            "replay_pull_dir": pull_dir,
            "bench": {"main_opponent": cfg["main_opponent"],
                      "secondary_opponent": cfg["secondary_opponent"],
                      "seeds_main": cfg["seeds_main"],
                      "seeds_secondary": cfg["seeds_secondary"],
                      "counter_config": cfg["counter_config"],
                      "counter_baseline": cfg["counter_baseline"],
                      "n_games_counter_r39": cfg["n_games_counter_r39"],
                      "n_games_counter_r37": cfg["n_games_counter_r37"],
                      "seeds_counter_r39": cfg["seeds_counter_r39"],
                      "seeds_counter_r37": cfg["seeds_counter_r37"]},
            "counter": {
                "kind": counter_meta["kind"],
                "config": counter_meta["config"],
                "script_path": counter_meta["script_path"],
                "script_sha256": counter_meta["script_sha256"],
            },
            "wall_s": round(time.perf_counter() - t0, 1),
            "method_notes": [
                "evidence dict 由本函数返回、不落盘；台账文件归实跑编排写入",
                "语料重叠（a22 灾难局 ⊂ r34a 败局）按唯一 episode 去重聚合，"
                "条目级逐条留痕",
                "反制对手件由 make_counter_opponent 生成、落盘临时件装载"
                "（脚本文本全文存 aggregate.counter_arm.script，可复跑复原）",
            ],
        },
    }
    return evidence


def flip_stats(states: Any, baseline: Any,
               internal: Any = None) -> Dict[str, Any]:
    """逐局统计 v2（R22 改造）：晚崩翻转判定（原局后半程被翻 vs 重演结局）、
    撞车品项 realized 价差、避让/抢跑次数；胜局对照终局资金差（不翻负判据）；
    +动作降量面（fire_count/dodge_postpone_count/credit_debited）。

    签名意图：输入: 对局状态序列+原局基线+运行内账 / 输出: {flip, realized,
    dodges, front_runs, fire_count, dodge_postpone_count, credit_debited,
    final_delta, verdict} / 错误: 缺字段→UNKNOWN。

    口径钉（实现与测试同钉；行契约=parse_episode_states 同构逐步双席行
    {step, seat, action, money, inventory, prices}——step/seat/action/money
    必填；inventory/prices 子键有则用、缺即该指标尽力核算/记 None）：

    - **席位**：baseline["our_seat"]=被测件（r38）所坐席；逐行按 seat 分席。
      rerun 终局资金=该席末拍 money；rerun_margin=我席末拍 money−对席末拍
      money。baseline 必填：our_seat/final_money/opp_final_money（原局该席/
      对席终局资金）/margin_d10/margin_d20/margin_final（原局我方队视角资金差
      探针，day 10/20 日终=step day*24+23 截尾）。
    - **晚崩判定（flip.late_collapse）**：loss_phase 主导段口径——三段增量
      （open=margin_d10−0、mid=margin_d20−margin_d10、late=margin_final−
      margin_d20）取最负段为主导（并列取较晚段）；主导=late（d20→终局段）
      →晚崩局。仅 kind="loss" 且 margin_final<0 的败局参与判定（胜局对照/
      非晚崩败局不计，flip.counted=False）；analysis22 group_stats.
      loss_phase_rule 同源（20 败局 late_d20_end=15/mid_d10_20=5）。
      次级标志 flip.lead_then_lost=（margin_d10>0 或 margin_d20>0）留档
      （立项文本「margin_d10>0 或 d20 领先但终局负」字面口径，实测 5/20，
      不进判据）。
    - **翻转判定（flip）**：Δmargin=重演该席 margin（rerun_margin）−原局该席
      margin（final_money−opp_final_money）；本席 flipped=Δmargin>0（R15
      「翻正（Δmargin>0）」同源用语）；局级翻正=双席 Δ 的 min>0（mix_lab/
      R14「局级 Δ=双席位 min>0，保守主口径」），合成在 judge_predict_replay
      聚合层完成。flip.rerun_win=重演 margin>0（W/L 翻转敏感度并列）。
    - **realized 价差（撞车品项）**：品项序 STRAWBERRY/MILK/WOOL/MELON，
      取首个双席皆有 SELL 提交的品项（无→退首个单侧有卖品项并标
      collision=False；全无→item=None 各值 None）。实现价=Σ(成交截断量×
      该拍 prices[item])/Σ成交截断量（成交截断 ex=min(提交量, 邻拍库存
      max)——inv[t−1] 与 inv[t] 的 item 量取 max 后逐单扣减，a22_dissect
      库存差分同构）；缺 prices 子键→实现价 None（note=prices_missing）、
      缺 inventory→成交截断退全额（note=inventory_missing）。realized=
      {item, collision, our_px, opp_px, delta_px(我−对手), our_qty, opp_qty,
      orig_our_px/orig_opp_px/delta_px_gain（baseline["realized"][item] 在
      场才算提升观测，缺即 None）}。
    - **避让/抢跑（动作差分痕迹）**：基准=baseline["sell_flow"]（原局该席
      逐品项 [[step, qty],…] 卖单事件流）对重演我席卖单事件流，逐品项按步序
      FIFO 对齐第 k 张：重演更早=抢跑+1；更晚=避让+1；同步减量=避让+1；
      原局剩单（重演无对应）=避让+1（删除痕迹）；重演多单=抢跑+1（新增痕迹）。
      缺 sell_flow→两计数 None。口径=痕迹计数（近似，动作流整体漂移亦会计
      入），运行内账精确数另由 judge_predict_replay 附记。
    - **final_delta（胜局对照不翻负判据）**：重演我席末拍 money−baseline
      final_money（R19「对照资金 l1/胜局不翻负」同源）；缺基线→None。
    - **动作降量面（v2 新增；运行内账=第三参 internal）**：internal 形
      {"written": [{"item","qty","tier"}…], "plan": [{"market": […]}…],
      "credit_debited": 数值|[{"qty"}…], "dodge_log": [{"item","gate"}…]}，
      裸字段缺时尽力核算：
      - fire_count=预测写入次数（运行内账/plan 写入痕迹计）：internal
        ["fire_count"] 整数 → written 条目数（非空主源）→ plan 槽 SELL
        单计数（written 空/缺时的备源）→ 仅 written 空表=0，皆缺→None；
      - credit_debited=累计减记额：internal["credit_debited"] 数值或条目
        qty 合计 → written 条目 qty 合计（非空）→ plan SELL qty 合计，
        仅 written 空表=0，皆缺→None；
      - dodge_postpone_count=dodge 推迟语义计数：dodge_log 里推迟型记录
        （gate∈{postpone,defer,delay} 或条目 postpone/deferred 真值）计数；
        **v2 件应恒 0**（改2 删「推迟自家卖单」语义，apply_dodge 只出
        allow/deny 门，deny 不算推迟——反例钉：门账+顺延样卖流差分亦记 0）。
    - **verdict**：缺关键字段（行缺 step/seat/action/money、非整 step/seat、
      非数值 money、无双席行、baseline 缺 our_seat/final_money/opp_final_money
      /margin 探针、**运行内账缺/非 dict/fire_count 与 credit_debited 不可
      解析**）或输入为空 → "UNKNOWN"（不抛，指标尽力核算）；否则
      {"kind", "counted", "pass"}——kind=baseline["kind"]（缺省按
      margin_final 符号推：≥0→control）；counted=晚崩局与否（非晚崩不计）；
      pass=对照局 final_delta≥0 / 晚崩局 Δmargin>0 / 其余 None。
    """
    turns_per_day = 24

    def _num(v):
        return (float(v) if isinstance(v, (int, float))
                and not isinstance(v, bool) else None)

    def _is_int(v):
        return isinstance(v, int) and not isinstance(v, bool)

    def _sell_ops(action):
        if isinstance(action, dict):
            market = action.get("market")
        elif isinstance(action, (list, tuple)):
            market = action
        else:
            return
        for op in (market or []):
            if (isinstance(op, (list, tuple)) and len(op) >= 3
                    and op[0] == "SELL" and isinstance(op[1], str)):
                qty = _num(op[2])
                if qty is not None and qty > 0:
                    yield op[1], qty

    # ---- 行扫描（缺关键字段→unknown，指标尽力核算） ----------------------
    unknown = False
    beats = []
    rows = list(states or [])
    for row in rows:
        if not isinstance(row, dict) or "step" not in row or "seat" not in row:
            unknown = True
            continue
        if not _is_int(row["step"]) or not _is_int(row["seat"]):
            unknown = True
            continue
        money = _num(row.get("money"))
        if money is None or row.get("action") is None:
            unknown = True
        inv = row.get("inventory")
        if not isinstance(inv, dict):
            inv = None
        prices = row.get("prices")
        if not isinstance(prices, dict):
            prices = None
        beats.append({
            "step": row["step"], "seat": row["seat"], "money": money,
            "inv": inv, "prices": prices,
            "sells": list(_sell_ops(row.get("action"))),
        })
    beats.sort(key=lambda b: (b["step"], b["seat"]))
    if not beats:
        unknown = True

    # ---- 基线扫描 --------------------------------------------------------
    base = baseline if isinstance(baseline, dict) else {}
    our_seat = base.get("our_seat")
    if not _is_int(our_seat):
        unknown = True
        our_seat = None
    final_money = _num(base.get("final_money"))
    opp_final_money = _num(base.get("opp_final_money"))
    m10 = _num(base.get("margin_d10"))
    m20 = _num(base.get("margin_d20"))
    mfinal = _num(base.get("margin_final"))
    if (final_money is None or opp_final_money is None
            or m10 is None or m20 is None or mfinal is None):
        unknown = True
    kind = base.get("kind")
    if kind not in ("loss", "control"):
        kind = ("control" if (mfinal is not None and mfinal >= 0) else "loss")

    our_beats = [b for b in beats if our_seat is not None
                 and b["seat"] == our_seat]
    opp_beats = [b for b in beats if our_seat is not None
                 and b["seat"] != our_seat]
    if not our_beats or not opp_beats:
        unknown = True

    our_final = our_beats[-1]["money"] if our_beats else None
    opp_final = opp_beats[-1]["money"] if opp_beats else None
    rerun_margin = (our_final - opp_final
                    if our_final is not None and opp_final is not None
                    else None)
    orig_run_margin = (final_money - opp_final_money
                       if final_money is not None
                       and opp_final_money is not None else None)
    delta_margin = (rerun_margin - orig_run_margin
                    if rerun_margin is not None
                    and orig_run_margin is not None else None)

    # ---- 晚崩判定（loss_phase 主导段口径）+ 次级标志 --------------------
    dominant = None
    late_collapse = False
    if (kind == "loss" and mfinal is not None and mfinal < 0
            and m10 is not None and m20 is not None):
        segs = (("open", m10 - 0.0), ("mid", m20 - m10),
                ("late", mfinal - m20))
        minv = min(v for _, v in segs)
        dominant = [name for name, v in segs if v == minv][-1]  # 并列取较晚段
        late_collapse = (dominant == "late")
    lead_then_lost = (bool(m10 > 0 or m20 > 0)
                      if (m10 is not None and m20 is not None) else None)

    flip = {
        "kind": kind,
        "late_collapse": late_collapse,
        "dominant_segment": dominant,
        "lead_then_lost": lead_then_lost,
        "counted": late_collapse,
        "delta_margin": delta_margin,
        "flipped": (delta_margin > 0) if delta_margin is not None else None,
        "rerun_margin": rerun_margin,
        "orig_run_margin": orig_run_margin,
        "rerun_win": (rerun_margin > 0) if rerun_margin is not None else None,
        "margin_d10": m10, "margin_d20": m20, "margin_final": mfinal,
    }

    final_delta = (our_final - final_money
                   if our_final is not None and final_money is not None
                   else None)

    # ---- 撞车品项 realized 价（邻拍库存差分截断） -----------------------
    def _seat_account(seat_sel):
        qty_tot: Dict[str, float] = {}
        val_tot: Dict[str, float] = {}
        priced_qty: Dict[str, float] = {}
        sell_items: Dict[str, list] = {}
        notes: set = set()
        prev_inv: Dict[str, Any] = None
        for b in beats:
            if b["seat"] != seat_sel:
                continue
            if b["inv"] is None:
                inv_prev = {}
                inv_now = {}
                stock_hi = None            # 无库存信息→成交截断退全额
                notes.add("inventory_missing")
            else:
                inv_prev = prev_inv or {}
                inv_now = b["inv"]
                stock_hi = {}
                for k in set(inv_prev) | set(inv_now):
                    stock_hi[k] = max(_num(inv_prev.get(k)) or 0,
                                      _num(inv_now.get(k)) or 0)
            for item, qty in b["sells"]:
                sell_items.setdefault(item, []).append([b["step"], qty])
                if stock_hi is None:
                    ex = float(qty)
                else:
                    ex = max(0.0, min(qty, stock_hi.get(item, 0)))
                    stock_hi[item] = stock_hi.get(item, 0) - ex
                if ex > 0:
                    qty_tot[item] = qty_tot.get(item, 0) + ex
                    px = (b["prices"] or {}).get(item) if b["prices"] else None
                    px = _num(px)
                    if px is not None:
                        val_tot[item] = val_tot.get(item, 0) + ex * px
                        priced_qty[item] = priced_qty.get(item, 0) + ex
                    else:
                        notes.add("prices_missing")
            if b["inv"] is not None:
                prev_inv = b["inv"]
        px_out = {}
        for item, q in qty_tot.items():
            px_out[item] = (round(val_tot[item] / q, 2)
                            if q > 0 and priced_qty.get(item) == q else None)
        return px_out, qty_tot, sell_items, notes

    if our_seat is not None:
        our_px, our_qty, our_flow, our_notes = _seat_account(our_seat)
        opp_px, opp_qty, _opp_flow, opp_notes = _seat_account(1 - our_seat)
    else:
        our_px, our_qty, our_flow = {}, {}, {}
        opp_px, opp_qty = {}, {}
        our_notes, opp_notes = set(), set()
    rz_notes = sorted(our_notes | opp_notes)

    both = [it for it in COLLISION_ITEMS
            if our_qty.get(it) and opp_qty.get(it)]
    any_side = [it for it in COLLISION_ITEMS
                if our_qty.get(it) or opp_qty.get(it)]
    item = both[0] if both else (any_side[0] if any_side else None)
    o_px = our_px.get(item) if item else None
    p_px = opp_px.get(item) if item else None
    delta_px = (o_px - p_px
                if o_px is not None and p_px is not None else None)
    orig_side = (base.get("realized") or {}).get(item) \
        if (item and isinstance(base.get("realized"), dict)) else None
    oo_px = (orig_side or {}).get("our_px") if isinstance(orig_side, dict) else None
    op_px = (orig_side or {}).get("opp_px") if isinstance(orig_side, dict) else None
    orig_delta = (oo_px - op_px
                  if isinstance(oo_px, (int, float))
                  and isinstance(op_px, (int, float)) else None)
    realized = {
        "item": item,
        "collision": bool(both),
        "our_px": o_px, "opp_px": p_px, "delta_px": delta_px,
        "our_qty": our_qty.get(item) if item else None,
        "opp_qty": opp_qty.get(item) if item else None,
        "orig_our_px": oo_px, "orig_opp_px": op_px,
        "orig_delta_px": orig_delta,
        "delta_px_gain": (delta_px - orig_delta
                          if delta_px is not None and orig_delta is not None
                          else None),
        "notes": rz_notes,
    }

    # ---- 避让/抢跑（动作差分痕迹，逐品项 FIFO 对齐） --------------------
    flow = base.get("sell_flow")
    dodges = front_runs = None
    if isinstance(flow, dict):
        dodges = front_runs = 0
        for it in set(flow) | set(our_flow):
            orig = sorted(([int(s), float(q)] for s, q in (flow.get(it) or [])),
                          key=lambda e: e[0])
            rer = sorted(our_flow.get(it) or [], key=lambda e: e[0])
            for k in range(max(len(orig), len(rer))):
                o = orig[k] if k < len(orig) else None
                r = rer[k] if k < len(rer) else None
                if o is not None and r is not None:
                    if r[0] < o[0]:
                        front_runs += 1
                    elif r[0] > o[0]:
                        dodges += 1
                    elif r[1] < o[1]:
                        dodges += 1
                elif o is not None:
                    dodges += 1          # 原局卖单未再现=删除/整单避让痕迹
                else:
                    front_runs += 1      # 重演新增卖单=抢跑痕迹

    # ---- 动作降量面（v2：运行内账/plan 写入痕迹） -------------------------
    def _sum_qty(entries):
        total = 0.0
        for e in entries or []:
            if isinstance(e, dict):
                q = _num(e.get("qty"))
                if q is not None:
                    total += q
        return total

    fire_count = None
    credit_debited = None
    dodge_postpone_count = 0
    acct = internal
    if acct is not None and not isinstance(acct, dict):
        unknown = True
        acct = None
    if isinstance(acct, dict):
        def _plan_sells():
            n, qty = 0, 0.0
            for slot in (acct.get("plan") or []):
                if not isinstance(slot, dict):
                    continue
                for o in (slot.get("market") or []):
                    if (isinstance(o, (list, tuple)) and len(o) >= 1
                            and o[0] == "SELL"):
                        n += 1
                        if len(o) >= 3:
                            qty += _num(o[2]) or 0
            return n, qty

        written = acct.get("written")
        n_written = len(written) if isinstance(written, list) else None
        n_plan, plan_qty = _plan_sells() \
            if isinstance(acct.get("plan"), list) else (None, None)
        raw_fire = acct.get("fire_count")
        if isinstance(raw_fire, int) and not isinstance(raw_fire, bool):
            fire_count = raw_fire
        elif n_written:
            fire_count = n_written          # 写入痕迹主源
        elif n_plan is not None:
            fire_count = n_plan             # plan 写入痕迹备源
        elif n_written is not None:
            fire_count = 0
        raw_credit = acct.get("credit_debited")
        if isinstance(raw_credit, (int, float)) \
                and not isinstance(raw_credit, bool):
            credit_debited = float(raw_credit)
        elif isinstance(raw_credit, list):
            credit_debited = _sum_qty(raw_credit)
        elif n_written:
            credit_debited = _sum_qty(written)
        elif plan_qty is not None:
            credit_debited = plan_qty
        elif n_written is not None:
            credit_debited = 0.0
        log = acct.get("dodge_log")
        if isinstance(log, list):
            for entry in log:
                if not isinstance(entry, dict):
                    continue
                gate = str(entry.get("gate") or "").lower()
                if (gate in ("postpone", "defer", "delay")
                        or entry.get("postpone") or entry.get("deferred")):
                    dodge_postpone_count += 1
    else:
        unknown = True            # 运行内账缺→缺字段（v2 三参契约）
    if fire_count is None or credit_debited is None:
        unknown = True            # 写入/减记痕迹缺→缺字段

    # ---- verdict --------------------------------------------------------
    if unknown:
        verdict: Any = "UNKNOWN"
    else:
        if kind == "control":
            passed = (final_delta is not None and final_delta >= 0)
        elif late_collapse:
            passed = (delta_margin is not None and delta_margin > 0)
        else:
            passed = None                # 非晚崩不计
        verdict = {"kind": kind, "counted": late_collapse, "pass": passed}

    return {"flip": flip, "realized": realized, "dodges": dodges,
            "front_runs": front_runs,
            "fire_count": fire_count,
            "dodge_postpone_count": dodge_postpone_count,
            "credit_debited": credit_debited,
            "final_delta": final_delta,
            "verdict": verdict}


# ===========================================================================
# make_counter_opponent（R22 改4）：反制对手生成（Wool Front-Runner 型）
# ===========================================================================
_COUNTER_DEFAULTS = {"sniff_window": 2, "dump_qty": 48, "anti_shock": True}

# 异常兜底：最简 PASS 对手件（末 callable=agent）
_PASS_SCRIPT = (
    "# -*- coding: utf-8 -*-\n"
    '# 最简 PASS 对手（make_counter_opponent 异常兜底）\n'
    "def agent(obs):\n"
    '    return {"farmer": ["PASS"], "hands": [], "market": []}\n')


def _counter_script(config: Dict[str, Any]) -> str:
    """反制对手脚本文本（纯构造；末 callable=agent）。

    行为三件（R22 改4 / references Q5 WOOL FRONT-RUNNER）：
    ①嗅探=对手（我方）羊 BUY_ANIMAL/剪毛 HARVEST 信号（对手动作流
      obs["opponent_action"]/obs["last_actions"] 对手席可见面；缺即农格差分：
      对手羊数增=BUY_ANIMAL、对手羊格 yield_units 落=HARVEST）；
    ②嗅探命中后提前 sniff_window（1-2）回合集中倒毛（WOOL 集中 SELL
      dump_qty 一次，抢在对手剪毛后卖流之前出货）；
    ③Anti-Shock：step-1 不跟大单、吸收麦冲击（step≤1 不出市场单、保现金）。
    任何运行异常→PASS 动作。config 已由 make_counter_opponent 校验。
    """
    return (
        "# -*- coding: utf-8 -*-\n"
        "# 反制对手（R22 make_counter_opponent 生成）：Wool Front-Runner 型\n"
        "# ①嗅探对手羊 BUY_ANIMAL/剪毛 HARVEST 信号（动作流或农格差分）\n"
        "# ②命中后提前 sniff_window(1-2) 回合集中倒毛 WOOL\n"
        "# ③Anti-Shock：step-1 不跟大单、吸收麦冲击\n"
        "_CFG = %r\n"
        "\n"
        "\n"
        "def _make_agent():\n"
        "    st = {\"dump_at\": None, \"opp_animals\": None, \"opp_yield\": None}\n"
        "\n"
        "    def _get(obs, key, default=None):\n"
        "        if isinstance(obs, dict):\n"
        "            return obs.get(key, default)\n"
        "        return getattr(obs, key, default)\n"
        "\n"
        "    def _int(v, default=0):\n"
        "        try:\n"
        "            if isinstance(v, bool):\n"
        "                return default\n"
        "            return int(v)\n"
        "        except Exception:\n"
        "            return default\n"
        "\n"
        "    def _sniff(obs):\n"
        "        player = _int(_get(obs, \"player\", 0), 0)\n"
        "        opp = 1 - player\n"
        "        farms = _get(obs, \"farms\") or []\n"
        "        farm = {}\n"
        "        if isinstance(farms, (list, tuple)) and 0 <= opp < len(farms) \\\n"
        "                and isinstance(farms[opp], dict):\n"
        "            farm = farms[opp]\n"
        "        animals, yld = 0, 0\n"
        "        for row in (farm.get(\"tiles\") or []):\n"
        "            if not isinstance(row, (list, tuple)):\n"
        "                continue\n"
        "            for tile in row:\n"
        "                if isinstance(tile, dict) and tile.get(\"animal\"):\n"
        "                    animals += 1\n"
        "                    yld += _int(tile.get(\"yield_units\"), 0)\n"
        "        act = _get(obs, \"opponent_action\")\n"
        "        if not isinstance(act, dict):\n"
        "            la = _get(obs, \"last_actions\")\n"
        "            if isinstance(la, (list, tuple)) and 0 <= opp < len(la):\n"
        "                act = la[opp]\n"
        "        hit = False\n"
        "        if isinstance(act, dict):\n"
        "            for o in (act.get(\"market\") or []):\n"
        "                if isinstance(o, (list, tuple)) and len(o) >= 2 \\\n"
        "                        and o[0] == \"BUY_ANIMAL\":\n"
        "                    hit = True\n"
        "            for u in [act.get(\"farmer\")] + list(act.get(\"hands\") or []):\n"
        "                if isinstance(u, (list, tuple)) and len(u) >= 1 \\\n"
        "                        and u[0] == \"HARVEST\":\n"
        "                    hit = True\n"
        "        if st[\"opp_animals\"] is not None and animals > st[\"opp_animals\"]:\n"
        "            hit = True\n"
        "        if st[\"opp_yield\"] is not None and yld < st[\"opp_yield\"]:\n"
        "            hit = True\n"
        "        st[\"opp_animals\"], st[\"opp_yield\"] = animals, yld\n"
        "        return hit\n"
        "\n"
        "    def agent(obs):\n"
        "        try:\n"
        "            raw_step = _get(obs, \"step\")\n"
        "            if raw_step is None:\n"
        "                step = _int(_get(obs, \"day\"), 0) * 24 \\\n"
        "                    + _int(_get(obs, \"hour\"), 0)\n"
        "            else:\n"
        "                step = _int(raw_step, None)\n"
        "                if step is None:\n"
        "                    return {\"farmer\": [\"PASS\"], \"hands\": [], \"market\": []}\n"
        "            action = {\"farmer\": [\"PASS\"], \"hands\": [], \"market\": []}\n"
        "            if _sniff(obs) and st[\"dump_at\"] is None:\n"
        "                lead = 1 if _CFG[\"sniff_window\"] <= 1 else 2\n"
        "                st[\"dump_at\"] = step + lead\n"
        "            # Anti-Shock：step-1 不跟大单、吸收麦冲击（该拍不出市场单）\n"
        "            if _CFG[\"anti_shock\"] and step <= 1:\n"
        "                return action\n"
        "            if st[\"dump_at\"] is not None and step >= st[\"dump_at\"]:\n"
        "                action[\"market\"] = [[\"SELL\", \"WOOL\", _CFG[\"dump_qty\"]]]\n"
        "                st[\"dump_at\"] = None\n"
        "            return action\n"
        "        except Exception:\n"
        "            return {\"farmer\": [\"PASS\"], \"hands\": [], \"market\": []}\n"
        "    return agent\n"
        "\n"
        "\n"
        "agent = _make_agent()\n") % (config,)


def _counter_factory(script_text: str):
    """脚本文本 → callable 工厂（每次调用全新命名空间装载，末 callable=对手）。"""

    def make():
        env: Dict[str, Any] = {}
        exec(compile(script_text, "<counter_opponent>", "exec"), env)
        callables_ = [v for v in env.values() if callable(v)]
        if not callables_:
            raise ValueError("反制对手件装载后无 callable")
        return callables_[-1]

    return make


def make_counter_opponent(config: Any) -> Any:
    """反制对手生成（R22 改4）：Wool Front-Runner 型——嗅探对手羊提交/剪毛窗
    →提前 1-2 回合集中倒毛 + Anti-Shock 吸收 step-1 麦冲击；输出可装载
    对手件（脚本文本或 callable 工厂）+特征说明。

    签名意图：输入: 配置（嗅探窗/倒毛量） / 输出: 对手件路径或工厂 /
    错误: 配置畸形即抛。

    口径钉（实现与测试同钉）：
    - 输出=对手件 dict：{"kind", "config", "features", "script", "factory"}。
      script=对手脚本文本（自包含、末 callable=agent，形态与 v1 闭环副证
      phase_b.load_l3_callable 的对手装载兼容）；factory=callable 工厂
      （factory()→全新对手 callable，每局新状态，内部 exec 同一 script 文本
      证明装载面恒等）；features=对手特征说明。
    - config={"sniff_window", "dump_qty", "anti_shock"}，缺省留档
      {"sniff_window": 2, "dump_qty": 48, "anti_shock": True}：
      sniff_window=嗅探命中后集中倒毛的提前回合窗（限 1-2，契约「提前 1-2
      回合」）；dump_qty=集中倒毛量（WOOL 集中 SELL 一次，限 1-99）；
      anti_shock=step-1 不跟大单、吸收麦冲击（step≤1 不出市场单）。
    - 行为：①嗅探对手（我方）羊 BUY_ANIMAL/剪毛 HARVEST 信号（对手动作流
      obs["opponent_action"]/obs["last_actions"] 对手席；缺即农格差分：对手
      羊数增/对手羊格 yield_units 落）→②命中后提前 sniff_window 回合集中
      倒毛（["SELL","WOOL",dump_qty] 一次）→③Anti-Shock。
    - 错误：config 非 dict/含未知键/sniff_window 非 1-2 整数/dump_qty 非
      1-99 整数/anti_shock 非 bool → ValueError（配置畸形即抛）；生成期任何
      其他异常→最简 PASS 对手（kind="pass_fallback"，agent 恒 PASS）。
    """
    # ---- 配置校验（畸形即抛，fail-closed） -------------------------------
    if config is None:
        config = {}
    if not isinstance(config, dict):
        raise ValueError(f"配置畸形：config 应为 dict，实为 {type(config).__name__}")
    unknown = set(config) - set(_COUNTER_DEFAULTS)
    if unknown:
        raise ValueError(f"配置畸形：未知配置键 {sorted(unknown)}")
    cfg = dict(_COUNTER_DEFAULTS)
    cfg.update(config)
    sw = cfg["sniff_window"]
    if isinstance(sw, bool) or not isinstance(sw, int) or not 1 <= sw <= 2:
        raise ValueError(f"配置畸形：sniff_window 须为 1-2 整数，实为 {sw!r}")
    dq = cfg["dump_qty"]
    if isinstance(dq, bool) or not isinstance(dq, int) or not 1 <= dq <= 99:
        raise ValueError(f"配置畸形：dump_qty 须为 1-99 整数，实为 {dq!r}")
    if not isinstance(cfg["anti_shock"], bool):
        raise ValueError(f"配置畸形：anti_shock 须为 bool，实为 {cfg['anti_shock']!r}")

    def _features(kind):
        return {
            "name": ("Wool Front-Runner 反制对手" if kind == "wool_front_runner"
                     else "最简 PASS 对手（兜底）"),
            "sniff": ("对手羊 BUY_ANIMAL/剪毛 HARVEST 信号（动作流 "
                      "opponent_action/last_actions 对手席或农格差分）"),
            "dump": (f"嗅探命中后提前 {cfg['sniff_window']} 回合集中倒毛："
                     f"WOOL 集中 SELL {cfg['dump_qty']} 一次"),
            "anti_shock": ("step-1 不跟大单、吸收麦冲击（step≤1 不出市场单）"
                           if cfg["anti_shock"] else "关闭"),
            "fallback": "异常→最简 PASS 对手",
            "defaults": dict(_COUNTER_DEFAULTS),
        }

    # ---- 生成（生成期异常→最简 PASS 对手） -------------------------------
    try:
        script_text = _counter_script(cfg)
        compile(script_text, "<counter_opponent>", "exec")   # 自检可编译
        factory = _counter_factory(script_text)
        return {"kind": "wool_front_runner", "config": cfg,
                "features": _features("wool_front_runner"),
                "script": script_text, "factory": factory}
    except Exception:
        cfg_fallback = dict(_COUNTER_DEFAULTS)
        return {"kind": "pass_fallback", "config": cfg_fallback,
                "features": _features("pass_fallback"),
                "script": _PASS_SCRIPT, "factory": _counter_factory(_PASS_SCRIPT)}
