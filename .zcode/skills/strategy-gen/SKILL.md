---
name: strategy-gen
description: 决策阶段：读取 KB 索引与团队画像，产出建议赛道对比矩阵、一鱼多吃路线与作品蓝图（schema 校验后呈报用户确认）。当用户触发 /attack、要求推荐比赛或制定参赛方案时使用。
---

# K-02 strategy-gen：推荐与蓝图生成

## 输入

- `kb/INDEX.md`（唯一入口；需要细节时按索引定位到条目再精读）
- `config/profile.yaml`（未填写则先向用户收集，或声明按"通用学生队低配"假设）
- 用户指定：赛事 ID 或方向描述

## 流程

1. **矩阵评分**：对 INDEX 中候选赛事逐个打分（时间窗匹配 2–10 周最优 / 技术契合度=KB-2 卡片与该赛获奖模式重叠——**"大显身手"信号显式化：近 90 天入库新卡 × 该赛 patterns 方法论分布的命中，作为加权项** / 通吃度=同一作品可复投数 / 画像匹配 / 竞争密度），产出对比矩阵写入 `workspace/strategy.md`。**每格标注证据强度**（该赛 patterns 有/无、KB-2 卡数）——证据不足的维度如实降权并在呈报时告知"该维度基于有限数据"，禁止假装有依据（当前多数赛事尚无 patterns，首跑建议引擎必然半饿，诚实亮边界）
2. **攻略标准化（D10）**：strategy.md 按 `config/templates/strategy-template.md` 六节产出——情报摘要（逐条回链条目 ID）/ 六维矩阵 / 大显身手信号行（具体卡片 ID）/ 一鱼多吃路线 / **合规与风险（mode 判定：prep/apply/assist，依据该赛 ai_policy 原文）/ 推荐结论（明确推荐第一名 + 理由；无可推荐窗口时诚实兜底，禁止硬推）**
3. **蓝图草稿**：按 `config/templates/blueprint-template.md` 骨架写 `workspace/blueprint.md`——验收清单默认抄模板的分类型默认线（软件一键启动/测试全过/实测取证；文档编译+数字一致；硬件编译+仿真断言+物理项 manual——"完整可实用"四标准：可运行/可验证/可维护/可交付）；frontmatter 必含：
   - campaign / scope（deliverables 逐项对齐该赛 meta.deliverables + out_of_scope 显式排除）/ tech_stack（**每项引用 kb_tech_ids**）
   - interface_contracts（software↔hardware 协议、document 消费路径——并发分发前钉死）
   - milestones（owner_role ∈ {software, hardware, document}）/ acceptance.checklist（id/category/item/method，可机检项加 cmd，样板见 config/templates/acceptance-cmds.md）/ compliance（**mode 三分 + apply/assist 必附 policy_basis 原文摘引**，schema 硬校验）
4. **校验**：`python scripts/kb/lint_kb.py --file workspace/blueprint.md`——不过不得呈报
5. **呈报（D10 口径：矩阵+明确推荐）**：四块固定格式——①六维矩阵（每格一句证据）②大显身手信号行 ③一鱼多吃路线图 ④推荐结论（明确第一名+理由+备选）——呈用户确认（**全流程唯一人工闸门**）；要求修改则回到第 3 步
6. 确认后：JOURNAL 记行，交 K-03 campaign-run

## 纪律

推荐结论必须引用具体 KB 条目 ID，禁止凭印象；ACM 方向只出训练体系类蓝图；蓝图验收项中物理测试标 category=manual。
