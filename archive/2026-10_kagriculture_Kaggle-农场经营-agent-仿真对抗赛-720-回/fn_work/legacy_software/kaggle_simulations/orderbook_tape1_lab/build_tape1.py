# -*- coding: utf-8 -*-
"""build_tape1（tape1 lab）：day0 做市单加重磁带变体（分析50 P1 台阶一）构建+五门+确定性打包。

手术对象（band-deepcut §4 我方行 → main.py 逐令定位）：
  我方 day0 磁带市场段 = tape step0  [BUY_PRODUCT WHEAT 8 | SELL WHEAT 3 | BUY_SEED WHEAT 1]
                     + tape step1  [HIRE×5 | BUY_ANIMAL COW 2 | SHEEP 2]（v9 剥离麦单后）
  （fingerprint s1/s2 = tape step0/1，索引 +1；s4 PICKUP SHEEP=tape s3、s7 MELON=tape s6 佐证）
  生成链：_R108_DATA route0 磁带 → _R42_OPENING（s0=13/30/30）→ _v9_opening
  （step0 重写为 V9_OPENING_STEP0=(BUY 8,SELL 3)、step1 剥麦单）→ _alt_install
  'HybridOpening'（+BUY_SEED WHEAT 1 功能种子腿）→ opening_liquidity_agent 观测口径
  [BUY 8,SELL 3,BUY_SEED 1]（该层 opening_stock_ok 断言即实证）。
  我方该段自 haodou 采纳以来从未调过（盲区）。

三档变体（挂 H1X 9d073fba… / 同手术挂 S8 a59208fe…）：
  ①WHEAT 首卖 3u→15/26/50u（轻/中/重） ②WHEAT 买 8u→两笔 6-25u ③step1 追加一拍
  SELL+BUY churn（净 0，恒 5/5）。
  约束（S3 教训 groove=step2 净麦恰 −5，v9 注释 net +5=净进 5 麦口径）：
  step2 净麦 = ΣSELL − ΣBUY_PRODUCT(WHEAT)（step0..2 累计，种子腿不计）：
    base 3−8=−5；t_lite 15−20=−5；t_mid 26−31=−5（两档保 groove）；
    t_heavy 50−50=0 → 破约束偏 +5，标注后单独测（修回形=买 27/28 或卖 45 档，留档未取）。

产物 orderbook_tape1_lab/build/<variant>/（h1x_t_lite/h1x_t_mid/h1x_t_heavy/
s8_t_lite/s8_t_mid/s8_t_heavy）：main.py+submission.tar.gz+build_manifest.json。
门（fail-closed 不产出）：①compile_ok ②last_callable_is_entry
③surgery_scope_ok（=基座逐字前缀+唯一手术块替换，零字节旁逸）④params_ok（量值门）
⑤groove_ok（净麦值=声明值）⑥确定性双跑（main/tar sha 同）⑦三成员合规包序。
只写 orderbook_tape1_lab/。不提交/不发射/不在线。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
H1X_MAIN = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
H1X_TAR = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "submission.tar.gz"
S8_MAIN = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
S8_TAR = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "submission.tar.gz"
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_tape1_manifest/1.0"
H1X_SHA = ("9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f9638"
           "97d9e9e6")
S8_SHA = ("a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae0"
          "4e7c0a6")

# ---- 三档参数（①首卖三档 ②两笔买 6-25u ③churn 净0）----
VARIANTS = {
    "t_lite": {"tier": "轻", "sell": 15, "buys": [10, 10], "churn": 5},
    "t_mid": {"tier": "中", "sell": 26, "buys": [15, 16], "churn": 5},
    "t_heavy": {"tier": "重", "sell": 50, "buys": [25, 25], "churn": 5},
}
BASE_OPEN = {"sell": 3, "buys": [8], "churn": 0}
GROOVE = -5  # S3 教训：step2 净麦恰 −5（sold−bought，净进 5 麦）

# ---- 手术块（H1X 与 S8 两基座该段逐字节同源，单块替换）----
OLD_BLOCK = '''V9_OPENING_STEP0 = (("BUY_PRODUCT", "WHEAT", 8), ("SELL", "WHEAT", 3))
_OPENING_LIQUIDITY_PARENT = rescue_agent
_OPENING_LIQUIDITY_REPORT = {'opening_calls': 0, 'opening_stock_ok': 0}

def opening_liquidity_agent(observation, configuration=None):
    action = _OPENING_LIQUIDITY_PARENT(observation, configuration)
    if int(observation['step']) == 0:
        _OPENING_LIQUIDITY_REPORT['opening_calls'] += 1
        orders = action.get('market', [])
        _OPENING_LIQUIDITY_REPORT['opening_stock_ok'] += int(
            orders[:2] == [['BUY_PRODUCT', 'WHEAT', 8], ['SELL', 'WHEAT', 3]]
            and orders[2:] == [['BUY_SEED', 'WHEAT', 1]])
    _OPENING_LIQUIDITY_REPORT['parent'] = dict(_R2_REPORT)
    return action

opening_liquidity_agent.telemetry = _OPENING_LIQUIDITY_REPORT'''

NEW_BLOCK_TPL = '''V9_OPENING_STEP0 = (("BUY_PRODUCT", "WHEAT", %(b0)d), ("BUY_PRODUCT", "WHEAT", %(b1)d), ("SELL", "WHEAT", %(sell)d))  # tape1 变体：做市单加重（band 带内台阶一复刻）
_OPENING_LIQUIDITY_PARENT = rescue_agent
_OPENING_LIQUIDITY_REPORT = {'opening_calls': 0, 'opening_stock_ok': 0, 'churn_applied': 0}

def opening_liquidity_agent(observation, configuration=None):
    action = _OPENING_LIQUIDITY_PARENT(observation, configuration)
    _step = int(observation['step'])
    if _step == 0:
        _OPENING_LIQUIDITY_REPORT['opening_calls'] += 1
        orders = action.get('market', [])
        _OPENING_LIQUIDITY_REPORT['opening_stock_ok'] += int(
            orders[:3] == [['BUY_PRODUCT', 'WHEAT', %(b0)d], ['BUY_PRODUCT', 'WHEAT', %(b1)d], ['SELL', 'WHEAT', %(sell)d]]
            and orders[3:] == [['BUY_SEED', 'WHEAT', 1]])
    elif _step == 1:
        _market = list(action.get('market') or [])
        action = dict(action, market=[['BUY_PRODUCT', 'WHEAT', %(churn)d], ['SELL', 'WHEAT', %(churn)d]] + _market)
        _OPENING_LIQUIDITY_REPORT['churn_applied'] += 1
    _OPENING_LIQUIDITY_REPORT['parent'] = dict(_R2_REPORT)
    return action

opening_liquidity_agent.telemetry = _OPENING_LIQUIDITY_REPORT'''


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _new_block(variant):
    p = dict(VARIANTS[variant])
    p["b0"], p["b1"] = p["buys"]
    return NEW_BLOCK_TPL % p


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


ADOPT_TAR = KSIM_DIR / "orderbook_haodou_adopt" / "submission.tar.gz"
S8_NOTE = '''

----
S8 base build, 2026-09-30 (orderbook_s8spike_lab/build/s8/main.py, SHA-256
a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae04e7c0a6):
public derivative of the haodou092 V82 kernel (Apache-2.0) composite v2:
order hygiene, wool defense, window focus, drop-half, fertilizer split,
state hardening, small-lot form, spike capture (八层修改署名), entry
_s8_agent. See the S8 build manifest for the layer-by-layer attribution.
'''


def _pack_members(base_tar, form):
    """合规包成员：基座三成员包优先；缺 LICENSE/NOTICE 时回退 haodou_adopt 原包。"""
    try:
        lic = _read_pack_member(base_tar, "LICENSE.txt")
        notice = _read_pack_member(base_tar, "NOTICE.txt").decode("utf-8")
        return lic, notice
    except KeyError:
        lic = _read_pack_member(ADOPT_TAR, "LICENSE.txt")
        notice = _read_pack_member(ADOPT_TAR, "NOTICE.txt").decode("utf-8")
        if form == "s8":
            notice += S8_NOTE
        return lic, notice


NOTICE_TAPE1_TPL = '''


----
tape1 build, 2026-10-01. Day-0 market-making tape surgery (analysis-50
band-deepcut step-1 replication) on the byte base above:
step-0 wheat orders BUY 8 / SELL 3 -> BUY %(b0)d + BUY %(b1)d (two 6-25u lots) /
SELL %(sell)d (first sell tier %(tier)s); step-1 prepended BUY_PRODUCT %(churn)d
+ SELL %(churn)d churn pair (net 0 wheat; buy-first leg order mirrors the
day-0 wash form and survives the s730 dead-order compaction layer, which
otherwise clips a stock-less SELL - observed in a heavy-tier probe). S3
groove accounting: step2
net wheat (sold-bought, product only) = %(net)d (base -5; %(groove_state)s).
Sold-buy legs carry no quantity outside the observed same-strategy band
(6-25u buys / 15-50u first sell). No other bytes changed
(surgery_scope gate). Test-only build; not submitted.
'''


def build_once(base_path, base_sha_expect, variant, form):
    """单次构建（字节级）→ (out_bytes, tar_bytes, checks, meta)。"""
    base_bytes = base_path.read_bytes()
    base_sha = _sha(base_bytes)
    if base_sha != base_sha_expect:
        raise RuntimeError("校验⓪红：%s 基座 sha %s ≠ 预期 %s"
                           % (form, base_sha[:16], base_sha_expect[:16]))
    src = base_bytes.decode("utf-8")
    if src.count(OLD_BLOCK) != 1:
        raise RuntimeError("校验红：手术块出现 %d 次（须恰 1）"
                           % src.count(OLD_BLOCK))
    built = src.replace(OLD_BLOCK, _new_block(variant))

    checks = {}
    compile(built, "tape1_main.py", "exec")                    # ①
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "tape1_main.py", "exec"), ns)          # ②
    entries = [v for v in ns.values() if callable(v)]
    want_entry = "_h1x_agent" if form == "h1x" else "_s8_agent"
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == want_entry)
    p = VARIANTS[variant]
    # ③手术域门：差异只落 OLD_BLOCK 域（逐字前缀+后缀恒等）
    i = src.find(OLD_BLOCK)
    checks["surgery_scope_ok"] = (
        built[:i] == src[:i]
        and built[i + len(_new_block(variant)):] == src[i + len(OLD_BLOCK):])
    # ④量值门（构建件内参数即声明值）
    m = re.search(r'V9_OPENING_STEP0 = \(\("BUY_PRODUCT", "WHEAT", (\d+)\), '
                  r'\("BUY_PRODUCT", "WHEAT", (\d+)\), '
                  r'\("SELL", "WHEAT", (\d+)\)\)', built)
    checks["params_ok"] = bool(m) and [int(m.group(1)), int(m.group(2))] == \
        p["buys"] and int(m.group(3)) == p["sell"] and \
        ("[['BUY_PRODUCT', 'WHEAT', %d], ['SELL', 'WHEAT', %d]]"
         % (p["churn"], p["churn"])) in built
    # ⑤groove 门：净麦值=声明值
    net = p["sell"] - sum(p["buys"])
    checks["groove_ok"] = (net == {"t_lite": -5, "t_mid": -5,
                                   "t_heavy": 0}[variant])
    if not all(checks.values()):
        raise RuntimeError("校验红 fail-closed: %s" % checks)

    out_bytes = built.encode("utf-8")
    base_tar = H1X_TAR if form == "h1x" else S8_TAR
    lic, notice = _pack_members(base_tar, form)
    notice += (NOTICE_TAPE1_TPL % {"b0": p["buys"][0], "b1": p["buys"][1],
                             "sell": p["sell"], "tier": p["tier"],
                             "churn": p["churn"], "net": net,
                             "groove_state": ("groove 保持" if net == GROOVE
                                              else "破约束（偏 %+d），标注单独测"
                                              % (net - GROOVE))})
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))
    meta = {"base_sha": base_sha, "net_step2": net}
    return out_bytes, tar_bytes, checks, meta


def build_variant(form, variant):
    base_path = H1X_MAIN if form == "h1x" else S8_MAIN
    base_sha = H1X_SHA if form == "h1x" else S8_SHA
    out1, tar1, checks1, meta1 = build_once(base_path, base_sha, variant, form)
    out2, tar2, checks2, meta2 = build_once(base_path, base_sha, variant, form)
    det = {"main_sha_run1": _sha(out1), "main_sha_run2": _sha(out2),
           "tar_sha_run1": _sha(tar1), "tar_sha_run2": _sha(tar2)}
    det["deterministic_ok"] = (det["main_sha_run1"] == det["main_sha_run2"]
                               and det["tar_sha_run1"] == det["tar_sha_run2"]
                               and checks1 == checks2)
    if not det["deterministic_ok"]:
        raise RuntimeError("校验⑥红：确定性双跑不一致 %s" % det)
    checks_all = dict(checks1)
    checks_all["deterministic_double_run_ok"] = True

    out_dir = OUT_DIR / ("%s_%s" % (form, variant))
    out_dir.mkdir(parents=True, exist_ok=True)
    main_path = out_dir / "main.py"
    main_path.write_bytes(out1)
    (out_dir / "submission.tar.gz").write_bytes(tar1)
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tf:
        members = [m.name for m in tf.getmembers()]
    if members != ["LICENSE.txt", "NOTICE.txt", "main.py"]:
        raise RuntimeError("校验⑦红：三成员包成员序 %s" % members)

    p = VARIANTS[variant]
    manifest = {
        "schema": SCHEMA, "form": "%s_%s" % (form, variant),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composition": "day0 做市单加重磁带变体（分析50 P1 台阶一）挂 %s 基座"
                       "（sha %s…）" % (form.upper(), base_sha[:8]),
        "surgery": {
            "target": "V9_OPENING_STEP0（tape step0 麦单对）+ "
                      "opening_liquidity_agent（step1 churn 注入+口径断言）",
            "old_block_sha256": _sha(OLD_BLOCK.encode("utf-8")),
            "new_block_sha256": _sha(_new_block(variant).encode("utf-8")),
            "diff_scope": "单块替换，其余字节=基座逐字（surgery_scope_ok）"},
        "params": {"first_sell": p["sell"], "buy_lots": p["buys"],
                   "churn_step1": [["BUY_PRODUCT", "WHEAT", p["churn"]],
                                   ["SELL", "WHEAT", p["churn"]]],
                   "churn_net_wheat": 0,
                   "churn_leg_order": "BUY→SELL（保腿过 s730 死单压缩；与 day0 "
                                      "洗价形买撑卖同构）"},
        "groove": {"rule": "S3 教训：step2 净麦=ΣSELL−ΣBUY_PRODUCT(WHEAT) "
                           "（step0..2 累计，种子腿不计）恰 −5",
                   "base": {"sell": BASE_OPEN["sell"],
                            "buys": BASE_OPEN["buys"],
                            "net_step2": BASE_OPEN["sell"]
                            - sum(BASE_OPEN["buys"])},
                   "variant_net_step2": meta1["net_step2"],
                   "holds": meta1["net_step2"] == GROOVE,
                   "flag": None if meta1["net_step2"] == GROOVE else
                   "破约束（step2 净麦 %+d≠−5，偏 %+d）——按任务令标注后单独测"
                   % (meta1["net_step2"], meta1["net_step2"] - GROOVE)},
        "base": {"path": str(base_path), "sha256": meta1["base_sha"]},
        "main": {"path": str(main_path), "sha256": det["main_sha_run1"],
                 "bytes": len(out1)},
        "tar": {"path": str(out_dir / "submission.tar.gz"),
                "sha256": det["tar_sha_run1"], "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": "_h1x_agent" if form == "h1x" else "_s8_agent",
        "compliance": "Apache-2.0 三成员包（基座 NOTICE 全文继承+tape1 手术署名）",
        "checks": checks_all, "determinism": det,
        "commands": ["python3 orderbook_tape1_lab/build_tape1.py",
                     "python3 orderbook_tape1_lab/judge_tape1.py"],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for form in ("h1x", "s8"):
        for variant in VARIANTS:
            m = build_variant(form, variant)
            out["%s_%s" % (form, variant)] = {
                "main_sha256": m["main"]["sha256"],
                "tar_sha256": m["tar"]["sha256"],
                "groove": m["groove"], "checks": m["checks"]}
            print("BUILD %s_%s" % (form, variant), m["main"]["sha256"][:16],
                  "tar", m["tar"]["sha256"][:16],
                  "net_step2", m["groove"]["variant_net_step2"], flush=True)
    (EVID_DIR / "build_tape1.json").write_text(
        json.dumps({"tape1": out}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("CHECKS all-pass:", all(v["checks"]["deterministic_double_run_ok"]
                                  and v["checks"]["params_ok"]
                                  and v["checks"]["groove_ok"]
                                  for v in out.values()), flush=True)
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return out


if __name__ == "__main__":
    main()
