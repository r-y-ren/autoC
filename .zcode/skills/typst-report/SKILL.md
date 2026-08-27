---
name: typst-report
description: 项目报告生成：从 Typst 模板与汇总指标生成竞赛项目报告 PDF。当 Document 角色需要产出报告、或用户要求生成项目文档时使用。
---

# K-07 typst-report：项目报告生成

## 前置

- `workspace/metrics.json`（汇总生成物）存在；否则先 `python scripts/verify/merge_metrics.py`
- typst 可用（`typst --version`）；缺失时提示安装：`winget install --id Typst.Typst`（E-02）
- 该赛事申报书等**格式化 Office 文档**需求不在本技能范围——复用 document-skills（docx/pptx/pdf/xlsx）

## 流程

1. 复制模板 → `workspace/docs/report.typ`：通用赛事用 `config/templates/report_template.typ`；**数模类战役（CUMCM/美赛/MathorCup）用 `config/templates/report-cumcm.typ` 变体**——已内置该赛格式规范结构（承诺书/编号页/摘要页≤1页/正文≤30页/AI 工具使用声明节/匿名纪律），依据为 cumcm meta 实抓的《论文格式规范（2026年修订稿）》；其他数模赛使用前先对照其 meta 的格式要求校准
2. 按章节填充：
   - 实验结果表格数字**只能**引用 `metrics.<role>.<键>`，表注标键名
   - 技术选型引用 kb/tech 卡片（注明 ID 与"用途/优势"结论出处）
   - 对比讨论引用该赛模式库（kb/INDEX.md 定位 → patterns.md）
   - 附录人机分工记录：按战役实际逐项填写（合规留痕，不可省略）
3. 编译：`typst compile workspace/docs/report.typ workspace/docs/report.pdf`
4. 自检：编译零警告级错误、章节完整（模板章节不得删节）、数字均带来源；不满足回到第 2 步

## 纪律

报告结构是反幻觉契约；图表缺数据 → 回工程侧要，不用占位数字顶替。
