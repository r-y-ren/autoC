---
id: gh-Zyrexnn_Cybermes
name: "Cybermes: 自主进攻安全/赏金自动化 Agent 框架"
field: [LLM agents, 网络安全自动化]
directions: [黑客松与数据竞赛]
published: "2026-08-19"
maturity: demo
signal:
  venue: GitHub
  stars: 617
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "AI 安全类黑客松（AI4Security/安全自动化赛道）的现成项目底座：LLM agent 编排（Hermes）+ 200+ 漏洞 SOP 知识库 + Go 高速流过滤（smart_pipe）+ 零误报 PoC 验证门 + 自动结构化报告（MD/JSON/HTML/PDF），比从零拼装侦察-扫描-验证-报告链路省 2-3 天；自带 mock 靶机可在赛场合法演示全闭环，'每个发现必须带可复现非破坏 PoC + 原始 HTTP 证据'的验证门设计是评委可感知的工程亮点"
    reuse_cost: "低"
    open_source: "https://github.com/Zyrexnn/Cybermes（Apache-2.0，Docker/一键安装/npm cybermes-mcp 3.2.0）"
sources:
  - url: https://github.com/Zyrexnn/Cybermes
    title: "Zyrexnn/Cybermes: Autonomous Offensive Security, Bug Bounty & Red Teaming Agent Framework"
    accessed: "2026-08-28"
  - url: https://api.github.com/repos/Zyrexnn/Cybermes
    title: "GitHub API 仓库元数据（stars/许可/创建时间快照）"
    accessed: "2026-08-28"
---

# Cybermes：LLM 编排的自主进攻安全与赏金自动化框架

## 是什么

Zyrexnn 于 2026-08-19 创建的开源框架（Python + Go，Apache-2.0），面向**授权的**赏金挖掘、侦察、漏洞研究与结构化报告：以 Hermes Agent 作自主决策环，经 MCP 工具调用驱动五段闭环管线——推理编排 → 侦察（subfinder/httpx/katana/ffuf）→ 分析与技能执行（209 个漏洞 SOP playbook 实测于 skills/ 目录，2026-08-28 实抓 API 确认；离线知识库 sub-50ms 检索 PayloadsAllTheThings/HackTricks）→ **零误报验证门**（每个发现必须生成可独立运行的非破坏 PoC 脚本并附原始 HTTP 证据链）→ 多格式报告（SUMMARY.md/metadata.json/交互 HTML/PDF）。原生 Go MCP 服务器（cybermes-mcp，npm 已发 3.2.0，2026-08-28 registry 实查）把 10+ 安全工具直接暴露给 Claude Code/Cursor/Gemini 等 AI 客户端（来源：https://github.com/Zyrexnn/Cybermes README 实抓 2026-08-28）。

## 解决什么问题

AI 助手做安全测试的三大痛点：fuzzer/爬虫输出淹没上下文（千行 404 噪声）、模式匹配式告警不可复现（无 PoC 验证）、结果是无结构文本堆（报告要手工整理）。Cybermes 用 Go 流过滤 + 强制 PoC 门 + 报告聚合器分别堵住三个漏点。

## 相比前方法优势

- 相比手工 Burp+nuclei 流程：agent 自主决策攻击路径，200+ SOP 知识库离线可查；
- 相比裸 LLM 对话式安全助手：MCP 工具化（非复制粘贴终端输出）+ 验证门消灭幻觉式漏洞报告；
- 相比同类 agent 框架：Windows 原生支持（多数进攻工具假设 Kali）+ doctor.py 环境自检自修 + Docker 全平台（README 对比表，2026-08-28 实抓）。

## 局限（如实标注）

- **仅限授权测试**：README 法律声明明确禁止未授权目标；赛场演示只能用自带 mock 靶机（examples/mock_vulnerable_app.py）或主办方授权环境——任何赛题方案都必须守住此边界；
- 9 天龄 617 star 属高增长，但非纯营销：仓库实质核实（209 playbooks、cmd/ 下 5 个 Go 工具源码、CI/Docker workflow、外部贡献者 PR #1/#4/#5 已合并），maturity 仍按 demo 标注；
- 依赖外部工具链（subfinder/katana/nuclei/sqlmap 等）与 LLM API key，赛场网络受限时需预装；
- 仓库 165MB（含知识库数据集），克隆与镜像成本高。

## 如何用于比赛

1. **AI 安全主题黑客松（主用）**：以 Cybermes 为底座做"自动渗透测试报告生成器"或"AI 红队助手"类作品：对自带 mock 靶机跑全闭环，答辩展示"侦察→发现→PoC 证据→PDF 报告"全自动链路；差异化点押在**零误报验证门**（多数同类作品止步于扫描器套壳，无证据链）。reuse_cost 低：Docker compose 或 npx 一键装，mock 靶机开箱即用（来源：README 安装节，抓取 2026-08-28）。
2. **攻防对抗类赛题**：防守方视角反向使用——用其报告结构（findings 分级 + metadata.json 计数器）作为自方漏洞治理看板的数据底座。
3. 合规红线：Apache-2.0 允许比赛使用；但按本仓 AGENTS.md 底线，禁止生成针对未授权目标的提交策略，方案书必须写明测试范围授权来源。
