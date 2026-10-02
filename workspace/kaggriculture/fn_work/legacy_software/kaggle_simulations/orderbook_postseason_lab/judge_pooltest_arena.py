# -*- coding: utf-8 -*-
"""judge_pooltest_arena（postseason lab）：战后开源潮 5 件许可干净提交件级开源件池测判决
（判决先行·只测不发·不提交·零修改原始件）。

件（fn_docs/hybrid/references/2026-10-02-postseason-github-scan.md §三 A 池测序，2026-10-02 实抓）：
  syx       = sunyuxiang136/kaggriculture-silver-agent main.py（Apache-2.0 单文件 5.8MB
              交件形态；自报银牌）——零修改直跑
  taeyan    = TaeyanG4/kaggriculture-strategy-meta agent/c1200_final.py（Apache-2.0 单文件
              21MB 生成件；自报提交号 56719658/56722176）——零修改直跑
  romansvet = romansvet/kaggriculture submission/（Apache-2.0 整包 37 文件+theta.npy/
              residual_head.npz 随仓；自报 #330）——多文件件，harness 适配层清 kagg3* 模块缓存
  carson    = CarsonBurke/kaggriculture（MIT 自报 #12）——缺 checkpoint 权重，装载失败 UNRUNNABLE
  debmal    = debmalyaroy/kaggriculture（MIT v63 提交号 56718979/56720196）——缺 route 表/配置
              payload，编译过但装载失败 UNRUNNABLE

面板（每对 n=12 fold 双席=24 局，中性块 674000+i*131 i=0..11）：
  件 vs {H1 王座锚（H1/oc_c3 行为孪生，BT 527.8）, mpx, r40（弱锚）, A（弱件锚）}
口径（同 EXP-066/godv7）：h2h=judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平，
缺席/红局→该 seed 记负 fail-closed）；margin=farms[obs.player] 终局钱差（干净口径，
banks 交叉登记）；realized_px=Σ(qty×卖时价)/Σ(qty×base)（BASE_PX milkwin 表，参考）；
胜率=硬通货。判决三档：BEATS_CEILING（vs 王座 H1 ≥0.5）/ COMPETITIVE（0.35-0.5）/
WEAK（<0.35）/ UNRUNNABLE（装载失败或红局>20%）。
sim_bridge 认证：composite lab 09-30 30/30 缓存附证 + 每件在环 30/30 一轮（件 vs r40，
双引擎逐局终局资金对照）。
第三方代码执行全程 bwrap 沙箱（根只读+/tmp+本 lab 可写+断网）。证据
orderbook_postseason_lab/evidence/pooltest_arena.json。只写本 lab。不改既有代码。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
EV_PATH = EVID_DIR / "pooltest_arena.json"
PIECES_DIR = HERE / "pieces"
BUILD_DIR = HERE / "build"

# ============================================================ 面板件 ==
H1 = KSIM_DIR / "orderbook_topform_lab" / "build" / "h1" / "main.py"
OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
MPX = (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
       / "main.py")
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A = KSIM_DIR / "orderbook_r44_a" / "main.py"

PANEL = {"H1": H1, "mpx": MPX, "r40": R40, "A": A}
PANEL_ROLE = {"H1": "王座锚（H1/oc_c3 行为孪生，BT 527.8）", "mpx": "面板强件",
              "r40": "弱锚", "A": "弱件锚"}

# ============================================================ 测件 ==
PIECES = {
    "syx": {
        "main": PIECES_DIR / "syx" / "main.py",
        "repo": "https://github.com/sunyuxiang136/kaggriculture-silver-agent",
        "commit": "be16043a8b6842357fea0b86a150629d62c7ab32",
        "license": "Apache-2.0",
        "form": "整包单文件（main.py 5,814,850B，纯标准库）；入口=末 callable "
                "agent(observation, configuration=None)（globals().pop 重排至末位）",
        "self_reported": "自报银牌（银牌方案完整源码；官方未发奖，终榜 ~10-15）；"
                         "自报 <3ms/step；README 致谢 2965 Hybrid V39/V46 系谱",
        "load_mode": "direct",
    },
    "taeyan": {
        "main": PIECES_DIR / "taeyan" / "agent" / "c1200_final.py",
        "repo": "https://github.com/TaeyanG4/kaggriculture-strategy-meta",
        "commit": "9e7daeb31a96b7fb883bc2691b7f26f6af083d53",
        "license": "Apache-2.0",
        "form": "整包单文件生成件（c1200_final.py 21,479,707B，base64+lzma 内嵌源码"
                " exec，纯标准库）；入口=末 callable agent(obs, configuration=None)",
        "self_reported": "自报提交号 c1054=56719658（09-30）/c1200=56722176（10-01，"
                         "晚于截止存疑）；自报 c1200 全家 ladder 118W8L2T；自报 c111 曾 2350.6",
        "load_mode": "direct",
    },
    "romansvet": {
        "main": PIECES_DIR / "romansvet" / "submission" / "main.py",
        "repo": "https://github.com/romansvet/kaggriculture",
        "commit": "4444cc7a977466a501957ed09cd64951afafa5e7",
        "license": "Apache-2.0",
        "form": "整包多文件（submission/ 37 文件：main.py 入口+kagg3/ 包+theta.npy 30,896B"
                "+residual_head.npz 59,370B）；入口=末 callable agent(observation, "
                "configuration=None)；numpy 前向；harness 适配=每局清 kagg3* 模块缓存",
        "self_reported": "自报峰 2,858/收官 2,230（rank 330 of 10,246 provisional）；"
                         "自报提交号 56718602/56707958（终两席）；~7.7k 浮点 ES 策略",
        "load_mode": "purge_kagg3",
    },
    "carson": {
        "main": None,
        "repo": "https://github.com/CarsonBurke/kaggriculture",
        "commit": "fbbf76f49fc833f5a444a6414a71c8e74d90c4f4",
        "license": "MIT",
        "form": "Python 神经推理包（src/kaggriculture 54 模块）+ 训练 checkpoint；"
                "打包线 scripts/build_submission.py --checkpoint（仓内无 runs/、无权重文件）",
        "self_reported": "自报 final submissions placed 12th of 10,246（#12）；"
                         "BC→PPO、Rust 位级仿真、LeJEPA、联盟 PPO",
        "load_mode": "unrunnable_preflight",
    },
    "debmal": {
        "main": None,
        "repo": "https://github.com/debmalyaroy/kaggriculture",
        "commit": "c681c269d9713de082468271b056cf410e246dc9",
        "license": "MIT",
        "form": "Rust agent-stdio 二进制 + main_config.py stdio 桥 + agent.json + "
                "base/routes.json(~4.8MB route 表) + 学习层 payload；仓明言 ships no data",
        "self_reported": "自报 v63.14=56718979（41W12L1D）/v63.16=56720196（53W11L）；"
                         "自报 v63.17 built not submittable",
        "load_mode": "unrunnable_preflight",
    },
}

SHA_PANEL = {}
N_FOLDS = int(os.environ.get("POOLTEST_FOLDS", "12"))
PANEL_FOLDS = [674000 + i * 131 for i in range(N_FOLDS)]
WORKERS = int(os.environ.get("POOLTEST_WORKERS", "2"))
RUN_PIECES = [s for s in os.environ.get(
    "POOLTEST_PIECES", "syx,taeyan,romansvet,carson,debmal").split(",") if s]
DO_AUTH = os.environ.get("POOLTEST_AUTH", "1") == "1"

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    EV_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                  default=str) + "\n", encoding="utf-8")


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ==================================================== 装载适配层 ==
def purge_piece_modules(piece):
    """多文件件模块缓存清理（harness 外部层；件本体零修改）。"""
    if PIECES.get(piece, {}).get("load_mode") == "purge_kagg3":
        for m in list(sys.modules):
            if m == "kagg3" or m.startswith("kagg3."):
                sys.modules.pop(m, None)


def load_entry(path, piece=None):
    """piece 非空=测件本体装载（先清其模块缓存）；对手装载不触发清理。"""
    if piece:
        purge_piece_modules(piece)
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    return j23._load_entry(path)


def _preflight_unrunnable(piece):
    """不可跑件装载失败实证（只读文件系统核查+二进制探针结果引用）。"""
    info = dict(PIECES[piece])
    if piece == "carson":
        root = PIECES_DIR / "carson"
        wext = (".pt", ".npz", ".npy", ".pth", ".ckpt", ".safetensors", ".bin")
        weights = [str(p.relative_to(root)) for p in root.rglob("*")
                   if p.is_file() and p.suffix in wext
                   and ".git" not in p.parts]
        entries = [str(p.relative_to(root)) for p in root.rglob("main.py")
                   if ".git" not in p.parts]
        return {
            "ok": False, "verdict": "UNRUNNABLE",
            "reason": "缺 checkpoint 权重：scripts/build_submission.py 打包硬性要求 "
                      "--checkpoint runs/ppo/best.pt（README 步骤 5），仓内无 runs/、"
                      "无任何权重文件、无提交入口 main.py；打包器另有 provenance/eval "
                      "证据绑定门（'will not package a checkpoint unless its "
                      "provenance and evaluation evidence match'）",
            "checks": {"weight_files_found": weights or "未找到",
                       "main_py_found": entries or "未找到",
                       "lfs_note": ".lfsconfig 仅排除 results/tensorboard/**（LFS 指针）"},
        }
    if piece == "debmal":
        bdir = BUILD_DIR / "debmal_build"
        binp = bdir / "target" / "release" / "agent-stdio"
        probe = ("agent-stdio --config configs/agents/c4.agent.json → "
                 "load .../configs/agents/base/routes.json: No such file or "
                 "directory (os error 2)（2026-10-02 bwrap 实测）")
        return {
            "ok": False, "verdict": "UNRUNNABLE",
            "reason": "缺提交配置 payload：v63 提交 tarball=main_config.py 桥+agent-stdio"
                      "+agent.json+base/routes.json(~4.8MB route 表)+学习层文件（policy.bin/"
                      "shield/knobs/dispatch/rshell/shell/endg/gt/preempt/group_knobs）；"
                      "仓 README 明言 'The repository ships no data (replays, tapes, "
                      "route tables, weights, builds)'，configs/ 仅构型模板（c4.agent.json"
                      " 等指向 base/、policy.bin 等缺失件），无可装载 v63 配置包",
            "checks": {
                "compile": "agent-stdio 编译过（bwrap 内 cargo build --release -p agent "
                           "--bin agent-stdio，8.76s，build/debmal_build/target/release/"
                           "agent-stdio 4,187,272B；fetch 在沙箱外=纯下载）",
                "binary_probe": probe,
                "missing_payloads": ["agent.json(v63 候选)", "base/routes.json",
                                     "base/router.json(模板在 configs/bases/*)",
                                     "policy.bin/shield.json/knobs.json/dispatch/",
                                     "rshell/shell/endg/gt/preempt/group_knobs"],
                "data_dir": "未找到（data/ 不存在）",
            },
        }
    return {"ok": False, "verdict": "UNRUNNABLE", "reason": "未知件"}


# ==================================================== 局跑口 ==
def _chunk(payload):
    """worker：双席 trace 局；干净口径 margin（同 exp066 _chunk）。

    逐局"装载→跑→下一局"串行（对齐 sim_bridge 批跑口的逐局解析语义）：多文件件
    （romansvet）惰性 import（residual_head 首个规划日）不允许被后续装载的模块
    清理误伤——件装载后到本局结束前不再触碰其模块缓存。
    """
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    out = []
    for spec in specs:
        load_s = {}
        try:
            agents, sinks = [], ({0: [], 1: []} if spec.get("trace") else None)
            for seat, a in enumerate(spec["agents"]):
                lt = time.perf_counter()
                inner = load_entry(a.get("path"), spec.get("piece")
                                   if a.get("kind") == "piece" else None)
                if a.get("kind") == "piece":
                    load_s["piece_load_s"] = round(time.perf_counter() - lt, 2)
                if sinks is not None:
                    agents.append(j23._Tracer(inner, seat, sinks[seat]))
                else:
                    agents.append(inner)
            res = sb.run_games([{"seed": int(spec["seed"]),
                                 "agents": agents}], cfg)
            rr = (res.get("games") or [{}])[0]
            berr = None
        except Exception as exc:
            res, rr, sinks, berr = {"engine": None}, {}, None, \
                repr(exc)[:160]
        row = {"game_id": spec.get("game_id"), "piece": spec.get("piece"),
               "seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"), "group": spec.get("group"),
               "engine": res.get("engine"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None,
               "rpx_us": None, "rpx_opp": None}
        row.update(load_s)
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
                row["rpx_us"] = realized_px(sinks[row["seat"]])
                row["rpx_opp"] = realized_px(sinks[1 - row["seat"]])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
        out.append(row)
    return out


def realized_px(sink):
    """提交口径实现价：Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表）。"""
    val = 0.0
    base = 0.0
    for _step, obs, act in (sink or []):
        if not isinstance(act, dict):
            continue
        prices = ((obs.get('market') or {}) if isinstance(obs.get('market'),
                  dict) else {}).get('prices') or {}
        for cmd in (act.get('market') or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                item = str(cmd[1])
                px = prices.get(item)
                try:
                    q = float(cmd[2])
                except Exception:
                    continue
                b = float(BASE_PX.get(item, 0) or 0)
                if isinstance(px, (int, float)) and q > 0 and b > 0:
                    val += q * float(px)
                    base += q * b
    return round(val / base, 4) if base > 0 else None


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(piece, piece_path, opp_name, opp_path, folds, group="panel"):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            specs.append({
                "game_id": "pt|%s|%s|%d-s%d" % (piece, opp_name, seed, seat),
                "seed": int(seed), "piece": piece, "our_seat": seat,
                "opponent": opp_name, "group": group,
                "trace": True,
                "agents": [{"type": "python", "path": str(piece_path),
                            "kind": "piece"},
                           {"type": "python", "path": str(opp_path),
                            "kind": "opp"}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows
           if isinstance(r.get("tm_opp"), (int, float))]
    rpx_u = [r["rpx_us"] for r in rows
             if isinstance(r.get("rpx_us"), (int, float))]
    rpx_o = [r["rpx_opp"] for r in rows
             if isinstance(r.get("rpx_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin"] = round(sum(r["margin_clean"] for r in rows
                                 if r["margin_clean"] is not None)
                             / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["realized_px_us"] = round(sum(rpx_u) / len(rpx_u), 4) if rpx_u else None
    f["realized_px_opp"] = round(sum(rpx_o) / len(rpx_o), 4) if rpx_o else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    loads = [r["piece_load_s"] for r in rows
             if isinstance(r.get("piece_load_s"), (int, float))]
    f["piece_load_s_mean"] = round(sum(loads) / len(loads), 2) if loads else None
    return f


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"auth_games": 0, "panel_games": 0}

    # ---- 断点续跑（POOLTEST_RESUME=1：并入既有证据，跳过已判决件）----
    prior = None
    if os.environ.get("POOLTEST_RESUME") == "1" and EV_PATH.is_file():
        try:
            prior = json.loads(EV_PATH.read_text(encoding="utf-8"))
        except Exception:
            prior = None

    EV.update({
        "version": "pooltest-arena/1.0",
        "task": "战后开源潮 5 件许可干净提交件级开源件池测判决（P1 池测判决）："
                "自报≠可迁移，判决只认本池实测（判决先行·只测不发·不提交）",
        "pieces": {k: {kk: (str(vv) if isinstance(vv, Path) else vv)
                       for kk, vv in v.items()}
                   for k, v in PIECES.items()},
        "source": {
            "commands": ["bwrap 沙箱内: python3 orderbook_postseason_lab/"
                         "judge_pooltest_arena.py"],
            "sandbox": "bwrap --ro-bind / / --dev /dev --proc /proc --bind /tmp "
                       "/tmp --bind <lab> <lab> --ro-bind <pieces> <pieces> "
                       "--unshare-net（第三方代码仅沙箱内执行）",
            "scan_ref": "fn_docs/hybrid/references/"
                        "2026-10-02-postseason-github-scan.md（抓取 2026-10-02 "
                        "10:40-11:25Z）；pieces/ 归档 2026-10-02 12:06Z",
            "corpus": {
                "panel_folds": PANEL_FOLDS,
                "panel_spec": "中性块 674000+i*131（i=0..%d）；每对 n=%d fold 双席"
                              "=%d 局" % (N_FOLDS - 1, N_FOLDS, 2 * N_FOLDS),
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "缺席/红局→该 seed 记负 fail-closed）",
                "margin": "farms[obs.player] 终局钱差（干净口径；banks 交叉登记）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表，参考）",
                "hard_currency": "胜率=硬通货；margin/realized_px 只作参考",
                "zero_modification": "件本体零修改；适配仅 harness 层（romansvet 每局清 "
                                     "kagg3* 模块缓存=对齐官方逐局全新解释器语义）",
                "fresh_ns_per_game": "每局全新命名空间装载（j23._load_entry；有状态件"
                                     "跨局不残留）",
            },
            "panel": {k: {"path": str(v), "sha": SHA_PANEL.get(k)}
                      for k, v in PANEL.items()},
            "panel_role": PANEL_ROLE,
        },
        "sim_auth": {}, "panel": {}, "verdicts": {}, "budget": budget,
        "panel_rows": [],
    })
    # 面板件 sha
    for k, v in PANEL.items():
        try:
            SHA_PANEL[k] = sha256_of(v)
        except Exception:
            SHA_PANEL[k] = None
    EV["source"]["panel"] = {k: {"path": str(v), "sha": SHA_PANEL.get(k)}
                            for k, v in PANEL.items()}
    if prior:
        EV["sim_auth"] = prior.get("sim_auth") or {}
        EV["panel"] = prior.get("panel") or {}
        EV["verdicts"] = prior.get("verdicts") or {}
        EV["panel_rows"] = prior.get("panel_rows") or []
        if isinstance(prior.get("budget"), dict):
            budget.update(prior["budget"])
        global RUN_PIECES
        RUN_PIECES = [p for p in RUN_PIECES if p not in EV["verdicts"]]
        ANOMALIES.append("POOLTEST_RESUME=1 断点续跑：并入既有证据（%s），"
                         "重跑 %s" % (EV_PATH.name, ",".join(RUN_PIECES) or "无"))
    flush_evid()

    # ---- sim_bridge 认证：composite 30/30 缓存附证 ----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = (KSIM_DIR / "orderbook_composite_lab" / "evidence"
                  / "sim_auth_cache.json")
    base_auth = None
    if AUTH_CACHE.is_file():
        try:
            base_auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        except Exception:
            base_auth = None
    EV["sim_auth"]["baseline_cache"] = {
        "reused_cache": True, "cache_path": str(AUTH_CACHE),
        "loaded": (base_auth or {}).get("loaded"),
        "consistency": (base_auth or {}).get("consistency"),
        "consistency_ok": (base_auth or {}).get("consistency_ok"),
        "engine": (base_auth or {}).get("engine"),
        "version": (base_auth or {}).get("version"),
        "wall_speedup": (base_auth or {}).get("wall_speedup")}
    if not prior:
        budget["auth_games"] = 30
    flush_evid()

    # sim_bridge 装载适配（多文件件模块缓存清理，进程内 harness 层）
    _orig_load = sb._load_agent_file

    def _purging_load(path):
        p = os.path.abspath(str(path))
        for name, meta in PIECES.items():
            if meta.get("main") and p == os.path.abspath(str(meta["main"])):
                purge_piece_modules(name)
        return _orig_load(path)

    sb._load_agent_file = _purging_load

    all_rows = list(EV.get("panel_rows") or [])
    verdicts = dict(EV.get("verdicts") or {})
    for piece in RUN_PIECES:
        meta = PIECES[piece]
        p_t0 = time.perf_counter()

        # ---- preflight / 装载 ----
        if meta.get("load_mode") == "unrunnable_preflight":
            pf = _preflight_unrunnable(piece)
            verdicts[piece] = {
                "verdict": "UNRUNNABLE",
                "rule": "BEATS_CEILING=vs 王座 H1 h2h≥0.5 / COMPETITIVE=0.35-0.5 / "
                        "WEAK=<0.35 / UNRUNNABLE=装载失败或红局>20%",
                "reason": pf["reason"], "checks": pf["checks"],
                "load_form": meta["form"], "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交（判决先行）；上线决策移交用户",
            }
            EV["verdicts"] = verdicts
            flush_evid()
            print("PREFLIGHT-FAIL:", piece, "UNRUNNABLE", flush=True)
            continue

        try:
            t_load = time.perf_counter()
            inner = load_entry(meta["main"], piece)
            preflight = {"ok": True,
                         "load_s": round(time.perf_counter() - t_load, 2),
                         "entry": getattr(inner, "__name__",
                                          type(inner).__name__)}
            del inner
        except Exception as exc:
            verdicts[piece] = {
                "verdict": "UNRUNNABLE",
                "rule": "装载失败或红局>20%",
                "reason": "装载失败: %s" % repr(exc)[:300],
                "load_form": meta["form"], "self_reported": meta["self_reported"],
                "vs_H1_h2h": None,
                "launch": "不发射不提交（判决先行）；上线决策移交用户",
            }
            EV["verdicts"] = verdicts
            flush_evid()
            print("LOAD-FAIL:", piece, repr(exc)[:120], flush=True)
            continue

        # ---- sim_bridge 在环认证 30/30（件 vs r40，双引擎）----
        piece_auth = None
        if DO_AUTH:
            try:
                piece_auth = sb.sim_bridge(
                    {"n_games": 30, "min_checked": 30,
                     "agents": [{"type": "python", "path": str(meta["main"])},
                                {"type": "python", "path": str(R40)}],
                     "record_path": str(EVID_DIR / ("sim_auth_record_%s.json"
                                                    % piece))},
                    PANEL_FOLDS + [675000 + i * 131 for i in range(28)])
                budget["auth_games"] += 30
            except Exception as exc:
                piece_auth = {"loaded": False, "consistency_ok": False,
                              "error": repr(exc)[:200]}
            EV["sim_auth"]["per_piece"] = EV["sim_auth"].get("per_piece", {})
            EV["sim_auth"]["per_piece"][piece] = {
                k: piece_auth.get(k) for k in
                ("loaded", "consistency", "consistency_ok", "degraded",
                 "degraded_reason", "engine", "version", "wall_speedup")}
        auth = piece_auth if (piece_auth and piece_auth.get("loaded")
                              and piece_auth.get("consistency_ok")) \
            else base_auth
        run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS,
                   "record_path": str(EVID_DIR / "sim_bridge_degraded.json")}
        flush_evid()

        # ---- 面板 ----
        panel = {}
        piece_rows = []
        for on, opath in PANEL.items():
            rows = play(unit_specs(piece, meta["main"], on, opath,
                                   PANEL_FOLDS), run_cfg)
            budget["panel_games"] += len(rows)
            piece_rows.extend(rows)
            panel[on] = fold_stats(rows)
            print("panel %s vs %s h2h=%s W/L/T=%s/%s/%s err=%d" %
                  (piece, on, panel[on]["h2h"], panel[on]["wins"],
                   panel[on]["losses"], panel[on]["ties"],
                   panel[on]["n_errors"]), flush=True)
            flush_evid()
        all_rows.extend(piece_rows)
        EV["panel_rows"] = all_rows
        EV["panel"][piece] = {
            "design": "%s 对 4 件面板：每对 n=%d fold 双席=%d 局（中性块 "
                      "674000+i*131）" % (piece, N_FOLDS, 2 * N_FOLDS),
            "pairs": panel}

        # ---- 判决 ----
        h_h1 = (panel.get("H1") or {}).get("h2h")
        n_err = sum((panel.get(o) or {}).get("n_errors", 0) for o in PANEL)
        n_tot = sum((panel.get(o) or {}).get("n_games", 0) for o in PANEL)
        if h_h1 is None or (n_tot and n_err / n_tot > 0.2):
            verdict = "UNRUNNABLE"
        elif h_h1 >= 0.5:
            verdict = "BEATS_CEILING"
        elif h_h1 >= 0.35:
            verdict = "COMPETITIVE"
        else:
            verdict = "WEAK"
        verdicts[piece] = {
            "verdict": verdict,
            "rule": "BEATS_CEILING=vs 王座 H1 h2h≥0.5 / COMPETITIVE=0.35-0.5 / "
                    "WEAK=<0.35 / UNRUNNABLE=装载失败或红局>20%",
            "vs_H1_h2h": h_h1,
            "panel_h2h": {o: (panel.get(o) or {}).get("h2h") for o in PANEL},
            "panel_WLT": {o: [panel[o]["wins"], panel[o]["losses"],
                              panel[o]["ties"]] for o in PANEL},
            "mean_margin_vs_H1": (panel.get("H1") or {}).get("mean_margin"),
            "realized_px_vs_H1": {
                "us": (panel.get("H1") or {}).get("realized_px_us"),
                "opp": (panel.get("H1") or {}).get("realized_px_opp")},
            "n_games": n_tot, "n_errors": n_err,
            "preflight": preflight,
            "load_form": meta["form"],
            "self_reported": meta["self_reported"],
            "piece_elapsed_s": round(time.perf_counter() - p_t0, 1),
            "launch": "不发射不提交（判决先行）；上线决策移交用户",
        }
        EV["verdicts"] = verdicts
        flush_evid()
        print("VERDICT:", piece, verdict, "vs_H1 h2h=", h_h1, flush=True)

    EV["verdicts"] = verdicts
    n_pp_auth = len((EV.get("sim_auth") or {}).get("per_piece") or {})
    budget["auth_games"] = 30 + 30 * n_pp_auth
    budget["panel_games"] = len(all_rows)
    budget["total_局次"] = budget["auth_games"] + budget["panel_games"]
    budget["note"] = ("局次=终局实数重算（baseline 认证 30 + 每件在环认证 30×%d "
                      "+ 逐局行 %d）" % (n_pp_auth, len(all_rows)))
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货，margin/realized_px 只作"
                     "参考；Never quote the peak；读数=本池实测，自报数字只登记")
    ANOMALIES.append("自报≠可迁移（战役 8 例教训）：5 件自报（银牌/#12/#330/提交号/对局"
                     "WLT）全部不作判决依据，仅登记对照行；官方终榜 ~10-15 出，名次均为"
                     " provisional")
    ANOMALIES.append("面板口径与 exp066_arena/godv7_arena 同构（674000+i*131、_fold_arm、"
                     "干净 margin）；H1=oc_c3 行为孪生（BT 527.8 并列王座），面板取 H1")
    ANOMALIES.append("装载语义=官方 last-callable（全新命名空间逐局装载）；romansvet 多文件"
                     "件每局清 kagg3* 模块缓存（harness 适配层，件本体零修改）")
    ANOMALIES.append("carson/debmal 装载失败为合法 verdict（UNRUNNABLE 附原因）；"
                     "debmal agent-stdio 编译过（bwrap 8.76s）但缺 route 表/配置 payload")
    ANOMALIES.append("taeyan c1200 为 21MB 生成件（lzma 内嵌源码），每局全新装载成本实测"
                     "见 piece_load_s_mean；其自报 56722176 提交号晚于截止，存疑待平台侧核")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
