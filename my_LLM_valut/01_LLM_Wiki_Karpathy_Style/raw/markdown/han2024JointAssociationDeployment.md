# Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-Enabled Large-Scale Mobile Edge Computing

Shoufei Han , Xiaojing Liu , MengChu Zhou , Fellow, IEEE, Kun Zhu , Member, IEEE, Liang Zhao , Member, IEEE, Aiiad Albeshri , and Abdullah Abusorrah , Senior Member, IEEE

AbstractâThis work investigates how multiple unmanned aerial vehicles (UAVs) assist the large-scale IoT devices (its count â¥ 100) in the edge computing system in accomplishing their tasks. The UAVs serve the latter as edge servers, and fly to footholds to collect task data from the latter, execute tasks locally and return results to the latter. The goal of this work is to minimize overall energy consumption by jointly optimizing the association between each UAV and ground-based IoT devices, deployments of UAVs, and their flight trajectories. To achieve this, this work proposes a joint optimization approach (JOA). It has three parts: 1) an improved k-means method is designed to handle the association between each UAV and ground-based IoT devices, where the number of clusters is equal to that of UAVs, which means that each UAV is responsible for the IoT devices within a cluster; 2) for the deployments of UAVs, an improved fireworks algorithm (IFWA) with variable-length encoding strategy and population size update strategy is proposed to optimize the number and locations of footholds of each UAV, where each member of the population symbolizes a UAV foothold, and each firework and its offspring are considered as the deployment of UAV. Also, the population size update strategy is employed to dynamically change the number of footholds; and 3) regarding UAV flight trajectory, a pre-computed greedy algorithm based on the footholds of UAVs obtained by IFWA is proposed to minimize

the total UAV distance. The proposed approach is verified on ten large-scale instances, and the results demonstrate its effectiveness in achieving minimal energy consumption when compared to other state-of-the-art methods.

Index TermsâAssociation, deployment, fireworks algorithm, flight trajectory, k-means, large-scale edge computing system, multi -UAV, pre-computed greedy algorithm.

## I. INTRODUCTION

## A. Background

W ITH the rapid development of mobile communicationtechnology, handling a variety of smart devices and technology, handling a variety of smart devices and huge amount of Big Data they generate is one of the challenges facing the next generation of IoT [1]. The Internet of Everything has brought about the continuous development and growth of business areas such as video streaming [2], home healthcare [3], transportation systems [4], smart driving [5], real-time haptic control [6], and augmented reality [7]. These applications require increasing computing and storage resources, while the limited energy, computing power and memory of IoT devices, especially mobile devices, cannot support their local processing of the required tasks. To solve this issue, an effective solution is to deploy servers or computing nodes closer to users. Mobile edge computing (MEC) [8] came into being about ten years. It is a technology that deeply integrates mobile access networks with Internet services. Compared with traditional cloud computing, MEC has the advantages of distributed computing, wireless connectivity and proximity communication. It is one of the important technologies to achieve edge intelligence in 5G and future 6G network architectures.

In an MEC system, cellular base stations and wireless access points boasting storage and computing capabilities offer task offloading services to users. However, the placement of these base stations or servers as edge computing nodes remains static, resulting in certain drawbacks such as constrained and unchanging service coverage, signal degradation due to long communication distances, and elevated expenses tied to the extensive deployment of fixed MEC servers. Consequently, addressing the deployment of edge computing nodes within dynamic environments or intricate landscapes with the goal of cost reduction emerges as a critical consideration in the future MEC network architecture.

In recent years, unmanned aerial vehicles (UAVs) have garnered sustained interest in wireless communications due to their easy to be deployed, mobility and portability. They have been applied to various fields successfully, such as data collection [9], cellular networks [10], video detection and tracking [11] and environmental monitoring [12]. More recently, UAVs have been seen as mobile base stations or servers in MEC [13], [14]. Their use brings the following advantages: 1) UAVs have the flexibility to fly anywhere to act as edge nodes, which can reduce communication distance effectively; and 2) UAVs have the capability to offer a better line-of-sight (LoS) wireless link, which can reduce transmission delay effectively. In this work, they are acted as edge nodes aiming to assist the large-scale IoT devices in completing the tasks, and then returning the results to the latter. In this system, we aim to minimize overall energy consumption by jointly optimizing their association with IoT devices, deployment and flight trajectories.

## B. Related Work

Related work on the association, deployment and flight trajectory optimization for UAVs is briefly reviewed.

1) Association Optimization: In a multi-UAV enabled mobile edge computing system, association optimization aims to assign different tasks or IoT devices to specific UAVs optimally in terms of overall energy consumption.

Wang et al. [15] studied uplink transmission in a UAV assisted cellular network by designing appropriate UAV deployment and association schemes to minimize the transmission power consumption of users and UAVs. They proposed their schemes based on statistical user location and a centralized multi-agent Q-learning algorithm. Hammouti et al. [16] proposed a Learn-As-You-Fly algorithm to optimize the 3D locations of UAVs and associate with ground users such that the network rate is maximized. In [17], they presented a game-theoretic learning algorithm and heuristic greedy algorithm to handle user-UAV association and UAV locations aiming to better serve a large number of ground users. Xi et al. [18] first modeled a joint user association and UAV location optimization problem as a mixed-integer non-convex optimization one, and then proposed an iterative algorithm to maximize the total data rates. Qian et al. [19] used an UAV to act as the edge computing server to assist in executing the tasks in MEC, jointly optimized user association and UAV trajectory to maximize sum bits offloaded. In [20], the authors first formulated a user association scheduling and power allocation problem as a Markov decision process, and then proposed a distributed relative value iteration method to solve it. Fu et al. [21] aimed to maximize the worst user rate by jointly optimizing UAV flight trajectory, user association and uplink power control, and utilized offline and online reinforcement learning to solve it. Han et al. [22] minimized the average task delay by jointly optimizing user association and UAV deployment, where they used optimal transport theory for the former and a particle swarm optimizer for the latter.

2) Deployment Optimization: The deployment of multiple UAVs is of key importance for multi-UAV-enabled mobile edge computing systems, and the optimal deployment can ensure that

UAVs use a relatively short distance and less time to obtain greater benefits, thereby saving more energy consumption. To better provide high-quality computing and communication services, Deng et al. [23] proposed a four-stage alternating iterative computation efficiency maximization algorithm to maximize the computation efficiency of devices by optimizing the CPU frequency, transmission power, offloading decision, and the 3D deployment and beamwidth of UAV. In [24], Liao et al. proposed an energy-aware 3D-deployment of UAVs to provide a high uplink rate with fewer UAVs in Internet of Vehicles, wherein the vehicles was first divided into a certain number of clusters, and the number was optimized via an iterative algorithm. Then, a stochastic gradient ascent method was developed to optimize the flight altitude of UAV. To reduce communication energy consumption, Lin et al. [25] developed an adaptive UAV deployment scheme to cover as many ground devices as possible, wherein iterative method and power control policy were designed to obtain the optimal UAV location in the context of emergency networking. In [26], Lai et al. first modeled a multi-UAV deployment problem as a user satisfaction maximization problem, and then proposed an interference-aware deployment algorithm to solve it. Wang and Duan [27] first formulated a learning-andadaption based UAV deployment problem as a partially observable Markov decision process aiming at maximizing the total discounted hit rate of active users, and then apply the Q-learning algorithm to solve it. To maximize the communication coverage, Zhou et al. [28] optimized the 3D placement of UAVs and transmission power for covert communications, where they derived the closed-form expressions to solve the optimal 3D placement and transmission problem. Zhang and Duan [29] studied the fast UAV deployment problem with two different objectives: one is to minimize the maximum deployment delay between all UAVs, and the other is to minimize the total deployment delay; and designed several optimization algorithms to solve them. Zhu et al. [30] considered both coverage and energy consumption objectives in their formulated multi-objective problem to optimize UAV deployment, and presented an improved multi-objective grey wolf optimizer to solve it.

3) Flight Trajectory Planning: For a multi-UAV-enabled mobile edge computing system, UAV flight trajectory planning is another important topic. A proper UAV flight trajectory can not only shorten the flight distance of UAVs, reduce task execution time, and improve the quality of service, but also can effectively save energy consumption for UAVs.

A 3D trajectory method for solar-powered UAVs is devised to collect data from multiple ground IoT devices while ensuring service fairness among ground IoT devices [31]. To minimize the energy consumption and transmission delay, Gong et al. [32] optimized UAV trajectory planning and network formation, where a multi-agent deep reinforcement learning and Bayesian optimization were used to handle the former, and a heuristic algorithm was applied to latter. In [33], a joint optimization problem for UAV trajectory planning, energy renewal and application placement was formulated to maximize the long-term energy efficiency, and then a novel triple learner based reinforcement learning approach was devised to handle it. Li et al. [34] used digital twin to assist vehicular edge computing networks, where UAV trajectory and computation resource were jointly optimized to minimize energy consumption. Liu et al. [35] studied a UAV-enabled wireless powered mobile edge learning system and proposed two effective algorithms, namely successive convex approximation and alternating optimization, were proposed to optimize sample size, transmission power, and UAV flight trajectory and velocity. Andreou et al. [36] proposed a modified $\mathbf { A } ^ { * }$ Algorithm for the planning of UAV flight paths. Wang et al. [37] designed and analyzed for the first time a cooperative path planning algorithm for large UAV swarms to optimally serve multiple spatial locations. Hu et al. [38] presented an integrated optimization problem to maximize the computational efficiency of the system through the joint design of formations, UAV trajectories and resource allocation. They proposed a Dinkelbach-based loop iterative optimizer to solve it.

KEY LIMITATIONS OF EXISTING WORK [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38]
<table><tr><td rowspan=1 colspan=1>Paper</td><td rowspan=1 colspan=1>Associationoptimization</td><td rowspan=1 colspan=1>Deploymentoptimization</td><td rowspan=1 colspan=1>Trajectoryplanning</td><td rowspan=1 colspan=1>Energyconsumption</td></tr><tr><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[16]-[18], [22]</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[19], [21]</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[23]-[25],[30]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1>[26]-[29]</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>Ã</td><td rowspan=1 colspan=1>Ã</td></tr><tr><td rowspan=1 colspan=1>[31]-[34]</td><td rowspan=1 colspan=1> $\times$ </td><td rowspan=1 colspan=1> $\times$ </td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1> $\checkmark$ </td></tr><tr><td rowspan=1 colspan=1>[35]-[38]</td><td rowspan=1 colspan=1> $\times$ </td><td rowspan=1 colspan=1> $\times$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\times$ </td></tr><tr><td rowspan=1 colspan=1>Ours</td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\checkmark$ </td><td rowspan=1 colspan=1> $\overline { { \checkmark } }$ </td></tr></table>

The primary constraints of the previously mentioned relevant research are outlined in Table I. From Table I, it can be observed that the above reviewed studies optimize only one or several of association, deployment and flight trajectory but not all three. It can be further found that some of them, i.e., [16], [17], [18], [19], [21], [22], [26], [27], [28], [29], [35], [36], [37], [38], are not mathematically modeled with energy consumption as an objective function. Different from them, this work jointly optimizes association, deployment and flight trajectory of UAVs to minimize the energy consumption.

## C. Challenges and Solution

In a large-scale MEC, UAVs are usually regarded as edge nodes to assist large-scale ground IoT devices to complete the latterâs tasks due to their convenience and mobility. Since the energy of each UAV itself is limited, how to best utilize its limited energy to complete as many tasks as possible is a challenge. Next, for large-scale ground IoT devices, as the scale increases, so does the complexity of the problem, thus leading many existing methodsâ failure to solve it in an acceptable time. As the count of footholds varies in deployment optimization, devising a solution becomes a complex task. Finally, joint optimization of association, deployment and flight trajectory of UAVs is a coupling problem, i.e., their results influence each other. In light of the preceding analysis, we assert that jointly optimizing of association, deployment and flight trajectory of UAVs for multi-UAV enabled large-scale MEC system is a highly challenging and open problem. To this end, this work designs a joint optimization approach to cope with the above challenges. Specifically, it designs the improved k-means method to put close IoT devices together to form a cluster, which effectively reduces the energy consumption of the UAVs serving the cluster. It designs a variable-length encoding strategy and a population size updating strategy to well solve the case of not getting an effective solution due to increasing problem scale. Finally, a greedy algorithm is proposed to obtain the UAV flight trajectory with the shortest distance.

## D. Contributions and Organization

This work attempts to make the following new contributions to the field of multi-UAV-enabled MEC.

1) Proposing a joint optimization approach (JOA) to optimize the association between UAVs and ground-based IoT devices, their deployment, and their flight trajectories such that the overall energy consumption is minimized.

2) Designing an improved k-means method (IKM) to handle association optimization, cluster centers are first determined based on the given locations of ground IoT devices, and then large-scale ground IoT devices are divided into multiple clusters, cluster is assigned a UAV to act as an edge node.

3) Proposing an improved fireworks algorithm (IFWA) to optimize deployments of UAVs, where a variable-length encoding strategy and population size update strategy are devised to optimize the number and locations of footholds for UAVs.

4) Developing a pre-computed greedy algorithm (PGA) to optimize flight trajectories of UAVs based on the given locations of footholds, the distances between each foothold are first computed and stored, and then a greedy algorithm is devised to chart an appropriate flight trajectory based on the precomputed distances

5) Verifying the effectiveness of the proposed method across ten large-scale instances by comparing their results with established algorithms.

The rest of this paper is structured as follows. In Section II, we present the system model and outline the problem formulation. Section III introduces the fireworks algorithm and explains why it is chosen. Section IV offers a comprehensive description of the proposed JOA. Section V gives experimental result analyses. Finally, Section VI concludes this paper.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

As depicted in Fig. 1, a multi-UAV-enabled large-scale MEC system in each UAV flies to its responsible area to assist the ground IoT devices to complete their corresponding tasks, and then returns the computed results to these devices. Large-scale ground IoT devices are first divided into multiple orange circles (clusters), and the count of clusters corresponds to that of UAVs. Then, each UAV flies to a cluster aiming to complete the tasks uploaded from ground IoT devices in that cluster. Finally, UAV in a cluster flies to one foothold to assist in completing tasks, and then it continues to fly to other footholds in a cluster to complete tasks. Considering that the energy of each UAV is limited, this work aims to minimize the energy consumption of the entire system. We have four types of energy consumption for task transmission, task execution, UAV hovering and UAV flight. They are computed as follows:

<!-- image-->  
Fig. 1. A scene where multiple UAVs are assisting ground IoT devices to complete tasks and each UAV is only responsible for the ground IoT devices in an orange circle.

1) Task Transmission: In the system, there are n UAVs (denoted as $\mathcal { N } = \{ 1 , 2 , . . . , n \} ;$ and m ground IoT devices (denoted as $\mathcal { M } = \{ 1 , 2 , . . . , m \} )$ , which means that m ground IoT devices =are divided into n clusters. We define the number of footholds in the i-th cluster as $k _ { i }$ (denoted as ${ \mathcal { K } } _ { i } = \{ 1 , 2 , . . . , k _ { i } \} , i \in { \mathcal { N } } )$ =Itâs important to note that the number of footholds varies among different clusters, and the specific number of footholds within each cluster is both variable and unknown in advance.

The location of the j-th foothold at the i-th cluster is denoted as $( X _ { j } ^ { i } , Y _ { j } ^ { i } , H )$ , where H is assigned a constant value. The location of the t-th IoT device at the i-th cluster is denoted as $( x _ { t } ^ { i } , y _ { t } ^ { i } , h _ { t } ^ { i } )$ . Then, the distance between the j-th foothold and the t-th IoT device at the i-th cluster can be expressed as:

$$
\begin{array} { r l } & { d _ { j t } ^ { i } = \sqrt { ( X _ { j } ^ { i } - x _ { t } ^ { i } ) ^ { 2 } + ( Y _ { j } ^ { i } - y _ { t } ^ { i } ) ^ { 2 } + ( H - h _ { t } ^ { i } ) ^ { 2 } } , } \\ & { \quad \quad \quad \forall i \in \mathcal { N } , j \in \mathcal { K } _ { i } , t \in \mathcal { M } . } \end{array}\tag{1}
$$

In this system, we consider line-of-sight (LoS) and non-lineof-sight (NLoS) models aiming to better fit the real situation. We have the average path loss between the j-th foothold and the t-th IoT device at the i-th cluster [15]:

$$
\begin{array} { r } { L _ { j t } ^ { i } = \widehat { P } _ { j t } ^ { i } \underbrace { K ( d _ { j t } ^ { i } ) ^ { 2 } \mu _ { L } } _ { \mathrm { L o S l i n k p a t h l o s s } } + \widetilde { P } _ { j t } ^ { i } \underbrace { K ( d _ { j t } ^ { i } ) ^ { 2 } \mu _ { N } } _ { \mathrm { N L o S l i n k p a t h l o s s } } , } \end{array}\tag{2}
$$

$$
K = { \frac { 4 \pi f } { V _ { L } } } ,\tag{3}
$$

where $\mu _ { L }$ and $\mu _ { N }$ are the LoS and NLOS additional path losses, respectively. $f$ is the carrier frequency and $V _ { L }$ is the speed of light. $\widehat { P } _ { j t } ^ { i }$ and $\widetilde { P } _ { j t } ^ { i }$ are the probabilities of the t-th IoT device sending tasks to the j-th foothold at the i-th cluster according to LoS and NLoS, respectively. They can be obtained as:

$$
\widehat { P } _ { j t } ^ { i } = \frac { 1 } { 1 + \alpha \exp { ( - \beta ( \frac { 1 8 0 } { \pi } e _ { j t } ^ { i } - \alpha ) ) } } ,\tag{4}
$$

$$
\widetilde { P } _ { j t } ^ { i } = 1 - \widehat { P } _ { j t } ^ { i } ,\tag{5}
$$

$$
e _ { j t } ^ { i } = \arcsin ( \frac { H } { d _ { j t } ^ { i } } ) ,\tag{6}
$$

where Î± and $\beta$ are environmental constants. $e _ { j t } ^ { i }$ denotes the angle of elevation from the t-th IoT device to the j-th foothold at the i-th cluster.

Then, we can have the average channel power gain [9]:

$$
g _ { j t } ^ { i } = \frac { 1 } { L _ { j t } ^ { i } } .\tag{7}
$$

For a better description, flag $F _ { j t } ^ { i }$ is defined to determine whether the IoT device transmits a task to its corresponding UAV (cluster) or not. $F _ { j t } ^ { i } = 1$ means that the t-th IoT device chooses =the UAV at the j-th foothold within the i-th cluster to transmit the task. Otherwise, $F _ { i t } ^ { i } = 0$ . Note that the communication between =UAV and IoT devices is interfered by other IoT devices selecting other UAVs for sending tasks. Therefore, the transmission rate is [39]:

$$
r _ { j t } ^ { i } = \frac { B } { \sum _ { t = 1 } ^ { m } F _ { j t } ^ { i } } l o g _ { 2 } ( 1 + \mathrm { S I N R } _ { j t } ^ { i } ) ,\tag{8}
$$

$$
\mathrm { S I N R } _ { j t } ^ { i } = \frac { P _ { t } g _ { j t } ^ { i } } { \sum _ { \alpha = 1 , \alpha \neq i } ^ { n } \sum _ { \beta = 1 , \beta \neq t } ^ { m } F _ { j \beta } ^ { \alpha } P _ { t } g _ { j \beta } ^ { \alpha } + \sigma ^ { 2 } } ,\tag{9}
$$

where B is the bandwidth and $\textstyle \sum _ { t = 1 } ^ { m } F _ { j t } ^ { i }$ represents the number of IoT devices for which the i-th UAV is responsible. $\mathrm { S I N R } _ { j t } ^ { i }$ is the signal-to-interference-plus-noise ratio (SINR) of the i-th UAV. $P _ { t }$ is the transmission power. $\sigma ^ { 2 }$ is the white Gaussian noise power.

In the system, each UAV hovers at a foothold to receive tasks from ground IoT devices, and thus each IoT device needs to store a certain number of tasks. We use T aski to demote that of the t-th IoT device at the i-th cluster. Then we can have the transmission time:

$$
T _ { j t } ^ { i } = \frac { T a s k _ { t } ^ { i } } { r _ { j t } ^ { i } } .\tag{10}
$$

After that, the energy consumption for data transmission from the t-th IoT device to the j-th foothold at the i-th cluster can be computed as:

$$
E _ { j t } ^ { i } = P _ { t } T _ { j t } ^ { i } .\tag{11}
$$

Further, the total transmission energy consumption of the system can be expressed as:

$$
E _ { 1 } = \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { k _ { i } } \sum _ { t = 1 } ^ { m } F _ { j t } ^ { i } E _ { j t } ^ { i } .\tag{12}
$$

2) Task Execution: Upon receiving the task from the t-th IoT device within the i-th cluster, the UAV located at the j-th foothold initiates task execution. With a consistent computing resource denoted as $c _ { j t } ^ { i }$ across all UAVs, the computing time can be calculated as follows:

$$
Q _ { j t } ^ { i } = \frac { T a s k _ { t } ^ { i } S _ { t } ^ { i } } { c _ { j t } ^ { i } } ,\tag{13}
$$

where $S _ { t } ^ { i }$ is the computing resource necessary to process a single bit within a task transmitted by the t-th IoT device within the i-th cluster.

Then, the execution energy consumption between the t-th IoT device and the j-th foothold at the i-th cluster can be expressed as:

$$
\widetilde { E } _ { j t } ^ { i } = P _ { e } Q _ { j t } ^ { i } ,\tag{14}
$$

where $P _ { e }$ is execution power. Therefore, the total execution energy consumption of the system can be expressed as:

$$
E _ { 2 } = \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { k _ { i } } \sum _ { t = 1 } ^ { m } F _ { j t } ^ { i } \widetilde { E } _ { j t } ^ { i } ,\tag{15}
$$

3) Hovering: In each cluster, a UAV must hover at each foothold to receive and carry out tasks. The time of UAV hovering at the j-th foothold can be formulated as follows:

$$
U _ { j } ^ { i } = \operatorname* { m a x } \{ T _ { j t } ^ { i } + Q _ { j t } ^ { i } \} , \forall t \in \mathcal { M } .\tag{16}
$$

The energy consumption during hovering at the j-th foothold is [40]:

$$
\widehat { E } _ { j } ^ { i } = P _ { h } U _ { j } ^ { i } , \forall i \in \mathcal { N } ,\tag{17}
$$

$$
P _ { h } = P _ { 0 } + P _ { 1 } = \underbrace { { \frac { \delta } { 8 } } \rho s A \Omega ^ { 3 } { \hat { R } } ^ { 3 } } _ { P _ { 0 } } + \underbrace { ( 1 + k ) { \frac { W ^ { \frac { 3 } { 2 } } } { \sqrt { 2 \rho A } } } } _ { P _ { 1 } }\tag{18}
$$

where $P _ { h }$ is hovering power, which is composed of profile power $( P _ { 0 } )$ and induced one $( P _ { 1 } )$ . Î´ is the airfoil drag coefficient. $\rho ,$ s and A represent air density, rotor compactness and rotor disc area, respectively. , R, W and k are the angular velocity of the Î©blades (radians/sec), the radius of the rotor (m), the weight of the UAV (Newtons), and the incremental correction factor for the induced power, respectively.

The total hover energy consumption of this system is:

$$
E _ { 3 } = \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { k _ { i } } \widehat { E } _ { j } ^ { i } ,\tag{19}
$$

4) Flight: Following the establishment of footholds within each cluster, UAVs initiate their journey to each foothold for data collection and task execution. Each foothold must be visited only once, making this scenario similar to the traveling salesman problem. Consequently, the total UAV flight distance within each cluster can be computed as:

$$
\widetilde { D } _ { f } ^ { i } = \sum _ { u = 1 } ^ { k _ { i } } \sum _ { v = 1 } ^ { k _ { i } } \hat { d } _ { u v } J _ { u v } , \forall i \in \mathcal { N } ,\tag{20}
$$

where $\hat { d } _ { u v }$ is the distance the distance between the u-th and v-th footholds. $J _ { u v }$ a binary parameter used to ascertain whether the footholds u and v are part of the loop path. It is set to 1 if the footholds u and v are on the loop path; and otherwise, it is set to 0.

Then, the flight time at the i-th cluster can be calculated as:

$$
G ^ { i } = \frac { \widetilde { D } _ { f } ^ { i } } { \nu } ,\tag{21}
$$

where Î½ is the speed of a UAV.

Thus, if the flight power is $P _ { f }$ , the total flight energy consumption is [39]:

$$
E _ { 4 } = \sum _ { i = 1 } ^ { n } P _ { f } G ^ { i } .\tag{22}
$$

$$
P _ { f } = P _ { 0 } \left( 1 + \frac { 3 \nu ^ { 2 } } { \nu _ { b } ^ { 2 } } \right) + \frac { P _ { 1 } \nu _ { 0 } } { \nu } + \frac { d _ { 0 } \rho s A \nu ^ { 3 } } { 2 } ,\tag{23}
$$

where $\nu _ { b }$ is the tip speed of the blade. $d _ { 0 }$ and $\nu _ { 0 }$ represent the fuselage resistance ratio and the mean rotor induced velocity, respectively.

## B. Problem Formulation

Our goal is to minimize energy consumption through the joint optimization of UAV associations, deployments, and flight trajectories. Specifically, the association between each UAV and ground-based IoT devices is first optimized and IoT devices are thus divided into different clusters. After that, each UAV is assigned to be responsible for a cluster. For cluster i, we further optimize the number of footholds, denoted as $k _ { i }$ , as well as the precise locations of these footholds, represented as $( X _ { j } ^ { i } , Y _ { j } ^ { i } ) , i \in$ N and $j \in \mathcal { K } _ { i }$ . Thus, this problem can be formulated as follows:

$$
\operatorname* { m i n } _ { ( X _ { j } ^ { i } , Y _ { j } ^ { i } ) , k _ { i } } w _ { 1 } E _ { 1 } + w _ { 2 } E _ { 2 } + w _ { 3 } E _ { 3 } + w _ { 4 } E _ { 4 }\tag{24a}
$$

$$
\begin{array} { r } { \mathrm { s . ~ t ~ } \ F _ { j t } ^ { i } , J _ { u v } \in \{ 0 , 1 \} , \forall i \in \mathcal { N } , j \in \mathcal { K } _ { i } , t \in \mathcal { M } , } \end{array}\tag{24b}
$$

$$
\sum _ { j = 1 } ^ { k _ { i } } { F } _ { j t } ^ { i } = 1 , \forall i \in \mathcal { N } , t \in \mathcal { M } ,\tag{24c}
$$

$$
\sum _ { t = 1 } ^ { m } F _ { j t } ^ { i } \leq M , \forall i \in \mathcal { N } , j \in \mathcal { K } _ { i } ,\tag{24d}
$$

$$
\sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { k _ { i } } \sum _ { t = 1 } ^ { m } F _ { j t } ^ { i } = m ,\tag{24e}
$$

$$
\sum _ { u = 1 } ^ { k _ { i } } J _ { u v } = 1 , \forall i \in \mathcal { N } , v \in \mathcal { K } _ { i } ,\tag{24f}
$$

$$
\sum _ { v = 1 } ^ { k _ { i } } J _ { u v } = 1 , \forall i \in \mathcal { N } , u \in \mathcal { K } _ { i } ,\tag{24g}
$$

$$
\sum _ { u \in S _ { i } } \sum _ { v \in S _ { i } } J _ { u v } \le | S _ { i } | - 1 , \forall S _ { i } \subset \mathcal { G } _ { i } , \forall i \in \mathcal { N } ,\tag{24h}
$$

$$
{ \check { X } } \le X _ { j } ^ { i } \le { \hat { X } } , \forall i \in \mathcal { N } , j \in \mathcal { K } _ { i } ,\tag{24i}
$$

$$
\check { Y } \le Y _ { j } ^ { i } \le \hat { Y } , \forall i \in \mathcal { N } , j \in \mathcal { K } _ { i } ,\tag{24j}
$$

$$
\check { k } _ { i } \leq k _ { i } \leq \hat { k } _ { i } , \forall i \in \mathcal { N } ,\tag{24k}
$$

In (24), $w _ { 1 } â w _ { 4 }$ are the weights to balance $E _ { 1 } â E _ { 4 } . \mathcal { G } _ { i }$ is the set of footholds at the i-th cluster, and $S _ { i }$ is its subset, the size of $s _ { i }$ $( | S _ { i } | )$ falls in $\{ 2 , 3 , . . . , k _ { i ^ { - 1 } } \}$ . X and ${ \hat { X } } , { \check { Y } }$ and $\hat { Y } , \check { k } _ { i }$ and $\hat { k } _ { i }$ are lower and upper bounds of the x-axis, y-axis and the number of footholds at the i-th cluster, respectively. Meanwhile, the maximum number $( \hat { k } _ { i } )$ and the minimum one $( \check { k } _ { i } )$ of footholds in the i-th cluster are respectively set to the number of IoT devices in the i-th cluster (denoted as A) and $\lfloor { \frac { A } { M } } \rfloor \ ( \lfloor \cdot \rfloor$ is a floor function) since we stipulate that a UAV can accept up to M IoT transmission tasks at each foothold due to the limitation of bandwidth.

From (24), it is evident that constraint (24c) ensures that within a cluster, each IoT device only choose one foothold for transmitting its task. Constraint (24d) specifies that a UAV situated at a given foothold can accommodate a maximum of M IoT devices for task transmission. Constraint (24e) ensures the completion of tasks by UAVs in each cluster. Lastly, constraints (24f)â(24h) correspond to those typically encountered in the traveling salesman problem.

Remark 1. We fix the height of UAV at one foothold in this work. Based on the above model, we conclude that as UAV height increases, transmission rate decreases and transmission time increases, resulting in an increase in energy consumption. Conversely, as it decreases, the average path loss decreases and the transmission rate increases, thereby reducing transmission time and energy consumption. Consequently, the selection of an appropriate UAV height at each foothold poses a challenge to be addressed in our future work.

(21) is a mixed-integer non-convex NP-hard problem, and it is also a large-scale optimization problem, which is generally difficult to deal with by traditional gradient-based methods. It is found that the evolutionary algorithms, as a type of gradient-free methods, have shown strong potential for solving such problems [41], [42]. Thus, this work proposes a joint optimization approach (JOA) to tackle it via an evolutionary algorithm. More specifically, we design an improved fireworks algorithm (IFWA) that incorporates variable-length encoding strategy and population size update strategy, to be presented next.

## III. FIREWORKS ALGORITHM

In this section, the basic operators of FireWorks Algorithm (FWA) is first introduced, and then we give the reasons that selecting it as the base approach for our concerned problem.

## A. Introduction to Fireworks Algorithm

FireWorks Algorithm (FWA) [43] is a swarm intelligence algorithm with an explosion search mechanism for global optimization problems, inspired by the observation of the phenomenon of fireworks explosion in the air. In it, each firework first generates a certain number of sparks through the explosion operator, and then the appropriate fireworks are selected from all the fireworks and generated sparks through a selection strategy to move to the next iteration and continue to evolve. FWA contains two basic operations, namely explosion and selection, which are presented in detail below.

1) Explosion: In FWA, a firework or spark represents a solution in a feasible space. Given firework $\mathbf { x } ( p )$ and its location expresses as $( x ^ { 1 } ( p ) , \bar { x ^ { 2 } } ( p ) , . . . , x ^ { l } ( p ) )$ , where p and l are the number of generations and problem dimension, respectively, $\mathbf { x } ( p )$ needs to generate a certain number of sparks through an explosion operator. The locations of the generated sparks are:

$$
{ \bf z } ( p ) = { \bf x } ( p ) + r _ { 1 } R ( p )\tag{25}
$$

where $r _ { 1 }$ is a random number in [-1, 1], and R is an explosion range. Note that the explosion range R is first set to a fixed value when $p = 1$ , and then dynamically updated, i.e., enlarged =or reduced. Specifically, it can be calculated as, $\forall p > 1$

$$
\begin{array}{c} R ( p ) = { \left\{ R ( p - 1 ) \times \phi \ \right.} & { f ( \mathbf { x } ( p ) ) \geq f ( \mathbf { x } ( p - 1 ) ) } \\ { R ( p - 1 ) \times \varphi } & { { \mathrm { o t h e r w i s e } } } \end{array}  \tag{26}
$$

where Ï and $\varphi$ are two factors to reduce and enlarge R, respectively. $f ( \cdot )$ is the function used to calculate the fitness value. (From (26), the dynamic update of R depends on the fitness value between two generations. For a minimization problem, if firework x can find a better spark in generation $p$ than in generation $p - 1$ , the explosion range is enlarged aiming to search more extensively in a larger area such that more potential areas can be found, otherwise the explosion range is reduced for a fine search.

2) Selection: After the sparks are generated, it is necessary to select a suitable individual from the fireworks and the newly generated sparks to enter the next generation. Therefore, a selection strategy is designed as follows:

$$
\mathbf { x } ( p + 1 ) = \arg \operatorname* { m i n } \{ f ( \mathbf { x } ( p ) ) , f ( \mathbf { z } ( p ) ) \}\tag{27}
$$

Referring to (27), this strategy initiates by treating the firework x alongside its sparks as a subpopulation. Subsequently, the individual with the best fitness value is chosen from this combined subpopulation (comprising both the original firework and the newly generated sparks) to enter into the next iteration. The flowchart of FWA can be found in Fig. S1 of the Supplementary File.

FWA has shown excellent performance and high efficiency in solving many complex optimization problems [44], [45], [46], [47] since the work [43]. Many improved versions were designed in the past decade. For example, Meng and Tan [48] proposed FWA with multiple guided sparks in which three strategies were designed to address some deficiencies in FWA. Chen and Tan [49] designed an adaptive fast FWA that can efficiently perform large-scale black-box optimization. Fan et al. [50] incorporated an orthogonal design and an enhanced bootstrapping method into FWA, thereby proposing an improved version, and showed that the improve one was highly competitive.

## B. Motivation to Choose Fireworks Algorithm

Here, we give the explanations for selecting FWA as our base method to solve (24):

1) Special offspring generation mechanism. In FWA, each firework can generate multiple sparks (one to multiple), which is different from other algorithms, i.e., particle swarm optimizer [51], differential evolution [52] and genetic algorithm [53], in which each individual can only generate one offspring (one to one). This special offspring generation mechanism provides us with a straightforward way to devise a variable-length encoding strategy for addressing the problem presented in (24).

2) Parallel search mechanism. In FWA, the initial population is usually composed of multiple fireworks. Each firework and its own sparks can be regarded as a subpopulation, and the subpopulations are optimized in parallel without interfering with each other. This mechanism is suitable for handling multi-UAV systems.

3) Powerful search ability. FWA has proven to be highly efficient in dealing with complex optimization problems [54], [55], [56]. (24) is a mixed-integer non-convex and NP-hard problem, and FWAâs powerful search ability renders it a fitting choice for tackling (24).

## IV. PROPOSED APPROACH

This work design a joint optimization approach (JOA) to solve (24). Its goal is to minimize the total energy consumption by jointly optimizing the association between UAVs and ground-based IoT devices, deployments of UAVs, and UAV flight trajectories. Specifically, an improved k-means method (IKM) is proposed to handle association optimization, and then an improved FWA (IFWA) with a variable-length encoding strategy and population size update strategy is proposed to optimize the number and locations of footholds of each UAV. Based on the locations of footholds, the flight trajectory of each UAV is designed through a pre-computed greedy algorithm (PGA). Finally, the general framework of JOA and its time complexity are given.

## A. Association Optimization

In a multi-UAV enabled large-scale MEC system, the first thing we need to solve is how to divide large-scale IoT devices into multiple areas (clusters), and then each UAV flies to its responsible cluster to perform tasks. To this end, an improved k-means method (IKM) is designed to divide the IoT devices, as realized in Algorithm S1 of Supplementary File.

In Algorithm S1, n clusters are first initialized, i.e., $\mathcal { C } _ { i } = \emptyset$ $\forall i \in \mathcal N$ =(line 1), and the area where all IoT devices are located is divided into n equal-area clusters and the average locations of IoT devices in n equal-area clusters are calculated, which are treated as the centers of n equal-area clusters (lines 2-4). Then, iterate and update the locations of the centers.

In an iterative process, we first calculate distance $d _ { t i }$ from the t-th IoT device to the center of the i-th cluster $( \forall i \in \mathcal { N } )$ , thus obtaining n distance values (lines 7-9). Then select the smallest distance from the n distance values and determine which cluster it belongs to, and add the current t-th IoT device to this cluster (lines 10-11). The above process is repeated until the center of each cluster does not change. Finally, return $\mathcal { C } _ { i } ~ ( \forall i \in \mathcal { N } )$ containing a certain number of IoT devices as the output of Algorithm S1.

Different from the basic k-means algorithm [57] that randomly selects centers, our proposed method improves on the center selection in the initialization phase, which can speed up the clustering and reduce blindness.

Remark 2. As described above, the output of Algorithm S1 is that all IoT devices are classified into different clusters by our proposed algorithm. Then, a UAV is assigned to each cluster, which means that the deployment and flight trajectory optimization of each UAV mentioned later is based on the clustering results. Therefore, how the clusters are found has a significant impact on this optimization problem, and different clustering results can lead to different UAV deployments and flight trajectories, thereby affecting the energy consumption of the whole system. Furthermore, the impact of different clustering algorithms on the system is compared and discussed in Section V-C.

## B. Deployment Optimization

Once the associations between each UAV and IoT devices are established, each UAV flies over the responsible IoT devices to assist them in completing their tasks. In order to save energy consumption, UAVs cannot hover blindly anywhere to collect tasks and complete them in each cluster. Therefore, the locations and number of footholds of UAVs need to be optimized. To this end, IFWA with a variable-length encoding strategy and population size update strategy is presented in this section. Next, a variable-length encoding strategy is first introduced, and then a population size update strategy is presented. Finally, the general framework of IFWA for deployment optimization is given.

1) Variable-Length Encoding: Most of current intelligent optimization algorithms have some problems with individual representation when solving such problems, especially for largescale problems. Take deployment optimization as an example to illustrate this, such as a fixed-length encoding strategy [58] (as shown in Fig. 2(a)), as a popular individual representation method, where each individual represents a deployment. It means that all footholds in the i-th cluster are represented by an individual, resulting in an increase in the dimension of each individual as the number of footholds increases. For instance, if there are $k _ { i }$ footholds in the i-th cluster, then the dimension of each individual in the fixed-length encoding strategy is 3ki. At the same time, it can be found that if the population has $k _ { i }$ individuals, which means that $k _ { i }$ deployment plans exist. It leads to an increase in search difficulty and time consumption.

Furthermore, $k _ { i }$ is not fixed (increased or decreased) during the optimization process, which makes the fixed-length encoding strategy unsuitable for solving it. In order to transform high-dimensional problem into low-dimensional one and reduce the difficulty of solving it, this work proposes a variable-length encoding strategy as shown in Fig. 2(b). In the proposed strategy, it becomes evident that each individual symbolizes a foothold, and the dimension of each individual is consistently set at three. Consequently, a population, comprising a firework and its generated sparks, is regarded as a deployment plan, differing from the fixed-length encoding strategy, and its advantages are summarized as follows:

<!-- image-->  
(a)Fixed-length encoding strategy

<!-- image-->  
(b) Our proposed variable-length encoding strategy  
Fig. 2. Illustration of (a) Fixed-length encoding strategy and (b) our proposed variable-length encoding strategy at the i-th cluster.

i) Reduce the complexity to solve our concerned problem. As pointed out above, our proposed strategy transforms the problem from a $3 k _ { i }$ dimension to a 3-dimensional one, which successfully reduces the dimension of the problem and effectively reduces the difficulty of solving the problem;

ii) Avoid introducing new parameters. In a fixed length encoding strategy, the population size needs to be manually set. On the contrary, the population size in our proposed strategy is directly set to the number of footholds, thereby avoiding the introduction of new parameters and reducing the impact of manually setting parameters on algorithm performance; and

iii) Maintain dimensional consistency. In the fixed-length encoding strategy,the variable number of footholds results in an inconsistent dimensionality for each individual within the population. In our proposed strategy, the change of the number of footholds only causes the change of the population size but not the dimensionality of individuals, thus ensuring the same dimensionality of each individual and facilitating the problem solving. In addition, it provides a basis for the next population size update strategy.

2) Population Size Update: In a multi-UAV enabled largescale MEC system, the number of footholds in each cluster is also our optimization goal, and thus the number of footholds may increase, remain unchanged, or decrease during the optimization process. On the basis of our proposed variable-length encoding strategy, we design a population size update strategy to dynamically adjust the population size (i.e., the number of footholds). Its process is shown in Algorithm S2 of Supplementary File, where Bi is the current deployment at the i-th cluster, $\mathbb { E } _ { i }$ is the energy consumption under current deployment, and g is a guidance vector to be introduced later.

Algorithm S2 is composed of three cases, namely increasing footholds increase, no change, and decreasing footholds. In the stage increasing, $\mathbb { L } _ { + }$ is first assign to $\mathbb { B } _ { i }$ (line 2), and a position is randomly generated as a foothold in the i-th cluster, which is inserted to $\mathbb { L } _ { + }$ to form a new deployment $\mathbb { L } _ { + } ^ { \prime }$ (lines 3-4). Subsequently, the fitness value of $\mathbb { L } _ { + } ^ { \prime }$ is evaluated (line 5).

In the stage of no footholds change, Lâ is also first initialized as $\mathbb { B } _ { i }$ (line 6), and then a foothold $\mathbf { X } _ { * }$ is randomly taken from $\mathbb { L } _ { * }$ (line 7). Based on $\mathbf { X } _ { * } ,$ , a guidance vector g is designed to guide it in a more precise direction in the search for optimisation. Afterward, the new $\mathbf { X } _ { * } ^ { \prime }$ is used to update $\mathbf { X } _ { * }$ in $\mathbb { L } _ { * } ,$ and the new deployment is denoted as $\mathbb { L } _ { * } ^ { \prime }$ (lines 8-9). Finally, the fitness value of $\mathbb { L } _ { * } ^ { \prime }$ is evaluated (line 10).

Similar to the above, Lâ is also first initialized as $\mathbb { B } _ { i }$ in the stage of decreasing footholds (line 11). Then, a foothold is randomly removed from $ \mathbb { L } _ { - } .$ , thereby forming new deployment Lâ (line 12) and its fitness value is evaluated (line 13).

After the loop ends, $3 \left| \mathbb { B } _ { i } \right|$ deployment plans are obtained, where | Â· | represents its size. Then, the best deployment (denoted as $\mathbb { L } _ { b e s t } )$ among $3 \left| \mathbb { B } _ { i } \right|$ deployment plans is identified and its fitness value (denoted as $\mathbb { E } _ { \operatorname* { m i n } } )$ is evaluated (lines 15-18). Furthermore, $\mathbb { B } _ { i }$ and $\mathbb { E } _ { i }$ are set to $\mathbb { L } _ { b e s t }$ and $\mathbb { E } _ { \mathrm { m i n } } .$ respectively (line 19). Finally, the updated $\mathbb { B } _ { i }$ and $\mathbb { E } _ { i }$ are returned as the output.

3) IFWA for Deployment Optimization: The general framework of IFWA for deployment optimization is presented in Algorithm S3 of Supplementary File. In it, the parameters of FWA including explosion range R and two factors (Ï and Ï) to control the explosion range are first initialized (line 1). Meanwhile, an empty archive set (denoted as A) is initialized to store the abandoned deployment. Then, an initial population P that needs to satisfy the constraints in (21) is initialized as UAV deployment (line 3). Note that population initialization is a cyclic process, which means that if the initialized population does not satisfy the constraints, it continues to initialize until the constraints are satisfied. After that, the program enters an iterative process.

In the iterative process, the footholds in P are first updated by (22) and re-evaluate it (lines 5-8). Then, the explosion range of FWA is updated based on the quality of the newly generated deployment (lines 9-13). Specifically, if the newly generated deployment is better than the previous deployment, the explosion range of FWA is increased. Otherwise, it is reduced. Meanwhile, a guidance vector g is constructed based on the archive set A if A $\neq \emptyset .$ . Otherwise, g is set to a zero vector. Afterward, the updated =deployment is modified again by the proposed population size update strategy and returns a new deployment and its fitness value (line 19). Also, the archive set A is updated with the newly generated deployments (line 20). Finally, P and its fitness value are displayed as the result if stop condition is met. If not, the procedure is reiterated.

In Algorithm S3, there are two remaining issues that need further explanations: i) how to update the archive set A; and ii) how to construct guidance vector g.

For the first issue, the maximum size of A (denoted as Îº) is first set, and the new deployments generated by the proposed population size update strategy are added into A if its size does not exceed $\kappa .$ If its size exceeds Îº, it is necessary to determine whether the newly added deployment is better than the existing deployments in A. If so, remove the worst deployment from A and add the new one. If not, A remains unchanged.

Regarding the second one, the deployments in A are first sorted in ascending order based on their fitness values, and the- - sorted A is denoted as $\widetilde { \mathbb { A } }$ . The guidance vector g can be obtained as:

$$
\mathbf { g } = \frac { 1 } { \lambda | \widetilde { \mathbb { A } } | } \left( \sum _ { i = 1 } ^ { \lambda | \widetilde { \mathbb { A } } | } \widetilde { \mathbb { A } } \{ i \} - \sum _ { i = | \widetilde { \mathbb { A } } | - \lambda | \widetilde { \mathbb { A } } | + 1 } ^ { | \widetilde { \mathbb { A } } | } \widetilde { \mathbb { A } } \{ i \} \right) ,\tag{28}
$$

where Î» is a percentage to control the number of deployments selected from $\widetilde { \mathbb { A } }$ . From (28), it is evident that the construction of the guidance vector g involves using the difference between the top $\lambda | \widetilde { \mathbb { A } } |$ individuals and the bottom $\lambda | \widetilde { \mathbb { A } } |$ in $\widetilde { \mathbb { A } }$ . This approach is chosen for its ability to produce an accurate guidance vector. A mathematical explanation is given as follows:

For a better understanding, we simplify the problem by assuming that  is a deployment in $\widetilde { \mathbb { A } }$ and only has one dimension. xIts value falls in $[ \check { X } , \hat { X } ]$ . Meanwhile, we use the error bound of the irrelevant guidance vector to represent accuracy in reverse, which means that the smaller the error bound, the more accurate the generated vector.

Theorem 1: If adheres to a uniform distribution $M ( { \check { X } } , { \hat { X } } )$ xthe error bound with probability at least 1 - Ï is

$$
b _ { e } \leq \frac { \hat { X } - \check { X } } { \sqrt { 6 \lambda | \widetilde { \mathbb { A } } | \vartheta } } .\tag{29}
$$

Its detail proof is included in Supplementary File.

It can be observed from (29) that a higher Î» value results in a reduced error bound $b _ { e }$ . With a fixed $b _ { e } ,$ , an increase in Î» leads to a decrease in Ï, thereby increasing 1 - Ï. It implies that a larger Î» enhances the likelihood of (28) yielding a more accurate guidance vector.

## C. Flight Trajectory Optimization

Based on the footholds in each cluster given by deployment optimization, each UAV needs to fly to each foothold in each cluster to perform tasks. How to minimize the flight distance of UAVs while ensuring the completion of their own tasks is a challenge. To this end, this work first considers flight trajectory optimization as a traveling salesman problem (TSP), and then proposes a pre-computed greedy algorithm (PGA) to handle it, which is realized in Algorithm S4 of Supplementary File.

From Algorithm S4, it can be seen that a set P is initialized and used to store paths (line 1), and the distances from each foothold to the remaining footholds are calculated (denoted as D) (lines 2). Then enter a pre-computed process (lines 3-16). Specifically, D is updated by calculating the distance between each foothold and the next Îµ footholds via a greedy algorithm, and Îµ is set to 5 in this work. Afterward, the process enters the iteration phase.

During the iteration stage, the i-th foothold is initially included in ${ \mathcal P } ,$ , followed by extracting the i-th row from ${ \mathcal { D } } ,$ , labeled as $\mathcal { D } _ { m }$ (lines 18-19). Then, the process enters greedy selection based on D. First, $\mathcal { D } _ { m }$ is arranged in ascending sequence and the cycle starts (lines 21-22). Second, we need to determine whether index j -th foothold belongs to P. If not, index j -th foothold ( )is added into P. Meanwhile, the index $( j )$ ( )-th row is taken from D to update $\mathcal { D } _ { m }$ , and $j$ ( )is assigned as the size of P in order to reach the condition that is to exit this loop (lines 23-27). Third, the distance of the current flight trajectory $\mathcal { P }$ is calculated and stored in $\mathcal { D } _ { \mathcal { P } }$ , and P is stored in $P a t h .$ , as well as $\mathcal { P }$ is reinitialized to null (lines 30-32). Finally, the minimum value in $\mathcal { D } _ { \mathcal { P } }$ and its corresponding flight trajectory are returned as the output.

D. Computational Complexity of Joint Optimization Approach (JOA)

The general framework of JOA is realized via Algorithm 1. In it, the number of UAVs n and that of IoT devices m are first set, and FWAâs parameters are initialized (line 1). After that m IoT devices are divided into n clusters by Algorithm S1 (line 2). Based on the clustering results, it enters the optimization process for deployments and flight trajectories of UAVs. For each cluster (UAV), it first randomly selects some from all the footholds in a cluster to compose an initial deployment that satisfies the constraints of (21) (line 4). Then it updates the deployment according to (22) while evaluating the energy consumption under the new deployment (lines 6-7). The explosion range is updated based on whether the deployment has improved or not, and the better deployment is retained (lines 8-9). Based on this, the proposed population size updating strategy is utilized to dynamically adjust the deployment (line 10). Algorithm S4 is then utilized to find the optimal flight trajectory on the new deployment (line 11). It repeats the process until the stop condition is reached (e.g., the maximum number of evaluations). Note that n clusters are processed in parallel due to the parallel mechanism of FWA.

JOA can be divided into three parts, i.e., association (Algorithm S1), deployment (Algorithm S3) and flight trajectory optimization (Algorithm S4). Algorithm S1 requires nm time consumption. Algorithm S3 includes using FWA and population size update strategies to update deployments, as well as sorting the updated deployments, requiring k, 3k and klog k time consumption, respectively. We assume that the number of footholds in each cluster is k. Algorithm S3âs computational complexity is 4k + k logk. Algorithm S4 takes $3 k ^ { 2 }$ of time to complete. If the upper bound of iterations is designated to ${ \widehat { I } } ,$ the computational complexity for JOA stands at $O ( n m + \widehat { I } ( 4 k + k \log k + 3 k ^ { 2 } ) )$ or simply, $O ( n m + \widehat { I } k ^ { 2 } )$ .

Algorithm 1: General Framework of JOA.   
Input:n, m   
Output:total energy consumption   
1: Initialize the parameters of FWA   
2: Divide m IoT devices into n clusters by Algorithm S1   
3: for each cluster do   
4: Initialize a deployment that satisfies the constraints   
in (21)   
5: repeat   
6: Generate new deployment by (22)   
7: Evaluate the fitness value of the newly generated   
deployment   
8: Update the explosion range by (23)   
9: Retain the better deployment by comparing their   
fitness values   
10: Update the deployment by the proposed population   
size update strategy   
11: Obtain the flight trajectory by Algorithm S4   
12: until Stop condition is met   
13: end for

## V. EXPERIMENTS AND ANALYSES

In this section, the following experiments are carried out with the following goals:

- investigate the effect of Î» in (28); and

assess the performance of the introduced variable-length encoding strategy, IKM, PGA, and multi-UAV enabled large-scale MEC system.

The mean results of 30 runs are reported, and each experiment is run on 10 different instances. The termination condition, i.e., the maximum number of evaluations, is set to $1 0 ^ { 4 }$ . Table S1 of Supplementary File lists the detailed parameter settings in our system.

The Wilcoxon rank-sum test and Friedman ranking (Ft) [59] are employed to establish the significant superiority of our proposed algorithms over their peers, where â+â, â-â and $^ { 6 6 } { \approx } ^ { 9 }$ indicates that ours are better, worse, or approximately the same to their peers. Each experiment is conducted using MATLAB (R2022b) on a Windows 10 (64-bit) computer equipped with 32 GB of RAM.

## A. Sensitivity to Î»

In (28), Î» is an important parameter that affects the construction of the guidance vector, and a suitable selection can improve the performance of the algorithm. In order to specifically verify its sensitivity, it is set to 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 and 1.0. Note that Î» 1.0 means that the proposed JOA without the guidance vector since $\begin{array} { r } { { \bf g } = \vec { 0 } . } \end{array}$ . Table II enumerates the results = 0of the Friedman ranking for varying values, while Table S2 in the Supplementary File lists the mean energy consumption in detail on ten instances.

TABLE II  
RESULTS OF $F _ { t }$ WHEN Î» TAKES DIFFERENT VALUES
<table><tr><td rowspan=1 colspan=1>å¥</td><td rowspan=1 colspan=1>0.1</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1>Ft</td><td rowspan=1 colspan=1>5.3000</td><td rowspan=1 colspan=1>4.8000</td><td rowspan=1 colspan=1>4.6000</td><td rowspan=1 colspan=1>5.6000</td><td rowspan=1 colspan=1>4.3000</td></tr><tr><td rowspan=1 colspan=1>å¥</td><td rowspan=1 colspan=1>0.6</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>0.9</td><td rowspan=1 colspan=1>1.0</td></tr><tr><td rowspan=1 colspan=1>Ft</td><td rowspan=1 colspan=1>5.2000</td><td rowspan=1 colspan=1>6.3000</td><td rowspan=1 colspan=1>5.2000</td><td rowspan=1 colspan=1>6.7000</td><td rowspan=1 colspan=1>7.0000</td></tr></table>

<!-- image-->  
Fig. 3. Results of JOA and JOAW on ten instances in terms of mean energy consumption.

From Table II, it can be seen that the proposed algorithm has the best $F _ { t }$ when Î± is set to 0.5, which means that $\lambda = 0 . 5$ is the most suitable selection among them, and thus $\lambda = 0 . 5$ is used next.

## B. Effectiveness of Proposed Variable-Length Encoding Strategy

To demonstrate the effectiveness of the proposed variablelength encoding strategy, a comparison is made with the fixedlength encoding approach. In this comparison, the proposed JOA whose encoding strategy is replaced with the latter is denoted as JOAW. Their results on ten instances are shown in Fig. 3.

It can be observed from Fig. 3 that the proposed JOA has smaller results than JOAW on all ten instances. Meanwhile, we can find that the energy consumption of JOAW increases faster than JOA with the increase of IoT devices.

Besides, the mean time consumption of the above two methods over ten instances is also compared, and the results are shown in Fig. 4. From it, we can see that the proposed JOA takes less time than JOAW. It indicates that our developed variable-length encoding strategy can save more time. The reason is that the number of footholds at each cluster decreases with iteration, while the dimension of an individual remains unchanged in a fixed-length encoding strategy.

Therefore, we conclude that our proposed strategy can save more energy consumption with less computing time on ten instances than the fixed-length encoding strategy.

## C. Effectiveness of Proposed Improved K-Means Method

In this section, the effectiveness of the proposed improved k-means method (IKM) is validated. three benchmark methods, namely empty circles based k-means method (ECKM) [60], homogeneous manifolds based k-means method (HMKM) [61], and the basic k-means method [62], are selected to compare with ours. ECKM uses the computational geometry to act as the initialization method of cluster centers, and HMKM applies the homogeneous manifolds to learn the number of clusters and select the initial centers. In all compared methods, the ECKM, HMKM, and basic k-means method are used to replace the IKM in JOA, respectively, which are denoted as JOA-EC, JOA-HM, and JOA-B. The results of mean energy consumption are shown in Fig. 5.

<!-- image-->

Fig. 4. Results of JOA and JOAW on ten instances in terms of mean time consumption.  
<!-- image-->  
Fig. 5. Mean energy consumption with JOA, JOA-EC, JOA-HM, and JOA-B on ten instances.

From Fig. 5, it can be intuitively and clearly seen that the proposed JOA has better results than its peers on all instances, which means that IKM is able to accurately cluster all IoT devices, thereby saving more energy in deployment and flight trajectory optimization. JOA-HM is slightly better than JOA-EC on nine instances, worse than it on one instance, while they are all better than JOA-B, which means that IKM, HMKM, and ECKM are more effective than the basic one when dealing with association optimization. Meanwhile, we also find that as the number of IoT devices increases, the mean energy consumption of our proposed IKM on ten instances increases uniformly, while its competitor increase very rapidly. It indicates that our proposed IKM is more stable for solving association optimization.

## D. Effectiveness of Proposed Pre-Computed Greedy Algorithm

In this section, the effectiveness of the proposed pre-computed greedy algorithm (PGA), which is used to optimize the flight trajectories of multiple UAVs, is studied. Four benchmark methods are selected to compare with our proposed PGA: 1) iterated greedy algorithm (IGA) [63], 2) Tabu Search (TS) [64], 3) improved ant colony optimization (IACO) [65] where heterogeneous population automation strategy, smoothing technique, and differential information are applied to improve its performance, and 4) improved simulated annealing (ISA) [66] where a list-based temperature cooling schedule and three local search operators are used to accelerate the convergence. For a fair comparison, their parameter settings follow their references [63], [64], [65], [66], and the upper bound of iterations is same as that of footholds. Their results are reported in Table III.

TABLE III  
MEAN ENERGY CONSUMPTION WHEN PGA, IGA, TS, IACO AND ISA ARE USED TO OPTIMIZE UAV FLIGHT TRAJECTORIES WHERE THE BOLD VALUE MEANS THE BEST RESULT
<table><tr><td>m</td><td>PGA</td><td>IGA</td><td>TS</td><td>IACO</td><td>ISA</td></tr><tr><td>100</td><td>1.1189E+06</td><td>1.2363E+06</td><td>1.7967E+06</td><td>1.3552E+06</td><td>1.3477E+06</td></tr><tr><td>200</td><td>1.5488E+06</td><td>1.6928E+06</td><td>1.8762E+06</td><td>1.8474E+06</td><td>1.7959E+06</td></tr><tr><td>300</td><td>1.9012E+06</td><td>2.1151E+06</td><td>2.5689E+06</td><td>2.3333E+06</td><td>2.2471E+06</td></tr><tr><td>400</td><td>2.1363E+06</td><td>2.3414E+06</td><td>3.1096E+06</td><td>2.6135E+06</td><td>2.5549E+06</td></tr><tr><td>500</td><td>2.3304E+06</td><td>2.5509E+06</td><td>3.6611E+06</td><td>2.8630E+06</td><td>2.8342E+06</td></tr><tr><td>600</td><td>2.6589E+06</td><td>2.8532E+06</td><td>4.3260E+06</td><td>3.2340E+06</td><td>3.0807E+06</td></tr><tr><td>700</td><td>2.8574E+06</td><td>3.0950E+06</td><td>5.1138E+06</td><td>3.5243E+06</td><td>3.3607E+06</td></tr><tr><td>800</td><td>3.0503E+06</td><td>3.2874E+06</td><td>5.7554E+06</td><td>3.7106E+06</td><td>3.5992E+06</td></tr><tr><td>900</td><td>3.1924E+06</td><td>3.4753E+06</td><td>6.1974E+06</td><td>3.9794E+06</td><td>3.7995E+06</td></tr><tr><td>1000</td><td>3.4157E+06</td><td>3.6305E+06</td><td>7.0410E+06</td><td>4.2360E+06</td><td>4.1461E+06</td></tr><tr><td>Ft</td><td>1.0000</td><td>2.0000</td><td>5.0000</td><td>4.0000</td><td>3.0000</td></tr><tr><td>+/~/-</td><td>N/A</td><td>10/0/0</td><td>10/0/0</td><td>10/0/0</td><td>10/0/0</td></tr></table>

The bold value means the best result.

<!-- image-->  
Fig. 6. Results of PGA, IGA, TS, IACO and ISA on ten instances in terms of mean computing time. Note that the vertical axis numbers represent the logarithm of mean computing time.

From Table III, it can be seen that the proposed PGA is the best on ten instances among them in terms of mean energy consumption, and thus $F _ { t }$ ranks the first. IGA is the second best. TS is better than IACO and ISA on the first instance, while it is worse than them on other instances. IACO and ISA are comparable in terms of their results. Judging from $F _ { t } ,$ , ISA ranks higher than IACO. The results of Wilcoxon rank-sum test are given in the bottom of Table III. It shows that the proposed PGA can provide better mean energy consumption in 10, 10, 10 and 10 instances out of 10 when comparing with IGA, TS, IACO and ISA, meaning that PGA is significantly better than its peers.

Their mean computing time is reported, and the results are shown in Fig. 6. IGA spends the least computing time among them. Our proposed PGA only spends more computing time than IGA, while it has less computing time than other peers. The reason is that the pre-computed process takes some time, resulting in an increase in computing time. IACO requires the most time. TS is better than ISA in terms of mean computing time.

TABLE IV  
MEAN ENERGY CONSUMPTION WITH JOA, IDA, IDE, DEVIPS, IRP AND RRR ON TEN INSTANCES WHERE THE BOLD VALUE MEANS THE BEST RESULT
<table><tr><td>m</td><td>JOA</td><td>IDA</td><td>IDE</td><td>DEVIPS</td><td>IRP</td><td>RRR</td></tr><tr><td>100</td><td>6.3502E+08</td><td>7.6203E+08</td><td>8.5728E+08</td><td>7.7520E+08</td><td>9.0220E+08</td><td>9.6176E+08</td></tr><tr><td>200</td><td>3.8143E+09</td><td> $4 . 5 7 7 2 \mathrm { E } \mathrm { + } 0 9$ </td><td>5.1493E+09</td><td> $5 . 2 1 4 9 \mathrm { E } { + } 0 9$ </td><td>5.9778E+09</td><td>6.5939E+09</td></tr><tr><td>300</td><td>1.1688E+10</td><td> $1 . 4 0 2 6 \mathrm { E } { + } 1 0$ </td><td>1.5780E+10</td><td> $1 . 6 4 4 2 \mathrm { E } { + } 1 0$ </td><td> $1 . 8 7 8 0 \mathrm { E } { + } 1 0$ </td><td>2.1738E+10</td></tr><tr><td>400</td><td>2.8184E+10</td><td> $3 . 3 8 2 1 \mathrm { E } { + } 1 0$ </td><td>3.8049E+10</td><td> $4 . 1 0 7 9 \mathrm { E } { + } 1 0$ </td><td> $4 . 6 7 1 6 \mathrm { E } { + } 1 0$ </td><td>5.7026E+10</td></tr><tr><td>500</td><td>5.3254E+10</td><td>6.3905E+10</td><td>7.1893E+10</td><td> $8 . 3 1 6 1 \mathrm { E } \mathrm { + } 1 0$ </td><td>9.3812E+10</td><td>1.2219E+11</td></tr><tr><td>600</td><td>9.1251E+10</td><td>1.0950E+11</td><td>1.2319E+11</td><td>1.4833E+11</td><td>1.6658E+11</td><td>2.1768E+11</td></tr><tr><td>700</td><td>1.4065E+11</td><td>1.6879E+11</td><td>1.8989E+11</td><td>2.5076E+11</td><td>2.7889E+11</td><td>3.6127E+11</td></tr><tr><td>800</td><td>2.2597E+11</td><td>2.7117E+11</td><td>3.0507E+11</td><td>4.0572E+11</td><td>4.5091E+11</td><td>5.9710E+11</td></tr><tr><td>900</td><td>3.4370E+11</td><td>4.1245E+11</td><td>4.6400E+11</td><td>6.4285E+11</td><td>7.1159E+11</td><td>9.5863E+11</td></tr><tr><td>1000</td><td>4.4130E+11</td><td>5.2956E+11</td><td>5.9576E+11</td><td>8.6329E+11</td><td>9.5155E+11</td><td>1.2806E+12</td></tr><tr><td> $\overline { { F _ { t } } }$ </td><td>1.0000</td><td>2.0000</td><td>3.1000</td><td>3.9000</td><td>5.0000</td><td>6.0000</td></tr><tr><td>+/~/-</td><td>N/A</td><td>10/0/0</td><td>10/0/0</td><td>10/0/0</td><td>10/0/0</td><td>10/0/0</td></tr></table>

The bold value means the best result.

Even though the proposed PGA is not the best in terms of computing time, it can optimize flight trajectories of multiple UAVs with the least energy consumption and accepted computing time.

## E. Effectiveness of Multi-UAV Enabled MEC System

This work proposes a joint optimization approach (JOA) by jointly optimizing the association between UAVs and IoT devices, UAV deployments, and UAV flight trajectories. To validate its effectiveness, the proposed JOA is compared against the following benchmark approaches:

1) IDA [9]: It introduces an enhanced dandelion algorithm with two mutation strategies for optimizing deployment, along with an iterated greedy algorithm for refining flight trajectory. Additionally, our proposed IKM is integrated into it for association optimization.

2) IDE [67]: It proposes an improved differential evolution algorithm to optimize the deployment, and a lowcomplexity greedy method is used to optimize the flight trajectory. IKM is embedded into it to perform association optimization.

3) DEVIPS [68]: It designs a variable population differential evolution algorithm to optimize the deployment. We embed IKM and PGA into it to optimize association and flight trajectory.

4) IKM+Rand+PGA (IRP): It uses the random strategy to replace IFWA in JOA, which means that the deployment is randomly generated.

5) Rand+Rand+Rand (RRR): It uses a random strategy to optimize the association, deployment and flight trajectory.

The results are listed in Table IV. It highlights that JOA has the best energy consumption and the top ranking among them in terms of $F _ { t } ,$ , followed by IDA and IDE. IDE and DEVIPS are comparable, and they are better than IRP and RRR. RRR has poor performance on ten instances, and ranks the end. The results of Wilcoxon rank-sum test, included at the end of

Table IV, confirm JOAâs superior performance in all ten instances compared to its peers.

In summary, it can be concluded that our proposed JOA can assist the MEC system in realizing association, deployment and flight trajectory optimization for UAVs such that the least energy consumption of the entire.

## F. Discussion

This work jointly optimizes the UAVsâ associations with ground-based IoT devices, deployments, and flight trajectories of multiple UAVs to minimize energy consumption in large-scale edge computing system. It also proposes a joint optimization approach to solve it, consisting of an improved k-means method, an improved FWA, and a pre-computed greedy algorithm. Empirical evaluations on ten large-scale instances demonstrate that the proposed methods outperform existing methods across multiple performance metrics. Specifically, improved k-means method can save more energy consumption compared to other state-ofthe-art k-means according to Fig. 6. In terms of Figs. 3 and 4, improved FWA can obtain lower energy consumption and time consumption than its peers. The pre-computed greedy algorithm can get better flight trajectory with low energy consumption and time consumption than its peers. From Table IV, we conclude that the proposed joint optimization approach is the best among all compared approaches.

Notably, the proposed JOA achieves state-of-the-art performance on 10 large-scale instances in comparison with its peers. The main reasons for this are as follows: 1) the improved k-means method gives an accurate clustering of ground-based IoT devices, which allows the UAV responsible for this cluster to traverse all points using the minimal energy consumption; 2) based on the clustering results, each UAV utilizes the proposed encoding strategy and population update strategy of FWA to find a smaller number and locations of footholds; and 3) a precomputed greedy algorithm is used to find a flight trajectory with the shortest distance based on the given locations of footholds. The three algorithms interact and complement each other to form a powerful optimization framework, which in turn yields the best results in terms of both energy and time consumption.

Although the proposed method achieves significant improvements over its existing peers, it is not without limitations, e.g., all the parameters need to be set manually, which can be timeconsuming.

## VI. CONCLUSION

This work studies a multi-UAV-enabled large-scale MEC system. Its goal is to minimize energy consumption by jointly optimizing the association, deployments and flight trajectories of multiple UAVs. A joint optimization approach (JOA) is proposed to do so. Specifically, an improved k-means method is first proposed to optimize the association, and then an improved fireworks algorithm consisting of a variable-length encoding strategy and population size update strategy is designed to achieve the best deployment of UAVs. For flight trajectories, we propose a pre-computed greedy algorithm to plan them. The experimental results on ten instances indicate that our proposed JOA can save more energy consumption than its compared ones.

Our future work plans to design an adaptive strategy to allow the manually set parameters in the system to be adaptively adjusted according to the environment and evolutionary progress. The optimal height of UAVs in the system is also worth studying. Also, it is interesting to use our proposed algorithms to solve other optimization problems [69], [70], [71].

## REFERENCES

[1] G. Fortino, C. Savaglio, G. Spezzano, and M. Zhou, âInternet of Things as system of systems: A review of methodologies, frameworks, platforms, and tools,â IEEE Trans. Syst. Man Cybern. Syst., vol. 51, no. 1, pp. 223â236, Jan. 2021.

[2] K. Zhu, L. Li, Y. Xu, T. Zhang, and L. Zhou, âMulti-connection based scalable video streaming in UDNs: A multi-agent multi-armed bandit approach,â IEEE Trans. Wirel. Commun., vol. 21, no. 2, pp. 1156â1169, Feb. 2022.

[3] A. A. Zaidan and B. B. Zaidan, âA review on intelligent process for smart home applications based on IoT: Coherent taxonomy, motivation, open challenges, and recommendations,â Artif. Intell. Rev., vol. 53, no. 1, pp. 141â165, 2020.

[4] P. Arthurs, L. Gillam, P. Krause, N. Wang, K. Halder, and A. Mouzakitis, âA taxonomy and survey of edge cloud computing for intelligent transportation systems and connected vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 6206â6221, Jul. 2022.

[5] J. Cao, âSmart application of 5G mobile edge computing with iot: Future insight of autonomous driving technologies,â in Proc. 3rd Int. Conf. Big Data Eng. Technol., Singapore, 2021, pp. 99â104.

[6] S. Kontogiannis and G. Kokkonis, âProposed fuzzy real-time haptics protocol carrying haptic data and multisensory streams,â Int. J. Comput. Commun. Control, vol. 15, no. 4, 2020, Art. no. 3842.

[7] H. Zhang, M. Uddin, F. Hao, S. Mukherjee, and P. Mohapatra, âMAIDE: Augmented reality (AR)-facilitated mobile system for onboarding of Internet of Things (IoT) devices at ease,â ACM Trans. Internet Things, vol. 3, no. 2, pp. 16:1â16:21, 2022.

[8] N. Abbas, Y. Zhang, A. Taherkordi, and T. Skeie, âMobile edge computing: A survey,â IEEE Internet Things J., vol. 5, no. 1, pp. 450â465, Feb. 2018.

[9] S. Han, K. Zhu, M. Zhou, and X. Liu, âJoint deployment optimization and flight trajectory planning for UAV assisted IoT data collection: A bilevel optimization approach,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 11, pp. 21492â21504, Nov. 2022.

[10] M. M. Azari, G. Geraci, A. GarcÃ­a-RodrÃ­guez, and S. Pollin, âUAV-to-UAV communications in cellular networks,â IEEE Trans. Wireless. Commun., vol. 19, no. 9, pp. 6130â6144, Sep. 2020.

[11] J. Li, D. H. Ye, M. Kolsch, J. P. Wachs, and C. A. Bouman, âFast and robust UAV to UAV detection and tracking from video,â IEEE Trans. Emerg. Top. Comput., vol. 10, no. 3, pp. 1519â1531, Third Quarter 2022.

[12] K. Liu and J. Zheng, âUAV trajectory optimization for time-constrained data collection in UAV-enabled environmental monitoring systems,â IEEE Internet Things J., vol. 9, no. 23, pp. 24300â24314, Dec. 2022.

[13] H. Hao, C. Xu, W. Zhang, S. Yang, and G.-M. Muntean, âJoint task offloading, resource allocation, and trajectory design for multi-UAV cooperative edge computing with task priority,â IEEE Trans. Mobile Comput., early access, Jan. 5, 2024, doi: 10.1109/TMC.2024.3350078.

[14] Z. Bai, Y. Lin, Y. Cao, and W. Wang, âDelay-aware cooperative task offloading for multi-UAV enabled edge-cloud computing,â IEEE Trans. Mob. Comput., vol. 23, no. 2, pp. 1034â1049, Feb. 2024.

[15] L. Wang, H. Zhang, S. Guo, and D. Yuan, âDeployment and association of multiple UAVs in UAV-assisted cellular networks with the knowledge of statistical user position,â IEEE Trans. Wirel. Commun., vol. 21, no. 8, pp. 6553â6567, Aug. 2022.

[16] H. El Hammouti, M. Benjillali, B. Shihada, and M.-S. Alouini, âLearnas-you-fly: A distributed algorithm for joint 3 D placement and user association in multi-UAVs networks,â IEEE Trans. Wirel. Commun., vol. 18, no. 12, pp. 5831â5844, Dec. 2019.

[17] H. E. Hammouti, D. Hamza, B. Shihada, M. Alouini, and J. S. Shamma, âThe optimal and the greedy: Drone association and positioning schemes for internet of UAVs,â IEEE Internet Things J., vol. 8, no. 18, pp. 14066â14079, Sep. 2021.

[18] X. Xi, X. Cao, P. Yang, J. Chen, T. Q. S. Quek, and D. Wu, âJoint user association and UAV location optimization for UAV-aided communications,â IEEE Wireless Commun. Lett., vol. 8, no. 6, pp. 1688â1691, Dec. 2019.

[19] Y. Qian, F. Wang, J. Li, L. Shi, K. Cai, and F. Shu, âUser association and path planning for UAV-aided mobile edge computing with energy restriction,â IEEE Wireless Commun. Lett., vol. 8, no. 5, pp. 1312â1315, Oct. 2019.

[20] X. Guan, Y. Huang, C. Dong, and Q. Wu, âUser association and power allocation for UAV-assisted networks: A distributed reinforcement learning approach,â China Commun., vol. 17, no. 12, pp. 110â122, 2020.

[21] C. Fu, M. Ku, Y. Chen, and T. Q. S. Quek, âUAV trajectory, user association, and power control for multi-UAV-enabled energy-harvesting communications: Offline design and online reinforcement learning,â IEEE Internet Things J., vol. 11, no. 6, pp. 9781â9800, Mar. 2024.

[22] Z. Han, T. Zhou, T. Xu, and H. Hu, âJoint user association and deployment optimization for delay-minimized UAV-aided MEC networks,â IEEE Wireless Commun. Lett., vol. 12, no. 10, pp. 1791â1795, Oct. 2023.

[23] X. Deng, J. Zhao, Z. Kuang, X. Chen, Q. Guo, and F. Tang, âComputation efficiency maximization in multi-UAV-enabled mobile edge computing systems based on 3D deployment optimization,â IEEE Trans. Emerg. Top. Comput., vol. 11, no. 3, pp. 778â790, Third Quarter 2023.

[24] Z. Liao, Y. Ma, J. Huang, and J. Wang, âEnergy-aware 3D-deployment of UAV for IoV with highway interchange,â IEEE Trans. Commun., vol. 71, no. 3, pp. 1536â1548, Mar. 2023.

[25] N. Lin, Y. Liu, L. Zhao, D. O. Wu, and Y. Wang, âAn adaptive UAV deployment scheme for emergency networking,â IEEE Trans. Wirel. Commun., vol. 21, no. 4, pp. 2383â2398, Apr. 2022.

[26] C.-C. Lai, A.-H. Tsai, C.-W. Ting, K.-H. Lin, J.-C. Ling, and C.-E. Tsai, âInterference-aware deployment for maximizing user satisfaction in multi-UAV wireless networks,â IEEE Wireless Commun. Lett., vol. 12, no. 7, pp. 1189â1193, Jul. 2023.

[27] Z. Wang and L. Duan, âChase or wait: Dynamic UAV deployment to learn and catch time-varying user activities,â IEEE Trans. Mob. Comput., vol. 22, no. 3, pp. 1369â1383, Mar. 2023.

[28] X. Zhou, S. Yan, D. W. K. Ng, and R. Schober, âThree-dimensional placement and transmit power design for UAV covert communications,â IEEE Trans. Veh. Technol., vol. 70, no. 12, pp. 13424â13429, Dec. 2021.

[29] X. Zhang and L. Duan, âFast deployment of UAV networks for optimal wireless coverage,â IEEE Trans. Mob. Comput., vol. 18, no. 3, pp. 588â601, Mar. 2019.

[30] X. Zhu, L. Zhai, N. Li, Y. Li, and F. Yang, âMulti-objective deployment optimization of UAVS for energy-efficient wireless coverage,â IEEE Trans. Commun., vol. 72, no. 6, pp. 3587â3601, Jun. 2024.

[31] C. Sun, X. Xiong, Z. Zhai, W. Ni, T. Ohtsuki, and X. Wang, âMax-min fair 3 D trajectory design and transmission scheduling for solar-powered fixed-wing UAV-assisted data collection,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8650â8665, Dec. 2023.

[32] S. Gong, M. Wang, B. Gu, W. Zhang, D. T. Hoang, and D. Niyato, âBayesian optimization enhanced deep reinforcement learning for trajectory planning and network formation in multi-UAV networks,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 10933â10948, Aug. 2023.

[33] J. Li, C. Yi, J. Chen, K. Zhu, and J. Cai, âJoint trajectory planning, application placement and energy renewal for UAV-assisted MEC: A triple-learner based approach,â IEEE Internet Things J., vol. 10, no. 15, pp. 13622â13636, Aug. 2023.

[34] B. Li, W. Xie, Y. Ye, L. Liu, and Z. Fei, âFlexEdge: Digital twin-enabled task offloading for UAV-aided vehicular edge computing,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 11086â11091, Aug. 2023.

[35] J. Liu, Z. Xu, and Z. Wen, âJoint data transmission and trajectory optimization in UAV-enabled wireless powered mobile edge learning systems,â IEEE Trans. Veh. Technol., vol. 72, no. 9, pp. 11617â11630, Sep. 2023.

[36] A. Andreou, C. X. Mavromoustakis, J. M. Batalla, E. K. Markakis, G. Mastorakis, and S. Mumtaz, âUAV trajectory optimisation in smart cities using modified a\* algorithm combined with haversine and vincenty formulas,â IEEE Trans. Veh. Technol., vol. 72, no. 8, pp. 9757â9769, Aug. 2023.

[37] K. Wang, X. Zhang, L. Duan, and J. Tie, âMulti-UAV cooperative trajectory for servicing dynamic demands and charging battery,â IEEE Trans. Mob. Comput., vol. 22, no. 3, pp. 1599â1614, Mar. 2023.

[38] H. Hu, Z. Chen, F. Zhou, R. Q. Hu, and H. Zhu, âComputation-efficient grouping, trajectory, and resource allocation for UAV swarm-assisted aerial-ground collaborative computing networks,â IEEE Internet Things J., vol. 11, no. 7, pp. 12510â12525, Apr. 2024.

[39] X. Li, Y. Qin, J. Huo, and H. Wei, âComputation offloading and trajectory planning of multi-UAV-enabled MEC: A knowledge-assisted multiagent reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 73, no. 5, pp. 7077â7088, May 2024.

[40] C. Liu, Y. Guo, N. Li, and X. Song, âAoI-minimal task assignment and trajectory optimization in multi-UAV-assisted IoT networks,â IEEE Internet Things J., vol. 9, no. 21, pp. 21777â21791, Nov. 2022.

[41] Y. Wang, Z. Ru, K. Wang, and P. Huang, âJoint deployment and task scheduling optimization for large-scale mobile users in multi-UAVenabled mobile edge computing,â IEEE Trans. Cybern., vol. 50, no. 9, pp. 3984â3997, Sep. 2020.

[42] N. Lin, L. Fu, L. Zhao, G. Min, A. Al-Dubai, and H. Gacanin, âA novel multimodal collaborative drone-assisted VANET networking model,â IEEE Trans. Wireless Commun., vol. 19, no. 7, pp. 4919â4933, Jul. 2020.

[43] Y. Tan, C. Yu, S. Zheng, and K. Ding, âIntroduction to fireworks algorithm,â Int. J. Swarm Intell. Res., vol. 4, no. 4, pp. 39â70, 2013.

[44] S. Han et al., âA novel multiobjective fireworks algorithm and its applications to imbalanced distance minimization problems,â IEEE CAA J. Autom. Sinica, vol. 9, no. 8, pp. 1476â1489, Aug. 2022.

[45] W. Wei, H. Ouyang, C. Zhang, S. Li, L. Fu, and L. Gao, âDynamic collaborative fireworks algorithm and its applications in robust pole assignment optimization,â Appl. Soft Comput., vol. 100, 2021, Art. no. 106999.

[46] J. Yu, J. Guo, X. Zhang, C. Zhou, T. Xie, and X. Han, âA novel tent-levy fireworks algorithm for the UAV task allocation problem under uncertain environment,â IEEE Access, vol. 10, pp. 102373â102385, 2022.

[47] S. Han, K. Zhu, M. Zhou, H. Alhumade, and A. Abusorrah, âLocating multiple equivalent feature subsets in feature selection for imbalanced classification,â IEEE Trans. Knowl. Data Eng., vol. 35, no. 9, pp. 9195â9209, Sep. 2023.

[48] X. Meng and Y. Tan, âMulti-guiding spark fireworks algorithm: Solving multimodal functions by multiple guiding sparks in fireworks algorithm,â Swarm Evol. Comput., vol. 85, 2024, Art. no. 101458.

[49] M. Chen and Y. Tan, âSF-FWA: A self-adaptive fast fireworks algorithm for effective large-scale optimization,â Swarm Evol. Comput., vol. 80, 2023, Art. no. 101314.

[50] M. Fan, Y. Zhou, M. Han, X. Zhao, L. Ye, and Y. Tan, âOLFWA: A novel fireworks algorithm with new explosion operator and two stages information utilization,â Inf. Sci., vol. 649, 2023, Art. no. 119609.

[51] K. Chen, B. Xue, M. Zhang, and F. Zhou, âNovel chaotic grouping particle swarm optimization with a dynamic regrouping strategy for solving numerical optimization tasks,â Knowl. Based Syst., vol. 194, 2020, Art. no. 105568.

[52] S. Gupta, S. Singh, R. Su, S. Gao, and J. C. Bansal, âMultiple elite individual guided piecewise search-based differential evolution,â IEEE CAA J. Autom. Sinica, vol. 10, no. 1, pp. 135â158, Jan. 2023.

[53] G. Acampora, R. Schiattarella, and A. Vitiello, âUsing quantum amplitude amplification in genetic algorithms,â Expert Syst. Appl., vol. 209, 2022, Art. no. 118203.

[54] Y. Gao, H. Wu, and W. Wang, âA hybrid ant colony optimization with fireworks algorithm to solve capacitated vehicle routing problem,â Appl. Intell., vol. 53, no. 6, pp. 7326â7342, 2023.

[55] A. M. Yadav, K. N. Tripathi, and S. C. Sharma, âAn enhanced multiobjective fireworks algorithm for task scheduling in fog computing environment,â Clust. Comput., vol. 25, no. 2, pp. 983â998, 2022.

[56] X. Liu and X. Qin, âA neighborhood information utilization fireworks algorithm and its application to traffic flow prediction,â Expert Syst. Appl., vol. 183, 2021, Art. no. 115189.

[57] A. M. Ikotun, A. E. Ezugwu, L. Abualigah, B. Abuhaija, and H. Jia, âKmeans clustering algorithms: A comprehensive review, variants analysis, and advances in the era of Big Data,â Inf. Sci., vol. 622, pp. 178â210, 2023.

[58] Y. Zhang, Y. Gong, T. Gu, Y. Li, and J. Zhang, âFlexible genetic algorithm: A simple and generic approach to node placement problems,â Appl. Soft Comput., vol. 52, pp. 457â470, 2017.

[59] S. Han, K. Zhu, M. Zhou, and X. Liu, âEvolutionary weighted broad learning and its application to fault diagnosis in self-organizing cellular networks,â IEEE Trans. Cybern., vol. 53, no. 5, pp. 3035â3047, May 2023.

[60] T. K. Biswas, K. Giri, and S. Roy, âECKM: An improved k-means clustering based on computational geometry,â Expert Syst. Appl., vol. 212, 2023, Art. no. 118862.

[61] C. Tan, H. Zhao, and H. Ding, âStatistical initialization of intrinsic kmeans clustering on homogeneous manifolds,â Appl. Intell., vol. 53, no. 5, pp. 4959â4978, 2023.

[62] C. J. Swinney and J. C. Woods, âK-means clustering approach to UAS classification via graphical signal representation of radio frequency signals for air traffic early warning,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 12, pp. 24957â24965, Dec. 2022.

[63] Z. Zhao, M. Zhou, and S. Liu, âIterated greedy algorithms for flow-shop scheduling problems: A tutorial,â IEEE Trans Autom. Sci. Eng., vol. 19, no. 3, pp. 1941â1959, Jul. 2022.

[64] X. Zuo et al., âOptimizing hospital emergency department layout via multiobjective tabu search,â IEEE Trans Autom. Sci. Eng., vol. 16, no. 3, pp. 1137â1147, Jul. 2019.

[65] W. Li, C. Wang, Y. Huang, and Y. Cheung, âHeuristic smoothing ant colony optimization with differential information for the traveling salesman problem,â Appl. Soft Comput., vol. 133, 2023, Art. no. 109943.

[66] I. Ilhan and G. GÃ¶kmen, âA list-based simulated annealing algorithm with crossover operator for the traveling salesman problem,â Neural Comput. Appl., vol. 34, no. 10, pp. 7627â7652, 2022.

[67] P. Huang, Y. Wang, and K. Wang, âEnergy-efficient trajectory planning for a multi-UAV-assisted mobile edge computing system,â Front. Inf. Technol. Electron. Eng., vol. 21, no. 12, pp. 1713â1725, 2020.

[68] P. Huang, Y. Wang, K. Wang, and K. Yang, âDifferential evolution with a variable population size for deployment optimization in a UAV-assisted IoT data collection system,â IEEE Trans. Emerg. Top. Comput. Intell., vol. 4, no. 3, pp. 324â335, Jun. 2020.

[69] J. Zhang et al., âPSO-based sparse source location in large-scale environments with a UAV swarm,â IEEE Trans. Intell. Transp. Syst., vol. 24, no. 5, pp. 5249â5258, May 2023.

[70] X. Xu, J. Li, and M. Zhou, âBi-objective colored traveling salesman problems,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 6326â6336, Jul. 2022.

[71] G. Sun et al., âJoint task offloading and resource allocation in aerialterrestrial UAV networks with edge and fog computing for post-disaster rescue,â IEEE Trans. Mobile Comput., early access, Jan. 8, 2024, doi: 10.1109/TMC.2024.3350886.

<!-- image-->

Shoufei Han is currently an associate professor with the School of Artificial Intelligence, Anhui University of Science and Technology, Huainan, China. His current research interests include machine learning, intelligent optimization algorithms, UAV, mobile edge computing, and evolutionary computation. He has more than ten publications including IEEE Transactions on Knowledge and Data Engineering, IEEE Transactions on Cybernetics, IEEE Transactions on Systems, Man, and Cybernetics, IEEE Transactions on Intelligent Transportation Systems, IEEE Trans-

actions on Computational Social Systems and IEEE/CAA JAS. He is a reviewer of IEEE Transactions on Cybernetics, IEEE Transactions on Intelligent Transportation Systems, IEEE Transactions on Neural Networks and Learning Systems, IEEE Transactions on Industrial Informatics and IEEE/CAA Journal of Automatica Sinica.

<!-- image-->

Xiaojing Liu is currently an associate professor with the School of Artificial Intelligence, Anhui University of Science and Technology, Huainan, China. Her current research interests include time dependent road network, deep learning, broad learning system, and their applications in intelligent transportation.

<!-- image-->

MengChu Zhou (Fellow, IEEE) received the BS degree in control engineering from the Nanjing University of Science and Technology, Nanjing, China, in 1983, the MS degree in automatic control from the Beijing Institute of Technology, Beijing, China, in 1986, and PhD degree in computer and systems engineering from Rensselaer Polytechnic Institute, Troy, New York, in 1990. He joined New Jersey Institute of Technology (NJIT), Newark, New Jersey, in 1990, and has been a distinguished professor of electrical and computer engineering since 2013. He

is with Zhejiang Gongshang University, Hangzhou 310018, China. His research interests are in intelligent automation, machine leaning, Petri nets, robotics, Internet of Things, Big Data, cloud/edge computing, transportation and energy systems. He has more than 1200 publications including 17 books, more than 850 journal papers (more than 650 in IEEE transactions), and 32 book-chapters. He holds 31 patents and several pending ones. His recently co-authored books include Learning Automata and their Applications to Intelligent Systems, IEEE Press/Wiley, Hoboken, New Jersey, 2024 (with J. Zhang), Device-Edge-Cloud Continuum Paradigms, Architectures and Applications, Springer Nature, 2023 (with C. Savaglio, G. Fortino, and J. Ma) and Sustainable Manufacturing Systems: An Energy Perspective, IEEE Press/Wiley, Hoboken, Hoboken, New Jersey, 2022 (with L. Li). He served as editor-in-chief of IEEE/CAA Journal of Automatica Sinica, associate editor of IEEE Transactions on Robotics and Automation, IEEE Transactions on Automation Science and Engineering, and IEEE Transactions on Industrial Informatics, and editor of IEEE Transactions on Automation Science and Engineering. He served as a guest-editor for many journals including IEEE Internet of Things Journal, IEEE Transactions on Industrial Electronics, and IEEE Transactions on Semiconductor Manufacturing. He is presently associate editor of research, IEEE Transactions on Intelligent Transportation Systems, IEEE Internet of Things Journal, and Frontiers of Information Technology & Electronic Engineering. He is founding chair/co-chair of Technical Committee on AI-based Smart Manufacturing Systems and Technical Committee on Humanized Crowd Computing of IEEE Systems, Man, and Cybernetics Society, Technical Committee on Semiconductor Manufacturing Automation and Technical Committee on Digital Manufacturing and Human-Centered Automation of IEEE Robotics and Automation Society. He is also a member of IEEE TAB Periodicals Committee and Periodicals Review and Advisory Committee. He was general chair of IEEE Conf. on Automation Science and Engineering, Washington D.C., August 23-26, 2008, general co-chair of 2003 IEEE International Conference on System, Man and Cybernetics (SMC), Washington DC, October 5-8, 2003 and 2019 IEEE International Conference on SMC, Bari, Italy, October 6-9, 2019, founding general co-chair of 2004 IEEE Int. Conf. on Networking, Sensing and Control, Taipei, March 21-23, 2004, and general chair of 2006 IEEE Int. Conf. on Networking, Sensing and Control, Ft. Lauderdale, Florida, April 23-25, 2006. He was program chair of 2010 IEEE International Conference on Mechatronics and Automation, August 4-7, 2010, Xiâan, China, 1998 and 2001 IEEE International Conference on SMC and 1997 IEEE International Conference on Emerging Technologies and Factory Automation. He has led or participated in more than 60 research and education projects with total budget more than \\$12M, funded by National Science Foundation, Department of Defense, NIST, New Jersey Science and Technology Commission, and industry. He is a recipient of Excellence in Research Prize and Medal from NJIT, Humboldt Research Award for US Senior Scientists from Alexander von Humboldt Foundation, and Franklin V. Taylor Memorial Award and the Norbert Wiener Award from IEEE SMC Society, Computer-Integrated Manufacturing UNIVERSITY-LEAD Award from Society of Manufacturing Engineers, Distinguished Service Award from IEEE Robotics and Automation Society, and Edison Patent Award from the Research & Development Council of New Jersey. He has been among most highly cited scholars since 2012 and ranked top one in the field of engineering worldwide in 2012 by Web of Science. He was ranked \#99 among the 2023 Top 1000 Scientists in Computer Science in the World, Research.com. He is a life member of Chinese Association for Science and Technology-USA and served as its president, in 1999. He is fellow of International Federation of Automatic Control (IFAC), American Association for the Advancement of Science (AAAS), Chinese Association of Automation (CAA) and National Academy of Inventors (NAI).

<!-- image-->

Kun Zhu (Member, IEEE) received the PhD degree in computer engineering from Nanyang Technological University, Singapore, in 2012. He is currently a professor with the College of Computer Science and Technology, Nanjing University of Aeronautics and Astronautics. He is also a Jiangsu Specially appointed professor. His interests include intelligent optimization algorithms, 5 G/B5G, resource management, and self-organization networks. He is an editor of Computer and Communications and has served as guest editors for several journals.

<!-- image-->

Liang Zhao (Member, IEEE) received the PhD degree from the School of Computing, Edinburgh Napier University, in 2011. He is a professor with Shenyang Aerospace University, China. He is also a JSPS invitational fellow (2023). He was listed as Top 2% of scientists in the world by Standford University (2022 and 2023). His research interests include ITS, VANET, WMN and SDN. He has published more than 150 articles. He is associate editor of Frontiers in Communications and Networking and Journal of Circuits Systems and Computers. He is/has been a guest editor of IEEE Transactions on Network Science and Engineering, Springer Journal of Computing, etc.

<!-- image-->

Aiiad Albeshri received MS and PhD degrees in information technology from the Queensland University of Technology, Brisbane, Australia, in 2007 and 2013 respectively. He has been an associate professor with Computer Science Department, King Abdulaziz University, Jeddah, Saudi Arabia since 2018. His current research interests include focuses on information security, trust in cloud computing, Big Data and HPC.

<!-- image-->

Abdullah Abusorrah (Senior Member, IEEE) received the doctoral degree from the University of Nottingham, U.K., in 2007. He is a professor with King Abdulaziz University (KAU). He leads the Center for Renewable Energy and Power Systems at KAU. His field of interest includes smart grid, energy systems, and computational intelligence.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_4_img_1.png|page_4_img_1]]
2. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_8_img_1.jpeg|page_8_img_1]]
3. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_14_img_1.jpeg|page_14_img_1]]
4. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_14_img_2.jpeg|page_14_img_2]]
5. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_15_img_1.jpeg|page_15_img_1]]
6. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_15_img_2.jpeg|page_15_img_2]]
7. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_15_img_3.jpeg|page_15_img_3]]
8. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_15_img_4.jpeg|page_15_img_4]]
9. [[../extracted_images/Joint_Association_Deployment_and_Flight_Trajectory_Optimization_for_Multi-UAV-Enabled_Large-Scale_Mobile_Edge_Computing/page_15_img_5.jpeg|page_15_img_5]]

---

