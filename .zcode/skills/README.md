# .zcode/skills/ —— SOP 纯函数技能库（占位）

T2 起逐个落盘，与 `docs/CAPABILITIES.md` 的 K-01…K-07 一一对应：

| ID | 技能 | 职责 | 所属阶段 |
|---|---|---|---|
| K-01 | kb-sync | 慢循环编排（分片派发 C-01/C-02 → lint → 索引 → changelog） | 慢循环 |
| K-02 | strategy-gen | 对比矩阵 + 一鱼多吃 + 蓝图草稿（schema 校验后呈报） | 决策 |
| K-03 | campaign-run | 任务包拆解与并发派发（**落地前须重估：角色身份级守卫、metrics 分片汇总**，见 DESIGN §6.2 后置项） | 交付 |
| K-04 | accept-run | 验收执行与失败工单回环（熔断） | 验收 |
| K-05 | archive-run | 归档与复位 | 归档 |
| K-06 | marp-deck | 答辩 PPT 生成（模板 + metrics.json） | 交付·文档 |
| K-07 | typst-report | 项目报告生成（模板 + metrics.json） | 交付·文档 |
| K-11 | self-run | 人工主导交付会话（副驾模式，D13；/self 入口） | 交付·人工 |
| K-14 | compete-strategy | 对抗比赛从零制胜方法论（控制论十步）：六问读引擎→坐标分级→转移函数→资产化→净账闭环（references 六问导读+T1-T5 模板） | 决策·策略 |

约束：技能只承载流程（顺序与判断要点），不承载状态；状态一律落 `.flow/` 与 `workspace/JOURNAL.md`。新增技能先在 CAPABILITIES.md 登记。K-08 起的后续技能（K-08/K-09/K-10/K-11）以 `docs/CAPABILITIES.md` §3 技能表为登记主表。
