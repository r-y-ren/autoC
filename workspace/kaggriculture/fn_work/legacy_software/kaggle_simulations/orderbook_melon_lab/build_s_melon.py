# -*- coding: utf-8 -*-
"""build_s_melon（melon lab）：S4 复刻线独立形态 S_melon——prvsiyan 冠军件署名移植。

S_melon = prvsiyan_melons（doan Champion 真身，kernel
"kaggriculture-frontier-the-moon-counts-melons"，sha256 178ae0f7…）整件 Apache-2.0
署名移植：注释头署名 + 源逐字节保留（行为零改动）。三支柱（果品专精产线 /
前跑卖引 / step712-718 终局块重排）随件携带，不叠我方卖面哲学。

合规：Apache-2.0 允许署名移植；上游通知（thomastschinkel/yhay81/destbreso/
aurax7/tetsutani/Dmitrii Gluzdov/Ahmed Berat Ozer/haideptry 2965 谱系）随件
逐字保留；LICENSE 全文抽出于源头部另存 LICENSE-APACHE-2.0.txt；NOTICE.md 登记
署名口径。mooman 件无许可，未移植未引用（如需概念参考走干净室）。

产物 orderbook_melon_lab/build/s_melon/main.py + LICENSE + NOTICE。只写本 lab；
不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
SRC = Path("/tmp/arms_e/pkg/prvsiyan_melons/main.py")
OUT_DIR = MODULE_DIR / "build" / "s_melon"
EVID_DIR = MODULE_DIR / "evidence"
EXPECTED_SHA = "178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a"

HEADER = """# ==== S_melon（S4 复刻线·独立形态）：prvsiyan_melons 冠军件署名移植（Apache-2.0） ====
# Port attribution: original agent "prvsiyan_melons" by prvsiyan, Kaggle kernel
#   https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons
#   mirror https://github.com/doanthuan/kaggriculture/blob/main/agents/public/prvsiyan_melons.py
# Frozen discovery winner, byte-identical to the decoded kernel body
#   (sha256 178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a).
# Apache-2.0; all upstream notices (thomastschinkel, yhay81, destbreso, aurax7,
# tetsutani, prvsiyan, Dmitrii Gluzdov, Ahmed Berat Ozer V-sessions, haideptry
# 2965 master hybrid engine lineage) are retained verbatim below.
# Port date 2026-09-30 (kaggriculture campaign lab orderbook_melon_lab, S4).
# Port is behavior-preserving: this header is comments only.
# LICENSE archived at orderbook_melon_lab/LICENSE-APACHE-2.0.txt; see NOTICE.md.
# S_melon pillars (strategy identity):
#   (1) fruit-specialized production line: MELON/TOMATO tilt in the route tapes
#       plus its matching sell method (V219/V221B tomato limited investment,
#       melon-first mix);
#   (2) front-run / lead selling: FRONT_RUN_ITEMS (MILK/WOOL/STRAWBERRY/MELON)
#       next-step pre-sale (native _sell_lead/_front_run hooks) + EXP293 sale
#       advance (4-turn lookahead, mirror front-run) + sell-block compaction;
#   (3) endgame SELL-block reorder: _v44y_reorder re-applied at the tail
#       (FRO entry) + Shop0909 step 712-718 physical-closure terminal planner.
# Not stacked on our own sell-face philosophy (independent line, own tapes).
"""


def main() -> None:
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECTED_SHA:
        raise SystemExit("prvsiyan source sha mismatch: %s" % sha)
    text = raw.decode("utf-8")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    # LICENSE 全文：源头部 Apache-2.0 块（含 APPENDIX）逐字抽出。
    lines = text.splitlines(keepends=True)
    lic = []
    in_lic = False
    for ln in lines:
        if ln.startswith("#                                  Apache License"):
            in_lic = True
        if in_lic:
            lic.append(ln[2:] if ln.startswith("# ") or ln == "#\n" or ln == "#" else (ln[1:] if ln.startswith("#") else ln))
        if in_lic and "END OF TERMS AND CONDITIONS" in ln:
            break
    (MODULE_DIR / "LICENSE-APACHE-2.0.txt").write_text("".join(lic), encoding="utf-8")

    out = HEADER + text
    out_bytes = out.encode("utf-8")
    (OUT_DIR / "main.py").write_bytes(out_bytes)

    manifest = {
        "schema": "orderbook_melon_manifest/1.0",
        "arm": "s_melon",
        "form": "独立形态（prvsiyan_melons 整件署名移植）",
        "src": str(SRC),
        "src_sha256": sha,
        "src_bytes": len(raw),
        "out": str(OUT_DIR / "main.py"),
        "out_sha256": hashlib.sha256(out_bytes).hexdigest(),
        "out_bytes": len(out_bytes),
        "behavior_change": "none（注释头；源逐字节保留在头部之后）",
        "entry": "kaggle_submission_agent/_final_sell_block_reorder_entrypoint（末 callable 语义不变）",
        "license": "Apache-2.0（全文 LICENSE-APACHE-2.0.txt；上游通知随件保留）",
        "pillars": [
            "果品专精产线：MELON/TOMATO 权重拉高（route tapes 果品倾斜）+V219/V221B 番茄有限投资配套卖法",
            "前跑卖引：FRONT_RUN_ITEMS 四品 next-step 预卖（_sell_lead/_front_run 钩子）+EXP293 四拍 ADV 镜像前跑",
            "终局块重排：step712-718 Shop0909 物理闭合终局规划 + _v44y_reorder 尾部再应用（FRO）",
        ],
        "mooman_cleanroom": "mooman 件无许可，未移植未引用；概念如需参考走干净室（本次未用）",
    }
    (EVID_DIR / "s_melon_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("s_melon built:", manifest["out_sha256"][:16], manifest["out_bytes"], "bytes")


if __name__ == "__main__":
    main()
