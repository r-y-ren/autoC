# vault-distill 样本验证报告（升级票04，2026-09-16）

管线四件套（SOP / bib 回填 / 建卡格式 / 拒收台账）在真实 valut 上的小样本验证。全量执行见票 05。

## 回填脚本实测

- `vault_bib_backfill.py --selftest`：3/3 通过（花括号清洗 / doi 提取 / venue 提取）。
- 真库：**535 条目 → kb/raw/vault-bib-map.yaml，DOI 覆盖 486（91%），url 覆盖 0**（valut bib 只用 doi 字段）。
- 样本 citekey `zhu2024FissionSpectralClustering` → 真实标题 "Fission Spectral Clustering Strategy for UAV Swarm Networks" / IEEE TSC / 2024 / DOI 10.1109/TSC.2024.3376191（完整回填成功）。

## 样本决策面（6 页实读）

| valut 页 | 类型 | 决策 | 依据 |
|---|---|---|---|
| Zhu2024_FANET中的UAV蜂群裂变谱聚类 | 论文页 | **收录** → `samples/tech/zhu2024FissionSpectralClustering.md` | UAV 蜂群聚类 ↔ 创新创业(智慧农业无人机集群)/黑客松 交集；4 枚举字段自 valut frontmatter 迁移；DOI 回填成功 |
| 裂变谱聚类 | 概念页 | **折叠**进上卡"关联概念"节 | 概念页不独立成卡（16 行 stub，锚定该论文） |
| FANET聚类 | 概念页 | **折叠**进上卡 | 同上 |
| 空战机动决策 | 概念页 | **拒收** → `sample-rejections.yaml` #1 | 军用空战主题与全部 directions 无交集 + 概念页无论文锚点 |
| 扩散模型强化学习 | 概念页 | **拒收**（样本期）→ #2 | 概念页规则；主题有 KB-2 邻近性，全量跑批应从论文页重判 |
| 示例论文笔记 | 归档/示例 | **跳过** | tags 含"归档，示例"，valut 内部脚手架页 |

## 卡片格式验证

- 样本卡通过 `lint_kb.py --file`（paper-distill sources + 4 枚举 + 仅年份 published 约定）——见提交时验证输出。
- 拒收样例格式与正式台账一致（{id, reason, stars, decided}，reason 含交集判断依据）。
