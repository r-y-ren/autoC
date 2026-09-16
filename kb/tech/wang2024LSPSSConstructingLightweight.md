---
id: wang2024LSPSSConstructingLightweight
name: LSPSS空中计算轻量级隐私存储与共享
field: [隐私计算, 密文检索, 空中计算]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 数据要素共享平台的隐私合规技术卖点——多维密文范围查询加结果完整性验证（ASPE/IPC/Merkle tree），轻量级设计适配资源受限的农业物联网与低空数据平台场景
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 位置/日志数据的密文范围查询与可验证检索组件可移植到隐私保护检索类赛题，论文自报 25000 文件规模下查询约 2.5s、验证约 400ms，量级上说明轻量可行
    reuse_cost: 中
sources:
  - paper_title: "LSPSS：Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing"
    doi: 10.1109/TSC.2023.3333347
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# LSPSS空中计算轻量级隐私存储与共享

## 单行摘要

面向 6G 空中计算（LAC）平台的多实体数据共享需求，提出 LSPSS 方案：对位置与日志两类多维数据做转换，用 ASPE/IPC 构建轻量级密文索引支持隐私范围查询，再以 G-tree + Merkle tree 组合验证查询结果完整性——在 UAV 采集数据不可明文出域的约束下实现可检索、可验证的安全共享。

## 方法快照

- 系统模型：UAV、区域服务器、区域管理员、KGA、LAC 平台与用户六实体协作；UAV 上传数据，区域服务器与 LAC 平台分别承担位置索引与日志索引服务。
- 多维数据转换：把位置特征与日志特征重写为便于 IPC 匹配的向量形式，再进入密文域。
- 轻量级密文索引：基于 ASPE（渐近安全的置换-扰动矩阵加密）与 IPC 实现多维范围查询，保护单维隐私与 query unlinkability。
- 结果验证：G-tree 与 Merkle tree 组合支持查询结果完整性验证，防返回篡改/不全。
- 验证：trace-driven（真实数据库但未公开数据名），论文自报 25000 文件规模下查询约 2.5s、结果验证约 400ms；未公开代码与平台栈。

## 比赛映射要点

- 双创申报：数据安全合规是评审高频关注点；本方案提供「数据不出域仍可查可验」的完整故事线，且轻量级定位贴合农业物联网/低空平台等算力受限场景，比链上或全同态路线的代价论证更容易落地。
- 黑客松数据算法赛：隐私保护检索/可验证查询类赛题可直接复用 ASPE 范围匹配 + Merkle 验证的组件组合；ASPE 有公开论文级构造可自行实现，Merkle tree 有成熟库。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_LSPSS空中计算中的轻量级隐私存储与共享`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `wang2024LSPSSConstructingLightweight` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。**留痕**：bib 原标题含 ASCII 冒号（`LSPSS: Constructing ...`），按前波 YAML 约定改全角冒号写入 paper_title。
- `published` 仅年份已知（2024），按 2024-01-01 填写；性能数字（2.5s/400ms/25000 文件）为论文自报值，验证类信息承自 vault 页自评，如需引用请以论文原文复核。
