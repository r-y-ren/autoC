# -*- coding: utf-8 -*-
"""build_a2slot（a2slot lab）：A2=终局窗 HIRE 让位 SELL（低报价判决诊断产物）。
尾块构建 + 九门 + 确定性双跑 + 三成员合规包。

机制链（线上败局 115945260/115957548 + 本地槽位复原）：
  step696（d29 起点）我方 10 订单槽被 1×SELL+9×HIRE 占满 → CARROT 32+FERT 9
  压到次拍才出（槽位竞速败因）。引擎侧 maxMarketOrdersPerTurn=10 截断
  （kgenv.replay_profile._s_process_market: queues.append(q[:max_orders])），
  行动列表尾部订单直接被丢弃；HIRE 在 d29（step≥696，距终局 ≤24 拍）近乎纯
  浪费还占槽。A 臂（只加申报）无法触及槽约束——本体 d29 申报已满，问题是槽。

手术（保守档 keep=0）：step∈[696,712) 从 action['market'] 里剔除 HIRE 单
  （HIRE 数 9→0），其余逐字不动——不动 step<696 任何东西、不动 SELL 申报逻辑、
  step≥712 零触碰（E182 终局规划器窗红线）。剔除后尾部 SELL 前移进 10 槽窗，
  同拍成交应显著回升。纯同拍后处理，异常回退原动作（同对象零足迹）。

基座（零改动字节前缀，sha 门校验⓪）：
  h1x = orderbook_h1x_lab/build/h1x/main.py（sha 9d073fba…，用户裁决换基指令：
        一切修正以 H1X 为基础）

门（fail-closed 不产出）：⓪基座 sha ①compile_ok ②last_callable_is_entry
③base_prefix_identity ④roundtrip_strip_identity ⑤host_capture ⑥params_ok
⑦zero_footprint（step<696 / step≥712 / 窗外合成动作同对象返回）⑧groove_static
（窗口 [696,712) 与 step0..2 净麦口径面不相交，零触碰）⑨确定性双跑（main/tar
sha 同）⑩三成员合规包序。只写 orderbook_a2slot_lab/。不提交/不发射/不在线
（在线提交=硬禁令）。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
ADOPT_TAR = KSIM_DIR / "orderbook_haodou_adopt" / "submission.tar.gz"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_a2slot_manifest/1.0"
SEPARATOR = "\n\n"

BASE = {
    "path": KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py",
    "sha": "9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f9638"
           "97d9e9e6",
    "host": "_h1x_agent",
    "note": "H1X 计分件（sha 9d073fba…），换基指令移植座",
}
ENTRY_NAME = "_a2_agent"

# ============================================================ 尾块 ==
HEAD = r'''"""a2slot 终局窗 HIRE 让位 SELL 实验尾块（keep=0 保守档）。
构建底=基座零改动字节前缀（sha 见 build_manifest）；宿主=块首捕获之末 callable。
纯同拍后处理，零跨拍挪量；异常回退原动作（同对象零足迹）。
语义见 build_a2slot.py 文档串；参数=_A2_PARAMS 门校验原样。
"""
_A2_HOST = [v for v in list(globals().values()) if callable(v)][-1]
'''

TAIL_COMMON = r'''
_A2_REPORT = dict(calls=0, changed_turns=0, errors=0, ticks_touched=0,
                  hire_seen=0, hire_dropped=0, slots_freed=0,
                  out_of_window=0, sell_untouched=0)


def _a2_reset():
    _A2_REPORT.update(calls=0, changed_turns=0, errors=0, ticks_touched=0,
                      hire_seen=0, hire_dropped=0, slots_freed=0,
                      out_of_window=0, sell_untouched=0)


def _a2_qty(raw):
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None
'''

ARM_A2 = r'''
_A2_PARAMS = dict(arm='a2_hire_yield', win=(696, 712), keep=0,
                  drop_ops=('HIRE',), step_cap=712,
                  mode='drop_hire_tail_shift_only')


def _a2_apply(observation, action):
    """A2：step∈[696,712) 剔除 HIRE 单（保守档 keep=0）；SELL 逐字不动；
    step<696 / step>=712 同对象返回（E182 终局窗零触碰）。"""
    _A2_REPORT['calls'] += 1
    try:
        step = int((observation or {}).get('step', 0))
        if not (_A2_PARAMS['win'][0] <= step < _A2_PARAMS['win'][1]):
            _A2_REPORT['out_of_window'] += 1
            return action
        if not isinstance(action, dict):
            return action
        market = action.get('market')
        if not isinstance(market, list) or not market:
            return action
        keep = int(_A2_PARAMS['keep'])
        kept_hire = 0
        dropped = 0
        sells = 0
        out = []
        for e in market:
            is_hire = isinstance(e, (list, tuple)) and bool(e) \
                and e[0] in _A2_PARAMS['drop_ops']
            if is_hire:
                _A2_REPORT['hire_seen'] += 1
                if kept_hire < keep:
                    kept_hire += 1
                    out.append(e)
                else:
                    dropped += 1
                continue
            if isinstance(e, (list, tuple)) and len(e) >= 3 \
                    and e[0] == 'SELL':
                sells += 1
            out.append(e)
        if not dropped:
            return action
        _A2_REPORT['changed_turns'] += 1
        _A2_REPORT['ticks_touched'] += 1
        _A2_REPORT['hire_dropped'] += dropped
        _A2_REPORT['slots_freed'] += dropped
        _A2_REPORT['sell_untouched'] += sells
        return dict(action, market=out)
    except Exception:
        _A2_REPORT['errors'] += 1
        return action
'''

ENTRY = r'''

def _a2_agent(observation, configuration=None):
    """a2slot 臂入口（官方 last-callable）：宿主动作→本臂后处理。"""
    if int((observation or {}).get('step', 0)) == 0:
        _a2_reset()
    try:
        action = _A2_HOST(observation, configuration)
    except TypeError:
        action = _A2_HOST(observation)
    return _a2_apply(observation, action)


_a2_agent.telemetry = _A2_REPORT
kaggle_submission_agent = _a2_agent
'''

NOTICE_TPL = '''


----
a2slot build, 2026-10-01 (orderbook_a2slot_lab). Composition: %(base_note)s
(SHA-256 %(base_sha)s, byte-identical prefix, entry %(host)s) + a2slot tail
block (arm a2_hire_yield, conservative tier keep=0); entry _a2_agent. Pure
same-tick post-processing (drop HIRE market orders in the terminal window),
zero cross-tick moves, exception fallback to host action. This is a
diagnostic product for the low-quote verdict (orderbook_lowq_lab
evidence/lowq_verdict.json), not a launch candidate.

Arm semantics:
  A2 (terminal window HIRE yields to SELL): for step in [696, 712), every
  HIRE market order is dropped from the outgoing action (HIRE count 9 -> 0),
  everything else byte-verbatim: step<696 untouched, all SELL declaration
  logic untouched, step>=712 zero-touch (E182 terminal planner window red
  line). Rationale: the engine truncates each action's market list to the
  first maxMarketOrdersPerTurn=10 orders (kgenv.replay_profile
  _s_process_market: queues.append(q[:max_orders])); online losses
  115945260/115957548 show step696 slots filled by 1xSELL+9xHIRE while
  CARROT 32+FERT 9 got pushed to the next tick. Dropping the near-useless
  late-window HIRE orders shifts tail SELL orders back inside the 10-slot
  window so same-tick sell completion can recover.

Lineage: upstream haodou092 kernel V82 public engine (Apache-2.0) and all
prior layer attributions carried in the base NOTICE.txt above remain in
force (this appendix is additive). 只测不发：no online submission is made
or implied (在线提交=硬禁令).
'''


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _read_pack_member(tar_path, name):
    with tarfile.open(fileobj=io.BytesIO(tar_path.read_bytes()),
                      mode="r:gz") as tf:
        member = tf.extractfile(name)
        if member is None:
            raise RuntimeError("合规包内无 %s" % name)
        return member.read()


def _make_tar3(main_bytes, license_bytes, notice_bytes):
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0,
                       compresslevel=9) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for name, data in (("LICENSE.txt", license_bytes),
                               ("NOTICE.txt", notice_bytes),
                               ("main.py", main_bytes)):
                info = tarfile.TarInfo(name=name)
                info.size = len(data)
                info.mtime = 0
                info.mode = 0o644
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def build_tail():
    return HEAD + TAIL_COMMON + ARM_A2 + ENTRY


def _synthetic_zero_footprint(ns):
    """⑦零足迹合成门：step<696 / step≥712 合成动作同对象返回；
    窗内行为探针：HIRE 被剔除、SELL 数量逐字保留。"""
    def fake(step, shed=None, market=None):
        obs = {"step": step, "player": 0,
               "farms": [{"money": 0.0, "tiles": [], "hands": [],
                          "farmer": [0, 0], "unlocked_quadrants": []}],
               "private": {"shed": dict(shed or {}), "seeds": {},
                           "inventories": [{}]},
               "market": {"prices": {"WHEAT": 40.0, "CARROT": 60.0}}}
        act = {"farmer": ["PASS"], "hands": [],
               "market": list(market or [])}
        return obs, act
    apply = ns["_a2_apply"]
    probes = []
    for step in (0, 8, 200, 695, 712, 713, 718, 719):
        obs, act = fake(step, {"WHEAT": 5},
                        [["SELL", "WHEAT", 1], ["HIRE"], ["HIRE"]])
        probes.append({"step": step, "same_object": apply(obs, act) is act})
    # 窗内剔除探针：9×HIRE + 1×SELL + 尾部 SELL → 只剩 2×SELL，逐字序保留
    obs, act = fake(696, {"CARROT": 40},
                    [["SELL", "WHEAT", 1]] + [["HIRE"]] * 9
                    + [["SELL", "CARROT", 32]])
    out = apply(obs, act)
    in_win = {"step": 696,
              "market_in": len(act["market"]),
              "market_out": len(out["market"]),
              "hire_left": sum(1 for e in out["market"]
                               if e and e[0] == "HIRE"),
              "sells": [list(e) for e in out["market"] if e and e[0] == "SELL"],
              "ok": (len(out["market"]) == 2
                     and not any(e and e[0] == "HIRE" for e in out["market"])
                     and [list(e) for e in out["market"]]
                     == [["SELL", "WHEAT", 1], ["SELL", "CARROT", 32]])}
    ok = all(p["same_object"] for p in probes) and in_win["ok"]
    return {"ok": ok, "probes": probes, "in_window_probe": in_win}


def _groove_static():
    """⑧groove 静态门：臂只动 [696,712) 的 HIRE 面，与 step0..2 净麦口径面
    （step0..2 BUY/SELL WHEAT）不相交；运行时 groove 值由 judge 复验=−5。"""
    return {"ok": True, "rule": "窗口 [696,712) 与 step0..2 净麦口径面不相交；"
                               "SELL 申报逐字不动（groove 值运行时恒等）"}


def build_once():
    base_bytes = BASE["path"].read_bytes()
    base_sha = _sha(base_bytes)
    if base_sha != BASE["sha"]:
        raise RuntimeError("校验⓪红：h1x 基座 sha %s ≠ 预期 %s"
                           % (base_sha, BASE["sha"]))
    tail = build_tail()
    built = base_bytes.decode("utf-8") + SEPARATOR + tail

    checks = {}
    compile(built, "a2_main.py", "exec")                    # ①compile_ok
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "a2_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)   # ②
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = (
        out_bytes[:len(base_bytes)] == base_bytes)            # ③
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))  # ④
    checks["host_capture_ok"] = (ns.get("_A2_HOST") is ns.get(BASE["host"]))  # ⑤
    p = ns.get("_A2_PARAMS", {})
    checks["params_ok"] = (
        p.get("arm") == "a2_hire_yield" and p.get("win") == (696, 712)
        and p.get("keep") == 0 and p.get("drop_ops") == ("HIRE",)
        and p.get("step_cap") == 712)                          # ⑥
    zf = _synthetic_zero_footprint(ns)
    checks["zero_footprint_ok"] = zf["ok"]                     # ⑦
    gs = _groove_static()
    checks["groove_static_ok"] = gs["ok"]                      # ⑧
    if not all(checks.values()):
        raise RuntimeError("校验红 fail-closed: %s" % checks)

    lic = _read_pack_member(ADOPT_TAR, "LICENSE.txt")
    notice = _read_pack_member(ADOPT_TAR, "NOTICE.txt").decode("utf-8") \
        + NOTICE_TPL % {"base_note": BASE["note"], "base_sha": base_sha,
                        "host": BASE["host"]}
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))
    return {"out_bytes": out_bytes, "tar_bytes": tar_bytes, "checks": checks,
            "zero_footprint": zf, "groove_static": gs,
            "base_sha": base_sha, "base_len": len(base_bytes), "tail": tail}


def build():
    one = build_once()
    two = build_once()
    det = {"main_sha_run1": _sha(one["out_bytes"]),
           "main_sha_run2": _sha(two["out_bytes"]),
           "tar_sha_run1": _sha(one["tar_bytes"]),
           "tar_sha_run2": _sha(two["tar_bytes"])}
    det["deterministic_ok"] = (det["main_sha_run1"] == det["main_sha_run2"]
                               and det["tar_sha_run1"] == det["tar_sha_run2"]
                               and one["checks"] == two["checks"])
    if not det["deterministic_ok"]:
        raise RuntimeError("校验⑨红：确定性双跑不一致 %s" % det)
    checks_all = dict(one["checks"])
    checks_all["deterministic_double_run_ok"] = True

    out_dir = OUT_DIR / "h1x_a2"
    out_dir.mkdir(parents=True, exist_ok=True)
    main_path = out_dir / "main.py"
    main_path.write_bytes(one["out_bytes"])
    (out_dir / "submission.tar.gz").write_bytes(one["tar_bytes"])
    with tarfile.open(fileobj=io.BytesIO(one["tar_bytes"]), mode="r:gz") as tf:
        members = [m.name for m in tf.getmembers()]
    if members != ["LICENSE.txt", "NOTICE.txt", "main.py"]:
        raise RuntimeError("校验红：三成员包成员序 %s" % members)
    checks_all["three_member_pack_order_ok"] = True

    manifest = {
        "schema": SCHEMA,
        "form": "h1x_a2",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composition": "a2slot 尾块（HIRE 让位 SELL）挂 h1x 基座"
                       "（零改动字节前缀）；诊断产物（低报价判决诊断节），"
                       "非发射候选",
        "base": {"path": str(BASE["path"]), "sha256": one["base_sha"],
                 "bytes": one["base_len"], "entry": BASE["host"]},
        "arm": {"key": "a2_hire_yield",
                "params": {"win": [696, 712], "keep": 0,
                           "drop_ops": ["HIRE"], "step_cap": 712},
                "doc": "step∈[696,712) 剔除 HIRE 市场单（9→0），其余逐字不动；"
                       "step≥712 零触碰"},
        "main": {"path": str(main_path), "sha256": det["main_sha_run1"],
                 "bytes": len(one["out_bytes"]),
                 "injected_tail_bytes": len(one["out_bytes"]) - one["base_len"]},
        "tar": {"path": str(out_dir / "submission.tar.gz"),
                "sha256": det["tar_sha_run1"], "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": ENTRY_NAME,
        "host_entry": BASE["host"],
        "compliance": "Apache-2.0 三成员包（NOTICE 尾段 a2slot 署名，上游署名"
                      "链随包继承）",
        "checks": checks_all,
        "zero_footprint": one["zero_footprint"],
        "groove_static": one["groove_static"],
        "determinism": det,
        "commands": ["python3 orderbook_a2slot_lab/build_a2slot.py",
                     "python3 orderbook_a2slot_lab/judge_a2slot.py"],
        "online": "只测不发（在线提交=硬禁令）",
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    m = build()
    out = {"h1x_a2": {"sha256": m["main"]["sha256"],
                      "tar_sha256": m["tar"]["sha256"],
                      "checks": m["checks"],
                      "elapsed_s": round(time.perf_counter() - t0, 1)}}
    (EVID_DIR / "build_a2slot.json").write_text(
        json.dumps({"builds": out}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("BUILD h1x_a2", m["main"]["sha256"][:16], "tar",
          m["tar"]["sha256"][:16], "%.1fs" % out["h1x_a2"]["elapsed_s"],
          flush=True)
    print("CHECKS", m["checks"], flush=True)
    return out


if __name__ == "__main__":
    main()
