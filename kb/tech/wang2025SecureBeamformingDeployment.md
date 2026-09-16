---
id: wang2025SecureBeamformingDeployment
name: RSMA-UAV安全波束赋形与三维部署联合优化
field: [UAV 通信, 物理层安全, 凸优化]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: "部署位置 + 资源分配双变量拆解后 SCA 凸化、AO 交替迭代的求解模板，可整体迁移到设施选址/基站布点 + 功率/频谱分配类优化赛题，比单变量搜索更能体现建模深度"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济/智慧农业场景中无人机作为空中基站的安全覆盖方案技术支撑——公共流同时充当服务消息与反窃听扰动的设计可直接写进低空农业网络方案书
    reuse_cost: 低
sources:
  - paper_title: Secure Beamforming and Deployment Design for Rate-Splitting Multiple Access-Based UAV Communications
    doi: 10.1007/s11432-024-4224-6
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# RSMA-UAV安全波束赋形与三维部署联合优化

## 单行摘要

针对被动窃听下的两用户 MISO UAV-RSMA 下行系统，联合优化 UAV-BS 三维部署位置与安全波束赋形：把每个用户消息拆为 common/private 两部分，将公共流设计成"对合法用户是服务消息、对窃听者是不可解码干扰"的双重角色，在 QoS、功率与飞行空间约束下最大化总保密速率；求解上对波束赋形与部署两个子问题分别用 SCA 凸化，再以 AO 交替迭代逼近联合最优（L-RSMA 算法）。

## 方法快照

- 系统模型：UAV-BS 面向两合法用户广播 common stream 与 private streams，窃听者被动监听全部流；LoS/NLoS 混合信道，UAV 三维位置为显式优化变量。
- 安全波束赋形：设计 common precoder 使窃听者难以解码公共流——公共流既是有效服务又是反窃听扰动。
- 联合优化：原问题拆为波束赋形子问题与部署位置子问题，各自 SCA 近似凸化，AO 交替更新至收敛。
- 基线对比：优于 L-SDMA、L-NOMA 的 sum secrecy rate。

## 比赛映射要点

- 数模优化/决策题：解决"设施往哪放 + 资源怎么分"耦合问题的标准套路——变量解耦、逐块凸近似、交替迭代；选址类赛题（基站、仓库、无人机补给点）可复用该求解骨架。
- 双创申报：低空农业网络（农田上空无人机基站为传感终端供网）方案的安全覆盖设计支撑点，RSMA"一鱼两吃"的公共流设计是可讲述的技术亮点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_RSMA安全波束赋形与部署协同`（frontmatter 4 枚举字段已迁移至本卡）。
- bib 回填：citekey `wang2025SecureBeamformingDeployment` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation、synthetic 场景、复现性 medium、无开源）承自 vault 页自评，如需引用请以论文原文复核。
