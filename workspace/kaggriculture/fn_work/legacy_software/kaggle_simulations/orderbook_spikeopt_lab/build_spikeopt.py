# -*- coding: utf-8 -*-
"""build_spikeopt（尖拍追加量参数优化 lab）：S8/H1X 尖拍层 lot 帽两档上调构建件。

H1X 线上体检（fn_docs/hybrid/results/2026-10-01-h1x-online-read.json，27 局）
定位参数问题：败局 115945260/115948784 尖价拍有货但追加量小（lot 2-4 小单帽
+10 槽帽下追加空间在高量竞速拍偏薄，capture_rate_qty 仅 0.51）。
本 lab 两档最小改动手术——**只动 lot 帽**（其余参数逐字不动，含 anti-幻影硬线/
10 槽帽/step≥712/加卖不挪卖）：
  - A 档：spike_append 的 _S8_LOT_MIN,_S8_LOT_MAX = 2,4 → 3,6
  - B 档：同手术 → 4,8
基座双轨：
  - s8a/s8b = orderbook_s8spike_lab/build/s8/main.py（sha a59208fe…）手术件
    （S8 上出机制层结论）；
  - h1x_a/h1x_b = orderbook_h1x_lab/build/h1x/main.py（sha 9d073fba…）同手术
    移植件（用户裁决 2026-10-01：胜者档以 H1X 为基础移植；尖拍尾块 machinery
    sha 19ae92bc… 与 S8 同源、手术点相同）。
产物 orderbook_spikeopt_lab/build/{s8a,s8b,h1x_a,h1x_b}/：main.py +
submission.tar.gz（三成员合规包 LICENSE.txt+NOTICE.txt+main.py，确定性打包
gzip mtime=0/tar mtime=0/uid=gid=0）+ build_manifest.json（sha 全链）。
门（fail-closed 不产出）：①compile_ok ②last_callable_is_entry
③base_sha_identity ④machinery_identity（尖拍机制块=19ae92bc… 与 S8 同源）
⑤single_line_diff（唯一差异=lot 行，difflib 逐行证）⑥host_capture
⑦params_ok（lot=本档；abs_lines/fg/slots/step_cap 逐字不动）⑧确定性双跑
main/tar sha 同 ⑨三成员序。只写 orderbook_spikeopt_lab/。不提交/不发射/不在线。
"""
from __future__ import annotations

import argparse
import difflib
import gzip
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_spikeopt_manifest/1.0"
ADOPT_TAR = KSIM_DIR / "orderbook_haodou_adopt" / "submission.tar.gz"

LOT_OLD = "_S8_LOT_MIN, _S8_LOT_MAX = 2, 4"
LOT_FMT = "_S8_LOT_MIN, _S8_LOT_MAX = %d, %d"
MACHINERY_FROM = "_S8_ITEMS_ABS = "
MACHINERY_SHA = ("19ae92bc86882e6eee176f0a136ab362d28d46b4942e47746eba8780"
                 "8ed0db20")     # S8/H1X 同源尖拍机制块

BASES = {
    "s8": dict(
        path=KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py",
        sha="a59208fe79985388a9a5790858b8bce52e0de530e9d2484d0eafbcae04e7c0a6",
        entry="_s8_agent", host="_sf_agent", host_var="_S8_HOST",
        mach_to="def _s8_agent(", notice_src="adopt",
        desc="S8 尖拍捕获+申报修复层构建件（s_append+尖拍尾块）"),
    "h1x": dict(
        path=KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py",
        sha="9d073fbaf4f5d74afcb51e861672e1f12d12dc71a7b640a6bc5f963897d9e9e6",
        entry="_h1x_agent", host="_hs_agent", host_var="_H1X_HOST",
        mach_to="def _h1x_agent(", notice_src="h1x",
        desc="H1X = H1 王座基座 + S8 尖拍尾块（machinery 与 S8 同源）"),
}
ARMS = {"a": (3, 6), "b": (4, 8)}
# 尖拍参数规范面（除 lot 外逐字不动）
PARAMS_CANON = {"abs_lines": {"WOOL": 144.0, "MILK": 124.0},
                "fg_items": ("WHEAT", "MELON"), "fg_window": (528, 552),
                "fg_quantile": 0.75, "fg_min_samples": 6,
                "max_slots": 10, "step_cap": 712}


def _machinery(text: str, mach_to: str) -> str:
    a = text.find(MACHINERY_FROM)
    b = text.find(mach_to)
    if a < 0 or b < 0 or b <= a:
        raise RuntimeError("机制块边界缺失 a=%s b=%s" % (a, b))
    return text[a:b]


def _read_tar_member(tar_bytes: bytes, name: str) -> bytes:
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        m = tf.extractfile(name)
        if m is None:
            raise RuntimeError("包内无 %s" % name)
        return m.read()


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


NOTICE_TMPL = '''


----
spikeopt build, 2026-10-01. Surgical lot-cap retune of the S8 spike-capture
layer (spike_append small-order lot band), motivated by the H1X online read
(fn_docs/hybrid/results/2026-10-01-h1x-online-read.json, 27 episodes):
losses 115945260 / 115948784 show spike-tick inventory with thin appended
volume (lot 2-4 cap + 10-slot cap), capture_rate_qty 0.51.

This artifact = %(base_desc)s
(SHA-256 %(base_sha)s, byte-identical except ONE line) with the single
change:
    %(lot_old)s   ->   %(lot_new)s
Everything else is byte-identical to the base: spike_detect / decl_topup /
anti_phantom (declared+appended <= projected sellable, hard line) / 10-slot
cap / step>=712 untouched / additive selling (no order-shifting) all
unchanged. Spike machinery block identity: SHA-256 %(machinery)s before
retune (shared with S8), post-retune %(machinery_new)s.

Provenance chain: upstream haodou092 kernel V82 (Apache-2.0) -> fourth
adoption 2026-09-29 -> s1form s_append -> S8 spike-capture layer
(a59208fe...) -> [H1X composition on H1 throne base 76b5f842...
(h1x variant)] -> spikeopt lot-cap retune A/B. Apache-2.0 terms preserved.
Built for offline pool testing only; NOT submitted online, NOT launched.
Entry: %(entry)s (official last-callable), host: %(host)s.
'''


def build_once(base_key: str, arm: str):
    """单次构建（字节级）→ (out_bytes, tar_bytes, checks, meta)。"""
    cfg = BASES[base_key]
    lot = ARMS[arm]
    base_path = Path(cfg["path"])
    base_bytes = base_path.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != cfg["sha"]:
        raise RuntimeError("校验⓪红：基座 sha %s ≠ 预期 %s"
                           % (base_sha, cfg["sha"]))
    base_text = base_bytes.decode("utf-8")

    checks = {}
    # ④机制块同源门（手术点=机制块内 lot 行）
    mach_before = _machinery(base_text, cfg["mach_to"])
    mach_sha = hashlib.sha256(mach_before.encode("utf-8")).hexdigest()
    checks["machinery_identity_ok"] = (mach_sha == MACHINERY_SHA)
    if not checks["machinery_identity_ok"]:
        raise RuntimeError("校验④红：机制块 sha %s ≠ 同源 %s"
                           % (mach_sha, MACHINERY_SHA))

    # ⑤单行手术门：唯一差异=lot 行
    if base_text.count(LOT_OLD) != 1:
        raise RuntimeError("校验⑤红：lot 行出现 %d 次 ≠ 1"
                           % base_text.count(LOT_OLD))
    lot_new = LOT_FMT % lot
    built = base_text.replace(LOT_OLD, lot_new)
    if built.count(lot_new) != 1 or built.replace(lot_new, LOT_OLD, 1) != \
            base_text:
        raise RuntimeError("校验⑤红：替换非单点手术")
    sm = difflib.SequenceMatcher(None, base_text.splitlines(),
                                 built.splitlines(), autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    checks["single_line_diff_ok"] = (
        len(ops) == 1 and ops[0][0] == "replace"
        and ops[0][2] - ops[0][1] == 1 and ops[0][4] - ops[0][3] == 1
        and base_text.splitlines()[ops[0][1]] == LOT_OLD
        and built.splitlines()[ops[0][3]] == lot_new)
    if not checks["single_line_diff_ok"]:
        raise RuntimeError("校验⑤红：diff 不是唯一 lot 行 %s" % (ops,))

    checks["compile_ok"] = True
    compile(built, "spikeopt_main.py", "exec")                  # ①
    ns = {}
    exec(compile(built, "spikeopt_main.py", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    checks["last_callable_is_entry"] = (
        getattr(entries[-1], "__name__", "") == cfg["entry"])   # ②
    if not checks["last_callable_is_entry"]:
        raise RuntimeError("校验②红：末 callable ≠ %s" % cfg["entry"])
    checks["host_capture_ok"] = (
        ns.get(cfg["host_var"]) is ns.get(cfg["host"]))         # ⑥
    if not checks["host_capture_ok"]:
        raise RuntimeError("校验⑥红：宿主捕获 ≠ %s" % cfg["host"])
    p = ns.get("_S8_PARAMS", {})
    ok_params = all(p.get(k) == v for k, v in PARAMS_CANON.items()) \
        and p.get("lot") == lot
    checks["params_ok"] = ok_params                             # ⑦
    if not ok_params:
        raise RuntimeError("校验⑦红：params %s" % p)

    out_bytes = built.encode("utf-8")
    checks["base_sha_identity_ok"] = (base_sha == cfg["sha"])    # ③
    mach_after = _machinery(built, cfg["mach_to"])
    mach_sha_new = hashlib.sha256(mach_after.encode("utf-8")).hexdigest()
    checks["machinery_single_line_ok"] = (
        mach_after.replace(lot_new, LOT_OLD, 1) == mach_before)

    # 三成员合规包
    if cfg["notice_src"] == "h1x":
        h1x_tar = (KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x"
                   / "submission.tar.gz").read_bytes()
        lic = _read_tar_member(h1x_tar, "LICENSE.txt")
        notice_base = _read_tar_member(h1x_tar, "NOTICE.txt").decode("utf-8")
    else:
        adopt_tar = ADOPT_TAR.read_bytes()
        lic = _read_tar_member(adopt_tar, "LICENSE.txt")
        notice_base = _read_tar_member(adopt_tar, "NOTICE.txt").decode("utf-8")
    notice = notice_base + NOTICE_TMPL % {
        "base_desc": cfg["desc"] + "（零改动字节前缀）",
        "base_sha": base_sha, "lot_old": LOT_OLD, "lot_new": lot_new,
        "machinery": mach_sha, "machinery_new": mach_sha_new,
        "entry": cfg["entry"], "host": cfg["host"]}
    tar_bytes = _make_tar3(out_bytes, lic, notice.encode("utf-8"))

    meta = dict(base_sha=base_sha, mach_sha=mach_sha, mach_sha_new=mach_sha_new,
                lot=lot, lot_new=lot_new, lic=lic, notice=notice)
    return out_bytes, tar_bytes, checks, meta


def build_arm(base_key: str, arm: str, form: str = None):
    """单臂构建：单跑 + ⑧确定性双跑 + ⑨三成员序门 + manifest 落盘。"""
    out_bytes, tar_bytes, checks, meta = build_once(base_key, arm)
    out2, tar2, checks2, meta2 = build_once(base_key, arm)      # ⑧
    det = {"main_sha_run1": hashlib.sha256(out_bytes).hexdigest(),
           "main_sha_run2": hashlib.sha256(out2).hexdigest(),
           "tar_sha_run1": hashlib.sha256(tar_bytes).hexdigest(),
           "tar_sha_run2": hashlib.sha256(tar2).hexdigest()}
    det["deterministic_ok"] = (det["main_sha_run1"] == det["main_sha_run2"]
                               and det["tar_sha_run1"] == det["tar_sha_run2"]
                               and checks == checks2
                               and meta["mach_sha_new"] == meta2["mach_sha_new"])
    if not det["deterministic_ok"]:
        raise RuntimeError("校验⑧红：确定性双跑不一致 %s" % det)
    checks_all = dict(checks)
    checks_all["base_sha_identity_ok"] = True
    checks_all["deterministic_double_run_ok"] = True
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        members = [m.name for m in tf.getmembers()]
    if members != ["LICENSE.txt", "NOTICE.txt", "main.py"]:     # ⑨
        raise RuntimeError("校验⑨红：三成员包成员序 %s" % members)
    checks_all["tar3_members_ok"] = True

    form = form or ("%s%s" % (base_key, arm))
    out_dir = MODULE_DIR / "build" / form
    out_dir.mkdir(parents=True, exist_ok=True)
    main_path = out_dir / "main.py"
    main_path.write_bytes(out_bytes)
    (out_dir / "submission.tar.gz").write_bytes(tar_bytes)
    manifest = {
        "schema": SCHEMA,
        "form": form,
        "base_key": base_key,
        "arm": arm,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "surgery": "spike_append lot 帽单行手术（其余逐字不动）："
                   "%s → %s" % (LOT_OLD, meta["lot_new"]),
        "base": {"path": str(BASES[base_key]["path"]),
                 "sha256": meta["base_sha"],
                 "desc": BASES[base_key]["desc"],
                 "entry": BASES[base_key]["entry"],
                 "host": BASES[base_key]["host"]},
        "spike_source": {"machinery_sha256_before": meta["mach_sha"],
                         "machinery_sha256_after": meta["mach_sha_new"],
                         "machinery_same_as_s8": meta["mach_sha"]
                         == MACHINERY_SHA,
                         "machinery": "spike_detect/spike_append/decl_topup/"
                                      "anti_phantom/conservation（除 lot 帽"
                                      "外参数原样）"},
        "main": {"path": str(main_path),
                 "sha256": det["main_sha_run1"],
                 "bytes": len(out_bytes)},
        "tar": {"path": str(out_dir / "submission.tar.gz"),
                "sha256": det["tar_sha_run1"], "members": members,
                "pack": "确定性 gzip mtime=0/tar mtime=0/uid=gid=0"},
        "entry": BASES[base_key]["entry"],
        "host_entry": BASES[base_key]["host"],
        "spike_params": {"abs_lines": {"WOOL": 144.0, "MILK": 124.0},
                         "fg_items": ["WHEAT", "MELON"],
                         "fg_window": [528, 552], "fg_quantile": 0.75,
                         "fg_min_samples": 6,
                         "lot": list(meta["lot"]),
                         "max_slots": 10, "step_cap": 712},
        "unchanged_params": ["anti_phantom=申报+追加≤投射可卖（硬线）",
                             "max_slots=10", "step_cap=712",
                             "加卖不挪卖（守恒）", "decl_topup 补至可卖上限",
                             "spike_detect 判定线（WOOL≥144/MILK≥124、果麦"
                             "d22 窗 0.75 分位）"],
        "compliance": "Apache-2.0 三成员包（LICENSE.txt+NOTICE.txt+main.py，"
                      "NOTICE 携本手术署名；h1x 件保留八层修改署名）",
        "checks": checks_all,
        "determinism": det,
        "commands": ["python3 orderbook_spikeopt_lab/build_spikeopt.py "
                     "--form %s" % form],
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--form", default="s8a,s8b",
                    help="s8a,s8b,h1x_a,h1x_b 逗号表")
    args = ap.parse_args()
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for form in args.form.split(","):
        form = form.strip()
        base_key, arm = form[:-1].rstrip("_"), form[-1]
        if base_key not in BASES or arm not in ARMS:
            raise SystemExit("未知 form: %s" % form)
        m = build_arm(base_key, arm, form)
        out[form] = {"sha256": m["main"]["sha256"],
                     "tar_sha256": m["tar"]["sha256"],
                     "lot": m["spike_params"]["lot"],
                     "checks": m["checks"]}
        print("BUILD %s main %s tar %s lot %s" % (
            form, m["main"]["sha256"][:16], m["tar"]["sha256"][:16],
            m["spike_params"]["lot"]), flush=True)
    (EVID_DIR / "build_spikeopt.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("BUILD OK %.1fs" % (time.perf_counter() - t0), flush=True)


if __name__ == "__main__":
    main()
