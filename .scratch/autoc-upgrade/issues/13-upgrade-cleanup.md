# 13: 升级收尾（清理+钩子恢复）

**What to build:** 两线落地并彩排通过后的收尾：删除升级过程临时产物（`.scratch/autoc-upgrade/` 票据；spec 按用户留痕决定去留）；.zcode/config.json 三个钩子恢复 enabled:true 并 commit+push（另一台机器 pull 后守卫恢复，需用户在彼端验证一次）；契约版本终检；JOURNAL/DESIGN/CAPABILITIES 对新 K 条目（K-12/K-13）与 planner 角色的收录核对完整。

**Blocked by:** 06、12（A 线终局 + B 线彩排全通过）

**Status:** ready-for-agent

- [ ] `.scratch/autoc-upgrade/` 已删除；spec 去留按用户决定执行
- [ ] config.json 钩子恢复启用，已 commit+push
- [ ] 契约版本终检一致（schema/脚本/播报三方同版）
- [ ] CAPABILITIES/DESIGN/JOURNAL 收录核对无缺漏
- [ ] 提醒用户在另一台机器 pull 并验证守卫恢复
