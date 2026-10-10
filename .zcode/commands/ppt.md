---
description: 正式答辩 PPT（K-12）：/accept 通过后运行——内容简报（document 角色）→ ppt-master 双用户门生成 pptx；精修=人工改稿或 ppt-master（见 K-12 技能精修段）
---

# /ppt —— 答辩 PPT 正式产线入口

用法：`/ppt <cid>`（该战役 /accept 已通过、尚未 /archive）。编排细节见 `.zcode/skills/ppt-run/SKILL.md` K-12。

1. **前置闸门**：`<战役根>/acceptance/` 存在 result=pass 报告——否则拒绝并指回 `/accept`
2. **内容简报**：document 角色产 `<战役根>/docs/ppt_brief.md`（输入=报告+蓝图+验收记录+metrics.json；**数字只出自 metrics 键**）
3. **ppt-master**：Default 路线以简报为源；项目目录路由 `<战役根>/docs/ppt/`；**Gate1/Gate2 为用户门**（模板选择与规格锁定由你拍板，不跳过）
4. **产物核验**（pptx 存在 + 数字逐键可溯）→ JOURNAL 记行 + commit → 提示 `/archive`（精修段：人工改稿 / ppt-master / edit-native，见 K-12）

铁律：正式答辩 pptx **唯一产线**（Marp/K-06 仅波内草稿）；数字一律溯源 metrics.json；窗口外（accept 未过/已归档）拒绝运行；战役产物只落战役根（D14）。
