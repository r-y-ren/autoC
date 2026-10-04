"""evaluate_ablation_tree（L1，R4，**v2 分阶段混合适应度**）。职责与验收
详见 fn_work/tape_gen/fn_docs/responsibility.md。

消融树评估：候选（库件 × 反射层配置）→ 分阶段混合适应度 +
稀疏惩罚（λ×启用模块数计入代价）。

**v2（2026-09-23 用户裁决，R5 适应度 v2）**：动机 = T4 M1 0/16 市场
耦合假说——v1 适应度（仅真实对手回放流）对普通对手 0.47 但对同级产者
（纯 v48）0.0，适应度必须含同级产者维度。分阶段：

* **粗筛 = 留出流 seated 不变**（每候选 ≤coarse_games 局种子化子样本，
  320 候选保预算；不混 h2h）；支持注入 v1 预评粗筛底表（payload
  ["coarse_rows"]——复用时跳过粗筛评估并登记 coarse_reused）。
* **精评 = top-K（K ≤ FINE_TOP_K_CAP=12）混入 h2h 臂**：每候选
  ① fine_games（v2 = 留出局集，payload["fine_games"]；缺省退化=games）
  seated 评估 + ② 对纯 v48 引擎对打 h2h_games（缺省 4 局 = 2 种子×
  AB/BA 席，≥4 契约下限；与 T4 M1 同通道：官方真引擎、席位显式、
  逐局全新装载）。
* **混合分 = 0.5×留出胜率 + 0.5×h2h 互胜 − λ×启用模块数**（两臂平局
  都计 0.5；h2h 臂缺行时退化为 v1 语义并留痕 h2h_missing——预算截断
  如实分档，不编数）。
* 精化（阈值微轴邻域）与 finalists 排序同用混合分；墙钟硬帽
  tiers["wall_clock_budget_s"]（v2 跑批登记 9000s=2.5h）——分级控预算，
  超帽截断留痕（R4 错误语义）。

* 反射层真值 = v48 深读档模块（fn_docs/hybrid/results/2026-09-23-v48-
  coordination-deepread/modules/，只读 import）：clone_preempt=
  v44.gold_floor.CloneSellPreemption（horizon=2↔0 开关，v48 gold 参数）、
  slot_reorder=v23.policy_library.reorder_sell_slots（legacy alpha=0 影响
  分槽位排序，v48 原生形态）、market_maker=v24.market_maker.
  MarketMakerExpert（v44 接线参数；v48 编译未启用——本搜索检验启用是否
  有益）、终局强改=scripts.v19_terminal.terminal_market(step 718,
  rule=collision, replace=True)。磁带底座 = replay_policy+wrap_weed_repair
  （机制基底，非开关轴）。
* **新增保险层（我方死价护栏）**：本文件实现——窗口 [0,700) 内，live 报价
  （obs.market.prices，缺省回退 market_price(item, inventory)）≤ ratio×
  market_price(item, 0)（新鲜市场基线）的 SELL 递延入 pending FIFO；每步
  先尝试 flush 报价恢复的 pending（市单项数 ≤10 封顶）；step ≥700 全量
  冲销（贱卖优于作废）。确定性：无随机源，逐席状态 step 0/回退复位。
* seated 评估 = rollout_with_replay_opponent（fn_work/src/
  run_official_bench，双席注入已修复版）：候选注入我席（me_seat=对手席
  对席），对手真实动作流注入对席，整季重演得双席终局资金 → 胜/平/负 +
  边际（我−对手）。评估器可注入（payload["evaluator"]，测试用假评估器，
  契约见 SeatedEvaluator.__call__）；缺省真实评估器 **batch 游戏主序**
  （每回放文件仅解析一次——单件 >30MB，候选主序不可承受）。
* 预算分级：粗筛（训练集子样本，每候选 ≤coarse_games 局，种子化）→ 精评
  （top-K：fine_games seated + h2h 臂）→ 阈值微轴精化（最佳配置邻域，
  可选）→ finalists（top-N）。墙钟预算耗尽 → 取已评最优并标注
  （R4 错误语义；h2h 臂截断候选留痕 h2h_missing）。
* 稀疏惩罚：score = winrate − λ×enabled_modules（λ 默认 0.02 登记可调）；
  同适应度取更稀疏枝（排序键 (-score, enabled_modules, candidate_id)）。

确定性：候选序、子样本、排序全种子化/规范序；不含墙钟（墙钟入
runtime_stats，不进账本）。
"""

from __future__ import annotations

import copy
import json
import time
from pathlib import Path

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_LIBRARY_DIR = _TAPE_GEN_ROOT / "library"
#: v48 深读档模块目录（反射层真值，只读 import）。
DEFAULT_DEEPREAD_MODULES = (_CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results"
                            / "2026-09-23-v48-coordination-deepread"
                            / "modules")

#: 反射层开关面（固定位序——candidate id 掩码与稀疏计数都依赖它）。
SWITCH_ORDER = (
    "clone_preempt",
    "slot_reorder",
    "market_maker",
    "terminal_forced",
    "dead_price_guard",
)

#: 阈值微轴缺省（v48 gold 真值 / 护栏缺省）。
DEFAULT_THRESHOLDS = {"clone_streak_required": 24, "dead_guard_ratio": 0.5}

#: v48 gold 反射层参数（v48_hybrid/main.py _V48_GOLD_CONFIG 真值转录；
#: horizon/terminal_rule 由开关面改写，故不在此列）。
V48_GOLD_PARAMS = {
    "clone_distance_threshold": 2.0,
    "clone_detection_start": 48,
    "clone_active_start": 160,
    "clone_maximum_batch": 10,
    "clone_veto_enabled": True,
    "clone_veto_step": 120,
    "clone_veto_first_shop": "BAKERY",
    "clone_veto_minimum_sheep": 4,
    "clone_veto_maximum_cows": 1,
    "clone_veto_minimum_wheat": 8,
    "clone_veto_minimum_melons": 7,
    "clone_veto_maximum_geese": 0,
    "clone_phase_detector": False,
}

#: 死价护栏窗口（与 v48 clone 窗 [160,700) 同上限；终局前必须冲销）。
GUARD_ACTIVE_STOP = 700
#: 每回合市单项数上限（引擎 maxMarketOrdersPerTurn）。
MAX_ORDERS_PER_TURN = 10

#: v2 精评 top-K 帽（契约：K ≤ 12）。
FINE_TOP_K_CAP = 12
#: v2 h2h 臂缺省局规格（seed×seat）：M1 通道种子域（run_m1_m2_gates.
#: H2H_SEEDS）两块各 1 种子 × AB/BA 席 = 4 局/候选（≥4 契约下限）。
DEFAULT_H2H_GAMES = ((101, 0), (101, 1), (201, 0), (201, 1))
#: v2 混合分两臂权重（用户裁决 0.5/0.5）。
MIXED_WEIGHTS = (0.5, 0.5)

_modules_ready = False


def _load_deepread(path=None):
    """把深读档 modules/ 插入 sys.path（只读；进程内一次）。"""
    global _modules_ready
    import sys
    root = Path(path) if path else DEFAULT_DEEPREAD_MODULES
    if not _modules_ready:
        if not (root / "v44" / "gold_floor.py").is_file():
            raise ValueError(f"deepread modules missing (fail-closed): "
                             f"{root}")
        sys.path.insert(0, str(root))
        _modules_ready = True
    return root


def _to_plain_obs(obs, step=None):
    """twin Observation（属性视图）→ 顶层 plain dict（深读档组件 obs.get
    契约）；嵌套结构原样传递。step：obs.step 为 None（seat1 twin 语义）
    时的计数器步号覆写。"""
    raw_step = getattr(obs, "step", None) if step is None else step
    return {
        "farms": obs.farms,
        "market": obs.market,
        "town": obs.town,
        "day": obs.day,
        "hour": obs.hour,
        "step": raw_step,
        "player": obs.player,
        "private": obs.private,
        "remainingOverageTime": obs.remainingOverageTime,
    }


class DeadPriceGuard:
    """我方死价护栏（新增保险层，本管线自有件——非 v48 移植）。

    语义（确定性，逐席状态，step 0/回退复位）：
    * 窗口 [0, GUARD_ACTIVE_STOP)：对 action.market 中每笔 SELL，若 live
      报价 ≤ ratio × market_price(item, 0)（新鲜基线）→ 从本步撤单、
      (item, qty) 入 pending FIFO；
    * 每步先 flush：pending 中报价已恢复（> ratio×基线）的项按 FIFO 重发
      于 market 首，总项数 ≤ MAX_ORDERS_PER_TURN；
    * step ≥ GUARD_ACTIVE_STOP：不再递延，pending 全量冲销（贱卖优于作废
      ——夜里棚溢弃件是纯损失），本步 SELL 原样放行。
    """

    def __init__(self, ratio: float, modules_path=None):
        self.ratio = float(ratio)
        _load_deepread(modules_path)
        from scripts.v22_market_impact import market_price
        self._market_price = market_price
        self.baseline = {
            item: market_price(item, 0)
            for item in (
                "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                "EGG", "MILK", "WOOL", "FERTILIZER")
        }
        self.states = {0: {}, 1: {}}
        self.telemetry = {"games": 0, "deferred_units": 0,
                          "deferred_orders": 0, "flushed_units": 0,
                          "flushed_orders": 0, "late_flush_units": 0}

    def _reset(self, seat: int, step: int) -> dict:
        state = {"last_step": step, "pending": []}
        self.states[seat] = state
        self.telemetry["games"] += 1
        return state

    def _quote(self, obs: dict, item: str) -> float:
        market = obs.get("market") or {}
        prices = market.get("prices") if isinstance(market, dict) else None
        quote = (prices or {}).get(item)
        if quote is None:
            inventory = (market.get("inventory") or {}) \
                if isinstance(market, dict) else {}
            quote = self._market_price(item, int(inventory.get(item, 10000)
                                                 or 0))
        return float(quote or 0.0)

    def _dead(self, obs: dict, item: str) -> bool:
        floor = float(self.baseline.get(item, 0)) * self.ratio
        return self._quote(obs, item) <= floor

    def apply(self, obs: dict, action: dict) -> dict:
        result = copy.deepcopy(action)
        market = [list(o) for o in (result.get("market") or [])]
        step = int(obs.get("step", 0) or 0)
        seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
        state = self.states[seat]
        if step == 0 or step < int(state.get("last_step", -1)):
            state = self._reset(seat, step)
        state["last_step"] = step

        pending = state["pending"]
        flushed = []
        # ---- flush：报价恢复（或已过窗）的 pending 先重发（FIFO）----
        if pending:
            alive = [row for row in list(pending)
                     if step >= GUARD_ACTIVE_STOP
                     or not self._dead(obs, str(row[0]))]
            for row in alive:
                if len(market) + len(flushed) >= MAX_ORDERS_PER_TURN:
                    break
                flushed.append(["SELL", str(row[0]), int(row[1])])
                pending.remove(row)
            if flushed:
                market = flushed + market[:MAX_ORDERS_PER_TURN
                                          - len(flushed)]
                self.telemetry["flushed_orders"] += len(flushed)
                self.telemetry["flushed_units"] += sum(
                    int(o[2]) for o in flushed)
        # ---- 递延：窗口内死价 SELL 撤单入 pending ----
        if step < GUARD_ACTIVE_STOP:
            kept = []
            for order in market:
                if (len(order) >= 3 and order[0] == "SELL"
                        and order[1] in self.baseline
                        and self._dead(obs, str(order[1]))):
                    pending.append((str(order[1]), max(0, int(order[2] or 0))))
                    self.telemetry["deferred_orders"] += 1
                    self.telemetry["deferred_units"] += max(
                        0, int(order[2] or 0))
                else:
                    kept.append(order)
            market = kept
            if pending and step == GUARD_ACTIVE_STOP - 1:
                # 窗末兜底：未恢复的 pending 贱卖冲销（下一分支已见不到）
                for item, qty in list(pending):
                    if len(market) >= MAX_ORDERS_PER_TURN:
                        break
                    market.append(["SELL", item, int(qty)])
                    pending.remove((item, qty))
                    self.telemetry["late_flush_units"] += int(qty)
        result["market"] = market[:MAX_ORDERS_PER_TURN]
        return result


def build_candidate_agent(tape, config, modules_path=None):
    """库件磁带 + 反射层配置 → twin 通道可调用 agent（fn(obs)->action）。

    config = {switches: {SWITCH_ORDER 五键}, thresholds:
    {clone_streak_required, dead_guard_ratio}}。组装序（v48/v44 接线保
    序）：磁带底座(replay_policy+weed_repair) → slot_reorder →
    clone_preempt → market_maker → 死价护栏 → 终局强改(step 718)。
    """
    switches = {name: bool(config.get("switches", {}).get(name, False))
                for name in SWITCH_ORDER}
    thresholds = dict(DEFAULT_THRESHOLDS)
    thresholds.update(config.get("thresholds") or {})
    tape = copy.deepcopy(tape)
    if not isinstance(tape, list) or not tape:
        raise ValueError("tape must be a non-empty step list (fail-closed)")
    _load_deepread(modules_path)
    from scripts.v21_route_memory_search import replay_policy
    from scripts.v22_weed_repair import wrap_weed_repair
    from v23.policy_library import reorder_sell_slots
    from v44.gold_floor import CloneSellPreemption, GoldFloorConfig
    from v24.market_maker import MarketMakerConfig, MarketMakerExpert
    from scripts.v19_terminal import terminal_market

    base = wrap_weed_repair(replay_policy(copy.deepcopy(tape)),
                            copy.deepcopy(tape), replay_steps=8)
    gold_params = dict(V48_GOLD_PARAMS)
    gold_params["clone_preempt_horizon"] = \
        2 if switches["clone_preempt"] else 0
    gold_params["clone_streak_required"] = int(
        thresholds["clone_streak_required"])
    gold_params["terminal_rule"] = "none"  # 终局由本组装器显式接线
    preemption = CloneSellPreemption(
        {"default": tape}, GoldFloorConfig(**gold_params))
    maker = MarketMakerExpert(
        copy.deepcopy(tape),
        MarketMakerConfig(enabled=True, item="WHEAT", feed_item="WHEAT",
                          start_step=260, stop_entry_step=716, max_batch=10,
                          minimum_expected_profit=25.0,
                          mirror_minimum_expected_profit=25.0,
                          minimum_cash_reserve=2500.0, feed_days_reserve=2.0,
                          investment_horizon=2, shed_headroom=15)) \
        if switches["market_maker"] else None
    guard = DeadPriceGuard(float(thresholds["dead_guard_ratio"]),
                           modules_path) \
        if switches["dead_price_guard"] else None
    taken = {"n": 0}

    def agent(obs):
        # twin 只维护 seat0 的 obs.step（seat1 恒 None——legacy_software
        # twin.py new_state_from_replay_head/step 的既有语义）；me_seat=1
        # 时用闭包步计数器补步号：注入点恒 0、每步恰一次调用，计数=真步号。
        raw_step = getattr(obs, "step", None)
        if raw_step is not None:
            step = int(raw_step)
        else:
            step = taken["n"]
        taken["n"] = step + 1
        d = _to_plain_obs(obs, step)
        result = base(d)
        if switches["slot_reorder"]:
            result = reorder_sell_slots(d, result, None, demand_alpha=0.0)
        result = preemption.apply(d, result, "default", None)
        if maker is not None:
            result = maker.apply(d, result, None)
        if guard is not None:
            result = guard.apply(d, result)
        if step == 718 and switches["terminal_forced"]:
            result = terminal_market(d, result, rule="collision",
                                     replace=True)
        return result

    agent.switches = switches
    agent.thresholds = thresholds
    return agent


def load_library_tapes(library_dir=None):
    """候选库面：routes.json + market_variants.json → {件id: 磁带}。"""
    library_dir = Path(library_dir) if library_dir else DEFAULT_LIBRARY_DIR
    tapes = {}
    routes_path = library_dir / "routes.json"
    variants_path = library_dir / "market_variants.json"
    if routes_path.is_file():
        for name, tape in json.loads(
                routes_path.read_text(encoding="utf-8")).items():
            tapes[f"route:{name}"] = tape
    if variants_path.is_file():
        for name, tape in json.loads(
                variants_path.read_text(encoding="utf-8")).items():
            tapes[f"variant:{name}"] = tape
    if not tapes:
        raise ValueError(f"candidate library empty (fail-closed): "
                         f"{library_dir}")
    return tapes


def enabled_modules_count(switches) -> int:
    return sum(1 for name in SWITCH_ORDER if bool(switches.get(name)))


class SeatedEvaluator:
    """真实 seated 评估器（twin 孪生通道；batch=游戏主序省解析）。

    __call__(candidate, games) 与 batch(candidates, games)（游戏主序，
    每回放解析一次）契约一致：{candidate_id: 行集}，行集 =
    {"games": [{episode_id, opponent, me_seat, win, draw, margin}],
     "n", "wins", "draws", "losses", "winrate"(平局 0.5), "margin_mean"}。
    stats 记录 rollout 计数（供 runtime_stats；不进账本）。
    """

    def __init__(self, library_dir=None, modules_path=None):
        self.tapes = load_library_tapes(library_dir)
        self.modules_path = modules_path
        self._replay = None
        self._replay_path = None
        self.stats = {"rollouts": 0, "replay_loads": 0,
                      "games_evaluated": 0}

    def _agent_for(self, candidate):
        tape = self.tapes.get(candidate["piece"])
        if tape is None:
            raise ValueError(f"unknown library piece (fail-closed): "
                             f"{candidate['piece']}")
        return build_candidate_agent(tape, candidate, self.modules_path)

    def _load_replay(self, path):
        if self._replay_path != path:
            self._replay = json.loads(
                Path(path).read_text(encoding="utf-8"))
            self._replay_path = path
            self.stats["replay_loads"] += 1
        return self._replay

    def _row(self, agent, game, replay, rollout):
        finals = rollout(replay, 0, agent, int(game["me_seat"]))
        self.stats["rollouts"] += 1
        me, opp = int(game["me_seat"]), int(game["opp_seat"])
        margin = float(finals[me]) - float(finals[opp])
        return {
            "episode_id": int(game["episode_id"]),
            "opponent": game.get("opponent"),
            "me_seat": me,
            "win": margin > 0,
            "draw": margin == 0,
            "margin": margin,
            "finals": [float(finals[0]), float(finals[1])],
        }

    @staticmethod
    def _summarize(candidate, rows):
        wins = sum(1 for r in rows if r["win"])
        draws = sum(1 for r in rows if r["draw"] and not r["win"])
        return {
            "candidate_id": candidate["id"],
            "games": rows,
            "n": len(rows),
            "wins": wins,
            "draws": draws,
            "losses": len(rows) - wins - draws,
            "winrate": (wins + 0.5 * draws) / len(rows) if rows else 0.0,
            "margin_mean": (sum(r["margin"] for r in rows) / len(rows))
            if rows else 0.0,
        }

    def batch(self, candidates, games):
        """游戏主序：每回放解析一次，内层循环候选（省 I/O 与解析）。
        每局为每候选新建 agent（步计数器与反射层状态逐局归零——twin
        seat1 的 obs.step=None 语义下计数器不跨局）。"""
        import sys
        src_root = str(_CAMPAIGN_ROOT / "fn_work" / "src")
        if src_root not in sys.path:
            sys.path.insert(0, src_root)
        from run_official_bench.rollout_with_replay_opponent import \
            rollout_with_replay_opponent
        results = {c["id"]: [] for c in candidates}
        for game in games:
            replay = self._load_replay(game["replay_path"])
            for candidate in candidates:
                agent = self._agent_for(candidate)
                row = self._row(agent, game, replay,
                                rollout_with_replay_opponent)
                results[candidate["id"]].append(row)
                self.stats["games_evaluated"] += 1
        return {cid: self._summarize(
            next(c for c in candidates if c["id"] == cid), rows)
            for cid, rows in results.items()}

    def __call__(self, candidate, games):
        return self.batch([candidate], games)[candidate["id"]]


def _call_evaluator(evaluator, candidates, games):
    """评估器适配：有 batch（游戏主序）用 batch；否则逐候选 __call__。"""
    batch = getattr(evaluator, "batch", None)
    if callable(batch):
        return batch(candidates, games)
    return {c["id"]: evaluator(c, games) for c in candidates}


def _Random(seed):
    """标准库随机源（独立实例，不染全局状态）。"""
    import random
    return random.Random(seed)


def _coarse_subsample(games, n, seed):
    """种子化训练子样本：优先对手互异（162 局 157 对手，可全异）。"""
    rng = _Random(seed)
    ordered = sorted(games, key=lambda g: (g["episode_id"],
                                           int(g["opp_seat"])))
    shuffled = list(ordered)
    rng.shuffle(shuffled)
    picked, seen = [], set()
    for game in shuffled:
        if len(picked) >= n:
            break
        if game["opponent"] in seen:
            continue
        seen.add(game["opponent"])
        picked.append(game)
    for game in shuffled:  # 对手互异不足时回填
        if len(picked) >= n:
            break
        if game not in picked:
            picked.append(game)
    return sorted(picked, key=lambda g: (g["episode_id"],
                                         int(g["opp_seat"])))


def score_row(entry, candidate, lambda_sparse):
    """稀疏惩罚评分：score = winrate − λ×启用模块数。"""
    return entry["winrate"] - lambda_sparse * candidate["enabled_modules"]


def mixed_score(seated_entry, h2h_entry, candidate, lambda_sparse):
    """v2 混合适应度：0.5×留出（seated）胜率 + 0.5×h2h 互胜 − λ×模块数。

    h2h_entry=None → v1 语义退化（seated 胜率 − λ×模块数；无 h2h 臂/
    截断留痕候选的同源账本分）。两臂 winrate 均平局计 0.5。"""
    seated = float(seated_entry["winrate"]) if seated_entry else 0.0
    if h2h_entry is None:
        return seated - lambda_sparse * candidate["enabled_modules"]
    return (MIXED_WEIGHTS[0] * seated + MIXED_WEIGHTS[1]
            * float(h2h_entry["winrate"])
            - lambda_sparse * candidate["enabled_modules"])


class H2HEvaluator:
    """真实 h2h 臂评估器（官方真引擎；与 T4 M1 同通道）。

    __call__(candidate, games)：games = [(seed, seat), ...]。每局：候选
    callable（build_candidate_agent **逐局新建**——步计数器/反射层状态
    归零）落 seat 席、纯 v48（load_submission_agent **逐局全新装载**，
    M1 _play_h2h_series 同纪律）落对席 → engine_game 整季 → margin =
    rewards[seat] − rewards[1−seat]。行集与 SeatedEvaluator 同形
    （winrate 平局 0.5；明细 seed/me_seat/margin/finals/statuses/turns
    ——**无墙钟字段**，账本确定性面）。

    stats 记录引擎局数（供 runtime_stats；不进账本）。
    """

    def __init__(self, library_dir=None, modules_path=None, base_main=None):
        self.tapes = load_library_tapes(library_dir)
        self.modules_path = modules_path
        self.base_main = base_main
        self.stats = {"engine_games": 0, "h2h_candidates": 0}

    def __call__(self, candidate, games):
        import sys
        src_root = str(_TAPE_GEN_ROOT / "src")
        if src_root not in sys.path:
            sys.path.insert(0, src_root)
        from assemble_and_gate.run_m1_m2_gates import (
            PURE_V48_MAIN,
            engine_game,
            load_submission_agent,
        )
        tape = self.tapes.get(candidate["piece"])
        if tape is None:
            raise ValueError(f"unknown library piece (fail-closed): "
                             f"{candidate['piece']}")
        base_main = str(self.base_main) if self.base_main \
            else str(PURE_V48_MAIN)
        rows = []
        for seed, seat in games:
            me = int(seat)
            agent = build_candidate_agent(tape, candidate,
                                          self.modules_path)
            pair = [load_submission_agent(base_main),
                    load_submission_agent(base_main)]
            pair[me] = agent          # 候选显式落 me 席（M1 同语义）
            rec = engine_game(pair[0], pair[1], int(seed))
            self.stats["engine_games"] += 1
            rewards = [float(r) for r in rec["rewards"]]
            margin = rewards[me] - rewards[1 - me]
            rows.append({
                "seed": int(seed),
                "opponent": "pure_v48",
                "me_seat": me,
                "win": margin > 0,
                "draw": margin == 0,
                "margin": margin,
                "finals": rewards,
                "statuses": rec["statuses"],
                "turns": rec["turns_played"],
            })
        self.stats["h2h_candidates"] += 1
        summary = SeatedEvaluator._summarize(candidate, rows)
        summary["all_done"] = all(r["statuses"] == ["DONE", "DONE"]
                                  for r in rows)
        return summary


def _rank_rows(rows_by_id, candidates_by_id, lambda_sparse, h2h_by_id=None):
    """排序键 (-score, enabled_modules, candidate_id)：同分取更稀疏枝。

    v2：h2h_by_id 给出该候选 h2h 行（None=无）时用混合分
    （mixed_score），否则 v1 稀疏惩罚分（score_row）——粗筛恒为后者。"""
    decorated = []
    for cid, entry in rows_by_id.items():
        candidate = candidates_by_id[cid]
        h2h = (h2h_by_id or {}).get(cid)
        decorated.append((
            -mixed_score(entry, h2h, candidate, lambda_sparse),
            int(candidate["enabled_modules"]),
            cid,
        ))
    decorated.sort()
    return [row[2] for row in decorated]


def evaluate_ablation_tree(payload=None):
    """意图级签名；真值在责任文档。

    payload：{candidates（define_config_space 产物）, games（粗筛局集/
    v1 兼容精评局集）, fine_games（v2 精评 seated 局集=留出局；缺省=
    games）, coarse_rows（可注入预评粗筛底表 {cid: 行}——复用登记）,
    evaluator（可注入；缺省 SeatedEvaluator）, h2h_runner（可注入；
    v2 h2h 臂——缺省 None=无该臂，混合分退化为 v1）, h2h_games
    （[(seed, seat)] 缺省 DEFAULT_H2H_GAMES）, lambda_sparse=0.02,
    tiers: {coarse_games=8, coarse_subsample_seed, fine_top_k=6（帽
    FINE_TOP_K_CAP）, refinement=true, finalists_n=3,
    wall_clock_budget_s=7200}}。
    返回 {coarse, fine, refinement, finalists, finalist_rows, budget,
    lambda_sparse, subsample, h2h_games}；行含 score（v2 有 h2h 行的
    候选=混合分）与 per-game 明细（seated+h2h 双臂）。
    预算耗尽：停止评估，取已评最优（粗筛表序）并标注
    budget.budget_exhausted=true（R4）；h2h 臂被截断的候选留痕
    budget.h2h_missing（其分退化 v1 语义——如实截断不编数）。
    """
    payload = dict(payload or {})
    candidates = payload.get("candidates") or []
    games = payload.get("games") or []
    if not candidates or not games:
        raise ValueError("evaluate_ablation_tree needs candidates and "
                         "games (fail-closed)")
    lambda_sparse = float(payload.get("lambda_sparse", 0.02))
    tiers = dict(payload.get("tiers") or {})
    coarse_games = int(tiers.get("coarse_games", 8))
    fine_top_k = int(tiers.get("fine_top_k", 6))
    if fine_top_k > FINE_TOP_K_CAP:
        raise ValueError(f"fine_top_k={fine_top_k} 超 v2 契约帽 "
                         f"{FINE_TOP_K_CAP} (fail-closed)")
    fine_games = payload.get("fine_games") or games
    h2h_games = [(int(g[0]), int(g[1]))
                 for g in (payload.get("h2h_games")
                           or DEFAULT_H2H_GAMES)]
    h2h_runner = payload.get("h2h_runner")
    coarse_prefetched = payload.get("coarse_rows")
    finalists_n = int(tiers.get("finalists_n", 3))
    do_refinement = bool(tiers.get("refinement", True))
    budget_s = float(tiers.get("wall_clock_budget_s", 7200.0))
    subsample_seed = int(tiers.get("coarse_subsample_seed", 20260923))
    evaluator = payload.get("evaluator")
    if evaluator is None:
        evaluator = SeatedEvaluator(
            library_dir=payload.get("library_dir"),
            modules_path=payload.get("modules_path"))

    started = time.monotonic()
    candidates_by_id = {c["id"]: c for c in candidates}

    def _elapsed():
        return time.monotonic() - started

    def _attach(candidate, entry, h2h_entry=None):
        row = dict(entry)
        row["h2h"] = h2h_entry
        row["score"] = mixed_score(entry, h2h_entry, candidate,
                                   lambda_sparse)
        row["enabled_modules"] = candidate["enabled_modules"]
        row["piece"] = candidate["piece"]
        row["switches"] = candidate["switches"]
        row["thresholds"] = candidate.get("thresholds")
        return row

    # ---- 粗筛：训练集子样本（每候选 ≤coarse_games 局；不混 h2h）----
    coarse_reused = coarse_prefetched is not None
    if coarse_reused:
        missing = [c["id"] for c in candidates
                   if c["id"] not in coarse_prefetched]
        if missing:
            raise ValueError(f"coarse_rows 底表缺候选 (fail-closed): "
                             f"{missing[:3]} …共 {len(missing)}")
        coarse_rows = {c["id"]: coarse_prefetched[c["id"]]
                       for c in candidates}
        first_row = next(iter(coarse_rows.values()), None)
        subsample = [g["episode_id"]
                     for g in ((first_row or {}).get("games") or [])]
        budget_exhausted = False
    else:
        subsample = _coarse_subsample(games, coarse_games, subsample_seed)
        coarse_rows, budget_exhausted = {}, False
        pending = list(candidates)
        index = 0
        while index < len(pending):
            chunk = pending[index:index + 16]
            if _elapsed() > budget_s:
                budget_exhausted = True
                break
            coarse_rows.update(_call_evaluator(evaluator, chunk,
                                               subsample))
            index += 16
        if budget_exhausted and not coarse_rows:
            raise ValueError("预算耗尽且无已评候选——无法取已评最优 "
                             "(fail-closed)")
    coarse_table = [_attach(candidates_by_id[cid], coarse_rows[cid])
                    for cid in _rank_rows(coarse_rows, candidates_by_id,
                                          lambda_sparse)]
    coarse_order = [row["candidate_id"] for row in coarse_table]

    # ---- 精评：top-K seated(fine_games=v2 留出局) + h2h 臂 ----
    fine_rows, fine_h2h = {}, {}
    top_k = [cid for cid in coarse_order[:fine_top_k]]
    if not budget_exhausted:
        top_candidates = [candidates_by_id[cid] for cid in top_k]
        for i in range(0, len(top_candidates), 4):
            if _elapsed() > budget_s:
                budget_exhausted = True
                break
            fine_rows.update(_call_evaluator(
                evaluator, top_candidates[i:i + 4], fine_games))
        if h2h_runner is not None:
            for cid in top_k:
                if cid not in fine_rows:
                    continue        # seated 臂已截断——h2h 无从混合
                if _elapsed() > budget_s:
                    budget_exhausted = True
                    break
                fine_h2h[cid] = h2h_runner(candidates_by_id[cid],
                                           h2h_games)
    for cid in top_k:
        if cid not in fine_rows:  # 预算截断：沿用粗筛行（局少，如实标注）
            fine_rows[cid] = coarse_rows[cid]
    h2h_missing = [cid for cid in top_k
                   if h2h_runner is not None and cid in fine_rows
                   and cid not in fine_h2h]

    # ---- 阈值微轴精化（最佳配置邻域，可选；同混 h2h）----
    refinement_rows, refinement_h2h = {}, {}
    refinement_variants = []
    if do_refinement and not budget_exhausted and fine_rows:
        best_id = _rank_rows(fine_rows, candidates_by_id, lambda_sparse,
                             fine_h2h)[0]
        best = candidates_by_id[best_id]
        for axis, values, gate in (
                ("clone_streak_required", (16,), "clone_preempt"),
                ("dead_guard_ratio", (0.65,), "dead_price_guard")):
            if not best["switches"].get(gate):
                continue  # 模块关则其阈值无效——不生成空洞变体
            for value in values:
                thresholds = dict(best.get("thresholds")
                                  or DEFAULT_THRESHOLDS)
                thresholds[axis] = value
                variant = dict(best)
                variant["thresholds"] = thresholds
                variant["id"] = f"{best_id}+{axis}={value}"
                refinement_variants.append(variant)
        for i in range(0, len(refinement_variants), 4):
            if _elapsed() > budget_s:
                budget_exhausted = True
                break
            refinement_rows.update(_call_evaluator(
                evaluator, refinement_variants[i:i + 4], fine_games))
        if h2h_runner is not None:
            for variant in refinement_variants:
                if variant["id"] not in refinement_rows:
                    continue
                if _elapsed() > budget_s:
                    budget_exhausted = True
                    break
                refinement_h2h[variant["id"]] = h2h_runner(
                    variant, h2h_games)
    h2h_missing += [vid for vid in (v["id"] for v in
                                    refinement_variants)
                    if h2h_runner is not None
                    and vid in refinement_rows
                    and vid not in refinement_h2h]

    merged = dict(fine_rows)
    merged.update(refinement_rows)
    merged_h2h = dict(fine_h2h)
    merged_h2h.update(refinement_h2h)
    merged_by_id = {cid: candidates_by_id.get(cid) or
                    next(c for c in refinement_variants if c["id"] == cid)
                    for cid in merged}
    final_order = _rank_rows(merged, merged_by_id, lambda_sparse,
                             merged_h2h)
    finalists = [cid for cid in final_order[:finalists_n]]

    fine_table = [_attach(candidates_by_id[cid], fine_rows[cid],
                          fine_h2h.get(cid))
                  for cid in _rank_rows(fine_rows, candidates_by_id,
                                        lambda_sparse, fine_h2h)]
    refinement_table = [_attach(merged_by_id[cid], refinement_rows[cid],
                                refinement_h2h.get(cid))
                        for cid in _rank_rows(refinement_rows, merged_by_id,
                                              lambda_sparse,
                                              refinement_h2h)]

    return {
        "lambda_sparse": lambda_sparse,
        "mixed_weights": list(MIXED_WEIGHTS),
        "subsample": [g["episode_id"] if isinstance(g, dict) else g
                      for g in subsample],
        "h2h_games": [list(g) for g in h2h_games],
        "coarse": coarse_table,
        "fine": fine_table,
        "refinement": refinement_table,
        "finalists": finalists,
        "finalist_rows": [_attach(merged_by_id[cid], merged[cid],
                                  merged_h2h.get(cid))
                          for cid in finalists],
        "budget": {
            "wall_clock_budget_s": budget_s,
            "wall_clock_used_s": round(_elapsed(), 3),
            "budget_exhausted": budget_exhausted,
            "coarse_reused": coarse_reused,
            "coarse_source": payload.get("coarse_source"),
            "n_coarse_candidates": len(coarse_rows),
            "n_coarse_games": len(subsample),
            "n_fine_candidates": len(fine_rows),
            "n_fine_games": len(fine_games),
            "n_refinement_candidates": len(refinement_rows),
            "h2h_arm": h2h_runner is not None,
            "n_h2h_games_per_candidate": len(h2h_games),
            "n_h2h_candidates": len(fine_h2h) + len(refinement_h2h),
            "h2h_missing": h2h_missing,
        },
    }
