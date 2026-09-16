---
id: liu2025MultiUAVassistedMECInternet
name: SC-MA-TD3：抗干扰多模态语义通信的多UAV车联网MEC
field: [语义通信, 多智能体强化学习, UAV 辅助 MEC]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把任务质量度量从误码率改为语义准确度、在持续干扰下联合优化轨迹/关联/信道的建模范式，可迁移到含噪声或对抗扰动因素的决策题，突出有效信息流而非原始数据量
    reuse_cost: 高
  - track: 黑客松-数据与算法
    edge: 多智能体 TD3 学习多 UAV 协同（轨迹/用户关联/信道选择三变量联合），配合语义压缩降上传负担，适合弱网图像传输类应用题，差异化于按比特传输+单智能体 RL 基线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业弱网环境下田间图像语义化回传（只传任务相关信息）的通信降本方案技术支撑（TMC 2025，语义通信+多机协同抗干扰）
    reuse_cost: 低
sources:
  - paper_title: "Multi-UAV-assisted MEC in Internet of Vehicles with Combined Multi-Modal Semantic Communication under Jamming Attacks"
    doi: 10.1109/TMC.2025.3550965
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# SC-MA-TD3：抗干扰多模态语义通信的多UAV车联网MEC

## 单行摘要

面向存在恶意干扰机的多 UAV 辅助车联网 MEC 场景，车辆上传图像、RSU 提供文本、UAV 结合空中视角完成多模态联合分析：引入多模态语义通信只传输任务相关语义信息以降低上传负担，并提出 SC-MA-TD3 多智能体强化学习联合优化 UAV 轨迹、用户关联与信道选择，在干扰环境下同时降低通信与计算时延、维持语义恢复准确度。

## 方法快照

- 问题结构：多模态任务需跨设备聚合，地面链路易受遮挡，干扰机在多信道持续发射；任务质量由语义准确度而非比特误码衡量。
- 语义层：图像/文本/空中视角三路语义输入汇聚到 UAV 侧联合分析，语义压缩直接改变上传数据量与链路需求。
- 决策层：UAV 既做空中接入点也承担计算与多模态融合；轨迹、关联、信道选择高度动态非凸，用多智能体 TD3 学习协同行为。
- 关键洞察：语义通信在 UAV-MEC 中不是单独编码层，会反向影响轨迹、关联与边缘计算组织。
- 验证：数值仿真（合成车辆/RSU/UAV/干扰场景）；平台与代码未披露。

## 比赛映射要点

- 数模决策题：对抗干扰+语义质量约束的联合决策建模，适配含干扰/噪声因素的资源分配与调度题。
- 黑客松算法题：多智能体 TD3 的协同决策骨架与语义压缩组件可拆用；弱网条件下按语义重要度传数据是可落地的应用层创新点。
- 双创申报：农村弱网农业图像回传的降带宽方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Liu2025_抗干扰多模态语义通信的多UAV车联网MEC`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `liu2025MultiUAVassistedMECInternet` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
