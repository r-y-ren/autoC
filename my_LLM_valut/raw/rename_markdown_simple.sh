#!/bin/bash
# 直接按照 auth.lower + year + shorttitle(3,3) 规则重命名Markdown文件
# 完全不依赖bib文件
#
# 共处理 187 个Markdown文件
#
set -e  # 遇到错误立即退出

cd /Users/wupengfei/Downloads/my_LLM_valut/raw

echo "开始Markdown文件重命名..."

# 无法处理: 1570937393.md
# 原因: 缺少年份信息

# 无法处理: 1570937499.md
# 原因: 缺少作者信息

# 无法处理: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md
# 原因: 缺少年份信息

# 无法处理: ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md
# 原因: 缺少年份信息

# 无法处理: A_Fast_UAV_Trajectory_Planning_Framework_in_RIS-Assisted_Communication_Systems_With_Accelerated_Learning_via_Multithreading_and_Federating.md
# 原因: 缺少年份信息

# 无法处理: A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md
# 原因: 缺少年份信息

# 无法处理: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md
# 原因: 缺少年份信息

# 无法处理: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# 原因: 缺少年份信息

# 无法处理: A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md
# 原因: 缺少年份信息

# 无法处理: A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying.md
# 原因: 缺少年份信息

# 无法处理: A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md
# 原因: 缺少年份信息

# 无法处理: Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning.md
# 原因: 缺少年份信息

# 无法处理: AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md
# 原因: 缺少年份信息

# 无法处理: Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md
# 原因: 缺少年份信息

# 无法处理: Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md
# 原因: 缺少年份信息

# 原文件: Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md
# 作者: Joint Trajectory
# 年份: 2024
# 标题: Alam和Moh 2024 Joint Trajectory Control, Frequency Allocation, and Routing for UA...
# 新文件名: trajectory2024Ala202Joi.md
if [ -f "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" ]; then
    mv "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" "markdown/trajectory2024Ala202Joi.md"
    echo "✓ 重命名: Alam和Moh - 2024 - Joint Trajectory Control, Freque... -> trajectory2024Ala202Joi.md"
else
    echo "⚠ 文件不存在: markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md"
fi

# 无法处理: An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md
# 原因: 缺少作者信息

# 无法处理: Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry.md
# 原因: 缺少年份信息

# 无法处理: Attitude control of a novel tilt-wing UAV in hovering flight..md
# 原因: 缺少作者信息

# 原文件: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md
# 作者: Aware Cooperative
# 年份: 2022
# 标题: Delay Aware Cooperative Task Offloading for Multi
# 新文件名: cooperative2022DelAwaCoo.md
if [ -f "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" ]; then
    mv "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" "markdown/cooperative2022DelAwaCoo.md"
    echo "✓ 重命名: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloa... -> cooperative2022DelAwaCoo.md"
else
    echo "⚠ 文件不存在: markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md"
fi

# 无法处理: Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md
# 原因: 缺少年份信息

# 无法处理: Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md
# 原因: 缺少年份信息

# 无法处理: Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md
# 原因: 缺少年份信息

# 原文件: Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md
# 作者: Adaptive Bitrate
# 年份: 2024
# 标题: Adaptive Bitrate Video Caching in UAV Assisted MEC
# 新文件名: bitrate2024AdaBitVid.md
if [ -f "markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md" ]; then
    mv "markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md" "markdown/bitrate2024AdaBitVid.md"
    echo "✓ 重命名: Chen 等 - 2024 - Adaptive Bitrate Video Caching in ... -> bitrate2024AdaBitVid.md"
else
    echo "⚠ 文件不存在: markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md"
fi

# 原文件: Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md
# 作者: User Task
# 年份: 2025
# 标题: Multi User Task Offloading in UAV Assisted LEO Satellite Edge Computing A Game T...
# 新文件名: task2025MulUseTas.md
if [ -f "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" ]; then
    mv "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" "markdown/task2025MulUseTas.md"
    echo "✓ 重命名: Chen 等 - 2025 - Multi-User Task Offloading in UAV-... -> task2025MulUseTas.md"
else
    echo "⚠ 文件不存在: markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md"
fi

# 原文件: Chen-2025-TypeFly_ Low-Latency Drone Planning.md
# 作者: Latency Drone
# 年份: 2025
# 标题: TypeFly Low Latency Drone Planning
# 新文件名: drone2025TypLowLat.md
if [ -f "markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md" ]; then
    mv "markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md" "markdown/drone2025TypLowLat.md"
    echo "✓ 重命名: Chen-2025-TypeFly_ Low-Latency Drone Planning.md -> drone2025TypLowLat.md"
else
    echo "⚠ 文件不存在: markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md"
fi

# 无法处理: CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md
# 原因: 缺少作者信息

# 原文件: Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md
# 作者: Exploiting Computing
# 年份: 2024
# 标题: ParallEdge Exploiting Computing Mobility Parallel
# 新文件名: computing2024ParExpCom.md
if [ -f "markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md" ]; then
    mv "markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md" "markdown/computing2024ParExpCom.md"
    echo "✓ 重命名: Cong 等 - 2024 - ParallEdge Exploiting Computing-Mo... -> computing2024ParExpCom.md"
else
    echo "⚠ 文件不存在: markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md"
fi

# 无法处理: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 原因: 缺少年份信息

# 原文件: Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md
# 作者: Assisted Task
# 年份: 2024
# 标题: UAV Assisted Task Offloading in Vehicular Edge Com
# 新文件名: task2024UavAssTas.md
if [ -f "markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md" ]; then
    mv "markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md" "markdown/task2024UavAssTas.md"
    echo "✓ 重命名: Dai 等 - 2024 - UAV-Assisted Task Offloading in Veh... -> task2024UavAssTas.md"
else
    echo "⚠ 文件不存在: markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md"
fi

# 无法处理: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md
# 原因: 缺少年份信息

# 无法处理: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md
# 原因: 缺少年份信息

# 原文件: Dou-2025-Scheduling Drone and Mobile Charger v.md
# 作者: Scheduling Drone
# 年份: 2025
# 标题: Scheduling Drone and Mobile Charger v
# 新文件名: drone2025SchDroAnd.md
if [ -f "markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md" ]; then
    mv "markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md" "markdown/drone2025SchDroAnd.md"
    echo "✓ 重命名: Dou-2025-Scheduling Drone and Mobile Charger v.md -> drone2025SchDroAnd.md"
else
    echo "⚠ 文件不存在: markdown/Dou-2025-Scheduling Drone and Mobile Charger v.md"
fi

# 无法处理: Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span.md
# 原因: 缺少年份信息

# 无法处理: DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md
# 原因: 缺少年份信息

# 无法处理: Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md
# 原因: 缺少作者信息

# 无法处理: Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md
# 原因: 缺少年份信息

# 无法处理: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 原因: 缺少年份信息

# 无法处理: Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md
# 原因: 缺少作者信息

# 无法处理: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md
# 原因: 缺少年份信息

# 无法处理: Fission Spectral Clustering Strategy for UAV Swarm Networks.md
# 原因: 缺少年份信息

# 原文件: Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md
# 作者: Agent Reinforcement
# 年份: 2025
# 标题: CSMAAC Multi Agent Reinforcement Lea
# 新文件名: reinforcement2025CsmMulAge.md
if [ -f "markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md" ]; then
    mv "markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md" "markdown/reinforcement2025CsmMulAge.md"
    echo "✓ 重命名: Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md -> reinforcement2025CsmMulAge.md"
else
    echo "⚠ 文件不存在: markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md"
fi

# 原文件: Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md
# 作者: Dynamic Topology
# 年份: 2024
# 标题: Dynamic Topology Organization and Maintenance Algo
# 新文件名: topology2024DynTopOrg.md
if [ -f "markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md" ]; then
    mv "markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md" "markdown/topology2024DynTopOrg.md"
    echo "✓ 重命名: Gaydamaka 等 - 2024 - Dynamic Topology Organization... -> topology2024DynTopOrg.md"
else
    echo "⚠ 文件不存在: markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md"
fi

# 原文件: Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md
# 作者: Ground Node
# 年份: 2024
# 标题: Energy Efficient 3 D UAV Ground Node Accessing Using the Minimum Number of UAVs
# 新文件名: node2024EneEff3.md
if [ -f "markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md" ]; then
    mv "markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md" "markdown/node2024EneEff3.md"
    echo "✓ 重命名: Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground No... -> node2024EneEff3.md"
else
    echo "⚠ 文件不存在: markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md"
fi

# 原文件: Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md
# 作者: Coverage Probability
# 年份: 2024
# 标题: Gui和Cai 2024 Coverage Probability and Throughput Optimization in Integrated mmWa...
# 新文件名: probability2024Gui202Cov.md
if [ -f "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" ]; then
    mv "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" "markdown/probability2024Gui202Cov.md"
    echo "✓ 重命名: Gui和Cai - 2024 - Coverage Probability and Throughp... -> probability2024Gui202Cov.md"
else
    echo "⚠ 文件不存在: markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md"
fi

# 原文件: Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md
# 作者: Joint Optimization
# 年份: 2024
# 标题: Joint Optimization of Trajectory and Jamming Power
# 新文件名: optimization2024JoiOptOf.md
if [ -f "markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md" ]; then
    mv "markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md" "markdown/optimization2024JoiOptOf.md"
    echo "✓ 重命名: Guo 等 - 2024 - Joint Optimization of Trajectory an... -> optimization2024JoiOptOf.md"
else
    echo "⚠ 文件不存在: markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md"
fi

# 原文件: Guo-2025-Mighty_ Towards Long-Range and High-T.md
# 作者: Towards Long
# 年份: 2025
# 标题: Mighty Towards Long Range and High T
# 新文件名: long2025MigTowLon.md
if [ -f "markdown/Guo-2025-Mighty_ Towards Long-Range and High-T.md" ]; then
    mv "markdown/Guo-2025-Mighty_ Towards Long-Range and High-T.md" "markdown/long2025MigTowLon.md"
    echo "✓ 重命名: Guo-2025-Mighty_ Towards Long-Range and High-T.md -> long2025MigTowLon.md"
else
    echo "⚠ 文件不存在: markdown/Guo-2025-Mighty_ Towards Long-Range and High-T.md"
fi

# 无法处理: HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md
# 原因: 缺少年份信息

# 原文件: Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md
# 作者: Collaborative Route
# 年份: 2024
# 标题: Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disa...
# 新文件名: route2024ColRouPla.md
if [ -f "markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md" ]; then
    mv "markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md" "markdown/route2024ColRouPla.md"
    echo "✓ 重命名: Han 等 - 2024 - Collaborative Route Planning of UAV... -> route2024ColRouPla.md"
else
    echo "⚠ 文件不存在: markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md"
fi

# 原文件: He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md
# 作者: Balancing Total
# 年份: 2024
# 标题: Balancing Total Energy Consumption and Mean Makesp
# 新文件名: total2024BalTotEne.md
if [ -f "markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md" ]; then
    mv "markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md" "markdown/total2024BalTotEne.md"
    echo "✓ 重命名: He 等 - 2024 - Balancing Total Energy Consumption a... -> total2024BalTotEne.md"
else
    echo "⚠ 文件不存在: markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md"
fi

# 原文件: Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md
# 作者: Finite Block
# 年份: 2024
# 标题: Finite Block Length NOMA MU Pairing UAV Enable System Performance Analysis and O...
# 新文件名: block2024FinBloLen.md
if [ -f "markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md" ]; then
    mv "markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md" "markdown/block2024FinBloLen.md"
    echo "✓ 重命名: Hoang 等 - 2024 - Finite Block Length NOMA MU Pairi... -> block2024FinBloLen.md"
else
    echo "⚠ 文件不存在: markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md"
fi

# 原文件: Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md
# 作者: Dynamic Task
# 年份: 2024
# 标题: Dynamic Task Offloading for Multi UAVs in Vehicular Edge Computing With Delay Gu...
# 新文件名: task2024DynTasOff.md
if [ -f "markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md" ]; then
    mv "markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md" "markdown/task2024DynTasOff.md"
    echo "✓ 重命名: Huang 等 - 2024 - Dynamic Task Offloading for Multi... -> task2024DynTasOff.md"
else
    echo "⚠ 文件不存在: markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md"
fi

# 原文件: IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md
# 作者: Sky Autonomous
# 年份: 2024
# 标题: IEEE Transactions on Mobile Computing 2024 All Sky Autonomous Computing in UAV S...
# 新文件名: autonomous2024IeeTraOn.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" "markdown/autonomous2024IeeTraOn.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - All... -> autonomous2024IeeTraOn.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md"
fi

# 原文件: IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md
# 作者: Joint Task
# 年份: 2024
# 标题: IEEE Transactions on Mobile Computing 2024 Joint Task Offloading, Resource Alloc...
# 新文件名: task2024IeeTraOn.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" "markdown/task2024IeeTraOn.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - Joi... -> task2024IeeTraOn.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md"
fi

# 原文件: IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md
# 作者: Service Experience
# 年份: 2024
# 标题: IEEE Transactions on Mobile Computing 2024 Service Experience Oriented Cooperati...
# 新文件名: experience2024IeeTraOn.md
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" "markdown/experience2024IeeTraOn.md"
    echo "✓ 重命名: IEEE Transactions on Mobile Computing - 2024 - Ser... -> experience2024IeeTraOn.md"
else
    echo "⚠ 文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md"
fi

# 无法处理: Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md
# 原因: 缺少年份信息

# 无法处理: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 原因: 缺少年份信息

# 无法处理: J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems.md
# 原因: 缺少年份信息

# 无法处理: Jia2024.md
# 原因: 缺少年份信息

# 无法处理: Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md
# 原因: 缺少作者信息

# 无法处理: Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md
# 原因: 缺少年份信息

# 无法处理: Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md
# 原因: 缺少年份信息

# 无法处理: Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md
# 原因: 缺少年份信息

# 无法处理: Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md
# 原因: 缺少年份信息

# 无法处理: Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md
# 原因: 缺少年份信息

# 无法处理: Joint_UAV_Deployment_and_Resource_Allocation_in_THz-Assisted_MEC-Enabled_Integrated_Space-Air-Ground_Networks.md
# 原因: 缺少年份信息

# 无法处理: Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md
# 原因: 缺少年份信息

# 原文件: Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md
# 作者: Based Distributed
# 年份: 2024
# 标题: A Blockchain Based Distributed and Intelligent Clu
# 新文件名: distributed2024ABloBas.md
if [ -f "markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md" ]; then
    mv "markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md" "markdown/distributed2024ABloBas.md"
    echo "✓ 重命名: Karmakar 等 - 2024 - A Blockchain-Based Distributed... -> distributed2024ABloBas.md"
else
    echo "⚠ 文件不存在: markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md"
fi

# 原文件: Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md
# 作者: Novel Federated
# 年份: 2024
# 标题: A Novel Federated Learning Based Smart Power and 3
# 新文件名: federated2024ANovFed.md
if [ -f "markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md" ]; then
    mv "markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md" "markdown/federated2024ANovFed.md"
    echo "✓ 重命名: Karmakar 等 - 2024 - A Novel Federated Learning-Bas... -> federated2024ANovFed.md"
else
    echo "⚠ 文件不存在: markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md"
fi

# 原文件: Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md
# 作者: Improved Algorithms
# 年份: 2024
# 标题: Improved Algorithms for Co Scheduling of Edge Anal
# 新文件名: algorithms2024ImpAlgFor.md
if [ -f "markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md" ]; then
    mv "markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md" "markdown/algorithms2024ImpAlgFor.md"
    echo "✓ 重命名: Khochare 等 - 2024 - Improved Algorithms for Co-Sch... -> algorithms2024ImpAlgFor.md"
else
    echo "⚠ 文件不存在: markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md"
fi

# 原文件: Kumar-2025-Drone-Assisted IRS System in 5G and.md
# 作者: Improving Reliability
# 年份: 2025
# 标题: Drone Assisted IRS System in 5G and
# 新文件名: reliability2025DroAssIrs.md
if [ -f "markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md" ]; then
    mv "markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md" "markdown/reliability2025DroAssIrs.md"
    echo "✓ 重命名: Kumar-2025-Drone-Assisted IRS System in 5G and.md -> reliability2025DroAssIrs.md"
else
    echo "⚠ 文件不存在: markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md"
fi

# 无法处理: LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md
# 原因: 缺少年份信息

# 无法处理: LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md
# 原因: 缺少年份信息

# 无法处理: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md
# 原因: 缺少年份信息

# 原文件: Lee-2025-Adaptive Stabilization Control by Dee.md
# 作者: Adaptive Stabilization
# 年份: 2025
# 标题: Adaptive Stabilization Control by Dee
# 新文件名: stabilization2025AdaStaCon.md
if [ -f "markdown/Lee-2025-Adaptive Stabilization Control by Dee.md" ]; then
    mv "markdown/Lee-2025-Adaptive Stabilization Control by Dee.md" "markdown/stabilization2025AdaStaCon.md"
    echo "✓ 重命名: Lee-2025-Adaptive Stabilization Control by Dee.md -> stabilization2025AdaStaCon.md"
else
    echo "⚠ 文件不存在: markdown/Lee-2025-Adaptive Stabilization Control by Dee.md"
fi

# 原文件: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md
# 作者: Objective Optimization
# 年份: 2024
# 标题: Multi Objective Optimization for UAV Swarm Assiste
# 新文件名: optimization2024MulObjOpt.md
if [ -f "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" ]; then
    mv "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" "markdown/optimization2024MulObjOpt.md"
    echo "✓ 重命名: Li 等 - 2024 - Multi-Objective Optimization for UAV... -> optimization2024MulObjOpt.md"
else
    echo "⚠ 文件不存在: markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md"
fi

# 原文件: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 作者: Dynamic Routing
# 年份: 2025
# 标题: Dynamic Routing Mechanism for Load Dis
# 新文件名: routing2025DynRouMec.md
if [ -f "markdown/Li-2025-Dynamic Routing Mechanism for Load Dis.md" ]; then
    mv "markdown/Li-2025-Dynamic Routing Mechanism for Load Dis.md" "markdown/routing2025DynRouMec.md"
    echo "✓ 重命名: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> routing2025DynRouMec.md"
else
    echo "⚠ 文件不存在: markdown/Li-2025-Dynamic Routing Mechanism for Load Dis.md"
fi

# 原文件: Li-2025-Taming Event Cameras With Bio-Inspired.md
# 作者: Taming Event
# 年份: 2025
# 标题: Taming Event Cameras With Bio Inspired
# 新文件名: event2025TamEveCam.md
if [ -f "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" ]; then
    mv "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" "markdown/event2025TamEveCam.md"
    echo "✓ 重命名: Li-2025-Taming Event Cameras With Bio-Inspired.md -> event2025TamEveCam.md"
else
    echo "⚠ 文件不存在: markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md"
fi

# 原文件: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md
# 作者: Collaborative Beamforming
# 年份: 2024
# 标题: UAV enabled Collaborative Beamforming via Multi Agent Deep Reinforcement Learnin...
# 新文件名: beamforming2024UavEnaCol.md
if [ -f "markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md" ]; then
    mv "markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md" "markdown/beamforming2024UavEnaCol.md"
    echo "✓ 重命名: Liu 等 - 2024 - UAV-enabled Collaborative Beamformi... -> beamforming2024UavEnaCol.md"
else
    echo "⚠ 文件不存在: markdown/Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md"
fi

# 原文件: Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md
# 作者: Resource Allocation
# 年份: 2025
# 标题: Resource Allocation for Adaptive Beam Alignment in UAV Assisted Integrated Sensi...
# 新文件名: allocation2025ResAllFor.md
if [ -f "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" ]; then
    mv "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" "markdown/allocation2025ResAllFor.md"
    echo "✓ 重命名: Liu 等 - 2025 - Resource Allocation for Adaptive Be... -> allocation2025ResAllFor.md"
else
    echo "⚠ 文件不存在: markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md"
fi

# 原文件: Liu-2025-Delay-Sensitive Goods Delivery and In.md
# 作者: Sensitive Goods
# 年份: 2025
# 标题: Delay Sensitive Goods Delivery and In
# 新文件名: goods2025DelSenGoo.md
if [ -f "markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md" ]; then
    mv "markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md" "markdown/goods2025DelSenGoo.md"
    echo "✓ 重命名: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> goods2025DelSenGoo.md"
else
    echo "⚠ 文件不存在: markdown/Liu-2025-Delay-Sensitive Goods Delivery and In.md"
fi

# 无法处理: Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md
# 原因: 缺少年份信息

# 原文件: Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md
# 作者: Deployment Cost
# 年份: 2024
# 标题: Deployment Cost Aware UAV and BS Collaboration in Cell Free Integrated Aerial Te...
# 新文件名: cost2024DepCosAwa.md
if [ -f "markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md" ]; then
    mv "markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md" "markdown/cost2024DepCosAwa.md"
    echo "✓ 重命名: Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS... -> cost2024DepCosAwa.md"
else
    echo "⚠ 文件不存在: markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md"
fi

# 无法处理: Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md
# 原因: 缺少年份信息

# 无法处理: Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md
# 原因: 缺少年份信息

# 无法处理: Multi-UAV-Assisted_MEC_in_Internet_of_Vehicles_With_Combined_Multi-Modal_Semantic_Communication_Under_Jamming_Attacks.md
# 原因: 缺少年份信息

# 无法处理: Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md
# 原因: 缺少年份信息

# 原文件: Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md
# 作者: Unmanned Aerial
# 年份: 2024
# 标题: On the Dilemma of Reliability or Security in Unman
# 新文件名: aerial2024OnTheDil.md
if [ -f "markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md" ]; then
    mv "markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md" "markdown/aerial2024OnTheDil.md"
    echo "✓ 重命名: Nguyen 等 - 2024 - On the Dilemma of Reliability or... -> aerial2024OnTheDil.md"
else
    echo "⚠ 文件不存在: markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md"
fi

# 原文件: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md
# 作者: Agent Deep
# 年份: 2024
# 标题: Multi Agent Deep Reinforcement Learning Based UAV
# 新文件名: deep2024MulAgeDee.md
if [ -f "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" ]; then
    mv "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" "markdown/deep2024MulAgeDee.md"
    echo "✓ 重命名: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Lea... -> deep2024MulAgeDee.md"
else
    echo "⚠ 文件不存在: markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md"
fi

# 无法处理: Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md
# 原因: 缺少年份信息

# 无法处理: Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios.md
# 原因: 缺少年份信息

# 无法处理: Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md
# 原因: 缺少年份信息

# 无法处理: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md
# 原因: 缺少年份信息

# 原文件: Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md
# 作者: Aware Perspective
# 年份: 2024
# 标题: Panahi 和 Panahi 2024 Reliable and Energy Efficient UAV Communications
# 新文件名: perspective2024Pan和Pan.md
if [ -f "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" ]; then
    mv "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" "markdown/perspective2024Pan和Pan.md"
    echo "✓ 重命名: Panahi 和 Panahi - 2024 - Reliable and Energy-Effic... -> perspective2024Pan和Pan.md"
else
    echo "⚠ 文件不存在: markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md"
fi

# 无法处理: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md
# 原因: 缺少年份信息

# 原文件: Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md
# 作者: Integrated Host
# 年份: 2024
# 标题: Integrated Host and Content Centric Routing for E
# 新文件名: host2024IntHosAnd.md
if [ -f "markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md" ]; then
    mv "markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md" "markdown/host2024IntHosAnd.md"
    echo "✓ 重命名: Qiu 等 - 2024 - Integrated Host- and Content-Centri... -> host2024IntHosAnd.md"
else
    echo "⚠ 文件不存在: markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md"
fi

# 无法处理: Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md
# 原因: 缺少年份信息

# 无法处理: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md
# 原因: 缺少年份信息

# 无法处理: Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control.md
# 原因: 缺少年份信息

# 无法处理: Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md
# 原因: 缺少年份信息

# 无法处理: Resource_Allocation_in_Blockchain_Integration_of_UAV-Enabled_MEC_Networks_A_Stackelberg_Differential_Game_Approach.md
# 原因: 缺少年份信息

# 无法处理: Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md
# 原因: 缺少作者信息

# 无法处理: Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md
# 原因: 缺少作者信息

# 无法处理: Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature.md
# 原因: 缺少年份信息

# 无法处理: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md
# 原因: 缺少年份信息

# 无法处理: Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md
# 原因: 缺少年份信息

# 原文件: Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md
# 作者: Stage Strategy
# 年份: 2023
# 标题: A Two Stage Strategy for UAV enabled Wireless Powe
# 新文件名: strategy2023ATwoSta.md
if [ -f "markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md" ]; then
    mv "markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md" "markdown/strategy2023ATwoSta.md"
    echo "✓ 重命名: Shi 等 - 2023 - A Two-Stage Strategy for UAV-enable... -> strategy2023ATwoSta.md"
else
    echo "⚠ 文件不存在: markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md"
fi

# 原文件: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md
# 作者: Energy Tradeoff
# 年份: 2024
# 标题: AoI and Energy Tradeoff for Aerial Ground Collaborative MEC A Multi Objective Le...
# 新文件名: tradeoff2024AoiAndEne.md
if [ -f "markdown/Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md" ]; then
    mv "markdown/Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md" "markdown/tradeoff2024AoiAndEne.md"
    echo "✓ 重命名: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial... -> tradeoff2024AoiAndEne.md"
else
    echo "⚠ 文件不存在: markdown/Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md"
fi

# 原文件: Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md
# 作者: Song
# 年份: 2024
# 标题: Methods to Assign UAVs for K Coverage and Rechargi
# 新文件名: song2024MetToAss.md
if [ -f "markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md" ]; then
    mv "markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md" "markdown/song2024MetToAss.md"
    echo "✓ 重命名: Song 等 - 2024 - Methods to Assign UAVs for K-Cover... -> song2024MetToAss.md"
else
    echo "⚠ 文件不存在: markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md"
fi

# 原文件: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md
# 作者: Catch Me
# 年份: 2025
# 标题: Catch Me If You Can Deep Meta RL for Search and Rescue Using LoRa UAV Networks
# 新文件名: me2025CatMeIf.md
if [ -f "markdown/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md" ]; then
    mv "markdown/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md" "markdown/me2025CatMeIf.md"
    echo "✓ 重命名: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL... -> me2025CatMeIf.md"
else
    echo "⚠ 文件不存在: markdown/Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md"
fi

# 无法处理: Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md
# 原因: 文件名冲突

# 原文件: Sun-2025-Aerial Reliable Collaborative Communi.md
# 作者: Aerial Reliable
# 年份: 2025
# 标题: Aerial Reliable Collaborative Communi
# 新文件名: reliable2025AerRelCol.md
if [ -f "markdown/Sun-2025-Aerial Reliable Collaborative Communi.md" ]; then
    mv "markdown/Sun-2025-Aerial Reliable Collaborative Communi.md" "markdown/reliable2025AerRelCol.md"
    echo "✓ 重命名: Sun-2025-Aerial Reliable Collaborative Communi.md -> reliable2025AerRelCol.md"
else
    echo "⚠ 文件不存在: markdown/Sun-2025-Aerial Reliable Collaborative Communi.md"
fi

# 无法处理: Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage.md
# 原因: 缺少年份信息

# 无法处理: TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md
# 原因: 缺少年份信息

# 原文件: Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md
# 作者: Agent Cooperation
# 年份: 2024
# 标题: Multi Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial ...
# 新文件名: cooperation2024MulAgeCoo.md
if [ -f "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" ]; then
    mv "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" "markdown/cooperation2024MulAgeCoo.md"
    echo "✓ 重命名: Tao 等 - 2024 - Multi-Agent Cooperation for Computi... -> cooperation2024MulAgeCoo.md"
else
    echo "⚠ 文件不存在: markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md"
fi

# 无法处理: Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md
# 原因: 缺少年份信息

# 原文件: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md
# 作者: Assisted Wireless
# 年份: 2024
# 标题: UAV Assisted Wireless Cooperative Communication an
# 新文件名: wireless2024UavAssWir.md
if [ -f "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" ]; then
    mv "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" "markdown/wireless2024UavAssWir.md"
    echo "✓ 重命名: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative ... -> wireless2024UavAssWir.md"
else
    echo "⚠ 文件不存在: markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md"
fi

# 无法处理: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md
# 原因: 缺少年份信息

# 无法处理: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md
# 原因: 缺少年份信息

# 无法处理: UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring.md
# 原因: 缺少年份信息

# 无法处理: UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming.md
# 原因: 缺少年份信息

# 无法处理: UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md
# 原因: 缺少年份信息

# 无法处理: UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach.md
# 原因: 缺少年份信息

# 无法处理: User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md
# 原因: 缺少年份信息

# 无法处理: VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md
# 原因: 缺少年份信息

# 原文件: Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md
# 作者: Objective Ant
# 年份: 2024
# 标题: Bi Objective Ant Colony Optimization for Trajectory Planning and Task Offloading...
# 新文件名: ant2024BiObjAnt.md
if [ -f "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" ]; then
    mv "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" "markdown/ant2024BiObjAnt.md"
    echo "✓ 重命名: Wang 等 - 2024 - Bi-Objective Ant Colony Optimizati... -> ant2024BiObjAnt.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md"
fi

# 原文件: Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md
# 作者: Decentralized Navigation
# 年份: 2024
# 标题: Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for...
# 新文件名: navigation2024DecNavWit.md
if [ -f "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" ]; then
    mv "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" "markdown/navigation2024DecNavWit.md"
    echo "✓ 重命名: Wang 等 - 2024 - Decentralized Navigation With Hete... -> navigation2024DecNavWit.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md"
fi

# 原文件: Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md
# 作者: Ensuring Threshold
# 年份: 2024
# 标题: Ensuring Threshold AoI for UAV Assisted Mobile Cro
# 新文件名: threshold2024EnsThrAoi.md
if [ -f "markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md" ]; then
    mv "markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md" "markdown/threshold2024EnsThrAoi.md"
    echo "✓ 重命名: Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Ass... -> threshold2024EnsThrAoi.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md"
fi

# 原文件: Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md
# 作者: Assisted Target
# 年份: 2024
# 标题: UAV Assisted Target Tracking and Computation Offloading in USV Based MEC Network...
# 新文件名: target2024UavAssTar.md
if [ -f "markdown/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md" ]; then
    mv "markdown/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md" "markdown/target2024UavAssTar.md"
    echo "✓ 重命名: Wang 等 - 2024 - UAV-Assisted Target Tracking and C... -> target2024UavAssTar.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md"
fi

# 原文件: Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md
# 作者: Wireless Powered
# 年份: 2024
# 标题: Wireless Powered Metaverse Joint Task Scheduling
# 新文件名: powered2024WirPowMet.md
if [ -f "markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md" ]; then
    mv "markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md" "markdown/powered2024WirPowMet.md"
    echo "✓ 重命名: Wang 等 - 2024 - Wireless Powered Metaverse Joint T... -> powered2024WirPowMet.md"
else
    echo "⚠ 文件不存在: markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md"
fi

# 原文件: Wang-2025-Optimizing Joint Speed and Altitude.md
# 作者: Optimizing Joint
# 年份: 2025
# 标题: Optimizing Joint Speed and Altitude
# 新文件名: joint2025OptJoiSpe.md
if [ -f "markdown/Wang-2025-Optimizing Joint Speed and Altitude.md" ]; then
    mv "markdown/Wang-2025-Optimizing Joint Speed and Altitude.md" "markdown/joint2025OptJoiSpe.md"
    echo "✓ 重命名: Wang-2025-Optimizing Joint Speed and Altitude.md -> joint2025OptJoiSpe.md"
else
    echo "⚠ 文件不存在: markdown/Wang-2025-Optimizing Joint Speed and Altitude.md"
fi

# 原文件: Wang-2025-Practical Optimizing UAV Trajectory.md
# 作者: Practical Optimizing
# 年份: 2025
# 标题: Practical Optimizing UAV Trajectory
# 新文件名: optimizing2025PraOptUav.md
if [ -f "markdown/Wang-2025-Practical Optimizing UAV Trajectory.md" ]; then
    mv "markdown/Wang-2025-Practical Optimizing UAV Trajectory.md" "markdown/optimizing2025PraOptUav.md"
    echo "✓ 重命名: Wang-2025-Practical Optimizing UAV Trajectory.md -> optimizing2025PraOptUav.md"
else
    echo "⚠ 文件不存在: markdown/Wang-2025-Practical Optimizing UAV Trajectory.md"
fi

# 原文件: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md
# 作者: Smart Shield
# 年份: 2025
# 标题: Smart Shield Prevent Aerial Eavesdr
# 新文件名: shield2025SmaShiPre.md
if [ -f "markdown/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md" ]; then
    mv "markdown/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md" "markdown/shield2025SmaShiPre.md"
    echo "✓ 重命名: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md -> shield2025SmaShiPre.md"
else
    echo "⚠ 文件不存在: markdown/Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md"
fi

# 原文件: Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md
# 作者: Hierarchical Network
# 年份: 2024
# 标题: Hierarchical Network Slicing for UAV Assisted Wireless Networks With Deployment ...
# 新文件名: network2024HieNetSli.md
if [ -f "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" ]; then
    mv "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" "markdown/network2024HieNetSli.md"
    echo "✓ 重命名: Wei 等 - 2024 - Hierarchical Network Slicing for UA... -> network2024HieNetSli.md"
else
    echo "⚠ 文件不存在: markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md"
fi

# 无法处理: Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md
# 原因: 缺少年份信息

# 原文件: Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md
# 作者: Optimization Protocol
# 年份: 2024
# 标题: MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy...
# 新文件名: protocol2024MacOptPro.md
if [ -f "markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md" ]; then
    mv "markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md" "markdown/protocol2024MacOptPro.md"
    echo "✓ 重命名: Wu 等 - 2024 - MAC Optimization Protocol for Cooper... -> protocol2024MacOptPro.md"
else
    echo "⚠ 文件不存在: markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md"
fi

# 原文件: Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md
# 作者: Vs Network
# 年份: 2024
# 标题: Multi UAVs Network Design Algorithms for Computed Rate Maximization
# 新文件名: network2024MulUavNet.md
if [ -f "markdown/Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md" ]; then
    mv "markdown/Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md" "markdown/network2024MulUavNet.md"
    echo "✓ 重命名: Wu 等 - 2024 - Multi-UAVs Network Design Algorithms... -> network2024MulUavNet.md"
else
    echo "⚠ 文件不存在: markdown/Wu 等 - 2024 - Multi-UAVs Network Design Algorithms for Computed Rate Maximization.md"
fi

# 原文件: Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md
# 作者: Stage Deep
# 年份: 2025
# 标题: Two Stage Deep Energy Optimization in IRS Assisted UAV Based Edge Computing Syst...
# 新文件名: deep2025TwoStaDee.md
if [ -f "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" ]; then
    mv "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" "markdown/deep2025TwoStaDee.md"
    echo "✓ 重命名: Wu 等 - 2025 - Two-Stage Deep Energy Optimization i... -> deep2025TwoStaDee.md"
else
    echo "⚠ 文件不存在: markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md"
fi

# 原文件: Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md
# 作者: Reward Maximization
# 年份: 2024
# 标题: Reward Maximization for Disaster Zone Monitoring W
# 新文件名: maximization2024RewMaxFor.md
if [ -f "markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md" ]; then
    mv "markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md" "markdown/maximization2024RewMaxFor.md"
    echo "✓ 重命名: Xu 等 - 2024 - Reward Maximization for Disaster Zon... -> maximization2024RewMaxFor.md"
else
    echo "⚠ 文件不存在: markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md"
fi

# 原文件: Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md
# 作者: Swarm Coordination
# 年份: 2024
# 标题: Semantic Aware UAV Swarm Coordination in the Metaverse A Reputation Based Incent...
# 新文件名: coordination2024SemAwaUav.md
if [ -f "markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md" ]; then
    mv "markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md" "markdown/coordination2024SemAwaUav.md"
    echo "✓ 重命名: Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordinatio... -> coordination2024SemAwaUav.md"
else
    echo "⚠ 文件不存在: markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md"
fi

# 原文件: Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md
# 作者: Towards Maximizing
# 年份: 2024
# 标题: Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling
# 新文件名: maximizing2024TowMaxCov.md
if [ -f "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" ]; then
    mv "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" "markdown/maximizing2024TowMaxCov.md"
    echo "✓ 重命名: Xue 等 - 2024 - Towards Maximizing Coverage of Targ... -> maximizing2024TowMaxCov.md"
else
    echo "⚠ 文件不存在: markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md"
fi

# 原文件: Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md
# 作者: Energy Efficient
# 年份: 2024
# 标题: Energy Efficient Transmission Strategy for Mobile
# 新文件名: efficient2024EneEffTra.md
if [ -f "markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md" ]; then
    mv "markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md" "markdown/efficient2024EneEffTra.md"
    echo "✓ 重命名: Yang 等 - 2024 - Energy Efficient Transmission Stra... -> efficient2024EneEffTra.md"
else
    echo "⚠ 文件不存在: markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md"
fi

# 原文件: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 作者: Hybrid Transformer
# 年份: 2025
# 标题: Hybrid Transformer Based Multi Agent R
# 新文件名: transformer2025HybTraBas.md
if [ -f "markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md" ]; then
    mv "markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md" "markdown/transformer2025HybTraBas.md"
    echo "✓ 重命名: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> transformer2025HybTraBas.md"
else
    echo "⚠ 文件不存在: markdown/Yu-2025-Hybrid Transformer Based Multi-Agent R.md"
fi

# 原文件: Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md
# 作者: Trajectory Optimization
# 年份: 2024
# 标题: 3D Trajectory Optimization for Multimission UAVs i
# 新文件名: optimization20243dTraOpt.md
if [ -f "markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md" ]; then
    mv "markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md" "markdown/optimization20243dTraOpt.md"
    echo "✓ 重命名: Zema 等 - 2024 - 3D Trajectory Optimization for Mul... -> optimization20243dTraOpt.md"
else
    echo "⚠ 文件不存在: markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md"
fi

# 原文件: Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md
# 作者: Autonomous Navigation
# 年份: 2024
# 标题: A3D Adaptive, Accurate, and Autonomous Navigation
# 新文件名: navigation2024A3dAdaAcc.md
if [ -f "markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md" ]; then
    mv "markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md" "markdown/navigation2024A3dAdaAcc.md"
    echo "✓ 重命名: Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autono... -> navigation2024A3dAdaAcc.md"
else
    echo "⚠ 文件不存在: markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md"
fi

# 原文件: Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md
# 作者: Aware Online
# 年份: 2024
# 标题: Interference Aware Online Optimization for Cellular Connected Multiple UAV Netwo...
# 新文件名: online2024IntAwaOnl.md
if [ -f "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" ]; then
    mv "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" "markdown/online2024IntAwaOnl.md"
    echo "✓ 重命名: Zhan 等 - 2024 - Interference-Aware Online Optimiza... -> online2024IntAwaOnl.md"
else
    echo "⚠ 文件不存在: markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md"
fi

# 原文件: Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md
# 作者: Tradeoff Between
# 年份: 2024
# 标题: Tradeoff Between Age of Information and Operation
# 新文件名: between2024TraBetAge.md
if [ -f "markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md" ]; then
    mv "markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md" "markdown/between2024TraBetAge.md"
    echo "✓ 重命名: Zhan 等 - 2024 - Tradeoff Between Age of Informatio... -> between2024TraBetAge.md"
else
    echo "⚠ 文件不存在: markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md"
fi

# 原文件: Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md
# 作者: Task Offloading
# 年份: 2024
# 标题: Task Offloading and Trajectory Optimization for Secure Communications in Dynamic...
# 新文件名: offloading2024TasOffAnd.md
if [ -f "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" ]; then
    mv "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" "markdown/offloading2024TasOffAnd.md"
    echo "✓ 重命名: Zhang 等 - 2024 - Task Offloading and Trajectory Op... -> offloading2024TasOffAnd.md"
else
    echo "⚠ 文件不存在: markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md"
fi

# 原文件: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md
# 作者: Enabled Collaborative
# 年份: 2024
# 标题: UAV Swarm Enabled Collaborative Secure Relay Communications With Time Domain Col...
# 新文件名: collaborative2024UavSwaEna.md
if [ -f "markdown/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md" ]; then
    mv "markdown/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md" "markdown/collaborative2024UavSwaEna.md"
    echo "✓ 重命名: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative S... -> collaborative2024UavSwaEna.md"
else
    echo "⚠ 文件不存在: markdown/Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md"
fi

# 原文件: Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md
# 作者: Large Models
# 年份: 2025
# 标题: Large Models for Aerial Edges An Edge Cloud Model Evolution and Communication Pa...
# 新文件名: models2025LarModFor.md
if [ -f "markdown/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md" ]; then
    mv "markdown/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md" "markdown/models2025LarModFor.md"
    echo "✓ 重命名: Zhang 等 - 2025 - Large Models for Aerial Edges An ... -> models2025LarModFor.md"
else
    echo "⚠ 文件不存在: markdown/Zhang 等 - 2025 - Large Models for Aerial Edges An Edge-Cloud Model Evolution and Communication Paradigm.md"
fi

# 原文件: Zhang-2025-Multi-Objective Aerial Collaborativ.md
# 作者: Objective Aerial
# 年份: 2025
# 标题: Multi Objective Aerial Collaborativ
# 新文件名: aerial2025MulObjAer.md
if [ -f "markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md" ]; then
    mv "markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md" "markdown/aerial2025MulObjAer.md"
    echo "✓ 重命名: Zhang-2025-Multi-Objective Aerial Collaborativ.md -> aerial2025MulObjAer.md"
else
    echo "⚠ 文件不存在: markdown/Zhang-2025-Multi-Objective Aerial Collaborativ.md"
fi

# 原文件: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 作者: Optimizing Monitoring
# 年份: 2025
# 标题: Optimizing Monitoring Utility of Un
# 新文件名: monitoring2025OptMonUti.md
if [ -f "markdown/Zhang-2025-Optimizing Monitoring Utility of Un.md" ]; then
    mv "markdown/Zhang-2025-Optimizing Monitoring Utility of Un.md" "markdown/monitoring2025OptMonUti.md"
    echo "✓ 重命名: Zhang-2025-Optimizing Monitoring Utility of Un.md -> monitoring2025OptMonUti.md"
else
    echo "⚠ 文件不存在: markdown/Zhang-2025-Optimizing Monitoring Utility of Un.md"
fi

# 原文件: Zhang-2025-Quantum-Assisted Online Task Offloa.md
# 作者: Assisted Online
# 年份: 2025
# 标题: Quantum Assisted Online Task Offloa
# 新文件名: online2025QuaAssOnl.md
if [ -f "markdown/Zhang-2025-Quantum-Assisted Online Task Offloa.md" ]; then
    mv "markdown/Zhang-2025-Quantum-Assisted Online Task Offloa.md" "markdown/online2025QuaAssOnl.md"
    echo "✓ 重命名: Zhang-2025-Quantum-Assisted Online Task Offloa.md -> online2025QuaAssOnl.md"
else
    echo "⚠ 文件不存在: markdown/Zhang-2025-Quantum-Assisted Online Task Offloa.md"
fi

# 原文件: Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md
# 作者: On Designing
# 年份: 2024
# 标题: On Designing Multi UAV Aided Wireless Powered Dynamic Communication via Hierarch...
# 新文件名: designing2024OnDesMul.md
if [ -f "markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md" ]; then
    mv "markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md" "markdown/designing2024OnDesMul.md"
    echo "✓ 重命名: Zhao 等 - 2024 - On Designing Multi-UAV Aided Wirel... -> designing2024OnDesMul.md"
else
    echo "⚠ 文件不存在: markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md"
fi

# 原文件: Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md
# 作者: Joint Content
# 年份: 2025
# 标题: Joint Content Caching, Service Placement, and Task Offloading in UAV Enabled Mob...
# 新文件名: content2025JoiConCac.md
if [ -f "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" "markdown/content2025JoiConCac.md"
    echo "✓ 重命名: Zhao 等 - 2025 - Joint Content Caching, Service Pla... -> content2025JoiConCac.md"
else
    echo "⚠ 文件不存在: markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md"
fi

# 原文件: Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md
# 作者: Joint Optimization
# 年份: 2025
# 标题: Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV Ass...
# 新文件名: optimization2025JoiOptOf.md
if [ -f "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" "markdown/optimization2025JoiOptOf.md"
    echo "✓ 重命名: Zhao 等 - 2025 - Joint Optimization of Trajectory, ... -> optimization2025JoiOptOf.md"
else
    echo "⚠ 文件不存在: markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md"
fi

# 原文件: Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md
# 作者: Content Delivery
# 年份: 2024
# 标题: Content Delivery Performance Analysis of a Cache E
# 新文件名: delivery2024ConDelPer.md
if [ -f "markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md" ]; then
    mv "markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md" "markdown/delivery2024ConDelPer.md"
    echo "✓ 重命名: Zheng 等 - 2024 - Content Delivery Performance Anal... -> delivery2024ConDelPer.md"
else
    echo "⚠ 文件不存在: markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md"
fi

# 原文件: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md
# 作者: Enabled Collaborative
# 年份: 2025
# 标题: UAV Swarm Enabled Collaborative Pos
# 新文件名: collaborative2025UavSwaEna.md
if [ -f "markdown/Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md" ]; then
    mv "markdown/Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md" "markdown/collaborative2025UavSwaEna.md"
    echo "✓ 重命名: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md -> collaborative2025UavSwaEna.md"
else
    echo "⚠ 文件不存在: markdown/Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md"
fi

# 原文件: Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md
# 作者: Federated Digital
# 年份: 2024
# 标题: A Federated Digital Twin Framework for UAVs Based
# 新文件名: digital2024AFedDig.md
if [ -f "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" ]; then
    mv "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" "markdown/digital2024AFedDig.md"
    echo "✓ 重命名: Zhou 等 - 2024 - A Federated Digital Twin Framework... -> digital2024AFedDig.md"
else
    echo "⚠ 文件不存在: markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md"
fi

# 无法处理: Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua.md
# 原因: 文件名冲突

# 原文件: Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md
# 作者: Augmented Multi
# 年份: 2024
# 标题: Symmetry Augmented Multi Agent Reinforcement Learning for Scalable UAV Trajector...
# 新文件名: multi2024SymAugMul.md
if [ -f "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" ]; then
    mv "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" "markdown/multi2024SymAugMul.md"
    echo "✓ 重命名: Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Rei... -> multi2024SymAugMul.md"
else
    echo "⚠ 文件不存在: markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md"
fi

# 原文件: Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md
# 作者: Collaborative Reinforcement
# 年份: 2024
# 标题: Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Traject...
# 新文件名: reinforcement2024ColReiLea.md
if [ -f "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" ]; then
    mv "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" "markdown/reinforcement2024ColReiLea.md"
    echo "✓ 重命名: Zhu 等 - 2024 - Collaborative Reinforcement Learnin... -> reinforcement2024ColReiLea.md"
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


# 以下文件无法自动处理，需要手动检查：

# 文件: 1570937393.md
# 前5行预览:
# # An Online Joint Optimization Approach for QoE Maximization in UAV-Enabled Mobile Edge Computing

â¡School of Computer Science and Technology, Dalian University of Technology, Dalian 116024, China

...

# 文件: 1570937499.md
# 前5行预览:
# INFOCOM 2024 1570937499

# A Two Time-Scale Joint Optimization Approach for UAV-assisted MEC

Zemin Sunâ , Geng Sunâ â, Long Heâ , Fang Meiâ , Shuang Liangâ¡, Yanheng Liuâ 

# 文件: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md
# 前5行预览:
# # A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection

Fadhila Tlili , Samiha Ayed , and Lamia Chaari Fourati

AbstractâA resilient and guaranteed Unmanned Aeri...

# 文件: ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md
# 前5行预览:
# # ASSUME: An Optimal Algorithm to Minimize UAV Energy by Altitude and Speed Scheduling

Jianping Huang , Feng Shan , Member, IEEE, Junzhou Luo , Member, IEEE, Runqun Xiong , Member, IEEE, and Wenjia W...

# 文件: A_Fast_UAV_Trajectory_Planning_Framework_in_RIS-Assisted_Communication_Systems_With_Accelerated_Learning_via_Multithreading_and_Federating.md
# 前5行预览:
# # A Fast UAV Trajectory Planning Framework in RIS-Assisted Communication Systems With Accelerated Learning via Multithreading and Federating

Jun Huang , Senior Member, IEEE, Beining Wu , Student Memb...

# 文件: A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md
# 前5行预览:
# # A Holistic and Hybrid Service Selection Strategy for MEC-Based UAV Last-Mile Delivery Systems

Jia Xu , Member, IEEE, Xiao Liu , Senior Member, IEEE, Azadeh Ghari Neiat , Liju Chu , Xuejun Li , Memb...

# 文件: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md
# 前5行预览:
# # A Joint Secure Mechanism of Multi-Task Learning for a UAV Team Under FDI Attacks

Rongfei Zeng , Member, IEEE, Chenyang Jiang , Xingwei Wang , and Baochun Li , Fellow, IEEE

AbstractâA UAV team sh...

# 文件: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# 前5行预览:
# # A Multi-UAV Cooperative Task Scheduling in Dynamic Environments: Throughput Maximization

Liang Zhao , Member, IEEE, Shuo Li , Zhiyuan Tan , Ammar Hawbani ,

Stelios Timotheou , Senior Member, IEEE,...

# 文件: A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md
# 前5行预览:
# # A Multimodal Scale Normalization Framework for Vision-Radar Small UAV Positioning

Yiyao Wan , Jiahuan Ji , Member, IEEE, Wenqing Xie, Guangyu Wu , Fuhui Zhou , Senior Member, IEEE, and Qihui Wu , F...

# 文件: A_Novel_MRR-UAV-Based_Relay_With_Optical_Network_Coding_A_Comparative_Study_With_Optical_IRS_and_Conventional_UAV_Relaying.md
# 前5行预览:
# # A Novel MRR-UAV-Based Relay With Optical Network Coding: A Comparative Study With Optical IRS and Conventional UAV Relaying

Mohammad Taghi Dabiri and Mazen Hasna , Senior Member, IEEE

Abstractâ ...

# 文件: A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md
# 前5行预览:
# # A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV Named Data Networking

Chenlang Jin , Graduate Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, J...

# 文件: Adaptive_3D_Placement_of_Multiple_UAV-Mounted_Base_Stations_in_6G_Airborne_Small_Cells_With_Deep_Reinforcement_Learning.md
# 前5行预览:
# # Adaptive 3D Placement of Multiple UAV-Mounted Base Stations in 6G Airborne Small Cells With Deep Reinforcement Learning

Linh T. Hoang , Chuyen T. Nguyen , Hoang D. Le, and Anh T. Pham , Senior Memb...

# 文件: AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md
# 前5行预览:
# # AeroEcho: Towards Agricultural Low-power Wide-area Backscatter with Aerial Excitation Source

Yidong Ren, Gen Li, Yimeng Liu, Younsuk Dong, Zhichao Cao

Michigan State University

# 文件: Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md
# 前5行预览:
# # Against Mobile Collusive Eavesdroppers: Cooperative Secure Transmission and Computation in UAV-Assisted MEC Networks

Mingxiong Zhao , Member, IEEE, Zirui Wang, Kun Guo , Member, IEEE, Rongqian Zhan...

# 文件: Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md
# 前5行预览:
# # Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-UUV Networks in Underwater Target Hunting

Xiangwang Hou , Member, IEEE, Tianyu Xing, Jingjing Wang , Senior Member, I...

# 文件: An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md
# 前5行预览:
# . RESEARCH PAPER .

August 2024, Vol. 67, Iss. 8, 182305:1â182305:15   
https://doi.org/10.1007/s11432-024-4056-8


# 文件: Anchor_A_Novel_Modeling_Methodology_for_Cooperative_UAV-MEC_Based_on_Stochastic_Geometry.md
# 前5行预览:
# # Anchor: A Novel Modeling Methodology forS 0(&4XHXHHOHQJWK Cooperative UAV-MEC Based on Stochastic+DQGRII3URF8\$9&R038\$9&R036HW2 K c  ZL Geometry

Yan Li1, Lailong Luo1, Bangbang Ren1, D...

# 文件: Attitude control of a novel tilt-wing UAV in hovering flight..md
# 前5行预览:
# . MOOP .

May 2023, Vol. 66 154201:1â154201:3   
https://doi.org/10.1007/s11432-022-3605-5


# 文件: Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md
# 前5行预览:
# . Supplementary File .

# Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems

Yuewei WU1, Peng XU1\*, Yi LV1, Dongming Wang2\*, Feifei Gao3\* ...

# 文件: Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md
# 前5行预览:
# # Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV Wireless Networks

Mingyue Xie , Zheng Chang , Senior Member, IEEE, Li Wang , Senior Member, IEEE, and Geyong Min , Senior M...

# 文件: Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md
# 前5行预览:
# # Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation in UAV-Assisted Wireless Networks

Qichao Xu , Zhou Su , Haixia Peng , Yuan Wu , and Ruidong Li , Senior Member, IEEE
...

# 文件: CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md
# 前5行预览:
# . LETTER .

May 2024, Vol. 67, Iss. 5, 159103:1â159103:2   
https://doi.org/10.1007/s11432-023-3984-7


# 文件: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 前5行预览:
# # Cooperative UAV-Mounted RISs-Assisted Energy-Efficient Communications

Hongyang Pan , Yanheng Liu , Geng Sun , Senior Member, IEEE, Qingqing Wu , Senior Member, IEEE, Tierui Gong , Member, IEEE, Pen...

# 文件: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md
# 前5行预览:
# # Deep Graph Reinforcement Learning for UAV-Enabled Multi-User Secure Communications

Xiao Tang , Member, IEEE, Kexin Zhao, Chao Shen , Senior Member, IEEE, Qinghe Du , Member, IEEE, Yichen Wang , Mem...

# 文件: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md
# 前5行预览:
# # Digital Twin Empowered mmWave Multi-Hop V2X Routing Scheme With UAV Assistance

Taolue Zhou , Xiaohan Wu, and Xinming Zhang , Senior Member, IEEE

AbstractâIn VANETs, millimeter wave (mmWave) is c...

# 文件: Drone-Assisted_IRS_System_in_5G_and_Beyond_Improving_Reliability_and_Enhancing_the_Network_Life_Span.md
# 前5行预览:
# # Drone-Assisted IRS System in 5G and Beyond: Improving Reliability and Enhancing the Network Life Span

Pankaj Kumar , Member, IEEE, Nikita Goel , and Manoj Tolani , Senior Member, IEEE

AbstractâT...

# 文件: DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md
# 前5行预览:
# # DroneMA: Drone Mobility Alignment Countering AI-based Spoofing Attacks

Weiyang Li1, Ning Wang1\*, Chuan Ma1, Tao Xiang1, Kai Zeng2

1College of computer science, Chongqing University, China

# 文件: Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md
# 前5行预览:
# . RESEARCH PAPER .

Special Topic: UAV Swarm Autonomous Control

August 2024, Vol. 67, Iss. 8, 180205:1â180205:18 https://doi.org/10.1007/s11432-023-4099-x

# 文件: Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md
# 前5行预览:
# # Dynamic Routing Mechanism for Load Distribution in UAV Swarm Networks With Edge Caching

Qun Li , Student Member, IEEE, Zunliang Wang , Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianl...

# 文件: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 前5行预览:
# # Energy-Efficient 3-D Data Collection for Multi-UAV Assisted Mobile Crowdsensing

Luwei Fu , Zhiwei Zhao , Member, IEEE, Geyong Min , Wang Miao , Liang Zhao , and Wenjie Huang

AbstractâMobile Crow...

# 文件: Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md
# 前5行预览:
# . RESEARCH PAPER .

December 2023, Vol. 66 222303:1â222303:15   
https://doi.org/10.1007/s11432-023-3821-3


# 文件: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md
# 前5行预览:
# # Exploring the Robustness: Hierarchical Federated Learning Framework for Object Detection of UAV Cluster

Xingyu Li , Wenzhe Zhang, Linfeng Liu , and Jia Xu , Senior Member, IEEE

AbstractâThe depl...

# 文件: Fission Spectral Clustering Strategy for UAV Swarm Networks.md
# 前5行预览:
# # Fission Spectral Clustering Strategy for UAV Swarm Networks

Gepeng Zhu , Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member, IEEE, Zunliang Wang , Graduate Student Member, IEEE, Di Wu , Student...

# 文件: HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md
# 前5行预览:
# # HaDT: Hardening Digital Twins for UAVs-Based Industrial Logistics Distribution Systems

Longyu Zhou1, Supeng Leng2, and Tony Q.S. Quek1

1Information Systems Technology and Design, Singapore Univers...

# 文件: Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md
# 前5行预览:
# # Improving Data Collection Efficiency of UAV-Assisted LoRa Networks via Directivity-Aware Link Model

Jiaqi Zhang , Xiaolong Zheng , Member, IEEE, Ruinan Li , Liang Liu , Member, IEEE, Huadong Ma , F...

# 文件: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 前5行预览:
# # Improving User QoE via Joint Trajectory and Resource Optimization in Multi-UAV Assisted MEC

Yang Gao , Member, IEEE, Jun Tao , Member, IEEE, Yifan Xu , Member, IEEE, Zuyan Wang , Yu Gao , and Meili...

# 文件: J--text-C---5--A Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems.md
# 前5行预览:
# # $\mathrm { J C ^ { 5 } A }$ : Service Delay Minimization for Aerial MEC-Assisted Industrial Cyber-Physical Systems

Geng Sun , Senior Member, IEEE, Jiaxu Wu, Zemin Sun , Member, IEEE, Long He , Jiac...

# 文件: Jia2024.md
# 前5行预览:
# # Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices

Riheng Jia , Qiyong Fu , Zhonglong Zheng , Guanglin Zhang , Member, IEEE, and Minglu Li , Fellow, IEEE

A...

# 文件: Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md
# 前5行预览:
# . RESEARCH PAPER .

September 2023, Vol. 66 192303:1â192303:20   
https://doi.org/10.1007/s11432-022-3667-3


# 文件: Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md
# 前5行预览:
# # Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-Enabled Large-Scale Mobile Edge Computing

Shoufei Han , Xiaojing Liu , MengChu Zhou , Fellow, IEEE, Kun Zhu , Member, ...

# 文件: Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md
# 前5行预览:
# # Joint Optimization of Beamforming and Trajectory for UAV-RIS-Assisted MU-MISO Systems Using GNN and SD3

Shumo Wang , Student Member, IEEE, Xiaoqin Song , Tiecheng Song , Member, IEEE, and Yang Yang...

# 文件: Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md
# 前5行预览:
# # Joint Positioning and Computation Offloading in Multi-UAV MEC for Low Latency Applications: A Proximal Policy Optimization Approach

Yuhui Wang , Student Member, IEEE, Junaid Farooq , Senior Member,...

# 文件: Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md
# 前5行预览:
# # Joint Task Offloading and Migration Optimization in UAV-Enabled Dynamic MEC Networks

Liang Wang , Member, IEEE, Bingnan Shen , Lianbo Ma , Senior Member, IEEE, Yao Zhang Yingnan Zhao , Hongzhi Guo ...

# 文件: Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md
# 前5行预览:
# # Joint Trajectory Optimization and Resource Allocation in UAV-MEC Systems: A Lyapunov-Assisted DRL Approach

Ying Chen , Senior Member, IEEE, Yaozong Yang , Yuan Wu , Senior Member, IEEE, Jiwei Huang...

# 文件: Joint_UAV_Deployment_and_Resource_Allocation_in_THz-Assisted_MEC-Enabled_Integrated_Space-Air-Ground_Networks.md
# 前5行预览:
# # Joint UAV Deployment and Resource Allocation in THz-Assisted MEC-Enabled Integrated Space-Air-Ground Networks

Yan Kyaw Tun , Member, IEEE, GyÃ¶rgy DÃ¡n , Senior Member, IEEE, Yu Min Park and Choong...

# 文件: Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md
# 前5行预览:
# # Jointly Optimizing the Energy and Time for Multi-UAV 3-D Coverage of Terrestrial Regions

Hao Gong , Baoqi Huang , Senior Member, IEEE, Bing Jia , Member, IEEE, Lifei Hao , Member, IEEE, and Zhenwei...

# 文件: LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md
# 前5行预览:
# Digital Object Identifier 10.1109/TKDE.2025.3579386

# LLM-QL: A LLM-Enhanced Q-Learning Approach for Scheduling Multiple Parallel Drones

Qian Zhou , Member, IEEE, Jiayang Wu , Mengyue Zhu, Yuhang Zh...

# 文件: LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md
# 前5行预览:
# # LSPSS: Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing

Haoyang Wang , Kai Fan , Member, IEEE, Chong Yu , Graduate Student Member, IEEE, Kuan Zhan...

# 文件: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md
# 前5行预览:
# # Large Models for Aerial Edges: An Edge-Cloud Model Evolution and Communication Paradigm

Shuhang Zhang, Member, IEEE, Qingyu Liu, Member, IEEE, Ke Chen , Member, IEEE, Boya Di , Member, IEEE, Hongli...

# 文件: Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md
# 前5行预览:
# # Maximizing Service Providerâs Profit in Multi-UAV 5G Network Via Deep Reinforcement Learning and Graph Coloring

Shilpi Kumari , Graduate Student Member, IEEE, and Ajay Pratap , Senior Member, IEE...

# 文件: Multi-Agent_Reinforcement_Learning_Aided_Computation_Offloading_in_Aerial_Computing_for_the_Internet-of-Things.md
# 前5行预览:
# # Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things

Zeyu Qin, Student Member, IEEE, Haipeng Yao , Senior Member, IEEE, Tianle Mai , Member...

# 文件: Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md
# 前5行预览:
# # Multi-Agent Reinforcement Learning in Adversarial Game Environments: Personalized Anti-Interference Strategies for Heterogeneous UAV Communication

Yeguang Qin , Graduate Student Member, IEEE, Jie T...

# 文件: Multi-UAV-Assisted_MEC_in_Internet_of_Vehicles_With_Combined_Multi-Modal_Semantic_Communication_Under_Jamming_Attacks.md
# 前5行预览:
# # Multi-UAV-Assisted MEC in Internet of Vehicles With Combined Multi-Modal Semantic Communication Under Jamming Attacks

Shuai Liu , Student Member, IEEE, Helin Yang , Senior Member, IEEE, Mengting Zh...

# 文件: Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md
# 前5行预览:
# # Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks

Shu-Wei Changâ , Jian-Jhih Kuoâ¡, Mong-Jen Kaoâ , Bo-Zhong Chenâ¡, and Qian-Jing Wangâ¡

â Dept. of Computer Scie...

# 文件: Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md
# 前5行预览:
# # Online Energy and Interference Management for Dynamic Target Tracking With Cellular-Connected UAV

Cheng Zhan , Member, IEEE, Huan Yan, Graduate Student Member, IEEE, Rongfei Fan , Member, IEEE, Han...

# 文件: Optical_RISs_Improve_the_Secret_Key_Rate_of_Free-Space_QKD_in_HAP-to-UAV_Scenarios.md
# 前5行预览:
# # Optical RISs Improve the Secret Key Rate of Free-Space QKD in HAP-to-UAV Scenarios

Phuc V. Trinh , Senior Member, IEEE, Shinya Sugiura , Senior Member, IEEE, Chao Xu , Senior Member, IEEE, and Lajo...

# 文件: Optimizing_Joint_Speed_and_Altitude_Schedule_for_UAV_Data_Collection_in_Low-Altitude_Airspace.md
# 前5行预览:
# # Optimizing Joint Speed and Altitude Schedule for UAV Data Collection in Low-Altitude Airspace

Yiqian Wang, Graduate Student Member, IEEE, Jianping Huang , Graduate Student Member, IEEE, Feng Shan ,...

# 文件: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md
# 前5行预览:
# # Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Effects

Haihan Zhang , Haipeng Dai , Yu Qiu , Enze Yu , Ruiben Zhou, Weijun Wang , Member, IEEE, Jingwu Wang, and Guiha...

# 文件: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md
# 前5行预览:
# # Practical Optimizing UAV Trajectory in Wireless Charging Networks: An Approximated Approach

Yundi Wang , Xiaoyu Wang , He Huang , Senior Member, IEEE, and Haipeng Dai , Senior Member, IEEE

Abstrac...

# 文件: Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md
# 前5行预览:
# # Quantum-Assisted Online Task Offloading and Resource Allocation in MEC-Enabled Satellite-Aerial-Terrestrial Integrated Networks

Yu Zhang , Student Member, IEEE, Yanmin Gong , Senior Member, IEEE, L...

# 文件: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md
# 前5行预览:
# # Reconfigurable Intelligent Surface Assisted UAV-MCS Based on Transformer Enhanced Deep Reinforcement Learning

Qianqian Wu , Qiang Liu , Member, IEEE, Ying He , Senior Member, IEEE, and Zefan Wu

Ab...

# 文件: Reliability-Optimal_UAV-Assisted_Mobile_Edge_Computing_Joint_Resource_Allocation_Data_Transmission_Scheduling_and_Motion_Control.md
# 前5行预览:
# # Reliability-Optimal UAV-Assisted Mobile Edge Computing: Joint Resource Allocation, Data Transmission Scheduling and Motion Control

Jianshan Zhou , Mingqian Wang, Daxin Tian , Fellow, IEEE, Kaige Qu...

# 文件: Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md
# 前5行预览:
# # Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks: A Stackelberg Differential Game Approach

Die Wang , Graduate Student Member, IEEE, Yunjian Jia , Member, IEEE, Liang Liang...

# 文件: Resource_Allocation_in_Blockchain_Integration_of_UAV-Enabled_MEC_Networks_A_Stackelberg_Differential_Game_Approach.md
# 前5行预览:
# # Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks: A Stackelberg Differential Game Approach

Die Wang , Graduate Student Member, IEEE, Yunjian Jia , Member, IEEE, Liang Liang...

# 文件: Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md
# 前5行预览:
# . LETTER .

June 2023, Vol. 66 169201:1â169201:2 https://doi.org/10.1007/s11432-020-3257-x

# Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties

# 文件: Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md
# 前5行预览:
# . RESEARCH PAPER .

January 2025, Vol. 68, Iss. 1, 112301:1â112301:15   
https://doi.org/10.1007/s11432-024-4224-6


# 文件: Securing_Autonomous_UAV_Cluster_With_Blockchain-Based_Threshold_Key_Management_System_Utilizing_Crypto-Asset_and_Multisignature.md
# 前5行预览:
# # Securing Autonomous UAV Cluster With Blockchain-Based Threshold Key Management System Utilizing Crypto-Asset and Multisignature

Mebanjop Kharjana , Subhas Chandra Sahana , and Goutam Saha

Abstract...

# 文件: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md
# 前5行预览:
# # Security-Aware Designs of Multi-UAV Deployment, Task Offloading and Service Placement in Edge Computing Networks

Mengru Wu , Haonan Wu, Weidang Lu , Senior Member, IEEE, Lei Guo , Member, IEEE, Ink...

# 文件: Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md
# 前5行预览:
# # Serv-HU: Service Hand-off for UAV-as-a-Service

Arijit Roy , Member, IEEE, Veera Manikantha Rayudu Tummala , and Vinay Yadam

AbstractâIn this work, we propose a UAV Service Hand-off scheme (Serv-...

# 文件: Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md
# 前5行预览:
# # Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing

Geng Sun , Senior Member, IEEE, Yixian Wang, Zemin Sun , Member, IEEE,

Qingqing Wu , Senior Member, IEEE, Jiawen Kang , Se...

# 文件: Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage.md
# 前5行预览:
# # Symmetry-Informed MARL: A Decentralized and Cooperative UAV Swarm Control Approach for Communication Coverage

Rongye Shi , Member, IEEE, Xin Yu , Yandong Wang, Yongkai Tian , Zhenyu Liu , Member, I...

# 文件: TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md
# 前5行预览:
# # TJCCT: A Two-Timescale Approach for UAV-Assisted Mobile Edge Computing

Zemin Sun , Member, IEEE, Geng Sun , Senior Member, IEEE, Qingqing Wu , Senior Member, IEEE, Long He , Shuang Liang , Hongyang...

# 文件: Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md
# 前5行预览:
# # Task Offloading and Resource Pricing Based on Game Theory in UAV-Assisted Edge Computing

Zhuoyue Chen , Yaozong Yang , Jiajie Xu , Ying Chen , Senior Member, IEEE, and Jiwei Huang , Senior Member, ...

# 文件: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md
# 前5行预览:
# # Trajectory Optimization and Power Allocation for Multi-UAV Wireless Networks: A Communication-Based Multi-Agent Deep Reinforcement Learning Approach

Zimeng Yuan , Yuanguo Bi , Member, IEEE, Yanbo F...

# 文件: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md
# 前5行预览:
# # Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-Assisted Wireless Networks

Qichao Xu , Ruidong Li , Senior Member, IEEE, Yihao Qi, Zhou Su , Senior Member, IEEE, and Dong...

# 文件: UAV swarm air combat maneuver decision-making method based on multi-agent reinforcement learning and transferring.md
# 前5行预览:
# . RESEARCH PAPER . Special Topic: UAV Swarm Autonomous Control

August 2024, Vol. 67, Iss. 8, 180204:1â180204:18   
https://doi.org/10.1007/s11432-023-4088-2


# 文件: UAV-Assisted_Communications_in_SAGIN-ISAC_Mobile_User_Tracking_and_Robust_Beamforming.md
# 前5行预览:
# # UAV-Assisted Communications in SAGIN-ISAC: Mobile User Tracking and Robust Beamforming

Weihao Mao , Student Member, IEEE, Yang Lu , Member, IEEE, Gaofeng Pan , Senior Member, IEEE, and Bo Ai , Fell...

# 文件: UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md
# 前5行预览:
# # UAV-Assisted Microservice Mobile Edge Computing Architecture: Addressing Post-Disaster Emergency Medical Rescue

Ji Li , Qiang He , Associate Member, IEEE, Xingwei Wang , Ammar Hawbani , Keping Yu ,...

# 文件: UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach.md
# 前5行预览:
# # UAV Swarm-Enabled Collaborative Post-Disaster Communications in Low Altitude Economy via a Two-Stage Optimization Approach

Xiaoya Zheng , Geng Sun , Senior Member, IEEE, Jiahui Li , Student Member,...

# 文件: User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md
# 前5行预览:
# # User Preference Oriented Service Caching and Task Offloading for UAV-Assisted MEC Networks

Ruiting Zhou , Member, IEEE, Yifeng Huang , Yufeng Wang, Lei Jiao , Member, IEEE, Haisheng Tan , Senior Me...

# 文件: VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md
# 前5行预览:
# # VerDT: A Versatile Digital Twins Framework for UAVs-Based Industrial Cyber-Physical Systems

Longyu Zhou , Member, IEEE, Supeng Leng , Member, IEEE, and Tony Q. S. Quek , Fellow, IEEE

AbstractâWi...

# 文件: Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md
# 前5行预览:
# # Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery

Jia Xu , Member, IEEE, Hao Liu, Xiao Liu , Senior Member, IEEE, Azadeh Ghari Neiat Xuejun Li , Member, IEEE, and Yun Yang ,...

# 文件: Zhou 等 - 2024 - Joint Optimization of Mobility and Reliability-Gua.md
# 前5行预览:
# # Joint Optimization of Mobility and Reliability-Guaranteed Air-to-Ground Communication for UAVs

Jianshan Zhou , Daxin Tian , Senior Member, IEEE, Yaqing Yan, Xuting Duan , and Xuemin Shen , Fellow, ...


echo "=================================================="
echo "Markdown文件重命名完成！共处理 79 个文件"
echo "无法自动处理: 83 个文件"
echo "=================================================="
echo "Markdown文件在: markdown/"
echo "请检查无法处理的文件，手动重命名。"