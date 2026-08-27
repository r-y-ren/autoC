# 待注册：每周深度评估 cron（本会话已绑定另一自动化，无法二次创建）

> 下次新会话中执行（或请用户说"注册每周深度 cron"）：
> CronCreate：cron=`0 9 * * 6`，recurring=true，title=`autoC 每周深度评估（kb-deep-sync，周六 09:00）`

prompt 内容（可直接粘贴）：

```
执行 autoC 工作区（C:\Users\OSS\Desktop\autoC）的每周深度知识库评估。SOP 见 .zcode/skills/kb-deep-sync/SKILL.md（K-08），要点：
1) python scripts/guard/init_state.py --phase collect --by kb-deep-sync；
2) 老化重验：last_verified 超 14 天的 KB 条目派发 scraper 分片重验（重点关键日期/ai_policy）；
3) 复核 kb/tech/.rejections.yaml 拒绝台账质量，明显误拒的标记下轮重评；
4) 处置 kb/quarantine/ 隔离条目（修复或删除并记录）；
5) winners/patterns 推进：选 1-2 个赛事推进历年获奖解构（扫描件先过 scripts/kb/ocr_pdf.py，模板在 config/templates/patterns-template.md）；单分片 token 预算注意——T3-c 实测 winners 样板约 8M tokens/43min，一次只推进一个年份分片；
6) python scripts/kb/build_index.py 重建索引（跑批表自动保留）→ INDEX 跑批记录追加（类型=deep）→ workspace/JOURNAL.md 记行 → git commit → init_state --phase idle。
纪律：遵守 AGENTS.md（引用纪律/分片/不读 raw 进主上下文）；宁缺毋滥；与每日轻量 cron 冲突时以本深度评估为准。若无老化条目且无需推进项，记录一行后直接回 idle。
```

注册完成后删除本文件。
