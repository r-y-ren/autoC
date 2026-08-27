---
description: 发起快循环：刷新 KB → 决策（矩阵/建议/攻略+蓝图）→ 等待用户确认
---

# /attack —— 快循环入口

用法：`/attack <赛事ID或方向描述>`（省略参数 = 询问建议）。

执行流程（编排细节见 `.zcode/skills/strategy-gen/SKILL.md`）：

1. 先触发一次慢循环增量（K-01 流程）确保决策基于最新 KB
2. 读 `kb/INDEX.md` + `config/profile.yaml`（画像未填先提示用户）
3. **攻略（strategy.md）**：按 `config/templates/strategy-template.md` 六节产出——情报摘要（回链条目 ID）/ 六维矩阵（**每格标证据强度**）/ 大显身手信号行（近 90 天 KB-2 新卡命中）/ 一鱼多吃路线 / 合规与风险（**mode 三分判定**）/ 推荐结论
4. **蓝图（blueprint.md）**：按 `config/templates/blueprint-template.md` 骨架——验收清单抄分类型默认线（"完整可实用"四标准）；`compliance.mode` ∈ prep/apply/assist（apply/assist 须附政策原文，schema 硬校验）
5. `python scripts/kb/lint_kb.py --file workspace/blueprint.md` 校验，不过不得呈报
6. **呈报（D10：矩阵+明确推荐）**：四块固定格式——六维矩阵 / 大显身手信号 / 一鱼多吃路线图 / **推荐第一名+理由+备选**——呈用户确认（全流程唯一人工闸门）；要求修改则改后重新校验呈报
7. 确认后交由交付编排（campaign-run，K-03）接管；mode=assist 的蓝图不会启动作品构建（K-03 闸门拦截）

铁律：蓝图未过 schema 校验禁止请求确认；推荐结论须引用具体 KB 条目 ID，禁止凭印象；数据不足的维度如实降权告知，禁止硬推。
