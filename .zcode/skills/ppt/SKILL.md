---
name: ppt
description: 答辩 PPT 产线入口（/ppt）：两段式——fn 取材→模板初稿（数字带来源），精修可选。当用户要生成答辩 PPT 时使用。
---

# ppt：命令入口壳（注册适配）

本技能是 `.zcode/commands/ppt.md` 命令的**同名斜杠入口壳**（客户端 `/` 菜单只认技能名，命令文档不参与技能注册——2026-10-10 评审补口）。薄壳不复制流程：

按 `.zcode/commands/ppt.md` 流程执行；编排细节调用 ppt-run 技能（K-12）。

## 产物说明（收尾必做，用户审阅口径）

产物说明：① `<战役根>/docs/ppt_material/deck_material.json` 与 `deck_brief.md`；② `<战役根>/docs/ppt/draft_deck.md`（及 pptx 如有）。
