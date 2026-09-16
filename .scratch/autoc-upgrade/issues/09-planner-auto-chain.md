# 09: planner 角色与 K-03 自动链编排

**What to build:** 蓝图确认且 auto_chain 开启时，/deliver 首波前派发新增的 planner 子 agent 跑 to-spec → to-tickets（mattpocock 技能，子 agent 内调用），产物落 `workspace/<cid>/specs/`；ticket 按 milestone × owner_role 归组为任务包派发实现，直通到 implement 完成后单次汇报（无中途人工门）。波次拓扑仍由蓝图 milestones 依赖关系决定（ticket 不改变拓扑），验收项 ID 前缀仍出自蓝图。software 角色章程加入自检前置条款（superpowers verification-before-completion / TDD 纪律：自检通过才报波门；波门五查继续兜底跨包契约，不加互审）。

**Blocked by:** 08（开关存在且可被编排消费）

**Status:** ready-for-agent

- [ ] planner 章程就位（.zcode/agents/），可在子 agent 内调用 mattpocock to-spec/to-tickets
- [ ] K-03 流程：首波前派发 planner，specs/ 产物落战役根
- [ ] ticket 按 milestone×owner_role 归组；波次拓扑不变；验收 ID 前缀出自蓝图
- [ ] 自动链直通完成后单次汇报（中间无人工停顿点）
- [ ] software 章程含自检前置条款；/accept 仍是唯一人工验收门
