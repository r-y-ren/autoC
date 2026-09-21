"""CODEMAP 4 失准处勘误记录后随新结构落地退役（新结构以 responsibility.md+包 docstring 替代；旧树冻结=只产勘误记录+退役标记，CODEMAP 物理退役=战后随 fn-close）。

上游: R7, R16, R18（详见 fn_docs/responsibility.md）

实现要点：
- 4 处失准（VERIFIED_ERRATA 模块级唯一事实源，证据=B14 实读实测）：
  E1 profile_v48_gap"（历史在役）"——实为输出路径损坏不可复跑
  （scripts/profile_v48_gap.py:100 以 REPO_ROOT——解析为 workspace/ 容器——拼
  'workspace/kaggriculture/...' 得双重前缀，mkdir(exist_ok=True) 无 parents 必崩）；
  E2 economy.py"market.py 消费"不实——全库导入扫描仅 kgenv/__init__（再导出）、
  redlines.py（自身孤儿）、tests/test_economy.py 三处，market.py 零消费；
  E3"D. tests/（53 个测试文件）"——tests/test_*.py 实数 51（+conftest.py 非测试），
  基线 990+2 系 Windows 主力机口径（R6 机器语境）；
  E4 opponents 行未标注入库落差——入库恰两套（v48_main+v72_main，PROVENANCE
  实证），旧 README"四套解码版"中 2945/island-ga/kaggri 系 machine-local
  references 不入库。
- 退役标记：替代面=fn_docs/responsibility.md（结构/职责单一事实源）
  +fn_work/src/<功能块>/<模块>.py 包 docstring（逐文件用途）；时点=战后
  fn-close（与 archive_registry 同批）；附 probes 子目录清单漂移注记（退役
  理由补充，非勘误主项）。
- errata_list 可注入（测试/复检用）；缺省=VERIFIED_ERRATA。产物单文件
  fn_work/doc_fixes/codemap_errata.md，零绝对路径（R20：经
  shared.discover_campaign_roots 发现根）。
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["retire_codemap_with_errata", "VERIFIED_ERRATA", "RETIREMENT_NOTE"]

# CODEMAP 4 失准处（2026-09-21 版 CODEMAP.md；证据=B14 本批实读实测）
VERIFIED_ERRATA = [
    {
        "id": "E1",
        "codemap_line": 93,
        "subject": "profile_v48_gap",
        "claim": "C 节『sprintA_structure_probe.py / profile_v48_gap.py / m4_switchover_regression.py / "
                 "solver_shadow_stats.py | …（历史在役）』——profile_v48_gap 被归入在役面",
        "reality": "输出路径损坏，不可复跑：scripts/profile_v48_gap.py:22-24 的 REPO_ROOT 解析为 "
                   "workspace/ 容器目录（SOFTWARE_ROOT 上两级），:100 再拼 "
                   "'workspace/kaggriculture/software/exports/probes/intel' 得双重前缀 "
                   "workspace/workspace/…（不存在），:101 scratch.mkdir(exist_ok=True) 无 parents=True "
                   "即 FileNotFoundError——一跑即崩",
        "evidence": "profile_v48_gap.py:22-24/100-101 实读；workspace/ 下无 workspace/ 子目录（实测）",
        "correction": "归类改『历史件（路径损坏，复跑需先修输出路径与语料依赖）』；v48 差距画像的"
                      "现役事实面=exports/replay_profiles 台账与 fn_docs 记录",
    },
    {
        "id": "E2",
        "codemap_line": 40,
        "subject": "economy",
        "claim": "B 节『kgenv/economy.py | 经济语义镜像（价格公式/棚容/城镇需求——market.py 消费）』",
        "reality": "market.py 消费不实：全库 economy 导入扫描仅三处——kgenv/__init__.py:19（eager "
                   "再导出）、kgenv/redlines.py:33（自身即评估链孤儿）、tests/test_economy.py:11"
                   "（测试）；提交链 src/market.py 与 scripts/ 零消费",
        "evidence": "grep 'kgenv.economy|from .economy|import economy' 全库实测三命中，market.py 零命中",
        "correction": "口径改『评估链孤儿库件（仅测试与再导出消费）』；处置=R13/R14 移测试资产区"
                      "（fn_docs/responsibility.md downgrade_dormant_assets 块）",
    },
    {
        "id": "E3",
        "codemap_line": 95,
        "subject": "tests",
        "claim": "D 节『tests/（53 个测试文件，基线 990 passed+2 skipped）』",
        "reality": "tests/test_*.py 实数 51（另有 conftest.py 引导件非测试）；基线 990+2 系 "
                   "Windows 主力机+语料在机口径（本机 Linux 976P/8F/8S 属环境性，R6 机器语境）",
        "evidence": "ls tests/test_*.py | wc -l = 51（实测）；机器语境见 fn_docs/machine_context.md",
        "correction": "计数改 51；基线数字挂机器语境标注（机器无关化=R6 portable_test_baseline）",
    },
    {
        "id": "E4",
        "codemap_line": 111,
        "subject": "opponents",
        "claim": "E 节『opponents/ | 本地陪练源码：v48_main.py（top-10 解码版）、v72_main.py（历史代）"
                 "+PROVENANCE.md』——未标注入库落差",
        "reality": "入库恰两套（ls 实测：v48_main.py+v72_main.py+PROVENANCE.md）；旧 README 面"
                   "『四套公开顶级 bot 的解码版（v48/2945/island-ga/kaggri）』中 2945/island-ga/"
                   "kaggri 系 machine-local references（gitignored）不入库——本行未标注该落差，"
                   "与 README 旧面叠加留有『≥三套在库』误读空间",
        "evidence": "kaggle_simulations/opponents/ 目录实测两 .py；opponents/PROVENANCE.md 仅两源记录；"
                    "gap_table §一#5（证据=opponents/、PROVENANCE.md）",
        "correction": "入库清单=两套口径（fn_docs/README.md 功能#7 已回写『入库两套』）；"
                      "2945/island-ga/kaggri 标注为本机 references 参考件",
    },
]

RETIREMENT_NOTE = {
    "retire_when": "战后 fn-close 期（旧树冻结解除，与 archive_forensic_assets 注册表同批执行）",
    "replaced_by": [
        "fn_docs/responsibility.md——新结构单一事实源（功能块/子函数/职责/签名意图/核验命令）",
        "fn_work/src/<功能块>/<模块>.py 包 docstring——逐文件用途与实现要点",
    ],
    "drift_note": "退役附注（清单漂移，非勘误主项）：G 节 probes 子目录清单"
                  "（round23_forensics/v48_launch/v48plus）与现状"
                  "（planner_bench/twin_fidelity/v143_sellrace/v15_ignition）漂移——probes 清理"
                  "所致；probes 面策略由本批 fn_work/doc_fixes/probes_policy.md 显式化",
}


def _render_erratum(e: dict) -> str:
    return (
        f"### {e['id']}（CODEMAP L{e['codemap_line']}，主题: {e['subject']}）\n"
        f"- **CODEMAP 原文**：{e['claim']}\n"
        f"- **实况**：{e['reality']}\n"
        f"- **证据**：{e['evidence']}\n"
        f"- **修正口径**：{e['correction']}\n"
    )


def retire_codemap_with_errata(errata_list: list = None, *,
                               doc_fixes_root=None) -> dict:
    """CODEMAP 勘误记录+退役标记落盘（旧树只读，产物=fn_work/doc_fixes/codemap_errata.md）。

    Args:
        errata_list: 勘误清单（dict 列表；None=VERIFIED_ERRATA 内建 4 条实测勘误）。
        doc_fixes_root: 产物落位根（None=战役根 fn_work/doc_fixes，特征发现）。

    Returns:
        dict：errata 数/产物路径（战役根相对，假树时为相对 doc_fixes_root）/ 退役标记摘要。

    Raises:
        ValueError: 注入的 errata_list 为空或条目缺必备键（fail-closed，不产空勘误）。
    """
    errata = VERIFIED_ERRATA if errata_list is None else list(errata_list)
    if not errata:
        raise ValueError("errata_list 为空——拒绝生成空勘误记录（fail-closed）")
    required = {"id", "codemap_line", "subject", "claim", "reality", "evidence", "correction"}
    for e in errata:
        missing = required - set(e)
        if missing:
            raise ValueError(f"勘误条目缺必备键 {sorted(missing)}: {e.get('id', e)!r}")

    if doc_fixes_root is None:
        roots = discover_campaign_roots()
        doc_fixes_root = roots["campaign_root"] / "fn_work" / "doc_fixes"
    doc_fixes_root = Path(doc_fixes_root)
    doc_fixes_root.mkdir(parents=True, exist_ok=True)

    lines = [
        "# CODEMAP 勘误记录与退役标记（R16/R19-勘误部分）",
        "",
        "> 对象：software/CODEMAP.md（2026-09-21 版，本批只读零改动——旧树冻结）。",
        "> 形态：勘误记录+退役标记；CODEMAP 物理退役=战后 fn-close（套用本记录后随新结构落地）。",
        f"> 生成：fn_work/src/sync_documentation/retire_codemap_with_errata.py"
        f"（B14，{datetime.now().astimezone().isoformat(timespec='seconds')}）。",
        "",
        "## 勘误（4 处失准，证据=本批实读实测）",
        "",
    ]
    lines += [_render_erratum(e) for e in errata]
    lines += [
        "## 退役标记",
        "",
        f"- **时点**：{RETIREMENT_NOTE['retire_when']}。",
        "- **替代面**：",
    ]
    lines += [f"  - {r}" for r in RETIREMENT_NOTE["replaced_by"]]
    lines += [
        f"- **{RETIREMENT_NOTE['drift_note'].split('：', 1)[0]}**：{RETIREMENT_NOTE['drift_note'].split('：', 1)[1]}",
        "",
    ]

    out_path = doc_fixes_root / "codemap_errata.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")

    try:
        rel = str(out_path.relative_to(discover_campaign_roots()["campaign_root"]))
    except Exception:  # 测试假树：doc_fixes 在战役根外/根不可发现
        rel = str(out_path)
    return {
        "errata_count": len(errata),
        "errata_ids": [e["id"] for e in errata],
        "path": rel,
        "retire_when": RETIREMENT_NOTE["retire_when"],
    }
