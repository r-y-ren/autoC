"""sync_documentation 镜像测试共用假树：tmp 内构建战役特征树（blueprint.md+software+fn_docs），
一切产物落 tmp 的 doc_fixes——绝不写真 fn_work/doc_fixes（任务约束）。"""

from __future__ import annotations

from pathlib import Path

# JOURNAL 假台账：含 09-20 交付行+09-21 正式裁决行（BC 收口行特征与真树同构）
JOURNAL_ROWS = [
    "| 日期 | 阶段 | 内容 | 下一步 |",
    "|---|---|---|---|",
    "| 2026-09-20 | deliver | **Track-C 票 03 交付（BC 迭代修复轮：判定=弃牌收刀，归因写死）**："
    "前置修正与五级阶梯数字 | 终局程序 |",
    "| 2026-09-21 | deliver | **Track-C 票 03 判定：弃牌收刀（379b41e）+ M1 结论正式勘误 + 票 08 关账**："
    "①勘误置顶；⑤票 04/05/06/07 按『过门才继续』不触发（GPU 未租用零成本）；"
    "终局程序继续：24h 复采样在飞→09-25 对结构决策→09-27 冻结→09-30 终交 | 终局程序专用 |",
]

# bc_track README 假件：含三处待修锚（路径拼写/双斜杠/票 03 节标题），与真树同构
BC_README = """# bc_track —— Track-C 行为克隆（BC）轨（spec: docs/track-C-bc-spec.md）

从顶部选手官方回放训练行为克隆 agent。standalone——
不嫁接 v14.x chassis、不改 src//planner/；评估缝=孪生 d0 全季注入协议。

## 一键复现（全管线，约 15 分钟 CPU）

```bash
cd workspace/kaggressure/software
python bc_track/scripts/extract_samples.py --include-rounds
```

## 票 03 迭代结果（2026-09-20，判定=弃牌）

诚实基线 0-8，收刀。
"""

TICKET_STATUS = {
    "01": "ready-for-agent",
    "02": "ready-for-agent",
    "03": "done（2026-09-20，判定=**弃牌**：最好候选=门 A 的 6.2%；差距归因见下，收刀）",
    "04": "ready-for-agent",
    "05": "ready-for-agent",
    "06": "ready-for-agent",
    "07": "ready-for-agent",
    "08": "ready-for-agent",
}
TICKET_NAMES = {
    "01": "corpus-samples", "02": "bc-v0-eval", "03": "iterate-best",
    "04": "pure-python-package", "05": "hard-gates", "06": "gpu-rental",
    "07": "rl-finetune", "08": "endgame-closeout",
}

# fn_docs 假记录：按 GAP_TABLE_ITEMS 锚点逐串铺设（真树锚点的同构缩影）
FN_DOCS_README = (
    "装载：main.py 是个薄装载器，自包含多模块包——不是单文件；按固定顺序把十个功能模块和"
    "规划器装进内存。评估体系：Elo 按对局顺序更新（该序恰是回归门依据），BT 批量、顺序无关。"
    "对手血统库：入库两套（v48 解码版+v72 历史件）。数字孪生注意口径：历史离线数字中坐 1 号位"
    "的局曾经过席位错位评估通道（伪影，已勘误）。治理现状：/accept 自 09-01 起静默，"
    "事实权威源是 JOURNAL 详记 + git 提交 + metrics 分片。"
)
FN_DOCS_RESPONSIBILITY = (
    "现役提交链 bot 的等价迁移——十模块+planner/六模块迁入新包。"
    "分区处置：gym_env/llm_provider 移实验区；economy/redlines 移测试资产区。"
)
FN_DOCS_LEDGER = "重算台账：席位错位通道未回流——受影响历史结论双口径并列。"

# probes_state 假快照：6 份摘要全入库+规则面缺口（与真树实测同构）
PROBES_STATE = {
    "probes_dir": "<fake>",
    "summaries": [
        {"relpath": f"software/exports/probes/planner_bench/{n}.md",
         "tracked": True, "bytes": 1000 + i}
        for i, n in enumerate([
            "round23_loss_forensics", "round24_loss_forensics",
            "v31_pressure_calibration_summary", "v3_readmission_summary"])
    ] + [
        {"relpath": "software/exports/probes/v143_sellrace/v143_sellrace_summary.md",
         "tracked": True, "bytes": 2000},
        {"relpath": "software/exports/probes/v15_ignition/v15_ignition_summary.md",
         "tracked": True, "bytes": 3000},
    ],
    "data_intermediates": [
        {"relpath": "software/exports/probes/twin_fidelity/engine_cache", "tracked": False},
    ],
    "rule_ignores_new_summary_md": True,
    "gitignore_patterns": [
        "workspace/kaggriculture/software/exports/probes/*",
        "!workspace/kaggriculture/software/exports/probes/README.md",
    ],
}


def make_ticket(ticket_id: str, status: str) -> str:
    return (
        f"# {ticket_id}: {TICKET_NAMES[ticket_id]}\n\n"
        f"**What to build:** 假票面。\n\n"
        f"**Blocked by:** None\n\n**Status:** {status}\n\n- [ ] 条目\n"
    )


def build_fake_campaign(tmp_path: Path) -> Path:
    """构建假战役树（含 bc_track 票面+fn_docs 锚点记录+JOURNAL 假台账），返回战役根。"""
    campaign = tmp_path / "campaign"
    (campaign / "software" / "bc_track" / "issues").mkdir(parents=True, exist_ok=True)
    (campaign / "fn_docs").mkdir(parents=True, exist_ok=True)
    (campaign / "blueprint.md").write_text("# blueprint\n", encoding="utf-8")
    (campaign / "JOURNAL.md").write_text("\n".join(JOURNAL_ROWS) + "\n", encoding="utf-8")
    bc = campaign / "software" / "bc_track"
    (bc / "README.md").write_text(BC_README, encoding="utf-8")
    for tid, status in TICKET_STATUS.items():
        (bc / "issues" / f"{tid}-{TICKET_NAMES[tid]}.md").write_text(
            make_ticket(tid, status), encoding="utf-8")
    fn_docs = campaign / "fn_docs"
    (fn_docs / "README.md").write_text(FN_DOCS_README, encoding="utf-8")
    (fn_docs / "responsibility.md").write_text(FN_DOCS_RESPONSIBILITY, encoding="utf-8")
    (fn_docs / "recalculation_ledger.md").write_text(FN_DOCS_LEDGER, encoding="utf-8")
    return campaign
