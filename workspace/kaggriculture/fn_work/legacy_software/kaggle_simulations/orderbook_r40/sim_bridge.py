# -*- coding: utf-8 -*-
"""sim_bridge（R23 L2）：Rust 仿真器判决基建桥接。

责任契约：加载 debmalyaroy 仿真器（kaggsim 纯 stdlib/预编译二进制，
fn_work/tools/sim_bridge/）；抽样 ≥30 局与官方引擎逐局对照（终局资金一致
100% 才算对照过）；跑判决局（16x）；对照不一致→降级回官方引擎并留档。

【安装面口径】仿真器=debmalyaroy/kaggriculture-simulation（Apache-2.0）：
kaggsim 纯 stdlib Python 包 + Rust 内核 kagg 二进制，安装件落
fn_work/tools/sim_bridge/（gitignore 本机区）。解析序：
  kaggsim 包：config["kaggsim_path"]（严格）→ 现场 import kaggsim（pip）→
    tools_dir/src/src-python → tools_dir/src-python → tools_dir/*/src-python；
  kagg 二进制：config["kagg_bin"] → $KAGG_BIN → tools_dir/kagg →
    tools_dir/src/src-rust/target/release/kagg → kaggsim.binary.find_kagg；
  装好后跑 `kagg version` 健康检查，失败即加载失败。
加载失败（网络/缺件）→ loaded=False+原因留档，全函数降级语义（wall_speedup=1.0）。

【对照口径】语料（replay 目录/文件/seed 列表）抽 n_games（缺省 30）局的
seed，同 seed 同 agent 双引擎逐局跑（官方=kaggle_environments kaggriculture
场景、仿真器=kaggsim Serve+run_match；每局每引擎各起全新 agent 实例，缺省
kaggsim 确定性 policy 对 scripted@11/random@12，config["agents"] 可换），
逐局终局资金（双方 bank）精确相等记 match：
  consistency = {n_checked, n_match, rate}，n_checked=抽样局数（引擎侧单局
  异常/资金缺失记不 match，不静默丢局）；
  consistency_ok = rate==1.0 且 n_checked≥min_checked（缺省 30）。
抽样确定性：seed 排序后 random.Random(sample_seed=20260927) 抽样。

【提速口径】wall_speedup=官方耗时/仿真器耗时（同语料逐局交替实测计总墙钟）。
【降级口径】任何降级（加载失败/对照不过/流程异常）→ 不抛、engine=official、
wall_speedup=1.0（官方引擎口径），实测比值留档在 timing.measured_speedup，
原因写入留档文件（config["record_path"]，缺省 evidence/sim_bridge_degraded.json
追加 records 列表）。fail-safe：函数任何异常均降级返回，不抛。

【run_games 口径】判决局跑口：config["bridge"]（缺省取最近一次 sim_bridge
结果）证得 loaded 且 consistency_ok → 仿真器跑（快线）；否则回退官方引擎并
留档（fallback_reason 记原因）。config["engine"]="sim"/"official" 可强制；
单局红计入不短路。
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MODULE_DIR = Path(__file__).resolve().parent
TOOLS_DIR = MODULE_DIR.parents[2] / "tools" / "sim_bridge"
DEFAULT_RECORD_PATH = MODULE_DIR / "evidence" / "sim_bridge_degraded.json"
DEFAULT_CORPUS_DIRS = ("/tmp/kagr23", "/tmp/kagr22")
REPLAY_GLOB = "episode-*-replay.json"
N_GAMES_DEFAULT = 30
MIN_CHECKED_DEFAULT = 30
SAMPLE_SEED_DEFAULT = 20260927
RECORD_VERSION = "simbridge/1.0"
DEFAULT_AGENT_SPECS = (
    {"type": "pypolicy", "kind": "scripted", "seed": 11},
    {"type": "pypolicy", "kind": "random", "seed": 12},
)

# 最近一次 sim_bridge 结果（run_games 缺省认证依据；仅本模块写入）
_LAST_BRIDGE: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------- 小工具 --

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_record(record_path: Any, record: Dict[str, Any]) -> Optional[str]:
    """降级/回退留档：追加进 records 列表。任何异常静默（留档不反伤主流程）。"""
    try:
        path = Path(record_path) if record_path else DEFAULT_RECORD_PATH
        data: Dict[str, Any] = {"record_version": RECORD_VERSION, "records": []}
        if path.is_file():
            try:
                old = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(old, dict) and isinstance(old.get("records"), list):
                    data = old
            except Exception:
                pass
        data.setdefault("records", []).append(record)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                        encoding="utf-8")
        return str(path)
    except Exception:
        return None


# ------------------------------------------------------------- agent 面 --

def _load_agent_file(path: Any) -> Any:
    """单文件 agent 装载（官方 runner 末位 callable 语义，全新命名空间）。"""
    p = os.path.abspath(str(path))
    if not os.path.isfile(p):
        raise FileNotFoundError(f"agent 文件不存在: {p}")
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns: Dict[str, Any] = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError(f"{p} 装载后无 callable")
    return entries[-1]


def _resolve_agents(specs: Any, config: Optional[Dict[str, Any]]) -> List[Any]:
    """agent spec → 两个全新实例（每局每引擎各起一份，防状态串局）。

    spec 形态：callable 原样 / {"type":"pypolicy","kind","seed"}（kaggsim
    确定性 policy）/ {"type":"python","path"} 或路径串（末位 callable）。
    """
    cfg = config or {}
    if specs is None:
        specs = cfg.get("agents") or list(DEFAULT_AGENT_SPECS)
    out: List[Any] = []
    for spec in specs:
        if callable(spec):
            out.append(spec)
        elif isinstance(spec, dict):
            stype = str(spec.get("type", "python")).lower()
            if stype == "pypolicy":
                from kaggsim.policies import make_policy
                out.append(make_policy(str(spec.get("kind", "random")),
                                       int(spec.get("seed", 0))))
            elif stype == "python":
                out.append(_load_agent_file(spec.get("path")))
            else:
                raise ValueError(f"未知 agent spec type: {stype}")
        elif isinstance(spec, (str, Path)):
            out.append(_load_agent_file(spec))
        else:
            raise ValueError(f"非法 agent spec: {spec!r}")
    if len(out) != 2:
        raise ValueError(f"agents 须为 2 座席，实得 {len(out)}")
    return out


# ------------------------------------------------------------- 安装加载 --

def _find_kaggsim(config: Dict[str, Any]) -> str:
    """kaggsim 包定位：返回其父目录（进 sys.path）或 ''（已可 import）。"""
    tools_dir = Path(config["tools_dir"]) if config.get("tools_dir") \
        else TOOLS_DIR
    if config.get("kaggsim_path"):
        kp = Path(config["kaggsim_path"])
        if not (kp / "kaggsim").is_dir():
            raise FileNotFoundError(f"kaggsim 包不可得: {kp}")
        return str(kp)
    try:
        import kaggsim  # noqa: F401
        return ""
    except ImportError:
        pass
    cands = [tools_dir / "src" / "src-python", tools_dir / "src-python"]
    if tools_dir.is_dir():
        cands.extend(sorted(tools_dir.glob("*/src-python")))
    for c in cands:
        if (c / "kaggsim").is_dir():
            return str(c)
    raise FileNotFoundError(
        f"kaggsim 包不可得（{tools_dir} 下无 src-python/kaggsim，pip 亦无）")


def _find_kagg_bin(config: Dict[str, Any]) -> str:
    """kagg 二进制定位（解析序见模块 docstring）。"""
    tools_dir = Path(config["tools_dir"]) if config.get("tools_dir") \
        else TOOLS_DIR
    cands: List[Any] = [config.get("kagg_bin"), os.environ.get("KAGG_BIN")]
    if tools_dir.is_dir():
        cands.append(tools_dir / "kagg")
        cands.append(tools_dir / "src" / "src-rust" / "target" / "release"
                     / "kagg")
        cands.extend(sorted(tools_dir.glob("*/src-rust/target/release/kagg")))
    for c in cands:
        if c and Path(c).is_file():
            return os.path.abspath(str(c))
    try:
        from kaggsim.binary import find_kagg
        return find_kagg()
    except Exception as exc:
        raise FileNotFoundError(f"kagg 二进制不可得: {exc}") from exc


def _load_simulator(config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """加载仿真器（kaggsim 包+kagg 二进制+健康检查）。失败→抛（调用方降级）。"""
    cfg = config or {}
    kaggsim_path = _find_kaggsim(cfg)
    if kaggsim_path and kaggsim_path not in sys.path:
        sys.path.insert(0, kaggsim_path)
    import kaggsim  # noqa: F401  （装载可用性验证）
    kagg_bin = _find_kagg_bin(cfg)
    out = subprocess.run([kagg_bin, "version"], capture_output=True,
                         text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(f"kagg version 健康检查失败: "
                           f"{(out.stderr or out.stdout)[-200:]}")
    version = (out.stdout or out.stderr).strip()
    return {"kaggsim_path": kaggsim_path or "<已可 import>",
            "kagg_bin": kagg_bin, "version": version,
            "tools_dir": str(Path(cfg["tools_dir"]) if cfg.get("tools_dir")
                             else TOOLS_DIR)}


# --------------------------------------------------------------- 语料面 --

def _seed_of_replay(path: Path) -> Optional[int]:
    """replay 文件→局 seed（info.seed 优先，configuration.seed 兜底）。"""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    info = data.get("info") if isinstance(data, dict) else None
    if isinstance(info, dict) and info.get("seed") is not None:
        return int(info["seed"])
    conf = data.get("configuration") if isinstance(data, dict) else None
    if isinstance(conf, dict) and conf.get("seed") is not None:
        return int(conf["seed"])
    return None


def _collect_games(corpus: Any,
                   config: Optional[Dict[str, Any]]) -> List[Tuple[int, str]]:
    """语料→[(seed, source)]（去重保序；坏件跳过）。"""
    cfg = config or {}
    pairs: List[Tuple[int, str]] = []
    seen = set()

    def _add(seed: Any, source: str) -> None:
        try:
            s = int(seed)
        except (TypeError, ValueError):
            return
        if s in seen:
            return
        seen.add(s)
        pairs.append((s, source))

    if corpus is None:
        dirs = [Path(d) for d in (cfg.get("corpus_dirs") or DEFAULT_CORPUS_DIRS)
                if Path(d).is_dir()]
        if not dirs:
            raise RuntimeError("语料不可得：无可用 corpus 目录")
        items: List[Any] = []
        for d in dirs:
            items.extend(sorted(d.glob(REPLAY_GLOB)))
    elif isinstance(corpus, (str, Path)):
        p = Path(corpus)
        if p.is_dir():
            items = sorted(p.glob(REPLAY_GLOB))
        elif p.is_file():
            items = [p]
        else:
            raise FileNotFoundError(f"语料不存在: {p}")
    elif isinstance(corpus, (list, tuple)):
        items = list(corpus)
    else:
        raise TypeError(f"corpus 形态非法: {type(corpus).__name__}")

    for it in items:
        if isinstance(it, bool):
            raise TypeError("corpus 元素非法（bool）")
        if isinstance(it, int):
            _add(it, "<seed>")
            continue
        if isinstance(it, dict):
            seed = it.get("seed")
            if seed is None and isinstance(it.get("info"), dict):
                seed = it["info"].get("seed")
            if seed is None:
                continue
            _add(seed, str(it.get("source", "<dict>")))
            continue
        if isinstance(it, (str, Path)):
            p = Path(it)
            seed = _seed_of_replay(p) if p.is_file() else None
            if seed is None:
                continue
            _add(seed, str(p))
            continue
        raise TypeError(f"corpus 元素非法: {type(it).__name__}")

    return pairs


def _sample_games(pairs: List[Tuple[int, str]], n: int,
                  config: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """确定性抽样：seed 排序后固定 rng 抽 n（不足全取）。"""
    ordered = sorted(pairs, key=lambda pr: (pr[0], pr[1]))
    if len(ordered) <= n:
        picked = ordered
    else:
        rng = random.Random(int((config or {}).get("sample_seed",
                                                   SAMPLE_SEED_DEFAULT)))
        picked = sorted(rng.sample(ordered, n))
    return [{"seed": s, "source": src} for s, src in picked]


# --------------------------------------------------------------- 引擎面 --

def _official_banks(seed: int, a0: Any, a1: Any) -> Tuple[float, float]:
    """官方引擎单局终局资金（优先 kaggsim.official 认证钉版引擎）。"""
    try:
        from kaggsim import official as _off
        banks, _env = _off.run_agents(a0, a1, int(seed))
    except ImportError:
        import kaggle_environments as ke
        env = ke.make("kaggriculture",
                      configuration={"seed": int(seed), "actTimeout": 60,
                                     "runTimeout": 100000},
                      info={"seed": int(seed)}, debug=False)
        env.run([a0, a1])
        steps = getattr(env, "steps", None)
        if not isinstance(steps, list) or not steps:
            raise RuntimeError("官方引擎无状态帧")
        banks = tuple(s.get("reward") for s in steps[-1])
    if any(b is None for b in banks):
        raise RuntimeError(f"官方引擎终局资金缺失: {banks!r}")
    return (float(banks[0]), float(banks[1]))


def _run_official_batch(games: List[Dict[str, Any]],
                        config: Optional[Dict[str, Any]]
                        ) -> Tuple[List[Dict[str, Any]], float]:
    """官方引擎逐局跑（单局红计入不短路）。→ ([{seed,banks,error}], 总耗时)。"""
    rows: List[Dict[str, Any]] = []
    t_all = time.perf_counter()
    for g in games:
        seed = int(g["seed"])
        t0 = time.perf_counter()
        row: Dict[str, Any] = {"seed": seed, "banks": None, "error": None}
        try:
            a0, a1 = _resolve_agents(g.get("agents"), config)
            row["banks"] = [float(x) for x in _official_banks(seed, a0, a1)]
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
        row["elapsed_s"] = round(time.perf_counter() - t0, 4)
        rows.append(row)
    return rows, time.perf_counter() - t_all


def _run_sim_batch(games: List[Dict[str, Any]], handle: Dict[str, Any],
                   config: Optional[Dict[str, Any]]
                   ) -> Tuple[List[Dict[str, Any]], float]:
    """仿真器逐局跑（同 Serve 复用；单局红计入不短路）。"""
    from kaggsim.serve import Serve, run_match
    rows: List[Dict[str, Any]] = []
    t_all = time.perf_counter()
    srv = Serve(handle.get("kagg_bin"))
    try:
        for g in games:
            seed = int(g["seed"])
            t0 = time.perf_counter()
            row: Dict[str, Any] = {"seed": seed, "banks": None, "error": None}
            try:
                a0, a1 = _resolve_agents(g.get("agents"), config)
                banks = run_match(a0, a1, seed, srv)
                row["banks"] = [float(x) for x in banks]
            except Exception as exc:
                row["error"] = f"{type(exc).__name__}: {exc}"
            row["elapsed_s"] = round(time.perf_counter() - t0, 4)
            rows.append(row)
    finally:
        try:
            srv.close()
        except Exception:
            pass
    return rows, time.perf_counter() - t_all


# --------------------------------------------------------------- 主入口 --

def _degrade(reason: str, config: Optional[Dict[str, Any]], loaded: bool,
             handle: Optional[Dict[str, Any]] = None,
             extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """统一降级返回：官方引擎口径 wall_speedup=1.0 + 留档。"""
    cfg = config or {}
    record_path = cfg.get("record_path")
    saved = _write_record(record_path, {
        "at": _now(), "kind": "degrade", "reason": reason,
        "loaded": bool(loaded), "version": RECORD_VERSION})
    out: Dict[str, Any] = {
        "loaded": bool(loaded),
        "consistency": {"n_checked": 0, "n_match": 0, "rate": None},
        "wall_speedup": 1.0,
        "consistency_ok": False,
        "degraded": True,
        "degraded_reason": reason,
        "engine": "official",
        "timing": None,
        "games": [],
        "install": handle,
        "record_path": saved,
        "n_games": 0,
        "elapsed_s": 0.0,
        "fallback_reason": reason,
        "version": RECORD_VERSION,
    }
    out.update(extra or {})
    return out


def sim_bridge(config: Any = None, corpus: Any = None) -> Dict[str, Any]:
    """仿真器加载+抽样对照一致性+提速读数。

    签名意图：输入: 仿真器配置+对照语料 / 输出: {loaded, consistency,
    wall_speedup} / 错误: 对照不过→降级不抛（留档）。
    """
    global _LAST_BRIDGE
    cfg = dict(config) if isinstance(config, dict) else {}
    try:
        try:
            handle = _load_simulator(cfg)
        except Exception as exc:
            res = _degrade(f"仿真器加载失败: {type(exc).__name__}: {exc}",
                           cfg, loaded=False)
            _LAST_BRIDGE = res
            return res
        try:
            pairs = _collect_games(corpus, cfg)
            n_games = int(cfg.get("n_games", N_GAMES_DEFAULT))
            min_checked = int(cfg.get("min_checked", MIN_CHECKED_DEFAULT))
            games = _sample_games(pairs, n_games, cfg)
            if not games:
                res = _degrade("语料无可用对局（seed 不可得）", cfg,
                               loaded=True, handle=handle)
                _LAST_BRIDGE = res
                return res
            off_rows, off_s = _run_official_batch(games, cfg)
            sim_rows, sim_s = _run_sim_batch(games, handle, cfg)
            detail: List[Dict[str, Any]] = []
            n_match = 0
            for g, ro, rs in zip(games, off_rows, sim_rows):
                ok = (ro.get("error") is None and rs.get("error") is None
                      and ro.get("banks") is not None
                      and rs.get("banks") is not None
                      and [float(x) for x in ro["banks"]]
                      == [float(x) for x in rs["banks"]])
                if ok:
                    n_match += 1
                detail.append({
                    "seed": g["seed"], "source": g["source"], "match": ok,
                    "official": ro.get("banks"), "sim": rs.get("banks"),
                    "error_official": ro.get("error"),
                    "error_sim": rs.get("error")})
            n_checked = len(games)
            rate = (n_match / n_checked) if n_checked else None
            consistency = {"n_checked": n_checked, "n_match": n_match,
                           "rate": rate}
            consistency_ok = bool(rate == 1.0 and n_checked >= min_checked)
            measured = (off_s / sim_s) if sim_s and sim_s > 0 else None
            timing = {"official_s": round(off_s, 4),
                      "sim_s": round(sim_s, 4),
                      "measured_speedup": (round(measured, 3)
                                           if measured else None)}
            res = {
                "loaded": True,
                "consistency": consistency,
                "wall_speedup": (round(measured, 3) if measured else 1.0),
                "consistency_ok": consistency_ok,
                "degraded": not consistency_ok,
                "degraded_reason": None,
                "engine": "sim",
                "timing": timing,
                "games": detail,
                "install": handle,
                "version": RECORD_VERSION,
            }
            if consistency_ok:
                res["record_path"] = None
            else:
                if n_checked < min_checked:
                    reason = (f"对照样本不足（n_checked={n_checked}"
                              f"<min_checked={min_checked}）")
                else:
                    reason = (f"对照未过：{n_match}/{n_checked} 局终局资金一致"
                              f"（rate={rate}）")
                res["degraded_reason"] = reason
                res["engine"] = "official"
                res["wall_speedup"] = 1.0        # 降级=官方引擎口径
                res["record_path"] = _write_record(cfg.get("record_path"), {
                    "at": _now(), "kind": "degrade", "reason": reason,
                    "loaded": True, "consistency": consistency,
                    "timing": timing, "version": RECORD_VERSION})
            _LAST_BRIDGE = res
            return res
        except Exception as exc:
            res = _degrade(f"对照流程异常: {type(exc).__name__}: {exc}",
                           cfg, loaded=True, handle=handle)
            _LAST_BRIDGE = res
            return res
    except Exception as exc:  # 兜底：任何意外均降级不抛
        res = _degrade(f"sim_bridge 异常: {type(exc).__name__}: {exc}",
                       cfg, loaded=False)
        _LAST_BRIDGE = res
        return res


# ------------------------------------------------------------- 判决跑口 --

def _normalize_games(games: Any,
                     config: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cfg = config or {}
    if isinstance(games, dict):
        games = [games]
    if not isinstance(games, (list, tuple)):
        raise TypeError("games 须为 list")
    plan: List[Dict[str, Any]] = []
    for g in games:
        if isinstance(g, bool):
            raise TypeError("game 元素非法（bool）")
        if isinstance(g, int):
            plan.append({"seed": int(g), "agents": cfg.get("agents")})
            continue
        if isinstance(g, dict):
            if g.get("seed") is None:
                raise ValueError("game 缺 seed")
            plan.append({"seed": int(g["seed"]),
                         "agents": g.get("agents", cfg.get("agents"))})
            continue
        raise TypeError(f"game 元素非法: {type(g).__name__}")
    return plan


def _pick_engine(config: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    """引擎选择：返回 (engine, 回退原因)。认证口径=bridge loaded+consistency_ok。"""
    engine = str(config.get("engine", "auto")).lower()
    if engine not in ("auto", "sim", "official"):
        raise ValueError(f"engine 非法: {engine}")
    if engine == "official":
        return "official", None
    if engine == "sim":
        return "sim", None
    bridge = config.get("bridge", _LAST_BRIDGE)
    if not isinstance(bridge, dict):
        return "official", "无对照记录（仿真器未认证）"
    if not bridge.get("loaded"):
        return "official", "仿真器未装载（loaded=False）"
    if not bridge.get("consistency_ok"):
        return "official", "对照未过（consistency_ok=False）"
    return "sim", None


def run_games(games: Any, config: Any = None) -> Dict[str, Any]:
    """判决局跑口：仿真器可用（已认证）走仿真器，否则回退官方引擎（回退留档）。

    签名意图：输入: 对局清单（seed+agents）+桥接配置 / 输出: {engine, games,
    elapsed_s, fallback_reason} / 错误: 任何异常→降级不抛（留档）。
    """
    cfg = dict(config) if isinstance(config, dict) else {}
    try:
        plan = _normalize_games(games, cfg)
        if not plan:
            raise ValueError("games 为空")
        engine, reason = _pick_engine(cfg)
        rows: Optional[List[Dict[str, Any]]] = None
        elapsed = 0.0
        if engine == "sim":
            try:
                handle = cfg.get("sim_handle") or _load_simulator(cfg)
                rows, elapsed = _run_sim_batch(plan, handle, cfg)
            except Exception as exc:
                engine = "official"
                reason = (reason or "") + \
                    f"仿真器运行异常: {type(exc).__name__}: {exc}"
        if engine != "sim":
            try:
                rows, elapsed = _run_official_batch(plan, cfg)
            except Exception as exc:
                return _degrade(
                    f"官方引擎运行异常: {type(exc).__name__}: {exc}", cfg,
                    loaded=bool(cfg.get("sim_handle")),
                    extra={"n_games": len(plan), "games": []})
        out: Dict[str, Any] = {
            "engine": engine, "n_games": len(plan), "games": rows,
            "elapsed_s": round(elapsed, 4),
            "fallback_reason": reason if engine == "official" else None,
            "degraded": engine != "sim" and reason is not None,
            "version": RECORD_VERSION,
        }
        if out["fallback_reason"]:
            out["record_path"] = _write_record(cfg.get("record_path"), {
                "at": _now(), "kind": "run_games_fallback",
                "reason": out["fallback_reason"], "engine": engine,
                "n_games": len(plan), "version": RECORD_VERSION})
        else:
            out["record_path"] = None
        return out
    except Exception as exc:
        return _degrade(f"run_games 异常: {type(exc).__name__}: {exc}", cfg,
                        loaded=bool(cfg.get("sim_handle")))
