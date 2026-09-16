# 3D Trajectory Optimization for Multimission UAVs in Smart City Scenarios

Nicola Roberto Zema , Enrico Natalizio , Senior Member, IEEE, Luigi Di Puglia Pugliese , and Francesca Guerriero , Member, IEEE

AbstractâThere is a definite possibility that, in a recent future, Unmanned Aerial Vehicles (UAVs) will form the backbone of any smart city in terms of automation and networking. One approach to extend the UAVsâ resources spectrum is to provide a mean for them to opportunistically recharge and connect to otherwise unreachable networks: provide Training and Recharge Areas (TRAs). In these dedicated areas, the UAVs could dock to Energy and Data Dispensers (EDD) devices to resupply their batteries and exploit a high-speed connection. To autonomously move through the smart city while accomplishing a set of given tasks but, at the same time, consider visiting the EDDs, is part of a tridimensional trajectory planning problem that needs to be addressed. In this paper, we formally define the combinatorial optimization problem representing the trajectory planning. We consider the case in which more than one UAV can be connected with the same EDD at the same time, by properly addressing the assignment of the bandwidth. Through simulative investigation, realistic values for the solution of the optimization problem are found. The behavior of the proposed model is compared with an âonlineâ approach that does not require the same resources and knowledge and whose evaluation and comparison with the âofflineâ approach are performed through network simulation.

Index TermsâDistributed control systems, MILP, reactive planning, wireless networks

O the best of our knowledge, besides our preliminary work [1], the tridimensional trajectory definition problem with bandwidth and time constraints has not been investigated in the literature.

## 1 INTRODUCTION

UAVs will play an important role in the future of our Smart Cities, thanks to the large spectrum of applications that could exploit their cheapness, effectiveness and reconfigurability, such as parcel delivery, infrastructure monitoring, event filming, surveillance, tracking, etc.

However, two main factors can affect their performance in carrying out varied missions: the energy consumption and the behavior required to handle the missions. A great deal of effort has been dedicated to the trajectory planning of multi-UAV fleets that try to optimize different parameters and, specifically, network and energy parameters [2], [3]. A stark example is the smart-city scenario, where multiple UAVs are deployed to accomplish a mission while maintaining connectivity among each other as well as having to plan careful trajectories for maximizing their battery endurance. The smart-city is plentiful of building roofs, where the UAVs could land or hover upon. In this scenario, we envisage the deployment of Training and Recharging areas (TRA) (Fig. 1), where the UAV can approach the energy and data dispensers (EDD) deployed in the TRA, in order to recharge their batteries by wireless energy transfer [4], as well as to download the latest software updates to modify their behavior in preparation for a new mission.

In fact, the UAVsâ response time to the request of a new mission is of paramount importance. Therefore, the time spent within the TRA represents a hard constraint to satisfy while moving towards the Mission Area (MA). Furthermore, we assume that the EDDs have a limited instantaneous capacity to distribute to the connected UAVs, in terms of both energy and bandwidth. Hence, each UAV must define an optimal movement trajectory within the TRAs, by taking into account the EDD limited capacity. The ideal trajectory is the one that would allow the UAV to exit the TRA in a predefined time, while connecting to the EDDs on the path to completely recharge their batteries as well as to download all the required updates.

The definition of the best trajectory to cross the TRA is the objective of this work. It is worth noting that the best trajectory definition can be considered as a more general problem, whose solution could be beneficial for numerous applications.

We use two methodological approaches to design strategies useful to determine the best trajectory: an offline approach based on the mathematical formulation of the problem, and an online approach based on the local information available at the UAVs. Both of them consider a tridimensional space. To find realistic values for the optimization problem parameters, we have chosen to create exemplary and static scenarios with the NS3 simulator [5], which capture the essence of communications between UAVs and EDDs, run evaluations on the performances of data transfers between them, and use these results as parameters for finding solutions to the optimization problem. At the same time, the online solution has been implemented as a mobility model in NS3 and the simulated nodes perform the data transfers with distances, propagation models and medium access taken into consideration by the simulator. To compare them meaningfully, we also extrapolate the optimization model solution and implement and compare against the offline model in NS3. To the best of our knowledge, besides our preliminary work [1], the tridimensional trajectory definition problem with bandwidth and time constraints has not been investigated in the literature.

<!-- image-->  
Fig. 1. Training and Recharging Area (TRA) and Mission Areas (MA) for UAVs in a Smart City scenario.

## 1.1 Contribution

In comparison to the literature on the trajectory planning problem and its solution approaches, our work presents the following novel contributions:

we introduce a new trajectory planning problem for UAVs that takes into account time and bandwidth constraints for a required data transfer in a tridimensional space;

we formulate the problem as a mixed integer linear program that linearizes the general model presented in [1];

we compare the found solution with an online approach that determines an efficient trajectory by using only information locally available at the UAVs;

we find optimization parameters through preliminary simulations in NS3 and implement the online solution in the same environment.

The rest of the paper is organized as follows: in Section 3, we introduce the general problem and the networking aspect related to it; in Section 3.2, we specialize the problem to a relaxed version that can be solved by using offline solution methods; Section 3.3 presents our online approach to solve the problem only by using local information available at the drone during their flight time; Section 4 shows the results of simulation and Section 5 concludes the paper.

## 2 RELATED WORKS

Multi robot trajectory planning is a domain that continues to attract a considerable amount of effort and specifically the problem of defining the best trajectory of a set of robots through a field of recharging stations has been investigated [2]. Still, a tridimensional MILP formulation, that takes in consideration also networking constraints and input from a networking simulation for bandwidth estimation, has not been considered in the scientific literature [3], [6], [7]. Most recent works focus either on single UAV [8] or on results obtained with simulative solutions not specifically designed for networking [8], [9]. At the same time, fully online algorithms, which seek for sub-optimal solutions, are even more lacking [10] and, to the authorsâ knowledge, they have not been yet benchmarked against optimal solution strategies. We split this Section into two subsections showcasing the works related to problems similar to that of our work and solution approaches, respectively.

## 2.1 3D Trajectory Planning With Time and Capacity Constraints

In robotics literature, the difference between the path planning and trajectory planning is described as the latter being a further refinement of the former [11]. When a path is found between a starting and an end point, if it is possible to describe it as a function of time, then it becomes a trajectory.

The trajectory planning problem, at hand, presents two main features: dispatching of vehicles and vehicle routing under communication constraints. Usually, the two features are considered separately by the scientific literature.

In particular, referring to the dispatching problem of vehicles, a pair of origin-destination points is associated with each vehicle. The vehicles have to move into a system where resources have to be shared. This kind of problems is common in the logistic field, especially, in transportation networks where the aim is the congestion reduction. In this case the resource is the road [12] but no communication is established among the vehicles.

Even though the literature shows several efforts in studying the best 3D path for different objectives [13], communication issues are taken into account only in the so-called close-enough routing problems [14], [15], [16]. A vehicle, starting from an origin node, has to visit either all or a subset of nodes and return to the destination node. Each node has a communication range. A node is said to be visited by the vehicle, if the latter passes into the communication area of the node. However, the scientific literature does not take into account time constraints in the close-enough routing problems [17].

In [18] the authors propose several formulations dealing with the problem of routing a single vehicle with the aim of collecting data from known deployed base stations within a predefined time horizon. They discretize the time horizon and allow the download of data from all the base stations located in a predefined coverage radius around the vehicle.

The problem of defining a two-dimensional trajectory of a single UAV is addressed in [19]. The UAV can fly at a given altitude. The authors suppose that the data are available at each sensor before a predefined instant time. The aim is to visit the maximum number of sensors.

## 2.2 Solution Approaches

The proposed solutions for the trajectory planning problem can be classified as offline and online approaches. On one side, the offline approaches, such as model predictive control [20], [21], graph theory solutions [22], [23] and Markov decision process techniques [24], [25], are based on a complete knowledge of the problem at each time-step and, usually, on a central point of data collection and solution computation.

In this paper we propose a mixed integer formulation of the problem involving routing, scheduling and communications constraints that focuses on trajectory planning for UAV fleets. The formulation does not include the capacity planning, which is usually performed at the core network. However, as we will show in the next Sections, this approach is impractical because of the knowledge needed to solve the problem and because of the computational resources required at the solver, even for small instances of the problem [18], [19].

On the other side, the online approaches are usually distributed, and do not require a complete knowledge of the context to provide sub-optimal solutions. The current state of the art provides different taxonomies for problems identified as path or trajectory planning with online methodologies [11], [26]. The literature distinguishes static and dynamic approaches, as well as it classifies the proposed solutions according to the knowledge scope needed at each algorithm step. From the point of view of a UAV, the environment is highly dynamic, and its knowledge of the context is limited to short-range real-time observations. In these conditions, the proposed solutions are classified under the name of Sampling Based methods. These methods use repeated environment sampling that is mapped to a model. The most prominent methods in this class are the Rapidlyexploring Random (RRT) Tree algorithm family [27], [28], the Probabilistic Roadmaps (PRM) family [29], Corridor Maps [30], Visibility Graphs [31]. The RTT approach determines paths with sudden and large variations of speed and direction, which are difficult to follow for the UAVs. PRMs, Corridor Maps and Visibility Graphs provide, as solutions, only probable sets of disjoint paths that need to be joined by other means. Recently, game-theory based online planning has been investigated [32]. However, the applicability of the method has been demonstrated only for two devices. The Artificial Potential method [33] creates smooth trajectories, it requires only local information and does not need to join different paths to build a whole trajectory. In our work, we leverage this last method in a way that (i) is implementable as a control model on UAVs for movements in a tridimensional space; (ii) includes real-time network parameters and (iii) provides a feasible solution, as it avoids local minima by enforcing time constraints on the sojourn duration in the TRA.

## 3 PROBLEM FORMULATION

In this Section we formally define the problem. We highlight that a general formulation is given in [1] where the optimization is given in the continuous space. The formulation is general in the sense that it provide an overview of the fundamental of the considered problem. Under an optimization view point, the general model needs to be specified by defining a linear program. This means to formulate the general feasible region in terms of linear constraints. The transformation goes through a relaxation of the general problem. Indeed, we need to discretize the tridimensional space. In addition, as shown later, both integer and continuous variables have to be defined. It follows that the proposed formulation is a mixed integer linear program (MILP). In the next section, we report the network assumptions, then we propose a MILP formulation for the addressed problem.

<!-- image-->  
Fig. 2. Scheme of two UAVs, at distance $d _ { 1 }$ and $d _ { 2 } ,$ connected to an EDD installed on the roof of a building.

## 3.1 Network Assumptions

Our work is based on a working scenario that captures the essence of the deployment of a UAV fleet and the placement of the EDD in a Smart City. As illustrated in Fig. 2, our scenario is a TRA where the EDDs placed on the buildingsâ rooftops. EDDs and UAVs can transfer data through digital wireless communications over a shared medium. To provide an estimation of the data transfer capabilities between EDDs and UAVs, we need to consider multiple factors, notably: the distance between the EDD and the UAV; the physical shared medium conditions and the interference generated by multiple simultaneous communications sharing the medium. Focusing only on a pair EDD-UAV, in absence of other parties, the communication bandwidth is dependent on the signal-to-noise ratio at the receiver (SNR) UAV. The value of SNR, for an Additive White Gaussian Noise (AWGN) channel with noise power $\sigma ^ { 2 }$ channel is

$$
S N R = \frac { R S S } { \sigma ^ { 2 } + R S S } .\tag{1}
$$

In Equation (1) the RSS is the received signal strength at the receiver. Devices available on the market and the protocols they implement have usually the possibility to do on-line analysis of channel conditions and modify their protocols parameters accordingly. In the IEEE 802 family, the devices involved in data exchange agree on these parameters through the implementation of a rate control algorithm [34], which usually samples the channel periodically.

Without real equipment, to estimate the RSS is a complex task and different techniques could be used, from the application of simulated ray-tracing to simplistic statistical propagation models [35].

However, after having a grasp of the signal strength evolution between two devices, then it is necessary to consider the interference generated by other devices on the same shared medium. The task is not simple and, for large numbers of devices, simulative approaches are the most used solutions as they apply propagation models when multiple transmission are supposed to superimpose.

For this reason, in this work we first give a general estimation of the bandwidth between communication actors and then, before computing a solution, we use a network simulator to compute the bandwidths between EDDs and UAVs.

For the following, if we suppose that multiple UAVs connected to an EDD on a shared medium with equal repartition of the bandwidth, the following holds

$$
B ( w ) = \frac { C _ { w } } { N _ { \mathrm { U A V } , w } ( t ) } .\tag{2}
$$

In Equation (2), we define that, at the time $t , \ N _ { \mathrm { U A V } , w } ( t )$ UAVs are connected to the EDD w, $B ( w )$ Ã° Ãis the function that Ã° Ãassigns the bandwidth to the UAVs connected to the EDD w. and $C _ { w }$ is an estimation of the total capacity for each EDD w, that depends on the technology used. In the context of this work, we have considered multiple different candidates for the feasible networking technology. Focusing on range and portability issues and how the different solutions address them, we have restricted our choices to two possibilities: (i) the mmWave and (ii) the IEEE 802.11 families. We claim that in the context of this work, the usage of mmWave would not be as effective and economically viable as the usage of IEEE 802.11 technology. In detail:

the high directional selectivity of a mmWave antenna, deployed on an EDD, would not allow a group of UAV to benefit of the same high bandwidth;

the need for a LoS link between each UAV and the EDD, would require the installation of tracking systems, which maybe economically feasible on sparse $5 \mathrm { G } / 6 \mathrm { G }$ base stations, but we consider too expensive to be done on dense EDDs;

the beam alignment phase between the UAV and the EDD could represent an unnecessary burden on the time budget of the system.

Therefore, we focused our efforts on the classic WiFi technology based on IEEE 802.11, which ensures a higher flexibility and effectiveness than the mmWave.

## 3.2 Mathematical Model

In this Section, we will show the specific model, which takes into account the assumptions to formulate a relaxed version of the generalized model proposed in [1]. In order to formulate the mixed integer model, we give useful notation in what follows.

We assume that the field is discretized, thus composed of possible positions $i \in V$ that the UAVs can visit. We sup-2pose the discretized space is represented as a tridimensional grid where each node represents a position $i \in V ,$ expressed by the coordinates $( x _ { i } ^ { 1 } , \bar { x _ { i } ^ { 2 } } , x _ { i } ^ { 3 } )$ 2. Let A be the set of arcs $( i , j )$ with $i , j \in V , i \neq j .$ Ã°  The arc $( i , j )$ Ã° Ãdefines the direct connection 2 6Â¼between positions i and $j , \mathrm { i . e . , }$ Ã the UAVs can reach position $j$ starting from position i through the arc i; j . Set A contains only feasible arcs. An arc $( i , j )$ is said to be feasible, if the Ã° Ãline that connects position i and $j$ does not intercept any obstacles, such as walls or buildings.

TABLE 1 Summing up the Variables
<table><tr><td>Variable</td><td>Meaning</td></tr><tr><td> $x _ { i j } ^ { u }$ </td><td>Binary variable.It defines whether the arc  $( i , j ) \in A$  istraversed by  $\mathrm { U A V } u \in U$ </td></tr><tr><td> $T _ { i } ^ { u }$ </td><td>Continuous variable.It defines the arrival time of UAV  $u \in U$  at position  $i \in V$ </td></tr><tr><td> $T e _ { i } ^ { u }$ </td><td>Continuous variable.It defines the departure time of  $\mathrm { U A V } u \in U$  from position  $i \in V$ </td></tr><tr><td> $t s _ { i } ^ { u t }$ </td><td>Continuous variable.Auxiliary variableused to define  $T e _ { i } ^ { u }$ </td></tr><tr><td> $n _ { i } ^ { u t }$ </td><td>Binary variable.It defineswhether  $\mathrm { U A V } u \in U$  is at position  $i \in V$  atinstant time t</td></tr><tr><td> $z _ { w i } ^ { u t }$ </td><td>Binary variable.Itdefineswhether  $\mathrm { U A V } u \in U$  is connected to  $\mathrm { E D D } w \in N$  at time  $t \in T ,$  whenitvisits</td></tr><tr><td> $t _ { i } ^ { u }$ </td><td>position  $i \in V$  Continuous variable.It defines the total time in which  $u \in U$  is connected to EDD w âN from position  $i \in V$ </td></tr></table>

The positions of the EDDs $w \in N$ are known in advance with coordinate $( y _ { w } ^ { 1 } , y _ { w } ^ { 2 } , y _ { w } ^ { 3 } )$ 2. Thus, we can calculate the distance

$$
d _ { w i } = \sqrt { ( y _ { w } ^ { 1 } - x _ { i } ^ { 1 } ) ^ { 2 } + ( y _ { w } ^ { 2 } - x _ { i } ^ { 2 } ) ^ { 2 } + ( y _ { w } ^ { 3 } - x _ { i } ^ { 3 } ) ^ { 2 } }
$$

between each EDD $w \in N$ and each possible position $i \in V$ for the UAVs.

In the following, we define the variables. Let:

$x _ { i j } ^ { u } \in \{ 0 , 1 \}$ be the flow variables that take value 2 f gequal to 1 if the corresponding arc $( i , j ) \in A$ is traversed by $\mathrm { U A V } ~ u \in U , \bar { 0 }$ Ã° Ã 2otherwise. We assume that each UAV $u \in U$ 2performs a path from the entrance point $s _ { u }$ 2to the exit point $d _ { u }$ . Thus, the visited position $i \in N$ appear only once in the path.

$T _ { i } ^ { u }$ ; be continuous variables defining the time in which $\mathrm { U A V } u \in U$ visits position $i \in V .$

$T e _ { i } ^ { u }$ 2 2; be continuous variables defining the time in which $\mathrm { U A V } u \in U$ leaves position $i \in V ,$

$t s _ { i } ^ { u t }$ 2 2be auxiliary continuous variables needed to define variables $T e _ { i } ^ { u }$

$n _ { i } ^ { u t } \in \{ 0 , 1 \}$ be binary variables stating whether UAV $u \in U$ f gis in position $i \in V$ at time $t \in { \bar { T } }$

$z _ { w i } ^ { u t }$ 2 2be binary variables indicating whether $\mathrm { U A V } ~ u \in$ $U$ is connected to EDD $w \in N$ at time $t \in T$ 2, when it visits position $i \in V$ 2 2. Since the UAVs can visit a posi-2tion only once, follows that UAV $u ,$ positioned at node $i \in V ,$ can be connected to EDD w $r \in N$ only 2once. Thus $\textstyle \sum _ { w \in N } z _ { w i } ^ { u t } \leq 1$ ; u $\in U , i \in V , t \in T$ . However, UAV $u \in N$  8 2 2can connect to a EDD $w \in N$ sev-2 2eral times, for instances, for each visited position.

In addition, given a UAV $u \in U$ at position $i \in V ,$ the term $\begin{array} { r } { t _ { i } ^ { u } = \sum _ { w \in N } \sum _ { t \in T } z _ { w i } ^ { u t } } \end{array}$ 2 2define the total time in Â¼ 2 2which u is connected to EDD $w \in N$ from position $i \in V .$

$B _ { w i } ^ { u t }$ be continuous variables defining the bandwidth assigned to $\mathrm { U A V } u \in U$ positioned at node $i \in V$ and connected to EDD $w \in N$ at time $t \in T$

2 2The variables and their meanings are summarized in Table 1.

We assume that the bandwidth assigned by the EDD $w \in$ N to UAV $u \in U .$ , located in position $i \in V ,$ 2, is linear with the distance $d _ { w i }$ 2. In particular, if $d _ { w i } > R ,$ , no bandwidth is assigned since it is not possible to ensure a connection between u located in i and the EDD w. On the other hand, the lower the distance $d _ { w i } ,$ the higher the bandwidth assigned, accordingly with equations (1) and (2). The mixed integer linear model follows:

$$
\operatorname* { m a x } g ( B ) = \sum _ { w \in N } \sum _ { i \in V } \sum _ { u \in U } \sum _ { t \in T } B _ { w i } ^ { u t }\tag{3}
$$

s:t:

$$
\sum _ { \{ j : ( i , j ) \in A \} } x _ { i j } ^ { u } - \sum _ { \{ j : ( j , i ) \in A \} } x _ { j i } ^ { u } = \left\{ \begin{array} { r l } { 1 } & { \mathrm { ~ i f } \quad i = s _ { u } } \\ { - 1 } & { \mathrm { ~ i f } \quad i = d _ { u } \ , } \\ { 0 } & { o t h e r w i s e } \end{array} \right.
$$

$$
\forall i \in V , u \in U\tag{4}
$$

$$
T _ { j } ^ { u } \geq T _ { i } ^ { u } + t _ { i } ^ { u } + \frac { d _ { i j } } { v } - M ( 1 - x _ { i j } ^ { u } ) , \forall ( i , j ) \in A , u \in U ,\tag{5}
$$

$$
T _ { s _ { u } } ^ { u } = \tilde { t } , \forall u \in U ,\tag{6}
$$

$$
n _ { i } ^ { u t } \in S , ~ \forall i \in V , u \in U , t \in T ,\tag{7}
$$

$$
z _ { w i } ^ { u t } \le \frac { R _ { w } } { d _ { w i } } n _ { i } ^ { u t } , \forall w \in N , i \in V , u \in U , t \in T ,\tag{8}
$$

$$
t s _ { i } ^ { u t } \geq \left( \sum _ { w \in N } z _ { w i } ^ { u t } - \sum _ { w \in N } z _ { w i } ^ { u t + 1 } \right) t , \forall i \in V , u \in U , t \in T ,\tag{9}
$$

$$
T e _ { i } ^ { u } \geq t s _ { i } ^ { u t } + 1 , \forall i \in V , u \in U , t \in T ,\tag{10}
$$

$$
z _ { w i } ^ { u t } \leq \frac { T e _ { i } ^ { u } } { t } , \forall w \in N , i \in V , u \in U , t \in T ,\tag{11}
$$

$$
1 + M \big ( 1 - z _ { w i } ^ { u t } \big ) \geq \frac { T _ { i } ^ { u } } { t } , \forall w \in N , i \in V , u \in U , t \in T ,\tag{12}
$$

$$
B _ { w i } ^ { u t } \le C _ { w } \biggl ( 1 - \frac { d _ { w i } } { R _ { w } } \biggr ) z _ { w i } ^ { u t } , \forall w \in N , i \in V , u \in U , t \in T ,\tag{13}
$$

$$
T _ { d u } ^ { u } \le T _ { u } , \quad \forall u \in U ,\tag{14}
$$

$$
\sum _ { i \in V } \sum _ { u \in U } B _ { w i } ^ { u t } \le C _ { w } , \quad \forall w \in N , t \in T .\tag{15}
$$

Equation (3) represents the objective function that maximizes the data downloaded by the UAVs. Equations from (4) to (15) are the constraints and are explained in what follows. Equations (4) represent the flow constraints associated with each $\mathrm { U A V } u \in U$ . Equations (5) define the arrival time of each UAV $u \in U$ in position j from position i, when the arc $( i , j )$ 2is traversed by the UAV u. Equations (6) define the Ã° Ãtime in which the UAV $u \in U$ enters the system from the entrance point $s _ { u }$ 2. Equations (7) define variables $n _ { i } ^ { u t }$ , where S is a set of constraints that will be defined later. Equations (8) and (9) define the variables $z _ { w i } ^ { u t }$ and $t s _ { i } ^ { u t }$ , respectively. Equations (10) define the variable $T e _ { i } ^ { u }$ starting from the variable $t s _ { i } ^ { u t }$ . In particular, $T e _ { i } ^ { u }$ assume value equal to the time in which the UAV u is no longer connected. Equations (11) and (12) impose that variable $z _ { w i } ^ { u t }$ assume value equal to 0 in the case $t > T e _ { i } ^ { u }$ and $t < T _ { i } ^ { u }$ , respectively. Equations (13) assign the bandwidth to the UAV u connected to the EDD w. Equations (14) impose that the UAVs have to reach their destination before the predefined sojourn time $T _ { u }$ in the TRA. Equations (15) impose that the bandwidth assigned to all $\mathrm { \bar { U } A V s }$ connected to the EDD w does not exceed the capacity $C _ { w }$ of the EDD w. We report a detailed description of the constraints in the Appendix (available online). The constant M is a big enough number introduced to proper define constraints (5) and (12). It can be set to the value $T _ { u } , \mathrm { i . e . }$ ., the maximum sojourn time of the UAV u in the TRA.

Model (3) â (15), called in the sequel M1, allows to determine the trajectory of each $\mathrm { U A V } u \in U$ in order to maximize 2the downloaded data within the limitation on the permanence in the system, $\mathrm { i . e . , } T _ { u }$ Â·

It is possible to design the trajectory for each UAV considering a certain amount of data to download, i.e., B with the aim of minimizing the overall permanence in the system within the imposed time horizon T . This new model, called on the sequel M2, differs from M1 in the objective function. In particular, the objective function of M2 is defined in the following

$$
\operatorname* { m i n } _ { \mathbf { \omega } } f ( T ) = \sum _ { u \in U } T _ { d _ { u } } ^ { u } .\tag{16}
$$

Thus, constraints (14) are no longer included. For model M2, the constant M can assume a value equal to T, i.e., the imposed time horizon. In addition, M2 presents the constraint which impose the minimum quantity of data to download as defined in the following

$$
g ( B ) = \sum _ { w \in N } \sum _ { i \in V } \sum _ { u \in U } \sum _ { t \in T } B _ { w i } ^ { u t } \geq B .\tag{17}
$$

## 3.3 Online Approach

In the previous section we have introduced a specific model that requires a global knowledge of all the elements in the TRA, UAVs or EDDs, including their mobility and available bandwidth. However, this information is not available in a real situation. In a previous publication [1], of which this paper is the extension, we developed an online approach based only on local information available on the UAVs, which is capable to drive these ones across the TRA, but also find and connect to the EDDs. The online approach already presented was based on Artificial Potentials and a detailed description of its internal is available in the related paper. The online approach consists in a distributed control system that runs on the UAVs and reacts according to the locally available information. Each UAV is driven towards the best EDD among those it is aware of. For the online approach, the UAVs know only the quantity of UAVs connected to each EDD of which they are aware, and location information is feed to the autopilot. The UAV control system has been modeled as an application that runs on the UAV flight controller. In opposition to the offline, in the online approach the information available at each UAV is purely local and sampled from the environment. In that work, each UAV is modeled as a single point on which a set of forces is applied. The applied forces are dependent from the sensed environment, which includes: the distance to the EDDs, the value of their advertised capacity and the distance from the TRA exit point. In this last case, the force component is inversely proportional to the time left before $T _ { u }$ expires. In that publication, we started from the following definitions:

Used Bandwidth $U B W _ { w } ( t )$ the bandwidth actually Ã° Ãused by all the UAV connected to the EDD;

Advertised Bandwidth $A B W _ { w } ( t )$ defined as $A B W _ { w } ( t ) =$ $C _ { w } - U B W _ { w } ( t )$

 Ã° ÃThen, we assumed equal repartition of bandwidth among the UAVs connected to an EDDs. In this work, instead, we model the $A B W _ { w } ( t )$ directly from our experiÃ° Ãmental setup. In our simulations, the value is continuously computed and then diffused to the UAVs. If multiple UAVs are connected to an EDD, they send their evaluation of the bandwidth to the the former, which is then diffused.

## 4 PERFORMANCE EVALUATION

As, in this work, we propose an offline model and an online scheme, this Section is split in multiple parts showcasing experiments for the two schemes in different simulative setups. To give a meaningful comparison we propose first a reference scenario that renders the presence of multiple UAVs in a TRA with multiple EDDs. Next, we present the results of a preliminary simulation campaign, where a baseline communication environment is determined by using NS3. The results of the preliminary campaign and the reference scenario are then feed to the offline model to determine a relevant solution. Subsequently, in a second campaign, we evaluate the performances of the online approach on small size instances. The numerical results collected are compared with those determined by solving the mathematical model. In the same campaign, the online scheme is then implemented in NS3 configured with the same scenario of the offline model and with the same simulation parameters of the first campaign. The results from this campaign show that the offline model has computational limitations with respect to input dimensions and, for this reason, in a third simulation campaign, we consider the online scheme only, while enlarging the input set.

## 4.1 Scenario and Preliminary Simulations

For our simulation campaigns, we have first identified an example scenario that could be used for both the online scheme and the offline model and then we feed it to the selected implementation.

The scenario consists in a TRA of $2 5 \times 2 5 \times 2 5 ~ m ^ { 3 } .$ , to  account for a city block. To simulate the positions of the EDDs on top of buildings, they are positioned in the TRA according to an uniform distribution spanning the whole area on the horizontal plane and restricted between 20 and 30 meters on the vertical plane.

All the UAVs start from a point external to the TRA, at a height $h _ { \mathrm { m a x } }$ of 25 meters and then they descend or ascend to the height of the EDDs they are moving to.

To test the offline model, we implemented it in Java and solved by CPLEX 12.10. For the online scheme, we have chosen to implement the mobility engine as an application level software for the NS3 simulator, version 3.30.

However, to give meaningful environmental parameters to the offline model, we first performed a preliminary set of simulations, with the intent of finding the bandwidth values, using the NS3 simulator. For its ubiquity and low cost, we have chosen to focus on IEEE 802.11 family of protocols and devices for the EDDs and UAVs communications.

<!-- image-->  
Fig. 3. Preliminary Simulation: how the number of UAVs connected to an EDD influences the average bandwidth per-UAV.

To do so, we implemented in NS3 the data transfer capabilities of UAVs and EDDs as an Application. Then, we created a simple scenario of an EDD surrounded by a variable number of UAVs, placed in an circle at a fixed distance of 10 meters from the EDD, and both the UAV and the EDD at 30 meters above ground level. Below the application layer, the communication is handled by unmodified TCP/IP NS3 stack. For realism purposes, we set the Rate Manager as MinstrelRateManager [36] and the propagation model as the Non-Line-of-Sight ITU-R 1411, a propagation model specific for short-range over-the-rooftops scenario [37].

We have increased the number of UAVs around the EDD and varied the Wi-Fi protocols between 802.11 g, 802.11n and 802.11ax.

Results are shown in Figs. 3 and 4. For Fig. 3, we have set the simulation to transfer an unlimited amount of data and have measured the bandwidth. In this way, we have been able to extrapolate the average bandwidth available at each UAV-EDD pair, when multiple UAVs are connected to the same EDD. For Fig. 4, instead we have measured the time necessary to complete a 10 MB data transfer.

From this simulation campaign we have an estimation of the communication environment, in terms of bandwidth and time necessary to complete a transfer, which could be used as parameters of the offline model.

## 4.2 Experimental Results

In this section we show the results of the two main simulation campaigns. In the first one we compare the Offline and the Online approaches on how they handle the reference scenario. In fact the two variants of the Offline model, M1 and M2, are translated in a set of constraints for the Online approach and then results are compared. In the second and last simulation campaign, we focus on the Online approach and, by increasing the number of UAVs and EDDs, we perform an analysis of how their spatial density affects the performances of the approach.

## 4.2.1 Offline Versus Online Approach

In order to evaluate the effectiveness of the proposed online approach, we compare its results with those obtained by the onJuly16,2024at03:13:31UTCfromIEEEXplore.Restrictionsapply.

<!-- image-->  
Fig. 4. Preliminary Simulation: how the number of UAVs connected to an EDD influences the average time to complete the transfer of a given data, averaged for each UAV.

offline approach, i.e., by solving models M1 and M2. Both models present a high number of variables and constraints. Hence, only small size instances have been considered for comparison. However, the solutions obtained with the offline approach are used as benchmarks to asses the goodness of the online approach. To this hand, we consider small size instances generated as described in the next Section.

Scenarios Generation: The experiments have been carried out on instances with $| N | = 5$ EDDs, randomly deployed in j j Â¼the reference scenario of Section 4.1. We consider four different altitudes, i.e., 10, 15, 20, and 25 m. Thus, the discretized tridimensional field can be viewed as a layered graph, i.e., a layer for each altitude with 9 possible positions each. Thus, the considered instances are characterized by $| V | =$ $9 \times 4$ . The set A is composed of arc $( i , j ) .$ j j Â¼, for each pair of  Ã° Ãpositions i and j. We recall that the feasible arcs are those on which a UAV can move without incurring in an obstacle. Thus, all direct connections between positions i and j are declared feasible. We highlight that this assumption makes the problem more difficult to solve since the associated instances contain a higher number of arcs than the case in which some arcs are declared infeasible due to the presence of obstacles. We consider a number of UAVs equal to 2 and 3, assuming $\tilde { t } _ { u } = 0 , \forall u \in U$ and four different values for the Â¼ 8 2permanence in the system, i.e., $T _ { u } \in \{ 1 0 , 2 0 , 3 0 , 4 0 \}$ s. The 2 f gmaximum speed of the UAVs is set to 10 m/s [38]. Selecting IEEE 802.11n because of its ubiquity and according to the results of the preliminary campaign, we have put the capacity $C _ { w } = 2 2$ MB/s at a communication range $\hat { R } _ { w } = 1 0 \mathrm { m }$ , for Â¼each EDD $w \in N$ Â¼. The model is implemented in Java and 2solved by CPLEX 12.7. We impose a time limit of 7200 seconds to CPLEX for solving each instance.

Online Model. The Online model of Section 3.3 is then implemented as a Mobility Model inside NS3 and activated in a set of nodes representing the UAVs, alongside the data transfer facilities. At the same time, the same facilities are implemented as another Application in a set of static nodes that represent the EDDs. To compare with the Online approach, the EDD positions and the UAVs entrance and exit points are feed to NS3, while the networking parameters are taken directly from the preliminary simulations of Section 4.1. In this way there is an acceptable level of similarity between the inputs and scenarios of the Online and the Offline approaches. As they comes from an event-based simulation rather than the solution of an optimization model, the results for the Offline model are labeled as Sim. Numerical Results: CPLEX is not able to solve to optimality any instance within the imposed time limit, considering both M1 and M2. This result highlights the difficulties on solving the problems to optimality. However, a feasible solution is available for each considered instance and model.

TABLE 2  
Results Comparing the Data Downloaded by the Offline (M1) and Online (Sim) Approaches
<table><tr><td rowspan="2">#UAVs</td><td colspan="3">M1</td><td colspan="3">Sim</td></tr><tr><td> $T _ { u }$ </td><td>g(B)</td><td>t</td><td>g(B)</td><td>t</td><td>gap</td></tr><tr><td>2</td><td>10</td><td>125.40</td><td>7200.00</td><td>175.27</td><td>54.60</td><td>28%</td></tr><tr><td>2</td><td>20</td><td>383.98</td><td>7200.00</td><td>547.65</td><td>169.40</td><td>30%</td></tr><tr><td>2</td><td>30</td><td>697.40</td><td>7200.00</td><td>970.37</td><td>297.00</td><td>28%</td></tr><tr><td>2</td><td>40</td><td>953.74</td><td>7200.00</td><td>1406.77</td><td>426.20</td><td>32%</td></tr><tr><td>avg</td><td></td><td>540.13</td><td>7200.00</td><td>775.01</td><td>236.80</td><td>30%</td></tr><tr><td>3</td><td>10</td><td>198.00</td><td>7200.00</td><td>287.25</td><td>89.80</td><td>31%</td></tr><tr><td>3</td><td>20</td><td>538.14</td><td>7200.00</td><td>877.00</td><td>269.40</td><td>39%</td></tr><tr><td>3</td><td>30</td><td>847.81</td><td>7200.00</td><td>1519.09</td><td>457.20</td><td>44%</td></tr><tr><td>3</td><td>40</td><td>766.50</td><td>7200.00</td><td>2176.64</td><td>647.60</td><td>65%</td></tr><tr><td>avg</td><td></td><td>587.61</td><td>7200.00</td><td>1215.00</td><td>366.00</td><td>52%</td></tr></table>

Main Results. The offline approach returns better solutions than those obtained with the online approach when the permanence time in the TRA is minimized guaranteeing a certain amount of data to download, i.e., model M2. When considering model M1, i.e., the maximization of the downloaded data in the imposed permanence time in the TRA, the online approach is able to provide solutions with a higher amount of downloaded data than those obtained with the offline approach. For both model M1 and M2, the offline approach is less efficient than the online one.

In the sequel, we analyze in details the numerical results collected by considering the offline approach.

Results for Model M1. Table 2 shows the amount of download data under column $g ( B )$ , the execution time under column t, and the value $1 - ( g ( B ) _ { M 1 / } g ( B ) _ { S i m } )$ 100 under column gap, where $g ( B ) _ { M 1 }$ Ã° Ã°and $g ( \boldsymbol { B } ) _ { S i m }$ Ã are the amount of Ã° Ã Ã° Ãdownloaded data returned by M1 and the online approach, respectively. The value gap gives the percentage increase of data downloaded of the simulation with respect to the results obtained by CPLEX within the imposed time limit of 7200 seconds.

Table 2 clearly shows the effectiveness of the online approach. Indeed, on average, it provides 30% and 52% more download data than that of the offline approach, for number of UAVs equal to 2 and 3, respectively. In addition, the value of gap increases when the value of $\dot { T } _ { u }$ increases as well. Beside the good results in terms of download data, the online approach is also less time-consuming. Indeed, on average, its computational overhead is equal to 236.80 and 366.00 seconds for number of UAVs equal to 2 and 3, respectively.

TABLE 3  
Results Comparing the Permanence Time in the System by the Offline (M2) and Online (Sim) Approaches
<table><tr><td rowspan="2">#UAVs</td><td colspan="4">M2</td><td colspan="3">Sim</td></tr><tr><td>B</td><td>f(T)</td><td>MS</td><td>t</td><td>f(T)</td><td>MS</td><td>t</td></tr><tr><td>2</td><td>40</td><td>13.17</td><td>9.21</td><td>7200.00</td><td>15.91</td><td>9.08</td><td>28.80</td></tr><tr><td>2</td><td>60</td><td>11.76</td><td>8.22</td><td>7200.00</td><td>18.65</td><td>10.87</td><td>40.40</td></tr><tr><td>2</td><td>80</td><td>17.98</td><td>14.19</td><td>7200.00</td><td>21.20</td><td>12.46</td><td>50.40</td></tr><tr><td>2</td><td>100</td><td>14.57</td><td>10.89</td><td>7200.00</td><td>23.66</td><td>14.00</td><td>64.20</td></tr><tr><td>avg</td><td></td><td>14.37</td><td>10.63</td><td>7200.00</td><td>19.85</td><td>11.60</td><td>45.95</td></tr><tr><td>3</td><td>40</td><td>16.00</td><td>7.67</td><td>7200.00</td><td>22.41</td><td>8.78</td><td>44.40</td></tr><tr><td>3</td><td>60</td><td>23.08</td><td>13.38</td><td>7200.00</td><td>25.98</td><td>10.32</td><td>62.20</td></tr><tr><td>3</td><td>80</td><td>19.76</td><td>12.55</td><td>7200.00</td><td>29.28</td><td>11.68</td><td>78.40</td></tr><tr><td>3</td><td>100</td><td>21.81</td><td>14.55</td><td>7200.00</td><td>32.60</td><td>13.05</td><td>96.80</td></tr><tr><td>avg</td><td></td><td>20.16</td><td>12.04</td><td>7200.00</td><td>27.57</td><td>10.96</td><td>70.45</td></tr></table>

TABLE 4

Instances for Scaling Analysis
<table><tr><td>ID instance</td><td>field dimension</td><td>#UAVs</td><td>#EDDs</td></tr><tr><td>1</td><td> $2 5 \times 2 5 \times 2 5$ </td><td>2</td><td>5</td></tr><tr><td>2</td><td> $3 5 \times 3 5 \times 2 5$ </td><td>3</td><td>6</td></tr><tr><td>3</td><td> $6 5 \times 6 5 \times 2 5$ </td><td>6</td><td>9</td></tr></table>

The numerical results collected in Table 2 highlight the effectiveness and the efficiency of the online approach in solving the problem. The offline approach gives worst feasible solution for each instance.

Results for Model M2. Considering model M2, where the permanence time in the system, required to download a certain quantity of data B, is minimized, the offline approach is competitive with the online one in terms of effectiveness. Indeed, M2 provides better solutions than the online approach for certain instances. In the computational experiment, we consider $B \in \{ 4 0 , 6 0 , 8 0 , 1 0 0 \}$ . Table 3 shows the 2 f gnumerical results obtained with CPLEX and the online approach. Column f T reports the total permanence time, Ã° Ãi.e., equation (16). Column MS reports the makespan, i.e., $\mathbf { M S } = \mathbf { m a x } _ { u \in U } T e _ { d } ^ { u } ,$ , where Teu is the exit time of UAV u. Col-2umn t reports the execution time.

CPLEX provides the best value of f T , i.e., it gives soluÃ° Ãtions with a permanence time to the system lower than that obtained with the online approach. In particular, the value of f T obtained by M2 is, on average, 1.38 and 1.37 times Ã° Ãlower than that obtained with Sim considering the case with 2 and 3 UAVs, respectively. The value for MS is better for M2 when 2 UAVs are considered. In this case, MS for M2 is 1.09 times lower than that obtained with Sim. When considering the case with 3 UAVs, Sim returns the best result. Indeed, MS for M2 is 1.10 times higher than that obtained with Sim. The latter is very efficient. Indeed, Sim provides very close values of both f T and MS to those obtained by Ã° ÃM2 with a very limited execution time, compared with that required by CPLEX.

Thanks to the availability of the solutions obtained with CPLEX, we can conclude that the online approach has a good trade-off between effectiveness of the solution and computational effort for the considered instances.

<!-- image-->  
IDinstance

Fig. 5. Execution time in logarithmic scale for obtaining the first feasible solution with M1 for each instance reported in Table 4.  
<!-- image-->  
Fig. 6. Execution time in logarithmic scale for obtaining the first feasible solution with M2 for each instance reported in Table 4.

Scalability of M1 and M2. In order to analyze models scalability, we conducted a further computational phase by removing the time limit and varying the instances dimension. In particular, we consider three instances of increasing size, whose characteristics are reported in Table 4.

We set the memory of the Java virtual machine at 7500 MB. Fig. 5 reports the execution time (in logarithmic scale) required by CPLEX to find the first feasible solution for each instance of Table 4, considering M1 and setting $T _ { u } = 1 0 , \forall u \in U$ . The execution time grows exponentially at Â¼ 8 2increasing the dimension of the instances. CPLEX returns the first feasible solution in 1.64 second for the instance 1, whereas it requires 71719.50 seconds for the instance 3. The first feasible solution is obtained after 553.84 seconds for the instance 2.

Fig. 6 reports the execution time in logarithmic scale for M2 setting ${ \bf { \bar { \boldsymbol { B } } } } = 4 0 $

Â¼Also for M2 the computational effort grows exponentially with the increasing of the dimension. The execution time for obtaining the first feasible solution is 4.13, 11.67, and 9475.84 for the instance 1, 2, and 3, respectively.

As observed from the numerical results, the offline approach is limited in terms of size of the instances. Hence, for the rest of the simulation campaign, we show the results obtained with the online approach only.

## 4.2.2 Online Approach Results

In a third set of simulation we focus on the Online approach and we increase the input size with respect to the simulation onJuly16,2024at03:13:31UTCfrom IEEEXplore.Restrictionsapply.

<!-- image-->  
Fig. 7. Online approach: UAVs average velocity vursus $T _ { u } . \rho = 0 . 2$

campaign with the Offline approach. In these simulation we keep the EDDs and the scenario of the previous Sections but we dramatically increase the number of EDDs positioned in the scenario.

We introduce now two important simulation parameters. One, r is the ratio between UAVs and EDD in the TRA. the other one is the Minimum Time (MT). To understand how imposing a maximum time for the UAVs to remain n the TRA, we introduce a threshold time, the MT: the time necessary for an UAV, flying at maximum speed, to traverse the TRA from the starting point to the exit point. It is then possible to set values of $T _ { u }$ as multiples of MT, to have a meaningful comparison, where u is the UAV index. We increase to 5 and keep constant the number of UAVs always present in the TRA: the UAVs enter the TRA in a sequence, with each entrance separated by an interval of one second. To keep r constant, every time that a UAV leaves the TRA, we force the entrance of a new UAV.

In the following, each curve, represents the averaging of 10 simulation runs. Confidence interval is computed with a student-t distribution and an interval of 95%; however, this data is omitted in the diagrams for clarity reasons.

By using r we evaluated the impact of varying the EDD density. We have increased progressively the value of the ratio r by keeping constant the number of UAVs and increasing the number of EDDs in the same area. We have measured the bandwidth assigned to the UAVs, as well as the total downloaded data. From Fig. 8, we can see that when the $T _ { u }$ is short, there is a drastic reduction of the bandwidth.

<!-- image-->

<!-- image-->  
Fig. 9. Online approach with no time limit. Time needed to exit the area vursus payload. Variable $\rho .$

We have found that, using the given propagation models, described at the beginning of this Section, higher densities are detrimental as much as low ones. In the latter case, the UAVs are driven in areas that cannot serve them swiftly. In the former, the sheer network congestion increases the BER of the transmissions and lowers the bandwidth.

According to the results, we have found out that the ratio that ensures the best performance is the one that considers a number of UAVs roughly half of the EDDs present in the area.

In the same environment, we have measured the time evolution of the absolute velocity of the UAVs. In Fig. 7, it is displayed the average velocity of the UAVs during the simulation. Increasing the $T _ { u } ,$ each UAV has the time to reach farther EDDs, thus maintaining a lower velocity for an extended time-frame.

Finally, we assessed the time to download a predefined payload. Hence, in the same density configurations of the previous simulations, we have removed the $T _ { u }$ constraint and measured how much time is necessary to exit the area after the whole download has been achieved (Fig. 9). From this set of figures, it is possible to see that a lower density is as detrimental as a higher one, which is the same conclusions we can infer from the previous campaign.

## 5 CONCLUSION

For the future of Smart Cities, we envision that, the UAVs will have the possibility to connect to a set of EDD, deployed in specific areas of the city: the TRAs. As the capacity of the EDDs, as well as the time of sojourn in the TRA available for the UAV are limited, it is indispensable for the UAVs to define an optimal movement trajectory among the EDDs. To determine the best trajectory, we introduce a new tridimensional trajectory planning problem for UAVs that takes into account time and capacity constraints. First, we present a general mathematical formulation of the problem and a relaxed version that allows us to the test an offline solution approach. Then, we design an online approach for the UAVs, which determines an efficient trajectory by using only local information. Results not only show the feasibility of our online approach, but we also find preliminary insights about the TRA dimensioning in terms of EDD density. For future works, we plan to introduce of EDD density.For future works,we plan to introduce onJuly16.2024at03:13:31UTCfromIEEEXploreï¼Restrictionsapply

Fig. 8. Online approach average bandwidth per-UAV vursus r and $T _ { u } .$ Authorized licensed use limited to: Beijing Normal University. Downloaded on July 16,2024 at 03:13:31 UTC from IEEE Xplore. Restrictions apply.

real-time obstacle avoidance, to include the details of more realistic localization services and, furthermore, to leverage the use of real drones to perform a set of live experiments in one of the authorâs facilities.

## REFERENCES

[1] E. Natalizio, N. R. Zema, L. Di Puglia Pugliese, and F. Guerriero, âDownload and fly: An online solution for the UAV 3D trajectory planning problem in smart cities,â in Proc. 9th ACM Symp. Des. Anal. Intell. Veh. Netw. Appl., 2019, pp. 49â56.

[2] R. Santin, L. Assis, A. Vivas, and L. C. Pimenta, âMatheuristics for multi-UAV routing and recharge station location for complete area coverage,â Sensors, vol. 21, no. 5, 2021, Art. no. 1705.

[3] M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah, âA tutorial on UAVs for wireless networks: Applications, challenges, and open problems,â IEEE Commun. Surv. Tut., vol. 21, no. 3, pp. 2334â2360, Third Quarter 2019.

[4] S. Li, F. Sun, D. An, and S. He, âIncreasing efficiency of a wireless energy transfer system by spatial translational transformation,â IEEE Trans. Power Electron., vol. 33, no. 4, pp. 3325â3332, Apr. 2018.

[5] B. Amina and E. Mohamed, âPerformance evaluation of VANETs routing protocols using sumo and NS3,â in Proc. IEEE 5th Int. Congr. Inf. Sci. Technol., 2018, pp. 525â530.

[6] H. Gedawy, A. Al-Ali, A. Mohamed, A. Erbad, and M. Guizani, âUAVs smart heuristics for target coverage and path planning through strategic locations,â in Proc. IEEE Int. Wireless Commun. Mobile Comput., 2021, pp. 278â284.

[7] A. Alaghehband, M. J. Sobouti, A. H. Mohajerzadeh, A. Vahedian, and S. A. H. Seno, âJoint optimization of 3D deployment and trajectory of fbss to reduce power consumption under backhaul constraints,â in Proc. IEEE 11th Int. Conf. Comput. Eng. Knowl., 2021, pp. 487â494.

[8] X. Ma, T. Liu, S. Liu, R. Kacimi, and R. Dhaou, âPriority-based data collection for UAV-aided mobile sensor network,â Sensors, vol. 20, no. 11, 2020, Art. no. 3034.

[9] R. A. Nazib and S. Moh, âEnergy-efficient and fast data collection in UAV-aided wireless sensor networks for hilly terrains,â IEEE Access, vol. 9, pp. 23168â23190, 2021.

[10] A. Madridano, A. Al-Kaff, D. Mart  Ä±n, and A. de la Escalera, âTrajectory planning for multi-robot systems: Methods and applications,â Expert Syst. Appl., vol. 173, 2021, Art. no. 114660.

[11] L. Yang, J. Qi, J. Xiao, and X. Yong, âA literature review of UAV 3D path planning,â in Proc. IEEE 11th World Congr. Intell. Control Automat., 2014, pp. 2376â2381.

[12] E. Angelelli, V. Morandi, and M. Speranza, âCongestion avoiding heuristic path generation for the proactive route guidance,â Comput. Operations Res., vol. 99, pp. 234â248, 2018.

[13] A. Madridano, A. Al-Kaff, D. Mart Ä±n, and A. de la Escalera, â3D trajectory planning method for UAVs swarm in building emergencies,â Sensors, vol. 20, no. 3, 2020, Art. no. 642. [Online]. Available: https:// www.mdpi.com/1424â8220/20/3/642

[14] F. Carrabs, C. Cerrone, R. Cerulli, and M. Gaudioso, âA novel discretization scheme for the close enough traveling salesman problem,â Comput. Operations Res., vol. 78, pp. 163â171, 2017.

[15] A. Grancharova, E. I. GrÃ¸tli, and T. A. Johansen, âDistributed MPCbased path planning for UAVs under radio communication path loss constraints,â IFAC Proc. Volumes, vol. 45, no. 4, pp. 254â259, 2012.

[16] J. T. GrÃ¸tliE.I., âPath planning for UAVs under communication constraints using SPLAT! and MILP,â J. Intell. Robot. Syst., vol. 65, pp. 265â282, 2012.

[17] A. Corber  an, I. M. PlanaReula, and J. M. Sanchis, âOn the distance-constrained close enough arc routing problem,â Eur. J. Oper. Res., vol. 291, pp. 32â51, 2020.

[18] L. Flores-Luyo, A. Agra, R. Figueiredo, and E. Ocana, âMixed inte- \~ ger formulations for a routing problem with information collection in wireless networks,â Eur. J. Oper. Res., vol. 280, no. 2, pp. 621â638, 2020.

[19] M. Samir, S. Sharafeddine, C. M. Assi, T. M. Nguyen, and A. Ghrayeb, âUAV trajectory planning for data collection from timeconstrained IoT devices,â IEEE Trans. Wireless Commun., vol. 19, no. 1, pp. 34â46, Jan. 2020.

[20] P. Falcone, F. Borrelli, J. Asgari, H. E. Tseng, and D. Hrovat, âPredictive active steering control for autonomous vehicle systems,â IEEE Trans. Control Syst. Technol., vol. 15, no. 3, pp. 566â580, May 2007.

[21] P. Falcone, M. Tufo, F. Borrelli, J. Asgari, and H. E. Tseng, âA linear time varying model predictive control approach to the integrated vehicle dynamics control problem in autonomous systems,â in Proc. IEEE 46th Conf. Decis. Control, 2007, pp. 2980â2985.

[22] R. Takei, R. Tsai, H. Shen, and Y. Landa, âA practical path-planning algorithm for a simple car: A hamilton-jacobi approach,â in Amer. Control Conf., 2010, pp. 6175â6180.

[23] M. Likhachev and D. Ferguson, âPlanning long dynamically feasible maneuvers for autonomous vehicles,â Int. J. Robot. Res., vol. 28, no. 8, pp. 933â945, 2009.

[24] M. Fakoor, A. Kosari, and M. Jafarzadeh, âHumanoid robot path planning with fuzzy markov decision processes,â J. Appl. Res. Technol., vol. 14, no. 5, pp. 300â310, 2016.

[25] M. T. Spaan and N. Vlassis, âA point-based POMDP algorithm for robot planning,â in Proc. IEEE Int. Conf. Robot. Automat., 2004, pp. 2399â2404.

[26] D. Gonzalez, J. Perez, V. Milanes, and F. Nashashibi, âA review of motion planning techniques for automated vehicles.,â IEEE Trans. Intell. Transp. Syst., vol. 17, no. 4, pp. 1135â1145, Apr. 2016.

[27] S. Karaman and E. Frazzoli, âSampling-based algorithms for optimal motion planning,â Int. J. Robot. Res., vol. 30, no. 7, pp. 846â894, 2011.

[28] S. Karaman and E. Frazzoli, âOptimal kinodynamic motion planning using incremental sampling-based methodsâ in Proc. IEEE 49th Conf. Decis. Control, 2010, pp. 7681â7687.

[29] F. Yuan, J.-H. Liang, Y.-W. Fu, H.-C. Xu, and K. Ma, âA hybrid sampling strategy with optimized probabilistic roadmap method,â in Proc. IEEE 12th Int. Conf. Fuzzy Syst. Knowl. Discov., 2015, pp. 2298â2302.

[30] R. Geraerts, âPlanning short paths with clearance using explicit corridors,â in Proc. IEEE Int. Conf. Robot. Automat., 2010, pp. 1997â2004.

[31] F. SchÃ¸ler, A. la Cour-Harbo, and M. Bisgaard, âGenerating approximative minimum length paths in 3D for UAVs,â in Proc. IEEE Intell. Veh. Symp., 2012, pp. 229â233.

[32] A. S. Bedi, K. Rajawat, and M. Coupechoux, âAn online approach to D2D trajectory utility maximization problem,â in Proc. IEEE Int. Conf. Comp. Commun., 2018, pp. 16â19.

[33] C. Wang, H. Lin, R. Zhang, and H. Jiang, âSEND: A situationaware emergency navigation algorithm with sensor networks,â IEEE Trans. Mobile Comput., vol. 16, no. 4, pp. 1149â1162, Apr. 2017.

[34] D. Xia, J. Hart, and Q. Fu, âOn the performance of rate control algorithm minstrel,â in Proc. IEEE 23rd Int. Symp. Pers. Indoor Mobile Radio Commun., 2012, pp. 406â412.

[35] Y. Singh, âComparison of okumura, hata and cost-231 models on the basis of path loss and signal strength,â Int. J. Comput. Appl., vol. 59, no. 11, pp. 37â41, 2012.

[36] W. Yin, P. Hu, J. Indulska, M. Portmann, and Y. Mao, âMAC-layer rate control for 802.11 networks: A survey,â Wireless Netw., vol. 26, pp. 3793â3830, 2020.

[37] T. Mangel, O. Klemp, and H. Hartenstein, â5.9 GHz inter-vehicle communication at intersections: A validated non-line-of-sight path-loss and fading model,â EURASIP J. Wireless Commun. Netw., vol. 2011, no. 1, 2011, Art. no. 182.

[38] S. Hayat, E. Yanmaz, and C. Bettstetter, âExperimental analysis of multipoint-to-point UAV communications with IEEE 802.11n and 802.11ac,â in Proc. IEEE 26th Annu. Int. Symp. Pers., Indoor, Mobile Radio Commun., 2015, pp. 1991â1996.

<!-- image-->  
Nicola Roberto Zema received the BS, MS and PhD degrees from the University âMediterraneaâ of Reggio Calabria, Italy, in 2009, 2011 and 2015, respectively. He is an associate professor with the University of Paris Saclay. Since then he has been a postdoc across Europe in University of Technology of Compiegne, Inria Lille and IFSTTAR Lille (France). Currently he is an associate professor with the LISN - Laboratoire Interdisciplinaire des Sciences du Numerique, University of Paris-Saclay, France. His current research activities include computer networks and combinatorial optimization.

<!-- image-->

Enrico Natalizio (Senior Member, IEEE) received the masterâs degree magna cum laude and the PhD degree in computer engineering from the University of Calabria (Italy), in 2000 and 2005, respectively. He is currently a vice president with the Autonomous Robotics Research Center, Technology Innovation Institute (UAE) and a full professor with the LORIA laboratory, Universite de Lorraine (France). In 2005- 2006 he was a visiting researcher with the BWN (Broadband Wireless Networking) Lab, Georgia Tech in Atlanta (USA). From 2006 till 2010, he was a

research fellow with the Titan Lab of the Universita della Calabria (Italy). In  October 2010, he joined POPS team with Inria Lille â Nord Europe (France) as a postdoc researcher and from 2012 till 2018 he was an Associate Professor with the Universite de technologie de Compi egne (France), and full pro- fessor with the Universite de Lorraine, from September 2018. His research interests include UAV communications and networking, robot and sensor communications with applications in networking technologies for disaster management and infrastructure monitoring, and IoT privacy and security. He is currently an associated editor of Elsevier Vehicular Communications, and Computer Networks.

<!-- image-->

Luigi Di Puglia Pugliese He received the PhD degree in operations research from the University of Calabria, in 2011, with a thesis entitled Models and Methods for the Constrained Shortest Path Problem and its Variants. He is a researcher with the Consiglio Nazionale delle Ricerche, Italy. His main research interests lie in the field of network optimisation. Other area of interests include logistics, combinatorial optimisation and project scheduling.

<!-- image-->

Francesca Guerriero (Member, IEEE) received the PhD degree in engineering of systems and informatics from University of Calabria, Italy. She is a full professor of operations research with the Department of Mechanical, Energy and Management Engineering (DIMEG), University of Calabria. She is currently the director of the DIMEG and a vice president of the Italian Operations Research Society. Her primary research interests lie in the field of network optimisation. Her other area of interests include logistics, revenue management

and combinatorial optimisation. She has published more than a hundred academic articles, in well-established international journals.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_2_img_1.jpeg|page_2_img_1]]
2. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_3_img_1.jpeg|page_3_img_1]]
3. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_6_img_1.jpeg|page_6_img_1]]
4. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_7_img_1.jpeg|page_7_img_1]]
5. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_8_img_1.jpeg|page_8_img_1]]
6. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_8_img_2.jpeg|page_8_img_2]]
7. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_9_img_1.jpeg|page_9_img_1]]
8. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_9_img_2.jpeg|page_9_img_2]]
9. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_9_img_3.jpeg|page_9_img_3]]
10. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_10_img_1.jpeg|page_10_img_1]]
11. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_11_img_1.jpeg|page_11_img_1]]
12. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_11_img_2.jpeg|page_11_img_2]]
13. [[../extracted_images/Zema 等 - 2024 - 3D Trajectory Optimization for Multimission UAVs i/page_11_img_3.jpeg|page_11_img_3]]

---

