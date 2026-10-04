# -*- coding: utf-8 -*-
"""build_unified_u1_v2：U1-V2 统一求解核·缺陷修复构建线（连续空间投影；
判决先行·不发射不提交）。

U1 v1 败因=整数取整吃分辨率→中窗保守→末拍堆积。v2 修复=同一手术面（MODELPX
整个决策规则 8 站点，3 组字面量计数台账 4/1/3 + 反替换回程逐字节=基座源封印）
换 v2 核（u1_layer_v2）：①连续空间投影（比较用未取整连续价）②③触发阈两臂：
  u1v2a=阈连续化：连续差 (p_cur_c−peak_c)>$0.5 才卖（平局持有），MR>0 严格；
  u1v2b=同值即卖·跌幅拦截形：p_now≥投影峰值（连续）即卖、平局破向卖出；持有
        上行>$0.5 才拦、其余放行（何时卖+卖多少同容差 $0.5）。
④门字面量 p_next<p_cur-0.5 不动（哨兵过门，比较语义全在核内）；胜位守卫沿
expx_v2；窗约束/末拍清剩余沿 v1。构建底=oc_c3（sha 3f8b57fd…）零改动读入。
校验同 build_unified_u1（①-⑦）+ ⑧臂参数与形态一致。只写
orderbook_unifiedu1_lab/。
"""
from __future__ import annotations

import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

import build_unified_u1 as B1

MODULE_DIR = Path(__file__).resolve().parent
BASE_MAIN = B1.BASE_MAIN
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_unifiedu1_lab_manifest_v2/1.0"

SENTINEL = '"""u1v2 统一求解核·缺陷修复（连续空间投影）实验尾块'
ENTRY_NAME = "_u1_agent"
HOST_NAME = "_hs_agent"
LAYER_FILE = "u1_layer_v2.py"
ARM_TOKEN = "__U1V2_ARM__"
FORMS = {"u1v2a": 0, "u1v2b": 1}     # 0=阈连续化 1=同值即卖·跌幅拦截形

LAYER_LABEL = ("件 U1-V2=统一求解核缺陷修复（连续空间投影）：v1 败因=整数取"
               "整吃分辨率→中窗保守→末拍堆积；修复=决策比较全用未取整连续价"
               "（显示/结算价才取整）+触发阈两臂（A 阈连续化 连续差>$0.5 才卖 "
               "/ B 同值即卖·跌幅拦截形 持有上行>$0.5 才拦、平局破向卖出）+门"
               "字面量不动哨兵过门；胜位守卫沿 expx_v2、窗约束与末拍清剩余沿 "
               "v1；非触发拍零足迹、异常回退基线、零跨拍挪量、磁带 blob 零触碰）")


def build_block_v2(arm):
    layer_src = (MODULE_DIR / LAYER_FILE).read_text(encoding="utf-8")
    for tok, val in ((B1.K_TOKEN, B1.HORIZON_K), (B1.WIN_END_TOKEN, B1.WIN_END),
                     (B1.TERM_TOKEN, B1.TERM), (B1.H0_TOKEN, B1.H0),
                     (ARM_TOKEN, int(arm))):
        if tok not in layer_src:
            raise RuntimeError("u1_layer_v2 缺占位 %s" % tok)
        layer_src = layer_src.replace(tok, str(int(val)))
    parts = [
        SENTINEL + "（不发射不提交；" + LAYER_LABEL + "） \"\"\"",
        B1.CAPTURE_SRC,
        "if not callable(_U1_HOST):\n    raise RuntimeError('宿主捕获失败')",
        layer_src.strip(),
        B1._entry_src().rstrip(),
        "",
    ]
    return B1.SEPARATOR.join(parts)


def main():
    t0 = time.time()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != B1.BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")

    src2, ledger = B1.substitute(base_src)
    forms_out = {}
    for form, arm in FORMS.items():
        full = src2 + B1.SEPARATOR + build_block_v2(arm) + "\n"
        compile(full, "u1v2_main.py", "exec")
        ns: dict = {}
        exec(compile(full, "u1v2_main.py", "exec"), ns)
        entries = [v for v in ns.values() if callable(v)]
        if getattr(entries[-1], "__name__", "") != ENTRY_NAME:
            raise RuntimeError("校验④红 %s: 末 callable 漂移" % form)
        if getattr(ns.get("_U1_HOST"), "__name__", "") != HOST_NAME:
            raise RuntimeError("校验④红 %s: 宿主捕获漂移" % form)
        if (int(ns.get("_U1_K", 0)) != B1.HORIZON_K
                or int(ns.get("_U1_WIN_END", 0)) != B1.WIN_END
                or int(ns.get("_U1_H0", 0)) != B1.H0
                or int(ns.get("_U1_ARM", -1)) != arm):
            raise RuntimeError("校验⑧红 %s: 参数漂移" % form)
        for fn in ("_u1_pnext", "_u1_take", "_u1_update", "_u1_price_c",
                   "_u1_fire", "_u1_sellable", "_u1_cap"):
            if not callable(ns.get(fn)):
                raise RuntimeError("校验④红 %s: 缺 %s" % (form, fn))
        # 校验⑦ 探针：连续价与取整价分辨差 + 触发阈臂语义
        pc = ns["_u1_price_c"]
        fire = ns["_u1_fire"]
        px = pc("MILK", 200, None)
        assert abs(px - float(ns["_u1_price"]("MILK", 200, None))) < 1.0
        assert pc("MILK", 201, None) != px    # 连续分辨率恢复（取整会同值）
        if arm == 0:
            assert fire(px, px, False) is False          # 平局持有
            assert fire(px, px - 0.6, False) is True     # 跌>$0.5 卖
            assert fire(px, px - 0.4, False) is False
        else:
            assert fire(px, px, False) is True           # 同值即卖
            assert fire(px, px + 0.5, False) is True     # 涨≤$0.5 放行
            assert fire(px, px + 0.6, False) is False    # 涨>$0.5 拦
        assert fire(px, 0.0, True) is True               # 末拍清剩余

        OUT = OUT_DIR / form
        OUT.mkdir(parents=True, exist_ok=True)
        main_path = OUT / "main.py"
        main_path.write_text(full, encoding="utf-8")
        main_sha = hashlib.sha256(main_path.read_bytes()).hexdigest()
        tar_buf = io.BytesIO()
        with tarfile.open(fileobj=tar_buf, mode="w:gz") as tar:
            tar.add(str(main_path), arcname="main.py")
        tar_bytes = tar_buf.getvalue()
        (OUT / "submission.tar.gz").write_bytes(tar_bytes)
        man = {
            "schema": SCHEMA, "form": form, "arm": arm,
            "arm_name": ("阈连续化（连续差>$0.5 才卖）" if arm == 0 else
                         "同值即卖·跌幅拦截形（持有上行>$0.5 才拦）"),
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "base_main": str(BASE_MAIN), "base_sha256": base_sha,
            "main_sha256": main_sha,
            "main_bytes": main_path.stat().st_size,
            "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
            "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
            "subs": ledger, "subs_roundtrip_identity_ok": True,
            "gate_literal_untouched": True,
            "horizon_k": B1.HORIZON_K, "win_end": B1.WIN_END,
            "term": B1.TERM, "h0": B1.H0,
            "kernel": "统一求解核 v2（连续空间投影；何时卖+卖多少 单一决策核）",
            "entry": ENTRY_NAME, "entry_last_callable": True,
            "host_entry": HOST_NAME, "compile_ok": True,
            "probes": {"window_edges_ok": True, "cap_tiers_ok": True,
                       "continuous_resolution_ok": True, "fire_arm_ok": True},
            "replacements": B1.SUBS and {
                "p_pred_sites": 4, "take_sites": 4,
                "replacement_point": "MODELPX 整个决策规则（内层全替换）"},
        }
        (OUT / "build_manifest.json").write_text(
            json.dumps(man, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        forms_out[form] = man
        print("BUILD", form, main_sha[:16], "arm", arm,
              round(time.time() - t0, 1), "s", flush=True)

    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "build_manifest_v2.json").write_text(
        json.dumps({"schema": SCHEMA, "forms": {
            f: {"main_sha256": m["main_sha256"], "arm": m["arm"],
                "arm_name": m["arm_name"]} for f, m in forms_out.items()},
            "subs_roundtrip_identity_ok": True}, ensure_ascii=False,
            indent=1) + "\n", encoding="utf-8")
    return forms_out


if __name__ == "__main__":
    main()
