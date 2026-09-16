# Practical Optimizing UAV Trajectory in Wireless Charging Networks: An Approximated Approach

Yundi Wang , Xiaoyu Wang , He Huang , Senior Member, IEEE, and Haipeng Dai , Senior Member, IEEE

AbstractâUnmanned Aerial Vehicles (UAVs) can be easily deployed as auxiliary base stations due to their convenience and flexibility. However, limited battery capacity becomes a bottleneck. Promising wireless power transfer (WPT) technologies can provide a continuous power supply for UAVs. Many of the recent works treat the UAV battery capacity as a constraint, which hinders the assurance of continuous UAV operation. Furthermore, most studies employ intelligent path-planning algorithms that lack explicit performance guarantees. In this paper, we study the problem of Practical Optimizing UAV Trajectory in Wireless Charging Networks (POTWCN), which involves planning the trajectory of the wireless-powered UAV in the practical environment with obstacles by selecting candidate passing positions and determining the access order in the charging network. The goal is to maximize the benefit, i.e., balancing the total task completion time and the number of charging stations visited, so as to minimize path length and flight time, and ensure energy constraints with performance bound. To solve this problem, we first formalize the problem and prove its submodularity. Then, we propose the obstacle-aware weighted graph generation algorithm (OWGGA) to deal with the obstacles in the environment, which forms an obstacle-avoidance path using tangents and arcs between two hovering positions and the blocking obstacles. Next, we propose a dynamic charging station selection algorithm (ACSA), which maximizes the UAVâs energy utilization by limiting the number of charging stations that can be included. In the algorithm, we introduce the Christofides algorithm and use the path length calculated by OWGGA as the edge weights of the graph. Subsequently, considering the UAVâs energy constraints, we iteratively solve the UAV trajectory planning problem by adding the charging station with a maximized marginal benefit to the path. We prove that the proposed algorithm achieves an approximation ratio 1 â 1/e as well as the path length is at most 3Ï/4 times the optimal solution. Simulation results show that our algorithm reduces the flight distance by 38.01% and the task completion time by 34.00% on average.

Index TermsâUAV trajectory optimization, approximation algorithm, wireless charging network.

## I. INTRODUCTION

U NMANNED Aerial Vehicles (UAVs) have garnered sig-nificant attention as a key technology due to their high flexibility, low cost, strong line-of-sight (LoS) communication for both downlink and uplink transmissions, and easy deployment [1]. The future market for UAVs is substantial. According to market research, the overall UAV market is projected to grow to 48.5 billion by 2029, with a compound annual growth rate \$(CAGR) of 9.9% [2].

Currently, UAVs can be used as communication base stations for data transmission tasks, as well as they can amplify Internet signals to provide access services to remote areas. However, as the demand for UAV capabilities grows, the energy constraints of UAVs increasingly fail to meet these demands. The rapidly developing technology of Wireless Power Transfer (WPT) offers a potential solution to this issue. For instance, SF Express began piloting drone logistics in 2017, primarily for express delivery in remote areas such as mountains and islands with limited transportation access. SFâs drones are equipped with high-capacity batteries and communication modules, enabling long-distance flights and real-time data transmission to assist in communication [3]. PowerLight Technologies has proposed deploying fiber optic power delivery technology on the ground and in the air, capable of transmitting hundreds of watts over hundreds of meters to charge UAVs [4]. Companies such as Huawei and Xiaomi have also introduced the concept of providing wireless charging through 5G base stations [5]. These applications demonstrate that integrating WPT technology with UAVs can effectively enhance UAV endurance, significantly improve task performance, and showcase substantial application potential.

Some research has integrated WPT technology. For example, research has incorporated UAV energy constraints into trajectory planning [6], [7], [8], set up UAV wireless charging stations [9], [10], and considered recharging UAVs during mission execution [11], [12]. However, there are still notable shortcomings. Certain studies perceive the energy constraint as a given condition, neglecting the aspect of recharging. Others consider charging as a static condition without incorporating dynamic planning for UAV trajectories. Still, some utilize intelligent algorithms such as heuristics, without establishing performance bounds.

At the same time, in the path planning problem, it is also necessary to consider real-world environmental factors and model this complex environment. UAVs need to accurately evaluate paths by taking into account fundamental constraints such as flight time, path length, and energy limitations, and plan reasonable routes to avoid obstacles [13]. Nowadays, UAV path planning has been proven to be an NP-hard problem [14]. However, while path planning primarily focuses on feasibility, our objective is to explore path optimization based on feasible paths, which is a more complex problem.

Specifically, we consider the problem of Practical Optimizing UAV Trajectory in Wireless Charging Networks (POTWCN), i.e., given all environmental information, planning an optimal closed and obstacle-avoiding trajectory for the UAV by selecting candidate passing positions and determining the access order, ensuring all devices are covered without depleting the UAVâs battery. The goal is to maximize the benefit, that is, to balance the total task completion time and the number of charging stations visited, while minimizing path length and time as much as possible, and ensuring energy constraints are met.

This problem is challenging for several reasons. First, due to the presence of obstacles in the environment, appropriate obstacle avoidance methods must be employed to ensure that the trajectory calculated during subsequent path planning remains feasible. Second, we need to compute a closed trajectory that passes through all known data collection points while minimizing the cost. This is essentially a Traveling Salesman Problem (TSP), which is NP-hard. Third, we must ensure that the UAV can remain in service, i.e., meeting energy constraints. We need to effectively select and add optimal charging stations to the trajectory to balance total time and the number of selected charging stations. Fourth, we need to consider all factors, including UAV flying distance, energy constraints, etc., to come up with the final algorithm with performance bound.

For the first challenge, we propose an obstacle-aware weighted graph generation algorithm (OWGGA) with $\pi / 2$ ap-2proximation, which specifically avoids obstacles by using tangent lines from the starting point and the arcs. For the second challenge, we introduce the Christofides algorithm [15] in our algorithm to solve the Traveling Salesman Problem (TSP) and integrate the OWGGA algorithm into the input graph of the TSP algorithm, enabling the calculated trajectory to achieve obstacle avoidance. For the third challenge, we first prove the submodularity of the objective function and then apply a greedy approach. Finally, in the algorithm, we dynamically adjust the number of charging stations the UAV passes through based on its energy level in each iteration. This ensures that the UAV meets energy constraints. We form the final algorithm as the adaptive charging station algorithm (ACSA), which has a  â /e approximation 1 1ratio and the path length is at most Ï/ times the optimal solution.

Simulation results demonstrate that our proposed algorithm reduces the flight distance by 38.01% and requires 34.00% less completion time on average compared with other algorithms, while also ensuring the convergence and stability of the results.

## II. RELATED WORK

Trajectory planning for energy-constrained UAVs: For example, Dai et al. [7] addressed UAV-assisted vehicle task offloading to minimize delays. Xu et al. [8] designed a multi-UAV base station cooperative edge computing scenario with energy constraints. Gong et al. [16] investigated the problem of minimizing both the number of energy-constrained UAV base stations and their energy consumption.

In addition to the aforementioned heuristic algorithms, some related works have also proposed approximation algorithms with provable approximation ratios. For example, Wang et al. [17] present a $1 - ( 1 - 1 / K ) ^ { K }$ -approximation algorithm to dynami-1 (1 1 )cally determine cooperative path planning for K UAVs, optimizing coverage of usersâ spatio-temporally distributed demands. Li et al. [18] proposed a / -approximation algorithm for 1 3data collection maximization problems to deal with full data collection from IoT devices. Qu et al. [19] designed a $1 / ( 4 + \epsilon ) \cdot$ approximation algorithm (where  is an arbitrarily small positive parameter) for urban sensing tasks using delivery drones, jointly optimizing route selection, sensing time, and delivery weight allocation to maximize delivery and sensing utility under energy constraints. Xu et al. [20] proposed a heterogeneous drone scheduling algorithm with $\mathrm { ~ a ~ } 1 / 3$ approximation ratio, coordi-1 3nating drones with different functionalities to monitor points of interest in disaster scenarios, achieving maximum monitoring revenue under energy constraints. Xu et al. [21] further developed a $1 / ( 6 + \epsilon )$ -approximation algorithm to solve the problem 1 (6 + )of finding a data collection trajectory for an energy-constrained UAV, maximizing the cumulative utility of collected data, where  is a given constant with $\epsilon > 0$ . These studies demonstrate the 0broad applicability and efficiency of approximation algorithms in UAV trajectory planning and resource optimization.

However, whether using heuristic approaches or efficient approximation algorithms, such work still fundamentally fails to address the energy constraints of UAVs, as they merely treat battery capacity as a single constraint.

Obstacle-avoidance trajectory planning for energyconstrained UAVs: Some studies have designed obstacle avoidance algorithms for UAVs while accounting for energy constraints. Most existing obstacle avoidance algorithms in the field of UAV fall into two categories.

1) Sampling-based algorithms: The Artificial Potential Field (APF) method, commonly used in autonomous vehicle driving [22], has the drawback of a slow convergence rate in complex environments. And for the typical sampling-based algorithm RRT [23] and its variants [24], [25], [26], however, the path calculated by the RRT algorithm is often rugged. Moreover, due to the randomness of the sampling algorithms, their convergence speed and efficiency are also subject to certain limitations.

2) Heuristic algorithms: Currently, a series of Genetic Algorithm (GA) [27] variants have been applied in the UAV domain [28], [29], [30], [31]. However, due to the uncontrollability of genetic crossover and mutation, genetic algorithms often exhibit poor local optimization capability and slow convergence speed [27]. Inspired by the predatory behavior of birds, the Particle Swarm Optimization (PSO) algorithm [32] has been proposed. For example, Pan et al. [6] jointly optimized UAV power allocation and trajectories in wireless-powered communication networks considering obstacles using PSO. However, the classic PSO algorithm tends to converge prematurely and get trapped in local optima. On the other hand, the Simulated

Annealing (SA) algorithm, based on the annealing process of physical phenomena, can probabilistically escape local optima [33]. Consequently, some studies have combined the PSO algorithm with the SA algorithm [34]. Although heuristic algorithms can address more complex optimization problems, they still exhibit deficiencies compared with approximation algorithms that can find quality-guaranteed solutions within a reasonable time.

To sum up, while these studies have explored more complex mission scenarios for UAVs, they either treat energy merely as a constraint without addressing replenishment or rely on intelligent algorithms without establishing performance bounds. Consequently, the proposed solutions are not applicable to our work.

Deployment and planning of UAVs with wireless charging stations: Lahmeri et al. [10] proposed a laser-powered UAV deployment strategy to balance energy supply and wireless coverage. Song et al. [9] introduced a UAV deployment strategy to maximize k-coverage duration by considering charging and working as two distinct states. However, these studies solely focus on the field of wireless charging itself or merely consider charging as a static state, failing to consider how to plan UAV wireless charging trajectories during actual mission execution. Subsequently, these studies cannot be applied to the problem in our paper.

Charging UAVs during trajectory planning: Du et al. [11] proposed a trajectory optimization algorithm to maximize the number of IoT devices serviced before their deadlines by collecting solar energy. However, solar energy collection is far less efficient than current wireless charging technologies. Hu et al. [12] considered wireless power transfer (WPT) between access points (APs) and UAVs in mobile edge computing (MEC) networks, using laser and radio frequency (RF) technologies. However, their solution suffers from low charging efficiency when UAVs are far from APs, making it unsuitable for our problem.

## III. SYSTEM MODEL

Suppose there are N devices on the ground denoted as a set $\mathcal { U } = \{ u _ { 1 } , u _ { 2 } , . . . , u _ { N } \}$ , where the ith device is located at coordi-=nate $\boldsymbol { u } _ { i } = ( x _ { i } , y _ { i } , 0 )$ . We assume that each device transmits data = ( 0)to the UAV with equal data volume D and transmission power $P _ { t r a n s } .$ All devices are served by a single UAV flying at a fixed height H starting from base station s0.

Given that the positions of all devices are known, the target area is partitioned into grids with grid cell length l with $l < < 2 r$ 2where r represents the UAVâs data transmission range projected on the ground. Clusters are formed based on the proximity principle, grouping devices according to their distance from the central point. The data collection points for the UAV are designated as the grid centers containing devices within the clusters. We denote $\mathcal { S P } = \{ s _ { 1 } , s _ { 2 } , . . . , s _ { M } \}$ as the grid centers =at a fixed height H with coordinate $\boldsymbol { s } _ { j } = ( x _ { j } , y _ { j } , H )$ where the UAV collects data.

Due to the substantial workload of the UAV, there have been deployed K wireless charging stations denoted as $\mathcal { C S } = \{ s _ { M + 1 } ^ { \prime } , s _ { M + 2 } ^ { \prime } , \ldots , s _ { M + K } ^ { \prime } \}$ , with coordinates $s _ { k } ^ { \prime } =$ $\left( { { x } _ { k } } , { { y } _ { k } } , { { H } _ { c s } } \right)$ with fixed height $H _ { c s }$ to replenish the $\mathrm { U A V } _ { \mathrm { \Delta } }$ ( )energy. The charging positions of these stations are represented by the set $\mathcal { C P } = \left\{ s _ { M + 1 } , s _ { M + 2 } , \ldots , s _ { M + K } \right\}$ , with coordinate $s _ { k } = ( x _ { k } , y _ { k } , H )$ . Clearly, the base station $s _ { 0 } ,$ , serving positions ${ \mathcal { S P } } .$ = ( ), and the wireless charging positions $\mathcal { C P }$ together constitute the entire hovering positions $\mathcal { H P }$ of the UAV.

<!-- image-->  
Fig. 1. Scenario.

Additionally, the real-world scenario contains obstacles such as tall buildings or trees. We use circumscribed cylinders to represent these obstacles, since cylindrical projections align with typical urban structures (e.g., towers, chimneys), as well as it is a good trade-off between realism and computational tractability in complex environments. These cylinders are denoted as $\mathcal { O } = \{ b _ { 1 } , b _ { 2 } , \ldots , b _ { Q } \}$ , with $r _ { q }$ representing the radius of the =circumscribed cylinder of obstacle $b _ { q } .$ And we configure the cylindrical shell such that twice its radius $( \mathrm { i . e . } ,$ , the diameter) always conservatively exceeds the maximum lateral dimension of the original obstacle, ensuring full encapsulation with a safety margin. Without ambiguity and for concise representation, we also use tuple $\langle b _ { q } , r _ { q } \rangle$ to represent the qth obstacle. Note that if some obstacles are too close, i.e., the circumscribed cylinders of these obstacles intersect or tangent, they are regarded as one obstacle in our model. Moreover, we only consider feasible hovering positions, i.e., positions not inside any circumscribed cylinders of the obstacles. Note that we will discuss the case of non-cylindrical approximate obstacles in Section VII.

The specific problem we address is to plan an obstacleavoidance trajectory for the UAV that starts from the initial base station $s _ { 0 } ,$ collects data from all devices in the areaâ visiting all serving points $s _ { 1 }$ through $s _ { M ^ { \ast } }$ âand then returns to the starting point. During this process, the UAV must maintain a sufficient battery level while balancing the total time spent and the number of selected charging stations.

We present a specific example with the scenario illustrated in Fig. 1. In the target area, there are $K = 2$ charging stations, $N = 1 6$ devices, $Q = 7$ = 2obstacles as well as one base station = 16 = 7and one UAV. We partition all devices into hovering positions at a constant height H based on the UAVâs communication radius r (projected on the ground) and set one hovering point for each charging station, resulting in M  hovering locations, labeled $s _ { 0 }$ through $s _ { 7 }$ = 8. The two charging stations are labeled $s _ { 6 } ^ { \prime }$ through $s _ { 7 } ^ { \prime }$ . In the figure, the trajectory passes through charging station $s _ { 6 } ^ { \prime } .$ , while charging station $s _ { 7 } ^ { \prime }$ is not selected.

## A. Wireless Data Collection Model

Due to the high flexibility of UAVs and their flight altitude, the likelihood of obstructions in ground-to-air communications is significantly reduced. We assume that the wireless communication channel between the UAV and ground devices in the service area is dominated by Line-of-Sight (LoS) links [1]. Therefore, the channel power gain from the UAV to each device is modeled as free-space trajectory loss. Given the UAVâs data transmission position coordinate $s _ { j }$ and the coordinates of the devices within its transmission range $u _ { i } ,$ , the channel power gain $g _ { i , j }$ from the UAV to each device is given by (1).

$$
g _ { i , j } = \frac { g _ { 0 } } { ( x _ { j } - x _ { i } ) ^ { 2 } + ( y _ { j } - y _ { i } ) ^ { 2 } + H ^ { 2 } } ,\tag{1}
$$

where $g _ { 0 }$ is the channel power gain at a reference distance of 1 m, and $U _ { s } ( s _ { j } )$ denotes the set of coordinates of all devices $u _ { i }$ ( )within the data transmission region of $s _ { j }$ . Given the transmission power $P _ { t r a n s }$ of the devices, the signal-to-noise ratio $( \mathrm { S N R } ) \gamma _ { i , j }$ for ground device i can be described as follows.

$$
\gamma _ { i , j } = \frac { P _ { t r a n s } g _ { i , j } } { \sigma ^ { 2 } } ,\tag{2}
$$

where $\sigma ^ { 2 }$ is the noise power for each ground device. If the SNR of device i is not less than the threshold $\gamma _ { t h }$ , then ground device i is considered to be covered by the UAV.

Therefore, we can determine the UAVâs wireless coverage range $r ,$ i.e., the maximum ground range that meets the threshold SNR $\gamma _ { t h }$

$$
r = \sqrt { \frac { P _ { t r a n s } g _ { 0 } } { \gamma _ { t h } \sigma ^ { 2 } } - H ^ { 2 } } ,\tag{3}
$$

Given the coordinates of data transmission position $s _ { j }$ and all ground devices, we can define the set of devices $U _ { s } ( s _ { j } )$ within the service range of $s _ { j }$ as (4).

$$
\begin{array} { r } { U _ { s } ( s _ { j } ) = \{ u _ { i } | ( x _ { i } - x _ { j } ) ^ { 2 } + ( y _ { i } - y _ { j } ) ^ { 2 } \leq r ^ { 2 } \} . } \end{array}\tag{4}
$$

Meanwhile, we select OFDMA as the uplink spectrum access method, allocating independent subcarriers to each device. For each device within the region of $s _ { j }$ , the data transmission rate $c _ { i , j }$ can be expressed as follows.

$$
c _ { i , j } = \frac { W } { | U _ { s } ( s _ { j } ) | } \log _ { 2 } ( 1 + \gamma _ { i , j } ) \geq c .\tag{5}
$$

where $W$ is the bandwidth and c represents the minimum transmission rate of the devices.

## B. Energy Consumption Model of UAV

The total energy consumption of a UAV can be divided into two parts. The first part is the energy consumed for communication, including signal modulation, demodulation, and radiation.

The second part is the energy required for the UAV to overcome gravity and provide thrust, ensuring that it can hover and fly. It is important to note that the energy consumption for communication is significantly less than the energy required to overcome gravity and provide thrust.

First, according to [35], the propulsion power consumption $P _ { p r o p } ( v )$ of a rotary-wing UAV at a uniform height as a function ( )of speed v is given by (6).

$$
\begin{array} { l r } { \displaystyle { P _ { p r o p } ( v ) = P _ { b l a d e } \left( 1 + \frac { 3 v ^ { 2 } } { v _ { t i p } ^ { 2 } } \right) + P _ { I } \left( \sqrt { 1 + \frac { v ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { v ^ { 2 } } { 2 v _ { 0 } ^ { 4 } } \right) ^ { \frac { 1 } { 2 } } } } \\ { \displaystyle { ~ + \frac { 1 } { 2 } \zeta \rho R _ { s o l i d } R _ { a r e a } v ^ { 3 } } , } \end{array}
$$

where $P _ { b l a d e }$ and $P _ { I }$ represent the blade profile power and the induced power in hover, respectively; $v _ { t i p } , v _ { 0 } , \zeta$ and Ï denote the tip speed of the rotor, the mean rotor induced velocity in hover, the fuselage drag ratio, and the air density, respectively; $R _ { s o l i d }$ and $R _ { a r e a }$ represent the rotor solidity and the area of the rotor disk, respectively.

In our model, the UAV operates in two states: hovering and flying. Based on the UAV propulsion power as a function of speed, the energy consumption for the UAV hovering at each data collection position in $\scriptstyle { S ^ { p } }$ can be calculated by (7).

$$
E _ { h } ^ { s p } = P _ { p r o p } ( 0 ) \cdot t _ { h } ^ { s p } + P _ { \mathrm { r x } } \cdot t _ { h } ^ { s p } = ( P _ { b l a d e } + P _ { I } + P _ { \mathrm { r x } } ) \frac { D } { c } ,\tag{7}
$$

where $P _ { \mathrm { r x } }$ is the data reception power of the UAV, and $t _ { h } ^ { s p }$ is the hovering time at each location in $\scriptstyle { S ^ { p } }$ , and we assume that it is determined by the device with the longest transmission time, i.e., transmitting at the slowest speed, which can be expressed as $\begin{array} { r } { t _ { h } ^ { s p } = \frac { D } { c } } \end{array}$ (where D is the equal data volume of each ground =device).

Since the calculation of charging time is related to the energy consumption during hovering while charging, and the amount of energy consumed during hovering is in turn determined by the charging time, these two variables are highly correlated. In order to make full use of the energy of the UAV, we have standardized the charging time for the drone at each charging station to the maximum charging time $t _ { \mathrm { m a x } } ^ { h a r v }$ . And the energy consumption of UAV at each location in $\mathcal { C P }$ can be calculated by (8).

$$
E _ { h } ^ { c p } = P _ { p r o p } ( 0 ) \cdot t _ { \mathrm { m a x } } ^ { h a r v } = ( P _ { b l a d e } + P _ { I } ) \frac { B _ { \mathrm { m a x } } } { P _ { h a r v } } .\tag{8}
$$

Without loss of generality, we consider the UAVâs change in speed during takeoff and landing. Assuming the UAVâs acceleration (or deceleration) is $^ { a , }$ the flight energy consumption $E _ { f } ^ { i , j }$ between any two hovering positions $s _ { i }$ and $s _ { j }$ is shown in $( 9 )$

$$
\begin{array} { l } { E _ { f } ^ { i , j } = \int _ { 0 } ^ { v / a } P _ { p r o p } ( a t ) d t + P _ { p r o p } ( v ) \cdot t _ { f } ^ { i , j } } \\ { \displaystyle + \int _ { 0 } ^ { v / a } P _ { p r o p } ( v - a t ) d t , } \end{array}\tag{9}
$$

where $t _ { f } ^ { i , j }$ is the constant speed flight time. We assume the constant flight speed of the UAV is v. Therefore, the constant

speed flight time between $s _ { i }$ and $s _ { j }$ can be expressed as $\textstyle { \frac { a \cdot d _ { i j } - v ^ { 2 } } { a v } }$ Here, $d _ { i j }$ represents the distance between position $s _ { i }$ and $s _ { j }$

## C. Wireless Charging Model

Currently, various wireless charging technologies exist, such as RF (radio frequency) charging and laser charging. Given the capability of laser to achieve long-distance and high-power transmission, we know that the charging station is at a fixed height $H _ { c s }$ , and is equipped with a laser transmitter that transmits laser energy to the UAV at a constant power $P _ { 0 } ,$ with power transmission occurring only when the UAV is directly above the charging station. The harvested laser charging power $P _ { h a r v }$ can be expressed as:

$$
P _ { h a r v } = \frac { \eta A _ { r e c } \vartheta P _ { 0 } e ^ { - \kappa _ { t t } ( H - H _ { c s } ) } } { ( A _ { e m i t } + \beta ( H - H _ { c s } ) ) ^ { 2 } } ,\tag{10}
$$

where $\eta$ is the UAVâs energy conversion efficiency, $A _ { r e c }$ is the area of the laser receiver lens, Ï is the combined transmission and receiver optical efficiency, $A _ { e m i t }$ is the initial laser beam size, $\kappa _ { t t }$ is the atmospheric attenuation coefficient, Î² is the beam divergence angle [10], [36], [37]. Thus, the total energy $\widehat { E _ { u } }$ harvested by the UAV during the charging time $t _ { \mathrm { m a x } } ^ { h a r v }$ can be calculated as (11).

$$
\widehat { E _ { u } } = P _ { h a r v } t _ { \operatorname* { m a x } } ^ { h a r v } .\tag{11}
$$

## IV. PROBLEM FORMULATION

First, we define a weighted directed complete graph G, where the vertices in the graph represent all potential locations in the UAV trajectory, and each edge represents the direct flight path between each pair of vertices, with the edge weight representing the flight distance. We define a binary variable $x _ { i j } = 1$ to indicate that the edge between vertices $s _ { i }$ and $s _ { j }$ = 1is part of the trajectory; $x _ { i j } = 0 _ { : }$ , otherwise. Let $\boldsymbol { \mathcal { S } }$ be an already computed = 0complete and ordered set of path vertices. The total distance of the trajectory with vertices in S can be expressed as follows.

$$
\mathcal { L } ( S ) = \sum _ { i = 0 } ^ { M + K } \sum _ { j = 0 , j \neq i } ^ { M + K } w ( i , j ) \cdot x _ { i j } ,\tag{12}
$$

where $w ( i , j )$ is the weight (i.e., total distance) of the edge ( )between vertices $s _ { i }$ and $s _ { j } ,$ , which can be expressed as $w ( i , j ) =$ $d _ { i j }$ . And the total time cost of the set $\boldsymbol { s }$ ( ) =can be expressed as follows.

$$
\begin{array} { r l } { \displaystyle T ( \mathcal { S } ) = \sum _ { i = 1 } ^ { M } t _ { h } ^ { s p } + \sum _ { i = 0 } ^ { M + K } \sum _ { j = M + 1 , j \neq i } ^ { M + K } x _ { i j } \cdot t _ { \operatorname* { m a x } } ^ { h a r v } } & { } \\ { \displaystyle + \sum _ { i = 0 } ^ { M + K } \sum _ { j = 0 , j \neq i } ^ { M + K } \left( \frac { v } { a } + \frac { w ( i , j ) } { v } \right) \cdot x _ { i j } , } & { } \end{array}\tag{13}
$$

where $\begin{array} { r } { \big ( \frac { v } { a } + \frac { w ( i , j ) } { v } \big ) } \end{array}$ is the flight time of the UAV between vertices $s _ { i }$ and $s _ { j }$

Next, we define $B _ { i }$ as the remaining energy of the UAV when it leaves the hovering position $s _ { i }$ . Assume that the UAV flies to

$s _ { j }$ in the next step. $B _ { j }$ can be calculated as (14) shows.

$$
B _ { j } = \left\{ \begin{array} { l l } { B _ { i } - E _ { f } ^ { i j } - E _ { h } ^ { s p } , \quad \quad 1 \leq j \leq M \quad \mathrm { a n d } \ x _ { i j } = 1 , } \\ { B _ { \operatorname* { m a x } } , \quad M + 1 \leq j \leq M + K \quad \mathrm { a n d } \ x _ { i j } = 1 . } \end{array} \right.\tag{14}
$$

We assume that the UAV starts with a full battery capacity and that the remaining energy of the UAV is non-negative when it leaves each data collection location. Specifically, $B _ { 0 } = B _ { \operatorname* { m a x } }$ and $B _ { i } > 0$ for $1 \leq i \leq M$

0 1Then, we require the UAV to move toward charging stations to replenish energy, so we set a reward for reaching each charging station as shown in (15).

$$
R e w a r d ( \boldsymbol { S } ) = \sum _ { i = 0 } ^ { M + K } \sum _ { j = M + 1 , j \neq i } ^ { M + K } x _ { i j } \cdot \tau ,\tag{15}
$$

where $\tau$ is a constant representing the reward for reaching each charging station. Our objective is to optimize the UAV trajectory, that is, which charging stations to visit should be carefully planned, thus balancing the total travel time and the number of selected charging stations. We introduce a weight Î» to jointly optimize these two variables and define the objective function f as (16) shows.

$$
f ( S ) = R e w a r d ( S ) - \lambda \cdot T ( S ) , \lambda > 0 .\tag{16}
$$

We assume that each charging station can be visited at most once. The Practical Optimizing UAV Trajectory in Wireless Charging Networks (POTWCN) problem can be formalized as problem P1.

P1  f S

$$
\mathrm { s . t . } \quad B _ { 0 } = B _ { \mathrm { m a x } } ,\tag{17}
$$

$$
B _ { i } > 0 , 1 \leq i \leq M ,\tag{18}
$$

$$
M + 1 \leq | \cal { S } | \leq M + K + 1 ,\tag{19}
$$

(20)

$$
\sum _ { j = 1 , j \neq i } ^ { M + K } x _ { i j } = \sum _ { j = 1 , j \neq i } ^ { M + K } x _ { j i } = 1 , 0 \leq i \leq M ,\tag{21}
$$

$$
\sum _ { j = 1 , j \neq i } ^ { M + K } x _ { i j } = \sum _ { j = 1 , j \neq i } ^ { M + K } x _ { j i } , 0 \leq i \leq M + K ,\tag{22}
$$

$$
x _ { i i } = 0 , x _ { i j } \in \{ 0 , 1 \} , 0 \leq i , j \leq M + K , i \neq j .\tag{23}
$$

In these constraints, (18) and (19) ensure the energy limitations, (20) limits the maximum number of charging stations that can be added, (21)-(22) enforce the trajectory selection constraints, and (22) specifies the binary nature of the decision variables.

Next, we have the following theorem to indicate the hardness of the problem POTWCN.

Theorem IV.1: The POTWCN problem is NP-hard.

Proof: To prove that the POTWCN problem is NP-hard, we reduce the Subset TSP problem [38], which is a known NP-hard problem, to the problem POTWCN. The Subset TSP problem is defined as follows: given a weighted graph, find the shortest tour that visits every vertex in a specified subset $s \subseteq \tau$ at least once, where vertices not in $S \ ( \mathrm { i . e . , } \ T - S )$ may or may not be included in the tour to achieving our goal. To reduce Subset TSP to POTWCN, we first convert the input of the Subset TSP problem into the input of the POTWCN problem, which includes the graph G and the vertex subset S, with edge weights representing negative benefits. In this conversion, the vertices in S are treated as device locations, and the remaining vertices $\mathcal { T } - \mathcal { S }$ are considered as optional charging stations. We examine a special case of the POTWCN problem where the UAVâs initial energy is sufficient to cover the entire Subset TSP tour without requiring any recharging. In this case, the solution to the POTWCN problem can be directly translated into a solution for the Subset TSP problem. This reduction demonstrates that solving the POTWCN problem is at least as hard as solving the Subset TSP problem, thereby proving that the POTWCN problem is NP-hard. -

## V. SOLUTION

## A. Algorithm Design

1) Obstacle-Aware Weighted Graph Generation Algorithm (OWGGA): First, we propose an algorithm that constructs a weighted complete graph G with vertices set HP, where the edge weights account for potential obstacles between vertices, as shown in Algorithm 1.

The algorithm iterates through all vertex pairs $s _ { i }$ and $s _ { j }$ in the hyperplane HP (line 1) and computes the actual flight distance between them. It first checks the case where no obstacles exist between the two points (line 3).

When an intersection between the line segment $s _ { i } s _ { j }$ and obstacles in set O is detected, the algorithm identifies the intersecting obstacles set O and calculates the intersection points $s _ { i j , 1 } ^ { p } , \ldots , s _ { i j , Q _ { i j } - 1 } ^ { p }$ on the cylindrically projected circles of the obstacles. These points are closer to $s _ { j }$ on each circle, excluding the circle nearest to $s _ { j }$ . The initial intersection point is set as the starting point of the segment (lines 5-7).

For each traversed obstacle $b _ { q _ { k } }$ , the algorithm computes the tangent points $s _ { i j , k , 1 }$ and $s _ { i j , k , 2 }$ on obstacle $b _ { q _ { k } }$ , corresponding to the previous intersection point $s _ { i j , k - 1 } ^ { p }$ and the current intersection point $s _ { i j , k } ^ { p }$ , respectively (line 9). It then calculates the straight-line distances $L _ { s _ { i j , k - 1 } ^ { p } , s _ { i j , k , 1 } } , L _ { s _ { i j , k } ^ { p } , s _ { i j , k , 2 } }$ , and the arc length $L _ { \overline { { { s _ { i j , k , 1 } s _ { i j , k , 2 } } } } }$ between the tangent points (lines 10-12). Finally, the algorithm sums these three values to obtain the total detour distance, which is returned as the edge weight between vertices $s _ { i }$ and $s _ { j }$ in graph G, representing the final flight distance (line 13).

This computation considers obstacles along the path, ensuring that the edge weights accurately reflect the potential detour the UAV might need to take in the environment.

2) Adaptive Charging Station Algorithm (ACSA): Then, we propose a greedy-based approximation algorithm that achieves a near-optimal solution for maximizing the objective function by limiting the number of charging stations along the route. We select one charging point with the maximum incrementation of the objective function f S in each iteration. The pseudocode ( )of our proposed algorithm is presented in Algorithm 2.

Algorithm 1: Obstacle-Aware Weighted Graph Generation   
Algorithm (OWGGA).   
Input : Hovering positions   
${ \mathcal { H P } } = \{ s _ { 0 } , s _ { 1 } , . . . , s _ { M } , s _ { M + 1 } , . . . , s _ { M + K } \} ,$   
obstacles set $\mathcal { O } = \{ b _ { 1 } , . . . , b _ { Q } \}$ ,and obstacle   
circumscribed cylinder radius set   
$\mathcal { R } = \{ r _ { 1 } , . . . , r _ { Q } \} .$   
Output: Weighted complete graph   
$G = ( \mathcal { H P } , \mathcal { H P } \times \mathcal { H P } )$ with edge weight   
matrix w.   
1 foreach pair of vertices $s _ { i }$ and $s _ { j }$ in $\mathcal { H P }$ do   
2 if $s _ { i } s _ { j }$ does not intersect any obstacle in O then   
3 $w ( i , j ) = w ( j , i ) = \sqrt { ( x _ { j } - x _ { i } ) ^ { 2 } + ( y _ { j } - y _ { i } ) ^ { 2 } } ;$   
4 else   
5 Find the obstacles   
$\mathcal { O } _ { i j } = \{ \langle b _ { q _ { 1 } } , r _ { q _ { 1 } } \rangle , . . . , \langle b _ { q _ { Q _ { i j } } } , r _ { q _ { Q _ { i j } } } \rangle \}$ that $s _ { i } s _ { j }$   
intersects;   
6 Compute intersection points of line $s _ { i } s _ { j }$ and   
the obstacles in ${ \mathcal { O } } ,$ and reserve the points   
nearer to $s _ { j }$ on each circle except the circle   
nearest to $s _ { j }$ as $s _ { i j , 1 } ^ { p } , . . . , s _ { i j , Q _ { i j } - 1 } ^ { p } ;$   
7 Set $s _ { i j , 0 } ^ { p } = s _ { i }$ and $s _ { i j , Q _ { i j } } ^ { p } = s _ { j } ;$   
8 for $k = 1$ to $Q _ { i j }$ do   
9 Compute tangent points $s _ { i j , k , 1 }$ and $s _ { i j , k , 2 }$   
on the circle of $( b _ { q _ { k } } , r _ { q _ { k } } )$ for $s _ { i j , k - 1 } ^ { p }$ and   
$s _ { i j , k } ^ { p } ;$   
10 $L _ { s _ { i j , k - 1 } ^ { p } , s _ { i j , k , 1 } } =$   
$\sqrt { ( x _ { s _ { i j , k - 1 } ^ { p } } - x _ { s _ { i j , k , 1 } } ) ^ { 2 } + ( y _ { s _ { i j , k - 1 } ^ { p } } - y _ { s _ { i j , k , 1 } } ) ^ { 2 } } ;$   
11 $L _ { s _ { i j , k } ^ { p } , s _ { i j , k , 2 } }$   
$\sqrt { ( x _ { s _ { i j , k } ^ { p } } - x _ { s _ { i j , k , 2 } } ) ^ { 2 } + ( y _ { s _ { i j , k } ^ { p } } - y _ { s _ { i j , k , 2 } } ) ^ { 2 } } ;$   
12 $\begin{array} { r } { L _ { \widehat { \^ { s _ { i j , k , 1 } s _ { i j , k , 2 } } } } = { r _ { q _ { k } } \cdot \angle s _ { i j , k - 1 } ^ { p } } b _ { { q _ { k } } } s _ { i j , k } ^ { p } ; } \end{array}$   
13 $w ( i , j ) = w ( j , i ) =$   
$\begin{array} { r } { \sum _ { k = 1 } ^ { Q _ { i j } } \biggl ( L _ { s _ { i j , k - 1 } ^ { p } , s _ { i j , k , 1 } } + L _ { \widehat { s _ { i j , k , 1 } s _ { i j , k , 2 } } } + L _ { s _ { i j , k } ^ { p } , s _ { i j , k , 2 } } \biggr ) ; } \end{array}$   
14 return G and w;

First, the algorithm ACSA initializes the number of selected charging positions k, the set S to record the indices of vertices currently on the trajectory and ${ \mathcal { C P } } ^ { \prime }$ to record the candidate indices of all charging positions (line 1). Then, ASCA iteratively increases the number of charging stations in the set $\boldsymbol { s }$ until it exceeds the maximum number K. Within the loop, we select the charging position $s _ { i ^ { * } }$ that provides the maximum increment of the objective function, add it to ${ \mathcal { S } } ,$ , and remove it from $\mathcal { C P ^ { \prime } }$ (lines 7-9). Next, we check if the energy constraints are met under the current number of charging stations, ensuring the UAV does not run out of battery during its flight. If the constraints are satisfied, the algorithm exits the loop; otherwise, it increases the number of allowed charging positions k and proceeds to the next iteration. Finally, the algorithm returns the final trajectory.

Algorithm 2: Adaptive Charging Station Algorithm   
(ACSA).   
Input :Base station $s _ { 0 } ,$ ï¼serving positions set   
$\begin{array} { r } { { \cal S } ^ { \mathcal { P } } = \{ s _ { 1 } , . . . , s _ { M } \} } \end{array}$ ,charging positions set   
$\mathcal { C P } = \{ s _ { M + 1 } , . . . s _ { M + K } \}$   
Output: Path vertices pair set $\mathcal { P } .$   
1 Initialize $k = 0 , S = S \mathcal { P } \cup \{ s _ { 0 } \}$ ,and $\begin{array} { r } { { \mathcal { C P } } ^ { \prime } = { \mathcal { C P } } ; } \end{array}$   
2 Calculate the edge weight matrix w by Alg. 1.   
3 repeat   
4 if $k = = 0$ then   
5 Calculate the trajectory $\mathcal { P }$ on graph   
$G = ( S , S \times S )$ with weight w by   
Christofides algorithm [15];   
6 else   
7 $\begin{array} { r } { s _ { i ^ { * } } = \arg \operatorname* { m a x } _ { s _ { i } \in \mathcal { C P } ^ { \prime } } \{ f ( S \cup \{ s _ { i } \} ) - f ( S ) \} ; } \end{array}$   
$/ / \mathrm { ~  ~ { ~ \ b ~ } ~ } f ( \cdot ) \mathrm { ~  ~ { ~ i ~ s ~ } ~ }$ calculated based on   
the $\mathtt { t r a j }$ ectory $\mathcal { P }$ generated by   
Christofides algorithm [15];   
8 $S = S \cup \{ s _ { i ^ { * } } \} ;$   
9 $\mathcal C \mathcal P ^ { \prime } = \mathcal C \hat { \mathcal P ^ { \prime } } \backslash \{ \dot { s } _ { i ^ { * } } \} ;$   
10 é $\forall ( s _ { j _ { 1 } } , s _ { j _ { 2 } } ) \in \mathcal { P } : B _ { j _ { 2 } } > 0$ then   
11 break;   
12 $k = k + 1 ;$   
13until $k > K ;$   
14 return S, P;

## B. Theoretical Analysis

In this section, we will give the theoretical analysis of the proposed algorithm, including the approximation ratio of the path length and the objective, as well as the time complexity.

1) Path Length Analysis: In this subsection, we will derive the approximation ratio of the detour path length of the proposed algorithm ASCA (Algorithm 2). We first give the following lemma.

Lemma V.1: Given any $( s _ { i } , s _ { j } ) \in \mathcal { P }$ , where P is the path ( )vertices pair set, the approximation ratio is given by:

$$
1 \leq \frac { w ( i , j ) } { d _ { i j } ^ { * } } \leq \frac { \pi } { 2 } .\tag{24}
$$

where $w ( i , j )$ the length of the detour path between $s _ { i }$ and $s _ { j }$ ( )calculated in Algorithm 1, and $d _ { i j } ^ { * }$ is the minimum detour path length between $s _ { i }$ and $s _ { j } .$

Proof: Let $d _ { i j }$ denote the length of the straight line segment $s _ { i } s _ { j }$ . It is obvious that $w ( i , j ) \geq d _ { i j } ^ { * } \geq d _ { i j } . w ( i , j ) = d _ { i j } ^ { * } = d _ { i j }$ ( )if and only if there is no obstacle between $s _ { i }$ ( )and $s _ { j }$ =. Thus, we have:

$$
1 \leq \frac { w ( i , j ) } { d _ { i j } ^ { * } } \leq \frac { w ( i , j ) } { d _ { i j } } .\tag{25}
$$

For the latter inequality in (24), we first consider that only one obstacle lies between $s _ { i }$ and $s _ { j }$ . As shown in Fig. 2, we use the top view to describe. Suppose that the obstacle $\langle b _ { q } , r _ { q } \rangle$ lies between $s _ { i }$ and $s _ { j }$ where $( s _ { i } , s _ { j } ) \in \mathcal { P }$ , that is, the distance between the point $b _ { q }$ (and the line $s _ { i } s _ { j }$ is no large than the radius $r _ { q } .$ . Draw the tangent lines to circle $b _ { q }$ from $s _ { i }$ and $s _ { j }$ with the direction that $\angle s _ { i } b _ { q } s _ { j } \le \pi$ , and we denote the tangent points as $s _ { i j , 1 }$ and $s _ { i j , 2 }$ , respectively. Thus, the whole detour is $( s _ { i } s _ { i j , 1 } +$ $\widehat { s _ { i j , 1 } s _ { i j , 2 } } + s _ { i j , 2 } s _ { j } )$ . Draw the perpendicular line from $b _ { q }$ to $s _ { i } s _ { j }$ + )and we denote the perpendicular point as $b _ { q , i j }$

<!-- image-->  
Fig. 2. Detour with one obstacle.

Here, we denote the euclidean distance $d _ { i j }$ of $s _ { i } s _ { j }$ as d to simplify. Let $d _ { 1 }$ be the distance from $b _ { q }$ to the line $s _ { i } s _ { j }$ , that is, the length of $b _ { q } b _ { q , i j }$ is $d _ { 1 }$ . Let $d _ { 2 }$ be the length of $s _ { i } b _ { q , i j }$ so the length of $s _ { j } b _ { q , i j }$ is $d - d _ { 2 }$ . Since $s _ { i }$ and $s _ { j }$ are available hovering positions, they must not be inside the obstacle circle. $\mathrm { S o } .$ , we have the constraints:

$$
\begin{array} { r } { \left( 0 \leq d _ { 1 } \leq r _ { q } , \right. } \end{array}\tag{26}
$$

$$
\begin{array} { r } { \left\{ d _ { 2 } \geq \sqrt { r _ { q } ^ { 2 } - d _ { 1 } ^ { 2 } } , \right. } \end{array}\tag{27}
$$

$$
\begin{array} { r } { \left\lfloor d - d _ { 2 } \geq \sqrt { r _ { q } ^ { 2 } - d _ { 1 } ^ { 2 } } . \right. } \end{array}\tag{28}
$$

We write the detour length w i, j as a function of $d _ { 1 }$ and $d _ { 2 }$ which is $L ( d _ { 1 } , d _ { 2 } )$ ( )as shown in (29).

$$
\begin{array} { r l r } {  { L ( d _ { 1 } , d _ { 2 } ) = \sqrt { d _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } + \sqrt { d _ { 1 } ^ { 2 } + ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } } \\ & { } & { \quad + r _ { q } ( \operatorname { a r c c o s } \frac { d _ { 1 } } { \sqrt { d _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } } + \operatorname { a r c c o s } \frac { d _ { 1 } } { \sqrt { d _ { 1 } ^ { 2 } + ( d - d _ { 2 } ) ^ { 2 } } }  } \\ & { } & { \quad  - \operatorname { a r c c o s } \frac { r _ { q } } { \sqrt { d _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } } - \operatorname { a r c c o s } \frac { r _ { q } } { \sqrt { d _ { 1 } ^ { 2 } + ( d - d _ { 2 } ) ^ { 2 } } } ) . } \end{array}\tag{29}
$$

In the following, we will prove the approximation ratio by two steps:

1) Fixing the length of $s _ { i } s _ { j }$ , i.e., d, find the case, i.e., the value of $d _ { 1 }$ and $d _ { 2 }$ , that $L ( d _ { 1 } , d _ { 2 } )$ is maximized. Suppose in this case, $d _ { 1 } = d _ { 1 } ^ { * }$ and $d _ { 2 } = d _ { 2 } ^ { * }$

=2) With the maximum value $L ( d _ { 1 } ^ { * } , d _ { 2 } ^ { * } )$ , find the maximum ratio of $L ( d _ { 1 } ^ { * } , d _ { 2 } ^ { * } ) / d \triangleq f _ { \gamma } ( d )$ ( ), that is, changing d to get the maximum ratio. Thus, we obtain the maximum value of $w ( i , j ) / d _ { i j }$

( )For the first step, we first fix $d _ { 2 } .$ , then calculate the distance from $b _ { q }$ to line $s _ { i } s _ { j }$ , i.e., the value of $d _ { 1 }$ , that maximizes $L ( d _ { 1 } , d _ { 2 } )$ . Note that all the derivatives in the following are ( )defined on the open interval for $d _ { 1 }$ and $d _ { 2 }$ to avoid zero values in the denominator.

$$
\begin{array} { r l } { \frac { \partial L ( A _ { 1 } , B _ { 2 } ) } { \partial A _ { 1 } } = } & { - \frac { \partial A _ { 1 } } { \partial A _ { 1 } } } \\ & { - \nu \Bigg ( \frac { \partial _ { 2 } } { \partial A _ { 1 } } + \frac { \partial _ { 2 } } { \partial x _ { 2 } } - c _ { \mathrm { a } } ^ { 2 } + \frac { \partial _ { 1 } } { \sqrt { u _ { 1 } ^ { 2 } + ( \partial ^ { 2 } - c _ { \mathrm { a } } ^ { 2 } ) ^ { 2 } } } - c _ { \mathrm { a } } ^ { 2 } } \\ & { - \nu \Bigg ( \frac { \partial _ { 2 } } { \partial x _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } + \frac { \partial _ { 2 } } { \partial x _ { 2 } ^ { 2 } + ( \partial ^ { 2 } - c _ { \mathrm { a } } ^ { 2 } ) ^ { 2 } } } \\ & { + \frac { \partial _ { 1 } } { ( \partial _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } ) ^ { 2 } } \nu \frac { \partial _ { 1 } } { \sqrt { u _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } } } \\ & { - \frac { \nu \partial _ { 1 } } { ( \partial ^ { 2 } + ( \partial ^ { 2 } - c _ { \mathrm { a } } ^ { 2 } ) ^ { 2 } ) \sqrt { u _ { 1 } ^ { 2 } + ( \partial ^ { 2 } - c _ { \mathrm { a } } ^ { 2 } ) ^ { 2 } } - c _ { \mathrm { a } } ^ { 2 } } \Bigg ) } \\ & { = \frac { \partial _ { 1 } \sqrt { u _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } - c _ { \mathrm { a } } ^ { 2 } u _ { 2 } } { \partial A _ { 1 } ^ { 2 } + d _ { 2 } ^ { 2 } } } \\ &  + \frac  \partial _ { 1 } \sqrt { u _ { 1 } ^ { 2 } + ( \partial ^ { 2 } - c _ { \mathrm { a } } ^ { 2 } ) ^ { 2 } } - c _ { \mathrm { a } } ^ { 2 } - c _  \end{array}\tag{30}
$$

Let $\begin{array} { r } { \frac { \partial L } { \partial d _ { 1 } } = 0 } \end{array}$ , we only get $d _ { 1 } = r _ { q }$ when $d _ { 1 } \in [ 0 , r _ { q } ]$ . When $d _ { 1 } =$ $\begin{array} { r } { 0 , \frac { \partial L } { \partial d _ { 1 } } = - r _ { q } ( 1 / d _ { 2 } + 1 / ( d - d _ { 2 } ) ) < 0 } \end{array}$ , that is, $\begin{array} { r } { \frac { \partial L } { \partial d _ { 1 } } \leq 0 } \end{array}$ when $d _ { 1 } \in [ 0 , r _ { q } ]$ (1. Thus, $L ( d _ { 1 } , d _ { 2 } )$ )) 0 0is a monotone decreasing function when $d _ { 2 }$ ] ( )is fixed and the maximum is obtained when $d _ { 1 } = 0$ i.e., the line $s _ { i } s _ { j }$ crosses the circle center.

Next, we calculate the value of $d _ { 2 }$ that maximizes $L ( 0 , d _ { 2 } )$

$$
\begin{array} { l } { { { \cal { L } } ( 0 , d _ { 2 } ) = \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } + \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } } \\ { { \phantom { \frac { 1 } { 2 } } + r _ { q } \left( \pi - \operatorname { a r c c o s } \frac { r _ { q } } { d _ { 2 } } - \operatorname { a r c c o s } \frac { r _ { q } } { d - d _ { 2 } } \right) . } } \end{array}\tag{31}
$$

Similarly, we also calculate the partial derivative.

$$
\begin{array} { c } { { \frac { \partial L ( 0 , d _ { 2 } ) } { \partial d _ { 2 } } = \displaystyle \frac { d _ { 2 } } { \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } } - \frac { d - d _ { 2 } } { \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } } } \\ { { - \frac { r _ { q } ^ { 2 } / d _ { 2 } ^ { 2 } } { \sqrt { 1 - ( r _ { q } / d _ { 2 } ) ^ { 2 } } } + \frac { r _ { q } ^ { 2 } / ( d - d _ { 2 } ) ^ { 2 } } { \sqrt { 1 - ( r _ { q } / ( d - d _ { 2 } ) ) ^ { 2 } } } } } \\ { { = \frac { \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } } { d _ { 2 } } - \frac { \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } { d - d _ { 2 } } . } } \end{array}\tag{2}
$$

Let $\begin{array} { r } { \frac { \partial L ( 0 , d _ { 2 } ) } { \partial d _ { 2 } } = 0 , } \end{array}$ , we get $d _ { 2 } = d / 2$ . To further check the mono-= 0tonicity of the function $f ( 0 , d _ { 2 } )$ 2, we calculate the second partial derivative.

$$
\frac { \partial ^ { 2 } L ( 0 , d _ { 2 } ) } { \partial d _ { 2 } ^ { 2 } } = \frac { \frac { d _ { 2 } ^ { 2 } } { \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } } - \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } } { d _ { 2 } ^ { 2 } }
$$

$$
\begin{array} { r l } & { \quad - \frac { - \frac { ( d - d _ { 2 } ) ^ { 2 } } { \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } + \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } { ( d - d _ { 2 } ) ^ { 2 } } } \\ & { \quad = \frac { r _ { q } ^ { 2 } } { d _ { 2 } ^ { 2 } \sqrt { d _ { 2 } ^ { 2 } - r _ { q } ^ { 2 } } } + \frac { r _ { q } ^ { 2 } } { ( d - d _ { 2 } ) ^ { 2 } \sqrt { ( d - d _ { 2 } ) ^ { 2 } - r _ { q } ^ { 2 } } } > 0 . } \end{array}\tag{33}
$$

Thus, $L ( 0 , d _ { 2 } )$ is a convex function and has the minimum value when $d _ { 2 } = d / 2$ and $d _ { 2 } \in ( r _ { q } , d - r _ { q } )$ . The maximum value is:

$$
\begin{array} { l } { { { \cal L } ( 0 , r _ { q } ) = { \cal L } ( 0 , d - r _ { q } ) } } \\ { { ~ = ~ \sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } } + r _ { q } \left( \pi - \operatorname { a r c c o s } \displaystyle \frac { r _ { q } } { d - r _ { q } } \right) . } } \end{array}\tag{34}
$$

Subsequently, we have:

$$
\begin{array} { l } { \displaystyle \frac { w ( i , j ) } { d _ { i j } } = \frac { L ( d _ { 1 } , d _ { 2 } ) } { d } \leq \frac { L ( 0 , d _ { 2 } ) } { d } \leq \frac { L ( 0 , r _ { q } ) } { d } } \\ { \displaystyle = \frac { \sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } } + r _ { q } \left( \pi - \operatorname { a r c c o s } \frac { r _ { q } } { d - r _ { q } } \right) } { d } . } \end{array}\tag{35}
$$

For the second step, we denote $\begin{array} { r } { f _ { \gamma } ( d ) \triangleq \frac { L ( 0 , r _ { q } ) } { d } } \end{array}$ in (35) to explore the maximum value of this function. Due to the constraints of (27) and (28), we have d $l \geq 2 r _ { q }$ when $d _ { 1 } = 0$

$$
\begin{array} { r l } & { f _ { \tau } ^ { * } ( d ) = \frac { 1 } { d ^ { 2 } } } \\ & { ( d ( \frac { d - r _ { q } } { \sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } } } - \frac { r _ { q } ^ { 2 } } { ( d - r _ { q } ) ^ { 2 } \sqrt { 1 - ( r _ { q } / d - r _ { q } ) } } ) ^ { 2 } ) } \\ & { - \sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } } - r _ { q } ( \tau - \mathrm { a r c o s s } \frac { r _ { q } } { d - r _ { q } } ) ) , } \\ & { = \frac { r _ { q } } { d ^ { 2 } ( d - r _ { q } ) } ( \sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } } - ( d - r _ { q } )  } \\ & {  ( \tau - \mathrm { a r c o s s } \frac { r _ { q } } { d - r _ { q } } ) ) } \\ & { \leq - \frac { r _ { q } ( d - r _ { q } ) ( \tau - \mathrm { a r c o s s } \frac { r _ { q } } { d - r _ { q } } - 1 ) } { d ^ { 2 } ( d - r _ { q } ) } < 0 , } \end{array}
$$

The first inequality is because $\sqrt { ( d - r _ { q } ) ^ { 2 } - r _ { q } ^ { 2 } < d - r _ { q } }$ . The last inequality is because $0 < \dot { r } _ { q } / ( d - r _ { q } ) \le 1$ , so $1 < \pi / 2 <$ $\begin{array} { r } { ( \pi - \operatorname { a r c c o s } \frac { r _ { q } } { d - r _ { q } } ) \leq \pi } \end{array}$ 0 ( ) 1 that is, Ï â $\frac { r _ { q } } { d - r _ { q } } - 1 ) > 0$ Thus, $f _ { \gamma } ( d )$ is a monotone decreasing function when $d \geq 2 r _ { q }$ ( )and the maximum value is $\pi / 2$ when $d = 2 r _ { q }$ 2. Therefore, com-2bined with (25) and (35), we have:

$$
1 \leq \frac { w ( i , j ) } { d _ { i j } ^ { * } } \leq \frac { w ( i , j ) } { d _ { i j } } \leq f _ { \gamma } ( d ) \leq \frac { \pi } { 2 } .\tag{37}
$$

The conclusion is proved when there is only one obstacle lying between $s _ { i }$ and $s _ { j }$

<!-- image-->  
Fig. 3. Detour with several obstacles.

If there is more than one obstacle lying between $s _ { i }$ and $s _ { j }$ as shown in Fig. 3, we separate $s _ { i } s _ { j }$ into several segments with $s _ { i } s _ { i j , 1 } ^ { p } , . . . , s _ { i } s _ { i j , Q _ { i j } - 1 } ^ { p }$ where $Q _ { i j }$ is the number of obstacles lying between, and $s _ { i j , 1 } ^ { p } , \ldots , s _ { i j , Q _ { i j } - 1 } ^ { p }$ are points on the circles as well as on the line $s _ { i } s _ { j }$ . On each segment, we calculate the detour length as previously shown. Thus, we have:

$$
1 \leq \frac { w ( i , j ) } { d _ { i j } ^ { * } } \leq \frac { w ( i , j ) } { d _ { i j } } = \frac { \sum _ { k = 1 } ^ { Q _ { i j } - 1 } w ( s _ { i } , s _ { i j , k } ^ { p } ) } { \sum _ { k = 1 } ^ { Q _ { i j } - 1 } d _ { s _ { i } , s _ { i j , k } ^ { p } } } \leq \frac { \pi } { 2 } .\tag{38}
$$

This completes the proof.

Then, we will derive the total path length approximation ratio of Algorithm 2. We give the following theorem.

Theorem V.1: Algorithm 2 achieves $\frac { 3 \pi } { 4 }$ -approximation ratio of the total path length.

Proof: The approximation ratio of the total path length in the ACSA algorithm is derived from two main components: the approximation ratio for each edgeâs detour path length and the approximation ratio of Christofidesâ algorithm for solving the TSP.

Suppose the optimal solution and the solution obtained by Algorithm 2 are denoted as $S ^ { * }$ and $S _ { S O L }$ , respectively. The corresponding path vertices pair sets are denoted as ${ \mathcal { P } } ^ { * }$ and $\mathcal { P } _ { S O L }$ , respectively. Moreover, the minimum detour length is denoted as function $\mathcal { L } ^ { * } ( \cdot )$

( )For the first part, based on Lemma V.1, the detour path length $w ( i , j )$ generated by the Algorithm 2 satisfies:

$$
1 \leq \frac { \mathcal { L } ( S ^ { * } ) } { \mathcal { L } ^ { * } ( S ^ { * } ) } = \frac { \sum _ { ( s _ { i } , s _ { j } ) \in \mathcal { P } ^ { * } } w ( i , j ) } { \sum _ { ( s _ { i } , s _ { j } ) \in \mathcal { P } ^ { * } } d _ { i j } ^ { * } } \leq \frac { \pi } { 2 } .\tag{39}
$$

For the second part, we consider the approximation ratio of the TSP. Christofidesâ algorithm provides a solution for the TSP with an approximation ratio of . , that is,

$$
1 \leq \frac { \mathcal { L } ( S _ { S O L } ) } { \mathcal { L } ( S ^ { * } ) } \leq \frac { 3 } { 2 } .\tag{40}
$$

Combine with (39) and (40), we can derive the total path length approximation ratio:

$$
1 \leq \frac { \mathcal { L } ( S _ { S O L } ) } { \mathcal { L } ^ { * } ( S ^ { * } ) } \leq \frac { 3 } { 2 } \times \frac { \pi } { 2 } = \frac { 3 \pi } { 4 } .\tag{41}
$$

This completes the proof.

2) Objective Approximation Ratio Analysis: In this part, we prove the approximation ratio of the objective function. To begin with, we give some definitions and lemmas to support the submodularity of the objective function in P1.

Definition $V . I { : }$ (Monotone submodular function [39]) A function $F : 2 ^ { U } \to R _ { > 0 }$ is monotone submodular if for all $\mathcal { S } \subseteq \mathcal { T } \subseteq U , F ( s _ { j } | S ) \bar { \geq } F ( s _ { j } | T )$ , where $F ( s _ { j } | S ) = F ( S \cup$ $\{ s _ { j } \} ) - F ( S )$ ( ) ( ) ( ) = (is the marginal improvement of adding element $s _ { j }$ ) ( )to the set S.

However, in most practical routing problems such as node coverage or TSP on graphs, the cost function is not submodular. The main limitation of existing work lies precisely in assuming the routing cost function to be submodular. On the other hand, there exist special cases of TSP that exhibit submodularity, such as when the graph forms a tree structure [39]. Inspired by this observation, we employ a natural relaxation of submodularity called Î±-submodularity.

Definition V.2: (Î±-submodularity [39]) For a function $F ,$ , we define it as Î±-submodular for

$$
\alpha = \operatorname* { m i n } _ { x } \operatorname* { m i n } _ { s , \mathcal { T } : S \subset \mathcal { T } } \frac { F ( x | S ) } { F ( x | \mathcal { T } ) } .\tag{42}
$$

Definition V.3: (Î± monotone submodular function properties [39]) For any Î± monotone submodular function $F ,$ , the following statements hold.

$$
\begin{array} { r l } & { \mathrm { ~ i j ~ } F ( s _ { j } | \mathcal { S } ) \geq \alpha F ( s _ { j } | \mathcal { T } ) , \forall \mathcal { S } \subseteq \mathcal { T } \subseteq U \mathrm { ~ a n d ~ } s _ { j } \in U \backslash \mathcal { T } . } \\ & { \mathrm { ~ i i } ) ~ F ( \mathcal { T } ) \leq F ( \mathcal { S } ) + \frac { 1 } { \alpha } \sum _ { s _ { j } \in \mathcal { T } \backslash \mathcal { S } } F ( s _ { j } | \mathcal { S } ) - } \\ & { \ \alpha \sum _ { s _ { j } \in \mathcal { S } \backslash \mathcal { T } } F ( \mathcal { S } \cup \mathcal { T } \backslash s _ { j } ) , \forall \mathcal { S } , \mathcal { T } \subseteq U . } \\ & { \mathrm { ~ i i i } ) ~ F ( \mathcal { T } ) \leq F ( \mathcal { S } ) + \frac { 1 } { \alpha } \sum _ { s _ { j } \in \mathcal { T } \backslash \mathcal { S } } F ( s _ { j } | \mathcal { S } ) , \forall \mathcal { S } \subseteq U , \mathcal { T } \subseteq } \\ & { \ U . } \\ & { \mathrm { ~ i v } ) ~ F ( \mathcal { T } ) \leq F ( \mathcal { S } ) - \alpha \sum _ { s _ { j } \in \mathcal { S } \backslash \mathcal { T } } F ( s _ { j } | \mathcal { S } \backslash s _ { j } ) , \forall \mathcal { T } \subseteq \mathcal { S } \subseteq } \\ & { \ \quad U . } \end{array}
$$

Then, we prove the time cost function is an Î± monotone submodular function in the following lemma.

Lemma V.2: Given sufficient charging duration $t _ { \mathrm { m a x } } ^ { h a r v }$ , the time cost function $T ( \cdot )$ defined in (13) is an Î± monotone submodular function.

Proof: Given two hovering positions sets $s$ and $\tau$ that ${ \mathcal { S } } \subseteq$ $\tau ,$ when adding a charging station $s _ { j }$ , we obtain the marginal gain of time cost as follows:

$$
T ( s _ { j } | S ) = t _ { \operatorname* { m a x } } ^ { h a r v } + \Delta t _ { f } ( S ) ,\tag{43}
$$

where $\Delta t _ { f }$ is the flight time increment when optimizing the path. ÎThen due to $T ( s _ { j } | S ) \geq 0$ , we have

$$
T ( { \cal S } ) \le T ( { \cal S } \cup \{ s _ { j } \} ) \le T ( { \cal T } ) .\tag{44}
$$

Since a larger number of elements in the set increases the likelihood of obtaining more optimized paths, thereby reducing the time increment, there exists $\alpha \in [ 0 , 1 ]$ for any $s \subseteq \tau$ such that

$$
\Delta t _ { f } ( S ) \geq \alpha \Delta t _ { f } ( \mathcal T ) .\tag{45}
$$

So, we can obtain that

$$
\begin{array} { r l r } & { } & { T ( s _ { j } | S ) - \alpha T ( s _ { j } | T ) = ( 1 - \alpha ) t _ { \mathrm { m a x } } ^ { h a r v } + \Delta t _ { f } ( S ) - \alpha \Delta t _ { f } ( T ) } \\ & { } & \\ & { } & { \geq ( 1 - \alpha ) t _ { \mathrm { m a x } } ^ { h a r v } \geq 0 . \qquad ( 4 6 ) } \end{array}
$$

According to Definition V.3(i), the time cost function $T ( \cdot )$ in (13) is an Î± monotone submodular function.

Next, we can obtain that Next, we attempt to prove the Î±- submodularity of the objective function. we have the following lemma.

Lemma V.3: For $\mathcal { S } \subseteq \mathcal { T }$ , it holds that

$$
f ( S ) = R e w a r d ( S ) - \lambda \cdot T ( S ) \le f ( T ) ,\tag{47}
$$

where $\begin{array} { r } { \lambda \le \frac { R e w a r d ( T ) - R e w a r d ( S ) } { T ( T ) - T ( S ) } } \end{array}$

Proof: Since $\begin{array} { r } { \lambda \leq \frac { R e w a r d ( T ) - R e w a r d ( S ) } { T ( T ) - T ( S ) } } \end{array}$ , and given that the time cost function is an Î± monotone submodular function (Lemma V.2), multiplying both sides of the inequality by the denominator (which preserves the inequality direction) yields, we have

$$
\begin{array} { r l } & { R e w a r d ( \ T ) - R e w a r d ( \mathcal S ) \geq \lambda \cdot ( T ( \mathcal T ) - T ( \mathcal S ) ) } \\ & { } \\ & { \qquad = \lambda \cdot T ( \mathscr T ) - \lambda \cdot T ( \mathcal S ) . } \end{array}\tag{48}
$$

Then we can obtain that

$$
\begin{array} { r l } { f ( S ) = R e w a r d ( S ) - \lambda \cdot T ( S ) } & { { } } \\ { \leq R e w a r d ( T ) - \lambda \cdot T ( T ) = f ( T ) . } \end{array}\tag{49}
$$

Next, we prove the Î±-submodularity property of the objective function.

Lemma V.4: For $s \subseteq \tau$ , it holds that

$$
f ( s _ { j } | S ) \geq \alpha f ( s _ { j } | T ) ,\tag{50}
$$

where $\begin{array} { r } { \lambda \le \frac { R e w a r d ( s _ { j } | S ) - \alpha R e w a r d ( s _ { j } | T ) } { T ( s _ { j } | S ) - \alpha T ( s _ { j } | T ) } } \end{array}$ , and Î± is from Definition V.2.

Proof: Due to $\begin{array} { r } { \lambda \le \frac { R e w a r d ( s _ { j } | S ) - \alpha R e w a r d ( s _ { j } | T ) } { T ( s _ { j } | S ) - \alpha T ( s _ { j } | T ) } } \end{array}$ , and similar to Lemma V.3, we obtain

$$
\begin{array} { r l r } & { } & { R e w a r d ( s _ { j } | \mathcal S ) - \alpha R e w a r d ( s _ { j } | \mathcal T ) \ge \lambda \big ( T ( s _ { j } | \mathcal S ) - \alpha T ( s _ { j } | \mathcal T ) \big ) } \\ & { } & \\ & { } & { = \lambda T ( s _ { j } | \mathcal S ) - \lambda \alpha T ( s _ { j } | \mathcal T ) . } \end{array}\tag{)(51}
$$

Then we can obtain that

$$
\begin{array} { r l } & { f ( s _ { j } | S ) = R e w a r d ( s _ { j } | S ) - \lambda \cdot T ( s _ { j } | S ) } \\ & { \phantom { f ( s _ { j } | S ) = R e w a r d ( s _ { j } | T ) } \geq \alpha ( R e w a r d ( s _ { j } | T ) - \lambda \cdot T ( s _ { j } | T ) ) = \alpha f ( s _ { j } | T ) . } \end{array}\tag{)(52}
$$

Therefore, according to Lemma V.3 and Lemma V.4, we find that by setting an appropriate value for Î», we can ensure that our objective function is a monotone increasing Î±-submodular function. By leveraging the diminishing marginal gains property of a monotone submodular function, we can naturally propose an approximation algorithm with guaranteed approximation bounds.

Theorem V.2: Algorithm 2 achieves $\textstyle ( 1 - { \frac { 1 } { e } } )$ -approximation ratio.

Proof: Suppose $S ^ { * }$ is the optimal solution. Si is the vertices set obtained after the ith iteration of Algorithm 2 and k is the number of selected charging stations in Algorithm $2 . f ( \cdot )$ is the ( )function defined in (16). According to Lemma V.3, Lemma V.4

and Definition V.3, we have

$$
\begin{array} { r l r } { f ( \mathcal { S } ^ { * } ) \leq f ( S _ { i - 1 } ) + \displaystyle \frac { 1 } { \alpha } \sum _ { q \in \mathcal { S } ^ { * } / S _ { i - 1 } } \left( f ( S _ { i - 1 } \cup \{ q \} ) - f ( S _ { i - 1 } ) \right) } \\ { \leq f ( S _ { i - 1 } ) + \displaystyle \frac { 1 } { \alpha } \sum _ { q \in \mathcal { S } ^ { * } / S _ { i - 1 } } \left( f ( S _ { i } ) - f ( S _ { i - 1 } ) \right) } \\ { \ } & { \leq f ( S _ { i - 1 } ) + \displaystyle \frac { k } { \alpha } ( f ( S _ { i } ) - f ( S _ { i - 1 } ) ) , } & { \quad { \scriptstyle ( 5 3 } } \end{array}
$$

where the first inequality holds due to Definition V.3, the second inequality holds due to the greedy rule, and the third inequality holds due to at most k charging stations to be selected in Algorithm 2. Now we subtract $k f ( S ^ { * } )$ from both sides of the (equation simultaneously, notice that

$$
\begin{array} { l } { \displaystyle f ( {  { \mathcal { S } } } _ { i - 1 } ) + \frac { k } { \alpha } f ( {  { \mathcal { S } } } _ { i } ) - \frac { k } { \alpha } f ( {  { \mathcal { S } } } _ { i - 1 } ) - \frac { k } { \alpha } f ( {  { \mathcal { S } } } ^ { * } ) } \\ { \displaystyle \geq f ( {  { \mathcal { S } } } ^ { * } ) - \frac { k } { \alpha } f ( {  { \mathcal { S } } } ^ { * } ) . } \end{array}\tag{54}
$$

Then according to mathematical induction, we can obtain that

$$
\begin{array} { r } { f ( S _ { i } ) - f ( S ^ { * } ) \geq \left( 1 - \displaystyle \frac { \alpha } { k } \right) ( f ( S _ { i - 1 } ) - f ( S ^ { * } ) ) } \\ { \geq \left( 1 - \displaystyle \frac { \alpha } { k } \right) ^ { i } ( f ( S _ { 0 } ) - f ( S ^ { * } ) ) . } \end{array}\tag{55}
$$

Thus, we have that

$$
f ( S _ { i } ) \geq \left( 1 - \left( 1 - { \frac { \alpha } { k } } \right) ^ { i } \right) f ( S ^ { * } ) .\tag{56}
$$

When i approaches k, we derive the total approximation ratio of the algorithm, that is

$$
\begin{array} { c l l } { f ( S _ { k } ) \geq \left( 1 - \left( 1 - { \frac { \alpha } { k } } \right) ^ { k } \right) f ( S ^ { * } ) } \\ { \geq ( 1 - e ^ { - \alpha } ) f ( S ^ { * } ) . } \end{array}\tag{57}
$$

In practical Î± approaches 1. The approximation ratio of Algorithm 2 reaches $\textstyle 1 - { \frac { 1 } { e } }$

13) Time Complexity Analysis: In this subsection, we proceed to calculate the time complexity of the proposed algorithm. We propose the following theorem.

Theorem V.3: Given a UAV candidate positions graph $G =$ $( \mathcal { H P } , \mathcal { H P } \times \mathcal { H P } )$ =, Algorithm 2 achieves a time complexity of $O ( Q n ^ { 2 } + K ^ { 2 } n ^ { 3 } )$ ), where K is the number of charging stations (and $n = | \mathcal { H } \mathcal { P } |$

=Proof: Algorithm 2 can be separated into two parts: the initialization part (lines 1-2) and the main body (lines 3-13).

For the initialization part, we need to calculate the time complexity of Algorithm 1 (line 2). In Algorithm 1, we need to enumerate all pairs of vertices in $\mathcal { H P }$ , so the total times of iterations for lines 1-13 is $C _ { n } ^ { 2 } = n ( n - 1 ) / 2 = O ( n ^ { 2 } )$ . We = ( 1) 2 = ( )then consider the worst case that the line between each pair of vertices intersects all the obstacles. Thus, the inner loop (lines 8-13) iterates Q times. The final time complexity of Algorithm 1 becomes $O ( Q n ^ { 2 } )$

( )For the main body, we still divide into two conditions: $k =$ and $k > 0$ . When $k = 0 .$ , line 5 is conducted with $O ( n ^ { 3 } )$

<!-- image-->  
Fig. 4. Model Example.

(Christofidesâ algorithm), and line 10 is conducted M times with M edges in graph G. When $k > 0 , f ( S \cup \{ s _ { i } \} )$ is calculated $\left( K - ( k - 1 ) \right)$ times with $| { \mathcal { C P } } ^ { \prime } | = ( K - ( k - 1 ) )$ and ( ( 1)) = ( ( 1))Christofidesâ algorithm is conducted once in each calculation. Thus, the time complexity of line 7 is $O ( ( K - ( k -$ $1 ) ) n ^ { 3 } )$ (( (. In this case, line 10 is conducted M k times with $( M + k )$ ( + )edges in graph G. Therefore, the time complexity of the main body becomes $\begin{array} { r } { O ( ( n ^ { 3 } + M ) + \sum _ { k = 1 } ^ { K } ( K - ( k - 1 ) ^ { 2 } ) = 0 , } \end{array}$ $1 ) ) n ^ { 3 } + ( M + \bar { k } ) ) ) = O ( K ^ { 2 } { n ^ { 3 } } )$

) + ( + ))) = ( )To sum up, the time complexity of Algorithm 2 is $O ( Q n ^ { 2 } +$ $K ^ { 2 } n ^ { 3 } )$

## VI. SIMULATION

In this section, we conduct simulations to evaluate our algorithm.

## A. Experimental Settings

As shown in Fig. 4, we consider a ground device network that consists of default 200 devices, 10 obstacles, and 6 charging stations randomly deployed in a   Ã   square area. 600 m 600 mTable I lists the default settings of the parameters in this paper. We assume that the UAV is deployed at a depot $s _ { 0 }$ initially. The UAV has an energy capacity of $B _ { \mathrm { m a x } } = 2 0 0 ~ \mathrm { k J }$ , a constant flight speed of $v = 5 \mathrm { m } / \mathrm { s }$ = 200and a flying altitude of $H = 2 0 \mathrm { m }$ , with an = 5acceleration of $0 . 5 \mathrm { m } / \mathrm { s } ^ { 2 }$ = 20 mduring takeoff and a deceleration of $0 . 5 \mathrm { m } / \mathrm { s } ^ { 2 }$ 0 5 m sduring landing. Additionally, through experimental 0 5 m svalidation, we demonstrated that the value of Î± in our objective function can exceed 0.9 and approach 1 when weight Î» is 10.

## B. Baselines

To evaluate the performance of the proposed algorithm, we introduce five comparison algorithms.

1) CEDAN [40]: The main idea of this algorithm is to first calculate the trajectory using the TSP algorithm. Then, using the function RADJUSTMENT, the edge weights of each trajectory are recalculated based on our predefined objective function values. Finally, a greedy selection is employed to readjust the sequence of node visits within the trajectory.

TABLE I PARAMETER SETTINGS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1>Datacollection area side length</td><td rowspan=1 colspan=1>600m</td></tr><tr><td rowspan=1 colspan=1>Datatransmissionrange ofUAVr</td><td rowspan=1 colspan=1>70m</td></tr><tr><td rowspan=1 colspan=1>The fixed altitude ofUAVH</td><td rowspan=1 colspan=1>20m</td></tr><tr><td rowspan=1 colspan=1>Acceleration of UAV a</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1>Objetcive functionweight å¥</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>Theblade profilepowerin hovering status $\overline { { P _ { b l a d e } } }$ </td><td rowspan=1 colspan=1>79.86</td></tr><tr><td rowspan=1 colspan=1>Induced power in hovering status P1</td><td rowspan=1 colspan=1>88.63</td></tr><tr><td rowspan=1 colspan=1>Tipspeed of the rotor blade $\underline { { v } } _ { t i p }$ </td><td rowspan=1 colspan=1>120m/s</td></tr><tr><td rowspan=1 colspan=1>Mean rotor induced velocity in hover vo</td><td rowspan=1 colspan=1>4.03</td></tr><tr><td rowspan=1 colspan=1>Fuselage dragratioï¼</td><td rowspan=1 colspan=1>0.6</td></tr><tr><td rowspan=1 colspan=1>Air density p</td><td rowspan=1 colspan=1> $\overline { { 1 . 2 2 5 \mathrm { k g } / \mathrm { m } ^ { 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Rotor solidity $\overline { { R _ { s o l i d } } }$ </td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1>Rotor disc area $R _ { a r e a }$ </td><td rowspan=1 colspan=1>0.503mÂ²</td></tr><tr><td rowspan=1 colspan=1>Nodedatavolume D</td><td rowspan=1 colspan=1>100MB</td></tr><tr><td rowspan=1 colspan=1>Minimum transmission rate c</td><td rowspan=1 colspan=1>150Mbps</td></tr><tr><td rowspan=1 colspan=1>Data reception power of the UAV Prx</td><td rowspan=1 colspan=1>0.5W</td></tr><tr><td rowspan=1 colspan=1>Energy conversion efficiencies n</td><td rowspan=1 colspan=1>0.8</td></tr><tr><td rowspan=1 colspan=1>Area of laser receiver&#x27;s telescope or collection lens $A _ { r e c }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 } ~ } } \mathrm { m } ^ { 2 }$ </td></tr><tr><td rowspan=1 colspan=1>Combined transmission receiver optical efficiency </td><td rowspan=1 colspan=1>0.2</td></tr><tr><td rowspan=1 colspan=1>Energytransmit power of the $\ \overline { { \mathrm { C S s } \ \mathrm { ~ } P _ { 0 } } }$ </td><td rowspan=1 colspan=1>60dBm</td></tr><tr><td rowspan=1 colspan=1>Size of the initial laser beam $\overline { { { A _ { e m i t } } } }$ </td><td rowspan=1 colspan=1> $\overline { { 0 . 0 5 m } }$ </td></tr><tr><td rowspan=1 colspan=1>Attenuation coefficient of the channel medium $\kappa _ { t t }$ </td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 6 } \mathrm { m } ^ { - 1 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Angularspread Î²</td><td rowspan=1 colspan=1> $\overline { { 3 . 4 \times 1 0 ^ { - 5 } } }$ </td></tr></table>

2) GA [27]: The classical heuristic algorithm, Genetic Algorithm (GA), searches for optimal solutions through processes such as chromosome encoding, mutation, crossover, selection, and decoding.

3) SA [33]: Another heuristic algorithm, Simulated Annealing (SA), is based on the annealing process of physical phenomena.

4) RRT [22]: A sampling-based algorithm, Rapidlyexploring Random Tree (RRT) algorithm, computes detour paths in the presence of obstacles.

5) PF [23]: Another sampling-based algorithm, Artificial Potential Field (PF), has been commonly used in vehicle autonomous driving in recent years.

The result of algorithms is obtained based on a machine with 2.10 GHz Intel i7 single-core CPU and 32 GB RAM. Each value in the figures is the mean of the results out of 50 random network topologies of the same size.

## C. Visualization of Final UAV Trajectories

First, we present the trajectory computed by our proposed algorithm under the settings of $K = 6 , l = 7 0 \mathrm { m } , B _ { \mathrm { m a x } } = 2 0 0$ kJ, = 6 = 70 m = 200as shown in Fig. 5. In this scenario, our ACSA algorithm reduces the UAV flight distance by 56.5%, 66.2%, 70.4%, 4.77%, and 9.86% compared with CEDAN, SA, GA, RRT, and PF, respectively, while also reducing the task completion time by 16.7%, 50.1%, 51.4%, 6.25%, and 13.5%, respectively.

In the figure, the gray dots represent devices deployed in the scenario, the black-numbered points indicate UAV hovering positions, the blue-numbered points denote UAV wireless charging stations deployed on the ground, and the blue circular regions represent obstacles in the scenario.

<!-- image-->  
(a) ACSA Path.

<!-- image-->  
(b) CEDAN Path.

<!-- image-->  
(c) GA Path.

<!-- image-->  
(d) SA Path.

<!-- image-->  
(e) RRT Path.

<!-- image-->  
(f)PF Path.  
Fig. 5. Visualization of final UAV trajectories.

The UAVâs starting base station is numbered as 0, and the figure includes 52 hovering positions numbered from 1 to 52 and charging stations numbered from 53 to 58.

From the Fig. 5, it can be seen that all six algorithms successfully traversed all hovering positions and generated a complete closed trajectory, ensuring each hovering position is visited only once. Moreover, all the trajectories effectively achieved obstacle avoidance. In Fig. 5(a), we present the trajectory computed by our proposed ACSA algorithm. Compared with the results of more random heuristic algorithms in Fig. 5(e) and (f), ACSA generates shorter and more structured detour paths. Moreover, as shown in Fig. 5(b), the trajectory of the CEDAN algorithm tends to fall into local optima, resulting in a longer path from 52 to 0. In Fig. 5(c) and (d), the heuristic algorithms GA and SA are displayed. These two algorithms generate several unnecessary detour trajectories under the constraint of a limited number of iterations due to the high complexity of heuristics. The results demonstrate that our proposed algorithm effectively solves the POTWCN problem and delivers superior performance.

## D. Impact of Number of Charging Stations K

Our ACSA algorithm reduces the flight distance of the UAV by 42.57%, 49.60%, 54.36%, 14.86%, and 22.27% compared to CEDAN, SA, GA, RRT and PF, respectively, while also reducing the task completion time by 36.45%, 43.68%, 49.64%, 15.53%, and 25.68%, respectively.

As shown in Fig. 6, we test the stability of the proposed algorithm by varying the number of charging stations K deployed in the scenario. The y-axis in the figure represents the completion time $T ,$ the minimum number of required charging stations k, and the total path length L, respectively. In this scenario, we varied the total number of charging stations from 3 to 8, under the settings of $l = 7 0 \mathrm { m } , B _ { \mathrm { m a x } } = 1 5 0 \mathrm { k J }$ , and assumed an average = 70 m = 150charging time of approximately 1.49 hours.

We observe that due to the strong correlation between time consumption and the number of charging stations, the overall trends of the curves in Fig. 6(a) and (b) are similar. Since the number of charging stations required remains relatively constant, increasing the total number of charging stations primarily increases the available options for each station addition. As such, the increase in charging station numbers from 3 to 8 in the same scenario has little impact on the results, aligning with our experimental observations.

However, CEDAN adjusts the path sequence after computing the trajectory, which may occasionally transform a reasonable path into an unreasonable one. Moreover, once CEDAN calculates the path and selects the charging station closest to the path, it does not dynamically optimize the path based on newly added charging stations in the scenario, causing the subsequent results to remain unchanged. Additionally, the remaining algorithms demonstrate instability and produce suboptimal solutions. In contrast, our proposed algorithm achieves better stable results and converges to significantly better solutions.

<!-- image-->  
(a) Total time cost.

<!-- image-->  
(b) Minimum number of required charging stations.

<!-- image-->  
(cï¼ Total distance.

Fig. 6. Performance of different algorithms by varying the value of K from 3 to 8.  
<!-- image-->  
(a) Total time cost.

<!-- image-->  
(b)Minimum number of required charging stations.

<!-- image-->  
(c) Total distance.  
Fig. 7. Performance of different algorithms by varying the value of $B _ { \mathrm { m a x } }$ from 100 kJ to 350 kJ.

## E. Impact of Number of UAV Battery Capacity $B _ { \mathrm { m a x } }$

Our ACSA algorithm reduces the UAV flight distance by 41.09%, 47.33%, 53.79%, 13.00%, and 19.88% compared with CEDAN, SA, GA, RRT, and PF respectively, while also reducing the task completion time by 40.45%, 36.76%, 43.93%, 21.52%, and 26.15%, respectively.

As shown in Fig. 7(a), (b), and (c), we compare the total task completion time T , the minimum number of charging stations k required to ensure continuous operation, and total flight distance L under different UAV battery capacities. Since the time spent detouring around obstacles contributes a small proportion to the total task time, we separately compare the detour algorithms in Fig. 8 for better visualization. The results indicate that the trajectories computed by our algorithm require less detour time. From Fig. 7(a) and (b), it is evident that as the UAV battery capacity increases, both the calculated task completion time and the required number of charging stations decrease, which aligns with our expectations. In the figures, we observe that although the CEDAN algorithm uses fewer charging stations, its characteristic of forcibly adjusting the path sequence leads to longer task completion times. Additionally, we observe a proportional relationship between the total task time and the number of charging stations. This is because, in our defined time function, the charging time at each charging station is significantly greater than the UAVâs flight time between points, making the number of charging stations a dominant factor affecting task completion time. Furthermore, Fig. 7(a) shows that, compared with other algorithms, our proposed algorithm achieves shorter and more stable total task completion times.

<!-- image-->  
Fig. 8. Obstacle detour time.

## F. Impact of Number of Grid Cell Size l

Our ACSA algorithm reduces the UAV flight distance by 62.92%, 65.54%, 69.31%, 15.95%, and 24.10% compared to

<!-- image-->  
(a) Total time cost.

<!-- image-->  
(b) Minimum number of required charging stations.

<!-- image-->  
(cï¼ Total distance.  
Fig. 9. Performance of different algorithms by varying the value of l from 50 m to 100 m.

CEDAN, SA, GA, RRT and PF, respectively, while also reducing the task completion time by 46.08%, 59.14%, 61.96%, 19.12%, and 41.88%, respectively.

Next, we compare the performance under different grid sizes l. In this simulation, we fix the UAVâs maximum battery capacity $B _ { \mathrm { m a x } }$ at 150 kJ and the maximum number of charging stations deployed in the scenario K at 6.

As shown in Fig. 9, we compare the impact of grid size variations on the total task completion time, the minimum number of charging stations required to be added to the trajectory, and the total path length. From Fig. 9(a), it can be seen that as the grid edge length increases, the total task completion time calculated by the six algorithms gradually decreases. At the same time, our proposed algorithm consistently achieves shorter completion times compared with the other five algorithms. This is also reflected in Fig. 9(b), where the number of charging stations required by our algorithm is fewer, which is proportional to the total time cost, further validating its effectiveness and correctness. This is because, as the grid edge length increases, the number of hovering positions M in the entire target area decreases, resulting in fewer nodes for the UAV to traverse. The reduction in nodes plays a significant role in lowering the total trajectory time, which aligns with our logical expectations. Fig. 9(c) further demonstrates that as the grid edge length increases, the total path length calculated by the six algorithms also gradually decreases. And our proposed algorithm exhibits significant advantages in both total path length and detour efficiency, whether compared with path optimization algorithms or obstacle-avoidance algorithms.

## G. Impact of Number of Obstacles Q

Our ACSA algorithm reduces the UAV flight distance by 40.05%, 47.24%, 51.76%, 9.67%, and 17.42% compared with CEDAN, SA, GA, RRT, and PF respectively, while also reducing the task completion time by 29.86%, 36.28%, 40.56%, 6.50%, and 11.79%.

Additionally, to investigate the impact of the number of obstacles on the experimental results, we tested the outcomes of the algorithms as the number of obstacles increased from 0 to 10, as shown in Fig. 10. To highlight the effect of obstacle numbers, we fixed the UAV battery capacity at a sufficiently large value to ensure adequate power. Under these conditions, all algorithms required zero charging stations.

<!-- image-->  
(a) Total time cost.

<!-- image-->  
(bï¼ Total distance.  
Fig. 10. Performance of different algorithms by varying the value of Q from 0 to 10.

We compared the total completion time and total path length calculated by each algorithm, as shown in Fig. 10(a) and (b), respectively. It can be observed that the two metrics exhibit a positive correlation. This is because the total time is calculated as the sum of charging time and travel time. When the charging time is constant, travel time accounts for a larger proportion, making the total completion time proportional to the travel distance. The experimental results align well with our theoretical analysis.

Moreover, as the number of obstacles increases from 0 to 10, the gap between the two obstacle-avoidance algorithms and the proposed algorithm gradually widens, and all three algorithms exhibit an upward trend. On the other hand, the remaining three path-planning algorithms inherently calculate longer path lengths, so the increase in path length due to obstacle avoidance has a relatively smaller impact on the overall results. Regardless of whether compared with path-planning algorithms or obstacle-avoidance algorithms, our proposed algorithm consistently produces superior and more stable solutions.

<!-- image-->  
Fig. 11. Detour with Multi-Shaped Obstacles.

## VII. DISCUSSION

Although the circumscribed cylinder approach for obstacle approximation proposed in this paper is applicable in most real-world scenarios, the UAVâs hovering points may lie inside the circumscribed cylindrical structure of the obstacles in some cases, such as:

1) Obstacles in the form of long strips, such as buildings with a significant difference in length and width.

2) Obstacles with non-convex shapes.

In such cases, for obstacles of different shapes, we still represent the obstacle set as $\mathcal { O } = \{ b _ { 1 } , . . . , b _ { Q } \}$ . However, unlike the previous definition, each obstacle $b _ { i }$ is defined as a set containing vertex information (coordinates) and arc information (circle center coordinates and radii):

$$
\begin{array} { r } { b _ { i } = \{ b _ { i , 1 } , . . . , b _ { i , Q _ { i } ^ { v } } , \langle b _ { i , 1 } ^ { a } , r _ { i } \rangle , . . . , \langle b _ { i , Q _ { i } ^ { a } } ^ { a } , r _ { i } \rangle \} , } \end{array}\tag{58}
$$

where $Q _ { i } ^ { v }$ and $Q _ { i } ^ { a }$ are the number of vertices and arcs of $b _ { i } .$ respectively, and $b _ { i , k }$ and $b _ { i , k } ^ { a }$ represent coordinates of the vertex and the circle center corresponding to the arc of $b _ { i }$ , as shown in Fig. 11.

When designing a new obstacle avoidance algorithm, we retain the core strategy but substitute tangent points with vertices for straight-line segments. Specifically, the UAV flies from the current position towards the vertex (for a straight edge) or the tangent point of the nearest obstacle, follows the obstacle boundary, and exits the current obstacle where the line connecting two consecutive hovering points intersects the obstacle. This process repeats until there is no obstruction along the line connecting the current position and the ending hovering point; it then flies directly to the ending hovering in a straight line.

Letâs take Fig. 11 as a toy example. The UAV needs to fly from si to $s _ { j }$ , but 3 obstacles blocks the trajectory. First, the current position is $s _ { i }$ and the nearest obstacle is $b _ { q _ { 1 } }$ . The algorithm calculates the distances $L _ { s _ { i } , b _ { q _ { 1 } , 1 } } , L _ { s _ { i } , b _ { q _ { 1 } , 2 } } , L _ { s _ { i } , b _ { q _ { 1 } , 3 } } ,$ and $L _ { s _ { i } , b _ { q _ { 1 } , 4 } }$ , and obtains the minimum distance $L _ { s _ { i } , b _ { q _ { 1 } , 2 } } .$ Thus, the UAV flies to $b _ { q _ { 1 } , 2 }$ . Then, the algorithm calculates which detour to the intersection point $( s _ { i j , 1 } ^ { p } )$ of $b _ { q _ { 1 } }$ and line $s _ { i } s _ { j }$ is the shortest, comparing the distances of paths $b _ { q _ { 1 } , 2 } \to b _ { q _ { 1 } , 1 } \to s _ { i j , 1 } ^ { p }$ and $b _ { q _ { 1 } , 2 } \to b _ { q _ { 1 } , 3 } \to b _ { q _ { 1 } , 4 } \to s _ { i j , 1 } ^ { p }$ . Obviously, the former path is shorter, so the UAV flies along it to $s _ { i j , 1 } ^ { p }$ . Next, similarly, the algorithm selects the nearest vertex $b _ { q _ { 2 } , 2 }$ of $b _ { q _ { 2 } }$ and the shortest detour $b _ { q _ { 2 } , 2 } \to b _ { q _ { 2 } , 1 } \to s _ { i j , 2 } ^ { p }$ . Afterwards, for obstacle $b _ { q _ { 3 } } ,$ the algorithm calculates the distances from $s _ { i j , 2 } ^ { p }$ to all the vertices and the tangent points of the arc, and chooses the nearest point $s _ { i j , 3 , 1 }$ . Finally, the algorithm calculates the shortest detour to $s _ { j }$ where the point at which the UAV leaves the last obstacle $b _ { q _ { 3 } }$ is a vertex or a tangent point of $b _ { q _ { 3 } }$ . So, the algorithm obtains the path $s _ { i j , 3 , 1 } \to b _ { q _ { 3 } , 1 } \to s _ { j }$ . And the final path has been obtained.

Note that this algorithm may not always obtain the shortest path. For example, in Fig. 11, the trajectory would be shorter if the UAV flew directly from $b _ { q _ { 1 } , 1 }$ to $b _ { q _ { 2 } , 1 }$ and from $b _ { q _ { 2 } , 1 } \mathrm { t o } s _ { i j , 3 , 1 }$ An improvement would be to leave obstacles at the vertices or tangent points and then decide the next flying position. However, this may cause significant computational overhead when calculating the shortest path.

## VIII. CONCLUSION

In this paper, we solve the Practical Optimizing UAV Trajectory in Wireless Charging Networks (POTWCN) problem in the presence of obstacles, to overcome the energy limitations encountered during UAV missions. We prove that this problem is NP-hard. The key technical depth lies in the design of an effective obstacle-avoidance trajectory with performance bound. We decompose the problem into two subproblems. We first design a geometry-based obstacle avoidance algorithm to complete the trajectory planning task with detour performance bound Ï/ . Second, we propose a $( 1 - { \frac { 1 } { e } } )$ -approximation algorithm 3 4 (1 )to balance the task completion time and the number of visited charging stations, leveraging the properties of the submodular function, and address the energy constraint issue by dynamically adjusting the number of charging stations. Experimental results demonstrate that our proposed algorithm is stable, and it can effectively reduce both the path length and the task completion time.

In the future, our goal is to consider the collaborative application of multiple UAVs in complex network environments.

## REFERENCES

[1] A. Al-Hourani, K. Sithamparanathan, and S. Lardner, âOptimal LAP altitude for maximum coverage,â IEEE Wireless Commun. Lett., vol. 3, no. 6, pp. 569â572, Dec. 2014.

[2] Marketsand markets. 2022. [Online]. Available: https://www.market sandmarkets.com/Market-Reports/unmanned-aerial-vehicles-uav-marke t-662.html

[3] SFâs drones. 2023. [Online]. Available: https://piw-mr-web.inn.sf-express .com/

[4] PowerLight technologies. 2023. [Online]. Available: https://power lighttech.com/autonomous-vehicles.html

[5] J. Fingas, âHuawei wants to use lasers to charge drones, cell towers,â 2017. [Online]. Available: https://www.engadget.com/2017-02-27- huawei-drone-charging-cell-towers.html

[6] H. Pan, Y. Liu, G. Sun, J. Fan, S. Liang, and C. Yuen, âJoint power and 3D trajectory optimization for UAV-enabled wireless powered communication networks with obstacles,â IEEE Trans. Commun., vol. 71, no. 4, pp. 2364â2380, Apr. 2023.

[7] X. Dai, Z. Xiao, H. Jiang, and J. C. S. Lui, âUAV-assisted task offloading in vehicular edge computing networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2520â2534, Apr. 2024.

[8] J. Xu, K. Ota, and M. Dong, âAerial edge computing: Flying attitudeaware collaboration for multi-UAV,â IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 5706â5718, Oct. 2023.

[9] Z. Song, K. Chin, C. Yang, and M. Ros, âMethods to assign UAVs for Kcoverage and recharging in IoT networks,â IEEE Trans. Mobile Comput., vol. 23, no. 4, pp. 2504â2519, Apr. 2024.

[10] M. Lahmeri, M. A. Kishk, and M. Alouini, âLaser-powered UAVs for wireless communication coverage: A large-scale deployment strategy,â IEEE Trans. Wireless Commun., vol. 22, no. 1, pp. 518â533, Jan. 2023.

[11] P. Du, F. Xie, S. Chen, and X. Zhang, âTime-constrained UAV-aided data collection for IoT networks with energy harvesting,â in Proc. IEEE Conf. Comput. Commun. Workshop, Hoboken, NJ, USA, 2023, pp. 1â6.

[12] X. Hu, K. Wong, and Y. Zhang, âWireless-powered edge computing with cooperative UAV: Task, time scheduling and trajectory design,â IEEE Trans. Wireless Commun., vol. 19, no. 12, pp. 8083â8098, Dec. 2020.

[13] S. Aggarwal and N. Kumar, âPath planning techniques for unmanned aerial vehicles: A review, solutions, and challenges,â Comput. Commun., vol. 149, pp. 270â299, 2020.

[14] W. Jiang, Y. Lyu, Y. Li, Y. Guo, and W. Zhang, âUAV path planning and collision avoidance in 3D environments based on pompd and improved grey wolf optimizer,â Aerosp. Sci. Technol., vol. 121, 2022, Art. no. 107314.

[15] N. Christofides, âWorst-case analysis of a new heuristic for the travelling salesman problem,â Oper. Res. Forum, vol. 3, no. 1, 2022, Art. no. 10.

[16] H. Gong, B. Huang, and B. Jia, âEnergy-efficient 3-D UAV ground node accessing using the minimum number of UAVs,â IEEE Trans. Mobile Comput., vol. 23, no. 12, pp. 12046â12060, Dec. 2024.

[17] K. Wang, X. Zhang, L. Duan, and J. Tie, âMulti-UAV cooperative trajectory for servicing dynamic demands and charging battery,â IEEE Trans. Mobile Comput., vol. 22, no. 3, pp. 1599â1614, Mar. 2023.

[18] Y. Li et al., âData collection maximization in IoT-sensor networks via an energy-constrained UAV,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 159â174, Jan. 2023.

[19] C. Xiang et al., âReusing delivery drones for urban crowdsensing,â IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2972â2988, May 2023.

[20] W. Xu et al., âReward maximization for disaster zone monitoring with heterogeneous UAVs,â IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 890â903, Feb. 2024.

[21] W. Xu et al., âCollect spatiotemporally correlated data in IoT networks with an energy-constrained UAV,â IEEE Internet Things J., vol. 11, no. 11, pp. 20486â20498, Jun. 2024.

[22] Y. Rasekhipour, A. Khajepour, S. Chen, and B. Litkouhi, âA potential field-based model predictive path-planning controller for autonomous road vehicles,â IEEE Trans. Intell. Transp. Syst., vol. 18, no. 5, pp. 1255â1267, May 2017.

[23] S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, and S. J. Teller, âAnytime motion planning using the RRT,â in Proc. IEEE Int. Conf. Robot. Automat., Shanghai, China, 2011, pp. 1478â1483.

[24] L. Jaillet, J. CortÃ©s, and T. SimÃ©on, âTransition-based RRT for path planning in continuous cost spaces,â in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., Nice, France, 2008, pp. 2145â2150.

[25] Z. Tahir, A. H. Qureshi, Y. Ayaz, and R. Nawaz, âPotentially guided bidirectionalized RRT\* for fast optimal path planning in cluttered environments,â Robot. Auton. Syst., vol. 108, pp. 13â27, 2018.

[26] Y. Chen and L. Wang, âAdaptively dynamic RRT\*-connect: Path planning for UAVs against dynamic obstacles,â in Proc. 7th Int. Conf. Automat., Control Robot. Eng., Xiâan, China, 2022, pp. 1â7.

[27] J. W. Kim and S. K. Kim, âFitness switching genetic algorithm for solving combinatorial optimization problems with rare feasible solutions,â J. Supercomput., vol. 72, no. 9, pp. 3549â3571, 2016.

[28] S. Choueiry, M. Owayjan, H. Diab, and R. Achkar, âMobile robot path planning using genetic algorithm in a static environment,â in Proc. 4th Int. Conf. Adv. Comput. Tools Eng. Appl., Beirut, Lebanon, 2019, pp. 1â6.

[29] Y. V. Pehlivanoglu, âA new vibrational genetic algorithm enhanced with a Voronoi diagram for path planning of autonomous UAV,â Aerosp. Sci. Technol., vol. 16, no. 1, pp. 47â55, 2012.

[30] M. da Silva Arantes, J. da Silva Arantes, C. F. M. Toledo, and B. C. Williams, âA hybrid multi-population genetic algorithm for UAV path planning,â in Proc. Genet. Evol. Comput. Conf., Denver, CO, USA, 2016, pp. 853â860.

[31] Y. Wu, S. Wu, and X. Hu, âCooperative path planning of UAVs & UGVs for a persistent surveillance task in urban environments,â IEEE Internet Things J., vol. 8, no. 6, pp. 4906â4919, Mar. 2021.

[32] Y. Zhang, X. Liu, F. Bao, J. Chi, C. Zhang, and P. Liu, âParticle swarm optimization with adaptive learning strategy,â Knowl. Based Syst., vol. 196, 2020, Art. no. 105789.

[33] M. Steinbrunn, G. Moerkotte, and A. Kemper, âHeuristic and randomized optimization for the join ordering problem,â VLDB J., vol. 6, no. 3, pp. 191â208, 1997.

[34] Z. Yu, Z. Si, X. Li, D. Wang, and H. Song, âA novel hybrid particle swarm optimization algorithm for path planning of UAVs,â IEEE Internet Things J., vol. 9, no. 22, pp. 22547â22558, Nov. 2022.

[35] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[36] J. Ouyang, Y. Che, J. Xu, and K. Wu, âThroughput maximization for laser-powered UAV wireless communication systems,â in Proc. IEEE Int. Conf. Commun. Workshops, Kansas City, MO, USA, 2018, pp. 1â6.

[37] D. Killinger, âFree space optics for laser communication through the air,â Opt. Photon. News, vol. 13, no. 10, pp. 36â42, 2002.

[38] H. Le, âA PTAS for subset TSP in minor-free graphs,â in Proc. ACM-SIAM Symp. Discrete Algorithms, Salt Lake City, UT, USA, 2020, pp. 2279â2298.

[39] H. Zhang and Y. Vorobeychik, âSubmodular optimization with routing constraints,â in Proc. 13th AAAI Conf. Artif. Intell., Phoenix, Arizona, USA, 2016, pp. 819â826.

[40] A. Bera, S. Misra, C. Chatterjee, and S. Mao, âCEDAN: Cost-effective data aggregation for UAV-enabled IoT networks,â IEEE Trans. Mobile Comput., vol. 22, no. 9, pp. 5053â5063, Sep. 2023.

<!-- image-->  
Yundi Wang received the BS degree from the School of Computer Science and Information, Anhui Normal University, in 2023. She is currently working toward the MS degree with the School of Computer Science and Technology, Soochow University. Her primary research interests lie in the fields of UAV networks and wireless charging.

<!-- image-->

Xiaoyu Wang received the BS degree in the School of Computer Science and Technology from Soochow University, Suzhou, Jiangsu, China, in 2016, and the PhD degree in the Department of Computer Science and Technology in Nanjing University, Nanjing, Jiangsu, China, in 2021. Her research interests focus on wireless charging and data mining. She is now an associate professor in School of Computer Science and Technology in Soochow University.

<!-- image-->

He Huang (Senior Member, IEEE) received the PhD degree from the School of Computer Science and Technology, University of Science and Technology of China (USTC), China, in 2011. He is currently a professor with the School of Computer Science and Technology, Soochow University, China. From 2019 to 2020, he was a visiting research scholar with Florida University, Gainesville. He has authored more than 100 papers in related international conference proceedings and journals. His current research interests include traffic measurement, computer networks,

and algorithmic game theory. He is a member of the Association for Computing Machinery (ACM). He received the best paper awards from Bigcom 2016, IEEE MSN 2018, and Bigcom 2018. He has served as the Technical Program Committee member of several conferences, including IEEE INFOCOM, IEEE MASS, IEEE ICC, and IEEE Globecom.

<!-- image-->

Haipeng Dai (Senior Member, IEEE) received the BS degree in the Department of Electronic Engineering from Shanghai Jiao Tong University, Shanghai, China, in 2010, and the PhD degree in the Department of Computer Science and Technology in Nanjing University, Nanjing, China, in 2014. His research interests are mainly in the areas of wireless charging, mobile computing, and data mining. He is an associate professor in School of Computer Science in Nanjing University. He has authored more than 200 papers in many prestigious conferences and journals such as USENIX NSDI, ACM UbiComp, IEEE INFOCOM, USENIX ATC, ACM EuroSys, ACM SIGMOD, Proceedings of the VLDB Endowment, IEEE ICDE, ACM SIGMETRICS, ACM MobiSys, ACM MobiHoc, IEEE ICNP, IEEE IPSN, IEEE Transactions on Mobile Computing, IEEE Journal on Selected Areas in Communications, IEEE/ACM Transactions on Networking, IEEE Transactions on Parallel and Distributed Systems, and IEEE TOSN. He is an IEEE senior member and ACM senior member. He serves/ed as the leading program chair of IEEE ISPAâ22-23, the Co-Vice Program Chair of IEEE HPCCâ21, Track Chair of the ICCCNâ19 and ICPADSâ21. He served as TPC member of international conferences such as INFOCOM, IJCAI, SC, VLDB, SIGKDD, MobiHoc, and ICNP. He received Best Paper Award from IEEE ICNPâ15, Best Paper Award Runner-up from IEEE SECONâ18, Best Paper Award Candidate from IEEE INFOCOMâ17, Best Paper Award from IEEE HPCCâ22, Best Paper Award from WASAâ22, and Distinguished Paper Award from ACM UbiCompâ22.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_1.png|page_7_img_1]]
3. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_2.jpeg|page_7_img_2]]
4. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_3.jpeg|page_7_img_3]]
5. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_4.png|page_7_img_4]]
6. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_5.png|page_7_img_5]]
7. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_6.png|page_7_img_6]]
8. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_7.png|page_7_img_7]]
9. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_8.png|page_7_img_8]]
10. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_9.png|page_7_img_9]]
11. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_10.png|page_7_img_10]]
12. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_11.png|page_7_img_11]]
13. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_12.png|page_7_img_12]]
14. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_13.png|page_7_img_13]]
15. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_7_img_14.png|page_7_img_14]]
16. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_1.png|page_9_img_1]]
17. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_2.png|page_9_img_2]]
18. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_3.png|page_9_img_3]]
19. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_4.png|page_9_img_4]]
20. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_5.png|page_9_img_5]]
21. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_6.png|page_9_img_6]]
22. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_7.png|page_9_img_7]]
23. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_8.png|page_9_img_8]]
24. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_9.png|page_9_img_9]]
25. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_10.png|page_9_img_10]]
26. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_11.png|page_9_img_11]]
27. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_12.png|page_9_img_12]]
28. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_13.png|page_9_img_13]]
29. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_14.png|page_9_img_14]]
30. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_15.png|page_9_img_15]]
31. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_16.png|page_9_img_16]]
32. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_17.png|page_9_img_17]]
33. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_18.png|page_9_img_18]]
34. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_19.png|page_9_img_19]]
35. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_20.png|page_9_img_20]]
36. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_21.png|page_9_img_21]]
37. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_22.png|page_9_img_22]]
38. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_23.png|page_9_img_23]]
39. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_24.png|page_9_img_24]]
40. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_9_img_25.png|page_9_img_25]]
41. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_1.png|page_15_img_1]]
42. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_2.png|page_15_img_2]]
43. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_3.png|page_15_img_3]]
44. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_4.png|page_15_img_4]]
45. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_5.png|page_15_img_5]]
46. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_6.png|page_15_img_6]]
47. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_7.png|page_15_img_7]]
48. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_8.png|page_15_img_8]]
49. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_9.png|page_15_img_9]]
50. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_10.png|page_15_img_10]]
51. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_11.png|page_15_img_11]]
52. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_12.png|page_15_img_12]]
53. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_13.png|page_15_img_13]]
54. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_14.png|page_15_img_14]]
55. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_15.png|page_15_img_15]]
56. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_16.png|page_15_img_16]]
57. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_17.png|page_15_img_17]]
58. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_15_img_18.png|page_15_img_18]]
59. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_16_img_1.jpeg|page_16_img_1]]
60. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_16_img_2.jpeg|page_16_img_2]]
61. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_17_img_1.jpeg|page_17_img_1]]
62. [[../extracted_images/Practical_Optimizing_UAV_Trajectory_in_Wireless_Charging_Networks_An_Approximated_Approach/page_17_img_2.jpeg|page_17_img_2]]

---

