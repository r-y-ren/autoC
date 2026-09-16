# 03: inbox 外来资料投递与消费

**What to build:** 维护者把任意资料丢进 `kb/inbox/`（可选伴随同名 `*.meta.yaml` 写 source_url/dropped_at/备注/意向方向），下次 K-01 手动 sync 或 K-08 深跑的 collect 态跑批自动检查并消费：赛事章程类→匹配条目 enrichment 或新条目候选；论文/技术类→技术卡候选队列走正常清洗链；无法归类→`kb/raw/leads/` 暂存。缺 sidecar 的文件不拒收，标"未溯源"只进 raw 当线索、永不晋级可引用条目，跑批报告点名催补。每轮消费受 budget.yaml 配额，剩余文件保留到下轮。资料涉及活跃战役时仅在报告提示，不自动改动战役。目录含 README.md 说明约定。

**Blocked by:** 01（多机协作地基——.gitignore 条目与协作节对 inbox 的引用）

**Status:** ready-for-agent

- [x] `kb/inbox/` + README 就位；无 sidecar 文件不被拒收
- [x] fixture 三用例断言：全 meta→候选队列；缺 meta→raw 线索+报告点名；超配额→剩余保留
- [x] 三分路由行为正确（章程→条目增补/新候选、论文→技术卡候选、不可归类→leads+点名）
- [x] 与活跃战役关键词匹配的文件在报告中出现提示，战役 references/ 未被自动改动
- [x] K-01 与 K-08 技能文档含 inbox 检查步骤
