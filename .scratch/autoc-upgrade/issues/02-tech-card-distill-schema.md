# 02: tech-card 溯源升级（提炼卡 schema）

**What to build:** kb 技术卡支持深度精读来源：tech-card schema 新增 4 个可选受控枚举字段 `venue_tier / evidence_tier / paper_role / reproducibility_level`（移植自 my_LLM_valut 词表），sources 支持 paper-distill 形态（论文标题必填，doi/url 可选，distilled_from/distilled_date 标记来源与日期）。存量 90+ 卡零迁移（不填合法）。同时把铁律 1"URL+抓取日期"的受控放宽边界（仅限 vault-distill 跑批使用 paper-distill 形态）写入 AGENTS.md。

**Blocked by:** None（可立即开工）

**Status:** ready-for-agent

- [ ] schema 含 4 个可选枚举字段，取值域受控（负例：非法枚举值被 lint 隔离）
- [ ] sources 支持 paper-distill 形态：合法样例卡过 lint，缺论文标题被拒
- [ ] 存量卡在未改动的情况下全部继续通过 lint（零迁移验证）
- [ ] AGENTS.md 铁律 1 的放宽边界成文（适用范围仅限提炼跑批）
