---
description: 参考方案供给：刷新 KB → 对比矩阵与方案书（赛事/方案/技术栈，纯参考）落 kb/briefs/；不影响推进
---

# /attack —— 参考方案供给（v2：纯参考）

用法：`/attack <赛事ID或方向描述>`（省略参数 = 询问建议）；`--to <战役根>` 可选把方案书复制进该项目 `docs/briefs/`。

执行流程（编排细节见 `.zcode/skills/strategy-gen/SKILL.md`）：

1. 先触发一次慢循环增量（K-01 流程）确保参考基于最新 KB
2. 读 `kb/INDEX.md` + `config/profile.yaml`（画像未填先提示用户）
2.5. **grilling 前置步**：以 KB 为语境对用户做完整 grilling（意图与优先级 / 时间窗与人力 / 范围边界 /
   技术栈偏好 / 一鱼多吃期望），纪要随方案书落 `kb/briefs/<同 slug>-grill-notes.md`
3. **方案书**：按 `config/templates/brief-template.md` **三节**产出——
   赛事（情报摘要回链条目 ID + 对比矩阵，每格标证据强度 + 大显身手信号行）/
   方案（一句话主张 + 一鱼多吃路线 + 范围边界 + 明确推荐结论）/
   技术栈（kb_tech_ids 引用 + 合规与风险 mode 判定）
4. 入库 `kb/briefs/<日期>-<赛事slug>-<方案slug>.md`，并在 `kb/briefs/README.md` 登记一行；
   `--to <战役根>` 时复制到 `<战役根>/docs/briefs/`
5. 摘要呈用户（**通知，非闸门**——方案书是参考信息，确认与否不影响任何流程）

铁律：方案书**禁止**包含 milestones / acceptance / 接口契约 / fn-ladder 需求种子——不得影响或
指挥后续推进；推荐结论须引用具体 KB 条目 ID，禁止凭印象；数据不足的维度如实降权告知，禁止硬推。
