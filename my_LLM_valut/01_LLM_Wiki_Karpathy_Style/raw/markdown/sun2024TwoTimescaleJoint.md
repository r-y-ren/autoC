# TJCCT: A Two-Timescale Approach for UAV-Assisted Mobile Edge Computing

Zemin Sun , Member, IEEE, Geng Sun , Senior Member, IEEE, Qingqing Wu , Senior Member, IEEE, Long He , Shuang Liang , Hongyang Pan , Dusit Niyato , Fellow, IEEE, Chau Yuen , Fellow, IEEE, and Victor C. M. Leung , Life Fellow, IEEE

AbstractâUnmanned aerial vehicle (UAV)-assisted mobile edge computing (MEC) is emerging as a promising paradigm to provide aerial-terrestrial computing services in close proximity to mobile devices (MDs). However, meeting the demands of computationintensive and delay-sensitive tasks for MDs poses several challenges, including the demand-supply contradiction between MDs and MEC servers, the demand-supply discrepancy between MDs

and MEC servers, the trajectory control requirements on energy efficiency and timeliness, and the different time-scale dynamics of the network. To address these issues, we first present a hierarchical architecture by incorporating terrestrial-aerial computing capabilities and leveraging UAV flexibility. Furthermore, we formulate a joint computing resource allocation, computation offloading, and trajectory control problem to maximize the system utility. Since the problem is a non-convex and NP-hard mixed integer nonlinear programming (MINLP), we propose a two-timescale joint computing resource allocation, computation offloading, and trajectory control (TJCCT) approach for solving the problem. In the short timescale, we propose a price-incentive model for on-demand computing resource allocation and a matching mechanism-based method for computation offloading. In the long timescale, we propose a convex optimization-based method for UAV trajectory control. Besides, we theoretically prove the stability and polynomial complexity of TJCCT. Extensive simulation results demonstrate that the proposed TJCCT is able to achieve superior performances in terms of the system utility, average processing rate, average completion delay, average completion ratio, and average cost, while meeting the energy constraints despite the trade-off of the increased energy consumption.

Index TermsâComputation offloading, computing resource allocation, trajectory control, UAV-assisted MEC network.

## I. INTRODUCTION

T HE development of wireless communications and the pro-liferation of mobile devices (MDs) triers various emerging liferation of mobile devices (MDs)triers various emerging applications, such as autonomous driving, online gaming, and augmented reality. These applications often require extensive computing resources and low latency to satisfy the quality of experience (QoE). However, fulfilling the computation-intensive and delay-sensitive computation tasks of these applications poses a great challenge to MDs with insufficient computational capability and finite energy capacity. To tackle this challenge, mobile edge computing (MEC) has been identified as a promising technology to meet the stringent requirements of these applications [1]. By offloading the computation-intensive tasks to proximate MEC servers, the QoE of MDs can be significantly enhanced in a cost-effective and energy-efficient way. However, due to the dependence on terrestrial infrastructures and environment, conventional terrestrial MEC servers are limited by the high cost of deployment, low adaptability to the network dynamic, and fixed service range.

Recent years have seen a paradigm shift from terrestrial edge computing toward aerial-terrestrial edge computing, i.e., UAV-assisted MEC networks, by integrating UAVs with MEC. With high maneuverability, UAVs could be rapidly and flexibly deployed as aerial MEC servers to assist the terrestrial MEC

Digital Object Identifier 10.1109/TMC.2024.3505155 servers in providing computation offloading services whenever and wherever needed. Moreover, the line-of-sight (LoS) link of UAVs can improve the communication reliability and network capacity of the terrestrial MEC networks.

Despite the aforementioned benefits, designing an efficient scheme of computation offloading in UAV-assisted MEC systems is facing several unprecedented challenges. i) Demand-Supply Contradiction for Resource Allocation. Compared to the cloud, MEC servers have limited computing capabilities, particularly for aerial MEC servers with constrained carrying capacity. However, the computation tasks of MDs are often computation-hungry and latency-sensitive. This demand-supply contradiction between the limited computing resources of MEC servers and the stringent requirement of MDs poses a challenge for efficient computing resource allocation. ii) Demand-Supply Discrepancy for Computation Offloading. Different computation tasks of MDs have diverse requirements on computing resources, while different MEC servers possess varying computing capabilities. This demand-supply discrepancy between the computation tasks of MDs and MEC servers could incur resource under-utilization among MEC servers, which brings difficulties in designing efficient computation offloading methods to ensure satisfied QoE for MDs and high resource utilization among MEC servers. iii) Energy-Efficient and Real-Time Trajectory Control. The mobility of MDs and random generation of computation tasks lead to spatiotemporal dynamics in the offloading requirements, which necessitates real-time trajectory control. However, the intrinsic limited onboard energy of UAVs restricts the service time, thus posing challenges for energy-efficient and real-time UAV trajectory control. iv) Different Time-Scale Dynamics. The dynamic characteristics of the UAV-assisted MEC network, such as the dynamic of the channel, random arrival of tasks, and mobility of MDs, vary across different timescales. Accordingly, integrating these features into a joint optimization framework for computing resource allocation, computation offloading, and trajectory control is significant but leads complexity to the algorithm design.

This work presents a two-timescale computing resource allocation, task offloading, and UAV trajectory control approach in UAV-assisted MEC. The main contributions are summarized as follows.

C System Architecture: We employ a hierarchical architecture for the UAV-assisted MEC network that consists of an MD layer, a terrestrial edge layer, an aerial edge layer, and a control layer. Under the coordination of the software-defined network (SDN) controller, the two-timescale decisions are made to deal with the demand-supply contradiction between MDs and MEC servers, demand-supply discrepancy between MDs and MEC servers, and the spatio-temporal dynamics of computation tasks.

Problem Formulation: We formulate a joint computing resource allocation, computation offloading, and trajectory control problem to maximize the system utility that is theoretically modeled by synthesizing the network dynamics between MDs and terrestrial/aerial edge links, MD mobility, MD QoE, and the energy consumption of terrestrial/aerial MEC servers. Moreover, the optimization problem is proved to be a non-convex and NP-hard mixed integer nonlinear programming (MINLP).

Algorithm Design: To solve the formulated problem, we propose a two-timescale joint computing resource allocation, computation offloading, and trajectory control (TJCCT) algorithm. Specifically, TJCCT consists of a price-incentive method for on-demand computing resource allocation, a matching mechanism-based method for computation offloading, and a convex optimizationbased method for UAV trajectory control.

- Performance Evaluation: The performance of TJCCT is verified through both theoretical analysis and simulation. First, the stability, optimality, and computation complexity of TJCCT are proved theoretically. Furthermore, simulation results demonstrate that TJCCT has better performances and scalability than the baseline algorithms.

The remaining of this work is organized as follows. Section II reviews the related work. Section III presents the system model and problem formulation. Section IV elaborates on the proposed TJCCT. The theoretical analysis is given in Section V. Section VI shows the simulation results and discussions. Finally, this work is concluded in Section VIII.

## II. RELATED WORK

In this section, we review the related work on the edge computing architecture, joint computation offloading, computing resource allocation, and the optimization approach.

## A. MEC Architecture

The MEC has been extensively studied to extend the computing capabilities of MDs through computation offloading. Numerous research efforts have focused on leveraging terrestrial MEC to offer low-latency offloading services in different scenarios. For example, Wang et al. [2] presented a non-cooperative computation offloading approach in a single-BS vehicular MEC network. Furthermore, Tao et al. [3] proposed a dynamic pricingbased computation offloading scheme for a single-cell and multuser MEC system. However, these studies mainly rely on the terrestrial MEC servers. In the dense area, the link between users and MEC servers experience severe blockage and poor signal strength.

To extend the capability of the traditional MEC system, some studies focused on cooperative computing schemes to fully exploit the computing resources of users. For example, You et al. [4] explored a co-computing system where a request user offloads computation to a helper user with idle resources. Xie et al. [5] focused on the cooperative computing for mobile crowdsensing, where the sensor data of source users can be offloaded to nearby mobile devices with unused computational resources. Moreover, Wei et al. [6] proposed a novel multi-tier task offloading approach in the vehicular fog computing, where vehicles with idle resources cooperatively provide edge computing capabilities through the designed vehicle-to-vehicle (V2V) trading.

However, the abovementioned studies such as [4], [5] explored the cooperation among MDs in the networks where edge computing infrastructures are absent, which could be insufficient to effectively process the computation-intensive and delay-sensitive tasks without the assistance of powerful MEC. Moreover, the authors in [6] mainly explored the cooperative computing for divisible tasks in conventional MEC systems. In contrast, our work considers the tasks of MDs as indivisible. Therefore, offloading the whole task to a cooperative MD could lead to failure due to the limited resources of MDs. Additionally, we take into account the diverse task requirements, varied computing capabilities of MDs, and different mobility patterns, which may result in uncertain service durations for an MD to corporately process the tasks of the other devices. As a result, the cooperative computing scheme unsuitable for our considered scenario.

To address the abovementioned limitations, recent studies have expanded the scope of terrestrial MEC to UAV-assisted MEC to offer flexible aerial computing services for users. For example, Lin et al. [7] explored maximizing the energy efficiency and offloading fairness in a single-UAV-assisted MEC system. Wang et al. [8] proposed a UAV-assisted architecture for post-disaster rescue by leveraging the computing capability of vehicles. However, most of these studies consider relatively simple scenarios where only one UAV is deployed, or users are assumed to be stationary. This may not be suitable for complex situations with heterogeneous MEC servers and MDs.

In summary, the existing MEC architecture is inadequate to adapt to the heterogeneous and dynamic scenario of the UAVassisted MEC system. To this end, we propose a hierarchical architecture to address the limitations of the existing works.

## B. Computation Offloading, Resource Allocation, and Trajectory Control

Researchers have explored various aspects of UAV-assisted MEC systems, with a primary focus on computation offloading, resource allocation, and UAV trajectory control.

To address the limited computing capability of the UAVassisted MEC system, several studies focused on joint computation offloading and computing resource allocation to optimize the performances such as delay and energy consumption. For example, Tun et al. [9] focused on a latency minimization problem in the collaborative UAV-assisted MEC system by jointly optimizing the strategies of offloading and resource allocation. Ei et al. [10] presented a joint computation offloading and resource allocation problem for UAV-assisted edge computing to minimize the energy consumption of the system. Moreover, research attentions have also been dedicated to the joint optimization of computation offloading and UAV trajectory control. For instance, Han et al. [11] formulated an optimization problem to minimize the average task delay via jointly optimizing user association and UAV deployment. Moreover, Wang et al. [12] aimed to minimize the energy consumption of the UAV via joint region partitioning and UAV trajectory scheduling.

The limitations of these previous studies are summarized as follows. First, these works primarily focused on optimizing a single performance of the system, such as latency and energy. Furthermore, most of these studies formulated optimization problems from the perspective of the users or MEC servers. However, focusing solely on optimizing one aspect of the performance metric without a holistic consideration of the diverse requirements could lead to imbalanced system performance and poor user experience. To address these limitations, we formulate a problem of joint computation offloading, resource allocation, and trajectory control problem to maximize the system utility, which incorporates delay and energy consumption of both MDs and MEC servers, as well as the dynamics of the network.

## C. Optimization Approach

To alleviate the complexity arising from the multi-timescale feature of the formulated problem, some studies designed a multi-timescale approach to decouple the problem into multitimescale subproblems. For example, Shi et al. [13], [14] proposed a novel two-timescale resource optimization method for

MEC to balance the service migration and task rerouting of MDs whenever handovers occur. Yang et al. [15] studied the two-timescale online optimization for building human digital twin by jointly optimizing the construction of virtual twins, task offloading, and resource allocation. Moreover, Shi et al. [16] designed a novel two-timescale online approach for microservice deployment optimization with layer sharing in MEC system.

However, the abovementioned studies designed the twotimescale approaches to handle the asynchronization between different decisions with different triggers such as the deployment strategy and the resource management strategy. In comparison, we focus on dynamic characteristics of the UAV-assisted MEC network, including the dynamic of the channel, random arrival of tasks, mobility of MDs, and flight of UAVs. Therefore, we design a two-timescale approach to adapt to the different-timescale dynamics of the system.

To solve the intricate optimization problem of computation offloading, resource allocation, and trajectory control for UAVassisted MEC, researchers are devoted to effective optimization algorithms by employing advanced methodologies such as heuristic algorithms [17], swarm intelligent algorithms [18], game theory [19], and reinforcement learning (RL) [20], [21]. For example, Laboni et al. [17] proposed a hyper-heuristic algorithm for resource allocation in the MEC network. Furthermore, Tian et al. [18] developed a genetic algorithm (GA)-based algorithm for task offloading and UAV scheduling in the UAVassisted MEC system. Moreover, Ning et al. [19] proposed a stochastic game-based approach for multi-user computation offloading and MEC server deployment. In addition, Xu et al. [22] designed a multi-UAV trajectory planning algorithm based on proximal policy optimization (PPO) [23]. Miao et al. [23] proposed a deep deterministic policy gradient (DDPG)-based algorithm to optimize the computational resources allocation and UAV flight trajectory for UAV-assisted MEC.

However, heuristic algorithms generally lack guaranteed optimality and can be sensitive to initial conditions. Moreover, swarm intelligence algorithms and Stochastic games often require a substantial number of iterations to converge to a near-optimal solution, resulting in high computation complexity. In addition, although RL is powerful for training agents to make decisions, it requires a number of interactions with the environment and significant computational resources, making it costly in the resource-constrained and heterogeneous MEC system.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

In this section, a UAV-assisted MEC architecture is first introduced, followed by the communication model, computation model, system cost model, and problem formulation. The major notations are listed in Table I.

## A. System Model

1) System Overview: We consider a hierarchical UAVassisted MEC system as shown in Fig. 1. In the spatial dimension, the hierarchical UAV-assisted MEC system comprises an MD layer, a terrestrial edge layer, an aerial edge layer, and a control layer.

Specifically, at the MD layer, a set of MDs I $\{ 1 , \ldots , i , \ldots , I \}$ =moving in the considered area periodically 1handle the tasks with diverse requirements. At the terrestrial edge layer, a macro base station (MBS) b equipped with terrestrial MEC server1 provides edge computing services for the MDs within its service range. At the aerial edge layer, the rotary-wing UAVs $\mathcal { U } = \{ 1 , . . . , U \}$ equipped with aerial MEC = 1servers2 are dispatched as aerial base stations to assist the MBS in providing supplementary computing services for MDs. At the control layer, the regional SDN controller, on which our algorithm runs, coordinates the decisions regarding computation offloading for MDs, computing resource allocation for MEC servers, and trajectory control for UAVs based on the knowledge acquired from the terrestrial and aerial edge layers. Furthermore, we consider that the radio access links of the system are allocated orthogonal frequency bands. Besides, both the terrestrial MEC server and aerial MEC servers are collectively referred to MEC server, which is indexed as $j \in \{ b \} \cup U$

TABLE I SUMMARY OF NOTATIONS
<table><tr><td rowspan=1 colspan=1>Symb</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\overline { { \mathcal { I } = \{ 1 , \cdot . . , i , . . . , I \} } }$ </td><td rowspan=1 colspan=1>The set of MDs</td><td rowspan=1 colspan=1>b</td><td rowspan=1 colspan=1>MBS</td></tr><tr><td rowspan=1 colspan=1>u=</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>The set of UAVs</td><td rowspan=1 colspan=1> $\neg j \in \{ b \} \cup U$ </td><td rowspan=1 colspan=1>The MEC server</td></tr><tr><td rowspan=1 colspan=1>T=</td><td rowspan=1 colspan=1> $\mathcal { T } = \stackrel { \cdot } { \{ 1 , \dotsc , t , \dotsc , T \} }$ </td><td rowspan=1 colspan=1>System timeline</td><td rowspan=1 colspan=1>Î´</td><td rowspan=1 colspan=1>Time slot</td></tr><tr><td rowspan=1 colspan=2> $t _ { 0 } \in \mathcal { T } _ { 0 } = \{ 1 , . . . , T _ { 0 } \}$ </td><td rowspan=1 colspan=1>System time epoch</td><td rowspan=1 colspan=1> $\overline { { \mathbf { v } _ { i } ^ { t _ { 0 } \Delta } } }$ </td><td rowspan=1 colspan=1>Velocity of UAV j at time epoch to</td></tr><tr><td rowspan=1 colspan=2> $\overline { { \mathbf { q } _ { j } ^ { t } = [ x _ { j } ^ { t } , y _ { j } ^ { t } ] } }$ </td><td rowspan=1 colspan=1>The horizontal position of UAV j</td><td rowspan=1 colspan=1>Wi</td><td rowspan=1 colspan=1>Uncorrelated random Gaussian process</td></tr><tr><td rowspan=1 colspan=2> $\alpha , { \bar { \mathbf { v } } } , { \bar { \sigma } }$ </td><td rowspan=1 colspan=1>The memorydegree,symptoticmeanndasymp-totic standard deviation of velocity</td><td rowspan=1 colspan=1> $\overline { { \mathbf { v } _ { i } ^ { t _ { 0 } \Delta } } }$ </td><td rowspan=1 colspan=1>The velocity of MDi at time epoch to</td></tr><tr><td rowspan=1 colspan=2> $\overline { { \mathbf { g } _ { i , t } } } = [ x _ { i } ^ { t } , y _ { i } ^ { t } ]$ </td><td rowspan=1 colspan=1>Thelocation ofMDi</td><td rowspan=1 colspan=1> $\overline { { v _ { I I } ^ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>The maximumvelocity of UAV</td></tr><tr><td rowspan=1 colspan=2> $\mathbf { q } _ { j } ^ { I } , \mathbf { q } _ { j } ^ { F }$ </td><td rowspan=1 colspan=1>The initial and final positions of UAV j</td><td rowspan=1 colspan=1> $\overline { { d _ { \mathrm { U } } ^ { \mathrm { s a f e } } } }$ </td><td rowspan=1 colspan=1>Safe distance</td></tr><tr><td rowspan=1 colspan=2> $\overline { { f _ { i } ^ { \mathrm { m a x } } , n _ { i } ^ { \mathrm { c o r e } } , E _ { i } ^ { \mathrm { m a x } } , \zeta _ { i } ^ { t } } }$ </td><td rowspan=1 colspan=1>The computation capability, CPU core number, en-ergy constraint,and task generation indicator ofMDi</td><td rowspan=1 colspan=1> $\overline { { r _ { i , j } ^ { t } } }$ </td><td rowspan=1 colspan=1>Theupload data rate</td></tr><tr><td rowspan=1 colspan=2> $\overline { { n _ { j } ^ { \mathrm { c o r e } } , f _ { j } ^ { \mathrm { m a x } } , E _ { j } ^ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>The CPU core number, computation resources,andenergy constraint of MEC server j</td><td rowspan=1 colspan=1> $\overline { { B _ { i , j } } }$ </td><td rowspan=1 colspan=1>The bandwidth</td></tr><tr><td rowspan=1 colspan=2> $\overline { { \mathcal { K } _ { i } ^ { t } = < l _ { i } ^ { t } , \mu _ { i } ^ { t } , \tau _ { i } ^ { t } > } }$ </td><td rowspan=1 colspan=1>The size, computation intensity,and deadline oftask</td><td rowspan=1 colspan=1> $\overline { { g _ { i , j } ^ { t } } }$ </td><td rowspan=1 colspan=1>The channel power gain</td></tr><tr><td rowspan=1 colspan=2> $\overline { { g _ { i , j } ^ { t , x } } }$ </td><td rowspan=1 colspan=1>The channel power gain between MD iand MECserver j</td><td rowspan=1 colspan=1> $\overline { { P _ { i } ^ { t } } }$ </td><td rowspan=1 colspan=1>The transmit power of MD iin time slott</td></tr><tr><td rowspan=1 colspan=2>xâ{L,N}</td><td rowspan=1 colspan=1>LoSorNLoSlinks</td><td rowspan=1 colspan=1> $\overline { { N _ { 0 } } }$ </td><td rowspan=1 colspan=1>Noise power</td></tr><tr><td rowspan=1 colspan=2> $\overline { { d _ { 1 } , d _ { 2 } , p _ { 1 } , p _ { 2 } } }$ </td><td rowspan=1 colspan=1>The parameters to fit the specific scenarios</td><td rowspan=1 colspan=1> $\underline { { \mathbb { P } _ { i , j } ^ { t } } }$ </td><td rowspan=1 colspan=1>The probability of LoS transmission</td></tr><tr><td rowspan=1 colspan=2> $\overline { { m _ { y } ^ { x } \in \{ m _ { \mathrm { T } } ^ { \mathrm { L } } , m _ { \mathrm { T } } ^ { \mathrm { N } } , m _ { \mathrm { A } } ^ { \mathrm { L } } , m _ { \mathrm { A } } ^ { \mathrm { N } } \} } }$ </td><td rowspan=1 colspan=1>The Nakagami-m fading parameters for terres-trial/aerial LoS/NLoS channel.</td><td rowspan=1 colspan=1> $d _ { i , j } ^ { t }$ </td><td rowspan=1 colspan=1>The instantaneous distance betweenMD iand the MBS j</td></tr><tr><td rowspan=1 colspan=2>â{ï¼Î²N}</td><td rowspan=1 colspan=1>The path loss exponent for LoS/NLoS</td><td rowspan=1 colspan=1> $\overline { { h _ { i , j } ^ { t , x } , L _ { i , j } ^ { t , x } } }$ </td><td rowspan=1 colspan=1>The parameters of small-scale andlarge-scale fading</td></tr><tr><td rowspan=1 colspan=2> $\overline { { \chi ^ { x } \in \{ \chi ^ { \mathrm { L } } , \chi ^ { \mathrm { N } } \} } }$ </td><td rowspan=1 colspan=1>Thestandarddeviation ofshadowingforLoS/NLoS transmission</td><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>Light speed</td></tr><tr><td rowspan=1 colspan=2>d/d</td><td rowspan=1 colspan=1>Thereference distance between MDiandMBS/UAV j</td><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>Carrier frequency</td></tr><tr><td rowspan=1 colspan=2> $\overline { { D _ { i , i } ^ { t } / D _ { i , j } ^ { t } } }$ </td><td rowspan=1 colspan=1>Completion delay for local/edge computing</td><td rowspan=1 colspan=1> $\overline { { E _ { i , i } ^ { t } / E _ { i , j } ^ { t } } }$ </td><td rowspan=1 colspan=1>Energy.consumption for local/edgecomputing</td></tr><tr><td rowspan=1 colspan=2>D</td><td rowspan=1 colspan=1>Transmission delay for task uploading</td><td rowspan=1 colspan=1> $D _ { i , i } ^ { \mathrm { e x e } }$ </td><td rowspan=1 colspan=1>Computation delay at MEC server j</td></tr><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>Energy consumption for task execution at MECserverj</td><td rowspan=1 colspan=1> $\overline { { E _ { j } ^ { t , \mathrm { { f l y } } } } }$ </td><td rowspan=1 colspan=1>Energy consumption for flight</td></tr><tr><td rowspan=1 colspan=2>m1,n2,n3,n4</td><td rowspan=1 colspan=1>Constants depend on the aerodynamic parametersof UAV</td><td rowspan=1 colspan=1> $\overline { { E _ { j } ^ { p } } }$ </td><td rowspan=1 colspan=1>unit propulsion energy for UAV j</td></tr><tr><td rowspan=1 colspan=2> $\overline { { s ^ { \mathrm { u n d e } } , s ^ { \mathrm { q u e u } } , s ^ { \mathrm { p r o c } } , s ^ { \mathrm { s u c c } } , s ^ { \mathrm { f a i l } } } }$ </td><td rowspan=1 colspan=1>The processing state of each task</td><td rowspan=1 colspan=1> $\overline { { v _ { c } ^ { \mathrm { t i p } } } }$ </td><td rowspan=1 colspan=1>The tip speed of the rotor blade</td></tr><tr><td rowspan=1 colspan=2> $\overline { { o _ { i , n } ^ { t } , n \in \mathcal { N } = \{ i , b \} \cup \mathcal { U } } }$ </td><td rowspan=1 colspan=1>Variableof offloading decision</td><td rowspan=1 colspan=1>ä¸­</td><td rowspan=1 colspan=1>The remaining lifespan of task</td></tr><tr><td rowspan=1 colspan=2> $\overline { { E _ { i } ^ { \mathrm { m a x } } / E _ { i } ^ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>The energy constraint of MDi/MEC server j</td><td rowspan=1 colspan=1> $\dot { \overline { { D ^ { t } } } }$ </td><td rowspan=1 colspan=1>Total completion delay</td></tr><tr><td rowspan=1 colspan=2>Et</td><td rowspan=1 colspan=1>System energy consumption</td><td rowspan=1 colspan=1> $\overline { { C ^ { t } , { \overline { { C ^ { t } } } } } }$ </td><td rowspan=1 colspan=1>System cost</td></tr><tr><td rowspan=1 colspan=2>O,F,Q</td><td rowspan=1 colspan=1>The strategies of computation offloading, comput-ingresourceallocation,and UAV trajectorycontrol</td><td rowspan=1 colspan=1> $p _ { j , i } ^ { t }$ </td><td rowspan=1 colspan=1>The unit price of computing resourcepaid byMDi</td></tr><tr><td rowspan=1 colspan=2> $\overline { { U _ { i , n } ^ { t } } }$ </td><td rowspan=1 colspan=1>The QoEachievedbyMDi</td><td rowspan=1 colspan=1> $\overline { { G _ { i } ^ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>The budget of MD i</td></tr><tr><td rowspan=1 colspan=2> $\overline { { U _ { j , i } ^ { t } } }$ </td><td rowspan=1 colspan=1>The revenue gained by MEC server j</td><td rowspan=1 colspan=1> $\dot { \overline { { U ^ { t } } } }$ </td><td rowspan=1 colspan=1>Systemutility</td></tr><tr><td rowspan=1 colspan=2> $V _ { { \kappa } _ { i } ^ { \mathrm { t } } , j ^ { \prime } } ^ { t } V _ { j , { \kappa } _ { i } ^ { \mathrm { t } } }$ </td><td rowspan=1 colspan=1>Preference values</td><td rowspan=1 colspan=1> $\overline { { f _ { j } ^ { t , \mathrm { a v I } } } }$ </td><td rowspan=1 colspan=1>Available computing resources</td></tr><tr><td rowspan=1 colspan=2> $\begin{array} { r } { \overline { { { \xi _ { i , i } ^ { t } } ^ { * } , { \xi _ { j , i } ^ { t } } ^ { * } , { \xi _ { i , j } ^ { t } } ^ { * } , { \xi _ { j , j } ^ { t } } ^ { * } } } } \end{array}$ </td><td rowspan=1 colspan=1>Satisfied partitions of the surplus</td><td rowspan=1 colspan=1> $\overline { { \lambda _ { i } ^ { t } , \lambda _ { j } ^ { t } } }$ </td><td rowspan=1 colspan=1>Discount factor</td></tr><tr><td rowspan=1 colspan=2> $\overline { { ( \mathcal { M } ^ { t } , \mathcal { L } ^ { t } , \Pi ^ { t } ) } }$ </td><td rowspan=1 colspan=1>Current matching</td><td rowspan=1 colspan=1> $\underline { { \pi _ { j , i } ^ { t } } }$ </td><td rowspan=1 colspan=1>The surplus of resource price</td></tr></table>

<!-- image-->  
Fig. 1. The architecture of computing resource allocation, computation offloading, and UAV trajectory control for UAV-assisted MEC system.

In the temporal dimension, we consider that the system operates in a two-timescale manner since the dynamic characteristics for channel state information (CSI), task arrival of MDs, and workload update of edge servers vary in a fine-grained timescale, while the mobility of MDs varies in a long timescale [24]. Specifically, the system time horizon is discretized into $T$ time slots $\mathcal { T } = \dot { \{ 1 , \dots , t , \dots , T \} }$ with equal slot duration $\delta ,$ which = 1is consistent with the coherence block of the wireless channel [24]. Furthermore, every $\Delta$ consecutive slots are combined into a time epoch indexed by $t _ { 0 } \in \mathcal { T } _ { 0 } = \{ 1 , . . . , T _ { 0 } \}$ , where each time epoch is denoted as $\mathcal { T } ( t _ { 0 } ) = \{ ( t _ { 0 } - 1 ) \Delta + \mathrm { 1 } , \dots , t _ { 0 } \Delta \}$ ( ) = ( 1)Î + 1 ÎHere,  is selected to be sufficiently small to guarantee that Îthe location of UAV is approximately constant within each epoch. Therefore, in the short timescale, the CSI, offloading requirements of MDs, and states of MEC servers are captured and updated, and the decisions of task offloading and computing resource allocation are decided. In the long timescale, the mobility states of MDs are captured and updated, and the UAV trajectory planning is decided.

2) Basic Models: The basic models of the system are given as follows.

(1) MD Mobility Model: The horizontal coordinate of each $\mathrm { { M D } } i \in \mathcal { I }$ is denoted as $\mathbf { q } _ { i , t } = [ x _ { i } ^ { t } , y _ { i } ^ { t } ] _ { i \in \mathbb { Z } } ^ { \mathrm { T } }$ . Moreover, we adopt = [ ]the Gauss Markov model to capture the temporal-dependent randomness in the movement of MDs. Specifically, the velocity of MD i at time epoch $t _ { 0 } + 1$ (i.e., time slot $( t _ { 0 } + 1 ) \Delta )$ can be given as:

$$
\mathbf { v } _ { i } ^ { ( t _ { 0 } + 1 ) \Delta } = \alpha \mathbf { v } _ { i } ^ { t _ { 0 } \Delta } + \left( 1 - \alpha \right) \bar { \mathbf { v } } + \bar { \sigma } \sqrt { 1 - \alpha ^ { 2 } } \mathbf { w } _ { i } ,\tag{1}
$$

where $\mathbf { v } _ { i } ^ { t _ { 0 } \Delta }$ is the velocity vector at time epoch $t _ { 0 }$ and $\mathbf { w } _ { i }$ is the uncorrelated random Gaussian process, i.e., $\mathbf { w } _ { i } \sim f ^ { \mathrm { G u a } } ( 0 , \bar { \sigma } ^ { 2 } )$ Besides, $0 \leq \alpha \leq 1$ , v, and $\bar { \sigma }$ (0 Â¯ )denote the memory degree, 0 1 Â¯ Â¯asymptotic mean, and asymptotic standard deviation of velocity, respectively. Therefore, the location of each MD can be updated as:

$$
\mathbf { q } _ { i } ^ { ( t _ { 0 } + 1 ) \Delta } = \mathbf { q } _ { i } ^ { t _ { 0 } \Delta } + \mathbf { v } _ { i } ^ { t _ { 0 } \Delta } \delta \Delta , ~ \forall i \in \mathcal { I } , t _ { 0 } \in \mathcal { T } _ { 0 } .\tag{2}
$$

(2) UAV Mobility Model: We consider that each $\mathrm { U A V } ~ j \in \mathcal { U }$ flies at a fixed altitude of H with the instantaneous horizontal coordinate of $\mathbf { q } _ { j } ^ { t } = [ x _ { j } ^ { t } , y _ { j } ^ { t } ] _ { j \in \mathcal { U } } ^ { T } [ 8 ]$ . Therefore, the location of = [ ]each UAV can be updated as follows:

$$
\mathbf { q } _ { j } ^ { ( t _ { 0 } + 1 ) \Delta } = \mathbf { q } _ { j } ^ { t _ { 0 } \Delta } + \mathbf { v } _ { j } ^ { t _ { 0 } \Delta } \delta \Delta , \forall j \in \mathcal { U } , t _ { 0 } \in \mathcal { T } _ { 0 } ,\tag{3}
$$

where $\mathbf { v } _ { i } ^ { t _ { 0 } \Delta }$ denotes the velocity of UAV j at time epoch $t _ { 0 }$ Furthermore, the position of each UAV should satisfy several practical constraints as follows:

$$
0 \leq x _ { j } ^ { t } \leq x ^ { \operatorname* { m a x } } , \forall j \in \mathcal { U } , t \in \mathcal { T } ,\tag{4a}
$$

$$
0 \leq y _ { j } ^ { t } \leq y ^ { \operatorname* { m a x } } , \quad \forall j \in \mathcal { U } , t \in \mathcal { T } ,\tag{4b}
$$

$$
\mathbf { q } _ { j } ^ { 1 } = \mathbf { q } _ { j } ^ { I } , \mathbf { q } _ { j } ^ { T _ { 0 } \Delta } = \mathbf { q } _ { j } ^ { F } , \forall j \in \mathcal { U } ,\tag{4c}
$$

$$
\begin{array} { r } { \lvert | \mathbf { q } _ { j } ^ { ( t _ { 0 } + 1 ) \Delta } - \mathbf { q } _ { j } ^ { t _ { 0 } \Delta } \rvert | \leq v _ { \mathrm { U } } ^ { \operatorname* { m a x } } \delta \Delta , \forall j \in \mathcal { U } , t _ { 0 } \in \mathcal { T } _ { 0 } , } \end{array}\tag{4d}
$$

$$
| | \mathbf { q } _ { j } ^ { F } - \mathbf { q } _ { j } ^ { t _ { 0 } \Delta } | | \leq v _ { \mathrm { U } } ^ { \operatorname* { m a x } } ( T _ { 0 } - t _ { 0 } ) \delta \Delta , \forall j \in \mathcal { U } , t _ { 0 } \in \mathcal { T } _ { 0 } ,\tag{4e}
$$

$$
\begin{array} { r } { | | \mathbf q _ { j } ^ { t _ { 0 } \Delta } - \mathbf q _ { j ^ { \prime } } ^ { t _ { 0 } \Delta } | | \geq d _ { \mathrm U } ^ { \mathrm { s a f e } } , \forall j , j ^ { \prime } \in \mathcal U , j \neq j ^ { \prime } , t _ { 0 } \in \mathcal T _ { 0 } , } \end{array}\tag{4f}
$$

where $v _ { U } ^ { \mathrm { m a x } }$ is the maximum velocity of UAV. Furthermore, Constraints (4a) and (4b) guarantee that each UAV cannot fly beyond the boundary of the considered area. Moreover, the initial and final positions of UAV j are predetermined by Constraints $\mathbf { q } _ { j } ^ { I }$ and $\mathbf { q } _ { j } ^ { F }$ , respectively, as given in Constraint (4c) [25]. In addition, Constraints (4d) and (4e) indicate that the flight distance of a UAV is constrained by the maximum velocity. Finally, each UAV should keep the minimum safe distance of $d _ { \mathrm { U } } ^ { \mathrm { s a f e } }$ with the other UAVs to avoid collision, as given in Constraint (4f).

(3) MD Model: Each MD i is characterized by the tuple $< f _ { i } ^ { \mathrm { m a x } } , n _ { i } ^ { \mathrm { c o r e } } , E _ { i } ^ { \mathrm { m a x } } , \zeta _ { i } ^ { t } , K _ { i } ^ { t } >$ , where $f _ { i } ^ { \mathrm { m a x } }$ represents the computation capability of MD i (in cycles/s), $n _ { i } ^ { \mathrm { c o r e } }$ denotes the number of CPU core of MD $i , E _ { i } ^ { \mathrm { m a \bar { x } } }$ denotes the energy constraint of MD $i , \zeta _ { i } ^ { t } \in \{ 0 , 1 \}$ is a binary variable that indicates whether 0 1a task is generated by MD i during time slot $t ,$ and $\mathcal { K } _ { i } ^ { t }$ denotes the task generated by MD i in time slot t. Specifically, each MD could generate one task $( \zeta _ { i } ^ { t } = 1 )$ or not $( \zeta _ { i } ^ { \bar { t } } = 0 )$ in time slot t. = 1 = 0Furthermore, due to the resource limitation, we assume that each MD is equipped with a single CPU core, $\mathrm { i . e . , } n _ { i } ^ { \mathrm { c o r e } } = 1 [ 2 6 ]$ .

= 1(4) Server Model: Similar to [26], we consider that each MEC server $j \in \{ b , \mathcal { U } \}$ are equipped with multi-core CPUs to enable parallel processing of multiple tasks. Consequently, each MEC server is characterized by the tuple $< n _ { j } ^ { \mathrm { c o r e } } , f _ { j } ^ { \mathrm { n a x } } , E _ { j } ^ { \mathrm { m a x } } > ,$ where $n _ { j } ^ { \mathrm { c o r e } }$ denotes the number of CPU cores, each of the CPU cores assumed to have homogeneous computational resources of $f _ { j } ^ { \mathrm { m a x } } \ \mathrm { ( c y c l e s / s ) }$ , and $E _ { j } ^ { \mathrm { m a x } }$ denotes the energy constraint of MEC server j.

(5) Computation Task Model: MDs have heterogeneous requirements on diverse computation tasks due to distinct task characteristics. Specifically, the task generated by MD i in time slot t is characterized by $\dot { \mathcal { K } } _ { i } ^ { t } = \langle l _ { i } ^ { t } , \mu _ { i } ^ { \top } , \tau _ { i } ^ { t } \rangle$ , where $l _ { i } ^ { t }$ is the task size, $\mu _ { i } ^ { t }$ =is the computation intensity (in cycles/bit), and $\boldsymbol { \tau } _ { i } ^ { t }$ is the deadline of the task.

## B. Communication Model

By adopting the widely used orthogonal frequency division multiple access (OFDMA), the instantaneous uplink data rate between MD $i \in \mathcal { T }$ and MEC server $j \in \{ b \} \cup \dot { U }$ can be given as:

$$
r _ { i , j } ^ { t } = B _ { i , j } \log _ { 2 } \left( 1 + \frac { P _ { i } ^ { t } g _ { i , j } ^ { t } } { N _ { 0 } } \right) ,\tag{5}
$$

where $B _ { i , j }$ is the subchannel bandwidth between MD i and MEC server $j , \tilde { P } _ { i } ^ { t }$ is the transmit power of MD i in time slot $t , N _ { 0 }$ is the noise power, and $g _ { i , j } ^ { t }$ is the instantaneous channel power gain between MD i and MEC server j.

Due to the complex nature of the communication environment in UAV-assisted MEC networks, such as the movement of MDs and UAVs, and the occasional blockages caused by obstacles, the channel power gain between MD i and MEC server $j$ is calculated by incorporating the commonly used probabilistic LoS channel with the large-scale and small-scale fadings as:

$$
g _ { i , j } ^ { t } = \mathbb { P } _ { i , j } ^ { t } g _ { i , j } ^ { t , \mathrm { L } } + ( 1 - \mathbb { P } _ { i , j } ^ { t } ) g _ { i , j } ^ { t , \mathrm { N L } } ,\tag{6}
$$

where $\mathbb { P } _ { i , j } ^ { t }$ denotes the probability of LoS transmission, $g _ { i , j } ^ { t , x }$ denotes the channel power gain between MD i and MEC server j, and $x \in \{ \mathrm { L } , \mathrm { N } \}$ represents LoS or non-line of sight (NLoS) L Nlinks. Moreover, the details of $\mathbb { P } _ { i , j } ^ { t }$ and $g _ { i , j } ^ { t , x }$ are presented as follows.

1) LoS Probability: For the MD-MBS link, according to the 3GPP standard [27], the probability of LoS transmission can be given as follows:

$$
\mathbb { P } _ { i , j } ^ { t } = \operatorname* { m i n } \left( \frac { d _ { 1 } } { d _ { i , j } ^ { t } } , 1 \right) \left( 1 - e ^ { - \frac { d _ { i , j } ^ { t } } { d _ { 2 } } } \right) + e ^ { - \frac { d _ { i , j } ^ { t } } { d _ { 2 } } } , j = b ,\tag{7}
$$

where $d _ { i , j } ^ { t }$ is the instantaneous distance between MD i and the MBS j. Besides, $d _ { 1 }$ and $d _ { 2 }$ are the parameters to fit the specific scenarios. Furthermore, for the MD-UAV link, an extensively employed LoS probability is calculated as [28]:

$$
\mathbb { P } _ { i , j } ^ { t } = \frac { 1 } { 1 + p _ { 1 } \mathrm { e } ^ { \left( - p _ { 2 } \left( \frac { 1 8 0 } { \pi } \arcsin \left( \frac { H } { d _ { i , j } ^ { t } } \right) - p _ { 1 } \right) \right) } } , j \in \mathcal { U } ,\tag{8}
$$

where $d _ { i , j } ^ { t }$ is the horizontal distance between MD i and UAV $j .$ Moreover, $p _ { 1 }$ and $p _ { 2 }$ denote the environment-dependent parameters.

2) Channel Power Gain: According to [29], the channel power gain between MD i and MEC server j in time slot t can be uniformly given as $g _ { i , j } ^ { t , x } = | h _ { i , j } ^ { t , x } | ^ { 2 } ( L _ { i , j } ^ { t , x } ) ^ { - 1 }$ , where $h _ { i , j } ^ { t , x }$ and $L _ { i , j } ^ { t , x }$ = ( )denotes the parameters of small-scale fading and large-scale fading, respectively, which are presented in detail as follows.

First, the small-scale fading for both MD-MBS and MD-UAV communications in time slot t is modeled as a parametricscalable and good-fitting generalized fading, i.e., Nakagami-m fading [30], which is given as:

$$
\begin{array} { r l } & { h _ { i , j } ^ { t , x } \sim f ^ { \mathrm { N a k } } \left( h _ { i , j } ^ { t , x } , m _ { y } ^ { x } \right) } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \Gamma ( m _ { y } ^ { x } ) ( \overline { { p } } ) ^ { m _ { y } ^ { x } } } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \Gamma ( m _ { y } ^ { x } ) ( \overline { { p } } ) ^ { m _ { y } ^ { x } } } \end{array} , ~ j \in \{ b , \mathcal { U } \} ,\tag{9}
$$

where $\overline { { p } }$ is the average received power, $\Gamma ( \cdot )$ is the Gamma function, and $m _ { y } ^ { x } \in \{ \breve { m } _ { \mathrm { T } } ^ { \mathrm { L } } , m _ { \mathrm { T } } ^ { \mathrm { N } } , m _ { \mathrm { A } } ^ { \mathrm { L } } , m _ { \mathrm { A } } ^ { \mathrm { N } } \}$ Î( )is the Nakagami-m fading parameters for terrestrial/aerial LoS/NLoS channel.

Furthermore, the large-scale fading for MD-MBS communication in time slot t can be given as:

$$
L _ { i , j } ^ { t , x } = \frac { ( 4 \pi d _ { 0 } ^ { \mathrm { T } } f _ { c } ) ^ { 2 } } { c ^ { 2 } } \left( \frac { d _ { i , j } ^ { t } } { d _ { 0 } ^ { \mathrm { T } } } \right) ^ { \beta _ { \mathrm { T } } ^ { x } } \chi ^ { x } , \ j = b ,\tag{10}
$$

where $d _ { 0 } ^ { \mathrm { T } }$ is the reference distance for the communication between MD and terrestrial MEC server, c denotes the light speed, $f _ { c }$ is the carrier frequency, $\beta _ { \mathrm { T } } ^ { x } \in \{ \beta _ { \mathrm { T } } ^ { \mathrm { L } } , \beta _ { \mathrm { T } } ^ { \mathrm { N } } \}$ is the path loss exponent for LoS/NLoS channel between MD i and the MBS j, and $\boldsymbol { \chi } ^ { x } \in \{ \boldsymbol { \chi } ^ { \mathrm { L } } , \boldsymbol { \chi } ^ { \mathrm { N } } \}$ denotes the standard deviation of shadowing for LoS/NLoS transmission [29], which follows the zero-mean Gaussian distributed random variable, ${ \mathrm { i . e . , } } \chi ^ { x } \sim f ^ { \mathrm { G u a } } ( 0 , ( \sigma ^ { x } ) ^ { 2 } )$

(0 ( ) )Besides, the large-scale fading for MD-UAV communication in time slot t can be given as:

$$
L _ { i , j } ^ { t } = \frac { ( 4 \pi d _ { 0 } ^ { A } f _ { c } ) ^ { 2 } } { c ^ { 2 } \kappa } \left( \frac { d _ { i , j } ^ { t } } { d _ { 0 } ^ { \mathrm { A } } } \right) ^ { \beta _ { \mathrm { A } } } , j \in \mathcal { U } ,\tag{11}
$$

where $d _ { 0 } ^ { \mathrm { A } }$ is the reference distance for the communication between MD i and the UAV j, $\beta _ { \mathrm { { A } } }$ is the path loss exponent of MD-UAV communication, and Îº is the additional attenuation factor due to the NLoS link.

## C. Computation Model

Each MD is capable of performing local computing and computation offloading simultaneously, as the communication circuit and computation unit are separate [31]. Both local computing and computation offloading generally incur overheads in terms of delay and energy consumption, which are detailed in the following subsections.

1) Local Computing Model: The completing delay and energy consumption for local computing are given as follows.

(1) Completion Delay: When task $\mathcal { K } _ { i } ^ { t }$ is executed locally by MD i, the task completion delay is mainly incurred by task computation, which can be given as follows:

$$
D _ { i , i } ^ { t } = \frac { \mu _ { i } ^ { t } } { f _ { i } ^ { t } } ,\tag{12}
$$

where $f _ { i } ^ { t }$ is the available computing resources of MD i in time slot t.

(2) Energy Consumption: Correspondingly, the energy consumption of MD i to execute task ${ \bf \mathcal { K } } _ { i } ^ { t }$ locally is given as:

$$
E _ { i , i } ^ { t } = \gamma _ { i } ( f _ { i } ^ { t } ) ^ { 2 } \mu _ { i } ^ { t } ,\tag{13}
$$

where $\gamma _ { i } \geq 0$ denotes the effective capacitance of MD iâs CPU 0that depends on the CPU chip architecture [32], [33].

2) Edge Offloading Model: The completing delay and energy consumption for edge offloading are given as follows.

(1) Completion Delay: When task $\mathcal { K } _ { i } ^ { t }$ is offloaded to MEC server $j$ for remote processing, the task completion delay mainly consists of transmission delay and computation delay, i.e.,

$$
\begin{array} { r } { D _ { i , j } ^ { t } = D _ { i , j } ^ { \mathrm { t r a } , t } + D _ { i , j } ^ { \mathrm { e x e } , t } , } \end{array}\tag{14}
$$

where $D _ { i , j } ^ { \mathrm { t r a } , t } = l _ { i } ^ { t } / r _ { i , j } ^ { t }$ represents the transmission delay that the task is uploaded from MD i to MEC server j. Moreover, $D _ { i , j } ^ { \mathrm { e x e , } t } =$ $\mu _ { i } ^ { t } / f _ { j , } ^ { t }$ represents the computation delay at MEC server $j ,$ which depends on the computing resources $f _ { j , i } ^ { t }$ allocated by MEC server $j$ in time slot t.

Remark 1: We consider the queuing delay in the process of task processing when the task arrives at the MEC server that is busy, which is detailed in Section A of the supplementary material.

(2) Energy Consumption: The remote execution of task $\mathcal { K } _ { i } ^ { t }$ on MEC server j could result in transmission energy consumption for the MD, computation energy consumption for the MEC server, and flight energy consumption for the UAV. For MD $i \in \mathcal { Z } ,$ , the energy consumed for task uploading is as

follows:

$$
E _ { i , j } ^ { t } = \frac { P _ { i } ^ { t } l _ { i } ^ { t } } { r _ { i , j } ^ { t } } .\tag{15}
$$

For MEC server j, the energy consumption for task execution can be given as:

$$
E _ { j , i } ^ { t , \mathrm { c o m p } } = \gamma _ { j } ( f _ { j , i } ^ { t } ) ^ { 2 } \mu _ { i } ^ { t } ,\tag{16}
$$

where $\gamma _ { j } \geq 0$ denotes the effective capacitance of terrestrial MEC server $j ^ { \prime } \mathbf { s }$ CPU [32], [33].

For aerial MEC server j, energy consumption also occurs during flight. Specifically, the energy consumption of a UAV flying to a new position during each time slot is given as:

$$
E _ { j } ^ { t , \mathrm { f l y } } = E _ { j } ^ { p } \delta ,\tag{17}
$$

where $E _ { j } ^ { p }$ denotes the unit propulsion energy of the rotary-wing UAV in straight-and-level flight includes the components of blade profile power, induced power, and parasite power [34], which can be given as:

$$
\begin{array} { r l } & { E _ { j } ^ { p } = } \\ & { \underbrace { \eta _ { 1 } \left( 1 + \frac { 3 ( v _ { j } ^ { t } ) ^ { 2 } } { v _ { j } ^ { \mathrm { i i p } ^ { 2 } } } \right) } _ { \mathrm { B l a d e p r o f i l e p o w e r } } + \underbrace { \eta _ { 2 } \sqrt { \sqrt { \eta _ { 3 } + \frac { ( v _ { j } ^ { t } ) ^ { 4 } } { 4 } } - \frac { ( v _ { j } ^ { t } ) ^ { 2 } } { 2 } } } _ { \mathrm { I n d u c e d p o w e r } } \underbrace { + \eta _ { 4 } ( v _ { j } ^ { t } ) ^ { 3 } } _ { \mathrm { P a r a s i t e p o w e r } } , } \end{array}\tag{18}
$$

where $v _ { j } ^ { \mathrm { t i p } }$ denotes the tip speed of the rotor blade. Moreover, $\eta _ { 1 }$ Î· $\eta _ { 2 } , \eta _ { 3 }$ , and $\eta _ { 4 }$ are the constants that depend on the aerodynamic parameters of the UAV. Therefore, it can be obtained form (18) that the energy consumption of each UAV flying from the initial point to the destination point over the entire timeline is the cumulative energy consumed to reach a set of new locations.

According to (15) and (17), the energy consumption of UAV $j$ to provide computation service for task $\mathcal { K } _ { i } ^ { t }$ can be concluded as:

$$
E _ { j , i } ^ { t } = \left\{ \begin{array} { l l } { \gamma _ { j } ( f _ { j , i } ^ { t } ) ^ { 2 } \mu _ { i } ^ { t } , } & { j = b , } \\ { \gamma _ { j } ( f _ { j , i } ^ { t } ) ^ { 2 } \mu _ { i } ^ { t } + E _ { j } ^ { p } \delta , } & { j \in \mathcal { U } . } \end{array} \right.\tag{19a}
$$

(19b)

Note that the delay and energy consumption of the result feedback are neglected since the result of a task is generally much smaller than that of the input [35].

Remark 2: We omit the costs of information gathering for SDN controller due to the relatively small size of information and low costs of transmission, and the reasons are as follows. On the one hand, the data gathered by the controller, which primarily consists of state information including the task requirements and the status of edge server resources, is typically lightweight compared to the tasks [36], [37]. On the other hand, each MEC server distributedly collects the information from MDs within its communication range, and subsequently transmits it to the controller through fiber links, resulting in low transmission costs for both fronthaul and backhaul links.

## D. System Cost Model

In this section, we present the system cost models for completion delay and energy consumption.

1) Completion Delay Model: First, we denote the offloading decision as a binary variable $o _ { i , n } ^ { t } \in \{ 0 , 1 \} , n \in \mathcal { N } = \{ i , b \} \cup \bar { \mathcal { U } } _ { }$ which indicates that task $\mathcal { K } _ { i } ^ { t }$ of MD i is processed locally $( o _ { i , i } ^ { t } =$ ) or offloaded to MEC server $j \in \{ b \} \cup U \ ( o _ { i , j } ^ { t } = 1 )$ in time 1 = 1slot t. Since the total completion delay consists of the delay for local computing and the delay for edge offloading, the total completion delay for MDs can be given by combining (12) and (14), i.e.,

$$
\begin{array} { l } { { \displaystyle { D } ^ { t } = \sum _ { i \in \mathcal { I } } \zeta _ { i } ^ { t } \left( o _ { i , i } ^ { t } D _ { i , i } ^ { t } + \sum _ { j \in \{ b \} \cup \mathcal { U } } o _ { i , j } ^ { t } D _ { i , j } ^ { t } \right) } } \\ { { \displaystyle \quad = \sum _ { i \in \mathcal { T } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } D _ { i , n } ^ { t } . } } \end{array}\tag{20}
$$

2) Energy Consumption Model: The system energy consumption include the energy consumption of MDs for task computing and task uploading, the energy consumption of MEC servers for task execution, and the energy consumption of UAV flying. Therefore, the system energy consumption can be calculated according to (15), (16), and (17), i.e.,

$$
\begin{array} { c } { E ^ { t } = \displaystyle \sum _ { i \in \mathcal { Z } } \zeta _ { i } ^ { t } \left( o _ { i , i } ^ { t } E _ { i , i } ^ { t } + \displaystyle \sum _ { j \in b \cup \mathcal { U } } o _ { i , j } ^ { t } \left( E _ { i , j } ^ { t } + E _ { j , i } ^ { t } \right) \right) } \\ { = \displaystyle \sum _ { i \in \mathcal { T } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } E _ { i , n } ^ { t } + \displaystyle \sum _ { i \in \mathcal { T } } \sum _ { j \in b \cup \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } E _ { j , i } ^ { t } . } \end{array}\tag{21}
$$

3) System Cost Model: With the discrepancy in the magnitudes of units between delay and energy consumption, the system cost is formulated as the sum of the normalized delay and normalized energy consumption based on (20) and (21), which is given as:

$$
\begin{array} { l } { { \displaystyle C ^ { t } = \sum _ { i \in \mathbb { Z } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } \frac { D _ { i , n } ^ { t } } { \tau _ { i } ^ { t } } + \sum _ { i \in \mathbb { Z } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } \frac { E _ { i , n } ^ { t } } { E _ { i } ^ { \operatorname* { m a x } } } } } \\ { { \displaystyle ~ + \sum _ { i \in \mathbb { Z } } \sum _ { j \in b \cup \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } \frac { E _ { j , i } ^ { t } } { E _ { j } ^ { \operatorname* { m a x } } } } , } \end{array}\tag{22}
$$

where $E _ { i } ^ { \mathrm { m a x } }$ and $E _ { j } ^ { \mathrm { m a x } }$ represent the energy constraints of MD i and MEC server j, respectively.

## E. Problem Formulation

The optimization problem is formulated to minimize the system cost over T slots by jointly determining the computation offloading strategy $\mathbf { O } = \{ \bar { o } _ { i , n } ^ { \bar { t } } \} _ { i \in \mathcal { T } , n \in \mathcal { N } , t \in \mathcal { T } } ,$ computing resource allocation and pricing strategy $\mathbf { F } = \{ f _ { j , i } ^ { t } , p _ { j , i } ^ { t } \} _ { i \in \mathbb { Z } , j \in \{ b \} }$ âªU,tâT, and UAV trajectory $\mathbf { Q } = \{ \mathbf { q } _ { u } ^ { t } \} _ { j \in \mathcal { U } , t \in \mathcal { T } } .$ Therefore, the problem can be formulated as:

$$
\mathbf { P _ { 0 } } : \quad \operatorname* { m i n } _ { \mathbf { O , F , Q } } \sum _ { t = 1 } ^ { T } C ^ { t } ,\tag{23a}
$$

$$
\mathrm { s . t . } \sigma _ { i , n } ^ { t } \in \{ 0 , 1 \} , \forall i \in \mathbb { Z } , n \in \mathcal { N } , t \in \mathcal { T } ,\tag{23b}
$$

$$
\sum _ { n \in \mathcal { N } } o _ { i , n } ^ { t } \leq 1 , \forall i \in \mathcal { T } , t \in \mathcal { T } ,\tag{23c}
$$

$$
\zeta _ { i } ^ { t } = \{ 0 , 1 \} , \forall i \in \mathcal { T } , t \in \mathcal { T } ,\tag{23d}
$$

$$
o _ { i , n } ^ { t } D _ { i , n } ^ { t } \leq \tau _ { i } ^ { t } , \forall i \in \mathbb { Z } , j \in \{ b \} \cup \mathcal { U } , n \in \mathcal { N } , t \in \mathcal { T } ,\tag{23e}
$$

$$
\sum _ { i \in \mathbb { Z } } o _ { i , j } ^ { t } f _ { j , i } ^ { t } \le f _ { j } ^ { \operatorname* { m a x } } , \quad \forall j \in \{ b \} \cup \mathcal { U } , t \in \mathbb { T } ,\tag{23f}
$$

$$
\sum _ { i \in \mathcal { I } } o _ { i , j } ^ { t } \le n _ { j } ^ { \mathrm { c o r e } } , \forall j \in \{ b \} \cup \mathcal { U } , t \in \mathcal { T } ,\tag{23g}
$$

$$
o _ { i , j } ^ { t } c _ { j , i } ^ { t } f _ { j , i } ^ { t } \le G _ { i } ^ { \operatorname* { m a x } } , \forall i \in \mathcal { T } , j \in \{ b \} \cup \mathcal { U } , t \in \mathcal { T } ,\tag{23h}
$$

$$
\varphi _ { i } ^ { t } = \varphi _ { i } ^ { t } - \delta , \varphi _ { i } ^ { t } > 0 ,\tag{23i}
$$

$$
( 1 ) \sim ( 4 ) .\tag{23j}
$$

Constraints (23b) and (23c) indicate that the offloading strategy for each task is binary. Constraint (23d) means that each MD generates at most one task in each time slot. Constraint (23e) ensures that the delay of completing the task should not exceed the deadline. Constraints (23f) and $( 2 3 \mathrm { g } )$ constrain the computing resources and the number of CPU cores, respectively, for MEC server. Constraint (23h) guarantees that the price paid by each MD to the MEC server should not exceed its budget. Moreover, Constraint (23i) indicates that the limit and update for the remaining lifespan of the computation task. In addition, Constraint (23j) limits the mobility of MDs and UAVs.

It can be deduced from Theorem 1 that it is difficult to find an optimal solution to problem $\mathbf { P _ { 0 } }$

Theorem 1: Problem P is a non-convex and NP-hard MINLP. Proof: The detailed proof is given is Appendix B of the supplemental material, available online.

## F. Problem Reformulation

Optimizing the system cost $C ^ { t }$ is still challenging because MDs and MEC servers have different priorities for delay and energy consumption, and optimizing delay and energy often leads to conflict. Therefore, in this section, we transform the system cost model into utility model by establishing a relationship between delay and energy consumption from the perspectives of MDs and MEC servers

1) System Cost Model Analysis: MDs and MEC servers have different priorities for delay and energy consumption. Specifically, MDs prioritize minimizing the task completion delay due to the time-sensitive nature of their tasks. In contrast, MEC servers focus on minimizing energy consumption due to their limited computing resources. Therefore, we model system cost $C ^ { t }$ by reorganizing the performance metrics from the perspectives of MDs and MEC servers as follows:

$$
\begin{array} { r l } { \overline { { C ^ { t } } } = \underbrace { \sum _ { i \in \overline { { Z } } } \displaystyle \sum _ { n \in \mathsf { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } \frac { D _ { i , n } ^ { t } } { D _ { i } ^ { \operatorname* { m a x } } } } _ { \mathrm { c o m p l e t i o n ~ d e l a y ~ f o r ~ M D s } } + \underbrace { \sum _ { i \in \overline { { Z } } } \displaystyle \sum _ { n \in \mathsf { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } \frac { E _ { i , n } ^ { t } } { E _ { i } ^ { \operatorname* { m a x } } } } _ { \mathrm { E n e r g y ~ c o n s u m p t i o n ~ f o r ~ M D s } } } & { } \\ { + \underbrace { \sum _ { i \in \overline { { Z } } } \displaystyle \sum _ { j \in b \cup \{ i \} } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } \frac { E _ { j , i } ^ { t } } { E _ { j } ^ { \operatorname* { m a x } } } } _ { \mathrm { E n e r g y ~ c o n s u m p l i o n ~ f o r ~ M E C ~ s e r v e r s } } } & { } \end{array}
$$

$$
= \underbrace { \sum _ { i \in \mathcal { Z } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } \left( \frac { D _ { i , n } ^ { t } } { D _ { i } ^ { \operatorname* { m a x } } } + \frac { E _ { i , n } ^ { t } } { E _ { i } ^ { \operatorname* { m a x } } } \right) } _ { i \in \mathcal { I } } + \underbrace { \sum _ { i \in \mathcal { T } } \sum _ { j \in b \cup \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } \frac { E _ { j , i } ^ { t } } { E _ { j } ^ { \operatorname* { m a x } } } } _ { i \in \mathcal { N } }
$$

$$
= C _ { 1 } + C _ { 2 } .\tag{24}
$$

Moreover, optimizing the objective function $\overline { { C ^ { t } } }$ is still challenging since optimizing delay and energy consumption can often conflict. Specifically, reducing the task completion delay typically requires higher allocations of computing resources, which in turn leads to increased energy consumption. Conversely, efforts to decrease energy consumption often involve reducing the computing resources allocated, which can result in increased delays. Moreover, increasing the flight speed of UAVs to reduce service delays leads to higher energy expenditures, while slowing down the UAVs to save energy can extend the delay. Thus, this trade-off necessitates a careful balance between delay and energy consumption.

Based on the discussions above, we aim to establish a relationship between delay and energy consumption from the perspectives of MDs and MEC servers. Specifically, we can observe from (24) that while $C _ { 1 }$ quantifies the delay and energy consumption for MDs, it does not include the metrics of MEC servers. Conversely, $C _ { 2 }$ is related to the energy consumption of MEC servers without connection to the metrics of MDs. Therefore, to bridge the relationship between $C _ { 1 }$ and $C _ { 2 } ,$ we introduce the price of computing resources. This is motivated by the advantages of the price-incentive model, which can facilitate the interaction between MDs and MEC servers on resource pricing, thereby achieving on-demand computing resource allocation.

2) Utility Model: Based on the abovementioned motivations, we aim to establish the system utility to bridge $C _ { 1 }$ and $C _ { 2 }$ by employing the price incentive.

QoE of MDs: For MDs, $C _ { 1 }$ is transformed into the sum of QoE of MDs. Specifically, the QoE achieved by MD i in time slot t is calculated as the difference between the satisfaction degree from task completion and the costs associated with task offloading. Moreover, the costs consist of the energy consumption and the fees paid to the MEC server, which depend on the offloading decision. Therefore, the QoE achieved by MD i in time slot t is calculated as follows:

$$
\begin{array} { r l } & { U _ { i , n } ^ { t } = w _ { i } \underbrace { \frac { \log \left( 1 + \pi _ { i } ^ { t } - D _ { i , n } ^ { t } \right) } { \log \left( 1 + \tau _ { i } ^ { t } \right) } } _ { \mathrm { S a t i s f u e n o t a g e } } - ( 1 - w _ { i } ) } \\ & { \left( \frac { \log \left( 1 + \cos \eta \operatorname* { m i n g } _ { n \in \mathcal { X } } \right) } { \frac { E _ { i , n } ^ { t } } { \sum _ { i = 0 } ^ { n } \log \left( 1 + \pi _ { i } ^ { t } \right) } } \cdot \overbrace { - \frac { \log \left( \frac { 1 } { n } \right) } { \sum _ { j = 0 } ^ { n } \log \left( 1 + \frac { \left( \frac { E _ { i , n } ^ { t } } { n } \right) } { \sum _ { i = 0 } ^ { n } \log \left( 1 + \pi _ { i } ^ { t } \right) } \right) } ^ { \mathbb { E } \mathbb { E } \mathbb { E } \mathbb { E } } } \right) } \\ & { \left( \frac { \log \left( 1 + \cos \eta \operatorname* { m i n g } _ { n \in \mathcal { X } } \right) } { \frac { E _ { i , n } ^ { t } } { \sum _ { i = 0 } ^ { n } \log \left( \exp \left( 1 + \pi _ { i } ^ { t } \right) \right) } ^ { \mathbb { E } \mathbb { E } \mathbb { E } } } + \frac { \int _ { 0 } ^ { t } \mathbb { D } _ { i , n } ^ { t } } { \sum _ { i = 0 } ^ { n } \exp \left( 1 + \frac { E _ { i , n } ^ { t } } { \sum _ { j = 0 } ^ { n } \log \left( 1 + \pi _ { i } ^ { t } \right) } \right) } ^ { \mathbb { E } \mathbb { E } } \right) , } \\ & { \forall i \in \mathcal { X } , j \in \{ b \} \cup \mathcal { U } , n \in \mathcal { N } , } \end{array}
$$

where the metrics of satisfaction degree and cost are incorporated using the weight parameter $w _ { i }$ . Specifically, the normalized satisfaction degree, i.e., $\mathrm { o g } ( 1 + \tau _ { i } ^ { \hat { t } } - D _ { i , j } ^ { t } ) / \log ( 1 + \tau _ { i } ^ { t } )$ reflects the satisfaction level of MD i in completing task ${ \boldsymbol { \mathcal { K } } } _ { i } ^ { t } .$ which is commonly modeled as a logarithmic function and extensively used for evaluating the benefit of task processing in mobile computing domains [38]. Moreover, $p _ { j , i } ^ { t } \bar { f } _ { j , i } ^ { t } / G _ { i } ^ { \mathrm { m } { } \bar { \cdot } }$ ax represents the normalized payment to MEC server j, where $f _ { j , i } ^ { t }$ is amount of computing resource allocated by MEC server j to MD i, $p _ { i , i } ^ { t }$ is the unit price of computing resource paid by MD i, and $\mathcal { \dot { G } } _ { i } ^ { \mathrm { { \scriptsize ~ \textmu } } }$ is the budget of MD i. Accordingly, $C _ { 1 }$ can be transformed into:

$$
C _ { 1 } \Leftrightarrow \sum _ { i \in \mathcal { T } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } U _ { i , n } ^ { t } .\tag{26}
$$

Revenue of MEC Servers: For MEC servers, $C _ { 2 }$ is transformed into the sum of revenue gained from executing tasks. Specifically, the revenue gained by MEC server j from executing task $\mathcal { K } _ { i } ^ { t }$ of MD i is calculated as the difference between the reward received from MD i and the cost of energy consumption, i.e.,

$$
U _ { j , i } ^ { t } = 1 w _ { j } ~ \underbrace { \frac { f _ { j , i } ^ { t } p _ { j , i } ^ { t } } { f _ { j } ^ { \operatorname* { m a x } } p _ { j } ^ { \operatorname* { m a x } } } } _ { \mathrm { R e w a r d f r o m M D } } - ( 1 - w _ { j } ) \underbrace { \frac { E _ { j , i } ^ { t } } { E _ { j } ^ { \operatorname* { m a x } } } } _ { \mathrm { E n e r g y c o s t } } , \forall i \in { \mathbb { Z } } , j \in \{ b \}\tag{âª U.}
$$

(27)

where the metrics of reward and cost are normalized and incorporated using the weight parameter wj. Specifically, $p _ { j , i } ^ { t } f _ { j , i } ^ { \bar { t } } / ( f _ { j } ^ { \operatorname* { m a x } } p _ { j } ^ { \operatorname* { m a x } } )$ denotes the normalized reward of MEC j ( )received by providing computational services to MD i, where $p _ { j } ^ { \mathrm { m a x } }$ is the maximum price for the computing resource of MEC server j. Accordingly, $C _ { 2 }$ is transformed into:

$$
C _ { 2 } \Leftrightarrow \sum _ { j \in b \cup \mathcal { U } } \sum _ { i \in \mathcal { T } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } U _ { j , i } ^ { t } .\tag{28}
$$

Utility of System: Based on (26) and (28), the system utility is calculated by summing the QoE of MDs and the revenue of MEC servers, which is as follows:

$$
\begin{array} { r } { U ^ { t } = \underbrace { \sum _ { i \in \mathbb { Z } } \sum _ { n \in \mathcal { N } } \zeta _ { i } ^ { t } o _ { i , n } ^ { t } U _ { i , n } ^ { t } } _ { \mathrm { T h e ~ t o t a l ~ Q o E ~ o f ~ M D s } } + \underbrace { \sum _ { j \in \{ b , \mathcal { U } \} } \sum _ { i \in \mathcal { I } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } U _ { j , i } ^ { t } } _ { \mathrm { T h e ~ t o t a l ~ r e v e n u e ~ o f ~ M E C ~ s e r v e r s } } . } \end{array}\tag{29}
$$

According to the steps above, the system cost is converted into the system utility. Therefore, the problem of minimizing the system cost can be converted into maximizing the system utility as:

$$
\mathbf { P } : \quad \operatorname* { m a x } _ { \mathbf { O } , \mathbf { F } , \mathbf { Q } } \sum _ { t = 1 } ^ { T } U ^ { t } ,\tag{30a}
$$

$$
\mathrm { s . t . } \ ( 2 3 b ) \sim ( 2 3 j )\tag{30b}
$$

However, the transformed optimization problem is still an NP-hard and non-convex MINLP due to the mixed integral decision variables and the non-linear objective function. Therefore, it is difficult to find an optimal solution to problem P, which motivates us to propose the TJCCT.

## IV. ALGORITHM

To solve problem P, we propose TJCCT, which is comprised of two-timescale optimization methods. Specifically, in the short timescale, a price-incentive trading model is constructed based on the bargaining mechanism to facilitate the negotiation between the MDs and the MEC servers for the on-demand computing resource allocation and pricing. Furthermore, to deal with the heterogeneity between the computation tasks of MDs and MEC servers, a many-to-one matching is established to stimulate the end-edge collaboration for mutual-satisfactory computation offloading. In the long timescale, based on the optimal strategies of computing resource allocation and computation offloading, UAV trajectory is optimized by using convex optimization. It should be noted that although we optimize the computing resource allocation, computation offloading, and UAV trajectory control in a decoupled manner, the decision variables related to these aspects are still considered together throughout the decoupling process. This is because optimizing one decision variable is conducted under the assumption of given values for the other two variables.

## A. Short Timescale: Computing Resource Allocation and Computation Offloading

In each time slot, the strategies of computing resource allocation and computation offloading are decided.

1) Computing Resource Allocation: In this subsection, given that the task $\mathcal { K } _ { i } ^ { t }$ generated by MD i will be processed by MEC server j at time t, the optimal computing resource allocation is presented. Specifically, the metric of the unit price for computing resources is introduced to capture the task processing costs of MEC servers that should be covered by MDs. This can be viewed as a market where MDs purchase computing resources from suitable MEC servers for task processing. However, the price of the computation resource affects the utilities of both MDs and MEC servers. Therefore, to optimize the utilities of MDs and MEC servers, an appropriate pricing strategy needs to be incorporated with the resource allocation strategy, taking into account the requirements of MDs and the computing capabilities of the MEC servers.

According to the analysis above, we construct a priceincentive trading model for MDs and MEC servers. Specifically, the negotiation is modeled as a Rubinstein bargaining model [39] where the MD i with an offloading request for its task $\mathcal { K } _ { i } ^ { t }$ acts as the buyer and the target MEC server $j$ acts as a seller. The objective of the negotiation is to determine the optimal strategy of computing resource allocation $f _ { j , i } ^ { t ^ { * } }$ with satisfied price incentive $p _ { j , i } ^ { t ^ { * } }$ during time slot Î´, which are detailed below.

(1) Optimal Computing Resource Allocation: Given any price of the computing resource $p _ { j , i } ^ { t }$ , the optimal computing resource allocation $f _ { j , i } ^ { t ^ { * } }$ can be determined as Theorem 2.

Theorem 2: The optimal computing resources that MD i expects to request from the target MEC server j to offload task ${ \kappa } _ { i } ^ { t }$ is determined as follows:

$$
f _ { j , i } ^ { t ^ { * } } = \frac { 2 w _ { i } G _ { i } ^ { \operatorname* { m a x } } } { \vartheta ( p _ { j , i } ^ { t } ) - \log ( 1 + \tau _ { i } ^ { t } ) p _ { j , i } ^ { t } ( 1 - w _ { i } ) } .\tag{31}
$$

Proof: The detailed proof is given in Appendix C of the supplemental material, available online.

(2) Satisfied Computing Resource Pricing: Given any allocation of the computing resource $f _ { j , i } ^ { t }$ for task ${ \bf \breve { \mathbf { \Lambda } } } _ { i } ^ { t }$ , the satisfied price of computing resource $p _ { j , i } ^ { t ^ { * } }$ can be determined by the following steps.

First, the upper bound and lower bound of the unit price of computing resource can be derived as Lemma 1.

Lemma 1: To achieve a successful negotiation between MD i and MEC server j regarding the resource allocation and pricing of task $\mathcal { K } _ { i } ^ { t }$ , the unit price of the computing resource should be bounded by $\underline { { p } } _ { j , i } ^ { t } \leq p _ { j , i } ^ { t } \leq \overline { { p } } _ { j , i } ^ { t }$ i, where

$$
\begin{array} { r l } & { \underline { { p } } _ { j , i } ^ { t } = \frac { \left( 1 - w _ { j } \right) E _ { j , i } ^ { t } p _ { j } ^ { \operatorname* { m a x } } f _ { j } ^ { \operatorname* { m a x } } } { w _ { j } E _ { j } ^ { \operatorname* { m a x } } f _ { j , i } ^ { t } } , } \\ & { \overline { { p } } _ { j , i } ^ { t } = \left( \frac { w _ { i } \log \left( 1 + \tau _ { i } ^ { t } - D _ { i , j } ^ { t } \right) } { \left( 1 - w _ { i } \right) \log \left( 1 + \tau _ { i } ^ { t } \right) } - \frac { P _ { i } ^ { t } l _ { i } ^ { t } } { r _ { i , j } ^ { t } \tau _ { i } ^ { t } } \right) \frac { G _ { i } ^ { \operatorname* { m a x } } } { f _ { j , i } ^ { t } } . } \end{array}\tag{32}
$$

(33)

Proof: The detailed proof is given in Appendix D of the supplemental material, available online. -

Second, we present the optimal negotiation between an MD and an MEC server by employing the Rubinstein bargaining model. According to Lemma 1, the surplus of the computing resource price can be obtained as $\pi _ { j , i } ^ { t } = \bar { p } _ { j , i } ^ { t } - \underline { { p } } _ { j , i } ^ { t }$ . Therefore, the negotiation between MD i and MEC server j on the price of the computation resources can be modeled as the bargaining over the surplus $\pi _ { j , i } ^ { t }$ . Specifically, MD i and MEC server j take turns making offers about how to divide the surplus. Apparently, both the seller and buyer are subject to impatience and prefer a quick consensus on the division to a postponed trading delay because the utilities are discounted in the future. Consequently, the discount factors [39] of MD i and MEC server j are used to evaluate the patience with the negotiation delay, which are given as:

$$
\lambda _ { i } ^ { t } = 1 - \frac { l _ { i } ^ { t } } { r _ { i , j } ^ { t } \tau _ { i } ^ { t } } ,\tag{34a}
$$

$$
\lambda _ { j } ^ { t } = 1 - \frac { \mu _ { i } ^ { t } } { f _ { j , i } ^ { t } \tau _ { i } ^ { t } } .\tag{34b}
$$

Eqs. (34a) and (34b) indicates that MD i could be impatient with the long delay of task uploading, resulting in lower $\lambda _ { i } ^ { t }$ Moreover, MEC server j could be impatient with the long delay of task execution, resulting in the lower value of $\lambda _ { j } ^ { t }$ . In addition, trading parties could be more patient with the longer tolerable delay, leading to higher $\lambda _ { i } ^ { t }$ and $\bar { \lambda } _ { j } ^ { t }$

Third, to derive the satisfied partition of the surplus $\pi _ { j , i } ^ { t } .$ , we introduce the concepts of Nash equilibrium (NE) and subgame perfect Nash equilibrium (SPE) [39] as follows.

Definition 1: NE. Any partition Î¾ can be an NE outcome of the negotiation if it satisfies the following conditions: MD i (or MEC server $j )$ always proposes $\xi = ( \xi _ { i } , \xi _ { j } )$ and only accepts the offers $\xi ^ { \prime }$ where $\xi _ { i } ^ { j } > \xi _ { i }$ (or $\xi _ { j } ^ { \prime } > \xi _ { j } )$

Definition 2: SPE. The partition $\xi ^ { * } = ( \xi _ { i } ^ { * } , \xi _ { i } ^ { * } )$ is an SPE if $\xi ^ { * }$ = ( )induces an NE each time a new offer is made and rejected.

According to Definitions 1 and 2, the satisfied partition of the surplus $\pi _ { j , i } ^ { t }$ can be obtained by Lemma 2.

Lemma 2: The bargaining model has a unique SPE. In the period $T ^ { b }$ when MD i makes a proposal, the satisfied partition of the surplus $\pi _ { j , i } ^ { t }$ for the computing resource price can be given as:

$$
\xi _ { i , i } ^ { t ^ { * } } = \lambda _ { i } ^ { t } - \frac { ( 1 - \lambda _ { i } ^ { t } ) \left( 1 - ( \lambda _ { i } ^ { t } \lambda _ { j } ^ { t } ) ^ { \lceil \frac { T ^ { b } } { 2 } \rceil } \right) } { 1 - \lambda _ { i } ^ { t } \lambda _ { j } ^ { t } } .\tag{35}
$$

In the period $T ^ { b }$ when MEC server $j$ makes a proposal, the satisfied partition can be given as:

$$
\xi _ { i , j } ^ { t ^ { * } } = \frac { ( 1 - \lambda _ { j } ^ { t } ) \left( 1 - ( \lambda _ { i } ^ { t } \lambda _ { j } ^ { t } ) ^ { \lceil \frac { T ^ { b } } { 2 } \rceil } \right) } { 1 - \lambda _ { i } ^ { t } \lambda _ { j } ^ { t } } .\tag{36}
$$

Proof: The detailed proof is given in Appendix E of the supplemental material, available online.

Fourth, according to Lemmas 1 and 2, the optimal price of the computing resource can be derived by Theorem 3.

Theorem 3: The satisfied outcome for the price of the computation resource $p _ { j , i } ^ { t ^ { * } }$ can be obtained as:

$$
p _ { j , i } ^ { t ^ { * } } = { \bar { p } } _ { j , i } ^ { t } - \pi _ { j , i } ^ { t } \xi _ { i , i } ^ { t ^ { * } } ,\tag{37a}
$$

$$
p _ { j , i } ^ { t ^ { * } } = { \bar { p } } _ { j , i } ^ { t } - \pi _ { j , i } ^ { t } \xi _ { i , j } ^ { t ^ { * } } ,\tag{37b}
$$

where (37a) indicates the optimal price of the computing resource obtained in the period when MD i makes an offer, and (37b) indicates the optimal price of the computing resource obtained in the period when MEC server j makes an offer.

Proof: The detailed proof is given in Appendix F of the supplemental material, available online.

(3) Optimal Computing Resource Allocation with Price Incentive: The optimal strategies of computing resource allocation with price incentive can be concluded from Theorems 2 and 3, as given in Corollary 1.

Corollary 1: A trading consensus can be reached on the amount and unit price of the allocated computing resources:

$$
f _ { j , i } ^ { t ^ { * } } = \frac { 2 w _ { i } G _ { i } ^ { \operatorname* { m a x } } } { \vartheta ( p _ { j , i } ^ { t ^ { * } } ) - \log \left( 1 + \tau _ { i } ^ { t } \right) p _ { j , i } ^ { t ^ { * } } \left( 1 - w _ { i } \right) } ,\tag{38}
$$

$$
p _ { j , i } ^ { t ^ { * } } = \left\{ \begin{array} { l l } { \overline { { p } } _ { j , i } ^ { t } - \pi _ { j , i } ^ { t } \xi _ { i , i } ^ { t ^ { * } } , } \\ { \overline { { p } } _ { j , i } ^ { t } - \pi _ { j , i } ^ { t } \xi _ { i , j } ^ { t ^ { * } } . } \end{array} \right.\tag{39a}
$$

(39b)

The trading contract between MD i and MEC server $j$ is presented in Definition 3. According to Corollary 1 and Definition 3, an alternative algorithm that iteratively optimizes the strategies of computing resource allocation and pricing is described in Algorithm 1. Specifically, the optimal strategy of computing resource allocation is initially set as the available resources of MEC server $j$ (line 2). Furthermore, in each iteration, MD i and MEC server j negotiate the satisfied price of the computing resource based on the trading contract (line 6). Then, they update the optimal strategy of computing resource allocation (line 7). The steps above are iterated until a consensus is reached.

Definition 3: Trading contract. The trading amount and price are determined based on the following terms.

- $\mathrm { I f } U _ { i , i } ^ { t } > 0 , U _ { i , i } ^ { t } > 0$ , a consensus is reached on the trading 0 0amount and price based on (38) and (39).

- $\mathrm { I f } U _ { i , i } ^ { t } > 0 , U _ { i , i } ^ { t } < 0$ , MD i makes an offer of the unit price 0 0of computing resources based on (39a).

- If $U _ { i , j } ^ { t } < 0 , \bar { U } _ { j , i } ^ { t } > 0$ , MEC server j makes an offer of the 0 0unit price of computing resources based on (39b).

- If $U _ { i , j } ^ { \hat { t } } < 0 , U _ { j , i } ^ { t } \dot { < } 0$ , either MD i or MEC server j can 0make an offer.

2) Computation Offloading: Matching mechanism offers an efficient tool to construct the mutual-beneficial relationship between two sets of entities with heterogeneous preferences. This motivates us to construct the matching among different MDs and MEC servers to alleviate the demand-supply discrepancy. By doing so, the MDs and MEC servers can achieve mutual-beneficial computation offloading results of satisfied QoE and high computing resource utilization. Denote the set of computation tasks that have not begun execution in time slot t as ${ \mathcal { K } _ { \mathrm { r e q } } ^ { t } } = \{ { \mathcal { K } _ { i } ^ { \sf t } } | i \in \mathbb { Z } , { \sf t } \in \mathcal { T } \}$ , where t is the generation = time of the computation task. Then the offloading strategy for these computation tasks in each time slot is decided using a many-to-one matching mechanism, which is defined by Definition 4.

Algorithm 1: Computing Resource Allocation.   
Input: Task $\mathcal { K } _ { i } ^ { t }$ of MDiand MEC server $j$   
Output: The optimal resource allocation with   
satisfied price $( f _ { j , i } ^ { t ^ { * } } , p _ { j , i } ^ { t ^ { * } } )$ in time slot t   
1 Initialization: $U _ { i , j } ^ { \hat { t } } = 0 ; U _ { j , i } ^ { t } = 0 ; \iota = 0 ; \iota ^ { \operatorname* { m a x } } = 1 0 0 ;$   
2 Set the optimal resource allocation as $f _ { j , i } ^ { t ^ { * } } = f _ { j } ^ { \mathrm { a v l } } ;$   
3 while $\iota \doteq \iota ^ { \mathrm { m a x } }$ do   
4 Update $p _ { j , i } ^ { t ^ { * } }$ based on Eq. (39);   
5 Calculate $\dot { U } _ { i , j } ^ { t } , U _ { j , i } ^ { t }$ based on Eqs.(25) and $( 2 7 ) ;$   
6 Perform the trading contract based on Definition   
3;   
7 Update $f _ { j , i } ^ { t ^ { * } }$ based on Eq. (38);   
8 $\iota = \iota + 1 ;$   
9return $( f _ { j , i } ^ { t ^ { * } } , p _ { j , i } ^ { t ^ { * } } ) ;$

Definition 4: The current matching is defined as a triplet of $( \mathcal { M } ^ { t } , \mathcal { L } ^ { t } , \Pi ^ { t } ) ;$

. $\mathcal { M } ^ { t } = \widetilde { ( } \mathcal { K } _ { \mathrm { r e q } } ^ { t } , \{ b \} \cup \mathcal { U } )$ consists of the tasks of MDs and the = (MEC servers.

- $\mathcal { L } ^ { t } = ( \mathcal { L } _ { \mathcal { K } _ { i } ^ { \mathtt { t } } } ^ { t } , \mathcal { L } _ { j } ^ { t } )$ consists of the preference lists of the tasks and MEC servers. Each task ${ \sf K } _ { i } ^ { { \sf t } } \in { \sf K } _ { \mathrm { r e q } } ^ { t }$ has a descending ordered preferences over the MEC servers, i.e., $\mathcal { L } _ { \mathcal { K } _ { i } ^ { \mathrm { t } } } ^ { t } =$ $\{ j | j \in \{ b \} \cup \mathcal { U } , j \succ _ { \mathcal { K } _ { i } ^ { \ t } } j ^ { \prime } \}$ , where $\succ _ { \mathcal { K } _ { i } ^ { \mathrm { t } } }$ is the preference of task $\kappa _ { i }$ towards the servers. Moreover, each MEC server j has a descending ordered preference list over the tasks, $\mathrm { i . e . , } \mathcal { L } _ { j } ^ { t } = \{ \mathcal { K } _ { i } ^ { \mathrm { t } } \in { \mathcal { K } _ { \mathrm { r e q } } ^ { t } } , \mathcal { K } _ { i } ^ { \mathrm { t } } \succ _ { j } \mathcal { K } _ { i } ^ { \mathrm { t ^ { \prime } } } \}$

$\Pi ^ { t } \subseteq { \mathcal { K } } _ { \mathrm { r e q } } ^ { t } \times \{ b \}$ âª U denotes the matching between the tasks and MEC servers. Each task ${ \mathcal { K } } _ { i } ^ { \sf t } \in { \mathcal { K } } _ { \mathrm { r e q } } ^ { t }$ can be matched with at most one MEC server, i.e., $\Pi _ { K _ { i } ^ { \ t } } ^ { t } \in \{ b \} \cup \mathcal { U }$ while each MEC server $j$ can be matched with multiple tasks, i.e., $\Pi _ { j } ^ { t } \subseteq { \mathcal { K } } _ { \mathrm { r e q } } ^ { t }$

Î  The main steps of the matching process are presented in Algorithm 2, and the details are further described as follows.

Preference List Construction: For each task ${ \mathcal { K } } _ { i } ^ { \sf t } \in { \mathcal { K } } _ { \mathrm { r e q } } ^ { t }$ and MEC server j, the preference lists are constructed based on the following steps: i) predict the optimal computing resource allocation and pricing by calling Algorithm 1 (line 4), ii) calculate the preference value for each task on MEC servers, i.e., $V _ { { \boldsymbol { \kappa } } _ { i } ^ { \mathrm { t } } , j } ^ { t }$ and the preference value for each MEC server on tasks, i.e., $V _ { j , \kappa _ { i } ^ { \mathrm { t } } }$ (line 5), iii) construct the preference list for each task and MEC server by ranking the preference values in descending order (lines 6 and 7).

Matching Construction: The matching process is implemented according to the following steps: i) for each computation task ${ \sf K } _ { i } ^ { { \sf t } } \in { \sf K } _ { \mathrm { r e j } } ^ { t } .$ , select the most preferred MEC server j and add it to the matching list temporarily (line 10), ii) if the computation task prefers MEC server $j ^ { \prime } ,$ add the computation task to the matching list of $j ^ { \prime }$ temporarily (lines 11 and 12), iii) for each MEC server that receives new requests, update the matching list by remaining the $\mathrm { t o p } { - } N _ { j }$ most preferred computation tasks and removing the less preferred computation tasks (lines 13 to 14) to guarantee that the current number of tasks and the allocated computing resources should not exceed the number of idle CPU cores $N _ { j } ^ { t , \mathrm { i d l } }$ and the available computing resources $f _ { j } ^ { t , \mathrm { a v l } }$ of the MEC server, respectively, iv) add the deleted computation tasks into the rejected set, v) update the preference list and matching list for the deleted computation tasks (lines 16 and 17). The steps above are repeated until all computation tasks have been matched with an MEC server, or the unmatched computation tasks have been rejected by all MEC servers.

Algorithm 2: Computation Offloading.   
Input: Tasks $K _ { \mathrm { r e q } } ^ { t } = \{ \mathcal { K } _ { i } ^ { \sf t } | i \in \mathcal { I } , t \in \mathcal { T } \}$ ,and MEC   
servers $\{ b \} \cup \mathcal { U }$   
Output: The optimal matching list $\Pi ^ { t ^ { * } }$ ,offloading   
$\mathbf { O ^ { \mathit { t } ^ { * } } }$ , and computing resource allocation $\Breve { \mathbf { F } } ^ { t ^ { * } }$   
1 Initialization: $\mathcal { K } _ { \mathrm { r e j } } ^ { t } = \dot { \mathcal { K } } _ { \mathrm { r e q } } ^ { t } , \Pi ^ { t ^ { * } } = \varnothing ;$   
2for $\mathcal { K } _ { i } ^ { \sf t } \in \mathcal { K } _ { r e q } ^ { t }$ do   
3 for $j \in \{ b , \mathcal { U } \}$ do   
4 Call Algorithm 1 to obtain $( { f } _ { j , i } ^ { \mathbf { t } ^ { * } } , { p } _ { j , i } ^ { \mathbf { t } ^ { * } } ) ;$   
5 Calculate $V _ { \mathcal { K } _ { i } ^ { \sf t } , j } ^ { t } = U _ { i , j } ^ { \sf t } , V _ { j , \mathcal { K } _ { i } ^ { \sf t } } = U _ { j , i } ^ { \sf t ^ { \prime } } ;$   
6 $V _ { { \mathcal { K } _ { i } ^ { \mathbf { t } } } , j } ^ { t } > V _ { K _ { i } ^ { \mathbf { t } } , j ^ { \prime } } ^ { t } \Leftrightarrow j \succ _ { K _ { i } ^ { \mathbf { t } } } j ^ { \prime } , { \mathcal { L } _ { K _ { i } ^ { \mathbf { t } } } } = \{ j , j ^ { \prime } \} ;$   
7 $V _ { j , \kappa } > V _ { j , \kappa ^ { \prime } } \Leftrightarrow K \succ _ { j } \kappa ^ { \prime } , \mathcal { L } _ { j } ^ { t } = \{ K , K ^ { \prime } \} ;$   
8 while There exists ${ \mathcal { K } } _ { i } ^ { \sf t } \in { \mathcal { K } } _ { \mathrm { r e j } } ^ { t } \colon { \mathcal { L } } _ { { \mathcal { K } } _ { i } ^ { \sf t } } ^ { t } \stackrel { ^ { \prime } } { \neq } \emptyset { \mathcal { K } } { \mathcal { K } } _ { i } ^ { { \sf t } }$   
do   
9 for ${ \cal K } _ { i } ^ { \mathbf { t } } \in { \cal K } _ { r e j } ^ { t }$ do   
10 $\Pi _ { K _ { i } ^ { \mathbf { t } } } ^ { \dot { t } } = \Pi _ { K _ { i } ^ { \mathbf { t } } } ^ { t } \cup j ^ { \prime } , \ j ^ { \prime } = \mathcal { L } _ { K _ { i } ^ { \mathbf { t } } } ^ { t } [ 1 ] ;$   
11 if $\dot { V } _ { \mathcal { K } _ { i } ^ { \mathrm { t } } , j ^ { \prime } } ^ { t } > 0$ then   
12 $\Pi _ { j ^ { \prime } } ^ { t } = \Pi _ { j ^ { \prime } } ^ { t } \cup \mathcal { K } _ { i } ^ { \mathbf { t } }$   
13 for $j \in \{ b , \mathcal { U } \}$ that receives new requests do   
14 $\begin{array} { r } { | \Pi _ { j } ^ { t } | \overset { \cdot } { \le } N _ { j } \le N _ { j } ^ { \mathrm { i d l } } , \sum _ { \mathcal { K } _ { i } ^ { \sf t } \in \Phi ( j ) } f _ { j , i } ^ { \sf t ^ { * } } \le f _ { j } ^ { t , \mathrm { a v l } } ; } \end{array}$   
15 $\Pi _ { j } ^ { \dot { t } } = \Pi _ { j } ^ { t } \setminus \mathcal { D } _ { j } ^ { t } , \dot { \mathcal { K } } _ { \mathrm { r e j } } ^ { t } = \dot { \mathcal { K } } _ { \mathrm { r e j } } ^ { t } \cup \mathcal { D } _ { j } ^ { \dot { t } }$   
16 for ${ \mathcal { K } } _ { i } ^ { \mathfrak { t } } \in { \mathcal { D } } _ { j } ^ { t }$ do   
17 $| | \mathcal { L } _ { K _ { i } ^ { \sf t } } ^ { \bar { t } } = \mathcal { L } _ { K _ { i } ^ { \sf t } } ^ { t } \ \backslash \ \{ j \} , \Pi _ { K _ { i } ^ { \sf t } } ^ { t } = \Pi _ { K _ { i } ^ { \sf t } } ^ { t } \ \backslash \ \{ j \} ;$   
18 return $\begin{array} { r } { \dot { \Pi } ^ { t ^ { * } } = \dot { \Pi } ^ { t } , \mathbf { O } ^ { t ^ { * } } = \{ o _ { i , j } ^ { t } | j ^ { \stackrel { * } { = } } \Pi _ { K _ { i } ^ { t } } ^ { t } , \dot { \mathcal { K } } _ { i } ^ { t } \in \mathcal { K } _ { r e q } ^ { t } \} , } \end{array}$   
$\mathbf { F } ^ { t ^ { * } } = \{ ( f _ { j , i } ^ { \mathbf { t } ^ { * } } , p _ { j , i } ^ { \mathbf { t } ^ { * } } ) | j = \Pi _ { \mathcal { K } _ { i } ^ { \mathbf { t } } } ^ { t } , \mathcal { K } _ { i } ^ { \mathbf { t } } \in \mathcal { K } _ { r e q } ^ { t ^ { * } } \} ;$

The weak-Pareto optimality of computation offloading is proved in Theorem 4.

Theorem 4: The result of computation offloading $\mathbf { O } ^ { t ^ { * } }$ is weak Pareto optimal.

Proof: The detailed proof is given in Appendix G of the supplemental material, available online.

Remark 3: In the short timescale, Algorithms 1 and 2 present the decisions of computing resource allocation and computation offloading by managing the interaction among MDs and MEC servers. Specifically, for Algorithm 1, it describes the interaction between any MD i and its preferred edge server j to determine the computing resource allocation of the edge server for the MD. It is noteworthy that although Algorithm 1 presents the negotiation between an MD and an edge server, it does not imply the negotiation is specific to a certain MD and the edge server. Instead, it assumes the negotiation party of any MD and its preferred MEC server.

For Algorithm 2, it presents the interaction among different MDs and edge servers to determine the computation offloading decisions. Note that although the matching is constructed between two sets of entities, i.e., MDs and edge servers, the collaboration occurs among different MDs and edge servers. This is because the computation tasks of multiple MDs could be offloaded to an MEC server in each time slot, while different computation tasks generated by an MD in different time slots could be executed by different MEC servers.

## B. Long Timescale: UAV Trajectory Control

In each time epoch, the UAV trajectory is optimized by applying the convex approximation method. Specifically, the movement of UAVs in the next time epoch is optimized based on the optimized strategies of computing resource allocation $\mathbf { F } ^ { t ^ { * } }$ and computation offloading $\mathbf { O } ^ { t ^ { * } }$ . Therefore, fixing $\mathbf { F } ^ { t ^ { * } }$ and $\mathbf { O } ^ { t ^ { * } }$ while eliminating the unrelated terms in the objective function and constraints, the problem of UAV trajectory optimization can be given as:

$$
\mathbf { P _ { t } } : \operatorname* { m a x } _ { \mathbf { Q } ^ { t ^ { \prime } } } U ^ { t } = \operatorname* { m a x } _ { \mathbf { Q } ^ { t ^ { \prime } } } \sum _ { i \in \mathcal { T } } \sum _ { j \in \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } \left( U _ { i , j } ^ { t } + U _ { j , i } ^ { t } \right)\tag{40a}
$$

$$
( 4 a ) \sim ( 4 f ) ,
$$

where $\mathbf { Q } ^ { t ^ { \prime } }$ denotes the positions of UAVs in the next time epoch $t ^ { \prime } = ( \bar { \left| t \right| } / \Delta \bar { \left| + 1 \right| } ) \Delta$

= ( Î + 1)ÎLemma 3: Problem $\mathbf { P _ { t } }$ can be approximately converted into:

$$
\begin{array} { r l r } { \overline { { \mathbf { P } } } _ { \mathrm { t } } : \displaystyle \operatorname* { m a x } _ { \mathbf { Q } ^ { t ^ { \prime } } } } & { \displaystyle \sum _ { i \in \mathcal { I } } \displaystyle \sum _ { j \in \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } \left( \vartheta _ { 0 } \log \left( 1 + \left( \tau _ { i } ^ { t } - \frac { l _ { i } ^ { t } } { \overline { { r } } _ { i , j } ^ { t ^ { \prime } } } - \vartheta _ { 1 } \right) \right) \right. } & \\ & { \quad \quad \quad \quad \quad \left. - \vartheta _ { 2 } \frac { l _ { i } ^ { t } } { \overline { { r } } _ { i , j } ^ { t } } - \vartheta _ { 3 } E _ { j } ^ { p } \delta \right) } & { \mathrm { ( 4 1 a ) } } \\ & { \quad \quad \quad \quad \quad \left( 4 a \right) \sim \left( 4 e \right) . } \end{array}
$$

where $\vartheta _ { 0 } = w _ { i } / ( 1 + \tau _ { i } ^ { t } ) , \qquad \vartheta _ { 1 } = \mu _ { i } ^ { t } / f _ { i , i } ^ { t } , \qquad \vartheta _ { 2 } = ( 1 -$ $w _ { i } ) P _ { i } ^ { t } / E _ { i } ^ { \operatorname* { m a x } } , \vartheta _ { 3 } = ( 1 - w _ { j } ) / E _ { j } ^ { \operatorname* { m a x } }$ x , and $\begin{array} { r } { \overline { { r } } _ { i , j } ^ { t ^ { \prime } } = B _ { i , j } ^ { t } \log _ { 2 } ( 1 + } \end{array}$ $P _ { i } ^ { t } { \bar { g } } _ { i , j } ^ { t } / ( N _ { 0 } ( \| \mathbf { q } _ { i } ^ { t ^ { \prime } } - \mathbf { q } _ { i } ^ { t } \| ^ { 2 } + H ^ { 2 } ) ^ { \bar { \beta } _ { A } / 2 } ) )$

Â¯ ( ( + ) ))Proof: The detailed proof is given in Appendix H of the supplemental material, available online.

However, problem $\overline { { \mathbf { P } } } _ { \mathbf { t } }$ is a non-convex optimization problem due to the non-concavity of the objective function and the nonconvexity of Constraint (4f). Therefore, it will be transformed into a convex problem by the following steps.

First, since the objective function of $\overline { { \mathbf { P } } } _ { \mathbf { t } }$ is non-convex with respect to $\mathit { \overline { { r } } _ { i , j } ^ { t ^ { \prime } } }$ , the auxiliary variables $\tilde { r } _ { i , j } ^ { t ^ { \prime } }$ is first introduced such that $\tilde { r } _ { i , j } ^ { t ^ { \prime } } \leq \bar { r } _ { i , j } ^ { t ^ { \prime } }$ , where the RHS is lower bounded by a concave Ëfunction as given in Lemma 4.

Lemma 4: Given the local point $\hat { \mathbf { q } } _ { j } ^ { s }$ at the s-th iteration, $\overline { { r } } _ { i , j } ^ { t }$ is lower bounded by:

$$
\begin{array} { r } { \overline { { r } } _ { i , j } ^ { t ^ { \prime } } \geq B _ { i , j } \log _ { 2 } \left( 1 + \frac { P _ { i } ^ { t } \bar { g } _ { i , j } ^ { t } } { N _ { 0 } ( H ^ { 2 } + \| \hat { \mathbf { q } } _ { j } ^ { s } - \mathbf { q } _ { i } ^ { t } \| ^ { 2 } ) ^ { \beta / 2 } } \right) } \\ { - \frac { B _ { i , j } \beta \left( \| \mathbf { q } _ { j } ^ { t ^ { \prime } } - \mathbf { q } _ { i } ^ { t } \| ^ { 2 } - \| \hat { \mathbf { q } } _ { j } ^ { s } - \mathbf { q } _ { i } ^ { t } \| ^ { 2 } \right) } { 2 \ln 2 ( H ^ { 2 } + \| \hat { \mathbf { q } } _ { j } ^ { s } - \mathbf { q } _ { i } ^ { t } \| ^ { 2 } ) } = \tilde { \tilde { r } } _ { i , j } ^ { s } . } \end{array}\tag{42}
$$

Proof: The detailed proof is given in Appendix I of the supplemental material, available online.

Second, for the non-convexity of the UAV propulsion energy $E _ { j } ^ { p }$ , we introduce an auxiliary variable Ï such that

$$
\phi ^ { 2 } \geq \sqrt { \eta _ { 3 } + \frac { ( v _ { j } ^ { t } ) ^ { 4 } } { 4 } } - \frac { ( v _ { j } ^ { t } ) ^ { 2 } } { 2 } \Longrightarrow \frac { \eta _ { 3 } } { ( \phi ) ^ { 2 } } \leq \phi ^ { 2 } + ( v _ { j } ^ { t } ) ^ { 2 } ,\tag{43}
$$

where $v _ { j } ^ { t } = \lVert \mathbf { q } _ { j } ^ { t ^ { \prime } } - \mathbf { q } _ { j } ^ { t } \rVert / ( \delta \Delta )$ . For the convex RHS of (43), a = ( Î)global concave lower bound can be obtained at the local point $\bar { \phi } ^ { s }$ by using the first-order Taylor expansion, i.e.,

$$
\begin{array} { l } { { \displaystyle { \phi ^ { 2 } + ( v _ { j } ^ { t } ) ^ { 2 } \geq ( \phi ^ { s } ) ^ { 2 } + 2 \phi ^ { s } ( \phi - \phi ^ { s } ) } } } \\ { { \displaystyle { + \frac { | | \hat { \mathbf { q } } _ { j } ^ { s } - \mathbf { q } _ { i } ^ { t } | | } { \Delta ^ { 2 } } + \frac { 2 } { \Delta ^ { 2 } } ( \hat { \mathbf { q } } _ { j } ^ { s } - \mathbf { q } _ { i } ^ { t } ) ^ { T } \left( \hat { \mathbf { q } } _ { u } ^ { t ^ { \prime } } - \mathbf { q } _ { i } ^ { t } \right) = \tilde { \phi } ^ { s } } } } \end{array}\tag{44}
$$

Third, to deal with the non-convex Constraint (4f), $| | \mathbf { q } _ { j } ^ { t } - \mathbf { \bar { \Sigma } }$ $\mathbf { q } _ { j ^ { \prime } } ^ { t } | | ^ { 2 }$ can be lower bounded by applying the first-order Taylor expansion at any given point $\hat { \mathbf { q } } _ { j } ^ { t }$ and qtj , i.e.,

$$
\begin{array} { r } { \vert \vert \mathbf { q } _ { j } ^ { t } - \mathbf { q } _ { j ^ { \prime } } ^ { t } \vert \vert ^ { 2 } \geq - \vert \vert \hat { \mathbf { q } } _ { j } ^ { t } - \hat { \mathbf { q } } _ { j ^ { \prime } } ^ { t } \vert \vert ^ { 2 } + 2 \left( \hat { \mathbf { q } } _ { j } ^ { t } - \hat { \mathbf { q } } _ { j ^ { \prime } } ^ { t } \right) ^ { T } ( \mathbf { q } _ { j } ^ { t } - \mathbf { q } _ { j ^ { \prime } } ^ { t } ) = \widetilde { d } _ { j , j ^ { \prime } } ^ { t } . } \end{array}\tag{45}
$$

Based on Lemmas 3 and 4, by introducing the auxiliary variables $\overline { { r } } _ { i , j } ^ { t } , \tilde { \tilde { r } } _ { i , j } ^ { s } , \phi , \tilde { \phi } ^ { s }$ , and $\widetilde { d } _ { j , j ^ { \prime } } ^ { t } , \overline { { \mathbf { P } } } _ { \mathbf { t } }$ can be transformed as:

$$
\begin{array} { r l } & { \overline { { \mathbf { P } } } _ { \mathrm { t 1 } } : \displaystyle \operatorname* { m a x } _ { \mathbf { Q } ^ { t r } } \sum _ { i \in \mathcal { T } } \sum _ { j \in \mathcal { U } } \zeta _ { i } ^ { t } o _ { i , j } ^ { t } } \\ & { \qquad \quad \times \left( \vartheta _ { 0 } \log \left( 1 + \tau _ { i } ^ { t } - \frac { l _ { i } ^ { t } } { \bar { T } _ { i , j } ^ { t ^ { \prime } } } - \vartheta _ { 1 } \right) - \displaystyle \frac { \vartheta _ { 2 } l _ { i } ^ { t } } { \bar { T } _ { i , j } ^ { t } } \right. } \\ & { \qquad \quad \left. - \vartheta _ { 3 } \left( \eta _ { 1 } \left( 1 + \frac { 3 ( v _ { j } ^ { t } ) ^ { 2 } } { v _ { j } ^ { \mathrm { i n } } ^ { 2 } } \right) + \eta _ { 2 } \phi + \eta _ { 4 } ( v _ { j } ^ { t } ) ^ { 3 } \right) \delta \right) } \end{array}\tag{46a}
$$

$$
\begin{array} { r } { \mathrm { s . t . } \ \overline { r } _ { i , j } ^ { t } \leq \tilde { \tilde { r } } _ { i , j } ^ { s } , \forall i \in \mathbb { Z } , j \in \mathcal { U } , t \in \mathcal { T } , } \end{array}
$$

$$
\frac { \eta _ { 3 } } { \phi ^ { 2 } } \leq \tilde { \phi } ^ { s } ~ \forall i \in \mathcal { T } , ~ j \in \mathcal { U } , ~ t \in \mathcal { T } ,\tag{46b}
$$

(46c)

$$
\begin{array} { r } { \widetilde { d } _ { j , j ^ { \prime } } ^ { t } \geq d _ { \mathrm { U } } ^ { \mathrm { s a f e } } , \forall j , j ^ { \prime } \in \mathcal { U } , j \not = j ^ { \prime } , t \in \mathcal { T } , } \end{array}\tag{46d}
$$

$$
( 4 a ) \sim ( 4 d ) ,
$$

where problem $\overline { { \mathbf { P } } } _ { \mathbf { t 1 } }$ is convex since the objective function is concave and the feasible region is convex, which can be easily solved by optimization tools such as CVX.

The solution of UAV trajectory control is summarized in Algorithm 3. First, in the s-th iteration, the lower bounds $\tilde { \tilde { r } } _ { i , j } ^ { s }$ and $\tilde { \phi } ^ { s }$ are calculated (line 3). Then, the optimal trajectory $\mathbf { Q } ^ { s ^ { * } }$ of Problem $\overline { { \mathbf { P } } } _ { \mathbf { t } 1 }$ is obtained as the local point for the next iteration $\mathbf { Q } ^ { s + 1 }$ (lines 4 and 5). The iteration ends when the difference in the objective value between successive iterations falls below a given threshold .

Although the non-convex problem $\mathbf { P _ { t } }$ is transformed to a convex problem, the transformation does not affect the optimality of problem $\mathbf { P _ { t } } .$ , as presented in Theorem 5.

Theorem 5: Problem $\overline { { \mathbf { P } } } _ { \mathbf { t } }$ does not change the optimality of problem $\mathbf { P _ { t } }$

Proof: The detailed proof is given in Appendix J of the supplemental material, available online.

## C. Main Steps of TJCCT

The main steps of TJCCT are given in Algorithm 4. Specifically, in each time slot, the MDs that have unprocessed computation tasks decide to process the tasks locally or offload them to the MEC servers (line 3). Then, obtain the optimal strategies of computing resource allocation and computation offloading in the current time slot by calling Algorithm 2 (line 4). Furthermore, perform the computing resource allocation and computation offloading based on the obtained strategies in each time slot (line 5). Moreover, update the task processing state and available computing resources of MEC servers in each time slot (line 6). In addition, calculate the optimal trajectories of UAVs and update the mobility states of MDs and UAVs in each time epoch (lines 9 and 10). Finally, calculate and update the system utility (lines 11 and 12).

Algorithm 3: UAV Trajectory Control.   
Input: UAV location $\mathbf { Q } ^ { t } .$ ,optimal offloading strategy   
$\mathbf { F } ^ { t ^ { * } }$ and optimal resorce allocation strategy   
$\mathbf { O } ^ { t ^ { * } }$ in time slot t   
Output: UAV trajecoty in the next time epoch $\mathbf { Q } ^ { t ^ { \prime * } }$   
1 Initialization: $\epsilon , s = \mathbf { \bar { 0 } } , { \hat { \mathbf { q } } } _ { j } ^ { s } = \mathbf { q } _ { j } ^ { t } , U ^ { s } = 0 ;$   
2 repeat   
3 Calculate $\tilde { \tilde { r } } _ { i , j } ^ { s }$ and $\tilde { \phi } ^ { s }$ based on Eqs. (42) and (46);   
4 Solve Problem $\overline { { \mathbf { P } } } _ { \mathbf { t 1 } }$ to obtain the optimal   
trajectory $\mathbf { Q } ^ { s ^ { * } }$ and objective value $U ^ { s ^ { * } }$   
5 Update $\dot { { \bf Q } } ^ { s + 1 } = { \bf Q } ^ { s ^ { * } } ;$   
6 Update $\mathbf { s } = \mathbf { s } + 1 ;$   
7until $\begin{array} { r } { \left| U ^ { s } - U ^ { s - 1 } \right| \le \epsilon ; } \end{array}$   
8 return $\mathbf { Q } ^ { t ^ { \prime * } } ;$

```perl
Algorithm 4: TJCCT.
Input: $\mathcal { T } , \{ b , \mathcal { U } \} , \mathcal { T }$
Output: U
1 Initialization: $t = 0 , U = 0 ;$
2 while $t \leq T$ do
3 Each MD processes the task locally if $U _ { i , 0 } ^ { t } > 0$
4 Call Algorithm 2 to obtain $\Pi ^ { t ^ { * } } , \mathbf { o } ^ { \check { t } ^ { * } }$ ,and $\mathbf { F } ^ { t ^ { * } } ;$
5 for $\Pi _ { j } ^ { t } \in \Pi ^ { t ^ { * } }$ do
6 Perform computing resource allocation and
charging;
7 Update the task processing state and
available computing resources of MEC
servers;
8 ift% $\Delta = = 0$ then
9 Call Algorithm 3 to obtain $\mathbf { Q } ^ { t ^ { \prime * } } ;$
10 Update the mobility of MDs and $\mathrm { U A V s } ;$
11 Calculate the current system utility $U ^ { t } ;$
12 Update the total system utility $U \overset { \cdot } { = } U + U ^ { t } ;$
13 $t \stackrel { \cdot } { = } t + \delta ;$
14 return $U ;$
```

## V. PERFORMANCE ANALYSIS

In this section, the stability, optimality, and computational complexity of the proposed TJCCT are analyzed.

## A. Stability

The stability of TJCCT depends on the decision of computation offloading, which, in turn, relies on the result of matching $\Pi ^ { t ^ { * } }$ . The stability of $\Pi ^ { t ^ { * } }$ is proven by Theorem 6.

Î Theorem 6: The result of matching $\Pi ^ { t ^ { * } }$ is stable.

Proof: The detailed proof is given in Appendix K of the supplemental material, available online.

According to Theorem 6, it can be concluded that the proposed TJCCT is stable.

## B. Computation Complexity

The computational complexity of TJCCT is given as Theorem 7. Note that the complexity reduction for solving problem P comes with the performance degradation due to the narrower solution space resulting from problem dividing. For example, the results in [40] demonstrates that network throughput and execution time both increase with more sophisticated algorithm designs. However, the proposed TJCCT still achieves a feasible solution that satisfies the QoE of users while meeting the constraints of the system, and the reasons are as follows. First, although dividing the original problem into subproblems narrows the solution space, the optimization objective and constraints remain unchanged for each subproblem, ensuring the feasibility of the solution to satisfy the requirements and constraints of the original problem. Similar approaches have been adopted in the studies [11] to address the original problem. Moreover, the optimality of the solution for each subproblem is proved, indicating that the outcome of each subproblem is optimal. Finally, the simulation results presented in the next section will also demonstrate the superiority of our algorithm in terms of the task processing performance and system performance under the energy constraints.

Theorem 7: The proposed algorithm has a polynomial worst-case complexity in each time slot, $\mathrm { i . e . , ~ } \mathcal { O } ( \iota ^ { \mathrm { m a x } } ( | \mathcal { U } | +$ $1 ) ( 2 | \mathcal { K } _ { \mathrm { r e q } } ^ { t } | \ +$ min $\{ | \dot { \mathcal { U } } | + 1 , | \mathcal { K } _ { \mathrm { r e q } } ^ { t } | \} ) ~ + ~ ( | \mathbb { Z } | | \mathcal { U } | ) ^ { 3 . 5 } \log _ { 2 } ( \ddot { 1 } / \dot { \epsilon } ) )$ +, where $| \mathcal { \bar { K } } _ { \mathrm { r e q } } ^ { t } |$ and |U| are the numbers of undecided tasks and MEC servers in time slot t, respectively.

Proof: The detailed proof is given in Appendix L of the supplemental material, available online.

## VI. SIMULATION RESULTS AND ANALYSIS

In this section, simulation results are presented to validate the effectiveness of the proposed approach.

## A. Simulation Setup

1) Scenarios: We consider a UAV-assisted MEC system where one MBS and four UAVs are deployed to jointly provide offloading service for 30 MDs in a $1 0 0 \times 1 0 0 0 \mathrm { \dot { m } ^ { 2 } }$ rectangular 1000 1000area. The time horizon is set as 60s, and it is divided into $T = 6 0 0$ time slots with equal length of $\delta = 1 0 0 ~ \mathrm { m s }$ = 600, and 10 time slots are grouped into a time epoch, $\mathrm { i . e . , } \Delta = 1 \mathrm { ~ s ~ }$

Î = 12) Parameters: For the MBS, the location and height are set as [500, 500] and 10 m [41], respectively. For UAVs, the fixed altitude is set as $H = 1 0 0 \mathrm { m }$ , and the initial positions and destinations are set as $( \mathbf { q } _ { 1 } ^ { I } , \mathbf { q } _ { 1 } ^ { F } ) = ( [ 5 0 , 9 0 0 ] , [ 5 0 0 , 5 0 0 ] ) , ( \mathbf { q } _ { 2 } ^ { I } , \mathbf { q } _ { 2 } ^ { F } ) =$ (, , , , $( \tilde { \mathbf { q } _ { 3 } ^ { I } } , \mathbf { q } _ { 3 } ^ { F } ) \stackrel { = } { = } \left( [ 1 0 0 , 1 0 \stackrel { . . . } { 0 } ] , [ 5 0 0 , 5 0 0 ] \right)$ , $( \mathbf { \bar { q } } _ { 4 } ^ { I } , \mathbf { q } _ { 4 } ^ { F } ) \stackrel { = } { = } \left( [ 8 0 0 , 1 0 \dot { 0 } 0 ] , [ 5 0 0 , 5 0 0 ] \right)$ = ([100 100] [500 500]), respectively. The default ( ) = ([800 1000] [500 500])values of the other parameters are listed in Table II.

3) Benchmarks: This work evaluates the proposed TJCCT in comparison with the following schemes.

Local-only strategy (LS): All MDs process the tasks locally without considering the MEC server resource allocation and UAV trajectory control.

Equal computing resource allocation strategy (ECRAS): the available computing resources of each MEC server are equally allocated to the requested MDs, and the strategies of computation offloading and trajectory control are determined based on TJCCT.

TABLE II SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Default value</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>CPUparameters</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 8 } \ [ 4 2 ] } }$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { \beta _ { \mathrm { T } } ^ { \mathrm { L } } / \beta _ { \mathrm { T } } ^ { \mathrm { N } } } }$ </td><td rowspan=1 colspan=1>Pathloss exponent for terrestrialcommunication</td><td rowspan=1 colspan=1>2.42/4.28 [43]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \beta _ { \mathrm { A } } } }$ </td><td rowspan=1 colspan=1>Path loss exponent for aerial com-munication</td><td rowspan=1 colspan=1>2 [34]</td></tr><tr><td rowspan=1 colspan=1> $\kappa$ </td><td rowspan=1 colspan=1>Additional attenuation factor forNLoS aerial communication</td><td rowspan=1 colspan=1>0.2[34]</td></tr><tr><td rowspan=1 colspan=1> $G _ { i } ^ { \mathrm { m a x } }$ </td><td rowspan=1 colspan=1>ThebudgetofMDi for the costspayed to the servers</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1> $\overline { { d _ { 0 } ^ { \mathrm { T } } / d _ { 0 } ^ { \mathrm { A } } } }$ </td><td rowspan=1 colspan=1>Reference distancesforMD-MBS/MD-UAV communication</td><td rowspan=1 colspan=1>1m/1 m [41]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { d _ { 1 } / d _ { 2 } } }$ </td><td rowspan=1 colspan=1>Environment parameters</td><td rowspan=1 colspan=1>18 m/36 m [41]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { m _ { \mathrm { T } } ^ { \mathrm { L } } / m _ { \mathrm { T } } ^ { \mathrm { N } } / } }$  $m _ { \mathrm { A } } ^ { \mathrm { L } } / m _ { \mathrm { A } } ^ { \mathrm { N } }$ </td><td rowspan=1 colspan=1>Nakagami fading parameter</td><td rowspan=1 colspan=1>4/2/3/1 [44]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { n _ { j } ^ { \mathrm { c o r e } } } }$ </td><td rowspan=1 colspan=1>CPU core number of MEC serverj</td><td rowspan=1 colspan=1>[2, 10]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N _ { 0 } } }$ </td><td rowspan=1 colspan=1>Noise power</td><td rowspan=1 colspan=1>-98 dBm</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \sigma ^ { \mathrm { L } } / \sigma ^ { \mathrm { N } } } }$ </td><td rowspan=1 colspan=1>Standard deviation of shadowingfor LoS/NLoS communication</td><td rowspan=1 colspan=1>4/6 [29]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \tau _ { i } ^ { t } } }$ </td><td rowspan=1 colspan=1>The deadline of task</td><td rowspan=1 colspan=1>[0.1, 5] s [45]</td></tr><tr><td rowspan=1 colspan=1> $\frac { \mathrm { {  m i n } } } { v _ { \mathrm { U } } ^ { \mathrm { { m i n } } } / v _ { \mathrm { U } } ^ { \mathrm { { m a x } } } }$ </td><td rowspan=1 colspan=1>The constraints of UAV velocity</td><td rowspan=1 colspan=1>0/30 m/s [34]</td></tr><tr><td rowspan=1 colspan=1> $p _ { 1 } , p _ { 2 }$ </td><td rowspan=1 colspan=1>Parameters for LoS probability ofMD-UAV link</td><td rowspan=1 colspan=1>10, 0.6 [28],[34]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { i } } }$ </td><td rowspan=1 colspan=1>Transmit power of each MD</td><td rowspan=1 colspan=1>[10,25] dBm</td></tr><tr><td rowspan=1 colspan=1> $\overline { { d ^ { \mathrm { s a f e } } } }$ </td><td rowspan=1 colspan=1>Safetydistance between UAVs</td><td rowspan=1 colspan=1>10m [25]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B _ { i , j } } }$ </td><td rowspan=1 colspan=1>Bandwidth between MDiandMEC server j</td><td rowspan=1 colspan=1>20MHz ${ \overline { { ( j = b ) } } } ,$ 10MHz ${ \bf \Xi } ( j { \bf \Xi } ) \in { \bf \Xi }$ u)[35]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mu _ { i } ^ { t } } }$ </td><td rowspan=1 colspan=1>Computation intensity of tasks</td><td rowspan=1 colspan=1>[500,1500] cy-cles/bit</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Task size</td><td rowspan=1 colspan=1>[1,5] Mb [46]</td></tr><tr><td rowspan=1 colspan=1> $\textstyle \frac { \iota } { E _ { i } ^ { \mathrm { m a x } } }$ </td><td rowspan=1 colspan=1>Energy constraint of MD i</td><td rowspan=1 colspan=1>1 (W.h/GHz)</td></tr><tr><td rowspan=1 colspan=1> $\frac { \ - \alpha _ { \eta } } { E _ { j } ^ { \mathrm { m a x } } }$ </td><td rowspan=1 colspan=1>Energy constraint of MEC serverj</td><td rowspan=1 colspan=1>1   (Wh/GHz)(j=b)360kJ(jâu)</td></tr><tr><td rowspan=1 colspan=1>fmax</td><td rowspan=1 colspan=1>Computing resources of MDi</td><td rowspan=1 colspan=1>[0.5, 1] GHz</td></tr><tr><td rowspan=1 colspan=1>fmaxJj</td><td rowspan=1 colspan=1>Computingresourcesof MECserver j</td><td rowspan=1 colspan=1>[20,40] GHz (j =b)ï¼[10,20]GHz(âu)</td></tr><tr><td rowspan=1 colspan=1>Î±</td><td rowspan=1 colspan=1>Memory degree of MD&#x27;svelocity</td><td rowspan=1 colspan=1>0.9</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \boldsymbol { v } } } _ { i }$ </td><td rowspan=1 colspan=1>Theaveragevelocity ofMDi</td><td rowspan=1 colspan=1>[0,1]m/s [31]</td></tr><tr><td rowspan=1 colspan=1> $\overline { { S _ { i } ^ { v } } }$ </td><td rowspan=1 colspan=1>Standardderivationofvelocity</td><td rowspan=1 colspan=1>2 [31]</td></tr></table>

Price adjustment strategy (PAS) [3]: The price of the computing resource is adjusted upwards or downwards by a fixed factor based on the available computing resource of the MEC server. Besides, the strategies of computation offloading, computing resource allocation, and trajectory control are determined based on TJCCT.

Game-theoretic computation offloading strategy (GCOS) [2]: The computation offloading strategies of MDs are iteratively determined competitively while the strategies of computing resource allocation and trajectory control are determined based on the proposed TJCCT.

Segment-constrained trajectory control strategy (STCS) [8]: The UAV trajectory is decided based on a segmentconstrained method while the strategies of computation offloading and computing resource allocation are decided by the proposed TJCCT.

PPO-based computation offloading, computing resource allocation, and trajectory control (PCCT) [22]: The strategies of computation offloading, computing resource allocation, and UAV trajectory control are decided by the PPO algorithm [47].

DDPG-based computation offloading, computing resource allocation, and trajectory control (DCCT) [23]: The strategies of computation offloading, computing resource allocation, and UAV trajectory control are decided by the DDPG algorithm [48].

4) Performance Indicators: To evaluate the overall performance of the proposed method, we adopt the following indicators. 1) System utility $\textstyle \sum _ { t \in T } U ^ { t }$ , which indicates the aggregated utility of the MDs and MEC servers. 2) Average processing rate $\sum _ { \boldsymbol { K } _ { i } ^ { t } \in \mathcal { K } _ { \mathrm { s u c c } } } l _ { i } ^ { t } \mu _ { i } ^ { t } / T$ , which represents the CPU cycles that are completed per unit time, where ${ \mathcal { K } } _ { \mathrm { s u c c } }$ is the set of tasks that are successfully computed, $T _ { \boldsymbol { { \ K } _ { i } ^ { t } } } ^ { \mathrm { c m p } }$ and $T _ { \kappa _ { i } ^ { t } } ^ { \mathrm { g e n } }$ are the completion time and generation time of the computation, respectively. 3) Average completion delay $\begin{array} { r } { \sum _ { \mathcal { K } _ { i } ^ { t } \in \mathcal { K } _ { \mathrm { s u c c } } } ( T _ { \mathcal { K } _ { i } ^ { t } } ^ { \mathrm { c m p } } - \mathbf { \dot { T } } _ { \mathcal { K } _ { i } ^ { t } } ^ { \mathrm { g e n } } ) / \vert \mathbf { \dot { K } } _ { \mathrm { s u c c } } \vert } \end{array}$ , which indicates the average delay for successfully completing a task, where $| { \cal K } _ { s u c c } |$ is the number of tasks that are completed. 4) Average completion ratio $| { \cal K } _ { \mathrm { s u c c } } | / { \sum _ { t \in { \mathcal T } } \sum _ { i \in { \mathcal T } } \zeta _ { i } ^ { t } }$ , which indicates the average ratio of tasks that are completed. 5) Average cost $\begin{array} { r } { \sum _ { \mathcal { K } _ { i } ^ { t } \in \mathcal { K } _ { \mathrm { s u c c } } } \Bigl ( \bigl ( \frac { D _ { i , i } ^ { t } } { \tau _ { i } ^ { t } } + \bigr . } \end{array}$ $\begin{array} { r } { \frac { E _ { i , i } ^ { t } } { E _ { i } ^ { \mathrm { m a x } } } \big ) o _ { i , i } ^ { t } + ( \frac { D _ { i , j } ^ { t } } { \tau _ { i } ^ { t } } + \frac { E _ { i , j } ^ { t } } { E _ { i } ^ { \mathrm { m a x } } } + \frac { E _ { j , i } ^ { t } } { E _ { i } ^ { \mathrm { m a x } } } ) o _ { i , j } ^ { t } ) / T . } \end{array}$ , which indicates the time-average sum of the normalized delay and normalized cost of the system. 6) Average total energy consumption $\begin{array} { r } { \sum _ { \mathcal { K } _ { i } ^ { t } \in \mathcal { K } _ { \mathrm { s u c c } } } \big ( E _ { i , i } ^ { t } \dot { o } _ { i , i } ^ { t } + ( E _ { i , j } ^ { t } + E _ { j , i } ^ { \tilde { t } } ) o _ { i , j } ^ { t } \big ) / T . } \end{array}$ which indicates ( + ( + ) )the average total energy consumption of the system during the considered system time. 7) Average computation energy consumption $\textstyle \sum _ { \mathcal { K } _ { i } ^ { t } \in { \mathcal { K } _ { \mathrm { s u c c } } } } { ( E _ { i , i } ^ { t } { o } _ { i , i } ^ { t } + E _ { j , i } ^ { t , \mathrm { c o m p } } { o } _ { i , j } ^ { t } ) } / T$ which ( + )indicates the average total energy consumption of the MDs and MEC servers during the considered system time. 8) Average flight energy consumption $\sum _ { j \in U } E _ { j } ^ { t , \mathrm { { f l y } } } / T$ , which indicates the average flight energy consumption of the UAVs during the considered system time.

## B. Evaluation Results

In this section, we first evaluate the system performance of the proposed TJCCT over time with default parameters. Subsequently, we compare the impacts of different parameters on the performance of the proposed TJCCT and the benchmark algorithms.

1) Performance Evaluation: Fig. 2(a), (b), (c), (d), (e), (f), (g), and (h) compare the performances of system utility, average processing rate, average completion delay, average completion ratio, average cost, average total energy consumption, average computing energy consumption, and average flight energy consumption, respectively with time slots. It can be observed that the proposed TJCCT outperforms other algorithms in terms of system utility, average processing rate, average completion delay, average completion ratio, and average cost with gradualsignificant performance advantages as the time elapses. Moreover, it also achieves relatively lower flight energy consumption but exhibits higher total energy consumption and computing energy consumption.

Several factors contribute to the above outcomes. First, the methods of resource trading, matching, and UAV trajectory control facilitate satisfactory computation offloading between MDs and MEC servers, leading to long-term benefits for both MDs and MEC servers and enhanced system utility. Moreover, the superior performances in processing rate, completion delay, and completion ratio stem from prioritizing computation quality, ensuring timely processing for delay-sensitive tasks. Furthermore, the balanced and superior average cost of the proposed TJCCT is achieved by optimizing the trade-off between delay and energy consumption, focusing on providing high computation quality while managing energy usage effectively. In addition, the design of UAV trajectory control makes the proposed TJCCT energyefficient during flight. Besides, the inferior performances in total energy consumption and computation energy consumption result from prioritizing computation quality over energy savings, which is crucial for scenarios with computation-intensive and delay-sensitive tasks.

<!-- image-->  
(a) System utility

<!-- image-->  
(b) Average processing rate

<!-- image-->  
(c) Average completion delay

<!-- image-->  
(d) Average completion ratio

<!-- image-->  
(e) Average cost

<!-- image-->

<!-- image-->

<!-- image-->  
(f)Average total energy consump-(gï¼ Average computing energy(hï¼Average flight energy contion consumption sumption

Fig. 2. System performance with time.  
<!-- image-->  
(a) System utility

<!-- image-->  
(b) Average processing rate

<!-- image-->  
(c) Average completion delay

<!-- image-->  
(d) Average completion ratio

<!-- image-->  
(e) Average cost

<!-- image-->

<!-- image-->

<!-- image-->  
(f)Average total energy consump-(gï¼ Average computing energy(hï¼ Average flight energy contion consumption sumption  
Fig. 3. System performance with the number of MDs.

In conclusion, this set of simulation results demonstrates that the proposed TJCCT is able to achieve superior overall performance while still meeting the energy constraints despite the trade-off of the increased energy consumption. Moreover, the proposed TJCCT can also be applied in the scenarios with various requirements on delay and energy consumption by adjusting the corresponding weights.

2) Impact of Parameters: Impact of MD Numbers: Fig. 3(a), (b), (c), (d), (e), (f), (g), and (h) depict the impact of MD numbers on system utility, average processing rate, average completion delay, average completion ratio, average cost, average total energy consumption, average computing energy consumption, and average flight energy consumption, respectively. Overall, the proposed TJCCT consistently demonstrates superior performance in terms of system utility, average processing rate, average completion delay, and average completion ratio as the number of MDs increases. It also exhibits inferior performance in total energy consumption and computation energy consumption among the eight algorithms, and shows similar performance in flight energy consumption compared to the benchmark schemes except STCS.

Specifically, Fig. 3(a) and (b) reveal that with an increasing number of MDs, the system utility and processing rate of TJCCT steadily rise, while those of the other algorithms exhibit minor initial upward trends, followed by gradual slowdowns, and approach stability or show decreasing tendencies. Furthermore, as shown in Fig. 3(c) and (d), it is evident that with an increasing number of MDs, the average completion delay and completion ratio of LS remain the worst levels while those of ECRAS, PAS, GCOS, STCS, PCCT, and DCCT exhibit obvious deterioration trends. In comparison, the proposed JTCCT show consistently superior performances with slight performance degradation in the average completion ratio and average completion delay, which vary within the range of 0.70s to 1.25s and 1% to 0.93%, respectively. More specifically, compared with LS, ECRAS, PAS, GCOS, STCS, PCCT, and DCCT, the proposed JTCCT can respectively reduce the completion delay by 79%, 41%, 23%, 63%, 77%, 68%, 70% and can respectively improve the completion ratio by 661%, 30%, 8%, 312%, 68%, 106%, 127% in the relative dense scenario (|I| â¥ ). Moreover, 90Fig. 3(e) to (h) demonstrate that the proposed JTCCT maintains a competitive average cost, exhibits a higher total energy consumption and computation, and shows constant flight energy consumption with varying-density scenarios.

On the one hand, the main reasons for the phenomena in Fig. 3(a) to (d) can be explained as follows. First, increasing amounts of computation are accomplished with the rising number of MDs, leading to the initial performance gains for most comparative algorithms in system utility, processing rate, completion delay, and completion ratio. Moreover, without efficient strategies for computation offloading, resource allocation, or trajectory control, the increasingly growing MDs could increase resource shortage at MEC servers, which further causes performance saturation or degradation in these aspects. On the other hand, the phenomena displayed in Fig. 3(e) to (h) can be attributed to the following reasons. First, the proposed TJCCT aims to task processing quality and resource utilization costeffectively, leading to the competitive performance in average cost of the system. Moreover, although the proposed TJCCT incurs higher computation energy consumption, it can achieve superior performances related to task processing. Besides, the UAV trajectory control strategy of the proposed TJCCT manages the energy consumption effectively during the flight. In conclusion, although the proposed TJCCT incurs higher computation energy consumption with an increasing number of MDs, it has better scalability to efficiently accomplish the delay-sensitive and computation-intensive tasks while maintaining lower system costs.

Impact of Average Computation Size: The impact of average computation size on the system performance for the comparative algorithms is given in Fig. 2 in Section M of the supplementary material. The simulation results demonstrate that the proposed TJCCT is able to adapt to the heavy-loaded scenarios with superior overall performance while meeting energy constraints, despite the trade-off of increased energy consumption.

Impact of Average Computing Resources of MEC Server: The impact of average computing resources of MEC servers on the system performance for the comparative algorithms is given in Fig. 3 in Section N of the supplementary material. The results demonstrate that the proposed TJCCT is able to achieve on-demand and efficient computing resource utilization by adjusting the decisions based on the available computing resources of MEC servers and the requirements of MDs.

3) UAV Trajectory: Fig. 4 shows the trajectories of the MDs and UAVs. It can be observed the trajectories of UAVs are consistent with the intuition. Specifically, UAVs tend to follow the trajectories of the MDs and tend to identify regions with dense data requirements. This is because the UAVs try to satisfy the QoE of the MDs for task offloading under the constraints of energy and velocity. Furthermore, it should be noted that the UAVs approach the final destinations but do not arrive at the destinations. The reason is that UAVs maintain a safe distance between each other to avoid collisions. In conclusion, the simulation result in Fig. 4 demonstrates that the UAVs can provide satisfied services according to the dynamic requirements of MDs while guaranteeing the safety of UAVs by adopting the trajectory control of the proposed TJCCT.

<!-- image-->  
Fig. 4. Trajectories of the MDs and UAVs.

## VII. DISCUSSION

To demonstrate the rationale for ignoring the costs of information gathering mentioned in Section III-C2, we show the impact of the information gathering. Specifically, the corresponding simulation results are shown in Fig. 4 of Appendix O of the supplemental material, available online. First, the simulation shows that the costs of latency and energy consumption for information gathering are significantly minor. Moreover, even when considering these costs, the proposed TJCCT still outperforms the comparative methods in terms of the performance metrics related to task processing while satisfying the energy constraints. In conclusion, this set of simulation results demonstrate the fairness of omitting the costs of information collection.

## VIII. CONCLUSION

In this work, we study computing resource allocation, computation offloading, and UAV trajectory control for UAV-assisted MEC system. First, we employ a hierarchical framework to coordinate the collaboration among MDs, terrestrial edge, aerial edge, and the controller. Then, we formulate an optimization problem to maximize the system utility. To solve the MINLP problem, we propose the TJCCT which consists of twotimescale optimization methods. In the short timescale, we propose a price-incentive model for on-demand computing resource allocation and a matching mechanism-based method for computation offloading. In the long timescale, we propose a convex optimization-based method for UAV trajectory control. Besides, the stability, optimality, and complexity of TJCCT are theoretically proved. Simulation results demonstrate that the proposed TJCCT is able to achieve superior performances in terms of the system utility, average processing rate, average completion delay, average completion ratio, and average cost. Moreover, although the proposed TJCCT exhibits inferior performance in energy consumption, it maintains a balanced and superior average cost by optimizing the trade-off between delay and energy consumption. This indicates that the proposed TJCCT is wellsuited for delay-sensitive and computation-intensive scenarios, ensuring superior task processing performance. Furthermore, TJCCT exhibits superior adaptability in heavy-loaded scenarios and demonstrates good scalability with an increasing number of MDs.

## REFERENCES

[1] Y. Qu et al., âCoTask: Correlation-aware task offloading in edge computing,â World Wide Web, vol. 25, no. 5, pp. 2185â2213, 2022.

[2] Y. Wang et al., âA game-based computation offloading method in vehicular multiaccess edge computing networks,â IEEE Internet Things J., vol. 7, no. 6, pp. 4987â4996, Jun. 2020.

[3] M. Tao, X. Li, K. Ota, and M. Dong, âSingle-cell multiuser computation offloading in dynamic pricing-aided mobile edge computing,â IEEE Trans. Comput. Soc. Syst., vol. 11, no. 2, pp. 3004â3014, Apr. 2024.

[4] C. You and K. Huang, âExploiting non-causal CPU-state information for energy-efficient mobile cooperative computing,â IEEE Trans. Wireless Commun., vol. 17, no. 6, pp. 4104â4117, Jun. 2018.

[5] X. Xie, T. Bai, W. Guo, Z. Wang, and A. Nallanathan, âCooperative computing for mobile crowdsensing: Design and optimization,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 6437â6454, May 2024.

[6] Z. Wei, B. Li, R. Zhang, X. Cheng, and L. Yang, âMany-to-many task offloading in vehicular fog computing: A multi-agent deep reinforcement learning approach,â IEEE Trans. Mobile Comput., vol. 23, no. 3, pp. 2107â2122, Mar. 2024.

[7] N. Lin, H. Tang, L. Zhao, S. Wan, A. Hawbani, and M. Guizani, âA PDDQNLP algorithm for energy efficient computation offloading in UAV-assisted MEC,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8876â8890, Dec. 2023.

[8] Y. Wang et al., âTask offloading for post-disaster rescue in unmanned aerial vehicles networks,â IEEE/ACM Trans. Netw., vol. 30, no. 4, pp. 1525â1539, Aug. 2022.

[9] Y. K. Tun, T. N. Dang, K. Kim, M. Alsenwi, W. Saad, and C. S. Hong, âCollaboration in the sky: A distributed framework for task offloading and resource allocation in multi-access edge computing,â IEEE Internet Things J., vol. 9, no. 23, pp. 24221â24235, Dec. 2022.

[10] N. N. Ei, M. Alsenwi, Y. K. Tun, Z. Han, and C. S. Hong, âEnergy-efficient resource allocation in multi-UAV-assisted two-stage edge computing for beyond 5G networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 16421â16432, Sep. 2022.

[11] Z. Han, T. Zhou, T. Xu, and H. Hu, âJoint user association and deployment optimization for delay-minimized UAV-aided MEC networks,â IEEE Wireless Commun. Lett., vol. 12, no. 10, pp. 1791â1795, Oct. 2023.

[12] D. Wang, J. Tian, H. Zhang, and D. Wu, âTask offloading and trajectory scheduling for UAV-enabled MEC networks: An optimal transport theory perspective,â IEEE Wireless Commun. Lett., vol. 11, no. 1, pp. 150â154, Jan. 2022.

[13] Y. Shi, C. Yi, B. Chen, C. Yang, and J. Cai, âA two-timescale online optimization for balancing service migration and task rerouting in MEC,â in Proc. Proc. IEEE Glob. Commun. Conf., 2023, pp. 5500â5505.

[14] Y. Shi, C. Yi, R. Wang, Q. Wu, B. Chen, and J. Cai, âService migration or task terouting: A two-timescale online resource optimization for MEC,â IEEE Trans. Wireless Commun., vol. 23, no. 2, pp. 1503â1519, Feb. 2024.

[15] Y. Yang et al., âDynamic human digital twin deployment at the edge for task execution: A two-timescale accuracy-aware online optimization,â 2024, arXiv:2401.16710.

[16] Y. Shi, Y. Yang, C. Yi, B. Chen, and J. Cai, âTowards online reliabilityenhanced microservice deployment with layer sharing in edge computing,â IEEE Internet Thing J., vol. 11, no. 13, pp. 23370â23383, Jul. 2024.

[17] N. M. Laboni, S. J. Safa, S. Sharmin, M. A. Razzaque, M. M. Rahman, and M. M. Hassan, âA hyper heuristic algorithm for efficient resource allocation in 5G mobile edge clouds,â IEEE Trans. Mobile Comput., vol. 23, no. 1, pp. 29â41, Jan. 2024.

[18] J. Tian, D. Wang, H. Zhang, and D. Wu, âService satisfaction-oriented task offloading and UAV scheduling in UAV-enabled MEC networks,â IEEE Trans. Wireless Commun., ol. 22, no. 12, pp. 8949â8964, Dec. 2023.

[19] Z. Ning et al., âDynamic computation offloading and server deployment for UAV-enabled multi-access edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2628â2644, May 2023.

[20] A. M. Seid, G. O. Boateng, S. Anokye, T. Kwantwi, G. Sun, and G. Liu, âCollaborative computation offloading and resource allocation in multi-UAV-assisted IoT networks: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 8, no. 15, pp. 12203â12218, Aug. 2021.

[21] F. Song et al., âEvolutionary multi-objective reinforcement learning based trajectory control and task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7387â7405, Dec. 2023.

[22] W. Xu, T. Zhang, X. Mu, Y. Liu, and Y. Wang, âTrajectory planning and resource allocation for multi-UAV cooperative computation,â IEEE Trans. Commun., vol. 72, no. 7, pp. 4305â4318, Jul. 2024.

[23] J. Miao, S. Bai, S. Mumtaz, Q. Zhang, and J. Mu, âUtility-oriented optimization for video streaming in UAV-aided MEC network: A DRL approach,â IEEE Trans. Green Commun. Netw., vol. 8, no. 2, pp. 878â889, Jun. 2024.

[24] L. Li et al., âData-driven optimization for cooperative edge service provisioning with demand uncertainty,â IEEE Internet Things J., vol. 8, no. 6, pp. 4317â4328, Mar. 2021.

[25] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint cache placement, flight trajectory, and transmission power optimization for multi-UAV assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5389â5403, Aug. 2020.

[26] Y. Dai, D. Xu, S. Maharjan, and Y. Zhang, âJoint load balancing and offloading in vehicular edge computing and networks,â IEEE Internet Things J., vol. 6, no. 3, pp. 4377â4387, Jun. 2019.

[27] âStudy on 3D channel model for LTE; Release 12,â V12.7.0, 3GPP, Tech. Rep. TR 36.873, Dec. 2014.

[28] A. Al-Hourani, K. Sithamparanathan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[29] âStudy on channel model for frequencies from 0.5 to 100 GHz; Release 16,â 3GPP, V16.1.0, Tech. Rep. TR 38.901, Nov. 2020.

[30] A. Boumaalif and O. Zytoune, âPower distribution of device-to-device communications under Nakagami fading channel,â IEEE Trans. Mob. Comput., vol. 21, no. 6, pp. 2158â2167, Jun. 2022.

[31] Z. Yang, S. Bi, and Y. A. Zhang, âOnline trajectory and resource optimization for stochastic UAV-enabled MEC systems,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5629â5643, Jul. 2022.

[32] T. D. Burd and R. W. Brodersen, âProcessor design for portable systems,â J. VLSI Signal Process. Syst. Signal, Image Video Technol., vol. 13, no. 2, pp. 203â221, 1996.

[33] Y. Pan, C. Pan, K. Wang, H. Zhu, and J. Wang, âCost minimization for cooperative computation framework in MEC networks,â IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3670â3684, Jun. 2021.

[34] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[35] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and A. Nallanathan, âDeep reinforcement learning based dynamic trajectory control for UAV-assisted mobile edge computing,â IEEE Trans. Mobile Comput., vol. 21, no. 10, pp. 3536â3550, Oct. 2022.

[36] A. W. Malik, A. U. Rahman, M. Ali, and M. M. Santos, âSymbiotic robotics network for efficient task offloading in smart industry,â IEEE Trans. Ind. Inform., vol. 17, no. 7, pp. 4594â4601, Jul. 2021.

[37] M. Wang, T. Wu, T. Ma, X. Fan, and M. Ke, âUsersâ experience matter: Delay sensitivity-aware computation offloading in mobile edge computing,â Digit. Commun. Netw., vol. 8, no. 6, pp. 955â963, 2022.

[38] S. Xia, Z. Yao, Y. Li, and S. Mao, âOnline distributed offloading and computing resource management with energy harvesting for heterogeneous MEC-enabled IoT,â IEEE Trans. Wireless Commun., vol. 20, no. 10, pp. 6743â6757, Oct. 2021.

[39] A. Rubinstein, âPerfect Equilibrium in a bargaining model,â Econometrica J., vol. 50, pp. 97â109, 1982.

[40] H. Wu, F. Lyu, C. Zhou, J. Chen, L. Wang, and X. Shen, âOptimal UAV caching and trajectory in aerial-assisted vehicular networks: A learning-based approach,â IEEE J. Select. Areas Commun., vol. 38, no. 12, pp. 2783â2797, Dec. 2020.

[41] âStudy on channel model for frequencies from 0.5 to 100 GHz; Release 14,â 3GPP, V14.0.0, Tech. Rep. TR 38.901, May 2017.

[42] H. Hu, W. Song, Q. Wang, R. Q. Hu, and H. Zhu, âEnergy efficiency and delay tradeoff in an MEC-enabled mobile IoT network,â IEEE Internet Thing J., vol. 9, no. 17, pp. 15942â15956, Sep. 2022.

[43] B. Yang, G. Mao, M. Ding, X. Ge, and X. Tao, âDense small cell networks: From noise-limited to dense interference-limited,â IEEE Trans. Veh. Technol., vol. 67, no. 5, pp. 4262â4277, May 2018.

[44] J. Peng, W. Tang, and H. Zhang, âDirectional antennas modeling and coverage analysis of UAV-assisted networks,â IEEE Wireless Commun. Lett., vol. 11, no. 10, pp. 2175â2179, Oct. 2022.

[45] S. A. Kazmi et al., âA novel contract theory-based incentive mechanism for cooperative task-offloading in electrical vehicular networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 8380â8395, Jul. 2022.

[46] Z. Yu, Y. Gong, S. Gong, and Y. Guo, âJoint task offloading and resource allocation in UAV-enabled mobile edge computing,â IEEE Internet Things J., vol. 7, no. 4, pp. 3147â3159, Apr. 2020.

[47] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, âProximal policy optimization algorithms,â 2017, arXiv: 1707.06347.

<!-- image-->

[48] D. Silver, G. Lever, N. Heess, T. Degris, D. Wierstra, and M. Riedmiller, âDeterministic policy gradient algorithms,â in Proc. Int. Conf. Mach. Learn., 2014, pp. 387â395.

<!-- image-->  
Zemin Sun (Member, IEEE) received the BS degree in software engineering, the MS degree and PhD degrees in computer science and technology from Jilin University, Changchun, China, in 2015, 2018, and 2022, respectively. Her research interests include vehicular networks, edge computing, and game theory.

<!-- image-->

<!-- image-->

Geng Sun (Senior Member, IEEE) received the BS degree in communication engineering from Dalian Polytechnic University, and the PhD degree in computer science and technology from Jilin University, in 2011 and 2018, respectively. He was a visiting researcher with the School of Electrical and Computer Engineering, Georgia Institute of Technology, USA. He is a professor with the College of Computer Science and Technology, Jilin University. His research interests include wireless networks, UAV communications, collaborative beamforming and optimizations.

<!-- image-->

<!-- image-->

Qingqing Wu (Senior Member, IEEE) received the BEng and the PhD degrees in electronic engineering from the South China University of Technology and Shanghai Jiao Tong University (SJTU), in 2012 and 2016, respectively. From 2016 to 2020, he was a research fellow with the Department of Electrical and Computer Engineering, National University of Singapore. He is currently an associate professor with Shanghai Jiao Tong University. His current research interest includes intelligent reflecting surface (IRS), unmanned aerial vehicle (UAV) communications, and

MIMO transceiver design.

<!-- image-->

<!-- image-->

Shuang Liang received the BS degree in communication engineering from Dalian Polytechnic University, China, in 2011, the MS degree in software engineering from Jilin University, China, in 2017, and the PhD degree in computer science from Jilin University, China, in 2022. She is a post-doctoral with the School of Information Science and Technology, Northeast Normal University, and her research interests focus on wireless communication and UAV networks.

Long He received the BS degree in computer science and technology from the Chengdu University of Technology, Sichuan, China, in 2019. He is currently working toward the PhD degree in computer science and technology with Jilin University, Changchun, China. His research interests include vehicular networks and edge computing.

Hongyang Pan received the BS degree in process equipment and control engineering from the Dalian University of Technology, in 2017. He is currently working toward the PhD degree in computer science and technology, Jilin University. His research interests include the wireless communications and optimizations.

Dusit Niyato (Fellow, IEEE) received the BEng degree from the King Mongkuts Institute of Technology Ladkrabang (KMITL), Thailand, in 1999, and the PhD degree in electrical and computer engineering from the University of Manitoba, Canada, in 2008. He is currently a professor with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. His research interests include the Internet of Things (IoT), machine learning, and incentive mechanism design.

<!-- image-->

Chau Yuen (Fellow, IEEE) received the BEng and PhD degrees in information and communication from Nanyang Technological University, Singapore, in 2000 and 2004, respectively. He was a post-doctoral fellow with the Lucent Technologies Bell Laboratories, Murray Hill, in 2005. From 2006 to 2010, he was with the Institute for Infocomm Research (12R), Singapore. Since 2010, he has been with the Singapore University of Technology and Design.

Victor C. M. Leung (Life Fellow, IEEE) is a dean and professor with Artificial Intelligence Research Institute Shenzhen MSU-BIT University, Shenzhen, Gongdong, China. He is a distinguished professor of computer science and software engineering with Shenzhen University, Shenzhen. He is also an Emeritus professor of electrial and computer engineering and the director with the Laboratory for Wireless Networks and Mobile Systems, University of British Columbia (UBC). His research is in the broad areas of wireless networks and mobile systems.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_1.jpeg|page_18_img_1]]
3. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_2.jpeg|page_18_img_2]]
4. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_3.jpeg|page_18_img_3]]
5. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_4.jpeg|page_18_img_4]]
6. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_5.jpeg|page_18_img_5]]
7. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_6.jpeg|page_18_img_6]]
8. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_7.jpeg|page_18_img_7]]
9. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_8.jpeg|page_18_img_8]]
10. [[../extracted_images/TJCCT_A_Two-Timescale_Approach_for_UAV-Assisted_Mobile_Edge_Computing/page_18_img_9.jpeg|page_18_img_9]]

---

