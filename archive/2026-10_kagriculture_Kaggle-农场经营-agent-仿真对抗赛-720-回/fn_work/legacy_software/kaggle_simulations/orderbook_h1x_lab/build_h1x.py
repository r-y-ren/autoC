# -*- coding: utf-8 -*-
"""build_h1x（H1X = H1 王座基座 + S8 尖拍捕获层）：构建+五门+确定性打包。

H1X = orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…，零改动字节前缀）
+ S8 尖拍捕获尾块（机制自 orderbook_s8spike_lab/build/s8/main.py 尾部提取，
  sha a59208fe…；spike_detect/spike_append/decl_topup/anti_phantom/conservation
  五机制参数原样：WOOL≥144/MILK≥124 绝对线、WHEAT/MELON d22 窗 [528,552) ≥当日
  0.75 分位（样本≥6）、lot 2-4、申报补至可卖上限、防幻影封顶、加卖不挪卖、
  step≥712 零触碰）挂到 H1 host（_hs_agent，arity-adaptive inspect.signature
  调用=d27 layer-S 先例）。

产物 orderbook_h1x_lab/build/h1x/：
  - main.py（H1 逐字前缀 + 尾块；末 callable=_h1x_agent）
  - submission.tar.gz（三成员合规包 LICENSE.txt+NOTICE.txt+main.py；
    八层修改署名；确定性打包 gzip mtime=0/tar mtime=0）
  - build_manifest.json（sha 全链）
门（fail-closed 不产出）：①compile_ok ②last_callable_is_entry
③base_prefix_identity（H1 前缀逐字节）④roundtrip_strip_identity
⑤host_capture（_H1X_HOST is _hs_agent）⑥params_ok（尖拍参数门）
⑦确定性双跑 main/tar sha 同。只写 orderbook_h1x_lab/。不提交/不发射/不在线。
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
BASE_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
S8_MAIN = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
ADOPT_TAR = KSIM_DIR / "orderbook_haodou_adopt" / "submission.tar.gz"
OUT_DIR = MODULE_DIR / "build" / "h1x"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_h1x_manifest/1.0"
BASE_SHA = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764974b"
            "22f337")
S8_SHA = ("a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae04"
          "e7c0a6")
ENTRY_NAME = "_h1x_agent"
HOST_NAME = "_hs_agent"
SEPARATOR = "\n\n"
S8_DOC_ANCHOR = '"""s8 尖拍捕获'
MACHINERY_FROM = "_S8_ITEMS_ABS = "
MACHINERY_TO = "def _s8_agent("
NOTICE_EIGHT_LAYERS = "八层修改署名"


# ==== H1X 尾块头（宿主捕获 + inspect.signature 元数自适应调用，d27 先例） ====
HEAD = r'''"""h1x 尖拍捕获实验尾块（H1X=H1 王座基座+尖拍层）。
构建底=orderbook_strongest_lab/build/h1/main.py 零改动字节前缀（sha 76b5f842…）；
尖拍机制块提取自 orderbook_s8spike_lab/build/s8/main.py 尾部（sha a59208fe…，
五机制参数原样）；宿主=块首捕获之 H1 末 callable（_hs_agent）。纯同拍后处理，
零跨拍挪量；异常回退原动作。
语义：
- ①尖拍判定：本步某品 quote ≥ 尖价线（分品绝对线沿 D8：WOOL≥144/MILK≥124；
  果麦 WHEAT/MELON d22 窗 step∈[528,552) ≥ 当日 0.75 分位，样本≥6 起判），
  且该品非"本轮已满申报"（本拍申报已达投射可卖上限则跳过）；
- ②尖拍补卖：尖价拍该品本拍无原生卖单→追加小单（lot 2-4、单≤4、槽位 10 帽内）
  至可卖库存上限（投射可卖−本拍已申报）；
- ③同拍申报修复：该品本拍有原生卖单→申报量补至可卖上限（只补申报不改时点）；
- ④anti-幻影：本拍申报+追加总量 ≤ 投射可卖（真实可卖），绝不超卖；
- ⑤守恒：同品累计成交可超原计划（加卖非挪卖，A 件日新高先例合法）；非触发拍
  零足迹（同对象返回）；异常回退原动作；step≥712（E182 终局规划器窗）零触碰。
"""
import inspect as _h1x_inspect

_H1X_HOST = [v for v in list(globals().values()) if callable(v)][-1]
'''

ENTRY = r'''def _h1x_agent(observation, configuration=None):
    """h1x 尖拍捕获入口（官方 last-callable）：H1 宿主动作→尖拍层后处理。
    元数自适应宿主调用：inspect.signature().bind 只探不调定形态（d27 layer-S
    先例；元数不可判→2 参先例形态）；宿主 _hs_agent 双形态兼容。"""
    if int((observation or {}).get('step', 0)) == 0:
        _s8_reset()
    _host_form2 = True
    try:
        _sig = _h1x_inspect.signature(_H1X_HOST)
        try:
            _sig.bind(observation, configuration)
        except TypeError:
            _sig.bind(observation)          # 1 参形态
            _host_form2 = False
    except Exception:
        _host_form2 = True                  # 元数不可判→2 参先例形态
    if _host_form2:
        action = _H1X_HOST(observation, configuration)
    else:
        action = _H1X_HOST(observation)
    return _s8_apply(observation, action)


_h1x_agent.telemetry = _S8_REPORT
kaggle_submission_agent = _h1x_agent
'''

# 八层修改署名（NOTICE.txt 尾段）
NOTICE_H1X = '''


----
H1X build, 2026-10-01. Composition: orderbook_strongest_lab/build/h1/main.py
(SHA-256 76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764974b22f337,
byte-identical prefix, entry _hs_agent) + spike-capture tail block extracted
verbatim-mechanism from orderbook_s8spike_lab/build/s8/main.py (SHA-256
a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae04e7c0a6), rehosted
on the H1 host _hs_agent with arity-adaptive inspect.signature calling
(d27 layer-S precedent); entry _h1x_agent.

Eight-layer modification attribution (八层修改署名):
1. Upstream haodou092 kernel V82 public engine (Metav4 production and market
   controller), Apache-2.0, including the upstream local V82 edit (revealed
   PET_CAFE temporarily changes _CA_MARGIN from -15 to -22, days 10-23).
2. Fourth adoption 2026-09-29 (verbatim, main.py SHA-256 bdb82117...).
3. X1 = d27 lot-wall hygiene layer (same-tick dead-order cleanup / over-shed
   clamp / per-item fragment merge to earliest slot; zero cross-tick moves),
   from orderbook_strongest_lab/layer_x1.py.
4. H1 composite assembly (orderbook_strongest_lab/build/h1, 76b5f842...) =
   H + X1, entry _hs_agent.
5. spike_detect: spike-tick detection - absolute lines WOOL>=144 / MILK>=124
   (D8 spike-band lower edge); WHEAT/MELON d22 window step in [528,552) with
   quote >= same-day 0.75 quantile (ceil rank, >=6 samples, includes current
   tick); fully-declared items skipped.
6. spike_append: spike-tick appended small lots (lot 2-4, single order <=4,
   slot cap 10) up to projected sellable cap when the item has no native sell
   order this tick.
7. decl_topup + anti_phantom: same-tick declaration top-up to sellable cap
   (declaration only, timing unchanged); total declared+appended <= projected
   sellable (never oversell; D8 phantom-declaration lesson).
8. conservation + H1X composition: additive selling (cumulative fills may
   exceed the original plan), zero footprint on non-trigger ticks (same-object
   return), exception fallback to original action, step>=712 untouched (E182
   endgame window); spike tail rehosted on H1 host _hs_agent (entry
   _h1x_agent, official last-callable semantics).

Mechanism parameters carried unchanged from the S8 block: absolute lines
WOOL>=144/MILK>=124; WHEAT/MELON window [528,552), same-day quantile 0.75,
min samples 6; lot 2-4; max slots 10; step cap 712.
'''


def _extract_s8_machinery(s8_text):
    """从 s8/main.py 尾部提取尖拍机制块（_S8_ITEMS_ABS..def _s8_agent 前）。"""
    if S8_DOC_ANCHOR not in s8_text:
        raise RuntimeError("S8 尾块锚点缺失")
    a = s8_text.find(MACHINERY_FROM)
    b = s8_text.find(MACHINERY_TO)
    if a < 0 or b < 0 or b <= a:
        raise RuntimeError("S8 机制块边界缺失 a=%s b=%s" % (a, b))
    return s8_text[a:b]


def _build_tail(s8_text):
    """H1X 尾块 = 头（宿主捕获+inspect 导入）+ S8 机制块原样 + h1x 入口。"""
    machinery = _extract_s8_machinery(s8_text)
    return HEAD + machinery + ENTRY


def _make_tar3(main_bytes, license_bytes, notice_bytes):
    """三成员合规包：确定性打包（gzip mtime=0、tar mtime=0/uid=gid=0）。"""
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


def _read_adopt_member(name):
    with tarfile.open(fileobj=io.BytesIO(ADOPT_TAR.read_bytes()),
                      mode="r:gz") as tf:
        member = tf.extractfile(name)
        if member is None:
            raise RuntimeError("haodou_adopt 包内无 %s" % name)
        return member.read()


def build_once():
    """单次构建（字节级）→ (out_bytes, tar_bytes, checks, machinery_sha)。"""
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA:
        raise RuntimeError("校验⓪红：H1 基座 sha %s ≠ 预期 %s"
                           % (base_sha, BASE_SHA))
    s8_text = S8_MAIN.read_text(encoding="utf-8")
    s8_sha = hashlib.sha256(S8_MAIN.read_bytes()).hexdigest()
    if s8_sha != S8_SHA:
        raise RuntimeError("校验⓪红：S8 件 sha %s ≠ 预期 %s" % (s8_sha, S8_SHA))
    tail = _build_tail(s8_text)
    built = base_bytes.decode("utf-8") + SEPARATOR + tail

    checks = {}
    compile(built, "h1x_main.py", "exec")                 # ①compile_ok
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "h1x_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)   # ②
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = \
        out_bytes[:len(base_bytes)] == base_bytes             # ③
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))  # ④
    checks["host_capture_is_hs_agent"] = (
        ns.get("_H1X_HOST") is ns.get(HOST_NAME))             # ⑤
    p = ns.get("_S8_PARAMS", {})
    checks["params_ok"] = (                            # ⑥尖拍参数门
        p.get("abs_lines") == {"WOOL": 144.0, "MILK": 124.0}
        and p.get("fg_items") == ("WHEAT", "MELON")
        and p.get("fg_window") == (528, 552)
        and p.get("fg_quantile") == 0.75
        and p.get("fg_min_samples") == 6
        and p.get("lot") == (2, 4)
        and p.get("max_slots") == 10
        and p.get("step_cap") == 712)
    if not all(checks.values()):
        raise RuntimeError("校验红 fail-closed: %s" % checks)

    lic = _read_adopt_member("LICENSE.txt")
    notice = _read_adopt_member("NOTICE.txt").decode("utf-8") + NOTICE_H1X
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))
    mach_sha = hashlib.sha256(
        _extract_s8_machinery(s8_text).encode("utf-8")).hexdigest()
    return out_bytes, tar_bytes, checks, mach_sha, base_sha, s8_sha, \
        len(base_bytes)


def build_h1x():
    out_bytes, tar_bytes, checks, mach_sha, base_sha, s8_sha, base_len = \
        build_once()
    # ⑦确定性双跑：main/tar sha 同
    out2, tar2, checks2, mach2, _, _, _ = build_once()
    det = {"main_sha_run1": hashlib.sha256(out_bytes).hexdigest(),
           "main_sha_run2": hashlib.sha256(out2).hexdigest(),
           "tar_sha_run1": hashlib.sha256(tar_bytes).hexdigest(),
           "tar_sha_run2": hashlib.sha256(tar2).hexdigest()}
    det["deterministic_ok"] = (det["main_sha_run1"] == det["main_sha_run2"]
                               and det["tar_sha_run1"] == det["tar_sha_run2"]
                               and checks == checks2 and mach_sha == mach2)
    if not det["deterministic_ok"]:
        raise RuntimeError("校验⑦红：确定性双跑 sha 不一致 %s" % det)
    checks_all = dict(checks)
    checks_all["deterministic_double_run_ok"] = True

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    main_path = OUT_DIR / "main.py"
    main_path.write_bytes(out_bytes)
    (OUT_DIR / "submission.tar.gz").write_bytes(tar_bytes)
    main_sha = det["main_sha_run1"]
    tar_sha = det["tar_sha_run1"]
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        members = [m.name for m in tf.getmembers()]
    if members != ["LICENSE.txt", "NOTICE.txt", "main.py"]:
        raise RuntimeError("校验红：三成员包成员序 %s" % members)

    manifest = {
        "schema": SCHEMA,
        "form": "h1x",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composition": "H1X = H1(76b5f842…) + S8 尖拍捕获尾块(a59208fe… 机制块"
                       "原样提取) 挂 _hs_agent（inspect.signature 元数自适应）",
        "base": {"path": str(BASE_MAIN), "sha256": base_sha,
                 "bytes": base_len, "entry": HOST_NAME},
        "spike_source": {"path": str(S8_MAIN), "sha256": s8_sha,
                         "machinery_sha256": mach_sha,
                         "machinery": "spike_detect/spike_append/decl_topup/"
                                      "anti_phantom/conservation（参数原样）"},
        "main": {"path": str(main_path), "sha256": main_sha,
                 "bytes": len(out_bytes),
                 "injected_tail_bytes": len(out_bytes) - base_len},
        "tar": {"path": str(OUT_DIR / "submission.tar.gz"),
                "sha256": tar_sha, "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": ENTRY_NAME,
        "host_entry": HOST_NAME,
        "spike_params": {"abs_lines": {"WOOL": 144.0, "MILK": 124.0},
                         "fg_items": ["WHEAT", "MELON"],
                         "fg_window": [528, 552], "fg_quantile": 0.75,
                         "fg_min_samples": 6, "lot": [2, 4],
                         "max_slots": 10, "step_cap": 712},
        "compliance": "Apache-2.0 三成员包（八层修改署名）",
        "checks": checks_all,
        "determinism": det,
        "commands": ["python3 orderbook_h1x_lab/build_h1x.py",
                     "python3 orderbook_h1x_lab/judge_h1x.py"],
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    m = build_h1x()
    (EVID_DIR / "build_h1x.json").write_text(
        json.dumps({"h1x": {"sha256": m["main"]["sha256"],
                            "tar_sha256": m["tar"]["sha256"],
                            "checks": m["checks"]}},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD h1x", m["main"]["sha256"][:16], "tar",
          m["tar"]["sha256"][:16], flush=True)
    print("CHECKS", m["checks"], flush=True)
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return m


if __name__ == "__main__":
    main()
