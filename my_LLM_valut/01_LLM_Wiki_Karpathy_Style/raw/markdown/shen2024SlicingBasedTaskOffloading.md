See discussions, stats, and author profiles for this publication at: https://www.researchgate.net/publication/371384092

# Slicing-Based Task Offloading in Space-Air-Ground Integrated Vehicular Networks

ArticleÂ Â inÂ Â IEEE Transactions on Mobile Computing Â· May 2024   
DOI: 10.1109/TMC.2023.3283852

CITATIONS 6

4 authors, including:

<!-- image-->

Hang Shen Nanjing Tech University

63 PUBLICATIONSÂ Â Â 498 CITATIONS

SEE PROFILE

READS 100

<!-- image-->

78 PUBLICATIONSÂ Â Â 771 CITATIONS

SEE PROFILE

# Slicing-Based Task Offloading in Space-Air-Ground Integrated Vehicular Networks

Hang Shen , Member, IEEE, Yibo Tian, Tianjing Wang , Member, IEEE, and Guangwei Bai

AbstractâA slicing-based collaborative task offloading framework for space-air-ground integrated vehicular networks is proposed in this study, which can provide differentiated qualityof-service (QoS) guarantees for task offloading for high-speed vehicles while maximizing the number of completed tasks. A service-oriented radio access network (RAN) slicing framework is presented that supports slicing window adaptation, spectrum and computing resource orchestration, and collaboration among heterogeneous base stations. Based on the queuing model, the collaborative decision-making of RAN slicing and task offloading is modeled as a problem of maximizing the number of long-term task completions, which consists of three subproblems-slicing window division, resource slicing, and task scheduling-which are solved by a multi-access edge computing (MEC)-enabled controller, forming a closed loop with the slicing window as the period. When a new slicing window arrives, the controller determines its duration according to task traffic fluctuations and allocates resources to RAN slices through an optimization method. A double deep Q-learning network (DDQN)-based algorithm is developed for scheduling workflow on small time scales within a slicing window. Simulation results demonstrate that the proposed scheme performs better than existing approaches in terms of adaptability, task completion rate, and control overhead.

Index TermsâSpace-air-ground integrated vehicular networks, slicing window adaptation, RAN slicing, task scheduling, deep reinforcement learning.

## I. INTRODUCTION

T HE characteristics of the fifth-generation (5 G) networks,such as high bandwidth, millisecond-level delay, and ultra- such as high bandwidth, millisecond-level delay,and ultrahigh-density connections, facilitate the development of Internet of vehicles (IoV), which connects vehicles, base stations (BSs), and service providers as a collaborative system and realizes the real-time acquisition of comprehensive information [1]. Invehicle devices have limited computing and storage capabilities, and therefore do not meet the requirements of high-complexity, data-intensive, and delay-sensitive applications. A feasible solution is the multi-access edge computing (MEC) paradigm [2], by which the computation tasks released by vehicles are offloaded to MEC servers on BSs for processing, and the computation results are sent back to vehicles, thereby supporting low-delay and high-efficiency vehicle services. However, there are issues related to terrestrial RANs, such as limited coverage, rigid network structure, and slow service response [3]. The high mobility of vehicles, complex urban road conditions, and diverse task requirements exacerbate the difficulty of task offloading and resource provisioning.

Space-air-ground integrated vehicular networks (SAGVNs) as promising networking architecture, utilize ground-based networks, supported by air- and space-based networks, which can provide seamless, comprehensive information services for vehicles and meet all-time and all-domain service needs [4]. The ground-based network is composed of cellular BSs, which offer services to areas with heavy traffic of people and vehicles. The air-based network consists of drone BSs, with mobile deployment and line-of-sight (LoS) advantages. The space-based network consists of low earth-orbit (LEO) satellites, and is a crucial structure to achieve global coverage and universal connectivity. Both drones and LEO satellites can serve as MEC platforms [5], [6], providing network access and task offloading for vehicles at the edge of the ground-based network, and areas with poor infrastructure.

With the development of intelligent transportation and autonomous driving, more and more in-vehicle applications are being developed, which are either delay-sensitive (e.g., route planning [7] and collision warning [8]) or delay-tolerant (e.g., high-definition (HD) map downloads [9]). Network slicing technology [10] can divide a physical RAN into multiple isolated virtual networks (i.e., RAN slices), to provide customized services for different applications. RAN slicing can provide differentiated quality-of-service (QoS) for IoV task offloading. The MEC-enbaled controller allocates computing and communication resources for a RAN slice based on information such as task traffic. In the sliced IoV, the offloading strategy decides where to offload tasks based on task attributes, BS loads, vehicle speeds, and routes. A natural step in the evolution of SAGVNs is to extend RAN slicing from ground-based networks to air- and space-based networks to support diverse IoV applications.

## A. Challenging Issues and Related Works

SAGVN is a dynamic architecture with the features of multinetwork integration and high vehicle speed, which bring many challenges to RAN slicing and task offloading:

1) Dynamic Adjustment of Slicing Window: This is a fundamental problem, and the key to balancing overhead and QoS. Due to the dynamic nature of the network and the time-varying task traffic, the service provision capability of slices will gradually weaken over time. The MEC controller must periodically reallocate resources to RAN slices. If the slicing window is too short, resource reallocation will be triggered frequently, which brings huge control and computing costs. However, if the slicing window is too long, the fluctuation of task traffic may lead to the destruction of slice performance isolation. Zhang et al. proposed a dynamic RAN slicing framework for IoV, which divides time into multiple equal-length slicing windows, where the optimal resource allocation strategy is calculated for each window [11]. Li et al. proposed a hierarchical soft RAN slicing framework for differentiated service provisioning, which conducts network-level and BS-level resource slicing on both large and small timescales [12]. In the above methods, resources are allocated in a fixed slicing window.

2) Multi-Dimensional Resource Orchestration for Multi-tier Networks: The traffic in a road network is unevenly distributed in both time and space. There are generally large differences in the deployment, coverage, and resources for heterogeneous BSs. The coupling of resources in heterogeneous networks exacerbates the complexity of decision-making. Most studies have considered only terrestrial networks or a single type of resource slicing. Ye et al. proposed a downlink spectrum resource slicing framework for heterogeneous wireless networks, which achieved differentiated QoS provisioning for machinetype devices and end devices [13]. Peng et al. incorporated a transmit power adjustment mechanism and designed a spectrum slicing strategy based on multi-access edge computing [14]. A spectrum and computing resource slicing framework was proposed by Wu et al. to meet the requirements of task offloading of differentiated QoS in IoV [15]. Peng et al. combined a deep deterministic policy gradient (DDPG) and hierarchical learning to achieve multidimensional resource allocation in vehicular networks [16]. Li et al. presented a resource allocation framework for terrestrial-satellite networks, integrating a multi-agent DDPG algorithm to allocate resources and deploy cache equipment for maximum energy efficiency [17].

3) Collaboration Among Heterogeneous BSs: The interaction between a high-speed vehicle and a BS is instantaneous and is affected by vehicle speed, direction, and road conditions. The collaboration among air-ground, space-ground, and air-space BSs helps to reduce delay and facilitate task completions. Traditional model optimization and heuristic methods [18], [19], [20] cannot deal with real-time task offloading in dynamic scenarios. By integrating the decision-making advantages of reinforcement learning (RL) and the perceptual benefits of deep learning (DL), deep reinforcement learning (DRL) [21] allows individuals to perceive the environment and act accordingly, to deal with high-dimensional state-action spaces. Apostolopoulos et al. proposed a drone-Assisted framework for making data offloading decisions, allowing users to offload their data to ground or drone-mounted MEC servers [22]. The optimal offloading for each user was formulated as a maximization problem of their satisfaction and treated as a non-cooperative game. Most existing studies on BS collaboration in IoV consider the ground network. Kai et al. proposed a pipeline-based task offloading method by which mobile devices can offload tasks to edge nodes or the cloud according to their computing and communication capabilities [23]. Bai et al. investigated a delay minimization problem for multi-UAV-enabled edge-cloud cooperative offloading [24]. The problem was formulated as a non-convex problem considering network congestion, air-to-ground channels, and cooperative computing. Li et al. proposed a DRL-assisted task division and scheduling algorithm to maintain service continuity by preselecting edge servers, and reduce computing delays through edge-side collaboration [25]. Based on the multi-armed bandit theory, the online and off-policy learning approaches were presented in [26] to predict the offloading latency and select the least congested network. Wang et al. proposed an imitation learning-based task scheduling algorithm to minimize energy consumption under the task latency constraint of vehicular networks [27]. By combing actor-critic (A3C) and deep Q-network (DQN), Dai et al. developed an asynchronous task offloading algorithm to achieve fast convergence in an asynchronous way [28].

## B. Contributions and Organization

In view of the above challenges, we propose a slicing-based collaborative task offloading framework for SAGVNs, which maximizes the number of completed tasks with differentiated QoS provisioning for task offloading. The main contributions of the study are three folded:

- A service-oriented RAN slicing framework is presented, which supports adaptive slicing window duration, multidimensional resource orchestration, and collaborative task offloading. Based on the queuing model, the decisionmaking of RAN slicing and task offloading is modeled as an optimization problem to maximize the number of long-term task completions under coupled resource capacity constraints;

- To balance QoS and overhead, an adaptive strategy for slicing window duration is proposed. During peak traffic hours, the slicing window length is reduced to facilitate resource reallocation. During off-peak periods, the slicing window length is increased to reduce overhead. For each window, an optimization method is applied to solve the spectrum and computing resource allocation problem for slices on heterogeneous BSs;

- A task scheduling approach based on the double deep Q-learning network (DDQN) is developed to determine task distribution under small timescales among heterogeneous BSs, where vehicle speed, driving direction, BS workloads, and task type are considered. In simulations, the proposed scheme outperforms existing methods in terms of adaptability, resource utilization, and task completion rate.

The remainder of this article is organized as follows. Section II presents the RAN slicing framework, communication model, and task scheduling framework. In Section III, the joint optimization of RAN slicing and task scheduling is modeled as a constrained stochastic optimization problem. Section IV presents the solutions to each subproblem and proposes a joint optimization framework. Section V describes simulation experiments for performance evaluation. Section VI summarizes the study and discusses future prospects. The main notations and variables are listed in Table I.

TABLE I  
MAIN NOTATIONS AND VARIABLES
<table><tr><td>Symbols</td><td>Definition</td><td>Symbols</td><td>Definition</td></tr><tr><td> $a _ { m , i , j }$ </td><td>0-1 variable for establishing an upload connection</td><td> $r _ { j ^ { \prime } , i , m }$ </td><td>Downlink transmission rate for task m&#x27;s result</td></tr><tr><td> $a ^ { ( \ell ) }$ </td><td>Workflow scheduling action at epoch l</td><td> $r ^ { ( \ell ) }$ </td><td>Reward given by the environment at epoch l</td></tr><tr><td> $\mathcal { A } ^ { ( w ) }$ </td><td>Set of scheduling strategies in window w</td><td> $\mathcal { R } _ { t , o }$ </td><td>Set of task receptions of type o in time slot t</td></tr><tr><td> $\boldsymbol { A } _ { t }$ </td><td>Set of scheduling strategies in time slot t</td><td> $s _ { j }$ </td><td>Num. of VM instances held by BS j</td></tr><tr><td> $b _ { m , i , j ^ { \prime } }$ </td><td>0-1 variable for transferring task m to BS j&#x27;</td><td> $s _ { j , o }$ </td><td>Num. of VM instances allocated to slice o at BS j</td></tr><tr><td> $\boldsymbol { B }$ </td><td>Set of of ground BS indexes</td><td> $s ^ { ( \ell ) }$ </td><td>Environment state for epoch l</td></tr><tr><td> $c _ { j }$ </td><td>Num. of subchannels held by BS j</td><td> $\boldsymbol { S } ^ { ( w ) }$ </td><td>Set of computing resource allocation strategies</td></tr><tr><td> $c _ { j , o }$ </td><td>Num. of subchannels allocated to slice o from Cj</td><td> ${ \mathcal { T } } ^ { ( w ) }$ </td><td>Set of scheduling slots in slicing window w</td></tr><tr><td> $\mathcal { C } ^ { ( w ) }$ </td><td>Set of subchannel allocation strategies</td><td> $U ^ { ( w ) }$ </td><td>Average reward of the system</td></tr><tr><td> $d _ { m }$ </td><td>Total service delay of task m</td><td> $\mathcal { W } / W$ </td><td>Set/Num. of slicing windows</td></tr><tr><td> $\ddot { d } _ { m }$ </td><td>Estimated reception time for the result of task m</td><td> $y _ { m }$ </td><td>Num.of subchannels allocated to task m</td></tr><tr><td> $e _ { m }$ </td><td>O-1 variable for the result return of task m</td><td> $z _ { m }$ </td><td>Num.of subchannels allocated to task m&#x27;s result</td></tr><tr><td> $f ^ { ( w ) }$ </td><td>Duration of slicing window w</td><td> $\lambda _ { i , o }$ </td><td>Arrival rate of type o tasks in vehicle i</td></tr><tr><td> $\dot { \boldsymbol { H } } ^ { ( w ) }$ </td><td>Average loss due to incomplete tasks</td><td> $\varepsilon _ { m }$ </td><td>Data size of task m</td></tr><tr><td> $\mathcal { T }$ </td><td>Set of vehicle indexes</td><td> $\tau _ { m }$ </td><td>Required num.of VM instances of task m</td></tr><tr><td> $\mathcal { \kappa }$ </td><td>Set of drone indexes</td><td> $\iota _ { m }$ </td><td>Computation result size of task m</td></tr><tr><td> $\mathcal { L }$ </td><td>Set of satellite indexes</td><td> $\nu _ { m }$ </td><td>Delay constraint of task m</td></tr><tr><td> $\mathcal { M } _ { j , o } ^ { ( w ) } / M _ { j , o } ^ { ( w ) }$ </td><td> Set/Num. of type o tasks collected by BS j</td><td> $\rho _ { o } ^ { ( w ) }$ </td><td>Service intensity of offloading queue o</td></tr><tr><td> $r _ { m , i , j }$ </td><td>Uplink transmission rate of task m</td><td> $\mu _ { o }$ </td><td>Average time for tasks of type o</td></tr></table>

## II. SAGVN MODEL

Fig. 1 shows an SAGVN composed of an LEO satellite constellation, ground BSs, and drones. Ground BSs and drones have limited coverage, whereas LEO satellites can seamlessly cover the entire road network. The vehicles are equipped with three signal transceivers that can connect to satellites, ground BSs, and drones, while only one can be connected in a single time slot. The satellites are connected to the core network through the ground BSs. Drones that support task processing are pre-deployed, and positions can be adjusted as needed. They can connect to the ground BSs through a line-of-sight link and interact with the core network via ground BSs. An MEC-enabled controller is connected to different types of BSs through wireless relays or the core network and is responsible for multidimensional resource allocation on the RAN side and task scheduling among heterogeneous BSs.

## A. RAN Slicing Framework

A service-oriented RAN slicing framework is proposed for task offloading, as shown in Fig. 2. The physical resources of each satellite, ground and drone BS are orchestrated into two service slices 1 and 2, for delay-sensitive and delay-tolerant tasks. The sets of satellite, ground, and drone BSs are denoted as L, B, and K, respectively. The length of the slicing window can be adaptively adjusted according to network situations (details in Section IV-B). The time domain is divided into a series of slicing windows of different lengths, each containing multiple scheduling slots of equal length. The duration of slicing window w is denoted as $f ^ { ( w ) }$ , with a set of scheduling slots denoted as $\mathcal { T } ^ { ( w ) }$ . The spectrum and computing resources are allocated in units of subchannels and virtual machine (VM) instances. The number of subchannels and VM instances held by BS j are denoted as $c _ { j }$ and $s _ { j } \colon : \cdot$ respectively. At the beginning of slicing window w, the resources of each BS are sliced according to task scheduling decisions in window $w - 1$ . Let $c _ { j , o }$ and $s _ { j , o }$ denote the number of the subchannels and VM instances allocated to slice o at BS j (with $\begin{array} { r } { c _ { j } = \sum _ { o \in \{ 1 , 2 \} } c _ { j , o } ^ { ( w ) } } \end{array}$ , and $\begin{array} { r } { s _ { j } = \sum _ { o \in \{ 1 , 2 \} } s _ { j , o } ^ { ( w ) } ) } \end{array}$ . The resource slicing strategy continues until the end of slicing window w. At the beginning of each scheduling slot in $\mathcal { T } ^ { ( w ) }$ , the controller transfers the collected tasks to appropriate BSs for processing. BSs allocate resources for received tasks and transmit the computation results back to the original vehicle. At the end of each slicing window, the task scheduling decisions in this window are collected for the next window.

## B. Communication Model

Since a long distance separates a satellite and a vehicle, the influence of vehicle movement on vehicle-to-satellite channel gain can be neglected in a small area. The average channel gain of vehicle i within the coverage of $\mathbf { B S } j \in \mathcal { L } \cup B \cup \mathcal { K }$ is denoted as ${ \mathit { g } } _ { i , j } ,$ which is quantified using the method described by Erceg et al. [29].

The transmit powers of vehicle i and BS j are denoted as $p _ { i }$ and $p _ { j }$ , respectively. During communication with BS $j ,$ other BSs can interfere with vehicle i. Spectrum resources in a slice are allocated to each vehicle in units of mutually orthogonal subchannels [30], [31]. Assume that the bandwidth of each subchannel is h. Let $y _ { m }$ denote the number of subchannels allocated to task m. The uplink transmission rate when vehicle i submits task m to BS j is calculated as

<!-- image-->  
Fig. 1. SAGVN scenario.

$$
r _ { m , i , j } = y _ { m } h \mathrm { l o g } _ { 2 } \left( 1 + \frac { p _ { i } g _ { i , j } } { \displaystyle \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { W } \backslash \{ j \} } p _ { j ^ { \prime } } g _ { i , j ^ { \prime } } + \sigma ^ { 2 } } \right) ,\tag{1}
$$

where Ï is the average background noise. Let $z _ { m }$ denote the number of subchannels allocated to the computation result of task m. The downlink transmission rate of transferring the computational result of task m from BS j to vehicle i is calculated as

$$
r _ { j ^ { \prime } , i , m } = z _ { m } h \mathrm { l o g } _ { 2 } \left( 1 + \frac { p _ { j ^ { \prime } } g _ { i , j } } { \displaystyle { \sum _ { j \in \mathcal { L } \cup \mathcal { W } \backslash \{ j ^ { \prime } \} } } p _ { j } g _ { i , j } + \sigma ^ { 2 } } \right) .\tag{2}
$$

## C. Task Scheduling Framework

A BS-collaborative framework is designed to take into account the high-speed movement of vehicles. Task offloading and processing no longer rely on a single BS but allow execution at two different BSs. Each BS has processing queues 1 and 2, to buffer delay-sensitive and delay-tolerant tasks, respectively. Similarly, the MEC controller has offloading queues 1 and 2 to buffer the two types of tasks received from heterogeneous BSs. According to network situations, these tasks are transferred to different BSs for collaborative processing. Two examples are described below.

1) Scheduling of delay-sensitive tasks: In Fig. 3(a), a vehicle is located within the coverage of the satellite and ground BS 1 when a task is generated. According to the principle of proximity, the task is collected by ground BS 1 and transferred to offloading queue 1 of the MEC controller. According to the direction and speed of the vehicle, the satellite and drone are selected as candidate collaborative BSs. Due to the low latency requirement, the controller selects the drone, which has a low load, to process the task, where the drone follows the first-come-first-serve (FCFS) rule to allocate resources for the task and transmit the processed results back to the vehicle.

2) Scheduling of delay-tolerant tasks: In Fig. 3(b), a vehicle is within the coverage of the satellite, drone, and ground BS 2. The drone receives the generated task and transfers it to offloading queue 2 of the controller. Based on the speed and direction of the vehicle, the satellites or ground BS 2 are listed as candidate collaborators. The controller selects the satellite with a low load to process the task.

<!-- image-->  
Fig. 2. RAN slicing framework for vehicle task offloading.

From the above examples, task scheduling should consider vehicle speed, driving direction, and BS workloads.

We next derive task service delay based on queuing theory. Each computation task is characterized by four parameters $\{ \varepsilon _ { m } , \tau _ { m } , \iota _ { m } , \nu _ { m } \}$ extending from [15], [32], where $\varepsilon _ { m } , \tau _ { m } , \iota _ { m } ,$ and $\nu _ { m }$ denote the task data size, the required number of VM instances, task computation result size, and delay constraint of task m.

1) Offloading Delay: The offloading delay (e.g., step 1 in Fig. 3(a) and (b)) refers to the time taken from a task being uploaded by the receiving BS to the offloading queue at the controller and transferred to the processing queue at the cooperating BS.

Denoted by I the vehicle set. The set of type o tasks collected by ${ \mathrm { B S ~ } } j$ is denoted as $\mathcal { M } _ { j , o } ^ { ( w ) }$ with $M _ { j , o } ^ { ( w ) }$ being its cardinality, in which $o = 1$ and $o = 2$ represent delay-sensitive and delaytolerant task types. Let $a _ { m , i , j } = 1$ represent that vehicle i and BS j establishes an uploading connection for task m, and otherwise, $a _ { i , m , j } = 0$ . According to (1), the average delay to upload a type o task from a vehicle to a BS is

$$
\mu _ { o } ^ { ( w ) } = \frac { \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } { \sum } \underset { m \in \mathcal { M } _ { j , o } ^ { ( w ) } } { \sum } \underset { i \in \mathbb { Z } } { \sum } \left( \varepsilon _ { m } a _ { m , i , j } / r _ { m , i , j } \right) } { \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } { \sum } M _ { j , o } ^ { ( w ) } } .\tag{3}
$$

The task arrivals for individual vehicles and BSs are modeled as Poisson processes as in [32]. Denote $\lambda _ { i , o } ^ { ( w ) }$ as the arrival rate of type o tasks at vehicle i. The task arrival rate of offloading

queue o in the controller is expressed as

$$
\lambda _ { o } ^ { ( w ) } = \sum _ { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \sum _ { m \in \mathcal { M } _ { j , o } ^ { ( w ) } } \sum _ { i \in \mathcal { I } } a _ { m , i , j } \lambda _ { i , o } ^ { ( w ) } .\tag{4}
$$

Only one task is processed at a time. The task offloading process is modeled as an M/M/1 queue. The service intensity of offloading queue o is defined as

$$
\rho _ { o } ^ { ( w ) } \triangleq \lambda _ { o } ^ { ( w ) } \mu _ { o } ^ { ( w ) } .\tag{5}
$$

Enqueueing is determined by task arrival, and dequeuing by task assignment. When the enqueue rate is greater than the dequeue rate, the accumulation of tasks may cause an overflow. To ensure queue stability, (5) must satisfy

$$
\rho _ { o } ^ { ( w ) } < 1 , \forall o \in \{ 1 , 2 \} .\tag{6}
$$

Denote $\Omega ( m )$ as the set of tasks queued before task m. Then, the offloading delay of task m is calculated as

$$
d _ { m } ^ { ( 1 ) } = \sum _ { i \in \mathcal { I } } \sum _ { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \sum _ { m ^ { \prime } \in \{ \Omega ( m ) , m \} } \frac { a _ { m , i , j } \varepsilon _ { m ^ { \prime } } } { r _ { m ^ { \prime } , i , j } } + \zeta _ { m } ,\tag{7}
$$

where $\zeta _ { m }$ is the delay for submitting task m via the receiving BS and forwarding it via the controller.

2) Processing Delay: The processing delay (e.g., step 2 in Fig. 3(a) and (b)) is the time from when a task enters a processing queue at a collaborative BS to when the task processing is completed.

<!-- image-->

(a) Delay-sensitive task scheduling (case-1).  
<!-- image-->  
(b) Delay-tolerant task scheduling (case-2).  
Fig. 3. Examples of collaborative task scheduling.

The BS allocates VM instances for each task as needed. Assume that the maximum CPU cycle of each VM instance is $\tau ^ { \mathrm { ( m a x ) } }$ Hz per second. If the number of VM instances allocated by BS $j$ for task m is $s _ { m }$ , the average processing time of the tasks in processing queue o in window w is calculated as

$$
\mu _ { j ^ { \prime } , o } ^ { ( w ) } = \frac { 1 } { M _ { j ^ { \prime } , o } ^ { ( w ) } } \sum _ { m \in { \mathcal { M } _ { j ^ { \prime } , o } ^ { ( w ) } } } \frac { \tau _ { m } } { s _ { m } \tau ^ { ( \operatorname* { m a x } ) } } .\tag{8}
$$

The tasks in the offloading queues in the controller are distributed to the processing queues of different BSs. Let $b _ { m , i , j ^ { \prime } }$ be 1 if the controller transfers the task m generated by vehicle i to BS $j ^ { \prime }$ for collaborative processing, and otherwise be 0. In slicing window w, the proportion of tasks assigned by the controller to BS j is expressed as

$$
\eta _ { j ^ { \prime } , o } ^ { ( w ) } = \frac { \displaystyle \sum _ { i \in \mathbb { Z } } \sum _ { m \in \mathcal { M } _ { j ^ { \prime } , o } ^ { ( w ) } } b _ { m , i , j ^ { \prime } } } { \displaystyle \sum _ { i \in \mathbb { Z } } \sum _ { m \in \mathcal { M } _ { j ^ { \prime } , o } ^ { ( w ) } } \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } b _ { m , i , j ^ { \prime } } } .\tag{9}
$$

The arrival of tasks in processing queue o at BS $j ^ { \prime }$ is also assumed to follow a Poisson process, where the task arrival rate $j ^ { \prime }$ is $\eta _ { j ^ { \prime } , o } ^ { ( w ) } \lambda _ { o } ^ { ( w ) }$ . The task processing is modeled as an M/M/1 queue. Based on (4), (8), and (9), the service intensity of processing queue o in the BS is defined as

$$
\rho _ { j ^ { \prime } , o } ^ { ( w ) } \triangleq \eta _ { j ^ { \prime } , o } ^ { ( w ) } \lambda _ { o } ^ { ( w ) } \mu _ { j ^ { \prime } , o } ^ { ( w ) } .\tag{10}
$$

Similar to (6), (10) must satisfy

$$
\begin{array} { r } { \rho _ { j ^ { \prime } , o } ^ { ( w ) } < 1 , \forall j ^ { \prime } \in \mathcal { L } \cup B \cup \mathcal { K } , o \in \{ 1 , 2 \} . } \end{array}\tag{11}
$$

At BS $j ^ { \prime } ,$ , the set of tasks queued before task m is denoted as $\Psi _ { j ^ { \prime } } ( m )$ , and the processing delay of task m is calculated as

$$
d _ { m } ^ { ( 2 ) } = \sum _ { i \in \mathcal { T } } \sum _ { m ^ { \prime } \in \{ \Psi _ { j ^ { \prime } } ( m ) , m \} } \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \frac { b _ { m , i , j ^ { \prime } } \tau _ { m ^ { \prime } } } { s _ { m } \tau ^ { ( \operatorname* { m a x } ) } } .\tag{12}
$$

3) Handover Delay: After a task is processed at collaborative BS $j ,$ , the BS sends the result back to the vehicle (e.g., step 3 in Fig. 3(a) and (b)). Based on (2), the delay for BS $j ^ { \prime }$ to hand over the computation result of task m to vehicle i is

$$
d _ { m } ^ { ( 3 ) } = \sum _ { i \in \mathcal { T } } \sum _ { j ^ { \prime } \in \mathcal { L } \cup B \cup \mathcal { K } } \frac { b _ { m , i , j ^ { \prime } } l _ { m } } { r _ { j ^ { \prime } , i , m } } .\tag{13}
$$

Suppose that task m issued by vehicle i is assigned to be processed by BS $j ^ { \prime }$ . If the speed vector of vehicle i is $\vec { v _ { i } }$ and the remaining driving distance to leaving the coverage of BS $j ^ { \prime }$ is $\omega _ { i , j ^ { \prime } }$ , the remaining time for vehicle i to receive the computation result of task m is estimated as

$$
\widehat { d } _ { m } = \sum _ { i \in \mathcal { I } } \sum _ { j ^ { \prime } \in \mathcal { L } \cup B \cup \mathcal { K } } \frac { b _ { m , i , j ^ { \prime } } \omega _ { i , j ^ { \prime } } } { \vec { v _ { i } } } + \varrho ,\tag{14}
$$

where $\varrho$ is an adjustable parameter related to special events. For instance, when vehicle i is about to encounter a red light, $\varrho$ can be set to the duration of the red light.

Combining (14) and $\nu _ { m }$ , the deadline of task m generated by vehicle i is rewritten as

$$
\operatorname* { m i n } \left\{ \nu _ { m } , \widehat { d } _ { m } \right\} .\tag{15}
$$

Factors such as driving direction variations may also cause its failed encounter with collaborative BS $j ^ { \prime }$ . In this case, even if the task is processed by BS $j ^ { \prime }$ within (15), the result cannot be transmitted back to vehicle i.

## III. PROBLEM FORMUATION

In the proposed framework, a challenging problem is the joint optimization of slicing window division, resource orchestration, and task scheduling.

The total service delay of task m is the summation of (7), (12), and (13), i.e.,

$$
d _ { m } = d _ { m } ^ { ( 1 ) } + d _ { m } ^ { ( 2 ) } + d _ { m } ^ { ( 3 ) } .\tag{16}
$$

Based on (15) and (16), we define a binary variable,

$$
e _ { m } \triangleq \left\{ \begin{array} { l l } { 1 , \mathrm { i f } \operatorname* { m i n } \left\{ \nu _ { m } , \widehat { d } _ { m } \right\} \geq d _ { m } } \\ { 0 , \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{17}
$$

where $e _ { m } = 1$ if and only if the result of task m is successfully delivered within the specified time. In slicing window w, the average reward of the system for completing the tasks is defined as

$$
U ^ { ( w ) } \triangleq \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \sum _ { o \in \{ 1 , 2 \} } \sum _ { i \in \mathcal { T } } \sum _ { m \in \mathcal { M } _ { j ^ { \prime } , o } ^ { ( w ) } } u _ { j ^ { \prime } , o } b _ { m , i , j ^ { \prime } } e _ { m } ,\tag{18}
$$

where $u _ { j ^ { \prime } , o } \in ( 0 , 1 )$ is the reward factor for the completion of type o tasks in collaborative BS $j ^ { \prime }$ . The average loss due to incomplete tasks is defined as

$$
H ^ { ( w ) } \triangleq \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \sum _ { o \in \{ 1 , 2 \} } \sum _ { i \in \mathcal { T } } \sum _ { m \in \mathcal { M } _ { j ^ { \prime } , o } ^ { ( w ) } } h _ { j ^ { \prime } , o } b _ { m , i , j ^ { \prime } } ( 1 - e _ { m } ) ,\tag{19}
$$

where $h _ { j ^ { \prime } , o } \in \{ 0 , 1 \}$ is the loss factor for the failure to complete the tasks of type o in collaborative BS $j ^ { \prime }$

In slicing window w, the strategy sets of spectrum allocation, computing resource allocation are denoted by

$$
\mathcal { C } ^ { ( w ) } = \left. c _ { j , o } ^ { ( w ) } | o \in \left. 1 , 2 \right. , j \in \mathcal { L } \cup B \cup \mathcal { K } \right. ,
$$

and

$$
\begin{array} { r } { \mathcal { S } ^ { ( w ) } = \left\{ { s } _ { j , o } ^ { ( w ) } \middle | o \in \left\{ 1 , 2 \right\} , j \in \mathcal { L } \cup B \cup \mathcal { K } \right\} . } \end{array}
$$

In time slot t, the set of task receptions of type o is denoted as $\mathcal { R } _ { t , o } .$ , and the set of scheduling strategies is denoted as $\boldsymbol { A } _ { t } =$ $\{ a _ { m , i , j } , b _ { m , i , j ^ { \prime } } | i \in \mathcal { I } , o \in \{ 1 , 2 \} , m \in \mathcal { R } _ { t , o } , j , j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } \}$ Given $\mathcal { T } ^ { ( w ) }$ , the set of scheduling strategies in slicing window w is expressed as

$$
\mathcal { A } ^ { ( w ) } = \bigcup _ { t \in \mathcal { T } ^ { ( w ) } } \mathcal { A } _ { t } .
$$

The slicing window index set and its set cardinality are denoted as W and W . The maximization of task completion under long-term accumulation is modeled as P1.

$$
\mathcal { P } 1 : \operatorname* { m a x } _ { \{ f ^ { ( w ) } , \mathcal { A } ^ { ( w ) } , \mathcal { C } ^ { ( w ) } , \mathcal { S } ^ { ( w ) } \} _ { w \in \mathcal { W } } } \operatorname* { l i m } _ { W \to \infty } \sum _ { w \in \mathcal { W } } \left( \frac { U ^ { ( w ) } - H ^ { ( w ) } } { f ^ { ( w ) } } \right)
$$

$$
\left\{ \sum _ { o \in \{ 1 , 2 \} } c _ { j , o } ^ { ( w ) } = c _ { j } , \forall j \in \mathcal { L } \cup B \cup \mathcal { K } \right.\tag{20a}
$$

$$
\sum _ { o \in \{ 1 , 2 \} } s _ { j , o } ^ { ( w ) } = s _ { j } , \forall j \in \mathcal { L } \cup B \cup \mathcal { K }\tag{20b}
$$

$$
\sum _ { m \in \mathcal { R } _ { t , o } } \sum _ { i \in \mathcal { I } } \sum _ { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } \left( a _ { m , i , j } y _ { m } + b _ { m , i , j } z _ { m } \right)
$$

$$
\leq c _ { j , o } ^ { ( w ) } , \forall o \in \{ 1 , 2 \} , t \in \mathcal { T } ^ { ( w ) }\tag{20c}
$$

$$
\mathrm { s . t . } \left\{ \sum _ { m \in \mathcal { R } _ { t , o } } \sum _ { i \in \mathcal { I } } \sum _ { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } b _ { m , i , j } s _ { m } \leq s _ { j , o } ^ { ( w ) } , \right.
$$

$$
\forall o \in \{ 1 , 2 \} , t \in \mathcal { T } ^ { ( w ) }\tag{20d}
$$

$$
\biggr | \sum _ { i \in \mathbb { Z } } \sum _ { j \in \mathcal { L } \cup B \cup \mathcal { K } } a _ { m , i , j } = 1 , \forall m \in \mathcal { M } _ { j , 1 } ^ { ( w ) } \cup \mathcal { M } _ { j , 2 } ^ { ( w ) }\tag{20e}
$$

$$
\biggr | \sum _ { i \in \mathcal { I } } \sum _ { j ^ { \prime } \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } b _ { m , i , j ^ { \prime } } = 1 , \forall m \in \mathcal { M } _ { j , 1 } ^ { ( w ) } \cup \mathcal { M } _ { j , 2 } ^ { ( w ) }\tag{20f}
$$

(20g)

The problem is to allocate the spectrum and computing resources to each slice, balance BS loads, and maximize the long-term average number of completed tasks. Constraints (20a)

<!-- image-->  
Fig. 4. State machine for the MEC controller.

and (20b) demonstrate the requirements on bandwidth and computing resource allocation for slices 1 and 2 at each BS. The number of spectrum and computing resources allocated to tasks by each BS should not exceed the total number of resources held by itself, corresponding to constraints (20c) and (20d). Constraint (20e) means that each vehicle can only connect to a unique BS for task uploading, and (20f) ensures that each task is assigned to a unique BS for processing. Constraint (20g) aims to maintain the stability of each offloading/processing queue. Both resource allocation and task scheduling decisions affect queue stability.

The objective of P1 is a long-term non-smooth maximum function. Constraints (20e) and (20f) contain two binary integer variables, and the variables in (20g) are coupled to each other. Therefore, it is difficult to obtain an exact optimal solution for $\mathcal { P } 1$ under conventional optimization methods.

## IV. SOLUTION

## A. Problem-Solving Framework

To facilitate processing, P1 is decoupled into three subproblems: 1) adaptive slicing window division; 2) resource allocation (large timescale), and 3) task scheduling (small timescale). These are solved alternately by the MEC controller, forming a closed loop that runs continuously. As shown in Fig. 4, the behavior of the controller is abstracted as a state machine with three states, each corresponding to a subproblem-solution module. When the system reaches a certain state, the corresponding function module is activated. The operations of each state are described below.

Slicing window adaptation (State 1): When slicing window w â 1 ends, the controller determines the length $\bar { f } ^ { ( w ) }$ of the slicing window according to task traffic fluctuation (details in Section IV-B);

- RAN slicing (State 2): After the length of slicing window w is determined, the task scheduling in window $w - 1$ becomes a known condition for determining resource allocation with respect to $\mathcal { C } ^ { ( w ) }$ and $\boldsymbol { S } ^ { ( w ) }$ in window w (details in Section IV-C). Resource reallocation for each slice is made by the controller at the beginning of each slicing window, and remains unchanged until its end;

<!-- image-->  
(a) Case-1(x<0,Î±= -9.36,Î²= 77.5)  
Fig. 5. Fitting of task traffic fluctuation and optimal slicing window duration.

Task scheduling (State 3): At the beginning of each scheduling slot in window w, $\mathcal { C } ^ { ( w ) }$ and $\bar { \boldsymbol { S } } ^ { ( w ) }$ are fed into a DDQN algorithm to determine task scheduling (details in Section IV-D). At the end of the last slot in each slicing window, all scheduling decisions within this window are saved as $\mathcal { A } ^ { ( w ) }$ , which are subsequently used to determine $\mathcal { C } ^ { ( w + 1 ) }$ and $\boldsymbol { S } ^ { ( w + 1 ) }$

The detailed solutions to the three subproblems in the closedloop framework are discussed below.

## B. Slicing Window Division

In reality, the release of vehicle task requests is time-varying and uncertain. If resource allocation is performed under a fixed slicing window mode, the resource scheduling of RAN slices will be unable to cope with the fluctuation of task arrivals. During the peak traffic period, the proportions of various types of tasks will fluctuate continuously and significantly. At this time, reducing the slicing window length can promote resource redistribution and adapt to fluctuations in task traffic. In off-peak periods, the proportion of different tasks is relatively stable [33], and the window length can be increased to reduce unnecessary control overhead.

The optimal match between task traffic fluctuation and slicing window length was explored experimentally. The minimum adjustment interval of the slicing window length was 10 minutes. The system first had a preset short window length, which was then tentatively increased. Multiple initial time points were selected, and the numerical pairs of task traffic fluctuation and optimal slicing window length were collected, and fitted as

$$
y = \alpha \mathrm { l o g } _ { 2 } x + \beta .\tag{21}
$$

The fitting process is to find Î± and Î² that minimize the residual sum of squares. Two fitted curves were generated. Fig. 5(a) corresponds to the situation where the task traffic continues to decrease, in which the slicing window length gradually increases with the decrease of traffic. Fig. 5(b) shows the situation where the task traffic falls, in which the variation is the opposite of Fig. 5(a). It can be seen that the more severe the fluctuation of task traffic, the smaller the optimal slicing window length, which is as expected.

At the end of window $w - 1$ , the ARIMA-ANN Hybrid model [34] was used to predict the task traffic at the beginning of the next window w, denoting the predicted value as $\varpi ^ { ( w ) }$

<!-- image-->  
(b)Case-2(x >0,Î± = -8.37,Î²= 71.25)

The ARIMA and ANN models are suitable for processing linear and nonlinear historical data, and to integrate them can improve prediction accuracy. Based on (21) and $\varpi ^ { ( w ) }$ , the duration of slicing window w is determined as

$$
\begin{array}{c} \begin{array} { r } { f ^ { ( w ) } = \{ \gamma \big \vert \alpha _ { 1 } \mathrm { l o g } _ { 2 } ( - x ) + \beta _ { 1 } \big \vert , x \in ( - \infty , 0 )  , } \\ { \gamma \lceil \alpha _ { 2 } \mathrm { l o g } _ { 2 } x + \beta _ { 2 } \rceil , x \in ( 0 , + \infty ) } \end{array}  ,  \end{array}\tag{22}
$$

where $x = ( \varpi ^ { ( w ) } - \varpi ^ { ( w - 1 ) } ) / \varpi ^ { ( w - 1 ) } , \ \gamma$ is a constant representing the smallest unit of slicing window length, and 
Â· and Â· denote rounding up and down.

## C. Resource Slicing

The resource slicing subproblem is to maximize task completions by allocating spectrum and computing resources across RAN slices, i.e.,

$$
\begin{array} { r l } & { \mathcal { P } 1 . 1 : \underset { \{ \mathcal { C } ^ { ( w ) } , \mathcal { S } ^ { ( w ) } \} _ { w \in \mathcal { W } } } { \operatorname* { m a x } } \underset { W \to \infty } { \operatorname* { l i m } } \sum _ { w \in \mathcal { W } } \left( \frac { U ^ { ( w ) } - H ^ { ( w ) } } { f ^ { ( w ) } } \right) } \\ & { \mathrm { s . t . } ( 2 0 \mathrm { a } ) , ( 2 0 \mathrm { b } ) , ( 2 0 \mathrm { c } ) , \mathrm { a n d } ( 2 0 \mathrm { d } ) . } \end{array}
$$

According to (18) and (19), the decision of each slicing window is independent, and the tasks within the window are independently allocated resources. In the real world, the task traffic does not fluctuate continuously in adjacent slicing windows. Based on $\mathcal { A } ^ { ( w - 1 ) }$ , the controller can calculate the amount of spectrum and computing resources required for each slice in window w. Accordingly, P1.1 is transformed to a one-shot optimization of maximizing task completions in window w as P1.1a.

$$
\begin{array} { r l } & { \mathcal { P } 1 . \mathrm { 1 a } : \displaystyle \operatorname* { m a x } _ { \mathcal { C } ^ { ( w ) } } \frac { U ^ { ( w ) } - H ^ { ( w ) } } { f ^ { ( w ) } } } \\ & { \mathrm { s . t . ~ } ( 2 0 \mathrm { a } ) , ( 2 0 \mathrm { b } ) , ( 2 0 \mathrm { c } ) , \mathrm { a n d ~ } ( 2 0 \mathrm { d } ) . } \end{array}
$$

P1.1a belongs to a multi-constraint multivariate function extremum problem. A Lagrange multiplier was used to solve the problem by transforming a multivariate and multi-constraint optimization problem to a multivariate unconstrained extremum problem. Then P1.1a is converted to P1.1b (shown at the bottom of this page) by taking $\mathcal { C } ^ { ( w ) }$ and $\boldsymbol { S } ^ { ( w ) }$ as input parameters to the problem. The optimal resource allocation scheme for P1.1b can be obtained by gradient descent.

## D. DDQN-Based Task Scheduling

The task scheduling subproblem is to maximize task completions by selecting collaborative BSs for tasks, i.e.,

$$
\begin{array} { r l } & { \mathcal { P } 1 . 2 : \underset { \{ A _ { t } \} _ { t \in T ^ { ( w ) } , w \in \mathcal { W } } } { \operatorname* { m a x } } \underset { W \to \infty } { \operatorname* { l i m } } \sum _ { w \in \mathcal { W } } \left( \frac { U ^ { ( w ) } - H ^ { ( w ) } } { f ^ { ( w ) } } \right) } \\ & { \mathrm { s . t . } \ ( 2 0 \mathrm { e } ) , ( 2 0 \mathrm { f } ) , \mathrm { a n d } \ ( 2 0 \mathrm { g } ) . } \end{array}
$$

As described in Section IV-C, the resource allocation in each slicing window is independent. When the resource allocation is determined, the task scheduling in each slicing window is also independent. Therefore, the long-term optimization problem in P1.2 can be decomposed into a short-term optimization problem for a single slicing window, which is a Markov decision problem with a finite horizon.

The task scheduling subproblem within a slicing window is constructed as a Markov decision process (MDP). The MEC controller is abstracted as an agent, making workflow scheduling action $a ^ { ( \ell ) }$ according to $s ^ { ( \ell ) }$ , the environment state for training epoch . The reward given by the environment is denoted as $r ^ { ( \ell ) }$ . The controller updates the environment state to $s ^ { ( \ell + 1 ) }$ according to state transition probability $\operatorname* { P r } ( s ^ { ( \ell + 1 ) } | s ^ { ( \ell ) } , a ^ { ( \ell ) } )$ The expressions of the state space, action space, and reward are as follows.

- State Space: Task scheduling should consider real-time information about tasks, vehicles, slice workloads. Let $l _ { i }$ and $\varphi _ { j , o }$ denote the position of vehicle i and the number of tasks in processing queue o at BS j. Then the state of training epoch  is expressed as

$$
\begin{array} { r l } & { s ^ { ( \ell ) } = \{ \varepsilon _ { m } , \tau _ { m } , \iota _ { m } , \nu _ { m } \} _ { o \in \{ 1 , 2 \} , t \in { \mathcal T } ^ { ( w ) } , m \in { \mathcal R } _ { t , o } } } \\ & { \cup \{ l _ { i } , \vec { v } _ { i } \} _ { i \in { \mathcal T } } \cup \{ c _ { j , o } ^ { ( w ) } , s _ { j , o } ^ { ( w ) } , \varphi _ { j , o } ^ { ( w ) } \} _ { j \in { \mathcal L } \cup { \mathcal N } , o \in \{ 1 , 2 \} } . } \end{array}\tag{23}
$$

- Action Space: The workflow scheduling action made by the system in training epoch  is

$$
a ^ { ( \ell ) } = \mathcal { A } ^ { ( \ell ) } ,\tag{24}
$$

where $\mathbf { \mathcal { A } } ^ { ( \ell ) }$ is the set of task scheduling decisions in training epoch , i.e., the controller assigns a set of tasks to collaborative BSs. Under (20e) and (20f), the decision variable for each action is 0 or 1, which is determined by the current state;

. Reward: The reward reflects the pros and cons of actions performed in a certain state. The goal of the system is converted from maximizing the number of task completions to maximizing the reward. Based on (18) and (19), the reward is

$$
r ^ { ( \ell ) } ( s ^ { ( \ell ) } , a ^ { ( \ell ) } ) = U ^ { ( \ell ) } - H ^ { ( \ell ) } ,\tag{25}
$$

where $U ^ { ( \ell ) }$ is the sum of the rewards obtained for completing the tasks in training epoch 1, and $H ^ { ( \ell ) }$ is the sum of the losses for task failures in training epoch . The task scheduling action decides which BSs cooperatively handle the tasks. If a task is completed, the environment will provide a reward to recognize the action. Meanwhile, a penalty mechanism is intoduced to prevent decisions that could cause a high BS load or destabilize the processing queue.

In the MDP, task scheduling refers to the process that the controller maximizes its rewards by allocating tasks in the offloading queue to different collaborative BSs,

$$
{ \mathcal { P } } 1 . 2 { \mathrm { a } } : \operatorname* { m a x } _ { \pi \in \Pi } \sum _ { \ell } { \Big [ } \delta ^ { ( \ell ) } \cdot r ^ { ( \ell ) } \left( s ^ { ( \ell ) } , a ^ { ( \ell ) } \right) | \pi { \Big ] } ,
$$

where  is the set of all possible task allocation strategies, and $\delta ^ { ( \ell ) } \in ( 0 , 1 )$ is the discount factor in epoch . Due to the unpredictability of request releases, state transitions are difficult to determine. The problem cannot be solved by model-based methods such as value iteration and strategy iteration [35]. A realistic solution is to use a model-free scheme that does not rely on state transition probabilities. However, due to the complexity of task scheduling in SAGVNs, traditional model-free RL algorithms are unable to process complex action and state spaces. The DQN algorithm, as an improvement of Q-learning, does not rely on prior knowledge and can adapt to large action-state spaces. DDQN separately trains the evaluation and target networks to avoid overestimation caused by bootstrapping. Therefore, a DDQN-based method is proposed for solving task scheduling on small time scales.

In the state space, the reward of each action is estimated and stored into a Q-table. The action value function is denoted as $Q ( s ^ { ( \ell ) } , a ^ { ( \ell ) } )$ ). The maximum reward for each state in the Qtable represents the maximum possible reward in the future. By querying the Q-table, the action with the maximum reward in each state is determined as

$$
a ^ { * } = \arg \operatorname* { m a x } _ { a } Q ^ { * } ( s ^ { ( \ell ) } , a ^ { ( \ell ) } ) , a ^ { ( \ell ) } \in \pi .\tag{26}
$$

$$
\begin{array} { r l } & { \mathcal { P } \mathrm { 1 . 1 b : } \underset { \{ \mathcal { C } ^ { ( w ) } , S ^ { ( w ) } \} } { \operatorname* { m a x } } F ( \mathcal { C } ^ { ( w ) } , \mathcal { S } ^ { ( w ) } , \kappa _ { 1 } , \kappa _ { 2 } ) } \\ & { = \left( \frac { U ^ { ( w ) } - H ^ { ( w ) } } { f ^ { ( w ) } } \right) + \kappa _ { 1 } \underset { t \in \mathcal { T } ^ { ( w ) } } { \sum } \underset { o \in \{ 1 , 2 \} } { \sum } \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } { \sum } \left( c _ { j , o } - \underset { m \in \mathcal { R } _ { \mathrm { t } , o } } { \sum } \underset { i \in \mathcal { T } } { \sum } \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } { \sum } \big ( a _ { m , i , j } y _ { m } + b _ { m , i , j } z _ { m } \big ) \right) } \\ & { \quad + \kappa _ { 2 } \underset { t \in \mathcal { T } ^ { ( w ) } } { \sum } \underset { o \in \{ 1 , 2 \} } { \sum } \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } { \sum } \left( s _ { j , o } - \underset { m \in \mathcal { R } _ { \mathrm { t } , o } } { \sum } \underset { i \in \mathbb { Z } } { \sum } \underset { j \in \mathcal { L } \cup \mathcal { B } \cup \mathcal { K } } b _ { m , i , j } s _ { m } \right) . } \end{array}
$$

Algorithm 1: DDQN-Based Task Scheduling.   
input : $\left\{ \varepsilon _ { m } , \tau _ { m } , \iota _ { m } , \nu _ { m } \right\} _ { o \in \{ 1 , 2 \} , t \in { \mathcal { T } } ^ { ( w ) } , m \in { \mathcal { R } } _ { t , o } } \cup$   
$\{ l _ { i } , \vec { v } _ { i } \} _ { i \in \mathcal { T } } \cup \{ c _ { j , o } ^ { ( w ) } , s _ { j , o } ^ { ( w ) } , \varphi _ { j , o } ^ { ( w ) } \}$ jâLUBUK,oâ{1,2}   
output: $\pi ^ { * }$   
1 Initialize DDQN parameters and $Q ( s ^ { ( \ell ) } , a ^ { ( \ell ) } ) ;$   
2 Initialize experience replay buffer;   
3 Initialize evaluation network parameters by   
selecting random weight $\theta ;$   
4 Initialize target network parameters by $\theta ^ { - }  \theta ;$   
5 for episode $ 1$ to $| \mathcal { T } ^ { ( w ) } |$ do   
6 Initialize $s ^ { ( 1 ) }$ by observing the environment;   
for $\ell \gets 1$ to $\ell ^ { \mathrm { ( m a x ) } }$ do   
8 With a probability select a random action $a ^ { ( \ell ) }$   
otherwise select $a ^ { ( \ell ) } \gets \pi ( s ^ { ( \ell ) } ) .$   
9 Execute $a ^ { ( \ell ) } ,$ observe $s ^ { ( \ell + 1 ) }$ and reward $r ^ { ( \ell ) } ;$   
10 Store quadruple $( s ^ { ( \ell ) } , a ^ { ( \ell ) } , r ^ { ( \ell ) } , s ^ { ( \ell + 1 ) }$ in the   
experience replay buffer;   
11 if experience replay buffer is not empty then   
12 Sample a batch of quads from the buffer;   
13 if $\ell { = } { = } \ell ^ { ( \mathrm { m a x } ) }$ then   
14 $Q ( s ^ { ( \ell ) } , a ^ { ( \ell ) } | \theta ) \gets r ^ { ( \ell ) } ;$ Break;   
15 else   
16 $Q ( s ^ { ( t ) } , a ^ { ( t ) } | \theta ^ { - } ) \gets$   
$r ^ { ( \ell ) } + \eta \cdot \operatorname* { m a x } _ { \alpha ^ { * } } Q ^ { \prime } ( s ^ { ( t + 1 ) } , a ^ { * ( t + 1 ) } | \theta ^ { - } ) ;$   
17 Update the evaluation network   
parameters via gradient descent $\theta ;$   
18 $\bar { \pi ( s ^ { ( t ) } ) } \longleftarrow \arg \operatorname* { m a x } _ { a ^ { * } } Q ( s ^ { ( \ell ) } , a ^ { * } { } ^ { ( \ell ) } | \theta ) ;$   
19 $\theta ^ { - }  \theta$ every k iterations;   
20 return Strategy set $\pi ^ { * }$ in slicing window w

Applying the Bellman equation to (26), the value in the Q-table can be obtained as

$$
Q { \Big ( } s ^ { ( \ell + 1 ) } , a ^ { ( \ell + 1 ) } { \Big ) } = Q { \Big ( } s ^ { ( \ell ) } , a ^ { ( \ell ) } { \Big ) } + \phi { \Big [ } r ^ { ( \ell ) } + \upsilon \operatorname* { m a x } _ { a ^ { * } } Q { \Big ( } s ^ { ( \ell + 1 ) } ,
$$

$$
\times a ^ { ( \ell + 1 ) } \Big ) - Q \Big ( s ^ { ( \ell ) } , a ^ { ( \ell ) } \Big ) \Big ] ,\tag{27}
$$

where $\phi$ is the learning rate and Ï is the greedy probability.

As shown in Fig. 6, the DDQN-based workflow scheduling scheme uses two neural networks (an evaluation network and a target network) with the same training structures. DDQN-based collaborative task scheduling is named as Algorithm 1. Compared with DQN, Algorithm 1 adds two modules: the experience replay pool and the target network. The experience replay mechanism builds a data pool, storing data obtained during the model and environment interaction in the form of $( s ^ { ( \ell ) } , \breve { a } ^ { ( \ell ) } , r ^ { ( \ell ) } , s ^ { ( \ell + 1 ) } )$ as samples. The samples are randomly selected from the stored memory data units to update the parameters of neural networks. Since $\mathbf { \boldsymbol { s } } ^ { ( \ell ) }$ and $s ^ { ( \ell + 1 ) }$ estimated by DQN are time-dependent, DQN suffers from overestimation bias with a reduced training effect. The experience replay pool in DDQN randomly selects samples during neural network training. Disrupting sample correlation and using data multiple times helps to make better task-offloading decisions than DQN. In addition, the evaluation network and target network have the same structure and asynchronous parameters, where Î¸ is used to select an optimal action, and $\theta ^ { - }$ to evaluate the Q-value of the action. The single neural network in DQN determines both action selection and strategy evaluation. The training of this network relies on (26) for parameters update. From (26), continuing to estimate based on valuation will bring about overestimation. DDQN separates action selection and strategy evaluation from each other. The evaluation network is used to select the optimal action. After the k-step iterative calculation, the evaluation network weight (Î¸) is copied to the target network weight $( \theta ^ { - } )$ for evaluating the Q-value of the optimal action. By delaying parameter updates, DDQN reduces the correlation for evaluation and target networks, reducing the risk of overestimating Q-values.

<!-- image-->  
Fig. 6. DDQN structure for task scheduling.

## E. Computational Complexity Analysis

The advantage of the proposed DDQN-based algorithm is that each time slot can process a batch of computing task requests simultaneously, with improved processing speed and environmental adaptability. In this subsection, we analyze the complexity of Algorithm 1 by comparing it with the DQN algorithm. Assume that the computational complexity of DQN training N training episodes is $\mathcal { O } ( N )$ . DDQN adds a target network based on DQN to reduce the negative impact of data correlation. However, this neural network does not require additional training, and its weight parameters are copied from the evaluation network every k-step. $a ^ { * }$ is selected by the evaluation network, and $Q ( s , a ^ { * } )$ is obtained from the target network. In this way, the action selection and the strategy evaluation operations are separated to reduce data correlation. Compared with DQN, the proposed DDQN-based algorithm improves the rationality of decision-making with almost no increase in the cost of model training. Accordingly, the complexity of Algorithm 1 can be approximated as $\mathcal { O } ( ( 1 + 1 / k ) N )$

<!-- image-->  
(a) Reward acquisition.

Fig. 7. Effect of training epochs.  
<!-- image-->  
(b) Number of tasks completions.

<!-- image-->  
(c) Task failure rate.

## V. PERFORMANCE EVALUATION

Simulations were carried out to verify the effectiveness and superiority of the proposed method. For a four-lane highway that is 1,000 meters long; the origin was set at the starting point of the highway. The scenario contained two ground BSs, three drones, and one satellite. The satellite covered the entire highway, and the two ground BSs each covered about 500 m. The drones hovered above the highway at an altitude of 120 m, with an effective coverage radius of 80 m. The satellite, ground BS, and drone have the transmit powers of 27 w, 40 dBm, and 0.1 w, respectively. The traffic flow trace was selected from OpenITS,1 an open road network traffic data platform. The vehicle density was set to 0.4 vehicles/m2. Autonomous vehicle platooning and HD map downloading simulate delay-sensitive and delay-tolerant tasks. The CPU of the model training platform is AMD Ryzen5 3500X with six cores and six threads, and the graphics card is NVIDIA GeForce GTX 1660 SUPER. Default simulation parameters are shown in Table II, where the deadlines of latency-sensitive and latency-tolerant tasks and the computation result size are randomly generated in the given ranges.

Four methods were selected as baselines, each including three functional modules: slicing window adjustment, resource allocation, and task scheduling. Table III presents the implementation details of each baseline.

## A. Effect of Training Epochs

We evaluated the effect of the number of training epochs on performance. The DRL-based algorithms used the same settings with 4,000 pieces of data. In DRL, the learning speed and training effect are affected by the update period and learning rate. The agentâs propensity for long- and short-term rewards is affected by the discount rate in the cumulative discounted reward. In the simulation regarding Fig. 7(a), we studied the reward and convergence of the proposed method with initial learning rates of 0.1, 0.005, and 0.001. Model training was performed offline. The training time was similar, taking about 12 minutes to execute 100 training episodes. There was a proportional relationship between the reward and the number of completed tasks. In the first 20 training epochs, the rewards first increased rapidly, and then the increase slowed. Due to randomly selected parameters, the agent could not adapt to the environment at the initial stage. Only after learning with a large amount of data could the data correlation be captured and the parameters updated. When the learning rate was at a high level of 0.1, the reward obtained by the proposed solution converged to a maximum value of 1,500. The reward fluctuation throughout the process was apparent. When the learning rate was 0.001, the reward converged to about 2,700, where the system fell into a local optimum, and the training effect could not be improved even by increasing the training epoch. The algorithmâs performance with a learning rate of 0.005 was better compared to the other two learning rates. Not only was the highest reward obtained, but the training effect steadily improved with the increase in the number of training epochs. The reward value rose to 3,157 when training epochs reached 100.

TABLE II  
DEFAULT PARAMETER SETTINGS
<table><tr><td>Parameters</td><td>Values</td></tr><tr><td>Background noise power  $( \sigma ^ { 2 } )$ </td><td>-110 dBm</td></tr><tr><td>Bandwidth of each subchannel (h) CPU cycle of each VMinstance  $( \tau ^ { ( \mathrm { m a x } ) } )$ </td><td>180 kHz</td></tr><tr><td>Number of subchannels held by each</td><td>10 GHz</td></tr><tr><td>ground/drone/satellite BS Number of VM instances held by each</td><td>15/10/40</td></tr><tr><td>ground/drone/satellite BS Deadlineofdelay-sensitive/-tolerant task</td><td>15/8/30</td></tr><tr><td>Arrival rate of delay-sensitive/-tolerant tasks at vehicle i</td><td>0.05-1s/3-10s 4/20 req/s</td></tr><tr><td> $( \lambda _ { i , 1 } / \lambda _ { i , 2 } )$  Data size of delay-sensitive/-tolerant tasks Computation result size of task m  $\left( \iota _ { m } \right)$ </td><td>2000/9000bits 1000-5000bits</td></tr></table>

TABLE III

IMPLEMENTATION OF BASELINE APPROACHES
<table><tr><td>Baseline approach</td><td>Slicing window</td><td>Resource allocation</td><td>Task Scheduling</td></tr><tr><td>Baseline-1 Baseline-2 Baseline-3 Baseline-4</td><td>Static [15], [36] Static [15], [36] Section 4.1</td><td>Section 4.2 Section 4.2 Section 4.2 [16], [36]</td><td>Section 4.3 DQN [37] DQN [37] Max-SINR [38]</td></tr></table>

<!-- image-->  
(a) Task failure rate

<!-- image-->  
(b) Number of slicing windows  
Fig. 8. Impact of delay-sensitive task proportion under different slicing window modes.

Fig. 7(b) shows the number of tasks completed by different methods. Baseline-4 only considered link quality, and did not involve model training, hence its results are used as a reference. After five training epochs, the number of completed tasks by the proposed algorithm and baseline-3 surpassed that of baseline-4 and then continued to rise steadily. The number of tasks completed by the proposed scheme was always higher than baseline-3. As seen in Fig. 7(c), the task failure rate of baseline-4 remained at 29%. As a variant of DQN, DDQN reduces data correlation, and thus has better learning and convergence performance. After 100 training epochs, the task failure rates of the proposed method and baseline-1 were about 21% and 25%, respectively. The former was always lower than the latter.

## B. Impact of Slicing Window Strategy

We verified the performance of the proposed adaptive slicing window strategy. As seen in Fig. 8(a), with the increase of the ratio of delay-sensitive tasks, the task failure rate of baseline-1 and baseline-2 with static slicing window showed an upward trend. Yet, the proposed method and baseline-3 with dynamic window division had stable task failure rates, indicating that the proposed slicing window mode had high adaptability to workload fluctuations. Fig. 8(b) shows the number of slicing windows generated by different methods within two hours. When a new window arrives, the controller will trigger resource reallocation of RAN slices, resulting in a huge signaling overhead. From Fig. 8(a) and (b), the number of windows and the task failure rate of the proposed method were lower than those of baseline-1, suggesting that the proposed method can provide higher-quality services with lower overhead, validating the effectiveness of window adaptation.

We further examined the behavior of different slice window partitioning strategies in response to fluctuations in computing task requests during morning peak hours (6:00 am to 8:00 am). The static strategy divided the timeline evenly into two slicing windows (see Fig. 9(a)). In contrast, the proposed strategy divided the timeline into three slicing windows unevenly (see

Fig. 9(c)) by capturing the fluctuations in the number of tasks. Specifically, the slice windowâs length gradually decreases with an increased task traffic rate. From Fig. 9(b) and (d), the task completion rate was almost the same from 6:00 am to 7:00 am, no matter whether dynamic or static strategies were adopted because the traffic peak had not yet arrived. However, from 7:00 am to 8:00 am, the task completion rate of the proposed strategy remained above 80%, which was higher than that of the static window division strategy. The average task completion rate of baseline-1 with a static policy was only 71%, and that of baseline-5 was even lower than 50%. During the peak hours of traffic flow, the number of windows divided by the proposed scheme may be higher than that of the static strategy. However, throughout the day, the number of slicing windows divided by the former was significantly smaller than that of the latter, confirmed by the results in Fig. 8. The proposed scheme can enhance network managementâs agility and balance control overhead and QoS from the above results.

## C. Impact of Resources and Workloads

Fig. 10(a) shows the effect of spectrum resources on the task failure rate when the number of computing resources is fixed at 15. The task failure rate of each method gradually decreased and stabilized at about 10%. Sufficient spectrum resources enable the controller to have more options, although not the only condition for performance improvement. Next, the effect of computing resources was studied when the number of subchannels was fixed at 20. In Fig. 10(b), the task failure rate dropped rapidly in the initial stage, but when the number of computing resources reached 15, to further increasing the computing resources did not improve performance. At this time, a bottleneck was created by the spectrum resources.

Next, we simulated the situation where the number of released tasks continued to increase over a period of one hour, as shown in Fig. 11(a). Due to resource constraints, the task failure rate generally showed an uptrend. Due to the lack of flexibility, the task failure rate of SINR-based baseline-4 increased from 35% to 52%, while that of DQN-based baseline-2 and baseline-3 increased from 20% to 31%. However, thanks to the collaboration of heterogeneous BSs, the task failure rate of the proposed method increased from 18% to 28% and remained lower than that of the other approaches. Similarly, increases in the proportion of delay-sensitive tasks also decreased the task completion rate. In Fig. 11(b), when the proportion of delay-sensitive tasks was 0.2, the task completion rate of baseline-4 was 52%, and those of baseline-3 and the proposed method were 78% and 85%, respectively. When the proportion of delay-sensitive tasks was 0.8, the task completion rates of the proposed method, baseline-3, and baseline-4 were 58%, 53%, and 26%, respectively. The task scheduling strategy generated by the proposed solution was more reasonable than other methods.

<!-- image-->  
(a)Slicing window division (Static strategy).

<!-- image-->  
(b) Task completed rate in each window (Static strategy).

<!-- image-->  
(c) Slicing window division (Proposed strategy).

<!-- image-->  
(d) Task completed rate in each window (Proposed strategy).

Fig. 9. Slicing window behavior and its effect on task completion rate.  
<!-- image-->  
(a)Impact of spectrum resource variation

<!-- image-->  
(b) Impact of computing resource variation.

Fig. 10. Impact of the number of available spectrum and computing resources.  
<!-- image-->  
(a) Task failure rate under different workloads.

<!-- image-->  
(b) Task failure rate under task proportion.  
Fig. 11. Impact of workloads on task completion rate.

<!-- image-->  
(a) Latency-sensitive tasks.

Fig. 12. CDF of task service delay.  
<!-- image-->  
(b) Latency-tolerant tasks.

Lastly, we observed the cumulative distribution function (CDF) of service latency distribution for those tasks completed under latency constraints. From Fig. 12(a) and (b), the curves of the proposed scheme are on the left side of the other approaches for both latency-sensitive and latency-tolerant tasks, which means that the proposed solution can handle more tasks in the same period than other methods.

## D. Scalability Analysis

We conducted a scalability analysis to demonstrate the efficiency and robustness of the proposed framework.

1) Scalability at the Service-Type Level: The number of slices on each satellite, ground BS, or drone can be increased to support more vehicle services. However, creating more slices will inevitably increase the pressure on resource allocation, and more task types require high service stability and robustness. For the former case, we can refer to the case in Fig. 10, demonstrating that the proposed framework can maintain an acceptable task completion rate when communication and computing resources are insufficient. For the latter case, the results about varying task proportions, as in Figs. 11 and 12, can be used for reference, confirming the efficiency and robustness of the proposed framework.

2) Scalability at the Service-Coverage Level: The considered scenario, managed by an MEC controller, is reproducible. The proposed solution is controller-centric and can be deployed to MEC controllers in multiple areas to extend the service coverage. The number and position of drones in each service area can be adjusted as needed. Using the learning-based approach, each controller tailors a policy that matches the localeâs environment. Moreover, the number and location of drones can be adjusted as needed. After modification and adaptation, the proposed scheme can be applied to special scenarios (e.g., drone RANs, satelliteground networks, and satellite-drone networks).

Besides efficiency and robustness, the proposed framework keeps the control overhead low through the proposed slicing window adaptive mechanism and realizes the dual optimization of QoS and control overhead. This feature is beneficial to support more types of vehicle services and large-scale scenarios.

## VI. CONCLUSION

In this article, we have presented a slicing-based task offloading solution for SAGVNs to support diverse IoV services with differentiated QoS requirements. Unlike traditional RAN slicing approaches, the proposed framework integrates slicing window adaptation, resource slicing, and DDQN-based task scheduling, with the ability to adapt to vehicle task traffic fluctuations without future information. Trace-driven simulation results confirm that the proposed algorithm can effectively increase the number of task competitions, especially in the case of a high proportion of delay-sensitive tasks. Regarding adaptability, the proposed scheme is not constrained by the number of drones and deployment locations. With slicing window adaptation, it can balance the network-wide control overhead and QoS according to task traffic variation. For scalability, the proposed framework can support more vehicle services based on RAN slicing. Algorithms in this framework can be deployed to MEC-enabled controllers in different areas to expand service scope. In addition to task offloading, the proposed framework has the potential to support services such as content distribution and data collection. Our ongoing work will develop a federated DRL-based algorithm for large-scale SAGVNs.

## REFERENCES

[1] W. Zhuang, Q. Ye, F. Lyu, N. Cheng, and J. Ren, âSDN/NFV-empowered future IoV with enhanced communication, computing, and caching,â in Proc. IEEE, vol. 108, no. 2, pp. 274â291, Feb. 2020.

[2] R. Meneguette, R. De Grande, J. Ueyama, G. P. R. Filho, and E. Madeira, âVehicular edge computing: Architecture, resource management, security, and challenges,â ACM Comput. Surv., vol. 55, no. 1, pp. 1â46, 2023.

[3] H. Shen, Y. Heng, N. Shi, T. Wang, and G. Bai, âDrone-small-cell-assisted spectrum management for 5G and beyond vehicular networks,â in Proc. IEEE Symp. Comput. Commun., 2022, pp. 1â8.

[4] B. Cao et al., âEdgeâcloud resource scheduling in space-air-groundintegrated networks for Internet of Vehicles,â IEEE Internet Things J., vol. 9, no. 8, pp. 5765â5772, Apr. 2022.

[5] T. Pfandzelter, J. Hasenburg, and D. Bermbach, âTowards a computing platform for the LEO edge,â in Proc. 4th Int. Workshop Edge Syst. Analytics Netw., 2021, pp. 43â48.

[6] B. Mao, F. Tang, Y. Kawamoto, and N. Kato, âOptimizing computation offloading in satellite-UAV-served 6G IoT: A deep learning approach,â IEEE Netw., vol. 35, no. 4, pp. 102â108, Jul./Aug. 2021.

[7] V.-L. Nguyen, R.-H. Hwang, and P.-C. Lin, âControllable path planning and traffic scheduling for emergency services in the Internet of Vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12399â12413, Aug. 2022.

[8] L. Tao, Y. Watanabe, Y. Li, S. Yamada, and H. Takada, âCollision risk assessment service for connected vehicles: Leveraging vehicular state and motion uncertainties,â IEEE Internet Things J., vol. 8, no. 14, pp. 11548â11560, Jul. 2021.

[9] J. Zhang and K. B. Letaief, âMobile edge intelligence and computing for the Internet of Vehicles,â Proc. IEEE, vol. 108, no. 2, pp. 246â261, Feb. 2020.

[10] C. Sexton, N. Marchetti, and L. A. DaSilva, âCustomization and trade-offs in 5G RAN slicing,â IEEE Commun. Mag., vol. 57, no. 4, pp. 116â122, Apr. 2019.

[11] N. Zhang, S. Zhang, P. Yang, O. Alhussein, W. Zhuang, and X. S. Shen, âSoftware defined space-air-ground integrated vehicular networks: Challenges and solutions,â IEEE Commun. Mag., vol. 55, no. 7, pp. 101â109, Jul. 2017.

[12] J. Li et al., âA hierarchical soft RAN slicing framework for differentiated service provisioning,â IEEE Wireless Commun., vol. 27, no. 6, pp. 90â97, Dec. 2020.

[13] Q. Ye, W. Zhuang, S. Zhang, A.-L. Jin, X. Shen, and X. Li, âDynamic radio resource slicing for a two-tier heterogeneous wireless network,â IEEE Trans. Veh. Technol., vol. 67, no. 10, pp. 9896â9910, Oct. 2018.

[14] H. Peng, Q. Ye, and X. Shen, âSpectrum management for multi-access edge computing in autonomous vehicular networks,â IEEE Trans. Intell. Transp. Syst., vol. 21, no. 7, pp. 3001â3012, Jul. 2020.

[15] W. Wu et al., âDynamic RAN slicing for service-oriented vehicular networks via constrained learning,â IEEE J. Sel. Areas Commun., vol. 39, no. 7, pp. 2076â2089, Jul. 2021.

[16] H. Peng and X. Shen, âDeep reinforcement learning based resource management for multi-access edge computing in vehicular networks,â IEEE Trans. Netw. Sci. Eng., vol. 7, no. 4, pp. 2416â2428, Fourth Quarter 2020.

[17] X. Li et al., âMulti-agent DRL for resource allocation and cache design in terrestrial-satellite networks,â IEEE Trans. Wireless Commun., early access, Dec. 29, 2022, doi: 10.1109/TWC.2022.3231379.

[18] M. Chen, Y. Hao, L. Hu, K. Huang, and V. K. Lau, âGreen and mobilityaware caching in 5G networks,â IEEE Trans. Wireless Commun., vol. 16, no. 12, pp. 8347â8361, Dec. 2017.

[19] J. Ji, K. Zhu, D. Niyato, and R. Wang, âJoint cache placement, flight trajectory, and transmission power optimization for multi-UAV assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 19, no. 8, pp. 5389â5403, Aug. 2020.

[20] X. Sun and N. Ansari, âJointly optimizing drone-mounted base station placement and user association in heterogeneous networks,â in Proc. IEEE Int. Conf. Commun., 2018, pp. 1â6.

[21] E. Karimi, Y. Chen, and B. Akbari, âTask offloading in vehicular edge computing networks via deep reinforcement learning,â Comput. Commun., vol. 189, pp. 193â204, 2022.

[22] P. A. Apostolopoulos, G. Fragkos, E. E. Tsiropoulou, and S. Papavassiliou, âData offloading in UAV-assisted multi-access edge computing systems under resource uncertainty,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 175â190, Jan. 2023.

[23] C. Kai, H. Zhou, Y. Yi, and W. Huang, âCollaborative cloud-edge-end task offloading in mobile-edge computing networks with limited communication capability,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 2, pp. 624â634, Jun. 2021.

[24] Z. Bai, Y. Lin, Y. Cao, and W. Wang, âDelay-aware cooperative task offloading for multi-UAV enabled edge-cloud computing,â IEEE Trans. Mobile Comput., early access, Dec. 27, 2022, doi: 10.1109/TMC.2022.3232375.

[25] M. Li, J. Gao, L. Zhao, and X. Shen, âDeep reinforcement learning for collaborative edge computing in vehicular networks,â IEEE Trans. Cogn. Commun. Netw., vol. 6, no. 4, pp. 1122â1135, Dec. 2020.

[26] A. Bozorgchenani, S. Maghsudi, D. Tarchi, and E. Hossain, âComputation offloading in heterogeneous vehicular edge networks: On-line and offpolicy bandit solutions,â IEEE Trans. Mobile Comput., vol. 21, no. 12, pp. 4233â4248, Dec. 2022.

[27] X. Wang, Z. Ning, S. Guo, and L. Wang, âImitation learning enabled task scheduling for online fting,â IEEE Trans. Mobile Comput., vol. 21, no. 2, pp. 598â611, Feb. 2022.

[28] P. Dai, K. Hu, X. Wu, H. Xing, and Z. Yu, âAsynchronous deep reinforcement learning for data-driven task offloading in MEC-empowered vehicular networks,â in Proc. IEEE Conf. Comput. Commun., 2021, pp. 1â10.

[29] V. Erceg et al., âAn empirically based path loss model for wireless channels in suburban environments,â IEEE J. Sel. Areas Commun., vol. 17, no. 7, pp. 1205â1211, Jul. 1999.

[30] S. Zhang, H. Luo, J. Li, W. Shi, and X. Shen, âHierarchical soft slicing to meet multi-dimensional QoS demand in cache-enabled vehicular networks,â IEEE Trans. Wireless Commun., vol. 19, no. 3, pp. 2150â2162, Mar. 2020.

[31] Y. Chen, Y. Wang, M. Liu, J. Zhang, and L. Jiao, âNetwork slicing enabled resource management for service-oriented ultra-reliable and lowlatency vehicular networks,â IEEE Trans. Veh. Technol., vol. 69, no. 7, pp. 7847â7862, Jul. 2020.

[32] Y. Sun, S. Zhou, and J. Xu, âEMM: Energy-aware mobility management for mobile edge computing in ultra dense networks,â IEEE J. Sel. Areas Commun., vol. 35, no. 11, pp. 2637â2646, Nov. 2017.

[33] D. Chen, Y.-C. Liu, B. Kim, J. Xie, C. S. Hong, and Z. Han, âEdge computing resources reservation in vehicular networks: A meta-learning approach,â IEEE Trans. Veh. Technol., vol. 69, no. 5, pp. 5634â5646, May 2020.

[34] C. N. Babu and B. E. Reddy, âA moving-average filter based hybrid ARIMAâANN model for forecasting time series data,â Appl. Soft Comput., vol. 23, pp. 27â38, 2014.

[35] X. Yang, J.-Q. Hu, J. Hu, and Y. Peng, âAsynchronous value iteration for Markov decision processes with continuous state spaces,â in Proc. Winter Simul. Conf., 2020, pp. 2856â2866.

[36] Q. Ye, W. Shi, K. Qu, H. He, W. Zhuang, and X. Shen, âJoint RAN slicing and computation offloading for autonomous vehicular networks: A learning-assisted hierarchical approach,â IEEE Open J. Veh. Technol., vol. 2, pp. 272â288, Jun. 2021.

[37] F. Dai, G. Liu, Q. Mo, W. Xu, and B. Huang, âTask offloading for vehicular edge computing with edge-cloud cooperation,â World Wide Web, vol. 25, pp. 1999â2017, 2022.

[38] Y. Gao, W. Wu, J. Dong, Y. Yin, and P. Si, âDeep reinforcement learning based node pairing scheme in edge-chain for IoT applications,â in Proc. IEEE Glob. Commun. Conf., 2020, pp. 1â6.

<!-- image-->

Hang Shen (Member, IEEE) received the PhD degree (with honors) in computer science from the Nanjing University of Science and Technology. He worked as a full-time postdoctoral fellow with the Broadband Communications Research (BBCR) Lab, Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, ON, Canada, from 2018 to 2019. He is currently an associate professor with the Department of Computer Science and Technology, Nanjing Tech University, Nanjing, China. His research interests involve radio access network slicing,

space-air-ground integrated networks, network security, and privacy protection. He is an associate editor for the IEEE Access and an academic editor of the Mathematical Problems in Engineering. He was a guest editor for the Peer-to-Peer Networking and Applications and a TPC member of the Annual International Conference on Privacy, Security and Trust (PST) 2021. He is a member of the IEEE Computer Society, Communication Society, and Vehicular Technology Society and a member of the ACM.

<!-- image-->  
Yibo Tian received the BS degree in computer science from Central South University, Changsha, China. He is currently working toward the MS degree with the Department of Computer Science and Technology, Nanjing Tech University, Nanjing, China. His research interests include space-air-ground integrated networks and edge intelligence for vehicular networks.

<!-- image-->

Guangwei Bai received the BEng and MEng degrees in computer engineering from Xiâan Jiaotong University, Xiâan, China, in 1983 and 1986, respectively, and the PhD degree in computer science from the University of Hamburg, Hamburg, Germany, in 1999. From 1999 to 2001, he worked with the German National Research Center for Information Technology, Germany, as a research scientist. In 2001, he joined the University of Calgary, Calgary, AB, Canada, as a research associate. Since 2005, he has been working with Nanjing Tech University, Nanjing, China, as a

<!-- image-->

Tianjing Wang (Member, IEEE) received the BSc degree in mathematics from Nanjing Normal University, in 2000, the MSc degree in mathematics from Nanjing University, in 2002, and the PhD degree in signal and information system with the Nanjing University of Posts and Telecommunications, in 2009. From 2011 to 2013, she was a postdoctoral fellow with the School of Electronic Science and Engineering, Nanjing University of Posts and Telecommunications. From 2013 to 2014, she was a visiting scholar with the Department of Electrical and Computer Enprofessor in computer science. From October to December 2010, he was a visiting professor with the Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, ON, Canada. His research interests include architecture and protocol design for communication networks, QoS, multimedia networking, network security, and location-based services. He is a member of the ACM and a distinguished member of the CCF.

gineering, State University of New York at Stony Brook. She is now an associate professor with the Department of Communication Engineering, Nanjing Tech University. Her research interests include vehicular networks and distributed machine learning.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_5_img_1.png|page_5_img_1]]
2. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_6_img_1.jpeg|page_6_img_1]]
3. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_7_img_1.png|page_7_img_1]]
4. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_8_img_1.png|page_8_img_1]]
5. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_11_img_1.jpeg|page_11_img_1]]
6. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_13_img_1.png|page_13_img_1]]
7. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_14_img_1.png|page_14_img_1]]
8. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_16_img_1.jpeg|page_16_img_1]]
9. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_17_img_1.jpeg|page_17_img_1]]
10. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_17_img_2.jpeg|page_17_img_2]]
11. [[../extracted_images/Shen 等 - 2024 - Slicing-Based Task Offloading in Space-Air-Ground /page_17_img_3.jpeg|page_17_img_3]]

---

