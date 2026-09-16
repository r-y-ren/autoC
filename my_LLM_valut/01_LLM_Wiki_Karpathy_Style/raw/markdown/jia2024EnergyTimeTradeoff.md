# Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices

Riheng Jia , Qiyong Fu , Zhonglong Zheng , Guanglin Zhang , Member, IEEE, and Minglu Li , Fellow, IEEE

Abstractâ In this work, we study the problem of dispatching multiple unmanned aerial vehicles (UAVs) for data collection in internet of things (IoT), where each UAV departs from its start point, visits some IoT devices for data collection and returns to its destination point. Considering the UAVâs limited onboard energy and the time required to collect data from all IoT devices, it is essential to appropriately assign the data collection task for each UAV, such that none of the dispatched UAVs consumes excessive energy and the maximum task completion time among all UAVs is minimized. To optimize those two conflicting objectives, we focus on minimizing the maximum task completion time and the maximum energy consumption among all UAVs, by jointly designing the flight trajectory, hovering positions for data collection and flight speed of each UAV. We formulate this problem as a multiobjective optimization problem with the aim of obtaining a set of Pareto-optimal solutions in terms of time or energy dominance. Due to the NP-hardness and complexity of the formulated problem, we propose a multi-strategy multi-objective ant colony optimization algorithm (MSMOACO), which is developed based on a constrained ant colony optimization algorithm with a fitnessguided mutation strategy and an adaptive hovering strategy being delicately incorporated, to solve the problem. To accommodate the practical scenario, we also design a novel geometry-based collision avoidance strategy to reduce the possibility of collisions among UAVs. Extensive evaluations validate the effectiveness and superiority of the proposed MSMOACO, compared with previous approaches.

Index Termsâ Multi-UAV network, multi-objective optimization, cooperative trajectory planning, speed control.

## I. INTRODUCTION

WITH the rapid development of the internet of things(IoT) and the corresponding ever-increasing data gen- (IoT) and the corresponding ever-increasing data generation rate, more efficient and robust data collection methods are required to enable the better decision-making process. Traditional data collection methods usually face limitations [1], such as the inability to quickly reach distant target areas, difficulty in obtaining high-quality data and restrictions related to terrain and environmental conditions. In recent years, the unmanned aerial vehicle (UAV)-enabled data collection technology has attracted extensive attentions and applications, since UAVs have various advantages including the fast deployment, high maneuverability, large-area coverage, high communication efficiency and so on [2], [3], [4], [5], [6], [7], [8], [9], and [10].

<!-- image-->  
Fig. 1. Network model.

In this work, we investigate the problem of dispatching multiple UAVs for data collection of IoT devices in a largescale IoT network, where a large number of IoT devices are sparsely located at some fixed locations to monitor network events. Each IoT device needs to upload a certain amount of data, which is then used for decision-making of the system. Due to the limited energy of IoT devices and sparse distribution of IoT devices, it is usually unrealistic for them to deliver the generated data to a data sink via the multihop transmission. Thus, multiple UAVs are dispatched to cooperatively collect data from all IoT devices deployed within the network. Each UAV departs from its start point (SP), visits some IoT devices and returns to its destination point (DP). To ensure the data transmission efficiency, we assume that the UAV must hover within the communication range of a visited IoT device while collecting data from it. Thus it is essential to identify an appropriate hovering position near each IoT device, since the hovering position affects both the data transmission rate and the UAVâs flight trajectory. For example in Fig. 1, two UAVs depart from their SPs, then travel along two designed trajectories (i.e., the red and purple curves) and finally return to their DPs respectively. At each hovering position, the UAV spends some time collecting data from one or multiple visited IoT devices and the hovering time is decided by the data volume and the data transmission rate. For the general case, since each UAV can carry the limited amount of onboard energy, we need to carefully assign the data collection task for each UAV, such that none of the dispatched UAVs consumes excessive energy. On the other hand, to ensure the freshness of the collected data, it is essential to minimize the time from when all UAVs are simultaneously dispatched until the last UAV returns to its DP, i.e., reducing the longest task completion time among all UAVs. Thus in this work, we aim to minimize the maximum task completion time and the maximum energy consumption among all UAVs, such that each IoT device successfully uploads its requested amount of data. We list the challenges of problem-solving as follows.

Large and complex decision space: Solving the proposed problem involves optimizing the following decision variables: 1) the exact IoT devices to be visited by each UAV and the corresponding visiting order; 2) the hovering position of each UAV for each of its visited IoT devices; 3) the flight speed of each UAV. The above decision variables have different dimensions and mutual influence, making it challenging to find the optimal solution.

Two conflicting optimizing objectives and NP-hardness: There exists a trade-off between the maximum task completion time and the maximum energy consumption among all UAVs. For example, the task completion time can be reduced by increasing the UAVâs flight speed, which however may exponentially increase the UAVâs flight power consumption [11]. The NP-hardness can be proved by reducing the proposed problem into a single-objective multi-trajectory optimization problem, which is NP-hard [12], [13], [14].

The trade-off between the hovering time and flight time: Since the UAV can hover anywhere within the communication range of the visited IoT device for data collection, it is essential to carefully optimize the UAVâs hovering position for each IoT device to balance the hovering time (data uploading time) and flight time. For example, hovering directly above the IoT device can maximize the data uploading rate (reducing the hovering time), which however may increase the trajectory length (increasing the flight time).

To tackle the above challenges, we simultaneously minimize the maximum task completion time and the maximum energy consumption among all UAVs, by jointly optimizing the flight trajectory, hovering positions and flight speed of each UAV. We formulate the proposed problem as a multi-objective optimization problem and develop a multi-strategy multi-objective ant colony optimization algorithm (MSMOACO) to handle the complex decision space as well as the inherent trade-offs in the problem. The main contributions are summarized as follows.

1) We consider a typical multi-UAV enabled data collection scenario where multiple UAVs are dispatched to cooperatively collect data from a large number of IoT devices. From a new perspective of minimizing both the maximum task completion time and the maximum energy consumption among all UAVs, we formulate a multi-objective optimization problem by jointly considering the flight trajectory, hovering positions for data collection and flight speed of each UAV and the collision avoidance between UAVs.

2) We propose a multi-strategy multi-objective ant colony optimization algorithm (MSMOACO) to solve the formulated problem. In MSMOACO, we first develop the constrained ant colony optimization algorithm to enable the multi-trajectory planning and introduce the fitnessguided mutation strategy to deal with the premature convergence and susceptibility to local optima. Then, we devise an adaptive hovering strategy to optimize the hovering position for each IoT device, which provides feedback to further improve the trajectories designed in the first step. Finally, we devise a flight speed updating strategy to find the optimal trade-off between the two optimization objectives. In addition, we develop a novel geometry-based collision avoidance strategy to ensure UAVsâ safety during the task.

3) We conduct extensive evaluations to validate the effectiveness and superiority of the proposed method. We also reveal and explain why it makes sense for each UAV to maintain the same constant flight speed during the task, in terms of achieving the optimal time-energy trade-off.

The remainder of this work is organized as follows. We summarize the existing related works in Section II. We introduce the system model and problem formulation in Section III. We in detail illustrate the algorithm design and implementation in Section IV. We conduct the performance evaluation in Section V. Section VI concludes this work.

## II. RELATED WORKS

## A. Sing-Objective Optimization

Time-related optimization: Time-related optimization is important within the research area of UAV-enabled IoT applications, including the optimization of task completion time, data freshness, transmission time and so on. For example, Zhang et al. [15] employed the deep deterministic policy gradient (DDPG) method to minimize the task completion time of a single UAV by optimizing the association scheme of IoT devices, real-time location and velocity of the UAV. Tsai et al. [16] considered a UAV-enabled surveillance mission within an area where multiple task regions and restricted regions coexist. The minimum completion time (MinTime) algorithm was proposed to determine the optimal UAV trajectory that minimizes the mission completion time. Zhu and Wang [17] proposed a cooperative trajectory planning scheme to deal with the energy bottleneck of the UAV, where a truck moves along with a UAV to provide charging services if needed. The target is to minimize the total mission time for gathering data from all deployed sensors. In a dynamic environment with moving obstacles, Khamidehi and Sousa [18] integrated deep reinforcement learning (RL) with graph-based global path planning to find a collision-free path that the UAV will travel along to complete the data collection task in the shortest possible time. In addition, some researchers optimized the task completion time by taking into account the data freshness. For example, Liu and Zheng [8] focused on optimizing a UAVâs trajectory to minimize its data collection completion time, taking into account the age of information (AoI) of the collected data and the UAVâs limited onboard energy. Zhan et al. [19] aimed to minimize the weighted sum of operation time and total AoI for the UAV by jointly optimizing transmission scheduling, association with base stations and UAV trajectory. Different from the above works on single-UAV scenario, some researchers studied the time-related optimization problem in a multi-UAV scenario. For example, without the precise location information of IoT devices, Nie et al. [20] proposed a coarse multi-UAV trajectory design solution without repeated edges, which significantly reduces the parallel data collection completion time across multiple UAVs in large areas. Song et al. [21] investigated the multi-UAV trajectory optimization problem in free space optics (FSO) based wireless communication networks to maximize the service time for ground terminals. Xu et al. [22] proposed a three-step approach to minimize the mission completion time in a multi-UAV communication system, by jointly considering the UAVâs speed, the collision avoidance and communication interference among UAVs. Wang et al. [23] proposed a multiagent deep reinforcement learning (DRL)-based algorithm with centralized learning and decentralized execution, which cooperatively schedule multiple UAVs to collect data with the goal of minimizing the total average AoI.

Energy-related optimization: Due to the limited onboard energy of the UAV, the energy-related optimization, e.g., minimizing the energy consumption under some quality of service (QoS) constraints and maximizing the energy efficiency under UAVsâ energy constraint, draw great attention in the research area of UAV-enabled IoT applications. For example, Zhan et al. [24] introduced a novel design framework for urban aerial video surveillance. Under the constraints of onboard energy and QoS, the joint optimization of task completion time, UAV trajectory, transmission scheduling and association was performed to achieve the minimized energy consumption of the UAV. Zhu et al. [25] minimized the total energy consumption of a UAV-aided wireless sensor network (WSN), where a UAV is dispatched to collect data from cluster heads which gather data from their member nodes. A novel DRL-based technique called Ptr-Aâ was proposed, which can efficiently learn the UAV trajectory policy for minimizing the energy consumption. Dai et al. [26] proposed a generalized propulsive energy consumption model (PECM) for rotary-wing UAVs, based on which the user scheduling and UAV trajectory are jointly optimized to maximize the energy efficiency of the UAV for serving ground users. Shan et al. [27] considered a UAV-enabled data collection scenario where a UAV flies along a straight line while collecting data from ground nodes. A looking before crossing algorithm was proposed to enable the real-time speed control of the UAV, for minimizing the UAVâs flight energy consumption. Similarly, Zhou et al. [28] minimized the energy consumption of a UAV for power line inspection, taking into account the trajectory design, speed control, relay selection and power allocation. Zhan and Zeng [29] aimed to minimize the energy consumption of a cellular-connected UAV by jointly designing the UAV trajectory and base station association, while ensuring a satisfactory communication connectivity with the ground cellular network. Huynh et al. [30] proposed optimal path planning approaches for minimizing the energy consumption of multiple UAVsâ deployment for data collection, taking into account the peer-to-peer and clustering UAV-IoT sensing models respectively. To minimize the energy consumption of UAVs acting as mobile base stations to serve users, Chen et al. [31] proposed a hybrid natural-inspired optimization algorithm (HNIO) and its discrete counterpart of designing a coding strategy. Li et al. [32] aimed to find a closed-tour for an energy-constrained UAV such that the accumulated amount of data collected within the tour is maximized. The corresponding approximation and heuristic algorithms were designed to optimize the tour as well as the energy consumed on both hovering and flying.

## B. Multi-Objective Optimization

In addition to the above extensively investigated singleobjective optimization problem, we usually need to deal with multiple non-conflicting or conflicting optimization objectives in practical UAV-enabled IoT application scenarios. For example, Dai et al. [33] utilized a group of UAVs acting as aerial base stations to move around and collect data from ground users. A model-based DRL framework called GCRLmin(AoI) was proposed to maximize UAVsâ collected data and geographical coverage and minimize the AoI of all ground users simultaneously. Das et al. [34] addressed a vehicle routing problem with time windows and synchronized UAVs, where trucks work as mobile launching and retrieval sites to assist UAVsâ package delivery. A novel collaborative Pareto ant colony optimization algorithm was proposed to simultaneously minimize the travel costs and maximize the service level in terms of timely deliveries. To balance the total flight path length and the terrain threat in a UAVassisted disaster emergency response scenario, Wan et al. [35] proposed an accurate UAV 3-D path planning approach in accordance with an enhanced multi-objective swarm intelligence algorithm (APPMS), which was proved to be effective in reducing the flight time and the possibility of collision at the same time. Liao and Friderikos [36] proposed a multiobjective mixed-integer linear programming (MILP) method with a flow-based constraint set to appropriately design a single UAVâs path, for jointly optimizing the AoI and energy efficiency in a UAV-assisted wireless network. Yu et al. [37] developed the multi-objective DDPG (MODDPG) algorithm to jointly optimize three objectives including the sum data rates, total harvested energy and UAVâs energy consumption within a particular mission period. In a UAV-enabled mobile edge computing (MEC) system, Zhu et al. [38] proposed a non-dominated sorting genetic algorithm II (NSGA-II)-based solution to minimize the total cost and the completion time of all tasks, where the total cost is decided by the total flying time and the price of flying the UAV per unit time. Sun et al. [39] studied a UAV-enabled communication scenario where multiple UAVs communicate with different remote base stations (BSs) by using the virtual antenna array. Their target is to simultaneously minimize the total transmission time and total energy consumption of UAVs by jointly deciding optimal positions, flight speeds and excitation current weights of UAVs, as well as the order of communicating with different BSs. Gao et al. [40] minimized the aerial cost and the maximum mission completion time of UAVs, by optimizing the mission allocation and UAVsâ trajectories and flight speeds. In particular, the aerial cost refers to the purchase and maintenance costs of UAVs.

Our work differs from the above multi-objective optimization problems in the following main aspects: 1) We focus on minimizing the maximum task completion time and the maximum energy consumption among all dispatched UAVs, while the optimal trade-off between these two conflicting optimization objectives hasnât been analyzed yet but is important, considering the limited onboard energy of each UAV and the requirement of finishing data collection of all IoT devices timely; 2) We do not pose any constraints on the start point and destination point of each deployed UAV, which generalizes existing models for UAV-enabled data collection of IoT devices; 3) We comprehensively consider the node associations (which IoT devices to visit for each UAV), visiting order of nodes, hovering positions, flight speed and collision avoidance, making the problem-solving more challenging than most existing works.

## III. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

We consider K identical UAVs which depart from their start points (SPs), then cooperatively collect data from N IoT devices (nodes)1 randomly distributed in a certain network area, and finally return to their destination points (DPs). Note that in this work, we do not pose any constraints on the setting of UAVsâ SPs and DPs. For example, for each UAV, its SP and DP can either be the same one or two different ones.

We assume that locations of all nodes are known and each node needs to upload a certain amount of data. Without loss of generality, we adopt a three-dimensional (3-D) Cartesian coordinate system and all UAVs have the same flight altitude denoted as H. According to 3GPP specification [41], the altitude for urban macro (UMa) deployment is recommended to be 100 meters and thus we assume that all UAVs fly at a constant height of H = 100 meters.

The set of all SPs of K UAVs is denoted as $\{ K S _ { 1 } , K S _ { 2 } , \ldots , K S _ { K } \}$ and the coordinate of the k-th SP $K S _ { k }$ is represented as $K S _ { k } = ( x s _ { k } , y s _ { k } , 0 )$ , where $k \_ =$ $1 , 2 , \ldots , K .$ The set of all DPs of K UAVs is denoted as $\{ K E _ { 1 } , K E _ { 2 } , \ldots , K E _ { K } \}$ and the coordinate of the k-th $\mathsf { D P } \ K E _ { k }$ is represented as $K E _ { k } = ( x e _ { k } , y e _ { k } , 0 )$ , where $k ~ = ~ 1 , 2 , \ldots , K$ . The set of N IoT devices is denoted as $\{ S N _ { 1 } , S N _ { 2 } , \ldots , S N _ { N } \}$ and the coordinate of the n-th IoT device $S N _ { n }$ is represented as $S N _ { n } = ( x s _ { n } , y s _ { n } , 0 )$ where $n = 1 , 2 , \ldots , N .$ . The amount of data that each IoT device needs to upload is denoted as $\{ B _ { 1 } , B _ { 2 } , \ldots , B _ { N } \}$ The set of all communication ranges of N IoT devices is denoted as $\{ C _ { 1 } , C _ { 2 } , \ldots , C _ { N } \}$ . The set of K UAVsâ flight speeds is denoted as $\left\{ V _ { 1 } , V _ { 2 } , \ldots , V _ { K } \right\}$ , where $V _ { K } \in$ $[ V _ { \operatorname* { m i n } } , V _ { \operatorname* { m a x } } ]$ . In addition, to ensure the data transmission efficiency, we assume that each UAV must hover while collecting data from the corresponding IoT device. We denote the set of all hovering positions for data collection as $\{ Q _ { 1 } , Q _ { 2 } , \dots , Q _ { N } \}$ and the coordinate of the n-th hovering position $Q _ { n }$ is represented as $Q _ { n } = ( x q _ { n } , y q _ { n } , H )$ , where $n = 1 , 2 , \ldots , N$

Routing Example: Assuming the k-th UAV departs from its SP $K S _ { k }$ and sequentially visits M nodes, where $\begin{array} { r l r } { M } & { { } < } & { N } \end{array}$ We denote the set of all those visited nodes as $\{ S N _ { 1 } , S N _ { 2 } , \ldots , S N _ { M } \}$ by their visiting order, and the corresponding hovering positions are denoted as $\left\{ Q _ { 1 } , Q _ { 2 } , \dots , Q _ { M } \right\}$ . The amount of data collected from all those visited nodes is denoted as $\{ B _ { 1 } , B _ { 2 } , \dots , B _ { M } \}$ . Finally, the k-th UAV flies back to its DP $K E _ { k }$ . The entire trajectory of the k-th UAV consists of $M + 2$ points (one SP, one DP and M hovering positions) and segments connecting all pairs of neighbouring points.

1) Time and Communication Model: For each UAV k, its task completion time can be divided into two parts, i.e., the total flight time and the total hovering time. The total flight time of the k-th UAV is calculated as follow,

$$
T _ { k } ^ { f l y } = \frac { D i s t _ { k } } { V _ { k } } ,\tag{1}
$$

where $D i s t _ { k }$ represents the trajectory length of the k-th UAV and $V _ { k }$ represents the flight speed of the k-th UAV.

The hovering time of the UAV at each hovering position is determined by the amount of data that the corresponding IoT device needs to upload and the data transmission rate. In this work, a statistical wireless channel model is employed to facilitate the data transmission [42], [43], [44], [45], [46], [47]. The probability of line-of-sight (LoS) transmission between UAV k and node i is calculated as follow,

$$
P _ { \mathrm { L o S } } ^ { k , i } = \frac { 1 } { 1 + C \exp ( - D \left[ \theta _ { k , i } - C \right] ) } ,\tag{2}
$$

where $C$ and D are constants that depend on the specific propagation environment, and $\textstyle \theta _ { k , i } ~ = ~ { \frac { 1 8 0 } { \pi } } \sin ^ { - 1 } \left( { \frac { \bar { H } } { d _ { k , i } } } \right)$ is the elevation angle in degree. We denote $d _ { k , i }$ as the Euclidean distance between UAV k and node i, where $d _ { k , i } \ = \ \sqrt { ( x q _ { n } - x s _ { n } ) ^ { 2 } + ( y q _ { n } - y s _ { n } ) ^ { 2 } + H ^ { 2 } }$ . In particular, the probability of non-line-of-sight (NLoS) transmission between UAV k and node i can be obtained as $P _ { \mathrm { N L o S } } ^ { k , i } ~ =$ $1 - P _ { \mathrm { L o S } } ^ { k , i }$ . We use $L _ { \mathrm { d B } }$ to represent the average path loss for the ground-to-air data transmission, which is calculated as follow,

$$
L _ { \mathrm { d B } } = \bigg ( \frac { 4 \pi f _ { c } } { c l } \bigg ) ^ { 2 } d _ { k , i } ^ { \alpha } \left[ P _ { \mathrm { L o S } } ^ { k , i } \mu _ { \mathrm { L o S } } + P _ { \mathrm { N L o S } } ^ { k , i } \mu _ { \mathrm { N L o S } } \right] ,\tag{3}
$$

where $f _ { c }$ represents the carrier frequency and cl denotes the speed of light. We denote Î± as the path loss exponent. We denote $\mu _ { \mathrm { L o S } }$ and $\mu _ { \mathrm { N L o S } }$ as the average additional losses for LoS and NLoS connections respectively, which are two constants dependent on the specific propagation environment.

Therefore, the received signal power at UAV k from node i can be calculated as follow,

$$
P _ { k , i } = \frac { P ^ { t } } { L _ { \mathrm { d B } } \sigma ^ { 2 } } ,\tag{4}
$$

where $P ^ { t }$ is the transmit power and $\sigma ^ { 2 }$ is the noise power. Based on the Shannon formula, we denote the data

transmission rate between node i and UAV k as follow,

$$
R _ { k , i } = B { \log _ { 2 } } \left( 1 + P _ { k , i } \right) ,\tag{5}
$$

where B represents the available bandwidth. Then, the total hovering time of the k-th UAV is calculated as follow,

$$
T _ { k } ^ { h o v e r } = \sum _ { i = 1 } ^ { M } \frac { B _ { i } } { R _ { k , i } } .\tag{6}
$$

The task completion time of the k-th UAV is calculated as

$$
T _ { k } ^ { t o t a l } = T _ { k } ^ { f l y } + T _ { k } ^ { h o v e r } .\tag{7}
$$

2) Energy Consumption Model: For the k-th UAV, its energy consumption is determined by the energy consumed during flight and hovering respectively. The total amount of energy consumed during flight depends on the total flight time $T _ { k } ^ { f l j }$ and the flight power. The flight power of the k-th UAV is calculated as follow [42],

$$
\begin{array} { c l c c } { { P \left( V _ { k } \right) = P _ { 0 } \left( 1 + \frac { { 3 { V _ { k } ^ { 2 } } } } { { { U _ { t i p } ^ { 2 } } } } \right) + P _ { i } \left( \sqrt { { 1 + \frac { { V _ { k } ^ { 4 } } } { { 4 { v _ { 0 } ^ { 4 } } } } } } { - \frac { { V _ { k } ^ { 2 } } } { { 2 { v _ { 0 } ^ { 2 } } } } } \right) ^ { \frac 1 2 } } }  \\ { { + \frac { { d _ { 0 } } \rho s A { V _ { k } ^ { 3 } } } { 2 } , } } \end{array}\tag{8}
$$

where $P _ { 0 } , P _ { i } , U _ { t i p } , v _ { 0 } , d _ { 0 } , s , \rho ,$ and A represent the UAVâs constant mechanical parameters. The total energy consumption of the k-th UAV during flight is calculated as

$$
E _ { k } ^ { f l y } = P \left( V _ { k } \right) \cdot T _ { k } ^ { f l y } .\tag{9}
$$

Based on [42], when $V _ { k } = 0 , P ( 0 )$ represents the UAVâs power consumption during hovering. Thus, the total energy consumption of the k-th UAV during hovering is calculated as

$$
E _ { k } ^ { h o v e r } = P \left( 0 \right) \cdot T _ { k } ^ { h o v e r } .\tag{10}
$$

The total energy consumption of the k-th UAV during its task is calculated as

$$
E _ { k } ^ { t o t a l } = E _ { k } ^ { f l y } + E _ { k } ^ { h o v e r } .\tag{11}
$$

Note that we ignore the UAVâs acceleration and deceleration processes, since the time and energy consumed during acceleration and deceleration processes accounts for a small portion of the total time and energy consumption [36], which will not affect the algorithm design in this work.

3) Collision Avoidance Model: To accommodate practical scenarios, in this work, we assume that the minimum collisionfree distance between any two UAVs is $d _ { \mathrm { m i n } }$ . Thus, to avoid collision, the real-time positions of any two UAVs i and $j$ during either flight or hovering must satisfy

$$
\left\| q _ { i } ^ { t } - q _ { j } ^ { t } \right\| \geq d _ { \operatorname* { m i n } } , \forall i \neq j , i , j \in K ,\tag{12}
$$

where $q _ { i } ^ { t }$ and $q _ { j } ^ { t }$ represent positions of UAV i and UAV $j$ at time t, respectively.

## B. Problem Formulation

We derive the mathematical formulation of the proposed multi-objective optimization problem as follow,

$$
\left\{ \begin{array} { l l } { f _ { 1 } \left( \boldsymbol { X } \right) = \displaystyle \operatorname* { m a x } _ { k \in { K } } \left( T _ { k } ^ { t o t a l } \right) ; } \\ { f _ { 2 } \left( \boldsymbol { X } \right) = \displaystyle \operatorname* { m a x } _ { k \in { K } } \left( E _ { k } ^ { t o t a l } \right) ; } \\ { \displaystyle \operatorname* { m i n } _ { \boldsymbol { X } \in { \mathcal { X } } } F \left( \boldsymbol { X } \right) = \{ f _ { 1 } ( \boldsymbol { X } ) , f _ { 2 } ( \boldsymbol { X } ) \} ^ { T } , } \end{array} \right.\tag{13}
$$

where X represents the decision variables, including the trajectories, hovering positions and flight speeds of all UAVs. The following constraints must be satisfied.

Constraint 1: The flight speed of each UAV is limited within the range $[ V _ { \mathrm { m i n } } , V _ { \mathrm { m a x } } ]$

Constraint 2: Each IoT device must be visited by one and only one UAV.

Constraint 3: The distance between the UAVâs hovering position and the corresponding visited IoT device must be no larger than the communication range.

Constraint 4: After collecting data from a certain IoT device, the UAV immediately flies to the next hovering position, except that the current hovering position and the next hovering position coincide.

Constraint 5: Each UAV can only collect data from one device at a time.

Constraint 6: At any time t, the relative distance between any two UAVs must satisfy Eq. (12) to avoid collisions.

## IV. ALGORITHM DESIGN AND IMPLEMENTATION

The pseudocode of the proposed MSMOACO algorithm is presented in Algorithm 1. In the following, we in detail illustrate Algorithm 1 by module.

## A. Representation of Decision Variables

1) Trajectories: For each UAV, we need to decide which nodes to visit and the corresponding visiting order. Intuitively, if the nodes to be visited are determined, then optimizing the visiting order becomes a simple traveling salesman problem (TSP). However, those two subproblems are correlated, which thus cannot be optimized separately. Since all the N nodes, K start points and K destination points must be visited once, we consolidate the trajectories of all K UAVs into a single decision variable $X ^ { 1 }$ as follows.

$$
\begin{array} { r } { X ^ { 1 } = [ 1 , 2 , \dotsc , N , K S _ { 1 } , K S _ { 2 } , \dotsc , K E _ { K } ] _ { K } } \\ { \dotsc \dotsc , K S _ { K } , K E _ { 1 } , K E _ { 2 } , \dotsc , K E _ { K } ] . } \end{array}\tag{14}
$$

However, the above simple formulation does not explicitly denote the node indices and the corresponding trajectory for each UAV. Thus, we introduce the following additional constraints on $X ^ { 1 }$ to capture multi-UAV trajectories when applying $X ^ { 1 }$ to the algorithm design.

Constraint 1: The first column of $X ^ { 1 }$ must be $K S _ { 1 }$ , representing the start point of the first UAV.

Constraint 2: If the i-th column of $X ^ { 1 }$ represents the destination point $K E _ { k }$ of the k-th UAV, then the $( i + 1 )$ )-th column must be the start point $K S _ { k + 1 }$ of the (k + 1)-th UAV.

Constraint 3: Assuming the i-th column and the j-th column represent the start point and destination point of the k-th UAV respectively, then there exist no other UAVsâ start points or destination points between the i-th and j-th columns.

Algorithm 1 MSMOACO   
Input: $K S _ { k } , K E _ { k } , S N _ { n } , C _ { n } , B _ { n } , V _ { \mathrm { m i n } } , V _ { \mathrm { m a x } } ,$ where $k \in K$   
and $n \in N$   
Output: The task planning for each UAV and the Pareto   
set consisting of the maximum task completion time and the   
maximum energy consumption among all UAVs.   
1: Define the parameters: m, maxGen, $\alpha , ~ \beta , ~ \rho _ { a c o }$ and   
Q. //The specific meanings of the parameters are   
described in Section V-B.   
2: Initialize the population. //Please refer to Algorithm 2.   
3: Initialize the pheromone matrix Ï and the distance  
probability matrix Î·.   
4: Initialize the external archive to store the non-dominated   
solution set.   
5: while gen â¤ maxGen do   
6: Multi-UAV trajectory planning. //Please refer to   
Algorithm 3 and section IV-C for details.   
7: Optimize the hovering positions for data collection.   
//Please refer to section IV-D for details.   
8: Update the flight speeds of UAVs. //Please refer to   
section IV-E for details.   
9: Calculate the fitness of the population and determine   
the non-dominated ranks of the population.   
10: Save new non-dominated solutions and update the   
external archive.   
11: endwhile   
12: Applying the geometry-based collision avoidance strategy   
to adjust the trajectory of each UAV. //Please refer to   
section IV-F for details.

Constraint 4: The last column of $X ^ { 1 }$ must be $K E _ { K }$ representing the destination point of the last UAV.

2) Hovering Positions: The UAVs are dispatched to collect data from N IoT devices. Although UAVs must hover during the data collection, they do not need to hover directly above each IoT device. Instead, it is sufficient for the UAV to hover within the communication range of each node during data collection. Thus, we use the decision variable $X ^ { 2 }$ to represent the hovering positions of all UAVs as follow,

$$
X ^ { 2 } = { \left[ \begin{array} { l } { Q _ { 1 } } \\ { Q _ { 2 } } \\ { \vdots } \\ { Q _ { N } } \end{array} \right] } = { \left[ \begin{array} { l } { x q _ { 1 } , y q _ { 1 } , H } \\ { x q _ { 2 } , y q _ { 2 } , H } \\ { \vdots } \\ { x q _ { N } , y q _ { N } , H } \end{array} \right] } ,\tag{15}
$$

where each row of $X ^ { 2 }$ represents the coordinate of a hovering position of the UAV within a specific visited nodeâs communication range. Note that each row of $X ^ { 2 }$ must satisfy Constraint 3 defined in Section III-B.

3) Flight Speeds: The flight speed of each UAV significantly impacts both the task completion time and energy consumption. Therefore, it is worth investigating whether each UAV should change the flight speed over time or keep the flight speed constant during the task. We first give the following proposition.

<!-- image-->  
Fig. 2. A proof example of maintaining a constant flight speed.

Proposition 1: For each of the dispatched UAVs, to simultaneously minimize its task completion time and energy consumption, it is necessary to maintain a constant flight speed during the task.

Proof: We first consider a scenario shown in Fig. 2, where a UAV sequentially visits the three hovering positions A, B and C, along the two trajectories AB and BC. We assume that the length of AB is $D _ { 1 }$ and the UAVâs flight speed over AB is $V _ { 1 }$ . Similarly, the length of BC is $D _ { 2 }$ and the UAVâs flight speed over BC is $V _ { 2 }$ . Then, without considering the hovering time (i.e., the data collection time), the UAVâs task completion time and energy consumption are calculated in Eq. (16).

$$
\left\{ \begin{array} { l l } { \displaystyle T _ { 1 2 } = \frac { D _ { 1 } } { V _ { 1 } } + \frac { D _ { 2 } } { V _ { 2 } } ; } \\ { \displaystyle E _ { 1 2 } = P \left( V _ { 1 } \right) \cdot \frac { D _ { 1 } } { V _ { 1 } } + P \left( V _ { 2 } \right) \cdot \frac { D _ { 2 } } { V _ { 2 } } . } \end{array} \right.\tag{16}
$$

Since $D _ { 1 }$ and $D _ { 2 }$ are fixed, the energy consumption of the UAV is inherently related to $\frac { P ( V _ { 1 } ) } { V _ { 1 } }$ and $\frac { P ( V _ { 2 } ) } { V _ { 2 } }$ . We start to prove by considering the following four scenarios. If the UAV uses the same flight speed $V _ { 1 }$ over both AB and BC, the task completion time and energy consumption can be expressed as Eq. (17). Similarly, if the UAV uses the same flight speed $V _ { 2 }$ over both AB and BC, the task completion time and energy consumption can be expressed as Eq. (18).

$$
\begin{array} { l } { \displaystyle \left\{ \begin{array} { l } { \displaystyle T _ { 1 1 } = \frac { D _ { 1 } } { V _ { 1 } } + \frac { D _ { 2 } } { V _ { 1 } } ; } \\ { \displaystyle E _ { 1 1 } = D _ { 1 } \cdot \frac { P \left( V _ { 1 } \right) } { V _ { 1 } } + D _ { 2 } \cdot \frac { P \left( V _ { 1 } \right) } { V _ { 1 } } . } \end{array} \right. } \\ { \displaystyle \left\{ \begin{array} { l } { \displaystyle T _ { 2 2 } = \frac { D _ { 1 } } { V _ { 2 } } + \frac { D _ { 2 } } { V _ { 2 } } ; } \\ { \displaystyle E _ { 2 2 } = D _ { 1 } \cdot \frac { P \left( V _ { 2 } \right) } { V _ { 2 } } + D _ { 2 } \cdot \frac { P \left( V _ { 2 } \right) } { V _ { 2 } } . } \end{array} \right. } \end{array}\tag{17}
$$

(18)

Scenario 1: $V _ { 1 } < V _ { 2 }$ and $\frac { P ( V _ { 1 } ) } { V _ { 1 } } ~ < ~ \frac { P ( V _ { 2 } ) } { V _ { 2 } }$ . By comparing Eq. (17) and Eq. (18), we can conclude that $T _ { 1 1 } > T _ { 1 2 } , E _ { 1 1 } <$ $E _ { 1 2 }$ and $T _ { 2 2 } < T _ { 1 2 } , E _ { 2 2 } > E _ { 1 2 }$ , which is shown in Fig. 3(a). Scenario 2: $V _ { 1 } < V _ { 2 }$ and $\frac { \tilde { P ( V _ { 1 } ) } } { V _ { 1 } } ~ > ~ \frac { P ( V _ { 2 } ) } { V _ { 2 } }$ . By comparing Eq. (17) and Eq. (18), we can conclude that $T _ { 1 1 } > T _ { 1 2 } , E _ { 1 1 } >$ $E _ { 1 2 }$ and $T _ { 2 2 } < T _ { 1 2 } , E _ { 2 2 } < E _ { 1 2 } ,$ , which is shown in Fig. 3(b). Scenario 3: $V _ { 1 } > V _ { 2 }$ and ${ \frac { \mathbf { \tilde { { P } } } ( V _ { 1 } ) } { V _ { 1 } } } ~ > ~ { \frac { { P ( V _ { 2 } ) } } { V _ { 2 } } }$ . By comparing Eq. (17) and Eq. (18), we can conclude that $T _ { 1 1 } < T _ { 1 2 } , E _ { 1 1 } >$ $E _ { 1 2 }$ and $T _ { 2 2 } > T _ { 1 2 } , E _ { 2 2 } < E _ { 1 2 } ,$ , which is shown in Fig. 3(c). Scenario 4: $V _ { 1 } > V _ { 2 }$ and $\frac { \mathop { \bf \ddot { P } } ( V _ { 1 } ) } { V _ { 1 } } ~ < ~ \frac { \mathop { P } ( V _ { 2 } ) } { V _ { 2 } }$ . By comparing Eq. (17) and Eq. (18), we can conclude that $T _ { 1 1 } < T _ { 1 2 } , E _ { 1 1 } <$ $E _ { 1 2 }$ and $T _ { 2 2 } > T _ { 1 2 } , E _ { 2 2 } > E _ { 1 2 }$ , which is shown in Fig. 3(d).

Based on the above analysis, particularly in Scenarios 2 and 4, we find that maintaining the same flight speed over both AB and BC yields better solutions (i.e., both of the task completion time and energy consumption are minimized), compared with strategies of using different flight speeds. For Scenarios 1 and 3, although the minimized task completion time and energy consumption can not be simultaneously achieved by using the same flight speed $( V _ { 1 }$ or $V _ { 2 } )$ over both $A B$ and $B C ,$ , we can prove that there exists a flight speed $V$ where min $( V _ { 1 } , V _ { 2 } ) \leq V \leq \operatorname* { m a x } ( V _ { 1 } , V _ { 2 } )$ such that maintaining flight speed V over both AB and BC results in the shorter task completion time and lower energy consumption at the same time, compared with strategies of using different flight speeds. The proof is illustrated as follows.

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
ï¼cï¼

<!-- image-->  
(d)  
Fig. 3. A UAVâs task completion time and energy consumption in different flight speed scenarios.

First, we prove that points $( T _ { 1 1 } , E _ { 1 1 } ) , ~ ( T _ { 1 2 } , E _ { 1 2 } )$ and $\left( T _ { 2 2 } , E _ { 2 2 } \right)$ are collinear in Scenarios 1 and 3. For points $( T _ { 1 1 } , E _ { 1 1 } )$ and $\left( { { T _ { 1 2 } } , { E _ { 1 2 } } } \right)$ , the absolute value of the slope of the line connecting these two points is calculated using Eq. (19), as shown at the bottom of the page. Similarly, the absolute value of the slope of the line connecting points $\left( { { T _ { 1 2 } } , { E _ { 1 2 } } } \right)$ and $\left( T _ { 2 2 } , E _ { 2 2 } \right)$ is calculated using Eq. (20), as shown at the bottom of the page. Based on Eq. (19) and Eq. (20), it is clear that $K _ { 1 1 - 1 2 } ~ = ~ K _ { 2 2 - 1 2 }$ , implying that the three points $( T _ { 1 1 } , E _ { 1 1 } ) , \ ( T _ { 1 2 } , E _ { 1 2 } )$ and $\left( T _ { 2 2 } , E _ { 2 2 } \right)$ are collinear.

Next, we demonstrate that the energy consumption function with respect to the task completion time is concave. If so, then in Fig. 3(a) and Fig. 3(c), there must exist a flight speed $V ,$ where min $( V _ { 1 } , V _ { 2 } ) \leq V \leq \operatorname* { m a x } ( V _ { 1 } , V _ { 2 } )$ , such that the task completion time and energy consumption are smaller than $T _ { 1 2 }$ and $E _ { 1 2 }$ respectively. The proof is illustrated as follows.

Based on Eq. (16), we reconstruct the task completion time and energy consumption functions with the decision variable V in Eq. (21), where min $( V _ { 1 } , V _ { 2 } ) \leq V \leq \operatorname* { m a x } ( V _ { 1 } , V _ { 2 } )$

$$
\left\{ \begin{array} { l l } { \displaystyle T = \frac { D _ { 1 } } { V } + \frac { D _ { 2 } } { V } = \frac { \left( D _ { 1 } + D _ { 2 } \right) } { V } ; } \\ { \displaystyle E = D _ { 1 } \cdot \frac { P \left( V \right) } { V } + D _ { 2 } \cdot \frac { P \left( V \right) } { V } = \frac { \left( D _ { 1 } + D _ { 2 } \right) \cdot P \left( V \right) } { V } . } \end{array} \right.\tag{21}
$$

By taking the second derivative of the function E with respect to $T ,$ we obtain $\begin{array} { r } { \frac { \partial ^ { 2 } E } { \partial T ^ { 2 } } \ = \ \frac { V ^ { 3 } \cdot P ^ { \prime \prime } ( V ) } { D _ { 1 } + D _ { 2 } } } \end{array}$ , where $P ^ { \prime \prime } \left( V \right)$ represents the second derivative of $\operatorname { E q . } \ ( 8 )$ with respect to $V .$ Since the flight power-speed function is concave with respect to the flight speed, we have $P ^ { \prime \prime } \left( V \right) > 0$ . Also, considering that $D _ { 1 } { + } D _ { 2 } > 0$ and $V > 0$ , we have $\frac { \partial ^ { 2 } E } { \partial T ^ { 2 } } > 0$ . Thus, we conclude that it is always better for a UAV to maintain a constant flight speed during the task, for simultaneously minimizing its time and energy consumption.

Proposition 2: To simultaneously minimize the maximum task completion time and maximum energy consumption among all UAVs, it is sufficient for all UAVs to maintain the same constant flight speed during the task.

Proof: We consider a two-UAV task scenario where those two UAVs have different flight trajectories. We first consider the case when two UAVs use the same constant flight speed V and let V ranges from 0.1m/s to 40m/s with the sampling interval of 0.5. The corresponding solution set regarding the trade-off between the maximum task completion time and maximum energy consumption is illustrated by the red points in Fig. 4(c). Then, we consider the case when two UAVs use two different constant flight speeds $V _ { 1 }$ and $V _ { 2 } .$ . Let $V _ { 1 }$ and $V _ { 2 }$ independently range from 0.1m/s to 40m/s with the sampling interval of 0.5 and we can obtain totally 6400 different flight speed combinations. The corresponding solution set regarding the trade-off between the maximum task completion time and maximum energy consumption is illustrated by the blue points in Fig. 4(c). Based on Fig. 4(d), we find that the Pareto fronts of the time-energy trade-off under two different speed settings coincide, which implies that the solution set achieved when two UAVs use the same constant flight speed is the nondominated solution set.

Based on the above analysis, we can represent the flight speeds of all UAVs as the third decision variable $X ^ { 3 }$

$$
X ^ { 3 } = [ V _ { 1 } , V _ { 2 } , \ldots , V _ { K } ] = V .\tag{22}
$$

Thus, the decision variables determining UAVsâ task completion time and energy consumption are defined in Eq. (23).

$$
X = [ X ^ { 1 } , X ^ { 2 } , X ^ { 3 } ] .\tag{23}
$$

$$
K _ { 1 1 - 1 2 } = \left\| \frac { E _ { 1 1 } - E _ { 1 2 } } { T _ { 1 1 } - T _ { 1 2 } } \right\| = \left\| \frac { \left( D _ { 1 } \cdot \frac { P ( V _ { 1 } ) } { V _ { 1 } } + D _ { 2 } \cdot \frac { P ( V _ { 1 } ) } { V _ { 1 } } \right) - \left( D _ { 1 } \cdot \frac { P ( V _ { 1 } ) } { V _ { 1 } } + D _ { 2 } \cdot \frac { P ( V _ { 2 } ) } { V _ { 2 } } \right) } { \left( \frac { D _ { 1 } } { V _ { 1 } } + \frac { D _ { 2 } } { V _ { 1 } } \right) - \left( \frac { D _ { 1 } } { V _ { 1 } } + \frac { D _ { 2 } } { V _ { 2 } } \right) } \right\| = \left\| \frac { V _ { 2 } P \left( V _ { 1 } \right) - V _ { 1 } P \left( V _ { 2 } \right) } { V _ { 2 } - V _ { 1 } } \right\| .\tag{19}
$$

$$
K _ { 2 2 - 1 2 } = \left\| \frac { E _ { 2 2 } - E _ { 1 2 } } { T _ { 2 2 } - T _ { 1 2 } } \right\| = \left\| \frac { \left( D _ { 1 } \cdot \frac { P ( V _ { 2 } ) } { V _ { 2 } } + D _ { 2 } \cdot \frac { P ( V _ { 2 } ) } { V _ { 2 } } \right) - \left( D _ { 1 } \cdot \frac { P ( V _ { 1 } ) } { V _ { 1 } } + D _ { 2 } \cdot \frac { P ( V _ { 2 } ) } { V _ { 2 } } \right) } { \left( \frac { D _ { 1 } } { V _ { 2 } } + \frac { D _ { 2 } } { V _ { 2 } } \right) - \left( \frac { D _ { 1 } } { V _ { 1 } } + \frac { D _ { 2 } } { V _ { 2 } } \right) } \right\| = \left\| \frac { V _ { 1 } P \left( V _ { 2 } \right) - V _ { 2 } P \left( V _ { 1 } \right) } { V _ { 1 } - V _ { 2 } } \right\| .\tag{20}
$$

<!-- image-->  
(@)

<!-- image-->  
(b)

<!-- image-->  
(cï¼

<!-- image-->  
(d)

Fig. 4. The tradeoff between the maximum task completion time and the maximum energy consumption under two different speed settings.  
Algorithm 2 Population Initialization   
Input: m (number of Population)   
Output: Population   
1: for i=1:m do   
2: Assign the coordinates of the N nodes to $X ^ { 2 }$   
3: $X ^ { 3 } = V _ { \mathrm { m i n } } \ +$ rand $( ) \ast ( V _ { \mathrm { m a x } } \ : - \ : V _ { \mathrm { m i n } } )$ .//Randomly   
initialize the flight speeds of UAVs.   
4: Population $\mathrm { ( i ) } { < } { - } [ X ^ { \overline { { 2 } } } , X ^ { \overline { { 3 } } } ]$ . //Store the initialized deci  
sion variables in the population.   
5: endfor

## B. Population Initialization

The population initialization is developed to generate a set of initial solutions, based on which we start to search the optimal solution. In this work, we need to initialize the population for the decision variables $X ~ = ~ [ X ^ { 1 } , X ^ { 2 } , X ^ { 3 } ]$ Specifically, since $X ^ { 1 }$ is optimized using an improved ant colony algorithm, which does not require initialization as the ant colony algorithm does not need population initialization. For $X ^ { 2 }$ , it is initialized by assigning the coordinates of IoT devices, resulting in the initial hovering positions being directly above the nodes with the same altitude H. For $X ^ { 3 } ,$ it is randomly initialized within the range of flight speed. The specific initialization procedure is shown in Algorithm 2.

## C. Multi-UAV Trajectory Planning

The ant colony optimization algorithm (ACO) is widely applied to solve combinatorial optimization problems. In this work, we aim to improve and perfect the ACO algorithm to enable the multi-trajectory planning for multi-UAV cooperative scheduling. To accommodate the decision variable $X ^ { 1 }$ introduced in Section IV-A, we develop the ACO algorithm with constraints, which is presented in Algorithm 3. In particular, constraints are included in lines 3, 5, 6 and 13 of Algorithm 3. Moreover, since we are dealing with a multi-objective optimization problem, the fitness evaluation yields two scores, i.e., the task completion time and energy consumption. When updating the pheromone matrix, guidance based on only one score is insufficient. To address this issue, the fitness is subjected to non-dominated [48] sorting and the pheromone matrix is updated according to the individualâs non-dominated rank (line 19 of Algorithm 3).

Due to the high sensitivity of ACO algorithms to interposition distances, the introduction of constraints may render some distance relationships ineffective, resulting in the premature convergence and susceptibility to local optima. To address this concern, we devise a fitness-guided mutation strategy, which employs Eq. (24) to select UAVs with the highest and lowest energy consumption, or the maximum and minimum task completion time, among all K UAVs, where rand() denotes a random number generator. Based on the selected UAVs that achieve the maximum and minimum values for a particular objective, a mutation process is applied.

Algorithm 3 Constrained ACO for Multi-UAV Trajectory   
Planning   
Input: Parameters required by ACO   
Output: Population   
1: The Route matrix is initialized to store and record the   
generated trajectories, which satisfy the constraints of   
${ \bar { X } } ^ { 1 }$   
2: for i=1:m do   
3: Define the start point of the i-th ant as $K S _ { 1 }$ and save   
it to update the Route.   
4: for $\mathrm { j } { = } 2 { : } \mathrm { N } { + } 2 \mathrm { K } { - } 1$ do //Iterate to select the next node to   
visit   
5: if The previous visited node is the destination point   
of the k-th UAV then   
6: The next node to be visited is the start point   
of the (k + 1)-th UAV.   
7: else   
8: Calculate the selection probabilities of nodes   
within the allowed choice list (excluding   
nodes that violate Constraint 3)   
9: Normalize the probabilities and use a roulette   
wheel selection to choose the next visited   
node.   
10: endif   
11: Record the calculated next visited node in Route.   
12: endfor   
13: Define the end path of the i-th ant as KEK and save   
it in the updated Route.   
14: endfor   
15: Store Route in Population.   
16: Calculate the fitness and non-dominance level of the   
Population.   
17: Apply the proposed fitness-guided mutation strategy to   
mutate the trajectories   
18: Calculate the fitness and non-dominance level of the   
population after mutation   
19: Update the pheromone matrix based on the non  
dominance ranks of solutions in the population.

<!-- image-->  
Fig. 5. Illustration of the fitness-guided mutation strategy for multi-UAV trajectory planning.

( Select based on energy consumption, rand $( ) > 0 . 5 ;$ Select based on task completion time, otherwise.

(24)

Considering the goal in this work, balancing the task completion time and energy consumption among all dispatched UAVs are of equal importance. Favoring either one of the two objectives could lead to the sub-optimal solution to the Pareto set. Thus, we set the value in Eq. (24) to 0.5.

Trajectory Mutation Example: For example in Fig. 5(a), assuming that UAV $k _ { 1 }$ achieves the minimum value on a certain objective and UAV $k _ { 2 }$ achieves the maximum value on the same objective accordingly. For UAV $k _ { 1 }$ in Fig. 5(b), we first calculate the distances from other nodes (i.e., the nodes that are not visited by UAV $k _ { 1 } )$ to the trajectory of UAV $k _ { 1 }$ . Then, we use a roulette wheel selection mechanism to choose the closest node and incorporate it into the trajectory of UAV $k _ { 1 }$ . For UAV $k _ { 2 }$ in Fig. 5(c), we calculate the distances from each of the nodes visited by UAV $k _ { 2 }$ to trajectories of other two UAVs. Similarly, we use a roulette wheel selection mechanism to choose the node that is closest to other two trajectories and UAV $k _ { 2 }$ will abandon visiting that node, allowing other UAVs to visit it.

## D. Optimizing Hovering Positions

According to Eq. (5), the data transmission rate is influenced by the distance between the hovering position and the target node, which further affects the task completion time and energy consumption. For example in Fig. 6, the UAV flies from $Q _ { A }$ to $Q _ { O }$ , hover at $Q _ { O }$ while collecting data from node $S N _ { O }$ , and then flies to $Q _ { C }$ (the red route). It is clear that if the UAV follows the black route (i.e., $Q _ { A } \to S N _ { O } \to Q _ { C } )$ the trajectory becomes longer, resulting in the longer flight time and larger flight energy consumption with the same flight speed. However, the UAV can achieve the higher data transmission rate when hovering at $S N _ { O }$ , leading to the shorter hovering time and smaller hovering energy consumption for collecting the same amount of data. If the reduction in flight time and flight energy consumption by following the red trajectory outweighs the corresponding increase in time and energy consumption during hovering, then the red trajectory is considered superior. Thus, it is necessary and significant to optimize the hovering position for each visited IoT device to obtain improved solutions.

<!-- image-->

Fig. 6. Different hovering positions and corresponding trajectories.  
<!-- image-->  
Fig. 7. The adaptive hovering strategy at two different iteration stages.

In this work, we develop an adaptive hovering strategy to iteratively search the optimal hovering position for each visited node. Specifically, during the first half of the iteration process, we concentrate the search space within the shaded region shown in Fig. 7(a). During the remaining iterations, we conduct the local search within the vicinity of the candidate optimal hovering position found in early iterations, which is illustrated in Fig. 7(b). For node $S N _ { O }$ , its corresponding hovering position for data collection is updated as follows.

$$
\begin{array} { r } { Q _ { O } ^ { t + 1 } = \left\{ \begin{array} { l l } { S N _ { O } + \left( R \cdot R 1 \cdot \overrightarrow { O A } + R \cdot R 2 \cdot \overrightarrow { O C } \right) , } \\ { \qquad \operatorname { r a n d } ( ) > \mathrm { a d a p t e r } ; } \\ { Q _ { O } ^ { t } + R 3 \cdot \overrightarrow { E _ { O } } , } \end{array} \right. } \end{array}\tag{25}
$$

where $\overrightarrow { O A }$ and $\overrightarrow { O C }$ represent unit vectors of $\overrightarrow { Q _ { O } Q _ { A } }$ and $\overrightarrow { Q _ { O } Q _ { C } }$ respectively; R is the projected communication range of node $S N _ { O } ;$ ; R1, R2 and R3 are random numbers; $Q _ { O } ^ { t }$ represents the updated hovering position at the t-th iteration; $\overrightarrow { E _ { O } }$ represents a unit vector in any direction; adapter $= \frac { t } { m a x T }$ is an adaptive variable used to regulate the update of hovering positions; t and maxT denote the current number of iterations and the maximum number of iterations respectively. Note that if the distance between the updated hovering position $Q _ { O } ^ { t + 1 }$ and node $S N _ { O }$ exceeds R or if the fitness of the updated hovering position $Q _ { O } ^ { t + 1 }$ gets worse, then the hovering position is not updated.

## E. Optimizing Flight Speed

Intuitively, increasing the UAVâs flight speed results in the reduced task completion time, which however may increase the $\mathrm { U A V } _ { \mathrm { \Delta } }$ flight energy consumption. Thus in this work, we need to carefully investigate the impact of flight speed on both the task completion time and flight energy consumption. Inspired by heuristic algorithms, we develop the updating function of the UAVâs flight speed as follows,

$$
\begin{array} { r l } & { V ^ { t + 1 } = V ^ { t } + R 4 \cdot \left( V ^ { b e s t } - V ^ { t } \right) } \\ & { ~ + R 5 \cdot \left( 1 - \mathrm { a d a p t e r } \right) \cdot \left( V _ { \mathrm { m a x } } - V _ { \mathrm { m i n } } \right) , } \end{array}\tag{26}
$$

where R4 and R5 are random numbers; $V ^ { b e s t }$ represents the flight speed of any solution in the non-dominated archive; $R \hat { 4 } \cdot \left( \hat { V } ^ { b e s t } - V ^ { t } \right)$ is used to guide the population towards the optimal solution; $R 5 \cdot ( 1 - \mathrm { a d a p t e r } ) \cdot ( V _ { \mathrm { m a x } } - V _ { \mathrm { m i n } } )$ is employed to avoid getting trapped in local optima by introducing random perturbations.

## F. Geometry-Based Collision Avoidance Strategy

To avoid collisions among UAVs whenever they fly or hover, we develop a geometry-based collision avoidance strategy in this work. The developed strategy addresses two main scenarios: 1) collisions between in-flight UAVs; 2) collisions between in-flight UAVs and in-hover UAVs.

We first assume that when $t \ = \ 0 ,$ , all UAVs start to execute their tasks simultaneously by following Algorithm 1 without considering the developed collision avoidance strategy. As time goes on, the real-time position of each UAV is recorded at intervals of $\Delta t .$ , which is calculated as follow,

$$
\Delta t = { \frac { d _ { \operatorname* { m i n } } } { 2 V } } ,\tag{27}
$$

where V represents the UAVâs flight speed. Thus, we can guarantee that any potential collision (i.e., the distance between two UAVs is no larger than $d _ { \mathrm { m i n } } )$ between any two UAVs can be captured by employing the recording interval defined in Eq. (27), since the relative distance between two UAVs can be reduced by at most $d _ { \mathrm { m i n } }$ during ât. In the following, we in detail illustrate how multiple UAVs adjust their flight trajectories once a potential collision is detected.

Collision Avoidance Example: Assuming that at recording time $t = T ,$ , the distance between UAVs is detected to be less than or equal to $d _ { \mathrm { m i n } } ,$ we identify the most recent recording time $t = T ^ { \prime }$ when the distance between UAVs is larger than or equal to $d _ { \mathrm { m i n } } .$ . For example in Fig. 8(a), UAV i flies along the black trajectory while UAV j hovers at the blue point for data collection. If UAV i continues flying along its original trajectory, a collision would be inevitable. Therefore, based on the proposed geometry-based collision avoidance strategy, at time $t = T ^ { \prime }$ , UAV i changes its flight trajectory to avoid collision. The updated flight trajectory of UAV i is shown in Fig. 8(a). For two in-flight UAVs i and j that may collide with each other shown in Fig. 8(b), at time $t = T ^ { \prime } .$ UAV i changes its flight trajectory by flying towards the real-time position of UAV j, while UAV j continues flying along its original flight trajectory. In the case of potential simultaneous collision among three UAVs shown in Fig. 8(c), at time $t = T ^ { \prime }$ , UAV i changes its flight trajectory by flying towards the real-time position of UAV j, UAV j changes its flight trajectory by flying towards the real-time position of UAV k, and UAV k continues flying along its original flight trajectory. In the case of potential successive collision among three UAVs shown in Fig. 8(d), UAV i changes its flight trajectory by flying towards the real-time position of UAV j at time $t \ = \ T ^ { \prime }$ . UAV j continues flying along its original flight trajectory until time $t = t ^ { \prime \prime }$ and then changes to fly towards the real-time position of UAV k. UAV k always flies along its original flight trajectory. In general, for the case when more than three UAVs have the possibility of collision, following a counterclockwise order, each UAV changes its original flight trajectory by flying along a new polygonal flight trajectory except that the last UAV maintains its original flight trajectory.

<!-- image-->  
Fig. 8. Geometry-based collision avoidance in four scenarios: (a) an in-flight UAV and an in-hover UAV; (b) two in-flight UAVs; (c) three in-flight UAVs that may collide with each other simultaneously; (d) three in-flight UAVs that may collide with each other successively.

## G. Computational Complexity Analysis

Firstly, we analyze the computational complexity of MSMOACO without considering the collision avoidance. We develop a constrained ACO to optimize the trajectories of K UAVs, which has the computational complexity of $O \left( m N + N ^ { 2 } \right)$ , where m is the number of used ants. The computational complexity of the fitness-guided mutation strategy mainly lies in calculating the shortest distances from nodes to trajectories. Since there are at most N nodes, the computational complexity is $O \left( N ^ { 2 } \right)$ . The computational complexity of updating the UAVsâ hovering positions using Eq. (25) is $O \left( N \right)$ . Updating the UAVsâ flight speeds by Eq. (26) has the computational complexity of $O \left( 1 \right)$ . Finally, the computational complexity of calculating the non-dominated level of the solution set and managing external archives is $O \left( o b j \cdot m ^ { 2 } \right)$ , where obj = 2 is the number of objectives. Thus, the overall computational complexity of the first part is $O \left( m a x I t e r \cdot ( m N ^ { ^ { - } } + N ^ { 2 } + 2 m ^ { 2 } ) \right)$ , where maxIter is the maximum number of iterations.

TABLE I  
THE UAVâS SYSTEM PARAMETER ASSIGNMENT
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>Flightaltitude of the UAV</td><td rowspan=1 colspan=1>100m</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P ^ { t } } }$ </td><td rowspan=1 colspan=1>Transmission power of each node</td><td rowspan=1 colspan=1>0.1W</td></tr><tr><td rowspan=1 colspan=1> $\overline { { { \delta } ^ { 2 } } }$ </td><td rowspan=1 colspan=1>Noise power</td><td rowspan=1 colspan=1>-110dBm</td></tr><tr><td rowspan=1 colspan=1>P0</td><td rowspan=1 colspan=1>Channel power gainat d =1m</td><td rowspan=1 colspan=1>-60dB</td></tr><tr><td rowspan=1 colspan=1> $\overline { { V _ { \mathrm { m a x } } } }$ </td><td rowspan=1 colspan=1>Maximum UAV speed</td><td rowspan=1 colspan=1>40m/s</td></tr><tr><td rowspan=1 colspan=1> $V _ { \mathrm { m i n } }$ </td><td rowspan=1 colspan=1>Minimum UAV speed</td><td rowspan=1 colspan=1>0.1m/s</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B _ { i } } }$ </td><td rowspan=1 colspan=1>Data volume of each node</td><td rowspan=1 colspan=1>[100,500]Mbits</td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Aircraft weightinNewton</td><td rowspan=1 colspan=1>0.02kg</td></tr><tr><td rowspan=1 colspan=1>p</td><td rowspan=1 colspan=1>Air density</td><td rowspan=1 colspan=1>1.225kg/m3</td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Rotorradiusin meter</td><td rowspan=1 colspan=1>0.4m</td></tr><tr><td rowspan=1 colspan=1> $A$ </td><td rowspan=1 colspan=1>Rotor disc area, $A \triangleq \pi R ^ { 2 }$ </td><td rowspan=1 colspan=1>0.503mÂ²</td></tr><tr><td rowspan=1 colspan=1>Î©</td><td rowspan=1 colspan=1>Blade angular velocity in radians/second</td><td rowspan=1 colspan=1>300</td></tr><tr><td rowspan=1 colspan=1> $U _ { t i p }$ </td><td rowspan=1 colspan=1>Tip speed of the rotor blade, ${ U _ { t i p } } \triangleq \Omega R$ </td><td rowspan=1 colspan=1>120m/s</td></tr><tr><td rowspan=1 colspan=1> $\underline b$ </td><td rowspan=1 colspan=1>Numberof blades</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>Blade oraerofoil chord length</td><td rowspan=1 colspan=1>0.0157m</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Rotor solidity defined as the ratioof the total blade area $b \cdot c \cdot R$ to the disc area $\begin{array} { l l } { A , { \mathrm { i . e . , ~ } } s \triangleq { \frac { b c } { \pi R } } } \end{array}$ </td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1> $\overline { { S _ { F P } } }$ </td><td rowspan=1 colspan=1>Fuselage equivalent plate area</td><td rowspan=1 colspan=1>0.0151mÂ²</td></tr><tr><td rowspan=1 colspan=1> $\kappa$ </td><td rowspan=1 colspan=1>Incremental correction factor toinduced power</td><td rowspan=1 colspan=1>0.1</td></tr><tr><td rowspan=1 colspan=1> $v _ { 0 }$ </td><td rowspan=1 colspan=1>Mean rotor induced velocity in hover,where $\begin{array} { r } { v _ { 0 } = \sqrt { \frac { W } { 2 \rho A } } } \end{array}$ </td><td rowspan=1 colspan=1>4.03m/s</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Profile dragcoefficient</td><td rowspan=1 colspan=1>0.012</td></tr><tr><td rowspan=1 colspan=1> $C$ </td><td rowspan=1 colspan=1>Constant value</td><td rowspan=1 colspan=1>11.95</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>Constant value</td><td rowspan=1 colspan=1>0.14</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Transmission bandwidth</td><td rowspan=1 colspan=1>2MHz</td></tr><tr><td rowspan=1 colspan=1> $\mu _ { \mathrm { L o S } }$ </td><td rowspan=1 colspan=1>Additional path loss forLoSconnection</td><td rowspan=1 colspan=1>3dB</td></tr><tr><td rowspan=1 colspan=1> $\underline { { \mu _ { \mathrm { N L o S } } } }$ </td><td rowspan=1 colspan=1>Additional path loss for NLoS connection</td><td rowspan=1 colspan=1>23dB</td></tr><tr><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>The noise power</td><td rowspan=1 colspan=1>50m</td></tr><tr><td rowspan=1 colspan=1> $c l$ </td><td rowspan=1 colspan=1>The speed of light</td><td rowspan=1 colspan=1> $\overline { { { 3 . 0 * 1 0 ^ { 8 } \mathrm { m } } / { \mathrm { s } } } }$ </td></tr></table>

The second part involves running the geometry-based collision avoidance strategy. Assuming that the maximum flight trajectory length among all UAVs is maxlen and thus the running time of the strategy is $\frac { m a x l e n } { \Delta t }$ . At each time of $\Delta t ,$ we need to calculate the distance between any two of the dispatched UAVs, which has the computational complexity of $O \left( K ^ { 2 } \right)$ . In addition, at each time of ât, certain operations may be conducted to adjust UAVsâ trajectories to avoid potential collisions, which have the computational complexity of O (1). Thus, the overall computational complexity of the second part is $\begin{array} { r } { O \left( \frac { m a x l e n } { \Delta t } K ^ { 2 } \right) } \end{array}$

## V. PERFORMANCE EVALUATION

We consider random distribution of IoT devices within a given area of 4000mÃ4000m. Each UAVâs flight altitude is fixed as 100m. The communication range of each IoT device is randomly set within [50m, 100m]. The UAVâs system parameter assignment is shown in Table I. The population size is set to 100 and the maximum number of iterations is set to 100. To accommodate practical scenarios and prove the applicability of the proposed algorithm, we consider the following three different network scenarios based on an extensive investigation of existing works on UAV-enabled data collection networks: 1) Each UAVâs start point and destination point are two different points [22], [27]; 2) Each UAVâs start point is also its destination point [23]; 3) Each UAV departs from the same start point and returns to that start point [16], [40], [49].

<!-- image-->  
Fig. 9. HV defined in a two-dimensional space.

## A. Hypervolume (HV)-Performance Metric in Multi-Objective Optimization

HV is widely used for evaluating multi-objective optimization algorithms [50], which quantifies the quality of non-dominated solutions by measuring the volume they dominate in the objective space. It provides a comprehensive assessment of an algorithmâs exploration of the solution space and the corresponding Pareto frontâs coverage. Fig. 9 shows how HV is defined in a two-dimensional space, where the shaded area represents the HV for a set of Pareto solutions. Specifically, $Z ^ { \ast }$ denotes the reference point, which is chosen as the maximum values of objectives among all Pareto solutions. HV is calculated as follow,

$$
\begin{array} { r } { H V = \delta \left( \bigcup _ { i = 1 } ^ { | S | } v _ { i } \right) , } \end{array}\tag{28}
$$

where $\delta$ represents the Lebesgue measure, which is used to measure the volume, |S| denotes the number of non-dominated solutions, $v _ { i }$ depicts the hypervolume formed by the reference point and the i-th non-dominated solution. In this work, the higher value of HV indicates the better performance of the designed algorithm.

## B. Sensitivity Analysis of ACO-Related Main Parameters

As introduced in Section IV-C, UAVsâ trajectories are generated by the improved ACO algorithm, which relies on several key parameters, mainly including Î± representing the importance of pheromone and $\beta$ representing the importance of the heuristic factor. Also, the designed algorithm involves parameters such as $\rho _ { a c o }$ denoting the pheromone evaporation rate and $Q$ denoting the pheromone constant. Due to the introduction of additional constraints in this work, it may cause the designed algorithm to get trapped in local optima by simply concentrating on optimizing the shortest distance. Therefore, it is crucial to balance the values of Î± and $\beta .$ In this work, sensitivity analysis is conducted to determine appropriate values of these two parameters. In addition, for parameters $\rho _ { a c o }$ and $Q ,$ which have relatively weak impacts on the performance of the designed algorithm, we set them to 0.5 and 1 respectively.

We conduct extensive experiments to investigate the impact of $\alpha$ and $\beta$ on the performance of the designed algorithm. Specifically, we vary these two parameters from 0 to 5 with an interval of 0.5. For each pair of Î± and $\beta$ we independently run 20 experiments and average the HV results for evaluation. The color intensity in Fig. 10 reflects the degree of influence of parameter values on the designed algorithmâs performance.

<!-- image-->  
Fig. 10. Parameter sensitivity analysis.

Scenario 1  
<!-- image-->  
Scenario 2

<!-- image-->  
Scenario 3

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(cï¼  
Fig. 11. Optimized multi-UAV trajectories by MSMOACO in Scenarios 1-3.

Darker colors indicate better effects of the corresponding parameter values on the designed algorithmâs performance. Based on Fig. 10, we observe variations in the impact of Î± and $\beta$ on the designed algorithmâs performance across different network scenarios. Specifically, after introducing constraints, certain heuristic factors may become ineffective as they are based on distance calculations. Overreliance on heuristic factors may cause the designed algorithm to get trapped in local optima. In Scenario 1, the optimal value of HV is obtained when Î± and $\beta$ are set to 0.5 and 3.5 respectively. In Scenario 2, setting Î± and $\beta$ to 0 and 5 yields the optimal value of HV. In Scenario 3, the optimal value of HV is achieved when Î± and $\beta$ are set to 2 and 4 respectively. Results in Fig. 10 indicate the importance of choosing Î± and $\beta$ appropriately in different network scenarios, for guaranteeing the best performance of the designed algorithm.

## C. Energy and Time Trade-off Evaluation and the Optimized Multi-UAV Trajectories

In this section, we conduct extensive experiments to evaluate the trade-off between the maximum task completion time and the maximum energy consumption among all UAVs. We also evaluate the multi-UAV trajectories generated by the proposed MSMOACO, which are shown in Fig. 11.

To evaluate the effectiveness and performance of the proposed MSMOACO algorithm, we conduct a series of comparative experiments. Firstly, we introduce the conventional multi-objective particle swarm optimization algorithm (MOPSO), non-dominated sorting genetic algorithm II (NSGA-II), multi-objective dragonfly algorithm (MODA) and multi-objective antlion optimization algorithm (MOALO) as benchmark algorithms to solve the proposed problem in this work for comparison. Secondly, we compare the proposed algorithm with three recent studies on UAV-enabled wireless data collection. Specifically, Gao et al. [51] developed an AoI-optimal trajectory planning combine improved ACO (AOTPACO) algorithm comprising of association and planning to minimize sensor nodesâ AoIs through an iterative three-step process. Sun et al. [39] proposed an improved multi-objective ant lion optimization (IMOALO) algorithm with chaos-opposition based learning solution initialization and hybrid solution update operators to optimize the trade-off between energy consumption and transmission performance in a multi-UAV communication scenario. Liao and Friderikos [36] jointly optimized the UAVâs energy efficiency and sensor nodesâ AoI by formulating a multi-objective mixed integer linear programming (MILP) with a flow-based constraint set. The corresponding solution is referred to as MILP_P9 in this work. Finally, we devise an approach called

<!-- image-->  
(a)

<!-- image-->  
(b)

<!-- image-->  
(cï¼  
Fig. 12. The optimal trade-off between the maximum task completion time and the maximum energy consumption among all UAVs by different methods.

MSMOACO-H that removes the adaptive hovering strategy from MSMOACO for comparison. We also devise an approach called MSMOACO-M that removes the fitness-guided mutation strategy from MSMOACO for comparison. We run each of the above 10 designed algorithms 20 times respectively and record the non-dominated solution sets obtained from each experiment. Fig. 12 shows the optimal Pareto solution sets obtained from 20 experiments in three different network scenarios.

In Fig. 12, we can see that the proposed MSMOACO algorithm outperforms the four classic multi-objective optimization algorithms as well as the three approaches from recent works in three different network scenarios, in terms of the Pareto front. The advantage of our designed algorithm mainly lies in the embedded multiple strategies and the way that they are being incorporated, which could well handle the premature convergence and susceptibility to local optima due to the various correlated decision variables.

We can also find that the proposed MSMOACO algorithm yields the superior Pareto front, compared with MSMOACO-H and MSMOACO-M in Fig. 12. Specifically, the introduction of the adaptive hovering strategy results in a marginal performance improvement, since reducing the flight trajectory length may increase the hovering time at the same time. On the contrary, the introduction of the fitness-guided mutation strategy significantly improves the trade-off between the maximum task completion time and the maximum energy consumption among all UAVs. In Fig. 12(a), we find that the ACO-related distance heuristic factor has less effect on the performance improvement due to the non-adjacent and random distribution of start points and destination points of UAVs. When the start and destination points coincide in Fig. 12(b) and Fig. 12(c), the distance heuristic factor causes the algorithm to converge to local optima and thus the fitness-guided mutation strategy is introduced to balance the task completion time and energy consumption among UAVs. In fact, the comparative experiment of MSMOACO with MSMOACO-H and MSMOACO-M can be viewed as an ablation experiment, which proves the effectiveness of incorporating the two designed strategies.

TABLE II  
HV AND SIGNIFICANCE TESTING OF THE RESULTS FROM 20 EXPERIMENTS
<table><tr><td rowspan="2">HV</td><td colspan="3">Scenario 1</td><td colspan="3">Scenario 2</td><td colspan="3">Scenario 3</td></tr><tr><td>Mean</td><td>Std</td><td>T-test</td><td>Mean</td><td>Std</td><td>T-test</td><td>Mean</td><td>Std</td><td>T-test</td></tr><tr><td>MOPSO</td><td>0.3533</td><td>0.0354</td><td>+</td><td>0.3878</td><td>0.0276</td><td>+</td><td>0.3554</td><td>0.0423</td><td>+</td></tr><tr><td>NSGA-II</td><td>0.4164</td><td>0.0418</td><td>+</td><td>0.4587</td><td>0.0232</td><td>+</td><td>0.4564</td><td>0.0270</td><td>+</td></tr><tr><td>MODA</td><td>0.3014</td><td>0.0265</td><td>+</td><td>0.2247</td><td>0.0219</td><td>+</td><td>0.2069</td><td>0.0235</td><td>+</td></tr><tr><td>MOALO</td><td>0.2916</td><td>0.0181</td><td>+</td><td>0.3542</td><td>0.0229</td><td>+</td><td>0.3416</td><td>0.0303</td><td>+</td></tr><tr><td>MILP_P9</td><td>0.5076</td><td>0.0201</td><td>+</td><td>0.5605</td><td>0.0203</td><td>+</td><td>0.5598</td><td>0.0166</td><td>+</td></tr><tr><td>AOTPACO</td><td>0.6194</td><td>0.0029</td><td>+</td><td>0.5730</td><td>0.0029</td><td>+</td><td>0.2328</td><td>0.0022</td><td>+</td></tr><tr><td>IMOALO</td><td>0.2656</td><td>0.0186</td><td>+</td><td>0.3063</td><td>0.0132</td><td>+</td><td>0.3041</td><td>0.0179</td><td>+</td></tr><tr><td>MSMOACO-M</td><td>0.6393</td><td>0.0170</td><td>+</td><td>0.2853</td><td>0.0072</td><td>+</td><td>0.2748</td><td>0.0053</td><td>+</td></tr><tr><td>MSMOACO-H</td><td>0.6607</td><td>0.0124</td><td>+</td><td>0.6232</td><td>0.0185</td><td>+</td><td>0.5887</td><td>0.0362</td><td>+</td></tr><tr><td>MSMOACO</td><td>0.6824</td><td>0.0042</td><td></td><td>0.6696</td><td>0.0081</td><td></td><td>0.6486</td><td>0.0170</td><td></td></tr></table>

To comprehensively evaluate the performance of MSMOACO, we employ HV as the evaluation metric for quantitative analysis of the above comparative experiment results. In addition, we conduct paired t-tests to evaluate the statistical significance of the HV results at a significance level of 0.05. Table II shows the mean and variance of the HV values obtained from the 20 experiments. From Table II, it is clear that MSMOACO yields the best result and the paired t-tests reveal significant differences between MSMOACO and other compared algorithms.

Further, we randomly select 10 solutions from the nondominated solution set to evaluate the task completion time and energy consumption of each UAV. Fig. 13 and Fig. 14 illustrate the task completion time and energy consumption of each UAV for these 10 solutions. Results show that the task completion time and energy consumption are relatively uniform among all UAVs. For example in Scenario 1, UAVs have relatively the same task completion time, where the maximum gap is approximately 10 seconds. The differences in energy consumption between UAVs are within 1000 joules. In Scenarios 2 and 3, the variations in task completion time among UAVs are within 40 seconds and the differences in energy consumption among UAVs are within 10000 joules.

## D. Collision Avoidance Experiment

In order to validate the effectiveness of the proposed collision avoidance strategy, we conduct experiments shown in Fig. 15. The experiment involves four UAVs and four IoT devices. Each UAV starts from its start point, collects some data from one of the four IoT devices and returns to its destination point. Assuming the UAVâs flight speed is denoted as V , based on Eq. (27), the four UAVsâ positions are recorded every ât seconds and corresponding distances between UAVs are calculated. If the distance between any two UAVs is detected to be less than or equal to $d _ { \mathrm { m i n } }$ , we identify the most recent recording time when the relative distance is larger than or equal to $d _ { \mathrm { m i n } }$ and execute the proposed collision avoidance strategy. As shown in Fig. 15, subfigure (a) presents the flight trajessctories of UAVs without considering collision avoidance. Subfigure (b) illustrates the updated trajectories using the proposed geometry-based collision avoidance strategy. Specifically in subfigure (a), three potential collisions may happen if the four UAVs fly along their original trajectories: (1) UAV 1, UAV 2 and UAV 3 may simultaneously collide with each other during their flights; (2) UAV 1 and UAV 3 may have the second collision even if they successfully avoid the first collision; (3) UAV 2 may collide with UAV 4 when UAV 4 is hovering near $S N _ { 4 } ,$ even if it successfully avoids the collision with UAV 1 and UAV 3 in the first place. Subfigures (d), (e) and (f) provide enlarged views of how UAVs adjust their flight trajectories to avoid the above potential collisions respectively. In particular, we use colored points to represent real-time positions of UAVs. The points in the same color on different trajectories represent real-time positions of different UAVs at the same time instant, $\mathrm { e . g . }$ , the dark brown points in circles in subfigure (d). Results show that the proposed geometry-based collision avoidance strategy can prevent collisions among UAVs in various situations.

<!-- image-->

<!-- image-->  
Fig. 13. Task completion time of each UAV in selected non-dominated solutions.

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 14. Energy consumption of each UAV in selected non-dominated solutions.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 15. Experiments of trajectories updates using the proposed geometry-based collision avoidance strategy.

## VI. CONCLUSION

In this work, we investigated the problem of simultaneously minimizing the maximum task completion time and the maximum energy consumption among multiple UAVs dispatched to collect data in a large-scale IoT network. We designed a multistrategy multi-objective ant colony optimization algorithm (MSMOACO) to jointly optimize the flight trajectory, hovering positions for data collection, flight speed and collision avoidance of each UAV, for achieving the optimal trade-off between the maximum task completion time and the maximum energy consumption among all dispatched UAVs. We conducted extensive evaluations to demonstrate the effectiveness and superiority of our designed algorithm. Results showed that MSMOACO can well balance the task loads among all dispatched UAVs, in terms of both the task completion time and energy consumption. MSMOACO outperformed previous approaches by achieving a superior time-energy trade-off in various network scenarios.

## REFERENCES

[1] M. Kishk, A. Bader, and M.-S. Alouini, âAerial base station deployment in 6G cellular networks using tethered drones: The mobility and endurance tradeoff,â IEEE Veh. Technol. Mag., vol. 15, no. 4, pp. 103â111, Dec. 2020.

[2] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surveys Tuts., vol. 21, no. 3, pp. 2334â2360, 3rd Quart., 2019.

[3] X. Yuan, Y. Hu, J. Zhang, and A. Schmeink, âJoint user scheduling and UAV trajectory design on completion time minimization for UAVaided data collection,â IEEE Trans. Wireless Commun., vol. 22, no. 6, pp. 3884â3898, Jun. 2023.

[4] J. Zhang et al., âMinimizing the number of deployed UAVs for delaybounded data collection of IoT devices,â in Proc. IEEE Conf. Comput. Commun., May 2021, pp. 1â10.

[5] J. Gong, T.-H. Chang, C. Shen, and X. Chen, âFlight time minimization of UAV for data collection over wireless sensor networks,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1942â1954, Sep. 2018.

[6] M. Seong, O. Jo, and K. Shin, âMulti-UAV trajectory optimizer: A sustainable system for wireless data harvesting with deep reinforcement learning,â Eng. Appl. Artif. Intell., vol. 120, pp. 1â11, Apr. 2023.

[7] C. Zhan, Y. Zeng, and R. Zhang, âEnergy-efficient data collection in UAV enabled wireless sensor network,â IEEE Wireless Commun. Lett., vol. 7, no. 3, pp. 328â331, Jun. 2018.

[8] K. Liu and J. Zheng, âUAV trajectory optimization for time-constrained data collection in UAV-enabled environmental monitoring systems,â IEEE Internet Things J., vol. 9, no. 23, pp. 24300â24314, Dec. 2022.

[9] C. Zhao, J. Liu, M. Sheng, W. Teng, Y. Zheng, and J. Li, âMulti-UAV trajectory planning for energy-efficient content coverage: A decentralized learning-based approach,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3193â3207, Oct. 2021.

[10] X. Wang, M. C. Gursoy, T. Erpek, and Y. E. Sagduyu, âLearningbased UAV path planning for data collection with integrated collision avoidance,â IEEE Internet Things J., vol. 9, no. 17, pp. 16663â16676, Sep. 2022.

[11] J. K. Stolaroff, C. Samaras, E. R. OâNeill, A. Lubers, A. S. Mitchell, and D. Ceperley, âEnergy use and life cycle greenhouse gas emissions of drones for commercial package delivery,â Nature Commun., vol. 9, no. 1, pp. 1â13, Feb. 2018.

[12] W. Xu et al., âMinimizing the deployment cost of UAVs for delaysensitive data collection in IoT networks,â IEEE/ACM Trans. Netw., vol. 30, no. 2, pp. 812â825, Apr. 2022.

[13] W. Xu, W. Liang, X. Jia, H. Kan, Y. Xu, and X. Zhang, âMinimizing the maximum charging delay of multiple mobile chargers under the multinode energy charging scheme,â IEEE Trans. Mobile Comput., vol. 20, no. 5, pp. 1846â1861, May 2021.

[14] Q. Guo et al., âMinimizing the longest tour time among a fleet of UAVs for disaster area surveillance,â IEEE Trans. Mobile Comput., vol. 21, no. 7, pp. 2451â2465, Jul. 2022.

[15] S. Zhang, W. Liu, and N. Ansari, âCompletion time minimization for data collection in a UAV-enabled IoT network: A deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 72, no. 11, pp. 14734â14742, Nov. 2023.

[16] H.-C. Tsai, Y.-W. P. Hong, and J.-P. Sheu, âCompletion time minimization for UAV-enabled surveillance over multiple restricted regions,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 6907â6920, Dec. 2023.

[17] Y. Zhu and S. Wang, âEfficient aerial data collection with cooperative trajectory planning for large-scale wireless sensor networks,â IEEE Trans. Commun., vol. 70, no. 1, pp. 433â444, Jan. 2022.

[18] B. Khamidehi and E. S. Sousa, âReinforcement-learning-aided safe planning for aerial robots to collect data in dynamic environments,â IEEE Internet Things J., vol. 9, no. 15, pp. 13901â13912, Aug. 2022.

[19] C. Zhan, H. Hu, J. Wang, Z. Liu, and S. Mao, âTradeoff between age of information and operation time for UAV sensing over multi-cell cellular networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2976â2991, Apr. 2023.

[20] G. Nie, T. Ma, Z. Zhang, H. Tian, S. Mumtaz, and Z. Ding, âCoarse closed-loop trajectory design of multiple UAVs for parallel data collection,â IEEE Trans. Veh. Technol., vol. 72, no. 3, pp. 4026â4039, Mar. 2023.

[21] S. Song, M. Choi, D.-E. Ko, and J.-M. Chung, âMulti-UAV trajectory optimization considering collisions in FSO communication networks,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3378â3394, Nov. 2021.

[22] S. Xu, X. Zhang, C. Li, D. Wang, and L. Yang, âDeep reinforcement learning approach for joint trajectory design in multi-UAV IoT networks,â IEEE Trans. Veh. Technol., vol. 71, no. 3, pp. 3389â3394, Mar. 2022.

[23] X. Wang, M. Yi, J. Liu, Y. Zhang, M. Wang, and B. Bai, âCooperative data collection with multiple UAVs for information freshness in the Internet of Things,â IEEE Trans. Commun., vol. 71, no. 5, pp. 2740â2755, May 2023.

[24] C. Zhan, H. Hu, S. Mao, and J. Wang, âEnergy-efficient trajectory optimization for aerial video surveillance under QoS constraints,â in Proc. IEEE Conf. Comput. Commun., May 2022, pp. 1559â1568.

[25] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and J. Henry, âUAV trajectory planning in wireless sensor networks for energy consumption minimization by deep reinforcement learning,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 9540â9554, Sep. 2021.

[26] X. Dai, B. Duo, X. Yuan, and W. Tang, âEnergy-efficient UAV communications: A generalized propulsion energy consumption model,â IEEE Wireless Commun. Lett., vol. 11, no. 10, pp. 2150â2154, Oct. 2022.

[27] F. Shan, J. Luo, R. Xiong, W. Wu, and J. Li, âLooking before crossing: An optimal algorithm to minimize UAV energy by speed scheduling with a practical flight energy model,â in Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM), Oct. 2020, pp. 1758â1767.

[28] Z. Zhou, C. Zhang, C. Xu, F. Xiong, Y. Zhang, and T. Umer, âEnergyefficient industrial Internet of UAVs for power line inspection in smart grid,â IEEE Trans. Ind. Informat., vol. 14, no. 6, pp. 2705â2714, Jun. 2018.

[29] C. Zhan and Y. Zeng, âEnergy minimization for cellular-connected UAV: From optimization to deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5541â5555, Jul. 2022.

[30] D. Van Huynh, T. Do-Duy, L. D. Nguyen, M.-T. Le, N.-S. Vo, and T. Q. Duong, âReal-time optimized path planning and energy consumption for data collection in unmanned ariel vehicles-aided intelligent wireless sensing,â IEEE Trans. Ind. Informat., vol. 18, no. 4, pp. 2753â2761, Apr. 2022.

[31] Y. Chen, D. Pi, S. Yang, Y. Xu, J. Chen, and A. W. Mohamed, âHNIO: A hybrid nature-inspired optimization algorithm for energy minimization in UAV-assisted mobile edge computing,â IEEE Trans. Netw. Service Manage., vol. 19, no. 3, pp. 3264â3275, Sep. 2022.

[32] Y. Li et al., âData collection maximization in IoT-sensor networks via an energy-constrained UAV,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 159â174, Jan. 2023.

[33] Z. Dai et al., âAoI-minimal UAV crowdsensing by model-based graph convolutional reinforcement learning,â in Proc. IEEE INFOCOM Conf. Comput. Commun., May 2022, pp. 1029â1038.

[34] D. N. Das, R. Sewani, J. Wang, and M. K. Tiwari, âSynchronized truck and drone routing in package delivery logistics,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 9, pp. 5772â5782, Sep. 2021.

[35] Y. Wan, Y. Zhong, A. Ma, and L. Zhang, âAn accurate UAV 3-D path planning method for disaster emergency response based on an improved multiobjective swarm intelligence algorithm,â IEEE Trans. Cybern., vol. 53, no. 4, pp. 2658â2671, Apr. 2023.

[36] Y. Liao and V. Friderikos, âEnergy and age Pareto optimal trajectories in UAV-assisted wireless data collection,â IEEE Trans. Veh. Technol., vol. 71, no. 8, pp. 9101â9106, Aug. 2022.

[37] Y. Yu, J. Tang, J. Huang, X. Zhang, D. K. C. So, and K.-K. Wong, âMulti-objective optimization for UAV-assisted wireless powered IoT networks based on extended DDPG algorithm,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6361â6374, Sep. 2021.

[38] J. Zhu, X. Wang, H. Huang, S. Cheng, and M. Wu, âA NSGA-II algorithm for task scheduling in UAV-enabled MEC system,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 9414â9429, Jul. 2022.

[39] G. Sun, J. Li, Y. Liu, S. Liang, and H. Kang, âTime and energy minimization communications based on collaborative beamforming for UAV networks: A multi-objective optimization method,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3555â3572, Nov. 2021.

[40] X. Gao, X. Zhu, and L. Zhai, âMinimization of aerial cost and mission completion time in multi-UAV-enabled IoT networks,â IEEE Trans. Commun., vol. 71, no. 9, pp. 5335â5347, Sep. 2023.

[41] X. Lin, J. G. Andrews, A. Ghosh, and R. Ratasuk, âAn overview of 3GPP device-to-device proximity services,â IEEE Commun. Mag., vol. 52, no. 4, pp. 40â48, Apr. 2014.

[42] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[43] A. Hourani, S. Kandeepan, and A. Jamalipour, âModeling air-toground path loss for low altitude platforms in urban environments,â in Proc. IEEE Global Telecommun. Conf. (GLOBECOM), Oct. 2014, pp. 2898â2904.

[44] A. Al-Hourani, S. Kandeepan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[45] M. Mozaffari, W. Saad, M. Bennis, and M. Debbah, âUnmanned aerial vehicle with underlaid device-to-device communications: Performance and tradeoffs,â IEEE Trans. Wireless Commun., vol. 15, no. 6, pp. 3949â3963, Jun. 2016.

[46] Z. Yang, W. Xu, and M. Shikh-Bahaei, âEnergy efficient UAV communication with energy harvesting,â IEEE Trans. Veh. Technol., vol. 69, no. 2, pp. 1913â1927, Feb. 2020.

[47] Y. Wang, Z. Hu, X. Wen, Z. Lu, and J. Miao, âMinimizing data collection time with collaborative UAVs in wireless sensor networks,â IEEE Access, vol. 8, pp. 98659â98669, 2020.

[48] K. Deb, S. Agrawal, A. Pratap, and T. Meyarivan, âA fast elitist nondominated sorting genetic algorithm for multi-objective optimization: NSGA-II,â in Proc. 6th Int. Conf. Parallel Problem Solving Nature, Paris, France. Berlin, Germany: Springer, Sep. 2000, pp. 849â858.

[49] M. Li, S. He, and H. Li, âMinimizing mission completion time of UAVs by jointly optimizing the flight and data collection trajectory in UAV-enabled WSNs,â IEEE Internet Things J., vol. 9, no. 15, pp. 13498â13510, Aug. 2022.

[50] C. Sandoval, O. Cuate, L. C. GonzÃ¡lez, L. Trujillo, and O. SchÃ¼tze, âTowards fast approximations for the hypervolume indicator for multiobjective optimization problems by genetic programming,â Appl. Soft Comput., vol. 125, Aug. 2022, Art. no. 109103.

[51] X. Gao, X. Zhu, and L. Zhai, âAoI-sensitive data collection in multi-UAV-assisted wireless sensor networks,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5185â5197, Aug. 2023.

<!-- image-->  
Riheng Jia received the B.E. degree in electronics and information engineering from the Huazhong University of Science and Technology, China, in 2012, and the Ph.D. degree in computer science and technology from Shanghai Jiao Tong University, Shanghai, China, in 2018. He is currently an Associate Professor with the School of Computer Science and Technology, Zhejiang Normal University, China. His current research interests include wireless networks, energy harvesting networks, and smart IoT.

<!-- image-->  
Qiyong Fu received the M.S. degree in electronic information engineering from Zhejiang Normal University, China, in 2024. He is currently pursuing the Ph.D. degree with the School of Computer Science and Engineering, Central South University, Changsha, China. His current research interests include smart IoT and big data.

<!-- image-->

Zhonglong Zheng received the B.E. degree from China University of Petroleum, China, in 1999, and the Ph.D. degree from Shanghai Jiao Tong University, China, in 2005. He is currently a Full Professor with the School of Computer Science and Technology, Zhejiang Normal University, China. His research interests include machine learning, computer vision, and blockchain.

<!-- image-->

Guanglin Zhang (Member, IEEE) received the B.S. degree in applied mathematics from Shandong Normal University, Jinan, China, in 2003, the M.S. degree in operational research and cybernetics from Shanghai University, Shanghai, China, in 2006, and the Ph.D. degree in information and communication engineering from Shanghai Jiao Tong University, Shanghai, in 2012. From 2013 to 2014, he was a Post-Doctoral Research Associate with the Institute of Network Coding, The Chinese University of Hong Kong. He joined Donghua University, as an

Associate Professor, in 2014. From 2015 to 2021, he was the Department Chair of Communication Engineering. He was promoted to a Full Professor in 2017. From 2020 to 2023, he was the Associate Dean of the College of Information Science and Technology, Donghua University. He is currently the Special Appointment Eastern Scholar Professor, the Director of the Office of Talent Affairs, and the Associate Director of the Department of Human Resources, Donghua University. His research interests include online algorithms, capacity scaling of wireless networks, vehicular networks, smart microgrids, and mobile edge computing. He serves as a Technical Program Committee Member for IEEE GLOBECOM 2016â2017, IEEE ICC 2014, 2015, and 2017, IEEE VTC 2017 Fall, IEEE/CIC ICCC 2014, WCSP 2014, APCC 2013, and WASA 2012. He serves as the Local Arrangement Chair for ACM TURC 2017 and the Vice TPC Co-Chair for ACM TURC 2018. He serves as an Editor on the Editorial Board for China Communications. He is an Associate Editor of Computers and Electrical Engineering.

<!-- image-->

Minglu Li (Fellow, IEEE) received the Ph.D. degree in computer software from Shanghai Jiao Tong University in 1996. He is currently a Full Professor and the Director of the Artificial Intelligence Internet of Things (AIoT) Center, Zhejiang Normal University. He is also the Holding Director of the Network Computing Center, Shanghai Jiao Tong University. He has published more than 400 papers in academic journals and international conferences. His research interests include vehicular networks, big data, cloud computing, and wireless sensor networks. He also

served as a PC Member for more than 50 international conferences, including IEEE INFOCOM 2009â2016 and IEEE CCGrid 2008. From 2004 to 2016, he was the Chairperson of the Technical Committee on Services Computing (TCSVC) and the Technical Committee on Distributed Processing (TCDP) of the IEEE Computer Society in the Great China Region from 2005 to 2017. He served as the General Co-Chair for IEEE SCC, IEEE CCGrid, IEEE ICPADS, and IEEE IPDPS, and the Vice Chair for IEEE INFOCOM.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_1.png|page_12_img_1]]
2. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_2.png|page_12_img_2]]
3. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_3.png|page_12_img_3]]
4. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_4.png|page_12_img_4]]
5. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_5.png|page_12_img_5]]
6. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_12_img_6.png|page_12_img_6]]
7. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_16_img_1.png|page_16_img_1]]
8. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_16_img_2.png|page_16_img_2]]
9. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_16_img_3.png|page_16_img_3]]
10. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_16_img_4.png|page_16_img_4]]
11. [[../extracted_images/Jia 等 - 2024 - Energy and Time Trade-Off Optimization for Multi-UAV Enabled Data Collection of IoT Devices/page_16_img_5.png|page_16_img_5]]

---

