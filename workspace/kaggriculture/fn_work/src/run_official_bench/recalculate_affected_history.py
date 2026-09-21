"""对 G1 受影响历史结论逐条用 seated 通道重算，产出双口径台账 recalculation_ledger.md。

上游: R2（详见 fn_docs/responsibility.md run_official_bench 块
recalculate_affected_history 节）

实现要点（[新增]件，契约=该节职责行）：
- 输入 = 受影响结论清单（behavior_inventory.md §0 缺陷 G1 行所列）：
  v3 复裁 b（原 5/9）/c（原 7/13）、v48plus 巨人门 9 局、round24_d0
  反事实、经错位通道的 planner_official_bench 历史数字（正确 seated
  参照 = software/scripts/v143_sellrace_gates.py:91-116）。每条结论自带
  局号集合（episode -> 回放路径 -> me_seat，me_seat 缺省由回放
  info.TeamNames 中队伍席位推导）、注入点、决策 persona
  （agent_callable 或惰性 agent_factory）与可选聚合 aggregate/
  翻转谓词 flip；default_affected_conclusions() 提供该 G1 实清单。
- 重算通道 = 本包 rollout_with_replay_opponent（seated 版：mine→
  seats[me]、回放对手动作→对席）。本模块只 import 该下层，不 import
  旧树 scripts/（persona 由条目注入，缺 persona 记 SKIP 而非禁席伪算）。
- 台账（Markdown，默认 <战役根>/fn_docs/recalculation_ledger.md，路径
  参数化 ledger_path 供测试以 tmp_path 重定向）：每条含 结论标识/局号/
  原值（错位口径）/重算值（seated 口径）/是否翻转/状态；头部注明口径
  定义与重跑前提；与既有 JOURNAL 并列留痕，不改 JOURNAL。
- SKIP 语义（契约"单条重算失败记 SKIP 留因，不中断整批"）：
  replay_data_missing = 官方回放语料缺失（G1 结论依赖 references/
  data/online-replays/**，本机 gitignored——在持数据的主力机上重跑本
  函数即可回填真值）；persona_missing = 未注入决策 persona（惰性禁席
  rollout 不构成忠实重算，persona_note 注明原脚本同源 persona 出处）；
  invalid_entry / recalc_error = 其余单条失败。SKIP 条目重算值/翻转记
  空，台账仍完整落盘。
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path

from run_official_bench.rollout_with_replay_opponent import (
    rollout_with_replay_opponent,
)

__all__ = ["recalculate_affected_history", "default_affected_conclusions",
           "LEDGER_COLUMNS", "LEDGER_ENTRY_KEYS"]

# 战役根目录特征（与 rollout 下层同款三特征判据，不写字面战役路径）
_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")
_TEAM_DEFAULT = "renyxin"

# 台账 schema（列序即 Markdown 表列序；条目键为返回值/台账行结构）
LEDGER_COLUMNS = ("结论标识", "局号", "原值（错位口径）",
                  "重算值（seated 口径）", "是否翻转", "状态")
LEDGER_ENTRY_KEYS = ("id", "episodes", "original_value", "recalc_value",
                     "flipped", "status")

# G1 受影响结论的实清单常量（来源: behavior_inventory.md §0 G1 行；
# 局号与 software/scripts/v3_readmission_suite.py:49-54、
# v48plus_ab_gate.py:48-49 的 TARGET9/WINS13 同表）
_ROUND24_REPLAYS = "references/data/online-replays/round24"
_TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
            110699710, 110685617, 110841464, 110701172)
_WINS13 = (110681129, 110682284, 110683437, 110686759, 110690133,
           110691193, 110692292, 110693383, 110695554, 110696787,
           110697778, 110698875, 110790899)


def _campaign_root() -> Path:
    """自本模块 __file__ 上溯发现战役根（三特征齐备），fail-closed。"""
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists() for name in _CAMPAIGN_FEATURES):
            return candidate
    raise RuntimeError(
        "未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES) + f"），"
        f"上溯起点: {here}")


def _resolve(path, root: Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else root / p


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _derive_me_seat(replay, team: str) -> int:
    teams = list((replay.get("info") or {}).get("TeamNames") or [])
    if team not in teams:
        raise ValueError(f"回放 info.TeamNames 不含队伍 {team!r}: {teams}")
    return int(teams.index(team))


def _default_aggregate(results: list) -> list:
    """默认重算值：逐局 {局号, 我方席位, 双席终局资金}（序=(seat0,seat1)）。"""
    return [{"episode": r["episode"], "me_seat": r["me_seat"],
             "seated_final": r["seated_final"]} for r in results]


def _episode_specs(entry: Mapping, root: Path) -> list:
    """解析条目局号规格：显式 episodes 或 replay_root+episode_glob 发现。

    Returns: [{"episode", "replay_path"(Path), "me_seat"}...]（保持输入序；
    glob 发现按路径排序保证确定性）。
    Raises: ValueError(原因文本) → 调用方记 invalid_entry。
    """
    specs = []
    if "episodes" in entry:
        raw_eps = entry["episodes"] or []
        if not isinstance(raw_eps, (list, tuple)):
            raise ValueError("episodes 必须为列表")
        for spec in raw_eps:
            if not isinstance(spec, Mapping) or "replay_path" not in spec:
                raise ValueError(f"局规格缺 replay_path: {spec!r:.80}")
            path = _resolve(spec["replay_path"], root)
            episode = spec.get("episode")
            if episode is None:
                episode = Path(spec["replay_path"]).name.rsplit(".", 1)[0]
            specs.append({"episode": episode, "replay_path": path,
                          "me_seat": spec.get("me_seat")})
    elif "replay_root" in entry:
        replay_root = _resolve(entry["replay_root"], root)
        if not replay_root.is_dir():
            raise FileNotFoundError(f"回放根缺失: {_rel(replay_root, root)}")
        pattern = entry.get("episode_glob", "**/episode-*-replay.json")
        found = sorted(p for p in replay_root.glob(pattern) if p.is_file())
        if not found:
            raise FileNotFoundError(
                f"回放根无匹配语料: {_rel(replay_root, root)}/{pattern}")
        specs = [{"episode": p.name.rsplit(".", 1)[0], "replay_path": p,
                  "me_seat": entry.get("me_seat")} for p in found]
    else:
        raise ValueError("条目缺 episodes / replay_root")
    if not specs:
        raise ValueError("局号集合为空")
    return specs


def _skip_row(slug: str, detail, cid=None, orig=None, eps=None) -> dict:
    return {"id": cid, "episodes": eps or [], "original_value": orig,
            "recalc_value": None, "flipped": None,
            "status": f"SKIP({slug})", "detail": detail}


def _recalc_one(raw, root: Path, deps) -> dict:
    """单条结论重算（一切单条失败 → SKIP 行，不抛出）。"""
    if not isinstance(raw, Mapping):
        return _skip_row("invalid_entry",
                         f"条目非映射: {type(raw).__name__}")
    cid = raw.get("id")
    if not isinstance(cid, str) or not cid:
        return _skip_row("invalid_entry", f"条目缺字符串 id: {cid!r:.60}")
    if "original_value" not in raw:
        return _skip_row("invalid_entry",
                         "条目缺 original_value（原值/错位口径）", cid=cid)
    original = raw["original_value"]

    def skip(slug, detail, eps=None):
        return _skip_row(slug, detail, cid=cid, orig=original, eps=eps)

    # ---- 局号规格解析（含 replay_root 缺失 → replay_data_missing）----
    try:
        specs = _episode_specs(raw, root)
    except FileNotFoundError as exc:
        return skip("replay_data_missing", str(exc))
    except ValueError as exc:
        return skip("invalid_entry", str(exc))
    episode_ids = [s["episode"] for s in specs]

    # ---- 语料在位检查（任一缺失即整条 SKIP，先于 persona/装载）----
    missing = [s for s in specs if not s["replay_path"].is_file()]
    if missing:
        paths = "、".join(_rel(s["replay_path"], root) for s in missing)
        return skip("replay_data_missing",
                    f"回放缺失 {len(missing)}/{len(specs)} 局: {paths}",
                    eps=episode_ids)

    # ---- 决策 persona（callable 或惰性 factory；缺即 SKIP，不伪算）----
    agent = raw.get("agent_callable")
    if agent is None:
        factory = raw.get("agent_factory")
        if factory is None:
            return skip(
                "persona_missing",
                raw.get("persona_note")
                or "未注入决策 persona（agent_callable/agent_factory）",
                eps=episode_ids)
        try:
            agent = factory()
        except Exception as exc:  # noqa: BLE001 单条失败留因
            return skip("recalc_error",
                        f"agent_factory 失败: {type(exc).__name__}: {exc}",
                        eps=episode_ids)

    # ---- 逐局 seated 重算（任何异常 → SKIP(recalc_error)）----
    injection = int(raw.get("injection_point", 0))
    team = raw.get("team", _TEAM_DEFAULT)
    results = []
    try:
        for spec in specs:
            replay = json.loads(
                spec["replay_path"].read_text(encoding="utf-8"))
            me = spec["me_seat"]
            me = _derive_me_seat(replay, team) if me is None else int(me)
            final = rollout_with_replay_opponent(
                replay, injection, agent, me, deps=deps)
            results.append({"episode": spec["episode"], "me_seat": me,
                            "seated_final": [float(x) for x in final]})
    except Exception as exc:  # noqa: BLE001 单条失败留因，不中断整批
        done = len(results)
        return skip("recalc_error",
                    f"第 {done + 1} 局失败: {type(exc).__name__}: {exc}",
                    eps=episode_ids)

    aggregate = raw.get("aggregate") or _default_aggregate
    recalc_value = aggregate(results)
    flip = raw.get("flip") or (lambda orig, recalc: orig != recalc)
    flipped = bool(flip(original, recalc_value))
    return {"id": cid, "episodes": episode_ids, "original_value": original,
            "recalc_value": recalc_value, "flipped": flipped,
            "status": "RECALC", "detail": None}


def _fmt_value(value) -> str:
    """台账单元格渲染：None→—，str 原样，容器 JSON 紧凑，转义表格符。"""
    if value is None:
        return "—"
    text = value if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, separators=(",", ":"),
        default=repr)
    return text.replace("|", "\\|").replace("\n", " ")


def _fmt_flipped(flipped) -> str:
    return "—" if flipped is None else ("是" if flipped else "否")


def _fmt_episodes(episodes) -> str:
    ids = [str(e) for e in episodes or []]
    if not ids:
        return "—"
    if len(ids) > 12:
        head = "、".join(ids[:12])
        return f"{head} …（共 {len(ids)} 局）"
    return "、".join(ids)


def _render_ledger(rows: list, n_recalc: int, n_skip: int) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# G1 受影响历史结论重算台账（recalculation_ledger）",
        "",
        f"- 生成时间: {stamp}",
        "- 生成入口: fn_work/src/run_official_bench/"
        "recalculate_affected_history.py::recalculate_affected_history",
        "- 结论清单来源: fn_docs/behavior_inventory.md §0 缺陷 G1"
        "（席位错位通道未回流——受影响历史结论）",
        f"- 条目: {len(rows)} 条 = RECALC {n_recalc} + SKIP {n_skip}",
        "- 本台账与既有 JOURNAL 并列留痕（不改 JOURNAL）。",
        "",
        "## 口径定义",
        "",
        "- **原值（错位口径）**: 旧 planner_offline_bench 内联通道——"
        "`deps[\"step\"](state, [mine, theirs])` 恒把\"我方动作\"注入 "
        "seat0（G1：planner_offline_bench.py:319 及其内联同构扩散），"
        "me_seat=1 局终局数字为双席互换伪影。",
        "- **重算值（seated 口径）**: fn_work/src/run_official_bench/"
        "rollout_with_replay_opponent.py——显式 me_seat 注入"
        "（mine→seats[me]、回放对手动作→对席），返回序=(seat0, seat1)"
        "；正确参照 software/scripts/v143_sellrace_gates.py:91-116。",
        "- **是否翻转**: 重算值与原值在结论自身判据语义下不等价"
        "（默认值级不等；语义级判定由条目 flip 谓词给出）。",
        "- **状态**: RECALC=已用 seated 通道重算；SKIP(<原因>)=本条未"
        "重算、原因留档——单条失败不中断整批（契约）。",
        "",
        "## 重跑前提",
        "",
        "- 官方回放语料 `references/data/online-replays/**`（gitignored）"
        "须在位：缺失条目记 SKIP(replay_data_missing)，在持有语料的"
        "主力机上重跑 `recalculate_affected_history("
        "default_affected_conclusions())` 即回填真值并重新落盘本台账。",
        "- 各结论须注入与原脚本同源的决策 persona（条目 "
        "agent_callable/agent_factory；缺 persona 记 "
        "SKIP(persona_missing)，persona_note 注明出处）。",
        "- 引擎指纹链 fail-closed：wheel/场景 sha256 不符即抛，不静默降级"
        "（该类失败记 SKIP(recalc_error)）。",
        "",
        "## 台账",
        "",
        "| " + " | ".join(LEDGER_COLUMNS) + " |",
        "|" + "---|" * len(LEDGER_COLUMNS),
    ]
    for row in rows:
        lines.append(
            "| " + " | ".join((
                _fmt_value(row["id"]),
                _fmt_episodes(row["episodes"]),
                _fmt_value(row["original_value"]),
                _fmt_value(row["recalc_value"]),
                _fmt_flipped(row["flipped"]),
                row["status"],
            )) + " |")
    skips = [r for r in rows if r["status"] != "RECALC"]
    if skips:
        lines += ["", "## SKIP 详情", ""]
        for row in skips:
            lines.append(f"- **{row['id']}** [{row['status']}] "
                         f"{row.get('detail') or '（未留详情）'}")
    lines.append("")
    return "\n".join(lines)


def recalculate_affected_history(affected_conclusions: list,
                                 ledger_path=None, deps=None) -> dict:
    """对受影响结论清单逐条用 seated 通道重算并落盘台账。

    Args:
        affected_conclusions: 结论条目列表（Mapping，每条键：id 结论标识 /
            original_value 原值（错位口径）/ episodes[
            {episode, replay_path, me_seat}] 或 replay_root+episode_glob /
            injection_point（默认 0）/ agent_callable 或 agent_factory
            （决策 persona，缺即 SKIP(persona_missing)）/ aggregate
            （逐局结果→重算值，缺省逐局双席终局）/ flip（原值×重算值→
            是否翻转，缺省值级不等）/ team（me_seat 推导队伍，默认
            "renyxin"）/ persona_note（SKIP 留因用））。
        ledger_path: 台账落盘路径（缺省 <战役根>/fn_docs/
            recalculation_ledger.md；测试以 tmp_path 重定向）。
        deps: rollout 依赖组（透传下层；None=默认 twin 依赖组，引擎装载
            含 fail-closed 指纹校验）。

    Returns:
        {"ledger_path": str, "n_entries": int, "n_recalc": int,
        "n_skip": int, "entries": [台账行 dict（键=LEDGER_ENTRY_KEYS
        +detail）]}——单条失败不中断整批（SKIP 行留因）。
    """
    root = _campaign_root()
    out_path = (Path(ledger_path) if ledger_path is not None
                else root / "fn_docs" / "recalculation_ledger.md")
    rows = [_recalc_one(raw, root, deps)
            for raw in list(affected_conclusions or [])]
    n_recalc = sum(1 for r in rows if r["status"] == "RECALC")
    n_skip = len(rows) - n_recalc
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(_render_ledger(rows, n_recalc, n_skip),
                        encoding="utf-8")
    return {"ledger_path": str(out_path), "n_entries": len(rows),
            "n_recalc": n_recalc, "n_skip": n_skip, "entries": rows}


def _eps(episode_ids) -> list:
    """round24 官方回放局规格（me_seat 缺省=由 TeamNames 推导）。"""
    return [{"episode": ep,
             "replay_path": f"{_ROUND24_REPLAYS}/episode-{ep}-replay.json",
             "me_seat": None} for ep in episode_ids]


def default_affected_conclusions() -> list:
    """G1 受影响结论实清单（behavior_inventory.md §0 G1 行；局号与
    v3_readmission_suite.py / v48plus_ab_gate.py 的 TARGET9/WINS13 同表；
    原值出处 exports/probes/planner_bench/v3_readmission_summary.md）。

    注意：各条目未内嵌决策 persona（本模块不 import 旧树 scripts/，
    persona 由持语料主力机重跑时注入；缺 persona 记 SKIP(persona_missing)
    而非以禁席伪算）。
    """
    return [
        {"id": "v3_readmission:criterion_b_giants",
         "original_value": "5/9（判据 b 九巨人败局回归，阈值 ≥4/9 判 "
                           "PASS；错位通道口径）",
         "episodes": _eps(_TARGET9), "injection_point": 0,
         "persona_note": "v3 运行点 base 臂 persona（v3_readmission_suite "
                         "同源：v13_factory(None)+V3_RUNTIME_CONFIG）"},
        {"id": "v3_readmission:criterion_c_wins",
         "original_value": "7/13（判据 c 十三胜局回归，损伤 >5% 局数 ≤2 "
                           "判 PASS、实测 7 局判 FAIL；错位通道口径）",
         "episodes": _eps(_WINS13), "injection_point": 0,
         "persona_note": "同 criterion_b_giants（v3 运行点 base 臂）"},
        {"id": "v48plus_ab_gate:giants_d0",
         "original_value": "9 巨人局 v48plus−v48 挽回方向判据"
                          "（direction_ok/improved 计数；历史明细 "
                          "exports/probes/v48plus/ gitignored 未随库）",
         "episodes": _eps(_TARGET9), "injection_point": 0,
         "persona_note": "v48/v48plus 双臂 file-loaded submission agent"
                         "（v48plus_ab_gate.giants_block 同源；v48 臂依赖 "
                         "references/intel-notebooks 语料）"},
        {"id": "round24_d0_counterfactual",
         "original_value": "22 局 d0 反事实 base/V_LAND/V_WALLET/V_COMB "
                           "四臂终局与 ≥5/9 挽回门（错位通道口径）",
         "episodes": _eps(_TARGET9 + _WINS13), "injection_point": 0,
         "persona_note": "v13 base 臂+三旋钮臂（round24_d0_counterfactual "
                         "LOSS_VARIANTS/WIN_VARIANTS 同源）"},
        {"id": "planner_official_bench:history",
         "original_value": "m7 判据 a 等离线基准历史数字"
                          "（planner_offline_bench.py:319 恒 mine→seat0）",
         "replay_root": "references/data/online-replays",
         "episode_glob": "**/episode-*-replay.json",
         "injection_point": 0,
         "persona_note": "bench 策略 persona（--strategy 同源，随发现局"
                         "逐局注入）"},
    ]
