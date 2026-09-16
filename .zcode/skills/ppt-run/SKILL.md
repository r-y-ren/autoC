---
name: ppt-run
description: 正式答辩 PPT 产线（K-12，升级票10）：/accept 通过后、/archive 前，先由 document 角色从项目文档总结内容简报（数字只出自 metrics），再走 ppt-master 双用户门生成正式答辩 pptx。当用户触发 /ppt 时使用。
---

# K-12 ppt-run：正式答辩 PPT 产线（升级票10，2026-09-16）

## 定位

- **窗口**：/accept 通过后、/archive 前（战役 verify 态；守卫对该态放行 `docs/` 子树——升级票10 的等价"post-accept 子态"）。
- **产线唯一性**：正式答辩 pptx 只由本技能产出；Marp（K-06）自本票起定位为**波内草稿**（数字溯源快稿、/accept 审阅辅助），归档不出现两份正式 PPT。
- **内容简报是战役归档物**：人机分工留痕、数字可溯源自 metrics.json（铁律 4），换 PPT 工具不用重写。

## 前置

1. 战役处于 verify 态且 /accept 已通过（`<战役根>/acceptance/` 存在 result=pass 的报告；否则拒绝并指回 /accept）
2. ppt-master 插件在位（SessionStart 播报缺失 → 先补装再运行）
3. `python scripts/guard/contract_check.py` 无落后警示

## 流程

1. **内容简报**：派 document 子 agent 写 `<战役根>/docs/ppt_brief.md`——
   - 输入=最终报告 + `blueprint.md` + 验收记录 + `metrics.json`（**数字只出自 metrics 键**，禁编造/估算）
   - 结构：受众与时长 / 核心主张线 / 逐页要点（含 `metrics.<role>.<键>` 引用）/ 图表清单与数据来源 / 风险与 Q&A 预案
   - 该职责以**任务包条款**下达（document 章程的正式措辞更新待用户提交其未提交改动后一并补录，行为以本任务包为准）
2. **ppt-master 生成**：调用 ppt-master 技能（Default 路线），以 ppt_brief.md 为输入源——
   - **项目目录显式路由到 `<战役根>/docs/ppt/`**（D14：战役产物只落战役根；图片/模板资源同置于此）
   - Gate1（沟通契约+模板选择）与 Gate2（规格锁定）即**用户门**，如实走完不跳过；⛔BLOCKING 门须用户显式确认
3. **产物核验**：`<战役根>/docs/ppt/exports/*.pptx` 存在；ppt_brief 每个数字能在 metrics.json 中找到对应键。
4. JOURNAL 记行 + git commit → 提示：`/archive`（战役收尾）或 `/ppt-self`（细节微调副驾）。

## 禁止

- 禁在窗口外运行（accept 未过 / 已 archive）；禁绕过 ppt-master 自带用户门全自动导出；禁编造数字（一律回 metrics）；禁把 ppt-master 项目目录落到战役根之外。

## 备注

ppt-master 不依赖 document-skills（自带脚本链）；Marp 产物如已存在于 docs/，归档时标注"草稿"不得与正式 pptx 混淆。
