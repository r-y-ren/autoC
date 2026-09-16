# 12: 端到端彩排战役（主力验证缝）

**What to build:** B 线全部落地后，用一次性小战役走完整新链路做行为验收：/attack 完整 grilling → 蓝图（含 auto_chain 开关呈报与确认）→ /deliver planner 派发 + 自动链 + 包级自检 → /accept → /ppt 全流程。彩排产物落彩排战役根，结束后按当时纪律清理或归档。

**Blocked by:** 11（传递覆盖 07–10 全部 B 线能力）

**Status:** ready-for-agent

- [ ] 彩排战役从 grill 到 ppt 全链路走通，无中途人工门之外的停顿
- [ ] specs/、自检记录、ppt_brief.md、pptx 产物齐备且落位正确
- [ ] /accept 清单全 PASS；数字溯源全部命中 metrics.json
