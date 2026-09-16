#!/bin/bash
# 改进的重命名脚本 - 同时处理PDF和Markdown文件
# 基于CCFA.bib中的citation key
#
# 共处理 534 个文献条目
#
set -e  # 遇到错误立即退出

cd /Users/wupengfei/Downloads/my_LLM_valut/raw

echo "开始文件重命名..."

# alam2024JoiTraCon
# Joint Trajectory Control, Frequency Allocation, and Routing for UAV
# PDF相似度: 100.00%, Markdown相似度: 72.83%
if [ -f "pdfs/alam2024JointTrajectoryControl.pdf" ]; then
    mv "pdfs/alam2024JointTrajectoryControl.pdf" "pdfs/alam2024JoiTraCon.pdf"
    echo "✓ PDF重命名: alam2024JointTrajectoryControl.pdf -> alam2024JoiTraCon.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/alam2024JointTrajectoryControl.pdf"
fi

# Markdown跳过（相似度较低）: Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md -> alam2024JoiTraCon.md

# alkouz2022InfEneCom
# In-Flight Energy-Driven Composition of Drone Swarm Services
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/alkouz2022InflightEnergydrivenComposition.pdf" ]; then
    mv "pdfs/alkouz2022InflightEnergydrivenComposition.pdf" "pdfs/alkouz2022InfEneCom.pdf"
    echo "✓ PDF重命名: alkouz2022InflightEnergydrivenComposition.pdf -> alkouz2022InfEneCom.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/alkouz2022InflightEnergydrivenComposition.pdf"
fi

if [ -f "markdown/In-Flight Energy-Driven Composition of Drone Swarm Services.md" ]; then
    mv "markdown/In-Flight Energy-Driven Composition of Drone Swarm Services.md" "markdown/alkouz2022InfEneCom.md"
    echo "✓ Markdown重命名: In-Flight Energy-Driven Composition of Drone Swarm Services.... -> alkouz2022InfEneCom.md"
else
    echo "⚠ Markdown文件不存在: markdown/In-Flight Energy-Driven Composition of Drone Swarm Services.md"
fi

# bai2024DelCooTas
# Delay-Aware Cooperative Task Offloading
# PDF相似度: 100.00%, Markdown相似度: 75.00%
if [ -f "pdfs/bai2024DelayAwareCooperativeTask.pdf" ]; then
    mv "pdfs/bai2024DelayAwareCooperativeTask.pdf" "pdfs/bai2024DelCooTas.pdf"
    echo "✓ PDF重命名: bai2024DelayAwareCooperativeTask.pdf -> bai2024DelCooTas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/bai2024DelayAwareCooperativeTask.pdf"
fi

# Markdown跳过（相似度较低）: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md -> bai2024DelCooTas.md

# chen2024AdaBitVid
# Adaptive Bitrate Video Caching
# PDF相似度: 100.00%, Markdown相似度: 62.50%
if [ -f "pdfs/chen2024AdaptiveBitrateVideo.pdf" ]; then
    mv "pdfs/chen2024AdaptiveBitrateVideo.pdf" "pdfs/chen2024AdaBitVid.pdf"
    echo "✓ PDF重命名: chen2024AdaptiveBitrateVideo.pdf -> chen2024AdaBitVid.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2024AdaptiveBitrateVideo.pdf"
fi

# Markdown跳过（相似度较低）: Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md -> chen2024AdaBitVid.md

# chen2025EneOveCom
# Energy-Efficient over-the-Air Computation in UAV-assisted IIoT
# PDF相似度: 100.00%, Markdown相似度: 85.71%
if [ -f "pdfs/chen2025EnergyefficientOvertheairComputation.pdf" ]; then
    mv "pdfs/chen2025EnergyefficientOvertheairComputation.pdf" "pdfs/chen2025EneOveCom.pdf"
    echo "✓ PDF重命名: chen2025EnergyefficientOvertheairComputation.pdf -> chen2025EneOveCom.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2025EnergyefficientOvertheairComputation.pdf"
fi

if [ -f "markdown/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks.md" ]; then
    mv "markdown/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks.md" "markdown/chen2025EneOveCom.md"
    echo "✓ Markdown重命名: Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_II... -> chen2025EneOveCom.md"
else
    echo "⚠ Markdown文件不存在: markdown/Energy-Efficient_Over-the-Air_Computation_in_UAV-Assisted_IIoT_Networks.md"
fi

# chen2025JoiTraOpt
# Joint Trajectory Optimization and Resource Allocation in UAV-MEC
# PDF相似度: 100.00%, Markdown相似度: 67.46%
if [ -f "pdfs/chen2025JointTrajectoryOptimization.pdf" ]; then
    mv "pdfs/chen2025JointTrajectoryOptimization.pdf" "pdfs/chen2025JoiTraOpt.pdf"
    echo "✓ PDF重命名: chen2025JointTrajectoryOptimization.pdf -> chen2025JoiTraOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2025JointTrajectoryOptimization.pdf"
fi

# Markdown跳过（相似度较低）: Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md -> chen2025JoiTraOpt.md

# chen2025MulTasOff
# Multi-User Task Offloading in UAV-assisted LEO
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/chen2025MultiuserTaskOffloading.pdf" ]; then
    mv "pdfs/chen2025MultiuserTaskOffloading.pdf" "pdfs/chen2025MulTasOff.pdf"
    echo "✓ PDF重命名: chen2025MultiuserTaskOffloading.pdf -> chen2025MulTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2025MultiuserTaskOffloading.pdf"
fi

# chen2025TasOffAnd
# Task Offloading and Resource Pricing Based on Game Theory in UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 78.26%
if [ -f "pdfs/chen2025TaskOffloadingResource.pdf" ]; then
    mv "pdfs/chen2025TaskOffloadingResource.pdf" "pdfs/chen2025TasOffAnd.pdf"
    echo "✓ PDF重命名: chen2025TaskOffloadingResource.pdf -> chen2025TasOffAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2025TaskOffloadingResource.pdf"
fi

# Markdown跳过（相似度较低）: Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md -> chen2025TasOffAnd.md

# cui2024TheDatVal
# The Data Value Based Asynchronous Federated Learning
# PDF相似度: 100.00%, Markdown相似度: 85.47%
if [ -f "pdfs/cui2024DataValueBased.pdf" ]; then
    mv "pdfs/cui2024DataValueBased.pdf" "pdfs/cui2024TheDatVal.pdf"
    echo "✓ PDF重命名: cui2024DataValueBased.pdf -> cui2024TheDatVal.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/cui2024DataValueBased.pdf"
fi

if [ -f "markdown/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni.md" ]; then
    mv "markdown/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni.md" "markdown/cui2024TheDatVal.md"
    echo "✓ Markdown重命名: Cui 等 - 2024 - The Data Value Based Asynchronous Federated L... -> cui2024TheDatVal.md"
else
    echo "⚠ Markdown文件不存在: markdown/Cui 等 - 2024 - The Data Value Based Asynchronous Federated Learni.md"
fi

# dabiri2025ANovMrr
# A Novel MRR-UAV-based
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/dabiri2025NovelMRRUAVbasedRelay.pdf" ]; then
    mv "pdfs/dabiri2025NovelMRRUAVbasedRelay.pdf" "pdfs/dabiri2025ANovMrr.pdf"
    echo "✓ PDF重命名: dabiri2025NovelMRRUAVbasedRelay.pdf -> dabiri2025ANovMrr.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/dabiri2025NovelMRRUAVbasedRelay.pdf"
fi

# dou2025SchDroAnd
# Scheduling Drone and Mobile Charger via Hybrid-Action Deep Reinforcement Learnin...
# PDF相似度: 100.00%, Markdown相似度: 61.04%
if [ -f "pdfs/dou2025SchedulingDroneMobile.pdf" ]; then
    mv "pdfs/dou2025SchedulingDroneMobile.pdf" "pdfs/dou2025SchDroAnd.pdf"
    echo "✓ PDF重命名: dou2025SchedulingDroneMobile.pdf -> dou2025SchDroAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/dou2025SchedulingDroneMobile.pdf"
fi

# Markdown跳过（相似度较低）: Autonomous multi-drone racing method based on deep reinforcement learning.md -> dou2025SchDroAnd.md

# fu2022Ene3d
# Energy-Efficient 3D
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/fu2022Energyefficient3DData.pdf" ]; then
    mv "pdfs/fu2022Energyefficient3DData.pdf" "pdfs/fu2022Ene3d.pdf"
    echo "✓ PDF重命名: fu2022Energyefficient3DData.pdf -> fu2022Ene3d.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/fu2022Energyefficient3DData.pdf"
fi

# gao2024SerExpOri
# Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs
# PDF相似度: 100.00%, Markdown相似度: 67.30%
if [ -f "pdfs/gao2024ServiceExperienceOriented.pdf" ]; then
    mv "pdfs/gao2024ServiceExperienceOriented.pdf" "pdfs/gao2024SerExpOri.pdf"
    echo "✓ PDF重命名: gao2024ServiceExperienceOriented.pdf -> gao2024SerExpOri.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gao2024ServiceExperienceOriented.pdf"
fi

# Markdown跳过（相似度较低）: IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md -> gao2024SerExpOri.md

# gao2025ImpUseQoe
# Improving User QoE
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/gao2025ImprovingUserQoE.pdf" ]; then
    mv "pdfs/gao2025ImprovingUserQoE.pdf" "pdfs/gao2025ImpUseQoe.pdf"
    echo "✓ PDF重命名: gao2025ImprovingUserQoE.pdf -> gao2025ImpUseQoe.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gao2025ImprovingUserQoE.pdf"
fi

# gao2025TraLeaFor
# Transfer Learning for Joint Trajectory Control and Task Offloading in Large-Scal...
# PDF相似度: 100.00%, Markdown相似度: 88.24%
if [ -f "pdfs/gao2025TransferLearningJoint.pdf" ]; then
    mv "pdfs/gao2025TransferLearningJoint.pdf" "pdfs/gao2025TraLeaFor.pdf"
    echo "✓ PDF重命名: gao2025TransferLearningJoint.pdf -> gao2025TraLeaFor.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gao2025TransferLearningJoint.pdf"
fi

if [ -f "markdown/Transfer_Learning_for_Joint_Trajectory_Control_and_Task_Offloading_in_Large-Scale_Partially_Observable_UAV-Assisted_MEC.md" ]; then
    mv "markdown/Transfer_Learning_for_Joint_Trajectory_Control_and_Task_Offloading_in_Large-Scale_Partially_Observable_UAV-Assisted_MEC.md" "markdown/gao2025TraLeaFor.md"
    echo "✓ Markdown重命名: Transfer_Learning_for_Joint_Trajectory_Control_and_Task_Offl... -> gao2025TraLeaFor.md"
else
    echo "⚠ Markdown文件不存在: markdown/Transfer_Learning_for_Joint_Trajectory_Control_and_Task_Offloading_in_Large-Scale_Partially_Observable_UAV-Assisted_MEC.md"
fi

# gaydamaka2024DynTopOrg
# Dynamic Topology Organization
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/gaydamaka2024DynamicTopologyOrganization.pdf" ]; then
    mv "pdfs/gaydamaka2024DynamicTopologyOrganization.pdf" "pdfs/gaydamaka2024DynTopOrg.pdf"
    echo "✓ PDF重命名: gaydamaka2024DynamicTopologyOrganization.pdf -> gaydamaka2024DynTopOrg.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gaydamaka2024DynamicTopologyOrganization.pdf"
fi

# gong2024Ene3dUav
# Energy-Efficient 3-D UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/gong2024Energyefficient3DUAV.pdf" ]; then
    mv "pdfs/gong2024Energyefficient3DUAV.pdf" "pdfs/gong2024Ene3dUav.pdf"
    echo "✓ PDF重命名: gong2024Energyefficient3DUAV.pdf -> gong2024Ene3dUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gong2024Energyefficient3DUAV.pdf"
fi

# gong2025JoiOptThe
# Jointly Optimizing the Energy and Time for Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 64.29%
if [ -f "pdfs/gong2025JointlyOptimizingEnergy.pdf" ]; then
    mv "pdfs/gong2025JointlyOptimizingEnergy.pdf" "pdfs/gong2025JoiOptThe.pdf"
    echo "✓ PDF重命名: gong2025JointlyOptimizingEnergy.pdf -> gong2025JoiOptThe.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gong2025JointlyOptimizingEnergy.pdf"
fi

# Markdown跳过（相似度较低）: Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md -> gong2025JoiOptThe.md

# gui2024CovProAnd
# Coverage Probability and Throughput Optimization in Integrated mmWave
# PDF相似度: 100.00%, Markdown相似度: 74.19%
if [ -f "pdfs/gui2024CoverageProbabilityThroughput.pdf" ]; then
    mv "pdfs/gui2024CoverageProbabilityThroughput.pdf" "pdfs/gui2024CovProAnd.pdf"
    echo "✓ PDF重命名: gui2024CoverageProbabilityThroughput.pdf -> gui2024CovProAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gui2024CoverageProbabilityThroughput.pdf"
fi

# Markdown跳过（相似度较低）: Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md -> gui2024CovProAnd.md

# guo2024JoiOpt
# Joint Optimization
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/guo2024JointOptimizationTrajectory.pdf" ]; then
    mv "pdfs/guo2024JointOptimizationTrajectory.pdf" "pdfs/guo2024JoiOpt.pdf"
    echo "✓ PDF重命名: guo2024JointOptimizationTrajectory.pdf -> guo2024JoiOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/guo2024JointOptimizationTrajectory.pdf"
fi

# guo2025MigTow
# Mighty: Towards
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/guo2025MightyLongrangeHighthroughput.pdf" ]; then
    mv "pdfs/guo2025MightyLongrangeHighthroughput.pdf" "pdfs/guo2025MigTow.pdf"
    echo "✓ PDF重命名: guo2025MightyLongrangeHighthroughput.pdf -> guo2025MigTow.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/guo2025MightyLongrangeHighthroughput.pdf"
fi

# han2024ColRouPla
# Collaborative Route Planning of UAVs
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/han2024CollaborativeRoutePlanning.pdf" ]; then
    mv "pdfs/han2024CollaborativeRoutePlanning.pdf" "pdfs/han2024ColRouPla.pdf"
    echo "✓ PDF重命名: han2024CollaborativeRoutePlanning.pdf -> han2024ColRouPla.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/han2024CollaborativeRoutePlanning.pdf"
fi

# han2024JoiAssDep
# Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-e...
# PDF相似度: 100.00%, Markdown相似度: 75.12%
if [ -f "pdfs/han2024JointAssociationDeployment.pdf" ]; then
    mv "pdfs/han2024JointAssociationDeployment.pdf" "pdfs/han2024JoiAssDep.pdf"
    echo "✓ PDF重命名: han2024JointAssociationDeployment.pdf -> han2024JoiAssDep.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/han2024JointAssociationDeployment.pdf"
fi

# Markdown跳过（相似度较低）: Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md -> han2024JoiAssDep.md

# hao2024JoiTasOff
# Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 69.91%
if [ -f "pdfs/hao2024JointTaskOffloading.pdf" ]; then
    mv "pdfs/hao2024JointTaskOffloading.pdf" "pdfs/hao2024JoiTasOff.pdf"
    echo "✓ PDF重命名: hao2024JointTaskOffloading.pdf -> hao2024JoiTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/hao2024JointTaskOffloading.pdf"
fi

# Markdown跳过（相似度较低）: IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md -> hao2024JoiTasOff.md

# hao2025RelOptOf
# Reliability-Aware Optimization of Task Offloading for UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 81.63%
if [ -f "pdfs/hao2025ReliabilityawareOptimizationTask.pdf" ]; then
    mv "pdfs/hao2025ReliabilityawareOptimizationTask.pdf" "pdfs/hao2025RelOptOf.pdf"
    echo "✓ PDF重命名: hao2025ReliabilityawareOptimizationTask.pdf -> hao2025RelOptOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/hao2025ReliabilityawareOptimizationTask.pdf"
fi

if [ -f "markdown/Reliability-Aware_Optimization_of_Task_Offloading_for_UAV-Assisted_Edge_Computing.md" ]; then
    mv "markdown/Reliability-Aware_Optimization_of_Task_Offloading_for_UAV-Assisted_Edge_Computing.md" "markdown/hao2025RelOptOf.md"
    echo "✓ Markdown重命名: Reliability-Aware_Optimization_of_Task_Offloading_for_UAV-As... -> hao2025RelOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Reliability-Aware_Optimization_of_Task_Offloading_for_UAV-Assisted_Edge_Computing.md"
fi

# he2024BalTotEne
# Balancing Total Energy Consumption
# PDF相似度: 100.00%, Markdown相似度: 69.39%
if [ -f "pdfs/he2024BalancingTotalEnergy.pdf" ]; then
    mv "pdfs/he2024BalancingTotalEnergy.pdf" "pdfs/he2024BalTotEne.pdf"
    echo "✓ PDF重命名: he2024BalancingTotalEnergy.pdf -> he2024BalTotEne.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/he2024BalancingTotalEnergy.pdf"
fi

# Markdown跳过（相似度较低）: He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md -> he2024BalTotEne.md

# hoang2024FinBloLen
# Finite Block Length NOMA MU
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/hoang2024FiniteBlockLength.pdf" ]; then
    mv "pdfs/hoang2024FiniteBlockLength.pdf" "pdfs/hoang2024FinBloLen.pdf"
    echo "✓ PDF重命名: hoang2024FiniteBlockLength.pdf -> hoang2024FinBloLen.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/hoang2024FiniteBlockLength.pdf"
fi

# hoang2025Ada3d
# Adaptive 3D
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/hoang2025Adaptive3DPlacementa.pdf" ]; then
    mv "pdfs/hoang2025Adaptive3DPlacementa.pdf" "pdfs/hoang2025Ada3d.pdf"
    echo "✓ PDF重命名: hoang2025Adaptive3DPlacementa.pdf -> hoang2025Ada3d.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/hoang2025Adaptive3DPlacementa.pdf"
fi

# hou2025AgeOfInf
# Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-...
# PDF相似度: 100.00%, Markdown相似度: 74.51%
if [ -f "pdfs/hou2025AgeInformationawareMultiobjective.pdf" ]; then
    mv "pdfs/hou2025AgeInformationawareMultiobjective.pdf" "pdfs/hou2025AgeOfInf.pdf"
    echo "✓ PDF重命名: hou2025AgeInformationawareMultiobjective.pdf -> hou2025AgeOfInf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/hou2025AgeInformationawareMultiobjective.pdf"
fi

# Markdown跳过（相似度较低）: Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md -> hou2025AgeOfInf.md

# huang2024DynTasOff
# Dynamic Task Offloading for Multi-UAVs
# PDF相似度: 100.00%, Markdown相似度: 60.19%
if [ -f "pdfs/huang2024DynamicTaskOffloading.pdf" ]; then
    mv "pdfs/huang2024DynamicTaskOffloading.pdf" "pdfs/huang2024DynTasOff.pdf"
    echo "✓ PDF重命名: huang2024DynamicTaskOffloading.pdf -> huang2024DynTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/huang2024DynamicTaskOffloading.pdf"
fi

# Markdown跳过（相似度较低）: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md -> huang2024DynTasOff.md

# huang2025AFasUav
# A Fast UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/huang2025FastUAVTrajectory.pdf" ]; then
    mv "pdfs/huang2025FastUAVTrajectory.pdf" "pdfs/huang2025AFasUav.pdf"
    echo "✓ PDF重命名: huang2025FastUAVTrajectory.pdf -> huang2025AFasUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/huang2025FastUAVTrajectory.pdf"
fi

# ji2024DecAssWit
# Decoupled Association With Rate Splitting Multiple Access
# PDF相似度: 100.00%, Markdown相似度: 82.64%
if [ -f "pdfs/ji2024DecoupledAssociationRate.pdf" ]; then
    mv "pdfs/ji2024DecoupledAssociationRate.pdf" "pdfs/ji2024DecAssWit.pdf"
    echo "✓ PDF重命名: ji2024DecoupledAssociationRate.pdf -> ji2024DecAssWit.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/ji2024DecoupledAssociationRate.pdf"
fi

if [ -f "markdown/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple.md" ]; then
    mv "markdown/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple.md" "markdown/ji2024DecAssWit.md"
    echo "✓ Markdown重命名: Ji 等 - 2024 - Decoupled Association With Rate Splitting Mult... -> ji2024DecAssWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/Ji 等 - 2024 - Decoupled Association With Rate Splitting Multiple.md"
fi

# jia2024EneAndTim
# Energy and Time Trade-off Optimization for Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/jia2024EnergyTimeTradeoff.pdf" ]; then
    mv "pdfs/jia2024EnergyTimeTradeoff.pdf" "pdfs/jia2024EneAndTim.pdf"
    echo "✓ PDF重命名: jia2024EnergyTimeTradeoff.pdf -> jia2024EneAndTim.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/jia2024EnergyTimeTradeoff.pdf"
fi

# jia2025DisRobOpt
# Distributionally Robust Optimization for Aerial Multi-Access Edge Computing via ...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/jia2025DistributionallyRobustOptimization.pdf" ]; then
    mv "pdfs/jia2025DistributionallyRobustOptimization.pdf" "pdfs/jia2025DisRobOpt.pdf"
    echo "✓ PDF重命名: jia2025DistributionallyRobustOptimization.pdf -> jia2025DisRobOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/jia2025DistributionallyRobustOptimization.pdf"
fi

# Markdown跳过（相似度较低）: jia2025DistributionallyRobustOptimization.md -> jia2025DisRobOpt.md

# jin2025AResCon
# A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV
# PDF相似度: 100.00%, Markdown相似度: 76.32%
if [ -f "pdfs/jin2025ResourceefficientContentSharing.pdf" ]; then
    mv "pdfs/jin2025ResourceefficientContentSharing.pdf" "pdfs/jin2025AResCon.pdf"
    echo "✓ PDF重命名: jin2025ResourceefficientContentSharing.pdf -> jin2025AResCon.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/jin2025ResourceefficientContentSharing.pdf"
fi

# Markdown跳过（相似度较低）: A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md -> jin2025AResCon.md

# kang2024AutMulRac
# Autonomous Multi-Drone Racing Method Based on Deep Reinforcement Learning
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/kang2024AutonomousMultidroneRacing.pdf" ]; then
    mv "pdfs/kang2024AutonomousMultidroneRacing.pdf" "pdfs/kang2024AutMulRac.pdf"
    echo "✓ PDF重命名: kang2024AutonomousMultidroneRacing.pdf -> kang2024AutMulRac.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/kang2024AutonomousMultidroneRacing.pdf"
fi

if [ -f "markdown/Autonomous multi-drone racing method based on deep reinforcement learning.md" ]; then
    mv "markdown/Autonomous multi-drone racing method based on deep reinforcement learning.md" "markdown/kang2024AutMulRac.md"
    echo "✓ Markdown重命名: Autonomous multi-drone racing method based on deep reinforce... -> kang2024AutMulRac.md"
else
    echo "⚠ Markdown文件不存在: markdown/Autonomous multi-drone racing method based on deep reinforcement learning.md"
fi

# karmakar2024ABloDis
# A Blockchain-Based Distributed
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/karmakar2024BlockchainBasedDistributedIntelligent.pdf" ]; then
    mv "pdfs/karmakar2024BlockchainBasedDistributedIntelligent.pdf" "pdfs/karmakar2024ABloDis.pdf"
    echo "✓ PDF重命名: karmakar2024BlockchainBasedDistributedIntelligent.pdf -> karmakar2024ABloDis.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/karmakar2024BlockchainBasedDistributedIntelligent.pdf"
fi

# karmakar2024ANovFed
# A Novel Federated Learning-Based Smart Power
# PDF相似度: 100.00%, Markdown相似度: 77.19%
if [ -f "pdfs/karmakar2024NovelFederatedLearningBased.pdf" ]; then
    mv "pdfs/karmakar2024NovelFederatedLearningBased.pdf" "pdfs/karmakar2024ANovFed.pdf"
    echo "✓ PDF重命名: karmakar2024NovelFederatedLearningBased.pdf -> karmakar2024ANovFed.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/karmakar2024NovelFederatedLearningBased.pdf"
fi

# Markdown跳过（相似度较低）: Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md -> karmakar2024ANovFed.md

# karmakar2024APuf
# A PUF
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/karmakar2024PUFFuzzyExtractorBased.pdf" ]; then
    mv "pdfs/karmakar2024PUFFuzzyExtractorBased.pdf" "pdfs/karmakar2024APuf.pdf"
    echo "✓ PDF重命名: karmakar2024PUFFuzzyExtractorBased.pdf -> karmakar2024APuf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/karmakar2024PUFFuzzyExtractorBased.pdf"
fi

# kharjana2025SecAutUav
# Securing Autonomous UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/kharjana2025SecuringAutonomousUAV.pdf" ]; then
    mv "pdfs/kharjana2025SecuringAutonomousUAV.pdf" "pdfs/kharjana2025SecAutUav.pdf"
    echo "✓ PDF重命名: kharjana2025SecuringAutonomousUAV.pdf -> kharjana2025SecAutUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/kharjana2025SecuringAutonomousUAV.pdf"
fi

# khochare2024ImpAlg
# Improved Algorithms
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/khochare2024ImprovedAlgorithmsCoScheduling.pdf" ]; then
    mv "pdfs/khochare2024ImprovedAlgorithmsCoScheduling.pdf" "pdfs/khochare2024ImpAlg.pdf"
    echo "✓ PDF重命名: khochare2024ImprovedAlgorithmsCoScheduling.pdf -> khochare2024ImpAlg.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/khochare2024ImprovedAlgorithmsCoScheduling.pdf"
fi

# kumar2025DroIrs
# Drone-Assisted IRS
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/kumar2025DroneassistedIRSSystem.pdf" ]; then
    mv "pdfs/kumar2025DroneassistedIRSSystem.pdf" "pdfs/kumar2025DroIrs.pdf"
    echo "✓ PDF重命名: kumar2025DroneassistedIRSSystem.pdf -> kumar2025DroIrs.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/kumar2025DroneassistedIRSSystem.pdf"
fi

# kumari2025MaxSerPro
# Maximizing Service Provider's Profit in Multi-UAV 5G
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/kumari2025MaximizingServiceProviders.pdf" ]; then
    mv "pdfs/kumari2025MaximizingServiceProviders.pdf" "pdfs/kumari2025MaxSerPro.pdf"
    echo "✓ PDF重命名: kumari2025MaximizingServiceProviders.pdf -> kumari2025MaxSerPro.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/kumari2025MaximizingServiceProviders.pdf"
fi

# lee2025AdaStaCon
# Adaptive Stabilization Control by Deep Reinforcement Learning for Hovering Drone...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/lee2025AdaptiveStabilizationControl.pdf" ]; then
    mv "pdfs/lee2025AdaptiveStabilizationControl.pdf" "pdfs/lee2025AdaStaCon.pdf"
    echo "✓ PDF重命名: lee2025AdaptiveStabilizationControl.pdf -> lee2025AdaStaCon.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/lee2025AdaptiveStabilizationControl.pdf"
fi

# lei2025EdgInfHub
# Edge Information Hub: Orchestrating
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/lei2025EdgeInformationHub.pdf" ]; then
    mv "pdfs/lei2025EdgeInformationHub.pdf" "pdfs/lei2025EdgInfHub.pdf"
    echo "✓ PDF重命名: lei2025EdgeInformationHub.pdf -> lei2025EdgInfHub.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/lei2025EdgeInformationHub.pdf"
fi

# li2024SecOffWit
# Secure Offloading with Adversarial Multi-Agent Reinforcement Learning against In...
# PDF相似度: 100.00%, Markdown相似度: 86.21%
if [ -f "pdfs/li2024SecureOffloadingAdversarial.pdf" ]; then
    mv "pdfs/li2024SecureOffloadingAdversarial.pdf" "pdfs/li2024SecOffWit.pdf"
    echo "✓ PDF重命名: li2024SecureOffloadingAdversarial.pdf -> li2024SecOffWit.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2024SecureOffloadingAdversarial.pdf"
fi

if [ -f "markdown/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp.md" ]; then
    mv "markdown/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp.md" "markdown/li2024SecOffWit.md"
    echo "✓ Markdown重命名: Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent... -> li2024SecOffWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/Li 等 - 2024 - Secure Offloading With Adversarial Multi-Agent Reinforcement Learning Against Intelligent Eavesdropp.md"
fi

# li2025CooNonMul
# Cooperative Non-Orthogonal Multiple Access with Index Modulation for Air-Ground ...
# PDF相似度: 100.00%, Markdown相似度: 85.56%
if [ -f "pdfs/li2025CooperativeNonorthogonalMultiple.pdf" ]; then
    mv "pdfs/li2025CooperativeNonorthogonalMultiple.pdf" "pdfs/li2025CooNonMul.pdf"
    echo "✓ PDF重命名: li2025CooperativeNonorthogonalMultiple.pdf -> li2025CooNonMul.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025CooperativeNonorthogonalMultiple.pdf"
fi

if [ -f "markdown/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks.md" ]; then
    mv "markdown/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks.md" "markdown/li2025CooNonMul.md"
    echo "✓ Markdown重命名: Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modula... -> li2025CooNonMul.md"
else
    echo "⚠ Markdown文件不存在: markdown/Cooperative_Non-Orthogonal_Multiple_Access_With_Index_Modulation_for_Air-Ground_Multi-UAV_Networks.md"
fi

# li2025DynRouMec
# Dynamic Routing Mechanism for Load Distribution in UAV
# PDF相似度: 100.00%, Markdown相似度: 76.00%
if [ -f "pdfs/li2025DynamicRoutingMechanism.pdf" ]; then
    mv "pdfs/li2025DynamicRoutingMechanism.pdf" "pdfs/li2025DynRouMec.pdf"
    echo "✓ PDF重命名: li2025DynamicRoutingMechanism.pdf -> li2025DynRouMec.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025DynamicRoutingMechanism.pdf"
fi

# Markdown跳过（相似度较低）: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> li2025DynRouMec.md

# li2025FedMetBas
# Federated Meta-Learning Based Computation Offloading Approach with Energy-Delay ...
# PDF相似度: 100.00%, Markdown相似度: 89.91%
if [ -f "pdfs/li2025FederatedMetalearningBased.pdf" ]; then
    mv "pdfs/li2025FederatedMetalearningBased.pdf" "pdfs/li2025FedMetBas.pdf"
    echo "✓ PDF重命名: li2025FederatedMetalearningBased.pdf -> li2025FedMetBas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025FederatedMetalearningBased.pdf"
fi

if [ -f "markdown/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC.md" ]; then
    mv "markdown/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC.md" "markdown/li2025FedMetBas.md"
    echo "✓ Markdown重命名: Federated_Meta-Learning_Based_Computation_Offloading_Approac... -> li2025FedMetBas.md"
else
    echo "⚠ Markdown文件不存在: markdown/Federated_Meta-Learning_Based_Computation_Offloading_Approach_With_Energy-Delay_Tradeoffs_in_UAV-Assisted_VEC.md"
fi

# li2025TamEveCam
# Taming Event Cameras with Bio-Inspired Architecture and Algorithm: A
# PDF相似度: 100.00%, Markdown相似度: 66.67%
if [ -f "pdfs/li2025TamingEventCameras.pdf" ]; then
    mv "pdfs/li2025TamingEventCameras.pdf" "pdfs/li2025TamEveCam.pdf"
    echo "✓ PDF重命名: li2025TamingEventCameras.pdf -> li2025TamEveCam.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025TamingEventCameras.pdf"
fi

# Markdown跳过（相似度较低）: Li-2025-Taming Event Cameras With Bio-Inspired.md -> li2025TamEveCam.md

# liau2025LasUav
# Laser-Powered UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/liau2025LaserpoweredUAVTrajectory.pdf" ]; then
    mv "pdfs/liau2025LaserpoweredUAVTrajectory.pdf" "pdfs/liau2025LasUav.pdf"
    echo "✓ PDF重命名: liau2025LaserpoweredUAVTrajectory.pdf -> liau2025LasUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liau2025LaserpoweredUAVTrajectory.pdf"
fi

# liu2025DelGooDel
# Delay-Sensitive Goods Delivery and in-Situ Sensing Using a Multi-Task Drone
# PDF相似度: 100.00%, Markdown相似度: 61.16%
if [ -f "pdfs/liu2025DelaysensitiveGoodsDelivery.pdf" ]; then
    mv "pdfs/liu2025DelaysensitiveGoodsDelivery.pdf" "pdfs/liu2025DelGooDel.pdf"
    echo "✓ PDF重命名: liu2025DelaysensitiveGoodsDelivery.pdf -> liu2025DelGooDel.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2025DelaysensitiveGoodsDelivery.pdf"
fi

# Markdown跳过（相似度较低）: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> liu2025DelGooDel.md

# liu2025AHybOpt
# A Hybrid Optimization Framework for Age of Information Minimization in UAV-assis...
# PDF相似度: 100.00%, Markdown相似度: 87.36%
if [ -f "pdfs/liu2025HybridOptimizationFramework.pdf" ]; then
    mv "pdfs/liu2025HybridOptimizationFramework.pdf" "pdfs/liu2025AHybOpt.pdf"
    echo "✓ PDF重命名: liu2025HybridOptimizationFramework.pdf -> liu2025AHybOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2025HybridOptimizationFramework.pdf"
fi

if [ -f "markdown/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS.md" ]; then
    mv "markdown/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS.md" "markdown/liu2025AHybOpt.md"
    echo "✓ Markdown重命名: A_Hybrid_Optimization_Framework_for_Age_of_Information_Minim... -> liu2025AHybOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Hybrid_Optimization_Framework_for_Age_of_Information_Minimization_in_UAV-Assisted_MCS.md"
fi

# liu2025MulMec
# Multi-UAV-assisted MEC
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/liu2025MultiUAVassistedMECInternet.pdf" ]; then
    mv "pdfs/liu2025MultiUAVassistedMECInternet.pdf" "pdfs/liu2025MulMec.pdf"
    echo "✓ PDF重命名: liu2025MultiUAVassistedMECInternet.pdf -> liu2025MulMec.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2025MultiUAVassistedMECInternet.pdf"
fi

# liu2025ResAllFor
# Resource Allocation for Adaptive Beam Alignment in UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 70.79%
if [ -f "pdfs/liu2025ResourceAllocationAdaptive.pdf" ]; then
    mv "pdfs/liu2025ResourceAllocationAdaptive.pdf" "pdfs/liu2025ResAllFor.pdf"
    echo "✓ PDF重命名: liu2025ResourceAllocationAdaptive.pdf -> liu2025ResAllFor.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2025ResourceAllocationAdaptive.pdf"
fi

# Markdown跳过（相似度较低）: Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md -> liu2025ResAllFor.md

# liu2025OnTheRob
# On the Robust Topology Recovery of UAV
# PDF相似度: 100.00%, Markdown相似度: 88.10%
if [ -f "pdfs/liu2025RobustTopologyRecovery.pdf" ]; then
    mv "pdfs/liu2025RobustTopologyRecovery.pdf" "pdfs/liu2025OnTheRob.pdf"
    echo "✓ PDF重命名: liu2025RobustTopologyRecovery.pdf -> liu2025OnTheRob.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2025RobustTopologyRecovery.pdf"
fi

if [ -f "markdown/Liu-2025-On the Robust Topology Recovery of UA.md" ]; then
    mv "markdown/Liu-2025-On the Robust Topology Recovery of UA.md" "markdown/liu2025OnTheRob.md"
    echo "✓ Markdown重命名: Liu-2025-On the Robust Topology Recovery of UA.md -> liu2025OnTheRob.md"
else
    echo "⚠ Markdown文件不存在: markdown/Liu-2025-On the Robust Topology Recovery of UA.md"
fi

# matar2025JoiOptOf
# Joint Optimization of User Association, Power Control, and Dynamic Spectrum Shar...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/matar2025JointOptimizationUser.pdf" ]; then
    mv "pdfs/matar2025JointOptimizationUser.pdf" "pdfs/matar2025JoiOptOf.pdf"
    echo "✓ PDF重命名: matar2025JointOptimizationUser.pdf -> matar2025JoiOptOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/matar2025JointOptimizationUser.pdf"
fi

# mittal2024DepCosUav
# Deployment Cost-Aware UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/mittal2024DeploymentCostawareUAV.pdf" ]; then
    mv "pdfs/mittal2024DeploymentCostawareUAV.pdf" "pdfs/mittal2024DepCosUav.pdf"
    echo "✓ PDF重命名: mittal2024DeploymentCostawareUAV.pdf -> mittal2024DepCosUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/mittal2024DeploymentCostawareUAV.pdf"
fi

# nabi2025JoiOffDec
# Joint Offloading Decision, User Association, and Resource Allocation in Hierarch...
# PDF相似度: 100.00%, Markdown相似度: 82.45%
if [ -f "pdfs/nabi2025JointOffloadingDecision.pdf" ]; then
    mv "pdfs/nabi2025JointOffloadingDecision.pdf" "pdfs/nabi2025JoiOffDec.pdf"
    echo "✓ PDF重命名: nabi2025JointOffloadingDecision.pdf -> nabi2025JoiOffDec.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/nabi2025JointOffloadingDecision.pdf"
fi

if [ -f "markdown/Joint_Offloading_Decision_User_Association_and_Resource_Allocation_in_Hierarchical_Aerial_Computing_Collaboration_of_UAVs_and_HAP.md" ]; then
    mv "markdown/Joint_Offloading_Decision_User_Association_and_Resource_Allocation_in_Hierarchical_Aerial_Computing_Collaboration_of_UAVs_and_HAP.md" "markdown/nabi2025JoiOffDec.md"
    echo "✓ Markdown重命名: Joint_Offloading_Decision_User_Association_and_Resource_Allo... -> nabi2025JoiOffDec.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint_Offloading_Decision_User_Association_and_Resource_Allocation_in_Hierarchical_Aerial_Computing_Collaboration_of_UAVs_and_HAP.md"
fi

# nelson2024RlbEneDat
# RL-Based Energy-Efficient Data Transmission Over Hybrid BLE
# PDF相似度: 100.00%, Markdown相似度: 60.80%
if [ -f "pdfs/nelson2024RLBasedEnergyEfficientData.pdf" ]; then
    mv "pdfs/nelson2024RLBasedEnergyEfficientData.pdf" "pdfs/nelson2024RlbEneDat.pdf"
    echo "✓ PDF重命名: nelson2024RLBasedEnergyEfficientData.pdf -> nelson2024RlbEneDat.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/nelson2024RLBasedEnergyEfficientData.pdf"
fi

# Markdown跳过（相似度较低）: Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md -> nelson2024RlbEneDat.md

# nguyen2024OnTheDil
# On the Dilemma
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/nguyen2024DilemmaReliabilitySecurity.pdf" ]; then
    mv "pdfs/nguyen2024DilemmaReliabilitySecurity.pdf" "pdfs/nguyen2024OnTheDil.pdf"
    echo "✓ PDF重命名: nguyen2024DilemmaReliabilitySecurity.pdf -> nguyen2024OnTheDil.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/nguyen2024DilemmaReliabilitySecurity.pdf"
fi

# ning2024MulDeeRei
# Multi-Agent Deep Reinforcement Learning Based UAV Trajectory Optimization
# PDF相似度: 100.00%, Markdown相似度: 71.94%
if [ -f "pdfs/ning2024MultiAgentDeepReinforcement.pdf" ]; then
    mv "pdfs/ning2024MultiAgentDeepReinforcement.pdf" "pdfs/ning2024MulDeeRei.pdf"
    echo "✓ PDF重命名: ning2024MultiAgentDeepReinforcement.pdf -> ning2024MulDeeRei.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/ning2024MultiAgentDeepReinforcement.pdf"
fi

# Markdown跳过（相似度较低）: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md -> ning2024MulDeeRei.md

# ning2025JoiOptOf
# Joint Optimization of Data Acquisition and Trajectory Planning for UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 81.03%
if [ -f "pdfs/ning2025JointOptimizationData.pdf" ]; then
    mv "pdfs/ning2025JointOptimizationData.pdf" "pdfs/ning2025JoiOptOf.pdf"
    echo "✓ PDF重命名: ning2025JointOptimizationData.pdf -> ning2025JoiOptOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/ning2025JointOptimizationData.pdf"
fi

if [ -f "markdown/Ning 等 - 2025 - Joint Optimization of Data Acquisition and Trajectory Planning for UAV-Assisted Wireless Powered Int.md" ]; then
    mv "markdown/Ning 等 - 2025 - Joint Optimization of Data Acquisition and Trajectory Planning for UAV-Assisted Wireless Powered Int.md" "markdown/ning2025JoiOptOf.md"
    echo "✓ Markdown重命名: Ning 等 - 2025 - Joint Optimization of Data Acquisition and T... -> ning2025JoiOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Ning 等 - 2025 - Joint Optimization of Data Acquisition and Trajectory Planning for UAV-Assisted Wireless Powered Int.md"
fi

# panahi2024RelAndEne
# Reliable and Energy-Efficient UAV Communications
# PDF相似度: 100.00%, Markdown相似度: 78.69%
if [ -f "pdfs/panahi2024ReliableEnergyEfficientUAV.pdf" ]; then
    mv "pdfs/panahi2024ReliableEnergyEfficientUAV.pdf" "pdfs/panahi2024RelAndEne.pdf"
    echo "✓ PDF重命名: panahi2024ReliableEnergyEfficientUAV.pdf -> panahi2024RelAndEne.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/panahi2024ReliableEnergyEfficientUAV.pdf"
fi

# Markdown跳过（相似度较低）: Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md -> panahi2024RelAndEne.md

# qian2024APatPla
# A Path Planning Algorithm for a Crop Monitoring Fixed-Wing Unmanned Aerial Syste...
# PDF相似度: 100.00%, Markdown相似度: 99.39%
if [ -f "pdfs/qian2024PathPlanningAlgorithm.pdf" ]; then
    mv "pdfs/qian2024PathPlanningAlgorithm.pdf" "pdfs/qian2024APatPla.pdf"
    echo "✓ PDF重命名: qian2024PathPlanningAlgorithm.pdf -> qian2024APatPla.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/qian2024PathPlanningAlgorithm.pdf"
fi

if [ -f "markdown/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system..md" ]; then
    mv "markdown/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system..md" "markdown/qian2024APatPla.md"
    echo "✓ Markdown重命名: A path planning algorithm for a crop monitoring fixed-wing u... -> qian2024APatPla.md"
else
    echo "⚠ Markdown文件不存在: markdown/A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system..md"
fi

# qin2022MulReiLea
# Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Comput...
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/qin2022MultiagentReinforcementLearning.pdf" ]; then
    mv "pdfs/qin2022MultiagentReinforcementLearning.pdf" "pdfs/qin2022MulReiLea.pdf"
    echo "✓ PDF重命名: qin2022MultiagentReinforcementLearning.pdf -> qin2022MulReiLea.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/qin2022MultiagentReinforcementLearning.pdf"
fi

if [ -f "markdown/Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things.md" ]; then
    mv "markdown/Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things.md" "markdown/qin2022MulReiLea.md"
    echo "✓ Markdown重命名: Multi-Agent Reinforcement Learning Aided Computation Offload... -> qin2022MulReiLea.md"
else
    echo "⚠ Markdown文件不存在: markdown/Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things.md"
fi

# qin2025MulReiLea
# Multi-Agent Reinforcement Learning in Adversarial Game Environments: Personalize...
# PDF相似度: 100.00%, Markdown相似度: 64.60%
if [ -f "pdfs/qin2025MultiagentReinforcementLearning.pdf" ]; then
    mv "pdfs/qin2025MultiagentReinforcementLearning.pdf" "pdfs/qin2025MulReiLea.pdf"
    echo "✓ PDF重命名: qin2025MultiagentReinforcementLearning.pdf -> qin2025MulReiLea.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/qin2025MultiagentReinforcementLearning.pdf"
fi

# Markdown跳过（相似度较低）: Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md -> qin2025MulReiLea.md

# qiu2024IntHos
# Integrated Host-
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/qiu2024IntegratedHostContentCentric.pdf" ]; then
    mv "pdfs/qiu2024IntegratedHostContentCentric.pdf" "pdfs/qiu2024IntHos.pdf"
    echo "✓ PDF重命名: qiu2024IntegratedHostContentCentric.pdf -> qiu2024IntHos.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/qiu2024IntegratedHostContentCentric.pdf"
fi

# ren2024IntAdaGos
# Intelligent Adaptive Gossip-Based Broadcast Protocol
# PDF相似度: 100.00%, Markdown相似度: 85.47%
if [ -f "pdfs/ren2024IntelligentAdaptiveGossipBased.pdf" ]; then
    mv "pdfs/ren2024IntelligentAdaptiveGossipBased.pdf" "pdfs/ren2024IntAdaGos.pdf"
    echo "✓ PDF重命名: ren2024IntelligentAdaptiveGossipBased.pdf -> ren2024IntAdaGos.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/ren2024IntelligentAdaptiveGossipBased.pdf"
fi

if [ -f "markdown/Ren 等 - 2024 - Intelligent Adaptive Gossip-Based Broadcast Protoc.md" ]; then
    mv "markdown/Ren 等 - 2024 - Intelligent Adaptive Gossip-Based Broadcast Protoc.md" "markdown/ren2024IntAdaGos.md"
    echo "✓ Markdown重命名: Ren 等 - 2024 - Intelligent Adaptive Gossip-Based Broadcast P... -> ren2024IntAdaGos.md"
else
    echo "⚠ Markdown文件不存在: markdown/Ren 等 - 2024 - Intelligent Adaptive Gossip-Based Broadcast Protoc.md"
fi

# rizvi2025MonIntSer
# Monitoring Inter-Drone Service Interference for Resilient Operations
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/rizvi2025MonitoringInterdroneService.pdf" ]; then
    mv "pdfs/rizvi2025MonitoringInterdroneService.pdf" "pdfs/rizvi2025MonIntSer.pdf"
    echo "✓ PDF重命名: rizvi2025MonitoringInterdroneService.pdf -> rizvi2025MonIntSer.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/rizvi2025MonitoringInterdroneService.pdf"
fi

if [ -f "markdown/Monitoring Inter-Drone Service Interference for Resilient Operations.md" ]; then
    mv "markdown/Monitoring Inter-Drone Service Interference for Resilient Operations.md" "markdown/rizvi2025MonIntSer.md"
    echo "✓ Markdown重命名: Monitoring Inter-Drone Service Interference for Resilient Op... -> rizvi2025MonIntSer.md"
else
    echo "⚠ Markdown文件不存在: markdown/Monitoring Inter-Drone Service Interference for Resilient Operations.md"
fi

# shao2024DeeReiLea
# Deep Reinforcement Learning-Based Resource Management for UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/shao2024DeepReinforcementLearningbased.pdf" ]; then
    mv "pdfs/shao2024DeepReinforcementLearningbased.pdf" "pdfs/shao2024DeeReiLea.pdf"
    echo "✓ PDF重命名: shao2024DeepReinforcementLearningbased.pdf -> shao2024DeeReiLea.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/shao2024DeepReinforcementLearningbased.pdf"
fi

# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> shao2024DeeReiLea.md

# shi2024ATwoStr
# A Two-Stage Strategy
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/shi2024TwoStageStrategyUAVenabled.pdf" ]; then
    mv "pdfs/shi2024TwoStageStrategyUAVenabled.pdf" "pdfs/shi2024ATwoStr.pdf"
    echo "✓ PDF重命名: shi2024TwoStageStrategyUAVenabled.pdf -> shi2024ATwoStr.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/shi2024TwoStageStrategyUAVenabled.pdf"
fi

# shi2025SymMar
# Symmetry-Informed MARL
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/shi2025SymmetryinformedMARLDecentralized.pdf" ]; then
    mv "pdfs/shi2025SymmetryinformedMARLDecentralized.pdf" "pdfs/shi2025SymMar.pdf"
    echo "✓ PDF重命名: shi2025SymmetryinformedMARLDecentralized.pdf -> shi2025SymMar.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/shi2025SymmetryinformedMARLDecentralized.pdf"
fi

# singh2024StaMatBas
# Stable Matching Based Revenue Maximization for Federated Learning in UAV-assiste...
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/singh2024StableMatchingBased.pdf" ]; then
    mv "pdfs/singh2024StableMatchingBased.pdf" "pdfs/singh2024StaMatBas.pdf"
    echo "✓ PDF重命名: singh2024StableMatchingBased.pdf -> singh2024StaMatBas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/singh2024StableMatchingBased.pdf"
fi

if [ -f "markdown/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs.md" ]; then
    mv "markdown/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs.md" "markdown/singh2024StaMatBas.md"
    echo "✓ Markdown重命名: Stable Matching Based Revenue Maximization for Federated Lea... -> singh2024StaMatBas.md"
else
    echo "⚠ Markdown文件不存在: markdown/Stable Matching Based Revenue Maximization for Federated Learning in UAV-Assisted WBANs.md"
fi

# song2024EneTraOpt
# Energy-Efficient Trajectory Optimization with Wireless Charging in UAV-assisted ...
# PDF相似度: 100.00%, Markdown相似度: 83.42%
if [ -f "pdfs/song2024EnergyefficientTrajectoryOptimization.pdf" ]; then
    mv "pdfs/song2024EnergyefficientTrajectoryOptimization.pdf" "pdfs/song2024EneTraOpt.pdf"
    echo "✓ PDF重命名: song2024EnergyefficientTrajectoryOptimization.pdf -> song2024EneTraOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/song2024EnergyefficientTrajectoryOptimization.pdf"
fi

if [ -f "markdown/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O.md" ]; then
    mv "markdown/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O.md" "markdown/song2024EneTraOpt.md"
    echo "✓ Markdown重命名: Song 等 - 2024 - Energy-Efficient Trajectory Optimization Wit... -> song2024EneTraOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Song 等 - 2024 - Energy-Efficient Trajectory Optimization With Wireless Charging in UAV-Assisted MEC Based on Multi-O.md"
fi

# song2024MetToAss
# Methods to Assign UAVs
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/song2024MethodsAssignUAVs.pdf" ]; then
    mv "pdfs/song2024MethodsAssignUAVs.pdf" "pdfs/song2024MetToAss.pdf"
    echo "✓ PDF重命名: song2024MethodsAssignUAVs.pdf -> song2024MetToAss.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/song2024MethodsAssignUAVs.pdf"
fi

# soorki2025CatMeIf
# Catch Me If You Can: Deep
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/soorki2025CatchMeIf.pdf" ]; then
    mv "pdfs/soorki2025CatchMeIf.pdf" "pdfs/soorki2025CatMeIf.pdf"
    echo "✓ PDF重命名: soorki2025CatchMeIf.pdf -> soorki2025CatMeIf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/soorki2025CatchMeIf.pdf"
fi

# sun2024AllAutCom
# All-Sky Autonomous Computing in UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/sun2024AllskyAutonomousComputing.pdf" ]; then
    mv "pdfs/sun2024AllskyAutonomousComputing.pdf" "pdfs/sun2024AllAutCom.pdf"
    echo "✓ PDF重命名: sun2024AllskyAutonomousComputing.pdf -> sun2024AllAutCom.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2024AllskyAutonomousComputing.pdf"
fi

# sun2025AerRelCol
# Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Ev...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/sun2025AerialReliableCollaborative.pdf" ]; then
    mv "pdfs/sun2025AerialReliableCollaborative.pdf" "pdfs/sun2025AerRelCol.pdf"
    echo "✓ PDF重命名: sun2025AerialReliableCollaborative.pdf -> sun2025AerRelCol.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2025AerialReliableCollaborative.pdf"
fi

# sun2025JteTex
# J\$\textbackslash text\textbraceleftC
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/sun2025J$textC^5$aServiceDelay.pdf" ]; then
    mv "pdfs/sun2025J$textC^5$aServiceDelay.pdf" "pdfs/sun2025JteTex.pdf"
    echo "✓ PDF重命名: sun2025J$textC^5$aServiceDelay.pdf -> sun2025JteTex.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2025J$textC^5$aServiceDelay.pdf"
fi

# tang2025DeeGraRei
# Deep Graph Reinforcement Learning for UAV-enabled
# PDF相似度: 100.00%, Markdown相似度: 67.18%
if [ -f "pdfs/tang2025DeepGraphReinforcement.pdf" ]; then
    mv "pdfs/tang2025DeepGraphReinforcement.pdf" "pdfs/tang2025DeeGraRei.pdf"
    echo "✓ PDF重命名: tang2025DeepGraphReinforcement.pdf -> tang2025DeeGraRei.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tang2025DeepGraphReinforcement.pdf"
fi

# Markdown跳过（相似度较低）: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md -> tang2025DeeGraRei.md

# tao2024MulCooFor
# Multi-Agent Cooperation for Computing Power Scheduling in UAVs
# PDF相似度: 100.00%, Markdown相似度: 71.26%
if [ -f "pdfs/tao2024MultiagentCooperationComputing.pdf" ]; then
    mv "pdfs/tao2024MultiagentCooperationComputing.pdf" "pdfs/tao2024MulCooFor.pdf"
    echo "✓ PDF重命名: tao2024MultiagentCooperationComputing.pdf -> tao2024MulCooFor.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tao2024MultiagentCooperationComputing.pdf"
fi

# Markdown跳过（相似度较低）: Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md -> tao2024MulCooFor.md

# tian2024UavWirCoo
# UAV-Assisted Wireless Cooperative Communication
# PDF相似度: 100.00%, Markdown相似度: 83.19%
if [ -f "pdfs/tian2024UAVAssistedWirelessCooperative.pdf" ]; then
    mv "pdfs/tian2024UAVAssistedWirelessCooperative.pdf" "pdfs/tian2024UavWirCoo.pdf"
    echo "✓ PDF重命名: tian2024UAVAssistedWirelessCooperative.pdf -> tian2024UavWirCoo.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tian2024UAVAssistedWirelessCooperative.pdf"
fi

if [ -f "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" ]; then
    mv "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" "markdown/tian2024UavWirCoo.md"
    echo "✓ Markdown重命名: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communicat... -> tian2024UavWirCoo.md"
else
    echo "⚠ Markdown文件不存在: markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md"
fi

# tlili2023ANewHyb
# A New Hybrid Adaptive Deep Learning-Based Framework for UAVs
# PDF相似度: 100.00%, Markdown相似度: 80.54%
if [ -f "pdfs/tlili2023NewHybridAdaptive.pdf" ]; then
    mv "pdfs/tlili2023NewHybridAdaptive.pdf" "pdfs/tlili2023ANewHyb.pdf"
    echo "✓ PDF重命名: tlili2023NewHybridAdaptive.pdf -> tlili2023ANewHyb.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tlili2023NewHybridAdaptive.pdf"
fi

if [ -f "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" ]; then
    mv "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" "markdown/tlili2023ANewHyb.md"
    echo "✓ Markdown重命名: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs... -> tlili2023ANewHyb.md"
else
    echo "⚠ Markdown文件不存在: markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md"
fi

# tong2023EneUav
# Energy-Efficient UAV-NOMA
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/tong2023EnergyefficientUAVNOMAAided.pdf" ]; then
    mv "pdfs/tong2023EnergyefficientUAVNOMAAided.pdf" "pdfs/tong2023EneUav.pdf"
    echo "✓ PDF重命名: tong2023EnergyefficientUAVNOMAAided.pdf -> tong2023EneUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tong2023EnergyefficientUAVNOMAAided.pdf"
fi

# trinh2025OptRis
# Optical RISs
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/trinh2025OpticalRISsImprove.pdf" ]; then
    mv "pdfs/trinh2025OpticalRISsImprove.pdf" "pdfs/trinh2025OptRis.pdf"
    echo "✓ PDF重命名: trinh2025OpticalRISsImprove.pdf -> trinh2025OptRis.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/trinh2025OpticalRISsImprove.pdf"
fi

# tun2025JoiUav
# Joint UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/tun2025JointUAVDeployment.pdf" ]; then
    mv "pdfs/tun2025JointUAVDeployment.pdf" "pdfs/tun2025JoiUav.pdf"
    echo "✓ PDF重命名: tun2025JointUAVDeployment.pdf -> tun2025JoiUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/tun2025JointUAVDeployment.pdf"
fi

# wan2025AMulSca
# A Multimodal Scale Normalization Framework for Vision-Radar Small UAV
# PDF相似度: 100.00%, Markdown相似度: 81.33%
if [ -f "pdfs/wan2025MultimodalScaleNormalization.pdf" ]; then
    mv "pdfs/wan2025MultimodalScaleNormalization.pdf" "pdfs/wan2025AMulSca.pdf"
    echo "✓ PDF重命名: wan2025MultimodalScaleNormalization.pdf -> wan2025AMulSca.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wan2025MultimodalScaleNormalization.pdf"
fi

if [ -f "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" ]; then
    mv "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" "markdown/wan2025AMulSca.md"
    echo "✓ Markdown重命名: A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_... -> wan2025AMulSca.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md"
fi

# wang2024AnAda3d
# An Adaptive 3D
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2024Adaptive3DReconstruction.pdf" ]; then
    mv "pdfs/wang2024Adaptive3DReconstruction.pdf" "pdfs/wang2024AnAda3d.pdf"
    echo "✓ PDF重命名: wang2024Adaptive3DReconstruction.pdf -> wang2024AnAda3d.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024Adaptive3DReconstruction.pdf"
fi

# wang2024BioAntCol
# Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading...
# PDF相似度: 100.00%, Markdown相似度: 92.59%
if [ -f "pdfs/wang2024BiobjectiveAntColony.pdf" ]; then
    mv "pdfs/wang2024BiobjectiveAntColony.pdf" "pdfs/wang2024BioAntCol.pdf"
    echo "✓ PDF重命名: wang2024BiobjectiveAntColony.pdf -> wang2024BioAntCol.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024BiobjectiveAntColony.pdf"
fi

if [ -f "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" ]; then
    mv "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" "markdown/wang2024BioAntCol.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Tra... -> wang2024BioAntCol.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md"
fi

# wang2024DecNavWit
# Decentralized Navigation with Heterogeneous Federated Reinforcement Learning for...
# PDF相似度: 100.00%, Markdown相似度: 88.89%
if [ -f "pdfs/wang2024DecentralizedNavigationHeterogeneous.pdf" ]; then
    mv "pdfs/wang2024DecentralizedNavigationHeterogeneous.pdf" "pdfs/wang2024DecNavWit.pdf"
    echo "✓ PDF重命名: wang2024DecentralizedNavigationHeterogeneous.pdf -> wang2024DecNavWit.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024DecentralizedNavigationHeterogeneous.pdf"
fi

if [ -f "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" ]; then
    mv "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" "markdown/wang2024DecNavWit.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Decentralized Navigation With Heterogeneous ... -> wang2024DecNavWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md"
fi

# wang2024ResAllIn
# Resource Allocation in Blockchain Integration of UAV-enabled MEC
# PDF相似度: 100.00%, Markdown相似度: 71.91%
if [ -f "pdfs/wang2024ResourceAllocationBlockchain.pdf" ]; then
    mv "pdfs/wang2024ResourceAllocationBlockchain.pdf" "pdfs/wang2024ResAllIn.pdf"
    echo "✓ PDF重命名: wang2024ResourceAllocationBlockchain.pdf -> wang2024ResAllIn.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024ResourceAllocationBlockchain.pdf"
fi

# Markdown跳过（相似度较低）: Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md -> wang2024ResAllIn.md

# wang2024AUavTru
# A UAV-Assisted Truth Discovery Approach With Incentive Mechanism Design
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2024UAVAssistedTruthDiscovery.pdf" ]; then
    mv "pdfs/wang2024UAVAssistedTruthDiscovery.pdf" "pdfs/wang2024AUavTru.pdf"
    echo "✓ PDF重命名: wang2024UAVAssistedTruthDiscovery.pdf -> wang2024AUavTru.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024UAVAssistedTruthDiscovery.pdf"
fi

# wang2025JoiOptOf
# Joint Optimization of Beamforming and Trajectory for UAV-RIS-assisted MU-MISO
# PDF相似度: 100.00%, Markdown相似度: 76.67%
if [ -f "pdfs/wang2025JointOptimizationBeamforming.pdf" ]; then
    mv "pdfs/wang2025JointOptimizationBeamforming.pdf" "pdfs/wang2025JoiOptOf.pdf"
    echo "✓ PDF重命名: wang2025JointOptimizationBeamforming.pdf -> wang2025JoiOptOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025JointOptimizationBeamforming.pdf"
fi

# Markdown跳过（相似度较低）: Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md -> wang2025JoiOptOf.md

# wang2025JoiPosAnd
# Joint Positioning and Computation Offloading in Multi-UAV MEC
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2025JointPositioningComputation.pdf" ]; then
    mv "pdfs/wang2025JointPositioningComputation.pdf" "pdfs/wang2025JoiPosAnd.pdf"
    echo "✓ PDF重命名: wang2025JointPositioningComputation.pdf -> wang2025JoiPosAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025JointPositioningComputation.pdf"
fi

# wang2025JoiTasOff
# Joint Task Offloading and Migration Optimization in UAV-enabled
# PDF相似度: 100.00%, Markdown相似度: 76.19%
if [ -f "pdfs/wang2025JointTaskOffloading.pdf" ]; then
    mv "pdfs/wang2025JointTaskOffloading.pdf" "pdfs/wang2025JoiTasOff.pdf"
    echo "✓ PDF重命名: wang2025JointTaskOffloading.pdf -> wang2025JoiTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025JointTaskOffloading.pdf"
fi

# Markdown跳过（相似度较低）: Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md -> wang2025JoiTasOff.md

# wang2025OptJoiSpe
# Optimizing Joint Speed and Altitude Schedule for UAV
# PDF相似度: 100.00%, Markdown相似度: 72.16%
if [ -f "pdfs/wang2025OptimizingJointSpeed.pdf" ]; then
    mv "pdfs/wang2025OptimizingJointSpeed.pdf" "pdfs/wang2025OptJoiSpe.pdf"
    echo "✓ PDF重命名: wang2025OptimizingJointSpeed.pdf -> wang2025OptJoiSpe.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025OptimizingJointSpeed.pdf"
fi

# Markdown跳过（相似度较低）: Wang-2025-Optimizing Joint Speed and Altitude.md -> wang2025OptJoiSpe.md

# wang2025SecBeaAnd
# Secure Beamforming and Deployment Design for Rate-Splitting Multiple Access-Base...
# PDF相似度: 100.00%, Markdown相似度: 91.89%
if [ -f "pdfs/wang2025SecureBeamformingDeployment.pdf" ]; then
    mv "pdfs/wang2025SecureBeamformingDeployment.pdf" "pdfs/wang2025SecBeaAnd.pdf"
    echo "✓ PDF重命名: wang2025SecureBeamformingDeployment.pdf -> wang2025SecBeaAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025SecureBeamformingDeployment.pdf"
fi

if [ -f "markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md" ]; then
    mv "markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md" "markdown/wang2025SecBeaAnd.md"
    echo "✓ Markdown重命名: Secure beamforming and deployment design for rate-splitting ... -> wang2025SecBeaAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md"
fi

# wang2025SmaShiPre
# Smart Shield: Prevent
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2025SmartShieldPrevent.pdf" ]; then
    mv "pdfs/wang2025SmartShieldPrevent.pdf" "pdfs/wang2025SmaShiPre.pdf"
    echo "✓ PDF重命名: wang2025SmartShieldPrevent.pdf -> wang2025SmaShiPre.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025SmartShieldPrevent.pdf"
fi

# wei2024HieNetSli
# Hierarchical Network Slicing for UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wei2024HierarchicalNetworkSlicing.pdf" ]; then
    mv "pdfs/wei2024HierarchicalNetworkSlicing.pdf" "pdfs/wei2024HieNetSli.pdf"
    echo "✓ PDF重命名: wei2024HierarchicalNetworkSlicing.pdf -> wei2024HieNetSli.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wei2024HierarchicalNetworkSlicing.pdf"
fi

# wu2024BeaPreBas
# Beamforming Prediction Based on the Multireward DQN
# PDF相似度: 100.00%, Markdown相似度: 64.15%
if [ -f "pdfs/wu2024BeamformingPredictionBased.pdf" ]; then
    mv "pdfs/wu2024BeamformingPredictionBased.pdf" "pdfs/wu2024BeaPreBas.pdf"
    echo "✓ PDF重命名: wu2024BeamformingPredictionBased.pdf -> wu2024BeaPreBas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2024BeamformingPredictionBased.pdf"
fi

# Markdown跳过（相似度较低）: Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md -> wu2024BeaPreBas.md

# wu2025RecIntSur
# Reconfigurable Intelligent Surface Assisted UAV-MCS
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wu2025ReconfigurableIntelligentSurface.pdf" ]; then
    mv "pdfs/wu2025ReconfigurableIntelligentSurface.pdf" "pdfs/wu2025RecIntSur.pdf"
    echo "✓ PDF重命名: wu2025ReconfigurableIntelligentSurface.pdf -> wu2025RecIntSur.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2025ReconfigurableIntelligentSurface.pdf"
fi

# wu2025TwoDeeEne
# Two-Stage Deep Energy Optimization in IRS-assisted UAV-based
# PDF相似度: 100.00%, Markdown相似度: 76.43%
if [ -f "pdfs/wu2025TwostageDeepEnergy.pdf" ]; then
    mv "pdfs/wu2025TwostageDeepEnergy.pdf" "pdfs/wu2025TwoDeeEne.pdf"
    echo "✓ PDF重命名: wu2025TwostageDeepEnergy.pdf -> wu2025TwoDeeEne.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2025TwostageDeepEnergy.pdf"
fi

# Markdown跳过（相似度较低）: Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md -> wu2025TwoDeeEne.md

# xiang2025Emp
# {\emph{EagleEye
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/xiang2025EagleEyeBalancingLatency.pdf" ]; then
    mv "pdfs/xiang2025EagleEyeBalancingLatency.pdf" "pdfs/xiang2025Emp.pdf"
    echo "✓ PDF重命名: xiang2025EagleEyeBalancingLatency.pdf -> xiang2025Emp.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xiang2025EagleEyeBalancingLatency.pdf"
fi

# xie2024ASecUav
# A Secure UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/xie2024SecureUAVCooperative.pdf" ]; then
    mv "pdfs/xie2024SecureUAVCooperative.pdf" "pdfs/xie2024ASecUav.pdf"
    echo "✓ PDF重命名: xie2024SecureUAVCooperative.pdf -> xie2024ASecUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xie2024SecureUAVCooperative.pdf"
fi

# xie2025BloLigCro
# Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 82.93%
if [ -f "pdfs/xie2025BlockchainassistedLightweightCrossdomain.pdf" ]; then
    mv "pdfs/xie2025BlockchainassistedLightweightCrossdomain.pdf" "pdfs/xie2025BloLigCro.pdf"
    echo "✓ PDF重命名: xie2025BlockchainassistedLightweightCrossdomain.pdf -> xie2025BloLigCro.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xie2025BlockchainassistedLightweightCrossdomain.pdf"
fi

if [ -f "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" "markdown/xie2025BloLigCro.md"
    echo "✓ Markdown重命名: Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_... -> xie2025BloLigCro.md"
else
    echo "⚠ Markdown文件不存在: markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md"
fi

# xu2024AHolAnd
# A Holistic and Hybrid Service Selection Strategy for MEC-based UAV
# PDF相似度: 100.00%, Markdown相似度: 71.70%
if [ -f "pdfs/xu2024HolisticHybridService.pdf" ]; then
    mv "pdfs/xu2024HolisticHybridService.pdf" "pdfs/xu2024AHolAnd.pdf"
    echo "✓ PDF重命名: xu2024HolisticHybridService.pdf -> xu2024AHolAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2024HolisticHybridService.pdf"
fi

# Markdown跳过（相似度较低）: A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md -> xu2024AHolAnd.md

# xu2024RewMax
# Reward Maximization
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/xu2024RewardMaximizationDisaster.pdf" ]; then
    mv "pdfs/xu2024RewardMaximizationDisaster.pdf" "pdfs/xu2024RewMax.pdf"
    echo "✓ PDF重命名: xu2024RewardMaximizationDisaster.pdf -> xu2024RewMax.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2024RewardMaximizationDisaster.pdf"
fi

# xu2024SemUav
# Semantic-Aware UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/xu2024SemanticawareUAVSwarm.pdf" ]; then
    mv "pdfs/xu2024SemanticawareUAVSwarm.pdf" "pdfs/xu2024SemUav.pdf"
    echo "✓ PDF重命名: xu2024SemanticawareUAVSwarm.pdf -> xu2024SemUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2024SemanticawareUAVSwarm.pdf"
fi

# xu2025BloGamThe
# Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation ...
# PDF相似度: 100.00%, Markdown相似度: 82.69%
if [ -f "pdfs/xu2025BlockchainempoweredGameTheoretical.pdf" ]; then
    mv "pdfs/xu2025BlockchainempoweredGameTheoretical.pdf" "pdfs/xu2025BloGamThe.pdf"
    echo "✓ PDF重命名: xu2025BlockchainempoweredGameTheoretical.pdf -> xu2025BloGamThe.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2025BlockchainempoweredGameTheoretical.pdf"
fi

if [ -f "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025BloGamThe.md"
    echo "✓ Markdown重命名: Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_B... -> xu2025BloGamThe.md"
else
    echo "⚠ Markdown文件不存在: markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md"
fi

# xu2025TruGamInc
# Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-assis...
# PDF相似度: 100.00%, Markdown相似度: 80.43%
if [ -f "pdfs/xu2025TrustenhancedGameIncentive.pdf" ]; then
    mv "pdfs/xu2025TrustenhancedGameIncentive.pdf" "pdfs/xu2025TruGamInc.pdf"
    echo "✓ PDF重命名: xu2025TrustenhancedGameIncentive.pdf -> xu2025TruGamInc.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2025TrustenhancedGameIncentive.pdf"
fi

if [ -f "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025TruGamInc.md"
    echo "✓ Markdown重命名: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_L... -> xu2025TruGamInc.md"
else
    echo "⚠ Markdown文件不存在: markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md"
fi

# xu2025WinSerPro
# Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/xu2025WindawareServiceProvisioning.pdf" ]; then
    mv "pdfs/xu2025WindawareServiceProvisioning.pdf" "pdfs/xu2025WinSerPro.pdf"
    echo "✓ PDF重命名: xu2025WindawareServiceProvisioning.pdf -> xu2025WinSerPro.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xu2025WindawareServiceProvisioning.pdf"
fi

if [ -f "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" ]; then
    mv "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" "markdown/xu2025WinSerPro.md"
    echo "✓ Markdown重命名: Wind-Aware Service Provisioning Strategy for Multi-Package D... -> xu2025WinSerPro.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md"
fi

# xue2024TowMaxCov
# Towards Maximizing Coverage of Targets for WRSNs
# PDF相似度: 100.00%, Markdown相似度: 67.13%
if [ -f "pdfs/xue2024MaximizingCoverageTargets.pdf" ]; then
    mv "pdfs/xue2024MaximizingCoverageTargets.pdf" "pdfs/xue2024TowMaxCov.pdf"
    echo "✓ PDF重命名: xue2024MaximizingCoverageTargets.pdf -> xue2024TowMaxCov.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/xue2024MaximizingCoverageTargets.pdf"
fi

# Markdown跳过（相似度较低）: Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md -> xue2024TowMaxCov.md

# yang2023RobTraTra
# Robust Transition Trajectory Optimization for Tail-Sitter UAVs
# PDF相似度: 100.00%, Markdown相似度: 82.67%
if [ -f "pdfs/yang2023RobustTransitionTrajectory.pdf" ]; then
    mv "pdfs/yang2023RobustTransitionTrajectory.pdf" "pdfs/yang2023RobTraTra.pdf"
    echo "✓ PDF重命名: yang2023RobustTransitionTrajectory.pdf -> yang2023RobTraTra.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/yang2023RobustTransitionTrajectory.pdf"
fi

if [ -f "markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md" ]; then
    mv "markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md" "markdown/yang2023RobTraTra.md"
    echo "✓ Markdown重命名: Robust transition trajectory optimization for tail-sitter UA... -> yang2023RobTraTra.md"
else
    echo "⚠ Markdown文件不存在: markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md"
fi

# yang2024EneEffTra
# Energy Efficient Transmission Strategy
# PDF相似度: 100.00%, Markdown相似度: 73.08%
if [ -f "pdfs/yang2024EnergyEfficientTransmission.pdf" ]; then
    mv "pdfs/yang2024EnergyEfficientTransmission.pdf" "pdfs/yang2024EneEffTra.pdf"
    echo "✓ PDF重命名: yang2024EnergyEfficientTransmission.pdf -> yang2024EneEffTra.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/yang2024EnergyEfficientTransmission.pdf"
fi

# Markdown跳过（相似度较低）: Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md -> yang2024EneEffTra.md

# yu2025HybTraBas
# Hybrid Transformer Based Multi-Agent Reinforcement Learning for Multiple Unpilot...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/yu2025HybridTransformerBased.pdf" ]; then
    mv "pdfs/yu2025HybridTransformerBased.pdf" "pdfs/yu2025HybTraBas.pdf"
    echo "✓ PDF重命名: yu2025HybridTransformerBased.pdf -> yu2025HybTraBas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/yu2025HybridTransformerBased.pdf"
fi

# yuan2024DynEveFau
# Dynamic Event-Triggered Fault-Tolerant Cooperative Resilient Tracking Control wi...
# PDF相似度: 100.00%, Markdown相似度: 100.00%
if [ -f "pdfs/yuan2024DynamicEventtriggeredFaulttolerant.pdf" ]; then
    mv "pdfs/yuan2024DynamicEventtriggeredFaulttolerant.pdf" "pdfs/yuan2024DynEveFau.pdf"
    echo "✓ PDF重命名: yuan2024DynamicEventtriggeredFaulttolerant.pdf -> yuan2024DynEveFau.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/yuan2024DynamicEventtriggeredFaulttolerant.pdf"
fi

if [ -f "markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md" ]; then
    mv "markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md" "markdown/yuan2024DynEveFau.md"
    echo "✓ Markdown重命名: Dynamic event-triggered fault-tolerant cooperative resilient... -> yuan2024DynEveFau.md"
else
    echo "⚠ Markdown文件不存在: markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md"
fi

# yuan2025TraOptAnd
# Trajectory Optimization and Power Allocation for Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/yuan2025TrajectoryOptimizationPower.pdf" ]; then
    mv "pdfs/yuan2025TrajectoryOptimizationPower.pdf" "pdfs/yuan2025TraOptAnd.pdf"
    echo "✓ PDF重命名: yuan2025TrajectoryOptimizationPower.pdf -> yuan2025TraOptAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/yuan2025TrajectoryOptimizationPower.pdf"
fi

# zeng2025AJoiSec
# A Joint Secure Mechanism of Multi-Task Learning for a UAV
# PDF相似度: 100.00%, Markdown相似度: 70.07%
if [ -f "pdfs/zeng2025JointSecureMechanism.pdf" ]; then
    mv "pdfs/zeng2025JointSecureMechanism.pdf" "pdfs/zeng2025AJoiSec.pdf"
    echo "✓ PDF重命名: zeng2025JointSecureMechanism.pdf -> zeng2025AJoiSec.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zeng2025JointSecureMechanism.pdf"
fi

# Markdown跳过（相似度较低）: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md -> zeng2025AJoiSec.md

# zhan2024IntOnlOpt
# Interference-Aware Online Optimization for Cellular-Connected Multiple UAV
# PDF相似度: 100.00%, Markdown相似度: 77.89%
if [ -f "pdfs/zhan2024InterferenceawareOnlineOptimization.pdf" ]; then
    mv "pdfs/zhan2024InterferenceawareOnlineOptimization.pdf" "pdfs/zhan2024IntOnlOpt.pdf"
    echo "✓ PDF重命名: zhan2024InterferenceawareOnlineOptimization.pdf -> zhan2024IntOnlOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhan2024InterferenceawareOnlineOptimization.pdf"
fi

# Markdown跳过（相似度较低）: Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md -> zhan2024IntOnlOpt.md

# zhan2024TraBetAge
# Tradeoff Between Age
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhan2024TradeoffAgeInformation.pdf" ]; then
    mv "pdfs/zhan2024TradeoffAgeInformation.pdf" "pdfs/zhan2024TraBetAge.pdf"
    echo "✓ PDF重命名: zhan2024TradeoffAgeInformation.pdf -> zhan2024TraBetAge.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhan2024TradeoffAgeInformation.pdf"
fi

# zhan2025OnlEneAnd
# Online Energy and Interference Management for Dynamic Target Tracking with Cellu...
# PDF相似度: 100.00%, Markdown相似度: 88.66%
if [ -f "pdfs/zhan2025OnlineEnergyInterference.pdf" ]; then
    mv "pdfs/zhan2025OnlineEnergyInterference.pdf" "pdfs/zhan2025OnlEneAnd.pdf"
    echo "✓ PDF重命名: zhan2025OnlineEnergyInterference.pdf -> zhan2025OnlEneAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhan2025OnlineEnergyInterference.pdf"
fi

if [ -f "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" ]; then
    mv "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" "markdown/zhan2025OnlEneAnd.md"
    echo "✓ Markdown重命名: Online_Energy_and_Interference_Management_for_Dynamic_Target... -> zhan2025OnlEneAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md"
fi

# zhang2023JoiTasSch
# Joint Task Scheduling and Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2023JointTaskScheduling.pdf" ]; then
    mv "pdfs/zhang2023JointTaskScheduling.pdf" "pdfs/zhang2023JoiTasSch.pdf"
    echo "✓ PDF重命名: zhang2023JointTaskScheduling.pdf -> zhang2023JoiTasSch.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2023JointTaskScheduling.pdf"
fi

# zhang2024HumIrrRis
# Human-Centric Irregular RIS-Assisted Multi-UAV Networks With Resource Allocation
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2024HumanCentricIrregularRISAssisted.pdf" ]; then
    mv "pdfs/zhang2024HumanCentricIrregularRISAssisted.pdf" "pdfs/zhang2024HumIrrRis.pdf"
    echo "✓ PDF重命名: zhang2024HumanCentricIrregularRISAssisted.pdf -> zhang2024HumIrrRis.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2024HumanCentricIrregularRISAssisted.pdf"
fi

# zhang2024IncMec
# Incentive Mechanisms
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2024IncentiveMechanismsOnline.pdf" ]; then
    mv "pdfs/zhang2024IncentiveMechanismsOnline.pdf" "pdfs/zhang2024IncMec.pdf"
    echo "✓ PDF重命名: zhang2024IncentiveMechanismsOnline.pdf -> zhang2024IncMec.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2024IncentiveMechanismsOnline.pdf"
fi

# zhang2024TasOffAnd
# Task Offloading and Trajectory Optimization for Secure Communications in Dynamic...
# PDF相似度: 100.00%, Markdown相似度: 92.09%
if [ -f "pdfs/zhang2024TaskOffloadingTrajectory.pdf" ]; then
    mv "pdfs/zhang2024TaskOffloadingTrajectory.pdf" "pdfs/zhang2024TasOffAnd.pdf"
    echo "✓ PDF重命名: zhang2024TaskOffloadingTrajectory.pdf -> zhang2024TasOffAnd.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2024TaskOffloadingTrajectory.pdf"
fi

if [ -f "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" ]; then
    mv "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" "markdown/zhang2024TasOffAnd.md"
    echo "✓ Markdown重命名: Zhang 等 - 2024 - Task Offloading and Trajectory Optimization... -> zhang2024TasOffAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md"
fi

# zhang2025ImpDatCol
# Improving Data Collection Efficiency of UAV-assisted LoRa
# PDF相似度: 100.00%, Markdown相似度: 65.38%
if [ -f "pdfs/zhang2025ImprovingDataCollection.pdf" ]; then
    mv "pdfs/zhang2025ImprovingDataCollection.pdf" "pdfs/zhang2025ImpDatCol.pdf"
    echo "✓ PDF重命名: zhang2025ImprovingDataCollection.pdf -> zhang2025ImpDatCol.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2025ImprovingDataCollection.pdf"
fi

# Markdown跳过（相似度较低）: Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md -> zhang2025ImpDatCol.md

# zhang2025LarModFor
# Large Models for Aerial Edges: An
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2025LargeModelsAerial.pdf" ]; then
    mv "pdfs/zhang2025LargeModelsAerial.pdf" "pdfs/zhang2025LarModFor.pdf"
    echo "✓ PDF重命名: zhang2025LargeModelsAerial.pdf -> zhang2025LarModFor.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2025LargeModelsAerial.pdf"
fi

# zhang2025MulAerCol
# Multi-Objective Aerial Collaborative Secure Communication Optimization via Gener...
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2025MultiobjectiveAerialCollaborative.pdf" ]; then
    mv "pdfs/zhang2025MultiobjectiveAerialCollaborative.pdf" "pdfs/zhang2025MulAerCol.pdf"
    echo "✓ PDF重命名: zhang2025MultiobjectiveAerialCollaborative.pdf -> zhang2025MulAerCol.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2025MultiobjectiveAerialCollaborative.pdf"
fi

# zhang2025OptMonUti
# Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Ef...
# PDF相似度: 100.00%, Markdown相似度: 89.41%
if [ -f "pdfs/zhang2025OptimizingMonitoringUtility.pdf" ]; then
    mv "pdfs/zhang2025OptimizingMonitoringUtility.pdf" "pdfs/zhang2025OptMonUti.pdf"
    echo "✓ PDF重命名: zhang2025OptimizingMonitoringUtility.pdf -> zhang2025OptMonUti.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2025OptimizingMonitoringUtility.pdf"
fi

if [ -f "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" ]; then
    mv "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" "markdown/zhang2025OptMonUti.md"
    echo "✓ Markdown重命名: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Co... -> zhang2025OptMonUti.md"
else
    echo "⚠ Markdown文件不存在: markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md"
fi

# zhang2025QuaOnlTas
# Quantum-Assisted Online Task Offloading and Resource Allocation in MEC-enabled
# PDF相似度: 100.00%, Markdown相似度: 68.29%
if [ -f "pdfs/zhang2025QuantumassistedOnlineTask.pdf" ]; then
    mv "pdfs/zhang2025QuantumassistedOnlineTask.pdf" "pdfs/zhang2025QuaOnlTas.pdf"
    echo "✓ PDF重命名: zhang2025QuantumassistedOnlineTask.pdf -> zhang2025QuaOnlTas.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2025QuantumassistedOnlineTask.pdf"
fi

# Markdown跳过（相似度较低）: Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md -> zhang2025QuaOnlTas.md

# zhao2024OnDesMul
# On Designing Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhao2024DesigningMultiUAVAided.pdf" ]; then
    mv "pdfs/zhao2024DesigningMultiUAVAided.pdf" "pdfs/zhao2024OnDesMul.pdf"
    echo "✓ PDF重命名: zhao2024DesigningMultiUAVAided.pdf -> zhao2024OnDesMul.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhao2024DesigningMultiUAVAided.pdf"
fi

# zhao2025JoiConCac
# Joint Content Caching, Service Placement, and Task Offloading in UAV-enabled
# PDF相似度: 100.00%, Markdown相似度: 79.17%
if [ -f "pdfs/zhao2025JointContentCaching.pdf" ]; then
    mv "pdfs/zhao2025JointContentCaching.pdf" "pdfs/zhao2025JoiConCac.pdf"
    echo "✓ PDF重命名: zhao2025JointContentCaching.pdf -> zhao2025JoiConCac.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhao2025JointContentCaching.pdf"
fi

# Markdown跳过（相似度较低）: Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md -> zhao2025JoiConCac.md

# zhao2025JoiOptOf
# Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-ass...
# PDF相似度: 100.00%, Markdown相似度: 91.75%
if [ -f "pdfs/zhao2025JointOptimizationTrajectory.pdf" ]; then
    mv "pdfs/zhao2025JointOptimizationTrajectory.pdf" "pdfs/zhao2025JoiOptOf.pdf"
    echo "✓ PDF重命名: zhao2025JointOptimizationTrajectory.pdf -> zhao2025JoiOptOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhao2025JointOptimizationTrajectory.pdf"
fi

if [ -f "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" "markdown/zhao2025JoiOptOf.md"
    echo "✓ Markdown重命名: Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading... -> zhao2025JoiOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md"
fi

# zhao2025AgaMobCol
# Against Mobile Collusive Eavesdroppers: Cooperative
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhao2025MobileCollusiveEavesdroppers.pdf" ]; then
    mv "pdfs/zhao2025MobileCollusiveEavesdroppers.pdf" "pdfs/zhao2025AgaMobCol.pdf"
    echo "✓ PDF重命名: zhao2025MobileCollusiveEavesdroppers.pdf -> zhao2025AgaMobCol.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhao2025MobileCollusiveEavesdroppers.pdf"
fi

# zhao2025AMul
# A Multi-UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhao2025MultiUAVCooperativeTask.pdf" ]; then
    mv "pdfs/zhao2025MultiUAVCooperativeTask.pdf" "pdfs/zhao2025AMul.pdf"
    echo "✓ PDF重命名: zhao2025MultiUAVCooperativeTask.pdf -> zhao2025AMul.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhao2025MultiUAVCooperativeTask.pdf"
fi

# zheng2024ConDelPer
# Content Delivery Performance Analysis
# PDF相似度: 100.00%, Markdown相似度: 71.15%
if [ -f "pdfs/zheng2024ContentDeliveryPerformance.pdf" ]; then
    mv "pdfs/zheng2024ContentDeliveryPerformance.pdf" "pdfs/zheng2024ConDelPer.pdf"
    echo "✓ PDF重命名: zheng2024ContentDeliveryPerformance.pdf -> zheng2024ConDelPer.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zheng2024ContentDeliveryPerformance.pdf"
fi

# Markdown跳过（相似度较低）: Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md -> zheng2024ConDelPer.md

# zheng2024DuaUav
# Dual-Functional UAV-empowered
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zheng2024DualfunctionalUAVempoweredSpaceairground.pdf" ]; then
    mv "pdfs/zheng2024DualfunctionalUAVempoweredSpaceairground.pdf" "pdfs/zheng2024DuaUav.pdf"
    echo "✓ PDF重命名: zheng2024DualfunctionalUAVempoweredSpaceairground.pdf -> zheng2024DuaUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zheng2024DualfunctionalUAVempoweredSpaceairground.pdf"
fi

# zhou2024AFedDig
# A Federated Digital Twin Framework
# PDF相似度: 100.00%, Markdown相似度: 68.00%
if [ -f "pdfs/zhou2024FederatedDigitalTwin.pdf" ]; then
    mv "pdfs/zhou2024FederatedDigitalTwin.pdf" "pdfs/zhou2024AFedDig.pdf"
    echo "✓ PDF重命名: zhou2024FederatedDigitalTwin.pdf -> zhou2024AFedDig.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2024FederatedDigitalTwin.pdf"
fi

# Markdown跳过（相似度较低）: Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md -> zhou2024AFedDig.md

# zhou2024JoiOpt
# Joint Optimization
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2024JointOptimizationMobility.pdf" ]; then
    mv "pdfs/zhou2024JointOptimizationMobility.pdf" "pdfs/zhou2024JoiOpt.pdf"
    echo "✓ PDF重命名: zhou2024JointOptimizationMobility.pdf -> zhou2024JoiOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2024JointOptimizationMobility.pdf"
fi

# zhou2024JoiUav
# Joint UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2024JointUAVTrajectory.pdf" ]; then
    mv "pdfs/zhou2024JointUAVTrajectory.pdf" "pdfs/zhou2024JoiUav.pdf"
    echo "✓ PDF重命名: zhou2024JointUAVTrajectory.pdf -> zhou2024JoiUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2024JointUAVTrajectory.pdf"
fi

# zhou2024SymMulRei
# Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV
# PDF相似度: 100.00%, Markdown相似度: 75.27%
if [ -f "pdfs/zhou2024SymmetryaugmentedMultiagentReinforcement.pdf" ]; then
    mv "pdfs/zhou2024SymmetryaugmentedMultiagentReinforcement.pdf" "pdfs/zhou2024SymMulRei.pdf"
    echo "✓ PDF重命名: zhou2024SymmetryaugmentedMultiagentReinforcement.pdf -> zhou2024SymMulRei.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2024SymmetryaugmentedMultiagentReinforcement.pdf"
fi

# Markdown跳过（相似度较低）: zhou2024SymmetryaugmentedMultiagentReinforcement.md -> zhou2024SymMulRei.md

# zhou2025DigTwiEmp
# Digital Twin Empowered mmWave
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2025DigitalTwinEmpowered.pdf" ]; then
    mv "pdfs/zhou2025DigitalTwinEmpowered.pdf" "pdfs/zhou2025DigTwiEmp.pdf"
    echo "✓ PDF重命名: zhou2025DigitalTwinEmpowered.pdf -> zhou2025DigTwiEmp.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025DigitalTwinEmpowered.pdf"
fi

# zhou2025RelUav
# Reliability-Optimal UAV-assisted
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2025ReliabilityoptimalUAVassistedMobile.pdf" ]; then
    mv "pdfs/zhou2025ReliabilityoptimalUAVassistedMobile.pdf" "pdfs/zhou2025RelUav.pdf"
    echo "✓ PDF重命名: zhou2025ReliabilityoptimalUAVassistedMobile.pdf -> zhou2025RelUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025ReliabilityoptimalUAVassistedMobile.pdf"
fi

# zhou2025UsePreOri
# User Preference Oriented Service Caching and Task Offloading for UAV-assisted ME...
# PDF相似度: 100.00%, Markdown相似度: 83.04%
if [ -f "pdfs/zhou2025UserPreferenceOriented.pdf" ]; then
    mv "pdfs/zhou2025UserPreferenceOriented.pdf" "pdfs/zhou2025UsePreOri.pdf"
    echo "✓ PDF重命名: zhou2025UserPreferenceOriented.pdf -> zhou2025UsePreOri.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025UserPreferenceOriented.pdf"
fi

if [ -f "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" ]; then
    mv "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" "markdown/zhou2025UsePreOri.md"
    echo "✓ Markdown重命名: User_Preference_Oriented_Service_Caching_and_Task_Offloading... -> zhou2025UsePreOri.md"
else
    echo "⚠ Markdown文件不存在: markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md"
fi

# zhu2023AttConOf
# Attitude Control of a Novel Tilt-Wing UAV
# PDF相似度: 100.00%, Markdown相似度: 80.39%
if [ -f "pdfs/zhu2023AttitudeControlNovel.pdf" ]; then
    mv "pdfs/zhu2023AttitudeControlNovel.pdf" "pdfs/zhu2023AttConOf.pdf"
    echo "✓ PDF重命名: zhu2023AttitudeControlNovel.pdf -> zhu2023AttConOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhu2023AttitudeControlNovel.pdf"
fi

if [ -f "markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md" ]; then
    mv "markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md" "markdown/zhu2023AttConOf.md"
    echo "✓ Markdown重命名: Attitude control of a novel tilt-wing UAV in hovering flight... -> zhu2023AttConOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md"
fi

# zhu2024ColReiLea
# Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV
# PDF相似度: 100.00%, Markdown相似度: 76.34%
if [ -f "pdfs/zhu2024CollaborativeReinforcementLearning.pdf" ]; then
    mv "pdfs/zhu2024CollaborativeReinforcementLearning.pdf" "pdfs/zhu2024ColReiLea.pdf"
    echo "✓ PDF重命名: zhu2024CollaborativeReinforcementLearning.pdf -> zhu2024ColReiLea.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhu2024CollaborativeReinforcementLearning.pdf"
fi

# Markdown跳过（相似度较低）: Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md -> zhu2024ColReiLea.md

# zhu2024FisSpeClu
# Fission Spectral Clustering Strategy for UAV
# PDF相似度: 100.00%, Markdown相似度: 85.44%
if [ -f "pdfs/zhu2024FissionSpectralClustering.pdf" ]; then
    mv "pdfs/zhu2024FissionSpectralClustering.pdf" "pdfs/zhu2024FisSpeClu.pdf"
    echo "✓ PDF重命名: zhu2024FissionSpectralClustering.pdf -> zhu2024FisSpeClu.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhu2024FissionSpectralClustering.pdf"
fi

if [ -f "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" ]; then
    mv "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" "markdown/zhu2024FisSpeClu.md"
    echo "✓ Markdown重命名: Fission Spectral Clustering Strategy for UAV Swarm Networks.... -> zhu2024FisSpeClu.md"
else
    echo "⚠ Markdown文件不存在: markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md"
fi

# zhu2025AnEffUav
# An Effective UAV
# PDF相似度: 100.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhu2025EffectiveUAVScheduling.pdf" ]; then
    mv "pdfs/zhu2025EffectiveUAVScheduling.pdf" "pdfs/zhu2025AnEffUav.pdf"
    echo "✓ PDF重命名: zhu2025EffectiveUAVScheduling.pdf -> zhu2025AnEffUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhu2025EffectiveUAVScheduling.pdf"
fi

# chen2025Typ
# TypeFly
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/chen2025TypeFlyLowlatencyDrone.pdf" ]; then
    mv "pdfs/chen2025TypeFlyLowlatencyDrone.pdf" "pdfs/chen2025Typ.pdf"
    echo "✓ PDF重命名: chen2025TypeFlyLowlatencyDrone.pdf -> chen2025Typ.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/chen2025TypeFlyLowlatencyDrone.pdf"
fi

# cong2024Par
# ParallEdge
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/cong2024ParallEdgeExploitingComputingMobility.pdf" ]; then
    mv "pdfs/cong2024ParallEdgeExploitingComputingMobility.pdf" "pdfs/cong2024Par.pdf"
    echo "✓ PDF重命名: cong2024ParallEdgeExploitingComputingMobility.pdf -> cong2024Par.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/cong2024ParallEdgeExploitingComputingMobility.pdf"
fi

# gao2025Csm
# CSMAAC
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/gao2025CSMAACMultiagentReinforcement.pdf" ]; then
    mv "pdfs/gao2025CSMAACMultiagentReinforcement.pdf" "pdfs/gao2025Csm.pdf"
    echo "✓ PDF重命名: gao2025CSMAACMultiagentReinforcement.pdf -> gao2025Csm.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/gao2025CSMAACMultiagentReinforcement.pdf"
fi

# huang2025Ass
# ASSUME
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/huang2025ASSUMEOptimalAlgorithm.pdf" ]; then
    mv "pdfs/huang2025ASSUMEOptimalAlgorithm.pdf" "pdfs/huang2025Ass.pdf"
    echo "✓ PDF重命名: huang2025ASSUMEOptimalAlgorithm.pdf -> huang2025Ass.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/huang2025ASSUMEOptimalAlgorithm.pdf"
fi

# huang2025Li2
# LI2
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/huang2025LI2NewLearningbased.pdf" ]; then
    mv "pdfs/huang2025LI2NewLearningbased.pdf" "pdfs/huang2025Li2.pdf"
    echo "✓ PDF重命名: huang2025LI2NewLearningbased.pdf -> huang2025Li2.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/huang2025LI2NewLearningbased.pdf"
fi

# lam20256d
# 6D
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/lam20256DSelflocalizationDrones.pdf" ]; then
    mv "pdfs/lam20256DSelflocalizationDrones.pdf" "pdfs/lam20256d.pdf"
    echo "✓ PDF重命名: lam20256DSelflocalizationDrones.pdf -> lam20256d.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/lam20256DSelflocalizationDrones.pdf"
fi

# li2024Cod
# CoDetect
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/li2024CoDetectCooperativeAnomaly.pdf" ]; then
    mv "pdfs/li2024CoDetectCooperativeAnomaly.pdf" "pdfs/li2024Cod.pdf"
    echo "✓ PDF重命名: li2024CoDetectCooperativeAnomaly.pdf -> li2024Cod.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2024CoDetectCooperativeAnomaly.pdf"
fi

# li2025Dro
# DroneMA
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/li2025DroneMADroneMobility.pdf" ]; then
    mv "pdfs/li2025DroneMADroneMobility.pdf" "pdfs/li2025Dro.pdf"
    echo "✓ PDF重命名: li2025DroneMADroneMobility.pdf -> li2025Dro.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025DroneMADroneMobility.pdf"
fi

# li2025Uav
# UAV-assisted
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/li2025UAVassistedMicroserviceMobile.pdf" ]; then
    mv "pdfs/li2025UAVassistedMicroserviceMobile.pdf" "pdfs/li2025Uav.pdf"
    echo "✓ PDF重命名: li2025UAVassistedMicroserviceMobile.pdf -> li2025Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025UAVassistedMicroserviceMobile.pdf"
fi

# liao2023Uav
# UAV
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/liao2023UAVSwarmFormation.pdf" ]; then
    mv "pdfs/liao2023UAVSwarmFormation.pdf" "pdfs/liao2023Uav.pdf"
    echo "✓ PDF重命名: liao2023UAVSwarmFormation.pdf -> liao2023Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liao2023UAVSwarmFormation.pdf"
fi

# liu2024Uav
# UAV-assisted
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/liu2024UAVenabledCollaborativeBeamforming.pdf" ]; then
    mv "pdfs/liu2024UAVenabledCollaborativeBeamforming.pdf" "pdfs/liu2024Uav.pdf"
    echo "✓ PDF重命名: liu2024UAVenabledCollaborativeBeamforming.pdf -> liu2024Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2024UAVenabledCollaborativeBeamforming.pdf"
fi

# mao2025Uav
# UAV-assisted
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/mao2025UAVassistedCommunicationsSAGINISAC.pdf" ]; then
    mv "pdfs/mao2025UAVassistedCommunicationsSAGINISAC.pdf" "pdfs/mao2025Uav.pdf"
    echo "✓ PDF重命名: mao2025UAVassistedCommunicationsSAGINISAC.pdf -> mao2025Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/mao2025UAVassistedCommunicationsSAGINISAC.pdf"
fi

# premachandra2024Gan
# GAN
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/premachandra2024GANBasedAudio.pdf" ]; then
    mv "pdfs/premachandra2024GANBasedAudio.pdf" "pdfs/premachandra2024Gan.pdf"
    echo "✓ PDF重命名: premachandra2024GANBasedAudio.pdf -> premachandra2024Gan.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/premachandra2024GANBasedAudio.pdf"
fi

# ren2025Aer
# AeroEcho
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/ren2025AeroEchoAgriculturalLowpower.pdf" ]; then
    mv "pdfs/ren2025AeroEchoAgriculturalLowpower.pdf" "pdfs/ren2025Aer.pdf"
    echo "✓ PDF重命名: ren2025AeroEchoAgriculturalLowpower.pdf -> ren2025Aer.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/ren2025AeroEchoAgriculturalLowpower.pdf"
fi

# roy2025Ser
# Serv-HU
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/roy2025ServHUServiceHandoff.pdf" ]; then
    mv "pdfs/roy2025ServHUServiceHandoff.pdf" "pdfs/roy2025Ser.pdf"
    echo "✓ PDF重命名: roy2025ServHUServiceHandoff.pdf -> roy2025Ser.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/roy2025ServHUServiceHandoff.pdf"
fi

# seth2024Aer
# AeroBridge
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/seth2024AeroBridgeAutonomousDrone.pdf" ]; then
    mv "pdfs/seth2024AeroBridgeAutonomousDrone.pdf" "pdfs/seth2024Aer.pdf"
    echo "✓ PDF重命名: seth2024AeroBridgeAutonomousDrone.pdf -> seth2024Aer.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/seth2024AeroBridgeAutonomousDrone.pdf"
fi

# song2024Aoi
# AoI
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/song2024AoIEnergyTradeoff.pdf" ]; then
    mv "pdfs/song2024AoIEnergyTradeoff.pdf" "pdfs/song2024Aoi.pdf"
    echo "✓ PDF重命名: song2024AoIEnergyTradeoff.pdf -> song2024Aoi.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/song2024AoIEnergyTradeoff.pdf"
fi

# sun2025Tjc
# TJCCT
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/sun2025TJCCTTwotimescaleApproach.pdf" ]; then
    mv "pdfs/sun2025TJCCTTwotimescaleApproach.pdf" "pdfs/sun2025Tjc.pdf"
    echo "✓ PDF重命名: sun2025TJCCTTwotimescaleApproach.pdf -> sun2025Tjc.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2025TJCCTTwotimescaleApproach.pdf"
fi

# wang2024Lsp
# LSPSS
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2024LSPSSConstructingLightweight.pdf" ]; then
    mv "pdfs/wang2024LSPSSConstructingLightweight.pdf" "pdfs/wang2024Lsp.pdf"
    echo "✓ PDF重命名: wang2024LSPSSConstructingLightweight.pdf -> wang2024Lsp.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024LSPSSConstructingLightweight.pdf"
fi

# wang2024Uav
# UAV-assisted
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2024UAVassistedTargetTracking.pdf" ]; then
    mv "pdfs/wang2024UAVassistedTargetTracking.pdf" "pdfs/wang2024Uav.pdf"
    echo "✓ PDF重命名: wang2024UAVassistedTargetTracking.pdf -> wang2024Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024UAVassistedTargetTracking.pdf"
fi

# wang2025Sta
# STAR-RIS
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2025STARRISAidedCovert.pdf" ]; then
    mv "pdfs/wang2025STARRISAidedCovert.pdf" "pdfs/wang2025Sta.pdf"
    echo "✓ PDF重命名: wang2025STARRISAidedCovert.pdf -> wang2025Sta.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025STARRISAidedCovert.pdf"
fi

# wu2024Mac
# MAC
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wu2024MACOptimizationProtocol.pdf" ]; then
    mv "pdfs/wu2024MACOptimizationProtocol.pdf" "pdfs/wu2024Mac.pdf"
    echo "✓ PDF重命名: wu2024MACOptimizationProtocol.pdf -> wu2024Mac.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2024MACOptimizationProtocol.pdf"
fi

# wu2024Mul
# Multi-UAVs
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/wu2024MultiUAVsNetworkDesign.pdf" ]; then
    mv "pdfs/wu2024MultiUAVsNetworkDesign.pdf" "pdfs/wu2024Mul.pdf"
    echo "✓ PDF重命名: wu2024MultiUAVsNetworkDesign.pdf -> wu2024Mul.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2024MultiUAVsNetworkDesign.pdf"
fi

# zeng2024A3d
# A3D
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zeng2024A3DAdaptiveAccurate.pdf" ]; then
    mv "pdfs/zeng2024A3DAdaptiveAccurate.pdf" "pdfs/zeng2024A3d.pdf"
    echo "✓ PDF重命名: zeng2024A3DAdaptiveAccurate.pdf -> zeng2024A3d.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zeng2024A3DAdaptiveAccurate.pdf"
fi

# zhang2024Uav
# UAV
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhang2024UAVSwarmenabledCollaborative.pdf" ]; then
    mv "pdfs/zhang2024UAVSwarmenabledCollaborative.pdf" "pdfs/zhang2024Uav.pdf"
    echo "✓ PDF重命名: zhang2024UAVSwarmenabledCollaborative.pdf -> zhang2024Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhang2024UAVSwarmenabledCollaborative.pdf"
fi

# zheng2024Uav
# UAV
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zheng2024UAVSwarmAir.pdf" ]; then
    mv "pdfs/zheng2024UAVSwarmAir.pdf" "pdfs/zheng2024Uav.pdf"
    echo "✓ PDF重命名: zheng2024UAVSwarmAir.pdf -> zheng2024Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zheng2024UAVSwarmAir.pdf"
fi

# zheng2025Uav
# UAV
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zheng2025UAVSwarmenabledCollaborative.pdf" ]; then
    mv "pdfs/zheng2025UAVSwarmenabledCollaborative.pdf" "pdfs/zheng2025Uav.pdf"
    echo "✓ PDF重命名: zheng2025UAVSwarmenabledCollaborative.pdf -> zheng2025Uav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zheng2025UAVSwarmenabledCollaborative.pdf"
fi

# zhou2025Had
# HaDT
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2025HaDTHardeningDigital.pdf" ]; then
    mv "pdfs/zhou2025HaDTHardeningDigital.pdf" "pdfs/zhou2025Had.pdf"
    echo "✓ PDF重命名: zhou2025HaDTHardeningDigital.pdf -> zhou2025Had.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025HaDTHardeningDigital.pdf"
fi

# zhou2025Llm
# LLM-QL
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2025LLMQLLLMenhancedQlearning.pdf" ]; then
    mv "pdfs/zhou2025LLMQLLLMenhancedQlearning.pdf" "pdfs/zhou2025Llm.pdf"
    echo "✓ PDF重命名: zhou2025LLMQLLLMenhancedQlearning.pdf -> zhou2025Llm.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025LLMQLLLMenhancedQlearning.pdf"
fi

# zhou2025Ver
# VerDT
# PDF相似度: 90.00%, Markdown相似度: 0.00%
if [ -f "pdfs/zhou2025VerDTVersatileDigital.pdf" ]; then
    mv "pdfs/zhou2025VerDTVersatileDigital.pdf" "pdfs/zhou2025Ver.pdf"
    echo "✓ PDF重命名: zhou2025VerDTVersatileDigital.pdf -> zhou2025Ver.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zhou2025VerDTVersatileDigital.pdf"
fi

# li2024MaxNetThr
# Maximizing Network Throughput
# PDF相似度: 87.10%, Markdown相似度: 0.00%
if [ -f "pdfs/li2024MaximizingNetworkThroughput.pdf" ]; then
    mv "pdfs/li2024MaximizingNetworkThroughput.pdf" "pdfs/li2024MaxNetThr.pdf"
    echo "✓ PDF重命名: li2024MaximizingNetworkThroughput.pdf -> li2024MaxNetThr.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2024MaximizingNetworkThroughput.pdf"
fi

# pan2025CooUavRis
# Cooperative UAV-mounted RISs-assisted
# PDF相似度: 85.71%, Markdown相似度: 66.04%
if [ -f "pdfs/pan2025CooperativeUAVmountedRISsassisted.pdf" ]; then
    mv "pdfs/pan2025CooperativeUAVmountedRISsassisted.pdf" "pdfs/pan2025CooUavRis.pdf"
    echo "✓ PDF重命名: pan2025CooperativeUAVmountedRISsassisted.pdf -> pan2025CooUavRis.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/pan2025CooperativeUAVmountedRISsassisted.pdf"
fi

# Markdown跳过（相似度较低）: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> pan2025CooUavRis.md

# sun2024UavSecCom
# UAV-Enabled Secure Communications
# PDF相似度: 85.71%, Markdown相似度: 0.00%
if [ -f "pdfs/sun2024UAVEnabledSecureCommunications.pdf" ]; then
    mv "pdfs/sun2024UAVEnabledSecureCommunications.pdf" "pdfs/sun2024UavSecCom.pdf"
    echo "✓ PDF重命名: sun2024UAVEnabledSecureCommunications.pdf -> sun2024UavSecCom.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2024UAVEnabledSecureCommunications.pdf"
fi

# liu2024SpaIntNet
# Space-Air-Ground Integrated Networks
# PDF相似度: 85.33%, Markdown相似度: 0.00%
if [ -f "pdfs/liu2024SpaceAirGroundIntegratedNetworks.pdf" ]; then
    mv "pdfs/liu2024SpaceAirGroundIntegratedNetworks.pdf" "pdfs/liu2024SpaIntNet.pdf"
    echo "✓ PDF重命名: liu2024SpaceAirGroundIntegratedNetworks.pdf -> liu2024SpaIntNet.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/liu2024SpaceAirGroundIntegratedNetworks.pdf"
fi

# sun2024MulOptFor
# Multi-Objective Optimization for Multi-UAV-assisted
# PDF相似度: 84.00%, Markdown相似度: 76.52%
if [ -f "pdfs/sun2024MultiobjectiveOptimizationMultiUAVassisted.pdf" ]; then
    mv "pdfs/sun2024MultiobjectiveOptimizationMultiUAVassisted.pdf" "pdfs/sun2024MulOptFor.pdf"
    echo "✓ PDF重命名: sun2024MultiobjectiveOptimizationMultiUAVassisted.pdf -> sun2024MulOptFor.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/sun2024MultiobjectiveOptimizationMultiUAVassisted.pdf"
fi

# Markdown跳过（相似度较低）: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md -> sun2024MulOptFor.md

# guo2025JoiTraPla
# Joint Trajectory Planning
# PDF相似度: 83.64%, Markdown相似度: 0.00%
if [ -f "pdfs/guo2025JointTrajectoryPlanning.pdf" ]; then
    mv "pdfs/guo2025JointTrajectoryPlanning.pdf" "pdfs/guo2025JoiTraPla.pdf"
    echo "✓ PDF重命名: guo2025JointTrajectoryPlanning.pdf -> guo2025JoiTraPla.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/guo2025JointTrajectoryPlanning.pdf"
fi

# dai2024UavTasOff
# UAV-Assisted Task Offloading
# PDF相似度: 83.33%, Markdown相似度: 62.16%
if [ -f "pdfs/dai2024UAVAssistedTaskOffloading.pdf" ]; then
    mv "pdfs/dai2024UAVAssistedTaskOffloading.pdf" "pdfs/dai2024UavTasOff.pdf"
    echo "✓ PDF重命名: dai2024UAVAssistedTaskOffloading.pdf -> dai2024UavTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/dai2024UAVAssistedTaskOffloading.pdf"
fi

# Markdown跳过（相似度较低）: Zhang-2025-Quantum-Assisted Online Task Offloa.md -> dai2024UavTasOff.md

# wang2024WirPowMet
# Wireless Powered Metaverse
# PDF相似度: 82.76%, Markdown相似度: 0.00%
if [ -f "pdfs/wang2024WirelessPoweredMetaverse.pdf" ]; then
    mv "pdfs/wang2024WirelessPoweredMetaverse.pdf" "pdfs/wang2024WirPowMet.pdf"
    echo "✓ PDF重命名: wang2024WirelessPoweredMetaverse.pdf -> wang2024WirPowMet.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2024WirelessPoweredMetaverse.pdf"
fi

# zema20243dTraOpt
# 3D Trajectory Optimization
# PDF相似度: 82.76%, Markdown相似度: 0.00%
if [ -f "pdfs/zema20243DTrajectoryOptimization.pdf" ]; then
    mv "pdfs/zema20243DTrajectoryOptimization.pdf" "pdfs/zema20243dTraOpt.pdf"
    echo "✓ PDF重命名: zema20243DTrajectoryOptimization.pdf -> zema20243dTraOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/zema20243DTrajectoryOptimization.pdf"
fi

# li2025ExpTheRob
# Exploring the Robustness: Hierarchical
# PDF相似度: 82.67%, Markdown相似度: 0.00%
if [ -f "pdfs/li2025ExploringRobustnessHierarchical.pdf" ]; then
    mv "pdfs/li2025ExploringRobustnessHierarchical.pdf" "pdfs/li2025ExpTheRob.pdf"
    echo "✓ PDF重命名: li2025ExploringRobustnessHierarchical.pdf -> li2025ExpTheRob.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2025ExploringRobustnessHierarchical.pdf"
fi

# li2024MulOpt
# Multi-Objective Optimization
# PDF相似度: 82.54%, Markdown相似度: 60.87%
if [ -f "pdfs/li2024MultiObjectiveOptimizationUAV.pdf" ]; then
    mv "pdfs/li2024MultiObjectiveOptimizationUAV.pdf" "pdfs/li2024MulOpt.pdf"
    echo "✓ PDF重命名: li2024MultiObjectiveOptimizationUAV.pdf -> li2024MulOpt.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2024MultiObjectiveOptimizationUAV.pdf"
fi

# Markdown跳过（相似度较低）: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md -> li2024MulOpt.md

# shen2024SliTasOff
# Slicing-Based Task Offloading
# PDF相似度: 82.54%, Markdown相似度: 82.54%
if [ -f "pdfs/shen2024SlicingBasedTaskOffloading.pdf" ]; then
    mv "pdfs/shen2024SlicingBasedTaskOffloading.pdf" "pdfs/shen2024SliTasOff.pdf"
    echo "✓ PDF重命名: shen2024SlicingBasedTaskOffloading.pdf -> shen2024SliTasOff.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/shen2024SlicingBasedTaskOffloading.pdf"
fi

if [ -f "markdown/shen2024SlicingBasedTaskOffloading.md" ]; then
    mv "markdown/shen2024SlicingBasedTaskOffloading.md" "markdown/shen2024SliTasOff.md"
    echo "✓ Markdown重命名: shen2024SlicingBasedTaskOffloading.md -> shen2024SliTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/shen2024SlicingBasedTaskOffloading.md"
fi

# xu2023TamEveCam
# Taming Event Cameras
# PDF相似度: 81.82%, Markdown相似度: 60.61%
# Markdown跳过（相似度较低）: Li-2025-Taming Event Cameras With Bio-Inspired.md -> xu2023TamEveCam.md

# wang2025PraOptUav
# Practical Optimizing UAV
# PDF相似度: 81.48%, Markdown相似度: 69.57%
if [ -f "pdfs/wang2025PracticalOptimizingUAV.pdf" ]; then
    mv "pdfs/wang2025PracticalOptimizingUAV.pdf" "pdfs/wang2025PraOptUav.pdf"
    echo "✓ PDF重命名: wang2025PracticalOptimizingUAV.pdf -> wang2025PraOptUav.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wang2025PracticalOptimizingUAV.pdf"
fi

# Markdown跳过（相似度较低）: Wang-2025-Practical Optimizing UAV Trajectory.md -> wang2025PraOptUav.md

# wu2025SecDesOf
# Security-Aware Designs of Multi-UAV
# PDF相似度: 81.16%, Markdown相似度: 0.00%
if [ -f "pdfs/wu2025SecurityawareDesignsMultiUAV.pdf" ]; then
    mv "pdfs/wu2025SecurityawareDesignsMultiUAV.pdf" "pdfs/wu2025SecDesOf.pdf"
    echo "✓ PDF重命名: wu2025SecurityawareDesignsMultiUAV.pdf -> wu2025SecDesOf.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/wu2025SecurityawareDesignsMultiUAV.pdf"
fi

# li2024OptDro
# Optics-Driven Drone
# PDF相似度: 80.95%, Markdown相似度: 0.00%
if [ -f "pdfs/li2024OpticsdrivenDrone.pdf" ]; then
    mv "pdfs/li2024OpticsdrivenDrone.pdf" "pdfs/li2024OptDro.pdf"
    echo "✓ PDF重命名: li2024OpticsdrivenDrone.pdf -> li2024OptDro.pdf"
else
    echo "⚠ PDF文件不存在: pdfs/li2024OpticsdrivenDrone.pdf"
fi

# dai2023MulDeeRei
# Multi-Agent Deep Reinforcement Learning
# PDF相似度: 80.52%, Markdown相似度: 74.29%
# Markdown跳过（相似度较低）: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md -> dai2023MulDeeRei.md

# wang2024EnsThrAoi
# Ensuring Threshold AoI
# PDF相似度: 80.00%, Markdown相似度: 0.00%
# PDF跳过（相似度较低）: wang2024EnsuringThresholdAoI.pdf -> wang2024EnsThrAoi.pdf

# li2023MulOptApp
# Multi-Objective Optimization Approaches
# PDF相似度: 72.97%, Markdown相似度: 64.08%
# Markdown跳过（相似度较低）: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md -> li2023MulOptApp.md

# krishna moorthy2022EsnReiLea
# ESN Reinforcement Learning
# PDF相似度: 71.88%, Markdown相似度: 68.75%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> krishna moorthy2022EsnReiLea.md

# zheng2021ComReiLea
# Combining Reinforcement Learning
# PDF相似度: 71.43%, Markdown相似度: 62.86%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> zheng2021ComReiLea.md

# zhu2024MulDepOpt
# Multi-Objective Deployment Optimization of UAVs
# PDF相似度: 70.73%, Markdown相似度: 63.06%
# Markdown跳过（相似度较低）: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md -> zhu2024MulDepOpt.md

# peng2021MulReiLea
# Multi-Agent Reinforcement Learning Based Resource Management
# PDF相似度: 63.27%, Markdown相似度: 68.25%
# Markdown跳过（相似度较低）: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md -> peng2021MulReiLea.md

# ferdowsi2021NeuComDee
# Neural Combinatorial Deep Reinforcement Learning
# PDF相似度: 62.79%, Markdown相似度: 62.79%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> ferdowsi2021NeuComDee.md

# song2023EvoMulRei
# Evolutionary Multi-Objective Reinforcement Learning Based Trajectory Control
# PDF相似度: 0.00%, Markdown相似度: 61.97%
# Markdown跳过（相似度较低）: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md -> song2023EvoMulRei.md

# hoang2023DeeReiLea
# Deep Reinforcement Learning-Based Online Resource Management
# PDF相似度: 61.22%, Markdown相似度: 61.22%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> hoang2023DeeReiLea.md

# wang2022DeeReiLea
# Deep Reinforcement Learning Based Dynamic Trajectory Control
# PDF相似度: 61.22%, Markdown相似度: 61.22%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> wang2022DeeReiLea.md

# hsu2022ReiLeaCol
# Reinforcement Learning-Based Collision Avoidance
# PDF相似度: 60.47%, Markdown相似度: 60.47%
# Markdown跳过（相似度较低）: shao2024DeepReinforcementLearningbased.md -> hsu2022ReiLeaCol.md


echo "=================================================="
echo "文件重命名完成！共处理 207 个文献"
echo "高质量匹配: 194 个"
echo "=================================================="
echo "PDF文件在: pdfs/"
echo "Markdown文件在: markdown/"
echo "请检查重命名结果。"