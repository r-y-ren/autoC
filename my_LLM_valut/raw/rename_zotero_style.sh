#!/bin/bash
# 基于Zotero citation key规则的重命名脚本
# 规则：auth.lower + year + shorttitle(3,3)
# 例如：wu2026ServiceorientedSegmentedTrajectory
#
# 共处理 528 个文献条目
#
set -e  # 遇到错误立即退出

cd /Users/wupengfei/Downloads/my_LLM_valut/raw

# akram2022ASecAnd
# A Secure and Lightweight Drones-Access Protocol for Smart City Surveillance

# alam2024JoiTraCon
# Joint Trajectory Control, Frequency Allocation, and Routing for UAV

# alkouz2022InfEneCom
# In-Flight Energy-Driven Composition of Drone Swarm Services

# chen2024AdaBitVid
# Adaptive Bitrate Video Caching

# chen2024Uit
# UITDE

# dai2023DelEneUav
# Delay-Sensitive Energy-Efficient UAV Crowdsensing

# dai2023MulDeeRei
# Multi-Agent Deep Reinforcement Learning

# dai2024UavTasOff
# UAV-Assisted Task Offloading

# gao2024SerExpOri
# Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs

# gong2025JoiOptThe
# Jointly Optimizing the Energy and Time for Multi-UAV

# gui2024CovProAnd
# Coverage Probability and Throughput Optimization in Integrated mmWave

# han2021UavBacCom
# UAV-Aided Backscatter Communications

# han2024JoiAssDep
# Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-e...

# han2024ColRouPla
# Collaborative Route Planning of UAVs

# hao2024JoiTasOff
# Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV

# hao2025RelOptOf
# Reliability-Aware Optimization of Task Offloading for UAV-assisted

# he2024BalTotEne
# Balancing Total Energy Consumption

# he2024AnOnlJoi
# An Online Joint Optimization Approach for QoE

# hu2023AMobSpe
# A Mobility-Resilient Spectrum Sharing Framework

# huang2021AUavUbi
# A UAV-Assisted Ubiquitous Trust Communication System

# iyer2020AirSenNet
# Airdropping Sensor Networks from Drones and Insects

# ji2024DecAssWit
# Decoupled Association With Rate Splitting Multiple Access

# jia2024EneAndTim
# Energy and Time Trade-off Optimization for Multi-UAV

# jia2025DisRobOpt
# Distributionally Robust Optimization for Aerial Multi-Access Edge Computing via ...

# jin2025AResCon
# A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV

# kang2024AutMulRac
# Autonomous Multi-Drone Racing Method Based on Deep Reinforcement Learning

# kumar2025DroIrs
# Drone-Assisted IRS

# kumari2025MaxSerPro
# Maximizing Service Provider's Profit in Multi-UAV 5G

# lei2025EdgInfHub
# Edge Information Hub: Orchestrating

# li2024UavQos
# UAVs-assisted QoS

# li2024MaxNetThr
# Maximizing Network Throughput

# li2025DynRouMec
# Dynamic Routing Mechanism for Load Distribution in UAV

# li2025FedMetBas
# Federated Meta-Learning Based Computation Offloading Approach with Energy-Delay ...

# li2025TamEveCam
# Taming Event Cameras with Bio-Inspired Architecture and Algorithm: A

# lin2024ALyaApp
# A Lyapunov-Based Approach to Joint Optimization of Resource Allocation and 3-D

# liu2020DisEneMul
# Distributed Energy-Efficient Multi-UAV Navigation

# liu2020EneUavCro
# Energy-Efficient UAV Crowdsensing

# liu2020AccPoi
# Access Points

# liu2025DelGooDel
# Delay-Sensitive Goods Delivery and in-Situ Sensing Using a Multi-Task Drone

# liu2025AHybOpt
# A Hybrid Optimization Framework for Age of Information Minimization in UAV-assis...

# liu2025OnTheRob
# On the Robust Topology Recovery of UAV

# matar2025JoiOptOf
# Joint Optimization of User Association, Power Control, and Dynamic Spectrum Shar...

# nelson2024RlbEneDat
# RL-Based Energy-Efficient Data Transmission Over Hybrid BLE

# ning2025JoiOptOf
# Joint Optimization of Data Acquisition and Trajectory Planning for UAV-assisted

# pan2025CooUavRis
# Cooperative UAV-mounted RISs-assisted

# qian2024APatPla
# A Path Planning Algorithm for a Crop Monitoring Fixed-Wing Unmanned Aerial Syste...

# qin2023JoiOptOf
# Joint Optimization of Resource Allocation, Phase Shift, and UAV

# qin2022MulReiLea
# Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Comput...

# ren2024IntAdaGos
# Intelligent Adaptive Gossip-Based Broadcast Protocol

# rizvi2025MonIntSer
# Monitoring Inter-Drone Service Interference for Resilient Operations

# shao2024DeeReiLea
# Deep Reinforcement Learning-Based Resource Management for UAV-assisted

# shen2024SliTasOff
# Slicing-Based Task Offloading

# shi2024ATwoStr
# A Two-Stage Strategy

# singh2024StaMatBas
# Stable Matching Based Revenue Maximization for Federated Learning in UAV-assiste...

# song2024EneTraOpt
# Energy-Efficient Trajectory Optimization with Wireless Charging in UAV-assisted ...

# sun2024AllAutCom
# All-Sky Autonomous Computing in UAV

# sun2024MulOptFor
# Multi-Objective Optimization for Multi-UAV-assisted

# sun2025AerRelCol
# Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Ev...

# tang2021AnAerCom
# An Aerodynamic, Computer Vision, and Network Simulator for Networked Drone Appli...

# tian2024UavWirCoo
# UAV-Assisted Wireless Cooperative Communication

# tlili2023ANewHyb
# A New Hybrid Adaptive Deep Learning-Based Framework for UAVs

# wan2025AMulSca
# A Multimodal Scale Normalization Framework for Vision-Radar Small UAV

# wang2024BioAntCol
# Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading...

# wang2024DecNavWit
# Decentralized Navigation with Heterogeneous Federated Reinforcement Learning for...

# wang2024ResAllIn
# Resource Allocation in Blockchain Integration of UAV-enabled MEC

# wang2024Uav
# UAV-assisted

# wang2024AUavTru
# A UAV-Assisted Truth Discovery Approach With Incentive Mechanism Design

# wang2024WirPowMet
# Wireless Powered Metaverse

# wang2025JoiTasOff
# Joint Task Offloading and Migration Optimization in UAV-enabled

# wu2025SecDesOf
# Security-Aware Designs of Multi-UAV

# wu2025TwoDeeEne
# Two-Stage Deep Energy Optimization in IRS-assisted UAV-based

# xie2025BloLigCro
# Blockchain-Assisted Lightweight Cross-Domain Authentication for Multi-UAV

# xu2025BloGamThe
# Blockchain-Empowered Game Theoretical Incentive for Secure Bandwidth Allocation ...

# xu2025TruGamInc
# Trust-Enhanced Game Incentive for Secure Quantum Federated Learning in UAV-assis...

# xu2025WinSerPro
# Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery

# xue2024TowMaxCov
# Towards Maximizing Coverage of Targets for WRSNs

# yuan2024DynEveFau
# Dynamic Event-Triggered Fault-Tolerant Cooperative Resilient Tracking Control wi...

# zeng2019EneMinFor
# Energy Minimization for Wireless Communication with Rotary-Wing UAV

# zeng2025AJoiSec
# A Joint Secure Mechanism of Multi-Task Learning for a UAV

# zhan2025OnlEneAnd
# Online Energy and Interference Management for Dynamic Target Tracking with Cellu...

# zhang2025LarModFor
# Large Models for Aerial Edges: An

# zhang2025OptMonUti
# Optimizing Monitoring Utility of Uncrewed Aerial Vehicles Considering Adverse Ef...

# zhao2025JoiConCac
# Joint Content Caching, Service Placement, and Task Offloading in UAV-enabled

# zhao2025JoiOptOf
# Joint Optimization of Trajectory, Offloading, Caching, and Migration for UAV-ass...

# zheng2024ConDelPer
# Content Delivery Performance Analysis

# zhou2021UavCovWir
# UAV-Enabled Covert Wireless Data Collection

# zhou2024AFedDig
# A Federated Digital Twin Framework

# zhou2024SymMulRei
# Symmetry-Augmented Multi-Agent Reinforcement Learning for Scalable UAV

# zhou2025DigTwiEmp
# Digital Twin Empowered mmWave

# zhou2025UsePreOri
# User Preference Oriented Service Caching and Task Offloading for UAV-assisted ME...

# zhu2023Uav
# UAV

# zhu2024ColReiLea
# Collaborative Reinforcement Learning Based Unmanned Aerial Vehicle (UAV

# zhu2024FisSpeClu
# Fission Spectral Clustering Strategy for UAV

# zhu2023AttConOf
# Attitude Control of a Novel Tilt-Wing UAV


echo "=================================================="
echo "文件重命名完成！共处理 94 个文献"
echo "=================================================="
echo "PDF文件在: pdfs/"
echo "Markdown文件在: markdown/"
echo "请检查重命名结果。"