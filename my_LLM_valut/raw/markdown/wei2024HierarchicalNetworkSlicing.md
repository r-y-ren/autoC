# Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization

Fengsheng Wei , Member, IEEE, Gang Feng , Senior Member, IEEE, Shuang Qin , Senior Member, IEEE, Youkun Peng , and Yijing Liu , Member, IEEE

Abstractâ Unmanned aerial vehicle (UAV) has been recognized as a key supplement for terrestrial networks to meet the stringent requirements of the forthcoming 6G networks. However, a significant challenge lies in providing differentiated services through a common UAV network, without the need to deploy individual networks for each service type. In this paper, we consider the problem of joint network slicing and UAV deployment under dynamic wireless environments as well as the uncertain traffic demands. To overcome the challenges posed by the network dynamics, we propose an intelligent hierarchical UAV slicing framework that operates at two different time-scales. At the large time-scale, the problem of inter-slice resource slicing and UAV deployment is formulated as a mixed integer nonlinear program, and a decomposition technique is applied to resolve it. At the small time-scale, the problem of intra-slice resource adjustment is modeled as a stochastic game and a distributed learning algorithm is proposed to find its Nash Equilibrium. Simulation results demonstrate that the proposed framework is lightweight and outperforms a number of known benchmark algorithms in terms of system utility, throughput and transmission delay.

Index Termsâ UAV assisted wireless networks, network slicing, decomposition technique, distributed learning.

## I. INTRODUCTION

HE 6G network is envisaged to build a data-driven society featured by seamless connectivity, ubiquitous intelligence, green communication, and autonomous systems. Specifically, it intends to support a variety of differentiated services with a peak data rate of Tbps level, reliability of 99.99999%, connection density of 100 million devices/km3, user-plane latency of 0.1ms, etc [1]. Meeting these stringent and diversified requirements by pre-deployed fixed infrastructure will be insufficient and costly. Thus, space-air-ground integrated networks (SAGINs) have been proposed as a promising paradigm shift, capable of providing ubiquitous on-demand and cost-effective wireless connections [2]. Particularly, unmanned aerial vehicles (UAVs)-assisted wireless network (UAWN) exploits UAVs to enhance the terrestrial network, which transforms the fixed 2D network into a flexible 3D network where UAVs serve as aerial base stations [3], [4]. Leveraging on the salient features of UAVs such as adjustable altitude, flexible deployment, agile relaying, fast data collection, and low cost, UAWNs are capable of providing additional capacity to hot-spots and extending the network to hard-to-reach areas [5].

Since different services may have unique requirements and specifications, it is impractical to expect a single UAWN to accommodate all services without the necessity of deploying individual networks for each service type [6]. With the aid of network slicing, the need to deploy individual UAV networks for each type of service can be avoided, thus the number of UAVs can be significantly reduced. Particularly, by exploiting technologies such as network function virtualization (NFV) and software-defined networking (SDN) that enable network slicing, a UAV can be sliced into multiple virtual UAVs, each of which can be customized to support a specific type of service [7]. In UAV slicing, one of the major challenges lies in how to jointly optimize resource allocations and UAV deployment, while accommodating to the dynamic wireless environment as well as the uncertain user demands. Recently, a number of UAV slicing schemes have been proposed, wherein machine learning (ML) is widely exploited to cope with the dynamics of the wireless networks and the time-varying traffic demand [6], [8], [9]. However, the training of these ML models is computationally demanding, necessitating substantial computing and power resources which are insufficiently available in UAVs. To cope with these challenges, a lightweight dynamic UAV slicing scheme becomes crucial.

In this paper, we propose an intelligent hierarchical network slicing framework for UAWNs, which jointly optimizes the resource slicing and the UAVâs altitude. The proposed framework is composed of a large time-scale resource slicing scheme and a small time-scale slice adjustment scheme. At the large time-scale, the resource slicing scheme is proposed to allocate virtual resources with coarse granularity. We model the large time-scale resource slicing problem (RSP) as a mixed integer nonlinear program (MINLP). Based on the problem structure, we propose a decomposition technique to transform the challenging MINLP into simpler sub-problems, which are solved in pseudo-polynomial time by using dynamic programming. After the virtual resources are allocated, a fully distributed slice adjustment scheme is designed to allocate the corresponding physical resources according to the ever-changing environment at the small time-scale. In particular, we formulate the small time-scale slice adjustment problem (SAP) as a stochastic game to capture the dynamic network conditions. Furthermore, we prove that the game has at least one pure-strategy Nash equilibrium (NE). Thereafter, a lightweight distributed learning algorithm is proposed to find a pure-strategy NE of the game.

The main contributions of this work are summarized as follows:

â¢ A two time-scale dynamic network slicing framework for UAWN is proposed to make adaptive control at different granularity, which not only can avoid frequent slice reconfiguration but also can maximize the resource utilization in dynamic environments.

â¢ We formulate the large time-scale resource slicing problem as a MINLP, which is NP-hard. Based on the decomposition technique and the structure of the problem, we propose a pseudo-polynomial algorithm to find its optimal solution.

â¢ We propose a stochastic game to capture the dynamics of the UAWN and the uncertainty of user demands. Based on the theory of potential game and distributed learning, a fully distributed scheme is devised to find the NE of the stochastic game.

â¢ As an important theoretical contribution of this paper, we have proved that for every finite ordinal potential game, linear reward inaction (LRI)-based learning automata (LA) converges to an NE. Thereby the application scope of LRI-based LA has been extensively expanded.

The remainder of this paper is organized as follows. Section II reviews the related work on network slicing for UAWN. In Section III, we formulate the RSP and elaborate its solution. In Section IV, we formulate the game model of SAP and solve it by exploiting distributed learning. In Section V, numerical simulations are conducted to verify the effectiveness of the proposed UAV network slicing framework. Finally, we conclude the paper in Section VI. For ease of reference, we list the key abbreviations in Table I.

## II. RELATED WORK

In this section, we overview the investigations on UAWN network slicing that are related to our work.

## A. Network Slicing for Terrestrial Networks

There are plenty of pioneer investigations that focus on slicing the terrestrial networks. Intrinsically, network slicing is a hierarchical allocation problem that involves resource slicing at multiple levels, including the network-level, gNodeB-level and packet scheduling level. Thus, it is natural to model the network slicing problem as a multi-level optimization problem [10], [11], [12]. In [10], the authors proposed a self-leaning framework to achieve adaptive radio access network (RAN) slicing under unforeseen network conditions. Similarly, the authors of [11] proposed a hierarchical slicing framework that consists of the large time-scale gNodeB pre-allocation and the small time-scale resource adaption to accommodate the time-varying traffic. The authors of [12] proposed a two-level RAN slicing strategy, where the upper-level performs slice configuration at a coarse granularity, while the lower-level controller schedules the resource block (RB) and power allocation at a fine granularity. They modeled the problem as a multi time-scale Markov decision process (MDP) and resolved it by proposing a hierarchical deep reinforcement learning (DRL) framework which jointly exploits DDPG and double-DQN.

TABLE I  
LIST OF KEY ABBREVIATIONS
<table><tr><td>Abbr.</td><td>Definition</td></tr><tr><td>DP</td><td>Demand Point</td></tr><tr><td>FDLA</td><td>Fully Distributed Learning Algorithm</td></tr><tr><td>GA</td><td>Genetic Algorithm</td></tr><tr><td>GAC GAT</td><td>Genetic Algorithm Centralized</td></tr><tr><td>ILP</td><td>Graph Attention Network</td></tr><tr><td>LA</td><td>Integer Linear Program Learning Automata</td></tr><tr><td>LRI</td><td>Linear Reward Inaction</td></tr><tr><td>LTRSA</td><td>Large Time-Scale Resource Slicing Algorithm</td></tr><tr><td>MARL</td><td>Multi-Agent Reinforcement Learning</td></tr><tr><td>MINLP</td><td>Mixed Integer Nonlinear Program</td></tr><tr><td>MP</td><td>Master Problem</td></tr><tr><td>NE</td><td>Nash Equilibrium</td></tr><tr><td>ODE</td><td>Ordinary Differential Equation</td></tr><tr><td>PPAD</td><td>Polynomial Parity Arguments on Directed graphs</td></tr><tr><td>RAN</td><td>Radio Access Network</td></tr><tr><td>RSP</td><td>Resource Slicing Problem</td></tr><tr><td>RSS</td><td>Random Strategy Selection</td></tr><tr><td>SAGVN</td><td>Space-Air-Ground integrated Vehicular Network</td></tr><tr><td>SAP</td><td>Slice Adjustment Problem</td></tr><tr><td>SLA</td><td>Service Level Agreement</td></tr><tr><td>SP</td><td>Sub-Problem</td></tr><tr><td>TTI</td><td>Transmission Time Interval</td></tr><tr><td>UAWN</td><td>UAV-Assisted Wireless Network</td></tr><tr><td></td><td></td></tr><tr><td>UKP</td><td>Unbounded Knapsack Problem</td></tr></table>

Since the slicing of RAN involves multiple tenants, it is straightforward to model the problem as a multi-agent system that learns to adapt to the ever-changing networks [13], [14], [15]. However, one of the most important issues in multi-agent reinforcement learning (MARL) as well as DRL is to address the curse of dimensionality caused by the large action spaces [16]. A number of attempts have shown great success in overcoming this issue when MARL is exploited in RAN slicing. In [13], the authors considered dense networks with moving subscribers in which each base station (BS) is regarded as an agent. They proposed a MARL algorithm that combines graph attention network (GAT) with DRL to learn resource management strategies. In [15], the authors proposed a MARL method for RAN slicing, where each slice is modeled as a competitive agent that competes for RB resources through correlated Q-learning.

## B. Network Slicing for Non-Terrestrial Networks

In contrast to terrestrial networks, there is very limited work focuses on the slicing of non-terrestrial networks. The authors of [17] proposed an automatic network slicing framework for non-terrestrial networks, which addresses route computation and resource allocation with minimal SLA violations. The authors of [18] proposed a slicing-based task offloading framework for the space-air-ground integrated vehicular network (SAGVN), where a paradigm of optimization-with-learning is exploited to address the joint network slicing and task offloading problem. In [19], the problem of slice admission, UAV dispatching and resource slicing are jointly considered, and a Lyapunov-based optimization framework is proposed for the SAGVN. Similarly, the authors of [6] also proposed a Lyapunov-based network slicing framework for UAWN. With the aim of enhancing the system performance, they employ distributed learning and deep neural networks (DNNs) to respectively predict the user location and the channel model. An RL-based joint network slicing and computation offloading scheme for UAWN is presented in [9]. However, the proposed solution is centralized and computation-intensive, which may place a considerable burden on the resource-limited UAV.

The above existing solutions are insufficient for various reasons. First, optimization and game theoretic-based methods are only suitable for the static or quasi-static environment. In dynamic networks such as UAWNs, these mechanisms need to be executed periodically by a central controller to accommodate the network dynamics. Second, the training of DRL and MARL agents requires numerous agent-environment interactions, which leads to extensive signaling overhead before convergence. Moreover, the training also requires substantial computation and power resources, which are generally unavailable for the UAV. In addition, stochastic arrivals/departures of network slices and the User Equipments (UEs) will change the dimensions of both state and action spaces, resulting in the socalled open multi-agent system that is intractable by existing learning-based methods [20]. By combining large time-scale optimization with small time-scale distributed learning, our solution can overcome these challenges efficiently.

## III. LARGE TIME-SCALE RESOURCE SLICING PROBLEM A. System Model

1) Network Model: As shown in Fig. 1, we consider a typical uplink UAWN which is composed of the terrestrial network and the aerial network, upon which a set of I heterogeneous network slices will be deployed. We denote the set of network slices by $\mathcal { T } = \{ 1 , \cdots , I \}$ . In the terrestrial network, a number of UEs are served by a BS, which provides elementary services for the UEs. In the aerial network, a UAV acts as an airborne BS is deployed as a supplement to the ground BS. We assume that the wireless resources reserved for the terrestrial and aerial networks do not overlap, and their available bandwidths are denoted by $W ^ { U }$ and $W ^ { B }$ respectively. In this paper, we aim to design a holistic framework that efficiently allocates resources within the UAWN to meet the heterogeneous QoS requirements of UEs across each slice under dynamic network conditions.

<!-- image-->  
Fig. 1. System model and the timing of the proposed network slicing framework.

In UAWNs, resource scheduling should be frequently executed to match the network dynamics caused by UAV flight, network failures, user mobility, channel fading, etc. As a consequence, the incurred signaling and computing overhead will be substantial, which will easily drain the battery of the UAV. To address this issue, we categorize the dynamics of the UAWN into two distinct time-scales, and design corresponding algorithms tailored for them. At large time-scale, joint UAV deployment and inter-slice resource allocation are performed to adapt to network dynamics caused by UAV flight, sudden network failure, traffic burst, etc. Then real-time resource adjustment will be executed at small time-scale, whereby the sub-channels are allocated to UEs to adapt to small-scale channel fading, user movement, and the time-varying demand. Such a synergy of large and small time-scale operations allows for a reduction in the frequency of resource scheduling, while ensuring that the resource provisioning meets the ever-changing network conditions.

As illustrated in Fig. 1, our proposed solution is a slotted framework that is operated at two different time-scales. At the large time-scale, resource slicing is executed over timeslots (e.g., minute level) indexed by $\mathcal { T } = \{ 1 , 2 , \cdots , \mathrm  { T } \}$ , each of which is composed of $T _ { s }$ consecutive minislots (e.g., second level). A minislot corresponds to a basic scheduling interval for conducting fine-grained time-scale adjustment within each slice. At the beginning of each timeslot, the virtual radio resources are coarsely allocated to each network slice according to their historical quality of service (QoS) requirements. Note that the large time-scale operations can also be triggered by unexpected events, such as sudden spikes in demand or network failures, thus to avoid the imbalance between resource supply and demand in the event of significant fluctuations of network conditions. Thereafter, small time-scale slice adjustments will be performed at each minislots to allocate sub-channels to each UE. In this section, we focus on solving RSP. SAP will be elaborated in Section IV.

TABLE II
<table><tr><td colspan="2">SUMMARYOFMAINNOTATIONS</td></tr><tr><td>Notation</td><td>Description</td></tr><tr><td> $\mathcal { T }$ </td><td>Sets</td></tr><tr><td> $\mathcal { D } _ { i }$ </td><td>The set of network slices</td></tr><tr><td> $\mathcal { M } _ { j } ^ { i }$ </td><td>The set of DPs belonging to slice i The set of UEs belonging to DP  $d _ { j } ^ { i }$ </td></tr><tr><td> $d _ { i } ^ { i }$ </td><td>Parameters  $\mathcal { D } _ { i }$ </td></tr><tr><td> $W ^ { U } , W ^ { B }$ </td><td>The j-th DP in Available bandwidth of the aerial and terres- trial networks,respectively</td></tr><tr><td> $W _ { i } ^ { U } , W _ { i } ^ { B }$ </td><td>Sub-channel bandwidth of slice i for aerial and terrestrial networks,respectively</td></tr><tr><td> $p _ { j } ^ { i , U } , p _ { j } ^ { i , B }$ </td><td>Transmission power of DP  $d _ { j } ^ { i }$  to the UAV and the BS,respectively</td></tr><tr><td> $p ^ { \mathrm { m o v } } , p ^ { \mathrm { h o v } }$ </td><td>Power consumption of the UAV in flying and hovering mode,respectively</td></tr><tr><td> $\phi ^ { U } , \phi ^ { B } , \phi _ { j } ^ { i }$ </td><td>2D vectors that represent the coordinates of the UAV, the BS,and DP  $d _ { j } ^ { i }$  ï¼respectively</td></tr><tr><td> $\tilde { R } _ { i } ^ { i }$   $\dot { E _ { s } } , T _ { s }$ </td><td>Data rate requested by DP  $d _ { j } ^ { i }$  Available energy of the UAV in each times-</td></tr><tr><td> $r _ { m } , \psi _ { m }$ </td><td>lot,and the duration of the timeslot The data rate and the delay of UE m, re- spectively</td></tr><tr><td> $q _ { m }$ </td><td>The traffic demand of UE m Variables</td></tr><tr><td> $\mathbf { x } ^ { i } , \mathbf { y } ^ { i }$ </td><td>Slicing strategies of slice i for aerial and</td></tr><tr><td> $h$ </td><td>terrestrial networks,respectively Altitudeof theUAV</td></tr><tr><td> $\mathbf { a } _ { m }$ </td><td>Strategy of UE m</td></tr><tr><td> $\mathbf { a } _ { - m }$ </td><td>Partial strategy profle of all UEs within a</td></tr><tr><td></td><td>DP, except UE m</td></tr></table>

In the considered UAWN, the UEs are geographically partitioned into clusters. Within each cluster, the UEs served by the same slice are abstracted to a demand point (DP) belonging to that slice [21]. Without loss of generality, we consider the case where each UE is subscribed only to one slice. In each timeslot, the set of UEs constituting a DP does not change, but may vary between consecutive timeslots. Let $D _ { i }$ denote the number of DPs in slice i. Thus, the set of DPs in slice i can be represented by $\mathcal { D } _ { i } = \{ d _ { 1 } ^ { i } , \cdot \cdot \cdot , d _ { D _ { i } } ^ { i } \}$ . We assume that DP $d _ { i } ^ { i }$ is composed of $M _ { j } ^ { i }$ UEs, which is represented by the set $\mathcal { M } _ { j } ^ { i }$ . In RSP, we allocate radio resources to DPs rather than directly to UEs, since large time-scale resource slicing only provides coarse-grained control. For DP $d _ { j } ^ { i }$ , its traffic demand at the current timeslot, denoted by $\tilde { R } _ { i } ^ { i }$ , can be evaluated by some prediction mechanism based on the historical demands of all UEs within the DP [7].

For service differentiation and QoS provisioning, we exploit the multi-numerology technology [22] in our framework. In multi-numerology, radio resources are not partitioned into rigid structures in the time and frequency domain, but are flexibly configured according to the QoS requirements of each network slice. In particular, the available spectrum of the UAWN will be partitioned into a number of independent flat-fading sub-channels, each of which is composed of contiguous RBs having the same numerology scheme. For slice i, we assume that the sub-channel bandwidths of its aerial and the terrestrial network are $W _ { i } ^ { U }$ MHz and $W _ { i } ^ { B }$ , respectively. Therefore, the slicing strategy of slice i can be represented by $\mathbf { x } ^ { i } = ( x _ { 1 } ^ { i } , \cdot \cdot \cdot , x _ { D _ { i } } ^ { i } )$ and $\mathbf { y } ^ { i } = ( y _ { 1 } ^ { i } , \cdot \cdot \cdot , y _ { D _ { i } } ^ { i } )$ , which are the slicing strategies of the aerial and the terrestrial networks respectively. In particular, $\boldsymbol { x } _ { j } ^ { i }$ and $y _ { j } ^ { i }$ are non-negative integer variables that represent the number of sub-channels allocated to DP $d _ { i } ^ { i }$ by the UAV and the terrestrial BS, respectively.

2) Aerial Network Slicing: We use Î¸ to represent the antenna beamwidth of the UAV. Let h be the UAVâs altitude in the current timeslot. Then the UAV must satisfy the following coverage constraint:

$$
h \tan \theta \geq \Omega ,\tag{1}
$$

where â¦ is the radius of the UAWN. We use c to denote the UAVâs flying speed. To ensure that the UAV can fly to the next location within a timeslot, we have

$$
\begin{array} { r } { \tau = \left| h - \hat { h } \right| / c \leq T _ { s } , } \end{array}\tag{2}
$$

where $\hat { h }$ is the height of the UAV at the previous timeslot. Let $\phi _ { i } ^ { i } = ( l _ { i } ^ { i , 1 } , l _ { i } ^ { i , 2 } )$ denote the geographic center of DP $d _ { j } ^ { i } ,$ and let $\phi ^ { U } = ( l ^ { U , 1 } , l ^ { U , 2 } )$ denote the coordinate of the UAV projected on the ground. The channel gain between the UAV and DP $d _ { j } ^ { i }$ will be

$$
g ( h ) = \frac { g _ { 0 } \tilde { g } _ { j } ^ { i , U } } { \theta ^ { 2 } ( \eta _ { j } ^ { i } + h ^ { 2 } ) ^ { \alpha / 2 } } ,\tag{3}
$$

where $g _ { 0 }$ is the channel power gain at a reference distance of 1 m; $\tilde { g } _ { j } ^ { i , \tilde { U } }$ represents the Rician distributed small-scale fading; Î± is the path-loss exponent [23]; $\eta _ { j } ^ { i } = \left\| \phi _ { j } ^ { i } - \phi ^ { U } \right\| ^ { 2 }$ is the squared horizontal distance between the UAV and DP $d _ { i } ^ { i }$

In the aerial network, the transmission power of each UE in the same DP $d _ { j } ^ { i }$ is assumed to be identical and represented by $p _ { j } ^ { i , U }$ . This is reasonable since for one thing, the services requested by the UEs within a common slice are usually homogeneous. For another, since the geographical locations of the UEs in the same DP are adjacent, their wireless environments are similar such that they tend to transmit at the same power level. As such, the average uplink rate from DP $d _ { j } ^ { i }$ to the UAV is

$$
R _ { j } ^ { i , U } ( \mathbf { x } , z ) = x _ { j } ^ { i } W _ { i } ^ { U } \log \left( 1 + \frac { g _ { 0 } \tilde { g } _ { j } ^ { i , U } p _ { j } ^ { i , U } } { \sigma _ { 0 } ^ { 2 } \theta ^ { 2 } ( \eta _ { j } ^ { i } + h ^ { 2 } ) ^ { \alpha / 2 } } \right) ,\tag{4}
$$

where $\sigma _ { 0 } ^ { 2 }$ is the power of background noise.

3) Terrestrial Network Slicing: Similar to the aerial network, we assume that the transmission power of the UEs in the same DP is identical, which is denoted by $p _ { j } ^ { i , B }$ . Let $\phi ^ { B } = ( l ^ { B , 1 } , l ^ { B , 2 } )$ denote the location of the terrestrial BS. Then the achievable uplink rate from DP $d _ { j } ^ { i }$ to the BS is

$$
R _ { j } ^ { i , B } ( { \bf y } ) = y _ { j } ^ { i } W _ { i } ^ { B } \log \left( 1 + \frac { g _ { 0 } \tilde { g } _ { j } ^ { i , B } p _ { j } ^ { i , B } } { \sigma _ { 0 } ^ { 2 } \left\| \phi ^ { B } - \phi _ { j } ^ { i } \right\| ^ { \alpha } } \right) ,\tag{5}
$$

where $\tilde { g } _ { j } ^ { i , B }$ represents the Rician distributed small scale fading.

## B. Formulation of RSP

At the large time-scale, we aim to decide the optimal network slicing strategies x and y, as well as the optimal altitude h of the UAV. The objective is to maximize the total transmission rate with proportional fairness for each DP. Thus, RSP can be formulated as

$$
( R S P : ) \operatorname* { m a x } _ { { \bf x } , { \bf y } , h } \sum _ { i \in \mathcal { I } } \sum _ { j \in \mathcal { D } _ { i } } ( R _ { j } ^ { i , U } ( { \bf x } , h ) + R _ { j } ^ { i , B } ( { \bf y } ) ) / \tilde { R } _ { j } ^ { i } ,\tag{6}
$$

$$
s . t . \ ( 1 ) - ( 2 ) ,\tag{6.1}
$$

$$
\sum _ { i \in \mathcal { T } } \sum _ { j \in \mathcal { D } _ { i } } x _ { j } ^ { i } W _ { i } ^ { U } \leq W ^ { U } ,\tag{6.2}
$$

$$
\sum _ { i \in \mathcal { T } } \sum _ { j \in \mathcal { D } _ { i } } y _ { j } ^ { i } W _ { i } ^ { B } \leq W ^ { B } ,\tag{6.3}
$$

$$
h _ { \operatorname* { m i n } } \leq h \leq h _ { \operatorname* { m a x } } ,\tag{6.4}
$$

$$
p ^ { \mathrm { m o v } } \tau + \left( \sum _ { i \in \mathbb { Z } } \sum _ { j \in \mathcal { D } _ { i } } x _ { j } ^ { i } p _ { j } ^ { i , U } + p ^ { \mathrm { h o v } } \right) ( T _ { s } - \tau ) \leq E _ { s } ,\tag{6.5}
$$

$$
x _ { j } ^ { i } , y _ { j } ^ { i } \in \mathbb { N } , \forall j \in \mathcal { D } _ { i } , \forall i \in \mathcal { I } ,\tag{6.6}
$$

where $\tilde { R } _ { j } ^ { i }$ is the requested data rate of DP $d _ { j } ^ { i }$ ; N is the set of non-negative integers. In RSP, constraints (6.2) and (6.3) state that the allocated bandwidth cannot exceed the available bandwidth of the aerial and the terrestrial network, respectively. Constraint (6.4) guarantees that the altitude of the UAV is lower-bounded by $h _ { \mathrm { m i n } }$ to avoid collision with obstacles on the ground, and is upper-bounded by $h _ { \mathrm { m a x } }$ which is the maximum allowable flying altitude of the UAV. Constraint (6.5) constrains that the energy consumed in each timeslot can not exceed $E _ { s }$ , which is the maximum available energy of the UAV for each timeslot. In (6.5), $p ^ { \mathrm { m o v } }$ and $p ^ { \mathrm { h o v } }$ are the power consumption of the UAV in flying and hovering modes, respectively. Constraint (6.6) is the integrality constraints on the decision variables x and y.

It should be noted that the parameters of RSP explicitly satisfy the following relationship:

$$
E _ { s } / T _ { s } \geq p ^ { \mathrm { m o v } } + p ^ { \mathrm { h o v } } + \sum _ { i , j } x _ { j } ^ { i } p _ { j } ^ { i , U } .\tag{7}
$$

In other words, the power consumed by the UAV should not exceed its available power in each timeslot.

RSP is a challenging MINLP due to the nonlinear nature of the objective and constraint (6.5) and the presence of mixed integer variables. Moreover, even if we have relaxed the integer variables, RSP is still hard to address since its objective function is non-convex. Generally, MINLP is NP-hard and cannot be solved in polynomial time unless P=NP. In what follows, we propose a decomposition technique to facilitate RSP, such that a pseudo-polynomial algorithm can be readily devised.

## C. Decomposition Technique for RSP

In this subsection, we will address RSP by exploiting a decomposition technique. The heart of this technique is the operation of projection, sometimes also known as partitioning [24]. Based on projection, we have devised a Benders-like decomposition method to address RSP, which is named the large time-scale resource slicing algorithm (LTRSA). The solution strategy of LTRSA is illustrated in Fig. 2.

<!-- image-->  
Fig. 2. Solution strategy of the proposed algorithm for the large time-scale problem.

1) Projection Onto the (x, y)-Axis: By projection, we mean to project both the objective function and the feasible set of RSP onto the (x, y)-axis. The projection of RSP onto the (x, y)-axis is given by

$$
( M P : ) \operatorname* { m a x } _ { \mathbf { x } \in X , \mathbf { y } \in Y } v ( \pmb { x } , \pmb { y } ) ,\tag{8}
$$

$$
s . t . ( \mathbf { x } , \mathbf { y } ) \in V ,\tag{9}
$$

where $X \ : = \ \{ x _ { i } ^ { i } \ \in \ \mathbb { N } | .$ x satisfies (6.2)}, $Y \ : = \ \{ y _ { j } ^ { i } \in \quad$ N|y satisfies $( 6 . 3 ) \check  \}$ , and

$$
V = \{ { \bf x } | { \bf x } \ \mathrm { s a t i s f i e s } \ ( 6 . 5 ) \ \mathrm { f o r \ s o m e } \ h \in H \} ,\tag{10}
$$

in which $H : = \{ h | h$ satisfies (1), (2), and (6.4) }. In (8), $v ( { \pmb x } , { \pmb y } )$ is defined as

$$
( S P : ) \ v ( { \pmb x } , { \pmb y } ) = \operatorname* { s u p } _ { h } \sum _ { i , j } \left( R _ { j } ^ { i , U } ( { \bf x } , h ) + R _ { j } ^ { i , B } ( { \bf y } ) \right) / \tilde { R } _ { j } ^ { i } ,
$$

$$
s . t . \ \bar { h } _ { \operatorname* { m i n } } \leq h \leq h _ { \operatorname* { m a x } } ,\tag{11}
$$

$$
p ^ { \mathrm { m o v } } \tau + p ( { \pmb x } ) ( T _ { s } - \tau ) \leq E _ { s } ,\tag{12}
$$

$$
| h - \hat { h } | \leq c T _ { s } ,\tag{13}
$$

(14)

in which $\bar { h } _ { \operatorname* { m i n } } = \operatorname* { m a x } \{ h _ { \operatorname* { m i n } } , \Omega / t a n \theta \}$ , and

$$
p ( { \bf x } ) = \sum _ { i , j } x _ { j } ^ { i } p _ { j } ^ { i , U } + p ^ { \mathrm { h o v } } .\tag{15}
$$

Namely, $p ( \mathbf { x } )$ is the total power consumed by the UAV for hovering and communication. For ease of analysis, we assume that

$$
| \bar { h } _ { \operatorname* { m i n } } - \hat { h } | \leq c T _ { s } ,\tag{16}
$$

which means that in each timeslot, the UAV can descend to the minimum altitude from its previous position. This assumption can generally be satisfied and is not restrictive, as we have the flexibility to increase $T _ { s }$ in order to avoid any potential violation of (16).

Problem (8) and problem (11) are the so-called master problem (MP) and the subproblem (SP) of RSP, respectively. Then we have the following lemma [24].

Lemma 1: RSP is equivalent to MP. That is:

$R S P$ is infeasible or its optimal value is unbounded if and only if the same is true for problem MP;

$H f \ \left( \mathbf { x } ^ { * } , \mathbf { y } ^ { * } , h ^ { * } \right)$ is the optimal solution of RSP, then $\left( \mathbf { x } ^ { * } , \mathbf { y } ^ { * } \right)$ must be optimal in problem MP;

$I f \left( \mathbf { x } ^ { * } , \mathbf { y } ^ { * } \right)$ is optimal in problem MP and $h ^ { * }$ achieves the supremum in SP with $( { \bf x } , { \bf y } ) = ( { \bf x } ^ { * } , { \bf y } ^ { * } )$ , then $\left( \mathbf { x } ^ { * } , \mathbf { y } ^ { * } , h ^ { * } \right)$ must be optimal in RSP.

Therefore, solving RSP is equivalent to solving MP, in which an SP should be solved for every pair of $\pmb { x } \in X , \pmb { y } \in Y$ However, in the case of a large scale UAWN, the number of combinations of the pair $( { \pmb x } , { \pmb y } )$ grows exponentially with the network scale, which leads to a substantial number of SPs. Furthermore, even if we can solve SP for every possible combinations of (x, y), MP is still unsolvable because the explicit expression of the set V is unknown.

2) Solution of the SP: Fortunately, a closed form of the solution to SP can be derived, which is independent of $( { \pmb x } , { \pmb y } )$ Indeed, for fixed $\pmb { x } \in X , \pmb { y } \in Y$ , the objective in (11) is reduced to

$$
\begin{array} { r } { f ( h ) : = \sum _ { i , j } A _ { j } ^ { i } \log \left( 1 + \frac { B _ { j } ^ { i } } { ( \eta _ { j } ^ { i } + h ^ { 2 } ) ^ { \alpha / 2 } } \right) , } \end{array}\tag{17}
$$

where $A _ { j } ^ { i } = x _ { j } ^ { i } W _ { i } ^ { U } / \tilde { R _ { j } ^ { i } }$ and $B _ { j } ^ { i } = { g _ { 0 } } \tilde { g } _ { j } ^ { i , U } p _ { j } ^ { i , U } / ( \sigma _ { 0 } ^ { 2 } \theta ^ { 2 } )$ , which are constants for fixed $( { \pmb x } , { \pmb y } )$ . Obviously, the objective of SP is a strictly decreasing function of h. Thus, the optimal solution $h ^ { * }$ of SP is the minimum value of its feasible set. In the following theorem, we will demonstrate that $h ^ { * } = \tilde { h } _ { \operatorname* { m i n } }$ , where

$$
\tilde { h } _ { \operatorname* { m i n } } : = \operatorname* { m a x } \{ \bar { h } _ { \operatorname* { m i n } } , \hat { h } - c T _ { s } \} .\tag{18}
$$

Theorem 1: For every fixed $\pmb { x } \in X , \pmb { y } \in Y ,$ , if the corresponding SP is feasible, then its optimal solution is $h ^ { * } = \tilde { h } _ { \operatorname* { m i n } } .$

Proof: First, it is seen that $\tilde { h } _ { \mathrm { m i n } }$ satisfies constraints (12) and (14). For constraint (13), we can transform it into

$$
| h - \hat { h } | \cdot ( p ^ { \mathrm { m o v } } - p ( { \pmb x } ) ) \leq c ( E _ { s } - T _ { s } p ( { \pmb x } ) ) .\tag{19}
$$

According to (7), we have

$$
\begin{array} { r } { E _ { s } \geq T _ { s } p ( \pmb { x } ) . } \end{array}\tag{20}
$$

For constraint (19), there are two possible cases as follows:

1) If $p ^ { \mathrm { m o v } } - p ( \mathbf { x } ) \leq 0 .$ , then $\tilde { h } _ { \mathrm { m i n } }$ satisfies constraint (13) automatically. Since $\ddot { h } _ { \operatorname* { m i n } }$ is the minimum value that satisfies constraints $( 1 2 ) \textrm { - } ( 1 4 )$ , therefore $h ^ { * } = \tilde { h } _ { \operatorname* { m i n } }$

2) Otherwise if $p ^ { \mathrm { m o v } } - p ( \mathbf { x } ) > 0$ , we will show that we also have $h ^ { * } = \tilde { h } _ { \operatorname* { m i n } }$ in what follows.

Since $p ^ { \mathrm { m o v } } - p ( \mathbf { x } ) > 0$ , constraint (19) is equivalent to

$$
\hat { h } - \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } \leq h \leq \hat { h } + \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } .\tag{21}
$$

Therefore, case b) can be further divided into the following two sub-cases:

$1 ) \ \hat { h } \ \le \ c ( E _ { s } - T _ { s } p ( { \pmb x } ) ) / ( p ^ { \mathrm { m o v } } - p ( { \pmb x } ) )$ . Since h must be positive, there must be $h ^ { * } = \ddot { h } _ { \operatorname* { m i n } }$

$2 ) \ \hat { h } \ > \ c ( E _ { s } - T _ { s } p ( { \pmb x } ) ) / ( p ^ { \mathrm { m o v } } - p ( { \pmb x } ) )$ . In this sub-case, we have:

$$
h ^ { \ast } = \operatorname* { m a x } \left\{ \tilde { h } _ { \mathrm { m i n } } , \hat { h } - \frac { c ( E _ { s } - T _ { s } p ( { \pmb x } ) ) } { p ^ { \mathrm { m o v } } - p ( { \pmb x } ) } \right\} .\tag{22}
$$

According to the meaning of the max operator in the above equation, we get the following condition:

$$
\begin{array} { r l } & { h ^ { * } > \tilde { h } _ { \mathrm { m i n } } \iff \hat { h } > \frac { c ( E _ { s } - T _ { s } p ( \pmb { x } ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb { x } ) } , } \\ & { \mathrm { a n d ~ } \hat { h } - \frac { c ( E _ { s } - T _ { s } p ( \pmb { x } ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb { x } ) } > \tilde { h } _ { \mathrm { m i n } } . } \end{array}\tag{23}
$$

After some transformation, the above conditions can be equivalently simplified to:

$$
h ^ { \ast } > \tilde { h } _ { \operatorname* { m i n } } \iff \frac { \hat { h } - \tilde { h } _ { \operatorname* { m i n } } } { c T _ { s } } - 1 > \frac { E _ { s } / T _ { s } - p ^ { \mathrm { m o v } } } { p ^ { \mathrm { m o v } } - p ( { \pmb x } ) } .\tag{24}
$$

Since $\hat { h } { - } \tilde { h } _ { \operatorname* { m i n } } \leq c T _ { s }$ (cf. (18)) and $E _ { s } / T _ { s } - p ^ { \mathrm { m o v } } > 0$ (cf. (7)), the right-hand-side of condition (24) will never be satisfied. Thus, $h ^ { * } = \tilde { h } _ { \operatorname* { m i n } }$ â¡

Theorem 2: If RSP is feasible, then the set V is equivalent to

$$
V ^ { \prime } = \{ { \bf x } | { \bf x \ } s a t i s f i e s ~ ( 6 . 5 ) ~ f o r ~ h = h ^ { * } \} .\tag{25}
$$

Proof: First, it is obvious that $V ^ { \prime } \subseteq V$ . We prove $V \subseteq V ^ { \prime }$ as follows.

For any $\mathbf { x } \in V$ , according to the definition of V , there is $h _ { 0 } \in H$ such that x satisfies (6.5). Equivalently,

$$
\hat { h } - \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } \le h _ { 0 } \le \hat { h } + \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } .\tag{26}
$$

By Theorem $1 , h ^ { * }$ is the minimum value of $\mathrm { { S P } ^ { \prime } { s } }$ feasible set, we have

$$
\hat { h } - \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } \le h ^ { \ast } \le h _ { 0 } \le \hat { h } + \frac { c ( E _ { s } - T _ { s } p ( \pmb x ) ) } { p ^ { \mathrm { m o v } } - p ( \pmb x ) } .\tag{27}
$$

Thus, x satisfies (6.5) for $h ^ { * }$ as well, which indicates that $V \subseteq V ^ { \prime }$ . Therefore, $V = V ^ { \prime }$

3) Solution of the MP: According to the above theorems, the explicit form of $v ( { \pmb x } , { \pmb y } )$ can be obtained by substituting variable h in (8) and (10) with hâ. Thus, MP can be equivalently transformed into the following Integer Linear Program (ILP):

$$
( I L P : ) \operatorname* { m a x } _ { \substack { { \boldsymbol { x } } \in X , { \boldsymbol { y } } \in Y } } \sum _ { i , j } ( R _ { j } ^ { i , U } ( { \boldsymbol { \mathbf { x } } } , { \boldsymbol { h } } ^ { * } ) + R _ { j } ^ { i , B } ( { \boldsymbol { \mathbf { y } } } ) ) / { \tilde { R } _ { j } ^ { i } } ,\tag{28}
$$

$$
s . t . ~ x _ { j } ^ { i } , y _ { j } ^ { i } \in \mathbb { N } , \forall j \in \mathcal { D } _ { i } , \forall i \in \mathcal { I } .\tag{29}
$$

The above ILP is separable, which means that it can be decomposed into the following two independent unbounded knapsack problems (UKPs):

$$
( U K P 1 : ) \operatorname* { m a x } _ { \substack { x \in X \cap \mathbb { N } } } \sum _ { i , j } R _ { j } ^ { i , U } ( { \bf x } , h ^ { * } ) / \tilde { R } _ { j } ^ { i } ,\tag{30}
$$

and

$$
( U K P 2 : ) \operatorname* { m a x } _ { \pmb { y } \in Y \cap \mathbb { N } } \sum _ { i , j } R _ { j } ^ { i , B } ( \mathbf { y } ) / \tilde { R } _ { j } ^ { i } ,\tag{31}
$$

where X and Y can be seen as the set corresponding to the capacity constraints of these knapsack problems. For UKP1, $W _ { i } ^ { \bar { U } }$ corresponds to the weight of the item to be packed; $W _ { i } ^ { U }$ log $\left( 1 + ( g _ { 0 } \tilde { g } _ { j } ^ { i , U } p _ { j } ^ { i , U } ) / ( \sigma _ { 0 } ^ { 2 } \theta ^ { 2 } ( \eta _ { j } ^ { i } + ( h ^ { * } ) ^ { 2 } ) ^ { \alpha / 2 } ) \right)$ is the value of each item; $W ^ { U }$ is the capacity of the knapsack. UKP2 has a similar correspondence.

UKPs are NP-complete problems, which are unable to be addressed in polynomial time. Fortunately, UKPs fall in an easier problem set which can be solved by dynamic programming in pseudo-polynomial time $O ( n C )$ , where n and C are the number of items and the capacity of the knapsack respectively. In particular, by using dynamic programming, the time complexity of UKP1 and UKP2 will be $\begin{array} { r } { O \left( \sum _ { i \in \mathcal { T } } D _ { i } W ^ { U } \right) } \end{array}$ and $O \left( \sum _ { i \in \mathcal { T } } D _ { i } W ^ { B } \right)$ , respectively. Therefore, following the solution strategy illustrated in Fig. 2, a dynamic programming based algorithm named large time-scale resource slicing algorithm (LTRSA) can be readily devised. To save space, its pseudo-code is omitted.

## IV. SMALL TIME-SCALE SLICE ADAPTION PROBLEM

## A. Stochastic Game Model for SAP

In RSP, the resources are allocated coarsely since we assume that the channel gains are the same for the UEs in the same DP. However, this assumption no longer holds at the small time-scale, as the effects of stochastic channel fading, mobility of the UE and UAV, and the time-varying traffic cannot be ignored. In light of these effects, in SAP, our objective is to devise a real-time channel allocation scheme that allocates the sub-channels to each UE in such a dynamic environment. In addition, since the small-time-scale slice adaptation is performed among the UEs within individual DPs, we only need to consider SAP on a single DP. Moreover, as the UAV does not move within a timeslot, it can be treated similarly as the terrestrial BS, except that their channel gains are different. Therefore, in what follows, we focus on a specific DP $d _ { j } ^ { i }$ in slice i, whose UE set is $\mathcal { M } _ { j } ^ { i }$ . For ease of presentation, we omit the subscripts and superscripts to denote the UE set $\mathcal { M } _ { j } ^ { i }$ by $\mathcal { M } = \{ 1 , \cdots , M \}$

After the LTRSA is executed, a number of sub-channels will be allocated to the considered DP. We denote the allocated sub-channels by $\mathcal { N } = \{ 1 , \cdots , N \}$ . The UEs in M will share these sub-channels. Since each UE wishes to transmit its data through one or several orthogonal sub-channels, we can define the sub-channel allocation matrix $\mathbf { A } = ( a _ { m n } ) _ { M \times N }$ as

$$
a _ { m n } = \left\{ \begin{array} { l } { { 1 , \mathrm { ~ i f ~ U E ~ } m \mathrm { ~ s e l e c t s ~ s u b } \mathrm { - c h a n n e l ~ } n , } } \\ { { 0 , \mathrm { o t h e r w i s e . } } } \end{array} \right.\tag{32}
$$

Therefore, the selection of UE m can be represented by $\mathbf { a } _ { m } ^ { T } .$ which is the m-th row of A. To ensure fairness, we constrain that the number of sub-channels occupied by each UE is within the bound $[ 1 , \lceil N / M \rceil ]$ . In other words, the row sum of A satisfies:

$$
1 \leq \sum _ { n = 1 } ^ { N } a _ { m n } \leq \lceil N / M \rceil , \forall m \in \mathcal { M } .\tag{33}
$$

The strategy space of UE m can be represented by:

$$
A _ { m } = \big \{ \mathbf { a } _ { m } ^ { T } | a _ { m n } \in \{ 0 , 1 \} , 1 \leq \mathbf { 1 } ^ { T } \mathbf { a } _ { m } \leq \lceil N / M \rceil \big \} ,\tag{34}
$$

where 1 is a column vector with all 1 elements. It can be seen that the strategy spaces of different UEs are the same, $\mathrm { i . e . , }$ $A _ { l } = A _ { m } , \forall l , m \in \mathcal { M }$ . Thus, we will omit the subscript of $A _ { m }$ in cases where it is unnecessary. The joint strategy space can be represented by $\textstyle A = \prod _ { m = 1 } ^ { M } { \dot { A } }$

The channel gain matrix is $\mathbf { G } = ( g _ { m n } ) _ { M \times N }$ , where $g _ { m n } >$ 0 is the gain of sub-channel n from UE m to the UAV/BS. We assume that UE m transmits at a fixed power level $p _ { m }$ on each sub-channel. Since $a _ { m n }$ is a binary variable, thus the achievable transmission rate of UE m can be represented by:

$$
r _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) = \sum _ { n = 1 } ^ { N } W \log ( 1 + \frac { a _ { m n } p _ { m } g _ { m n } } { \displaystyle \sum _ { k \neq m } a _ { k n } p _ { k } g _ { k n } + \sigma _ { 0 } ^ { 2 } } ) ,\tag{35}
$$

where $\mathbf { a } _ { - m }$ is the partial strategy of all UE in the DP, except UE m; W is the bandwidth of the sub-channel. Assume that in the current minislot, the amount of data to be transmitted by UE m is $q _ { m }$ . Thus, the transmission delay of UE m is

$$
\psi _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) = \frac { q _ { m } } { r _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) } .\tag{36}
$$

We define the utility of each UE $m \in \mathcal { M }$ as:

$$
u _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) = \mu _ { m } \frac { \bar { \psi } _ { m } - \psi _ { m } } { \bar { \psi } _ { m } } + \nu _ { m } \frac { r _ { m } - \bar { r } _ { m } } { \bar { r } _ { m } } ,\tag{37}
$$

where $\mu _ { m } \in [ 0 , 1 ]$ is the preference on latency of UE m and $\mu _ { m } + \nu _ { m } = 1 ; \psi _ { m }$ and $\bar { r } _ { m }$ are the maximum delay and the minimum transmission rate requested by UE m. Thus, the small time-scale slice adaption problem can be formulated as the following strategic game:

$$
\mathcal { G } = < \mathcal { M } , \mathcal { A } , ( u _ { m } ) _ { m \in \mathcal { M } } > ,\tag{38}
$$

which is a stochastic game since the channel gain matrix G and the user demand $q _ { m }$ are stochastic. To proceed, we present the concept of (pure-strategy) NE as follows.

Definition 1: A strategy profile $\mathbf { a } = ( a _ { 1 } , \cdots , a _ { m } )$ is a pure strategy NE of the game G if for all $m \in \mathcal { M }$ and $\mathbf { a } _ { - m } \in \mathcal { A } _ { - m } ,$ it holds that

$$
\Phi _ { m } ( a _ { m } , { \bf a } _ { - m } ) \geq \Phi _ { m } ( a _ { m } ^ { \prime } , { \bf a } _ { - m } ) , \forall a _ { m } ^ { \prime } \in { \cal A } _ { m } ,\tag{39}
$$

where $\begin{array} { r } { \mathcal { A } _ { - m } = \prod _ { l \neq m } A _ { l } } \end{array}$ is the partial strategy space of all UEs within the DP, except UE m.

## B. Existence of NEs of G

Theoretically, the problem of finding the NE of a strategic game is proven to fall in a complexity class called PPAD-complete, where PPAD is a subclass of NP-complete problems [25]. As a result, there is no polynomial time algorithm capable of finding an NE, even for finding a mixed-strategy of a two-player game. Fortunately, the game G falls in a special type of game called potential games, where a pure-strategy NE can be easily found. Potential games encompass many different sub-classes, two of which are defined in the following.

Definition 2 (Exact Potential Game): The game $\mathcal { G }$ is an exact potential game, if and only if there exists a potential function $\Phi \ : \ A \ \to \ \mathbb { R }$ such that for all $\textit { m } \in \textit { M }$ and $\forall \mathbf { a } _ { - m } \in \mathcal { A } _ { - m }$

$$
\begin{array} { r l } & { u _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) - u _ { m } ( \mathbf { a } _ { m } ^ { \prime } , \mathbf { a } _ { - m } ) = } \\ & { \Phi ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) - \Phi ( \mathbf { a } _ { m } ^ { \prime } , \mathbf { a } _ { - m } ) , \forall \mathbf { a } _ { m } , \mathbf { a } _ { m } ^ { \prime } \in A _ { m } . } \end{array}\tag{40}
$$

Definition 3 (Ordinal Potential Game): The game $\mathcal { G }$ is an ordinal potential game, if and only if there exists a potential

function $\Phi : { \mathcal { A } }  \mathbb { R }$ such that for all $m \in \mathcal { M }$ and $\forall \mathbf { a } _ { - m } \in$ $A _ { - m }$ , there is

$$
\begin{array} { r l } & { u _ { m } ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) - u _ { m } ( \mathbf { a } _ { m } ^ { \prime } , \mathbf { a } _ { - m } ) > 0 \iff } \\ & { \Phi ( \mathbf { a } _ { m } , \mathbf { a } _ { - m } ) - \Phi ( \mathbf { a } _ { m } ^ { \prime } , \mathbf { a } _ { - m } ) > 0 , \forall \mathbf { a } _ { m } , \mathbf { a } _ { m } ^ { \prime } \in A _ { m } . } \end{array}\tag{41}
$$

It is seen that any exact potential game is an ordinal potential game. One can easily verify the following lemma about these two kinds of potential games.

Lemma 2: Assume the game $\mathcal { G } _ { 1 } = < \mathcal { M } , \mathcal { A } , \{ u _ { m } ^ { \prime } \} _ { m \in \mathcal { M } } >$ is an exact potential game with potential function Î¦. Consider the strategic game defined by $\mathcal { G } _ { 2 } = < \mathcal { M } , \mathcal { A } , \{ u _ { m } ^ { \prime \prime } \} _ { m \in \mathcal { M } } > .$ If $u _ { m } ^ { \prime \prime } = \rho ( u _ { m } ^ { \prime } )$ such that $\rho ( \cdot )$ is a strictly increasing function, then $\mathcal { G } _ { 2 }$ must be an ordinal potential game with the potential function Î¦.

Based on the above lemma, we can derive the following conclusion about the game G.

Theorem 3: The game G is an ordinal potential game with the potential function given by:

$$
\Phi ( { \bf a _ { m } } , { \bf a _ { - m } } ) = \sum _ { n = 1 } ^ { N } W \log \left( \sigma _ { 0 } ^ { 2 } + \sum _ { m = 1 } ^ { M } a _ { m n } p _ { m } g _ { m n } \right)\tag{42}
$$

Proof: Consider the game ${ \mathcal { G } } ^ { \prime } \stackrel { \cdots } { = } { < { \mathcal { M } } } , { \mathcal { A } } , ( r _ { m } ) _ { m \in { \mathcal { M } } } ^ { \prime } > ,$ where $r _ { m }$ is defined by (35). We notice that

$$
\begin{array} { l } { { \log ( 1 + \frac { a _ { m n } p _ { m } g _ { m n } } { \displaystyle \sum _ { k \neq m } a _ { k n } p _ { k } g _ { k n } + \sigma _ { 0 } ^ { 2 } } ) } \ ~ } \\ { { = \log ( \displaystyle \sum _ { k } a _ { k n } p _ { k } g _ { k n } + \sigma _ { 0 } ^ { 2 } ) - \log ( \displaystyle \sum _ { k \neq m } a _ { k n } p _ { k } g _ { k n } + \sigma _ { 0 } ^ { 2 } ) . } } \end{array}
$$

Thus for all $m \in \mathcal { M }$ and $\forall \mathbf { a } _ { - m } \in A _ { - m } .$

$$
\begin{array} { r l } & { \mathbb { P } _ { \mathrm { r e f } } \{ \Delta \mathbf { r } _ { 1 } , \mathbf { R } _ { 2 } , \mathbf { u } _ { 2 } , \mathbf { b } _ { 1 } , \mathbf { b } _ { 2 } , \mathbf { b } _ { 2 } \} } \\ & { = \displaystyle \sum _ { s = 1 } ^ { N } W \log ( 1 + \frac { G _ { \mathrm { a n d } } p q B _ { \mathrm { a n d } } \log m _ { \mathrm { a n d } } } { \sum _ { s = 1 } ^ { N } m _ { s } ! p q B _ { \mathrm { a n d } } \int _ { 0 } ^ { 1 } N + 1 + \frac { G _ { \mathrm { a n d } } ^ { 2 } p q B _ { \mathrm { a n d } } } { \sum _ { s = 1 } ^ { N } m _ { s } ! p q B _ { \mathrm { a n d } } \int _ { 0 } ^ { 1 } N } ) } } \\ &  \quad - \displaystyle \sum _ { s = 1 } ^ { N } W \log ( 1 - \frac { G _ { \mathrm { a n d } } ^ { 2 } p q B _ { \mathrm { a n d } } \log m _ { \mathrm { a n d } } } { \sum _ { s = 1 } ^ { N } m _ { s } ! p q B _ { \mathrm { a n d } } \phi _ { \mathrm { a n d } } + \frac { G _ { \mathrm { a n d } } ^ { 2 } } { \sum _ { s = 1 } ^ { N } m _ { s } ! p q B _ { \mathrm { a n d } } \phi _ { \mathrm { a n d } } } + \frac { G _ { \mathrm { a n d } } ^ { 2 } } { \sum _ { s = 1 } ^ { N } m _ { s } ! p q B _ { \mathrm { a n d } } \phi _ { \mathrm { a n d } } } ) } \\ & { = \displaystyle \sum _ { s = 1 } ^ { N } W \log ( \sum _ { s = 1 } ^ { \infty } a _ { s } ! p B _ { \mathrm { a n d } } + a _ { \mathrm { a n d } } p _ { \mathrm { a n d } } \log m _ { \mathrm { a n d } } + a _ { \mathrm { a n d } } ^ { 2 } ) } \\ &  \quad - \displaystyle \sum _ { s = 1 } ^ { N } W \log ( 1 - \sum _ { s = 1 } ^ { N } a _ { s } ! p B _  \mathrm  \end{array}
$$

Therefore, $\mathcal { G } ^ { \prime }$ is an exact potential game with potential function Î¦. It is seen that $u _ { m }$ is a strictly increasing function of $r _ { m } .$ From Lemma 2, we conclude that $\mathcal { G }$ is an ordinal potential game with potential function Î¦. â¡

The existence of NE of an ordinal potential game is guaranteed by the following lemma (Corollary 2.1 of [26]):

Lemma 3: For any ordinal potential game, if its potential function has a maximum point in its strategy space, then it has at least one pure-strategy NE.

Finally, we obtain the following theorem about the existence of pure strategy NE of G.

Theorem 4: The game G has a pure-strategy NE.

Proof: Since the strategy space A of game G is finite and the potential function Î¦ is bounded, thus Î¦ has a maximum point in A. According to Lemma 3, we conclude that G has a pure-strategy NE. â¡

For ordinal potential games, there are some algorithms that can converge to the NE, such as spatial adaptive play [27], fictitious play [28], [29] and best-response dynamics [30]. However, these algorithms are not applicable in our stochastic game for several reasons. First, the convergence of these algorithms is only guaranteed for potential games in static environments. Second, these algorithms are not fully distributed and complete information about the actions chosen by other players is required in each iteration. Considering the salient features of distributed learning, such as privacy-preserving nature and the ability to learn in dynamic environments [31], [32], [33], we resort to it for addressing the aforementioned challenges.

In particular, our proposed method is based on LA, which is a distributed learning algorithm for adaptive decision-making in unknown and dynamic environments [34]. Currently, due to its simplicity, little need for information, and distributed nature, LA is among the most valuable tools for designing RL and MARL algorithms for Markov games [35]. One classical LA is LRI-based LA, which is lightweight and fully distributed algorithm for stochastic games. Aided by the LRI-based LA, we propose a fully distributed learning algorithm (FDLA) to find the NE of the stochastic game G. The pseudo-code of FDLA is presented in Algorithm 1.

## C. Fully Distributed Learning-Based Slice Adaption Algorithm

FDLA starts at a random mixed-strategy profile $\begin{array} { r l } { \mathbf { P } ^ { t } } & { { } = } \end{array}$ $( \mathbf { p } _ { 1 } ^ { t } , \cdots , \mathbf { p } _ { M } ^ { t } )$ , in which

$$
\mathbf { p } _ { m } ^ { t } = ( p _ { m 1 } ^ { t } , \cdot \cdot \cdot , p _ { m k _ { m } } ^ { t } ) .\tag{44}
$$

In other words, $ { \mathbf { p } } _ { m } ^ { t }$ is a probability vector such that $p _ { m j } ^ { t } \ge$ 0 and $\begin{array} { r } { \sum _ { j = 1 } ^ { | A | } p _ { m j } ^ { t } = 1 } \end{array}$ . Here, $p _ { m j } ^ { t } ( j \in A )$ is the probability that UE m to choose the jth action at tth minislot. At the iteration step, all active UEs select actions according to their current mixed strategy profile to play the game. At each minislot, the stochastic game G is played and each UE will evaluate its achieved utility $u _ { m } ^ { t }$ . Note that $u _ { m } ^ { t }$ is determined by the locally measured $r _ { m }$ and $\psi _ { m }$ from UE m in a statistical manner, without requiring calculations based on equations (35) and (36). Consequently, there is no need for information exchange with the BS/UAV or other UEs, thus eliminating the signaling overhead caused by channel estimation and action exchange.

Based solely on the achieved utility $u _ { m } ^ { t }$ and the selected action $a _ { m }$ , each active UE will update its strategy profile according to (43). The strategy updating rule in (43) can be interpreted intuitively as follows. If action $a _ { m }$ can increase the utility of UE m, it will be reinforced in the next minislot by increasing its probability been selected. Otherwise, the probability of selecting action $a _ { m }$ will be decreased. The algorithm terminates if a pure-strategy profile is found $( \mathrm { i . e . } ,$ if max $_ { ( j \in A _ { m } } p _ { m j } ^ { t } \geq 1 - \epsilon , \forall m \in \mathcal { M } .$ , where Ïµ is a small positive scalar), or the iteration limit $t _ { m a x }$ is reached. We will show that by properly choosing the parameters Î» and $t _ { m a x } ,$ , FDLA can always converge to a pure-strategy NE of the stochastic game G.

Algorithm 1 The Fully Distributed Learning   
Algorithm (FDLA) for SAP   
Input : Î», Ïµ, tmax   
1 Initialization: $\mathbf { A } { \mathrm { t } } \ t = 0 ,$ , the mixed strategy of each   
UE $m \in \mathcal { M }$ is set as ${ \bf p } _ { m } ^ { 0 } = ( 1 / N , \cdots , 1 / N )$ ;   
2 while $t \leq t _ { m a x }$ andâm $\in { \mathcal { M } } ,$ such that   
max $_ { j \in A _ { m } } p _ { m j } ^ { t } < 1 - \epsilon$ do   
3 a) Generate slice adaption actions: At the   
beginning of tth minislot, each active UE $m \in \mathcal { M }$   
randomly selects an action $a _ { m }$ according to its   
current mixed strategy $ { \mathbf { p } } _ { m } ^ { t }$ . The inactive UEs take   
no action.   
4 b) Evaluate stochastic utilities: After the   
stochastic game is played, each active UE   
evaluates its utility $u _ { m } .$ , while the inactive UEs   
take no action.   
5 c) Update the strategy profile: Each active UE   
updates its mixed strategy for the $( t + 1 ) \cdot \mathrm { t h }$   
minislot according to the following rule:   
$\mathbf { p } _ { m } ^ { t + 1 } = \mathbf { p } _ { m } ^ { t } + \lambda \frac { u _ { m } ^ { t } } { u _ { m a x } } ( \mathbf { e } _ { a _ { m } } - \mathbf { p } _ { m } ^ { t } ) ,$ (43)   
where $\lambda \in ( 0 , 1 ) ; u _ { m } ^ { t }$ is the utility of UE m at   
t-th minislot; $u _ { m a x }$ is a scaling factor such that   
$u _ { m } ^ { t } / u _ { m a x } \in [ 0 , 1 ] ; \mathbf { e } _ { a _ { m } }$ is an $\left| A _ { m } \right|$ -dimensional   
unit vector with $a _ { m }$ th competent unity. The   
inactive UEs keep their strategy unchanged.   
6 $t \gets t + 1 .$   
7 end   
Output: A strategy profile $\mathbf { P } = ( \mathbf { p } _ { 1 } , \cdots , \mathbf { p } _ { M } ) .$

## D. Convergence of FDLA

To proceed, we denote the set of all mixed-strategy profiles of G by K. The updating rule of (43) can be represented as

$$
\mathbf { P } ^ { t + 1 } = \mathbf { P } ^ { t } + \lambda G ( \mathbf { P } ^ { t } , \mathbf { a } ^ { t } , \mathbf { u } ^ { t } ) ,\tag{45}
$$

where $\mathbf { a } ^ { t } = ( a _ { 1 } ^ { t } , \cdots , a _ { M } ^ { t } )$ and $\mathbf { u } ^ { t } = ( u _ { 1 } ^ { t } , \cdot \cdot \cdot , u _ { M } ^ { t } )$ denote the selected actions and the achieved utilities by the UEs at tth minislot, respectively; $G ( \cdot , \cdot , \cdot )$ is specified by the updating rule of (43). We denote the generated sequence of algorithm FDLA by {Pt}. According to Theorem 3.1 of [36] we have

Lemma 4: With a sufficiently small step size $\lambda ,$ the sequence $\mathbf { P } ^ { t }$ will converge weakly to $\mathbf { P } ^ { * }$ , where $\mathbf { P } ^ { * }$ is the solution of the following autonomous ordinary differential equation (ODE):

$$
\frac { d \mathbf { P } } { d t } = f ( \mathbf { P } ) , \mathbf { P } ( 0 ) = \mathbf { P } ^ { 0 } ,\tag{46}
$$

in which $\mathbf { P } ^ { 0 }$ is the initial mixed-strategy profile, and $f ( \mathbf { P } )$ is defined as:

$$
f ( \mathbf { P } ) = \mathbb { E } \left\{ G ( \mathbf { P } ^ { t } , \mathbf { a } ^ { t } , \mathbf { u } ^ { t } ) | \mathbf { P } ^ { t } \right\} .\tag{47}
$$

The following lemma characterizes the relationship between the solutions of ODE (46) and the NEs of game G (see Theorem 3.2 of [36]).

Lemma 5: If Î» is sufficiently small, all the stable stationary points of (46) are NEs of game G.

In the following two theorems, we prove that the proposed FDLA algorithm converges to an NE of game G. To this end, we first define $h _ { m j } ( \mathbf { P } )$ as the expected utility of UE m if it employs pure strategy $j \in A$ while other UEs employ mixed strategy $\bar { \mathbf { p } } _ { - m } ^ { t } = ( \mathbf { p } _ { 1 } ^ { t } , \cdot \cdot \cdot , \mathbf { p } _ { m - 1 } ^ { t } , \mathbf { p } _ { m + 1 } ^ { t } , \cdot \cdot \cdot \mathbf { p } _ { M } ^ { t } )$ . Formally,

$$
h _ { m j } ( \mathbf { P } ) = \sum _ { \mathbf { a } _ { - m } ^ { t } } \mathbb { E } [ u _ { m } ( j , \mathbf { a } _ { - m } ^ { t } ) ] \prod _ { k \neq m } p _ { k a _ { k } ^ { t } } ,\tag{48}
$$

where $\mathbf { a } _ { - m } ^ { t } ~ = ~ ( a _ { 1 } ^ { t } , \cdot \cdot \cdot ~ , a _ { m - 1 } ^ { t } , a _ { m + 1 } ^ { t } , \cdot \cdot \cdot , a _ { M } ^ { t } )$ . Based on Lemma 4 and Lemma 5, we can derive the following sufficient condition that guarantees the convergence of $\{ \mathbf { P } ^ { t } \}$ towards the NE of game G.

Theorem 5: If there exists a bounded differentiable function $X : \mathbb { R } ^ { | \mathcal { A } | } $ R such that for all $m \in { \mathcal { M } } ,$ , and $\forall j , k \in A ,$ $\forall \mathbf { P } \in \mathbf { K } ,$

$$
\frac { \partial X ( \mathbf { P } ) } { \partial p _ { m j } } - \frac { \partial X ( \mathbf { P } ) } { \partial p _ { m k } } > 0 \Longleftrightarrow h _ { m j } ( \mathbf { P } ) - h _ { m k } ( \mathbf { P } ) > 0 ,\tag{49}
$$

then the algorithm FDLA always converges to an NE of g. then the algorithm FDLA always converges to an NE of G.

Proof: We observe that P contains $M \times | A |$ non-negative components denoted by $p _ { m j } \geq 0 , m \in \mathcal { M } , j \in A .$ . And $f$ also has the same number of components and can be denoted as $f _ { m j }$ . Thus, the component equations of ODE (46) are:

$$
\frac { d p _ { m j } } { d t } = f _ { m j } ( \mathbf { P } ) , m \in \mathcal { M } , j \in A .\tag{50}
$$

According to Equation (16) of [36], the ODE (46) can be written as

$$
\frac { d p _ { m j } } { d t } = p _ { m j } \sum _ { k \in A } p _ { m k } \left[ h _ { m j } ( \mathbf { P } ) - h _ { m k } ( \mathbf { P } ) \right] , m \in \mathcal { M } , j \in A .\tag{51}
$$

Consider the variation of $X ( \cdot )$ along the trajectories of the ODE (46). According to the equation of total derivative, we have

$$
\begin{array} { l } { \displaystyle \frac { d X } { d t } = \sum _ { m \in \mathcal { M } } \sum _ { j \in A } \frac { \partial X ( \mathbf { P } ) } { \partial p _ { m j } } \frac { d p _ { m j } } { d t } } \\ { \displaystyle ~ = \sum _ { m } \sum _ { j } \frac { \partial X ( \mathbf { P } ) } { \partial p _ { m j } } p _ { m j } \sum _ { k \in A } p _ { m k } \left[ h _ { m j } ( \mathbf { P } ) - h _ { m k } ( \mathbf { P } ) \right] } \\ { \displaystyle ~ = \frac { 1 } { 2 } \sum _ { m , j , k } p _ { m j } p _ { m k } \left( \frac { \partial X ( \mathbf { P } ) } { \partial p _ { m j } } - \frac { \partial X ( \mathbf { P } ) } { \partial p _ { m k } } \right) } \\ { ~ \displaystyle ~ \cdot \left[ h _ { m j } ( \mathbf { P } ) - h _ { m k } ( \mathbf { P } ) \right] . } \end{array}\tag{}
$$

By (49), we conclude that

$$
{ \frac { d X ( \mathbf { P } ) } { d t } } \geq 0 .\tag{53}
$$

Therefore, $X ( \mathbf { P } )$ is non-decreasing along the trajectories of the ODE (46). According to the procedure of FDLA, it is seen that the solutions of the ODE are confined to K which is a compact subset of $\mathbb { R } ^ { | \boldsymbol { A } | }$ . Thus, by [36] and Theorem 2.7 of [37], P converges to $\mathbf { P } ^ { * }$ such that:

$$
\frac { d X ( \mathbf { P } ^ { * } ) } { d t } = 0 .\tag{54}
$$

Since $p _ { m j } ^ { * } \ge 0 .$ , according to (49), we have

$$
p _ { m j } ^ { * } p _ { m k } ^ { * } \left[ h _ { m j } ( \mathbf { P } ^ { * } ) - h _ { m k } ( \mathbf { P } ^ { * } ) \right] ^ { 2 } = 0 , \forall m \in \mathcal { M } , \forall j , k \in A ,\tag{55}
$$

which suggests for all $m \in \mathcal { M }$ , and $\forall j \in A$

$$
\begin{array} { l } { f _ { m j } ( \mathbf { P } ^ { * } ) = \displaystyle \frac { d p _ { m j } ^ { * } } { d t } } \\ { = \displaystyle \sum _ { k \in \cal A } p _ { m j } ^ { * } p _ { m k } ^ { * } \left[ h _ { m j } ( \mathbf { P } ^ { * } ) - h _ { m k } ( \mathbf { P } ^ { * } ) \right] = 0 . } \end{array}\tag{56}
$$

Thus, $\mathbf { P } ^ { * }$ is a stable stationary point of the ODE (46). By Lemma 5, we conclude that FDLA converges to an NE of G provided that there exists a bounded differentiable $X ( \cdot )$ satisfying (49).

Until now, we have not proved whether FDLA can converge to the NE of G. In the following theorem, we will prove this by showing that game G satisfies the sufficient condition of Theorem 5.

Theorem 6: Define the function $X : \mathbb { R } ^ { | \mathcal { A } | } \longrightarrow \mathbb { R }$ as

$$
X ( { \bf P } ) = \mathbb { E } \left[ \Phi ( a _ { m } ^ { t } , { \bf a } _ { - m } ^ { t } ) | { \bf P } \right] = \sum _ { j \in A } p _ { m j } \mathbb { E } \left[ \Phi ( j , { \bf a } _ { - m } ^ { t } ) | { \bf P } \right] ,\tag{57}
$$

then $X ( \cdot )$ satisfies condition (49) of Theorem 5. Namely, FDLA converges to an NE of G.

Proof: It can be seen that the function $X ( \cdot )$ given by (57) is bounded since Î¦ is bounded. Also, $X ( \cdot )$ is differentiable with the partial derivatives given by:

$$
\frac { \partial X ( \mathbf { P } ) } { \partial p _ { m j } } = \mathbb { E } \left[ \Phi ( j , \mathbf { a } _ { - m } ^ { t } ) | \mathbf { P } \right] , \forall m \in \mathcal { M } , \forall j \in A .\tag{58}
$$

Thus

$$
\begin{array} { r l } & { \frac { \partial X ( { \bf P } ) } { \partial p _ { m j } } - \frac { \partial X ( { \bf P } ) } { \partial p _ { m k } } = \mathbb { E } \left[ \Phi ( j , { \bf a } _ { - m } ^ { t } ) - \Phi ( k , { \bf a } _ { - m } ^ { t } ) | { \bf P } \right] } \\ & { = \displaystyle \sum _ { { \bf a } _ { - m } ^ { t } } \mathbb { E } [ \Phi ( j , { \bf a } _ { - m } ^ { t } ) - \Phi ( k , { \bf a } _ { - m } ^ { t } ) ] \prod _ { s \ne m } p _ { s a _ { s } ^ { t } } . } \end{array}
$$

By the definition of $h _ { m j } ( \mathbf { P } )$ (cf. Equation (48)), we have

$$
\begin{array} { l } { { \displaystyle h _ { m j } ( { \bf P } ) - h _ { m k } ( { \bf P } ) } \ ~ } \\ { { \displaystyle = \sum _ { { \bf a } _ { - m } ^ { t } } \left\{ \mathbb { E } [ u _ { m } ( j , { \bf a } _ { - m } ^ { t } ) ] \ - \mathbb { E } [ u _ { m } ( k , { \bf a } _ { - m } ^ { t } ) ] \right\} \prod _ { s \neq m } p _ { s a _ { s } ^ { t } } } . } \end{array}
$$

According to the definition of ordinal potential game, it follows that $X ( \cdot )$ satisfies condition (49). Thus, by Theorem 5, we finally prove that FDLA is guaranteed to converge to an NE of G.

Remark 1: Note that the above proof does not depend on the specific form of ${ \mathcal { G } } ,$ but only relies on the boundedness of the potential function Î¦. For finite ordinal potential games, the boundedness of their potential functions is always guaranteed. In this context, âfiniteâ refers to the finiteness of the gameâs strategy space [26]. Thus, as an important theoretical contribution of this paper, we have proved the following theorem.

Theorem 7: For finite ordinal potential games, LRI-based LA is guaranteed to converge to an NE.

Note also that we have only proved that algorithm FDLA can converge to an NE of G. Whether the limit point is a pure-strategy NE or a mixed-strategy NE has not been proved. Fortunately, extensive studies have shown that for potential games, LRI-based LA always converges to a pure-strategy NE rather than to a mixed strategy NE [38], [39], [40]. In Section V. We will demonstrate that our proposed FDLA has the same property as well.

Remark 2: Some implementation issues must be clarified. It is seen that the small time-scale slice adaption can be divided into two stages: the learning stage and the transmission stage. At the learning stage, each UE learns to adapt to the dynamic environment by sending some data to the BS/UAV. Based on the statistics, the achieved utility can be evaluated locally and the algorithm iterates until converges. After the strategy converges to an NE, each UE will transmit its data following the converged strategy at the transmission stage. According to our simulation results as shown in Fig. 3b and Fig. 3c, we can see that FDLA can converge within hundreds of iterations. Since the computation overhead of LTRSA and FDLA is very small (see the analysis in Section III-C and Equation (43)), we conclude that our proposed two time-scale approach is lightweight and efficient.

## V. NUMERICAL RESULTS AND DISCUSSIONS

In this section, we evaluate the performance of our proposed framework by numerical simulations. First, we elaborate the scenarios and parameters used in the simulations. Then we examine the convergence property of the proposed algorithms. Finally, we compare our algorithms with some known benchmark algorithms to examine their performance gains.

## A. Simulation Settings

We consider a UAWN where a UAV supplements a terrestrial wireless network which covers a circular area with a radius of 1km. The BS and the UAV are located at the center of the UAWN, while the UEs are randomly distributed. The available bandwidths of the BS and the UAV are set as $W ^ { U } = W ^ { B } = 1 0 0 \mathbf { M } \mathrm { { H z } }$ . For the UAV, the antenna beamwidth is set as $\theta = \pi / 4$ , while its altitude is confined in the range [50, 500]m [23]. In this scenario, 5 network slices are deployed over the UAWN, each of which contains 30 to 80 UEs. For each slice, its subscribed UEs are geographically partitioned into 10 groups, each of which corresponds to a DP. According to [41], the transmission power of each UE is randomly generated in [0.05, 0.15] Watt. The gain of the sub-channels between the UE and the BS and the UAV is proportional to $d ^ { - \eta }$ , where $\eta = 4$ is the path loss exponent according to the channel model in urban and suburban areas [41]. The power of background noise is set to -100 dBm.

<!-- image-->  
(a) Computation time of LTRSA

<!-- image-->  
(b) Convergence of the strategy of FDLA

<!-- image-->  
(c) Convergence of the utility of FDLA  
Fig. 3. The convergence results of LTRSA and FDLA.

The service type of each slice is randomly selected from the following two kinds of services: uRLLC and eMBB. The sub-channel bandwidths of the network slice are randomly chosen from {0.1, 0.5} MHz (for uRLLC type) and {2, 5} MHz (for eMBB type), respectively. The preference on latency $\mu _ { m }$ of each UE is set to 0.8 and 0.6 for uRLLC and eMBB, respectively. To emulate the dynamic environment of the considered scenario, we assume that the sub-channels are Rayleigh fading channels. We use the straight line motion with random bouncing, a well-known mobility pattern defined in 3GPP [42]. Furthermore, we simulate the stochastic demand of the UE by assuming that the arrival of the requests follows Poisson processes with an arrival rate of 0.1 pkt/TTI and 0.03 pkt/TTI for uRLLC and eMBB, respectively. In the simulation, we assume that the minislot corresponds to one TTI.

## B. Convergence Performance

First, we show the convergence performance of LTRSA by evaluating its running time. We set the number of network slices from 5 to 20 and run LTRSA 100 times at each setting. The results are shown by the boxplot in Fig. 3a. As can be seen from Fig. 3a, the running time of LTRSA increases linearly with the number of slices. This result verifies that LTRSA is a pseudo-polynomial algorithm. Then in Fig. 3b, we evaluate the convergence performance of FDLA by plotting the evolution of sub-channel selection probabilities $p _ { m j } ^ { t }$ for an arbitrary UE. The input parameters Î» and Ïµ of FDLA are set to 0.05 and 0.001, respectively. It can be seen that the strategy of the UE evolves from a mixed strategy to a pure strategy within 1000 minislots. This result verifies that FDLA can converge to a pure-strategy NE of the stochastic game rapidly. As each iteration of FDLA involves simple operations( as shown in (43)), this result verifies that FDLA can converge to a pure-strategy NE of the stochastic game in a short period of time. Therefore, we conclude that our proposed framework is lightweight and converges fast.

## C. Comparison With Benchmark Algorithms

Although the comparison between LTRSA and other algorithms is useful, it is dispensable since the large time-scale problem is solved by the proposed LTRSA optimally. Due to the page limit, we only focus on comparing FDLA with some known algorithms for the small time-scale problem. To ensure the fairness of the comparison, we have compared FDLA with two distributed algorithms. Additionally, to evaluate the impact of the absence of information exchange in FDLA, we also compare it with two centralized algorithms. In particular, the comparison benchmarks are:

â¢ Genetic Algorithm Centralized (GAC): In this algorithm, SAP is modeled as a MINLP which aims at maximizing the sum of instantaneous utilities of all UEs. Due to its NP-hardness, the MINLP is solved by the Genetic Algorithm (GA), where the population size and the number of iterations are set to 300 and 500, respectively. Note that GAC is a centralized algorithm that requires a central controller to collect the information of all UEs in each minislot.

â¢ Multi-Agent Deep Deterministic Policy Gradient (MADDPG) [43] : In this algorithm, SAP is regarded as a multi-agent problem and is solved by MADDPG. Although MADDPG utilizes the centralized-training and distributed execution, it is indeed a centralized algorithm since the information of channel state, UEsâ actions and the rewards should be exchanged.

â¢ Greedy Algorithm (Greedy): In this algorithm, the UEs select the sub-channels sequentially according to a predefined order. For the jth UE, it greedily selects âN/Mâ sub-channels by trial-and-error to maximize its QoE. This scheme is can be seen as a distributed algorithm, since only ordinal information is broadcasted to each UE.

â¢ Random Strategy Selection (RSS): In this algorithm, each UE selects an arbitrary strategy to transmit their data in each minislot. RSS is an instinctive algorithm under dynamic environments where information exchange is prohibited [44]. Besides, it is fully distributed since the channel conditions are a priori unknown and information exchange is prohibited.

1) Performance Under Different Sub-Channel Bandwidths: We compare the average utility, throughput, and delay with the benchmark algorithms under different sub-channel bandwidths. Note that before this simulation, the large time-scale algorithm LTRSA is executed and as a result, 8 sub-channels have been allocated to the considered DP, which is composed of 15 UEs. In this simulation, the channel bandwidth of the sub-channel varies from 0.5 MHz to 4.5 MHz. The results are shown in Fig. 4. Also note that we average the results for 500 simulations to avoid randomness.

<!-- image-->  
(a) utility

<!-- image-->  
(bï¼ throughput

<!-- image-->  
(c) delay

Fig. 4. Performance comparison w.r.t. sub-channel bandwidth.  
<!-- image-->  
(a) throughput  
Fig. 5. Performance comparison w.r.t. the number of UEs per slice.

In Fig. 4a, the average utilities of different algorithms are compared. It is seen that the curves of FDLA and GAC almost overlap, with a gap of only 0.3%. Hence, the fully distributed FDLA algorithm exhibits nearly the same performance as the centralized GAC algorithm. In addition, although information exchange is allowed in MADDPG, its utility is lower than that of FDLA. This is due to the fact that FDLA can converge to the NE of the game, while MADDPG can only converge to an approximate NE [45]. In Fig. 4b, the curves of the average throughput are plotted. As expected, we can see that the average throughput of these algorithms increases linearly with the bandwidth of the sub-channel. Furthermore, it can be seen that the average throughput of FDLA is about 9% lower than that of GAC, and is higher than the other benchmarks. Fig. 4c shows the curve of the average delay of these algorithms. We can observe that the average delay of FDLA is very close to GAC. Comparing the figures in Fig. 4, we observe a significantly smaller delay gap between FDLA and GAC compared to the throughput gap. This discrepancy can be attributed to the higher preference given to delay, as reflected in the values of $\mu _ { m }$ being within the set {0.6, 0.8}. To summarize, these results indicate that the prohibition of information exchange has a minor effect on the performance of FDLA.

<!-- image-->  
(b) delay

2) Performance Under Different Numbers of UEs: In this simulation, we compare our proposed FDLA with the benchmark algorithms under different numbers of UEs. Similar to the settings of the previous simulation, 8 sub-channels have been allocated to the DP by the LTRSA algorithm. The number of the UEs in the DP varies from 6 to 14. The results are averaged for 500 simulations and are plotted in Fig. 5. Note that this experiment does not show the results of MADDPG, as it does not support a variable number of agents [46].

In Fig. 5a, we see that the gap between the curves of FDLA and GAC is very small. In addition, we can also observe that the average throughputs of FDLA, GAC and Greedy decrease with the number of UEs, and ultimately approach a level comparable to that of the RSS algorithm. This is reasonable because as the channel becomes crowded, the optimal allocation scheme is to choose sub-channels randomly. In Fig. 5b, as expected, we can see that the average delay increases with the number of UEs in a DP. Moreover, it is also observed that the curve of FDLA is close to that of the GAC, with a gap of approximately 5%. In summary, we conclude that FDLA can efficiently maximize the system utility and throughput, while decreasing the latency of the UE.

## VI. CONCLUSION AND FUTURE WORK

In this paper, we focus on the problem of joint network slicing and UAV deployment in 6G networks. We have proposed a hierarchical framework that performs network slicing at different levels of time and resource granularity. At the large time-scale, we have designed a UAV slicing scheme to optimize the altitude of the UAV while performing inter-slice resource allocation. Then at the small time-scale, a lightweight distributed learning scheme is proposed to perform intra-slice resource adjustment according to the dynamic environment and the uncertain demand. The simulation results demonstrate that our proposed algorithms converge fast and have superior performance compared with the benchmark algorithms.

In this paper, we mainly focus on UAV slicing without considering the optimization of the power allocation, UAVâs beamwidth, etc. In the future, we intend to take power and beamwidth into consideration thus to further improve the efficiency of the proposed scheme.

## REFERENCES

[1] R. Ahmad, M. Ayyash, H. B. Salameh, R. El-Khazali, and H. Elgala, âIndoor flying networks for 6G: Concepts, challenges, enabling technologies, and opportunities,â IEEE Commun. Mag., vol. 61, no. 10, pp. 156â162, Oct. 2023.

[2] Y. Wang, M. Yan, G. Feng, S. Qin, and F. Wei, âAutonomous on-demand deployment for UAV assisted wireless networks,â IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 9488â9501, Dec. 2023.

[3] N. Qi, Z. Huang, W. Sun, S. Jin, and X. Su, âCoalitional formation-based group-buying for UAV-enabled data collection: An auction game approach,â IEEE Trans. Mobile Comput., vol. 22, no. 12, pp. 7420â7437, Dec. 2022. [Online]. Available: https://ieeexplore.ieee.org/document/9907875/

[4] W. Wang, N. Qi, L. Jia, C. Li, T. A. Tsiftsis, and M. Wang, âEnergyefficient UAV-relaying 5G/6G spectrum sharing networks: Interference coordination with power management and trajectory design,â IEEE Open J. Commun. Soc., vol. 3, pp. 1672â1687, 2022.

[5] N. Qi, Z. Huang, F. Zhou, Q. Shi, Q. Wu, and M. Xiao, âA taskdriven sequential overlapping coalition formation game for resource allocation in heterogeneous UAV networks,â IEEE Trans. Mobile Comput., vol. 22, no. 8, pp. 4439â4455, Aug. 2023. [Online]. Available: https://ieeexplore.ieee.org/document/9756371/

[6] P. Yang, X. Xi, K. Guo, T. Q. S. Quek, J. Chen, and X. Cao, âProactive UAV network slicing for URLLC and mobile broadband service multiplexing,â IEEE J. Sel. Areas Commun., vol. 39, no. 10, pp. 3225â3244, Oct. 2021.

[7] F. Wei, S. Qin, G. Feng, Y. Sun, J. Wang, and Y.-C. Liang, âHybrid model-data driven network slice reconfiguration by exploiting prediction interval and robust optimization,â IEEE Trans. Netw. Service Manage., vol. 19, no. 2, pp. 1426â1441, Jun. 2022.

[8] Y.-H. Xu, J.-H. Li, W. Zhou, and C. Chen, âLearning-empowered resource allocation for air slicing in UAV-assisted cellular V2X communications,â IEEE Syst. J., vol. 17, no. 1, pp. 1008â1011, Mar. 2023.

[9] G. Faraci, C. Grasso, and G. Schembra, âDesign of a 5G network slice extension with MEC UAVs managed with reinforcement learning,â IEEE J. Sel. Areas Commun., vol. 38, no. 10, pp. 2356â2371, Oct. 2020.

[10] J. Mei, X. Wang, and K. Zheng, âAn intelligent self-sustained RAN slicing framework for diverse service provisioning in 5G-beyond and 6G networks,â Intell. Converg. Netw., vol. 1, no. 3, pp. 281â294, Dec. 2020.

[11] J. Li et al., âA hierarchical soft RAN slicing framework for differentiated service provisioning,â IEEE Wireless Commun., vol. 27, no. 6, pp. 90â97, Dec. 2020.

[12] J. Mei, X. Wang, K. Zheng, G. Boudreau, A. B. Sediq, and H. Abou-Zeid, âIntelligent radio access network slicing for service provisioning in 6G: A hierarchical deep reinforcement learning approach,â IEEE Trans. Commun., vol. 69, no. 9, pp. 6063â6078, Sep. 2021.

[13] Y. Shao, R. Li, B. Hu, Y. Wu, Z. Zhao, and H. Zhang, âGraph attention network-based multi-agent reinforcement learning for slicing resource management in dense cellular network,â IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 10792â10803, Oct. 2021.

[14] H. Zhou, M. Elsayed, and M. Erol-Kantarci, âRAN resource slicing in 5G using multi-agent correlated Q-learning,â in Proc. IEEE 32nd Annu. Int. Symp. Pers. Indoor Mobile Radio Commun. (PIMRC), Sep. 2021, pp. 1179â1184.

[15] I. VilÃ , J. PÃ©rez-Romero, O. Sallent, and A. Umbert, âA multi-agent reinforcement learning approach for capacity sharing in multi-tenant scenarios,â IEEE Trans. Veh. Technol., vol. 70, no. 9, pp. 9450â9465, Sep. 2021.

[16] F. Wei, G. Feng, Y. Sun, Y. Wang, S. Qin, and Y.-C. Liang, âNetwork slice reconfiguration by exploiting deep reinforcement learning with large action space,â IEEE Trans. Netw. Service Manag., vol. 17, no. 4, pp. 2197â2211, Dec. 2020.

[17] A. Kak and I. F. Akyildiz, âTowards automatic network slicing for the Internet of Space Things,â IEEE Trans. Netw. Service Manage., vol. 19, no. 1, pp. 392â412, Mar. 2022.

[18] H. Shen, Y. Tian, T. Wang, and G. Bai, âSlicing-based task offloading in space-air-ground integrated vehicular networks,â IEEE Trans. Mobile Comput., vol. 23, no. 5, pp. 4009â4024, May 2023.

[19] F. Lyu et al., âService-oriented dynamic resource slicing and optimization for space-air-ground integrated vehicular networks,â IEEE Trans. Intell. Transp. Syst., vol. 23, no. 7, pp. 7469â7483, Jul. 2022.

[20] C. M. de Galland and J. M. Hendrickx, âFundamental performance limitations for average consensus in open multi-agent systems,â IEEE Trans. Autom. Control, vol. 68, no. 2, pp. 646â659, Feb. 2023.

[21] Y. Wang, S. Qin, G. Feng, J. Zhou, and F. Wei, âGAN-based Pareto optimization for self-healing of radio access network slices,â IEEE Trans. Netw. Service Manage., vol. 19, no. 1, pp. 146â157, Mar. 2022.

[22] W. Sui, X. Chen, S. Zhang, Z. Jiang, and S. Xu, âEnergy-efficient resource allocation with flexible frame structure for hybrid eMBB and URLLC services,â IEEE Trans. Green Commun. Netw., vol. 5, no. 1, pp. 72â83, Mar. 2021.

[23] A. A. Nasir, H. D. Tuan, T. Q. Duong, and H. V. Poor, âUAV-enabled communication using NOMA,â IEEE Trans. Commun., vol. 67, no. 7, pp. 5126â5138, Jul. 2019.

[24] A. M. Geoffrion, âGeneralized benders decomposition,â J. Optim. Theory Appl., vol. 10, no. 4, pp. 237â260, 1972.

[25] C. Daskalakis, P. W. Goldberg, and C. H. Papadimitriou, âThe complexity of computing a Nash equilibrium,â SIAM J. Comput., vol. 39, no. 1, pp. 195â259, Jan. 2009.

[26] Q. D. LÃ£, Y. H. Chew, and B.-H. Soong, Potential Game Theory. Cham, Switzerland: Springer, 2016.

[27] J. R. Marden, G. Arslan, and J. S. Shamma, âCooperative control and potential games,â IEEE Trans. Syst., Man, Cybern. B, Cybern., vol. 39, no. 6, pp. 1393â1407, Dec. 2009.

[28] D. Monderer and L. S. Shapley, âFictitious play property for games with identical interests,â J. Econ. Theory, vol. 68, no. 1, pp. 258â265, 1996.

[29] J. Marden, G. Arslan, and J. Shamma, âJoint strategy fictitious play with inertia for potential games,â IEEE Trans. Autom. Control, vol. 54, no. 2, pp. 208â220, Feb. 2009.

[30] D. Monderer and L. S. Shapley, âPotential games,â Games Econ. Behav., vol. 14, no. 1, pp. 124â143, May 1996.

[31] H. Chen, M. Xiao, and Z. Pang, âSatellite-based computing networks with federated learning,â IEEE Wireless Commun., vol. 29, no. 1, pp. 78â84, Feb. 2022. [Online]. Available: https://ieeexplore. ieee.org/document/9749193/

[32] Y. Ye, H. Chen, M. Xiao, M. Skoglund, and H. V. Poor, âPrivacypreserving incremental ADMM for decentralized consensus optimization,â IEEE Trans. Signal Process., vol. 68, pp. 5842â5854, 2020. [Online]. Available: https://ieeexplore.ieee.org/document/9214458/

[33] W. Lei, Y. Ye, M. Xiao, M. Skoglund, and Z. Han, âAdaptive stochastic ADMM for decentralized reinforcement learning in edge IoT,â IEEE Internet Things J., vol. 9, no. 22, pp. 22958â22971, Nov. 2022. [Online]. Available: https://ieeexplore.ieee.org/document/9810334/

[34] B. Masoumi and M. R. Meybodi, âLearning automata based multi-agent system algorithms for finding optimal policies in Markov games,â Asian J. Control, vol. 14, no. 1, pp. 137â152, 2012.

[35] Z. Zhang, D. Wang, and J. Gao, âLearning automata-based multiagent reinforcement learning for optimization of cooperative tasks,â IEEE Trans. Neural Netw. Learn. Syst., vol. 32, no. 10, pp. 4639â4652, Oct. 2021.

[36] P. S. Sastry, V. V. Phansalkar, and M. A. L. Thathachar, âDecentralized learning of Nash equilibria in multi-person stochastic games with incomplete information,â IEEE Trans. Syst., Man, Cybern., vol. 24, no. 5, pp. 769â777, May 1994.

[37] K. Narendra and A. Annaswamy, Stable Adaptive Systems. Upper Saddle River, NJ, USA: Prentice-Hall, 1989. [Online]. Available: https://books.google.com/books?id=6eD0oQEACAAJ

[38] J. Zheng, Y. Cai, W. Yang, Y. Xu, and A. Anpalagan, âA game-theoretic approach to exploit partially overlapping channels in dynamic and distributed networks,â IEEE Commun. Lett., vol. 18, no. 12, pp. 2201â2204, Dec. 2014.

[39] Y. Xu, J. Wang, Q. Wu, A. Anpalagan, and Y.-D. Yao, âOpportunistic spectrum access in unknown dynamic environment: A gametheoretic stochastic learning solution,â IEEE Trans. Wireless Commun., vol. 11, no. 4, pp. 1380â1391, Apr. 2012. [Online]. Available: http://ieeexplore.ieee.org/document/6151775/

[40] H. Cao and J. Cai, âDistributed multiuser computation offloading for cloudlet-based mobile cloud computing: A game-theoretic machine learning approach,â IEEE Trans. Veh. Technol., vol. 67, no. 1, pp. 752â764, Jan. 2018.

[41] L. Yang, H. Zhang, X. Li, H. Ji, and V. C. Leung, âA distributed computation offloading strategy in small-cell networks integrated with mobile edge computing,â IEEE/ACM Trans. Netw., vol. 26, no. 6, pp. 2762â2773, Dec. 2018.

[42] Multi-access Edge Computing (MEC); Support for Network Slicing, document TR 36.839, 3GPP, 2012.

[43] G. Zhou, L. Zhao, G. Zheng, S. Song, J. Zhang, and L. Hanzo, âMultiobjective optimization of spaceâairâground-integrated network slicing relying on a pair of central and distributed learning algorithms,â IEEE Internet Things J., vol. 11, no. 5, pp. 8327â8344, Mar. 2024.

[44] Y. Xu, J. Wang, Q. Wu, J. Zheng, L. Shen, and A. Anpalagan, âDynamic spectrum access in time-varying environment: Distributed learning beyond expectation optimization,â IEEE Trans. Commun., vol. 65, no. 12, pp. 5305â5318, Dec. 2017.

[45] H. Zhang et al., âBi-level actor-critic for multi-agent coordination,â in Proc. AAAI Conf. Artif. Intell., 2020, vol. 34, no. 5, pp. 7325â7332.

[46] H. Khorasgani, H. Wang, H.-K. Tang, and C. Gupta, âK-nearest multiagent deep reinforcement learning for collaborative tasks with a variable number of agents,â in Proc. IEEE Int. Conf. Big Data (Big Data), Dec. 2021, pp. 3883â3889.

<!-- image-->

Fengsheng Wei (Member, IEEE) received the B.E., M.E., and Ph.D. degrees from the School of Communication and Information Engineering, University of Electronic Science and Technology of China (UESTC), Huzhou, China, in 2012, 2016, and 2022, respectively. He is currently a full-time Researcher with Yangtze Delta Region Institute (Huzhou), University of Electronic Science and Technology of China. His current research interests include next-generation mobile communication systems, machine learning, global optimization, and network slicing for wireless networks.

<!-- image-->

Gang Feng (Senior Member, IEEE) received the B.Eng. and M.Eng. degrees in electronic engineering from the University of Electronic Science and Technology of China (UESTC), China, in 1986 and 1989, respectively, and the Ph.D. degree in information engineering from The Chinese University of Hong Kong in 1998. He joined as an Assistant Professor and an Associate Professor with the School of Electric and Electronic Engineering, Nanyang Technological University, in 2000 and 2005, respectively. He is currently a Professor with the National Key

Laboratory of Wireless Communications, UESTC. His research interests include AI-enabled wireless networking, distributed and collaborative machine learning, and next-generation cellular networks. He was a recipient of the IEEE Communications Society Technical Committee on Transmission Access and Optical Systems (TAOS) Best Paper Award in 2019, the ICC 2019 Best Paper Award, and the Best Paper Award of IEEE INTERNET OF THINGS JOURNAL in 2022.

<!-- image-->

Shuang Qin (Senior Member, IEEE) received the B.E. degree in electronic information science and technology and the Ph.D. degree in communication and information systems from the University of Electronic Science and Technology of China (UESTC) in 2006 and 2012, respectively. He is currently a Professor with the National Key Laboratory of Science and Technology on Communications, UESTC. His research interests include cooperative communication in wireless networks, data transmission in opportunistic networks, and green

communication in heterogeneous networks.

<!-- image-->

Youkun Peng received the bachelorâs degree in network engineering from the School of Information and Communication Engineering, University of Electronic Science and Technology of China. He is currently pursuing the Ph.D. degree with the National Key Laboratory of Wireless Communications, University of Electronic Science and Technology of China. His current research interests include resource allocation in wireless networks, non-terrestrial networks, and machine learning for wireless communications.

<!-- image-->

Yijing Liu (Member, IEEE) received the B.S. degree from the College of Communication and Information Engineering, Chongqing University of Posts and Telecommunications, in 2017, and the Ph.D. degree from the National Key Laboratory of Wireless Communications, University of Electronic Science and Technology of China, Chengdu, China, in 2023. She is currently a Post-Doctoral Researcher with the University of Electronic Science and Technology of China. Her current research interests include wireless networking, distributed and collaborative machine learning, and edge AI. She was awarded the Fellowship of China National Postdoctoral Program for Innovative Talents in 2023.

---



## 📷 Images

The following images were extracted from this PDF:

1. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_1.png|page_12_img_1]]
2. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_2.png|page_12_img_2]]
3. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_3.png|page_12_img_3]]
4. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_4.png|page_12_img_4]]
5. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_5.png|page_12_img_5]]
6. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_6.png|page_12_img_6]]
7. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_7.png|page_12_img_7]]
8. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_8.png|page_12_img_8]]
9. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_12_img_9.png|page_12_img_9]]
10. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_14_img_1.png|page_14_img_1]]
11. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_14_img_2.png|page_14_img_2]]
12. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_14_img_3.png|page_14_img_3]]
13. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_14_img_4.png|page_14_img_4]]
14. [[../extracted_images/Wei 等 - 2024 - Hierarchical Network Slicing for UAV-Assisted Wireless Networks With Deployment Optimization/page_14_img_5.png|page_14_img_5]]

---

