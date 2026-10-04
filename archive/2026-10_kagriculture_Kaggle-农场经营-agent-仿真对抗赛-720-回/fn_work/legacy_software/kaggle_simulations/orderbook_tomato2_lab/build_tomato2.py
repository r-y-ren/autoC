# -*- coding: utf-8 -*-
"""build_tomato2（T2 = H1X 基座 + TOMATO 微单滴灌层）：构建+五门+确定性打包。

T2 = orderbook_h1x_lab/build/h1x/main.py（sha 9d073fba…，零改动字节前缀）
+ TOMATO 微单滴灌尾块（machinery 自包含：滴灌判定/qty-1 粒度手术/价门/
  频率上限/防幻影/守恒/step≥712 零触碰）挂到 H1X host（_h1x_agent，
  arity-adaptive inspect.signature 调用=h1x/d27 layer-S 先例）。

滴灌语义（分析50 台阶二 red-blackbst 复刻；n=1 队观察性，方向性校准）：
  番茄=hinge 品（T=200/gain 8 凸价格曲线，tetsutani 实现价表 2.08×），整批
  出货自踩凸价；qty-1 微单滴灌=「不砸价不断供」极限形态。
  粒度手术口径：本拍番茄出货流 q→qty-1 微单（出货粒度），未出量留仓由宿主
  下拍自计划——总番茄出货计划不变（game-wide 守恒，E182 终局清算兜底）、只改
  粒度；层内零跨拍挪量/零账本/零排程（红线区分：R26 跨拍拆单排程 7 连负族）。
硬约束：①每拍订单槽 ≤10 帽 ②申报（滴灌单）≤投射可卖（防幻影，S8 先例）
  ③step≥712（E182 终局规划器窗）零触碰 ④价门 quote≥base(60) 不过→同对象
  零足迹（不冲量） ⑤频率上限 24 滴/日 ⑥异常回退原动作。

产物 orderbook_tomato2_lab/build/t2/：
  - main.py（H1X 逐字前缀 + 尾块；末 callable=_t2_agent）
  - submission.tar.gz（三成员合规包 LICENSE.txt+NOTICE.txt+main.py；
    九层修改署名；确定性打包 gzip mtime=0/tar mtime=0）
  - build_manifest.json（sha 全链）
门（fail-closed 不产出）：①compile_ok ②last_callable_is_entry
③base_prefix_identity+roundtrip_strip_identity ④host_capture
（_T2_HOST is _h1x_agent）⑤params_ok（滴灌参数门）⑥确定性双跑 main/tar sha 同。
只写 orderbook_tomato2_lab/。不提交/不发射/不在线。
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
BASE_MAIN = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
ADOPT_TAR = KSIM_DIR / "orderbook_haodou_adopt" / "submission.tar.gz"
OUT_DIR = MODULE_DIR / "build" / "t2"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_tomato2_manifest/1.0"
BASE_SHA = ("9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f9638"
            "97d9e9e6")
ENTRY_NAME = "_t2_agent"
HOST_NAME = "_h1x_agent"
SEPARATOR = "\n\n"
MACHINERY_FROM = "_T2_ITEM = "
MACHINERY_TO = "def _t2_agent("


# ==== T2 尾块（宿主捕获 + inspect.signature 元数自适应调用，h1x/d27 先例） ====
HEAD = r'''"""t2 tomato 微单滴灌实验尾块（T2=H1X 基座+滴灌层）。
构建底=orderbook_h1x_lab/build/h1x/main.py 零改动字节前缀（sha 9d073fba…）；
宿主=块首捕获之 H1X 末 callable（_h1x_agent）。纯同对象后处理，层内零跨拍挪量；
异常回退原动作。机制假设（分析50 台阶二，n=1 队观察性）：番茄=hinge 品
（T=200/gain 8 凸价格；tetsutani 实现价表 2.08×），整批出货自踩凸价曲线，
qty-1 微单滴灌=「不砸价不断供」极限形态。
语义：
- ①滴灌判定：本拍动作含 SELL TOMATO 正挂量卖单（番茄出货流），且价门
  quote≥base(60)（抛售门：不冲量，保护实现价），且当日滴灌预算未用尽
  （频率上限 24 滴/日）；
- ②qty-1 粒度手术：本拍番茄出货流收敛为 qty-1 微单（出货粒度 q→1），
  未出量留仓、交由宿主下拍自计划——总番茄出货计划不变（game-wide 守恒，
  E182 终局清算兜底）、只改粒度；层内零跨拍挪量/零账本/零排程（红线区分：
  R23/R26 跨拍卖时移动 7 连负族 vs 本层=S8/X1 同形态手术安全先例）；
- ③硬约束：每拍订单槽 ≤10 帽（滴灌单原位改写不增槽）；申报（滴灌单）≤
  投射可卖（防幻影，S8 先例）；多余番茄卖单置 0 保槽位（base 抑制层先例
  "A zero-quantity order keeps later market race slots intact"）；
- ④零足迹：无番茄卖单/价门不过/预算用尽→同对象返回；step≥712（E182 终局
  规划器窗）零触碰；异常回退原动作。
"""
import inspect as _t2_inspect

_T2_HOST = [v for v in list(globals().values()) if callable(v)][-1]
'''

MACHINERY = r'''_T2_ITEM = 'TOMATO'
_T2_BASE = 60.0
_T2_DROPLET = 1
_T2_DAY_CAP = 24
_T2_MAX_SLOTS = 10
_T2_STEP_CAP = 712
_T2_PARAMS = dict(form='tomato2_drip/1.0', item=_T2_ITEM, base=_T2_BASE,
                  droplet=_T2_DROPLET, day_cap=_T2_DAY_CAP,
                  max_slots=_T2_MAX_SLOTS, step_cap=_T2_STEP_CAP,
                  invariant='粒度手术（出货粒度 q→1）零跨拍挪量/零账本/零排程；'
                            '申报（滴灌单）≤投射可卖（anti-幻影）；价门 quote≥base；'
                            '24 滴/日；step≥712 零触碰；异常回退')
_T2_REPORT = dict(calls=0, changed_turns=0, errors=0, drip_ticks=0,
                  droplets=0, deferred_units=0, gate_skip=0, day_cap_skip=0,
                  phantom_clamp=0, step_cap_out=0, no_tomato_ticks=0,
                  per_day={})
_T2_STATE = {'day': -1, 'used': 0}


def _t2_reset():
    _T2_REPORT.update(calls=0, changed_turns=0, errors=0, drip_ticks=0,
                      droplets=0, deferred_units=0, gate_skip=0,
                      day_cap_skip=0, phantom_clamp=0, step_cap_out=0,
                      no_tomato_ticks=0)
    _T2_REPORT['per_day'] = {}
    _T2_STATE['day'] = -1
    _T2_STATE['used'] = 0


def _t2_qty(raw):
    """挂量解析：int/整值 float→int；bool/负/其余→None（保守不动）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw if raw >= 0 else None
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _t2_sellable(observation, action):
    """投射可卖（防幻影上限）：宿主 projected_shed 优先，回退 shed+手存。"""
    try:
        fn = globals().get('projected_shed')
        fv = globals().get('FarmView')
        if callable(fn) and fv is not None:
            stock = fn(action, fv(observation))
            return int(stock.get(_T2_ITEM, 0))
    except Exception:
        pass
    try:
        priv = (observation or {}).get('private') or {}
        shed = int((priv.get('shed') or {}).get(_T2_ITEM, 0))
        invs = sum(int(inv.get(_T2_ITEM, 0))
                   for inv in (priv.get('inventories') or []))
        return shed + invs
    except Exception:
        return None


def _t2_apply(observation, action):
    _T2_REPORT['calls'] += 1
    try:
        if not isinstance(action, dict):
            return action
        step = int((observation or {}).get('step', 0))
        if step >= _T2_STEP_CAP:
            _T2_REPORT['step_cap_out'] += 1
            return action                        # ④ E182 终局规划器窗零触碰
        market = action.get('market')
        if not isinstance(market, list) or not market:
            return action
        idxs, declared, unparsed = [], 0, False
        for i, entry in enumerate(market):
            if not isinstance(entry, (list, tuple)) or len(entry) < 2:
                continue
            if entry[0] != 'SELL' or entry[1] != _T2_ITEM or len(entry) < 3:
                continue
            q = _t2_qty(entry[2])
            if q is None:
                unparsed = True                  # 不确定挂量：保守不动
                break
            if q > 0:
                idxs.append(i)
                declared += q
        if unparsed:
            return action
        if declared <= 0:
            _T2_REPORT['no_tomato_ticks'] += 1
            return action                        # 非触发拍零足迹（同对象）
        # ①价门 quote≥base（抛售门：不冲量，保护实现价）
        try:
            prices = ((observation or {}).get('market') or {}).get('prices') \
                or {}
            quote = float(prices.get(_T2_ITEM))
        except (TypeError, ValueError):
            quote = None
        if quote is None or quote < _T2_BASE:
            _T2_REPORT['gate_skip'] += 1
            return action                        # 价门不过：零足迹
        # ⑤频率上限 24 滴/日
        day = step // 24
        if _T2_STATE['day'] != day:
            _T2_STATE['day'] = day
            _T2_STATE['used'] = 0
        budget = _T2_DAY_CAP - _T2_STATE['used']
        if budget <= 0:
            _T2_REPORT['day_cap_skip'] += 1
            return action
        # ②qty-1 粒度手术：本拍出货粒度 q→1 微单（未出量留仓，宿主再计划）
        k = min(_T2_DROPLET, budget, declared)
        # ③防幻影：申报（滴灌单）≤投射可卖
        avail = _t2_sellable(observation, action)
        if avail is not None and k > avail:
            _T2_REPORT['phantom_clamp'] += 1
            k = min(k, max(0, avail))
        if k <= 0:
            return action
        out = list(market)
        first = True
        for i in idxs:
            ent = list(out[i])
            if first:
                ent[2] = int(k)                  # qty-1 滴灌微单（原位改写不增槽）
                first = False
            else:
                ent[2] = 0                       # 多余番茄卖单置 0 保槽位
            out[i] = ent
        if len(out) > _T2_MAX_SLOTS:             # 槽位帽（原位改写下不触发）
            return action
        _T2_STATE['used'] += k
        _T2_REPORT['changed_turns'] += 1
        _T2_REPORT['drip_ticks'] += 1
        _T2_REPORT['droplets'] += k
        _T2_REPORT['deferred_units'] += declared - k
        row = _T2_REPORT['per_day'].setdefault(
            str(day), dict(droplets=0, deferred=0))
        row['droplets'] += k
        row['deferred'] += declared - k
        return dict(action, market=out)
    except Exception:
        _T2_REPORT['errors'] += 1
        return action                            # ④异常回退（同对象零足迹）
'''

ENTRY = r'''def _t2_agent(observation, configuration=None):
    """t2 滴灌入口（官方 last-callable）：H1X 宿主动作→滴灌层后处理。
    元数自适应宿主调用：inspect.signature().bind 只探不调定形态（h1x/d27
    layer-S 先例；元数不可判→2 参先例形态）；宿主 _h1x_agent 双形态兼容。"""
    if int((observation or {}).get('step', 0)) == 0:
        _t2_reset()
    _host_form2 = True
    try:
        _sig = _t2_inspect.signature(_T2_HOST)
        try:
            _sig.bind(observation, configuration)
        except TypeError:
            _sig.bind(observation)          # 1 参形态
            _host_form2 = False
    except Exception:
        _host_form2 = True                  # 元数不可判→2 参先例形态
    if _host_form2:
        action = _T2_HOST(observation, configuration)
    else:
        action = _T2_HOST(observation)
    return _t2_apply(observation, action)


_t2_agent.telemetry = _T2_REPORT
kaggle_submission_agent = _t2_agent
'''

# 九层修改署名（NOTICE.txt 尾段）
NOTICE_T2 = '''


----
T2 build, 2026-10-01. Composition: orderbook_h1x_lab/build/h1x/main.py
(SHA-256 9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f963897d9e9e6,
byte-identical prefix, entry _h1x_agent) + tomato micro-drip tail block
(machinery self-contained), rehosted on the H1X host _h1x_agent with
arity-adaptive inspect.signature calling (h1x/d27 layer-S precedent);
entry _t2_agent.

Nine-layer modification attribution (九层修改署名; layers 1-8 = the H1X
NOTICE block above, unchanged):
1. Upstream haodou092 kernel V82 public engine (Metav4 production and market
   controller), Apache-2.0, including the upstream local V82 edit (revealed
   PET_CAFE temporarily changes _CA_MARGIN from -15 to -22, days 10-23).
2. Fourth adoption 2026-09-29 (verbatim, main.py SHA-256 bdb82117...).
3. X1 = d27 lot-wall hygiene layer (same-tick dead-order cleanup / over-shed
   clamp / per-item fragment merge to earliest slot; zero cross-tick moves),
   from orderbook_strongest_lab/layer_x1.py.
4. H1 composite assembly (orderbook_strongest_lab/build/h1, 76b5f842...) =
   H + X1, entry _hs_agent.
5. spike_detect (S8): absolute lines WOOL>=144 / MILK>=124; WHEAT/MELON d22
   window step in [528,552) with quote >= same-day 0.75 quantile (min 6).
6. spike_append: spike-tick appended small lots (lot 2-4, single order <=4,
   slot cap 10) up to projected sellable cap.
7. decl_topup + anti_phantom (S8): same-tick declaration top-up to sellable
   cap; total declared+appended <= projected sellable (never oversell).
8. conservation + H1X composition: additive selling, zero footprint on
   non-trigger ticks, exception fallback, step>=712 untouched; spike tail
   rehosted on H1 host (entry _h1x_agent).
9. tomato micro-drip layer (T2, this build): when the host action carries a
   positive-quantity SELL TOMATO order and quote >= base (60, the TOMATO
   market-param base; dump gate - never push volume below base), the tick's
   tomato outflow granularity is re-cut to a qty-1 micro order (form surgery:
   the extra tomato sell orders become zero-quantity slot placeholders per the
   base suppression-layer precedent); unsold units stay in the shed and are
   re-planned by the host itself next tick - the game-wide tomato outflow plan
   is conserved (only granularity changes), with zero cross-tick moves, zero
   ledger and zero rescheduling inside the layer (red-line family: R23/R26
   cross-tick sell-time moves 7 straight losses; this layer follows the S8/X1
   same-form surgery precedent). Rate cap 24 droplets/day; order slots <= 10
   (in-place rewrite adds no slots); declared droplet <= projected sellable
   (anti-phantom, S8 precedent); step >= 712 (E182 endgame window) untouched;
   non-trigger ticks same-object return; exception falls back to the host
   action. Mechanism hypothesis (analysis 50 step-2, redblackbst n=1 band,
   directional only): TOMATO is a hinge good (T=200, hinge gain 8; tetsutani
   realised-price table 2.08x base) whose convex scarcity curve self-crashes
   under batch outflow; the qty-1 drip is the limiting form of "don't crash
   the price, don't break supply".
'''


def _build_tail():
    """T2 尾块 = 头（宿主捕获+inspect 导入）+ 滴灌机制块 + t2 入口。"""
    return HEAD + MACHINERY + ENTRY


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
    """单次构建（字节级）→ (out_bytes, tar_bytes, checks, mach_sha)。"""
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA:
        raise RuntimeError("校验⓪红：H1X 基座 sha %s ≠ 预期 %s"
                           % (base_sha, BASE_SHA))
    tail = _build_tail()
    built = base_bytes.decode("utf-8") + SEPARATOR + tail

    checks = {}
    compile(built, "t2_main.py", "exec")                 # ①compile_ok
    checks["compile_ok"] = True
    ns = {}
    exec(compile(built, "t2_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == ENTRY_NAME)   # ②
    out_bytes = built.encode("utf-8")
    checks["base_prefix_identity_ok"] = \
        out_bytes[:len(base_bytes)] == base_bytes             # ③a
    checks["roundtrip_strip_identity_ok"] = (
        out_bytes[len(base_bytes):] == (SEPARATOR + tail).encode("utf-8"))  # ③b
    checks["host_capture_is_h1x_agent"] = (
        ns.get("_T2_HOST") is ns.get(HOST_NAME))              # ④
    p = ns.get("_T2_PARAMS", {})
    checks["params_ok"] = (                            # ⑤滴灌参数门
        p.get("item") == "TOMATO"
        and p.get("base") == 60.0
        and p.get("droplet") == 1
        and p.get("day_cap") == 24
        and p.get("max_slots") == 10
        and p.get("step_cap") == 712)
    if not all(checks.values()):
        raise RuntimeError("校验红 fail-closed: %s" % checks)

    lic = _read_adopt_member("LICENSE.txt")
    notice = _read_adopt_member("NOTICE.txt").decode("utf-8") + NOTICE_T2
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))
    mach_sha = hashlib.sha256(MACHINERY.encode("utf-8")).hexdigest()
    return out_bytes, tar_bytes, checks, mach_sha, base_sha, len(base_bytes)


def build_tomato2():
    out_bytes, tar_bytes, checks, mach_sha, base_sha, base_len = build_once()
    # ⑥确定性双跑：main/tar sha 同
    out2, tar2, checks2, mach2, _, _ = build_once()
    det = {"main_sha_run1": hashlib.sha256(out_bytes).hexdigest(),
           "main_sha_run2": hashlib.sha256(out2).hexdigest(),
           "tar_sha_run1": hashlib.sha256(tar_bytes).hexdigest(),
           "tar_sha_run2": hashlib.sha256(tar2).hexdigest()}
    det["deterministic_ok"] = (det["main_sha_run1"] == det["main_sha_run2"]
                               and det["tar_sha_run1"] == det["tar_sha_run2"]
                               and checks == checks2 and mach_sha == mach2)
    if not det["deterministic_ok"]:
        raise RuntimeError("校验⑥红：确定性双跑 sha 不一致 %s" % det)
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
        "form": "t2",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "composition": "T2 = H1X(9d073fba…) + TOMATO 微单滴灌尾块（machinery "
                       "自包含）挂 _h1x_agent（inspect.signature 元数自适应）",
        "base": {"path": str(BASE_MAIN), "sha256": base_sha,
                 "bytes": base_len, "entry": HOST_NAME},
        "drip_machinery": {"machinery_sha256": mach_sha,
                           "machinery": "drip_gate/qty1_granularity/anti_"
                                        "phantom/conservation/step_cap"
                                        "（自包含）"},
        "main": {"path": str(main_path), "sha256": main_sha,
                 "bytes": len(out_bytes),
                 "injected_tail_bytes": len(out_bytes) - base_len},
        "tar": {"path": str(OUT_DIR / "submission.tar.gz"),
                "sha256": tar_sha, "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": ENTRY_NAME,
        "host_entry": HOST_NAME,
        "drip_params": {"item": "TOMATO", "base": 60.0, "droplet": 1,
                        "day_cap": 24, "max_slots": 10, "step_cap": 712,
                        "gate": "quote≥base(60) 不过零足迹（不冲量）",
                        "conservation": "粒度手术 q→1；未出量留仓宿主再计划；"
                                        "game-wide 守恒只改粒度；零跨拍挪量"},
        "compliance": "Apache-2.0 三成员包（九层修改署名）",
        "checks": checks_all,
        "determinism": det,
        "commands": ["python3 orderbook_tomato2_lab/build_tomato2.py",
                     "python3 orderbook_tomato2_lab/judge_tomato2.py"],
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    m = build_tomato2()
    (EVID_DIR / "build_tomato2.json").write_text(
        json.dumps({"t2": {"sha256": m["main"]["sha256"],
                           "tar_sha256": m["tar"]["sha256"],
                           "checks": m["checks"]}},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD t2", m["main"]["sha256"][:16], "tar",
          m["tar"]["sha256"][:16], flush=True)
    print("CHECKS", m["checks"], flush=True)
    print("BUILD OK %.1fs" % (time.perf_counter() - t0))
    return m


if __name__ == "__main__":
    main()
