"""文档层一致性收口编排（bc 记录修正/CODEMAP 勘误退役/probes 策略显式化），对账失败即失败（R16 验收=gap_table §一清单逐项清零）。

上游: R7, R16, R18（详见 fn_docs/responsibility.md）

实现要点：
- 编排三叶（fix_bc_track_records→retire_codemap_with_errata→codify_probes_policy，
  产物全落 fn_work/doc_fixes/）+顶层对账+收口报告 sync_report.md。
- 对账口径：旧树文件（software/README.md、CODEMAP.md）的物理修正属战后；
  本批口径=**修正副本覆盖 gap_table §一全部 8 项对应面**——逐项核对新文档面
  锚点在档：#1-#7=fn_docs/README.md v1（阶段三裁决后回写的 README 修正副本）
  及其配套 fn_docs 记录（responsibility.md/recalculation_ledger.md）；#8=本批
  doc_fixes/codemap_errata.md（4 勘误）。任一锚点缺档=对账失败（ReconciliationError，
  fail-closed），报告先行落盘（FAIL 横幅如实）。
- 裁决 dict：{leaves, reconciliation{items,passed,criteria}, postwar_actions,
  artifacts, passed}；GAP_TABLE_ITEMS 为模块级唯一事实源（8 项=gap_table §一
  逐条，锚点串均对真实新文档面实测）。
- 全参可注入（campaign_root/doc_fixes_root/journal_ledger/errata_list/
  probes_state）——测试用 tmp 假树，不写真 doc_fixes；实跑缺省=特征发现
  根+实况构建（R20：零字面战役路径）。
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots
from sync_documentation.codify_probes_policy import codify_probes_policy
from sync_documentation.fix_bc_track_records import fix_bc_track_records
from sync_documentation.retire_codemap_with_errata import retire_codemap_with_errata

__all__ = ["ReconciliationError", "sync_documentation", "reconcile_gap_table",
           "GAP_TABLE_ITEMS"]

_ERRATA_ANCHOR = "doc_fixes"  # 特殊锚点键：解析为 doc_fixes_root/codemap_errata.md


class ReconciliationError(RuntimeError):
    """gap_table §一 8 项对账失败（修正副本未覆盖全部对应面）——fail-closed。"""


# gap_table §一 8 项（README/代码矛盾）→ 新文档面锚点（对应面覆盖判据）
GAP_TABLE_ITEMS = [
    {
        "id": 1,
        "claim": "README 功能表#1『stdlib-only 单文件自包含程序』",
        "reality": "tar.gz 多模块包（main+src 10+planner 6）；『薄装载器』表述反而正确",
        "surface": "fn_docs/README.md §工作流程A#1+功能#1（多模块包修正面）",
        "anchors": [("fn_docs/README.md", ["不是单文件", "自包含多模块包"])],
    },
    {
        "id": 2,
        "claim": "README 流程A#1『九个功能模块』",
        "reality": "_MODULE_ORDER=10 模块（wave 加入后）；main.py 头注释同过期",
        "surface": "fn_docs/README.md §A#1『十个』+responsibility.md 迁移口径",
        "anchors": [("fn_docs/README.md", ["十个"]),
                    ("fn_docs/responsibility.md", ["十模块"])],
    },
    {
        "id": 3,
        "claim": "README 功能表#3『Elo/BT 评级（顺序无关批量）』",
        "reality": "Elo 顺序敏感（其序恰为冻结回归门依据）；仅 BT 批量顺序无关",
        "surface": "fn_docs/README.md 功能#3（双轨口径拆分）",
        "anchors": [("fn_docs/README.md", ["按对局顺序更新", "顺序无关"])],
    },
    {
        "id": 4,
        "claim": "README 功能表#3 将『红线清单』列为本地评估体系组成",
        "reality": "redlines.py 零 gate/arena 消费，孤儿模块",
        "surface": "fn_docs/responsibility.md R13/R14 处置（economy/redlines 移测试资产区）",
        "anchors": [("fn_docs/responsibility.md", ["redlines 移测试资产区"])],
    },
    {
        "id": 5,
        "claim": "README 功能表#7『四套公开顶级 bot 的解码版（v48/2945/island-ga/kaggri）』",
        "reality": "库内 opponents/ 仅 v48_main+v72 两套；2945/island-ga/kaggri 系 "
                   "machine-local references（gitignored）不入库",
        "surface": "fn_docs/README.md 功能#7『入库两套』+本批 codemap_errata E4",
        "anchors": [("fn_docs/README.md", ["入库两套"]),
                    (_ERRATA_ANCHOR, ["opponents"])],
    },
    {
        "id": 6,
        "claim": "README 功能表#2/流程隐含『孪生与 d0 反事实=可信计算』",
        "reality": "孪生本身逐位保真成立；harness 席位错位使 me_seat=1 局 d0 反事实/"
                   "离线基准数字系伪影（已知勘误，重算入台账）",
        "surface": "fn_docs/README.md 功能#2 口径注+recalculation_ledger.md 双口径台账",
        "anchors": [("fn_docs/README.md", ["席位错位"]),
                    ("fn_docs/recalculation_ledger.md", ["席位"])],
    },
    {
        "id": 7,
        "claim": "README 工作流程 D『每波过查→/accept 全量验收→分片汇总入 metrics』",
        "reality": "/accept 链 09-01 起静默（m6/m7 无验收记录）；事实治理=JOURNAL 详记"
                   "+git 提交+metrics 分片",
        "surface": "fn_docs/README.md §D 实际治理现状（诚实口径）",
        "anchors": [("fn_docs/README.md", ["静默", "JOURNAL 详记"])],
    },
    {
        "id": 8,
        "claim": "CODEMAP『economy.py market.py 消费』『profile_v48_gap 在役』『53 tests』『opponents』",
        "reality": "economy 零消费；profile_v48_gap 路径损坏必崩；51 tests；入库两套",
        "surface": "本批 doc_fixes/codemap_errata.md（E1-E4 勘误+退役标记）",
        "anchors": [(_ERRATA_ANCHOR, ["profile_v48_gap", "economy", "tests", "opponents"])],
    },
]


def _anchor_file(anchor_path: str, campaign_root: Path, doc_fixes_root: Path) -> Path:
    if anchor_path == _ERRATA_ANCHOR:
        return doc_fixes_root / "codemap_errata.md"
    return campaign_root / anchor_path


def _rel(path, campaign_root: Path) -> str:
    """报告内路径战役根相对化（假树/根外回落原串），保持跨机可 diff。"""
    try:
        return str(Path(path).relative_to(campaign_root))
    except ValueError:
        return str(path)


def reconcile_gap_table(campaign_root, doc_fixes_root) -> dict:
    """gap_table §一 8 项在新文档面的清零核对（修正副本覆盖全部对应面=锚点逐项在档）。"""
    campaign_root, doc_fixes_root = Path(campaign_root), Path(doc_fixes_root)
    items = []
    for spec in GAP_TABLE_ITEMS:
        details, ok = [], True
        for anchor_path, needles in spec["anchors"]:
            f = _anchor_file(anchor_path, campaign_root, doc_fixes_root)
            if not f.is_file():
                ok = False
                details.append(f"缺档: {anchor_path}")
                continue
            text = f.read_text(encoding="utf-8")
            for n in needles:
                hit = n in text
                ok = ok and hit
                details.append(f"{'✓' if hit else '✗'} {anchor_path} 含『{n}』")
        items.append({"id": spec["id"], "claim": spec["claim"],
                      "reality": spec["reality"], "surface": spec["surface"],
                      "passed": ok, "detail": details})
    return {
        "items": items,
        "passed": all(i["passed"] for i in items),
        "criteria": "修正副本覆盖 gap_table §一全部 8 项对应面"
                    "（旧树物理修正战后；新文档面锚点逐项在档）",
    }


def sync_documentation(*, campaign_root=None, doc_fixes_root=None,
                       journal_ledger=None, errata_list=None,
                       probes_state=None) -> dict:
    """文档层一致性收口编排（三叶+对账+收口报告；产物全落 fn_work/doc_fixes/）。

    Returns:
        裁决 dict：{leaves, reconciliation, postwar_actions, artifacts, passed}。

    Raises:
        ReconciliationError: 8 项对账未全覆盖（报告已先落盘，FAIL 如实）。
    """
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    campaign_root = Path(campaign_root)
    if doc_fixes_root is None:
        doc_fixes_root = campaign_root / "fn_work" / "doc_fixes"
    doc_fixes_root = Path(doc_fixes_root)
    doc_fixes_root.mkdir(parents=True, exist_ok=True)

    # ---------- 三叶 ----------
    bc = fix_bc_track_records(journal_ledger, campaign_root=campaign_root,
                              doc_fixes_root=doc_fixes_root)
    err = retire_codemap_with_errata(errata_list, doc_fixes_root=doc_fixes_root)
    policy_path, pol = codify_probes_policy(probes_state, doc_fixes_root=doc_fixes_root)

    # ---------- 对账 ----------
    recon = reconcile_gap_table(campaign_root, doc_fixes_root)

    postwar_actions = [
        f"bc_track 修正副本+diff 注册（{bc['diff_count']} 处）按 diff_registry.json"
        " 战后套用并跑 R7 复现命令核验",
        f"CODEMAP 勘误（{err['errata_count']} 条）战后套用，CODEMAP 随 fn-close 退役"
        "（替代面=responsibility.md+包 docstring）",
    ] + list(pol["postwar_actions"])

    # ---------- 收口报告 ----------
    verdict = bool(recon["passed"])
    lines = [
        "# sync_documentation 收口报告（W4 文档层，B14 实跑）",
        "",
        f"> 生成：fn_work/src/sync_documentation/sync_documentation.py"
        f"（{datetime.now().astimezone().isoformat(timespec='seconds')}）。",
        f"> 对账口径：{recon['criteria']}。",
        "",
        "## 三叶产物",
        "",
        f"- **fix_bc_track_records**：修正副本 {len(bc['corrected_files'])} 件"
        f"（README 3 处 diff+票面 03/08/04-07 六件 Status diff={bc['diff_count']} 处），"
        f"diff 注册={_rel(bc['registry'], campaign_root)}（战后套用清单，台账依据=JOURNAL "
        f"{bc['ledger']['date']} 收口行）。",
        f"- **retire_codemap_with_errata**：勘误 {'/'.join(err['errata_ids'])} "
        f"落 {err['path']}；退役时点={err['retire_when']}。",
        f"- **codify_probes_policy**：策略文档落 {_rel(policy_path, campaign_root)}；现存 "
        f"{pol['summary_count']} 份摘要全部入库（{pol['summary_check']}）；"
        f"不一致 {len(pol['inconsistencies'])} 条（规则面缺口，已标 postwar_action）。",
        "",
        "## gap_table §一 8 项对账（新文档面清零核对）",
        "",
        "| # | 旧面失准表述 | 实况 | 新文档面覆盖（对应面） | 清零 |",
        "|---|---|---|---|---|",
    ]
    for i in recon["items"]:
        lines.append(f"| {i['id']} | {i['claim']} | {i['reality']} | {i['surface']} "
                     f"| {'✓' if i['passed'] else '✗ ' + '; '.join(d for d in i['detail'] if d.startswith('✗') or d.startswith('缺'))} |")
    lines += [
        "",
        "## 战后动作（旧树冻结解除后套用）",
        "",
    ]
    lines += [f"- {a}" for a in postwar_actions]
    lines += ["", f"## 裁决: {'PASS（8/8 清零）' if verdict else 'FAIL（见上表 ✗ 项）'}", ""]

    report_path = doc_fixes_root / "sync_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    # ---------- 实跑播报（原文即核验输出） ----------
    print(f"[sync_documentation] 三叶产物: bc_track 修正副本+diff 注册 "
          f"({bc['diff_count']} diffs) / codemap_errata ({err['errata_count']} 条) / "
          f"probes_policy ({pol['summary_count']} 份摘要核对, "
          f"不一致 {len(pol['inconsistencies'])})")
    print(f"[sync_documentation] report -> {report_path}")
    for i in recon["items"]:
        marks = "; ".join(i["detail"])
        print(f"[sync_documentation] 对账 #{i['id']} {'PASS' if i['passed'] else 'FAIL'}: {marks}")
    print(f"[sync_documentation] 裁决: {'PASS' if verdict else 'FAIL'} "
          f"({sum(1 for i in recon['items'] if i['passed'])}/8) —— {recon['criteria']}")

    result = {
        "leaves": {"fix_bc_track_records": bc,
                   "retire_codemap_with_errata": err,
                   "codify_probes_policy": {"path": policy_path, **pol}},
        "reconciliation": recon,
        "postwar_actions": postwar_actions,
        "artifacts": [str(p) for p in sorted(doc_fixes_root.rglob("*")) if p.is_file()],
        "passed": verdict,
    }
    if not verdict:
        failed = [i["id"] for i in recon["items"] if not i["passed"]]
        raise ReconciliationError(
            f"gap_table §一对账失败（未覆盖项: {failed}）——修正副本须覆盖全部 8 项对应面；"
            f"详情见 {report_path}"
        )
    return result
