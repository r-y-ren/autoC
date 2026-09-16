---
id: tian2024UAVAssistedWirelessCooperative
name: MA2T-DRL 应急编码缓存与功率联合优化
field: [编码缓存, 多智能体强化学习, 应急通信]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: MDS 编码缓存命中率解析把社会关系与移动接触时长一起写进模型，配「慢尺度缓存放置 / 快尺度功率控制」双时间尺度分解，适配应急物资/内容预置类决策题——「能连上」与「愿不愿服务」双约束的建模角度可复用
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: ST-DQN（慢尺度放置）+ FT-DQN（快尺度功率）+ QMIX 聚合多代理的两时间尺度学习骨架，组件全部在开源 RL 生态可得，实现成本可控且结构清晰可讲
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 灾害应急通信保障方案（地面指挥车编码缓存为主、UAV 补位缓存为辅）支撑点，「UAV 不替代地面节点而是补足不确定性」的角色定位叙事成熟
    reuse_cost: 低
sources:
  - paper_title: "UAV-Assisted Wireless Cooperative Communication and Coded Caching: A Multiagent Two-Timescale DRL Approach"
    doi: 10.1109/TMC.2023.3298641
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# MA2T-DRL 应急编码缓存与功率联合优化

## 单行摘要

面向灾害应急场景中基础设施脆弱、现场用户需快速获取图像/视频/指令内容的问题，把地面指挥车辆与 UAV 一起建模为内容提供者：地面 CP 用 (n,k) MDS 编码存储内容片段、请求者经 D2D 接触取片段，UAV 缓存完整文件在地面命中失败时补位服务。在编码缓存、社会关系与移动接触时长约束下，用 MA2T-DRL 联合优化缓存策略与发射功率以最大化整体内容命中率——慢时间尺度缓存放置交给 ST-DQN、快时间尺度功率控制交给 FT-DQN，再以 QMIX 聚合慢尺度代理降低多代理训练开销，UAV 轨迹另以 PSO/greedy 补充优化。

## 方法快照

- 缓存结构：地面 MDS 编码片段（抗部分接触失败）+ UAV 完整文件补位，两级递进。
- 命中建模：交付成功率与命中率表达式同时纳入物理接触时长与社会关系（「能连上」与「愿不愿服务」双因素）。
- 决策分解：慢尺度放置（ST-DQN）/快尺度功率（FT-DQN）显式分离，QMIX 聚合局部代理控制训练复杂度。
- 补充优化：UAV 轨迹用 PSO / greedy。
- 验证：数值仿真（合成场景，i7-7500U/8GB）；未披露统一代码框架与真实应急链路测试，复现性 medium。

## 比赛映射要点

- 数模：内容/物资预置 + 不确定交付类题可复用「编码冗余换鲁棒 + 双时间尺度决策」框架；社会关系因子进入命中率函数的写法可直接迁移到带信任/意愿的传播模型。
- 黑客松：多代理缓存/资源预放置赛题可套 QMIX + 双 DQN 组件化实现；命中率作为统一评价口径便于搭 baseline 对比。
- 双创申报：应急通信、防灾减灾类项目的「空地协同内容保障」章节素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Tian2024_UAV辅助无线协同通信与编码缓存`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `tian2024UAVAssistedWirelessCooperative` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、算法组件明确但代码未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
