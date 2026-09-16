# 04: vault-distill 跑批管线与样本验证

**What to build:** my_LLM_valut 一次性提炼的执行管线就绪：跑批 SOP 技能文件（复用全量构建模式：独立分支、停双机 cron、配额豁免、按主题分片派发子 agent、波次 commit 断点可续、收录/拒绝落拒绝台账、按 kb directions 交集筛选——UAV/MEC→智慧农业、LLM 前沿→KB-2 雷达，raw 未编译论文原则上不提炼）；bib 回填辅助脚本（Zotero bib + citekey 映射 → 输出 论文标题→DOI/URL 映射供卡溯源用）；提炼卡强制填写 02 号票的 4 个枚举字段与论文标题。先用十余页样本+假 bib 试跑验证管线，全量执行留给下一票。

**Blocked by:** 02（tech-card 溯源升级——提炼卡的 schema 必须先存在）

**Status:** ready-for-agent

- [ ] 跑批 SOP 技能文件完整（分支/cron/豁免/分片/波次/断点/台账/筛选规则）
- [ ] bib 回填脚本对样本 bib 输出正确的标题→DOI/URL 映射
- [ ] 样本试跑 PASS：产物卡过 lint、正文标注论文标题、可回填项已回填、拒收落台账
- [ ] 拒收理由记录含方向交集判断依据（可审计）
