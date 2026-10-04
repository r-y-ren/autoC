"""归档编排（R11+R12）：三档划分核验、保留档可跑探针、归档档 import 面断言、bc models 登记、分层注册表落盘（旧树冻结，注册表即战后 fn-close 搬移执行清单）。

上游: R11, R12（详见 fn_docs/responsibility.md）

实现要点：
- 五步编排：①实际清单核验（裁决清单须全部在场，缺件 fail-closed；范围外
  脚本登记不静默——R11 只辖 26 件法证脚本，评估链/库件归其他需求）；
  ②partition_script_tiers 三档划分；③v143 前置探针（fn_work run_official_bench
  模块 docstring 含 seated=吸收留痕；未吸收即拒绝归档 v143——裁决档位保留、
  战后搬移执行面封锁、overall=False）；④保留档 5 件逐件可跑性探针
  （默认 `python <script> --help` 子进程，只读旧树）+归档档 import 面源文本
  扫描（import/from 语句与带引号文件名引用命中即失败；docstring 散文提及
  不算依赖——实测 p41 对 round23_dtsp_stepdiff_probe 仅口径注释）；⑤注册表
  落盘 <战役根>/fn_work/archive_registry.json+裁决 dict。
- 零物理移动（旧树冻结）：归档档 dest=forensics_archive/scripts/、bc models
  dest=forensics_archive/bc_models/（战役根内新定义布局，D14 合规）——
  本批只登记路径；物理搬移属战后 fn-close 期按注册表逐件 git mv。
- 探针/吸收检查器可注入（probe_runner/bench_absorption_checker），
  镜像测试在 tmp 假树上全链演练；路径全由调用方传入（R20：模块内零字面
  战役路径）。
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from archive_forensic_assets.archive_bc_models import archive_bc_models
from archive_forensic_assets.partition_script_tiers import (
    ADJUDICATED_TIERS,
    TIER_ARCHIVE,
    TIER_RETAIN,
    TIER_TOOLBOX,
    partition_script_tiers,
)

__all__ = ["archive_forensic_assets", "SCRIPTS_POSTWAR_DIR",
           "PROBE_TIMEOUT_S"]

# 归档档脚本战后落位（战役根相对）；保留/工具箱档留主线原位（dest=None）
SCRIPTS_POSTWAR_DIR = "forensics_archive/scripts"
PROBE_TIMEOUT_S = 120

# 归档件在保留/工具箱 import 面的命中模式：import/from 语句 + 带引号文件名
# 引用（subprocess/importlib 动态装载形态）；散文提及（docstring 口径注释）不算
_IMPORT_STMT_TMPL = r"(?m)^[ \t]*(?:import[ \t]+{mod}\b|from[ \t]+{mod}\b)"
_FILENAME_REF_TMPL = r"[\"']{file}[\"']"

_REGISTRY_CONTRACT = "R11+R12 archive_forensic_assets（fn_docs/responsibility.md）"


def _default_probe_runner(script_path) -> tuple[bool, str]:
    """保留档可跑性探针：`python <script> --help`（只读，exit 0 即可跑）。"""
    path = Path(script_path)
    try:
        proc = subprocess.run(
            [sys.executable, str(path), "--help"],
            capture_output=True, text=True, timeout=PROBE_TIMEOUT_S,
            cwd=str(path.parent))
    except subprocess.TimeoutExpired:
        return False, f"--help 超时（>{PROBE_TIMEOUT_S}s）"
    detail = (proc.stderr or proc.stdout or "").strip().splitlines()
    head = detail[0][:120] if detail else ""
    return proc.returncode == 0, f"exit {proc.returncode} (--help) {head}".rstrip()


def _default_bench_absorption_checker(campaign_root) -> dict:
    """v143 前置检查：fn_work run_official_bench 模块 docstring 含 seated（B3 吸收留痕）。"""
    bench = Path(campaign_root) / "fn_work" / "src" / "run_official_bench" \
        / "run_official_bench.py"
    if not bench.is_file():
        return {"absorbed": False,
                "evidence": f"吸收实现缺失: {bench} 不存在（B3 未完成？）"}
    text = bench.read_text(encoding="utf-8", errors="replace")
    docstring = text.split('"""')[1] if '"""' in text else ""
    if "seated" in docstring:
        return {"absorbed": True,
                "evidence": f"{bench.relative_to(campaign_root)} 模块 docstring "
                            f"含 seated 吸收留痕（B3 完成）"}
    return {"absorbed": False,
            "evidence": f"{bench.relative_to(campaign_root)} 模块 docstring "
                        f"未见 seated 吸收留痕"}


def _scan_import_face(scripts_dir, retained_toolbox: list[dict],
                      archived: list[dict]) -> list[dict]:
    """归档档模块在保留/工具箱源文本中的 import 面命中（语句/带引号文件名）。"""
    patterns = []
    for entry in archived:
        mod = Path(entry["file"]).stem
        patterns.append((entry["file"], re.compile(
            _IMPORT_STMT_TMPL.format(mod=re.escape(mod))))
        )
        patterns.append((entry["file"], re.compile(
            _FILENAME_REF_TMPL.format(file=re.escape(entry["file"]))))
        )
    hits = []
    for host in retained_toolbox:
        source = (Path(scripts_dir) / host["file"]).read_text(
            encoding="utf-8", errors="replace")
        for target, pattern in patterns:
            match = pattern.search(source)
            if match:
                line_no = source.count("\n", 0, match.start()) + 1
                hits.append({"file": target, "referer": host["file"],
                             "line": line_no})
    return sorted(hits, key=lambda h: (h["referer"], h["file"]))


def _postwar_execution(archive_count: int, models_count: int,
                       blocked: list[str]) -> dict:
    return {
        "when": "fn-close 期（战后收口，旧树冻结解除后）",
        "registry_only": True,
        "steps": [
            f"归档档 {archive_count} 件按 dest 逐件 git mv 至 "
            f"{SCRIPTS_POSTWAR_DIR}/（保留/工具箱档 dest=null 留主线原位）",
            f"bc models {models_count} 件按 dest 逐件 git mv 至 "
            f"forensics_archive/bc_models/",
            "搬移后跑 R11 验收：归档件不在主线 import 路径（grep 断言）"
            "+ 保留档 5 件逐件可跑",
            "搬移后跑 R12 验收：新结构代码树（fn_work/src）grep bc_model 零命中",
        ],
        "blocked_files": blocked,
        "note": "blocked_files 列出前置未满足而拒绝搬移的件（如 v143 未吸收 seated），"
                "前置满足后从本清单移除方可执行其搬移。",
    }


def archive_forensic_assets(scripts_dir, models_dir, *, registry_path=None,
                            bench_absorption_checker=None,
                            probe_runner=None) -> dict:
    """三档归档编排+验证+注册表落盘（旧树零物理移动），返回裁决 dict。

    Args:
        scripts_dir: <战役根>/software/scripts（实际清单来源，只读）。
        models_dir: <战役根>/software/bc_track/models（R12 证据件，只读）。
        registry_path: 注册表落盘路径；None=战役根/fn_work/archive_registry.json。
        bench_absorption_checker: v143 前置检查器 () -> {"absorbed": bool,
            "evidence": str}；None=默认读 fn_work run_official_bench docstring。
        probe_runner: 保留档探针 (script_path) -> (ok, detail)；None=默认
            子进程 `python <script> --help`。

    Returns:
        裁决 dict：{overall, counts, retained_probes, import_face_clean,
        import_face_hits, v143_precondition, missing_adjudicated,
        out_of_r11_scope, bc_models_total_bytes, registry_path, summary}
        overall ⇔ 裁决件全在场 + 保留档 5 件探针全过 + 归档档 import 面零命中
        + v143 前置满足。

    Raises:
        ValueError: scripts 目录缺失/裁决清单引用缺件（fail-closed）。
    """
    scripts = Path(scripts_dir)
    if not scripts.is_dir():
        raise ValueError(f"scripts 目录不存在或非目录: {scripts}")
    campaign_root = scripts.parent.parent
    checker = bench_absorption_checker or (
        lambda: _default_bench_absorption_checker(campaign_root))
    probe = probe_runner or _default_probe_runner

    # ---- ① 实际清单核验（裁决件全在场；范围外登记不静默）----
    actual = sorted(p.name for p in scripts.glob("*.py"))
    if not actual:
        raise ValueError(f"scripts 目录无 .py 脚本: {scripts}")
    missing_adjudicated = sorted(set(ADJUDICATED_TIERS) - set(actual))
    if missing_adjudicated:
        raise ValueError(
            f"R11 裁决清单引用的 {len(missing_adjudicated)} 件在实际目录缺失，"
            f"fail-closed 拒绝划分: {missing_adjudicated}\n"
            f"排查: 确认传入 <战役根>/software/scripts（实际清单={len(actual)} 件）。")
    scope = sorted(set(ADJUDICATED_TIERS) & set(actual))
    out_of_scope = sorted(set(actual) - set(ADJUDICATED_TIERS))

    # ---- ② 三档划分 + v143 前置（未吸收即拒绝归档 v143）----
    tiers = partition_script_tiers(scope)
    v143_precondition = checker()
    blocked = [] if v143_precondition["absorbed"] else ["v143_sellrace_gates.py"]

    # ---- ③ 保留档探针 + 归档档 import 面扫描 ----
    retained_probes = []
    for entry in tiers[TIER_RETAIN]:
        ok, detail = probe(scripts / entry["file"])
        retained_probes.append({"file": entry["file"], "ok": ok,
                                "detail": detail})
    import_face_hits = _scan_import_face(
        scripts, tiers[TIER_RETAIN] + tiers[TIER_TOOLBOX],
        tiers[TIER_ARCHIVE])
    import_face_clean = not import_face_hits

    # ---- ④ bc models 归档登记（R12）----
    bc = archive_bc_models(models_dir)

    # ---- ⑤ 注册表落盘 + 裁决 ----
    def with_dest(entry: dict) -> dict:
        dest = (f"{SCRIPTS_POSTWAR_DIR}/{entry['file']}"
                if entry["tier"] == TIER_ARCHIVE else None)
        return {**entry, "postwar_dest": dest}

    counts = {**tiers["counts"], "bc_models": len(bc["entries"]),
              "out_of_r11_scope": len(out_of_scope)}
    overall = (not missing_adjudicated
               and all(p["ok"] for p in retained_probes)
               and import_face_clean
               and v143_precondition["absorbed"])
    summary = (f"三档 {tiers['counts'][TIER_RETAIN]}/{tiers['counts'][TIER_TOOLBOX]}/"
               f"{tiers['counts'][TIER_ARCHIVE]} + bc_models {len(bc['entries'])} 件登记；"
               f"保留档探针 {sum(p['ok'] for p in retained_probes)}/"
               f"{len(retained_probes)} 过；import 面"
               f"{'零命中' if import_face_clean else f'{len(import_face_hits)} 命中'}；"
               f"v143 前置{'满足' if v143_precondition['absorbed'] else '未满足（拒绝归档）'}"
               f"——{'PASS' if overall else 'FAIL'}")
    verdict = {
        "overall": overall,
        "counts": counts,
        "retained_probes": retained_probes,
        "import_face_clean": import_face_clean,
        "import_face_hits": import_face_hits,
        "v143_precondition": v143_precondition,
        "missing_adjudicated": missing_adjudicated,
        "out_of_r11_scope": out_of_scope,
        "bc_models_total_bytes": bc["total_bytes"],
        "summary": summary,
    }

    registry = {
        "contract": _REGISTRY_CONTRACT,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "frozen_tree": True,
        "postwar_execution": _postwar_execution(
            tiers["counts"][TIER_ARCHIVE], len(bc["entries"]), blocked),
        "counts": counts,
        "tiers": {tier: [with_dest(e) for e in tiers[tier]]
                  for tier in (TIER_RETAIN, TIER_TOOLBOX, TIER_ARCHIVE)},
        "bc_models": bc,
        "out_of_r11_scope": out_of_scope,
        "verdict": verdict,
    }
    reg_path = Path(registry_path) if registry_path is not None \
        else campaign_root / "fn_work" / "archive_registry.json"
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    verdict["registry_path"] = str(reg_path)
    return verdict
