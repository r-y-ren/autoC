#!/bin/bash
# 直接使用Zotero citation key重命名Markdown文件
# 规则：auth.lower + year + shorttitle(3,3)
#
# 共处理 534 个文献条目
#
set -e  # 遇到错误立即退出

cd /Users/wupengfei/Downloads/my_LLM_valut/raw

echo "开始Markdown文件重命名..."

# alkouz2022InfEneCom
# In-Flight Energy-Driven Composition of Drone Swarm Services
# 相似度: 100.00%
if [ -f "markdown/alkouz2022InfEneCom.md" ]; then
    mv "markdown/alkouz2022InfEneCom.md" "markdown/alkouz2022InfEneCom.md"
    echo "✓ Markdown重命名: alkouz2022InfEneCom.md -> alkouz2022InfEneCom.md"
else
    echo "⚠ Markdown文件不存在: markdown/alkouz2022InfEneCom.md"
fi

# chen2025EneOveCom
# Energy-Efficient over-the-Air Computation in UAV-assisted IIoT
# 相似度: 100.00%
if [ -f "markdown/chen2025EneOveCom.md" ]; then
    mv "markdown/chen2025EneOveCom.md" "markdown/chen2025EneOveCom.md"
    echo "✓ Markdown重命名: chen2025EneOveCom.md -> chen2025EneOveCom.md"
else
    echo "⚠ Markdown文件不存在: markdown/chen2025EneOveCom.md"
fi

# cui2024TheDatVal
# The Data Value Based Asynchronous Federated Learning
# 相似度: 100.00%
if [ -f "markdown/cui2024TheDatVal.md" ]; then
    mv "markdown/cui2024TheDatVal.md" "markdown/cui2024TheDatVal.md"
    echo "✓ Markdown重命名: cui2024TheDatVal.md -> cui2024TheDatVal.md"
else
    echo "⚠ Markdown文件不存在: markdown/cui2024TheDatVal.md"
fi

# gao2025TraLeaFor
# Transfer Learning for Joint Trajectory Control and Task Offloading in Large-Scal...
# 相似度: 100.00%
if [ -f "markdown/gao2025TraLeaFor.md" ]; then
    mv "markdown/gao2025TraLeaFor.md" "markdown/gao2025TraLeaFor.md"
    echo "✓ Markdown重命名: gao2025TraLeaFor.md -> gao2025TraLeaFor.md"
else
    echo "⚠ Markdown文件不存在: markdown/gao2025TraLeaFor.md"
fi

# hao2025RelOptOf
# Reliability-Aware Optimization of Task Offloading for UAV-assisted
# 相似度: 100.00%
if [ -f "markdown/hao2025RelOptOf.md" ]; then
    mv "markdown/hao2025RelOptOf.md" "markdown/hao2025RelOptOf.md"
    echo "✓ Markdown重命名: hao2025RelOptOf.md -> hao2025RelOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/hao2025RelOptOf.md"
fi

# ji2024DecAssWit
# Decoupled Association With Rate Splitting Multiple Access
# 相似度: 100.00%
if [ -f "markdown/ji2024DecAssWit.md" ]; then
    mv "markdown/ji2024DecAssWit.md" "markdown/ji2024DecAssWit.md"
    echo "✓ Markdown重命名: ji2024DecAssWit.md -> ji2024DecAssWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/ji2024DecAssWit.md"
fi

# kang2024AutMulRac
# Autonomous Multi-Drone Racing Method Based on Deep Reinforcement Learning
# 相似度: 100.00%
if [ -f "markdown/kang2024AutMulRac.md" ]; then
    mv "markdown/kang2024AutMulRac.md" "markdown/kang2024AutMulRac.md"
    echo "✓ Markdown重命名: kang2024AutMulRac.md -> kang2024AutMulRac.md"
else
    echo "⚠ Markdown文件不存在: markdown/kang2024AutMulRac.md"
fi

# li2024SecOffWit
# Secure Offloading with Adversarial Multi-Agent Reinforcement Learning against In...
# 相似度: 100.00%
if [ -f "markdown/li2024SecOffWit.md" ]; then
    mv "markdown/li2024SecOffWit.md" "markdown/li2024SecOffWit.md"
    echo "✓ Markdown重命名: li2024SecOffWit.md -> li2024SecOffWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/li2024SecOffWit.md"
fi

# li2025CooNonMul
# Cooperative Non-Orthogonal Multiple Access with Index Modulation for Air-Ground ...
# 相似度: 100.00%
if [ -f "markdown/li2025CooNonMul.md" ]; then
    mv "markdown/li2025CooNonMul.md" "markdown/li2025CooNonMul.md"
    echo "✓ Markdown重命名: li2025CooNonMul.md -> li2025CooNonMul.md"
else
    echo "⚠ Markdown文件不存在: markdown/li2025CooNonMul.md"
fi

# li2025FedMetBas
# Federated Meta-Learning Based Computation Offloading Approach with Energy-Delay ...
# 相似度: 100.00%
if [ -f "markdown/li2025FedMetBas.md" ]; then
    mv "markdown/li2025FedMetBas.md" "markdown/li2025FedMetBas.md"
    echo "✓ Markdown重命名: li2025FedMetBas.md -> li2025FedMetBas.md"
else
    echo "⚠ Markdown文件不存在: markdown/li2025FedMetBas.md"
fi

# liu2025AHybOpt
# A Hybrid Optimization Framework for Age of Information Minimization in UAV-assis...
# 相似度: 100.00%
if [ -f "markdown/liu2025AHybOpt.md" ]; then
    mv "markdown/liu2025AHybOpt.md" "markdown/liu2025AHybOpt.md"
    echo "✓ Markdown重命名: liu2025AHybOpt.md -> liu2025AHybOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/liu2025AHybOpt.md"
fi

# liu2025OnTheRob
# On the Robust Topology Recovery of UAV
# 相似度: 100.00%
if [ -f "markdown/liu2025OnTheRob.md" ]; then
    mv "markdown/liu2025OnTheRob.md" "markdown/liu2025OnTheRob.md"
    echo "✓ Markdown重命名: liu2025OnTheRob.md -> liu2025OnTheRob.md"
else
    echo "⚠ Markdown文件不存在: markdown/liu2025OnTheRob.md"
fi

# nabi2025JoiOffDec
# Joint Offloading Decision, User Association, and Resource Allocation in Hierarch...
# 相似度: 100.00%
if [ -f "markdown/nabi2025JoiOffDec.md" ]; then
    mv "markdown/nabi2025JoiOffDec.md" "markdown/nabi2025JoiOffDec.md"
    echo "✓ Markdown重命名: nabi2025JoiOffDec.md -> nabi2025JoiOffDec.md"
else
    echo "⚠ Markdown文件不存在: markdown/nabi2025JoiOffDec.md"
fi

# ning2025JoiOptOf
# Joint Optimization of Data Acquisition and Trajectory Planning for UAV-assisted
# 相似度: 100.00%
if [ -f "markdown/ning2025JoiOptOf.md" ]; then
    mv "markdown/ning2025JoiOptOf.md" "markdown/ning2025JoiOptOf.md"
    echo "✓ Markdown重命名: ning2025JoiOptOf.md -> ning2025JoiOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/ning2025JoiOptOf.md"
fi

# qian2024APatPla
# A Path Planning Algorithm for a Crop Monitoring Fixed-Wing Unmanned Aerial Syste...
# 相似度: 100.00%
if [ -f "markdown/qian2024APatPla.md" ]; then
    mv "markdown/qian2024APatPla.md" "markdown/qian2024APatPla.md"
    echo "✓ Markdown重命名: qian2024APatPla.md -> qian2024APatPla.md"
else
    echo "⚠ Markdown文件不存在: markdown/qian2024APatPla.md"
fi

# qin2022MulReiLea
# Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Comput...
# 相似度: 100.00%
if [ -f "markdown/qin2022MulReiLea.md" ]; then
    mv "markdown/qin2022MulReiLea.md" "markdown/qin2022MulReiLea.md"
    echo "✓ Markdown重命名: qin2022MulReiLea.md -> qin2022MulReiLea.md"
else
    echo "⚠ Markdown文件不存在: markdown/qin2022MulReiLea.md"
fi

# ren2024IntAdaGos
# Intelligent Adaptive Gossip-Based Broadcast Protocol
# 相似度: 100.00%
if [ -f "markdown/ren2024IntAdaGos.md" ]; then
    mv "markdown/ren2024IntAdaGos.md" "markdown/ren2024IntAdaGos.md"
    echo "✓ Markdown重命名: ren2024IntAdaGos.md -> ren2024IntAdaGos.md"
else
    echo "⚠ Markdown文件不存在: markdown/ren2024IntAdaGos.md"
fi

# rizvi2025MonIntSer
# Monitoring Inter-Drone Service Interference for Resilient Operations
# 相似度: 100.00%
if [ -f "markdown/rizvi2025MonIntSer.md" ]; then
    mv "markdown/rizvi2025MonIntSer.md" "markdown/rizvi2025MonIntSer.md"
    echo "✓ Markdown重命名: rizvi2025MonIntSer.md -> rizvi2025MonIntSer.md"
else
    echo "⚠ Markdown文件不存在: markdown/rizvi2025MonIntSer.md"
fi

# singh2024StaMatBas
# Stable Matching Based Revenue Maximization for Federated Learning in UAV-assiste...
# 相似度: 100.00%
if [ -f "markdown/singh2024StaMatBas.md" ]; then
    mv "markdown/singh2024StaMatBas.md" "markdown/singh2024StaMatBas.md"
    echo "✓ Markdown重命名: singh2024StaMatBas.md -> singh2024StaMatBas.md"
else
    echo "⚠ Markdown文件不存在: markdown/singh2024StaMatBas.md"
fi

# song2024EneTraOpt
# Energy-Efficient Trajectory Optimization with Wireless Charging in UAV-assisted ...
# 相似度: 100.00%
if [ -f "markdown/song2024EneTraOpt.md" ]; then
    mv "markdown/song2024EneTraOpt.md" "markdown/song2024EneTraOpt.md"
    echo "✓ Markdown重命名: song2024EneTraOpt.md -> song2024EneTraOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/song2024EneTraOpt.md"
fi

# xu2025WinSerPro
# Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery
# 相似度: 100.00%
if [ -f "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" ]; then
    mv "markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md" "markdown/xu2025WinSerPro.md"
    echo "✓ Markdown重命名: Wind-Aware Service Provisioning Strategy for Multi-Package D... -> xu2025WinSerPro.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery.md"
fi

# yuan2024DynEveFau
# Dynamic Event-Triggered Fault-Tolerant Cooperative Resilient Tracking Control wi...
# 相似度: 100.00%
if [ -f "markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md" ]; then
    mv "markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md" "markdown/yuan2024DynEveFau.md"
    echo "✓ Markdown重命名: Dynamic event-triggered fault-tolerant cooperative resilient... -> yuan2024DynEveFau.md"
else
    echo "⚠ Markdown文件不存在: markdown/Dynamic event-triggered fault-tolerant cooperative resilient tracking control with prescribed performance for UAVs.md"
fi

# zhan2025OnlEneAnd
# Online Energy and Interference Management for Dynamic Target Tracking with Cellu...
# 相似度: 100.00%
if [ -f "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" ]; then
    mv "markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md" "markdown/zhan2025OnlEneAnd.md"
    echo "✓ Markdown重命名: Online_Energy_and_Interference_Management_for_Dynamic_Target... -> zhan2025OnlEneAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Online_Energy_and_Interference_Management_for_Dynamic_Target_Tracking_With_Cellular-Connected_UAV.md"
fi

# zhang2025OptMonUti
# Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Ef...
# 相似度: 100.00%
if [ -f "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" ]; then
    mv "markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md" "markdown/zhang2025OptMonUti.md"
    echo "✓ Markdown重命名: Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Co... -> zhang2025OptMonUti.md"
else
    echo "⚠ Markdown文件不存在: markdown/Optimizing_Monitoring_Utility_of_Uncrewed_Aerial_Vehicles_Considering_Adverse_Effects.md"
fi

# wang2024BioAntCol
# Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading...
# 相似度: 95.03%
if [ -f "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" ]; then
    mv "markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md" "markdown/wang2024BioAntCol.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Tra... -> wang2024BioAntCol.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC.md"
fi

# zhou2025UsePreOri
# User Preference Oriented Service Caching and Task Offloading for UAV-assisted ME...
# 相似度: 94.59%
if [ -f "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" ]; then
    mv "markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md" "markdown/zhou2025UsePreOri.md"
    echo "✓ Markdown重命名: User_Preference_Oriented_Service_Caching_and_Task_Offloading... -> zhou2025UsePreOri.md"
else
    echo "⚠ Markdown文件不存在: markdown/User_Preference_Oriented_Service_Caching_and_Task_Offloading_for_UAV-Assisted_MEC_Networks.md"
fi

# zhao2025JoiOptOf
# Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-ass...
# 相似度: 94.55%
if [ -f "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md" "markdown/zhao2025JoiOptOf.md"
    echo "✓ Markdown重命名: Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading... -> zhao2025JoiOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhao 等 - 2025 - Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-Assisted MEC.md"
fi

# zhang2024TasOffAnd
# Task Offloading and Trajectory Optimization for Secure Communications in Dynamic...
# 相似度: 94.51%
if [ -f "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" ]; then
    mv "markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md" "markdown/zhang2024TasOffAnd.md"
    echo "✓ Markdown重命名: Zhang 等 - 2024 - Task Offloading and Trajectory Optimization... -> zhang2024TasOffAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhang 等 - 2024 - Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC.md"
fi

# wang2024DecNavWit
# Decentralized Navigation with Heterogeneous Federated Reinforcement Learning for...
# 相似度: 91.71%
if [ -f "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" ]; then
    mv "markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md" "markdown/wang2024DecNavWit.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Decentralized Navigation With Heterogeneous ... -> wang2024DecNavWit.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Decentralized Navigation With Heterogeneous Federated Reinforcement Learning for UAV-Enabled Mobile.md"
fi

# wan2025AMulSca
# A Multimodal Scale Normalization Framework for Vision-Radar Small UAV
# 相似度: 91.60%
if [ -f "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" ]; then
    mv "markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md" "markdown/wan2025AMulSca.md"
    echo "✓ Markdown重命名: A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_... -> wan2025AMulSca.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Multimodal_Scale_Normalization_Framework_for_Vision-Radar_Small_UAV_Positioning.md"
fi

# wang2025SecBeaAnd
# Secure Beamforming and Deployment Design for Rate-Splitting Multiple Access-Base...
# 相似度: 91.36%
if [ -f "markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md" ]; then
    mv "markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md" "markdown/wang2025SecBeaAnd.md"
    echo "✓ Markdown重命名: Secure beamforming and deployment design for rate-splitting ... -> wang2025SecBeaAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Secure beamforming and deployment design for rate-splitting multiple access-based UAV communications.md"
fi

# xu2025BloGamThe
# Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation ...
# 相似度: 91.30%
if [ -f "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025BloGamThe.md"
    echo "✓ Markdown重命名: Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_B... -> xu2025BloGamThe.md"
else
    echo "⚠ Markdown文件不存在: markdown/Blockchain-Empowered_Game_Theoretical_Incentive_for_Secure_Bandwidth_Allocation_in_UAV-Assisted_Wireless_Networks.md"
fi

# chen2025TasOffAnd
# Task Offloading and Resource Pricing Based on Game Theory in UAV-assisted
# 相似度: 90.51%
if [ -f "markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md" ]; then
    mv "markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md" "markdown/chen2025TasOffAnd.md"
    echo "✓ Markdown重命名: Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in... -> chen2025TasOffAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Task_Offloading_and_Resource_Pricing_Based_on_Game_Theory_in_UAV-Assisted_Edge_Computing.md"
fi

# xu2025TruGamInc
# Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-assis...
# 相似度: 90.00%
if [ -f "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" ]; then
    mv "markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md" "markdown/xu2025TruGamInc.md"
    echo "✓ Markdown重命名: Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_L... -> xu2025TruGamInc.md"
else
    echo "⚠ Markdown文件不存在: markdown/Trust-Enhanced_Game_Incentive_for_Secure_Quantum_Federated_Learning_in_UAV-Assisted_Wireless_Networks.md"
fi

# xie2025BloLigCro
# Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV
# 相似度: 89.04%
if [ -f "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" ]; then
    mv "markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md" "markdown/xie2025BloLigCro.md"
    echo "✓ Markdown重命名: Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_... -> xie2025BloLigCro.md"
else
    echo "⚠ Markdown文件不存在: markdown/Blockchain-Assisted_Lightweight_Cross-Domain_Authentication_for_Multi-UAV_Wireless_Networks.md"
fi

# tian2024UavWirCoo
# UAV-Assisted Wireless Cooperative Communication
# 相似度: 88.66%
if [ -f "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" ]; then
    mv "markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md" "markdown/tian2024UavWirCoo.md"
    echo "✓ Markdown重命名: Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communicat... -> tian2024UavWirCoo.md"
else
    echo "⚠ Markdown文件不存在: markdown/Tian 等 - 2024 - UAV-Assisted Wireless Cooperative Communication an.md"
fi

# shen2024SliTasOff
# Slicing-Based Task Offloading
# 相似度: 86.67%
if [ -f "markdown/shen2024SlicingBasedTaskOffloading.md" ]; then
    mv "markdown/shen2024SlicingBasedTaskOffloading.md" "markdown/shen2024SliTasOff.md"
    echo "✓ Markdown重命名: shen2024SlicingBasedTaskOffloading.md -> shen2024SliTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/shen2024SlicingBasedTaskOffloading.md"
fi

# wang2025JoiOptOf
# Joint Optimization of Beamforming and Trajectory for UAV-RIS-assisted MU-MISO
# 相似度: 86.27%
if [ -f "markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md" ]; then
    mv "markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md" "markdown/wang2025JoiOptOf.md"
    echo "✓ Markdown重命名: Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS... -> wang2025JoiOptOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint_Optimization_of_Beamforming_and_Trajectory_for_UAV-RIS-Assisted_MU-MISO_Systems_Using_GNN_and_SD3.md"
fi

# wang2025JoiTasOff
# Joint Task Offloading and Migration Optimization in UAV-enabled
# 相似度: 85.94%
if [ -f "markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md" ]; then
    mv "markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md" "markdown/wang2025JoiTasOff.md"
    echo "✓ Markdown重命名: Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enab... -> wang2025JoiTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint_Task_Offloading_and_Migration_Optimization_in_UAV-Enabled_Dynamic_MEC_Networks.md"
fi

# zhu2024FisSpeClu
# Fission Spectral Clustering Strategy for UAV
# 相似度: 85.71%
if [ -f "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" ]; then
    mv "markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md" "markdown/zhu2024FisSpeClu.md"
    echo "✓ Markdown重命名: Fission Spectral Clustering Strategy for UAV Swarm Networks.... -> zhu2024FisSpeClu.md"
else
    echo "⚠ Markdown文件不存在: markdown/Fission Spectral Clustering Strategy for UAV Swarm Networks.md"
fi

# jin2025AResCon
# A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV
# 相似度: 85.50%
if [ -f "markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md" ]; then
    mv "markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md" "markdown/jin2025AResCon.md"
    echo "✓ Markdown重命名: A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scal... -> jin2025AResCon.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Resource-Efficient_Content_Sharing_Mechanism_in_Large-Scale_UAV_Named_Data_Networking.md"
fi

# alam2024JoiTraCon
# Joint Trajectory Control, Frequency Allocation, and Routing for UAV
# 相似度: 85.00%
if [ -f "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" ]; then
    mv "markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md" "markdown/alam2024JoiTraCon.md"
    echo "✓ Markdown重命名: Alam和Moh - 2024 - Joint Trajectory Control, Frequency Alloca... -> alam2024JoiTraCon.md"
else
    echo "⚠ Markdown文件不存在: markdown/Alam和Moh - 2024 - Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks A Multi-Agent De.md"
fi

# amodu2023AgeOfInf
# Age of Information
# 相似度: 85.00%
if [ -f "markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md" ]; then
    mv "markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md" "markdown/amodu2023AgeOfInf.md"
    echo "✓ Markdown重命名: Zhan 等 - 2024 - Tradeoff Between Age of Information and Oper... -> amodu2023AgeOfInf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhan 等 - 2024 - Tradeoff Between Age of Information and Operation .md"
fi

# bai2024DelCooTas
# Delay-Aware Cooperative Task Offloading
# 相似度: 85.00%
if [ -f "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" ]; then
    mv "markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md" "markdown/bai2024DelCooTas.md"
    echo "✓ Markdown重命名: Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for M... -> bai2024DelCooTas.md"
else
    echo "⚠ Markdown文件不存在: markdown/Bai 等 - 2022 - Delay-Aware Cooperative Task Offloading for Multi-.md"
fi

# chang2024NeaUav
# Near-Optimal UAV
# 相似度: 85.00%
if [ -f "markdown/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md" ]; then
    mv "markdown/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md" "markdown/chang2024NeaUav.md"
    echo "✓ Markdown重命名: Near-Optimal UAV Deployment for Delay-Bounded Data Collectio... -> chang2024NeaUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks.md"
fi

# chen2024AdaBitVid
# Adaptive Bitrate Video Caching
# 相似度: 85.00%
if [ -f "markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md" ]; then
    mv "markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md" "markdown/chen2024AdaBitVid.md"
    echo "✓ Markdown重命名: Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assist... -> chen2024AdaBitVid.md"
else
    echo "⚠ Markdown文件不存在: markdown/Chen 等 - 2024 - Adaptive Bitrate Video Caching in UAV-Assisted MEC.md"
fi

# chen2025MulTasOff
# Multi-User Task Offloading in UAV-assisted LEO
# 相似度: 85.00%
if [ -f "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" ]; then
    mv "markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md" "markdown/chen2025MulTasOff.md"
    echo "✓ Markdown重命名: Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted L... -> chen2025MulTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/Chen 等 - 2025 - Multi-User Task Offloading in UAV-Assisted LEO Satellite Edge Computing A Game-Theoretic Approach.md"
fi

# chen2025Typ
# TypeFly
# 相似度: 85.00%
if [ -f "markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md" ]; then
    mv "markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md" "markdown/chen2025Typ.md"
    echo "✓ Markdown重命名: Chen-2025-TypeFly_ Low-Latency Drone Planning.md -> chen2025Typ.md"
else
    echo "⚠ Markdown文件不存在: markdown/Chen-2025-TypeFly_ Low-Latency Drone Planning.md"
fi

# cheng2023Ai
# AI
# 相似度: 85.00%
if [ -f "markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md" ]; then
    mv "markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md" "markdown/cheng2023Ai.md"
    echo "✓ Markdown重命名: Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edg... -> cheng2023Ai.md"
else
    echo "⚠ Markdown文件不存在: markdown/Dai 等 - 2024 - UAV-Assisted Task Offloading in Vehicular Edge Com.md"
fi

# cong2024Par
# ParallEdge
# 相似度: 85.00%
if [ -f "markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md" ]; then
    mv "markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md" "markdown/cong2024Par.md"
    echo "✓ Markdown重命名: Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Par... -> cong2024Par.md"
else
    echo "⚠ Markdown文件不存在: markdown/Cong 等 - 2024 - ParallEdge Exploiting Computing-Mobility Parallel.md"
fi

# dai2022Ros
# ROSE
# 相似度: 85.00%
if [ -f "markdown/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md" ]; then
    mv "markdown/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md" "markdown/dai2022Ros.md"
    echo "✓ Markdown重命名: UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture... -> dai2022Ros.md"
else
    echo "⚠ Markdown文件不存在: markdown/UAV-Assisted_Microservice_Mobile_Edge_Computing_Architecture_Addressing_Post-Disaster_Emergency_Medical_Rescue.md"
fi

# dai2023MulDeeRei
# Multi-Agent Deep Reinforcement Learning
# 相似度: 85.00%
if [ -f "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" ]; then
    mv "markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md" "markdown/dai2023MulDeeRei.md"
    echo "✓ Markdown重命名: Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Base... -> dai2023MulDeeRei.md"
else
    echo "⚠ Markdown文件不存在: markdown/Ning 等 - 2024 - Multi-Agent Deep Reinforcement Learning Based UAV .md"
fi

# gao2024SerExpOri
# Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs
# 相似度: 85.00%
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md" "markdown/gao2024SerExpOri.md"
    echo "✓ Markdown重命名: IEEE Transactions on Mobile Computing - 2024 - Service Exper... -> gao2024SerExpOri.md"
else
    echo "⚠ Markdown文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks.md"
fi

# gao2025Csm
# CSMAAC
# 相似度: 85.00%
if [ -f "markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md" ]; then
    mv "markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md" "markdown/gao2025Csm.md"
    echo "✓ Markdown重命名: Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md -> gao2025Csm.md"
else
    echo "⚠ Markdown文件不存在: markdown/Gao-2025-CSMAAC_ Multi-Agent Reinforcement Lea.md"
fi

# gaydamaka2024DynTopOrg
# Dynamic Topology Organization
# 相似度: 85.00%
if [ -f "markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md" ]; then
    mv "markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md" "markdown/gaydamaka2024DynTopOrg.md"
    echo "✓ Markdown重命名: Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maint... -> gaydamaka2024DynTopOrg.md"
else
    echo "⚠ Markdown文件不存在: markdown/Gaydamaka 等 - 2024 - Dynamic Topology Organization and Maintenance Algo.md"
fi

# gong2024Ene3dUav
# Energy-Efficient 3-D UAV
# 相似度: 85.00%
if [ -f "markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md" ]; then
    mv "markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md" "markdown/gong2024Ene3dUav.md"
    echo "✓ Markdown重命名: Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessi... -> gong2024Ene3dUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Gong 等 - 2024 - Energy-Efficient 3-D UAV Ground Node Accessing Using the Minimum Number of UAVs.md"
fi

# gui2024CovProAnd
# Coverage Probability and Throughput Optimization in Integrated mmWave
# 相似度: 85.00%
if [ -f "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" ]; then
    mv "markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md" "markdown/gui2024CovProAnd.md"
    echo "✓ Markdown重命名: Gui和Cai - 2024 - Coverage Probability and Throughput Optimiz... -> gui2024CovProAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/Gui和Cai - 2024 - Coverage Probability and Throughput Optimization in Integrated mmWave and Sub-6 GHz Multi-UAV-Assist.md"
fi

# guo2021UavTra
# UAV Trajectory
# 相似度: 85.00%
if [ -f "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" ]; then
    mv "markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md" "markdown/guo2021UavTra.md"
    echo "✓ Markdown重命名: Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement... -> guo2021UavTra.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhou 等 - 2024 - Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV Trajectory Design and User Sc.md"
fi

# guo2024JoiOpt
# Joint Optimization
# 相似度: 85.00%
if [ -f "markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md" ]; then
    mv "markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md" "markdown/guo2024JoiOpt.md"
    echo "✓ Markdown重命名: Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming ... -> guo2024JoiOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Guo 等 - 2024 - Joint Optimization of Trajectory and Jamming Power.md"
fi

# hajihoseini gazestani2022ResAll
# Resource Allocation
# 相似度: 85.00%
if [ -f "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" ]; then
    mv "markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md" "markdown/hajihoseini gazestani2022ResAll.md"
    echo "✓ Markdown重命名: Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignme... -> hajihoseini gazestani2022ResAll.md"
else
    echo "⚠ Markdown文件不存在: markdown/Liu 等 - 2025 - Resource Allocation for Adaptive Beam Alignment in UAV-Assisted Integrated Sensing and Communication.md"
fi

# han2024ColRouPla
# Collaborative Route Planning of UAVs
# 相似度: 85.00%
if [ -f "markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md" ]; then
    mv "markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md" "markdown/han2024ColRouPla.md"
    echo "✓ Markdown重命名: Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers... -> han2024ColRouPla.md"
else
    echo "⚠ Markdown文件不存在: markdown/Han 等 - 2024 - Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response.md"
fi

# hao2024JoiTasOff
# Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV
# 相似度: 85.00%
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md" "markdown/hao2024JoiTasOff.md"
    echo "✓ Markdown重命名: IEEE Transactions on Mobile Computing - 2024 - Joint Task Of... -> hao2024JoiTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Com.md"
fi

# he2024BalTotEne
# Balancing Total Energy Consumption
# 相似度: 85.00%
if [ -f "markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md" ]; then
    mv "markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md" "markdown/he2024BalTotEne.md"
    echo "✓ Markdown重命名: He 等 - 2024 - Balancing Total Energy Consumption and Mean Ma... -> he2024BalTotEne.md"
else
    echo "⚠ Markdown文件不存在: markdown/He 等 - 2024 - Balancing Total Energy Consumption and Mean Makesp.md"
fi

# hoang2024FinBloLen
# Finite Block Length NOMA MU
# 相似度: 85.00%
if [ -f "markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md" ]; then
    mv "markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md" "markdown/hoang2024FinBloLen.md"
    echo "✓ Markdown重命名: Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Ena... -> hoang2024FinBloLen.md"
else
    echo "⚠ Markdown文件不存在: markdown/Hoang 等 - 2024 - Finite Block Length NOMA MU Pairing UAV-Enable System Performance Analysis and Optimization.md"
fi

# hoang2025Ada3d
# Adaptive 3D
# 相似度: 85.00%
if [ -f "markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md" ]; then
    mv "markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md" "markdown/hoang2025Ada3d.md"
    echo "✓ Markdown重命名: An adaptive 3D reconstruction method for asymmetric dual-ang... -> hoang2025Ada3d.md"
else
    echo "⚠ Markdown文件不存在: markdown/An adaptive 3D reconstruction method for asymmetric dual-angle multispectral stereo imaging system on UAV platform.md"
fi

# huang2024DynTasOff
# Dynamic Task Offloading for Multi-UAVs
# 相似度: 85.00%
if [ -f "markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md" ]; then
    mv "markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md" "markdown/huang2024DynTasOff.md"
    echo "✓ Markdown重命名: Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in V... -> huang2024DynTasOff.md"
else
    echo "⚠ Markdown文件不存在: markdown/Huang 等 - 2024 - Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing With Delay Guarantees A Consensu.md"
fi

# huang2025Ass
# ASSUME
# 相似度: 85.00%
if [ -f "markdown/ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md" ]; then
    mv "markdown/ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md" "markdown/huang2025Ass.md"
    echo "✓ Markdown重命名: ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitu... -> huang2025Ass.md"
else
    echo "⚠ Markdown文件不存在: markdown/ASSUME_An_Optimal_Algorithm_to_Minimize_UAV_Energy_by_Altitude_and_Speed_Scheduling.md"
fi

# karmakar2024ABloDis
# A Blockchain-Based Distributed
# 相似度: 85.00%
if [ -f "markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md" ]; then
    mv "markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md" "markdown/karmakar2024ABloDis.md"
    echo "✓ Markdown重命名: Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intel... -> karmakar2024ABloDis.md"
else
    echo "⚠ Markdown文件不存在: markdown/Karmakar 等 - 2024 - A Blockchain-Based Distributed and Intelligent Clu.md"
fi

# karmakar2024ANovFed
# A Novel Federated Learning-Based Smart Power
# 相似度: 85.00%
if [ -f "markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md" ]; then
    mv "markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md" "markdown/karmakar2024ANovFed.md"
    echo "✓ Markdown重命名: Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart P... -> karmakar2024ANovFed.md"
else
    echo "⚠ Markdown文件不存在: markdown/Karmakar 等 - 2024 - A Novel Federated Learning-Based Smart Power and 3.md"
fi

# khochare2024ImpAlg
# Improved Algorithms
# 相似度: 85.00%
if [ -f "markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md" ]; then
    mv "markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md" "markdown/khochare2024ImpAlg.md"
    echo "✓ Markdown重命名: Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of... -> khochare2024ImpAlg.md"
else
    echo "⚠ Markdown文件不存在: markdown/Khochare 等 - 2024 - Improved Algorithms for Co-Scheduling of Edge Anal.md"
fi

# kumar2025DroIrs
# Drone-Assisted IRS
# 相似度: 85.00%
if [ -f "markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md" ]; then
    mv "markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md" "markdown/kumar2025DroIrs.md"
    echo "✓ Markdown重命名: Kumar-2025-Drone-Assisted IRS System in 5G and.md -> kumar2025DroIrs.md"
else
    echo "⚠ Markdown文件不存在: markdown/Kumar-2025-Drone-Assisted IRS System in 5G and.md"
fi

# li2024Cod
# CoDetect
# 相似度: 85.00%
if [ -f "markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md" ]; then
    mv "markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md" "markdown/li2024Cod.md"
    echo "✓ Markdown重命名: CoDetect cooperative anomaly detection with privacy protecti... -> li2024Cod.md"
else
    echo "⚠ Markdown文件不存在: markdown/CoDetect cooperative anomaly detection with privacy protection towards UAV swarm.md"
fi

# li2024MulOpt
# Multi-Objective Optimization
# 相似度: 85.00%
if [ -f "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" ]; then
    mv "markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md" "markdown/li2024MulOpt.md"
    echo "✓ Markdown重命名: Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Ass... -> li2024MulOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Li 等 - 2024 - Multi-Objective Optimization for UAV Swarm-Assiste.md"
fi

# li2025Dro
# DroneMA
# 相似度: 85.00%
if [ -f "markdown/DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md" ]; then
    mv "markdown/DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md" "markdown/li2025Dro.md"
    echo "✓ Markdown重命名: DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofin... -> li2025Dro.md"
else
    echo "⚠ Markdown文件不存在: markdown/DroneMA_Drone_Mobility_Alignment_Countering_AI-Based_Spoofing_Attacks.md"
fi

# liu2024Uav
# UAV-enabled
# 相似度: 85.00%
if [ -f "markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md" ]; then
    mv "markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md" "markdown/liu2024Uav.md"
    echo "✓ Markdown重命名: Joint_Association_Deployment_and_Flight_Trajectory_Optimizat... -> liu2024Uav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing.md"
fi

# mittal2024DepCosUav
# Deployment Cost-Aware UAV
# 相似度: 85.00%
if [ -f "markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md" ]; then
    mv "markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md" "markdown/mittal2024DepCosUav.md"
    echo "✓ Markdown重命名: Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collabora... -> mittal2024DepCosUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Mittal 等 - 2024 - Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks.md"
fi

# nguyen2024OnTheDil
# On the Dilemma
# 相似度: 85.00%
if [ -f "markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md" ]; then
    mv "markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md" "markdown/nguyen2024OnTheDil.md"
    echo "✓ Markdown重命名: Nguyen 等 - 2024 - On the Dilemma of Reliability or Security ... -> nguyen2024OnTheDil.md"
else
    echo "⚠ Markdown文件不存在: markdown/Nguyen 等 - 2024 - On the Dilemma of Reliability or Security in Unman.md"
fi

# panahi2024RelAndEne
# Reliable and Energy-Efficient UAV Communications
# 相似度: 85.00%
if [ -f "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" ]; then
    mv "markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md" "markdown/panahi2024RelAndEne.md"
    echo "✓ Markdown重命名: Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV C... -> panahi2024RelAndEne.md"
else
    echo "⚠ Markdown文件不存在: markdown/Panahi 和 Panahi - 2024 - Reliable and Energy-Efficient UAV Communications .md"
fi

# qiu2024IntHos
# Integrated Host-
# 相似度: 85.00%
if [ -f "markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md" ]; then
    mv "markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md" "markdown/qiu2024IntHos.md"
    echo "✓ Markdown重命名: Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing ... -> qiu2024IntHos.md"
else
    echo "⚠ Markdown文件不存在: markdown/Qiu 等 - 2024 - Integrated Host- and Content-Centric Routing for E.md"
fi

# ren2025Aer
# AeroEcho
# 相似度: 85.00%
if [ -f "markdown/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md" ]; then
    mv "markdown/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md" "markdown/ren2025Aer.md"
    echo "✓ Markdown重命名: AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatte... -> ren2025Aer.md"
else
    echo "⚠ Markdown文件不存在: markdown/AeroEcho_Towards_Agricultural_Low-power_Wide-area_Backscatter_with_Aerial_Excitation_Source.md"
fi

# roy2025Ser
# Serv-HU
# 相似度: 85.00%
if [ -f "markdown/Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md" ]; then
    mv "markdown/Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md" "markdown/roy2025Ser.md"
    echo "✓ Markdown重命名: Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md -> roy2025Ser.md"
else
    echo "⚠ Markdown文件不存在: markdown/Serv-HU_Service_Hand-off_for_UAV-as-a-Service.md"
fi

# shi2024ATwoStr
# A Two-Stage Strategy
# 相似度: 85.00%
if [ -f "markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md" ]; then
    mv "markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md" "markdown/shi2024ATwoStr.md"
    echo "✓ Markdown重命名: Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless... -> shi2024ATwoStr.md"
else
    echo "⚠ Markdown文件不存在: markdown/Shi 等 - 2023 - A Two-Stage Strategy for UAV-enabled Wireless Powe.md"
fi

# song2024Aoi
# AoI
# 相似度: 85.00%
if [ -f "markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md" ]; then
    mv "markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md" "markdown/song2024Aoi.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobi... -> song2024Aoi.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Ensuring Threshold AoI for UAV-Assisted Mobile Cro.md"
fi

# song2024MetToAss
# Methods to Assign UAVs
# 相似度: 85.00%
if [ -f "markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md" ]; then
    mv "markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md" "markdown/song2024MetToAss.md"
    echo "✓ Markdown重命名: Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Re... -> song2024MetToAss.md"
else
    echo "⚠ Markdown文件不存在: markdown/Song 等 - 2024 - Methods to Assign UAVs for K-Coverage and Rechargi.md"
fi

# sun2024AllAutCom
# All-Sky Autonomous Computing in UAV
# 相似度: 85.00%
if [ -f "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" ]; then
    mv "markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md" "markdown/sun2024AllAutCom.md"
    echo "✓ Markdown重命名: IEEE Transactions on Mobile Computing - 2024 - All-Sky Auton... -> sun2024AllAutCom.md"
else
    echo "⚠ Markdown文件不存在: markdown/IEEE Transactions on Mobile Computing - 2024 - All-Sky Autonomous Computing in UAV Swarm.md"
fi

# sun2024MulOptFor
# Multi-Objective Optimization for Multi-UAV-assisted
# 相似度: 85.00%
if [ -f "markdown/Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md" ]; then
    mv "markdown/Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md" "markdown/sun2024MulOptFor.md"
    echo "✓ Markdown重命名: Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-As... -> sun2024MulOptFor.md"
else
    echo "⚠ Markdown文件不存在: markdown/Sun 等 - 2024 - Multi-Objective Optimization for Multi-UAV-Assisted Mobile Edge Computing.md"
fi

# sun2025Tjc
# TJCCT
# 相似度: 85.00%
if [ -f "markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md" ]; then
    mv "markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md" "markdown/sun2025Tjc.md"
    echo "✓ Markdown重命名: TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_... -> sun2025Tjc.md"
else
    echo "⚠ Markdown文件不存在: markdown/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing.md"
fi

# tao2024MulCooFor
# Multi-Agent Cooperation for Computing Power Scheduling in UAVs
# 相似度: 85.00%
if [ -f "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" ]; then
    mv "markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md" "markdown/tao2024MulCooFor.md"
    echo "✓ Markdown重命名: Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power S... -> tao2024MulCooFor.md"
else
    echo "⚠ Markdown文件不存在: markdown/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems.md"
fi

# thibbotuwawa2019EneCon
# Energy Consumption
# 相似度: 85.00%
if [ -f "markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md" ]; then
    mv "markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md" "markdown/thibbotuwawa2019EneCon.md"
    echo "✓ Markdown重命名: Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV ... -> thibbotuwawa2019EneCon.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wu 等 - 2024 - MAC Optimization Protocol for Cooperative UAV Based on Dual Perception of Energy Consumption and Cha.md"
fi

# tlili2023ANewHyb
# A New Hybrid Adaptive Deep Learning-Based Framework for UAVs
# 相似度: 85.00%
if [ -f "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" ]; then
    mv "markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md" "markdown/tlili2023ANewHyb.md"
    echo "✓ Markdown重命名: A New Hybrid Adaptive Deep Learning-Based Framework for UAVs... -> tlili2023ANewHyb.md"
else
    echo "⚠ Markdown文件不存在: markdown/A New Hybrid Adaptive Deep Learning-Based Framework for UAVs Faults and Attacks Detection.md"
fi

# tong2023EneUav
# Energy-Efficient UAV-NOMA
# 相似度: 85.00%
if [ -f "markdown/Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md" ]; then
    mv "markdown/Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md" "markdown/tong2023EneUav.md"
    echo "✓ Markdown重命名: Energy-efficient UAV-NOMA aided wireless coverage with massi... -> tong2023EneUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Energy-efficient UAV-NOMA aided wireless coverage with massive connections.md"
fi

# wang2024Lsp
# LSPSS
# 相似度: 85.00%
if [ -f "markdown/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md" ]; then
    mv "markdown/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md" "markdown/wang2024Lsp.md"
    echo "✓ Markdown重命名: LSPSS Constructing Lightweight and Secure Scheme for Private... -> wang2024Lsp.md"
else
    echo "⚠ Markdown文件不存在: markdown/LSPSS Constructing Lightweight and Secure Scheme for Private Data Storage and Sharing in Aerial Computing.md"
fi

# wang2024ResAllIn
# Resource Allocation in Blockchain Integration of UAV-enabled MEC
# 相似度: 85.00%
if [ -f "markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md" ]; then
    mv "markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md" "markdown/wang2024ResAllIn.md"
    echo "✓ Markdown重命名: Resource Allocation in Blockchain Integration of UAV-Enabled... -> wang2024ResAllIn.md"
else
    echo "⚠ Markdown文件不存在: markdown/Resource Allocation in Blockchain Integration of UAV-Enabled MEC Networks A Stackelberg Differential Game Approach.md"
fi

# wang2024WirPowMet
# Wireless Powered Metaverse
# 相似度: 85.00%
if [ -f "markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md" ]; then
    mv "markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md" "markdown/wang2024WirPowMet.md"
    echo "✓ Markdown重命名: Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Schedu... -> wang2024WirPowMet.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang 等 - 2024 - Wireless Powered Metaverse Joint Task Scheduling .md"
fi

# wang2025PraOptUav
# Practical Optimizing UAV
# 相似度: 85.00%
if [ -f "markdown/Wang-2025-Practical Optimizing UAV Trajectory.md" ]; then
    mv "markdown/Wang-2025-Practical Optimizing UAV Trajectory.md" "markdown/wang2025PraOptUav.md"
    echo "✓ Markdown重命名: Wang-2025-Practical Optimizing UAV Trajectory.md -> wang2025PraOptUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang-2025-Practical Optimizing UAV Trajectory.md"
fi

# wei2024HieNetSli
# Hierarchical Network Slicing for UAV-assisted
# 相似度: 85.00%
if [ -f "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" ]; then
    mv "markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md" "markdown/wei2024HieNetSli.md"
    echo "✓ Markdown重命名: Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted... -> wei2024HieNetSli.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization.md"
fi

# wu2020TraOpt
# Trajectory Optimization
# 相似度: 85.00%
if [ -f "markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md" ]; then
    mv "markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md" "markdown/wu2020TraOpt.md"
    echo "✓ Markdown重命名: Robust transition trajectory optimization for tail-sitter UA... -> wu2020TraOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Robust transition trajectory optimization for tail-sitter UAVs considering uncertainties.md"
fi

# wu2024BeaPreBas
# Beamforming Prediction Based on the Multireward DQN
# 相似度: 85.00%
if [ -f "markdown/Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md" ]; then
    mv "markdown/Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md" "markdown/wu2024BeaPreBas.md"
    echo "✓ Markdown重命名: Beamforming prediction based on the multireward DQN framewor... -> wu2024BeaPreBas.md"
else
    echo "⚠ Markdown文件不存在: markdown/Beamforming prediction based on the multireward DQN framework for UAV-RIS-assisted THz communication systems.md"
fi

# wu2025TwoDeeEne
# Two-Stage Deep Energy Optimization in IRS-assisted UAV-based
# 相似度: 85.00%
if [ -f "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" ]; then
    mv "markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md" "markdown/wu2025TwoDeeEne.md"
    echo "✓ Markdown重命名: Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assi... -> wu2025TwoDeeEne.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wu 等 - 2025 - Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems.md"
fi

# xu2023TamEveCam
# Taming Event Cameras
# 相似度: 85.00%
if [ -f "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" ]; then
    mv "markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md" "markdown/xu2023TamEveCam.md"
    echo "✓ Markdown重命名: Li-2025-Taming Event Cameras With Bio-Inspired.md -> xu2023TamEveCam.md"
else
    echo "⚠ Markdown文件不存在: markdown/Li-2025-Taming Event Cameras With Bio-Inspired.md"
fi

# xu2024RewMax
# Reward Maximization
# 相似度: 85.00%
if [ -f "markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md" ]; then
    mv "markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md" "markdown/xu2024RewMax.md"
    echo "✓ Markdown重命名: Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitori... -> xu2024RewMax.md"
else
    echo "⚠ Markdown文件不存在: markdown/Xu 等 - 2024 - Reward Maximization for Disaster Zone Monitoring W.md"
fi

# xu2024SemUav
# Semantic-Aware UAV
# 相似度: 85.00%
if [ -f "markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md" ]; then
    mv "markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md" "markdown/xu2024SemUav.md"
    echo "✓ Markdown重命名: Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the M... -> xu2024SemUav.md"
else
    echo "⚠ Markdown文件不存在: markdown/Xu 等 - 2024 - Semantic-Aware UAV Swarm Coordination in the Metaverse A Reputation-Based Incentive Mechanism.md"
fi

# xue2024TowMaxCov
# Towards Maximizing Coverage of Targets for WRSNs
# 相似度: 85.00%
if [ -f "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" ]; then
    mv "markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md" "markdown/xue2024TowMaxCov.md"
    echo "✓ Markdown重命名: Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WR... -> xue2024TowMaxCov.md"
else
    echo "⚠ Markdown文件不存在: markdown/Xue 等 - 2024 - Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling.md"
fi

# yang2024EneEffTra
# Energy Efficient Transmission Strategy
# 相似度: 85.00%
if [ -f "markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md" ]; then
    mv "markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md" "markdown/yang2024EneEffTra.md"
    echo "✓ Markdown重命名: Yang 等 - 2024 - Energy Efficient Transmission Strategy for M... -> yang2024EneEffTra.md"
else
    echo "⚠ Markdown文件不存在: markdown/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile .md"
fi

# zema20243dTraOpt
# 3D Trajectory Optimization
# 相似度: 85.00%
if [ -f "markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md" ]; then
    mv "markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md" "markdown/zema20243dTraOpt.md"
    echo "✓ Markdown重命名: Zema 等 - 2024 - 3D Trajectory Optimization for Multimission ... -> zema20243dTraOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i.md"
fi

# zeng2024A3d
# A3D
# 相似度: 85.00%
if [ -f "markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md" ]; then
    mv "markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md" "markdown/zeng2024A3d.md"
    echo "✓ Markdown重命名: Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navig... -> zeng2024A3d.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zeng 等 - 2024 - A3D Adaptive, Accurate, and Autonomous Navigation.md"
fi

# zhan2024IntOnlOpt
# Interference-Aware Online Optimization for Cellular-Connected Multiple UAV
# 相似度: 85.00%
if [ -f "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" ]; then
    mv "markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md" "markdown/zhan2024IntOnlOpt.md"
    echo "✓ Markdown重命名: Zhan 等 - 2024 - Interference-Aware Online Optimization for C... -> zhan2024IntOnlOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhan 等 - 2024 - Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks With Energy Cons.md"
fi

# zhang2023JoiTasSch
# Joint Task Scheduling and Multi-UAV
# 相似度: 85.00%
if [ -f "markdown/Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md" ]; then
    mv "markdown/Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md" "markdown/zhang2023JoiTasSch.md"
    echo "✓ Markdown重命名: Joint task scheduling and multi-UAV deployment for aerial co... -> zhang2023JoiTasSch.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint task scheduling and multi-UAV deployment for aerial computing in emergency communication networks.md"
fi

# zhao2024OnDesMul
# On Designing Multi-UAV
# 相似度: 85.00%
if [ -f "markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md" ]; then
    mv "markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md" "markdown/zhao2024OnDesMul.md"
    echo "✓ Markdown重命名: Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powere... -> zhao2024OnDesMul.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhao 等 - 2024 - On Designing Multi-UAV Aided Wireless Powered Dynamic Communication via Hierarchical Deep Reinforcem.md"
fi

# zhao2025JoiConCac
# Joint Content Caching, Service Placement, and Task Offloading in UAV-enabled
# 相似度: 85.00%
if [ -f "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" ]; then
    mv "markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md" "markdown/zhao2025JoiConCac.md"
    echo "✓ Markdown重命名: Zhao 等 - 2025 - Joint Content Caching, Service Placement, an... -> zhao2025JoiConCac.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhao 等 - 2025 - Joint Content Caching, Service Placement, and Task Offloading in UAV-Enabled Mobile Edge Computing N.md"
fi

# zheng2024ConDelPer
# Content Delivery Performance Analysis
# 相似度: 85.00%
if [ -f "markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md" ]; then
    mv "markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md" "markdown/zheng2024ConDelPer.md"
    echo "✓ Markdown重命名: Zheng 等 - 2024 - Content Delivery Performance Analysis of a ... -> zheng2024ConDelPer.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zheng 等 - 2024 - Content Delivery Performance Analysis of a Cache-E.md"
fi

# zhou2024AFedDig
# A Federated Digital Twin Framework
# 相似度: 85.00%
if [ -f "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" ]; then
    mv "markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md" "markdown/zhou2024AFedDig.md"
    echo "✓ Markdown重命名: Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-... -> zhou2024AFedDig.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhou 等 - 2024 - A Federated Digital Twin Framework for UAVs-Based .md"
fi

# zhou2025Had
# HaDT
# 相似度: 85.00%
if [ -f "markdown/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md" ]; then
    mv "markdown/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md" "markdown/zhou2025Had.md"
    echo "✓ Markdown重命名: HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logis... -> zhou2025Had.md"
else
    echo "⚠ Markdown文件不存在: markdown/HaDT_Hardening_Digital_Twins_for_UAVs-Based_Industrial_Logistics_Distribution_Systems.md"
fi

# zhou2025Llm
# LLM-QL
# 相似度: 85.00%
if [ -f "markdown/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md" ]; then
    mv "markdown/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md" "markdown/zhou2025Llm.md"
    echo "✓ Markdown重命名: LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Mul... -> zhou2025Llm.md"
else
    echo "⚠ Markdown文件不存在: markdown/LLM-QL_A_LLM-Enhanced_Q-Learning_Approach_for_Scheduling_Multiple_Parallel_Drones.md"
fi

# zhou2025Ver
# VerDT
# 相似度: 85.00%
if [ -f "markdown/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md" ]; then
    mv "markdown/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md" "markdown/zhou2025Ver.md"
    echo "✓ Markdown重命名: VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Ind... -> zhou2025Ver.md"
else
    echo "⚠ Markdown文件不存在: markdown/VerDT_A_Versatile_Digital_Twins_Framework_for_UAVs-Based_Industrial_Cyber-Physical_Systems.md"
fi

# zhu2023AttConOf
# Attitude Control of a Novel Tilt-Wing UAV
# 相似度: 85.00%
if [ -f "markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md" ]; then
    mv "markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md" "markdown/zhu2023AttConOf.md"
    echo "✓ Markdown重命名: Attitude control of a novel tilt-wing UAV in hovering flight... -> zhu2023AttConOf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Attitude control of a novel tilt-wing UAV in hovering flight..md"
fi

# zhu2024ColReiLea
# Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV
# 相似度: 85.00%
if [ -f "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" ]; then
    mv "markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md" "markdown/zhu2024ColReiLea.md"
    echo "✓ Markdown重命名: Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Un... -> zhu2024ColReiLea.md"
else
    echo "⚠ Markdown文件不存在: markdown/Zhu 等 - 2024 - Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV) Trajectory Design for 3D UA.md"
fi

# zeng2025AJoiSec
# A Joint Secure Mechanism of Multi-Task Learning for a UAV
# 相似度: 83.19%
if [ -f "markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md" ]; then
    mv "markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md" "markdown/zeng2025AJoiSec.md"
    echo "✓ Markdown重命名: A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Te... -> zeng2025AJoiSec.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Joint_Secure_Mechanism_of_Multi-Task_Learning_for_a_UAV_Team_Under_FDI_Attacks.md"
fi

# xu2024AHolAnd
# A Holistic and Hybrid Service Selection Strategy for MEC-based UAV
# 相似度: 82.96%
if [ -f "markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md" ]; then
    mv "markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md" "markdown/xu2024AHolAnd.md"
    echo "✓ Markdown重命名: A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Bas... -> xu2024AHolAnd.md"
else
    echo "⚠ Markdown文件不存在: markdown/A_Holistic_and_Hybrid_Service_Selection_Strategy_for_MEC-Based_UAV_Last-Mile_Delivery_Systems.md"
fi

# hou2025AgeOfInf
# Age of Information-Aware Multi-Objective Optimization for Heterogeneous UAV-USV-...
# 相似度: 81.36%
if [ -f "markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md" ]; then
    mv "markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md" "markdown/hou2025AgeOfInf.md"
    echo "✓ Markdown重命名: Age_of_Information-Aware_Multi-Objective_Optimization_for_He... -> hou2025AgeOfInf.md"
else
    echo "⚠ Markdown文件不存在: markdown/Age_of_Information-Aware_Multi-Objective_Optimization_for_Heterogeneous_UAV-USV-UUV_Networks_in_Underwater_Target_Hunting.md"
fi

# li2025DynRouMec
# Dynamic Routing Mechanism for Load Distribution in UAV
# 相似度: 77.05%
if [ -f "markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md" ]; then
    mv "markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md" "markdown/li2025DynRouMec.md"
    echo "✓ Markdown重命名: Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm... -> li2025DynRouMec.md"
else
    echo "⚠ Markdown文件不存在: markdown/Dynamic_Routing_Mechanism_for_Load_Distribution_in_UAV_Swarm_Networks_With_Edge_Caching.md"
fi

# chen2025JoiTraOpt
# Joint Trajectory Optimization and Resource Allocation in UAV-MEC
# 相似度: 76.19%
if [ -f "markdown/Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md" ]; then
    mv "markdown/Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md" "markdown/chen2025JoiTraOpt.md"
    echo "✓ Markdown重命名: Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV... -> chen2025JoiTraOpt.md"
else
    echo "⚠ Markdown文件不存在: markdown/Joint_Trajectory_Optimization_and_Resource_Allocation_in_UAV-MEC_Systems_A_Lyapunov-Assisted_DRL_Approach.md"
fi

# zhang2025QuaOnlTas
# Quantum-Assisted Online Task Offloading and Resource Allocation in MEC-enabled
# 相似度: 75.56%
if [ -f "markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md" ]; then
    mv "markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md" "markdown/zhang2025QuaOnlTas.md"
    echo "✓ Markdown重命名: Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocat... -> zhang2025QuaOnlTas.md"
else
    echo "⚠ Markdown文件不存在: markdown/Quantum-Assisted_Online_Task_Offloading_and_Resource_Allocation_in_MEC-Enabled_Satellite-Aerial-Terrestrial_Integrated_Networks.md"
fi

# tang2025DeeGraRei
# Deep Graph Reinforcement Learning for UAV-enabled
# 相似度: 74.78%
if [ -f "markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md" ]; then
    mv "markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md" "markdown/tang2025DeeGraRei.md"
    echo "✓ Markdown重命名: Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User... -> tang2025DeeGraRei.md"
else
    echo "⚠ Markdown文件不存在: markdown/Deep_Graph_Reinforcement_Learning_for_UAV-Enabled_Multi-User_Secure_Communications.md"
fi

# gong2025JoiOptThe
# Jointly Optimizing the Energy and Time for Multi-UAV
# 相似度: 74.58%
if [ -f "markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md" ]; then
    mv "markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md" "markdown/gong2025JoiOptThe.md"
    echo "✓ Markdown重命名: Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Cov... -> gong2025JoiOptThe.md"
else
    echo "⚠ Markdown文件不存在: markdown/Jointly_Optimizing_the_Energy_and_Time_for_Multi-UAV_3-D_Coverage_of_Terrestrial_Regions.md"
fi

# wang2025OptJoiSpe
# Optimizing Joint Speed and Altitude Schedule for UAV
# 相似度: 73.81%
if [ -f "markdown/Wang-2025-Optimizing Joint Speed and Altitude.md" ]; then
    mv "markdown/Wang-2025-Optimizing Joint Speed and Altitude.md" "markdown/wang2025OptJoiSpe.md"
    echo "✓ Markdown重命名: Wang-2025-Optimizing Joint Speed and Altitude.md -> wang2025OptJoiSpe.md"
else
    echo "⚠ Markdown文件不存在: markdown/Wang-2025-Optimizing Joint Speed and Altitude.md"
fi

# zhang2025ImpDatCol
# Improving Data Collection Efficiency of UAV-assisted LoRa
# 相似度: 73.53%
if [ -f "markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md" ]; then
    mv "markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md" "markdown/zhang2025ImpDatCol.md"
    echo "✓ Markdown重命名: Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Ne... -> zhang2025ImpDatCol.md"
else
    echo "⚠ Markdown文件不存在: markdown/Improving_Data_Collection_Efficiency_of_UAV-Assisted_LoRa_Networks_via_Directivity-Aware_Link_Model.md"
fi

# krishna moorthy2022EsnReiLea
# ESN Reinforcement Learning
# 相似度: 70.97%
if [ -f "markdown/shao2024DeepReinforcementLearningbased.md" ]; then
    mv "markdown/shao2024DeepReinforcementLearningbased.md" "markdown/krishna moorthy2022EsnReiLea.md"
    echo "✓ Markdown重命名: shao2024DeepReinforcementLearningbased.md -> krishna moorthy2022EsnReiLea.md"
else
    echo "⚠ Markdown文件不存在: markdown/shao2024DeepReinforcementLearningbased.md"
fi

# qin2025MulReiLea
# Multi-Agent Reinforcement Learning in Adversarial Game Environments: Personalize...
# 相似度: 70.94%
if [ -f "markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md" ]; then
    mv "markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md" "markdown/qin2025MulReiLea.md"
    echo "✓ Markdown重命名: Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Envir... -> qin2025MulReiLea.md"
else
    echo "⚠ Markdown文件不存在: markdown/Multi-Agent_Reinforcement_Learning_in_Adversarial_Game_Environments_Personalized_Anti-Interference_Strategies_for_Heterogeneous_UAV_Communication.md"
fi

# pan2025CooUavRis
# Cooperative UAV-mounted RISs-assisted
# 相似度: 69.47%
# 相似度较低，跳过: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 建议: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> pan2025CooUavRis.md

# wu2025RecIntSur
# Reconfigurable Intelligent Surface Assisted UAV-MCS
# 相似度: 64.34%
# 相似度较低，跳过: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md
# 建议: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md -> wu2025RecIntSur.md

# wang2025JoiPosAnd
# Joint Positioning and Computation Offloading in Multi-UAV MEC
# 相似度: 63.86%
# 相似度较低，跳过: Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md
# 建议: Joint_Positioning_and_Computation_Offloading_in_Multi-UAV_MEC_for_Low_Latency_Applications_A_Proximal_Policy_Optimization_Approach.md -> wang2025JoiPosAnd.md

# kumari2025MaxSerPro
# Maximizing Service Provider's Profit in Multi-UAV 5G
# 相似度: 62.86%
# 相似度较低，跳过: Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md
# 建议: Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring.md -> kumari2025MaxSerPro.md

# liu2025DelGooDel
# Delay-Sensitive Goods Delivery and in-Situ Sensing Using a Multi-Task Drone
# 相似度: 62.75%
# 相似度较低，跳过: Liu-2025-Delay-Sensitive Goods Delivery and In.md
# 建议: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> liu2025DelGooDel.md

# wang2025SmaShiPre
# Smart Shield: Prevent
# 相似度: 62.07%
# 相似度较低，跳过: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md
# 建议: Wang-2025-Smart Shield_ Prevent Aerial Eavesdr.md -> wang2025SmaShiPre.md

# cao2021RecIntSur
# Reconfigurable Intelligent Surface-Assisted Aerial-Terrestrial Communications
# 相似度: 61.90%
# 相似度较低，跳过: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md
# 建议: Reconfigurable_Intelligent_Surface_Assisted_UAV-MCS_Based_on_Transformer_Enhanced_Deep_Reinforcement_Learning.md -> cao2021RecIntSur.md

# zhao2025AgaMobCol
# Against Mobile Collusive Eavesdroppers: Cooperative
# 相似度: 61.74%
# 相似度较低，跳过: Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md
# 建议: Against_Mobile_Collusive_Eavesdroppers_Cooperative_Secure_Transmission_and_Computation_in_UAV-Assisted_MEC_Networks.md -> zhao2025AgaMobCol.md

# liu2020EneUavCro
# Energy-Efficient UAV Crowdsensing
# 相似度: 61.22%
# 相似度较低，跳过: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 建议: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md -> liu2020EneUavCro.md

# sun2025AerRelCol
# Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Ev...
# 相似度: 59.00%
# 相似度较低，跳过: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md
# 建议: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md -> sun2025AerRelCol.md

# dou2025SchDroAnd
# Scheduling Drone and Mobile Charger via Hybrid-Action Deep Reinforcement Learnin...
# 相似度: 58.18%
# 相似度较低，跳过: Dou-2025-Scheduling Drone and Mobile Charger v.md
# 建议: Dou-2025-Scheduling Drone and Mobile Charger v.md -> dou2025SchDroAnd.md

# li2025JoiSerCac
# Joint Service Caching and Computation Offloading Scheme with 3D UAV
# 相似度: 56.93%
# 相似度较低，跳过: Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md
# 建议: Wang 等 - 2024 - UAV-Assisted Target Tracking and Computation Offloading in USV-Based MEC Networks.md -> li2025JoiSerCac.md

# liu2023FaiEneRes
# Fair Energy-Efficient Resource Optimization for Green Multi-NOMA-UAV
# 相似度: 56.93%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> liu2023FaiEneRes.md

# wu2026SerSegTra
# Service-Oriented Segmented Trajectory Design for Low-Altitude UAV-assisted MEC
# 相似度: 56.16%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> wu2026SerSegTra.md

# zhou2025DigTwiEmp
# Digital Twin Empowered mmWave
# 相似度: 55.91%
# 相似度较低，跳过: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md
# 建议: Digital_Twin_Empowered_mmWave_Multi-Hop_V2X_Routing_Scheme_With_UAV_Assistance.md -> zhou2025DigTwiEmp.md

# wu2020DelTraDes
# Delay-Sensitive Trajectory Designing
# 相似度: 55.56%
# 相似度较低，跳过: Liu-2025-Delay-Sensitive Goods Delivery and In.md
# 建议: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> wu2020DelTraDes.md

# sun2021TimAndEne
# Time and Energy Minimization Communications Based
# 相似度: 54.72%
# 相似度较低，跳过: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 建议: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> sun2021TimAndEne.md

# kimura2020DisCol3dd
# Distributed Collaborative 3D-Deployment
# 相似度: 54.55%
# 相似度较低，跳过: Sun-2025-Aerial Reliable Collaborative Communi.md
# 建议: Sun-2025-Aerial Reliable Collaborative Communi.md -> kimura2020DisCol3dd.md

# li2025ExpTheRob
# Exploring the Robustness: Hierarchical
# 相似度: 54.40%
# 相似度较低，跳过: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md
# 建议: Exploring_the_Robustness_Hierarchical_Federated_Learning_Framework_for_Object_Detection_of_UAV_Cluster.md -> li2025ExpTheRob.md

# zhang2025MulAerCol
# Multi-Objective Aerial Collaborative Secure Communication Optimization via Gener...
# 相似度: 54.19%
# 相似度较低，跳过: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md
# 建议: Liu 等 - 2024 - UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning.md -> zhang2025MulAerCol.md

# ning2023DynComOff
# Dynamic Computation Offloading
# 相似度: 53.73%
# 相似度较低，跳过: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 建议: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> ning2023DynComOff.md

# dai2023DelEneUav
# Delay-Sensitive Energy-Efficient UAV Crowdsensing
# 相似度: 53.57%
# 相似度较低，跳过: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 建议: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md -> dai2023DelEneUav.md

# han2022JoiDepOpt
# Joint Deployment Optimization
# 相似度: 52.94%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> han2022JoiDepOpt.md

# zhang2025LarModFor
# Large Models for Aerial Edges: An
# 相似度: 52.94%
# 相似度较低，跳过: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md
# 建议: Large_Models_for_Aerial_Edges_An_Edge-Cloud_Model_Evolution_and_Communication_Paradigm.md -> zhang2025LarModFor.md

# lin2024ALyaApp
# A Lyapunov-Based Approach to Joint Optimization of Resource Allocation and 3-D
# 相似度: 52.53%
# 相似度较低，跳过: lin2024LyapunovbasedApproachJoint.md
# 建议: lin2024LyapunovbasedApproachJoint.md -> lin2024ALyaApp.md

# zhan2022EneTraOpt
# Energy-Efficient Trajectory Optimization
# 相似度: 52.17%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> zhan2022EneTraOpt.md

# zhang2022EneTraOpt
# Energy-Efficient Trajectory Optimization
# 相似度: 52.17%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> zhang2022EneTraOpt.md

# gao2023AUavMul
# A UAV-Assisted Multi-Task Allocation Method
# 相似度: 51.95%
# 相似度较低，跳过: Zhang-2025-Quantum-Assisted Online Task Offloa.md
# 建议: Zhang-2025-Quantum-Assisted Online Task Offloa.md -> gao2023AUavMul.md

# {do-duy2021JoiOpt
# Joint Optimisation
# 相似度: 51.72%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> {do-duy2021JoiOpt.md

# guo2025MigTow
# Mighty: Towards
# 相似度: 50.98%
# 相似度较低，跳过: Guo-2025-Mighty_ Towards Long-Range and High-T.md
# 建议: Guo-2025-Mighty_ Towards Long-Range and High-T.md -> guo2025MigTow.md

# zeng2019EneMinFor
# Energy Minimization for Wireless Communication with Rotary-Wing UAV
# 相似度: 50.00%
# 相似度较低，跳过: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md
# 建议: Trajectory_Optimization_and_Power_Allocation_for_Multi-UAV_Wireless_Networks_A_Communication-Based_Multi-Agent_Deep_Reinforcement_Learning_Approach.md -> zeng2019EneMinFor.md

# hanna2021UavSwaPos
# UAV Swarm Position Optimization
# 相似度: 49.28%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> hanna2021UavSwaPos.md

# li2023DatColMax
# Data Collection Maximization
# 相似度: 47.76%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> li2023DatColMax.md

# wu2025SecDesOf
# Security-Aware Designs of Multi-UAV
# 相似度: 47.62%
# 相似度较低，跳过: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md
# 建议: Security-Aware_Designs_of_Multi-UAV_Deployment_Task_Offloading_and_Service_Placement_in_Edge_Computing_Networks.md -> wu2025SecDesOf.md

# xu2022ThrMax
# Throughput Maximization
# 相似度: 47.62%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> xu2022ThrMax.md

# mao2022JoiDisBea
# Joint Distributed Beamforming
# 相似度: 47.06%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> mao2022JoiDisBea.md

# zhou2022ComBitMax
# Computation Bits Maximization
# 相似度: 47.06%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> zhou2022ComBitMax.md

# arribas2020CovOpt
# Coverage Optimization
# 相似度: 45.90%
# 相似度较低，跳过: jia2025DistributionallyRobustOptimization.md
# 建议: jia2025DistributionallyRobustOptimization.md -> arribas2020CovOpt.md

# pan2023ExtDelRan
# Extending Delivery Range
# 相似度: 45.90%
# 相似度较低，跳过: Liu-2025-Delay-Sensitive Goods Delivery and In.md
# 建议: Liu-2025-Delay-Sensitive Goods Delivery and In.md -> pan2023ExtDelRan.md

# wang2023MulCooTra
# Multi-UAV Cooperative Trajectory
# 相似度: 45.28%
# 相似度较低，跳过: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# 建议: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md -> wang2023MulCooTra.md

# li2024MaxNetThr
# Maximizing Network Throughput
# 相似度: 44.78%
# 相似度较低，跳过: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 建议: Zhang-2025-Optimizing Monitoring Utility of Un.md -> li2024MaxNetThr.md

# idrees2025ACluAlg
# A Clustering Algorithm for Detecting Differential Deviations in the Multivariate...
# 相似度: 44.44%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> idrees2025ACluAlg.md

# lin2021MinChaDel
# Minimizing Charging Delay
# 相似度: 44.44%
# 相似度较低，跳过: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 建议: Zhang-2025-Optimizing Monitoring Utility of Un.md -> lin2021MinChaDel.md

# yin2023ObsEveSli
# Observer-Based Event-Triggered Sliding Mode Control for Secure Formation Trackin...
# 相似度: 44.03%
# 相似度较低，跳过: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md
# 建议: Improving_User_QoE_via_Joint_Trajectory_and_Resource_Optimization_in_Multi-UAV_Assisted_MEC.md -> yin2023ObsEveSli.md

# sabzehali2022OptNumPla
# Optimizing Number, Placement, and Backhaul Connectivity of Multi-UAV
# 相似度: 44.00%
# 相似度较低，跳过: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 建议: Zhang-2025-Optimizing Monitoring Utility of Un.md -> sabzehali2022OptNumPla.md

# li2024UavQos
# UAVs-assisted QoS
# 相似度: 43.64%
# 相似度较低，跳过: Zhang-2025-Quantum-Assisted Online Task Offloa.md
# 建议: Zhang-2025-Quantum-Assisted Online Task Offloa.md -> li2024UavQos.md

# wu2022ANovAib
# A Novel AI-Based Framework
# 相似度: 43.64%
# 相似度较低，跳过: lin2024LyapunovbasedApproachJoint.md
# 建议: lin2024LyapunovbasedApproachJoint.md -> wu2022ANovAib.md

# baltaci2021ExpUavDat
# Experimental UAV Data Traffic Modeling
# 相似度: 43.14%
# 相似度较低，跳过: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 建议: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md -> baltaci2021ExpUavDat.md

# zheng2021UavComWit
# UAV Communications With WPT-Aided Cell-Free Massive MIMO Systems
# 相似度: 43.14%
# 相似度较低，跳过: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md
# 建议: Zhang 等 - 2024 - UAV Swarm-Enabled Collaborative Secure Relay Communications With Time-Domain Colluding Eavesdropper.md -> zheng2021UavComWit.md

# du2022RobTenAlg
# Robust Tensor-Based Algorithm
# 相似度: 43.08%
# 相似度较低，跳过: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 建议: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> du2022RobTenAlg.md

# zhang2021AoiStaDel
# AoI-Driven Statistical Delay
# 相似度: 43.08%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> zhang2021AoiStaDel.md

# dai2022AoiUavCro
# AoI-minimal UAV Crowdsensing
# 相似度: 43.01%
# 相似度较低，跳过: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 建议: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md -> dai2022AoiUavCro.md

# li2024ComOveThe
# Computing over the Sky: Joint UAV
# 相似度: 42.62%
# 相似度较低，跳过: lin2024LyapunovbasedApproachJoint.md
# 建议: lin2024LyapunovbasedApproachJoint.md -> li2024ComOveThe.md

# matar2021JoiSubAll
# Joint Subchannel Allocation
# 相似度: 42.42%
# 相似度较低，跳过: Sun-2025-Aerial Reliable Collaborative Communi.md
# 建议: Sun-2025-Aerial Reliable Collaborative Communi.md -> matar2021JoiSubAll.md

# qi2023CoaForGro
# Coalitional Formation-Based Group-Buying
# 相似度: 42.31%
# 相似度较低，跳过: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md
# 建议: Energy-Efficient_3-D_Data_Collection_forMulti-UAV_Assisted_Mobile_Crowdsensing.md -> qi2023CoaForGro.md

# wu2020AdaAndExt
# Adaptive and Extensible Energy Supply Mechanism
# 相似度: 42.31%
# 相似度较低，跳过: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 建议: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> wu2020AdaAndExt.md

# iyer2020AirSenNet
# Airdropping Sensor Networks from Drones and Insects
# 相似度: 41.60%
# 相似度较低，跳过: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md
# 建议: Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach.md -> iyer2020AirSenNet.md

# azizi2020ProMax
# Profit Maximization
# 相似度: 41.38%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> azizi2020ProMax.md

# xu2021StrLeaApp
# Strategic Learning Approach
# 相似度: 41.38%
# 相似度较低，跳过: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md
# 建议: Song 等 - 2024 - AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC A Multi-Objective Learning Approach.md -> xu2021StrLeaApp.md

# zhang2024IncMec
# Incentive Mechanisms
# 相似度: 41.38%
# 相似度较低，跳过: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 建议: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> zhang2024IncMec.md

# bannis2020BleMotAud
# Bleep: Motor-Enabled Audio Side-Channel for Constrained UAVs
# 相似度: 41.30%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> bannis2020BleMotAud.md

# jha2021VisEnaTim
# Visage: Enabling Timely Analytics for Drone Imagery
# 相似度: 40.48%
# 相似度较低，跳过: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 建议: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> jha2021VisEnaTim.md

# soorki2025CatMeIf
# Catch Me If You Can: Deep
# 相似度: 40.43%
# 相似度较低，跳过: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md
# 建议: Soorki 等 - 2025 - Catch Me If You Can Deep Meta-RL for Search-and-Rescue Using LoRa UAV Networks.md -> soorki2025CatMeIf.md

# tun2025JoiUav
# Joint UAV
# 相似度: 40.00%
# 相似度较低，跳过: Jia2024.md
# 建议: Jia2024.md -> tun2025JoiUav.md

# wang2023JoiUav
# Joint UAV
# 相似度: 40.00%
# 相似度较低，跳过: Jia2024.md
# 建议: Jia2024.md -> wang2023JoiUav.md

# zhou2024JoiUav
# Joint UAV
# 相似度: 40.00%
# 相似度较低，跳过: Jia2024.md
# 建议: Jia2024.md -> zhou2024JoiUav.md

# chiaraviglio2021MulThr
# Multi-Area Throughput
# 相似度: 39.58%
# 相似度较低，跳过: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md
# 建议: A_Multi-UAV_Cooperative_Task_Scheduling_in_Dynamic_Environments_Throughput_Maximization.md -> chiaraviglio2021MulThr.md

# cai2021EmpLowAir
# Empirical Low-Altitude Air-to-Ground Spatial Channel Characterization
# 相似度: 39.02%
# 相似度较低，跳过: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 建议: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> cai2021EmpLowAir.md

# ma2021ANonGeo
# A Non-Stationary Geometry-Based MIMO Channel Model
# 相似度: 39.02%
# 相似度较低，跳过: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 建议: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> ma2021ANonGeo.md

# sorbelli2022MeaErr
# Measurement Errors
# 相似度: 38.60%
# 相似度较低，跳过: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md
# 建议: Zheng-2025-UAV Swarm-Enabled Collaborative Pos.md -> sorbelli2022MeaErr.md

# hansen2017VarNeiSea
# Variable Neighborhood Search: Basics and Variants
# 相似度: 38.55%
# 相似度较低，跳过: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 建议: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> hansen2017VarNeiSea.md

# tang2020C14AssTim
# C-14: Assured Timestamps for Drone Videos
# 相似度: 37.84%
# 相似度较低，跳过: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 建议: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> tang2020C14AssTim.md

# dai2023VisUav
# Vision-Based UAV
# 相似度: 37.74%
# 相似度较低，跳过: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 建议: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> dai2023VisUav.md

# dai2023VisUav
# Vision-Based UAV
# 相似度: 37.74%
# 相似度较低，跳过: Yu-2025-Hybrid Transformer Based Multi-Agent R.md
# 建议: Yu-2025-Hybrid Transformer Based Multi-Agent R.md -> dai2023VisUav.md

# wang2023DynUavDep
# Dynamic UAV Deployment
# 相似度: 37.29%
# 相似度较低，跳过: Li-2025-Dynamic Routing Mechanism for Load Dis.md
# 建议: Li-2025-Dynamic Routing Mechanism for Load Dis.md -> wang2023DynUavDep.md

# zhu2025AnEffUav
# An Effective UAV
# 相似度: 36.36%
# 相似度较低，跳过: Zhang-2025-Multi-Objective Aerial Collaborativ.md
# 建议: Zhang-2025-Multi-Objective Aerial Collaborativ.md -> zhu2025AnEffUav.md

# tuan2021MpcUavNav
# MPC-Based UAV Navigation
# 相似度: 36.14%
# 相似度较低，跳过: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md
# 建议: Cooperative_UAV-Mounted_RISs-Assisted_Energy-Efficient_Communications.md -> tuan2021MpcUavNav.md

# sie2023Bat
# BatMobility
# 相似度: 35.29%
# 相似度较低，跳过: Zhang-2025-Optimizing Monitoring Utility of Un.md
# 建议: Zhang-2025-Optimizing Monitoring Utility of Un.md -> sie2023Bat.md

# zhang2021StaDel
# Statistical Delay
# 相似度: 32.14%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> zhang2021StaDel.md

# liwang2021LetTra
# Let's Trade
# 相似度: 32.00%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> liwang2021LetTra.md

# wu2020LoaBal
# Load Balance
# 相似度: 31.37%
# 相似度较低，跳过: Lee-2025-Adaptive Stabilization Control by Dee.md
# 建议: Lee-2025-Adaptive Stabilization Control by Dee.md -> wu2020LoaBal.md


echo "=================================================="
echo "Markdown文件重命名完成！共处理 210 个文件"
echo "高质量匹配: 129 个"
echo "=================================================="
echo "Markdown文件在: markdown/"
echo "请检查重命名结果。"