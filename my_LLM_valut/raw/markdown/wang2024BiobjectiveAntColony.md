# Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC Systems

Yiqian Wang , Jie Zhu , Haiping Huang , Member, IEEE, and Fu Xiao , Member, IEEE

AbstractâIn the paper, the Unmanned Aerial Vehicle (UAV) path planning and task offloading problem in UAV-assisted mobile edge computing (MEC) systems is investigated. A bi-criterion ant colony optimization (bi-ACO) framework is proposed for the considered problem with the objectives of minimizing the total cost and the completion time, meanwhile satisfying the energy, deadline, location, and priority constraints. In the bi-ACO framework, multiple heterogeneous colonies are introduced with different preferences of objectives. Each colony maintains five pairs of pheromone matrices for constructing feasible solutions. Besides the colony settings, three key components of bi-ACO are delicately designed: feasible solution generation method (FSGM) to construct a feasible solution, solution division method (SDM) to improve obtained solutions of good quality, and pheromone update method (PUM) to updates pheromone matrices by pheromone evaporation operation and pheromone enhancement operation based on the preferences of colonies. Four Pareto-based metrics are introduced to evaluate the performance of the compared algorithms. Experimental results show that the proposal outperforms the compared baseline algorithms in effectiveness and robustness.

Index TermsâACO, mobile edge computing, task offloading, trajectory planning, UAV.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs) are gaining moreand more popularity in a wide range of applications in transportation, disaster management, agriculture and health care.

<!-- image-->  
(a) Quasi-static deployment

<!-- image-->  
(b) Mobile deployment  
Fig. 1. UAV deployment modes.

Various difficulties in ground operations such as traffic congestion, extensive labor costs and severe weather conditions can be relieved by employing UAVs. In these UAV-assisted systems, UAVs can be provisioned as mobile base stations [1], mobile relays [2], mobile caches [3] and mobile surveillance [4].

One of the prevalent UAV-assisted innovative solutions is the UAV-assisted mobile edge computing (MEC) system where UAVs are equipped with powerful CPUs and taken as the roaming edge computing devices. In the general MEC systems, many smart devices (SDs) periodically collect and upload data to nearby base stations which then perform complex computing on these data and return results to SDs. The energy consumption of SDs is one of the major issues for the continuous availability of MEC applications. Introducing UAVs as mobile base stations can greatly reduce the energy consumption for data transmission which is the major energy consumption of SDs. Besides, the UAVs can also enhance the intelligent capabilities of MEC systems by playing as edge computing devices to perform complex computing on data.

In many UAV-assisted systems, UAVs are deployed as the air interfaces in the quasi-static manner [5], [6] (as shown in Fig. 1(a)). In these cases, each UAV serves for multiple SDs in a given area. The quasi-static UAVs may periodically adjust the locations but most of the time they stay at the fixed locations. If SDs are deployed sparsely, more quasi-static UAVs would be provisioned or the serving area of each UAV would be expanded. The former leads to a higher cost, and the latter reduces the quality of service.

Digital Object Identifier 10.1109/TMC.2024.3408603

The quasi-static deployment of UAVs does not take full advantage of the excellent maneuverability of the UAVs. Many benefits can be introduced by employing mobile UAVs in the UAV-assisted MEC systems (as shown in Fig. 1(b)). First, provisioning UAVs in the mobile manner is suitable for either sparse or dense deployment of SDs. Second, the locations of UAVs can be adaptive to the distribution of workload. Third, the UAVs can process data while flying to further improve the effectiveness of the systems.

In the paper, we consider an UAV scheduling problem where the trajectory planning and the multi-stage task offloading are jointly optimized. Many SDs are distributed in a given area and submit computation tasks periodically. The computation tasks are deadline-constraint and divided into three stages: the data transmission stage, the task computation stage and the result transmission stage. A fixed number of reserved UAVs are provisioned in several base stations and serving the area. In order to satisfy the deadline constraint in cases of heavy workload, an unlimited number of on-demand UAVs at a higher cost can be employed. The objectives are to minimize the total cost and the completion time of all tasks. The novelty of the problem under study lies in below. (i) The computation tasks are multi-stage tasks. Different task stages have different limitations for UAVs to fly or hover. (ii) Each SD should be visited twice for data fetching and result returning, and the time gap between two successive visits of a SD should be long enough to complete a task. (iii) UAVs are elastic resources with different price structures.

It is known that the multiple UAV trajectory planning problem has already proved to be NP-hard [7]. Therefore, it follows that the problem optimizing both the trajectory planning and the task offloading is also NP-hard. Offloading multi-stage tasks to geographically distributed and flying UAVs results in great challenges: (i) Energy management is critical for the considered problem. The energy capacity of each UAV is restricted. In order to gain an energy-efficient solution, the hovering time, the flying time and the time to change batteries should be elaborately planned. (ii) The trajectories of UAVs are more difficult to plan since each SD could be visited once or twice. An UAV can hover near a SD for the entire duration of the task, or leave during the computation stage and fly back for the result transmission. Therefore, a timetable of processing different stages of tasks should also be given. (iii) It is not easy to obtain an efficient task offloading solution. The sequence of SDs to visit in a trajectory planning only determines the order of the data and result transmission stages of tasks. The order of the computation stages of tasks assigned to the same UAV should be delicately scheduled. (iv) It is difficult to balance the conflicting objectives. In order to reduce the total cost, it is better to employ the on-demand UAVs as less as possible. However, the reserved UAVs may be overloaded and the deadline constraint may be not guaranteed or the completion time may be extended.

The paper aims to provide an effective and efficient method for the multiple UAV scheduling problem. The main novelty and contributions of this paper are summarized as follows.

1) Considering the energy consumption of UAVs and the characteristics of multi-stage tasks, a jointly trajectory planning and multi-stage task offloading problem model is formulated for scheduling multiple UAVs with multiple pricing structures.

2) We design an effective heuristics FSGM for quickly constructing feasible solutions for the trajectory planning and task offloading of every UAV. The heuristics includes several innovative components designed specially for the problem under study. The swapping task insertion method guarantees the energy constraint during the task offloading process. The task insertion method inserts tasks into appropriate positions depending on the pheromone intensity. The boundary update method helps the task insertion method to avoid unnecessary trials. Besides, a probabilistic loop-breaking step is designed to balance the workload of UAVs.

3) Solution division method (SDM) is developed to further reconstructed to new solution by the solution division method. Solution division method (SDM) can help improve the diversity of solutions.

4) A bi-objective ant colony optimization (bi-ACO) framework is proposed to generate near-Pareto-optimal solution set. bi-ACO is an enhanced variant of general ACO. It is integrated with many effective components designed especially for the problem under study. The novelty of bi-ACO lies in the following aspects. (1) Multiple heterogeneous colonies are introduced with different preferences of objectives. (2) One pair of pheromone matrices is used for computing the probability of task selection. (3) Four pairs of pheromone matrices are used to determine the insertion position of a task. (4) The pheromone update method is employed with the delicately designed pheromone evaporation operation and the pheromone enhancement operation which fully consider different stage of tasks.

The rest of the paper is organized as follows. Section II gives the review of the related works. The problem under study is formulated in Section III. Section IV introduces the proposed algorithm and its major components. Delicate experiments are designed to compare the proposal and the baseline algorithms in Section V, followed by conclusions and future research in Section VI.

## II. RELATED WORK

There have been many studies on UAV-assisted systems for these years. Deploying UAVs in these systems as the flying base stations [1], computation components [8], tracking agents [4] or logistics containers [9] provides a flexible and effective approach for many on-demand scenarios. The main research issues in these UAV-assisted systems can be classified into four categories: (1) computation task offloading problem, (2) UAV trajectory planning problem, (3) the hybrid problem of task offloading and UAV trajectory planning and (4) UAV placement/deployment problem.

In the UAV-assisted systems involving only the task offloading problem, the employed UAVs are usually quasi-static. In the case of quasi-static UAVs, the UAVs hover at fixed locations to provide computation or communication capabilities. They barely adjust the hovering locations, or periodically adjust the hovering locations. Luan et al. [10] consider a joint optimization of topology reconstruction and subtask scheduling in the cellular Internet of UAV-assisted MEC emergency system. A hybrid subtask scheduling scheme is presented to make optimal task scheduling decisions. There is a few studies on how to determine the appropriate hovering locations depending on the task allocation decision. Du et al. [11] introduce the UAV-enabled wirelessly-powered MEC system for IoT devices. They relax the task offloading and path planning problems into a convex problem and apply the flow-shop scheduling techniques to address it. Zhang et al. [12] explore the task offloading problem in an UAV-assisted edge computing system, where a number of ground mobile devices are served by a flying UAV and a ground base station. A game theory-based scheme is constructed and the existence of Nash equilibrium is proved. Liao et al. [13] establish a new UAV swarm-enabled MEC network where UAVs are deployed to support time-constrained and low-resource unmanned surface vehicle communication and computation. The offloading decision is formulated as mixed-integer non-linear programming and solved by a modified deferred acceptance algorithm.

UAV trajectory planning problem usually exists in the surveillance, damage assessment, delivery or search and rescue operations where there are a given set of target points to visit by a squad of UAVs. Wang et al. [14] introduce a low-altitude UAV platform as both a mobile data collector and an aerial anchor node to assist in data collection and device positioning. They develop an efficient differential evolution based method to obtain the UAV trajectory. Bartolini et al. [15] investigate the trajectory planning problem in the monitoring critical scenarios requiring early anomaly discovery and intervention. They propose an efficient polynomial algorithm, called Greedy and Prune, with the objective of maximizing weighted progressive coverage. Sun et al. [16] use an efficient ant colony-based algorithm to optimize the flight path of UAVs in the scenario of vessel monitoring. Rigas et al. [17] schedule a set of UAVs across a graph where the nodes need to be visited multiple times at pre-defined points in time. An greedy heuristics and an ant colony optimization algorithm are designed for the problem. Huang et al. [9] study the dynamic task scheduling and path planning problem in the UAV-based intelligent on-demand meal delivery system. The Roulette-based flight dispatching approach is integrated into the simulated annealing based local search method to optimize the solutions. Hu et al. [18] investigate RIS-assisted UAV-borne IoT platform under jamming. Without utlizing the channel state information (CSI), they apply a deep reinforcement learning based method to learn the trajectory of UAV as well as its reconfigurable intelligent surface (RIS) configuration to better eliminate the jamming. Kang et al. [19] design a UAV-assisted data fusion method to efficiently collect data from IoT devices. First, the method gathers the data to clustering heads (CHs) nodes in the ground. Then the paths of multiple UAVs are optimized to collect data from CHs by formulating the problem to a multi-UAV problem.

There are also some studies on the UAV trajectory planning in the UAV-assisted networks, where the UAV trajectory planning problem is critical to guarantee communication. Zhao et al. [20] investigate the UAV-assisted network where the UAV and base station serve ground users simultaneously. The method of block coordinate descent is applied for the UAV trajectory planning. Pang et al. [21] introduce the UAV into the wireless networks in order to enhance the secure transmission. An iterative heuristics is employed to solve the problem. Prasad and Ramkumar [22] consider the trajectory planning problem in a relay-based UAV-assisted cooperative communication for emergency applications. UAVs are used as both static base stations (cluster UAVs) and mobile base stations (relay UAVs). The Dijkstra algorithm is used to determine the optimal trajectory of UAVs. Eldeeb et al. [23] formulate an optimization problem in an IoT network, while minimizing the Age of Information (AoI) and energy consumption. They apply a deep reinforcement learning algorithm for the considered problem.

Many complex UAV-assisted systems need to solve both the task offloading and UAV trajectory planning problems. Most of the problems involve only one UAV and a set of tasks distributed in a given region. Sun et al. [24] jointly optimize the trajectory and CPU frequency of a fixed-wing UAV, and the offloading schedule to minimize the energy consumption of the UAV. An alternating optimization- and a successive convex approximationbased algorithms are developed to achieve the globally optimal linear trajectory, CPU configuration, and offloading schedule. Lin et al. [25] address the issue of how to effectively serve a 3-D wireless rechargeable sensor network with one UAV. They reduce the problem into a sub-modular maximization problem with routing constraints and present a cost-efficient algorithm. There are a few of studies on the trajectory planning and task scheduling for multiple UAVs. Miao et al. [26] raise a multi-UAVs-assisted MEC offloading algorithm for matching the dynamic mobile devices and UAV trajectory. In their proposal, first, a drone swarm scheduling and allocation strategy is developed to minimize the global flight length and energy consumption. Second, the optimal communication coverage of an UAV is computed to maximize the number of offloading services and minimize the total latency in completing the computation task. Finally, an UAV cluster computation offloading strategy with optimized energy efficiency is implemented. Khochare et al. [27] investigate a mission scheduling problem which co-schedules the UAV flight routes to visit and record video at waypoints, and their subsequent on-board edge analytics. They formulate the considered problem into a mixed integer linear programming problem and solve it accordingly. Tian et al. [28] study the service satisfaction-oriented task offloading and UAV scheduling problem for UAV-enabled MEC networks. Two genetic algorithms are proposed to solve the UAV scheduling sub-problem and the task offloading sub-problem, respectively.

The UAV placement or deployment problem exists in scenarios where the mobile network infrastructure is unable to provide wireless coverage. Yu et al. [29] study the placement problem of the UAV-mounted base stations. A backhaul-aware bandwidth allocation and an UAV placement algorithm are designed to efficiently solve the problem. Luo et al. [30] introduce the cached-enabled UAVs to provide on-demand content services for ground users. A weighted K-means method is employed for the UAV deployment problem. Liu et al. [31] study the UAV placement problem with the objective of maximizing the fair coverage versus energy consumption while satisfying the backhaul constraints. An accurate and efficient proximal stochastic gradient descent based alternating algorithm is proposed to optimize the UAV locations. Fazel et al. [32] use the fast global K-means algorithm to determine the number of UAVs and their horizontal placements. Then, the altitudes of UAVs are optimized by the interior-point method.

In our previous study [33], we investigate the task scheduling and trajectory planning problem in the UAV-enabled Mobile Edge-Computing system with the objectives of minimizing the cost and the completion time. A NSGA-II algorithm is proposed for the problem. In this paper, we investigate a similar problem and take our previous work as one of the baseline studies. Our simulation results will show that the proposed method in the paper outperforms the benchmark algorithms either in effectiveness or efficiency.

## III. PROBLEM DESCRIPTION

The notations used for the problem formulation are given in Table I.

In the considered problem, there are n SDs distributed in the given area. Each SD collects nearby data and generates one computation requirement periodically. Each computation requirement is taken as a task to be processed. The set $\mathbb { T } =$ $\{ T _ { 1 } , \ldots , T _ { n } \}$ includes the tasks to process in one period. We assume the release times of these tasks are the same and given. The computation resources considered are homogeneous, which means the computation and communication times of tasks are resource-independent. Therefore, task $T _ { i }$ can be described by a 5-tuple $< D T ( T _ { i } ) , P ( T _ { i } ) , R T ( T _ { i } ) , L ( T _ { i } ) , D ( T _ { i } ) >$ , where $D T ( T _ { i } )$ is the data transmission time, $P ( T _ { i } )$ is the task processing time, $R T ( T _ { i } )$ is the result transmission time and $L ( T _ { i } )$ is the location of $T _ { i }$ . In order to guarantee the data freshness, task $T _ { i }$ is assigned a deadline $D ( T _ { i } )$ . The computation resources are UAVs equipped with GPS, WiFi and computing modules. There are two types of UAVs: reserved UAVs and on-demand UAVs. $\mathbb { U } = \{ U _ { 1 } , \ldots , U _ { m } \}$ contains m reserved UAVs. Reserved UAVs can be taken as the computation resources with long-term contracts with lower price Î± per time unit $\varepsilon , \Psi ^ { \prime }$ contains employed on-demand UAVs. On-demand UAVs are temporary resources with higher unit price $\beta$ per time unit Îµ. The average flying speed of UAVs is $\nu .$ . The flying time from one location to another can be simply computed by $\overset { \mathbb { D } } { \frac { \mathbb { D } ( L , L ^ { \prime } ) } { \nu } }$ , where $\mathbb { D } ( L , L ^ { \prime } )$ is the distance between two locations $L$ and $L ^ { \prime }$ . Both reserved and on-demand UAVs are originally fully charged and provisioned in the base stations. We use B to denote the set of base stations. The initial location of $U _ { j }$ is $L ^ { 0 } ( U _ { j } ) \in \mathbb { B } . { \mathrm { U A V s } }$ could swap batteries at any base station and the swapping operation is assumed to take only one time unit Îµ.

The energy consumption $\mathbb { P } ( v )$ in watt (W) is defined as the function of the flying speed v (1). The energy consumption of rotary-wing UAVs consists of three components: blade profile, induced, and parasite power. For convenience, we employ all the constants and parameter settings directly from [34]. $\mathbb { P } ( 0 )$ is the energy consumption by a hovering UAV. The maximum energy capacity of an UAV is $E _ { \mathrm { m a x } }$ . Note that the GPS, WiFi and computation modules on an UAV are equipped with their own power system. The energy consumption for computing and data transmission are not considered in the problem model.

TABLE I NOTATIONS
<table><tr><td>Notation</td><td>Definition</td></tr><tr><td>n</td><td>Number of SDs/tasks</td></tr><tr><td> $\mathbb { T } = \{ T _ { 1 } , \dots , T _ { n } \}$ </td><td>Set of tasks</td></tr><tr><td> $T _ { i }$ </td><td> $i ^ { t h }$  task</td></tr><tr><td> $D T ( T _ { i } )$ </td><td>Data transmission time of  $T _ { i }$ </td></tr><tr><td> $P ( T _ { i } )$ </td><td>Processing time of  $T _ { i }$ </td></tr><tr><td> $R T ( T _ { i } )$ </td><td>Result transmission time of  $T _ { i }$ </td></tr><tr><td> $L ( T _ { i } )$ </td><td>Location of  $T _ { i }$ </td></tr><tr><td> $D ( T _ { i } )$ </td><td>Deadline of  $T _ { i }$ </td></tr><tr><td>m</td><td>Number of reserved  $\mathrm { U A V s }$ </td></tr><tr><td> $\mathbb { U } = \{ U _ { 1 } , \ldots , U _ { m } \}$ </td><td>Setof reserved UAVs</td></tr><tr><td> $U _ { j }$ </td><td> $j ^ { t h }$  UAV in U</td></tr><tr><td> $\mathbb { U } ^ { \prime }$ </td><td>Set of on-demand UAVs</td></tr><tr><td> $\varepsilon$ </td><td>Charing time unit of UAVs</td></tr><tr><td> $\alpha , \beta$ </td><td>Charing_prices of reserved and on- demand UAVs per time unit Îµ</td></tr><tr><td> $\nu$ </td><td>Average flying speed of UAVs</td></tr><tr><td> $\mathbb { D } ( L , L ^ { \prime } )$ </td><td>Distance between locations L and  $L ^ { \prime }$ </td></tr><tr><td>B</td><td>Set of base stations</td></tr><tr><td> $L ^ { 0 } ( U _ { j } ) \in \mathbb { B }$ </td><td>Initial location of  $U _ { j }$ </td></tr><tr><td> $\mathbb { P } ( v )$ </td><td>Energy consumption in watt with the</td></tr><tr><td> $E _ { m a x }$ </td><td>flying speed u Maximum energy capacity of an UAV</td></tr><tr><td> $T _ { i , 1 } , T _ { i , 2 } , T _ { i , 3 }$ </td><td>Three sub-tasks of  $T _ { i }$ </td></tr><tr><td> $S ( T _ { i , h } )$ </td><td>Starting time of  $T _ { i , h } , h = 1 , 2 , 3$ </td></tr><tr><td> $C ( T _ { i , h } )$ </td><td>Completion time of  $T _ { i , h } , h = 1 , 2 , 3$ </td></tr><tr><td> $a _ { i }$ </td><td>Task assignment of  $T _ { i }$ </td></tr><tr><td> $U ( T _ { i } )$ </td><td>UAV allocated to  $T _ { i }$ </td></tr><tr><td> $K _ { j }$ </td><td>Number of sub-tasks assigned to</td></tr><tr><td> $\pi _ { j } = ( \pi _ { j , 1 } , \ldots , \pi _ { j , K _ { j } } )$ </td><td> $U _ { j }$  Task assignment of  $U _ { j }$ </td></tr><tr><td> $\pi _ { j , k }$ </td><td> $k ^ { t h }$  task in Ï</td></tr><tr><td> $T _ { s w a p }$ </td><td>Swapping-battery task</td></tr><tr><td> $L _ { s } ( \pi _ { j , k } )$ </td><td>Location of UAV at time  $S ( \pi _ { j , k } )$ </td></tr><tr><td> $L _ { c } ( \pi _ { j , k } )$ </td><td>Location of UAV at time  $C ( \pi _ { j , k } )$ </td></tr><tr><td> ${ \mathbb S } = < A , \Pi >$ </td><td>Schedule solution</td></tr><tr><td> $A$ </td><td>Set of task assignments</td></tr><tr><td> $\Pi$ </td><td>Set of UAV assignments</td></tr><tr><td> $E _ { j } ( t )$ </td><td>Residual energy of  $U _ { j }$  at time t</td></tr><tr><td> $T C ( \mathbb { S } )$ </td><td>Total cost of S</td></tr><tr><td> $C T ( \mathbb { S } )$ </td><td>Completion time of S</td></tr></table>

$$
\begin{array} { r l } & { \mathbb { P } ( v ) = \underbrace { 0 . 0 4 4 v ^ { 2 } + 5 8 0 } _ { \mathrm { b l a d e ~ p r o f l e } } + \underbrace { 0 . 0 0 7 3 v ^ { 3 } } _ { \mathrm { p a r a s i t e } } } \\ & { \qquad + \underbrace { 7 9 0 . 6 7 \left( \sqrt { 1 + \frac { v ^ { 4 } } { 1 0 7 5 0 } } - \frac { v ^ { 2 } } { 1 0 3 . 6 8 } \right) ^ { \frac { 1 } { 2 } } } _ { \mathrm { i n d u c e d } } } \end{array}\tag{1}
$$

There are three stages for processing task $T _ { i }$ by an assigned UAV $U _ { j }$ as follows.

- Data Transmission (DT) stage. In this stage, $U _ { j }$ hovers on top of the corresponding SD and receives data of $T _ { i }$

- Data Computation (DC) stage. In this stage, $U _ { j }$ could hover near the SD or fly to another location.

Result Transmission (RT) stage. In this stage, $U _ { j }$ hovers on top of the corresponding SD and sends the result of $T _ { i }$ to SD.

Sub-tasks $T _ { i , 1 } , T _ { i , 2 }$ and $T _ { i , 3 }$ are introduced to represent three stages of $T _ { i }$ . Once a sub-task starts, it cannot be interrupted until it is completed. An UAV can only take one sub-task at a time and multi-thread mode is not considered. We employ $S ( T _ { i , h } ) / C ( T _ { i , h } )$ to denote the starting/completion times of $T _ { i , h }$ $( h = 1 , 2 , 3 )$

An assignment $a _ { i }$ of $T _ { i }$ is represented by a 7-tuple $<$ $U ( T _ { i } ) , S ( T _ { i , 1 } ) , C ( T _ { i , 1 } ) , S ( T _ { i , 2 } ) , C ( T _ { i , 2 } ) , S ( T _ { i , 3 } ) , C ( T _ { i , 3 } ) > .$ $U ( T _ { i } )$ is the UAV that $T _ { i }$ is assigned to. Accordingly, the assignment $\pi _ { j }$ of $U _ { j }$ can be represented by a sub-task sequence $\pi _ { j } = ( \pi _ { j , 1 } , \pi _ { j , 2 , \cdot \cdot \cdot , \pi _ { j , K _ { j } } } )$ , where $\pi _ { j , k } ( k = 1 , \ldots , K _ { j } )$ could be a sub-task or a swapping-battery task ${ \cal T } _ { s w a p } . K _ { j }$ is the number of sub-tasks (including swapping-battery tasks) assigned to $U _ { j }$ We define $L _ { s } ( \pi _ { j , k } )$ and $L _ { c } ( \pi _ { j , k } )$ as the locations at the times of $S ( \pi _ { j , k } )$ and $C ( \pi _ { j , k } )$ , respectively. $S ( \pi _ { j , k } ) / C ( \pi _ { j , k } )$ is the starting/completion time of $\pi _ { j , k }$

The schedule solution ${ \mathbb S } = < A , { \Pi } >$ of the considered problem is composed of the set of task assignments $A = \{ a _ { i } | i =$ $1 , \ldots , n \}$ and the set of UAV assignments $\Pi = \{ \pi _ { j } | U _ { j } \in \mathbb { U } \cup$ U - }. The schedule is feasible if and only if the following constraints are satisfied.

- Precedence constraint limits that a task should be processed in order of stages. Equ. (2) restricts that a stage can start only when its previous stage is completed.

- Location constraint is defined to restrict the motion of UAVs. When an UAV is processing the $1 ^ { s t }$ or $3 ^ { r d }$ stage sub-task, it must hover at the location of the sub-task until the sub-task is completed. The constraint is defined by (3).

Priority constraint restricts that the sub-tasks assigned to the same UAV should be processed in order of the sub-task sequence. A sub-task $\pi _ { j , k }$ in $\pi _ { j }$ can start only when $\pi _ { j , k - 1 }$ is completed. The constraint is defined by (4)â(5). Equ. (5) implies that the first sub-task of an UAV cannot start until the assigned UAV arrives at the location of the sub-task.

- Deadline constraint means that the completion time of a task cannot exceed its deadline. It is defined by (6).

Non-overlapping constraint makes sure that the processing times of sub-tasks on the same UAV cannot overlap in time. The constraint can be defined by (7).

Energy constraint guarantees each UAV has sufficient energy at any time during task execution. We use $E _ { j } ( t )$ to represent the residual energy of $U _ { j }$ at time t. $E _ { j } ( t )$ cannot be negative at any time. The energy constraint is defined by (8)â(15). Equ (8) indicates the residual energy of $U _ { j }$ at the starting time of $\pi _ { j , k }$ cannot be negative. The residual energy of $U _ { j }$ at the completion time of each sub-task cannot be negative as well (9). In order to compute $E _ { j } ( S ( \pi _ { j , k } ) )$ and $E _ { j } ( C ( \pi _ { j , k } ) )$ , we introduce two new notations: $\Delta E _ { j , k }$ to represent the energy consumption in the duration of sub-task $\pi _ { j , k }$ and $\Delta G _ { j , k }$ to represent the energy consumption during the time gap between two consecutive sub-tasks. There would be time gap between two consecutive sub-tasks. The time gap takes place when the UAV is idle and on the way flying to the next sub-task.

Equ (10) means the energy difference of $U _ { j }$ between the starting and completion time of $\pi _ { j , k }$ is $\Delta E _ { j , k }$ . Equ (11) means the energy consumed during the time gap between $C ( \pi _ { j , k - 1 } )$ and $S ( \pi _ { j , k } )$ is $\Delta G _ { j , k } . \ \Delta E _ { j , k }$ depends on the type of $\pi _ { j , k } ( 1 2 )$ . If Ïj,k is $T _ { s w a p } , U _ { j }$ would be fully charged at time $C ( \pi _ { j , k } )$ . If $\pi _ { j , k }$ is the $1 ^ { s t }$ or $3 ^ { r d }$ stage sub-task, the energy would be consumed based on the hovering duration. Otherwise, the consumed energy would include two parts: flying and hovering energy consumption. The flying time $t _ { j , k } ^ { \check { f } l y }$ of $U _ { j }$ during processing $\pi _ { j , k }$ depends on the distance it moves (13). Since the total duration of $\pi _ { j , k }$ is $P ( \pi _ { j , k } )$ ï¼ the hovering time $t _ { j , k } ^ { h o v e r }$ during processing $\pi _ { j , k }$ can be computed by (14). $\check { \Delta } G _ { j , k }$ can be computed by (15)).

$$
C ( T _ { i , 1 } ) \leq S ( T _ { i , 2 } ) , C ( T _ { i , 2 } ) \leq S ( T _ { i , 3 } )\tag{2}
$$

$$
i = 1 , \ldots , n
$$

$$
L _ { s } ( T _ { i , h } ) = L _ { c } ( T _ { i , h } ) = L ( T _ { i , h } ) , h = 1 , 3\tag{3}
$$

$$
S ( \pi _ { j , k } ) \ge C ( \pi _ { j , k - 1 } ) + \frac { \mathbb { D } ( L _ { c } ( \pi _ { j , k - 1 } ) , L _ { s } ( \pi _ { j , k } ) ) } { \nu }\tag{4}
$$

$$
S ( \pi _ { j , 1 } ) \geq \frac { \mathbb { D } ( L ^ { 0 } ( U _ { j } ) , L ( \pi _ { j , 1 } ) ) } { \nu }\tag{5}
$$

$$
C ( T _ { i } ) \leq D ( T _ { i } )\tag{6}
$$

$$
\operatorname* { m i n } \{ C ( T _ { i , h } ) , C ( T _ { i ^ { \prime } , h } ) \} \leq \operatorname* { m a x } \{ S ( T _ { i , h } ) , S ( T _ { i ^ { \prime } , h } ) \}\tag{7}
$$

$$
U ( T _ { i } ) = U ( T _ { i ^ { \prime } } ) , h = 1 , 2 , 3
$$

$$
E _ { j } ( C ( \pi _ { j , k } ) ) \ge 0
$$

$$
E _ { j } ( S ( \pi _ { j , k } ) ) \ge 0\tag{8}
$$

$$
E _ { j } ( C ( \pi _ { j , k } ) ) = E _ { j } ( S ( \pi _ { j , k } ) ) - \Delta E _ { j , k }\tag{9}
$$

$$
E _ { j } ( S ( \pi _ { j , k } ) ) = E _ { j } ( C ( \pi _ { j , k - 1 } ) ) - \Delta G _ { j , k }\tag{10}
$$

(11)

$$
\begin{array} { r } { \Delta E _ { j , k } = \left\{ \begin{array} { l l } { E _ { j } ( S ( \pi _ { j , k } ) ) - E _ { \operatorname* { m a x } } , } & { \pi _ { j , k } = T _ { s w a p } } \\ { \mathbb { P } ( 0 ) D T ( T _ { i } ) , } & { \pi _ { j , k } = T _ { i , 1 } } \\ { \mathbb { P } ( 0 ) R T ( T _ { i } ) , } & { \pi _ { j , k } = T _ { i , 3 } } \\ { \mathbb { P } ( \nu ) t _ { j , k } ^ { f l y } + \mathbb { P } ( 0 ) t _ { j , k } ^ { h o v e r } , } & { \pi _ { j , k } = T _ { i , 2 } } \end{array} \right. } \end{array}\tag{12}
$$

$$
t _ { j , k } ^ { f l y } = \frac { \mathbb { D } ( L _ { s } ( \pi _ { j , k } ) , L _ { c } ( \pi _ { j , k } ) ) } { \nu }\tag{13}
$$

$$
t _ { j , k } ^ { h o v e r } = P ( \pi _ { j , k } ) - t _ { j , k } ^ { f l y }\tag{14}
$$

$$
\Delta G _ { j , k } = \mathbb { P } ( \nu ) \times \frac { \mathbb { D } ( L _ { c } ( \pi _ { j , k - 1 } ) , L _ { s } ( \pi _ { j , k } ) ) } { \nu }\tag{15}
$$

Fig. 2 gives examples of two solutions. There are three tasks to schedule and two UAVs provisioned in two base stations respectively in Fig. 2. The information of tasks is shown in Table II. In the solution $\begin{array} { r l } { \mathrm { S } _ { 1 } } & { { } ( \mathrm { F i g . } \quad 2 ( \mathrm { a } ) ) } \end{array}$ , only $U _ { 1 }$ is employed. Its assignment $\pi _ { 1 }$ is $( T _ { 1 , 1 } , T _ { 1 , 2 } , T _ { 2 , 1 }$ , $T _ { 2 , 2 } , T _ { 3 , 1 } , T _ { 3 , 2 } , T _ { s w a p } , T _ { 1 , 3 } , T _ { 2 , 3 } , T _ { 3 , 3 } , T _ { s w a p } )$ . The Gantt chart of the solution is shown in Fig. 3(a). Table III gives the detail of the task assignments. In the solution $\mathbb { S } _ { 2 }$ (Fig. 2(b)), two UAVs $U _ { 1 }$ and $U _ { 2 }$ are employed. The assignment $\pi _ { 1 }$ is $( T _ { 1 , 1 } , T _ { 1 , 2 } , T _ { 2 , 1 } , T _ { 2 , 2 } , T _ { 2 , 3 } , T _ { 1 , 3 } , T _ { s w a p } )$ . The assignment $\pi _ { 2 }$ is $( T _ { 3 , 1 } , T _ { 3 , 2 } , T _ { 3 , 3 } , T _ { s w a p } )$ . The Gantt chart of the solution is shown in Fig. 3(b). Table IV gives the details of the task assignments.

<!-- image-->  
Fig. 2. Examples of solutions.

TABLE II  
INFORMATION OF TASKS
<table><tr><td></td><td> $D T ( T _ { i } )$ </td><td> $P ( T _ { i } )$ </td><td> $R T ( T _ { i } )$ </td><td> $D ( T _ { i } )$ </td></tr><tr><td> $T _ { 1 }$ </td><td>2</td><td>5</td><td>1</td><td>100</td></tr><tr><td> $T _ { 2 }$ </td><td>3</td><td>3</td><td>1</td><td>100</td></tr><tr><td> $T _ { 3 }$ </td><td>1</td><td>7</td><td>1</td><td>100</td></tr></table>

<!-- image-->

(a) Gantt chart of S1  
<!-- image-->  
Fig. 3. Gantt charts.

TABLE III  
TASK ASSIGNMENTS OF SOLUTION 1
<table><tr><td colspan="7"> $U ( T _ { i } )$   $S ( T _ { i , 1 } )$   $C ( T _ { i , 1 } )$   $S ( T _ { i , 2 } )$   $C ( T _ { i , 2 } )$   $S ( T _ { i , 3 } )$   $C ( T _ { i , 3 } )$ </td></tr><tr><td> $T _ { 1 }$ </td><td> $U _ { 1 }$ </td><td>10</td><td>12</td><td>12</td><td>17</td><td>62</td></tr><tr><td> $T _ { 2 }$ </td><td> $U _ { 1 }$ </td><td>27</td><td>30</td><td>30</td><td>33 78</td><td>63 79</td></tr><tr><td> $T _ { 3 }$ </td><td> $U _ { 1 }$ </td><td>42</td><td>43 43</td><td>50</td><td>91</td><td>92</td></tr></table>

Given a feasible S, its total cost T C(S) and the completion time $C T ( \mathbb { S } )$ can be computed by (16)â(17).

$$
T C ( \mathbb { S } ) = \alpha \sum _ { j \in \mathbb { U } } C ( \pi _ { j , K _ { j } } ) + \beta \sum _ { j \in \mathbb { U } ^ { \prime } } C ( \pi _ { j , K _ { j } } )\tag{16}
$$

TABLE IV  
TASK ASSIGNMENTS OF SOLUTION 2
<table><tr><td colspan="8"> $U ( T _ { i } )$   $S ( T _ { i , 1 } )$   $C ( T _ { i , 1 } )$   $S ( T _ { i , 2 } )$   $C ( T _ { i , 2 } )$   $S ( T _ { i , 3 } )$   $C ( T _ { i , 3 } )$ </td></tr><tr><td> $T _ { 1 }$ </td><td> $U _ { 1 }$ </td><td>10</td><td>12</td><td>12</td><td>17</td><td>49</td><td>50</td></tr><tr><td> $T _ { 2 }$ </td><td> $U _ { 1 }$ </td><td>27</td><td>30</td><td>30</td><td>33</td><td>33</td><td>34</td></tr><tr><td> $T _ { 3 }$ </td><td> $U _ { 2 }$ </td><td>10</td><td>11</td><td>11</td><td>18</td><td>18</td><td>19</td></tr></table>

$$
C T ( \mathbb { S } ) = \operatorname* { m a x } _ { i = 1 } ^ { n } C ( T _ { i } )\tag{17}
$$

As the solutions $\mathbb { S } _ { 1 }$ and $\mathbb { S } _ { 2 }$ shown in Fig. 3, $\mathbb { S } _ { 1 }$ employs only one reserved UAV $U _ { 1 }$ , but $\mathbb { S } _ { 2 }$ employs an extra on-demand UAV $U _ { 2 } .$ . Suppose $\alpha = 1$ and $\beta = 4 ,$ , we have $T C ( \mathbb { S } _ { 1 } ) = 9 2$ and $T C ( \mathrm { S } _ { 2 } ) = 1 2 0$ . Apparently, S1 tasks much less cost than that of $\mathbb { S } _ { 2 }$ . However, the reserved UAVs may be overloaded with less on-demand UAVs and the completion time of all tasks may be greatly increased. Taking the solutions in Fig. 3 as an example, $C S ( \mathbb { S } _ { 1 } ) = 9 2$ and $C S ( \mathbb { S } _ { 2 } ) = 4 4$ . Although $\mathbb { S } _ { 2 }$ has more cost, its completion time is greatly reduced. We introduce Pareto optimization for the considered problem. The paper aims to obtain the Pareto front of the considered problem.

## IV. PROPOSED METHOD

In the paper, we employ the bi-criterion ant colony optimization (bi-ACO) algorithm for the bi-objective optimization problem under study. We first introduce the main framework of bi-ACO, followed by the details for every key operations and settings.

## A. Main Framework of bi-ACO

Algorithm 1 describes the major framework of the proposal. N ant colonies $\mathit { C O } _ { 1 } , \mathit { C O } _ { 2 } , \ldots , \mathit { C O } _ { \mathcal { N } }$ are initially constructed with initial pheromone matrices (Lines 1-2). A global Pareto set $P F ^ { * }$ is maintained to accommodate non-dominated solutions and it is initially empty (Line 3). Then an iterative process (Lines 4-13) is repeated until the termination condition is met, i.e., $I _ { \mathrm { m a x } }$ generations have been done. In each generation, three steps (Lines 7-12) are performed by every ant in each colony:

1) Each ant constructs a feasible solution based on pheromone matrices and heuristic values (Line 7).

2) $P F ^ { * }$ is updated accordingly (Line 8).

3) If the obtained solution is a non-dominated one, it is modified to generate a promising solution (Lines 9-12). The feasibility of the promising solution is checked and $P F ^ { * }$ is updated accordingly.

At the end of each generation, the pheromone matrices of all colonies are updated according to $P F ^ { * }$ (Line 13).

As can be seen, the proposed bi-ACO algorithm consists of several major settings and components: the settings of heterogeneous colonies to define the pheromone matrices and heuristic matrices, the Feasible Solution Generation Method (FSGM) to generate a feasible solution, the Solution Division Method (SDM) to generate a promising solution and the Pheromone

Algorithm 1: bi-ACO Framework.   
1 Initialize Nant colonies $C O _ { 1 } , C O _ { 2 } , \ldots , C O _ { \mathcal { N } } ;$   
2 Initialize pheromone matrices for N colonies;   
3 $P F ^ { * }  \dot { \otimes } ; / \star P F ^ { * } \ \mathrm { ~ i ~ s ~ }$ the Pareto Front   
4 while Termination condition is not met do   
5 for $p = 1 , 2 , \ldots , \mathcal { N }$ do   
6 for $q = 1 , 2 , \ldots , n _ { a }$ do   
7 Call Feasible Solution Generation Method to generate a   
feasible solution $\mathbb { S } _ { 1 }$ based on pheromone matrices   
and heuristic values ;   
8 Update $P F ^ { * }$ by $\mathbb { S } _ { 1 } ;$   
9 $\mathbf { i f } ^ { \mathbf { ^ { \prime } } } \mathbb { S } _ { 1 } \in P F ^ { \ast }$ then   
10 Perform Solution Division Method on $\mathbb { S } _ { 1 }$ to   
generate a promising solution S2;   
11 if S2 is feasible then   
12 Update $P F ^ { * }$ by $\mathbb { S } _ { 2 } ;$   
13 Call Pheromone Update Method to update pheromone   
matrices of all colonies according to $P F ^ { * } ;$   
14 return $P F ^ { * } ,$

Update Method (PUM) to update pheromone matrices. The details of these settings and components are given in the following sub-sections.

## B. Colony Settings

There are $\mathcal { N }$ ant colonies $C O _ { 1 } , C O _ { 2 } , \ldots , C O _ { \mathcal { N } } . C O _ { p }$ is the $p ^ { t h }$ colony in the ant colony system. p is the index of a colony. Each colony has $n _ { a }$ ants $a n _ { 1 } , a n _ { 2 } , . . . , a n _ { n _ { a } } . a n _ { q }$ is the $q ^ { t h }$ ant in a colony. q is defined as the index of an ant. In each generation, an ant $a n _ { q }$ of $C O _ { p }$ makes the task offloading decisions based on the pheromone and heuristic values. One task offloading decision includes two parts: a task to select and its insertion position in the sequence. Each colony maintains five pairs of pheromone matrices where one pair is used for computing the probability of selecting a task and the other four pairs are used to determine the insertion position of a task.

The probability of an unscheduled task to be selected is defined in (18) which is shown at the bottom of this page. In the equation, Ti is the previously selected task and $T _ { i ^ { \prime } }$ denotes a candidate task about to be selected. Suppose W is the set of tasks which have been assigned to the current UAV and $\overline { W }$ is the set of unscheduled tasks. $\eta _ { i , i ^ { \prime } }$ (19) is the heuristic information corresponding to the total cost objective and $\widehat { \eta } _ { i , i ^ { \prime } }$ (20) is the heuristic information corresponding to the completion time objective. In (20), $S T ( T _ { i ^ { \prime } } )$ is defined as the slot time of $T _ { i ^ { \prime } }$ It can be computed by (21). $\left( \tau _ { i , i ^ { \prime } } \right)$ is the selection pheromone matrix corresponding to the total cost objective and $\left( \widehat { \tau } _ { i , i ^ { \prime } } \right)$ is the selection pheromone matrix corresponding to the completion time objective. All items in the selection pheromone matrices are initialized to 1. In order to promote the ants to search with different preferences of objectives, every ant in the colony has different relative importance factors for the objectives. The relative importance factor $\lambda _ { p , q }$ for the ant $a n _ { q }$ in the colony $C O _ { p }$

is defined by (22).

$$
\eta _ { i , i ^ { \prime } } = \left( \frac { \operatorname* { m a x } \{ { \mathbb { D } } ( L ( T _ { i ^ { \prime } } ) , L ( T _ { i ^ { \prime \prime } } ) ) | T _ { i ^ { \prime \prime } } \in W \} } { \nu } \right) ^ { - 1 }\tag{19}
$$

$$
\widehat { \eta } _ { i , i ^ { \prime } } = \left( S T ( T _ { i ^ { \prime } } ) - \frac { \mathbb { D } ( L ( T _ { i } ) , L ( T _ { i ^ { \prime } } ) ) } { \nu } \right) ^ { - 1 }\tag{20}
$$

$$
S T ( T _ { i ^ { \prime } } ) = D ( T _ { i ^ { \prime } } ) - D T ( T _ { i ^ { \prime } } ) - P ( T _ { i ^ { \prime } } ) - R T ( T _ { i ^ { \prime } } )\tag{21}
$$

$$
\lambda _ { p , q } = \frac { 2 ( q - 1 ) } { \mathcal { N } ^ { 2 } - 1 } + \frac { p - 1 } { \mathcal { N } + 1 }\tag{22}
$$

In particular, the probability of the first task to select by an UAV is defined by (23) which is shown at the bottom of the next page, where $T _ { 0 }$ is a dummy task.

Every colony maintains four pairs of insertion pheromone matrices $( \chi _ { i , i ^ { \prime } } ^ { f } )$ and $( \widehat { \chi } _ { i , i ^ { \prime } } ^ { f } ) \ : ( f = \bar { 1 } , 2 , 3 , 4 )$ , where $( \bar { \chi } _ { i , i ^ { \prime } } ^ { f } )$ is the insertion pheromone matrix corresponding to the total cost objective and $( \widehat { \chi } _ { i , i ^ { \prime } } ^ { f } )$ is the insertion pheromone matrix correspond-ing to the completion time objective. Similar to the selection pheromone matrices, all items in these insertion pheromone matrices are initialized to 1 and updated generation by generation. The reason that we need 4 pairs of matrices for task insertion is that there are 4 possible scenarios for an insertion position in the task insertion method. Given an insertion position, the closest transmission sub-tasks on its left and right sides may be 1) both the first-stage subtasks, 2) both the third-stage subtasks, 3) the first-stage sub-task and third-stage sub-task, or 4) the third-stage sub-task and first-stage sub-task. The usage of these matrices will be introduced in the following sub-sections.

## C. Feasible Solution Generation Method

The $q ^ { t h }$ ant of $C O _ { p }$ constructs a feasible solution by FSGM (Algorithm 2). There are three major steps in FSGM: First, the ant generates the task and UAV assignments for all reserved UAVs (Lines 3-27). Second, if all reserved UAVs are used but there are still unscheduled tasks, the on-demand UAVs are employed to undertake the rest tasks (Lines 28-32). Third, the ant improves the obtained solution by swapping assignments of some UAVs (Lines 33-36). The following subsections will introduce the major steps of FSGM and the details of key components.

1) Major Steps of FSGM: In each iteration (Lines 4-27) of the first step, the ant constantly tries to assign tasks to the current UAV until the termination conditions are met. There are three termination conditions: (1) all tasks have been scheduled (Line 8), (2) the boundary parameter becomes invalid (Line 23) and (3) the ant stops assigning at a given probability (Line 25). The boundary parameter B is used to restrict the task insertion positions in the Task Insertion Method.

The ant uses $\overline { { W } } _ { j }$ to preserve all candidate tasks to try. $\overline { { W } } _ { j }$ contains all unscheduled tasks at the beginning of each trial (Line 9). Then the ant iteratively performs the following process

$$
P ( p , q , T _ { i } , T _ { i ^ { \prime } } ) = \frac { ( ( \tau _ { i , j ^ { \prime } } ) ^ { \lambda _ { p , q } } ( \widehat { \tau } _ { i , j ^ { \prime } } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \phi } \cdot ( ( \eta _ { i , i ^ { \prime } } ) ^ { \lambda _ { p , q } } ( \widehat { \eta } _ { i , i ^ { \prime } } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \varphi } } { \sum _ { T _ { i ^ { \prime \prime } } \in W } ( ( \tau _ { i , i ^ { \prime \prime } } ) ^ { \lambda _ { p , q } } ( \widehat { \tau } _ { i , i ^ { \prime \prime } } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \phi } \cdot ( ( \eta _ { i , i ^ { \prime \prime } } ) ^ { \lambda _ { p , q } } ( \widehat { \eta } _ { i , i ^ { \prime \prime } } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \varphi } }\tag{18}
$$

Algorithm 2: Feasible Solution Generation Method   
$F S G M ( p , q )$   
1 $\overline { { W } }  \mathbb { T } ; / \star \overline { { W } }$   
2AâÎ±;I $ \emptyset ; \mathbb { U } ^ { \prime }  \emptyset ;$   
3for $\forall U _ { j } \in \mathbb { U }$ do   
4 $A _ { j } ^ { - }  \infty ; / \star A _ { j }$ contains assignments of tasks   
selected by $U _ { j }$   
5 $\pi _ { j } \gets ( ) ; / { \star } \mathsf { S u b { - } t a s k }$   
empty   
6 $T \gets \bar { T _ { 0 } } ; \bar { / } \star \ T$   
$B  1 ; / \star B ~ \mathrm { ~ i ~ s ~ } ~ \mathrm { t ~ h ~ }$   
restricting the task insertion operation   
8 while $\overline { W }$ is not empty do   
9 $\overline { { W } } _ { j }  \overline { { W } } ; / \star \ : ^ { ' } \dot { \overline { { W } } } _ { j }$   
$\star /$   
10 for $R = 1$ to Rmax do   
11 Compute $P ( p , q , T , T ^ { \prime } ) \mathrm { f o r } \forall T ^ { \prime } \in \overline { { W } } _ { j } ;$   
12 $T _ { i } \gets R W S \textcircled { P ( p , q , T , T ^ { \prime } ) } | _ { T ^ { \prime } \in \overline { { W } } _ { i } } ) ; / \star$ RWS is   
13 $< \pi _ { j } ^ { \prime } , A _ { j } ^ { \prime } >  T I M ( A _ { j } , \pi _ { j } , T _ { i } , B , p , q ) ; / \star$   
Task Insertion Method   
14 if $< \pi _ { j } ^ { \prime } , A _ { j } ^ { \prime } > i s$ feasible then   
15 $\pi _ { j }  \pi _ { j } ^ { \prime } ;$   
16 ${ \dot { A _ { j } } } \gets { \check { A } } _ { i } ^ { \prime } ;$   
17 $\ { \overline { { W } } }  \ { \overline { { W } } }$   
18 $T \gets T _ { i } ;$   
19 break;   
20 else   
21 $\begin{array} { r } { \mathsf { L } \quad \overline { { W } } _ { j } \gets \overline { { W } } _ { j } - \{ T _ { i } \} ; } \end{array}$   
22 $B  B U M ( \pi _ { j } , B ) ; / \star$ BUM is Boundary Update   
Method   
23 if $B = - 1$ then   
24 break;   
break at the probability of $\frac { \theta _ { b } \times \left( p - 1 \right) } { \mathcal { N } - 1 } ;$   
26 $A  A + A _ { j } ;$   
27 $\Pi  \Pi + \{ \check { \pi } _ { j } \}$   
28 while W is not empty do   
29 $\mathbb { U } ^ { \prime } \gets \mathbb { U } ^ { \prime } + \{ \dot { U } \} ; / \star$ Employ an on-demand UAV $U \_ { \mathbf { \Sigma } { \star } { } } \ / $   
30 Generate task assignment set A' and UAV assignment $\pi ^ { \prime }$ in   
the similar manner as steps 8-25;   
31 $A  A + A ^ { \prime } ;$   
32 I $ \Pi + \{ \pi ^ { \prime } \}$ ï¼   
33for $\forall U _ { j } \in \mathbb { U }$ and $\forall U _ { j ^ { \prime } } \in \mathbb { U } ^ { \prime }$ do   
34 if $\overset { \prime } { L } { } ^ { 0 } ( U _ { j } ) = L ^ { 0 } \overset { \prime } { ( } U _ { j ^ { \prime } } )$ then   
35 if $\dot { C } ( \pi _ { j , K _ { j } } ) { \prec } \dot { C } ( \pi _ { j ^ { \prime } , K _ { j ^ { \prime } } } )$ then   
36 Swap the task and UAV assignments of $U _ { j }$ and $U _ { j ^ { \prime } } { \mathrm { ; } }$   
37 return $< A , \Pi >$

(Lines 10-21) at most $R _ { \mathrm { m a x } }$ times unless a feasible assignment is obtained.

1) The probability of every candidate task to be selected is computed (Line 11).

2) Roulette Wheel Selection is performed and one task is selected (Line 12).

3) Task Insertion Method tries to insert the selected task into the current sub-task sequence of $U _ { j }$ (Line 13).

4) If the selected task is successfully inserted into the sub-task sequence (Line 14), the current sub-task sequence and task assignment are updated accordingly (Lines 15-16). The task is removed from the set of unscheduled tasks (Line 17) and it is marked as the previous selected task (Line 18). The current trial is completed (Line 19).

5) If the task insertion fails, the selected task is removed from the candidate set (Line 21) and the next iteration will begin.

Whether the above process successfully assigns a task to $U _ { j }$ or not, the boundary parameter will be updated according to the current sub-task sequence (Line 22). The ant would take a new trial of assigning task with the updated B. However, if the updated B is invalid, i.e., $B = - 1$ , then the ant would stop assigning tasks to the current UAV. Besides, the ant stops assigning at a given probability which is computed based on the index of the colony (Line 25). Without the probability condition for termination, an UAV would be assigned as many tasks as possible. But with the condition, some reserved UAVs may be not fully arranged and leave more tasks to on-demand UAVs. In other words, the lower the probability of breaking the loop (Lines 8-25), the fuller the reserved UAVs and the lower the cost. The colonies with smaller indexes have more preference towards the objective of cost and the colonies with lager indexes prefer to the objective of completion time. Therefore, we compute the probability condition based on the index of the colony, i.e., p. The colonies with smaller indexes will gain smaller probability of breaking the loop, vice versa. Besides, we introduce a breaking factor $\theta _ { b }$ to manipulate the probability of breaking the loop. $\theta _ { b } = 0$ indicates no breaking. The higher $\theta _ { b }$ is, the higher probability the algorithm will break the loop. $\theta _ { b }$ will be calibrated in the experiment section.

The second step (Lines 28-32) takes place if the reserved UAVs are not sufficient to handle all tasks. On-demand UAVs are randomly selected and take over the rest of tasks. The assignments of on-demand UAVs are generated in the similar manner as those of the reserved ones.

In the third step, the ant improves the obtained solution by swapping assignments of some UAVs (Lines 33-36). For every pair of UAVs with the same initial location but different types, the completion times of them are compared. If an on-demand UAV works more time than that of a reserved one, swapping the assignments between them can lead to lower cost.

There are two key components in FSGM: (1) Task Insertion Method inserts task into appropriate position of sub-task sequence for a given UAV, and (2) Boundary Update Method shrinks insertion position boundary in order to improve efficiency. The details of the components are given as follows.

2) Task Insertion Method: Algorithm 3 details how to insert the selected task into the current sub-task sequence. Task Insertion Method (TIM) tries to insert three stages of a given

$$
P ( p , q , T _ { 0 } , T _ { i } ) = \frac { ( ( \tau _ { 0 , i } ) ^ { \lambda _ { p , q } } ( \widehat { \tau } _ { 0 , i } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \phi } \cdot S T ( T _ { i } ) ^ { - \varphi } } { \sum _ { T _ { i ^ { \prime } } \in \overline { { W } } } ( ( \tau _ { 0 , i ^ { \prime } } ) ^ { \lambda _ { p , q } } ( \widehat { \tau } _ { 0 , i ^ { \prime } } ) ^ { ( 1 - \lambda _ { p , q } ) } ) ^ { \phi } \cdot S T ( T _ { i ^ { \prime } } ) ^ { - \varphi } }\tag{23}
$$

<!-- image-->  
(e) Try all candidate insertion positions and select the best one  
Fig. 4. Example of TIM procedure.

task $T _ { i }$ into the current sub-task sequence $\pi _ { j }$ of $U _ { j }$ with the given insertion boundary B. TIM may fail to obtain a feasible solution, therefore, it operates on the copy of input $\pi _ { j }$ (Line 1). If $T _ { i }$ is the first task assigned to $U _ { j }$ (Line 2), the sub-tasks of $T _ { i }$ are inserted sequentially (Line 3). $T _ { s w a p }$ is arranged by Swapping Task Insertion Method (Line 4). The corresponding task assignments are computed (Line 5). The obtained solution is returned if it is feasible (Lines 6-7). If $T _ { i }$ is not the first task to insert, then the following steps are performed.

1) Two sub-tasks $T _ { i , 1 }$ and $T _ { i , 2 }$ are inserted into the sub-task sequence from position B (Lines 8-9). We assume a task starts the computation stage immediately when the data transmission stage is completed.

2) Delete all $T _ { s w a p }$ sub-tasks from position $B + 2$ to the end (Line 10). $T _ { i , 3 }$ may be inserted into any position. $T _ { s w a p }$ sub-tasks arranged previously may become inappropriate. Therefore, it is necessary to remove these $T _ { s w a p }$ sub-tasks and rearrange them afterwards. After the insertion and delete operations, $\pi _ { j } ^ { \prime }$ is assumed to have $K _ { j }$ sub-tasks in total, i.e., $\pi _ { j } ^ { \prime } = ( \pi _ { j , 1 } ^ { \prime } , \pi _ { j , 2 } ^ { \prime } , \ldots , \pi _ { j , K _ { j } } ^ { \prime } )$

3) The pheromone intensity of the every possible position b (from $B + 2$ to $K _ { j } )$ is evaluated by PheromoneIntensity function (Lines 11-16). Set B is used to deposit all candidate positions and their pheromone intensities (Line 11). $T _ { i , 3 }$ must be inserted after position B + 1. If the sub-task at position b is a $2 ^ { n d }$ stage sub-task, $T _ { i , 3 }$ cannot inserted before it, since we assume the first two stages of the same task must be executed continuously (Lines 13-14).

4) All candidate positions are sorted in descending order of pheromone intensities and only the top five with the highest intensities are kept (Lines 17-18).

5) $T _ { i , 3 }$ are inserted into the position which can lead to the feasible solution and the completion time is minimal (Lines 19-32).

6) If no feasible solution can be obtained, the algorithm returns NULL (Lines 33-34).

Fig. 4 shows an example of TIM procedure. The current sub-task sequence is given as Fig. 4(a) and $T _ { 4 }$ is about to insert into it. Sub-tasks $T _ { 4 , 1 }$ and $T _ { 4 , 2 }$ are inserted at position B and $B + 1$ as shown in Fig. 4(b). Then all swapping tasks are removed $( \mathrm { F i g . 4 ( c ) ) }$ . There are 6 candidate insertion positions $( b = 5 , 7 , 8 , 1 0 , 1 1 , 1 2 )$ for inserting $T _ { 4 , 3 }$ and their pheromone intensities are computed. Five candidate insertion positions $( b =$ 5, 8, 10, 11, 12) with highest pheromone intensities are reserved (Fig. 4(d)). $T _ { 4 , 3 }$ is tried to insert into every candidate position and every attempt is evaluated (Fig. 4(e)). Finally, b = 12 is the best insertion position for $T _ { 4 , 3 }$

Algorithm 3: Task Insertion Method $\mathrm { T I M } ( A _ { j } , \pi _ { j } , T _ { i } ,$   
$B , p , q )$   
1 $\pi _ { j } ^ { \prime }  \pi _ { j } ; / \star \quad \pi _ { j } ^ { \prime }$ is a copy of $\pi _ { j }$   
2 $\mathbf { i } \mathbf { \dot { f } } \mathbf { \nabla } A _ { j } = \mathbf { \nabla } \boldsymbol { \mathcal { O } }$ then   
3 ${ \boldsymbol \pi } _ { j } ^ { \prime } \gets ( T _ { i , 1 } , T _ { i , 2 } , T _ { i , 3 } ) ;$   
4 Check the feasibility of $\pi _ { j } ^ { \prime }$ on the energy constraint and   
insert $T _ { s w a p }$ at appropriate positions by Swapping Task   
Insertion Method;   
5 Compute the task assignments $A _ { j } ^ { \prime }$ for $\pi _ { j } ^ { \prime } ;$   
6 if $A _ { j } ^ { \prime }$ and $\pi _ { j } ^ { \prime }$ are feasible then   
7 return $< \pi _ { j } ^ { \prime } , A _ { j } ^ { \prime } > ;$   
8Insert $T _ { i , 1 }$ at the position B of $\pi _ { j } ^ { \prime } ;$   
9Insert $T _ { i , 2 }$ at the position $B + 1 \ \mathrm { { o f } } \ \pi _ { j } ^ { \prime } ;$   
10 Delete all $T _ { s w a p }$ in $\pi _ { j } ^ { \prime }$ starting from the position $B + 2$ to the   
end;   
$\pi _ { j } ^ { \prime } = ( \pi _ { j , 1 } ^ { \prime } , \pi _ { j , 2 } ^ { \prime } , \ldots , \pi _ { j , K _ { j } } ^ { \prime } )$   
11 $B  \emptyset ; / \star B$ deposits candidate insertion   
positions and their pheromone intensities $\star /$   
12 for $\stackrel { \cdot } { b } = B + 2$ to $K _ { j } + 1$ do   
13 $\mathbf { i f } \ \pi _ { j , b } ^ { \prime } \ i s \ a \ 2 ^ { n d }$ stage sub-task then   
14 Continue ;   
15 $P i _ { b } \gets P I M ( \pi _ { i } ^ { \prime } , b , T _ { i } , p , q ) ; / * \mathbb { P I M } \mathrm { ~ \ i ~ s ~ }$ Pheromone   
Intensity Method   
16 $\{ \beta  B + \{ < b , \bar { P } i _ { b } > \} ;$   
17 Sort allitems in B in descending order of pheromone intensities;   
18 Remove all items from B except the top five items with the   
highest intensities;   
19 $A _ { i } ^ { * } \gets \emptyset ;$   
20 $\pi _ { j } ^ { * }  ( ) ;$   
21 $\check { C } T ^ { * } \gets + \infty ;$   
22 for $< b , P i _ { b } > \in B \ ,$ do   
23 $\pi _ { j } ^ { \prime \prime } ~  ~ \bar { \pi } _ { j } ^ { \prime } ; / \star ~ \pi _ { j } ^ { \prime \prime } ~ \mathrm { ~ i ~ s ~ a ~ }$ $\pi _ { j } ^ { \prime }$   
24 Insert $\check { T _ { i , 3 } }$ at the position b of $\pi _ { j } ^ { \prime \prime } ;$   
25 Check the feasibility of $\pi _ { j } ^ { \prime \prime }$ on the energy constraint and   
insert $T _ { s w a p }$ at appropriate positions by Swapping Task   
Insertion Method;   
26 Compute the task assignments $A _ { j } ^ { \prime \prime }$ for $\pi _ { j } ^ { \prime \prime } ;$   
27 if $A _ { i } ^ { \prime \prime }$ and $\pi _ { j } ^ { \prime \prime }$ are feasible then   
28 Compute the completion time CT of $A _ { j } ^ { \prime \prime } ;$   
29 if $\bar { C T } < \bar { C T } ^ { * }$ then   
30 $A _ { j } ^ { * }  A _ { j } ^ { \prime \prime } ;$   
31 $\pi _ { j } ^ { * }  \pi _ { j } ^ { \prime \prime } ;$   
32 ${ \check { C } } { \check { T } } ^ { * } \gets { \check { C } } T ;$   
33if $C T ^ { * } = + \infty$ then   
34 return NULL;   
35return $< \pi _ { j } ^ { * } , A _ { j } ^ { * } > ;$

There are two major components in Algorithm 3: (1) Swapping Task Insertion Method (STIM) to insert $T _ { s w a p }$ tasks to sub-task sequence and (2) Pheromone Intensity Method (PIM) to compute the pheromone intensity for a given insertion position. They are described as follows.

The key idea of STIM is to check if the residual energy of $U _ { j }$ at the end of a sub-task is sufficient enough to execute a closest $T _ { s w a p }$ task. In the case of insufficient energy, a $T _ { s w a p }$ task should be inserted before the sub-task. The $T _ { s w a p }$ task to insert should be delicately selected. Since it will be inserted between two sub-tasks $\pi _ { j , k - 1 }$ and $\pi _ { j , k }$ , the residual energy of $U _ { j }$ at the end of $\pi _ { j , k - 1 }$ should be sufficient to fly to the location of $T _ { s w a p }$

In PIM, four steps are performed to compute the pheromone intensity for a given insertion position (Algorithm 4):

1) The recent transmission sub-task $\pi _ { j , b _ { 1 } }$ before b is found first (Lines 6-14). $\pi _ { j , b _ { 1 } }$ could either be a data transmission sub-task or a result transmission sub-task. $h _ { 1 }$ and $i _ { 1 }$ are employed to denote the stage index and task index of $\pi _ { j , b _ { 1 } }$

2) Then the recent transmission sub-task $\pi _ { j , b _ { 2 } }$ after b is found (Lines 15-23). $h _ { 2 }$ and $i _ { 2 }$ are employed to denote the stage index and task index of $\pi _ { j , b _ { 2 } }$

3) It is possible that there is no transmission sub-task after $b ,$ then $i _ { 2 }$ is $n + 1$ indicating a dummy task index. In this case, $P i$ is set to $+ \infty$ (Lines 24-25);

4) Otherwise, P i is computed based on different insertion pheromone matrices according to the values of $h _ { 1 }$ and $h _ { 2 }$ (Lines 26-33).

There are four pairs of pheromone matrices employed in Algorithm 4 to compute pheromone intensity (Lines 26- 33). $\bar { ( \chi _ { i , i ^ { \prime } } ^ { 1 } ) } , ( \chi _ { i , i ^ { \prime } } ^ { 2 } ) , ( \chi _ { i , i ^ { \prime } } ^ { 3 } ) , ( \chi _ { i , i ^ { \prime } } ^ { \bar { 4 } } )$ are the insertion pheromone matrices corresponding to the total cost objective and $( \widehat { \chi } _ { i , i ^ { \prime } } ^ { 1 } ) , ( \widehat { \chi } _ { i , i ^ { \prime } } ^ { 2 } ) , ( \bar { \widehat { \chi } _ { i , i ^ { \prime } } ^ { 3 } } ) , ( \bar { \widehat { \chi } _ { i , i ^ { \prime } } ^ { 4 } } )$ are the insertion pheromone matrices corresponding to the completion time. Items $\chi _ { i , i ^ { \prime } } ^ { 1 }$ and $\widehat { \chi } _ { i , i ^ { \prime } } ^ { 1 }$ indicate the preference that $T _ { i ^ { \prime } , 3 }$ inserts after $T _ { i , 1 }$ . Items $\chi _ { i ^ { \prime } , i } ^ { 2 }$ and $\widehat { \chi } _ { i ^ { \prime } , i } ^ { 2 }$ indicate the preference that $T _ { i ^ { \prime } , 3 }$ inserts before $T _ { i , 1 }$ Items $\chi _ { i , i ^ { \prime } } ^ { 3 }$ and $\widehat { \chi } _ { i , i } ^ { 3 }$ - indicate the preference that $T _ { i ^ { \prime } , 3 }$ inserts after $T _ { i , 3 }$ . Items $\chi _ { i ^ { \prime } , i } ^ { 4 }$ and $\widehat { \chi } _ { i ^ { \prime } , i } ^ { 4 }$ indicate the preference that $T _ { i ^ { \prime } , 3 }$ inserts before $T _ { i , 3 }$

3) Boundary Update Method: Algorithm 5 reveals how to update B. The more tasks have been assigned to the UAV in the previous iterations, the more possible insertion positions there would be. It would be low in efficiency to try all possible positions to insert a task. B is slowly increased with the number of tasks assigned to the current UAV. B is updated to the position of the recent transmission sub-task (Lines 1-3). If there is no transmission sub-task after position B, then an invalid position is returned (Lines 4-5).

As in Fig. 4, the final sub-sequence is the one where $T _ { 4 , 3 }$ is inserted at position b = 12. Afterwards, B is updated to 5 by BUM.

## D. Solution Division Method

Solution division method (SDM) is designed to reconstruct a given solution to a new one (as shown in Algorithm 6). The following major steps are performed by SDM:

1) The input schedule is copied (Line 1). The following operations are performed on the copy of the input schedule.

2) The UAV $U _ { j }$ with the maximum completion time is found (Line 2).

3) Tasks in $U _ { j }$ are picked up and put into set $\mathbb { T } ^ { \prime }$ at a 50% probability (Lines 3-7). If all tasks are selected or no task is selected, then the algorithm returns NULL.

Algorithm 4: Pheromone Intensity Method $\operatorname { P I M } ( \pi _ { j } , b , T _ { i }$   
$p , q ) .$   
/\* Suppose $\pi _ { j } = ( \pi _ { j , 1 } , \pi _ { j , 2 , \cdot \cdot \cdot } , \pi _ { j , K _ { j } } )$ $\star /$   
$P i  0 ;$   
2 $h _ { 1 } \gets - 1 ;$   
$h _ { 2 }  - 1 ;$   
4 $i _ { 1 } \gets 0 ;$   
5 $i _ { 2 } \gets n + 1 ;$   
6 forbl=b-1 to1do   
if $\pi _ { j , b _ { 1 } }$ isa $1 ^ { s t }$ stage sub-task then   
8 ${ \tilde { h _ { 1 } } } \gets 1 ;$   
9 Set $i _ { 1 }$ to be the task index of $\pi _ { j , b _ { 1 } } ;$   
10 break;   
11 if $\pi _ { j , b _ { 1 } }$ $\iota 3 ^ { r d }$ stage sub-task then   
12 ${ \bar { h _ { 1 } } }  3 ;$   
13 Set i1 to be the task index of $\pi _ { j , b _ { 1 } } ;$   
14 break;   
15for $b _ { 2 } = b$ 0 $K _ { j }$ do   
16 if $\pi _ { j , b _ { 2 } }$ isa $\mathrm { i } ^ { s t }$ stage sub-task then   
17 ${ h _ { 2 } }  1 ;$   
18 Seti2 to be the task index of $\pi _ { j , b _ { 2 } } ;$   
19 break;   
20 if $\pi _ { j , b _ { 2 } }$ isa $3 ^ { r d }$ stage sub-task then   
21 ${ h _ { 2 } }  3 ;$   
22 Set i2 to be the task index of $\pi _ { j , b _ { 2 } } ;$   
23 break;   
24if $i _ { 2 } = n + 1$ then   
25 Piâ+â;   
26 else if $h _ { 1 } = 1$ and $h _ { 2 } = 1$ then   
27 Piâ   
$( \chi _ { i _ { 1 } , i } ^ { 1 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i _ { 1 } , i } ^ { 1 } ) ^ { ( 1 - \lambda _ { p , q } ) } + ( \chi _ { i , i _ { 2 } } ^ { 2 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i , i _ { 2 } } ^ { 2 } ) ^ { ( 1 - \lambda _ { p , q } ) }$   
28 else if $h _ { 1 } = 1$ and $h _ { 2 } = 3$ then   
29 Piâ   
$( \chi _ { i _ { 1 } , i } ^ { 1 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i _ { 1 } , i } ^ { 1 } ) ^ { ( 1 - \lambda _ { p , q } ) } + ( \chi _ { i , i _ { 2 } } ^ { 4 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i , i _ { 2 } } ^ { 4 } ) ^ { ( 1 - \lambda _ { p , q } ) }$   
30 else if $h _ { 1 } = 3$ and $h _ { 2 } = 1$ then   
31 Piâ   
$( \chi _ { i _ { 1 } , i } ^ { 3 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i _ { 1 } , i } ^ { 3 } ) ^ { ( 1 - \lambda _ { p , q } ) } + ( \chi _ { i , i _ { 2 } } ^ { 2 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i , i _ { 2 } } ^ { 2 } ) ^ { ( 1 - \lambda _ { p , q } ) }$   
32 else if $h _ { 1 } = 3$ and $h _ { 2 } = 3$ then   
33 Piâ   
$( \check { \chi } _ { i _ { 1 } , i } ^ { 3 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i _ { 1 } , i } ^ { 3 } ) ^ { ( 1 - \lambda _ { p , q } ) } + ( \chi _ { i , i _ { 2 } } ^ { 4 } ) ^ { \lambda _ { p , q } } \cdot ( \widehat { \chi } _ { i , i _ { 2 } } ^ { 4 } ) ^ { ( 1 - \lambda _ { p , q } ) }$   
34 return $P i ;$

```perl
Algorithm 5: Boundary Update Method BUM(Ï, B).
/* Suppose $\boldsymbol { \pi } _ { j } = ( \pi _ { j , 1 } , \pi _ { j , 2 } , \ldots , \pi _ { j , K _ { j } } )$ $\star /$
1 $B ^ { \prime } \gets B + 1 ;$
2while $\pi _ { j , B ^ { \prime } }$ is Tswap or a $2 ^ { n d }$ stage sub-task do
3 $\\\\\\\\\{ \begin{array} { r l } { \big \langle } & { { } B ^ { \prime } \bigleftarrows B ^ { \prime } + 1 ; } \end{array} $
4 $\mathbf { i f } \ B ^ { \prime } > K _ { j } + 1$ then
5 return -1;
6return $B ^ { \prime } ;$
```

4) All $T _ { s w a p }$ tasks are removed from $\pi _ { j }$ since the successive operations may course invalidity of these tasks (Line 8).

5) An idle reversed UAV is randomly selected. If there is no idle reserved UAV, an on-demand UAV is introduced (Lines 9-11).

6) The sub-tasks of selected tasks are added to $\pi _ { j ^ { \prime } }$ in the same order as they are sequenced in $\pi _ { j }$ (Lines 12-15).

7) The sub-tasks of selected tasks are removed from $\pi _ { j }$ (Lines 16-17).

Algorithm 6: Solution Division Method SDM $( \mathbb { S } ^ { \ast } ) .$   
1 $\mathbb { S }  \mathbb { S } ^ { * } ; / \star$ Following operations are performed on   
$\star /$   
2 $U _ { j }  a r g$ max $\{ C ( \pi _ { j , \bar { K _ { j } } } ) | U _ { j } \in \mathbb { U } \cup \mathbb { U } ^ { \prime } \} ;$   
3 $\mathbb { T } ^ { \prime }  \emptyset ;$   
4for $\forall a _ { i } \in A _ { j }$ do   
5 Put Ti into T' at a 50% probability;   
6if $A _ { j } | = | \mathbb { T } ^ { \prime } | ~ o r ~ | \mathbb { T } ^ { \prime } | = 0$ then   
7return NULL;   
8 Remove all $T _ { s w a p }$ inÏjï¼   
9 Select an idle UAV $U _ { j ^ { \prime } }$ where reserved one is preferred;   
10if $U _ { j ^ { \prime } }$ is an on-demand UAV then   
11 $\big \lfloor \mathrm { ~ \textmu ~ } ^ { \prime } \big \rceil  \mathbb { U } ^ { \prime } + \{ U _ { j ^ { \prime } } \}$   
12 $\pi _ { j ^ { \prime } }  ( ) ; / \star \pi _ { j ^ { \prime } }$ $U _ { j ^ { \prime } } \mathrm { \Sigma } \ \star / \mathrm { \Sigma }$   
$\pi _ { j }$ $\pi _ { j } = ( \pi _ { j , 1 , \cdot \cdot \cdot } , \pi _ { j , K _ { j } } )$   
13 for $k = 1$ to $K _ { j }$ do   
14 if $\pi _ { j , k } ~ i$ sthesub-taskofatask in $\mathbb { T } ^ { \prime }$ then   
15 Add $\pi _ { j , k }$ to the end of $\pi _ { j ^ { \prime } } , :$   
16for $\forall T _ { i } \in \mathbb { T } ^ { \prime }$ do   
Remove sub-tasks of $T _ { i }$ from $\pi _ { j } ;$   
18 Add $T _ { s w a p }$ tasks to $\pi _ { j }$ and $\pi _ { j } ^ { \prime }$ at appropriate positions by   
Swapping Task Insertion Method;   
19 Compute new assignments of tasks in $\pi _ { j }$ and $\pi _ { j } ^ { \prime } ;$   
20 for $\forall { \bar { U } } _ { j _ { 1 } } \in \mathbb { I }$ Uand $\forall U _ { j _ { 2 } } \in \mathbb { U } ^ { \prime }$ do   
21 if $\Breve { L } ^ { 0 } ( U _ { j _ { 1 } } ) = L ^ { 0 } ( \Breve { U } _ { j _ { 2 } } )$ then   
22 $\mathbf { i f } \ { \tilde { C } } ( \pi _ { j _ { 1 } , K _ { j _ { 1 } } } ) { \overset {  } { < } } C ( \pi _ { j _ { 2 } , K _ { j _ { 2 } } } )$ then   
23 Swap the task and $\mathrm { U A } \mathbf { \tilde { V } }$ assignments of $U _ { j _ { 1 } }$ and   
$U _ { j _ { 2 } } ;$   
24 Update S accordingly;   
25return $\mathbb { S } ;$

8) $T _ { s w a p }$ tasks are inserted into $\pi _ { j }$ and $\pi _ { j ^ { \prime } }$ at appropriate positions (Line 18).

9) Based on the new sub-task sequences, new assignments are computed (Line 19).

10) Finally, the obtained solution is enhanced by swapping assignments of some UAVs (Lines 20-23).

## E. Pheromone Update Method

Pheromone Update Method (PUM) updates pheromone matrices based on the solutions in the Pareto Front. There are three major steps in PUM:

1) Solutions in the given Pareto Front are sorted in ascending order of their objectives of total cost and divided equally into $\mathcal { N }$ groups: $P F _ { 1 } , P F _ { 2 } , \dots , P F _ { \mathcal { N } }$ . Apparently, the first group $P F _ { 1 }$ consists of solutions with lowest total costs and largest completion times. Conversely, the last group $P F _ { \mathcal { N } }$ includes the solutions of highest total costs and smallest completion times.

2) Pheromone evaporation operation is performed on every pheromone value of all matrices by multiplying it with the evaporation factor $\rho \left( 0 < \rho < 1 \right)$

3) Pheromone Enhancement Method (Algorithm 7) is performed on every colony to increase the pheromone values associated with the given solution group.

Algorithm 7 describes the details of Pheromone Enhancement Method. The pheromone matrices of colony $C O _ { p }$ are enhanced with the solution group $P F _ { p }$ . For each solution, the preference parameter $\mu$ is computed (Line 2). Î¼ is related to the preference of the colony and it depends on the size of $P F ^ { * }$ , the colony index and the solution ranking value. Then for each sub-task sequence, the selection pheromone matrices are enhanced (Lines 4-9), followed with the procedure for increasing the pheromone values in insertion pheromone matrices ((Lines 10-47)).

In the procedure of enhancing selection pheromone matrices (Lines 4-9), the task sequence is abstracted from the sub-task sequence (Line 4), which indicates the order that tasks are selected. For every two successive tasks in the task sequence, the corresponding pheromone values from $\left( \tau _ { i , i ^ { \prime } } \right)$ and $\left( \widehat { \tau } _ { i , i ^ { \prime } } \right)$ are enhanced (Lines 5-9). $\Delta \tau$ is defined as an enhancement factor. Both $\Delta \tau$ and $\mu$ are used to compute the increment of a pheromone value.

The procedure of enhancing insertion pheromone matrices (Lines 4-9) corresponds to the procedure of employing these matrices in Algorithm 4. Since insertion pheromone matrices are used for inserting $3 ^ { r d }$ sub-stage tasks, all $3 ^ { r d }$ stage sub-tasks are checked in the procedure. For each $3 ^ { r d }$ stage sub-task, the recent transmission sub-tasks before and after it are obtained (Lines 16-33). Finally, the pheromone values are updated accordingly (Lines 34-47). Noted that a $3 ^ { r d }$ stage sub-task may be the last sub-task except swapping tasks. In this case, only one pair of pheromone matrices would be enhanced (Lines 40-41).

## F. Time Complexity of bi-ACO

The best time complexity of bi-ACO is $\Omega ( n ^ { 3 } )$ and the worst one is $o ( n ^ { 4 } )$ . The detailed time complexity analysis for Algorithm 1â7 is given in Appendix A, available online. $\mathsf { A p - }$ parently, the time complexity of bi-ACO mainly depends on the number of tasks. It is affordable in practise when n is not too big. We evaluate the actual computation time of bi-ACO on the problems of different size (as shown in Table VI) in the next section.

## V. COMPUTATIONAL EXPERIMENTS

In the section, the multiple components of bi-ACO framework are calibrated first. Then the calibrated bi-ACO algorithm with the best combination of the components is compared with several baseline algorithms for the similar problems. All compared algorithms are encoded in Java, compiled by Eclipse ide 2022-09 JDK1.8.0 and run on a Alibaba Cloud sever with Intel Xeon (Ice Lake) Platinum 8369B (2.5 GHz) processor and 32 GB of RAM.

## A. Performance Metrics

Since the proposed bi-ACO and compared baseline algorithms are all Pareto-based algorithms, and each of which obtains a set of non-dominated solutions, it is difficult to employ single metric to evaluate the overall performance of algorithms. We employ four Pareto-based metrics as follows to measure the obtained non-dominated solutions and evaluate the compared algorithms on aspects of the solution quality, the solution coverage, etc.

Average Quality (AQ) was proposed in [35] to measures the quality of the solution set. A less AQ value indicates the higher average solution quality for a given set of non-dominated solutions. The metric is defined as (24)â(26). fj is the normalized $j ^ { t h }$ objective of the solution S and n is the number of the objectives $( n = 2$ in the paper). Min-Max normalization is employed to normalize the objectives.

Algorithm 7: Pheromone Enhancement Method PEM   
$( C O _ { p } ) .$   
1 for VS =<A,II>â $P F _ { p }$ do   
$r ^ { t h }$   
${ P \check { F } } _ { p } ^ { \check { \mathbf { \alpha } } }$   
2 $\begin{array} { r } { \mu  \frac { p - 1 } { \mathcal { N } } + \frac { r } { | P F ^ { * } | } ; } \end{array}$   
3 for $\forall \pi _ { j } \in \Pi$ do   
$/ \dot { \star }$   
$U _ { j }$   
4 Obtain task sequence $T _ { i _ { 1 } } , T _ { i _ { 2 } } , \ldots , T _ { i _ { N } }$ from Ïj   
satisfying $S ( T _ { i _ { 1 } , 1 } ^ { ' } ) < S ( T _ { i _ { 2 } , 1 } ) < \ldots < S ( T _ { i _ { N } , 1 } ) ;$   
5 $i \gets \bar { 0 } ;$   
$/ \star$   
6 for $\hat { i ^ { \prime } } = i _ { 1 } , \dots , i _ { N }$ do   
7 $\tau _ { i , i ^ { \prime } } \gets \tau _ { i , i ^ { \prime } } + \Delta \tau \times \mu ;$   
8 $\widehat { \tau } _ { i , i ^ { \prime } } ^ { \mathrm { ~ ~ } \dagger } \gets \widehat { \tau } _ { i , i ^ { \prime } } ^ { \mathrm { ~ ~ } \dagger } + \Delta \tau \times ( 1 - \mu ) ;$   
9 $i \gets i ^ { \prime } ;$   
$/ \star$ $\boldsymbol { \pi } _ { j } = ( \pi _ { j , 1 } , \pi _ { j , 2 } , \ldots , \pi _ { j , K _ { j } } )$   
10 for $k = 1 , \ldots , \check { K _ { j } }$ do   
11 if $\pi _ { j , k }$ isnota $3 ^ { r d }$ stage sub-task then   
12 continue;   
Set ito be the task index of $\pi _ { j , k } ;$   
14 $i _ { 1 } \gets 0 ; i _ { 2 } \gets n + 1 ;$   
$h _ { 1 }  - 1 ; h _ { 2 }  - 1 ;$   
16 for $k _ { 1 } = k - 1$ to 1do   
17 if $\pi _ { j , k _ { 1 } } ~ i s ~ a ~ 1 ^ { s t }$ stage sub-task then   
18 ${ \bar { h _ { 1 } } } \gets 1 ;$   
19 Set i to be the task index of $\pi _ { j , k _ { 1 } } ;$   
20 break;   
21 if $\pi _ { j , k _ { 1 } } ~ i s ~ a ~ 3 ^ { s t }$ stage sub-task then   
22 ${ h _ { 1 } } ^ { * } \gets 3 ;$   
23 Set $i _ { 1 }$ to be the task index of $\pi _ { j , k _ { 1 } } ;$   
24 break;   
25 for $k _ { 2 } = k + 1$ to $K _ { j }$ do   
26 if $\pi _ { j , k _ { 2 } }$ is a $1 ^ { s t }$ stage sub-task then   
27 ${ h _ { 2 } }  1 ;$   
28 Set i2 to be the task index of $\pi _ { j , k _ { 2 } } ;$   
29 break;   
30 if $\pi _ { j , k _ { 2 } } \ i s \ a \ 3 ^ { s t }$ stage sub-task then   
31 ${ \bar { h } } _ { 2 } \gets 3 ;$   
32 Set i2 to be the task index of $\pi _ { j , k _ { 2 } } ;$   
break;   
34 $\mathbf { i f } \ h _ { 1 } = 1$ then   
35 $\begin{array} { r } { \check { \chi } _ { i _ { 1 } , i } ^ { 1 } \gets \chi _ { i _ { 1 } , i } ^ { 1 } + \Delta \tau \times \mu ; } \end{array}$   
36 $\widehat { \chi } _ { i _ { 1 } , i } ^ { 1 ^ { \star } } \gets \widehat { \chi } _ { i _ { 1 } , i } ^ { 1 ^ { \star } } + \Delta \tau \times ( 1 - \mu ) ;$   
elseif $\mathrm { : ~ } h _ { 1 } = 3$ then   
38 ${ \chi _ { i _ { 1 } , i } ^ { 3 } } \gets { \chi _ { i _ { 1 } , i } ^ { 3 } } + \Delta \tau \times \mu ;$   
39 $\widehat { \chi } _ { i _ { 1 } , i } ^ { 3 ^ { \star } } \gets \widehat { \chi } _ { i _ { 1 } , i } ^ { 3 ^ { \star } } + \Delta \tau \times ( 1 - \mu ) ;$   
40 if $i _ { 2 } = n + 1$ then   
41 2continue;   
42 if $h _ { 2 } = 1$ then   
43 ${ \chi _ { i , i _ { 2 } } ^ { 2 } } \gets { \chi _ { i , i _ { 2 } } ^ { 2 } } + \Delta \tau \times \mu ;$   
44 $\begin{array} { r } { \widehat { \chi } _ { i , i _ { 2 } } ^ { 2 ^ { \prime } ^ { - } }  \widehat { \chi } _ { i , i _ { 2 } } ^ { 2 ^ { \prime } ^ { - } } + \Delta \tau \times ( 1 - \mu ) ; } \end{array}$   
45 else if $h _ { 2 } = 3$ then   
46 ${ \chi _ { i , i _ { 2 } } ^ { 4 } } \gets { \chi _ { i , i _ { 2 } } ^ { 4 } } + \Delta \tau \times \mu ;$   
47 $\begin{array} { r } { \widehat { \chi } _ { i , i _ { 2 } } ^ { 4 ^ { \prime } }  \widehat { \chi } _ { i , i _ { 2 } } ^ { 4 ^ { \prime } } + \Delta \tau \times ( 1 - \mu ) ; } \end{array}$

<!-- image-->

<!-- image-->  
Fig. 5. Maps.

Maximum Spread (MS) was defined in [36] to measure how well $P F ^ { * }$ is covered by the given non-dominated solution set $P F . \ P F ^ { * }$ is the near-optimal Pareto front based on the union of the non-dominated solutions obtained by all compared algorithms. The larger the metric is, the more the near-optimal Pareto front $P F ^ { * }$ is covered by the given P F . The metric is formulated as (27).

Maximum Distance $( D _ { \mathrm { m a x } } )$ and average Distance $( D _ { a v g } )$ were defined in [37] to measure how close $P F$ is to $P F ^ { * }$ Smaller $D _ { a v g }$ and $D _ { \mathrm { m a x } }$ values correspond to a better approximation to $P F ^ { * }$ . The metrics are defined as (28) and (29), respectively. $\Delta ( \mathbb { S } , \mathbb { S } ^ { * } )$ is the relative distance between two solutions (30).

$$
A Q ( P F ) = \sum _ { \lambda \in \Lambda } \frac { s _ { a } ( P F , \lambda ) } { | \Lambda | }\tag{24}
$$

$$
s _ { a } ( P F , \lambda ) = \operatorname* { m i n } _ { \mathbb { S } \in P F } \left\{ \operatorname* { m a x } _ { j } ^ { n } \{ \lambda _ { j } \mathbf { f } _ { j } ( \mathbb { S } ) \} + \sum _ { j } ^ { n } \frac { \lambda _ { j } \mathbf { f } _ { j } ( \mathbb { S } ) } { 1 0 0 } \right\}\tag{25}
$$

$$
\boldsymbol { \Lambda } = \{ ( \lambda _ { 1 } , \ldots , \lambda _ { n } ) |
$$

$$
\lambda _ { j } \in \left\{ 0 , \frac { 1 } { 5 0 } , \frac { 2 } { 5 0 } , \ldots , \frac { 4 9 } { 5 0 } , 1 \} , \sum _ { j = 1 } ^ { n } \lambda _ { j } = 1 \right\}\tag{26}
$$

$$
M S ( P F ) = { \sqrt { \frac { 1 } { n } \sum _ { j = 1 } ^ { n } \left( { \frac { \operatorname* { m a x } \mathbf { \mathbf { f } } _ { j } ( \mathbb { S } ) - \operatorname* { m i n } _ { \mathbb { S } \in P F } \mathbf { f } _ { j } ( \mathbb { S } ) } { \operatorname* { m a x } _ { \mathbb { S } \in P F ^ { * } } \mathbf { f } _ { j } ( \mathbb { S } ) - \operatorname* { m i n } _ { \mathbb { S } \in P F ^ { * } } \mathbf { f } _ { j } ( \mathbb { S } ) } } \right) } }\tag{27}
$$

$$
D _ { \operatorname* { m a x } } = \operatorname* { m a x } _ { \mathbb { S } ^ { * } \in P F ^ { * } } \{ \operatorname* { m i n } _ { \mathbb { S } \in P F } \Delta ( \mathbb { S } , \mathbb { S } ^ { * } ) \}\tag{28}
$$

$$
D _ { a v g } = \sum _ { \mathbb { S } ^ { * } \in P F ^ { * } } \frac { \operatorname* { m i n } _ { \mathbb { S } \in P F } \Delta ( \mathbb { S } , \mathbb { S } ^ { * } ) } { | P F ^ { * } | }\tag{29}
$$

$$
\Delta ( \mathbb { S } , \mathbb { S } ^ { * } ) = \operatorname* { m a x } _ { j = 1 } ^ { n } \left\{ \frac { \mathbf { f } _ { j } ( \mathbb { S } ) - \mathbf { f } _ { j } ( \mathbb { S } ^ { * } ) } { \operatorname* { m a x } _ { \mathbb { S } \in P F ^ { * } } \mathbf { f } _ { j } ( \mathbb { S } ) - \operatorname* { m i n } _ { \mathbb { S } \in \in P F ^ { * } } \mathbf { f } _ { j } ( \mathbb { S } ) } \right\}\tag{30}
$$

## B. Testing Instances

The performance of compared algorithms are tested on the testing instances from the literatures [33], [34], [38]. We employ 4 maps att48, new60, ch150, and att532 to simulate the SD distribution, where att48, ch150 and att532 are benchmark maps from TSPLIB [38]. Map new60 is a randomly generated map, where a given number of base stations are distributed randomly first and then the SDs are distributed randomly around each base station. The nodes in these maps are taken as the tasks in the considered problems. The tasks in these maps are depicted as blues nodes in Fig. 5. The numbers of tasks in map att48, new60, ch150 and att532 are 48, 60, 150 and 532, respectively. The size of these maps are $6 0 0 0 \mathrm { m } \times 8 0 0 0 \mathrm { m } .$ 6000 m Ã 8000 m, 6000 m Ã 8000 m and 7000 m Ã 8000 m, respectively. The number of base stations |B| is set to 	 n 
. The base stations are distributed as orange nodes in Fig. 5.

<!-- image-->

<!-- image-->

For the UAV settings, the number of reserved UAVs m is set to  n20  or  n25 . Reserved UAVs are randomly distributed on base stations. The flying speed of UAVs Î½ is set to 20, 30, 40 or $5 0 m / s$ . The computation time $P ( T _ { i } )$ (in second) follows the uniform distribution U (10, 100). The data transmission time $D T ( T _ { i } )$ (in second) is set to be linearly related to $P ( T _ { i } )$ , i.e., $D T ( T _ { i } ) = \theta _ { d t } \times P ( T _ { i } )$ , where $\theta _ { d t } \in \{ 0 . 2 5 , 0 . 5 , 0 . 7 5 \}$ . The result transmission time $R T ( T _ { i } )$ (in second) is set to be $P ( T _ { i } ) \times$ 0.01. The deadline $D ( T _ { i } )$ is set to $C T ( T _ { i } ) _ { m i n } \times \theta _ { d } .$ , where $\theta _ { d } \in \{ 5 , 1 0 , 1 5 \} . C T ( T _ { i } ) _ { m i n }$ is defined as the earliest completion time of $T _ { i }$ , which is computed by assuming the closest UAV to process the task in an exclusive manner. The unit price setting of UAVs satisfies the equation $\alpha = \theta _ { p } \times \beta$ with $\theta _ { p } \in \{ 2 , 4 , 6 \}$

There are $4 \times 2 \times 4 \times 3 \times 3 \times 3 = 8 6 4$ instance combinations $( n \in \{ 4 8 , 7 6 , 1 5 0 , 5 3 2 \}$ ï¼ m $\in \{ \lceil \frac { n } { 2 0 } \rceil , \lceil \frac { n } { 2 5 } \rceil \}$ , Î½ â $\{ 2 0 , 3 0 , 4 0 , 5 0 \} , \theta _ { d t } \in \{ 0 . 2 5 , 0 . 5 , 0 . 7 5 \} , \theta _ { d } \in \{  { \mathbb { S } } , 1 0 , 1 5 \} , \theta _ { p } \in  { \mathbb { R } } ^ { d } .$ $\{ 2 , 4 , 6 \} )$ .

## C. Parameter and Component Calibration

In order to show the advancement of the component SDM, two variants of the main framework are calibrated: the one with SDM (bi-ACO), and the one without it (bi-ACO-noSDM). In FSGM, each ant breaks the loop at a given probability which is computed based on the index of the colony and the breaking factor $\theta _ { b }$ (Line 25, Algorithm 2). To demonstrate the usefulness of this loop-breaking step, the variants of FSGM with different settings of $\theta _ { b } \in \{ 0 , 0 . 1 , 0 . 3 , 0 . 5 , 0 . 7 , 0 . 9 \}$ are calibrated. FSGM with $\theta _ { b } = 0$ is the variant without the breaking step. Besides, one algorithm parameter is calibrated: the colony number $\mathcal { N } \in \{ 1 , 5 , 1 0 , 2 0 \}$ . There are $2 \times 6 \times 4 = 4 8$ variants of the proposed bi-ACO in total to calibrate. Three random instances are generated for each possible combination of testing instances. Therefore, the variants of the proposal are calibrated on $8 6 4 \times 3 = 2 5 9 2$ instances in total. In other words, $4 8 \times 2 5 9 2 = 1 2 4$ , 416 experimental results are obtained. These experimental results are analyzed by the multi-factor analysis of variance (ANOVA) technique.

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->

Fig. 6. Mean plots of variants across all instances with 95.0% Tukey HSD intervals.  
<!-- image-->

<!-- image-->  
Fig. 7. Mean plots of variants with different N across all instances with 95.0% Tukey HSD intervals.

<!-- image-->

<!-- image-->

Fig. 6 shows four Pareto-based metrics for variants with 95.0% Tukey Honest Significant Difference (HSD) intervals. It can be observed that bi-ACO with SDM outperforms the one without SDM on all metrics. The reason lies in that SDM can improve the diversity of solutions in the non-dominated solution set. Fig. 6 also shows a statistically significant difference for the performance of FSGM variants on all metrics. FSGM variants with the loop-breaking step have better performance than the one without it $( \theta _ { b } = 0 )$ . We can observe that FSGM with $\theta _ { b } = 0 . 7$ has the best performance on the most metrics. If there is no loop-breaking step, every UAV is assigned as many tasks as possible, which would lead to longer completion time. Breaking the loop at a given probability can balance the workload of UAVs to some extend. It is reasonable that FSGM with the loop-breaking step demonstrates better performance.

As shown in Fig. $7 , \mathcal { N } = 1$ has the worst performance. The performance of variants with the other settings (N = 5, 10, 20) are not significantly different. In the variant with ${ \mathcal { N } } = 5$ , less ants are introduced, which means less computation time. Therefore, it is reasonable to set $\mathcal { N } = 5$ in the proposal.

Therefore, the best parameter and component combination is bi-ACO with SDM and loop-breaking components, and $\mathcal { N } = 5$

## D. Algorithm Comparison

The proposed bi-ACO is compared with five baseline algorithms for the similar problems: 1) NSGA-II [33], 2) Simulated Annealing (SA) [39], 3) Variable Neighborhood Descent (VND) [40], 4) Greedy Local Search (GLS) [33] and 5) ACO-DSP [16]. We adopt the similar component and parameter settings given in [33] for NSGA-II, SA, VND and GLS. In [16], ACO-DSP is an ACO variant for drone scheduling problem. ACO-DSP is developed for singe objective. In order to solve the bi-objective problem under study, we modify ACO-DSP in [16] by integrating it into an iterative heuristics with different preferences of objectives.

To compare the algorithms, 5 instances are randomly generated for each instance combination, i.e., $8 6 4 \times 6 = 5$ , 184 new instances for comparison. Four Pareto-based metrics for the compared algorithms are shown in Table VâVI. Table V illustrates that bi-ACO has the best performance on metric AQ (0.189) for all instance combinations. ACO-DSP is the second best one on the metric AQ (0.460), while VND is the worst one on the metric (0.729). For the metric MS, SA (0.958) outperforms all the other algorithms on most cases. Although bi-ACO does not have the best performance on metric MS, it is the second best one (0.940). VND performs the worst (0.016). Table VI shows that bi-ACO has the best performance on both $D _ { a v g }$ (0.04) and $D _ { \mathrm { m a x } }$ (0.172) for all instance combinations. ACO-DSP is the second best one on metrics $D _ { a v g } ( 0 . 5 6 )$ and $D _ { \operatorname* { m a x } } \left( 0 . 7 4 1 \right)$ .VND and GLS have the worst performance on $D _ { a v g } ( 0 . 8 1 6 )$ and $D _ { \mathrm { m a x } }$ (0.942), respectively. Table VII shows that the computation time of bi-ACO is more time-consuming than that of GLS and SA but less than that of VND, NSGA-II and ACO-DSP for all cases. According to the performance of compared algorithms on all metrics, we can conclude that bi-ACO is the most effective algorithm among all compared ones.

TABLE V  
EXPERIMENTAL RESULTS ON METRICS AQ AND MS
<table><tr><td rowspan="2">Param.</td><td rowspan="2">Value</td><td colspan="6">Average Quality (AQ)</td><td colspan="6">Maximum Spread (MS)</td></tr><tr><td>bi-ACO</td><td>GLS</td><td>NSGA-II</td><td>SA</td><td>VND</td><td>ACO-DSP</td><td>bi-ACO</td><td>GLS</td><td>NSGA-II</td><td>SA</td><td>VND</td><td>ACO-DSP</td></tr><tr><td rowspan="4">n</td><td>48 60</td><td>0.141</td><td>0.731</td><td>0.386</td><td>0.453</td><td>0.742</td><td>0.490</td><td>0.969</td><td>0.100</td><td>0.393</td><td>0.920</td><td>0.023</td><td>0.708</td></tr><tr><td></td><td>0.131</td><td>0.799</td><td>0.527</td><td>0.606</td><td>0.801</td><td>0.342</td><td>0.969</td><td>0.075</td><td>0.355</td><td>0.955</td><td>0.011</td><td>0.715</td></tr><tr><td>150 532</td><td>0.208</td><td>0.660</td><td>0.496</td><td>0.571</td><td>0.665</td><td>0.554</td><td>0.821</td><td>0.040</td><td>0.223</td><td>0.990</td><td>0.010</td><td>0.657</td></tr><tr><td></td><td>0.275</td><td>0.697</td><td>0.648</td><td>0.713</td><td>0.706</td><td>0.453</td><td>1.000</td><td>0.073</td><td>0.241</td><td>0.969</td><td>0.019</td><td>0.737</td></tr><tr><td rowspan="4">V</td><td>20 30</td><td>0.218</td><td>0.708</td><td>0.446</td><td>0.562</td><td>0.705</td><td>0.503</td><td>0.910</td><td>0.073</td><td>0.339</td><td>0.963</td><td>0.017</td><td>0.599</td></tr><tr><td>40</td><td>0.193</td><td>0.717</td><td>0.493</td><td>0.582</td><td>0.727</td><td>0.465</td><td>0.940</td><td>0.077</td><td>0.294</td><td>0.946</td><td>0.014</td><td>0.706</td></tr><tr><td>50</td><td>0.177 0.167</td><td>0.727</td><td>0.542</td><td>0.594 0.607</td><td>0.732</td><td>0.446 0.425</td><td>0.949</td><td>0.076</td><td>0.294</td><td>0.972</td><td>0.013</td><td>0.737</td></tr><tr><td>[n/20]</td><td></td><td>0.736</td><td>0.576</td><td></td><td>0.751</td><td></td><td>0.960</td><td>0.063</td><td>0.286</td><td>0.952</td><td>0.020</td><td>0.775</td></tr><tr><td rowspan="2">m</td><td>[n/25]</td><td>0.187 0.190</td><td>0.734 0.710</td><td>0.512 0.517</td><td>0.577 0.595</td><td>0.743 0.715</td><td>0.436 0.484</td><td>0.943 0.936</td><td>0.071 0.073</td><td>0.295 0.312</td><td>0.968</td><td>0.012 0.019</td><td>0.738 0.671</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.949</td><td></td><td></td></tr><tr><td rowspan="3"> $\theta _ { d t }$ </td><td>0.25 0.5</td><td>0.181</td><td>0.736</td><td>0.509 0.561</td><td>0.596 0.633</td><td>0.734 0.786</td><td>0.483</td><td>0.944 0.942</td><td>0.084</td><td>0.448</td><td>0.956</td><td>0.014 0.017</td><td>0.686 0.707</td></tr><tr><td>0.75</td><td>0.181 0.204</td><td>0.785 0.646</td><td>0.473</td><td>0.530</td><td>0.666</td><td>0.447 0.449</td><td>0.934</td><td>0.064 0.068</td><td>0.291 0.170</td><td>0.981</td><td>0.017</td><td>0.721</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.937</td><td></td><td></td></tr><tr><td rowspan="3"> $\theta _ { d }$ </td><td>5 10</td><td>0.145</td><td>0.614</td><td>0.507</td><td>0.615 0.584</td><td>0.606</td><td>0.320</td><td>0.992</td><td>0.051</td><td>0.429</td><td>0.875</td><td>0.022</td><td>0.932 0.429</td></tr><tr><td>15</td><td>0.234 0.187</td><td>0.741 0.811</td><td>0.514 0.522</td><td>0.559</td><td>0.757 0.823</td><td>0.618 0.442</td><td>0.844 0.983</td><td>0.110 0.055</td><td>0.302 0.178</td><td>1.000 1.000</td><td>0.020 0.005</td><td>0.753</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="3"> $\theta _ { p }$ </td><td>2 4</td><td>0.178</td><td>0.811</td><td>0.595</td><td>0.729</td><td>0.813</td><td>0.504</td><td>0.934</td><td>0.085</td><td>0.419</td><td>0.967</td><td>0.011</td><td>0.662 0.714</td></tr><tr><td></td><td>0.196</td><td>0.687</td><td>0.477</td><td>0.535 0.494</td><td>0.695 0.677</td><td>0.449 0.427</td><td>0.944 0.941</td><td>0.064 0.067</td><td>0.265 0.225</td><td>0.958</td><td>0.017 0.020</td><td></td></tr><tr><td>6</td><td>0.193</td><td>0.668</td><td>0.470</td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.950</td><td></td><td>0.737</td></tr><tr><td colspan="2">Average</td><td>0.189</td><td>0.722</td><td>0.514</td><td>0.586</td><td>0.729</td><td>0.460</td><td>0.940</td><td>0.072</td><td>0.303</td><td>0.958</td><td>0.016</td><td>0.704</td></tr></table>

TABLE VI

EXPERIMENTAL RESULTS ON METRICS $D _ { a v g }$ AND $D _ { \mathrm { m a x } }$
<table><tr><td rowspan="2">Param.</td><td rowspan="2">Value</td><td colspan="6">Average Distance  $( D _ { a v g } )$ </td><td colspan="6">Maximum Distance  $( D _ { m a x } )$ </td></tr><tr><td>bi-ACO</td><td>GLS</td><td>NSGA-II</td><td>SA</td><td>VND</td><td>ACO-DSP</td><td>bi-ACO</td><td>GLS</td><td>NSGA-II</td><td>SA</td><td>VND</td><td>ACO-DSP</td></tr><tr><td rowspan="4">n</td><td>48</td><td>0.012</td><td>0.813</td><td>0.412</td><td>0.566</td><td>0.823</td><td>0.625</td><td>0.063</td><td>0.932</td><td>0.679</td><td>0.714</td><td>0.931</td><td>0.828</td></tr><tr><td>60</td><td>0.004</td><td>0.857</td><td>0.612</td><td>0.772</td><td>0.861</td><td>0.369</td><td>0.035</td><td>0.938</td><td>0.834</td><td>0.881</td><td>0.935</td><td>0.655</td></tr><tr><td>150</td><td>0.047</td><td>0.774</td><td>0.546</td><td>0.705</td><td>0.783</td><td>0.715</td><td>0.227</td><td>0.936</td><td>0.853</td><td>0.897</td><td>0.932</td><td>0.837</td></tr><tr><td>532</td><td>0.097</td><td>0.783</td><td>0.702</td><td>0.826</td><td>0.799</td><td>0.529</td><td>0.365</td><td>0.960</td><td>0.931</td><td>0.966</td><td>0.963</td><td>0.642</td></tr><tr><td rowspan="4">V</td><td>20</td><td>0.080</td><td>0.787</td><td>0.465</td><td>0.683</td><td>0.788</td><td>0.638</td><td>0.265</td><td>0.932</td><td>0.755</td><td>0.865</td><td>0.926</td><td>0.838</td></tr><tr><td>30</td><td>0.037</td><td>0.807</td><td>0.549</td><td>0.716</td><td>0.819</td><td>0.583</td><td>0.182</td><td>0.941</td><td>0.819</td><td>0.865</td><td>0.940</td><td>0.767</td></tr><tr><td>40 50</td><td>0.026</td><td>0.808</td><td>0.609</td><td>0.727</td><td>0.816</td><td>0.529</td><td>0.138</td><td>0.941</td><td>0.855</td><td>0.864</td><td>0.942</td><td>0.700</td></tr><tr><td></td><td>0.016</td><td>0.825</td><td>0.650</td><td>0.742</td><td>0.842</td><td>0.488</td><td>0.104</td><td>0.952</td><td>0.869</td><td>0.865</td><td>0.954</td><td>0.657</td></tr><tr><td rowspan="3">m</td><td>[n/20] [n/25]</td><td>0.038</td><td>0.818</td><td>0.571</td><td>0.711</td><td>0.830</td><td>0.539</td><td>0.166</td><td>0.938</td><td>0.817</td><td>0.851</td><td>0.941</td><td>0.728</td></tr><tr><td></td><td>0.041</td><td>0.796</td><td>0.565</td><td>0.723</td><td>0.803</td><td>0.581</td><td>0.179</td><td>0.945</td><td>0.832</td><td>0.879</td><td>0.940</td><td>0.754</td></tr><tr><td>0.25</td><td>0.048</td><td>0.762</td><td>0.540</td><td>0.709</td><td>0.764</td><td>0.582</td><td>0.151</td><td>0.885</td><td>0.753</td><td>0.855</td><td>0.879</td><td>0.741</td></tr><tr><td rowspan="3"> $\theta _ { d t }$ </td><td>0.5 0.75</td><td>0.034</td><td>0.897</td><td>0.641</td><td>0.789</td><td>0.898</td><td>0.556</td><td>0.140</td><td>0.982</td><td>0.884</td><td>0.903</td><td>0.983</td><td>0.715</td></tr><tr><td></td><td>0.037</td><td>0.761</td><td>0.524</td><td>0.654</td><td>0.788</td><td>0.541</td><td>0.226</td><td>0.957</td><td>0.837</td><td>0.836</td><td>0.960</td><td>0.766</td></tr><tr><td>5</td><td>0.011</td><td>0.609</td><td>0.464</td><td>0.627</td><td>0.606</td><td>0.398</td><td>0.039</td><td>0.836</td><td>0.716</td><td>0.834</td><td>0.827</td><td>0.554</td></tr><tr><td rowspan="3"> $\theta _ { d }$ </td><td>10</td><td>0.077</td><td>0.870</td><td>0.616</td><td>0.769</td><td>0.893</td><td>0.763</td><td>0.320</td><td>0.990</td><td>0.874</td><td>0.894</td><td>0.995</td><td>0.920</td></tr><tr><td>15</td><td>0.031</td><td>0.941</td><td>0.624</td><td>0.756</td><td>0.950</td><td>0.518</td><td>0.159</td><td>0.999</td><td>0.883</td><td>0.867</td><td>0.999</td><td>0.747</td></tr><tr><td>2</td><td>0.038</td><td>0.875</td><td>0.650</td><td>0.854</td><td>0.877</td><td>0.639</td><td>0.157</td><td>0.966</td><td>0.853</td><td>0.946</td><td>0.966</td><td>0.798</td></tr><tr><td rowspan="2"> $\theta _ { p }$ </td><td>4 6</td><td>0.040</td><td>0.782</td><td>0.535</td><td>0.672</td><td>0.796</td><td>0.535</td><td>0.184</td><td>0.937</td><td>0.811</td><td>0.835</td><td>0.936</td><td>0.729</td></tr><tr><td></td><td>0.041</td><td>0.763</td><td>0.520</td><td>0.625</td><td>0.776</td><td>0.505</td><td>0.176</td><td>0.921</td><td>0.809</td><td>0.814</td><td>0.920</td><td>0.694</td></tr><tr><td colspan="2">Average</td><td>0.040</td><td>0.807</td><td>0.568</td><td>0.717</td><td>0.816</td><td>0.560</td><td>0.172</td><td>0.942</td><td>0.824</td><td>0.865</td><td>0.940</td><td>0.741</td></tr></table>

<!-- image-->

<!-- image-->

<!-- image-->

<!-- image-->  
Fig. 8. Interactions between instance parameters and the compared algorithms with 95.0% Tukey HSD intervals.

TABLE VII  
COMPUTATION TIME OF COMPARED ALGORITHMS
<table><tr><td rowspan="2"> $n , \theta _ { d }$ </td><td colspan="6">Time (s)</td></tr><tr><td>bi-ACO</td><td>GLS</td><td>NSGA-II</td><td>SA</td><td>VND</td><td>ACO-DSP</td></tr><tr><td>48,5</td><td>12.21</td><td>2.87</td><td>51.82</td><td>2.29</td><td>114.11</td><td>185.74</td></tr><tr><td>60,5</td><td>18.42</td><td>4.00</td><td>131.32</td><td>5.30</td><td>190.30</td><td>283.31</td></tr><tr><td>150,5</td><td>81.17</td><td>3.94</td><td>462.26</td><td>7.74</td><td>685.05</td><td>914.08</td></tr><tr><td>532,5</td><td>637.13</td><td>2.17</td><td>1883.86</td><td>16.34</td><td>1782.55</td><td>9970.69</td></tr><tr><td>48,10</td><td>11.68</td><td>2.87</td><td>86.62</td><td>1.58</td><td>282.66</td><td>193.08</td></tr><tr><td>60,10</td><td>17.95</td><td>4.49</td><td>315.15</td><td>3.75</td><td>352.01</td><td>297.58</td></tr><tr><td>150,10</td><td>79.99</td><td>4.98</td><td>1390.98</td><td>5.99</td><td>1076.64</td><td>915.22</td></tr><tr><td>532,10</td><td>723.25</td><td>4.28</td><td>5502.38</td><td>11.85</td><td>1959.62</td><td>9990.06</td></tr><tr><td>48,15</td><td>12.03</td><td>5.37</td><td>92.27</td><td>1.27</td><td>195.42</td><td>186.93</td></tr><tr><td>60,15</td><td>18.33</td><td>4.62</td><td>257.21</td><td>2.70</td><td>772.10</td><td>293.46</td></tr><tr><td>150,15</td><td>79.01</td><td>4.81</td><td>1586.62</td><td>5.70</td><td>960.77</td><td>912.98</td></tr><tr><td>532,15</td><td>647.02</td><td>5.32</td><td>10263.7</td><td>10.77</td><td>906.06</td><td>9909.66</td></tr><tr><td>Avg.</td><td>194.85</td><td>4.15</td><td>1835.36</td><td>6.28</td><td>773.11</td><td>2837.73</td></tr></table>

In order to show the robustness and reliability of the proposed algorithm, we conduct the parameter sensitivity experiments. Fig. 8 depicts the interactions between instance parameters and the compared algorithms. From Fig. 8 we can observe that bi-ACO is less sensitive to the parameter changes for most cases. For the metric of AQ, bi-ACO is a little sensitive to the parameter n. For the metric of MS, bi-ACO is robust on most parameters except n and $\theta _ { d } .$ For the metric of $D _ { a v g } ,$ bi-ACO is reliable on all parameters. For the metric of $D _ { \mathrm { m a x } } ,$ bi-ACO is sensitive only on parameters n and $\theta _ { d } .$ . Besides, we design three kinds of maps MAP1, MAP2 and MAP3 to show the performances of the compared algorithms on the different SD distributions. MAP1 includes 6 base stations and 60 SDs which are randomly generated obeying uniform distribution. In MAP2, 6 base stations are randomly generated obeying uniform distribution first, and then 60 SDs are uniformly distributed within 1000 meters of base stations. In MAP3, 6 base stations are randomly generated obeying uniform distribution first, and then 60 SDs are normally distributed around base stations. Fig. 9 depicts the performance of the compared algorithms with different SD distributions. It can be seen from the figure that the proposed algorithm is relatively stable with different SD distributions compared to other algorithms. Therefore, we can conclude that bi-ACO is robust and reliable for the problem under study.

Based on the experimental results, we can conclude that the proposed bi-ACO is the most effective and robust algorithm for the problem under study. It consumes more time than some of compared algorithms, however, it is acceptable for practical applications with respect to the solution quality of bi-ACO.

<!-- image-->  
Fig. 9. Interactions between SD distributions and the compared algorithms with 95.0% Tukey HSD intervals.

In order to show the feasibility of the proposed bi-ACO in practise, we perform the field tests. We adopt the remote control method for the field tests, i.e., the proposed bi-ACO runs on a powerful server and the trajectory plans it produces are sent to UAVs to perform. The field tests show that it is feasible to implement the proposed algorithm on real UAVs. The detail of the field tests is given in Appendix B, available online.

## VI. CONCLUSION

In this paper, we studied the problem jointly considering the multi-UAV trajectory planning and multi-stage task offloading. The problem involves the energy, deadline and precedence constraints, and the objectives are to minimize the total cost and the completion time. To solve the problem, we proposed the bi-ACO algorithm to obtain a non-dominated set containing promising solutions. In bi-ACO framework, massive ants are divided into several heterogeneous colonies, and ants in different colonies has different preferences of objectives to explore. Each colony maintains five pairs of pheromone matrices for computing the probability for selecting tasks and determining the insertion positions of tasks. Each ant first adopts component FSGM to generate a feasible solution according to the pheromone matrices and heuristic values, and then calls SDM to further improve the obtained solution. At the end of each iteration of bi-ACO, PUM is used to update pheromone matrices based on the obtained non-dominated solutions. Algorithm calibration was conducted to determine the best component and parameter combination for the bi-ACO framework. Then we evaluate performance of bi-ACO, NSGA-II, SA, VND, GLS and ACO by four Paretobased metrics. The experimental results illustrates that bi-ACO outperforms the compared algorithms on most metrics.

## REFERENCES

[1] J. Wang, C. Jin, Q. Tang, N. N. Xiong, and G. Srivastava, âIntelligent ubiquitous network accessibility for wireless-powered MEC in UAV-assisted B5G,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 4, pp. 2801â2813, Fourth Quarter, 2021.

[2] K. Li, W. Ni, X. Wang, R. P. Liu, S. S. Kanhere, and S. Jha, âEnergyefficient cooperative relaying for unmanned aerial vehicles,â IEEE Trans. Mobile Comput., vol. 15, no. 6, pp. 1377â1386, Jun. 2016.

[3] N. Zhao et al., âCaching UAV assisted secure transmission in hyper-dense networks based on interference alignment,â IEEE Trans. Commun., vol. 66, no. 5, pp. 2281â2294, May 2018.

[4] P. Valianti, P. Kolios, and G. Ellinas, âEnergy-aware tracking and jamming rogue UAVs using a swarm of pursuer UAV agents,â IEEE Syst. J., vol. 17, no. 1, pp. 1524â1535, Mar. 2023.

[5] J. Wang, K. Liu, and J. Pan, âOnline UAV-mounted edge server dispatching for mobile-to-mobile edge computing,â IEEE Internet Things J., vol. 7, no. 2, pp. 1375â1386, Feb. 2020.

[6] S. Hu, X. Yuan, W. Ni, X. Wang, E. Hossain, and H. V. Poor, âOFDMA-F2L: Federated learning with flexible aggregation over an OFDMA air interface,â IEEE Trans. Wireless Commun., early access, Jan. 15, 2024, doi: 10.1109/TWC.2023.3334691.

[7] H. Liu et al., âAn iterative two-phase optimization method based on divide and conquer framework for integrated scheduling of multiple UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 9, pp. 5926â5938, Sep. 2021.

[8] R. Yadav, W. Zhang, O. Kaiwartya, H. Song, and S. Yu, âEnergy-latency tradeoff for dynamic computation offloading in vehicular fog computing,â IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 14198â14211, Dec. 2020.

[9] H. Huang, C. Hu, J. Zhu, M. Wu, and R. Malekian, âStochastic task scheduling in UAV-based intelligent on-demand meal delivery system,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 13040â13054, Aug. 2022.

[10] Q. Luan, H. Cui, L. Zhang, and Z. Lv, âA hierarchical hybrid subtask scheduling algorithm in UAV-assisted MEC emergency network,â IEEE Internet Things J., vol. 9, no. 14, pp. 12737â12753, Jul. 2022.

[11] Y. Du, K. Yang, K. Wang, G. Zhang, Y. Zhao, and D. Chen, âJoint resources and workflow scheduling in UAV-enabled wirelessly powered MEC for IoT systems,â IEEE Trans. Veh. Technol., vol. 68, no. 10, pp. 10187â10200, Oct. 2019.

[12] K. Zhang, X. Gui, D. Ren, and D. Li, âEnergy latency tradeoff for computation offloading in UAV-assisted multiaccess edge computing system,â IEEE Internet Things J., vol. 8, no. 8, pp. 6709â6719, Apr. 2021.

[13] Y. Liao, X. Chen, S. Xia, Q. Ai and Q. Liu, âEnergy minimization for UAV swarm-enabled wireless inland ship MEC network with time windows,â IEEE Trans. Green Commun. Netw., vol. 7, no. 2, pp. 594â608, Jun. 2023.

[14] Z. Wang, R. Liu, Q. Liu, J. S. Thompson, and M. Kadoch, âEnergy-efficient data collection and device positioning in UAV-assisted IoT,â IEEE Internet Things J., vol. 7, no. 2, pp. 1122â1139, Feb. 2020.

[15] N. Bartolini, A. Coletta, G. Maselli, and A. Khalifeh, âA multi-trip task assignment for early target inspection in squads of aerial drones,â IEEE Trans. Mobile Comput., vol. 20, no. 11, pp. 3099â3116, Nov. 2021.

[16] Z.-H. Sun, X. Luo, E. Q. Wu, T.-Y. Zuo, Z.-R. Tang, and Z. Zhuang, âMonitoring scheduling of drones for emission control areas: An ant colony-based approach,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 11699â11709, Aug. 2022.

[17] E. S. Rigas, P. Kolios, M. Mavrovouniotis, and G. Ellinas, âScheduling a fleet of drones for monitoring missions with spatial, temporal, and energy constraints,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 15133â15145, Sep. 2022.

[18] S. Hu, X. Yuan, W. Ni, X. Wang and A. Jamalipour, âRIS-assisted jamming rejection and path planning for UAV-borne IoT platform: A new deep reinforcement learning rramework,â IEEE Internet Things J., vol. 10, no. 22, pp. 20162â20173, Nov. 2023.

[19] M. Kang and S. W. Jeon, âEnergy-efficient data aggregation and collection for Multi-UAV-Enabled IoT networks,â IEEE Wireless Commun. Lett., vol. 13, no. 4, pp. 1004â1008, Apr. 2024.

[20] N. Zhao et al., âJoint trajectory and precoding optimization for UAV-Assisted NOMA networks,â IEEE Trans. Commun., vol. 67, no. 5, pp. 3723â3735, May 2019.

[21] X. Pang, N. Zhao, J. Tang, C. Wu, D. Niyato and K. Wong, âIRS-Assisted secure UAV transmission via joint trajectory and beamforming design,â IEEE Trans. Commun., vol. 70, no. 2, pp. 1140â1152, Feb. 2022.

[22] N. L. Prasad and B. Ramkumar, â3-D deployment and trajectory planning for relay based UAV assisted cooperative communication for emergency scenarios using Dijkstraâs algorithm,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5049â5063, Apr. 2023.

[23] E. Eldeeb, J. M. d.S. SantâAna, D. E. PÃ©rez, M. Shehab, N. H. Mahmood, and H. Alves, âMulti-UAV path learning for age and power optimization in IoT with UAV battery recharge,â IEEE Trans. Veh. Technol., vol. 72, no. 4, pp. 5356â5360, Apr. 2023.

[24] C. Sun, W. Ni, and X. Wang, âJoint computation offloading and trajectory planning for UAV-assisted edge computing,â IEEE Trans. Wireless Commun., vol. 20, no. 8, pp. 5343â5358, Aug. 2021.

[25] C. Lin et al., âNear optimal charging schedule for 3-D wireless rechargeable sensor networks,â IEEE Trans. Mobile Comput., vol. 22, no. 6, pp. 5343â5358, Jun. 2023.

[26] Y. Miao, K. Hwang, D. Wu, Y. Hao, and M. Chen, âDrone swarm path planning for mobile edge computing in Industrial Internet of Things,â IEEE Trans. Ind. Inform., vol. 19, no. 5, pp. 6836â6848, May 2023.

[27] A. Khochare, F. B. Sorbelli, Y. WSimmhan, and S. K. Das, âImproved algorithms for co-scheduling of edge analytics and routes for UAV fleet missions,â IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 17â33, Feb. 2024. doi: 10.1109/TNET.2023.3277810.

[28] J. Tian, D. Wang, H. Zhang, and D. Wu, âService satisfaction-oriented task offloading and UAV scheduling in UAV-enabled MEC networks,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8949â8964, Dec. 2023. doi: 10.1109/TWC.2023.3267330.

[29] L. Yu, X. Sun, S. Shao, Y. Chen, and R. Albelaihi, âBackhaul-aware drone base station placement and resource management for FSO-based droneassisted mobile networks,â IEEE Trans. Netw. Sci. Eng., vol. 10, no. 3, pp. 1659â1668, May/Jun. 2023.

[30] J. Luo, J. Song, F. C. Zheng, L. Gao, and T. Wang, âUser-centric UAV deployment and content placement in cache-enabled multi-UAV networks,â IEEE Trans. Veh. Technol., vol. 71, no. 5, pp. 5656â5660, May 2022.

[31] Y. Liu, W. Huangfu, H. Zhou, H. Zhang, J. Liu and K. Long, âFair and energy-efficient coverage optimization for UAV placement problem in the cellular network,â IEEE Trans. Commun., vol. 70, no. 6, pp. 4222â4235, Jun. 2022.

[32] F. Fazel, J. Abouei, M. Jaseemuddin, A. Anpalagan and K. N. Plataniotis, âSecure throughput optimization for cache-enabled multi-UAVs networks,â IEEE Internet Things J., vol. 9, no. 10, pp. 7783â7801, May 2022.

[33] J. Zhu, X. Wang, H. Huang, S. Cheng, and M. Wu, âA NSGA-II algorithm for task scheduling in UAV-enabled MEC system,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 9414â9429, Jul. 2022.

[34] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[35] A. Jaszkiewicz, âDo multiple-objective metaheuristics deliver on their promises? A computational experiment on the set-covering problem,â IEEE Trans. Evol. Comput., vol. 7, no. 2, pp. 133â143, Apr. 2003.

[36] K. C. Tan, C. K. Goh, Y. J. Yang, and T. H. Lee, âEvolving better population distribution and exploration in evolutionary multi-objective optimization,â Eur. J. Oper. Res., vol. 171, no. 2, pp. 463â495, 2006.

[37] P. Czyzzak, and A. Jaszkiewicz, âPareto simulated annealing-a metaheuristic technique for multiple-objective combinatorial optimization,â J. Multi Criteria Decis. Anal., vol. 7, no. 1, pp. 34â47, 1998.

[38] G. Reinelt, âTSPLIB-a traveling salesman problem library,â INFORMS J. Comput., vol. 3, no. 3, pp. 376â384, 1991.

[39] H. Daryanavard and A. Harifi, âUAV path planning for data gathering of IoT nodes: Ant colony or simulated annealing optimization,â in Proc. 3rd Int. Conf. Internet Things Appl., 2019, pp. 1â4.

[40] H. Liu et al., âAn iterative two-phase optimization method based on divide and conquer framework for integrated scheduling of multiple UAVs,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 9, pp. 5926â5938, Sep. 2021.

<!-- image-->

Yiqian Wang received the B.E degree in computer science and technology from the Nanjing University of Posts and Telecommunications, Nanjing, China. He is working toward the master degree in the the School of Computer Science and Engineering, Southeast University, Nanjing. His research interests include trajectory planning and task scheduling.

<!-- image-->

Jie Zhu received the PhD degree in applied computer science from the School of Computer Science and Engineering, Southeast University, Nanjing, in 2011. From 2008 to 2009, she was with the Department of Electrical and Computer Engineering, University of Western Ontario, London, ON, Canada, as a visiting student. She joined the Nanjing University of Post and Telecommunication in 2014, where she is currently an associate professor with the School of Computer Science. Her research interests include machine scheduling, project scheduling, workflow optimization, and cloud computing, among which task scheduling and resource provisioning in clouds are her current core research areas.

<!-- image-->

Haiping Huang (Member, IEEE) received the BEng and MEng degrees in computer science and technology from the Nanjing University of Posts & Telecommunications, Nanjing, China, in 2002 and 2005, respectively, and the PhD degree in computer application technology from Soochow University, China, in 2009. From May 2013 to November 2013, he was a visiting scholar with the School of Electronics and Computer Science, University of Southampton, Southampton, U.K. He is currently a professor with the School of Computer Science and Technology,

Nanjing University of Posts and Telecommunications. His research interests include information security and privacy protection of wireless sensor networks.

<!-- image-->

Fu Xiao (Member, IEEE) received the PhD degree in computer science and technology from the Nanjing University of Science and Technology, Nanjing, China, in 2007. He is currently a professor and a PhD supervisor with the School of Computer Science, Nanjing University of Posts and Telecommunications, Nanjing. His research interests include wireless sensor networks.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_6_img_1.png|page_6_img_1]]
2. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_6_img_2.jpeg|page_6_img_2]]
3. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_9_img_1.png|page_9_img_1]]
4. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_13_img_1.jpeg|page_13_img_1]]
5. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_14_img_1.png|page_14_img_1]]
6. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_16_img_1.png|page_16_img_1]]
7. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_18_img_1.jpeg|page_18_img_1]]
8. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_18_img_2.jpeg|page_18_img_2]]
9. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_18_img_3.jpeg|page_18_img_3]]
10. [[../extracted_images/Wang 等 - 2024 - Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-Assisted MEC/page_18_img_4.jpeg|page_18_img_4]]

---

