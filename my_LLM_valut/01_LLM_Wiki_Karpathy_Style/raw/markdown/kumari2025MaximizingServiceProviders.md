# Maximizing Service Providerâs Profit in Multi-UAV 5G Network Via Deep Reinforcement Learning and Graph Coloring

Shilpi Kumari , Graduate Student Member, IEEE, and Ajay Pratap , Senior Member, IEEE

AbstractâThe current 5G network is expected to have a densely populated architecture comprising radio-enabled Service Provider (SP) and heterogeneous User Equipment (UE). Addressing the real-time service demands of UEs with strict deadlines is a critical challenge. Uncrewed Aerial Vehicle (UAV) assisted service provisioning is emerging as an efficient solution for timely service transfers. Therefore, SPs are interested in offering UAV-assisted service transmission to get profited by deploying UAVs. However, this introduces challenges like optimizing the locations of UAVs and Power Level (PL) along with interference management within limited available radio resources. Hence, we proposed a novel framework for multi-UAV-assisted service provisioning, consisting of Base Station (BS), UAVs, and heterogeneous UEs in 5G network. We formulate the SPâs profit maximization problem, optimizing UAVsâ location, PL, and resource allocation while considering service latency, interference management, and UAVsâ energy constraints collectively as an optimization problem. Furthermore, we propose a semi-centralized sub-optimal solution utilizing Multi-agent Deep Reinforcement Learning (MaDRL) and a Graph Coloring-based approach. Extensive simulation analysis demonstrates the proposed algorithmâs effectiveness, achieving an average of 99.05% profit compared to the optimal value.

Index TermsâUAV, 5G, deep reinforcement learning, resource allocation, graph coloring.

## I. INTRODUCTION

T HE current Fifth Generation (5G) cellular network is ex-pected to support User Equipment (UE) in various tasks pected to support User Equipment (UE) in various tasks like online gaming, video streaming, edge computing, and local caching, with reduced latency, lower power consumption, and enhanced data rates [1]. Performing such tasks on UEs with limited resources, including storage, computation, and battery capacity, poses several challenges [2]. However, UEs require services in remote or mountainous regions where communication infrastructure is often sparse, and communication conditions are challenging [3], [4]. Additionally, there might be a large number of UEs simultaneously requesting services. Routing service requests from UEs through Base Stations (BS) can lead to increased latency and diminished Quality of Service (QoS) [5].

The utilization of UAVs for service transfer is regarded as a promising strategy to enhance the QoS of Service Provider (SP), such as Internet Service Provider (ISP) or mobile network operator [6].Traditional BS coverage may be hindered by tall buildings or impaired by natural disasters. In that scenario, SP may use UAV as a mobile BS to provide services in hassle free manner [7], [8]. Choice of hovering locations, transmitting power, and allocation of limited available radio resources by UAVs have a direct impact on the QoS. Consequently, a comprehensive optimization approach that includes the positioning of UAVs, Power Level (PL) allocation, and radio resource allocation becomes necessary. UAVs reuse limited available radio resources from the cellular 5G network to serve maximum number of UEs [2]. However, this phenomenon creates severe interference problem in the network. Moreover, revenue can serve as an incentive, motivating SP to deliver better services to UEs with the help of UAVs. In other words, SP aim to maximize overall profit by serving UEs.

Many research have been done on UAVsâ location optimization, PL allocation, and resource management to maximize the serving capacity of UAVs [9], [10]. The existing approaches, such as game theory and static optimization, have been widely used to achieve global solutions based on the communication network [10], [11], [12]. However, in practice, the topology of the environment is initially unknown to UAVs due to dynamic behavior of UEsâ requests. These existing works cannot be applied directly in this dynamic environment. Thus, the aim of this paper is to facilitate a solution for real-time adaptation and decision-making based on learned experiences, enabling UAVs to dynamically respond to a changing environment.

In this paper, we formulate a profit maximization problem that considers QoS factors including UAVsâ energy consumption, service latency, and interference management via radio resource allocation. Multi-agent Deep Reinforcement Learning (MaDRL) has strong adaptability to dynamic and complex environments, which can be used for intelligent control of the UAVs to enhance the performance of the communication networks. However, solving the formulated problem through the joint optimization of UAVsâ locations, PL, and resource allocation forms a high decision-making dimension that cannot be solved by traditional MaDRL directly [13]. Thus, we proposed a novel approach that combines MaDRL and graph coloring framework for learning the best possible solution of the formulated problem. In proposed framework, UAVs function as real-time decisionmakers responsible for their placement and PL assignment, while the BS employs graph coloring algorithm for effective allocation of communication resources. The main contributions of this work can be summarized as follows:

TABLE I SUMMARY OF EXISTING WORKS
<table><tr><td rowspan=1 colspan=2>Work</td><td rowspan=1 colspan=1>Multi-UAV</td><td rowspan=1 colspan=1>HeterogeneousServices</td><td rowspan=1 colspan=1>PRBReusablity</td><td rowspan=1 colspan=1>PowerLevel</td><td rowspan=1 colspan=1>LatencyConstraint</td><td rowspan=1 colspan=1>EnergyConstraint</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[11]</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[14]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[12]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[17]</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=2>Ours</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td><td rowspan=1 colspan=1>â</td></tr></table>

- Propose a novel framework for multi-UAV-assisted service provisioning, consisting of BS, UAVs, and UEs.

Formulate an optimization problem that maximizes the SPâs profit considering interference, energy consumption, service latency altogether as an NP-hard problem.

Solve the formulated problem efficiently by proposing a semi-centralized Multi-agent Deep Reinforcement learning and graph Coloring (MaDRC) algorithm.

- Extensive performance assessment demonstrate the effectiveness of the proposed algorithm, achieving a noteworthy 99.05% profit of optimal value.

The rest of the paper is organized as follows: Section II reviews the related works. Section III formally defines the profit maximization problem. Section IV presents algorithm for solving the formulated problem. Section V evaluates the effectiveness of proposed algorithm, and Section VI offers conclusions and future research directions.

## II. BACKGROUND AND RELATED WORK

This section outlines related literature and provides a comparative analysis in Table I.

In [9], authors introduced a Mission Scheduling Problem (MSP), which involved coordinating flight routes to capture video at specific waypoints, followed by on-board edge analytics. They proposed a scheduling strategy to maximize activity utility while considering deadlines, energy constraints, and computing limitations and solved the MSP using heuristic algorithms. In [6], Dai et al. presented a resource allocation algorithm for UAV networks. This method employed a distributed architecture where UAVs are treated as independent agents. These agents enhance overall efficiency of UAV network by deciding on deployment location, sub-channels and transmission power using Multi-Agent Collaborative Environment Learning (MACEL) algorithm.

Tang et al. [12] introduced a QoE-driven video broadcast strategy for wireless UAV network. The objective was to maximize peak signal-to-noise ratio of video quality for ground users by simultaneously optimizing power allocation and trajectory of UAV. They devised an algorithm utilizing Block Coordinate Descent (BCD) and Successive Convex Approximation (SCA) methods to meet the objective. In [14], authors proposed a distributed mechanism for spectrum sharing between UAV and terrestrial networks. They used Q-learning for spectrum allocation in UAV-network.

The authors in [11] proposed a RL-based algorithm for planning UAV routes to collect data from scattered sensors. They divided their environment into grids, each with a central spot for UAV hovering and wireless charging. Considering data collection and energy consumption, they framed the problem as Markov decision process. They utilized Q-learning to find best strategy, designing a reward function that emphasized energy efficiency in UAV flight and data collection. In [10], the authors aimed to optimize uplink transmission between multiple UAV-BSs and IoT devices. They sought to minimize transmission power, considering shared frequency spectrum, similar UAV tasks, and limited subchannels. They introduced a modified K-means algorithm for balanced device assignment, proposed a modified-Hungarian-based dynamic manyâmany matching (HD4M) algorithm for subchannel allocation, and jointly optimized IoT devicesâ transmission power and UAV altitudes using Altitude and Power Control Algorithm (APCA).

In [15], the authors aimed to maximize system capacity by optimizing subchannel assignment, uplink power for IoT devices, and UAV flying heights. They used K-means for grouping IoT devices, then developed a matching algorithm for efficient subchannel assignment. They also derived solutions for power and flight heights using an Alternative Optimization (AO) and SCA methods based on the clustering results. In the work by Cui et al. [16], each UAV independently chose its communication user, power level, and subchannel without exchanging information with other UAVs. Each UAV operated as a learning agent, with resource allocation representing its actions. The authors introduced a multi-agent reinforcement learning framework, where each agent identified its best strategy based on local observations using Q-learning. In [17], the authors introduced the Single-drone Data-collection Maximization Problem (SDMP). The problem aimed to optimize a droneâs mission to maximize data rewards while considering energy and storage constraints. The authors proposed an Integer Linear Programming (ILP) solution and two heuristic algorithms to solve SDMP.

In [18], we addressed resource provisioning in a heterogeneous 5G network, aiming to maximize the benefit of Small Cell Access Points (SAPs) by determining the optimal Fog Servers (FSs) for offloading a set of IoT tasks. To achieve stability among IoTs, SAPs, and FSs within the cellular 5G networks, we implemented a Restricted Three-sided Matching with Size and Cyclic (R-TMSC) preference model. In [2], we introduced a cellular 5G network that facilitates the coexistence of heterogeneous SPs and Service Requesters (SRs). We formulated SPsâ revenue maximization problem through resource allocation, considering factors such as interference, data rate, and latency. Subsequently, we proposed a distributed many-to-many stable matching-based solution termed as Stable Matching based Static Resource Allocation (SMSRA) algorithm. Furthermore, we presented an adaptive stable matching-based distributed algorithm to address the problem in a dynamic network.

Shortcomings of the Existing Approaches: Existing works have primarily concentrated on enhancing the performance of UAV-assisted service transfer, neglecting the profit of the SP. As per our best knowledge, none of the existing studies tackle the collaborative integration of multi-UAVs as diverse service providers, considering factors such as interference management, PL optimization, capacity, latency, and energy constraints altogether. This integration is tackled through the joint optimization of UAV locations, PL, and PRB allocation within 5G network. Consequently, this paper introduces an innovative approach: Multi-UAV assisted service provisioning to maximize the SPâs profit in 5G network.

<!-- image-->  
Fig. 1. System model.

## III. SYSTEM MODEL

We consider a network framework comprises of a BS, UAVs, and UEs as shown in Fig. 1. The SP owns both the BS and the UAVs to accomplish its primary objective of delivering heterogeneous services to various UEs. Let $\mathbb { U } = \{ 1 , \dots , u , \dots , U \}$ and $\mathbb { M } = \{ 1 , \dots , m , \dots , M \}$ = 1be sets of UAVs and UEs, respec-= 1tively. The BS, denoted by Î´, manages the allocation of Physical Resource Blocks (PRBs)1 for establishing communication links between UAVs and UEs underlying cellular 5G network. Let $\mathbb { K } = \{ 1 , \dots , k , \dots , K \}$ and $\mathbb { L } = \{ 1 , \dots , l , \dots , L \}$ be the sets = 1of PRBs and $\mathrm { P L } \mathrm { s } ^ { 2 }$ = 1, respectively3 [2].

In this system, each UAV u is dedicated for providing a specific service, while each UE m requests for a particular service from BS at a time. For simplicity, let $\mathbb { S } \equiv \mathbb { U }$ be the available set of services for UEs. Both UAVs and UEs are inherently mobile, with changing positions over time. The system is analyzed over a series of predefined time intervals, represented by $\bar { \mathbb { T } } = \{ 1 , . . . , t , . . . , T \} . ^ { 4 }$ Let $\ell _ { \delta } = ( 0 , 0 , 0 ) \in \mathbb { R } ^ { 1 \times 3 } , \ell _ { u } ( t ) =$ $( x _ { u } ( t ) , y _ { u } ( t ) , h _ { u } ( t ) ) \in \mathbb { R } ^ { 1 \times 3 }$ , and $\ell _ { m } ( t ) = ( x _ { m } ( t ) , y _ { m } ( t ) , 0 )$ ( ( ) ( ) ( )) ( ) = ( ( ) ( ) 0)denote locations of BS Î´, UAV u, and UE m in 3D cartesian coordinate system, respectively. At different time intervals, the physical positions of UAVs and UEs, as well as their access patterns, may vary. To ensure the stability of service transfer, each UAV remains in a hovering state while the UEs are stationary [19]. However, UEs may exit the UAVâs coverage area after the service is delivered. As depicted in Fig. 2, there are two distinct stages for each UAV: hovering5 and traveling. During the hovering stage, UAV u adjusts its PL and requests for PRBs allocation from the BS for service transfer. Subsequently, BS allocates the necessary PRBs between UAV u and UE m (as illustrated in Fig. 3) to facilitate the service transfer to UEs within its coverage range. In traveling stage, each UAV proceeds to its next designated hovering location. This process ensures efficient coverage and service delivery across the network. A detailed description of the various entities involved in this model is discussed in the following section.

<!-- image-->  
Fig. 2. Stages of UAV.

<!-- image-->  
Fig. 3. Data flow diagram.

## A. Base Station

We assume that BS is connected to content servers on the Internet through high speed wired-line links, aiming to provide services to all UEs in association with UAVs [21]. However, if the BS provides services to all UEs directly, the increased distance to remote UEs necessitates maximum transmission power for each link, which limits PRB reuse due to interference, resulting in higher latency [22] and increased resource consumption [23]. To minimize the service latency, the BS dispatches a set UAVs that adjust their positions dynamically to be closer to UEs, thereby reducing communication distances, optimizing resource allocation to mitigate interference, and lowering service latency. Particularly, the roles of BS include receiving service requests from UEs, deploying UAVs to serve UEs, and allocating PRBs to establish communication links between UAVs and UEs as shown in Fig 3. Moreover, interference due to the re-usability of PRBs among UAVs and UEs necessitates efficient resource allocation in UAV-enabled 5G networks.

1) Communication Model: To serve UEs, it is essential to allocate PRBs between UEs and UAVs. Each UAV u can operate at a PL chosen from the set L. The selected PL l for UAV u is denoted by $p _ { u } ^ { l } ( t )$ , and $p _ { u } ^ { l } ( t ) < p _ { u } ^ { l ^ { \prime } } ( t )$ for ${ \mathit { l } } < { \mathit { l } } ^ { \prime }$ . Let $\Theta _ { u } ^ { l } ( t )$ be ( ) ( ) ( ) Î ( )the coverage range of UAV u at PL l. This range is defined as a distance within which the received signal strength from UAV u is higher than a specified threshold Î¶. Signal-to-Interference-Plus-Noise Ratio (SINR) at distance d from UAV u transmitting beacons at PL l and PRB k is denoted as $\Gamma _ { u , d } ^ { k , l } ( t )$ . Then, the coverage range $\Theta _ { u } ^ { l } ( t )$ can be calculated as $\Theta _ { u } ^ { l } ( t ) = \operatorname* { m a x } \{ d :$ $\Gamma _ { u , d } ^ { k , l } ( t ) \geq \zeta \}$ . It is worth noting that $\Theta _ { u } ^ { l } ( t ) < \Theta _ { u } ^ { l ^ { \prime } } ( t )$ = mfor ${ \mathit { l } } < { \mathit { l } } ^ { \prime } .$ Î ( ) Î ( ) Î ( )indicating that higher power levels result in an increased coverage range.

We define a binary variable, $X _ { u , m } ^ { ( k , l ) } ( t )$ to check PL and PRB ( )allocation between UAV u and UE m as:

$$
X _ { u , m } ^ { ( k , l ) } ( t ) = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f ~ U A V ~ } u \mathrm { ~ s e r v e s ~ U E ~ } m \mathrm { ~ a t ~ P R B ~ } k \mathrm { ~ a n d ~ } } \\ { ~ } & { \mathrm { ~ P L ~ } l \mathrm { ~ i n ~ t i m e ~ f r a m e ~ } t , } \\ { 0 , } & { \mathrm { ~ o t h e r w i s e . } } \end{array} \right.\tag{1}
$$

Thus, the achievable data rate of UAV u corresponding to UE m can be computed as follows [2]:

$$
R _ { u , m } ( t ) = \sum _ { k \in \mathbb { K } } \sum _ { l \in \mathbb { L } } X _ { u , m } ^ { ( k , l ) } ( t ) B \log _ { 2 } ( 1 + \Gamma _ { u , m } ^ { k , l } ( t ) ) ,\tag{2}
$$

where B is bandwidth corresponding to a PRB, and $\Gamma _ { u , m } ^ { k , l } ( t )$ represents SINR between UAV u and UE m, given as:

$$
\Gamma _ { u , m } ^ { k , l } ( t ) = \frac { G _ { u , m } ^ { k , l } ( t ) p _ { u } ^ { l } ( t ) } { I _ { u , m } ^ { k , l } ( t ) + \sigma ^ { 2 } } ,\tag{3}
$$

where $\sigma ^ { 2 } = \eta _ { 0 } B$ and, $\eta _ { 0 }$ denotes thermal noise. $G _ { u , m } ^ { k , l } ( t )$ and $I _ { u , m } ^ { k , l } ( t )$ are channel gain interference experienced between UAV ( )u and UE m, respectively given in (4) and (5):

$$
G _ { u , m } ^ { k , l } ( t ) = \frac { g _ { u } ^ { t x } g _ { m } ^ { r x } \left( \frac { c } { f _ { c } } \right) ^ { 2 } } { 1 6 \pi ^ { 2 } \left( \frac { d _ { u , m } ( t ) } { d _ { 0 } } \right) ^ { 2 } } ,\tag{4}
$$

$$
I _ { u , m } ^ { k , l } ( t ) = \sum _ { u ^ { \prime } \in \mathbb { U } , u ^ { \prime } \neq u } \sum _ { m ^ { \prime } \in \mathbb { M } } \sum _ { l ^ { \prime } \in \mathbb { L } } X _ { u ^ { \prime } , m ^ { \prime } } ^ { ( k , l ^ { \prime } ) } ( t ) G _ { u ^ { \prime } , m } ^ { k , l } ( t ) p _ { u ^ { \prime } } ^ { l } ( t ) ,\tag{5}
$$

where $g _ { m } ^ { r x }$ and $g _ { u } ^ { t x }$ are receiving and transmitting antenna gains of UE m, and UAV u, respectively. c is the speed of light, and $f _ { c }$ is the carrier frequency. $d _ { 0 }$ is the far field reference distance while $d _ { u , m } ( t )$ is the distance between UAV u and UE m, calculated as $d _ { u , m } ( t ) = \lVert \boldsymbol { \ell } _ { u } ( t ) - \boldsymbol { \ell } _ { m } ( t ) \rVert _ { 2 }$ . Moreover, $d _ { u , m } ( t ) \leq \Theta _ { u } ^ { l } ( t )$ , and $d _ { 0 } = 1$ m. $G _ { u ^ { \prime } , m } ^ { k , l } ( t )$ is the interference gain between any other = 1 ( )UAV u and UE m.

## B. UncrewedAerial Vehicles

To offer services to UEs, each UAV must undergo traversal, computation and communication, as described in the following section.

1) UAV Traversal Model: UAV u needs to traverse at a location $\ell _ { u } ^ { \prime } ( t ) = ( x _ { u } ^ { \prime } ( t ) , y _ { u } ^ { \prime } ( t ) , h _ { u } ^ { \prime } ( t ) ) \in \mathbb { R } ^ { 1 \times 3 }$ so that it can serve a ( ) = ( ( ) ( ) ( ))group of same service requesting UEs with better coverage and establish communication links. Thus, traversal latency of UAV u can be given by:

$$
\mathcal { T } _ { u , m } ^ { t r a v } ( t ) = \frac { d _ { u } ( t ) } { v _ { u } ( t ) } ,\tag{6}
$$

where $d _ { u } ( t ) = \Vert \ell _ { u } ( t ) - \ell _ { u } ^ { \prime } ( t ) \Vert _ { 2 }$ is the distance travelled by (UAV u and $v _ { u } ( t )$ ( ) ( )is average velocity of UAV u. Thus, traversal

TABLE II DESCRIPTION OF NOTATIONS
<table><tr><td>Symb.</td><td>Description</td></tr><tr><td>U, M, K,L</td><td>SetofUAVs,UEs,PRBsandPL,respectively</td></tr><tr><td> $U , M , K , L$ </td><td>Total number of UAVs,UEs,PRBsandPL,respectively</td></tr><tr><td> $\ell _ { \delta } , \ell _ { u } , \ell _ { m }$ </td><td>Location of DC,UAV u and UE m,respectively</td></tr><tr><td> $p _ { u } ^ { l } , \Gamma _ { u , m } ^ { k , l }$ </td><td>Power level of UAV u and SINR, respectively</td></tr><tr><td> $R _ { u , m }$ </td><td>Data rate of UAV u corresponding to UE m</td></tr><tr><td> $G _ { u . m } ^ { k , l }$ </td><td>Channel gain between UAV u and UE m</td></tr><tr><td> $\smash { \mathcal { T } _ { p s } ^ { t r a v } }$ </td><td>Traversal time of UAVu to serve UE m</td></tr><tr><td> $\mathcal { S } ^ { t r a v }$   $\varepsilon _ { u , m } ^ { \omega \upsilon }$ </td><td>Traversal energy of UAV u to serve UE m</td></tr><tr><td> $\mathcal { T } _ { u . m } ^ { t r a n s }$ </td><td>Transmission latency from UAV u to serve UE m</td></tr><tr><td> $\mathcal { E } _ { u . m . } ^ { t r a n s }$ </td><td>Transmission energy of UAV u to serve UE m</td></tr><tr><td> $\mathfrak { P } u , v _ { u }$ </td><td>Propulsion power and velocity of UAV u,respectively</td></tr><tr><td> $D _ { u , m }$ </td><td>Data size transferred from UAV u to UE m</td></tr><tr><td> ${ \mathcal { T } } _ { n } ^ { c o m p }$ </td><td>Total computation latency of UAV u to serve UE m</td></tr><tr><td> $\mathbf { \Sigma } _ { \mathcal { S } ^ { C O m p } } ^ { ' u , m }$   $\underline { { \boldsymbol { \varepsilon } } } _ { u , m } ^ { \mathrm { ~ \tiny ~ . ~ } }$ </td><td>Computation energy of UAV u to serve UE m</td></tr><tr><td> $\mathbb { E } _ { u , m }$ </td><td>Total energy consumption of UAV u to serve UE m</td></tr><tr><td> $\omega _ { u , m }$ </td><td>Total cost of UAV u to serve UE m</td></tr><tr><td>Î²u,m</td><td>Payment from UE m to UAV u</td></tr><tr><td> $\wp _ { u , m } ^ { t r a n s } , \wp _ { u , m } ^ { c o m p }$ </td><td>Payments for communication and computation</td></tr><tr><td>Sem</td><td>Payments for service</td></tr></table>

energy consumption of UAV u is given by [24]:

$$
\mathcal { E } _ { u , m } ^ { t r a v } ( t ) = \mathcal { T } _ { u , m } ^ { t r a v } ( t ) \mathfrak { P } _ { u } ( t ) ,\tag{7}
$$

where $\mathfrak { P } _ { u } ( t )$ is the propulsion power of UAV u.

( )2) UAV Transmission Model: Total transmission latency for transmitting service from UAV u to UE m, upon resource allocation i.e., $X _ { u , m } ^ { ( k , l ) } ( t ) > 0$ can be calculated as:

$$
\mathcal { T } _ { u , m } ^ { t r a n s } ( t ) = \frac { D _ { u , m } ( t ) } { R _ { u , m } ( t ) } ,\tag{8}
$$

where $D _ { u , m } ( t )$ is data size of the requested service transferred ( )from UAV u to UE m. Therefore, transmission energy of UAV u to transfer service to UE m is given by:

$$
\mathcal { E } _ { u , m } ^ { t r a n s } ( t ) = \mathcal { T } _ { u , m } ^ { t r a n s } ( t ) p _ { u } ^ { l } ( t ) .\tag{9}
$$

3) UAV Computation Model: Each UAV has the capability to serve multiple UEs that share its Central Processing Unit (CPU) capacity, denoted as $\Phi _ { u }$ . The CPU processing rate for each UE is Î¦influenced by the presence of other UEs sharing the same CPU resources. Let $C _ { u }$ be the CPU frequency of UAV u. For each co-CPU UE, an equal portion of the total CPU rate is allocated, which can be expressed as: $\begin{array} { r } { C _ { u , m } ( t ) = \frac { C _ { u } } { \sum _ { m \in \mathbb { M } } \sum _ { k \in \mathbb { K } } \sum _ { l \in \mathbb { L } } X _ { u , m } ^ { k , l } ( t ) } } \end{array}$ where $\begin{array} { r } { \sum _ { m \in \mathbb { M } } \sum _ { k \in \mathbb { K } } \sum _ { l \in \mathbb { L } } X _ { u , m } ^ { k , l } ( t ) > \overline { { 0 } } } \end{array}$ . Therefore, computa-( ) 0tion latency of UAV u to serve UE m can be given as:

$$
\mathcal { T } _ { u , m } ^ { c o m p } ( t ) = \frac { \vartheta _ { u } D _ { u , m } ( t ) } { C _ { u , m } ( t ) } ,\tag{10}
$$

where $\vartheta _ { u }$ is number of CPU cycles required for each input bit calculation. Thus, computation energy of UAV u to serve UE m can be calculated as:

$$
\mathcal { E } _ { u , m } ^ { c o m p } ( t ) = \vartheta _ { u } \nu _ { u } D _ { u , m } ( t ) .
$$

where $\nu _ { u }$ denotes energy consumption for each CPU cycle.

(11)

4) UAV Cost Model: The cost of UAVs for providing services to UEs can be quantified in terms of their energy expenditure. Total energy consumption of UAV u to serve UE m can be estimated as:

$$
\mathbb { E } _ { u , m } ( t ) = \mathcal { E } _ { u , m } ^ { t r a v } ( t ) + \mathcal { E } _ { u , m } ^ { t r a n s } ( t ) + \mathcal { E } _ { u , m } ^ { c o m p } ( t ) .\tag{12}
$$

Thus, total cost of UAV u to serve UE m is given as:

$$
\omega _ { u , m } ( t ) = \beta \mathbb { E } _ { u , m } ( t ) ,\tag{13}
$$

where $\beta$ is a parameter with unit dollar/joule energy.

## C. User Equipment

Based on the requested service type, BS assigns UAV u to serve UE m. Additionally, the BS allocates PRB $k \in \mathbb { K }$ to establish a communication link between UAV u and UE m. The request from UE m contains a five-tuple attribute $( m , \pmb { \mathscr { s } } _ { m } , D _ { m } , \pmb { \mathscr { L } } _ { m } , \ell _ { m } )$ , where m, $\mathfrak { s } _ { m } \in \mathbb { S } , D _ { m } , \mathcal { L } _ { m } ,$ and $\ell _ { m }$ rep-( )resent the id, service type, data size, latency requirement, and location of UE m, respectively. The revenue from UE m to UAV $u ,$ denoted as $\wp _ { u , m } ( t )$ , can be given as:

$$
\wp _ { u , m } ( t ) = \wp _ { u , m } ^ { t r a n s } ( t ) + \wp _ { u , m } ^ { c o m p } ( t ) + \wp _ { u , m } ^ { s e r v } ( t ) ,\tag{14}
$$

where $\wp _ { u , m } ^ { t r a n s } ( t ) , \wp _ { u , m } ^ { c o m p } ( t )$ , and $\wp _ { u , m } ^ { s e r v } ( t )$ represent payments for ( ) ( ) ( )communication, computation, and service, respectively. Here, $\wp _ { u , m } ^ { t r a n s } ( t ) = \beta \mathcal { E } _ { u , m } ^ { t r a n s } ( t )$ , and $\wp _ { u , m } ^ { c o m p } ( t ) = \beta \mathcal { E } _ { u , m } ^ { c o m p } ( t ) . \wp _ { u , m } ^ { s e r v } ( t )$ ( ) = ( )can be calculated as [25]:

$$
\wp _ { u , m } ^ { s e r v } ( t ) = f ( D _ { u , m } ( t ) , { \mathcal T } _ { u , m } ( t ) ) ,\tag{15}
$$

where $\mathcal { T } _ { u , m } ( t )$ is the total service delay between UAV u and UE ( )m for service. $f ( . )$ is monotonic increasing function for $D _ { u , m }$ and monotonic decreasing function for $\mathcal { T } _ { u , m }$ . For simplicity, we define $f ( D _ { u , m } ( t ) , \mathcal { T } _ { u , m } ( t ) )$ as:

$$
\begin{array} { r l r } {  { \wp _ { u , m } ^ { s e r v } ( t ) = \varrho \frac { D _ { u , m } ( t ) } { \mathcal { T } _ { u , m } ( t ) } } } \\ & { } & \\ & { } & { = \varrho \frac { D _ { u , m } ( t ) } { \mathcal { T } _ { u , m } ^ { t r a v } ( t ) + \mathcal { T } _ { u , m } ^ { t r a n s } ( t ) + \mathcal { T } _ { u , m } ^ { c o m p } ( t ) } , } \end{array}\tag{16}
$$

where 
 is a parameter with unit dollar/bps.

## D. Problem Formulation

We formulate the profit maximization problem for abovediscussed system architecture. The objective is to maximize the $\mathrm { { \sc ~ S P ~ s } }$ profit, defined as the difference between the revenues generated from offering services to UEs and UAVsâ deployment cost. Mathematically, this can be expressed as:

$$
\operatorname* { m a x } _ { X _ { u , m } ^ { k , l } ( t ) } \sum _ { u \in \mathbb { U } } \sum _ { l \in \mathbb { L } } \sum _ { m \in \mathbb { M } } \sum _ { k \in \mathbb { K } } \left( \wp _ { u , m } ( t ) - \omega _ { u , m } ( t ) \right) X _ { u , m } ^ { k , l } ( t )\tag{17}
$$

subject to:

$$
\mathcal { T } _ { u , m } ( t ) < \mathcal { L } _ { m } , \quad \forall u \in  { \mathbb { U } } , \forall m \in  { \mathbb { M } } ,\tag{17a}
$$

$$
\sum _ { l \in \mathbb { L } } \sum _ { k \in \mathbb { K } } \sum _ { m \in \mathbb { M } } X _ { u , m } ^ { k , l } ( t ) \leq \Phi _ { u } , \forall u \in \mathbb { U } ,\tag{17b}
$$

$$
R _ { u , m } ( t ) > R _ { \mathrm { t h r } } , \quad \forall u \in  { \mathbb { U } } , \forall m \in  { \mathbb { M } } ,\tag{17c}
$$

$$
\sum _ { u \in \mathbb { U } } \sum _ { l \in \mathbb { L } } \sum _ { k \in \mathbb { K } } X _ { u , m } ^ { k , l } ( t ) \leq 1 , \forall m \in \mathbb { M } ,\tag{17d}
$$

$$
\sum _ { m \in \mathbb { M } } \mathbb { E } _ { u , m } ( t ) < \mathcal { E } _ { u } ^ { \operatorname* { m a x } } ( t ) , \forall u \in \mathbb { U } ,\tag{17e}
$$

$$
d _ { u , u ^ { \prime } } ( t ) \geq d _ { \operatorname* { m i n } } , \quad \forall u , u ^ { \prime } \in \mathbb { U } , u \neq u ^ { \prime } ,\tag{17f}
$$

$$
X _ { u , m } ^ { k , l } ( t ) \in \{ 0 , 1 \} , \forall u \in \mathbb { U } , \forall m \in \mathbb { M } , \forall l \in \mathbb { L } , \forall k \in \mathbb { K }\tag{17g}
$$

where (17a) represents total service latency $\mathcal { T } _ { u , m } ( t )$ of UAV u should be less than maximum tolerable latency ${ \mathcal { L } } _ { m }$ of UE m. Eq. (17b) ensures the total number of UEs assigned to UAV u does not exceed its maximum capacity $\Phi _ { u }$ . Equation (17c) forces Î¦that the data rate between UAV u and UE m must exceed threshold data rate $R _ { \mathrm { t h r } }$ . Equation (17d) ensures each UE m is allocated to at most one UAV. Equation (17e) denotes the total energy consumption of UAV u remains below its maximum available energy $\mathcal { E } _ { u } ^ { \operatorname* { m a x } } ( t )$ . Equation (17f) represents the distance between ( )any two UAVs must be greater than $d _ { \mathrm { m i n } }$ to avoid collision. Equation (17g) denotes that the decision variable $X _ { u , m } ^ { k , l } ( t )$ is an integer constraint as per (1).

NP-hardness of the formulated problem is proven in the following theorem.

Theorem 1: Formulated problem (17) is NP-hard.

Proof: The well-known NP-complete 0/1 knapsack problem is mapped to the formulated problem (17). In 0/1 knapsack problem, from given items of different weights and prices, items must be selected in such a way that the total price of the items is the highest within a limited weight capacity. Referring to [26], consider a special case of the formulated problem, assuming that there is only one UAV u with its limited serving capacity $\Phi _ { u }$ . For the sake of simplicity, the constraints (17a), (17c), Î¦and (17e) are warded off. At this point, formulated problem can be reduced in polynomial time from a knapsack problem. Each request from UE m needs service from the UAV and pays $\wp _ { u , m } ( t )$ for getting service. Using only one UAV with limited ( )serving capacity, how to selectively serve requests from UEs, i.e, $\begin{array} { r } { \sum _ { m \in \mathbb { M } } \sum _ { k \in \mathbb { K } } \sum _ { l \in \mathbb { L } } X _ { u , m } ^ { k , l } ( t ) \leq \Phi _ { u } } \end{array}$ such that total profit of ( ) Î¦the UAV is maximized. Thus, the reduction method shows that the formulated problem is an NP-hard.

Due to the high complexity of the formulated problem, this paper proposes a semi-centralized MaDRC algorithm. By integrating MaDRL and Graph Coloring Algorithm (GCA), MaDRC enables real-time decision-making for UAVs in dynamic conditions and offers a near-optimal solution based on learned experiences. The following section provides a detailed discussion of the proposed algorithm.

## IV. MADRC ALGORITHM

In this section, we first re-model the formulated problem as a multi-agent extension of Markov Decision Process (MDP), which is then solved by the proposed MaDRC algorithm.

## A. MDP Formulation

We consider the above-defined system model as environment. Considering that UAVsâ actions may influence the environmental state, total profit is determined by current state of the environment and joint action of UAVs. Hence, the profit maximization problem can be re-formulated as a multi-agent MDP $\langle \mathbb { U } , S , \{ A _ { u } \} _ { u \in \mathbb { U } } , \epsilon , \{ r _ { u } \} _ { u \in \mathbb { U } } , \gamma \rangle$ where U is agent set, S is state set of all agents, Au is action space of agent u,  denotes state transition probability, $r _ { u }$ is reward function of agent $u ,$ and $\gamma \in [ 0 , 1 ]$ is discount factor. A detailed description is provided [0 1]in the following subsections.

1) MaDRC Agent Set: UAVs are modeled as agents in proposed MaDRC algorithm (see Fig. 4). UAVs learn to determine their position and PL in a manner that allows them to earn maximum profit while serving UEs with minimum interference in the environment. UAV set is denoted as agent set in rest of the manuscript.

2) State in MaDRC Module: The state of MaDRC agent u in DRL module is given by:

$$
s _ { u } ( t ) = \{ \ell _ { u } ( t ) , \psi _ { u } ( t ) , p _ { u } ^ { l } ( t ) \}\tag{18}
$$

<!-- image-->  
Fig. 4. Proposed MaDRC module.

Here, $\psi _ { u } ( t )$ denotes the total number of UEs receiving services ( )from agent u at PL $p _ { u } ^ { l } ( t )$ . This can be given as:

$$
\psi _ { u } ( t ) = \sum _ { m \in \mathbb { M } } \sum _ { k \in \mathbb { K } } X _ { u , m } ^ { k , l } ( t ) , ~ \forall d _ { u , m } < \Theta _ { u } ^ { l } ( t ) , \forall \mathfrak { s } _ { m } = = u\tag{19}
$$

3) Action in MaDRC Module: The possible actions of MaDRC agents directly correspond to directions of agents and respective PLs. Thus, the action space $a _ { u } ( t )$ of agent u is given as:

$$
a _ { u } ( t ) = \{ \emptyset _ { u } ( t ) , p _ { u } ^ { l } ( t ) \}\tag{20}
$$

where, $\boldsymbol { \mathcal { O } } _ { u } ( t )$ represents the flying direction of agent $u .$ . For ( )simplicity, we assume an UAV that can move in the direction of $0 ^ { 0 } , \dot { 4 } 5 ^ { 0 } , \dot { 9 } 0 ^ { 0 } , 1 3 5 ^ { 0 } , 1 8 0 ^ { 0 } , 2 2 5 ^ { 0 } , 2 7 0 ^ { 0 } , 3 1 5 ^ { 0 }$ , and $3 6 0 ^ { 0 }$ with a step 0 45length of $z _ { u }$ 135 180 225 270 315each time [6]. Based on action $a _ { u } ( t )$ 360, the coordinates of the next location $\ell _ { u } ( t + 1 )$ ( )of agent u can be calculated as [5]:

$$
x _ { u } ( t + 1 ) = x _ { u } ( t ) + z _ { u } ( t ) \cos ( \varpi _ { u } ( t ) )\tag{21}
$$

$$
y _ { u } ( t + 1 ) = y _ { u } ( t ) + z _ { u } ( t ) \sin ( \mathcal { D } _ { u } ( t ) )\tag{22}
$$

4) Reward in MaDRC Module: To solve the formulated problem (17), U agents should cooperatively maximize the profit of SP while satisfying constraints (17a)â(17f). Thus, the reward function of UAV u for providing service to UE m is given as:

$$
r _ { u , m } ( t ) = \left\{ \begin{array} { l l } { \left( \wp _ { u , m } ( t ) - \omega _ { u , m } ( t ) \right) X _ { u , m } ^ { k , l } ( t ) , } & { \mathrm { i f ~ s a t i s f i e s ~ a l l } } \\ { \qquad } & { \mathrm { c o n s t r a i n t s } , } \\ { - p _ { 1 } - p _ { 2 } - p _ { 3 } - p _ { 4 } - p _ { 5 } , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{23}
$$

where $p _ { 1 } , p _ { 2 } , p _ { 3 } , p _ { 4 }$ and $p _ { 5 }$ denote the penalties related to latency constraint (17a), capacity constraint (17b), data rate constraint (17c), energy constraint (17e), and minimum distance constraint (17f), respectively. Moreover, considering each UAV can serve multiple UEs simultaneously, the maximum expected discounted reward can be expressed as:

$$
\mathcal { R } ( t ) = \sum _ { u = 1 } ^ { U } \sum _ { m = 1 } ^ { M } r _ { u , m } ( t )\tag{24}
$$

## B. MaDRL Algorithm

In MaDRL module, each agent can acquire state information and execute policy based on the current communication network. The environment is then updated to the next state according to joint actions of all agents. Each agent interacts with environment continuously using a trial-and-error method and gets a reward corresponding to its action. The main objective is to create a policy Ï s that helps agents to take optimal decisions in any ( )situation, ultimately maximizing the long-term reward. This long-term reward is defined as the sum of the immediate reward and discounted future rewards of all potential states, and it can be represented as:

$$
r _ { u } ( t ) = \sum _ { t = 1 } ^ { T } \gamma r ( s _ { u } ( t ) , a _ { u } ( t ) )\tag{25}
$$

where $r ( . )$ represents the reward function. Each agent decides its action $a _ { u } ( t )$ based on -greedy policy for each decision episode. ( )The choice of optimal action in the current state depends on expected reward of each action in that state, represented by the state-action value function as:

$$
Q ( s _ { u } ( t ) , a _ { u } ( t ) ) = E _ { \pi } [ r _ { u } ( t ) | s _ { u } ( t ) , a _ { u } ( t ) ]\tag{26}
$$

In -greedy policy, each agent selects the action with maximum Q-value with probability  â , whereas a random action is taken 1with probability  to avoid getting stuck in a sub-optimal policy. The Q-value is continuously updated during training using the formula.:

$$
\begin{array} { r l } & { Q ( s _ { u } ( t ) , a _ { u } ( t ) ) = Q ( s _ { u } ( t ) , a _ { u } ( t ) ) } \\ & { + \alpha ( r + \gamma \operatorname* { m a x } Q ( s _ { u } ^ { \prime } ( t ) , a _ { u } ^ { \prime } ( t ) - Q ( s _ { u } ( t ) , a _ { u } ( t ) ) ) } \end{array}\tag{27}
$$

where Î± denotes learning rate. $s _ { u } ^ { \prime } ( t ) , a _ { u } ^ { \prime } ( t )$ represent the next ( ) ( )state and the action of agent u at time t  , respectively. To + 1enhance the efficiency of decision-making in RL, Deep Neural Network (DNN) is introduced to approximate optimal policy and value function. Specifically, DQN employs a DNN to approximate the action-value function, denoted as $Q ( s _ { u } ( t ) , a _ { u } ( t ) , \theta _ { u } )$ where $\theta _ { u }$ ( ( ) ( ) )signifies the weight parameter. DQN consists of two networks, i.e., Q-network and target network. Q-network is used for learning and prediction whereas, the target network with weight $\theta _ { u } ^ { - }$ deals with instability problem. In order to stabilize the training process, by copying the weights of corresponding Q-network, each agent updates the weight of target network every Î¼ step. Q-network updates its weight $\theta _ { u }$ in each training step using the gradient descent algorithm to minimize the loss function expressed as:

$$
\begin{array} { c } { { L ( { \theta } _ { u } ) = E [ ( r + \gamma \operatorname* { m a x } Q ( s _ { u } ^ { \prime } ( t ) , a _ { u } ^ { \prime } ( t ) ) , \theta _ { u } ^ { - } ) } } \\ { { - Q ( s _ { u } ( t ) , a _ { u } ( t ) , \theta _ { u } ) ] } } \end{array}\tag{28}
$$

In DQN algorithm, target network predicts the target Q-value which is expressed as:

$$
Q _ { u } ^ { \theta ^ { - } } = r + \gamma \operatorname* { m a x } Q ( s _ { u } ^ { \prime } ( t ) , a _ { u } ^ { \prime } ( t ) , \theta _ { u } ^ { - } )\tag{29}
$$

The Q-network predicts the current Q-value given by:

$$
Q _ { u } ^ { \theta } = r + \gamma \operatorname* { m a x } Q ( s _ { u } ( t ) , a _ { u } ( t ) , \theta _ { u } )\tag{30}
$$

In DNN, the gradient of the parameter can be calculated as:

$$
\begin{array} { r l } & { \nabla _ { { \theta } _ { u } } L _ { u } ( { \theta } _ { u } ) = E [ r + \gamma \operatorname* { m a x } Q ( s _ { u } ^ { \prime } ( t ) , a _ { u } ^ { \prime } ( t ) , \theta _ { u } ^ { - } ) } \\ & { \qquad - Q ( s _ { u } ( t ) , a _ { u } ( t ) , \theta _ { u } ) \nabla { \theta } _ { u } Q ( s _ { u } ( t ) , a _ { u } ( t ) , \theta _ { u } ) ] } \end{array}\tag{)](31}
$$

For stability and improved sample efficiency, each agent stores the current experience $( s _ { u } ( t ) , s _ { u } ^ { \prime } ( t ) , a _ { u } ( t ) , \mathcal { R } ( t ) )$ in re-( ( ) ( ) ( ) ( ))play buffer D. Agents randomly select mini-batches from D to

Algorithm 1: MaDRC Algorithm. Al   
Input: Location: $\ell _ { u } , \forall u \in \mathbb { U } , \ell _ { m } , \forall m \in \mathbb { M } ;$ capacity: I   
$\Phi _ { u } , \forall u \in \mathbb { U } , ,$ initial energy: $\mathcal { E } _ { u } \gets \mathcal { E } _ { u } ^ { m \hat { a } x }$ and,   
$X _ { u , m } ^ { k , l } \gets 0 , \forall u \in \mathbb { U } , \forall m \in \mathbb { M } , \forall l \in \bar { \mathbb { L } } , \forall k \in \mathbb { K }$   
Output: $\mathcal { R } ( t )$ C   
1for $u = 1$ toU do   
1 1   
2 Initialize $Q _ { u } ,$ and $\tilde { Q } _ { u }$ with D and weights $\theta _ { u } , \theta _ { u } ^ { - }$ 2 for 2f   
3 for episode = 1 to $Z$ do 3   
4 Initialize environment and the global state s(t); 4   
5 for $t = 1$ to Tdo 5 5   
6 for $u = 1$ to U do   
7 Obtain the state $s _ { u } ( t )$ and take action 6 for 6f   
$a _ { u } ( t )$ with e-greedy probability ; 7   
8 Execute action $a _ { u } ( t ) \ .$ 8 8   
9 Obtain next state $s _ { u } ( t + 1 )$ 9 9   
10 Obtain joint action of all agents, ${ \bf { a } } ( t ) ;$ 10 10   
11 Obtain s(t + 1) ; /\*Next $\mathrm { s t a t e } \quad \star /$   
12 Execute Algorithm 2 with input $\mathbf s ( t + 1 )$ and 11 11   
$\ell _ { m }$ ,Vm â M for PRB allocation; 12W   
13 for u=1 to U do 13 13   
14 $\mathcal { A } _ { u } = \phi ~ ;$ 14 14   
15 for m = 1 to M do 15 15   
16 $\mathbf { i f } \exists k \in \mathbb { K } , s . t . Y _ { u , m } ^ { k , l } = = 1$ then 16 16   
17 Estimate reward $r _ { u , m }$ 17 17   
18 $\mathcal { A } _ { u } \gets ( r _ { u , m } , m ) ,$ ï¼ 18 18   
19 Sort $\mathcal { A } _ { u }$ based on estimated reward ;   
20 form=1 to $| \mathcal { A } _ { u } |$ do 19r6   
21 if $\mathcal { E } _ { u } > \mathcal { E } _ { u } ^ { t \dot { h r } } \& \dot { \mathcal { E } } \subseteq \sum _ { m \in \mathbb { M } } X _ { u , m } ^ { k , l } < \Phi _ { u }$   
then   
22 if $\mathcal { T } _ { u , m } < \mathcal { L } _ { m } \& \& R _ { u , m } < R _ { t h r }$ then   
23 $X _ { u , m } ^ { k , l } = 1 , r _ { u } = r _ { u } + r _ { u , m } ;$ netw   
24 $\mathcal { E } _ { u } = \mathcal { E } _ { u } - \mathbb { E } _ { u , m } ;$ and   
of th   
2526 $u = 1$ to Utin intoreplaymemory MaDexpl   
$( s _ { u } ( t ) , a _ { u } ( t ) , r _ { u } ( t ) , s _ { u } ( t + 1 ) ) ;$ and   
27 Sample a random minibatch of transitions $( s _ { u } ^ { j } ( t ) , a _ { u } ^ { j } ( t ) , r _ { u } ^ { j } ( t ) , s _ { u } ^ { j } ( t + 1 ) )$ from D; $Q _ { u }$ $\theta _ { u }$ a   
$\dot { \nabla } _ { \theta _ { u } } L _ { u } ( \theta _ { u } )$ $\theta _ { u }$ beginUEs   
$\mu$   
30 Update weight $\theta _ { u } ^ { - }$ of the target-network are i   
In   
31 $\mathcal { R } ( t ) = \mathcal { R } ( t ) + r _ { u } ( t ) \ ; \quad / \star \mathrm { ~ E q ~ }$ curre   
its co

update their parameters. This reduces estimation inaccuracies, and enhance model convergence.

## C. MaDRC Algorithm

The proposed MaDRC algorithm exploits the concept of MaDRL and GCA. Unlike traditional MaDRL algorithms, our approach integrates resource allocation using GCA (i.e., Algorithm 2), with the goal of maximizing total profit in the network. The algorithm takes the initial positions of all agents and UEs, along with the capacities and maximum energy levels e UAVs, as input. Its output is the total profit for the SP. RC operates in three phases: initialization, exploitation or oration, and training.

gorithm 2: Graph Coloring Algorithm.   
Input: {lu}âueu,{lm}mâM,{pu}vuâu; /\* Output   
based on joint action of UAVs from   
Algorithm 1 \*/   
Output: $\{ Y _ { u , m } ^ { ( k , l ) } ( t ) \} _ { \forall u \in \mathbb { U } , \forall m \in \mathbb { M } }$   
$\mathcal { V }  \phi , \chi  \phi ;$   
$u = 1$ to U do   
for m=1 to M do   
if (service $t y p e { = } { = } u ) \& \& ( d _ { u , m } < \Theta _ { u } ^ { l } )$ then   
$\underline { { \vert } } \mathcal { V } \gets ( \bar { u , } m )$   
${ \mathfrak { v } } = 1$ to |V| do   
for $\mathfrak { v } ^ { \prime } = 1$ to_IV|do   
if $\mathfrak { v } \ne \mathfrak { v } ^ { \prime }$ then   
$\mathrm { i } \mathbf { \check { f } } u = = u ^ { \prime } | | d _ { u , m ^ { \prime } } < \Theta _ { u } ^ { l } | | d _ { u ^ { \prime } , m } < \Theta _ { u ^ { \prime } } ^ { l }$ then   
$\mathsf { L } \mathrm { \Delta } \chi \gets ( \mathsf { v } , \mathsf { v } ^ { \prime } )$   
$k  0 .$ $/ \star$ Color represents PRB $\star /$   
12 while V is not an empty set do   
if $k \leq K$ then   
$k \gets k + 1 ;$   
Pick a MIS, $\mathcal { V } ^ { I } \subseteq \mathcal { V }$   
Assign color k to all vertices $\mathfrak { v } \in \mathcal { V } ^ { I }$   
Set $\breve { Z } _ { \mathfrak { v } } ^ { k } = 1 , \forall \mathfrak { v } \in \mathcal { V } ^ { I }$   
Remove all $\mathfrak { v } \in \mathcal { V } ^ { I }$ from $\nu ,$ and remove all   
edges that have at least one endpoint in $\mathcal { V } ^ { I }$   
19 return $\{ Y _ { u , m } ^ { k , l } ( t ) \gets Z _ { \mathfrak { v } } ^ { k } \} _ { \forall u \in \mathbb { U } , \forall m \in \mathbb { M } }$

In Initialization phase, initial allocation between each agent and UE is set to 0. Each agent initializes its action-value function and target action-value function $\tilde { Q } _ { u }$ with respective weights and $\theta _ { u } ^ { - }$ along with its replay memory D (lines 1 - 2). At ning of each episode, the environment is reset: agents and return to their initial positions, agentsâ energy is set to maximum, allocations are reset to 0, and rewards for all agents nitialized to 0 (lines 3 - 4).

exploitation or exploration phase, each agent obtains its current state, which includes its location, number of UEs within verage range, and its PL at each time step of an episode. After observing the current state, agent takes action $a _ { u } ( t )$ according to its current policy and then obtains its next state $s _ { u } ( t + 1 )$ (lines $5 \textrm { - } 9 )$ ( + 1). Obtain joint action a t taken by all agents and global ( )state s t (i.e., locations, PLs, and number of UEs in the ( + 1)coverage range for all agents) in accordance with their action (lines 10 - 11). Feed $\mathbf s ( t + 1 )$ , and location of all UEs as input to ( + 1)Algorithm 2. Allocate PRBs between UAVs and UEs for service transfer (line 12). For each agent $u ,$ estimate the profit $r _ { u , m }$ of each UE $m \in M$ , if PRB is allocated, and store it along with UE m in list $\mathcal { A } _ { u }$ (lines 13-18). Sort the list $\mathcal { A } _ { u }$ for each agent u based on its profit in decreasing order (line 19). For each UE in $\mathcal { A } _ { u }$ of

UAV $u ,$ if remaining energy $\mathcal { E } _ { u }$ is greater than $\mathcal { E } _ { u } ^ { t h r }$ (constraint $( l 7 e ) )$ , current allocated UEs i.e. $\cdot , \bar { \sum } _ { m \in \mathbb { M } } X _ { u , m } ^ { k , l }$ is less than $\Phi _ { u }$ (constraint (17b)), estimated service latency $\mathcal { T } _ { u , m }$ Î¦is less than ${ \mathcal { L } } _ { m }$ (constraint (17a)), and data rate $R _ { u , m }$ is greater than $R _ { t h r }$ (constraint (17c)), then UE m is allocated to agent u for service transfer, and obtain reward $r _ { u }$ (lines 20-24).

In training phase, For each UAV u, store $( s _ { u } ( t ) , a _ { u } ( t )$ $r _ { u } ( t ) , s _ { u } ( t + 1 ) )$ ( ( ) ( )into replay buffer D, then sample a random ( ) ( + 1))minibatch of transitions $( \bar { s _ { u } ^ { j } } ( t ) , a _ { u } ^ { j } ( t ) , r _ { u } ^ { j } ( t ) , s _ { u } ^ { j } ( t + 1 ) )$ from D. Update weight $\theta _ { u }$ ( ( ) ( )and the gradient $\nabla _ { \theta _ { u } } L _ { u } ( \theta _ { u } )$ 1))of the $Q \mathrm { - }$ ( )network, accordingly. After Î¼ steps, update weight $\theta _ { u } ^ { - }$ of the target-network (lines 11-30). Obtain final reward $\mathcal { R } ( t )$ using (24) (line 31).

1) Graph Coloring Algorithm: GCA (Algorithm 2) has been exploited for efficient PRB allocation in the network, where each PRB is denoted as a color [23]. Specifically, this allocation is achieved by constructing a Link Conflict Graph (LCG) and performing node coloring, with each node representing a communication link between UAVs and UEs. To construct LCG, we need locations and PLs of UAVs along with locations of UEs from MaDRC algorithm. The graph is then colored using the minimum number of colors, which corresponds to minimizing the number of PRBs needed for transmitting services to each UE. The operations of the GCA are described below.

For LCG construction, initialize empty vertex and edge sets represented as $\nu ,$ and $\chi ,$ respectively (line 1). For each UAV u and UE m, if service type $\mathrm { i } . \mathrm { e } . , \mathfrak { s } _ { m }$ is same as u, and UE m is in range of UAV u then constructs a node $( u , m )$ and stores it ( )in V (lines 2-5). After including all possible nodes, edges are drawn between them. Each edge represents an interference link and is constructed if it satisfies either of the two conditions: (a). For each node ${ \mathfrak { v } } , { \mathfrak { v } } ^ { \prime } \in \nu$ where $\mathfrak { v } \ne \mathfrak { v } ^ { \prime } .$ , if UAV $u \in { \mathfrak { v } }$ is same as UAV $u ^ { \prime } \in { \mathfrak { v } } ^ { \prime } . \left( { \mathfrak { b } } \right)$ . For each node ${ \mathfrak { v } } , { \mathfrak { v } } ^ { \prime } \in \nu$ where $\mathfrak { v } \ne \mathfrak { v } ^ { \prime }$ , if UE m $\in { \mathfrak { v } }$ is in range of UAV $\boldsymbol { u } ^ { \prime } \in \mathfrak { v } ^ { \prime }$ or UE $m ^ { \prime } \in { \mathfrak { v } } ^ { \prime }$ =is in range of $\mathrm { U A V } ~ u \in { \mathfrak { v } }$ , then an interfering edge is constructed between v and v . Store the edge in Ï (lines 6-10). For node coloring, GCA picks up a Maximal Independent Set (MIS) [27] from LCG and assigns a unallocated color $k \in \mathbb { K }$ to it. Repeat it until all nodes are colored or colors are exhausted (lines 11-18). Finally, GCA returns PRB for all possible UAV-UE link (line 19).

## D. Complexity and Convergence Analysis

In this section, we discuss the complexity analysis of the proposed MaDRC algorithm, which comprises MaDRL and GCA. First, we explore the complexity of GCA and MaDRL. Subsequently, we address overall complexity MaDRC algorithm in the following.

In centralized PRB allocation, the BS communicates with UAVs to gather their locations and PL information, resulting in a complexity $O ( U )$ . Moreover, for PRB allocation, the complexity ( )for obtaining nodes is O U M (lines 1-5), the complexity for obtaining edges is $O ( | \mathcal { V } | ^ { 2 } )$ )(lines 6-10), and the complexity ( )for obtaining all MIS is O |V| |Ï|  |V|  k [27] (lines $\ 1 2 \AA - I 9 )$ ( ( + log )). Here, k is the total number of MIS, where $k \leq K$ $O ( | \mathcal { V } | ( | \chi | + | \mathcal { V } | \log k ) )$ can be represented as $O ( | \nu | ^ { 3 } )$ in worst ( ( + log )) ( )case. Thus, overall complexity of Algorithm 2 can be written as $O ( U M + | \mathcal { V } | ^ { 2 } + | \mathcal { V } | ^ { 3 } ) \overset { \cdot } { = } O \overset { \cdot } { ( } | \mathcal { V } | ^ { 3 } )$

TABLE III EXPERIMENT SETTINGS
<table><tr><td rowspan=1 colspan=1>Data</td><td rowspan=1 colspan=1>[M</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1> $\overline { { \Phi _ { u } } }$ </td><td rowspan=1 colspan=1> $\overline { { | \mathcal { L } _ { m } | } }$ </td></tr><tr><td rowspan=1 colspan=1>Set#1</td><td rowspan=1 colspan=2>50-250</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>Set #2</td><td rowspan=1 colspan=2>100</td><td rowspan=1 colspan=1>2-5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>Set#3</td><td rowspan=1 colspan=2>100</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>10-30</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>Set #4</td><td rowspan=1 colspan=2>100</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>5-25</td></tr></table>

In decentralized training process of MaDRL, each agent estimates Q-function values with Q-network and target network, where sizes of inputs and output are 5 (i.e., $x _ { u } ( t ) , y _ { u } ( t ) , h _ { u } ( t ) , p _ { u } ^ { l } ( t ) , \psi _ { u } ( t ) )$ ) and $2 ( \mathrm { i . e . , } \emptyset _ { u } ( t ) , p _ { u } ^ { l } ( t ) )$ , re-( ) ( ) ( ) ( ) ( ) ( ) ( )spectively. For a given fully connected neural network with fixed numbers of hidden layers and neurons, the computational complexity of back-propagation algorithm is proportional to product of input size and output size [5], [34]. Thus, overall complexity of decentralized MaDRL is $O ( U ^ { 2 } )$ .

( )The input for proposed MaDRC algorithm is $5 U + 3 M +$ 5 + 3 +UM, whereas the output is 1. After getting input, each UAV initializes Q-value, and target Q-value with weight $\theta _ { u }$ and $\theta _ { u } ^ { \prime }$ respectively along with replay buffer D. So, the complexity of initialization process is $O ( U )$ (lines 1-2). In each episode, ( )the complexity of initializing the environment with its initial values and getting global state is $O ( 5 U + 3 M + U M + 5 U ) =$ $O ( U M )$ (5 + 3 + + 5 ) =(lines 3-4). The complexity of taking action and ex-( )ecuting it in a decentralized way is constant in each time step and its complexity can be written as $O ( U )$ (lines 6-9). ( )The complexity of obtaining joint action and global state is O U (lines 10-11). Complexity of executing GCA algorithm is $\dot { O } ( | \mathcal { V } | ^ { 3 } )$ (line 12). The complexity for estimating and storing ( )reward of each UE in the list is O U M (lines 13-18). The ( )complexity for estimating and storing reward of each UE in the list is $\dot { O } ( U ( M + | A _ { u } | \log | A _ { u } | + | \dot { A } _ { u } | ) ) = O ( U M \log M )$ ( ( + log + )) = ( log )(lines 13-24). The complexity of storing the transition, sampling minibatch, and updating the weight of Q-network and targetnetwork is MADQN algorithm is $\mathsf { \bar { O } } ( U ^ { 2 } )$ (lines 25-31).

(Thus, complexity of MaDRC is ${ \cal O } ( U ) + { \cal O } ( Z ( U M +$ $U + | \mathcal { V } | ^ { 3 } ) + \bar { U } M + U M \log M + U ^ { 2 } ) \rangle$ ( ) +. Assuming $M > > U$ + ) + + log + ))complexity the proposed algorithm can be given as $O ( | \nu | ^ { 3 } )$

## V. PERFORMANCE STUDY

In this section, training performance of the proposed algorithm is analyzed. We first describe our environment setting and then analyze the simulation results in the following.

## A. Simulation Setup

We consider a square area of 200 m Ã 200 m to simulate the proposed algorithm. We have plotted different results as per the experiment settings mentioned in Table III. Tables IV and V represent the specific parameter setup for the network. MaDRC network has been designed with three hidden layers, containing 500, 400, and 300 neurons. A total of 5000 episodes of training are carried out, where each episode of training contains 50 execution steps. At the beginning of each episode, UEs locations are randomly initialized, and UAVs are located at BS. After that, in each episode of training, each UAV selects an action as per its current state, and obtains the corresponding reward and next state.

TABLE IV SIMULATION SETUP
<table><tr><td>Parameter</td><td>Vaue</td></tr><tr><td>Area Maximum velocity of UAVs</td><td>200Ã200mÂ² 30 m/s [28]</td></tr><tr><td>Transmit power of UAVs Transmit power of BS</td><td>40 dBm (10 W)[29] [30]</td></tr><tr><td></td><td>46.99 dBm [30]</td></tr><tr><td>Propulsion power of UAVs</td><td>386.32J/sec [31]</td></tr><tr><td>CPU cycle</td><td>500 cycle/bit [32]</td></tr><tr><td>Height of UAV Enegry consumption of 1 CPU cycle</td><td>50 meter [28]</td></tr><tr><td>J</td><td>9.5Ã10-11 J/cycle [32] 1.4Ã10-4[15]</td></tr><tr><td>Set of PL, L</td><td>{20,24,30,36,42} dBm [2]</td></tr><tr><td>no</td><td>-174 dBm/Hz_[2]</td></tr><tr><td>Bandwidth</td><td>20MHz[2]</td></tr><tr><td>PRB bandwidth</td><td>180 kHz [2]</td></tr><tr><td>UAV energy</td><td>1000J[28]</td></tr><tr><td>dmin</td><td>1 m [7]</td></tr><tr><td>Î²</td><td>0.05[24]</td></tr><tr><td>Carrier frequency, fe</td><td>2 GHz [2]</td></tr><tr><td>CPU frequency of UAV u, Cu</td><td>20 GHz [33]</td></tr><tr><td> $R _ { t h r }$ </td><td></td></tr><tr><td>No.of PRBs,K</td><td>[0.002-2] Mbps [2] 30</td></tr></table>

TABLE V

PARAMETERS OF MADRC
<table><tr><td rowspan=1 colspan=4>Parameter of neural network</td></tr><tr><td rowspan=1 colspan=1>Layers</td><td rowspan=1 colspan=1>Number</td><td rowspan=1 colspan=1>Size</td><td rowspan=1 colspan=1>Act.Function</td></tr><tr><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Hidden</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>500,400,300</td><td rowspan=1 colspan=1>ReLU</td></tr><tr><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>tanh</td></tr><tr><td rowspan=1 colspan=4>Key parameters of training stage</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>memory size</td><td rowspan=1 colspan=1>105</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=2>batch size</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=1 colspan=1>a</td><td rowspan=1 colspan=2>learning rate</td><td rowspan=1 colspan=1>0.0001</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>discount factor</td><td rowspan=1 colspan=1>0.98</td></tr><tr><td rowspan=1 colspan=1>e</td><td rowspan=1 colspan=2>greedy probability</td><td rowspan=1 colspan=1>0.2</td></tr><tr><td rowspan=1 colspan=1>ç</td><td rowspan=1 colspan=2>steps for updating target network</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>P</td><td rowspan=1 colspan=2>penalty</td><td rowspan=1 colspan=1>1000</td></tr><tr><td rowspan=1 colspan=1>Z</td><td rowspan=1 colspan=2>training episodes</td><td rowspan=1 colspan=1>5000</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=2>number of steps</td><td rowspan=1 colspan=1>50</td></tr></table>

We have compared our outcomes with the existing MACEL model [6], Multi-Agent Deep Q Learning (MADQL) algorithm, optimal solution using âGurobi Optimizerâ, and greedy algorithm. In MACEL and MADQL, flying direction, PL, and PRB allocation of each agent are selected using MADQN network. Gurobi Optimizer jointly determines UAVs positions, PLs, and allocates PRBs based on the current locations of UEs. Furthermore, the greedy approach positions UAVs to maximize the number of UEs served, without considering energy consumption and latency. Each UAV aims to serve maximum number of UEs at its maximum PL while randomly allocating PRBs, neglecting interference. We have used the same framework to compare all algorithms on a Windows 11 Pro system with an NVIDIA GeForce RTX 3050 Ti, utilizing Python 3.8.16 and PyTorch 2.1.0.

## B. Training Efficiency

Fig. 5 illustrates the training results obtained by deploying 3 UAVs to serve 100 UEs. Fig. 5(a) shows the convergence speed of the proposed MaDRC algorithm at various learning rates. The results indicate that a high learning rate $( \mathrm { e . g . , } \alpha = 0 . 1 )$ prevents = 0 1convergence, while lower rates slow it down but improve the systemâs average reward after convergence. The red box in the figure highlights this trade-off, demonstrating that a learning rate of 0.0001 achieves a balance between convergence speed and final performance.

The training curve of MaDRC in Fig. 5(b) shows that the reward starts increasing after 2000 episodes until convergence. Initially, agents explore the environment through random actions, after which the MaDRC model is trained using these experiences to serve UEs. This approach helps agents avoid penalties and gradually improve their rewards until convergence. In comparison, the MACEL and MADQL models face challenges due to their large action spacesâexpanding exponentially with the number of PRBsâwhile MADQLâs independent learning can lead to uneven performance among UAVs. Consequently, some UAVs may excel while others underperform, disrupting overall network efficiency. In contrast, MaDRC outperforms both models by utilizing GCA for PRB allocation, which reduces the action space and effectively manages interference, allowing for optimal selection of flying directions and PL, thereby enhancing overall performance.

After training using MaDRC algorithm, Fig. 5(c) presents the corresponding serving locations of three UAVs delivering high data rate multimedia content, along with their flight paths. UEs with different content demands are represented by different colors, where each UE requests one of the three types of services (audio, video, or files) provided by UAVs. The lavender shade represents the coverage area of each UAV, with each UAV positioned at the center of a cluster of UEs demanding its specific service. The content demand for each UE, $D _ { u , m } ( t )$ , is within the ( )[500k, 1M] bits range, and the maximum service latency varies between 5 and 25 seconds, depending on the service type.

## C. Result Analysis With Various Approaches

In this section, training performance of MaDRC is analyzed, and results are compared against MACEL, MADQL, optimal and greedy algorithm simulation results.

Fig. 6 compares the proposed algorithm against other methods on experiment data set 1 given in Table III. In Fig. 6(a), a #comparison is shown against total profit over total number of UEs in the network. Given that each UAV can serve up to 20 UEs (i.e., the capacity constraint $\Phi _ { u } = 2 0$ , we observe a gradual Î¦ = 20increase in reward as the number of UEs grows from 50 to 150. However, beyond this point, adding more UEs does not result in a significant increase in reward. This is because the serving capacity of the UAVs is fully utilized, and any additional UEs cannot be effectively served due to resource limitations. The proposed algorithm achieves a profit of 99.05% in comparison to optimal profit, outperforming MACEL, MADQL and greedy approaches, which achieve 61.44%, 56.29% and 49.47% of the overall profit, respectively. Furthermore, Fig. 6(b) and (c) show a comparison between UEs with total energy consumption and average latency, respectively. The energy consumption of the optimal algorithm is 3.52%, 48.87%, 55.01%, and 70.05% more efficient compared to MaDRC, MACEL, MADQL, and greedy algorithms, respectively. Moreover, optimal value of service latency is 3.54%, 22.70%, 25.11%, and 44.07% more efficient compared to proposed MaDRC, MACEL, MADQL, and greedy algorithms, respectively. As the number of UEs increases from 50 to 100, both energy consumption and average latency rise, as each UAV operates at maximum capacity. However, once enough UEs are present, energy consumption and latency begin to decrease, allowing each UAV to focus on selecting the most rewarding UEs with lower energy and latency within its limited capacity. Greedy algorithmâs strategy of maximizing coverage with UAVs at maximum PL leads to maximum energy consumption, latency, and interference, leading to poorest performance among compared algorithms. Additionally, we notice that the optimal solution performs slightly better than the proposed MaDRC, as UAVs in the optimal solution can be positioned at fractional coordinates, whereas in MaDRC, they are constrained to discrete coordinates, resulting in lower energy consumption and latency and improved profit.

<!-- image-->

(a) Reward under different learning rates.  
<!-- image-->  
(b) Reward per episode.

<!-- image-->  
(c) UAVs path.

Fig. 5. Results after training (UAVs = 3, UEs = 100).  
<!-- image-->  
(a) Profit v/s no. of UEs.

<!-- image-->  
(b) Energy v/s no. of UEs.

<!-- image-->  
(c) Latency v/s no. of UEs.

Fig. 6. Performance evaluation based on data set #1.  
<!-- image-->  
(a) Profit v/s no. of UAVs.

<!-- image-->  
(b) Energy v/s no. of UAVs.

<!-- image-->  
(c) Latency v/s no. of UAVs.  
Fig. 7. Performance evaluation based on data set #2.

Fig. 7 demonstrates experimental results obtained based on data set 2. Fig. 7(a) depicts a relation between total #profit and number of UAVs, for which proposed algorithm achieves 99.13% to optimal profit compared to 54.43%, 48.06% and 43.91% for MACEL, MADQL and greedy algorithm, respectively. Fig. 7(b) and (c) illustrate the relation of the number of UAVs with total energy consumption and average latency, respectively. The energy consumption of optimal algorithm is 3.52%, 51.33%, 62.38%, and 73.91% more efficient compared to the proposed MaDRC, MACEL, MADQL and greedy algorithms, respectively. Moreover, optimal value of the service latency is 1.68%, 22.70%, 26.71%, and 46.07% more efficient compared to the proposed MaDRC, MACEL, MADQL, and greedy algorithms, respectively. Itâs notable that energy consumption of UAVs tends to rise with an increasing number of UAVs, primarily due to the additional traversal energy required. Additionally, with a fixed number of UEs, average serving latency of UAVs decreases as number of UAVs rises.

Fig. 8 showcases the proposed algorithm using parameter data set 3. In Fig. 8(a), we see that the capacity of each UAV to #serve UEs ranges from 10 to 30, where the proposed MaDRC achieves 99.46% to optimal profit compared to 55.15%, 52.62% and 49.23% for MACEL, MADQL, and greedy algorithm, respectively. Notably, thereâs a clear positive relationship between the increase in UAV capacity and total profit. Furthermore, in Fig. 8(b) and (c), we observe the effect of capacity constraints upon total energy consumption and average latency, respectively. Energy consumption of optimal algorithm is 1.47%, 18.33%, 28.95%, and 65.25% more efficient compared to MaDRC, MADQL, MACEL, and greedy algorithms, respectively. Moreover, optimal value of service latency is 1.54%, 20.61%, 27.16%, and 40.98% more efficient compared to MaDRC, MACEL, MADQL, and Greedy algorithms, respectively. As each UAV gains the ability to serve more UEs, we can see that both energy consumption and average serving latency increase with the higher capacity constraint.

<!-- image-->  
(a) Profit v/s capacity.

<!-- image-->  
(b) Energy v/s capacity.

Fig. 8. Performance evaluation based on data set #3.  
<!-- image-->  
(c) Latency v/s capacity.

<!-- image-->  
(a) Profit v/s latency.

<!-- image-->  
(b) Energy v/s latency.  
Fig. 9. Performance evaluation based on data set #4.

Analysis of data set 4 is depicted in Fig. 9. In Fig. 9(a), #each UAV can serve up to 20 UEs, but the maximum allowed latency for serving each UE varies between  â  seconds. Our 5 25proposed algorithm achieves 99.05% to optimal profit compared to 47.17%, 45.42% and 39.93% for MACEL, MADQL, and greedy algorithm, respectively. The graph shows that the reward initially increases as the latency constraint tightens from 5 to 10 seconds, but levels off thereafter, indicating a saturation point due to fixed capacity. Moreover, a comparison between latency constraint and total energy consumption of UAVs is shown in Fig. 9(b). Energy consumption of optimal algorithm is 3.52%, 51.33%, 52.93%, and 73.11% more efficient compared to MaDRC, MADQL, MACEL, and greedy algorithms, respectively. As the maximum acceptable latency for serving a UE increases, UAVs energy consumption also rises, as they can handle more UEs within the extended latency. However, energy consumption eventually levels off once UAVs reach their maximum serving capacity.

Fig. 10(a) shows the average ratio of hovering latency to traversal latency under the capacity constraint of UAV u. The ratio increases with larger data sizes due to higher transmission latency and with greater capacity constraints as $C _ { u }$ is shared among more UEs. Fig. 10(b) compares the profit of the SP using only BS versus using BS in conjunction with UAVs. The results are plotted using 3 UAVs and 100 UEs in an area of 200 m Ã  m. The BS, limited to 30 PRBs (K ), 200 = 30serves only 30 UEs to avoid interference. In contrast, UAVs, each with a capacity of $\phi _ { u } = 2 0$ , reuse PRBs by adjusting their locations to minimize overlapping coverage, enabling them to serve more UEs without interference. This results in higher profit for UAV-assisted system than the BS-only setup, highlighting the advantages of UAV-assisted service provisioning over direct BS-UE communication.

(a) Average ratio v/s no. of UEs.  
<!-- image-->

<!-- image-->  
(b) Profit $\mathrm { v } / \mathrm { s }$ no. of UEs.  
Fig. 10. Effect of UEs on average latency and total profit.

## VI. CONCLUSION AND FUTURE WORKS

This paper presented a multi-UAV-assisted framework for service transfer focusing interference management and UAVsâ energy efficiency, where BS collaboratively allocates the radio resources between UAVs and UEs. Formulated an optimization problem that maximizes $\mathrm { S P ^ { \circ } s }$ profit while considering energy, latency, and capacity constraints of UAVs. The formulated optimization problem is solved using a novel semi-centralized MaDRC algorithm which combines MaDRL and GCA. Extensive simulation analysis validate the framework, achieving an average of 99.05% profit compared to the optimal value.

In future, this approach could be expanded to support multiple SPs and BSs, addressing priority-based service demands from UEs across multiple PRB allocations. This extension might involve integrating continuous space DRL with a stable-matching algorithm, enabling precise UAV placement and efficient PRB allocation. Such a combination would enhance real-time performance and robustness in 5G/6 G communication environments.

## REFERENCES

[1] X. Ye and L. Fu, âJoint MCS adaptation and RB allocation in cellular networks based on deep reinforcement learning with stable matching,â IEEE Trans. Mobile Comput., vol. 23, no. 1, pp. 549â565, Jan. 2024.

[2] A. Pratap and S. K. Das, âStable matching based resource allocation for service providerâs revenue maximization in 5G networks,â IEEE Trans. Mobile Comput., vol. 21, no. 11, pp. 4094â4110, Nov. 2022.

[3] Q. Chen, H. Zhu, L. Yang, X. Chen, S. Pollin, and E. Vinogradov, âEdge computing assisted autonomous flight for UAV: Synergies between vision and communications,â IEEE Commun. Mag., vol. 59, no. 1, pp. 28â33, Jan. 2021.

[4] B. Tian et al., âUAV-assisted wireless cooperative communication and coded caching: A multiagent two-timescale DRL approach,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4389â4404, May 2024.

[5] N. Zhao, Z. Ye, Y. Pei, Y.-C. Liang, and D. Niyato, âMulti-agent deep reinforcement learning for task offloading in UAV-assisted mobile edge computing,â IEEE Trans. Wireless Commun., vol. 21, no. 9, pp. 6949â6960, Sep. 2022.

[6] Z. Daii, Y. Zhang, W. Zhang, X. Luo, and Z. He, âA multi-agent collaborative environment learning method for UAV deployment and resource allocation,â IEEE Trans. Signal Info. Process. Over Net., vol. 8, pp. 120â130, 2022.

[7] L. Wang, K. Wang, C. Pan, W. Xu, N. Aslam, and L. Hanzo, âMulti-agent deep reinforcement learning-based trajectory planning for multi-UAV assisted mobile edge computing,â IEEE Trans. Cogn. Commun. Netw., vol. 7, no. 1, pp. 73â84, Mar. 2020.

[8] D. Wu, X. Sun, and N. Ansari, âAn FSO-based drone assisted mobile access network for emergency communications,â IEEE Trans. Netw. Sci. Eng., vol. 7, no. 3, pp. 1597â1606, Jul. 2020.

[9] A. Khochare, F. B. Sorbelli, Y. Simmhan, and S. K. Das, âImproved algorithms for co-scheduling of edge analytics and routes for UAV fleet missions,â IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 17â33, Feb. 2024.

[10] Y. Liu, K. Liu, J. Han, L. Zhu, Z. Xiao, and X. -G. Xia, âResource allocation and 3-D placement for UAV-enabled energy-efficient IoT communications,â IEEE Internet Things J., vol. 8, no. 3, pp. 1322â1333, Feb. 2021.

[11] S. Fu et al., âEnergy-efficient UAV-enabled data collection via wireless charging: A reinforcement learning approach,â IEEE Internet Things J., vol. 8, no. 12, pp. 10209â10219, Jun. 2021.

[12] X.-W. Tang, X. -L. Huang, and F. Hu, âQoE-driven UAV-enabled pseudoanalog wireless video broadcast: A joint optimization of power and trajectory,â IEEE Trans. Multimedia, vol. 23, pp. 2398â2412, 2020.

[13] S. Zhou, Y. Cheng, X. Lei, Q. Peng, J. Wang, and S. Li, âResource allocation in UAV-assisted networks: A clustering-aided reinforcement learning approach,â IEEE Trans. Veh. Technol., vol. 71, no. 11, pp. 12 088â12 103, 2022.

[14] A. Shamsoshoara et al., âDistributed cooperative spectrum sharing in UAV networks using multi-agent reinforcement learning,â in Proc. 16th IEEE Annu. Consum. Commun. Netw. Conf., 2019, pp. 1â6.

[15] R. Duan, J. Wang, C. Jiang, H. Yao, Y. Ren, and Y. Qian, âResource allocation for multi-UAV aided IoT NOMA uplink transmission systems,â IEEE Internet Things J., vol. 6, no. 4, pp. 7025â7037, Aug. 2019.

[16] J. Cui, Y. Liu, and A. Nallanathan, âMulti-agent reinforcement learningbased resource allocation for UAV networks,â IEEE Trans. Wireless Commun., vol. 19, no. 2, pp. 729â743, Feb. 2020.

[17] F. B. Sorbelli et al., âOptimal and heuristic algorithms for data collection by using an energy-and storage-constrained drone,â in Proc. Int. Symp. Algorithms Exp. Wireless Sensor Netw., 2022, pp. 18â30.

[18] A. Pratap, âCyclic stable matching inspired resource provisioning for IoT-enabled 5G networks,â IEEE Trans. Veh. Technol., vol. 71, no. 11, pp. 12195â12205, Nov. 2022.

[19] X. Wang and L. Duan, âEconomic analysis of unmanned aerial vehicle (UAV) provided mobile services,â IEEE Trans. Mobile Comput., vol. 20, no. 5, pp. 1804â1816, May 2021.

[20] M. B. Singh, H. Singh, and A. Pratap, âStable matching based revenue maximization for federated learning in UAV-assisted WBANs,â IEEE Trans. Serv. Comput., vol. 17, no. 4, pp. 1835â1846, Jul./Aug. 2024.

[21] Y. Li, Z. Wang, D. Jin, and S. Chen, âOptimal mobile content downloading in device-to-device communication underlaying cellular networks,â IEEE Trans. Wireless Commun., vol. 13, no. 7, pp. 3596â3608, Jul. 2014.

[22] X. Xi, X. Cao, P. Yang, J. Chen, T. Q. S. Quek, and D. Wu, âNetwork resource allocation for eMBB payload and URLLC control information communication multiplexing in a multi-UAV relay network,â IEEE Trans. Commun., vol. 69, no. 3, pp. 1802â1817, Mar. 2021.

[23] Z. Lu, T. Bansal, and P. Sinha, âAchieving user-level fairness in open-access femtocell-based architecture,â IEEE Trans. Mobile Comput., vol. 12, no. 10, pp. 1943â1954, Oct. 2013.

[24] W. Y. B. Lim et al., âTowards federated learning in UAV-enabled internet of vehicles: A multi-dimensional contract-matching approach,â IEEE Trans. Intell. Transp. Syst., vol. 22, no. 8, pp. 5140â5154, Aug. 2021.

[25] Y. Gu, Z. Chang, M. Pan, L. Song, and Z. Han, âJoint radio and computational resource allocation in IoT fog computing,â IEEE Trans. Veh. Technol., vol. 67, no. 8, pp. 7475â7484, Aug. 2018.

[26] H. Liu, S. Long, Z. Li, Y. Fu, Y. Zuo, and X. Zhang, âRevenue maximizing online service function chain deployment in multi-tier computing network,â IEEE Trans. Parallel Distrib. Syst., vol. 34, no. 3, pp. 781â796, Mar. 2023.

[27] D. S. Johnson, M. Yannakakis, and C. H. Papadimitriou, âOn generating all maximal independent sets,â Inf. Process. Lett., vol. 27, no. 3, pp. 119â123, 1988.

[28] M. Sun, X. Xu, X. Qin, and P. Zhang, âAoI-energy-aware UAV-assisted data collection for IoT networks: A deep reinforcement learning method,â IEEE Internet Things J., vol. 8, no. 24, pp. 17275â17289, Dec. 2021.

[29] O. S. Oubbati, M. Atiquzzaman, H. Lim, A. Rachedi, and A. Lakas, âSynchronizing UAV teams for timely data collection and energy transfer by deep reinforcement learning,â IEEE Trans. Veh. Tech., vol. 71, no. 6, pp. 6682â6697, Jun. 2022.

[30] Y. Wang, W. Feng, J. Wang, and T. Q. Quek, âHybrid satellite-UAVterrestrial networks for 6G ubiquitous coverage: A maritime communications perspective,â IEEE J. Sel. Areas Commun., vol. 39, no. 11, pp. 3475â3490, Nov. 2021.

[31] S. A. Hoseini, A. Bokani, J. Hassan, S. Salehi, and S. S. Kanhere, âEnergy and service-priority aware trajectory design for UAV-BSS using double Q-learning,â in Proc. IEEE 18th Annu. Consum. Commun. Netw. Conf., 2021, pp. 1â4.

[32] Z. Lv, J. Hao, and Y. Guo, âEnergy minimization for MEC-enabled cellular-connected UAV: Trajectory optimization and resource scheduling,â in Proc. IEEE Conf. Comput. Commun. Workshops, 2020, pp. 478â483.

[33] T.-H. Nguyen, T. P. Truong, A.-T. Tran, N.-N. Dao, L. Park, and S. Cho, âIntelligent heterogeneous aerial edge computing for advanced 5G access,â IEEE Trans. Netw. Sci. Eng., vol. 11, no. 4, pp. 3398â3411, Jul./Aug. 2024.

[34] M. Sipper, âA serial complexity measure of neural networks,â in Proc. IEEE Int. Conf. Neural Net, 1993, pp. 962â966.

<!-- image-->  
Shilpi Kumari (Graduate Student Member, IEEE) received the MTech degree from the School of Computer and Systems Sciences, Jawaharlal Nehru University, New Delhi, India, in 2021. She is currently working toward PhD degree in computer science and engineering, Indian Institute of Technology (BHU) Varanasi, India. Her current research interests include 5G/6 G and Reinforcement Learning.

<!-- image-->

Ajay Pratap (Senior Member, IEEE) is an assistant professor with the Department of Computer Science and Engineering, Indian Institute of Technology (BHU) Varanasi, India. He was a postdoctoral research fellow in the Department of Computer Science at Missouri University of Science and Technology, USA, from 2018 to 2019. His research interests include cyber-physical Systems, IoT-enabled smart environments, healthcare, statistical learning, and AI/ML for next-G cellular networks. He has received several awards, including the IEI Young

Engineer Award from the Institute of Engineers (India) and the Best Paper Award with the IEEE SmartComp conference in the USA.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring/page_3_img_1.jpeg|page_3_img_1]]
2. [[../extracted_images/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring/page_6_img_1.jpeg|page_6_img_1]]
3. [[../extracted_images/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring/page_10_img_1.png|page_10_img_1]]
4. [[../extracted_images/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring/page_12_img_1.jpeg|page_12_img_1]]
5. [[../extracted_images/Maximizing_Service_Providers_Profit_in_Multi-UAV_5G_Network_Via_Deep_Reinforcement_Learning_and_Graph_Coloring/page_12_img_2.jpeg|page_12_img_2]]

---

