# Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems

Ming Tao , Member, IEEE, Xueqiang Li , Jie Feng , Member, IEEE, Dapeng Lan, Member, IEEE, Jun Du , Senior Member, IEEE, and Celimuge Wu , Senior Member, IEEE

Abstractâ In the paradigm of ubiquitous edge computing, with those advantages, e.g., high mobility, fast response, flexibility and controllability, and low cost of use, Unmanned Aerial Vehicles (UAVs) could be used not only as relays to assist with data collection, but also as computing power nodes to process uncomplicated computational workloads from ground users. Especially, UAVs could be employed to provide alternative computing power resources in field, lake, post-disaster and other complex regional environments. In this paper, to address the issue of computing power scheduling in UAVs empowered aerial computing systems, a scenario where multiple UAVs from the same departure station cooperatively fly over hovering points and achieve the data collection and computation in a decentralized manner is investigated. Nevertheless, due to limited onboard battery capacities of UAVs and diverse service requests of ground users, it is necessary to optimize energy efficiency and service fairness for improving mission execution capabilities of UAVs and the quality of service (QoS) experienced by ground users, and a joint optimization problem of energy efficiency and service fairness is formulated. Through considering complex coupling associations among the departure station, flight paths and hovering points of UAVs, the problem is investigated from the trajectory planning of UAVs and the location planning for both the departure station and hovering points. Proving investigations to be Markov decision processes (MDP), multi-agent cooperation approaches are proposed as promising solutions, and simulation results have been shown to demonstrate that the performance

achieved by the proposal outperforms that achieved by schemes commonly used in literatures.

Index Termsâ Aerial computing systems, computing power scheduling, multi-agent cooperation, energy efficiency, service fairness.

## I. INTRODUCTION

WITH the emergence of mobile applications, thosecompute-intensive and delay-sensitive intelligent ser- compute-intensive and delay-sensitive intelligent services impose great pressures on energy and computing power of mobile terminals, and diverse service requests could not be well satisfied with the limited resource capacities. To address these challenges, being different from the centralized processing method adopted by the traditional cloud computing, mobile edge computing (MEC) as an emerging distributed network structure could sink the computing tasks of mobile terminals to the network edge, which effectively shorten the transmission delay of computing data and relieve the computing pressure of the core network, so as to meet the high-reliability and low-delay computing requests of mobile terminals, and greatly improve the computing capability of the network [1]. Nevertheless, due to the difficulty of deploying edge computing related infrastructures in fixed locations in some complex environments, e.g., field, lake, and post-disaster, mobile edge computing has been an effective alternative solution [2].

In the last decade, through being integrated into wireless sensing networks for Internet of Things (IoT) applications of air-ground collaboration, UAVs are popular to be used as relays to assist with the sensing data collection, and mobile access points to carry out emergency rescue [3], [4]. Nowadays, promoted by the enhancement of on-chip computing power, UAVs also could be taken as computing power nodes to process uncomplicated computational workloads from ground users [5], [6]. Therefore, in the paradigm of ubiquitous edge computing, with the advantages of high mobility, fast response, flexibility and controllability, and low cost of use, UAVs assisted aerial computing systems could break through the limitations of traditional edge computing applications in terms of inflexible deployment, constrained geographical location and coverage capabilities, and could greatly expand the application of edge computing through improving the network computing capability and the QoS experienced by ground users.

<!-- image-->  
Fig. 1. The diagram of investigations in this paper.

Being different from terrestrial edge computing power nodes deployed in fixed locations, UAVs as mobile computing power nodes could fly over the target area and cooperatively achieve the data collection and computation in a decentralized manner. Nevertheless, due to limited onboard battery capacities embedded in UAVs and diverse service requests put forwarded by ground users, operating the UAVs assisted aerial computing systems in optimal fashion still remains a challenging issue that is necessary to be reasonably solved [7]. To this end, to address the issue of computing power scheduling in UAVs empowered aerial computing systems, a scenario where multiple UAVs fly from the same departure station to achieve the cooperation is investigated in this paper. Additionally, since the cooperation of flight paths of UAVs is directly influenced by the departure station, and the efficiency of data collection and computation is directly influenced by flight paths and hovering points, the departure station, flight paths and hovering points of UAVs have obvious and complex coupling associations, the fundamental challenge is to determine the optimal departure station, flight paths and hovering points. To address these challenges, with the main contributions summarized as follows, a joint optimization of energy efficiency and service fairness is investigated in this paper to improve mission execution capabilities of UAVs and the service experience of ground users. The diagram of investigations is shown in Fig. 1.

â¢ Being different from existing proposals, both data collection and computation are investigated in multi-UAV assisted aerial computing systems, and with the consideration of limited onboard battery capacity of UAV and diverse service requests of ground users, both energy efficiency and service fairness are jointly optimized for computing power scheduling.

â¢ For improving mission execution capabilities of UAVs and the QoS experienced by ground users, achieving the energy efficiency is formulated as jointly minimizing the energy utilization and the standard deviation of energy consumption, and achieving the service fairness is formulated as jointly minimizing the maximum in minimum hop counts between ground users and their candidate serving UAVs, and the standard deviation of hop counts.

â¢ Through fully considering complex coupling associations among the departure station, flight paths and hovering points of UAVs, the trajectory planning of UAVs is investigated to maximize the energy efficiency, which is proven to be a fully observable discrete MDP, and an approach of multi-agent cooperative Q-learning is proposed as a promising solution.

â¢ Also, the location planning for the departure station and hovering points of UAVs is investigated to maximize the service fairness among ground users, which is proven to be a partially observable continuous MDP, an approach of policy optimization based multi-agent cooperative deep reinforcement learning within the architecture of Actor-Critic is proposed as a promising solution.

The rest of this paper is organized as follows. In Section II, a brief review of UAV applications is firstly stated, on the basis of the analysis, research motivations of this paper are discussed. In Section III, basic definitions in the considered scenario are clearly given. In Section IV, formulations of investigated problems including optimization objectives and constraints are comprehensively discussed. In Section V, through proving investigated problems to be Markov decision processes, multi-agent cooperative approaches are proposed as promising solutions. In Section VI, experiments and analysis are addressed to demonstrate the effectiveness of investigations. In Section VII, the summarization and future work are discussed.

## II. RELATED WORK AND MOTIVATIONS

Benefiting from advantages of high mobility, fast response, flexibility and controllability, and low cost of use, UAVs have been widely employed in various fields, e.g., intelligent agriculture, intelligent transportation, disaster management, environment monitoring and construction of smart city, through acting as mobile access points for data collection and mobile computing nodes for data computation. In the meantime, the involved theoretical and technical challenges also have attracted extensive attention from academia and industry, and some research progress has been obtained in some specific applications with different considerations.

## A. UAV-Assisted Data Collection

With high mobility and wide coverage, UAVs have providing new opportunities and conveniences for effective and timely data collection. Through reviewing application scenarios and key technologies, Wei et al., discussed the mathematical model of UAV assisted data collection, the mode of UAV assisted data collection and some open problems [8]. To minimize the energy consumption and completion time while achieving reliable data collection, through using a general fading channel model for sensor-UAV links, Zhan et al., investigated the trajectory planning and sensor wake-up schedule [9]. Yuan et al., also proposed a joint scheme of UAV trajectory and user scheduling to achieve the completion time minimization of data collection [10].

Through considering the sensing data collection with an UAV on a straight line, Gong et al., jointly optimized data collection intervals, the UAVâs speed, and sensorsâ transmission powers to achieve the minimization of UAV flight time [11]. With the UAV flight control, Li et al., also considered the limited energy of UAV to achieve the fairness of data collection in the scenario that the UAV could not achieve direct data collection for all devices [12]. Through designing fully or partially data collection problems, a scheme of maximizing the accumulative volume of data collection with energy-constrained UAV was also investigated in [13]. With the consideration of energy-constrained IoT devices and target data upload deadlines, Samir et al., formulated the joint optimization of UAV trajectory and radio resource allocation as a mixed integer non-convex problem to maximize the number of served IoT devices [14]. While considering the UAVs flying range, communication range and energy constraints, a scheme was also proposed in [15] to improve the network resource allocation fairness and efficiency.

To maintain the freshness of data collection, through comprehensively considering UAV trajectory and time for energy harvesting, Hu et al., designed a scheme to minimize the average Age of Information (AoI) [16]. With the consideration that the total AoI depends on the UAV flight time and the data collection time at hovering points, Zhu et al., designed a joint optimization problem of selecting hovering points and determining the visiting order to hovering points [17]. Gao et al., also jointly optimized the sensor uploading time, the UAV flight time and the data offloading time to improve the information freshness [18].

However, those proposals in literatures focused on simplified 2-D scenarios with perfect channel state information and generally formulated the challenges as no-convex problems solved by heuristic algorithms. Unlike those proposals, with the consideration of practical 3-D scenarios with imperfect channel state information and the usage of deep reinforcement learning approach, Wang et al., investigated the optimization of UAV trajectory to minimize the completion time of data collection [19], Nguyen et al., optimized the UAV trajectory planning while maximizing the collected data volume to enhance the throughput [20], Chen et al., jointly optimized the UAV trajectory and user association to maximize the network throughput and energy efficiency [21], Fan et al., also jointly optimized the UAV trajectory, sensors scheduling and discrete phase shifts of the reconfigurable intelligent surface (RIS) to minimize the AoI and maintain the data freshness [22].

## B. UAV-Assisted Mobile Edge Computing

MEC as an emerging paradigm has been demonstrated to promise low latency and low energy services. In extreme scenarios where terrestrial infrastructures are unavailable, with a certain on-chip computing power, UAV acting as a mobile edge computing node, could be taken as an alternative [23].

Through jointly optimizing the computing power, user associations and ground user locations, Shah et al., presented a maximization of UAV deployment and computation efficiency [24]. Taking the temporarily passing UAV as the relay and edge computing node to provide computing power service, Yang et al., proposed a learning based channel allocation and task offloading strategy [25]. To address the joint optimization of queue-based computation offloading and adaptive computing resource allocation, Goudarzi et al., proposed an computing resource allocation model optimized by cooperative evolutionary computation methods [26]. Through considering those constraints, e.g., resources budgets, computation deadline, data compression ratio and UAVs trajectory limitations, Cheng et al., investigated an offloading scheme to improve the overall computing performance and energy efficiency [27].

In UAV-mounted MEC systems, to assume that priorities of computation tasks from different users are time-varying and incorporated, Zhou et al., proposed a priority-aware resource scheduling problem which was solved by the deep Q-learning algorithm optimizing the UAV hotspot selection and task offloading [28]. For avoiding the problem of overloading and congestion at a UAV while achieving the minimization of makespan, Hoa et al., presented a cooperative multi-hop offloading problem solved by a deep reinforcement learning approach [29]. With the consideration of long-term constraints on queue stability and computational delay, Hoang et al., proposed an online resource allocation strategy, and used deep reinforcement learning approaches to achieve the minimization of overall energy consumption [30].

## C. Motivations

From above reviews, UAV-assisted data collection and computation as an on-demand decision making problem is NP-hard that could be solved by various optimization methods with different effectiveness. With the acknowledgement that those proposals in literatures are effective in some specific scenarios with different considerations, however, there is still lack of complete considerations that are necessary to be conducted further improvements. Some proposals only employed a single UAV to provide data collection and mobile computing service, while it was inadequate to take the cooperation among UAVs into consideration in those proposals employing multiple UAVs as well. In most proposals, the UAV trajectory planning was a general method used to optimize the energy consumption and service latency, and the departure station was generally deployed at a fixed location. In fact, the initial location of departure station in the considered scenario would have a great impact on conducting the subsequent trajectory planning of UAVs. However, those proposals were lack of complete consideration of complex coupling associations among the departure station, flight paths and hovering points of UAVs. Additionally, there has been sufficient research progress on UAVs acting as multiple access points for data collection, and UAV as edge computing node in some typical applications also has been investigated to a certain extent, however, for the computing power scheduling in UAVs empowered aerial computing systems, the involved theoretical and technical challenges still have not attracted extensive attention.

Motivated by the above analysis of existing proposals, but being different from them, a joint optimization of energy efficiency and service fairness in UAVs empowered aerial computing systems is investigated in this paper, which fully considers the cooperation among multiple UAVs and complex coupling associations among the departure station, flight paths and hovering points, and conducts investigations from the trajectory planning of UAVs and the location planning for both the departure station and hovering points of UAVs to achieve computing power scheduling.

<!-- image-->  
Fig. 2. Multi-UAV empowered edge computing power network.

TABLE I  
BRIEF INTRODUCTIONS OF INVOLVED SYMBOLS AND CORRESPONDING EXPLANATIONS
<table><tr><td rowspan=1 colspan=1>Symbols</td><td rowspan=1 colspan=1>Explanations</td></tr><tr><td rowspan=1 colspan=1> $G U = \{ g u _ { 1 } , . . . , g u _ { N } \}$ </td><td rowspan=1 colspan=1>Ground users.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D = \{ D _ { 1 } , . . . , D _ { N } \} } }$ </td><td rowspan=1 colspan=1>Data volumes generated by distinct ground users.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { U A V = \left\{ u _ { 1 } , . . . , u _ { M } \right\} } }$ </td><td rowspan=1 colspan=1>UAVs to be deployed.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { C = \{ c _ { 1 } , . . . , c _ { M } \} } }$ </td><td rowspan=1 colspan=1>Computing capacities of distinct UAVs.</td></tr><tr><td rowspan=1 colspan=1> $S ( o ) = \{ s _ { 0 } \}$ </td><td rowspan=1 colspan=1>Departure station whose location is to be optimized.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { S ( h ) = \left\{ s _ { 1 } , . . . , s _ { K } \right\} } }$ </td><td rowspan=1 colspan=1>Hovering points of UAVs whose locations are to be optimized.</td></tr><tr><td rowspan=1 colspan=1> $\overline { { \mathcal { M } ( h o p ) } }$ </td><td rowspan=1 colspan=1>Matrix of hops between entities (ground users, hovering points).</td></tr><tr><td rowspan=1 colspan=1> $x _ { i j } ^ { m }$ </td><td rowspan=1 colspan=1>Abinary variable indicating whether $u _ { m }$ flies between the two hovering points, $s _ { i }$ and $s _ { j } .$ </td></tr><tr><td rowspan=1 colspan=1> $y _ { k } ^ { n }$ </td><td rowspan=1 colspan=1>Abinary variable indicating whether the data of $g u _ { n }$ is processed by the UAV hovering at $s _ { k } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { G U _ { k } = \{ g u _ { k } ^ { 1 } , . . . , g u _ { k } ^ { N _ { k } } \} } }$ </td><td rowspan=1 colspan=1>Ground users served by $u _ { m }$ hovering at $s _ { k } .$ </td></tr><tr><td rowspan=1 colspan=1> $D _ { k }$ </td><td rowspan=1 colspan=1>Data volume to be processed by $u _ { m }$ hovering at1 $s _ { k } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { f l y } } }$ </td><td rowspan=1 colspan=1>Energy consumption of flight caused at $u _ { m } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { c o l } } }$ </td><td rowspan=1 colspan=1>Energy consumption of data collection caused at $u _ { m } .$ </td></tr><tr><td rowspan=1 colspan=1> $E _ { m } ^ { c o m }$ </td><td rowspan=1 colspan=1>Energy consumption of data computation caused at $u _ { m } .$ </td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { h o v e r } } }$ </td><td rowspan=1 colspan=1>Energy consumption of hovering caused at $u _ { m } .$ </td></tr></table>

## III. DEFINITIONS

As shown in Fig. 2, in the considered scenario with a regional scale of $\mathbb { R } ^ { 3 }$ , the involved parameters could be defined as follows, and brief introductions of involved symbols and corresponding explanations are stated in Table I.

Ground users represented as $\begin{array} { r c l } { G U } & { = } & { \{ g u _ { 1 } , . . . , g u _ { n } , } \end{array}$ $\dots , g u _ { N } \}$ act the random location distribution, and the data volume generated by distinct ground users is represented as $\textit { D } = \ \{ D _ { 1 } , \ldots , D _ { n } , \ldots , D _ { N } \}$ . M UAVs represented as $U A V ~ = ~ \{ u _ { 1 } , \ldots , u _ { m } , \ldots , u _ { M } \}$ whose embedded computing capacities are heterogeneous and represented as ${ \cal { C } } = $ $\{ c _ { 1 } , \hdots , c _ { m } , \hdots , c _ { M } \}$ , where, $c _ { m }$ (unit: cycles per second)

represents the computing capacity of $u _ { m }$ and $c _ { m } > 0 .$ A departure station whose location is to be optimized, and could be assumed as $S ( o ) = \{ s _ { 0 } \}$ . Hovering points of UAVs is represented as $S ( h ) = \left\{ s _ { 1 } , \ldots , s _ { k } , \ldots , s _ { K } \right\}$ to be optimized as well. Accordingly, ground users, the departure station and hovering points of UAVs could constitute an undirected graph, and the UAVs assisted edge computing power network could be represented as $G ( V , E )$ , in which, V represents the set of locations of ground users, the departure station and hovering points of UAVs, and $E$ represents the set of edges among ground users, edges between ground users and hovering points and edges among hovering points.

For establishing a reasonable data collection and computation model, the following definitions are necessary to be stated.

Definition 1 (Neighbor): In $G ( V , E )$ ï¼ assuming that the communication radius of terminals owned by ground users is represented as $r _ { g u } .$ , the communication radius of UAVs is represented as $r _ { u }$ and the flight altitude is $H ,$ , for any two nodes within the area, $v _ { i }$ and $v _ { j }$ , if the Euclidean distance $d ( v _ { i } , v _ { j } )$ could satisfy one of the following conditions, $v _ { i }$ and $v _ { j }$ are neighbors.

$$
\begin{array} { r l } & { \bullet ( v _ { i } , v _ { j } ) \in G U \ \& \ d ( v _ { i } , v _ { j } ) \leq r _ { g u } . } \\ & { \bullet ( v _ { i } , v _ { j } ) \in G U \times S ( h ) \ \& \ d ( v _ { i } , v _ { j } ) \leq \sqrt { r _ { u } ^ { 2 } - H ^ { 2 } } . } \end{array}
$$

Definition 2 (Connex): Assuming that $\Phi \ = \ \boldsymbol { v } _ { 0 } e _ { 1 } v _ { 1 } e _ { 2 } \ldots$ $e _ { \tau } v _ { \tau }$ is a sequence of alternating points and edges, for any i in the range of $[ 1 , \tau ] ,$ , if the two adjacent nodes $v _ { i - 1 }$ and $v _ { i }$ are neighbors, Î¦ has the connectivity.

Definition 3 (Reachability): For any two nodes $v _ { i }$ and $v _ { j } ,$ if there is a Connex, $v _ { i }$ and $v _ { j }$ have the reachability.

Definition 4 (Hop-Count): For any two nodes $v _ { i }$ and $v _ { j }$ if there is a Reachability and the number of edges connecting $v _ { i }$ and $v _ { j }$ is $N ( e )$ , the hop count could be represented as $R ( v _ { i } , v _ { j } ) = N ( e )$ , otherwise, $R ( v _ { i } , v _ { j } ) = \infty$ . Accordingly, in terms of locations of ground users and hovering points, using the Floyd algorithm to determine the shortest path between nodes, the hop count of each pair of ground users and that of each pair of associated ground user and hovering point could be calculated and constitute a matrix, $\mathcal { M } ( h o p )$ .

The two binary variables $x _ { i j } ^ { m }$ and $y _ { k } ^ { n }$ are also introduced to state associations among $\mathrm { U A V s } ,$ hovering points and ground users. $x _ { i j } ^ { m }$ indicates that whether $u _ { m }$ flies from the hovering point si to another hovering point $s _ { j } ,$ , in that case and $i \neq j ,$ $x _ { i j } ^ { m } = 1$ , otherwise, $x _ { i j } ^ { m } = 0 . ~ y _ { k } ^ { n }$ indicates that whether the data of $g u _ { n }$ is collected and calculated by the UAV hovering at $s _ { k }$ , in that case, $y _ { k } ^ { n } = 1$ , otherwise, $y _ { k } ^ { n } = 0$

If the data generated by a set of ground users, $G U _ { k } \ =$ $\{ g u _ { k } ^ { 1 } , g u _ { k } ^ { 2 } , \ldots , g u _ { k } ^ { N _ { k } } \}$ , would be collected and calculated by $u _ { m }$ hovering at $s _ { k } .$ , where, $N _ { k }$ represents the number of ground users in $G U _ { k }$ and $N _ { k } \ = \ \sum _ { n = 1 } ^ { N } y _ { k } ^ { n }$ , the data volume to be processed by $u _ { m }$ could be represented as $D _ { k } = \sum _ { i = 1 } ^ { N _ { k } } D _ { k } ^ { i }$ , which could be further defined as $D _ { k } = \sum _ { n = 1 } ^ { N } y _ { k } ^ { n } \cdot D _ { n }$

In the considered scenario, since different ground users served by the same UAV would use the same spectrum resource at the same time, the technology of Orthogonal Frequency Division Multiple Access (OFDMA) is employed in the uplink to avoid the conflict [31], [32], where the frequency bandwidth $B _ { m }$ of $u _ { m }$ could be evenly divided into $N _ { k }$ equal sub-bands to provide the service for a maximum of $N _ { k }$ ground users. With the Shannon formula, the uplink data transmission rate for $g u _ { k } ^ { i }$ could be defined as

$$
r _ { k } ^ { i } = \frac { B _ { m } } { N _ { k } } \cdot \log { \left( 1 + \frac { P _ { k } ^ { i } \cdot g _ { k } ^ { i } } { \frac { B _ { m } } { N _ { k } } \cdot \theta } \right) } ,\tag{1}
$$

where $P _ { k } ^ { i }$ is the uplink transmission power of $g u _ { k } ^ { i } , \ : g _ { k } ^ { i }$ is the uplink channel gain between $g u _ { k } ^ { i }$ and $u _ { m }$ , and Î¸ is the noise spectral power density.

On the basis of above, the following definitions could be further introduced.

Definition 5 (Energy Consumption of Fight): Assuming that Î´ represents the energy consumption coefficient of UAV

flight, for $u _ { m }$ , the energy consumption of flight could be defined as

$$
E _ { m } ^ { f l y } = \delta \cdot \sum _ { ( i , j ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } } x _ { i j } ^ { m } \cdot d _ { i j } ,\tag{2}
$$

where $d _ { i j }$ is the Euclidean distance between the two hovering points, $s _ { i }$ and $s _ { j }$

Definition 6 (Energy Consumption of Data Collection): In terms of above definitions, the transmission delay of data generated by $g u _ { k } ^ { i }$ could be represented as $t _ { k } ^ { i } ( u p ) = \left. D _ { k } ^ { i } \right/ _ { r _ { k } ^ { i } }$ Accordingly, the energy consumption of data collection for $g u _ { k } ^ { i }$ could be defined as $\begin{array} { r } { E _ { k } ^ { i } ( u p ) = \int _ { 0 } ^ { t _ { k } ^ { 2 } ( u p ) } P _ { k } ^ { i } ( t ) d t } \end{array}$ , and the total energy consumption of data collection of $u _ { m }$ hovering at $s _ { k }$ could be further defined as

$$
E _ { m } ^ { c o l } = \sum _ { i = 1 } ^ { N _ { k } } \int _ { 0 } ^ { t _ { k } ^ { i } ( u p ) } P _ { k } ^ { i } ( t ) d t .\tag{3}
$$

Definition 7 (Energy Consumption of Data Computation): The energy consumption of data computation of $u _ { m }$ hovering at $s _ { k }$ could be defined as

$$
E _ { m } ^ { c o m } = \kappa _ { m } \cdot c _ { m } ^ { 2 } \cdot D _ { k } ,\tag{4}
$$

where $\kappa _ { m }$ represents the energy coefficient determined by the chip structure of the UAV.

Definition 8 (Energy Consumption of Hovering): The time of data collection and that of data computation of $u _ { m }$ hovering at $s _ { k }$ respectively could be represented as $t _ { k } ( u p ) ~ =$ $\operatorname* { m a x } _ { i = 1 , 2 , . . . , N _ { k } } \{ t _ { k } ^ { i } ( u p ) \}$ and $t _ { k } ( e x e ) = \left. D _ { k } \right/ _ { c _ { m } }$ . Assuming that Î¾ is the energy consumption coefficient of UAV hovering, the total energy consumption of hovering therefore could be defined as

$$
E _ { m } ^ { h o v e r } = \xi \cdot \left( \operatorname* { m a x } _ { i = 1 , 2 , \ldots , N _ { k } } \{ t _ { k } ^ { i } ( u p ) \} + \frac { D _ { k } } { c _ { m } } \right) .\tag{5}
$$

## IV. FORMULATIONS

In the considered scenario, due to limited onboard battery capacities of UAVs and diverse service requests of ground users, it is necessary to optimize the trajectory planning of UAVs and the location planning for both the departure station and hovering points of UAVs, for improving the energy efficiency of UAVs and the service fairness experienced by ground users. In terms of above definitions, the following two optimization objectives could be formulated.

## A. Energy Efficiency

Through considering the timeliness of data collection and computation, and limited onboard battery capacities of UAVs for satisfying necessary energy supplies of making a return trip while completing data collection and calculation, to provide sufficient services for served ground users with limited energy consumption and achieved load balance, the first optimization objective is introduced to minimize the energy utilization and the standard deviation of energy consumption through conducting reasonable trajectory planning (TP) of UAVs, so as to maximize the energy efficiency of UAVs, which could be defined as

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { \mathbf { T } } ~ ( U ( E ) + \alpha \cdot S T D ( E ) ) } \\ { = \displaystyle \operatorname* { m i n } _ { \mathbf { T } \mathbf { P } } ~ \left( \frac { \sum _ { m = 1 } ^ { M } \frac { E _ { m } } { E _ { m } ^ { f u l } } } { M } + \alpha \cdot \sqrt { \frac { \displaystyle M } { \displaystyle m - 1 } ( E _ { m } - \bar { E } ) ^ { 2 } } \right) , } \end{array}\tag{6}
$$

where $\begin{array} { r } { U ( E ) = \sum _ { m = 1 } ^ { M } { \frac { E _ { m } } { E _ { m } ^ { f u l l } } } \bigg / _ { M } } \end{array}$ represents the average energy utilization of UAVs, $S T D ( E ) ~ = ~ \sqrt { \sum _ { m = 1 } ^ { M } \left( E - \bar { E } \right) ^ { 2 } \Big / M }$ representing the standard deviation of energy consumption of UAVs is an equilibrium coefficient of energy consumption, $E _ { m } ^ { f u l l }$ represents the full onboard battery capacity of $u _ { m }$ $\ c E _ { m } ^ { ' '  } = \ c E _ { m } ^ { ' f l y } + \ c E _ { m } ^ { c o l } + \ c E _ { m } ^ { c o m } + \ c E _ { m } ^ { h o v e r }$ represents the total energy consumption of $u _ { m }$ used to execute a flight mission, and $\bar { E } =$ $\textstyle \sum _ { m = 1 } ^ { M } \dot { E } _ { m } { \big / } _ { M }$ represents the average energy consumption of all UAVs.

In general, from the definition of $U ( E )$ , it is expected to maximize the energy utilization of UAVs with limited onboard battery capacities, however, with a certain number of deployed UAVs in the considered scenario, the minimization setting of energy utilization is adopted here to avoid the problem of UAV purposely executing a flight mission over long distance while increasing the unnecessary energy consumption, and enhance the energy efficiency accordingly. Additionally, in (6), the former optimization objective is used to minimize the energy utilization, so as to eliminate the unnecessary energy consumption of UAVs, the latter is used to minimize the standard deviation of energy consumption, so as to achieve the load balance of UAVs, therefore, a factor Î± is introduced to balance the relationship between the two optimization objectives, and determine the distinct importance.

## B. Service Fairness

The hop count between the ground user and the serving UAV, which indicates the serving delay, has direct influence on the QoS experienced by the ground user. Due to the limited number of UAVs executing flight missions and the limited signal coverage of the UAV with the flight altitude H, some ground users to be served by a UAV would choose other ground users as relay nodes to assist with the data transmission. Nevertheless, onboard battery capacities of terminals owned by ground users are limited as well, the imbalance of hop counts would result in the emergence of âenergy holesâ around some ground users, which would break up the network topology with the loss of connectivity and consequently shorten the network lifespan, as a result, those ground users could not experience the adequate service. Accordingly, the second optimization objective is introduced to minimize the maximum in minimum hop counts between ground users and their candidate serving UAVs and the standard deviation of hop counts through conducting reasonable location planning (LP) for both the departure station and hovering points, so as to maximize the service fairness among ground users, which

could be formulated as

$$
\begin{array} { r l } {  { \operatorname* { m i n } _ { { \bf L } { \bf P } } ( \operatorname* { m a x } _ { n = 1 , \cdots , N } R _ { n } + \beta \cdot S T D ( R ) ) } } \\ & { = \operatorname* { m i n } _ { { \bf L } { \bf P } } ( \operatorname* { m a x } _ { n = 1 , \cdots , N } ( \operatorname* { m i n } _ { k = 0 , \cdots , K } R ( g u _ { n } , s _ { k } ) ) ) , } \\ & { = + \beta \cdot \sqrt { \frac { \sum _ { n = 1 } ^ { N } ( R _ { n } - \bar { R } ) ^ { 2 } } { N } } } \end{array}\tag{7}
$$

where $R _ { n } = \operatorname* { m i n } _ { k = 0 , \cdots , K } R ( g u _ { n } , s _ { k } )$ represents the minimum of hop counts between gun and the chosen serving UAV hovering at $\begin{array} { r } { s _ { k } , \bar { R } = \sum _ { n = 1 } ^ { N } \bar { R _ { n } } \Big / _ { N } } \end{array}$ represents the average of minimum hop counts, $S T D ( R ) = \sqrt { \sum _ { n = 1 } ^ { N } \left( R _ { n } - \bar { R } \right) ^ { 2 } \bigg / _ { N } }$ representing the standard deviation of minimum hop counts, is introduced as a coefficient of fairness. The greater the standard deviation, the worse the fairness of different ground users in requesting computing power. Additionally, in (7), the former optimization objective is used to minimize the hop counts between any one ground user and the chosen serving UAV, so as to enhance the energy efficiency of data transmission, the later is used to minimize the standard deviation of hop counts, so as to balance the energy consumption of ground users, therefore, a factor $\beta$ is introduced to balance the relationship between the two optimization objectives, and determine the distinct importance.

## C. Constrains

In the considered scenario, taking into account of the airground limitation, the problem of recharge and recondition of UAVs, the association between ground user and UAV, the full coverage with limited UAVs, safe distances of UAVs flight and limited onboard battery capacities of UAVs, the following constraints are necessary to be introduced to solve the two formulated optimization objectives in an optimal fashion.

Constraint 1 (Area): Taking into account of the air-ground limitation, locations of ground users, the location of departure station (to be optimized) and locations of hovering points of UAVs (to be optimized) should be in the air-ground of $\mathbb { R } ^ { 3 } .$ . Meanwhile, due to the consideration of relay relationship among ground users, to ensure the isolation of service areas covered by hovering points, there should be a certain distance between hovering points. Therefore, Constraint 1 could be defined as

$$
\left\{ \begin{array} { l l } { d ( s _ { i } , s _ { j } ) > \hbar , \forall ( s _ { i } , s _ { j } ) \in S ( h ) ^ { 2 } , s _ { i } \neq s _ { j } , } \\ { G U , S ( o ) , S ( h ) \subseteq \mathbb { R } ^ { 3 } , } \end{array} \right.\tag{8}
$$

where, â is the threshold of distance.

Constraint 2 (Number of Flights): Through considering recharge and recondition of UAVs, each UAV only make up to one return trip, and Constraint 2 could be defined as

$$
\sum _ { k = 1 } ^ { K } x _ { s _ { 0 } s _ { k } } ^ { m } \leq 1 , \ \forall m \in \{ 1 , 2 , \cdots , M \} .\tag{9}
$$

Constraint 3 (Association): To ensure that all ground users could be fully served, and the integrity of data collection and computation for ground users, each ground user could only be associated with a hovering point of UAV, and

Constraint 3 could be defined as

$$
\sum _ { k = 0 } ^ { K } y _ { k } ^ { n } = 1 , \forall n \in \{ 1 , 2 , \cdots , N \} .\tag{10}
$$

Constraint 4 (Full Coverage): With the limited number of deployed UAVs, to ensure each ground user to be served by only one UAV, the serving coverage area of each determined hovering point should be visited by only one UAV, and Constraint 4 could be defined as

$$
\left\{ \begin{array} { l l } { \displaystyle \sum _ { m = 1 } ^ { M } \sum _ { k = 1 } ^ { K } x _ { s _ { 0 } s _ { k } } ^ { m } \le M , } \\ { \displaystyle \sum _ { m = 1 } ^ { M } x _ { s _ { i } s _ { k } } ^ { m } = \sum _ { m = 1 } ^ { M } x _ { s _ { k } s _ { j } } ^ { m } = 1 , } \\ { \displaystyle \forall s _ { k } \in S ( h ) , ( s _ { i } , s _ { j } ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } , k \neq i , k \neq j . } \end{array} \right.\tag{11}
$$

Constraint 5 (Flight Path): To effectively manage deployed UAVs and avoid collisions with safe flight distance, after each UAV completing the data collection and computation at hovering points along the determined flight path, each UAV follows its original path back to the departure station, and Constraint 5 could be defined as

$$
\sum _ { ( i , j ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } } x _ { i j } ^ { m } = \sum _ { ( j , i ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } } x _ { j , i } ^ { m } , \ i < j .\tag{12}
$$

Constraint 6 (Energy Consumption): Assuming that each UAV is not rechargeable during the flight, the maximum energy consumption used to execute a flight mission must not be exceed the full onboard battery capacity denoted as $E _ { m } ^ { f u l l }$ ï¼ and Constraint 6 could be defined as

$$
\operatorname* { m a x } _ { m \in \{ 1 , \cdots , M \} } E _ { m } \leq E _ { m } ^ { f u l l } .\tag{13}
$$

## D. Joint Optimization Problem

In terms of above defined formulations for optimizing the energy efficiency of UAVs and service fairness among ground users, and introduced constraints, the joint optimization problem for achieving reasonable computing power scheduling in the considered scenario could be stated as

$$
\begin{array} { r l } &  \{ \begin{array} { l l } { \mathbb { P } ^ { 1 } \cdot \operatorname* { m i n } ( U ( E ) + \alpha \cdot S ^ { [ \mathcal { D } ] } ( B ( E ) ) ) , } \\ { \mathbb { P } ^ { 2 } \cdot \operatorname* { m i n } ( \underbrace { \operatorname* { m a x } _ { 1 } \Biggl ( \theta _ { 1 } \cdot \operatorname* { m a x } _ { N } ( \theta _ { 1 } \cdot \mathcal { S } ^ { [ \mathcal { D } ] } ) ) } \\ { \mathbb { P } ^ { 3 } \cdot \operatorname* { m i n } ( \underbrace { \operatorname* { m a x } _ { 1 } \Biggl ( \theta _ { 1 } \cdot \operatorname* { m a x } _ { N } ( \theta _ { 1 } \cdot \mathcal { S } ^ { [ \mathcal { D } ] } ) ) } _ { \mathrm { t o r } \mathrm { t } } ) , } \end{array}  } \\ & { \quad \times 1 , \quad \epsilon \cdot \epsilon _ { 1 } \cdot \epsilon _ { 2 } \cdot \epsilon _ { 3 } \cdot \epsilon _ { 3 } \cdot \epsilon _ { 3 } \cdot \epsilon _ { 4 } \cdot \mathbb { P } ( \epsilon _ { 3 } \cdot \epsilon _ { 3 } ) \in S ( \mathbb { W } ) ^ { 2 } , \mathrm { ~ s q ~ \neq ~ s } \epsilon _ { 1 } , } \\ & { \quad \epsilon ^ { - 2 } \cdot \sum _ { i = 1 } ^ { N } \sum _ { \epsilon = 1 } ^ { N } \epsilon _ { i , i = 1 } ^ { N } \leq 1 , \mathrm { ~ s i n ~ e ~ } \epsilon _ { 1 } \cdot 1 , 2 , \cdots , M \epsilon _ { 1 } , } \\ & { \quad \epsilon \cdot \sum _ { i = 1 } ^ { N } \sum _ { \epsilon = 0 } ^ { N } \epsilon _ { i } - 1 , \mathrm { ~ s i n ~ e ~ } \epsilon _ { 1 } , } \\ &  \quad \epsilon \cdot \sum _ { i = 1 } ^ { N } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _ { i } \epsilon _  i  \end{array}
$$

$$
\begin{array} { r l r } { \quad } & { C 5 : \displaystyle \sum _ { ( i , j ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } } x _ { i j } ^ { m } = \displaystyle \sum _ { ( j , i ) \in \{ S ( o ) , S ( h ) \} ^ { 2 } } x _ { j , i } ^ { m } , i < j , } & \\ { \quad } & { C 6 : \displaystyle \operatorname* { m a x } _ { m \in \{ 1 , \cdots , M \} } E _ { m } \leq E _ { m } ^ { f u l l } . } & { ( 1 4 ) } \end{array}
$$

## V. SOLUTIONS

## A. Multi-Agent Cooperation for Energy Efficiency

Through fully considering complex coupling associations among the departure station, flight paths and hovering points of UAVs, the trajectory planning of UAVs is investigated to maximize the energy efficiency, which could be transformed into a discrete MDP that is fully observable for multiple agents.

Proof : For the problem of trajectory planning, the involved agents are M UAVs, which could be represented as $\Upsilon _ { u } \ \stackrel { \Delta } { = } \ \{ u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { M } \}$ . To execute a flight mission, starting from the departure station $s _ { 0 } ,$ , an agent would make a return trip through traversing a finite number of discrete hovering points $\{ s _ { k } ( x _ { k } , y _ { k } , z _ { k } ) \} _ { k \in \{ 0 , \cdots , K \} }$ , that is, $S ( o ) $ $S ( h ) ~  ~ S ( o )$ . For determining traversed hovering points, in terms of the state of the agent currently hovering at $s _ { k } .$ $u _ { m }$ would perform an action $a _ { k }$ according to the discrete sequence decision mode, and select the next hovering point $s _ { k + 1 } , \ s _ { k + 1 } \ \in \ S ( h ) \cup S ( o )$ . Therefore, the decision-making process could be considered as that the choice of hovering point is related to the state of the agent at the current hovering point, but has nothing to do with previous states, that is, $p \left( s _ { k + 1 } | { \left( s _ { k } , a _ { k } \right) } , \cdot \cdot \cdot , { \left( s _ { 0 } , a _ { 0 } \right) } \right) \ = \ p \left( s _ { k + 1 } | { \left( s _ { k } , a _ { k } \right) } \right)$ To improve the efficiency of trajectory planning while satisfying defined constraints, agents communicate with each other to share the observed information, $\mathcal { O } _ { u _ { m } }$ , including traversed hovering points and energy consumption, therefore, the environment is fully observable for trajectory planning. In conclusion, the problem of trajectory planning could be transformed into a fully observable discrete MDP. â 

Hence, a tuple $\langle S _ { u } , \mathcal { A } _ { u } , \mathcal { O } _ { u } , \mathcal { R } _ { u } , \mathcal { P } _ { u } , M \rangle$ is defined, $\mathcal { S } _ { u } =$ $\mathcal { S } _ { u _ { 1 } } \times \mathcal { S } _ { u _ { 2 } } \times \cdot \cdot \cdot \times \mathcal { S } _ { u _ { M } }$ is the global state space, $\mathcal { A } _ { u } = \mathcal { A } _ { u _ { 1 } } \times$ $\mathcal { A } _ { u _ { 2 } } \times \cdot \cdot \cdot \times \mathcal { A } _ { u _ { M } }$ is the action space shared by $\mathrm { U A V s , } O _ { u } =$ $\mathcal { O } _ { u _ { 1 } } \times \mathcal { O } _ { u _ { 2 } } \times \cdot \cdot \cdot \times \mathcal { O } _ { u _ { M } }$ is the observation space and $\mathcal { O } _ { u _ { m } }$ is generated by $u _ { m }$ local information. $\mathcal { R } _ { u }$ is the reward function, $\mathcal { P } _ { u } : \mathcal { S } _ { u } \times \mathcal { A } _ { u } \to \mathcal { S } _ { u } ^ { \prime }$ is the state transition probability function.

In the considered scenario, to better define the discrete MDP for trajectory planning, the decision-making process could be regarded as a sequencing problem of hovering points for each UAV. Assuming that hovering points (including the departure station) visited by a UAV could constitute a sequence and the maximum sequence length of hovering point for UAV is $L ,$ the $l - t h \ ( l \in \{ 1 , 2 , \cdots , L \} )$ hovering point of $u _ { m }$ is $u _ { m } ( l )$ , and $\underset { m = 1 } { M } \overset { L } { \underset { l = 1 } { \cup } } u _ { m } ( l ) = S ( o ) \cup S ( h )$ . Additionally, since the number of visited hovering points is different for different UAVs, the maximum sequence length of hovering point sequence is practically different for UAVs, if a UAV has been back to the departure station, the next visiting location would still be the departure station to ensure the consistency of expression. In discrete steps, each agent could interact with the environment to improve the policy of trajectory planning. As an illustration, at step $l , \ u _ { m }$ could obtain

$$
\mathcal { O } _ { u _ { m } } ( l )
$$

$S _ { u } ( l ) \overset { \Delta } { = } \{ \mathcal { O } _ { u _ { m } } ( l ) | \ \forall u _ { m } \in \Upsilon _ { u } \} , \mathcal { O } _ { u _ { m } } ( l ) : \mathcal { S } _ { u } ( l ) \to \mathcal { O } _ { u _ { m } } ( l )$ subsequently, with the observation, $u _ { m }$ could obtain rewards through executing corresponding actions, and the state could be transferred into a new one $\mathcal { S } _ { u } ( l + 1 )$ . The whole process would be repeated until the trained optimal trajectory planning is obtained.

To address the problem of achieving the energy efficiency of UAVs through trajectory planning, detail explanation of each component involved in the discrete MDP is stated as follows. To fully use the advantage of maximizing future rewards [33], [34], a multi-agent cooperative Q-learning algorithm is proposed as a promising solution, which is stated in Algorithm 1. State: With the formulated optimization problem, the state space has three components, e.g., UAVs, locations of hovering points and energy consumptions of UAVs at hovering points. For $u _ { m }$ hovering at $u _ { m } ( l ) \ ~ ( \forall l ^ { } \in \ \{ 1 , 2 , \cdot \cdot \cdot , L \} )$ , the local state space, $S _ { u _ { m } } ( l ) \ \in \ S _ { u _ { m } } ,$ could be defined as $\mathcal { S } _ { u _ { m } } ( l ) = \{ u _ { 1 } , \cdots , u _ { M } , s _ { 0 } , \cdots , s _ { K } , E _ { u _ { 1 } } ( l ) , \cdots , E _ { u _ { M } } ( l ) \}$ . The state space shared by agents therefore could be further defined as $S _ { u } \triangleq \{ S _ { u _ { m } } ( l ) \}$ .

Action: For $u _ { m }$ hovering at $u _ { m } ( l )$ , the chosen next hovering point constitutes the action space, that is, $\mathcal { A } u _ { m } \stackrel { \Delta } { = } \{ a _ { u _ { m } } ( l ) \}$ ï¼ where $a _ { u _ { m } } ( l ) ~ = ~ s _ { i } ( ~ s _ { i } ~ \in ~ S ( o ) ~ \cup ~ S ( h ) )$ . Therefore, the global action space shared by agents could be further defined as $\mathcal { A } _ { u } \stackrel { \Delta } { = } \{ \mathcal { A } u _ { m } \}$ . However, to ensure the serving coverage area of each determined hovering point to be visited by only one UAV, Constraint 4 should be satisfied in the global action space. Additionally, to ensure all ground users to be fully served by deployed UAVs, and each ground user to be associated with only one hovering point of UAV, if there is any one unserved ground user while all deployed UAVs being on the way departure station, the UAV closest to the unserved ground user would select the action of staying at the current hovering point, and provide service for the unserved ground user through a multi-hop connection, that is, if $a = s _ { 0 }$ $a = a ^ { \prime }  a _ { u _ { m } } ( l - 1 )$

Observation: Assuming that agents could communicate with each other to obtain locations of UAVs, currently visited hovering points and energy consumption, for $u _ { m }$ hovering at $u _ { m } ( l ) \ ~ ( \forall l  \in \ \{ 1 , 2 , \cdot \cdot \cdot , L \} )$ ), the local observation space $\begin{array} { r l r } { \mathcal { O } _ { u _ { m } } ( l ) } & { { } \in } & { \mathcal { O } _ { u _ { m } } , } \end{array}$ could be defined as $\begin{array} { l l l } { { { \mathcal O } _ { u _ { m } } ( l ) } } & { { = } } & { { \{ u _ { 1 } , \cdots , u _ { M } , s _ { 0 } , \cdots , s _ { K } , E _ { u _ { 1 } } ( l ) , \cdots , E _ { u _ { M } } ( l ) \} } } \end{array}$ , and the global observation space could be further defined as $\mathcal { O } _ { u } \overset { \Delta } { = } \{ \mathcal { O } _ { u _ { m } } ( l ) \}$

Reward: To improve the search efficiency of trajectory planning while satisfying defined constraints, and obtain optimal trajectory planning for all UAVs, negative and positive rewards could be introduced from perspectives of the energy consumption caused by each action choice, the full coverage that the serving area of each hovering point could be visited by only one UAV and the next action taken by $u _ { m }$ hovering at $u _ { m } ( l )$ should be the choice of hovering point that has not been visited yet, and all UAVs could make a return trip without energy exhaustion.

(1) To enable the path learned by the UAV to be the one with the highest energy efficiency that the UAV could make a return trip with enough energy, for each $\mathrm { U A V } _ { \mathrm { \Delta } }$ flight, $u _ { m }$ would be given the penalty for energy consumption. To assume that $E _ { s _ { i } , s _ { j } } ^ { f l y }$ is the energy consumption of $u _ { m }$ flying from $s _ { i }$ to $s _ { j } .$ , which could be calculated with Definition $^ { 5 , }$ and $E _ { m } ( s _ { j } ) \ ' = E _ { s _ { i } } ^ { c o l } + E _ { s _ { i } } ^ { c o m } + E _ { s _ { i } } ^ { h o v e r }$ is the summation of energy consumption of data collection, data computation and hovering of $u _ { m }$ at $s _ { j } ,$ which could be calculated with Definitions $\qquad 6 \sim 8 .$ $E _ { s _ { i } , s _ { j } } = \mathring { E } _ { s _ { i } , s _ { j } } ^ { f l y } + E _ { m } ( s _ { j } )$ could be taken as the total energy consumption caused by an action choice of $u _ { m }$ hovering at $s _ { i } .$ . Accordingly, for either pair of two hovering points, but $s _ { i } ~ \neq ~ s _ { j }$ , there is $E _ { s _ { i } , s _ { j } } ~ \neq ~ 0$ . If $s _ { i } ~ = ~ s _ { j } , ~ E _ { s _ { i } , s _ { j } } ~ = ~ 0$ All $E _ { s _ { i } , s _ { j } }$ could constitute a matrix of energy consumption, $\mathcal { M } ( E ) = \{ E _ { s _ { i } , s _ { j } } \} _ { ( K + 1 ) \times ( K + 1 ) } , \forall \left( s _ { i } , s _ { j } \right) \in ( S ( o ) \cup S ( h ) ) ^ { 2 }$ and for $u _ { m }$ hovering at $u _ { m } ( l )$ , the negative reward as the penalty for energy consumption could be defined as

```latex
Algorithm 1 Multi-Agent Cooperative Q-Learning for P1
Input: Defined parameters, the number of iterations Ï.
Output: Trajectory planning.
1: Obtaining the matrix $\mathcal { M } ( h o p )$ with Definition 4;
2: for $s _ { i } \in S ( o ) \cup S ( h ) )$ do
3: for $s _ { j } \in S ( o ) \cup S ( h )$ do
4: if $( s _ { i } \neq s _ { j } )$ then
5: Calculating $E _ { s _ { i } , s _ { i } } ^ { f l y }$ with Definition 5;
6: Calculating $E _ { m } ( \boldsymbol { s } _ { j } )$ with Definitions $\delta \sim \delta ;$
7: Calculating $\begin{array} { r } { E _ { s _ { i } , s _ { j } } = E _ { s _ { i } , s _ { j } } ^ { f l y } + E _ { m } ( s _ { j } ) ; } \end{array}$
8: else
9: $E _ { s _ { i } , s _ { j } } = 0 ;$
10: end if
11: end for
12: end for
13: Constituting the matrix of energy consumption, ${ \mathcal { M } } ( E ) ;$ ;
14: Initializing a Q table, $\forall s \in S _ { u } \ \& \ \forall a \in \mathcal A _ { u } ;$
15: With the number of agents, M , generating an initial
solution, and obtaining the value of ${ \mathcal { P } } 1 , { \mathcal { F } } ( L ) ;$ ;
/* Updating the Q table and $\mathcal { F } ( L ) . ^ { * } /$
16: for $\psi = 1 \mathrm { ~ t o ~ } \psi _ { m a x }$ do
17: $\begin{array} { r } { \rho \gets 1 - \frac { \psi } { \psi _ { \mathrm { m a x } } } ~ ; } \end{array}$
$/ { ^ { * } \mathrm { \Delta } } \rho$ is the adaptive exploring rate in Q-learning. */
18: for $m = 1$ to M do
19: for l = 1 to L do
20: Calculating the negative reward $p _ { e } ( l ) ;$
21: for $s \in \mathcal { S } _ { u _ { m } } ( l )$ do
22: for $a \in A _ { u _ { m } }$ do
23: if $( r a n d ( ) < \rho )$ then
24: Selecting a with $\mathcal { R } _ { u } ( s , a )$ using roulette;
25: else
26: Selecting a with the greatest value of $Q ;$
27: end if
28: if $( a = s _ { 0 } )$ then
29: $\begin{array} { r } { a = a ^ { \prime }  a _ { u _ { m } } ( l - 1 ) ; } \end{array}$
30: Calculating the negative reward $p _ { c } ( l ) ;$
31: else
32: $a = a ^ { \prime } ;$
33: end if
$\stackrel { \triangledown } { Q } \left( s , a \right) \gets Q \left( s , a \right) +$
34: $\lambda \cdot \left[ \mathcal { R } _ { u } \left( s , a \right) + \gamma \cdot \operatorname* { m a x } _ { a ^ { \prime } } Q \left( s , a ^ { \prime } \right) - Q \left( s , a \right) \right] ;$
35: end for
36: end for
37: end for
38: if $( u _ { m } ( L + 1 ) = s _ { 0 } )$ then
39: Calculating the positive reward $r ( L ) ;$
$Q \left( s , s _ { 0 } \right) \gets Q \left( s , s _ { 0 } \right) +$
40: $\lambda \cdot \left. \mathcal { R } _ { u } \left( s , s _ { 0 } \right) + \gamma \cdot \operatorname* { m a x } _ { s _ { 0 } } Q \left( s , s _ { 0 } \right) - Q \left( s , s _ { 0 } \right) \right. ;$
41: Obtaining the updated value of ${ \mathcal { P } } 1 , { \mathcal { F } } ^ { \prime } ( L )$
42: if $( \mathcal { F } ^ { \prime } ( L ) < \mathcal { F } ( L ) )$ then
43: $\mathcal { F } ( L )  \mathcal { F } ^ { \prime } ( L ) ;$
44: end if
45: Determining the path corresponding to $\mathcal { F } ( L )$
46: end if
47: end for
48: end for
```

$$
p _ { e } ( l ) = - r _ { e } \cdot \frac { E _ { m } ( l + 1 ) - E _ { m } ( l ) - \overline { { \mathcal { M } ( E ) } } } { \mathcal { M } ( E ) _ { m a x } } ,\tag{15}
$$

where ${ \overline { { \mathcal { M } ( E ) } } }$ is the mean of all elements in $\mathcal { M } ( E ) , \mathcal { M } ( E ) _ { m a x }$ is the maximum in $\mathcal { M } ( E ) , r _ { e } = 1$ is the penalty coefficient.

(2) To ensure all ground users to be fully served and the integrity of data collection and computation for ground users, if there is an unvisited hovering point while all UAVs being on the way departure station, the UAV would be given the penalty for incomplete coverage, which could be defined as

$$
p _ { c } ( l ) = - r _ { c } \cdot \left( K - \sum _ { i = 1 } ^ { K } \sum _ { k = 0 } ^ { K } \sum _ { m = 1 } ^ { M } x _ { s _ { i } s _ { k } } ^ { m } \right) ,\tag{16}
$$

where $r _ { c } = 1$ is the penalty coefficient.

(3) If all UAVs could make a return trip without energy exhaustion, and the learned path is optimal for each UAV, the positive reward given to each UAV could be defined as

$$
\begin{array} { r } { r ( L ) = 1 0 ^ { 1 + \frac { \mathcal { F } ( L ) - \mathcal { F } ^ { \prime } ( L ) } { \mathcal { F } ( L ) } } , } \end{array}\tag{17}
$$

where $\mathcal { F } ( L )$ is the value of $\mathcal { P } 1$ corresponding to the known optimal path, and ${ \mathcal { F } } ^ { \prime } ( L )$ is the value of P1 corresponding to the next path option.

## B. Multi-Agent Cooperation for Service Fairness

To maximize the service fairness experienced by ground users through minimizing the maximum in minimum hop counts between ground users and their candidate serving UAVs, and the standard deviation of hop counts, it is necessary to reasonably optimize locations for both the departure station and hovering points to satisfy requirements of association and full coverage. Therefore, this problem could be transformed into a partially observable continuous MDP with multiple agents.

Proof : For the problem of location planning, the involved agents are $K + 1$ locations, which could be represented as $\Upsilon _ { s } = \{ s _ { 0 } , s _ { 1 } , \cdot \cdot \cdot , s _ { K } \}$ , and agents could cooperate with each other to obtain the optimal $S ( o ) \cup S ( h ) =$ $\{ s _ { k } ( x _ { k } , y _ { k } , z _ { k } ) \} _ { k \in \{ 0 , \cdots , K \} }$ while achieving the expected service fairness. At the time-slot t in successive intervals, for determining optimal locations, in terms of the state at the current location, each agent $s _ { k }$ would perform an action $a _ { k }$ according to the continuous sequence decision mode, and generate a new location $s _ { k } ^ { t + 1 } ( x _ { k } ^ { \dot { t } + 1 } , y _ { k } ^ { t + 1 } , z _ { k } ^ { t + 1 } )$ ). Therefore, the decision-making process could be considered as that the generation of location is related to the state at the current location, but has nothing to do with previous states, that is, $p \left( s _ { k } ^ { t + 1 } | ( s _ { k } ^ { t } , a _ { k } ^ { t } ) , \cdot \cdot \cdot , \bar { ( } s _ { k } ^ { 1 } , a _ { k } ^ { 1 } ) \right) \ = \ p \hat { \left( \right)} s _ { k } ^ { t + 1 } | ( s _ { k } ^ { t } , a _ { k } ^ { t } ) $ To improve the efficiency of location planning while satisfying defined constraints, in each time-slot, UAVs hovering at agents could communication with each other to share the location information and the information of ground users to be served, $\mathcal { O } _ { s _ { k } } ( t )$ , but, sine the next actions adopted by agents are independent, the environment is partially observable for location planning. In conclusion, the location planning could be transformed into a partially observable continuous MDP. â 

Hence, a tuple $\langle S _ { s } , \mathcal { A } _ { s } , \mathcal { O } _ { s } , \mathcal { R } _ { s } , \mathcal { P } _ { s } , K \rangle$ is defined, $\begin{array} { r l } { \mathcal { S } _ { s } } & { { } = } \end{array}$ $S _ { s _ { 0 } } \times S _ { s _ { 1 } } \times \cdot \cdot \cdot \times S _ { s _ { K } }$ is the global state space, $\mathcal { A } _ { s } = \mathcal { A } _ { s _ { 0 } } \times$ $\mathcal { A } _ { s _ { 1 } } \times \cdots \times \mathcal { A } _ { s _ { K } }$ is the action space shared by agents, $\mathcal { O } _ { s } =$ $\mathcal { O } _ { s _ { 0 } } \times \mathcal { O } _ { s _ { 1 } } \times \cdot \cdot \cdot \times \mathcal { O } _ { s _ { K } }$ is the observation space and $\mathcal { O } _ { s _ { k } }$ is generated by $s _ { k }$ local information, $\mathcal { R } _ { s }$ is the reward function, $\mathcal { P } _ { s } : \mathcal { S } _ { s } \times \mathcal { A } _ { s } \to \mathcal { S } _ { s } ^ { \prime }$ is the state transition probability function.

In the considered scenario, to better define the continuous MDP for location planning, the decision-making process would be conducted in consecutive time intervals during $T ,$ and the time-slot is âT . Accordingly, the number of time-slots is $\begin{array} { r } { \frac { T } { \Delta T } . } \end{array}$ and the serial number of time-slot could be defined as $\vec { t } \in \{ 1 , 2 , \cdots , \frac { T } { \Delta T } \}$ . In continuous steps, each agent could interact with the environment to improve the policy of location planning. As an illustration, at step t, each agent $s _ { k }$ could obtain the current observation $\mathcal { O } _ { s _ { k } } ( t )$ from the global state space $S _ { s } ( t ) \overset { \Delta } { = } \{ \mathcal { O } _ { s _ { k } } ( t ) | \forall s _ { k } \in \Upsilon _ { s } \} , \mathcal { O } _ { s _ { k } } ( t ) : S _ { s } ( t ) \to \mathcal { O } _ { s _ { k } } ( t )$ ï¼ subsequently, with the observation, $s _ { k }$ could obtain rewards through executing corresponding actions, and the state would be transferred into a new one $S _ { s } ( t + 1 )$ . The whole process would be repeated until the trained optimal location planning is obtained.

To address the problem of achieving the service fairness among ground users through location planning, detail explanation of each component involved in the continuous MDP is stated as follows. Through comprehensively comparing popular policy optimization based multi-agent cooperative deep reinforcement learning approaches [35], [36], an algorithm based on the architecture of Actor-Critic is proposed as a promising solution, which is stated in Algorithm 2.

State: With the formulated optimization problem, the state space has five components, e.g., locations of the departure station and hovering points, locations of ground users, the communication radius of UAV, the communication radius of ground user, and the association between ground user and hovering point. The association could be determined with Def inition 4 and formulation (7). ât $\in \{ 1 , 2 , \cdots , \frac { T } { \Delta T } \}$ ï¼ the local state space, $S _ { s _ { k } } ( t ) ~ \in ~ S _ { s _ { k } }$ , could be defined as $S _ { s _ { k } } ( t ) ~ = ~ \{ s _ { 0 } , \cdots , s _ { K } , g u _ { 1 } , \cdots , g u _ { N } , r _ { u } , r _ { g u } , y _ { k } ^ { n } \}$ The global state space shared by agents therefore could be further defined as $\mathcal { S } _ { s } \triangleq \{ \mathcal { S } _ { s _ { k } } ( t ) \}$

Action: For $s _ { k }$ in the t-th time-slot, the chosen moving step size and direction, and shared information of locations constitute the action space, that is, $\begin{array} { r l } { \mathcal { A } _ { s _ { k } } ( t ) } & { { } = } \end{array}$ $\{ \zeta _ { s _ { k } } ( t ) , \vartheta _ { s _ { k } } ( t ) , s _ { 0 } ( t ) , \cdot \cdot \cdot , s _ { K } ( t ) \}$ , where $\zeta _ { s _ { k } } ( t )$ represents the moving step size and $\vartheta _ { s \boldsymbol { k } } \left( t \right) \ \left( \vartheta _ { s \boldsymbol { k } } \left( t \right) \in \left[ 0 , 2 \pi \right] \right)$ represents the moving direction. Therefore, the global action space shared by agents could be further defined as $\mathcal { A } _ { s } \triangleq \{ \mathcal { A } _ { s _ { k } } ( t ) \}$ . However, to ensure each ground user to be associated with only one hovering point of UAV, Constraint 3 should be satisfied in the global action space.

Algorithm 2 Multi-Agent Cooperative Actor-Critic for $\mathcal { P } 2$   
Input: Defined parameters.   
Output: Location planning.   
1: With the number of agents, $K + 1 ,$ , generating initial   
locations for $S ( o ) \cup S ( \bar { h } ) = \{ s _ { k } ^ { 0 } ( x _ { k } ^ { 0 } , y _ { k } ^ { \top } , z _ { k } ^ { 0 } ) \} _ { k \in \{ 0 , \cdots , K \} } ;$   
2: Initializing both the Actor network and the Critic network,   
and corresponding weights;   
3: Obtaining the matrix $\mathcal { M } ( h o p )$ with Definition $^ { 4 ; }$   
4: Obtaining the initial optimal value of $\mathcal { P } 2 , \mathcal { F } ( k ) ;$   
5: Initializing a $Q$ table, $\forall s \in S _ { s } \ \& \ \forall a \in A _ { s } ;$   
$/ { } ^ { * }$ Updating the $Q$ table and $\mathcal { F } ( k ) . ~ ^ { * } /$   
6: for $k = 0$ to $K$ do   
7: for $t = 1$ to $\frac { T } { \Delta T }$ do   
8: for $s \in  { S } _ { s }  { \overline { { ( t ) } } }$ do   
9: Selecting an action a $( a \in \mathcal { A } _ { s } )$ with $\varepsilon - g r e e d y ;$   
10: Calculating the corresponding possibility $\pi ( a | s )$   
with the strategy in the Actor network;   
11: Calculating the Q value with the strategy in the   
Critic network, $Q ( s , a ) ;$   
$/ { } ^ { * }$ Calculating rewards. \*/   
12: if $( \rho ^ { \prime } ( \mathrm { c o v . } ) > \rho ( \mathrm { c o v . } ) )$ then   
13: Calculating the positive reward $r _ { c } ( k )$   
14: else   
15: Calculating the negative reward $p _ { c } ( k ) ;$   
16: end if   
17: if $( R _ { \mathrm { m a x } } > R _ { \mathrm { m a x } } ^ { \prime } )$ then   
18: Calculating the positive reward $r _ { h } ( k ) ;$   
19: else   
20: Calculating the negative reward $p _ { h } ( k ) ;$   
21: end if   
22: if $( S T D ( R ) > S T D ( R ) ^ { \prime } )$ then   
23: Calculating the positive reward $r _ { d } ( k ) ;$   
24: else   
25: Calculating the negative reward $p _ { d } ( k ) _ { \astrosun }$   
26: end if   
27: Obtaining the instant reward, $\mathcal { R } _ { s } ( s , a )$ , and the   
updated value of $\mathcal { P } 2 , \mathcal { F } ^ { \prime } ( k ) ;$   
28: if $( \mathcal { F } ^ { \prime } ( k ) < \mathcal { F } ( k ) )$ then   
29: $\mathcal { F } ( k )  \mathcal { F } ^ { \prime } ( k ) ;$   
30: end if   
31: Updating the state after executing $a , s \to s ^ { \prime } ;$   
32: Calculating the Q value with the strategy in the   
Critic network, $Q ( s ^ { \prime } , a )$ ;   
33: Calculating the Temporal Difference, $\delta \quad =$   
$\mathcal { R } _ { s } ( s , a ) + \gamma \cdot Q ( s ^ { \prime } , a ) - Q ( s , a )$ ;   
34: Updating weights in the Critic network;   
35: Calculating the loss function in the Actor network,   
$F _ { l o s s } = - \delta \cdot \log \pi ( a | s ) ;$   
36: Updating weights in the Actor network;   
37: if (convergence) then   
38: Determining the location for $s _ { k } ( x _ { k } , y _ { k } , z _ { k } )$ with   
$\mathcal { F } ( k )$ ;   
39: else   
40: $s \gets s ^ { \prime } ,$ repeat steps: $9 \sim 3 6 ;$   
41: end if   
42: end for   
43: end for   
44: end for

Observation: Assuming that agents could communicate with each other to obtain locations of hovering points and associations between ground users and hovering points, therefore, for $s _ { k }$ in the t-th time-slot, the local observation space $\mathcal { O } _ { s _ { k } } ( t ) \in \mathcal { O } _ { s _ { k } } \ ( \forall t \in \{ 1 , 2 , \cdot \cdot \cdot , \frac { T } { \Delta T } \} )$ could be defined as $\mathcal { O } _ { s _ { k } } ( t ) = \{ s _ { 0 } , \cdot \cdot \cdot , s _ { K } , y _ { k } ^ { n } \}$ , and the global observation space could be further defined as $\mathcal { O } _ { s } \overset { \Delta } { = } \{ \mathcal { O } _ { s _ { k } } ( t ) \}$

Reward: To improve the search efficiency of location planning while satisfying defined constraints, and obtain optimal location planning for the departure station and hovering points of UAVs, negative and positive rewards could be introduced from perspectives of the full coverage that serving areas of hovering points should cover all ground users, the reduction of the maximum in minimum hop counts between ground users and their candidate serving UAVs, and the reduction of the standard deviation in minimum hop counts.

(1) To enable the full coverage with Constraint 4 that serving areas of determined hovering points could cover all ground users, for each action choice while the UAV flying into the service coverage area of the k-th hovering point, with the assumption that the reward has a linear relationship with the percentage increase in coverage rate, if the achieved coverage rate of ground users could be increased, the agent would be given a positive reward defined as

$$
r _ { c } ( k ) = r _ { c o v . } ^ { p o s . } \cdot \frac { \rho ^ { \prime } ( \mathrm { c o v } ) . - \rho ( \mathrm { c o v . } ) } { \rho ( \mathrm { c o v . } ) } ,\tag{18}
$$

where $r _ { c o v . } ^ { p o s . } ~ = ~ 1$ is the reward coefficient, $\rho ^ { \prime } ( \mathrm { c o v . } )$ is the coverage rate achieved with the current action choice, and $\rho ( \mathrm { c o v . } )$ is the historically optimal coverage rate achieved with action choices. Otherwise, if there are uncovered ground users, the agent would be given a penalty for incomplete coverage, which could be defined as

$$
p _ { c } ( k ) = - r _ { c o v . } ^ { n e g . } \cdot N ( u n c o v . ) ,\tag{19}
$$

where $r _ { c o v . } ^ { n e g . } = 1$ is the penalty coefficient, and N(uncov.) is the number of uncovered ground users.

(2) With ${ \mathcal { P } } 2 ,$ , to ensure the reduction of the maximum in minimum hop counts between ground users and their candidate serving UAVs, for each action choice while the UAV flying into the service coverage area of the k-th hovering point, with the assumption that the reward has a linear relationship with the percentage reduction of maximum in minimum hop counts, if the maximum in minimum hop counts could be declined, the agent would be given a positive reward defined as

$$
r _ { h } ( k ) = r _ { h o p } ^ { p o s . } \cdot \frac { R _ { \operatorname* { m a x } } - R _ { \operatorname* { m a x } } ^ { \prime } } { R _ { \operatorname* { m a x } } } ,\tag{20}
$$

where $r _ { h o p } ^ { p o s . } ~ = ~ 1$ is the reward coefficient, $R _ { \mathrm { m a x } } ^ { \prime }$ is the maximum in minimum hop counts achieved with the current action choice, $R _ { \mathrm { m a x } }$ is the historically optimal maximum in minimum hop counts achieved with action choices. Otherwise, with the assumption that the penalty has a linear relationship with the percentage increase of maximum in minimum hop counts, the agent would given a penalty for violating P2, which could be defined as

TABLE II  
CONFIGURATIONS OF SIMULATION PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Values</td></tr><tr><td rowspan=1 colspan=1> $\underline { { r _ { g u } } }$ (Communication radius of $\overline { { g u ) } }$ </td><td rowspan=1 colspan=1>1.5 m</td><td rowspan=1 colspan=1> $r _ { u }$ (Communication radius of UAV)</td><td rowspan=1 colspan=1>4m</td></tr><tr><td rowspan=1 colspan=1>Î±(Factor introduced in $\overline { { \mathcal { P } 1 ) } }$ </td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>Î² (Factor introduced in P2)</td><td rowspan=1 colspan=1>0.5</td></tr><tr><td rowspan=1 colspan=1> $\overline { { E _ { m } ^ { f u l l } } }$ (Full energy capacity of $u _ { m } )$ </td><td rowspan=1 colspan=1>200J</td><td rowspan=1 colspan=1> $B _ { m }$ (Uplink frequency bandwidth)</td><td rowspan=1 colspan=1>20 MHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { P _ { k } ^ { i } } }$ (Uplink transmission power of $\overline { { g u _ { k } ^ { i } ) } }$ </td><td rowspan=1 colspan=1>0.02W</td><td rowspan=1 colspan=1> $\underline { { \boldsymbol { g } _ { k } ^ { \imath } } }$ (Uplink channel gain of $\overline { { g u _ { k } ^ { i } ) } }$ </td><td rowspan=1 colspan=1>2 dBi</td></tr><tr><td rowspan=1 colspan=1>0 (Noise power spectral density)</td><td rowspan=1 colspan=1>-124.29 dBm/Hz</td><td rowspan=1 colspan=1>Î´(Energy consumption coefficient of UAV flight)</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $\kappa _ { m }$ (Energy coefficient of $u _ { m } )$ </td><td rowspan=1 colspan=1> $\overline { { 1 \times 1 0 ^ { - 9 } } }$ </td><td rowspan=1 colspan=1> $c _ { m }$ (Computing capacity of $u _ { m } )$ </td><td rowspan=1 colspan=1>1 GHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { D _ { n } } }$ (Data volume of $g u _ { n } )$ </td><td rowspan=1 colspan=1>[0,100] KB</td><td rowspan=1 colspan=1>(Energy consumption coefficient of UAV hovering)</td><td rowspan=1 colspan=1>1</td></tr></table>

$$
p _ { h } ( k ) = - r _ { h o p } ^ { n e g . } \cdot \frac { R _ { \operatorname* { m a x } } ^ { \prime } - R _ { \operatorname* { m a x } } } { R _ { \operatorname* { m a x } } ^ { \prime } } ,\tag{21}
$$

where $r _ { h o p . } ^ { n e g . } = 1$ is the penalty coefficient.

(3) With P2, to ensure the reduction of the standard deviation in minimum hop counts, for each action choice while the UAV flying into the service coverage area of the k-th hovering point, with the assumption that the reward has a linear relationship with the percentage reduction of standard deviation, if the standard deviation in minimum hop counts could be declined, the agent would be given a positive reward defined as

$$
r _ { d } ( k ) = r _ { d e v . } ^ { p o s . } \cdot \frac { S T D ( R ) - S T D ( R ) ^ { \prime } } { S T D ( R ) } ,\tag{22}
$$

where $r _ { d e v . } ^ { p o s . } = 1$ is the reward coefficient, $S T D ( R ) ^ { \prime }$ is the standard deviations achieved with the current action choice and $S T D ( R )$ is the historically optimal standard deviation achieved with action choices. Otherwise, assuming the penalty has a linear relationship with the percentage increase of standard deviation, the agent would given a penalty for violating P2, which could be defined as

$$
p _ { d } ( k ) = r _ { d e v . } ^ { n e g . } \cdot \frac { S T D ( R ) ^ { \prime } - S T D ( R ) } { S T D ( R ) ^ { \prime } } ,\tag{23}
$$

where $r _ { d e v . } ^ { n e g . } = 1$ is the penalty coefficient.

## VI. NUMERICAL RESULTS

## A. Simulation Configurations

In this paper, due to the cost of large-scale deployment and implementation, simulation experiments are conducted for effectively verifying the overall performance of investigations. Python 3.9.0 is used as the programming tool, and experiments are running on the server: Ubuntu 18.04.6 LTS operating system, Intel(R) Xeon(R) Silver 4210R CPU at 2.40GHz, and 64 GB of RAM. Even so, to fully demonstrate the practical feasibility and effectiveness of those investigations, as shown in Fig. 3, we also comprehensively consider attributes of involved entities in a real-world hardware platform, and further configure simulation parameters in Table II.

<!-- image-->

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Product Model</td></tr><tr><td rowspan=1 colspan=1>UAV</td><td rowspan=1 colspan=1>DJI MATRICE 100</td></tr><tr><td rowspan=1 colspan=1>Motor</td><td rowspan=1 colspan=1>DJI 3510</td></tr><tr><td rowspan=1 colspan=1>Electrically controlled model</td><td rowspan=1 colspan=1>DJIE SERIES 620D</td></tr><tr><td rowspan=1 colspan=1>Propeller</td><td rowspan=1 colspan=1>DJI1345s</td></tr><tr><td rowspan=1 colspan=1>Flying control system</td><td rowspan=1 colspan=1>N1</td></tr><tr><td rowspan=1 colspan=1>Charger</td><td rowspan=1 colspan=1>A14-100P1A</td></tr><tr><td rowspan=1 colspan=1>Remote-controller</td><td rowspan=1 colspan=1>C1</td></tr><tr><td rowspan=1 colspan=1>Battery</td><td rowspan=1 colspan=1>TB47D</td></tr></table>

(a) UAV  
<!-- image-->

(b) Data collection terminal of ground user

Fig. 3. Attributes of involved entities in a real-world platform.

## B. Evaluation of Energy Efficiency

Here, to effectively verify the achievement of the desired optimization objective of energy efficiency through reasonable trajectory planning, effectiveness and convergence of the proposed Algorithm 1 for P1 are evaluated.

Given the number of ground users, variations of the value of P1 with the number of UAVs are shown in Fig. 4. In the proposed Algorithm 1, the exploring rate used in Q-learning is adaptive to the number of iterations, therefore, different configurations for the combination of the learning rate Î» and the discount rate Î³ are used to evaluate the achieved effectiveness of Algorithm 1. From Fig. 4, we could clearly see that, along with the increase of the number of ground users, the number of deployed UAVs required to achieve the full converge is increasing as well. Nevertheless, no matter how the combination of Î» and Î³ is configured, the value of P1 is declining through conducting reasonable trajectory planning, which indicates variations of the value of P1 are consistent with the desired optimization objective of energy efficiency, and the effectiveness of Algorithm 1 is well demonstrated.

Given the number of ground users, through deploying the optimal number of UAVs to achieve the full converge, variations of the value of P1 with the number of iterations are shown in Fig. 5. Similarly, different configurations for the combination of Î» and Î³ are used to evaluate the achieved convergence of Algorithm 1. From Fig. 5, we could clearly see that, no matter how the combination of Î» and Î³ is configured, along with the increase of the number of iterations, the convergence of the value of P1 could be well achieved, which indicates that, the convergence of Algorithm 1 is well demonstrated, as well as, with the constraint of limited onboard battery capacities of UAVs, the desired optimization objective of energy efficiency could be well achieved through conducting reasonable trajectory planning.

<!-- image-->  
(a) N=500.

<!-- image-->  
(b) N=1000.

<!-- image-->  
(cï¼ N=1500.

<!-- image-->  
(d) N=2000.

Fig. 4. Variations of the value of P1 with the number of UAVs.  
<!-- image-->  
(a) N=500.

<!-- image-->

<!-- image-->  
(b) N=1000.

(c)N=1500.  
<!-- image-->  
(d) N=2000.  
Fig. 5. Variations of the value of P 1 with the number of iterations.

Given the number of ground users, with the optimal number of deployed UAVs determined by Algorithm 1, the trajectory planning of UAVs is shown in Fig. 6, and we could clearly see that, with the determined optimal number of deployed UAVs, the full coverage is well achieved through ensuring the serving coverage area of each determined hovering point to be visited by only one UAV, and each UAV to make only one return trip for providing complete service, which further indicates that, the effectiveness of Algorithm 1 is well demonstrated, and the desired optimization objective of energy efficiency is well achieved with defined constraints.

<!-- image-->  
(a) N=500.

<!-- image-->  
(b) N=1000.

<!-- image-->  
(c) N=1500.

<!-- image-->  
(d) N=2000.  
Fig. 6. Trajectory planning of UAVs.

## C. Evaluation of Service Fairness

Here, to effectively verify the achievement of the desired optimization objective of service fairness through conducting reasonable location planning for the departure station and hovering points, effectiveness and convergence of the proposed Algorithm 2 for P2 are evaluated, and the two algorithms, multi-agent proximal policy optimization (MAPPO) [37] and multi-agent deep deterministic policy gradient (MADDPG) [38], are used for comparative studies.

â¢ MAPPO: Within the framework of Centralized Training with Decentralized Execution (CTDE), MAPPO could use an Actor network and a Critic network to train multiple agents in a centralized manner, and utilize the global information of all agents during the training phase, however, in the execution phase, each agent could only select an action in terms of the local observations, and the achieved performance might be degraded due to the incomplete observations.

â¢ MADDPG: Within the framework of CTDE, MADDPG uses multiple Actor networks and Critic networks to train multiple agents. However, it is necessary to take longer time to perform the training, and the convergence rate is relatively slow. Additionally, without being influenced by other agents, each agent separately has a Actor network and a Critic network to perform the training operation in terms of the local policy. However, due to being lack of cooperation among agents, the policy of each agent would be prone to the local optimality, which inversely influences the global performance of the algorithm.

<!-- image-->  
(a) N=500.

<!-- image-->  
(b) N=1000.

<!-- image-->  
(cï¼ N=1500.

<!-- image-->  
(d) N=2000.  
Fig. 7. Variations of the value of P2 with the number of hovering points.

Given the number of ground users, variations of the value of P2 with the number of hovering points are shown in Fig. 7, and we could clearly see that, along with the increase of the number of ground users, the number of determined hovering points required to achieve the full converge is increasing as well. Nevertheless, for the three comparative algorithms, the obtained value of P2 is declining, which indicates that, variations of the value of P2 are consistent with the desired optimization objective of service fairness, and multi-agent deep reinforcement learning algorithms are suitable for solving the problem of defined continuous MDP. For the proposed Algorithm 2, in each time-slot, with well designed reward functions, the Critic network and the Actor network could cooperatively update involved weights through separately calculating the Temporal Difference, $\delta = \mathcal { R } _ { s } ( s , a ) + \gamma \cdot Q ( s ^ { \prime } , a ) -$ $Q ( s , a )$ , and the loss function, $F _ { l o s s } ~ = ~ - \delta ~ \cdot ~ \log \pi ( a | s )$ maximizing cumulative rewards of long-term expectations therefore could be achieved. Accordingly, the obtained value of P2 is the best in them obtained by the three comparative algorithms, which indicates that the effectiveness of Algorithm 2 is well demonstrated.

Given the number of ground users, through deploying the optimal number of hovering points to achieve the full converge, variations of the value of P2 with the number of iterations are shown in Fig. 8. For the three comparative algorithms, due to conducting the cooperation between the Critic network and the Actor network to find the optimal solution in Algorithm 2, there is a faster convergence of the value of P2, which indicates that, the convergence of Algorithm 2 is well demonstrated, as well as, with the constraint of limited onboard battery capacities of UAVs, the desired optimization objective of service fairness could be well achieved through conducting reasonable location planning for hovering points.

Given the number of ground users, with the optimal number of hovering points determined by Algorithm 2, the location planning of hovering points is shown in Fig. 9, and we could clearly see that, with the determined optimal number of hovering points, the full coverage is well achieved through ensuring the serving coverage area of each determined hovering point to be visited by only one UAV, and each ground user to be only associated with a hovering point of UAV, which further indicates that, the effectiveness of Algorithm 2 is well demonstrated, and the desired optimization objective of service fairness is well achieved with defined constraints.

<!-- image-->  
(a) N=500.

<!-- image-->  
(b) $N { = } 1 0 0 0 .$

<!-- image-->  
(c) N=1500.

<!-- image-->  
(d) $N { = } 2 0 0 0 .$

Fig. 8. Variations of the value of P 2 with the number of iterations.  
<!-- image-->  
(a) N=500.

<!-- image-->  
(b) N=1000.

<!-- image-->  
ï¼cï¼ $N { = } 1 5 0 0 .$

<!-- image-->  
(d) N=2000.  
Fig. 9. Location planning of hovering points.

## VII. CONCLUSION AND FUTURE WORK

In UAVs empowered aerial computing systems, to improve the energy efficiency of UAVs and the service fairness experienced by ground users while achieving reasonable computing power scheduling, a joint optimization with constraints is formulated in this paper. Through considering complex coupling associations among the departure station, flight paths and hovering points, the trajectory planning of UAVs is conducted to maximize the energy efficiency, and the location planning for both the departure station and hovering points is conducted to maximize the service fairness. As promising solutions, investigated problems are firstly proven to be Markov decision processes, on the basis, a multi-agent cooperative Q-learning approach is proposed for optimizing trajectory planning while maximizing the energy efficiency, and a policy optimization based multi-agent cooperative deep reinforcement learning approach using the architecture of Actor-Critic is proposed for optimizing location planning while maximizing the service fairness. Comparative experiments show that the performance achieved by investigations has obvious advantages.

With the development of emerging intelligent services in 6G mobile systems, to satisfy multi-dimensional extreme performance requirements, it is necessary to deeply integrate the wireless sensing function with the wireless transmission function, and use the ubiquitous computing power for auxiliary computation. In this context, UAVs empowered aerial computing systems would be a powerful complement for the integration of sensing, communication, and computing for edge intelligence in 6G networks, therefore, formulating more complete optimization models with more comprehensive considerations of inherent limitations of UAVs and diverse requirements of ground users, and comparing more versions of multi-agent reinforcement learning algorithms, are still interests for conducting further explores. Especially, the relevant research progress would be migrated and applied into integrated Ground-Air-Space wireless networks for 6G mobile.

## REFERENCES

[1] X. Wang et al., âWireless powered mobile edge computing networks: A survey,â ACM Comput. Surv., vol. 55, no. 135, pp. 1â37, 2023.

[2] X. Xia, S. M. M. Fattah, and M. A. Babar, âA survey on UAV-enabled edge computing: Resource management perspective,â ACM Comput. Surv., vol. 56, no. 3, pp. 1â36, Mar. 2024.

[3] X. Zhou et al., âSpatialâTemporal federated transfer learning with multisensor data fusion for cooperative positioning,â Inf. Fusion, vol. 105, May 2024, Art. no. 102182.

[4] M. Tao, X. Li, H. Yuan, and W. Wei, âUAV-aided trustworthy data collection in federated-WSN-enabled IoT applications,â Inf. Sci., vol. 532, pp. 155â169, Sep. 2020.

[5] F. Zhou, Y. Wu, R. Q. Hu, and Y. Qian, âComputation rate maximization in UAV-enabled wireless-powered mobile-edge computing systems,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1927â1941, Sep. 2018.

[6] H. Chen, M. Xiao, and Z. Pang, âSatellite-based computing networks with federated learning,â IEEE Wireless Commun., vol. 29, no. 1, pp. 78â84, Feb. 2022.

[7] W. Wu, F. Zhou, B. Wang, Q. Wu, C. Dong, and R. Q. Hu, âUnmanned aerial vehicle swarm-enabled edge computing: Potentials, promising technologies, and challenges,â IEEE Wireless Commun., vol. 29, no. 4, pp. 78â85, Aug. 2022.

[8] Z. Wei et al., âUAV-assisted data collection for Internet of Things: A survey,â IEEE Internet Things J., vol. 9, no. 17, pp. 15460â15483, Sep. 2022.

[9] C. Zhan and Y. Zeng, âCompletion time minimization for multi-UAVenabled data collection,â IEEE Trans. Wireless Commun., vol. 18, no. 10, pp. 4859â4872, Oct. 2019.

[10] X. Yuan, Y. Hu, J. Zhang, and A. Schmeink, âJoint user scheduling and UAV trajectory design on completion time minimization for UAVaided data collection,â IEEE Trans. Wireless Commun., vol. 22, no. 6, pp. 3884â3898, Jun. 2023.

[11] J. Gong, T.-H. Chang, C. Shen, and X. Chen, âFlight time minimization of UAV for data collection over wireless sensor networks,â IEEE J. Sel. Areas Commun., vol. 36, no. 9, pp. 1942â1954, Sep. 2018.

[12] X. Li, J. Tan, A. Liu, P. Vijayakumar, N. Kumar, and M. Alazab, âA novel UAV-enabled data collection scheme for intelligent transportation system through UAV speed control,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 4, pp. 2100â2110, Apr. 2021.

[13] Y. Li et al., âData collection maximization in IoT-sensor networks via an energy-constrained UAV,â IEEE Trans. Mobile Comput., vol. 22, no. 1, pp. 159â174, Jan. 2023.

[14] M. Samir, S. Sharafeddine, C. M. Assi, T. M. Nguyen, and A. Ghrayeb, âUAV trajectory planning for data collection from time-constrained IoT devices,â IEEE Trans. Wireless Commun., vol. 19, no. 1, pp. 34â46, Jan. 2020.

[15] T. Yuan, C. E. Rothenberg, K. Obraczka, C. Barakat, and T. Turletti, âHarnessing UAVs for fair 5G bandwidth allocation in vehicular communication via deep reinforcement learning,â IEEE Trans. Netw. Service Manag., vol. 18, no. 4, pp. 4063â4074, Dec. 2021.

[16] H. Hu, K. Xiong, G. Qu, Q. Ni, P. Fan, and K. B. Letaief, âAoI-minimal trajectory planning and data collection in UAV-assisted wireless powered IoT networks,â IEEE Internet Things J., vol. 8, no. 2, pp. 1211â1223, Jan. 2021.

[17] B. Zhu, E. Bedeer, H. H. Nguyen, R. Barton, and Z. Gao, âUAV trajectory planning for AoI-minimal data collection in UAV-aided IoT networks by transformer,â IEEE Trans. Wireless Commun., vol. 22, no. 2, pp. 1343â1358, Feb. 2023.

[18] X. Gao, X. Zhu, and L. Zhai, âAoI-sensitive data collection in multi-UAV-assisted wireless sensor networks,â IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5185â5197, Aug. 2023.

[19] Y. Wang et al., âTrajectory design for UAV-based Internet of Things data collection: A deep reinforcement learning approach,â IEEE Internet Things J., vol. 9, no. 5, pp. 3899â3912, Mar. 2022.

[20] K. K. Nguyen, T. Q. Duong, T. Do-Duy, H. Claussen, and L. Hanzo, â3D UAV trajectory and data collection optimisation via deep reinforcement learning,â IEEE Trans. Commun., vol. 70, no. 4, pp. 2358â2371, Apr. 2022.

[21] G. Chen, X. B. Zhai, and C. Li, âJoint optimization of trajectory and user association via reinforcement learning for UAV-aided data collection in wireless networks,â IEEE Trans. Wireless Commun., vol. 22, no. 5, pp. 3128â3143, May 2023.

[22] X. Fan, M. Liu, Y. Chen, S. Sun, Z. Li, and X. Guo, âRIS-assisted UAV for fresh data collection in 3D urban environments: A deep reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 72, no. 1, pp. 632â647, Jan. 2023.

[23] Y. Liu et al., âLatency optimization for multi-UAV-assisted task offloading in air-ground integrated millimeter-wave networks,â IEEE Trans. Wireless Commun., vol. 23, no. 10, pp. 13359â13376, Oct. 2024.

[24] Z. Shah, U. Javed, M. Naeem, S. Zeadally, and W. Ejaz, âMobile edge computing (MEC)-enabled UAV placement and computation efficiency maximization in disaster scenario,â IEEE Trans. Veh. Technol., vol. 72, no. 10, pp. 13406â13416, May 2023.

[25] C. Yang, B. Liu, H. Li, B. Li, K. Xie, and S. Xie, âLearning based channel allocation and task offloading in temporary UAV-assisted vehicular edge computing networks,â IEEE Trans. Veh. Technol., vol. 71, no. 9, pp. 9884â9895, Sep. 2022.

[26] S. Goudarzi, S. A. Soleymani, W. Wang, and P. Xiao, âUAV-enabled mobile edge computing for resource allocation using cooperative evolutionary computation,â IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 5, pp. 5134â5147, Jul. 2022.

[27] K. Cheng, X. Fang, and X. Wang, âEnergy efficient edge computing and data compression collaboration scheme for UAV-assisted network,â IEEE Trans. Veh. Technol., vol. 72, no. 12, pp. 16395â16408, Aug. 2023.

[28] W. Zhou et al., âPriority-aware resource scheduling for UAV-mounted mobile edge computing networks,â IEEE Trans. Veh. Technol., vol. 72, no. 7, pp. 9682â9687, Jul. 2023.

[29] N. T. Hoa, D. V. Dai, L. H. Lan, N. C. Luong, D. V. Le, and D. Niyato, âDeep reinforcement learning for multi-hop offloading in UAV-assisted edge computing,â IEEE Trans. Veh. Technol., vol. 72, no. 12, pp. 16917â16922, Dec. 2023.

[30] L. T. Hoang, C. T. Nguyen, and A. T. Pham, âDeep reinforcement learning-based online resource management for UAV-assisted edge computing with dual connectivity,â IEEE/ACM Trans. Netw., vol. 31, no. 6, pp. 2761â2776, May 2023.

[31] W. Lei, Y. Ye, and M. Xiao, âDeep reinforcement learning-based spectrum allocation in integrated access and backhaul networks,â IEEE Trans. Cognit. Commun. Netw., vol. 6, no. 3, pp. 970â979, Sep. 2020.

[32] N. Qi et al., âA learning-based spectrum access Stackelberg game: Friendly jammer-assisted communication confrontation,â IEEE Trans. Veh. Technol., vol. 70, no. 1, pp. 700â713, Jan. 2021.

[33] I.-J. Liu, U. Jain, R. A. Yeh, and A. Schwing, âCooperative exploration for multi-agent deep reinforcement learning,â in Proc. 38th Int. Conf. Mach. Learn., Vienna, Austria, 2021, pp. 6826â6836.

[34] T. Yuan, H.-M. Chung, J. Yuan, and X. Fu, âDACOM: Learning delay-aware communication for multi-agent reinforcement learning,â in Proc. AAAI Conf. Artif. Intell., Washington, DC, USA, Jun. 2023, pp. 11763â11771.

[35] T. Zhang, Q. Ye, J. Bian, G. Xie, and T.-Y. Liu, âMFVFD: A multiagent Q-learning approach to cooperative and non-cooperative tasks,â in Proc. 30th Int. Joint Conf. Artif. Intell., Aug. 2021, pp. 500â506.

[36] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, âMultiagent actor-critic for mixed cooperative-competitive environments,â in Proc. 31st Conf. Neural Inf. Process. Syst., Long Beach, CA, USA, 2017, pp. 6382â6393.

[37] Y. Guan, S. Zou, K. Li, W. Ni, and B. Wu, âMAPPO-based cooperative UAV trajectory design with long-range emergency communications in disaster areas,â in Proc. IEEE 24th Int. Symp. a World Wireless, Mobile Multimedia Netw. (WoWMoM), Boston, MA, USA, Jun. 2023, pp. 376â381.

[38] J. Du et al., âMADDPG-based joint service placement and task offloading in MEC empowered airâground integrated networks,â IEEE Internet Things J., vol. 11, no. 6, pp. 10600â10615, Mar. 2024.

<!-- image-->

Ming Tao (Member, IEEE) received the B.S. degree in computer science and technology from Anhui University, Hefei, China, in 2007, and the M.S. and Ph.D. degrees in computer application technology from the South China University of Technology, Guangzhou, China, in 2009 and 2012, respectively. He was also a Visiting Scholar with the Department of Information and Electronic Engineering, Muroran Institute of Technology, Japan. Currently, he is a Professor with the School of Computer Science and Technology, Dongguan University of Technology,

Dongguan, China, and the Director of the Key Laboratory of the Wireless Sensor Network System of Dongguan. His primary research interests include protocol design and performance analysis in next-generation wireless/mobile networks and AI+edge computing/cloud computing.

<!-- image-->

Xueqiang Li received the B.S. degree in information and computing science from Zhengzhou University of Light Industry, Zhengzhou, China, in 2006, the M.S. degree in computer science from Guangdong University of Technology, Guangzhou, China, in 2009, and the Ph.D. degree in computer application technology from the South China University of Technology, Guangzhou, in 2012. He is currently a Lecturer with the School of Computer Science and Technology, Dongguan University of Technology, Dongguan, China. His research interests

include edge computing and evolutionary computation.

<!-- image-->

Jie Feng (Member, IEEE) received the Ph.D. degree in communication and information systems from Xidian University, Xiâan, China, in 2020. From 2018 to 2019, she was a Visiting Ph.D. Student with Carleton University, Ottawa, ON, Canada. She is currently an Associate Professor with the Department of Electrical Engineering and Computer Science, Xidian University. Her current research interests include mobile-edge computing, blockchain, deep reinforcement learning, device-todevice communication, resource allocation, convex

optimization, and stochastic network optimization.

<!-- image-->

Dapeng Lan (Member, IEEE) received the B.Eng. degree in microelectronics from Sun Yat-sen University, Guangzhou, China, in 2014, the M.Sc. degree in information and communication technology (ICT) innovation from the KTH Royal Institute of Technology, Stockholm, Sweden, in 2016, the M.Sc. degree in innovation (information and communication technology) from the Technical University of Berlin, Berlin, Germany, in 2017, and the Ph.D. degree from the Department of Informatics, University of Oslo, Norway, in 2022. Formerly, he was a Post-Doctoral

Research Fellow with the Department of Informatics, University of Oslo. He currently holds the position of an Associate Professor with Shenyang Institute of Automation, Chinese Academy of Sciences, and a Guest Researcher with the University of Oslo. His research interests include edge computing, the Internet of Things, and industrial digitalization.

<!-- image-->

Jun Du (Senior Member, IEEE) received the B.S. degree in information and communication engineering from Beijing Institute of Technology, in 2009, and the M.S. and Ph.D. degrees in information and communication engineering from Tsinghua University, Beijing, in 2014 and 2018, respectively. From October 2016 to September 2017, she was a Sponsored Researcher. She visited the Imperial College London. Currently, she is an Assistant Professor with the Department of Electrical Engineering, Tsinghua University. Her research interests

are mainly in communication, networking, resource allocation and system security problems of heterogeneous networks, and space-based information networks. She has authored/co-authored more than 90 technical papers in renowned international journals and conferences, including more than 40 renowned IEEE journal articles. She was a recipient of the Best Student Paper Award from IEEE GlobalSIP in 2015, the Best Paper Award from IEEE ICC 2019, the first prize of Innovation Innovation Award from China Association of Invention in 2023, the Best Paper Award from IWCMC in 2020, WuWenJun Young Elite Scientist Award from CAAI (Chinese Association for Artificial Intelligence) in 2020, and the First Prize in Technical Inventions Award from The Chinese Institute of Electronics (CIE) in 2020.

<!-- image-->

Celimuge Wu (Senior Member, IEEE) received the Ph.D. degree from The University of Electro-Communications, Japan. He is currently a Professor and the Director of the Meta-Networking Research Center, The University of Electro-Communications. His research interests include vehicular networks, edge computing, the IoT, and AI for wireless networking and computing. He serves as an Associate Editor for IEEE TRANSACTIONS ON COGNITIVE COMMUNICATIONS AND NET-WORKING, IEEE TRANSACTIONS ON NETWORK

SCIENCE AND ENGINEERING, and IEEE TRANSACTIONS ON GREEN COM-MUNICATIONS AND NETWORKING. He is the Vice Chair (Asia Pacific) of IEEE Technical Committee on Big Data (TCBD). He was a recipient of 2021 IEEE Communications Society Outstanding Paper Award, 2021 IEEE Internet of Things Journal Best Paper Award, IEEE Computer Society 2020 Best Paper Award, and IEEE Computer Society 2019 Best Paper Award Runner-Up. He is an IEEE Vehicular Technology Society Distinguished Lecturer.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_4_img_1.jpeg|page_4_img_1]]
2. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_1.jpeg|page_11_img_1]]
3. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_2.jpeg|page_11_img_2]]
4. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_3.jpeg|page_11_img_3]]
5. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_4.jpeg|page_11_img_4]]
6. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_5.jpeg|page_11_img_5]]
7. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_6.jpeg|page_11_img_6]]
8. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_7.png|page_11_img_7]]
9. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_8.jpeg|page_11_img_8]]
10. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_9.jpeg|page_11_img_9]]
11. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_10.jpeg|page_11_img_10]]
12. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_11.jpeg|page_11_img_11]]
13. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_11_img_12.jpeg|page_11_img_12]]
14. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_1.jpeg|page_13_img_1]]
15. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_2.jpeg|page_13_img_2]]
16. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_3.jpeg|page_13_img_3]]
17. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_4.jpeg|page_13_img_4]]
18. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_5.jpeg|page_13_img_5]]
19. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_6.jpeg|page_13_img_6]]
20. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_7.jpeg|page_13_img_7]]
21. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_8.jpeg|page_13_img_8]]
22. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_9.jpeg|page_13_img_9]]
23. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_10.jpeg|page_13_img_10]]
24. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_11.jpeg|page_13_img_11]]
25. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_12.jpeg|page_13_img_12]]
26. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_13.jpeg|page_13_img_13]]
27. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_14.jpeg|page_13_img_14]]
28. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_15.jpeg|page_13_img_15]]
29. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_16.jpeg|page_13_img_16]]
30. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_17.jpeg|page_13_img_17]]
31. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_18.jpeg|page_13_img_18]]
32. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_19.jpeg|page_13_img_19]]
33. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_20.jpeg|page_13_img_20]]
34. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_21.jpeg|page_13_img_21]]
35. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_22.jpeg|page_13_img_22]]
36. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_23.png|page_13_img_23]]
37. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_24.jpeg|page_13_img_24]]
38. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_25.jpeg|page_13_img_25]]
39. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_26.jpeg|page_13_img_26]]
40. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_13_img_27.jpeg|page_13_img_27]]
41. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_1.png|page_15_img_1]]
42. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_2.png|page_15_img_2]]
43. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_3.png|page_15_img_3]]
44. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_4.png|page_15_img_4]]
45. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_5.jpeg|page_15_img_5]]
46. [[../extracted_images/Tao 等 - 2024 - Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems/page_15_img_6.jpeg|page_15_img_6]]

---

