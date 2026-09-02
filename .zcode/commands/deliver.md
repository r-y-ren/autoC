---
description: 交付入口：按已确认蓝图启动波次化制作（K-03 编排；多会话工作流中"制作会话"的起点）
---

# /deliver —— 交付会话入口

用法：在**新会话**中执行 `/deliver`（蓝图已在决策会话经你确认）。若蓝图未确认，本命令会拒绝并指回 `/attack`。想自己动手、由人指挥主会话直接干活的，改用姊妹入口 `/self`（K-11 副驾模式；两入口同处 deliver 阶段，可随时互换续跑）。

执行流程（编排细节见 `.zcode/skills/campaign-run/SKILL.md` K-03）：

1. **前置闸门**：读 `workspace/blueprint.md`——缺失或未过校验 → 指回 /attack；`compliance.mode=assist` → 拒绝启动交付（该模式无新作品战役）；mode=apply → 申报附件列入 document 任务包
2. **波次计算**：按 milestones 的 depends_on 拓扑分层（环 → 停止修蓝图）；轻蓝图自然单波
3. **逐波交付**：波内按角色并行派发（含"返回前自检 PASS"条款）+ 波门五查（验收项左移 `run_acceptance --only <前缀>` / 可编译测试 / 接口契约 / metrics 分片落盘 / JOURNAL+commit）——**波门即断点**，可跨会话接续（新会话说"继续交付"即从断点波续跑）
4. 末波：merge_metrics 汇总 → document 成稿（数字只引 metrics 键）
5. 提示执行 `/accept`（可在本会话继续，也可开会话 ④）

铁律：禁改蓝图（问题回 /attack 走重新确认）；波门不过不进下一波；scoped 验收不算终验。
