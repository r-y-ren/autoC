---
campaign: {competition_id: cala-hacks-ai-2026, name: "LA Hacks AI Hackathon 2026（E2E 彩排靶）", theme: 数据叙事小工具（prep 范本）}
scope:
  deliverables: [数据统计 CLI（读 CSV 输出统计 JSON）, 一页项目报告（PDF）, 答辩 PPT（正式产线产物）]
  out_of_scope: [真实报名与投递, 云端部署, 多用户/网络功能, 第三方依赖（仅 Python stdlib）]
tech_stack:
  - name: python-stdlib-cli
    kb_tech_ids: []
    rationale: 彩排最小闭环，零依赖可自检
    reuse_cost: 低
interface_contracts:
  - {between: [software, document], contract_file: interface/contract.md}
milestones:
  - {id: m1, task: "数据统计 CLI + 样例数据 + 接口契约 + metrics 分片（含报告数字核验脚本）", owner_role: software}
  - {id: m2, task: "一页报告（Typst→PDF，数字只引 metrics 键）", owner_role: document, depends_on: [m1]}
acceptance:
  checklist:
    - {id: a1, category: software, item: "CLI 对样例 CSV 输出统计 JSON 且自检退出码 0", method: exec, cmd: "python /mnt/data/Code/autoC/workspace/e2e-rehearsal-2026/software/stats_cli.py --csv /mnt/data/Code/autoC/workspace/e2e-rehearsal-2026/references/data/sample.csv --check"}
    - {id: a2, category: software, item: "CLI 单元测试全过", method: exec, cmd: "python -m unittest discover -s /mnt/data/Code/autoC/workspace/e2e-rehearsal-2026/software/tests -v"}
    - {id: a3, category: document, item: "报告 PDF 存在且其中数字逐键命中 metrics.json", method: exec, cmd: "python /mnt/data/Code/autoC/workspace/e2e-rehearsal-2026/software/check_report.py"}
compliance: {ai_policy_reviewed: true, mode: prep}
workflow: {auto_chain: true}
---

# 彩排蓝图：数据叙事小工具（E2E rehearsal）

## 范围与交付物

1. **stats_cli.py**：读取 CSV → 输出统计 JSON（行数/列数/数值列均值与最大值），`--check` 自检模式输出退出码。
2. **一页报告**：Typst 源 → PDF；数字只引 `metrics.software.*` 键。
3. **答辩 PPT**：走 K-12 /ppt 正式产线（document 简报 → ppt-master）。

## 里程碑与波次

- W1：m1（software）——CLI + tests + sample.csv（references/data/ 落位并登记 INDEX）+ interface/contract.md + software/metrics.json 分片 + check_report.py。
- W2：m2（document）——Typst 报告消费 m1 产物与 metrics。

## 验收口径

a1/a2/a3 见 frontmatter checklist（全部可机检 cmd）。manual 项：无（纯软件彩排）。

## 人机分工

agent 产全部工程物；用户参与：蓝图确认（decide 闸门）、ppt-master Gate1/Gate2（K-12 用户门）。
