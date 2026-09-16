---
id: sun2025JC5AServiceDelay
name: JC5A：空中MEC辅助工业CPS服务时延最小化
field: [移动边缘计算, 服务缓存, 无人机轨迹优化]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 工厂化农业/智能温室等 IIoT 场景的"传感设备-UAV 集群-宏站"三层算力方案支撑——通信、计算、缓存（3C）资源与服务缓存的系统级叙事超出普通"卸载+轨迹"方案，适合作为智慧农业高要求场景的差异化技术底座
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 把卸载、缓存、通信资源、计算资源、轨迹五类变量写成单一 MINLP 再三分解（BSUMM 处理离散决策 + 凸优化处理资源分配 + SCA 处理轨迹）的耦合问题分解模板，适用于多变量强耦合的大规模决策赛题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 「二元离散块坐标 + 连续凸近似 + SCA 轨迹迭代」的求解管线可复用为无人机调度类赛题的求解骨架；其 2D 轨迹近似 3D 的结论可简化赛题建模
    reuse_cost: 高
sources:
  - paper_title: JC5A：Service Delay Minimization for Aerial MEC-assisted Industrial Cyber-Physical Systems
    doi: 10.1109/TSC.2025.3592419
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# JC5A：空中 MEC 辅助工业 CPS 服务时延最小化

## 单行摘要

面向 6G 与 IIoT 驱动的工业信息物理系统（ICPS），构建 ISD-UAV 集群-MBS 三层协同架构，将总服务时延最小化问题（SDMOP）写成卸载 + 缓存 + 通信资源 + 计算资源 + UAV 轨迹的五元耦合 MINLP，提出 JC5A 算法：BSUMM 处理计算卸载与服务缓存的二元决策，凸优化分配通信与计算资源，SCA 迭代求解 UAV 轨迹，在能量受限下系统绑定 3C 资源与运动控制。

## 方法快照

- 三层架构：工业传感设备（ISD）周期产生时延敏感任务；协同 UAV 集群作 aerial MEC 提供近端计算与服务缓存；宏基站（MBS）作地面 MEC 缓解 UAV 过载。
- 问题构造：UAV 同时具有通信、计算、缓存三类资源与电池约束，能耗含飞行与计算服务两部分，轨迹控制与服务提供能力强耦合；缓存命中关系直接进入时延模型。
- 分解求解：SDMOP 拆成三个子问题——卸载与缓存（BSUMM）、通信/计算资源分配（凸优化）、轨迹控制（SCA）——迭代至收敛。
- 轨迹结论：在资源受限且结构化的工业环境中，2D 近地飞行可接近 3D 轨迹控制效果，降低控制自由度。
- 验证：合成工业任务流仿真，提供收敛性、复杂度与多组系统性能曲线；无真实工业数据或原型系统，平台未说明。

## 比赛映射要点

- 双创：智慧农业中的工厂化种植/智能温室是典型 IIoT 场景，本卡提供"边缘侧服务缓存 + UAV 机动算力 + 地面兜底"的完整系统架构叙事，区别于只谈卸载的普通方案（性能数字需自测）。
- 数模：五元耦合问题的"离散/连续/运动学"三路分解 + 交替迭代框架，可迁移到选址-配流-调度强耦合类赛题的求解组织方式。
- 黑客松：SCA + 块坐标求解管线复现门槛较高（reuse_cost 高），但"2D 轨迹足够"的结论可直接引用以简化赛题中的无人机运动模型。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Sun2025_JC5A空中MEC辅助工业CPS服务时延最小化`（frontmatter 4 枚举字段已迁移到本卡：venue_tier/evidence_tier/paper_role/reproducibility_level）。
- 错配修复留痕：分发清单所给 citekey `aServiceDelay` 为截断键；经页内 sources 核对，真实 Zotero 键为 `sun2025J$textC^5$aServiceDelay`（LaTeX 转义损坏形态，对应标题首词 `J\text{C}^{5}A` 即 JC5A），kb/raw/vault-bib-map.yaml 中该键唯一且 DOI/venue/year 一致，无冲突；因原键含 `$`/`^` 不符卡片 ID 字符集，本卡 id 采用去转义规范化键 `sun2025JC5AServiceDelay`（映射已回传 keymap 报告）。
- bib 回填：bib 中该条目标题同为 LaTeX 损坏形态，本卡 paper_title 按去转义还原（JC5A：Service Delay Minimization for Aerial MEC-assisted Industrial Cyber-Physical Systems）；标题 ASCII 冒号按格式规约改全角写入；DOI/venue 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
