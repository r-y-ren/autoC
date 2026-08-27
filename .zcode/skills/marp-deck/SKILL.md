---
name: marp-deck
description: 答辩 PPT 生成：从 Marp 模板与汇总指标生成竞赛答辩演示文稿并导出 pptx。当 Document 角色需要产出 PPT、或用户要求生成演示材料时使用。
---

# K-06 marp-deck：答辩 PPT 生成

## 前置

- `workspace/metrics.json`（汇总生成物）存在；否则先 `python scripts/verify/merge_metrics.py`
- marp-cli 可用（`marp --version`）；缺失时提示安装：`npm install -g @marp-team/marp-cli`（E-01），不擅自替代为手工 pptx

## 流程

1. 复制 `config/templates/presentation.marp.md` → `workspace/docs/deck.md`
2. 按章节填充：
   - 数字**只能**引用 `metrics.<role>.<键>`，文内注释标键名；禁止出现 metrics 之外的数字
   - 架构图用 diagram-maker 生成后以图片引用
   - 与历年获奖基准对比：经 kb/INDEX.md 定位该赛 patterns.md 后引用其结论（注明条目 ID）
3. 导出：`marp workspace/docs/deck.md -o workspace/docs/deck.pptx --pptx`（同时可导出 PDF 版备份）
4. 自检：页数 ≤ 限额（按赛事要求）、每页有且仅有一个论点、数字均带来源键；不满足回到第 2 步

## 纪律

模板结构（问题/方案/架构/实测/对比/展望）不得删节；缺口上报而非私改模板。
