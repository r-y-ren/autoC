---
competition_id: mlh-hack-the-north
last_verified: 2026-08-28
coverage: [2025-partial]   # 仅 1 个已证实获奖项目（DUM-E）深构；完整名单不可达
confidence: 低             # 单项目样本 + 官方奖项结构；完整 winners 数据缺口
sources:
  - url: https://hackthenorth.com/prizes
    title: 官方奖项页（主奖/新手奖双轨结构）
    accessed: 2026-08-28
  - url: https://hackthenorth.com/faq
    title: 官方 FAQ（expo 评审制/项目边界/团队规则）
    accessed: 2026-08-28
  - url: https://devpost.com/software/dum-e-kgx6at
    title: DUM-E 项目页（唯一深构样本）
    accessed: 2026-08-28
---

# Hack the North 模式库（patterns）

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- 评审制为 **expo 巡展 + Top-10 闭幕式现场 demo**（FAQ 原文）——现场演示与讲台叙事的权重显著高于书面材料。（官网级）
- 作为 MLH 赛季成员赛事适用 MLH 四等权标准 Technology / Design / Completion / Learning，明示不评代码质量/演讲原创性/实际用处——**"完成度与学习曲线"本身就是得分项**。（MLH 规则原文，官网级）
- 奖项结构显式鼓励新手：Beginner Prizes 独立赛道（≤2 场经验）且可与主奖兼得——主办方取向是参与梯度而非纯竞技。（官网级）

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| 多模态 LLM 空间决策（视觉坐标→动作） | 1/1（单样本，无代表性） | 2025：DUM-E | 中-高：可降级为 UI 坐标 agent |
| 快推理服务控延迟（Groq） | 1/1 | 2025：DUM-E | 高：API 即插即用 |
| 开源件套快速原型（Arduino+RPi+OpenCV+Whisper） | 1/1 | 2025：DUM-E | 高：件套成本低 |
| 软硬结合的 expo 叙事（真机演示） | 1/1 | 2025：DUM-E | 中：硬件调试时间盒风险 |

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 样本不足，**无法从实证名单归纳**（2025 完整名单不可达）——此节宁缺毋滥。
- 唯一可观察：DUM-E 类"现场可动起来的真机"项目进入官方画廊 Winner 位与官网首页往期展示位——实物演示的传播价值明确。（官网级，n=1）

## 四、反面观察（常见失分模式，若有依据）

- 规则红线（FAQ 原文）："Teams are expected to have done no work prior to the hackathon"——赛前成品参战属违规；可行准备物限 wireframes/schematics/pseudocode/mockups/slides。（官网级）
- 团队上限 4 人（FAQ）。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] Technology：核心技术链路（感知→决策→执行）在 demo 中可见端到端跑通
- [ ] Completion：36 小时内可演示的最小完整闭环（非半成品 API 拼装）
- [ ] Learning：提交叙事包含"团队新学了什么"显式段落（MLH Learning 权重）
- [ ] Design：交互入口（语音/触控）与反馈闭环可被 expo 观众 30 秒理解
- [ ] 现场：expo 讲稿 + 决赛 2 分钟 demo 双版本准备（Top-10 突发晋级）
- [ ] 合规：赛前零成品，仅携带设计类文件；团队 ≤4 人
- [ ] 新手队：若成员经验 ≤2 场，双投主奖+Beginner 赛道

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：北美线下旗舰，2026 届申请已关闭（07-17）——本季无参赛窗口；价值在 **2027 届申请窗口监控**与 expo 型评审的作品呈现策略样本。
- 作品工程要点：软硬/多模态 demo 的"现场可动"标准是我方验收清单可借鉴的 Completion 操作化定义。
- 合规栈：MLH 规则无 AI 限制条款，"AI 辅助原创"合规压力低；红线是赛前零代码。
- 数据管线教训：hackthenorth 官方站 past-winners 页存在渲染污染实证（Ascentra 事故，已证伪弃用）——该站名单必须以 Devpost 赛站原件为准并双源核对。
