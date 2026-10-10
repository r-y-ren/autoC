---
name: ppt-run
description: 正式答辩 PPT 产线（K-12，v2 两段式）：产稿段自动化（fn-ladder 取材→模板初稿），精修段可选（ppt-master 双用户门）。数据源=fn 实测产物，数字逐项可溯。当用户触发 /ppt 时使用。
---

# K-12 ppt-run：正式答辩 PPT 产线（v2 两段式，2026-10-09）

## 定位

- **窗口**：/accept 通过后、/archive 前（战役 verify 态；守卫对该态放行 `docs/` 子树）。
- **两段式**：
  - **产稿段（自动，零停等）**：取材器 + 叙事模板 → 五段初稿；
  - **精修段（可选）**：ppt-master Default 路线（Gate1/Gate2 用户门**保留**），输入=初稿+取材数据。
- **数据源改道（v2）**：数字只出自 **fn-ladder 实测产物**（`fn_work/runs/`、`fn_docs/results/`），
  经取材器提取并**逐项标注来源文件**；旧 metrics.json 溯源口径废止（metrics 降级为可选补充源）。
- **资产层复用**：叙事骨架（`config/templates/ppt/narrative-skeleton.md`）+ fn 取材映射
  （`fn-mapping.md`）+ 模板雏形（`deck-template.marp.md`）沉淀复用，不再从零画稿。

## 前置

1. 战役处于 verify 态且 /accept 已通过（`<战役根>/acceptance/` 存在 result=pass 的报告；否则拒绝并指回 /accept）
2. 项目根含 `fn_docs/` 与 `fn_work/`（fn-ladder 产物布局；缺件由取材器降级点名，不得占位顶替）
3. ppt-master 插件在位（仅精修段需要；SessionStart 播报缺失 → 先补装）；`contract_check` 无落后警示

## 流程

1. **取材**：`python scripts/ppt/collect_deck_material.py --project <战役根> --out-dir <战役根>/docs/ppt_material/`
   → `deck_material.json`（四段素材+带来源数据表）+ `deck_brief.md`（人读简报）；缺失项如实进 missing
2. **产稿**：`python scripts/ppt/build_draft_deck.py --material <战役根>/docs/ppt_material/deck_material.json --out <战役根>/docs/ppt/draft_deck.md`
   → 五段初稿（数字带来源脚注）；可用 Marp 渲染雏形：`marp <战役根>/docs/ppt/draft_deck.md -o <战役根>/docs/ppt/draft.pptx`
3. **精修（可选，两径任选）**：
   - **ppt-master 路线**：Default 路线，输入=draft+material——
     - **项目目录显式路由到 `<战役根>/docs/ppt/`**（D14：战役产物只落战役根；图片/模板资源同置于此）
     - Gate1（沟通契约+模板选择）与 Gate2（规格锁定）即**用户门**，⛔BLOCKING 须用户显式确认，不跳过
   - **人工径**：直接改稿，或走 ppt-master **原生 pptx 编辑路线**（edit-native，改既有 pptx 不重新生成）；
     **任何数字改动必须回 `deck_material.json` 来源标注核对（无来源数字不上片）**。
4. **产物核验**：`<战役根>/docs/ppt/exports/*.pptx`（或 draft.pptx）存在；**每个数字能在
   deck_material.json 的来源标注中找到**（无来源数字不得上片）。
5. JOURNAL 记行 + 项目仓库 commit → 提示：`/archive`（战役收尾）；精修段见上（两径任选）。

## 禁止

- 禁在窗口外运行（accept 未过 / 已 archive）；禁编造数字（一律来自取材器来源标注）；
  禁把 ppt 项目目录落到战役根之外；精修段禁绕过 ppt-master 自带用户门全自动导出。

## 备注

- Marp 产物归档时标"草稿"，不得与正式 pptx 混淆；换 PPT 工具时取材数据（deck_material.json）不作废。

## 产物说明（收尾必做，用户审阅口径）

执行完毕**必须**以「产物说明」收尾，逐项列出本次生成/修改文件的位置供用户审阅：

① `<战役根>/docs/ppt_material/deck_material.json` 与 `deck_brief.md`；② `<战役根>/docs/ppt/draft_deck.md`（及 `draft.pptx`/`exports/*.pptx` 如有）

无产物时明说「无产物（只读）」。
