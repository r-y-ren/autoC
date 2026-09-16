# vault-distill 样本验证报告（升级票04，2026-09-16）

管线四件套（SOP / bib 回填 / 建卡格式 / 拒收台账）在真实 vault 上的小样本验证（code-review 后扩至 18 页）。全量执行见票 05。

## 回填脚本实测

- `vault_bib_backfill.py --selftest`：3/3 通过（花括号清洗 / doi 提取 / venue 提取）。
- 真库：**535 条目 → kb/raw/vault-bib-map.yaml，DOI 覆盖 486（91%），url 覆盖 0**（vault bib 只用 doi 字段）。
- 样本 citekey `zhu2024FissionSpectralClustering` → 真实标题 "Fission Spectral Clustering Strategy for UAV Swarm Networks" / IEEE TSC / 2024 / DOI 10.1109/TSC.2024.3376191（完整回填成功）。

## 样本决策面（6 页实读）

| vault 页 | 类型 | 决策 | 依据 |
|---|---|---|---|
| Zhu2024_FANET中的UAV蜂群裂变谱聚类 | 论文页 | **收录** → `samples/tech/zhu2024FissionSpectralClustering.md` | UAV 蜂群聚类 ↔ 创新创业(智慧农业无人机集群)/黑客松 交集；4 枚举字段自 vault frontmatter 迁移；DOI 回填成功 |
| 裂变谱聚类 | 概念页 | **折叠**进上卡"关联概念"节 | 概念页不独立成卡（16 行 stub，锚定该论文） |
| FANET聚类 | 概念页 | **折叠**进上卡 | 同上 |
| 空战机动决策 | 概念页 | **拒收** → `sample-rejections.yaml` #1 | 军用空战主题与全部 directions 无交集 + 概念页无论文锚点 |
| 扩散模型强化学习 | 概念页 | **拒收**（样本期）→ #2 | 概念页规则；主题有 KB-2 邻近性，全量跑批应从论文页重判 |
| 示例论文笔记 | 归档/示例 | **跳过** | tags 含"归档，示例"，vault 内部脚手架页 |

## 扩展决策面（code-review 补 +12 页，共 18 页；按标题/命名约定判型，全量跑批逐页重判）

| vault 概念页 | 主题交集预判 | 样本决策 |
|---|---|---|
| 层次化联邦学习 | FL ↔ 黑客松/数模（分布式训练赛题） | eligible，全量从锚定论文页建卡覆盖 |
| 层次化空中计算 | 空中计算 MEC ↔ 智慧农业无人机集群 | eligible，同上 |
| 低轨卫星边缘计算 | SAGIN/LEO ↔ 黑客松/创新创业 | eligible，同上 |
| 大语言模型驱动无人机规划 | LLM×UAV ↔ KB-2 前沿 × 双创 | eligible，同上 |
| 低空经济（LAE） | 低空经济政策/产业 ↔ 创新创业申报 | eligible，同上 |
| 对称性增强多智能体强化学习 | MARL ↔ Kaggle/数模 | eligible，同上 |
| 代数连通度 | 图论谱方法 ↔ 数模（图算法题） | eligible，同上 |
| 定向性感知空地链路模型 | 空地链路建模 ↔ 数模建模 | eligible（偏弱），同上 |
| 导航质量（QoN） | QoN 指标 ↔ 数模评价体系 | eligible（偏弱），同上 |
| 部署成本效率（DCE） | 部署优化 ↔ 数模/黑客松 | eligible（偏弱），同上 |
| 层次化网络切片 | 通信底座，赛种映射勉强 | 拒收倾向，全量按锚定论文交集定 |
| 差异化服务 | QoS 底座，同上 | 拒收倾向，同上 |

## 词表实测（code-review 修正源）

vault 全库扫描：venue_tier 实取 {CCF-A:170, Unknown:4, Survey:1}、paper_role 实取 {anchor:172, supporting:2, survey:1}——schema 枚举已补 `unknown` 与 `survey`（ Unknown→unknown 映射写入字段 description）；evidence_tier 与 reproducibility_level 现有枚举全覆盖。

## 卡片格式验证

- 样本卡通过 `lint_kb.py --file`（paper-distill sources + 4 枚举 + 仅年份 published 约定）——见提交时验证输出。
- 拒收样例格式与正式台账一致（{id, reason, stars, decided}，reason 含交集判断依据）。
