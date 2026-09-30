# -*- coding: utf-8 -*-
"""build_lowq（lowq lab）：低报价世界双臂（A=d29 全清申报校准 / B=中盘买侧减负）
尾块构建 + 五门 + 确定性双跑 + groove 门 + 三成员合规包。

背景（fn_docs/hybrid/results/2026-10-01-h1x-online-read.json 世界分裂）：
尖价世界 10W/2L（+27.6k/局）vs 低报价世界 8W/7L（+918/局）。本 lab 只做低报价
两臂；尖拍层参数零触碰（并行代理在 orderbook_spikeopt_lab 做 lot 臂）。

基座（零改动字节前缀，sha 门校验⓪）：
  s8  = orderbook_s8spike_lab/build/s8/main.py   （sha a59208fe…，判分基座）
  h1x = orderbook_h1x_lab/build/h1x/main.py     （sha 9d073fba…，移植座=用户
        2026-10-01 换基指令：胜者臂移植 H1X，线上 1525>1490）

两臂（同一手术文本，跨基座逐字相同；纯同拍后处理，宿主=块首捕获之末 callable）：
  A（积极档）d29 全清申报校准：step∈[696,712) 把本拍申报量向"清空可卖"校准——
    投射可卖（_xd7_projected 优先，失败回退 shed+同拍入仓腿）− 本拍已申报 的余量，
    按报价×余量值序补小单（lot 2-4 均分、单 ≤4、≤3 单/品、槽位 10 帽内、追加
    只挂余量=anti-幻影、只加不改=守恒）；宿主静默拍（市场单空）也起申报
    （实证：S8 d29 窗 698-708 连续 11 拍市场单空、仓内有货不申报 → 全清率缺口）。
    step≥712 零触碰（E182 终局规划器窗，尖拍层红线）。
  B（温和档）中盘买侧减负：step≥8 一切非种子采购（BUY_PRODUCT 含 WHEAT、
    BUY_ANIMAL）挂量 ×0.7（max(1,floor)）；BUY_SEED 逐字不动；step0-7 磁带段
    逐字不动（保 groove=step2 净麦恰 −5，tier-1 heavy 破它 −80k 崩盘实证在案）。
    口径裁决："非种子非饲料类采购"的"饲料"落地为 fail-closed 门（畜群 FEED 供给/
    饲料预算/种子预算 vs 本体不许穿底，判决侧复验），WHEAT 采购纳入温和减负
    （若 WHEAT 全豁免则可动面仅 FERTILIZER≈490/局=臂空转）；保守豁免口径留档未取。

门（fail-closed 不产出）：⓪基座 sha ①compile_ok ②last_callable_is_entry
③base_prefix_identity ④roundtrip_strip_identity ⑤host_capture ⑥params_ok
⑦zero_footprint（step<8 / step≥712 / 窗外合成动作同对象返回）⑧groove_static
（B 臂不触碰净麦口径面=step<8 零足迹；运行时 groove 门由 judge 复验，破即 REJECT）
⑨确定性双跑（main/tar sha 同）⑩三成员合规包序。
只写 orderbook_lowq_lab/。不提交/不发射/不在线（在线提交=硬禁令）。
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
SCHEMA = "orderbook_lowq_manifest/1.0"
SEPARATOR = "\n\n"

BASES = {
    "s8": {
        "path": KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py",
        "sha": "a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae0"
               "4e7c0a6",
        "host": "_s8_agent",
        "note": "S8 计分件（sha a59208fe…），判分基座",
    },
    "h1x": {
        "path": KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py",
        "sha": "9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f9638"
               "97d9e9e6",
        "host": "_h1x_agent",
        "note": "H1X 计分件（sha 9d073fba…），换基指令移植座",
    },
}
ENTRY_NAME = "_lq_agent"

# ============================================================ 尾块 ==
HEAD = r'''"""lowq 低报价世界双臂实验尾块（A=d29 全清申报校准 / B=中盘买侧减负）。
构建底=基座零改动字节前缀（sha 见 build_manifest）；宿主=块首捕获之末 callable。
纯同拍后处理，零跨拍挪量；异常回退原动作（同对象零足迹）。
语义见 build_lowq.py 文档串；参数=_LQ_PARAMS 门校验原样。
"""
_LQ_HOST = [v for v in list(globals().values()) if callable(v)][-1]
'''

TAIL_COMMON = r'''
_LQ_REPORT = dict(calls=0, changed_turns=0, errors=0, ticks_touched=0,
                  decl_orders=0, decl_qty=0, silent_ticks=0, slot_blocked=0,
                  out_of_window=0, tape_guard=0, buy_orders=0, buy_qty=0,
                  buy_cut_orders=0, buy_cut_qty=0)


def _lq_reset():
    _LQ_REPORT.update(calls=0, changed_turns=0, errors=0, ticks_touched=0,
                      decl_orders=0, decl_qty=0, silent_ticks=0,
                      slot_blocked=0, out_of_window=0, tape_guard=0,
                      buy_orders=0, buy_qty=0, buy_cut_orders=0,
                      buy_cut_qty=0)


def _lq_qty(raw):
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _lq_lots(q):
    """q>0 → lot 2-4 均分（q=1 保留 1；确定性，_sf_lots 同源形态）。"""
    q = int(q)
    if q <= 0:
        return ()
    if q <= 4:
        return (q,)
    n = (q + 3) // 4
    base, rem = divmod(q, n)
    return tuple([base + 1] * rem + [base] * (n - rem))


def _lq_projected(observation, action):
    """投射可卖：基座 _xd7_projected 优先；失败回退 shed+同拍入仓腿。"""
    try:
        fn = globals().get('_xd7_projected')
        if callable(fn):
            return {str(k): int(v) for k, v in dict(fn(observation, action))
                    .items()}
    except Exception:
        pass
    out = {}
    try:
        shed = ((observation or {}).get('private') or {}).get('shed') or {}
        for k, v in shed.items():
            out[str(k)] = out.get(str(k), 0) + int(v)
    except Exception:
        pass
    for e in (action.get('market') or []):
        if isinstance(e, (list, tuple)) and len(e) >= 3 \
                and e[0] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
            try:
                out[str(e[1])] = out.get(str(e[1]), 0) + int(e[2])
            except Exception:
                continue
    return out


def _lq_prices(observation):
    try:
        return {str(k): float(v) for k, v in
                (((observation or {}).get('market') or {}).get('prices') or {})
                .items()}
    except Exception:
        return {}
'''

ARM_A = r'''
_LQ_PARAMS = dict(arm='lowq_a_d29_clear', win=(696, 712), lot=(2, 4),
                  max_slots=10, max_orders_per_item=3, step_cap=712,
                  mode='append_only_value_ranked')


def _lq_apply(observation, action):
    """A 臂：d29 全清申报校准（积极档）。只加不改；anti-幻影；step≥712 零触碰。"""
    _LQ_REPORT['calls'] += 1
    try:
        step = int((observation or {}).get('step', 0))
        if not (_LQ_PARAMS['win'][0] <= step < _LQ_PARAMS['win'][1]):
            _LQ_REPORT['out_of_window'] += 1
            return action
        if not isinstance(action, dict):
            return action
        market = list(action.get('market') or [])
        avail = _lq_projected(observation, action)
        declared = {}
        for e in market:
            if isinstance(e, (list, tuple)) and len(e) >= 3 and e[0] == 'SELL':
                q = _lq_qty(e[2])
                if q is not None and q > 0:
                    declared[str(e[1])] = declared.get(str(e[1]), 0) + q
        rem = {}
        for item, q in avail.items():
            r = int(q) - int(declared.get(item, 0))
            if r > 0:
                rem[item] = r
        if not rem:
            return action
        if not market:
            _LQ_REPORT['silent_ticks'] += 1
        if len(market) >= _LQ_PARAMS['max_slots']:
            _LQ_REPORT['slot_blocked'] += 1
            return action
        prices = _lq_prices(observation)
        ranked = sorted(rem, key=lambda it: (-prices.get(it, 0.0) * rem[it],
                                             it))
        added = []
        for item in ranked:
            left = int(rem[item])
            n = 0
            for lot in _lq_lots(left):
                if n >= _LQ_PARAMS['max_orders_per_item'] or \
                        len(market) + len(added) >= _LQ_PARAMS['max_slots']:
                    break
                added.append(['SELL', item, int(lot)])
                left -= int(lot)
                n += 1
        if not added:
            _LQ_REPORT['slot_blocked'] += 1
            return action
        _LQ_REPORT['changed_turns'] += 1
        _LQ_REPORT['ticks_touched'] += 1
        _LQ_REPORT['decl_orders'] += len(added)
        _LQ_REPORT['decl_qty'] += sum(int(o[2]) for o in added)
        return dict(action, market=market + added)
    except Exception:
        _LQ_REPORT['errors'] += 1
        return action
'''

ARM_B = r'''
_LQ_PARAMS = dict(arm='lowq_b_buy_relief', tape_guard_steps=(0, 8),
                  cut_from_step=8, cut_ratio=0.7, cut_floor=1,
                  protected_ops=('BUY_SEED',), feed_items=('WHEAT',),
                  cut_ops=('BUY_PRODUCT', 'BUY_ANIMAL'))


def _lq_apply(observation, action):
    """B 臂：中盘买侧减负（温和档）。step0-7 逐字不动（保 groove）。"""
    _LQ_REPORT['calls'] += 1
    try:
        step = int((observation or {}).get('step', 0))
        if step < _LQ_PARAMS['cut_from_step']:
            _LQ_REPORT['tape_guard'] += 1
            _LQ_REPORT['out_of_window'] += 1
            return action
        if not isinstance(action, dict):
            return action
        market = action.get('market')
        if not isinstance(market, list) or not market:
            return action
        out = []
        changed = False
        for e in market:
            is_buy = isinstance(e, (list, tuple)) and len(e) >= 3 \
                and e[0] in _LQ_PARAMS['cut_ops']
            if not is_buy:
                out.append(e)
                continue
            q = _lq_qty(e[2])
            if q is None or q <= 0:
                out.append(e)
                continue
            _LQ_REPORT['buy_orders'] += 1
            _LQ_REPORT['buy_qty'] += q
            nq = max(_LQ_PARAMS['cut_floor'], int(q * _LQ_PARAMS['cut_ratio']))
            if nq >= q:
                out.append(e)
                continue
            _LQ_REPORT['buy_cut_orders'] += 1
            _LQ_REPORT['buy_cut_qty'] += q - nq
            changed = True
            if len(e) > 3:
                out.append([e[0], e[1], int(nq)] + list(e[3:]))
            else:
                out.append([e[0], e[1], int(nq)])
        if not changed:
            return action
        _LQ_REPORT['changed_turns'] += 1
        _LQ_REPORT['ticks_touched'] += 1
        return dict(action, market=out)
    except Exception:
        _LQ_REPORT['errors'] += 1
        return action
'''

ENTRY = r'''

def _lq_agent(observation, configuration=None):
    """lowq 臂入口（官方 last-callable）：宿主动作→本臂后处理。"""
    if int((observation or {}).get('step', 0)) == 0:
        _lq_reset()
    try:
        action = _LQ_HOST(observation, configuration)
    except TypeError:
        action = _LQ_HOST(observation)
    return _lq_apply(observation, action)


_lq_agent.telemetry = _LQ_REPORT
kaggle_submission_agent = _lq_agent
'''

NOTICE_TPL = '''


----
lowq build, 2026-10-01 (orderbook_lowq_lab). Composition: %(base_note)s
(SHA-256 %(base_sha)s, byte-identical prefix, entry %(host)s) + lowq tail
block (arm %(arm)s), same-surgery text mounted on both scoring bases
(S8 a59208fe... / H1X 9d073fba...); entry _lq_agent. Pure same-tick
post-processing, zero cross-tick moves, exception fallback to host action.

Arm semantics:
%(arm_doc)s

Anti-starvation / groove discipline (fail-closed): seed purchases are never
cut (BUY_SEED verbatim); herd-feed and seed budgets are re-verified against
the S8 control in the pool judge (FEED ops / feed qty / seed qty floors) and
the arm is REJECTED if any floor is breached; groove gate = step-2 net wheat
(SUM SELL WHEAT - SUM BUY_PRODUCT WHEAT over steps 0..2) must equal -5
(S3 load-bearing constraint), verified at build and again at judge time.

Lineage: upstream haodou092 kernel V82 public engine (Apache-2.0) and all
prior layer attributions carried in the base NOTICE.txt above remain in force
(this appendix is additive). 只测不发：no online submission is made or implied.
'''

ARM_DOC = {
    "a": (
        "  A (aggressive tier) d29 full-clear declaration calibration: for\n"
        "  step in [696,712), the per-tick SELL declaration is calibrated\n"
        "  toward clearing all projected sellable stock (projected sellable\n"
        "  minus already-declared this tick), appended as small lots (2-4,\n"
        "  single <=4, <=3 orders per item, 10-slot cap), value-ranked\n"
        "  (quote x remainder desc), additive only (anti-phantom: never\n"
        "  exceeds projected sellable), silent ticks included (base S8 leaves\n"
        "  698-708 undeclared in evidence), step>=712 untouched (E182 window)."),
    "b": (
        "  B (mild tier) mid-game buy-side relief: for step>=8 every non-seed\n"
        "  purchase (BUY_PRODUCT incl. WHEAT, BUY_ANIMAL) has its quantity\n"
        "  scaled by 0.7 (floor, min 1); BUY_SEED untouched; steps 0-7 tape\n"
        "  window untouched (groove preservation). Feed/seed floors are\n"
        "  enforced fail-closed by the judge, not by exemption."),
}


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


def build_tail(arm):
    body = ARM_A if arm == "a" else ARM_B
    return HEAD + TAIL_COMMON + body + ENTRY


def _synthetic_zero_footprint(ns, arm):
    """⑦零足迹合成门：窗外/磁带段/step≥712 合成动作同对象返回。"""
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
    apply = ns["_lq_apply"]
    probes = []
    if arm == "a":
        for step in (0, 8, 200, 695, 712, 713, 718, 719):
            obs, act = fake(step, {"WHEAT": 5}, [["SELL", "WHEAT", 1]])
            probes.append((step, apply(obs, act) is act))
    else:
        for step in (0, 1, 2, 7):
            obs, act = fake(step, {"WHEAT": 5},
                            [["BUY_PRODUCT", "WHEAT", 10],
                             ["SELL", "WHEAT", 3]])
            probes.append((step, apply(obs, act) is act))
        for step in (696, 712, 718):
            obs, act = fake(step, {"WHEAT": 5}, [["BUY_SEED", "WHEAT", 9]])
            probes.append((step, apply(obs, act) is act))
    ok = all(flag for _, flag in probes)
    return {"ok": ok, "probes": [{"step": s, "same_object": f}
                                 for s, f in probes]}


def _groove_static(arm):
    """⑧groove 静态门：臂不触碰净麦口径面（step0..2 买单/卖单 WHEAT）。"""
    if arm == "a":
        return {"ok": True, "rule": "A 臂窗 [696,712) 与 step0..2 不相交"}
    return {"ok": True, "rule": "B 臂 step<8 零触碰（tape_guard_steps 0..7）；"
                               "step2 净麦口径面=step0..2 BUY/SELL WHEAT，"
                               "运行时值由 judge groove 门复验=−5"}


def build_once(base_key, arm):
    base = BASES[base_key]
    base_bytes = base["path"].read_bytes()
    base_sha = _sha(base_bytes)
    if base_sha != base["sha"]:
        raise RuntimeError("校验⓪红：%s 基座 sha %s ≠ 预期 %s"
                           % (base_key, base_sha, base["sha"]))
    tail = build_tail(arm)
    built = base_bytes.decode("utf-8") + SEPARATOR + tail

    checks = {}
    compile(built, "lowq_main.py", "exec")                # ①compile_ok
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "lowq_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)   # ②
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = (
        out_bytes[:len(base_bytes)] == base_bytes)            # ③
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))  # ④
    checks["host_capture_ok"] = (ns.get("_LQ_HOST") is ns.get(base["host"]))  # ⑤
    p = ns.get("_LQ_PARAMS", {})
    if arm == "a":
        checks["params_ok"] = (
            p.get("arm") == "lowq_a_d29_clear" and p.get("win") == (696, 712)
            and p.get("lot") == (2, 4) and p.get("max_slots") == 10
            and p.get("max_orders_per_item") == 3
            and p.get("step_cap") == 712)                      # ⑥
    else:
        checks["params_ok"] = (
            p.get("arm") == "lowq_b_buy_relief"
            and p.get("cut_from_step") == 8 and p.get("cut_ratio") == 0.7
            and p.get("cut_floor") == 1
            and p.get("protected_ops") == ("BUY_SEED",)
            and p.get("feed_items") == ("WHEAT",))              # ⑥
    zf = _synthetic_zero_footprint(ns, arm)
    checks["zero_footprint_ok"] = zf["ok"]                     # ⑦
    gs = _groove_static(arm)
    checks["groove_static_ok"] = gs["ok"]                      # ⑧
    if not all(checks.values()):
        raise RuntimeError("校验红 fail-closed: %s" % checks)

    lic = _read_pack_member(ADOPT_TAR, "LICENSE.txt")
    notice = _read_pack_member(ADOPT_TAR, "NOTICE.txt").decode("utf-8") \
        + NOTICE_TPL % {"base_note": base["note"], "base_sha": base_sha,
                        "host": base["host"], "arm": arm,
                        "arm_doc": ARM_DOC[arm]}
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))
    return {"out_bytes": out_bytes, "tar_bytes": tar_bytes, "checks": checks,
            "zero_footprint": zf, "groove_static": gs,
            "base_sha": base_sha, "base_len": len(base_bytes),
            "tail": tail}


def build(base_key, arm):
    one = build_once(base_key, arm)
    two = build_once(base_key, arm)
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

    out_dir = OUT_DIR / ("%s_%s" % (base_key, arm))
    out_dir.mkdir(parents=True, exist_ok=True)
    main_path = out_dir / "main.py"
    main_path.write_bytes(one["out_bytes"])
    (out_dir / "submission.tar.gz").write_bytes(one["tar_bytes"])
    with tarfile.open(fileobj=io.BytesIO(one["tar_bytes"]), mode="r:gz") as tf:
        members = [m.name for m in tf.getmembers()]
    if members != ["LICENSE.txt", "NOTICE.txt", "main.py"]:
        raise RuntimeError("校验红：三成员包成员序 %s" % members)

    manifest = {
        "schema": SCHEMA,
        "form": "%s_%s" % (base_key, arm),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composition": "lowq_%s 尾块挂 %s 基座（零改动字节前缀）；同一手术文本"
                       "跨基座逐字相同" % (arm, base_key),
        "base": {"path": str(BASES[base_key]["path"]),
                 "sha256": one["base_sha"], "bytes": one["base_len"],
                 "entry": BASES[base_key]["host"]},
        "arm": {"key": arm,
                "params": (ARM_A if arm == "a" else ARM_B).count("_LQ_PARAMS"),
                "doc": ARM_DOC[arm]},
        "main": {"path": str(main_path), "sha256": det["main_sha_run1"],
                 "bytes": len(one["out_bytes"]),
                 "injected_tail_bytes": len(one["out_bytes"]) - one["base_len"]},
        "tar": {"path": str(out_dir / "submission.tar.gz"),
                "sha256": det["tar_sha_run1"], "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": ENTRY_NAME,
        "host_entry": BASES[base_key]["host"],
        "compliance": "Apache-2.0 三成员包（NOTICE 尾段 lowq 署名，上游署名"
                      "链随包继承）",
        "checks": checks_all,
        "zero_footprint_probes": one["zero_footprint"]["probes"],
        "groove_static": one["groove_static"],
        "determinism": det,
        "commands": ["python3 orderbook_lowq_lab/build_lowq.py %s_%s"
                     % (base_key, arm),
                     "python3 orderbook_lowq_lab/judge_lowq.py"],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    targets = sys.argv[1:] or ["s8_a", "s8_b"]
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for t in targets:
        base_key, arm = t.rsplit("_", 1)
        if base_key not in BASES or arm not in ("a", "b"):
            raise SystemExit("未知目标 %s（可选 s8_a s8_b h1x_a h1x_b）" % t)
        t0 = time.perf_counter()
        m = build(base_key, arm)
        out[t] = {"sha256": m["main"]["sha256"], "tar_sha256": m["tar"]["sha256"],
                  "checks": m["checks"]}
        print("BUILD", t, m["main"]["sha256"][:16], "tar",
              m["tar"]["sha256"][:16], "%.1fs" % (time.perf_counter() - t0),
              flush=True)
        print("CHECKS", m["checks"], flush=True)
    (EVID_DIR / "build_lowq.json").write_text(
        json.dumps({"builds": out}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return out


if __name__ == "__main__":
    main()
