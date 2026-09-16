---
tags: [论文, 倾转翼无人机, 姿态控制, 原型验证, 飞行试验]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/zhu2023AttitudeControlNovel.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - prototype
  - field_test
data_origin:
  - self_collected
platforms: []
frameworks:
  - variable-gain linear/square-root control
  - velocity compensation
datasets: []
hardware_stack:
  - THU-TW001 tilt-wing UAV
  - 40-inch propellers
  - 13-inch propellers
  - 2.31 m wingspan
  - 23 kg takeoff weight
artifact_availability: unknown
reproducibility_level: medium
---

# Zhu2023_新型倾转翼UAV悬停姿态控制

## 单行摘要
论文围绕新型倾转翼原型 `THU-TW001` 的悬停姿态控制问题，提出带速度补偿的变量增益线性/平方根控制律，并通过多组真实飞行试验证明其比积分补偿更稳定。

## 题目驱动研究框架
- 研究场景：兼顾悬停与巡航效率的新型倾转翼 UAV 原型飞行控制。
- 研究对象：`THU-TW001`、悬停姿态控制律、速度补偿机制。
- 核心问题：新型分布式推进结构提高了平台性能，但也带来新的阻尼力矩和姿态控制难题。
- 标题承诺的方法：attitude control of a novel tilt-wing UAV in hovering flight。
- 期望效果：在悬停状态下平稳跟踪姿态指令，并避免长时间飞行中的振荡失稳。

## Algorithm Design 快照
论文先给出 `THU-TW001` 的新型平台设计：主翼与尾翼分别带可倾转推进系统，实现悬停控制力矩与巡航效率兼得。随后作者没有用复杂非线性控制，而是构建了变量增益线性/平方根控制律，并在内环中加入速度补偿以抵消推进系统的阻尼效应。最终通过系留与自由飞行实验对比证明，速度补偿比积分补偿更适合这一原型。

## 图1系统框架草案
- 实体：THU-TW001 原型、主/尾可倾转螺旋桨、姿态控制器。
- 输入：姿态指令、飞行速度、推力差分。
- 关键机理：推进系统阻尼效应、速度补偿、变量增益控制律。
- 画图提醒：把主/尾螺旋桨的差分力矩和倾转关系画出来很关键。

## System Model
- THU-TW001 采用“内翼固定 + 外翼可倾转”结构，并配置两大两小两组倾转螺旋桨。
- 悬停姿态控制依赖前后螺旋桨差分推力提供控制力矩。
- 新型推进布局带来时间变化的动力学与额外阻尼力矩，这是控制难点所在。
- 研究聚焦悬停姿态，而非全飞行包线控制。

## Algorithm Design 详解
- 第一步：分析原型推进系统对悬停姿态动力学的影响，识别阻尼力矩问题。
- 第二步：设计变量增益线性/平方根控制律，保证响应速度与鲁棒性。
- 第三步：在姿态内环引入飞行速度补偿，以削弱推进系统阻尼效应。
- 第四步：通过系留试飞、无补偿自由飞行、积分补偿飞行和速度补偿飞行做对照。

## 实验证据卡片
- 验证类型：`prototype` + `field_test`
- 数据来源：真实飞行试验数据
- 平台与软件：未明确说明
- 方法组件：变量增益线性/平方根控制、速度补偿
- 硬件与算力：`THU-TW001` 原型，`2.31 m` 翼展，`23 kg` 起飞重量，`40-inch`/`13-inch` 螺旋桨
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整飞控软件栈与参数表

## Introduction 写作素材
- 倾转翼平台的挑战不只在过渡飞行，悬停控制也会因推进系统结构而变得不再“等价于普通多旋翼”。
- 真正有工程价值的控制方法未必最复杂，关键是能贴住原型平台的新动力学特征。

## Related Work 写作素材
- 与传统 tilt-wing/tilt-rotor 设计相比，本文强调新型平台结构与控制问题联动。
- 与单纯积分补偿不同，本文强调速度补偿更适配该原型的阻尼力矩问题。

## 相关系统建模页
- [[容错控制与碰撞规避模型]]

## 相关概念与主题页
- [[倾转翼无人机]]
- [[姿态控制]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/zhu2023AttitudeControlNovel.md)
