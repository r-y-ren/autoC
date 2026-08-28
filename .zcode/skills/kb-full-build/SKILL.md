---
name: kb-full-build
description: 一次性全量知识库构建（D11）：配额豁免、按波次推进、每波提交断点可续，完成后恢复增量 cron。当用户要求全量构建知识库时使用。
---

# K-10 kb-full-build：一次性全量构建（D11，2026-08-28 裁决）

与 K-08 的区别：K-08 是无人值守配额化增量；本技能是**有监督一次性全量**——token 不设上限、
配额豁免（ winners/patterns/tech_cards 不受 1 片/轮限制），但**质量门槛一分不降**
（引用纪律、min_signal、结构 lint、SPA 预抓规则、分片自检全部照常——全量≠全收）。

## 前置

1. 暂停慢循环 cron（删除 + 规格存 `docs/PENDING-CRON.md`，完成后恢复）——防止构建中途无人值守跑批闯入
2. `init_state --phase collect --by full-build`；全程保持在 collect 态分波推进，**每波一个 git commit**（波次即断点）
3. 并发仍 ≤ budget.max_subagents_per_batch=4（稳定性优先，不因全量放宽）

## 波次（W0→W5，顺序执行；每波开始前 TodoWrite 对齐）

- **W0 存量修补**：award_levels 回填缺项；结构 lint WARN 清零（frontmatter 归位/必备节补齐）
- **W1/W2 赛事深化**（数模→黑客松）：每赛 winners 按覆盖标准（award_levels 前两级、倒推三年）补齐 +
  patterns 六节首建/升格；SPA 站点先主会话预抓；扫描件先过 ocr_pdf.py
- **W3 技术卡全消**：真实跑 sync（arXiv+gh+HF）收割候选 → Hunter 分片处理活跃队列至清空
  （拒绝照常进 .rejections.yaml）
- **W4 surveys**：≥3 卡的每个技术族建/刷 `_surveys/`
- **W5 收尾**：全量 lint + --structure 零 WARN → build_index → 跑批记录（类型=full，成本列=全程合计）
  → 双方向简报 `--formal` → JOURNAL → commit+push → idle → **恢复 cron（按 PENDING-CRON.md）** → 删除该文件

## 完成标准（Definition of Done）

11 条目全部 award_levels + patterns 六节 + winners 覆盖或如实缺口声明；活跃候选队列清空；
每族 survey 就位；结构 lint 零 WARN；简报正式版；cron 已恢复。

## 中断恢复

波次结构即断点：中断后看 TodoList 与 git log 定位到波，从该波未完成分片继续（已提交部分不重做）。
