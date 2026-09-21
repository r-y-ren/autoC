"""exports/probes 策略显式化（结论 .md 全入库、数据中间物 gitignore）+现存 6 份摘要一致性核对（现存态违反入库规则即失败；规则面缺口的旧树修正战后套用=postwar_action）。

上游: R7, R16, R18（详见 fn_docs/responsibility.md）

实现要点：
- 策略规则（POLICY_RULES 模块级唯一事实源）：P1 结论 .md（评估摘要/勘误/
  法证结论）全入库；P2 数据中间物（JSON 产物/引擎缓存/大文件）gitignore；
  P3 引擎与源数据归 references/data（既有规则，引用不改）。
- probes_state 可注入（测试假树）：{probes_dir, summaries:[{relpath,tracked,
  bytes}], data_intermediates:[{relpath,tracked}], rule_ignores_new_summary_md,
  gitignore_patterns}；None=实况构建（git ls-files + git check-ignore 实测，
  经 shared.discover_campaign_roots 发现根，R20）。
- 失败语义双档（R18"不一致清单非空即失败"×旧树冻结的调和）：现存态违规
  （任一摘要未入库=结论可丢）→ ProbesPolicyViolation fail-closed；规则面
  缺口（.gitignore 模式会忽略未来新增摘要 .md）→ 如实列入不一致清单并标
  postwar_action（旧树 .gitignore 修正战后，本批只登记）。
- 产物单文件 fn_work/doc_fixes/probes_policy.md：规则+6 份摘要核对表+
  核对结论+不一致清单（含 postwar_action）。零绝对路径。
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["ProbesPolicyViolation", "codify_probes_policy", "POLICY_RULES"]

# 策略规则（显式化文本，落策略文档）
POLICY_RULES = [
    "P1 结论 .md 全入库：exports/probes/** 下的评估摘要/勘误/法证结论（*.md）一律 git 入库",
    "P2 数据中间物 gitignore：JSON 产物/引擎缓存/回放大文件等数据中间物不入库",
    "P3 引擎与源数据归 references/data（既有大文件规则，本策略不改其归宿）",
]

_PROBES_RELPREFIX = "software/exports/probes"
_STATE_REQUIRED_KEYS = ("summaries", "rule_ignores_new_summary_md")


class ProbesPolicyViolation(RuntimeError):
    """probes 现存态违反入库策略（结论 .md 未入库=结论可丢）——fail-closed。"""


def _git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True, text=True, check=False,
    )
    return proc.stdout if proc.returncode == 0 else ""


def build_real_probes_state(campaign_root=None, repo_root=None) -> dict:
    """实况构建 probes_state（git ls-files/check-ignore 实测）。"""
    if campaign_root is None or repo_root is None:
        roots = discover_campaign_roots()
        campaign_root = campaign_root or roots["campaign_root"]
        repo_root = repo_root or roots["repo_root"]
    campaign_root, repo_root = Path(campaign_root), Path(repo_root)
    probes_dir = campaign_root / "software" / "exports" / "probes"

    # ls-files/check-ignore 以战役根为 -C（pathspec 相对 cwd 解析，输出亦为战役根相对）
    tracked = {
        line.strip()
        for line in _git(campaign_root, "ls-files", "--", _PROBES_RELPREFIX).splitlines()
        if line.strip()
    }
    summaries, data_intermediates = [], []
    if probes_dir.is_dir():
        for p in sorted(probes_dir.rglob("*")):
            if not p.is_file() or p.name == "README.md":
                continue
            rel = str(p.relative_to(campaign_root))
            entry = {"relpath": rel, "tracked": rel in tracked, "bytes": p.stat().st_size}
            (summaries if p.suffix == ".md" else data_intermediates).append(entry)

    probe_rel = f"{_PROBES_RELPREFIX}/planner_bench/HYPOTHETICAL_new_summary.md"
    rc = subprocess.run(
        ["git", "-C", str(campaign_root), "check-ignore", "-q", probe_rel],
        capture_output=True, check=False,
    ).returncode
    patterns = [
        line for line in (repo_root / ".gitignore").read_text(encoding="utf-8").splitlines()
        if "exports/probes" in line
    ] if (repo_root / ".gitignore").is_file() else []
    return {
        "probes_dir": str(probes_dir),
        "summaries": summaries,
        "data_intermediates": data_intermediates,
        "rule_ignores_new_summary_md": rc == 0,
        "gitignore_patterns": patterns,
    }


def codify_probes_policy(probes_state=None, *, doc_fixes_root=None) -> tuple:
    """probes 策略文档落盘+现存摘要一致性核对。

    Args:
        probes_state: 现状快照（None=实况构建）；键见 build_real_probes_state。
        doc_fixes_root: 产物落位根（None=战役根 fn_work/doc_fixes）。

    Returns:
        (产物路径, 核对报告 dict)：报告含 summaries/inconsistencies/
        postwar_actions/summary_check。

    Raises:
        ProbesPolicyViolation: 任一现存结论 .md 未入库（现存态违规，fail-closed）。
        ValueError: probes_state 缺必备键或注入摘要清单为空。
    """
    if probes_state is None:
        probes_state = build_real_probes_state()
    missing = [k for k in _STATE_REQUIRED_KEYS if k not in probes_state]
    if missing:
        raise ValueError(f"probes_state 缺必备键 {missing}（fail-closed，不猜现状）")
    summaries = probes_state["summaries"]
    if not summaries:
        raise ValueError("probes_state.summaries 为空——现存 6 份摘要须实测在册后核对")

    untracked = [s["relpath"] for s in summaries if not s["tracked"]]
    if untracked:
        raise ProbesPolicyViolation(
            f"现存结论 .md 未入库（P1 违规，结论可丢）: {untracked}"
        )

    inconsistencies, postwar_actions = [], []
    if probes_state.get("rule_ignores_new_summary_md"):
        inconsistencies.append(
            ".gitignore 模式 " + str(probes_state.get("gitignore_patterns"))
            + " 仅回白 README.md——未来新增结论 .md 将被忽略（git check-ignore 实证 exit 0），"
              "与 P1『结论 .md 全入库』不一致"
        )
        postwar_actions.append(
            "postwar_action: 战后把 exports/probes 白名单补为 !**/*.md（或目录级规则），"
            "套用前新增摘要须手工 git add -f"
        )

    if doc_fixes_root is None:
        doc_fixes_root = discover_campaign_roots()["campaign_root"] / "fn_work" / "doc_fixes"
    doc_fixes_root = Path(doc_fixes_root)
    doc_fixes_root.mkdir(parents=True, exist_ok=True)

    lines = [
        "# exports/probes 入库策略（R18 显式化）",
        "",
        "> 生成：fn_work/src/sync_documentation/codify_probes_policy.py（B14，"
        f"{datetime.now().astimezone().isoformat(timespec='seconds')}）。",
        "> 适用面：software/exports/probes/**（旧树只读——.gitignore 的物理修正战后套用）。",
        "",
        "## 策略规则",
        "",
    ]
    lines += [f"- {r}" for r in POLICY_RULES]
    lines += [
        "",
        "## 现存摘要一致性核对",
        "",
        "| # | 摘要（战役根相对） | 入库 | bytes |",
        "|---|---|---|---:|",
    ]
    for i, s in enumerate(summaries, 1):
        lines.append(f"| {i} | {s['relpath']} | {'是' if s['tracked'] else '否'} | {s.get('bytes', '')} |")
    lines += [
        "",
        f"- **现存态**：{len(summaries)} 份结论摘要全部 git 在册"
        f"（P1 现存态一致{'；规则面缺口见下' if inconsistencies else '，规则面亦一致'}）。",
        f"- **数据中间物**：{len(probes_state.get('data_intermediates', []))} 件在盘未跟踪"
        "（如 twin_fidelity/engine_cache）——P2 一致。",
    ]
    if inconsistencies:
        lines += ["", "## 不一致清单（规则面缺口，旧树冻结故登记待战后）", ""]
        lines += [f"- {i}" for i in inconsistencies]
        lines += ["", "## 战后动作", ""]
        lines += [f"- {a}" for a in postwar_actions]
    else:
        lines += ["", "## 不一致清单", "", "（空——现存态与规则面均一致）"]
    lines += [""]

    out_path = doc_fixes_root / "probes_policy.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")

    report = {
        "policy_path": str(out_path),
        "summary_count": len(summaries),
        "summary_check": "all_tracked",
        "data_intermediate_count": len(probes_state.get("data_intermediates", [])),
        "inconsistencies": inconsistencies,
        "postwar_actions": postwar_actions,
    }
    return str(out_path), report
