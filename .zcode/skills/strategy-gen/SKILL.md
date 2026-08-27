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

1. **矩阵评分**：对 INDEX 中候选赛事逐个打分（时间窗匹配 2–10 周最优 / 技术契合度=KB-2 卡片与该赛获奖模式重叠——**"大显身手"信号显式化：近 90 天入库新卡 × 该赛 patterns 方法论分布的命中，作为加权项** / 通吃度=同一作品可复投数 / 画像匹配 / 竞争密度），产出对比矩阵写入 `workspace/strategy.md`
2. **一鱼多吃路线**：识别复用组合（如数模作品→挑战杯论文通道→大创结题），标注各赛事截止时间与改造工作量
3. **蓝图草稿**：写 `workspace/blueprint.md`，frontmatter 必须含：
   - campaign / scope（deliverables + out_of_scope 显式排除）/ tech_stack（**每项引用 kb_tech_ids**）
   - interface_contracts（software↔hardware 协议、document 消费路径——并发分发前钉死）
   - milestones（owner_role ∈ {software, hardware, document}）/ acceptance.checklist（id/category/item/method，可机检项加 cmd）/ compliance（ai_policy_reviewed）
4. **校验**：`python scripts/kb/lint_kb.py --file workspace/blueprint.md`——不过不得呈报
5. **呈报**：矩阵 + 路线 + 蓝图要点呈用户确认（**全流程唯一人工闸门**）；要求修改则回到第 3 步
6. 确认后：JOURNAL 记行，交 K-03 campaign-run

## 纪律

推荐结论必须引用具体 KB 条目 ID，禁止凭印象；ACM 方向只出训练体系类蓝图；蓝图验收项中物理测试标 category=manual。
