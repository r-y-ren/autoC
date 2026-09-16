---
id: tun2025JointUAVDeployment
name: THz空天地网络UAV部署与资源联合优化
field: [空天地一体网络, 移动边缘计算, 资源分配]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 设施加载与部署选址 + 资源分配的强耦合联合优化骨架——BCD 把问题拆为卸载比例（凸优化）、子带与功率（matching game + CCP）、部署位置（SCA）、二次卸载（BSUM）四个可解子问题，是数模中「选址部署类 + 资源调度类」赛题的现成分解求解范式
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 全流程基于 Python + CVXPY 数值仿真即可复现验证，K-means 关联 + matching 原型成本低，适合做应急通信/无基础设施区域组网类算法题的差异化方案
    reuse_cost: 中
sources:
  - paper_title: "Joint UAV Deployment and Resource Allocation in THz-assisted MEC-enabled Integrated Space-Air-Ground Networks"
    doi: 10.1109/TMC.2024.3516655
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# THz空天地网络UAV部署与资源联合优化

## 单行摘要

针对缺乏地面基础设施区域的 THz 辅助空天地一体 MEC 网络，联合优化设备任务卸载比例、THz 子带分配、功率控制、UAV 部署位置与 UAV 二次卸载决策（UAV 间协作转发或上送 LEO 卫星），以任务时延为约束最小化终端与 UAV 总能耗——用 BCD 把五类强耦合决策拆成四个子问题分别求解，得到可迭代收敛的联合算法，并给出「4 架 UAV 已接近能效最优」的边际部署结论。

## 方法快照

- 系统链路：地面设备 →（THz 接入）关联 UAV →（本地算 / UAV 间转发 / LEO 卫星回传）二跳服务链。
- 难点：离散卸载决策、THz 子带匹配、连续功率、连续部署位置与二次卸载目的地强耦合。
- 求解：BCD 分解——子问题1 卸载比例用标准凸优化；子问题2 子带分配 + 功率控制用 one-to-one matching game + CCP；子问题3 部署位置用 SCA 逐步凸化；子问题4 二次卸载用 BSUM 处理离散协作决策。
- 验证：Python + CVXPY 数值仿真（合成空天地场景），95% 置信区间 + 多变体对比；结论含 UAV 数量的能效边际递减。

## 比赛映射要点

- 数模：设施选址 / 应急部署 + 通信资源分配的混合耦合是高频题型，BCD「拆子问题—各配求解器—迭代收敛」的论文级工具箱（SCA、matching、CCP）可直接迁移进答卷并支撑算法合理性论证。
- 黑客松/算法赛：无地面网络区域的应急组网、空中基站调度类赛题可用 K-means 关联 + matching 原型快速落地；「UAV 数量边际收益」分析可作为方案的成本论证亮点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Tun2025_THz辅助空天地一体网络中的UAV部署与资源分配`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `tun2025JointUAVDeployment` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
