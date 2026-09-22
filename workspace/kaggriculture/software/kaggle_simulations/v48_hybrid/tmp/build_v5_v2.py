# -*- coding: utf-8 -*-
# 【中文】build_v5_v2.py —— v5 v2 重建驱动（临时脚本，落 tmp/，R8-v2 F5）
# ===========================================================================
# 与 tmp/build_v5.py（F4b v1 驱动）同构：旗面不变 P1/P3 off、P2/P4 on
# （--p4 on --p1 off --p3 off）；差异仅产物文案对齐 R8-v2 触发面（双条件
# 并集 + 峰值运行寄存器）。核验链沿用 v1 驱动六步：
#   ① CLI 子进程构建 sha == 进程内 build_once；② 双跑 build_once / 双次
#   pack_tar 逐字节一致；③ 零接线：P1+P3 token 零出现、P2+P4 token 在场
#   （P4 token 集含 _V48H_P4_REGISTER）；④ P4-off 无扰动对照：v4b 旗面
#   重建 == v4b/ 包（含 tar）、P1-P3 全开（P4 off）== 根提交件；⑤ blob
#   身份：只内嵌 P2+P4 v2 源，与 patches/ 逐字节一致；⑥ 基底逐字前缀 +
#   tar 单成员回读。产物原地重建 v48_hybrid/v5/（战后资产，不上线）。
# ===========================================================================
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import zlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # v48_hybrid/
V5_DIR = os.path.join(HERE, "v5")

SUBMIT_MESSAGE_V5 = ("public derivative with economic-guard + "
                     "lead-protection layers (post-war build, not for "
                     "current competition)")

sys.dont_write_bytecode = True


def load_build_module():
    spec = importlib.util.spec_from_file_location(
        "v48h_build_mod_v5v2", os.path.join(HERE, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob_identity(main_bytes: bytes) -> dict:
    """v5 内嵌 blob 只含 P2+P4 源（P1/P3 模块零内嵌），源字节与 patches/ 一致。"""
    text = main_bytes.decode("utf-8")
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("_V48H_MODULES = "))
    chunk = []
    for ln in lines[start + 1:]:
        if ln.startswith("    '") and ln.rstrip().endswith("'"):
            chunk.append(ln.strip()[1:-1])
        elif ln == ")" and chunk:
            break
    if not chunk:
        return {"ok": False, "error": "blob block not found"}
    blob_text = "".join(chunk)
    modules = json.loads(zlib.decompress(
        base64.b85decode(blob_text)).decode("utf-8"))
    detail = {}
    for name, src in modules.items():
        src_file = next(m["source"] for m in _B.PATCHES.values()
                        if m["module"] == name)
        disk = open(os.path.join(HERE, "patches", src_file), "rb").read()
        detail[name] = {
            "source": f"patches/{src_file}",
            "embedded_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "disk_sha256": hashlib.sha256(disk).hexdigest(),
            "identical": src == disk.decode("utf-8"),
        }
    expect = ["v48h.lead_protection", "v48h.p2_economic_guard"]
    return {"ok": (all(v["identical"] for v in detail.values())
                   and sorted(modules) == expect),
            "embedded_modules": sorted(modules),
            "p1_module_absent": not any("p1_" in k for k in modules),
            "p3_module_absent": not any("p3_" in k for k in modules),
            "detail": detail}


def build_readme_v5(main_sha, main_bytes, tar_sha, tar_bytes,
                    patch_shas, patch_sizes) -> str:
    lines = []
    a = lines.append
    a("# v5 — v48 混合战后资产包（R8-v2 F5：经济保险 + 终局保果层 v2）")
    a("")
    a("> **public derivative with economic-guard + lead-protection layers "
      "(post-war build, not for current competition)**")
    a("")
    a("> 战后资产（R8-v2）：只构建 + 离线验证，不上线——零提交冻结 ba1b44c。"
      "旗面 `P1/P3 off、P2/P4 on`：在 v4b 形态（行为级≡纯 v48 + P2 死价"
      "保险）之上叠加 P4 终局保果层 v2——触发=双条件并集【day≥15 且峰回撤"
      " peak−lead≥2000 且 lead≥1500】∪【day≥24 且 lead≥3000】，峰值经运行"
      "峰寄存器跟踪（编排处持有 `_V48H_P4_REGISTER`，跨回合注入，补丁模块"
      "保持纯函数）；未触发形态零足迹=原对象返回。由 `python build.py "
      "--p4 on --p1 off --p3 off` 的装配函数经 `tmp/build_v5_v2.py` 确定性"
      "驱动生成。")
    a("")
    a("## 身份链（identity chain）")
    a("")
    a("| 件 | sha256 | 字节 |")
    a("|---|---|---|")
    a(f"| 基底 `../v48_derivative/main.py` | `{_B.BASE_SHA256}` | "
      f"{_B.BASE_BYTES_EXPECT} |")
    for key in _B.PATCH_ORDER:
        a(f"| {key} `patches/{_B.PATCHES[key]['source']}` | "
          f"`{patch_shas[key]}` | {patch_sizes[key]} |")
    a(f"| 混合 `main.py`（基底逐字前缀 + 追加块） | `{main_sha}` | "
      f"{main_bytes} |")
    a(f"| `submission.tar.gz`（单成员 main.py，确定性 tar） | `{tar_sha}` | "
      f"{tar_bytes} |")
    a("")
    a("P4-off 无扰动对照：同装配器以 v4b 旗面（P4 off）重建与 `../v4b/` 包"
      "逐字节一致（含 tar）；P1-P3 全开（P4 off）重建与根提交件 `../main.py` "
      "逐字节一致——旗面增量对既有构建零扰动（`build_manifest.json` 的 "
      "`p4_off_no_disturbance`）。")
    a("")
    a("## 接线与仲裁")
    a("")
    a("卖单面次序：P2 产线否决（死价 BUY/建棚→PASS）→ P4 "
      "`build_lead_protection(obs, day=step//24, market, "
      "register=_V48H_P4_REGISTER)`（P4 自带门栈：双条件并集触发——回撤臂 "
      "day≥15 且 peak−lead≥2000 且 lead≥1500 ∪ 原臂 day≥24 且 lead≥3000；"
      "保护时点 6/12/18；step≥717 清仓窗让位；透传现有卖单、仅分批前移补发，"
      "量帽 split_qty_cap=4/线数帽 4；未触发/异常=原对象零足迹）；P1/P3 零"
      "接线。基底五零改动区以前缀构造保持字节一致（`../audit_base.py` 分区"
      "审计）。")
    a("")
    a("## 提交（冻结：不提交）")
    a("")
    a("战后资产不进当前赛事（零提交冻结 ba1b44c）；描述文案留档："
      f"`{SUBMIT_MESSAGE_V5}`")
    a("")
    a("## 门禁结果（发射冒烟四门，tmp/fourgate_v5.py 回填）")
    a("")
    a("| 门 | 判据 | 结果 |")
    a("|---|---|---|")
    a("| gate1 官方装载语义 | 干净 -I 子进程 get_last_callable 复刻一致 | "
      "PENDING |")
    a("| gate2 双席自打 | seeds 101/102 双局 720 回合 DONE、每步 <1000ms | "
      "PENDING |")
    a("| gate3 确定性 | seed101 重跑动作流哈希逐字节一致 | PENDING |")
    a("| gate4 体积 | tar ≤ 100MB | PENDING |")
    a("")
    return "\n".join(lines) + "\n"


_B = None


def main() -> int:
    global _B
    _B = load_build_module()
    b = _B
    flags = {"P1": False, "P2": True, "P3": False, "P4": True}

    # ① CLI 子进程诊断构建（build.py --p4 on --p1 off --p3 off）
    proc = subprocess.run([sys.executable, os.path.join(HERE, "build.py"),
                           "--p4", "on", "--p1", "off", "--p3", "off"],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        print(proc.stdout[-800:], proc.stderr[-800:], sep="\n")
        raise SystemExit("build.py --p4 on --p1 off --p3 off failed")
    cli_info = json.loads(proc.stdout)
    cli_path = cli_info["diagnostic_build"]
    cli_sha = cli_info["sha256"]
    print(f"[cli] --p4 on --p1 off --p3 off -> {cli_path} sha256={cli_sha} "
          f"bytes={cli_info['bytes']} flags={cli_info['flags']}", flush=True)

    # ② 进程内双跑 build_once（与 CLI 同函数）
    main_v5 = b.build_once(flags)
    if main_v5 != b.build_once(flags):
        raise SystemExit("in-process build_once not deterministic")
    if b.sha256_bytes(main_v5) != cli_sha:
        raise SystemExit(f"cli vs in-process sha mismatch: {cli_sha} vs "
                         f"{b.sha256_bytes(main_v5)}")
    compile(main_v5, "main.py", "exec")

    # ③ 零接线（P1+P3 token 零在场；P2+P4 token 在场=接线真实；P4 token 集
    #    v2 增 _V48H_P4_REGISTER——寄存器接线亦须真实在场）
    v5_text = main_v5.decode("utf-8")
    all_on = open(os.path.join(HERE, "main.py"), "rb").read().decode("utf-8")
    wiring = {}
    for key in ("P1", "P2", "P3", "P4"):
        toks = b.PATCHES[key]["tokens"]
        hits = {t: v5_text.count(t) for t in toks}
        ok = (all(v == 0 for v in hits.values()) if key in ("P1", "P3")
              else all(v >= 1 for v in hits.values()))
        wiring[key] = {"v5_token_hits": hits, "ok": ok}
        print(f"[wiring] {key} ok={ok} v5_hits={hits}", flush=True)
    if not all(w["ok"] for w in wiring.values()):
        raise SystemExit("wiring verification failed")

    # ④ P4-off 无扰动对照（v4b 旗面 = v4b 包逐字节；全开旗面 = 根提交件）
    ctrl_v4b = b.build_once({"P1": False, "P2": True, "P3": False,
                             "P4": False})
    v4b_main = open(os.path.join(HERE, "v4b", "main.py"), "rb").read()
    v4b_tar = open(os.path.join(HERE, "v4b", "submission.tar.gz"),
                   "rb").read()
    ctrl_root = b.build_once({"P1": True, "P2": True, "P3": True,
                              "P4": False})
    root_main = open(os.path.join(HERE, "main.py"), "rb").read()
    no_dist = {
        "v4b_flags_p4_off_matches_v4b_main": ctrl_v4b == v4b_main,
        "v4b_flags_p4_off_tar_matches_v4b_tar":
            b.pack_tar(ctrl_v4b) == v4b_tar,
        "all_on_p123_p4_off_matches_root_main": ctrl_root == root_main,
    }
    print(json.dumps(no_dist), flush=True)
    if not all(no_dist.values()):
        raise SystemExit(f"P4-off no-disturbance control failed: {no_dist}")

    # ⑤ blob 身份（只内嵌 P2+P4 v2 源，源与 patches/ 逐字节一致）
    ident = blob_identity(main_v5)
    print(f"[blob] ok={ident['ok']} embedded={ident['embedded_modules']} "
          f"p1_absent={ident['p1_module_absent']} "
          f"p3_absent={ident['p3_module_absent']}", flush=True)
    if not ident["ok"]:
        raise SystemExit("blob identity verification failed")

    # ⑥ 基底逐字前缀 + 确定性打包 + tar 内容回读
    base = b.load_base()
    if not main_v5.startswith(base):
        raise SystemExit("v5 main.py is not a byte-verbatim base prefix")
    tar_bytes = b.pack_tar(main_v5)
    if b.pack_tar(b.build_once(flags)) != tar_bytes:
        raise SystemExit("tar packing not deterministic")
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
        names = t.getnames()
        inner = t.extractfile("main.py").read()
    if names != ["main.py"] or inner != main_v5:
        raise SystemExit("tar member/byte mismatch")

    # 产物落盘（v5/ 原地重建）
    os.makedirs(V5_DIR, exist_ok=True)
    with open(os.path.join(V5_DIR, "main.py"), "wb") as h:
        h.write(main_v5)
    with open(os.path.join(V5_DIR, "submission.tar.gz"), "wb") as h:
        h.write(tar_bytes)

    slug, _ = b.extract_slug()
    patch_shas, patch_sizes = {}, {}
    for key in b.PATCH_ORDER:
        raw = open(os.path.join(b.PATCH_DIR, b.PATCHES[key]["source"]),
                   "rb").read()
        patch_shas[key] = b.sha256_bytes(raw)
        patch_sizes[key] = len(raw)

    manifest = {
        "variant": {
            "name": "v5",
            "revision": "R8-v2 (F5, 2026-09-22)",
            "cli": "python build.py --p4 on --p1 off --p3 off",
            "rationale": "R8-v2 F5 判决实验重建：v4b 形态（P1/P3 双旗关，"
                         "行为级≡纯 v48 + P2 死价保险）之上叠加 P4 终局保果"
                         "层 v2——触发=双条件并集【day≥15 且峰回撤 "
                         "peak−lead≥2000 且 lead≥1500】∪【day≥24 且 "
                         "lead≥3000】，峰值经运行峰寄存器（编排处持有 "
                         "_V48H_P4_REGISTER）跟踪；未触发形态零足迹；只构建"
                         "+离线验证，不上线（零提交冻结 ba1b44c）。v1 尸检："
                         "触发过晚（9/14 局峰值日 d17 前，6 局重演 P4 形态"
                         "从未在场）致 v1 判决 FAIL 0/14",
        },
        "base": {"path": "software/kaggle_simulations/v48_derivative/main.py",
                 "sha256": b.BASE_SHA256, "bytes": b.BASE_BYTES_EXPECT,
                 "verbatim_prefix": True},
        "patches": {key: {"module": b.PATCHES[key]["module"],
                          "source": f"patches/{b.PATCHES[key]['source']}",
                          "sha256": patch_shas[key],
                          "bytes": patch_sizes[key],
                          "role": b.PATCHES[key]["role"],
                          "embedded": key in ("P2", "P4")}
                    for key in b.PATCH_ORDER},
        "flags": {"P1_ON": False, "P2_ON": True, "P3_ON": False,
                  "P4_ON": True},
        "flag_off_zero_wiring": {
            "P1": {"ok": True, "v5_token_hits": wiring["P1"]["v5_token_hits"]},
            "P3": {"ok": True, "v5_token_hits": wiring["P3"]["v5_token_hits"]},
            "verified": "v5 文本中 P1+P3 接线 token 计数全零；P2+P4 token "
                        "在场=接线真实（P4 token 集 v2 增 "
                        "_V48H_P4_REGISTER）",
        },
        "p4_off_no_disturbance": {
            **no_dist,
            "verified": "P4 旗增量无扰动自证：同装配器 P4-off 重建（v4b 旗面"
                        "与 P1-P3 全开旗面）与既有包/根提交件逐字节一致"
                        "（含 tar 逐字节）",
        },
        "wiring_check_detail": wiring,
        "blob_identity": ident,
        "cli_diagnostic_build": {"path": cli_path, "sha256": cli_sha,
                                 "bytes": cli_info["bytes"],
                                 "sha_match_in_process": True},
        "main_py": {"bytes": len(main_v5),
                    "sha256": b.sha256_bytes(main_v5),
                    "base_prefix_bytes": b.BASE_BYTES_EXPECT},
        "submission_tar_gz": {"bytes": len(tar_bytes),
                              "sha256": b.sha256_bytes(tar_bytes),
                              "members": names,
                              "deterministic_double_pack": True},
        "deterministic_double_build": True,
        "stdlib_only": True,
        "competition_slug": {"value": slug,
                             "extracted_from":
                                 "software/scripts/sync_online_probe.py"},
        "submit_message": SUBMIT_MESSAGE_V5,
        "gate_results": {"status": "PENDING",
                         "note": "R8-v2 F5 发射冒烟四门回填（tmp/fourgate_v5.py"
                                 " → tmp/probes_v5/v5_smoke.json）；双臂对照"
                                 "判决 gates/out/lead_protection_v2_verdict"
                                 ".json；h2h/panel 战后资产不适用（零提交冻结"
                                 " ba1b44c）"},
    }
    with open(os.path.join(V5_DIR, "build_manifest.json"), "w",
              encoding="utf-8") as h:
        json.dump(manifest, h, ensure_ascii=False, indent=2, sort_keys=True)
        h.write("\n")

    readme = build_readme_v5(manifest["main_py"]["sha256"],
                             manifest["main_py"]["bytes"],
                             manifest["submission_tar_gz"]["sha256"],
                             manifest["submission_tar_gz"]["bytes"],
                             patch_shas, patch_sizes)
    with open(os.path.join(V5_DIR, "README.md"), "w", encoding="utf-8") as h:
        h.write(readme)

    print(json.dumps({
        "v5_main_sha256": manifest["main_py"]["sha256"],
        "v5_main_bytes": manifest["main_py"]["bytes"],
        "v5_tar_sha256": manifest["submission_tar_gz"]["sha256"],
        "v5_tar_bytes": manifest["submission_tar_gz"]["bytes"],
        "base_sha256": b.BASE_SHA256,
        "slug": slug, "submit_message": SUBMIT_MESSAGE_V5,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
