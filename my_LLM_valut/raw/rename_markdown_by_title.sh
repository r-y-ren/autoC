#!/bin/bash
# 通过标题匹配bib文件，使用citation key重命名Markdown文件
#
# 共处理 187 个Markdown文件
#
set -e  # 遇到错误立即退出

cd /Users/wupengfei/Downloads/my_LLM_valut/raw

echo "开始Markdown文件重命名..."

# 原文件: 1570937393.md
# Markdown标题: An Online Joint Optimization Approach for QoE Maximization in UAVEnabled Mobile ...
# 匹配的bib标题: An Online Joint Optimization Approach for QoE
# 相似度: 64.75%
# Citation key: he2024OnlineJointOptimization
# 新文件名: he2024OnlineJointOptimization.md
if [ -f "markdown/1570937393.md" ]; then
    mv "markdown/1570937393.md" "markdown/he2024OnlineJointOptimization.md"
    echo "✓ 重命名: 1570937393.md -> he2024OnlineJointOptimization.md"
else
    echo "⚠ 文件不存在: markdown/1570937393.md"
fi

# 无法处理: 1570937499.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 29.27%)

# 原文件: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md
# Markdown标题: A New Hybrid Adaptive Deep LearningBased Framework for UAVs Faults and Attacks D...
# 匹配的bib标题: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs
# 相似度: 80.27%
# Citation key: tlili2023NewHybridAdaptive
# 新文件名: tlili2023NewHybridAdaptive.md
if [ -f "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" ]; then
    mv "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" "markdown/tlili2023NewHybridAdaptive.md"
    echo "✓ 重命名: A New Hybrid Adaptive Deep Learning-Based Framewor... -> tlili2023NewHybridAdaptive.md"
else
    echo "⚠ 文件不存在: markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md"
fi

# 无法处理: ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 41.79%)

# 无法处理: A_Fast_UAV_Trajectory_Planning_Framework_in_RIS-Assisted_Communication_Systems_With_Accelerated_Learning_via_Multithreading_and_Federating.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.81%)

# 原文件: A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md
# Markdown标题: A Holistic and Hybrid Service Selection Strategy for MECBased UAV LastMile Deliv...
# 匹配的bib标题: A Holistic and Hybrid Service Selection Strategy for MEC-based UAV
# 相似度: 83.33%
# Citation key: xu2024HolisticHybridService
# 新文件名: xu2024HolisticHybridService.md
if [ -f "markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md" ]; then
    mv "markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md" "markdown/xu2024HolisticHybridService.md"
    echo "✓ 重命名: A_Holistic_and_Hybrid_Service_Selection_Strategy_f... -> xu2024HolisticHybridService.md"
else
    echo "⚠ 文件不存在: markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md"
fi

# 原文件: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md
# Markdown标题: A Joint Secure Mechanism of MultiTask Learning for a UAV Team Under FDI Attacks
# 匹配的bib标题: A Joint Secure Mechanism of Multi-Task Learning for a UAV
# 相似度: 82.96%
# Citation key: zeng2025JointSecureMechanism
# 新文件名: zeng2025JointSecureMechanism.md
if [ -f "markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md" ]; then
    mv "markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md" "markdown/zeng2025JointSecureMechanism.md"
    echo "✓ 重命名: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_fo... -> zeng2025JointSecureMechanism.md"
else
    echo "⚠ 文件不存在: markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md"
fi

# 无法处理: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.62%)

# 原文件: A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md
# Markdown标题: A Multimodal Scale Normalization Framework for VisionRadar Small UAV Positioning
# 匹配的bib标题: A Multimodal Scale Normalization Framework for Vision-Radar Small UAV
# 相似度: 91.89%
# Citation key: wan2025MultimodalScaleNormalization
# 新文件名: wan2025MultimodalScaleNormalization.md
if [ -f "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" ]; then
    mv "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" "markdown/wan2025MultimodalScaleNormalization.md"
    echo "✓ 重命名: A_Multimodal_Scale_Normalization_Framework_for_Vis... -> wan2025MultimodalScaleNormalization.md"
else
    echo "⚠ 文件不存在: markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md"
fi

# 无法处理: A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 39.53%)

# 原文件: A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md
# Markdown标题: A ResourceEfficient Content Sharing Mechanism in LargeScale UAV Named Data Netwo...
# 匹配的bib标题: A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV
# 相似度: 85.14%
# Citation key: jin2025ResourceefficientContentSharing
# 新文件名: jin2025ResourceefficientContentSharing.md
if [ -f "markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md" ]; then
    mv "markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md" "markdown/jin2025ResourceefficientContentSharing.md"
    echo "✓ 重命名: A_Resource-Efficient_Content_Sharing_Mechanism_in_... -> jin2025ResourceefficientContentSharing.md"
else
    echo "⚠ 文件不存在: markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md"
fi

# 无法处理: Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.74%)

# 无法处理: AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 41.94%)

# 原文件: Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md
# Markdown标题: Against Mobile Collusive Eavesdroppers Cooperative Secure Transmission and Compu...
# 匹配的bib标题: Against Mobile Collusive Eavesdroppers: Cooperative
# 相似度: 60.98%
# Citation key: zhao2025MobileCollusiveEavesdroppers
# 新文件名: zhao2025MobileCollusiveEavesdroppers.md
if [ -f "markdown/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md" ]; then
    mv "markdown/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md" "markdown/zhao2025MobileCollusiveEavesdroppers.md"
    echo "✓ 重命名: Against_Mobile_Collusive_Eavesdroppers_Cooperative... -> zhao2025MobileCollusiveEavesdroppers.md"
else
    echo "⚠ 文件不存在: markdown/Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md"
fi

# 原文件: Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md
# Markdown标题: Age of InformationAware MultiObjective Optimization for Heterogeneous UAVUSVUUV ...
# 匹配的bib标题: Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-...
# 相似度: 80.61%
# Citation key: hou2025AgeInformationawareMultiobjective
# 新文件名: hou2025AgeInformationawareMultiobjective.md
if [ -f "markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md" ]; then
    mv "markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md" "markdown/hou2025AgeInformationawareMultiobjective.md"
    echo "✓ 重命名: Age_of_Information-Aware_Multi-Objective_Optimizat... -> hou2025AgeInformationawareMultiobjective.md"
else
    echo "⚠ 文件不存在: markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md"
fi

# 原文件: Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md
# Markdown标题: Joint Trajectory Control Frequency Allocation and Routing for UAV Swarm Networks...
# 匹配的bib标题: Joint Trajectory Control, Frequency Allocation, and Routing for UAV
# 相似度: 66.67%
# Citation key: alam2024JointTrajectoryControl
# 新文件名: alam2024JointTrajectoryControl.md
if [ -f "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" ]; then
    mv "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" "markdown/alam2024JointTrajectoryControl.md"
    echo "✓ 重命名: Alam和Moh - 2024 - Joint Trajectory Control, Freque... -> alam2024JointTrajectoryControl.md"
else
    echo "⚠ 文件不存在: markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md"
fi

# 原文件: An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md
# Markdown标题: RESEARCH PAPER
# 匹配的bib标题: RF-Search
# 相似度: 63.64%
# Citation key: zhang2023RFSearchSearchingUnconscious
# 新文件名: zhang2023RFSearchSearchingUnconscious.md
if [ -f "markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md" ]; then
    mv "markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md" "markdown/zhang2023RFSearchSearchingUnconscious.md"
    echo "✓ 重命名: An adaptive 3D reconstruction method for asymmetri... -> zhang2023RFSearchSearchingUnconscious.md"
else
    echo "⚠ 文件不存在: markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md"
fi

# 无法处理: Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 34.15%)

# 无法处理: Attitude control of a novel tilt-wing UAV in hovering flight..md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 50.00%)

# 原文件: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md
# Markdown标题: DelayAware Cooperative Task Offloading for MultiUAV Enabled EdgeCloud Computing
# 匹配的bib标题: Delay-Aware Cooperative Task Offloading
# 相似度: 64.96%
# Citation key: bai2024DelayAwareCooperativeTask
# 新文件名: bai2024DelayAwareCooperativeTask.md
if [ -f "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" ]; then
    mv "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" "markdown/bai2024DelayAwareCooperativeTask.md"
    echo "✓ 重命名: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloa... -> bai2024DelayAwareCooperativeTask.md"
else
    echo "⚠ 文件不存在: markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md"
fi

# 无法处理: Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.27%)

# 原文件: Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md
# Markdown标题: BlockchainAssisted Lightweight CrossDomain Authentication for MultiUAV Wireless ...
# 匹配的bib标题: Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV
# 相似度: 88.61%
# Citation key: xie2025BlockchainassistedLightweightCrossdomain
# 新文件名: xie2025BlockchainassistedLightweightCrossdomain.md
if [ -f "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" "markdown/xie2025BlockchainassistedLightweightCrossdomain.md"
    echo "✓ 重命名: Blockchain-Assisted_Lightweight_Cross-Domain_Authe... -> xie2025BlockchainassistedLightweightCrossdomain.md"
else
    echo "⚠ 文件不存在: markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md"
fi

# 原文件: Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md
# Markdown标题: BlockchainEmpowered Game Theoretical Incentive for Secure Bandwidth Allocation i...
# 匹配的bib标题: Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation ...
# 相似度: 91.18%
# Citation key: xu2025BlockchainempoweredGameTheoretical
# 新文件名: xu2025BlockchainempoweredGameTheoretical.md
if [ -f "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025BlockchainempoweredGameTheoretical.md"
    echo "✓ 重命名: Blockchain-Empowered_Game_Theoretical_Incentive_fo... -> xu2025BlockchainempoweredGameTheoretical.md"
else
    echo "⚠ 文件不存在: markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md"
fi

# 无法处理: Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 45.30%)

# 原文件: Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md
# Markdown标题: MultiUser Task Offloading in UAVAssisted LEO Satellite Edge Computing A GameTheo...
# 匹配的bib标题: Multi-User Task Offloading in UAV-assisted LEO
# 相似度: 63.77%
# Citation key: chen2025MultiuserTaskOffloading
# 新文件名: chen2025MultiuserTaskOffloading.md
if [ -f "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" ]; then
    mv "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" "markdown/chen2025MultiuserTaskOffloading.md"
    echo "✓ 重命名: Chen 等 - 2025 - Multi-User Task Offloading in UAV-... -> chen2025MultiuserTaskOffloading.md"
else
    echo "⚠ 文件不存在: markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md"
fi

# 无法处理: Chen-2025-TypeFly_ Low-Latency Drone Planning.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.92%)

# 原文件: CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md
# Markdown标题: LETTER
# 匹配的bib标题: Let's Trade
# 相似度: 62.50%
# Citation key: liwang2021LetsTradeFuture
# 新文件名: liwang2021LetsTradeFuture.md
if [ -f "markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md" ]; then
    mv "markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md" "markdown/liwang2021LetsTradeFuture.md"
    echo "✓ 重命名: CoDetect cooperative anomaly detection with privac... -> liwang2021LetsTradeFuture.md"
else
    echo "⚠ 文件不存在: markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md"
fi

# 无法处理: Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 44.44%)

# 原文件: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# Markdown标题: Cooperative UAVMounted RISsAssisted EnergyEfficient Communications
# 匹配的bib标题: Cooperative UAV-mounted RISs-assisted
# 相似度: 69.31%
# Citation key: pan2025CooperativeUAVmountedRISsassisted
# 新文件名: pan2025CooperativeUAVmountedRISsassisted.md
if [ -f "markdown/Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md" ]; then
    mv "markdown/Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md" "markdown/pan2025CooperativeUAVmountedRISsassisted.md"
    echo "✓ 重命名: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Effic... -> pan2025CooperativeUAVmountedRISsassisted.md"
else
    echo "⚠ 文件不存在: markdown/Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md"
fi

# 无法处理: Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 59.34%)

# 原文件: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md
# Markdown标题: Deep Graph Reinforcement Learning for UAVEnabled MultiUser Secure Communications
# 匹配的bib标题: Deep Graph Reinforcement Learning for UAV-enabled
# 相似度: 75.00%
# Citation key: tang2025DeepGraphReinforcement
# 新文件名: tang2025DeepGraphReinforcement.md
if [ -f "markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md" ]; then
    mv "markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md" "markdown/tang2025DeepGraphReinforcement.md"
    echo "✓ 重命名: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_... -> tang2025DeepGraphReinforcement.md"
else
    echo "⚠ 文件不存在: markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md"
fi

# 无法处理: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.72%)

# 原文件: Dou-2025-Scheduling Drone and Mobile Charger v.md
# Markdown标题: Scheduling Drone and Mobile Charger via HybridAction Deep Reinforcement Learning
# 匹配的bib标题: Scheduling Drone and Mobile Charger via Hybrid-Action Deep Reinforcement Learnin...
# 相似度: 100.00%
# Citation key: dou2025SchedulingDroneMobile
# 新文件名: dou2025SchedulingDroneMobile.md
if [ -f "markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md" ]; then
    mv "markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md" "markdown/dou2025SchedulingDroneMobile.md"
    echo "✓ 重命名: Dou-2025-Scheduling Drone and Mobile Charger v.md -> dou2025SchedulingDroneMobile.md"
else
    echo "⚠ 文件不存在: markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md"
fi

# 无法处理: Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 38.82%)

# 无法处理: DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.37%)

# 无法处理: Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md
# 原因: Citation key zhang2023RFSearchSearchingUnconscious 已被使用

# 原文件: Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md
# Markdown标题: Dynamic Routing Mechanism for Load Distribution in UAV Swarm Networks With Edge ...
# 匹配的bib标题: Dynamic Routing Mechanism for Load Distribution in UAV
# 相似度: 76.60%
# Citation key: li2025DynamicRoutingMechanism
# 新文件名: li2025DynamicRoutingMechanism.md
if [ -f "markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md" ]; then
    mv "markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md" "markdown/li2025DynamicRoutingMechanism.md"
    echo "✓ 重命名: Dynamic_Routing_Mechanism_for_Load_Distribution_in... -> li2025DynamicRoutingMechanism.md"
else
    echo "⚠ 文件不存在: markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md"
fi

# 无法处理: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 59.26%)

# 无法处理: Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md
# 原因: Citation key zhang2023RFSearchSearchingUnconscious 已被使用

# 无法处理: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 53.24%)

# 原文件: Fission Spectral Clustering Strategy for UAV Swarm Networks.md
# Markdown标题: Fission Spectral Clustering Strategy for UAV Swarm Networks
# 匹配的bib标题: Fission Spectral Clustering Strategy for UAV
# 相似度: 85.44%
# Citation key: zhu2024FissionSpectralClustering
# 新文件名: zhu2024FissionSpectralClustering.md
if [ -f "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" ]; then
    mv "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" "markdown/zhu2024FissionSpectralClustering.md"
    echo "✓ 重命名: Fission Spectral Clustering Strategy for UAV Swarm... -> zhu2024FissionSpectralClustering.md"
else
    echo "⚠ 文件不存在: markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md"
fi

# 无法处理: Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.35%)

# 无法处理: Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 52.25%)

# 无法处理: Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 49.54%)

# 原文件: Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md
# Markdown标题: Coverage Probability and Throughput Optimization in Integrated mmWave and Sub6 G...
# 匹配的bib标题: Coverage Probability and Throughput Optimization in Integrated mmWave
# 相似度: 71.50%
# Citation key: gui2024CoverageProbabilityThroughput
# 新文件名: gui2024CoverageProbabilityThroughput.md
if [ -f "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" ]; then
    mv "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" "markdown/gui2024CoverageProbabilityThroughput.md"
    echo "✓ 重命名: Gui和Cai - 2024 - Coverage Probability and Throughp... -> gui2024CoverageProbabilityThroughput.md"
else
    echo "⚠ 文件不存在: markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md"
fi

# 无法处理: Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 59.67%)

# 无法处理: Guo-2025-Mighty_ Towards Long-Range and High-T.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.37%)

# 无法处理: HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 42.96%)

# 无法处理: Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 56.69%)

# 无法处理: He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.22%)

# 无法处理: Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.24%)

# 无法处理: Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.54%)

# 原文件: IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md
# Markdown标题: AllSky Autonomous Computing in UAV Swarm
# 匹配的bib标题: All-Sky Autonomous Computing in UAV
# 相似度: 91.89%
# Citation key: sun2024AllskyAutonomousComputing
# 新文件名: sun2024AllskyAutonomousComputing.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" "markdown/sun2024AllskyAutonomousComputing.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - All... -> sun2024AllskyAutonomousComputing.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md"
fi

# 原文件: IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md
# Markdown标题: Joint Task Offloading Resource Allocation and Trajectory Design for MultiUAV Coo...
# 匹配的bib标题: Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV
# 相似度: 76.77%
# Citation key: hao2024JointTaskOffloading
# 新文件名: hao2024JointTaskOffloading.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" "markdown/hao2024JointTaskOffloading.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - Joi... -> hao2024JointTaskOffloading.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md"
fi

# 原文件: IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md
# Markdown标题: Service Experience Oriented Cooperative Computing in CacheEnabled UAVs Assisted ...
# 匹配的bib标题: Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs
# 相似度: 86.42%
# Citation key: gao2024ServiceExperienceOriented
# 新文件名: gao2024ServiceExperienceOriented.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" "markdown/gao2024ServiceExperienceOriented.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - Ser... -> gao2024ServiceExperienceOriented.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md"
fi

# 原文件: Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md
# Markdown标题: Improving Data Collection Efficiency of UAVAssisted LoRa Networks via Directivit...
# 匹配的bib标题: Improving Data Collection Efficiency of UAV-assisted LoRa
# 相似度: 73.20%
# Citation key: zhang2025ImprovingDataCollection
# 新文件名: zhang2025ImprovingDataCollection.md
if [ -f "markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md" ]; then
    mv "markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md" "markdown/zhang2025ImprovingDataCollection.md"
    echo "✓ 重命名: Improving_Data_Collection_Efficiency_of_UAV-Assist... -> zhang2025ImprovingDataCollection.md"
else
    echo "⚠ 文件不存在: markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md"
fi

# 原文件: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# Markdown标题: Improving User QoE via Joint Trajectory and Resource Optimization in MultiUAV As...
# 匹配的bib标题: Joint Trajectory Optimization and Resource Allocation in UAV-MEC
# 相似度: 60.13%
# Citation key: chen2025JointTrajectoryOptimization
# 新文件名: chen2025JointTrajectoryOptimization.md
if [ -f "markdown/Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md" ]; then
    mv "markdown/Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md" "markdown/chen2025JointTrajectoryOptimization.md"
    echo "✓ 重命名: Improving_User_QoE_via_Joint_Trajectory_and_Resour... -> chen2025JointTrajectoryOptimization.md"
else
    echo "⚠ 文件不存在: markdown/Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md"
fi

# 无法处理: J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 45.90%)

# 原文件: Jia2024.md
# Markdown标题: Energy and Time TradeOff Optimization for MultiUAV Enabled Data Collection of Io...
# 匹配的bib标题: Energy and Time Trade-off Optimization for Multi-UAV
# 相似度: 71.94%
# Citation key: jia2024EnergyTimeTradeoff
# 新文件名: jia2024EnergyTimeTradeoff.md
if [ -f "markdown/Jia2024.md" ]; then
    mv "markdown/Jia2024.md" "markdown/jia2024EnergyTimeTradeoff.md"
    echo "✓ 重命名: Jia2024.md -> jia2024EnergyTimeTradeoff.md"
else
    echo "⚠ 文件不存在: markdown/Jia2024.md"
fi

# 无法处理: Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md
# 原因: Citation key zhang2023RFSearchSearchingUnconscious 已被使用

# 原文件: Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md
# Markdown标题: Joint Association Deployment and Flight Trajectory Optimization for MultiUAVEnab...
# 匹配的bib标题: Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-e...
# 相似度: 83.42%
# Citation key: han2024JointAssociationDeployment
# 新文件名: han2024JointAssociationDeployment.md
if [ -f "markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md" ]; then
    mv "markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md" "markdown/han2024JointAssociationDeployment.md"
    echo "✓ 重命名: Joint_Association_Deployment_and_Flight_Trajectory... -> han2024JointAssociationDeployment.md"
else
    echo "⚠ 文件不存在: markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md"
fi

# 原文件: Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md
# Markdown标题: Joint Optimization of Beamforming and Trajectory for UAVRISAssisted MUMISO Syste...
# 匹配的bib标题: Joint Optimization of Beamforming and Trajectory for UAV-RIS-assisted MU-MISO
# 相似度: 85.06%
# Citation key: wang2025JointOptimizationBeamforming
# 新文件名: wang2025JointOptimizationBeamforming.md
if [ -f "markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md" ]; then
    mv "markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md" "markdown/wang2025JointOptimizationBeamforming.md"
    echo "✓ 重命名: Joint_Optimization_of_Beamforming_and_Trajectory_f... -> wang2025JointOptimizationBeamforming.md"
else
    echo "⚠ 文件不存在: markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md"
fi

# 原文件: Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md
# Markdown标题: Joint Positioning and Computation Offloading in MultiUAV MEC for Low Latency App...
# 匹配的bib标题: Joint Positioning and Computation Offloading in Multi-UAV MEC
# 相似度: 63.49%
# Citation key: wang2025JointPositioningComputation
# 新文件名: wang2025JointPositioningComputation.md
if [ -f "markdown/Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md" ]; then
    mv "markdown/Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md" "markdown/wang2025JointPositioningComputation.md"
    echo "✓ 重命名: Joint_Positioning_and_Computation_Offloading_in_Mu... -> wang2025JointPositioningComputation.md"
else
    echo "⚠ 文件不存在: markdown/Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md"
fi

# 原文件: Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md
# Markdown标题: Joint Task Offloading and Migration Optimization in UAVEnabled Dynamic MEC Netwo...
# 匹配的bib标题: Joint Task Offloading and Migration Optimization in UAV-enabled
# 相似度: 85.52%
# Citation key: wang2025JointTaskOffloading
# 新文件名: wang2025JointTaskOffloading.md
if [ -f "markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md" ]; then
    mv "markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md" "markdown/wang2025JointTaskOffloading.md"
    echo "✓ 重命名: Joint_Task_Offloading_and_Migration_Optimization_i... -> wang2025JointTaskOffloading.md"
else
    echo "⚠ 文件不存在: markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md"
fi

# 无法处理: Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md
# 原因: Citation key chen2025JointTrajectoryOptimization 已被使用

# 无法处理: Joint_UAV_Deployment_and_Resource_Allocation_in_THz-Assisted_MEC-Enabled_Integrated_Space-Air-Ground_Networks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 52.79%)

# 原文件: Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md
# Markdown标题: Jointly Optimizing the Energy and Time for MultiUAV 3D Coverage of Terrestrial R...
# 匹配的bib标题: Jointly Optimizing the Energy and Time for Multi-UAV
# 相似度: 74.45%
# Citation key: gong2025JointlyOptimizingEnergy
# 新文件名: gong2025JointlyOptimizingEnergy.md
if [ -f "markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md" ]; then
    mv "markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md" "markdown/gong2025JointlyOptimizingEnergy.md"
    echo "✓ 重命名: Jointly_Optimizing_the_Energy_and_Time_for_Multi-U... -> gong2025JointlyOptimizingEnergy.md"
else
    echo "⚠ 文件不存在: markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md"
fi

# 无法处理: Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 59.30%)

# 无法处理: Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 56.68%)

# 无法处理: Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 50.96%)

# 无法处理: Kumar-2025-Drone-Assisted IRS System in 5G and.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 38.82%)

# 无法处理: LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 34.21%)

# 无法处理: LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 40.57%)

# 无法处理: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.70%)

# 原文件: Lee-2025-Adaptive Stabilization Control by Dee.md
# Markdown标题: Adaptive Stabilization Control by Deep Reinforcement Learning for Hovering Drone...
# 匹配的bib标题: Adaptive Stabilization Control by Deep Reinforcement Learning for Hovering Drone...
# 相似度: 100.00%
# Citation key: lee2025AdaptiveStabilizationControl
# 新文件名: lee2025AdaptiveStabilizationControl.md
if [ -f "markdown/Lee-2025-Adaptive Stabilization Control by Dee.md" ]; then
    mv "markdown/Lee-2025-Adaptive Stabilization Control by Dee.md" "markdown/lee2025AdaptiveStabilizationControl.md"
    echo "✓ 重命名: Lee-2025-Adaptive Stabilization Control by Dee.md -> lee2025AdaptiveStabilizationControl.md"
else
    echo "⚠ 文件不存在: markdown/Lee-2025-Adaptive Stabilization Control by Dee.md"
fi

# 原文件: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md
# Markdown标题: MultiObjective Optimization for UAV SwarmAssisted IoT With Virtual Antenna Array...
# 匹配的bib标题: Multi-Objective Optimization for Multi-UAV-assisted
# 相似度: 66.67%
# Citation key: sun2024MultiobjectiveOptimizationMultiUAVassisted
# 新文件名: sun2024MultiobjectiveOptimizationMultiUAVassisted.md
if [ -f "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" ]; then
    mv "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" "markdown/sun2024MultiobjectiveOptimizationMultiUAVassisted.md"
    echo "✓ 重命名: Li 等 - 2024 - Multi-Objective Optimization for UAV... -> sun2024MultiobjectiveOptimizationMultiUAVassisted.md"
else
    echo "⚠ 文件不存在: markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md"
fi

# 无法处理: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 原因: Citation key li2025DynamicRoutingMechanism 已被使用

# 原文件: Li-2025-Taming Event Cameras With Bio-Inspired.md
# Markdown标题: Taming Event Cameras With BioInspired Architecture and Algorithm A Case for Dron...
# 匹配的bib标题: Taming Event Cameras with Bio-Inspired Architecture and Algorithm: A
# 相似度: 79.52%
# Citation key: li2025TamingEventCameras
# 新文件名: li2025TamingEventCameras.md
if [ -f "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" ]; then
    mv "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" "markdown/li2025TamingEventCameras.md"
    echo "✓ 重命名: Li-2025-Taming Event Cameras With Bio-Inspired.md -> li2025TamingEventCameras.md"
else
    echo "⚠ 文件不存在: markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md"
fi

# 原文件: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md
# Markdown标题: UAVenabled Collaborative Beamforming via MultiAgent Deep Reinforcement Learning
# 匹配的bib标题: Multi-Agent Deep Reinforcement Learning
# 相似度: 64.96%
# Citation key: dai2023MultiAgentDeepReinforcement
# 新文件名: dai2023MultiAgentDeepReinforcement.md
if [ -f "markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md" ]; then
    mv "markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md" "markdown/dai2023MultiAgentDeepReinforcement.md"
    echo "✓ 重命名: Liu 等 - 2024 - UAV-enabled Collaborative Beamformi... -> dai2023MultiAgentDeepReinforcement.md"
else
    echo "⚠ 文件不存在: markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md"
fi

# 原文件: Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md
# Markdown标题: Resource Allocation for Adaptive Beam Alignment in UAVAssisted Integrated Sensin...
# 匹配的bib标题: Resource Allocation for Adaptive Beam Alignment in UAV-assisted
# 相似度: 72.94%
# Citation key: liu2025ResourceAllocationAdaptive
# 新文件名: liu2025ResourceAllocationAdaptive.md
if [ -f "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" ]; then
    mv "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" "markdown/liu2025ResourceAllocationAdaptive.md"
    echo "✓ 重命名: Liu 等 - 2025 - Resource Allocation for Adaptive Be... -> liu2025ResourceAllocationAdaptive.md"
else
    echo "⚠ 文件不存在: markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md"
fi

# 原文件: Liu-2025-Delay-Sensitive Goods Delivery and In.md
# Markdown标题: DelaySensitive Goods Delivery and InSitu Sensing Using a MultiTask Drone
# 匹配的bib标题: Delay-Sensitive Goods Delivery and in-Situ Sensing Using a Multi-Task Drone
# 相似度: 100.00%
# Citation key: liu2025DelaysensitiveGoodsDelivery
# 新文件名: liu2025DelaysensitiveGoodsDelivery.md
if [ -f "markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md" ]; then
    mv "markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md" "markdown/liu2025DelaysensitiveGoodsDelivery.md"
    echo "✓ 重命名: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> liu2025DelaysensitiveGoodsDelivery.md"
else
    echo "⚠ 文件不存在: markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md"
fi

# 原文件: Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md
# Markdown标题: Maximizing Service Providers Profit in MultiUAV 5G Network Via Deep Reinforcemen...
# 匹配的bib标题: Maximizing Service Provider's Profit in Multi-UAV 5G
# 相似度: 62.89%
# Citation key: kumari2025MaximizingServiceProviders
# 新文件名: kumari2025MaximizingServiceProviders.md
if [ -f "markdown/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md" ]; then
    mv "markdown/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md" "markdown/kumari2025MaximizingServiceProviders.md"
    echo "✓ 重命名: Maximizing_Service_Providers_Profit_in_Multi-UAV_5... -> kumari2025MaximizingServiceProviders.md"
else
    echo "⚠ 文件不存在: markdown/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md"
fi

# 无法处理: Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 49.77%)

# 原文件: Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md
# Markdown标题: MultiAgent Reinforcement Learning Aided Computation Offloading in Aerial Computi...
# 匹配的bib标题: Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Comput...
# 相似度: 100.00%
# Citation key: qin2022MultiagentReinforcementLearning
# 新文件名: qin2022MultiagentReinforcementLearning.md
if [ -f "markdown/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md" ]; then
    mv "markdown/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md" "markdown/qin2022MultiagentReinforcementLearning.md"
    echo "✓ 重命名: Multi-Agent_Reinforcement_Learning_Aided_Computati... -> qin2022MultiagentReinforcementLearning.md"
else
    echo "⚠ 文件不存在: markdown/Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md"
fi

# 原文件: Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md
# Markdown标题: MultiAgent Reinforcement Learning in Adversarial Game Environments Personalized ...
# 匹配的bib标题: Multi-Agent Reinforcement Learning in Adversarial Game Environments: Personalize...
# 相似度: 71.17%
# Citation key: qin2025MultiagentReinforcementLearning
# 新文件名: qin2025MultiagentReinforcementLearning.md
if [ -f "markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md" ]; then
    mv "markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md" "markdown/qin2025MultiagentReinforcementLearning.md"
    echo "✓ 重命名: Multi-Agent_Reinforcement_Learning_in_Adversarial_... -> qin2025MultiagentReinforcementLearning.md"
else
    echo "⚠ 文件不存在: markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md"
fi

# 无法处理: Multi-UAV-Assisted_MEC_in_Internet_of_Vehicles_With_Combined_Multi-Modal_Semantic_Communication_Under_Jamming_Attacks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.25%)

# 无法处理: Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.15%)

# 无法处理: Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 44.67%)

# 原文件: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md
# Markdown标题: MultiAgent Deep Reinforcement Learning Based UAV Trajectory Optimization for Dif...
# 匹配的bib标题: Multi-Agent Deep Reinforcement Learning Based UAV Trajectory Optimization
# 相似度: 83.72%
# Citation key: ning2024MultiAgentDeepReinforcement
# 新文件名: ning2024MultiAgentDeepReinforcement.md
if [ -f "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" ]; then
    mv "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" "markdown/ning2024MultiAgentDeepReinforcement.md"
    echo "✓ 重命名: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Lea... -> ning2024MultiAgentDeepReinforcement.md"
else
    echo "⚠ 文件不存在: markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md"
fi

# 原文件: Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md
# Markdown标题: Online Energy and Interference Management for Dynamic Target Tracking With Cellu...
# 匹配的bib标题: Online Energy and Interference Management for Dynamic Target Tracking with Cellu...
# 相似度: 100.00%
# Citation key: zhan2025OnlineEnergyInterference
# 新文件名: zhan2025OnlineEnergyInterference.md
if [ -f "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" ]; then
    mv "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" "markdown/zhan2025OnlineEnergyInterference.md"
    echo "✓ 重命名: Online_Energy_and_Interference_Management_for_Dyna... -> zhan2025OnlineEnergyInterference.md"
else
    echo "⚠ 文件不存在: markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md"
fi

# 无法处理: Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 43.06%)

# 原文件: Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md
# Markdown标题: Optimizing Joint Speed and Altitude Schedule for UAV Data Collection in LowAltit...
# 匹配的bib标题: Optimizing Joint Speed and Altitude Schedule for UAV
# 相似度: 72.22%
# Citation key: wang2025OptimizingJointSpeed
# 新文件名: wang2025OptimizingJointSpeed.md
if [ -f "markdown/Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md" ]; then
    mv "markdown/Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md" "markdown/wang2025OptimizingJointSpeed.md"
    echo "✓ 重命名: Optimizing_Joint_Speed_and_Altitude_Schedule_for_U... -> wang2025OptimizingJointSpeed.md"
else
    echo "⚠ 文件不存在: markdown/Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md"
fi

# 原文件: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md
# Markdown标题: Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Ef...
# 匹配的bib标题: Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Ef...
# 相似度: 100.00%
# Citation key: zhang2025OptimizingMonitoringUtility
# 新文件名: zhang2025OptimizingMonitoringUtility.md
if [ -f "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" ]; then
    mv "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" "markdown/zhang2025OptimizingMonitoringUtility.md"
    echo "✓ 重命名: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_V... -> zhang2025OptimizingMonitoringUtility.md"
else
    echo "⚠ 文件不存在: markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md"
fi

# 原文件: Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md
# Markdown标题: Reliable and EnergyEfficient UAV Communications A CostAware Perspective
# 匹配的bib标题: Reliable and Energy-Efficient UAV Communications
# 相似度: 79.66%
# Citation key: panahi2024ReliableEnergyEfficientUAV
# 新文件名: panahi2024ReliableEnergyEfficientUAV.md
if [ -f "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" ]; then
    mv "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" "markdown/panahi2024ReliableEnergyEfficientUAV.md"
    echo "✓ 重命名: Panahi 和 Panahi - 2024 - Reliable and Energy-Effic... -> panahi2024ReliableEnergyEfficientUAV.md"
else
    echo "⚠ 文件不存在: markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md"
fi

# 无法处理: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 53.80%)

# 无法处理: Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 43.87%)

# 原文件: Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md
# Markdown标题: QuantumAssisted Online Task Offloading and Resource Allocation in MECEnabled Sat...
# 匹配的bib标题: Quantum-Assisted Online Task Offloading and Resource Allocation in MEC-enabled
# 相似度: 76.38%
# Citation key: zhang2025QuantumassistedOnlineTask
# 新文件名: zhang2025QuantumassistedOnlineTask.md
if [ -f "markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md" ]; then
    mv "markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md" "markdown/zhang2025QuantumassistedOnlineTask.md"
    echo "✓ 重命名: Quantum-Assisted_Online_Task_Offloading_and_Resour... -> zhang2025QuantumassistedOnlineTask.md"
else
    echo "⚠ 文件不存在: markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md"
fi

# 原文件: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md
# Markdown标题: Reconfigurable Intelligent Surface Assisted UAVMCS Based on Transformer Enhanced...
# 匹配的bib标题: Reconfigurable Intelligent Surface Assisted UAV-MCS
# 相似度: 63.29%
# Citation key: wu2025ReconfigurableIntelligentSurface
# 新文件名: wu2025ReconfigurableIntelligentSurface.md
if [ -f "markdown/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md" ]; then
    mv "markdown/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md" "markdown/wu2025ReconfigurableIntelligentSurface.md"
    echo "✓ 重命名: Reconfigurable_Intelligent_Surface_Assisted_UAV-MC... -> wu2025ReconfigurableIntelligentSurface.md"
else
    echo "⚠ 文件不存在: markdown/Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md"
fi

# 无法处理: Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 48.13%)

# 原文件: Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md
# Markdown标题: Resource Allocation in Blockchain Integration of UAVEnabled MEC Networks A Stack...
# 匹配的bib标题: Resource Allocation in Blockchain Integration of UAV-enabled MEC
# 相似度: 71.59%
# Citation key: wang2024ResourceAllocationBlockchain
# 新文件名: wang2024ResourceAllocationBlockchain.md
if [ -f "markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md" ]; then
    mv "markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md" "markdown/wang2024ResourceAllocationBlockchain.md"
    echo "✓ 重命名: Resource Allocation in Blockchain Integration of U... -> wang2024ResourceAllocationBlockchain.md"
else
    echo "⚠ 文件不存在: markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md"
fi

# 无法处理: Resource_Allocation_in_Blockchain_Integration_of_UAV-Enabled_MEC_Networks_A_Stackelberg_Differential_Game_Approach.md
# 原因: Citation key wang2024ResourceAllocationBlockchain 已被使用

# 无法处理: Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md
# 原因: Citation key liwang2021LetsTradeFuture 已被使用

# 无法处理: Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md
# 原因: Citation key zhang2023RFSearchSearchingUnconscious 已被使用

# 无法处理: Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 38.91%)

# 无法处理: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.57%)

# 无法处理: Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 53.33%)

# 无法处理: Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 52.63%)

# 无法处理: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 44.25%)

# 无法处理: Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 49.44%)

# 无法处理: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 48.48%)

# 无法处理: Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md
# 原因: Citation key sun2024MultiobjectiveOptimizationMultiUAVassisted 已被使用

# 原文件: Sun-2025-Aerial Reliable Collaborative Communi.md
# Markdown标题: Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Ev...
# 匹配的bib标题: Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Ev...
# 相似度: 100.00%
# Citation key: sun2025AerialReliableCollaborative
# 新文件名: sun2025AerialReliableCollaborative.md
if [ -f "markdown/Sun-2025-Aerial Reliable Collaborative Communi.md" ]; then
    mv "markdown/Sun-2025-Aerial Reliable Collaborative Communi.md" "markdown/sun2025AerialReliableCollaborative.md"
    echo "✓ 重命名: Sun-2025-Aerial Reliable Collaborative Communi.md -> sun2025AerialReliableCollaborative.md"
else
    echo "⚠ 文件不存在: markdown/Sun-2025-Aerial Reliable Collaborative Communi.md"
fi

# 无法处理: Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.58%)

# 原文件: TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md
# Markdown标题: TJCCT A TwoTimescale Approach for UAVAssisted Mobile Edge Computing
# 匹配的bib标题: A Two Time-Scale Joint Optimization Approach for UAV-assisted MEC
# 相似度: 66.15%
# Citation key: sun2024TwoTimescaleJoint
# 新文件名: sun2024TwoTimescaleJoint.md
if [ -f "markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md" ]; then
    mv "markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md" "markdown/sun2024TwoTimescaleJoint.md"
    echo "✓ 重命名: TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mo... -> sun2024TwoTimescaleJoint.md"
else
    echo "⚠ 文件不存在: markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md"
fi

# 原文件: Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md
# Markdown标题: MultiAgent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial C...
# 匹配的bib标题: Multi-Agent Cooperation for Computing Power Scheduling in UAVs
# 相似度: 77.71%
# Citation key: tao2024MultiagentCooperationComputing
# 新文件名: tao2024MultiagentCooperationComputing.md
if [ -f "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" ]; then
    mv "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" "markdown/tao2024MultiagentCooperationComputing.md"
    echo "✓ 重命名: Tao 等 - 2024 - Multi-Agent Cooperation for Computi... -> tao2024MultiagentCooperationComputing.md"
else
    echo "⚠ 文件不存在: markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md"
fi

# 原文件: Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md
# Markdown标题: Task Offloading and Resource Pricing Based on Game Theory in UAVAssisted Edge Co...
# 匹配的bib标题: Task Offloading and Resource Pricing Based on Game Theory in UAV-assisted
# 相似度: 90.57%
# Citation key: chen2025TaskOffloadingResource
# 新文件名: chen2025TaskOffloadingResource.md
if [ -f "markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md" ]; then
    mv "markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md" "markdown/chen2025TaskOffloadingResource.md"
    echo "✓ 重命名: Task_Offloading_and_Resource_Pricing_Based_on_Game... -> chen2025TaskOffloadingResource.md"
else
    echo "⚠ 文件不存在: markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md"
fi

# 原文件: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md
# Markdown标题: UAVAssisted Wireless Cooperative Communication and Coded Caching A Multiagent Tw...
# 匹配的bib标题: UAV-Assisted Wireless Cooperative Communication
# 相似度: 61.74%
# Citation key: tian2024UAVAssistedWirelessCooperative
# 新文件名: tian2024UAVAssistedWirelessCooperative.md
if [ -f "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" ]; then
    mv "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" "markdown/tian2024UAVAssistedWirelessCooperative.md"
    echo "✓ 重命名: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative ... -> tian2024UAVAssistedWirelessCooperative.md"
else
    echo "⚠ 文件不存在: markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md"
fi

# 无法处理: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 56.72%)

# 原文件: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md
# Markdown标题: TrustEnhanced Game Incentive for Secure Quantum Federated Learning in UAVAssiste...
# 匹配的bib标题: Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-assis...
# 相似度: 90.00%
# Citation key: xu2025TrustenhancedGameIncentive
# 新文件名: xu2025TrustenhancedGameIncentive.md
if [ -f "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025TrustenhancedGameIncentive.md"
    echo "✓ 重命名: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_F... -> xu2025TrustenhancedGameIncentive.md"
else
    echo "⚠ 文件不存在: markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md"
fi

# 无法处理: UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 41.03%)

# 无法处理: UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.27%)

# 无法处理: UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 43.93%)

# 无法处理: UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.03%)

# 原文件: User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md
# Markdown标题: User Preference Oriented Service Caching and Task Offloading for UAVAssisted MEC...
# 匹配的bib标题: User Preference Oriented Service Caching and Task Offloading for UAV-assisted ME...
# 相似度: 94.67%
# Citation key: zhou2025UserPreferenceOriented
# 新文件名: zhou2025UserPreferenceOriented.md
if [ -f "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" ]; then
    mv "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" "markdown/zhou2025UserPreferenceOriented.md"
    echo "✓ 重命名: User_Preference_Oriented_Service_Caching_and_Task_... -> zhou2025UserPreferenceOriented.md"
else
    echo "⚠ 文件不存在: markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md"
fi

# 无法处理: VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.26%)

# 原文件: Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md
# Markdown标题: BiObjective Ant Colony Optimization for Trajectory Planning and Task Offloading ...
# 匹配的bib标题: Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading...
# 相似度: 96.08%
# Citation key: wang2024BiobjectiveAntColony
# 新文件名: wang2024BiobjectiveAntColony.md
if [ -f "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" ]; then
    mv "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" "markdown/wang2024BiobjectiveAntColony.md"
    echo "✓ 重命名: Wang 等 - 2024 - Bi-Objective Ant Colony Optimizati... -> wang2024BiobjectiveAntColony.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md"
fi

# 原文件: Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md
# Markdown标题: Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for...
# 匹配的bib标题: Decentralized Navigation with Heterogeneous Federated Reinforcement Learning for...
# 相似度: 89.22%
# Citation key: wang2024DecentralizedNavigationHeterogeneous
# 新文件名: wang2024DecentralizedNavigationHeterogeneous.md
if [ -f "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" ]; then
    mv "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" "markdown/wang2024DecentralizedNavigationHeterogeneous.md"
    echo "✓ 重命名: Wang 等 - 2024 - Decentralized Navigation With Hete... -> wang2024DecentralizedNavigationHeterogeneous.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md"
fi

# 无法处理: Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.90%)

# 无法处理: Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md
# 原因: Citation key wang2025JointPositioningComputation 已被使用

# 无法处理: Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 56.50%)

# 无法处理: Wang-2025-Optimizing Joint Speed and Altitude.md
# 原因: Citation key wang2025OptimizingJointSpeed 已被使用

# 无法处理: Wang-2025-Practical Optimizing UAV Trajectory.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 53.80%)

# 无法处理: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 53.33%)

# 原文件: Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md
# Markdown标题: Hierarchical Network Slicing for UAVAssisted Wireless Networks With Deployment O...
# 匹配的bib标题: Hierarchical Network Slicing for UAV-assisted
# 相似度: 65.19%
# Citation key: wei2024HierarchicalNetworkSlicing
# 新文件名: wei2024HierarchicalNetworkSlicing.md
if [ -f "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" ]; then
    mv "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" "markdown/wei2024HierarchicalNetworkSlicing.md"
    echo "✓ 重命名: Wei 等 - 2024 - Hierarchical Network Slicing for UA... -> wei2024HierarchicalNetworkSlicing.md"
else
    echo "⚠ 文件不存在: markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md"
fi

# 原文件: Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md
# Markdown标题: WindAware Service Provisioning Strategy for MultiPackage Drone Delivery
# 匹配的bib标题: Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery
# 相似度: 100.00%
# Citation key: xu2025WindawareServiceProvisioning
# 新文件名: xu2025WindawareServiceProvisioning.md
if [ -f "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" ]; then
    mv "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" "markdown/xu2025WindawareServiceProvisioning.md"
    echo "✓ 重命名: Wind-Aware Service Provisioning Strategy for Multi... -> xu2025WindawareServiceProvisioning.md"
else
    echo "⚠ 文件不存在: markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md"
fi

# 无法处理: Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 43.68%)

# 无法处理: Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 50.33%)

# 原文件: Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md
# Markdown标题: TwoStage Deep Energy Optimization in IRSAssisted UAVBased Edge Computing Systems
# 匹配的bib标题: Two-Stage Deep Energy Optimization in IRS-assisted UAV-based
# 相似度: 83.21%
# Citation key: wu2025TwostageDeepEnergy
# 新文件名: wu2025TwostageDeepEnergy.md
if [ -f "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" ]; then
    mv "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" "markdown/wu2025TwostageDeepEnergy.md"
    echo "✓ 重命名: Wu 等 - 2025 - Two-Stage Deep Energy Optimization i... -> wu2025TwostageDeepEnergy.md"
else
    echo "⚠ 文件不存在: markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md"
fi

# 无法处理: Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 52.17%)

# 无法处理: Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 44.72%)

# 原文件: Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md
# Markdown标题: Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling
# 匹配的bib标题: Towards Maximizing Coverage of Targets for WRSNs
# 相似度: 75.00%
# Citation key: xue2024MaximizingCoverageTargets
# 新文件名: xue2024MaximizingCoverageTargets.md
if [ -f "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" ]; then
    mv "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" "markdown/xue2024MaximizingCoverageTargets.md"
    echo "✓ 重命名: Xue 等 - 2024 - Towards Maximizing Coverage of Targ... -> xue2024MaximizingCoverageTargets.md"
else
    echo "⚠ 文件不存在: markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md"
fi

# 无法处理: Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 51.70%)

# 原文件: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# Markdown标题: Hybrid Transformer Based MultiAgent Reinforcement Learning for Multiple Unpilote...
# 匹配的bib标题: Hybrid Transformer Based Multi-Agent Reinforcement Learning for Multiple Unpilot...
# 相似度: 100.00%
# Citation key: yu2025HybridTransformerBased
# 新文件名: yu2025HybridTransformerBased.md
if [ -f "markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md" ]; then
    mv "markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md" "markdown/yu2025HybridTransformerBased.md"
    echo "✓ 重命名: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> yu2025HybridTransformerBased.md"
else
    echo "⚠ 文件不存在: markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md"
fi

# 无法处理: Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 57.78%)

# 无法处理: Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.89%)

# 原文件: Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md
# Markdown标题: InterferenceAware Online Optimization for CellularConnected Multiple UAV Network...
# 匹配的bib标题: Interference-Aware Online Optimization for Cellular-Connected Multiple UAV
# 相似度: 81.36%
# Citation key: zhan2024InterferenceawareOnlineOptimization
# 新文件名: zhan2024InterferenceawareOnlineOptimization.md
if [ -f "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" ]; then
    mv "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" "markdown/zhan2024InterferenceawareOnlineOptimization.md"
    echo "✓ 重命名: Zhan 等 - 2024 - Interference-Aware Online Optimiza... -> zhan2024InterferenceawareOnlineOptimization.md"
else
    echo "⚠ 文件不存在: markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md"
fi

# 无法处理: Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 48.75%)

# 原文件: Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md
# Markdown标题: Task Offloading and Trajectory Optimization for Secure Communications in Dynamic...
# 匹配的bib标题: Task Offloading and Trajectory Optimization for Secure Communications in Dynamic...
# 相似度: 96.08%
# Citation key: zhang2024TaskOffloadingTrajectory
# 新文件名: zhang2024TaskOffloadingTrajectory.md
if [ -f "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" ]; then
    mv "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" "markdown/zhang2024TaskOffloadingTrajectory.md"
    echo "✓ 重命名: Zhang 等 - 2024 - Task Offloading and Trajectory Op... -> zhang2024TaskOffloadingTrajectory.md"
else
    echo "⚠ 文件不存在: markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md"
fi

# 无法处理: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 50.31%)

# 无法处理: Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 54.70%)

# 原文件: Zhang-2025-Multi-Objective Aerial Collaborativ.md
# Markdown标题: MultiObjective Aerial Collaborative Secure Communication Optimization via Genera...
# 匹配的bib标题: Multi-Objective Aerial Collaborative Secure Communication Optimization via Gener...
# 相似度: 100.00%
# Citation key: zhang2025MultiobjectiveAerialCollaborative
# 新文件名: zhang2025MultiobjectiveAerialCollaborative.md
if [ -f "markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md" ]; then
    mv "markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md" "markdown/zhang2025MultiobjectiveAerialCollaborative.md"
    echo "✓ 重命名: Zhang-2025-Multi-Objective Aerial Collaborativ.md -> zhang2025MultiobjectiveAerialCollaborative.md"
else
    echo "⚠ 文件不存在: markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md"
fi

# 无法处理: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 原因: Citation key zhang2025OptimizingMonitoringUtility 已被使用

# 无法处理: Zhang-2025-Quantum-Assisted Online Task Offloa.md
# 原因: Citation key zhang2025QuantumassistedOnlineTask 已被使用

# 无法处理: Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 55.50%)

# 原文件: Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md
# Markdown标题: Joint Content Caching Service Placement and Task Offloading in UAVEnabled Mobile...
# 匹配的bib标题: Joint Content Caching, Service Placement, and Task Offloading in UAV-enabled
# 相似度: 82.49%
# Citation key: zhao2025JointContentCaching
# 新文件名: zhao2025JointContentCaching.md
if [ -f "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" "markdown/zhao2025JointContentCaching.md"
    echo "✓ 重命名: Zhao 等 - 2025 - Joint Content Caching, Service Pla... -> zhao2025JointContentCaching.md"
else
    echo "⚠ 文件不存在: markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md"
fi

# 原文件: Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md
# Markdown标题: Joint Optimization of Trajectory Offloading Caching and Migration for UAVAssiste...
# 匹配的bib标题: Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-ass...
# 相似度: 100.00%
# Citation key: zhao2025JointOptimizationTrajectory
# 新文件名: zhao2025JointOptimizationTrajectory.md
if [ -f "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" "markdown/zhao2025JointOptimizationTrajectory.md"
    echo "✓ 重命名: Zhao 等 - 2025 - Joint Optimization of Trajectory, ... -> zhao2025JointOptimizationTrajectory.md"
else
    echo "⚠ 文件不存在: markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md"
fi

# 无法处理: Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 47.74%)

# 无法处理: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 46.03%)

# 原文件: Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md
# Markdown标题: A Federated Digital Twin Framework for UAVsBased Mobile Scenarios
# 匹配的bib标题: A Federated Digital Twin Framework
# 相似度: 68.69%
# Citation key: zhou2024FederatedDigitalTwin
# 新文件名: zhou2024FederatedDigitalTwin.md
if [ -f "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" ]; then
    mv "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" "markdown/zhou2024FederatedDigitalTwin.md"
    echo "✓ 重命名: Zhou 等 - 2024 - A Federated Digital Twin Framework... -> zhou2024FederatedDigitalTwin.md"
else
    echo "⚠ 文件不存在: markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md"
fi

# 无法处理: Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua.md
# 原因: 在bib文件中未找到匹配的标题 (最高相似度: 59.17%)

# 原文件: Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md
# Markdown标题: SymmetryAugmented MultiAgent Reinforcement Learning for Scalable UAV Trajectory ...
# 匹配的bib标题: Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV
# 相似度: 78.16%
# Citation key: zhou2024SymmetryaugmentedMultiagentReinforcement
# 新文件名: zhou2024SymmetryaugmentedMultiagentReinforcement.md
if [ -f "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" ]; then
    mv "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" "markdown/zhou2024SymmetryaugmentedMultiagentReinforcement.md"
    echo "✓ 重命名: Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Rei... -> zhou2024SymmetryaugmentedMultiagentReinforcement.md"
else
    echo "⚠ 文件不存在: markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md"
fi

# 原文件: Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md
# Markdown标题: Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle UAV Trajector...
# 匹配的bib标题: Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV
# 相似度: 78.65%
# Citation key: zhu2024CollaborativeReinforcementLearning
# 新文件名: zhu2024CollaborativeReinforcementLearning.md
if [ -f "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" ]; then
    mv "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" "markdown/zhu2024CollaborativeReinforcementLearning.md"
    echo "✓ 重命名: Zhu 等 - 2024 - Collaborative Reinforcement Learnin... -> zhu2024CollaborativeReinforcementLearning.md"
else
    echo "⚠ 文件不存在: markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md"
fi

# 已符合格式，跳过: alkouz2022InfEneCom.md

# 已符合格式，跳过: chen2025EneOveCom.md

# 已符合格式，跳过: cui2024TheDatVal.md

# 已符合格式，跳过: gao2025TraLeaFor.md

# 已符合格式，跳过: hao2025RelOptOf.md

# 已符合格式，跳过: ji2024DecAssWit.md

# 已符合格式，跳过: jia2025DistributionallyRobustOptimization.md

# 已符合格式，跳过: kang2024AutMulRac.md

# 已符合格式，跳过: li2024SecOffWit.md

# 已符合格式，跳过: li2025CooNonMul.md

# 已符合格式，跳过: li2025FedMetBas.md

# 已符合格式，跳过: lin2024LyapunovbasedApproachJoint.md

# 已符合格式，跳过: liu2025AHybOpt.md

# 已符合格式，跳过: liu2025OnTheRob.md

# 已符合格式，跳过: nabi2025JoiOffDec.md

# 已符合格式，跳过: ning2025JoiOptOf.md

# 已符合格式，跳过: qian2024APatPla.md

# 已符合格式，跳过: qin2022MulReiLea.md

# 已符合格式，跳过: ren2024IntAdaGos.md

# 已符合格式，跳过: rizvi2025MonIntSer.md

# 已符合格式，跳过: shao2024DeepReinforcementLearningbased.md

# 已符合格式，跳过: shen2024SlicingBasedTaskOffloading.md

# 已符合格式，跳过: singh2024StaMatBas.md

# 已符合格式，跳过: song2024EneTraOpt.md

# 已符合格式，跳过: zhou2024SymmetryaugmentedMultiagentReinforcement.md


# 低相似度匹配（可能需要手动确认）：

# 文件: ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md
# Markdown标题: ASSUME An Optimal Algorithm to Minimize UAV Energy by Altitu...
# 最佳匹配: 无...
# 相似度: 41.79%

# 文件: A_Fast_UAV_Trajectory_Planning_Framework_in_RIS-Assisted_Communication_Systems_With_Accelerated_Learning_via_Multithreading_and_Federating.md
# Markdown标题: A Fast UAV Trajectory Planning Framework in RISAssisted Comm...
# 最佳匹配: 无...
# 相似度: 46.81%

# 文件: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# Markdown标题: A MultiUAV Cooperative Task Scheduling in Dynamic Environmen...
# 最佳匹配: 无...
# 相似度: 47.62%

# 文件: A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying.md
# Markdown标题: A Novel MRRUAVBased Relay With Optical Network Coding A Comp...
# 最佳匹配: 无...
# 相似度: 39.53%

# 文件: Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning.md
# Markdown标题: Adaptive 3D Placement of Multiple UAVMounted Base Stations i...
# 最佳匹配: 无...
# 相似度: 54.74%

# 文件: AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md
# Markdown标题: AeroEcho Towards Agricultural Lowpower Widearea Backscatter ...
# 最佳匹配: 无...
# 相似度: 41.94%

# 文件: Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry.md
# Markdown标题: Anchor A Novel Modeling Methodology forS 04XHXHHOHQJWK Coope...
# 最佳匹配: 无...
# 相似度: 34.15%

# 文件: Attitude control of a novel tilt-wing UAV in hovering flight..md
# Markdown标题: MOOP
# 最佳匹配: 无...
# 相似度: 50.00%

# 文件: Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md
# Markdown标题: Supplementary File
# 最佳匹配: 无...
# 相似度: 47.27%

# 文件: Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md
# Markdown标题: Adaptive Bitrate Video Caching in UAVAssisted MEC Networks B...
# 最佳匹配: 无...
# 相似度: 45.30%

# 文件: Chen-2025-TypeFly_ Low-Latency Drone Planning.md
# Markdown标题: TypeFly LowLatency Drone Planning With Large Language Models
# 最佳匹配: 无...
# 相似度: 47.92%

# 文件: Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md
# Markdown标题: ParallEdge Exploiting ComputingMobility Parallelism for Effi...
# 最佳匹配: 无...
# 相似度: 44.44%

# 文件: Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md
# Markdown标题: UAVAssisted Task Offloading in Vehicular Edge Computing Netw...
# 最佳匹配: 无...
# 相似度: 59.34%

# 文件: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md
# Markdown标题: Digital Twin Empowered mmWave MultiHop V2X Routing Scheme Wi...
# 最佳匹配: 无...
# 相似度: 54.72%

# 文件: Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span.md
# Markdown标题: DroneAssisted IRS System in 5G and Beyond Improving Reliabil...
# 最佳匹配: 无...
# 相似度: 38.82%

# 文件: DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md
# Markdown标题: DroneMA Drone Mobility Alignment Countering AIbased Spoofing...
# 最佳匹配: 无...
# 相似度: 47.37%

# 文件: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# Markdown标题: EnergyEfficient 3D Data Collection for MultiUAV Assisted Mob...
# 最佳匹配: 无...
# 相似度: 59.26%

# 文件: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md
# Markdown标题: Exploring the Robustness Hierarchical Federated Learning Fra...
# 最佳匹配: 无...
# 相似度: 53.24%

# 文件: Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md
# Markdown标题: CSMAAC MultiAgent Reinforcement Learning Based Flight Contro...
# 最佳匹配: 无...
# 相似度: 54.35%

# 文件: Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md
# Markdown标题: Dynamic Topology Organization and Maintenance Algorithms for...
# 最佳匹配: 无...
# 相似度: 52.25%

# 文件: Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md
# Markdown标题: EnergyEfficient 3D UAV Ground Node Accessing Using the Minim...
# 最佳匹配: 无...
# 相似度: 49.54%

# 文件: Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md
# Markdown标题: Joint Optimization of Trajectory and Jamming Power for Multi...
# 最佳匹配: 无...
# 相似度: 59.67%

# 文件: Guo-2025-Mighty_ Towards Long-Range and High-T.md
# Markdown标题: Mighty Towards LongRange and HighThroughput Backscatter for ...
# 最佳匹配: 无...
# 相似度: 47.37%

# 文件: HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md
# Markdown标题: HaDT Hardening Digital Twins for UAVsBased Industrial Logist...
# 最佳匹配: 无...
# 相似度: 42.96%

# 文件: Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md
# Markdown标题: Collaborative Route Planning of UAVs Workers and Cars for Cr...
# 最佳匹配: 无...
# 相似度: 56.69%

# 文件: He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md
# Markdown标题: Balancing Total Energy Consumption and Mean Makespan in Data...
# 最佳匹配: 无...
# 相似度: 47.22%

# 文件: Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md
# Markdown标题: Finite Block Length NOMA MU Pairing UAVEnable System Perform...
# 最佳匹配: 无...
# 相似度: 47.24%

# 文件: Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md
# Markdown标题: Dynamic Task Offloading for MultiUAVs in Vehicular Edge Comp...
# 最佳匹配: 无...
# 相似度: 46.54%

# 文件: J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems.md
# Markdown标题: mathrm J C 5 A Service Delay Minimization for Aerial MECAssi...
# 最佳匹配: 无...
# 相似度: 45.90%

# 文件: Joint_UAV_Deployment_and_Resource_Allocation_in_THz-Assisted_MEC-Enabled_Integrated_Space-Air-Ground_Networks.md
# Markdown标题: Joint UAV Deployment and Resource Allocation in THzAssisted ...
# 最佳匹配: 无...
# 相似度: 52.79%

# 文件: Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md
# Markdown标题: A BlockchainBased Distributed and Intelligent ClusteringEnab...
# 最佳匹配: 无...
# 相似度: 59.30%

# 文件: Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md
# Markdown标题: A Novel Federated LearningBased Smart Power and 3D Trajector...
# 最佳匹配: 无...
# 相似度: 56.68%

# 文件: Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md
# Markdown标题: Improved Algorithms for CoScheduling of Edge Analytics and R...
# 最佳匹配: 无...
# 相似度: 50.96%

# 文件: Kumar-2025-Drone-Assisted IRS System in 5G and.md
# Markdown标题: DroneAssisted IRS System in 5G and Beyond Improving Reliabil...
# 最佳匹配: 无...
# 相似度: 38.82%

# 文件: LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md
# Markdown标题: Digital Object Identifier 101109TKDE20253579386
# 最佳匹配: 无...
# 相似度: 34.21%

# 文件: LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md
# Markdown标题: LSPSS Constructing Lightweight and Secure Scheme for Private...
# 最佳匹配: 无...
# 相似度: 40.57%

# 文件: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md
# Markdown标题: Large Models for Aerial Edges An EdgeCloud Model Evolution a...
# 最佳匹配: 无...
# 相似度: 54.70%

# 文件: Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md
# Markdown标题: Deployment CostAware UAV and BS Collaboration in CellFree In...
# 最佳匹配: 无...
# 相似度: 49.77%

# 文件: Multi-UAV-Assisted_MEC_in_Internet_of_Vehicles_With_Combined_Multi-Modal_Semantic_Communication_Under_Jamming_Attacks.md
# Markdown标题: MultiUAVAssisted MEC in Internet of Vehicles With Combined M...
# 最佳匹配: 无...
# 相似度: 46.25%

# 文件: Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md
# Markdown标题: NearOptimal UAV Deployment for DelayBounded Data Collection ...
# 最佳匹配: 无...
# 相似度: 46.15%

# 文件: Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md
# Markdown标题: On the Dilemma of Reliability or Security in Unmanned Aerial...
# 最佳匹配: 无...
# 相似度: 44.67%

# 文件: Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios.md
# Markdown标题: Optical RISs Improve the Secret Key Rate of FreeSpace QKD in...
# 最佳匹配: 无...
# 相似度: 43.06%

# 文件: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md
# Markdown标题: Practical Optimizing UAV Trajectory in Wireless Charging Net...
# 最佳匹配: 无...
# 相似度: 53.80%

# 文件: Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md
# Markdown标题: Integrated Host and ContentCentric Routing for Efficient and...
# 最佳匹配: 无...
# 相似度: 43.87%

# 文件: Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control.md
# Markdown标题: ReliabilityOptimal UAVAssisted Mobile Edge Computing Joint R...
# 最佳匹配: 无...
# 相似度: 48.13%

# 文件: Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature.md
# Markdown标题: Securing Autonomous UAV Cluster With BlockchainBased Thresho...
# 最佳匹配: 无...
# 相似度: 38.91%

# 文件: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md
# Markdown标题: SecurityAware Designs of MultiUAV Deployment Task Offloading...
# 最佳匹配: 无...
# 相似度: 47.57%

# 文件: Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md
# Markdown标题: ServHU Service Handoff for UAVasaService
# 最佳匹配: 无...
# 相似度: 53.33%

# 文件: Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md
# Markdown标题: A TwoStage Strategy for UAVEnabled Wireless Power Transfer i...
# 最佳匹配: 无...
# 相似度: 52.63%

# 文件: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md
# Markdown标题: AoI and Energy Tradeoff for AerialGround Collaborative MEC A...
# 最佳匹配: 无...
# 相似度: 44.25%

# 文件: Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md
# Markdown标题: Methods to Assign UAVs for KCoverage and Recharging in IoT N...
# 最佳匹配: 无...
# 相似度: 49.44%

# 文件: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md
# Markdown标题: Catch Me If You Can Deep MetaRL for SearchandRescue Using Lo...
# 最佳匹配: 无...
# 相似度: 48.48%

# 文件: Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage.md
# Markdown标题: SymmetryInformed MARL A Decentralized and Cooperative UAV Sw...
# 最佳匹配: 无...
# 相似度: 46.58%

# 文件: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md
# Markdown标题: Trajectory Optimization and Power Allocation for MultiUAV Wi...
# 最佳匹配: 无...
# 相似度: 56.72%

# 文件: UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring.md
# Markdown标题: RESEARCH PAPER Special Topic UAV Swarm Autonomous Control
# 最佳匹配: 无...
# 相似度: 41.03%

# 文件: UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming.md
# Markdown标题: UAVAssisted Communications in SAGINISAC Mobile User Tracking...
# 最佳匹配: 无...
# 相似度: 46.27%

# 文件: UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md
# Markdown标题: UAVAssisted Microservice Mobile Edge Computing Architecture ...
# 最佳匹配: 无...
# 相似度: 43.93%

# 文件: UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach.md
# Markdown标题: UAV SwarmEnabled Collaborative PostDisaster Communications i...
# 最佳匹配: 无...
# 相似度: 46.03%

# 文件: VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md
# Markdown标题: VerDT A Versatile Digital Twins Framework for UAVsBased Indu...
# 最佳匹配: 无...
# 相似度: 46.26%

# 文件: Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md
# Markdown标题: Ensuring Threshold AoI for UAVAssisted Mobile Crowdsensing b...
# 最佳匹配: 无...
# 相似度: 54.90%

# 文件: Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md
# Markdown标题: Wireless Powered Metaverse Joint Task Scheduling and Traject...
# 最佳匹配: 无...
# 相似度: 56.50%

# 文件: Wang-2025-Practical Optimizing UAV Trajectory.md
# Markdown标题: Practical Optimizing UAV Trajectory in Wireless Charging Net...
# 最佳匹配: 无...
# 相似度: 53.80%

# 文件: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md
# Markdown标题: Smart Shield Prevent Aerial Eavesdropping via Cooperative In...
# 最佳匹配: 无...
# 相似度: 53.33%

# 文件: Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md
# Markdown标题: MAC Optimization Protocol for Cooperative UAV Based on Dual ...
# 最佳匹配: 无...
# 相似度: 43.68%

# 文件: Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md
# Markdown标题: MultiUAVs Network Design Algorithms for Computed Rate Maximi...
# 最佳匹配: 无...
# 相似度: 50.33%

# 文件: Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md
# Markdown标题: Reward Maximization for Disaster Zone Monitoring With Hetero...
# 最佳匹配: 无...
# 相似度: 52.17%

# 文件: Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md
# Markdown标题: SemanticAware UAV Swarm Coordination in the Metaverse A Repu...
# 最佳匹配: 无...
# 相似度: 44.72%

# 文件: Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md
# Markdown标题: Energy Efficient Transmission Strategy for Mobile Edge Compu...
# 最佳匹配: 无...
# 相似度: 51.70%

# 文件: Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md
# Markdown标题: 3D Trajectory Optimization for Multimission UAVs in Smart Ci...
# 最佳匹配: 无...
# 相似度: 57.78%

# 文件: Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md
# Markdown标题: A3D Adaptive Accurate and Autonomous Navigation for EdgeAssi...
# 最佳匹配: 无...
# 相似度: 47.89%

# 文件: Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md
# Markdown标题: Tradeoff Between Age of Information and Operation Time for U...
# 最佳匹配: 无...
# 相似度: 48.75%

# 文件: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md
# Markdown标题: UAV SwarmEnabled Collaborative Secure Relay Communications W...
# 最佳匹配: 无...
# 相似度: 50.31%

# 文件: Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md
# Markdown标题: Large Models for Aerial Edges An EdgeCloud Model Evolution a...
# 最佳匹配: 无...
# 相似度: 54.70%

# 文件: Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md
# Markdown标题: On Designing MultiUAV Aided Wireless Powered Dynamic Communi...
# 最佳匹配: 无...
# 相似度: 55.50%

# 文件: Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md
# Markdown标题: Content Delivery Performance Analysis of a CacheEnabled UAV ...
# 最佳匹配: 无...
# 相似度: 47.74%

# 文件: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md
# Markdown标题: UAV SwarmEnabled Collaborative PostDisaster Communications i...
# 最佳匹配: 无...
# 相似度: 46.03%

# 文件: Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua.md
# Markdown标题: Joint Optimization of Mobility and ReliabilityGuaranteed Air...
# 最佳匹配: 无...
# 相似度: 59.17%


echo "=================================================="
echo "Markdown文件重命名完成！共处理 71 个文件"
echo "无法自动处理: 91 个文件"
echo "低相似度匹配: 77 个"
echo "=================================================="
echo "Markdown文件在: markdown/"
echo "请检查无法处理的文件，手动重命名。"