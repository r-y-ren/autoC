# Energy Efficient Transmission Strategy for Mobile Edge Computing Network in UAV-Based Patrol Inspection System

Dingcheng Yang , Jun Wang , Fahui Wu , Lin Xiao , Yu Xu , and Tiankui Zhang , Senior Member, IEEE

AbstractâIn this paper, we consider an unmanned aerial vehicle (UAV)-based patrol inspection scenario, where the cellularconnected UAV traverses multiple pre-determined waypoints for data collection, and then offloads computation task to the ground base stations (GBSs). This paper aims to minimize the sum of the total energy consumption by jointly optimizing the task completion time, communication scheduling, computation resource allocation, and UAVâs trajectory. First, we decompose the original problem into two trackable subproblems: 1) design the optimal traverse order among cruise points; and 2) determine the optimal transmission strategy between two consecutive cruise points. Then, by involving the communication rate performance and the topology construct among the GBSs and the cruise points, a novel weighted factor of the edge is proposed to design the traverse order, which can be compatible with the light and heavy task offloading scenarios. The successive convex approximation (SCA) technique and block coordinate descent (BCD) framework are adopted to optimize the UAVâs trajectory and the wireless resource allocation. The numerical results finally indicate that our proposed transmission strategy solution decreases the total energy consumption in various scenarios and outperforms other benchmark schemes.

Index TermsâCellular-connected UAV, mobile-edge computing, patrol inspection, energy consumption.

## I. INTRODUCTION

U NMANNED aerial vehicles (UAVs) are a promising toolto be applied in wireless communication systems because of their mobility, flexibility, and scalability. The UAVs equipped with communication equipments can be deployed for a variety of emergency missions such as reconnaissance and tracking. The article [1] describes a framework for a UAV-assisted emergency network in disaster scenarios. Generally, integrating UAVs into cellular networks can further improve the performance

of UAVs [2]. As thus, cellular-connected UAVs are gradually demonstrating advantages in high-altitude operations and it can perform many complex tasks, such as power inspections, military reconnaissance, cargo delivery, remote sensing, etc. This mechanized operation method not only significantly improves work efficiency, but also ensures safety. For these scenarios, the patrolling inspection tasks would have a lot of computing requirements. However, it is well known that UAVs have limited on-board energy. Therefore, the computation-intensive and/or latency-sensitive tasks would be a challenge for cellularconnected UAVs. Against this background, mobile-edge computing (MEC) technique is introduced to address this issue by offloading the tasks to the adjacent resource-rich servers, which moderates the contradiction between the limited energy and the latency sensitivity. This paper introduces the MEC technique to the cellular-connected UAV in patrol inspection scenario, and investigates the energy consumption of the UAV. In practice, the algorithm proposed in this paper not only saves the UAV energy, but also fully exploits the resources of ground base stations (GBSs), which greatly reduces the task completion time of the network.

## A. Related Works and Motivations

There is a burgeoning interest in integrating UAVs into cellular networks. Thanks to the ubiquitous accessibility and robust navigation, cellular-connected UAVs are exploited to perform various tasks. The cellular-connected UAVs offer significant advantages over the traditional UAVs that act as aerial base stations [3]. There has been a lot of works on cellular-connected UAVs [4], [5], [6], [7]. In [4], the authors utilize the deep reinforcement learning method to design UAV trajectory, by minimizing the weighted sum of the task completion time and the communication interruption time. The work in [5] investigates the delay issue of the UAV offloading different packets to the GBSs. The work [6] minimizes the energy consumption of cellular-connected UAVs by jointly optimizing task completion time, communication scheduling, and trajectory for channel knowledge map availability and unavailability cases. To maintain the connection between the UAV and GBSs, the authors in [7] propose an iterative algorithm based on the geometric planning to design the UAV trajectory.

There are also some works on cellular-connected UAVs in MEC cases, where the computationally intensive tasks need to be offloaded by the UAV to GBSs or access points (APs) because of the UAVâs limited computing power. Specifically, in [8], the authors consider an application scenario where a fixed-wing UAV offloads data to a GBS for computation, and the UAV flight energy consumption and communication energy consumption are minimized by optimizing the UAV trajectory, velocity, and computation resource allocation. The work in [9] further considers multiple UAVs performing computing and offloading tasks to explore the performance of multiple-UAV scheduling. The paper proposes four uplink transmission methods. Both the above-mentioned works consider the single one BS. Actually, in realistic scenarios, the UAV may fly in the coverage area of multiple GBSs. In [10], the UAV selectively offloads the task to multiple GBSs. Then, these GBSs return the results to the UAV. Moreover, T. Bai et al. in [11] study the computation energy consumption as well as the communication energy consumption of cellular-connected UAVs to obtain the optimal solution by optimizing the UAV transmitting power, computation time, and computation size, but the flight energy consumption of UAV is neglected. A rotary-wing UAV is employed in [12] to perform the data offloading, and the trajectory of the UAV is designed. However, the task completion time in this work is not considered.

The utilizing of UAVs for patrolling inspection is of practical importance because the task can be done more efficiently by utilizing the mobility and high scalability of UAVs [13]. The paper [14] provides a comprehensive introduction and guidance on UAV-based patrolling inspection platforms. The work in [15] introduces a rotary-wing UAV-based patrolling inspection platform in more detail, and reveals that the efficiency and safety of UAV-based mechanical inspection are higher than those of manual inspections. The paper [16] investigates the scenario of multiple patrolling UAVs as aerial base stations, which can provide better channel conditions for cell-edge users. In this paper, the authors propose two patrolling algorithms, based on which the UAVsâ trajectories are designed. The authors in [17] optimize the UAV 3D trajectory by minimizing the energy consumption, they only consider the patrolling UAV passing through a few fixed points without considering the data processing. The paper [18] explores the multi-UAV patrolling problem in terms of minimizing mission completion time. The authors first optimize the mission point visiting order and then optimize the UAV trajectory, but they ignore the potential impact of energy. Considering the limited energy on board, the work in [19] focuses on the endurance of the patrolling UAVs, by planning paths rationally so that the patrolling UAVs can make multiple trips to the charging stations to recharge power. Similarly, the work [20] proposes a deterministic algorithm for planning the path to reduce the task completion time. In addition, the article [21] combines non-orthogonal multiple access (NOMA) and millimeter-wave (mmWave) to investigate the problem of energy efficiency maximization.

To the best of our knowledge, for the point-by-point patrolling inspection scenarios, few work related to the cellular-connected UAV-MEC framework has investigated the problem of minimizing the energy consumption, which motivates us to carry out this work and make progress in this area.

## B. Main Contributions

In this paper, we investigate the problem of minimizing the total energy consumption in a cellular-connected UAV-MEC system. We use a rotary-wing UAV with quick shooting and computing capabilities for data collection and processing. The patrolling UAV needs to perform shooting tasks at each predetermined cruising point, after which the UAV and GBSs have to process the collected data timely. Our work differs from the existing efforts [22], [23], [24], where the UAVs are not required to travel to multiple predetermined locations for patrol missions. In particular, to meet the patrol requirements, we propose a novel scheme to determine the cruising point traverse order. The main contributions of this paper are summarized as follows:

1) We propose a UAV-MEC framework in patrol inspection scenarios. The patrolling UAV performs both fixed-point shooting and data processing, which can capture current status information and make timely decisions for the complex tasks. Considering the limited onboard energy and limited computation capacity, the patrolling UAV will select the surrounding GBS for helping it complete the data processing. In addition, considering the delay-sensitive computation offloading in the patrolling inspection scenario, the process of performing tasks is divided into several sub-processes for handling.

2) Considering that the traditional trajectory initialization method cannot effectively meet the requirements of traversing multiple cruise points and improving the system performance, we propose a novel criterion to design the cruise point traverse order. This proposed scheme can flexibly determine the traverse order based on the relationship between the estimated throughput of the edge and the size of the captured data. When the data size is small, the proposed scheme mainly considers traveling distance as a dominant factor to determine the traverse order. When the amount of data is large, the scheme further considers the communication rate for data offloading as the dominant factor. The proposed scheme unifies the traveling salesman problem (TSP) criterion and energy-efficient traveling salesman problem (EETSP) criterion. Moreover, it is more flexible than the TSP criterion and EETSP criterion.

3) We propose a mathematical model for minimizing the sum of UAV flight energy, communication energy, and computation energy, by optimizing the UAV trajectory, mission completion time, communication scheduling, and computational resource allocation. The formulated problem is difficult to handle, since it contains continuous optimization variables. As a result, we first decompose the original problem into several parallel subproblems. Then, we apply the path disretization technique to transform the problems into discrete ones. Next, we further deal with the non-convexity of the obtained problem via using the successive convex approximation (SCA) technique and the block coordinate descent (BCD) framework, based on which an iterative algorithm is finally derived.

4) The simulation results demonstrate the effectiveness and feasibility of the proposed algorithm. Compared to the traditional schemes, e.g., the round tour or the exhaustive optimum, the proposed scheme is superior with lower complexity. Besides, the proposed algorithm provides more options for trajectory design and is of great relevance in the UAV patrolling inspection scenarios.

<!-- image-->  
Fig. 1. System model for the cellular-connected UAV-MEC patrol inspection system.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

As shown in Fig. 1, we consider a cellular-connected UAV patrol inspection system, which consists of a rotary-wing UAV equipped with a MEC server and a powerful data acquisition equipment such as the laser radar or high definition (HD) camera. There are $M \geq 1 \mathrm { G B S s }$ equipped with high-performance MEC servers. These GBSs are distributed within the UAVâs cruise region, denoted by the set $\mathcal { G } = \{ g _ { 1 } , . . . , g _ { M } \}$ . Assuming that =the patrol UAV needs to traverse the $K \geq 1$ cruise points in 1one flight mission. The cruise points are denoted by the set $\boldsymbol { S } = \{ s _ { 1 } , . . . , s _ { K } \}$ . The coordinates of the GBSs and the cruise points are represented by $\mathbf { w } _ { g _ { m } } \in \mathbb { R } ^ { 2 \times 1 } , g _ { m } \in \mathcal { G }$ , and ${ \bf w } _ { s _ { k } } \in  { \bf \Psi }$ $\mathbb { R } ^ { 2 \times 1 } , s _ { k } \in \mathcal { S }$ , respectively.

Assume that there are enough GBSs in the terrestrial network to ensure the seamless coverage. In one period, the UAV first takes off from a given starting point $\mathbf q _ { I } \in \mathbb R ^ { 2 \times 1 }$ at a certain altitude $H _ { U } > 0$ . Then, it traverses the cruise points and makes 0the data acquisition and processing. Finally, it lands on the ending point $\mathbf q _ { F } \in \mathbb R ^ { 2 \times 1 }$ . Suppose the traverse order of the UAV can be expressed as $\pmb { \eta } \triangleq \{ \eta ( 0 ) , \eta ( 1 ) , . . \eta ( k ) . . , \eta ( K ) , \eta ( K + 1 ) \}$ , where $\eta ( k ) \in \eta$ = (0) (1) ( ) ( ) ( + 1)indicates the index of the kth visited cruise point $s _ { \eta ( k ) } \in \mathcal { S }$ . It holds that $s _ { \eta ( 0 ) } = \mathbf { q } _ { \iota }$ and $\begin{array} { r } { s _ { \eta ( K + 1 ) } = \mathbf q _ { F } } \end{array}$ = =The whole operating time, or the period, is represented as T .

For the UAV patrol inspection scenario, the UAV visits each cruise point and employs the laser radar or HD camera to capture the key information of the target area, such as the large amount of HD quick photos/videos or 3D point cloud data. These generated datas need to be processed by the UAV for the purpose of obtaining the result such as target recognition or environment reconstruction for the patrol inspection. Assume that there is $Q _ { s _ { k } }$ in bits of data is captured by the UAV at the cruise point $s _ { k } .$ k. Generally, considering a latency-sensitive case, the UAV should complete the information computation and obtain the result before reaching the next cruise point. Due to the limited computing capacity and energy, the UAV cannot afford a huge calculation ability. Therefore, offloading the data to the GBSs is adopted for the UAV, which can ensure the latency-sensitive tasks being completed in time.

In order to utilize the limited energy effectively, the dynamic voltage and frequency scaling (DVFS) technique [25] is adopted for the MEC servers at the UAV and GBSs. Let $f _ { U } ( t )$ and $f _ { g _ { m } } ( t )$ ( )as the CPU frequency at time instant t for the UAV and GBS $g _ { m } .$ satisfying $f _ { U } ( t ) \leq f _ { U } ^ { \operatorname* { m a x } }$ and $f _ { g _ { m } } ( t ) \leq f _ { g _ { m } } ^ { \operatorname* { m a x } }$ , where $f _ { U } ^ { \mathrm { m a x } }$ and ( ) m( ) m  f maxg indicate the maximum CPU frequency of the servers at the Jgm mUAV and the GBS $g _ { m }$ . Moreover, let $C _ { U }$ as the number of CPU cycles required to execute per 1-bit data, which is determined by the task type [26].

Without loss of generality, we assume all the GBSs have the same height, denoted as $H _ { G }$ . Let $\mathbf { q } ( t ) = [ x ( t ) , y ( t ) ] \in \mathbb { R } ^ { 2 \times 1 }$ ( ) = [ ( ) ( )]represent the position of the UAV at time t. Then, the distance between the UAV and GBS $g _ { m }$ can be expressed as

$$
d _ { g _ { m } } ( t ) = \sqrt { ( H _ { U } - H _ { G } ) ^ { 2 } + \| \mathbf { q } ( t ) - \mathbf { w } _ { g _ { m } } \| ^ { 2 } } .\tag{1}
$$

The velocity of the UAV can be denoted as $\mathbf { v } ( t ) \triangleq { \dot { \mathbf { q } } } ( t )$ , and $\| \mathbf { v } ( t ) \| \leq V _ { \operatorname* { m a x } } , \forall t \in [ 0 , T ]$ , where $V _ { \mathrm { m a x } }$ ( ) = ( )is the maximum speed ( )value.

For the sake of statistically describing the UAV-GBS channels, a probabilistic LoS channel is adopted. The equation for the elevation angle between the GBS $g _ { m }$ and the UAV at time t is given by

$$
\theta g _ { m } ( t ) \triangleq \frac { 1 8 0 } { \pi } \arctan \left( \frac { H _ { U } - H _ { G } } { \lVert \mathbf { q } ( t ) - \mathbf { w } g _ { m } \rVert } \right) .\tag{2}
$$

According to [27], the probability of LoS between the UAV and GBS $g _ { m }$ at any time t can be expressed as

$$
\mathbb { P } _ { g _ { m } } ^ { L o S } ( t ) = C _ { 3 } + \frac { C _ { 4 } } { 1 + e ^ { - \left( C _ { 1 } + C _ { 2 } \theta _ { g _ { m } } ( t ) \right) } } ,\tag{3}
$$

where $C _ { 1 } , C _ { 2 } , C _ { 3 }$ and $C _ { 4 }$ are constants, and the specific values are determined by the propagation environment. Moreover, $C _ { 3 }$ and $C _ { 4 }$ satisfy the equation $C _ { 3 } + C _ { 4 } = 1$ [27].

+We introduce the binary variable $\lambda _ { g _ { m } } ( t )$ to denote the channel state between the UAV and GBS $g _ { m }$ m ( ). If $\lambda _ { g _ { m } } ( t ) = 1$ , it means m( ) =that the channel state between the UAV and GBS $g _ { m }$ is LoS; otherwise, it is NLoS. As a result, the channel gain $h g _ { m } ( t )$ between the UAV and GBS $g _ { m }$ m( )at any time t can be expressed as

$$
\begin{array} { r } { h g _ { m } ( t ) = \lambda g _ { m } ( t ) h _ { g _ { m } } ^ { L o S } ( t ) + ( 1 - \lambda g _ { m } ( t ) ) h _ { g _ { m } } ^ { N L o S } ( t ) , } \end{array}\tag{4}
$$

where $h _ { g _ { m } } ^ { L o S } ( t ) = \beta _ { 0 } d _ { g _ { m } } ^ { - \alpha } ( t )$ and $h _ { g _ { m } } ^ { N L o S } ( t ) = \mu \beta _ { 0 } d _ { g _ { m } } ^ { - \alpha _ { N L o S } } ( t )$ m ( ) = m( ) m ( ) = m ( )denote the channel power gain in LoS and NLoS states, respectively; Î± and $\alpha _ { N L o S }$ are the path loss components in LoS state and NLoS state, respectively, with $2 \le \alpha < \alpha _ { N L o S } \le 6 ; \beta _ { 0 }$ is the average channel power gain at $d = 1$ 6m, and Î¼ is an additional =factor caused by the NLoS link, with $\mu < 1$

1The maximum achievable rate for the link between UAV and the GBS $g _ { m }$ can be expressed as

$$
R g _ { m } \left( t \right) = B \log _ { 2 } \left( 1 + \frac { h g _ { m } \left( t \right) P \left( t \right) } { \sigma ^ { 2 } \Gamma } \right) ,\tag{5}
$$

where B is channel bandwidth in Hertz (Hz), $\sigma ^ { 2 }$ denotes the noise power at the GBS receiver, $P ( t )$ represents the transmitting power of the UAV, and $\Gamma > 1$ ( )denotes signal-to-noise ratio gap. Combining expressions (4) and (5), we can obtain the real-time channel-state-dependent achievable communication rate as

$$
\begin{array} { r } { R g _ { m } ( t ) = \lambda g _ { m } ( t ) R _ { g _ { m } } ^ { L o S } ( t ) + ( 1 - \lambda g _ { m } ( t ) ) R _ { g _ { m } } ^ { N L o S } ( t ) , } \end{array}\tag{6}
$$

where $\begin{array} { r } { R _ { g _ { m } } ^ { L o S } ( t ) = B \log _ { 2 } ( 1 + \frac { \hat { \gamma } P ( t ) } { ( d g _ { m } ( t ) ) ^ { \alpha } } ) } \end{array}$ and $R _ { g _ { m } } ^ { N L o S } ( t ) =$ $\begin{array} { r } { B \log _ { 2 } ( 1 + \frac { \mu \hat { \gamma } P ( t ) } { ( d _ { q _ { m } } ( t ) ) ^ { \alpha _ { N L o S } } } ) } \end{array}$ denote the achievable communicalog (1 + gm NLoS )tion rates in LoS condition and NLoS condition, respectively, and $\begin{array} { r } { \hat { \gamma } \overset { \Delta } { = } \frac { \beta _ { 0 } } { \sigma ^ { 2 } \Gamma } } \end{array}$ . However, it is hard to obtain the real channel Ë =state information during the period, we only know the channel distribution information. Thus, we consider the expected communication rate. According to (3) and (6), we have

$$
\begin{array} { r } { \mathbb { E } \left[ R _ { g _ { m } } ( t ) \right] = \mathbb { P } _ { g _ { m } } ^ { L o S } ( t ) R _ { g _ { m } } ^ { L o S } ( t ) + \left( 1 - \mathbb { P } _ { g _ { m } } ^ { L o S } ( t ) \right) R _ { g _ { m } } ^ { N L o S } ( t ) . } \end{array}\tag{)(7}
$$

We notice that the expression (7) is a highly complex function that is intractable to analyze. Therefore, we replace this function with its lower bound by using the approximation method in [27], which can be written as

$$
\begin{array} { l } { \displaystyle \mathbb { E } \left[ R _ { g _ { m } } ( t ) \right] \geq \mathbb { P } _ { g _ { m } } ^ { L o S } ( t ) R _ { g _ { m } } ^ { L o S } ( t ) } \\ { \displaystyle = \left( C _ { 3 } + \frac { C _ { 4 } } { 1 + e ^ { - \left( C _ { 1 } + C _ { 2 } \theta g _ { m } ( t ) \right) } } \right) } \\ { \displaystyle \mathrm { ~ \ } \times B \log _ { 2 } \left( 1 + \frac { \hat { \gamma } P ( t ) } { \left( d g _ { m } ( t ) \right) ^ { \alpha } } \right) \triangleq \tilde { R } _ { g _ { m } } ( t ) . } \end{array}\tag{8}
$$

The time-division multiple access (TDMA) scheme is employed for the patrol UAV to connect with the GBSs. We use $\pmb { \xi } ( t ) = [ \xi _ { g _ { 1 } } ( t ) , \xi _ { g _ { 2 } } ( t ) , . . . , \xi _ { g _ { m } } ( t ) , . . . , \xi _ { g _ { M } } ( t ) ]$ as an indi-( )cator. For $\xi _ { g _ { m } } ( t ) = 1$ ( ) m( ) M ( ), it denotes that the GBS $g _ { m }$ is schedm( ) = 1uled to serve the UAV; otherwise, $\xi _ { g _ { m } } ( t ) = 0$ . Thus, we have $\begin{array} { r } { \sum _ { m = 1 } ^ { M } \xi _ { g _ { m } } ( t ) \leq 1 , \forall t \in [ 0 , T ] } \end{array}$ . Then, the number of aggregated m( ) 1 [0 ]offloading data of the UAV is presented as

$$
\widehat { R } _ { g _ { m } } \left( T _ { G } , \xi _ { g _ { m } } ( t ) , \mathbf { q } ( t ) \right) = \int _ { 0 } ^ { T _ { G } } \xi _ { g _ { m } } ( t ) \tilde { R } _ { g _ { m } } ( t ) d t .\tag{9}
$$

For the GBSs, the information causality constraint should be maintained, i.e., the amount of data processed by each GBS cannot exceed the amount of received data from the UAV at any time $T _ { G } \in [ 0 , T ]$ . The information-causality constraint can be [0 ]formulated as follows:

$$
\int _ { 0 } ^ { T _ { G } } \xi _ { g _ { m } } ( t ) \tilde { R } _ { g _ { m } } ( t ) d t \geq \int _ { 0 } ^ { T _ { G } } \frac { f _ { g _ { m } } ( t ) } { C _ { U } } d t ,\tag{10}
$$

where the left side of the expression in (10) represents the data offloaded by the UAV to GBS $g _ { m }$ from the start time to time $T _ { G }$ and the right side of the inequality represents the data calculated by GBS $g _ { m }$ during this time.

## B. Energy Consumption Model

There are three categories energy consumption for the patrol inspection system: the energy consumption for UAV computing, the energy consumption for data transmission, and the energy

consumption for UAV flight. For the data transmission energy consumption of the UAV, it can be presented as

$$
E t r a = \sum _ { m = 1 } ^ { M } \sum _ { k = 1 } ^ { K } \int _ { 0 } ^ { T _ { s _ { k } } } \xi _ { g _ { m } } ( t ) P ( t ) d t ,\tag{11}
$$

where $\begin{array} { r } { \int _ { 0 } ^ { T _ { s _ { k } } } \xi _ { g _ { m } } ( t ) P ( t ) d t } \end{array}$ denotes the communication energy m( ) ( )consumption between the UAV and GBS $g _ { m }$ during inspecting the cruise point $s _ { k }$

Based on [28], [29], the computation energy consumption of the UAV can be given as

$$
E _ { c o p } = \int _ { 0 } ^ { T } \kappa _ { U } f _ { U } ^ { 3 } ( t ) d t ,\tag{12}
$$

where $\kappa _ { U }$ denotes the effective capacitance coefficient of the UAV, which is related to the chip architecture of the processor.

Based on [30], [31], the propulsion energy consumption of the rotary-wing UAV can be modeled as

$$
\begin{array} { l } { \displaystyle E _ { f } = \int _ { 0 } ^ { T } \left( P _ { 0 } \left( 1 + \frac { 3 \left\| \mathbf { v } \left( t \right) \right\| ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) + \right. } \\ { \displaystyle \left. P _ { i } \left( \sqrt { 1 + \frac { \left\| \mathbf { v } \left( t \right) \right\| ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \left\| \mathbf { v } \left( t \right) \right\| ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { \frac { 1 } { 2 } } + \frac { 1 } { 2 } d _ { 0 } \rho s A \| \mathbf { v } ( t ) \| ^ { 3 } \right) d t , } \end{array}\tag{13}
$$

where the first term on the right side of the equation in (13) means the blade profile power, the second term is the induced power, and the third term denotes the parasite power. Specifically, $P _ { 0 }$ and $P _ { i }$ denote the blade profile power and induced power in hovering status, respectively. $U _ { t i p }$ denotes the tip speed of the rotor blade, and $v _ { 0 }$ is the mean rotor induced velocity in hover. $d _ { 0 }$ is the fuselage drag ratio, $\rho$ denotes the air density, and s and A are the rotor solidity and rotor disc area, respectively. Notice that an accurate energy consumption model for the rotary-wing UAV is still unavailable in literature. In this sense, the existing model in (13) is appropriate to characterize the UAVâs energy consumption in this stage.

Therefore, the total energy consumption of the UAV can be expressed as

$$
E _ { T o t a l } = E _ { c o p } + E _ { t r a } + E _ { f } .\tag{14}
$$

## C. Problem Statement

For the patrol inspection mission, the UAV should traverse all the cruise points to capture the data and complete the computations task within the reasonable time by consuming the minimum energy. Hence, we goal is to minimize the total energy consumption during operating the patrol inspection mission, by jointly optimizing the traverse order $\{ \eta ( k ) \}$ , communication scheduling $\{ \xi _ { g _ { m } } ( t ) \}$ , task completion time $\{ \dot { T } , t _ { s _ { \eta ( k ) } } \}$ , UAV trajectory $\{ \mathbf { q } ( t ) \}$ m( ), and CPU frequency $\{ f _ { U } ( t ) , f _ { g _ { m } } ( t ) \}$ . Therefore, ( ) ( ) m( )the original optimization problem can be formulated as

$$
\left( \mathrm { P 0 } \right) : \operatorname* { m i n } _ { \{ \eta ( k ) \} , \{ \mathfrak { q } ( t ) \} , \{ \theta _ { g _ { m } } ( t ) \} , t _ { s _ { \eta ( k ) } } , \atop { T , \left\{ \xi _ { g _ { m } } ( t ) \right\} , \left\{ f _ { U } ( t ) , f _ { g _ { m } } ( t ) \right\} } } E _ { T o t a l }
$$

$$
\mathrm { s . t . } \xi _ { g _ { m } } ( t ) \in \{ 0 , 1 \} , \sum _ { m = 1 } ^ { M } \xi _ { g _ { m } } ( t ) \leq 1 , \forall m , t \in [ 0 , T ] ,\tag{15a}
$$

$$
\sum _ { m = 1 } ^ { M } \int _ { t _ { s _ { \eta ( k ) } } } ^ { t _ { s _ { \eta ( k + 1 ) } } } \frac { f _ { g _ { m } } ( t ) } { C _ { U } } d t + \int _ { t _ { s _ { \eta ( k ) } } } ^ { t _ { s _ { \eta ( k + 1 ) } } } \frac { f _ { U } ( t ) } { C _ { U } } d t \ge Q _ { s _ { \eta ( k ) } } ,
$$

$$
\forall t \in [ t _ { s _ { \eta ( k ) } } , t _ { s _ { \eta ( k + 1 ) } } ] , k = 1 , . . . , K ,\tag{15b}
$$

$$
\int _ { 0 } ^ { T _ { G } } \xi _ { g _ { m } } ( t ) \tilde { R } _ { g _ { m } } ( t ) d t \geq \int _ { 0 } ^ { T _ { G } } \frac { f _ { g _ { m } } ( t ) } { C _ { U } } d t , \forall m ,\tag{15c}
$$

$$
\theta g _ { m } ( t ) = \frac { 1 8 0 } { \pi } \arctan \left( \frac { H \upsilon - H \cal { G } } { \| \mathbf { q } ( t ) - \mathbf { w } g _ { m } \| } \right) , \forall m ,\tag{15d}
$$

$$
0 \leq f _ { U } ( t ) \leq f _ { U } ^ { \operatorname* { m a x } } , \forall t \in [ 0 , T ] ,\tag{15e}
$$

$$
0 \leq f _ { g _ { m } } ( t ) \leq f _ { g _ { m } } ^ { \operatorname* { m a x } } , \forall m , t \in [ 0 , T ] ,\tag{15f}
$$

$$
| | \mathbf { \dot { q } } ( t ) | | \leq V _ { \operatorname* { m a x } } , \forall t \in [ 0 , T ] ,\tag{15g}
$$

$$
\mathbf { q } ( t _ { s _ { \eta ( k ) } } ) = \mathbf { w } _ { s _ { \eta ( k ) } } , k = 0 , . . . , K + 1 ,\tag{15h}
$$

$$
\mathbf { w } _ { s _ { \eta ( 0 ) } } = \mathbf { q } _ { I } , \quad \mathbf { w } _ { s _ { \eta ( K + 1 ) } } = \mathbf { q } _ { F } ,\tag{15i}
$$

$$
t _ { s _ { \eta ( 0 ) } } = 0 , ~ t _ { s _ { \eta ( K + 1 ) } } = T ,\tag{15j}
$$

where the constraint (15a) denotes the GBSs scheduling during the UAVâs data offloading. The constraint (15b) indicates that the cumulative amount of the data jointly processed by the patrol UAV and GBSs should be larger than the amount of the data captured by the UAV at the cruise point $s _ { \eta ( k ) }$ during the flight between two consecutive cruise points $s _ { \eta ( k ) }$ and $s _ { \eta ( k + 1 ) }$ The information causality constraint is presented in (15c). The constraints (15h), (15i) and (15j) ensure the patrol UAV traverses all the cruise points with the traverse order Î·.

The original optimization problem (P0) involves the design of traverse order Î·, the communication and computation resource allocation, and the UAV trajectory planning. The constraint (15b) is a piecewise function that is non-convex. Moreover, how to find the optimal traverse order Î· is a non-deterministic polynomial hard (NP-hard) problem. Therefore, the optimal solution is difficult to obtain directly. To deal with this issue, we decompose the original problem into two sub-problems: one is optimal transmission strategy design between two consecutive cruise points, the other one is the optimal traverse order among the cruise points. A novel traverse criterion is proposed to maintain the tradeoff between flight distance and data offloading efficiency. Moreover, the SCA and alternating optimization method are adopt to obtain an efficient solution for the resource allocation and trajectory design.

## III. TWO SUB-PROBLEMS AND PROPOSED SOLUTIONS

In order to make the original optimization problem more trackable, we propose a two-step successive algorithm to deal with it. First, considering the pre-determined transmission strategy and trajectory, we propose a novel method by using a weighted factor to design the traverse order for visiting the cruise points. Then, with the obtained traverse order, the transmission scheduling and trajectory design can be optimized. Via the two steps above, the original problem can be solved in an iterative manner.

## A. The Traverse Order Among Cruise Points

Notice that the UAVâs moving range is mainly determined by the traverse order of the cruise points. Therefore, a suitable traverse order would dramatically decrease the propulsion energy consumption of the UAV. Moreover, the patrol UAV not only collects the information at various cruise points, but also offloads the captured data to surrounding GBSs for further data processing. The traverse order between cruise point and GBSs determines the transmission rates and affects the performance of data offloading time for the UAV. Considering one patrol inspection mission, there are K traverse orders to be selected !for the UAV, which is dramatically large with the increase of K. Evidently, it is a challenging NP-hard problem. In this paper, we propose a novel criterion to investigate the traverse order for decreasing the total energy consumption.

First, based on the topology of cruise points and GBSs, a directed weighted graph is constructed and denoted as $\Psi \stackrel { \Delta } { = }$ $\{ V , L \}$ , where the vertex set V is presented by

$$
V = \{ s _ { 0 } , s _ { 1 } , s _ { 2 } , . . . , s _ { k } , . . . , s _ { K } , s _ { K + 1 } \} .\tag{16}
$$

For ease of expressions, let $s _ { 0 } = \mathbf q _ { I }$ and $\mathbf { \boldsymbol { s } } _ { K + 1 } = \mathbf { \boldsymbol { q } } _ { F }$ . The edge set L can be given by

$$
L = \{ ( s _ { i } , s _ { j } ) , i \neq j , i , j \in K \} .\tag{17}
$$

The weight of each edge is an important factor for the traverse order design. However, the optimal trajectory and resource management issues between each two cruise points are very difficult to be solved. For these issues, we have to deal with $K ( K + 1 )$ optimization problems, which has extremely com-( + 1)putation complexity. Therefore, we explore a novel scheme to find the optimal traverse order without large computation complexity. Considering the weighted value of the edge, there are two critical issues for the weight design, i.e., the UAVâs energy consumption and the rate of data offloading. Generally, the length of each edge would determine the energy consumption of the patrol UAVâs flight. Moreover, the topological construct between GBSs and each edge would affect the achievable offloading rate. The energy consumption for per bit offloading can efficiently characterize the data offloading performance and the energy efficiency. This parameter can evaluate the potential performance of the edges based on the topological construct between GBSs and each edge.

Therefore, we propose a novel weight factor for the edges among the cruise points, expressed as

$$
W ( s _ { i } , s _ { j } ) = Q _ { s _ { i } } * \frac { E _ { s _ { i } , s _ { j } } } { Q _ { s _ { i } , s _ { j } } } , \forall i , j \in \mathcal { K } , i \neq j ,\tag{18}
$$

where $E _ { s _ { i } , s _ { j } }$ denotes the energy consumption of the patrol UAV i jduring the edge $[ s _ { i } , s _ { j } ] , Q _ { s _ { i } , s _ { j } }$ denotes the actual throughput of [ ] i jthe data offloading for the patrol UAV during the edge $[ s _ { i } , s _ { j } ]$ [ ]Moreover, in order to avoid the amount of offloading data to exceed that of data $Q _ { s _ { i } }$ captured at the cruise point, the constraint

$Q _ { s _ { i } , s _ { j } } = \operatorname * { m i n } [ \hat { Q } _ { s _ { i } , s _ { j } } , Q _ { s _ { i } } ]$ should be satisfied, where $\hat { Q } _ { s _ { i } , s _ { j } }$ dei j = min[ i j i] i jnotes the throughput between the UAV and GBSs during the edge $[ s _ { i } , s _ { j } ]$

[ ]To ensure that the traverse order starts at cruise point $s _ { 0 }$ and ends at cruise point $s _ { K + 1 }$ , the following weights should be predefined:

$$
W \left( s _ { 0 } , s _ { K + 1 } \right) = + \infty ,\tag{19}
$$

$$
W \left( s _ { K + 1 } , s _ { k } \right) = + \infty ,\tag{20}
$$

$$
\begin{array} { r } { W \left( s _ { K + 1 } , s _ { 0 } \right) = 0 . } \end{array}\tag{21}
$$

It is indicated that, based on the directed graph, the ending point $s _ { K + 1 }$ should be directed to the starting point to construct the specific return traverse order. Then, the problem can be formulated as follows:

$$
( \mathrm { P 1 } ) : \qquad \operatorname* { m i n } \sum _ { i \in \mathcal { K } } \sum _ { j \in \mathcal { K } , i \neq j } \tau _ { i , j } W \left( s _ { i } , s _ { j } \right)
$$

$$
\mathrm { s . t . } \sum _ { i \in \mathcal { K } , i \neq j } \tau _ { i , j } = 1 , \forall j \in \mathcal { K } ,\tag{22a}
$$

$$
\sum _ { j \in \mathcal { K } , j \not = i } \tau _ { i , j } = 1 , \forall i \in \mathcal { K } ,\tag{22b}
$$

$$
\tau _ { i , j } \in \left\{ 0 , 1 \right\} , \forall i , j \in \mathcal { K } , i \neq j ,\tag{22c}
$$

$$
\tau _ { i , j } + \tau _ { j , i } \leq 1 , \forall i , j \in \mathcal { K } , i \neq j ,\tag{22d}
$$

$$
u _ { i } - u _ { j } + \left( K + 2 \right) \tau _ { i , j } \leq K + 1 ,
$$

$$
i , j \in \left\{ 1 , . . . , K + 1 \right\} , i \neq j ,\tag{22e}
$$

$$
u _ { 0 } = 1 ,\tag{22f}
$$

$$
2 \leq u _ { i } \leq K + 2 ~ i \in \mathcal { K } , i \geq 1 ,\tag{22g}
$$

where $\tau _ { i , j } , \forall i , j \in \mathcal { K } , i \neq j$ is introduced to indicate the choice of path. If $\tau _ { i , j } = 1$ =, it indicates that the UAV passes the directed = 1edge connecting i and $j ,$ otherwise it means that the UAV does not pass it. Besides, we introduce the auxiliary variable $u _ { i } , i \in$ $\kappa ,$ to denote the index of cruise point in the traverse order. The constraint (22e) is established for the elimination of the subloop excluding the initial location. The constraint (22f) is introduced to indicate that the order starts from the cruise point $s _ { 0 }$ . The constraint (22g) restricts the range of the visited indexes. Then, the problem (P1) can be solved as a weighted TSP issue. We can obtain the traverse order $\eta ( k )$ among the cruise points by applying the width/depth search criterion.

## B. The Optimal Transmission Strategy

Considering the determined traverse order among the cruise points, the optimal transmission strategy can be decomposed into $K + 1$ independent subproblems, i.e., the optimal resource management between two consecutive cruise points. In this subsection, we would tackle this optimization problem by jointly optimizing the flight duration time $T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } }$ , the patrol UAVâs trajectory q t , the CPU frequency ${ \dot { f } } _ { g _ { m } } ( t ) , f _ { U } ( t )$ , and the ( )scheduling factor $\{ \xi _ { g _ { m } } ( t ) \}$ m( ) ( )}. The optimization problem can be

formulated as

$$
\begin{array} { c c } { { } } & { { \displaystyle \operatorname* { m i n } _ { { } \atop { } \{ \bf { q } ( t ) \} , \{ \xi _ { g _ { m } } ( t ) \} , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } , \{ \theta _ { g _ { m } } ( t ) \} , } { E _ { T o t a l } [ t _ { s _ { \eta ( k ) } } , t _ { s _ { \eta ( k + 1 ) } } ] } } } \\ { { } } & { { \displaystyle \{ f _ { U } ( t ) , f _ { g _ { m } } ( t ) \} } } \end{array}\tag{P2}
$$

$$
\mathrm { s . t . } \xi _ { g _ { m } } ( t ) \in \{ 0 , 1 \} , \sum _ { m = 1 } ^ { M } \xi _ { g _ { m } } ( t ) \leq 1 ,
$$

$$
\forall m , t \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23a}
$$

$$
\sum _ { m = 1 } ^ { M } \int _ { 0 } ^ { T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } } \frac { f _ { g _ { m } } ( t ) } { C _ { U } } d t + \int _ { 0 } ^ { T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } } \frac { f _ { U } ( t ) } { C _ { U } } d t
$$

$$
\geq Q _ { s _ { \eta ( k ) } , \forall t } \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23b}
$$

$$
\int _ { 0 } ^ { T _ { G } } \xi _ { g _ { m } } ( t ) \tilde { R } _ { g _ { m } } ( t ) d t \geq \int _ { 0 } ^ { T _ { G } } \frac { f _ { g _ { m } } ( t ) } { C _ { U } } d t ,
$$

$$
\forall m , T _ { G } \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23c}
$$

$$
\theta g _ { m } ( t ) = \frac { 1 8 0 } { \pi } \arctan \left( \frac { H U - H G } { \lVert \mathbf { q } ( t ) - \mathbf { w } g _ { m } \rVert } \right) ,
$$

$$
\forall m , t \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23d}
$$

$$
0 \leq f _ { U } ( t ) \leq f _ { U } ^ { \operatorname* { m a x } } , \forall t \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23e}
$$

$$
0 \le f _ { g _ { m } } ( t ) \le f _ { g _ { m } } ^ { \operatorname* { m a x } } , \quad \forall m , t \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23f}
$$

$$
| | \dot { \mathbf { q } } ( t ) | | \leq V _ { \operatorname* { m a x } } , \forall t \in [ 0 , T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ] ,\tag{23g}
$$

$$
\begin{array} { r } { \mathbf q ( 0 ) = \mathbf w _ { s _ { \eta ( k ) } } , \mathbf q ( T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } ) = \mathbf w _ { s _ { \eta ( k + 1 ) } } , } \end{array}\tag{23h}
$$

where the constraint (23b) ensures that the UAV and GBSs should complete the task calculation at $s _ { \eta ( k ) }$ before the UAV arriving the next cruise point $s _ { \eta ( k + 1 ) }$ . There are continuous variables and binary variables in the optimization problem. In addition, the objective function and constraint (23c) are nonconvex. Therefore, the mixed-integer non-convex problem is still difficult to deal with. In order to solve this problem, we propose a path discrete technique and alternate optimization scheme. The specific details are introduced as follows:

1) Problem Reformulation: We adopt the path discretization technique to reformulate propblem (P2) based on [30], [32]. Specifically, the flight trajectory of the patrol UAV can be approximated by a finite number of line segments. As long as the length of the line segment is short enough, the distance between the UAV and the GBSs can be considered unchanged, and the channel gain between the UAV and the GBSs can be considered to maintain consistency. Compared to the time discretization scheme where the task completion time $T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } }$ Î· kis pre-determined, the path discretization scheme can be adopted to optimize the task completion time for each edge flight, which makes efficient use of the resources.

We discretize the UAV trajectory into N line segments, and the position of the UAV is represented by N waypoints and the trajectory can be discretized as $\{ \mathbf { q } [ n ] , 0 \leq n \leq N \}$ , with $\mathbf { q } [ 0 ] = \mathbf { w } _ { s _ { \eta ( k ) } }$ and $\mathbf { q } [ N ] = \mathbf { w } _ { s _ { \eta ( k + 1 ) } }$ [ ] 0. Time t can be replaced [0]with $\delta [ n ]$ Î· k [ ] = Î· k, which represents the time spent by the UAV along [ ]the nth line segment. Therefeore, the UAV trajectory and the task completion time can be approximated as $\{ \mathbf { q } [ n ] \} _ { n = 0 } ^ { N }$ and $\begin{array} { r } { T _ { s _ { \eta ( k ) } } ^ { s _ { \eta ( k + 1 ) } } = \sum _ { n = 1 } ^ { N } \delta [ n ] } \end{array}$ , respectively. Thus, we have the followÎ· k =ing constraint:

$$
| | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | \leq \Delta _ { \operatorname* { m a x } } , \forall n ,\tag{24}
$$

where $\Delta _ { \mathrm { m a x } }$ represents the maximum allowable distance be-Îtween two adjacent waypoints. In addition, in order to ensure that the UAV can fly to any cruising points, N needs to meet $N \Delta _ { \mathrm { m a x } } \geq \bar { D }$ , where D represents the maximum dis-Îtance between any two consecutive cruise points, i.e., $\bar { D } =$ max $\{ \| \mathbf { w } _ { s _ { \eta ( k + 1 ) } } - \mathbf { w } _ { s _ { \eta ( k ) } } \| \}$ , âk.

ax Î· k Î· kThe flight velocity of the UAV along the nth line segment is given by $\begin{array} { r } { \mathbf { v } [ n ] = \frac { \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] } { \delta [ n ] } , 1 \le n \le N } \end{array}$ . For $P ( t ) , f _ { g _ { m } } ( t )$ and $f _ { U } ( t )$ , their corresponding discrete forms can be written as $P [ n ] , f _ { g _ { m } } [ n ]$ and $f _ { U } [ n ]$ , respectively. The communication rate mbetween the UAV and GBS $g _ { m }$ along the nth line segment can be expressed as

$$
\begin{array} { l } { { \displaystyle \tilde { R } g _ { m } \left[ n \right] = \left( C _ { 3 } + \frac { C _ { 4 } } { 1 + e ^ { - \left( C _ { 1 } + C _ { 2 } \theta g _ { m } \left[ n \right] \right) } } \right) } } \\ { { \displaystyle \times B \mathrm { l o g } _ { 2 } \left( 1 + \frac { P \left[ n \right] \hat { \gamma } } { \left( \left( H \eta - H G \right) ^ { 2 } + \left. \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right. ^ { 2 } \right) ^ { \alpha / 2 } } \right) , } } \end{array}\tag{25}
$$

where $\theta g _ { m } [ n ] \stackrel { \Delta } { = } \frac { 1 8 0 } { \pi }$ arctan $\big ( \frac { H \boldsymbol { U } - H _ { G } } { \lVert \mathbf { q } [ n ] - \mathbf { w } _ { g _ { m } } \rVert } \big )$ . Let an non-negative parameter $\phi _ { g _ { m } } [ n ]$ mdenote the duration time for the GBS $g _ { m }$ m[ ]scheduled to serve the UAVâs offloading task on the nth line segment. Therefore, constraint (23a) can be reconstructed as $\bar { \sum _ { m = 1 } ^ { M } \phi _ { g _ { m } } [ n ] } \leq \delta [ n ]$

m [ ] [ ]Finally, we rewrite all the energy functions in discrete forms, expressed as

$$
\begin{array} { l } { { \displaystyle E _ { f } = \sum _ { n = 1 } ^ { N } \delta [ n ] \left( P _ { 0 } \left( 1 + \frac { 3 \left( \left\| \mathbf { v } [ n ] \right\| \right) ^ { 2 } } { U _ { t i p } ^ { 2 } } \right) + \right. } } \\ { { \displaystyle P _ { i } \left( \sqrt { 1 + \frac { \left( \left\| \mathbf { v } [ n ] \right\| \right) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { \left( \left\| \mathbf { v } [ n ] \right\| \right) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } + \frac { 1 } { 2 } d _ { 0 } \rho s A ( \left\| \mathbf { v } [ n ] \right\| ) ^ { 3 } \left. \right) , } } \end{array}\tag{26}
$$

$$
E _ { t r a } = \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } \phi _ { g _ { m } } [ n ] P [ n ] ,\tag{27}
$$

$$
E _ { c o p } = \sum _ { n = 1 } ^ { N } \delta [ n ] \kappa _ { U } ( f _ { U } [ n ] ) ^ { 3 } .\tag{28}
$$

As thus, we rewrite the formula of UAV flight energy consumption as

$$
\begin{array} { l } { { \displaystyle E _ { f } = P _ { 0 } \sum _ { n = 1 } ^ { N } \left( \delta [ n ] + \frac { 3 ( \varpi [ n ] ) ^ { 2 } } { \delta [ n ] U _ { t i p } ^ { 2 } } \right) } } \\ { { \displaystyle ~ + P _ { i } \sum _ { n = 1 } ^ { N } \left( \sqrt { ( \delta [ n ] ) ^ { 4 } + \frac { ( \varpi [ n ] ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( \varpi [ n ] ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } } \end{array}
$$

$$
+ \frac { 1 } { 2 } d _ { 0 } \rho s A \sum _ { n = 1 } ^ { N } \frac { ( \varpi [ n ] ) ^ { 3 } } { ( \delta [ n ] ) ^ { 2 } } ,\tag{29}
$$

where $\boldsymbol { \varpi } [ n ] = | | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | |$ represents the length of the [ ] = [ ] [ 1]UAV flying along the nth line segment. Besides, $I [ n ] =$ $\frac { \delta [ n ] f _ { U } [ n ] } { C _ { U } }$ denotes the size of data processed by the UAV in the nth line segment. Let $\begin{array} { r } { O _ { g _ { m } } [ n ] = \frac { \delta [ n ] f _ { g _ { m } } [ n ] } { C _ { U } } } \end{array}$ denote the data size calculated by GBS $g _ { m }$ m [ ] = Uat the nth time duration. As a result, we can get the expressions of $f _ { U } [ n ]$ and $f _ { g _ { m } } [ n ]$ with respect to $I [ n ]$ and $\begin{array} { r } { O _ { g _ { m } } [ n ] , \mathrm { i . e . , } f _ { U } [ n ] = \frac { C \phantom { } _ { U } I [ n ] } { \delta [ n ] } , f _ { g _ { m } } [ n ] = \frac { C \phantom { } _ { U } O _ { g _ { m } } [ n ] } { \delta [ n ] } } \end{array}$ [ ]Furthermore, $E _ { c o p }$ [ ] = m [ ] =can be written as the following form:

$$
E _ { c o p } = \sum _ { n = 1 } ^ { N } \frac { \kappa _ { U } C _ { U } ^ { 3 } \left( I \left[ n \right] \right) ^ { 3 } } { \left( \delta \left[ n \right] \right) ^ { 2 } } , \forall n .\tag{30}
$$

Based on the discussions above, we convert problem (P2) into a discrete form as follows:

$$
\begin{array} { r l r } { \mathrm { : } } & { { } \underset { \left\{ \mathbf { q } [ n ] \right\} , \{ \theta g _ { m } [ n ] \} , \{ \phi _ { g _ { m } } [ n ] , \delta [ n ] \} , } { \operatorname* { m i n } } } & { E _ { c o p } + E _ { t r a } + E _ { f } } \\ { \mathrm { } } & { { } } & { \left\{ I [ n ] , O g _ { m } [ n ] \right\} } \end{array}\tag{P3}
$$

$$
\mathrm { s . t . } \sum _ { m = 1 } ^ { M } \phi _ { g _ { m } } [ n ] \leq \delta [ n ] , \phi _ { g _ { m } } [ n ] \geq 0 , \forall m , n ,\tag{31a}
$$

$$
\phi _ { g _ { m } } [ N ] = 0 , { \cal O } _ { g _ { m } } [ 1 ] = 0 , \forall m ,\tag{31b}
$$

$$
\sum _ { n = 1 } ^ { N } I [ n ] + \sum _ { m = 1 } ^ { M } \sum _ { n = 1 } ^ { N } O _ { g _ { m } } [ n ] \geq Q _ { s _ { \eta ( k ) } } ,\tag{31c}
$$

$$
\sum _ { l = 1 } ^ { n - 1 } \phi _ { g _ { m } } [ l ] \tilde { R } _ { g _ { m } } [ l ] \geq \sum _ { l = 2 } ^ { n } O _ { g _ { m } } [ l ] , \forall m , \forall n = 2 , . . . , N ,\tag{31d}
$$

$$
\theta g _ { m } \left[ n \right] = \frac { 1 8 0 } { \pi } \arctan \left( \frac { H _ { U } - H _ { G } } { \left\| \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| } \right) , \forall m , n ,\tag{31e}
$$

$$
0 \leq \frac { C _ { U } I [ n ] } { \delta [ n ] } \leq f _ { U } ^ { \operatorname* { m a x } } , \forall n ,\tag{31f}
$$

$$
0 \leq \frac { C _ { U } O _ { g _ { m } } [ n ] } { \delta [ n ] } \leq f _ { g _ { m } } ^ { \operatorname* { m a x } } , \forall m , \forall n ,\tag{31g}
$$

$$
| | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | \leq \operatorname* { m i n } \{ V _ { \operatorname* { m a x } } \delta [ n ] , \Delta _ { \operatorname* { m a x } } \} ,\tag{ân,}
$$

(31h)

$$
\mathbf { q } [ 0 ] = \mathbf { w } _ { s _ { \eta ( k ) } } , \mathbf { q } [ N ] = \mathbf { w } _ { s _ { \eta ( k + 1 ) } } .\tag{31i}
$$

In problem (P3), the flight energy consumption $E f$ in the objective function is non-convex. Constraint (31b) takes into account the delay in data transmission. The constraint (31d) is a non-convex function with respect to the trajectory q n . [ ]Due to the the non-convexity, it is difficult to directly solve problem (P3). In order to address this problem, we propose an alternate optimization scheme. Specifically, the problem (P3) is divided into two sub-problems, and the locally optimal solution is obtained by alternately optimizing the two sub-problems.

2) Iterative Algorithm: In this part, we consider to decompose the problem (P3) into two sub-problems and deal with them alternatively. Specifically, with the predetermined the trajectory of the patrol UAV, the scheduling parameters $\{ \delta [ n ] \} , \{ \phi _ { g _ { m } } [ n ] \}$ ï¼ and $\{ I [ n ] , O _ { g _ { m } } [ n ] \}$ [ ] m [ ]can be optimized in the first sub-problem. [ ] m[ ]With the given scheduling parameters, we can optimize the trajectory $\{ \mathbf { q } [ n ] \}$ in the second sub-problem. In the following, we will introduce the specific details.

With the fixed UAV trajectory, the optimization problem (P3) is reformulated as

$$
\begin{array} { c } { { ( \mathrm { P 4 } ) : \displaystyle { \operatorname* { m i n } _ { \{ \phi _ { g _ { m } } [ n ] \} , \{ \delta [ n ] \} \{ I [ n ] , O _ { g _ { m } } [ n ] \} } } E _ { c o p } + E _ { t r a } + E _ { f } } } \\ { { \mathrm { s . t . } ( 3 1 \mathrm { a } ) - ( 3 1 \mathrm { d } ) , ( 3 1 \mathrm { f } ) - ( 3 1 \mathrm { h } ) . } } \end{array}\tag{32}
$$

In problem (P4), all the constraints satisfy convex constraint rules. However, the function $E _ { f }$ in the objective function is nonconvex with respect to $\delta [ n ]$ . Therefore, we introduce the slack variable Î¶ n to handle $E f$ ], satisfying the following equation:

$$
( \zeta [ n ] ) ^ { 2 } = \sqrt { ( \delta [ n ] ) ^ { 4 } + \frac { ( \varpi [ n ] ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( \varpi [ n ] ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } .\tag{33}
$$

We can transform the expression (33) as

$$
\frac { ( \delta [ n ] ) ^ { 4 } } { ( \zeta [ n ] ) ^ { 2 } } = ( \zeta [ n ] ) ^ { 2 } + \frac { ( \varpi [ n ] ) ^ { 2 } } { v _ { 0 } ^ { 2 } } .\tag{34}
$$

However, we still cannot deal with the (34) directly. Considering the RHS of expression in (34) involves $( \zeta [ n ] ) ^ { 2 }$ , which is a convex function with respect to $\zeta [ n ]$ . Furthermore, the LHS [ ]of the equation is jointly convex with respect to $\zeta [ n ]$ and $\delta [ n ]$ [ ] [ ]Hence, we adopt the SCA technique to obtain the lower bound of the RHS of (34), by performing the first-order Taylor expansion, expressed as

$$
\begin{array} { r l } & { ( \zeta [ n ] ) ^ { 2 } + \displaystyle \frac { ( \varpi [ n ] ) ^ { 2 } } { v _ { 0 } ^ { 2 } } } \\ & { \geq ( \zeta ^ { r } [ n ] ) ^ { 2 } + 2 \zeta ^ { r } [ n ] ( \zeta [ n ] - \zeta ^ { r } [ n ] ) + \displaystyle \frac { ( \varpi [ n ] ) ^ { 2 } } { v _ { 0 } ^ { 2 } } , } \end{array}\tag{35}
$$

where $\zeta ^ { r } [ n ]$ is the value of $\zeta [ n ]$ at the rth iteration, with $\zeta ^ { r } [ n ] \ge$ [ ]. By this, the function $E _ { f }$ [ ] [ ]is reformulated as a convex form. 0Then, the problem (P4) can be rewritten as

$$
\begin{array} { r l r } { \mathrm { ( P S ) } : } &  \displaystyle  \operatorname * { m i n } _ { \{ \phi _ { s m } [ n ] \} , \{ \delta [ n ] \} \} } \operatorname * { m i n } _ { \substack { f [ n ] , 0 , \eta _ { s m } [ n ] \} , \{ \zeta [ n ] \} } E _ { c o p } + E _ { t r a } } & \\ & { } & { \qquad + \left( P _ { 0 } \displaystyle { \sum _ { n = 1 } ^ { N } \left( \delta [ n ] + \frac { 3 ( \varpi [ n ] ) ^ { 2 } } { \delta [ n ] U _ { t i p } ^ { 2 } } \right) } + P _ { i } \displaystyle { \sum _ { n = 1 } ^ { N } \zeta [ n ] } \right. } \\ & { } & { \qquad \left. + \displaystyle { \frac { 1 } { 2 } } d _ { 0 } \rho s A \displaystyle { \sum _ { n = 1 } ^ { N } \frac { ( \varpi [ n ] ) ^ { 3 } } { ( \delta [ n ] ) ^ { 2 } } } \right) } \\ & { } & { \qquad \mathrm { s . t . } ~ ( 3 1 \Delta ) - ( 3 1 \mathrm { d } ) , ( 3 1 \mathrm { f } ) - ( 3 1 \mathrm { h } ) , } \end{array}\tag{6a}
$$

$$
\frac { ( \delta [ n ] ) ^ { 4 } } { ( \zeta [ n ] ) ^ { 2 } } \leq ( \zeta ^ { r } [ n ] ) ^ { 2 } + 2 \zeta ^ { r } [ n ] ( \zeta [ n ] - \zeta ^ { r } [ n ] )
$$

$$
c + \frac { ( \varpi [ n ] ) ^ { 2 } } { v _ { 0 } ^ { 2 } } ,\tag{36b}
$$

$$
\zeta [ n ] \geq 0 .\tag{36c}
$$

Problem (P5) is a convex optimization problem. We can use standard convex optimization tools such as CVX to solve problem (P5) to obtain the optimal values. It is noted that the rotated_lorentz transform can be adopted to reformulate $E _ { c o p }$ to adapt the CVX tool box.

The second sub-problem is aiming to optimize the UAVâs trajectory ${ \bf q } [ n ]$ with the fixed $\{ \delta [ n ] \} , \{ \phi _ { g _ { m } } [ n ] \}$ , and $\{ I [ n ] , O _ { g _ { m } } [ n ] \}$ [ ] [ ] m [ ]. The second sub-problem is expressed as

$$
\begin{array} { r l }  { \displaystyle ( \mathrm { P } 6 ) : \operatorname* { m i n } _ { \{ \mathrm { q } [ n ] \} , \mathrm { t } \theta _ { m } [ n ] \} } } & { { \displaystyle R _ { 0 \to 1 } ^ { N } \left( \delta [ n ] + \frac { 3 ( \varpi [ n ] ) ^ { 2 } } { \delta [ n ] } U _ { t , i p } ^ { ( 2 ) } \right) } } \\ { { } } & { { ~ + ~ P _ { i } \sum _ { n = 1 } ^ { N } \left( \sqrt { ( \delta [ n ] ) ^ { 4 } + \frac { ( \varpi [ n ] ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( \varpi [ n ] ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } \right) ^ { 1 / 2 } } } \\ { { } } & { { ~ + \displaystyle \frac { 1 } { 2 } d _ { 0 } \rho s A \sum _ { n = 1 } ^ { N } \frac { ( \varpi [ n ] ) ^ { 3 } } { ( \delta [ n ] ) ^ { 2 } } } } \\ { { } } & { { ~ \mathrm { s . t . ~ } ( 3 1 \mathrm { d } ) , ( 3 1 \mathrm { e } ) , ( 3 1 \mathrm { h } ) , ( 3 1 \mathrm { i } ) . } } \end{array}\tag{7}
$$

The objective function in problem (P6) is only related to the flight energy consumption of the UAV, which is depended on the trajectory ${ \bf q } [ n ]$ . Moreover, the second term of the objective [ ]function is non-convex with respect to ${ \bf q } [ n ]$ . Similar to problem (P4), we introduce the slack variable $\varsigma [ n ]$ to deal with this [ ]problem. According to (33), we rewrite (34) as

$$
\frac { ( \delta [ n ] ) ^ { 4 } } { ( \varsigma [ n ] ) ^ { 2 } } = ( \varsigma [ n ] ) ^ { 2 } + \frac { | | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } } .\tag{38}
$$

Note that the RHS of (38) are convex with regard to $\varsigma [ n ]$ and $| | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | |$ [ ]. Thus, the RHS of (38) can be lower-[ ] [ 1]bounded by the first-order Taylor approximation at $\varsigma [ n ]$ and $| | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | |$ , expressed by

$$
\begin{array} { r l r } {  { \big ( \varsigma [ n ] \big ) ^ { 2 } + \frac { | | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } } } } \\ & { } & \\ & { \geq \big ( \varsigma ^ { r } [ n ] \big ) ^ { 2 } + 2 \varsigma ^ { r } [ n ] ( \varsigma [ n ] - \varsigma ^ { r } [ n ] ) - \frac { | | \mathbf { q } ^ { r } [ n ] - \mathbf { q } ^ { r } [ n - 1 ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } } } \\ & { } & \\ & { + \frac { 2 } { v _ { 0 } ^ { 2 } } ( \mathbf { q } ^ { r } [ n ] - \mathbf { q } ^ { r } [ n - 1 ] ) ^ { T } ( \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] ) , } & { ( 3 9 ) } \end{array}
$$

where $\mathbf { q } ^ { r } [ n ]$ represents the value of ${ \bf q } [ n ]$ for the problem in the [ ]rth iteration, and $( { \bf q } ^ { r } [ n ] - { \bf q } ^ { r } [ n - 1 ] ) ^ { \dot { T } }$ represents the transpose of $( \mathbf { q } ^ { r } [ n ] - \mathbf { q } ^ { r } [ n - 1 ] )$ ] [ 1]). In the constraint (31d), it is worth noting (that $\tilde { R } _ { g _ { m } } [ n ]$ is a convex function with respect to $\lVert \mathbf { q } [ n ] - \mathbf { w } _ { g _ { m } } \rVert ^ { 2 }$ and $e ^ { - ( C _ { 1 } + C _ { 2 } \theta g _ { m } [ n ] ) }$ . The first-order Taylor approximation is adopted to deal with $\tilde { R } _ { g _ { m } } [ n ]$ with the given local points ${ \bf q } ^ { r } [ n ]$ and $\theta _ { g _ { m } } ^ { r } [ n ]$ m [ ] [ ]in the rth iteration. As a result, we obtain the lower bound $\hat { R } _ { g _ { m } } ^ { L } [ n ]$ of $\tilde { R } _ { g _ { m } } [ n ]$ , i.e.,

$$
\tilde { R } g _ { m } \left[ n \right] = \left( C _ { 3 } + \frac { C _ { 4 } } { 1 + e ^ { - \left( C _ { 1 } + C _ { 2 } \theta g _ { m } \left[ n \right] \right) } } \right)
$$

$$
\times B \log _ { 2 } \left( 1 + \frac { P \left[ n \right] \hat { \gamma } } { \left( \left( H _ { U } - H _ { G } \right) ^ { 2 } + \left. \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right. ^ { 2 } \right) ^ { \alpha / 2 } } \right)
$$

$$
\begin{array} { r l } & { \geq \hat { C } _ { g _ { m } } ^ { r } [ n ] - \hat { X } _ { g _ { m } } ^ { r } [ n ] \left( e ^ { - \left( C _ { 1 } + C _ { 2 } \theta g _ { m } [ n ] \right) } - \hat { J } _ { g _ { m } } ^ { r } [ n ] \right) } \\ & { \quad - \hat { I } _ { g _ { m } } ^ { r } [ n ] \left( \left\| \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| ^ { 2 } - \left\| \mathbf { q } ^ { r } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| ^ { 2 } \right) } \\ & { \stackrel { \Delta } { = } \hat { R } _ { g _ { m } } ^ { L } [ n ] , } \end{array}\tag{40}
$$

where

$$
\hat { C } _ { g _ { m } } ^ { r } [ n ] = \left( C _ { 3 } + \frac { C _ { 4 } } { 1 + \hat { J } _ { g _ { m } } ^ { r } [ n ] } \right) B \log _ { 2 } \left( 1 + \frac { P \left[ n \right] \hat { \gamma } } { \left( \hat { A } _ { g _ { m } } ^ { r } [ n ] \right) ^ { \alpha / 2 } } \right) \ :\tag{41}
$$

$$
\hat { X } _ { g _ { m } } ^ { r } [ n ] = \frac { C _ { 4 } B \log _ { 2 } \bigg ( 1 + \frac { \hat { \gamma } P [ n ] } { \big ( \hat { A } _ { g _ { m } } ^ { r } [ n ] \big ) ^ { \alpha / 2 } } \bigg ) } { \bigg ( 1 + \hat { J } _ { g _ { m } } ^ { r } [ n ] \bigg ) ^ { 2 } } ,\tag{42}
$$

$$
\hat { I } _ { g _ { m } } ^ { r } [ n ] = \frac { \left( C _ { 3 } + \frac { C _ { 4 } } { 1 + \hat { J } _ { g _ { m } } ^ { r } [ n ] } \right) B \left( \alpha / 2 \right) \log _ { 2 } ( e ) P \left[ n \right] \hat { \gamma } } { \hat { A } _ { g _ { m } } ^ { r } [ n ] \left( \left( \hat { A } _ { g _ { m } } ^ { r } [ n ] \right) ^ { \alpha / 2 } + P \left[ n \right] \hat { \gamma } \right) } ,\tag{43}
$$

$$
\hat { J } _ { g _ { m } } ^ { r } [ n ] = e ^ { - \big ( C _ { 1 } + C _ { 2 } \theta _ { g _ { m } } ^ { r } [ n ] \big ) } ,\tag{44}
$$

$$
\hat { A } _ { g _ { m } } ^ { r } [ n ] = \left( H _ { U } - H _ { G } \right) ^ { 2 } + \big \| \mathbf { q } ^ { r } [ n ] - \mathbf { w } _ { g _ { m } } \big \| ^ { 2 } .\tag{45}
$$

Let $\hat { R } _ { g _ { m } } ^ { L } [ n ]$ replace $\tilde { R } _ { g _ { m } } [ n ]$ in the constraint (31d), we obtain m [ ]the following expression:

$$
\sum _ { l = 1 } ^ { n - 1 } \phi _ { g _ { m } } [ l ] \hat { R } _ { g _ { m } } ^ { L } [ n ] \ge \sum _ { l = 2 } ^ { n } O _ { g _ { m } } [ l ] , \forall m , \forall n = 2 , . . . , N .\tag{46}
$$

Moreover, the constraint (31e) is tricky to handle. According to the work [27], the constraint (31e) can be transformed into a new form, given by

$$
\theta { { g } _ { m } } \left[ n \right] \leq \frac { 1 8 0 } { \pi } \arctan \left( \frac { H U - H G } { \left\| \mathbf { q } \left[ n \right] - \mathbf { w } _ { { { g } _ { m } } } \right\| } \right) , \forall m , n .\tag{47}
$$

Note that the constraint (47) is also non-convex, we can obtain the lower bound of the RHS of the constraint (47) by the firstorder Taylor expansion, which leads to the following expression:

$$
\begin{array} { r l } & { \arctan \left( \frac { H _ { U } - H _ { G } } { \left\| \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| } \right) \ge \arctan \left( \frac { H _ { U } - H _ { G } } { \left\| \mathbf { q } ^ { r } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| } \right) } \\ & { - \frac { H _ { U } - H _ { G } } { \hat { A } _ { g _ { m } } ^ { r } \left[ n \right] } \left( \left\| \mathbf { q } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| - \left\| \mathbf { q } ^ { r } \left[ n \right] - \mathbf { w } _ { g _ { m } } \right\| \right) \triangleq \psi _ { g _ { m } } \left[ n \right] . } \end{array}\tag{48}
$$

As as result, problem (P6) can be approximately reformulated as

$$
\begin{array} { l } { { \displaystyle ( \mathrm { P } ^ { 7 } ) : \operatorname* { m i n } _ { \{ \mathbf { q } [ n ] \} , \{ \theta _ { g _ { m } } [ n ] \} , \{ \varsigma [ n ] \} } P _ { 0 } } } \\ { { \displaystyle \sum _ { n = 1 } ^ { N } \left( \delta [ n ] + \frac { 3 | | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | ^ { 2 } } { \delta [ n ] U _ { t i p } ^ { 2 } } \right) } } \end{array}
$$

Algorithm 1: Joint Optimization Algorithm for Problem (P0).

1: Traverse order Design: Define the initial trajectory and resource management criteria for the edges between each two cruise points, including straight fligh, fixed power, and resource allocation.

2: Calculate the weight factor $W ( s _ { i } , s _ { j } )$ , and obtain the traversal order $\eta ( k )$ ( )by utilizing the weighted directed TSP criterion.

3: Trajectory and Resource management: Set a feasible initial flight trajectory of the UAV $\{ \mathbf { q } ^ { 0 } [ n ] \}$ , give the slack variables $\zeta ^ { r } [ n ] , \varsigma ^ { r } [ n ]$

4: Let $r = 0 .$

=5: repeat

6: With given $\{ \mathbf { q } ^ { r } [ n ] , \delta ^ { r } [ n ] \}$ , solve sub-problem (P5) to [ ] [ ]obtain task completion time $\{ \delta ^ { r + 1 } [ n ] \}$ ï¼ communication scheduling $\{ \bar { \phi } _ { q _ { m } } ^ { r + 1 } [ \bar { n } ] \}$ , and the amount of calculated tasks $\{ I ^ { r + 1 } [ n ] , \stackrel { \sim } { O } _ { g _ { m } } ^ { r + 1 } [ n ] \}$

7: With given $\{ \mathbf q ^ { r } [ n ] \} , \{ \delta ^ { r + 1 } [ n ] \}$ m, and $\{ \phi _ { g _ { m } } ^ { r + 1 } [ n ] \}$ , solve [ ] [ ] m [ ]sub-problem (P7) to find the optimized UAV trajectory $\{ \mathbf { q } ^ { r + 1 } [ n ] \}$

8: Update $r = r + 1$

9: until

10: The total energy value $E _ { T o t a l }$ converges to a preset accuracy $\varepsilon \left( \varepsilon > 0 \right)$

$$
+ P _ { i } \sum _ { n = 1 } ^ { N } \varsigma [ n ] + \frac { 1 } { 2 } d _ { 0 } \rho s A \sum _ { n = 1 } ^ { N } \frac { | | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | ^ { 3 } } { ( \delta [ n ] ) ^ { 2 } }
$$

$$
\mathrm { s . t . } \sum _ { l = 1 } ^ { n - 1 } \phi _ { g _ { m } } [ l ] \hat { R } _ { g _ { m } } ^ { L } [ l ] \geq \sum _ { l = 2 } ^ { n } O _ { g _ { m } } [ l ] , \forall m , n ,\tag{49a}
$$

$$
\theta g _ { m } \left[ n \right] \leq \frac { 1 8 0 } { \pi } \psi _ { g _ { m } } \left[ n \right] , \forall m , n ,\tag{49b}
$$

$$
| | \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] | | \leq \operatorname* { m i n } \{ V _ { \mathrm { m a x } } \delta [ n ] , \Delta _ { \mathrm { m a x } } \} , \forall n ,\tag{49c}
$$

$$
\mathbf { q } [ 0 ] = \mathbf { w } _ { s _ { \eta ( k ) } } , \mathbf { q } [ N ] = \mathbf { w } _ { s _ { \eta ( k + 1 ) } } ,\tag{49d}
$$

$$
\frac { ( \delta [ n ] ) ^ { 4 } } { ( \varsigma [ n ] ) ^ { 2 } } \leq ( \varsigma ^ { r } [ n ] ) ^ { 2 } + 2 \varsigma ^ { r } [ n ] ( \varsigma [ n ] - \varsigma ^ { r } [ n ] ) -
$$

$$
\frac { | | \mathbf { q } ^ { r } [ n ] - \mathbf { q } ^ { r } [ n - 1 ] | | ^ { 2 } } { v _ { 0 } ^ { 2 } } +
$$

$$
\frac { 2 } { v _ { 0 } ^ { 2 } } ( \mathbf { q } ^ { r } [ n ] - \mathbf { q } ^ { r } [ n - 1 ] ) ^ { T } ( \mathbf { q } [ n ] - \mathbf { q } [ n - 1 ] ) , \forall n ,\tag{49e}
$$

$$
{ \mathsf { S } } [ n ] \geq 0 , { \forall n . }\tag{49f}
$$

Problem (P7) is a standard convex optimization problem that can be solved by adopting the convex optimization tools such as the CVX solver. In problem (P7), by introducing the slack parameters $( \varsigma [ n ] ) ^ { 2 } , { \hat { R } _ { g _ { m } } } ^ { - } [ n ]$ and $\psi _ { g _ { m } } [ n ]$ , we can obtain the upper bound of $\begin{array} { r } { ( \sqrt { ( \delta [ n ] ) ^ { 4 } + \frac { ( \varpi [ n ] ) ^ { 4 } } { 4 v _ { 0 } ^ { 4 } } } - \frac { ( \varpi [ n ] ) ^ { 2 } } { 2 v _ { 0 } ^ { 2 } } ) } \end{array}$ and the lower bound of $\tilde { R } _ { g _ { m } } [ n ]$ . Therefore, the solution obtained by solving m [ ]the problem (P7) also satisfies the constraints in problem (P6).

<!-- image-->  
(a) Round tour

<!-- image-->  
(bï¼ The TSP criterion

<!-- image-->  
(cï¼ The EETSP criterion

<!-- image-->  
(d) The proposed scheme

Fig. 2. Optimized UAV trajectories with $Q _ { s _ { k } } = 2 0 0 { \mathrm { M b i t s } } .$  
<!-- image-->  
(a) Round tour

<!-- image-->  
(bï¼ The TSP criterion

<!-- image-->  
(cï¼The EETSP criterion

<!-- image-->  
(d) The proposed scheme

Fig. 3. Optimized UAV trajectories with $Q _ { s _ { k } } = 5 5 0 { \mathrm { M b i t s } } .$  
<!-- image-->  
(a) Round tour

<!-- image-->  
(bï¼ The TSP criterion

<!-- image-->  
(cï¼ The EETSP criterion

<!-- image-->  
(d) The proposed scheme  
Fig. 4. Optimized UAV speed with different initialization schemes and data size $Q _ { s _ { k } }$

3) Proposed Algorithm: Via the analysis above, the original optimization problem is solved efficiently. The proposed algorithm is summarized in Algorithm 1.

In Algorithm 1, the complexity of steps 6 and 7 for solving the (P5) and (P7) can be expressed as $\mathcal { O } ( \bar { R _ { i } } n ^ { 3 } \log ( { \varepsilon _ { i } } ^ { - 1 } ) )$ , where $R _ { i }$ and $\varepsilon _ { i }$ ( log( ))denote the number of iterations and the accuracy of the Algorithm 1 in optimizing the ith segment, respectively. As a result, the overall complexity of Algorithm 1 is expressed as $\mathcal { O } ( 2 ( K + 1 ) R _ { i } ( N + 1 ) ^ { 3 } \log ( \dot { \varepsilon } _ { i } - 1 ) )$

## IV. SIMULATION RESULTS

In this section, we evaluate the performance of the proposed algorithm. It is assuemed that the altitudes of the GBSs and UAV are 25 m and 100 m [33], respectively. The CPU frequencies at the UAV and GBSs are 0.8 GHz and 8 GHz, respectively. Other related simulation parameters are summarized in Table I. Using the black solid circles to represent the starting and ending points, the rectangular box to represent the cruise point, and the pink pentagram to represent the GBSs.

In realistic patrol inspection scenario, the traditional round tour and TSP criterion are usually adopted to initialize the UAVâs trajectory. For the round tour criterion, the UAV traverses the cruise points successively according to the value of row/column coordinates. For the TSP criterion, it aims to minimize the total flight distance of the patrol UAV, then the traverse order can be obtained by applying the depth/width search method. In this work, we propose an EETSP criterion to design the traverse order, in which the energy efficiency of the data transmission is the weighted factor for each edge, with the goal of maximizing the total energy efficiency of the system. Therefore, we adopt these three criteria as the benchmark methods to evaluate the performance of the proposed algorithm.

First, we investigate the optimal flight trajectory of the patrol UAV under different amount of collecting data. As shown in Figs. 2 and 3, four patrol UAVâs trajectories are designed with different traverse criteria, with the given data size $Q _ { s _ { k } } = 2 0 0$ Mbits and $Q _ { s _ { k } } = 5 5 0$ Mbits.

TABLE I RELATED SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Notation</td><td rowspan=1 colspan=1>Definition</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Vmax</td><td rowspan=1 colspan=1>Maximum speed of the UAV (m/s)</td><td rowspan=1 colspan=1>50[33]</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Channel bandwidth (MHz)</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> ${ \underline { { \beta _ { 0 } } } }$ </td><td rowspan=1 colspan=1>The average channel power gain at $\overline { { d _ { 0 } = 1 } } \mathrm { m }$ (dB)</td><td rowspan=1 colspan=1>-50</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \sigma ^ { 2 } } }$ </td><td rowspan=1 colspan=1>The noise power at the receiver (dBm)</td><td rowspan=1 colspan=1>-100</td></tr><tr><td rowspan=1 colspan=1> $\alpha$ </td><td rowspan=1 colspan=1>Path loss component</td><td rowspan=1 colspan=1>2.2[33]</td></tr><tr><td rowspan=1 colspan=1> $\varepsilon$ </td><td rowspan=1 colspan=1>Convergence accuracy</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 3 } } }$ </td></tr><tr><td rowspan=1 colspan=1> $C \boldsymbol { U }$ </td><td rowspan=1 colspan=1>Therequired numberof CPUcycles per bit (cycles/bit)</td><td rowspan=1 colspan=1> $1 0 0 0 ~ [ 3 4 ]$ </td></tr><tr><td rowspan=1 colspan=1> $\kappa _ { U }$ </td><td rowspan=1 colspan=1>Theeffective capacitance coefficientof theUAV</td><td rowspan=1 colspan=1> $\overline { { 1 0 ^ { - 2 7 } \ [ 3 5 ] } }$ </td></tr><tr><td rowspan=1 colspan=1> $\overbrace { P \left[ n \right] } ^ { - }$ </td><td rowspan=1 colspan=1>UAVtransmitting power(W)</td><td rowspan=1 colspan=1>0.1</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { 0 } } }$ </td><td rowspan=1 colspan=1>Blade profile power in hovering status (W)</td><td rowspan=1 colspan=1> ${ \overline { { 7 9 . 8 ~ [ 3 6 ] } } }$ </td></tr><tr><td rowspan=1 colspan=1> $P _ { i }$ </td><td rowspan=1 colspan=1>Induced power in hovering status (W)</td><td rowspan=1 colspan=1>88.6</td></tr><tr><td rowspan=1 colspan=1> $v _ { 0 }$ </td><td rowspan=1 colspan=1>Mean rotor induced velocity in hover (m/s)</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1> $d _ { 0 }$ </td><td rowspan=1 colspan=1>Fuselage dragratio</td><td rowspan=1 colspan=1>0.6</td></tr><tr><td rowspan=1 colspan=1> $\rho$ </td><td rowspan=1 colspan=1>Air density $\overline { { ( \mathrm { k g / m } ^ { 3 } ) } }$ </td><td rowspan=1 colspan=1>1.2</td></tr><tr><td rowspan=1 colspan=1> $s$ </td><td rowspan=1 colspan=1>Rotor solidity</td><td rowspan=1 colspan=1>0.05</td></tr><tr><td rowspan=1 colspan=1> $\overline { { A } }$ </td><td rowspan=1 colspan=1>Rotor disc area $\overline { { ( \mathrm { m } ^ { 2 } ) } }$ </td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1> $\overline { { U _ { t i p } } }$ </td><td rowspan=1 colspan=1>Tip speed of the rotor blade (m/s)</td><td rowspan=1 colspan=1>120[36]</td></tr></table>

k = 550For the scenario with $Q _ { s _ { k } } = 2 0 0 { \mathrm { M b i t s } }$ , the UAV traverses the k = 200cruise points in round order based on the value of the column coordinate of them, as shown in Fig. 2(a). Since the distance between two successive cruise points is long enough, the UAV can just operate a straight-line flight with an energy-efficient speed, then the data offloading demand can be easily satisfied. However, the total energy consumption would be large due to the long flight duration. In Fig. 2(b), based on the TSP criterion, the total flight distance for the UAV is minimized, and the trajectory is optimized according to the topology construct between GBSs and cruise points, such as the segment $s _ { 4 } - s _ { 2 }$ , where the flight path is biased towards the nearby GBSs. In Fig. 2(c), the energy efficiency is maximized during the flight. It observes that the traverse order is different from the TSP criterion. However, due to the amount of data is not enough large, there is little room for trajectory optimization, e.g., the segments $s _ { 5 } - s _ { 2 } , s _ { 2 } - s _ { 3 }$ and $s _ { 6 } - s _ { 4 }$ are straight-flight path. In Fig. 2(d), it shows that the proposed criterion is flexible to adapt different sizes of the offloading data. For this scenario, the optimal trajectory degrades as the TSP criterion. The energy consumption of these four schemes are 75.979 kJ, 55.002 kJ, 58.061 kJ, and 55.002 kJ, which indicates that the proposed scheme is superior to the round tour and the EETSP criterion.

For the scenario with $Q _ { s _ { k } } = 5 5 0 ~ \mathrm { M b i t s }$ , the topology conkstruct between the GBSs and edges performs the dominate factor for the trajectory design when increasing the offloading data, as shown in Fig. 3. Specifically, in Fig. 3(a) and (b), the optimal trajectories of the UAV tend to the nearby GBSs to achieve better channel quality. In Fig. 3(c), driven by the EETSP criterion, the UAVâs trajectory is closer to the GBSs to obtain higher rate performance. During the segments $s _ { 1 } - s _ { 5 } , s _ { 6 } - s _ { 4 } ,$ , and $s _ { 4 } - \mathbf q _ { F }$ ï¼ the UAV hovers over the GBSs to offload the data. In Fig. 3(d), our proposed criterion degrades as the EETSP criterion to obtain the minimized energy consumption. The energy consumption for the four methods in this scenario are 98.812 kJ, 86.198 kJ, 75.231 kJ, and 75.231 kJ. This indicates that the EETSP criterion is more suitable for the larger data offloading scenario, and shows that the proposed method is compatible for this scenario with the optimal solution.

<!-- image-->  
(a) $Q _ { s _ { k } } = 2 0 0$ Mbits

<!-- image-->  
(b) $Q _ { s _ { k } } = 5 5 0$ Mbits  
Fig. 5. Chart for communication scheduling with different task size $Q _ { s _ { k } }$

Moreover, the UAVâs speed and mission completion time are plotted in Fig. 4. In the scenario of $Q _ { s _ { k } } = 2 0 0$ Mbits, due to the k = 200small amount of offloading data, the UAV tends to traverse all the cruise points. For the scenario $Q _ { s _ { k } } = 5 5 0 ~ \mathrm { M b i t s }$ , in order k = 550to get more high quality channel gain, the UAV flies to the GBSs with a large speed, and the speed would be decreased to obtain more time to offload the task when closing to the GBSs. From this picture, it is shown that our proposed scheme can save more energy through the trajectory optimization. It is worth mentioning that the patrol UAV collects data with a powerful HD camera or laser radar, thus the operation time is quite short. As a result, the data collection time is ignored in this paper, and the flight speed of the UAV at any patrol point is an approximately non-zero constant.

The communication scheduling charts of $Q _ { s _ { k } } = 2 0 0$ Mbits and $Q _ { s _ { k } } = 5 5 0$ kMbits are shown in Fig. 5. For the scenario with $Q _ { s _ { k } } = \mathrm { 2 0 0 M b i t s }$ , there is a communication interruption during k = 200the flight, which indicates that the UAV does not offload data during this time. It is because that the distance between UAV and

<!-- image-->  
(a) $Q _ { s _ { k } } = 2 0 0 \mathrm { M b i t s }$

<!-- image-->  
(b) $Q _ { s _ { k } } = 5 5 0 \mathrm { M b i t s }$

Fig. 6. Average communication rate with different initialization schemes and data size $Q _ { s _ { k } }$  
<!-- image-->  
Fig. 7. Convergence of different schemes with $Q _ { s _ { k } } = 5 5 0 { \mathrm { M b i t s } } .$

GBSs is too large to offload the data. In other words, when the computation task is relatively small, the UAV would compute the task by itself, which is more energy-efficient. However, when the computation task is heavy, the UAV would keep communicating with the GBSs. Thus, the UAV needs to make full utilization of the time to offload the data to the GBSs, which can be shown by Fig. 6(b). Moreover, it can be observed that the UAV would maintain communication with the nearest GBS in each sub-time slot, which helps the UAV obtain the best rate performance.

<!-- image-->  
(a) Total system energy consumption

<!-- image-->  
(bï¼ Mission completion time  
Fig. 8. Energy consumption and mission completion time versus task size $Q _ { s _ { k } }$

Fig. 6 shows the average communication rate between the UAV and the GBSs. We use the parameter $R ^ { a v e } [ n ] =$ $\begin{array} { r } { \sum _ { m = 1 } ^ { M } \phi _ { g _ { m } } [ n ] \tilde { R } g _ { m } [ n ] / \delta [ n ] } \end{array}$ to indicate the performance of m[ ] m[ ] [ ]communication rate. Fig. 6(a) and (b) show that the average communication rate of the EETSP criterion is higher than that of the TSP criterion and round tour. The reason for this phenomenon is that the EETSP criterion considers the energy efficiency of communication as a whole. The TSP criterion only concentrates on the flight distance and neglects the communication rate. The average communication rate of the round tour trajectory is larger than the TSP scheme at a certain time. However, it should be noted that the purpose of patrol inspection is to traverse all the cruise points. For the scenario with a low value of $Q _ { s _ { k } }$ , the kdata offloading is easily accomplished when the UAV flies from the last cruise point to the next cruise point. Moreover, in this case, there are some communication interruptions between UAV and GBSs under the EETSP criterion and round tour method, which means that there is no need for data offloading when the channel state is terrible. For the scenario with a high value of $Q _ { s _ { k } }$ , the data offloading is a hard task for the optimal design. kIn this case, the EETSP criterion would be a better choice for the optimal traverse order design. Overall, the proposed scheme is compatible with these two scenarios, and can help the patrol UAV obtain the energy-efficient trajectory.

<!-- image-->  
(a) The TSP criterion

<!-- image-->  
(bï¼The EETSP criterion

<!-- image-->  
(c) The proposed scheme  
Fig. 9. Optimized UAV trajectories with $Q _ { s _ { k } } = [ 3 0 , 1 6 0 , 6 8 0 , 1 5 0 , 6 6 0 , 2 0 0 , 5 0 , 5 9 0 , 6 0 0 , 5 6 0 ] \mathrm { M b i t s }$

Fig. 7 shows the convergence of the alternating optimization algorithm with different traversal order schemes for $Q _ { s _ { k } } = 5 5 0$ k = 550Mbits. It can be seen from this figure that the curves first decrease, and then gradually converge to a level after several iterations, which proves the convergence of the proposed algorithm. In addition, the energy consumption obtained by the proposed algorithm is always minimum compared to other schemes, which is sufficient to indicate the feasibility and superiority of the proposed scheme.

Next, we evaluate the performance of energy consumption and completion time under different amounts of data. Note that to highlight the advantages of the proposed scheme, the exhaustive optimal energy scheme is added in this paper, which first obtains the minimum energy between any two cruising points, and then finds the overall minimum value by permutation. Fig. 8(a) depicts the energy consumption performance for the different task sizes. Notice that when the data size of the task is less than about 280 Mbits, the TSP criterion can obtain the best performance compared to round tour and the EETSP criterion. It is close to the exhaustive optimal energy and the proposed solution. This is because that the patrol UAVâs flying energy consumption is the dominate factor for the optimal trajectory design, and the communication rate requirement can be easily satisfied. When the task data size is larger than 280 Mbits, the data communication design would be the dominate factor for the optimal trajectory design. The EETSP criterion obtains a higher communication performance by considering the topology construct between GBSs and cruise points. Then, the performance of the EETSP criterion is close to the exhaustive optimal solution. Moreover, we adopt a fixed trajectory (FT) scheme that is the initial trajectory for the EETSP criterion. For the FT, we only optimize the scheduling parameter with the fixed trajectory. From Fig. 8, it can be found that the trajectory optimization design can save more energy in the scenarios with large data size. Overall, the proposed algorithm is applicable in these two scenarios, and achieves a comparable performance with the exhaustive optimum. In addtion, Fig. 8(b) illustrates the relationship between task completion time and data size, and shows that the proposed criteria owns the superiority in different cases.

Finally, we consider the scenario where the cruise points have different data sizes. Due to the single criterion for the edge weight design, the TSP criterion and EETSP criterion cannot be compatible for the different cruise points to obtain the optimal solution. Fortunately, our proposed novel edge weight factor can comprehensively evaluate the effect of the flight distance and communication rate for the trajectory design. In Fig. 9, we consider the scenario that there are 10 cruising points which have different sizes. The optimal trajectories are different based on the three traverse order criteria. It can be observed that our proposed method flexibly fits the offloading demand of these cruising points. For the task of lower offloading data, the UAV just takes straight flight between two successive points, such as the segments $s _ { 4 } - s _ { 5 } , s _ { 6 } - s _ { 3 } , s _ { 7 } - s _ { 1 0 }$ . This can save more propulsion energy for UAVâs flight. Based on the EETSP criterion, the segments $s _ { 4 } - s _ { 8 } , s _ { 6 } - s _ { 5 }$ would be selected due to the high energy efficiency through flying over the GBSs. However, the cruise points $s _ { 4 }$ and $s _ { 6 }$ do not have a large number of offloading data. Thus, the propulsion energy consumption is not optimal for this criterion. In other side, for the TSP criterion, although the segments $s _ { 1 0 } - s _ { 9 }$ and $s _ { 8 } - \mathbf { q } _ { F }$ have the small flight distance, while the GBSs are far away from the flight path, which decreases the throughput performance and increases the energy consumption. It can be shown that the large offloading demand forces the UAV to fly close to the GBSs. The energy consumption for the TSP criterion, the EETSP criterion, and the proposed method are 136.667 kJ, 153.695 kJ, and 129.509 kJ, respectively. Moreover, the completion time for the TSP criterion, the EETSP criterion, and the proposed method is 855 s, 976 s, and 830 s, respectively, which indicates that the proposed scheme is superior to the other benchmark schemes.

## V. CONCLUSION

In this paper, we investigated the energy consumption problem of a cellular-connected UAV-MEC system in patrol inspection scenarios. Considering the data offloading of the multiple cruise points, we aimed to minimize the energy consumption of the network. A novel edge weighted factor was proposed to design the traverse order among the cruise points. It was compatible with minimizing the propulsion energy and maximizing the task data offloading efficiency. Moreover, by adopting the graph theory and path discretization technique, a joint traverse order, UAV trajectory, and resource allocation optimization method was proposed. It was a two-step algorithm with low computation complexity. Numerical results demonstrated the effectiveness of the proposed solution, where the energy consumption performance of the proposed criterion was superior to the TSPbased and EETSP-based schemes. The proposed algorithm in this paper was compatible with different offloading tasks of the cruise points, which can be efficiently applied in practical implementation.

## REFERENCES

[1] N. Zhao et al., âUAV-Assisted emergency networks in disasters,â IEEE Wireless Commun., vol. 26, no. 1, pp. 45â51, Feb. 2019.

[2] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surveys Tuts., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[3] Y. Zeng, J. Lyu, and R. Zhang, âCellular-connected UAV: Potential, challenges, and promising technologies,â IEEE Wireless Commun., vol. 26, no. 1, pp. 120â127, Feb. 2019.

[4] Y. Zeng, X. Xu, S. Jin, and R. Zhang, âSimultaneous navigation and radio mapping for cellular-connected UAV with deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 20, no. 7, pp. 4205â4220, Jul. 2021.

[5] H. Zhu et al., âOn the end-to-end latency of cellular-connected UAV communications,â in Proc. Eur. Conf. Antennas Propag., Dusseldorf, Germany, 2021, pp. 1â5.

[6] C. Zhan and Y. Zeng, âEnergy minimization for cellular-connected UAV: From optimization to deep reinforcement learning,â IEEE Trans. Wireless Commun., vol. 21, no. 7, pp. 5541â5555, Jul. 2022.

[7] D. Yang, Q. Dan, L. Xiao, C. Liu, and L. Cuthbert, âAn efficient trajectory planning for cellular-connected UAV under the connectivity constraint,â China Commun., vol. 18, no. 2, pp. 136â151, Feb. 2021.

[8] M. Hua, Y. Huang, Y. Sun, Y. Wang, and L. Yang, âEnergy optimization for cellular-connected UAV mobile edge computing systems,â in Proc. IEEE Int. Conf. Commun. Syst., Chengdu, China, 2018, pp. 1â6.

[9] M. Hua, Y. Huang, Y. Wang, Q. Wu, H. Dai, and L. Yang, âEnergy optimization for cellular-connected multi-UAV mobile edge computing systems with multi-access schemes,â J. Commun. Inf. Netw., vol. 3, no. 4, pp. 33â44, Dec. 2018.

[10] X. Cao, J. Xu, and R. Zhang, âMobile edge computing for cellularconnected UAV: Computation offloading and trajectory optimization,â in Proc. IEEE Int. Workshop Signal Process. Adv. Wireless Commun., Kalamata, Greece, 2018, pp. 1â5.

[11] T. Bai, J. Wang, Y. Ren, and L. Hanzo, âEnergy-efficient computation offloading for secure UAV-edge-computing systems,â IEEE Trans. Veh. Technol., vol. 68, no. 6, pp. 6074â6087, Jun. 2019.

[12] Z. Lv, J. Hao, and Y. Guo, âEnergy minimization for MEC-enabled cellular-connected UAV: Trajectory optimization and resource scheduling,â in Proc. IEEE Conf. Comput. Commun. Workshops, Toronto, ON, Canada, 2020, pp. 478â483.

[13] Y. Liu, H. N. Dai, Q. Wang, M. K. Shukla, and M. Imran, âUnmanned aerial vehicle for internet of everything: Opportunities and challenges,â Comput. Commun., vol. 155, pp. 66â83, Apr. 2020.

[14] IEEE Guide for Unmanned Aerial Vehicle-Based Patrol Inspection System for Transmission Lines, IEEE Standard 2821â2020, pp. 1â49, Nov. 2020.

[15] Q. Chen et al., âDesign of patrol inspection system for special equipment based on UAV,â in Proc. 3rd World Conf. Mech. Eng. Intell. Manuf., Shanghai, China, 2020, pp. 143â146.

[16] X. Zhang and L. Duan, âOptimal patrolling trajectory design for multi-UAV wireless servicing and battery swapping,â in Proc. IEEE Globecom Workshops, Waikoloa, HI, USA, 2019, pp. 1â6.

[17] Z. Changxin et al., âUAV electric patrol path planning based on improved ant colony optimization-A\* algorithm,â in Proc. IEEE Int. Conf. Elect. Eng. Big Data Algorithms, Changchun, China, 2022, pp. 1374â1380.

[18] L. Cheng, L. Zhong, S. Tian, and J. Xing, âTask assignment algorithm for road patrol by multiple UAVs with multiple bases and rechargeable endurance,â IEEE Access, vol. 7, pp. 144 381â144 397, 2019.

[19] P. GuimarÃ£es de Vargas, K. S. Kappel, J. L. Marins, T. M. Cabreira, and P. R. Ferreira, âPatrolling strategy for multiple UAVs with recharging stations in unknown environments,â in Proc. Latin Amer. Robot. Symp. Braz. Symp. Robot. Workshop Robot. Educ., Rio Grande, Brazil, 2019, pp. 346â351.

[20] L. Morando, C. T. Recchiuto, and A. Sgorbissa, âSocial drone sharing to increase the UAV patrolling autonomy in emergency scenarios,â in Proc. IEEE Int. Conf. Robot. Hum. Interact. Commun., Naples, Italy, 2020, pp. 539â546.

[21] X. Pang, J. Tang, N. Zhao, X. Y. Zhang, and Y. Qian, âEnergy-efficient design for mmWave-enabled NOMA-UAV networks,â Sci. China Inf. Sci., vol. 64, Apr. 2021, Art. no. 140303.

[22] Y. K. Tun, Y. M. Park, N. H. Tran, W. Saad, S. R. Pandey, and C. S. Hong, âEnergy-efficient resource management in UAV-assisted mobile edge computing,â IEEE Commun. Lett., vol. 25, no. 1, pp. 249â253, Jan. 2021.

[23] X. Qin, Z. Song, Y. Hao, and X. Sun, âJoint resource allocation and trajectory optimization for multi-UAV-assisted multi-access mobile edge computing,â IEEE Wireless Commun. Lett., vol. 10, no. 7, pp. 1400â1404, Jul. 2021.

[24] Z. Hu, F. Zeng, Z. Xiao, B. Fu, H. Jiang, and H. Chen, âComputation efficiency maximization and QoE-provisioning in UAV-enabled MEC communication systems,â IEEE Trans. Netw. Sci. Eng., vol. 8, no. 2, pp. 1630â1645, Second Quarter 2021.

[25] Y. Wang, M. Sheng, X. Wang, L. Wang, and J. Li, âMobile-edge computing: Partial computation offloading using dynamic voltage scaling,â IEEE Trans. Commun., vol. 64, no. 10, pp. 4268â4282, Oct. 2016.

[26] Y. Ding et al., âOnline edge learning offloading and resource management for UAV-assisted MEC secure communications,â IEEE J. Sel. Topics Signal Process., vol. 17, no. 1, pp. 54â65, Jan. 2023.

[27] C. You and R. Zhang, âHybrid offline-online design for UAV-enabled data harvesting in probabilistic LoS channels,â IEEE Trans. Wireless Commun., vol. 19, no. 6, pp. 3753â3768, Jun. 2020.

[28] Y. Xu, T. Zhang, Y. Liu, D. Yang, L. Xiao, and M. Tao, âUAV-assisted MEC networks with aerial and ground cooperation,â IEEE Trans. Wireless Commun., vol. 20, no. 12, pp. 7712â7727, Dec. 2021.

[29] T. Zhang, Y. Xu, J. Loo, D. Yang, and L. Xiao, âJoint computation and communication design for UAV-assisted mobile edge computing in IoT,â IEEE Trans. Ind. Inform., vol. 16, no. 8, pp. 5505â5516, Aug. 2020.

[30] Y. Zeng, J. Xu, and R. Zhang, âEnergy minimization for wireless communication with rotary-wing UAV,â IEEE Trans. Wireless Commun., vol. 18, no. 4, pp. 2329â2345, Apr. 2019.

[31] C. Zhan and H. Lai, âEnergy minimization in Internet-of-Things system based on rotary-wing UAV,â IEEE Wireless Commun. Lett., vol. 8, no. 5, pp. 1341â1344, Oct. 2019.

[32] H. Wang, J. Wang, G. Ding, J. Chen, F. Gao, and Z. Han, âCompletion time minimization with path planning for fixed-wing UAV communications,â IEEE Trans. Wireless Commun., vol. 18, no. 7, pp. 3485â3499, Jul. 2019.

[33] C. Zhan and Y. Zeng, âEnergy-efficient data uploading for cellularconnected UAV systems,â IEEE Trans. Wireless Commun., vol. 19, no. 11, pp. 7279â7292, Nov. 2020.

[34] C. Zhan, H. Hu, X. Sui, Z. Liu, and D. Niyato, âCompletion time and energy optimization in the UAV-enabled mobile-edge computing system,â IEEE Internet of Things J., vol. 7, no. 8, pp. 7808â7822, Aug. 2020.

[35] Y. Zhou et al., âSecure communications for UAV-enabled mobile edge computing systems,â IEEE Trans. Commun., vol. 68, no. 1, pp. 376â388, Jan. 2020.

[36] Z. Sun, D. Yang, L. Xiao, L. Cuthbert, F. Wu, and Y. Zhu, âJoint energy and trajectory optimization for UAV-enabled relaying network with multi-pair users,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 3, pp. 939â954, Sep. 2021.

<!-- image-->  
Dingcheng Yang received the BS degree in electronic engineering and the PhD degree in space physics from Wuhan University, Wuhan, China, in 2006 and 2012, respectively. He is currently a professor with the Information Engineering School, Nanchang University, Nanchang, China. He had published more than 50 papers including journal papers on the IEEE Transactions on Vehicular Technology, etc. and conference papers such as IEEE GLOBECOM. His research interests include cooperation communications, IoT/cyber-physical systems, UAV communications,  
and wireless resource management.

<!-- image-->

Jun Wang received the BS degree in electronic information science and technology from Chizhou University, Chizhou, China, in 2020. He is currently working toward the masterâs degree with the Information Engineering School, Nanchang University, Nanchang, China. His research interests include MEC technology, UAV communications, and wireless resource management.

<!-- image-->

Yu Xu received the PhD degree from the School of Information and Communication Engineering, Beijing University of Posts and Telecommunications, China, in 2023. He is currently a lecturer with the Information Engineering School, Nanchang University, Nanchang, China. His research interests include mobile edge computing, UAV communications, integrated sensing and communication, and reconfigurable intelligence surface.

<!-- image-->

<!-- image-->

Fahui Wu received the BS degree from the School of Information Engineering and the PhD degree from the School of Mechanical and Electrical Engineering, Nanchang University, Nanchang, China, in 2014 and 2020, respectively. He is currently a college lecturer with the Information Engineering School, Nanchang University. His research interests include convex optimization, AI empowered wireless communication, and UAV communications.

Lin Xiao received the PhD degree in electronic engineering from the School of Electronic Engineering and Computer Science, Queen Mary University of London, London, U.K., in 2010. After that, she worked with China Academy of Telecommunication Research, MITT for one year. She is currently a professor with the Information Engineering School, Nanchang University, Nanchang, China. Her research interests include wireless communication and networks, in particular, UAV network planning and optimization, radio resource management, relay, and cooperation communication.

<!-- image-->

Tiankui Zhang (Senior Member, IEEE) received the BS degree in communication engineering and the PhD degree in information and communication engineering from the Beijing University of Posts and Telecommunications (BUPT), China, in 2003 and 2008, respectively. Currently, he is a professor with the School of Information and Communication Engineering, BUPT. His research interests include wireless communication networks, mobile edge computing and caching, signal processing for wireless communication, content centric networks. He had published more than 100 papers including journal papers on the IEEE Journal on Selected Areas in Communications, IEEE Transaction on Communications, etc., and conference papers, such as IEEE GLOBECOM and IEEE ICC.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_14_img_1.jpeg|page_14_img_1]]
3. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_15_img_1.jpeg|page_15_img_1]]
4. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_15_img_2.jpeg|page_15_img_2]]
5. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_15_img_3.jpeg|page_15_img_3]]
6. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_15_img_4.jpeg|page_15_img_4]]
7. [[../extracted_images/Yang 等 - 2024 - Energy Efficient Transmission Strategy for Mobile /page_15_img_5.jpeg|page_15_img_5]]

---

