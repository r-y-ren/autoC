---
name: marp-deck
description: 答辩 PPT 波内草稿生成（升级票10 降级定位）：从 Marp 模板与汇总指标生成快速迭代演示草稿。正式答辩 pptx 唯一产线为 K-12 /ppt（ppt-master）。当 Document 角色需要波内草稿、或用户要求快速演示材料时使用。
---

# K-06 marp-deck：答辩 PPT 波内草稿生成

> **定位（升级票10，2026-09-16）**：本产线自 K-12 落地起定位为**波内草稿**——数字溯源快稿、/accept 审阅辅助、内参迭代。正式答辩 PPT 由 `/ppt`（K-12，ppt-master 双用户门）产出；归档时本线产物标注"草稿"，不得与正式 pptx 混淆。

## 前置

- `workspace/<cid>/metrics.json`（汇总生成物）存在；否则先 `python scripts/verify/merge_metrics.py`
- marp-cli 可用（`marp --version`）；缺失时提示安装：`npm install -g @marp-team/marp-cli`（E-01），不擅自替代为手工 pptx

## 流程

1. 复制 `config/templates/presentation.marp.md` → `workspace/<cid>/docs/deck.md`
2. 按章节填充：
   - 数字**只能**引用 `metrics.<role>.<键>`，文内注释标键名；禁止出现 metrics 之外的数字
   - 架构图用 diagram-maker 生成后以图片引用
   - 与历年获奖基准对比：经 kb/INDEX.md 定位该赛 patterns.md 后引用其结论（注明条目 ID）
3. 导出：`marp workspace/<cid>/docs/deck.md -o workspace/<cid>/docs/deck.pptx --pptx`（同时可导出 PDF 版备份）
4. 自检：页数 ≤ 限额（按赛事要求）、每页有且仅有一个论点、数字均带来源键；不满足回到第 2 步

## 纪律

模板结构（问题/方案/架构/实测/对比/展望）不得删节；缺口上报而非私改模板。

## 产物说明（收尾必做，用户审阅口径）

执行完毕**必须**以「产物说明」收尾，逐项列出本次生成/修改文件的位置供用户审阅：

① `<战役根>/docs/deck.md`（波内草稿）；② 渲染产物 `deck.pptx`/`deck.html`（如有，归档时标『草稿』）

无产物时明说「无产物（只读）」。
