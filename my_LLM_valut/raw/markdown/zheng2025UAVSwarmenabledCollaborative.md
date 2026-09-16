# UAV Swarm-Enabled Collaborative Post-Disaster Communications in Low Altitude Economy via a Two-Stage Optimization Approach

Xiaoya Zheng , Geng Sun , Senior Member, IEEE, Jiahui Li , Student Member, IEEE, Jiacheng Wang , Member, IEEE, Qingqing Wu , Senior Member, IEEE, Dusit Niyato , Fellow, IEEE, and Abbas Jamalipour , Fellow, IEEE

AbstractâThe low-altitude economy (LAE), as a new economic paradigm, plays an indispensable role in cargo transportation, healthcare, infrastructure inspection, and especially post-disaster communications. Specifically, uncrewed aerial vehicles (UAVs), as one of the core technologies of the LAE, can be deployed to provide communication coverage, facilitate data collection, and relay data for trapped users, thereby significantly enhancing the efficiency of post-disaster response efforts. However, conventional UAV selforganizing networks exhibit low reliability in long-range cases due to their limited onboard energy and transmit ability. Therefore, in this paper, we design an efficient and robust UAV-swarm enabled collaborative self-organizing network to facilitate post-disaster communications. Specifically, a ground device transmits data to UAV swarms, which then use collaborative beamforming (CB) technique to form virtual antenna arrays and relay the data to a remote access point (AP) efficiently. Then, we formulate a rescue-oriented post-disaster transmission rate maximization optimization problem (RPTRMOP), aimed at maximizing the transmission rate of

Received 2 January 2025; revised 17 April 2025; accepted 17 June 2025. Date of publication 26 June 2025; date of current version 3 October 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62272194 and Grant 62471200, in part by the Science and Technology Development Plan Project of Jilin Province under Grant 20250101027JJ, in part by the National Research Foundation, Singapore, and Infocomm Media Development Authority under its Future Communications Research & Development Programme, Defence Science Organisation (DSO) National Laboratories under the AI Singapore Programme under Grant FCP-NTU-RG-2022-010 and Grant FCP-ASTAR-TG-2022-003, in part by Singapore Ministry of Education (MOE) Tier 1 under Grant RG87/22, and in part by the NTU Centre for Computational Technologies in Finance (NTU-CCTF). Recommended for acceptance by H. Yao. (Corresponding authors: Geng Sun; Jiahui Li.)

Qingqing Wu is with the Department of Electronic Engineering, Shanghai Jiao Tong University, Shanghai 200240, China (e-mail: qingqingwu@sjtu.edu.cn).

Abbas Jamalipour is with the School of Electrical and Computer Engineering, University of Sydney, Sydney, NSW 2006, Australia (e-mail: a.jamalipour@ieee.org).

This article has supplementary downloadable material available at https://doi.org/10.1109/TMC.2025.3583510, provided by the authors.

Digital Object Identifier 10.1109/TMC.2025.3583510

the whole network. Given the challenges of solving the formulated RPTRMOP by using traditional algorithms, we propose a twostage optimization approach to address it. In the first stage, the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the network are derived. In the second stage, we transform the formulated RPTRMOP into a variant named V-RPTRMOP based on the obtained optimal multi-path traffic routing, aimed at rendering the actual transmission rate closely approaches its theoretical upper bound by optimizing the excitation current weight and the placement of each participating UAV via a diffusion model-enabled particle swarm optimization (DM-PSO) algorithm. Simulation results show the effectiveness of the proposed two-stage optimization approach in improving the transmission rate of the constructed network, which demonstrates the great potential for post-disaster communications. Moreover, the robustness of the constructed network is also validated via evaluating the impact of three unexpected situations on the system transmission rate.

Index TermsâUncrewed aerial vehicles (UAVs), post-disaster communications, collaborative beamforming (CB), multi-path traffic routing design, UAV swarm optimization.

## I. INTRODUCTION

L OW-ALTITUDE economy (LAE), centered on low-altitude airspace, serves as a burgeoning and comprehensive economic form of future economic activities, carrying out various low-altitude flight activities below 1000 meters in altitude [1], [2]. LAE integrates advanced technologies such as uncrewed aerial vehicles, satellite communication, artificial intelligence, network communication, and uncrewed traffic management systems to enable the efficient integration of applications across various fields, including logistics, emergency response, and urban management [3]. The synergy among these technologies not only drives the development of the low-altitude economy but also positions it as a crucial link connecting ground-based economies with airspace resources, offering new opportunities for social and economic development as well as technological innovation [4], [5].

Beyond the aforementioned applications, the potential of the LAE in disaster relief is immense. Natural disasters, such as earthquakes, floods, or typhoons, often lead to the paralysis of terrestrial infrastructure and the malfunction of communication systems, significantly impairing the efficiency of search and rescue operations [6]. In such extreme conditions, LAE technologies, particularly uncrewed aerial vehicle (UAV) communication networks, can provide essential emergency communication services to the trapped ground users. Specifically, due to their agility and mobility, UAVs can be swiftly deployed to various gathering points, where affected users converge around limited rescue resources, providing reliable wireless communication services within their coverage areas [7]. Moreover, their high altitude facilitates line-of-sight (LoS) communication, which means that even though the distances among these gathering points are considerable, UAVs are still able to establish a self-organizing network to achieve connectivity both between gathering points and with remote access points (APs) or base stations [8].

However, conventional UAV-enabled self-organizing networks face significant limitations. Typically, data is forwarded by a single UAV to the next hop or receiver, which leads to two challenges. First, data forwarding is restricted to a single path, which significantly limits the transmission rate. Second, if the UAV responsible for a particular hop fails, the transmission task is completely disrupted, potentially leading to the collapse of the entire network. Thus, how to establish efficient and robust self-organizing networks becomes a critical challenge in such scenarios.

Multi-path routing provides an efficient solution to the first limitation. Specifically, it enables the parallel transmission of data packets across several distinct routes between the source and destination nodes. In the context of post-disaster relief, this inherent parallelism ensures that even if one or more paths are disrupted by environmental factors or node failures, the data transmission can continue uninterrupted through the remaining active routes.

Collaborative beamforming (CB) is an effective approach to addressing the second issue [9]. Specifically, multiple UAV elements can be deployed to form a virtual antenna array (VAA), and then transmit data towards the remote receiver in a cooperative manner [10]. By utilizing CB, the communication capabilities between widely separated gathering points and with external networks can be significantly enhanced. The application of CB offers the following typical advantages. First, if a single UAV within the VAA fails or becomes incapacitated, the remaining UAVs can dynamically adjust their respective excitation current weights to compensate for the loss. Second, compared to the conventional multi-hop communication mechanism, where multiple UAVs may fly far to predefined locations, CB only necessitates that UAVs fine-tune the excitation current weights and adjust their placements within a designated area to achieve a beam pattern with a high-gain mainlobe, making it a cost-effective approach, especially for UAV networks with limited resources. The approach enhances robustness by reducing reliance on extensive UAV flight, thereby mitigating risks related to energy consumption, navigation errors, or mechanical issues. Finally, with $N _ { \mathrm { U } }$ UAV elements, the formed VAA can achieve a gain of $N _ { \mathrm { U } } ^ { 2 }$ in received power, thereby significantly boosting communication performance [11]. This power gain further contributes to robustness by improving the capacity of the system to maintain stable communication under diverse conditions, such as signal fading, weather fluctuations, and the presence of obstacles. In conclusion, CB provides a plausible direction to establish a UAV swarm-enabled collaborative self-organizing network for postdisaster communications, facilitating connections between gathering points and between the gathering points and external APs.

Despite the advantages of CB, implementing a UAV-swarm enabled collaborative self-organizing network for post-disaster relief still faces several critical challenges. First, inappropriate multi-path traffic routing design can cause some nodes to become overloaded, leading to increased packet loss rates. Therefore, designing appropriate routing protocols is essential to ensure the integrity and reliability of post-disaster data transmission. Second, even with a designed multi-path traffic routing, UAV swarm optimization remains indispensable. By optimizing parameters such as UAV placement and resource allocation, resource utilization efficiency can be enhanced, which further reduces the communication delays and energy consumption. These challenges motivate us to explore new approaches that differ from existing literature. Different from our previous work, which focused on a single-hop architecture [12], this study presents a novel UAV swarm-enabled collaborative communication mechanism capable of achieving extended-distance communication in post-disaster scenarios. The main contributions are summarized as follows.

. Virtual Antenna Array-based Collaborative UAV Networking for Post-disaster Communications: We consider a post-disaster communication scenario, and design a novel network structure in which multiple UAV swarms relay data from a ground device in the post-disaster area to a remote access point (AP) in a CB manner. Intuitively, the constructed network is a realistic and meaningful system since the deployment of multiple UAV swarms can cover a wider post-disaster area and enhance network reliability. Moreover, applying CB in UAV networks is expected to significantly enhance data transmission efficiency. The network architecture exhibits robust since neither the failure of a single UAV nor the simultaneous incapacitation of an entire swarm results in a complete operational breakdown. To the best of our knowledge, the integration of CB with multiple UAV swarms for post-disaster communications has not yet been investigated.

- A Rescue-oriented Post-disaster Transmission Rate Maximization Problem Formulation: We formulate an optimization problem, termed rescue-oriented post-disaster transmission rate maximization optimization problem (RP-TRMOP), to improve the transmission rate of the communication network by conducting multi-path traffic routing design and controlling the excitation current weights and placements of UAVs. Though the structure of RPTRMOP appears simple, it cannot be directly handled using existing optimization algorithms.

Two-stage Optimization Approach Using Ford-Fulkerson and DM-PSO Algorithms: We propose an efficient twostage optimization approach to deal with the formulated RPTRMOP. In the first stage, the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the system are derived through theoretical analysis and the Ford-Fulkerson algorithm [13]. In the second stage, we transform the formulated RPTRMOP into a variant named V-RPTRMOP based on the obtained optimal multipath traffic routing, and propose a diffusion model-enabled particle swarm optimization (DM-PSO) algorithm to address it by optimizing the excitation current weight and the placement of each participating UAV, so that the actual transmission rate closely approaches its theoretical upper bound.

Performance Validation of the Collaborative UAV Networking and Two-stage Optimization Approach: Simulation results demonstrate the effectiveness of the proposed two-stage optimization approach in improving the transmission rate of the UAV-swarm enabled collaborative self-organizing network. Moreover, the robustness of the proposed network as well as the optimization approach is also validated through evaluating the impact of three unexpected situations on system performance.

The remainder of this work is organized as follows. Section II provides a comprehensive review of related works. Section III introduces the system model and formulates the optimization problem. Sections IV and V present the first and second stages in addressing the formulated optimization problem, respectively. Simulation results are presented in Section VI. Finally, Section VII concludes the paper.

## II. RELATED WORK

This section reviews works on UAV-assisted post-disaster communications, collaborative beamforming for UAV networks, routing design and UAV network optimization, and solution mechanisms in UAV communications. A summary of the key comparisons between related works and this work is provided in Table I, and the details are discussed as follows.

## A. UAV-Assisted Post-Disaster Communications

The application of UAVs for disaster response and relief has been extensively studied in the literature. For example, Tran et al. [14] deployed a UAV-mounted BS as a relay to collect data from the latency-sensitive Internet of Things (IoT) devices in post-disaster areas and then transfer it to a ground gateway. Specifically, they aimed to maximize the number of the served IoT devices, while considering the storage capacity of UAVs and the requirements of each device. Liu et al. [15] dispatched a multi-antenna UAV to provide emergency coverage for ground devices in disaster areas, with each antenna serving a device independently. To extend UAV coverage, the ground devices that are outside of its range can connect with those within it by using the proposed shortest-path routing algorithm. However, the works above rely on only a single UAV to provide communication services in post-disaster areas, which exposes the system to significant vulnerability since a failure or damage to the UAV could paralyze the entire communication system and result in data loss. Moreover, communication overload may occur as a single UAV must handle all requests from ground devices.

To overcome the aforementioned limitations and further enhance the coverage and reliability of post-disaster communication systems, numerous studies have explored the application of multiple UAVs working in collaboration. For example, Shah et al. [16] constructed a UAV-enabled mobile edge computing (MEC) network where UAVs are responsible for executing computational tasks offloaded by user equipments. Specifically, they aimed to optimize the system utility by optimizing user associations and other factors. Do-Duy et al. [17] deployed multiple UAVs as airborne relay stations to facilitate communication between a massive multi-input multi-output BS and several user clusters, focusing on the joint optimization of real-time deployment and resource allocation of the dispatched UAVs. Yao et al. [18] explored the application of intelligent reflective surface-assisted UAV communication networks. Then, they introduced a novel fading channel model for the network and optimized power allocation based on this model. Moreover, Wang et al. [19] studied a fog computing-based UAV system where UAVs offload intensive computational missions to vehicles with high processing capabilities, and proposed a game theory-based allocation strategy. However, due to limited transmit power, UAVs typically need to stay close to the served users to ensure high communication quality. In this case, the UAVs are required to keep flying or hovering for extended periods, leading to significant energy consumption, which is challenging for resource-constrained UAVs in disaster relief tasks.

## B. Collaborative Beamforming for UAV Networks

Several previous works considered to apply CB into UAV networks to reduce the energy consumption and enhance the data transmission efficiency. For example, Xu et al. [20] investigated a secure UAV swarm communication system where the target receivers and interception eavesdroppers coexist. For the purpose of enhancing target receiver radiation power and mitigating eavesdropper radiation power, a beamforming optimization problem is formulated and subsequently decomposed into static and dynamic optimization problems. Then, theoretical analysis, as well as conventional heuristic algorithm, are used to deal with them, respectively. Jung et al. [22] focused on the analog CB with random VAA topologies to provide a relatively higher secrecy rate by generating noise-like signals to eavesdroppers. Given limited onboard energy of UAVs, they proposed stochastic VAA where a group of UAVs randomly adjust their positions in a distributed manner, effectively randomizing the array factor of the VAA. Moreover, Li et al. [23] investigated a two-way distributed CB-enabled communication with multiple colluding eavesdroppers. Accordingly, the secrecy capacity and the maximum sidelobe level are minimized to avoid data leakage, while they also optimizing energy consumption of UAVs in both two swarms when constructing VAAs.

Shifting the focus from specific system designs to a more generalized framework, Moorthy et al. [21] proposed a learningbased framework termed as FlyBeam to overcome the impact of UAV altitude, mobility, and link blockages on beamforming gain. Specifically, a control problem is formulated to maximize the throughput of the UAV swarm network, and then an algorithm which integrates echo state network learning and online reinforcement learning is designed to deal with the problem. However, the aforementioned works only considered single VAA, while the coverage of a single VAA is limited, making it difficult to achieve wide-area signal coverage. Moreover, the entire communication link will be disrupted once the UAV swarm experiences a failure, leading to diminished system robustness.

TABLE I  
COMPARISONS BETWEEN RELATED WORKS WITH THIS WORK
<table><tr><td rowspan=1 colspan=1>Relatedworks</td><td rowspan=1 colspan=1>Numberof UAVs</td><td rowspan=1 colspan=1>Communicationscenarios</td><td rowspan=1 colspan=1>Optimizationvariables</td><td rowspan=1 colspan=1>Routingdesign</td><td rowspan=1 colspan=1>Networkoptimizationmetrics</td><td rowspan=1 colspan=1>Optimizationmethods</td></tr><tr><td rowspan=1 colspan=1>[14]</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>UAV-aided relaycommunication</td><td rowspan=1 colspan=1>Bandwidth, powerand UAV trajectory</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>The number ofserved devices</td><td rowspan=1 colspan=1>Iteration algorithm</td></tr><tr><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>UAV-assisted multihopD2D communication</td><td rowspan=1 colspan=1>Precoding anddecoding vector</td><td rowspan=1 colspan=1>Shortest pathrouting</td><td rowspan=1 colspan=1>Outrage proability,sum rate</td><td rowspan=1 colspan=1>Low-complexityalgorithm</td></tr><tr><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-assisted mobileedge computing</td><td rowspan=1 colspan=1>User associations,time, power, andlocation of UAVs</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Computationalefficiency</td><td rowspan=1 colspan=1>Multi-stageoffloadingalgorithm</td></tr><tr><td rowspan=1 colspan=1>[17]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-enabled relaycommunication</td><td rowspan=1 colspan=1>Time transferringand power allocation</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Energy efficiency</td><td rowspan=1 colspan=1>K-means clusteringalgorithm</td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-enabled relaycommunication</td><td rowspan=1 colspan=1>Bandwidth andtransmit power</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Capacity andenergy efficiency</td><td rowspan=1 colspan=1>Joint bandwidth andpower allocationalgorithm</td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Fog computing-basedUAVcommunication</td><td rowspan=1 colspan=1>Task offloading</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Utility of UAVs</td><td rowspan=1 colspan=1>Matching algorithm</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>CB-based UAV swarmsecure communication</td><td rowspan=1 colspan=1>UAV positions, andamplitude and phaseweights of signals</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Radiation power</td><td rowspan=1 colspan=1>Closed-formsolution and PSO</td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Distributed CB-basedUAVcommunication</td><td rowspan=1 colspan=1>Beamformingandflight of UAVs</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Network capacity</td><td rowspan=1 colspan=1>Reinforcementlearning</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Analog CB-based UAVsecure communication</td><td rowspan=1 colspan=1>Location of UAVs</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Security energyefficiency</td><td rowspan=1 colspan=1> Stochastic strategy</td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>CB-based two-wayUAV communication</td><td rowspan=1 colspan=1>3D placements,excitation current,and receivers</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Secrecy capacity,sidelobe level,andenergy consumption</td><td rowspan=1 colspan=1>Heuristic algorithm</td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Cognitive UAV Swarmcommunication</td><td rowspan=1 colspan=1>Next forwardingUAV</td><td rowspan=1 colspan=1>Intelligentrouting basedon Q-learning</td><td rowspan=1 colspan=1>Network utility</td><td rowspan=1 colspan=1>Iterative algorithm</td></tr><tr><td rowspan=1 colspan=1>[25]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-assisted datadissemination</td><td rowspan=1 colspan=1>Next forwardingUAV</td><td rowspan=1 colspan=1>Multi-hopopportunistic3D routing</td><td rowspan=1 colspan=1>The expectedprogress of data</td><td rowspan=1 colspan=1>Closed-form analysis</td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Three-layer UAVnetwork-assistedcommunication</td><td rowspan=1 colspan=1>Optimalnext-hop UAV</td><td rowspan=1 colspan=1>Greedyperimetercomprehensiveevaluation</td><td rowspan=1 colspan=1>Throughput ofUAVrelay</td><td rowspan=1 colspan=1>Analytic hierarchyprocess</td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Multi-UAV-enabledremote MEC</td><td rowspan=1 colspan=1>Resource allocation and deployment</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Networkcomputingrate</td><td rowspan=1 colspan=1>Global and localoptimal resourceallocation algorithms</td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-aided relaycommunication</td><td rowspan=1 colspan=1>Trajectories andpower allocationof UAVs</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Networkdata flow</td><td rowspan=1 colspan=1>Spectral graphtheory and convexoptimization</td></tr><tr><td rowspan=1 colspan=1>[28]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>NOMA-basedmulti-UAVcommunication</td><td rowspan=1 colspan=1>Transmit powerof UAVs</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Prioritized delayamong users</td><td rowspan=1 colspan=1>SDS-BSUMalgorithm</td></tr><tr><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-assisted MECcommunication</td><td rowspan=1 colspan=1>Topologyreconstruction andsubtask scheduling</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Average completiontime of the subtask</td><td rowspan=1 colspan=1>Game theory</td></tr><tr><td rowspan=1 colspan=1>[30]</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>UAV-enabled uplinkcommunication</td><td rowspan=1 colspan=1>UAV altitude,power,and bandwidthallocation</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>System uplinkthroughput</td><td rowspan=1 colspan=1>Successive convexapproximation</td></tr><tr><td rowspan=1 colspan=1>[31]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-assisteddispersed computing</td><td rowspan=1 colspan=1>Task size andtask offloading</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Energy consumptionof the system</td><td rowspan=1 colspan=1>Distributed algorithmbased on convexoptimization</td></tr><tr><td rowspan=1 colspan=1>[32]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-aided downlinkcommunication</td><td rowspan=1 colspan=1>UAV trajectory andpower allocation</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Network capacity</td><td rowspan=1 colspan=1>Successive convexapproximation</td></tr><tr><td rowspan=1 colspan=1>[33]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>UAV-enabled relaycommunication</td><td rowspan=1 colspan=1>UAV trajectory</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Interaction overheadand deploymentefficiency</td><td rowspan=1 colspan=1> Multi agent PPO</td></tr><tr><td rowspan=1 colspan=1>[34]</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>Multi-UAV-assisteddata collection</td><td rowspan=1 colspan=1>Multi-UAVscheduling</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Data value collectedbyallUAVs</td><td rowspan=1 colspan=1>Attention-basedDRL algorithm</td></tr><tr><td rowspan=1 colspan=1>[35]</td><td rowspan=1 colspan=1>Single</td><td rowspan=1 colspan=1>UAV-mounted BSfor date collection</td><td rowspan=1 colspan=1>UAV trajectory</td><td rowspan=1 colspan=1>Notmentioned</td><td rowspan=1 colspan=1>Uplink throughputof UAV networks</td><td rowspan=1 colspan=1>A safe-DQN-basedalgorithm</td></tr><tr><td rowspan=1 colspan=1>Ourwork</td><td rowspan=1 colspan=1>Multiple</td><td rowspan=1 colspan=1>CB-based UAV swarms long-rangecommunication</td><td rowspan=1 colspan=1>3D placement andexcitation currentweights of UAVs</td><td rowspan=1 colspan=1>Ford-Fulkersonalgorithm-basedmulti-pathrouting</td><td rowspan=1 colspan=1>Data transmissionrate of the wholesystem</td><td rowspan=1 colspan=1>DM-PSO</td></tr></table>

## C. Routing Design and UAV Network Optimization

Traffic routing design for post-disaster UAV networks has been widely investigated in existing works. For example, Zhang et al. [24] investigated the integration of cognitive radio with UAV swarms for emergency communications, and proposed a Q-learning-based architecture to obtain the intelligent routing. Sharvari et al. [25] proposed an opportunistic routing scheme considering UAV coverage and collision constraints, to maximize the expected progress of each hop data packet. Moreover, Yang et al. [8] constructed a three-layer UAV network to assist post-disaster relief and developed a greedy perimeter comprehensive evaluation routing algorithm. This algorithm selects the optimal next-hop UAV by assessing the link stability, throughput, and available energy of neighboring nodes. However, the works above do not consider UAV network optimization, potentially compromising transmission efficiency and reliability.

Several studies have investigated UAV network optimization for post-disaster communications. For example, He et al. [26] considered a multi-hop task offloading framework in which multiple UAVs collaborate to offload task while simultaneously performing edge computing operations, and they proposed two algorithms to optimize the resource allocation and deployment of the UAVs. Rahmati et al. [27] deployed multiple relaying UAVs to enhance the data rate between a base station and a user. Then, they maximized data flow of the constructed network by optimize UAV trajectories and transmit power. Lin et al. [28] formulated a maximum delay minimization problem for a postdisaster UAV network, and proposed an SDS-BSUM algorithm to optimize the transmit powers of all users. Moreover, Luan et al. [29] constructed a UAV-enabled MEC emergency network. To minimize the average subtask completion time, they used game theory to reconstruct the network topology and proposed a scheduling mechanism for subtask management. However, the absence of optimal traffic routing design in these works may result in data congestion and degraded network performance.

## D. Solution Mechanisms

Convex optimization is a widely used technique for solving optimization problems in UAV communications and networking. For example, Hu et al. [30] deployed a UAV as a relay to facilitate uplink communication between a group of disconnected APs and a remote BS. Then, they formulated an uplink throughput maximization problem and adopted successive convex approximation (SCA) to handle the corresponding subproblems by introducing auxiliary variables. Niu et al. [31] considered a distributed system consisting of multiple UAVs and mobile devices, both responsible for executing tasks offloaded from the control center, and proposed a convex optimizationbased decision algorithm to tackle the task scheduling problem. Zhang et al. [32] formulated a capacity maximization problem within a multi-UAV-enabled emergency communication network. Then, they decomposed the non-convex problem into two subproblems and used SCA as well as block coordinate update algorithm to handle them. However, not all optimization problems are suitable for solving with convex optimization. For example, some practical problems, such as UAV path planning, are non-convex. Transforming these non-convex problems into convex ones often involves complex mathematical transformations, which may not always be feasible or efficient in practice. Moreover, convex optimization cannot deal with complex and large-scale optimization problems.

Deep reinforcement learning (DRL) technique has also been widely used for handling optimization problems in disaster scenario. For example, Guan et al. [33] deployed multiple UAVs as relays to bridge links between mobile users in disaster area and BSs. They proposed a trajectory design mechanism based on the K-means strategy and multi-agent proximal policy optimization (PPO) algorithms to optimize overhead and improve deployment efficiency. Wan et al. [34] dispatched UAVs for disaster data collection considering the time-varying data value, and proposed an attention-based DRL scheme for multi-UAV scheduling. Moreover, Zhang et al. [35] deployed a UAV-mounted BS to collect data from ground users located in post-disaster area, and formulated a UAV trajectory design problem considering the available energy of ground users and obstacles. Specifically, they modeled the UAV as an agent, transformed the formulated problem into a constrained Markov decision-making process, and proposed a deep-Q-network-based algorithm to address the problem. However, rapid response is critical during post-disaster relief, especially in dynamic environments. The relatively long training time of DRL models may hinder their ability to provide timely responses.

In contrast to the works above, we propose a UAV-swarm enabled collaborative self-organizing network to establish links between a ground device in a post-disaster area and a remote AP. Then, we design the optimal multi-path traffic routing through theoretical analysis and optimize the communication network by using a heuristic-based algorithm, which enables efficient and robust data transmission in post-disaster areas.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, we present the architecture of the UAV-swarm enabled collaborative self-organizing network. Then, we introduce the communication model which contains VAA model, channel model, and transmission model. Finally, we formulate the optimization problem. Note that vectors and matrices are represented by bold lowercase and uppercase letters, respectively, and Table II summarizes the notations in this paper.

## A. Network Architecture

The architecture of the proposed UAV-swarm enabled collaborative self-organizing network for post-disaster communications is illustrated in Fig. 1. Specifically, it primarily consists of the following components:

TABLE II SUMMARY OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>a</td><td rowspan=1 colspan=1>The path loss component</td><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>The generalized adjacency matrix</td></tr><tr><td rowspan=1 colspan=1> $A$ </td><td rowspan=1 colspan=1>The rotor disc area</td><td rowspan=1 colspan=1> $\alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { 3 } , \alpha _ { 4 }$ </td><td rowspan=1 colspan=1>The weighting factors to balance the four propos-als of the transformed problem</td></tr><tr><td rowspan=1 colspan=1> $\alpha _ { \mathrm { s } }$ </td><td rowspan=1 colspan=1>The coefficient that controls the weight of theoriginal data and noise</td><td rowspan=1 colspan=1> $B$ </td><td rowspan=1 colspan=1>The channel bandwidth</td></tr><tr><td rowspan=1 colspan=1> $c$ </td><td rowspan=1 colspan=1>The speed of light</td><td rowspan=1 colspan=1> $\overline { { C _ { i , j } } }$ </td><td rowspan=1 colspan=1>The maximum capacity of link &lt;i,j &gt;â Îµ</td></tr><tr><td rowspan=1 colspan=1> $\underline { { c _ { i , j } } }$ </td><td rowspan=1 colspan=1>The residual capacity of link &lt;i,j &gt;âÎµ</td><td rowspan=1 colspan=1> $\overline { { c _ { \mathrm { r } } ( p _ { \mathrm { a } } ) } }$ </td><td rowspan=1 colspan=1>The residual capacity of the augmenting path</td></tr><tr><td rowspan=1 colspan=1> $\underline { { c _ { 1 } , c _ { 2 } } }$ </td><td rowspan=1 colspan=1>The learning coefficients</td><td rowspan=1 colspan=1> $c d _ { p }$ </td><td rowspan=1 colspan=1>The crowding distance of the pth agent</td></tr><tr><td rowspan=1 colspan=1>cd, cdsorted</td><td rowspan=1 colspan=1>The crowding distance vector of the populationand its sorted version,respectively</td><td rowspan=1 colspan=1> $D _ { u _ { 1 } , u _ { 2 } }$ </td><td rowspan=1 colspan=1>The distance between two UAVs u1 and u2 in the same swarm</td></tr><tr><td rowspan=1 colspan=1> $D _ { \mathrm { m i n } }$ </td><td rowspan=1 colspan=1>The threshold of the distance between two UAVsin the same swarm</td><td rowspan=1 colspan=1> $d _ { i , j } / H _ { i , j }$ </td><td rowspan=1 colspan=1>The total/vertical distance between nodes i and</td></tr><tr><td rowspan=1 colspan=1> $E _ { u } ^ { s }$ </td><td rowspan=1 colspan=1>The flight energy consumption of the uth UAVin the sth swarm</td><td rowspan=1 colspan=1> $F _ { s }$ </td><td rowspan=1 colspan=1>Thearray factor of the VAA formedby the sthUAV swarm</td></tr><tr><td rowspan=1 colspan=1> $f _ { \mathrm { c } }$ </td><td rowspan=1 colspan=1>Thecarrier frequency</td><td rowspan=1 colspan=1> $g$ </td><td rowspan=1 colspan=1>The gravitational acceleration</td></tr><tr><td rowspan=1 colspan=1> $G _ { s }$ </td><td rowspan=1 colspan=1>The antenna gain of the VAA of the sth swarm</td><td rowspan=1 colspan=1> $\overline { { G _ { i } } }$ </td><td rowspan=1 colspan=1>The antenna gain of node i</td></tr><tr><td rowspan=1 colspan=1> $G = \{ \nu , \varepsilon , \mathcal { W } \}$ </td><td rowspan=1 colspan=1>The directed weighted graph that describes thecommunication network</td><td rowspan=1 colspan=1> $G _ { \mathrm { r } }$ </td><td rowspan=1 colspan=1>The residual network of the original network G</td></tr><tr><td rowspan=1 colspan=1> $\overline { { G ^ { \prime } } }$ </td><td rowspan=1 colspan=1>The optimized network</td><td rowspan=1 colspan=1> $h _ { i , j }$ </td><td rowspan=1 colspan=1>The channel power gain between nodes iand j</td></tr><tr><td rowspan=1 colspan=1> $I _ { u } ^ { s }$ </td><td rowspan=1 colspan=1>The excitation current weight of the uth UAV inthe sth swarm</td><td rowspan=1 colspan=1> $i _ { \mathrm { u } }$ </td><td rowspan=1 colspan=1>The imaginary unit</td></tr><tr><td rowspan=1 colspan=1>1, P</td><td rowspan=1 colspan=1>Decision variables of the RPTRMOP.I, the exci-tation current weights,and P,the 3D positions</td><td rowspan=1 colspan=1> $\mathbf { m } _ { p } , \mathbf { m } _ { p } ^ { \mathrm { s o r t e d } }$ </td><td rowspan=1 colspan=1>The distance vector of the pth agent and its sortedversion,respectively</td></tr><tr><td rowspan=1 colspan=1> $m _ { u }$ </td><td rowspan=1 colspan=1>The mass of the uth UAV in the sth swarm</td><td rowspan=1 colspan=1> $m , n$ </td><td rowspan=1 colspan=1>Thechannel parametersof probabilityLoS model</td></tr><tr><td rowspan=1 colspan=1> $N _ { \mathrm { S } }$ </td><td rowspan=1 colspan=1>The total numberofUAV swarms</td><td rowspan=1 colspan=1> $N _ { \mathrm { U } }$ </td><td rowspan=1 colspan=1>ThenumberofUAVsineach swarm</td></tr><tr><td rowspan=1 colspan=1> $N _ { \mathrm { L } } / N _ { \mathrm { L } } ^ { \prime }$ </td><td rowspan=1 colspan=1>The number of communication linksin networkG/G&#x27;</td><td rowspan=1 colspan=1> $N _ { \mathrm { p o p } }$ </td><td rowspan=1 colspan=1>The population size</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { \mathrm { N } } } }$ </td><td rowspan=1 colspan=1>The number of neighbors of agents</td><td rowspan=1 colspan=1> $\overline { { N _ { \mathrm { P } } } }$ </td><td rowspan=1 colspan=1>The number of perturbed agents</td></tr><tr><td rowspan=1 colspan=1>p</td><td rowspan=1 colspan=1>The phase constant</td><td rowspan=1 colspan=1> $\overline { { P _ { i } } }$ </td><td rowspan=1 colspan=1>The transmit power of node i</td></tr><tr><td rowspan=1 colspan=1>pt</td><td rowspan=1 colspan=1>The transmit power of a UAV or the device</td><td rowspan=1 colspan=1> $\overline { { P L _ { i , j } } }$ </td><td rowspan=1 colspan=1>The path loss between nodesi and j</td></tr><tr><td rowspan=1 colspan=1>P</td><td rowspan=1 colspan=1>The blade profile power</td><td rowspan=1 colspan=1> $\overline { { P _ { \mathrm { I } } } }$ </td><td rowspan=1 colspan=1>The induced power in hovering status</td></tr><tr><td rowspan=1 colspan=1> $\mathbb { P } _ { i , j } ^ { \mathrm { L o S } } / \mathbb { P } _ { i , j } ^ { \mathrm { N L o S } }$ </td><td rowspan=1 colspan=1>The LoS/NLoS probability between nodes i andi</td><td rowspan=1 colspan=1> $p _ { \mathrm { a } }$ </td><td rowspan=1 colspan=1>The augmenting path in the residual network Gr</td></tr><tr><td rowspan=1 colspan=1> $p _ { \operatorname* { m a x } } / p _ { \operatorname* { m i n } }$ </td><td rowspan=1 colspan=1>The maximum/minimum proportion of the per-turbed agents</td><td rowspan=1 colspan=1> $\mathbf { q } _ { \mathrm { d } } / \mathbf { q } _ { \mathrm { a } } / \mathbf { q } _ { u } ^ { s }$ </td><td rowspan=1 colspan=1>The locations of the ground device/the AP/theuth UAV in the sth swarm</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathbb { R } _ { s } ^ { 3 } } }$ </td><td rowspan=1 colspan=1>The movement area of UAVs in the sth swarm</td><td rowspan=1 colspan=1> $\overline { { R _ { i , j } } }$ </td><td rowspan=1 colspan=1>The transmission rate between nodes i and j</td></tr><tr><td rowspan=1 colspan=1> $s , \rho$ </td><td rowspan=1 colspan=1>The air density and rotor solidity,respectively</td><td rowspan=1 colspan=1> $\overline { { \boldsymbol { S } _ { s } } }$ </td><td rowspan=1 colspan=1>The sthUAV swarm</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>The number of maximum iterations</td><td rowspan=1 colspan=1>u</td><td rowspan=1 colspan=1>The set of all UAV swarms</td></tr><tr><td rowspan=1 colspan=1> $\underline { { v _ { \mathrm { b } } } }$ </td><td rowspan=1 colspan=1>The tip speed of the rotor blade</td><td rowspan=1 colspan=1> ${ \underline { { v _ { \mathrm { m } } } } }$ </td><td rowspan=1 colspan=1>The mean rotor induced velocity in hovering</td></tr><tr><td rowspan=1 colspan=1> $v _ { u }$ </td><td rowspan=1 colspan=1>The velocity of the uth UAV in the sth swarm</td><td rowspan=1 colspan=1> $w ( \theta , \phi )$ </td><td rowspan=1 colspan=1>The magnitude of the far-field beam pattern of aUAV</td></tr><tr><td rowspan=1 colspan=1> $\omega$ </td><td rowspan=1 colspan=1>The inertia weight</td><td rowspan=1 colspan=1> $\mathbf { x } _ { i } , \mathbf { v } _ { i } , f _ { i }$ </td><td rowspan=1 colspan=1>Theposition,velocity,and objective functionvalue of the ith agent,respectively</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { x } _ { \mathrm { p b e s t } , i } ,$  $f _ { \mathrm { p b e s t } , i }$ </td><td rowspan=1 colspan=1>The position and objective function value of thepersonal optima of the ith agent, respectively</td><td rowspan=1 colspan=1> $\mathbf { x } _ { \mathrm { g b e s t } } , f _ { \mathrm { g b e s t } }$ </td><td rowspan=1 colspan=1>The position and objective function value of theglobal optima</td></tr><tr><td rowspan=1 colspan=1> $\mathbf { z } _ { \mathrm { s } }$ </td><td rowspan=1 colspan=1>The noise sampled from normal distribution</td><td rowspan=1 colspan=1>å¥</td><td rowspan=1 colspan=1>Thecarrierwavelength</td></tr><tr><td rowspan=1 colspan=1> $\overline { { ( \theta _ { r } , \phi _ { r } ) } }$ </td><td rowspan=1 colspan=1>The direction of a receiver</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>The efficiency of a VAA</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \eta ^ { \mathrm { L o S } } / \eta ^ { \mathrm { N L o S } } } }$ </td><td rowspan=1 colspan=1>The attenuation factors for LoS/NLoS links</td><td rowspan=1 colspan=1> $\overline { { \sigma ^ { 2 } } }$ </td><td rowspan=1 colspan=1>The noise power</td></tr></table>

<!-- image-->  
Fig. 1. A UAV-swarm enabled collaborative self-organizing network for postdisaster communications.

A ground device in the post-disaster area which urgently needs to establish a communication link with external equipments to send distress signals.

- A remote AP located outside the post-disaster area. Specifically, the AP enables the trapped devices to transmit urgent information and restore communication links with the external areas.

- A UAV network comprising multiple UAV swarms, denoted as $\mathcal { U } = \{ S _ { 1 } , S _ { 2 } , . . . , S _ { N _ { \mathrm { S } } } \}$ . These UAV swarms are =deployed over different spots of the post-disaster area to execute disaster missions, such as relaying data between devices and the remote AP. Each UAV swarm, denoted as $\mathcal { S } _ { s } = \{ 1 , 2 , . . . , N _ { \mathrm { U } } \}$ , is controlled by a ground rescue team = 1 2for ease of management.

- A high-altitude platform (HAP), serving as an essential coordination hub in LAE, which is responsible for executing algorithms and generating control strategies based on its powerful computational capabilities. These strategies are used to adjust system parameters such as positions of UAVs, to enhance system performance. The motivation for the use of HAP in this manuscript includes centralized control and global optimization [36], [37], extend coverage and improve communication efficiency, and improve network robustness and reliability. Note that the HAP does not participate in data transmission.

<!-- image-->  
Fig. 2. An example illustrating the mapping of the association relationship among components in the network and the adjacency matrix. (a) A twodimensional sketch map of a simple self-organizing network on the ground. (b) The adjacency matrix of the self-organizing network.

Due to long distances, obstacles, not any pairs of the ground device, multiple UAV swarms, and the AP can establish a communication link. In this case, we introduce the generalized adjacency matrix A to record the connectivity relationships among the communication components. Specifically, the mapping of a UAV network and its adjacency matrix is shown in Fig. 2. Accordingly, the working mechanism of the network for data transmission is described as follows.

1) The ground device searches A and transmits data to all neighbors with which it can establish a link, by using a time division multiple access (TDMA) method.

2) If the receiver is the AP, the data transmission will stop. Otherwise, if a UAV swarm receives the data, it will search A and forward the received data to its neighbors by using the TDMA approach.

3) The transmission process will terminate once upon the AP receives all the intended data from different links.

During the data forwarding process, it is assumed that a single UAV within the swarm receives the data and forwards it to other UAVs in the swarm for transmission.

We consider a three-dimensional (3D) Cartesian coordinate system, where the locations of the ground device, the AP, and the uth UAV in $ { \boldsymbol { S } } _ { s }$ are $\begin{array} { r } { \mathbf { q } _ { \mathrm { d } } = [ x _ { \mathrm { d } } , y _ { \mathrm { d } } , z _ { \mathrm { d } } ] , \mathbf { q } _ { \mathrm { a } } = [ x _ { \mathrm { a } } , y _ { \mathrm { a } } , z _ { \mathrm { a } } ] , } \end{array}$ , and $\mathbf { q } _ { u } ^ { s } = [ x _ { u } ^ { s } , y _ { u } ^ { s } , z _ { u } ^ { s } ]$ = [ ] = [ ], respectively. Note that the locations of the = [ ]ground device and the AP are static, while the movement area of UAVs in $S _ { s }$ is confined in $\mathbb { R } _ { s } ^ { 3 }$ for ease of control.

## B. Communication Model

1) Virtual Antenna Array Model: The array factor (AF) is used to characterize the beam pattern of each VAA. Specifically, the AF of the VAA formed by UAVs in the sth UAV swarm is given by [38]:

$$
F _ { s } ( \theta , \phi ) = \sum _ { u = 1 } ^ { N _ { \mathrm { U } } } { I _ { u } ^ { s } \mathrm { e } ^ { i _ { \mathrm { u } } [ p ( x _ { u } ^ { s } \sin \theta \cos \phi + y _ { u } ^ { s } \sin \theta \sin \phi + z _ { u } ^ { s } \cos \theta ) ] } } ,\tag{1}
$$

where $i _ { \mathrm { u } }$ represents the imaginary unit, and $p = 2 \pi / \lambda$ denotes = 2the phase constant with Î» being the carrier wavelength.

Accordingly, through regarding the whole antenna array as a single directional antenna, the antenna gain $G _ { s }$ of the VAA formed by UAVs in the sth UAV swarm is given by [39]:

$$
G _ { s } = \frac { 4 \pi | F _ { s } ( \theta _ { r } , \phi _ { r } ) | ^ { 2 } w ( \theta _ { r } , \phi _ { r } ) ^ { 2 } } { \int _ { 0 } ^ { 2 \pi } \int _ { 0 } ^ { \pi } | F _ { s } ( \theta , \phi ) | ^ { 2 } w ( \theta , \phi ) ^ { 2 } \sin \theta d \theta d \phi } \eta ,\tag{2}
$$

where $( \theta _ { r } , \phi _ { r } )$ refers to the direction of the receiver. Moreover, $w ( \theta , \phi )$ )is the magnitude of the far-field beam pattern of each ( )UAV element, and Î· denotes the antenna array efficiency.

2) Channel Model: The network comprises three types of communication links, which are device-to-UAV swarm (groundto-air, G2A), UAV swarm-to-UAV swarm (air-to-air, A2A), and UAV swarm-to-AP (air-to-ground, A2G) links, respectively. To accurately model these diverse links, a probabilistic LoS model is used. Generally, the path loss between any two nodes i and j is as follows [40]:

$$
P L _ { i , j } = \left\{ \begin{array} { l l } { { ( K _ { \mathrm { o } } d _ { i , j } ) ^ { \alpha } \eta ^ { \mathrm { L o S } } , } } & { { \mathrm { L o S \ l i n k } } } \\ { { ( K _ { \mathrm { o } } d _ { i , j } ) ^ { \alpha } \eta ^ { \mathrm { N L o S } } , } } & { { \mathrm { n o n - L o S \ l i n k } , } } \end{array} \right.\tag{3}
$$

where $K _ { \mathrm { o } } = 4 \pi f _ { \mathrm { c } / } c$ is the path loss constant, $f _ { \mathrm { c } }$ refers to the carrier frequency and c is the speed of light. Moreover, $d _ { i , j }$ is the total distance between nodes i and j, and Î± is the path loss exponent. In addition, $\eta ^ { \mathrm { L o S } }$ and $\eta ^ { \mathrm { N L o S } }$ are attenuation factors for LoS and non-NLoS (NLoS) links, respectively. Accordingly, the A2A and G2A/A2G channel models are described as follows.

A2A Channel Model: Due to the unobstructed nature of the high-altitude environment, A2A links between aerial components are predominantly characterized by LoS propagation. Therefore, the channel power gain between nodes i and j, which establish A2A communication links, is given by:

$$
h _ { i , j } = \left( K _ { \mathrm { o } } d _ { i , j } \right) ^ { - \alpha } \left( \eta ^ { \mathrm { L o S } } \right) ^ { - 1 } .\tag{4}
$$

G2A/A2G Channel Model: G2A and A2G links are subject to both LoS and NLoS propagation due to potential obstacles in the ground environment and other factors. Specifically, the probability of a LoS link between nodes i and j is given by [41], [42]:

$$
\mathbb { P } _ { i , j } ^ { \mathrm { L o S } } = \frac { 1 } { 1 + m \exp { ( - n ( 1 8 0 / \pi \arcsin ( H _ { i , j } / d _ { i , j } ) - m ) ) } } ,\tag{) (5}
$$

where m and n are environment-dependent constants, and $H _ { i , j }$ represents the vertical distance between nodes i and j. Consequently, the probability of an NLoS link is $\mathbb { P } _ { i , j } ^ { \mathrm { N L o S } } = \dot { 1 } - \mathbb { P } _ { i , j } ^ { \mathrm { L o S } } .$

= 1Accordingly, the channel power gain between nodes i and j in G2A/A2G channel is given by:

$$
h _ { i , j } = ( K _ { \mathrm { o } } d _ { i , j } ) ^ { - \alpha } \left( \mathbb { P } _ { i , j } ^ { \mathrm { L o S } } \eta ^ { \mathrm { L o S } } + \mathbb { P } _ { i , j } ^ { \mathrm { N L o S } } \eta ^ { \mathrm { N L o S } } \right) ^ { - 1 } .\tag{6}
$$

3) Transmission Model: Given the VAA and channel models described above, the transmission rate $R _ { i , j }$ between nodes i and j is given by [43]:

$$
R _ { i , j } = B \log _ { 2 } \left( 1 + P _ { i } G _ { i } h _ { i , j } / \sigma ^ { 2 } \right) ,\tag{7}
$$

where B and $\sigma ^ { 2 }$ refer to the channel bandwidth and noise power, respectively. Moreover, $P$ denotes the transmit power of node i. If node i is the ground device, then $P = p _ { t }$ , where $p _ { \mathrm { t } }$ denotes the =transmit power of the ground device or a single UAV. Conversely, if node i represents the sth UAV swarm, then $P _ { i }$ is given by $\begin{array} { r } { P _ { i } = \sum _ { u = 1 } ^ { N _ { \mathrm { U } } } ( I _ { u } ^ { s } ) ^ { 2 } p _ { \mathrm { t } } } \end{array}$ . In addition, $G _ { i }$ is the antenna gain of node = ( )i, which is as follows:

$$
G _ { i } = \left\{ { 1 , \atop { G _ { s } , } } \right. \mathrm { n o d e ~ i ~ i s ~ t h e ~ g r o u n d ~ d e v i c e } \nonumber\tag{8}
$$

The routing efficiency of the entire network heavily depends on the data transmission capability between the nodes in the network. Therefore, the aforementioned calculation method forms the foundation for the following proposed routing strategy.

Note that the communications among UAVs within each UAV swarm are achieved by a time division multiple access (TDMA)-based channel access with ACK-NACK for reliability, complemented by periodic beaconing for awareness and a priority queuing system for conflict resolution. Given the short distances among UAVs within the same swarm and the predominantly LoS nature of the corresponding channels, the variation in transmission rates among UAVs is minimal and thus has a negligible impact on routing efficiency. Moreover, the frequency, time, and phase synchronization among UAVs are assumed to be ensured by the RFClock [44]. In addition, the decision-making process within each UAV swarm is achieved by the well-known Paxos algorithm [45].

## C. Energy Consumption Model

When the uth UAV in the sth swarm flies in a 2D plane with speed $v _ { u } .$ , the propulsion power consumption is as follows:

$$
\begin{array} { l } { { P ( v _ { u } ) = P _ { 0 } \left( 1 + \displaystyle \frac { 3 v _ { u } ^ { 2 } } { v _ { \mathrm { b } } ^ { 2 } } \right) + P _ { \mathrm { I } } \left( \sqrt { 1 + \displaystyle \frac { v _ { u } ^ { 4 } } { 4 v _ { \mathrm { m } } ^ { 4 } } } - \displaystyle \frac { v _ { u } ^ { 2 } } { 2 v _ { \mathrm { m } } ^ { 2 } } \right) ^ { 1 / 2 } } } \\ { { \displaystyle ~ + \displaystyle \frac { 1 } { 2 } d _ { 0 } \rho s A v _ { u } ^ { 3 } , } } \end{array}\tag{9}
$$

where $P _ { 0 }$ and $P _ { \mathrm { I } }$ are the blade profile power and induced power in hovering status, respectively. Moreover, $v _ { \mathrm { b } }$ and $v _ { \mathrm { m } }$ are the tip speed of the rotor blade and the mean rotor induced velocity in hovering, respectively. In addition, $d _ { 0 } , \rho , s ,$ , and A are the fuselage drag ratio, air density, rotor solidity, and rotor disc area, respectively. Accordingly, for the uth UAV in the sth swarm with a 3D trajectory $\mathbf { q } _ { u } ( t )$ , its energy consumption is given by [46]:

$$
\begin{array} { r l r } {  { E _ { u } ^ { s } ( \mathbf { q } _ { u } ^ { s } ( t ) ) \approx \int _ { 0 } ^ { T } P ( v _ { u } ( t ) ) d t + \frac { 1 } { 2 } m _ { u } ( v _ { u } ( T ) ^ { 2 } - v _ { u } ( 0 ) ^ { 2 } ) } } \\ & { } & { + m _ { u } g ( h ( T ) - h ( 0 ) ) , \quad \quad ( 1 0 } \end{array}\tag{0}
$$

where $m _ { u }$ and $g$ represent the mass of the uth UAV and gravitational acceleration, respectively. Moreover, $T$ is the flight time of the UAV. Accordingly, the flight energy consumption of the whole system is $\begin{array} { r } { E = \sum _ { s = 1 } ^ { N _ { \mathrm { S } } } \sum _ { u = 1 } ^ { N _ { \mathrm { U } } } E _ { u } ^ { s } } \end{array}$

## D. Problem Formulation

In post-disaster areas, critical data such as rescue requests, health information, and situational reports must be delivered to remote base stations or APs timely. Moreover, communication opportunities may be brief in post-disaster areas due to the environmental challenges and the mobility of UAVs, etc. In this case, to guarantee that the urgent data can be relayed promptly and reduce the risk of data loss, we formulate an RPTRMOP aimed at maximizing the data transmission rate $R _ { d , a }$ between the ground device and the AP. Accordingly, the RPTRMOP is given by:

$$
\operatorname* { m a x } _ { { \bf { I } } , { \bf { P } } } R _ { d , a } ,\tag{11a}
$$

$$
\mathrm { s . t . } C 1 : 0 \leq { I _ { u } ^ { s } } \leq 1 , \forall s \in \mathcal { U } , u \in \mathcal { S } _ { s } ,\tag{11b}
$$

$$
C 2 : [ x _ { u } ^ { s } , y _ { u } ^ { s } , z _ { u } ^ { s } ] \in \mathbb { R } _ { s } ^ { 3 } , \forall s \in \mathcal { U } , u \in \mathcal { S } _ { s } ,\tag{11c}
$$

$$
C 3 : D _ { u _ { 1 } , u _ { 2 } } \geq ( D _ { \operatorname* { m i n } } , \lambda / 2 ) , \forall u _ { 1 } , u _ { 2 } \in S _ { s } ,
$$

$$
C 4 : E \le E _ { \mathrm { t h } } ,\tag{11d}
$$

(11e)

where I and P are decision variables of the formulated RPTR-MOP, with I denoting the set of UAV excitation current weights, which is directly associated with the transmit power and P being the set of 3D placements of UAVs, respectively. Moreover, the constraint (11b) restricts the value of the excitation current weight of each UAV to $[ 0 ,$ 1], the constraint (11c) confines the 3D placements of UAVs in the sth swarm to a predefined area $\mathbb { R } _ { s } ^ { 3 }$ , and the constraint (11d) ensures that the distance between two UAVs in the sth swarm exceeds a specified threshold to avoid collisions. In addition, the constraint (11e) ensures the flight energy consumption of the entire system lower than the threshold $E _ { \mathrm { t h } }$ Â·

Though the structure is seemingly simple, the formulated RPTRMOP is intractable. The reason is that $R _ { d , a }$ cannot be expressed with a specific formula. On the one hand, optimizing $R _ { d , a }$ requires first determining the optimal multi-path traffic routing. However, the considered network has a mesh structure, which implies that the topologies among UAV swarms are complex, making the determination of the multi-path traffic routing for data transmission particularly challenging. On the other hand, even after the multi-path traffic routing is determined, the excitation current weights and positions of the UAVs within each swarm involved in data transmission must be optimized to achieve the optimal transmission rate for each communication link. Then, the optimal transmission rate between the ground device and the AP can be attained.

Given the aforementioned challenges, we propose a two-stage optimization approach to solve the formulated problem. In the first stage, the optimal multi-path traffic routing is obtained via theoretical analysis and an existing method. In the second stage, the network is optimized based on the routing derived from the first stage.

## IV. STAGE ONE: ROUTING DESIGN

In this section, we first derive the theoretical upper bound on the transmission rate of each link in the communication network. Then, we model the network as a directed weighted graph, and classify the formulated RPTRMOP as a maximum flow problem. Finally, we deduce the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the entire network by using an existing method.

## A. Derivation of Theoretical Upper Bound on the Transmission Rate of Each Communication Link

In this part, we show the theoretical upper bound on the transmission rate of each communication link in the network. Specifically, we first deduce the theoretical upper bound on the signal-to-noise ratio (SNR) of each communication link in the following lemma.

Lemma 1: Consider a collaborative system comprising $N _ { \mathrm { U } }$ UAVs that form a VAA. Let $\rho$ denote the SNR achieved by a single UAV transmission. Then, the maximum achievable SNR of the VAA system, denoted as $\rho _ { N _ { \mathrm { U } } } ,$ , is upper-bounded by:

$$
\rho _ { N _ { \mathrm { U } } } \leq N _ { \mathrm { U } } ^ { 2 } \rho ,\tag{12}
$$

where the equality holds under ideal beamforming conditions.

Proof: The proof follows from two key aspects. First, let $p _ { \mathrm { t } }$ denote the transmit power of a single UAV. When all UAVs operate at maximum excitation current weights, the total transmit power of a $\mathrm { \Delta V A A } \ P _ { \mathrm { t o t a l } }$ satisfies $\begin{array} { r } { P _ { \mathrm { t o t a l } } = \sum _ { u = 1 } ^ { N _ { \mathrm { U } } } p _ { \mathrm { t } } = N _ { \mathrm { U } } p _ { \mathrm { t } } } \end{array}$ = =Second, under ideal beamforming conditions, the array gain provides an additional factor of $N _ { \mathrm { U } }$ in received power due to coherent signals combining [47]. Consequently, the maximum achievable SNR of the VAA system is $\rho _ { N _ { \mathrm { U } } } = N _ { \mathrm { U } } \cdot N _ { \mathrm { U } } \rho =$ $N _ { \mathrm { { I 7 } } } ^ { 2 } \rho .$ =-

Based on Lemma 1, the theoretical upper bound on the transmission rate of each communication link in the network can be acquired in the following theorem.

Theorem 1: For a collaborative system with $N _ { \mathrm { U } }$ UAVs, let B denote the channel bandwidth, h the channel power gain, $p _ { \mathrm { t } }$ the transmit power of each UAV, and $\sigma ^ { 2 }$ the noise power. Then, the theoretical upper bound on the achievable transmission rate C is given by:

$$
C \leq B \log _ { 2 } \left( 1 + \frac { N _ { \mathrm { U } } ^ { 2 } p _ { \mathrm { t } } h } { \sigma ^ { 2 } } \right) .\tag{13}
$$

Proof: For a single UAV transmit data with power $p _ { \mathrm { t } } .$ the achieved SNR is $\rho = p _ { \mathrm { t } } h / \sigma ^ { 2 }$ . Based on Lemma 1, the =achieved SNR of a VAA system with $N _ { \mathrm { U } }$ UAVs is $\rho _ { N _ { \mathrm { U } } } =$ $N _ { \mathrm { U } } ^ { 2 } p _ { \mathrm { t } } h / \sigma ^ { 2 }$ =under ideal beamforming conditions. Thus, by applying the Shannon-Hartley theorem, the theoretical upper bound on the transmission rate of the VAA system is $C =$ B $ ' \log _ { 2 } ( 1 + N _ { \mathrm { U } } ^ { 2 } p _ { \mathrm { t } } h / \sigma ^ { 2 } )$ . -

log (1 + )We obtain the theoretical upper bound on the transmission rate of a VAA based on Lemma 1 and Theorem 1. Subsequently, the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the network are obtained.

## B. Multi-Path Traffic Routing Design

In this section, we first model the communication network as a directed weighted graph. Then, the formulated RPTRMOP is classified as a maximum flow problem. Finally, we obtain the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the network by using Ford-Fulkerson algorithm.

1) Graph Construction: The constructed network can be represented as a directed weighted graph $G = \{ \mathcal { V } , \mathcal { E } , \mathcal { W } \}$ , in which V denotes the set of all nodes in the network, E is the set of communication links among the nodes, and W specifies the capacity of each communication link in V. Specifically, the graph is constructed as follows:

a) Label Network Nodes: Each UAV swarm is treated as a distinct entity and labeled sequentially as $1 , 2 { , } . . . , N _ { \mathrm { S } }$ Moreover, the device and AP are represented by 0 and $N _ { \mathrm { S } } + 1$ , respectively. Therefore, the set of all nodes in the network, V, is constructed as

$$
\mathcal { V } = \{ 0 , 1 , 2 , . . . , N _ { \mathrm { S } } + 1 \} .\tag{14}
$$

b) Define the Connectivity among Nodes: The adjacency matrix A is used to represent the connectivity among the nodes in V. For each pair of nodes i and j in V, if $a _ { i , j } = 1$ (i.e., there is a link between nodes i and j), then $< i , j >$ is placed into the set of communication links $\mathcal { E }$ as follows:

$$
\mathcal { E }  < i , j > , \{ i , j \} \in \mathcal { V } , i \neq j .\tag{15}
$$

c) Calculate the Capacity of Each Communication Link: For each $< i , j > \in \mathcal { E }$ , calculate the maximum capacity $C _ { i , j }$ based on Theorem 1, which provides the theoretical upper bound on the transmission rate between nodes i and j. Then, $C _ { i , j }$ is put into the set of capacities W as follows:

$$
\mathcal { W }  C _ { i , j } , < i , j > \in \mathcal { E } , i \neq j .\tag{16}
$$

2) Problem Reformulation: Given the graph G above, the intractable problem formulated in (11a) can be reformulated as follows:

(17a)

$$
\begin{array} { r l } & { \displaystyle \operatorname* { m a x } _ { \mathbf { I } , \mathbf { P } } R _ { 0 , N _ { \mathrm { S } } + 1 } , } \\ & { \displaystyle \mathrm { s . t . } C 1 : \displaystyle \sum _ { < i , j > \in \mathcal { E } } R _ { i , j } - \displaystyle \sum _ { < j , k > \in \mathcal { E } } R _ { j , k } = 0 , } \\ & { \quad \quad \quad \forall j \in \mathcal { V } \backslash \{ 0 , N _ { \mathrm { S } } + 1 \} , } \\ & { \quad \quad \quad C 2 : 0 \leq R _ { i , j } \leq C _ { i , j } , \forall < i , j > \in \mathcal { E } , } \\ & { \quad \quad \quad ( 1 1 \mathrm { b } ) , ( 1 1 \mathrm { c } ) , ( 1 1 \mathrm { d } ) , ( 1 1 \mathrm { e } ) , } \end{array}\tag{17b}
$$

(17c)

where the constraint (17b) shows the assumption of balanced transmission rates for all UAV swarms. Moreover, the constraint (17c) ensures that the transmission rate of each link in E does not exceed the derived maximum capacity. Based on the architecture of the reformulated problem, we have the following theorem.

Theorem 2: The reformulated optimization problem in (17) is a typical maximum flow problem.

Proof: The analysis is conducted from three key aspects. First, the network is modeled as a directed weighted graph G, consistent with the structure of a maximum flow problem. Moreover, our objective is to maximize the transmission rate $R _ { 0 , N _ { \mathrm { S } } + 1 }$ between the ground device and the AP, corresponding to the goal of maximizing flow in a typical maximum flow problem. Finally, the constraint (17b) ensures balanced inflow and outflow at the UAV swarms, while the constraint (17c) limits the transmission rate of each link to its capacity. Both constraints are key conditions in a maximum flow problem.

Algorithm 1: Ford-Fulkerson Algorithm.   
Input: Directed weighted graph $G .$   
$/ \star$ Initialization stage $\star /$   
1 Initialize theoretical upper bound on the transmission   
rate of the network ${ \overline { { R } } } _ { 0 , N _ { \mathrm { S } } + 1 } = 0 ;$   
2for $< i , j > \in \mathcal { E }$ do   
3 $R _ { i , j } = 0 ;$   
4 $R _ { j , i } = 0 ;$   
/\* Update stage   
5 while there is a path $p _ { \mathrm { a } }$ in the residual network $G _ { r }$ do   
6 $c _ { r } ( p _ { \mathrm { a } } ) = \operatorname* { m i n } \{ c _ { r } ( i , j ) , < i , j > \in p _ { \mathrm { a } } \} ;$   
$/ /$ Computing the path capacity   
7 for each $< i , j > \in p _ { \mathrm { a } }$ do   
8 $R _ { i , j } = R _ { i , j } + c _ { r } ( p _ { \mathrm { a } } ) ;$   
9 $R _ { j , i } \mathop { = } - R _ { i , j } ;$   
10 $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 } = \overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 } + c _ { r } ( p _ { \mathrm { a } } ) ; ~ / /$ Updating the   
total transmission rate   
Output: $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$ and the optimized network $G ^ { \prime } .$

Thus, the reformulated problem is a typical maximum flow problem [40], [48].

Given the aforementioned property of the reformulated problem, the well-known Ford-Fulkerson algorithm is adopted to deal with it in the following.

3) Ford-Fulkerson Algorithm: Several existing methods can calculate the theoretical upper bound on the transmission rate $R _ { 0 , N _ { \mathrm { S } } + 1 }$ between the ground device and the AP [13], such as the Ford-Fulkerson algorithm, the Edmonds-Karp algorithm, and the Dinic Push-Relabel algorithm. Due to its simplicity, efficiency, and applicability to any network, the Ford-Fulkerson algorithm is adopted in this study. To enhance understanding of the algorithm, several technical terms are explained first, as detailed in [13], [49].

Definition 1. (Residual capacity): For a pair of nodes i and j in the network, the residual capacity of the link $< i , j >$ refers to the maximum additional transmission rate that can be pushed from i to j without exceeding the corresponding capacity $C _ { i , j }$ which is defined as $c _ { i , j } = C _ { i , j } - R _ { i , j }$

=Definition 2. (Reverse Link): Reverse link is a introduced virtual link. For a link $< i , j >$ with transmission rate $R _ { i , j } ,$ , a corresponding reverse link exists in the residual network from j to i, with a residual capacity $c _ { j , i } = R _ { i , j }$

=Definition 3. (Residual network): For an original network G, the residual network is $G _ { \mathrm { r } } = \{ \mathcal { V } , \mathcal { E } _ { \boldsymbol { r } } , \mathcal { W } _ { \boldsymbol { r } } \}$ , where $\mathcal { E } _ { r } = \mathcal { E } \cup$ $\mathcal { E } _ { a } .$ , with $\mathcal { E } _ { a } = \{ < j , i > | < i , j > \in \mathcal { E } , i \neq j \}$ =being the set of =reverse links, and ${ \mathcal { W } } _ { r }$ =is the set of residual capacities of links in ${ \mathcal { E } } _ { r }$

Definition 4. (Augmenting path): Given an original network G, an augmenting path $p _ { \mathrm { a } }$ is a path from 0 to $N _ { \mathrm { S } } + 1$ in the residual network $G _ { \mathrm { r } }$ + 1. The introduction of augmenting path can increase the total transmission rate from 0 to $N _ { \mathrm { S } } + 1$

Based on the definitions provided above, the main framework of the Ford-Fulkerson algorithm for solving the reformulated problem in (17) is outlined in Algorithm 1. The detailed steps are presented as follows:

a) Initialization: Set the transmission rate between 0 and $N _ { \mathrm { S } } + 1$ as 0. Moreover, set the transmission rate of each link $< i , j > \in \mathcal { E }$ in G and its reverse link $< j , i > \mathrm { t o } 0 .$

b) Augmented Path Finding: Check if there exists any augmenting path in the residual network $G _ { \mathrm { r } }$ . If a path $p _ { \mathrm { a } }$ is found, define the residual capacity of the path $c _ { r } ( p _ { \mathrm { a } } )$ as the minimum residual capacity of all links in $p _ { \mathrm { a } }$

c) Transmission Rate Update: For each link $< i , j >$ in $p _ { \mathrm { a } } .$ add the calculated path capacity $c _ { r } ( p _ { \mathrm { a } } )$ to the transmission rate $R _ { i , j }$ ( ). Simultaneously, adjust the transmission rate of the reverse link $R _ { j , i }$ by setting it to the negative of the updated $R _ { i , j }$ . Then, increment the total transmission rate $R _ { 0 , N _ { \mathrm { S } } + 1 } \mathrm { b y } \ c _ { r } ( p _ { \mathrm { a } } )$

( )d) Termination: Continue iterating through the second step until no further augmenting paths are found in $G _ { \mathrm { r } }$

After the algorithm is executed, the theoretical upper bound on the transmission rate of the network $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$ is obtained, accompanied by a optimized network $G ^ { \prime }$ . Specifically, $G ^ { \prime }$ is obtained by eliminating the nodes which no not need to execute any data receiving or forwarding tasks at all, along with the links whose transmission rates are zero. Akin to the structure of the original network G, the components in the optimized network $G ^ { \prime } = ( \mathcal { V } ^ { \prime } , \mathcal { E } ^ { \prime } , \mathcal { W } ^ { \prime } )$ is as follows:

$\mathcal { V } ^ { \prime } = \{ 0 , . . . , N _ { \mathrm { S } } ^ { \prime } , N _ { \mathrm { S } } ^ { \prime } + 1 \}$ contains the ground device, the $N _ { \mathrm { S } } ^ { \prime }$ = 0 + 1UAV swarms that participate in the data transmission, and the AP, subject to $\mathcal { V } ^ { \prime } \subseteq \mathcal { V }$

$$
\mathcal { E } ^ { \prime } = \{ < i , j > | R _ { i , j } \neq 0 o r R _ { j , i } \neq 0 \}
$$

$$
\mathcal { V } ^ { \prime }
$$

. $\mathcal { W } ^ { \prime } = \{ \overline { { R } } _ { i , j } | < i , j > \in \mathcal { E } ^ { \prime } \}$ represents the set of expected =transmission rate of each link in ${ \mathcal { E } } ^ { \prime }$

Intuitively, G
 provides the optimal multi-path traffic routing, rather than relying on a single route [50], [51]. The routing strategy enhances the post-disaster communications by establishing multiple routes to increase reliability and robustness against congestion, enabling parallel data transmission to improve throughput, and providing the adaptability needed to respond to dynamic network changes. In this way, the transmission rate for each link in each path corresponds to its optimal value. Fig. 3 provides a simple example illustrating the Ford-Fulkerson algorithm for calculating the theoretical upper bound on the transmission rate of a network, and demonstrates the relationships among the original, residual, and final optimized networks.

The computational complexity of the Ford-Fulkerson algorithm in our optimization problem is analyzed in the following theorem. Notably, since the Ford-Fulkerson algorithm guarantees the optimal maximum flow solution, the complexity analysis represents both the best case and worst case scenarios.

Theorem 3: Given that the number of links in the set $\mathcal { E }$ is $N _ { L }$ and the theoretical upper bound on the transmission rate of the system is $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$ , the Ford-Fulkerson algorithm achieves a computational complexity of $\mathcal { O } ( N _ { L } \overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 } )$ when solving the (maximum flow problem formulated in (17).

Proof: The complexity analysis is derived from the operation of the Ford-Fulkerson algorithm in this problem setting. The algorithm identifies augmenting paths iteratively using depth-first searches, where each path increases the flow value by at least one unit. Since the theoretical upper bound on the transmission rate is bounded by $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$ , the algorithm requires at most $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$ iterations to identify all augmenting paths. In each iteration, a depth-first search may traverse all $N _ { L }$ links in the set E , resulting in a per-iteration complexity of $\mathcal { O } ( N _ { L } ) \left[ 5 2 \right]$ . Therefore, the total ( )computational complexity is given by $\mathcal { O } ( N _ { L } \overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 } )$ -

<!-- image-->  
Fig. 3. An example illustrating the Ford-Fulkerson algorithms for calculating the theoretical upper bound on the transmission rate of a network and the optimal multi-path traffic routing. (a) The original network, where node 0 is the transmitter and the node 4 is the receiver. (b) A residual network of (a), where an augmenting path 0â 1 â4 exists, thus the current upper bound on the transmission rate is 1. (c) A residual network of (a), where an augmenting path $0 \to 3 \to 4$ exists, thus the current upper bound on the transmission rate is 2. (d) A residual network of (a) with no augmenting paths. (e) The final optimized network with an upper bound on the transmission rate of 2 and two corresponding paths.

( )Based on the theoretical analysis of the first stage, we obtain the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the network. In the following, the excitation current weight and placement of each participating UAV are designed to optimize the communication network, ensuring that the actual transmission rate approaches its theoretical upper bound, i.e., $\overline { { R } } _ { 0 , N _ { \mathrm { S } } + 1 }$

## V. STAGE TWO: UAV SWARM OPTIMIZATION

In this section, we first transform the formulated RPTRMOP into its penalty-based variant, V-RPTRMOP, and provide a detailed analysis of the V-RPTRMOP. Then, we propose an optimization method to solve the V-RPTRMOP effectively.

## A. Problem Transformation and Analysis

In this work, four Parts are considered when transforming the formulated RPTRMOP into a more tractable format, which are as follows:

Motivation I. Diminishing the gap between the actual and expected transmission rates of each communication link: To render the communication network closely align with the optimized network, the transmission rate $R _ { i , j }$ of the link $< i , j >$ should be closely approach its theoretical upper bound, i.e., $\overline { { R } } _ { i , j }$ . Accordingly, the sum of differences between the actual and expected transmission rates of all links should be minimized.

- Motivation II. Mitigating extreme cases: If only proposal I is considered, extreme situations may occur, where the differences between the actual and expected transmission rates for different links become excessively huge. For instance, with $\overline { { R } } _ { 1 , 2 } = 1 . 0 \times 1 0 ^ { 7 }$ bps and $\overline { { R } } _ { 1 , 3 } = 1 . 2 \times 1 0 ^ { 7 }$ bps, the result could lead to $R _ { 1 , 2 } = 1 \times 1 0 ^ { 6 }$ = 1bps and $R _ { 1 , 3 } =$ $1 . 2 \times 1 0 ^ { 7 }$ = 1 10 =bps. In this case, only the second link achieves an 1 2 10acceptable transmission rate, while the counterpart of the other link is not optimized at all. To avoid such extreme cases, standard deviation is introduced as a corrective measure.

Motivation III. Preventing communication network congestion: In the constructed communication network, UAV swarms are responsible for both receiving and transmitting data. If the actual transmission rate $R _ { i , j }$ falls below its theoretical upper bound $\overline { { R } } _ { i , j }$ , the achievable rate of the receiver j will be adversely affected, since it will not be able to transmit sufficient data, potentially leading to network congestion. To address this issue, a penalty mechanism is implemented. Specifically, the penalty term $\delta _ { i , j }$ of the link $< i , j > \in \mathcal { E }$ is given by:

$$
\delta _ { i , j } = \left\{ { 1 , \begin{array} { l l } { { \mathrm { i f } } R _ { i , j } < { \overline { { R } } } _ { i , j } } \\ { { \mathrm { 0 } } , } & { { \mathrm { i f } } R _ { i , j } \ge { \overline { { R } } } _ { i , j } . } \end{array} } \right.\tag{18}
$$

Motivation IV. Avoiding excessive flight energy consumption: Excessive energy consumption can significantly diminish the endurance of UAVs, thereby restricting their flight range and mission duration. Thus, an additional penalty term Î· is introduced to regulate flight energy consumption and extend UAV operational time, which is given by:

$$
\eta = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f } } E > E _ { \mathrm { t h } } } \\ { 0 , } & { { \mathrm { i f } } E \le E _ { \mathrm { t h } } . } \end{array} } \right.\tag{19}
$$

Based on the aforementioned considerations, the V-RPTRMOP is as follows:

$$
\begin{array}{c} \operatorname* { m i n } _ { { \bf l } , { \bf P } } f = \underbrace { \alpha _ { 1 } \sum _ { \langle i , j \rangle \in { \mathcal E } } | R _ { i , j } - \overline { { R } } _ { i , j } | } _ { \mathrm { P a r t I } } + \underbrace { \alpha _ { 2 } \sqrt { \sum _ { \langle i , j \rangle \in { \mathcal E } } \frac { | R _ { i , j } - \overline { { R } } _ { i , j } | ^ { 2 } } { N _ { \mathrm { L } } ^ { \prime } } } } _ { \mathrm { P a r t \bf I } }  \\ { + \underbrace { \alpha _ { 3 } \sum _ { \langle i , j \rangle \in { \mathcal E } } \delta _ { i , j } } _ { \mathrm { P a r t I I } } + \underbrace { \alpha _ { 4 } \eta } _ { \mathrm { p a r t N } } , } \\ { \mathrm { s . t . } ( 1 1 6 ) , ~ ( 1 1 \mathrm { e } ) , ~ } & { { ( 2 0 \mathrm { a } } } \end{array}
$$

where $\alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { 3 }$ , and $\alpha _ { 4 }$ are weighting factors to balance the four Parts. Moreover, $N _ { \mathrm { L } } ^ { \prime }$ is the number of communication links in the optimized network G
 . Due to the particularity of the post-disaster relief network, Parts III and IV are hard conditions items and their triggering should be minimized.

The aforementioned problem is a large-scale optimization problem due to the large number of decision variables and constraints, as well as the complexity of the objective function. First, the decision variables of the problem include the placement and excitation current weights of each UAV in swarms for relaying data. As a result, the number of decision variables increases rapidly as the network size expands, particularly when there are a large number of UAVs and links. Moreover, the number of constraints grows proportionally with the number of UAV swarms, communication links, and UAVs in each swarm. In addition, for large networks with numerous communication links, optimizing this objective function becomes computationally expensive. Therefore, given the significant number of decision variables, the constraints, and the computational complexity of the objective function, the transformed problem (20) is qualified as a large-scale optimization problem.

Then, we characterize the NP-hardness and non-convexity of the V-RPTRMOP in the following theorems.

Theorem 4: The problem in (20) is NP-hard since it is a nonlinear multi-dimensional 0-1 knapsack problem.

Proof: For simplicity, we assume the placement of each UAV is pre-designed and fixed. In this case, the excitation current weights for all UAVs I become the exclusive decision variable. Accordingly, the V-RPTRMOP is as follows:

$$
\operatorname* { m i n } _ { \mathbf { I } } \ f ,\tag{21a}
$$

$$
\mathrm { s . t . } C 1 : I _ { u } ^ { s } \in \{ 0 , 1 \} , \forall s \in \mathcal { U } , u \in \mathcal { S } _ { s } ,\tag{21b}
$$

$$
C 2 : \sum _ { u = 1 } ^ { N _ { \mathrm { U } } } I _ { u } ^ { s } < N _ { \mathrm { U } } , \forall s \in \mathcal { U } , u \in \mathcal { S } _ { s } .\tag{21c}
$$

It is shown that the simplified V-RPTRMOP is a nonlinear multi-dimensional 0-1 knapsack problem which has shown to be a typical NP-hard problem [53]. Thus, the simplified V-RPTRMOP is NP-hard, and the V-RPTRMOP is also proven to be NP-hard accordingly. -

Theorem 5: The transformed problem in (20) is non-convex since each Part of the objective function in (20a) is non-convex.

Proof: The objective function of the V-RPTRMOP consists of four Parts. In Part I, the absolute value function $| R _ { i , j } - \overline { { R } } _ { i , j }$ is non-convex since it is not differentiable at $R _ { i , j } = \overline { { R } } _ { i , j }$ . Moreover, the square root function $\begin{array} { r } { \sqrt { \sum _ { \langle i , j \rangle \in { \mathcal E } } | R _ { i , j } - \overline { { R } } _ { i , j } | ^ { 2 } / N _ { \mathrm { L } } ^ { \prime } } } \end{array}$ in Part II is non-linear and concave. Finally, the penalty terms $\delta _ { i , j }$ and Î· in Parts III and IV take values of either 0 or 1, making them discontinuous. Therefore, as all four Parts of the objective function are non-convex, the overall objective function in (20a) is non-convex. Consequently, the transformed problem in (20) is non-convex as well.

For the V-RPTRMOP, which is large-scale, NP-hard, and nonconvex, potential solution methods include convex optimization, DRL, and heuristic algorithms. However, due to the complexity of the objective function and constraints, it is impractical to convert the problem into a convex optimization problem. Therefore, convex optimization is not suitable for solving the V-RPTRMOP. Moreover, DRL models require extensive training time and incur significant overhead, rendering them unsuitable for rapidly changing post-disaster environments. Given these limitations, heuristic algorithms, commonly used for optimization problems involving beamforming techniques [54], [55], present a feasible solution, which motivate us to propose a heuristic algorithm to solve the V-RPTRMOP.

Algorithm 2: DM-PSO.   
Input: Population size $N _ { \mathrm { p o p } } ,$ number of maximum   
iterations $T _ { \mathrm { m a x } } ,$ objective function $f .$   
$/ \star$ Initialization stage   
1 Initialize the position of the global best agent,   
$\mathbf { x } _ { \mathrm { g b e s t } } = \boldsymbol { \mathcal { D } } ,$ ,and its corresponding value, $f _ { \mathrm { g b e s t } } = \mathcal { O } ;$   
2 for $i = 1$ to $N _ { \mathrm { p o p } }$ do   
population   
3 Initialize position $\mathbf { x } _ { i }$ and velocity $\mathbf { v } _ { i }$ of the i-th   
agent;   
4 Calculate the objective function value $f _ { i }$ of $\mathbf { x } _ { i } ;$   
5 $\begin{array} { r } { \mathbf { x } _ { \mathrm { p b e s t } , i } = \mathbf { x } _ { i } , f _ { \mathrm { p b e s t } , i } = f _ { i } ; } \end{array}$   
6 $f _ { i } < f _ { \mathrm { g b e s t } }$ then $/ /$ Updating global best   
7 $\mathbf { x } _ { \mathrm { g b e s t } } = \mathbf { x } _ { i } , f _ { \mathrm { g b e s t } } = f _ { i } ;$   
8for $t = 1$ to $T _ { \mathrm { m a x } }$ do   
/\* Evolutionary stage   
9 for $i = 1$ to $N _ { \mathrm { p o p } }$ do // Updating agents   
based on conventional PSO   
10 Update $\mathbf { x } _ { i }$ and $\mathbf { v } _ { i }$ of the i-th agent based on   
Eqs.(22) and (23);   
11 Calculate the objective function value $f _ { i }$ of $\mathbf { x } _ { i } ;$   
12 if $f _ { i } < f _ { \mathrm { p b e s t } , i }$ then   
13 $\begin{array} { r } { \mathbf { x } _ { \mathrm { p b e s t } , i } = \mathbf { x } _ { i } , f _ { \mathrm { p b e s t } , i } = f _ { i } ; } \end{array}$   
14 $\mathbf { i f } \ f _ { \mathrm { p b e s t } , i } < f _ { \mathrm { g b e s t } }$ then   
15 $\mathbf { x } _ { \mathrm { g b e s t } } = \mathbf { x } _ { i } , f _ { \mathrm { g b e s t } } = f _ { i } ;$   
/\* Diffusion stage   
16 XâPerturbatior $\mathrm { \Delta } ( N _ { \mathrm { p o p } } , T _ { \mathrm { m a x } } ) ; \mathrm { \Delta } / /$ Executing   
perturbation utilizing Algorithm 3   
Output: Position of the global best agent, $\mathbf { x } _ { \mathrm { g b e s t } } ,$ and   
its corresponding value, $f _ { \mathrm { g b e s t } } .$

## B. Diffusion Model-Enabled Particle Swarm Optimization

Traditional PSO is highly effective in exploitation, refining solutions by iteratively updating the positions of particles based on their individual and global best positions. However, it often faces challenges in exploration, particularly in high-dimensional solution spaces. Diffusion models (DM) excel at exploring the solution space by generating diverse potential candidates, thereby enhancing global exploration. Thus, a DM-PSO is proposed to tackle the transformed V-RPTRMOP, which couples the exploitation efficiency of PSO and the exploration strength of diffusion models. Specifically, the main framework of the proposed algorithm is presented in Algorithm 3, and the key steps are described as follows:

a) Initialization Stage: Initialize the velocity and position of each agent randomly, and calculate the objective function value for position of each agent. Then, update the global and local bests based on the obtained objective function values.

b) Update Stage: During each iteration, the velocity $\mathbf { v } _ { i }$ of the ith agent is updated as follows [56]:

$$
\mathbf { v } _ { i } = \omega \mathbf { v } _ { i } + c _ { 1 } r _ { 1 } ( \mathbf { x } _ { \mathrm { p b e s t } , i } - \mathbf { x } _ { i } ) + c _ { 2 } r _ { 2 } ( \mathbf { x } _ { \mathrm { g b e s t } } - \mathbf { x } _ { i } ) ,\tag{22}
$$

where $\omega$ is the inertia weight, $c _ { 1 }$ and $c _ { 2 }$ refer to the learning coefficients, $r _ { 1 }$ and $r _ { 2 }$ are random numbers, subject to (0,1). Moreover, $\mathbf { x } _ { \mathrm { p b e s t } , i }$ and $\mathbf { x } _ { \mathrm { g b e s t } }$ represent the locations of personal and global best agents, respectively.

```powershell
Algorithm 3: Diffusion-Enabled Perturbation Scheme.
Input: Population size $N _ { \mathrm { p o p } } ,$ positions $\mathbf { x , }$ number of
neighbors $N _ { \mathrm { N } } ,$ ,maximumiterations $T _ { \mathrm { m a x } } ,$
maximum $p _ { \mathrm { m a x } }$ and minimum $p _ { \mathrm { m i n } }$
proportion of perturbed agents.
1 Initialize crowding distance vector cd $= \mathcal { D } ;$
2 for $p = 1$ to $N _ { \mathrm { p o p } }$ do // Calculating the
crowding distance of each agent
3 Calculate distance vector $\mathbf { m } _ { p }$ for the pth agent;
4 Sort $\mathbf { m } _ { p }$ into $\mathbf { m } _ { p } ^ { \mathrm { s o r t e d } }$ in ascending order;
5 Select $N _ { \mathrm { N } }$ closest neighbors as $\sigma _ { 1 } , . . . , \sigma _ { N _ { \mathrm { N } } } ;$
6 Compute crowding distance $c d _ { p }$ using Eq. (24);
7 Update cd â cd $\cup c d _ { p } ;$
8 Sort cd into $\mathbf { c d } ^ { \mathrm { s o r t e d } }$ in ascending order;
9 Compute the number of perturbed agents $N _ { \mathrm { P } }$ using
Eq. (25);
10 Select the first $N _ { \mathrm { P } }$ agents in $\mathbf { c d } ^ { \mathrm { s o r t e d } }$ as $\mu _ { 1 } , . . . \mu _ { N _ { \mathrm { P } } } ;$
11 for $p = 1$ to $N _ { \mathrm { P } }$ do $/ /$ Executing
perturbation to the $N _ { \mathrm { P } }$ agents
12 Add noise to position $\mathbf { x } _ { \mu _ { p } }$ of the $\mu _ { p }$ th agent using
Eq. (26);
Output: Updated positions x.
```

According to the obtained $\mathbf { v } _ { i }$ , the position $\mathbf { x } _ { i }$ of the ith agent is updated as follows:

$$
\mathbf { x } _ { i } = \mathbf { x } _ { i } + \mathbf { v } _ { i } .\tag{23}
$$

c) Diffusion Stage: To avoid premature convergence and maintain the diversity of agents, we introduce a diffusion-enabled perturbation scheme. Specifically, the framework is outlined in Algorithm 3 and the details are as follows:

Crowding distance calculation: First, for the pth agent, the scheme calculates $\mathbf { m } _ { p } = \{ d _ { p , 1 } , . . . , d _ { p , N _ { \mathrm { p o p } } } \}$ which contains the =euclidean distances from the pth agent to other agents. Second, the scheme sorts the distance vector $\mathbf { m } _ { p }$ into $\mathbf { m } _ { p } ^ { \mathrm { s o r t e d } } =$ $\{ d _ { p , \sigma _ { 1 } } , . . . , d _ { p , \sigma _ { N _ { \mathrm { p o p } } } } \}$ in ascending order. Third, the first $N _ { \mathrm { N } }$ agents denoted as $\sigma _ { 1 } , . . . , \sigma _ { N _ { \mathrm { N } } }$ are selected as the neighbors of the pth agent. Finally, the crowding distance of the pth agent is calculated as follows:

$$
c d _ { p } = \sum _ { j = 1 } ^ { N _ { \mathrm { N } } } d _ { p , \sigma _ { j } } / N _ { \mathrm { N } } .\tag{24}
$$

Then, $c d _ { p }$ is put into the crowding distance vector cd. Finally, the scheme sorts cd into $\mathbf { c d } ^ { \mathrm { { s o r t e d } } }$ in ascending order.

Agent position perturbation: First, the number of perturbed agents $N _ { \mathrm { P } }$ is calculated as follows:

$$
N _ { \mathrm { P } } = N _ { \mathrm { p o p } } \left[ p _ { \mathrm { m a x } } - ( p _ { \mathrm { m a x } } - p _ { \mathrm { m i n } } ) t / T _ { \mathrm { m a x } } \right] .\tag{25}
$$

Second, the first $N _ { \mathrm { P } }$ agents in cd $\mathrm { s o r t e d }$ , corresponding to those with the smallest crowding distances, are selected for perturbation. These agents are denoted as $\mu _ { 1 } , . . . . , \mu _ { N _ { \mathrm { P } } }$ . Third, perturbation is conducted by fine-tuning the forward process of the diffusion model. Specifically, for each of the selected agents $\mu _ { p } \left( \mathrm { f o r } p = 1 , . . . , N _ { \mathrm { P } } \right)$ , noise is added to their current position $\mathbf { x } _ { \mu _ { p } }$ at each time step as follows:

$$
\begin{array} { r } { \mathbf { x } _ { \mu _ { p } } = \sqrt { \alpha _ { \mathrm { s } } } \mathbf { x } _ { \mu _ { p } } + \sqrt { 1 - \alpha _ { \mathrm { s } } } \mathbf { z } _ { \mathrm { s } } , \mathbf { z } _ { \mathrm { s } } \sim \mathcal { N } ( 0 , I ) , } \end{array}\tag{26}
$$

where $\alpha _ { \mathrm { s } }$ is a coefficient that controls the weight of the original data and noise, and $\mathbf { z } _ { \mathrm { s } }$ is noise sampled from normal distribution. Based on this, the updated x is obtained.

Once upon $T _ { \mathrm { m a x } }$ is reached, the DM-PSO is suspended, and the position $\mathbf { x } _ { \mathrm { g b e s t } }$ along with the objective function value $f _ { \mathrm { g b e s t } }$ of the global best are obtained. Otherwise, the proposed algorithm continues as scheduled.

Given the aforementioned general framework of the DM-PSO, we analyze the computational complexity of the algorithm in the following theorem.

Theorem 6: The complexity of the proposed DM-PSO is $\mathcal { O } ( T _ { \mathrm { m a x } } ( N _ { \mathrm { L } } ^ { \prime } N _ { \mathrm { U } } N _ { \mathrm { p o p } } + N _ { \mathrm { p o p } } ^ { 2 } \log N _ { \mathrm { p o p } } ) )$

( ( + log ))Proof: See Appendix A of the supplemental material, available online.

## VI. SIMULATION RESULTS

In this section, we execute simulations to show the advantages of deploying a UAV-swarm enabled collaborative selforganizing network to assist post-disaster communications, and validate the performance of the proposed two-stage optimization approach in solving the formulated RPTRMOP.

## A. Simulation Setup

1) Scenario Setup: In this work, the locations of the ground device and the remote AP are set at (0, 4500, 0) m and (12000, 4500, 0) m, respectively. Moreover, we consider two cases where the numbers of UAV swarms are 4 and 8, respectively, with each swarm consisting of 8 UAVs. Note that the number of UAVs in each swarm can be generalized to be different. In addition, the movement area of UAVs in each swarm is defined as 100 m $\times ~ 1 0 0 \mathrm { { m } }$ , and the altitude of each UAV is constrained to [100, 120] m [57].

2) Parameter Setting: The wavelength Î», frequency $f _ { \mathrm { c } } ,$ path loss exponent Î±, bandwidth $B ,$ noise power spectral density, and transmit power of the ground device or a single $\mathrm { U A V } _ { \mathit { p } _ { t } }$ are 0.33 m, 0.9 GHz [58], 2 [59], 2 MHz [57], â157 dBm/Hz [60], and 0.1 W [61], respectively. The threshold of the distance between any two UAVs in the same swarm $D _ { \mathrm { m i n } }$ is 0.5 m. Moreover, the value of $\eta ^ { \mathrm { L o S } }$ in the A2A channel model is set to 1, while the parameters for the G2A/A2G channel model, $\mathrm { i . e . , ~ } m , ~ n , ~ \eta ^ { \mathrm { L o S } }$ , and $\eta ^ { \mathrm { N L o S } }$ , are set to 4.88, 0.43, 0.977, and 0.00974 [62], respectively.

The weighting factors of the transformed V-RPTRMOP $\alpha _ { 1 }$ $\alpha _ { 2 } , \alpha _ { 3 }$ , and $\alpha _ { 4 }$ are $1 , 1 , 2 \times 1 0 ^ { 7 }$ , and $2 \times 1 0 ^ { 7 }$ , respectively. Note that the values of $\alpha _ { 3 }$ 2and $\alpha _ { 4 }$ are set to be relatively large since the corresponding Parts III and IV represent hard constraints. Moreover, the population size $N _ { \mathrm { p o p } } .$ the maximum number of iterations $T _ { \mathrm { m a x } }$ , inertia weight Ï, and learning coefficients $c _ { 1 }$ and $c _ { 2 }$ are set as 100, 500, 1, 1.5, and 2, respectively. In addition, the number of agent neighbors $N _ { \mathrm { N } }$ , the maximum and minimum proportion of the perturbed agents $p _ { \mathrm { m a x } }$ and $p _ { \mathrm { m i n } }$ are 10, 0.3 and 0.1, respectively.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(cï¼

Fig. 4. The communication networks in different stages for case 1. (a) The communication network in the first stage after deducing the theoretical upper bound on the transmission rate of each link. (b) The optimized network in the first stage after conducting Ford-Fulkerson algorithm, with the theoretical upper bound on the transmission rate of the whole network is 4.48 Ã 106 bps. (c) The actual communication network in the second stage after UAV swarm optimization by DM-PSO, with the actual transmission rate of the whole network is 4.48 Ã 106 bps.  
<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(cï¼  
Fig. 5. The communication networks in different stages for case 2. (a) The communication network in the first stage after deducing the theoretical upper bound on the transmission rate of each link. (b) The optimized network in the first stage after conducting Ford-Fulkerson algorithm, with the theoretical upper bound on the transmission rate of the whole network is 7.64 Ã 106 bps. (c) The actual communication network in the second stage after UAV swarm optimization by DM-PSO, with the actual transmission rate of the whole network is 7.64 Ã 106 bps.

## B. Performance Evaluation

1) Visualization Results of the Proposed Two-Stage Optimization Approach: Figs. 4 and 5 illustrate the communication networks in different stages for the considered two cases. First, compared with the constructed network shown in Figs. 4(a) and 5(a), several links and UAV swarms are excluded from the data transmission process in Figs. 4(b) and 5(b). On the one hand, eliminating redundant communication links reduces the waste of communication resources. On the other hand, UAV swarms that do not participate in the whole data transmission process can execute other relief missions in the post-disaster area, significantly enhancing the efficiency of disaster relief. Second, the optimized transmission rates of several links in Figs. 4(b) and 5(b) are lower than their theoretical upper bounds, indicating that UAVs are not always required to operate at maximum transmission power when transmitting data, which also helps conserve their limited resources. Finally, it can be observed from Figs. 4(c) and 5(c) that the transmission rate of each communication link is well optimized, ensuring no congestion occurs. Moreover, the difference between the actual transmission rates of the communication links in Fig. 4(c) and the expected rates in Fig. 4(b) is minimal, and the actual transmission rate of the whole network closely aligns with the theoretical upper bound, which can be attributed to the first three proposals of V-RPTRMOP in Section V. Note that this analysis also applies to Fig. 5.

In conclusion, the proposed two-stage optimization approach can efficiently optimize the transmission rate of the entire network and is resource-friendly for post-disaster communications.

2) Comparison of Multi-Path Traffic Routing Design With Other Existing Protocols: To evaluate the proposed multi-path traffic routing design, several existing routing protocols are used as benchmarks, detailed as follows:

Routing Information Protocol (RIP): A distance-vector routing protocol that selects the path with the fewest hops as the optimal routing [63].

Open Shortest Path First (OSPF): A link-state protocol which uses the Dijkstra algorithm to determine the multi-path traffic routing from the ground device to the AP [64].

- Greedy Perimeter Stateless Routing (GPSR): A locationbased protocol where each node selects the neighbor closest to the location of AP as the next hop [65].

- Zone Routing Protocol (ZRP): A hybrid protocol that defines areas by hop count, using proactive routing within zones and on-demand routing between them [66].

<!-- image-->  
(a) Case 1

<!-- image-->  
(b) Case 2  
Fig. 6. Theoretical upper bound on the transmission rate of the whole network obtained by several existing routing protocols and the proposed multi-path traffic routing method for the two cases.

Temporally Ordered Routing Algorithm (TORA): An ondemand routing protocol for dynamic networks, where each node selects the neighbor with the lowest height value as the next hop [67].

As shown in Fig. 6, there is a clear performance hierarchy, with GPSR and ZRP performing the worst among the adopted protocols. Moreover, RIP, OSPF, and TORA demonstrate better performance than GPSR and ZRP, however, their theoretical upper bounds on transmission rates remain unsatisfactory. Finally, the proposed multi-path traffic routing method achieves the highest theoretical upper bound on the transmission rate of the whole network, which is almost 2 times that of RIP, OSPF, and TORA, and 4 times that of GPSR and ZRP, demonstrating its superior efficiency. This significant improvement stems from the fact that conventional protocols restrict each node to transmitting data to a single receiver, whereas the proposed method enables nodes to transmit data to multiple receivers simultaneously. Consequently, data can reach the AP through multiple paths, substantially enhancing the overall transmission rate.

3) Comparison of DM-PSO With Other Algorithms: We compare the performance of our proposed DM-PSO with several benchmark heuristic algorithms, including differential evolution (DE) [68], genetic algorithm (GA) [69], artificial bee colony (ABC) [70], salp swarm algorithm (SSA) [71], and conventional PSO.

The objective function values f for the V-RPTRMOP obtained by these algorithms for the considered two cases are shown in Fig. 7. As can be seen, the curves of DE and ABC remain stable with minimal reductions in the objective function value as the number of iterations increases. The reason is that DE and ABC converge prematurely to local optimal solutions. Moreover, the performance of SSA and PSO in different cases is relatively unstable, since heuristic algorithms exhibit varying effectiveness when solving diverse problems or even the same problem under different setting. In addition, it can be found that GA outperforms the aforementioned three algorithms. However, final objective value of GA remains higher than that of DM-PSO. Finally, even in the later iterations, the objective function value achieved by DM-PSO continues to decrease, highlighting its superior exploration and exploitation capabilities.

<!-- image-->

(a) Case 1  
<!-- image-->  
(b) Case 2  
Fig. 7. Objective function value f of the V-RPTRMOP obtained by several benchmark heuristic algorithms and the proposed DM-PSO for the two cases.

TABLE III  
NUMERICAL OPTIMIZATION RESULTS OF THE FOUR PARTS OBTAINED BY SEVERAL BENCHMARK HEURISTIC ALGORITHMS AND THE PROPOSED DM-PSO FOR THE TWO CASES
<table><tr><td rowspan=1 colspan=1>Case</td><td rowspan=1 colspan=1>Algorithm</td><td rowspan=1 colspan=2>PartI</td><td rowspan=1 colspan=1>Part II</td><td rowspan=1 colspan=1>Part III</td><td rowspan=1 colspan=1>Part IV</td></tr><tr><td rowspan=5 colspan=1>1</td><td rowspan=5 colspan=1>DE [68]GA [69]ABC[70]SSA [71]PSO [56]DM-PSO</td><td rowspan=5 colspan=2>101440.5119.783021.0164.080.90</td><td rowspan=5 colspan=1>45196.256.533286.373.540.80</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td></tr><tr><td rowspan=2 colspan=1>00</td><td rowspan=3 colspan=1>000</td></tr><tr><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=6 colspan=1>2</td><td rowspan=6 colspan=1>DE[68]GA [69]ABC [70]SSA [71]PSO [56]DM-PSO</td><td rowspan=4 colspan=2>4983108.811855.75832599.85334978.4</td><td rowspan=1 colspan=1>1151133.9</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>2473.6</td><td rowspan=1 colspan=1>0</td><td rowspan=2 colspan=1>00</td></tr><tr><td rowspan=1 colspan=1>1151161.9</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>5334978.4</td><td rowspan=1 colspan=1>1568413.9</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=2 colspan=2>136976.9659.5</td><td rowspan=1 colspan=1>136976.9</td><td rowspan=1 colspan=1>38215.1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>132.2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr></table>

Table III shows the final optimized values of the four Parts in the V-RPTRMOP obtained by several benchmark algorithms and the proposed DM-PSO for both cases 1 and 2. Intuitively, DM-PSO achieves significantly lower values in the objective function defined in (20a) for both Parts I and II compared with other benchmark algorithms, which further illustrates the superiority of the proposed DM-PSO. Moreover, the optimized values of Parts III and IV are 0, the reason is that these two Parts are hard constraints and the corresponding weight factors are set relatively large, so that all algorithms adapt during the iterative process to optimize the first two Parts without triggering the latter two penalty conditions. Finally, it can be observed that, compared to the results of case 1, the values of Parts I and II obtained by these algorithms for case 2 are larger. The reason is that the network scale of case 2 is larger, with more transmission links and higher solution dimensionality during optimization, making it more challenging for these algorithms to find the optimal solution.

<!-- image-->  
(a) Part Iof Case 1

<!-- image-->  
(b) Part II of Case 1

<!-- image-->  
(c) Part Iof Case 2

<!-- image-->  
(d) Part I of Case 2  
Fig. 8. The CDFs of the values for Parts I and II corresponding to solutions of the proposed DM-PSO and benchmark algorithms for the two cases.

In conclusion, the performance of DM-PSO is superior to that of the other benchmark algorithms in solving the V-RPTRMOP. This improvement is due to the introduction of the diffusion model, which enables the more crowded agents to escape local optima and explore a broader search space.

4) Stability Analysis of DM-PSO: In this part, 30 times independently replicated trials are executed to validate the stability of the proposed DM-PSO and benchmark algorithms. Fig. 8 presents the cumulative distribution functions (CDFs) for Parts I and II obtained by the solutions of the proposed DM-PSO and other benchmark algorithms for the two cases. As illustrated, the performance of the benchmark algorithms is inferior to that of the proposed DM-PSO. Specifically, the solutions obtained by the SSA exhibit considerable instability in both Parts I and II. Moreover, although the DE, ABC, and GA demonstrate relatively stable performance, their solutions correspond to high values of Parts I and II. In addition, while the conventional PSO performs better than the aforementioned benchmarks, its solutions still show a wider spread in Parts I and II compared to those of the proposed DM-PSO. Notably, the majority of solutions obtained by the proposed DM-PSO consistently yields the smallest values of both Parts I and II for the two cases, which owes to the introduction of the diffusion model that enables the more crowded agents to escape from the local optima and explore a boarder search space. In particular, in case 1, the values of Part I of the solutions obtained by the proposed DM-PSO are nearly zero. In conclusion, the stability and superiority of the proposed DM-PSO are effectively demonstrated.

## C. Robustness Analysis

The robustness of the constructed communication network is validated by evaluating the impact of three unexpected situations on network performance, which are position jitters, phase errors of UAVs, and communication link interruption, respectively. To mitigate randomness, 30 independent trials are conducted, and the average results are presented. Detailed results and analyses are provided in the Appendix B of the supplemental material, available online.

## VII. CONCLUSION

In this work, we have designed a UAV-swarm enabled collaborative self-organizing network to assist post-disaster communications. We have formulated an optimization problem termed as RPTRMOP to maximize the transmission rate of the constructed communication network. Given that the formulated RPTRMOP cannot be tackled by traditional methods directly, we have proposed a two-stage optimization approach. In the first stage, the optimal multi-path traffic routing and the theoretical upper bound on the transmission rate of the network have been derived by using theoretical analysis and the Ford-Fulkerson algorithm. In the second stage, we have transformed the formulated RPTRMOP into a variant named V-RPTRMOP based on the obtained optimal multi-path traffic routing. Then, we have optimized the excitation current weight and the placement of each participating UAV via the proposed DM-PSO, so that the actual transmission rate closely can approach its theoretical upper bound. Simulation results have validated the effectiveness of the proposed two-stage optimization approach in solving the formulated problem, which demonstrates significant potential for post-disaster communications. Moreover, we have evaluated the impact of UAV position jitters and phase errors on system performance, and the decent results manifests the robustness of the constructed network.

Despite these promising results, this work has certain limitations. First, the lack of specific security measures renders UAV swarms vulnerable to eavesdropping, making them attractive targets for adversaries seeking to exploit weaknesses in the communication links. Moreover, this work does not conduct a comprehensive real-world deployment to assess the practical applicability of the adopted coordination mechanism among UAVs in the considered scenario. To address the aforementioned limitations and further advance this research, our future research will focus on UAVs-enabled covert communications, adaptive UAV clustering and coordination in disaster environments, and solar-powered UAV-assisted post-disaster communications.

## REFERENCES

[1] Y. Jiang et al., â6G non-terrestrial networks enabled low-altitude economy: Opportunities and challenges,â 2023, arXiv:2311.09047.

[2] J. Yang et al., âA case study on the development and application of low-altitude economy in agriculture in China: Based on demand-supplyenvironment perspective,â Academic J. Bus. Manage., vol. 6, no. 9, pp. 168â176, 2024.

[3] X. LIAO, C. XU, and H. YE, âBenefits and challenges of constructing low-altitude air route network infrastructure for developing low-altitude economy,â Bull. Chin. Acad. Sci., vol. 39, no. 11, pp. 1966â1981, 2024.

[4] G. Cheng, X. Song, Z. Lyu, and J. Xu, âNetworked ISAC for lowaltitude economy: Transmit beamforming and UAV trajectory design,â 2024, arXiv:2405.07568.

[5] OpenAI, âChatGPT,â 2023. Accessed: Jan. 05, 2025. [Online]. Available: [Online]. Available: https://chat.openai.com

[6] Y. Wang, Z. Su, Q. Xu, R. Li, T. H. Luan, and P. Wang, âA secure and intelligent data sharing scheme for UAV-assisted disaster rescue,â IEEE/ACM Trans. Netw., vol. 31, no. 6, pp. 2422â2438, Dec. 2023.

[7] N. Zhao et al., âUAV-assisted emergency networks in disasters,â IEEE Wireless Commun., vol. 26, no. 1, pp. 45â51, Feb. 2019.

[8] X. Yang, B. Han, G. Zhang, P. Zheng, J. Bai, and D. Qin, âNOMA-assisted routing algorithm design for UAV ad hoc relay networks,â IEEE Sens. J., vol. 23, no. 3, pp. 3296â3312, Feb. 2023.

[9] J. Garza et al., âDesign of UAVs-based 3D antenna arrays for a maximum performance in terms of directivity and SLL,â Int. J. Antenn. Propag., vol. 2016, 2016, Art. no. 2621862.

[10] G. Sun et al., âEnergy efficient collaborative beamforming for reducing sidelobe in wireless sensor networks,â IEEE Trans. Mobile Comput., vol. 20, no. 3, pp. 965â982, Mar. 2021.

[11] S. Jayaprakasam, S. K. A. Rahim, and C. Y. Leow, âDistributed and collaborative beamforming in wireless sensor networks: Classifications, trends, and research directions,â IEEE Commun. Surv. Tut., vol. 19, no. 4, pp. 2092â2116, Fourth Quarter 2017.

[12] G. Sun et al., âUAV-enabled secure communications via collaborative beamforming with imperfect eavesdropper information,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 3291â3308, Apr. 2024.

[13] L. R. Ford Jr and D. R. Fulkerson, Flows in Networks, vol. 56. Princeton, NJ, USA: Princeton Univ. Press, 2015.

[14] D.-H. Tran, V.-D. Nguyen, S. Chatzinotas, T. X. Vu, and B. Ottersten, âUAV relay-assisted emergency communications in IoT networks: Resource allocation and trajectory optimization,â IEEE Trans. Wireless Commun., vol. 21, no. 3, pp. 1621â1637, Mar. 2022.

[15] X. Liu et al., âTransceiver design and multihop D2D for UAV IoT coverage in disasters,â IEEE Internet Things J., vol. 6, no. 2, pp. 1803â1815, Apr. 2019.

[16] Z. Shah, U. Javed, M. Naeem, S. Zeadally, and W. Ejaz, âMobile edge computing (MEC)-enabled UAV placement and computation efficiency maximization in disaster scenario,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13406â13416, Oct. 2023.

[17] T. Do-Duy, L. D. Nguyen, T. Q. Duong, S. R. Khosravirad, and H. Claussen, âJoint optimisation of real-time deployment and resource allocation for UAV-Aided disaster emergency communications,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3411â3424, Nov. 2021.

[18] Z. Yao, W. Cheng, W. Zhang, and H. Zhang, âResource allocation for 5G-UAV-Based emergency wireless communications,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3395â3410, Nov. 2021.

[19] Y. Wang et al., âTask offloading for post-disaster rescue in unmanned aerial vehicles networks,â IEEE ACM Trans. Netw., vol. 30, no. 4, pp. 1525â1539, Aug. 2022.

[20] Z. Xu, X. Zheng, and J. Zhou, âOptimization design of collaborative beamforming for heterogeneous UAV swarm,â Phys. Commun, vol. 61, 2023, Art. no. 102202.

[21] S. K. Moorthy, N. Mastronarde, S. Pudlewski, E. S. Bentley, and Z. Guan, âSwarm UAV networking with collaborative beamforming and automated ESN learning in the presence of unknown blockages,â Comput. Netw., vol. 231, 2023, Art. no. 109804.

[22] H. Jung, I.-H. Lee, and J. Joung, âSecurity energy efficiency analysis of analog collaborative beamforming with stochastic virtual antenna array of UAV swarm,â IEEE Trans. Veh. Technol., vol. 71, no. 8, pp. 8381â8397, Aug. 2022.

[23] J. Li, G. Sun, Q. Wu, S. Liang, P. Wang, and D. Niyato, âTwo-way aerial secure communications via distributed collaborative beamforming under eavesdropper collusion,â in Proc. IEEE Conf. Comput. Commun., 2024, pp. 331â340.

[24] L. Zhang, X. Ma, Z. Zhuang, H. Xu, V. Sharma, and Z. Han, âQ-learning aided intelligent routing with maximum utility in cognitive UAV swarm for emergency communications,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 3707â3723, Mar. 2023.

[25] N. P. Sharvari, D. Das, J. Bapat, and D. Das, âConnectivity and collision constrained opportunistic routing for emergency communication using UAV,â Comput. Netw., vol. 220, 2023, Art. no. 109468.

[26] X. He, R. Jin, and H. Dai, âMulti-hop task offloading with on-the-fly computation for multi-UAV remote edge computing,â IEEE Trans. Commun., vol. 70, no. 2, pp. 1332â1344, Feb. 2022.

[27] A. Rahmati et al., âDynamic interference management for UAV-assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 21, no. 4, pp. 2637â2653, Apr. 2022.

[28] L. Lin, W. Xu, W. Chen, F. Wang, G. Li, and M. Pan, âPrioritized delay optimization for NOMA-based Multi-UAV emergency networks,â IEEE Trans. Veh. Technol., vol. 71, no. 10, pp. 11222â11227, Oct. 2022.

[29] Q. Luan, H. Cui, L. Zhang, and Z. Lv, âA hierarchical hybrid subtask scheduling algorithm in UAV-assisted MEC emergency network,â IEEE Internet Things J., vol. 9, no. 14, pp. 12737â12753, Jul. 2022.

[30] B. Hu, L. Wang, S. Chen, J. Cui, and L. Chen, âAn uplink throughput optimization scheme for UAV-enabled urban emergency communications,â IEEE Internet Things J., vol. 9, no. 6, pp. 4291â4302, Mar. 2022.

[31] Z. Niu, H. Liu, X. Lin, and J. Du, âTask scheduling with UAV-assisted dispersed computing for disaster scenario,â IEEE Syst. J., vol. 16, no. 4, pp. 6429â6440, Dec. 2022.

[32] Y. Zhang and W. Cheng, âTrajectory and power optimization for multi-UAV enabled emergency wireless communications networks,â in Proc. IEEE ICC Workshops, 2019, pp. 1â6.

[33] Y. Guan, S. Zou, H. Peng, W. Ni, Y. Sun, and H. Gao, âCooperative UAV trajectory design for disaster area emergency communications: A multiagent PPO method,â IEEE Internet Things J., vol. 11, no. 5, pp. 8848â8859, Mar. 2024.

[34] P. Wan, G. Xu, J. Chen, and Y. Zhou, âDeep reinforcement learning enabled multi-UAV scheduling for disaster data collection with time-varying value,â IEEE Trans. Intell. Transp. Syst., vol. 25, no. 7, pp. 6691â6702, Jul. 2024.

[35] T. Zhang, J. Lei, Y. Liu, C. Feng, and A. Nallanathan, âTrajectory optimization for UAV emergency communication with limited user equipment energy: A safe-DQN approach,â IEEE Trans. Green Commun. Netw., vol. 5, no. 3, pp. 1236â1247, Sep. 2021.

[36] L. Zhang, H. Zhang, C. Guo, H. Xu, L. Song, and Z. Han, âSatelliteaerial integrated computing in disasters: User association and offloading decision,â in Proc. IEEE Int. Conf. Commun., 2020, pp. 554â559.

[37] L. Zhang, Y. Wang, M. Min, C. Guo, V. Sharma, and Z. Han, âPrivacyaware laser wireless power transfer for aerial multi-access edge computing: A colonel Blotto game approach,â IEEE Internet Things J., vol. 10, no. 7, pp. 5923â5939, Apr. 2023.

[38] J. Li, H. Kang, G. Sun, S. Liang, Y. Liu, and Y. Zhang, âPhysical layer secure communications based on collaborative beamforming for UAV networks: A multi-objective optimization approach,â in Proc. IEEE Conf. Comput. Commun., 2021, pp. 1â10.

[39] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âCommunications and control for wireless drone-based antenna array,â IEEE Trans. Commun., vol. 67, no. 1, pp. 820â834, Jan. 2019.

[40] A. Rahmati, X. He, I. Guvenc, and H. Dai, âDynamic mobility-aware interference avoidance for aerial base stations in cognitive radio networks,â in Proc. IEEE Conf. Comput. Commun., 2019, pp. 595â603.

[41] A. Al-Hourani, K. Sithamparanathan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[42] J. Du, C. Jiang, A. Benslimane, S. Guo, and Y. Ren, âSDN-based resource allocation in edge and cloud computing systems: An evolutionary Stackelberg differential game approach,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1613â1628, Aug. 2022.

[43] Y. Zeng and R. Zhang, âEnergy-efficient UAV communication with trajectory optimization,â IEEE Trans. Wireless Commun., vol. 16, no. 6, pp. 3747â3760, Jun. 2017.

[44] K. Alemdar, D. Varshney, S. Mohanti, U. Muncuk, and K. Chowdhury, Rfclock: Timing, Phase And Frequency Synchronization for Distributed Wireless Networks. New York, NY, USA: ACM, 2021, pp. 15â27.

[45] L. Lamport, âPaxos made simple,â ACM SIGACT News (Distrib. Comput. Column), vol. 32, pp. 51â58, 2001.

[46] Y. Zeng, Q. Wu, and R. Zhang, âAccessing from the sky: A tutorial on UAV communications for 5G and beyond,â in Proc. IEEE, vol. 107, no. 12, pp. 2327â2375, Dec. 2019.

[47] L. Dong, A. P. Petropulu, and H. V. Poor, âA cross-layer approach to collaborative beamforming for wireless ad hoc networks,â IEEE Trans. Signal Process., vol. 56, no. 7, pp. 2981â2993, Jul. 2008.

[48] L. R. Ford Jr and D. R. Fulkerson, âMaximal flow through a network,â Can. J. Math., vol. 8, pp. 399â404, 1956.

[49] R. K. Ahuja et al., Network Flows: Theory, Algorithms, and Applications, vol. 1. Englewood Cliffs, NJ, USA: Prentice-Hall, 1993.

[50] S.-W. Jeon, K. Jung, and H. Chang, âFully distributed algorithms for minimum delay routing under heavy traffic,â IEEE Trans. Mobile Comput., vol. 13, no. 5, pp. 1048â1060, May 2014.

[51] J. Du, T. Lin, C. Jiang, Q. Yang, C. F. Bader, and Z. Han, âDistributed foundation models for multi-modal learning in 6G wireless networks,â IEEE Wireless Commun., vol. 31, no. 3, pp. 20â30, Jun. 2024.

[52] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms. Cambridge, MA, USA: MIT Press, 2022.

[53] P. Goos, U. Syafitri, B. Sartono, and A. Vazquez, âA nonlinear multidimensional knapsack problem in the optimal design of mixture experiments,â Eur. J. Oper. Res., vol. 281, no. 1, pp. 201â221, 2020.

[54] S. Jayaprakasam, S. K. Abdul Rahim, C. Y. Leow, T. O. Ting, and A. A. Eteng, âMultiobjective beampattern optimization in collaborative beamforming via NSGA-II with selective distance,â IEEE Trans. Antennas Propag., vol. 65, no. 5, pp. 2348â2357, May 2017.

[55] J. Li, Q. Lv, P. Zhu, D. Wang, J. Wang, and X. You, âNetwork-assisted full-duplex distributed massive MIMO systems with beamforming training based CSI estimation,â IEEE Trans. Wirel. Commun., vol. 20, no. 4, pp. 2190â2204, Apr. 2021.

[56] J. Kennedy and R. Eberhart, âParticle swarm optimization,â in Proc. Int. Conf. Neural Netw., 1995, pp. 1942â1948.

[57] J. Li, G. Sun, L. Duan, and Q. Wu, âMulti-objective optimization for UAV swarm-assisted IoT with virtual antenna arrays,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4890â4907, May 2024.

[58] J. Du, C. Jiang, J. Wang, Y. Ren, and M. Debbah, âMachine learning for 6G wireless networks: Carry-forward-enhanced bandwidth, massive access, and ultrareliable/low latency,â IEEE Veh. Technol. Mag., vol. 15, no. 4, pp. 123â134, Dec. 2020.

[59] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[60] Z. Wang, J. Zhang, E. BjÃ¶rnson, D. Niyato, and B. Ai, âOptimal bilinear equalizer for cell-free massive MIMO systems over correlated Rician channels,â IEEE Trans. Signal Process., early access, Mar. 11, 2025, doi: 10.1109/TSP.2025.3547380.

[61] N. Gupta, S. Agarwal, D. Mishra, and B. Kumbhani, âTrajectory and resource allocation for UAV replacement to provide uninterrupted service,â IEEE Trans. Commun., vol. 71, no. 12, pp. 7288â7302, Dec. 2023.

[62] M. Samir, C. Assi, S. Sharafeddine, and A. Ghrayeb, âOnline altitude control and scheduling policy for minimizing AoI in UAV-assisted IoT wireless networks,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2493â2505, Jul. 2022.

[63] C. L. Hedrick, âRouting information protocol,â RFC 1058, Rutgers Univ., Tech. Rep., 1988.

[64] M. PiÃ³ro, Ã. Szentesi, J. Harmatos, A. JÃ¼ttner, P. Gajowniczek, and S. Kozdrowski, âOn open shortest path first related network optimisation problems,â Perform. Eval., vol. 48, no. 1â4, pp. 201â223, 2002.

[65] B. Karp and H.-T. Kung, âGPSR: Greedy perimeter stateless routing for wireless networks,â in Proc. 6th Annu. Int. Conf. Mobile Comput. Netw., 2000, pp. 243â254.

[66] N. Beijar, âZone routing protocol (ZRP),â Netw. Lab., Helsinki Univ. Technol., vol. 9, no. 1, 2002, Art. no. 12.

[67] V. D. Park and M. S. Corson, âA performance comparison of the temporally-ordered routing algorithm and ideal link-state routing,â in Proc. 3rd IEEE Symp. Comput. Commun., 1998, pp. 592â598.

[68] S. Das and P. N. Suganthan, âDifferential evolution: A survey of the stateof-the-art,â IEEE Trans. Evol. Comput., vol. 15, no. 1, pp. 4â31, 2010.

[69] S. Mirjalili and S. Mirjalili, âGenetic algorithm,â Evol. algorithms neural networks: theory Appl., pp. 43â55, Feb. 2021.

[70] D. Karaboga and B. Akay, âA comparative study of artificial bee colony algorithm,â Appl. Math. Comput., vol. 214, no. 1, pp. 108â132, 2009.

[71] S. Mirjalili, A. H. Gandomi, S. Z. Mirjalili, S. Saremi, H. Faris, and S. M. Mirjalili, âSALP swarm algorithm: A bio-inspired optimizer for engineering design problems,â Adv. Eng. Softw., vol. 114, pp. 163â191, 2017.

<!-- image-->

<!-- image-->

Geng Sun (Senior Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, in 2007, and the PhD degree in computer science and technology from Jilin University, in 2018. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is a professor in College of Computer Science and Technology with Jilin University, and his research interests include wireless networks, UAV communications, collaborative beamforming, and optimizations.

Xiaoya Zheng received the BS degree in software engineering from Hebei Geology University, in 2021, and the MS degree in the College of Computer Science and Technology from Jilin University, in 2024. She is currently working toward the PhD degree with the College of Computer Science and Technology, Jilin University. Her research interests focus on UAV networks and optimization techniques.

<!-- image-->

<!-- image-->

Jiacheng Wang (Member, IEEE) received the PhD degree in the School of Communications and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China. He is the research fellow in the College of Computing and Data Science with Nanyang Technological University, Singapore. His research interests include wireless sensing, semantic communications, and generative AI, Metaverse.

Jiahui Li (Student Member, IEEE) received the BS degree in software engineering, and the MS and PhD degrees in computer science and technology from Jilin University, Changchun, China, in 2018, 2021, and 2024, respectively. He was a visiting PhD student with the Singapore University of Technology and Design (SUTD). He currently serves as an assistant researcher in the College of Computer Science and Technology with Jilin University. His current research focuses on integrated air-ground networks, UAV networks, wireless energy transfer, and optimization.

<!-- image-->

Qingqing Wu (Senior Member, IEEE) received the BEng and the PhD degrees in electronic engineering from the South China University of Technology and Shanghai Jiao Tong University, in 2012 and 2016, respectively. From 2016 to 2020, he was a research fellow in the Department of Electrical and Computer Engineering, National University of Singapore. He is currently an associate professor with Shanghai Jiao Tong University. His current research interest includes IRS, UAV communications, and MIMO transceiver design. He has coauthored more than 100

IEEE journal papers with 26 ESI highly cited papers and 8 ESI hot papers, which have received more than 18,000 Google citations. He was listed as the Clarivate ESI Highly Cited Researcher, in 2022 and 2021, the Most Influential Scholar Award in AI-2000 by Aminer, in 2021 and Worldâs Top 2% Scientist by Stanford University, in 2020 and 2021.

<!-- image-->  
Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, in 1999, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a professor with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

<!-- image-->

Abbas Jamalipour (Fellow, IEEE) received the PhD degree in electrical engineering from Nagoya University, Nagoya, Japan, in 1996. He is currently a professor of ubiquitous mobile networking with The University of Sydney. He has authored nine technical books, eleven book chapters, more than 550 technical papers, and five patents, all in wireless communications and networking. He was a member of the Board of Governors of the IEEE Communications Society. He has been an elected member of the Board of Governors of the IEEE Vehicular Technology So-

ciety since 2014. He is a member of the Advisory Board of IEEE Internet of Things Journal. He is a fellow of the Institute of Electrical, Information, and Communication Engineers (IEICE), and the Institution of Engineers Australia, an ACM Professional Member, and an IEEE Distinguished Speaker. He was a recipient of a number of prestigious awards, such as the 2019 IEEE ComSoc Distinguished Technical Achievement Award in Green Communications, the 2016 IEEE ComSoc Distinguished Technical Achievement Award in Communications Switching and Routing, the 2010 IEEE ComSoc Harold Sobol Award, the 2006 IEEE ComSoc Best Tutorial Paper Award, and more than 15 best paper awards. He has been the general chair or the technical program chair of several prestigious conferences, including IEEE ICC, GLOBECOM, WCNC, and PIMRC. He is the editor-in-chief of IEEE Transactions on Vehicular Technology. He was the president of the IEEE Vehicular Technology Society from 2020 to 2021. Previously, he held the positions of the executive vice-president and the editor-in-chief of VTS Mobile World. He was the editor-in-chief of IEEE Wireless Communications and the vice president-Conferences. He sits on the Editorial Board of IEEE Access and several other journals.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_6_img_1.jpeg|page_6_img_1]]
2. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_6_img_2.jpeg|page_6_img_2]]
3. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_6_img_3.jpeg|page_6_img_3]]
4. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_7_img_1.jpeg|page_7_img_1]]
5. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_11_img_1.jpeg|page_11_img_1]]
6. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_11_img_2.jpeg|page_11_img_2]]
7. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_11_img_3.jpeg|page_11_img_3]]
8. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_11_img_4.jpeg|page_11_img_4]]
9. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_16_img_1.png|page_16_img_1]]
10. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_18_img_1.jpeg|page_18_img_1]]
11. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_18_img_2.jpeg|page_18_img_2]]
12. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_18_img_3.jpeg|page_18_img_3]]
13. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_18_img_4.jpeg|page_18_img_4]]
14. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_18_img_5.jpeg|page_18_img_5]]
15. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_19_img_1.jpeg|page_19_img_1]]
16. [[../extracted_images/UAV_Swarm-Enabled_Collaborative_Post-Disaster_Communications_in_Low_Altitude_Economy_via_a_Two-Stage_Optimization_Approach/page_19_img_2.jpeg|page_19_img_2]]

---

