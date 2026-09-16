# 05: vault-distill 全量执行

**What to build:** 按 04 号票的 SOP 对 my_LLM_valut 全量执行：建独立分支（batch/vault-distill）、两台机器 cron 暂停、波次推进 384 页 wiki 的方向交集筛选提炼（断点可续）、完成后 lint 全绿 + INDEX 收录 + 拒绝台账完整、合并回 main、恢复 cron。

**Blocked by:** 04（管线与样本验证通过）

**Status:** ready-for-agent

- [ ] batch 分支建立，双机 cron 确认暂停
- [ ] 全量提炼完成，波次 commit 历史完整可续
- [ ] lint 0 不合格、INDEX 收录全部新卡、拒收台账完整
- [ ] 合并回 main 并 push，cron 恢复
